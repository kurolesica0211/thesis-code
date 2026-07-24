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
@prefix ns1: <http://www.w3.org/2003/11/swrl#> .
@prefix ns2: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
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

:hasDeathYear a owl:AnnotationProperty .

:hasMarriageYear a owl:AnnotationProperty .

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

ns2:isRuleEnabled a owl:AnnotationProperty .

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

:isAncestorOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation .

:isSisterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf .

:hasChild a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:inverseOf :isChildOf .

:hasParent a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Person ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:equivalentProperty :isChildOf ;
    owl:inverseOf :isParentOf .

:isSiblingOf a owl:ObjectProperty,
        owl:SymmetricProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isBloodrelationOf ;
    owl:propertyChainAxiom ( :hasParent :isParentOf ) .

:Sex a owl:Class ;
    rdfs:subClassOf :DomainEntity ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Female :Male ) ] .

:isChildOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:propertyDisjointWith :isSisterOf .

:x a ns1:Variable .

:Man a owl:Class ;
    owl:disjointWith :Sex,
        :Woman ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Male ] ) ] .

:isParentOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:propertyDisjointWith :isSisterOf .

:Woman a owl:Class ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Female ] ) ] .

:y a ns1:Variable .

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

[] a ns1:Imp ;
    rdfs:label "infer hasSon" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasBrother" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasSister" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (bbdc6240-2600-4d6b-9272-f7121abb8c01)
 Call ID: bbdc6240-2600-4d6b-9272-f7121abb8c01
  Args:
    type: :Woman
    source: Lady_Pamela_Hicks
  AssignClass (3a00329f-b4c3-41a2-96e6-0cfc5ece0c37)
 Call ID: 3a00329f-b4c3-41a2-96e6-0cfc5ece0c37
  Args:
    type: :Woman
    source: Edwina_Ashley
  AssignClass (4ccd4d88-7154-4af4-87fa-d4d5f1f64620)
 Call ID: 4ccd4d88-7154-4af4-87fa-d4d5f1f64620
  Args:
    type: :Man
    source: Louis_Mountbatten
  AssignClass (0e0bdc9e-afd4-4c34-b22a-f7b34fba46da)
 Call ID: 0e0bdc9e-afd4-4c34-b22a-f7b34fba46da
  Args:
    type: :Man
    source: David_Nightingale_Hicks
  AssignClass (acc8549b-b999-43df-92fd-ab887b72e091)
 Call ID: acc8549b-b999-43df-92fd-ab887b72e091
  Args:
    type: :Man
    source: Herbert_Hicks
  AssignClass (a292895d-6aee-4065-85f4-051fc8981333)
 Call ID: a292895d-6aee-4065-85f4-051fc8981333
  Args:
    type: :Woman
    source: Iris_Elsie_Platten
  AssignClass (fa449b6c-a2ce-4d64-952f-a8dab927c379)
 Call ID: fa449b6c-a2ce-4d64-952f-a8dab927c379
  Args:
    type: :Woman
    source: Patricia_Mountbatten
  AssignClass (61d4d0fc-21b7-4ab7-9142-fbab237a64bc)
 Call ID: 61d4d0fc-21b7-4ab7-9142-fbab237a64bc
  Args:
    type: :Woman
    source: India_Hicks
  AssignClass (e9552b3d-f6f5-45e1-9e7f-98f2f4eea56e)
 Call ID: e9552b3d-f6f5-45e1-9e7f-98f2f4eea56e
  Args:
    type: :Man
    source: Prince_Louis_of_Battenberg
  AssignClass (a8c175e5-43db-4ce0-b918-f1a1a028de75)
 Call ID: a8c175e5-43db-4ce0-b918-f1a1a028de75
  Args:
    type: :Woman
    source: Princess_Victoria_of_Hesse
  AssignClass (f5d8e763-d1da-4296-ba65-028ec73ab5e1)
 Call ID: f5d8e763-d1da-4296-ba65-028ec73ab5e1
  Args:
    type: :Man
    source: Baron_Mount_Temple
  AddLiteral (9e07e2ea-269f-4bc4-9eb1-88288fd2fa3e)
 Call ID: 9e07e2ea-269f-4bc4-9eb1-88288fd2fa3e
  Args:
    literal_type: xsd:positiveInteger
    relation: :hasBirthYear
    literal_value: 1929
    source: Lady_Pamela_Hicks
  AddLiteral (ef0bb3f3-b144-458d-a93b-6a2c031de523)
 Call ID: ef0bb3f3-b144-458d-a93b-6a2c031de523
  Args:
    literal_value: 1929
    relation: :hasBirthYear
    literal_type: xsd:positiveInteger
    source: David_Nightingale_Hicks
  AddLiteral (1d90d146-6e63-48e1-a7cd-3440eff98e7d)
 Call ID: 1d90d146-6e63-48e1-a7cd-3440eff98e7d
  Args:
    literal_value: 1998
    relation: :hasDeathYear
    literal_type: xsd:positiveInteger
    source: David_Nightingale_Hicks
  AddTriple (d7fc376d-2f51-4616-8af9-44d2f2ffe074)
 Call ID: d7fc376d-2f51-4616-8af9-44d2f2ffe074
  Args:
    target: Louis_Mountbatten
    relation: :hasFather
    source: Lady_Pamela_Hicks
  AddTriple (38ccf883-ff19-43c1-8926-1d802c831fda)
 Call ID: 38ccf883-ff19-43c1-8926-1d802c831fda
  Args:
    relation: :hasMother
    target: Edwina_Ashley
    source: Lady_Pamela_Hicks
  AddTriple (3b122fbc-73ed-4f32-b65c-7fee7db18f24)
 Call ID: 3b122fbc-73ed-4f32-b65c-7fee7db18f24
  Args:
    target: Herbert_Hicks
    relation: :hasFather
    source: David_Nightingale_Hicks
  AddTriple (0817153c-d13a-4d69-a6a3-29ede51363a1)
 Call ID: 0817153c-d13a-4d69-a6a3-29ede51363a1
  Args:
    source: David_Nightingale_Hicks
    target: Iris_Elsie_Platten
    relation: :hasMother
  AddTriple (c3cfc959-b43d-4ac3-9a4a-17aa8b36455d)
 Call ID: c3cfc959-b43d-4ac3-9a4a-17aa8b36455d
  Args:
    source: Louis_Mountbatten
    relation: :hasFather
    target: Prince_Louis_of_Battenberg
  AddTriple (0dc1cf82-7c8d-4a41-a5e2-d98c5dd494af)
 Call ID: 0dc1cf82-7c8d-4a41-a5e2-d98c5dd494af
  Args:
    source: Louis_Mountbatten
    target: Princess_Victoria_of_Hesse
    relation: :hasMother
  AddTriple (af54de3d-d739-48c9-8739-424cf8e9b3bc)
 Call ID: af54de3d-d739-48c9-8739-424cf8e9b3bc
  Args:
    source: Edwina_Ashley
    relation: :hasFather
    target: Baron_Mount_Temple
  AddTriple (33ac8969-8afb-4ad6-bf5a-fdac177db3c7)
 Call ID: 33ac8969-8afb-4ad6-bf5a-fdac177db3c7
  Args:
    source: Lady_Pamela_Hicks
    relation: :hasSister
    target: Patricia_Mountbatten
  AddTriple (a35d214e-aa6e-49ce-be32-7491fa55fb4c)
 Call ID: a35d214e-aa6e-49ce-be32-7491fa55fb4c
  Args:
    source: India_Hicks
    target: Lady_Pamela_Hicks
    relation: :hasMother
  Finish (81852f0e-d9fc-44d7-be90-d0faa66b91a3)
 Call ID: 81852f0e-d9fc-44d7-be90-d0faa66b91a3
  Args: