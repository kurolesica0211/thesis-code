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
Beatrice was educated at St George's School, Ascot, before reading history at Goldsmiths, University of London, where she graduated with a BA degree.
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
Beatrice married Mapelli Mozzi in a private ceremony on 17 July 2020 at the Royal Chapel of All Saints, Royal Lodge, Windsor.
Her father's association with Jeffrey Epstein, an American financier and convicted sex offender, also affected the scale of the wedding; following Andrew's widely criticised  BBC interview and subsequent withdrawal from royal duties, the arrangements were significantly reduced.
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
  AssignClass (b4b10c54-adc0-435b-9295-f1b89d760a28)
 Call ID: b4b10c54-adc0-435b-9295-f1b89d760a28
  Args:
    type: :Woman
    source: :PrincessBeatrice
  AssignClass (42858b98-a4ba-4c7b-8f60-b450a7b5047c)
 Call ID: 42858b98-a4ba-4c7b-8f60-b450a7b5047c
  Args:
    source: :PrincessBeatrice
    type: :Person
  AddLiteral (f33e6777-088e-4879-b633-9e14a42e69c2)
 Call ID: f33e6777-088e-4879-b633-9e14a42e69c2
  Args:
    literal_type: xsd:integer
    literal_value: 1988
    source: :PrincessBeatrice
    relation: :hasBirthYear
  AssignClass (6cff7e3e-1857-4846-a2ad-488e7c4ea4f0)
 Call ID: 6cff7e3e-1857-4846-a2ad-488e7c4ea4f0
  Args:
    source: :AndrewMountbattenWindsor
    type: :Man
  AssignClass (b27a5378-220b-4fb7-baa7-cf7df70e3767)
 Call ID: b27a5378-220b-4fb7-baa7-cf7df70e3767
  Args:
    type: :Person
    source: :AndrewMountbattenWindsor
  AssignClass (0d87c8fc-4800-417f-8e16-6f51c1a3403e)
 Call ID: 0d87c8fc-4800-417f-8e16-6f51c1a3403e
  Args:
    source: :SarahFerguson
    type: :Woman
  AssignClass (f9cc7cce-c90a-49e8-a320-c59393ba77ba)
 Call ID: f9cc7cce-c90a-49e8-a320-c59393ba77ba
  Args:
    source: :SarahFerguson
    type: :Person
  AddTriple (169c33e9-2b9c-437b-b1ab-094170fb6c65)
 Call ID: 169c33e9-2b9c-437b-b1ab-094170fb6c65
  Args:
    target: :PrincessBeatrice
    relation: :isFatherOf
    source: :AndrewMountbattenWindsor
  AddTriple (72227820-8b69-420d-bd62-1994af22016b)
 Call ID: 72227820-8b69-420d-bd62-1994af22016b
  Args:
    relation: :isMotherOf
    target: :PrincessBeatrice
    source: :SarahFerguson
  AssignClass (34f05a0c-d8a4-4f36-b4b5-d2c06ab7067e)
 Call ID: 34f05a0c-d8a4-4f36-b4b5-d2c06ab7067e
  Args:
    source: :KingCharlesIII
    type: :Man
  AssignClass (5f84e415-76e7-4967-a481-68c4cbba8fb7)
 Call ID: 5f84e415-76e7-4967-a481-68c4cbba8fb7
  Args:
    type: :Person
    source: :KingCharlesIII
  AssignClass (f199ef1b-0578-44df-9680-c7f64b6519ca)
 Call ID: f199ef1b-0578-44df-9680-c7f64b6519ca
  Args:
    type: :Man
    source: :EdoardoMapelliMozzi
  AssignClass (5ec68e9d-10fa-4439-b2af-cdb07013d80d)
 Call ID: 5ec68e9d-10fa-4439-b2af-cdb07013d80d
  Args:
    type: :Person
    source: :EdoardoMapelliMozzi
  AddTriple (e81e3b19-3e8b-4cec-a540-32b6e7d66a02)
 Call ID: e81e3b19-3e8b-4cec-a540-32b6e7d66a02
  Args:
    source: :PrincessBeatrice
    target: :EdoardoMapelliMozzi
    relation: :hasMarriageYear
  AddLiteral (32568aff-15a9-443a-87b0-2b6909398ca3)
 Call ID: 32568aff-15a9-443a-87b0-2b6909398ca3
  Args:
    literal_value: 2020
    source: :PrincessBeatrice
    relation: :hasMarriageYear
    literal_type: xsd:integer
  AssignClass (ba67cbe1-8518-4aaf-a925-addfb7e61120)
 Call ID: ba67cbe1-8518-4aaf-a925-addfb7e61120
  Args:
    source: :QueenElizabethII
    type: :Woman
  AssignClass (f21d3f79-0f51-4a49-8855-43f327cc01fb)
 Call ID: f21d3f79-0f51-4a49-8855-43f327cc01fb
  Args:
    source: :QueenElizabethII
    type: :Person
  AssignClass (37d86fca-fed2-4925-a6ca-52adf8f1c9f3)
 Call ID: 37d86fca-fed2-4925-a6ca-52adf8f1c9f3
  Args:
    source: :PrincePhilip
    type: :Man
  AssignClass (8df7e03b-0987-4cce-846f-e2ae82102525)
 Call ID: 8df7e03b-0987-4cce-846f-e2ae82102525
  Args:
    type: :Person
    source: :PrincePhilip
  AssignClass (0850f29c-b803-4322-be9d-d5c0b4e6cc8e)
 Call ID: 0850f29c-b803-4322-be9d-d5c0b4e6cc8e
  Args:
    type: :Woman
    source: :PrincessEugenie
  AssignClass (02abf957-bdc6-4f6e-b0f0-51f1845a29e2)
 Call ID: 02abf957-bdc6-4f6e-b0f0-51f1845a29e2
  Args:
    type: :Person
    source: :PrincessEugenie
  AddTriple (1fcb187e-8b65-4fc1-8536-f96ec8139784)
 Call ID: 1fcb187e-8b65-4fc1-8536-f96ec8139784
  Args:
    relation: :isSisterOf
    target: :PrincessBeatrice
    source: :PrincessEugenie
  AssignClass (f2e01247-2595-41d7-b0a7-aaf2d09b1ffe)
 Call ID: f2e01247-2595-41d7-b0a7-aaf2d09b1ffe
  Args:
    source: :AlexMapelliMozzi
    type: :Man
  AssignClass (ac0f081a-596c-42ff-8f3a-8dcd87be364c)
 Call ID: ac0f081a-596c-42ff-8f3a-8dcd87be364c
  Args:
    source: :AlexMapelliMozzi
    type: :Person
  AddTriple (08ecebde-b893-46ed-8146-79d1527c6fa4)
 Call ID: 08ecebde-b893-46ed-8146-79d1527c6fa4
  Args:
    relation: :isFatherOf
    target: :EdoardoMapelliMozzi
    source: :AlexMapelliMozzi
  AssignClass (3bccd19a-d5ae-48bd-8bf9-a5d77b473fb7)
 Call ID: 3bccd19a-d5ae-48bd-8bf9-a5d77b473fb7
  Args:
    type: :Woman
    source: :SiennaElizabethMapelliMozzi
  AssignClass (66e9d4b4-559b-4613-b907-ee6c710d897c)
 Call ID: 66e9d4b4-559b-4613-b907-ee6c710d897c
  Args:
    source: :SiennaElizabethMapelliMozzi
    type: :Person
  AddTriple (66c42763-cb23-404a-8d06-04ef12235655)
 Call ID: 66c42763-cb23-404a-8d06-04ef12235655
  Args:
    target: :SiennaElizabethMapelliMozzi
    relation: :isMotherOf
    source: :PrincessBeatrice
  AddTriple (0faff6bd-3d44-4b57-b77d-74ee53793949)
 Call ID: 0faff6bd-3d44-4b57-b77d-74ee53793949
  Args:
    relation: :isFatherOf
    target: :SiennaElizabethMapelliMozzi
    source: :EdoardoMapelliMozzi
  AssignClass (8a2d4465-9445-451b-bc2c-6498c194ca63)
 Call ID: 8a2d4465-9445-451b-bc2c-6498c194ca63
  Args:
    source: :AthenaElizabethRose
    type: :Woman
  AssignClass (142f935a-e2b2-43ed-95f0-cd7c4a532a37)
 Call ID: 142f935a-e2b2-43ed-95f0-cd7c4a532a37
  Args:
    type: :Person
    source: :AthenaElizabethRose
  AddTriple (a442d1a4-727d-4ebe-81cf-aa08fcb361a1)
 Call ID: a442d1a4-727d-4ebe-81cf-aa08fcb361a1
  Args:
    relation: :isMotherOf
    target: :AthenaElizabethRose
    source: :PrincessBeatrice
  AddTriple (4ae2d816-dd9f-4c7d-817a-4b2b84769f41)
 Call ID: 4ae2d816-dd9f-4c7d-817a-4b2b84769f41
  Args:
    relation: :isFatherOf
    target: :AthenaElizabethRose
    source: :EdoardoMapelliMozzi
  Finish (5067bba1-c091-46a7-819f-bf5630ccb4d8)
 Call ID: 5067bba1-c091-46a7-819f-bf5630ccb4d8
  Args: