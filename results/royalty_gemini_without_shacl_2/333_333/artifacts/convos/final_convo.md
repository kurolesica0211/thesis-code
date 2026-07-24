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
  AssignClass (709b055d-7f0f-426b-be11-c0f344ae9171)
 Call ID: 709b055d-7f0f-426b-be11-c0f344ae9171
  Args:
    type: :Woman
    source: :Anne-Marie
  AssignClass (ee66ac0f-d830-4433-8e71-3d4df1545a1b)
 Call ID: ee66ac0f-d830-4433-8e71-3d4df1545a1b
  Args:
    type: :Person
    source: :Anne-Marie
  AddLiteral (c540f4f5-d61d-4381-aa12-7989e4513edb)
 Call ID: c540f4f5-d61d-4381-aa12-7989e4513edb
  Args:
    relation: :hasBirthYear
    source: :Anne-Marie
    literal_value: 1946
    literal_type: xsd:positiveInteger
  AssignClass (9a81eed7-0dc2-4e27-853c-823446ea5e69)
 Call ID: 9a81eed7-0dc2-4e27-853c-823446ea5e69
  Args:
    type: :Man
    source: :Frederik_IX
  AssignClass (b2549b36-b62a-4ea0-927c-0247fe3c9102)
 Call ID: b2549b36-b62a-4ea0-927c-0247fe3c9102
  Args:
    type: :Person
    source: :Frederik_IX
  AssignClass (6e5d40e2-7f4b-4ded-946a-56289c3c190e)
 Call ID: 6e5d40e2-7f4b-4ded-946a-56289c3c190e
  Args:
    type: :Woman
    source: :Ingrid_of_Sweden
  AssignClass (760c0ca7-9302-479a-b113-ada85340e1e9)
 Call ID: 760c0ca7-9302-479a-b113-ada85340e1e9
  Args:
    type: :Person
    source: :Ingrid_of_Sweden
  AddTriple (57b2cef4-9b7e-4f6b-91ba-7133c55edb97)
 Call ID: 57b2cef4-9b7e-4f6b-91ba-7133c55edb97
  Args:
    target: :Frederik_IX
    source: :Anne-Marie
    relation: :hasFather
  AddTriple (50316441-35c6-49e8-9a57-4b3fc8919ce9)
 Call ID: 50316441-35c6-49e8-9a57-4b3fc8919ce9
  Args:
    target: :Ingrid_of_Sweden
    source: :Anne-Marie
    relation: :hasMother
  AssignClass (e6341578-a61c-4892-999e-ef5da1518ba5)
 Call ID: e6341578-a61c-4892-999e-ef5da1518ba5
  Args:
    type: :Man
    source: :Constantine_II
  AssignClass (84f44a2b-c6ce-4a90-a8b0-0472f3a66262)
 Call ID: 84f44a2b-c6ce-4a90-a8b0-0472f3a66262
  Args:
    type: :Person
    source: :Constantine_II
  AddLiteral (5b2cd776-b2b6-4a36-b37f-b51aa668a6f9)
 Call ID: 5b2cd776-b2b6-4a36-b37f-b51aa668a6f9
  Args:
    literal_value: 1964
    relation: :hasMarriageYear
    source: :Anne-Marie
    literal_type: xsd:positiveInteger
  AddTriple (76a88db1-1f96-4cc9-a0f7-ab619b9c0b5f)
 Call ID: 76a88db1-1f96-4cc9-a0f7-ab619b9c0b5f
  Args:
    source: :Anne-Marie
    relation: :hasRelation
    target: :Constantine_II
  AssignClass (138f5f2b-5591-4564-b63f-04fde774d36f)
 Call ID: 138f5f2b-5591-4564-b63f-04fde774d36f
  Args:
    type: :Woman
    source: :Margrethe_II
  AssignClass (0819c481-3204-4494-a532-8050319e1be3)
 Call ID: 0819c481-3204-4494-a532-8050319e1be3
  Args:
    type: :Person
    source: :Margrethe_II
  AssignClass (e84f2dab-96d9-4761-96a1-41a2d2da0053)
 Call ID: e84f2dab-96d9-4761-96a1-41a2d2da0053
  Args:
    type: :Woman
    source: :Benedikte
  AssignClass (ba0091db-6459-4c6e-b95f-ff59e4a11f37)
 Call ID: ba0091db-6459-4c6e-b95f-ff59e4a11f37
  Args:
    type: :Person
    source: :Benedikte
  AddTriple (3d8bbf7a-33f9-429d-bee3-62f72a9a04fc)
 Call ID: 3d8bbf7a-33f9-429d-bee3-62f72a9a04fc
  Args:
    target: :Margrethe_II
    source: :Anne-Marie
    relation: :isSisterOf
  AddTriple (4606f027-a723-49e6-991f-39b5360efd34)
 Call ID: 4606f027-a723-49e6-991f-39b5360efd34
  Args:
    target: :Benedikte
    relation: :isSisterOf
    source: :Anne-Marie
  AssignClass (a43fd908-1326-4465-b552-93dcdb2ca2cb)
 Call ID: a43fd908-1326-4465-b552-93dcdb2ca2cb
  Args:
    type: :Woman
    source: :Alexia
  AssignClass (57fe7945-9dda-4234-b695-294a07b859f9)
 Call ID: 57fe7945-9dda-4234-b695-294a07b859f9
  Args:
    type: :Person
    source: :Alexia
  AssignClass (eaaccac6-6f5a-4ac9-a8be-fbe5c44a6ba7)
 Call ID: eaaccac6-6f5a-4ac9-a8be-fbe5c44a6ba7
  Args:
    type: :Man
    source: :Pavlos
  AssignClass (93e18ce9-b846-46f2-8a0d-6be2542af193)
 Call ID: 93e18ce9-b846-46f2-8a0d-6be2542af193
  Args:
    type: :Person
    source: :Pavlos
  AssignClass (5795227f-e0a6-4cc1-aba8-99f6102e1636)
 Call ID: 5795227f-e0a6-4cc1-aba8-99f6102e1636
  Args:
    type: :Man
    source: :Nikolaos
  AssignClass (979335dd-ea50-4446-b07f-d407ecf8351e)
 Call ID: 979335dd-ea50-4446-b07f-d407ecf8351e
  Args:
    type: :Person
    source: :Nikolaos
  AssignClass (53981a1d-462f-46ca-a7bf-97a1aec633ad)
 Call ID: 53981a1d-462f-46ca-a7bf-97a1aec633ad
  Args:
    type: :Woman
    source: :Theodora
  AssignClass (a663bebb-5ab1-4e97-a2dc-50ba1d4c3a6c)
 Call ID: a663bebb-5ab1-4e97-a2dc-50ba1d4c3a6c
  Args:
    type: :Person
    source: :Theodora
  AssignClass (8ea963bc-0be5-4ed6-bfd3-0658f3242976)
 Call ID: 8ea963bc-0be5-4ed6-bfd3-0658f3242976
  Args:
    type: :Man
    source: :Philippos
  AssignClass (3d51f501-89fa-4d6e-a9f4-caf536943395)
 Call ID: 3d51f501-89fa-4d6e-a9f4-caf536943395
  Args:
    type: :Person
    source: :Philippos
  AddTriple (8accc66b-7dad-4c93-92e9-438ddf691b41)
 Call ID: 8accc66b-7dad-4c93-92e9-438ddf691b41
  Args:
    target: :Alexia
    relation: :hasChild
    source: :Anne-Marie
  AddTriple (f832b6a0-447c-4b91-825e-339971f4f166)
 Call ID: f832b6a0-447c-4b91-825e-339971f4f166
  Args:
    source: :Anne-Marie
    relation: :hasChild
    target: :Pavlos
  AddTriple (714c6448-befd-42a3-b056-b846a8393b04)
 Call ID: 714c6448-befd-42a3-b056-b846a8393b04
  Args:
    source: :Anne-Marie
    relation: :hasChild
    target: :Nikolaos
  AddTriple (b2f7cdbb-5dd7-400e-b30f-cd0556066a12)
 Call ID: b2f7cdbb-5dd7-400e-b30f-cd0556066a12
  Args:
    relation: :hasChild
    source: :Anne-Marie
    target: :Theodora
  AddTriple (96afecd7-d974-4a21-840c-e35355109e6f)
 Call ID: 96afecd7-d974-4a21-840c-e35355109e6f
  Args:
    source: :Anne-Marie
    relation: :hasChild
    target: :Philippos
  AddTriple (6d87b5c1-e59b-42cc-9306-b7ed741c5037)
 Call ID: 6d87b5c1-e59b-42cc-9306-b7ed741c5037
  Args:
    target: :Alexia
    relation: :hasChild
    source: :Constantine_II
  AddTriple (8f6eb1e0-3eed-4bad-af29-047d7ca55cd4)
 Call ID: 8f6eb1e0-3eed-4bad-af29-047d7ca55cd4
  Args:
    source: :Constantine_II
    relation: :hasChild
    target: :Pavlos
  AddTriple (7f7e77af-601f-4f3d-b76d-b32819298a12)
 Call ID: 7f7e77af-601f-4f3d-b76d-b32819298a12
  Args:
    target: :Nikolaos
    source: :Constantine_II
    relation: :hasChild
  AddTriple (7c14c20b-d0f9-4be3-b722-1fb4739900e0)
 Call ID: 7c14c20b-d0f9-4be3-b722-1fb4739900e0
  Args:
    target: :Theodora
    source: :Constantine_II
    relation: :hasChild
  AddTriple (183364d6-e4cd-424b-9ac9-bbc1423f3e2c)
 Call ID: 183364d6-e4cd-424b-9ac9-bbc1423f3e2c
  Args:
    source: :Constantine_II
    relation: :hasChild
    target: :Philippos
  AssignClass (31c64ce8-7cc6-4be8-b2e2-094bb3f51b93)
 Call ID: 31c64ce8-7cc6-4be8-b2e2-094bb3f51b93
  Args:
    type: :Woman
    source: :Frederica_of_Greece
  AssignClass (eee233a5-a581-4358-8f4f-54c59b147a55)
 Call ID: eee233a5-a581-4358-8f4f-54c59b147a55
  Args:
    type: :Person
    source: :Frederica_of_Greece
  AssignClass (e56d18e5-872d-4617-b288-f9c6b9429772)
 Call ID: e56d18e5-872d-4617-b288-f9c6b9429772
  Args:
    type: :Man
    source: :Paul_of_Greece
  AssignClass (44ea48c7-3006-475a-b27b-5db4b3cab696)
 Call ID: 44ea48c7-3006-475a-b27b-5db4b3cab696
  Args:
    type: :Person
    source: :Paul_of_Greece
  AddTriple (66146412-6060-4a37-a753-3d0cd009e05e)
 Call ID: 66146412-6060-4a37-a753-3d0cd009e05e
  Args:
    target: :Paul_of_Greece
    relation: :hasFather
    source: :Constantine_II
  AddTriple (5137fdca-a14e-49f8-a17b-aa1b2b25e659)
 Call ID: 5137fdca-a14e-49f8-a17b-aa1b2b25e659
  Args:
    target: :Frederica_of_Greece
    source: :Constantine_II
    relation: :hasMother
  AssignClass (46fdbd4c-4fb7-4bd4-a87c-550c9531ed6d)
 Call ID: 46fdbd4c-4fb7-4bd4-a87c-550c9531ed6d
  Args:
    type: :Woman
    source: :Sophia_of_Greece_and_Denmark
  AssignClass (b57c190d-a8c1-48b3-82cf-9266f32c346a)
 Call ID: b57c190d-a8c1-48b3-82cf-9266f32c346a
  Args:
    type: :Person
    source: :Sophia_of_Greece_and_Denmark
  AddTriple (dd40d4ef-8deb-4dab-822d-fde489c98b48)
 Call ID: dd40d4ef-8deb-4dab-822d-fde489c98b48
  Args:
    target: :Constantine_II
    source: :Sophia_of_Greece_and_Denmark
    relation: :isSisterOf
  AssignClass (a267050c-b3e4-40b6-8bb8-6ef4dbfdb09c)
 Call ID: a267050c-b3e4-40b6-8bb8-6ef4dbfdb09c
  Args:
    type: :Man
    source: :Juan_Carlos_of_Spain
  AssignClass (fc3c16fd-7224-44e7-aff5-1fde25f62899)
 Call ID: fc3c16fd-7224-44e7-aff5-1fde25f62899
  Args:
    type: :Person
    source: :Juan_Carlos_of_Spain
  AddTriple (c4f94fc5-1aa6-45fb-8f20-9dabc31e75fc)
 Call ID: c4f94fc5-1aa6-45fb-8f20-9dabc31e75fc
  Args:
    target: :Juan_Carlos_of_Spain
    relation: :hasRelation
    source: :Sophia_of_Greece_and_Denmark
  AssignClass (8bdca35f-b960-4db2-964a-1ed5b4fb6442)
 Call ID: 8bdca35f-b960-4db2-964a-1ed5b4fb6442
  Args:
    type: :Man
    source: :Christian_X_of_Denmark
  AssignClass (0444bc77-60fa-46ad-afe1-e7cbc8280974)
 Call ID: 0444bc77-60fa-46ad-afe1-e7cbc8280974
  Args:
    type: :Person
    source: :Christian_X_of_Denmark
  AssignClass (887d2252-0d63-46c0-be7b-f61d58f0ab3b)
 Call ID: 887d2252-0d63-46c0-be7b-f61d58f0ab3b
  Args:
    type: :Woman
    source: :Alexandrine_of_Mecklenburg-Schwerin
  AssignClass (2bdd5479-1c96-4822-93ff-1f3240e4d0db)
 Call ID: 2bdd5479-1c96-4822-93ff-1f3240e4d0db
  Args:
    type: :Person
    source: :Alexandrine_of_Mecklenburg-Schwerin
  AddTriple (26f7b240-2860-452f-8ed1-0abce09b9333)
 Call ID: 26f7b240-2860-452f-8ed1-0abce09b9333
  Args:
    target: :Christian_X_of_Denmark
    source: :Frederik_IX
    relation: :hasFather
  AddTriple (141e0fcc-62db-481c-89de-744b9c52b5e9)
 Call ID: 141e0fcc-62db-481c-89de-744b9c52b5e9
  Args:
    target: :Alexandrine_of_Mecklenburg-Schwerin
    relation: :hasMother
    source: :Frederik_IX
  AssignClass (12a22ec6-8cc2-44b1-9972-9847031b9be1)
 Call ID: 12a22ec6-8cc2-44b1-9972-9847031b9be1
  Args:
    type: :Man
    source: :Gustaf_VI_Adolf
  AssignClass (f3b5aece-c108-4aad-80c5-0c25605a91eb)
 Call ID: f3b5aece-c108-4aad-80c5-0c25605a91eb
  Args:
    type: :Person
    source: :Gustaf_VI_Adolf
  AssignClass (80ab49e0-c8ba-41fb-b6de-f3ce3de8d76f)
 Call ID: 80ab49e0-c8ba-41fb-b6de-f3ce3de8d76f
  Args:
    type: :Woman
    source: :Margaret_of_Connaught
  AssignClass (9c6b6a51-b8e4-4ac3-afd4-acb3077b823f)
 Call ID: 9c6b6a51-b8e4-4ac3-afd4-acb3077b823f
  Args:
    type: :Person
    source: :Margaret_of_Connaught
  AddTriple (3a5e736b-581e-4d4c-bc52-242794f047ae)
 Call ID: 3a5e736b-581e-4d4c-bc52-242794f047ae
  Args:
    target: :Gustaf_VI_Adolf
    relation: :hasFather
    source: :Ingrid_of_Sweden
  AddTriple (d588daa7-7e40-4fa3-88e7-c6c89e2195f0)
 Call ID: d588daa7-7e40-4fa3-88e7-c6c89e2195f0
  Args:
    target: :Margaret_of_Connaught
    relation: :hasMother
    source: :Ingrid_of_Sweden
  Finish (4530af09-3aa7-4ae5-9304-227b9317e9d8)
 Call ID: 4530af09-3aa7-4ae5-9304-227b9317e9d8
  Args: