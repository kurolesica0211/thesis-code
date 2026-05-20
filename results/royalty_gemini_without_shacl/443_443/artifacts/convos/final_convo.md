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
Lady Elizabeth Georgiana Shakerley CVO (née Anson; 7 June 1941 – 1 November 2020) was a British party planner, writer and socialite from the Anson family.
She was a first cousin once removed of Queen Elizabeth II and sister of Patrick Anson, 5th Earl of Lichfield.
Early life

The Honourable Elizabeth Georgiana Anson was born on 7 June 1941 at Windsor Castle to Thomas Anson, Viscount Anson (1913–1958), and Anne Bowes-Lyon.
Shakerley's mother was a niece of Queen Elizabeth (later the Queen Mother).
She was the niece of Nerissa and Katherine Bowes-Lyon.
In 1960, her paternal grandfather, the 4th Earl of Lichfield, died and her brother, Patrick, inherited the title and family seat, Shugborough Hall near Great Haywood, Staffordshire.
Despite the estate's passing to the National Trust in lieu of death duties, Lord Lichfield maintained an apartment for himself and his sister.
Subsequently, her mother married Prince Georg of Denmark and moved to Paris where Prince Georg served as military, naval and air attaché.
Her father died in 1958 before acceding to the earldom of  Lichfield.
On 12 July 1961, Queen Elizabeth II issued a Royal Warrant of Precedence granting Shakerley the title, rank, place, pre-eminence and precedence of the daughter of an Earl as if her father had succeeded.
Thus, she became known as Lady Elizabeth Anson.
In 1966, Shakerley was a bridesmaid at the wedding of Princess Beatrix of the Netherlands and Claus van Amsberg.
Career

Following the stress of planning her own debutante ball in 1959, Lady Elizabeth founded the firm Party Planners in 1960.
From then on she planned parties for her cousin Queen Elizabeth II.
Even after her marriage, she continued to be known as Elizabeth Anson professionally.
In 1986, Shakerley published Lady Elizabeth Anson's Party Planners Book.
The courts eventually ruled in favour of Trump.


Notable events she planned include: Sting's 1992 wedding to Trudie Styler; Margaret Thatcher's 70th birthday party in 1995; Queen Elizabeth II's 80th and 90th birthday parties in 2006 and 2016, respectively; Crown Prince Pavlos of Greece's 1995 wedding to Marie-Chantal Miller; and a reception for foreign royal guests the night before the Prince William's 2011 wedding to Catherine Middleton.
In 2000, she planned three consecutive events for the royal family; Prince William's 18th birthday on 21 June, Princess Anne's 50th birthday on 15 August and Princess Margaret's 70th birthday on 21 August.
As the stepdaughter of a Danish prince, Shakerley also attended many royal events in continental Europe, including the birthday celebrations of the King Harald V of Norway (her stepfather's first cousin) and the funeral of Jean, Grand Duke of Luxembourg.
In 2018, Shakerley attended a state banquet given by Queen Elizabeth II in honour of the King and Queen of the Netherlands at Buckingham Palace.
Personal life and death

On 27 July 1972, Shakerley married Sir Geoffrey Shakerley, 6th Bt, at Westminster Abbey.
Guests at the wedding included Queen Elizabeth II, Queen Elizabeth the Queen Mother and Princess Beatrix of the Netherlands.
Her second cousins Princess Anne and Lady Sarah Armstrong-Jones were among her bridesmaids.
Lady Elizabeth and Shakerley separated in 1986 and divorced in 2009.
They had one daughter and two grandchildren:


Shakerley suffered from chronic fatigue syndrome.
She is buried in the Anson family vault at St Michael and All Angels Church, Colwich, Staffordshire, near Shugborough Hall.
The Countess of Wessex (representing Queen Elizabeth II), Princess Beatrix of the Netherlands and Sheikh Hamad bin Khalifa Al Thani of Qatar attended.



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
  AssignClass (a74780b5-0ad9-4ead-b20f-24cdb61e46eb)
 Call ID: a74780b5-0ad9-4ead-b20f-24cdb61e46eb
  Args:
    source: Lady_Elizabeth_Georgiana_Shakerley
    type: :Woman
  AssignClass (8272217c-1055-4db4-b898-605ef215453c)
 Call ID: 8272217c-1055-4db4-b898-605ef215453c
  Args:
    type: :Person
    source: Lady_Elizabeth_Georgiana_Shakerley
  AddLiteral (146ae82f-5ace-4afb-985f-139e15ae19c9)
 Call ID: 146ae82f-5ace-4afb-985f-139e15ae19c9
  Args:
    relation: :hasBirthYear
    literal_value: 1941
    literal_type: xsd:integer
    source: Lady_Elizabeth_Georgiana_Shakerley
  AddLiteral (3f4f787a-43eb-427c-9418-c01c94f2986b)
 Call ID: 3f4f787a-43eb-427c-9418-c01c94f2986b
  Args:
    relation: :hasDeathYear
    literal_value: 2020
    source: Lady_Elizabeth_Georgiana_Shakerley
    literal_type: xsd:integer
  AddLiteral (09725865-fc11-432d-9ddf-23d0e8faec53)
 Call ID: 09725865-fc11-432d-9ddf-23d0e8faec53
  Args:
    relation: :knownAs
    literal_value: Lady Elizabeth Anson
    literal_type: xsd:string
    source: Lady_Elizabeth_Georgiana_Shakerley
  AssignClass (07db5409-02ab-459b-9838-f624cc105409)
 Call ID: 07db5409-02ab-459b-9838-f624cc105409
  Args:
    source: Thomas_Anson_Viscount_Anson
    type: :Man
  AssignClass (f6ecde3a-1f2e-4af8-b004-ecbea9548f79)
 Call ID: f6ecde3a-1f2e-4af8-b004-ecbea9548f79
  Args:
    type: :Person
    source: Thomas_Anson_Viscount_Anson
  AssignClass (e6025cc0-83e4-472e-8f97-ea83682ba532)
 Call ID: e6025cc0-83e4-472e-8f97-ea83682ba532
  Args:
    type: :Ancestor
    source: Thomas_Anson_Viscount_Anson
  AddLiteral (e7da594d-8365-4c89-b1c1-4ed33df6595c)
 Call ID: e7da594d-8365-4c89-b1c1-4ed33df6595c
  Args:
    source: Thomas_Anson_Viscount_Anson
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1913
  AddLiteral (ac402aa8-c0ed-4401-a1bb-e0b68e8a38a4)
 Call ID: ac402aa8-c0ed-4401-a1bb-e0b68e8a38a4
  Args:
    source: Thomas_Anson_Viscount_Anson
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1958
  AssignClass (4169eb0a-e924-4b7a-b14c-15794fc0e244)
 Call ID: 4169eb0a-e924-4b7a-b14c-15794fc0e244
  Args:
    source: Anne_Bowes-Lyon
    type: :Woman
  AssignClass (729d0285-a909-490a-90a7-0d577a7c72d8)
 Call ID: 729d0285-a909-490a-90a7-0d577a7c72d8
  Args:
    type: :Person
    source: Anne_Bowes-Lyon
  AssignClass (642d15e2-d176-41a5-9ee4-35144cbc2f28)
 Call ID: 642d15e2-d176-41a5-9ee4-35144cbc2f28
  Args:
    source: Anne_Bowes-Lyon
    type: :Ancestor
  AddTriple (2004f6a3-620a-4955-94de-cd60f7984aea)
 Call ID: 2004f6a3-620a-4955-94de-cd60f7984aea
  Args:
    target: Thomas_Anson_Viscount_Anson
    relation: :hasFather
    source: Lady_Elizabeth_Georgiana_Shakerley
  AddTriple (fb0ee514-1396-478c-92b0-2ae39735eacd)
 Call ID: fb0ee514-1396-478c-92b0-2ae39735eacd
  Args:
    source: Lady_Elizabeth_Georgiana_Shakerley
    target: Anne_Bowes-Lyon
    relation: :hasMother
  AssignClass (339bcdba-7b2e-4bf4-9fd1-36038f3f775f)
 Call ID: 339bcdba-7b2e-4bf4-9fd1-36038f3f775f
  Args:
    source: Patrick_Anson_5th_Earl_of_Lichfield
    type: :Man
  AssignClass (2363d481-945f-4134-ae41-9b9e3ae5927c)
 Call ID: 2363d481-945f-4134-ae41-9b9e3ae5927c
  Args:
    type: :Person
    source: Patrick_Anson_5th_Earl_of_Lichfield
  AddTriple (36effb4c-8eeb-4d45-b994-bf88c2c17499)
 Call ID: 36effb4c-8eeb-4d45-b994-bf88c2c17499
  Args:
    source: Lady_Elizabeth_Georgiana_Shakerley
    target: Patrick_Anson_5th_Earl_of_Lichfield
    relation: :hasBrother
  AssignClass (83323291-fbc8-4d4d-90e9-4cc0735784c4)
 Call ID: 83323291-fbc8-4d4d-90e9-4cc0735784c4
  Args:
    type: :Man
    source: Sir_Geoffrey_Shakerley_6th_Bt
  AssignClass (8ab856da-3331-497e-b011-1185118b34a5)
 Call ID: 8ab856da-3331-497e-b011-1185118b34a5
  Args:
    type: :Person
    source: Sir_Geoffrey_Shakerley_6th_Bt
  AddLiteral (abc7473e-5710-4c9d-85e5-8c00c6712895)
 Call ID: abc7473e-5710-4c9d-85e5-8c00c6712895
  Args:
    literal_value: 1972
    relation: :hasMarriageYear
    source: Lady_Elizabeth_Georgiana_Shakerley
    literal_type: xsd:integer
  Finish (8a1042dd-4b05-4d25-9d82-d7b49071f57e)
 Call ID: 8a1042dd-4b05-4d25-9d82-d7b49071f57e
  Args: