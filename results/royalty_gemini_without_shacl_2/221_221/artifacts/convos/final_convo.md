================================ System Message ================================

### Role
You are an expert Knowledge Graph Engineer. Your task is to update and refine a Data Graph based on a provided Input Text and a strict Ontology. You must ensure the Data Graph accurately reflects the information in the text while remaining compliant with the ontological constraints.

### Inputs
1. **Ontology**: Allowed classes and properties.
2. **Input Text**: The ONLY source of truth.
3. **Current Data Graph**: The starting state.

### Strict Grounding & Scope
- **No External Knowledge**: You are a "clean slate" engineer. Even if you know more about the subject from your training data, you MUST NOT add any node or relation that is not explicitly mentioned in the **Input Text**.
- **No Hypothetical Nodes**: Do not create placeholder nodes or sequences (e.g., Marriage1, Marriage2) to represent "patterns" mentioned in the text. Only create nodes for specific instances described.
- **Quantities**: If the text says "fifteen children" but does not name them, do NOT create 15 generic child nodes. Only create nodes for entities with specific names or identifiers provided in the text.

### Triadic Directionality & Predicate Logic (STRICT ENFORCEMENT)
The Data Graph is a **Directed Acyclic Graph**. Swapping Source and Target is a critical failure that invalidates the entire graph. You MUST follow the **Flow of Action**.

#### 1. The "Sentence Test" Requirement
Before executing any `AddTriple` call, you must mentally or explicitly (in your thought process) perform the following test:
* **Formula**: `[Source Entity] + [Property Name] + [Target Entity]`
* **Check**: Does this form a grammatically and logically correct sentence based *only* on the text?
* **Example Failure**: If the text says "John is the employer of Mary," the triple `(Mary, isEmployerOf, John)` fails because "Mary isEmployerOf John" is factually false.

#### 2. Identifying the Anchor (Domain vs. Range)
* **The Source**: The "Origin" or "Owner." If the property is a verb, the Source is the one performing it. Source is always to the left of a relation.
* **The Target**: The "Destination" or "Attribute." If the property is a verb, the Target is the one being acted upon. Target is always to the right of a relation.

#### 3. Handling Inverse Property Confusion
Many errors occur because the LLM confuses a relation with its inverse. You must be hyper-vigilant:
* **Active (`worksFor`, `isEmployerOf`)**: The "Superior" or "Source" is the Source.
* **Passive (`employedBy`, `childOf`)**: The "Subordinate" or "Recipient" is the Source.
* **Partitive (`hasPart`, `contains`)**: The "Container/Whole" is the Source.
* **Membership (`isPartOf`, `memberOf`)**: The "Component/Part" is the Source.

#### 4. Negative Constraints
* **NEVER** use the property name as a bidirectional link.
* **NEVER** assume the first entity mentioned in a sentence is automatically the Source; analyze the verb direction.

#### 5. Arguments Order
* When calling `AddTriple` `source` **ALWAYS** comes first, then `relation`, and only after them `target`.

> **STOP & VERIFY**: If your triple reads like "Employee isEmployerOf Employer" or "Room contains Building," you have flipped the nodes. **STOP and swap them before calling the tool.**


### Naming Conventions
- **Identifiers**: Use semantic identifiers derived from the text. 
- **Avoid Numbering**: Do not use arbitrary numbers unless that specific number appears in the text in relation to that entity.
- **Inclusion of Titles**: Retain all regnal numbers, honorary prefixes, or noble titles if they are part of the primary identifying name (e.g., "Crown Prince [Name]" or "[Name] II").
- **Territorial Origins**: If a person is identified by their house, dynasty, or place of origin as part of their formal name, include the full "of [Location]" or "[Location-Suffix]" descriptor.
- **Avoid Pronouns/Aliases**: Never use pronouns or shortened versions of the name mentioned later in the text. Always map back to the most complete version of the name found within the source material.

### Instructions & Workflow
1. **Analyze**: Identify specific entities and relations in the text.
2. **Edit**: Use tools to modify the graph.
   - Every node MUST have a class assignment (`AssignClass`).
   - Ground every edit in text evidence.
3. **Finalize**: Use `Finish` once the graph is a **faithful** representation of the text.

### Tool Usage Constraints
- **AssignClass / UnassignClass**: For `rdf:type` only.
- **AddTriple / RemoveTriple**: For properties only.
- **AddLiteral / RemoveLiteral**: For literals (raw data: dates, numbers, strings, etc.) only.
- **Finish**: Once you are finished, use this tool.
- **Batching**: You may use multiple tools, but **DON'T EXCEED 20 TOOL CALLS IN A SINGLE ANSWER**. Focus on quality and grounding over quantity.

================================ Human Message =================================

Please update the Knowledge Graph based on the provided data.

### Input Text:
Anne Ferelith Fenella Bowes-Lyon (4 December 1917 – 26 September 1980), later styled Viscountess Anson and later Princess Anne of Denmark, was a British noblewoman and member of the Danish royal family by marriage, and a first cousin of Elizabeth II.
Born into the Bowes-Lyon family, she married Thomas Anson, Viscount Anson, and had two children, Patrick Anson, 5th Earl of Lichfield, and Lady Elizabeth Shakerley, before divorcing Anson in 1948.
She became a princess of Denmark by her second marriage to Prince Georg of Denmark in 1950.
Family

Anne Bowes-Lyon was born in Washington, D.C., in 1917.
John Herbert Bowes-Lyon and her mother was the Hon.
Fenella Hepburn-Stuart-Forbes-Trefusis, daughter of Charles Hepburn-Stuart-Forbes-Trefusis, 21st Baron Clinton.
Anne's paternal grandfather was Claude Bowes-Lyon, 14th
Earl of Strathmore and Kinghorne.
She was a niece of Queen Elizabeth the Queen Mother.
Anne had three younger sisters, two of whom were Nerissa and Katherine Bowes-Lyon, who were institutionalized in 1941 for severe intellectual disability.
Apart from early deceased Patricia (1916–1917), Nerissa (1919–1986) and Katherine (1926–2014), Anne also had one younger sister, Diana Cinderella Somervell (1923–1986).
Marriages

Anne married Lieutenant-Colonel Thomas William Arnold Anson (1913–1958) on 28 April 1938.
As her husband held the courtesy title of Viscount Anson, Anne was styled Viscountess Anson upon their marriage.
On 16 September 1950, at Glamis Castle, Anne, Viscountess Anson subsequently married Prince Georg of Denmark, upon which she became Her Highness Princess Anne of Denmark.
Death

Anne died in 1980, aged 62, in London of a heart attack.
She is buried alongside her second husband, Prince George of Denmark, at Bernstorffpark, Gentofte, Denmark.



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix ns1: <http://www.w3.org/2003/11/swrl#> .
@prefix ns2: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

: a owl:Ontology ;
    dcterms:source <http://www.co-ode.org/roberts/family-tree.owl> .

:alsoKnownAs a owl:AnnotationProperty .

:formerlyKnownAs a owl:AnnotationProperty .

:hasBirthYear a rdfs:Datatype,
        owl:AnnotationProperty .

:hasDeathYear a owl:AnnotationProperty .

:hasMarriageYear a owl:AnnotationProperty .

:isAuntOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    owl:propertyChainAxiom ( :isSisterOf :isParentOf ) .

:isUncleOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Person ;
    owl:propertyChainAxiom ( :isBrotherOf :isParentOf ) .

:knownAs a owl:AnnotationProperty .

dcterms:source a owl:AnnotationProperty .

ns2:isRuleEnabled a owl:AnnotationProperty .

:hasBrother a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Man ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:inverseOf :isBrotherOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:hasDaughter a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Woman ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf ;
    owl:inverseOf :isDaughterOf .

:hasFather a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Man ;
    rdfs:subPropertyOf :hasParent ;
    owl:inverseOf :isFatherOf .

:hasMother a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Woman ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf ;
    owl:inverseOf :isMotherOf .

:hasSister a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Woman ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:inverseOf :isSisterOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:hasSon a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Man ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf ;
    owl:inverseOf :isSonOf .

:isBloodrelationOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation,
        owl:topObjectProperty .

:isDaughterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf .

:isFatherOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor,
        :Man ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf .

:isMotherOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor,
        :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf .

:isSonOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf .

:DomainEntity a owl:Class .

:Female a owl:Class ;
    rdfs:subClassOf :Sex ;
    owl:disjointWith :Male .

:hasAncestor a owl:ObjectProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasRelation,
        owl:topObjectProperty ;
    owl:inverseOf :isAncestorOf .

:isBrotherOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:Male a owl:Class ;
    rdfs:subClassOf :Sex .

:hasRelation a owl:ObjectProperty,
        owl:SymmetricProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person .

:hasSex a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Sex .

:isAncestorOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation .

:isSisterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf .

:hasChild a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:inverseOf :isChildOf .

:hasParent a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Person ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:equivalentProperty :isChildOf ;
    owl:inverseOf :isParentOf .

:isSiblingOf a owl:ObjectProperty,
        owl:SymmetricProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isBloodrelationOf ;
    owl:propertyChainAxiom ( :hasParent :isParentOf ) .

:Sex a owl:Class ;
    rdfs:subClassOf :DomainEntity ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Female :Male ) ] .

:isChildOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:propertyDisjointWith :isSisterOf .

:x a ns1:Variable .

:Man a owl:Class ;
    owl:disjointWith :Sex,
        :Woman ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Male ] ) ] .

:isParentOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:propertyDisjointWith :isSisterOf .

:Woman a owl:Class ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Female ] ) ] .

:y a ns1:Variable .

:Ancestor a owl:Class ;
    owl:disjointWith :Sex ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :isAncestorOf ;
                        owl:someValuesFrom :Person ] ) ] .

:Person a owl:Class ;
    rdfs:subClassOf [ a owl:Restriction ;
            owl:onProperty :hasFather ;
            owl:someValuesFrom :Man ],
        [ a owl:Restriction ;
            owl:onProperty :hasMother ;
            owl:someValuesFrom :Woman ],
        [ a owl:Restriction ;
            owl:onProperty :hasSex ;
            owl:someValuesFrom :Sex ],
        [ a owl:Restriction ;
            owl:maxQualifiedCardinality "2"^^xsd:nonNegativeInteger ;
            owl:onClass :Person ;
            owl:onProperty :hasParent ],
        :DomainEntity ;
    owl:disjointWith :Sex ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Man :Woman ) ] .

[] a ns1:Imp ;
    rdfs:label "infer hasSon" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasBrother" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasSister" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (b3eabebc-38da-4a72-b710-d8724eadb842)
 Call ID: b3eabebc-38da-4a72-b710-d8724eadb842
  Args:
    source: Anne_Bowes-Lyon
    type: :Woman
  AssignClass (b0df40fb-362d-484d-a0b4-bdae5baa5b52)
 Call ID: b0df40fb-362d-484d-a0b4-bdae5baa5b52
  Args:
    source: Anne_Bowes-Lyon
    type: :Person
  AddLiteral (b0d5c124-f331-4163-9f3a-db92b48512ac)
 Call ID: b0d5c124-f331-4163-9f3a-db92b48512ac
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1917
    source: Anne_Bowes-Lyon
  AddLiteral (01e2e5fc-274e-46c4-afca-2d5d31ac0e5f)
 Call ID: 01e2e5fc-274e-46c4-afca-2d5d31ac0e5f
  Args:
    literal_type: xsd:integer
    literal_value: 1980
    source: Anne_Bowes-Lyon
    relation: :hasDeathYear
  AssignClass (56154ff4-a60e-48de-a43b-64849358be90)
 Call ID: 56154ff4-a60e-48de-a43b-64849358be90
  Args:
    type: :Man
    source: John_Herbert_Bowes-Lyon
  AssignClass (da162b25-cad4-48a7-a1cb-0c8ccc82c494)
 Call ID: da162b25-cad4-48a7-a1cb-0c8ccc82c494
  Args:
    type: :Person
    source: John_Herbert_Bowes-Lyon
  AddTriple (d71e5d9b-035c-44b8-a0bf-30554da92a8c)
 Call ID: d71e5d9b-035c-44b8-a0bf-30554da92a8c
  Args:
    relation: :hasFather
    source: Anne_Bowes-Lyon
    target: John_Herbert_Bowes-Lyon
  AssignClass (2dae2a2b-def4-4a61-be94-62f00b1a815a)
 Call ID: 2dae2a2b-def4-4a61-be94-62f00b1a815a
  Args:
    type: :Woman
    source: Fenella_Hepburn-Stuart-Forbes-Trefusis
  AssignClass (ce4e9e8a-da1b-49b3-83af-0273e9639367)
 Call ID: ce4e9e8a-da1b-49b3-83af-0273e9639367
  Args:
    source: Fenella_Hepburn-Stuart-Forbes-Trefusis
    type: :Person
  AddTriple (33b42d62-102e-478c-8eae-535f71ddfdc7)
 Call ID: 33b42d62-102e-478c-8eae-535f71ddfdc7
  Args:
    relation: :hasMother
    target: Fenella_Hepburn-Stuart-Forbes-Trefusis
    source: Anne_Bowes-Lyon
  AssignClass (d936a052-799c-4290-b993-358486aeb991)
 Call ID: d936a052-799c-4290-b993-358486aeb991
  Args:
    source: Charles_Hepburn-Stuart-Forbes-Trefusis
    type: :Man
  AssignClass (15934f04-8256-4c6d-8d6d-22d5abe8a185)
 Call ID: 15934f04-8256-4c6d-8d6d-22d5abe8a185
  Args:
    source: Charles_Hepburn-Stuart-Forbes-Trefusis
    type: :Person
  AddTriple (b25e7551-5c53-4493-98dc-d9d752b9525c)
 Call ID: b25e7551-5c53-4493-98dc-d9d752b9525c
  Args:
    relation: :isFatherOf
    source: Charles_Hepburn-Stuart-Forbes-Trefusis
    target: Fenella_Hepburn-Stuart-Forbes-Trefusis
  AssignClass (e07fe455-aa23-4f15-bbf3-651a979e94ac)
 Call ID: e07fe455-aa23-4f15-bbf3-651a979e94ac
  Args:
    type: :Man
    source: Claude_Bowes-Lyon
  AssignClass (b3bef068-bb23-4781-b948-ab9073426b47)
 Call ID: b3bef068-bb23-4781-b948-ab9073426b47
  Args:
    source: Claude_Bowes-Lyon
    type: :Person
  AddTriple (5409652f-b336-4417-9a76-c4ed3cbf0ac3)
 Call ID: 5409652f-b336-4417-9a76-c4ed3cbf0ac3
  Args:
    relation: :isFatherOf
    target: John_Herbert_Bowes-Lyon
    source: Claude_Bowes-Lyon
  AssignClass (76d9e10e-8ad4-4f61-ac8c-28828a609432)
 Call ID: 76d9e10e-8ad4-4f61-ac8c-28828a609432
  Args:
    type: :Man
    source: Patrick_Anson
  AssignClass (0237d6c6-1209-49bd-b958-d1a6ab64ea12)
 Call ID: 0237d6c6-1209-49bd-b958-d1a6ab64ea12
  Args:
    type: :Person
    source: Patrick_Anson
  AddTriple (3d6c7d74-230a-436d-ba77-2e5b8971940c)
 Call ID: 3d6c7d74-230a-436d-ba77-2e5b8971940c
  Args:
    relation: :hasSon
    target: Patrick_Anson
    source: Anne_Bowes-Lyon
  AssignClass (90892662-09a6-4ae1-bdff-627131e35c31)
 Call ID: 90892662-09a6-4ae1-bdff-627131e35c31
  Args:
    type: :Woman
    source: Elizabeth_Shakerley
  AssignClass (25cf1799-fd21-4de0-878d-752754ad71c5)
 Call ID: 25cf1799-fd21-4de0-878d-752754ad71c5
  Args:
    source: Elizabeth_Shakerley
    type: :Person
  AddTriple (a3b037bc-75ae-41a6-83ac-585ef8289e96)
 Call ID: a3b037bc-75ae-41a6-83ac-585ef8289e96
  Args:
    target: Elizabeth_Shakerley
    source: Anne_Bowes-Lyon
    relation: :hasDaughter
  AssignClass (6fe1b6d0-f41f-4729-a143-5f6428db1843)
 Call ID: 6fe1b6d0-f41f-4729-a143-5f6428db1843
  Args:
    type: :Man
    source: Thomas_Anson
  AssignClass (0ea30618-f99d-4e53-91f9-73963a4b17a0)
 Call ID: 0ea30618-f99d-4e53-91f9-73963a4b17a0
  Args:
    source: Thomas_Anson
    type: :Person
  AddTriple (0f6db7ab-abeb-4685-ad96-353b4c6f3a60)
 Call ID: 0f6db7ab-abeb-4685-ad96-353b4c6f3a60
  Args:
    target: Patrick_Anson
    source: Thomas_Anson
    relation: :isFatherOf
  AddTriple (203be11a-a82a-4702-a6bb-5a8708043120)
 Call ID: 203be11a-a82a-4702-a6bb-5a8708043120
  Args:
    relation: :isFatherOf
    source: Thomas_Anson
    target: Elizabeth_Shakerley
  AddLiteral (e3dca55c-8378-42c3-8a53-fea15ab2a9c4)
 Call ID: e3dca55c-8378-42c3-8a53-fea15ab2a9c4
  Args:
    relation: :hasMarriageYear
    literal_value: 1938
    source: Anne_Bowes-Lyon
    literal_type: xsd:integer
  AssignClass (f1961309-97be-477d-b3d9-defaaad78dfc)
 Call ID: f1961309-97be-477d-b3d9-defaaad78dfc
  Args:
    type: :Man
    source: Prince_Georg_of_Denmark
  AssignClass (b51ac727-6cb2-4d93-8296-1992f02f43cb)
 Call ID: b51ac727-6cb2-4d93-8296-1992f02f43cb
  Args:
    type: :Person
    source: Prince_Georg_of_Denmark
  AddLiteral (c45cb5d1-5dc9-4211-9392-04ac12566632)
 Call ID: c45cb5d1-5dc9-4211-9392-04ac12566632
  Args:
    literal_value: 1950
    source: Anne_Bowes-Lyon
    relation: :hasMarriageYear
    literal_type: xsd:integer
  AssignClass (a878ec14-5b15-45dd-adc1-72b6ba930d1f)
 Call ID: a878ec14-5b15-45dd-adc1-72b6ba930d1f
  Args:
    type: :Woman
    source: Patricia_Bowes-Lyon
  AssignClass (1631da96-b5c3-4c2d-b7f1-55275e481d95)
 Call ID: 1631da96-b5c3-4c2d-b7f1-55275e481d95
  Args:
    source: Patricia_Bowes-Lyon
    type: :Person
  AddTriple (0b0fea32-100a-47fd-af0e-41a429c39e2c)
 Call ID: 0b0fea32-100a-47fd-af0e-41a429c39e2c
  Args:
    target: Patricia_Bowes-Lyon
    source: Anne_Bowes-Lyon
    relation: :isSiblingOf
  AssignClass (a4b0e6b6-43b0-4939-ac2b-07aaecc645e4)
 Call ID: a4b0e6b6-43b0-4939-ac2b-07aaecc645e4
  Args:
    type: :Woman
    source: Nerissa_Bowes-Lyon
  AssignClass (a6da3b83-58fe-4e37-9766-5275fdded01d)
 Call ID: a6da3b83-58fe-4e37-9766-5275fdded01d
  Args:
    type: :Person
    source: Nerissa_Bowes-Lyon
  AddTriple (0c4b79ce-6377-4199-ab09-cd9a3f85c7d5)
 Call ID: 0c4b79ce-6377-4199-ab09-cd9a3f85c7d5
  Args:
    relation: :isSiblingOf
    target: Nerissa_Bowes-Lyon
    source: Anne_Bowes-Lyon
  AssignClass (25505bbb-16a2-4f3a-9fd7-f407e55c259d)
 Call ID: 25505bbb-16a2-4f3a-9fd7-f407e55c259d
  Args:
    source: Katherine_Bowes-Lyon
    type: :Woman
  AssignClass (a303e407-b21c-48ab-b99f-641846d6ec5a)
 Call ID: a303e407-b21c-48ab-b99f-641846d6ec5a
  Args:
    source: Katherine_Bowes-Lyon
    type: :Person
  AddTriple (b0b676b0-8b04-4928-97e3-ef7218c0dc55)
 Call ID: b0b676b0-8b04-4928-97e3-ef7218c0dc55
  Args:
    source: Anne_Bowes-Lyon
    target: Katherine_Bowes-Lyon
    relation: :isSiblingOf
  AssignClass (7c48404e-7a25-4015-9f9b-8b2f318f1275)
 Call ID: 7c48404e-7a25-4015-9f9b-8b2f318f1275
  Args:
    source: Diana_Cinderella_Somervell
    type: :Woman
  AssignClass (2a614b59-c1f2-493b-80da-92bd290d349e)
 Call ID: 2a614b59-c1f2-493b-80da-92bd290d349e
  Args:
    source: Diana_Cinderella_Somervell
    type: :Person
  AddTriple (40ffee35-2e70-4f06-aebc-537ddf28c7b8)
 Call ID: 40ffee35-2e70-4f06-aebc-537ddf28c7b8
  Args:
    relation: :isSiblingOf
    target: Diana_Cinderella_Somervell
    source: Anne_Bowes-Lyon
  Finish (8e4b1ebb-4b8e-4094-9760-5a1c8dfd4847)
 Call ID: 8e4b1ebb-4b8e-4094-9760-5a1c8dfd4847
  Args: