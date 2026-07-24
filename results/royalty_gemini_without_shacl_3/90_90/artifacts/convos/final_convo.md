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
  AssignClass (66e8ab50-f668-42aa-aeba-df4cdff06a47)
 Call ID: 66e8ab50-f668-42aa-aeba-df4cdff06a47
  Args:
    source: Princess_Marina_of_Greece_and_Denmark
    type: :Woman
  AssignClass (4a949b4d-6288-46d9-9de9-14ceb768dd7b)
 Call ID: 4a949b4d-6288-46d9-9de9-14ceb768dd7b
  Args:
    source: Princess_Marina_of_Greece_and_Denmark
    type: :Person
  AddLiteral (257969d8-4c50-4402-bc38-beee983aa075)
 Call ID: 257969d8-4c50-4402-bc38-beee983aa075
  Args:
    literal_type: xsd:integer
    literal_value: 1906
    relation: :hasBirthYear
    source: Princess_Marina_of_Greece_and_Denmark
  AddLiteral (565ea7eb-4cc8-4579-ae6f-e3db0f297dcb)
 Call ID: 565ea7eb-4cc8-4579-ae6f-e3db0f297dcb
  Args:
    source: Princess_Marina_of_Greece_and_Denmark
    relation: :hasDeathYear
    literal_value: 1968
    literal_type: xsd:integer
  AssignClass (bb33d63a-3169-48c9-b721-28945ebf690d)
 Call ID: bb33d63a-3169-48c9-b721-28945ebf690d
  Args:
    type: :Man
    source: Prince_Nicholas_of_Greece_and_Denmark
  AssignClass (3ac3a918-0896-4c09-8185-dc69bffc8c78)
 Call ID: 3ac3a918-0896-4c09-8185-dc69bffc8c78
  Args:
    source: Prince_Nicholas_of_Greece_and_Denmark
    type: :Person
  AssignClass (1d52058d-763b-44e5-b53d-f00cc994eb86)
 Call ID: 1d52058d-763b-44e5-b53d-f00cc994eb86
  Args:
    source: Grand_Duchess_Elena_Vladimirovna_of_Russia
    type: :Woman
  AssignClass (02c990fe-5fbb-4871-924b-2a8f4fc91693)
 Call ID: 02c990fe-5fbb-4871-924b-2a8f4fc91693
  Args:
    type: :Person
    source: Grand_Duchess_Elena_Vladimirovna_of_Russia
  AddTriple (83b935c3-8789-43c8-aa7f-82272451ade4)
 Call ID: 83b935c3-8789-43c8-aa7f-82272451ade4
  Args:
    source: Princess_Marina_of_Greece_and_Denmark
    target: Prince_Nicholas_of_Greece_and_Denmark
    relation: :hasFather
  AddTriple (3e85d146-480d-4ff7-8b60-4e10a5e0a917)
 Call ID: 3e85d146-480d-4ff7-8b60-4e10a5e0a917
  Args:
    relation: :hasMother
    target: Grand_Duchess_Elena_Vladimirovna_of_Russia
    source: Princess_Marina_of_Greece_and_Denmark
  AssignClass (fe43454a-e6c1-4bea-a642-e8d8bd194d8a)
 Call ID: fe43454a-e6c1-4bea-a642-e8d8bd194d8a
  Args:
    type: :Man
    source: Prince_George_Duke_of_Kent
  AssignClass (b2c578e8-15b2-449c-92f7-c6a458459e01)
 Call ID: b2c578e8-15b2-449c-92f7-c6a458459e01
  Args:
    source: Prince_George_Duke_of_Kent
    type: :Person
  AddLiteral (1c9fa364-d056-49f5-b3e9-2b6e7b1304b3)
 Call ID: 1c9fa364-d056-49f5-b3e9-2b6e7b1304b3
  Args:
    literal_value: 1934
    literal_type: xsd:integer
    relation: :hasMarriageYear
    source: Princess_Marina_of_Greece_and_Denmark
  AddTriple (97f67ba1-a5ca-4cd6-9786-5848368e356a)
 Call ID: 97f67ba1-a5ca-4cd6-9786-5848368e356a
  Args:
    target: Prince_George_Duke_of_Kent
    relation: :hasRelation
    source: Princess_Marina_of_Greece_and_Denmark
  AssignClass (e998deba-72ac-4ee9-ad6c-8c6f008e5e9a)
 Call ID: e998deba-72ac-4ee9-ad6c-8c6f008e5e9a
  Args:
    source: King_George_I_of_Greece
    type: :Man
  AssignClass (5f0c8d42-5d0c-41c0-afce-d2fe1feeb38c)
 Call ID: 5f0c8d42-5d0c-41c0-afce-d2fe1feeb38c
  Args:
    source: King_George_I_of_Greece
    type: :Person
  AssignClass (b45f4402-6d62-46e6-b940-2f914748df74)
 Call ID: b45f4402-6d62-46e6-b940-2f914748df74
  Args:
    source: Queen_Olga_of_Greece
    type: :Woman
  AssignClass (eb834dac-f925-4a48-92d2-f180b16fd3c3)
 Call ID: eb834dac-f925-4a48-92d2-f180b16fd3c3
  Args:
    source: Queen_Olga_of_Greece
    type: :Person
  AddTriple (0e020bff-d062-4f73-b3fb-f2567bfe9a2a)
 Call ID: 0e020bff-d062-4f73-b3fb-f2567bfe9a2a
  Args:
    relation: :isFatherOf
    target: Prince_Nicholas_of_Greece_and_Denmark
    source: King_George_I_of_Greece
  AddTriple (6e8fa7a2-34ed-4e07-a850-e197e68f22c1)
 Call ID: 6e8fa7a2-34ed-4e07-a850-e197e68f22c1
  Args:
    source: Queen_Olga_of_Greece
    relation: :isMotherOf
    target: Prince_Nicholas_of_Greece_and_Denmark
  AssignClass (b382fe53-b4ae-425f-81f2-c73ef30c4321)
 Call ID: b382fe53-b4ae-425f-81f2-c73ef30c4321
  Args:
    source: Grand_Duke_Vladimir_Alexandrovich
    type: :Man
  AssignClass (5f432643-fe58-4360-915e-eb51ec88fd59)
 Call ID: 5f432643-fe58-4360-915e-eb51ec88fd59
  Args:
    type: :Person
    source: Grand_Duke_Vladimir_Alexandrovich
  AssignClass (13700999-7e63-4987-a1d1-c53440ed1959)
 Call ID: 13700999-7e63-4987-a1d1-c53440ed1959
  Args:
    type: :Woman
    source: Grand_Duchess_Maria_Pavlovna_of_Russia
  AssignClass (ff605eb6-226b-420b-a572-10b781fd204a)
 Call ID: ff605eb6-226b-420b-a572-10b781fd204a
  Args:
    source: Grand_Duchess_Maria_Pavlovna_of_Russia
    type: :Person
  AddTriple (a0a7bb4c-4543-407b-9840-5810d8944859)
 Call ID: a0a7bb4c-4543-407b-9840-5810d8944859
  Args:
    target: Grand_Duchess_Elena_Vladimirovna_of_Russia
    relation: :isFatherOf
    source: Grand_Duke_Vladimir_Alexandrovich
  AddTriple (3d4a0c9d-9f4e-4858-b933-e9e6212fce5b)
 Call ID: 3d4a0c9d-9f4e-4858-b933-e9e6212fce5b
  Args:
    source: Grand_Duchess_Maria_Pavlovna_of_Russia
    target: Grand_Duchess_Elena_Vladimirovna_of_Russia
    relation: :isMotherOf
  AssignClass (edcfae57-9296-4474-96c9-b8a70f23e78c)
 Call ID: edcfae57-9296-4474-96c9-b8a70f23e78c
  Args:
    type: :Woman
    source: Princess_Olga
  AssignClass (50685d62-05d2-456b-9d35-d6d1a5b0c51d)
 Call ID: 50685d62-05d2-456b-9d35-d6d1a5b0c51d
  Args:
    source: Princess_Olga
    type: :Person
  AssignClass (afaf0fe7-0ec2-49e3-a36a-2dd16ec0c0eb)
 Call ID: afaf0fe7-0ec2-49e3-a36a-2dd16ec0c0eb
  Args:
    source: Princess_Elizabeth
    type: :Woman
  AssignClass (76ece832-adbf-4c11-91fc-f9ac9668d5cf)
 Call ID: 76ece832-adbf-4c11-91fc-f9ac9668d5cf
  Args:
    type: :Person
    source: Princess_Elizabeth
  AddTriple (08d26d78-5c16-4569-a804-07b5fce97272)
 Call ID: 08d26d78-5c16-4569-a804-07b5fce97272
  Args:
    source: Princess_Marina_of_Greece_and_Denmark
    target: Princess_Olga
    relation: :hasSister
  AddTriple (8ef0031f-1678-489c-99ab-7a815a8ee30b)
 Call ID: 8ef0031f-1678-489c-99ab-7a815a8ee30b
  Args:
    target: Princess_Elizabeth
    relation: :hasSister
    source: Princess_Marina_of_Greece_and_Denmark
  AssignClass (cdb59907-cde0-4a16-a5d9-39729edf7d29)
 Call ID: cdb59907-cde0-4a16-a5d9-39729edf7d29
  Args:
    type: :Man
    source: Prince_Paul_of_Yugoslavia
  AssignClass (a58033a2-62a1-40c1-845e-c15176fc2378)
 Call ID: a58033a2-62a1-40c1-845e-c15176fc2378
  Args:
    type: :Person
    source: Prince_Paul_of_Yugoslavia
  AddLiteral (ab288aa9-c3c9-4675-921e-918352543803)
 Call ID: ab288aa9-c3c9-4675-921e-918352543803
  Args:
    source: Princess_Olga
    relation: :hasMarriageYear
    literal_value: 1923
    literal_type: xsd:integer
  AddTriple (83ca643d-7b44-40a1-b184-c81350d8c0ef)
 Call ID: 83ca643d-7b44-40a1-b184-c81350d8c0ef
  Args:
    relation: :hasRelation
    target: Prince_Paul_of_Yugoslavia
    source: Princess_Olga
  AssignClass (f50458a4-2fc6-4a97-866d-0383f7ad30b7)
 Call ID: f50458a4-2fc6-4a97-866d-0383f7ad30b7
  Args:
    source: Edward
    type: :Man
  AssignClass (3a21a06f-8aeb-4297-af88-7af994eea6cf)
 Call ID: 3a21a06f-8aeb-4297-af88-7af994eea6cf
  Args:
    type: :Person
    source: Edward
  AssignClass (8932f3b8-7981-4f20-886c-691d1ae7fcb0)
 Call ID: 8932f3b8-7981-4f20-886c-691d1ae7fcb0
  Args:
    source: Alexandra
    type: :Woman
  AssignClass (6a38e0bf-9b95-4a43-b30a-e14e18f0e543)
 Call ID: 6a38e0bf-9b95-4a43-b30a-e14e18f0e543
  Args:
    source: Alexandra
    type: :Person
  AssignClass (9252ac96-4f44-4d6b-9f07-f1bf29af49f9)
 Call ID: 9252ac96-4f44-4d6b-9f07-f1bf29af49f9
  Args:
    type: :Man
    source: Michael
  AssignClass (6974e525-3f58-4ac5-a9f8-bec925e3c08f)
 Call ID: 6974e525-3f58-4ac5-a9f8-bec925e3c08f
  Args:
    type: :Person
    source: Michael
  AddTriple (5b6871c0-6a28-4f23-86ca-6ed65df584e2)
 Call ID: 5b6871c0-6a28-4f23-86ca-6ed65df584e2
  Args:
    source: Prince_George_Duke_of_Kent
    relation: :hasSon
    target: Edward
  AddTriple (b9e5efb8-d7ca-4ddb-b5c6-92cb5a65268d)
 Call ID: b9e5efb8-d7ca-4ddb-b5c6-92cb5a65268d
  Args:
    source: Prince_George_Duke_of_Kent
    relation: :hasDaughter
    target: Alexandra
  AddTriple (859996e8-7612-4257-b7db-6877bc4b0bef)
 Call ID: 859996e8-7612-4257-b7db-6877bc4b0bef
  Args:
    relation: :hasSon
    target: Michael
    source: Prince_George_Duke_of_Kent
  AddTriple (d2d814ad-fc7d-4055-b402-5669c22845e4)
 Call ID: d2d814ad-fc7d-4055-b402-5669c22845e4
  Args:
    source: Edward
    target: Princess_Marina_of_Greece_and_Denmark
    relation: :hasMother
  AddTriple (c14c0d5e-b281-4d87-a311-98d0213dfb6e)
 Call ID: c14c0d5e-b281-4d87-a311-98d0213dfb6e
  Args:
    target: Princess_Marina_of_Greece_and_Denmark
    relation: :hasMother
    source: Alexandra
  AddTriple (12019da7-14dc-4963-a2b0-bcc949d66171)
 Call ID: 12019da7-14dc-4963-a2b0-bcc949d66171
  Args:
    target: Princess_Marina_of_Greece_and_Denmark
    relation: :hasMother
    source: Michael
  AssignClass (6cc165c0-9085-4d45-b9a9-c5dc52ec29c5)
 Call ID: 6cc165c0-9085-4d45-b9a9-c5dc52ec29c5
  Args:
    type: :Man
    source: King_George_V
  AssignClass (bc30be9c-0d58-4a2f-b128-9b375297c94f)
 Call ID: bc30be9c-0d58-4a2f-b128-9b375297c94f
  Args:
    type: :Person
    source: King_George_V
  AssignClass (ebc1f922-9a0d-4c90-9a79-d63a1994758e)
 Call ID: ebc1f922-9a0d-4c90-9a79-d63a1994758e
  Args:
    type: :Woman
    source: Queen_Mary
  AssignClass (26501172-ce1a-46c0-84be-0b8a01927bd1)
 Call ID: 26501172-ce1a-46c0-84be-0b8a01927bd1
  Args:
    source: Queen_Mary
    type: :Person
  AddTriple (b3770ca3-199c-4511-8ef3-e74c59fd1e30)
 Call ID: b3770ca3-199c-4511-8ef3-e74c59fd1e30
  Args:
    source: Prince_George_Duke_of_Kent
    target: King_George_V
    relation: :hasFather
  AddTriple (e17b5357-6f5a-46cf-badf-5e86b67b37f5)
 Call ID: e17b5357-6f5a-46cf-badf-5e86b67b37f5
  Args:
    relation: :hasMother
    target: Queen_Mary
    source: Prince_George_Duke_of_Kent
  AssignClass (6a44c3aa-614e-463b-b2c1-72b91d2fe5b9)
 Call ID: 6a44c3aa-614e-463b-b2c1-72b91d2fe5b9
  Args:
    source: Christian_IX_of_Denmark
    type: :Man
  AssignClass (e062f943-d490-4772-8d27-56aaaee6f92a)
 Call ID: e062f943-d490-4772-8d27-56aaaee6f92a
  Args:
    type: :Person
    source: Christian_IX_of_Denmark
  AssignClass (4d47d3c8-eecb-47c1-b7c8-d264ce67d507)
 Call ID: 4d47d3c8-eecb-47c1-b7c8-d264ce67d507
  Args:
    source: Emperor_Alexander_II_of_Russia
    type: :Man
  AssignClass (b4aad1b0-9120-412a-88d9-bb6f83728250)
 Call ID: b4aad1b0-9120-412a-88d9-bb6f83728250
  Args:
    type: :Person
    source: Emperor_Alexander_II_of_Russia
  AddTriple (b71fcd66-beb4-47eb-94de-8fe1d10eff69)
 Call ID: b71fcd66-beb4-47eb-94de-8fe1d10eff69
  Args:
    target: Christian_IX_of_Denmark
    relation: :hasAncestor
    source: Princess_Marina_of_Greece_and_Denmark
  AddTriple (32e9b661-3a04-4a7d-bf5a-e371f1adb9bb)
 Call ID: 32e9b661-3a04-4a7d-bf5a-e371f1adb9bb
  Args:
    relation: :hasAncestor
    target: Emperor_Alexander_II_of_Russia
    source: Princess_Marina_of_Greece_and_Denmark
  AssignClass (1b2665bc-db63-476e-a861-341e8aec9ad6)
 Call ID: 1b2665bc-db63-476e-a861-341e8aec9ad6
  Args:
    source: Prince_Andrew_of_Greece_and_Denmark
    type: :Man
  AssignClass (da56b9ea-a17c-47db-9aaa-adb8822782f5)
 Call ID: da56b9ea-a17c-47db-9aaa-adb8822782f5
  Args:
    source: Prince_Andrew_of_Greece_and_Denmark
    type: :Person
  AssignClass (f3541d9f-c8dd-46b8-87ff-72a08e34bc49)
 Call ID: f3541d9f-c8dd-46b8-87ff-72a08e34bc49
  Args:
    type: :Man
    source: Prince_Philip_Duke_of_Edinburgh
  AssignClass (922d4ce7-3dad-4be1-ae1e-91e19506caba)
 Call ID: 922d4ce7-3dad-4be1-ae1e-91e19506caba
  Args:
    type: :Person
    source: Prince_Philip_Duke_of_Edinburgh
  AddTriple (4b49c4f9-9920-4568-a8b3-5338062b876c)
 Call ID: 4b49c4f9-9920-4568-a8b3-5338062b876c
  Args:
    target: Prince_Philip_Duke_of_Edinburgh
    relation: :isFatherOf
    source: Prince_Andrew_of_Greece_and_Denmark
  AddTriple (b644b92a-84aa-4ea0-8e0c-be0b76c12189)
 Call ID: b644b92a-84aa-4ea0-8e0c-be0b76c12189
  Args:
    source: Prince_Andrew_of_Greece_and_Denmark
    relation: :hasFather
    target: King_George_I_of_Greece
  Finish (f41706e8-211e-4da9-bd3e-44a2ae900778)
 Call ID: f41706e8-211e-4da9-bd3e-44a2ae900778
  Args: