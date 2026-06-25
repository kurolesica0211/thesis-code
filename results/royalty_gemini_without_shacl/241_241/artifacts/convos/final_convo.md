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
  AssignClass (eba09ca4-d4c8-4e75-9598-6787d9d74205)
 Call ID: eba09ca4-d4c8-4e75-9598-6787d9d74205
  Args:
    source: Felipe_Juan_Froilan_de_Todos_los_Santos_de_Marichalar_y_Borbon
    type: :Man
  AssignClass (9b647171-453d-4ecd-b09c-1bd99b5363d7)
 Call ID: 9b647171-453d-4ecd-b09c-1bd99b5363d7
  Args:
    source: Felipe_Juan_Froilan_de_Todos_los_Santos_de_Marichalar_y_Borbon
    type: :Person
  AddLiteral (82f10a84-dc2d-4649-8d49-caf609957e9d)
 Call ID: 82f10a84-dc2d-4649-8d49-caf609957e9d
  Args:
    literal_value: 1998
    literal_type: xsd:integer
    source: Felipe_Juan_Froilan_de_Todos_los_Santos_de_Marichalar_y_Borbon
    relation: :hasBirthYear
  AddLiteral (b35597cb-fe39-461a-bf23-1aaada3f2f31)
 Call ID: b35597cb-fe39-461a-bf23-1aaada3f2f31
  Args:
    literal_type: xsd:string
    source: Felipe_Juan_Froilan_de_Todos_los_Santos_de_Marichalar_y_Borbon
    literal_value: Froilan
    relation: :knownAs
  AssignClass (89d9e017-d149-47e1-b737-5e4f80952042)
 Call ID: 89d9e017-d149-47e1-b737-5e4f80952042
  Args:
    type: :Woman
    source: Infanta_Elena_Duchess_of_Lugo
  AssignClass (05cad11e-4b71-46d5-b985-9d0e88912f84)
 Call ID: 05cad11e-4b71-46d5-b985-9d0e88912f84
  Args:
    type: :Person
    source: Infanta_Elena_Duchess_of_Lugo
  AssignClass (66af0452-ca29-4de6-b5ef-1eeefd5921fe)
 Call ID: 66af0452-ca29-4de6-b5ef-1eeefd5921fe
  Args:
    type: :Man
    source: Jaime_de_Marichalar
  AssignClass (4753bce5-dc39-4e8e-b6e7-834f3603d9f8)
 Call ID: 4753bce5-dc39-4e8e-b6e7-834f3603d9f8
  Args:
    type: :Person
    source: Jaime_de_Marichalar
  AddTriple (69a281b9-1352-4b30-a101-5ba126bb1276)
 Call ID: 69a281b9-1352-4b30-a101-5ba126bb1276
  Args:
    relation: :hasMother
    target: Infanta_Elena_Duchess_of_Lugo
    source: Felipe_Juan_Froilan_de_Todos_los_Santos_de_Marichalar_y_Borbon
  AddTriple (deadc446-a8e2-4035-a6e1-eafd07f028ee)
 Call ID: deadc446-a8e2-4035-a6e1-eafd07f028ee
  Args:
    relation: :hasFather
    source: Felipe_Juan_Froilan_de_Todos_los_Santos_de_Marichalar_y_Borbon
    target: Jaime_de_Marichalar
  AssignClass (b64e257d-b11e-40d0-a80a-e04a8d197508)
 Call ID: b64e257d-b11e-40d0-a80a-e04a8d197508
  Args:
    source: Juan_Carlos_I
    type: :Man
  AssignClass (c9ee44d8-d468-4180-9618-bf7d61afe2b2)
 Call ID: c9ee44d8-d468-4180-9618-bf7d61afe2b2
  Args:
    source: Juan_Carlos_I
    type: :Person
  AssignClass (f93727be-50b4-455e-b22b-3cc878581796)
 Call ID: f93727be-50b4-455e-b22b-3cc878581796
  Args:
    source: Sofia_of_Spain
    type: :Woman
  AssignClass (2d7f8fbd-482a-491d-99b4-a634cd59b437)
 Call ID: 2d7f8fbd-482a-491d-99b4-a634cd59b437
  Args:
    type: :Person
    source: Sofia_of_Spain
  AddTriple (9eb9aa55-c8b4-4a08-8641-3120570ff048)
 Call ID: 9eb9aa55-c8b4-4a08-8641-3120570ff048
  Args:
    relation: :hasParent
    source: Infanta_Elena_Duchess_of_Lugo
    target: Juan_Carlos_I
  AddTriple (359916d1-416b-4db5-a178-63dd839bf12b)
 Call ID: 359916d1-416b-4db5-a178-63dd839bf12b
  Args:
    target: Sofia_of_Spain
    source: Infanta_Elena_Duchess_of_Lugo
    relation: :hasParent
  AssignClass (0da57e5d-dab8-4e5a-b432-a5b9db7c2dab)
 Call ID: 0da57e5d-dab8-4e5a-b432-a5b9db7c2dab
  Args:
    type: :Man
    source: Felipe_VI
  AssignClass (d1154b45-67b9-45c6-bb18-5ce30b755c0d)
 Call ID: d1154b45-67b9-45c6-bb18-5ce30b755c0d
  Args:
    source: Felipe_VI
    type: :Person
  AssignClass (9252f4ad-2e58-4574-9742-bb9f8887a315)
 Call ID: 9252f4ad-2e58-4574-9742-bb9f8887a315
  Args:
    source: Amalio_de_Marichalar_y_Bruguera
    type: :Man
  AssignClass (f103f5a8-958d-46f6-a9ba-b61a77dbb11e)
 Call ID: f103f5a8-958d-46f6-a9ba-b61a77dbb11e
  Args:
    type: :Person
    source: Amalio_de_Marichalar_y_Bruguera
  AssignClass (2ba0825f-5ffe-407e-8c21-19abadd05742)
 Call ID: 2ba0825f-5ffe-407e-8c21-19abadd05742
  Args:
    source: Concepcion_Saenz_de_Tejada
    type: :Woman
  AssignClass (ae480ed9-6b01-4fee-9f48-d373cc6dbcf9)
 Call ID: ae480ed9-6b01-4fee-9f48-d373cc6dbcf9
  Args:
    source: Concepcion_Saenz_de_Tejada
    type: :Person
  AddTriple (52cbc491-a708-455e-8d59-1faa52d8553f)
 Call ID: 52cbc491-a708-455e-8d59-1faa52d8553f
  Args:
    relation: :hasParent
    target: Amalio_de_Marichalar_y_Bruguera
    source: Jaime_de_Marichalar
  AddTriple (af509885-8bdd-4c79-8bc0-00c6de9ecfac)
 Call ID: af509885-8bdd-4c79-8bc0-00c6de9ecfac
  Args:
    relation: :hasParent
    target: Concepcion_Saenz_de_Tejada
    source: Jaime_de_Marichalar
  AssignClass (8bde81d2-e677-449e-82f9-31fe217c1520)
 Call ID: 8bde81d2-e677-449e-82f9-31fe217c1520
  Args:
    source: Victoria_de_Marichalar_y_Borbon
    type: :Woman
  AssignClass (5fe5e897-b253-4a0e-9093-579be485eac4)
 Call ID: 5fe5e897-b253-4a0e-9093-579be485eac4
  Args:
    source: Victoria_de_Marichalar_y_Borbon
    type: :Person
  AddTriple (8eefc8db-ba39-4fd6-a9f6-4d659e970540)
 Call ID: 8eefc8db-ba39-4fd6-a9f6-4d659e970540
  Args:
    target: Victoria_de_Marichalar_y_Borbon
    source: Felipe_Juan_Froilan_de_Todos_los_Santos_de_Marichalar_y_Borbon
    relation: :hasSister
  AddTriple (11843d06-4363-4ac3-9d45-c877a5aa0082)
 Call ID: 11843d06-4363-4ac3-9d45-c877a5aa0082
  Args:
    relation: :hasMother
    target: Infanta_Elena_Duchess_of_Lugo
    source: Victoria_de_Marichalar_y_Borbon
  AddTriple (4db3cf34-a7ea-4d13-b83d-fe9dafd172a5)
 Call ID: 4db3cf34-a7ea-4d13-b83d-fe9dafd172a5
  Args:
    target: Jaime_de_Marichalar
    source: Victoria_de_Marichalar_y_Borbon
    relation: :hasFather
  AssignClass (0c64dd52-4c3c-4022-ac2b-123ffa72249b)
 Call ID: 0c64dd52-4c3c-4022-ac2b-123ffa72249b
  Args:
    type: :Woman
    source: Leonor_Princess_of_Asturias
  AssignClass (2a5d953c-fa89-4d04-97d0-2a7ad4c4a59b)
 Call ID: 2a5d953c-fa89-4d04-97d0-2a7ad4c4a59b
  Args:
    type: :Person
    source: Leonor_Princess_of_Asturias
  AssignClass (ee3aaf53-7478-442b-9a57-780b3f881694)
 Call ID: ee3aaf53-7478-442b-9a57-780b3f881694
  Args:
    source: Infanta_Sofia_of_Spain
    type: :Woman
  AssignClass (d3fb8a0b-f917-4563-8bd3-80270a4a1766)
 Call ID: d3fb8a0b-f917-4563-8bd3-80270a4a1766
  Args:
    source: Infanta_Sofia_of_Spain
    type: :Person
  AddTriple (75f3ada4-81ea-4323-ae6e-e8106491fff8)
 Call ID: 75f3ada4-81ea-4323-ae6e-e8106491fff8
  Args:
    relation: :hasFather
    target: Felipe_VI
    source: Leonor_Princess_of_Asturias
  AddTriple (f1984416-7d73-4966-8961-7652a696369d)
 Call ID: f1984416-7d73-4966-8961-7652a696369d
  Args:
    target: Felipe_VI
    source: Infanta_Sofia_of_Spain
    relation: :hasFather
  Finish (ddba833f-2944-47c6-b5a7-96e29d39c762)
 Call ID: ddba833f-2944-47c6-b5a7-96e29d39c762
  Args: