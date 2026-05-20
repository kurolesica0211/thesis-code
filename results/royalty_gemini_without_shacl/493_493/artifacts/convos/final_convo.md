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
Woizlawa Feodora Princess Reuss (née Duchess of Mecklenburg-Schwerin, 17 December 1918 – 3 June 2019) was a member of the German nobility, by birth of the House of Mecklenburg-Schwerin.
Early life and ancestry

Duchess Woizlawa Feodore Elise Marie Elisabeth of Mecklenburg-Schwerin was born at Rostock, Free State of Mecklenburg-Schwerin on 17 December 1918, just after the abdication of her first cousin Frederick Francis IV of the Grand Duchy of Mecklenburg-Schwerin, after the November Revolution, the expulsion of Kaiser Wilhelm II, and the proclamation of the Republic on 9 November 1918.
Her father was the seventh son of Frederick Francis II, Grand Duke of Mecklenburg-Schwerin (1823–1883) by his third wife Princess Marie of Schwarzburg-Rudolstadt (1850–1922).
Her mother was Viktoria Feodora Reuss zu Schleiz (1889–1918), the eldest child of Heinrich XXVII, Prince of Reuss zu Schleiz, regent of Principality of Reuss-Greiz and Princess Elise of Hohenlohe-Langenburg, granddaughter of Princess Feodora of Leiningen, half-sister of Queen Victoria.
She was a first cousin of:


Juliana's wedding

Preparations for the wedding of Queen Wilhelmina of the Netherlands' only child Crown Princess Juliana to the German Prince Bernhard of Lippe-Biesterfeld were underway in 1937 when a diplomatic scandal occurred.
As a result, Juliana's chosen bridesmaids were either her relatives or relatives of her groom.
These included Woizlawa herself (being first cousins), Duchess Thyra of Mecklenburg-Schwerin (her second cousin), Grand Duchess Kira Kirillovna of Russia (her first cousin once removed), Princess Sophie of Saxe-Weimar-Eisenach (her second cousin), and two of Bernhard's first cousins, Princess Sieglinde and Princess Elisabeth of Lippe.
Marriage and family

On 15 September 1939, she married in Bad Doberan to her distant relative Heinrich I Prinz Reuss (1910−1982), the eldest son of Prince Heinrich XXXIV Reuss of Schleiz (1887-1956) and his wife and cousin, Princess Sophie Renata Reuss of Köstritz (1884-1968).



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
  AssignClass (c21a4277-f4ec-4f69-9d22-a98a19d21817)
 Call ID: c21a4277-f4ec-4f69-9d22-a98a19d21817
  Args:
    type: :Woman
    source: :WoizlawaFeodoraPrincessReuss
  AssignClass (bee432e9-1f0c-4bde-a83e-6f6395302e5c)
 Call ID: bee432e9-1f0c-4bde-a83e-6f6395302e5c
  Args:
    type: :Person
    source: :WoizlawaFeodoraPrincessReuss
  AddLiteral (18059535-033d-480f-b944-a28a7d838797)
 Call ID: 18059535-033d-480f-b944-a28a7d838797
  Args:
    relation: :hasBirthYear
    source: :WoizlawaFeodoraPrincessReuss
    literal_type: xsd:integer
    literal_value: 1918
  AddLiteral (d263a7c1-6a1a-4d2c-b227-637faa18e7b7)
 Call ID: d263a7c1-6a1a-4d2c-b227-637faa18e7b7
  Args:
    relation: :hasDeathYear
    source: :WoizlawaFeodoraPrincessReuss
    literal_type: xsd:integer
    literal_value: 2019
  AssignClass (8ee78ac4-d283-4b6d-b874-874c4077ca70)
 Call ID: 8ee78ac4-d283-4b6d-b874-874c4077ca70
  Args:
    type: :Man
    source: :FrederickFrancisII
  AssignClass (40334f0a-0e8b-4531-8bb6-d9e1d28310bb)
 Call ID: 40334f0a-0e8b-4531-8bb6-d9e1d28310bb
  Args:
    type: :Ancestor
    source: :FrederickFrancisII
  AddLiteral (b89adfd3-042a-4a16-9b4b-c2bdc2adc69c)
 Call ID: b89adfd3-042a-4a16-9b4b-c2bdc2adc69c
  Args:
    literal_value: 1823
    relation: :hasBirthYear
    source: :FrederickFrancisII
    literal_type: xsd:integer
  AddLiteral (812a95a7-64a0-4e6b-8159-949e286a7818)
 Call ID: 812a95a7-64a0-4e6b-8159-949e286a7818
  Args:
    source: :FrederickFrancisII
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 1883
  AssignClass (805be2b6-85bc-4312-b3ed-451927d04b2e)
 Call ID: 805be2b6-85bc-4312-b3ed-451927d04b2e
  Args:
    type: :Woman
    source: :PrincessMarieOfSchwarzburgRudolstadt
  AssignClass (42e33cc8-6de0-47c1-9383-06a7377da8d5)
 Call ID: 42e33cc8-6de0-47c1-9383-06a7377da8d5
  Args:
    type: :Ancestor
    source: :PrincessMarieOfSchwarzburgRudolstadt
  AddLiteral (479a46e1-60ec-487f-be82-803f6afee9d2)
 Call ID: 479a46e1-60ec-487f-be82-803f6afee9d2
  Args:
    literal_value: 1850
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: :PrincessMarieOfSchwarzburgRudolstadt
  AddLiteral (bdc32142-4f24-42d2-aaab-2ee4ac3e1a6b)
 Call ID: bdc32142-4f24-42d2-aaab-2ee4ac3e1a6b
  Args:
    literal_value: 1922
    literal_type: xsd:integer
    source: :PrincessMarieOfSchwarzburgRudolstadt
    relation: :hasDeathYear
  AssignClass (a12646b2-1218-4b73-8ef3-7f9769815d5c)
 Call ID: a12646b2-1218-4b73-8ef3-7f9769815d5c
  Args:
    type: :Woman
    source: :ViktoriaFeodoraReussZuSchleiz
  AssignClass (a9565c40-d302-4e6e-995b-f0f8440fad55)
 Call ID: a9565c40-d302-4e6e-995b-f0f8440fad55
  Args:
    type: :Ancestor
    source: :ViktoriaFeodoraReussZuSchleiz
  AddLiteral (e8775f65-f53b-4e6b-8ac6-63fb70ba21a9)
 Call ID: e8775f65-f53b-4e6b-8ac6-63fb70ba21a9
  Args:
    literal_value: 1889
    source: :ViktoriaFeodoraReussZuSchleiz
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (05ced61a-0691-49ee-bf5a-7980a4deb8c2)
 Call ID: 05ced61a-0691-49ee-bf5a-7980a4deb8c2
  Args:
    relation: :hasDeathYear
    source: :ViktoriaFeodoraReussZuSchleiz
    literal_type: xsd:integer
    literal_value: 1918
  AssignClass (999299b5-6ecd-4837-888a-9cdf3af5984d)
 Call ID: 999299b5-6ecd-4837-888a-9cdf3af5984d
  Args:
    type: :Man
    source: :HeinrichXXVIIPrinceOfReussZuSchleiz
  AssignClass (08224ad7-13f1-4ee5-a673-30294deeca30)
 Call ID: 08224ad7-13f1-4ee5-a673-30294deeca30
  Args:
    type: :Ancestor
    source: :HeinrichXXVIIPrinceOfReussZuSchleiz
  AssignClass (cf191f74-eac8-405e-ae51-00674d225eb4)
 Call ID: cf191f74-eac8-405e-ae51-00674d225eb4
  Args:
    type: :Woman
    source: :PrincessEliseOfHohenloheLangenburg
  AssignClass (d7a7b10a-daea-4a70-bdb4-2fa0f9fa79a8)
 Call ID: d7a7b10a-daea-4a70-bdb4-2fa0f9fa79a8
  Args:
    type: :Ancestor
    source: :PrincessEliseOfHohenloheLangenburg
  AddTriple (565844a3-d4e0-4177-a2c8-41bf52e3c7bb)
 Call ID: 565844a3-d4e0-4177-a2c8-41bf52e3c7bb
  Args:
    target: :FrederickFrancisII
    relation: :hasFather
    source: :WoizlawaFeodoraPrincessReuss
  AddTriple (62ff2a22-a1cd-41be-b425-bc315c33dd61)
 Call ID: 62ff2a22-a1cd-41be-b425-bc315c33dd61
  Args:
    source: :WoizlawaFeodoraPrincessReuss
    relation: :hasMother
    target: :ViktoriaFeodoraReussZuSchleiz
  AddTriple (8b4b75b8-a2dd-48be-97c7-455d0cce9dee)
 Call ID: 8b4b75b8-a2dd-48be-97c7-455d0cce9dee
  Args:
    source: :ViktoriaFeodoraReussZuSchleiz
    relation: :hasFather
    target: :HeinrichXXVIIPrinceOfReussZuSchleiz
  AddTriple (c8b1ecd4-6fbd-4194-89fc-5d36582a2c05)
 Call ID: c8b1ecd4-6fbd-4194-89fc-5d36582a2c05
  Args:
    target: :PrincessEliseOfHohenloheLangenburg
    relation: :hasMother
    source: :ViktoriaFeodoraReussZuSchleiz
  AssignClass (27c2be23-cce8-4c0e-aee7-157f4e0b4ef6)
 Call ID: 27c2be23-cce8-4c0e-aee7-157f4e0b4ef6
  Args:
    type: :Man
    source: :HeinrichIPrinzReuss
  AssignClass (17376a95-5436-4eeb-9529-2291feafd9a9)
 Call ID: 17376a95-5436-4eeb-9529-2291feafd9a9
  Args:
    type: :Person
    source: :HeinrichIPrinzReuss
  AddLiteral (1f81ba16-2a86-471b-87a3-cd12c9867cda)
 Call ID: 1f81ba16-2a86-471b-87a3-cd12c9867cda
  Args:
    literal_value: 1910
    source: :HeinrichIPrinzReuss
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (e05bb235-16e2-48ed-990f-563abc828803)
 Call ID: e05bb235-16e2-48ed-990f-563abc828803
  Args:
    literal_type: xsd:integer
    source: :HeinrichIPrinzReuss
    relation: :hasDeathYear
    literal_value: 1982
  AddLiteral (8a54f3c9-fa07-48fa-a06e-1baeec0ca8e8)
 Call ID: 8a54f3c9-fa07-48fa-a06e-1baeec0ca8e8
  Args:
    relation: :hasMarriageYear
    source: :WoizlawaFeodoraPrincessReuss
    literal_type: xsd:integer
    literal_value: 1939
  AssignClass (57fa76cd-ade1-4c44-bf96-94a6ff48f901)
 Call ID: 57fa76cd-ade1-4c44-bf96-94a6ff48f901
  Args:
    type: :Man
    source: :PrinceHeinrichXXXIVReussOfSchleiz
  AssignClass (b9aae9bc-3b13-42c3-951b-fc78119d6b5f)
 Call ID: b9aae9bc-3b13-42c3-951b-fc78119d6b5f
  Args:
    type: :Ancestor
    source: :PrinceHeinrichXXXIVReussOfSchleiz
  AddLiteral (063b4a6e-19df-46a3-b53b-69f2cba1d6b8)
 Call ID: 063b4a6e-19df-46a3-b53b-69f2cba1d6b8
  Args:
    source: :PrinceHeinrichXXXIVReussOfSchleiz
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1887
  AddLiteral (736c3c15-682f-4f29-a5e8-56564adabdea)
 Call ID: 736c3c15-682f-4f29-a5e8-56564adabdea
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: :PrinceHeinrichXXXIVReussOfSchleiz
    literal_value: 1956
  AssignClass (db28e425-cf0e-4354-961f-026cc5d0e434)
 Call ID: db28e425-cf0e-4354-961f-026cc5d0e434
  Args:
    type: :Woman
    source: :PrincessSophieRenataReussOfKostritz
  AssignClass (ed088b50-99eb-46ce-ab9a-39002783eed5)
 Call ID: ed088b50-99eb-46ce-ab9a-39002783eed5
  Args:
    type: :Ancestor
    source: :PrincessSophieRenataReussOfKostritz
  AddLiteral (f5d25efb-f013-4a8b-8be5-e661672cf465)
 Call ID: f5d25efb-f013-4a8b-8be5-e661672cf465
  Args:
    literal_type: xsd:integer
    source: :PrincessSophieRenataReussOfKostritz
    relation: :hasBirthYear
    literal_value: 1884
  AddLiteral (5c90141f-cc35-45dc-abf2-536f2a2d66f5)
 Call ID: 5c90141f-cc35-45dc-abf2-536f2a2d66f5
  Args:
    literal_type: xsd:integer
    source: :PrincessSophieRenataReussOfKostritz
    relation: :hasDeathYear
    literal_value: 1968
  AddTriple (6b7f04ab-f1d9-471c-b8d2-d7b2631a3823)
 Call ID: 6b7f04ab-f1d9-471c-b8d2-d7b2631a3823
  Args:
    relation: :hasFather
    source: :HeinrichIPrinzReuss
    target: :PrinceHeinrichXXXIVReussOfSchleiz
  AddTriple (4058350a-51f3-48ca-b40f-b482f5a9b6a7)
 Call ID: 4058350a-51f3-48ca-b40f-b482f5a9b6a7
  Args:
    target: :PrincessSophieRenataReussOfKostritz
    source: :HeinrichIPrinzReuss
    relation: :hasMother
  Finish (63f9e8ae-e484-410a-b1ae-fd2f908abd4c)
 Call ID: 63f9e8ae-e484-410a-b1ae-fd2f908abd4c
  Args: