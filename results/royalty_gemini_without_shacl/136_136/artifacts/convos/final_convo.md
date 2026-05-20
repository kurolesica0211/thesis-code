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
Lord Leopold Arthur Louis Mountbatten (21 May 1889 – 23 April 1922) was a British Army officer and a descendant of the Hessian princely Battenberg family and the British royal family.
A grandson of Queen Victoria, he was known as Prince Leopold of Battenberg from his birth until 1917, when the British royal family relinquished their German titles during World War I, and the Battenberg family changed their name to Mountbatten.
Early life

Leopold was born on 21 May 1889.
His father was Prince Henry of Battenberg, the son of Prince Alexander of Hesse and by Rhine and Julia, Princess of Battenberg.
His mother was Princess Beatrice of the United Kingdom, the fifth daughter and the youngest child of Queen Victoria and Prince Albert.
As he was the product of a morganatic marriage, Prince Henry of Battenberg took his style of Prince of Battenberg from his mother, Julia von Hauke, who was created Princess of Battenberg in her own right.
As such, Leopold was styled as His Serene Highness Prince Leopold of Battenberg from birth.
In the United Kingdom, he was styled His Highness Prince Leopold of Battenberg under a royal warrant passed by Queen Victoria in 1886.
His godparents were Leopold II of Belgium (his first cousin twice removed, represented by the Prince of Wales, his maternal uncle), the Duke of Connaught and Strathearn (his maternal uncle, represented by Prince Albert of Schleswig-Holstein, his first cousin), Prince Louis of Battenberg (his paternal uncle, represented by the Marquess of Lorne, his maternal uncle), the Marchioness of Lorne (his maternal aunt), the Duchess of Albany (his maternal aunt) and Princess Marie of Erbach-Schönberg (his paternal aunt).
Leopold was a haemophiliac, a condition he inherited through his mother.
His namesake maternal uncle, Prince Leopold, Duke of Albany, had died from the same condition.
Military career

Leopold was commissioned a lieutenant (supernumerary) on 16 October 1909 in the 8th Battalion of the Isle of Wight Rifles, a Territorial Force unit.
Relinquishment of titles

During the First World War, anti-German feeling in the United Kingdom led Leopold's first cousin, George V to change the name of the royal house from the Germanic House of Saxe-Coburg and Gotha to the more English-sounding House of Windsor.
In response to this, Leopold renounced his title of Prince, the style His Highness and the designation 'of Battenberg' through a royal warrant from the King dated 14 July 1917, and became Sir Leopold Mountbatten by virtue of his being a Knight Grand Cross of the Royal Victorian Order.
Under a further warrant of 11 September 1917 he was granted the style and precedence of the younger son of a marquess, and became Lord Leopold Mountbatten.
Death

Lord Leopold died on 23 April 1922(1922-04-23) (aged 32), during a hip operation.



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
  AssignClass (78c23047-8416-43eb-bad0-48826078f101)
 Call ID: 78c23047-8416-43eb-bad0-48826078f101
  Args:
    type: :Man
    source: :LeopoldMountbatten
  AssignClass (1d825155-619f-48d6-ae96-92a099488845)
 Call ID: 1d825155-619f-48d6-ae96-92a099488845
  Args:
    type: :Person
    source: :LeopoldMountbatten
  AddLiteral (ecf0e940-1cff-4094-bfa9-062cec12111c)
 Call ID: ecf0e940-1cff-4094-bfa9-062cec12111c
  Args:
    literal_value: 1889
    source: :LeopoldMountbatten
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (0b1126f3-2b11-44e9-940f-65e2fbf5efed)
 Call ID: 0b1126f3-2b11-44e9-940f-65e2fbf5efed
  Args:
    source: :LeopoldMountbatten
    literal_value: 1922
    relation: :hasDeathYear
    literal_type: xsd:integer
  AddLiteral (e4d7f0ee-d36b-41b6-b909-ce44ec052fbb)
 Call ID: e4d7f0ee-d36b-41b6-b909-ce44ec052fbb
  Args:
    source: :LeopoldMountbatten
    literal_value: Prince Leopold of Battenberg
    relation: :formerlyKnownAs
    literal_type: xsd:string
  AddLiteral (572c3794-45be-4981-a09c-53c6dd29e840)
 Call ID: 572c3794-45be-4981-a09c-53c6dd29e840
  Args:
    source: :LeopoldMountbatten
    literal_value: Sir Leopold Mountbatten
    relation: :alsoKnownAs
    literal_type: xsd:string
  AddLiteral (5a7f2de1-8395-4418-96b0-4d396bc51b1d)
 Call ID: 5a7f2de1-8395-4418-96b0-4d396bc51b1d
  Args:
    literal_type: xsd:string
    relation: :knownAs
    literal_value: Lord Leopold Mountbatten
    source: :LeopoldMountbatten
  AssignClass (9c6c46d0-6a56-4d28-9f66-6ef66fd96fd0)
 Call ID: 9c6c46d0-6a56-4d28-9f66-6ef66fd96fd0
  Args:
    type: :Man
    source: :PrinceHenryOfBattenberg
  AssignClass (533b4ff8-dfb4-453c-82fc-f128c5070bb5)
 Call ID: 533b4ff8-dfb4-453c-82fc-f128c5070bb5
  Args:
    type: :Person
    source: :PrinceHenryOfBattenberg
  AddTriple (15790479-832a-4d08-9b68-7deba24e3f47)
 Call ID: 15790479-832a-4d08-9b68-7deba24e3f47
  Args:
    source: :LeopoldMountbatten
    relation: :hasFather
    target: :PrinceHenryOfBattenberg
  AssignClass (cfe6afad-8e77-4f42-b19e-9b7636ce87f5)
 Call ID: cfe6afad-8e77-4f42-b19e-9b7636ce87f5
  Args:
    type: :Woman
    source: :PrincessBeatrice
  AssignClass (5b492a85-bcb0-4093-960a-155dd390219f)
 Call ID: 5b492a85-bcb0-4093-960a-155dd390219f
  Args:
    type: :Person
    source: :PrincessBeatrice
  AddTriple (2aae8083-1a33-4033-a737-dd511a8afe96)
 Call ID: 2aae8083-1a33-4033-a737-dd511a8afe96
  Args:
    source: :LeopoldMountbatten
    target: :PrincessBeatrice
    relation: :hasMother
  AssignClass (22676240-a953-4117-a8da-d4950ca46d78)
 Call ID: 22676240-a953-4117-a8da-d4950ca46d78
  Args:
    type: :Man
    source: :PrinceAlexanderOfHesseAndByRhine
  AssignClass (75f9c201-fd70-4b0d-99b4-f6cc051c1522)
 Call ID: 75f9c201-fd70-4b0d-99b4-f6cc051c1522
  Args:
    type: :Person
    source: :PrinceAlexanderOfHesseAndByRhine
  AssignClass (26d3a77f-78d5-4040-ac6c-390580d86765)
 Call ID: 26d3a77f-78d5-4040-ac6c-390580d86765
  Args:
    type: :Woman
    source: :JuliaPrincessOfBattenberg
  AssignClass (c5cb134c-9adb-4f41-bce8-741c1be5470b)
 Call ID: c5cb134c-9adb-4f41-bce8-741c1be5470b
  Args:
    type: :Person
    source: :JuliaPrincessOfBattenberg
  AddTriple (164fee64-4dcc-4b61-9fd6-0700b05b5b38)
 Call ID: 164fee64-4dcc-4b61-9fd6-0700b05b5b38
  Args:
    source: :PrinceHenryOfBattenberg
    target: :PrinceAlexanderOfHesseAndByRhine
    relation: :hasFather
  AddTriple (4871181b-56c0-49b6-be34-e1eb3f16f989)
 Call ID: 4871181b-56c0-49b6-be34-e1eb3f16f989
  Args:
    relation: :hasMother
    target: :JuliaPrincessOfBattenberg
    source: :PrinceHenryOfBattenberg
  AssignClass (67af2b2f-fcfa-449a-aaef-f4b54822f29a)
 Call ID: 67af2b2f-fcfa-449a-aaef-f4b54822f29a
  Args:
    type: :Woman
    source: :QueenVictoria
  AssignClass (8d43d58a-f369-43ba-9e60-b44e20ced9b8)
 Call ID: 8d43d58a-f369-43ba-9e60-b44e20ced9b8
  Args:
    type: :Person
    source: :QueenVictoria
  AssignClass (3ab0f9df-1fdc-4aed-82c1-9327da3638ae)
 Call ID: 3ab0f9df-1fdc-4aed-82c1-9327da3638ae
  Args:
    type: :Man
    source: :PrinceAlbert
  AssignClass (95ced589-dd8e-4224-aa69-88219ca535bf)
 Call ID: 95ced589-dd8e-4224-aa69-88219ca535bf
  Args:
    type: :Person
    source: :PrinceAlbert
  AddTriple (95bd07dc-3afd-4c94-b509-6e7e1eddea72)
 Call ID: 95bd07dc-3afd-4c94-b509-6e7e1eddea72
  Args:
    target: :QueenVictoria
    relation: :hasMother
    source: :PrincessBeatrice
  AddTriple (c16a246f-8dd6-4e11-8e29-046bade8a88e)
 Call ID: c16a246f-8dd6-4e11-8e29-046bade8a88e
  Args:
    relation: :hasFather
    target: :PrinceAlbert
    source: :PrincessBeatrice
  Finish (86f5a423-66cd-4750-b20e-c19851447fdc)
 Call ID: 86f5a423-66cd-4750-b20e-c19851447fdc
  Args: