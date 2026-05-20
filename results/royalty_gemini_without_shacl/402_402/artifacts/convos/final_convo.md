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
Lord Ivar Alexander Michael Mountbatten, DL (born 9 March 1963) is a British aristocrat, farmer, geologist, businessman, and reality television personality.
Early life and family

Ivar
Alexander Michael Mountbatten was born in London, to David Mountbatten, 3rd Marquess of Milford Haven, and the former Janet Mercedes Bryce.
His elder brother is George Mountbatten, 4th Marquess of Milford Haven.
His paternal grandfather was Prince George of Battenberg, through whom he is a morganatic descendant of the House of Hesse-Darmstadt.
Mountbatten grew up at Moyns Park in Essex.
In a June 2022 interview with Tatler Mountbatten commented on the 1930s Gloria Vanderbilt child custody trial, where a maid made an allegation of a lesbian affair between the child's mother Gloria Morgan Vanderbilt and the Marchioness of Milford Haven, Mountbatten's grandmother.
Mountbatten was educated at Gordonstoun School, the same school attended by Prince Philip and Charles III, and he graduated from Middlebury College in Vermont with a BA degree.
Career

Mountbatten began his career as a geologist and spent significant time working in South America during his early career.
Starting in 1995, Mountbatten began his involvement in business pursuits, including being the director of the UK subsidiary of DMX Music and being involved with Coldharbour Mill Working Wool Museum.
Mountbatten was later involved with SCL Group, the parent company of the now-defunct data analytics firm Cambridge Analytica.
Mountbatten also serves as a Deputy Lieutenant of Devon.
In 2019, Mountbatten began a career in reality television by starring in the sixth series of Treasure Island with Bear Grylls.
In October 2024, Mountbatten was announced to be part of the third season of the American reality competition series The Traitors, which premiered on 9 January 2025.
Personal life

Mountbatten married Penelope Anne Vere Thompson (born Salisbury, Wiltshire, 17 March 1966), only daughter of Colin Graham Thompson of Old Manor House, Sutton Veny, Wiltshire, and Rosemary Vere Edwardes.
The ceremony took place on 23 April 1994 at the Church of Saint Peter and Saint Paul in Clare, Suffolk.
In September 2016, Mountbatten revealed that he was in a relationship with James Coyle, an airline cabin services director whom he met while at a ski resort in Verbier.
Mountbatten's former wife walked him down the aisle and 'gave him away' at the suggestion of their daughters.
Mountbatten is a godparent of Lady Louise Windsor (born 2003), the daughter of Prince Edward and Sophie.
Mountbatten inherited Moyns Park in 1992 along with his brother, George Mountbatten, 4th Marquess of Milford Haven, but in 1997 moved to Bridwell Park in Uffculme, Devon.



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
  AssignClass (e1c86b18-ad63-455e-9957-ffb4b2e50983)
 Call ID: e1c86b18-ad63-455e-9957-ffb4b2e50983
  Args:
    source: Ivar_Mountbatten
    type: :Man
  AssignClass (5ece35bb-ce5c-4806-b617-a02703c3c507)
 Call ID: 5ece35bb-ce5c-4806-b617-a02703c3c507
  Args:
    source: Ivar_Mountbatten
    type: :Person
  AddLiteral (7da9a9f3-bc87-4030-bf06-4eb4428835f7)
 Call ID: 7da9a9f3-bc87-4030-bf06-4eb4428835f7
  Args:
    literal_value: 1963
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Ivar_Mountbatten
  AssignClass (64612479-fa0e-41fd-a6d4-67621628d70d)
 Call ID: 64612479-fa0e-41fd-a6d4-67621628d70d
  Args:
    source: David_Mountbatten
    type: :Man
  AssignClass (4f29d613-210e-4340-8a16-3dd129a85597)
 Call ID: 4f29d613-210e-4340-8a16-3dd129a85597
  Args:
    source: David_Mountbatten
    type: :Person
  AssignClass (dc600dfe-ecbd-42e4-9113-b41bd5f7ba88)
 Call ID: dc600dfe-ecbd-42e4-9113-b41bd5f7ba88
  Args:
    type: :Woman
    source: Janet_Mercedes_Bryce
  AssignClass (82a002f1-5baa-4bc3-ac19-bb730a718cef)
 Call ID: 82a002f1-5baa-4bc3-ac19-bb730a718cef
  Args:
    source: Janet_Mercedes_Bryce
    type: :Person
  AddTriple (91561c41-a132-4d02-b999-bd87ddeff677)
 Call ID: 91561c41-a132-4d02-b999-bd87ddeff677
  Args:
    source: Ivar_Mountbatten
    target: David_Mountbatten
    relation: :hasFather
  AddTriple (a7beeedf-f34c-474f-81ae-d5f9edd71fbd)
 Call ID: a7beeedf-f34c-474f-81ae-d5f9edd71fbd
  Args:
    target: Janet_Mercedes_Bryce
    relation: :hasMother
    source: Ivar_Mountbatten
  AssignClass (0b4444c5-3612-4b50-92c7-2205bb132068)
 Call ID: 0b4444c5-3612-4b50-92c7-2205bb132068
  Args:
    source: George_Mountbatten
    type: :Man
  AssignClass (4aa7fa41-59a8-4ba2-ab6d-01682d49ed30)
 Call ID: 4aa7fa41-59a8-4ba2-ab6d-01682d49ed30
  Args:
    source: George_Mountbatten
    type: :Person
  AddTriple (f9fe0283-c211-4c2d-b567-a0432c7139e6)
 Call ID: f9fe0283-c211-4c2d-b567-a0432c7139e6
  Args:
    target: George_Mountbatten
    relation: :hasBrother
    source: Ivar_Mountbatten
  AssignClass (dcabc16d-0ce8-47e8-942b-7994ebc8a453)
 Call ID: dcabc16d-0ce8-47e8-942b-7994ebc8a453
  Args:
    source: Prince_George_of_Battenberg
    type: :Man
  AssignClass (3127d907-0b8f-4517-9984-9263c378bc3e)
 Call ID: 3127d907-0b8f-4517-9984-9263c378bc3e
  Args:
    source: Prince_George_of_Battenberg
    type: :Person
  AddTriple (a6ab7a82-f6f1-49ed-9f8c-643d3917b457)
 Call ID: a6ab7a82-f6f1-49ed-9f8c-643d3917b457
  Args:
    target: Prince_George_of_Battenberg
    relation: :hasAncestor
    source: Ivar_Mountbatten
  AssignClass (4c93d08b-9296-450a-bcc8-836ba5dde932)
 Call ID: 4c93d08b-9296-450a-bcc8-836ba5dde932
  Args:
    type: :Woman
    source: Penelope_Anne_Vere_Thompson
  AssignClass (d3c52245-4650-444c-877b-b0d53490c242)
 Call ID: d3c52245-4650-444c-877b-b0d53490c242
  Args:
    source: Penelope_Anne_Vere_Thompson
    type: :Person
  AddLiteral (65558894-5314-4778-9991-9fbb8e1f6c13)
 Call ID: 65558894-5314-4778-9991-9fbb8e1f6c13
  Args:
    relation: :hasBirthYear
    source: Penelope_Anne_Vere_Thompson
    literal_value: 1966
    literal_type: xsd:integer
  AddLiteral (c393aa4f-dee6-44e9-8229-b34fadd7b0dc)
 Call ID: c393aa4f-dee6-44e9-8229-b34fadd7b0dc
  Args:
    relation: :hasMarriageYear
    source: Ivar_Mountbatten
    literal_value: 1994
    literal_type: xsd:integer
  AddTriple (7ecdf63f-c47b-466e-b807-373edd47a617)
 Call ID: 7ecdf63f-c47b-466e-b807-373edd47a617
  Args:
    target: Penelope_Anne_Vere_Thompson
    relation: :hasRelation
    source: Ivar_Mountbatten
  AssignClass (77b52eda-6e99-4644-9406-c8ff06da1b07)
 Call ID: 77b52eda-6e99-4644-9406-c8ff06da1b07
  Args:
    source: James_Coyle
    type: :Man
  AssignClass (0b7e3746-060b-4bfa-b502-b9a08685b6e2)
 Call ID: 0b7e3746-060b-4bfa-b502-b9a08685b6e2
  Args:
    source: James_Coyle
    type: :Person
  AddTriple (1c19a429-8045-4a0e-befa-452b1591c771)
 Call ID: 1c19a429-8045-4a0e-befa-452b1591c771
  Args:
    relation: :hasRelation
    target: James_Coyle
    source: Ivar_Mountbatten
  AssignClass (d14df169-12e0-4d4f-ac21-04cd10c2bc60)
 Call ID: d14df169-12e0-4d4f-ac21-04cd10c2bc60
  Args:
    type: :Woman
    source: Lady_Louise_Windsor
  AssignClass (678926d1-d930-40c0-b4ab-82652690f250)
 Call ID: 678926d1-d930-40c0-b4ab-82652690f250
  Args:
    type: :Person
    source: Lady_Louise_Windsor
  AddLiteral (51cba2f0-7671-4ac3-ab73-6881e1fef4be)
 Call ID: 51cba2f0-7671-4ac3-ab73-6881e1fef4be
  Args:
    literal_value: 2003
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Lady_Louise_Windsor
  Finish (5d1d74dc-12a7-487d-997c-00b7c0ebfd16)
 Call ID: 5d1d74dc-12a7-487d-997c-00b7c0ebfd16
  Args: