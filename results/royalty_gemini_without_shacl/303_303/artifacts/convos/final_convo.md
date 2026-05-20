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
  AssignClass (e49c5595-cf73-4aa5-b0a3-a0b8770a3fa7)
 Call ID: e49c5595-cf73-4aa5-b0a3-a0b8770a3fa7
  Args:
    type: :Man
    source: :PrinceFriso
  AssignClass (801b7051-cda4-4a52-8c6a-dbb70459c08e)
 Call ID: 801b7051-cda4-4a52-8c6a-dbb70459c08e
  Args:
    type: :Person
    source: :PrinceFriso
  AddLiteral (958fa6bb-34a7-4f55-99e1-e77f6a1ad84e)
 Call ID: 958fa6bb-34a7-4f55-99e1-e77f6a1ad84e
  Args:
    literal_type: xsd:string
    source: :PrinceFriso
    literal_value: Johan Friso Bernhard Christiaan David van Oranje-Nassau van Amsberg
    relation: :knownAs
  AddLiteral (613d549f-e65f-419a-92fb-ba8032684297)
 Call ID: 613d549f-e65f-419a-92fb-ba8032684297
  Args:
    literal_value: 1968
    literal_type: xsd:integer
    source: :PrinceFriso
    relation: :hasBirthYear
  AddLiteral (7521f61d-6956-4571-9a4b-aa219891aa16)
 Call ID: 7521f61d-6956-4571-9a4b-aa219891aa16
  Args:
    relation: :hasDeathYear
    literal_value: 2013
    literal_type: xsd:integer
    source: :PrinceFriso
  AssignClass (939bbb64-7f77-4dc3-8a51-9979c039a388)
 Call ID: 939bbb64-7f77-4dc3-8a51-9979c039a388
  Args:
    type: :Woman
    source: :QueenBeatrix
  AssignClass (06801225-544c-4e46-9029-6e45c36da1e5)
 Call ID: 06801225-544c-4e46-9029-6e45c36da1e5
  Args:
    type: :Person
    source: :QueenBeatrix
  AssignClass (fc0697a8-6fbb-4da4-8ed4-6a8dc53dd678)
 Call ID: fc0697a8-6fbb-4da4-8ed4-6a8dc53dd678
  Args:
    type: :Man
    source: :ClausVonAmsberg
  AssignClass (f17a34c3-08bd-4222-b849-fc8917b1085e)
 Call ID: f17a34c3-08bd-4222-b849-fc8917b1085e
  Args:
    type: :Person
    source: :ClausVonAmsberg
  AddTriple (a02d0187-8cb9-419f-8b92-ce4625459ff8)
 Call ID: a02d0187-8cb9-419f-8b92-ce4625459ff8
  Args:
    relation: :hasFather
    target: :ClausVonAmsberg
    source: :PrinceFriso
  AddTriple (563f0293-041f-4ca2-a076-989c50d08365)
 Call ID: 563f0293-041f-4ca2-a076-989c50d08365
  Args:
    relation: :hasMother
    target: :QueenBeatrix
    source: :PrinceFriso
  AssignClass (db444ea8-172c-436c-85df-9b099ffea93c)
 Call ID: db444ea8-172c-436c-85df-9b099ffea93c
  Args:
    type: :Man
    source: :KingWillemAlexander
  AssignClass (5af2d319-77ff-4ae2-8e6b-e11b6d6037ab)
 Call ID: 5af2d319-77ff-4ae2-8e6b-e11b6d6037ab
  Args:
    type: :Person
    source: :KingWillemAlexander
  AddTriple (68229450-63be-4342-ba13-5e0ea4e8967e)
 Call ID: 68229450-63be-4342-ba13-5e0ea4e8967e
  Args:
    source: :PrinceFriso
    relation: :hasBrother
    target: :KingWillemAlexander
  AssignClass (601b210b-7514-48f1-b017-8be41011ea49)
 Call ID: 601b210b-7514-48f1-b017-8be41011ea49
  Args:
    type: :Man
    source: :PrinceConstantijn
  AssignClass (00c495ab-faac-4636-a1e4-b882ed7ccb74)
 Call ID: 00c495ab-faac-4636-a1e4-b882ed7ccb74
  Args:
    type: :Person
    source: :PrinceConstantijn
  AddTriple (d64d7d8b-595c-4205-a4d4-e182ab0b4383)
 Call ID: d64d7d8b-595c-4205-a4d4-e182ab0b4383
  Args:
    relation: :hasBrother
    target: :PrinceConstantijn
    source: :PrinceFriso
  AssignClass (7d1c3ef9-8267-4ee4-aa90-ecfcdd9e0a77)
 Call ID: 7d1c3ef9-8267-4ee4-aa90-ecfcdd9e0a77
  Args:
    type: :Woman
    source: :QueenJuliana
  AssignClass (04589ff2-45bf-4d41-b034-38517d02cc03)
 Call ID: 04589ff2-45bf-4d41-b034-38517d02cc03
  Args:
    type: :Person
    source: :QueenJuliana
  AssignClass (472b8add-08ce-462a-9d4c-cb46e703a975)
 Call ID: 472b8add-08ce-462a-9d4c-cb46e703a975
  Args:
    type: :Man
    source: :PrinceBernhard
  AssignClass (5666d119-a997-4631-8e00-57d44b12a35e)
 Call ID: 5666d119-a997-4631-8e00-57d44b12a35e
  Args:
    type: :Person
    source: :PrinceBernhard
  AssignClass (0c04e417-ffc5-422b-bbad-60a525062605)
 Call ID: 0c04e417-ffc5-422b-bbad-60a525062605
  Args:
    type: :Woman
    source: :MabelWisseSmit
  AssignClass (f7d44295-39d5-413e-bb99-e24fec3fa0f1)
 Call ID: f7d44295-39d5-413e-bb99-e24fec3fa0f1
  Args:
    type: :Person
    source: :MabelWisseSmit
  AddLiteral (0ba0f8c5-3962-477a-a26b-7a5bdc87fa91)
 Call ID: 0ba0f8c5-3962-477a-a26b-7a5bdc87fa91
  Args:
    literal_type: xsd:integer
    source: :PrinceFriso
    literal_value: 2004
    relation: :hasMarriageYear
  AssignClass (fa60d893-4763-47b5-9462-a35793007772)
 Call ID: fa60d893-4763-47b5-9462-a35793007772
  Args:
    type: :Woman
    source: :EmmaLuanaNinetteSophie
  AssignClass (0f2354ab-3a86-482b-a55a-04015a8259ce)
 Call ID: 0f2354ab-3a86-482b-a55a-04015a8259ce
  Args:
    type: :Person
    source: :EmmaLuanaNinetteSophie
  AddTriple (8c16670f-30f8-4992-bfe4-04b2e624197b)
 Call ID: 8c16670f-30f8-4992-bfe4-04b2e624197b
  Args:
    relation: :isDaughterOf
    target: :PrinceFriso
    source: :EmmaLuanaNinetteSophie
  AddTriple (d4299bcf-9248-4e33-b8b7-c23570ea9e5c)
 Call ID: d4299bcf-9248-4e33-b8b7-c23570ea9e5c
  Args:
    source: :EmmaLuanaNinetteSophie
    relation: :isDaughterOf
    target: :MabelWisseSmit
  AssignClass (0561b23c-ab35-4463-b7e8-6e42cfbd3b06)
 Call ID: 0561b23c-ab35-4463-b7e8-6e42cfbd3b06
  Args:
    type: :Woman
    source: :JoannaZariaNicolineMilou
  AssignClass (40b8bc94-6ff1-474e-a364-69086fbe3c0c)
 Call ID: 40b8bc94-6ff1-474e-a364-69086fbe3c0c
  Args:
    type: :Person
    source: :JoannaZariaNicolineMilou
  AddTriple (32413a30-569f-40cd-8bca-ab673a82b70c)
 Call ID: 32413a30-569f-40cd-8bca-ab673a82b70c
  Args:
    source: :JoannaZariaNicolineMilou
    relation: :isDaughterOf
    target: :PrinceFriso
  AddTriple (53e1f59a-31be-4a26-8a78-6cbad935fd1e)
 Call ID: 53e1f59a-31be-4a26-8a78-6cbad935fd1e
  Args:
    source: :JoannaZariaNicolineMilou
    relation: :isDaughterOf
    target: :MabelWisseSmit
  Finish (4a74c699-2bdc-48d6-b4fe-adb0045a9399)
 Call ID: 4a74c699-2bdc-48d6-b4fe-adb0045a9399
  Args: