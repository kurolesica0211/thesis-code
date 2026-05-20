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
Fergus Bowes-Lyon (18 April 1889 – 27 September 1915) was a British officer and older brother of Elizabeth Bowes-Lyon, who later became the queen consort of King George VI.
He was a maternal uncle of Queen Elizabeth II.
Early life and marriage

Fergus Bowes-Lyon was born at Forbes House in Ham, Surrey, the son of Claude Bowes-Lyon, 14th
Bowes-Lyon had his early education at Ludgrove School.
On 17 September 1914, Bowes-Lyon married Lady Christian Norah Dawson-Damer (7 August 1890 – 29 March 1959), daughter of the 5th Earl of Portarlington.
Rosemary was only two months old when Fergus died in the line of duty on 27 September 1915, only 10 days after the first anniversary of his wedding.
His issue:


World War I

In the First World War, Bowes-Lyon served with the 8th Battalion, Black Watch: as a lieutenant since 19 August 1914, and as temporary captain since 17 November.
Bowes-Lyon was killed in action on 27 September 1915, during the Battle of the Hohenzollern Redoubt in the Battle of Loos.
At the time of Bowes-Lyon's death, his brother John was also serving with the Black Watch.
His mother, Cecilia Bowes-Lyon, Countess of Strathmore and Kinghorne, was severely affected by the loss of her son, and after his death became an invalid, withdrawn from public life until the marriage of her daughter Elizabeth to the future king George VI in 1923.
Fergus's widow later married Captain William Frederick Martin (d. 6 October 1947).
In November 2011, Bowes-Lyon's grandson supplied family records to the Commonwealth War Graves Commission detailing his original burial place, and showing that it had remained marked until the end of the war.



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
  AssignClass (8aa48506-bc12-447e-ab2a-dae5098babd2)
 Call ID: 8aa48506-bc12-447e-ab2a-dae5098babd2
  Args:
    source: Fergus Bowes-Lyon
    type: :Man
  AssignClass (8facc506-4384-4bae-8976-3a693ba7173d)
 Call ID: 8facc506-4384-4bae-8976-3a693ba7173d
  Args:
    source: Fergus Bowes-Lyon
    type: :Person
  AddLiteral (922a8c87-e2f4-4704-8482-18723e978f45)
 Call ID: 922a8c87-e2f4-4704-8482-18723e978f45
  Args:
    literal_type: xsd:string
    source: Fergus Bowes-Lyon
    relation: :hasBirthYear
    literal_value: 1889
  AddLiteral (a12f2527-d60a-419d-acfe-fd517bbdcb1d)
 Call ID: a12f2527-d60a-419d-acfe-fd517bbdcb1d
  Args:
    literal_value: 1915
    literal_type: xsd:string
    source: Fergus Bowes-Lyon
    relation: :hasDeathYear
  AssignClass (e78cf00a-2298-4db6-8865-f169452e8981)
 Call ID: e78cf00a-2298-4db6-8865-f169452e8981
  Args:
    source: Elizabeth Bowes-Lyon
    type: :Woman
  AssignClass (c156384c-4ffb-4cda-ba2f-8da94a1ba307)
 Call ID: c156384c-4ffb-4cda-ba2f-8da94a1ba307
  Args:
    type: :Person
    source: Elizabeth Bowes-Lyon
  AddTriple (49aa851b-db63-409f-b0e3-3f209a9a697a)
 Call ID: 49aa851b-db63-409f-b0e3-3f209a9a697a
  Args:
    target: Elizabeth Bowes-Lyon
    relation: :isBrotherOf
    source: Fergus Bowes-Lyon
  AssignClass (96b6ea7b-c634-4326-a4a4-f8140a0bc970)
 Call ID: 96b6ea7b-c634-4326-a4a4-f8140a0bc970
  Args:
    source: Queen Elizabeth II
    type: :Woman
  AssignClass (acc4b2b4-97e3-4a53-83b7-0ddb7ef6eee7)
 Call ID: acc4b2b4-97e3-4a53-83b7-0ddb7ef6eee7
  Args:
    source: Queen Elizabeth II
    type: :Person
  AddTriple (2f61040d-f3e9-40e8-9097-aba37d6565ce)
 Call ID: 2f61040d-f3e9-40e8-9097-aba37d6565ce
  Args:
    source: Fergus Bowes-Lyon
    relation: :isUncleOf
    target: Queen Elizabeth II
  AssignClass (e14a256f-48c5-49ee-b6dd-7549c4c0ca0d)
 Call ID: e14a256f-48c5-49ee-b6dd-7549c4c0ca0d
  Args:
    type: :Man
    source: Claude Bowes-Lyon
  AssignClass (262049a6-4bf9-4768-879e-b8d5185ad0c6)
 Call ID: 262049a6-4bf9-4768-879e-b8d5185ad0c6
  Args:
    source: Claude Bowes-Lyon
    type: :Person
  AddTriple (a831fc60-0b21-4a41-938f-ecd6c9aae1fd)
 Call ID: a831fc60-0b21-4a41-938f-ecd6c9aae1fd
  Args:
    target: Claude Bowes-Lyon
    source: Fergus Bowes-Lyon
    relation: :hasFather
  AssignClass (549bbc9c-36de-4cf2-b1d4-fa5fce872fb6)
 Call ID: 549bbc9c-36de-4cf2-b1d4-fa5fce872fb6
  Args:
    type: :Woman
    source: Lady Christian Norah Dawson-Damer
  AssignClass (d0a7a582-4b97-4934-a26e-65af83bce0b4)
 Call ID: d0a7a582-4b97-4934-a26e-65af83bce0b4
  Args:
    type: :Person
    source: Lady Christian Norah Dawson-Damer
  AddTriple (d347122d-130c-4c25-9c09-9dc3c5d0226e)
 Call ID: d347122d-130c-4c25-9c09-9dc3c5d0226e
  Args:
    target: Lady Christian Norah Dawson-Damer
    source: Fergus Bowes-Lyon
    relation: :hasRelation
  AddLiteral (62ed6c8f-d886-4aa7-b0db-fb91310c65ab)
 Call ID: 62ed6c8f-d886-4aa7-b0db-fb91310c65ab
  Args:
    literal_value: 1914
    literal_type: xsd:string
    relation: :hasMarriageYear
    source: Fergus Bowes-Lyon
  AssignClass (bc67140e-1d9f-4b30-bc22-9ee987caf88f)
 Call ID: bc67140e-1d9f-4b30-bc22-9ee987caf88f
  Args:
    type: :Woman
    source: Cecilia Bowes-Lyon
  AssignClass (ee9ffc69-e7b9-4c90-b67a-d3a0fa11aa3b)
 Call ID: ee9ffc69-e7b9-4c90-b67a-d3a0fa11aa3b
  Args:
    source: Cecilia Bowes-Lyon
    type: :Person
  AddTriple (4f2b03ca-55c2-4f82-8e09-723fe388df47)
 Call ID: 4f2b03ca-55c2-4f82-8e09-723fe388df47
  Args:
    source: Fergus Bowes-Lyon
    relation: :hasMother
    target: Cecilia Bowes-Lyon
  AssignClass (2015422f-b267-4fdf-96d6-fba4ccc612b3)
 Call ID: 2015422f-b267-4fdf-96d6-fba4ccc612b3
  Args:
    source: John Bowes-Lyon
    type: :Man
  AssignClass (e331ca61-ef1a-4a7f-940f-7623099a5444)
 Call ID: e331ca61-ef1a-4a7f-940f-7623099a5444
  Args:
    type: :Person
    source: John Bowes-Lyon
  AddTriple (4500c637-a7eb-4555-b021-f2812521f9ae)
 Call ID: 4500c637-a7eb-4555-b021-f2812521f9ae
  Args:
    source: Fergus Bowes-Lyon
    relation: :isBrotherOf
    target: John Bowes-Lyon
  Finish (eb050e84-8967-454b-85ff-9c666b7449f4)
 Call ID: eb050e84-8967-454b-85ff-9c666b7449f4
  Args: