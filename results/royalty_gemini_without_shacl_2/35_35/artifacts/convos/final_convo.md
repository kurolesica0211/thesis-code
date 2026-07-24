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
  AssignClass (bf9a9e99-c9c7-4fec-af4f-c55c2d033d06)
 Call ID: bf9a9e99-c9c7-4fec-af4f-c55c2d033d06
  Args:
    type: :Man
    source: Louis_Alphonse_de_Bourbon
  AssignClass (6bfdaba6-d0d2-4a05-ae63-4ab5df6b9c5a)
 Call ID: 6bfdaba6-d0d2-4a05-ae63-4ab5df6b9c5a
  Args:
    type: :Person
    source: Louis_Alphonse_de_Bourbon
  AddLiteral (3a11834b-1f2c-458a-a68d-c6482cc76d7b)
 Call ID: 3a11834b-1f2c-458a-a68d-c6482cc76d7b
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Louis_Alphonse_de_Bourbon
    literal_value: 1974
  AssignClass (22772281-0403-4e9a-a15a-4c61db4de64b)
 Call ID: 22772281-0403-4e9a-a15a-4c61db4de64b
  Args:
    type: :Man
    source: Alfonso_de_Borbon
  AssignClass (077bd7ca-7a25-476e-a15e-52d60f9df083)
 Call ID: 077bd7ca-7a25-476e-a15e-52d60f9df083
  Args:
    source: Alfonso_de_Borbon
    type: :Person
  AssignClass (057dd855-023c-4412-8abd-d314362f1863)
 Call ID: 057dd855-023c-4412-8abd-d314362f1863
  Args:
    source: Maria_del_Carmen_Martinez-Bordiu_y_Franco
    type: :Woman
  AssignClass (e8849738-e995-461a-9ba9-618d78e79ad7)
 Call ID: e8849738-e995-461a-9ba9-618d78e79ad7
  Args:
    source: Maria_del_Carmen_Martinez-Bordiu_y_Franco
    type: :Person
  AddTriple (0259ecff-cbbf-4e82-8bdc-74f377862ba1)
 Call ID: 0259ecff-cbbf-4e82-8bdc-74f377862ba1
  Args:
    relation: :hasFather
    source: Louis_Alphonse_de_Bourbon
    target: Alfonso_de_Borbon
  AddTriple (e466406d-18d6-4642-b585-2b890ea71589)
 Call ID: e466406d-18d6-4642-b585-2b890ea71589
  Args:
    relation: :hasMother
    source: Louis_Alphonse_de_Bourbon
    target: Maria_del_Carmen_Martinez-Bordiu_y_Franco
  AssignClass (39c17f1b-0acc-446e-a96d-75e3ad23630e)
 Call ID: 39c17f1b-0acc-446e-a96d-75e3ad23630e
  Args:
    source: Francisco_Bordon
    type: :Man
  AssignClass (9cfebdcd-e07d-47de-a1a8-b9880e01b550)
 Call ID: 9cfebdcd-e07d-47de-a1a8-b9880e01b550
  Args:
    type: :Person
    source: Francisco_Bordon
  AddTriple (a4cda04d-2893-483d-9690-e9a7115d5d3b)
 Call ID: a4cda04d-2893-483d-9690-e9a7115d5d3b
  Args:
    relation: :hasFather
    source: Francisco_Bordon
    target: Alfonso_de_Borbon
  AddTriple (21598e5a-b146-405a-a310-468a96481476)
 Call ID: 21598e5a-b146-405a-a310-468a96481476
  Args:
    relation: :hasMother
    source: Francisco_Bordon
    target: Maria_del_Carmen_Martinez-Bordiu_y_Franco
  AddTriple (653d7c1e-6558-46e2-a2e9-0fa8aa3819e4)
 Call ID: 653d7c1e-6558-46e2-a2e9-0fa8aa3819e4
  Args:
    source: Francisco_Bordon
    target: Louis_Alphonse_de_Bourbon
    relation: :isBrotherOf
  AssignClass (22fdf673-ea87-4f08-8293-206149ceca8f)
 Call ID: 22fdf673-ea87-4f08-8293-206149ceca8f
  Args:
    type: :Man
    source: Infante_Jaime_Duke_of_Segovia
  AssignClass (06a199ea-c6a1-4e7d-a1c6-e6033b64bb1f)
 Call ID: 06a199ea-c6a1-4e7d-a1c6-e6033b64bb1f
  Args:
    type: :Person
    source: Infante_Jaime_Duke_of_Segovia
  AddTriple (dcdcb3de-d598-4175-ad91-b301bd59514f)
 Call ID: dcdcb3de-d598-4175-ad91-b301bd59514f
  Args:
    relation: :hasFather
    source: Alfonso_de_Borbon
    target: Infante_Jaime_Duke_of_Segovia
  AssignClass (81bbcc62-949a-4c75-b25c-13169ea523fa)
 Call ID: 81bbcc62-949a-4c75-b25c-13169ea523fa
  Args:
    type: :Woman
    source: Emmanuelle_de_Dampierre
  AssignClass (8640a500-ab6b-4cdf-8d34-9b706692bf4e)
 Call ID: 8640a500-ab6b-4cdf-8d34-9b706692bf4e
  Args:
    type: :Person
    source: Emmanuelle_de_Dampierre
  AddTriple (cb748f0e-cd77-4928-a629-6ad0a2bb26e1)
 Call ID: cb748f0e-cd77-4928-a629-6ad0a2bb26e1
  Args:
    relation: :hasMother
    source: Alfonso_de_Borbon
    target: Emmanuelle_de_Dampierre
  AssignClass (5b89e9a6-8623-4554-a56e-50a2f527869b)
 Call ID: 5b89e9a6-8623-4554-a56e-50a2f527869b
  Args:
    type: :Man
    source: Francisco_Franco
  AssignClass (822888e4-cea5-4b21-a19d-3045514918c0)
 Call ID: 822888e4-cea5-4b21-a19d-3045514918c0
  Args:
    source: Francisco_Franco
    type: :Person
  AssignClass (daa4fae1-6ec7-452e-8b52-c23a365de007)
 Call ID: daa4fae1-6ec7-452e-8b52-c23a365de007
  Args:
    source: Carmen_Franco_1st_Duchess_of_Franco
    type: :Woman
  AssignClass (44963573-2a3c-405f-934b-0fc95becb913)
 Call ID: 44963573-2a3c-405f-934b-0fc95becb913
  Args:
    source: Carmen_Franco_1st_Duchess_of_Franco
    type: :Person
  AddTriple (f6330ac1-7bc6-4b76-8f35-66f5a246ab06)
 Call ID: f6330ac1-7bc6-4b76-8f35-66f5a246ab06
  Args:
    relation: :hasFather
    source: Carmen_Franco_1st_Duchess_of_Franco
    target: Francisco_Franco
  AddTriple (bab65a3a-363d-4559-a2d2-d468000910b6)
 Call ID: bab65a3a-363d-4559-a2d2-d468000910b6
  Args:
    relation: :hasMother
    source: Maria_del_Carmen_Martinez-Bordiu_y_Franco
    target: Carmen_Franco_1st_Duchess_of_Franco
  AssignClass (4738941d-2b03-4d6d-87a5-8e501f026550)
 Call ID: 4738941d-2b03-4d6d-87a5-8e501f026550
  Args:
    source: Maria_Margarita_Vargas_Santaella
    type: :Woman
  AssignClass (c7495d15-115c-4c8c-a285-80af150c04eb)
 Call ID: c7495d15-115c-4c8c-a285-80af150c04eb
  Args:
    source: Maria_Margarita_Vargas_Santaella
    type: :Person
  AssignClass (221e30dc-d2c4-4c8b-b4b5-a20e82f0f3f3)
 Call ID: 221e30dc-d2c4-4c8b-b4b5-a20e82f0f3f3
  Args:
    source: Eugenie_de_Borbon_y_Vargas
    type: :Woman
  AssignClass (0ba45efe-8590-4a9e-b13a-645c669a66e3)
 Call ID: 0ba45efe-8590-4a9e-b13a-645c669a66e3
  Args:
    type: :Person
    source: Eugenie_de_Borbon_y_Vargas
  AddTriple (d20a9540-c902-471b-9fc5-63e2f7dab6a9)
 Call ID: d20a9540-c902-471b-9fc5-63e2f7dab6a9
  Args:
    relation: :hasFather
    source: Eugenie_de_Borbon_y_Vargas
    target: Louis_Alphonse_de_Bourbon
  AddTriple (40b37d1f-af17-4b31-8aba-347a26cf57a6)
 Call ID: 40b37d1f-af17-4b31-8aba-347a26cf57a6
  Args:
    source: Eugenie_de_Borbon_y_Vargas
    target: Maria_Margarita_Vargas_Santaella
    relation: :hasMother
  AssignClass (ce099a04-71fb-4999-b022-bc22c4b439c6)
 Call ID: ce099a04-71fb-4999-b022-bc22c4b439c6
  Args:
    type: :Man
    source: Luis_de_Borbon_y_Vargas
  AssignClass (06b009b1-4551-42f3-92a7-115767c529fa)
 Call ID: 06b009b1-4551-42f3-92a7-115767c529fa
  Args:
    type: :Person
    source: Luis_de_Borbon_y_Vargas
  AddTriple (11d47b20-2fe5-46c3-ad97-17234ddf50c1)
 Call ID: 11d47b20-2fe5-46c3-ad97-17234ddf50c1
  Args:
    source: Luis_de_Borbon_y_Vargas
    target: Louis_Alphonse_de_Bourbon
    relation: :hasFather
  AddTriple (43a0282d-8182-49a1-aa89-bb1dd41271e3)
 Call ID: 43a0282d-8182-49a1-aa89-bb1dd41271e3
  Args:
    relation: :hasMother
    source: Luis_de_Borbon_y_Vargas
    target: Maria_Margarita_Vargas_Santaella
  AssignClass (b80dc396-7821-4ca1-bf17-07b7d4878525)
 Call ID: b80dc396-7821-4ca1-bf17-07b7d4878525
  Args:
    source: Alphonse_de_Borbon_y_Vargas
    type: :Man
  AssignClass (4c658d6f-ce99-42d1-8dc7-80b6d3d59d95)
 Call ID: 4c658d6f-ce99-42d1-8dc7-80b6d3d59d95
  Args:
    source: Alphonse_de_Borbon_y_Vargas
    type: :Person
  AddTriple (936c7ee3-6f5b-452f-ad1a-2b08979e8034)
 Call ID: 936c7ee3-6f5b-452f-ad1a-2b08979e8034
  Args:
    source: Alphonse_de_Borbon_y_Vargas
    target: Louis_Alphonse_de_Bourbon
    relation: :hasFather
  AddTriple (09c4d515-f19d-49e4-90d2-ada8a923cd2c)
 Call ID: 09c4d515-f19d-49e4-90d2-ada8a923cd2c
  Args:
    source: Alphonse_de_Borbon_y_Vargas
    target: Maria_Margarita_Vargas_Santaella
    relation: :hasMother
  AssignClass (40957c86-910e-4125-9916-79244a2b4791)
 Call ID: 40957c86-910e-4125-9916-79244a2b4791
  Args:
    type: :Man
    source: Henri_de_Borbon_y_Vargas
  AssignClass (d97bb98d-b681-4cdf-8ae3-9eefcf76ccfe)
 Call ID: d97bb98d-b681-4cdf-8ae3-9eefcf76ccfe
  Args:
    source: Henri_de_Borbon_y_Vargas
    type: :Person
  AddTriple (417561b1-da5b-48cc-8055-c1e48e84153e)
 Call ID: 417561b1-da5b-48cc-8055-c1e48e84153e
  Args:
    source: Henri_de_Borbon_y_Vargas
    target: Louis_Alphonse_de_Bourbon
    relation: :hasFather
  AddTriple (72ad80d6-fdb3-4e54-a2e1-448320434f86)
 Call ID: 72ad80d6-fdb3-4e54-a2e1-448320434f86
  Args:
    source: Henri_de_Borbon_y_Vargas
    target: Maria_Margarita_Vargas_Santaella
    relation: :hasMother
  AssignClass (b0090998-a3b9-4042-8cdf-34ec1d0181b1)
 Call ID: b0090998-a3b9-4042-8cdf-34ec1d0181b1
  Args:
    type: :Man
    source: Victor_Vargas
  AssignClass (b4a1e48f-2985-4d7f-9504-9a304939062e)
 Call ID: b4a1e48f-2985-4d7f-9504-9a304939062e
  Args:
    source: Victor_Vargas
    type: :Person
  AddTriple (8a17ee58-f266-45f1-8eae-9fdefd34d7e0)
 Call ID: 8a17ee58-f266-45f1-8eae-9fdefd34d7e0
  Args:
    source: Maria_Margarita_Vargas_Santaella
    target: Victor_Vargas
    relation: :hasFather
  Finish (8e57d040-597f-4d27-b6bd-efebb971567f)
 Call ID: 8e57d040-597f-4d27-b6bd-efebb971567f
  Args: