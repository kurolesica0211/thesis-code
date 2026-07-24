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
Princess Beatrix*


Princess Margriet*Pieter van Vollenhoven*


Beatrix (Beatrix Wilhelmina Armgard, .mw-parser-output .IPA-label-small{font-size:85%}.mw-parser-output .references .IPA-label-small,.mw-parser-output .infobox .IPA-label-small,.mw-parser-output .navbox .IPA-label-small{font-size:100%}Dutch pronunciation:  i; born 31 January 1938) is a member of the Dutch royal house who reigned as Queen of the Netherlands from 30 April 1980 until her abdication in 2013.
Beatrix was born during the reign of her maternal grandmother, Queen Wilhelmina, and became heiress presumptive upon the accession of her mother, Queen Juliana, in 1948.
Beatrix attended a public primary school in Canada during World War II, and then finished her primary and secondary education in the Netherlands in the post-war period.
In 1966, Beatrix married Claus von Amsberg, a German diplomat, with whom she had three children.
When her mother abdicated on 30 April 1980, Beatrix succeeded her as queen.
Beatrix's reign saw the country's Caribbean territories reshaped with Aruba's secession and becoming its own constituent country within the kingdom in 1986.
This was followed by the dissolution of the Netherlands Antilles in 2010, which created the new special municipalities of Bonaire, Sint Eustatius, and Saba, and the two new constituent countries of Curaçao and Sint Maarten.
On Koninginnedag (Queensday), 30 April 2013, Beatrix abdicated in favour of her eldest son, Willem-Alexander.
At the time of her abdication at age 75, Beatrix was the oldest reigning monarch in the country's history.
Early life

Princess Beatrix Wilhelmina Armgard was born on 31 January 1938 at Soestdijk Palace in Baarn, Netherlands, as the first child of Princess Juliana of the Netherlands and her husband, Prince Bernhard of Lippe-Biesterfeld.
Beatrix was baptised on 12 May 1938 in the Great Church in The Hague.
Her five godparents were King Leopold III of Belgium; Princess Alice, Countess of Athlone; Beatrix's maternal great-great-aunt Elisabeth, Princess of Erbach-Schönberg; her paternal great-uncle Duke Adolf Friedrich of Mecklenburg; and Countess Allene de Kotzebue.
Beatrix's middle names are the first names of her grandmothers, Queen Wilhelmina of the Netherlands and Armgard, Princess of Lippe-Biesterfeld.
When Beatrix was one year old, in 1939, her younger sister Princess Irene was born.
World War II broke out in the Netherlands on 10 May 1940 (Westfeldzug).
One month later, Beatrix went to Ottawa, Ontario, Canada, with her mother Juliana and her sister Irene, while her father Bernhard and maternal grandmother Queen Wilhelmina remained in London.
While on Bigwin Island, the constitution of the Netherlands was stored in the safe of Bigwin Inn's rotunda building.
Princess Juliana and her family were remembered for their "down to earth" friendliness, general gratefulness and great reverence for their homeland and people, to whom they paid homage by refraining from all luxuries offered to guests at the resort that was once billed as the largest and most luxurious summer resort in Canada.
In the years following the shuttering and neglect of the island resort, the "Juliana" cottages were well maintained and preserved in an informal tribute to Princess Juliana and her family.
In appreciation for the protection of her and her daughters, Princess Juliana established the custom of delivery to the Canadian government every spring of tulips, which is the centrepiece of the Canadian Tulip Festival.
The second sister of Beatrix, Princess Margriet, was born in Ottawa in 1943.
During their exile in Canada, Beatrix attended nursery and Rockcliffe Park Public School, a primary school where she was known as "Trixie Orange".
On 5 May 1945, the German troops in the Netherlands surrendered.
The family returned to the Netherlands on 2 August 1945.
Beatrix went to the progressive primary school De Werkplaats in Bilthoven run by pacifist social reformers Kees Boeke and Beatrice Boeke-Cadbury.
On 6 September 1948, her mother succeeded her grandmother Wilhelmina as Queen of the Netherlands.
Since she had no brothers, Beatrix became the heiress presumptive to the Dutch throne at the age of ten.
Education

In April 1950, Princess Beatrix entered the Incrementum, a part of Baarnsch Lyceum, where, in 1956, she passed her school graduation examinations in the subjects of arts and classics.
In 1954, Beatrix served as a bridesmaid at the wedding of Baroness van Randwijck and Mr. T Boey.
On 31 January 1956, Beatrix celebrated her 18th birthday.
From that date, under the Constitution of the Netherlands, she was entitled to assume the Royal Prerogative.
In the course of her studies she also attended lectures on the cultures of Suriname and the Netherlands Antilles, the Charter for the Kingdom of the Netherlands, international affairs, international law, history and European law.
Political involvement

In 1965, Beatrix became engaged to the German aristocrat Claus von Amsberg, a diplomat working for the German Foreign Office.
Prince Claus had served in the Hitler Youth and the Wehrmacht and therefore was easily associated with German Nazism.
Protests included slogans like "Claus 'raus!"
(Claus out!) and "Mijn fiets terug" ("Return my bicycle" – a reference to German soldiers confiscating Dutch bicycles during WWII).
As time went on, Prince Claus became one of the most popular members of the Dutch monarchy.
On 25 November 1975, Beatrix and Prince Claus attended the independence ceremony of Suriname, held in the new nation's capital, Paramaribo, representing her mother the Queen.
As a monarch, Beatrix had weekly meetings with the prime minister.
Beatrix is a member of the Bilderberg Group.
Marriage and children

Engagement to Claus

On 28 June 1965, the engagement of Princess Beatrix to the German diplomat Claus von Amsberg was announced.
Claus and Beatrix had met at the wedding-eve party of Princess Tatjana of Sayn-Wittgenstein-Berleburg and Moritz, Landgrave of Hesse, in summer 1964.
After Parliament consented to the marriage, Claus von Amsberg became a Dutch citizen, and upon his marriage became Prince Claus of the Netherlands, Jonkheer van Amsberg.
Wedding, 1966

Beatrix married Claus von Amsberg on 10 March 1966 in civil and religious ceremonies.
The senior bridesmaids were the bride's youngest sister, Princess Christina of the Netherlands; Princess Christina of Sweden; Lady Elizabeth Anson; Joanna Roëll; Eugénie Loudon; and the bridegroom's sister, Christina von Amsberg.
The junior bridesmaids were Daphne Stewart-Clark and Carolijn Alting von Geusau, with page boys Joachim Jencquel and Markus von Oeynhausen-Sierstorpff.
They lived at Drakensteyn Castle in Lage Vuursche with their children until Beatrix ascended the throne.
Accession and inauguration

From the 1970s, Beatrix began to prepare more intensively for her future position as head of state.
She made many trips abroad with Prince Claus, including a controversial one to the Soviet Union.
After the Lockheed affair, Beatrix and Claus began to delve into the royal household and made plans to adapt it.
In addition, they asked advisers to prepare for Beatrix's reign.
On 31 January 1980, the birthday of her eldest daughter and heiress presumptive, Queen Juliana announced during a live television speech that she wished to abdicate on 30 April in favor of her daughter Beatrix.
That Beatrix would succeed her mother as queen was not a matter of course when she was born.
It was only after it was clear that Juliana was biologically unable to have any more children, let alone a son, that Beatrix was certain that she was the intended successor.
On 30 April 1980, Juliana abdicated, and Beatrix became the 13th member of the House of Orange to reign over the Netherlands.
Reign

Beatrix's constitutional duties included those typically accorded to a head of state; this includes having to sign every piece of legislation before it becomes law, formally appointing various officials, receiving and accrediting ambassadors, and awarding honours and medals, among others.
Beatrix was rarely quoted directly in the press during her reign, for the government information service (Rijksvoorlichtingsdienst) made it a condition of interviews that she should not be quoted.
It did not apply to her son Prince Willem-Alexander.
Throughout much of her reign, Beatrix had a considerable role in the cabinet formation process; notably she appointed the informateur and formateur, the person who leads the negotiations that ultimately lead to the formation of a government.
Beatrix was included in Andy Warhol's portrait series in 1985 as one of four Reigning Queens, alongside Elizabeth II, Margrethe II of Denmark and Ntfombi of Eswatini.
On 1 January 1986, Aruba seceded from the Netherlands Antilles and became a separate constituent country within the Dutch Kingdom.
Kissed by a bystander

During 1988 Queen's Day, Queen Beatrix was kissed by a bystander, later identified as Maarten Rijkers, when she walked through the crowd of people at a flea market in the Jordaan.
When Beatrix walked alongside Rijkers he said "Give me a kiss, girl", after which he gave her a hug and two kisses.
Later years

On 6 October 2002, the Queen's husband, Prince Claus, died after a long illness.
On 8 February 2005, Beatrix received a rare honorary doctorate from Leiden University, an honour the Queen does not usually accept.
Beatrix was to tie the prestigious medal to the standard of the incumbents of the 1st Independent Polish Parachute Brigade.
On 30 April 2009, Beatrix and other members of the royal family were targeted in a car attack by a man named Karst Tates.
Within hours, Beatrix made a rare televised address to express her shock and condolences.
Abdication

In a broadcast on national media on 28 January 2013, Beatrix announced her intention to abdicate on 30 April (Koninginnedag), when she would have been on the throne for exactly 33 years.
Beatrix stated that it was time to "place the responsibility for the country in the hands of a new generation."
Her heir apparent was her eldest son, Prince Willem-Alexander.
The broadcast was followed by a statement from Prime Minister Mark Rutte who paid tribute to Beatrix, saying "Since her investiture in 1980, she has applied herself heart and soul to Dutch society."
Post-abdication

Beatrix continues to undertake some royal duties and is a patron of many organisations.
Honorific eponyms

Beatrix has given her name to a number of facilities in the Netherlands and beyond.
These include:


A few parks in the country also bear her name:


It has been speculated that Beatrix is De Onbekende Beeldhouwer (Unknown Sculptor), whose work has been appearing in Amsterdam since 1983.
Titles, styles, honours and arms

Princess Beatrix has held titles throughout her life, as a granddaughter or daughter of a monarch, and eventually as the Sovereign.
Beatrix's official title was Her Majesty the Queen of the Netherlands, Princess of Orange-Nassau, etc., etc., etc.
She signed official documents with only "Beatrix".
Beatrix has received honours and awards from countries around the world, both during her life as a princess and as a monarch.
From birth till her inauguration as queen, she had the following name and titles, to which she reverted after her abdication: Her Royal Highness Princess Beatrix of the Netherlands, Princess of Orange-Nassau, Princess of Lippe-Biesterfeld.
Prime Ministers during her reign

Notes

References

Books

External links

2 also Princess of Lippe-Biesterfeld



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
  AssignClass (02fa0c60-e0c9-4031-8c82-ef51cfc069ba)
 Call ID: 02fa0c60-e0c9-4031-8c82-ef51cfc069ba
  Args:
    source: Beatrix
    type: :Woman
  AssignClass (957b3bcb-c448-47f8-91e1-aea923abe980)
 Call ID: 957b3bcb-c448-47f8-91e1-aea923abe980
  Args:
    source: Beatrix
    type: :Person
  AddLiteral (2ecadbfb-4d00-4ace-8784-cdb96f6bdb34)
 Call ID: 2ecadbfb-4d00-4ace-8784-cdb96f6bdb34
  Args:
    source: Beatrix
    relation: :hasBirthYear
    literal_type: xsd:positiveInteger
    literal_value: 1938
  AssignClass (12ab36ee-b00b-4bd8-bd15-2d4f9ba09b2b)
 Call ID: 12ab36ee-b00b-4bd8-bd15-2d4f9ba09b2b
  Args:
    source: Juliana
    type: :Woman
  AssignClass (1ece8eba-b260-44c8-9b85-042794014954)
 Call ID: 1ece8eba-b260-44c8-9b85-042794014954
  Args:
    source: Juliana
    type: :Person
  AssignClass (2f3b21de-88d6-4d33-9ab5-7e2417f1029c)
 Call ID: 2f3b21de-88d6-4d33-9ab5-7e2417f1029c
  Args:
    type: :Man
    source: Bernhard
  AssignClass (887bffa3-9f0b-48fc-9251-210b94395c02)
 Call ID: 887bffa3-9f0b-48fc-9251-210b94395c02
  Args:
    type: :Person
    source: Bernhard
  AddTriple (256daf42-17e5-42a9-bf55-4f6677d34fb6)
 Call ID: 256daf42-17e5-42a9-bf55-4f6677d34fb6
  Args:
    relation: :hasMother
    source: Beatrix
    target: Juliana
  AddTriple (dfeac946-dedf-4974-a2f6-552e12397fdb)
 Call ID: dfeac946-dedf-4974-a2f6-552e12397fdb
  Args:
    target: Bernhard
    relation: :hasFather
    source: Beatrix
  AssignClass (f704d114-0788-4f16-ad6a-c2f01f269bcf)
 Call ID: f704d114-0788-4f16-ad6a-c2f01f269bcf
  Args:
    type: :Woman
    source: Wilhelmina
  AssignClass (f9d4c878-b2fd-4fd7-b49d-ff5da3595581)
 Call ID: f9d4c878-b2fd-4fd7-b49d-ff5da3595581
  Args:
    source: Wilhelmina
    type: :Person
  AddTriple (ea99b8bf-c978-42d9-ae82-4a55e79c371d)
 Call ID: ea99b8bf-c978-42d9-ae82-4a55e79c371d
  Args:
    relation: :hasMother
    source: Juliana
    target: Wilhelmina
  AssignClass (f628424a-ca39-4430-84d9-1936ad226eb1)
 Call ID: f628424a-ca39-4430-84d9-1936ad226eb1
  Args:
    type: :Woman
    source: Irene
  AssignClass (49f1d62f-aa1d-4ada-8568-31e5dc530dc6)
 Call ID: 49f1d62f-aa1d-4ada-8568-31e5dc530dc6
  Args:
    type: :Person
    source: Irene
  AddTriple (07ff767e-024c-4a10-be90-f5c3bc69d7b8)
 Call ID: 07ff767e-024c-4a10-be90-f5c3bc69d7b8
  Args:
    relation: :hasMother
    source: Irene
    target: Juliana
  AddTriple (57848ae9-cacc-4721-91b0-a4af0aee383d)
 Call ID: 57848ae9-cacc-4721-91b0-a4af0aee383d
  Args:
    source: Irene
    relation: :hasFather
    target: Bernhard
  AssignClass (0aae2116-fa44-4d93-933c-821fe23226ab)
 Call ID: 0aae2116-fa44-4d93-933c-821fe23226ab
  Args:
    type: :Woman
    source: Margriet
  AssignClass (b92c7623-1d1b-4feb-bfb4-06e05d9f7172)
 Call ID: b92c7623-1d1b-4feb-bfb4-06e05d9f7172
  Args:
    type: :Person
    source: Margriet
  AddTriple (57fe3580-154c-49d1-84f6-6439748c882d)
 Call ID: 57fe3580-154c-49d1-84f6-6439748c882d
  Args:
    relation: :hasMother
    source: Margriet
    target: Juliana
  AddTriple (2db9be21-b9f7-40b6-803b-4c2fb7db9148)
 Call ID: 2db9be21-b9f7-40b6-803b-4c2fb7db9148
  Args:
    target: Bernhard
    relation: :hasFather
    source: Margriet
  AssignClass (6d539462-490e-434e-b666-211cab198d63)
 Call ID: 6d539462-490e-434e-b666-211cab198d63
  Args:
    source: Claus_von_Amsberg
    type: :Man
  AssignClass (0dfce2a7-63e2-491f-b409-0c6c337060a7)
 Call ID: 0dfce2a7-63e2-491f-b409-0c6c337060a7
  Args:
    type: :Person
    source: Claus_von_Amsberg
  AddTriple (078dbc45-4329-4d37-834f-6b6893b6e062)
 Call ID: 078dbc45-4329-4d37-834f-6b6893b6e062
  Args:
    target: Claus_von_Amsberg
    relation: :hasRelation
    source: Beatrix
  AddLiteral (6e5f8d17-bd00-4ee1-b21e-328abbaaf8a3)
 Call ID: 6e5f8d17-bd00-4ee1-b21e-328abbaaf8a3
  Args:
    relation: :hasMarriageYear
    source: Beatrix
    literal_type: xsd:positiveInteger
    literal_value: 1966
  AssignClass (1a58d6a8-71b0-4de1-a9be-6578e69858e8)
 Call ID: 1a58d6a8-71b0-4de1-a9be-6578e69858e8
  Args:
    type: :Man
    source: Willem-Alexander
  AssignClass (1c8d6cae-a9ce-4681-9f5a-67767ad58993)
 Call ID: 1c8d6cae-a9ce-4681-9f5a-67767ad58993
  Args:
    source: Willem-Alexander
    type: :Person
  AddTriple (dbe6b3ea-ac19-404a-8182-423ac2ce493d)
 Call ID: dbe6b3ea-ac19-404a-8182-423ac2ce493d
  Args:
    source: Willem-Alexander
    relation: :hasMother
    target: Beatrix
  AddTriple (c6010d82-7433-402a-902a-21c4130ac965)
 Call ID: c6010d82-7433-402a-902a-21c4130ac965
  Args:
    source: Willem-Alexander
    relation: :hasFather
    target: Claus_von_Amsberg
  Finish (96e30636-d70e-4bb3-9a68-5b2ccddb2595)
 Call ID: 96e30636-d70e-4bb3-9a68-5b2ccddb2595
  Args: