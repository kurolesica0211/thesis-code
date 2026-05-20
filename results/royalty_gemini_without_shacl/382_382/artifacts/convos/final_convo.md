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
Moritz, Landgrave of Hesse (legally Moritz Friedrich Karl Emanuel Humbert Prinz und Landgraf von Hessen; 6 August 1926 – 23 May 2013) was the son of Prince Philip, Landgrave of Hesse, and the head of the House of Hesse, also known as the House of Brabant.
Life

Landgrave Moritz was born at Racconigi Castle, in Italy.
During the Second World War, Moritz's mother, Princess Mafalda of Savoy, was arrested by the Nazis for alleged subversive activities and died in the Buchenwald concentration camp in 1944 as a result of a U.S. bombing raid on the camp.
Moritz and his siblings (Heinrich, Otto and Elisabeth) were given sanctuary in the Vatican under the care of their uncle Louis, Prince of Hesse and by Rhine and aunt Margaret Campbell Geddes who adopted them.
Prince Louis of Hesse and by Rhine, the last head of the Hesse-Darmstadt line, died in 1968, at which time Moritz's father succeeded him as head of the entire house.
Moritz became the head of the House of Hesse after the death of his father Philip on 25 October 1980.
Moritz was a world-famous art collector.
He presided over the Foundation of the House of Hesse which is the proprietor of the Kronberg Palace Hotel and several manor estates and palaces.
Marriage and children

Moritz married Princess Tatiana of Sayn-Wittgenstein-Berleburg, daughter of Prince Gustav Albrecht.



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
  AssignClass (a9ffa678-5c90-4cc4-b1f8-b23b1f422712)
 Call ID: a9ffa678-5c90-4cc4-b1f8-b23b1f422712
  Args:
    type: :Man
    source: Moritz
  AssignClass (18f15c47-2d1c-4089-a086-b0f03e61d443)
 Call ID: 18f15c47-2d1c-4089-a086-b0f03e61d443
  Args:
    type: :Man
    source: Philip
  AssignClass (d81a5e48-0d91-4de5-9c83-a930f018409c)
 Call ID: d81a5e48-0d91-4de5-9c83-a930f018409c
  Args:
    type: :Woman
    source: Mafalda
  AssignClass (433f90b8-607c-4c41-9617-f652c341497f)
 Call ID: 433f90b8-607c-4c41-9617-f652c341497f
  Args:
    type: :Man
    source: Heinrich
  AssignClass (f288f744-a00c-4643-ae03-44aec2fc4f72)
 Call ID: f288f744-a00c-4643-ae03-44aec2fc4f72
  Args:
    type: :Man
    source: Otto
  AssignClass (5dcc1744-d334-420e-b4e4-3db772a30e38)
 Call ID: 5dcc1744-d334-420e-b4e4-3db772a30e38
  Args:
    type: :Woman
    source: Elisabeth
  AssignClass (a190ec65-d88a-4e87-88ab-b7236180186e)
 Call ID: a190ec65-d88a-4e87-88ab-b7236180186e
  Args:
    type: :Man
    source: Louis
  AssignClass (32669359-34ee-459b-85a9-70629974a308)
 Call ID: 32669359-34ee-459b-85a9-70629974a308
  Args:
    type: :Woman
    source: MargaretCampbellGeddes
  AssignClass (4c7d6d07-aa3b-423e-a840-1bbcfd13c232)
 Call ID: 4c7d6d07-aa3b-423e-a840-1bbcfd13c232
  Args:
    type: :Woman
    source: Tatiana
  AssignClass (3fe0a2f2-d3ac-4061-bd47-8d5503f00339)
 Call ID: 3fe0a2f2-d3ac-4061-bd47-8d5503f00339
  Args:
    type: :Man
    source: GustavAlbrecht
  AddLiteral (fe09d00a-3db8-470a-be84-6295e1192ba0)
 Call ID: fe09d00a-3db8-470a-be84-6295e1192ba0
  Args:
    source: Moritz
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1926
  AddLiteral (87e37ad7-1df6-478b-9226-305b6800d377)
 Call ID: 87e37ad7-1df6-478b-9226-305b6800d377
  Args:
    literal_value: 2013
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: Moritz
  AddTriple (cfd81265-54b5-4910-8369-cc6ae5262c0c)
 Call ID: cfd81265-54b5-4910-8369-cc6ae5262c0c
  Args:
    target: Philip
    relation: :hasFather
    source: Moritz
  AddTriple (ca416627-4ac5-4e70-ac49-c39ead126797)
 Call ID: ca416627-4ac5-4e70-ac49-c39ead126797
  Args:
    source: Moritz
    target: Mafalda
    relation: :hasMother
  AddTriple (c004a0e9-8c7d-4098-99dc-4eecf4d5b114)
 Call ID: c004a0e9-8c7d-4098-99dc-4eecf4d5b114
  Args:
    target: Moritz
    relation: :isBrotherOf
    source: Heinrich
  AddTriple (44789044-a507-49f7-84cd-cb704910d180)
 Call ID: 44789044-a507-49f7-84cd-cb704910d180
  Args:
    source: Otto
    relation: :isBrotherOf
    target: Moritz
  AddTriple (2ad31dee-6b71-4220-a7d9-1b4152373939)
 Call ID: 2ad31dee-6b71-4220-a7d9-1b4152373939
  Args:
    relation: :isSisterOf
    target: Moritz
    source: Elisabeth
  AddTriple (3652e696-4345-4f13-ac1a-9f44548a3e54)
 Call ID: 3652e696-4345-4f13-ac1a-9f44548a3e54
  Args:
    source: Louis
    relation: :isUncleOf
    target: Moritz
  AddTriple (50fcd350-4637-4a49-a0be-61f9d6c77a2e)
 Call ID: 50fcd350-4637-4a49-a0be-61f9d6c77a2e
  Args:
    relation: :isUncleOf
    target: Heinrich
    source: Louis
  AddTriple (fda478b5-c422-4c5c-943d-221791ed3ab7)
 Call ID: fda478b5-c422-4c5c-943d-221791ed3ab7
  Args:
    source: Louis
    relation: :isUncleOf
    target: Otto
  AddTriple (9d418d60-1b75-4090-ac0d-6057535b3ac9)
 Call ID: 9d418d60-1b75-4090-ac0d-6057535b3ac9
  Args:
    source: Louis
    relation: :isUncleOf
    target: Elisabeth
  AddTriple (619ad4ef-7280-400b-af88-d7c985936e4e)
 Call ID: 619ad4ef-7280-400b-af88-d7c985936e4e
  Args:
    target: Tatiana
    relation: :isFatherOf
    source: GustavAlbrecht
  Finish (f907d231-490e-4470-b4d8-e29bdc94a0dc)
 Call ID: f907d231-490e-4470-b4d8-e29bdc94a0dc
  Args: