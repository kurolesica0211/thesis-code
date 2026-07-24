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
  AssignClass (7636f957-c6c2-44f5-a331-79e4d2934da6)
 Call ID: 7636f957-c6c2-44f5-a331-79e4d2934da6
  Args:
    type: :Woman
    source: :LadyPamelaHicks
  AssignClass (82bc7e32-f308-496c-9f69-71b66ac40c7f)
 Call ID: 82bc7e32-f308-496c-9f69-71b66ac40c7f
  Args:
    type: :Person
    source: :LadyPamelaHicks
  AddLiteral (cf5cb7cf-729e-43a6-861d-27f28ce114f3)
 Call ID: cf5cb7cf-729e-43a6-861d-27f28ce114f3
  Args:
    relation: :hasBirthYear
    source: :LadyPamelaHicks
    literal_type: xsd:integer
    literal_value: 1929
  AssignClass (6feb6259-f09d-4f4e-ba81-4709c556d620)
 Call ID: 6feb6259-f09d-4f4e-ba81-4709c556d620
  Args:
    source: :LordLouisMountbatten
    type: :Man
  AssignClass (529a2aed-41e6-4cc7-914c-13f10cdff193)
 Call ID: 529a2aed-41e6-4cc7-914c-13f10cdff193
  Args:
    type: :Person
    source: :LordLouisMountbatten
  AssignClass (3f19be22-7796-4077-8432-ebd6329085b8)
 Call ID: 3f19be22-7796-4077-8432-ebd6329085b8
  Args:
    type: :Woman
    source: :EdwinaAshley
  AssignClass (c43376fb-4074-44f4-8cf8-d66363f45163)
 Call ID: c43376fb-4074-44f4-8cf8-d66363f45163
  Args:
    type: :Person
    source: :EdwinaAshley
  AddTriple (e3e1cfb4-bf55-4c33-8b73-7220fab4b5cb)
 Call ID: e3e1cfb4-bf55-4c33-8b73-7220fab4b5cb
  Args:
    source: :LadyPamelaHicks
    target: :LordLouisMountbatten
    relation: :hasFather
  AddTriple (5bfb4ae4-7a98-42fa-a82a-68ce5ed3053e)
 Call ID: 5bfb4ae4-7a98-42fa-a82a-68ce5ed3053e
  Args:
    target: :EdwinaAshley
    relation: :hasMother
    source: :LadyPamelaHicks
  AssignClass (0e3bc649-b531-49db-8d51-60b1f01f11c2)
 Call ID: 0e3bc649-b531-49db-8d51-60b1f01f11c2
  Args:
    type: :Woman
    source: :PatriciaKnatchbull
  AssignClass (baf73f5a-6cfa-48dd-89a9-4fc3387ab138)
 Call ID: baf73f5a-6cfa-48dd-89a9-4fc3387ab138
  Args:
    type: :Person
    source: :PatriciaKnatchbull
  AddTriple (fe364994-32d0-406e-8fe1-ac3cbbc2d1c9)
 Call ID: fe364994-32d0-406e-8fe1-ac3cbbc2d1c9
  Args:
    target: :PatriciaKnatchbull
    relation: :isSisterOf
    source: :LadyPamelaHicks
  AssignClass (a5b6bdf7-c1b1-4432-afbc-9b722f93982b)
 Call ID: a5b6bdf7-c1b1-4432-afbc-9b722f93982b
  Args:
    type: :Man
    source: :DavidNightingaleHicks
  AssignClass (1c1c5075-f197-4987-900a-69b575639d82)
 Call ID: 1c1c5075-f197-4987-900a-69b575639d82
  Args:
    type: :Person
    source: :DavidNightingaleHicks
  AddLiteral (39a85909-0dc3-4a30-ad49-925a90ad4b1a)
 Call ID: 39a85909-0dc3-4a30-ad49-925a90ad4b1a
  Args:
    source: :DavidNightingaleHicks
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1929
  AddLiteral (9c4812e4-99c7-419c-868a-6a1c3078a430)
 Call ID: 9c4812e4-99c7-419c-868a-6a1c3078a430
  Args:
    relation: :hasDeathYear
    source: :DavidNightingaleHicks
    literal_type: xsd:integer
    literal_value: 1998
  AssignClass (29dfcdbc-0750-497d-8881-a7253051902b)
 Call ID: 29dfcdbc-0750-497d-8881-a7253051902b
  Args:
    source: :HerbertHicks
    type: :Man
  AssignClass (aeb1d20a-0b7a-43e0-ba7a-bb50b0e45fbf)
 Call ID: aeb1d20a-0b7a-43e0-ba7a-bb50b0e45fbf
  Args:
    source: :HerbertHicks
    type: :Person
  AssignClass (4a6b9a01-b597-497e-ac61-0594100173d9)
 Call ID: 4a6b9a01-b597-497e-ac61-0594100173d9
  Args:
    source: :IrisElsiePlatten
    type: :Woman
  AssignClass (5564fd84-4ad6-48f7-b4e0-2f9b27ed52b7)
 Call ID: 5564fd84-4ad6-48f7-b4e0-2f9b27ed52b7
  Args:
    source: :IrisElsiePlatten
    type: :Person
  AddTriple (7102eecd-daa2-4e87-8d4e-9e2974aeab1b)
 Call ID: 7102eecd-daa2-4e87-8d4e-9e2974aeab1b
  Args:
    relation: :hasFather
    target: :HerbertHicks
    source: :DavidNightingaleHicks
  AddTriple (ac4274e6-78aa-46c6-9efc-d5ec38ccf1c3)
 Call ID: ac4274e6-78aa-46c6-9efc-d5ec38ccf1c3
  Args:
    target: :IrisElsiePlatten
    relation: :hasMother
    source: :DavidNightingaleHicks
  AssignClass (3eea9e9e-746e-4e58-be01-bd15f58744ae)
 Call ID: 3eea9e9e-746e-4e58-be01-bd15f58744ae
  Args:
    type: :Woman
    source: :IndiaHicks
  AssignClass (41f2d3af-2aa6-44ff-91c7-c7aba312cb89)
 Call ID: 41f2d3af-2aa6-44ff-91c7-c7aba312cb89
  Args:
    type: :Person
    source: :IndiaHicks
  AddTriple (42f5635e-7c5b-4e17-bd9a-6fad64f30c2b)
 Call ID: 42f5635e-7c5b-4e17-bd9a-6fad64f30c2b
  Args:
    source: :IndiaHicks
    relation: :isChildOf
    target: :LadyPamelaHicks
  AddTriple (ad31bb8b-3097-4700-b78e-c09ad678667d)
 Call ID: ad31bb8b-3097-4700-b78e-c09ad678667d
  Args:
    relation: :isChildOf
    target: :DavidNightingaleHicks
    source: :IndiaHicks
  AssignClass (750883b1-358b-427b-9efe-48e67c7774b3)
 Call ID: 750883b1-358b-427b-9efe-48e67c7774b3
  Args:
    type: :Man
    source: :PrinceLouisOfBattenberg
  AssignClass (73d723f2-83ac-4e46-a96b-04f09135fd6c)
 Call ID: 73d723f2-83ac-4e46-a96b-04f09135fd6c
  Args:
    source: :PrinceLouisOfBattenberg
    type: :Person
  AssignClass (702c3888-f63c-4b9f-bdf4-b3d0cab120e2)
 Call ID: 702c3888-f63c-4b9f-bdf4-b3d0cab120e2
  Args:
    type: :Woman
    source: :PrincessVictoriaOfHesse
  AssignClass (99a14c6d-6484-4ac3-9094-d4fd44e90710)
 Call ID: 99a14c6d-6484-4ac3-9094-d4fd44e90710
  Args:
    source: :PrincessVictoriaOfHesse
    type: :Person
  AddTriple (67ca7223-49fe-49a0-b7ab-5010a4536230)
 Call ID: 67ca7223-49fe-49a0-b7ab-5010a4536230
  Args:
    relation: :isFatherOf
    target: :LordLouisMountbatten
    source: :PrinceLouisOfBattenberg
  AddTriple (091e3064-859e-45d9-9ba0-dbe7a91dfe38)
 Call ID: 091e3064-859e-45d9-9ba0-dbe7a91dfe38
  Args:
    source: :PrincessVictoriaOfHesse
    target: :LordLouisMountbatten
    relation: :isMotherOf
  Finish (29a34a8b-bc9e-4487-b7fd-c023819738e6)
 Call ID: 29a34a8b-bc9e-4487-b7fd-c023819738e6
  Args: