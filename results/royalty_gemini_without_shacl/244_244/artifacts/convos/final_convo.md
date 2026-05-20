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
Lady Pamela Carmen Louise Hicks (née Mountbatten; born 19 April 1929) is a British aristocrat and relative of the British royal family.
Earl Mountbatten of Burma (formerly Prince Louis of Battenberg) and of heiress Edwina Ashley.
Through her father, Lady Pamela is a first cousin of the late Prince Philip, Duke of Edinburgh, and a grandniece of the last Empress of Russia, Alexandra Feodorovna.
She served as a bridesmaid and later as a lady-in-waiting to Queen Elizabeth II, her third cousin.
Early life and family

Lady Pamela was born on 19 April 1929 in Barcelona, Spain, to Edwina Ashley and the then Lord Louis Mountbatten (who later became The 1st Earl Mountbatten of Burma).
Countess Mountbatten of Burma.
A member of the Mountbatten family by birth, she descended from the Battenberg family, a morganatic cadet branch of the House of Hesse-Darmstadt.
At the request of King George V, her grandparents, Prince Louis of Battenberg and Princess Victoria of Hesse and by Rhine, relinquished their German princely titles in 1917 in exchange for titles in the British peerage due to anti-German sentiment in Britain.
Her father, who was also born a prince of Battenberg, was later created Earl Mountbatten of Burma.
Through her father, she is a great-great-granddaughter of Queen Victoria and Prince Albert of Saxe-Coburg and Gotha, and as of 2026, their oldest surviving descendant.
Her mother, Edwina, was the daughter of The 1st Baron Mount Temple.
Through her mother, Lady Pamela is also a great-granddaughter of Sir Ernest Cassel and a great-great-granddaughter of The 7th Earl of Shaftesbury.
Through her father, she is a first cousin of Prince Philip, Duke of Edinburgh.
Her baptism was celebrated on 12 July 1929 in the Chapel Royal, St. James's Palace.
Her godparents were: King Alfonso XIII and The Duke of Kent; Nadejda Mountbatten and Marjorie, Countess of Brecknock (Lady Louis' first cousin); and the Duchess of Peñaranda (María del Carmen Saavedra y Collado, Marqués de Villaviciosa)..
She attended Hewitt School in New York City, like her sister Patricia.
In 1947, Lady Pamela accompanied her parents to British India, remaining with them throughout her father's term as the last Viceroy of India and then as Governor-General of post-Partition India through 1948, living with them in the palatial Viceroy's House in New Delhi and at the summer Viceregal Lodge in Simla.
Official duties

In November 1947, Lady Pamela acted as a bridesmaid to then-Princess Elizabeth at her 1947 wedding to Prince Philip, Duke of Edinburgh.
As lady-in-waiting to Princess Elizabeth she was with her and the Duke of Edinburgh in Kenya when George VI died on 6 February 1952.
In late 1953 and early 1954, she accompanied the Queen as lady-in-waiting on the royal tour to Jamaica, Panama, Fiji, Tonga, New Zealand, Australia, Ceylon, Aden, Libya, Malta and Gibraltar.
Lady Pamela was the Corps Commandant of the Girls' Nautical Training Corps from around 1952 to around 1959.
She attended the wedding of Prince Edward, Duke of Kent and Katharine Worsley in 1961.
Marriage and children

Lady Pamela is the widow of interior decorator and designer David Nightingale Hicks (25 March 1929 – 29 March 1998), son of stockbroker Herbert Hicks and Iris Elsie Platten.
The bridesmaids were Princess Anne, Princess Clarissa of Hesse (daughter of her cousin Sophie), Victoria Marten (god-daughter of the bride), the Hon.
Amanda Knatchbull (daughters of the bride's sister Patricia).
Upon returning from honeymoon in the West Indies and New York, Lady Pamela learnt of the death of her mother in Jesselton in February 1960.
Together, the couple had three children:


David died on 29 March 1998, aged 69, from lung cancer.
According to their daughter India, two ladies who knew David had been invited to the Grove by him shortly before his death.
They were told by Lady Pamela that he had died a few hours ago (Hicks was lying ‘in state’ in his garden according to his instructions) but as they had driven from London, she invited them to have ‘a cup of tea’.
Later life

Lady Pamela has been a Director of H Securities Unlimited, a fund management and brokerage firm, since 1991.
In 2007, Lady Pamela published her memoirs of her days in New Delhi and Simla, when India was partitioned into India and Pakistan and the Union Jack came down.
She wrote in India Remembered: A Personal Account of the Mountbattens During the Transfer of Power that, while her mother, Countess Mountbatten of Burma, and Jawaharlal Nehru, the future Prime Minister of India, were deeply in love, "the relationship remained platonic", In 2012, she published the second volume of her memoirs titled Daughter of Empire:
Life as a Mountbatten, chronicling her childhood, her time in India, and her time as lady-in-waiting to the Queen.
After the death of her cousin, Prince Philip, Duke of Edinburgh in 2021, she is the last surviving great-grandchild of Princess Alice of the United Kingdom, and following the death of Queen Elizabeth II in September 2022, she became the oldest living descendant of Queen Victoria.
With her daughter, India Hicks, she attended the Queen's state funeral on 19 September 2022.



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
  AssignClass (1c479a6c-e3a4-468f-be8e-6e3d94d3d51d)
 Call ID: 1c479a6c-e3a4-468f-be8e-6e3d94d3d51d
  Args:
    type: :Woman
    source: Lady_Pamela_Hicks
  AssignClass (b5c348f8-e1a4-4988-92d4-d3bfbf063f2d)
 Call ID: b5c348f8-e1a4-4988-92d4-d3bfbf063f2d
  Args:
    source: Lady_Pamela_Hicks
    type: :Person
  AddLiteral (37393ef2-1c08-4393-a11d-84c787faa4f9)
 Call ID: 37393ef2-1c08-4393-a11d-84c787faa4f9
  Args:
    literal_type: xsd:integer
    source: Lady_Pamela_Hicks
    literal_value: 1929
    relation: :hasBirthYear
  AssignClass (95f1b466-d768-451f-afde-2fdd555cba1a)
 Call ID: 95f1b466-d768-451f-afde-2fdd555cba1a
  Args:
    type: :Man
    source: Louis_Mountbatten
  AssignClass (27fc33d1-2abd-45f7-b395-383b1c68f7f2)
 Call ID: 27fc33d1-2abd-45f7-b395-383b1c68f7f2
  Args:
    source: Louis_Mountbatten
    type: :Person
  AssignClass (87e7af25-982d-460c-9c85-67f56f355bf8)
 Call ID: 87e7af25-982d-460c-9c85-67f56f355bf8
  Args:
    source: Edwina_Ashley
    type: :Woman
  AssignClass (db9cc29b-95b6-493e-b166-6bfcdcb66724)
 Call ID: db9cc29b-95b6-493e-b166-6bfcdcb66724
  Args:
    type: :Person
    source: Edwina_Ashley
  AddTriple (3e88605b-8e44-4c7b-ac16-e989e48a6423)
 Call ID: 3e88605b-8e44-4c7b-ac16-e989e48a6423
  Args:
    relation: :hasFather
    source: Lady_Pamela_Hicks
    target: Louis_Mountbatten
  AddTriple (c96e5bac-7122-4467-b12b-9920defa15a5)
 Call ID: c96e5bac-7122-4467-b12b-9920defa15a5
  Args:
    source: Lady_Pamela_Hicks
    target: Edwina_Ashley
    relation: :hasMother
  AssignClass (7f26c393-cbfa-4767-85d1-692e328e8d2c)
 Call ID: 7f26c393-cbfa-4767-85d1-692e328e8d2c
  Args:
    type: :Woman
    source: Patricia_Knatchbull
  AssignClass (f5fbacc2-ebc9-4ddd-a2e7-f44cd1cdcdbc)
 Call ID: f5fbacc2-ebc9-4ddd-a2e7-f44cd1cdcdbc
  Args:
    source: Patricia_Knatchbull
    type: :Person
  AddTriple (0fb4d378-0a59-43ec-8dce-a95e109ad07e)
 Call ID: 0fb4d378-0a59-43ec-8dce-a95e109ad07e
  Args:
    relation: :isSisterOf
    target: Lady_Pamela_Hicks
    source: Patricia_Knatchbull
  AssignClass (09e9f468-d9de-44b0-ab7c-01c141521d55)
 Call ID: 09e9f468-d9de-44b0-ab7c-01c141521d55
  Args:
    source: David_Nightingale_Hicks
    type: :Man
  AssignClass (73f4aaaf-7ba7-4a89-94bc-0837ffa97015)
 Call ID: 73f4aaaf-7ba7-4a89-94bc-0837ffa97015
  Args:
    type: :Person
    source: David_Nightingale_Hicks
  AddLiteral (1ed88f13-bbd6-4415-9087-14fc6e523cee)
 Call ID: 1ed88f13-bbd6-4415-9087-14fc6e523cee
  Args:
    source: David_Nightingale_Hicks
    literal_type: xsd:integer
    literal_value: 1929
    relation: :hasBirthYear
  AddLiteral (10d81c2d-4338-4523-a987-2f3789afd537)
 Call ID: 10d81c2d-4338-4523-a987-2f3789afd537
  Args:
    relation: :hasDeathYear
    literal_value: 1998
    literal_type: xsd:integer
    source: David_Nightingale_Hicks
  AssignClass (4f1162bc-617d-491c-ba9e-9924410daad7)
 Call ID: 4f1162bc-617d-491c-ba9e-9924410daad7
  Args:
    type: :Man
    source: Herbert_Hicks
  AssignClass (d8053154-f304-41e1-be58-507931ae8a1d)
 Call ID: d8053154-f304-41e1-be58-507931ae8a1d
  Args:
    source: Herbert_Hicks
    type: :Person
  AssignClass (64e2d12a-dff9-4e8a-9808-64afe5b11d89)
 Call ID: 64e2d12a-dff9-4e8a-9808-64afe5b11d89
  Args:
    type: :Woman
    source: Iris_Elsie_Platten
  AssignClass (8876e2e8-2e4f-43e2-a068-a3b5cded07ca)
 Call ID: 8876e2e8-2e4f-43e2-a068-a3b5cded07ca
  Args:
    type: :Person
    source: Iris_Elsie_Platten
  AddTriple (36d32c00-ebbb-45a6-96c8-827da9032d59)
 Call ID: 36d32c00-ebbb-45a6-96c8-827da9032d59
  Args:
    target: Herbert_Hicks
    source: David_Nightingale_Hicks
    relation: :hasFather
  AddTriple (acef3622-c1c5-4ed8-a373-e1b30d2284ac)
 Call ID: acef3622-c1c5-4ed8-a373-e1b30d2284ac
  Args:
    target: Iris_Elsie_Platten
    source: David_Nightingale_Hicks
    relation: :hasMother
  AssignClass (bdbb5251-c8c4-4e98-bfe0-4cf9ca6ffd16)
 Call ID: bdbb5251-c8c4-4e98-bfe0-4cf9ca6ffd16
  Args:
    type: :Woman
    source: India_Hicks
  AssignClass (06f14338-3f06-4813-ab20-accdbad369e3)
 Call ID: 06f14338-3f06-4813-ab20-accdbad369e3
  Args:
    source: India_Hicks
    type: :Person
  AddTriple (66e00247-602b-474b-b058-f1b67373b336)
 Call ID: 66e00247-602b-474b-b058-f1b67373b336
  Args:
    source: India_Hicks
    target: Lady_Pamela_Hicks
    relation: :isDaughterOf
  AddTriple (fef8eb68-198a-4edc-9450-35a1db07c8c2)
 Call ID: fef8eb68-198a-4edc-9450-35a1db07c8c2
  Args:
    source: India_Hicks
    target: David_Nightingale_Hicks
    relation: :isDaughterOf
  AssignClass (2b60b01e-5c58-41f0-bd54-c78b4bdc38de)
 Call ID: 2b60b01e-5c58-41f0-bd54-c78b4bdc38de
  Args:
    source: Prince_Louis_of_Battenberg
    type: :Man
  AssignClass (b508eb21-ffb1-42c2-bfa6-f44a22040bdb)
 Call ID: b508eb21-ffb1-42c2-bfa6-f44a22040bdb
  Args:
    source: Prince_Louis_of_Battenberg
    type: :Person
  AssignClass (f7a33273-6371-44e6-a6c9-b69bd55a525f)
 Call ID: f7a33273-6371-44e6-a6c9-b69bd55a525f
  Args:
    source: Princess_Victoria_of_Hesse
    type: :Woman
  AssignClass (745edd33-7768-4fcc-9231-dc66cd57575a)
 Call ID: 745edd33-7768-4fcc-9231-dc66cd57575a
  Args:
    source: Princess_Victoria_of_Hesse
    type: :Person
  AddTriple (c04d58e9-2c0b-4340-a6b2-85dda24e19cf)
 Call ID: c04d58e9-2c0b-4340-a6b2-85dda24e19cf
  Args:
    target: Louis_Mountbatten
    source: Prince_Louis_of_Battenberg
    relation: :isFatherOf
  AddTriple (f8b5e160-2b4a-42de-89eb-11e34788bdff)
 Call ID: f8b5e160-2b4a-42de-89eb-11e34788bdff
  Args:
    target: Louis_Mountbatten
    source: Princess_Victoria_of_Hesse
    relation: :isMotherOf
  AssignClass (dde49188-8fd3-4234-9f03-b0246108a628)
 Call ID: dde49188-8fd3-4234-9f03-b0246108a628
  Args:
    type: :Man
    source: Baron_Mount_Temple
  AssignClass (55782a3d-be47-47ec-a1c7-9290ee800d67)
 Call ID: 55782a3d-be47-47ec-a1c7-9290ee800d67
  Args:
    source: Baron_Mount_Temple
    type: :Person
  AddTriple (012baa47-4739-415e-8dca-0cde81b76a38)
 Call ID: 012baa47-4739-415e-8dca-0cde81b76a38
  Args:
    source: Baron_Mount_Temple
    target: Edwina_Ashley
    relation: :isFatherOf
  Finish (7c8a0a7d-669e-41f2-a3dd-68de30f9202f)
 Call ID: 7c8a0a7d-669e-41f2-a3dd-68de30f9202f
  Args: