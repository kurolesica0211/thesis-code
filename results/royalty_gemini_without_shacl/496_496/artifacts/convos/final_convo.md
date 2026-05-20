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
Roger de Vilmorin (Roger Marie Vincent Philippe Lévêque de Vilmorin; 12 September 1905 – 20 July 1980) was a French botanist and geneticist, as well as an illegitimate son of Alfonso XIII of Spain.
Biography

Roger was born on 12 September 1905 in Paris, the natural son of Mélanie de Gaufridy de Dortan (1876–1937) and the King of Spain Alfonso XIII.
However, he was recognized by his mother's legitimate husband, Philippe de Vilmorin, a well-known botanist and horticulturist.
Roger followed in his legal father's footsteps, becoming a botanist and geneticist himself.
Between 1926 and 1964 he directed the scientific services of Vilmorin & Cie, the family seed manufacturing company.
Honours

In 1990, Roger and his half-brother Olivier were included among the Righteous Among the Nations by the National Holocaust Remembrance Institute in Jerusalem because during the Second World War they saved some Jews from deportation to Auschwitz.
Roger de Vilmorin was an officer of the Order of Academic Palms and of the National Order of the Legion of Honour, Commander of the Order of Agricultural Merit and Knight of the National Order of Merit.
The Arboretum Vilmorin is dedicated to him and Philippe de Vilmorin.



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
  AssignClass (60f27681-da13-41fa-9ce6-49334c1fdd37)
 Call ID: 60f27681-da13-41fa-9ce6-49334c1fdd37
  Args:
    source: :Roger_de_Vilmorin
    type: :Man
  AssignClass (e48ca15e-a4b9-4b98-a7ad-f75450fde39e)
 Call ID: e48ca15e-a4b9-4b98-a7ad-f75450fde39e
  Args:
    type: :Person
    source: :Roger_de_Vilmorin
  AddLiteral (3df4ae70-36ca-40cd-8c00-5d7f3882566c)
 Call ID: 3df4ae70-36ca-40cd-8c00-5d7f3882566c
  Args:
    relation: :hasSex
    literal_type: xsd:string
    source: :Roger_de_Vilmorin
    literal_value: Male
  AddLiteral (11da3314-01b3-445e-8687-db1c109012b6)
 Call ID: 11da3314-01b3-445e-8687-db1c109012b6
  Args:
    literal_value: 1905
    source: :Roger_de_Vilmorin
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (ddfae10f-27c3-4c6f-93c0-76e613729b2a)
 Call ID: ddfae10f-27c3-4c6f-93c0-76e613729b2a
  Args:
    literal_value: 1980
    literal_type: xsd:integer
    source: :Roger_de_Vilmorin
    relation: :hasDeathYear
  AssignClass (8fb18129-f05f-43c9-a227-2b9beb59aab0)
 Call ID: 8fb18129-f05f-43c9-a227-2b9beb59aab0
  Args:
    source: :Mélanie_de_Gaufridy_de_Dortan
    type: :Woman
  AssignClass (c5558597-82e5-44e8-8a73-669a2eab12f8)
 Call ID: c5558597-82e5-44e8-8a73-669a2eab12f8
  Args:
    type: :Person
    source: :Mélanie_de_Gaufridy_de_Dortan
  AddLiteral (3718eb93-3405-4ac1-97a2-feee2a4c870f)
 Call ID: 3718eb93-3405-4ac1-97a2-feee2a4c870f
  Args:
    source: :Mélanie_de_Gaufridy_de_Dortan
    literal_type: xsd:integer
    literal_value: 1876
    relation: :hasBirthYear
  AddLiteral (8bb760d6-0d7b-481d-9558-cc74941b2dfc)
 Call ID: 8bb760d6-0d7b-481d-9558-cc74941b2dfc
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: :Mélanie_de_Gaufridy_de_Dortan
    literal_value: 1937
  AssignClass (12a25e8e-d763-4e53-9948-d57f5309f88a)
 Call ID: 12a25e8e-d763-4e53-9948-d57f5309f88a
  Args:
    type: :Man
    source: :Alfonso_XIII_of_Spain
  AssignClass (aba6640f-b338-4a01-8bc6-b61cdf77f755)
 Call ID: aba6640f-b338-4a01-8bc6-b61cdf77f755
  Args:
    type: :Person
    source: :Alfonso_XIII_of_Spain
  AssignClass (bcf85d7a-5217-4906-98e9-f4a14062dfe1)
 Call ID: bcf85d7a-5217-4906-98e9-f4a14062dfe1
  Args:
    type: :Man
    source: :Philippe_de_Vilmorin
  AssignClass (50130f96-ab5c-415e-a93d-3bd27c5dd697)
 Call ID: 50130f96-ab5c-415e-a93d-3bd27c5dd697
  Args:
    source: :Philippe_de_Vilmorin
    type: :Person
  AddTriple (969f8d7c-c56c-46c7-a5ba-997543b95f86)
 Call ID: 969f8d7c-c56c-46c7-a5ba-997543b95f86
  Args:
    target: :Mélanie_de_Gaufridy_de_Dortan
    source: :Roger_de_Vilmorin
    relation: :hasMother
  AddTriple (419c7a8c-46cf-4414-8866-ad8f52e9fce7)
 Call ID: 419c7a8c-46cf-4414-8866-ad8f52e9fce7
  Args:
    source: :Roger_de_Vilmorin
    target: :Alfonso_XIII_of_Spain
    relation: :hasFather
  AddTriple (0d36fd4b-4ee0-4f95-b5bc-432802a1c244)
 Call ID: 0d36fd4b-4ee0-4f95-b5bc-432802a1c244
  Args:
    relation: :hasFather
    source: :Roger_de_Vilmorin
    target: :Philippe_de_Vilmorin
  AssignClass (ec65da6f-5b7d-4337-8dd1-fa10bd724152)
 Call ID: ec65da6f-5b7d-4337-8dd1-fa10bd724152
  Args:
    type: :Man
    source: :Olivier
  AssignClass (63cf22a4-2895-43b8-8b94-f6597396bf9a)
 Call ID: 63cf22a4-2895-43b8-8b94-f6597396bf9a
  Args:
    type: :Person
    source: :Olivier
  AddTriple (92a7458e-1812-4f79-b1bf-35e35780fc59)
 Call ID: 92a7458e-1812-4f79-b1bf-35e35780fc59
  Args:
    source: :Roger_de_Vilmorin
    target: :Olivier
    relation: :hasBrother
  Finish (7e1c70ae-2deb-485a-a54c-c0fd4a1155b6)
 Call ID: 7e1c70ae-2deb-485a-a54c-c0fd4a1155b6
  Args: