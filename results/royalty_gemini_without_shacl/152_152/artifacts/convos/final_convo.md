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
Princess María de las Mercedes of Bourbon-Two Sicilies (.mw-parser-output .IPA-label-small{font-size:85%}.mw-parser-output .references .IPA-label-small,.mw-parser-output .infobox .IPA-label-small,.mw-parser-output .navbox .IPA-label-small{font-size:100%}Spanish: ; María de las Mercedes Cristina Genara Isabel Luisa Carolina Victoria y Todos los Santos de Borbón y Orléans; 23 December 1910 – 2 January 2000) was a member of the Spanish royal family and the mother of King Juan Carlos I.


The daughter of Prince Carlos of Bourbon-Two Sicilies and Princess Louise of Orléans, she married Infante Juan, Count of Barcelona, claimant to the Spanish throne.
Biography

María was born in Madrid, daughter of Prince Carlos of Bourbon-Two Sicilies, Infante of Spain, a grandson of King Ferdinand II of the Two Sicilies, and his second wife, Princess Louise of Orléans, daughter of Prince Philippe, Count of Paris, a pretender to the French throne.
She was granted, at birth, the rank and precedence of an infanta of Spain, although not the actual use of the title, her own being Princess of Bourbon-Two Sicilies.
When the Second Spanish Republic forced them into exile, they lived in Cannes and later in Paris, where she studied art at the Louvre.
On 14 January 1935, she attended the wedding, in Rome, of Infanta Beatriz of Spain, daughter of King Alfonso XIII, to Alessandro Torlonia, 5th Prince of Civitella-Cesi.
There she met the brother of the bride, her third cousin and future husband, the Infante Juan, fourth son and designated heir of Alfonso XIII.
When her husband took up Count of Barcelona as a title of pretence on 8 March 1941, María became the Countess of Barcelona.
They lived in Cannes and Rome, and, with the outbreak of World War II, they moved to Lausanne to live with Queen Victoria Eugenie, the mother of Infante Juan.
In 1953, the Countess represented the Spanish Royal Family at the coronation of Queen Elizabeth II.
In 1976, one year after the monarchy was restored in Spain in the person of her son, Juan Carlos, they returned to Spain.
She mediated between her son and her husband, estranged since Juan Carlos had been designated heir by Franco.
In 1977, Juan renounced his rights in favour of their son, who officially allowed him to retain the title of Count of Barcelona.
In 1995, her granddaughter Infanta Elena married in Seville in part because the Countess' love for the city.



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
  AssignClass (d66a315e-6cee-461f-9340-935284e445d3)
 Call ID: d66a315e-6cee-461f-9340-935284e445d3
  Args:
    source: :MariaDeLasMercedes
    type: :Woman
  AssignClass (f7b224d0-fb28-462e-a878-122ffddafdd7)
 Call ID: f7b224d0-fb28-462e-a878-122ffddafdd7
  Args:
    source: :MariaDeLasMercedes
    type: :Person
  AssignClass (5eeb1cf0-5255-4f1c-b617-ef2156fbeb70)
 Call ID: 5eeb1cf0-5255-4f1c-b617-ef2156fbeb70
  Args:
    source: :CarlosOfBourbonTwoSicilies
    type: :Man
  AssignClass (0ddfd5b9-62c3-4ca7-8fc5-026d7f3dd374)
 Call ID: 0ddfd5b9-62c3-4ca7-8fc5-026d7f3dd374
  Args:
    source: :CarlosOfBourbonTwoSicilies
    type: :Person
  AssignClass (00c271cd-9374-4946-a0f1-a348cae348d8)
 Call ID: 00c271cd-9374-4946-a0f1-a348cae348d8
  Args:
    type: :Woman
    source: :LouiseOfOrleans
  AssignClass (5a823010-5868-433c-8f10-b8b648bad066)
 Call ID: 5a823010-5868-433c-8f10-b8b648bad066
  Args:
    source: :LouiseOfOrleans
    type: :Person
  AssignClass (9182c65a-743f-445e-8b3e-7aa09fa82468)
 Call ID: 9182c65a-743f-445e-8b3e-7aa09fa82468
  Args:
    type: :Man
    source: :JuanCarlosI
  AssignClass (cf72e35e-29e6-485b-9b44-81c32d395517)
 Call ID: cf72e35e-29e6-485b-9b44-81c32d395517
  Args:
    type: :Person
    source: :JuanCarlosI
  AssignClass (ede1a313-d568-4153-be30-ffde34a34462)
 Call ID: ede1a313-d568-4153-be30-ffde34a34462
  Args:
    source: :JuanCountOfBarcelona
    type: :Man
  AssignClass (a7cc3e65-84ad-42ff-9116-1641d1589e88)
 Call ID: a7cc3e65-84ad-42ff-9116-1641d1589e88
  Args:
    type: :Person
    source: :JuanCountOfBarcelona
  AssignClass (8a4733c3-dd83-453b-a87d-e3a1c5de3a88)
 Call ID: 8a4733c3-dd83-453b-a87d-e3a1c5de3a88
  Args:
    source: :FerdinandII
    type: :Man
  AssignClass (0798bb89-a516-446b-a47f-4ff4545ff0d2)
 Call ID: 0798bb89-a516-446b-a47f-4ff4545ff0d2
  Args:
    source: :FerdinandII
    type: :Person
  AssignClass (adf77565-02de-4ff5-b2bf-5a9cdb24a962)
 Call ID: adf77565-02de-4ff5-b2bf-5a9cdb24a962
  Args:
    type: :Man
    source: :PhilippeCountOfParis
  AssignClass (07bc2e7e-d3cf-4b85-bc6e-cf69c26dacc3)
 Call ID: 07bc2e7e-d3cf-4b85-bc6e-cf69c26dacc3
  Args:
    type: :Person
    source: :PhilippeCountOfParis
  AssignClass (4b1e4904-fd6b-4cd0-b89c-826a58c7db02)
 Call ID: 4b1e4904-fd6b-4cd0-b89c-826a58c7db02
  Args:
    source: :BeatrizOfSpain
    type: :Woman
  AssignClass (74b4bc41-8df0-4205-b663-3226d0e1a604)
 Call ID: 74b4bc41-8df0-4205-b663-3226d0e1a604
  Args:
    source: :BeatrizOfSpain
    type: :Person
  AssignClass (3d7adfad-a092-4ae9-be93-e2c584e8f077)
 Call ID: 3d7adfad-a092-4ae9-be93-e2c584e8f077
  Args:
    source: :AlfonsoXIII
    type: :Man
  AssignClass (48e09b0d-db98-422e-aac3-155f7539fc86)
 Call ID: 48e09b0d-db98-422e-aac3-155f7539fc86
  Args:
    source: :AlfonsoXIII
    type: :Person
  AssignClass (5a759308-b052-415f-bc1b-f441c5b071ca)
 Call ID: 5a759308-b052-415f-bc1b-f441c5b071ca
  Args:
    type: :Man
    source: :AlessandroTorlonia
  AssignClass (0d4bb21d-ebfc-4feb-9618-06e7c19f9f57)
 Call ID: 0d4bb21d-ebfc-4feb-9618-06e7c19f9f57
  Args:
    source: :AlessandroTorlonia
    type: :Person
  AssignClass (1df7d4d8-486c-4f3b-b1d5-5eddce24d3e2)
 Call ID: 1df7d4d8-486c-4f3b-b1d5-5eddce24d3e2
  Args:
    source: :VictoriaEugenie
    type: :Woman
  AssignClass (78f56827-1b78-4f3a-9de4-773281d5723d)
 Call ID: 78f56827-1b78-4f3a-9de4-773281d5723d
  Args:
    type: :Person
    source: :VictoriaEugenie
  AssignClass (7b298998-8738-4dba-afa8-d4391599cd13)
 Call ID: 7b298998-8738-4dba-afa8-d4391599cd13
  Args:
    type: :Woman
    source: :Elena
  AssignClass (5e596c8c-f5ff-453f-a23a-cb166f988e69)
 Call ID: 5e596c8c-f5ff-453f-a23a-cb166f988e69
  Args:
    source: :Elena
    type: :Person
  AddLiteral (2b2b138f-e05c-49fb-a52a-d12207cb9ff5)
 Call ID: 2b2b138f-e05c-49fb-a52a-d12207cb9ff5
  Args:
    source: :MariaDeLasMercedes
    literal_type: xsd:integer
    literal_value: 1910
    relation: :hasBirthYear
  AddLiteral (de7b65b8-b0e9-4a9f-86c3-5edce0e5e0ff)
 Call ID: de7b65b8-b0e9-4a9f-86c3-5edce0e5e0ff
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: :MariaDeLasMercedes
    literal_value: 2000
  AddTriple (8259600c-ca59-4529-a13e-cbfa9bc5ba90)
 Call ID: 8259600c-ca59-4529-a13e-cbfa9bc5ba90
  Args:
    source: :MariaDeLasMercedes
    target: :LouiseOfOrleans
    relation: :hasMother
  AddTriple (9464e897-cf90-4f98-a952-151f94547249)
 Call ID: 9464e897-cf90-4f98-a952-151f94547249
  Args:
    source: :MariaDeLasMercedes
    target: :CarlosOfBourbonTwoSicilies
    relation: :hasFather
  AddTriple (57d25abd-f5f3-461c-a954-b4d7ec3179c4)
 Call ID: 57d25abd-f5f3-461c-a954-b4d7ec3179c4
  Args:
    relation: :isMotherOf
    target: :JuanCarlosI
    source: :MariaDeLasMercedes
  AddTriple (cbd0ca0f-276f-499d-94f3-678870b74db3)
 Call ID: cbd0ca0f-276f-499d-94f3-678870b74db3
  Args:
    relation: :isFatherOf
    target: :JuanCarlosI
    source: :JuanCountOfBarcelona
  AddTriple (fb8e5ff5-6e14-47ec-b5f7-5fb399124fa4)
 Call ID: fb8e5ff5-6e14-47ec-b5f7-5fb399124fa4
  Args:
    target: :CarlosOfBourbonTwoSicilies
    relation: :isFatherOf
    source: :FerdinandII
  AddTriple (5c2fcb61-eb8f-467d-9fd2-a1c40b41c486)
 Call ID: 5c2fcb61-eb8f-467d-9fd2-a1c40b41c486
  Args:
    source: :PhilippeCountOfParis
    target: :LouiseOfOrleans
    relation: :isFatherOf
  AddTriple (fae7b906-8c04-439c-9d45-8a949fe347aa)
 Call ID: fae7b906-8c04-439c-9d45-8a949fe347aa
  Args:
    relation: :isFatherOf
    target: :BeatrizOfSpain
    source: :AlfonsoXIII
  AddTriple (b4be18f1-fd32-4a98-9d7c-67a7ee49546f)
 Call ID: b4be18f1-fd32-4a98-9d7c-67a7ee49546f
  Args:
    relation: :isFatherOf
    target: :JuanCountOfBarcelona
    source: :AlfonsoXIII
  AddTriple (0525465d-24b9-4581-a969-7acbac2af115)
 Call ID: 0525465d-24b9-4581-a969-7acbac2af115
  Args:
    source: :VictoriaEugenie
    target: :JuanCountOfBarcelona
    relation: :isMotherOf
  AddTriple (e0d7d194-0957-497a-82c2-5c57428b539c)
 Call ID: e0d7d194-0957-497a-82c2-5c57428b539c
  Args:
    relation: :isMotherOf
    target: :Elena
    source: :MariaDeLasMercedes
  AddTriple (859ce146-3d08-4afd-9626-72fc45f5a2df)
 Call ID: 859ce146-3d08-4afd-9626-72fc45f5a2df
  Args:
    source: :BeatrizOfSpain
    target: :JuanCountOfBarcelona
    relation: :isSisterOf
  Finish (fde5bb31-b430-4fd4-8610-3c329f39d570)
 Call ID: fde5bb31-b430-4fd4-8610-3c329f39d570
  Args: