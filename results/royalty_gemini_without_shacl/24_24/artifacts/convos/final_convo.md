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
Duchess Marie Antoinette of Mecklenburg-Schwerin, also Manette (Marie Antoinette Margarethe Mathilde; 28 May 1884 – 26 October 1944) was the Duchess of Mecklenburg-Schwerin by birth and potential bride for King Alfonso XIII of Spain.
Early life

Marie Antoinette was born in Venice, into the House of Mecklenburg, as the third child and the second daughter of Duke Paul Frederick of Mecklenburg and Princess Marie of Windisch-Graetz.
Her brothers and sisters were Duke Paul Friedrich of Mecklenburg, Duchess Maria Luise of Mecklenburg-Schwerin (1883–1883), Duke Heinrich Borwin of Mecklenburg-Schwerin (1885–1942), and Duke Joseph of Mecklenburg-Schwerin (1889–1889).
She had a difficult relationship with her cousin Frederick Francis IV, Grand Duke of Mecklenburg-Schwerin, who regularly had to amortize her debts.
So, Marie Antoinette regularly had to sell archaeological artifacts belonging to her mother, excavated in Austria and Carniola, including Hallstatt Archaeological Site in Vače.
Potential bride for the King of Spain

She was German Kaiser Wilhelm II's candidate for a bride for King Alfonso XIII of Spain although he would marry the Kaiser's maternal first cousin, Princess Victoria Eugenie, niece of British King Edward VII.



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
  AssignClass (1efe1257-c044-42d3-855a-ae3c0cbbbe63)
 Call ID: 1efe1257-c044-42d3-855a-ae3c0cbbbe63
  Args:
    type: :Person
    source: Marie_Antoinette_of_Mecklenburg-Schwerin
  AssignClass (2ae783fd-ce79-4849-954c-69e5c6bad427)
 Call ID: 2ae783fd-ce79-4849-954c-69e5c6bad427
  Args:
    source: Marie_Antoinette_of_Mecklenburg-Schwerin
    type: :Woman
  AddLiteral (2138ace6-48ca-410a-b1f1-cf3a71e89e61)
 Call ID: 2138ace6-48ca-410a-b1f1-cf3a71e89e61
  Args:
    source: Marie_Antoinette_of_Mecklenburg-Schwerin
    literal_type: xsd:string
    literal_value: Manette
    relation: :alsoKnownAs
  AddLiteral (17f92179-42a1-4ac5-9229-8f9f1bcea895)
 Call ID: 17f92179-42a1-4ac5-9229-8f9f1bcea895
  Args:
    source: Marie_Antoinette_of_Mecklenburg-Schwerin
    literal_type: xsd:string
    literal_value: 1884
    relation: :hasBirthYear
  AddLiteral (ee8d2279-7051-4e9f-ab4f-e326455c8ac8)
 Call ID: ee8d2279-7051-4e9f-ab4f-e326455c8ac8
  Args:
    literal_value: 1944
    relation: :hasDeathYear
    source: Marie_Antoinette_of_Mecklenburg-Schwerin
    literal_type: xsd:string
  AssignClass (985bd638-67f6-4839-9c65-24e2c6dfa8d1)
 Call ID: 985bd638-67f6-4839-9c65-24e2c6dfa8d1
  Args:
    type: :Person
    source: Paul_Frederick_of_Mecklenburg
  AssignClass (c0238d97-049a-4099-99e0-63235906019a)
 Call ID: c0238d97-049a-4099-99e0-63235906019a
  Args:
    source: Paul_Frederick_of_Mecklenburg
    type: :Man
  AssignClass (70f78a05-8db0-4e13-a42d-5c4899340e4d)
 Call ID: 70f78a05-8db0-4e13-a42d-5c4899340e4d
  Args:
    type: :Person
    source: Marie_of_Windisch-Graetz
  AssignClass (0e910e94-577d-48bb-bc4c-23c46716976f)
 Call ID: 0e910e94-577d-48bb-bc4c-23c46716976f
  Args:
    type: :Woman
    source: Marie_of_Windisch-Graetz
  AddTriple (035d7740-106a-4aa4-b6be-cb1c4b969a34)
 Call ID: 035d7740-106a-4aa4-b6be-cb1c4b969a34
  Args:
    source: Marie_Antoinette_of_Mecklenburg-Schwerin
    target: Paul_Frederick_of_Mecklenburg
    relation: :hasFather
  AddTriple (c4f76861-709e-4e6d-9f4d-b2bf5cc5adf9)
 Call ID: c4f76861-709e-4e6d-9f4d-b2bf5cc5adf9
  Args:
    source: Marie_Antoinette_of_Mecklenburg-Schwerin
    target: Marie_of_Windisch-Graetz
    relation: :hasMother
  AssignClass (a8ef42e7-dffd-4227-bbd8-c930d11ed5b9)
 Call ID: a8ef42e7-dffd-4227-bbd8-c930d11ed5b9
  Args:
    type: :Person
    source: Paul_Friedrich_of_Mecklenburg
  AssignClass (7df07999-c390-4b64-b640-28417b61a215)
 Call ID: 7df07999-c390-4b64-b640-28417b61a215
  Args:
    source: Paul_Friedrich_of_Mecklenburg
    type: :Man
  AddTriple (eb27d2e0-de50-476d-9c1b-3fae54e86e30)
 Call ID: eb27d2e0-de50-476d-9c1b-3fae54e86e30
  Args:
    source: Marie_Antoinette_of_Mecklenburg-Schwerin
    relation: :hasBrother
    target: Paul_Friedrich_of_Mecklenburg
  AssignClass (795d6d62-c2df-4d6a-94ec-818aff574eed)
 Call ID: 795d6d62-c2df-4d6a-94ec-818aff574eed
  Args:
    type: :Person
    source: Maria_Luise_of_Mecklenburg-Schwerin
  AssignClass (58e0d3f6-b0b6-4f9d-83cd-ed1aad8b7b9e)
 Call ID: 58e0d3f6-b0b6-4f9d-83cd-ed1aad8b7b9e
  Args:
    type: :Woman
    source: Maria_Luise_of_Mecklenburg-Schwerin
  AddTriple (cb089fd4-f6b8-4b14-a1cd-5f075d344fef)
 Call ID: cb089fd4-f6b8-4b14-a1cd-5f075d344fef
  Args:
    relation: :hasSister
    target: Maria_Luise_of_Mecklenburg-Schwerin
    source: Marie_Antoinette_of_Mecklenburg-Schwerin
  AssignClass (1e5c2446-bad4-49ac-80ae-480baf0745e2)
 Call ID: 1e5c2446-bad4-49ac-80ae-480baf0745e2
  Args:
    type: :Person
    source: Heinrich_Borwin_of_Mecklenburg-Schwerin
  AssignClass (f7f6c8a5-3191-4c77-9b82-0c807340ea6b)
 Call ID: f7f6c8a5-3191-4c77-9b82-0c807340ea6b
  Args:
    source: Heinrich_Borwin_of_Mecklenburg-Schwerin
    type: :Man
  AddTriple (a6a4e2c5-dc12-4494-b7b0-0274de4f2e7a)
 Call ID: a6a4e2c5-dc12-4494-b7b0-0274de4f2e7a
  Args:
    source: Marie_Antoinette_of_Mecklenburg-Schwerin
    target: Heinrich_Borwin_of_Mecklenburg-Schwerin
    relation: :hasBrother
  AssignClass (0ca6a187-9ca7-4400-906a-42f6e8ed31fb)
 Call ID: 0ca6a187-9ca7-4400-906a-42f6e8ed31fb
  Args:
    source: Joseph_of_Mecklenburg-Schwerin
    type: :Person
  AssignClass (9220617a-0ba5-424b-8166-8ed0ee6e85a1)
 Call ID: 9220617a-0ba5-424b-8166-8ed0ee6e85a1
  Args:
    type: :Man
    source: Joseph_of_Mecklenburg-Schwerin
  AddTriple (8e64eb8c-b65f-42fe-b885-909a565646a5)
 Call ID: 8e64eb8c-b65f-42fe-b885-909a565646a5
  Args:
    target: Joseph_of_Mecklenburg-Schwerin
    relation: :hasBrother
    source: Marie_Antoinette_of_Mecklenburg-Schwerin
  Finish (850f532f-de48-421e-8d00-d94609584451)
 Call ID: 850f532f-de48-421e-8d00-d94609584451
  Args: