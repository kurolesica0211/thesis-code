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
Prince Friso of Orange-Nassau (Dutch: Johan Friso Bernhard Christiaan David van Oranje-Nassau van Amsberg; 25 September 1968 – 12 August 2013) was the second son of Queen Beatrix of the Netherlands and Claus von Amsberg, and younger brother of King Willem-Alexander.
On 17 February 2012, Prince Friso was buried under an avalanche in Lech, Austria, while skiing off piste.
On 12 August 2013, one and a half years after the accident, Prince Friso died from complications.
Early life and education

Johan Friso Bernhard Christiaan David was born on 25 September 1968 at the Academic Hospital Utrecht (now the University Medical Center Utrecht) in Utrecht, Netherlands.
He was the second son of Princess Beatrix and Prince Claus, and grandson of Queen Juliana of the Netherlands and Prince Bernhard.
He had one older brother, current King Willem-Alexander of the Netherlands (b. 1967), and one younger brother, Prince Constantijn (b. 1969).
His titles at birth were Prince of the Netherlands, Prince of Orange-Nassau, and Jonkheer van Amsberg.
Prince Friso was baptized on 28 December 1968 in the Dom Church in Utrecht.
His godparents were Prince Harald of Norway, Johan Christian Baron von Jenisch, Herman van Roijen, Queen Juliana of the Netherlands and Christina von Amsberg.
Work

Prince Friso worked from 1995 to 1996 at the Amsterdam branch of the international management consultancy McKinsey.
After completing an MBA-programme at INSEAD, Prince Friso worked from 1998 to 2003 as a vice president at Goldman Sachs International in London.
From October 2006, Prince Friso was managing director in the London office of a private investment and advisory firm, Wolfensohn & Company.
Prince Friso was a co-founder of the MRI Centre in Amsterdam and was also a founding shareholder of Wizzair, the largest low-cost airline in Eastern Europe.
He was honorary chairman of the Prince Claus Fund for Culture and Development (a position he held together with his younger brother, Prince Constantijn).
Prior to his accident, Prince Friso was working as a chief financial officer for URENCO, a uranium enrichment company.
Marriage and children

On 30 June 2003, it was announced that Prince Friso was to marry Mabel Wisse Smit.
The Dutch cabinet, however, did not seek permission from parliament for this marriage, a constitutional requirement if Prince Friso was to remain a member of the Dutch Royal House and in line of succession for the throne; at the time, he was second in line after his older brother, Willem-Alexander.
The Prime Minister Jan Peter Balkenende explained that this was due to discussions with Mabel Wisse Smit in October 2003, when she had admitted that her previous statements about an alleged relationship with Klaas Bruinsma (1953–1991), a known Dutch drug baron, had not been complete and accurate.
They nevertheless married at Oude Kerk (Delft) on 24 April 2004, and Mabel Wisse Smit became a member of the Dutch Royal Family but not a member of the Dutch Royal House.
Considering that his elder brother King Willem-Alexander has three daughters, Prince Friso's exclusion from the succession was unlikely to have an effect on the monarchy in the Netherlands.
After their marriage, Prince Friso and his wife Princess Mabel set up home in London, in the suburb of Kew.
The couple's first daughter, Countess Emma Luana Ninette Sophie of Orange-Nassau, Jonkvrouwe van Amsberg, was born on 26 March 2005 in London.
Their second daughter, Countess Joanna Zaria Nicoline Milou of Orange-Nassau, Jonkvrouwe van Amsberg, was born on 18 June 2006, also in London.
Avalanche accident

Accident

On 17 February 2012, Prince Friso was buried under an avalanche in Lech, Austria, and he was taken to a hospital in Innsbruck.
According to a formal statement of the Netherlands Government Information Service (RVD), a prognosis could be given only after some days.
The prince's condition was described as "stable, but critical".
Resulting complications

The Dutch Royal Family issued a statement on 19 February saying "The Royal Family is very grateful and deeply touched by all expressions of support and sympathy after the ski accident of His Royal Highness Prince Friso.
On 24 February, an Innsbruck medical team announced that the prince had been buried for 25 minutes, followed by a 50-minute CPR to treat his cardiac arrest.
It remained unclear whether the prince would ever regain full consciousness.
Koller said that the Prince's family might now look for a rehabilitation institution.
On the same day the Dutch Royal Family issued a statement requesting that the privacy of the Prince's family be respected to enable them to come to terms with his condition.
On 1 March 2012, Prince Friso was transferred to the Wellington Hospital, in London where he and his wife had lived for many years.
On 19 November 2012, it was announced that the prince had started to show some signs of consciousness but it was still not certain whether he would ever wake up, and if he did, in what state.
On 9 July 2013, Prince Friso was moved back to Huis ten Bosch in the Netherlands.
Death and funeral

On 12 August 2013, it was announced that Prince Friso had died in Huis ten Bosch of complications from the accident.
He was buried on 16 August in the Dutch Reformed Cemetery in the hamlet of Lage Vuursche near Drakesteijn Castle, where he had spent his childhood and where Princess Beatrix returned to live in February 2014.
Titles, styles and honours

Titles and styles

Under the Act on the Membership of the Royal House (2002), Prince Friso lost the title 'Prince of the Netherlands' by entering into a marriage without an Act of Consent.
By a royal decree of 19 March 2004, Prince Friso was granted the surname 'Van Oranje-Nassau van Amsberg', the hereditary noble predicate 'Jonkheer (Jonkvrouw) van Amsberg and the hereditary title 'Count of Orange-Nassau', to take effect upon his marriage.
By the same decree, he was allowed to retain his title 'Prince of Orange-Nassau' as a personal and non-hereditary title and the style of 'Royal Highness'.
According to the notification of this Royal Decree, any children born to the couple were to receive the surname 'van Oranje-Nassau van Amsberg' and become a 'Count (Countess) of Orange-Nassau' and also have the noble predicate 'Jonkheer (Jonkvrouw) van Amsberg'.
So his children had the same titles and names as those of Prince Constantijn, and showing that they belong to the royal family descending from Queen Beatrix and Prince Claus.
Referred to from birth as Prince Johan-Friso, in 2004, the royal court announced that he had requested that he would henceforth be called "Prince Friso".
Honours

National

Ancestry

References

External links

2 gave up the title "Prince of the Netherlands, but still held the title "Prince of Orange-Nassau"
3 title granted by Royal Decree to descendants of Princess Irene



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
  AssignClass (201ce79f-dcdd-4c0b-bb04-604b2c611552)
 Call ID: 201ce79f-dcdd-4c0b-bb04-604b2c611552
  Args:
    type: :Man
    source: Prince_Friso
  AssignClass (67017ef8-4753-4fa9-86c6-17096bdbaff3)
 Call ID: 67017ef8-4753-4fa9-86c6-17096bdbaff3
  Args:
    source: Prince_Friso
    type: :Person
  AssignClass (f829d174-3e86-4b91-9fdf-901d755b79ba)
 Call ID: f829d174-3e86-4b91-9fdf-901d755b79ba
  Args:
    type: :Woman
    source: Queen_Beatrix
  AssignClass (b102d2f5-29f7-4aa8-838d-8669fdf15bd8)
 Call ID: b102d2f5-29f7-4aa8-838d-8669fdf15bd8
  Args:
    source: Queen_Beatrix
    type: :Person
  AssignClass (3b0c74a2-f2dc-4d0b-8369-5ac6aa37897a)
 Call ID: 3b0c74a2-f2dc-4d0b-8369-5ac6aa37897a
  Args:
    type: :Man
    source: Claus_von_Amsberg
  AssignClass (e6ae7ba2-7a75-482f-86b1-224d067f7645)
 Call ID: e6ae7ba2-7a75-482f-86b1-224d067f7645
  Args:
    source: Claus_von_Amsberg
    type: :Person
  AssignClass (603420a1-4e48-422c-bdec-d97fdfe27b23)
 Call ID: 603420a1-4e48-422c-bdec-d97fdfe27b23
  Args:
    type: :Man
    source: Willem-Alexander
  AssignClass (d3bf069c-d31c-4f20-8b6a-4d072b88d9f9)
 Call ID: d3bf069c-d31c-4f20-8b6a-4d072b88d9f9
  Args:
    type: :Person
    source: Willem-Alexander
  AssignClass (bf4304ac-faf3-4c65-ab19-c40450877c0c)
 Call ID: bf4304ac-faf3-4c65-ab19-c40450877c0c
  Args:
    source: Prince_Constantijn
    type: :Man
  AssignClass (11d65f4e-2826-4054-b916-7ad98d46eab4)
 Call ID: 11d65f4e-2826-4054-b916-7ad98d46eab4
  Args:
    type: :Person
    source: Prince_Constantijn
  AssignClass (9f1a117a-5fd2-407e-bdbc-650bfdb68267)
 Call ID: 9f1a117a-5fd2-407e-bdbc-650bfdb68267
  Args:
    source: Queen_Juliana
    type: :Woman
  AssignClass (8c501d8e-f0e1-4709-bd9b-7c85f1554490)
 Call ID: 8c501d8e-f0e1-4709-bd9b-7c85f1554490
  Args:
    source: Queen_Juliana
    type: :Person
  AssignClass (9e77c5e3-5675-410b-aeb1-49b79a112c1f)
 Call ID: 9e77c5e3-5675-410b-aeb1-49b79a112c1f
  Args:
    type: :Man
    source: Prince_Bernhard
  AssignClass (67cdac5f-5487-4a66-acac-36bd151ce399)
 Call ID: 67cdac5f-5487-4a66-acac-36bd151ce399
  Args:
    source: Prince_Bernhard
    type: :Person
  AssignClass (990dd5e5-3592-4dcd-aa61-6f974be92ffb)
 Call ID: 990dd5e5-3592-4dcd-aa61-6f974be92ffb
  Args:
    type: :Woman
    source: Mabel_Wisse_Smit
  AssignClass (39dfd0d5-98e8-481b-9342-c6f9b9380b90)
 Call ID: 39dfd0d5-98e8-481b-9342-c6f9b9380b90
  Args:
    type: :Person
    source: Mabel_Wisse_Smit
  AssignClass (8828cb31-082e-4746-988f-a7d44385f2ec)
 Call ID: 8828cb31-082e-4746-988f-a7d44385f2ec
  Args:
    type: :Woman
    source: Countess_Emma_Luana_Ninette_Sophie
  AssignClass (82be9651-7aba-45b1-bba4-73bdaeb4267b)
 Call ID: 82be9651-7aba-45b1-bba4-73bdaeb4267b
  Args:
    type: :Person
    source: Countess_Emma_Luana_Ninette_Sophie
  AssignClass (85ae0c0e-9320-4811-adb2-ac007f2bebf4)
 Call ID: 85ae0c0e-9320-4811-adb2-ac007f2bebf4
  Args:
    source: Countess_Joanna_Zaria_Nicoline_Milou
    type: :Woman
  AssignClass (cb79416a-139e-409c-a911-d743d7372b51)
 Call ID: cb79416a-139e-409c-a911-d743d7372b51
  Args:
    type: :Person
    source: Countess_Joanna_Zaria_Nicoline_Milou
  AddLiteral (59dd4c7e-22bb-473a-bd10-cf27d979a47f)
 Call ID: 59dd4c7e-22bb-473a-bd10-cf27d979a47f
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1968
    source: Prince_Friso
  AddLiteral (aa7d751f-cfca-43e8-a138-73374bf1e9b5)
 Call ID: aa7d751f-cfca-43e8-a138-73374bf1e9b5
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: Prince_Friso
    literal_value: 2013
  AddTriple (1fbf0520-7a86-4a8f-a3f0-5ae0b4057983)
 Call ID: 1fbf0520-7a86-4a8f-a3f0-5ae0b4057983
  Args:
    relation: :hasMother
    source: Prince_Friso
    target: Queen_Beatrix
  AddTriple (0e480cbd-3818-447d-a84b-4c3f7184d494)
 Call ID: 0e480cbd-3818-447d-a84b-4c3f7184d494
  Args:
    target: Claus_von_Amsberg
    source: Prince_Friso
    relation: :hasFather
  AddTriple (7b63f12c-e11b-47b7-b7b8-11300b07744a)
 Call ID: 7b63f12c-e11b-47b7-b7b8-11300b07744a
  Args:
    target: Willem-Alexander
    source: Prince_Friso
    relation: :isBrotherOf
  AddTriple (e7e5704e-0d12-4d3d-8970-9b12fd54ef52)
 Call ID: e7e5704e-0d12-4d3d-8970-9b12fd54ef52
  Args:
    target: Prince_Constantijn
    source: Prince_Friso
    relation: :isBrotherOf
  AddTriple (e31e8553-2ad3-4ab5-b21d-14b0a2191fea)
 Call ID: e31e8553-2ad3-4ab5-b21d-14b0a2191fea
  Args:
    source: Willem-Alexander
    target: Queen_Beatrix
    relation: :hasMother
  AddTriple (1a0b1a2a-41d3-4401-8a9d-27f9106398c2)
 Call ID: 1a0b1a2a-41d3-4401-8a9d-27f9106398c2
  Args:
    relation: :hasFather
    target: Claus_von_Amsberg
    source: Willem-Alexander
  AddTriple (480eca03-621a-4834-8427-18a29ee36002)
 Call ID: 480eca03-621a-4834-8427-18a29ee36002
  Args:
    relation: :hasMother
    target: Queen_Beatrix
    source: Prince_Constantijn
  AddTriple (d0db424e-ed7e-481e-8be1-4a601af40410)
 Call ID: d0db424e-ed7e-481e-8be1-4a601af40410
  Args:
    source: Prince_Constantijn
    target: Claus_von_Amsberg
    relation: :hasFather
  AddTriple (f8b46d62-10ba-4cc9-8c84-9892e2dab862)
 Call ID: f8b46d62-10ba-4cc9-8c84-9892e2dab862
  Args:
    source: Queen_Juliana
    target: Queen_Beatrix
    relation: :isMotherOf
  AddTriple (e7510d71-ca4b-4c9b-bc72-6eed43ff4764)
 Call ID: e7510d71-ca4b-4c9b-bc72-6eed43ff4764
  Args:
    relation: :isFatherOf
    target: Queen_Beatrix
    source: Prince_Bernhard
  AddLiteral (5e4c3e75-babc-400e-acd6-d1c11f82f751)
 Call ID: 5e4c3e75-babc-400e-acd6-d1c11f82f751
  Args:
    relation: :hasMarriageYear
    literal_type: xsd:integer
    literal_value: 2004
    source: Prince_Friso
  AddTriple (19255920-ffa4-44dd-ad3b-73324b0db859)
 Call ID: 19255920-ffa4-44dd-ad3b-73324b0db859
  Args:
    source: Prince_Friso
    target: Countess_Emma_Luana_Ninette_Sophie
    relation: :hasChild
  AddTriple (d9d1e9d6-2624-4f11-848e-ed3c143352db)
 Call ID: d9d1e9d6-2624-4f11-848e-ed3c143352db
  Args:
    source: Prince_Friso
    target: Countess_Joanna_Zaria_Nicoline_Milou
    relation: :hasChild
  AddTriple (1632bca6-66fe-471b-b828-a8564f59cab5)
 Call ID: 1632bca6-66fe-471b-b828-a8564f59cab5
  Args:
    source: Countess_Emma_Luana_Ninette_Sophie
    target: Mabel_Wisse_Smit
    relation: :hasMother
  AddTriple (95bf3acd-6e93-4d68-9ace-3a8441914041)
 Call ID: 95bf3acd-6e93-4d68-9ace-3a8441914041
  Args:
    target: Mabel_Wisse_Smit
    source: Countess_Joanna_Zaria_Nicoline_Milou
    relation: :hasMother
  AddLiteral (4798c0af-9012-431a-b38c-dd9c1db5e911)
 Call ID: 4798c0af-9012-431a-b38c-dd9c1db5e911
  Args:
    source: Prince_Friso
    literal_value: Johan Friso Bernhard Christiaan David van Oranje-Nassau van Amsberg
    literal_type: xsd:string
    relation: :knownAs
  Finish (86e77b07-8836-4d87-90d1-06fbe324a710)
 Call ID: 86e77b07-8836-4d87-90d1-06fbe324a710
  Args: