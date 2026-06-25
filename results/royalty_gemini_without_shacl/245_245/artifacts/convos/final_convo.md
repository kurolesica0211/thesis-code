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
  AssignClass (91967bd1-8f58-4e7b-99d0-6475a05f6058)
 Call ID: 91967bd1-8f58-4e7b-99d0-6475a05f6058
  Args:
    type: :Person
    source: Pamela_Hicks
  AssignClass (db5ff49d-0732-447c-9f29-7fe4a1fd2f4c)
 Call ID: db5ff49d-0732-447c-9f29-7fe4a1fd2f4c
  Args:
    source: Pamela_Hicks
    type: :Woman
  AddLiteral (5408ab70-ef9b-427e-a3d7-71c3287b7e3c)
 Call ID: 5408ab70-ef9b-427e-a3d7-71c3287b7e3c
  Args:
    source: Pamela_Hicks
    literal_value: 1929
    literal_type: xsd:integer
    relation: :hasBirthYear
  AssignClass (7b5925c3-cb84-42b8-bea6-af05d28312a7)
 Call ID: 7b5925c3-cb84-42b8-bea6-af05d28312a7
  Args:
    type: :Person
    source: Louis_Mountbatten
  AssignClass (11d03346-8c17-4efe-99c5-a4af8cc5635b)
 Call ID: 11d03346-8c17-4efe-99c5-a4af8cc5635b
  Args:
    source: Louis_Mountbatten
    type: :Man
  AssignClass (e426f5e5-1dd8-4f33-af65-9c9356429b96)
 Call ID: e426f5e5-1dd8-4f33-af65-9c9356429b96
  Args:
    type: :Person
    source: Edwina_Ashley
  AssignClass (f95fd06a-aaf7-40dc-a60f-ec8fdfced3a0)
 Call ID: f95fd06a-aaf7-40dc-a60f-ec8fdfced3a0
  Args:
    type: :Woman
    source: Edwina_Ashley
  AddTriple (bb828153-4a40-4760-8dd0-08cdc9ec52d2)
 Call ID: bb828153-4a40-4760-8dd0-08cdc9ec52d2
  Args:
    relation: :hasFather
    target: Louis_Mountbatten
    source: Pamela_Hicks
  AddTriple (9c2cd896-ff35-41ea-a25c-65308775fb11)
 Call ID: 9c2cd896-ff35-41ea-a25c-65308775fb11
  Args:
    target: Edwina_Ashley
    source: Pamela_Hicks
    relation: :hasMother
  AssignClass (10ceaf25-a10d-4df4-aad6-94d7ee73f9df)
 Call ID: 10ceaf25-a10d-4df4-aad6-94d7ee73f9df
  Args:
    type: :Person
    source: Patricia_Mountbatten
  AssignClass (d9dc90e9-07d0-4464-8e80-b9e663055a16)
 Call ID: d9dc90e9-07d0-4464-8e80-b9e663055a16
  Args:
    type: :Woman
    source: Patricia_Mountbatten
  AddTriple (89467cd9-680b-4176-949b-9b7ec817eb83)
 Call ID: 89467cd9-680b-4176-949b-9b7ec817eb83
  Args:
    target: Patricia_Mountbatten
    source: Pamela_Hicks
    relation: :hasSister
  AssignClass (533184fd-ac7c-4472-a752-7861e2269a46)
 Call ID: 533184fd-ac7c-4472-a752-7861e2269a46
  Args:
    type: :Person
    source: David_Nightingale_Hicks
  AssignClass (a50cef2c-954c-43fa-bb61-abcfb576474e)
 Call ID: a50cef2c-954c-43fa-bb61-abcfb576474e
  Args:
    source: David_Nightingale_Hicks
    type: :Man
  AddLiteral (0a861e1d-2f31-4cc0-8c60-83455102479a)
 Call ID: 0a861e1d-2f31-4cc0-8c60-83455102479a
  Args:
    source: David_Nightingale_Hicks
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1929
  AddLiteral (a2f5b7c2-eb3b-4bed-87e5-e45b86eaeedd)
 Call ID: a2f5b7c2-eb3b-4bed-87e5-e45b86eaeedd
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 1998
    source: David_Nightingale_Hicks
  AssignClass (0d0382b3-aefb-4ba2-a4cb-12df6fca9de3)
 Call ID: 0d0382b3-aefb-4ba2-a4cb-12df6fca9de3
  Args:
    type: :Person
    source: Herbert_Hicks
  AssignClass (3166cfb5-b40e-46d6-a6ae-e7ab1bcf6f73)
 Call ID: 3166cfb5-b40e-46d6-a6ae-e7ab1bcf6f73
  Args:
    type: :Man
    source: Herbert_Hicks
  AssignClass (175ef0dd-cbea-41f5-a9c7-daf4f48a79e9)
 Call ID: 175ef0dd-cbea-41f5-a9c7-daf4f48a79e9
  Args:
    source: Iris_Elsie_Platten
    type: :Person
  AssignClass (d6a8fead-7fe4-4a60-8882-491f6a6d8a83)
 Call ID: d6a8fead-7fe4-4a60-8882-491f6a6d8a83
  Args:
    source: Iris_Elsie_Platten
    type: :Woman
  AddTriple (645d9946-2d67-44bd-a941-d1d2ad632964)
 Call ID: 645d9946-2d67-44bd-a941-d1d2ad632964
  Args:
    source: David_Nightingale_Hicks
    target: Herbert_Hicks
    relation: :hasFather
  AddTriple (1eb133b0-e6a7-4f45-93b1-6feb1b295afd)
 Call ID: 1eb133b0-e6a7-4f45-93b1-6feb1b295afd
  Args:
    relation: :hasMother
    target: Iris_Elsie_Platten
    source: David_Nightingale_Hicks
  AssignClass (791b1909-c236-4b8b-a10c-f6b3a76ec906)
 Call ID: 791b1909-c236-4b8b-a10c-f6b3a76ec906
  Args:
    source: India_Hicks
    type: :Person
  AssignClass (d1f4a643-81ae-4ae0-b86c-8b8db38e5f95)
 Call ID: d1f4a643-81ae-4ae0-b86c-8b8db38e5f95
  Args:
    type: :Woman
    source: India_Hicks
  AddTriple (6b4642d2-3d78-4206-9e4f-4a62e1ec405c)
 Call ID: 6b4642d2-3d78-4206-9e4f-4a62e1ec405c
  Args:
    source: India_Hicks
    target: Pamela_Hicks
    relation: :hasMother
  AddTriple (f80a41d0-92db-4b63-b073-fe724dc5e6ae)
 Call ID: f80a41d0-92db-4b63-b073-fe724dc5e6ae
  Args:
    source: India_Hicks
    target: David_Nightingale_Hicks
    relation: :hasFather
  AssignClass (da7b97c9-3065-4ca0-a33a-5b32d551b05b)
 Call ID: da7b97c9-3065-4ca0-a33a-5b32d551b05b
  Args:
    type: :Person
    source: Prince_Louis_of_Battenberg
  AssignClass (79e5fa25-95bd-4bed-a200-6ac8379e8e54)
 Call ID: 79e5fa25-95bd-4bed-a200-6ac8379e8e54
  Args:
    type: :Man
    source: Prince_Louis_of_Battenberg
  AssignClass (7993d2c6-77f1-4a8a-83e7-28f77ab5314c)
 Call ID: 7993d2c6-77f1-4a8a-83e7-28f77ab5314c
  Args:
    type: :Person
    source: Princess_Victoria_of_Hesse
  AssignClass (daee0256-05a5-453a-b070-6b4173afce32)
 Call ID: daee0256-05a5-453a-b070-6b4173afce32
  Args:
    type: :Woman
    source: Princess_Victoria_of_Hesse
  AddTriple (52c6ab7b-c61a-4608-8125-39968c79b6e5)
 Call ID: 52c6ab7b-c61a-4608-8125-39968c79b6e5
  Args:
    target: Prince_Louis_of_Battenberg
    source: Louis_Mountbatten
    relation: :hasFather
  AddTriple (a894cc54-770d-4004-b11f-5ada7004dcb3)
 Call ID: a894cc54-770d-4004-b11f-5ada7004dcb3
  Args:
    relation: :hasMother
    target: Princess_Victoria_of_Hesse
    source: Louis_Mountbatten
  AssignClass (af0d981b-cdb5-4614-94a6-a3c87dbd55d5)
 Call ID: af0d981b-cdb5-4614-94a6-a3c87dbd55d5
  Args:
    source: 1st_Baron_Mount_Temple
    type: :Person
  AssignClass (21c39775-3d66-4075-b617-92152e257dc2)
 Call ID: 21c39775-3d66-4075-b617-92152e257dc2
  Args:
    type: :Man
    source: 1st_Baron_Mount_Temple
  AddTriple (c663d46f-cef5-4d0a-bc48-c7b80ac91f51)
 Call ID: c663d46f-cef5-4d0a-bc48-c7b80ac91f51
  Args:
    target: 1st_Baron_Mount_Temple
    source: Edwina_Ashley
    relation: :hasFather
  Finish (9c2ac2c5-a1bc-46cb-b409-4b7de49ed8a5)
 Call ID: 9c2ac2c5-a1bc-46cb-b409-4b7de49ed8a5
  Args: