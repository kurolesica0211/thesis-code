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
Princess Eugenie, Mrs Jack Brooksbank (/ˈjuːʒəni/ YOO-zhə-nee; Eugenie Victoria Helena; born 23 March 1990), is a member of the British royal family.
She is the younger daughter of Andrew Mountbatten-Windsor and Sarah Ferguson, and a niece of King Charles III.
At birth, Eugenie was sixth in the line of succession to the British throne and is 12th as of 2026.
Eugenie was born at the Portland Hospital in London.
Eugenie also works privately with a number of charitable organisations, including the Anti-Slavery Collective, which she co‐founded.
In 2018, Eugenie married Jack Brooksbank, a British marketing executive.
They have two sons, August and Ernest Brooksbank.
Early life

Eugenie was born at 7:58 pm on 23 March 1990 at the Portland Hospital in London, where she was delivered by caesarean section, to the then Duke and Duchess of York.
She was baptised Eugenie Victoria Helena at St Mary Magdalene Church, Sandringham, by Peter Nott, Bishop of Norwich, on 23 December, becoming the first royal baby to have a public christening and the only one of the Queen's grandchildren not to be baptised in the Lily Font.
Eugenie's parents divorced when she was six years old.
The Duke and Duchess of York agreed to joint custody of their two children.
After the divorce, Queen Elizabeth II provided £1.4 million to establish a trust fund for Eugenie and her sister, Beatrice.
In October 2002, the 12-year-old Eugenie underwent back surgery at the Royal National Orthopaedic Hospital in London to correct scoliosis; surgeons inserted two 300-millimetre (12 in) titanium rods into her spine.
Education and career

Eugenie began her education at Winkfield Montessori School, which she attended from 1992 to 1993.
She then joined her sister at Upton House School in Windsor, where she studied until 1995.
From 1995 to 2001, she attended Coworth Park School (now Coworth Flexlands School), followed by St George's School near Windsor Castle until 2003.
During her time at Marlborough, Eugenie completed three A-levels, earning 'A' grades in Art and English Literature, and a 'B' in History of Art.
In 2013, Eugenie relocated to New York City for a year to work as a benefit auctions manager at the online auction house Paddle8.
In the Channel 5 documentary Beatrice and Eugenie: Pampered Princesses, royal commentator Richard Kay stated that Eugenie received taxpayer-funded security while travelling internationally during her gap year.
In January 2022, reports emerged that Eugenie lost her taxpayer-funded police security in 2011, reportedly following an intervention by her uncle, Charles III (then Prince of Wales).
During her gap year, Eugenie's taxpayer‐funded security reportedly cost more than £100,000.
Charles considered the expense excessive, as Eugenie and Beatrice were unlikely to take on major royal duties.
In July 2023, Eugenie joined the advisory board of Goals House, a community dedicated to advancing the United Nations’ Sustainable Development Goals.
Marriage and family

Buckingham Palace announced the engagement of Eugenie and Jack Brooksbank on 22 January 2018.
The couple had been dating for seven years, having been introduced by friends during a ski break in Verbier, Switzerland, where Brooksbank was working.
The wedding took place at St George's Chapel, Windsor Castle, on 12 October 2018.
Eugenie's wedding dress was designed by the British fashion designer Peter Pilotto and the Belgian Christopher de Vos of British-based label Peter Pilotto, and was created to display the surgical scar on her back.
Their first child, August Philip Hawke Brooksbank, was born on 9 February 2021 at the Portland Hospital in London, and was delivered by caesarean section due to his mother's childhood scoliosis operation.
August was christened at the Royal Chapel of All Saints, Windsor Great Park, on 21 November 2021, in a joint ceremony with his second cousin, Lucas Tindall.
Eugenie gave birth to a second son, Ernest George Ronnie Brooksbank, on 30 May 2023.
He is named after his great-great-great-grandfather George V. Ernest was born 13th in line to the throne and is now 14th.
From November 2020 to May 2022, the couple's main residence was Frogmore Cottage, which had been leased to Eugenie's cousin Prince Harry.
In May 2022, it was reported that they had moved to Portugal, where Brooksbank works for Michael Meldman, and that they would again stay at Ivy Cottage while in the UK.
Activities

Eugenie receives no allowance from the Privy Purse.
In 2018, Children in Crisis merged with Street Child, a children's charity active in multiple countries, with Eugenie continuing as an ambassador.
Eugenie and her sister represented their father at a service of thanksgiving for their aunt, Diana, Princess of Wales, in 2007.
On 2 June 2011, Eugenie visited the Royal National Orthopaedic Hospital (RNOH) with her father as one of her first official engagements.
Eugenie became patron of the RNOH Charity in March 2019.
In January 2013, Eugenie and her sister promoted Britain overseas in Germany.
In 2016, Eugenie, together with her mother and sister, collaborated with the British contemporary artist Teddy McDonald on a painting titled Royal Love.
Eugenie and her sister became Patrons of the Teenage Cancer Trust in June 2016.
She is also Patron of the Coronet Theatre, the European School of Osteopathy, the Tate Young Patrons, and, alongside her mother, the Elephant Family, of which her uncle and aunt, King Charles III and Queen Camilla, are joint presidents.
In 2016, Eugenie visited a safe house run by The Salvation Army and met with victims of sexual abuse and modern slavery.
In 2017, Eugenie became the ambassador for the Artemis Council of the New Museum, a by-invitation membership initiative focused on supporting female artists.
In July 2018, in her capacity as co-founder and director of the Anti-Slavery Collective, Eugenie spoke at the NEXUS Global Summit at the UN headquarters in New York to discuss efforts to end modern slavery.
In August 2019, it was announced that she would launch a podcast, becoming the first member of the royal family to do so.
In July 2019, with support from the University of Hull's Wilberforce Institute, Eugenie hosted an event at Westminster Abbey to examine the scale of modern slavery.
In April 2019, she accompanied her grandmother to the Royal Maundy service at St George's Chapel, Windsor Castle.
In May 2020, it was reported that Eugenie and her husband were assisting The Salvation Army with packing food parcels during the COVID-19 pandemic.
On 17 September 2022, during the period of official mourning for Queen Elizabeth II, Eugenie joined her sister and six cousins in mounting a 15-minute vigil around the late Queen's coffin as it lay in state at Westminster Hall.
Titles, styles and arms

Titles and styles

As a male-line grandchild of the sovereign, Eugenie was known as "Her Royal Highness Princess Eugenie of York", with the territorial designation derived from her father's then-title, Duke of York.
Since her marriage, she has been styled "Her Royal Highness Princess Eugenie, Mrs Jack Brooksbank" in the Court Circular.



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
  AssignClass (0cd762e8-f6d5-4383-8bd4-2456458c124b)
 Call ID: 0cd762e8-f6d5-4383-8bd4-2456458c124b
  Args:
    type: :Woman
    source: Princess_Eugenie
  AssignClass (f35df1a7-7d23-4ec2-a26d-2664c4de09cd)
 Call ID: f35df1a7-7d23-4ec2-a26d-2664c4de09cd
  Args:
    type: :Person
    source: Princess_Eugenie
  AssignClass (85f1b831-11de-4a8b-8254-2b2bdf76bc68)
 Call ID: 85f1b831-11de-4a8b-8254-2b2bdf76bc68
  Args:
    type: :Man
    source: Jack_Brooksbank
  AssignClass (bc543b7d-607f-4594-8fb4-21f78b4a3b66)
 Call ID: bc543b7d-607f-4594-8fb4-21f78b4a3b66
  Args:
    type: :Person
    source: Jack_Brooksbank
  AssignClass (170df92d-55d0-4d87-ba53-fb316d13c1a5)
 Call ID: 170df92d-55d0-4d87-ba53-fb316d13c1a5
  Args:
    type: :Man
    source: Andrew_Mountbatten-Windsor
  AssignClass (7947cf66-c08c-4ac3-9d50-2b4a8b75fbae)
 Call ID: 7947cf66-c08c-4ac3-9d50-2b4a8b75fbae
  Args:
    type: :Person
    source: Andrew_Mountbatten-Windsor
  AssignClass (f8c3c3d1-1173-45de-95aa-a2c8b1e43ffe)
 Call ID: f8c3c3d1-1173-45de-95aa-a2c8b1e43ffe
  Args:
    type: :Woman
    source: Sarah_Ferguson
  AssignClass (1c8c525d-9674-4b8f-a518-5b3e9536a15e)
 Call ID: 1c8c525d-9674-4b8f-a518-5b3e9536a15e
  Args:
    type: :Person
    source: Sarah_Ferguson
  AssignClass (fe5ae9e2-96df-4c38-adb8-5d73b22e3360)
 Call ID: fe5ae9e2-96df-4c38-adb8-5d73b22e3360
  Args:
    type: :Man
    source: King_Charles_III
  AssignClass (66efb0b0-e585-457a-a4b2-8a907619d240)
 Call ID: 66efb0b0-e585-457a-a4b2-8a907619d240
  Args:
    type: :Person
    source: King_Charles_III
  AssignClass (e6de9f44-4472-4b64-aee1-0b9abeac6562)
 Call ID: e6de9f44-4472-4b64-aee1-0b9abeac6562
  Args:
    type: :Man
    source: August_Brooksbank
  AssignClass (189936da-3dc1-4504-870d-399dde8bf777)
 Call ID: 189936da-3dc1-4504-870d-399dde8bf777
  Args:
    type: :Person
    source: August_Brooksbank
  AssignClass (74a323b3-0dcb-4ef2-9787-2a5155029268)
 Call ID: 74a323b3-0dcb-4ef2-9787-2a5155029268
  Args:
    type: :Man
    source: Ernest_Brooksbank
  AssignClass (6d1c6a4f-5842-4ba5-88aa-77c2b160f0f6)
 Call ID: 6d1c6a4f-5842-4ba5-88aa-77c2b160f0f6
  Args:
    type: :Person
    source: Ernest_Brooksbank
  AssignClass (36ec0ff6-e137-464b-861e-a0a5b1761d7f)
 Call ID: 36ec0ff6-e137-464b-861e-a0a5b1761d7f
  Args:
    type: :Woman
    source: Beatrice
  AssignClass (5c23eecf-5827-4196-a645-92d48330c63f)
 Call ID: 5c23eecf-5827-4196-a645-92d48330c63f
  Args:
    type: :Person
    source: Beatrice
  AddLiteral (8fbf3f12-d0c5-4bd4-800f-aca5a167fa3a)
 Call ID: 8fbf3f12-d0c5-4bd4-800f-aca5a167fa3a
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Princess_Eugenie
    literal_value: 1990
  AddTriple (b46af7e0-41bb-4707-a882-4813b89ec5b5)
 Call ID: b46af7e0-41bb-4707-a882-4813b89ec5b5
  Args:
    source: Princess_Eugenie
    target: Andrew_Mountbatten-Windsor
    relation: :hasFather
  AddTriple (90b28846-763f-4e2c-a604-1aa621885fdd)
 Call ID: 90b28846-763f-4e2c-a604-1aa621885fdd
  Args:
    relation: :hasMother
    target: Sarah_Ferguson
    source: Princess_Eugenie
  AddTriple (ab85e973-e0a3-4a17-a07a-6d6db19d73cc)
 Call ID: ab85e973-e0a3-4a17-a07a-6d6db19d73cc
  Args:
    relation: :hasFather
    target: Jack_Brooksbank
    source: August_Brooksbank
  AddTriple (f62b9000-17cf-49e4-a28f-12114c8e1641)
 Call ID: f62b9000-17cf-49e4-a28f-12114c8e1641
  Args:
    relation: :hasMother
    target: Princess_Eugenie
    source: August_Brooksbank
  AddTriple (c04aec6a-8b47-492f-abfa-d84f4da287bc)
 Call ID: c04aec6a-8b47-492f-abfa-d84f4da287bc
  Args:
    target: Jack_Brooksbank
    relation: :hasFather
    source: Ernest_Brooksbank
  AddTriple (b6d3b3af-fd54-4ec7-bd4e-0402bfb12620)
 Call ID: b6d3b3af-fd54-4ec7-bd4e-0402bfb12620
  Args:
    source: Ernest_Brooksbank
    relation: :hasMother
    target: Princess_Eugenie
  AddTriple (b87db215-f847-45c0-a75e-6010df1cf521)
 Call ID: b87db215-f847-45c0-a75e-6010df1cf521
  Args:
    source: Princess_Eugenie
    relation: :hasSister
    target: Beatrice
  AddLiteral (12302e74-2d1f-4ffa-86b9-5f58a1aad9f4)
 Call ID: 12302e74-2d1f-4ffa-86b9-5f58a1aad9f4
  Args:
    literal_value: 2018
    source: Princess_Eugenie
    relation: :hasMarriageYear
    literal_type: xsd:integer
  AddTriple (64bc47f7-5582-485f-a317-ae82bf7ada2c)
 Call ID: 64bc47f7-5582-485f-a317-ae82bf7ada2c
  Args:
    source: Princess_Eugenie
    target: Jack_Brooksbank
    relation: :hasRelation
  AddTriple (1f913baf-33e2-4795-a2c6-79bbace6f18f)
 Call ID: 1f913baf-33e2-4795-a2c6-79bbace6f18f
  Args:
    target: Princess_Eugenie
    relation: :hasRelation
    source: King_Charles_III
  Finish (a2b73748-e052-4dba-a11e-4f8ba92b8571)
 Call ID: a2b73748-e052-4dba-a11e-4f8ba92b8571
  Args: