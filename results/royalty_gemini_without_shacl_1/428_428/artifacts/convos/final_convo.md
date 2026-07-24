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
Prince Michael of Greece and Denmark (Greek: Μισέλ ντε Γκρες, romanized: Michel de Grèce; 7 January 1939 – 28 July 2024) was a Greek historian, author, and member of the Greek royal family.
He was a first cousin, among others, of Kings George II of Greece, Paul of Greece, their sister,  Queen Helen, Queen Mother of Romania, in addition to Prince Philip, Duke of Edinburgh and also of Prince Henri d'Orléans.


Birth and family

Michael was born in Rome to Prince Christopher of Greece and Denmark (youngest son of King George I of Greece) and his second wife, Princess Françoise d'Orléans (daughter of the Orleanist claimant to the defunct French throne, Jean d'Orléans, Duke of Guise).
His godparents were his two first cousins Queen Helen, Queen Mother of Romania and King George II of Greece (eldest children of his paternal uncle King Constantine I).
His father died in 1940, when Michael was a year old.
His mother died in 1953, when Michael was 14, leaving him an orphan.
Although a Greek prince, like many members of his dynasty he grew up largely abroad, sometimes in exile.
As Europe marched into World War II, the infant Michael's family scattered: his mother's father, the Duke of Guise, left his residence of exile in Brussels, the Manoir d'Anjou, for their property at Larache, Morocco, in March 1939 where he died on 24 August, the Manoir having become the Belgian headquarters for Germany's invading Wehrmacht.
About eight months before her father's death, Françoise was widowed by the death of Prince Christopher, following an abscess of the lung, in Athens in January.
She took Michael to join her mother's household in Larache where her elder sister, Princess Isabelle Murat and her family, had also taken refuge from Europe.
Their brother, Henri, Count of Paris, who succeeded his own father as head of the Orleanist monarchist movement, sent for his wife and children to come from their relatives in Brazil, and by the spring of 1941 they too were settled in Spanish Morocco (still being banned from the French sector), near Casablanca, in a small house without electricity that was named Oued Akreech in the town of Rabat.
Michael lived his early childhood years on the African continent in the midst of his mother's family.
By the time Michael's mother died in Paris in early 1953, France had repealed the law of banishment against its former ruling families (24 June 1950) and the Comte de Paris had taken up residence in the capital.
When, in August 1953, Monseigneur moved the Comtesse and their children to a new estate, the Manoir du Cœur Volant in Louveciennes, Michael joined the couple and their four eldest children in the main building, while the seven younger children and their governesses occupied an annex given the name la maison de Blanche Neige ("Snow White's cottage").
Henceforth, Michael was given into the care of his uncle and raised with his Orléans cousins.
Michael later acknowledged that his uncle had been a poor manager of his ward's assets, but maintained that there was no malfeasance or attempt to conceal losses.
Following the death of his second cousin, Christian Ludwig Gustav Fritz Castenskiold (1926–2024), on 16 July 2024, he became the last surviving great-grandchild of King Christian IX of Denmark.
Activities

Michael studied political science in Paris.
He then re-patriated to Greece for military duty, serving for four years in the Cavalry-Tank Corps, in Athens and Thessaloniki.
He inherited from his mother a half-interest in the domain of the Nouvion-en-Thiérache, once the seat of the Dukes of Guise, from whom the Bourbon-Orléans inherited the vast property, which included a grand château and a petit château, in Aisne.
He and Michael sold the grand château in 1980 to the city of Roubaix, which subsequently became a conference center for environmental studies, while the petit château was sold in 1986 to the local government of Nouvion.
List of works

Having watched his mother observe a family tradition by igniting what he called a kind of auto-da-fé in which she burned his late father's papers and memorabilia following the sale of his villa in Rome after the war, Prince Michael grew up to become a biographer and historian.
Marriage and issue

Michael married Marina Karella (born 17 July 1940) on 7 February 1965 in Athens, daughter of Theódoros Karellas and Elli Chalikiopoulos.
Marina is a Greek artist and sculptor of international reputation whose work has often been exhibited in Athens, Paris and New York.
This was a non-dynastic marriage, which obtained the legally required authorisation of King Constantine II only after Michael renounced all rights of succession to the Greek throne for himself and his descendants.
The couple have two daughters:


Death

Prince Michael died at a hospital in Athens, on 28 July 2024, at the age of 85.
He was the last surviving grandchild of George I of Greece.
He has lineage to the House of Bourbon through his mother's side of the family and the last surviving great-grandchild of Christian IX of Denmark.
His immediate family – Marina Karella, Princess Alexandra of Greece, Nicolas Mirzayantz, Princess Olga, Duchess of Aosta, Prince Aimone, Duke of Aosta, and his grandchildren – attended the funeral.
Other dignitaries included Queen Anne-Marie of Greece, Pavlos, Crown Prince of Greece, Marie-Chantal, Crown Princess of Greece, Princess Alexia of Greece and Denmark, Prince Nikolaos of Greece and Denmark, Princess Theodora of Greece and Denmark, Prince Philippos of Greece and Denmark, Queen Sofía of Spain, Princess Irene of Greece and Denmark, Princess Anne, Duchess of Calabria, Princess Mafalda of Savoy-Aosta, Princess Bianca of Savoy-Aosta and Mareva Grabowski, the wife of the Prime Minister of Greece, Kyriakos Mitsotakis.



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
  AssignClass (b26413d2-d554-4e56-8b28-a52aa6df52c4)
 Call ID: b26413d2-d554-4e56-8b28-a52aa6df52c4
  Args:
    source: Prince_Michael_of_Greece_and_Denmark
    type: :Man
  AssignClass (b21091d4-162f-44ef-8a9b-adc958e5b8c5)
 Call ID: b21091d4-162f-44ef-8a9b-adc958e5b8c5
  Args:
    source: Prince_Christopher_of_Greece_and_Denmark
    type: :Man
  AssignClass (213bec6d-e75e-498b-b26f-98cf189b47bc)
 Call ID: 213bec6d-e75e-498b-b26f-98cf189b47bc
  Args:
    type: :Woman
    source: Princess_Francoise_dOrleans
  AssignClass (e7cccc6e-7723-40d0-a9a7-7deca826288f)
 Call ID: e7cccc6e-7723-40d0-a9a7-7deca826288f
  Args:
    type: :Man
    source: King_George_I_of_Greece
  AssignClass (392e4823-361c-49a5-9a17-e0b56d34151a)
 Call ID: 392e4823-361c-49a5-9a17-e0b56d34151a
  Args:
    type: :Man
    source: Jean_dOrleans_Duke_of_Guise
  AssignClass (4a93d946-a7ea-4eb7-91e3-2a16903f3c53)
 Call ID: 4a93d946-a7ea-4eb7-91e3-2a16903f3c53
  Args:
    type: :Woman
    source: Marina_Karella
  AssignClass (582f56b1-7bbd-4e61-a7e9-9dae4f6a0fb6)
 Call ID: 582f56b1-7bbd-4e61-a7e9-9dae4f6a0fb6
  Args:
    source: Theodoros_Karellas
    type: :Man
  AssignClass (6027119e-19af-4930-90a9-dbab7531e0c8)
 Call ID: 6027119e-19af-4930-90a9-dbab7531e0c8
  Args:
    source: Elli_Chalikiopoulos
    type: :Woman
  AddLiteral (a58e736d-ad8b-4868-9aac-7bb8c47e3581)
 Call ID: a58e736d-ad8b-4868-9aac-7bb8c47e3581
  Args:
    literal_value: 1939
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Prince_Michael_of_Greece_and_Denmark
  AddLiteral (306f0f78-1c41-4fbe-a842-dc6087e83ee4)
 Call ID: 306f0f78-1c41-4fbe-a842-dc6087e83ee4
  Args:
    relation: :hasDeathYear
    source: Prince_Michael_of_Greece_and_Denmark
    literal_type: xsd:integer
    literal_value: 2024
  AddLiteral (eb483760-51e7-4e74-8bc6-903ebcdf251a)
 Call ID: eb483760-51e7-4e74-8bc6-903ebcdf251a
  Args:
    literal_value: 1940
    literal_type: xsd:integer
    source: Prince_Christopher_of_Greece_and_Denmark
    relation: :hasDeathYear
  AddLiteral (29f9b303-f8bf-443e-8da0-b85574a7c1e4)
 Call ID: 29f9b303-f8bf-443e-8da0-b85574a7c1e4
  Args:
    literal_type: xsd:integer
    source: Princess_Francoise_dOrleans
    relation: :hasDeathYear
    literal_value: 1953
  AddLiteral (3a18b9d2-3686-4f6c-b677-ce601b7562fa)
 Call ID: 3a18b9d2-3686-4f6c-b677-ce601b7562fa
  Args:
    literal_value: 1940
    literal_type: xsd:integer
    source: Marina_Karella
    relation: :hasBirthYear
  AddLiteral (6befc854-badb-448b-af8c-e3ba2165773b)
 Call ID: 6befc854-badb-448b-af8c-e3ba2165773b
  Args:
    literal_value: 1965
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: Prince_Michael_of_Greece_and_Denmark
  AddTriple (894e9f76-ef4d-4c27-90de-4a0b65def9bf)
 Call ID: 894e9f76-ef4d-4c27-90de-4a0b65def9bf
  Args:
    source: Prince_Michael_of_Greece_and_Denmark
    relation: :hasFather
    target: Prince_Christopher_of_Greece_and_Denmark
  AddTriple (b38b7f5a-aa7f-473b-b9fd-8835b999c5a3)
 Call ID: b38b7f5a-aa7f-473b-b9fd-8835b999c5a3
  Args:
    relation: :hasMother
    source: Prince_Michael_of_Greece_and_Denmark
    target: Princess_Francoise_dOrleans
  AddTriple (2bb86585-41b8-4de0-a314-81e90063d3f4)
 Call ID: 2bb86585-41b8-4de0-a314-81e90063d3f4
  Args:
    source: Prince_Christopher_of_Greece_and_Denmark
    relation: :hasFather
    target: King_George_I_of_Greece
  AddTriple (803eb8dd-27e7-4d71-9a82-1a14edbe2cec)
 Call ID: 803eb8dd-27e7-4d71-9a82-1a14edbe2cec
  Args:
    target: Jean_dOrleans_Duke_of_Guise
    relation: :hasFather
    source: Princess_Francoise_dOrleans
  AddTriple (a57d9de9-512f-45e7-92ab-55114e63b203)
 Call ID: a57d9de9-512f-45e7-92ab-55114e63b203
  Args:
    source: Prince_Michael_of_Greece_and_Denmark
    relation: :hasRelation
    target: Marina_Karella
  AddTriple (d3d2b13c-d6a7-400a-ae69-8c1e91840611)
 Call ID: d3d2b13c-d6a7-400a-ae69-8c1e91840611
  Args:
    target: Theodoros_Karellas
    relation: :hasFather
    source: Marina_Karella
  AddTriple (2e61343a-b178-4405-a3ea-8a73d504d5c5)
 Call ID: 2e61343a-b178-4405-a3ea-8a73d504d5c5
  Args:
    target: Elli_Chalikiopoulos
    source: Marina_Karella
    relation: :hasMother
  Finish (75f3f061-f59d-4754-a7fb-59ac5bf75a0b)
 Call ID: 75f3f061-f59d-4754-a7fb-59ac5bf75a0b
  Args: