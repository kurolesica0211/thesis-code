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
  AssignClass (a3b52a91-a331-4a59-a6a9-a5a46df6e2b5)
 Call ID: a3b52a91-a331-4a59-a6a9-a5a46df6e2b5
  Args:
    source: :PrincessBeatrice
    type: :Woman
  AssignClass (4a143cfe-da07-4b8c-bc1b-ab7fa9e20656)
 Call ID: 4a143cfe-da07-4b8c-bc1b-ab7fa9e20656
  Args:
    type: :Person
    source: :PrincessBeatrice
  AddLiteral (a84f8e04-28fb-4c59-a173-fa5eee698fb5)
 Call ID: a84f8e04-28fb-4c59-a173-fa5eee698fb5
  Args:
    relation: :hasBirthYear
    source: :PrincessBeatrice
    literal_value: 1988
    literal_type: xsd:integer
  AssignClass (b70c39ba-167a-43dc-964e-ddfd78e56dce)
 Call ID: b70c39ba-167a-43dc-964e-ddfd78e56dce
  Args:
    type: :Man
    source: :AndrewMountbattenWindsor
  AssignClass (2bfcd853-4c0d-45bf-85b1-bb5915022ec4)
 Call ID: 2bfcd853-4c0d-45bf-85b1-bb5915022ec4
  Args:
    type: :Person
    source: :AndrewMountbattenWindsor
  AssignClass (d9900bc5-ca66-463c-9087-317c44e60cce)
 Call ID: d9900bc5-ca66-463c-9087-317c44e60cce
  Args:
    type: :Woman
    source: :SarahFerguson
  AssignClass (d0c1bb1c-8531-4a57-8bf5-bde839674e24)
 Call ID: d0c1bb1c-8531-4a57-8bf5-bde839674e24
  Args:
    source: :SarahFerguson
    type: :Person
  AddTriple (0cfe1eec-1dbe-4e37-8d8b-1595b2cbb441)
 Call ID: 0cfe1eec-1dbe-4e37-8d8b-1595b2cbb441
  Args:
    target: :AndrewMountbattenWindsor
    relation: :hasFather
    source: :PrincessBeatrice
  AddTriple (f747d8d9-ed1a-4f29-bfdb-5f7d39f7994e)
 Call ID: f747d8d9-ed1a-4f29-bfdb-5f7d39f7994e
  Args:
    relation: :hasMother
    target: :SarahFerguson
    source: :PrincessBeatrice
  AssignClass (27a904e1-3403-4c0e-af24-4d55eb2c7144)
 Call ID: 27a904e1-3403-4c0e-af24-4d55eb2c7144
  Args:
    source: :KingCharlesIII
    type: :Man
  AssignClass (d77a4521-a25e-4326-b6b3-f752e5e7cea0)
 Call ID: d77a4521-a25e-4326-b6b3-f752e5e7cea0
  Args:
    source: :KingCharlesIII
    type: :Person
  AssignClass (132214ff-b218-4c43-98d3-cd15fc024ac1)
 Call ID: 132214ff-b218-4c43-98d3-cd15fc024ac1
  Args:
    type: :Woman
    source: :PrincessEugenie
  AssignClass (2776f6c4-3c07-439b-9b3c-cd322460b973)
 Call ID: 2776f6c4-3c07-439b-9b3c-cd322460b973
  Args:
    source: :PrincessEugenie
    type: :Person
  AddTriple (834dbd8f-a8e4-4a7f-a781-0745b23d3da8)
 Call ID: 834dbd8f-a8e4-4a7f-a781-0745b23d3da8
  Args:
    source: :PrincessBeatrice
    relation: :hasSister
    target: :PrincessEugenie
  AssignClass (8c223f12-1469-48c0-ace5-665a312e9391)
 Call ID: 8c223f12-1469-48c0-ace5-665a312e9391
  Args:
    source: :EdoardoMapelliMozzi
    type: :Man
  AssignClass (09ce95f6-b53f-48b5-bb1c-aecebf94213e)
 Call ID: 09ce95f6-b53f-48b5-bb1c-aecebf94213e
  Args:
    source: :EdoardoMapelliMozzi
    type: :Person
  AddLiteral (fb7ba7ec-b98c-4985-ba7f-6b7abd7ad0a3)
 Call ID: fb7ba7ec-b98c-4985-ba7f-6b7abd7ad0a3
  Args:
    relation: :hasMarriageYear
    literal_type: xsd:integer
    literal_value: 2020
    source: :PrincessBeatrice
  AddTriple (d9e991f5-20df-43c4-9742-eef0ddafe6ec)
 Call ID: d9e991f5-20df-43c4-9742-eef0ddafe6ec
  Args:
    source: :PrincessBeatrice
    target: :EdoardoMapelliMozzi
    relation: :hasRelation
  AssignClass (36c679dd-5f6c-4b1b-a89a-3537bee9bcd3)
 Call ID: 36c679dd-5f6c-4b1b-a89a-3537bee9bcd3
  Args:
    type: :Woman
    source: :QueenElizabethII
  AssignClass (9961cee6-8fb7-4c52-b564-7bc6ed224616)
 Call ID: 9961cee6-8fb7-4c52-b564-7bc6ed224616
  Args:
    type: :Person
    source: :QueenElizabethII
  AssignClass (cb197751-8a82-46ba-bfda-26ab881f9c93)
 Call ID: cb197751-8a82-46ba-bfda-26ab881f9c93
  Args:
    type: :Man
    source: :PrincePhilip
  AssignClass (a4695b20-4163-433e-a316-4f52b421032d)
 Call ID: a4695b20-4163-433e-a316-4f52b421032d
  Args:
    source: :PrincePhilip
    type: :Person
  AssignClass (26fc14c3-caaf-463d-9852-033f45eb35d2)
 Call ID: 26fc14c3-caaf-463d-9852-033f45eb35d2
  Args:
    type: :Woman
    source: :SiennaElizabethMapelliMozzi
  AssignClass (07de2dec-5d28-4885-a393-54de39589078)
 Call ID: 07de2dec-5d28-4885-a393-54de39589078
  Args:
    type: :Person
    source: :SiennaElizabethMapelliMozzi
  AddTriple (11cb0bea-2823-4d57-8f0b-db3f8e72c8e8)
 Call ID: 11cb0bea-2823-4d57-8f0b-db3f8e72c8e8
  Args:
    relation: :hasMother
    target: :PrincessBeatrice
    source: :SiennaElizabethMapelliMozzi
  AddTriple (fe2a8784-fae2-4236-8076-43e4f3ee9d9c)
 Call ID: fe2a8784-fae2-4236-8076-43e4f3ee9d9c
  Args:
    relation: :hasFather
    target: :EdoardoMapelliMozzi
    source: :SiennaElizabethMapelliMozzi
  AssignClass (801debaf-0fa6-4e16-8490-0638ff3c707d)
 Call ID: 801debaf-0fa6-4e16-8490-0638ff3c707d
  Args:
    source: :AthenaElizabethRose
    type: :Woman
  AssignClass (6bc60c02-742c-40cf-9600-07ca60023d83)
 Call ID: 6bc60c02-742c-40cf-9600-07ca60023d83
  Args:
    source: :AthenaElizabethRose
    type: :Person
  AddTriple (88856b2a-41cb-4e86-91f4-026a66895067)
 Call ID: 88856b2a-41cb-4e86-91f4-026a66895067
  Args:
    source: :AthenaElizabethRose
    relation: :hasMother
    target: :PrincessBeatrice
  AddTriple (a37c36d9-1eb6-4ed7-ae00-225609b336fa)
 Call ID: a37c36d9-1eb6-4ed7-ae00-225609b336fa
  Args:
    source: :AthenaElizabethRose
    target: :EdoardoMapelliMozzi
    relation: :hasFather
  AssignClass (dadc831b-dbee-45f3-bda5-85d66c89d630)
 Call ID: dadc831b-dbee-45f3-bda5-85d66c89d630
  Args:
    type: :Man
    source: :AlexMapelliMozzi
  AssignClass (27ea8b96-cd2b-4228-9906-dc7477fe5651)
 Call ID: 27ea8b96-cd2b-4228-9906-dc7477fe5651
  Args:
    source: :AlexMapelliMozzi
    type: :Person
  AddTriple (7add5152-34a9-4c05-9312-3f181f06b57c)
 Call ID: 7add5152-34a9-4c05-9312-3f181f06b57c
  Args:
    target: :AlexMapelliMozzi
    relation: :hasFather
    source: :EdoardoMapelliMozzi
  AssignClass (fa69a2ed-a606-41af-9c32-cf0e69f8d4e5)
 Call ID: fa69a2ed-a606-41af-9c32-cf0e69f8d4e5
  Args:
    type: :Man
    source: :PaoloMapelliMozzi
  AssignClass (92a72f0c-2b15-4438-8aed-cdf93ae4d374)
 Call ID: 92a72f0c-2b15-4438-8aed-cdf93ae4d374
  Args:
    type: :Person
    source: :PaoloMapelliMozzi
  AssignClass (f9cd815f-9782-4f7b-8ee3-2c531fc8736c)
 Call ID: f9cd815f-9782-4f7b-8ee3-2c531fc8736c
  Args:
    source: :ChristopherWoolf
    type: :Man
  AssignClass (d437e46e-e58f-4ea5-9a90-c7110aef4586)
 Call ID: d437e46e-e58f-4ea5-9a90-c7110aef4586
  Args:
    type: :Person
    source: :ChristopherWoolf
  AssignClass (47a4c995-924b-4e90-b7db-fea5908064cb)
 Call ID: 47a4c995-924b-4e90-b7db-fea5908064cb
  Args:
    type: :Woman
    source: :DaraHuang
  AssignClass (3705b485-cbad-4009-a258-7a0ed673d00f)
 Call ID: 3705b485-cbad-4009-a258-7a0ed673d00f
  Args:
    type: :Person
    source: :DaraHuang
  AddTriple (fefbdcf7-707f-4755-82db-d8091152bae5)
 Call ID: fefbdcf7-707f-4755-82db-d8091152bae5
  Args:
    source: :ChristopherWoolf
    target: :DaraHuang
    relation: :hasMother
  AddTriple (d0e2f6ae-7f35-41b0-9082-8ab4af91a05e)
 Call ID: d0e2f6ae-7f35-41b0-9082-8ab4af91a05e
  Args:
    target: :EdoardoMapelliMozzi
    relation: :hasFather
    source: :ChristopherWoolf
  Finish (648614dc-ba0a-4e42-b9aa-9bfbe1d2b147)
 Call ID: 648614dc-ba0a-4e42-b9aa-9bfbe1d2b147
  Args: