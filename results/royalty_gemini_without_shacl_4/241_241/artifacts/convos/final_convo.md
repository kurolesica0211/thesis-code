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
  AssignClass (a974ea05-3635-4250-a952-c76f7947020e)
 Call ID: a974ea05-3635-4250-a952-c76f7947020e
  Args:
    source: Felipe_Juan_Froilan_de_Todos_los_Santos_de_Marichalar_y_Borbon
    type: :Man
  AssignClass (df8bab4f-9c2e-476e-9cac-c8159533e2a7)
 Call ID: df8bab4f-9c2e-476e-9cac-c8159533e2a7
  Args:
    source: Felipe_Juan_Froilan_de_Todos_los_Santos_de_Marichalar_y_Borbon
    type: :Person
  AddLiteral (013b7fc3-93ba-4b7d-a2a5-25f4220e2f89)
 Call ID: 013b7fc3-93ba-4b7d-a2a5-25f4220e2f89
  Args:
    literal_value: Froilán
    source: Felipe_Juan_Froilan_de_Todos_los_Santos_de_Marichalar_y_Borbon
    relation: :knownAs
    literal_type: xsd:string
  AddLiteral (a5a4008e-bb36-47dc-8199-baabbaa5259c)
 Call ID: a5a4008e-bb36-47dc-8199-baabbaa5259c
  Args:
    literal_value: 1998
    literal_type: xsd:integer
    source: Felipe_Juan_Froilan_de_Todos_los_Santos_de_Marichalar_y_Borbon
    relation: :hasBirthYear
  AssignClass (be8e6333-48b0-44b9-9694-a31cb942ca65)
 Call ID: be8e6333-48b0-44b9-9694-a31cb942ca65
  Args:
    type: :Woman
    source: Infanta_Elena_Duchess_of_Lugo
  AssignClass (a1acf620-2a7c-41b0-9edc-af199e994974)
 Call ID: a1acf620-2a7c-41b0-9edc-af199e994974
  Args:
    type: :Person
    source: Infanta_Elena_Duchess_of_Lugo
  AssignClass (05538048-f68b-45ad-ae23-568f30868f35)
 Call ID: 05538048-f68b-45ad-ae23-568f30868f35
  Args:
    source: Jaime_de_Marichalar
    type: :Man
  AssignClass (b6963c39-2b29-4f8f-89db-67f3abdf4ccf)
 Call ID: b6963c39-2b29-4f8f-89db-67f3abdf4ccf
  Args:
    type: :Person
    source: Jaime_de_Marichalar
  AddTriple (62303dec-01fa-4064-a4a7-a1aee20c50d7)
 Call ID: 62303dec-01fa-4064-a4a7-a1aee20c50d7
  Args:
    target: Infanta_Elena_Duchess_of_Lugo
    source: Felipe_Juan_Froilan_de_Todos_los_Santos_de_Marichalar_y_Borbon
    relation: :hasMother
  AddTriple (8978bdf3-5191-47e8-93b1-88be8e0c198d)
 Call ID: 8978bdf3-5191-47e8-93b1-88be8e0c198d
  Args:
    source: Felipe_Juan_Froilan_de_Todos_los_Santos_de_Marichalar_y_Borbon
    relation: :hasFather
    target: Jaime_de_Marichalar
  AssignClass (976509a9-d722-491d-8365-72d2ec50ca30)
 Call ID: 976509a9-d722-491d-8365-72d2ec50ca30
  Args:
    type: :Man
    source: Juan_Carlos_I
  AssignClass (5ea41579-20ae-4d09-8622-0be6ee395ecd)
 Call ID: 5ea41579-20ae-4d09-8622-0be6ee395ecd
  Args:
    type: :Person
    source: Juan_Carlos_I
  AssignClass (5aa3715e-a849-4a2b-863d-bcab73e48e67)
 Call ID: 5aa3715e-a849-4a2b-863d-bcab73e48e67
  Args:
    source: Sofia_of_Spain
    type: :Woman
  AssignClass (4c743e6b-d2ef-4c02-a299-5683580a21b9)
 Call ID: 4c743e6b-d2ef-4c02-a299-5683580a21b9
  Args:
    type: :Person
    source: Sofia_of_Spain
  AddTriple (a3bc69f8-155f-4312-a3dd-0c1c3ec5110d)
 Call ID: a3bc69f8-155f-4312-a3dd-0c1c3ec5110d
  Args:
    target: Sofia_of_Spain
    source: Infanta_Elena_Duchess_of_Lugo
    relation: :hasMother
  AddTriple (5c05cbfc-71fd-4510-9880-58267bd88b29)
 Call ID: 5c05cbfc-71fd-4510-9880-58267bd88b29
  Args:
    relation: :hasFather
    source: Infanta_Elena_Duchess_of_Lugo
    target: Juan_Carlos_I
  AssignClass (ed63b49c-89de-462e-a65d-6c29dd3ef254)
 Call ID: ed63b49c-89de-462e-a65d-6c29dd3ef254
  Args:
    type: :Man
    source: Amalio_de_Marichalar_y_Bruguera
  AssignClass (2088b4fa-8153-43a4-9cdd-cbc9d373697b)
 Call ID: 2088b4fa-8153-43a4-9cdd-cbc9d373697b
  Args:
    source: Amalio_de_Marichalar_y_Bruguera
    type: :Person
  AssignClass (283af6d2-b26a-435f-809e-dd371380935b)
 Call ID: 283af6d2-b26a-435f-809e-dd371380935b
  Args:
    type: :Woman
    source: Concepcion_Saenz_de_Tejada
  AssignClass (090f3258-eeaf-4e87-9ffc-5152ee4f60c0)
 Call ID: 090f3258-eeaf-4e87-9ffc-5152ee4f60c0
  Args:
    type: :Person
    source: Concepcion_Saenz_de_Tejada
  AddTriple (00a6ef12-393d-45bc-ab3f-cd305416f497)
 Call ID: 00a6ef12-393d-45bc-ab3f-cd305416f497
  Args:
    target: Amalio_de_Marichalar_y_Bruguera
    relation: :hasFather
    source: Jaime_de_Marichalar
  AddTriple (a1c7bec2-c64f-4bdc-b6a2-fa9e6540b005)
 Call ID: a1c7bec2-c64f-4bdc-b6a2-fa9e6540b005
  Args:
    target: Concepcion_Saenz_de_Tejada
    source: Jaime_de_Marichalar
    relation: :hasMother
  AssignClass (91d8c774-053a-4110-84e2-e98b211bd007)
 Call ID: 91d8c774-053a-4110-84e2-e98b211bd007
  Args:
    type: :Woman
    source: Victoria_de_Marichalar_y_Borbon
  AssignClass (afb87ff3-bb00-4eaf-bb8a-e6943629c615)
 Call ID: afb87ff3-bb00-4eaf-bb8a-e6943629c615
  Args:
    source: Victoria_de_Marichalar_y_Borbon
    type: :Person
  AddTriple (2df52d09-3322-4977-8c35-158cb27e5237)
 Call ID: 2df52d09-3322-4977-8c35-158cb27e5237
  Args:
    target: Victoria_de_Marichalar_y_Borbon
    relation: :hasSister
    source: Felipe_Juan_Froilan_de_Todos_los_Santos_de_Marichalar_y_Borbon
  AddTriple (f3ca3159-2bd6-443b-8848-4727585686f3)
 Call ID: f3ca3159-2bd6-443b-8848-4727585686f3
  Args:
    target: Infanta_Elena_Duchess_of_Lugo
    source: Victoria_de_Marichalar_y_Borbon
    relation: :hasMother
  AddTriple (72ece457-4a44-4063-b373-487a1314f4da)
 Call ID: 72ece457-4a44-4063-b373-487a1314f4da
  Args:
    target: Jaime_de_Marichalar
    relation: :hasFather
    source: Victoria_de_Marichalar_y_Borbon
  Finish (73cf93fc-e521-4a93-a2f9-0521d580d9ce)
 Call ID: 73cf93fc-e521-4a93-a2f9-0521d580d9ce
  Args: