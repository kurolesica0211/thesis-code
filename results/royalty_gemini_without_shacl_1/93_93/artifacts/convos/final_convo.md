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
Prince George of Greece and Denmark (Greek: Γεώργιος, romanized: Geórgios; 24 June 1869 – 25 November 1957) was the second son and child of George I of Greece and Olga Konstantinovna of Russia.
He served as high commissioner of the Cretan State during its transition towards independence from Ottoman rule and union (Enosis) with Greece.
Childhood

Born at Mon Repos palace in Corfu, Prince George spent his childhood in Greece with his parents and his six siblings, splitting their time between the Royal Palace on Syntagma Square and the Tatoi Palace, north of Athens, at the foot of Mount Parnitha.
George I often reminded his children: "Never forget that you are strangers among the Greeks, and make sure they never remember it".
A typical day for young Prince George and his siblings began at 6am, with a cold bath.
George followed this routine until the age of fourteen, after which he was allowed to dine with his elders, but still had to be in bed at precisely 10pm.
George and his brothers were taught by three foreign tutors:
The children's mother tongue was English, which they spoke with their parents, but their father, George I, insisted that they use Greek during their lessons.
George was not a particularly bright student.
Naval training with Prince Valdemar

In 1883, George's father sent him to live at Bernstorff Palace near Copenhagen in Denmark.
George was to enlist in the Danish royal navy, aged just fourteen.
While in Denmark, the teenage George was in the care of his grandfather, King Christian IX, and his youngest uncle, Prince Valdemar.
However, George and Valdemar's relationship quickly developed beyond familial relations.
While watching his parents' boat leave Denmark, George was overwhelmed by a strong sense of abandonment.
Realising this, Valdemar took George's hand.
For the teenage George, this sign of affection was a revelation.
This passion between the two men would last until Prince Valdemar's death on 14th January 1939.
Even after they were both married, George and Valdemar would meet every year for several weeks, in Denmark or abroad.
As his duty as a prince was principally to have a family and continue the royal family line, George's family sought to find him a wife.
In 1888, while his older brother Prince Constantine's marriage was being arranged with Sophie of Prussia, negociations were begun for a marriage the following year for George and Princess Marguerite of Orléans.
This marriage would have made George Valdemar's brother-in-law, as Marguerite's sister Marie was Valdemar's wife.
However the negociations fell through and George remained single for several years.
The Ōtsu Incident

After his time with the Danish fleet, Prince George left to pursue his naval training in Russia, where he was made Lieutenant of the imperial navy.
However, their stay in Japan would make a lasting mark on George's life.
On the 11th May 1891, Tsuda Sanzō, a Japanese policeman escorting the Russian crown prince attempted to assassinate Nicholas, striking him twice with a sabre.
George was able to knock Sanzō unconscious with his cane, saving the life of the future Tsar.
The Greek Prince's actions prompted immediate thanks from the representatives of Japanese emperor Meiji Tenno, who was anxious to preserve good relations between Japan and Russia.
The emperor and his wife gifted George an elephant made of Satsuma porcelaine.
However, the news of the attack that reached Europe did not portray George as his cousin's saviour.
The version of the incident that arrived at Saint Petersburg reported Prince George as the assassin.
According to this account, the young Prince had taken his cousin into dangerous areas and then encouraged him to desecrate a temple which provoked the people's anger.
George was forced to leave his cousin, in disgrace, causing lasting damage to his reputation.
First modern Olympic games

George, along with his brothers Constantine and Nicholas, were involved with the organization of the 1896 Summer Olympics in Athens — the first modern Olympic games.
George served as president of the Sub-Committee for Nautical Sports on the newly created Hellenic Olympic Committee.
During the marathon event, won by the shepherd Spiridon Louis, George and Constantine left the spectator's stand to run the last metres with the runner.
As President of the Olympic judges, George was involved in examining the case of Hungarian sprinter Gyula Kellner, who disputed his fourth place ranking, against the Greek Spyridon Belokas in third place.
The Prince decided to disqualify Belokas.
The Games were a great success for Greece, revitalising Greek national pride.
In February 1897, a Greek navy fleet, lead by Prince George was sent to Souda bay by the Prime Minister Theodoros Deligiannis's government.
When 2,000 Greek volunteers landed in Crete, George was commanding a flotilla of six torpedo boats that patrolled in northern Cretan waters to prevent any intervention from the Ottoman navy.
By the end of March, the Great Powers were considering George to be the island's governor.
It is thought that France proposed the post of High Commissioner, whereas Russia suggested the title of the 'Prince of Candia', rather than merely being a governor.
In April, Greece declared war on the Ottoman empire, known as the Thirty days' war.
Prince George, not yet thirty, was made High Commissioner, and a joint Muslim-Christian assembly was part-elected, part-appointed.
However, this was not enough to satisfy Cretan desire for union with Greece.
Eleftherios Venizelos was the leader of the movement to unite Crete with Greece.
He had fought in the earlier revolts and was now a member of the Assembly, acting as minister of justice to Prince George.
George, a staunch royalist, had assumed absolute power.
During the revolt, the newly created Cretan Gendarmerie remained faithful to George.
In this difficult period, the Cretan population were divided: in the 1906 elections the pro-Prince parties took 38,127 votes, while pro-Venizelos parties took 33,279.
Finally, in September 1906, George was forced to resign and was replaced by former Greek prime minister and future president Alexandros Zaimis.
George left the island and, in 1908, the Cretan Assembly unilaterally declared enosis (union) with Greece.
In October 1912 George returned from Paris to Athens so that he could join the naval ministry as Greece prepared for war against the Ottoman Empire.
Later he served as aide-de-camp to King George who, however, was assassinated in March 1913.
Following the assassination, George temporarily moved to Copenhagen to settle his father's financial affairs there, as he had never ceased to be a Prince of Denmark.
Marriage and family


Following a Parisian luncheon between King George and Prince Roland Bonaparte in September 1906 during which the king agreed to the prospect of a marriage between their children, George met Roland's daughter, Princess Marie Bonaparte (2 July 1882 – 21 September 1962) on 19 July 1907 at the Bonapartes' home in Paris.
A member of one of the non-imperial branches of the Bonaparte dynasty, she was an heiress to the Blanc casino fortune through her mother.
Although a homosexual, who lived most of the year with his uncle Prince Valdemar of Denmark with whom he had a life-long relationship, he dutifully courted her for twenty-eight days.
He also admitted that, contrary to what he knew were her hopes, he could not commit to living in France permanently since he had to remain prepared to undertake royal duties in Greece or Crete if summoned to do so.
Once his proposal of marriage was tentatively accepted, the bride's father was astonished when George waived any contractual clause guaranteeing an allowance or inheritance from Marie; she would retain and manage her own fortune (a trust yielding 800,000 francs per annum) and only their future children would receive legacies.
George wed Marie in a civil ceremony in Paris on 21 November 1907 at the town hall in the 16th arrondissement.
George's groomsmen were his brother Nicholas and the Greek minister Nikolaos Deligiannis.
Marie's bridesmaids were her two aunts: Princess Jeanne Bonaparte and Louise Radziwill.
They also held a second Greek Orthodox ceremony in Athens the following December, during which George's uncle Valdemar served as the koumbaros.
To avoid facing his Greek political enemies, George would have preferred to have the religious ceremony in France, but his family would not hear of it.
By March Marie was pregnant and, as agreed, the couple returned to France to take up residence.
When George brought his bride to Bernstorff for the first family visit, Valdemar's wife Marie d'Orléans was at pains to explain to Marie Bonaparte the intimacy which united uncle and nephew, so deep that at the end of each of George's several yearly visits to Bernstorff, he would weep, Valdemar would take sick, and the women learned the patience not to intrude upon their husbands' private moments.
During the first of these visits, Marie Bonaparte and Valdemar found themselves engaging in the kind of passionate intimacies she had looked forward to with her husband who, however, only seemed to enjoy them vicariously, sitting or lying beside his wife and uncle.
On a later visit, Marie Bonaparte carried on a passionate flirtation with Prince Aage, Valdemar's eldest son.
In neither case does it appear that George objected, or felt obliged to give the matter any attention.
However, George criticized Marie d'Orléans to his wife, alleging that she drank too much and was having an affair with his uncle's stablemaster.
But Marie Bonaparte found no fault with her husband's aunt, rather, she admired the forbearance and independence of Valdemar's wife under circumstances which caused her bewilderment and estrangement from her own husband.
From 1913 to early 1916, George's wife carried on an intense flirtation, then an affair until May 1919 with French prime minister Aristide Briand.
In 1915 Briand wrote to Marie that, having come to know and like Prince George, he felt guilty about their secret passion.
George tried to persuade him that Greece, officially neutral during World War I but suspected of sympathy for the Central Powers, really hoped for an Allied victory: He may have influenced Briand to support the disastrous Allied expedition against the Turks at Salonika.
When the prince and princess returned in July 1915 to France following a visit to the ailing King Constantine I in Greece, her affair with Briand had become notorious and George expressed a restrained jealousy.
By December 1916 the French fleet was bombing Athens and in Paris Briand was suspected, alternately, of having seduced Marie in a futile attempt to bring Greece over to the Allied side, or of having been seduced by her to oust Constantine and set George upon the Greek throne.
Although he was on friendly terms with his wife's mentor, Sigmund Freud, in 1925 George asked Marie to give up her work as a psychoanalyst to devote herself to their family life, but she declined.
When he learned from the newspapers in 1938 that his only son had married a Russian commoner, George forbade him to return home and refused ever to meet his wife.
Prince George and Princess Marie had two children, Petros and Evgenia.
In 1948, Prince George was named as one of the sponsors/godparents of his grandnephew Prince Charles of the United Kingdom (later King Charles III) along with King George VI, King Haakon VII of Norway, Queen Mary, Princess Margaret, the Dowager Marchioness of Milford Haven, Pamela, Lady Brabourne, and David Bowes-Lyon.
Death

On 21 November 1957 Princess Marie and her husband celebrated their golden wedding anniversary.
Prince George died 25 November 1957, aged eighty-eight, the longest-living dynast of the House of Oldenburg of his generation.
Prince George was the last living child of King George and Queen Olga.
Georgioupolis, a coastal resort between Chania and Rethimno, was named after Prince George.



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
  AssignClass (b58f9090-b199-4cf1-987c-0e7cdf4cef6f)
 Call ID: b58f9090-b199-4cf1-987c-0e7cdf4cef6f
  Args:
    source: Prince_George_of_Greece_and_Denmark
    type: :Man
  AssignClass (789ff800-898b-490a-aa83-7483c3092aeb)
 Call ID: 789ff800-898b-490a-aa83-7483c3092aeb
  Args:
    type: :Man
    source: George_I_of_Greece
  AssignClass (ce1b3f12-d607-4dbe-9472-a1d91c574c4d)
 Call ID: ce1b3f12-d607-4dbe-9472-a1d91c574c4d
  Args:
    source: Olga_Konstantinovna_of_Russia
    type: :Woman
  AddLiteral (b5c596cf-7121-43c9-9e34-70758e096081)
 Call ID: b5c596cf-7121-43c9-9e34-70758e096081
  Args:
    source: Prince_George_of_Greece_and_Denmark
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1869
  AddLiteral (a7a59b75-c220-4d5b-a159-81348bc7de9a)
 Call ID: a7a59b75-c220-4d5b-a159-81348bc7de9a
  Args:
    relation: :hasDeathYear
    source: Prince_George_of_Greece_and_Denmark
    literal_value: 1957
    literal_type: xsd:integer
  AddTriple (46aa3589-8411-445f-a2d1-4faacea6b594)
 Call ID: 46aa3589-8411-445f-a2d1-4faacea6b594
  Args:
    source: Prince_George_of_Greece_and_Denmark
    relation: :hasFather
    target: George_I_of_Greece
  AddTriple (6c8a41ea-241a-416c-a909-5e2a6bc3c50f)
 Call ID: 6c8a41ea-241a-416c-a909-5e2a6bc3c50f
  Args:
    source: Prince_George_of_Greece_and_Denmark
    relation: :hasMother
    target: Olga_Konstantinovna_of_Russia
  AssignClass (79c0b4ff-dbc6-454e-a3f3-074997671477)
 Call ID: 79c0b4ff-dbc6-454e-a3f3-074997671477
  Args:
    type: :Man
    source: Christian_IX_of_Denmark
  AddTriple (57e8718b-dc86-4080-a948-96e2d6d53994)
 Call ID: 57e8718b-dc86-4080-a948-96e2d6d53994
  Args:
    source: George_I_of_Greece
    relation: :hasFather
    target: Christian_IX_of_Denmark
  AssignClass (543c7f06-aa6d-4d7a-9493-ef9b463770be)
 Call ID: 543c7f06-aa6d-4d7a-9493-ef9b463770be
  Args:
    type: :Man
    source: Prince_Valdemar_of_Denmark
  AddTriple (f255cd4a-70f7-4d9a-9827-c7b30c187eda)
 Call ID: f255cd4a-70f7-4d9a-9827-c7b30c187eda
  Args:
    source: Prince_Valdemar_of_Denmark
    relation: :hasFather
    target: Christian_IX_of_Denmark
  AssignClass (c66fc8fd-5310-470c-88fd-9bf72788b827)
 Call ID: c66fc8fd-5310-470c-88fd-9bf72788b827
  Args:
    type: :Man
    source: Prince_Constantine_of_Greece
  AddTriple (7e391c79-0562-4009-b409-7605a1881255)
 Call ID: 7e391c79-0562-4009-b409-7605a1881255
  Args:
    target: George_I_of_Greece
    source: Prince_Constantine_of_Greece
    relation: :hasFather
  AddTriple (7da0a33f-8fc3-4592-a754-5ff96f4ad11f)
 Call ID: 7da0a33f-8fc3-4592-a754-5ff96f4ad11f
  Args:
    target: Prince_Constantine_of_Greece
    source: Prince_George_of_Greece_and_Denmark
    relation: :isSiblingOf
  AssignClass (8d02faa1-1433-4531-91e5-5a4af7573a6f)
 Call ID: 8d02faa1-1433-4531-91e5-5a4af7573a6f
  Args:
    type: :Man
    source: Prince_Nicholas_of_Greece
  AddTriple (7dab5b2f-9fbe-4fc2-94bb-43a38cc9bb62)
 Call ID: 7dab5b2f-9fbe-4fc2-94bb-43a38cc9bb62
  Args:
    target: George_I_of_Greece
    source: Prince_Nicholas_of_Greece
    relation: :hasFather
  AddTriple (884dccbe-0f77-442d-9135-8294966f6789)
 Call ID: 884dccbe-0f77-442d-9135-8294966f6789
  Args:
    target: Prince_Nicholas_of_Greece
    source: Prince_George_of_Greece_and_Denmark
    relation: :isSiblingOf
  AssignClass (54dc9673-4e1f-407e-af31-f1f584b40671)
 Call ID: 54dc9673-4e1f-407e-af31-f1f584b40671
  Args:
    source: Princess_Marie_Bonaparte
    type: :Woman
  AddLiteral (3674931b-c8e3-4786-bec7-d9302aae4f63)
 Call ID: 3674931b-c8e3-4786-bec7-d9302aae4f63
  Args:
    literal_type: xsd:integer
    literal_value: 1907
    relation: :hasMarriageYear
    source: Prince_George_of_Greece_and_Denmark
  AddTriple (3d071b77-c482-438a-8d05-435fe146eaeb)
 Call ID: 3d071b77-c482-438a-8d05-435fe146eaeb
  Args:
    target: Princess_Marie_Bonaparte
    source: Prince_George_of_Greece_and_Denmark
    relation: :hasRelation
  AssignClass (98457cbd-ebdd-4ee6-a3ca-4d15a945a1c3)
 Call ID: 98457cbd-ebdd-4ee6-a3ca-4d15a945a1c3
  Args:
    type: :Man
    source: Prince_Roland_Bonaparte
  AddTriple (7c05ac1d-ac2f-4ff8-a752-417c0da93288)
 Call ID: 7c05ac1d-ac2f-4ff8-a752-417c0da93288
  Args:
    source: Princess_Marie_Bonaparte
    relation: :hasFather
    target: Prince_Roland_Bonaparte
  AssignClass (7f30208d-1a91-4c6c-9c54-fc160d0a955d)
 Call ID: 7f30208d-1a91-4c6c-9c54-fc160d0a955d
  Args:
    type: :Man
    source: Petros_of_Greece_and_Denmark
  AddTriple (b8ad96d0-7ba8-494d-879e-783def053f89)
 Call ID: b8ad96d0-7ba8-494d-879e-783def053f89
  Args:
    source: Petros_of_Greece_and_Denmark
    relation: :hasFather
    target: Prince_George_of_Greece_and_Denmark
  AddTriple (dc0b1782-11f5-40b0-9e15-2a461e047175)
 Call ID: dc0b1782-11f5-40b0-9e15-2a461e047175
  Args:
    target: Princess_Marie_Bonaparte
    source: Petros_of_Greece_and_Denmark
    relation: :hasMother
  AssignClass (a401c1a1-446e-4874-b404-6186cad587ca)
 Call ID: a401c1a1-446e-4874-b404-6186cad587ca
  Args:
    source: Evgenia_of_Greece_and_Denmark
    type: :Woman
  AddTriple (4f1d2975-91c0-4f54-8979-8ad75575e810)
 Call ID: 4f1d2975-91c0-4f54-8979-8ad75575e810
  Args:
    target: Prince_George_of_Greece_and_Denmark
    source: Evgenia_of_Greece_and_Denmark
    relation: :hasFather
  AddTriple (de1ffc91-e00d-49e1-afc0-c90c5ecab5e8)
 Call ID: de1ffc91-e00d-49e1-afc0-c90c5ecab5e8
  Args:
    target: Princess_Marie_Bonaparte
    source: Evgenia_of_Greece_and_Denmark
    relation: :hasMother
  AssignClass (4f14a3e2-6e5f-4ae5-bbc2-e47302ab5999)
 Call ID: 4f14a3e2-6e5f-4ae5-bbc2-e47302ab5999
  Args:
    type: :Woman
    source: Marie_dOrleans
  AddTriple (5d06513f-114f-45e4-9dea-dd92262907cf)
 Call ID: 5d06513f-114f-45e4-9dea-dd92262907cf
  Args:
    source: Prince_Valdemar_of_Denmark
    relation: :hasRelation
    target: Marie_dOrleans
  AssignClass (5f00fb7d-497a-4132-a349-5da6d6833012)
 Call ID: 5f00fb7d-497a-4132-a349-5da6d6833012
  Args:
    type: :Man
    source: Prince_Aage_of_Denmark
  AddTriple (cac98bbb-064b-4d2f-b710-b3f0df8446dd)
 Call ID: cac98bbb-064b-4d2f-b710-b3f0df8446dd
  Args:
    target: Prince_Valdemar_of_Denmark
    source: Prince_Aage_of_Denmark
    relation: :hasFather
  AddTriple (92c64c8f-10fd-4776-b272-53cc71a65f40)
 Call ID: 92c64c8f-10fd-4776-b272-53cc71a65f40
  Args:
    target: Marie_dOrleans
    source: Prince_Aage_of_Denmark
    relation: :hasMother
  Finish (d1f72bc2-ced6-4d6d-ab06-49babe753587)
 Call ID: d1f72bc2-ced6-4d6d-ab06-49babe753587
  Args: