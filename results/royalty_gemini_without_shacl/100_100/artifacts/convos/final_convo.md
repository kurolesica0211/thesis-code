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
The Crown PrinceThe Crown Princess


Princess Tomislav


Princess Alexander


Princess Elizabeth


Prince Dimitri Nicholas Paul George Maria of Yugoslavia (born 18 June 1958), also known as Dimitri Karageorgevich or Dimitrije Karađorđević, is a gemologist and member of the Royal House of Yugoslavia.
He founded the jewellery firm bearing his name, Prince Dimitri Company, and continues to serve as its president and creative director.
Life and career

Born in Boulogne-Billancourt, France, Prince Dimitri was raised in Versailles, attending boarding schools in France and Switzerland.
Prince Dimitri began designing jewellery in 1999, with a collection of gemstone cufflinks that was sold at Bergdorf Goodman and Saks Fifth Avenue.
In 2007, he and business partner Todd Morley founded the Prince Dimitri Company, which opened a salon in Manhattan.
Family

Prince Dimitri and Prince Michael of Yugoslavia are the first set of twins born to Prince Alexander of Yugoslavia and his first wife, Princess Maria Pia of Savoy, the eldest daughter of Umberto II of Italy in 1958.
Maria Pia had a second set of twins, Prince Serge and Princess Helene of Yugoslavia in 1963.
They have a younger half-brother, Prince Dushan of Yugoslavia, from their father's second marriage to Princess Barbara of Liechtenstein.
Prince Dimitri belongs to the cadet branch of the Royal House of Yugoslavia, descending from Prince Regent Paul of Yugoslavia.
He is a third cousin of Alexander, Crown Prince of Yugoslavia.
Honours

Ancestry

Dimitri is a member of the House of Karađorđević cadet branch.
He is a great-great-grandson of Prince Alexander of Serbia (reigned 1842–1858).
Through his father, Dimitri descends from kings George I of Greece and Christian IX of Denmark, as well as emperor Alexander II of Russia.
Through his mother, Dimitri descends from kings Umberto II of Italy, Albert I of Belgium, and furthermore from Nicholas I of Montenegro and Miguel I of Portugal.



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
  AssignClass (f8df7741-509d-47f8-bde0-dd4b54de3451)
 Call ID: f8df7741-509d-47f8-bde0-dd4b54de3451
  Args:
    source: PrinceDimitriOfYugoslavia
    type: :Man
  AssignClass (433e2b09-25fa-4f4f-be48-e767c4c8b1a9)
 Call ID: 433e2b09-25fa-4f4f-be48-e767c4c8b1a9
  Args:
    type: :Person
    source: PrinceDimitriOfYugoslavia
  AssignClass (c76f3d15-6dd4-4080-8997-09f632520587)
 Call ID: c76f3d15-6dd4-4080-8997-09f632520587
  Args:
    type: :Man
    source: PrinceMichaelOfYugoslavia
  AssignClass (9540fecf-8efc-4312-a225-4a64c096f2e4)
 Call ID: 9540fecf-8efc-4312-a225-4a64c096f2e4
  Args:
    type: :Person
    source: PrinceMichaelOfYugoslavia
  AssignClass (a10a6b8a-5465-4644-b9da-90c04260bd41)
 Call ID: a10a6b8a-5465-4644-b9da-90c04260bd41
  Args:
    type: :Man
    source: PrinceAlexanderOfYugoslavia
  AssignClass (4dcd7f36-74da-4b19-b471-228077fb2028)
 Call ID: 4dcd7f36-74da-4b19-b471-228077fb2028
  Args:
    type: :Person
    source: PrinceAlexanderOfYugoslavia
  AssignClass (50c441d5-b2bf-4722-81ad-b07eb49c3012)
 Call ID: 50c441d5-b2bf-4722-81ad-b07eb49c3012
  Args:
    type: :Woman
    source: PrincessMariaPiaOfSavoy
  AssignClass (9811f952-ae59-4090-b826-e388f2132f9f)
 Call ID: 9811f952-ae59-4090-b826-e388f2132f9f
  Args:
    source: PrincessMariaPiaOfSavoy
    type: :Person
  AssignClass (ada64cc7-c3b2-4c77-a39e-f1e81ab02579)
 Call ID: ada64cc7-c3b2-4c77-a39e-f1e81ab02579
  Args:
    type: :Man
    source: PrinceSergeOfYugoslavia
  AssignClass (cce7feee-9701-425f-810f-af4f655c14fb)
 Call ID: cce7feee-9701-425f-810f-af4f655c14fb
  Args:
    source: PrinceSergeOfYugoslavia
    type: :Person
  AssignClass (33e9a80d-c6d5-4320-a3d6-9d490a792499)
 Call ID: 33e9a80d-c6d5-4320-a3d6-9d490a792499
  Args:
    type: :Woman
    source: PrincessHeleneOfYugoslavia
  AssignClass (ba0f0506-8b40-42ec-b44c-d80f91d6500e)
 Call ID: ba0f0506-8b40-42ec-b44c-d80f91d6500e
  Args:
    source: PrincessHeleneOfYugoslavia
    type: :Person
  AssignClass (e8460d2c-9a84-44e4-a491-1080742542f8)
 Call ID: e8460d2c-9a84-44e4-a491-1080742542f8
  Args:
    type: :Man
    source: PrinceDushanOfYugoslavia
  AssignClass (4b39fb84-48b9-4718-b98d-ee3687765a44)
 Call ID: 4b39fb84-48b9-4718-b98d-ee3687765a44
  Args:
    type: :Person
    source: PrinceDushanOfYugoslavia
  AssignClass (4c8a9457-a0af-4b5b-a402-cdf6ad7a545f)
 Call ID: 4c8a9457-a0af-4b5b-a402-cdf6ad7a545f
  Args:
    type: :Woman
    source: PrincessBarbaraOfLiechtenstein
  AssignClass (86ea3e0e-a2a6-4c38-ba95-98e2b8a425e1)
 Call ID: 86ea3e0e-a2a6-4c38-ba95-98e2b8a425e1
  Args:
    source: PrincessBarbaraOfLiechtenstein
    type: :Person
  AddLiteral (50f8ed19-2966-4c85-881c-17d4697fbb75)
 Call ID: 50f8ed19-2966-4c85-881c-17d4697fbb75
  Args:
    literal_value: 1958
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: PrinceDimitriOfYugoslavia
  AddLiteral (69b1076f-ebc3-4a6a-828b-6e858709c818)
 Call ID: 69b1076f-ebc3-4a6a-828b-6e858709c818
  Args:
    literal_value: Dimitri Karageorgevich
    literal_type: xsd:string
    relation: :alsoKnownAs
    source: PrinceDimitriOfYugoslavia
  AddLiteral (e646dd78-990d-42a3-9b27-c99f5b7a5ab6)
 Call ID: e646dd78-990d-42a3-9b27-c99f5b7a5ab6
  Args:
    source: PrinceDimitriOfYugoslavia
    literal_type: xsd:string
    literal_value: Dimitrije Karađorđević
    relation: :alsoKnownAs
  AddTriple (bdf9407d-6891-4f4a-9124-9277c0dcca66)
 Call ID: bdf9407d-6891-4f4a-9124-9277c0dcca66
  Args:
    relation: :isSonOf
    target: PrinceAlexanderOfYugoslavia
    source: PrinceDimitriOfYugoslavia
  AddTriple (59ab8ae4-e758-4c58-b64b-497b5d50d2ec)
 Call ID: 59ab8ae4-e758-4c58-b64b-497b5d50d2ec
  Args:
    source: PrinceDimitriOfYugoslavia
    target: PrincessMariaPiaOfSavoy
    relation: :isSonOf
  AddTriple (dcba6400-658a-4483-b55c-df201e7a5478)
 Call ID: dcba6400-658a-4483-b55c-df201e7a5478
  Args:
    relation: :isSonOf
    source: PrinceMichaelOfYugoslavia
    target: PrinceAlexanderOfYugoslavia
  AddTriple (2b81c83d-1321-4435-9f96-39619dd2a73a)
 Call ID: 2b81c83d-1321-4435-9f96-39619dd2a73a
  Args:
    relation: :isSonOf
    target: PrincessMariaPiaOfSavoy
    source: PrinceMichaelOfYugoslavia
  AddTriple (d7313f09-e0f6-4f2e-9ec1-779925b61b90)
 Call ID: d7313f09-e0f6-4f2e-9ec1-779925b61b90
  Args:
    target: PrinceMichaelOfYugoslavia
    source: PrinceDimitriOfYugoslavia
    relation: :isSiblingOf
  AddTriple (9afe8be3-6149-4426-881a-cad30003f42a)
 Call ID: 9afe8be3-6149-4426-881a-cad30003f42a
  Args:
    target: PrincessMariaPiaOfSavoy
    source: PrinceSergeOfYugoslavia
    relation: :isSonOf
  AddTriple (231bcd27-73ef-4b51-a437-7a77803e7475)
 Call ID: 231bcd27-73ef-4b51-a437-7a77803e7475
  Args:
    target: PrincessMariaPiaOfSavoy
    source: PrincessHeleneOfYugoslavia
    relation: :isDaughterOf
  AddTriple (bb8c5718-e418-437c-b2c2-a02ca3299572)
 Call ID: bb8c5718-e418-437c-b2c2-a02ca3299572
  Args:
    target: PrincessHeleneOfYugoslavia
    source: PrinceSergeOfYugoslavia
    relation: :isSiblingOf
  AddTriple (da396e64-6b0d-46ee-bf11-d51bfe00d489)
 Call ID: da396e64-6b0d-46ee-bf11-d51bfe00d489
  Args:
    target: PrinceAlexanderOfYugoslavia
    source: PrinceDushanOfYugoslavia
    relation: :isSonOf
  AddTriple (c0159400-4b89-4332-92aa-5fa45e32c6bf)
 Call ID: c0159400-4b89-4332-92aa-5fa45e32c6bf
  Args:
    relation: :isSonOf
    target: PrincessBarbaraOfLiechtenstein
    source: PrinceDushanOfYugoslavia
  Finish (12dc4b5d-467d-41ff-92bc-5123e90051ce)
 Call ID: 12dc4b5d-467d-41ff-92bc-5123e90051ce
  Args: