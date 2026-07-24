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
  AssignClass (4dfba395-63ee-4d74-9deb-c12f8bb1afc6)
 Call ID: 4dfba395-63ee-4d74-9deb-c12f8bb1afc6
  Args:
    source: Felipe_Juan_Froilán_de_Todos_los_Santos_de_Marichalar_y_Borbón
    type: :Man
  AssignClass (794cb799-b76d-434b-a66e-1cfdede7cf77)
 Call ID: 794cb799-b76d-434b-a66e-1cfdede7cf77
  Args:
    source: Felipe_Juan_Froilán_de_Todos_los_Santos_de_Marichalar_y_Borbón
    type: :Person
  AddLiteral (b8277c99-fde0-4b68-8ca8-4d7e00799a43)
 Call ID: b8277c99-fde0-4b68-8ca8-4d7e00799a43
  Args:
    relation: :knownAs
    literal_type: xsd:string
    literal_value: Froilán
    source: Felipe_Juan_Froilán_de_Todos_los_Santos_de_Marichalar_y_Borbón
  AddLiteral (64d5d7ee-d394-4609-b2c5-b0b8d2ddbfc5)
 Call ID: 64d5d7ee-d394-4609-b2c5-b0b8d2ddbfc5
  Args:
    source: Felipe_Juan_Froilán_de_Todos_los_Santos_de_Marichalar_y_Borbón
    literal_type: xsd:integer
    literal_value: 1998
    relation: :hasBirthYear
  AssignClass (c18b5340-2adb-4173-bf46-6af1db6cf7b7)
 Call ID: c18b5340-2adb-4173-bf46-6af1db6cf7b7
  Args:
    type: :Woman
    source: Infanta_Elena_Duchess_of_Lugo
  AssignClass (3752ced9-709e-4966-baa3-188574243d81)
 Call ID: 3752ced9-709e-4966-baa3-188574243d81
  Args:
    type: :Person
    source: Infanta_Elena_Duchess_of_Lugo
  AssignClass (d77fd0dd-b3cb-4d0f-8d28-8e13f662f530)
 Call ID: d77fd0dd-b3cb-4d0f-8d28-8e13f662f530
  Args:
    type: :Man
    source: Jaime_de_Marichalar
  AssignClass (d88d9b67-9098-4b19-9915-da20f0ca4926)
 Call ID: d88d9b67-9098-4b19-9915-da20f0ca4926
  Args:
    source: Jaime_de_Marichalar
    type: :Person
  AddTriple (6d79e267-1354-40f7-83a7-a003387e3321)
 Call ID: 6d79e267-1354-40f7-83a7-a003387e3321
  Args:
    source: Felipe_Juan_Froilán_de_Todos_los_Santos_de_Marichalar_y_Borbón
    relation: :isSonOf
    target: Infanta_Elena_Duchess_of_Lugo
  AddTriple (bfc97405-b0e6-4c1b-8055-2ce6e816ba77)
 Call ID: bfc97405-b0e6-4c1b-8055-2ce6e816ba77
  Args:
    source: Felipe_Juan_Froilán_de_Todos_los_Santos_de_Marichalar_y_Borbón
    target: Jaime_de_Marichalar
    relation: :isSonOf
  AssignClass (56fc1500-a591-430a-8bd8-a0293980b47b)
 Call ID: 56fc1500-a591-430a-8bd8-a0293980b47b
  Args:
    source: King_Juan_Carlos_I
    type: :Man
  AssignClass (0b32173b-e201-4d1d-be6b-f2ad890fb9ef)
 Call ID: 0b32173b-e201-4d1d-be6b-f2ad890fb9ef
  Args:
    type: :Person
    source: King_Juan_Carlos_I
  AssignClass (95a95f17-d267-49fe-b46c-890b8e217efa)
 Call ID: 95a95f17-d267-49fe-b46c-890b8e217efa
  Args:
    type: :Woman
    source: Queen_Sofía_of_Spain
  AssignClass (f767b0be-005c-4641-9801-30106dcd4e14)
 Call ID: f767b0be-005c-4641-9801-30106dcd4e14
  Args:
    type: :Person
    source: Queen_Sofía_of_Spain
  AddTriple (f1e6606b-91a2-4a02-a89b-80e21f99e31b)
 Call ID: f1e6606b-91a2-4a02-a89b-80e21f99e31b
  Args:
    target: King_Juan_Carlos_I
    relation: :isSonOf
    source: Infanta_Elena_Duchess_of_Lugo
  AddTriple (c91aaac0-68b4-4399-a7bb-64f40518fdcf)
 Call ID: c91aaac0-68b4-4399-a7bb-64f40518fdcf
  Args:
    target: Queen_Sofía_of_Spain
    relation: :isSonOf
    source: Infanta_Elena_Duchess_of_Lugo
  AssignClass (8cf0aa13-b8e6-4bdc-a416-3955655f6714)
 Call ID: 8cf0aa13-b8e6-4bdc-a416-3955655f6714
  Args:
    source: Amalio_de_Marichalar_y_Bruguera
    type: :Man
  AssignClass (c9fbbe6b-aea3-4056-b06b-f587a0986264)
 Call ID: c9fbbe6b-aea3-4056-b06b-f587a0986264
  Args:
    type: :Person
    source: Amalio_de_Marichalar_y_Bruguera
  AssignClass (9cb3c42c-dfc3-40a8-8ff8-74a10d4371ee)
 Call ID: 9cb3c42c-dfc3-40a8-8ff8-74a10d4371ee
  Args:
    type: :Woman
    source: Concepción_Sáenz_de_Tejada
  AssignClass (ced82fb5-35bb-496b-9cab-43b17904b5a2)
 Call ID: ced82fb5-35bb-496b-9cab-43b17904b5a2
  Args:
    type: :Person
    source: Concepción_Sáenz_de_Tejada
  AddTriple (398c4175-7256-4daa-93bd-e19dce56bcd4)
 Call ID: 398c4175-7256-4daa-93bd-e19dce56bcd4
  Args:
    source: Jaime_de_Marichalar
    relation: :isSonOf
    target: Amalio_de_Marichalar_y_Bruguera
  AddTriple (fd5d68bd-2ef1-4da9-b61c-17ef6aab32f6)
 Call ID: fd5d68bd-2ef1-4da9-b61c-17ef6aab32f6
  Args:
    target: Concepción_Sáenz_de_Tejada
    relation: :isSonOf
    source: Jaime_de_Marichalar
  AssignClass (acdf9504-19b4-4d01-88d8-7f0391a7d403)
 Call ID: acdf9504-19b4-4d01-88d8-7f0391a7d403
  Args:
    type: :Man
    source: King_Felipe_VI
  AssignClass (ab49a9e6-8e1e-4b4a-bff2-0e3ac530c6f7)
 Call ID: ab49a9e6-8e1e-4b4a-bff2-0e3ac530c6f7
  Args:
    type: :Person
    source: King_Felipe_VI
  AssignClass (fd405980-82df-49a2-b60f-5803f567224b)
 Call ID: fd405980-82df-49a2-b60f-5803f567224b
  Args:
    type: :Woman
    source: Victoria_de_Marichalar_y_Borbón
  AssignClass (ad41784b-7881-4117-b779-7bd6b5fac5f4)
 Call ID: ad41784b-7881-4117-b779-7bd6b5fac5f4
  Args:
    source: Victoria_de_Marichalar_y_Borbón
    type: :Person
  AddTriple (51817ee2-527c-4a7a-8d1c-72c3752b75c6)
 Call ID: 51817ee2-527c-4a7a-8d1c-72c3752b75c6
  Args:
    source: Felipe_Juan_Froilán_de_Todos_los_Santos_de_Marichalar_y_Borbón
    relation: :isSiblingOf
    target: Victoria_de_Marichalar_y_Borbón
  Finish (c8db01d7-377a-409f-a5fb-ffaa4afa5cf4)
 Call ID: c8db01d7-377a-409f-a5fb-ffaa4afa5cf4
  Args: