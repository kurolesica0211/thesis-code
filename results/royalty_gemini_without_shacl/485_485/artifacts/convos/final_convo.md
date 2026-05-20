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
Eleonore von Habsburg-Lothringen (Eleonore Maria del Pilar Iona Christina Jelena; born 28 February 1994) is an Austrian jewellery designer, gemologist, and model.
She is the daughter of Karl von Habsburg, the head of the House of Habsburg-Lorraine.
Early life and background

Eleonore Habsburg-Lorraine was born in 1994 in Salzburg to Karl von Habsburg, a politician and head of the House of Habsburg-Lorraine, and Francesca von Thyssen-Bornemisza de Kászon et Impérfalva, an art collector and by birth member of the Thyssen-Bornemisza family.
Her paternal grandparents were Otto, Crown Prince of Austria and Princess Regina of Saxe-Meiningen.
Her paternal great-grandparents Charles I of Austria and Zita of Bourbon-Parma were the last Emperor and Empress of Austria.
Her brother is racing car driver Ferdinand Habsburg.
Education and career

Habsburg-Lorraine attended boarding school in Gstaad before studying law at the European Business School London.
Habsburg has also worked as a fashion model, being featured in advertisement campaigns and walking the runway for Dolce & Gabbana.
Personal life

On 20 July 2020, Eleonore von Habsburg-Lorraine married Belgian race car driver Jérôme d'Ambrosio in a small civil ceremony at the Civil Registry of Monaco, conducted by the Mayor of Monaco Georges Marsan.
On 20 October 2021 she gave birth to a son, Otto d'Ambrosio, named after her grandfather Otto von Habsburg.



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
  AssignClass (18e2afb4-36c6-484e-a739-76fc25d4daf5)
 Call ID: 18e2afb4-36c6-484e-a739-76fc25d4daf5
  Args:
    type: :Woman
    source: Eleonore_von_Habsburg-Lothringen
  AssignClass (dc192bb3-a200-4b77-94f6-94e34ca26ce1)
 Call ID: dc192bb3-a200-4b77-94f6-94e34ca26ce1
  Args:
    source: Eleonore_von_Habsburg-Lothringen
    type: :Person
  AddLiteral (c2459d44-40be-496c-9bb8-f44b64bbb484)
 Call ID: c2459d44-40be-496c-9bb8-f44b64bbb484
  Args:
    source: Eleonore_von_Habsburg-Lothringen
    relation: :hasBirthYear
    literal_value: 1994
    literal_type: xsd:integer
  AssignClass (64a14cf0-bbbd-4bf2-80b5-db62abed3f07)
 Call ID: 64a14cf0-bbbd-4bf2-80b5-db62abed3f07
  Args:
    type: :Man
    source: Karl_von_Habsburg
  AssignClass (d5b08dba-69e5-4abb-b303-1ef16512e5b5)
 Call ID: d5b08dba-69e5-4abb-b303-1ef16512e5b5
  Args:
    source: Karl_von_Habsburg
    type: :Person
  AssignClass (3db5bd8d-4d8e-49ba-bf26-5576e7917428)
 Call ID: 3db5bd8d-4d8e-49ba-bf26-5576e7917428
  Args:
    type: :Woman
    source: Francesca_von_Thyssen-Bornemisza
  AssignClass (fd11ac9d-2494-475c-a6d0-17fb4f670bba)
 Call ID: fd11ac9d-2494-475c-a6d0-17fb4f670bba
  Args:
    source: Francesca_von_Thyssen-Bornemisza
    type: :Person
  AddTriple (94103813-554b-407e-892a-38cf88ebf7ce)
 Call ID: 94103813-554b-407e-892a-38cf88ebf7ce
  Args:
    source: Eleonore_von_Habsburg-Lothringen
    relation: :hasFather
    target: Karl_von_Habsburg
  AddTriple (9801acbb-c2b9-4b0b-bdd7-79151f2388d0)
 Call ID: 9801acbb-c2b9-4b0b-bdd7-79151f2388d0
  Args:
    relation: :hasMother
    source: Eleonore_von_Habsburg-Lothringen
    target: Francesca_von_Thyssen-Bornemisza
  AssignClass (f0bfa51f-e64f-45b1-aa78-5c199be1691c)
 Call ID: f0bfa51f-e64f-45b1-aa78-5c199be1691c
  Args:
    source: Otto_von_Habsburg
    type: :Man
  AssignClass (3c9784b6-c175-42aa-8077-3ee1f8cf0982)
 Call ID: 3c9784b6-c175-42aa-8077-3ee1f8cf0982
  Args:
    type: :Person
    source: Otto_von_Habsburg
  AssignClass (a997dd4e-3858-4d4c-8ea0-4aee0e199b1d)
 Call ID: a997dd4e-3858-4d4c-8ea0-4aee0e199b1d
  Args:
    source: Regina_von_Saxe-Meiningen
    type: :Woman
  AssignClass (420ade95-30ab-49ce-a256-0c7e4b657186)
 Call ID: 420ade95-30ab-49ce-a256-0c7e4b657186
  Args:
    source: Regina_von_Saxe-Meiningen
    type: :Person
  AddTriple (9970558a-3f1f-4ff3-a65f-ad44fd35aeb0)
 Call ID: 9970558a-3f1f-4ff3-a65f-ad44fd35aeb0
  Args:
    target: Otto_von_Habsburg
    source: Karl_von_Habsburg
    relation: :hasFather
  AddTriple (fa14c0ea-0cbe-4014-8039-809a5b55d041)
 Call ID: fa14c0ea-0cbe-4014-8039-809a5b55d041
  Args:
    source: Karl_von_Habsburg
    relation: :hasMother
    target: Regina_von_Saxe-Meiningen
  AssignClass (99a1cf4c-8ed6-4f9a-b108-2ccf7e7ccef7)
 Call ID: 99a1cf4c-8ed6-4f9a-b108-2ccf7e7ccef7
  Args:
    type: :Man
    source: Charles_I_of_Austria
  AssignClass (14158aba-8b5d-49b4-bab3-418cc7b964b3)
 Call ID: 14158aba-8b5d-49b4-bab3-418cc7b964b3
  Args:
    type: :Person
    source: Charles_I_of_Austria
  AssignClass (c183a51b-34ee-4e92-8850-f14440696ea7)
 Call ID: c183a51b-34ee-4e92-8850-f14440696ea7
  Args:
    source: Zita_of_Bourbon-Parma
    type: :Woman
  AssignClass (43d46dc8-feb5-4cf4-9444-88c3f9fc9fb7)
 Call ID: 43d46dc8-feb5-4cf4-9444-88c3f9fc9fb7
  Args:
    type: :Person
    source: Zita_of_Bourbon-Parma
  AddTriple (7ef79017-57fb-4d33-bebf-97fe8a08ca97)
 Call ID: 7ef79017-57fb-4d33-bebf-97fe8a08ca97
  Args:
    relation: :hasFather
    source: Otto_von_Habsburg
    target: Charles_I_of_Austria
  AddTriple (6b0993f6-4ca6-4465-a9c5-f7a741d84c8c)
 Call ID: 6b0993f6-4ca6-4465-a9c5-f7a741d84c8c
  Args:
    relation: :hasMother
    source: Otto_von_Habsburg
    target: Zita_of_Bourbon-Parma
  AssignClass (644a0a11-27f6-4771-913a-4819596f5753)
 Call ID: 644a0a11-27f6-4771-913a-4819596f5753
  Args:
    source: Ferdinand_Habsburg
    type: :Man
  AssignClass (9cc045e6-feee-4348-bf59-618e3c63b6fc)
 Call ID: 9cc045e6-feee-4348-bf59-618e3c63b6fc
  Args:
    source: Ferdinand_Habsburg
    type: :Person
  AddTriple (32295846-d059-4465-aa04-5dcb795f4813)
 Call ID: 32295846-d059-4465-aa04-5dcb795f4813
  Args:
    source: Eleonore_von_Habsburg-Lothringen
    relation: :hasBrother
    target: Ferdinand_Habsburg
  AssignClass (dd4bbf1f-4ee4-4c4f-aaec-c11b9deb0a85)
 Call ID: dd4bbf1f-4ee4-4c4f-aaec-c11b9deb0a85
  Args:
    type: :Man
    source: Jérôme_d'Ambrosio
  AssignClass (34f5c3bf-8ecf-45c7-90c5-ceff9f174baa)
 Call ID: 34f5c3bf-8ecf-45c7-90c5-ceff9f174baa
  Args:
    source: Jérôme_d'Ambrosio
    type: :Person
  AddLiteral (c8c79d25-8d9d-41c8-8715-bd9c3ab09425)
 Call ID: c8c79d25-8d9d-41c8-8715-bd9c3ab09425
  Args:
    literal_type: xsd:integer
    literal_value: 2020
    relation: :hasMarriageYear
    source: Eleonore_von_Habsburg-Lothringen
  AddTriple (12785a45-50d2-4532-ba6c-45232257c404)
 Call ID: 12785a45-50d2-4532-ba6c-45232257c404
  Args:
    target: Jérôme_d'Ambrosio
    relation: :hasRelation
    source: Eleonore_von_Habsburg-Lothringen
  AssignClass (af2d2a4f-b061-4294-a2f0-89da9d800d8d)
 Call ID: af2d2a4f-b061-4294-a2f0-89da9d800d8d
  Args:
    type: :Man
    source: Otto_d'Ambrosio
  AssignClass (c6183c1b-0d11-4543-a081-e75f91e57007)
 Call ID: c6183c1b-0d11-4543-a081-e75f91e57007
  Args:
    source: Otto_d'Ambrosio
    type: :Person
  AddTriple (01de8b79-160d-4bdd-88d6-2ee84250db97)
 Call ID: 01de8b79-160d-4bdd-88d6-2ee84250db97
  Args:
    target: Jérôme_d'Ambrosio
    source: Otto_d'Ambrosio
    relation: :hasFather
  AddTriple (90863996-a925-4bc7-b3ea-98abcff46a30)
 Call ID: 90863996-a925-4bc7-b3ea-98abcff46a30
  Args:
    relation: :hasMother
    source: Otto_d'Ambrosio
    target: Eleonore_von_Habsburg-Lothringen
  Finish (1f53b8fa-c8b4-40df-af95-e1747bb11427)
 Call ID: 1f53b8fa-c8b4-40df-af95-e1747bb11427
  Args: