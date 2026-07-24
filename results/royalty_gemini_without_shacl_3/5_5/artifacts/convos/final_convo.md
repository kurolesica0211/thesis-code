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
  AssignClass (b26e5c4e-ae8c-4987-8c6f-0ddeac6af219)
 Call ID: b26e5c4e-ae8c-4987-8c6f-0ddeac6af219
  Args:
    source: Iris_Mountbatten
    type: :Woman
  AddLiteral (dcc9bcb5-8a45-4e24-9b46-b033b03d806d)
 Call ID: dcc9bcb5-8a45-4e24-9b46-b033b03d806d
  Args:
    literal_value: 1920
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Iris_Mountbatten
  AddLiteral (f82b7528-2ad1-475c-a2e4-938e656e685d)
 Call ID: f82b7528-2ad1-475c-a2e4-938e656e685d
  Args:
    source: Iris_Mountbatten
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 1982
  AssignClass (94e83f24-a947-4be7-9e94-c0b3ad4f150f)
 Call ID: 94e83f24-a947-4be7-9e94-c0b3ad4f150f
  Args:
    source: Alexander_Mountbatten
    type: :Man
  AddTriple (a4de1a6b-bc88-4fd5-b814-5c250497fb1c)
 Call ID: a4de1a6b-bc88-4fd5-b814-5c250497fb1c
  Args:
    source: Alexander_Mountbatten
    target: Iris_Mountbatten
    relation: :isFatherOf
  AssignClass (330dfbbf-373a-4af9-90a9-46dc756dfe57)
 Call ID: 330dfbbf-373a-4af9-90a9-46dc756dfe57
  Args:
    source: Irene_Frances_Adza_Denison
    type: :Woman
  AddLiteral (824fc848-8d00-4a98-8212-6977da32fe8a)
 Call ID: 824fc848-8d00-4a98-8212-6977da32fe8a
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1890
    source: Irene_Frances_Adza_Denison
  AddLiteral (666295e8-62f2-4aa4-99b5-5884fe6bedc8)
 Call ID: 666295e8-62f2-4aa4-99b5-5884fe6bedc8
  Args:
    literal_type: xsd:integer
    literal_value: 1956
    relation: :hasDeathYear
    source: Irene_Frances_Adza_Denison
  AddTriple (74bf570e-3212-4e31-9142-5e873e55b27e)
 Call ID: 74bf570e-3212-4e31-9142-5e873e55b27e
  Args:
    source: Irene_Frances_Adza_Denison
    relation: :isMotherOf
    target: Iris_Mountbatten
  AssignClass (0f9af785-edda-4a2d-b991-33ab8c9525bb)
 Call ID: 0f9af785-edda-4a2d-b991-33ab8c9525bb
  Args:
    source: William_Francis_Henry_Denison
    type: :Man
  AddTriple (a2d3714c-f815-48c3-8e2a-9eab4898c4ba)
 Call ID: a2d3714c-f815-48c3-8e2a-9eab4898c4ba
  Args:
    target: Irene_Frances_Adza_Denison
    relation: :isFatherOf
    source: William_Francis_Henry_Denison
  AssignClass (35d3a039-d122-4a55-a0b4-51a5b44f28e8)
 Call ID: 35d3a039-d122-4a55-a0b4-51a5b44f28e8
  Args:
    source: Grace_Adelaide_Fane
    type: :Woman
  AddLiteral (4fe899cc-8eeb-4901-8a82-4f5ae06ca02b)
 Call ID: 4fe899cc-8eeb-4901-8a82-4f5ae06ca02b
  Args:
    source: Grace_Adelaide_Fane
    literal_value: 1860
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (83ed8765-43b7-42eb-be64-a091f223c401)
 Call ID: 83ed8765-43b7-42eb-be64-a091f223c401
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 1933
    source: Grace_Adelaide_Fane
  AddTriple (89a3c0cc-3cb6-46af-956a-3394794cca68)
 Call ID: 89a3c0cc-3cb6-46af-956a-3394794cca68
  Args:
    source: Grace_Adelaide_Fane
    target: Irene_Frances_Adza_Denison
    relation: :isMotherOf
  AssignClass (ba70ebd8-dbba-4c03-a0be-77848130678d)
 Call ID: ba70ebd8-dbba-4c03-a0be-77848130678d
  Args:
    source: Francis_William_Henry_Fane
    type: :Man
  AddTriple (150a7844-c8c2-4646-b375-fcee0d7bf03f)
 Call ID: 150a7844-c8c2-4646-b375-fcee0d7bf03f
  Args:
    source: Francis_William_Henry_Fane
    relation: :isFatherOf
    target: Grace_Adelaide_Fane
  AssignClass (3a30c3d4-de61-4062-8754-2973464e9a2d)
 Call ID: 3a30c3d4-de61-4062-8754-2973464e9a2d
  Args:
    source: Hugo_William_Cecil_Denison
    type: :Man
  AddTriple (bf1b5eee-a67c-4d91-9506-76e3c3e33a9c)
 Call ID: bf1b5eee-a67c-4d91-9506-76e3c3e33a9c
  Args:
    target: Irene_Frances_Adza_Denison
    relation: :isBrotherOf
    source: Hugo_William_Cecil_Denison
  AssignClass (5e2067fc-3e89-4ccd-82f9-1055178d939e)
 Call ID: 5e2067fc-3e89-4ccd-82f9-1055178d939e
  Args:
    type: :Woman
    source: Zinnia_Rosemary_Denison
  AddLiteral (f5efc023-0bf0-466e-9f2d-b13fc5754776)
 Call ID: f5efc023-0bf0-466e-9f2d-b13fc5754776
  Args:
    source: Zinnia_Rosemary_Denison
    relation: :hasBirthYear
    literal_value: 1937
    literal_type: xsd:integer
  AddLiteral (f356b24b-e559-49bc-a768-9e69a29c3566)
 Call ID: f356b24b-e559-49bc-a768-9e69a29c3566
  Args:
    literal_value: 1997
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: Zinnia_Rosemary_Denison
  AddTriple (cf1e1974-4080-458f-8bd3-452e97c87442)
 Call ID: cf1e1974-4080-458f-8bd3-452e97c87442
  Args:
    target: Zinnia_Rosemary_Denison
    relation: :isFatherOf
    source: Hugo_William_Cecil_Denison
  AssignClass (552a02a6-4673-45c4-b7c6-27610b1003e7)
 Call ID: 552a02a6-4673-45c4-b7c6-27610b1003e7
  Args:
    source: Hamilton_Joseph_Keyes_OMalley
    type: :Man
  AddTriple (1143bec8-0618-40e5-887c-cbde13156cd5)
 Call ID: 1143bec8-0618-40e5-887c-cbde13156cd5
  Args:
    relation: :hasRelation
    target: Hamilton_Joseph_Keyes_OMalley
    source: Iris_Mountbatten
  AssignClass (8c866677-ae2f-4f5e-a3bc-600277c33b23)
 Call ID: 8c866677-ae2f-4f5e-a3bc-600277c33b23
  Args:
    type: :Man
    source: Robin_Alexander_Bryan
  AddLiteral (98bc6608-b9d3-4507-9d28-0e9b7d516698)
 Call ID: 98bc6608-b9d3-4507-9d28-0e9b7d516698
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1957
    source: Robin_Alexander_Bryan
  AddTriple (e9c600d0-d920-41d2-b030-53b4582a82e2)
 Call ID: e9c600d0-d920-41d2-b030-53b4582a82e2
  Args:
    source: Iris_Mountbatten
    relation: :isMotherOf
    target: Robin_Alexander_Bryan
  AssignClass (ba46162f-6557-4b0f-92f5-1c89d937bb28)
 Call ID: ba46162f-6557-4b0f-92f5-1c89d937bb28
  Args:
    source: William_Alexander_Kemp
    type: :Man
  AddLiteral (1622c535-b5f5-4d24-823d-4009ab8239a5)
 Call ID: 1622c535-b5f5-4d24-823d-4009ab8239a5
  Args:
    source: William_Alexander_Kemp
    literal_type: xsd:integer
    literal_value: 1921
    relation: :hasBirthYear
  AddLiteral (ee734b25-6290-4ed5-906a-46064516247f)
 Call ID: ee734b25-6290-4ed5-906a-46064516247f
  Args:
    source: William_Alexander_Kemp
    literal_type: xsd:integer
    literal_value: 1991
    relation: :hasDeathYear
  AddTriple (aa1b9211-7203-42e4-9fe2-a3c1bb8cce2e)
 Call ID: aa1b9211-7203-42e4-9fe2-a3c1bb8cce2e
  Args:
    target: William_Alexander_Kemp
    relation: :hasRelation
    source: Iris_Mountbatten
  AssignClass (7585a553-cdec-44eb-bfca-dc37660e9fae)
 Call ID: 7585a553-cdec-44eb-bfca-dc37660e9fae
  Args:
    source: Clarence_Arthur_Kemp
    type: :Man
  AddTriple (08c52ef3-c04d-4200-b263-62dd9425cd9b)
 Call ID: 08c52ef3-c04d-4200-b263-62dd9425cd9b
  Args:
    relation: :isFatherOf
    target: William_Alexander_Kemp
    source: Clarence_Arthur_Kemp
  AssignClass (9120527f-f45f-4de9-928f-66164957ca4f)
 Call ID: 9120527f-f45f-4de9-928f-66164957ca4f
  Args:
    source: Helen_Janet_Ballantyne
    type: :Woman
  AddTriple (2d7e8813-1862-4edc-bc1c-a1c4455fe9e5)
 Call ID: 2d7e8813-1862-4edc-bc1c-a1c4455fe9e5
  Args:
    target: William_Alexander_Kemp
    relation: :isMotherOf
    source: Helen_Janet_Ballantyne
  Finish (bb48b8aa-c5a5-4bc5-8837-b396119e2931)
 Call ID: bb48b8aa-c5a5-4bc5-8837-b396119e2931
  Args: