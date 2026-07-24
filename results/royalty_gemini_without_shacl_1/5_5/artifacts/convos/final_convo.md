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
  AssignClass (9d318b4e-0aa7-474b-90bd-72c30b9c8ba4)
 Call ID: 9d318b4e-0aa7-474b-90bd-72c30b9c8ba4
  Args:
    source: Iris_Mountbatten
    type: :Woman
  AssignClass (d8304daa-f968-44b7-805c-3a95a4805792)
 Call ID: d8304daa-f968-44b7-805c-3a95a4805792
  Args:
    source: Iris_Mountbatten
    type: :Person
  AddLiteral (b323c782-f938-4f8a-abae-618472eca567)
 Call ID: b323c782-f938-4f8a-abae-618472eca567
  Args:
    literal_type: xsd:integer
    source: Iris_Mountbatten
    literal_value: 1920
    relation: :hasBirthYear
  AddLiteral (c9918891-795d-4fdd-91d4-75954261b898)
 Call ID: c9918891-795d-4fdd-91d4-75954261b898
  Args:
    literal_type: xsd:integer
    source: Iris_Mountbatten
    literal_value: 1982
    relation: :hasDeathYear
  AddLiteral (36f28d57-5b03-4f22-8fa3-c9223fdc0a9a)
 Call ID: 36f28d57-5b03-4f22-8fa3-c9223fdc0a9a
  Args:
    relation: :knownAs
    literal_value: Lady Iris Victoria Beatrice Grace Kemp
    source: Iris_Mountbatten
    literal_type: xsd:string
  AddLiteral (2d31915a-3095-4578-8a68-ef5323f4e195)
 Call ID: 2d31915a-3095-4578-8a68-ef5323f4e195
  Args:
    literal_value: Iris Mountbatten
    source: Iris_Mountbatten
    literal_type: xsd:string
    relation: :formerlyKnownAs
  AssignClass (26d07228-b0cd-4d70-ac61-34762b15bc87)
 Call ID: 26d07228-b0cd-4d70-ac61-34762b15bc87
  Args:
    source: Alexander_Mountbatten
    type: :Man
  AssignClass (645c253b-de73-4f1f-ad3c-22e32a8da0cd)
 Call ID: 645c253b-de73-4f1f-ad3c-22e32a8da0cd
  Args:
    source: Alexander_Mountbatten
    type: :Person
  AssignClass (d0b37b7a-dae4-4b00-aee2-ec33f3da7260)
 Call ID: d0b37b7a-dae4-4b00-aee2-ec33f3da7260
  Args:
    source: Irene_Frances_Adza_Denison
    type: :Woman
  AssignClass (1918aa08-ef76-427e-968d-d0fd5277a1a6)
 Call ID: 1918aa08-ef76-427e-968d-d0fd5277a1a6
  Args:
    type: :Person
    source: Irene_Frances_Adza_Denison
  AddTriple (5736313d-a08a-4a86-8493-2bc156ee1bbb)
 Call ID: 5736313d-a08a-4a86-8493-2bc156ee1bbb
  Args:
    relation: :hasFather
    target: Alexander_Mountbatten
    source: Iris_Mountbatten
  AddTriple (0777bcea-1e6d-4c7d-92cc-1a5523088329)
 Call ID: 0777bcea-1e6d-4c7d-92cc-1a5523088329
  Args:
    source: Iris_Mountbatten
    relation: :hasMother
    target: Irene_Frances_Adza_Denison
  AddLiteral (457375f0-e16a-4716-a717-43016b71d357)
 Call ID: 457375f0-e16a-4716-a717-43016b71d357
  Args:
    literal_value: 1890
    source: Irene_Frances_Adza_Denison
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (7d713720-78d1-472f-bcfd-cbfb9940b05e)
 Call ID: 7d713720-78d1-472f-bcfd-cbfb9940b05e
  Args:
    literal_type: xsd:integer
    source: Irene_Frances_Adza_Denison
    literal_value: 1956
    relation: :hasDeathYear
  AssignClass (365c2d50-e791-4d00-99a8-1c8ce8a182a0)
 Call ID: 365c2d50-e791-4d00-99a8-1c8ce8a182a0
  Args:
    type: :Woman
    source: Princess_Beatrice
  AssignClass (0c961644-224e-408b-972e-24f3c806855f)
 Call ID: 0c961644-224e-408b-972e-24f3c806855f
  Args:
    type: :Person
    source: Princess_Beatrice
  AssignClass (24813949-d8d2-4932-94ff-02d8f82ce468)
 Call ID: 24813949-d8d2-4932-94ff-02d8f82ce468
  Args:
    type: :Man
    source: Prince_Henry_of_Battenberg
  AssignClass (29254336-7c45-4456-8fd9-ee89cde5c64c)
 Call ID: 29254336-7c45-4456-8fd9-ee89cde5c64c
  Args:
    type: :Person
    source: Prince_Henry_of_Battenberg
  AddTriple (33ac99d8-322a-4bb9-b3dc-e2359d37febf)
 Call ID: 33ac99d8-322a-4bb9-b3dc-e2359d37febf
  Args:
    source: Alexander_Mountbatten
    relation: :hasMother
    target: Princess_Beatrice
  AddTriple (f24c5430-f80f-4c31-8485-715721a25144)
 Call ID: f24c5430-f80f-4c31-8485-715721a25144
  Args:
    target: Prince_Henry_of_Battenberg
    relation: :hasFather
    source: Alexander_Mountbatten
  AssignClass (b6896336-c079-4af6-993c-262b30c908d1)
 Call ID: b6896336-c079-4af6-993c-262b30c908d1
  Args:
    type: :Man
    source: William_Francis_Henry_Denison
  AssignClass (209df26a-41ad-4a97-8a4a-6c645f67f599)
 Call ID: 209df26a-41ad-4a97-8a4a-6c645f67f599
  Args:
    type: :Person
    source: William_Francis_Henry_Denison
  AssignClass (b1011c05-1fe7-44ae-ba1f-0131ba3764c9)
 Call ID: b1011c05-1fe7-44ae-ba1f-0131ba3764c9
  Args:
    type: :Woman
    source: Grace_Adelaide_Fane
  AssignClass (fcd42af1-5256-4696-9a5b-7785705a4aeb)
 Call ID: fcd42af1-5256-4696-9a5b-7785705a4aeb
  Args:
    source: Grace_Adelaide_Fane
    type: :Person
  AddTriple (694c7130-0ba4-4c2b-8431-dd10016f4a09)
 Call ID: 694c7130-0ba4-4c2b-8431-dd10016f4a09
  Args:
    target: William_Francis_Henry_Denison
    relation: :hasFather
    source: Irene_Frances_Adza_Denison
  AddTriple (cdf57e5f-385b-489e-b97e-37ccf5fd0833)
 Call ID: cdf57e5f-385b-489e-b97e-37ccf5fd0833
  Args:
    target: Grace_Adelaide_Fane
    relation: :hasMother
    source: Irene_Frances_Adza_Denison
  AddLiteral (c3b4b0c1-78cc-4c7f-ae48-2c8fb7f2e69c)
 Call ID: c3b4b0c1-78cc-4c7f-ae48-2c8fb7f2e69c
  Args:
    source: Grace_Adelaide_Fane
    literal_value: 1860
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (398a1270-fb88-4631-8bd3-b2717795c5e5)
 Call ID: 398a1270-fb88-4631-8bd3-b2717795c5e5
  Args:
    relation: :hasDeathYear
    literal_value: 1933
    source: Grace_Adelaide_Fane
    literal_type: xsd:integer
  AssignClass (aa4316ff-1547-4da3-bc9c-5fbd751f0e3d)
 Call ID: aa4316ff-1547-4da3-bc9c-5fbd751f0e3d
  Args:
    type: :Man
    source: Francis_William_Henry_Fane
  AssignClass (716b7345-b4e6-49b4-b406-b90e2e6b9370)
 Call ID: 716b7345-b4e6-49b4-b406-b90e2e6b9370
  Args:
    source: Francis_William_Henry_Fane
    type: :Person
  AddTriple (77178dce-93fd-4877-95de-ee25664d6cff)
 Call ID: 77178dce-93fd-4877-95de-ee25664d6cff
  Args:
    relation: :hasFather
    target: Francis_William_Henry_Fane
    source: Grace_Adelaide_Fane
  AssignClass (06bd5582-8625-4255-9a34-c41e411caa86)
 Call ID: 06bd5582-8625-4255-9a34-c41e411caa86
  Args:
    type: :Man
    source: Hugo_William_Cecil_Denison
  AssignClass (e1f0d851-4422-478f-a80a-9d1bbe8cae7a)
 Call ID: e1f0d851-4422-478f-a80a-9d1bbe8cae7a
  Args:
    source: Hugo_William_Cecil_Denison
    type: :Person
  AddTriple (7938c9be-1307-4479-bdb7-60e32fdac8e0)
 Call ID: 7938c9be-1307-4479-bdb7-60e32fdac8e0
  Args:
    target: Hugo_William_Cecil_Denison
    relation: :hasBrother
    source: Irene_Frances_Adza_Denison
  AssignClass (d8fdd827-901c-40fe-a9e8-27139e05f38c)
 Call ID: d8fdd827-901c-40fe-a9e8-27139e05f38c
  Args:
    source: Zinnia_Rosemary_Denison
    type: :Woman
  AssignClass (10369bf9-c388-479e-b504-0f04122d9b2c)
 Call ID: 10369bf9-c388-479e-b504-0f04122d9b2c
  Args:
    source: Zinnia_Rosemary_Denison
    type: :Person
  AddTriple (c906c18c-c614-46be-b10b-2eef95408639)
 Call ID: c906c18c-c614-46be-b10b-2eef95408639
  Args:
    relation: :hasFather
    target: Hugo_William_Cecil_Denison
    source: Zinnia_Rosemary_Denison
  AddLiteral (7c336758-02b9-4373-9377-ddd801c194e9)
 Call ID: 7c336758-02b9-4373-9377-ddd801c194e9
  Args:
    literal_type: xsd:integer
    literal_value: 1937
    source: Zinnia_Rosemary_Denison
    relation: :hasBirthYear
  AddLiteral (7c7e8e95-220e-4eb1-a64d-9e2f75cf8070)
 Call ID: 7c7e8e95-220e-4eb1-a64d-9e2f75cf8070
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: Zinnia_Rosemary_Denison
    literal_value: 1997
  AssignClass (98d412d3-bf2c-4d08-bde9-98aeb31ad829)
 Call ID: 98d412d3-bf2c-4d08-bde9-98aeb31ad829
  Args:
    type: :Man
    source: Hamilton_Joseph_Keyes_OMalley
  AssignClass (dc2ed9b0-5b60-4b37-b2a3-e9ddbaedeeed)
 Call ID: dc2ed9b0-5b60-4b37-b2a3-e9ddbaedeeed
  Args:
    source: Hamilton_Joseph_Keyes_OMalley
    type: :Person
  AddLiteral (580934e2-7f50-49d7-a0d0-0244fb35d82b)
 Call ID: 580934e2-7f50-49d7-a0d0-0244fb35d82b
  Args:
    source: Hamilton_Joseph_Keyes_OMalley
    literal_value: 1941
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AssignClass (166309d0-82f5-40e4-bab5-c3b4e87d86c5)
 Call ID: 166309d0-82f5-40e4-bab5-c3b4e87d86c5
  Args:
    type: :Man
    source: Robin_Alexander_Bryan
  AssignClass (2e8626fa-ea51-44dc-ae8f-26c457e1519f)
 Call ID: 2e8626fa-ea51-44dc-ae8f-26c457e1519f
  Args:
    source: Robin_Alexander_Bryan
    type: :Person
  AddTriple (cdadbf32-b8b0-4e4e-af3b-f5e6d39863e2)
 Call ID: cdadbf32-b8b0-4e4e-af3b-f5e6d39863e2
  Args:
    source: Robin_Alexander_Bryan
    relation: :hasMother
    target: Iris_Mountbatten
  AddLiteral (6268ee28-22c5-427d-9d10-e53f332adb16)
 Call ID: 6268ee28-22c5-427d-9d10-e53f332adb16
  Args:
    literal_type: xsd:integer
    literal_value: 1957
    source: Robin_Alexander_Bryan
    relation: :hasBirthYear
  AssignClass (883bc6ad-3055-460e-9cfa-17453d8ce506)
 Call ID: 883bc6ad-3055-460e-9cfa-17453d8ce506
  Args:
    type: :Man
    source: William_Alexander_Kemp
  AssignClass (b654272c-49ad-4c82-b9a4-59f1c92dfe1b)
 Call ID: b654272c-49ad-4c82-b9a4-59f1c92dfe1b
  Args:
    type: :Person
    source: William_Alexander_Kemp
  AddLiteral (c165aafa-d8a9-4752-97a3-738892cd7817)
 Call ID: c165aafa-d8a9-4752-97a3-738892cd7817
  Args:
    relation: :hasMarriageYear
    literal_type: xsd:integer
    literal_value: 1965
    source: William_Alexander_Kemp
  AddLiteral (111c7b71-53c6-4e25-92e5-b8a09b0c97b1)
 Call ID: 111c7b71-53c6-4e25-92e5-b8a09b0c97b1
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: William_Alexander_Kemp
    literal_value: 1921
  AddLiteral (bc245ee2-b6fc-4455-9dfb-b9fe912b418f)
 Call ID: bc245ee2-b6fc-4455-9dfb-b9fe912b418f
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 1991
    source: William_Alexander_Kemp
  AssignClass (c917781b-84cf-41ae-9c5b-ee5cca1e9cb5)
 Call ID: c917781b-84cf-41ae-9c5b-ee5cca1e9cb5
  Args:
    source: Clarence_Arthur_Kemp
    type: :Man
  AssignClass (e86160a9-2886-431e-b049-58d1a86106cc)
 Call ID: e86160a9-2886-431e-b049-58d1a86106cc
  Args:
    source: Clarence_Arthur_Kemp
    type: :Person
  AssignClass (f3b84591-87c4-4d66-a1af-3905ee914f55)
 Call ID: f3b84591-87c4-4d66-a1af-3905ee914f55
  Args:
    source: Helen_Janet_Ballantyne
    type: :Woman
  AssignClass (8e83d314-7af9-4c00-b61d-94d5a84caa93)
 Call ID: 8e83d314-7af9-4c00-b61d-94d5a84caa93
  Args:
    type: :Person
    source: Helen_Janet_Ballantyne
  AddTriple (63928b4e-8159-4296-abeb-67fc7b637940)
 Call ID: 63928b4e-8159-4296-abeb-67fc7b637940
  Args:
    relation: :hasFather
    target: Clarence_Arthur_Kemp
    source: William_Alexander_Kemp
  AddTriple (60178fa0-6c56-41bc-99c9-a2e61d43a8cc)
 Call ID: 60178fa0-6c56-41bc-99c9-a2e61d43a8cc
  Args:
    relation: :hasMother
    target: Helen_Janet_Ballantyne
    source: William_Alexander_Kemp
  Finish (58aa1054-33a6-4b4d-9b68-27a8c3f0cfa4)
 Call ID: 58aa1054-33a6-4b4d-9b68-27a8c3f0cfa4
  Args: