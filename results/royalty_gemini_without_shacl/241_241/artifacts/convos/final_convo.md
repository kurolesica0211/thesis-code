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
Princess Marie Alexandra of Baden (Marie Alexandra Thyra Victoria Louise Carola Hilda; 1 August 1902 – 29 January 1944) was a Hessian princess by marriage.
Family

She was the only daughter and elder child of Prince Maximilian of Baden (1867–1929) and Princess Marie Louise of Hanover and Cumberland.
Her paternal grandparents were Prince Wilhelm of Baden (1829–97) and Princess Maria Maximilianovna of Leuchtenberg (1841–1914), a daughter of Maximilian, Duke of Leuchtenberg (1817–52) and Grand Duchess Maria Nikolaevna (1819–1876).
Princess Marie-Louise of Hanover (1879–1948) was a daughter of Ernest Augustus, Crown Prince of Hanover, claimant of the annexed Kingdom of Hanover.
Marriage

On 17 September 1924, she married her fourth cousin Prince Wolfgang of Hesse (1896–1989).
Death

Princess Marie Alexandra was killed in an attack by the U.S. Army Air Forces during an air-raid on Frankfurt am Main on 29–30 January 1944 during World War II.
She and seven other women, who were aid workers, were killed when the cellar, in which they had taken refuge, collapsed under the weight of the building, rendering Marie Alexandra's body barely recognisable.



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
  AssignClass (59853b74-22b5-47f1-ab66-59c0705f23ec)
 Call ID: 59853b74-22b5-47f1-ab66-59c0705f23ec
  Args:
    type: :Woman
    source: Princess_Marie_Alexandra_of_Baden
  AssignClass (fa9c7ae5-55b8-492a-a0a4-716210c0e7e3)
 Call ID: fa9c7ae5-55b8-492a-a0a4-716210c0e7e3
  Args:
    type: :Person
    source: Princess_Marie_Alexandra_of_Baden
  AddLiteral (7e94d324-aab5-42dd-a493-baf09d04d108)
 Call ID: 7e94d324-aab5-42dd-a493-baf09d04d108
  Args:
    literal_type: xsd:integer
    source: Princess_Marie_Alexandra_of_Baden
    relation: :hasBirthYear
    literal_value: 1902
  AddLiteral (c8aa423b-fbe3-43ad-a7fb-ff98647bc139)
 Call ID: c8aa423b-fbe3-43ad-a7fb-ff98647bc139
  Args:
    literal_type: xsd:integer
    literal_value: 1944
    source: Princess_Marie_Alexandra_of_Baden
    relation: :hasDeathYear
  AssignClass (831b5f21-867a-4324-ba34-361c4b7e9fbe)
 Call ID: 831b5f21-867a-4324-ba34-361c4b7e9fbe
  Args:
    type: :Man
    source: Prince_Maximilian_of_Baden
  AssignClass (e9996267-d852-4b7c-8101-efe12dcd9889)
 Call ID: e9996267-d852-4b7c-8101-efe12dcd9889
  Args:
    type: :Person
    source: Prince_Maximilian_of_Baden
  AssignClass (68e058d4-e90b-47bc-86cf-42a1aef8f716)
 Call ID: 68e058d4-e90b-47bc-86cf-42a1aef8f716
  Args:
    type: :Ancestor
    source: Prince_Maximilian_of_Baden
  AddLiteral (e1f086ea-65bf-461e-9cd4-2236358d7c2f)
 Call ID: e1f086ea-65bf-461e-9cd4-2236358d7c2f
  Args:
    literal_type: xsd:integer
    literal_value: 1867
    relation: :hasBirthYear
    source: Prince_Maximilian_of_Baden
  AddLiteral (076e691c-1e8d-4b44-acbc-58d701b26692)
 Call ID: 076e691c-1e8d-4b44-acbc-58d701b26692
  Args:
    source: Prince_Maximilian_of_Baden
    relation: :hasDeathYear
    literal_value: 1929
    literal_type: xsd:integer
  AssignClass (1d2af75a-e7c4-494d-beb7-561c4d3dcf4a)
 Call ID: 1d2af75a-e7c4-494d-beb7-561c4d3dcf4a
  Args:
    type: :Woman
    source: Princess_Marie_Louise_of_Hanover_and_Cumberland
  AssignClass (c630824d-b693-44dc-82a0-0fb96a09538e)
 Call ID: c630824d-b693-44dc-82a0-0fb96a09538e
  Args:
    type: :Person
    source: Princess_Marie_Louise_of_Hanover_and_Cumberland
  AssignClass (12edb0e4-b055-4535-8e8a-a8847e30662e)
 Call ID: 12edb0e4-b055-4535-8e8a-a8847e30662e
  Args:
    type: :Ancestor
    source: Princess_Marie_Louise_of_Hanover_and_Cumberland
  AddTriple (ef50238b-6c8b-41b4-ba3a-352238b7b1ab)
 Call ID: ef50238b-6c8b-41b4-ba3a-352238b7b1ab
  Args:
    source: Princess_Marie_Alexandra_of_Baden
    relation: :hasFather
    target: Prince_Maximilian_of_Baden
  AddTriple (50322f19-de02-4800-a398-d9d76ec3db96)
 Call ID: 50322f19-de02-4800-a398-d9d76ec3db96
  Args:
    target: Princess_Marie_Louise_of_Hanover_and_Cumberland
    source: Princess_Marie_Alexandra_of_Baden
    relation: :hasMother
  AssignClass (aae44665-dd9d-4591-8efc-81ca6b093fce)
 Call ID: aae44665-dd9d-4591-8efc-81ca6b093fce
  Args:
    type: :Man
    source: Prince_Wilhelm_of_Baden
  AssignClass (9f52b4e1-0a64-443e-90ed-0ac8ae30bf7e)
 Call ID: 9f52b4e1-0a64-443e-90ed-0ac8ae30bf7e
  Args:
    type: :Person
    source: Prince_Wilhelm_of_Baden
  AssignClass (975e2537-9332-4e3d-b3ac-9a7ba2db3ca4)
 Call ID: 975e2537-9332-4e3d-b3ac-9a7ba2db3ca4
  Args:
    type: :Ancestor
    source: Prince_Wilhelm_of_Baden
  AddLiteral (126e1f78-155c-484c-b4d9-9283f70b80c1)
 Call ID: 126e1f78-155c-484c-b4d9-9283f70b80c1
  Args:
    source: Prince_Wilhelm_of_Baden
    relation: :hasBirthYear
    literal_value: 1829
    literal_type: xsd:integer
  AddLiteral (f1ed103d-3bfe-4368-9c37-28e3cba0349c)
 Call ID: f1ed103d-3bfe-4368-9c37-28e3cba0349c
  Args:
    literal_type: xsd:integer
    literal_value: 1897
    relation: :hasDeathYear
    source: Prince_Wilhelm_of_Baden
  AssignClass (25625fcf-3ff0-456a-9d49-d11b31e252a3)
 Call ID: 25625fcf-3ff0-456a-9d49-d11b31e252a3
  Args:
    type: :Woman
    source: Princess_Maria_Maximilianovna_of_Leuchtenberg
  AssignClass (a31765be-baba-4c76-a98d-2af4b8413895)
 Call ID: a31765be-baba-4c76-a98d-2af4b8413895
  Args:
    type: :Person
    source: Princess_Maria_Maximilianovna_of_Leuchtenberg
  AssignClass (5cbe9da5-939f-4c7f-bb8e-a2508ba1bdad)
 Call ID: 5cbe9da5-939f-4c7f-bb8e-a2508ba1bdad
  Args:
    type: :Ancestor
    source: Princess_Maria_Maximilianovna_of_Leuchtenberg
  AddLiteral (c5d018f7-1569-4b5e-9455-38df23404b84)
 Call ID: c5d018f7-1569-4b5e-9455-38df23404b84
  Args:
    relation: :hasBirthYear
    source: Princess_Maria_Maximilianovna_of_Leuchtenberg
    literal_value: 1841
    literal_type: xsd:integer
  AddLiteral (5d5f4046-f529-4dd2-96bc-0fbddff3dd2f)
 Call ID: 5d5f4046-f529-4dd2-96bc-0fbddff3dd2f
  Args:
    literal_type: xsd:integer
    source: Princess_Maria_Maximilianovna_of_Leuchtenberg
    relation: :hasDeathYear
    literal_value: 1914
  AddTriple (de638d88-c119-4af3-b2c0-7a826bd34da9)
 Call ID: de638d88-c119-4af3-b2c0-7a826bd34da9
  Args:
    target: Prince_Wilhelm_of_Baden
    source: Prince_Maximilian_of_Baden
    relation: :hasFather
  AddTriple (292ae8ee-68cd-4a42-b53b-b1214f068502)
 Call ID: 292ae8ee-68cd-4a42-b53b-b1214f068502
  Args:
    target: Princess_Maria_Maximilianovna_of_Leuchtenberg
    source: Prince_Maximilian_of_Baden
    relation: :hasMother
  AssignClass (a0d64608-3df9-4881-b0e4-50d55e41f121)
 Call ID: a0d64608-3df9-4881-b0e4-50d55e41f121
  Args:
    type: :Man
    source: Maximilian_Duke_of_Leuchtenberg
  AssignClass (8998f200-26ee-4db4-b734-e0739dba6d23)
 Call ID: 8998f200-26ee-4db4-b734-e0739dba6d23
  Args:
    type: :Person
    source: Maximilian_Duke_of_Leuchtenberg
  AssignClass (be8d772d-b47b-4c96-9a88-71131762a66a)
 Call ID: be8d772d-b47b-4c96-9a88-71131762a66a
  Args:
    type: :Ancestor
    source: Maximilian_Duke_of_Leuchtenberg
  AddLiteral (6c5b0022-2aae-45e8-8a8c-d94d713fe262)
 Call ID: 6c5b0022-2aae-45e8-8a8c-d94d713fe262
  Args:
    literal_type: xsd:integer
    literal_value: 1817
    source: Maximilian_Duke_of_Leuchtenberg
    relation: :hasBirthYear
  AddLiteral (fcbc0a8c-0cda-47de-b457-64ac03baef48)
 Call ID: fcbc0a8c-0cda-47de-b457-64ac03baef48
  Args:
    source: Maximilian_Duke_of_Leuchtenberg
    relation: :hasDeathYear
    literal_value: 1852
    literal_type: xsd:integer
  AssignClass (cee35ba1-ccfc-4b99-a73f-71262b242f7e)
 Call ID: cee35ba1-ccfc-4b99-a73f-71262b242f7e
  Args:
    type: :Woman
    source: Grand_Duchess_Maria_Nikolaevna
  AssignClass (ed433c49-712c-4b0b-ad58-a541f438bcf4)
 Call ID: ed433c49-712c-4b0b-ad58-a541f438bcf4
  Args:
    type: :Person
    source: Grand_Duchess_Maria_Nikolaevna
  AssignClass (e1dc22bf-e0ab-48b7-8e45-cc2f633ec3c8)
 Call ID: e1dc22bf-e0ab-48b7-8e45-cc2f633ec3c8
  Args:
    type: :Ancestor
    source: Grand_Duchess_Maria_Nikolaevna
  AddLiteral (fc6515ef-bf9d-458d-bbc0-9d526e05e706)
 Call ID: fc6515ef-bf9d-458d-bbc0-9d526e05e706
  Args:
    literal_type: xsd:integer
    source: Grand_Duchess_Maria_Nikolaevna
    relation: :hasBirthYear
    literal_value: 1819
  AddLiteral (2e838aaf-6800-4708-8d37-311f4223a76f)
 Call ID: 2e838aaf-6800-4708-8d37-311f4223a76f
  Args:
    literal_value: 1876
    relation: :hasDeathYear
    source: Grand_Duchess_Maria_Nikolaevna
    literal_type: xsd:integer
  AddTriple (2fb8da8e-f13d-44ca-9148-eba7a0eb8e5c)
 Call ID: 2fb8da8e-f13d-44ca-9148-eba7a0eb8e5c
  Args:
    target: Maximilian_Duke_of_Leuchtenberg
    relation: :hasFather
    source: Princess_Maria_Maximilianovna_of_Leuchtenberg
  AddTriple (49634b50-daa1-4ced-b02b-66b02959f5ed)
 Call ID: 49634b50-daa1-4ced-b02b-66b02959f5ed
  Args:
    target: Grand_Duchess_Maria_Nikolaevna
    relation: :hasMother
    source: Princess_Maria_Maximilianovna_of_Leuchtenberg
  AssignClass (be9177c8-b45e-4798-ba67-dae06fe18cd3)
 Call ID: be9177c8-b45e-4798-ba67-dae06fe18cd3
  Args:
    type: :Man
    source: Ernest_Augustus_Crown_Prince_of_Hanover
  AssignClass (c940a1f1-1ef3-43a1-922f-eafa7e3af06b)
 Call ID: c940a1f1-1ef3-43a1-922f-eafa7e3af06b
  Args:
    type: :Person
    source: Ernest_Augustus_Crown_Prince_of_Hanover
  AssignClass (c4f73e9c-fce4-4e00-b78b-fcc49fb57551)
 Call ID: c4f73e9c-fce4-4e00-b78b-fcc49fb57551
  Args:
    type: :Ancestor
    source: Ernest_Augustus_Crown_Prince_of_Hanover
  AddTriple (ede15e75-938e-4617-b553-eb0b3b6bfccf)
 Call ID: ede15e75-938e-4617-b553-eb0b3b6bfccf
  Args:
    target: Ernest_Augustus_Crown_Prince_of_Hanover
    source: Princess_Marie_Louise_of_Hanover_and_Cumberland
    relation: :hasFather
  AssignClass (cb544f7d-cbe7-4c22-84bf-3b9f6499e19c)
 Call ID: cb544f7d-cbe7-4c22-84bf-3b9f6499e19c
  Args:
    type: :Man
    source: Prince_Wolfgang_of_Hesse
  AssignClass (1e54df71-b263-4d04-b843-794c472286db)
 Call ID: 1e54df71-b263-4d04-b843-794c472286db
  Args:
    type: :Person
    source: Prince_Wolfgang_of_Hesse
  AddLiteral (99bb84d5-d1f8-498f-a60b-e1e75c7f45d5)
 Call ID: 99bb84d5-d1f8-498f-a60b-e1e75c7f45d5
  Args:
    literal_type: xsd:integer
    literal_value: 1896
    source: Prince_Wolfgang_of_Hesse
    relation: :hasBirthYear
  AddLiteral (259edf12-e535-43f5-9000-8fe1a6c49915)
 Call ID: 259edf12-e535-43f5-9000-8fe1a6c49915
  Args:
    relation: :hasDeathYear
    source: Prince_Wolfgang_of_Hesse
    literal_value: 1989
    literal_type: xsd:integer
  AddLiteral (a785f9a1-d51a-4f17-a96f-6ec2daa2c020)
 Call ID: a785f9a1-d51a-4f17-a96f-6ec2daa2c020
  Args:
    literal_value: 1924
    relation: :hasMarriageYear
    source: Princess_Marie_Alexandra_of_Baden
    literal_type: xsd:integer
  AddTriple (811742d7-6715-4635-9c22-e0b84c5fcc7e)
 Call ID: 811742d7-6715-4635-9c22-e0b84c5fcc7e
  Args:
    source: Princess_Marie_Alexandra_of_Baden
    relation: :hasRelation
    target: Prince_Wolfgang_of_Hesse
  Finish (65f6c227-1c07-47e5-868a-2251870cdb7b)
 Call ID: 65f6c227-1c07-47e5-868a-2251870cdb7b
  Args: