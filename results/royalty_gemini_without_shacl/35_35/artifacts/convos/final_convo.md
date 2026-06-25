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
  AssignClass (b7d5aeb3-8967-4c41-bcab-32156d9a7a90)
 Call ID: b7d5aeb3-8967-4c41-bcab-32156d9a7a90
  Args:
    type: :Man
    source: Louis_Alphonse_de_Bourbon
  AssignClass (e6585b07-eec4-46e0-a19c-392d0705cccd)
 Call ID: e6585b07-eec4-46e0-a19c-392d0705cccd
  Args:
    source: Alfonso_de_Borbon
    type: :Man
  AssignClass (9bf409f7-0dc3-456a-97f2-810d3fc21143)
 Call ID: 9bf409f7-0dc3-456a-97f2-810d3fc21143
  Args:
    source: Maria_del_Carmen_Martinez-Bordiu_y_Franco
    type: :Woman
  AssignClass (21eead22-5a7a-4620-bae9-67cfc4c34c69)
 Call ID: 21eead22-5a7a-4620-bae9-67cfc4c34c69
  Args:
    type: :Man
    source: Francisco_Franco
  AssignClass (91bb7990-399f-46e0-987c-bd894cc969da)
 Call ID: 91bb7990-399f-46e0-987c-bd894cc969da
  Args:
    source: Infante_Jaime
    type: :Man
  AssignClass (888742ca-d7f4-4452-9c50-db6b6b4bc9da)
 Call ID: 888742ca-d7f4-4452-9c50-db6b6b4bc9da
  Args:
    type: :Man
    source: Francisco_de_Borbon
  AssignClass (0c80de8f-8ef2-4e4b-bbde-1e5ec2663081)
 Call ID: 0c80de8f-8ef2-4e4b-bbde-1e5ec2663081
  Args:
    source: Alfonso_XIII
    type: :Man
  AssignClass (78b0e2d5-350b-4a80-8389-cd820ff51455)
 Call ID: 78b0e2d5-350b-4a80-8389-cd820ff51455
  Args:
    type: :Woman
    source: Emmanuelle_de_Dampierre
  AssignClass (93ad9582-4084-4926-8b2e-db7d07c59939)
 Call ID: 93ad9582-4084-4926-8b2e-db7d07c59939
  Args:
    type: :Woman
    source: Maria_Margarita_Vargas_Santaella
  AssignClass (6f340255-67bb-4dc2-8952-186c1fc79b57)
 Call ID: 6f340255-67bb-4dc2-8952-186c1fc79b57
  Args:
    type: :Man
    source: Victor_Vargas
  AssignClass (a984a798-0cb6-4568-9e0f-633b34c73890)
 Call ID: a984a798-0cb6-4568-9e0f-633b34c73890
  Args:
    type: :Woman
    source: Eugenie_de_Borbon_y_Vargas
  AssignClass (a43cbc09-5c23-4aa0-be59-a50845b32e68)
 Call ID: a43cbc09-5c23-4aa0-be59-a50845b32e68
  Args:
    source: Louis_de_Borbon_y_Vargas
    type: :Man
  AssignClass (053cbef2-6f04-4cc9-ad91-1f52540e40e2)
 Call ID: 053cbef2-6f04-4cc9-ad91-1f52540e40e2
  Args:
    source: Alphonse_de_Borbon_y_Vargas
    type: :Man
  AssignClass (52241923-42ea-4313-9758-c499d6ef935c)
 Call ID: 52241923-42ea-4313-9758-c499d6ef935c
  Args:
    source: Henri_de_Borbon_y_Vargas
    type: :Man
  AssignClass (263d2f73-b9b2-40aa-b4ea-9e9ffa12f34c)
 Call ID: 263d2f73-b9b2-40aa-b4ea-9e9ffa12f34c
  Args:
    source: Carmen_Franco
    type: :Woman
  AddLiteral (f8d78fe6-ef37-421f-be78-4bb5556b42d7)
 Call ID: f8d78fe6-ef37-421f-be78-4bb5556b42d7
  Args:
    literal_value: 1974
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Louis_Alphonse_de_Bourbon
  AddTriple (a6161c24-d181-4d43-918a-9c49f86a4845)
 Call ID: a6161c24-d181-4d43-918a-9c49f86a4845
  Args:
    source: Louis_Alphonse_de_Bourbon
    target: Alfonso_de_Borbon
    relation: :hasFather
  AddTriple (2d6263d5-7a97-402c-b8f4-6cd22c49ff16)
 Call ID: 2d6263d5-7a97-402c-b8f4-6cd22c49ff16
  Args:
    source: Louis_Alphonse_de_Bourbon
    target: Maria_del_Carmen_Martinez-Bordiu_y_Franco
    relation: :hasMother
  AddTriple (c6938390-f11f-4854-8061-40a5dc7a9e6b)
 Call ID: c6938390-f11f-4854-8061-40a5dc7a9e6b
  Args:
    source: Alfonso_de_Borbon
    target: Infante_Jaime
    relation: :hasFather
  AddTriple (e2b8f054-a3ac-4c6a-b016-6739363531c1)
 Call ID: e2b8f054-a3ac-4c6a-b016-6739363531c1
  Args:
    source: Louis_Alphonse_de_Bourbon
    relation: :hasFather
    target: Francisco_de_Borbon
  AddTriple (8b57de55-04a7-41d0-9f24-fa798e2e6483)
 Call ID: 8b57de55-04a7-41d0-9f24-fa798e2e6483
  Args:
    target: Alfonso_XIII
    relation: :hasFather
    source: Infante_Jaime
  AddTriple (f3c32d4b-1392-44ba-85a0-5e5af17dad6b)
 Call ID: f3c32d4b-1392-44ba-85a0-5e5af17dad6b
  Args:
    source: Alfonso_de_Borbon
    relation: :hasMother
    target: Emmanuelle_de_Dampierre
  AddTriple (b37c0246-de62-4d0c-b82e-a2def37e3711)
 Call ID: b37c0246-de62-4d0c-b82e-a2def37e3711
  Args:
    target: Francisco_Franco
    relation: :hasFather
    source: Maria_del_Carmen_Martinez-Bordiu_y_Franco
  AddTriple (c5ac2b6b-a022-4b67-91ff-9a29ebec96a1)
 Call ID: c5ac2b6b-a022-4b67-91ff-9a29ebec96a1
  Args:
    source: Eugenie_de_Borbon_y_Vargas
    relation: :hasFather
    target: Louis_Alphonse_de_Bourbon
  AddTriple (fc5b6ece-5201-4460-8bc6-c81b4f89bd36)
 Call ID: fc5b6ece-5201-4460-8bc6-c81b4f89bd36
  Args:
    relation: :hasMother
    target: Maria_Margarita_Vargas_Santaella
    source: Eugenie_de_Borbon_y_Vargas
  AddTriple (d5fcd96a-d76e-477d-aa76-19361a853c3f)
 Call ID: d5fcd96a-d76e-477d-aa76-19361a853c3f
  Args:
    source: Louis_de_Borbon_y_Vargas
    target: Louis_Alphonse_de_Bourbon
    relation: :hasFather
  AddTriple (e2009629-4663-45eb-97ab-93389911dd95)
 Call ID: e2009629-4663-45eb-97ab-93389911dd95
  Args:
    relation: :hasMother
    target: Maria_Margarita_Vargas_Santaella
    source: Louis_de_Borbon_y_Vargas
  AddTriple (babf1f90-71e6-4d58-b944-f5b9ca275c3b)
 Call ID: babf1f90-71e6-4d58-b944-f5b9ca275c3b
  Args:
    source: Alphonse_de_Borbon_y_Vargas
    target: Louis_Alphonse_de_Bourbon
    relation: :hasFather
  AddTriple (fe66985c-0b15-42ee-8c40-7972b44ad136)
 Call ID: fe66985c-0b15-42ee-8c40-7972b44ad136
  Args:
    source: Alphonse_de_Borbon_y_Vargas
    relation: :hasMother
    target: Maria_Margarita_Vargas_Santaella
  AddTriple (4045e469-7580-450d-8c5f-a1b474b1e628)
 Call ID: 4045e469-7580-450d-8c5f-a1b474b1e628
  Args:
    target: Louis_Alphonse_de_Bourbon
    relation: :hasFather
    source: Henri_de_Borbon_y_Vargas
  AddTriple (6263f786-5ae5-498e-8a8c-124841210892)
 Call ID: 6263f786-5ae5-498e-8a8c-124841210892
  Args:
    relation: :hasMother
    target: Maria_Margarita_Vargas_Santaella
    source: Henri_de_Borbon_y_Vargas
  AddTriple (1143ff51-26f7-4469-ae93-b136311b1b20)
 Call ID: 1143ff51-26f7-4469-ae93-b136311b1b20
  Args:
    target: Victor_Vargas
    relation: :hasFather
    source: Maria_Margarita_Vargas_Santaella
  AddTriple (6e4705f3-960d-4980-899b-24061f2523d7)
 Call ID: 6e4705f3-960d-4980-899b-24061f2523d7
  Args:
    relation: :hasMother
    target: Carmen_Franco
    source: Maria_del_Carmen_Martinez-Bordiu_y_Franco
  Finish (5aa146d9-5bf7-47a7-b4a1-a8b34ee1cb0f)
 Call ID: 5aa146d9-5bf7-47a7-b4a1-a8b34ee1cb0f
  Args: