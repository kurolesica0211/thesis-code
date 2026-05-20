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
Princess Beatrix of Hohenlohe-Langenburg (German: Beatrix Alice Marie Melita Margarete Prinzessin zu Hohenlohe-Langenburg; 10 July 1936 – 15 November 1997) was a German princess from the House of Hohenlohe-Langenburg.
She was a niece of Prince Philip, Duke of Edinburgh, and thus a first cousin of King Charles III.
Biography

Beatrix was born on 10 July 1936 in Schwäbisch Hall to Gottfried, Hereditary Prince of Hohenlohe-Langenburg, and Princess Margarita of Greece and Denmark, the eldest sister of Prince Philip, Duke of Edinburgh.
The family was not invited to Philip's wedding to Princess Elizabeth of the United Kingdom in 1947, due to her parents' membership in the Nazi Party.
Six years later, however, Beatrix and her family were seated in the royal box at  her aunt's coronation in Westminster Abbey.
In January 1956, Beatrix and her cousin, Princess Christina of Hesse, moved to London into a flat arranged by their uncle, Prince Philip, in Dolphin Square.
Beatrix took dressmaking classes at the Royal College of Art.
While Princess Christina eventually settled in the United Kingdom, marrying Prince Andrew of Yugoslavia whom the princesses were close friends with during their stay, Beatrix returned to Germany that same year.
In 1961, Beatrix became engaged to her first cousin, Maximilian, Hereditary Prince of Baden.
Maximilian later married Archduchess Valerie of Austria (b. 1941) in 1966 and Beatrix never married.
In her later years, she served as secretary to Margaret, Princess of Hesse and by Rhine, the sister-in-law of her aunt, Princess Cecilie.
She lived in Langenburg, Germany, for most of her life.
She continued to attend family events in Britain, such as the weddings of her cousins Prince Charles (later King Charles III) and Prince Andrew in 1981 and 1986, respectively.
Beatrix died on 15 November 1997, aged 61, in the town where she was born.



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
  AssignClass (70007f76-9f84-4ab5-9640-09b913a3857b)
 Call ID: 70007f76-9f84-4ab5-9640-09b913a3857b
  Args:
    source: :Beatrix_of_Hohenlohe-Langenburg
    type: :Person
  AssignClass (575d38a3-fe22-4f53-9619-0283c8b43dec)
 Call ID: 575d38a3-fe22-4f53-9619-0283c8b43dec
  Args:
    source: :Beatrix_of_Hohenlohe-Langenburg
    type: :Woman
  AddLiteral (7d1ded2c-2464-4263-b612-d5e78245fcb5)
 Call ID: 7d1ded2c-2464-4263-b612-d5e78245fcb5
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: :Beatrix_of_Hohenlohe-Langenburg
    literal_value: 1936
  AddLiteral (e10ac8c9-92af-438e-80d5-49db0bed3a65)
 Call ID: e10ac8c9-92af-438e-80d5-49db0bed3a65
  Args:
    literal_value: 1997
    source: :Beatrix_of_Hohenlohe-Langenburg
    relation: :hasDeathYear
    literal_type: xsd:integer
  AssignClass (ba4c5e54-6b74-458a-99e3-6f5405272f61)
 Call ID: ba4c5e54-6b74-458a-99e3-6f5405272f61
  Args:
    source: :Gottfried_Hereditary_Prince_of_Hohenlohe-Langenburg
    type: :Person
  AssignClass (62815547-cb68-45ef-85dc-510a2527428d)
 Call ID: 62815547-cb68-45ef-85dc-510a2527428d
  Args:
    source: :Gottfried_Hereditary_Prince_of_Hohenlohe-Langenburg
    type: :Man
  AddTriple (973ca0bd-8b19-4334-91b2-1cb860f4c19b)
 Call ID: 973ca0bd-8b19-4334-91b2-1cb860f4c19b
  Args:
    target: :Gottfried_Hereditary_Prince_of_Hohenlohe-Langenburg
    source: :Beatrix_of_Hohenlohe-Langenburg
    relation: :hasFather
  AssignClass (391ded45-b0de-4103-89c6-50c64566dc74)
 Call ID: 391ded45-b0de-4103-89c6-50c64566dc74
  Args:
    source: :Margarita_of_Greece_and_Denmark
    type: :Person
  AssignClass (af05908b-8d3d-4b3d-b83d-8da56f2e5c10)
 Call ID: af05908b-8d3d-4b3d-b83d-8da56f2e5c10
  Args:
    source: :Margarita_of_Greece_and_Denmark
    type: :Woman
  AddTriple (6ab88ae2-c8a6-4e6f-99d5-d095b9e5661c)
 Call ID: 6ab88ae2-c8a6-4e6f-99d5-d095b9e5661c
  Args:
    target: :Margarita_of_Greece_and_Denmark
    relation: :hasMother
    source: :Beatrix_of_Hohenlohe-Langenburg
  AssignClass (cf40af76-6d0d-473d-b8d2-9fe26835bb7d)
 Call ID: cf40af76-6d0d-473d-b8d2-9fe26835bb7d
  Args:
    type: :Person
    source: :Prince_Philip_Duke_of_Edinburgh
  AssignClass (c93ab401-9202-452d-b894-d3d557080e70)
 Call ID: c93ab401-9202-452d-b894-d3d557080e70
  Args:
    type: :Man
    source: :Prince_Philip_Duke_of_Edinburgh
  AddTriple (7a66e5cd-6b50-45aa-b60d-fa139674d687)
 Call ID: 7a66e5cd-6b50-45aa-b60d-fa139674d687
  Args:
    relation: :isSisterOf
    source: :Margarita_of_Greece_and_Denmark
    target: :Prince_Philip_Duke_of_Edinburgh
  AssignClass (0a2ceec0-2533-47c5-81a3-4c27d7784d4e)
 Call ID: 0a2ceec0-2533-47c5-81a3-4c27d7784d4e
  Args:
    type: :Person
    source: :King_Charles_III
  AssignClass (b498e8db-3f71-4806-94bd-02bb88d8d65d)
 Call ID: b498e8db-3f71-4806-94bd-02bb88d8d65d
  Args:
    source: :King_Charles_III
    type: :Man
  AssignClass (744ee7e6-19f0-48c2-bc11-71dbc09bef74)
 Call ID: 744ee7e6-19f0-48c2-bc11-71dbc09bef74
  Args:
    source: :Princess_Christina_of_Hesse
    type: :Person
  AssignClass (9a9648d1-0787-4448-87b0-e08b711cf936)
 Call ID: 9a9648d1-0787-4448-87b0-e08b711cf936
  Args:
    type: :Woman
    source: :Princess_Christina_of_Hesse
  AssignClass (123f6ccf-8ee1-421b-bd9b-17a550b21b12)
 Call ID: 123f6ccf-8ee1-421b-bd9b-17a550b21b12
  Args:
    source: :Maximilian_Hereditary_Prince_of_Baden
    type: :Person
  AssignClass (8191e193-796d-42b4-aa64-8ca4ff750ed5)
 Call ID: 8191e193-796d-42b4-aa64-8ca4ff750ed5
  Args:
    source: :Maximilian_Hereditary_Prince_of_Baden
    type: :Man
  AssignClass (7d0883a3-6e63-44d7-b068-26dfb2cdf757)
 Call ID: 7d0883a3-6e63-44d7-b068-26dfb2cdf757
  Args:
    source: :Archduchess_Valerie_of_Austria
    type: :Person
  AssignClass (bff57cb0-d777-4394-a5ed-12663855185d)
 Call ID: bff57cb0-d777-4394-a5ed-12663855185d
  Args:
    source: :Archduchess_Valerie_of_Austria
    type: :Woman
  AssignClass (3a5cd1f0-883a-4493-b6cd-044282e74e00)
 Call ID: 3a5cd1f0-883a-4493-b6cd-044282e74e00
  Args:
    source: :Margaret_Princess_of_Hesse_and_by_Rhine
    type: :Person
  AssignClass (4be4b051-89f7-49eb-bd86-4b8864a660bd)
 Call ID: 4be4b051-89f7-49eb-bd86-4b8864a660bd
  Args:
    source: :Margaret_Princess_of_Hesse_and_by_Rhine
    type: :Woman
  AssignClass (1c8a141e-48b7-4b30-801d-b2e20e6f4752)
 Call ID: 1c8a141e-48b7-4b30-801d-b2e20e6f4752
  Args:
    type: :Person
    source: :Princess_Cecilie
  AssignClass (4ad363b2-f876-494c-a8ee-56850bd87b92)
 Call ID: 4ad363b2-f876-494c-a8ee-56850bd87b92
  Args:
    source: :Princess_Cecilie
    type: :Woman
  Finish (bac2bfcb-1a13-488c-8a9b-6d81a267453c)
 Call ID: bac2bfcb-1a13-488c-8a9b-6d81a267453c
  Args: