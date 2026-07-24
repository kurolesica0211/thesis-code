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
She is the elder daughter of Andrew Mountbatten-Windsor and Sarah Ferguson, and a niece of King Charles III.
Born fifth in the line of succession to the British throne, she is ninth as of 2026.
Beatrice was educated at St George's School, Ascot, before reading history at Goldsmiths, University of London, where she graduated with a BA degree.
She has held roles at the Foreign Office and Sony Pictures, and currently serves as Vice-President of Strategic Partnerships at the software company Afiniti.
In 2020, Beatrice married Edoardo Mapelli Mozzi, an English-born property developer with descent from Italian nobility.
Early life and education

Beatrice was born at 8:18 pm on 8 August 1988 at the Portland Hospital in London, to the then Duke and Duchess of York.
She is the fifth grandchild of Queen Elizabeth II and Prince Philip, Duke of Edinburgh.
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
Their wedding was initially scheduled for 29 May 2020 at the Chapel Royal at St James's Palace, followed by a private reception in Buckingham Palace Gardens, but first the reception and then the wedding itself were postponed because of the COVID-19 pandemic.
Beatrice married Mapelli Mozzi in a private ceremony on 17 July 2020 at the Royal Chapel of All Saints, Royal Lodge, Windsor.
Her father's association with Jeffrey Epstein, an American financier and convicted sex offender, also affected the scale of the wedding; following Andrew's widely criticised  BBC interview and subsequent withdrawal from royal duties, the arrangements were significantly reduced.
Although Andrew walked Beatrice down the aisle, he did not appear in the official wedding portraits released by Buckingham Palace.
Beatrice wore a remodelled Sir Norman Hartnell gown lent by the Queen, and the Queen Mary Fringe Tiara, which the Queen had worn at her own wedding.
Beatrice has a stepson, Christopher Woolf ("Wolfie"), from her husband's previous relationship with the architect Dara Huang.
She gave birth to a daughter, Sienna Elizabeth Mapelli Mozzi, on 18 September 2021 at the Chelsea and Westminster Hospital in London.
At birth, Sienna was 11th in line to the British throne, and following the death of Queen Elizabeth II on 8 September 2022, she is now 10th.
She was christened at the Chapel Royal at St James's Palace on 29 April 2022.
Beatrice and her husband initially lived in a four-bedroom apartment at St James's Palace, but reportedly moved to a manor house in the Cotswolds in late 2022.
Beatrice gave birth to their second daughter, Athena Elizabeth Rose, on 22 January 2025 at the Chelsea and Westminster Hospital in London, several weeks prematurely.
She was christened at the Chapel Royal at St James's Palace on 12 December.
Athena is 11th in line to the British throne.
Charity work

In 2002, Beatrice visited children living with HIV in Russia.
In an interview to mark her 18th birthday, Beatrice said she wished to use her position to assist others through charity work; she had already undertaken charitable duties alongside her mother through the various organisations supported by the Duchess.
In April 2010, Beatrice became the first member of the British royal family to complete the London Marathon, running to raise money for Children in Crisis.
She is the patron of Forget-Me-Not Children's Hospice, which supports children with life-shortening conditions in West Yorkshire and North Manchester.
At the April 2011 wedding of her cousin Prince William, Beatrice's unusual fascinator, designed by Philip Treacy, attracted significant public and media attention.
In November 2012, Beatrice became a patron of the York Musical Society.
In 2016, she, her mother, and her sister Eugenie collaborated with the British contemporary artist Teddy McDonald to create the first royal contemporary art painting.
In 2018, Children in Crisis merged with Street Child, a children's charity active in multiple countries, with Beatrice serving as its ambassador.
Beatrice took part in a South Asia Tour in 2016 that lasted nine days.
A few weeks later, she attended the 2016 Asia Game Changer Awards Dinner at the United Nations in New York City, which honoured Ruit and others.
She and Charles Rockefeller presented Ruit with his Asia Society Asia Game Changer Award.
Beatrice is the founder of Big Change, a charity she established with six friends to encourage young people to develop skills "outside a traditional academic curriculum".
Be Nice and gave an interview to Vogue at a House of Lords event, speaking about her own experiences of being bullied for her fashion choices in early adulthood.
In May 2018, she attended the Met Gala in New York City.
In March 2019, Beatrice was elected to the board of the UK charity the Outward Bound Trust as a trustee, after her father succeeded to the royal patronage from his father, the Duke of Edinburgh.
In May 2019, she was honoured at a New York City gala for her work with Friends Without a Border.
In April 2022, in her capacity as an ambassador for the charity Made By Dyslexia, she and her husband took part in the first World Dyslexia Assembly, hosted by Prince Carl Philip of Sweden.
In February 2023, Beatrice was named patron of the British Skin Foundation.
In July 2025, she was appointed patron of the Chartered College of Teaching, a role previously held by her grandfather Prince Philip.
In November 2025, Beatrice was appointed deputy patron of Outward Bound Trust.
Titles, styles, and arms

Titles and styles

As a male-line grandchild of the British sovereign, Beatrice was known at birth as "Her Royal Highness Princess Beatrice of York", the territorial designation deriving from her father's former title, Duke of York.
Since her marriage, she has been styled in the Court Circular as "Her Royal Highness Princess Beatrice, Mrs Edoardo Mapelli Mozzi".



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
  AssignClass (bf49b072-dd58-417c-a32a-d8157e1625e5)
 Call ID: bf49b072-dd58-417c-a32a-d8157e1625e5
  Args:
    source: Princess_Beatrice
    type: :Woman
  AssignClass (3a65b463-5e30-416c-b0b1-1ff0743910bc)
 Call ID: 3a65b463-5e30-416c-b0b1-1ff0743910bc
  Args:
    source: Princess_Beatrice
    type: :Person
  AddLiteral (e371c8cd-e04e-4fa5-b71e-dc1a1726035b)
 Call ID: e371c8cd-e04e-4fa5-b71e-dc1a1726035b
  Args:
    literal_value: Beatrice Elizabeth Mary
    relation: :knownAs
    source: Princess_Beatrice
    literal_type: xsd:string
  AddLiteral (19e3b310-7764-49ad-8d14-17a7823de27d)
 Call ID: 19e3b310-7764-49ad-8d14-17a7823de27d
  Args:
    source: Princess_Beatrice
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1988
  AssignClass (cd1c1392-8ad5-485d-b512-7584094681c5)
 Call ID: cd1c1392-8ad5-485d-b512-7584094681c5
  Args:
    type: :Man
    source: Andrew_Mountbatten-Windsor
  AssignClass (4945db0f-d4ad-49a3-9d07-3744c9e16d8b)
 Call ID: 4945db0f-d4ad-49a3-9d07-3744c9e16d8b
  Args:
    type: :Person
    source: Andrew_Mountbatten-Windsor
  AssignClass (35290af1-9cc3-4ac6-aed0-4e101ed54727)
 Call ID: 35290af1-9cc3-4ac6-aed0-4e101ed54727
  Args:
    type: :Woman
    source: Sarah_Ferguson
  AssignClass (5191d4e8-f791-4e09-99a7-b7423d956a17)
 Call ID: 5191d4e8-f791-4e09-99a7-b7423d956a17
  Args:
    type: :Person
    source: Sarah_Ferguson
  AddTriple (0a779616-a90c-4d39-99e8-97ac021e3109)
 Call ID: 0a779616-a90c-4d39-99e8-97ac021e3109
  Args:
    source: Princess_Beatrice
    relation: :hasFather
    target: Andrew_Mountbatten-Windsor
  AddTriple (5fea2924-d489-4538-b173-0391912f01b1)
 Call ID: 5fea2924-d489-4538-b173-0391912f01b1
  Args:
    target: Sarah_Ferguson
    relation: :hasMother
    source: Princess_Beatrice
  AssignClass (97360b72-469d-44af-8982-55cac5000b8c)
 Call ID: 97360b72-469d-44af-8982-55cac5000b8c
  Args:
    source: King_Charles_III
    type: :Man
  AssignClass (1b3b74fa-fff0-4676-88b3-210dfdf665b2)
 Call ID: 1b3b74fa-fff0-4676-88b3-210dfdf665b2
  Args:
    type: :Person
    source: King_Charles_III
  AssignClass (988150da-40ff-420b-a87a-c0ea3398fa3f)
 Call ID: 988150da-40ff-420b-a87a-c0ea3398fa3f
  Args:
    source: Princess_Eugenie
    type: :Woman
  AssignClass (032b940b-afcf-4bfa-b095-bfe04348571e)
 Call ID: 032b940b-afcf-4bfa-b095-bfe04348571e
  Args:
    source: Princess_Eugenie
    type: :Person
  AddTriple (29ac8882-c76f-4097-b901-a34f0dccd410)
 Call ID: 29ac8882-c76f-4097-b901-a34f0dccd410
  Args:
    target: Princess_Eugenie
    relation: :isSisterOf
    source: Princess_Beatrice
  AddTriple (67dd2976-ce40-4af7-8d0e-49148d34591b)
 Call ID: 67dd2976-ce40-4af7-8d0e-49148d34591b
  Args:
    source: Princess_Eugenie
    relation: :hasFather
    target: Andrew_Mountbatten-Windsor
  AddTriple (7bbb6326-402b-46ab-915e-13900d770a79)
 Call ID: 7bbb6326-402b-46ab-915e-13900d770a79
  Args:
    source: Princess_Eugenie
    relation: :hasMother
    target: Sarah_Ferguson
  AssignClass (77eb29ea-a20a-4f68-a5f2-977b2f3c2a02)
 Call ID: 77eb29ea-a20a-4f68-a5f2-977b2f3c2a02
  Args:
    type: :Man
    source: Edoardo_Mapelli_Mozzi
  AssignClass (0f2c9354-5464-4d0b-a716-ba45cc8c5d36)
 Call ID: 0f2c9354-5464-4d0b-a716-ba45cc8c5d36
  Args:
    source: Edoardo_Mapelli_Mozzi
    type: :Person
  AddLiteral (4d966f32-de55-4edd-a1bb-a98b92e8dcf8)
 Call ID: 4d966f32-de55-4edd-a1bb-a98b92e8dcf8
  Args:
    literal_value: 2020
    relation: :hasMarriageYear
    source: Princess_Beatrice
    literal_type: xsd:integer
  AddTriple (1deb85db-3866-4d20-835a-f231235f5cdb)
 Call ID: 1deb85db-3866-4d20-835a-f231235f5cdb
  Args:
    relation: :hasRelation
    source: Princess_Beatrice
    target: Edoardo_Mapelli_Mozzi
  AssignClass (1c6af682-e287-4db5-a00a-84b2eff128c6)
 Call ID: 1c6af682-e287-4db5-a00a-84b2eff128c6
  Args:
    source: Sienna_Elizabeth_Mapelli_Mozzi
    type: :Woman
  AssignClass (e2f548ee-3e90-43f7-9601-8ce94c60c5a2)
 Call ID: e2f548ee-3e90-43f7-9601-8ce94c60c5a2
  Args:
    type: :Person
    source: Sienna_Elizabeth_Mapelli_Mozzi
  AddTriple (6138c3a1-c815-4a81-a061-3e9cd48d53da)
 Call ID: 6138c3a1-c815-4a81-a061-3e9cd48d53da
  Args:
    target: Princess_Beatrice
    source: Sienna_Elizabeth_Mapelli_Mozzi
    relation: :hasMother
  AddTriple (fccd2d59-202f-4fa5-9749-4539e19f7706)
 Call ID: fccd2d59-202f-4fa5-9749-4539e19f7706
  Args:
    target: Edoardo_Mapelli_Mozzi
    source: Sienna_Elizabeth_Mapelli_Mozzi
    relation: :hasFather
  AssignClass (81458873-e7bb-4f00-968b-92634bfc9dae)
 Call ID: 81458873-e7bb-4f00-968b-92634bfc9dae
  Args:
    source: Athena_Elizabeth_Rose
    type: :Woman
  AssignClass (3b13575b-70c8-4f1f-a595-9e603e4f3459)
 Call ID: 3b13575b-70c8-4f1f-a595-9e603e4f3459
  Args:
    type: :Person
    source: Athena_Elizabeth_Rose
  AddTriple (1c129e51-52da-47f7-a4e7-e13538aa85e5)
 Call ID: 1c129e51-52da-47f7-a4e7-e13538aa85e5
  Args:
    relation: :hasMother
    source: Athena_Elizabeth_Rose
    target: Princess_Beatrice
  AddTriple (d8e42eb4-3093-47b0-88ca-d5e4367c1493)
 Call ID: d8e42eb4-3093-47b0-88ca-d5e4367c1493
  Args:
    target: Edoardo_Mapelli_Mozzi
    source: Athena_Elizabeth_Rose
    relation: :hasFather
  AssignClass (81e564a3-c471-483f-ad34-3e2138cfbc6a)
 Call ID: 81e564a3-c471-483f-ad34-3e2138cfbc6a
  Args:
    source: Alex_Mapelli-Mozzi
    type: :Man
  AssignClass (f722ca87-9c0a-4181-9d7c-1c90faaa49fc)
 Call ID: f722ca87-9c0a-4181-9d7c-1c90faaa49fc
  Args:
    source: Alex_Mapelli-Mozzi
    type: :Person
  AddTriple (ac853676-e868-4b17-87db-fbd675e90656)
 Call ID: ac853676-e868-4b17-87db-fbd675e90656
  Args:
    target: Alex_Mapelli-Mozzi
    relation: :hasFather
    source: Edoardo_Mapelli_Mozzi
  AssignClass (658f887a-b4e7-4bad-b786-d59e016b4ea2)
 Call ID: 658f887a-b4e7-4bad-b786-d59e016b4ea2
  Args:
    source: Paolo_Mapelli_Mozzi
    type: :Man
  AssignClass (f9a02f13-8903-46cb-a1fa-25638d6c886a)
 Call ID: f9a02f13-8903-46cb-a1fa-25638d6c886a
  Args:
    type: :Person
    source: Paolo_Mapelli_Mozzi
  Finish (76d29d74-f1d0-4bf1-b59c-a6f914e9fd90)
 Call ID: 76d29d74-f1d0-4bf1-b59c-a6f914e9fd90
  Args: