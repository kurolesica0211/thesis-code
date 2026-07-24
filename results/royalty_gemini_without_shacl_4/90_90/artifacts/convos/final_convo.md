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
Princess Marina of Greece and Denmark (Greek: Μαρίνα; 13 December  1906 – 27 August 1968), later Duchess of Kent, was a Greek and Danish princess by birth and a British princess by marriage.
A granddaughter of King George I of Greece and Queen Olga, she was the daughter of Prince Nicholas of Greece and Denmark and Grand Duchess Elena Vladimirovna of Russia.
In 1934, she married Prince George, Duke of Kent, the fourth son of King George V and Queen Mary.
Edward, Alexandra, and Michael.
Early life

Marina was born on 13 December 1906 in Athens, Greece, during the reign of her paternal grandfather, George I of Greece.
She was the third and youngest daughter of Prince Nicholas of Greece and Denmark and his wife, Grand Duchess Elena Vladimirovna of Russia.
Her father was the third son of George I of Greece and Queen Olga, while her mother was the only daughter of Grand Duke Vladimir Alexandrovich and Grand Duchess Maria Pavlovna of Russia.
Through her father she was a great-granddaughter of Christian IX of Denmark, and through her mother a granddaughter of Emperor Alexander II of Russia.
Marina had two elder sisters, Princess Olga and Princess Elizabeth.
Olga married Prince Paul of Yugoslavia in 1923; following the assassination of his cousin, Alexander I of Yugoslavia, Paul served as Prince Regent of Yugoslavia from 1934 to 1941.
One of their paternal uncles was Prince Andrew of Greece and Denmark, father of Prince Philip, Duke of Edinburgh, making Marina and her sisters Philip's first cousins.
Marina spent her early years in Greece and lived with her parents and paternal grandparents at Tatoi Palace.
She and her sisters were raised to be devout and religious, a quality encouraged by their grandmother, Queen Olga of Greece.
The family travelled outside Greece frequently, especially during the summer months.
Marina's first recorded visit to Britain was in 1910, when she was three, following the death of her godfather, Edward VII.
During that visit she met her godmother and future mother-in-law, Queen Mary, who treated Marina and her sisters as if they were her own children.
The Greek royal family was forced into exile when Marina was 11, following the overthrow of the monarchy.
They later settled in Paris, while Marina spent periods living with her extended family across Europe.
Marriage and children

Wedding ceremony

In 1932, Marina met Prince George (later the Duke of Kent), her second cousin through Christian IX of Denmark, in London.
Their betrothal was announced in August 1934, and George was created Duke of Kent on 9 October.
It was the first major royal wedding since that of Prince Albert, Duke of York (later George VI), and Lady Elizabeth Bowes-Lyon (later Queen Elizabeth the Queen mother) 11 years earlier.
Marina remains the most recent foreign princess to marry into the British royal family.
Married life

Marina and George established their first home at 3 Belgrave Square, close to Buckingham Palace.
Marina became patroness of several organisations and charities, including the Elizabeth Garrett Anderson Hospital, the Women's Hospital Fund, and the Central School of Speech and Drama, causes she continued to support throughout her life.
She developed a close relationship with her mother-in-law with whom she often spent time while George was undertaking royal duties.
The couple had three children:


George was killed on 25 August 1942 in an air crash at Eagle's Rock, near Dunbeath, Caithness, Scotland, while on active service with the Royal Air Force.
According to royal biographer Hugo Vickers, Marina was "the only war widow in Britain whose estate was forced to pay death duties".
During the Second World War, Marina trained as a nurse for three months under the pseudonym "Sister Kay" and joined the Civil Nursing Reserve.
Later life and death

After her husband's death, Marina continued to be an active member of the British royal family, carrying out a wide range of royal and official engagements.
In 1947, Marina visited Greece and Italy.
Later in 1952, Marina visited Sarawak (then a British Crown Colony), where she laid the foundation stone of the St. Thomas's Cathedral in Kuching.
In 1954, Marina was granted an Apartment at Kensington Palace as a permanent grace-and-favour residence.
During her early widowhood she had often stayed with her mother-in-law at Marlborough House; however Mary's death in 1953 created a need for Marina to have her own London residence.
The Apartment had stood vacant for nearly 15 years, having previously been the home of Princess Louise, Duchess of Argyll, prior to her death in 1939.
As the apartment was considered too large for Marina's needs, its eastern half was divided to create Apartment 1A.
During the renovations, Marina reportedly considered removing an original Wren staircase inside Apartment 1, finding it "too much like a servant's staircase" and too narrow for descending in full evening dress; palace officials intervened to prevent its removal.
Marina and her three children took up residence in October 1955, and Apartment 1 remained her home until her death in 1968.
In March 1957, when the Gold Coast achieved independence from Britain as Ghana, Marina was appointed to represent the Queen at the celebrations.
50 years later, at the 50th anniversary of Ghana's independence, her son, Edward, was appointed by the Queen to represent her.
Marina earned a place in the International Best Dressed List Hall of Fame in 1960, together with the Princess of Monaco, Patricia Lopez-Willshaw, and Merle Oberon.
In September and October 1966, when the British Protectorates of Bechuanaland and Basutoland became the Republic of Botswana and the Kingdom of Lesotho respectively, Marina was again appointed to represent the Queen at both independence celebrations.
The main public hospital in Gaborone, the new capital of Botswana, is named Princess Marina Hospital.
She served as Chancellor of the University of Kent at Canterbury from 1963 until her death.
Marina died at 11:40 am on 27 August 1968 at Kensington Palace from a brain tumour, aged 61.
Her funeral service was held at St. George's Chapel, Windsor Castle, on 30 August.
Her funeral was the last royal ceremony attended by her brother-in-law, the former king Edward VIII.
Marina's will was sealed in London after her death.
Legacy

Marina gave her name to a number of institutions and facilities, including:


References in popular culture

Titles, styles, honours, and arms

Titles and styles

Marina was known as the Princess Marina of Greece.
After her marriage she was styled Her Royal Highness The Duchess of Kent, and was later known as Her Royal Highness The Princess Marina, Duchess of Kent.



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
  AssignClass (3b6d7d83-f530-48e6-bb68-573c2f088707)
 Call ID: 3b6d7d83-f530-48e6-bb68-573c2f088707
  Args:
    type: :Woman
    source: Marina
  AddLiteral (b0e24b99-e3f1-4b21-aee1-e69795a1c991)
 Call ID: b0e24b99-e3f1-4b21-aee1-e69795a1c991
  Args:
    literal_type: xsd:nonNegativeInteger
    relation: :hasBirthYear
    source: Marina
    literal_value: 1906
  AddLiteral (818121e2-09a8-4e65-8f8c-57e55ea62606)
 Call ID: 818121e2-09a8-4e65-8f8c-57e55ea62606
  Args:
    literal_type: xsd:nonNegativeInteger
    relation: :hasDeathYear
    source: Marina
    literal_value: 1968
  AssignClass (d41def67-e8f7-4d05-8c1e-040bf3ca5a2c)
 Call ID: d41def67-e8f7-4d05-8c1e-040bf3ca5a2c
  Args:
    type: :Man
    source: GeorgeIOfGreece
  AssignClass (14907a03-ec5a-404b-8389-387d886f7e45)
 Call ID: 14907a03-ec5a-404b-8389-387d886f7e45
  Args:
    type: :Woman
    source: QueenOlgaOfGreece
  AssignClass (d0907ecf-e2f0-43a5-baef-4983f4c42e05)
 Call ID: d0907ecf-e2f0-43a5-baef-4983f4c42e05
  Args:
    type: :Man
    source: PrinceNicholasOfGreeceAndDenmark
  AssignClass (3d6de1e7-e903-41ff-a4ab-91d39a21c82f)
 Call ID: 3d6de1e7-e903-41ff-a4ab-91d39a21c82f
  Args:
    type: :Woman
    source: GrandDuchessElenaVladimirovnaOfRussia
  AddTriple (2039390f-6620-453f-8687-d3041f95eb1b)
 Call ID: 2039390f-6620-453f-8687-d3041f95eb1b
  Args:
    relation: :hasFather
    target: PrinceNicholasOfGreeceAndDenmark
    source: Marina
  AddTriple (4f596bd5-d244-4cf4-b4bf-d033e8c6f231)
 Call ID: 4f596bd5-d244-4cf4-b4bf-d033e8c6f231
  Args:
    source: Marina
    target: GrandDuchessElenaVladimirovnaOfRussia
    relation: :hasMother
  AddTriple (2eb93493-7611-42cf-a531-5cda630cff67)
 Call ID: 2eb93493-7611-42cf-a531-5cda630cff67
  Args:
    source: PrinceNicholasOfGreeceAndDenmark
    target: GeorgeIOfGreece
    relation: :hasFather
  AddTriple (50bdd914-aa6c-4540-bede-e5552846eb5e)
 Call ID: 50bdd914-aa6c-4540-bede-e5552846eb5e
  Args:
    relation: :hasMother
    target: QueenOlgaOfGreece
    source: PrinceNicholasOfGreeceAndDenmark
  AssignClass (17a7d51b-2793-421b-9c77-77de95efddf8)
 Call ID: 17a7d51b-2793-421b-9c77-77de95efddf8
  Args:
    type: :Man
    source: PrinceGeorgeDukeOfKent
  AddLiteral (964dbc36-6e7d-4a1c-8b40-c9a3da722e55)
 Call ID: 964dbc36-6e7d-4a1c-8b40-c9a3da722e55
  Args:
    source: Marina
    literal_value: 1934
    literal_type: xsd:nonNegativeInteger
    relation: :hasMarriageYear
  AddTriple (9aeee857-4725-4218-a323-0ebabea697db)
 Call ID: 9aeee857-4725-4218-a323-0ebabea697db
  Args:
    source: Marina
    target: PrinceGeorgeDukeOfKent
    relation: :hasRelation
  AssignClass (cd4205d3-7099-49ac-b0aa-7cd539037f7d)
 Call ID: cd4205d3-7099-49ac-b0aa-7cd539037f7d
  Args:
    type: :Man
    source: KingGeorgeV
  AssignClass (15b0672f-13b2-45df-8866-326894528540)
 Call ID: 15b0672f-13b2-45df-8866-326894528540
  Args:
    type: :Woman
    source: QueenMary
  AddTriple (96e64e13-d413-48a9-a94f-2a1d37ce8f1a)
 Call ID: 96e64e13-d413-48a9-a94f-2a1d37ce8f1a
  Args:
    target: KingGeorgeV
    relation: :hasFather
    source: PrinceGeorgeDukeOfKent
  AddTriple (14e63c74-f6af-45be-8666-268c85f80468)
 Call ID: 14e63c74-f6af-45be-8666-268c85f80468
  Args:
    target: QueenMary
    relation: :hasMother
    source: PrinceGeorgeDukeOfKent
  AssignClass (e3aa7834-95dc-494e-97d5-3e630dd3e06a)
 Call ID: e3aa7834-95dc-494e-97d5-3e630dd3e06a
  Args:
    type: :Man
    source: Edward
  AssignClass (fee53fc2-1b0f-4945-bce4-8aaf0d147e62)
 Call ID: fee53fc2-1b0f-4945-bce4-8aaf0d147e62
  Args:
    type: :Woman
    source: Alexandra
  AssignClass (8dc106b2-68ef-4cf0-a3ad-9d018f642086)
 Call ID: 8dc106b2-68ef-4cf0-a3ad-9d018f642086
  Args:
    type: :Man
    source: Michael
  AddTriple (d59efe2a-3cdd-472a-b4ad-33db80a8b7f1)
 Call ID: d59efe2a-3cdd-472a-b4ad-33db80a8b7f1
  Args:
    source: Marina
    target: Edward
    relation: :hasChild
  AddTriple (e42b76e9-b13c-4258-9c47-d89d775447ff)
 Call ID: e42b76e9-b13c-4258-9c47-d89d775447ff
  Args:
    source: Marina
    relation: :hasChild
    target: Alexandra
  AddTriple (3617ffe6-d7a3-4e12-864b-1dc4950454e0)
 Call ID: 3617ffe6-d7a3-4e12-864b-1dc4950454e0
  Args:
    target: Michael
    relation: :hasChild
    source: Marina
  AddTriple (0591148e-1255-479b-9ba5-f34e5a586007)
 Call ID: 0591148e-1255-479b-9ba5-f34e5a586007
  Args:
    source: PrinceGeorgeDukeOfKent
    target: Edward
    relation: :hasChild
  AddTriple (97b265b4-c09f-415e-b32e-ddb10888f22e)
 Call ID: 97b265b4-c09f-415e-b32e-ddb10888f22e
  Args:
    source: PrinceGeorgeDukeOfKent
    relation: :hasChild
    target: Alexandra
  AddTriple (8910afdb-b4d2-40c1-b1f8-9cc448eb84e6)
 Call ID: 8910afdb-b4d2-40c1-b1f8-9cc448eb84e6
  Args:
    source: PrinceGeorgeDukeOfKent
    target: Michael
    relation: :hasChild
  AssignClass (50ec26db-b51a-452e-a67e-b977b111c34a)
 Call ID: 50ec26db-b51a-452e-a67e-b977b111c34a
  Args:
    type: :Woman
    source: PrincessOlga
  AssignClass (aa7579cf-2f87-4035-855f-d4aca3820af2)
 Call ID: aa7579cf-2f87-4035-855f-d4aca3820af2
  Args:
    type: :Woman
    source: PrincessElizabeth
  AddTriple (f22e6e6e-785c-4ca1-9100-5860b21c9f0a)
 Call ID: f22e6e6e-785c-4ca1-9100-5860b21c9f0a
  Args:
    target: PrincessOlga
    relation: :hasSister
    source: Marina
  AddTriple (38464f75-fe99-44ce-a948-971523d223ac)
 Call ID: 38464f75-fe99-44ce-a948-971523d223ac
  Args:
    target: PrincessElizabeth
    relation: :hasSister
    source: Marina
  AssignClass (4b75b131-57de-4d82-8f84-94dc8050867f)
 Call ID: 4b75b131-57de-4d82-8f84-94dc8050867f
  Args:
    type: :Man
    source: GrandDukeVladimirAlexandrovich
  AssignClass (a4f23786-4a09-483f-b9c8-911d5ba0b95a)
 Call ID: a4f23786-4a09-483f-b9c8-911d5ba0b95a
  Args:
    type: :Woman
    source: GrandDuchessMariaPavlovnaOfRussia
  AddTriple (81e13268-09a2-40fa-a86a-f66e160eb563)
 Call ID: 81e13268-09a2-40fa-a86a-f66e160eb563
  Args:
    relation: :hasFather
    target: GrandDukeVladimirAlexandrovich
    source: GrandDuchessElenaVladimirovnaOfRussia
  AddTriple (36fa50b6-e495-4943-a3be-5a42c5010777)
 Call ID: 36fa50b6-e495-4943-a3be-5a42c5010777
  Args:
    relation: :hasMother
    target: GrandDuchessMariaPavlovnaOfRussia
    source: GrandDuchessElenaVladimirovnaOfRussia
  AssignClass (c7b3b9ad-8d8a-48ff-9a4e-44ec9e911dc0)
 Call ID: c7b3b9ad-8d8a-48ff-9a4e-44ec9e911dc0
  Args:
    type: :Man
    source: PrinceAndrewOfGreeceAndDenmark
  AddTriple (434bafac-3b85-441c-9862-07957c658cac)
 Call ID: 434bafac-3b85-441c-9862-07957c658cac
  Args:
    source: PrinceNicholasOfGreeceAndDenmark
    relation: :hasBrother
    target: PrinceAndrewOfGreeceAndDenmark
  AssignClass (61b21874-0802-4390-a9e7-d69ab4bde5e3)
 Call ID: 61b21874-0802-4390-a9e7-d69ab4bde5e3
  Args:
    type: :Man
    source: PrincePhilipDukeOfEdinburgh
  AddTriple (206b5771-854e-471e-8999-f164ba1666df)
 Call ID: 206b5771-854e-471e-8999-f164ba1666df
  Args:
    source: PrincePhilipDukeOfEdinburgh
    relation: :hasFather
    target: PrinceAndrewOfGreeceAndDenmark
  Finish (b8fa2550-53ab-43fe-9056-45ffeb5dc615)
 Call ID: b8fa2550-53ab-43fe-9056-45ffeb5dc615
  Args: