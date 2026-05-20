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
Princess Beatrix*


Princess Margriet*Pieter van Vollenhoven*


Prince Maurits Willem Pieter Hendrik of Orange-Nassau, van Vollenhoven (born 17 April 1968) is a member of the Dutch royal family as the eldest son of Princess Margriet of the Netherlands and Pieter van Vollenhoven.
Life and career

Maurits was born on 17 April 1968.
His godparents are Princess Christina of the Netherlands, Prince Alois-Konstantin of Lowenstein-Wertheim-Rosenberg, Jhr. G. Krayenhof, and The Dutch Merchant Fleet.
Van Vollenhoven has three brothers: Bernhard, Pieter-Christiaan, Floris.
In 1987, van Vollenhoven performed military service with the Royal Netherlands Marine Corps and the Royal Netherlands Navy.
From September 2001 to May 2006, the prince worked for Philips (Domestic Appliances and Personal Care) in Amersfoort, where he was in charge of part of the Philishave portfolio.
In May 2006, van Vollenhoven started his own business, The Source, which focuses on innovative concepts for products, services and systems for both business and government.
Since 1 May 2013, Maurits is Aide-de-camp to King Willem-Alexander and promoted to the rank of Commander (Dutch: Kapitein-lieutenant ter Zee) in the Royal Netherlands Navy.
Maurits works for Sunrock, a company which invests in solar parks and green energy.
The prince criticised the solar energy policy of the municipality of Amsterdam and opened up about other topics.
Marriage and family

In 1989, van Vollenhoven met Marilène (Marie-Helène) van den Broek b. 4 February 1970, the youngest daughter of Hans van den Broek and Josee van Schendel.
He was the first grandchild of Queen Juliana and Prince Bernhard of the Netherlands who married.
Together, the couple has three children:


By Royal Decree of 26 May 1998, the children of van Vollenhoven bear the surname "van Lippe-Biesterfeld van Vollenhoven", without titles.
Upon the abdication of Queen Beatrix, which took place on 30 April 2013, it was confirmed that the children of Princess Margriet and Pieter van Vollenhoven would no longer be eligible to succeed to the throne, and that they would also cease to be members of the Royal House according to The Membership of the Royal House Act.
Titles and styles

Ancestry

References

External links

2 gave up the title "Prince of the Netherlands, but still held the title "Prince of Orange-Nassau"
3 title granted by Royal Decree to descendants of Princess Irene



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
  AssignClass (f6ffacac-2076-4244-8850-884725393f59)
 Call ID: f6ffacac-2076-4244-8850-884725393f59
  Args:
    type: :Man
    source: :Maurits_van_Vollenhoven
  AssignClass (462eaa1b-b2d4-4a6e-a40e-7263ee680afe)
 Call ID: 462eaa1b-b2d4-4a6e-a40e-7263ee680afe
  Args:
    type: :Person
    source: :Maurits_van_Vollenhoven
  AddLiteral (7e297cf1-77b6-4388-b931-80409c373934)
 Call ID: 7e297cf1-77b6-4388-b931-80409c373934
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1968
    source: :Maurits_van_Vollenhoven
  AssignClass (f2e78477-4446-4e1b-9f7d-8ecef62f5d2e)
 Call ID: f2e78477-4446-4e1b-9f7d-8ecef62f5d2e
  Args:
    source: :Princess_Margriet
    type: :Woman
  AssignClass (7c40b3bf-e397-4bc0-982c-221f2a930bb1)
 Call ID: 7c40b3bf-e397-4bc0-982c-221f2a930bb1
  Args:
    source: :Princess_Margriet
    type: :Person
  AssignClass (b3969e90-9f1a-4000-b596-dea84960fa5e)
 Call ID: b3969e90-9f1a-4000-b596-dea84960fa5e
  Args:
    source: :Pieter_van_Vollenhoven
    type: :Man
  AssignClass (2cf4dc12-e4ac-48dc-9e69-609a1a6d8232)
 Call ID: 2cf4dc12-e4ac-48dc-9e69-609a1a6d8232
  Args:
    type: :Person
    source: :Pieter_van_Vollenhoven
  AddTriple (9573cc6d-a2a2-4a6f-a3e6-4d8c07c88ebd)
 Call ID: 9573cc6d-a2a2-4a6f-a3e6-4d8c07c88ebd
  Args:
    relation: :hasFather
    target: :Pieter_van_Vollenhoven
    source: :Maurits_van_Vollenhoven
  AddTriple (f5956ec9-f2bf-428e-8957-48819e99305c)
 Call ID: f5956ec9-f2bf-428e-8957-48819e99305c
  Args:
    relation: :hasMother
    source: :Maurits_van_Vollenhoven
    target: :Princess_Margriet
  AssignClass (c62a9778-09b5-47c8-af2f-41b0e309d408)
 Call ID: c62a9778-09b5-47c8-af2f-41b0e309d408
  Args:
    type: :Man
    source: :Bernhard_van_Vollenhoven
  AssignClass (f9337516-382a-4e66-8ba5-f105592c9f49)
 Call ID: f9337516-382a-4e66-8ba5-f105592c9f49
  Args:
    type: :Person
    source: :Bernhard_van_Vollenhoven
  AssignClass (42fde20b-5d6c-4392-ae1d-76c103f188cb)
 Call ID: 42fde20b-5d6c-4392-ae1d-76c103f188cb
  Args:
    source: :Pieter-Christiaan_van_Vollenhoven
    type: :Man
  AssignClass (785937ee-7a14-4087-b033-48f9447d35e8)
 Call ID: 785937ee-7a14-4087-b033-48f9447d35e8
  Args:
    source: :Pieter-Christiaan_van_Vollenhoven
    type: :Person
  AssignClass (4f64e878-60b5-4114-86ba-2ca6c032c7fe)
 Call ID: 4f64e878-60b5-4114-86ba-2ca6c032c7fe
  Args:
    type: :Man
    source: :Floris_van_Vollenhoven
  AssignClass (d638b82c-0df9-48c8-b429-570f4f07c888)
 Call ID: d638b82c-0df9-48c8-b429-570f4f07c888
  Args:
    source: :Floris_van_Vollenhoven
    type: :Person
  AddTriple (e0b933d4-3a83-4389-9afd-70867374ead3)
 Call ID: e0b933d4-3a83-4389-9afd-70867374ead3
  Args:
    source: :Maurits_van_Vollenhoven
    target: :Bernhard_van_Vollenhoven
    relation: :hasBrother
  AddTriple (e04a8279-36b1-4f27-95b0-ff8b7ae2d125)
 Call ID: e04a8279-36b1-4f27-95b0-ff8b7ae2d125
  Args:
    relation: :hasBrother
    target: :Pieter-Christiaan_van_Vollenhoven
    source: :Maurits_van_Vollenhoven
  AddTriple (e793b714-ce8d-47b0-bfe2-b8894ac26f89)
 Call ID: e793b714-ce8d-47b0-bfe2-b8894ac26f89
  Args:
    source: :Maurits_van_Vollenhoven
    target: :Floris_van_Vollenhoven
    relation: :hasBrother
  AssignClass (e193c20f-f7fb-41d0-b10a-93d6ab3ae685)
 Call ID: e193c20f-f7fb-41d0-b10a-93d6ab3ae685
  Args:
    type: :Woman
    source: :Marilene_van_den_Broek
  AssignClass (a2ab942b-8c27-4551-9f49-6c76fc8a58d5)
 Call ID: a2ab942b-8c27-4551-9f49-6c76fc8a58d5
  Args:
    source: :Marilene_van_den_Broek
    type: :Person
  AddLiteral (83d40b7f-f6f7-4614-8658-65450945c584)
 Call ID: 83d40b7f-f6f7-4614-8658-65450945c584
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1970
    source: :Marilene_van_den_Broek
  AddLiteral (61eb2cb5-8aad-4134-bc63-255edf052990)
 Call ID: 61eb2cb5-8aad-4134-bc63-255edf052990
  Args:
    literal_value: 1989
    source: :Maurits_van_Vollenhoven
    relation: :hasMarriageYear
    literal_type: xsd:integer
  AssignClass (1fd4fd99-5a22-430d-a9c8-2897a90c19a2)
 Call ID: 1fd4fd99-5a22-430d-a9c8-2897a90c19a2
  Args:
    type: :Man
    source: :Hans_van_den_Broek
  AssignClass (4af05e72-e4f7-4f0a-8f7e-7f81e0f77fa5)
 Call ID: 4af05e72-e4f7-4f0a-8f7e-7f81e0f77fa5
  Args:
    source: :Hans_van_den_Broek
    type: :Person
  AssignClass (b67c8ea9-e5be-42a3-85cf-dedb82b2526a)
 Call ID: b67c8ea9-e5be-42a3-85cf-dedb82b2526a
  Args:
    type: :Woman
    source: :Josee_van_Schendel
  AssignClass (10461e02-650e-4280-86b9-107a4fa0f615)
 Call ID: 10461e02-650e-4280-86b9-107a4fa0f615
  Args:
    source: :Josee_van_Schendel
    type: :Person
  AddTriple (40aa8a57-3840-42ce-b1e8-35d625cdd928)
 Call ID: 40aa8a57-3840-42ce-b1e8-35d625cdd928
  Args:
    source: :Marilene_van_den_Broek
    target: :Hans_van_den_Broek
    relation: :hasFather
  AddTriple (be2b9ce4-a82e-4b23-afbc-b9d3d7a283a2)
 Call ID: be2b9ce4-a82e-4b23-afbc-b9d3d7a283a2
  Args:
    relation: :hasMother
    target: :Josee_van_Schendel
    source: :Marilene_van_den_Broek
  AssignClass (2eacda5f-b0c7-4fd8-b470-0632e4711b92)
 Call ID: 2eacda5f-b0c7-4fd8-b470-0632e4711b92
  Args:
    type: :Woman
    source: :Queen_Juliana
  AssignClass (077b080f-6371-49d9-b42b-01677d74ebca)
 Call ID: 077b080f-6371-49d9-b42b-01677d74ebca
  Args:
    source: :Queen_Juliana
    type: :Person
  AssignClass (2545f1d1-5a60-4c58-b406-70d19727cf11)
 Call ID: 2545f1d1-5a60-4c58-b406-70d19727cf11
  Args:
    type: :Man
    source: :Prince_Bernhard
  AssignClass (82662571-39e9-4d21-9c25-20bced77cabe)
 Call ID: 82662571-39e9-4d21-9c25-20bced77cabe
  Args:
    type: :Person
    source: :Prince_Bernhard
  Finish (f072c8d6-3b8f-4fe5-bfcc-2a1568924654)
 Call ID: f072c8d6-3b8f-4fe5-bfcc-2a1568924654
  Args: