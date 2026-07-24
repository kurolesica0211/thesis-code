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
  AssignClass (a232326d-c1ae-451c-8193-783bf5364698)
 Call ID: a232326d-c1ae-451c-8193-783bf5364698
  Args:
    source: :FelipeJuanFroilandeTodoslosSantosdeMarichalaryBorbon
    type: :Man
  AssignClass (e5bde922-7545-4ed7-8026-409df54a19a7)
 Call ID: e5bde922-7545-4ed7-8026-409df54a19a7
  Args:
    source: :FelipeJuanFroilandeTodoslosSantosdeMarichalaryBorbon
    type: :Person
  AddLiteral (6f5cdb81-b743-4b6b-8cd3-a5fc4e1f6273)
 Call ID: 6f5cdb81-b743-4b6b-8cd3-a5fc4e1f6273
  Args:
    literal_type: xsd:string
    source: :FelipeJuanFroilandeTodoslosSantosdeMarichalaryBorbon
    relation: :knownAs
    literal_value: Froilan
  AddLiteral (b286c23c-f25b-48f5-a948-d4fd5ce6aff2)
 Call ID: b286c23c-f25b-48f5-a948-d4fd5ce6aff2
  Args:
    literal_type: xsd:integer
    literal_value: 1998
    relation: :hasBirthYear
    source: :FelipeJuanFroilandeTodoslosSantosdeMarichalaryBorbon
  AssignClass (c9720ff4-c29b-499d-9e6f-15bb45c714a3)
 Call ID: c9720ff4-c29b-499d-9e6f-15bb45c714a3
  Args:
    type: :Woman
    source: :InfantaElenaDuchessofLugo
  AssignClass (36dd9258-d676-415d-84bc-4bfe71207c2c)
 Call ID: 36dd9258-d676-415d-84bc-4bfe71207c2c
  Args:
    source: :InfantaElenaDuchessofLugo
    type: :Person
  AssignClass (517aaf49-de55-4ee8-8f50-1a02f5054c54)
 Call ID: 517aaf49-de55-4ee8-8f50-1a02f5054c54
  Args:
    source: :JaimedeMarichalar
    type: :Man
  AssignClass (d4d506bb-0964-4505-a562-2bfab4cf19af)
 Call ID: d4d506bb-0964-4505-a562-2bfab4cf19af
  Args:
    source: :JaimedeMarichalar
    type: :Person
  AddTriple (0441f5ef-a440-41d3-ac23-1cc5426cbcaa)
 Call ID: 0441f5ef-a440-41d3-ac23-1cc5426cbcaa
  Args:
    source: :FelipeJuanFroilandeTodoslosSantosdeMarichalaryBorbon
    target: :InfantaElenaDuchessofLugo
    relation: :hasMother
  AddTriple (1f496a0c-6b01-4805-9025-72de386a36c7)
 Call ID: 1f496a0c-6b01-4805-9025-72de386a36c7
  Args:
    relation: :hasFather
    source: :FelipeJuanFroilandeTodoslosSantosdeMarichalaryBorbon
    target: :JaimedeMarichalar
  AssignClass (0dbd30a6-8fe7-4e25-b872-9c9498fb9667)
 Call ID: 0dbd30a6-8fe7-4e25-b872-9c9498fb9667
  Args:
    source: :JuanCarlosI
    type: :Man
  AssignClass (35133ffb-e681-43b4-b98b-a3b67267736f)
 Call ID: 35133ffb-e681-43b4-b98b-a3b67267736f
  Args:
    source: :JuanCarlosI
    type: :Person
  AssignClass (befff505-7b3b-424f-9084-da2dbb892211)
 Call ID: befff505-7b3b-424f-9084-da2dbb892211
  Args:
    source: :SofiaofSpain
    type: :Woman
  AssignClass (caff075b-dfb9-43be-9ae0-31c8f87f2e21)
 Call ID: caff075b-dfb9-43be-9ae0-31c8f87f2e21
  Args:
    source: :SofiaofSpain
    type: :Person
  AddTriple (80ae6a67-6713-4b9d-9ef2-e3243df600b7)
 Call ID: 80ae6a67-6713-4b9d-9ef2-e3243df600b7
  Args:
    relation: :hasMother
    source: :InfantaElenaDuchessofLugo
    target: :SofiaofSpain
  AddTriple (27082493-ad0c-4bfb-8f1e-fe700b5a2f7f)
 Call ID: 27082493-ad0c-4bfb-8f1e-fe700b5a2f7f
  Args:
    source: :InfantaElenaDuchessofLugo
    target: :JuanCarlosI
    relation: :hasFather
  AssignClass (86bc5bf8-7633-4565-9c56-8f6d5e5ef3ce)
 Call ID: 86bc5bf8-7633-4565-9c56-8f6d5e5ef3ce
  Args:
    type: :Man
    source: :AmaliodeMarichalaryBruguera
  AssignClass (1503acac-2482-4bcb-81b7-2a3a01bf3eb4)
 Call ID: 1503acac-2482-4bcb-81b7-2a3a01bf3eb4
  Args:
    source: :AmaliodeMarichalaryBruguera
    type: :Person
  AssignClass (49751bf2-7fc7-4472-a3e0-c0976fb364cf)
 Call ID: 49751bf2-7fc7-4472-a3e0-c0976fb364cf
  Args:
    type: :Woman
    source: :ConcepcionSaenzdeTejada
  AssignClass (ec6e9b66-c9da-4fc4-9604-c8aea7995d64)
 Call ID: ec6e9b66-c9da-4fc4-9604-c8aea7995d64
  Args:
    type: :Person
    source: :ConcepcionSaenzdeTejada
  AddTriple (7f0fea58-430c-4762-8471-158ecd7edeb9)
 Call ID: 7f0fea58-430c-4762-8471-158ecd7edeb9
  Args:
    source: :JaimedeMarichalar
    target: :AmaliodeMarichalaryBruguera
    relation: :hasFather
  AddTriple (a39eb15b-a25d-464c-96ed-d57c3bcf9f0d)
 Call ID: a39eb15b-a25d-464c-96ed-d57c3bcf9f0d
  Args:
    source: :JaimedeMarichalar
    target: :ConcepcionSaenzdeTejada
    relation: :hasMother
  AssignClass (aa41e90a-3cc1-47d7-959a-5418b173e6ac)
 Call ID: aa41e90a-3cc1-47d7-959a-5418b173e6ac
  Args:
    type: :Woman
    source: :VictoriaDeMarichalaryBorbon
  AssignClass (f52febd9-40b3-41d9-82dc-c2251c5ec09c)
 Call ID: f52febd9-40b3-41d9-82dc-c2251c5ec09c
  Args:
    type: :Person
    source: :VictoriaDeMarichalaryBorbon
  AddTriple (6627352c-ac6f-4567-a7f7-1273e9c0368b)
 Call ID: 6627352c-ac6f-4567-a7f7-1273e9c0368b
  Args:
    source: :FelipeJuanFroilandeTodoslosSantosdeMarichalaryBorbon
    target: :VictoriaDeMarichalaryBorbon
    relation: :hasSister
  AddTriple (d2c1247f-d282-40e5-b627-3684704f439b)
 Call ID: d2c1247f-d282-40e5-b627-3684704f439b
  Args:
    relation: :hasMother
    source: :VictoriaDeMarichalaryBorbon
    target: :InfantaElenaDuchessofLugo
  AddTriple (2542c193-abb0-4045-a86f-5eab81c8d480)
 Call ID: 2542c193-abb0-4045-a86f-5eab81c8d480
  Args:
    relation: :hasFather
    source: :VictoriaDeMarichalaryBorbon
    target: :JaimedeMarichalar
  Finish (8c7dab00-8556-4a6c-99f0-a8f17fd32654)
 Call ID: 8c7dab00-8556-4a6c-99f0-a8f17fd32654
  Args: