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
  AssignClass (5f5e763b-27ac-4352-a249-97f0ca2eaae7)
 Call ID: 5f5e763b-27ac-4352-a249-97f0ca2eaae7
  Args:
    source: :Anne_Bowes-Lyon
    type: :Person
  AssignClass (bf2b19a5-b845-414b-8255-ddbdd8c3b8ab)
 Call ID: bf2b19a5-b845-414b-8255-ddbdd8c3b8ab
  Args:
    type: :Woman
    source: :Anne_Bowes-Lyon
  AddLiteral (dd79eeb1-60cf-4183-8819-fd3f6c15812f)
 Call ID: dd79eeb1-60cf-4183-8819-fd3f6c15812f
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: :Anne_Bowes-Lyon
    literal_value: 1917
  AddLiteral (eeae8d04-97d3-443e-b1ef-3ac860833d4a)
 Call ID: eeae8d04-97d3-443e-b1ef-3ac860833d4a
  Args:
    literal_value: 1980
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: :Anne_Bowes-Lyon
  AddLiteral (7fcefea0-2a15-4a9f-bde4-e1ccd196c9ae)
 Call ID: 7fcefea0-2a15-4a9f-bde4-e1ccd196c9ae
  Args:
    literal_value: Anne Ferelith Fenella Bowes-Lyon
    source: :Anne_Bowes-Lyon
    literal_type: xsd:string
    relation: :knownAs
  AddLiteral (94fa914e-4124-417e-a105-88d7bfaf3658)
 Call ID: 94fa914e-4124-417e-a105-88d7bfaf3658
  Args:
    literal_value: Viscountess Anson
    relation: :alsoKnownAs
    literal_type: xsd:string
    source: :Anne_Bowes-Lyon
  AddLiteral (a6ec4374-bd97-46f5-bf62-436239d6ec9e)
 Call ID: a6ec4374-bd97-46f5-bf62-436239d6ec9e
  Args:
    literal_value: Princess Anne of Denmark
    relation: :alsoKnownAs
    source: :Anne_Bowes-Lyon
    literal_type: xsd:string
  AssignClass (5db58b5f-44b7-44e4-8fc2-59a7c0773fe6)
 Call ID: 5db58b5f-44b7-44e4-8fc2-59a7c0773fe6
  Args:
    source: :Thomas_Anson
    type: :Person
  AssignClass (a8d67f23-5361-49a7-805d-31c79f80040d)
 Call ID: a8d67f23-5361-49a7-805d-31c79f80040d
  Args:
    source: :Thomas_Anson
    type: :Man
  AddLiteral (66dc2c85-976b-4909-acee-a661895d1048)
 Call ID: 66dc2c85-976b-4909-acee-a661895d1048
  Args:
    source: :Anne_Bowes-Lyon
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 1938
  AddTriple (c5cf877d-1b41-496c-834c-05e361f480f7)
 Call ID: c5cf877d-1b41-496c-834c-05e361f480f7
  Args:
    source: :Anne_Bowes-Lyon
    target: :Thomas_Anson
    relation: :hasRelation
  AssignClass (255b6e24-7b5f-46e4-9b0b-ec4fd3c1c3cf)
 Call ID: 255b6e24-7b5f-46e4-9b0b-ec4fd3c1c3cf
  Args:
    source: :Prince_Georg_of_Denmark
    type: :Person
  AssignClass (e67dab6f-2eba-4cfb-90f8-0120847bb05d)
 Call ID: e67dab6f-2eba-4cfb-90f8-0120847bb05d
  Args:
    source: :Prince_Georg_of_Denmark
    type: :Man
  AddLiteral (f7fb88dd-92b8-4590-908b-90ccfb5be2a6)
 Call ID: f7fb88dd-92b8-4590-908b-90ccfb5be2a6
  Args:
    source: :Anne_Bowes-Lyon
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 1950
  AddTriple (7566b95a-0edb-4df8-98b4-3a53be8d62e0)
 Call ID: 7566b95a-0edb-4df8-98b4-3a53be8d62e0
  Args:
    target: :Prince_Georg_of_Denmark
    source: :Anne_Bowes-Lyon
    relation: :hasRelation
  AssignClass (d9997154-3187-4b7f-b4ae-cd7fea6f109b)
 Call ID: d9997154-3187-4b7f-b4ae-cd7fea6f109b
  Args:
    source: :Patrick_Anson
    type: :Person
  AssignClass (d9762fe4-3df2-4afc-be68-a2d0edc42ab1)
 Call ID: d9762fe4-3df2-4afc-be68-a2d0edc42ab1
  Args:
    type: :Man
    source: :Patrick_Anson
  AddTriple (54df5e72-d8d4-4ae5-815e-a1f2c41628d5)
 Call ID: 54df5e72-d8d4-4ae5-815e-a1f2c41628d5
  Args:
    relation: :isChildOf
    target: :Anne_Bowes-Lyon
    source: :Patrick_Anson
  AssignClass (e09d1fdf-5ec2-40f1-845e-1ec61a9a26cc)
 Call ID: e09d1fdf-5ec2-40f1-845e-1ec61a9a26cc
  Args:
    source: :Lady_Elizabeth_Shakerley
    type: :Person
  AssignClass (ff1139cf-04f0-4cf8-bac7-2e9a68dbc605)
 Call ID: ff1139cf-04f0-4cf8-bac7-2e9a68dbc605
  Args:
    type: :Woman
    source: :Lady_Elizabeth_Shakerley
  AddTriple (38954f3b-6522-4956-a68d-a39e05391257)
 Call ID: 38954f3b-6522-4956-a68d-a39e05391257
  Args:
    source: :Lady_Elizabeth_Shakerley
    target: :Anne_Bowes-Lyon
    relation: :isChildOf
  AssignClass (c58dfb23-edf5-4fab-b4b7-20c2db41fec3)
 Call ID: c58dfb23-edf5-4fab-b4b7-20c2db41fec3
  Args:
    type: :Person
    source: :John_Herbert_Bowes-Lyon
  AssignClass (bbeed955-533a-457a-8821-5006ed483085)
 Call ID: bbeed955-533a-457a-8821-5006ed483085
  Args:
    type: :Man
    source: :John_Herbert_Bowes-Lyon
  AddTriple (06b4c3e3-b533-47cd-af99-18aa51eac7ac)
 Call ID: 06b4c3e3-b533-47cd-af99-18aa51eac7ac
  Args:
    relation: :hasFather
    source: :Anne_Bowes-Lyon
    target: :John_Herbert_Bowes-Lyon
  AssignClass (f0538555-53d7-4005-b1fb-b4eb902d500b)
 Call ID: f0538555-53d7-4005-b1fb-b4eb902d500b
  Args:
    source: :Fenella_Hepburn-Stuart-Forbes-Trefusis
    type: :Person
  AssignClass (c98fa70c-721f-4891-8405-ea3a88640c52)
 Call ID: c98fa70c-721f-4891-8405-ea3a88640c52
  Args:
    source: :Fenella_Hepburn-Stuart-Forbes-Trefusis
    type: :Woman
  AddTriple (7a7543c4-b017-4ffb-98d7-10ec9cd17152)
 Call ID: 7a7543c4-b017-4ffb-98d7-10ec9cd17152
  Args:
    relation: :hasMother
    target: :Fenella_Hepburn-Stuart-Forbes-Trefusis
    source: :Anne_Bowes-Lyon
  AssignClass (65638507-6785-4637-95d2-d44529c9159b)
 Call ID: 65638507-6785-4637-95d2-d44529c9159b
  Args:
    type: :Person
    source: :Charles_Hepburn-Stuart-Forbes-Trefusis
  AssignClass (4be02497-c621-4e9b-9854-f18fe767c063)
 Call ID: 4be02497-c621-4e9b-9854-f18fe767c063
  Args:
    source: :Charles_Hepburn-Stuart-Forbes-Trefusis
    type: :Man
  AddTriple (369d47e8-bf0d-4773-ac3b-181391d6c9b0)
 Call ID: 369d47e8-bf0d-4773-ac3b-181391d6c9b0
  Args:
    target: :Fenella_Hepburn-Stuart-Forbes-Trefusis
    source: :Charles_Hepburn-Stuart-Forbes-Trefusis
    relation: :isFatherOf
  AssignClass (ccecac0d-46b0-4cb9-924a-00da40a8b9aa)
 Call ID: ccecac0d-46b0-4cb9-924a-00da40a8b9aa
  Args:
    source: :Claude_Bowes-Lyon
    type: :Person
  AssignClass (583aa195-5200-4407-913e-ac5258787c18)
 Call ID: 583aa195-5200-4407-913e-ac5258787c18
  Args:
    type: :Man
    source: :Claude_Bowes-Lyon
  AddTriple (3861edf6-9814-4331-8392-b05888d518d9)
 Call ID: 3861edf6-9814-4331-8392-b05888d518d9
  Args:
    relation: :isFatherOf
    target: :John_Herbert_Bowes-Lyon
    source: :Claude_Bowes-Lyon
  AssignClass (2e090995-f3c9-4af0-99c9-e9f9f82bd5ee)
 Call ID: 2e090995-f3c9-4af0-99c9-e9f9f82bd5ee
  Args:
    source: :Nerissa_Bowes-Lyon
    type: :Person
  AssignClass (7f7f4135-2e4f-4c8f-9135-4d69c9e157b1)
 Call ID: 7f7f4135-2e4f-4c8f-9135-4d69c9e157b1
  Args:
    type: :Woman
    source: :Nerissa_Bowes-Lyon
  AddTriple (1248ffd8-9605-43a9-9936-96ce65a228b6)
 Call ID: 1248ffd8-9605-43a9-9936-96ce65a228b6
  Args:
    relation: :isSiblingOf
    source: :Anne_Bowes-Lyon
    target: :Nerissa_Bowes-Lyon
  AssignClass (05b1ca4b-45d9-44f6-a8dd-f43b3696d86c)
 Call ID: 05b1ca4b-45d9-44f6-a8dd-f43b3696d86c
  Args:
    source: :Katherine_Bowes-Lyon
    type: :Person
  AssignClass (7df49794-a59a-4a1f-8878-67934d257262)
 Call ID: 7df49794-a59a-4a1f-8878-67934d257262
  Args:
    type: :Woman
    source: :Katherine_Bowes-Lyon
  AddTriple (7c98f879-ac08-44c7-9e4d-0312f2904fea)
 Call ID: 7c98f879-ac08-44c7-9e4d-0312f2904fea
  Args:
    source: :Anne_Bowes-Lyon
    target: :Katherine_Bowes-Lyon
    relation: :isSiblingOf
  AssignClass (ee95c1a7-27f5-40d8-a17a-d1c7c89121ee)
 Call ID: ee95c1a7-27f5-40d8-a17a-d1c7c89121ee
  Args:
    source: :Patricia_Bowes-Lyon
    type: :Person
  AssignClass (fc50aaa5-8521-4e93-84e3-aefe11f51fc0)
 Call ID: fc50aaa5-8521-4e93-84e3-aefe11f51fc0
  Args:
    type: :Woman
    source: :Patricia_Bowes-Lyon
  AddTriple (cfb4dfe5-3db1-44e1-b662-9808a05e6e96)
 Call ID: cfb4dfe5-3db1-44e1-b662-9808a05e6e96
  Args:
    relation: :isSiblingOf
    source: :Anne_Bowes-Lyon
    target: :Patricia_Bowes-Lyon
  AssignClass (f60efc5e-9aef-4d47-b94e-47064c3ff5f5)
 Call ID: f60efc5e-9aef-4d47-b94e-47064c3ff5f5
  Args:
    source: :Diana_Cinderella_Somervell
    type: :Person
  AssignClass (1cae9c5f-92cc-4093-bc31-0bf9de404a10)
 Call ID: 1cae9c5f-92cc-4093-bc31-0bf9de404a10
  Args:
    type: :Woman
    source: :Diana_Cinderella_Somervell
  AddTriple (5cae838c-ffba-46b0-93d4-7e9f336eac9e)
 Call ID: 5cae838c-ffba-46b0-93d4-7e9f336eac9e
  Args:
    source: :Anne_Bowes-Lyon
    target: :Diana_Cinderella_Somervell
    relation: :isSiblingOf
  Finish (1b0ac230-a653-4ffd-8e83-327eb5db0ade)
 Call ID: 1b0ac230-a653-4ffd-8e83-327eb5db0ade
  Args: