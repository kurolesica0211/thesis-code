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
  AssignClass (5cbd583b-570e-4bd0-aba7-a50fff6f0fd9)
 Call ID: 5cbd583b-570e-4bd0-aba7-a50fff6f0fd9
  Args:
    source: Beatrix
    type: :Woman
  AssignClass (4375edcf-18a2-45c5-99c1-522d2700d1f3)
 Call ID: 4375edcf-18a2-45c5-99c1-522d2700d1f3
  Args:
    type: :Person
    source: Beatrix
  AddLiteral (98db4cf7-7c87-4d42-89f1-ddf7e7b90fa1)
 Call ID: 98db4cf7-7c87-4d42-89f1-ddf7e7b90fa1
  Args:
    literal_value: 1938
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Beatrix
  AssignClass (07b8ec44-0868-4421-8584-6a9ac1be49cb)
 Call ID: 07b8ec44-0868-4421-8584-6a9ac1be49cb
  Args:
    source: Juliana
    type: :Woman
  AssignClass (d32f1e6f-74f8-4e91-a910-eb085a3bb0d6)
 Call ID: d32f1e6f-74f8-4e91-a910-eb085a3bb0d6
  Args:
    source: Juliana
    type: :Person
  AssignClass (54a6d745-d288-47ca-a132-3899525c6e7e)
 Call ID: 54a6d745-d288-47ca-a132-3899525c6e7e
  Args:
    source: Bernhard
    type: :Man
  AssignClass (9e0477a9-f066-483c-b86f-207fe1c3e3c0)
 Call ID: 9e0477a9-f066-483c-b86f-207fe1c3e3c0
  Args:
    type: :Person
    source: Bernhard
  AddTriple (544e5c50-5db6-4eac-993a-b2bdfed749ab)
 Call ID: 544e5c50-5db6-4eac-993a-b2bdfed749ab
  Args:
    relation: :hasMother
    source: Beatrix
    target: Juliana
  AddTriple (6f08797f-6908-403c-8cc8-50427cf1e0b5)
 Call ID: 6f08797f-6908-403c-8cc8-50427cf1e0b5
  Args:
    target: Bernhard
    relation: :hasFather
    source: Beatrix
  AssignClass (e08a1d90-8e7c-46a2-95dd-f4eb2ea3dd40)
 Call ID: e08a1d90-8e7c-46a2-95dd-f4eb2ea3dd40
  Args:
    source: Irene
    type: :Woman
  AssignClass (9c3a938e-27c0-4ac3-b168-3cd19c64bff8)
 Call ID: 9c3a938e-27c0-4ac3-b168-3cd19c64bff8
  Args:
    source: Irene
    type: :Person
  AddTriple (36b30817-5df7-4360-a1ba-d7588cf19739)
 Call ID: 36b30817-5df7-4360-a1ba-d7588cf19739
  Args:
    relation: :isSisterOf
    source: Irene
    target: Beatrix
  AddTriple (b448048f-cae8-4535-ad64-ed74aa1be3d6)
 Call ID: b448048f-cae8-4535-ad64-ed74aa1be3d6
  Args:
    target: Juliana
    source: Irene
    relation: :hasMother
  AssignClass (7550d16f-ed3b-45b9-beb5-f764e421d1e4)
 Call ID: 7550d16f-ed3b-45b9-beb5-f764e421d1e4
  Args:
    type: :Woman
    source: Margriet
  AssignClass (aac07285-fa7a-43de-b092-113fec8bf5fc)
 Call ID: aac07285-fa7a-43de-b092-113fec8bf5fc
  Args:
    source: Margriet
    type: :Person
  AddTriple (aae178fd-d44c-4ad3-a5fe-b032af4b832d)
 Call ID: aae178fd-d44c-4ad3-a5fe-b032af4b832d
  Args:
    source: Margriet
    relation: :isSisterOf
    target: Beatrix
  AddTriple (b0916c88-ccdb-4d7d-9758-ae66761c6d39)
 Call ID: b0916c88-ccdb-4d7d-9758-ae66761c6d39
  Args:
    relation: :hasMother
    source: Margriet
    target: Juliana
  AssignClass (597099d0-3943-4dc6-ab24-aa075bf14234)
 Call ID: 597099d0-3943-4dc6-ab24-aa075bf14234
  Args:
    source: Claus_von_Amsberg
    type: :Man
  AssignClass (ea894b51-5755-427f-a14a-da8837ba1ae7)
 Call ID: ea894b51-5755-427f-a14a-da8837ba1ae7
  Args:
    source: Claus_von_Amsberg
    type: :Person
  AddTriple (49ac1f4e-efba-4a7b-a98d-bec6af1105a8)
 Call ID: 49ac1f4e-efba-4a7b-a98d-bec6af1105a8
  Args:
    target: Claus_von_Amsberg
    source: Beatrix
    relation: :hasRelation
  AddLiteral (1769e074-401b-4c6b-9bb0-1ac23f24d66a)
 Call ID: 1769e074-401b-4c6b-9bb0-1ac23f24d66a
  Args:
    source: Beatrix
    literal_type: xsd:integer
    literal_value: 1966
    relation: :hasMarriageYear
  AssignClass (9d4e6ca4-c833-4998-9d9f-5c9101a84349)
 Call ID: 9d4e6ca4-c833-4998-9d9f-5c9101a84349
  Args:
    type: :Man
    source: Willem-Alexander
  AssignClass (8ebfbe92-0a3a-49e2-b658-5f3e3253a2df)
 Call ID: 8ebfbe92-0a3a-49e2-b658-5f3e3253a2df
  Args:
    type: :Person
    source: Willem-Alexander
  AddTriple (54e1f347-c3cb-4fb5-9386-355c3111c9bf)
 Call ID: 54e1f347-c3cb-4fb5-9386-355c3111c9bf
  Args:
    target: Beatrix
    relation: :isSonOf
    source: Willem-Alexander
  Finish (39be6c2b-d264-46fe-9a17-35e06477d7cc)
 Call ID: 39be6c2b-d264-46fe-9a17-35e06477d7cc
  Args: