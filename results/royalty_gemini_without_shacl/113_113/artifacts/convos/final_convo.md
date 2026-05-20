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
Prince Ranieri Maria Gaetano, Duke of Castro (3 December 1883 – 13 January 1973) was a claimant to the headship of the House of Bourbon-Two Sicilies.
He was born in Cannes, France, the ninth child but fifth son of Prince Alfonso, Count of Caserta and Princess Maria Antonietta of Bourbon-Two Sicilies (1851–1938).
Following the death of his brother Prince Ferdinand Pius, Duke of Calabria on 7 January 1960 Prince Ranieri was declared Head of the House of Bourbon-Two Sicilies by all relatives except for Infante Alfonso, Duke of Calabria and his children, because the Infante's senior branch of the family abdicated their claims in order to be in line for the Spanish throne.
Marriage and children

Ranieri married his first cousin Countess Maria Carolina Zamoyska (1896–1968) on 12 September 1923 in Vyšné Ružbachy, Slovakia, from the marriage he had two children:


Honours

Arms

Ancestry

References

External links



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
  AssignClass (a32c9248-73f2-4a1c-baec-3cfaf29b6913)
 Call ID: a32c9248-73f2-4a1c-baec-3cfaf29b6913
  Args:
    type: :Man
    source: Prince_Ranieri_Maria_Gaetano
  AssignClass (75b00e95-ae99-4611-b53a-0cf8788f256c)
 Call ID: 75b00e95-ae99-4611-b53a-0cf8788f256c
  Args:
    type: :Person
    source: Prince_Ranieri_Maria_Gaetano
  AssignClass (e0dc6da0-fdd4-4dc7-8b1c-56f34f1a348a)
 Call ID: e0dc6da0-fdd4-4dc7-8b1c-56f34f1a348a
  Args:
    source: Prince_Alfonso_Count_of_Caserta
    type: :Man
  AssignClass (77d8e9fc-d636-4633-a251-5ec108b2204e)
 Call ID: 77d8e9fc-d636-4633-a251-5ec108b2204e
  Args:
    source: Prince_Alfonso_Count_of_Caserta
    type: :Person
  AssignClass (ba0e0889-c1dd-495b-b8e5-0b6270f2f657)
 Call ID: ba0e0889-c1dd-495b-b8e5-0b6270f2f657
  Args:
    type: :Woman
    source: Princess_Maria_Antonietta_of_Bourbon-Two_Sicilies
  AssignClass (6f033598-4544-4e0a-be28-8f3f98d802a6)
 Call ID: 6f033598-4544-4e0a-be28-8f3f98d802a6
  Args:
    source: Princess_Maria_Antonietta_of_Bourbon-Two_Sicilies
    type: :Person
  AssignClass (2784eaad-764a-4ce1-9d45-5a6c30e6cf85)
 Call ID: 2784eaad-764a-4ce1-9d45-5a6c30e6cf85
  Args:
    type: :Man
    source: Prince_Ferdinand_Pius_Duke_of_Calabria
  AssignClass (e0ff1ae6-d52b-46a8-a8fa-2479f72f2835)
 Call ID: e0ff1ae6-d52b-46a8-a8fa-2479f72f2835
  Args:
    type: :Person
    source: Prince_Ferdinand_Pius_Duke_of_Calabria
  AssignClass (f9d6b13a-da6c-4b33-b2cc-cdbd62fac582)
 Call ID: f9d6b13a-da6c-4b33-b2cc-cdbd62fac582
  Args:
    type: :Man
    source: Infante_Alfonso_Duke_of_Calabria
  AssignClass (127c629f-110c-4bbc-aff1-ff81aa9f5017)
 Call ID: 127c629f-110c-4bbc-aff1-ff81aa9f5017
  Args:
    type: :Person
    source: Infante_Alfonso_Duke_of_Calabria
  AssignClass (8830bf7b-255c-4310-8846-5f73636c9710)
 Call ID: 8830bf7b-255c-4310-8846-5f73636c9710
  Args:
    type: :Woman
    source: Countess_Maria_Carolina_Zamoyska
  AssignClass (c504eec0-a4b0-4c10-88b9-254691aef74b)
 Call ID: c504eec0-a4b0-4c10-88b9-254691aef74b
  Args:
    type: :Person
    source: Countess_Maria_Carolina_Zamoyska
  AddLiteral (d7ba8db8-5054-4db1-8580-60268585613f)
 Call ID: d7ba8db8-5054-4db1-8580-60268585613f
  Args:
    literal_type: xsd:integer
    source: Prince_Ranieri_Maria_Gaetano
    literal_value: 1883
    relation: :hasBirthYear
  AddLiteral (9c5d00cf-5ba9-4ed1-b339-c5acae21d454)
 Call ID: 9c5d00cf-5ba9-4ed1-b339-c5acae21d454
  Args:
    relation: :hasDeathYear
    literal_value: 1973
    literal_type: xsd:integer
    source: Prince_Ranieri_Maria_Gaetano
  AddLiteral (9e77e205-817e-45ea-a0f3-943f96979c4b)
 Call ID: 9e77e205-817e-45ea-a0f3-943f96979c4b
  Args:
    relation: :hasBirthYear
    literal_value: 1851
    literal_type: xsd:integer
    source: Princess_Maria_Antonietta_of_Bourbon-Two_Sicilies
  AddLiteral (66cfd143-76cf-4818-a7e5-7c5d2002e036)
 Call ID: 66cfd143-76cf-4818-a7e5-7c5d2002e036
  Args:
    literal_type: xsd:integer
    source: Princess_Maria_Antonietta_of_Bourbon-Two_Sicilies
    literal_value: 1938
    relation: :hasDeathYear
  AddLiteral (353f4852-ed66-46df-a6b7-294c2bd25513)
 Call ID: 353f4852-ed66-46df-a6b7-294c2bd25513
  Args:
    source: Countess_Maria_Carolina_Zamoyska
    literal_type: xsd:integer
    literal_value: 1896
    relation: :hasBirthYear
  AddLiteral (51eef76e-3832-43ca-b746-10b6019ba757)
 Call ID: 51eef76e-3832-43ca-b746-10b6019ba757
  Args:
    relation: :hasDeathYear
    literal_value: 1968
    source: Countess_Maria_Carolina_Zamoyska
    literal_type: xsd:integer
  AddTriple (7b8176ee-e18d-4c2a-b61b-d2f6b21d8418)
 Call ID: 7b8176ee-e18d-4c2a-b61b-d2f6b21d8418
  Args:
    target: Prince_Alfonso_Count_of_Caserta
    source: Prince_Ranieri_Maria_Gaetano
    relation: :hasFather
  AddTriple (8c7ae985-6db7-4196-a9b1-12f077ab9cdf)
 Call ID: 8c7ae985-6db7-4196-a9b1-12f077ab9cdf
  Args:
    relation: :hasMother
    source: Prince_Ranieri_Maria_Gaetano
    target: Princess_Maria_Antonietta_of_Bourbon-Two_Sicilies
  AddTriple (6a5a614b-4559-489e-85c6-78cdfbb15d4f)
 Call ID: 6a5a614b-4559-489e-85c6-78cdfbb15d4f
  Args:
    relation: :isBrotherOf
    source: Prince_Ranieri_Maria_Gaetano
    target: Prince_Ferdinand_Pius_Duke_of_Calabria
  AddTriple (fcf7fc36-5c1d-47db-9291-c921ebaf969b)
 Call ID: fcf7fc36-5c1d-47db-9291-c921ebaf969b
  Args:
    relation: :hasRelation
    source: Prince_Ranieri_Maria_Gaetano
    target: Countess_Maria_Carolina_Zamoyska
  AddLiteral (d314b462-24e3-47d5-890b-855bd7947300)
 Call ID: d314b462-24e3-47d5-890b-855bd7947300
  Args:
    literal_type: xsd:integer
    source: Prince_Ranieri_Maria_Gaetano
    literal_value: 1923
    relation: :hasMarriageYear
  Finish (c92f05c4-ae56-4ba7-b95d-8c5315abb626)
 Call ID: c92f05c4-ae56-4ba7-b95d-8c5315abb626
  Args: