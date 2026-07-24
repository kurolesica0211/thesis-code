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
  AssignClass (15cf7d25-db76-43fe-94cc-41a1c3ddbb07)
 Call ID: 15cf7d25-db76-43fe-94cc-41a1c3ddbb07
  Args:
    source: :Anne_Bowes-Lyon
    type: :Person
  AssignClass (24b26b8e-eaed-47f3-aab0-75b751a65d16)
 Call ID: 24b26b8e-eaed-47f3-aab0-75b751a65d16
  Args:
    type: :Woman
    source: :Anne_Bowes-Lyon
  AddLiteral (faf86b93-4629-40ac-a9b4-275fe6318179)
 Call ID: faf86b93-4629-40ac-a9b4-275fe6318179
  Args:
    literal_type: xsd:nonNegativeInteger
    relation: :hasBirthYear
    source: :Anne_Bowes-Lyon
    literal_value: 1917
  AddLiteral (24679919-bc89-4b1a-851a-8324edd0c840)
 Call ID: 24679919-bc89-4b1a-851a-8324edd0c840
  Args:
    literal_type: xsd:nonNegativeInteger
    relation: :hasDeathYear
    source: :Anne_Bowes-Lyon
    literal_value: 1980
  AddTriple (2adc4704-a107-4601-abd3-0d21313c49d4)
 Call ID: 2adc4704-a107-4601-abd3-0d21313c49d4
  Args:
    source: :Anne_Bowes-Lyon
    target: :John_Herbert_Bowes-Lyon
    relation: :hasFather
  AddTriple (85a35dba-9c5c-48dc-bb6d-0d474af3ca8a)
 Call ID: 85a35dba-9c5c-48dc-bb6d-0d474af3ca8a
  Args:
    source: :Anne_Bowes-Lyon
    target: :Fenella_Hepburn-Stuart-Forbes-Trefusis
    relation: :hasMother
  AssignClass (f9501ada-ed99-49e6-b8da-21cb9f5b7717)
 Call ID: f9501ada-ed99-49e6-b8da-21cb9f5b7717
  Args:
    source: :John_Herbert_Bowes-Lyon
    type: :Person
  AssignClass (52f2683b-e5fa-4f23-9877-537593ccebae)
 Call ID: 52f2683b-e5fa-4f23-9877-537593ccebae
  Args:
    source: :John_Herbert_Bowes-Lyon
    type: :Man
  AssignClass (f2d8e0e0-6f0e-46c8-a66b-8dd1322d6961)
 Call ID: f2d8e0e0-6f0e-46c8-a66b-8dd1322d6961
  Args:
    type: :Person
    source: :Fenella_Hepburn-Stuart-Forbes-Trefusis
  AssignClass (37a2f809-7b43-4707-b4af-78204c3e31bf)
 Call ID: 37a2f809-7b43-4707-b4af-78204c3e31bf
  Args:
    source: :Fenella_Hepburn-Stuart-Forbes-Trefusis
    type: :Woman
  AddTriple (f952e80f-e0ba-4403-b68b-525e4ef1ab19)
 Call ID: f952e80f-e0ba-4403-b68b-525e4ef1ab19
  Args:
    target: :Charles_Hepburn-Stuart-Forbes-Trefusis
    source: :Fenella_Hepburn-Stuart-Forbes-Trefusis
    relation: :hasFather
  AssignClass (68387c98-fd63-4f2b-b38c-6329fe148c18)
 Call ID: 68387c98-fd63-4f2b-b38c-6329fe148c18
  Args:
    type: :Person
    source: :Charles_Hepburn-Stuart-Forbes-Trefusis
  AssignClass (b5eb52e0-2cea-4a42-a5b8-6be918e9d48d)
 Call ID: b5eb52e0-2cea-4a42-a5b8-6be918e9d48d
  Args:
    source: :Charles_Hepburn-Stuart-Forbes-Trefusis
    type: :Man
  AddTriple (8a59af57-ffa9-4b9c-a73d-93f45af5e878)
 Call ID: 8a59af57-ffa9-4b9c-a73d-93f45af5e878
  Args:
    relation: :hasFather
    target: :Claude_Bowes-Lyon
    source: :John_Herbert_Bowes-Lyon
  AssignClass (5fb61b1c-b391-49aa-b2ff-9b8e63bbf895)
 Call ID: 5fb61b1c-b391-49aa-b2ff-9b8e63bbf895
  Args:
    source: :Claude_Bowes-Lyon
    type: :Person
  AssignClass (906622b2-0d39-4c9f-a2fa-306cee7e85e9)
 Call ID: 906622b2-0d39-4c9f-a2fa-306cee7e85e9
  Args:
    type: :Man
    source: :Claude_Bowes-Lyon
  AddTriple (fbecf496-2d16-4846-afbc-7ab621c9d08b)
 Call ID: fbecf496-2d16-4846-afbc-7ab621c9d08b
  Args:
    target: :Patrick_Anson
    source: :Anne_Bowes-Lyon
    relation: :hasChild
  AddTriple (52f5b20b-102e-4883-8aa3-f191fa4c2adb)
 Call ID: 52f5b20b-102e-4883-8aa3-f191fa4c2adb
  Args:
    relation: :hasChild
    source: :Anne_Bowes-Lyon
    target: :Elizabeth_Shakerley
  AssignClass (21c93974-c29b-4c5a-9855-dc5455ea5dfa)
 Call ID: 21c93974-c29b-4c5a-9855-dc5455ea5dfa
  Args:
    type: :Person
    source: :Patrick_Anson
  AssignClass (8d20e8f1-decc-4653-866c-dab942eae093)
 Call ID: 8d20e8f1-decc-4653-866c-dab942eae093
  Args:
    source: :Patrick_Anson
    type: :Man
  AssignClass (4977d29c-66c6-4ce8-8607-547b643de4fa)
 Call ID: 4977d29c-66c6-4ce8-8607-547b643de4fa
  Args:
    type: :Person
    source: :Elizabeth_Shakerley
  AssignClass (8f9cf4ae-e33c-4a9e-b70d-f9bff71922ed)
 Call ID: 8f9cf4ae-e33c-4a9e-b70d-f9bff71922ed
  Args:
    source: :Elizabeth_Shakerley
    type: :Woman
  AddTriple (872bed9c-1e0d-48b1-98b7-eb58948fe1fc)
 Call ID: 872bed9c-1e0d-48b1-98b7-eb58948fe1fc
  Args:
    target: :Thomas_Anson
    source: :Patrick_Anson
    relation: :hasFather
  AddTriple (598d806e-bed2-4879-9be0-1fb4791dc862)
 Call ID: 598d806e-bed2-4879-9be0-1fb4791dc862
  Args:
    relation: :hasFather
    source: :Elizabeth_Shakerley
    target: :Thomas_Anson
  AssignClass (aaede3d1-035d-49c9-a0ed-9e4278049d50)
 Call ID: aaede3d1-035d-49c9-a0ed-9e4278049d50
  Args:
    type: :Person
    source: :Thomas_Anson
  AssignClass (7010f708-dbe5-4fb8-a9e7-7c11b0ce021a)
 Call ID: 7010f708-dbe5-4fb8-a9e7-7c11b0ce021a
  Args:
    source: :Thomas_Anson
    type: :Man
  AddLiteral (41b877bf-f13d-41fe-9e1d-99f600b825ea)
 Call ID: 41b877bf-f13d-41fe-9e1d-99f600b825ea
  Args:
    relation: :hasMarriageYear
    literal_type: xsd:nonNegativeInteger
    literal_value: 1938
    source: :Anne_Bowes-Lyon
  AddTriple (e881ae21-e8e5-4bce-85f3-91ac5d4301d1)
 Call ID: e881ae21-e8e5-4bce-85f3-91ac5d4301d1
  Args:
    source: :Anne_Bowes-Lyon
    target: :Thomas_Anson
    relation: :hasRelation
  AddTriple (c6951599-24e4-4c08-9ada-db165dec12bd)
 Call ID: c6951599-24e4-4c08-9ada-db165dec12bd
  Args:
    target: :Prince_Georg_of_Denmark
    source: :Anne_Bowes-Lyon
    relation: :hasRelation
  AssignClass (32eac6c7-92be-401d-97ad-97d4c29943bc)
 Call ID: 32eac6c7-92be-401d-97ad-97d4c29943bc
  Args:
    source: :Prince_Georg_of_Denmark
    type: :Person
  AssignClass (cb09f572-4a20-472c-9214-079092dfb26e)
 Call ID: cb09f572-4a20-472c-9214-079092dfb26e
  Args:
    source: :Prince_Georg_of_Denmark
    type: :Man
  AddLiteral (502caeea-c256-41a9-92c9-89ef6768cc02)
 Call ID: 502caeea-c256-41a9-92c9-89ef6768cc02
  Args:
    literal_value: 1950
    source: :Anne_Bowes-Lyon
    literal_type: xsd:nonNegativeInteger
    relation: :hasMarriageYear
  AddTriple (af852ff7-cb6b-49fc-ad21-e547ecd842a5)
 Call ID: af852ff7-cb6b-49fc-ad21-e547ecd842a5
  Args:
    target: :Anne_Bowes-Lyon
    source: :Nerissa_Bowes-Lyon
    relation: :isSisterOf
  AddTriple (304a8c22-0179-4fa8-a4b7-c4116217be5f)
 Call ID: 304a8c22-0179-4fa8-a4b7-c4116217be5f
  Args:
    relation: :isSisterOf
    target: :Anne_Bowes-Lyon
    source: :Katherine_Bowes-Lyon
  AddTriple (d6bb3911-b332-42c0-bea1-4c2ba95307d9)
 Call ID: d6bb3911-b332-42c0-bea1-4c2ba95307d9
  Args:
    relation: :isSisterOf
    source: :Patricia_Bowes-Lyon
    target: :Anne_Bowes-Lyon
  AddTriple (72b8e9ff-02be-4512-ad6f-362deede6d0e)
 Call ID: 72b8e9ff-02be-4512-ad6f-362deede6d0e
  Args:
    relation: :isSisterOf
    target: :Anne_Bowes-Lyon
    source: :Diana_Cinderella_Somervell
  AssignClass (d4802f5f-0829-48df-8f9b-eb193325ebbe)
 Call ID: d4802f5f-0829-48df-8f9b-eb193325ebbe
  Args:
    type: :Person
    source: :Nerissa_Bowes-Lyon
  AssignClass (09f0c30c-2a7a-46e4-8103-6887e95c3c1c)
 Call ID: 09f0c30c-2a7a-46e4-8103-6887e95c3c1c
  Args:
    type: :Woman
    source: :Nerissa_Bowes-Lyon
  AssignClass (90d6ed6a-cf14-46d2-a853-d19518433a1d)
 Call ID: 90d6ed6a-cf14-46d2-a853-d19518433a1d
  Args:
    source: :Katherine_Bowes-Lyon
    type: :Person
  AssignClass (ecd68e46-da2f-47e7-9c89-36f753de9ae8)
 Call ID: ecd68e46-da2f-47e7-9c89-36f753de9ae8
  Args:
    type: :Woman
    source: :Katherine_Bowes-Lyon
  AssignClass (f1d87fc1-5359-4dc5-bf27-3ef6f2bde64c)
 Call ID: f1d87fc1-5359-4dc5-bf27-3ef6f2bde64c
  Args:
    type: :Person
    source: :Patricia_Bowes-Lyon
  AssignClass (647b9fe8-882f-4348-bf97-8e19cd1c9de6)
 Call ID: 647b9fe8-882f-4348-bf97-8e19cd1c9de6
  Args:
    source: :Patricia_Bowes-Lyon
    type: :Woman
  AssignClass (15c1146a-9c99-4f51-a6c3-767b5355aa4d)
 Call ID: 15c1146a-9c99-4f51-a6c3-767b5355aa4d
  Args:
    type: :Person
    source: :Diana_Cinderella_Somervell
  AssignClass (035e17f0-98d1-4716-a168-0d63e6d0fc83)
 Call ID: 035e17f0-98d1-4716-a168-0d63e6d0fc83
  Args:
    type: :Woman
    source: :Diana_Cinderella_Somervell
  Finish (7567780d-4ed0-443f-8398-4187d856b727)
 Call ID: 7567780d-4ed0-443f-8398-4187d856b727
  Args: