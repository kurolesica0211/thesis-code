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
Prince Edward, Duke of Kent (Edward George Nicholas Paul Patrick; born 9 October 1935), is a member of the British royal family.
The elder son of Prince George, Duke of Kent, and Princess Marina of Greece and Denmark, he is a grandson of George V, nephew of Edward VIII and George VI, and first cousin of Elizabeth II.
Edward's mother was also a first cousin of Prince Philip, Elizabeth's husband, making him both a second cousin and first cousin once removed to Charles III.
In 2025, following the death of his wife, Katharine, Duchess of Kent, Edward became the oldest living member of the British royal family.
Edward has held the title of Duke of Kent for over 83 years.
Edward carried out engagements on behalf of Elizabeth II and is involved with over 140 charitable organisations.
Edward has been Chancellor of the University of Surrey since June 1976.
Early life and education

Edward was born at 2:05 am on 9 October 1935 at No. 3
Belgrave Square, London, the eldest child of  Prince George, Duke of Kent, and Princess Marina, Duchess of Kent.
His father was the fourth son of King George V and Queen Mary, and his mother was the daughter of Prince Nicholas of Greece and Denmark and Grand Duchess Elena Vladimirovna of Russia.
His godparents were his grandparents, King George V, Queen Mary, and Prince Nicholas of Greece and Denmark; the Prince of Wales; the Princess Royal; the Duke of Connaught and Strathearn (whose son, Prince Arthur of Connaught, stood proxy); and the Duchess of Argyll.
Edward began his education at Ludgrove, a preparatory school in Berkshire, before going on to Eton College and subsequently Le Rosey in Switzerland.
Edward speaks fluent French, having been raised in a house where, according to his younger brother, Prince Michael of Kent, their mother and aunts spoke French as a matter of preference.
On 25 August 1942, Edward's father, the Duke of Kent, was killed when his aircraft crashed in bad weather in Caithness.
Edward, then six years old, succeeded to his father's titles as Duke of Kent, Earl of St Andrews, and Baron Downpatrick.
In 1952, at the age of 16, he walked behind the coffin of his uncle, George VI, at the King's state funeral.
Military service

On 29 July 1955, Edward graduated from the Royal Military Academy Sandhurst as a second lieutenant in the Royal Scots Greys, marking the beginning of a military career that lasted more than 20 years.
From 1962 to 1963, Edward served in Hong Kong, later joining the staff in Eastern Command.
During the early 1970s, Edward also served briefly in Northern Ireland with his regiment.
Edward, then aged 35, had been deployed to Northern Ireland with his unit, but the Queen raised concerns during her weekly audience with the prime minister, Edward Heath.
Edward retired from the army on 15 April 1976.
Marriage and personal life

Edward met Katharine Worsley while he was based at Catterick Garrison.
Marina reportedly disapproved of her son's choice of bride and twice forbade the match before agreeing to the marriage in 1961.
Katharine converted to Catholicism in 1994, but because the conversion occurred during, and not before, their marriage, it did not cause Edward to lose his place in the line of succession, as the Act of Settlement 1701 applied only where the spouse was a Catholic at the time of marriage.
The couple have three living children:


Katharine had a miscarriage in 1975 owing to rubella, and gave birth to a stillborn son, Patrick, in 1977.
Edward resides at Wren House, Kensington Palace, in London.
In 2011, close associates of Jonathan Rees, a private investigator connected to the News International phone hacking scandal, alleged that he had accessed the bank accounts of Edward and his wife.
Edward had a mild stroke on the morning of 18 March 2013.
His wife, Katharine, died on 4 September 2025 at the age of 92.
Following her death, Edward became the oldest living member of the British royal family.
Activities

Edward performed engagements on behalf of his cousin, Queen Elizabeth II, for more than 50 years.
One of Edward's major public roles for many years was vice-chairman of British Trade International, formerly known as the British Overseas Trade Board, and later as the United Kingdom's Special Representative for International Trade and Investment.
The then Prince Andrew succeeded him in this position, later known as UK Trade & Investment (or UKTI), although Andrew resigned from the post in 2011.
In 1979, Edward became the first member of the royal family to visit China, focusing on the British Energy Exhibition in Beijing.
From 1971 to 2000, Edward served as president of The Football Association, the governing body of English football.
He has been president of The Scout Association since 1975, and, together with Prince William of Wales, visited the Centenary World Scout Jamboree at Hylands Park, Chelmsford, in July 2007.
His other roles include president of the RAF Benevolent Fund, the Royal National Lifeboat Institution, the Stroke Association, the Royal United Services Institute, the Royal Institution, the British Racing Drivers' Club, and patron of the American Air Museum in Britain, Royal West Norfolk Golf Club, Kent County Cricket Club, Opera North, and Trinity Laban Conservatoire of Music and Dance.
Edward is also one of the Royal Fellows of the Royal Academy of Engineering.
For almost 29 years, Edward has been the patron of Endeavour, a national youth organisation.
"


On 2 June 2022, Edward appeared alongside the Queen on the balcony of Buckingham Palace during the Trooping the Colour, which formed part of the Platinum Jubilee celebrations.
Edward was colonel of the Scots Guards for 50 years from 9 September 1974 to 14 April 2024, being succeeded by the Duke of Edinburgh.
In April 2026, Edward attended a commemorative reception held to mark the centenary of Queen Elizabeth II's birth.
Freemasonry

Edward was initiated into Royal Alpha Lodge No. 16 on 16 December 1963, and was elected its Worshipful Master for 1965 and 1966.
Having been appointed Senior Grand Warden in 1966, he was elected Grand Master the following year and was installed on 14 June 1967 during the United Grand Lodge of England's 250th-anniversary celebrations at the Royal Albert Hall.
He is the 10th, and longest-serving, Grand Master of UGLE, the governing body of Freemasonry in England and Wales.
In December 2013, Edward celebrated 50 years as a freemason.
In October 2017, he presided over the tercentenary celebrations of UGLE, marking the 300th anniversary of the founding of the original Grand Lodge, one of the two bodies that merged to form UGLE in 1813.
The main ceremony was held at the Royal Albert Hall, in the year that also marked Edward's 50th anniversary of installation as Grand Master.
Titles, styles, honours and arms

Titles and styles

Military ranks

Honours

Foreign

Civilian appointments

Wear of orders, decorations, and medals

The ribbons worn regularly by Edward in undress uniform are as follows:


With medals, Edward normally wears the breast stars of the Garter, St Michael and St George, and Royal Victorian Order.



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix ns1: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
@prefix ns2: <http://www.w3.org/2003/11/swrl#> .
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

ns1:isRuleEnabled a owl:AnnotationProperty .

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

:x a ns2:Variable .

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

:y a ns2:Variable .

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

[] a ns2:Imp ;
    rdfs:label "infer hasSon" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasBrother" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasSister" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (d42392f1-bf7d-4382-9e75-26292704e2f5)
 Call ID: d42392f1-bf7d-4382-9e75-26292704e2f5
  Args:
    type: :Man
    source: Prince_Edward_Duke_of_Kent
  AssignClass (027783ba-35db-49c5-9208-63caf36c3554)
 Call ID: 027783ba-35db-49c5-9208-63caf36c3554
  Args:
    type: :Man
    source: Prince_George_Duke_of_Kent
  AssignClass (7d44bbb0-7b76-436e-a84a-dca342b634b9)
 Call ID: 7d44bbb0-7b76-436e-a84a-dca342b634b9
  Args:
    type: :Woman
    source: Princess_Marina_of_Greece_and_Denmark
  AssignClass (df8758bc-a02c-4b8a-afe0-a1af363955a8)
 Call ID: df8758bc-a02c-4b8a-afe0-a1af363955a8
  Args:
    type: :Man
    source: George_V
  AssignClass (4f1223b9-3b4a-4d6a-845a-01c4b9b3f0f5)
 Call ID: 4f1223b9-3b4a-4d6a-845a-01c4b9b3f0f5
  Args:
    type: :Woman
    source: Queen_Mary
  AssignClass (a755cd2c-56d1-477f-892a-3148b13afd1f)
 Call ID: a755cd2c-56d1-477f-892a-3148b13afd1f
  Args:
    type: :Man
    source: Prince_Nicholas_of_Greece_and_Denmark
  AssignClass (87e9b0ed-e486-47be-8d54-90cd8fa83e03)
 Call ID: 87e9b0ed-e486-47be-8d54-90cd8fa83e03
  Args:
    type: :Woman
    source: Grand_Duchess_Elena_Vladimirovna_of_Russia
  AssignClass (954baf3c-b193-433a-b085-fcf235d8aa63)
 Call ID: 954baf3c-b193-433a-b085-fcf235d8aa63
  Args:
    type: :Man
    source: Prince_Michael_of_Kent
  AssignClass (99e00443-259a-4660-8e7b-a67d91027ea4)
 Call ID: 99e00443-259a-4660-8e7b-a67d91027ea4
  Args:
    type: :Woman
    source: Katharine_Duchess_of_Kent
  AssignClass (f916389e-88a7-4766-9c33-f97858ac1c6b)
 Call ID: f916389e-88a7-4766-9c33-f97858ac1c6b
  Args:
    type: :Man
    source: Patrick
  AddLiteral (422d39fb-aa1b-4ee0-8761-5afeeeaee152)
 Call ID: 422d39fb-aa1b-4ee0-8761-5afeeeaee152
  Args:
    literal_type: xsd:integer
    literal_value: 1935
    source: Prince_Edward_Duke_of_Kent
    relation: :hasBirthYear
  AddTriple (ca3412c0-a46b-4806-adf5-fe35c0f84a83)
 Call ID: ca3412c0-a46b-4806-adf5-fe35c0f84a83
  Args:
    target: Prince_George_Duke_of_Kent
    source: Prince_Edward_Duke_of_Kent
    relation: :hasFather
  AddTriple (dfa6e178-d25d-44d6-8e5d-1f9a1b93f813)
 Call ID: dfa6e178-d25d-44d6-8e5d-1f9a1b93f813
  Args:
    target: Princess_Marina_of_Greece_and_Denmark
    relation: :hasMother
    source: Prince_Edward_Duke_of_Kent
  AddTriple (c382b7f2-ed1c-43d3-8bca-3c20211e61d8)
 Call ID: c382b7f2-ed1c-43d3-8bca-3c20211e61d8
  Args:
    relation: :hasFather
    source: Prince_George_Duke_of_Kent
    target: George_V
  AddTriple (76f43887-da84-4e9f-ab33-9750a06810ab)
 Call ID: 76f43887-da84-4e9f-ab33-9750a06810ab
  Args:
    source: Prince_George_Duke_of_Kent
    relation: :hasMother
    target: Queen_Mary
  AddTriple (bdac806a-0744-4cc9-985d-cb43744ca638)
 Call ID: bdac806a-0744-4cc9-985d-cb43744ca638
  Args:
    source: Princess_Marina_of_Greece_and_Denmark
    relation: :hasFather
    target: Prince_Nicholas_of_Greece_and_Denmark
  AddTriple (4285a3a3-f142-4db5-9c74-7f2e42a7a7fc)
 Call ID: 4285a3a3-f142-4db5-9c74-7f2e42a7a7fc
  Args:
    target: Grand_Duchess_Elena_Vladimirovna_of_Russia
    source: Princess_Marina_of_Greece_and_Denmark
    relation: :hasMother
  AddTriple (5c743137-1685-4bf5-a9fe-d6b8e881d995)
 Call ID: 5c743137-1685-4bf5-a9fe-d6b8e881d995
  Args:
    relation: :hasBrother
    source: Prince_Edward_Duke_of_Kent
    target: Prince_Michael_of_Kent
  AddTriple (fdd48f27-0fe8-448f-b444-981f0d3e0279)
 Call ID: fdd48f27-0fe8-448f-b444-981f0d3e0279
  Args:
    source: Prince_Michael_of_Kent
    relation: :hasParent
    target: Prince_George_Duke_of_Kent
  AddTriple (c3fccba8-7018-428c-bfdf-bcd1971d8b76)
 Call ID: c3fccba8-7018-428c-bfdf-bcd1971d8b76
  Args:
    target: Princess_Marina_of_Greece_and_Denmark
    relation: :hasParent
    source: Prince_Michael_of_Kent
  AddLiteral (01efc4cc-f417-4139-a4e1-c236f76274e1)
 Call ID: 01efc4cc-f417-4139-a4e1-c236f76274e1
  Args:
    literal_value: 1961
    relation: :hasMarriageYear
    source: Prince_Edward_Duke_of_Kent
    literal_type: xsd:integer
  AddTriple (2e0ef354-a2a1-43e8-a0fc-65337f959c34)
 Call ID: 2e0ef354-a2a1-43e8-a0fc-65337f959c34
  Args:
    relation: :hasRelation
    source: Prince_Edward_Duke_of_Kent
    target: Katharine_Duchess_of_Kent
  AddLiteral (02c330b1-281d-4c0b-b506-b86d6944906e)
 Call ID: 02c330b1-281d-4c0b-b506-b86d6944906e
  Args:
    literal_type: xsd:integer
    literal_value: 2025
    source: Katharine_Duchess_of_Kent
    relation: :hasDeathYear
  AddTriple (13152752-a262-4224-976b-503217b53308)
 Call ID: 13152752-a262-4224-976b-503217b53308
  Args:
    relation: :hasParent
    source: Patrick
    target: Prince_Edward_Duke_of_Kent
  AddTriple (0166c8d3-e81e-4738-9554-9d83f0e22545)
 Call ID: 0166c8d3-e81e-4738-9554-9d83f0e22545
  Args:
    source: Patrick
    relation: :hasParent
    target: Katharine_Duchess_of_Kent
  AddLiteral (ccc47af1-495c-4a05-9e79-33d68b411a15)
 Call ID: ccc47af1-495c-4a05-9e79-33d68b411a15
  Args:
    literal_value: 1977
    source: Patrick
    relation: :hasBirthYear
    literal_type: xsd:integer
  Finish (53859ffd-c54b-45e5-8b8e-fd0fec93a1c9)
 Call ID: 53859ffd-c54b-45e5-8b8e-fd0fec93a1c9
  Args: