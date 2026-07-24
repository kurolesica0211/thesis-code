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
  AssignClass (8f437574-adef-43cb-a750-5b454ee1a16f)
 Call ID: 8f437574-adef-43cb-a750-5b454ee1a16f
  Args:
    type: :Woman
    source: Maria_Pavlovna_of_Russia
  AssignClass (c7cb78aa-386d-4236-a70e-34dc6ea31bad)
 Call ID: c7cb78aa-386d-4236-a70e-34dc6ea31bad
  Args:
    type: :Person
    source: Maria_Pavlovna_of_Russia
  AddLiteral (27a4c882-f08c-43c0-8a82-bb3591643ae7)
 Call ID: 27a4c882-f08c-43c0-8a82-bb3591643ae7
  Args:
    literal_type: xsd:date
    literal_value: 1890-04-18
    source: Maria_Pavlovna_of_Russia
    relation: :hasBirthYear
  AddLiteral (2fa2f751-235b-4481-baf0-8e0da7a07fcb)
 Call ID: 2fa2f751-235b-4481-baf0-8e0da7a07fcb
  Args:
    relation: :hasDeathYear
    source: Maria_Pavlovna_of_Russia
    literal_value: 1958-12-13
    literal_type: xsd:date
  AddLiteral (7347aff3-1034-4423-a185-018eb71d23f3)
 Call ID: 7347aff3-1034-4423-a185-018eb71d23f3
  Args:
    source: Maria_Pavlovna_of_Russia
    literal_value: Maria Pavlovna the Younger
    literal_type: xsd:string
    relation: :knownAs
  AssignClass (a5d12cc2-017f-484e-87c7-cdd6af817363)
 Call ID: a5d12cc2-017f-484e-87c7-cdd6af817363
  Args:
    type: :Man
    source: Paul_Alexandrovich_of_Russia
  AssignClass (bce87840-dd66-435b-8a91-7c928ea46e96)
 Call ID: bce87840-dd66-435b-8a91-7c928ea46e96
  Args:
    source: Paul_Alexandrovich_of_Russia
    type: :Person
  AssignClass (5a7b493f-27b7-4d22-b7b6-f190def75530)
 Call ID: 5a7b493f-27b7-4d22-b7b6-f190def75530
  Args:
    type: :Woman
    source: Alexandra_Georgievna_of_Russia
  AssignClass (737c5091-abde-4ad4-9bdb-416aeb6acfc2)
 Call ID: 737c5091-abde-4ad4-9bdb-416aeb6acfc2
  Args:
    source: Alexandra_Georgievna_of_Russia
    type: :Person
  AddTriple (647e1076-fb2e-40d7-a3cb-e9bb8d855a0f)
 Call ID: 647e1076-fb2e-40d7-a3cb-e9bb8d855a0f
  Args:
    source: Maria_Pavlovna_of_Russia
    target: Paul_Alexandrovich_of_Russia
    relation: :hasFather
  AddTriple (b582e307-996b-4990-9bd1-f7d690cfd092)
 Call ID: b582e307-996b-4990-9bd1-f7d690cfd092
  Args:
    target: Alexandra_Georgievna_of_Russia
    relation: :hasMother
    source: Maria_Pavlovna_of_Russia
  AssignClass (7be35e1d-1686-4eac-8662-d4f4f8820f4d)
 Call ID: 7be35e1d-1686-4eac-8662-d4f4f8820f4d
  Args:
    source: Dmitri_Pavlovich_of_Russia
    type: :Man
  AssignClass (837d0547-f117-4a07-9afe-e30ff0ba971e)
 Call ID: 837d0547-f117-4a07-9afe-e30ff0ba971e
  Args:
    source: Dmitri_Pavlovich_of_Russia
    type: :Person
  AddTriple (19f0e3d2-6de6-4231-b7b9-1ba3e326c047)
 Call ID: 19f0e3d2-6de6-4231-b7b9-1ba3e326c047
  Args:
    source: Maria_Pavlovna_of_Russia
    target: Dmitri_Pavlovich_of_Russia
    relation: :hasBrother
  AddTriple (bb7e9f7f-c272-4754-9077-8f08d0caa140)
 Call ID: bb7e9f7f-c272-4754-9077-8f08d0caa140
  Args:
    relation: :hasFather
    target: Paul_Alexandrovich_of_Russia
    source: Dmitri_Pavlovich_of_Russia
  AddTriple (dae3018e-3174-4c66-92e8-0c793b329647)
 Call ID: dae3018e-3174-4c66-92e8-0c793b329647
  Args:
    source: Dmitri_Pavlovich_of_Russia
    target: Alexandra_Georgievna_of_Russia
    relation: :hasMother
  AssignClass (301d0106-425c-470e-a446-d4ab3756654c)
 Call ID: 301d0106-425c-470e-a446-d4ab3756654c
  Args:
    type: :Man
    source: Sergei_Alexandrovich
  AssignClass (663843c8-e83a-4cc3-ba44-7f588071dabf)
 Call ID: 663843c8-e83a-4cc3-ba44-7f588071dabf
  Args:
    type: :Person
    source: Sergei_Alexandrovich
  AssignClass (4c544d71-22fd-45b4-8b01-6f2485bb9d0b)
 Call ID: 4c544d71-22fd-45b4-8b01-6f2485bb9d0b
  Args:
    source: Elizabeth_Feodorovna
    type: :Woman
  AssignClass (071b510a-5228-4e94-b7f4-3f8148f78bf3)
 Call ID: 071b510a-5228-4e94-b7f4-3f8148f78bf3
  Args:
    type: :Person
    source: Elizabeth_Feodorovna
  AddTriple (bd4cbb4d-9b16-4785-ae6a-e171e2e06b0a)
 Call ID: bd4cbb4d-9b16-4785-ae6a-e171e2e06b0a
  Args:
    relation: :isBrotherOf
    target: Paul_Alexandrovich_of_Russia
    source: Sergei_Alexandrovich
  AddTriple (41bee688-6977-4524-a96a-0e9da11a555f)
 Call ID: 41bee688-6977-4524-a96a-0e9da11a555f
  Args:
    source: Elizabeth_Feodorovna
    relation: :isSisterOf
    target: Alexandra_Feodorovna_Tsarina
  AssignClass (ce0b5ced-775e-4691-9315-c7738a016384)
 Call ID: ce0b5ced-775e-4691-9315-c7738a016384
  Args:
    source: Alexandra_Feodorovna_Tsarina
    type: :Woman
  AssignClass (2145cc75-d80c-4fec-94d1-c5df0d5ea171)
 Call ID: 2145cc75-d80c-4fec-94d1-c5df0d5ea171
  Args:
    type: :Person
    source: Alexandra_Feodorovna_Tsarina
  AssignClass (d18ec7ff-c042-4da6-ba9f-1b86800086de)
 Call ID: d18ec7ff-c042-4da6-ba9f-1b86800086de
  Args:
    type: :Man
    source: Wilhelm_Duke_of_Sodermanland
  AssignClass (ad7fdb5c-4da4-4e1b-a01a-a4fc9db899a5)
 Call ID: ad7fdb5c-4da4-4e1b-a01a-a4fc9db899a5
  Args:
    source: Wilhelm_Duke_of_Sodermanland
    type: :Person
  AddLiteral (ace6047f-bddf-4356-848c-db43fc72e7e1)
 Call ID: ace6047f-bddf-4356-848c-db43fc72e7e1
  Args:
    source: Maria_Pavlovna_of_Russia
    literal_value: 1908
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AddTriple (a1562b9f-af45-4faf-9ad7-9a1f503c0528)
 Call ID: a1562b9f-af45-4faf-9ad7-9a1f503c0528
  Args:
    target: Wilhelm_Duke_of_Sodermanland
    relation: :hasRelation
    source: Maria_Pavlovna_of_Russia
  AssignClass (f6dd59a0-c19e-48b6-bfc1-b61d656721da)
 Call ID: f6dd59a0-c19e-48b6-bfc1-b61d656721da
  Args:
    type: :Man
    source: Lennart_Duke_of_Smaland
  AssignClass (cc2c44ae-63fa-40d9-a93f-4711a8f8c3f6)
 Call ID: cc2c44ae-63fa-40d9-a93f-4711a8f8c3f6
  Args:
    source: Lennart_Duke_of_Smaland
    type: :Person
  AddTriple (3d9676f0-0a95-4d3e-8f58-95dac9b46bbc)
 Call ID: 3d9676f0-0a95-4d3e-8f58-95dac9b46bbc
  Args:
    source: Maria_Pavlovna_of_Russia
    relation: :hasSon
    target: Lennart_Duke_of_Smaland
  AddTriple (bb9a144e-8ca1-4f40-a4b0-d735062cbc50)
 Call ID: bb9a144e-8ca1-4f40-a4b0-d735062cbc50
  Args:
    source: Lennart_Duke_of_Smaland
    target: Wilhelm_Duke_of_Sodermanland
    relation: :hasFather
  AssignClass (fe90799f-8178-4c68-83ad-af6008744ccd)
 Call ID: fe90799f-8178-4c68-83ad-af6008744ccd
  Args:
    source: Sergei_Mikhailovich_Putyatin
    type: :Man
  AssignClass (6d208faa-8704-4b1d-8464-7863ea5bef41)
 Call ID: 6d208faa-8704-4b1d-8464-7863ea5bef41
  Args:
    source: Sergei_Mikhailovich_Putyatin
    type: :Person
  AddLiteral (d4c4841c-8823-499c-81de-934086b5da7f)
 Call ID: d4c4841c-8823-499c-81de-934086b5da7f
  Args:
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: Maria_Pavlovna_of_Russia
    literal_value: 1917
  AddTriple (080e5a43-e3c8-4869-afdd-1a1cc3737992)
 Call ID: 080e5a43-e3c8-4869-afdd-1a1cc3737992
  Args:
    source: Maria_Pavlovna_of_Russia
    target: Sergei_Mikhailovich_Putyatin
    relation: :hasRelation
  AssignClass (0168b62e-dac3-4765-bd6a-9c666557088b)
 Call ID: 0168b62e-dac3-4765-bd6a-9c666557088b
  Args:
    source: Roman_Sergeievich_Putyatin
    type: :Man
  AssignClass (0fca63d1-a953-45c8-a63f-8e73148e07f5)
 Call ID: 0fca63d1-a953-45c8-a63f-8e73148e07f5
  Args:
    source: Roman_Sergeievich_Putyatin
    type: :Person
  AddTriple (fde69a34-93e8-4ae9-950f-cad2ab6db5dc)
 Call ID: fde69a34-93e8-4ae9-950f-cad2ab6db5dc
  Args:
    target: Roman_Sergeievich_Putyatin
    relation: :hasSon
    source: Maria_Pavlovna_of_Russia
  AddTriple (e943baa3-fd8a-4ace-a02b-463ab8ad8d3b)
 Call ID: e943baa3-fd8a-4ace-a02b-463ab8ad8d3b
  Args:
    relation: :hasFather
    target: Sergei_Mikhailovich_Putyatin
    source: Roman_Sergeievich_Putyatin
  Finish (76c0b1fe-65fa-4c98-b449-22a902fcb388)
 Call ID: 76c0b1fe-65fa-4c98-b449-22a902fcb388
  Args: