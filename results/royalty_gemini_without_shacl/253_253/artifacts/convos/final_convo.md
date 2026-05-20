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
George Henry Hubert Lascelles, 7th Earl of Harewood (7 February 1923 – 11 July 2011), styled The Honourable George Lascelles before 1929 and Viscount Lascelles between 1929 and 1947, was a British classical music administrator and author, and a member of the extended British royal family, as a maternal grandson of King George V and Queen Mary, and thus a first cousin of Queen Elizabeth II.
Harewood was the elder son of the 6th Earl of Harewood and Princess Mary, Princess Royal, the only daughter of King George V and Queen Mary.
Lord Harewood was the eldest grandchild of King George V and Queen Mary, nephew of both King Edward VIII and King George VI and first cousin of Queen Elizabeth II.
He was the first member of the Royal Family to obtain a divorce (as opposed to an annulment).
he was the director of the Edinburgh Festival from 1961-1965


Early life

George Henry Hubert Lascelles was born at his parents' London home of Chesterfield House on 7 February 1923, the first child of Henry, Viscount Lascelles, and Princess Mary, Viscountess Lascelles, and first grandchild of King George V and Queen Mary, who stood as sponsors at his christening.
The christening took place on 25 March 1923 at St Mary's Church in the village of Goldsborough, near Knaresborough adjoining the family home Goldsborough Hall.
After his paternal grandfather's death in 1929, he was styled as Viscount Lascelles as his father succeeded to the earldom.
He served as a Page of Honour at the coronation of his uncle King George VI in May 1937.
He was raised at Harewood House in Yorkshire.
Military service

Lascelles joined the British Army where he was commissioned as a second lieutenant into the Grenadier Guards (his father's regiment) in 1942, attaining the rank of captain.
As the nephew of King George VI, Lascelles was one of the Prominente at Colditz, considered a potential bargaining chip by the Nazis.
— Lord Harewood, Desert Island Discs, 1982
In March 1945, Adolf Hitler signed his death warrant; the SS general in command of prisoner-of-war camps, Gottlob Berger, realizing the war was lost, refused to carry out the sentence and released Lascelles to the Swiss.
Lord Harewood served as a Counsellor of State in 1947, 1953–54, and 1956.
House of Lords

Lascelles succeeded his father in 1947.
Career

Opera

A music enthusiast, Lord Harewood devoted most of his career to opera with his Yorkshire heritage fostering his interest; in March 1949, as a young single man, he had been among the audience at the Leeds Town Hall for a  performance of operatic works by the Yorkshire Symphony Orchestra.
He was director of the Royal Opera House, Covent Garden from 1951 to 1953 and again from 1969 to 1972.
Lord Harewood served as a governor of the BBC from 1985 to 1987 and as the president of the British Board of Film Classification from 1985 to 1996.
Public life

Lascelles was the only person to serve as Counsellor of State without being a Prince of the United Kingdom, serving from 1945 to 1951, then from 1952 to 1956.
The estate and house, Harewood House, are held by a charity with £9 million of assets, and were not counted as part of his wealth.
Honours

Queen Elizabeth II created him a Knight Commander of the Order of the British Empire (KBE) in the Queen's Birthday Honours List on 13 June 1986.
In 1959, Harewood received the Grand Decoration in Silver with Sash for Services to the Republic of Austria.
Personal life

Marriages and children

On 29 September 1949 at St. Mark's Church, London, Lord Harewood married Marion Stein, a concert pianist and the daughter of the Viennese music publisher Erwin Stein.
Because of Harewood's position in the line of succession, the marriage was subject to approval from the sovereign, under the Royal Marriages Act 1772.
Queen Mary, mother of George VI, objected to the marriage but permission was eventually granted.
Benjamin Britten, a friend of the Stein family, composed an anthem, "Amo Ergo Sum", for the wedding ceremony.
Lord and Lady Harewood had three sons:


The earl's marriage to Marion Stein ended in divorce in 1967, after the earl's mistress, Patricia "Bambi" Tuckwell – an Australian violinist and sister of the musician Barry Tuckwell – gave birth to his son.
Stein went on to marry politician Jeremy Thorpe.
Lord Harewood married Tuckwell (24 November 1926 – 4 May 2018) on 31 July 1967.
They were obliged to be married abroad as, in England, registry office marriages were barred at the time for persons covered by the Royal Marriages Act, and divorcees could not marry in the Church of England.
They had one son: Mark Lascelles.
Death

Lord Harewood died peacefully at home, on 11 July 2011, aged 88 years.
Arms

Books

The Tongs and the Bones: The Memoirs of Lord Harewood, published by George Weidenfeld & Nicolson (1981), .mw-parser-output cite.citation{font-style:inherit;word-wrap:break-word}.mw-parser-output .citation q{quotes:"\"""\"""'""'"}.mw-parser-output .citation:target{background-color:rgba(0,127,255,0.133)}.mw-parser-output .id-lock-free.id-lock-free a{background:url("//upload.wikimedia.org/wikipedia/commons/6/65/Lock-green.svg")right 0.1em center/9px no-repeat}.mw-parser-output .id-lock-limited.id-lock-limited a,.mw-parser-output .id-lock-registration.id-lock-registration a{background:url("//upload.wikimedia.org/wikipedia/commons/d/d6/Lock-gray-alt-2.svg")right 0.1em center/9px no-repeat}.mw-parser-output .id-lock-subscription.id-lock-subscription a{background:url("//upload.wikimedia.org/wikipedia/commons/a/aa/Lock-red-alt-2.svg")right 0.1em center/9px no-repeat}.mw-parser-output .cs1-ws-icon a{background:url("//upload.wikimedia.org/wikipedia/commons/4/4c/Wikisource-logo.svg")right 0.1em center/12px no-repeat}body:not(.skin-timeless):not(.skin-minerva) .mw-parser-output .id-lock-free a,body:not(.skin-timeless):not(.skin-minerva) .mw-parser-output .id-lock-limited a,body:not(.skin-timeless):not(.skin-minerva) .mw-parser-output .id-lock-registration a,body:not(.skin-timeless):not(.skin-minerva) .mw-parser-output .id-lock-subscription a,body:not(.skin-timeless):not(.skin-minerva) .mw-parser-output .cs1-ws-icon a{background-size:contain;padding:0 1em 0 0}.mw-parser-output .cs1-code{color:inherit;background:inherit;border:none;padding:inherit}.mw-parser-output .cs1-hidden-error{display:none;color:var(--color-error,#bf3c2c)}.mw-parser-output .cs1-visible-error{color:var(--color-error,#bf3c2c)}.mw-parser-output .cs1-maint{display:none;color:#085;margin-left:0.3em}.mw-parser-output .cs1-kern-left{padding-left:0.2em}.mw-parser-output .cs1-kern-right{padding-right:0.2em}.mw-parser-output .citation .mw-selflink{font-weight:inherit}@media screen{.mw-parser-output .cs1-format{font-size:95%}html.skin-theme-clientpref-night .mw-parser-output .cs1-maint{color:#18911f}}@media screen and (prefers-color-scheme:dark){html.skin-theme-clientpref-os .mw-parser-output .cs1-maint{color:#18911f}}ISBN 0-297-77960-5 is George Lascelles's autobiography.



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
  AssignClass (223bf7d6-6584-4811-82ca-1c08ea1941be)
 Call ID: 223bf7d6-6584-4811-82ca-1c08ea1941be
  Args:
    source: George_Henry_Hubert_Lascelles
    type: :Man
  AssignClass (2fadba6d-20e6-483e-8183-e9755db26af6)
 Call ID: 2fadba6d-20e6-483e-8183-e9755db26af6
  Args:
    type: :Person
    source: George_Henry_Hubert_Lascelles
  AddLiteral (bc7265c7-e403-4bd9-a796-9065cc47378f)
 Call ID: bc7265c7-e403-4bd9-a796-9065cc47378f
  Args:
    source: George_Henry_Hubert_Lascelles
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1923
  AddLiteral (96fed020-7d13-489c-9928-c2c3465c303c)
 Call ID: 96fed020-7d13-489c-9928-c2c3465c303c
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 2011
    source: George_Henry_Hubert_Lascelles
  AssignClass (154ca2da-e750-4a63-bf08-c571ab4be7ca)
 Call ID: 154ca2da-e750-4a63-bf08-c571ab4be7ca
  Args:
    type: :Man
    source: Henry_Viscount_Lascelles
  AssignClass (92bc30af-33f8-416e-9526-6a6328e77393)
 Call ID: 92bc30af-33f8-416e-9526-6a6328e77393
  Args:
    type: :Person
    source: Henry_Viscount_Lascelles
  AssignClass (95ca6cbf-9f73-429d-85c1-af79afd057a9)
 Call ID: 95ca6cbf-9f73-429d-85c1-af79afd057a9
  Args:
    type: :Woman
    source: Princess_Mary_Princess_Royal
  AssignClass (6245366b-c27c-40f1-bcfe-d38c52e7d049)
 Call ID: 6245366b-c27c-40f1-bcfe-d38c52e7d049
  Args:
    source: Princess_Mary_Princess_Royal
    type: :Person
  AddTriple (eeb2eaf0-493a-4487-830e-18ef46b2efe9)
 Call ID: eeb2eaf0-493a-4487-830e-18ef46b2efe9
  Args:
    relation: :hasFather
    target: Henry_Viscount_Lascelles
    source: George_Henry_Hubert_Lascelles
  AddTriple (0d911139-bc2e-45d5-ba55-4c7a478b61f1)
 Call ID: 0d911139-bc2e-45d5-ba55-4c7a478b61f1
  Args:
    target: Princess_Mary_Princess_Royal
    relation: :hasMother
    source: George_Henry_Hubert_Lascelles
  AssignClass (9c03532f-b986-4210-9658-c56554f95726)
 Call ID: 9c03532f-b986-4210-9658-c56554f95726
  Args:
    source: King_George_V
    type: :Man
  AssignClass (0c5ececc-afd1-460b-b82d-4654a82b64f1)
 Call ID: 0c5ececc-afd1-460b-b82d-4654a82b64f1
  Args:
    source: King_George_V
    type: :Person
  AssignClass (c4a62f2e-a9ce-4eb6-b7c0-6081bcb8596c)
 Call ID: c4a62f2e-a9ce-4eb6-b7c0-6081bcb8596c
  Args:
    type: :Woman
    source: Queen_Mary
  AssignClass (5e5a4208-37f6-4543-9cfa-58995c4750d2)
 Call ID: 5e5a4208-37f6-4543-9cfa-58995c4750d2
  Args:
    type: :Person
    source: Queen_Mary_ consort_of_George_V
  AddTriple (c39cfdc8-9281-46a4-a3e3-a3cd6e098f5f)
 Call ID: c39cfdc8-9281-46a4-a3e3-a3cd6e098f5f
  Args:
    relation: :hasFather
    target: King_George_V
    source: Princess_Mary_Princess_Royal
  AddTriple (d398d186-c8ef-46c1-bc40-df300b7c3181)
 Call ID: d398d186-c8ef-46c1-bc40-df300b7c3181
  Args:
    source: Princess_Mary_Princess_Royal
    target: Queen_Mary
    relation: :hasMother
  AssignClass (d3c5c66d-7a83-4266-a745-4562515e49b2)
 Call ID: d3c5c66d-7a83-4266-a745-4562515e49b2
  Args:
    source: Marion_Stein
    type: :Woman
  AssignClass (a7d31b89-baba-4df0-80b7-fad69558eb2c)
 Call ID: a7d31b89-baba-4df0-80b7-fad69558eb2c
  Args:
    type: :Person
    source: Marion_Stein
  AddTriple (b11f82fc-e815-40ba-a946-335a54978946)
 Call ID: b11f82fc-e815-40ba-a946-335a54978946
  Args:
    relation: :hasRelation
    target: Marion_Stein
    source: George_Henry_Hubert_Lascelles
  AddLiteral (568c3606-a8ee-4a7e-907d-4ad69f296313)
 Call ID: 568c3606-a8ee-4a7e-907d-4ad69f296313
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 1949
    source: George_Henry_Hubert_Lascelles
  AssignClass (494a9d4c-58b4-4b58-a5fe-61ba49691ed7)
 Call ID: 494a9d4c-58b4-4b58-a5fe-61ba49691ed7
  Args:
    source: Patricia_Tuckwell
    type: :Woman
  AssignClass (83149a93-d9b8-4030-a7ee-9970bec5fe4e)
 Call ID: 83149a93-d9b8-4030-a7ee-9970bec5fe4e
  Args:
    type: :Person
    source: Patricia_Tuckwell
  AddTriple (27b07f21-038e-49b9-b6a0-3fb0493915e7)
 Call ID: 27b07f21-038e-49b9-b6a0-3fb0493915e7
  Args:
    source: George_Henry_Hubert_Lascelles
    relation: :hasRelation
    target: Patricia_Tuckwell
  AddLiteral (cd3a354b-d3ef-4810-8407-3a80b8da8dcc)
 Call ID: cd3a354b-d3ef-4810-8407-3a80b8da8dcc
  Args:
    source: George_Henry_Hubert_Lascelles
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 1967
  AssignClass (80b3faa1-8044-4d98-9649-d3b256654417)
 Call ID: 80b3faa1-8044-4d98-9649-d3b256654417
  Args:
    source: Mark_Lascelles
    type: :Man
  AssignClass (bf97fef6-60f7-4ef4-9e72-e8d4d377910d)
 Call ID: bf97fef6-60f7-4ef4-9e72-e8d4d377910d
  Args:
    type: :Person
    source: Mark_Lascelles
  AddTriple (6e9f1117-3547-4661-949d-fdc9774b7ca3)
 Call ID: 6e9f1117-3547-4661-949d-fdc9774b7ca3
  Args:
    source: Mark_Lascelles
    target: George_Henry_Hubert_Lascelles
    relation: :hasFather
  AddTriple (af28e34a-2bb3-4354-b3f1-4a8d16e07a30)
 Call ID: af28e34a-2bb3-4354-b3f1-4a8d16e07a30
  Args:
    source: Mark_Lascelles
    target: Patricia_Tuckwell
    relation: :hasMother
  Finish (0119ba61-3245-4727-a0dd-71298dd283d8)
 Call ID: 0119ba61-3245-4727-a0dd-71298dd283d8
  Args: