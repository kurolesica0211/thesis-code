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
Baroness Gösta von dem Bussche-Haddenhausen (German: Freiin Gösta Julie Adelheid Marion Marie von dem Bussche-Haddenhausen; 26 January 1902 – 13 June 1996) was a German noblewoman and the mother of Prince Claus of the Netherlands.
Life in Germany

Gösta was born at Döbeln, Kingdom of Saxony, German Empire (now Saxony, Germany), the second child and daughter of Baron George von dem Bussche-Haddenhausen (1869–1923), and his wife, Baroness Gabriele von dem Bussche-Ippenburg (1877–1973).
Her father belonged to the Bussche-Haddenhausen branch of the Bussche family, and her mother belonged to the Bussche-Ippenburg branch.
Both of Gösta's parents were descended from Clamor von dem Bussche (1532–1573).
Gösta's mother was the heir of Dötzingen Estate near Hitzacker, which her maternal grandfather had inherited from the Counts von Oeynhausen after 1918.
Gösta's father was an officer in the Royal Saxon Army.
Dötzingen Estate later passed on to Gösta's brother Baron Julius von dem Bussche-Haddenhausen (1906–1977).
After Gösta's return from Africa and her husband's death in 1963, she spent the rest of her life in Dötzingen.
Gösta died at the age of 94 in Hitzacker, Germany.
Marriage

Gösta married Claus Felix von Amsberg (1890–1953), son of Wilhelm von Amsberg and Elise von Vieregge, on 4 September 1924 at Hitzacker.
Together, Gösta and Claus Felix had six daughters and one son:


Life in Africa

Gösta's husband Claus Felix had returned from the Tanganyika Territory (now Tanzania), a German colony, during World War I to become the manager of Dötzingen Estate in 1917.
Shortly after, the estate passed on to the Bussche family.
In 1924, Gösta and Claus Felix married, and in 1926, their son Claus was born at Dötzingen.
Claus Felix was the manager of a German-British tea and sisal plantation.
Claus was sent back to a German boarding school in 1933, but he returned to Africa in 1936.
In 1938, Gösta returned to Germany, and Claus was sent to a boarding school in Misdroy before being drafted by the army.
Gösta's husband returned to Germany in 1947.
Family relations

Gösta was a second cousin of Dorothea von Salviati (wife of Wilhelm, German Crown Prince's eldest son Prince Wilhelm of Prussia), both being great-granddaughters of Heinrich von Salviati and Caroline Rahlenbeck.
Gösta's younger and only brother Julius (1906–1977) was married to Anna-Elisabeth von Pfuel (1909–2005).
Gösta's family's home, Dötzingen Castle in Lower Saxony, had passed to her maternal grandfather, Eberhard Friedrich Gustav von dem Bussche-Ippenburg, from the Counts von Oeynhausen.
At a dinner party hosted by a distant cousin, the Count von Oeynhausen-Sierstorpff in Bad Driburg, on New Year's Eve 1962, Gösta's son Claus met then-Princess Beatrix of the Netherlands for the first time.
Beatrix, like Gösta and Claus, was a cousin of the Counts von Oeynhausen: Beatrix's paternal grandmother Armgard von Cramm was a daughter of Baron Aschwin of Sierstorpff-Cramm (1846–1909) and his wife, Baroness Hedwig von Sierstorpff-Driburg (1848–1900).
Additionally, Armgard's elder sister Baroness Hedwig von Sierstorpff-Cramm (1874–1907) was the heir to her mother's family's Driburg Estate.



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
  AssignClass (0d8e61db-27c3-4fd4-a0a2-c8548b9cfaa6)
 Call ID: 0d8e61db-27c3-4fd4-a0a2-c8548b9cfaa6
  Args:
    type: :Woman
    source: Gösta_von_dem_Bussche-Haddenhausen
  AssignClass (5f0a8449-54de-443c-9e77-acdace1991fe)
 Call ID: 5f0a8449-54de-443c-9e77-acdace1991fe
  Args:
    type: :Person
    source: Gösta_von_dem_Bussche-Haddenhausen
  AddLiteral (3346ead9-8e30-4d12-8ab6-a27f6a63a7e1)
 Call ID: 3346ead9-8e30-4d12-8ab6-a27f6a63a7e1
  Args:
    source: Gösta_von_dem_Bussche-Haddenhausen
    literal_value: 1902
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (d291db53-0893-47d3-9969-898edb0bf6d4)
 Call ID: d291db53-0893-47d3-9969-898edb0bf6d4
  Args:
    source: Gösta_von_dem_Bussche-Haddenhausen
    literal_value: 1996
    relation: :hasDeathYear
    literal_type: xsd:integer
  AssignClass (0b8eb163-465f-4426-ad3e-2b94594548f1)
 Call ID: 0b8eb163-465f-4426-ad3e-2b94594548f1
  Args:
    type: :Man
    source: George_von_dem_Bussche-Haddenhausen
  AssignClass (6ca1056c-7ed0-4830-9477-47d5afa0cffe)
 Call ID: 6ca1056c-7ed0-4830-9477-47d5afa0cffe
  Args:
    type: :Person
    source: George_von_dem_Bussche-Haddenhausen
  AddLiteral (94d973c4-1679-4ad8-ab0a-739d73f40697)
 Call ID: 94d973c4-1679-4ad8-ab0a-739d73f40697
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1869
    source: George_von_dem_Bussche-Haddenhausen
  AddLiteral (b45b5800-aca0-4eeb-8629-ef8dc9928e94)
 Call ID: b45b5800-aca0-4eeb-8629-ef8dc9928e94
  Args:
    literal_value: 1923
    source: George_von_dem_Bussche-Haddenhausen
    relation: :hasDeathYear
    literal_type: xsd:integer
  AssignClass (e112f2f5-94fe-41a5-96ff-a3abae16f4c5)
 Call ID: e112f2f5-94fe-41a5-96ff-a3abae16f4c5
  Args:
    type: :Woman
    source: Gabriele_von_dem_Bussche-Ippenburg
  AssignClass (d688ff4f-346a-458c-a5ab-a15dec48f631)
 Call ID: d688ff4f-346a-458c-a5ab-a15dec48f631
  Args:
    type: :Person
    source: Gabriele_von_dem_Bussche-Ippenburg
  AddLiteral (9266da16-6efe-4cef-afa0-2ac88e1dcf79)
 Call ID: 9266da16-6efe-4cef-afa0-2ac88e1dcf79
  Args:
    source: Gabriele_von_dem_Bussche-Ippenburg
    literal_value: 1877
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (0aba1df1-3f26-4587-97a8-852426325ae6)
 Call ID: 0aba1df1-3f26-4587-97a8-852426325ae6
  Args:
    source: Gabriele_von_dem_Bussche-Ippenburg
    literal_value: 1973
    relation: :hasDeathYear
    literal_type: xsd:integer
  AddTriple (4df99979-4cc8-46f9-961e-4d74e18a9c10)
 Call ID: 4df99979-4cc8-46f9-961e-4d74e18a9c10
  Args:
    target: George_von_dem_Bussche-Haddenhausen
    relation: :hasFather
    source: Gösta_von_dem_Bussche-Haddenhausen
  AddTriple (3c8e5abf-081f-4592-9711-44be4cc8bdf6)
 Call ID: 3c8e5abf-081f-4592-9711-44be4cc8bdf6
  Args:
    relation: :hasMother
    source: Gösta_von_dem_Bussche-Haddenhausen
    target: Gabriele_von_dem_Bussche-Ippenburg
  AssignClass (612be9b4-16e3-42d7-8cf6-99171cb51e58)
 Call ID: 612be9b4-16e3-42d7-8cf6-99171cb51e58
  Args:
    type: :Man
    source: Clamor_von_dem_Bussche
  AssignClass (d48b8b47-9ac9-4432-8918-1a1377beb59c)
 Call ID: d48b8b47-9ac9-4432-8918-1a1377beb59c
  Args:
    type: :Person
    source: Clamor_von_dem_Bussche
  AddTriple (4ee15895-9854-483a-93cd-a1401b5d6888)
 Call ID: 4ee15895-9854-483a-93cd-a1401b5d6888
  Args:
    target: Clamor_von_dem_Bussche
    relation: :hasAncestor
    source: George_von_dem_Bussche-Haddenhausen
  AddTriple (72a9477d-3dc4-4778-9bf0-c5c665f0ba7a)
 Call ID: 72a9477d-3dc4-4778-9bf0-c5c665f0ba7a
  Args:
    source: Gabriele_von_dem_Bussche-Ippenburg
    relation: :hasAncestor
    target: Clamor_von_dem_Bussche
  AssignClass (8616a840-c9e1-4bea-9541-102846a09d6b)
 Call ID: 8616a840-c9e1-4bea-9541-102846a09d6b
  Args:
    type: :Man
    source: Julius_von_dem_Bussche-Haddenhausen
  AssignClass (bcc0b700-1630-4e29-95d1-9be0392180e3)
 Call ID: bcc0b700-1630-4e29-95d1-9be0392180e3
  Args:
    type: :Person
    source: Julius_von_dem_Bussche-Haddenhausen
  AddLiteral (2710717e-8717-4482-a597-bc8a1d513f3e)
 Call ID: 2710717e-8717-4482-a597-bc8a1d513f3e
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1906
    source: Julius_von_dem_Bussche-Haddenhausen
  AddLiteral (cfcbfd04-5e77-48fb-9cea-87599a98907a)
 Call ID: cfcbfd04-5e77-48fb-9cea-87599a98907a
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1977
    source: Julius_von_dem_Bussche-Haddenhausen
  AddTriple (a11a4f02-9375-49b9-9f83-2e88ce1d34b5)
 Call ID: a11a4f02-9375-49b9-9f83-2e88ce1d34b5
  Args:
    target: Julius_von_dem_Bussche-Haddenhausen
    source: Gösta_von_dem_Bussche-Haddenhausen
    relation: :hasBrother
  AssignClass (3a07c713-b70c-43d5-9902-b7cd897f28ab)
 Call ID: 3a07c713-b70c-43d5-9902-b7cd897f28ab
  Args:
    type: :Man
    source: Claus_Felix_von_Amsberg
  AssignClass (9e02bdcc-bd23-4450-a869-2cc4d9c8ade5)
 Call ID: 9e02bdcc-bd23-4450-a869-2cc4d9c8ade5
  Args:
    type: :Person
    source: Claus_Felix_von_Amsberg
  AddLiteral (18d3cbd9-2710-4516-9be9-c691e6b665fe)
 Call ID: 18d3cbd9-2710-4516-9be9-c691e6b665fe
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1890
    source: Claus_Felix_von_Amsberg
  AddLiteral (63b92129-7eea-4b75-935d-f48b07f30fbd)
 Call ID: 63b92129-7eea-4b75-935d-f48b07f30fbd
  Args:
    source: Claus_Felix_von_Amsberg
    literal_value: 1953
    relation: :hasDeathYear
    literal_type: xsd:integer
  AddLiteral (66ac0f97-759d-449f-88b3-db4523ee282c)
 Call ID: 66ac0f97-759d-449f-88b3-db4523ee282c
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    source: Gösta_von_dem_Bussche-Haddenhausen
    literal_value: 1924
  AssignClass (bd63891e-96a7-4f46-a643-c36bedd1b090)
 Call ID: bd63891e-96a7-4f46-a643-c36bedd1b090
  Args:
    type: :Man
    source: Wilhelm_von_Amsberg
  AssignClass (10a56539-0df7-4cca-a7a9-82dd1af7381d)
 Call ID: 10a56539-0df7-4cca-a7a9-82dd1af7381d
  Args:
    type: :Person
    source: Wilhelm_von_Amsberg
  AssignClass (d966c3ca-5180-48a7-af38-8be8ea887e00)
 Call ID: d966c3ca-5180-48a7-af38-8be8ea887e00
  Args:
    type: :Woman
    source: Elise_von_Vieregge
  AssignClass (91cc4d67-62dd-4b75-b23b-9e2cd0044496)
 Call ID: 91cc4d67-62dd-4b75-b23b-9e2cd0044496
  Args:
    type: :Person
    source: Elise_von_Vieregge
  AddTriple (39b2d194-d603-42b0-addb-ecec9b040162)
 Call ID: 39b2d194-d603-42b0-addb-ecec9b040162
  Args:
    relation: :hasFather
    source: Claus_Felix_von_Amsberg
    target: Wilhelm_von_Amsberg
  AddTriple (1846f2c3-26bb-4660-ac7a-8c94778d8a3b)
 Call ID: 1846f2c3-26bb-4660-ac7a-8c94778d8a3b
  Args:
    relation: :hasMother
    source: Claus_Felix_von_Amsberg
    target: Elise_von_Vieregge
  AssignClass (5745b363-3132-45cb-9e41-9bbf46c694c3)
 Call ID: 5745b363-3132-45cb-9e41-9bbf46c694c3
  Args:
    type: :Man
    source: Claus_Netherlands
  AssignClass (77ce84dc-b887-4d11-90a6-bc412bc855d6)
 Call ID: 77ce84dc-b887-4d11-90a6-bc412bc855d6
  Args:
    type: :Person
    source: Claus_Netherlands
  AddTriple (9d8e8c5a-3cb8-4682-9a66-e76cd3b9a84c)
 Call ID: 9d8e8c5a-3cb8-4682-9a66-e76cd3b9a84c
  Args:
    relation: :hasFather
    source: Claus_Netherlands
    target: Claus_Felix_von_Amsberg
  AddTriple (ed8ae922-f25c-4d83-be77-abf4f1423299)
 Call ID: ed8ae922-f25c-4d83-be77-abf4f1423299
  Args:
    source: Claus_Netherlands
    relation: :hasMother
    target: Gösta_von_dem_Bussche-Haddenhausen
  AddLiteral (c4aeb72c-d238-48fa-a55a-9c71b100d666)
 Call ID: c4aeb72c-d238-48fa-a55a-9c71b100d666
  Args:
    literal_value: 1926
    source: Claus_Netherlands
    relation: :hasBirthYear
    literal_type: xsd:integer
  AssignClass (7699dd15-686d-4ca5-b900-eaf5c5ed662e)
 Call ID: 7699dd15-686d-4ca5-b900-eaf5c5ed662e
  Args:
    type: :Woman
    source: Anna-Elisabeth_von_Pfuel
  AssignClass (569d2ba7-850e-46ef-9174-5e4ba435f37a)
 Call ID: 569d2ba7-850e-46ef-9174-5e4ba435f37a
  Args:
    type: :Person
    source: Anna-Elisabeth_von_Pfuel
  AddLiteral (1084062a-36dd-4598-83d4-ef3031ed2da8)
 Call ID: 1084062a-36dd-4598-83d4-ef3031ed2da8
  Args:
    source: Anna-Elisabeth_von_Pfuel
    literal_value: 1909
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (885d0ef5-7ec1-4f58-9548-a8d33ea97899)
 Call ID: 885d0ef5-7ec1-4f58-9548-a8d33ea97899
  Args:
    literal_value: 2005
    source: Anna-Elisabeth_von_Pfuel
    relation: :hasDeathYear
    literal_type: xsd:integer
  AssignClass (89b50abb-bd5b-45f2-aec8-1b369db06655)
 Call ID: 89b50abb-bd5b-45f2-aec8-1b369db06655
  Args:
    type: :Man
    source: Eberhard_Friedrich_Gustav_von_dem_Bussche-Ippenburg
  AssignClass (98a92a88-db4d-48c9-bae2-4f20ae46950d)
 Call ID: 98a92a88-db4d-48c9-bae2-4f20ae46950d
  Args:
    type: :Person
    source: Eberhard_Friedrich_Gustav_von_dem_Bussche-Ippenburg
  AddTriple (454b8a71-a270-4149-9f45-63b04d4b755b)
 Call ID: 454b8a71-a270-4149-9f45-63b04d4b755b
  Args:
    source: Gabriele_von_dem_Bussche-Ippenburg
    relation: :hasFather
    target: Eberhard_Friedrich_Gustav_von_dem_Bussche-Ippenburg
  AssignClass (d82f8797-7c19-4440-a709-4ced3118876c)
 Call ID: d82f8797-7c19-4440-a709-4ced3118876c
  Args:
    type: :Woman
    source: Armgard_von_Cramm
  AssignClass (ee142ef1-a166-4e1d-9256-8900f35acf56)
 Call ID: ee142ef1-a166-4e1d-9256-8900f35acf56
  Args:
    type: :Person
    source: Armgard_von_Cramm
  AssignClass (378238af-173d-43b8-9ceb-09e387183cc7)
 Call ID: 378238af-173d-43b8-9ceb-09e387183cc7
  Args:
    type: :Man
    source: Aschwin_of_Sierstorpff-Cramm
  AssignClass (eb810b40-8cb5-4ab8-a309-a1c03a1dd680)
 Call ID: eb810b40-8cb5-4ab8-a309-a1c03a1dd680
  Args:
    type: :Person
    source: Aschwin_of_Sierstorpff-Cramm
  AddLiteral (ed4e7edd-d6b6-473a-9e1a-46b1d0401744)
 Call ID: ed4e7edd-d6b6-473a-9e1a-46b1d0401744
  Args:
    literal_value: 1846
    source: Aschwin_of_Sierstorpff-Cramm
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (3d96d85b-fcf6-4699-b48e-047c88fa99a7)
 Call ID: 3d96d85b-fcf6-4699-b48e-047c88fa99a7
  Args:
    literal_value: 1909
    source: Aschwin_of_Sierstorpff-Cramm
    relation: :hasDeathYear
    literal_type: xsd:integer
  AssignClass (e2bbca89-b259-4336-92ab-f443a2a044af)
 Call ID: e2bbca89-b259-4336-92ab-f443a2a044af
  Args:
    type: :Woman
    source: Hedwig_von_Sierstorpff-Driburg
  AssignClass (7abdde4d-0951-4837-a7eb-04054e3178d2)
 Call ID: 7abdde4d-0951-4837-a7eb-04054e3178d2
  Args:
    type: :Person
    source: Hedwig_von_Sierstorpff-Driburg
  AddLiteral (f0c5a5ab-6678-4850-aba0-c8655508788e)
 Call ID: f0c5a5ab-6678-4850-aba0-c8655508788e
  Args:
    source: Hedwig_von_Sierstorpff-Driburg
    literal_value: 1848
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (d5b70902-e636-40c9-981b-cb1bdd471b3c)
 Call ID: d5b70902-e636-40c9-981b-cb1bdd471b3c
  Args:
    source: Hedwig_von_Sierstorpff-Driburg
    literal_value: 1900
    literal_type: xsd:integer
    relation: :hasDeathYear
  AddTriple (e9a36680-036d-4398-b7f1-e4808efc38ec)
 Call ID: e9a36680-036d-4398-b7f1-e4808efc38ec
  Args:
    target: Aschwin_of_Sierstorpff-Cramm
    relation: :hasFather
    source: Armgard_von_Cramm
  AddTriple (af355373-bdcf-493a-a180-634fd078c2c7)
 Call ID: af355373-bdcf-493a-a180-634fd078c2c7
  Args:
    relation: :hasMother
    source: Armgard_von_Cramm
    target: Hedwig_von_Sierstorpff-Driburg
  AssignClass (41876558-5e97-4d9a-a542-4ad917dff0b0)
 Call ID: 41876558-5e97-4d9a-a542-4ad917dff0b0
  Args:
    type: :Woman
    source: Hedwig_von_Sierstorpff-Cramm
  AssignClass (ea58921c-d3e2-4a01-9364-a9b22d4acda8)
 Call ID: ea58921c-d3e2-4a01-9364-a9b22d4acda8
  Args:
    type: :Person
    source: Hedwig_von_Sierstorpff-Cramm
  AddLiteral (844bd661-8353-4769-aaea-4a292ee82011)
 Call ID: 844bd661-8353-4769-aaea-4a292ee82011
  Args:
    literal_value: 1874
    source: Hedwig_von_Sierstorpff-Cramm
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (6c1ef67d-7619-48ae-a2b6-f16c1a7b4370)
 Call ID: 6c1ef67d-7619-48ae-a2b6-f16c1a7b4370
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: Hedwig_von_Sierstorpff-Cramm
    literal_value: 1907
  AddTriple (f56c0ac4-5a94-41ee-b88b-2c4acaf15665)
 Call ID: f56c0ac4-5a94-41ee-b88b-2c4acaf15665
  Args:
    source: Hedwig_von_Sierstorpff-Cramm
    relation: :hasFather
    target: Aschwin_of_Sierstorpff-Cramm
  AddTriple (7e77fc04-22b3-48df-bfe8-49393da3c248)
 Call ID: 7e77fc04-22b3-48df-bfe8-49393da3c248
  Args:
    target: Hedwig_von_Sierstorpff-Driburg
    relation: :hasMother
    source: Hedwig_von_Sierstorpff-Cramm
  Finish (31263315-0109-466e-9db6-2187bb91de73)
 Call ID: 31263315-0109-466e-9db6-2187bb91de73
  Args: