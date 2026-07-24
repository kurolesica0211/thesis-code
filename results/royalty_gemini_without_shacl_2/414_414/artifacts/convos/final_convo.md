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
  AssignClass (3261997a-09d2-4ab5-b7ad-eace990d29d2)
 Call ID: 3261997a-09d2-4ab5-b7ad-eace990d29d2
  Args:
    type: :Man
    source: Infante_Alfonso_of_Spain
  AssignClass (8a549410-d1a2-4b9f-8114-f0f3a8d652f5)
 Call ID: 8a549410-d1a2-4b9f-8114-f0f3a8d652f5
  Args:
    source: Infante_Alfonso_of_Spain
    type: :Person
  AssignClass (2a7bbe84-dc8c-45a7-8579-bb765c6f8f0a)
 Call ID: 2a7bbe84-dc8c-45a7-8579-bb765c6f8f0a
  Args:
    source: King_Juan_Carlos_I_of_Spain
    type: :Man
  AssignClass (9b4f6cf5-10f9-4ae9-a52e-4c5175097a91)
 Call ID: 9b4f6cf5-10f9-4ae9-a52e-4c5175097a91
  Args:
    type: :Person
    source: King_Juan_Carlos_I_of_Spain
  AssignClass (95f1d080-4d69-4258-a50e-573c710fcb19)
 Call ID: 95f1d080-4d69-4258-a50e-573c710fcb19
  Args:
    source: Infante_Juan_Count_of_Barcelona
    type: :Man
  AssignClass (1444a20a-cd67-4d8d-b56b-02b486a19070)
 Call ID: 1444a20a-cd67-4d8d-b56b-02b486a19070
  Args:
    source: Infante_Juan_Count_of_Barcelona
    type: :Person
  AssignClass (ee0e39a9-edc3-4373-892c-8b206e6e0dbd)
 Call ID: ee0e39a9-edc3-4373-892c-8b206e6e0dbd
  Args:
    source: Princess_Maria_Mercedes_of_Bourbon_Two_Sicilies
    type: :Woman
  AssignClass (ef057f42-a09c-45bc-8327-24f0a308c9f6)
 Call ID: ef057f42-a09c-45bc-8327-24f0a308c9f6
  Args:
    type: :Person
    source: Princess_Maria_Mercedes_of_Bourbon_Two_Sicilies
  AssignClass (0a2d0010-4b12-4687-983c-2d03d4c57337)
 Call ID: 0a2d0010-4b12-4687-983c-2d03d4c57337
  Args:
    type: :Man
    source: King_Alfonso_XIII
  AssignClass (1a4c0766-2438-45c1-bb37-fc5eba91e815)
 Call ID: 1a4c0766-2438-45c1-bb37-fc5eba91e815
  Args:
    source: King_Alfonso_XIII
    type: :Person
  AssignClass (603de3a4-75ed-4215-997a-6106f5269321)
 Call ID: 603de3a4-75ed-4215-997a-6106f5269321
  Args:
    source: Infante_Alfonso_de_Orleans_y_Borbon
    type: :Man
  AssignClass (4b043dc3-bb53-4306-9de3-3d9be6567e18)
 Call ID: 4b043dc3-bb53-4306-9de3-3d9be6567e18
  Args:
    type: :Person
    source: Infante_Alfonso_de_Orleans_y_Borbon
  AssignClass (af58b930-80b0-4b62-a743-7bba59c80c8e)
 Call ID: af58b930-80b0-4b62-a743-7bba59c80c8e
  Args:
    type: :Woman
    source: Infanta_Maria_Cristina_of_Spain
  AssignClass (d3ff6424-9165-42c3-99a2-2b589307c6ec)
 Call ID: d3ff6424-9165-42c3-99a2-2b589307c6ec
  Args:
    source: Infanta_Maria_Cristina_of_Spain
    type: :Person
  AssignClass (d76d288f-22ca-4969-8f54-80e75141859a)
 Call ID: d76d288f-22ca-4969-8f54-80e75141859a
  Args:
    type: :Man
    source: Francisco_Franco
  AssignClass (cdde10df-68fd-4332-90a0-c3310fcd6f62)
 Call ID: cdde10df-68fd-4332-90a0-c3310fcd6f62
  Args:
    type: :Person
    source: Francisco_Franco
  AssignClass (e781ce32-2bf3-429f-b8ab-48970b310375)
 Call ID: e781ce32-2bf3-429f-b8ab-48970b310375
  Args:
    source: Pilar
    type: :Woman
  AssignClass (2fbf614a-a2fa-44b0-b32b-97f9e038c279)
 Call ID: 2fbf614a-a2fa-44b0-b32b-97f9e038c279
  Args:
    type: :Person
    source: Pilar
  AddLiteral (1df1f0b7-7920-4dc2-8ca8-c752677b1afb)
 Call ID: 1df1f0b7-7920-4dc2-8ca8-c752677b1afb
  Args:
    literal_type: xsd:string
    literal_value: Alfonso
    relation: :knownAs
    source: Infante_Alfonso_of_Spain
  AddLiteral (e4796d5d-68b5-406a-b542-a8c1405fdff3)
 Call ID: e4796d5d-68b5-406a-b542-a8c1405fdff3
  Args:
    source: Infante_Alfonso_of_Spain
    literal_type: xsd:string
    literal_value: Alfonsito
    relation: :alsoKnownAs
  AddLiteral (4ac1992e-cf8d-491e-a941-c03aa3183b26)
 Call ID: 4ac1992e-cf8d-491e-a941-c03aa3183b26
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1941
    source: Infante_Alfonso_of_Spain
  AddLiteral (f839a59e-a556-4ac5-9b1a-b548283f3674)
 Call ID: f839a59e-a556-4ac5-9b1a-b548283f3674
  Args:
    source: Infante_Alfonso_of_Spain
    literal_type: xsd:integer
    literal_value: 1956
    relation: :hasDeathYear
  AddTriple (1e8b3d67-1ddb-4d71-b64b-a8f673f49e41)
 Call ID: 1e8b3d67-1ddb-4d71-b64b-a8f673f49e41
  Args:
    relation: :isBrotherOf
    source: Infante_Alfonso_of_Spain
    target: King_Juan_Carlos_I_of_Spain
  AddTriple (73d54fe7-0050-44e0-b428-ceb164f27dd7)
 Call ID: 73d54fe7-0050-44e0-b428-ceb164f27dd7
  Args:
    relation: :hasFather
    source: Infante_Alfonso_of_Spain
    target: Infante_Juan_Count_of_Barcelona
  AddTriple (1738af2b-225d-4cc0-83f6-8eac10f782a0)
 Call ID: 1738af2b-225d-4cc0-83f6-8eac10f782a0
  Args:
    relation: :hasMother
    source: Infante_Alfonso_of_Spain
    target: Princess_Maria_Mercedes_of_Bourbon_Two_Sicilies
  AddTriple (5d88a861-b804-42e1-a511-a71d81c6ce6d)
 Call ID: 5d88a861-b804-42e1-a511-a71d81c6ce6d
  Args:
    relation: :hasFather
    source: King_Juan_Carlos_I_of_Spain
    target: Infante_Juan_Count_of_Barcelona
  AddTriple (3c52c3d5-23fb-449d-86a7-2312a4415775)
 Call ID: 3c52c3d5-23fb-449d-86a7-2312a4415775
  Args:
    source: King_Juan_Carlos_I_of_Spain
    target: Princess_Maria_Mercedes_of_Bourbon_Two_Sicilies
    relation: :hasMother
  AddTriple (cedfefd6-8bb5-4602-841d-7183f87ec721)
 Call ID: cedfefd6-8bb5-4602-841d-7183f87ec721
  Args:
    relation: :isFatherOf
    source: King_Alfonso_XIII
    target: Infante_Juan_Count_of_Barcelona
  AddTriple (b3c50832-6926-4656-8f61-6125ebd0e36f)
 Call ID: b3c50832-6926-4656-8f61-6125ebd0e36f
  Args:
    source: Infanta_Maria_Cristina_of_Spain
    target: Infante_Juan_Count_of_Barcelona
    relation: :isSisterOf
  AddTriple (7479079d-0e81-4dac-831c-cb8a84d5479e)
 Call ID: 7479079d-0e81-4dac-831c-cb8a84d5479e
  Args:
    relation: :isSisterOf
    source: Pilar
    target: King_Juan_Carlos_I_of_Spain
  Finish (6cd1481b-67b2-432c-859f-ca882717952a)
 Call ID: 6cd1481b-67b2-432c-859f-ca882717952a
  Args: