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
  AssignClass (7f326a32-a69b-4b05-9592-cfa6a2bd915f)
 Call ID: 7f326a32-a69b-4b05-9592-cfa6a2bd915f
  Args:
    type: :Woman
    source: Lady_Iris_Mountbatten
  AssignClass (26cfa17d-467b-4c30-9466-f07d5ab4c741)
 Call ID: 26cfa17d-467b-4c30-9466-f07d5ab4c741
  Args:
    source: Alexander_Mountbatten
    type: :Man
  AssignClass (746a8bbb-0554-439e-99b2-46cbd04a6372)
 Call ID: 746a8bbb-0554-439e-99b2-46cbd04a6372
  Args:
    type: :Woman
    source: Irene_Frances_Adza_Denison
  AssignClass (0ab2192f-c327-4236-9dd0-e572264dc461)
 Call ID: 0ab2192f-c327-4236-9dd0-e572264dc461
  Args:
    type: :Woman
    source: Princess_Beatrice
  AssignClass (24dfc13b-4b7b-4665-80ee-7ef8f7c1579f)
 Call ID: 24dfc13b-4b7b-4665-80ee-7ef8f7c1579f
  Args:
    source: Prince_Henry_of_Battenberg
    type: :Man
  AssignClass (f6776915-ca4c-418a-8830-8caa0d510c4a)
 Call ID: f6776915-ca4c-418a-8830-8caa0d510c4a
  Args:
    type: :Man
    source: William_Francis_Henry_Denison
  AssignClass (d2835d84-3d7a-4b50-831f-cb62788e3d26)
 Call ID: d2835d84-3d7a-4b50-831f-cb62788e3d26
  Args:
    type: :Woman
    source: Lady_Grace_Adelaide_Fane
  AssignClass (a2044482-39be-4b87-b6c3-1d25551f8c21)
 Call ID: a2044482-39be-4b87-b6c3-1d25551f8c21
  Args:
    source: Francis_William_Henry_Fane
    type: :Man
  AssignClass (ac1ab42c-747b-4fd2-8a2c-e277beb3afb7)
 Call ID: ac1ab42c-747b-4fd2-8a2c-e277beb3afb7
  Args:
    type: :Man
    source: Hugo_William_Cecil_Denison
  AssignClass (a793fdb9-a2bf-4fc6-82e4-390cf996bc84)
 Call ID: a793fdb9-a2bf-4fc6-82e4-390cf996bc84
  Args:
    type: :Woman
    source: Lady_Zinnia_Rosemary_Denison
  AssignClass (b7a2cbb7-c183-402c-b47c-0cb126b0f26e)
 Call ID: b7a2cbb7-c183-402c-b47c-0cb126b0f26e
  Args:
    type: :Man
    source: Hamilton_Joseph_Keyes_OMalley
  AssignClass (bb1911c8-dbe3-4693-a33f-17769ab7458b)
 Call ID: bb1911c8-dbe3-4693-a33f-17769ab7458b
  Args:
    source: Robin_Alexander_Bryan
    type: :Man
  AssignClass (e87fbd60-7244-4b5a-81b4-f0c701a2818d)
 Call ID: e87fbd60-7244-4b5a-81b4-f0c701a2818d
  Args:
    source: William_Alexander_Kemp
    type: :Man
  AssignClass (a079b12f-5665-4e57-9a4c-ed5829d4c65b)
 Call ID: a079b12f-5665-4e57-9a4c-ed5829d4c65b
  Args:
    type: :Man
    source: Clarence_Arthur_Kemp
  AssignClass (14f7a426-780f-4118-ac9d-af9b19584ca7)
 Call ID: 14f7a426-780f-4118-ac9d-af9b19584ca7
  Args:
    source: Helen_Janet_Ballantyne
    type: :Woman
  AddLiteral (06de0fad-b306-4c8b-9c27-abf8837a7717)
 Call ID: 06de0fad-b306-4c8b-9c27-abf8837a7717
  Args:
    relation: :hasBirthYear
    source: Lady_Iris_Mountbatten
    literal_type: xsd:integer
    literal_value: 1920
  AddLiteral (6387fa9b-c16d-4bad-9aa6-977296eff91f)
 Call ID: 6387fa9b-c16d-4bad-9aa6-977296eff91f
  Args:
    source: Lady_Iris_Mountbatten
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1982
  AddTriple (00e497a4-9a27-4c8f-ad50-1155647d926b)
 Call ID: 00e497a4-9a27-4c8f-ad50-1155647d926b
  Args:
    relation: :hasFather
    source: Lady_Iris_Mountbatten
    target: Alexander_Mountbatten
  AddTriple (3425b8c7-c106-4377-92ef-045791d1a765)
 Call ID: 3425b8c7-c106-4377-92ef-045791d1a765
  Args:
    relation: :hasMother
    source: Lady_Iris_Mountbatten
    target: Irene_Frances_Adza_Denison
  AddTriple (479fc42c-505d-493b-87a5-595ff84f2b1f)
 Call ID: 479fc42c-505d-493b-87a5-595ff84f2b1f
  Args:
    target: Prince_Henry_of_Battenberg
    relation: :hasFather
    source: Alexander_Mountbatten
  AddTriple (98d7aad5-834c-461c-bf57-60267de1347c)
 Call ID: 98d7aad5-834c-461c-bf57-60267de1347c
  Args:
    relation: :hasMother
    source: Alexander_Mountbatten
    target: Princess_Beatrice
  AddTriple (18ab25ae-b41e-4c7a-a1c4-ac2af82fe65a)
 Call ID: 18ab25ae-b41e-4c7a-a1c4-ac2af82fe65a
  Args:
    source: Irene_Frances_Adza_Denison
    relation: :hasFather
    target: William_Francis_Henry_Denison
  AddTriple (88ca7588-f191-4578-a1e8-852602684175)
 Call ID: 88ca7588-f191-4578-a1e8-852602684175
  Args:
    target: Lady_Grace_Adelaide_Fane
    source: Irene_Frances_Adza_Denison
    relation: :hasMother
  AddTriple (bbfba20d-bed6-497e-9a47-b2514762ced4)
 Call ID: bbfba20d-bed6-497e-9a47-b2514762ced4
  Args:
    target: Francis_William_Henry_Fane
    source: Lady_Grace_Adelaide_Fane
    relation: :hasFather
  AddTriple (177b5739-2770-495d-88a7-f4aee5b1a159)
 Call ID: 177b5739-2770-495d-88a7-f4aee5b1a159
  Args:
    source: Hugo_William_Cecil_Denison
    relation: :hasFather
    target: William_Francis_Henry_Denison
  AddTriple (d22664d3-1c3d-4209-a92a-1ec4a4715867)
 Call ID: d22664d3-1c3d-4209-a92a-1ec4a4715867
  Args:
    target: Lady_Grace_Adelaide_Fane
    relation: :hasMother
    source: Hugo_William_Cecil_Denison
  AddTriple (d9753645-820a-4ff0-b739-b9d2adaece56)
 Call ID: d9753645-820a-4ff0-b739-b9d2adaece56
  Args:
    relation: :hasFather
    source: Lady_Zinnia_Rosemary_Denison
    target: Hugo_William_Cecil_Denison
  AddTriple (bae3acd7-a852-4990-880a-0d624ea1e085)
 Call ID: bae3acd7-a852-4990-880a-0d624ea1e085
  Args:
    source: Robin_Alexander_Bryan
    relation: :hasMother
    target: Lady_Iris_Mountbatten
  AddTriple (0dcc9549-19f7-4efa-93bb-0cbcbe963359)
 Call ID: 0dcc9549-19f7-4efa-93bb-0cbcbe963359
  Args:
    source: William_Alexander_Kemp
    relation: :hasFather
    target: Clarence_Arthur_Kemp
  AddTriple (f39574c8-30ca-4d1b-98d7-d7575fcd5160)
 Call ID: f39574c8-30ca-4d1b-98d7-d7575fcd5160
  Args:
    relation: :hasMother
    source: William_Alexander_Kemp
    target: Helen_Janet_Ballantyne
  Finish (8ccdb3c4-924f-4fb9-b81b-a6af70955082)
 Call ID: 8ccdb3c4-924f-4fb9-b81b-a6af70955082
  Args: