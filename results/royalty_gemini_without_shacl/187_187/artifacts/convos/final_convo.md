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
Princess Theodora of Greece and Denmark (Greek: Θεοδώρα; 30 May 1906 – 16 October 1969) was a Greek and Danish princess by birth and Margravine of Baden through her marriage to Berthold, pretender to the throne of the Grand Duchy of Baden.
The second of five children of Prince Andrew of Greece and Denmark and Princess Alice of Battenberg, Theodora spent a happy childhood between Athens and Corfu.
For the young princess and her relatives, these conflicts had dramatic consequences and led to their exile in Switzerland (between 1917 and 1920), then in France and the United Kingdom (from 1922 to 1936).
During their exile, Theodora and her family depended on the generosity of their foreign relatives, in particular Marie Bonaparte (who offered them accommodation in Saint-Cloud) and Lady Louis Mountbatten (who supported them financially).
At the end of the 1920s, Theodora's mother was struck by a mental health crisis which led to her confinement in a Swiss psychiatric hospital.
Shortly after, in 1931, Theodora married Berthold, Margrave of Baden, son of Chancellor of the German Reich Prince Maximilian.
The princess gave birth to three children there: Margarita, Maximilian and Ludwig.
Opposed to Nazism, Theodora and her husband kept their distance from the Nazi regime; however, this did not prevent Berthold from enlisting in the Wehrmacht at the start of the Second World War.
Affected by the conflict, which divided her family into two factions, Theodora became involved in the German Red Cross and other charitable organizations.
The defeat of Germany and its occupation by the Allies brought new upheavals in the life of Theodora and Berthold.
Though not held by the Soviets, responsible for the death of several of their cousins, the couple was ostracized by the British royal family at the time of the marriage of Prince Philip, Theodora's only brother, to Princess Elizabeth of the United Kingdom (later Queen Elizabeth II) in 1947.
Over the years, the couple was nevertheless reintegrated into the life of the European elite, as illustrated by their invitation and presence at the coronation of Elizabeth II in 1953 and at the wedding of Juan Carlos, Prince of Asturias, and Princess Sophia of Greece and Denmark in 1962.
Theodora died of heart problems six years after her husband, in 1969.
She was the paternal aunt of the Prince of Wales, who later became King Charles III.
Biography

Childhood

In Greece and abroad

The second daughter of Prince Andrew of Greece and Denmark and Princess Alice of Battenberg, Theodora was born at Tatoi Palace, near Athens, on 30 May 1906.
At the time of her birth, her father was traveling to Spain, where he represented the Greek royal family on the occasion of the marriage of King Alfonso XIII of Spain to Princess Victoria Eugenie of Battenberg, a cousin of her mother Alice.
Baptised "Theodora" in honor of the Byzantine empress, but nicknamed "Dolla" by her family, the princess was raised within a united household, together with her elder sister Margarita, and younger sisters Cecilie, and Sophie.
With their mother, Theodora and her sisters communicated in English, but they also used French, German, and Greek in the presence of their relatives and governesses.
Theodora's early childhood was affected by the instability that the Kingdom of Greece experienced at the start of the twentieth century.
Tired of attacks from the press and the opposition, Andrew and Alice found refuge in travel and spent most of the period between 1907 and 1908 outside the borders of their country.
With their daughters, they stayed in the United Kingdom, Germany, Malta and Russia, where they reunited with their many relatives including Edward VII of the United Kingdom, Ernest Louis, Grand Duke of Hesse, Alexandra Feodorovna, and Prince and Princess Louis of Battenberg (Alice's parents).
At this time, Theodora was introduced to her young maternal uncle and aunt, Louis and Louise, to whom she and her sister Margarita later became very close.
In 1909, the Goudi coup occurred, a military putsch organized against the government of King George I of Greece, Theodora's grandfather.
Shortly after this event, Prince Andrew and his brothers were forced to resign from the army.
Concerned about the political situation of their country, Andrew and Alice once again found refuge abroad and stayed in the United Kingdom, France and Hesse.
After considering a life in exile for a while, the couple returned to live in Greece, where their third daughter was born.
At that time, Theodora was described by her maternal grandmother as a funny and imaginative little girl, but also very scatterbrained.
The Balkan Wars and the First World War

Between 1912 and 1913, Greece engaged in the Balkan Wars, which put the country in opposition to the Ottoman Empire and to Bulgaria.
Called to join the army again, Prince Andrew served under Crown Prince Constantine, while Princess Alice worked as a nurse for wounded soldiers.
Too young to follow their parents, Theodora and her sisters spent the duration of the conflict in Athens, with the exception of a brief stay in Thessaloniki in December 1912.
Greece came out of the Balkan Wars with an expanded territory, but the conflict also led to the assassination of George I in March 1913.
The death of the King of the Hellenes caused significant changes in the life of Theodora and her relatives.
In his will, the sovereign bequeathed the Corfiote palace of Mon Repos to Andrew.
After years of living in close proximity to the monarch, in the palaces of Athens and Tatoi, Andrew and his family therefore finally had their own residence.
When peace returned, Andrew, Alice and their daughters left Greece in August 1913.
After a visit to Germany, they stayed in the United Kingdom, with Theodora's maternal grandparents.
Returning to Greece on 17 November 1913, the family was then retained in the country by Alice's fourth pregnancy and, above all, by the outbreak of the First World War.
With Greece having proclaimed its neutrality, this new conflict initially hardly affected Theodora and her relatives.
Things changed as war entered into the life of the country's people.
Stationed in Thessaloniki with his garrison, Andrew was thus confronted with the occupation of the city by the Allies in October 1915.
Shortly after, in December, the routed Serbian army found refuge in Corfu, leading Alice and her daughters to abandon Mon Repos for the capital.
Over the months, the amount of threats against members of the royal dynasty increased.
In addition, on 1 December, the French navy bombarded the royal palace in Athens, forcing Theodora and her sisters to take refuge in the cellars with their mother.
Exile in Switzerland

In June 1917, King Constantine I was deposed and driven out of Greece by the Allies, who replaced him on the throne by his second son, the young Alexander.
Fifteen days later, Theodora's family was in turn forced into exile in order to remove the possibility of the new monarch being influenced by those close to him.
Following the Russian Revolution, several of Theodora's relatives (the Romanovs)  were executed in Russia.
Shortly after these events, the Grand Ducal family of Hesse, to which Theodora was closely related through her mother, was overthrown along with all the other German dynasties during the winter of 1918–1919.
At the beginning of 1919, Theodora nevertheless had the joy of reuniting with her paternal grandmother, the Dowager Queen Olga, spared by the Bolsheviks thanks to the diplomatic intervention of the Danes.
In the months that followed, she also reconnected with her maternal grandparents, whom the war had forced to abandon the name of Battenberg for that of Mountbatten.
For Theodora, who now formed a duo with her elder sister Margarita, exile was synonymous with sadness but also an opportunity for long family reunions and walks in the mountains.
Young adulthood

Brief return to Greece

On 2 October 1920, King Alexander, cousin of Theodora, was bitten by a domestic monkey during a walk in Tatoi.
The death of the sovereign caused a violent institutional crisis in Greece.
Humiliated, he retired abroad while a referendum reinstalled Constantine I on the throne.
Prince Andrew was received triumphantly in Athens on 23 November 1920, and his wife and four daughters joined him a few days later.
Theodora then returned to live in Corfu with her family.
At the same time, Princess Alice found out that she was pregnant again.
On 10 June 1921, the family welcomed Prince Philip of Greece and Denmark (later Prince Philip, Duke of Edinburgh, 1921–2021).
The joy that surrounded this birth, however, was obscured by the absence of Prince Andrew, who joined the Greek forces in Asia Minor during the Occupation of Smyrna.
Despite concerns about the war, Theodora and her siblings enjoyed life at Mon Repos, where they received a visit from their maternal grandmother and their aunt Louise in the spring of 1922.
In the park near the palace, built on an ancient cemetery, the princesses devoted themselves to archeology and discovered some pottery, bronze pieces and bones.
During this period, Theodora and her sisters also participated, for the first time, in a number of great social events.
In March 1921, the princesses attended in Athens the wedding of their cousin Helen to Crown Prince Carol of Romania.
In July 1922, they went to the United Kingdom to be bridesmaids at the wedding of their uncle Louis Mountbatten to the wealthy heiress Edwina Ashley.
However, the military defeat of Greece against Turkey and the political unrest that it caused disrupted the life of Theodora and her family.
In September 1922, Constantine I abdicated in favor of his eldest son, George II.
A month later, Prince Andrew was arrested before being tried by a military tribunal, which declared him responsible for the defeat of the Sakarya.
Saved from execution by the intervention of foreign chancelleries, the prince was condemned to banishment and cashiering.
After a brief stop in Corfu, the prince and his relatives hurriedly left Greece aboard HMS Calypso in early December 1922.
In the UK and France

After a journey of several weeks, which led them successively to Italy, France and the United Kingdom, Theodora, her parents and her siblings settled in Saint-Cloud in 1923.
Settled in a house adjoining the home of Princess Marie Bonaparte, the family depended for seven years on her generosity, and two other aunts of Theodora: first Princess Anastasia and then Lady Louis Mountbatten.
Marie Bonaparte financed the studies of her nieces and nephew, while Lady Mountbatten got into the habit of offering her nieces her "used" clothes.
In fact, Theodora's parents had little income and the children were the regular witnesses to their money problems and their difficulty in maintaining a household.
Deprived of their Greek nationality after the proclamation of the Second Hellenic Republic in March 1924, Theodora and her family received Danish passports from their cousin King Christian X.
Now of marrying age, the princess and her sister Margarita regularly left France for the United Kingdom, where they lived with their maternal grandmother, the Dowager Marchioness of Milford Haven.
With their aunt Louise, who increasingly replaced their mother as a chaperone and confidante, the two young girls attended most of the events by British aristocracy during the 1920s, including balls and dances, birthdays and garden parties at Buckingham Palace, horse races, etc.
However, the young girls' lack of fortune and their life in exile meant that they hardly had any suitors.
This did not prevent them from rejoicing for their aunt Louise when she was asked by Gustaf Adolf, Crown Prince of Sweden, to marry him in June 1923.
Alice's confinement

Theodora, Margarita and Philip spent the summer of 1928 in Romania.
Invited by Princess Helen, whose son Michael I was the same age as Philip, the two young women and their brother stayed for several weeks in Sinaia.
At the time, Prince Nicholas of Romania was still single and Helen wanted to see him marry one of her relatives, but her plans for her brother-in-law to marry one of her cousins came to nothing.
A few months after this trip, Alice began to suffer from psychological problems.
Struck by a mental health crisis, the princess convinced herself that she possessed healing powers and that she was receiving divine messages about potential husbands for her daughters.
Distraught by the situation, Prince Andrew finally made the decision to place his wife in a sanatorium.
He took advantage of his family's stay in Darmstadt, Germany, in April 1930, to send Alice to a psychiatric hospital located in Kreuzlingen, Switzerland.
In the months which followed, Theodora's three sisters successively married German princes.
Sophie married Prince Christoph of Hesse in December 1930, followed by Cecilie who married Georg Donatus, Hereditary Grand Duke of Hesse in February 1931, and Margarita who married Gottfried, Hereditary Prince of Hohenlohe-Langenburg in April 1931.
Theodora thus became the last of the four sisters to get married.
Son of the last chancellor of the German Empire and titular Grand Duke of Baden from November 1929, Berthold was in charge of a substantial fortune.
On 17 August 1931, Theodora and Berthold married in a double religious ceremony, both Lutheran and Orthodox, at the Neues Schloss in Baden-Baden, which resulted in a large family reunion, at which the bride's mother, Princess Alice, was not present.
Concerned about her mother's fate, Theodora visited her several times in Kreuzlingen, but Alice did not always receive her daughter warmly.
Aware that her brother had been living a chaotic existence since their mother's placement in a sanatorium, Theodora got Philip to go to school in Salem and to come and live with her and her husband in 1933.
Over the years, Theodora welcomed several members of her family to Salem.
The Dowager Marchioness of Milford Haven stayed on several occasions with her granddaughter, as did Prince Andrew.
The princess also received her mother, once she had recovered from her health problems, and her sisters.
Political upheavals

While several of their relatives such as Cecilie and Margarita, (Theodora's sisters) as well as Marie Alexandra (Berthold's sister), gradually joined the Nazi Party, the Margrave and Margravine of Baden tried to keep their distance from the Nazi regime.
A month later, King George II, Theodora's cousin, was reinstalled on the throne after a referendum.
At the beginning of 1936, the banishment sentence issued in 1922 against Theodora's father Prince Andrew was lifted, which allowed him to stay in his country again.
A regular target for the Hellenic press, the prince however chose to stay abroad for most of the year.
Estranged from her husband since her confinement, Princess Alice made the choice to return and live in Athens, where she settled in November 1938.
In the meantime, Theodora also returned to Greece with Berthold on the occasion of the marriage of Crown Prince Paul to Princess Frederica of Hanover in January 1938.
Second World War and its aftermath

Enlisted in the Wehrmacht shortly after the outbreak of the Second World War, Theodora's husband was seriously injured in the leg during the Battle of France in 1940.
While Theodora engaged with the German Red Cross and other charitable organizations, Berthold took part in riskier actions, by attempting to hide Jews in his castle.
Affected by the occupation of Greece by the Nazis, Theodora was cut off from a large part of her family because of the conflict.
Her father, Prince Andrew, found himself isolated on the French Riviera and contacting him became very difficult.
As for her mother, she spent the war in Athens, but managed to pay a few visits to her daughters in 1940, 1942, and 1944 Added to this was the anguish of knowing her brothers-in-law Christoph and Gottfried and her brother Philip were fighting in opposite camps.
The war brought its share of tragedies for Theodora and her relatives.
In October 1943, her sister Sophie's husband died in a plane crash while flying over the Apennine Mountains.
Finally, in December 1944, her father Prince Andrew died in Monaco without having been able to see his children again.
These events greatly affected Theodora, who then went through a period of depression.
Post-war years

Occupation of Germany and Philip's marriage

The defeat of Germany and its occupation by the Allies brought new upheavals in the life of the former German princely families, several of whom (such as Hermine Reuss of Greiz, Joachim Ernst, Duke of Anhalt, or Georg, Prince of Saxe-Meiningen) perished in hands of the Soviets.
Baden was placed under the administration of France and the United States, however, Berthold and Theodora were not under threat, and it did not take long for the margrave to find a leading social role.
Berthold was thus able to reopen the Salem School, which he entrusted to his cousin, Prince George William of Hanover, in 1948.
Two years earlier, the latter had married Theodora's sister Sophie (widowed since 1943), and the couple's move to Salem allowed Theodora to maintain close ties with her sister.
Theodora's relationship with her brother Philip was, on the other hand, more complicated.
Since 1939, he had been linked to Princess Elizabeth of the United Kingdom, and the two's engagement was officially announced on 10 July 1947.
However, the ties of Philip's family to Germany frightened the British court and government, who feared that the public could be reminded of the Germanic origins of the House of Windsor if the royal family were publicly associated with former Nazi Party members.
Prince Philip found himself unable to invite his sisters to his wedding.
Aware of the difficulties their brother had to face, Theodora, Margarita and Sophie considered their sidelining wrong and hurtful.
Harassed by the press, who submitted requests for interviews with them, Theodora and her sisters spent the day of 20 November 1947 at Marienburg Castle with their families.
Invited by the Duke and Duchess of Brunswick, they celebrated the union of their brother in the company of their cousin Princess Elizabeth of Greece and Denmark and Prince Louis and Princess Margaret of Hesse and by Rhine.
A few days later, the Greek princesses received a visit from the Queen of the Hellenes (who came to bring them a letter from their mother Princess Alice describing the wedding in detail) and the Duchess of Kent.
Reintegration into royal circles

Once the monarchy was restored in Greece in 1946, Theodora and her husband were regularly invited to Athens.
Theodora and her family were also invited to Athens on the occasion of the marriage of Princess Sophia of Greece and Denmark and Juan Carlos, Prince of Asturias in 1962, and the marriage of King Constantine II and Princess Anne-Marie of Denmark in 1964.
In the early 1950s, relations between the British royal family and their German relatives in turn normalized.
Theodora, her sisters, their husbands and some of their children were thus invited to the coronation of Elizabeth II in 1953.
Over the years, Theodora forged a close relationship with the British sovereign Queen Elizabeth II, who came to consider her as her favorite sister-in-law, according to the Spanish biographer Ricardo Mateos Sainz de Medrano.
The marriages of their daughter Margarita to Prince Tomislav of Yugoslavia in 1957 and their son Maximilian to Archduchess Valerie of Austria in 1966 were the occasions for great meetings of the European aristocracy.
In 1965, Theodora organized a large reception in Salem on the occasion of the official trip of Queen Elizabeth II and Prince Philip to West Germany.
Final years

At the end of the 1940s, Theodora began to suffer from heart problems.
Over time, her health deteriorated and she appeared very diminished at the wedding of Prince Juan Carlos and Princess Sophia in 1962.
Upset by the death of her husband, Theodora then hurriedly returned from Italy, where she was on vacation.
Theodora's last years were affected by the establishment of the Regime of the Colonels in Greece and by the departure into exile of King Constantine II and his family.
Hospitalized at the clinic of Doctor Büdingen in Konstanz, Theodora died on 16 October 1969, 7 weeks before her mother Princess Alice of Battenberg.
Her funeral was held at the mausoleum of the Baden family in Salem in the presence of many members of the aristocracy, including her nephew Prince Charles, but not her brother Prince Philip who was on an official trip to Canada.
In popular culture

A brief allusion to Theodora and Berthold is made in the episode "Dear Mrs Kennedy" (season 2, episode 8) of the historical drama series The Crown (2017).
Ancestry

Through her father, she was a grandchild of George I of Greece and Olga Konstantinovna of Russia and a great-great-granddaughter of Emperor Nicholas I of Russia.
Her mother was a granddaughter of Princess Alice, second daughter of Queen Victoria.
Notes and references

Notes

References

Bibliography

On Theodora and the Greek royal family

On Theodora and her German relatives

Biographies of Theodora's relatives



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
  AssignClass (db85f9ff-9c73-4422-a7ee-d1e8cb523181)
 Call ID: db85f9ff-9c73-4422-a7ee-d1e8cb523181
  Args:
    type: :Woman
    source: Theodora_of_Greece_and_Denmark
  AssignClass (ea39bbc3-c8af-4567-9611-1c97c5d03607)
 Call ID: ea39bbc3-c8af-4567-9611-1c97c5d03607
  Args:
    type: :Person
    source: Theodora_of_Greece_and_Denmark
  AddLiteral (dfec5d16-0b12-4ac9-b030-6a7f09f55017)
 Call ID: dfec5d16-0b12-4ac9-b030-6a7f09f55017
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Theodora_of_Greece_and_Denmark
    literal_value: 1906
  AddLiteral (bccc38f7-6389-48ef-98c6-0a3c8264617d)
 Call ID: bccc38f7-6389-48ef-98c6-0a3c8264617d
  Args:
    relation: :hasDeathYear
    literal_value: 1969
    source: Theodora_of_Greece_and_Denmark
    literal_type: xsd:integer
  AssignClass (07f35736-5da4-49c5-be3a-2814a4b63ce1)
 Call ID: 07f35736-5da4-49c5-be3a-2814a4b63ce1
  Args:
    type: :Man
    source: Andrew_of_Greece_and_Denmark
  AssignClass (b38248ac-13da-4295-ae19-57a7cf36eaed)
 Call ID: b38248ac-13da-4295-ae19-57a7cf36eaed
  Args:
    type: :Person
    source: Andrew_of_Greece_and_Denmark
  AssignClass (c6d9a8d8-e5b7-46f4-8acf-092d40f0d128)
 Call ID: c6d9a8d8-e5b7-46f4-8acf-092d40f0d128
  Args:
    type: :Ancestor
    source: Andrew_of_Greece_and_Denmark
  AssignClass (7efd2c4a-de14-47a7-9052-1d66d223ac7c)
 Call ID: 7efd2c4a-de14-47a7-9052-1d66d223ac7c
  Args:
    source: Alice_of_Battenberg
    type: :Woman
  AssignClass (37f35852-2367-499d-a2ae-bf56ddb75eb4)
 Call ID: 37f35852-2367-499d-a2ae-bf56ddb75eb4
  Args:
    type: :Person
    source: Alice_of_Battenberg
  AssignClass (ff184e6c-5cb6-4067-9c77-99937201a10b)
 Call ID: ff184e6c-5cb6-4067-9c77-99937201a10b
  Args:
    type: :Ancestor
    source: Alice_of_Battenberg
  AddTriple (97118f6c-35d3-4c2b-a3d0-024f8d486928)
 Call ID: 97118f6c-35d3-4c2b-a3d0-024f8d486928
  Args:
    target: Andrew_of_Greece_and_Denmark
    source: Theodora_of_Greece_and_Denmark
    relation: :hasFather
  AddTriple (176eb3ce-3a99-46d3-beba-1f0e16056a5e)
 Call ID: 176eb3ce-3a99-46d3-beba-1f0e16056a5e
  Args:
    target: Alice_of_Battenberg
    source: Theodora_of_Greece_and_Denmark
    relation: :hasMother
  AssignClass (3ea0a2ee-71f3-47ef-914b-e2dd4676e1ce)
 Call ID: 3ea0a2ee-71f3-47ef-914b-e2dd4676e1ce
  Args:
    source: Berthold_of_Baden
    type: :Man
  AssignClass (981f6fb2-76b9-4a7b-893f-a4a18e13194b)
 Call ID: 981f6fb2-76b9-4a7b-893f-a4a18e13194b
  Args:
    type: :Person
    source: Berthold_of_Baden
  AddTriple (c8111d4d-9ee3-44f1-9ee8-97dddd045d25)
 Call ID: c8111d4d-9ee3-44f1-9ee8-97dddd045d25
  Args:
    relation: :hasRelation
    target: Berthold_of_Baden
    source: Theodora_of_Greece_and_Denmark
  AddLiteral (dc3f6d0e-f95d-4c82-9074-bf30904f74e6)
 Call ID: dc3f6d0e-f95d-4c82-9074-bf30904f74e6
  Args:
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: Theodora_of_Greece_and_Denmark
    literal_value: 1931
  AssignClass (078bb2cd-9ee9-47d4-9fe1-53928aad78af)
 Call ID: 078bb2cd-9ee9-47d4-9fe1-53928aad78af
  Args:
    type: :Woman
    source: Margarita_of_Baden
  AssignClass (cf81937d-f3e5-464f-b0a5-3f6a49488485)
 Call ID: cf81937d-f3e5-464f-b0a5-3f6a49488485
  Args:
    type: :Person
    source: Margarita_of_Baden
  AssignClass (bcbe88f9-db25-443b-9e6d-8d199aa384af)
 Call ID: bcbe88f9-db25-443b-9e6d-8d199aa384af
  Args:
    source: Maximilian_of_Baden
    type: :Man
  AssignClass (ffd7d0be-fafd-403d-bf5c-5747f1f9cc43)
 Call ID: ffd7d0be-fafd-403d-bf5c-5747f1f9cc43
  Args:
    type: :Person
    source: Maximilian_of_Baden
  AssignClass (bd9baeea-bca5-4218-820b-8bef72131e77)
 Call ID: bd9baeea-bca5-4218-820b-8bef72131e77
  Args:
    type: :Man
    source: Ludwig_of_Baden
  AssignClass (c2759f52-d740-4374-ba22-9699230afd9c)
 Call ID: c2759f52-d740-4374-ba22-9699230afd9c
  Args:
    type: :Person
    source: Ludwig_of_Baden
  AddTriple (ec124675-4812-4146-a240-a43c99c4eed9)
 Call ID: ec124675-4812-4146-a240-a43c99c4eed9
  Args:
    source: Theodora_of_Greece_and_Denmark
    target: Margarita_of_Baden
    relation: :hasDaughter
  AddTriple (95359d1a-c59b-4923-811e-23abfb23b0c4)
 Call ID: 95359d1a-c59b-4923-811e-23abfb23b0c4
  Args:
    target: Maximilian_of_Baden
    source: Theodora_of_Greece_and_Denmark
    relation: :hasSon
  AddTriple (abe54008-1487-437a-a21b-4109e5ea4221)
 Call ID: abe54008-1487-437a-a21b-4109e5ea4221
  Args:
    target: Ludwig_of_Baden
    source: Theodora_of_Greece_and_Denmark
    relation: :hasSon
  AssignClass (9cac5397-2849-4764-8ac3-a457e0ea8aa2)
 Call ID: 9cac5397-2849-4764-8ac3-a457e0ea8aa2
  Args:
    type: :Man
    source: Philip_of_Greece_and_Denmark
  AssignClass (77e1b090-1656-4200-86cf-a346192e122a)
 Call ID: 77e1b090-1656-4200-86cf-a346192e122a
  Args:
    source: Philip_of_Greece_and_Denmark
    type: :Person
  AddTriple (9dd3b24b-6582-418d-869e-e51fbd73174a)
 Call ID: 9dd3b24b-6582-418d-869e-e51fbd73174a
  Args:
    target: Philip_of_Greece_and_Denmark
    source: Theodora_of_Greece_and_Denmark
    relation: :hasBrother
  AssignClass (70c956a5-9b82-4d2f-aac9-833935439f8a)
 Call ID: 70c956a5-9b82-4d2f-aac9-833935439f8a
  Args:
    source: Margarita_sister_of_Theodora
    type: :Woman
  AssignClass (6ae45c65-1b01-47a1-81a7-05c7cdf68b28)
 Call ID: 6ae45c65-1b01-47a1-81a7-05c7cdf68b28
  Args:
    type: :Person
    source: Margarita_sister_of_Theodora
  AssignClass (513a148e-e47e-4fab-9b85-72239837ea1b)
 Call ID: 513a148e-e47e-4fab-9b85-72239837ea1b
  Args:
    type: :Woman
    source: Cecilie_of_Greece
  AssignClass (6cd5536d-8814-48c3-aad0-5ccc8e96f415)
 Call ID: 6cd5536d-8814-48c3-aad0-5ccc8e96f415
  Args:
    type: :Person
    source: Cecilie_of_Greece
  AssignClass (6b307b91-f69a-4d19-b58c-f528d9578027)
 Call ID: 6b307b91-f69a-4d19-b58c-f528d9578027
  Args:
    type: :Woman
    source: Sophie_of_Greece
  AssignClass (e82d1b19-ceac-4a49-a0b5-b694a4162626)
 Call ID: e82d1b19-ceac-4a49-a0b5-b694a4162626
  Args:
    source: Sophie_of_Greece
    type: :Person
  AddTriple (390777a8-0220-42ed-b347-718e1ce7a2d1)
 Call ID: 390777a8-0220-42ed-b347-718e1ce7a2d1
  Args:
    target: Margarita_sister_of_Theodora
    source: Theodora_of_Greece_and_Denmark
    relation: :hasSister
  AddTriple (e9c3c97f-ea09-4483-833d-cc07dc612e98)
 Call ID: e9c3c97f-ea09-4483-833d-cc07dc612e98
  Args:
    target: Cecilie_of_Greece
    source: Theodora_of_Greece_and_Denmark
    relation: :hasSister
  AddTriple (a9b8626b-609d-4f37-83e8-9dd5b42c177e)
 Call ID: a9b8626b-609d-4f37-83e8-9dd5b42c177e
  Args:
    relation: :hasSister
    source: Theodora_of_Greece_and_Denmark
    target: Sophie_of_Greece
  Finish (2b33bac2-8281-4955-89ec-dbb7908d98da)
 Call ID: 2b33bac2-8281-4955-89ec-dbb7908d98da
  Args: