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
Grand Duke Dmitri Pavlovich of Russia (Russian: Великий Князь Дмитрий Павлович; 18 September 1891 – 5 March 1942) was a son of Grand Duke Paul Alexandrovich of Russia, a grandson of Tsar Alexander II of Russia and a first cousin of Tsar Nicholas II, Marie of Edinburgh (consort of Ferdinand I of Romania), King George II of Greece, King Alexander of Greece, Helen of Greece and Denmark, (second wife of Carol II of Romania), King Paul of Greece, and Prince Philip, Duke of Edinburgh (consort of Queen Elizabeth II).
His early life was marked by the death of his mother and his father's banishment from Russia after marrying a commoner in 1902.
Grand Duke Dmitri and his elder sister Grand Duchess Maria Pavlovna, to whom he remained very close throughout his life, were raised in Moscow by their paternal uncle Grand Duke Sergei Alexandrovich and his wife Grand Duchess Elizabeth Feodorovna of Russia, an older sister of Empress Alexandra Feodorovna.
His uncle was killed in 1905 and as his aunt entered religious life, Dmitri spent a great deal of his youth in the company of Tsar Nicholas II and his immediate family at the Alexander Palace as they viewed him almost like a foster son.
Grand Duke Dmitri followed a military career, graduating from the Nicholas Cavalry College .
In 1926, he married Audrey Emery, an American heiress.
As the youngest Grand Duke to have survived the Russian Revolution, he was a prominent figure in the Russian community in exile, but he was not interested in politics, supporting instead the claim of his first cousin, Grand Duke Kirill Vladimirovich of Russia.
Early life

Grand Duke Dmitri was born on 18 September  1891 as the second child and only son of Grand Duke Paul Alexandrovich and his first wife, Grand Duchess Alexandra Georgievna of Russia, born Princess Alexandra of Greece and Denmark.
Dmitri's father, Grand Duke Paul Alexandrovich, was the youngest child of Tsar Alexander II of Russia and his first wife, Empress Maria Alexandrovna.
Dmitri's mother, Alexandra, was a daughter of George I of Greece and Olga Konstantinovna of Russia, and a sister of King Constantine I, and Andrew who was the father of Prince Philip, Duke of Edinburgh, making them first cousins.
He was also first cousins to Marie, Queen of Romania and Grand Duchess Victoria Feodorovna of Russia, who were the daughters of his paternal aunt Grand Duchess Maria Alexandrovna of Russia who married Alfred, Duke of Saxe-Coburg and Gotha, the second son of Queen Victoria and Prince Albert of Saxe-Coburg and Gotha.
During the summer of 1891, Grand Duchess Alexandra and Grand Duke Paul visited Paul's brother Grand Duke Serge Alexandrovich at his country estate Ilyinskoye  near Moscow.
Alexandra was seven months pregnant with Dmitri when, while taking a stroll with some friends by the Moskva River, she jumped into a boat, falling as she got in.
The next day, she collapsed in the middle of a ball from violent labor pains brought on by the previous day's activities; Dmitri was born in the hours following the accident.
Alexandra slipped into a coma from which she never emerged.
She died of eclampsia six days after Dmitri's birth.
Although doctors had no hope for Dmitri's survival, he still lived, with the help of his uncle Grand Duke Sergei Alexandrovich of Russia, who gave the premature Dmitri the baths that were prescribed by the doctors, wrapped him in cotton wool and kept him in a cradle filled with hot water bottles to keep his temperature regulated, the treatment of the time to keep premature babies alive.
At birth, Dmitri had an older sister, Grand Duchess Maria Pavlovna, with whom he had a close relationship throughout his life.
Grand Duke Paul was so distraught by the unexpected death of his young wife that he initially neglected his two small children: Dmitri and his older sister Grand Duchess Maria Pavlovna.
The children were therefore largely cared for by Paul's elder brother, Grand Duke Sergei Alexandrovich, and his wife Grand Duchess Elizabeth Feodorovna, who had no children of their own.
They spent Christmases and later some summer holidays with Grand Duke Sergei and Grand Duchess Elisabeth who set aside a playroom and bedrooms for the youngsters at their country home, Ilinskoe.
In his widowhood, Grand Duke Paul settled with his children in his palace in St Petersburg.
A commander of the imperial Horse Guards, Grand Duke Paul loved his children, but as was customary at the time, he refrained from showing them spontaneous affection.
Dmitri and his sister were initially educated at home by governesses and private tutors, while they adored their father who visited them twice daily.
Like all male members of the Romanov family, Grand Duke Dmitri was destined to follow a military career which traditionally began for a Grand Duke at the age of seven.
This was delayed, in Dmitri's case, until he was nine years old.
In the spring of 1901, his education was entrusted to General George Mikhailovich Laiming.
In their apartments, Dmitri and his sister enjoyed a warm family environment.
Youth and education

In 1895, Grand Duke Paul began an affair with a married woman, Olga Valerianova Pistolkors.
He was able to obtain a divorce for her and he eventually married Olga in 1902, while the couple was staying abroad.
The marriage was a violation of the house law of the Romanovs, and as they had married defying Nicholas II's opposition, the Tsar forbade them to return to Russia and Grand Duke Paul was not allowed to take the children with him into exile.
Left fatherless, eleven-year-old Dmitri and his twelve-year-old sister were sent to live with their uncle, Grand Duke Sergei, and his wife Grand Duchess Elizabeth Feodorovna (the Empress's sister), in Moscow.
In her memoirs, Grand Duchess Maria Pavlovna (the Younger) describes Grand Duke Sergei as a stern disciplinarian, and his wife, Grand Duchess Elizabeth as a cold and unwelcoming presence.
In 1903, at the age of twelve, Dmitri was enrolled in the Chevalier Guard regiment following studies at the Calvary Academy.
On 4 February 1905, Grand Duke Sergei, who had recently resigned from the post of Governor-General of Moscow, was assassinated by Ivan Kalyaev, a member of the Socialist-Revolutionary Party.
Kalyaev, armed with a homemade bomb, had aborted his first attempt to kill the Grand Duke when he spotted Dmitri and Marie with their uncle in his carriage.
The assassination of Grand Duke Sergei is the subject matter of the  French writer and philosopher Albert Camus' 1949 play The Just Assassins.
His uncle's death was only one of several assassinations that robbed Dmitri of close family members.
After Sergei's death, Dmitri's father, Grand Duke Paul was allowed to return to Russia to attend the funeral.
He asked Nicholas II to restore the custody of his children but instead, Nicholas named Sergei's widow Grand Duchess Elizabeth Feodorovna as the children's guardian.
Maria Pavlovna continued to have some feelings of anger toward her aunt, whom she would blame for her overly hasty and unsuccessful marriage to Prince Wilhelm of Sweden in 1908, but Dmitri formed a very strong bond with Elizabeth and came to admire her personal fortitude.
It was during this period that Dmitri began to form a close bond with Nicholas II, looking upon him as a surrogate father.
Nicholas, in turn, treated Dmitri very kindly.
In 1909, Dmitri left his aunt's care to move to St Petersburg with his head tutor and companion, General Laiming.
He lived at his father's vacant palace and then at the Beloselsky-Belozersky Palace, which he had inherited from his uncle Grand Duke Sergei, and would become his principal residence until he left Russia.
He placed ninth in the individual jumping event whereas Russia placed fifth in the team jumping event.
Disappointed in the performance of the Russian team, Dmitri started the idea of a national Russian sports competition, the very beginning of what under Soviet rule became the Spartakiad.
In Spring 1914, Dmitri's father returned to live in Russia, settling with his second wife and new family at Tsarskoye Selo.
Around the same time, Dmitri's sister, Grand Duchess Maria Pavlovna, who had divorced her husband, also returned to Russia moving with Dmitri.
However, troubled by her strong need for him, Dmitri distanced himself somewhat from his sister, hurting her terribly.
Dmitri served with the Life Guard Horse Regiment, participating in the campaign in East Prussia.
During the first weeks of the war he was awarded the Order of St. George after he rescued a wounded corporal under heavy gunfire.
In 1914, his friend Felix Yusupov married the Tsar's only niece, Princess Irina.
Historian Greg King claimed that Dmitri "harboured an intensely romantic devotion" to the openly bisexual Felix.
Killing of Rasputin

In August 1915 when Nicholas II left St. Petersburg to take full command of the Russian armies fighting World War I, his wife Empress Alexandra Feodorovna took on the daily administrative affairs of the government from the capital.
Alexandra relied on Grigori Rasputin, a peasant healer who appeared to have brought her hemophiliac son Alexei, the Tsarevich, back from the brink of death.
As Russian defeats mounted during the war, both Rasputin and Alexandra became increasingly unpopular.
Eventually, Grand Duke Dmitri Pavlovich joined Felix Yusupov, Vladimir Purishkevich (the leader of the monarchists in the Duma) Dr. Stanislaus de Lazovert and Lieutenant Sergei Mikhailovich Sukhotin, an officer in the Preobrazhensky Regiment, in a conspiracy to kill Grigory Rasputin hoping that ending his influence over the imperial family this would have a beneficial effect on the Tsar's policies.
Then, while both were sitting, Yusupov shot Rasputin at close range using Dmitri's Browning pistol.
He joined his fellow conspirators: Grand Duke Dmitri, politician Vladimir Purishkevich, and army officer Sergei Mikhailovich Sukhotin who were waiting in a ground floor study/drawing-room.
Dmitri drove the men and Rasputin's body, wrapped in a broadcloth, to Petrovskii Bridge, which crossed to Krestovsky Island.
All along, Grand Duke Dmitri, who was driving the car, never saw Rasputin.
By Sunday, Dmitri was placed under house arrest.
He was then living at his mother-in-law's palace, but on the advice of his uncle by marriage Grand Duke Nicholas Michailovich, he moved to Dmitri's palace for protection as it was the prerogative of the Tsar alone to prosecute members of the Imperial family.
He did interview Grand Duke Dmitri, Felix Yusupov, and Vladimir Purishkevich, but he decided not to charge them with murder.
Exile

Banishment to Persia

As a result of his participation in Rasputin's assassination, Grand Duke Dmitri Pavlovich was banished from the Russian court and was sent to exile to the Persian war front.
In the early hours of 6 January   1917, Grand Duke Dmitri left Saint Petersburg never to return.
General Baratov asked Dmitri to leave since there were rumblings from the lower ranks, and his safety could not be guaranteed.
Ronald Wingate entertained Pavlovich when he passed through Najaf.
The Provisional Government invited him to return to Russia, but he declined.
In the summer of 1917, Dmitri left the Russian occupation zone moving to Tehran.
Dmitri stayed briefly with General Meidel (ru), then the head of the Persian Cossack Division, before being taken in by the British Minister to Tehran, Sir Charles Murray Marling, and his wife, Lucia.
Through 1917 and most of 1918 Grand Duke Dmitri lived with the Marlings.
Marling obtained an honorary commission for Pavlovich as a liaison officer with the British Mission and eventually persuaded the British Foreign Office in 1918 that he would become the next Emperor of Russia, gaining his admission to England.
Marling became an important father figure to Pavlovich, and the relationship there established between them would prove to be close and enduring.
Interlude in England

Marling and his family took Dmitri with them when they left Tehran for England at the end of 1918.
During the long journey to England in a slow steamer, Pavlovich fell ill with typhoid fever in Bombay and nearly died.
The Marlings took him to London where he was reunited with his maternal aunt Grand Duchess Maria Georgievna.
Pavlovich took a room at the Ritz and spent most of his time with his aunt.
Lady Marling went to see the King's assistant private secretary Lord Cromer to inform him of the grand duke's arrival.
King George V was horrified; his presence was an inconvenience to the British government that did not want to upset the new Bolshevik regime.
In London, Dmitri was finally reunited with his sister Grand Duchess Maria Pavlovna who had escaped Revolutionary Russia though Ukraine with her second husband, Prince Sergei Mikhailovich Putiatin.
Dmitri moved with his sister and brother-in-law taking a house together in South Kensington.
The Yusupovs had escaped Russia with the Dowager Empress, Maria Feodorovna, and they too settled in London.
Pavlovich avoided Yusupov, resenting his breaking the silence regarding the details of Rasputin's assassination.
Relations between Dmitri and Putiatin also soon soured.
In spring 1920, Maria Pavlovna returned to Paris to meet with their stepmother, Princess Olga Paley, and their two half-sisters.
Unhappy in England, Dmitri followed his sister to Paris in the summer of 1920.
Exile in Paris

In Paris, Dmitri took rooms at a hotel until he found a modest two-room apartment.
In the summer of 1921, Dmitri accompanied his sister to Denmark to a reunion with her son Prince Lennart.
While in Denmark, Dmitri saw the Marling family again and with his sister visited Maria Feodorovna, who had retired to her villa Hvidore.
With his economic resources depleting, Grand Duke Dmitri found employment serving on the board of a Champagne firm.
An American journalist described him around this time as attractive: "He is, in his slender well-groomed person, all that a grand duke should be – especially if you like your grand duke young, clean-shaven, and concave at the waistline.
Well known in the Paris scene of the 1920s, Dmitri was then having an affair with opera singer Marthe Davelli.
It was through her that Dmitri became close to Gabrielle "Coco" Chanel.
Chanel and Dmitri, who had actually met before in pre-World War I Paris, became lovers.
Dmitri's sister, Maria Pavlovna, found a niche for herself in the rising Paris fashion industry by founding a business called "Kitmir" that specialized in bead and sequin embroidery and did much work for Chanel.
It was Dmitri who introduced Chanel to Ernest Beaux, the perfumer who created Chanel No. 5, her most enduring product.
Coco and Dmitri spent a happy summer at a villa near Arcachon.
Chanel would later comment: "These grand dukes, they are all the same, an admirable face behind which there is nothing, green eyes, broad shoulders, fine hands... the most peaceful people, shyness itself.
"


As the youngest Grand Duke to have survived the Russian Revolution, Pavlovich was a prominent figure of the Russian community in exile.
During the early 1920s, there was a bitter rivalry between the camps of the supporters of Grand Duke Kirill Vladimirovich and those of Grand Duke Nicholas Nikolaevich.
While those who supported neither Nicholas nor Kirill advocated for Dmitri's candidacy for the Russian throne.
On 8 August 1922, a makeshift Zemsky Sobor was convened at Priamurye, and Grand Duke Nicholas Nikolaevich was "elected" Emperor.
The Grand Duke neither accepted nor refused this empty gesture.
Having waited for confirmation of the death of Tsar Nicholas II, his son, and his brother, in 1924 Grand Duke Kirill Vladimirovich announced (also on 8 August) that he would assume "guardianship" of the throne of Russia.
On 25 September 1924, Grand Duke Alexander Michailovich issued an appeal to Russians to stand with Grand Duke Kirill Vladimirovich.
It was at this time that Grand Duke Dmitri Pavlovich, who had no political ambitions for himself, supported instead the claim of his first cousin, Grand Duke Kirill Vladimirovich.
Grand Duke Dmitri was also active politically.
Together with his cousin, Prince Dmitri Alexandrovich, he was very involved in the monarchist youth organizations which sprang up in the years between the wars.
By 1923, the largest of these was the "Union of Young Russia" which preached orthodoxy, nationalism, monarchism and peasant collectivism.
Marriage

In 1923 Grand Duchess Maria Pavlovna divorced her second husband and bought a small house at Boulogne-sur-Seine and Dmitri moved with her to the top floor.
Invited to a tea party at Versailles with his sister, he met Audrey Emery, a sophisticated and attractive American heiress.
Grand Duke Dmitri had no fortune to offer, but they fell in love and they were married in the Orthodox Church at Biarritz on 21 November 1926.
It was a morganatic marriage, and Audrey, who converted to Russian Orthodoxy and took the name Anna Ioannovna in baptism, was granted the title Her Serene Highness, Princess Romanovskaya-Ilyinskaya by his cousin, Grand Duke Kyril.
The couple's only child, Paul Romanovsky-Ilyinsky, was born in London in 1928.
Paul grew up in France, Britain, and the United States; he served as a US Marine in the Korean War.
Following the fall of communist Russia in 1991, a delegation of Russian royalists approached him and asked him to assume the title of Tsar, which he declined.
In 1928, the Dowager Empress died, and Grand Duke Kirill was received at the funeral as head of the House of Romanoff by the royal family of Denmark – it was the last time that the entire dynasty appeared as a single undivided family and Grand Duke Dmitri was a prominent figure in the proceedings.
The youngest of the Grand Dukes, Dmitri Pavlovich frequently represented Grand Duke Kirill at events public, private, and political.
He was prominent at the funerals of King Constantine I of Greece (1923), Queen Astrid of the Belgians (1935), at the wedding of Grand Duke Kirill's daughter, Grand Duchess Kira to Prince Louis Ferdinand of Prussia (1938), and also at the ceremonies surrounding the accession of Grand Duke Vladimir Kirillovich of Russia to the rights of the headship of the imperial house on the death of his father in 1938.
Grand Duke Dmitri was a noted collector of model trains and was at one point considered to have had one of the largest collections in Europe.
During the Nazi annexation of Paris, Dmitri's collection vanished, and it has since been theorized that they were seized by Hermann Göring, a model train collector himself.
In the late 1920s, Grand Duke Dmitri became involved with his cousin, Prince Dmitri Alexandrovich Romanoff in the monarchist youth organizations which sprang up in the years between the wars.
It was a Russian nationalist group influenced by Italian Fascism, formed with the express purpose of establishing a "Soviet monarchy" in Russia.
He joined this group as a stand-in for Grand Duke Kirill Vladimirovich, who, as pretender to the throne, could not affiliate himself directly with any political organization or party.
In 1935, Grand Duke Dmitri gave a series of speeches to Young Russia chapters throughout France.
Grand Duke Dmitri reputedly rebuked later advances from Hitler to lead exiled Russian nobles within the German army against the Bolsheviks with the firm statement that nothing would induce him to fight against fellow Russians.
Last years

Grand Duke Dmitri Pavlovich and his wife could afford a very opulent lifestyle with homes in London, Biarritz, Neuilly-sur-Seine, and Château de Beaumesnil near Caen, and visits to America.
Dmitri then lived at the Château de Beaumesnil in Beaumesnil, Eure, France, which he had bought in 1927.
Over the years, Dmitri became disappointed with the prospects for the restoration of the monarchy in Russia and withdrew from public life.
His son was at school in England, but Dmitri could spend the school holidays with him until 1939, when it was decided to send Paul to America for safety.
They saw each other for the last time in Genoa spending three days before Paul embarked to America.
Despite not having strong health, Grand Duke Dmitri was, for most of his life, a very active sportsman, excelling at polo, horse riding, tennis, and bobsledding.
From the safety of the sanatorium in Davos, Dmitri followed with great interest the events of World War II; he wrote to a friend on 10 April 1940, on the eve of the collapse of France, "everything starts looking petty in comparison with world events".
On 4 March 1942, Grand Duke Dmitri organized a Russian festival to entertain himself with his friend and the staff.
The following morning Dmitri suffered a sudden attack of uremia and died at the age of fifty.
After the death of Dmitri's sister Maria Pavlovna in December 1958, his nephew, Prince Lennart Bernadotte, had him buried alongside his sister, in the chapel of his castle on the island of Mainau in Lake Constance, where they now lie beside his sister in the Bernadotte family crypt.



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
  AssignClass (b0f81925-5af7-4b02-84e5-c8c4a7c240c0)
 Call ID: b0f81925-5af7-4b02-84e5-c8c4a7c240c0
  Args:
    type: :Man
    source: :GrandDukeDmitriPavlovich
  AssignClass (0f2afe40-8664-4a55-8399-5893f4f3e102)
 Call ID: 0f2afe40-8664-4a55-8399-5893f4f3e102
  Args:
    type: :Person
    source: :GrandDukeDmitriPavlovich
  AddLiteral (5fde2f27-19e5-4876-bcf2-410a4873f758)
 Call ID: 5fde2f27-19e5-4876-bcf2-410a4873f758
  Args:
    source: :GrandDukeDmitriPavlovich
    literal_type: xsd:integer
    literal_value: 1891
    relation: :hasBirthYear
  AddLiteral (f1227395-f626-4fe8-81f0-485024865d75)
 Call ID: f1227395-f626-4fe8-81f0-485024865d75
  Args:
    literal_type: xsd:integer
    literal_value: 1942
    relation: :hasDeathYear
    source: :GrandDukeDmitriPavlovich
  AssignClass (7c7c8dc8-8e28-457f-b9cc-a7cde5bb9e16)
 Call ID: 7c7c8dc8-8e28-457f-b9cc-a7cde5bb9e16
  Args:
    type: :Man
    source: :GrandDukePaulAlexandrovich
  AssignClass (475dee71-c7b6-4b7e-aa41-832c361b509d)
 Call ID: 475dee71-c7b6-4b7e-aa41-832c361b509d
  Args:
    type: :Person
    source: :GrandDukePaulAlexandrovich
  AddTriple (4992c9ad-2cdd-41bf-90c5-f347e061a891)
 Call ID: 4992c9ad-2cdd-41bf-90c5-f347e061a891
  Args:
    relation: :hasFather
    target: :GrandDukePaulAlexandrovich
    source: :GrandDukeDmitriPavlovich
  AssignClass (3b3205fa-71e4-4712-820b-027d5ee44012)
 Call ID: 3b3205fa-71e4-4712-820b-027d5ee44012
  Args:
    type: :Woman
    source: :GrandDuchessAlexandraGeorgievna
  AssignClass (d08777e0-1e05-408c-86b4-7577381e4093)
 Call ID: d08777e0-1e05-408c-86b4-7577381e4093
  Args:
    type: :Person
    source: :GrandDuchessAlexandraGeorgievna
  AddTriple (d362cf64-16e2-4202-9959-70c62e171391)
 Call ID: d362cf64-16e2-4202-9959-70c62e171391
  Args:
    relation: :hasMother
    target: :GrandDuchessAlexandraGeorgievna
    source: :GrandDukeDmitriPavlovich
  AssignClass (a60778b9-3c36-47b6-8a1e-c2bcbbc2bd8e)
 Call ID: a60778b9-3c36-47b6-8a1e-c2bcbbc2bd8e
  Args:
    type: :Woman
    source: :GrandDuchessMariaPavlovna
  AssignClass (6bc50fe9-316f-43c5-b606-272f01014d9a)
 Call ID: 6bc50fe9-316f-43c5-b606-272f01014d9a
  Args:
    type: :Person
    source: :GrandDuchessMariaPavlovna
  AddTriple (2c82c0ce-e688-4077-a8dd-e3693e192e2f)
 Call ID: 2c82c0ce-e688-4077-a8dd-e3693e192e2f
  Args:
    source: :GrandDuchessMariaPavlovna
    target: :GrandDukeDmitriPavlovich
    relation: :isSisterOf
  AssignClass (ef193b05-64d7-4963-8c62-2ca90030a809)
 Call ID: ef193b05-64d7-4963-8c62-2ca90030a809
  Args:
    type: :Man
    source: :TsarAlexanderII
  AssignClass (c8dd7ee2-d79b-48fd-97fc-1f0023ce1a2a)
 Call ID: c8dd7ee2-d79b-48fd-97fc-1f0023ce1a2a
  Args:
    type: :Person
    source: :TsarAlexanderII
  AddTriple (ea495f92-0398-4470-8d0f-6fb1d89eb9d4)
 Call ID: ea495f92-0398-4470-8d0f-6fb1d89eb9d4
  Args:
    target: :TsarAlexanderII
    relation: :hasFather
    source: :GrandDukePaulAlexandrovich
  AssignClass (8d7a5f3d-f0d3-44b7-ac1c-f5469b86ded6)
 Call ID: 8d7a5f3d-f0d3-44b7-ac1c-f5469b86ded6
  Args:
    type: :Woman
    source: :EmpressMariaAlexandrovna
  AssignClass (688a4508-be14-42be-af8b-cac001f41110)
 Call ID: 688a4508-be14-42be-af8b-cac001f41110
  Args:
    type: :Person
    source: :EmpressMariaAlexandrovna
  AddTriple (1f41e024-db51-4eed-b568-b3a461a64482)
 Call ID: 1f41e024-db51-4eed-b568-b3a461a64482
  Args:
    relation: :hasMother
    target: :EmpressMariaAlexandrovna
    source: :GrandDukePaulAlexandrovich
  AssignClass (202fff1e-412a-4220-85bd-85f53ffadac8)
 Call ID: 202fff1e-412a-4220-85bd-85f53ffadac8
  Args:
    type: :Man
    source: :GeorgeIGreece
  AssignClass (1bbba970-87cd-42a7-b6d7-38dc6167eee2)
 Call ID: 1bbba970-87cd-42a7-b6d7-38dc6167eee2
  Args:
    type: :Person
    source: :GeorgeIGreece
  AddTriple (fc2bf144-24a0-40f8-9317-4d8bd4857078)
 Call ID: fc2bf144-24a0-40f8-9317-4d8bd4857078
  Args:
    target: :GeorgeIGreece
    relation: :hasFather
    source: :GrandDuchessAlexandraGeorgievna
  AssignClass (bd3c805c-8128-46e1-b1b3-f46d9f7424cf)
 Call ID: bd3c805c-8128-46e1-b1b3-f46d9f7424cf
  Args:
    type: :Woman
    source: :OlgaKonstantinovna
  AssignClass (906a5f6b-9e5f-4f21-8ef4-6c1e960d4234)
 Call ID: 906a5f6b-9e5f-4f21-8ef4-6c1e960d4234
  Args:
    type: :Person
    source: :OlgaKonstantinovna
  AddTriple (f47d114d-d858-477e-9f27-25b6b50f9ac3)
 Call ID: f47d114d-d858-477e-9f27-25b6b50f9ac3
  Args:
    source: :GrandDuchessAlexandraGeorgievna
    relation: :hasMother
    target: :OlgaKonstantinovna
  AssignClass (e80c966b-a92d-43c2-9310-6edffb25b281)
 Call ID: e80c966b-a92d-43c2-9310-6edffb25b281
  Args:
    type: :Man
    source: :GrandDukeSergeiAlexandrovich
  AssignClass (816a72e6-627d-427e-96c5-3f103dee9565)
 Call ID: 816a72e6-627d-427e-96c5-3f103dee9565
  Args:
    type: :Person
    source: :GrandDukeSergeiAlexandrovich
  AddTriple (eb7661ff-54ae-4595-9cd6-084c079e7a9a)
 Call ID: eb7661ff-54ae-4595-9cd6-084c079e7a9a
  Args:
    target: :GrandDukeSergeiAlexandrovich
    relation: :hasBrother
    source: :GrandDukePaulAlexandrovich
  AssignClass (c5c4f463-523c-4006-8dd4-315444c56303)
 Call ID: c5c4f463-523c-4006-8dd4-315444c56303
  Args:
    type: :Woman
    source: :GrandDuchessElizabethFeodorovna
  AssignClass (9b8d7bcb-9e1a-438b-9832-754a13ec818b)
 Call ID: 9b8d7bcb-9e1a-438b-9832-754a13ec818b
  Args:
    type: :Person
    source: :GrandDuchessElizabethFeodorovna
  AddTriple (38207c97-cf23-4df1-b782-98183ceb3b86)
 Call ID: 38207c97-cf23-4df1-b782-98183ceb3b86
  Args:
    source: :GrandDuchessElizabethFeodorovna
    target: :EmpressAlexandraFeodorovna
    relation: :isSisterOf
  AssignClass (9535bde5-02d7-483d-9904-b1e055f1f256)
 Call ID: 9535bde5-02d7-483d-9904-b1e055f1f256
  Args:
    type: :Woman
    source: :EmpressAlexandraFeodorovna
  AssignClass (b70031cb-d3da-473b-ae2a-e7af71f3df5d)
 Call ID: b70031cb-d3da-473b-ae2a-e7af71f3df5d
  Args:
    type: :Person
    source: :EmpressAlexandraFeodorovna
  AssignClass (a867158c-9256-4dd1-b9b2-f51712ad8f5b)
 Call ID: a867158c-9256-4dd1-b9b2-f51712ad8f5b
  Args:
    type: :Woman
    source: :AudreyEmery
  AssignClass (bf10059a-ac35-4363-967a-c9ecc53cae8f)
 Call ID: bf10059a-ac35-4363-967a-c9ecc53cae8f
  Args:
    type: :Person
    source: :AudreyEmery
  AddTriple (2b8be6a7-b925-42c5-85ec-210377748be8)
 Call ID: 2b8be6a7-b925-42c5-85ec-210377748be8
  Args:
    source: :GrandDukeDmitriPavlovich
    target: :AudreyEmery
    relation: :hasRelation
  AddLiteral (d0917058-38e5-4447-b168-4da734dcbd30)
 Call ID: d0917058-38e5-4447-b168-4da734dcbd30
  Args:
    literal_type: xsd:integer
    literal_value: 1926
    relation: :hasMarriageYear
    source: :GrandDukeDmitriPavlovich
  AssignClass (d9a384ce-3dae-450e-81d1-5ff612945d1d)
 Call ID: d9a384ce-3dae-450e-81d1-5ff612945d1d
  Args:
    type: :Man
    source: :PaulRomanovskyIlyinsky
  AssignClass (47dfdb90-3364-4698-9357-f468950150bb)
 Call ID: 47dfdb90-3364-4698-9357-f468950150bb
  Args:
    type: :Person
    source: :PaulRomanovskyIlyinsky
  AddTriple (56ae7229-1a91-44e3-9560-9380968b210b)
 Call ID: 56ae7229-1a91-44e3-9560-9380968b210b
  Args:
    source: :PaulRomanovskyIlyinsky
    target: :GrandDukeDmitriPavlovich
    relation: :hasFather
  AddTriple (594c6743-7c84-43ab-854a-3a205efb67ea)
 Call ID: 594c6743-7c84-43ab-854a-3a205efb67ea
  Args:
    relation: :hasMother
    target: :AudreyEmery
    source: :PaulRomanovskyIlyinsky
  Finish (57671cf0-f535-4fcc-836c-ad05ce93d5b0)
 Call ID: 57671cf0-f535-4fcc-836c-ad05ce93d5b0
  Args: