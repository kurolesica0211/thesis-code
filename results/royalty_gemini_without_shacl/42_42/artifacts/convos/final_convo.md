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
Prince George of Wales (George Alexander Louis; born 22 July 2013) is a member of the British royal family.
He is the eldest child of William, Prince of Wales, and Catherine, Princess of Wales, and the eldest grandchild of King Charles III and Diana, Princess of Wales.
George was born at St Mary's Hospital, London, during the reign of his paternal great-grandmother, Queen Elizabeth II, and was third in line before her death.
Infancy

George was born at 4:24 pm on 22 July 2013 at St Mary's Hospital, London, during the reign of his paternal great-grandmother, Queen Elizabeth II.
He is the eldest child of Prince William and Catherine (then known as Duke and Duchess of Cambridge).
He has a younger sister and brother, Princess Charlotte and Prince Louis.
His name was announced as George Alexander Louis on 24 July.
George was third in the line of succession to the British throne at the time of his birth.
For the first time since the reign of Queen Victoria, three generations in direct line of succession to the British throne were alive at the same time: George; his father, William; and his grandfather, Charles.
George was christened on 23 October by the archbishop of Canterbury, Justin Welby, in the Chapel Royal at St James's Palace.
Upbringing

George spent his first months in Anglesey, Wales, before his family relocated to Kensington Palace in 2014.
Although George appeared only twice, the BBC described the "nine-month-old future king" as "the star of the show".
The then Australian prime minister Tony Abbott predicted in the Parliament House, Canberra, that George would one day be welcomed there as King of Australia.
In June 2015, George made his first appearance on the balcony of Buckingham Palace following the Trooping the Colour parade.
George met Barack and Michelle Obama, then President and First Lady of the United States, in April 2016.
George started junior school under the name George Cambridge in September 2017, at Thomas's School, an independent preparatory school in Battersea.
Since September of that year, George and his siblings have attended Lambrook, an independent preparatory school in Berkshire.
George commenced flying lessons in September 2024.
George took part in his great-grandmother's Platinum Jubilee celebration in June 2022, including the Trooping the Colour carriage procession.
Elizabeth II died on 8 September 2022 and was succeeded by George's grandfather, Charles III, making George second in line to the throne behind his father.
George and his siblings occasionally accompany their parents on royal engagements, tours, and diplomatic visits.
In December 2025, George accompanied his father on a visit to The Passage, a homelessness charity of which his father is patron.
Public image

Clothing and other products used by George are often sold out, a phenomenon termed the "Prince George effect".
In August 2015, Kensington Palace stated that they wanted all global media to stop taking unauthorised photographs of George, saying that "a line  been crossed" in paparazzi methods of locating and photographing him, including surveilling the family and sending children to bring George into view.
Title and styles

George is a British prince with the official style and title "His Royal Highness Prince George of Wales".
During the reign of his great-grandmother, he was styled "His Royal Highness Prince George of Cambridge".



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
  AssignClass (9b5b79f2-5721-449b-ad4b-94639df86bd1)
 Call ID: 9b5b79f2-5721-449b-ad4b-94639df86bd1
  Args:
    type: :Person
    source: George_Alexander_Louis
  AssignClass (8a03d926-c158-4d0b-b458-99df305d9cac)
 Call ID: 8a03d926-c158-4d0b-b458-99df305d9cac
  Args:
    type: :Person
    source: William_Prince_of_Wales
  AssignClass (7c80aab9-dae0-49d3-8fae-f2bb1497b554)
 Call ID: 7c80aab9-dae0-49d3-8fae-f2bb1497b554
  Args:
    type: :Person
    source: Catherine_Princess_of_Wales
  AssignClass (58e3b4f5-f5d5-47ba-afe8-227d18d41485)
 Call ID: 58e3b4f5-f5d5-47ba-afe8-227d18d41485
  Args:
    type: :Person
    source: Charles_III
  AssignClass (d65e007b-84b9-413e-9a61-2be6f68239f2)
 Call ID: d65e007b-84b9-413e-9a61-2be6f68239f2
  Args:
    type: :Person
    source: Diana_Princess_of_Wales
  AssignClass (bcbc600c-8600-4f9b-911a-2b35c693d9f8)
 Call ID: bcbc600c-8600-4f9b-911a-2b35c693d9f8
  Args:
    type: :Person
    source: Elizabeth_II
  AssignClass (e020a250-ae27-4ea3-9d7c-bd0c30673457)
 Call ID: e020a250-ae27-4ea3-9d7c-bd0c30673457
  Args:
    type: :Person
    source: Charlotte
  AssignClass (659b9549-747a-4306-b2e7-6bdb3fb3759e)
 Call ID: 659b9549-747a-4306-b2e7-6bdb3fb3759e
  Args:
    type: :Person
    source: Louis
  AssignClass (68747708-0551-4006-a38f-ded166efd181)
 Call ID: 68747708-0551-4006-a38f-ded166efd181
  Args:
    type: :Man
    source: George_Alexander_Louis
  AssignClass (343002c8-ce39-4b55-ad24-5acb1cea1d32)
 Call ID: 343002c8-ce39-4b55-ad24-5acb1cea1d32
  Args:
    type: :Man
    source: William_Prince_of_Wales
  AssignClass (fe960e43-263b-4bdc-9bd9-b021c1a3c869)
 Call ID: fe960e43-263b-4bdc-9bd9-b021c1a3c869
  Args:
    type: :Woman
    source: Catherine_Princess_of_Wales
  AssignClass (54de6b8e-1011-4f84-953f-0a6cf7c46855)
 Call ID: 54de6b8e-1011-4f84-953f-0a6cf7c46855
  Args:
    type: :Man
    source: Charles_III
  AssignClass (c80c8007-5493-44d5-bc42-786dabf1d6be)
 Call ID: c80c8007-5493-44d5-bc42-786dabf1d6be
  Args:
    type: :Woman
    source: Diana_Princess_of_Wales
  AssignClass (1843e1fc-b33c-40c0-af2b-b89857f669ad)
 Call ID: 1843e1fc-b33c-40c0-af2b-b89857f669ad
  Args:
    type: :Woman
    source: Elizabeth_II
  AssignClass (41a6cee2-e08d-4da5-842a-06f8278b8a8c)
 Call ID: 41a6cee2-e08d-4da5-842a-06f8278b8a8c
  Args:
    type: :Woman
    source: Charlotte
  AssignClass (302c7cc7-6c80-43fd-bb35-cc3de9a24e0d)
 Call ID: 302c7cc7-6c80-43fd-bb35-cc3de9a24e0d
  Args:
    type: :Man
    source: Louis
  AddLiteral (ae28fd5f-9f67-4f86-8117-5b25a77a4fb7)
 Call ID: ae28fd5f-9f67-4f86-8117-5b25a77a4fb7
  Args:
    source: George_Alexander_Louis
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 2013
  AddTriple (53837f5d-8510-45f0-94d4-a6b42356cc9f)
 Call ID: 53837f5d-8510-45f0-94d4-a6b42356cc9f
  Args:
    target: William_Prince_of_Wales
    source: George_Alexander_Louis
    relation: :hasFather
  AddTriple (43f3826c-9595-415c-b448-85a3856a5cd1)
 Call ID: 43f3826c-9595-415c-b448-85a3856a5cd1
  Args:
    target: Catherine_Princess_of_Wales
    source: George_Alexander_Louis
    relation: :hasMother
  AddTriple (4eedfd39-2a8b-455a-b688-5637b15e237c)
 Call ID: 4eedfd39-2a8b-455a-b688-5637b15e237c
  Args:
    relation: :hasSister
    source: George_Alexander_Louis
    target: Charlotte
  AddTriple (c51b62d4-20b2-4716-a32f-72edce59b446)
 Call ID: c51b62d4-20b2-4716-a32f-72edce59b446
  Args:
    source: George_Alexander_Louis
    relation: :hasBrother
    target: Louis
  AddTriple (ee1c3b93-e288-4bda-85dc-6e73870e1d95)
 Call ID: ee1c3b93-e288-4bda-85dc-6e73870e1d95
  Args:
    target: Charles_III
    source: William_Prince_of_Wales
    relation: :hasFather
  AddTriple (240ce81a-92f8-4fff-a8f5-4d643de33dc6)
 Call ID: 240ce81a-92f8-4fff-a8f5-4d643de33dc6
  Args:
    relation: :hasMother
    source: William_Prince_of_Wales
    target: Diana_Princess_of_Wales
  Finish (8ef8c338-afbb-4b3e-96e7-d9f5a27b2907)
 Call ID: 8ef8c338-afbb-4b3e-96e7-d9f5a27b2907
  Args: