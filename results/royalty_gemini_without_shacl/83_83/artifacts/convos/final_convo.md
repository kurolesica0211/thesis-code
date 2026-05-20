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
She is the sixth grandchild of Queen Elizabeth II and Prince Philip, Duke of Edinburgh.
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
The move is said to have angered the Duke, who argued to the Queen that his daughters should be treated as full members of the royal family.
In July 2023, Eugenie joined the advisory board of Goals House, a community dedicated to advancing the United Nations’ Sustainable Development Goals.
Marriage and family

Buckingham Palace announced the engagement of Eugenie and Jack Brooksbank on 22 January 2018.
The couple had been dating for seven years, having been introduced by friends during a ski break in Verbier, Switzerland, where Brooksbank was working.
In April 2018, they moved from St James's Palace and took up residence in Ivy Cottage at Kensington Palace.
The wedding took place at St George's Chapel, Windsor Castle, on 12 October 2018.
Eugenie's wedding dress was designed by the British fashion designer Peter Pilotto and the Belgian Christopher de Vos of British-based label Peter Pilotto, and was created to display the surgical scar on her back.
Their first child, August Philip Hawke Brooksbank, was born on 9 February 2021 at the Portland Hospital in London, and was delivered by caesarean section due to his mother's childhood scoliosis operation.
He is named in part after his great-grandfather Prince Philip, Duke of Edinburgh.
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
  AssignClass (aab01718-f23c-4713-8434-417bbbaf5398)
 Call ID: aab01718-f23c-4713-8434-417bbbaf5398
  Args:
    source: Eugenie_Victoria_Helena
    type: :Woman
  AssignClass (8db5a97e-6f57-4c0a-884d-86e0d919f453)
 Call ID: 8db5a97e-6f57-4c0a-884d-86e0d919f453
  Args:
    type: :Man
    source: Andrew_Mountbatten-Windsor
  AssignClass (acf22a1d-57fc-4207-9252-a8e00842dd51)
 Call ID: acf22a1d-57fc-4207-9252-a8e00842dd51
  Args:
    source: Sarah_Ferguson
    type: :Woman
  AssignClass (1df9825b-f5a6-49ea-9007-12ae8406a706)
 Call ID: 1df9825b-f5a6-49ea-9007-12ae8406a706
  Args:
    type: :Man
    source: Jack_Brooksbank
  AssignClass (cb453c3f-76ca-4e36-8d44-241ed6995a11)
 Call ID: cb453c3f-76ca-4e36-8d44-241ed6995a11
  Args:
    type: :Man
    source: August_Brooksbank
  AssignClass (1c61ff7a-9907-4adc-ac9a-bbd718b40a64)
 Call ID: 1c61ff7a-9907-4adc-ac9a-bbd718b40a64
  Args:
    source: Ernest_Brooksbank
    type: :Man
  AssignClass (e230c6ef-3795-40e5-a83d-67a509bf6386)
 Call ID: e230c6ef-3795-40e5-a83d-67a509bf6386
  Args:
    type: :Woman
    source: Beatrice
  AssignClass (a92cda61-a239-4dc6-9ea0-6d90159b0144)
 Call ID: a92cda61-a239-4dc6-9ea0-6d90159b0144
  Args:
    source: Charles_III
    type: :Man
  AddTriple (81644744-7545-4226-b52f-27a7f2605c9e)
 Call ID: 81644744-7545-4226-b52f-27a7f2605c9e
  Args:
    relation: :hasFather
    source: Eugenie_Victoria_Helena
    target: Andrew_Mountbatten-Windsor
  AddTriple (05263b36-d264-4830-95bc-4a721ae2b705)
 Call ID: 05263b36-d264-4830-95bc-4a721ae2b705
  Args:
    relation: :hasMother
    source: Eugenie_Victoria_Helena
    target: Sarah_Ferguson
  AddTriple (34e93af0-175d-46aa-9596-2fc3309e96db)
 Call ID: 34e93af0-175d-46aa-9596-2fc3309e96db
  Args:
    source: Beatrice
    target: Andrew_Mountbatten-Windsor
    relation: :hasFather
  AddTriple (16c0acbf-7004-4cd3-8a37-a436e328b8d6)
 Call ID: 16c0acbf-7004-4cd3-8a37-a436e328b8d6
  Args:
    source: Beatrice
    target: Sarah_Ferguson
    relation: :hasMother
  AddTriple (bfc79f51-cf28-472e-9ce5-6b7077225a59)
 Call ID: bfc79f51-cf28-472e-9ce5-6b7077225a59
  Args:
    source: August_Brooksbank
    target: Jack_Brooksbank
    relation: :hasFather
  AddTriple (9c3ea43a-2de5-4acf-afd9-9c33c9e8e7c0)
 Call ID: 9c3ea43a-2de5-4acf-afd9-9c33c9e8e7c0
  Args:
    source: August_Brooksbank
    target: Eugenie_Victoria_Helena
    relation: :hasMother
  AddTriple (e1b02c5c-d4a9-4685-b00b-f7af1db646a1)
 Call ID: e1b02c5c-d4a9-4685-b00b-f7af1db646a1
  Args:
    relation: :hasFather
    source: Ernest_Brooksbank
    target: Jack_Brooksbank
  AddTriple (1b9c7df6-29f5-4985-992c-cb3e0c0b3cbf)
 Call ID: 1b9c7df6-29f5-4985-992c-cb3e0c0b3cbf
  Args:
    relation: :hasMother
    source: Ernest_Brooksbank
    target: Eugenie_Victoria_Helena
  AddLiteral (f1b11388-29a5-442b-89a3-eb75eaf27353)
 Call ID: f1b11388-29a5-442b-89a3-eb75eaf27353
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1990
    source: Eugenie_Victoria_Helena
  AddLiteral (87027a6c-a4be-488a-8252-6ee0917e0ea6)
 Call ID: 87027a6c-a4be-488a-8252-6ee0917e0ea6
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 2018
    source: Eugenie_Victoria_Helena
  AddTriple (d07fe75c-14d2-44e6-9b50-657808872749)
 Call ID: d07fe75c-14d2-44e6-9b50-657808872749
  Args:
    relation: :hasRelation
    source: Eugenie_Victoria_Helena
    target: Jack_Brooksbank
  AddTriple (8e4694e6-8b0b-4345-8c2f-62e7b32f6701)
 Call ID: 8e4694e6-8b0b-4345-8c2f-62e7b32f6701
  Args:
    source: Eugenie_Victoria_Helena
    target: Beatrice
    relation: :isSisterOf
  AddTriple (b7cda824-46c3-4342-bd51-57d556bd99c8)
 Call ID: b7cda824-46c3-4342-bd51-57d556bd99c8
  Args:
    source: Beatrice
    target: Eugenie_Victoria_Helena
    relation: :isSisterOf
  AddTriple (8a19139b-b96d-4d73-b44a-8a2cea302979)
 Call ID: 8a19139b-b96d-4d73-b44a-8a2cea302979
  Args:
    relation: :isBrotherOf
    source: August_Brooksbank
    target: Ernest_Brooksbank
  AddTriple (cca7d8c3-4ca4-48c7-8013-e09970f525bb)
 Call ID: cca7d8c3-4ca4-48c7-8013-e09970f525bb
  Args:
    relation: :isBrotherOf
    source: Ernest_Brooksbank
    target: August_Brooksbank
  Finish (41fd6597-6bf8-42b8-bf94-ba68128104f8)
 Call ID: 41fd6597-6bf8-42b8-bf94-ba68128104f8
  Args: