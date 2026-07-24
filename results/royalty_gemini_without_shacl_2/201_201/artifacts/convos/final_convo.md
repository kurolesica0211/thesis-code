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
Wilhelm II (Friedrich Wilhelm Viktor Albert; 27 January 1859 – 4 June 1941) was the last German Emperor from 1888 until his abdication in 1918.
Born during the reign of his granduncle Frederick William IV of Prussia, Wilhelm was the son of Prince Frederick William and Victoria, Princess Royal.
Through his mother, he was the eldest of the 42 grandchildren of Queen Victoria of the United Kingdom.
In March 1888, Wilhelm's father, Frederick William, ascended the German and Prussian thrones as Frederick III.
Frederick died just 99 days later, and his son succeeded him as Kaiser Wilhelm II.
However, Wilhelm often undermined such progress by making tactless and threatening statements towards other countries without first consulting his ministers.
Likewise, he and his government did much to alienate the German Empire from most of Europe by initiating a massive naval build-up, contesting French control of Morocco, backing Austria-Hungary's annexation of Bosnia and threatening Britain's access to the Persian Gulf by  building a railway through Baghdad.
Despite strengthening Germany's position as a great power in the short term by building a powerful navy and promoting scientific innovation within its borders, Wilhelm II's erratic foreign policy greatly antagonized the international community and is considered by many to have led to the fall of the German Empire.
A lax wartime leader, Wilhelm left virtually all decisions regarding strategy and organisation of the war effort to the German Supreme Army Command.
Losing the support of his country's military and many of his subjects, Wilhelm was forced to abdicate during the German Revolution of 1918–1919 which converted Germany into an unstable democratic state known as the Weimar Republic.
Wilhelm subsequently fled to exile in the Netherlands, where he remained during its occupation by Nazi Germany in 1940 before dying there in 1941.
Early life

Wilhelm was born in Berlin on 27 January 1859—at the Crown Prince's Palace—to Victoria, Princess Royal ("Vicky") and Prince Frederick William of Prussia ("Fritz", the future Frederick III).
His mother, Vicky, was the eldest child of Queen Victoria of the United Kingdom.
At the time of Wilhelm's birth, his granduncle Frederick William IV was king of Prussia.
Frederick William IV had been left permanently incapacitated by a series of strokes, and his younger brother Wilhelm, the young prince's grandfather, was acting as regent.
Prince Wilhelm was the oldest of the 42 grandchildren of his maternal grandparents (Queen Victoria and Prince Albert).
Upon the death of Frederick William IV in January 1861, Wilhelm's namesake grandfather became king, and the two-year-old Wilhelm became second in the line of succession to the Prussian throne.
After 1871, Wilhelm also became second in the line to the newly created German Empire, which, according to the constitution of the German Empire, was ruled by the Prussian king.
Traumatic birth

Shortly before midnight on 26 January 1859, Princess Vicky experienced labour pains, followed by her water breaking, after which August Wegner, the family's personal physician, was summoned.
Modern medical assessments have concluded Wilhelm's hypoxic state at birth, due to the breech delivery and the heavy dosage of chloroform, left him with minimal to mild brain damage, which manifested itself in his subsequent hyperactive and erratic behaviour, limited attention span and impaired social abilities.
The brachial plexus injury resulted in Erb's palsy, which left Wilhelm with a withered left arm about six inches (15 centimetres) shorter than his right.
Early years

In 1863, Wilhelm was taken to England to be present at the wedding of his uncle Bertie and Princess Alexandra of Denmark (later King Edward VII and Queen Alexandra).
Wilhelm attended the ceremony in a Highland costume, complete with a small toy dirk.
His 18-year-old uncle Prince Alfred, charged with keeping an eye on him, told him to be quiet, but Wilhelm drew his dirk and threatened Alfred.
When Alfred attempted to subdue him by force, Wilhelm bit him on the leg.
His grandmother, Queen Victoria, missed seeing the fracas; to her Wilhelm remained "a clever, dear, good little child, the great favourite of my beloved Vicky".
The thought that Wilhelm, as heir to the throne, should not be able to ride was intolerable to her.
Riding lessons began when Wilhelm was eight and were a matter of endurance for him.
Wilhelm, from six years of age, was tutored and heavily influenced by the 39-year-old teacher Georg Ernst Hinzpeter.
"


As a teenager, Wilhelm was educated at Kassel at the Friedrichsgymnasium.
In January 1877, Wilhelm finished high school and on his eighteenth birthday received as a present from his grandmother the Order of the Garter.
Wilhelm possessed a quick intelligence, but this was often overshadowed by a cantankerous temper.
As a scion of the royal house of Hohenzollern, Wilhelm was exposed from an early age to the military society of the Prussian aristocracy.
This had a major impact on him, and in maturity Wilhelm was seldom seen out of uniform.
The hyper-masculine military culture of Prussia in this period did much to frame his political ideals and personal relationships.
Wilhelm was in awe of his father, whose status as a hero of the wars of unification was largely responsible for the young Wilhelm's attitude, as were the circumstances in which he was raised; close emotional contact between father and son was not encouraged.
Later, as he came into contact with the Crown Prince's political opponents, Wilhelm came to adopt more ambivalent feelings toward his father, perceiving the influence of Wilhelm's mother over a figure who should have been possessed of masculine independence and strength.
Wilhelm also idolised his grandfather, Wilhelm I, and he was instrumental in later attempts to foster a cult of the first German Emperor as "Wilhelm the Great".
Wilhelm resisted attempts by his parents, especially his mother, to educate him in a spirit of British liberalism.
The German Emperor, Wilhelm I, watched as his grandson, guided principally by the Crown Princess Victoria, grew to manhood.
When Wilhelm was nearing 21, the Emperor decided it was time his grandson should begin the military phase of his preparation for the throne.
"In the Guards," Wilhelm said, "I really found my family, my friends, my interests—everything of which I had up to that time had to do without."
When Wilhelm was in his early twenties, Chancellor Otto von Bismarck tried to separate him from his parents, who opposed Bismarck and his policies, with some success.
Bismarck planned to use the young prince as a weapon against his parents in order to retain his own political dominance.
Wilhelm thus developed a dysfunctional relationship with his parents, but especially with his English mother.
In an outburst in April 1889, Wilhelm angrily implied that "an English doctor killed my father, and an English doctor crippled my arm—which is the fault of my mother", who allowed no German physicians to attend to herself or her immediate family.
As a young man, Wilhelm fell in love with one of his maternal first cousins, Princess Elisabeth of Hesse-Darmstadt.
In 1880 Wilhelm became engaged to Princess Augusta Victoria of Schleswig-Holstein, known as "Dona".
Between 1882 and 1892, Augusta bore Wilhelm seven children, six sons and a daughter.
Beginning in 1884, Bismarck began advocating that Kaiser Wilhelm send his grandson on diplomatic missions, a privilege denied to the Crown Prince.
That year, Prince Wilhelm was sent to the court of Tsar Alexander III of Russia in St. Petersburg to attend the coming-of-age ceremony of the 16-year-old Tsarevich Nicholas.
Wilhelm's behaviour did little to ingratiate himself to the tsar.
Two years later, Kaiser Wilhelm I took Prince Wilhelm on a trip to meet with Emperor Franz Joseph I of Austria-Hungary.
In 1886, also, thanks to Herbert von Bismarck, the son of the Chancellor, Prince Wilhelm began to be trained twice a week at the Foreign Ministry.
Accession

Kaiser Wilhelm I died in Berlin on 9 March 1888, and Prince Wilhelm's father ascended the throne as Frederick III.
On 15 June of that same year, his 29-year-old son succeeded him as German Emperor and King of Prussia.
Although in his youth he had been a great admirer of Otto von Bismarck, Wilhelm's characteristic impatience soon brought him into conflict with the "Iron Chancellor", the dominant figure in the foundation of his empire.
While the imperial constitution vested executive power in the monarch, Wilhelm I had been content to leave day-to-day administration to Bismarck.
Early conflicts between Wilhelm II and his chancellor soon poisoned the relationship between the two men.
Bismarck had believed that Wilhelm was a lightweight who could be dominated, and he showed escalating disrespect for Wilhelm's favored policy objectives in the late 1880s.
The final split between monarch and statesman occurred soon after an attempt by Bismarck to implement far-reaching anti-Socialist laws in early 1890.
They favoured making the anti-Socialist laws permanent, with one exception: giving the German police the power, similarly to the Tsarist Okhrana, to expel alleged Socialist agitators from their homes by decree and into internal exile.
As the debate continued, Wilhelm became more and more interested in the social problems being exploited in the propaganda of the Socialists, especially the treatment of mine workers who went on strike in 1889.
Bismarck, in turn, sharply disagreed with Wilhelm's pro-labor union policies and worked to circumvent them.
The final break between the Iron Chancellor and the Kaiser came when Bismarck initiated discussions with the opposition to form a new parliamentary majority without consulting with Wilhelm first.
The Kartell, the shifting coalition government that Bismarck had been able to maintain since 1867, had finally lost its majority of seats in the Reichstag due to the Anti-Socialist Laws fiasco.
In most parliamentary systems, the head of government depends upon the confidence of the parliamentary majority and has the right to form coalitions to maintain a majority of supporters.
After a heated argument at Bismarck's estate over the latter's alleged disrespect for the Imperial Family, Wilhelm stormed out.
In later years, Bismarck created the "Bismarck myth"; the view (which some historians have argued was confirmed by subsequent events) that Wilhelm II's successful demand for Bismarck's resignation destroyed any chance Imperial Germany ever had of stable government and international peace.
According to this view, what Wilhelm termed "The New Course" is characterised as Germany's ship of state going dangerously off course, leading directly to the carnage of the First and Second World Wars.
In interviews with C.L. Sulzberger for the book The Fall of Eagles, Prince Louis Ferdinand of Prussia, grandson and heir of Kaiser Wilhelm II, further commented, "Bismarck was certainly our greatest statesman, but he had very bad manners and he became increasingly overbearing with age.
"


Wilhelm in control

The New Course

Bismarck was succeeded as Chancellor of Germany and Minister-President of Prussia by Leo von Caprivi.
At the opening of the Reichstag on 6 May 1890, the Kaiser stated that the most pressing issue was the further enlargement of the bill concerning the protection of the labourer.
Following the dismissal of Hohenlohe in 1900, Wilhelm appointed the man whom he regarded as "his own Bismarck", Bernhard von Bülow.
In appointing Caprivi and then Hohenlohe, Wilhelm was embarking upon what is known to history as "the New Course", in which he hoped to exert decisive influence in the government of the empire.
There is debate amongst historians as to the precise degree to which Wilhelm succeeded in implementing "personal rule" in this era, but what is clear is the very different dynamic which existed between the Crown and its chief political servant (the Chancellor) in the "Wilhelmine Era".
Wilhelm wanted to preclude the emergence of another Iron Chancellor, whom he ultimately detested as being "a boorish old killjoy" who had not permitted any minister to see the Emperor except in his presence, keeping a stranglehold on effective political power.
Upon his enforced retirement and until his dying day, Bismarck became a bitter critic of Wilhelm's policies, but without gaining the support of a majority within the Reichstag there was little chance of Bismarck exerting a decisive influence on policy.
In the early twentieth century, Wilhelm began to concentrate upon his real agenda: the creation of a German Navy that would rival that of Britain and enable Germany to declare itself a world power.
Bülow and Bethmann Hollweg, his loyal chancellors, looked after domestic affairs, while Wilhelm obliviously began to spread alarm in the chancelleries of Europe with his increasingly eccentric and ill-advised statements on foreign affairs.
Promoter of arts and sciences

Wilhelm enthusiastically promoted the arts and sciences, as well as public education and social welfare.
He sponsored the Kaiser Wilhelm Society for the promotion of scientific research; it was funded by wealthy private donors and by the state and comprised a number of research institutes in both pure and applied sciences.
Wilhelm supported the modernisers as they tried to reform the Prussian system of secondary education, which was rigidly traditional, elitist, politically authoritarian, and unchanged by the progress in the natural sciences.
Wilhelm continued as Protector of the Order even after 1918, as the position was in essence attached to the head of the House of Hohenzollern.
Personality

Historians have frequently stressed the role of Wilhelm's personality in shaping his reign.
Thus, Thomas Nipperdey concludes he was:


...gifted, with a quick understanding, sometimes brilliant, with a taste for the modern,—technology, industry, science—but at the same time superficial, hasty, restless, unable to relax, without any deeper level of seriousness, without any desire for hard work or drive to see things through to the end, without any sense of sobriety, for balance and boundaries, or even for reality and real problems, uncontrollable and scarcely capable of learning from experience, desperate for applause and success,—as Bismarck said early on in his life, he wanted every day to be his birthday—romantic, sentimental and theatrical, unsure and arrogant, with an immeasurably exaggerated self-confidence and desire to show off, a juvenile cadet, who never took the tone of the officers' mess out of his voice, and brashly wanted to play the part of the supreme warlord, full of panicky fear of a monotonous life without any diversions, and yet aimless, pathological in his hatred against his English mother.
Historian David Fromkin states that Wilhelm had a love–hate relationship with Britain.
Langer et al. (1968) emphasise the negative international consequences of Wilhelm's erratic personality:
"He believed in force, and the 'survival of the fittest' in domestic as well as foreign politics ...
Relationships with foreign relatives

As a grandchild of Queen Victoria, Wilhelm was a first cousin of King George V of the United Kingdom, as well as of queens Marie of Romania, Maud of Norway, Victoria Eugenie of Spain and Empress Alexandra of Russia.
In 1889, Wilhelm's younger sister Sophia married Constantine, Crown Prince of Greece.
Wilhelm was infuriated by his sister's conversion from Lutheranism to Greek Orthodoxy; upon her marriage, he attempted to ban her from entering Germany.
Wilhelm's most contentious relationships were with his British relations.
He craved the acceptance of his grandmother, Queen Victoria, and of the rest of her family.
Between 1888 and 1901, Wilhelm resented Bertie, who despite being the heir apparent to the British throne, treated Wilhelm not as a reigning monarch, but merely as another nephew.
In turn, Wilhelm often snubbed his uncle, whom he referred to as "the old peacock" and lorded his position as emperor over him.
Beginning in the 1890s, Wilhelm made visits to England for Cowes Week on the Isle of Wight and often competed against his uncle in the yacht races.
Bertie's wife, Alexandra, also disliked Wilhelm.
Even though Wilhelm had not been on the throne at the time, Alexandra felt anger over the Prussian seizure of Schleswig-Holstein from her native Denmark in the 1860s, and was also annoyed over Wilhelm's treatment of his mother.
Despite his poor relations with his English relatives, when he received news that Queen Victoria was dying at Osborne House in January 1901, Wilhelm travelled to England and was at her bedside when she died, and he remained for the funeral.
In 1913, Wilhelm hosted a lavish wedding in Berlin for his only daughter, Victoria Louise.
Among the guests at the wedding were his cousins Tsar Nicholas II of Russia and King George V of the United Kingdom, and George's wife, Queen Mary.


Foreign affairs

German foreign policy under Wilhelm II was faced with a number of significant problems.
Perhaps the most apparent was that Wilhelm was an impatient man, subjective in his reactions and affected strongly by sentiment and impulse.
There were a number of examples, such as the Kruger telegram of 1896 in which Wilhelm congratulated President Paul Kruger for preventing the Transvaal Republic from being annexed by the British Empire during the Jameson Raid.
During the First World War, he became the central target of British anti-German propaganda and the personification of a hated enemy.
Wilhelm exploited fears of a yellow peril trying to interest other European rulers in the perils they faced by invading China; few other leaders paid attention.
Wilhelm also used the Japanese victory in the Russo-Japanese War to try to incite fear in the west of the yellow peril that they faced by a resurgent Imperial Japan, which Wilhelm claimed would ally with China to overrun the conventional European Powers.
Wilhelm also invested in strengthening the German colonial empire in Africa and the Pacific, but few became profitable and all were lost during the First World War.
In South West Africa (now Namibia), a native revolt against German rule led to the Herero and Nama genocide, although Wilhelm eventually ordered it to be stopped and recalled its mastermind General Lothar von Trotha.
One of the few times when Wilhelm succeeded in personal diplomacy was when in 1900, he supported the morganatic marriage of Archduke Franz Ferdinand of Austria to Countess Sophie Chotek, and helped negotiate an end to the opposition to the wedding by Emperor Franz Joseph I of Austria.
A domestic triumph for Wilhelm was when his daughter Victoria Louise married the Duke of Brunswick in 1913; this helped heal the rift between the House of Hanover and the House of Hohenzollern that had followed Bismarck's invasion and annexation of the Kingdom of Hanover in 1866.
Political visits to the Ottoman Empire

In his first visit to Constantinople in 1889, Wilhelm secured the sale of German-made rifles to the Ottoman Army.
Deeply moved by this imposing spectacle, and likewise by the consciousness of standing on the spot where held sway one of the most chivalrous rulers of all times, the great Sultan Saladin, a knight sans peur et sans reproche, who often taught his adversaries the right conception of knighthood, I seize with joy the opportunity to render thanks, above all to the Sultan Abdul Hamid for his hospitality.
— Kaiser Wilhelm II, 

On 10 November, Wilhelm went to visit Baalbek before heading to Beirut to board his ship back home on 12 November.
In his second visit, Wilhelm secured a promise for German companies to construct the Berlin–Baghdad railway, and had the German Fountain constructed in Constantinople to commemorate his journey.
Hun speech of 1900

The Boxer Rebellion, an anti-foreign uprising in China, was put down in 1900 by an international force known as the Eight-Nation Alliance.
Wilhelm's fiery rhetoric clearly expressed his vision for Germany as one of the great powers.
The term "Hun" later became the favoured epithet of Allied anti-German war propaganda during the First World War.
Assassination attempt

On 6 March 1901, during a visit to Bremen, in an apparent assassination attempt Wilhelm was struck in the face by a sharp iron object thrown at him.
"


Eulenberg Scandal

In the years 1906–1909, Socialist journalist Maximilian Harden published accusations of homosexual activity involving ministers, courtiers, army officers, and Wilhelm's closest friend and advisor, Prince Philipp zu Eulenberg.
Harden, like some in the upper echelons of the military and Foreign Office, resented Eulenberg's approval of the Anglo-French Entente, and also his encouragement of Wilhelm to rule personally.
The scandal led to Wilhelm experiencing a nervous breakdown, and the removal of Eulenberg and others of his circle from the court.
The view that Wilhelm was a deeply repressed homosexual is increasingly supported by scholars: certainly, he never came to terms with his feelings for Eulenberg.
Historians have linked the Eulenberg scandal to a fundamental shift in German policy that heightened its military aggressiveness and ultimately contributed to World War I.


Moroccan Crisis

One of Wilhelm's diplomatic blunders sparked the Moroccan Crisis of 1905.
Wilhelm had viewed the article, which was based on discussions he had had with Colonel Edward Stuart-Wortley in 1907, as an opportunity to promote his views on Anglo-German friendship, but due to the content and emotional tone of many of his statements, he ended up further alienating not only the British but also the French, Russians and Japanese.
The Daily Telegraph crisis deeply wounded Wilhelm's previously unimpaired self-confidence, and he experienced a severe bout of depression.
He kept a low profile for many months after the scandal broke, although in July 1909 he took the opportunity to force the resignation of the chancellor, Prince von Bülow, whose defence of him in the Reichstag had been aimed primarily at shifting blame from himself for not stopping the publication of the article.
As a result of the scandal, Wilhelm had less influence in domestic and foreign policy for the remainder of his reign than he had previously exercised.
Naval arms race with Britain

Nothing Wilhelm did in the international arena was of more influence than his decision to pursue a policy of massive naval construction.
A powerful navy was Wilhelm's pet project.
He had inherited from his mother a love of the British Royal Navy, which was at that time the world's largest.
He once confided to his uncle, the Prince of Wales, that his dream was to have a "fleet of my own some day".
Wilhelm's frustration over his fleet's poor showing at the Fleet Review at his grandmother's Diamond Jubilee celebrations, combined with his inability to exert German influence in South Africa following the dispatch of the Kruger telegram, led to Wilhelm taking definitive steps toward the construction of a fleet to rival that of his British cousins.
Wilhelm called on the services of the dynamic naval officer Alfred von Tirpitz, whom he appointed to the head of the Imperial Naval Office in 1897.
Tirpitz enjoyed Wilhelm's full support in his advocacy of successive naval bills of 1897 and 1900, by which the German navy was built up to contend with that of the British Empire.
Naval expansion under the Fleet Acts eventually led to severe financial strains in Germany by 1914, as by 1906 Wilhelm had committed his navy to construction of the much larger, more expensive dreadnought type of battleship.
The British depended on naval superiority and its response was to make Germany its most feared enemy.
In 1889 Wilhelm reorganised top-level control of the navy by creating a Naval Cabinet (Marine-Kabinett) equivalent to the German Imperial Military Cabinet which had previously functioned in the same capacity for both the army and navy.
Each of these three heads of department reported separately to Wilhelm.
World War I

Historians typically argue that Wilhelm was largely confined to ceremonial duties during the war—there were innumerable parades to review and honours to award.
"


The Sarajevo crisis

Wilhelm was a friend of Franz Ferdinand, and he was deeply shocked by his assassination on 28 June 1914.
Wilhelm offered to support Austria-Hungary in crushing the Black Hand, the secret organisation that had plotted the killing, and even sanctioned the use of force by Austria against the perceived source of the movement—Serbia (this is often called "the blank cheque").
Wilhelm made erratic attempts to stay on top of the crisis via telegram, and when the Austro-Hungarian ultimatum was delivered to Serbia, he hurried back to Berlin.
July 1914


On the night of 30 July 1914, when handed a document stating that Russia would not cancel its mobilisation, Wilhelm wrote a lengthy commentary containing these observations:
More recent British authors state that Wilhelm II really declared, "Ruthlessness and weakness will start the most terrifying war of the world, whose purpose is to destroy Germany.
When it became clear that Germany would experience a war on two fronts and that Britain would enter the war if Germany attacked France through neutral Belgium, the panic-stricken Wilhelm attempted to redirect the main attack against Russia.
When Helmuth von Moltke (the younger) (who had chosen the old plan from 1905, made by General von Schlieffen for the possibility of German war on two fronts) told him that this was impossible, Wilhelm said: "Your uncle would have given me a different answer!"
Wilhelm is also reported to have said, "To think that George and Nicky should have played me false!
Defeating France had been easy for Prussia in the Franco-Prussian War in 1870.
However, Wilhelm II stopped any invasion of the Netherlands.
Early War

On 1 August 1914 (Saturday), Wilhelm II made a war speech in front of a great crowd.
On 19 August 1914, Wilhelm II predicted that Germany would win the war.
"


Shadow-Kaiser

Wilhelm's role in wartime was one of ever-decreasing power as he increasingly handled awards ceremonies and honorific duties.
Increasingly cut off from reality and the political decision-making process, Wilhelm vacillated between defeatism and dreams of victory, depending upon the fortunes of his armies.
Nevertheless, Wilhelm still retained the ultimate authority in matters of political appointment, and it was only after his consent had been gained that major changes to the high command could be brought about.
Wilhelm was in favour of the dismissal of Colonel General Helmuth von Moltke in September 1914 and his replacement by General Erich von Falkenhayn.
Upon hearing in July 1917 that his cousin George V had changed the name of the British royal house to Windsor, Wilhelm remarked that he planned to see Shakespeare's play "The Merry Wives of Saxe-Coburg-Gotha".
That year also saw Wilhelm sickened during the worldwide Spanish flu outbreak, though he survived.
Abdication and exile

Wilhelm was at the Imperial Army headquarters in Spa, Belgium, when the uprisings in Berlin and other centres took him by surprise in late 1918.
After the outbreak of the German Revolution, Wilhelm could not make up his mind whether to abdicate.
Wilhelm thought he ruled as emperor in a personal union with Prussia.
In truth, the constitution defined the empire as a confederation of states under the permanent presidency of Prussia.
The imperial crown was thus tied to the Prussian crown, meaning that Wilhelm could not renounce one crown without renouncing the other.
Wilhelm's hope of retaining at least one of his crowns was revealed as unrealistic when, in the hope of preserving the monarchy in the face of growing revolutionary unrest, Chancellor Prince Max of Baden announced Wilhelm's abdication of both titles on 9 November 1918.
Prince Max himself was forced to resign later the same day, when it became clear that only Friedrich Ebert, leader of the SPD, could effectively exert control.
Wilhelm accepted this fait accompli only after Ludendorff's replacement, General Wilhelm Groener, had informed him that the officers and men of the army would march back in good order under Hindenburg's command, but would certainly not fight for Wilhelm's throne.
On 10 November, Wilhelm crossed the border by train and went into exile in the neutral Netherlands.
Upon the conclusion of the Treaty of Versailles in early 1919, Article 227 expressly provided for the prosecution of Wilhelm "for a supreme offence against international morality and the sanctity of treaties", but the Dutch government refused to extradite him.
The request for extradition will not be based on genuine desire on the part of British officials to bring the kaiser to trial, according to authoritative information, but is considered necessary formality to 'save the face' of politicians who promised to see that Wilhelm was punished for his crimes.
President Woodrow Wilson of the United States opposed extradition, arguing that prosecuting Wilhelm would destabilise international order and lose the peace.
Wilhelm first settled in Amerongen, where on 28 November he issued a belated statement of abdication from both the Prussian and imperial thrones, thus formally ending the Hohenzollerns' 500-year rule over Prussia and its predecessor state, Brandenburg.
Finally accepting the reality that he had lost both of his crowns for good, he gave up his rights to "the throne of Prussia and to the German Imperial throne connected therewith".
He also released his soldiers and officials in both Prussia and the empire from their oath of loyalty to him.
The Weimar Republic allowed Wilhelm to remove twenty-three railway wagons of furniture, twenty-seven containing packages of all sorts, one bearing a car and another a boat, from the New Palace at Potsdam.
Life in exile

In 1922, Wilhelm published the first volume of his memoirs—a very slim volume that insisted he was not guilty of initiating the Great War, and defended his conduct throughout his reign, especially in matters of foreign policy.
Wilhelm had developed a penchant for archaeology while residing at the Corfu Achilleion, excavating at the site of the Temple of Artemis in Corfu, a passion he retained in his exile.
In exile, one of Wilhelm's greatest passions was hunting, and he killed thousands of animals, both beast and bird.
Wealth

Wilhelm II was seen as the richest man in Germany before 1914.
Views on Nazism

In the early 1930s, Wilhelm apparently hoped that the successes of the Nazi Party would stimulate interest in a restoration of the House of Hohenzollern, with his eldest grandson as the new Kaiser.
Though he played host to Hermann Göring at Doorn on at least one occasion, Wilhelm learned to distrust Hitler.
Hearing of the murder of the wife of former Chancellor Kurt von Schleicher during the Night of the Long Knives, Wilhelm said, "We have ceased to live under the rule of law and everyone must be prepared for the possibility that the Nazis will push their way in and put them up against the wall!"
Wilhelm was also appalled at the Kristallnacht of 9–10 November 1938, saying "I have just made my views clear to Auwi  in the presence of his brothers.
Wilhelm also stated, "For the first time, I am ashamed to be a German":


There's a man alone, without family, without children, without God  He builds legions, but he doesn't build a nation.
And I was gratified to see that there were, associated with it for a time, some of the wisest and most outstanding Germans.
— Wilhelm on Hitler, December 1938

In the wake of the German victory over Poland in September 1939, Wilhelm's adjutant, Wilhelm von Dommes, wrote on his behalf to Hitler, stating that the House of Hohenzollern "remained loyal" and noted that nine Prussian Princes (one son and eight grandchildren) were stationed at the front, concluding "because of the special circumstances that require residence in a neutral foreign country, His Majesty must personally decline to make the aforementioned comment.
Wilhelm greatly admired the success which the Wehrmacht was able to achieve in the opening months of the Second World War, and personally sent Hitler a congratulatory telegram when the Netherlands surrendered in May 1940: "My Führer, I congratulate you and hope that under your marvellous leadership the German monarchy will be restored completely."
Upon the fall of Paris a month later, Wilhelm sent another telegram: "Under the deeply moving impression of France's capitulation I congratulate you and all the German armed forces on the God-given prodigious victory with the words of Kaiser Wilhelm the Great of the year 1870: 'What a turn of events through God's dispensation!'
In a letter to his daughter Victoria Louise, Duchess of Brunswick, he wrote triumphantly, "Thus is the pernicious Entente Cordiale of Uncle Edward VII brought to nought."
In a September 1940 letter to an American journalist, Wilhelm praised Germany's rapid early conquests as "a succession of miracles", but remarked also that "the brilliant leading Generals in this war came from My school, they fought under my command in the World War as lieutenants, captains and young majors.
After the German conquest of the Netherlands in 1940, the aging Wilhelm retired completely from public life.
In May 1940, Wilhelm declined an offer from Winston Churchill of asylum in Great Britain, preferring to die at Huis Doorn.
Anti-English, antisemitic, and anti-Freemason views

During his last year at Doorn, Wilhelm believed that Germany was still the land of monarchy and Christianity, while England was the land of classical liberalism and therefore of Satan and the Antichrist.
Wilhelm asserted that the "British people must be liberated from Antichrist Juda.
Continental Europe was now, Wilhelm wrote, "consolidating and closing itself off from British influences after the elimination of the British and the Jews!"
In a 1940 letter to his sister Princess Margaret, Wilhelm wrote: "The hand of God is creating a new world & working  ...
Despite their very troubled relationship, Wilhelm wrote to a friend, "Today the 100th birthday of my mother!
"


Death

Wilhelm died of a pulmonary embolism in Doorn, Netherlands, on 4 June 1941, at the age of 82, just weeks before the Axis invasion of the Soviet Union.
However, it was then revealed that Wilhelm's orders were that his body was not to return to Germany unless the monarchy was first restored.
The mourners included Field Marshal August von Mackensen, fully dressed in his old Imperial Hussars uniform, former World War I Office of Naval Intelligence field agent Admiral Wilhelm Canaris, Colonel General Curt Haase, World War I flying ace turned Wehrmachtbefehlshaber for the Netherlands General Friedrich Christiansen, and Reichskommissar for the Netherlands Arthur Seyss-Inquart, along with a few other military advisers.
However, Kaiser Wilhelm's insistence that the swastika and Nazi Party regalia not be displayed at his funeral was ignored, as is seen in the photographs of the funeral taken by a Dutch photographer.
Wilhelm was buried in a mausoleum upon the grounds of Huis Doorn, which has since become a place of pilgrimage for German monarchists, who gather there every year on the anniversary of his death to pay their homage to the last German Emperor.
Historiography

Three trends have characterised the writing about Wilhelm.
Second, there came those who judged Wilhelm to be completely unable to handle the great responsibilities of his position, a ruler too reckless to deal with power.
Third, after 1950, later scholars have sought to transcend the passions of the early 20th century and attempted an objective portrayal of Wilhelm and his rule.
The accompanying story called him "the greatest factor for peace that our time can show", and credited Wilhelm with frequently rescuing Europe from the brink of war.
Until the late 1950s, Germany under the last Kaiser was depicted by most historians as an almost absolute monarchy.
More recently, historian John C. G. Röhl has portrayed Wilhelm as the key figure in understanding the recklessness and downfall of Imperial Germany.
Marriages and issue

Wilhelm and his first wife, Augusta Victoria of Schleswig-Holstein, were married on 27 February 1881.
They had seven children:


Empress Augusta, known affectionately as "Dona", was a constant companion to Wilhelm, and her death from a heart attack on 11 April 1921 was a devastating blow.
It also came less than a year after their son Joachim committed suicide.
Remarriage

The following January, Wilhelm received a birthday greeting from a son of the late Prince Johann George Ludwig Ferdinand August Wilhelm of Schönaich-Carolath.
The 63-year-old Wilhelm invited the boy and his mother, Princess Hermine Reuss of Greiz, to Doorn.
Wilhelm found 35-year-old Hermine very attractive, and greatly enjoyed her company.
The couple were wed in Doorn on 5 November 1922 despite the objections of Wilhelm's monarchist supporters and his children.
Hermine's daughter, Princess Henriette, married the late Prince Joachim's son, Karl Franz Josef, in 1940, but divorced in 1946.
Religion

Own views

In accordance with his role as the King of Prussia, Emperor Wilhelm II was a Lutheran member of the Evangelical State Church of Prussia's older Provinces.
Attitude towards Islam

Wilhelm II was on friendly terms with the Muslim world.
Following his trip to Constantinople (which he visited three times—an unbeaten record for any European monarch) in 1898, Wilhelm II wrote to Nicholas II that:


If I had come there without any religion at all, I certainly would have turned Mohammedan!
Antisemitism

Wilhelm's biographer Lamar Cecil identified Wilhelm's "curious but well-developed anti-Semitism", noting that in 1888 a friend of Wilhelm "declared that the young Kaiser's dislike of his Hebrew subjects, one rooted in a perception that they possessed an overweening influence in Germany, was so strong that it could not be overcome".
Cecil concludes:


Wilhelm never changed, and throughout his life he believed that Jews were perversely responsible, largely through their prominence in the Berlin press and in leftist political movements, for encouraging opposition to his rule.
At the height of German military intervention against the Red Army during the Russian Civil War in 1918, Kaiser Wilhelm also suggested a similar campaign against the "Jew-Bolsheviks" who were slaughtering the Baltic German nobility in the Baltic states, citing the example of what Turks had done to the Ottoman Armenians just a few years earlier.
On 2 December 1919, Wilhelm wrote to Mackensen, denouncing the November Revolution of 1918 and his own forced abdication as the "deepest, most disgusting shame ever perpetrated by a person in history, the Germans have done to themselves ... egged on and misled by the tribe of Judah ...
Wilhelm advocated a "regular international all-worlds pogrom à la Russe" as "the best cure" and further believed that Jews were a "nuisance that humanity must get rid of some way or other.



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
  AssignClass (2f61c9c9-709e-400a-96d8-b343e6cc9191)
 Call ID: 2f61c9c9-709e-400a-96d8-b343e6cc9191
  Args:
    type: :Man
    source: :Wilhelm_II
  AssignClass (fb4906be-3686-449b-9530-8b72e0444df9)
 Call ID: fb4906be-3686-449b-9530-8b72e0444df9
  Args:
    source: :Wilhelm_II
    type: :Person
  AddLiteral (060f3f68-c272-4a1c-9d85-6309ef928922)
 Call ID: 060f3f68-c272-4a1c-9d85-6309ef928922
  Args:
    literal_value: 1859
    literal_type: xsd:integer
    source: :Wilhelm_II
    relation: :hasBirthYear
  AddLiteral (134858b6-86e4-4818-b719-0d32bb8bed7c)
 Call ID: 134858b6-86e4-4818-b719-0d32bb8bed7c
  Args:
    relation: :hasDeathYear
    literal_value: 1941
    literal_type: xsd:integer
    source: :Wilhelm_II
  AssignClass (f5f93f2e-732e-4f84-8b78-b665ca419712)
 Call ID: f5f93f2e-732e-4f84-8b78-b665ca419712
  Args:
    type: :Man
    source: :Frederick_III
  AssignClass (7a2e79ae-6eed-4120-aa86-89f950f31e4a)
 Call ID: 7a2e79ae-6eed-4120-aa86-89f950f31e4a
  Args:
    type: :Person
    source: :Frederick_III
  AssignClass (500d0426-7ca2-404b-8754-1cfd94087566)
 Call ID: 500d0426-7ca2-404b-8754-1cfd94087566
  Args:
    source: :Victoria_Princess_Royal
    type: :Woman
  AssignClass (5b801cba-051e-473b-868c-5f76d60107c7)
 Call ID: 5b801cba-051e-473b-868c-5f76d60107c7
  Args:
    type: :Person
    source: :Victoria_Princess_Royal
  AddTriple (80c67940-577d-42f0-b3ff-2ec314988dda)
 Call ID: 80c67940-577d-42f0-b3ff-2ec314988dda
  Args:
    relation: :hasFather
    target: :Frederick_III
    source: :Wilhelm_II
  AddTriple (22f66215-a74d-4e63-bf15-a48d4f26fcb7)
 Call ID: 22f66215-a74d-4e63-bf15-a48d4f26fcb7
  Args:
    relation: :hasMother
    source: :Wilhelm_II
    target: :Victoria_Princess_Royal
  AssignClass (ae5623f4-3c54-4e12-a357-10561e6637d9)
 Call ID: ae5623f4-3c54-4e12-a357-10561e6637d9
  Args:
    type: :Woman
    source: :Queen_Victoria
  AssignClass (076eae53-800f-4d8e-a42f-9df4448e07f5)
 Call ID: 076eae53-800f-4d8e-a42f-9df4448e07f5
  Args:
    source: :Queen_Victoria
    type: :Person
  AddTriple (ebdc5692-bd60-497c-9f05-adf1dd9f7c1e)
 Call ID: ebdc5692-bd60-497c-9f05-adf1dd9f7c1e
  Args:
    target: :Queen_Victoria
    source: :Victoria_Princess_Royal
    relation: :hasMother
  AssignClass (82725793-ca78-4620-a868-11e79c1bf4e8)
 Call ID: 82725793-ca78-4620-a868-11e79c1bf4e8
  Args:
    type: :Man
    source: :Prince_Albert
  AssignClass (7d873765-74ad-4d3b-8fd2-9e7e405e862e)
 Call ID: 7d873765-74ad-4d3b-8fd2-9e7e405e862e
  Args:
    type: :Person
    source: :Prince_Albert
  AddTriple (94236d39-3466-4b1a-b1ce-d532d377b460)
 Call ID: 94236d39-3466-4b1a-b1ce-d532d377b460
  Args:
    relation: :hasFather
    target: :Prince_Albert
    source: :Victoria_Princess_Royal
  AssignClass (b9a24e87-4e64-4d61-a95f-723fec29c90d)
 Call ID: b9a24e87-4e64-4d61-a95f-723fec29c90d
  Args:
    source: :Frederick_William_IV
    type: :Man
  AssignClass (a16b6696-68aa-4251-9daa-110754c5def7)
 Call ID: a16b6696-68aa-4251-9daa-110754c5def7
  Args:
    source: :Frederick_William_IV
    type: :Person
  AssignClass (2c4f1d32-f8b6-4292-9e75-26bc145a7e1a)
 Call ID: 2c4f1d32-f8b6-4292-9e75-26bc145a7e1a
  Args:
    type: :Man
    source: :Wilhelm_I
  AssignClass (f8c1f2d1-7022-485f-a2c7-27bf31b55eb5)
 Call ID: f8c1f2d1-7022-485f-a2c7-27bf31b55eb5
  Args:
    type: :Person
    source: :Wilhelm_I
  AddTriple (7122444f-153d-4b77-8e4f-06e31733ed57)
 Call ID: 7122444f-153d-4b77-8e4f-06e31733ed57
  Args:
    source: :Wilhelm_I
    target: :Frederick_William_IV
    relation: :isBrotherOf
  AddTriple (b9ba6194-1a70-4d18-8f8b-84a11f4262ed)
 Call ID: b9ba6194-1a70-4d18-8f8b-84a11f4262ed
  Args:
    target: :Wilhelm_I
    source: :Frederick_III
    relation: :hasFather
  AssignClass (c74e0dca-4021-460d-a1b7-7463f7d54652)
 Call ID: c74e0dca-4021-460d-a1b7-7463f7d54652
  Args:
    source: :Augusta_Victoria_of_Schleswig_Holstein
    type: :Woman
  AssignClass (277e14bd-c5be-414c-aef2-477db750f1c5)
 Call ID: 277e14bd-c5be-414c-aef2-477db750f1c5
  Args:
    source: :Augusta_Victoria_of_Schleswig_Holstein
    type: :Person
  AddLiteral (6869df9e-338e-43dd-91c3-1abb481c8c5e)
 Call ID: 6869df9e-338e-43dd-91c3-1abb481c8c5e
  Args:
    relation: :hasMarriageYear
    literal_type: xsd:integer
    literal_value: 1881
    source: :Wilhelm_II
  AddTriple (91f50637-9645-4a1a-bf0a-a178874cb9e1)
 Call ID: 91f50637-9645-4a1a-bf0a-a178874cb9e1
  Args:
    relation: :hasRelation
    target: :Augusta_Victoria_of_Schleswig_Holstein
    source: :Wilhelm_II
  AssignClass (9b3aa629-acbe-41bd-96c8-773fdacef98b)
 Call ID: 9b3aa629-acbe-41bd-96c8-773fdacef98b
  Args:
    source: :Sophia_of_Prussia
    type: :Woman
  AssignClass (9009bff1-db92-47ee-a0ee-4eec7f53919a)
 Call ID: 9009bff1-db92-47ee-a0ee-4eec7f53919a
  Args:
    source: :Sophia_of_Prussia
    type: :Person
  AddTriple (7cb92450-085d-4b5d-a168-3e7e432f242a)
 Call ID: 7cb92450-085d-4b5d-a168-3e7e432f242a
  Args:
    relation: :hasSister
    source: :Wilhelm_II
    target: :Sophia_of_Prussia
  AddTriple (3fb960f6-7aa5-4201-b1e6-508d769e47e2)
 Call ID: 3fb960f6-7aa5-4201-b1e6-508d769e47e2
  Args:
    target: :Frederick_III
    source: :Sophia_of_Prussia
    relation: :hasParent
  AddTriple (360237fc-cda2-4b21-89d2-75c0f0e18299)
 Call ID: 360237fc-cda2-4b21-89d2-75c0f0e18299
  Args:
    target: :Victoria_Princess_Royal
    source: :Sophia_of_Prussia
    relation: :hasParent
  AssignClass (37908dd3-e42d-4295-9dc8-08a571802caf)
 Call ID: 37908dd3-e42d-4295-9dc8-08a571802caf
  Args:
    type: :Man
    source: :Constantine_Crown_Prince_of_Greece
  AssignClass (047c351f-b6b3-4bb0-a05e-ba6335b00b09)
 Call ID: 047c351f-b6b3-4bb0-a05e-ba6335b00b09
  Args:
    type: :Person
    source: :Constantine_Crown_Prince_of_Greece
  AddTriple (1b928999-1553-446a-a636-2d91aaa3c8f2)
 Call ID: 1b928999-1553-446a-a636-2d91aaa3c8f2
  Args:
    relation: :hasRelation
    source: :Sophia_of_Prussia
    target: :Constantine_Crown_Prince_of_Greece
  AssignClass (19b08dbb-89bd-424d-baf1-c2fa8d643ec7)
 Call ID: 19b08dbb-89bd-424d-baf1-c2fa8d643ec7
  Args:
    source: :Victoria_Louise_of_Prussia
    type: :Woman
  AssignClass (d80bcb9f-835b-4850-9ec7-864108365241)
 Call ID: d80bcb9f-835b-4850-9ec7-864108365241
  Args:
    type: :Person
    source: :Victoria_Louise_of_Prussia
  AddTriple (d39bb2e7-3a5b-48e1-878d-f4387ed9c5d3)
 Call ID: d39bb2e7-3a5b-48e1-878d-f4387ed9c5d3
  Args:
    source: :Wilhelm_II
    target: :Victoria_Louise_of_Prussia
    relation: :hasDaughter
  AssignClass (afc21ea6-c65a-4e88-bf85-6a4def81c051)
 Call ID: afc21ea6-c65a-4e88-bf85-6a4def81c051
  Args:
    source: :Hermine_Reuss_of_Greiz
    type: :Woman
  AssignClass (4139333d-f5cd-400a-a3dd-0870f6e1bea9)
 Call ID: 4139333d-f5cd-400a-a3dd-0870f6e1bea9
  Args:
    type: :Person
    source: :Hermine_Reuss_of_Greiz
  AddLiteral (48ae3c35-3b48-44ad-94bc-214ccc80b400)
 Call ID: 48ae3c35-3b48-44ad-94bc-214ccc80b400
  Args:
    literal_value: 1922
    literal_type: xsd:integer
    source: :Wilhelm_II
    relation: :hasMarriageYear
  AddTriple (4f88d690-4a72-47b9-b88d-68ee20678a42)
 Call ID: 4f88d690-4a72-47b9-b88d-68ee20678a42
  Args:
    relation: :hasRelation
    target: :Hermine_Reuss_of_Greiz
    source: :Wilhelm_II
  Finish (63692d5f-942c-4367-8756-788020fe01a3)
 Call ID: 63692d5f-942c-4367-8756-788020fe01a3
  Args: