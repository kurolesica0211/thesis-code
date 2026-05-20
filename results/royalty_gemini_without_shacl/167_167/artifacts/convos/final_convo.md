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
Princess Margarita of Greece and Denmark (Greek: Μαργαρίτα; 18 April 1905 – 24 April 1981) was a Greek and Danish princess by birth and Princess of Hohenlohe-Langenburg by marriage.
An elder sister of Prince Philip, Duke of Edinburgh (husband of Queen Elizabeth II), she was, for a time, linked to the Nazi regime.
The eldest daughter of Prince Andrew of Greece and Denmark and Princess Alice of Battenberg, Margarita spent a happy childhood between Athens and Corfu.
For the young princess and her relatives, these conflicts had dramatic consequences and led to their exile in Switzerland (between 1917 and 1920), then in France and the United Kingdom (from 1922 to 1936).
During their exile, Margarita and her family depended on the generosity of their foreign relatives, in particular Princess George of Greece and Denmark (who offered them accommodation in Saint-Cloud) and Lady Louis Mountbatten (who supported them financially).
At the end of the 1920s, Margarita's mother had a mental health crisis which led to her confinement in a Swiss psychiatric hospital.
Shortly after, in 1931, Margarita married Prince Gottfried of Hohenlohe-Langenburg.
The couple then moved to Weikersheim Castle, where they raised four sons (Princes Kraft, Georg Andreas, Rupprecht and Albrecht) and a daughter (Princess Beatrix).
Members of the Nazi party from 1937, Gottfried and Margarita used their family connections to promote a rapprochement of Nazism within the United Kingdom, though without success.
In particular, she visited New York in 1934 to testify in favor of Gloria Morgan Vanderbilt, Gottfried's former fiancée, in the case between her and her in-laws for the custody of her daughter, also named Gloria.
Affected by the Second World War, which divided her relatives into two factions, Margarita spent time in Langenburg during the conflict.
The defeat of Germany and its occupation by the Allies brought new upheavals in the life of Margarita and Gottfried.
Though preserved from Soviets, who caused the death of several of their cousins, the couple were ostracized by the British royal family at the time of the marriage of Prince Philip, Margarita's only brother, to Princess Elizabeth of the United Kingdom in 1947.
Over the years, the couple were reintegrated into the life of the European elite, as illustrated by their invitation and presence at the coronation of Elizabeth II in 1953, and the princess's presence at the wedding of Juan Carlos, Prince of Asturias, and Princess Sophia of Greece and Denmark in 1962.
Widowed in 1960, Margarita witnessed a fire at Langenburg Castle in 1963.
The princess died in 1981 and her body was buried in the Hohenlohe-Langenburg family mausoleum.
Margarita was the paternal aunt of the Prince of Wales, who later became King Charles III.
Biography

Childhood

In Greece and abroad

The eldest daughter of Prince Andrew of Greece and Denmark and Princess Alice of Battenberg, Margarita was born at the Royal Palace in Athens on 18 April 1905.
Baptized on 11 May in the presence of her maternal grandparents, Margarita grew up surrounded by her father's animals, and within a united household, which rapidly expanded with the arrival of her sisters Theodora (1906–1969), Cecilie (1911–1937), and Sophie (1914–2001).
With their mother, Margarita and her sisters communicated in English, but they also used French, German, and Greek in the presence of their relatives and governesses.
Margarita's early childhood was marked by the instability that the Kingdom of Greece experienced at the beginning of the twentieth century.
Tired of attacks from the press and the opposition, Andrew and Alice found refuge in travel and made many stays outside the borders of their home country.
With their daughters, they stayed in the United Kingdom, Germany, Malta and Russia, where they reunited with their numerous relatives including Edward VII of the United Kingdom, Ernest Louis, Grand Duke of Hesse, Alexandra Feodorovna, Prince and Princess Louis of Battenberg (Alice's parents), etc.
From 1905, Margarita was thus introduced to her young maternal uncle and aunt, Louis and Louise, to whom she and her sister Theodora subsequently became very close.
In 1909, the Goudi coup occurred, a military putsch organized against the government of King George I of Greece, Margarita's grandfather.
Shortly after this event, Prince Andrew and his brothers were forced to resign from the army.
Concerned about the political situation of their country, Andrew and Alice once again found refuge abroad and stayed in the United Kingdom, France and Hesse.
After considering a life in exile for a while, the couple returned to live in Greece, where their third daughter was born.
The Balkan Wars and the First World War

Between 1912 and 1913, Greece engaged in the Balkan Wars, which put the country in opposition to the Ottoman Empire and to Bulgaria.
Called to join the army again, Prince Andrew served under Crown Prince Constantine while Princess Alice worked as a nurse for wounded soldiers.
Too young to follow their parents, Margarita and her sisters spent the duration of the conflict in Athens, with the exception of a brief stay in Thessaloniki in December 1912.
Greece came out of the Balkan Wars with an expanded territory, but the conflict also led to the demise of George I, who was assassinated in March 1913.
The death of the King of the Hellenes caused significant changes in the life of Margarita and her relatives.
In his will, the sovereign bequeathed the Corfiote palace of Mon Repos to Andrew.
After years of living in close proximity to the monarch, in the palaces of Athens and Tatoi, Andrew and his family therefore finally had their own residence.
When peace returned, Andrew, Alice and their daughters left Greece in August 1913.
After a visit to Germany, they stayed in the United Kingdom, with Margarita's maternal grandparents.
Returning to Greece on 17 November 1913, the family was then retained in the country by Alice's fourth pregnancy and, above all, by the outbreak of the First World War.
With Greece having proclaimed its neutrality, this new conflict initially hardly affected Margarita and her relatives.
Things changed as war creeped into the life of the country's people.
Stationed in Thessaloniki with his garrison, Andrew was thus confronted with the occupation of the city by the Allies in October 1915.
Shortly after, in December, the routed Serbian army found refuge in Corfu, leading Alice and her daughters to abandon Mon Repos for the capital.
Over the months, the amount of threats against members of the royal dynasty increased.
In addition, on 1 December, the French navy bombarded the royal palace in Athens, forcing Margarita and her sisters to take refuge in the cellars with their mother.
Exile in Switzerland

In June 1917, King Constantine I was finally deposed and driven out of Greece by the Allies, who replaced him on the throne by his second son, the young Alexander.
Fifteen days later, Margarita's family was in turn forced into exile in order to remove the possibility of the new monarch being influenced by those close to him.
With the fall of the Russian Empire in 1917, several of Margarita's relatives were murdered in Russia.
Shortly after these events, the Grand Ducal family of Hesse, to which Margarita was closely related through her mother, was overthrown along with all the other German dynasties during the winter of 1918–1919.
At the beginning of 1919, Margarita nevertheless had the joy of reuniting with her paternal grandmother, the Dowager Queen Olga, spared by the Bolsheviks thanks to the diplomatic intervention of the Danes.
In the months that followed, she reconnected, moreover, with her maternal grandparents, whom the war forced to abandon the name of Battenberg for that of Mountbatten.
For Margarita, who now formed a duo with her younger sister Theodora, exile was not only synonymous with nostalgia; it was also an opportunity for long family reunions and walks in the mountains.
Young adulthood

Brief return to Greece

On 2 October 1920, King Alexander, cousin of Margarita, was bitten by a domestic monkey during a walk in Tatoi.
The death of the sovereign caused a violent institutional crisis in Greece.
Humiliated, he retired abroad while a referendum reinstalled Constantine I on the throne.
Prince Andrew was received triumphantly in Athens on 23 November 1920, and his wife and four daughters joined him a few days later.
Margarita then returned to live in Corfu with her family.
At the same time, Princess Alice found out that she was pregnant again.
On 10 June 1921, the family welcomed Philip (1921–2021), the future Duke of Edinburgh.
The joy that surrounded this birth, however, was obscured by the absence of Prince Andrew, who joined the Greek forces in Asia Minor during the Occupation of Smyrna.
Despite worries about the war, Margarita and her siblings enjoyed life at Mon Repos, where they received a visit from their maternal grandmother and their aunt Louise in the spring of 1922.
In the park near the palace, built on an ancient cemetery, the princesses devoted themselves to archeology and discovered some pottery, bronze pieces and bones.
During this period, Margarita and her sisters also participated, for the first time, in a number of great social events.
In March 1921, the princesses attended in Athens the wedding of their cousin Helen to Crown Prince Carol of Romania.
In July 1922, they went to the United Kingdom to be bridesmaids at the wedding of their uncle Louis Mountbatten to the wealthy heiress Edwina Ashley.
However, the military defeat of Greece against Turkey and the political unrest that it caused disrupted the life of Margarita and her family.
In September 1922, Constantine I abdicated in favor of his eldest son, George II.
A month later, Prince Andrew was arrested before being tried by a military tribunal, which declared him responsible for the defeat of the Sakarya.
Saved from execution by the intervention of foreign chancelleries, the prince was condemned to banishment and cashiering.
After a brief stop in Corfu, the prince and his relatives hurriedly left Greece aboard HMS Calypso in early December 1922.
Marriage prospects

After a journey of several weeks, which led them successively to Italy, France and the United Kingdom, Margarita, her parents and her siblings settled in Saint-Cloud in 1923.
Settled in a house adjoining that of Princess Marie Bonaparte, the family depended for seven years on her generosity, and two other aunts of Margarita: first Princess Anastasia and then Edwina, Countess Mountbatten of Burma.
Marie Bonaparte financed the studies of her nieces and nephew, while Lady Mountbatten got into the habit of offering her nieces her "used" clothes.
In fact, Margarita's parents had little income and the children were the regular witnesses to their money problems and their difficulty in maintaining a household.
Deprived of their Greek nationality after the proclamation of the Second Hellenic Republic in March 1924, Margarita and her family received Danish passports from their cousin King Christian X.
Now of marrying age, the princess and her sister Theodora regularly left France for Great Britain, where they lived with their maternal grandmother, the Dowager Marchioness of Milford Haven.
With their aunt Louise, who increasingly replaced their mother as a chaperone and confidante, the two young girls attended most of the events by British aristocracy during the 1920s, including balls and dances, birthdays and garden parties at Buckingham Palace, horse races, etc.
However, the young girls' lack of fortune and their life in exile meant that they hardly had any suitors, which was a matter of concern to their mother Alice.
During the summer of 1926, Margarita met Prince François-Ferdinand d'Isembourg-Birstein, eldest son of Prince François-Joseph d'Isembourg-Birstein, during a stay in Tarasp with her great-uncle Ernest Louis, Grand Duke of Hesse.
Margarita was enchanted by her suitor and by the region where he lived.
However, François-Ferdinand was of the Catholic faith and the princess refused to give up Orthodox faith, which soon put an end to their romance.
Thus, by 1930, neither Margarita nor Theodora had yet found a fiancé.
This did not prevent them from rejoicing for their aunt Louise when she was asked by Gustaf Adolf, Crown Prince of Sweden, to marry him in June 1923.
Alice's confinement

Margarita, Theodora and Philip spent the summer of 1928 in Romania.
Invited by Princess Helen, whose son Michael I was the same age as Philip, the two young women and their brother stayed for several weeks in Sinaia.
At the time, Prince Nicholas of Romania was still single and Helen would like to see him marry one of her relatives, but her plans for her brother-in-law to marry one of her cousins came to nothing.
A few months after this trip, Alice allegedly began to suffer from psychological problems.
Struck by a mental health crisis, the prince said that the princess convinced herself she possessed healing powers and that she was receiving divine messages about potential husbands for her daughters.
Prince Andrew finally made the decision to place his wife in a sanatorium, with the agreement of his mother-in-law, the Dowager Marchioness of Milford Haven.
During his family's stay in Darmstadt, Germany, in April 1930, he sent Alice to a psychiatric hospital located in Kreuzlingen, Switzerland.
Margarita's two youngest sisters were married successively to German princes.
Sophie married Prince Christoph of Hesse in December 1930, followed by Cecilie who married Georg Donatus, Hereditary Grand Duke of Hesse in February 1931.
After years of celibacy, Margarita and Theodora were quick to marry in their turn.
Settling in Germany and stays abroad

Family life and adherence to Nazism

In 1930, Margarita was 25 when she met Gottfried ("Friedel"), hereditary prince of Hohenlohe-Langenburg, who like her descended from Queen Victoria of the United Kingdom.
Coming from the House of Hohenlohe, whose states were publicized at the beginning of the 19th century, the prince was heir to a fortune made up of castles, farmland and forests.
Margarita and Gottfried fell in love and married on 20 April 1931.
The occasion was a large family reunion, at which Margarita's mother Alice was not present.
Among the many guests were the Dowager Queen Marie of Romania and Grand Duchess Victoria Feodorovna of Russia (aunts of the groom) as well as Prince George of Greece and Denmark and Louise, Crown Princess of Sweden (uncle and aunt of the bride).
Once their marriage was celebrated, Margarita and Gottfried settled at Weikersheim Castle, located not far from the town of Langenburg.
After a stillbirth in 1933, Margarita gave birth to three children: Kraft (1935–2004), Beatrix (1936–1997), and Georg Andreas (1938–2021).
Concerned about her mother's fate, Margarita visited her several times in Kreuzlingen, and their reunion was often filled with emotions.
However, Alice was angry with those close to her for having her placed in an asylum and, once released from there in 1933, she made known her desire to stay away from her family.
The reconciliation of the princess and her children finally happened in 1937, and Margarita saw her mother for the first time in July.
When she was not taking care of those close to her, Margarita was involved in charitable works, which soon earned her the admiration of the inhabitants of the former principality of Hohenlohe-Langenburg.
Like several members of her entourage, Margarita joined the Nazi Party on 1 May 1937 at the same time as her husband.
In October 1934, Gottfried and Margarita visited New York to testify in favor of Gloria Morgan Vanderbilt in the lawsuit involving her and her in-laws for the custody of her daughter Gloria Vanderbilt.
A few years before his marriage to Margarita, Gottfried had an affair with the wealthy American widow, whom he even almost married with the blessing of his parents.
For her part, Margarita visited Gloria Morgan Vanderbilt at her aunt Nadejda Mountbatten's place.
However, the in-laws of Gloria Morgan Vanderbilt accused her of having abandoned her daughter by leading a dissolute life with Gottfried in Europe.
Margarita further suspected the young woman of having a romantic relationship with Nadejda.
Margarita therefore had interest in restoring the honor of her family by participating in the trial with her husband.
In spite of the testimonies of the Prince and the Princess of Hohenlohe-Langenburg, who assured the good morality of their friend in front of the press and in court, Gloria Morgan Vanderbilt lost the lawsuit.
Gottfried and Margarita left the United States in early November to attend the wedding of Marina, cousin of the princess, and the Duke of Kent in London.
Travel to Greece

While Germany sank into dictatorship from 1933, the Hellenic Republic was overthrown by General Kondylis in October 1935.
A month later, King George II, Margarita's cousin, was reinstalled on the throne after a referendum.
At the beginning of 1936, the banishment sentence issued in 1922 against Margarita's father Prince Andrew was lifted, which allowed him to stay in his country again.
A regular target for the Hellenic press, the prince however chose to stay abroad for most of the year.
Estranged from her husband since her confinement, Princess Alice made the choice to return and live in Athens, where she settled in November 1938.
In the meantime, Margarita also returned to Greece with Gottfried on the occasion of the marriage of Crown Prince Paul to Princess Frederica of Hanover in January 1938.
Second World War and subsequent events

Family torn apart by war

The outbreak of the Second World War greatly affected Margarita, whose family found themselves divided by the conflict.
While her husband and brothers-in-law Prince Christoph of Hesse and Berthold, Margrave of Baden, joined the German ranks, her brother Philip fought in the British Royal Navy.
The invasion and occupation of France by Germany also block Prince Andrew on the French Riviera and contacting him became very difficult.
As for Princess Alice, she refused to leave Greece at the time of invasion and spent most of the conflict in Athens helping refugees and hiding Jews, though she managed to pay a few visits to her daughters in 1940, 1942, and 1944.
Margarita spent the duration of the conflict with her children in Langenburg, a small town far from the zones of combat and where the family did not suffer much deprivation.
According to the Spanish biographer Ricardo Mateos Sainz de Medrano, the Prince of Hohenlohe-Langenburg was wounded during the Battle of Amiens and he spent the remainder of the conflict with his family in Langenburg.
More credible is therefore the version given by the Hohenloher Tagblatt in an article devoted to the prince in 2010.
Seriously wounded on the Eastern Front, where he commanded a reconnaissance unit until 1944, Gottfried was dismissed from the army at the continuation of the decree banning people of royal descent from serving in the army.
Back in Langenburg, the prince transformed the family castle into a hospital, before welcoming refugees there.
The war period brought its share of mourning for Margarita's family.
In April 1942, her mother-in-law, the Dowager Princess of Hohenlohe-Langenburg, died in Schwäbisch Hall after a long illness.
A little over a year later, in October 1943, Prince Christoph, husband Margarita's sister Sophie, was killed in a plane crash while flying over the Apennine Mountains.
Finally, in December 1944, her father Prince Andrew died in Monaco without having been able to see his children again.
Post-war years

The defeat of Germany and its occupation by the Allies brought new upheavals in the life of the former German princely families, several of whom (such as Hermine Reuss of Greiz, Joachim Ernst, Duke of Anhalt, or Georg, Prince of Saxe-Meiningen) perished in hands of the Soviets.
When the war ended, Margarita and her family found themselves in the American-occupied part of Germany, so their lives were not under threat.
Despite her own Germanic origins, Princess Alice of Battenberg thus developed a deep disgust for the German people and refused, until 1949, to return to stay in her daughters' country.
For his part, Prince Philip (officially renamed Philip Mountbatten in 1947) found himself unable to invite his sisters on the occasion of his marriage to Princess Elizabeth of the United Kingdom because of anti-German sentiment prevailing in Great Britain after the war.
Aware of the difficulties their brother had to face, Margarita, Theodora and Sophie considered their sidelining wrong and hurtful.
Harassed by the press, who submitted requests for interviews with them, Margarita and her sisters spent the day of 20 November 1947 at Marienburg Castle with their families.
Invited by the Duke and Duchess of Brunswick, they celebrated the union of their brother in the company of their cousin Princess Elizabeth of Greece and Denmark and Prince Louis and Princess Margaret of Hesse and by Rhine.
A few days later, the Greek princesses received a visit from the Queen of the Hellenes (who came to bring them a letter from their mother Princess Alice describing the wedding in detail) and the Duchess of Kent.
Return to normal life

Reintegration into royal circles

In March 1948, Margarita and her three elder children were invited to Athens by Princess Alice, who offered them the trip thanks to the pension that the Countess Mountbatten of Burma continued to pay her.
Invited to stay at the Royal Palace by King Paul and Queen Frederica, Margarita was delighted to be back in her home country.
In the years that followed, the Hohenlohe-Langenburgs made several other stays in Greece.
In 1962, the Princess attended the wedding of Princess Sophia of Greece and Denmark and Juan Carlos, Prince of Asturias.
The Greek royal family was not the only royal house to show its desire to reconnect with the Hohenlohe-Langenburgs.
In 1950, Margarita was allowed to return to the United Kingdom on the occasion of the funeral of her grandmother, the Dowager Marchioness of Milford Haven.
A few months later, the princess was chosen to be one of the godmothers of her niece, Princess Anne.
Above all, in 1953, Margarita, her sisters, their husbands and some of their children were invited to the coronation of Elizabeth II.
Satisfied not to have been sidelined once again, the Princess of Hohenlohe-Langenburg nonetheless noted with sadness the anguish of her brother Philip, who considered with apprehension his new status as prince consort.
In the 1950s, Margarita and her husband also visited Spain on several occasions.
There they found various members of Gottfried's relatives: Princess Beatrice of Saxe-Coburg and Gotha and her husband Infante Alfonso, Duke of Galliera (maternal aunt and uncle of the prince), Princess Alexandra of Hohenlohe-Langenburg (sister of the prince), as well as Prince Alfonso of Hohenlohe-Langenburg and his wife Ira von Fürstenberg (distant cousins of the prince).
Life in Langenburg

In December 1950, Prince Ernest II, Margarita's father-in-law, died and Gottfried succeeded him as head of the House of Hohenlohe.
The prince then inherited a substantial fortune, made up of agricultural land and forests, but also of two castles (Langenburg and Weikersheim), both very expensive to maintain.
The prince also sought to develop tourism in the former principality of Hohenlohe-Langenburg.
Beginning in the 1930s, Margarita gained a lot of weight, which was of concern to those close to her.
At the end of the 1950s, however, Gottfried's state of health deteriorated and he died on 11 May 1960, making Prince Kraft, his eldest son, the new head of the house of Hohenlohe.
Very affected by the demise of her husband, Margarita nevertheless followed the advice of her mother, who recommended her not to withdraw and to take a more active part in social life.
In 1961, the princess thus attended the wedding of Prince Edward, Duke of Kent, and Katharine Worsley.
Shortly after, she was present a reception in honor of US President John F. Kennedy at Buckingham Palace.
There were no casualties but the private apartments of the princess and many of her personal objects were destroyed.
The damage to the building was considerable and forced Prince Kraft to sell Weikersheim Castle in 1967 to finance the renovation work.
This did not prevent the Hohenlohe-Langenburgs from receiving Queen Elizabeth II and Prince Philip in their castle during their official trip to West Germany in 1965.
For Margarita, the 1960s saw the marriages of two of her children.
In 1965, Prince Kraft married Princess Charlotte von Croÿ.
Then, in 1969, Prince Georg Andreas married Princess Luise von Schönburg-Waldenburg.
The engagement of Princess Beatrix to her nephew Maximilian, Margrave of Baden, son of Princess Theodora, on the other hand broke off in 1961 and the princess remained unmarried all her life.
This event did not prevent Margarita from remaining close to her sister until her death in October 1969.
Devastated by the loss of her younger sister, who was only one year younger than her, Margarita also lost her mother Alice two months later.
Final years

Margarita's son Albrecht married Maria Hildegard-Fischer in 1976.
His twin brother, Rupprecht, took his own life in 1978.
Margarita died on 24 April 1981 at a clinic in Bad Wiessee, Bavaria, from congresive heart failure, just six days after her 76th birthday.
Attended by her brother the Duke of Edinburgh, her funeral took place in Langenburg, where she was interred beside her husband.
Archives

Margarita's personal papers (including family correspondence and photographs) are preserved in the Hohenlohe-Langenburg family archive (Nachlass Fürstin Margarita, HZAN La 148), which is in the Hohenlohe Central Archive (Hohenlohe-Zentralarchiv Neuenstein) in Neuenstein Castle in the town of Neuenstein, Baden-Württemberg, Germany.
Ancestry

Notes and references

Notes

References

Bibliography

On Margarita and the Greek royal family

On Margarita and her German relatives

Biographies of Margarita's relatives

On the Vanderbilt affair

External links



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
  AssignClass (5dc8fbe2-7aab-4214-a5e8-964a3dcf73e9)
 Call ID: 5dc8fbe2-7aab-4214-a5e8-964a3dcf73e9
  Args:
    type: :Woman
    source: Margarita_of_Greece_and_Denmark
  AssignClass (48067ba0-4420-465f-a0e5-9591ab2f96df)
 Call ID: 48067ba0-4420-465f-a0e5-9591ab2f96df
  Args:
    type: :Person
    source: Margarita_of_Greece_and_Denmark
  AddLiteral (1c0036ac-1a64-41ab-bd9f-859618938c0d)
 Call ID: 1c0036ac-1a64-41ab-bd9f-859618938c0d
  Args:
    literal_value: 1905
    source: Margarita_of_Greece_and_Denmark
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (d764266e-7b7f-45f1-bfb8-57f61129ab46)
 Call ID: d764266e-7b7f-45f1-bfb8-57f61129ab46
  Args:
    literal_type: xsd:integer
    literal_value: 1981
    source: Margarita_of_Greece_and_Denmark
    relation: :hasDeathYear
  AssignClass (e615d2e2-702a-4246-943d-01c7f497d075)
 Call ID: e615d2e2-702a-4246-943d-01c7f497d075
  Args:
    type: :Man
    source: Andrew_of_Greece_and_Denmark
  AssignClass (e034dd00-b581-44f3-8824-a8392b6445a0)
 Call ID: e034dd00-b581-44f3-8824-a8392b6445a0
  Args:
    source: Andrew_of_Greece_and_Denmark
    type: :Person
  AssignClass (b3743316-e939-4493-b1c0-6ee8e0215baf)
 Call ID: b3743316-e939-4493-b1c0-6ee8e0215baf
  Args:
    type: :Woman
    source: Alice_of_Battenberg
  AssignClass (591dead0-073f-4867-88f8-ce5f9b9331b1)
 Call ID: 591dead0-073f-4867-88f8-ce5f9b9331b1
  Args:
    source: Alice_of_Battenberg
    type: :Person
  AddTriple (51a49f29-9002-4cf5-93bb-839f47784a56)
 Call ID: 51a49f29-9002-4cf5-93bb-839f47784a56
  Args:
    relation: :hasFather
    target: Andrew_of_Greece_and_Denmark
    source: Margarita_of_Greece_and_Denmark
  AddTriple (df4a93c7-3bf3-4d94-b8e9-f69fe01183de)
 Call ID: df4a93c7-3bf3-4d94-b8e9-f69fe01183de
  Args:
    relation: :hasMother
    target: Alice_of_Battenberg
    source: Margarita_of_Greece_and_Denmark
  AssignClass (fe4c7b1b-d721-4b71-b766-537ba69d5360)
 Call ID: fe4c7b1b-d721-4b71-b766-537ba69d5360
  Args:
    source: Prince_Philip
    type: :Man
  AssignClass (9f53d9db-ece1-4338-8022-77cde5ed5844)
 Call ID: 9f53d9db-ece1-4338-8022-77cde5ed5844
  Args:
    source: Prince_Philip
    type: :Person
  AddTriple (868adc17-dc70-4130-b430-3f9a10b16300)
 Call ID: 868adc17-dc70-4130-b430-3f9a10b16300
  Args:
    relation: :isSiblingOf
    target: Prince_Philip
    source: Margarita_of_Greece_and_Denmark
  AssignClass (dfa848c7-f590-4f99-8dc0-0b908d4a54fb)
 Call ID: dfa848c7-f590-4f99-8dc0-0b908d4a54fb
  Args:
    source: Theodora_of_Greece_and_Denmark
    type: :Woman
  AssignClass (eab59914-5fce-4c24-bd6a-74734800f9b0)
 Call ID: eab59914-5fce-4c24-bd6a-74734800f9b0
  Args:
    type: :Person
    source: Theodora_of_Greece_and_Denmark
  AddTriple (637ecaaf-8786-4900-bd1a-951cbf1e3ae8)
 Call ID: 637ecaaf-8786-4900-bd1a-951cbf1e3ae8
  Args:
    relation: :isSisterOf
    target: Margarita_of_Greece_and_Denmark
    source: Theodora_of_Greece_and_Denmark
  AssignClass (60fe51a3-c8ce-47f1-8d87-553b60682462)
 Call ID: 60fe51a3-c8ce-47f1-8d87-553b60682462
  Args:
    source: Cecilie_of_Greece_and_Denmark
    type: :Woman
  AssignClass (cd54d8f8-0f8c-4dad-b734-fd03c632fa2c)
 Call ID: cd54d8f8-0f8c-4dad-b734-fd03c632fa2c
  Args:
    type: :Person
    source: Cecilie_of_Greece_and_Denmark
  AddTriple (49b9be90-72f5-415d-b088-36884a55dda0)
 Call ID: 49b9be90-72f5-415d-b088-36884a55dda0
  Args:
    source: Cecilie_of_Greece_and_Denmark
    target: Margarita_of_Greece_and_Denmark
    relation: :isSisterOf
  AssignClass (88dcbec3-6822-4262-97a0-17526561cf37)
 Call ID: 88dcbec3-6822-4262-97a0-17526561cf37
  Args:
    source: Sophie_of_Greece_and_Denmark
    type: :Woman
  AssignClass (c36a86bf-2ea1-4ab8-8bc8-a90812d85070)
 Call ID: c36a86bf-2ea1-4ab8-8bc8-a90812d85070
  Args:
    source: Sophie_of_Greece_and_Denmark
    type: :Person
  AddTriple (45797f5d-f0b1-4b2b-a4fc-a85e145b6f62)
 Call ID: 45797f5d-f0b1-4b2b-a4fc-a85e145b6f62
  Args:
    relation: :isSisterOf
    source: Sophie_of_Greece_and_Denmark
    target: Margarita_of_Greece_and_Denmark
  AssignClass (82984bc0-3916-48c3-b844-f7f0643f387e)
 Call ID: 82984bc0-3916-48c3-b844-f7f0643f387e
  Args:
    source: Gottfried_of_Hohenlohe-Langenburg
    type: :Man
  AssignClass (e14deaec-edbc-4483-90f6-0bb13dfdca97)
 Call ID: e14deaec-edbc-4483-90f6-0bb13dfdca97
  Args:
    source: Gottfried_of_Hohenlohe-Langenburg
    type: :Person
  AddLiteral (7ea2a6b9-b962-4576-b598-61e49fd8f22a)
 Call ID: 7ea2a6b9-b962-4576-b598-61e49fd8f22a
  Args:
    relation: :hasMarriageYear
    literal_type: xsd:integer
    literal_value: 1931
    source: Margarita_of_Greece_and_Denmark
  AddTriple (9eb5e695-c5cb-4645-8cc2-8b7e8169a033)
 Call ID: 9eb5e695-c5cb-4645-8cc2-8b7e8169a033
  Args:
    target: Gottfried_of_Hohenlohe-Langenburg
    source: Margarita_of_Greece_and_Denmark
    relation: :hasRelation
  AssignClass (ba7f517c-2921-4d61-bdfd-ceb4a7c2660f)
 Call ID: ba7f517c-2921-4d61-bdfd-ceb4a7c2660f
  Args:
    source: Kraft_of_Hohenlohe-Langenburg
    type: :Man
  AssignClass (032847b8-37e0-4c40-a6f2-d098fa7a84e4)
 Call ID: 032847b8-37e0-4c40-a6f2-d098fa7a84e4
  Args:
    source: Kraft_of_Hohenlohe-Langenburg
    type: :Person
  AddTriple (432ffe75-be88-4de1-b4e5-81decb70518e)
 Call ID: 432ffe75-be88-4de1-b4e5-81decb70518e
  Args:
    target: Kraft_of_Hohenlohe-Langenburg
    source: Margarita_of_Greece_and_Denmark
    relation: :hasSon
  AssignClass (3b2a8c3a-34c0-463b-8d9c-ac6acb0a56fa)
 Call ID: 3b2a8c3a-34c0-463b-8d9c-ac6acb0a56fa
  Args:
    source: Georg_Andreas_of_Hohenlohe-Langenburg
    type: :Man
  AssignClass (df557e83-6156-4146-a15f-662b247f1463)
 Call ID: df557e83-6156-4146-a15f-662b247f1463
  Args:
    type: :Person
    source: Georg_Andreas_of_Hohenlohe-Langenburg
  AddTriple (cd924f00-25c6-43f7-9c19-6099f7701f42)
 Call ID: cd924f00-25c6-43f7-9c19-6099f7701f42
  Args:
    relation: :hasSon
    source: Margarita_of_Greece_and_Denmark
    target: Georg_Andreas_of_Hohenlohe-Langenburg
  AssignClass (a63d69f8-3bce-457e-9a95-a350404b6a04)
 Call ID: a63d69f8-3bce-457e-9a95-a350404b6a04
  Args:
    source: Rupprecht_of_Hohenlohe-Langenburg
    type: :Man
  AssignClass (0e26f74e-9c29-44fa-860a-48999c477410)
 Call ID: 0e26f74e-9c29-44fa-860a-48999c477410
  Args:
    type: :Person
    source: Rupprecht_of_Hohenlohe-Langenburg
  AddTriple (088198ee-e705-4621-889c-cc9970e6c92c)
 Call ID: 088198ee-e705-4621-889c-cc9970e6c92c
  Args:
    source: Margarita_of_Greece_and_Denmark
    target: Rupprecht_of_Hohenlohe-Langenburg
    relation: :hasSon
  AssignClass (f04ca1fb-c251-4f53-9f19-2d1c410fef69)
 Call ID: f04ca1fb-c251-4f53-9f19-2d1c410fef69
  Args:
    type: :Man
    source: Albrecht_of_Hohenlohe-Langenburg
  AssignClass (0c07ed14-3867-4187-af20-747c30743ffc)
 Call ID: 0c07ed14-3867-4187-af20-747c30743ffc
  Args:
    source: Albrecht_of_Hohenlohe-Langenburg
    type: :Person
  AddTriple (97ed2c8f-c883-4578-aca3-bdb2d511192d)
 Call ID: 97ed2c8f-c883-4578-aca3-bdb2d511192d
  Args:
    relation: :hasSon
    source: Margarita_of_Greece_and_Denmark
    target: Albrecht_of_Hohenlohe-Langenburg
  AssignClass (8e56e5a6-75b3-4465-8574-a6565daafa00)
 Call ID: 8e56e5a6-75b3-4465-8574-a6565daafa00
  Args:
    source: Beatrix_of_Hohenlohe-Langenburg
    type: :Woman
  AssignClass (bd84ece8-4927-4c93-8f58-71a7986985b9)
 Call ID: bd84ece8-4927-4c93-8f58-71a7986985b9
  Args:
    type: :Person
    source: Beatrix_of_Hohenlohe-Langenburg
  AddTriple (4e533571-ae1f-4b33-8294-b43557520316)
 Call ID: 4e533571-ae1f-4b33-8294-b43557520316
  Args:
    relation: :hasDaughter
    target: Beatrix_of_Hohenlohe-Langenburg
    source: Margarita_of_Greece_and_Denmark
  Finish (ceaabbd6-dc22-47ad-9354-04f22dba3beb)
 Call ID: ceaabbd6-dc22-47ad-9354-04f22dba3beb
  Args: