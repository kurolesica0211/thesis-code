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
Louis Alphonse de Bourbon, Duke of Anjou (Spanish: Luis Alfonso Gonzalo Víctor Manuel Marco de Borbón y Martínez-Bordiú; born 25 April 1974) is regarded by French Legitimists as the head of the House of Bourbon and the rightful claimant to the defunct throne of France under the name Louis XX.
His claim is based on his descent from Louis XIV (r. 1643–1715) through his grandson Philip V of Spain.
The rival Orleanist pretenders argue that this, as well as being born a Spanish citizen, makes Louis Alphonse ineligible for the throne.
Louis Alphonse is patrilineally the senior great-grandson of King Alfonso XIII of Spain.
His grandfather Infante Jaime, Duke of Segovia, renounced his rights to the Spanish throne for himself and his descendants owing to his deafness.
Since the death of his father in 1989, he has used the courtesy title of Duke of Anjou.
Early life

Birth

Louis Alphonse was born in Madrid, the second son of Alfonso de Borbón, Duke of Anjou and Cádiz, and of his wife María del Carmen Martínez-Bordiú y Franco, eldest granddaughter of Francisco Franco.
Alfonso was at that time the dauphin (using "Duke of Bourbon" as title of pretence) according to those who supported the claim of his father, Infante Jaime, Duke of Segovia to the French throne.
On 20 March 1975, Jaime died, and Alfonso then asserted his claim to be Head of the House of Bourbon and Legitimist claimant to the throne of France.
As such, he took the title "Duke of Anjou".
Childhood

Louis Alphonse's parents separated in 1982, and their Catholic marriage was annulled in 1986.
On 7 February 1984, Louis Alphonse's older brother Francisco died as the result of a car crash in which Louis Alphonse was also injured, although less so than their father, who was driving the automobile.
From that date Louis Alphonse was recognised as the heir apparent to his father by the Legitimists.
As such, he was given the additional title Duke of Bourbon on 27 September 1984 by his father.
In 1987, the Spanish government declared that titles traditionally attached to the dynasty (such as the Dukedom of Cádiz) would henceforth be borne by its members on a lifetime only basis, forestalling Louis Alphonse from inheriting that grandeeship.
Education

Louis Alphonse took his primary studies at College Molière, a bilingual school, where he earned his baccalaureate.
Louis is multilingual, speaking English, Spanish, and French (in addition to some Italian and German).
In 1994, Louis Alphonse received 150 million pesetas from a lawsuit against Vail Associates, which owned the ski resort where the accident occurred.
Louis Alphonse was recognised by some members of the Capetian dynasty as Chef de la Maison de Bourbon (Head of the House of Bourbon) and took the title Duke of Anjou, but not his father's Spanish dukedom.
Louis Alphonse was the heir apparent to his mother's Spanish Dukedom of Franco and Grandeeship until the abolition of the titles by the Democratic Memory Law.
In 2002, Louis Alphonse was elected by the French Society of the Cincinnati as the representative of Louis XVI.
In addition to his Spanish citizenship, Louis Alphonse acquired French nationality through his paternal grandmother, Emmanuelle de Dampierre, also a French citizen.
In 2017, Louis Alphonse stated that he wishes for the remains of his ancestors, including King Charles X, to remain at the Kostanjevica Monastery, after a movement reportedly began to have the King's remains moved to be buried along with other French monarchs in Basilica of St Denis.
In 2021, Louis Alphonse attended the wedding of Grand Duke George Mikhailovich of Russia.
I consider it my role as head of the House of Bourbon and heir of the dynasty that made France to speak on the issue...At a moment of decision, I hope that the monarchical legacy of which I am the trustee is still sufficiently vibrant in the heart of my compatriots to be a source of inspiration and, I must say, hope."
- Louis Alphonse de Bourbon, in October 2025, amid the 2024–2025 French political crisis.
Louis Alphonse describes himself as a monarchist, "but not anti-republican".
In March 2018, Louis Alphonse was named honorary president of the Francisco Franco National Foundation, a position held by his grandmother, Carmen Franco, 1st Duchess of Franco, until her death in December 2017.
On 15 July, later that year, he headed a Movement-for-Spain demonstration at the Valley of the Fallen monument, leading supporters of the late Spanish dictator, his great-grandfather Francisco Franco.
They opposed the Spanish social democratic government's plan to remove Franco's remains from a basilica near Madrid.
"


Marriage and children

Louis Alphonse's engagement to marry María Margarita Vargas Santaella, the daughter of Venezuelan businessman Victor Vargas, was announced in November 2003.
Although no official reason was given, it was no secret that the then king of Spain, Juan Carlos I, did not approve his cousin's claim to the French throne, nor the fact that Louis Alphonse issued the wedding invitations styled as "Duke of Anjou".
Louis Alphonse and María Margarita had their first child, Eugénie, on 5 March 2007 at Mount Sinai Medical Center in Miami, Florida.
Her godparents are Prince Charles-Emmanuel of Bourbon-Parma and his wife, Constance.
French Legitimists recognize her as Eugénie, Madame Royale,: 47  the style commonly attributed to the eldest unmarried daughter of a king of France (in Spain her name is Dona Eugenia de Borbón y Vargas).
: 47 


The couple had twin sons, Louis and Alphonse, on 28 May 2010 in New York City.
Their father has conferred upon them the historic French titles of, respectively, Duke of Burgundy (duc de Bourgogne) and Duke of Berry (duc de Berry).
In Spain, the twins are Don Luis and Don Alfonso de Borbón y Vargas.:
47 


Their fourth child, Henri, was born on 1 February 2019 in New York and was granted the title of Duke of Touraine (duc de Touraine) by his father.



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
  AssignClass (ef5fc239-5ab2-4477-a409-c485b4495fa8)
 Call ID: ef5fc239-5ab2-4477-a409-c485b4495fa8
  Args:
    type: :Man
    source: Louis_Alphonse_de_Bourbon
  AssignClass (23f3452c-cfca-47b6-b983-9af61898e7f6)
 Call ID: 23f3452c-cfca-47b6-b983-9af61898e7f6
  Args:
    type: :Man
    source: Alfonso_de_Borbon_Duke_of_Anjou_and_Cadiz
  AssignClass (3d3a1920-a8cb-4e7a-8370-9b27b58540c9)
 Call ID: 3d3a1920-a8cb-4e7a-8370-9b27b58540c9
  Args:
    type: :Woman
    source: Maria_del_Carmen_Martinez-Bordiu_y_Franco
  AssignClass (0aaa170f-1883-4def-be53-599b0a044891)
 Call ID: 0aaa170f-1883-4def-be53-599b0a044891
  Args:
    type: :Man
    source: Francisco_Franco
  AssignClass (13f0f83c-c1b9-4ebf-8152-6382860d9c9a)
 Call ID: 13f0f83c-c1b9-4ebf-8152-6382860d9c9a
  Args:
    type: :Man
    source: Infante_Jaime_Duke_of_Segovia
  AssignClass (9a0373e5-9b17-4155-85ba-f29ac831b86f)
 Call ID: 9a0373e5-9b17-4155-85ba-f29ac831b86f
  Args:
    type: :Man
    source: Francisco_de_Borbon
  AssignClass (523e5ffa-56e7-4668-b7b2-f3d37d79aa1c)
 Call ID: 523e5ffa-56e7-4668-b7b2-f3d37d79aa1c
  Args:
    type: :Woman
    source: Emmanuelle_de_Dampierre
  AssignClass (857f0c6c-3f39-4a7e-82a4-b86bd6888e28)
 Call ID: 857f0c6c-3f39-4a7e-82a4-b86bd6888e28
  Args:
    type: :Woman
    source: Maria_Margarita_Vargas_Santaella
  AssignClass (c3356b9b-d130-4222-acb4-c19a07215796)
 Call ID: c3356b9b-d130-4222-acb4-c19a07215796
  Args:
    type: :Man
    source: Victor_Vargas
  AssignClass (443e4741-e400-4921-8008-38500b24e1f9)
 Call ID: 443e4741-e400-4921-8008-38500b24e1f9
  Args:
    type: :Woman
    source: Eugenie_de_Borbon_y_Vargas
  AssignClass (e5bc619a-29d8-4d15-a116-dea51765862f)
 Call ID: e5bc619a-29d8-4d15-a116-dea51765862f
  Args:
    type: :Man
    source: Louis_de_Borbon_y_Vargas
  AssignClass (7c922762-b258-46fd-866c-0263eda37575)
 Call ID: 7c922762-b258-46fd-866c-0263eda37575
  Args:
    type: :Man
    source: Alphonse_de_Borbon_y_Vargas
  AssignClass (7eedd762-bba9-4bb9-97c1-72e9c938e25d)
 Call ID: 7eedd762-bba9-4bb9-97c1-72e9c938e25d
  Args:
    type: :Man
    source: Henri_de_Borbon_y_Vargas
  AddLiteral (94f52980-2e9b-481e-9bb4-553118df1f38)
 Call ID: 94f52980-2e9b-481e-9bb4-553118df1f38
  Args:
    source: Louis_Alphonse_de_Bourbon
    literal_type: xsd:positiveInteger
    relation: :hasBirthYear
    literal_value: 1974
  AddTriple (321b1bc5-0410-4697-a1a4-e8075fdc9d3c)
 Call ID: 321b1bc5-0410-4697-a1a4-e8075fdc9d3c
  Args:
    target: Alfonso_de_Borbon_Duke_of_Anjou_and_Cadiz
    source: Louis_Alphonse_de_Bourbon
    relation: :hasFather
  AddTriple (f0a53bb0-0573-49e1-a9ab-cd68eb37f991)
 Call ID: f0a53bb0-0573-49e1-a9ab-cd68eb37f991
  Args:
    source: Louis_Alphonse_de_Bourbon
    relation: :hasMother
    target: Maria_del_Carmen_Martinez-Bordiu_y_Franco
  AddTriple (031d8ed1-149b-4734-ae69-1f518801be66)
 Call ID: 031d8ed1-149b-4734-ae69-1f518801be66
  Args:
    relation: :hasFather
    source: Alfonso_de_Borbon_Duke_of_Anjou_and_Cadiz
    target: Infante_Jaime_Duke_of_Segovia
  AddTriple (6101fa18-9a14-48b0-b71d-807bb2d83e3a)
 Call ID: 6101fa18-9a14-48b0-b71d-807bb2d83e3a
  Args:
    source: Maria_del_Carmen_Martinez-Bordiu_y_Franco
    relation: :hasMother
    target: Carmen_Franco_1st_Duchess_of_Franco
  AssignClass (159ddad3-3c29-41fb-8b59-292eccb70989)
 Call ID: 159ddad3-3c29-41fb-8b59-292eccb70989
  Args:
    type: :Woman
    source: Carmen_Franco_1st_Duchess_of_Franco
  AddTriple (9dd9e911-d927-4852-9772-6cb1ce2f13b7)
 Call ID: 9dd9e911-d927-4852-9772-6cb1ce2f13b7
  Args:
    target: Francisco_Franco
    relation: :hasFather
    source: Carmen_Franco_1st_Duchess_of_Franco
  AddTriple (87ffa198-0d6e-414d-8e48-f00f7c4c83a9)
 Call ID: 87ffa198-0d6e-414d-8e48-f00f7c4c83a9
  Args:
    target: Francisco_de_Borbon
    relation: :hasBrother
    source: Louis_Alphonse_de_Bourbon
  AddTriple (77c3d062-c3f0-444a-9a84-c3c969644e4e)
 Call ID: 77c3d062-c3f0-444a-9a84-c3c969644e4e
  Args:
    relation: :hasFather
    source: Francisco_de_Borbon
    target: Alfonso_de_Borbon_Duke_of_Anjou_and_Cadiz
  AddTriple (2d11fda0-1051-4447-8c5a-5f49b89b4ad5)
 Call ID: 2d11fda0-1051-4447-8c5a-5f49b89b4ad5
  Args:
    relation: :hasMother
    source: Francisco_de_Borbon
    target: Maria_del_Carmen_Martinez-Bordiu_y_Franco
  AddTriple (f4973cad-be64-4da2-8434-496d00aab9f5)
 Call ID: f4973cad-be64-4da2-8434-496d00aab9f5
  Args:
    relation: :hasMother
    source: Alfonso_de_Borbon_Duke_of_Anjou_and_Cadiz
    target: Emmanuelle_de_Dampierre
  AddTriple (2e9397f6-aef4-4e7b-abed-e86f047b621a)
 Call ID: 2e9397f6-aef4-4e7b-abed-e86f047b621a
  Args:
    relation: :hasMother
    source: Eugenie_de_Borbon_y_Vargas
    target: Maria_Margarita_Vargas_Santaella
  AddTriple (0233632a-06da-4f1e-a20a-669db9937617)
 Call ID: 0233632a-06da-4f1e-a20a-669db9937617
  Args:
    target: Louis_Alphonse_de_Bourbon
    relation: :hasFather
    source: Eugenie_de_Borbon_y_Vargas
  AddTriple (2a9f4ee2-b02d-46a1-92cc-634cdf7b2627)
 Call ID: 2a9f4ee2-b02d-46a1-92cc-634cdf7b2627
  Args:
    source: Louis_de_Borbon_y_Vargas
    relation: :hasMother
    target: Maria_Margarita_Vargas_Santaella
  AddTriple (69bbcee9-a06c-4968-9bbd-24b412dbe949)
 Call ID: 69bbcee9-a06c-4968-9bbd-24b412dbe949
  Args:
    target: Louis_Alphonse_de_Bourbon
    relation: :hasFather
    source: Louis_de_Borbon_y_Vargas
  AddTriple (35393f59-925f-4184-a764-3bf9691387c8)
 Call ID: 35393f59-925f-4184-a764-3bf9691387c8
  Args:
    relation: :hasMother
    source: Alphonse_de_Borbon_y_Vargas
    target: Maria_Margarita_Vargas_Santaella
  AddTriple (ebe2a0ee-d55d-4159-99fb-106fb008f6ee)
 Call ID: ebe2a0ee-d55d-4159-99fb-106fb008f6ee
  Args:
    target: Louis_Alphonse_de_Bourbon
    source: Alphonse_de_Borbon_y_Vargas
    relation: :hasFather
  AddTriple (13e03987-2322-4576-92dc-a2d084628583)
 Call ID: 13e03987-2322-4576-92dc-a2d084628583
  Args:
    source: Henri_de_Borbon_y_Vargas
    relation: :hasMother
    target: Maria_Margarita_Vargas_Santaella
  AddTriple (334c982e-8b15-4a92-8a6a-a3ffd2078e1f)
 Call ID: 334c982e-8b15-4a92-8a6a-a3ffd2078e1f
  Args:
    relation: :hasFather
    source: Henri_de_Borbon_y_Vargas
    target: Louis_Alphonse_de_Bourbon
  AddTriple (a7a10430-871b-4e91-b399-669292510db1)
 Call ID: a7a10430-871b-4e91-b399-669292510db1
  Args:
    target: Victor_Vargas
    relation: :hasFather
    source: Maria_Margarita_Vargas_Santaella
  Finish (d85705da-5c8b-4259-ba4a-0df4407849e1)
 Call ID: d85705da-5c8b-4259-ba4a-0df4407849e1
  Args: