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
Prince Ferdinand Pius (Ferdinando Pio Maria), Duke of Calabria and Castro (25 July 1869, Rome – 7 January 1960, Lindau), was head of the House of Bourbon-Two Sicilies and pretender to the throne of the extinct Kingdom of the Two Sicilies from 1934 to 1960.
Family

Ferdinand was the eldest child of Prince Alfonso, Count of Caserta and his wife Princess Maria Antonietta of Bourbon-Two Sicilies.
He was a grandson of Ferdinand II of the Two Sicilies and an older brother of Prince Carlos of Bourbon-Two Sicilies, Maria Immaculata, Princess Johann Georg of Saxony, Maria Cristina, Archduchess Peter Ferdinand of Austria, Maria di Grazia, Princess Imperial of Brazil, Prince Ranieri, Duke of Castro, Prince Philip of Bourbon-Two Sicilies, and Prince Gabriel of Bourbon-Two Sicilies.
Marriage

Ferdinand married Princess Maria Ludwiga Theresia of Bavaria, daughter of King Ludwig III of Bavaria on 31 May 1897.
They had six children:


Ferdinand and Maria lived for many years at Villa Amsee, Lindau.
Disputed succession

Following Ferdinand's death, the headship of the House of Bourbon-Two Sicilies was claimed by both his nephew Infante Alfonso, Duke of Calabria, and his brother Prince Ranieri, Duke of Castro, and remains disputed between their descendants.
The basis of Alfonso’s claim was that his late father, Prince Carlos of Bourbon-Two Sicilies (1870–1949), had been Ferdinand's next oldest brother.
But Henri, Count of Paris, upheld the claim of Ferdinand's younger brother, Prince Ranieri, Duke of Castro (1883–1973), contending that Carlos had renounced his rights of succession for himself and his descendants in 1901 when he married the Spanish heiress presumptive María de las Mercedes, Princess of Asturias.
The Count of Paris was well aware that his own claim to the French throne depended on the validity of the renunciation in 1713 of Philip V of Spain, in favor of the junior House of Orléans.
In 1900, Prince Carlos had executed the Act of Cannes, in anticipation of his marriage to María de las Mercedes, and in 1901 he became a Spanish subject and accepted the title of Infante.
The position of Ranieri was that by so doing Carlos had renounced any claim to the throne of the Two Sicilies.
But Alfonso had a different interpretation, which was that the Act of Cannes would have taken effect only if Mercedes and Carlos had succeeded to the Spanish throne.
He also argued that the Act of Cannes was invalid under the succession rules of the house of Two Sicilies.
Military service

Ferdinand initially served in the Spanish Army, and after leaving service held the honorary rank of Comandante of the General Staff of the Spanish Army.
Feld-Artillerie-Regiment "Prinz Ferdinand von Bourbon, Herzog von Calabrien"), which was renamed in honor of him.



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
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

:hasDeathYear a owl:AnnotationProperty .

:hasMarriageYear a owl:AnnotationProperty .

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

:hasChild a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:inverseOf :isChildOf .

:isAncestorOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation .

:isSiblingOf a owl:ObjectProperty,
        owl:SymmetricProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isBloodrelationOf ;
    owl:propertyChainAxiom ( :hasParent :isParentOf ) .

:isSisterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf .

:hasParent a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Person ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:equivalentProperty :isChildOf ;
    owl:inverseOf :isParentOf .

:Sex a owl:Class ;
    rdfs:subClassOf :DomainEntity ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Female :Male ) ] .

:isChildOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:propertyDisjointWith :isSisterOf .

:Man a owl:Class ;
    owl:disjointWith :Sex,
        :Woman ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Male ] ) ] .

:Woman a owl:Class ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Female ] ) ] .

:isParentOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:propertyDisjointWith :isSisterOf .

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



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (b444fac3-1e7a-4a98-8de7-6c36733f55c2)
 Call ID: b444fac3-1e7a-4a98-8de7-6c36733f55c2
  Args:
    type: :Man
    source: Ferdinand_Pius
  AssignClass (11411c1b-2937-495f-bce7-b454666ad5f7)
 Call ID: 11411c1b-2937-495f-bce7-b454666ad5f7
  Args:
    type: :Man
    source: Alfonso_Count_of_Caserta
  AssignClass (18cf878c-7217-4325-bd8b-7be25048c608)
 Call ID: 18cf878c-7217-4325-bd8b-7be25048c608
  Args:
    type: :Woman
    source: Maria_Antonietta
  AssignClass (89204a6a-bc80-4311-a780-117a608cf16b)
 Call ID: 89204a6a-bc80-4311-a780-117a608cf16b
  Args:
    source: Ferdinand_II_of_the_Two_Sicilies
    type: :Man
  AssignClass (55b2f7c9-447e-485d-8474-bcdff6e8ccc4)
 Call ID: 55b2f7c9-447e-485d-8474-bcdff6e8ccc4
  Args:
    source: Carlos_of_Bourbon-Two_Sicilies
    type: :Man
  AssignClass (7962291b-6621-4b2d-bba9-86dd3aa0b4a2)
 Call ID: 7962291b-6621-4b2d-bba9-86dd3aa0b4a2
  Args:
    type: :Woman
    source: Maria_Immaculata
  AssignClass (655d15e3-8527-4b00-996e-df9c1c230969)
 Call ID: 655d15e3-8527-4b00-996e-df9c1c230969
  Args:
    source: Maria_Cristina
    type: :Woman
  AssignClass (69abfb09-3bf8-4d8e-b464-68c7333a212e)
 Call ID: 69abfb09-3bf8-4d8e-b464-68c7333a212e
  Args:
    source: Maria_di_Grazia
    type: :Woman
  AssignClass (aa8e6aa3-e0f2-4131-9353-374762fbec3f)
 Call ID: aa8e6aa3-e0f2-4131-9353-374762fbec3f
  Args:
    type: :Man
    source: Ranieri_Duke_of_Castro
  AssignClass (dfbd37a6-a47d-4f3e-b21b-be646042f9bc)
 Call ID: dfbd37a6-a47d-4f3e-b21b-be646042f9bc
  Args:
    type: :Man
    source: Philip_of_Bourbon-Two_Sicilies
  AssignClass (0feaeb18-e4a0-4c6b-9b34-02e5924a34e4)
 Call ID: 0feaeb18-e4a0-4c6b-9b34-02e5924a34e4
  Args:
    type: :Man
    source: Gabriel_of_Bourbon-Two_Sicilies
  AssignClass (cfa8d831-a0d8-4a6f-819f-d38990d58a5d)
 Call ID: cfa8d831-a0d8-4a6f-819f-d38990d58a5d
  Args:
    source: Maria_Ludwiga_Theresia_of_Bavaria
    type: :Woman
  AssignClass (db58f21e-3a20-482b-b58e-43fe3134a9fa)
 Call ID: db58f21e-3a20-482b-b58e-43fe3134a9fa
  Args:
    type: :Man
    source: Ludwig_III_of_Bavaria
  AddLiteral (a34ec53b-a9f1-4442-9a27-226069bc0880)
 Call ID: a34ec53b-a9f1-4442-9a27-226069bc0880
  Args:
    relation: :knownAs
    source: Ferdinand_Pius
    literal_value: Ferdinand Pius
    literal_type: xsd:string
  AddLiteral (c4697bf1-cf34-4d32-baed-7d0ead4e2dfa)
 Call ID: c4697bf1-cf34-4d32-baed-7d0ead4e2dfa
  Args:
    source: Ferdinand_Pius
    relation: :alsoKnownAs
    literal_type: xsd:string
    literal_value: Ferdinando Pio Maria
  AddLiteral (7208e6da-d51e-4c3c-bf10-f1d22ee9348e)
 Call ID: 7208e6da-d51e-4c3c-bf10-f1d22ee9348e
  Args:
    source: Ferdinand_Pius
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1869
  AddLiteral (9b4ade2d-2880-4f8e-8540-b0c9c8eb53db)
 Call ID: 9b4ade2d-2880-4f8e-8540-b0c9c8eb53db
  Args:
    relation: :hasDeathYear
    source: Ferdinand_Pius
    literal_value: 1960
    literal_type: xsd:integer
  AddTriple (2d103519-c7ff-4c7b-98b4-24f23af25c12)
 Call ID: 2d103519-c7ff-4c7b-98b4-24f23af25c12
  Args:
    target: Alfonso_Count_of_Caserta
    source: Ferdinand_Pius
    relation: :hasFather
  AddTriple (6a43baee-9cb3-461a-917f-a3f8aa84fb9a)
 Call ID: 6a43baee-9cb3-461a-917f-a3f8aa84fb9a
  Args:
    target: Maria_Antonietta
    relation: :hasMother
    source: Ferdinand_Pius
  AddTriple (4d02c310-2384-40f8-8f52-b3fe768603d0)
 Call ID: 4d02c310-2384-40f8-8f52-b3fe768603d0
  Args:
    target: Ferdinand_II_of_the_Two_Sicilies
    source: Alfonso_Count_of_Caserta
    relation: :hasFather
  AddTriple (0e284936-3424-462e-a628-511cdcd9ecdb)
 Call ID: 0e284936-3424-462e-a628-511cdcd9ecdb
  Args:
    source: Ferdinand_Pius
    relation: :hasBrother
    target: Carlos_of_Bourbon-Two_Sicilies
  AddTriple (af861a7f-7e07-4ff1-ada4-bedd103c7472)
 Call ID: af861a7f-7e07-4ff1-ada4-bedd103c7472
  Args:
    target: Maria_Immaculata
    relation: :hasSister
    source: Ferdinand_Pius
  AddTriple (fda3b874-9c8b-4b25-bc18-05109c84f605)
 Call ID: fda3b874-9c8b-4b25-bc18-05109c84f605
  Args:
    target: Maria_Cristina
    source: Ferdinand_Pius
    relation: :hasSister
  AddTriple (5b09e9d5-dc8e-4b15-a810-f71d1e9cc273)
 Call ID: 5b09e9d5-dc8e-4b15-a810-f71d1e9cc273
  Args:
    source: Ferdinand_Pius
    relation: :hasSister
    target: Maria_di_Grazia
  AddTriple (ee9430a2-7038-49dc-95c2-815eca8eb4f2)
 Call ID: ee9430a2-7038-49dc-95c2-815eca8eb4f2
  Args:
    source: Ferdinand_Pius
    relation: :hasBrother
    target: Ranieri_Duke_of_Castro
  AddTriple (4e8477ce-eaea-4d17-bdd0-9eb5b7469108)
 Call ID: 4e8477ce-eaea-4d17-bdd0-9eb5b7469108
  Args:
    target: Philip_of_Bourbon-Two_Sicilies
    source: Ferdinand_Pius
    relation: :hasBrother
  AddTriple (e1f5825f-4c7a-4bac-a44b-e12c8cc7ce92)
 Call ID: e1f5825f-4c7a-4bac-a44b-e12c8cc7ce92
  Args:
    relation: :hasBrother
    source: Ferdinand_Pius
    target: Gabriel_of_Bourbon-Two_Sicilies
  AddTriple (02190ff5-4dc6-4786-92dd-e736adb604a1)
 Call ID: 02190ff5-4dc6-4786-92dd-e736adb604a1
  Args:
    target: Ludwig_III_of_Bavaria
    relation: :hasFather
    source: Maria_Ludwiga_Theresia_of_Bavaria
  AddLiteral (c21b6320-3f6a-41dc-866d-db97e4b8d1ce)
 Call ID: c21b6320-3f6a-41dc-866d-db97e4b8d1ce
  Args:
    relation: :hasMarriageYear
    source: Ferdinand_Pius
    literal_value: 1897
    literal_type: xsd:integer
  Finish (382253c3-3364-4db4-91af-dd676d741020)
 Call ID: 382253c3-3364-4db4-91af-dd676d741020
  Args: