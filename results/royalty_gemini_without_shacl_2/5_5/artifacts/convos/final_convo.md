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
Lady Iris Victoria Beatrice Grace Kemp (née Mountbatten, formerly O'Malley, later Bryan; 13 January 1920 – 1 September 1982) was an English actress and model, and a member of the Battenberg/Mountbatten family.
She was also a niece of Queen Victoria Eugenie of Spain, making her a first cousin of Infante Juan, Count of Barcelona, father of Juan Carlos I and grandfather of current King Felipe VI of Spain, as well as Infante Jaime, Duke of Segovia, the Legitimist claimant to the French throne.
Family and early life

Iris Victoria Beatrice Grace Mountbatten was born at Kensington Palace, London on 13 January 1920, the only child of Alexander Mountbatten, 1st Marquess of Carisbrooke, eldest of three sons and one daughter of Princess Beatrice and Prince Henry of Battenberg.
Her mother, the Marchioness of Carisbrooke, was born Lady Irene Frances Adza Denison (4 July 1890 – 16 July 1956)
the only daughter of William Francis Henry Denison, 2nd Earl of Londesborough and Lady Grace Adelaide Fane (3 October 1860 – 13 June 1933), a daughter of Francis William Henry Fane, 12th Earl of Westmorland.
Lady Carisbrooke had two brothers of whom only one, Hugo William Cecil Denison, 4th and last Earl of Londesborough, was married.
He and his wife had one child, Iris's only maternal first cousin, Lady Zinnia Rosemary Denison (25 November 1937 – 13 July 1997) a keen equestrian and Master of the Whaddon Chase Hunt 1982–84. '
On 29 November 1934, Iris was a bridesmaid at the wedding of her third cousin, Princess Marina of Greece and Denmark, to Iris’ second cousin, Prince George, Duke of Kent.
(Marina and Iris were related through the Hesse family, while George and Iris were both great-grandchildren of Queen Victoria.)
On 12 May 1937 at their coronation, Iris was one of the six train bearers to Queen Elizabeth, wife and consort of her second cousin King George VI.
During World War II she worked as a nurse's aide, later moving to the United States, where she taught dance.
Marriages

Lady Iris was married three times.
On 29 January 1941 Lady Iris received Royal Licence by King George VI to marry Captain (later Major) Hamilton Joseph Keyes O'Malley (after an engagement formally announced in The Times on 18 January 1941).
Lady Iris formally reverted to her maiden name of Mountbatten by Deed poll dated 7 January 1949.
Lady Iris, by her second marriage, had one child, Robin Alexander Bryan (born Mount Sinai Hospital, Manhattan, New York City, 20 December 1957), who has three natural children from three different women.
On 11 December 1965, she married William Alexander Kemp (10 July 1921 – 12 December 1991), son of Clarence Arthur Kemp and Helen Janet Ballantyne, a Canadian actor and announcer.
Death

Lady Iris died on 1 September 1982 at Wellesley Hospital, Toronto, Ontario, Canada, of a brain tumour.
Her ashes were brought to the Isle of Wight for interment in the Battenberg Chapel, at St. Mildred's Church, Whippingham.



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
  AssignClass (6c7852a3-20d0-4d81-8658-363ec4d097ae)
 Call ID: 6c7852a3-20d0-4d81-8658-363ec4d097ae
  Args:
    source: Iris_Mountbatten
    type: :Woman
  AddLiteral (89e1e1b6-a6f2-4c90-bac6-a0ccbf0ba2bd)
 Call ID: 89e1e1b6-a6f2-4c90-bac6-a0ccbf0ba2bd
  Args:
    source: Iris_Mountbatten
    relation: :hasBirthYear
    literal_value: 1920
    literal_type: xsd:integer
  AddLiteral (98a6b563-9d8e-47a3-8478-9e60698f0f17)
 Call ID: 98a6b563-9d8e-47a3-8478-9e60698f0f17
  Args:
    literal_type: xsd:integer
    literal_value: 1982
    relation: :hasDeathYear
    source: Iris_Mountbatten
  AssignClass (2c0eb366-7b96-4b4c-820c-4b943f67531a)
 Call ID: 2c0eb366-7b96-4b4c-820c-4b943f67531a
  Args:
    source: Alexander_Mountbatten
    type: :Man
  AddTriple (3b764a20-f54a-4668-88b7-70346988ee09)
 Call ID: 3b764a20-f54a-4668-88b7-70346988ee09
  Args:
    relation: :hasFather
    source: Iris_Mountbatten
    target: Alexander_Mountbatten
  AssignClass (77e681c2-b5da-4ab8-b676-7e035e644e48)
 Call ID: 77e681c2-b5da-4ab8-b676-7e035e644e48
  Args:
    source: Irene_Frances_Adza_Denison
    type: :Woman
  AddTriple (69fe9264-c9f4-4bef-b557-95e948b48203)
 Call ID: 69fe9264-c9f4-4bef-b557-95e948b48203
  Args:
    relation: :hasMother
    source: Iris_Mountbatten
    target: Irene_Frances_Adza_Denison
  AddLiteral (63f18ebe-dea0-4536-8cbb-809d4b53e83e)
 Call ID: 63f18ebe-dea0-4536-8cbb-809d4b53e83e
  Args:
    source: Irene_Frances_Adza_Denison
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1890
  AddLiteral (a0759d5b-b36d-4d20-81d2-a92a43598169)
 Call ID: a0759d5b-b36d-4d20-81d2-a92a43598169
  Args:
    source: Irene_Frances_Adza_Denison
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 1956
  AssignClass (5052511c-b3ad-4d45-a19e-82b452117fd9)
 Call ID: 5052511c-b3ad-4d45-a19e-82b452117fd9
  Args:
    source: William_Francis_Henry_Denison
    type: :Man
  AssignClass (6d9f001b-e2cb-4c7a-8918-b9a17bcde6d5)
 Call ID: 6d9f001b-e2cb-4c7a-8918-b9a17bcde6d5
  Args:
    source: Grace_Adelaide_Fane
    type: :Woman
  AddTriple (35c5ac88-7b6b-4018-8797-5c31331d51cb)
 Call ID: 35c5ac88-7b6b-4018-8797-5c31331d51cb
  Args:
    relation: :hasFather
    target: William_Francis_Henry_Denison
    source: Irene_Frances_Adza_Denison
  AddTriple (a2040c0c-ec1b-4da4-b917-7f690cbaff34)
 Call ID: a2040c0c-ec1b-4da4-b917-7f690cbaff34
  Args:
    relation: :hasMother
    target: Grace_Adelaide_Fane
    source: Irene_Frances_Adza_Denison
  AddLiteral (ec8a6578-4a82-4e7d-8b43-1024f8770d4c)
 Call ID: ec8a6578-4a82-4e7d-8b43-1024f8770d4c
  Args:
    source: Grace_Adelaide_Fane
    literal_value: 1860
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (d92c6eb7-a8ea-4231-996b-19d5effc1dd3)
 Call ID: d92c6eb7-a8ea-4231-996b-19d5effc1dd3
  Args:
    source: Grace_Adelaide_Fane
    relation: :hasDeathYear
    literal_value: 1933
    literal_type: xsd:integer
  AssignClass (40281b10-8c95-44de-87ff-411ffac6c0d5)
 Call ID: 40281b10-8c95-44de-87ff-411ffac6c0d5
  Args:
    source: Francis_William_Henry_Fane
    type: :Man
  AddTriple (7fcb9aa3-e47c-4f4f-93b3-36a90733e5f3)
 Call ID: 7fcb9aa3-e47c-4f4f-93b3-36a90733e5f3
  Args:
    target: Francis_William_Henry_Fane
    source: Grace_Adelaide_Fane
    relation: :hasFather
  AssignClass (b1287b24-e32b-46e6-9a5a-dd0349c39d4c)
 Call ID: b1287b24-e32b-46e6-9a5a-dd0349c39d4c
  Args:
    type: :Man
    source: Hugo_William_Cecil_Denison
  AddTriple (cd2ce32b-67a1-455e-9aa4-79ca8830ce5a)
 Call ID: cd2ce32b-67a1-455e-9aa4-79ca8830ce5a
  Args:
    relation: :isBrotherOf
    source: Hugo_William_Cecil_Denison
    target: Irene_Frances_Adza_Denison
  AssignClass (1e02e98c-7e0e-4f45-b3f3-ca87df16a911)
 Call ID: 1e02e98c-7e0e-4f45-b3f3-ca87df16a911
  Args:
    type: :Woman
    source: Zinnia_Rosemary_Denison
  AddTriple (43b4f9ba-04cb-4ac9-8741-60a2a4abe642)
 Call ID: 43b4f9ba-04cb-4ac9-8741-60a2a4abe642
  Args:
    source: Zinnia_Rosemary_Denison
    target: Hugo_William_Cecil_Denison
    relation: :isChildOf
  AssignClass (f00acaf5-3972-4917-9d14-0b51bf7e57f0)
 Call ID: f00acaf5-3972-4917-9d14-0b51bf7e57f0
  Args:
    source: Hamilton_Joseph_Keyes_OMalley
    type: :Man
  AddLiteral (3d40d5bf-3a19-4a44-9f02-0d3d37d4d9d8)
 Call ID: 3d40d5bf-3a19-4a44-9f02-0d3d37d4d9d8
  Args:
    source: Iris_Mountbatten
    relation: :hasMarriageYear
    literal_value: 1941
    literal_type: xsd:integer
  AssignClass (da822750-b538-4c96-a3a0-d4b98200f821)
 Call ID: da822750-b538-4c96-a3a0-d4b98200f821
  Args:
    source: Robin_Alexander_Bryan
    type: :Man
  AddTriple (c229942e-1ddb-477c-b75e-f0ed61e0805b)
 Call ID: c229942e-1ddb-477c-b75e-f0ed61e0805b
  Args:
    source: Robin_Alexander_Bryan
    target: Iris_Mountbatten
    relation: :isChildOf
  AssignClass (9ca271ef-eb99-4c8a-9edd-61219d4855c5)
 Call ID: 9ca271ef-eb99-4c8a-9edd-61219d4855c5
  Args:
    type: :Man
    source: William_Alexander_Kemp
  AddLiteral (a681d3b2-f3ec-4efc-9966-191b8fa7e6b4)
 Call ID: a681d3b2-f3ec-4efc-9966-191b8fa7e6b4
  Args:
    source: Iris_Mountbatten
    literal_type: xsd:integer
    literal_value: 1965
    relation: :hasMarriageYear
  AddLiteral (10efecff-fc18-4763-ab3a-e8f4416a874d)
 Call ID: 10efecff-fc18-4763-ab3a-e8f4416a874d
  Args:
    source: William_Alexander_Kemp
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1921
  AddLiteral (aab787a8-6106-41b2-a006-abbba7f4bccf)
 Call ID: aab787a8-6106-41b2-a006-abbba7f4bccf
  Args:
    source: William_Alexander_Kemp
    literal_value: 1991
    literal_type: xsd:integer
    relation: :hasDeathYear
  AssignClass (8f55c726-2cde-492e-b2d0-7eae25b26f73)
 Call ID: 8f55c726-2cde-492e-b2d0-7eae25b26f73
  Args:
    source: Clarence_Arthur_Kemp
    type: :Man
  AssignClass (23046918-f017-47ef-ace4-e73726b75725)
 Call ID: 23046918-f017-47ef-ace4-e73726b75725
  Args:
    type: :Woman
    source: Helen_Janet_Ballantyne
  AddTriple (02aa016b-f44d-4b0a-8a1a-7461f4813b0f)
 Call ID: 02aa016b-f44d-4b0a-8a1a-7461f4813b0f
  Args:
    target: Clarence_Arthur_Kemp
    source: William_Alexander_Kemp
    relation: :hasFather
  AddTriple (5cc8ee7c-3865-4a6b-a925-acc35a6dec1a)
 Call ID: 5cc8ee7c-3865-4a6b-a925-acc35a6dec1a
  Args:
    source: William_Alexander_Kemp
    target: Helen_Janet_Ballantyne
    relation: :hasMother
  Finish (c6b67051-d517-47a4-8cf9-c5334561105e)
 Call ID: c6b67051-d517-47a4-8cf9-c5334561105e
  Args: