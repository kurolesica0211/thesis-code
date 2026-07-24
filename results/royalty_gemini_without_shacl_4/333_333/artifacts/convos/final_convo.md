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
  AssignClass (f1a7f15c-5347-4ea6-acf8-82ce5715d1ab)
 Call ID: f1a7f15c-5347-4ea6-acf8-82ce5715d1ab
  Args:
    type: :Woman
    source: Anne-Marie
  AssignClass (8aee1c24-61f7-446f-9793-b9f1a312b3fc)
 Call ID: 8aee1c24-61f7-446f-9793-b9f1a312b3fc
  Args:
    source: Anne-Marie
    type: :Person
  AssignClass (8a505819-3f48-4b28-ae1b-09c2adb4f1ff)
 Call ID: 8a505819-3f48-4b28-ae1b-09c2adb4f1ff
  Args:
    source: Frederik_IX
    type: :Man
  AssignClass (77b5cdfe-078a-494b-8b28-d2182972c970)
 Call ID: 77b5cdfe-078a-494b-8b28-d2182972c970
  Args:
    source: Frederik_IX
    type: :Person
  AssignClass (42fea21e-6388-4769-9497-c57dd2f89ae2)
 Call ID: 42fea21e-6388-4769-9497-c57dd2f89ae2
  Args:
    type: :Woman
    source: Ingrid_of_Sweden
  AssignClass (258d1822-94e2-4aaa-aa23-a1fd15fb3065)
 Call ID: 258d1822-94e2-4aaa-aa23-a1fd15fb3065
  Args:
    type: :Person
    source: Ingrid_of_Sweden
  AddTriple (fdf9e465-1dbd-4a17-8e44-e61c6933d4da)
 Call ID: fdf9e465-1dbd-4a17-8e44-e61c6933d4da
  Args:
    target: Frederik_IX
    relation: :hasFather
    source: Anne-Marie
  AddTriple (60ff851f-daec-42a6-aa73-7ef1f5c3be0c)
 Call ID: 60ff851f-daec-42a6-aa73-7ef1f5c3be0c
  Args:
    target: Ingrid_of_Sweden
    relation: :hasMother
    source: Anne-Marie
  AddLiteral (654d5f20-f951-4092-af54-ec53d36c9ded)
 Call ID: 654d5f20-f951-4092-af54-ec53d36c9ded
  Args:
    relation: :hasBirthYear
    source: Anne-Marie
    literal_type: xsd:positiveInteger
    literal_value: 1946
  AssignClass (04546a27-947c-44bb-af8c-eef9bd44f7a0)
 Call ID: 04546a27-947c-44bb-af8c-eef9bd44f7a0
  Args:
    source: Constantine_II
    type: :Man
  AssignClass (ce0b6360-e637-4595-b531-c2e37f8ac438)
 Call ID: ce0b6360-e637-4595-b531-c2e37f8ac438
  Args:
    source: Constantine_II
    type: :Person
  AddTriple (22c4c458-72b5-4290-a4d3-afd0b423b30b)
 Call ID: 22c4c458-72b5-4290-a4d3-afd0b423b30b
  Args:
    target: Constantine_II
    relation: :hasRelation
    source: Anne-Marie
  AddLiteral (67692c85-bdbe-40d0-bef2-263998c554ca)
 Call ID: 67692c85-bdbe-40d0-bef2-263998c554ca
  Args:
    literal_value: 1964
    literal_type: xsd:positiveInteger
    source: Anne-Marie
    relation: :hasMarriageYear
  AddLiteral (e4ffb0c0-b78a-4d4a-99b8-409a4700b439)
 Call ID: e4ffb0c0-b78a-4d4a-99b8-409a4700b439
  Args:
    literal_value: 1964
    relation: :hasMarriageYear
    literal_type: xsd:positiveInteger
    source: Constantine_II
  AssignClass (75349547-d042-4225-a5de-58d9947dff34)
 Call ID: 75349547-d042-4225-a5de-58d9947dff34
  Args:
    source: Margrethe_II
    type: :Woman
  AssignClass (3eab1253-1185-405f-8124-0e6b56d9b7b8)
 Call ID: 3eab1253-1185-405f-8124-0e6b56d9b7b8
  Args:
    source: Margrethe_II
    type: :Person
  AddTriple (083a8cac-3fd8-4763-b2f7-b9992da79846)
 Call ID: 083a8cac-3fd8-4763-b2f7-b9992da79846
  Args:
    target: Margrethe_II
    source: Anne-Marie
    relation: :isSisterOf
  AssignClass (bdeb54e2-e243-4e0c-945e-2c983d5f6e60)
 Call ID: bdeb54e2-e243-4e0c-945e-2c983d5f6e60
  Args:
    type: :Woman
    source: Benedikte
  AssignClass (b91b8904-3a59-4422-a092-0bbc098b5637)
 Call ID: b91b8904-3a59-4422-a092-0bbc098b5637
  Args:
    type: :Person
    source: Benedikte
  AddTriple (fc94cfd0-f0b6-4e19-8a10-7bb384754b9f)
 Call ID: fc94cfd0-f0b6-4e19-8a10-7bb384754b9f
  Args:
    source: Anne-Marie
    relation: :isSisterOf
    target: Benedikte
  AssignClass (ad92e19b-1784-416a-b882-a340c948306e)
 Call ID: ad92e19b-1784-416a-b882-a340c948306e
  Args:
    source: Christian_X
    type: :Man
  AssignClass (d6e69858-179c-498d-b2bd-f2b2d3127e03)
 Call ID: d6e69858-179c-498d-b2bd-f2b2d3127e03
  Args:
    source: Christian_X
    type: :Person
  AssignClass (75ce0644-3b2c-4668-b5ca-799e45af53f3)
 Call ID: 75ce0644-3b2c-4668-b5ca-799e45af53f3
  Args:
    source: Alexandrine_of_Mecklenburg-Schwerin
    type: :Woman
  AssignClass (fa63250d-00b2-4507-abd5-ecbec755d31b)
 Call ID: fa63250d-00b2-4507-abd5-ecbec755d31b
  Args:
    source: Alexandrine_of_Mecklenburg-Schwerin
    type: :Person
  AddTriple (b18b2e7a-f222-4646-886c-a11cd056a12a)
 Call ID: b18b2e7a-f222-4646-886c-a11cd056a12a
  Args:
    relation: :hasFather
    source: Frederik_IX
    target: Christian_X
  AddTriple (6658af03-1add-49eb-916f-034184ff4b97)
 Call ID: 6658af03-1add-49eb-916f-034184ff4b97
  Args:
    relation: :hasMother
    source: Frederik_IX
    target: Alexandrine_of_Mecklenburg-Schwerin
  AssignClass (9a45a0f8-b84f-4153-9f81-daf51507dae6)
 Call ID: 9a45a0f8-b84f-4153-9f81-daf51507dae6
  Args:
    type: :Man
    source: Gustaf_VI_Adolf
  AssignClass (9eec15df-d4fa-41ea-b654-76b4932c3a78)
 Call ID: 9eec15df-d4fa-41ea-b654-76b4932c3a78
  Args:
    type: :Person
    source: Gustaf_VI_Adolf
  AssignClass (75508e44-e238-4d59-8410-e4fd7cf0a7df)
 Call ID: 75508e44-e238-4d59-8410-e4fd7cf0a7df
  Args:
    type: :Woman
    source: Margaret_of_Connaught
  AssignClass (909ba2a7-fc08-427d-a80e-2e8d5068e4a0)
 Call ID: 909ba2a7-fc08-427d-a80e-2e8d5068e4a0
  Args:
    type: :Person
    source: Margaret_of_Connaught
  AddTriple (5d44c8ad-a3ec-4c77-9337-a66f95ff9c12)
 Call ID: 5d44c8ad-a3ec-4c77-9337-a66f95ff9c12
  Args:
    target: Gustaf_VI_Adolf
    relation: :hasFather
    source: Ingrid_of_Sweden
  AddTriple (80cbdf85-f898-45c5-8ced-7e1f61814bef)
 Call ID: 80cbdf85-f898-45c5-8ced-7e1f61814bef
  Args:
    source: Ingrid_of_Sweden
    relation: :hasMother
    target: Margaret_of_Connaught
  AssignClass (e239bc97-f425-42b2-9c7c-9e328ac2f6d3)
 Call ID: e239bc97-f425-42b2-9c7c-9e328ac2f6d3
  Args:
    type: :Woman
    source: Alexia
  AssignClass (65790861-cd39-40c3-b5bd-85b96ad7b22f)
 Call ID: 65790861-cd39-40c3-b5bd-85b96ad7b22f
  Args:
    type: :Person
    source: Alexia
  AssignClass (5fd9b4d2-0c2e-4ddf-b9e4-3be98d8651e2)
 Call ID: 5fd9b4d2-0c2e-4ddf-b9e4-3be98d8651e2
  Args:
    type: :Man
    source: Pavlos
  AssignClass (ca577941-2809-4e17-87ae-84ec87551b88)
 Call ID: ca577941-2809-4e17-87ae-84ec87551b88
  Args:
    type: :Person
    source: Pavlos
  AssignClass (365e4a6f-4f92-49b2-a4d7-932d102f4854)
 Call ID: 365e4a6f-4f92-49b2-a4d7-932d102f4854
  Args:
    source: Nikolaos
    type: :Man
  AssignClass (3ec48196-cbc2-4017-9c4e-8b38e331b635)
 Call ID: 3ec48196-cbc2-4017-9c4e-8b38e331b635
  Args:
    source: Nikolaos
    type: :Person
  AssignClass (a7df2ae6-fdee-4144-bd7b-cb3976d7824b)
 Call ID: a7df2ae6-fdee-4144-bd7b-cb3976d7824b
  Args:
    source: Theodora
    type: :Woman
  AssignClass (7e5101c5-8a65-4c16-9217-6b16c33508bf)
 Call ID: 7e5101c5-8a65-4c16-9217-6b16c33508bf
  Args:
    source: Theodora
    type: :Person
  AssignClass (f15933c4-d04d-4e5f-b80f-c26b4e160a14)
 Call ID: f15933c4-d04d-4e5f-b80f-c26b4e160a14
  Args:
    type: :Man
    source: Philippos
  AssignClass (84e8e5ca-1228-42e2-9e35-8fa23edc6e37)
 Call ID: 84e8e5ca-1228-42e2-9e35-8fa23edc6e37
  Args:
    type: :Person
    source: Philippos
  AddTriple (f2d8f10f-09e6-47a0-a987-b416b36f0700)
 Call ID: f2d8f10f-09e6-47a0-a987-b416b36f0700
  Args:
    target: Alexia
    relation: :isMotherOf
    source: Anne-Marie
  AddTriple (cafb5d3a-5f68-43aa-b842-fb905f1d82eb)
 Call ID: cafb5d3a-5f68-43aa-b842-fb905f1d82eb
  Args:
    source: Anne-Marie
    relation: :isMotherOf
    target: Pavlos
  AddTriple (fb394f79-37c8-4e33-beee-a1e1185cf1f5)
 Call ID: fb394f79-37c8-4e33-beee-a1e1185cf1f5
  Args:
    target: Nikolaos
    source: Anne-Marie
    relation: :isMotherOf
  AddTriple (c3746139-dfd9-4c04-9ee4-bafab513aaeb)
 Call ID: c3746139-dfd9-4c04-9ee4-bafab513aaeb
  Args:
    target: Theodora
    relation: :isMotherOf
    source: Anne-Marie
  AddTriple (1528427f-781a-44d5-b47f-4dec167b214a)
 Call ID: 1528427f-781a-44d5-b47f-4dec167b214a
  Args:
    source: Anne-Marie
    relation: :isMotherOf
    target: Philippos
  AddTriple (2e7d3763-5700-4120-be2f-db591636966a)
 Call ID: 2e7d3763-5700-4120-be2f-db591636966a
  Args:
    source: Constantine_II
    relation: :isFatherOf
    target: Alexia
  AddTriple (5023c673-779e-4356-8d59-4dc85adae07c)
 Call ID: 5023c673-779e-4356-8d59-4dc85adae07c
  Args:
    source: Constantine_II
    relation: :isFatherOf
    target: Pavlos
  AddTriple (6c3b3915-ad20-490e-a527-72845ef0d367)
 Call ID: 6c3b3915-ad20-490e-a527-72845ef0d367
  Args:
    relation: :isFatherOf
    source: Constantine_II
    target: Nikolaos
  AddTriple (fe833d9c-ed20-4ec2-a481-540156ab3759)
 Call ID: fe833d9c-ed20-4ec2-a481-540156ab3759
  Args:
    relation: :isFatherOf
    source: Constantine_II
    target: Theodora
  AddTriple (0e7f402d-e46e-4095-9ae2-d590314f5f0e)
 Call ID: 0e7f402d-e46e-4095-9ae2-d590314f5f0e
  Args:
    relation: :isFatherOf
    source: Constantine_II
    target: Philippos
  AssignClass (c3fe594d-ce7d-4478-a77e-1771b486b36b)
 Call ID: c3fe594d-ce7d-4478-a77e-1771b486b36b
  Args:
    type: :Man
    source: Paul_of_Greece
  AssignClass (7d506d35-2622-4dec-8957-6ca82aa8d4e7)
 Call ID: 7d506d35-2622-4dec-8957-6ca82aa8d4e7
  Args:
    type: :Person
    source: Paul_of_Greece
  AssignClass (55a02dd5-60e0-4f57-9cfc-316972522c4e)
 Call ID: 55a02dd5-60e0-4f57-9cfc-316972522c4e
  Args:
    type: :Woman
    source: Frederica_of_Greece
  AssignClass (2f2a82f9-1bcb-401f-bfd1-c0020ca2fb77)
 Call ID: 2f2a82f9-1bcb-401f-bfd1-c0020ca2fb77
  Args:
    source: Frederica_of_Greece
    type: :Person
  AddTriple (cade9286-8535-46cc-87ec-b9289d5e87e4)
 Call ID: cade9286-8535-46cc-87ec-b9289d5e87e4
  Args:
    target: Paul_of_Greece
    relation: :hasFather
    source: Constantine_II
  AddTriple (e10a9a51-0e53-413e-86ba-dd53d9b9492b)
 Call ID: e10a9a51-0e53-413e-86ba-dd53d9b9492b
  Args:
    target: Frederica_of_Greece
    relation: :hasMother
    source: Constantine_II
  AssignClass (8a409227-2f09-4a33-9d3a-c9c65ce6716f)
 Call ID: 8a409227-2f09-4a33-9d3a-c9c65ce6716f
  Args:
    type: :Woman
    source: Sophia_of_Greece
  AssignClass (2c7a8801-49b0-4518-a631-8f0e72e5e280)
 Call ID: 2c7a8801-49b0-4518-a631-8f0e72e5e280
  Args:
    source: Sophia_of_Greece
    type: :Person
  AddTriple (e9efb245-312c-4700-afd2-7ac8a1a76754)
 Call ID: e9efb245-312c-4700-afd2-7ac8a1a76754
  Args:
    target: Sophia_of_Greece
    relation: :isSisterOf
    source: Constantine_II
  AssignClass (ba925b66-53fd-4ad2-a1cd-56b2e0730bba)
 Call ID: ba925b66-53fd-4ad2-a1cd-56b2e0730bba
  Args:
    type: :Man
    source: Juan_Carlos_of_Spain
  AssignClass (3f97c00b-ef97-49ae-a0ef-569b72fdbd01)
 Call ID: 3f97c00b-ef97-49ae-a0ef-569b72fdbd01
  Args:
    type: :Person
    source: Juan_Carlos_of_Spain
  AddTriple (8bdeab14-8a40-4583-a364-6a6b836b21f2)
 Call ID: 8bdeab14-8a40-4583-a364-6a6b836b21f2
  Args:
    target: Juan_Carlos_of_Spain
    relation: :hasRelation
    source: Sophia_of_Greece
  AssignClass (5b79184f-4994-430a-82da-acc96b41ebc6)
 Call ID: 5b79184f-4994-430a-82da-acc96b41ebc6
  Args:
    type: :Woman
    source: Irene_of_Greece
  AssignClass (8c401274-1063-4efd-855a-7b16921be4eb)
 Call ID: 8c401274-1063-4efd-855a-7b16921be4eb
  Args:
    type: :Person
    source: Irene_of_Greece
  AssignClass (6ac85975-ef64-41fd-9e5b-513162d4b1a4)
 Call ID: 6ac85975-ef64-41fd-9e5b-513162d4b1a4
  Args:
    type: :Woman
    source: Katherine_of_Greece
  AssignClass (a919720f-5b44-44ad-9166-00059c1e5128)
 Call ID: a919720f-5b44-44ad-9166-00059c1e5128
  Args:
    source: Katherine_of_Greece
    type: :Person
  AssignClass (9180b6c4-6959-46b6-837d-ec39545b626d)
 Call ID: 9180b6c4-6959-46b6-837d-ec39545b626d
  Args:
    source: Frederik_X
    type: :Man
  AssignClass (1644a03a-8574-4ad9-99b6-2aa61aa98600)
 Call ID: 1644a03a-8574-4ad9-99b6-2aa61aa98600
  Args:
    type: :Person
    source: Frederik_X
  AddTriple (2b0283f0-fb2f-43a9-8739-cc9c0724b962)
 Call ID: 2b0283f0-fb2f-43a9-8739-cc9c0724b962
  Args:
    relation: :isAuntOf
    source: Anne-Marie
    target: Frederik_X
  AssignClass (32ff22c8-c94d-4cda-bf47-54822ddc8b63)
 Call ID: 32ff22c8-c94d-4cda-bf47-54822ddc8b63
  Args:
    source: Carl_XVI_Gustaf
    type: :Man
  AssignClass (99631d05-2c9d-451a-9b87-7a274b232bd9)
 Call ID: 99631d05-2c9d-451a-9b87-7a274b232bd9
  Args:
    source: Carl_XVI_Gustaf
    type: :Person
  AddTriple (e84d3acc-a8f5-4ee4-8695-854a0aa433a2)
 Call ID: e84d3acc-a8f5-4ee4-8695-854a0aa433a2
  Args:
    relation: :isBloodrelationOf
    source: Anne-Marie
    target: Carl_XVI_Gustaf
  AssignClass (663b4f86-c765-46bc-b2c4-0288a08a8c4b)
 Call ID: 663b4f86-c765-46bc-b2c4-0288a08a8c4b
  Args:
    type: :Man
    source: Felipe_VI_of_Spain
  AssignClass (c9e1b72d-cce9-45ae-b976-0e720f48ac72)
 Call ID: c9e1b72d-cce9-45ae-b976-0e720f48ac72
  Args:
    source: Felipe_VI_of_Spain
    type: :Person
  AddTriple (45cbbeab-8c7c-4e4c-9381-9bb95e53bf25)
 Call ID: 45cbbeab-8c7c-4e4c-9381-9bb95e53bf25
  Args:
    target: Felipe_VI_of_Spain
    source: Anne-Marie
    relation: :isAuntOf
  AssignClass (ab6d9791-6049-4e27-9a57-009eb15ee913)
 Call ID: ab6d9791-6049-4e27-9a57-009eb15ee913
  Args:
    type: :Woman
    source: Marie-Chantal_Miller
  AssignClass (b06ef99f-58a1-4b0d-a160-9e3e9d996c8c)
 Call ID: b06ef99f-58a1-4b0d-a160-9e3e9d996c8c
  Args:
    source: Marie-Chantal_Miller
    type: :Person
  AddTriple (e43807d5-44c7-4535-b6a3-61e78fd7fa23)
 Call ID: e43807d5-44c7-4535-b6a3-61e78fd7fa23
  Args:
    target: Marie-Chantal_Miller
    source: Pavlos
    relation: :hasRelation
  Finish (68dbd35f-7859-4e39-a302-7cdeb5bb8fce)
 Call ID: 68dbd35f-7859-4e39-a302-7cdeb5bb8fce
  Args: