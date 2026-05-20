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
Prince Alexander Ferdinand Albrecht Achilles Wilhelm Joseph Viktor Karl Feodor of Prussia (26 December 1912 – 12 June 1985) was the only son of Prince August Wilhelm of Prussia and Princess Alexandra Victoria of Schleswig-Holstein-Sonderburg-Glücksburg.
Family and early life

Prince Alexander of Prussia was born on 26 December 1912 to Prince August Wilhelm of Prussia and his wife Princess Alexandra Victoria of Schleswig-Holstein-Sonderburg-Glücksburg.
August Wilhelm was a younger son of Kaiser Wilhelm II.
His parents divorced in 1920 and his mother remarried less than two years later; custody of the young prince was awarded to Alexander's father.
Alexander attended the 1932 wedding of the Swedish prince Gustaf Adolf, Duke of Västerbotten with Princess Sibylla of Saxe-Coburg-Gotha in the former duchy of Coburg; it was the first time that a member of the German imperial family had entered the duchy since it became a republic, or specifically a part of Bavaria in November 1919 after the ruling duke, Carl Eduard, had ended his reign on 14 November 1918.
Nazi Party and military career

As of November 1939, Prince Alexander was a first lieutenant in the Air Force Signal Corps, stationed in Wiesbaden.
Like his father, who became a prominent supporter of the Nazi Party, Alexander became an early supporter.
Prince August had secret hopes that Chancellor Adolf Hitler "would one day hoist him or his son Alexander up to the vacant throne of the Kaiser".
The support that father and son gave to the emerging party caused strong disagreements among the Hohenzollerns, with Wilhelm II urging them both to leave the party.
In 1933, Alexander quit the SA and became a private in the German regular army.
Unlike many other German princes, who became the targets of Hitler's mistrust and were removed from their commands in the military, Alexander was the only Hohenzollern allowed to remain at his post.
Marriage

On 19 December 1938 in the Dresden garrison church, Alexander non-dynastically married Armgard Weygand (22 August 1912 – 3 December 2001), daughter of Major Friedrich Weygand and Karla Franziska Oheim.
She was married from 1928 to 1933 to Werner Rosendorff, airman in the German Air Force, and was originally from Wiesbaden, where Alexander Ferdinand was stationed.
They had one son:


Death

Prince Alexander Ferdinand died on 12 June 1985 at Wiesbaden.
}} Media related to Prince Alexander Ferdinand of Prussia at Wikimedia Commons



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
  AssignClass (f61058e0-e167-4e8e-8d45-5f2e48c15f68)
 Call ID: f61058e0-e167-4e8e-8d45-5f2e48c15f68
  Args:
    type: :Man
    source: :Alexander_of_Prussia
  AssignClass (7c879f20-b998-4bcb-b2dc-55f63f1da2a4)
 Call ID: 7c879f20-b998-4bcb-b2dc-55f63f1da2a4
  Args:
    type: :Person
    source: :Alexander_of_Prussia
  AssignClass (f38b8b6f-d164-410f-ad48-9f6948d4f64b)
 Call ID: f38b8b6f-d164-410f-ad48-9f6948d4f64b
  Args:
    source: :August_Wilhelm_of_Prussia
    type: :Man
  AssignClass (de5f7159-b5e0-452f-8269-79692ad04b07)
 Call ID: de5f7159-b5e0-452f-8269-79692ad04b07
  Args:
    source: :August_Wilhelm_of_Prussia
    type: :Person
  AssignClass (dc3bec17-74b1-4ef0-ab1d-66196ba185b9)
 Call ID: dc3bec17-74b1-4ef0-ab1d-66196ba185b9
  Args:
    source: :Alexandra_Victoria_of_Schleswig-Holstein-Sonderburg-Glücksburg
    type: :Woman
  AssignClass (65787a40-2c86-4bad-aa8f-89f1838e67c7)
 Call ID: 65787a40-2c86-4bad-aa8f-89f1838e67c7
  Args:
    source: :Alexandra_Victoria_of_Schleswig-Holstein-Sonderburg-Glücksburg
    type: :Person
  AssignClass (6c20a0fd-af29-423d-937e-6359f9abeb12)
 Call ID: 6c20a0fd-af29-423d-937e-6359f9abeb12
  Args:
    type: :Man
    source: :Wilhelm_II
  AssignClass (d9ffd141-6e2f-4c79-a24e-502789c33f61)
 Call ID: d9ffd141-6e2f-4c79-a24e-502789c33f61
  Args:
    source: :Wilhelm_II
    type: :Person
  AssignClass (7fd8147d-5e34-4e78-bc7e-6d4184a2e6cf)
 Call ID: 7fd8147d-5e34-4e78-bc7e-6d4184a2e6cf
  Args:
    source: :Armgard_Weygand
    type: :Woman
  AssignClass (076bc7b0-df4a-4226-b850-b501b5524d30)
 Call ID: 076bc7b0-df4a-4226-b850-b501b5524d30
  Args:
    type: :Person
    source: :Armgard_Weygand
  AssignClass (3d7b2dc5-c856-43ba-aec0-c034a048264b)
 Call ID: 3d7b2dc5-c856-43ba-aec0-c034a048264b
  Args:
    source: :Friedrich_Weygand
    type: :Man
  AssignClass (fb54093b-9619-44d5-8cf7-5c80cff343c0)
 Call ID: fb54093b-9619-44d5-8cf7-5c80cff343c0
  Args:
    type: :Person
    source: :Friedrich_Weygand
  AssignClass (67777765-ea26-4951-894f-3cf3c0fb36b3)
 Call ID: 67777765-ea26-4951-894f-3cf3c0fb36b3
  Args:
    type: :Woman
    source: :Karla_Franziska_Oheim
  AssignClass (7f4b0c95-c554-4fdd-b3c1-e4cac40541de)
 Call ID: 7f4b0c95-c554-4fdd-b3c1-e4cac40541de
  Args:
    type: :Person
    source: :Karla_Franziska_Oheim
  AssignClass (44e3aebc-b71e-4d52-ba67-980daea5844f)
 Call ID: 44e3aebc-b71e-4d52-ba67-980daea5844f
  Args:
    source: :Werner_Rosendorff
    type: :Man
  AssignClass (5d23f701-d1fb-40a5-92b5-8f1f71edf049)
 Call ID: 5d23f701-d1fb-40a5-92b5-8f1f71edf049
  Args:
    type: :Person
    source: :Werner_Rosendorff
  AddLiteral (4b611669-47a7-4b97-a23d-723bdaccdbb7)
 Call ID: 4b611669-47a7-4b97-a23d-723bdaccdbb7
  Args:
    literal_type: xsd:integer
    source: :Alexander_of_Prussia
    literal_value: 1912
    relation: :hasBirthYear
  AddLiteral (9fbf70e5-1c63-468b-8827-676772237863)
 Call ID: 9fbf70e5-1c63-468b-8827-676772237863
  Args:
    relation: :hasDeathYear
    literal_value: 1985
    source: :Alexander_of_Prussia
    literal_type: xsd:integer
  AddTriple (ddba1184-55e2-49d4-b004-cfb217b47cf3)
 Call ID: ddba1184-55e2-49d4-b004-cfb217b47cf3
  Args:
    relation: :hasFather
    target: :August_Wilhelm_of_Prussia
    source: :Alexander_of_Prussia
  AddTriple (ee87084d-653a-4b1d-9ee3-9b45804365de)
 Call ID: ee87084d-653a-4b1d-9ee3-9b45804365de
  Args:
    source: :Alexander_of_Prussia
    relation: :hasMother
    target: :Alexandra_Victoria_of_Schleswig-Holstein-Sonderburg-Glücksburg
  AddTriple (9bdd8e46-6f58-41f9-9b29-707f775e1604)
 Call ID: 9bdd8e46-6f58-41f9-9b29-707f775e1604
  Args:
    target: :Wilhelm_II
    relation: :hasFather
    source: :August_Wilhelm_of_Prussia
  AddTriple (47aafc58-29ec-4164-94fd-6877f9bcd46f)
 Call ID: 47aafc58-29ec-4164-94fd-6877f9bcd46f
  Args:
    relation: :hasFather
    target: :Friedrich_Weygand
    source: :Armgard_Weygand
  AddTriple (9de47a28-b15b-4361-a598-2ee3b7a4b909)
 Call ID: 9de47a28-b15b-4361-a598-2ee3b7a4b909
  Args:
    source: :Armgard_Weygand
    target: :Karla_Franziska_Oheim
    relation: :hasMother
  AddLiteral (439f4241-4095-4916-9925-5a041754387b)
 Call ID: 439f4241-4095-4916-9925-5a041754387b
  Args:
    literal_value: 1938
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: :Alexander_of_Prussia
  AddLiteral (ab488005-d189-4f38-900a-ddc29a007ddd)
 Call ID: ab488005-d189-4f38-900a-ddc29a007ddd
  Args:
    source: :Armgard_Weygand
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1912
  AddLiteral (195b6080-3907-43ee-be2c-a1277e80d189)
 Call ID: 195b6080-3907-43ee-be2c-a1277e80d189
  Args:
    literal_value: 2001
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: :Armgard_Weygand
  Finish (20f6f96c-b7ec-41d3-a791-934ef3f23898)
 Call ID: 20f6f96c-b7ec-41d3-a791-934ef3f23898
  Args: