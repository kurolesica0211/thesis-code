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
Princess Viktoria of Prussia (Friederike Amalia Wilhelmine Viktoria; 12 April 1866 – 13 November 1929) was the second daughter of Frederick III, German Emperor and his wife Victoria, Princess Royal, eldest daughter of Queen Victoria.
Born a member of the Prussian royal house of Hohenzollern, she became Princess Adolf of Schaumburg-Lippe following her first marriage in 1890.
Raised by her mother in a close, liberal, and anglophile environment, Viktoria fell in love with Alexander of Battenberg, the Prince of Bulgaria, but there was great opposition to the match and the couple never married.
Following the end of her courtship with Alexander, Viktoria suffered from an eating disorder and was unlucky in her search for a suitable husband.
Adolf died during the First World War, two years before the German Empire came to an end.
In 1927, Viktoria caused a royal scandal by marrying a university student 35 years her junior.
Early life

Birth and baptism

Viktoria was born on 12 April 1866 in the New Palace in Potsdam, to Crown Prince Frederick William and Crown Princess Victoria of Prussia.
Her father was the only son of King Wilhelm I of Prussia and Princess Augusta of Saxe-Weimar; her mother, Victoria ("Vicky"), was the eldest child of Queen Victoria of the United Kingdom and her consort, Prince Albert.
Viktoria was baptised in the New Palace as Friederike Amalia Wilhelmine Viktoria on 24 May 1866, the birthday of her grandmother Queen Victoria, who was also one of her godparents.
Other sponsors included her grandfather the King of Prussia, and Princess Marie of Hohenzollern-Sigmaringen.
Following the birth of Princess Viktoria, Queen Victoria wrote a letter to her daughter Crown Princess Victoria, mentioning that she was happy with her granddaughter being named after her:


"I am much pleased & touched that the dear, new baby (& long may she remain the Baby!) is to be called after me", Victoria wrote Vicky, "as I cannot deny that it pained me very much that 4 children were born without one being called after either of your parents.
Youth and education

Viktoria was her parents' fifth child and second daughter.
Two months after her birth, on 18 June 1866, Viktoria's nearly two-year-old brother, Sigismund, died of meningitis.
On 19 June Vicky wrote to her mother Queen Victoria:


"...I wish you to know all, you are so kind, darling Mama, that you will wish to hear all about the last terrible days, I cannot describe them.
I am calm now, for Fritz's sake and my little ones', but oh how bitter is this cup..."

 Following this event, Viktoria's mother chose to raise her younger children herself, as opposed to leaving them in the care of tutors and governesses as she had with her older children, Wilhelm, Charlotte, and Henry.
For this reason, Viktoria and her three younger siblings, Waldemar, Sophie, and Margaret, were far closer to their parents.
Viktoria and her siblings lived at two main residences, the New Palace in Potsdam and the Kronprinzenpalais in Berlin.
In 1871, Viktoria's grandfather Wilhelm I became German Emperor, and her parents became Crown Prince and Princess of a unified German Empire.
Still, the Crown Princely couple raised their children away from the Berlin court, which disliked Frederick William and Victoria and their liberal beliefs.
Much of Viktoria's childhood care and education was based on that of Vicky's British upbringing, and Viktoria and her younger siblings had British nannies and went on many trips to visit their family in Britain.
Raised in a close environment, less strict than that of her elder siblings' childhood, Viktoria was an active and enthusiastic child.
She attended weekly dance lessons and enjoyed riding her Shetland pony, a gift from Queen Victoria.
Young adult years

Alexander of Battenberg

In 1881, Alexander, Prince of Bulgaria, born Prince Alexander of Battenberg, who had been the sovereign of the Principality of Bulgaria since 1879, visited the Prussian court at the behest of Viktoria's mother.
As her mother and Queen Victoria recommended Alexander as a possible match, 16-year-old Viktoria quickly caught their enthusiasm and by the time of Sandro's next visit the following spring, she had fallen in love with the attractive prince.
Though her parents wanted the couple to marry, much of Viktoria's Prussian family was opposed.
Her elder siblings, paternal grandparents Emperor Wilhelm I and Empress Augusta, and German chancellor Otto von Bismarck were opposed to the match.
Alexander of Battenberg's actions in Bulgaria irritated the Russian tsar, and it was feared that if Viktoria married Alexander, Tsar Alexander III would be offended, even though Alexander of Battenberg and Tsar Alexander III were first cousins.
Furthermore, Alexander was born of a morganatic marriage, and his position as Prince of Bulgaria was unstable; he had more to gain than Viktoria through marriage to a daughter of the future German emperor.
By 1888, pushback from Wilhelm I and Bismarck all but forced Viktoria and her parents to give up on the marriage.
Depression and changing life


As Viktoria was losing hope of marrying Sandro, her grandfather Emperor Wilhelm I and her father Crown Prince Frederick William were both ailing, and her sister Sophie was preparing to move to Athens in order to marry the Crown Prince of Greece.
The Emperor died on 9 March 1888, and Frederick William and Victoria became the new emperor and empress.
Frederick, however, was dying of throat cancer, and reigned for only 99 days before succumbing to his illness on 15 June.
Viktoria's eldest brother, now Emperor Wilhelm II, despised his parents and, though Frederick had requested in his will that Wilhelm allow Viktoria to marry Sandro, the new emperor instead wrote to Sandro to definitively end the couple's courtship.
Sandro returned to Viktoria all the letters and gifts she had sent to him, and wrote her a farewell note.
Viktoria, now 22, worried she might end up a spinster.
Not considered an attractive girl – especially by herself – Viktoria tried to improve her appearance by dieting "maniacally" to the point of starving herself.
Wrote her mother to Queen Victoria in 1889: 

You would indeed make me most happy and do me the greatest favour, if you could induce Moretta not to be so foolish about her food!
Viktoria likely had some form of disordered eating.
Subtly pushed out of the Berlin social sphere by Wilhelm, she lived with her mother and younger sister Margaret at Schloss Friedrichshof in Hesse.
Vicky sent the depressed Viktoria to Britain, to recover and spend time with her British relatives.
Further suitors

Following the collapse of Viktoria's plans to marry Sandro, her mother (now known as "Empress Frederick") and grandmother, Queen Victoria, continued to look for possible suitors, and enlisted the help of the Duchess of Edinburgh and Princess of Leiningen.
Though she was not thought of as exceedingly attractive, Viktoria was described as having "immense charm".
Prince Carl of Sweden, Duke of Västergötland, "refused to consider marrying her"; this news worsened Viktoria's disordered eating.
Another suitor was Ernest, the future Prince of Hohenlohe-Langenburg; he later married Viktoria's first cousin Alexandra of Saxe-Coburg and Gotha.
Crown Prince Carlos of Portugal was proposed by Otto von Bismarck, but Viktoria refused to convert to Catholicism.
Maurice Bourke, a younger son of Richard Bourke, 6th Earl of Mayo, was proposed by Queen Victoria; he was seriously considered.
As her elder sister, Charlotte, began gossiping about her love life at court, Viktoria became convinced she would never marry, and told her grandmother she was no longer interested in marriage.
First marriage and adult life

Engagement and wedding

In June 1890, Viktoria, with her mother and sister Margaret, visited their cousin Marie of Nassau, the widowed Princess of Wied.
Adolf and Viktoria spent time together and, during the same visit, Adolf proposed on 11 June.
Viktoria's mother had previously considered Adolf as a marriage candidate, but had considered him unworthy of her daughter; she wept at the news of the couple's engagement.
Although Viktoria said in her memoirs that she had loved Adolf at first sight, she wrote to her mother that she had only married him out of "desperation from fear at withering on the vine."
When Queen Victoria inspected Adolf, she approved of him, but did not believe that Viktoria was entirely happy, nor did Vicky.
Furthermore, Adolf held only the style of Serene Highness, while Viktoria was a Royal Highness and the daughter of an Emperor.
The widowed Empress continued to suggest other suitors, but was thwarted, especially by Wilhelm II, who was highly in favour of the match.
In the months leading up to the wedding, Viktoria remained depressed.
The wedding party and the couple's families attended the opera, and the next day Viktoria's mother held a banquet for the guests.
Viktoria and Adolf married on 19 November 1890 in a Lutheran ceremony, in the chapel of Berlin's Alte Schloss.
Much of Viktoria's extended family made up the nearly sixty royal guests, as well as the large wedding party.
Viktoria's brother Wilhelm gave the toast.
Viktoria wore a wedding gown of "cream satin, brocaded and trimmed with wild roses and silver", and a veil "of tulle interwoven with silver and surmounted with a wreath of orange blossoms and myrtles".
Viktoria and Adolf had a long honeymoon, during which they travelled throughout Europe and the Mediterranean, stopping in Greece to visit Viktoria's sister Sophie.
They were forced to cut this final visit short in order to return to Germany for medical care, as Viktoria had suffered an early miscarriage.
Viktoria and Adolf had a peaceful marriage, and mutually respected one another.
However, Viktoria did not love her husband, and in the later years of her marriage considered divorcing Adolf to marry one of his nephews.
Princess Adolf of Schaumburg-Lippe

Adolf purchased from a cloth manufacturer a neoclassical palace that would become the Palais Schaumburg, in Bonn.
Viktoria was often alone there, as Adolf was busy with his military duties.
Viktoria lived a quiet life in Bonn, and continued to frequently visit members of her large family.
Adolf installed tennis courts at their home upon Viktoria's request, and encouraged her love of gardening.
Soon, however, Viktoria admitted she was bored and unhappy.
Viktoria and Adolf entered Lippe's capital, Detmold, on 4 May 1895 and remained there until Adolf's term as regent ended.
During this time, Viktoria enjoyed her new public responsibilities as wife of the principality's regent, and her mental health improved.
Queen Victoria was upset when, in September 1895, Adolf requested that Viktoria end her visit to her widowed and lonely mother.
In 1898, Viktoria's mother Vicky was diagnosed with breast cancer, which spread to her spine and weakened her.
Viktoria was thrown from her carriage in 1901 while out driving in Bonn, but she was not seriously injured.
That year, between the deaths of Queen Victoria and Vicky, she celebrated her 35th birthday with family at Friedrichshof.
For Viktoria, who adored her mother's British homeland, the war was doubly stressful.
Despite being the sister of the Kaiser of Germany, Viktoria was very sympathetic to the British cause.
In 1915, the 49-year-old "but very wealthy and young looking" Viktoria left Berlin and moved into a "luxuriously furnished" castle in Bonn.
The war years threw Viktoria's life into chaos:
Adolf died in July 1916, after nearly thirty years of marriage; in 1917, Viktoria's brother-in-law the King of the Hellenes, who married her sister Queen Sophia of Greece in 1890, was deposed; and in 1918, her brother Wilhelm II was forced to abdicate and the German nobles and royals legally lost their titles under the new Weimar Republic.
After Adolf's death, Viktoria asked her brother for permission to marry one of Adolf's nephews; Wilhelm refused.
Following the war, though she did not lose her home, Viktoria's finances began to dwindle.
Second marriage

In 1927, Viktoria held a party for university students at her castle in Bonn.
Zoubkoff told Viktoria that he had fled the Russian Revolution and that he had been a baron.
Infatuated with Zoubkoff, Viktoria provided the young student – 35 years her junior – with lavish gifts; he, in turn, proposed marriage.
Without asking permission from the former Emperor Wilhelm, Viktoria renounced her titles and married Zoubkoff first at the town hall in Bonn, then in a Greek Orthodox ceremony at which none of her family was in attendance.
The couple were married on 19 November 1927, which would have been Viktoria and Adolf's 37th wedding anniversary.
Viktoria was 61, while Alexander was only 27.
The two had known one another for only two months, and their wedding was a royal and society scandal.
Soon after the wedding, Alexander Zoubkoff, whom Viktoria called "Sascha", began spending large amounts of Viktoria's dwindling fortune.
The restaurant advertised with a sign that read: "The Emperor's brother-in-law is serving you here".
Although she had at first stood by her husband, in 1928, Viktoria separated from him, considering his antics too much.
Her own financial struggles caught up to her, and Viktoria was forced to auction off nearly all of her belongings.
Viktoria was forced to move into a single rented room in the suburbs of Bonn.
That same year Viktoria caused another scandal by filing for divorce from Zoubkoff after less than two years of marriage, on the grounds that his behaviour had resulted in his expulsion from Germany, he was unable to maintain her, and that "conjugal relations did not exist".
Before they could be divorced, or her siblings could have their marriage annulled, Viktoria came down with a fever and was taken to the Hospital of St Francis, in Bonn, where she was diagnosed with pneumonia.
In the hours before her death, her brother Wilhelm and sister Margaret attempted to contact her, but were not allowed.
Viktoria died on 13 November 1929, "penniless, lonely, loveless, and without her family's forgiveness".
She was buried at Schloss Friedrichshof, the home of her sister Margaret.
Archives

Viktoria's letters to her sister Margaret are preserved in the Archive of the House of Hesse, which is kept in Fasanerie Palace in Eichenzell, Germany.



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
  AssignClass (f21af2ad-020e-42e9-911c-c713cc9d0266)
 Call ID: f21af2ad-020e-42e9-911c-c713cc9d0266
  Args:
    type: :Woman
    source: :Viktoria_of_Prussia
  AssignClass (51c5e609-ca60-407a-b726-7c27be8641dc)
 Call ID: 51c5e609-ca60-407a-b726-7c27be8641dc
  Args:
    type: :Person
    source: :Viktoria_of_Prussia
  AddLiteral (3d446ed4-0509-4923-ac0b-51ea9f89fc18)
 Call ID: 3d446ed4-0509-4923-ac0b-51ea9f89fc18
  Args:
    literal_value: 1866
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: :Viktoria_of_Prussia
  AddLiteral (2b7345df-f0c7-48a9-a51a-6d71cf07c405)
 Call ID: 2b7345df-f0c7-48a9-a51a-6d71cf07c405
  Args:
    literal_value: 1929
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: :Viktoria_of_Prussia
  AssignClass (304ded0d-3ed2-43ef-8268-71a6e92b0b13)
 Call ID: 304ded0d-3ed2-43ef-8268-71a6e92b0b13
  Args:
    type: :Man
    source: :Frederick_III_German_Emperor
  AssignClass (8c501d2b-2e6d-4b48-9fa5-b736d6fcce41)
 Call ID: 8c501d2b-2e6d-4b48-9fa5-b736d6fcce41
  Args:
    type: :Ancestor
    source: :Frederick_III_German_Emperor
  AssignClass (ec917e73-87e5-4403-a820-88a31be8d5b9)
 Call ID: ec917e73-87e5-4403-a820-88a31be8d5b9
  Args:
    source: :Victoria_Princess_Royal
    type: :Woman
  AssignClass (6f2bea2f-e8d9-4f62-bf33-8c3c9a1fe2ee)
 Call ID: 6f2bea2f-e8d9-4f62-bf33-8c3c9a1fe2ee
  Args:
    type: :Ancestor
    source: :Victoria_Princess_Royal
  AddTriple (f9fb3e9b-1267-48d9-975d-949581c2bb18)
 Call ID: f9fb3e9b-1267-48d9-975d-949581c2bb18
  Args:
    target: :Frederick_III_German_Emperor
    source: :Viktoria_of_Prussia
    relation: :isDaughterOf
  AddTriple (3219e678-cd42-47b1-bc42-3558ded11e64)
 Call ID: 3219e678-cd42-47b1-bc42-3558ded11e64
  Args:
    relation: :isDaughterOf
    source: :Viktoria_of_Prussia
    target: :Victoria_Princess_Royal
  AssignClass (340964fe-e564-41bb-9e32-a0173fa50191)
 Call ID: 340964fe-e564-41bb-9e32-a0173fa50191
  Args:
    source: :Queen_Victoria
    type: :Woman
  AssignClass (b8b0099d-2143-427e-ade1-af47e83807df)
 Call ID: b8b0099d-2143-427e-ade1-af47e83807df
  Args:
    type: :Ancestor
    source: :Queen_Victoria
  AddTriple (dd4dda87-ca37-40e4-a29d-f95cb31eb7bc)
 Call ID: dd4dda87-ca37-40e4-a29d-f95cb31eb7bc
  Args:
    target: :Queen_Victoria
    source: :Victoria_Princess_Royal
    relation: :isDaughterOf
  AssignClass (d847ca8f-cb11-416d-8334-0f0f65f91a8c)
 Call ID: d847ca8f-cb11-416d-8334-0f0f65f91a8c
  Args:
    source: :Prince_Adolf_of_Schaumburg-Lippe
    type: :Man
  AssignClass (b20a73c4-f1ca-4363-8b56-16158341d733)
 Call ID: b20a73c4-f1ca-4363-8b56-16158341d733
  Args:
    source: :Prince_Adolf_of_Schaumburg-Lippe
    type: :Person
  AddLiteral (d5a71f27-9c89-44ed-9a35-188762bc40bf)
 Call ID: d5a71f27-9c89-44ed-9a35-188762bc40bf
  Args:
    literal_value: 1890
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: :Viktoria_of_Prussia
  AddTriple (b9e7ce04-ece1-4111-9005-121c898659d9)
 Call ID: b9e7ce04-ece1-4111-9005-121c898659d9
  Args:
    target: :Prince_Adolf_of_Schaumburg-Lippe
    source: :Viktoria_of_Prussia
    relation: :hasRelation
  AssignClass (2dd289fa-d473-45f8-ad54-e11b29fa83c4)
 Call ID: 2dd289fa-d473-45f8-ad54-e11b29fa83c4
  Args:
    source: :Alexander_Zoubkoff
    type: :Man
  AssignClass (ae85a628-2037-4d0d-b046-4f5b2591a3fb)
 Call ID: ae85a628-2037-4d0d-b046-4f5b2591a3fb
  Args:
    source: :Alexander_Zoubkoff
    type: :Person
  AddLiteral (6626323d-ebca-4199-93cf-4fcbb385ca8b)
 Call ID: 6626323d-ebca-4199-93cf-4fcbb385ca8b
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 1927
    source: :Viktoria_of_Prussia
  AddTriple (c8b9ab9c-b956-4774-aff2-16d4c438e833)
 Call ID: c8b9ab9c-b956-4774-aff2-16d4c438e833
  Args:
    relation: :hasRelation
    source: :Viktoria_of_Prussia
    target: :Alexander_Zoubkoff
  AssignClass (b1af3883-9570-4b7a-9d6e-6166a5495ec4)
 Call ID: b1af3883-9570-4b7a-9d6e-6166a5495ec4
  Args:
    type: :Man
    source: :Sigismund_of_Prussia
  AssignClass (348cf0fa-9856-4309-b14b-15507041f279)
 Call ID: 348cf0fa-9856-4309-b14b-15507041f279
  Args:
    source: :Sigismund_of_Prussia
    type: :Person
  AddTriple (841b7991-bc8f-4c16-97a8-010a2c4bf9f4)
 Call ID: 841b7991-bc8f-4c16-97a8-010a2c4bf9f4
  Args:
    relation: :isBrotherOf
    source: :Sigismund_of_Prussia
    target: :Viktoria_of_Prussia
  AssignClass (1b43169b-a104-44ac-af35-19c8327ec5d8)
 Call ID: 1b43169b-a104-44ac-af35-19c8327ec5d8
  Args:
    source: :Waldemar_of_Prussia
    type: :Man
  AssignClass (c2bc1df0-4ba0-4997-bbd6-ca2e807d301e)
 Call ID: c2bc1df0-4ba0-4997-bbd6-ca2e807d301e
  Args:
    type: :Person
    source: :Waldemar_of_Prussia
  AddTriple (fb18cb21-7b9b-4b6e-b39a-d7f38ea05f08)
 Call ID: fb18cb21-7b9b-4b6e-b39a-d7f38ea05f08
  Args:
    relation: :isBrotherOf
    target: :Viktoria_of_Prussia
    source: :Waldemar_of_Prussia
  AssignClass (f2477c00-df30-4199-b651-233ced5eb846)
 Call ID: f2477c00-df30-4199-b651-233ced5eb846
  Args:
    source: :Sophie_of_Prussia
    type: :Woman
  AssignClass (dbde1160-1981-427e-89a8-5e9e057e0e5f)
 Call ID: dbde1160-1981-427e-89a8-5e9e057e0e5f
  Args:
    source: :Sophie_of_Prussia
    type: :Person
  AddTriple (68acf532-59a8-46ba-815f-b5eb38db123a)
 Call ID: 68acf532-59a8-46ba-815f-b5eb38db123a
  Args:
    relation: :isSisterOf
    target: :Viktoria_of_Prussia
    source: :Sophie_of_Prussia
  AssignClass (6ada6dfc-a29f-4d10-8baf-f89d49df7acf)
 Call ID: 6ada6dfc-a29f-4d10-8baf-f89d49df7acf
  Args:
    type: :Woman
    source: :Margaret_of_Prussia
  AssignClass (4c3694c1-d5ec-4ff8-87ae-8b9de979e94c)
 Call ID: 4c3694c1-d5ec-4ff8-87ae-8b9de979e94c
  Args:
    source: :Margaret_of_Prussia
    type: :Person
  AddTriple (d9bfb703-ee62-4412-ab82-bc611ec238b5)
 Call ID: d9bfb703-ee62-4412-ab82-bc611ec238b5
  Args:
    source: :Margaret_of_Prussia
    target: :Viktoria_of_Prussia
    relation: :isSisterOf
  AssignClass (86994c1f-7df3-4a98-ae34-c0f0c3bdf33f)
 Call ID: 86994c1f-7df3-4a98-ae34-c0f0c3bdf33f
  Args:
    type: :Man
    source: :Wilhelm_II_German_Emperor
  AssignClass (3ea592d4-8102-474b-91ad-6f4d550b8909)
 Call ID: 3ea592d4-8102-474b-91ad-6f4d550b8909
  Args:
    source: :Wilhelm_II_German_Emperor
    type: :Person
  AddTriple (abb36071-5c67-4b47-aaeb-9a1da5bd6ce2)
 Call ID: abb36071-5c67-4b47-aaeb-9a1da5bd6ce2
  Args:
    source: :Wilhelm_II_German_Emperor
    target: :Viktoria_of_Prussia
    relation: :isBrotherOf
  AssignClass (06f9a899-aaf4-4362-8db4-faa9f85172e8)
 Call ID: 06f9a899-aaf4-4362-8db4-faa9f85172e8
  Args:
    source: :Charlotte_of_Prussia
    type: :Woman
  AssignClass (d17f6865-e111-4ae0-ad9c-0ed4880d630f)
 Call ID: d17f6865-e111-4ae0-ad9c-0ed4880d630f
  Args:
    source: :Charlotte_of_Prussia
    type: :Person
  AddTriple (be0bf642-55b0-4fda-b437-83d5dfe5c14a)
 Call ID: be0bf642-55b0-4fda-b437-83d5dfe5c14a
  Args:
    source: :Charlotte_of_Prussia
    target: :Viktoria_of_Prussia
    relation: :isSisterOf
  AssignClass (89df96dc-ed9a-47c0-a2d3-cc799823a781)
 Call ID: 89df96dc-ed9a-47c0-a2d3-cc799823a781
  Args:
    source: :Henry_of_Prussia
    type: :Man
  AssignClass (34b11eed-c327-40b8-9192-6ce155ec7292)
 Call ID: 34b11eed-c327-40b8-9192-6ce155ec7292
  Args:
    type: :Person
    source: :Henry_of_Prussia
  AddTriple (d437c242-9b12-4c0a-93b8-dccc8ccb76f3)
 Call ID: d437c242-9b12-4c0a-93b8-dccc8ccb76f3
  Args:
    relation: :isBrotherOf
    source: :Henry_of_Prussia
    target: :Viktoria_of_Prussia
  Finish (1f5baa7f-808d-48b7-b7ca-34dc749f2856)
 Call ID: 1f5baa7f-808d-48b7-b7ca-34dc749f2856
  Args: