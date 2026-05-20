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
Princess Beatrice, Mrs Edoardo Mapelli Mozzi (Beatrice Elizabeth Mary; born 8 August 1988), is a member of the British royal family.
Beatrice was educated at St George's School, Ascot, before reading history at Goldsmiths, University of London, where she graduated with a BA degree.
In 2020, Beatrice married Edoardo Mapelli Mozzi, an English-born property developer with descent from Italian nobility.
Early life and education

Beatrice was born at 8:18 pm on 8 August 1988 at the Portland Hospital in London, to the then Duke and Duchess of York.
Beatrice was baptised in the Chapel Royal at St James's Palace on 20 December.
Her younger sister, Princess Eugenie, was born in 1990.
Beatrice's parents divorced amicably when she was seven years old and agreed to joint custody of their two children.
After the divorce, the Queen provided her parents with £1.4 million to establish a trust fund for her and Eugenie.
Beatrice and her sister frequently travelled abroad, always with one or both of their parents.
Beatrice began her early education at the independent Upton House School in Windsor in 1991.
Beatrice continued her education at the independent St George's School in Ascot, where she was a pupil from 2000 to 2007.
Beatrice celebrated her 18th birthday with a masked ball at Windsor Castle in July 2006.
In September 2008, Beatrice began a three-year course at Goldsmiths, University of London, to read history and history of ideas, graduating in 2011 with a BA (2:1 degree).
Career

During the summer of 2008, Beatrice obtained work experience as a sales assistant at Selfridges.
Beatrice became the first member of the family to appear in a non-documentary film when she had a small, non-speaking role as an extra in The Young Victoria (2009), based on the accession and early reign of her ancestor Queen Victoria.
In April 2015, it was reported that Beatrice had decided to move to New York City.
By April 2017, she held a full-time job and divided her time between London and New York.
Known professionally as Beatrice York, she served as Vice‐President of Partnerships and Strategy at Afiniti from 2016 to 2025.
In January 2022, it was reported that Beatrice had lost her taxpayer-funded police security in 2011, reportedly after her uncle Charles (then Prince of Wales) intervened as part of a cost-cutting initiative.
In 2025, Beatrice launched Purpose Economy Intelligence Ltd alongside Luis Alvarado Martínez, a Spanish‐born executive who has worked at the World Economic Forum since 2021.
Duties and appointments

Beatrice and Prince Philip, Duke of Edinburgh accompanied Queen Elizabeth II to the traditional Royal Maundy services on 5 April 2012 in York.
There, Beatrice interacted with parishioners, received flowers from the public, and assisted the Queen in giving Maundy money to the pensioners.
In 2013, Beatrice and her sister promoted Britain overseas in Germany.
She visited the Isle of Wight in 2014, whose former Governor had been her namesake Princess Beatrice, daughter of Queen Victoria.
On 17 September 2022, during the period of official mourning for Queen Elizabeth II, Beatrice joined her sister and six cousins to mount a 15-minute vigil around the late Queen's coffin as it lay in state at Westminster Hall.
Upon the accession of Charles III, her position in the line of succession made Beatrice eligible to be appointed a Counsellor of State.
Personal life

Early relationships

Beatrice briefly dated Paolo Liuzzo in 2006, an Italo-American whose previous charge for assault and battery caused controversy at the time.
Marriage and family

In March 2019, Beatrice attended a fundraising event at the National Portrait Gallery in London accompanied by the Anglo-Italian property developer Edoardo Mapelli Mozzi.
The only son of Alex Mapelli-Mozzi, a former Alpine skier for the Great Britain Olympic team, he is a legitimate male‐line descendant of the Mapelli Mozzi family, whose members were granted the title of Count of the Kingdom of Italy in 1913 by King Victor Emmanuel III, with remainder to all male descendants of Edoardo's great‐grandfather Paolo Mapelli Mozzi (1854–1921).
They attended the May 2019 wedding of Lady Gabriella Windsor, Beatrice's second cousin once removed.
Beatrice and Mapelli Mozzi became engaged in Italy in September 2019, with their betrothal formally announced by Andrew's office on 26 September.
Beatrice married Mapelli Mozzi in a private ceremony on 17 July 2020 at the Royal Chapel of All Saints, Royal Lodge, Windsor.
Although Andrew walked Beatrice down the aisle, he did not appear in the official wedding portraits released by Buckingham Palace.
Beatrice wore a remodelled Sir Norman Hartnell gown lent by the Queen, and the Queen Mary Fringe Tiara, which the Queen had worn at her own wedding.
Beatrice has a stepson, Christopher Woolf ("Wolfie"), from her husband's previous relationship with the architect Dara Huang.
She gave birth to a daughter, Sienna Elizabeth Mapelli Mozzi, on 18 September 2021 at the Chelsea and Westminster Hospital in London.
At birth, Sienna was 11th in line to the British throne, and following the death of Queen Elizabeth II on 8 September 2022, she is now 10th.
Beatrice and her husband initially lived in a four-bedroom apartment at St James's Palace, but reportedly moved to a manor house in the Cotswolds in late 2022.
Beatrice gave birth to their second daughter, Athena Elizabeth Rose, on 22 January 2025 at the Chelsea and Westminster Hospital in London, several weeks prematurely.
Charity work

In 2002, Beatrice visited children living with HIV in Russia.
In an interview to mark her 18th birthday, Beatrice said she wished to use her position to assist others through charity work; she had already undertaken charitable duties alongside her mother through the various organisations supported by the Duchess.
In April 2010, Beatrice became the first member of the British royal family to complete the London Marathon, running to raise money for Children in Crisis.
At the April 2011 wedding of her cousin Prince William, Beatrice's unusual fascinator, designed by Philip Treacy, attracted significant public and media attention.
In November 2012, Beatrice became a patron of the York Musical Society.
In 2016, she, her mother, and her sister Eugenie collaborated with the British contemporary artist Teddy McDonald to create the first royal contemporary art painting.
In 2018, Children in Crisis merged with Street Child, a children's charity active in multiple countries, with Beatrice serving as its ambassador.
Beatrice took part in a South Asia Tour in 2016 that lasted nine days.
A few weeks later, she attended the 2016 Asia Game Changer Awards Dinner at the United Nations in New York City, which honoured Ruit and others.
Beatrice is the founder of Big Change, a charity she established with six friends to encourage young people to develop skills "outside a traditional academic curriculum".
In May 2018, she attended the Met Gala in New York City.
In March 2019, Beatrice was elected to the board of the UK charity the Outward Bound Trust as a trustee, after her father succeeded to the royal patronage from his father, the Duke of Edinburgh.
In May 2019, she was honoured at a New York City gala for her work with Friends Without a Border.
In February 2023, Beatrice was named patron of the British Skin Foundation.
In November 2025, Beatrice was appointed deputy patron of Outward Bound Trust.
Titles, styles, and arms

Titles and styles

As a male-line grandchild of the British sovereign, Beatrice was known at birth as "Her Royal Highness Princess Beatrice of York", the territorial designation deriving from her father's former title, Duke of York.
Since her marriage, she has been styled in the Court Circular as "Her Royal Highness Princess Beatrice, Mrs Edoardo Mapelli Mozzi".



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
  AssignClass (94b039fb-2fa7-4ced-a07a-bb3335b3e196)
 Call ID: 94b039fb-2fa7-4ced-a07a-bb3335b3e196
  Args:
    source: Princess Beatrice
    type: :Person
  AssignClass (f594fbfd-7d63-43a6-8e85-bd34abd4d52a)
 Call ID: f594fbfd-7d63-43a6-8e85-bd34abd4d52a
  Args:
    type: :Woman
    source: Princess Beatrice
  AddLiteral (c41e0f2d-3933-45be-83b2-135222699eef)
 Call ID: c41e0f2d-3933-45be-83b2-135222699eef
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1988
    source: Princess Beatrice
  AssignClass (d893b219-7336-4647-9b28-92abf8db8642)
 Call ID: d893b219-7336-4647-9b28-92abf8db8642
  Args:
    source: Princess Eugenie
    type: :Person
  AssignClass (c4bb581d-0cba-488c-b7aa-ea30f37e631c)
 Call ID: c4bb581d-0cba-488c-b7aa-ea30f37e631c
  Args:
    source: Princess Eugenie
    type: :Woman
  AddTriple (1a423abd-073e-4530-9533-b5eb591ccc0f)
 Call ID: 1a423abd-073e-4530-9533-b5eb591ccc0f
  Args:
    target: Princess Beatrice
    relation: :isSisterOf
    source: Princess Eugenie
  AssignClass (53c7db5e-8c0f-4b42-97d6-08431159f5b0)
 Call ID: 53c7db5e-8c0f-4b42-97d6-08431159f5b0
  Args:
    type: :Person
    source: Edoardo Mapelli Mozzi
  AssignClass (d659698d-eed1-476e-9c6e-e521a5d84813)
 Call ID: d659698d-eed1-476e-9c6e-e521a5d84813
  Args:
    source: Edoardo Mapelli Mozzi
    type: :Man
  AddTriple (aae7d596-b2a0-49a4-a09b-013878cd76ca)
 Call ID: aae7d596-b2a0-49a4-a09b-013878cd76ca
  Args:
    source: Princess Beatrice
    relation: :hasRelation
    target: Edoardo Mapelli Mozzi
  AddLiteral (c8bbf315-074a-4b50-b185-c080fb66a472)
 Call ID: c8bbf315-074a-4b50-b185-c080fb66a472
  Args:
    literal_value: 2020
    literal_type: xsd:integer
    relation: :hasMarriageYear
    source: Princess Beatrice
  AssignClass (72e52df4-2844-43eb-9b09-b6c84ba920c9)
 Call ID: 72e52df4-2844-43eb-9b09-b6c84ba920c9
  Args:
    source: Sienna Elizabeth Mapelli Mozzi
    type: :Person
  AssignClass (251de19e-b932-4fdf-84a8-d8a6a049982e)
 Call ID: 251de19e-b932-4fdf-84a8-d8a6a049982e
  Args:
    source: Sienna Elizabeth Mapelli Mozzi
    type: :Woman
  AddTriple (464b2eee-1c63-49d3-8cf1-92b20a2c6bfe)
 Call ID: 464b2eee-1c63-49d3-8cf1-92b20a2c6bfe
  Args:
    source: Sienna Elizabeth Mapelli Mozzi
    relation: :isDaughterOf
    target: Princess Beatrice
  AddTriple (a45a7637-04c2-4991-a7b8-27d6e55178b8)
 Call ID: a45a7637-04c2-4991-a7b8-27d6e55178b8
  Args:
    relation: :isDaughterOf
    target: Edoardo Mapelli Mozzi
    source: Sienna Elizabeth Mapelli Mozzi
  AssignClass (a1af3fa8-d2b7-4461-841d-b19c37c59ce3)
 Call ID: a1af3fa8-d2b7-4461-841d-b19c37c59ce3
  Args:
    source: Athena Elizabeth Rose
    type: :Person
  AssignClass (4ff62661-754f-4a61-8889-3ae427bd15c7)
 Call ID: 4ff62661-754f-4a61-8889-3ae427bd15c7
  Args:
    type: :Woman
    source: Athena Elizabeth Rose
  AddTriple (a94d6a10-ed58-4aa6-b2e1-3570b7163aa7)
 Call ID: a94d6a10-ed58-4aa6-b2e1-3570b7163aa7
  Args:
    source: Athena Elizabeth Rose
    relation: :isDaughterOf
    target: Princess Beatrice
  AddTriple (8b906900-eea3-4c07-95f8-43a644f1796f)
 Call ID: 8b906900-eea3-4c07-95f8-43a644f1796f
  Args:
    target: Edoardo Mapelli Mozzi
    relation: :isDaughterOf
    source: Athena Elizabeth Rose
  AssignClass (ad6504a0-19e0-49ed-bd8e-9a6b8d103384)
 Call ID: ad6504a0-19e0-49ed-bd8e-9a6b8d103384
  Args:
    source: Alex Mapelli-Mozzi
    type: :Person
  AssignClass (bd07ec42-8962-45b6-8a4a-ea09fb80b6f1)
 Call ID: bd07ec42-8962-45b6-8a4a-ea09fb80b6f1
  Args:
    type: :Man
    source: Alex Mapelli-Mozzi
  AddTriple (baa17c9c-8d12-4458-a2f1-01d19f8f8e08)
 Call ID: baa17c9c-8d12-4458-a2f1-01d19f8f8e08
  Args:
    relation: :isFatherOf
    target: Edoardo Mapelli Mozzi
    source: Alex Mapelli-Mozzi
  AssignClass (4d42a6b8-989e-461f-8da6-ee2ff30ca097)
 Call ID: 4d42a6b8-989e-461f-8da6-ee2ff30ca097
  Args:
    source: Paolo Mapelli Mozzi
    type: :Person
  AssignClass (b4c5ae40-ac3c-4c32-8c0d-e74e7b69ffde)
 Call ID: b4c5ae40-ac3c-4c32-8c0d-e74e7b69ffde
  Args:
    type: :Man
    source: Paolo Mapelli Mozzi
  AddTriple (5481fb0d-6d58-4abe-bf1c-b16eded2ac5a)
 Call ID: 5481fb0d-6d58-4abe-bf1c-b16eded2ac5a
  Args:
    source: Paolo Mapelli Mozzi
    target: Edoardo Mapelli Mozzi
    relation: :isAncestorOf
  AssignClass (585bc626-b553-4104-8a92-32f61a7a658c)
 Call ID: 585bc626-b553-4104-8a92-32f61a7a658c
  Args:
    source: Christopher Woolf
    type: :Person
  AssignClass (d557093d-7057-4733-9aa4-5e8fa9bd21b2)
 Call ID: d557093d-7057-4733-9aa4-5e8fa9bd21b2
  Args:
    type: :Man
    source: Christopher Woolf
  AddTriple (6cdb5b2b-49ad-4b40-bb11-16743b7e8ca0)
 Call ID: 6cdb5b2b-49ad-4b40-bb11-16743b7e8ca0
  Args:
    source: Christopher Woolf
    target: Edoardo Mapelli Mozzi
    relation: :isSonOf
  AssignClass (a2953ff4-7deb-4499-9516-b8c97c59d77a)
 Call ID: a2953ff4-7deb-4499-9516-b8c97c59d77a
  Args:
    type: :Person
    source: Dara Huang
  AssignClass (8e46e66e-bad8-4ea8-9595-0267ab4277f8)
 Call ID: 8e46e66e-bad8-4ea8-9595-0267ab4277f8
  Args:
    source: Dara Huang
    type: :Woman
  AddTriple (ac53b261-77a6-4290-a7bf-36b71d389109)
 Call ID: ac53b261-77a6-4290-a7bf-36b71d389109
  Args:
    target: Christopher Woolf
    relation: :isMotherOf
    source: Dara Huang
  AssignClass (316c3c10-0297-4d5f-afda-84b26e8c9597)
 Call ID: 316c3c10-0297-4d5f-afda-84b26e8c9597
  Args:
    type: :Person
    source: Queen Victoria
  AssignClass (a2942958-42a5-4f0c-9d8b-d54984fc7899)
 Call ID: a2942958-42a5-4f0c-9d8b-d54984fc7899
  Args:
    type: :Woman
    source: Queen Victoria
  AddTriple (71e70a5f-d2f0-4a27-a0e2-f34c50b385d6)
 Call ID: 71e70a5f-d2f0-4a27-a0e2-f34c50b385d6
  Args:
    target: Princess Beatrice
    relation: :isAncestorOf
    source: Queen Victoria
  AssignClass (00ec0243-7592-407b-a167-14ce0d1841f7)
 Call ID: 00ec0243-7592-407b-a167-14ce0d1841f7
  Args:
    source: Charles III
    type: :Person
  AssignClass (98939aae-62b4-46d0-b6fd-2f07407f2158)
 Call ID: 98939aae-62b4-46d0-b6fd-2f07407f2158
  Args:
    type: :Man
    source: Charles III
  AddTriple (3fdc4986-e623-489a-a05d-ec520e9dc226)
 Call ID: 3fdc4986-e623-489a-a05d-ec520e9dc226
  Args:
    source: Charles III
    target: Princess Beatrice
    relation: :hasRelation
  AddLiteral (fbc2c01d-77ad-4681-a736-725e8aafa552)
 Call ID: fbc2c01d-77ad-4681-a736-725e8aafa552
  Args:
    relation: :knownAs
    literal_type: xsd:string
    literal_value: Beatrice York
    source: Princess Beatrice
  Finish (bf53ff15-b677-4200-b439-bcc318f6ba78)
 Call ID: bf53ff15-b677-4200-b439-bcc318f6ba78
  Args: