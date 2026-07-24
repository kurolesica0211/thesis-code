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
Princess Sophie of Greece and Denmark (Greek: Σοφία, romanized: Sofía; 26 June 1914 – 24 November 2001) was by birth a Greek and Danish princess, as well as a princess of Hesse-Kassel and a princess of Hanover through her successive marriages to Prince Christoph of Hesse and Prince George William of Hanover.
An elder sister of Prince Philip, Duke of Edinburgh (husband of Queen Elizabeth II), she was, for a time, linked to the Nazi regime.
The fourth of five children of Prince Andrew of Greece and Denmark and Princess Alice of Battenberg, Sophie spent a happy childhood.
During their exile, Sophie and her family depended on the generosity of their foreign relatives, in particular Marie Bonaparte (who offered them accommodation in Saint-Cloud) and Lady Louis Mountbatten (who supported them financially).
At the end of the 1920s, Sophie fell in love with one of her distant cousins, Prince Christoph of Hesse.
Married in December 1930, Sophie moved to Berlin with her husband.
Close to the Nazi circles, in which her husband and several of her in-laws were involved from 1930, Sophie joined the National Socialist Women's League in 1938.
Sophie and her in-laws served as unofficial intermediaries between Nazi Germany and the European dynasties to which they were related.
Christoph and Sophie moved into a large house located in Dahlem, in 1936.
The outbreak of the Second World War, however, forced the couple to separate; Sophie moved with her children to her mother-in-law at Friedrichshof Castle in Kronberg im Taunus.
Adolf Hitler's growing distrust of the German aristocracy (from 1942) and the betrayal of King Victor Emmanuel III of Italy (in 1943) led the Nazi regime to turn against the House of Hesse-Kassel.
Princess Mafalda, daughter of the Italian monarch and sister-in-law of Sophie, was imprisoned in Buchenwald, where she was seriously wounded and died shortly after, while her husband, Philipp, Landgrave of Hesse, was confined in Flossenbürg until the victory of the Allies.
At the same time, Christoph was found dead in mysterious circumstances, leaving Sophie almost alone with her four children and a fifth one on the way, as well as the children of Philipp and Mafalda.
The tragic events made Sophie turn against Nazism.
The defeat of Germany and its occupation by the Allies brought new difficulties in the life of Sophie, who found herself in a precarious financial situation due to the theft of her jewelry by American soldiers in 1946 and the sequestration of the property of her first husband until 1953.
After living for several months in Wolfsgarten, she began a relationship with another cousin, Prince George William of Hanover, whom she married in 1946.
Excluded from the 1947 wedding of her brother Prince Philip to Princess Elizabeth of the United Kingdom (later Queen Elizabeth II) because of her past links to the Nazi regime, Sophie was reintegrated into the royal circles in the early 1950s.
She nevertheless led a discreet and withdrawn life, spending her time reading, listening to music and gardening.
The last surviving sibling of the Duke of Edinburgh, she died in a retirement home in Schliersee in 2001.
She was the paternal aunt of the Prince of Wales, who later became King Charles III.
Biography

Childhood

First World War and exile in Switzerland

The fourth daughter of Prince Andrew of Greece and Denmark and Princess Alice of Battenberg, Sophie was born on 26 June 1914 at Mon Repos, a palace in Corfu that her parents inherited after the assassination of King George I in 1913.
Nicknamed "Tiny" by her family, the princess grew up within a united household, together with her elder sisters Margarita (1905–1981), Theodora (1906–1969), and Cecilie (1911–1937).
With their mother, Sophie and her sisters communicated in English, but they also used French, German, and Greek in the presence of their relatives and governesses.
Sophie's early childhood was marked by the instability that the Kingdom of Greece experienced due to the First World War.
The conflict divided her family into opposing branches, and Greece eventually set aside its neutrality due to the Triple Entente.
Sophie and her sisters were in the royal palace of Athens when it was bombarded by the French Navy during the battle in the capital on 1 December 1916.
In June 1917, King Constantine I, Sophie's uncle, was finally deposed and driven out of Greece by the Allies, who replaced him on the throne by his second son, the young Alexander.
Fifteen days later, Sophie's family was in turn forced into exile and had to leave Mon Repos in order to remove the possibility of the new monarch being influenced by those close to him.
Following the Russian Revolution, Sophie's Romanov relatives were murdered in Russia.
Shortly after these events, the Grand Ducal family of Hesse, to which Sophie was closely related through her mother, was overthrown along with all the other German dynasties during the winter of 1918–1919.
At the beginning of 1919, Sophie reunited with her paternal grandmother, the Dowager Queen Olga, spared by the Bolsheviks thanks to the diplomatic intervention of the Danes.
In the following months, Sophie attended a family reunion with her maternal grandparents, and met her aunt Louise and uncle Louis Mountbatten.
For Sophie, who now formed a duo with her third-eldest sister Cecilie, exile was not only synonymous with sadness; it was also an opportunity for long family reunions and walks in the mountains.
Brief return to Greece

On 2 October 1920, King Alexander, cousin of Sophie, was bitten by a domestic monkey during a walk in Tatoi.
The death of the sovereign caused a violent institutional crisis in Greece.
Humiliated, he retired abroad while a referendum reinstalled Constantine I on the throne.
Prince Andrew was received triumphantly in Athens on 23 November 1920, and his wife and four daughters joined him a few days later.
Sophie then returned to live in Corfu with her family.
At the same time, Princess Alice found out that she was pregnant again.
On 10 June 1921, the family welcomed Philip (1921–2021), later the Duke of Edinburgh.
The joy that surrounded this birth, however, was obscured by the absence of Prince Andrew, who joined the Greek forces in Asia Minor during the Occupation of Smyrna.
Despite worries about the war, Sophie and her siblings enjoyed life at Mon Repos, where they received a visit from their maternal grandmother and their aunt Louise in the spring of 1922.
In the park near the palace, built on an ancient cemetery, the princesses devoted themselves to archeology and discovered some pottery, bronze pieces and bones.
During this period, Sophie and her sisters also participated, for the first time, in a number of great social events.
In March 1921, the princesses attended in Athens the wedding of their cousin Helen to Crown Prince Carol of Romania.
In July 1922, they visited the United Kingdom to be bridesmaids at the wedding of their uncle Louis Mountbatten to the wealthy heiress and aristocrat Edwina Ashley.
However, the military defeat of Greece against Turkey and the political unrest that it caused disrupted the life of Sophie and her family.
In September 1922, Constantine I abdicated in favor of his eldest son, George II.
A month later, Prince Andrew was arrested before being tried by a military tribunal, which declared him responsible for the defeat of the Sakarya.
Saved from execution by the intervention of foreign chancelleries, the prince was condemned to banishment and cashiering.
After a brief stop in Corfu, the prince and his relatives hurriedly left Greece aboard HMS Calypso in early December 1922.
Exile in France

After a journey of several weeks, which led them successively to Italy, France and the United Kingdom, Sophie, her parents and her siblings settled in Saint-Cloud in 1923.
Settled in a house adjoining that of Princess Marie Bonaparte, the family depended for seven years on her generosity, and two other aunts of Sophie: first Princess Anastasia and then Lady Louis Mountbatten.
Marie Bonaparte financed the studies of her nieces and nephew, while Lady Mountbatten gained the habit of offering her nieces her "used" clothes.
In fact, Sophie's parents had little income and the children were the regular witnesses to their money problems and their difficulty in maintaining a household.
Deprived of their Greek nationality after the proclamation of the Second Hellenic Republic in March 1924, Sophie and her family received Danish passports from their cousin King Christian X. In Saint-Cloud, the small group spent a relatively simple life.
Sophie and her siblings continued their studies in private institutions, and, during their free time, their father took them regularly to Paris or to the Bois de Boulogne.
Every Sunday, the family was received for lunch by Princess Marie Bonaparte and Prince George of Greece and Denmark.
Sophie and her family also regularly met Prince Nicholas of Greece and Denmark and his wife Elena Vladimirovna of Russia, who had also chosen France to spend their time in exile with their daughters.
Finally, they often saw their cousin Princess Margaret of Denmark, who settled in the Paris region after her marriage to Prince René of Bourbon-Parma.
Sophie and her relatives made frequent stays abroad, and in particular in the United Kingdom.
In 1923, the princess was invited to London to be a bridesmaid at the wedding of her aunt Louise Mountbatten to the future Gustav VI Adolf of Sweden.
Young adulthood

First marriage and settling in Germany

In 1927, Sophie met one of her distant cousins, Prince Philipp of Hesse-Kassel.
Shortly after, she met two of his brothers, the twins Christoph and Richard of Hesse-Kassel at Schloss Hemmelmark, the home of her great-aunt Princess Irene of Hesse and by Rhine.
Despite her being 13 years their junior, the two German princes soon attempted to court her and it was Christoph who managed to grab her attention.
Their romance eventually ended in an engagement, which was officially celebrated when Sophie turned 16, in 1930.
Around the same time, Cecilie, Sophie's favorite sister, became engaged to another member of the House of Hesse, Georg Donatus, Hereditary Grand Duke of Hesse.
The happiness of the princess was however clouded by the situation of her mother, whose mental health deteriorated sharply after the celebration of her silver wedding anniversary with Prince Andrew, in 1928.
Struck by a mental health crisis, the princess convinced herself that she possessed healing powers and that she was receiving divine messages about potential husbands for her daughters.
Distraught by the situation, Prince Andrew finally made the decision to place his wife in a sanatorium.
He took advantage of his family's stay in Darmstadt, on the occasion of the celebration for Cecilie's official engagement in April 1930, to send Alice to a psychiatric hospital located in Kreuzlingen, Switzerland.
In the absence of their mother, Sophie and Cecilie made their wedding preparations together.
The nuptials of Sophie and Christoph were celebrated in Kronberg im
They were married in two religious ceremonies, with the Orthodox one held at Friedrichshof Castle, owned by her mother-in-law Princess Margaret of Prussia, and the Lutheran one at a church in the city.
With their honeymoon over, Sophie and Christoph moved into an apartment in Berlin's Schöneberg quarter.
After working for a long time in the Maybach car factory in Friedrichshafen, the prince had just been hired as a broker by the Victoria insurance company.
While the princess moved to Germany to start a family, Greece went through a tumultuous political period, marked by numerous coups d'état.
Confronted with permanent instability, the population gradually lost confidence in the institutions of the Hellenic Republic and King George II (Sophie's cousin) was finally reinstalled on the throne in November 1935.
Family life and adherence to Nazism

In October 1930, Prince August Wilhelm of Prussia, son of Kaiser Wilhelm II, introduced his cousin Christoph to the politician Hermann Göring, and it did not take long for the two to form a closer relationship.
Under the influence of Göring, the prince and his wife then met Adolf Hitler, who deceived them with his charm and his apparent modesty.
Under these conditions, Christoph joined the Nazi Party, first secretly in 1931, and then publicly in 1933.
However, in his family, Christoph was not an exceptional case.
Subsequently, their respective twins, Princes Wolfgang and Richard of Hesse-Kassel, joined the party in 1932.
Finally, their parents, Frederick Charles, Landgrave of Hesse and Princess Margaret, followed the example of their sons in May 1938.
Unlike her sisters Cecilie and Margarita, who joined the Nazi Party at the same time as their husbands in 1937, Sophie never became a member of the Nazi Party.
Like her sisters-in-law, Princess Mafalda and Princess Marie Alexandra, she nevertheless joined the National Socialist Women's League in 1938.
In fact, Sophie had long shown enthusiasm for Nazi Germany.
Linked to the elite of the Hitler regime, the princess thus maintained friendly relations with Emmy Sonnemann, and was one of the guests of honor at the time of her marriage in April 1935 to Hermann Göring, who notably had Adolf Hitler as a witness.
From a financial point of view, the coming to power of Adolf Hitler significantly improved the situation of Christoph and Sophie.
In 1933, the prince was appointed personal advisor to State Secretary to the Prussian State Ministry Paul Körner.
Two years later, Göring placed Christoph in charge of the Forschungsamt, an intelligence service responsible for spying on the telecommunications of Nazi Germany.
Under these conditions, Sophie and her husband left their old apartment for a new one in 1933, before moving into a large red brick villa located in Dahlem in 1936.
At the same time as these events, Sophie and Christoph's family grew larger with the successive births of Christina (1933–2011), Dorothea (1934–2025), Karl (1937–2022), and Rainer of Hesse (born 1939).
Sophie also continued to worry about the fate of her mother Alice, whom she visited several times during the latter's confinement in Kreuzlingen between 1930 and 1933.
Sophie also happily attended the weddings of her two eldest sisters, Margarita and Theodora, to German princes Gottfried, Prince of Hohenlohe-Langenburg and Berthold, Margrave of Baden in 1931.
Sophie and Christoph also maintained their ties to their foreign relatives.
The princess made several visits to the United Kingdom, and also stayed in Italy (1936) and Yugoslavia (1939).
According to historian Jonathan Petropoulos, their travels were an opportunity for the couple to carry out, for the benefit of the Nazi Germany, a parallel diplomacy with their European cousins, such as Prince Paul of Yugoslavia and his wife Princess Olga of Greece and Denmark.
Second World War and the death of Prince Christoph

As a means of protection, Christoph warned Sophie about the need to beware of prying ears and never to speak politics with people other than her sisters and cousins.
Even though he probably moved away from the SS from 1934, the prince nonetheless remained a staunch supporter of the Nazi regime.
Sophie and her four children then left Berlin to settle in Friedrichshof, near her husband's parents the Landgrave and the Landgravine of Hesse.
Then began a close correspondence between the couple, which testified to the love that Sophie and her husband had for each other.
Shortly after Sophie moved to Kronberg im
Taunus on 28 May 1940, her father-in-law died in Wilhelmshöhe, making his eldest surviving son Philipp the new head of the House of Hesse-Kassel.
At the same time, most of Europe fell under Nazi rule and Sophie's parents found themselves isolated far from their children.
After the invasion of France, Prince Andrew was stuck on the French Riviera in June 1940.
For her part, Princess Alice chose to stay in Athens despite the occupation of Greece and the departure into exile of other members of the Greek royal family in April 1941.
This did not prevent Sophie from continuing to support the Nazi regime, as illustrated by the continuation of her visits to Emmy and Hermann Göring.
In January and October 1943, Princes Wolfgang and Richard of Hesse-Kassel were successively dismissed from the army, without being threatened by the Nazi regime.
At the same time, searches were carried out by Obergruppenführer Josias, Hereditary Prince of Waldeck and Pyrmont, in the residences of Philipp and his mother.
All these events led Sophie to open her eyes completely to the true nature of the Nazi regime.
The tragedies of the House of Hesse-Kassel did not end there, however.
On 7 October 1943, Prince Christoph died under mysterious circumstances during a plane crash in the Apennine Mountains, near Forlì.
A few months later, Princess Marie Alexandra of Baden (wife of Wolfgang) perished buried during an air-raid on Frankfurt am Main on 29–30 January 1944.
Widowed and pregnant with her fifth child (Princess Clarissa, who was born on 6 February 1944), Sophie therefore found herself in a precarious situation, with her mother-in-law, Landgravine Margaret as her main support.
Tired and emaciated, the princess was now responsible for bringing up her children on her own, while also taking care of Philipp and Mafalda's four children.
As Christoph's death was not made public by the Nazi regime, Sophie published a simple death notice for her husband in the Völkischer Beobachter on 18 October 1943.
A few weeks later, in November 1943, the princess and her mother-in-law received a visit from Obergruppenführer Siegfried Taubert, commissioned by Heinrich Himmler to discreetly spy on the family.
Aware of their vulnerability, the two women then refrained from expressing doubts about the conditions surrounding Christoph's death.
Eager to know more about the fate of Philipp and Mafalda, Sophie tried, on the other hand, to obtain information from Emmy Göring, without success.
At the same time, several relatives of the princess visited Friedrichshof, including her mother, Princess Alice, who managed to obtain a pass for Germany at the end of January 1944 and stayed with her daughter until April.
Other relatives, including her brother-in-law Wolfgang and their cousin Prince August Wilhelm of Prussia arrived at the castle in February 1945.
Post-war years

Occupation of Friedrichshof

The defeat of Germany and its occupation by the Allies affected the lives of Sophie and those close to her.
Before the arrival of the US Army, the Hesse-Kassels removed compromising documents, such as books of a political nature from their library.
In the days following the beginning of the occupation, the American intelligence services arrested Princes August Wilhelm of Prussia (7 April) and Wolfgang of Hesse (12 April).
With Landgravine Margaret suffering from pneumonia, Sophie found herself in the situation of having to represent her family alone before the authorities.
However, on 12 April, the American army ordered the evacuation of Friedrichshof, leaving to Hesse-Kassel family only the use of its dependencies.
Sophie and her mother-in-law had to find refuge with neighbors, and in particular with the parents of the future MP Walther Leisler Kiep.
While Friedrichshof was transformed into an officers' club by the American army, the Hesse-Kassels settled in Wolfsgarten in May, where they were received by Louis, Prince of Hesse and by Rhine and his wife Margaret Campbell Geddes, who soon took care of the younger children of Philipp, Landgrave of Hesse.
Deprived of her husband's property, which was placed in receivership until 1953, Sophie found herself in a very precarious financial situation.
Under these conditions, the death of her father Prince Andrew (who died in Monaco in December 1944) brought her a mediocre, but welcome inheritance.
Second marriage

Widowed since October 1943 and mother to five children, Sophie got close to Prince George William of Hanover, son of Ernest Augustus, Duke of Brunswick, and brother of Frederica, Queen of the Hellenes.
Encouraged by Princess Margaret of Hesse and by Rhine, their romance ended in an engagement, which was celebrated in January 1946.
As the House of Hanover was related to the British royal family, George William's father had previously sought permission from King George VI to proceed with the engagement.
As her wedding was scheduled for April, Sophie was trying to convince to the American authorities to allow her to use the jewelry she left in Friedrichshof and wished to wear during the ceremony.
Having obtained the necessary permit, the princess and Landgravine Margaret went to the castle, where they thought they would find the jewelry that Prince Wolfgang hid in the cellar in 1943.
To their dismay, however, the two women realized that the jewels had been stolen and an investigation was soon opened to find out what happened to them.
Under these conditions, the marriage of Sophie and George William took on a simpler form than expected.
Organized at Salem Castle, property of Berthold, Margrave of Baden (husband of Sophie's sister Theodora), the event was the occasion for the bride to reunite with her brother Prince Philip, whom she had not seen since 1937 and who came to Germany with his arms laden with food and gifts.
In the years that followed, Sophie gave birth to three more children: Welf Ernst (1947–1981), Georg (born 1949) and Friederike of Hanover (born 1954).
Philip's marriage

Since 1939, Sophie's brother Prince Philip had been linked to Princess Elizabeth of the United Kingdom.
Already in love, the two were unofficially engaged at Balmoral in 1946, and shortly after, Philip adopted British nationality.
However, the ties of Philip's family to Germany frightened the British court and government, who feared that the public could be reminded of the Germanic origins of the House of Windsor if the royal family were publicly associated with former Nazi Party members.
Prince Philip found himself unable to invite his sisters to his wedding.
Aware of the difficulties their brother had to face, Sophie, Margarita and Theodora nevertheless considered their sidelining wrong and hurtful.
Harassed by the press, who submitted requests for interviews with them, Sophie and her sisters spent the wedding day, 20 November 1947, at Marienburg Castle with their families.
Invited by Sophie's in-laws, Duke and Duchess of Brunswick, they celebrated the union of their brother in the company of their cousin Princess Elizabeth of Greece and Denmark and Prince Louis and Princess Margaret of Hesse and by Rhine.
A few days later, the Greek princesses received a visit from Prince George William's sister, the Queen of the Hellenes, who came to bring them a letter from their mother Princess Alice describing the wedding in detail; the queen was accompanied by the Duchess of Kent, widow of the bride's uncle.
Return to normal life

Settling in Salem

With George William having completed his law studies at the University of Göttingen in 1948, he was approached by his brother-in-law, Berthold, Margrave of Baden, to take over the management of the Salem Castle School, which had since been closed due to the Second World War.
A former student of the institution, the prince then went to Scotland with his wife to meet with Kurt Hahn, the founder of the school, and to visit Gordonstoun, the establishment that the latter founded when he had to flee Nazi Germany because of his Jewish origins.
For Sophie, who was very affected by the way she was treated at the time of her brother's wedding, this trip to the United Kingdom was an opportunity to discreetly reconnect with Prince Philip and Princess Elizabeth.
Once in Salem, George William and Sophie settled in a large house provided by the Margrave of Baden, and the children of the princess were educated in the institution run by George William.
In fact, the financial situation of Sophie and her husband remained precarious for a long time.
For the princess, however, things gradually improved from 1950, when she received a small inheritance from her maternal grandmother, the Dowager Marchioness of Milford Haven.
The conclusion in 1951 of the case of jewelry theft from the residence of Hesse-Kassels, and the end of the investigation into the role of Sophie's first husband Christoph in the Nazi regime in 1953 then helped to normalize her financial situation and that of her five elder children.
Sophie and her family remained in Salem until 1959, when George William gave up his post of school director.
In the meantime, the couple welcomed their nieces to their home, Princesses Sophia and Irene of Greece and Denmark, sent to Salem by their father, King Paul, to complete their studies.
Reintegration into royal circles

Once the monarchy was restored in Greece in 1946, Sophie was invited to Athens by her mother, Princess Alice, some time later, in 1948.
In the years that followed, Sophie and George William got closer to their brother-in-law, King Paul of Greece, and to his family.
Queen Frederica thus came to consider Sophie as her best friend.
As a result, the princess and her husband were regularly welcomed at the Greek Court, and the couple was among the many personalities invited by the Greek sovereign to the "Cruise of the Kings" in 1954.
Sophie and her family were also invited to Athens on the occasion of the wedding of Princess Sophia of Greece and Denmark and Juan Carlos, Prince of Asturias in 1962.
They were also present at the wedding of King Constantine II of Greece and Princess Anne-Marie of Denmark in 1964.
In the early 1950s, relations between the British royal family and their German relatives in turn normalized, and Sophie, her sisters and their husbands were all invited to the coronation of Elizabeth II in 1953.
The princesses and their families were then frequently invited to Buckingham Palace and Sandringham House.
In 1964, Sophie was chosen as godmother to her nephew Prince Edward.
In 1978, she attended the wedding of Prince Michael of Kent (son of her cousin Princess Marina of Greece and Denmark) and Baroness Marie Christine von Reibnitz.
In 1997, she was invited, with her husband, to the celebrations for the golden wedding anniversary of Queen Elizabeth II and Prince Philip.
Over the years, Sophie also developed a special relationship with Prince Charles (later King Charles III), who received her on several occasions at his Highgrove residence.
Family losses

In 1958, Sophie and George William bought a large chalet located in Schliersee, Bavaria.
Well integrated with the local population, the couple led a relatively simple and discreet life in the village.
When she was not taking care of her children, Sophie would devote herself to gardening, reading and listening to music while her husband went about his professional tasks.
In the same years, the elder children of the princess formed their own families.
Princess Christina was the first of Sophie's eight children to marry, in 1956.
Princess Dorothea married Prince Friedrich of Windisch-Graetz at Schliersee in March 1959.
Over the years, Princess Alice's state of health became a source of concern for Sophie and her family.
Despite repeated requests from her children and her advancing age, she refused to move abroad and continued to live almost alone in Athens most of the year.
After the establishment of the Regime of the Colonels in 1967, however, Sophie went to the Hellenic capital to persuade her mother to leave Greece and settle in the United Kingdom, which she finally agreed to do.
Two years later, in 1969, Alice died at Buckingham Palace and Sophie and her family traveled to London to attend her funeral.
Struck by these successive losses, Sophie accompanied, in the weeks that followed, her sister-in-law, Queen Frederica and her niece Princess Irene on a spiritual journey to India.
A long legal battle ensued, during which Sophie and George William challenged their daughter-in-law, Wibke van Gunsteren, to win the custody of their granddaughter, Princess Saskia of Hanover, who was finally entrusted to her aunt Princess Christina.
Final years

In 1988, Sophie had the satisfaction of making her mother's last wishes come true by transferring her remains to the Church of Mary Magdalene, on the Mount of Olives, in Jerusalem.
A few years later, in 1993, the Yad Vashem Memorial honored Princess Alice as "Righteous Among the Nations" for supporting a Jewish family during the Second World War.
Sophie and Philip, her last surviving children since Margarita's death in 1981, were invited to the Israeli capital in 1994, for a ceremony in honor of their mother.
As the Spanish historian Ricardo Mateos Sainz de Medrano pointed out, there was a certain irony here, considering Sophie's past links to the Nazi regime.
The year 1994 also brought the accidental death of one of Sophie's grandsons, Prince Christopher of Yugoslavia.
A science teacher at a high school in Bowmore, Scotland, the 34-year-old prince died when he was hit by a car on his way home on his bicycle.
Informed by the Duke of Edinburgh while staying in the UK, Sophie was shocked by the news.
The princess spent the last months of her life in a nursing home in Schliersee, where she died on 24 November 2001 and was survived by her husband, seven children, fourteen grandchildren and fourteen great-grandchildren.
In popular culture

Documentaries

Prince Karl of Hesse briefly discusses his mother's childhood and her ties to the Nazi regime in a documentary about his uncle, Prince Philip:
In the same documentary, it is mentioned that Princess Sophie is the author of an as of yet unpublished memoir.
Princess Sophie is also mentioned in episode 6 ("Hesse Jewels") of the second season of the documentary series Daring Capers (2001).
Film and television

Sophie features as a character in the 2009 Belgian pseudo-film noir The Hessen Affair (The Hessen Conspiracy on DVD), the plot of which centers around the theft of her jewels and the entirely fictional post-1871 Imperial German crown jewels from Kronberg Castle.
Sophie is briefly portrayed by actress Eliza Sodró in the episode "Paterfamilias" of the second season of the television series The Crown (2017).
Ancestry

Notes and references

Notes

References

Bibliography

On Sophie

Press articles devoted to Sophie

On Sophie and the Greek royal family

On Sophie and the princely family of Hesse-Kassel

Biographies of Sophie's relatives



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
  AssignClass (c7dac8e6-4558-4fdf-8ca2-820348301abd)
 Call ID: c7dac8e6-4558-4fdf-8ca2-820348301abd
  Args:
    source: Princess_Sophie_of_Greece_and_Denmark
    type: :Woman
  AssignClass (15180e53-59eb-4e23-9070-706836b26546)
 Call ID: 15180e53-59eb-4e23-9070-706836b26546
  Args:
    source: Princess_Sophie_of_Greece_and_Denmark
    type: :Person
  AddLiteral (c99e9d96-5d74-4491-90ad-42e1d5a9c4b5)
 Call ID: c99e9d96-5d74-4491-90ad-42e1d5a9c4b5
  Args:
    source: Princess_Sophie_of_Greece_and_Denmark
    literal_value: 1914
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (4b90ee92-b7cd-422f-86c0-0c2f7ce8d1db)
 Call ID: 4b90ee92-b7cd-422f-86c0-0c2f7ce8d1db
  Args:
    literal_value: 2001
    source: Princess_Sophie_of_Greece_and_Denmark
    literal_type: xsd:integer
    relation: :hasDeathYear
  AssignClass (03b5b34c-b67a-4522-8654-ededb8bbb7f2)
 Call ID: 03b5b34c-b67a-4522-8654-ededb8bbb7f2
  Args:
    source: Prince_Andrew_of_Greece_and_Denmark
    type: :Man
  AssignClass (2e6c31c3-6b76-4cae-807a-6d721870edbb)
 Call ID: 2e6c31c3-6b76-4cae-807a-6d721870edbb
  Args:
    type: :Person
    source: Prince_Andrew_of_Greece_and_Denmark
  AssignClass (ced5b848-6a49-4195-aac8-47c3f4f36fca)
 Call ID: ced5b848-6a49-4195-aac8-47c3f4f36fca
  Args:
    type: :Woman
    source: Princess_Alice_of_Battenberg
  AssignClass (f7b0cf12-1add-49c7-a323-364d64ff2ef0)
 Call ID: f7b0cf12-1add-49c7-a323-364d64ff2ef0
  Args:
    source: Princess_Alice_of_Battenberg
    type: :Person
  AddTriple (f464cc97-bc3b-445b-8960-01f8c53b135e)
 Call ID: f464cc97-bc3b-445b-8960-01f8c53b135e
  Args:
    target: Prince_Andrew_of_Greece_and_Denmark
    relation: :hasFather
    source: Princess_Sophie_of_Greece_and_Denmark
  AddTriple (7646aac3-9491-417e-80a4-4ef10810cf62)
 Call ID: 7646aac3-9491-417e-80a4-4ef10810cf62
  Args:
    target: Princess_Alice_of_Battenberg
    relation: :hasMother
    source: Princess_Sophie_of_Greece_and_Denmark
  AssignClass (1267f3a2-4733-48e7-b8cd-26a5de0d7073)
 Call ID: 1267f3a2-4733-48e7-b8cd-26a5de0d7073
  Args:
    type: :Man
    source: Prince_Christoph_of_Hesse
  AssignClass (bbf09941-fa42-4592-9f25-3f97c802bac3)
 Call ID: bbf09941-fa42-4592-9f25-3f97c802bac3
  Args:
    source: Prince_Christoph_of_Hesse
    type: :Person
  AddLiteral (4f6ba8f4-7c07-4514-b7ec-abdcaf55569a)
 Call ID: 4f6ba8f4-7c07-4514-b7ec-abdcaf55569a
  Args:
    literal_value: 1930
    source: Princess_Sophie_of_Greece_and_Denmark
    relation: :hasMarriageYear
    literal_type: xsd:integer
  AddTriple (91bed57c-32c6-4ed3-beb8-a1b0369702d1)
 Call ID: 91bed57c-32c6-4ed3-beb8-a1b0369702d1
  Args:
    target: Prince_Christoph_of_Hesse
    source: Princess_Sophie_of_Greece_and_Denmark
    relation: :hasRelation
  AssignClass (793462f5-cfee-4a1a-89e6-b5d44abb8224)
 Call ID: 793462f5-cfee-4a1a-89e6-b5d44abb8224
  Args:
    type: :Man
    source: Prince_George_William_of_Hanover
  AssignClass (eb2628b3-e7c9-4aad-9bfe-9963f4a99093)
 Call ID: eb2628b3-e7c9-4aad-9bfe-9963f4a99093
  Args:
    type: :Person
    source: Prince_George_William_of_Hanover
  AddLiteral (ad934454-33c7-43dd-a4d3-a0c22cfa4705)
 Call ID: ad934454-33c7-43dd-a4d3-a0c22cfa4705
  Args:
    literal_value: 1946
    source: Princess_Sophie_of_Greece_and_Denmark
    relation: :hasMarriageYear
    literal_type: xsd:integer
  AddTriple (8e030bc5-ea0b-4e6a-8fb4-3f692d9e4d52)
 Call ID: 8e030bc5-ea0b-4e6a-8fb4-3f692d9e4d52
  Args:
    source: Princess_Sophie_of_Greece_and_Denmark
    relation: :hasRelation
    target: Prince_George_William_of_Hanover
  AssignClass (39bc22d5-fef8-42cc-963c-a2457434760f)
 Call ID: 39bc22d5-fef8-42cc-963c-a2457434760f
  Args:
    source: Prince_Philip_Duke_of_Edinburgh
    type: :Man
  AssignClass (f5835198-fae4-4aa0-9ea6-5174b903e6bb)
 Call ID: f5835198-fae4-4aa0-9ea6-5174b903e6bb
  Args:
    type: :Person
    source: Prince_Philip_Duke_of_Edinburgh
  AddTriple (1d03ebfc-894c-4d72-a67e-5055b9031eee)
 Call ID: 1d03ebfc-894c-4d72-a67e-5055b9031eee
  Args:
    source: Prince_Philip_Duke_of_Edinburgh
    relation: :hasSister
    target: Princess_Sophie_of_Greece_and_Denmark
  AssignClass (d539dca3-5d4e-4a53-a99e-ff7a61a8643d)
 Call ID: d539dca3-5d4e-4a53-a99e-ff7a61a8643d
  Args:
    type: :Woman
    source: Margarita_of_Greece_and_Denmark
  AssignClass (6c91e34a-7465-4584-bb8a-212fa2c8269e)
 Call ID: 6c91e34a-7465-4584-bb8a-212fa2c8269e
  Args:
    type: :Person
    source: Margarita_of_Greece_and_Denmark
  AssignClass (f84d22de-1379-470a-8c47-f778650ce6e1)
 Call ID: f84d22de-1379-470a-8c47-f778650ce6e1
  Args:
    type: :Woman
    source: Theodora_of_Greece_and_Denmark
  AssignClass (38ab038f-daf2-4b0d-bb73-906a03db5c19)
 Call ID: 38ab038f-daf2-4b0d-bb73-906a03db5c19
  Args:
    type: :Person
    source: Theodora_of_Greece_and_Denmark
  AssignClass (08479fa1-2d63-4043-97bc-8b094d513ddb)
 Call ID: 08479fa1-2d63-4043-97bc-8b094d513ddb
  Args:
    source: Cecilie_of_Greece_and_Denmark
    type: :Woman
  AssignClass (5359f1fe-6e1d-4f84-9baf-6a716484ea7d)
 Call ID: 5359f1fe-6e1d-4f84-9baf-6a716484ea7d
  Args:
    type: :Person
    source: Cecilie_of_Greece_and_Denmark
  AddTriple (ead8c051-b609-45ce-aee8-edef0863e8d1)
 Call ID: ead8c051-b609-45ce-aee8-edef0863e8d1
  Args:
    target: Margarita_of_Greece_and_Denmark
    relation: :hasSister
    source: Princess_Sophie_of_Greece_and_Denmark
  AddTriple (72734745-07ef-41d0-b072-f4879204d751)
 Call ID: 72734745-07ef-41d0-b072-f4879204d751
  Args:
    relation: :hasSister
    source: Princess_Sophie_of_Greece_and_Denmark
    target: Theodora_of_Greece_and_Denmark
  AddTriple (13e48651-dd10-4210-a792-86b7e7a12a0e)
 Call ID: 13e48651-dd10-4210-a792-86b7e7a12a0e
  Args:
    target: Cecilie_of_Greece_and_Denmark
    relation: :hasSister
    source: Princess_Sophie_of_Greece_and_Denmark
  Finish (c1e8085b-d5f7-43e9-a369-f619563376a9)
 Call ID: c1e8085b-d5f7-43e9-a369-f619563376a9
  Args: