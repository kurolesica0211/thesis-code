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
Queen Anne-Marie


Queen Sofía of Spain


Marina, consort of Prince Michael


Queen Margrethe II


Anne-Marie RE (Greek: Άννα-Μαρία, romanized: Ánna-María; born Princess Anne-Marie Dagmar Ingrid of Denmark, 30 August 1946) is a Danish princess who was Queen of Greece as the consort of King Constantine II from their marriage on 18 September 1964 until the abolition of the Greek monarchy on 1 June 1973.
Anne-Marie is the youngest daughter of Frederik IX of Denmark and Ingrid of Sweden.
In 1964, she married Constantine and became queen consort of Greece.
As queen, Anne-Marie spent much of her time working for a charitable foundation known as "Her Majesty's Fund", a foundation established by her mother-in-law, Queen Frederica of Greece.
In 1967, Anne-Marie and her family were forced into exile upon the rise of a military dictatorship.
Anne-Marie and her family were stripped of their Greek citizenship and had their property revoked, leading them to sue in the European Court of Human Rights.
From the compensation she earned, Anne-Marie set up the "Anne-Marie Foundation", which provided assistance to people in rural areas of Greece.
In 2013, she and Constantine moved back to Greece.
They moved to Athens in 2022, where Constantine died in January the following year.
Birth and family

Anne-Marie was born on 30 August 1946 at Frederik VIII's Palace, an 18th-century palace which forms part of the Amalienborg Palace complex in central Copenhagen.
She was the third and last daughter and child of Crown Prince Frederik and Crown Princess Ingrid of Denmark.
Her father was the eldest son of Christian X of Denmark and Alexandrine of Mecklenburg-Schwerin; her mother, born a princess of Sweden, was the only daughter of the Crown Prince of Sweden (later King Gustaf VI Adolf) and Princess Margaret of Connaught.
At birth, Anne-Marie had two elder sisters: Princess Margrethe (later queen of Denmark) and Princess Benedikte (who became princess of Sayn-Wittgenstein-Berleburg).
Anne-Marie was baptised on 9 October at the Holmen Church in Copenhagen.
Her godparents were her paternal grandparents, King Christian X and Queen Alexandrine of Denmark; her maternal grandfather, Crown Prince Gustaf Adolf of Sweden; her maternal uncle Prince Bertil, Duke of Halland; her paternal great-uncle King Haakon VII of Norway; her paternal great-aunt Princess Dagmar of Denmark; her grandfather's cousin Prince George of Greece and Denmark; her father's cousin, Crown Princess Märtha of Norway; Queen Mary of the United Kingdom; and Crown Princess Juliana of the Netherlands.
Anne-Marie is a great-great-granddaughter of both Queen Victoria and Christian IX of Denmark.
Therefore, she is related to many other members of European royalty, such as her future husband Constantine II, who is also a great-great-grandchild of both Queen Victoria and Christian IX of Denmark.
Moreover, Anne-Marie is the maternal aunt of Frederik X of Denmark, the first cousin of Carl XVI Gustaf of Sweden, and an aunt by marriage of Felipe VI of Spain.
Early life

Anne-Marie and her sisters grew up in apartments at Frederik VIII's Palace at Amalienborg in Copenhagen and in Fredensborg Palace in North Zealand.
On 20 April 1947, less than a year after Anne-Marie's birth, her grandfather, Christian X, died, and her father ascended the throne as King Frederik IX.
At the time of her father's accession to the throne, only males could ascend the throne of Denmark.
As Anne-Marie's parents had no sons, it was assumed that her paternal uncle, Prince Knud, would one day assume the throne.
The popularity of Frederik IX and his daughters and the more prominent role of women in Danish life paved the way for a new Act of Succession in 1953 which permitted female succession to the throne following the principle of male-preference primogeniture, where a female can ascend to the throne if she has no brothers.
Her eldest sister, Margrethe, therefore became heir presumptive, and Benedikte and Anne-Marie became second and third in the line of succession.
Anne-Marie was educated at N. Zahle's School, a private school in Copenhagen, from 1952 to 1961.
Upon returning from schooling, Anne-Marie undertook childcare work for a few years.
Marriage

In 1959, at the age of 13, Anne-Marie first met her future husband, her third cousin Constantine, Crown Prince of Greece, who accompanied his parents, King Paul and Queen Frederica, on a state visit to Denmark.
Constantine at the time was 19 years old.
They met a second time in Denmark in 1961, when Constantine declared to his parents his intention to marry Anne-Marie.
The pair became secretly engaged without telling the public nor members of their families due to Frederik IX's opposition to their relationship because of her young age.
They met again in Athens in May 1962 at the wedding of Constantine's older sister, Princess Sophia of Greece and Denmark, and Prince Juan Carlos of Spain.
Anne-Marie was a bridesmaid, while Constantine was a groomsman for the future monarchs of Spain.
Following this, Anne-Marie began studying the history of Greece and the history of the Greek monarchy, as well as taking Modern Greek lessons in order to learn the language of the country her husband was to reign over.
Constantine's mother, Frederica, initially requested that one million dollars be spent on the wedding, however, the private office of the Danish royal family denied this.
In July 1964, the announcement of the engagement of Constantine and Anne-Marie raised the polite protests of the Left in Denmark.
Previously, on 6 March 1964, King Paul died, and Constantine succeeded him as King of the Hellenes.
However, Frederica requested that their marriage take place on its original date.
Anne-Marie and Constantine were married on 18 September 1964 (two weeks after Anne-Marie's 18th birthday) in the Metropolis, the Greek Orthodox Cathedral of Athens.
Anne-Marie converted from Lutheranism to the Greek Orthodox Church 7 months and 3 days after her marriage.
There was a special permission, for this, from the Archbishop of Athens and all Greece, who is the head of the Orthodox Church of Greece.
Also, as she was marrying a foreign ruler, consent to the marriage was given on the condition that Anne-Marie renounce her succession rights to the Danish throne for herself and her descendants.
Queen of the Hellenes

As Queen of Greece, Anne-Marie's initial primary role was to provide the nation with an heir who would eventually take over as King.
Anne-Marie spent much of her time working for a charitable foundation known as "Her Majesty's Fund" and later as the "Anne-Marie Foundation", which provided assistance to people in rural areas of Greece.
Her Majesty's Fund was an organisation set up by Frederica during her husband's reign which aimed at assisting the poor and disadvantaged.
Anne-Marie also worked closely with the Red Cross and other not-for-profit charities.
On 10 July 1965, Queen Anne-Marie gave birth at the villa Mon Repos in Corfu to her first child, Princess Alexia, who was heir presumptive to the throne of Greece, from her birth until the birth of her younger brother Crown Prince Pavlos on 20 May 1967 in accordance with Greece's order of succession adhering to male-preference primogeniture.
At the time of Alexia and Pavlos' births, political stability within Greece was diminishing due to a schism between Constantine and the Prime Minister Georgios Papandreou, who wished to demote the minister of defence, Petros Garoufalias, in order to assume office himself.
A group of Greek soldiers in April 1967 overthrew the government of the new Prime Minister, Panagiotis Kanellopoulos, which marked the beginning of a military dictatorship in Greece.
The royal family was left unaware and in order to avoid fighting, Constantine and Anne-Marie agreed to recognise the dictatorship against their will, however many members of the public therefore believed that they supported and even funded the coup.
The following month, Anne-Marie gave birth to a son, Pavlos, who immediately assumed the position of Crown Prince of Greece from his sister.
At his baptism, Anne-Marie and Constantine decided to make Frederica his godmother and the Hellenic Army his godfather figure.
Margrethe II of Denmark, the future queen of Denmark, was married to Henri de Laborde de Monpezat at their wedding on 10 June 1967.
Anne-Marie, the sister of Margrethe, and Constantine were subsequently denied an invite to their wedding, further ruining relations for a period of time.
Exile

In December 1967, Constantine attempted to shake off the military's authoritarian regime by trying to stage a counter-coup with the help of his political allies.
Upon the coup's abandonment, the military junta in Greece strongly advised Anne-Marie and Constantine to leave the country.
Anne-Marie and Constantine fled to nearby Italy and sought refuge at the Greek Embassy in Rome, where Anne-Marie and Constantine became puppet monarchs.
After two months of refuge at the Greek Embassy, Anne-Marie and Constantine received greeting from Moritz, Landgrave of Hesse, who organised to put them up at the Villa Polissena, an Italian palace where Moritz himself had previously lived upon his family's exile.
Anne-Marie eventually agreed with Constantine to move to 13 Via di Porta Latina, where a large villa owned by Countess Cristina Paolozzi was located.
Possibly due to stress and worry, Anne-Marie suffered a miscarriage in early 1968.
Anne-Marie fell pregnant again in February of the next year and gave birth to Prince Nikolaos of Greece and Denmark.
Anne-Marie and Constantine established a small school in their villa to preserve the Greek culture among their children.
Despite the expansion of their family, Anne-Marie and Constantine had been experiencing some marital struggles in the early 1970s.
It was reported that Anne-Marie in 1974 was considering filing a divorce and moving back to Denmark, however, their relationship was repaired and even "strengthened" as a result.
Throughout this time, although they were living in exile, Anne-Marie and Constantine still formally remained the monarchs of Greece.
They were still allowed to represent Greece and the Greek crown at international royal events.
For example, the pair attended the 21st birthday of Charles, Prince of Wales, in 1969, the 2500th anniversary of the founding of the Persian Empire in 1971, and the baptism in Madrid of François, the eldest son of Alfonso, Duke of Anjou and Cádiz.
One of the last events Anne-Marie and Constantine attended as the monarchs of Greece was the funeral of Frederik IX, Anne-Marie's father, whom she grieved deeply.
Dethronement

The military junta in Greece began noticeably distancing itself from the monarchy when Georgios Zoitakis replaced Georgios Papadopoulos as the Regent of Greece.
In 1972, Constantine's face was replaced on coins by a phoenix, a symbol of the Greek military and the national bird of Greece.(Palmer & Greece 1990, p. 114)
Anne-Marie and Constantine were officially dethroned by the 1974 Greek republic referendum on 29 July 1974.
Margrethe II immediately agreed to house Anne-Marie, Constantine and their family in Amalienborg for a year.
Anne-Marie moved with her family to England.
The military dictatorship in Greece collapsed in 1974 after a failed coup d'état, which aimed to unite Greece and Cyprus.
It was hoped that their positions as King and Queen of the Hellenes would be restored as democracy was reinstated, but another referendum confirmed that the monarchy would stay abolished and the Third Hellenic Republic was finally formed.
The new Greek government continued to enforce the exile of Anne-Marie and her family as they saw them as a threat to the new republic.
They were denied entry into the country even for Frederica's funeral.
Frederica had died in exile in February 1981 in Madrid, where she had been staying with her daughter, Sofía.
In London, Anne-Marie established with Constantine the Hellenic College of London to again help their children learn the Greek language and culture.
Anne-Marie and Constantine received financial aid from Hussein of Jordan and Mohammad Reza Pahlavi, the Shah of Iran.
Following a miscarriage in 1980, Anne-Marie and Constantine agreed to expand their family.
After the christening of Prince Peter of Yugoslavia, whom Anne-Marie and Constantine baptised, the couple welcomed Princess Theodora in June 1983 and later Prince Philippos in April 1986.
In 1989, the silver anniversary of Anne-Marie's marriage to Constantine was celebrated at Kronborg Castle in Denmark.
Return to Greece

The government of Greece in 1991 granted Anne-Marie and Constantine permission to retrieve over 68 tonnes of their belongings to either keep or sell.
Two years later, the couple were allowed to enter Greece again in a private visit on their yacht with their children.
When the family stopped for oil at a port in southern Greece, Anne-Marie and Constantine were swarmed with crowds of people and press, who greeted them with cheers and claps.
This was called evidence that the pair still held "real influence in Greece".
Finally, the government stripped the Greek royal family of their Greek citizenship and passport, unless they renounced their dynastic rights, abandoned the name "of Greece" and swore an oath to the republic.
Anne-Marie and Constantine called it "the greatest insult in this world for a Greek to be told that he is not a Greek".
In addition, they were accused by the Greek government of tampering with the 1974 republic referendum results by officiating the marriage of Pavlos and Marie-Chantal Miller in London as a real princely marriage.
Anne-Marie and Constantine, along with Princess Irene and Princess Katherine, made the decision to take the Greek government to court in April 1996 over the confiscation of their citizenships and properties.
The Supreme Civil and Criminal Court of Greece agreed with their discrimination claim, however, the Council of State overrode their decision and stated that the removal of their passports was a measure taken that conforms with the constitution of the Third Republic.
As a result, the family took Greece to court in the European Court of Human Rights and sued them for €200 million.
Of the €200 million claim, Anne-Marie and Constantine won €12 million, Irene won €900,000 and Katherine €300,000.
Although originally requesting Spanish citizenships, Anne-Marie eventually requested from her sister, Margrethe II, to have Danish diplomatic passports established in the names of the members of the Greek royal family.
She agreed and in their Danish passports, their names were established as "HM Queen Anne-Marie" and "HM King Constantine II".
In 2003, Constantine used the money they received to establish the Anna-Maria Foundation, a not-for-profit organisation aimed to provide aid to victims of natural disasters, particularly those of floods, earthquakes and bushfires.
Since 2019, Anne-Marie has headed the foundation as its president.
On 14 August 2004, Anne-Marie and her husband Constantine visited their former home in Athens, the former Royal Palace, which is now the Presidential Palace, for the first time since 1967.
They were received by then-President of Greece Costis Stephanopoulos along with other members of the International Olympic Committee, of which Constantine was an honorary member.
In December 2004, Constantine, Anne-Marie and their children were again invited to pay a personal private visit by President Stephanopoulos.
Once the games concluded, the government announced that Anne-Marie and Constantine's exile would finally be revoked.
In 2013, Anne-Marie and Constantine returned to reside in Greece.
They sold their home in London for €11.5 million and announced their return to Greece.
He and his wife, Anne-Marie, purchased a villa in Porto Cheli, Peloponnese residing there until they relocated to Athens in the spring of 2022.
For her 60th birthday, Anne-Marie boarded the cruise ship the Aphroessa, which Constantine had organised for her.
Constantine began experiencing health and mobility issues, leading to him requiring more care from Anne-Marie.
On 10 January 2023, Anne-Marie became widowed when her husband died of a stroke at the private Hygeia Hospital in Athens at the age of 82.
On 19 December 2024, Anne-Marie's children and five of her grandchildren applied for Greek citizenship, selecting the surname "Ντε Γκρες" (De Grèce; "of Greece").
Anne-Marie did not apply, with it being reported that she was "not interested".
Titles, styles, honours, and arms

Titles and styles

She has been the titular Queen of the Hellenes since 1973.
This title is not recognized under the terms of the republican Constitution of Greece.
Honours

National

Foreign

Arms and monogram

The coats of arms of Queen Anne-Marie combine the 1936–1973 royal coat of arms of Greece and the 1948–1972 coat of arms of Denmark which was current at the time of her marriage in 1964.
Issue

Constantine and Anne-Marie had five children:


Ancestry

References

Citations

Bibliography

External links



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix ns1: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
@prefix ns2: <http://www.w3.org/2003/11/swrl#> .
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

ns1:isRuleEnabled a owl:AnnotationProperty .

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

:x a ns2:Variable .

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

:y a ns2:Variable .

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

[] a ns2:Imp ;
    rdfs:label "infer hasSon" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasBrother" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasSister" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (b8e8a26b-2026-46a1-975d-b249ebe8b4ab)
 Call ID: b8e8a26b-2026-46a1-975d-b249ebe8b4ab
  Args:
    source: :Anne-Marie
    type: :Woman
  AssignClass (e2eabf45-5b26-4def-a295-10583031e001)
 Call ID: e2eabf45-5b26-4def-a295-10583031e001
  Args:
    type: :Person
    source: :Anne-Marie
  AddLiteral (2480f632-0824-4e37-812f-9114fff85e8a)
 Call ID: 2480f632-0824-4e37-812f-9114fff85e8a
  Args:
    literal_value: 1946
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: :Anne-Marie
  AssignClass (692d8d54-0de3-4095-9397-ca096079fcdd)
 Call ID: 692d8d54-0de3-4095-9397-ca096079fcdd
  Args:
    source: :FrederikIX
    type: :Man
  AssignClass (4925726b-f08e-4da7-bb1f-e9735e8d240b)
 Call ID: 4925726b-f08e-4da7-bb1f-e9735e8d240b
  Args:
    source: :FrederikIX
    type: :Person
  AssignClass (c85b48df-eec8-484e-b6df-ceaf89f922b6)
 Call ID: c85b48df-eec8-484e-b6df-ceaf89f922b6
  Args:
    type: :Woman
    source: :IngridOfSweden
  AssignClass (9ce4f691-ba46-43bb-812e-84082fb74110)
 Call ID: 9ce4f691-ba46-43bb-812e-84082fb74110
  Args:
    type: :Person
    source: :IngridOfSweden
  AddTriple (aa43ccf7-16c7-415e-85b7-b32314089689)
 Call ID: aa43ccf7-16c7-415e-85b7-b32314089689
  Args:
    target: :FrederikIX
    source: :Anne-Marie
    relation: :hasFather
  AddTriple (00a4a585-2335-423e-af5d-85ab79c74dc4)
 Call ID: 00a4a585-2335-423e-af5d-85ab79c74dc4
  Args:
    source: :Anne-Marie
    relation: :hasMother
    target: :IngridOfSweden
  AssignClass (b3fefab3-8f38-431a-90f2-14cfb971ee86)
 Call ID: b3fefab3-8f38-431a-90f2-14cfb971ee86
  Args:
    source: :ConstantineII
    type: :Man
  AssignClass (a496f7ae-81a8-4425-818a-5bbbd43e49b9)
 Call ID: a496f7ae-81a8-4425-818a-5bbbd43e49b9
  Args:
    type: :Person
    source: :ConstantineII
  AddTriple (36eb08fa-36a3-4715-bf29-5c77522fc1db)
 Call ID: 36eb08fa-36a3-4715-bf29-5c77522fc1db
  Args:
    target: :ConstantineII
    relation: :hasRelation
    source: :Anne-Marie
  AddLiteral (532b7d8d-03eb-4bef-b14f-1d15f48e4c7f)
 Call ID: 532b7d8d-03eb-4bef-b14f-1d15f48e4c7f
  Args:
    literal_value: 1964
    literal_type: xsd:integer
    relation: :hasMarriageYear
    source: :Anne-Marie
  AddLiteral (9ac96cee-a866-4486-bc19-a43bbd5dd38b)
 Call ID: 9ac96cee-a866-4486-bc19-a43bbd5dd38b
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: :ConstantineII
    literal_value: 2023
  AssignClass (b34e0cfa-dd06-4f9a-b0f4-f4be28764792)
 Call ID: b34e0cfa-dd06-4f9a-b0f4-f4be28764792
  Args:
    source: :MargretheII
    type: :Woman
  AssignClass (3d9feb3a-b1a2-4998-b204-9de1d2c2dcc5)
 Call ID: 3d9feb3a-b1a2-4998-b204-9de1d2c2dcc5
  Args:
    type: :Person
    source: :MargretheII
  AssignClass (b1c0decf-34c1-47a5-8e92-320303de97e2)
 Call ID: b1c0decf-34c1-47a5-8e92-320303de97e2
  Args:
    type: :Woman
    source: :Benedikte
  AssignClass (b7161a75-3166-4da4-9df3-777814e37764)
 Call ID: b7161a75-3166-4da4-9df3-777814e37764
  Args:
    source: :Benedikte
    type: :Person
  AddTriple (8a030549-df88-4cfe-a11f-3fec4e6b2b89)
 Call ID: 8a030549-df88-4cfe-a11f-3fec4e6b2b89
  Args:
    source: :Anne-Marie
    relation: :isSiblingOf
    target: :MargretheII
  AddTriple (a9b432a0-b539-47b3-afa5-9eeb129e6798)
 Call ID: a9b432a0-b539-47b3-afa5-9eeb129e6798
  Args:
    source: :Anne-Marie
    relation: :isSiblingOf
    target: :Benedikte
  AssignClass (031a5ae8-df26-4afb-954b-ddabca13de6e)
 Call ID: 031a5ae8-df26-4afb-954b-ddabca13de6e
  Args:
    type: :Man
    source: :ChristianX
  AssignClass (e6f2585d-09ef-48c8-a025-aa502f8b8476)
 Call ID: e6f2585d-09ef-48c8-a025-aa502f8b8476
  Args:
    type: :Person
    source: :ChristianX
  AssignClass (913fc04d-eb27-46b6-8960-1cea25f3bb44)
 Call ID: 913fc04d-eb27-46b6-8960-1cea25f3bb44
  Args:
    source: :AlexandrineOfMecklenburgSchwerin
    type: :Woman
  AssignClass (d39fb601-ab87-4442-9042-936ea4e63b4b)
 Call ID: d39fb601-ab87-4442-9042-936ea4e63b4b
  Args:
    source: :AlexandrineOfMecklenburgSchwerin
    type: :Person
  AddTriple (f6d14239-9de7-4a9f-9c5d-debaaaa5759f)
 Call ID: f6d14239-9de7-4a9f-9c5d-debaaaa5759f
  Args:
    target: :ChristianX
    relation: :hasFather
    source: :FrederikIX
  AddTriple (c24ac239-33f8-498e-a351-3d230706aba9)
 Call ID: c24ac239-33f8-498e-a351-3d230706aba9
  Args:
    source: :FrederikIX
    relation: :hasMother
    target: :AlexandrineOfMecklenburgSchwerin
  AssignClass (fe3d6871-841f-4af7-8172-ce87696e648e)
 Call ID: fe3d6871-841f-4af7-8172-ce87696e648e
  Args:
    source: :GustafVIAdolf
    type: :Man
  AssignClass (386ec709-254c-4de4-a0ef-afba0b97102b)
 Call ID: 386ec709-254c-4de4-a0ef-afba0b97102b
  Args:
    type: :Person
    source: :GustafVIAdolf
  AssignClass (d0ddc4cc-eee8-45c4-9bd3-e91f7a79320e)
 Call ID: d0ddc4cc-eee8-45c4-9bd3-e91f7a79320e
  Args:
    source: :MargaretOfConnaught
    type: :Woman
  AssignClass (45628691-6ada-456c-b03d-105178285218)
 Call ID: 45628691-6ada-456c-b03d-105178285218
  Args:
    source: :MargaretOfConnaught
    type: :Person
  AddTriple (f21000b3-36c8-4100-bdcb-93675a57e154)
 Call ID: f21000b3-36c8-4100-bdcb-93675a57e154
  Args:
    source: :IngridOfSweden
    relation: :hasFather
    target: :GustafVIAdolf
  AddTriple (a6f96bca-2a1a-4991-a822-e3f68a64e1e7)
 Call ID: a6f96bca-2a1a-4991-a822-e3f68a64e1e7
  Args:
    source: :IngridOfSweden
    relation: :hasMother
    target: :MargaretOfConnaught
  AssignClass (3f78e2e2-ce19-4bb9-a91b-6c24f03bc72d)
 Call ID: 3f78e2e2-ce19-4bb9-a91b-6c24f03bc72d
  Args:
    type: :Woman
    source: :Alexia
  AssignClass (04de2934-bae0-4588-aebd-34c1703eda02)
 Call ID: 04de2934-bae0-4588-aebd-34c1703eda02
  Args:
    source: :Alexia
    type: :Person
  AssignClass (bf3e6288-f976-4dc6-b8c2-1c10b30b396d)
 Call ID: bf3e6288-f976-4dc6-b8c2-1c10b30b396d
  Args:
    source: :Pavlos
    type: :Man
  AssignClass (6bfbb0d9-6724-476d-b6e1-489296b590c2)
 Call ID: 6bfbb0d9-6724-476d-b6e1-489296b590c2
  Args:
    type: :Person
    source: :Pavlos
  AssignClass (09515bb1-cd57-45b5-8d88-593435175d03)
 Call ID: 09515bb1-cd57-45b5-8d88-593435175d03
  Args:
    source: :Nikolaos
    type: :Man
  AssignClass (633c12cd-3ebc-4436-8f66-06f1ffdd4fdf)
 Call ID: 633c12cd-3ebc-4436-8f66-06f1ffdd4fdf
  Args:
    type: :Person
    source: :Nikolaos
  AssignClass (ac1cf910-8067-4957-9c58-c01c44cd820f)
 Call ID: ac1cf910-8067-4957-9c58-c01c44cd820f
  Args:
    type: :Woman
    source: :Theodora
  AssignClass (8b805d22-80f6-44d8-841b-404d2eb56f7a)
 Call ID: 8b805d22-80f6-44d8-841b-404d2eb56f7a
  Args:
    type: :Person
    source: :Theodora
  AssignClass (97b5b0da-fe97-4f68-961a-941d66aae421)
 Call ID: 97b5b0da-fe97-4f68-961a-941d66aae421
  Args:
    type: :Man
    source: :Philippos
  AssignClass (9229fab6-f00d-4686-874d-b804d37de4ef)
 Call ID: 9229fab6-f00d-4686-874d-b804d37de4ef
  Args:
    type: :Person
    source: :Philippos
  AddTriple (04d0bcc3-7b99-4c51-86e6-09725f5dc125)
 Call ID: 04d0bcc3-7b99-4c51-86e6-09725f5dc125
  Args:
    target: :Anne-Marie
    relation: :isChildOf
    source: :Alexia
  AddTriple (b6a803dd-e74c-4bf6-bef4-278f63e0b0c9)
 Call ID: b6a803dd-e74c-4bf6-bef4-278f63e0b0c9
  Args:
    relation: :isChildOf
    source: :Alexia
    target: :ConstantineII
  AddTriple (f1a421ab-0ff9-4e01-a9af-46da49bc1515)
 Call ID: f1a421ab-0ff9-4e01-a9af-46da49bc1515
  Args:
    relation: :isChildOf
    source: :Pavlos
    target: :Anne-Marie
  AddTriple (ee5a1791-0c0a-4888-9fb3-bafb432e0157)
 Call ID: ee5a1791-0c0a-4888-9fb3-bafb432e0157
  Args:
    relation: :isChildOf
    source: :Pavlos
    target: :ConstantineII
  AddTriple (ab7d9641-2885-4660-a6b1-83dde19fc31a)
 Call ID: ab7d9641-2885-4660-a6b1-83dde19fc31a
  Args:
    target: :Anne-Marie
    relation: :isChildOf
    source: :Nikolaos
  AddTriple (d288aaa7-3c71-49e1-85d0-c106457cccc5)
 Call ID: d288aaa7-3c71-49e1-85d0-c106457cccc5
  Args:
    relation: :isChildOf
    source: :Nikolaos
    target: :ConstantineII
  AddTriple (c52099f1-31bb-434a-bde8-028d77362a65)
 Call ID: c52099f1-31bb-434a-bde8-028d77362a65
  Args:
    target: :Anne-Marie
    source: :Theodora
    relation: :isChildOf
  AddTriple (c833e796-244d-46ca-8052-37c836554035)
 Call ID: c833e796-244d-46ca-8052-37c836554035
  Args:
    source: :Theodora
    relation: :isChildOf
    target: :ConstantineII
  AddTriple (f1f49531-d9bc-437f-aff2-80378a5d442d)
 Call ID: f1f49531-d9bc-437f-aff2-80378a5d442d
  Args:
    source: :Philippos
    relation: :isChildOf
    target: :Anne-Marie
  AddTriple (af97cbb9-e95a-416e-a18b-c55e9c161348)
 Call ID: af97cbb9-e95a-416e-a18b-c55e9c161348
  Args:
    target: :ConstantineII
    source: :Philippos
    relation: :isChildOf
  AssignClass (89720d21-8bd3-49e7-aeb1-4f038326f8a7)
 Call ID: 89720d21-8bd3-49e7-aeb1-4f038326f8a7
  Args:
    type: :Woman
    source: :FredericaOfGreece
  AssignClass (371517f6-98e1-4a19-9771-3fdb59aa2e48)
 Call ID: 371517f6-98e1-4a19-9771-3fdb59aa2e48
  Args:
    source: :FredericaOfGreece
    type: :Person
  AssignClass (812b80b4-588c-4bfa-a448-0f9825182701)
 Call ID: 812b80b4-588c-4bfa-a448-0f9825182701
  Args:
    source: :PaulOfGreece
    type: :Man
  AssignClass (30da5fc8-26e4-4be5-9029-4c496f728336)
 Call ID: 30da5fc8-26e4-4be5-9029-4c496f728336
  Args:
    type: :Person
    source: :PaulOfGreece
  AddTriple (3fd08f99-796c-4f88-a0dd-012e38372971)
 Call ID: 3fd08f99-796c-4f88-a0dd-012e38372971
  Args:
    target: :PaulOfGreece
    source: :ConstantineII
    relation: :hasFather
  AddTriple (7734cc32-cc5a-4693-99c9-982ff44a6fb4)
 Call ID: 7734cc32-cc5a-4693-99c9-982ff44a6fb4
  Args:
    source: :ConstantineII
    relation: :hasMother
    target: :FredericaOfGreece
  AssignClass (49af3ab5-04f3-4a22-bd0e-f51c4e0db424)
 Call ID: 49af3ab5-04f3-4a22-bd0e-f51c4e0db424
  Args:
    type: :Woman
    source: :SophiaOfGreeceAndDenmark
  AssignClass (11c6fc2e-51ff-4542-99fb-fbb02c7ec35f)
 Call ID: 11c6fc2e-51ff-4542-99fb-fbb02c7ec35f
  Args:
    source: :SophiaOfGreeceAndDenmark
    type: :Person
  AddTriple (f696ecad-8f88-4793-be35-bccbbf637c6a)
 Call ID: f696ecad-8f88-4793-be35-bccbbf637c6a
  Args:
    target: :SophiaOfGreeceAndDenmark
    relation: :isSiblingOf
    source: :ConstantineII
  AssignClass (0883eceb-c425-426d-a6d0-ac07d594b05a)
 Call ID: 0883eceb-c425-426d-a6d0-ac07d594b05a
  Args:
    source: :JuanCarlosOfSpain
    type: :Man
  AssignClass (338c882f-4925-402f-acca-0aa06fd0c863)
 Call ID: 338c882f-4925-402f-acca-0aa06fd0c863
  Args:
    source: :JuanCarlosOfSpain
    type: :Person
  AddTriple (a5532722-4e33-4bd8-947b-f9c7ba7996ac)
 Call ID: a5532722-4e33-4bd8-947b-f9c7ba7996ac
  Args:
    target: :JuanCarlosOfSpain
    relation: :hasRelation
    source: :SophiaOfGreeceAndDenmark
  AssignClass (46bbae76-6ccd-4015-bdec-b1beb68f89f7)
 Call ID: 46bbae76-6ccd-4015-bdec-b1beb68f89f7
  Args:
    type: :Man
    source: :FrederikXOfDenmark
  AssignClass (cc7ac45e-2dcc-47c1-a499-8be58f0f7701)
 Call ID: cc7ac45e-2dcc-47c1-a499-8be58f0f7701
  Args:
    source: :FrederikXOfDenmark
    type: :Person
  AssignClass (e6be65db-8606-4bc6-9d3e-23020823a3df)
 Call ID: e6be65db-8606-4bc6-9d3e-23020823a3df
  Args:
    type: :Man
    source: :CarlXVIGustafOfSweden
  AssignClass (ce818186-8096-4d02-8daf-20ee3a654d35)
 Call ID: ce818186-8096-4d02-8daf-20ee3a654d35
  Args:
    source: :CarlXVIGustafOfSweden
    type: :Person
  AssignClass (6043bf5b-c294-4f99-8a1b-18284901b666)
 Call ID: 6043bf5b-c294-4f99-8a1b-18284901b666
  Args:
    type: :Man
    source: :FelipeVIOfSpain
  AssignClass (e54e5af5-0fc4-40ae-b7f8-a491c28c54ef)
 Call ID: e54e5af5-0fc4-40ae-b7f8-a491c28c54ef
  Args:
    source: :FelipeVIOfSpain
    type: :Person
  Finish (35fbc6df-1e5e-4d1f-96b0-72f8fd1b982d)
 Call ID: 35fbc6df-1e5e-4d1f-96b0-72f8fd1b982d
  Args: