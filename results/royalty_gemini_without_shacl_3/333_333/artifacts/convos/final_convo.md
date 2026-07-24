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
  AssignClass (a7ae0edc-1830-4be1-a489-9c8467ee8baf)
 Call ID: a7ae0edc-1830-4be1-a489-9c8467ee8baf
  Args:
    type: :Woman
    source: Anne-Marie
  AssignClass (ee30a5fe-aac4-4ee5-8934-0523361476b2)
 Call ID: ee30a5fe-aac4-4ee5-8934-0523361476b2
  Args:
    type: :Man
    source: Constantine_II
  AssignClass (cf3496a3-73ea-408c-895b-2621fa3c5f51)
 Call ID: cf3496a3-73ea-408c-895b-2621fa3c5f51
  Args:
    type: :Man
    source: Frederik_IX
  AssignClass (3fc47163-3dea-4c4b-86fc-f0ed8e8c726a)
 Call ID: 3fc47163-3dea-4c4b-86fc-f0ed8e8c726a
  Args:
    type: :Woman
    source: Ingrid_of_Sweden
  AssignClass (cb63608b-2469-43ad-b6f5-da77af174014)
 Call ID: cb63608b-2469-43ad-b6f5-da77af174014
  Args:
    type: :Man
    source: Christian_X
  AssignClass (cc627969-809b-4c75-a330-6f0becab39ef)
 Call ID: cc627969-809b-4c75-a330-6f0becab39ef
  Args:
    type: :Woman
    source: Alexandrine_of_Mecklenburg-Schwerin
  AssignClass (a0a34d39-b222-4353-8744-64f1e665e9d8)
 Call ID: a0a34d39-b222-4353-8744-64f1e665e9d8
  Args:
    type: :Man
    source: Gustaf_VI_Adolf
  AssignClass (193e3230-6cf7-4427-85b4-28a33b1ed55f)
 Call ID: 193e3230-6cf7-4427-85b4-28a33b1ed55f
  Args:
    type: :Woman
    source: Margaret_of_Connaught
  AssignClass (eab346c2-da3e-4939-9eb8-62bb33a81ed0)
 Call ID: eab346c2-da3e-4939-9eb8-62bb33a81ed0
  Args:
    type: :Woman
    source: Margrethe_II
  AssignClass (45a356ef-09e0-44a2-a0c5-b6971d512acd)
 Call ID: 45a356ef-09e0-44a2-a0c5-b6971d512acd
  Args:
    type: :Woman
    source: Benedikte
  AssignClass (44d5bebf-e4ea-4629-b605-33730a8f5dba)
 Call ID: 44d5bebf-e4ea-4629-b605-33730a8f5dba
  Args:
    type: :Man
    source: Paul_of_Greece
  AssignClass (57d27b0b-364c-4b33-8d22-8db38b81f915)
 Call ID: 57d27b0b-364c-4b33-8d22-8db38b81f915
  Args:
    type: :Woman
    source: Frederica_of_Greece
  AssignClass (1ea4bec2-f01e-46dc-9d21-f2a23e99fdfd)
 Call ID: 1ea4bec2-f01e-46dc-9d21-f2a23e99fdfd
  Args:
    type: :Woman
    source: Alexia
  AssignClass (b049842e-3fe1-4b50-a4c2-5970d3091152)
 Call ID: b049842e-3fe1-4b50-a4c2-5970d3091152
  Args:
    type: :Man
    source: Pavlos
  AssignClass (10f707bc-d4dd-4ecd-ad07-7e58e04887c9)
 Call ID: 10f707bc-d4dd-4ecd-ad07-7e58e04887c9
  Args:
    type: :Man
    source: Nikolaos
  AssignClass (a18add20-4572-4c52-a5e8-6caa28f154c5)
 Call ID: a18add20-4572-4c52-a5e8-6caa28f154c5
  Args:
    type: :Woman
    source: Theodora
  AssignClass (69af4826-567e-4e15-9bb2-5b8cda4cd232)
 Call ID: 69af4826-567e-4e15-9bb2-5b8cda4cd232
  Args:
    type: :Man
    source: Philippos
  AddLiteral (70fca532-087f-432c-88e5-f1f5bf1bc143)
 Call ID: 70fca532-087f-432c-88e5-f1f5bf1bc143
  Args:
    literal_value: 1946
    relation: :hasBirthYear
    source: Anne-Marie
    literal_type: xsd:integer
  AddTriple (afa69862-5919-41d0-8963-4afcb37f6fe9)
 Call ID: afa69862-5919-41d0-8963-4afcb37f6fe9
  Args:
    source: Anne-Marie
    relation: :hasFather
    target: Frederik_IX
  AddTriple (28360089-65db-4b98-8ed5-9c702f6e9efb)
 Call ID: 28360089-65db-4b98-8ed5-9c702f6e9efb
  Args:
    relation: :hasMother
    source: Anne-Marie
    target: Ingrid_of_Sweden
  AddTriple (76b4f0c8-6220-4da4-9030-11a7bbcf1a03)
 Call ID: 76b4f0c8-6220-4da4-9030-11a7bbcf1a03
  Args:
    target: Christian_X
    relation: :hasFather
    source: Frederik_IX
  AddTriple (22798407-2361-46ae-9e1d-55a419937fb2)
 Call ID: 22798407-2361-46ae-9e1d-55a419937fb2
  Args:
    source: Frederik_IX
    relation: :hasMother
    target: Alexandrine_of_Mecklenburg-Schwerin
  AddTriple (ef738318-6771-4295-9b32-405065e205cd)
 Call ID: ef738318-6771-4295-9b32-405065e205cd
  Args:
    relation: :hasFather
    source: Ingrid_of_Sweden
    target: Gustaf_VI_Adolf
  AddTriple (df455994-74e0-4764-9883-438aa2dc28f0)
 Call ID: df455994-74e0-4764-9883-438aa2dc28f0
  Args:
    source: Ingrid_of_Sweden
    relation: :hasMother
    target: Margaret_of_Connaught
  AddTriple (ecdd1fee-1b7c-41f6-9b20-ea0372d89a45)
 Call ID: ecdd1fee-1b7c-41f6-9b20-ea0372d89a45
  Args:
    source: Anne-Marie
    relation: :isSisterOf
    target: Margrethe_II
  AddTriple (9b5abc25-2c7e-463c-acae-cde16f372114)
 Call ID: 9b5abc25-2c7e-463c-acae-cde16f372114
  Args:
    relation: :isSisterOf
    source: Anne-Marie
    target: Benedikte
  AddTriple (2ef3aff6-5902-4da5-8c34-d4b758d778e4)
 Call ID: 2ef3aff6-5902-4da5-8c34-d4b758d778e4
  Args:
    target: Paul_of_Greece
    relation: :hasFather
    source: Constantine_II
  AddTriple (52181eaa-8f5f-42f7-b348-5d6976401b76)
 Call ID: 52181eaa-8f5f-42f7-b348-5d6976401b76
  Args:
    target: Frederica_of_Greece
    source: Constantine_II
    relation: :hasMother
  AddTriple (8814782a-da9b-4808-9843-9ece3a63a7e3)
 Call ID: 8814782a-da9b-4808-9843-9ece3a63a7e3
  Args:
    source: Constantine_II
    relation: :hasChild
    target: Alexia
  AddTriple (f919e3a1-9098-444b-8d4f-473b7530c54d)
 Call ID: f919e3a1-9098-444b-8d4f-473b7530c54d
  Args:
    relation: :hasChild
    source: Anne-Marie
    target: Alexia
  AddTriple (c8a3ce58-a2da-44f9-ae69-09744cc46a91)
 Call ID: c8a3ce58-a2da-44f9-ae69-09744cc46a91
  Args:
    target: Pavlos
    relation: :hasChild
    source: Constantine_II
  AddTriple (dde2e15a-78dc-412e-8eee-181286cc3811)
 Call ID: dde2e15a-78dc-412e-8eee-181286cc3811
  Args:
    target: Pavlos
    relation: :hasChild
    source: Anne-Marie
  AddTriple (8c0d7079-13aa-41b4-89e9-7ac39a43debf)
 Call ID: 8c0d7079-13aa-41b4-89e9-7ac39a43debf
  Args:
    target: Nikolaos
    source: Constantine_II
    relation: :hasChild
  AddTriple (1d410463-d9a5-4103-a6ee-f24b3a951bf6)
 Call ID: 1d410463-d9a5-4103-a6ee-f24b3a951bf6
  Args:
    relation: :hasChild
    source: Anne-Marie
    target: Nikolaos
  AddTriple (68b846e8-4d59-450c-a90d-ea724f930208)
 Call ID: 68b846e8-4d59-450c-a90d-ea724f930208
  Args:
    relation: :hasChild
    source: Constantine_II
    target: Theodora
  AddTriple (ab9377e0-bfae-46db-b48b-64c7753110b5)
 Call ID: ab9377e0-bfae-46db-b48b-64c7753110b5
  Args:
    target: Theodora
    relation: :hasChild
    source: Anne-Marie
  AddTriple (8a575d03-eb14-4fa2-90fb-67117e81abef)
 Call ID: 8a575d03-eb14-4fa2-90fb-67117e81abef
  Args:
    target: Philippos
    source: Constantine_II
    relation: :hasChild
  AddTriple (f3462599-6c1b-4282-aa71-163f8ceb1b9a)
 Call ID: f3462599-6c1b-4282-aa71-163f8ceb1b9a
  Args:
    source: Anne-Marie
    relation: :hasChild
    target: Philippos
  AddLiteral (6581c6e1-b0e2-4e47-891f-73edad7631cd)
 Call ID: 6581c6e1-b0e2-4e47-891f-73edad7631cd
  Args:
    literal_type: xsd:integer
    source: Anne-Marie
    relation: :hasMarriageYear
    literal_value: 1964
  AddTriple (3869aff0-7407-46cc-8288-dcfa37baf4d5)
 Call ID: 3869aff0-7407-46cc-8288-dcfa37baf4d5
  Args:
    target: Constantine_II
    relation: :hasRelation
    source: Anne-Marie
  Finish (fb457da4-1634-4d1a-a0ea-eb7a6336c4c3)
 Call ID: fb457da4-1634-4d1a-a0ea-eb7a6336c4c3
  Args: