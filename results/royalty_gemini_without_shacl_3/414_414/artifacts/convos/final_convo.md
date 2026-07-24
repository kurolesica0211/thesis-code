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
  AssignClass (17069a3b-e1c0-4412-8a93-da242ae078a7)
 Call ID: 17069a3b-e1c0-4412-8a93-da242ae078a7
  Args:
    type: :Man
    source: :Alfonso_of_Spain
  AssignClass (abf52a39-ca55-4844-a51e-04447807bb81)
 Call ID: abf52a39-ca55-4844-a51e-04447807bb81
  Args:
    type: :Person
    source: :Alfonso_of_Spain
  AddLiteral (0d6fddc0-53fc-47b0-8686-b3e2866a2ac6)
 Call ID: 0d6fddc0-53fc-47b0-8686-b3e2866a2ac6
  Args:
    source: :Alfonso_of_Spain
    literal_value: 1941
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (5922cd51-dd1b-4175-9b1d-a9e52ec2102a)
 Call ID: 5922cd51-dd1b-4175-9b1d-a9e52ec2102a
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: :Alfonso_of_Spain
    literal_value: 1956
  AddLiteral (01eaa17f-8bff-4800-a868-ec4316e19aa4)
 Call ID: 01eaa17f-8bff-4800-a868-ec4316e19aa4
  Args:
    source: :Alfonso_of_Spain
    literal_value: Alfonsito
    relation: :alsoKnownAs
    literal_type: xsd:string
  AssignClass (d70c76a9-c89d-4d06-8e3e-3e7c27f96189)
 Call ID: d70c76a9-c89d-4d06-8e3e-3e7c27f96189
  Args:
    type: :Man
    source: :Juan_Carlos_I_of_Spain
  AssignClass (62d5dfc8-dbf5-44f2-a4ec-b2f64850e9eb)
 Call ID: 62d5dfc8-dbf5-44f2-a4ec-b2f64850e9eb
  Args:
    type: :Person
    source: :Juan_Carlos_I_of_Spain
  AddTriple (5587e4eb-049a-4afc-8cb6-ebccbd03f9b4)
 Call ID: 5587e4eb-049a-4afc-8cb6-ebccbd03f9b4
  Args:
    relation: :isBrotherOf
    source: :Alfonso_of_Spain
    target: :Juan_Carlos_I_of_Spain
  AssignClass (f2588a49-4fa9-457a-8e53-34d028e071a7)
 Call ID: f2588a49-4fa9-457a-8e53-34d028e071a7
  Args:
    type: :Man
    source: :Juan_Count_of_Barcelona
  AssignClass (8d7eb8a0-86fe-47ea-8d7a-406a98848a5d)
 Call ID: 8d7eb8a0-86fe-47ea-8d7a-406a98848a5d
  Args:
    type: :Person
    source: :Juan_Count_of_Barcelona
  AssignClass (1b0d652c-d618-4d8b-8a00-d27bc95660bb)
 Call ID: 1b0d652c-d618-4d8b-8a00-d27bc95660bb
  Args:
    type: :Woman
    source: :Maria_Mercedes_of_Bourbon_Two_Sicilies
  AssignClass (2f5ab4f3-5a0e-4010-8f55-2b0d742e6a02)
 Call ID: 2f5ab4f3-5a0e-4010-8f55-2b0d742e6a02
  Args:
    type: :Person
    source: :Maria_Mercedes_of_Bourbon_Two_Sicilies
  AddTriple (e0085e55-8340-47b4-b4c9-48b3c37d02ee)
 Call ID: e0085e55-8340-47b4-b4c9-48b3c37d02ee
  Args:
    relation: :hasFather
    target: :Juan_Count_of_Barcelona
    source: :Alfonso_of_Spain
  AddTriple (5cbe08b2-a1cf-4735-bdf1-ab00e52c5ad1)
 Call ID: 5cbe08b2-a1cf-4735-bdf1-ab00e52c5ad1
  Args:
    relation: :hasMother
    source: :Alfonso_of_Spain
    target: :Maria_Mercedes_of_Bourbon_Two_Sicilies
  AssignClass (1f19e35f-4b2a-4564-9a85-f7f65e5525ec)
 Call ID: 1f19e35f-4b2a-4564-9a85-f7f65e5525ec
  Args:
    type: :Man
    source: :Alfonso_XIII
  AssignClass (31c104a0-1826-4a71-9c71-8570e86e5b97)
 Call ID: 31c104a0-1826-4a71-9c71-8570e86e5b97
  Args:
    type: :Person
    source: :Alfonso_XIII
  AddTriple (39311d34-3901-4231-a31e-f491d916d4d9)
 Call ID: 39311d34-3901-4231-a31e-f491d916d4d9
  Args:
    relation: :hasAncestor
    target: :Alfonso_XIII
    source: :Alfonso_of_Spain
  AssignClass (e0f7dce8-1ddb-4395-bc5b-1dba64cb92dc)
 Call ID: e0f7dce8-1ddb-4395-bc5b-1dba64cb92dc
  Args:
    type: :Man
    source: :Alfonso_de_Orleans_y_Borbon
  AssignClass (cd34c921-7dae-410c-859d-128dd431777d)
 Call ID: cd34c921-7dae-410c-859d-128dd431777d
  Args:
    type: :Person
    source: :Alfonso_de_Orleans_y_Borbon
  AssignClass (c7410ba9-0edb-4286-9d1c-44f7db2f7fb7)
 Call ID: c7410ba9-0edb-4286-9d1c-44f7db2f7fb7
  Args:
    type: :Woman
    source: :Maria_Cristina_of_Spain
  AssignClass (a85cc23b-ebfe-4ab3-8523-26cbba82e1ba)
 Call ID: a85cc23b-ebfe-4ab3-8523-26cbba82e1ba
  Args:
    type: :Person
    source: :Maria_Cristina_of_Spain
  AddTriple (ca44c45a-865a-46cc-a969-51f43f3ad9c2)
 Call ID: ca44c45a-865a-46cc-a969-51f43f3ad9c2
  Args:
    target: :Juan_Count_of_Barcelona
    source: :Maria_Cristina_of_Spain
    relation: :isSisterOf
  AssignClass (a002a30b-c59f-42b9-a71b-92f6dd79221b)
 Call ID: a002a30b-c59f-42b9-a71b-92f6dd79221b
  Args:
    type: :Man
    source: :Francisco_Franco
  AssignClass (3758873e-449e-4170-af4b-303afaf2166e)
 Call ID: 3758873e-449e-4170-af4b-303afaf2166e
  Args:
    type: :Person
    source: :Francisco_Franco
  AssignClass (c827cd92-cca9-4cd8-afec-7f6f56591391)
 Call ID: c827cd92-cca9-4cd8-afec-7f6f56591391
  Args:
    type: :Woman
    source: :Pilar
  AssignClass (65bcbf4f-c557-4df8-935b-a87b0e55b9af)
 Call ID: 65bcbf4f-c557-4df8-935b-a87b0e55b9af
  Args:
    type: :Person
    source: :Pilar
  AddTriple (12da559f-2f18-4eb2-b2b5-a9ff2bec5cf3)
 Call ID: 12da559f-2f18-4eb2-b2b5-a9ff2bec5cf3
  Args:
    source: :Pilar
    target: :Juan_Carlos_I_of_Spain
    relation: :isSisterOf
  AssignClass (20ed25e2-10f4-4a4b-94f3-82c15b99a7bc)
 Call ID: 20ed25e2-10f4-4a4b-94f3-82c15b99a7bc
  Args:
    type: :Man
    source: :Fernando_Cento
  AssignClass (6737c07e-27a0-4b57-82fe-7392b68a83e4)
 Call ID: 6737c07e-27a0-4b57-82fe-7392b68a83e4
  Args:
    type: :Person
    source: :Fernando_Cento
  Finish (e46147a2-3b24-46ad-80b0-cc242d66ddf5)
 Call ID: e46147a2-3b24-46ad-80b0-cc242d66ddf5
  Args: