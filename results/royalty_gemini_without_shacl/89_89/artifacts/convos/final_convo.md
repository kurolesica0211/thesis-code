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
Prince Nicholas of Greece and Denmark (Greek: Νικόλαος, romanized: Nikólaos; 22 January 1872 – 8 February 1938) was the fourth child and third son of King George I of Greece, and of Queen Olga.
He was known as "Greek Nicky" within the family to distinguish him from his cousin Emperor Nicholas II of Russia (first cousin on the paternal side and second cousin on the maternal side).
Prince Nicholas was a talented painter, often signing his works as "Nicolas Leprince".
Marriage and issue

He married Grand Duchess Elena Vladimirovna of Russia (1882–1957), daughter of Grand Duke Vladimir Alexandrovich of Russia and Marie of Mecklenburg-Schwerin, the only sister of the future Russian imperial pretender, Grand Duke Kirill Vladimirovich, and his second cousin through his mother Olga Constantinovna of Russia and her father Grand Duke Vladimir Alexandrovich of Russia, on 29 August 1902 in Tsarskoye Selo, Russia.
Residence in Athens

Nicholas' marriage significantly improved his own financial position; his wife Elena received the customary imperial dowry of a Russian Grand Duchess, amounting to 1,000,000 roubles.
The dowry capital was held in Russia, from which Elena was paid an annual income of 50,000 roubles.
After their marriage the couple resided in Athens; in late 1902 they purchased a large house near the city centre, which was thereafter known as the Nicholas Palace.
Prince and Princess Nicholas took up residence at the newly-renovated Nicholas Palace in 1904.
The advent of the Russian Revolution in 1917 and the exile of the Greek Royal Family in 1923 had a significant impact on the couple's income, and as a result the Nicholas Palace was leased to the Hotel Grande Bretagne during the 1920s, who used the building as a 60-bed luxury annex known as the “Petit Palais”.
The Italian Government later purchased the Nicholas Palace from the widowed Princess Nicholas in 1955; the site has subsequently remained the home of the Italian Embassy in Athens ever since.
Public life

Along with his elder brothers Constantine and George, Nicholas helped to organize the 1896 Summer Olympics in Athens, the first to be held since 393.
Nicholas served as president of the Sub-Committee for Shooting.
His father bequeathed him the Royal Theater of Greece which Nicholas, in turn, transferred to the Greek state in 1935.
He was friends with George Simitis and was godfather to his son, future socialist Prime Minister Kostas Simitis.
Death and burial

Prince Nicholas died in Athens on February 8, 1938 and was buried in the Royal tomb at the Palace of Tatoi.



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
  AssignClass (ab366eaa-cc08-4373-a99c-f5f0ca7803c2)
 Call ID: ab366eaa-cc08-4373-a99c-f5f0ca7803c2
  Args:
    type: :Man
    source: :PrinceNicholasOfGreeceAndDenmark
  AssignClass (deb1d5cb-1812-451e-a122-bbf09d12765a)
 Call ID: deb1d5cb-1812-451e-a122-bbf09d12765a
  Args:
    type: :Person
    source: :PrinceNicholasOfGreeceAndDenmark
  AddLiteral (1b4bde85-bf20-4ea0-91a0-9c8e22eec330)
 Call ID: 1b4bde85-bf20-4ea0-91a0-9c8e22eec330
  Args:
    relation: :hasSex
    literal_type: xsd:string
    source: :PrinceNicholasOfGreeceAndDenmark
    literal_value: male
  AddLiteral (70c07024-d66c-4812-a0fc-ae23c83e6eb3)
 Call ID: 70c07024-d66c-4812-a0fc-ae23c83e6eb3
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: :PrinceNicholasOfGreeceAndDenmark
    literal_value: 1872
  AddLiteral (b561cd25-a999-47fe-b51d-dc825670a86a)
 Call ID: b561cd25-a999-47fe-b51d-dc825670a86a
  Args:
    literal_type: xsd:integer
    source: :PrinceNicholasOfGreeceAndDenmark
    literal_value: 1938
    relation: :hasDeathYear
  AddLiteral (eacb55d7-9dcc-43e4-9d3a-0d5012ec5449)
 Call ID: eacb55d7-9dcc-43e4-9d3a-0d5012ec5449
  Args:
    relation: :knownAs
    literal_type: xsd:string
    source: :PrinceNicholasOfGreeceAndDenmark
    literal_value: Greek Nicky
  AddLiteral (0a19d827-eb3f-4db7-b1ea-0a2d5f207d0f)
 Call ID: 0a19d827-eb3f-4db7-b1ea-0a2d5f207d0f
  Args:
    relation: :alsoKnownAs
    literal_value: Nicolas Leprince
    literal_type: xsd:string
    source: :PrinceNicholasOfGreeceAndDenmark
  AssignClass (83d37450-0141-4886-bf30-09deac14562a)
 Call ID: 83d37450-0141-4886-bf30-09deac14562a
  Args:
    type: :Man
    source: :KingGeorgeIOfGreece
  AssignClass (2f934c18-ba8d-470c-ae87-914ea246a095)
 Call ID: 2f934c18-ba8d-470c-ae87-914ea246a095
  Args:
    type: :Person
    source: :KingGeorgeIOfGreece
  AddTriple (a91cd2e1-27ee-44e4-b56a-96acc8c3f70c)
 Call ID: a91cd2e1-27ee-44e4-b56a-96acc8c3f70c
  Args:
    source: :PrinceNicholasOfGreeceAndDenmark
    relation: :hasFather
    target: :KingGeorgeIOfGreece
  AssignClass (dc8d73af-bd11-4fe5-a96c-c0a5f4e57e93)
 Call ID: dc8d73af-bd11-4fe5-a96c-c0a5f4e57e93
  Args:
    type: :Woman
    source: :QueenOlga
  AssignClass (8af7c475-3325-4ce0-9f3a-388f4738f50e)
 Call ID: 8af7c475-3325-4ce0-9f3a-388f4738f50e
  Args:
    type: :Person
    source: :QueenOlga
  AddTriple (f6eebc11-e46a-48f9-96b2-4bb73f48da19)
 Call ID: f6eebc11-e46a-48f9-96b2-4bb73f48da19
  Args:
    source: :PrinceNicholasOfGreeceAndDenmark
    relation: :hasMother
    target: :QueenOlga
  AssignClass (26371bc7-d4fa-42a9-a778-17cd9c10f7a2)
 Call ID: 26371bc7-d4fa-42a9-a778-17cd9c10f7a2
  Args:
    type: :Woman
    source: :GrandDuchessElenaVladimirovnaOfRussia
  AssignClass (2acbb289-8833-4739-9d30-1775533f1ef4)
 Call ID: 2acbb289-8833-4739-9d30-1775533f1ef4
  Args:
    type: :Person
    source: :GrandDuchessElenaVladimirovnaOfRussia
  AddLiteral (7d53aaa0-c731-41ce-b1ef-0b73c8b559fa)
 Call ID: 7d53aaa0-c731-41ce-b1ef-0b73c8b559fa
  Args:
    relation: :hasBirthYear
    source: :GrandDuchessElenaVladimirovnaOfRussia
    literal_type: xsd:integer
    literal_value: 1882
  AddLiteral (801cd580-bfbe-4b8c-817b-0fd0e5712d56)
 Call ID: 801cd580-bfbe-4b8c-817b-0fd0e5712d56
  Args:
    literal_value: 1957
    literal_type: xsd:integer
    source: :GrandDuchessElenaVladimirovnaOfRussia
    relation: :hasDeathYear
  AddLiteral (5769ff09-1a1a-4ec3-9171-f7dcd7be3ea9)
 Call ID: 5769ff09-1a1a-4ec3-9171-f7dcd7be3ea9
  Args:
    literal_type: xsd:integer
    source: :PrinceNicholasOfGreeceAndDenmark
    literal_value: 1902
    relation: :hasMarriageYear
  AssignClass (ff5e1f98-718f-4f12-a107-32dfb676acb9)
 Call ID: ff5e1f98-718f-4f12-a107-32dfb676acb9
  Args:
    type: :Man
    source: :GrandDukeVladimirAlexandrovichOfRussia
  AssignClass (1ffb3381-2e4d-4e78-a851-d2e3304a6079)
 Call ID: 1ffb3381-2e4d-4e78-a851-d2e3304a6079
  Args:
    type: :Person
    source: :GrandDukeVladimirAlexandrovichOfRussia
  AddTriple (a21fc1b1-adce-4a42-93e9-b7d8f264fa8f)
 Call ID: a21fc1b1-adce-4a42-93e9-b7d8f264fa8f
  Args:
    source: :GrandDuchessElenaVladimirovnaOfRussia
    relation: :hasFather
    target: :GrandDukeVladimirAlexandrovichOfRussia
  AssignClass (603456fe-8564-4581-a0b6-4aed628c88a0)
 Call ID: 603456fe-8564-4581-a0b6-4aed628c88a0
  Args:
    type: :Woman
    source: :MarieOfMecklenburgSchwerin
  AssignClass (0f90235d-80a5-47c9-9c09-1ba4dcb74659)
 Call ID: 0f90235d-80a5-47c9-9c09-1ba4dcb74659
  Args:
    type: :Person
    source: :MarieOfMecklenburgSchwerin
  AddTriple (c38cdcf6-e9be-4dae-bedf-4555c44e5133)
 Call ID: c38cdcf6-e9be-4dae-bedf-4555c44e5133
  Args:
    relation: :hasMother
    source: :GrandDuchessElenaVladimirovnaOfRussia
    target: :MarieOfMecklenburgSchwerin
  AssignClass (edb367eb-fee2-4162-aa6d-d54187738005)
 Call ID: edb367eb-fee2-4162-aa6d-d54187738005
  Args:
    type: :Man
    source: :GrandDukeKirillVladimirovich
  AssignClass (ceedb238-8916-4935-9c88-5081b52c3db0)
 Call ID: ceedb238-8916-4935-9c88-5081b52c3db0
  Args:
    type: :Person
    source: :GrandDukeKirillVladimirovich
  AddTriple (89a41ced-3b53-4a8a-bfbe-34650daefd3b)
 Call ID: 89a41ced-3b53-4a8a-bfbe-34650daefd3b
  Args:
    source: :GrandDuchessElenaVladimirovnaOfRussia
    relation: :isSisterOf
    target: :GrandDukeKirillVladimirovich
  AssignClass (dab4b2b0-a23f-4c03-b9e5-e2fe5b1bfbec)
 Call ID: dab4b2b0-a23f-4c03-b9e5-e2fe5b1bfbec
  Args:
    type: :Man
    source: :Constantine
  AssignClass (bbc687cb-f0b6-4550-8122-293f5053daed)
 Call ID: bbc687cb-f0b6-4550-8122-293f5053daed
  Args:
    type: :Person
    source: :Constantine
  AddTriple (7ea27a04-4076-4682-882d-9d42e9941642)
 Call ID: 7ea27a04-4076-4682-882d-9d42e9941642
  Args:
    source: :PrinceNicholasOfGreeceAndDenmark
    relation: :isBrotherOf
    target: :Constantine
  AssignClass (19d5c5c5-4a95-4642-a0f8-2193989dec00)
 Call ID: 19d5c5c5-4a95-4642-a0f8-2193989dec00
  Args:
    type: :Man
    source: :George
  AssignClass (437bdd37-b262-450e-8aa3-85de1ef139b5)
 Call ID: 437bdd37-b262-450e-8aa3-85de1ef139b5
  Args:
    type: :Person
    source: :George
  AddTriple (8b9f125b-b639-497a-b71b-705eb50cbe8e)
 Call ID: 8b9f125b-b639-497a-b71b-705eb50cbe8e
  Args:
    relation: :isBrotherOf
    source: :PrinceNicholasOfGreeceAndDenmark
    target: :George
  AssignClass (8d3f7d77-afd1-467a-9152-fba7aaa22011)
 Call ID: 8d3f7d77-afd1-467a-9152-fba7aaa22011
  Args:
    type: :Man
    source: :GeorgeSimitis
  AssignClass (54a05938-c5a1-4c96-8357-b9f2db55d0aa)
 Call ID: 54a05938-c5a1-4c96-8357-b9f2db55d0aa
  Args:
    type: :Person
    source: :GeorgeSimitis
  AssignClass (3ac1224a-6235-4849-a2d9-3e2fdff3dcc7)
 Call ID: 3ac1224a-6235-4849-a2d9-3e2fdff3dcc7
  Args:
    type: :Man
    source: :KostasSimitis
  AssignClass (c0a19240-416a-4762-82d3-360480496ca2)
 Call ID: c0a19240-416a-4762-82d3-360480496ca2
  Args:
    type: :Person
    source: :KostasSimitis
  AddTriple (c0f82a7f-fea0-491b-811d-c9048a715a98)
 Call ID: c0f82a7f-fea0-491b-811d-c9048a715a98
  Args:
    source: :KostasSimitis
    relation: :hasFather
    target: :GeorgeSimitis
  Finish (10052f18-5c9d-4410-8b7c-b9d3dde2fc57)
 Call ID: 10052f18-5c9d-4410-8b7c-b9d3dde2fc57
  Args: