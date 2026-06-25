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
Grand Duchess Maria Pavlovna of Russia (Russian: Великая Княгиня Мария Павловна; 18 April  1890 – 13 December 1958), known as Maria Pavlovna the Younger, was a granddaughter of Alexander II of Russia.
She was a paternal first cousin of Nicholas II (Russia's last Tsar) and Marie of Edinburgh (consort of Ferdinand I of Romania) and maternal first cousin of George II, Alexander, and Paul (all kings of Greece), Helen of Greece and Denmark, (second wife of Carol II of Romania), and Prince Philip, Duke of Edinburgh (consort of Elizabeth II).
She was also both the first grandchild of George I of Greece and the first great-grandchild of his father Christian IX of Denmark.
Her early life was marked by the death of her mother and her father's banishment from Russia when he remarried a commoner in 1902.
Grand Duchess Maria and her younger brother Dmitri, to whom she remained very close throughout her life, were raised in Moscow by their paternal uncle Grand Duke Sergei Alexandrovich and his wife Grand Duchess Elizabeth Feodorovna of Russia, a granddaughter of Queen Victoria.
In 1908, Maria Pavlovna married Prince Wilhelm, Duke of Södermanland.
The couple had one son, Prince Lennart, Duke of Småland, later Count Bernadotte af Wisborg.
During World War I, Grand Duchess Maria Pavlovna served as a nurse until the fall of the Russian monarchy in February 1917.
In September 1917, during the period of the Russian Provisional Government, she married Prince Sergei Putyatin.
They had a son, Prince Roman Sergeievich Putyatin, who died in infancy.
The couple escaped revolutionary Russia through Ukraine in July 1918.
In exile, Grand Duchess Maria Pavlovna lived briefly in Bucharest and London, then she settled in Paris in 1920.
In 1942, Grand Duchess Maria Pavlovna moved to Argentina where she spent the years of World War II.
Early life

Grand Duchess Maria Pavlovna was born 18 April  1890 in Saint Petersburg.
She was the first child and only daughter of Grand Duke Paul Alexandrovich of Russia and his first wife, Grand Duchess Alexandra Georgievna of Russia, born Princess Alexandra of Greece and Denmark.
The baby was named after her late paternal grandmother, the Empress Maria Alexandrovna, and her paternal aunt, maternal grandaunt, and godmother, the Empress Maria Feodorovna, and was known by the nickname "Marisha" Maria was not yet two years old when her mother died from complications after giving birth to Maria's younger brother, Grand Duke Dmitri Pavlovich of Russia in 1891.
Grand Duke Paul was so distraught by the unexpected death of his young wife that he neglected his two small children, who were left in the care of his elder brother, Grand Duke Sergei Alexandrovich, who had no children of his own.
Once he recovered emotionally, Grand Duke Paul took the two children away with him.
A commander of the Imperial horse Guards, Grand Duke Paul loved his children, but as was customary at the time, he refrained from showing them spontaneous affection.
Maria and her brother were raised by governesses and tutors, but they adored their father who visited them twice a day.
The children spent Christmases and later some summer holidays with Grand Duke Sergei and his wife Grand Duchess Elisabeth Feodorovna.
Maria Pavlovna's childhood was spent in splendor.
Until she was age 6, Maria spoke Russian badly as all of her governesses and the immediate family spoke English.
Growing up without a mother and with a frequently absent father, Grand Duchess Maria and her brother Dimitri became very close, relying on each other for affection and companionship.
Education

In 1895, Grand Duke Paul began an affair with Olga Valerianova von Pistolkors, a married woman.
As they had married by defying Nicholas II's opposition, the tsar forbade them to return to Russia.
Left fatherless, 12-year-old Maria and 11-year-old Dmitri moved to Moscow placed under the custody of their uncle Grand Duke Sergei and his wife Grand Duchess Elisabeth Feodorovna, a sister of the Tsarina Alexandra.
Maria and Dimitri resented their aunt and uncle, blaming them for the forced separation from their real father, who had abandoned them.
Grand Duke Sergei was strict and demanding, but devoted and affectionate toward the children.
Maria Pavlovna also commented that she could not entirely disagree with those who thought Grand Duke Sergei heartless, self-centered and cruel.
Maria had a somewhat strained relationship with her aunt.
Grand Duchess Elisabeth Feodorovna found it difficult to relate to the children, and she was cold and distant toward them.
The teenage Maria was described by her maternal aunt Grand Duchess Maria Georgievna of Russia as "full of life and very jolly, but inclined to be self-willed and selfish, and rather difficult to deal with.
"


Grand Duke Sergei, who served as Governor General of Moscow, was a polarizing figure.
The bomber had refrained from an earlier attack because he saw that Grand Duchess Elisabeth, 15-year-old Maria, and her younger brother Dmitri were in the carriage, and he did not want to kill women and children.
After the assassination of their uncle, both children were emotionally distraught, particularly Dmitri.
Grand Duke Paul claimed the custody of his children, but the tsar made Elisabeth their guardian.
Grand Duke Paul was allowed to visit them, but not to return to Russia permanently.
After her husband's assassination, Grand Duchess Elisabeth Feodorovna regretted treating the children poorly, and she became closer to them.
First marriage

During the next two years, Maria's aunt turned toward religion and charity work.
Planning to retire from court and to form a religious order, Grand Duchess Elisabeth decided to find a husband for her niece, along with the help of her cousin, Crown Princess Margaret of Sweden.
Shortly after Easter 1907, Prince Wilhelm, Duke of Södermanland, the second son of King Gustav V of Sweden and Victoria of Baden, visited St Petersburg, and he was introduced to the 16-year-old Maria Pavlovna.
The prince was tall, thin, dark and distinguished looking "with beautiful grey eyes", Maria recalled.
He stayed for dinner, and the following day, Maria was told that he wished to marry her.
Pressed by her aunt to give a speedy answer, Maria agreed to the prince's proposal and found herself engaged to a man she had known for only few hours.
Maria Pavlovna wrote later that she felt her aunt had rushed her into the marriage.
"Then we will be able to travel together," she wrote to Wilhelm after their engagement.
"


The marriage had positive political and diplomatic implications for both Russia and Sweden, and Tsar Nicholas II gave his consent.
Grand Duke Paul was not consulted.
Contemporary newspaper reports suggest that Maria Pavlovna brought a large fortune to the marriage; as a Granddaughter of Tsar Alexander II, she was entitled to an annuity of 50,000 roubles prior to reaching the age of majority, and 100,000 roubles (approximately £10,500 in 1908) per year thereafter .
As a Russian Grand Duchess, she also was reported to have received a dowry of 1,000,000 roubles upon her marriage, as well as a share in the estimated 8,000,000 rouble fortune left by her father upon his death.
From Peterhof, Maria Pavlovna went to Grand Duchess Elisabeth's rural estate Ilinskoe, near Moscow, where Wilhelm joined them for a month before he left on a cruise to the United States.
Maria imagined herself in love: "It’s lovely to have somebody, even far away, who love you more than anything and whom you love more than everybody on earth“, she wrote to him.
In October, Wilhelm returned to Russia joining Grand Duchess Maria and her brother Dimitri who introduced the Swedish prince to their father, Grand Duke Paul, who was permitted to come back to Russia for his daughter's wedding set to take place after she turned age 18 the next April.
At Wilhelm's departure, Maria wrote to him: " I love you, so much with every day, every hour more and more.
In her book of memoirs, written more than 20 years later, the grand duchess made different claims: "I was using Wilhelm, in a sense, only to obtain my freedom".
As the wedding day approached, she began to have doubts and wished to break off the engagement, but Princess Irene of Hesse, who was visiting her sister Grand Duchess Elisabeth Feodorovna, persuaded her otherwise.
Soon Maria Pavlovna was  again looking forward with enthusiasm to a new life.
Swedish princess

After a honeymoon in Germany, Italy and France, the newlyweds went to Sweden, where an official ceremonial reception awaited them with the state flags of Russia and Sweden waving in Stockholm.
The couple set up their home in the Swedish countryside in the province of Södermanland.
Maria added Swedish to the other five languages she spoke, and she became popular in her new country.
Maria Pavlovna, known in Sweden as the Duchess of Södermanland, was pregnant by the fall, but she quickly realized that she had little in common with her husband.
He was Prince Lennart, Duke of Småland, later Count of Wisborg (1909–2004)
In the autumn of 1910, Maria Pavlovna moved with her husband and their son to Oak Hill, a house she had built for herself outside Stockholm.
Maria went hunting, attended horse races, practiced winter sports and even played field hockey on her sister-in-law, Crown Princess Margaret's team.
Maria occasionally played with her son, who remembered sitting on her lap when they slid down a flight of steps on a large silver tray.
However, life at the Swedish court had as many restrictions on Maria Pavlovna as she had had in Russia.
Her husband Wilhelm, as a naval officer, had little time to spend with her.
Maria had an opportunity to meet other men.
King Vajiravudh and the Duke of Montpensier began to court her, and she enjoyed the flirtation.
He was devastated by her decision, begging her to give their marriage another chance, "but since he blamed most of our failure on me, we did not make any progress" Maria wrote.
In 1913, they were reunited when she went to Russia to attend the celebrations for the 300-year anniversary of the Romanov family.
When she returned to Stockholm, doctors alleged (falsely as it turned out) that Maria Pavlovna had a serious kidney ailment, and she was sent to Capri to recuperate in the winter 1913–1914.
Decades later, she described the horror she had felt toward the Swedish royal family because of their unlimited support of Munthe as the main reason she fled them and filed for divorce from Prince Wilhelm.
My God!"

Relatives in both Russia and Sweden viewed a divorce as unavoidable, and on 13 March 1914, her marriage officially was dissolved, an action then confirmed by an edict issued by Nicholas II on 15 July 1914.
Maria left her son behind in Sweden under his father's custody.
In Paris, Grand Duchess Maria re-established ties with her father, who had provided her with three half-siblings.
Maria Pavlovna studied at a painting school, and then traveled to Italy and Greece.
In the spring 1914, age 24, Maria Pavlovna returned to Russia.
She lived near her younger brother Dmitri, to whom she was intensely attached.
Troubled by her strong need for him, Dmitri distanced himself somewhat from his sister, hurting her terribly.
World War I, revolution and second marriage

At the outbreak of the war, Grand Duchess Maria Pavlovna trained as a nurse.
With Princess Helen of Serbia, the grand duchess was sent to the northern front, at Instenburg in East Prussia, under command of General Paul von Rennenkampf.
For bravery under airplane fire, she was awarded the George Medal.
Maria Pavlovna was at Pskov when she learned that Dmitri had participated in the murder of Grigori Rasputin on 17 December 1916; she was stunned.
Maria signed a letter along with other members of the Imperial family, begging Nicholas II to reverse his decision to exile Dmitri to the Persian front.
Two months later, the February Revolution erupted, and Tsar Nicholas II, Maria's first cousin, abdicated.
Maria Pavlovna left Pskov for Petrograd joining her father and his family at Tsarkoe Selo.
Earlier in the war, she had been reacquainted with Prince Sergei Mikhailovich Putyatin (1893–1966), the son of Prince Mikhail Sergeyevich Putyatin (1861–1938), palace commandant at Tsarskoye Selo, the tsar's country residence.
In the summer, they became engaged, and in love for the first time, Maria Pavlovna married Putyatin in the Pavlovsk Palace on 19 September  1917.
The couple spent the early months of their married life in Petrograd, living at first in Dmitri's palace.
The successful Bolshevik coup of November 1917 surprised Maria Pavlovna and her husband in Moscow, where they had traveled to remove some of Maria's jewels from the state bank.
Later, Serge's parents retrieved Maria's diamonds.
In the spring 1918, the couple moved to a cottage in Tsarkoe Selo to be closer to Grand Duke Paul, who was under house arrest.
There, the grand duchess tended a vegetable garden and kept a goat.
On 8 July 1918, she gave birth to a son, Prince Roman Sergeievich Putyatin (1918–1919).
The same day of Prince Roman's baptism on 18 July 1918, but they did not know it, Maria's half-brother Prince Vladimir Paley and her aunt Grand Duchess Elizabeth were murdered by the Bolsheviks.
With the situation quickly deteriorating in Russia for the Romanovs under the Bolshevik regime, Maria Pavlovna decided to leave for exile, leaving her baby under the care of her in-laws.
With her husband and her brother-in-law Prince Alexander Putyatin (1897–1954), Grand Duchess Maria Pavlovna left Tsarkoie Selo in late July.
Without traveling documents and fearing to be arrested at any stop, Maria Pavlovna, her husband and brother-in-law made their way by train during two nights and a day.
She had concealed, inside a bar of soap, a Swedish document identifying her as a former royal princess of that country.
After reaching Kishinev, Moldavia, they received an invitation from Queen Marie of Romania, Maria's first cousin, who had used Joseph W. Boyle to track them and bring them to safety.
Ill with influenza, the grand duchess arrived in Romania, beginning her life in exile.
Exile

In December 1918, Grand Duchess Maria Pavlovna and her second husband arrived in Bucharest staying at a local hotel.
In January 1919, they were given private apartments at the Cotroceni Palace as guests of the Romanian Queen Maria.
Tragic news came from Russia.
The following month, Maria Pavlovna learned that her father Grand Duke Paul Alexandrovich had been assassinated by the Bolsheviks along with three of his cousins.
A couple of weeks later, she received the news that her aunt Grand Duchess Elizabeth Feodorovna and half-brother Prince Vladimir Paley had been murdered with several other Romanov relatives in the summer 1918.
Maria Pavlovna's parents-in-law arrived in Bucharest with her son Roman, but once she obtained a traveling visa, Maria Pavlovna left with Putyatin for Paris, finding a house in Passy.
For the first time in her life, the 28-year-old grand duchess was forced to face everyday problems.
Her first years of exile were financed by the sale of the jewels she had had smuggled to Sweden before escaping Russia.
While in Paris in 1919, the grand duchess received a letter from her husband's parents telling her that one-year-old Roman had died of an intestinal disorder on 29 July.
Maria Pavlovna was reunited with her brother Dmitri in London.
She rented a small apartment with her husband to be close to her brother, but relations between Dmitri and Putyatin soon soured.
In the spring 1920, Maria Pavlovna returned to Paris to meet with her stepmother Princess Olga Paley and Maria's two half-sisters.
Her brother Dmitri followed her to Paris.
Missing her son Lennart, who had been left in Sweden, Maria and Dimitri went to meet him in Copenhagen in the early summer of 1921.
In Paris, Grand Duchess Maria opened a quality embroidering and sewing textile shop named Kitmir.
Through her brother, Maria Pavlovna met Coco Chanel in the autumn 1921.
The grand duchess was helped by her mother-in-law Princess Sophia Putyatina (1866–1940), and she employed Russians refugees in order to help them.
However, Kitmir was plagued by organizational problems, resulting in the dissipation of Maria's money from the sale of her jewels and leaving her heavily in debt.
After her divorce, Maria Pavlovna continued to work in Paris, but she moved to Boulogne, the south west suburb of Paris, where many Russians had taken residence.
In 1928, as embroidery began to be out of fashion, Maria Pavlovva sold her workshop to Maison Hurel.
Having suffered a defeat, but not surrendering, the grand duchess moved to London in the spring 1928 where she started selling Prince Igor, her own perfume, following in the footsteps of Chanel No. 5 and Patou's perfume Joy.
Failings in advertising and distribution made that Prince Igor was not a success.
Undeterred, Grand Duchess Maria Pavlovna emigrated to the United States hoping for a new start.
In the United States

Grand Duchess Maria Pavlovna's arrival in New York City was greeted by the press with great enthusiasm and curiosity.
In May 1929, Grand Duchess Maria Pavlovna started working for the New York department store Bergdorf Goodman.
Her book of memoirs was translated from Russian to English and published in two volumes: the first was titled The Education of a Princess, and the second was A Princess in Exile.
The success of her books improved Maria Pavlovna's finances.
Grand Duchess Maria Pavlovna always had an interest in photography, and in 1935, she was sent by Hearst to Germany as a photojournalist.
While living in New York, Maria Pavlovna collected Russian books and surrounded herself with a group of friends that included her half-sister Princess Natalia Paley, the photographer Horst P. Horst, Valentina Sanina, founder of the fashion house Valentina, and Sanina's husband George Schlee.
In 1937, Maria Pavlovna visited her son Lennart and his family in Mainau.
They bonded over their shared interest in photography, and she got along with his wife, even though the grand duchess had been disappointed when her son renounced his royal status in order to marry a commoner in 1932.
Maria Pavlovna, who had little maternal feelings, took no interest in her two grand daughters: Birgitta, then age 4, and Marie Louise, age two.
Because of Lennart, the King of Sweden, who sympathized with Maria Pavlovna, arranged a Swedish diplomatic passport for her to replace her old Nansen passport.
Last years

In Argentina, Maria Pavlovna rented a small house with a garden in the Barrio Norte in Buenos Aires and devoted her spare time to painting, even managing to sell several of her works.
The cosmetic line did not take off, but Grand Duchess Maria Pavlovna remained in South America.
There was a large Russian émigré community in Buenos Aires, and she became close friends with the family of Prince Meshchersky, Prince Michel Aleksandrovich Gorchakov (1905–1996) and his wife Princess Olga, née Orlova-Davydova (1904–1991).
During weekends, she went to Los Leones, a huge property owned by Prince Karl von Auersperg (1895–1980) and his wife, Countess Henriette von Meran  (1904–2000), member of a morganatic branch of the House of Habsburg.
In 1942, she received news of the death of her brother Dmitri in Davos, Switzerland.
In 1947, Maria Pavlovna's son Lennart came from Germany on a business visit that lasted several months.
Maria told Lennart that she had felt lonely all of her life due to her rootless childhood.
Two years later, Maria Pavlovna returned to Europe, where, at the home of her son on the island of Mainau in Germany, she re-encountered her first husband Prince Wilhelm of Sweden for the first time in many years.
During the 1950s, Grand Duchess Maria Pavlovna stayed with friends or appeared unexpectedly in Mainau in the house of her son Lennart with her camera, easel and paints.
She is buried in a side altar of the palace church in Mainau, next to her brother Grand Duke Dmitri.



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
  AssignClass (f480bfdf-003f-4e9b-8bd7-9be074b8732a)
 Call ID: f480bfdf-003f-4e9b-8bd7-9be074b8732a
  Args:
    type: :Woman
    source: :MariaPavlovna
  AssignClass (8ab121de-9d5a-4617-8568-b6e4c3502281)
 Call ID: 8ab121de-9d5a-4617-8568-b6e4c3502281
  Args:
    source: :MariaPavlovna
    type: :Person
  AddLiteral (eae57429-53c0-403f-9df3-e42ab0b21211)
 Call ID: eae57429-53c0-403f-9df3-e42ab0b21211
  Args:
    source: :MariaPavlovna
    literal_value: 1890
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (c5967c5b-f7cc-487e-a512-ac4ffb1b8544)
 Call ID: c5967c5b-f7cc-487e-a512-ac4ffb1b8544
  Args:
    literal_value: 1958
    source: :MariaPavlovna
    relation: :hasDeathYear
    literal_type: xsd:integer
  AddLiteral (8481ccfc-472d-467f-86bc-83a11433807a)
 Call ID: 8481ccfc-472d-467f-86bc-83a11433807a
  Args:
    relation: :knownAs
    literal_type: xsd:string
    source: :MariaPavlovna
    literal_value: Maria Pavlovna the Younger
  AssignClass (8b914869-c761-4049-82a8-bf58bd28d76f)
 Call ID: 8b914869-c761-4049-82a8-bf58bd28d76f
  Args:
    type: :Man
    source: :PaulAlexandrovich
  AssignClass (18e0e8e0-c85a-483b-bf49-fffdc72664db)
 Call ID: 18e0e8e0-c85a-483b-bf49-fffdc72664db
  Args:
    type: :Person
    source: :PaulAlexandrovich
  AssignClass (1d08041e-1405-4734-853e-f054a86d69e6)
 Call ID: 1d08041e-1405-4734-853e-f054a86d69e6
  Args:
    type: :Woman
    source: :AlexandraGeorgievna
  AssignClass (62b46013-fad8-42af-810f-427b6cff44af)
 Call ID: 62b46013-fad8-42af-810f-427b6cff44af
  Args:
    source: :AlexandraGeorgievna
    type: :Person
  AddTriple (befa5178-f6ca-4e62-a647-829b68d30127)
 Call ID: befa5178-f6ca-4e62-a647-829b68d30127
  Args:
    relation: :hasFather
    target: :PaulAlexandrovich
    source: :MariaPavlovna
  AddTriple (12742d26-372f-418b-b7d0-924427e9b619)
 Call ID: 12742d26-372f-418b-b7d0-924427e9b619
  Args:
    target: :AlexandraGeorgievna
    source: :MariaPavlovna
    relation: :hasMother
  AssignClass (c5ed5c1e-2cb1-4d3b-af8f-02ca9f2b9197)
 Call ID: c5ed5c1e-2cb1-4d3b-af8f-02ca9f2b9197
  Args:
    type: :Man
    source: :DmitriPavlovich
  AssignClass (6eb132b1-bc33-43b3-b78f-7bff28e05b44)
 Call ID: 6eb132b1-bc33-43b3-b78f-7bff28e05b44
  Args:
    type: :Person
    source: :DmitriPavlovich
  AddTriple (65cce640-2f49-4549-972d-0915243b0137)
 Call ID: 65cce640-2f49-4549-972d-0915243b0137
  Args:
    source: :DmitriPavlovich
    target: :MariaPavlovna
    relation: :isBrotherOf
  AddTriple (e6baaebf-7a1a-4dd4-b250-4340950f021f)
 Call ID: e6baaebf-7a1a-4dd4-b250-4340950f021f
  Args:
    relation: :hasFather
    target: :PaulAlexandrovich
    source: :DmitriPavlovich
  AddTriple (a6fc0cce-ddfc-4713-9eb6-f06e924cfcc4)
 Call ID: a6fc0cce-ddfc-4713-9eb6-f06e924cfcc4
  Args:
    relation: :hasMother
    source: :AlexandraGeorgievna
    target: :DmitriPavlovich
  AssignClass (727e3ecc-0905-48ff-a8a6-f4e45b260256)
 Call ID: 727e3ecc-0905-48ff-a8a6-f4e45b260256
  Args:
    source: :SergeiAlexandrovich
    type: :Man
  AssignClass (c81d8ca0-fcec-4739-a805-e50dbb74a2ef)
 Call ID: c81d8ca0-fcec-4739-a805-e50dbb74a2ef
  Args:
    type: :Person
    source: :SergeiAlexandrovich
  AssignClass (cb5c7c5e-f0f8-4a81-847b-2b782c022feb)
 Call ID: cb5c7c5e-f0f8-4a81-847b-2b782c022feb
  Args:
    type: :Woman
    source: :ElizabethFeodorovna
  AssignClass (309b3419-c806-40d9-8069-42765cd10cd4)
 Call ID: 309b3419-c806-40d9-8069-42765cd10cd4
  Args:
    source: :ElizabethFeodorovna
    type: :Person
  AddTriple (e2492788-540e-4d8b-b4ea-3c5e65d398c7)
 Call ID: e2492788-540e-4d8b-b4ea-3c5e65d398c7
  Args:
    relation: :isBrotherOf
    source: :SergeiAlexandrovich
    target: :PaulAlexandrovich
  AddTriple (3e9eb319-b775-4e7a-87df-e1f80e5637a8)
 Call ID: 3e9eb319-b775-4e7a-87df-e1f80e5637a8
  Args:
    target: :PaulAlexandrovich
    source: :SergeiAlexandrovich
    relation: :hasFather
  AddTriple (982291de-8b15-4402-9476-6c251d11b0a0)
 Call ID: 982291de-8b15-4402-9476-6c251d11b0a0
  Args:
    target: :SergeiAlexandrovich
    source: :ElizabethFeodorovna
    relation: :hasMother
  AssignClass (503ec9e7-a445-4a4f-a8a7-509456ba61d6)
 Call ID: 503ec9e7-a445-4a4f-a8a7-509456ba61d6
  Args:
    type: :Man
    source: :WilhelmSweden
  AssignClass (cea43d79-6fc6-4e38-b266-63da93b7587a)
 Call ID: cea43d79-6fc6-4e38-b266-63da93b7587a
  Args:
    type: :Person
    source: :WilhelmSweden
  AddLiteral (669b62db-f83e-4101-8f2c-308f645e9c69)
 Call ID: 669b62db-f83e-4101-8f2c-308f645e9c69
  Args:
    source: :MariaPavlovna
    literal_value: 1908
    relation: :hasMarriageYear
    literal_type: xsd:integer
  AssignClass (8f0ed5a3-4251-4762-a95f-9999ef6d8d64)
 Call ID: 8f0ed5a3-4251-4762-a95f-9999ef6d8d64
  Args:
    type: :Man
    source: :LennartBernadotte
  AssignClass (c8b7ebdb-beb1-407c-ba7e-31a66957097d)
 Call ID: c8b7ebdb-beb1-407c-ba7e-31a66957097d
  Args:
    type: :Person
    source: :LennartBernadotte
  AddTriple (68e4ecd4-6746-4b4c-905e-6c9cff7f6610)
 Call ID: 68e4ecd4-6746-4b4c-905e-6c9cff7f6610
  Args:
    target: :WilhelmSweden
    source: :LennartBernadotte
    relation: :hasFather
  AddTriple (9d2e0f47-2ccf-4daa-bde1-c3ad571c43b5)
 Call ID: 9d2e0f47-2ccf-4daa-bde1-c3ad571c43b5
  Args:
    relation: :hasMother
    source: :LennartBernadotte
    target: :MariaPavlovna
  AssignClass (920ae303-a08d-435f-9d0e-ac8f6d803e1a)
 Call ID: 920ae303-a08d-435f-9d0e-ac8f6d803e1a
  Args:
    source: :SergeiPutyatin
    type: :Man
  AssignClass (8f81b517-fbdc-4807-b4b1-42589c735673)
 Call ID: 8f81b517-fbdc-4807-b4b1-42589c735673
  Args:
    type: :Person
    source: :SergeiPutyatin
  AddLiteral (675088e4-6c40-4346-8c05-b48450877a8a)
 Call ID: 675088e4-6c40-4346-8c05-b48450877a8a
  Args:
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: :MariaPavlovna
    literal_value: 1917
  AssignClass (0cd6790c-3556-4a99-8a4c-e4101598519a)
 Call ID: 0cd6790c-3556-4a99-8a4c-e4101598519a
  Args:
    source: :RomanSergeievichPutyatin
    type: :Man
  AssignClass (d62d89e2-128f-4e71-b834-e7e3e6748991)
 Call ID: d62d89e2-128f-4e71-b834-e7e3e6748991
  Args:
    source: :RomanSergeievichPutyatin
    type: :Person
  AddTriple (bb0773c1-7bef-487e-954b-1dbc660b7239)
 Call ID: bb0773c1-7bef-487e-954b-1dbc660b7239
  Args:
    relation: :hasFather
    source: :RomanSergeievichPutyatin
    target: :SergeiPutyatin
  AddTriple (e041ba72-f3e7-4ce2-9e32-7ed11b0fd93c)
 Call ID: e041ba72-f3e7-4ce2-9e32-7ed11b0fd93c
  Args:
    target: :MariaPavlovna
    source: :RomanSergeievichPutyatin
    relation: :hasMother
  Finish (38aa2b72-4fe2-492d-9a51-77bf0f329b11)
 Call ID: 38aa2b72-4fe2-492d-9a51-77bf0f329b11
  Args: