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
Princess Alexandra, The Honourable Lady Ogilvy (Alexandra Helen Elizabeth Olga Christabel; born 25 December 1936), is a member of the British royal family.
She is the only daughter of Prince George, Duke of Kent, and Princess Marina of Greece and Denmark, the only living granddaughter of George V, a niece of Edward VIII and George VI, and a first cousin of Elizabeth II.
Alexandra's mother was also a first cousin of Prince Philip, Duke of Edinburgh, consort of Elizabeth II, making her both a second cousin and first cousin once removed of Charles III.
Alexandra was married to the businessman Sir Angus Ogilvy from 1963 until his death in 2004.
Early life

Alexandra was born at 11:20 am on Christmas Day 1936 at 3 Belgrave Square, London, the second child and only daughter of Prince George, Duke of Kent, the fourth son of King George V and Queen Mary, and Princess Marina of Greece and Denmark, a daughter of Prince Nicholas of Greece and Denmark and Grand Duchess Elena Vladimirovna of Russia.
She was named after her paternal great-grandmother, Queen Alexandra; her grandmother, Grand Duchess Elena Vladimirovna of Russia; and both of her maternal aunts, Countess Elizabeth of Törring-Jettenbach and Princess Olga of Yugoslavia.
She received the name Christabel because she was born on Christmas Day, like her aunt Princess Alice, Duchess of Gloucester.
As a male-line granddaughter of the British monarch, she was styled as a British princess with the prefix Her Royal Highness.
At the time of her birth she was sixth in the line of succession to the British throne, behind her cousins Princess Elizabeth (later Queen Elizabeth II) and Princess Margaret, her uncle the Duke of Gloucester, her father the Duke of Kent, and her elder brother Prince Edward.
She was born two weeks after the abdication of her uncle King Edward VIII.
Alexandra was baptised in the Private Chapel at Buckingham Palace on 9 February 1937, and her godparents were King George VI and Queen Elizabeth (her paternal uncle and aunt); the Queen of Norway (her great-aunt); Princess Nicholas of Greece and Denmark (her maternal grandmother); Princess Olga of Yugoslavia (her maternal aunt); Princess Beatrice (her paternal great-great-aunt); the Earl of Athlone (her paternal great-uncle); and Count Karl Theodor of Törring-Jettenbach (her maternal uncle by marriage).
Alexandra spent most of her childhood at her family's country house, Coppins, in Buckinghamshire.
Alexandra has the distinction of being the first British princess to have attended a boarding school, Heathfield School near Ascot.
Marriage and personal life

On 24 April 1963, Alexandra married The Hon.
Angus James Bruce Ogilvy (1928–2004), the second son of David Ogilvy, 12th Earl of Airlie, and Lady Alexandra Coke, at Westminster Abbey.
Ogilvy presented Alexandra with an engagement ring made of a cabochon sapphire set in gold and surrounded by diamonds on both sides.
Alexandra travelled with her brother, the Duke of Kent, from Kensington Palace to the Abbey.
The bridesmaids included Princess Anne and Archduchess Elisabeth of Austria, and the best man was Peregrine Fairfax.
Ogilvy declined the Queen's offer to be created an earl upon marriage, so the couple's children carry no titles.
Ogilvy was knighted in 1988 (when Alexandra assumed the style of The Hon.
Lady Ogilvy), and was sworn of the Privy Council in 1997.
Alexandra and Ogilvy had two children:


Marina's first pregnancy, announced in late 1989, caused controversy as the couple were not married.
The situation led to a feud with her parents, who suggested that Marina either marry her companion in a shotgun wedding or have an abortion.
In an interview with a tabloid at the time, Marina claimed that her parents had cut off her trust fund and monthly allowance due to their disapproval of her conduct.
Marina's parents denied her allegations, stating that they loved her, had not cut her off, and that she was welcome at home at any time.
Activities

Beginning in the late 1950s, Alexandra undertook an extensive programme of engagements in support of the Queen, both in the United Kingdom and overseas.
The "Alexandra Waltz" was composed for the visit by radio announcer Russ Tyson and television musical director Clyde Collins, and was sung for the princess by the teenage Gay Kahler, who later performed under the name Gay Kayler.
In 1961, Alexandra visited Hong Kong, including stops at Aberdeen Fish Market, Lok Ma Chau police station, and So Uk Estate, a public housing complex.
The Princess Alexandra Hospital in Brisbane is named in her honour.
Alexandra represented the Queen when Nigeria gained independence from the United Kingdom on 1 October 1960, and she opened the first Parliament on 3 October.
Alexandra opened the new hospital in Harlow, Essex, named in her honour, on 27 April 1965.
The Princess Alexandra Hospital NHS Trust was announced by the Prime Minister, Boris Johnson, in September 2019 as part of the government's new health infrastructure programme to build a replacement hospital.
Alexandra is an honorary fellow of the Royal College of Physicians and Surgeons of Glasgow, the Faculty of Anaesthetists of the Royal College of Surgeons of England, the Royal College of Obstetricians and Gynaecologists, and the Royal College of Physicians.
She is president of Alexandra Rose Day, founded in honour of her great-grandmother, Queen Alexandra, and was patron of The Royal School, Hampstead.
Until its abolition in 2013, she received £225,000 per year from the Civil List to cover the cost of official expenses, although, as with other members of the royal family (except the Duke of Edinburgh), the Queen repaid this amount to HM Treasury.
Alexandra lives at Thatched House Lodge in Richmond, London, a Crown property purchased on a 150-year lease from the Crown Estate Commissioners by Angus Ogilvy after their wedding in 1963.
She has been patron of the Royal Alexandra Children's Hospital in Brighton since 1954 and of Alzheimer's Society since 1990.
Alexandra is also the royal patron of Children and Families Across Borders (CFAB), a charity dedicated to reuniting children separated from their families.
In November 2016, one month before Alexandra's 80th birthday, the Queen held a reception at Buckingham Palace in honour of her charitable work.
In February 2024, she began using a wheelchair and attended a thanksgiving service for Constantine II of Greece later that month.
In April 2026, Alexandra attended a commemorative reception held to mark the centenary of Queen Elizabeth II's birth.
Titles, styles, honours and arms

Titles and styles

Alexandra is often referred to simply as Her Royal Highness Princess Alexandra.
She has held the following styles officially:


Honours

Eponyms

Appointments

Honorary military appointments

Arms

Issue

Ancestry

Since Princess Alexandra's mother was a first cousin of Prince Philip, Duke of Edinburgh, she is a second cousin to King Charles III and his siblings, in addition to being their first cousin once removed because her father was Queen Elizabeth II's uncle.



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
  AssignClass (5f7cc8b7-7ea1-45c8-8e2f-f07a18cffa7d)
 Call ID: 5f7cc8b7-7ea1-45c8-8e2f-f07a18cffa7d
  Args:
    type: :Woman
    source: Princess_Alexandra
  AssignClass (41cf7b2b-f8c0-48e5-8fb7-3396085e80c5)
 Call ID: 41cf7b2b-f8c0-48e5-8fb7-3396085e80c5
  Args:
    type: :Man
    source: Prince_George_Duke_of_Kent
  AssignClass (2ea7d278-0540-4383-bf9d-98010e922eb1)
 Call ID: 2ea7d278-0540-4383-bf9d-98010e922eb1
  Args:
    source: Princess_Marina_of_Greece_and_Denmark
    type: :Woman
  AssignClass (2c34e3d1-397d-43bc-8b44-6577187504a5)
 Call ID: 2c34e3d1-397d-43bc-8b44-6577187504a5
  Args:
    source: Sir_Angus_Ogilvy
    type: :Man
  AddLiteral (6e663e8f-efde-4238-95c4-c79ff56862ef)
 Call ID: 6e663e8f-efde-4238-95c4-c79ff56862ef
  Args:
    source: Princess_Alexandra
    literal_type: xsd:integer
    literal_value: 1936
    relation: :hasBirthYear
  AddTriple (6905ec2e-ac76-418a-b17d-430d6928a43e)
 Call ID: 6905ec2e-ac76-418a-b17d-430d6928a43e
  Args:
    source: Princess_Alexandra
    relation: :hasFather
    target: Prince_George_Duke_of_Kent
  AddTriple (ac0387f2-3f66-4323-834f-766ae2feb107)
 Call ID: ac0387f2-3f66-4323-834f-766ae2feb107
  Args:
    source: Princess_Alexandra
    target: Princess_Marina_of_Greece_and_Denmark
    relation: :hasMother
  AddTriple (f01433d3-6c8f-4b9b-bc39-2b938b7a27cb)
 Call ID: f01433d3-6c8f-4b9b-bc39-2b938b7a27cb
  Args:
    source: Princess_Alexandra
    relation: :hasRelation
    target: Sir_Angus_Ogilvy
  AddLiteral (cc35930a-f495-4c18-a699-dc0a5267b71d)
 Call ID: cc35930a-f495-4c18-a699-dc0a5267b71d
  Args:
    literal_value: 1963
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: Princess_Alexandra
  AddLiteral (315f600c-aba8-4c3f-8ca6-cc3562448447)
 Call ID: 315f600c-aba8-4c3f-8ca6-cc3562448447
  Args:
    source: Sir_Angus_Ogilvy
    literal_value: 2004
    relation: :hasDeathYear
    literal_type: xsd:integer
  Finish (844a476e-bd4e-428b-a265-115dbda4a46e)
 Call ID: 844a476e-bd4e-428b-a265-115dbda4a46e
  Args: