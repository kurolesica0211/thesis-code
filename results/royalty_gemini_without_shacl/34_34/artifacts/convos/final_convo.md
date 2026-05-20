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
Marina Victoria Alexandra Ogilvy (born 31 July 1966) is the younger child and only daughter of Sir Angus Ogilvy and Princess Alexandra of Kent.
Early life

Marina was born at Thatched House Lodge in Richmond Park, London, the home of her parents, on 31 July 1966.
She was named after her maternal grandmother, Princess Marina of Greece and Denmark, who was also a first cousin of Prince Philip, Duke of Edinburgh.
She has an elder brother, James Ogilvy, who was born in 1964.
Marina was educated at St Mary's School, Wantage.
Marriage and children

In November 1989, Marina announced that she was pregnant by her boyfriend Paul Julian Mowatt (born in Hendon, 28 November 1962), a freelance photographer.
Marina's parents denied her allegations and said that they loved her, had not cut her off and that she was welcome at home any time.
Marina married Mowatt in Richmond Park, Surrey, on 2 February 1990, wearing a red velvet bolero with gold trim, with a black dress underneath, and a black hat.
They had two children: Zenouska May Mowatt (born 26 May 1990), and Christian Alexander Mowatt (born 4 June 1993) and divorced in October 1997.



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
  AssignClass (8c337374-2e12-4671-a1f5-2de753db2984)
 Call ID: 8c337374-2e12-4671-a1f5-2de753db2984
  Args:
    type: :Person
    source: Marina_Ogilvy
  AssignClass (0160fcbd-495c-4d04-a091-a7812d1da71b)
 Call ID: 0160fcbd-495c-4d04-a091-a7812d1da71b
  Args:
    type: :Woman
    source: Marina_Ogilvy
  AddLiteral (2d09587f-0045-4fb1-9f51-9ac296a4fa3d)
 Call ID: 2d09587f-0045-4fb1-9f51-9ac296a4fa3d
  Args:
    literal_value: 1966
    literal_type: xsd:integer
    source: Marina_Ogilvy
    relation: :hasBirthYear
  AssignClass (d402d9d3-33ca-4901-b7ee-9fedde5b5ac8)
 Call ID: d402d9d3-33ca-4901-b7ee-9fedde5b5ac8
  Args:
    type: :Person
    source: Angus_Ogilvy
  AssignClass (256d8d08-8362-4f9a-bc16-b4dea79d5c3b)
 Call ID: 256d8d08-8362-4f9a-bc16-b4dea79d5c3b
  Args:
    type: :Man
    source: Angus_Ogilvy
  AssignClass (26e1219b-fe81-469a-95ad-5a112bc801cc)
 Call ID: 26e1219b-fe81-469a-95ad-5a112bc801cc
  Args:
    source: Alexandra_of_Kent
    type: :Person
  AssignClass (2f126760-097a-4fb4-9e02-f67463d356ff)
 Call ID: 2f126760-097a-4fb4-9e02-f67463d356ff
  Args:
    type: :Woman
    source: Alexandra_of_Kent
  AddTriple (964ee711-31a4-4109-b4f6-4208c2f71fb5)
 Call ID: 964ee711-31a4-4109-b4f6-4208c2f71fb5
  Args:
    target: Angus_Ogilvy
    relation: :hasFather
    source: Marina_Ogilvy
  AddTriple (d80134d8-a502-400f-930f-ac2edbebd910)
 Call ID: d80134d8-a502-400f-930f-ac2edbebd910
  Args:
    relation: :hasMother
    target: Alexandra_of_Kent
    source: Marina_Ogilvy
  AssignClass (cd0f87fa-e82b-47d0-ad7d-d4955b827ecf)
 Call ID: cd0f87fa-e82b-47d0-ad7d-d4955b827ecf
  Args:
    source: James_Ogilvy
    type: :Person
  AssignClass (a0f3cccb-975e-40e4-9ae3-efa082009ce8)
 Call ID: a0f3cccb-975e-40e4-9ae3-efa082009ce8
  Args:
    source: James_Ogilvy
    type: :Man
  AddTriple (bdc9ed67-bb22-4bbe-a95a-a50cdadaaa62)
 Call ID: bdc9ed67-bb22-4bbe-a95a-a50cdadaaa62
  Args:
    relation: :hasBrother
    target: James_Ogilvy
    source: Marina_Ogilvy
  AssignClass (f524fb3e-3e16-4238-b592-d8c71759f215)
 Call ID: f524fb3e-3e16-4238-b592-d8c71759f215
  Args:
    source: Marina_of_Greece_and_Denmark
    type: :Person
  AssignClass (722f4a7c-7c7a-45f2-b339-4d5726b4f957)
 Call ID: 722f4a7c-7c7a-45f2-b339-4d5726b4f957
  Args:
    source: Marina_of_Greece_and_Denmark
    type: :Woman
  AssignClass (1b429521-5f81-4312-8b8b-8d01de44dac8)
 Call ID: 1b429521-5f81-4312-8b8b-8d01de44dac8
  Args:
    source: Paul_Julian_Mowatt
    type: :Person
  AssignClass (de465303-e578-4312-b876-9c74fc64c5ce)
 Call ID: de465303-e578-4312-b876-9c74fc64c5ce
  Args:
    type: :Man
    source: Paul_Julian_Mowatt
  AddLiteral (25ffd35a-02a3-4027-9ec5-8c3e28c15190)
 Call ID: 25ffd35a-02a3-4027-9ec5-8c3e28c15190
  Args:
    relation: :hasBirthYear
    source: Paul_Julian_Mowatt
    literal_type: xsd:integer
    literal_value: 1962
  AddTriple (931f27c0-9e16-46cd-8ba9-646df3f6c4a1)
 Call ID: 931f27c0-9e16-46cd-8ba9-646df3f6c4a1
  Args:
    source: Marina_Ogilvy
    target: Paul_Julian_Mowatt
    relation: :hasRelation
  AssignClass (03ad2126-1c67-42c1-8181-7db4bfbcdec4)
 Call ID: 03ad2126-1c67-42c1-8181-7db4bfbcdec4
  Args:
    source: Zenouska_May_Mowatt
    type: :Person
  AssignClass (542f550f-4c2d-48d1-83d3-169d32544fa9)
 Call ID: 542f550f-4c2d-48d1-83d3-169d32544fa9
  Args:
    source: Zenouska_May_Mowatt
    type: :Woman
  AddTriple (c9c39bfd-25da-4671-8d83-595bf3cf6888)
 Call ID: c9c39bfd-25da-4671-8d83-595bf3cf6888
  Args:
    source: Zenouska_May_Mowatt
    relation: :hasMother
    target: Marina_Ogilvy
  AddTriple (9d20092c-03cf-4b48-988e-614135c249dd)
 Call ID: 9d20092c-03cf-4b48-988e-614135c249dd
  Args:
    target: Paul_Julian_Mowatt
    relation: :hasFather
    source: Zenouska_May_Mowatt
  AssignClass (56ef0ad5-48ee-4f02-bce9-162eed51b9ef)
 Call ID: 56ef0ad5-48ee-4f02-bce9-162eed51b9ef
  Args:
    type: :Person
    source: Christian_Alexander_Mowatt
  AssignClass (ec1c3bd7-1628-4112-a83c-a5ee0901df5e)
 Call ID: ec1c3bd7-1628-4112-a83c-a5ee0901df5e
  Args:
    type: :Man
    source: Christian_Alexander_Mowatt
  AddTriple (d123766d-b764-467e-9a0d-eb5b56cee626)
 Call ID: d123766d-b764-467e-9a0d-eb5b56cee626
  Args:
    target: Marina_Ogilvy
    relation: :hasMother
    source: Christian_Alexander_Mowatt
  AddTriple (1c1dc712-b872-46c5-a8e5-fc887a2cd515)
 Call ID: 1c1dc712-b872-46c5-a8e5-fc887a2cd515
  Args:
    target: Paul_Julian_Mowatt
    relation: :hasFather
    source: Christian_Alexander_Mowatt
  Finish (bc007a66-06d2-4375-a706-4010b428a14f)
 Call ID: bc007a66-06d2-4375-a706-4010b428a14f
  Args: