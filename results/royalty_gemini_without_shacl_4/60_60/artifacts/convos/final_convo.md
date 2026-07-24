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
Juliana (.mw-parser-output .IPA-label-small{font-size:85%}.mw-parser-output .references .IPA-label-small,.mw-parser-output .infobox .IPA-label-small,.mw-parser-output .navbox .IPA-label-small{font-size:100%}Dutch pronunciation:  i; Juliana Louise Emma Marie Wilhelmina; 30 April 1909 – 20 March 2004) was Queen of the Netherlands from 1948 until her abdication in 1980.
Juliana was the only child of Queen Wilhelmina and Duke Henry of Mecklenburg-Schwerin.
In 1937, she married Prince Bernhard of Lippe-Biesterfeld with whom she had four daughters: Beatrix, Irene, Margriet, and Christina.
During the German invasion of the Netherlands in the Second World War, the royal family was evacuated to the United Kingdom.
Juliana then relocated to Canada with her children, while Wilhelmina and Bernhard remained in Britain.
The royal family returned to the Netherlands after its liberation in 1945.
Due to Wilhelmina's failing health, Juliana took over royal duties briefly in 1947 and 1948.
In September 1948, Wilhelmina abdicated and Juliana ascended to the Dutch throne.
Her reign saw the decolonization and independence of the Dutch East Indies and Suriname, and the creation and dissolution of the Netherlands-Indonesia Union, of which she served as head of state.
Despite a series of controversies involving the royal family, Juliana remained a popular figure among the Dutch.
In April 1980, Juliana abdicated in favour of her eldest daughter, Beatrix.
Early life and education

Juliana was born on 30 April 1909 at Noordeinde Palace in The Hague, the only child of the reigning Dutch monarch, Queen Wilhelmina.
Her father was Duke Henry of Mecklenburg-Schwerin.
She was the first Dutch royal baby since Wilhelmina herself was born in 1880.
Wilhelmina had suffered two miscarriages and had given birth to a premature and stillborn son, raising the prospect of a succession crisis.
The Queen's nearest relative was Prince Heinrich XXXII Reuss of Köstritz, whose close ties to Germany made him unpopular in the Netherlands, leading to concerns that if Wilhelmina died without an heir, he would turn the Netherlands into a puppet state of Germany.
Juliana's birth thus assured the royal family's survival.
Her mother suffered two further miscarriages after her birth, leaving Juliana as the royal couple's only child.
According to several sources Juliana was happy to be an only child because that meant she did not have to fight for attention.
Juliana spent her childhood at Het Loo Palace in Apeldoorn, and at Noordeinde Palace and Huis ten Bosch Palace in The Hague.
As the Dutch constitution specified that Princess Juliana should be ready to succeed to the throne by the age of eighteen, her education proceeded at a faster pace than that of most children.
On 30 April 1927, Princess Juliana celebrated her eighteenth birthday.
In the course of her studies, she also attended lectures on the cultures of Suriname and the Netherlands Antilles, international affairs, international law, history, and European law.
Marriage

In the 1930s, Queen Wilhelmina began a search for a suitable husband for her daughter.
At the time, the House of Orange-Nassau was one of the most strictly religious royal families in the world, and it was very difficult to find a Protestant prince who suited their standards.
At the 1936 Winter Olympics in Bavaria, she met Prince Bernhard of Lippe-Biesterfeld, a young German Prince who was her 7th cousin, as both descended from Lebrecht, Prince of Anhalt-Zeitz-Hoym.
His rank and religion were suitable; so Princess Juliana's royal engagement was arranged by her mother.
Princess Juliana fell deeply in love with her fiancé, a love that was to last a lifetime and that withstood separation during the war and Bernhard's extramarital affairs and illegitimate children.
Queen Wilhelmina, by then the richest woman in the world, left nothing to chance.
Wilhelmina had her lawyers draw up a prenuptial agreement that specified exactly what the German-born prince could and could not do, and what money he would receive from the royal estate.
Prior to the wedding, on 24 November 1936, Prince Bernhard was granted Dutch citizenship and changed the spelling of his names from German to Dutch.
They married in The Hague on 7 January 1937, the date on which Princess Juliana's grandparents, King William III and Queen Emma, had married fifty-eight years earlier.
Juliana's chosen bridesmaids were either relatives or family friends.
These included Duchess Woizlawa Feodora of Mecklenburg-Schwerin (her first cousin), Duchess Thyra of Mecklenburg-Schwerin (her second cousin), Grand Duchess Kira Kirillovna of Russia (her first cousin once removed), Princess Sophie of Saxe-Weimar-Eisenach (her second cousin), and two of Bernhard's first cousins, Princess Sieglinde of Lippe and Princess Elisabeth of Lippe.
Canadian exile

On 12 May 1940, during the invasion of the Netherlands by Germany in the Second World War, Prince Bernhard and Princess Juliana were evacuated to the United Kingdom to be followed the next day by Queen Wilhelmina and the Dutch Government, who set up a government in exile.
When her third child, Princess Margriet, was born on 19 January 1943, Governor General Lord Athlone granted royal assent to a special law declaring Princess Juliana's rooms at the Ottawa Civic Hospital to be extraterritorial in order that the infant would have exclusively Dutch, not dual nationality.
Prince Bernhard, who had remained in London to assist his mother in law Queen Wilhelmina and the government with operating in exile, was able to visit his family in Canada and be there for Margriet's birth.
Princess Juliana's genuine warmth and the gestures of her Canadian hosts created a lasting bond, which was reinforced when Canadian soldiers fought and died by the thousands in 1944 and 1945 to liberate the Netherlands from the Nazis.
She returned with Queen Wilhelmina by a military transport plane to the liberated part of the Netherlands on 2 May 1945, rushing to Breda to set up a temporary Dutch government.
Juliana erected a wooden lectern and brass plaque which is dedicated in thanks to the St. Andrew's Presbyterian Church (Ottawa) for their hospitality during her residence in Ottawa.
The following year (1946), Juliana donated another 20,500 bulbs, with the request that a portion of these be planted at the grounds of the Ottawa Civic Hospital where she had given birth to Margriet.
On 2 May 1945, Princess Juliana was returned with her mother to Dutch soil.
Juliana took part in the post-war relief operation for the people in the northern part of the country who had suffered through starvation during the Hunger Winter of 1944–1945, which had taken the lives of many of her countrymen.
Her down-to-earth manner endeared her to her people so much that a majority of the Dutch people would soon want Queen Wilhelmina to abdicate in favour of her daughter.
In the spring of 1946 Princess Juliana and Prince Bernhard visited the countries that had helped the Netherlands during the occupation.
During her pregnancy with her last child, Marijke Christina, Princess Juliana contracted rubella.
Reign

Regency and early reign

Wilhelmina's increasingly precarious health made it increasingly difficult for her to perform her duties.
Juliana was forced to take over as regent from 14 October to 1 December 1947.
Wilhelmina seriously considered abdicating in favour of Juliana at the end of 1947, but Juliana urged her mother to stay on the throne so she could celebrate her golden jubilee in 1948.
However, Wilhelmina was forced by further health problems to relinquish her royal duties to Juliana once again on 4 May 1948.
The independence of Indonesia, which saw more than 150,000 Dutch troops stationed there as decolonization force, was regarded as an economic disaster for the Netherlands.
Two days later, with the eyes of the world upon her, Juliana was sworn in and inaugurated as monarch during a joint session of the States General at a ceremony held in the Nieuwe Kerk in Amsterdam, becoming the 12th member of the House of Orange to rule the Netherlands.
On 27 December 1949 at Dam Palace in Amsterdam, Queen Juliana signed the papers that recognised Indonesian sovereignty over the former Dutch colony.
She became Hoofd der Unie (Head of the Union) of the Netherlands-Indonesian Union (1949–1956).
On 15 December 1954, the Queen announced that the nation's Caribbean possessions of the Netherlands Antilles and Suriname were to be reconstituted as constituent countries of the Kingdom of the Netherlands, making them equal partners with the mainland.
However, the debate subsided in part due to Juliana's efforts to connect with her people.
On the international stage, Queen Juliana was interested in the problems of developing countries, the refugee problem, and particularly child welfare in developing countries.
Francis of Bavaria, a participant, reports in his memoirs the anecdote that the queens of Greece, the Netherlands and Italy went ashore in a harbor in the middle of a crowd of nephews and nieces, and a waiting journalist called out to them: "What is the purpose of this trip?", whereupon Queen Juliana replied with a friendly smile: "Oh, you know, this is our union's company outing.
"


Crises and recovery

On the night of 31 January 1953, the Netherlands was hit by the most destructive storm in more than five hundred years.
Dressed in boots and an old coat, Queen Juliana waded through water and slopped through deep mud all over the devastated areas to bring desperate people food and clothing.
Showing compassion and concern, reassuring the people, her tireless efforts would permanently endear her to the citizens of the Netherlands.
In 1956, the influence of Hofmans on Juliana's political views almost brought down the monarchy in a constitutional crisis; this caused the court and the royal family to split into a "Bernhard faction", set on removing a queen considered a religious fanatic and a threat to NATO, and the queen's pious and pacifist courtiers.
The crisis was resolved, when Hofmans was banished from the court and Juliana's supporters were sacked or pensioned.
Prince Bernhard planned to divorce his wife but decided against it when he, as he told an American journalist, "found out that the woman still loved him" .
Queen Juliana faced another crisis among her Protestant citizens in 1963, when her second daughter Irene secretly converted to Roman Catholicism and, without government approval, on 29 April 1964 married Prince Carlos Hugo of Bourbon, Duke of Parma, a claimant to the Spanish throne and also a leader in Spain's Carlist party.
Another crisis developed as a result of the announcement in July 1965 of the engagement of Princess Beatrix, heir to the throne, to German diplomat Claus von Amsberg.
After attempting to have the marriage cancelled, Queen Juliana acquiesced and the marriage took place under a continued storm of protest; an almost certain attitude pervaded the country that Princess Beatrix might be the last member of the House of Orange to ever reign in the Netherlands.
Despite all these difficulties, Queen Juliana's personal popularity suffered only temporarily.
In May 1959, for example, Polish-American ufologist George Adamski received a letter from the head of the Dutch Unidentified Flying Objects Society, Rey d'Aquilla, informing him that she had been contacted by Queen Juliana's palace and "that the Queen would like to receive you".
Once again, Queen Juliana's weakness for the preternatural had landed her back in the headlines: she had invited to the palace a crackpot from California who numbered among his friends men from Mars, Venus and other solar-system suburbs.
Representing the Queen at the independence ceremony in the Surinamese capital, Paramaribo, were the heir presumptive Princess Beatrix, and her husband Prince Claus.
Scandal rocked the royal family again in 1976, when it was revealed that Prince Bernhard had accepted a US$1.1 million bribe from U.S. aircraft manufacturer Lockheed Corporation to influence the Dutch government's purchase of fighter aircraft in what became known as the Lockheed Scandal.
Prime Minister Joop den Uyl ordered an inquiry into the affair, while Prince Bernhard refused to answer reporters' questions, stating: "I am above such things."
Rather than calling on the Queen to abdicate, the Dutch people were this time fearful that their beloved Juliana might abdicate out of shame or because of a criminal prosecution conducted in her name against her consort.
On 26 August 1976, a censored and toned-down yet devastating report on Prince Bernhard's activities was released to a shocked Dutch public.
The prince resigned his various high-profile positions as a lieutenant admiral, a general, and an Inspector General of the Armed Forces.
The prince also accepted that he would have to give up wearing his beloved uniforms.
On her Silver Jubilee in 1973, Queen Juliana donated all of the money that had been raised by the National Silver Jubilee Committee to organizations for children in need throughout the world.
On 30 April 1980, her 71st birthday, Queen Juliana abdicated and her eldest daughter succeeded her.
Juliana remained active in numerous charitable causes until well into her eighties.
Queen Juliana was very attached to Monte Argentario, in Tuscany, a favorite place for the Dutch royal family for their summer holidays for more than 40 years.
Illness and death

From the mid-1990s, Juliana's health declined as she suffered the progressive onset of dementia.
Juliana did not appear in public after this time.
At the order of the Royal Family's doctors, Juliana was placed under 24-hour care.
Prince Bernhard said in a television interview in 2001 that the former Queen was no longer able to recognise her family and that she had been suffering from Alzheimer's disease for several years.
Juliana died in her sleep on 20 March 2004 at the age of 94, at Soestdijk Palace in Baarn, from complications of pneumonia, seventy years to the day after her grandmother, Queen Emma.
She was embalmed, unlike her mother Wilhelmina, who chose not to be, and on 30 March 2004 interred beside her mother in the royal vaults under the Nieuwe Kerk in Delft.
Juliana's husband Prince Bernhard died about nine months later aged 93, on 1 December 2004; his remains were placed next to hers.
In 2009, an exhibition of portraits of Juliana, and objects from her life, was held at the Het Loo Palace to mark the centenary of her birth.
Titles, styles, and arms

Juliana's full title and style as an unmarried woman was: Her Royal Highness Princess Juliana Louisa
Emma Marie Wilhelmina of the Netherlands, Princess of Orange-Nassau, Duchess of Mecklenburg, etc.
Her mother issued a decree allowing her to adopt her husband's princely title as customary, providing that it be preceded by the title she held as a member of the House of Mecklenburg.
The decree became effective upon her marriage, and changed her full title and style to: Her Royal Highness Princess Juliana of the Netherlands, Princess of Orange-Nassau, Duchess of Mecklenburg, Princess of Lippe-Biesterfeld, etc.
After her accession to the throne, Juliana's official title was: "Her Majesty, Juliana, Queen of the Netherlands, Princess of Orange-Nassau, Duchess of Mecklenburg, Princess of Lippe-Biesterfeld, etc, etc, etc".
Issue

Legacy

References

External links

2 also Princess of Lippe-Biesterfeld



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
  AssignClass (2a967ead-c390-4b4e-8ad1-f5ea97c550c6)
 Call ID: 2a967ead-c390-4b4e-8ad1-f5ea97c550c6
  Args:
    source: Juliana
    type: :Woman
  AssignClass (71b08ebc-d642-43b3-868e-db71561b706a)
 Call ID: 71b08ebc-d642-43b3-868e-db71561b706a
  Args:
    source: Juliana
    type: :Person
  AddLiteral (caad5db7-640d-4289-acb8-2877563f9203)
 Call ID: caad5db7-640d-4289-acb8-2877563f9203
  Args:
    source: Juliana
    relation: :hasBirthYear
    literal_value: 1909
    literal_type: xsd:integer
  AddLiteral (a624b4e8-24e1-4924-9a5e-daa87c11e96b)
 Call ID: a624b4e8-24e1-4924-9a5e-daa87c11e96b
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 2004
    source: Juliana
  AssignClass (fe708313-8a06-47c0-b893-c42a35991da4)
 Call ID: fe708313-8a06-47c0-b893-c42a35991da4
  Args:
    type: :Woman
    source: Wilhelmina
  AssignClass (6fef5e71-02d4-418c-b18b-5c8ee042cb2c)
 Call ID: 6fef5e71-02d4-418c-b18b-5c8ee042cb2c
  Args:
    source: Wilhelmina
    type: :Person
  AssignClass (e8ded591-7fd5-420b-b616-9923b2ff679d)
 Call ID: e8ded591-7fd5-420b-b616-9923b2ff679d
  Args:
    type: :Man
    source: Henry_of_Mecklenburg-Schwerin
  AssignClass (0fb097d0-4055-496c-aab5-6eebcd20ee0f)
 Call ID: 0fb097d0-4055-496c-aab5-6eebcd20ee0f
  Args:
    type: :Person
    source: Henry_of_Mecklenburg-Schwerin
  AddTriple (6a310abd-53ab-4f48-80b4-6f95f426a18e)
 Call ID: 6a310abd-53ab-4f48-80b4-6f95f426a18e
  Args:
    target: Wilhelmina
    relation: :hasMother
    source: Juliana
  AddTriple (9bd268a2-a750-4386-b288-18947f1b8dc9)
 Call ID: 9bd268a2-a750-4386-b288-18947f1b8dc9
  Args:
    target: Henry_of_Mecklenburg-Schwerin
    relation: :hasFather
    source: Juliana
  AssignClass (bee96cc9-a33d-44f1-b1c1-1799f347825a)
 Call ID: bee96cc9-a33d-44f1-b1c1-1799f347825a
  Args:
    source: Bernhard_of_Lippe-Biesterfeld
    type: :Man
  AssignClass (8c1d8cce-f44a-49bb-834e-99596d887809)
 Call ID: 8c1d8cce-f44a-49bb-834e-99596d887809
  Args:
    source: Bernhard_of_Lippe-Biesterfeld
    type: :Person
  AddLiteral (18654964-4206-4e82-bbf6-0128136305e3)
 Call ID: 18654964-4206-4e82-bbf6-0128136305e3
  Args:
    relation: :hasMarriageYear
    literal_value: 1937
    source: Juliana
    literal_type: xsd:integer
  AddTriple (42818f77-aa6e-4320-82e1-85690075e2ed)
 Call ID: 42818f77-aa6e-4320-82e1-85690075e2ed
  Args:
    target: Bernhard_of_Lippe-Biesterfeld
    source: Juliana
    relation: :hasRelation
  AssignClass (686a8017-bd51-4ca7-b39d-2dd7dc952a6c)
 Call ID: 686a8017-bd51-4ca7-b39d-2dd7dc952a6c
  Args:
    type: :Woman
    source: Beatrix
  AssignClass (e5fe4efa-b66f-410e-9683-63d768ab7265)
 Call ID: e5fe4efa-b66f-410e-9683-63d768ab7265
  Args:
    type: :Person
    source: Beatrix
  AssignClass (07fd2736-d199-4bdf-ab5e-7f57735c3b65)
 Call ID: 07fd2736-d199-4bdf-ab5e-7f57735c3b65
  Args:
    type: :Woman
    source: Irene
  AssignClass (e964881f-ef02-4ca9-b945-570623899788)
 Call ID: e964881f-ef02-4ca9-b945-570623899788
  Args:
    type: :Person
    source: Irene
  AssignClass (e2a71c1c-68ef-422d-8b27-db10945dcb0d)
 Call ID: e2a71c1c-68ef-422d-8b27-db10945dcb0d
  Args:
    source: Margriet
    type: :Woman
  AssignClass (5526bbe2-63da-4d12-8032-9e48b1bda8ea)
 Call ID: 5526bbe2-63da-4d12-8032-9e48b1bda8ea
  Args:
    type: :Person
    source: Margriet
  AssignClass (830d0cd2-e5cb-4002-8b15-369a6424edc0)
 Call ID: 830d0cd2-e5cb-4002-8b15-369a6424edc0
  Args:
    source: Christina
    type: :Woman
  AssignClass (481f7290-9a57-4905-b1e9-fa16690dc9a3)
 Call ID: 481f7290-9a57-4905-b1e9-fa16690dc9a3
  Args:
    source: Christina
    type: :Person
  AddTriple (541da1e4-dc5a-44bc-8366-ad9199b044ad)
 Call ID: 541da1e4-dc5a-44bc-8366-ad9199b044ad
  Args:
    relation: :hasChild
    source: Juliana
    target: Beatrix
  AddTriple (b3cba67d-2d92-4e95-bd26-9a462fec145b)
 Call ID: b3cba67d-2d92-4e95-bd26-9a462fec145b
  Args:
    relation: :hasChild
    source: Juliana
    target: Irene
  AddTriple (ef3acdb2-5046-45da-812f-84f261617b33)
 Call ID: ef3acdb2-5046-45da-812f-84f261617b33
  Args:
    source: Juliana
    relation: :hasChild
    target: Margriet
  AddTriple (7e1d5020-3f67-42f9-acba-5b63347bd6f3)
 Call ID: 7e1d5020-3f67-42f9-acba-5b63347bd6f3
  Args:
    target: Christina
    source: Juliana
    relation: :hasChild
  AddTriple (a033237b-73a0-4fb1-9155-e2b5fda3dc26)
 Call ID: a033237b-73a0-4fb1-9155-e2b5fda3dc26
  Args:
    target: Beatrix
    source: Bernhard_of_Lippe-Biesterfeld
    relation: :hasChild
  AddTriple (d4fe7b63-35f2-4332-a8eb-71479739a832)
 Call ID: d4fe7b63-35f2-4332-a8eb-71479739a832
  Args:
    target: Irene
    source: Bernhard_of_Lippe-Biesterfeld
    relation: :hasChild
  AddTriple (a95ae293-d868-4051-9e45-42df9951173a)
 Call ID: a95ae293-d868-4051-9e45-42df9951173a
  Args:
    target: Margriet
    source: Bernhard_of_Lippe-Biesterfeld
    relation: :hasChild
  AddTriple (22397f32-1cc3-41f1-9627-c2d8dbe99c76)
 Call ID: 22397f32-1cc3-41f1-9627-c2d8dbe99c76
  Args:
    relation: :hasChild
    source: Bernhard_of_Lippe-Biesterfeld
    target: Christina
  AssignClass (c653f63b-09a4-4d50-b255-6cb2303b2982)
 Call ID: c653f63b-09a4-4d50-b255-6cb2303b2982
  Args:
    source: Emma
    type: :Woman
  AssignClass (4e6967fc-9ceb-434f-88c2-cd3543497acc)
 Call ID: 4e6967fc-9ceb-434f-88c2-cd3543497acc
  Args:
    type: :Person
    source: Emma
  AssignClass (7f4cd966-652e-4dd5-9a2a-e670296537f9)
 Call ID: 7f4cd966-652e-4dd5-9a2a-e670296537f9
  Args:
    type: :Man
    source: William_III
  AssignClass (eb6e41a4-e91e-4e75-9912-eafc3dfacad3)
 Call ID: eb6e41a4-e91e-4e75-9912-eafc3dfacad3
  Args:
    type: :Person
    source: William_III
  AddTriple (b3fc56c3-65cc-4331-8bf0-4fe1962f416e)
 Call ID: b3fc56c3-65cc-4331-8bf0-4fe1962f416e
  Args:
    relation: :hasFather
    source: Wilhelmina
    target: William_III
  AddTriple (d9d135c7-9c10-4127-9b12-1f9aafe868df)
 Call ID: d9d135c7-9c10-4127-9b12-1f9aafe868df
  Args:
    target: Emma
    relation: :hasMother
    source: Wilhelmina
  AssignClass (2da7868a-34e1-4202-b4d0-5ab6d0c6ce9a)
 Call ID: 2da7868a-34e1-4202-b4d0-5ab6d0c6ce9a
  Args:
    type: :Man
    source: Carlos_Hugo_of_Bourbon
  AssignClass (88ccc25e-511b-421c-98e1-9a418dc73e31)
 Call ID: 88ccc25e-511b-421c-98e1-9a418dc73e31
  Args:
    type: :Person
    source: Carlos_Hugo_of_Bourbon
  AddTriple (35cbe93b-045f-4c9d-bb1f-b42b2eab7fce)
 Call ID: 35cbe93b-045f-4c9d-bb1f-b42b2eab7fce
  Args:
    source: Irene
    relation: :hasRelation
    target: Carlos_Hugo_of_Bourbon
  AssignClass (b936ace9-fad5-4d10-bef2-33cc56b038d9)
 Call ID: b936ace9-fad5-4d10-bef2-33cc56b038d9
  Args:
    type: :Man
    source: Claus_von_Amsberg
  AssignClass (c58b3396-2c44-4889-8168-3e1ff7060539)
 Call ID: c58b3396-2c44-4889-8168-3e1ff7060539
  Args:
    source: Claus_von_Amsberg
    type: :Person
  AddTriple (3f3c117d-432e-4870-9587-4c5d01d3a901)
 Call ID: 3f3c117d-432e-4870-9587-4c5d01d3a901
  Args:
    target: Claus_von_Amsberg
    source: Beatrix
    relation: :hasRelation
  Finish (812702c6-5299-4fc7-97ff-3ce49a4bb2e0)
 Call ID: 812702c6-5299-4fc7-97ff-3ce49a4bb2e0
  Args: