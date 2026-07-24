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
Felipe Juan Froilán de Todos los Santos de Marichalar y Borbón, Lord of Tejada GE (born 17 July 1998), widely known as Froilán, is the elder child and only son of Infanta Elena, Duchess of Lugo, and Jaime de Marichalar.
He is the maternal-line grandson of King Juan Carlos I and Queen Sofía of Spain, and the nephew of King Felipe VI.
He is the paternal-line grandson of Amalio de Marichalar y Bruguera, VIII Count of Ripalda and Concepción Sáenz de Tejada, Lady of Tejada.
He is fourth in the line of succession to the Spanish throne, after his cousins (King Felipe's daughters) Leonor, Princess of Asturias, and Infanta Sofía of Spain and his mother, Elena.
He has a sister two years younger, Victoria de Marichalar y Borbón.
Early life

Birth and christening

Felipe de Marichalar y Borbón was born on 17 July 1998 at Ruber International Hospital in Madrid.
He was baptized on Sunday 4 October 1998 day of the feast of San Francisco de Asis and on the eve of San Froilán, patron of Lugo, the mass was celebrated in the audience hall of the Zarzuela Palace.
His godparents were his maternal grandfather, Juan Carlos of Spain, and his paternal grandmother, Concepción Sáez de Tejada y Fernández de Boadilla, Dowager Countess of Ripalda (1929–2014).
Froilán took a course at Cottesmore, a boarding prep school in West Sussex, to return the following year, in 2011, to Colegio Santa María del Pilar in Madrid, where he remained for three years.
On 9 April 2012, Felipe de Marichalar accidentally shot himself in his right foot while he was on a farm of his father's family in Garray (Soria).
The judge dismissed the case against Jaime de Marichalar, considering it not gross negligence but a small misdemeanor.
The tuition, which for each course amounted to $45,000, was paid for by his maternal grandfather King Juan Carlos I.


He then began his higher education studies, majoring in Business Administration and Management at the College for International Studies in Madrid, a Spanish Higher Education institution associated with Endicott College.
In January 2023 it was announced that Felipe would be going to live in the United Arab Emirates with his grandfather, Juan Carlos I. Froilán will work for the ADNOC oil company, owned by the Minister of Advanced Technology of the United Arab Emirates, Sultan Ahmed Al-Jaber.
Titles, styles, honours and arms

He is styled as The Most Excellent Don Felipe Juan Froilán de Todos los Santos de Marichalar y Borbón, Grandee of Spain and Caballero Divisoro Hijodalgo of the Illustrious Solar de Tejada


References



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
  AssignClass (581242a1-65f3-415f-9574-6581836baf3d)
 Call ID: 581242a1-65f3-415f-9574-6581836baf3d
  Args:
    type: :Man
    source: Felipe_Juan_Froilán_de_Todos_los_Santos_de_Marichalar_y_Borbón
  AssignClass (0faa6e8a-a0df-4e0b-877c-159980961244)
 Call ID: 0faa6e8a-a0df-4e0b-877c-159980961244
  Args:
    type: :Person
    source: Felipe_Juan_Froilán_de_Todos_los_Santos_de_Marichalar_y_Borbón
  AssignClass (95a7f4f8-d92e-4d2e-bf59-d0e8a057acda)
 Call ID: 95a7f4f8-d92e-4d2e-bf59-d0e8a057acda
  Args:
    type: :Woman
    source: Infanta_Elena
  AssignClass (e17ebef1-6f80-4e97-8515-92c8a9ef8208)
 Call ID: e17ebef1-6f80-4e97-8515-92c8a9ef8208
  Args:
    source: Infanta_Elena
    type: :Person
  AssignClass (ac257a60-d835-4ac1-80ad-c044b0569d5a)
 Call ID: ac257a60-d835-4ac1-80ad-c044b0569d5a
  Args:
    source: Jaime_de_Marichalar
    type: :Man
  AssignClass (e70484c6-5d79-44a1-a828-92e930560802)
 Call ID: e70484c6-5d79-44a1-a828-92e930560802
  Args:
    source: Jaime_de_Marichalar
    type: :Person
  AddLiteral (7cff4400-3250-4b64-8416-4e7b334642b4)
 Call ID: 7cff4400-3250-4b64-8416-4e7b334642b4
  Args:
    literal_type: xsd:integer
    source: Felipe_Juan_Froilán_de_Todos_los_Santos_de_Marichalar_y_Borbón
    literal_value: 1998
    relation: :hasBirthYear
  AddTriple (a8052d68-a38a-49a7-a1d8-1722598dc21e)
 Call ID: a8052d68-a38a-49a7-a1d8-1722598dc21e
  Args:
    target: Infanta_Elena
    relation: :hasMother
    source: Felipe_Juan_Froilán_de_Todos_los_Santos_de_Marichalar_y_Borbón
  AddTriple (5c4ad804-cb39-4d6c-8f03-68076fb74f9b)
 Call ID: 5c4ad804-cb39-4d6c-8f03-68076fb74f9b
  Args:
    relation: :hasFather
    source: Felipe_Juan_Froilán_de_Todos_los_Santos_de_Marichalar_y_Borbón
    target: Jaime_de_Marichalar
  AddLiteral (31010500-a6b7-45b6-9c6e-a1183f04b9aa)
 Call ID: 31010500-a6b7-45b6-9c6e-a1183f04b9aa
  Args:
    relation: :knownAs
    literal_type: xsd:string
    source: Felipe_Juan_Froilán_de_Todos_los_Santos_de_Marichalar_y_Borbón
    literal_value: Froilán
  AssignClass (5919d8c4-0151-4d01-b35d-f526aeec385c)
 Call ID: 5919d8c4-0151-4d01-b35d-f526aeec385c
  Args:
    source: Juan_Carlos_I
    type: :Man
  AssignClass (8939350e-f4dd-447d-80f4-8d889ac07dc1)
 Call ID: 8939350e-f4dd-447d-80f4-8d889ac07dc1
  Args:
    source: Juan_Carlos_I
    type: :Person
  AssignClass (0f07d21e-a983-4717-aa2b-4db35a4bb15c)
 Call ID: 0f07d21e-a983-4717-aa2b-4db35a4bb15c
  Args:
    source: Sofía_of_Spain
    type: :Woman
  AssignClass (866bdc4b-897d-4a15-af8b-102c1e179d66)
 Call ID: 866bdc4b-897d-4a15-af8b-102c1e179d66
  Args:
    source: Sofía_of_Spain
    type: :Person
  AddTriple (426054a8-0228-4c61-9ae6-b4c2a389e2bb)
 Call ID: 426054a8-0228-4c61-9ae6-b4c2a389e2bb
  Args:
    target: Juan_Carlos_I
    source: Infanta_Elena
    relation: :hasFather
  AddTriple (b20395f9-1856-450e-bd4a-c7f686f596ea)
 Call ID: b20395f9-1856-450e-bd4a-c7f686f596ea
  Args:
    target: Sofía_of_Spain
    source: Infanta_Elena
    relation: :hasMother
  AssignClass (327d6a9b-6220-4f05-8954-f2ee81425d56)
 Call ID: 327d6a9b-6220-4f05-8954-f2ee81425d56
  Args:
    source: Amalio_de_Marichalar_y_Bruguera
    type: :Man
  AssignClass (bc5a1981-bb93-4b7e-bbb1-b817fe997245)
 Call ID: bc5a1981-bb93-4b7e-bbb1-b817fe997245
  Args:
    source: Amalio_de_Marichalar_y_Bruguera
    type: :Person
  AssignClass (a5435772-f57a-4c9e-91f8-6d5fc25a735c)
 Call ID: a5435772-f57a-4c9e-91f8-6d5fc25a735c
  Args:
    source: Concepción_Sáenz_de_Tejada
    type: :Woman
  AssignClass (65fbe08c-55b7-42be-a347-96e55c7f18a7)
 Call ID: 65fbe08c-55b7-42be-a347-96e55c7f18a7
  Args:
    type: :Person
    source: Concepción_Sáenz_de_Tejada
  AddTriple (447887b5-41fc-4141-94fe-a731e09da1cb)
 Call ID: 447887b5-41fc-4141-94fe-a731e09da1cb
  Args:
    relation: :hasFather
    source: Jaime_de_Marichalar
    target: Amalio_de_Marichalar_y_Bruguera
  AddTriple (8637ec3f-ff15-4b48-8300-010b19b917b0)
 Call ID: 8637ec3f-ff15-4b48-8300-010b19b917b0
  Args:
    target: Concepción_Sáenz_de_Tejada
    relation: :hasMother
    source: Jaime_de_Marichalar
  AssignClass (d126faca-9b27-4228-96ff-4bd5844a7aef)
 Call ID: d126faca-9b27-4228-96ff-4bd5844a7aef
  Args:
    source: Victoria_de_Marichalar_y_Borbón
    type: :Woman
  AssignClass (c71d899b-4830-49d8-b1f6-8aeb5f61a7a7)
 Call ID: c71d899b-4830-49d8-b1f6-8aeb5f61a7a7
  Args:
    source: Victoria_de_Marichalar_y_Borbón
    type: :Person
  AddTriple (6d71e7ab-0271-4c02-8938-3a0e69441e58)
 Call ID: 6d71e7ab-0271-4c02-8938-3a0e69441e58
  Args:
    target: Victoria_de_Marichalar_y_Borbón
    source: Felipe_Juan_Froilán_de_Todos_los_Santos_de_Marichalar_y_Borbón
    relation: :hasSister
  AddTriple (b34da61a-bae8-4c79-a4ee-afc14a551f2e)
 Call ID: b34da61a-bae8-4c79-a4ee-afc14a551f2e
  Args:
    target: Infanta_Elena
    relation: :hasMother
    source: Victoria_de_Marichalar_y_Borbón
  AddTriple (9f0a965f-f413-474c-8a03-a7c72632e9a8)
 Call ID: 9f0a965f-f413-474c-8a03-a7c72632e9a8
  Args:
    target: Jaime_de_Marichalar
    relation: :hasFather
    source: Victoria_de_Marichalar_y_Borbón
  AssignClass (7db27416-6e51-4fe1-afbe-b531e3ff0de3)
 Call ID: 7db27416-6e51-4fe1-afbe-b531e3ff0de3
  Args:
    source: Felipe_VI
    type: :Man
  AssignClass (1e78c0c7-9280-40d5-92c3-451c0c413ab2)
 Call ID: 1e78c0c7-9280-40d5-92c3-451c0c413ab2
  Args:
    source: Felipe_VI
    type: :Person
  AddTriple (50571c5e-924e-4368-a3df-7172f67fb08d)
 Call ID: 50571c5e-924e-4368-a3df-7172f67fb08d
  Args:
    source: Infanta_Elena
    relation: :isSiblingOf
    target: Felipe_VI
  Finish (458c2eab-b2d3-40ea-b40e-72f63eeea135)
 Call ID: 458c2eab-b2d3-40ea-b40e-72f63eeea135
  Args: