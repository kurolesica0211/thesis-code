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
Princess Cecilie of Greece and Denmark (Greek: Καικιλία, romanized: Kaikilía; 22 June 1911 – 16 November 1937) was by birth a Greek and Danish princess who became titular Hereditary Grand Duchess of Hesse and by Rhine through her marriage to Prince Georg Donatus, pretender to the throne of the Grand Duchy of Hesse.
She was also the third-eldest sister to Prince Philip of Greece and Denmark (later Duke of Edinburgh).
The third of five children of Prince Andrew of Greece and Denmark and Princess Alice of Battenberg, Cecilie had a happy childhood.
For the young princess and her relatives, these conflicts had dramatic consequences and led to their exile in Switzerland (between 1917 and 1920), and then in France (from 1922 to 1936).
During their exile, Cecilie and her family depended on the generosity of their foreign relatives, in particular Marie Bonaparte (who offered them accommodation in Saint-Cloud) and Lady Louis Mountbatten (who supported them financially).
The year 1929 was a turning point in Cecilie's life.
She formed a relationship with her maternal cousin, Georg Donatus, Hereditary Grand Duke of Hesse.
After marrying Georg Donatus in 1931, Cecilie moved to Darmstadt.
Soon after, the princess and her family (except for Johanna who stayed behind),  embarked on a trip to the United Kingdom, where they were to attend the wedding of her brother-in-law Louis, Prince of Hesse and by Rhine, to Margaret Campbell Geddes.
Repatriated to Darmstadt, their remains were buried in the Grand Ducal new mausoleum of Rosenhöhe Park on 23 November 1937.
Biography

Childhood

The Balkan Wars and the First World War

The third daughter of Prince Andrew of Greece and Denmark and Princess Alice of Battenberg, Cecilie was born at Tatoi Palace, near Athens, on 22 June 1911.
Baptised on 10 July, her godparents were King George V of the United Kingdom, Ernest Louis, Grand Duke of Hesse, Prince Nicholas of Greece and Denmark and Grand Duchess Vera Konstantinovna of Russia.
Cecilie spent a happy childhood within a united household that was already made up of two daughters, Margarita (1905–1981) and Theodora (1906–1969), and was further expanded with the arrival of Sophie (1914–2001).
Coming from a cosmopolitan dynasty, Cecilie and her sisters communicated in English with their mother, but they also used French, German, and Greek with their relatives and their governesses.
In 1911 and 1913, Cecilie thus went to the United Kingdom and Germany, where she was introduced to her mother's relatives.
Cecilie's early years were marked by the instability that the Kingdom of Greece experienced at the start of the twentieth century.
Between 1912 and 1913, Greece engaged in the Balkan Wars, during which Prince Andrew served under Crown Prince Constantine while Princess Alice worked as a nurse for wounded soldiers.
They were, however, especially affected by the First World War, which created division between different branches of their family as Greece set aside its neutrality due to the Triple Entente.
Cecilie and her sisters were in the royal palace of Athens when it was bombarded by the French Navy during the battle in the capital on 1 December 1916.
Exile in Switzerland

In June 1917, King Constantine I was finally deposed and driven out of Greece by the Allies, who replaced him on the throne by his second son, the young Alexander.
Fifteen days later, Cecilie's family was in turn forced into exile in order to remove the possibility of the new monarch being influenced by those close to him.
Following the Russian Revolution in 1917, some of Cecilie's Romanov relatives were murdered in Russia.
Shortly after these events, the Grand Ducal family of Hesse, to which Cecilie was closely related through her mother, was overthrown along with all the other German dynasties during the winter of 1918–1919.
Finally, the family went through some health problems, with Cecilie contracting the flu and scarlet fever in 1920.
At the beginning of 1919, Cecilie reunited with her paternal grandmother, the Dowager Queen Olga, spared by the Bolsheviks thanks to the diplomatic intervention of the Danes.
In the months that followed, Cecilie attended a family reunion with her maternal grandparents, and met her aunt Louise and uncle Louis Mountbatten.
For Cecilie, who now formed a duo with her younger sister Sophie, exile was not only synonymous with sadness; it was also an opportunity for long family reunions and walks in the mountains.
Brief return to Greece

On 2 October 1920, King Alexander, cousin of Cecilie, was bitten by a domestic monkey during a walk in Tatoi.
The death of the sovereign caused a violent institutional crisis in Greece.
Humiliated, he retired abroad while a referendum reinstalled Constantine I on the throne.
Prince Andrew was received triumphantly in Athens on 23 November 1920, and his wife and four daughters joined him a few days later.
Cecilie then returned to live in Corfu with her family.
At the same time, Princess Alice found out that she was pregnant again.
On 10 June 1921, the family welcomed Philip (1921–2021), later the Duke of Edinburgh.
The joy that surrounded this birth, however, was obscured by the absence of Prince Andrew, who joined the Greek forces in Asia Minor during the Occupation of Smyrna.
Despite worries about the war, Cecilie and her siblings enjoyed life at Mon Repos, where they received a visit from their maternal grandmother and their aunt Louise in the spring of 1922.
In the park near the palace, built on an ancient cemetery, the princesses devoted themselves to archeology and discovered some pottery, bronze pieces and bones.
During this period, Cecilie and her sisters also participated, for the first time, in a number of great social events.
In March 1921, the princesses attended in Athens the wedding of their cousin Helen to Crown Prince Carol of Romania.
In July 1922, they went to the United Kingdom to be bridesmaids at the wedding of their uncle Louis Mountbatten to the wealthy heiress Edwina Ashley, whose beauty fascinated Cecilie.
However, the military defeat of Greece against Turkey and the political unrest that it caused disrupted the life of Cecilie and her family.
In September 1922, Constantine I abdicated in favor of his eldest son, George II.
A month later, Prince Andrew was arrested before being tried by a military tribunal, which declared him responsible for the defeat of the Sakarya.
Saved from execution by the intervention of foreign chancelleries, the prince was condemned to banishment and cashiering.
The prince and his relatives hurriedly left Greece aboard HMS Calypso in early December 1922.
Teenage years and young adulthood

In the UK and France

After a journey of several weeks, which led them successively to Italy, France and the United Kingdom, Cecilie, her parents and her siblings settled in Saint-Cloud in 1923.
Settled in a house adjoining that of Princess Marie Bonaparte, the family depended for seven years on her generosity, and two other aunts of Cecilie: first Princess Anastasia and then Lady Louis Mountbatten.
Marie Bonaparte financed the studies of her nieces and nephew, while Lady Mountbatten got into the habit of offering her nieces her "used" clothes.
In fact, Cecilie's parents had little income and the children were the regular witnesses to their money problems and their difficulty in maintaining a household.
Deprived of their Greek nationality after the proclamation of the Second Hellenic Republic in March 1924, Cecilie and her family received Danish passports from their cousin King Christian X. In Saint-Cloud, the small group spent a relatively simple life.
Cecilie and her siblings continued their studies in private institutions, and, during their free time, their father took them regularly to Paris or to the Bois de Boulogne.
Every Sunday, the family was received for lunch by Princess Marie Bonaparte and Prince George of Greece and Denmark.
Cecilie and her family also regularly met Prince Nicholas of Greece and Denmark and his wife Elena Vladimirovna of Russia, who had also chosen France to spend their time in exile with their daughters.
Finally, they often saw their cousin Princess Margaret of Denmark, who settled in the Paris region after her marriage to Prince René of Bourbon-Parma.
Cecilie and her relatives made frequent stays abroad, and in particular in the United Kingdom.
In 1923, the princess was invited to London to be a bridesmaid at the wedding of her aunt Louise Mountbatten to the future Gustav VI Adolf of Sweden.
Engagement and family difficulties

Considered by her maternal grandmother, the Dowager Marchioness of Milford Haven, as the prettiest of the four daughters of Andrew and Alice, Cecilie made her debut in the United Kingdom, during the summer of 1928.
Aged 17, she took part in her first ball at the Earl and Countess of Ellesmere's Bridgewater House, before attending the Cowes Week and then being invited by King George V to stay a few days in Balmoral, Scotland.
Although her two elder sisters were still single, and the relative poverty of her parents was not unrelated to this situation, Cecilie's family did not give up on finding a good match for her.
Now Crown Princess of Sweden, her aunt Louise was planning to betroth her to Crown Prince Frederik of Denmark, but the plan did not succeed.
Since her childhood, Cecilie had in fact been in contact with her cousins, Princes Georg Donatus and Louis of Hesse, whom she first met in 1919, while she was living in exile in Switzerland.
The relationship between the princess and Georg Donatus turned into a romance during the year 1929 and the two were unofficially engaged in early 1930.
At that time, Cecilie was just 18 years old and Georg Donatus, the pretender to the throne of Hesse, was 23.
The happiness of the princess was however clouded by the situation of her mother, whose mental health deteriorated sharply after the celebration of her silver wedding anniversary with Prince Andrew, in 1928.
Struck by a mental health crisis, the princess convinced herself that she possessed healing powers and that she was receiving divine messages about potential husbands for her daughters.
Distraught by the situation, Prince Andrew finally made the decision to place his wife in a sanatorium.
He took advantage of his family's stay in Darmstadt, on the occasion of the celebration for Cecilie's official engagement in April 1930, to send Alice to a psychiatric hospital located in Kreuzlingen, Switzerland.
Marriage and settling in Germany

Wedding

With her sister Sophie having become engaged almost at the same time as her to another member of the House of Hesse, Prince Christoph of Hesse, Cecilie made the preparations for her wedding in the company of her younger sister, aged 16.
The nuptials of Sophie and Christoph were celebrated at Schlosshotel Kronberg in Kronberg im
The wedding of Cecilie and Georg Donatus took place at the Neue Palais in Darmstadt on 2 February 1931.
To the surprise of the foreign guests, who expected a much colder welcome from a population that had dethroned Grand Duke Ernest Louis in 1918, the wedding aroused the enthusiasm of the people, who gathered in droves to attend the event and cheer their former princely family.
The ceremony brought together some fifty guests from all over Europe, but took place in the absence of the bride's mother Princess Alice, who was still hospitalized in Switzerland.
Motherhood and reconnecting with Alice

After their marriage, Cecilie and Georg Donatus moved to Schloß Wolfsgarten, the main residence of Grand Duke Ernest Louis and his wife Grand Duchess Eleonore, since their deposition.
In Hesse, the young couple led a relatively simple life, punctuated by frequent stays abroad.
Cecilie was involved in several charitable organizations and became the head of Alice Frauen Verein, an association dedicated to women.
She also quickly gave birth to three children: Prince Ludwig (born 25 October 1931), Prince Alexander (born 14 April 1933) and Princess Johanna of Hesse (born 20 September 1936).
Very close to her family, Cecilie was concerned about the situation of her mother, who remained institutionalized until the beginning of 1933.
During this period, the relationship between Alice and her children became complicated.
Cecilie maintained correspondence with her mother, and visited her once in Kreuzlingen.
However, Alice was angry with those close to her for having her institutionalized and her anger manifested itself in fits of rage, which pushed her, for example, to tear up the photograph that Cecilie sent her after the birth of her first child.
Once released from the hospital, Alice made known her desire to stay away from her family and four years passed before she put an end to her voluntary exile.
During this period, Cecilie continued, despite everything, to write to her and to send her photos of the family.
In December 1936, Alice finally made the decision to reconnect with her family, and it was Cecilie that she got closer to first.
Association with the Nazi Party and restoration of the monarchy in Greece

Prince Christoph of Hesse, Cecilie's brother-in-law, joined the Nazi Party in 1931 and the SS in 1932.
For their part, the princes of Hesse kept their distance from the far-right party for a long time because the Grand Duke Ernest Louis had no sympathy for the Führer's ideas.
On that date, Georg Donatus and Louis, the two sons of the former sovereign, joined the Nazi Party.
Following the example of her husband and her brother-in-law, Cecilie joined the party at the same time.
While in Germany the establishment of the Nazi regime prevented any plans to restore the monarchy, in Greece the republic collapsed after the putsch of General Georgios Kondylis in November 1935.
Reinstalled on the throne by a referendum, George II then lifted the banishment sentence issued against Cecilie's father in 1922.
In November 1936, the King of the Hellenes also organized the return of the remains and ashes of members of the Greek royal family who died in exile.
This event was the opportunity for Cecilie and her family to return, for the first time, to Greece after fourteen years of banishment.
Titular Grand Duchess of Hesse and by Rhine

In 1937, Cecilie became pregnant again.
At the same time, the health of her father-in-law, Grand Duke Ernest Louis, deteriorated sharply.
Suffering from lung cancer, the former ruler hoped to live long enough to attend the wedding of his second son, Louis, to Hon.
Margaret Campbell Geddes, scheduled to take place in London on 23 October 1937.
However, the Grand Duke died a fortnight before the ceremony, on 9 October, making Georg Donatus the new head of House of Hesse-Darmstadt.
Under these circumstances, the marriage of Prince Louis was postponed to 20 November, in order to give his family time to organize the funeral of Ernest Louis, which took place on 12 October.
Death

With Prince Louis' wedding approaching, Cecilie and her family went to Frankfurt on 16 November 1937 to board a plane of the Belgian company Sabena which was to take them to London, via a stopover in Ostend where it was planned to pick up two other passengers.
The small group, which consisted of Cecilie (eight months pregnant), Georg Donatus, their two sons Ludwig (aged 6) and Alexander (aged 4) and the Dowager Grand Duchess Eleonore, was accompanied by Baron Joachim von Riedesel, chosen by Louis to be his witness, and Alice Hahn.
According to biographer Philip Eade, Cecilie hated taking the plane and she always dressed in black when she made a trip like this.
However, during the maneuver, the aircraft struck the chimney of a factory, causing the destruction of a wing and an engine of the aircraft.
The accident caused the immediate death of all passengers, including a newborn baby whom Cecilie seemed to have given birth to during the flight.
Funeral

Despite the death of his family, Prince Louis married Margaret Campbell Geddes, in London, the day after the plane crash.
After the wedding, which took place in a climate of extreme gloom, the couple went to Belgium to collect the remains of Cecilie and her family, kept until then at the civil hospital in Ostend.
Once back in Darmstadt, Louis and his wife adopted their niece, Johanna, the only child of Cecilie and Georg Donatus not to have taken part in the plane trip due to her very young age.
The funeral of Cecilie and her relatives took place in Darmstadt on 23 November 1937.
It was also an opportunity for Cecilie's parents to meet for the first time since 1931.
Reconciled by tragedy, Andrew and Alice nevertheless continued separate lives after the funeral.
The trauma of her daughter's death healed Alice, whose mental state returned to a completely normal level once the funeral was over.
After the ceremony, the remains of Cecilie and her family were buried in a family vault at the Grand Ducal mausoleum of Rosenhöhe, not far from the graves of her godfather and father-in-law Grand Duke Ernest Louis and his daughter Elisabeth.
In popular culture

Commemoration

On 16 November 2017 in Darmstadt, the Hessian State Archives, in collaboration with the Foundation of the House of Hesse (Hessische Hausstiftung), held a commemorative ceremony in honor of the victims of the accident in Ostend.
On this occasion, wreaths were placed on the vault of Cecilie and her family, in Rosenhöhe.
Documentaries

The plane crash that caused the death of Princess Cecilie and her family was recounted in the sixth episode of the documentary series Mémoires d'exil (1999) by Frédéric Mitterrand.
TV series

The death of Cecilie and her family is also mentioned by the character of Prince Philip, in the third episode ("Windsor") of the first season of the series The Crown (2016), and by a journalist, in the second episode ("A Company of Men") of the second season (2017).
It is also depicted in the ninth episode of season 2 ("Paterfamilias"), during a flashback to Philip's early years.
In this episode, Princess Cecilie is portrayed by German actress Leonie Benesch.
However, this fictionalised version wrongly implied that Philip was to blame for Cecilie taking the flight, whereas in reality "her decision to travel to London had nothing to do with Philip".
Novels

The death of Cecilie and her family is also recounted in the novel A Matter of Honor by Jeffrey Archer (1986).
In this fictionalized version, the accident in Ostend is caused by the KGB, which wants to recover the jewels of Tsarina Alexandra Fedorovna, bequeathed to the House of Hesse-Darmstadt after the Russian Revolution.
Ancestry

Notes and references

Notes

References

Bibliography

On Cecilie and her family

Biographies of Cecilie's relatives

Other works on royal families



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
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

:hasDeathYear a owl:AnnotationProperty .

:hasMarriageYear a owl:AnnotationProperty .

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

:hasChild a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:inverseOf :isChildOf .

:isAncestorOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation .

:isSiblingOf a owl:ObjectProperty,
        owl:SymmetricProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isBloodrelationOf ;
    owl:propertyChainAxiom ( :hasParent :isParentOf ) .

:isSisterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf .

:hasParent a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Person ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:equivalentProperty :isChildOf ;
    owl:inverseOf :isParentOf .

:Sex a owl:Class ;
    rdfs:subClassOf :DomainEntity ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Female :Male ) ] .

:isChildOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:propertyDisjointWith :isSisterOf .

:Man a owl:Class ;
    owl:disjointWith :Sex,
        :Woman ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Male ] ) ] .

:Woman a owl:Class ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Female ] ) ] .

:isParentOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:propertyDisjointWith :isSisterOf .

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



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (c4b190c5-bad1-4e3b-8d0b-0167df44bd9e)
 Call ID: c4b190c5-bad1-4e3b-8d0b-0167df44bd9e
  Args:
    type: :Woman
    source: :Cecilie_of_Greece_and_Denmark
  AssignClass (4eab3477-0a64-4b74-92f4-b4254305a2d2)
 Call ID: 4eab3477-0a64-4b74-92f4-b4254305a2d2
  Args:
    type: :Person
    source: :Cecilie_of_Greece_and_Denmark
  AddLiteral (25efb5e8-b78a-4711-a9cd-91716f2d1a8b)
 Call ID: 25efb5e8-b78a-4711-a9cd-91716f2d1a8b
  Args:
    literal_type: xsd:integer
    literal_value: 1911
    source: :Cecilie_of_Greece_and_Denmark
    relation: :hasBirthYear
  AddLiteral (408f475e-2acd-4570-8e9e-e49f5b97becf)
 Call ID: 408f475e-2acd-4570-8e9e-e49f5b97becf
  Args:
    literal_value: 1937
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: :Cecilie_of_Greece_and_Denmark
  AssignClass (ac775ce8-6cd0-49ea-9397-63af8687a5cc)
 Call ID: ac775ce8-6cd0-49ea-9397-63af8687a5cc
  Args:
    type: :Man
    source: :Prince_Andrew_of_Greece_and_Denmark
  AssignClass (f4535ec0-b86f-40b9-bb29-ec74e2ff45cf)
 Call ID: f4535ec0-b86f-40b9-bb29-ec74e2ff45cf
  Args:
    type: :Person
    source: :Prince_Andrew_of_Greece_and_Denmark
  AssignClass (5945ec80-78c5-4955-a1ee-1f2d9ee32cb6)
 Call ID: 5945ec80-78c5-4955-a1ee-1f2d9ee32cb6
  Args:
    type: :Woman
    source: :Princess_Alice_of_Battenberg
  AssignClass (3ead0096-f1d5-4346-9aa2-70045c37ed7a)
 Call ID: 3ead0096-f1d5-4346-9aa2-70045c37ed7a
  Args:
    type: :Person
    source: :Princess_Alice_of_Battenberg
  AddTriple (3257c43d-cc4d-486e-9157-cb9f78aa46d8)
 Call ID: 3257c43d-cc4d-486e-9157-cb9f78aa46d8
  Args:
    target: :Prince_Andrew_of_Greece_and_Denmark
    relation: :hasFather
    source: :Cecilie_of_Greece_and_Denmark
  AddTriple (ce89c4a4-43f9-4f88-b1be-5085208d1092)
 Call ID: ce89c4a4-43f9-4f88-b1be-5085208d1092
  Args:
    target: :Princess_Alice_of_Battenberg
    relation: :hasMother
    source: :Cecilie_of_Greece_and_Denmark
  AssignClass (dce9c851-6696-49f6-abfe-9a4ba38d1da2)
 Call ID: dce9c851-6696-49f6-abfe-9a4ba38d1da2
  Args:
    type: :Man
    source: :Prince_Georg_Donatus
  AssignClass (7d5bda6f-3d1c-41c8-973b-0efaad95ae48)
 Call ID: 7d5bda6f-3d1c-41c8-973b-0efaad95ae48
  Args:
    type: :Person
    source: :Prince_Georg_Donatus
  AddTriple (67798772-3b35-4d1c-81b6-0fd0f6e5869e)
 Call ID: 67798772-3b35-4d1c-81b6-0fd0f6e5869e
  Args:
    target: :Prince_Georg_Donatus
    relation: :hasRelation
    source: :Cecilie_of_Greece_and_Denmark
  AddLiteral (7f820a33-c892-4dfe-8928-1fddd33a5b9b)
 Call ID: 7f820a33-c892-4dfe-8928-1fddd33a5b9b
  Args:
    source: :Cecilie_of_Greece_and_Denmark
    relation: :hasMarriageYear
    literal_value: 1931
    literal_type: xsd:integer
  AssignClass (f16e3bbb-72cc-4b9d-b46d-fd805b0de774)
 Call ID: f16e3bbb-72cc-4b9d-b46d-fd805b0de774
  Args:
    type: :Man
    source: :Prince_Philip_of_Greece_and_Denmark
  AssignClass (0d1cfe35-9de0-4234-857b-6d6b27bd039b)
 Call ID: 0d1cfe35-9de0-4234-857b-6d6b27bd039b
  Args:
    type: :Person
    source: :Prince_Philip_of_Greece_and_Denmark
  AddTriple (18db9383-ce11-4966-b2c1-500c82eed82b)
 Call ID: 18db9383-ce11-4966-b2c1-500c82eed82b
  Args:
    relation: :isSiblingOf
    target: :Prince_Philip_of_Greece_and_Denmark
    source: :Cecilie_of_Greece_and_Denmark
  AssignClass (0d68638b-3a39-4522-860e-8c6c33c4c0ed)
 Call ID: 0d68638b-3a39-4522-860e-8c6c33c4c0ed
  Args:
    type: :Woman
    source: :Margarita
  AssignClass (9b308c3a-306b-4e3b-97f9-82facc20bcfd)
 Call ID: 9b308c3a-306b-4e3b-97f9-82facc20bcfd
  Args:
    type: :Person
    source: :Margarita
  AssignClass (0bbd947e-d4a7-4e38-b511-13016f71a168)
 Call ID: 0bbd947e-d4a7-4e38-b511-13016f71a168
  Args:
    type: :Woman
    source: :Theodora
  AssignClass (8cb0ef56-c5be-4d80-b0c2-43037a0ecc3d)
 Call ID: 8cb0ef56-c5be-4d80-b0c2-43037a0ecc3d
  Args:
    type: :Person
    source: :Theodora
  AssignClass (395d55a0-122a-4431-a856-93d1bab90d41)
 Call ID: 395d55a0-122a-4431-a856-93d1bab90d41
  Args:
    type: :Woman
    source: :Sophie
  AssignClass (59a5a50e-7ae6-428b-84f9-c73f37bf8bb3)
 Call ID: 59a5a50e-7ae6-428b-84f9-c73f37bf8bb3
  Args:
    type: :Person
    source: :Sophie
  AddTriple (b47b528c-953a-4fe3-aed9-886dabe31353)
 Call ID: b47b528c-953a-4fe3-aed9-886dabe31353
  Args:
    relation: :isSiblingOf
    target: :Margarita
    source: :Cecilie_of_Greece_and_Denmark
  AddTriple (66d029c8-1da1-41e6-850e-c1c7a265d3d2)
 Call ID: 66d029c8-1da1-41e6-850e-c1c7a265d3d2
  Args:
    source: :Cecilie_of_Greece_and_Denmark
    relation: :isSiblingOf
    target: :Theodora
  AddTriple (1f4e4e2f-9e45-4bec-ac1d-57f864b1b740)
 Call ID: 1f4e4e2f-9e45-4bec-ac1d-57f864b1b740
  Args:
    source: :Cecilie_of_Greece_and_Denmark
    target: :Sophie
    relation: :isSiblingOf
  AssignClass (1ce8e8ed-d499-4633-b2ba-a825e2a8f601)
 Call ID: 1ce8e8ed-d499-4633-b2ba-a825e2a8f601
  Args:
    type: :Man
    source: :Ludwig_of_Hesse
  AssignClass (3ac5eb0a-5870-41a4-a577-396578f92bf4)
 Call ID: 3ac5eb0a-5870-41a4-a577-396578f92bf4
  Args:
    type: :Person
    source: :Ludwig_of_Hesse
  AssignClass (ffbb3ad6-b5e2-4008-b248-3a2b182d3126)
 Call ID: ffbb3ad6-b5e2-4008-b248-3a2b182d3126
  Args:
    type: :Man
    source: :Alexander_of_Hesse
  AssignClass (487098ed-8412-4188-962e-0d51f8d7fcd0)
 Call ID: 487098ed-8412-4188-962e-0d51f8d7fcd0
  Args:
    type: :Person
    source: :Alexander_of_Hesse
  AssignClass (2a4ee3da-80b3-4c29-92f8-1d668b405339)
 Call ID: 2a4ee3da-80b3-4c29-92f8-1d668b405339
  Args:
    type: :Woman
    source: :Johanna_of_Hesse
  AssignClass (ad07179c-9fda-42cf-a021-86a08d813ef6)
 Call ID: ad07179c-9fda-42cf-a021-86a08d813ef6
  Args:
    type: :Person
    source: :Johanna_of_Hesse
  AddTriple (b1d21374-e7dc-47b1-8d25-d66612408848)
 Call ID: b1d21374-e7dc-47b1-8d25-d66612408848
  Args:
    relation: :hasSon
    target: :Ludwig_of_Hesse
    source: :Cecilie_of_Greece_and_Denmark
  AddTriple (7377b4ca-6368-485f-a79f-13d65e388cc1)
 Call ID: 7377b4ca-6368-485f-a79f-13d65e388cc1
  Args:
    source: :Cecilie_of_Greece_and_Denmark
    relation: :hasSon
    target: :Alexander_of_Hesse
  AddTriple (54638ee8-9b88-4323-bf77-5986d5bb3fcf)
 Call ID: 54638ee8-9b88-4323-bf77-5986d5bb3fcf
  Args:
    source: :Cecilie_of_Greece_and_Denmark
    target: :Johanna_of_Hesse
    relation: :hasDaughter
  Finish (acac3bdf-3d36-4981-a982-459efc0fd4e5)
 Call ID: acac3bdf-3d36-4981-a982-459efc0fd4e5
  Args: