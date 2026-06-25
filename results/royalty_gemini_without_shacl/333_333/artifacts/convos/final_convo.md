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
  AssignClass (2399546b-a970-4a88-8659-93277e83be76)
 Call ID: 2399546b-a970-4a88-8659-93277e83be76
  Args:
    type: :Woman
    source: Anne-Marie
  AssignClass (4b91624e-5301-4fa2-82d0-e6dd3f2cfb9f)
 Call ID: 4b91624e-5301-4fa2-82d0-e6dd3f2cfb9f
  Args:
    source: Anne-Marie
    type: :Person
  AddLiteral (df63d2a9-7d68-4240-974f-9022b5b9ff7e)
 Call ID: df63d2a9-7d68-4240-974f-9022b5b9ff7e
  Args:
    literal_type: xsd:integer
    source: Anne-Marie
    literal_value: 1946
    relation: :hasBirthYear
  AssignClass (d6b84bc0-76f1-4bc4-b9f9-b93da24c29dd)
 Call ID: d6b84bc0-76f1-4bc4-b9f9-b93da24c29dd
  Args:
    source: Frederik_IX_of_Denmark
    type: :Man
  AssignClass (8a87c2ca-9b09-49fd-add5-cb0c815cb50b)
 Call ID: 8a87c2ca-9b09-49fd-add5-cb0c815cb50b
  Args:
    type: :Person
    source: Frederik_IX_of_Denmark
  AssignClass (e6817ddd-694a-4979-a2e7-13b4e4b6e6b5)
 Call ID: e6817ddd-694a-4979-a2e7-13b4e4b6e6b5
  Args:
    source: Ingrid_of_Sweden
    type: :Woman
  AssignClass (8116a93d-f113-4852-9d68-cc4a1e8acce9)
 Call ID: 8116a93d-f113-4852-9d68-cc4a1e8acce9
  Args:
    type: :Person
    source: Ingrid_of_Sweden
  AddTriple (a194c8ff-77f3-4f95-b2ec-f8a7115bd420)
 Call ID: a194c8ff-77f3-4f95-b2ec-f8a7115bd420
  Args:
    source: Anne-Marie
    target: Frederik_IX_of_Denmark
    relation: :hasFather
  AddTriple (6d74023d-55e1-4f63-bb51-c4a257df2c49)
 Call ID: 6d74023d-55e1-4f63-bb51-c4a257df2c49
  Args:
    target: Ingrid_of_Sweden
    source: Anne-Marie
    relation: :hasMother
  AssignClass (1b19825c-0e15-4b93-912d-2d34af6f596f)
 Call ID: 1b19825c-0e15-4b93-912d-2d34af6f596f
  Args:
    source: Constantine_II_of_Greece
    type: :Man
  AssignClass (b64e37e2-ea15-4f2e-9f59-7fae25d68f78)
 Call ID: b64e37e2-ea15-4f2e-9f59-7fae25d68f78
  Args:
    source: Constantine_II_of_Greece
    type: :Person
  AddLiteral (8df5da61-c626-4780-8102-5218e902b00b)
 Call ID: 8df5da61-c626-4780-8102-5218e902b00b
  Args:
    source: Anne-Marie
    literal_type: xsd:integer
    literal_value: 1964
    relation: :hasMarriageYear
  AddTriple (c77c3a5e-0c08-424d-8261-b2d65c3bc3ac)
 Call ID: c77c3a5e-0c08-424d-8261-b2d65c3bc3ac
  Args:
    relation: :hasRelation
    source: Anne-Marie
    target: Constantine_II_of_Greece
  AssignClass (5c699137-2e0e-4df8-911c-e16d605e0a01)
 Call ID: 5c699137-2e0e-4df8-911c-e16d605e0a01
  Args:
    source: Princess_Alexia
    type: :Woman
  AssignClass (81740ce5-7e88-4e91-8204-45645f618451)
 Call ID: 81740ce5-7e88-4e91-8204-45645f618451
  Args:
    type: :Person
    source: Princess_Alexia
  AddTriple (565f5336-9a91-461e-ba6a-e976a48eae40)
 Call ID: 565f5336-9a91-461e-ba6a-e976a48eae40
  Args:
    source: Anne-Marie
    target: Princess_Alexia
    relation: :hasChild
  AddTriple (58f1e81e-faf7-4b80-9fdc-5b5590da3b79)
 Call ID: 58f1e81e-faf7-4b80-9fdc-5b5590da3b79
  Args:
    relation: :hasFather
    source: Princess_Alexia
    target: Constantine_II_of_Greece
  AssignClass (b816e196-cea8-4576-ad97-0027d5b0f44e)
 Call ID: b816e196-cea8-4576-ad97-0027d5b0f44e
  Args:
    source: Crown_Prince_Pavlos
    type: :Man
  AssignClass (17fe65d4-3393-47bf-a0cc-3fa8c8792308)
 Call ID: 17fe65d4-3393-47bf-a0cc-3fa8c8792308
  Args:
    type: :Person
    source: Crown_Prince_Pavlos
  AddTriple (c3ad6846-064f-41ae-8731-dc72aacfa1a2)
 Call ID: c3ad6846-064f-41ae-8731-dc72aacfa1a2
  Args:
    relation: :hasChild
    source: Anne-Marie
    target: Crown_Prince_Pavlos
  AddTriple (a6fe7b35-ac64-4866-8d76-0d091308695b)
 Call ID: a6fe7b35-ac64-4866-8d76-0d091308695b
  Args:
    relation: :hasFather
    source: Crown_Prince_Pavlos
    target: Constantine_II_of_Greece
  AssignClass (e5083aca-1d2d-41f0-a9ae-b916f145ea4f)
 Call ID: e5083aca-1d2d-41f0-a9ae-b916f145ea4f
  Args:
    source: Prince_Nikolaos
    type: :Man
  AssignClass (2dc708d9-33b8-4e4c-b2a8-2dae6f8fa11b)
 Call ID: 2dc708d9-33b8-4e4c-b2a8-2dae6f8fa11b
  Args:
    type: :Person
    source: Prince_Nikolaos
  AddTriple (997e2172-03e9-4af9-bb29-21340a1e2851)
 Call ID: 997e2172-03e9-4af9-bb29-21340a1e2851
  Args:
    source: Anne-Marie
    target: Prince_Nikolaos
    relation: :hasChild
  AddTriple (7e55e2cd-ca61-4889-b4ef-35d54f71bf55)
 Call ID: 7e55e2cd-ca61-4889-b4ef-35d54f71bf55
  Args:
    target: Constantine_II_of_Greece
    source: Prince_Nikolaos
    relation: :hasFather
  AssignClass (7ce9a277-175d-49b2-bb0c-a43f94641e2e)
 Call ID: 7ce9a277-175d-49b2-bb0c-a43f94641e2e
  Args:
    type: :Woman
    source: Princess_Theodora
  AssignClass (50788c8d-cd94-41bf-8af1-ca1a06878178)
 Call ID: 50788c8d-cd94-41bf-8af1-ca1a06878178
  Args:
    source: Princess_Theodora
    type: :Person
  AddTriple (9a319c56-38e6-4ca0-a996-9e6123242c12)
 Call ID: 9a319c56-38e6-4ca0-a996-9e6123242c12
  Args:
    relation: :hasChild
    target: Princess_Theodora
    source: Anne-Marie
  AddTriple (f31a5b63-98b1-4557-9bc3-beb0cf35c10a)
 Call ID: f31a5b63-98b1-4557-9bc3-beb0cf35c10a
  Args:
    target: Constantine_II_of_Greece
    source: Princess_Theodora
    relation: :hasFather
  AssignClass (d2b1f441-c9ab-40e1-a3b0-19915aeb4e5c)
 Call ID: d2b1f441-c9ab-40e1-a3b0-19915aeb4e5c
  Args:
    type: :Man
    source: Prince_Philippos
  AssignClass (6e92f4bb-7aed-4b9e-843c-2e2ba3d18f93)
 Call ID: 6e92f4bb-7aed-4b9e-843c-2e2ba3d18f93
  Args:
    source: Prince_Philippos
    type: :Person
  AddTriple (f47c1ece-f681-430a-9319-5cda7278393b)
 Call ID: f47c1ece-f681-430a-9319-5cda7278393b
  Args:
    target: Prince_Philippos
    source: Anne-Marie
    relation: :hasChild
  AddTriple (bf2886dc-43b7-40cb-835f-d87d2b9ff5b3)
 Call ID: bf2886dc-43b7-40cb-835f-d87d2b9ff5b3
  Args:
    source: Prince_Philippos
    target: Constantine_II_of_Greece
    relation: :hasFather
  AssignClass (b2029f72-0363-4a4c-baba-c8560fa7d014)
 Call ID: b2029f72-0363-4a4c-baba-c8560fa7d014
  Args:
    source: Queen_Margrethe_II
    type: :Woman
  AssignClass (00d75892-c74e-4450-804f-dd18995da802)
 Call ID: 00d75892-c74e-4450-804f-dd18995da802
  Args:
    type: :Person
    source: Queen_Margrethe_II
  AddTriple (d7d70120-b091-4619-bac1-35bc1e6b257e)
 Call ID: d7d70120-b091-4619-bac1-35bc1e6b257e
  Args:
    relation: :isSisterOf
    source: Anne-Marie
    target: Queen_Margrethe_II
  AssignClass (e42800c6-ea15-4313-8531-4e92c62d42b2)
 Call ID: e42800c6-ea15-4313-8531-4e92c62d42b2
  Args:
    type: :Woman
    source: Princess_Benedikte
  AssignClass (971ab95a-ada7-437b-987d-1a89373fc8a4)
 Call ID: 971ab95a-ada7-437b-987d-1a89373fc8a4
  Args:
    source: Princess_Benedikte
    type: :Person
  AddTriple (2d811cb4-e268-4033-af5c-e65955911909)
 Call ID: 2d811cb4-e268-4033-af5c-e65955911909
  Args:
    relation: :isSisterOf
    target: Princess_Benedikte
    source: Anne-Marie
  AssignClass (b07a4d31-d855-4dbc-bbc3-6c240d988d04)
 Call ID: b07a4d31-d855-4dbc-bbc3-6c240d988d04
  Args:
    source: Queen_Frederica_of_Greece
    type: :Woman
  AssignClass (c3dae9a1-10f4-4a4a-886b-d5d093f8eb2e)
 Call ID: c3dae9a1-10f4-4a4a-886b-d5d093f8eb2e
  Args:
    type: :Person
    source: Queen_Frederica_of_Greece
  AddTriple (d0fdb086-a1e8-41c8-ae62-4ac5d25d985f)
 Call ID: d0fdb086-a1e8-41c8-ae62-4ac5d25d985f
  Args:
    source: Constantine_II_of_Greece
    target: Queen_Frederica_of_Greece
    relation: :hasMother
  AssignClass (abf77c0b-b109-405e-b8b4-e1fe7cfc4798)
 Call ID: abf77c0b-b109-405e-b8b4-e1fe7cfc4798
  Args:
    source: King_Paul_of_Greece
    type: :Man
  AssignClass (773bd741-b0d4-44c9-96e8-f4711e4ca421)
 Call ID: 773bd741-b0d4-44c9-96e8-f4711e4ca421
  Args:
    type: :Person
    source: King_Paul_of_Greece
  AddTriple (5543e233-e80a-4a27-9a84-19c821528d25)
 Call ID: 5543e233-e80a-4a27-9a84-19c821528d25
  Args:
    relation: :hasFather
    source: Constantine_II_of_Greece
    target: King_Paul_of_Greece
  AssignClass (eaaf1dbd-0426-4d55-aa69-975ccc96a9ad)
 Call ID: eaaf1dbd-0426-4d55-aa69-975ccc96a9ad
  Args:
    source: Queen_Sofia_of_Spain
    type: :Woman
  AssignClass (61cdab4a-af72-44a9-a226-fb4ee27003a7)
 Call ID: 61cdab4a-af72-44a9-a226-fb4ee27003a7
  Args:
    type: :Person
    source: Queen_Sofia_of_Spain
  AddTriple (1c20680b-4131-4b7c-a04e-8dae6860be76)
 Call ID: 1c20680b-4131-4b7c-a04e-8dae6860be76
  Args:
    target: Queen_Sofia_of_Spain
    source: Constantine_II_of_Greece
    relation: :isSisterOf
  Finish (06b5186e-44a5-4a92-881f-9409a48f367e)
 Call ID: 06b5186e-44a5-4a92-881f-9409a48f367e
  Args: