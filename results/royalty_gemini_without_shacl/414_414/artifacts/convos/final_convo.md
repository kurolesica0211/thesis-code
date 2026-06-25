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
Infante Alfonso of Spain (Don Alfonso Cristino Teresa Ángelo Francisco de Asís y Todos los Santos de Borbón y Borbón Dos-Sicilias; 3 October 1941 – 29 March 1956) was the younger brother of King Juan Carlos I of Spain.
He was also the youngest son of Infante Juan, Count of Barcelona and Princess María de las Mercedes of Bourbon-Two Sicilies, and the grandson of King Alfonso XIII.
He died young at 14 from a shot to the forehead by Juan Carlos' gun, but the circumstances of his death remain unclear to this day.
Early life

Alfonso was born at Hotel NH Firenze Anglo American in Rome, the youngest son of the Infante Juan of Spain, Count of Barcelona, and of his wife, Princess Maria Mercedes of Bourbon-Two Sicilies.
His godfather was the Infante Alfonso de Orleans y Borbón; his godmother was his father's sister Infanta Maria Cristina of Spain.
Within his own family, he was called Alfonsito to distinguish him from other family members with the name Alfonso.
When Alfonso was still just a baby, his family moved to Lausanne in Switzerland where they lived in the Villa Les Rocailles.
In 1947, Alfonso visited Spain for the first time at the invitation of caudillo Francisco Franco.
In 1950, he and his brother Juan Carlos were sent to study in Spain.
Later, Alfonso and Juan Carlos attended the military academy in Zaragoza.


Death and burial

On the evening of Maundy Thursday, 29 March 1956, Alfonso and Juan Carlos were at their parents' home Villa Giralda in Estoril, Portugal, for the Easter vacation, where Alfonso died in a gun accident.
The Spanish Embassy in Portugal issued an official communiqué:


Alfonso had won a local junior golf tournament earlier on the day, then went to evening Mass and rushed up to the room to see Juan Carlos who had come home for the Easter holidays from military school.
It is alleged that Juan Carlos began playing with a .22 caliber revolver that had apparently been given to Alfonso by General Francisco Franco.
Rumors appeared in newspapers that the .22 caliber revolver had actually been held by Juan Carlos at the moment the shot was fired.
As they were the only two in the room, it is unclear how Alfonso was shot but according to Josefina Carolo, dressmaker to Juan Carlos's mother, Juan Carlos pointed the pistol at Alfonso and pulled the trigger, unaware that the pistol was loaded.
Bernardo Arnoso, a Portuguese friend of Juan Carlos, also said that Juan Carlos fired the pistol not knowing that it was loaded, and adding that the bullet ricocheted off a wall hitting Alfonso in the face.
Helena Matheopoulos, a Greek author who spoke with Juan Carlos's sister Pilar, said that Alfonso had been out of the room and when he returned and pushed the door open, the door knocked Juan Carlos in the arm causing him to fire the pistol.
In his 2025 autobiography Juan Carlos I d’Espagne:
Réconciliation, Juan Carlos recounted how he and Alfonso had been playing with the gun, believing it to be safe as the magazine had been removed, without realising there was a bullet in the chamber, and that he had shot his brother into the forehead.
It is alleged that Infante Juan, Count of Barcelona, the children's father, threw the gun into the sea some time after Alfonso's death.
The funeral liturgy for Alfonso was held on Holy Saturday and was presided over by Monsignor Fernando Cento, Apostolic Nuncio to Portugal.



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
  AssignClass (b4f380c1-7222-4142-b9f6-db900676d77c)
 Call ID: b4f380c1-7222-4142-b9f6-db900676d77c
  Args:
    type: :Man
    source: :Alfonso_of_Spain
  AssignClass (969dc7b3-6993-4719-b38a-4acef505e7c2)
 Call ID: 969dc7b3-6993-4719-b38a-4acef505e7c2
  Args:
    source: :Alfonso_of_Spain
    type: :Person
  AddLiteral (c52b0421-cf39-492e-8fab-46053ff98786)
 Call ID: c52b0421-cf39-492e-8fab-46053ff98786
  Args:
    literal_value: 1941
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: :Alfonso_of_Spain
  AddLiteral (c0cb4250-29ad-4624-94e2-f99f6d755c98)
 Call ID: c0cb4250-29ad-4624-94e2-f99f6d755c98
  Args:
    source: :Alfonso_of_Spain
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1956
  AddLiteral (8688911e-c13c-43e1-b3e8-6ee7089f02ab)
 Call ID: 8688911e-c13c-43e1-b3e8-6ee7089f02ab
  Args:
    literal_type: xsd:string
    source: :Alfonso_of_Spain
    literal_value: Alfonsito
    relation: :alsoKnownAs
  AssignClass (46bebfb6-4451-4ec1-af5f-889ea5d40593)
 Call ID: 46bebfb6-4451-4ec1-af5f-889ea5d40593
  Args:
    type: :Man
    source: :Juan_Carlos_I
  AssignClass (aee8f786-1946-4dbc-a33d-4b500a484114)
 Call ID: aee8f786-1946-4dbc-a33d-4b500a484114
  Args:
    source: :Juan_Carlos_I
    type: :Person
  AddTriple (9a852f8f-1526-433a-a108-07f80744f225)
 Call ID: 9a852f8f-1526-433a-a108-07f80744f225
  Args:
    relation: :isBrotherOf
    target: :Juan_Carlos_I
    source: :Alfonso_of_Spain
  AssignClass (9d6a6ecb-eb4d-4040-809a-d73aa7c1385d)
 Call ID: 9d6a6ecb-eb4d-4040-809a-d73aa7c1385d
  Args:
    type: :Man
    source: :Juan_Count_of_Barcelona
  AssignClass (3db4ba3e-f41f-47f7-b5bc-4b120c0f21bb)
 Call ID: 3db4ba3e-f41f-47f7-b5bc-4b120c0f21bb
  Args:
    source: :Juan_Count_of_Barcelona
    type: :Person
  AssignClass (9d8e5500-44c1-49f7-846f-67d24ab2467b)
 Call ID: 9d8e5500-44c1-49f7-846f-67d24ab2467b
  Args:
    source: :Juan_Count_of_Barcelona
    type: :Ancestor
  AssignClass (92d92327-6d12-4eef-ab96-7b9539047e9d)
 Call ID: 92d92327-6d12-4eef-ab96-7b9539047e9d
  Args:
    source: :Maria_Mercedes_of_Bourbon-Two_Sicilies
    type: :Woman
  AssignClass (085c41f0-cef9-468c-89a6-8272b2cb7d71)
 Call ID: 085c41f0-cef9-468c-89a6-8272b2cb7d71
  Args:
    source: :Maria_Mercedes_of_Bourbon-Two_Sicilies
    type: :Person
  AssignClass (2de15cba-6e16-46f3-8d70-d630256fb64a)
 Call ID: 2de15cba-6e16-46f3-8d70-d630256fb64a
  Args:
    type: :Ancestor
    source: :Maria_Mercedes_of_Bourbon-Two_Sicilies
  AddTriple (05e46da0-fb5c-4f00-8249-5f1e887bdf2a)
 Call ID: 05e46da0-fb5c-4f00-8249-5f1e887bdf2a
  Args:
    target: :Juan_Count_of_Barcelona
    relation: :hasFather
    source: :Alfonso_of_Spain
  AddTriple (4e7785ef-cecb-4d5a-92ac-92db2456e301)
 Call ID: 4e7785ef-cecb-4d5a-92ac-92db2456e301
  Args:
    target: :Maria_Mercedes_of_Bourbon-Two_Sicilies
    relation: :hasMother
    source: :Alfonso_of_Spain
  AssignClass (316f6e11-93a8-4d5c-9355-54d6c4fcf059)
 Call ID: 316f6e11-93a8-4d5c-9355-54d6c4fcf059
  Args:
    source: :Alfonso_XIII
    type: :Man
  AssignClass (5c8c9c27-4351-4e07-88d4-ef355428be1c)
 Call ID: 5c8c9c27-4351-4e07-88d4-ef355428be1c
  Args:
    source: :Alfonso_XIII
    type: :Person
  AssignClass (59b6ca2e-962c-4230-a32a-d7abe2a505e6)
 Call ID: 59b6ca2e-962c-4230-a32a-d7abe2a505e6
  Args:
    source: :Alfonso_XIII
    type: :Ancestor
  AddTriple (f4dc5f4f-5d91-4445-8ba1-79491ca48bc0)
 Call ID: f4dc5f4f-5d91-4445-8ba1-79491ca48bc0
  Args:
    target: :Alfonso_XIII
    relation: :hasAncestor
    source: :Alfonso_of_Spain
  AssignClass (f39ae5a7-7d41-4474-a795-fc5ee5ac3da6)
 Call ID: f39ae5a7-7d41-4474-a795-fc5ee5ac3da6
  Args:
    source: :Alfonso_de_Orleans_y_Borbon
    type: :Man
  AssignClass (36d94a23-9b33-4d4e-8edd-b8254a1ddaef)
 Call ID: 36d94a23-9b33-4d4e-8edd-b8254a1ddaef
  Args:
    type: :Person
    source: :Alfonso_de_Orleans_y_Borbon
  AssignClass (5173f93e-a1a4-4967-a705-41a8df137bf1)
 Call ID: 5173f93e-a1a4-4967-a705-41a8df137bf1
  Args:
    source: :Maria_Cristina_of_Spain
    type: :Woman
  AssignClass (a523faaf-0523-4a1e-bcc5-3cee4575e6b3)
 Call ID: a523faaf-0523-4a1e-bcc5-3cee4575e6b3
  Args:
    type: :Person
    source: :Maria_Cristina_of_Spain
  AddTriple (90a3e184-e84c-4e25-b553-400f95777071)
 Call ID: 90a3e184-e84c-4e25-b553-400f95777071
  Args:
    target: :Juan_Count_of_Barcelona
    relation: :hasFather
    source: :Juan_Carlos_I
  AddTriple (b1b11b6d-c7e8-4e45-96eb-e39116b618a8)
 Call ID: b1b11b6d-c7e8-4e45-96eb-e39116b618a8
  Args:
    source: :Juan_Carlos_I
    target: :Maria_Mercedes_of_Bourbon-Two_Sicilies
    relation: :hasMother
  AssignClass (49d0bfbe-602e-48a3-b042-2df2ef9f092c)
 Call ID: 49d0bfbe-602e-48a3-b042-2df2ef9f092c
  Args:
    type: :Woman
    source: :Pilar
  AssignClass (dc883d7b-a271-4361-b9e6-058d67a98add)
 Call ID: dc883d7b-a271-4361-b9e6-058d67a98add
  Args:
    source: :Pilar
    type: :Person
  AddTriple (3be55bc3-57e2-49e3-80e1-800e64379508)
 Call ID: 3be55bc3-57e2-49e3-80e1-800e64379508
  Args:
    relation: :isSisterOf
    target: :Juan_Carlos_I
    source: :Pilar
  Finish (28f6bb42-ca8b-4547-8311-12f6c66eb537)
 Call ID: 28f6bb42-ca8b-4547-8311-12f6c66eb537
  Args: