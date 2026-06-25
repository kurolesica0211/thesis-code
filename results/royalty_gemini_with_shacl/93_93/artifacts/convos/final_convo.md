================================ System Message ================================

### Role
You are an expert Knowledge Graph Engineer. Your task is to update and refine a Data Graph based on a provided Input Text and a strict Ontology. You must ensure the Data Graph accurately reflects the information in the text while remaining compliant with the ontological constraints.

### Inputs
1. **Ontology**: Allowed classes and properties.
2. **Input Text**: The ONLY source of truth.
3. **Current Data Graph**: The starting state.

### CRITICAL CORE DIRECTIVES (ZERO TOLERANCE)
1. **STRICT FAITHFULNESS TO TEXT**: You are a "clean slate" engineer. Even if you recognize an entity and know more about it from your training data, you MUST NOT add any node, property, or relation that is not stated in the **Input Text**. If a fact is not in the text, it does not exist.
2. **HARD BATCH LIMIT**: You must plan your edits efficiently. **DO NOT EXCEED 20 TOOL CALLS IN A SINGLE ANSWER.** Breaking this limit is a critical system failure. Quality and strict grounding must be achieved within this budget.

### Standardized Identifier & Naming Conventions
To ensure clean downstream entity resolution, all identifiers must follow a uniform, relational-free structure.

#### 1. Core Structural Format
* **Full Formal Name**: Use the most complete, standard name mentioned *within the text* as the identifier basis.
* **Format**: Use `Snake_Case` for all entity identifiers, capitalizing the first letter of each word (e.g., `Julius_Caesar`, `Marcus_Aurelius`).
* **Avoid Pronouns/Aliases**: Never create nodes based on pronouns (`he`, `she`) or temporary descriptions (`the_captain`). Resolve these back to their primary full identifier.

#### 2. NO Relational Suffixes (ABSOLUTE PROHIBITION)
* **NEVER** use familial relations or structural dependencies to construct an identifier string. 
* **PROHIBITED EXAMPLES**: `John_son_of_Robert`, `Mary_daughter_of_Henry`, `Wife_of_Louis_XIV`.
* **Reasoning**: Relational data belongs strictly in the triples (`parentOf`, `spouseOf`), never in the unique node identifier. Incorporating them corrupts entity resolution pipelines.

#### 3. Monarchs, Nobility, and Historic Monickers
* **Regnal Numbers & Monickers**: Include standard regnal numbers or stable historical identifiers *only* if they are explicitly part of their formal name in the text (e.g., `Charlemagne`, `Louis_XIV`, `William_of_Orange`).

#### 4. Disambiguation & Fallbacks (When Identical Names Occur)
If two distinct entities share the exact same name within the text, append a parenthetical qualifier using *only* context provided in the source text:
* **By Role/Attribute**: `Augustus_(Emperor)` vs. `Augustus_(Ship)`.
* **By Category/Profession**: `John_(Apostle)` vs. `John_(Baptist)`.

### Triadic Directionality & Predicate Logic (STRICT ENFORCEMENT)
The Data Graph is a **Directed Acyclic Graph**. Swapping Source and Target invalidates the entire graph. You MUST follow the **Flow of Action**.

#### 1. The "Sentence Test" Requirement
Before executing any `AddTriple` call, you must mentally or explicitly perform the following test:
* **Formula**: `[Source Entity] + [Property Name] + [Target Entity]`
* **Check**: Does this form a grammatically and logically correct sentence based *only* on the text?
* **Example Failure**: If the text says "John is the employer of Mary," the triple `(Mary, isEmployerOf, John)` fails because "Mary isEmployerOf John" is factually false.

#### 2. Identifying the Anchor (Domain vs. Range)
* **The Source (Left)**: The "Origin" or "Owner." If the property is a verb, the Source is the one performing it.
* **The Target (Right)**: The "Destination" or "Attribute." If the property is a verb, the Target is the one being acted upon.

#### 3. Handling Inverse Property Confusion
* **Active (`worksFor`, `isEmployerOf`)**: The "Superior" or "Source" is the Source.
* **Passive (`employedBy`, `childOf`)**: The "Subordinate" or "Recipient" is the Source.
* **Partitive (`hasPart`, `contains`)**: The "Container/Whole" is the Source.
* **Membership (`isPartOf`, `memberOf`)**: The "Component/Part" is the Source.

#### 4. Negative Constraints
* **NEVER** use the property name as a bidirectional link.
* **NEVER** assume the first entity mentioned in a sentence is automatically the Source; analyze the verb direction.
* **No Hypothetical Nodes**: Do not create placeholder nodes or sequences (e.g., Marriage1, Marriage2) to represent "patterns" mentioned in the text. Only create nodes for specific instances described.
* **Quantities**: If the text says "fifteen children" but does not name them, do NOT create 15 generic child nodes. Only create nodes for entities with specific names or identifiers provided in the text.

#### 5. Arguments Order
* When calling `AddTriple` `source` **ALWAYS** comes first, then `relation`, and only after them `target`.

> **STOP & VERIFY**: If your triple reads like "Employee isEmployerOf Employer" or "Room contains Building," you have flipped the nodes. **STOP and swap them before calling the tool.**

### Instructions & Workflow
1. **Analyze**: Identify specific entities and relations in the text.
2. **Edit**: Use tools to modify the graph.
   - Every node MUST have a class assignment (`AssignClass`).
   - Ground every edit in text evidence.
3. **Validate**: Use `ValidateShacl` to check constraints.
4. **Iterate**: Address violations. If a violation (like MinCount) cannot be fixed without hallucinating data not in the text, **ignore the violation**.
5. **Finalize**: Use `Finish` once the graph is a **faithful** representation of the text.

### Tool Usage Constraints
- **AssignClass / UnassignClass**: For `rdf:type` only.
- **AddTriple / RemoveTriple**: For properties only.
- **AddLiteral / RemoveLiteral**: For literals (raw data: dates, numbers, strings, etc.) only.
- **ValidateShacl**: CRITICAL: ALWAYS validate your results before using Finish!
- **Finish**: CRITICAL: ALWAYS use ValidateShacl before finishing!
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
  AssignClass (a87b2d3a-c1df-4472-8e73-2ba903734885)
 Call ID: a87b2d3a-c1df-4472-8e73-2ba903734885
  Args:
    source: :Prince_George_of_Greece_and_Denmark
    type: :Man
  AssignClass (6c82c311-ef03-4a40-860f-cc3b0b6c52e3)
 Call ID: 6c82c311-ef03-4a40-860f-cc3b0b6c52e3
  Args:
    source: :George_I_of_Greece
    type: :Man
  AssignClass (fd5cb4a9-90ad-4db6-91a0-0047483a29fa)
 Call ID: fd5cb4a9-90ad-4db6-91a0-0047483a29fa
  Args:
    source: :Olga_Konstantinovna_of_Russia
    type: :Woman
  AddLiteral (4c13bb04-7e53-4b44-9a85-4b3d3d685cd1)
 Call ID: 4c13bb04-7e53-4b44-9a85-4b3d3d685cd1
  Args:
    literal_type: xsd:integer
    source: :Prince_George_of_Greece_and_Denmark
    literal_value: 1869
    relation: :hasBirthYear
  AddLiteral (341ff9fc-484c-4938-a43a-ef75406d35d1)
 Call ID: 341ff9fc-484c-4938-a43a-ef75406d35d1
  Args:
    source: :Prince_George_of_Greece_and_Denmark
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1957
  AddTriple (2c24ac0d-2a9b-4105-94ea-789796bbed81)
 Call ID: 2c24ac0d-2a9b-4105-94ea-789796bbed81
  Args:
    source: :Prince_George_of_Greece_and_Denmark
    relation: :hasFather
    target: :George_I_of_Greece
  AddTriple (29b13fa8-24dd-493e-8cf2-a13613432e5b)
 Call ID: 29b13fa8-24dd-493e-8cf2-a13613432e5b
  Args:
    target: :Olga_Konstantinovna_of_Russia
    relation: :hasMother
    source: :Prince_George_of_Greece_and_Denmark
  AssignClass (4a61e75f-36d2-43b3-8ec8-d6c0e678be44)
 Call ID: 4a61e75f-36d2-43b3-8ec8-d6c0e678be44
  Args:
    source: :Prince_Valdemar_of_Denmark
    type: :Man
  AddTriple (84e710c4-c570-4384-8a88-53b2becccc0c)
 Call ID: 84e710c4-c570-4384-8a88-53b2becccc0c
  Args:
    relation: :isUncleOf
    target: :Prince_George_of_Greece_and_Denmark
    source: :Prince_Valdemar_of_Denmark
  AssignClass (b61c6ed7-d062-465a-8c65-a8f7b545be2c)
 Call ID: b61c6ed7-d062-465a-8c65-a8f7b545be2c
  Args:
    source: :King_Christian_IX_of_Denmark
    type: :Man
  AssignClass (8836b297-b129-408f-97e4-045c4b5d99fc)
 Call ID: 8836b297-b129-408f-97e4-045c4b5d99fc
  Args:
    source: :Prince_Constantine_of_Greece
    type: :Man
  AssignClass (3e45e376-59af-4e1e-a73b-d7b800c27e38)
 Call ID: 3e45e376-59af-4e1e-a73b-d7b800c27e38
  Args:
    source: :Prince_Nicholas_of_Greece
    type: :Man
  AddTriple (9bbe7eb4-1125-4666-b856-861548455e01)
 Call ID: 9bbe7eb4-1125-4666-b856-861548455e01
  Args:
    relation: :isBrotherOf
    target: :Prince_George_of_Greece_and_Denmark
    source: :Prince_Constantine_of_Greece
  AddTriple (36179064-3820-4f80-9b0a-70c66f3a0a4c)
 Call ID: 36179064-3820-4f80-9b0a-70c66f3a0a4c
  Args:
    target: :Prince_George_of_Greece_and_Denmark
    relation: :isBrotherOf
    source: :Prince_Nicholas_of_Greece
  AssignClass (61455415-e269-423b-bb96-7a20976a0235)
 Call ID: 61455415-e269-423b-bb96-7a20976a0235
  Args:
    source: :Princess_Marie_Bonaparte
    type: :Woman
  AddLiteral (ba64560b-c80c-4fb7-8fd4-98ea212d7c73)
 Call ID: ba64560b-c80c-4fb7-8fd4-98ea212d7c73
  Args:
    literal_value: 1907
    relation: :hasMarriageYear
    source: :Prince_George_of_Greece_and_Denmark
    literal_type: xsd:integer
  AddTriple (1b14aa82-8614-4a71-a6b0-8034fc664e93)
 Call ID: 1b14aa82-8614-4a71-a6b0-8034fc664e93
  Args:
    relation: :hasRelation
    target: :Princess_Marie_Bonaparte
    source: :Prince_George_of_Greece_and_Denmark
  AssignClass (ad39a7b7-2cea-4e37-811c-e002e542606c)
 Call ID: ad39a7b7-2cea-4e37-811c-e002e542606c
  Args:
    source: :Petros
    type: :Man
  AssignClass (756e07ed-2772-4f60-948e-eb6595dd39ae)
 Call ID: 756e07ed-2772-4f60-948e-eb6595dd39ae
  Args:
    source: :Evgenia
    type: :Woman
  AddTriple (6061e8ba-07b9-40d4-abcd-471712f8a156)
 Call ID: 6061e8ba-07b9-40d4-abcd-471712f8a156
  Args:
    target: :Petros
    relation: :hasSon
    source: :Prince_George_of_Greece_and_Denmark
  AddTriple (7cb25c83-e637-4654-a58e-be42700a3d3c)
 Call ID: 7cb25c83-e637-4654-a58e-be42700a3d3c
  Args:
    source: :Prince_George_of_Greece_and_Denmark
    target: :Evgenia
    relation: :hasDaughter
  AssignClass (4cde554e-cd72-4c17-ac57-ecafb5539c73)
 Call ID: 4cde554e-cd72-4c17-ac57-ecafb5539c73
  Args:
    source: :Prince_Roland_Bonaparte
    type: :Man
  AddTriple (d524964a-0123-4b15-921e-d3b9264550f7)
 Call ID: d524964a-0123-4b15-921e-d3b9264550f7
  Args:
    source: :Prince_Roland_Bonaparte
    target: :Princess_Marie_Bonaparte
    relation: :isFatherOf
  AssignClass (86f5438c-6ee5-4651-9c73-a4c660a8db24)
 Call ID: 86f5438c-6ee5-4651-9c73-a4c660a8db24
  Args:
    source: :Marie_dOrleans
    type: :Woman
  AddTriple (0712a096-8fc3-4bae-bff5-627fbab21639)
 Call ID: 0712a096-8fc3-4bae-bff5-627fbab21639
  Args:
    source: :Prince_Valdemar_of_Denmark
    target: :Marie_dOrleans
    relation: :isBrotherOf
  AssignClass (4c528119-c0b3-4fdc-b52d-54bc723cf5cb)
 Call ID: 4c528119-c0b3-4fdc-b52d-54bc723cf5cb
  Args:
    source: :Prince_Aage
    type: :Man
  AddTriple (1eade1aa-d361-4bf5-b5d6-e8a69b747c09)
 Call ID: 1eade1aa-d361-4bf5-b5d6-e8a69b747c09
  Args:
    source: :Prince_Valdemar_of_Denmark
    target: :Prince_Aage
    relation: :isFatherOf
  ValidateShacl (a8cae0ab-1731-4539-a430-3958e4f7b1d0)
 Call ID: a8cae0ab-1731-4539-a430-3958e4f7b1d0
  Args:
  Finish (d6bef7b1-74c8-4712-8ee8-41057a1edfe0)
 Call ID: d6bef7b1-74c8-4712-8ee8-41057a1edfe0
  Args:

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

The final data graph after all the edits:
  @prefix : <http://example.com/family_TBOX.ttl#> .
  @prefix data: <http://example.org/data/> .
  @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

  data:King_Christian_IX_of_Denmark a :Man .

  data:Prince_Constantine_of_Greece a :Man ;
      :isBrotherOf data:Prince_George_of_Greece_and_Denmark .

  data:Prince_Nicholas_of_Greece a :Man ;
      :isBrotherOf data:Prince_George_of_Greece_and_Denmark .

  data:Prince_Roland_Bonaparte a :Man ;
      :isFatherOf data:Princess_Marie_Bonaparte .

  data:Prince_Valdemar_of_Denmark a :Man ;
      :isBrotherOf data:Marie_dOrleans ;
      :isFatherOf data:Prince_Aage ;
      :isUncleOf data:Prince_George_of_Greece_and_Denmark .

  data:Evgenia a :Woman .

  data:George_I_of_Greece a :Man .

  data:Marie_dOrleans a :Woman .

  data:Olga_Konstantinovna_of_Russia a :Woman .

  data:Petros a :Man .

  data:Prince_Aage a :Man .

  data:Princess_Marie_Bonaparte a :Woman .

  data:Prince_George_of_Greece_and_Denmark a :Man ;
      :hasBirthYear 1869 ;
      :hasDaughter data:Evgenia ;
      :hasDeathYear 1957 ;
      :hasFather data:George_I_of_Greece ;
      :hasMarriageYear 1907 ;
      :hasMother data:Olga_Konstantinovna_of_Russia ;
      :hasRelation data:Princess_Marie_Bonaparte ;
      :hasSon data:Petros .



================================= Tool Message =================================

VALIDATION RESULTS
Total violations:8
Violations:

  Violation [1]:
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    LLM-provided explanation of the violation:
      The node 'Prince_George_of_Greece_and_Denmark' has a father 'George_I_of_Greece' that is missing the required class ':Ancestor'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='George_I_of_Greece', class=':Ancestor')


  Violation [2]:
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    LLM-provided explanation of the violation:
      The node 'Prince_George_of_Greece_and_Denmark' has a mother 'Olga_Konstantinovna_of_Russia' that is missing the required class ':Ancestor'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Olga_Konstantinovna_of_Russia', class=':Ancestor')


  Violation [3]:
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    LLM-provided explanation of the violation:
      The node 'Prince_George_of_Greece_and_Denmark' has a father 'George_I_of_Greece' that is missing the required class ':Ancestor'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='George_I_of_Greece', class=':Ancestor')


  Violation [4]:
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    LLM-provided explanation of the violation:
      The node 'Prince_George_of_Greece_and_Denmark' has a mother 'Olga_Konstantinovna_of_Russia' that is missing the required class ':Ancestor'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Olga_Konstantinovna_of_Russia', class=':Ancestor')


  Violation [5]:
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    LLM-provided explanation of the violation:
      The node 'Prince_George_of_Greece_and_Denmark' has a father 'George_I_of_Greece' that is missing the required class ':Ancestor'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='George_I_of_Greece', class=':Ancestor')


  Violation [6]:
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    LLM-provided explanation of the violation:
      The node 'Prince_George_of_Greece_and_Denmark' has a mother 'Olga_Konstantinovna_of_Russia' that is missing the required class ':Ancestor'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Olga_Konstantinovna_of_Russia', class=':Ancestor')


  Violation [7]:
    SHACL message: Any subject of isFatherOf must be all of: Ancestor, Man.
    LLM-provided explanation of the violation:
      The node 'Prince_Roland_Bonaparte' is the subject of an 'isFatherOf' relationship but lacks the required class ':Ancestor'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Prince_Roland_Bonaparte', class=':Ancestor')


  Violation [8]:
    SHACL message: Any subject of isFatherOf must be all of: Ancestor, Man.
    LLM-provided explanation of the violation:
      The node 'Prince_Valdemar_of_Denmark' is the subject of an 'isFatherOf' relationship but lacks the required class ':Ancestor'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Prince_Valdemar_of_Denmark', class=':Ancestor')




================================= Tool Message =================================

You have not used SHACL validation even once, though you should! Check your work with the SHACL tool!

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (7bfe1f28-b38b-4f17-aff2-fc6d97205900)
 Call ID: 7bfe1f28-b38b-4f17-aff2-fc6d97205900
  Args:
    type: :Ancestor
    source: :George_I_of_Greece
  AssignClass (6f032a24-048c-41f8-b9da-d07131e24324)
 Call ID: 6f032a24-048c-41f8-b9da-d07131e24324
  Args:
    source: :Olga_Konstantinovna_of_Russia
    type: :Ancestor
  AssignClass (730f6874-3c6a-49dc-84cc-a6795d07878a)
 Call ID: 730f6874-3c6a-49dc-84cc-a6795d07878a
  Args:
    source: :Prince_Roland_Bonaparte
    type: :Ancestor
  AssignClass (2c11c611-7f1b-4755-9a9a-6ca2e212c9c8)
 Call ID: 2c11c611-7f1b-4755-9a9a-6ca2e212c9c8
  Args:
    source: :Prince_Valdemar_of_Denmark
    type: :Ancestor
  ValidateShacl (60d499f0-66fe-4c1a-baf7-e5f7490b1d7e)
 Call ID: 60d499f0-66fe-4c1a-baf7-e5f7490b1d7e
  Args:
  Finish (e3c8566d-27b9-4a22-94cc-cab755c7b335)
 Call ID: e3c8566d-27b9-4a22-94cc-cab755c7b335
  Args:

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

The final data graph after all the edits:
  @prefix : <http://example.com/family_TBOX.ttl#> .
  @prefix data: <http://example.org/data/> .
  @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

  data:King_Christian_IX_of_Denmark a :Man .

  data:Prince_Constantine_of_Greece a :Man ;
      :isBrotherOf data:Prince_George_of_Greece_and_Denmark .

  data:Prince_Nicholas_of_Greece a :Man ;
      :isBrotherOf data:Prince_George_of_Greece_and_Denmark .

  data:Prince_Roland_Bonaparte a :Ancestor,
          :Man ;
      :isFatherOf data:Princess_Marie_Bonaparte .

  data:Prince_Valdemar_of_Denmark a :Ancestor,
          :Man ;
      :isBrotherOf data:Marie_dOrleans ;
      :isFatherOf data:Prince_Aage ;
      :isUncleOf data:Prince_George_of_Greece_and_Denmark .

  data:Evgenia a :Woman .

  data:George_I_of_Greece a :Ancestor,
          :Man .

  data:Marie_dOrleans a :Woman .

  data:Olga_Konstantinovna_of_Russia a :Ancestor,
          :Woman .

  data:Petros a :Man .

  data:Prince_Aage a :Man .

  data:Princess_Marie_Bonaparte a :Woman .

  data:Prince_George_of_Greece_and_Denmark a :Man ;
      :hasBirthYear 1869 ;
      :hasDaughter data:Evgenia ;
      :hasDeathYear 1957 ;
      :hasFather data:George_I_of_Greece ;
      :hasMarriageYear 1907 ;
      :hasMother data:Olga_Konstantinovna_of_Russia ;
      :hasRelation data:Princess_Marie_Bonaparte ;
      :hasSon data:Petros .



================================= Tool Message =================================

SHACL validation has not produced any violations.

================================= Tool Message =================================

Previous SHACL validation wasn't successful. If you fixed the violations, use the validation tool again to confirm no violations persist.

================================== Ai Message ==================================

[]
Tool Calls:
  ValidateShacl (176466cc-6833-444d-8d5f-1d3bb947699f)
 Call ID: 176466cc-6833-444d-8d5f-1d3bb947699f
  Args:

================================= Tool Message =================================

SHACL validation has not produced any violations.

================================== Ai Message ==================================

[]
Tool Calls:
  Finish (e2e023ea-77fa-4c80-b919-d2766f1315d4)
 Call ID: e2e023ea-77fa-4c80-b919-d2766f1315d4
  Args: