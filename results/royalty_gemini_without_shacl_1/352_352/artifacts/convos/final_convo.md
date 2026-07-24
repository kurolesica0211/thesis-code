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
Princess Charlotte of Prussia (German: Victoria Elisabeth Augusta Charlotte, Prinzessin von Preußen; 24 July 1860 – 1 October 1919) was Duchess of Saxe-Meiningen from 1914 to 1918 as the wife of Bernhard III, the duchy's last ruler.
Born at the Neues Palais in Potsdam, she was the second child and eldest daughter of Prince Frederick of Prussia, a member of the House of Hohenzollern who became Crown Prince of Prussia in 1861 and German Emperor in 1888.
Through her mother Victoria, Princess Royal, Charlotte was the eldest granddaughter of Queen Victoria of the United Kingdom and Prince Albert of Saxe-Coburg and Gotha.
Princess Charlotte was a difficult child and indifferent student, with a nervous disposition.
As she grew older, Charlotte developed a penchant for spreading gossip and causing trouble.
Eager to escape from parental control, at age seventeen, she married Prince Bernhard of Saxe-Meiningen in 1878.
Known for spreading gossip and her eccentric personality, Princess Charlotte enjoyed Berlin society while frequently leaving her only child, Princess Feodora, in the care of family members.
Charlotte and Feodora, in turn, also had a difficult relationship.
Charlotte's brother succeeded their father as Emperor Wilhelm II in 1888, increasing her social influence.
She became Duchess of Saxe-Meiningen in 1914, only for her husband to lose his title with the end of World War I in November 1918.
Charlotte died the following year of a heart attack in Baden-Baden.
Recent historians have argued that she had porphyria, a genetic disease that afflicted the British royal family.
Early life

Birth and family

Princess Viktoria Elisabeth Auguste Charlotte was born on 24 July 1860 at the Neues Palais in Potsdam.
She was the eldest daughter and second child of Prince Frederick William of Prussia and his wife Victoria, Princess Royal, known as Vicky in the family.
The product of an easy labour, she was a healthy baby who arrived 19 months after the difficult birth of her elder brother, Prince Wilhelm.
Her grandmother, Queen Victoria, wanted her eldest granddaughter to be named after her.
However, the Prussians wanted the new princess to be named Charlotte after Empress Alexandra Feodorovna of Russia, who had been born Princess Charlotte of Prussia, her paternal great-aunt.
As a compromise, her first name was Victoria, but she was always referred to as Charlotte.
She was also named after her paternal grandmother, Queen Augusta of Prussia.
Charlotte's paternal family belonged to the House of Hohenzollern, a royal house that had ruled the German state of Prussia since the seventeenth century.
By the end of her first year, Charlotte's father had become Crown Prince as his father ascended to the Prussian throne as King Wilhelm I. Charlotte's mother, Vicky, was the eldest daughter of the British monarch Queen Victoria and her husband Albert, Prince Consort.
Charlotte and her brother, Wilhelm, were the only grandchildren born in Albert's lifetime.
He and Victoria visited their daughter and two grandchildren when Charlotte was two months old; Vicky and Frederick William in turn brought Wilhelm and Charlotte on a visit to England in June 1861, six months before Albert's death.
Shortly after arriving in her new adopted country, Vicky observed the continuous arguments and intrigues within the Prussian royal family.
While Vicky was close with her eldest daughter, this changed as the girl grew older; by the time she was two years old, Charlotte had become known as "sweet naughty little Ditta" and would prove to be the most difficult of the family's eight children.
Queen Victoria wrote to her daughter, "tell Charlotte I was appalled to hear of her biting her things.
In 1863 the Crown Princess recorded in her diary that Charlotte's "little mind seems almost too active for her body – she is so nervous & sensitive and so quick.
Charlotte developed violent tantrums; Vicky described them as "such outbreaks of rage & stubbornness that she screams blue murder."
Charlotte was an indifferent student, to the dismay of her mother, who placed a high value on education.
Charlotte's governess declared she had never seen "more difficulties" than with the princess, while Vicky once wrote of Charlotte in a letter to her mother that "Stupidity is not a sin, but it renders education a hard and difficult task."
The Crown Princess rarely withheld her true thoughts of those who displeased her, and bluntly admonished her children to encourage their efforts and help them avoid vanity.
Queen Victoria urged her daughter to act encouragingly rather than reproachfully towards Charlotte, believing that she could not expect the young princess to share Vicky's tastes.
The deaths of Charlotte's brothers Sigismund and Waldemar in 1866 and 1879, respectively, devastated the Crown Princess.
The strict upbringing Vicky gave to the eldest three children—Wilhelm, Charlotte, and Henry—was not replicated in her relationship with her three youngest surviving children, Viktoria, Sophia, and Margaret.
The historian John Van der Kiste speculates that had Vicky shown the same level of acceptance with Charlotte as with her younger children, "the relationship between them might have been a happier one".


Charlotte was a favourite of her paternal grandparents, whom she frequently saw.
King Wilhelm and Queen Augusta spoiled their granddaughter and encouraged her rebellion against the Crown Prince and Princess, and Charlotte and her brother frequently took their side in disputes with her parents.
This rebellion was encouraged by the German chancellor Otto von Bismarck, who held political disagreements with the liberal Crown Prince and Princess.
Charlotte also enjoyed a close relationship with her eldest brother, though they grew apart after his marriage in 1881 to Augusta Victoria of Schleswig-Holstein ("Dona"), a princess described by Charlotte as plain, slow-witted, and shy.
Charlotte's relationship with Wilhelm would remain troubled as a result.
Charlotte's cousin, Queen Marie of Romania, wrote in her memoirs: "it was greatly owing to Charly's intrigues that King Carol's animosity against the Emperor Wilhelm was kept alive.
"


Engagement and marriage

By the time she reached fourteen, Charlotte was described by Vicky as appearing much younger than her age; Vicky wrote, "Charlotte is in everything – health, looks and understanding, like a child of ten!"
The princess had short legs, which, paired with a long waist and arms, made her appear tall when sitting but short when standing.
As Charlotte grew older, her behaviour came to include flirtation, spreading malicious gossip, and causing trouble, traits her mother had noticed in her daughter's youth and had hoped she would outgrow.
She believed that Charlotte's "pretty exterior" hid "dangerous character traits," and blamed nature for producing such qualities in her daughter.
In April 1877, the sixteen-year-old Charlotte became engaged to her second cousin Prince Bernhard of Saxe-Meiningen, heir to the German Duchy of Saxe-Meiningen.
According to a story related by Vicky's biographer, Hannah Pakula, Charlotte fell in love with the prince while they were driving with her eldest brother; Wilhelm sped up during the drive, alarming Charlotte and causing her to cling to Bernhard's arm.
Pakula adds that this sudden but temporary passion likely fit Charlotte's "changeable" personality.
Van der Kiste believes Charlotte's decision to marry Bernhard also stemmed from a desire to become independent of her parents, and especially from her mother's criticism.
Prince Bernhard, an army officer serving in a Potsdam regiment, was nine years her senior and a veteran of the recent Franco-Prussian War.
Charlotte did not share these interests, but Vicky hoped that time as well as marriage would guide Charlotte, so that "at least her wicked qualities will not be able to cause any harm".
They were married in Berlin on 18 February 1878, in a double ceremony that also included Princess Elisabeth Anna of Prussia's marriage to Frederick Augustus of Oldenburg.
Charlotte's maternal uncles, the Prince of Wales and Duke of Connaught and Strathearn, attended the wedding, as did King Leopold II and Queen Marie Henriette of Belgium.
The new couple established their household near the Neues Palais, in villa Liegnitz, previously inhabited by Auguste, Princess of Liegnitz, the morganatic wife of Frederick William III of Prussia.
They also purchased a villa in Cannes, a decision that angered Wilhelm, who viewed France as an enemy country; Charlotte eventually spent most of her winters in the French city, as she hoped that its warm climate would help alleviate her lifetime of ill health.
Birth of Princess Feodora

A year after their marriage, Charlotte gave birth to a daughter, Princess Feodora, on 12 May 1879.
The new princess was the first grandchild of the Crown Prince and Princess, as well as the first great-grandchild of Queen Victoria and Emperor Wilhelm.
Charlotte had hated the limitations placed on her while pregnant, and decided this would be her only child, to the dismay of her mother.
Following Feodora's birth, Charlotte devoted her time to enjoying society life in Berlin and embarking on long holiday trips.
During these trips, Charlotte would often leave her daughter to stay with Vicky, whom she viewed as the source of a convenient nursery.
"


Among the era's royal families, it was unusual to be an only child; Feodora likely endured a lonely childhood.
Feodora also lacked an interest in her studies, a deficit blamed by Vicky on a lack of parental guidance, as Charlotte and Bernhard were frequently away.
With Charlotte for an example, what else can one expect".
Adulthood

Wilhelm I granted Charlotte and Bernhard a villa near Tiergarten in Berlin and transferred Bernhard to a regiment in the city.
Charlotte spent much of her time socialising with other ladies, where it was common to pursue activities such as skating, gossiping, and holding dinner parties.
Charlotte also smoked and drank, and was liked by many for hosting entertaining parties.
Charlotte's father ascended the German throne as Emperor Frederick III in March 1888, only to succumb to throat cancer in June of that year.
Charlotte stayed with her ailing father during this period, alongside most of her siblings.
With her brother's ascension as Wilhelm II, Charlotte's social influence increased in Berlin, where she surrounded herself with a wild group of nobles, diplomats, and young officials from the court.
While she had gradually reconciled with her mother during Frederick's illness, Charlotte sided with Wilhelm when he complained that he should have attended Queen Victoria's Golden Jubilee in place of his ailing father.
Upon Wilhelm's ascension, Charlotte and Bernhard took his side in disputes with Vicky; the Dowager Empress, in turn, was defended by her three youngest daughters.
In one letter during this period, Vicky characterised her eldest daughter as "most odd" and "hardly com near me, also describing Bernhard as impertinent and rude.
Letters scandal

In early 1891, Berlin society erupted in scandal after a series of anonymous letters circulated to prominent members of the court, including Wilhelm and his wife Dona.
Some included pornographic images layered upon royal photographs.
Wilhelm ordered an investigation, but the writer (or writers) were never identified.
Some contemporaries speculated that Charlotte, known for her sharp tongue and love of gossip, may have been responsible.
Historians have since suggested that the writer may have been Dona's brother Duke Ernst Gunther of Schleswig-Holstein in collaboration with his mistress.
It is clear that the author had an intimate understanding of the many personalities within the royal family, likely making him or her either a family member or courtier.
During the letters scandal, Charlotte lost her diary which contained both family secrets and critical thoughts on various members of her family; the diary was eventually given to Wilhelm, who never forgave her for its contents.
Bernhard was transferred to a regiment in Breslau, effectively exiling him and his wife.
As controller of Charlotte's allowance, Wilhelm also limited their ability to travel outside of the country unless they were willing to go without royal honours.
In 1896, Dona accused Charlotte of engaging in an affair with Karl-August Freiherr Roeder von Diersburg, a court official.
Charlotte fiercely denied the allegations.
Bernhard defended his wife and criticised the Hohenzollerns for attempting to keep every Prussian princess under the control of the family.
Bernhard considered resigning his army position and leaving with his wife for Meiningen, though the dispute eventually resolved itself when von Diersburg returned to court with his wife.
The exiled Prince Peter Karađorđević, thirty-six years her senior, unsuccessfully requested her hand in marriage.
Another potential candidate was her cousin Alfred, Hereditary Prince of Saxe-Coburg and Gotha.
In late 1897, Feodora became engaged to Prince Henry XXX of Reuss, and they married the following year, on 24 September 1898 in a Lutheran ceremony at Breslau.
After a visit by the couple in 1899, Charlotte wrote that Feodora was "incomprehensible" and "shrinks away, whenever I try to influence her, concerning her person & health".
Charlotte also disliked her son-in-law, criticizing his appearance and inability to control his strong-willed wife.
Unlike her mother, Feodora wanted children; her inability to conceive left Feodora disappointed, though it pleased Charlotte, who had no desire for grandchildren.
Van der Kiste writes that Charlotte and Feodora had very similar personalities, "both strong-willed creatures who loved gossip and were too ready to believe the worst of each other".
Eventually, their relationship deteriorated enough for Charlotte to bar Feodora and Henry from her house.
Charlotte refused to accept Feodora's claim to have malaria, believing instead that her daughter had contracted a venereal disease from Henry; this opinion outraged Feodora.
Charlotte did not write to Feodora for nearly a decade, finally doing so after Feodora underwent a dangerous operation to help her conceive.
Charlotte expressed outrage that such an operation had been approved, but eventually visited her in the sanatorium at Feodora's request.
Duchess of Saxe-Meiningen; death

In June 1911, Charlotte attended the coronation of her cousin King George V in England, but the country's summer heat left her bed-ridden with a swollen face and pain in her limbs.
On 25 June 1914, her husband inherited his father's duchy and became Bernhard III, Duke of Saxe-Meiningen.
World War I broke out on 28 July; Bernhard left for the front while Charlotte remained behind to oversee the duchy, serving mainly as a figurehead (German: Landesregentin).
During the war, Charlotte increasingly experienced various pains including chronic aches, swollen legs, and kidney problems.
The end of the war in 1918 led to the political demise of the German Empire, as well as all of its many duchies; consequently, Bernhard was forced to abdicate his rule over Saxe-Meiningen.
The following year, Charlotte travelled to Baden-Baden to seek medical treatment for her heart, ultimately dying there of a heart attack on 1 October 1919 at the age of 59.
Bernhard died nine years later and was buried with her at Schloss Altenstein in Thuringia.
Medical analysis

Recent historians have argued that Charlotte and Feodora were afflicted with porphyria, a genetic disease that is believed to have affected some members of the British Royal Family, most notably King George III.
In their 1998 book Purple Secret: Genes, 'Madness', and the Royal Houses of Europe, the historian John C. G. Röhl and the geneticists Martin Warren and David Hunt identify Charlotte as "occup a crucial position in  search for the porphyria mutation in the descendants of the Hanoverians".
For evidence, Röhl reviewed letters between Charlotte and her doctor, as well as correspondence with her parents, that had been sent over a 25-year period; he found that even as a little girl, Charlotte had suffered from hyperactivity and indigestion.
As a young woman, Charlotte became gravely ill with what her mother called "malaria poisoning and anaemia," followed by "neuralgia, fainting and nausea," all described by Röhl as a "textbook list of the symptoms of porphyria, and this several decades before the disorder was clinically identified".
Röhl also notes further symptoms described in letters between Charlotte and her physician Ernst Schweninger who treated her for over two decades beginning in the early 1890s.
In them, Charlotte variously complains of "toothache, backache, insomnia, dizzy spells, nausea, constipation, excruciating 'wandering' abdominal pains, skin oedema and itching, partial paralysis of the legs and dark red or orange urine," the last of which Röhl calls the "decisive diagnostic symptom.
"


In the 1990s, a team led by Röhl exhumed Charlotte's and Feodora's graves and took samples of each princess for testing.
While the team noted they could not be completely certain that this mutation was caused by the genetic disease, they believed it beyond dispute, based on the historical and biological evidence, and noted that many of the same symptoms were found in Charlotte's mother, Vicky, as well as other family members including Queen Victoria.
Röhl, Warren, and Hunt conclude "...for what else could have caused their terrible attacks of lameness and abdominal pain and skin rashes – and in Charlotte's case dark red urine?



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
  AssignClass (e11bdb93-3ab9-43b5-95fa-edce9fb8eb6b)
 Call ID: e11bdb93-3ab9-43b5-95fa-edce9fb8eb6b
  Args:
    type: :Woman
    source: :Charlotte_of_Prussia
  AssignClass (0c57394e-8ba9-4221-be93-dafe513fba05)
 Call ID: 0c57394e-8ba9-4221-be93-dafe513fba05
  Args:
    source: :Charlotte_of_Prussia
    type: :Person
  AddLiteral (ea0a74b2-e65b-4d09-86bd-9d793c660d60)
 Call ID: ea0a74b2-e65b-4d09-86bd-9d793c660d60
  Args:
    literal_type: xsd:string
    relation: :knownAs
    literal_value: Victoria Elisabeth Augusta Charlotte
    source: :Charlotte_of_Prussia
  AddLiteral (7b705c19-2f23-43bd-b3c1-0c082184a68b)
 Call ID: 7b705c19-2f23-43bd-b3c1-0c082184a68b
  Args:
    source: :Charlotte_of_Prussia
    relation: :hasBirthYear
    literal_value: 1860
    literal_type: xsd:integer
  AddLiteral (d33d67bf-904c-4caf-9d17-d6f6cf3f891f)
 Call ID: d33d67bf-904c-4caf-9d17-d6f6cf3f891f
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1919
    source: :Charlotte_of_Prussia
  AssignClass (de7ba724-32a9-4137-99bf-940cfd43b201)
 Call ID: de7ba724-32a9-4137-99bf-940cfd43b201
  Args:
    type: :Man
    source: :Frederick_William_of_Prussia
  AssignClass (f330148a-152e-4132-bd2e-9a268e9dccc5)
 Call ID: f330148a-152e-4132-bd2e-9a268e9dccc5
  Args:
    source: :Frederick_William_of_Prussia
    type: :Person
  AssignClass (792bbae1-7c75-4c84-aa05-16acbc2abeaa)
 Call ID: 792bbae1-7c75-4c84-aa05-16acbc2abeaa
  Args:
    type: :Woman
    source: :Victoria_Princess_Royal
  AssignClass (a8792ba1-7911-4569-a63c-88df97a92c96)
 Call ID: a8792ba1-7911-4569-a63c-88df97a92c96
  Args:
    source: :Victoria_Princess_Royal
    type: :Person
  AddTriple (28c2f244-9c67-413f-acde-7c658a56a014)
 Call ID: 28c2f244-9c67-413f-acde-7c658a56a014
  Args:
    relation: :hasFather
    source: :Charlotte_of_Prussia
    target: :Frederick_William_of_Prussia
  AddTriple (45720808-1577-4c08-b1d8-cd0b929c134b)
 Call ID: 45720808-1577-4c08-b1d8-cd0b929c134b
  Args:
    relation: :hasMother
    source: :Charlotte_of_Prussia
    target: :Victoria_Princess_Royal
  AssignClass (a42243e7-b02b-4724-9a85-8e02d0385679)
 Call ID: a42243e7-b02b-4724-9a85-8e02d0385679
  Args:
    type: :Man
    source: :Bernhard_III_of_Saxe_Meiningen
  AssignClass (1f189ad8-68be-4a5b-9b19-843ed9cc6bee)
 Call ID: 1f189ad8-68be-4a5b-9b19-843ed9cc6bee
  Args:
    source: :Bernhard_III_of_Saxe_Meiningen
    type: :Person
  AddTriple (7cf716b8-e7ec-4aa0-a52d-c1bcc988622f)
 Call ID: 7cf716b8-e7ec-4aa0-a52d-c1bcc988622f
  Args:
    source: :Charlotte_of_Prussia
    target: :Bernhard_III_of_Saxe_Meiningen
    relation: :hasRelation
  AddLiteral (d1389a6d-f68d-4d75-ab04-7d34858c198b)
 Call ID: d1389a6d-f68d-4d75-ab04-7d34858c198b
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 1878
    source: :Charlotte_of_Prussia
  AssignClass (83a9ce86-979a-4cd5-aef3-c3ca38e285ab)
 Call ID: 83a9ce86-979a-4cd5-aef3-c3ca38e285ab
  Args:
    source: :Feodora_of_Saxe_Meiningen
    type: :Woman
  AssignClass (4dd7f558-0c97-442e-9d32-37f4da121de8)
 Call ID: 4dd7f558-0c97-442e-9d32-37f4da121de8
  Args:
    type: :Person
    source: :Feodora_of_Saxe_Meiningen
  AddTriple (6f12e640-b52d-4fa4-a9ba-60464285dd69)
 Call ID: 6f12e640-b52d-4fa4-a9ba-60464285dd69
  Args:
    relation: :hasMother
    target: :Charlotte_of_Prussia
    source: :Feodora_of_Saxe_Meiningen
  AddTriple (32372fc6-6689-4af8-9d83-327e6a9b3689)
 Call ID: 32372fc6-6689-4af8-9d83-327e6a9b3689
  Args:
    relation: :hasFather
    source: :Feodora_of_Saxe_Meiningen
    target: :Bernhard_III_of_Saxe_Meiningen
  AssignClass (0e164eb7-4732-43bf-9c3b-c0f3498f2767)
 Call ID: 0e164eb7-4732-43bf-9c3b-c0f3498f2767
  Args:
    type: :Man
    source: :Wilhelm_II
  AssignClass (f93510dc-a9e0-43d0-8524-b6df3b2650db)
 Call ID: f93510dc-a9e0-43d0-8524-b6df3b2650db
  Args:
    source: :Wilhelm_II
    type: :Person
  AddTriple (c97fce3f-9784-4d0f-87e5-b6db601db2e9)
 Call ID: c97fce3f-9784-4d0f-87e5-b6db601db2e9
  Args:
    relation: :hasBrother
    source: :Charlotte_of_Prussia
    target: :Wilhelm_II
  AssignClass (2780ccde-e41b-45cf-8264-12332c1feb6f)
 Call ID: 2780ccde-e41b-45cf-8264-12332c1feb6f
  Args:
    source: :Queen_Victoria
    type: :Woman
  AssignClass (b46be2b3-194d-43f3-984e-bd9f7a08920e)
 Call ID: b46be2b3-194d-43f3-984e-bd9f7a08920e
  Args:
    type: :Person
    source: :Queen_Victoria
  AssignClass (6a2bcb52-3c96-4366-a43d-85196755427f)
 Call ID: 6a2bcb52-3c96-4366-a43d-85196755427f
  Args:
    type: :Man
    source: :Prince_Albert
  AssignClass (ee284adc-2207-47ee-9c77-5090e083dc6f)
 Call ID: ee284adc-2207-47ee-9c77-5090e083dc6f
  Args:
    source: :Prince_Albert
    type: :Person
  AddTriple (3fd41380-af1b-41ca-bfd2-ff981f96d0c5)
 Call ID: 3fd41380-af1b-41ca-bfd2-ff981f96d0c5
  Args:
    relation: :hasMother
    target: :Queen_Victoria
    source: :Victoria_Princess_Royal
  AddTriple (6e24aea6-872a-4d8e-8839-061d434056f4)
 Call ID: 6e24aea6-872a-4d8e-8839-061d434056f4
  Args:
    source: :Victoria_Princess_Royal
    target: :Prince_Albert
    relation: :hasFather
  Finish (240d1315-b01a-4c71-a310-7652ca0b9eb5)
 Call ID: 240d1315-b01a-4c71-a310-7652ca0b9eb5
  Args: