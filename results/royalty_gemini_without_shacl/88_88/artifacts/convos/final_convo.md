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
  AssignClass (771b7047-61e8-4459-bcb0-8257c6bf5694)
 Call ID: 771b7047-61e8-4459-bcb0-8257c6bf5694
  Args:
    source: Louis_Alphonse_de_Bourbon
    type: :Man
  AddLiteral (d4cfd72e-3e36-47ca-ae8b-85cced203209)
 Call ID: d4cfd72e-3e36-47ca-ae8b-85cced203209
  Args:
    source: Louis_Alphonse_de_Bourbon
    literal_type: xsd:integer
    literal_value: 1974
    relation: :hasBirthYear
  AssignClass (d0063df2-5fd0-4da4-aa83-2b696167d5eb)
 Call ID: d0063df2-5fd0-4da4-aa83-2b696167d5eb
  Args:
    source: Alfonso_de_Borbon
    type: :Man
  AssignClass (3c80ebc5-508c-4794-8c1a-c3cbeeff3cec)
 Call ID: 3c80ebc5-508c-4794-8c1a-c3cbeeff3cec
  Args:
    source: Maria_del_Carmen_Martinez-Bordiu_y_Franco
    type: :Woman
  AddTriple (6889b332-f65e-4a0f-8ced-77edccf26c3e)
 Call ID: 6889b332-f65e-4a0f-8ced-77edccf26c3e
  Args:
    source: Louis_Alphonse_de_Bourbon
    target: Alfonso_de_Borbon
    relation: :hasFather
  AddTriple (a40cbe36-a258-4cdd-b603-1443ff20bbeb)
 Call ID: a40cbe36-a258-4cdd-b603-1443ff20bbeb
  Args:
    source: Louis_Alphonse_de_Bourbon
    target: Maria_del_Carmen_Martinez-Bordiu_y_Franco
    relation: :hasMother
  AssignClass (0144a540-278d-4686-a8d7-949c4e7b6f46)
 Call ID: 0144a540-278d-4686-a8d7-949c4e7b6f46
  Args:
    source: Francisco_de_Borbon
    type: :Man
  AddTriple (cdb94581-10f2-45c6-b902-6888d6bf2a05)
 Call ID: cdb94581-10f2-45c6-b902-6888d6bf2a05
  Args:
    target: Francisco_de_Borbon
    source: Louis_Alphonse_de_Bourbon
    relation: :hasBrother
  AddTriple (7ba1695d-6a51-479a-b342-e0814ca822a7)
 Call ID: 7ba1695d-6a51-479a-b342-e0814ca822a7
  Args:
    source: Francisco_de_Borbon
    target: Alfonso_de_Borbon
    relation: :hasFather
  AddTriple (d7dad328-1ebd-4eff-85b9-f40b37ea1585)
 Call ID: d7dad328-1ebd-4eff-85b9-f40b37ea1585
  Args:
    source: Francisco_de_Borbon
    target: Maria_del_Carmen_Martinez-Bordiu_y_Franco
    relation: :hasMother
  AssignClass (f9916349-4baf-4d4e-946c-384815b3ce41)
 Call ID: f9916349-4baf-4d4e-946c-384815b3ce41
  Args:
    source: Infante_Jaime_Duke_of_Segovia
    type: :Man
  AddTriple (12d0271f-4f3e-425c-97a2-a3154da38459)
 Call ID: 12d0271f-4f3e-425c-97a2-a3154da38459
  Args:
    target: Infante_Jaime_Duke_of_Segovia
    source: Alfonso_de_Borbon
    relation: :hasFather
  AssignClass (8ca172eb-c5df-4b26-99ea-7b3ede7d181f)
 Call ID: 8ca172eb-c5df-4b26-99ea-7b3ede7d181f
  Args:
    source: Emmanuelle_de_Dampierre
    type: :Woman
  AddTriple (4547a890-84c9-46da-957e-8d6c85409845)
 Call ID: 4547a890-84c9-46da-957e-8d6c85409845
  Args:
    source: Alfonso_de_Borbon
    target: Emmanuelle_de_Dampierre
    relation: :hasMother
  AssignClass (27b2cf24-6850-4f8e-90df-44251dcf7e41)
 Call ID: 27b2cf24-6850-4f8e-90df-44251dcf7e41
  Args:
    source: Francisco_Franco
    type: :Man
  AssignClass (31e52707-a334-449c-887e-668ae46afb1c)
 Call ID: 31e52707-a334-449c-887e-668ae46afb1c
  Args:
    source: Carmen_Franco_1st_Duchess_of_Franco
    type: :Woman
  AddTriple (01b85726-7359-46b6-9594-493f15a37a8b)
 Call ID: 01b85726-7359-46b6-9594-493f15a37a8b
  Args:
    relation: :hasMother
    source: Maria_del_Carmen_Martinez-Bordiu_y_Franco
    target: Carmen_Franco_1st_Duchess_of_Franco
  AddTriple (99b2cb2c-15c2-4bbe-82b8-e9224a74defd)
 Call ID: 99b2cb2c-15c2-4bbe-82b8-e9224a74defd
  Args:
    relation: :hasFather
    source: Carmen_Franco_1st_Duchess_of_Franco
    target: Francisco_Franco
  AssignClass (7a2116be-d4e1-49ab-b0db-898acd1bc0db)
 Call ID: 7a2116be-d4e1-49ab-b0db-898acd1bc0db
  Args:
    source: Maria_Margarita_Vargas_Santaella
    type: :Woman
  AssignClass (9d6dc8b7-a1bc-4ccf-881e-fb60a27eb5ab)
 Call ID: 9d6dc8b7-a1bc-4ccf-881e-fb60a27eb5ab
  Args:
    source: Victor_Vargas
    type: :Man
  AddTriple (5c1607ab-5d05-4f5a-a756-5830d90e8a2d)
 Call ID: 5c1607ab-5d05-4f5a-a756-5830d90e8a2d
  Args:
    target: Victor_Vargas
    source: Maria_Margarita_Vargas_Santaella
    relation: :hasFather
  AssignClass (bd2c287f-09b9-40ef-bbc0-d4b5be4b736c)
 Call ID: bd2c287f-09b9-40ef-bbc0-d4b5be4b736c
  Args:
    source: Eugenie_de_Borbon_y_Vargas
    type: :Woman
  AddTriple (6b49d6d3-509c-4492-b3b9-ed59e0be54fe)
 Call ID: 6b49d6d3-509c-4492-b3b9-ed59e0be54fe
  Args:
    relation: :hasFather
    source: Eugenie_de_Borbon_y_Vargas
    target: Louis_Alphonse_de_Bourbon
  AddTriple (eb217852-58f4-4b3c-90ca-2c6a81f8b6ed)
 Call ID: eb217852-58f4-4b3c-90ca-2c6a81f8b6ed
  Args:
    source: Eugenie_de_Borbon_y_Vargas
    target: Maria_Margarita_Vargas_Santaella
    relation: :hasMother
  AssignClass (3fb13b45-c4c8-4b70-9f9b-e31180f0bd00)
 Call ID: 3fb13b45-c4c8-4b70-9f9b-e31180f0bd00
  Args:
    source: Louis_de_Borbon_y_Vargas
    type: :Man
  AddTriple (8b412c8a-ce29-41de-b9a2-ff4b09fe0393)
 Call ID: 8b412c8a-ce29-41de-b9a2-ff4b09fe0393
  Args:
    relation: :hasFather
    source: Louis_de_Borbon_y_Vargas
    target: Louis_Alphonse_de_Bourbon
  AddTriple (ad690aaf-7517-44c2-b856-7979d428b8a5)
 Call ID: ad690aaf-7517-44c2-b856-7979d428b8a5
  Args:
    target: Maria_Margarita_Vargas_Santaella
    source: Louis_de_Borbon_y_Vargas
    relation: :hasMother
  AssignClass (9afebbda-ac02-4233-a220-3af1005df9e0)
 Call ID: 9afebbda-ac02-4233-a220-3af1005df9e0
  Args:
    source: Alphonse_de_Borbon_y_Vargas
    type: :Man
  AddTriple (d2c901d0-6297-4b98-b364-d38263e3dda0)
 Call ID: d2c901d0-6297-4b98-b364-d38263e3dda0
  Args:
    relation: :hasFather
    source: Alphonse_de_Borbon_y_Vargas
    target: Louis_Alphonse_de_Bourbon
  AddTriple (f8ac3305-7c89-4088-87cc-f9f87468c036)
 Call ID: f8ac3305-7c89-4088-87cc-f9f87468c036
  Args:
    target: Maria_Margarita_Vargas_Santaella
    source: Alphonse_de_Borbon_y_Vargas
    relation: :hasMother
  AssignClass (6679f739-1e53-44f6-8ce8-58093854bdd5)
 Call ID: 6679f739-1e53-44f6-8ce8-58093854bdd5
  Args:
    source: Henri_de_Borbon_y_Vargas
    type: :Man
  AddTriple (ca8c3e1f-f4a7-4e4a-a251-e3df51495d21)
 Call ID: ca8c3e1f-f4a7-4e4a-a251-e3df51495d21
  Args:
    target: Louis_Alphonse_de_Bourbon
    source: Henri_de_Borbon_y_Vargas
    relation: :hasFather
  AddTriple (223ab1fe-2945-4476-8784-be9d113fc935)
 Call ID: 223ab1fe-2945-4476-8784-be9d113fc935
  Args:
    relation: :hasMother
    target: Maria_Margarita_Vargas_Santaella
    source: Henri_de_Borbon_y_Vargas
  Finish (490f614d-a1e2-4b23-a343-6e36b70c1381)
 Call ID: 490f614d-a1e2-4b23-a343-6e36b70c1381
  Args: