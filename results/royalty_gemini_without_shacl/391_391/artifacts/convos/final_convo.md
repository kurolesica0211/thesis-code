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
Princess Marie Alix of Schaumburg-Lippe (Marie Alix zu Schaumburg-Lippe; 2 April 1923 – 1 November 2021) was Duchess of Schleswig-Holstein as the wife of Peter, Duke of Schleswig-Holstein from 1965 to 1980.
Biography

Family

Marie Alix was the only daughter of Prince Stefan of Schaumburg-Lippe  and Ingeborg Alix, Princess Stephan Alexander of Schaumburg-Lippe .
She was the niece of Adolf II, the last ruler of the Principality of Schaumburg-Lippe, who abdicated following the German Revolution of 1918–1919.
Marie Alix's younger brother, Prince Georg Moritz of Schaumburg-Lippe, was killed in a car accident in 1970 without marrying or having children.
Marriage and issue

Marie Alix married Peter, Duke of Schleswig-Holstein, third son of Wilhelm Friedrich, Duke of Schleswig-Holstein, and Princess Marie Melita of Hohenlohe-Langenburg, in Glücksburg on 9 October 1947.
They had four children:


Work

She was a co-founder of the Stiftung Louisenlund, which runs an eponymous boarding school in Güby, Schleswig-Holstein, Germany.
Death and funeral

Princess Marie Alix of Schaumburg-Lippe died in Thumby on 1 November 2021 at the age of 98.
Her funeral was held 11 November 2021 in Schleswig Cathedral and she was buried in a family crypt at the family home, Louisenlund.



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
  AssignClass (7a3c377c-fdba-458d-9d00-fad0d1bafcd9)
 Call ID: 7a3c377c-fdba-458d-9d00-fad0d1bafcd9
  Args:
    source: Marie_Alix_of_Schaumburg-Lippe
    type: :Woman
  AssignClass (d42c2893-3946-436a-b048-c55054b1e00c)
 Call ID: d42c2893-3946-436a-b048-c55054b1e00c
  Args:
    source: Marie_Alix_of_Schaumburg-Lippe
    type: :Person
  AddLiteral (aea5a11f-5b64-4cbb-ba9f-ebea775794fb)
 Call ID: aea5a11f-5b64-4cbb-ba9f-ebea775794fb
  Args:
    literal_type: xsd:integer
    source: Marie_Alix_of_Schaumburg-Lippe
    literal_value: 1923
    relation: :hasBirthYear
  AddLiteral (30d06de7-8a84-48a6-84f4-8fa9cfd2b3ac)
 Call ID: 30d06de7-8a84-48a6-84f4-8fa9cfd2b3ac
  Args:
    literal_type: xsd:integer
    source: Marie_Alix_of_Schaumburg-Lippe
    relation: :hasDeathYear
    literal_value: 2021
  AddLiteral (dc2f4fdb-95b7-4b76-b05a-e554b6321ae8)
 Call ID: dc2f4fdb-95b7-4b76-b05a-e554b6321ae8
  Args:
    literal_type: xsd:string
    source: Marie_Alix_of_Schaumburg-Lippe
    relation: :alsoKnownAs
    literal_value: Marie Alix zu Schaumburg-Lippe
  AssignClass (5c641cad-e503-4c59-9bb0-ee4cfc8ff1e2)
 Call ID: 5c641cad-e503-4c59-9bb0-ee4cfc8ff1e2
  Args:
    type: :Man
    source: Peter_Duke_of_Schleswig-Holstein
  AssignClass (ee448aba-e1f8-4f89-8de5-7ae7ebda1fc4)
 Call ID: ee448aba-e1f8-4f89-8de5-7ae7ebda1fc4
  Args:
    source: Peter_Duke_of_Schleswig-Holstein
    type: :Person
  AddLiteral (0268ecd1-34e1-459a-81b4-882c84817f39)
 Call ID: 0268ecd1-34e1-459a-81b4-882c84817f39
  Args:
    source: Marie_Alix_of_Schaumburg-Lippe
    literal_type: xsd:integer
    literal_value: 1965
    relation: :hasMarriageYear
  AssignClass (4b7df95d-e6b7-46ec-ae6c-c36913ce8fa9)
 Call ID: 4b7df95d-e6b7-46ec-ae6c-c36913ce8fa9
  Args:
    source: Stefan_of_Schaumburg-Lippe
    type: :Man
  AssignClass (a2b8f836-464f-4194-a2dd-ad74468eb45e)
 Call ID: a2b8f836-464f-4194-a2dd-ad74468eb45e
  Args:
    source: Stefan_of_Schaumburg-Lippe
    type: :Person
  AssignClass (6922bbb1-bc48-474f-ae67-57a1b1dbd98b)
 Call ID: 6922bbb1-bc48-474f-ae67-57a1b1dbd98b
  Args:
    source: Ingeborg_Alix_of_Schaumburg-Lippe
    type: :Woman
  AssignClass (9c5460b4-bb83-46ca-9d62-f7d525d1b119)
 Call ID: 9c5460b4-bb83-46ca-9d62-f7d525d1b119
  Args:
    type: :Person
    source: Ingeborg_Alix_of_Schaumburg-Lippe
  AddTriple (82fff719-4045-4557-b320-115e9c32e01a)
 Call ID: 82fff719-4045-4557-b320-115e9c32e01a
  Args:
    target: Stefan_of_Schaumburg-Lippe
    source: Marie_Alix_of_Schaumburg-Lippe
    relation: :hasFather
  AddTriple (556e1da0-4428-4164-958a-5bad6da880f7)
 Call ID: 556e1da0-4428-4164-958a-5bad6da880f7
  Args:
    source: Marie_Alix_of_Schaumburg-Lippe
    target: Ingeborg_Alix_of_Schaumburg-Lippe
    relation: :hasMother
  AssignClass (ac73e3b5-3b7f-4c34-999f-73d0401c28ff)
 Call ID: ac73e3b5-3b7f-4c34-999f-73d0401c28ff
  Args:
    source: Adolf_II_of_Schaumburg-Lippe
    type: :Man
  AssignClass (1e9b674b-5913-49fb-8f31-32a3227b6cb4)
 Call ID: 1e9b674b-5913-49fb-8f31-32a3227b6cb4
  Args:
    type: :Person
    source: Adolf_II_of_Schaumburg-Lippe
  AssignClass (11cf1537-99d9-4edc-9ac8-d6a0d00de6d6)
 Call ID: 11cf1537-99d9-4edc-9ac8-d6a0d00de6d6
  Args:
    source: Georg_Moritz_of_Schaumburg-Lippe
    type: :Man
  AssignClass (53a60bf8-451f-41cf-ad6d-10cdee6a5101)
 Call ID: 53a60bf8-451f-41cf-ad6d-10cdee6a5101
  Args:
    type: :Person
    source: Georg_Moritz_of_Schaumburg-Lippe
  AddTriple (924f37b9-b2d9-4b5b-943f-4dc8aa6cfa46)
 Call ID: 924f37b9-b2d9-4b5b-943f-4dc8aa6cfa46
  Args:
    relation: :hasBrother
    source: Marie_Alix_of_Schaumburg-Lippe
    target: Georg_Moritz_of_Schaumburg-Lippe
  AssignClass (916baadf-929c-46cc-a2e2-da75c622d512)
 Call ID: 916baadf-929c-46cc-a2e2-da75c622d512
  Args:
    source: Wilhelm_Friedrich_of_Schleswig-Holstein
    type: :Man
  AssignClass (465ef5cb-3de8-4849-8138-5d1dbb68b107)
 Call ID: 465ef5cb-3de8-4849-8138-5d1dbb68b107
  Args:
    source: Wilhelm_Friedrich_of_Schleswig-Holstein
    type: :Person
  AssignClass (fb9d9ac8-f981-4151-abb7-2b71c2118dc6)
 Call ID: fb9d9ac8-f981-4151-abb7-2b71c2118dc6
  Args:
    type: :Woman
    source: Marie_Melita_of_Hohenlohe-Langenburg
  AssignClass (f756688c-e7c9-439b-b234-1329841b4481)
 Call ID: f756688c-e7c9-439b-b234-1329841b4481
  Args:
    source: Marie_Melita_of_Hohenlohe-Langenburg
    type: :Person
  AddTriple (5441fb6a-8574-4f60-a2fc-a699c8fd5c91)
 Call ID: 5441fb6a-8574-4f60-a2fc-a699c8fd5c91
  Args:
    relation: :hasFather
    target: Wilhelm_Friedrich_of_Schleswig-Holstein
    source: Peter_Duke_of_Schleswig-Holstein
  AddTriple (e43743fb-e007-46aa-a77d-9ba83c927267)
 Call ID: e43743fb-e007-46aa-a77d-9ba83c927267
  Args:
    target: Marie_Melita_of_Hohenlohe-Langenburg
    source: Peter_Duke_of_Schleswig-Holstein
    relation: :hasMother
  Finish (96d3e679-8920-4896-8d06-814f7952022c)
 Call ID: 96d3e679-8920-4896-8d06-814f7952022c
  Args: