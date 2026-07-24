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
  AssignClass (bbd8cc97-ae33-4b67-93f0-5ddf32f12805)
 Call ID: bbd8cc97-ae33-4b67-93f0-5ddf32f12805
  Args:
    source: PrinceEdwardDukeOfKent
    type: :Man
  AssignClass (7cd5a99c-a0ea-43ac-847d-0d16a1bce474)
 Call ID: 7cd5a99c-a0ea-43ac-847d-0d16a1bce474
  Args:
    source: PrinceEdwardDukeOfKent
    type: :Person
  AddLiteral (aeb212bb-03b2-4af1-9575-d93baacdfcd2)
 Call ID: aeb212bb-03b2-4af1-9575-d93baacdfcd2
  Args:
    relation: :hasBirthYear
    source: PrinceEdwardDukeOfKent
    literal_value: 1935
    literal_type: xsd:integer
  AssignClass (64d6b36f-b730-42be-812f-457d726eda6f)
 Call ID: 64d6b36f-b730-42be-812f-457d726eda6f
  Args:
    source: PrinceGeorgeDukeOfKent
    type: :Man
  AssignClass (676c2d54-8095-45f3-b348-6f27f8678e70)
 Call ID: 676c2d54-8095-45f3-b348-6f27f8678e70
  Args:
    source: PrinceGeorgeDukeOfKent
    type: :Person
  AssignClass (c9fa2e38-f68c-4c6d-aabb-39cf96b3ee4f)
 Call ID: c9fa2e38-f68c-4c6d-aabb-39cf96b3ee4f
  Args:
    type: :Woman
    source: PrincessMarinaDuchessOfKent
  AssignClass (c5d810c7-d29b-4d9d-900f-bb1bbaed6ada)
 Call ID: c5d810c7-d29b-4d9d-900f-bb1bbaed6ada
  Args:
    source: PrincessMarinaDuchessOfKent
    type: :Person
  AddTriple (f8ede0af-e81b-4dff-9fd1-fa1c6b198369)
 Call ID: f8ede0af-e81b-4dff-9fd1-fa1c6b198369
  Args:
    relation: :hasFather
    target: PrinceGeorgeDukeOfKent
    source: PrinceEdwardDukeOfKent
  AddTriple (f38a8584-de65-4c58-85b8-2b9448b97e3d)
 Call ID: f38a8584-de65-4c58-85b8-2b9448b97e3d
  Args:
    relation: :hasMother
    target: PrincessMarinaDuchessOfKent
    source: PrinceEdwardDukeOfKent
  AssignClass (c8754f3d-66a9-48aa-a1eb-15d629687c5f)
 Call ID: c8754f3d-66a9-48aa-a1eb-15d629687c5f
  Args:
    type: :Man
    source: GeorgeV
  AssignClass (02863689-e78e-4d5a-86c0-d6c26b704f2c)
 Call ID: 02863689-e78e-4d5a-86c0-d6c26b704f2c
  Args:
    source: GeorgeV
    type: :Person
  AssignClass (cc9cd800-4432-4ae6-94c4-7a0798c45df7)
 Call ID: cc9cd800-4432-4ae6-94c4-7a0798c45df7
  Args:
    type: :Woman
    source: QueenMary
  AssignClass (7fa91c52-db7b-4e46-86fb-30858e096e31)
 Call ID: 7fa91c52-db7b-4e46-86fb-30858e096e31
  Args:
    source: QueenMary
    type: :Person
  AddTriple (3db69b4a-7f0f-48f1-bea1-662e34014277)
 Call ID: 3db69b4a-7f0f-48f1-bea1-662e34014277
  Args:
    target: GeorgeV
    relation: :hasFather
    source: PrinceGeorgeDukeOfKent
  AddTriple (0f8ec2d0-f7ff-4815-a8f3-6e33298c961a)
 Call ID: 0f8ec2d0-f7ff-4815-a8f3-6e33298c961a
  Args:
    relation: :hasMother
    target: QueenMary
    source: PrinceGeorgeDukeOfKent
  AssignClass (98cd0020-daa9-4792-bcf8-28a907f7865d)
 Call ID: 98cd0020-daa9-4792-bcf8-28a907f7865d
  Args:
    source: PrinceNicholasOfGreeceAndDenmark
    type: :Man
  AssignClass (75b4f56c-f030-45b4-a593-ff3c5b99b280)
 Call ID: 75b4f56c-f030-45b4-a593-ff3c5b99b280
  Args:
    type: :Person
    source: PrinceNicholasOfGreeceAndDenmark
  AssignClass (337ee95b-1b09-4fa7-b96b-71941edceb00)
 Call ID: 337ee95b-1b09-4fa7-b96b-71941edceb00
  Args:
    source: GrandDuchessElenaVladimirovnaOfRussia
    type: :Woman
  AssignClass (2406663e-8bc2-423c-ad77-17b5748443a3)
 Call ID: 2406663e-8bc2-423c-ad77-17b5748443a3
  Args:
    source: GrandDuchessElenaVladimirovnaOfRussia
    type: :Person
  AddTriple (c692b201-4a40-4912-9aae-584d3be38115)
 Call ID: c692b201-4a40-4912-9aae-584d3be38115
  Args:
    source: PrincessMarinaDuchessOfKent
    relation: :hasFather
    target: PrinceNicholasOfGreeceAndDenmark
  AddTriple (6d5133af-930c-49f9-b2c5-eef701e5ced4)
 Call ID: 6d5133af-930c-49f9-b2c5-eef701e5ced4
  Args:
    source: PrincessMarinaDuchessOfKent
    target: GrandDuchessElenaVladimirovnaOfRussia
    relation: :hasMother
  AssignClass (e5c30aeb-8c8c-4f41-850c-2e418c8e78ce)
 Call ID: e5c30aeb-8c8c-4f41-850c-2e418c8e78ce
  Args:
    type: :Man
    source: PrinceMichaelOfKent
  AssignClass (b8a8786f-1795-4f15-8ddd-ce0f5d21040b)
 Call ID: b8a8786f-1795-4f15-8ddd-ce0f5d21040b
  Args:
    type: :Person
    source: PrinceMichaelOfKent
  AddTriple (23b6f771-207e-4ac5-860d-f4e5dc28c26a)
 Call ID: 23b6f771-207e-4ac5-860d-f4e5dc28c26a
  Args:
    source: PrinceEdwardDukeOfKent
    relation: :isSiblingOf
    target: PrinceMichaelOfKent
  AssignClass (3f54a131-5464-4f1f-881e-bb18fbc14628)
 Call ID: 3f54a131-5464-4f1f-881e-bb18fbc14628
  Args:
    source: KatharineDuchessOfKent
    type: :Woman
  AssignClass (b21cf299-cfc3-43aa-8050-de3d3a200d4a)
 Call ID: b21cf299-cfc3-43aa-8050-de3d3a200d4a
  Args:
    source: KatharineDuchessOfKent
    type: :Person
  AddTriple (294ffa82-2ac6-44d1-8eb6-f96c10e26c0b)
 Call ID: 294ffa82-2ac6-44d1-8eb6-f96c10e26c0b
  Args:
    relation: :hasRelation
    target: KatharineDuchessOfKent
    source: PrinceEdwardDukeOfKent
  AddLiteral (e9d63a8e-3889-413f-9547-0c11892fc29e)
 Call ID: e9d63a8e-3889-413f-9547-0c11892fc29e
  Args:
    literal_type: xsd:integer
    source: PrinceEdwardDukeOfKent
    literal_value: 1961
    relation: :hasMarriageYear
  AddLiteral (e64b38c9-ed54-45b0-b974-1ead451c9c21)
 Call ID: e64b38c9-ed54-45b0-b974-1ead451c9c21
  Args:
    relation: :hasDeathYear
    literal_value: 2025
    source: KatharineDuchessOfKent
    literal_type: xsd:integer
  AssignClass (05f57803-bd94-41b5-b711-7f4333aeeb52)
 Call ID: 05f57803-bd94-41b5-b711-7f4333aeeb52
  Args:
    type: :Man
    source: Patrick
  AssignClass (b5d44b84-7612-42f3-8da9-84d44f1f1c92)
 Call ID: b5d44b84-7612-42f3-8da9-84d44f1f1c92
  Args:
    type: :Person
    source: Patrick
  AddTriple (8d258562-5599-4cff-80d9-8776c30e074f)
 Call ID: 8d258562-5599-4cff-80d9-8776c30e074f
  Args:
    relation: :hasFather
    target: PrinceEdwardDukeOfKent
    source: Patrick
  AddTriple (3da9103f-6542-4ddc-9d1d-835a6a08b766)
 Call ID: 3da9103f-6542-4ddc-9d1d-835a6a08b766
  Args:
    relation: :hasMother
    target: KatharineDuchessOfKent
    source: Patrick
  AddLiteral (6cee045d-92f6-4a98-882c-bb1a97b7c525)
 Call ID: 6cee045d-92f6-4a98-882c-bb1a97b7c525
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1977
    source: Patrick
  Finish (31fb53a8-3045-40e8-9a18-8a0fcb67c527)
 Call ID: 31fb53a8-3045-40e8-9a18-8a0fcb67c527
  Args: