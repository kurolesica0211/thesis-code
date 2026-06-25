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
Alfonso XIII (Spanish: Alfonso León Fernando María Jaime Isidro Pascual Antonio de Borbón y Habsburgo-Lorena; French: Alphonse Léon Ferdinand Marie Jacques Isidore Pascal Antoine de Bourbon; 17 May 1886 – 28 February 1941), also known as El Africano or the African for his Africanist views, was King of Spain from his birth until 14 April 1931, when the Second Spanish Republic was proclaimed.
He became a monarch at birth as his father, Alfonso XII, had died the previous year.
Alfonso's mother, Maria Christina of Austria, served as regent until he assumed full powers on his sixteenth birthday in 1902.
Alfonso XIII's upbringing and public image were closely linked to the military estate; he often presented himself as a soldier-king.
His wedding to Princess Victoria Eugenie of Battenberg in 1906 was marred by an attempt at regicide; he was unharmed.
With public opinion divided over World War I, and moreover a split between pro-German and pro-Entente sympathizers, Alfonso XIII used his relations with other European royal families to help preserve a stance of neutrality, as espoused by his government; however, several factors weakened the monarch's constitutional legitimacy: the rupture of the turno system, the deepening of the Restoration system crisis in the 1910s, a trio of crises in 1917, the spiral of violence in Morocco, and especially the lead-up to the 1923 installment of the dictatorship of Miguel Primo de Rivera, an event that succeeded by means of both military coup d'état and the king's acquiescence.
Upon the political failure of the dictatorship, Alfonso XIII removed support from Primo de Rivera (who was thereby forced to resign in 1930) and favoured (during the dictablanda) an attempted return to the pre-1923 state of affairs.
He left Spain voluntarily after the municipal elections of April 1931 – which was understood as a plebiscite on maintaining the monarchy or declaring a republic – the result of which led to the proclamation of the Second Spanish Republic on 14 April 1931.
Reign

Early life and education

Alfonso XIII was born at the Royal Palace of Madrid on 17 May 1886.
He was the posthumous son of Alfonso XII of Spain, who had died in November 1885, and became king upon his birth.
His mother, Maria Christina of Austria, served as his regent until his sixteenth birthday.
During the regency, in 1898, Spain lost its colonial rule over Cuba, Puerto Rico, Guam and the Philippines to the United States as a result of the Spanish–American War.
Alfonso became seriously ill during the 1889–1890 pandemic.
When Alfonso came of age in May 1902, the week of his majority was marked by festivities, bullfights, balls and receptions throughout Spain.
Alfonso received, to a large extent, a military education that imbued him with "a Spanish nationalism strengthened by his military vocation".
Besides the clique of military tutors, Alfonso also received political teachings from a liberal, Vicente Santamaría de Paredes , and moral precepts from an integrist, José Fernández de la Montaña.
Engagement and marriage

By 1905, Alfonso was looking for a suitable consort.
There he met Princess Victoria Eugenie of Battenberg, the daughter of Edward VII's youngest sister Princess Beatrice, and a granddaughter of Queen Victoria.
Victoria was a Protestant, and would have to become a Catholic.
Victoria's brother, Leopold, was a haemophiliac, so there was a 50 percent chance that Victoria was a carrier of the trait.
Finally, Alfonso's mother Maria Christina wanted him to marry a member of her family, the House of Habsburg-Lorraine, or some other Catholic princess, as she considered the Battenbergs to be non-dynastic.
Victoria was willing to change her religion, and her being a haemophilia carrier was only a possibility.
Maria Christina was eventually persuaded to drop her opposition.
In January 1906 she wrote an official letter to Princess Beatrice proposing the match.
Victoria met Maria Christina and Alfonso in Biarritz, France, later that month, and converted to Catholicism in San Sebastián in March.
Alfonso and Victoria were married at the Royal Monastery of San Jerónimo in Madrid on 31 May 1906, with British royalty in attendance, including Victoria's cousins the Prince and Princess of Wales (later King George V and Queen Mary).
The wedding was marked by an assassination attempt on Alfonso and Victoria by Catalan anarchist Mateu Morral.
On 10 May 1907, the couple's first child, Alfonso, Prince of Asturias, was born.
Victoria was in fact a haemophilia carrier, and Alfonso inherited the condition.
Alfonso distanced himself from his wife for transmitting the condition to their sons.
World War I

During World War I, because of his family connections with both sides and the division of popular opinion, Spain remained neutral.
Alfonso attempted to save the Russian Tsar Nicholas II and his family from the Bolsheviks who captured them, sending two telegrams offering the Russian imperial family refuge in Spain.
As such, he continued to push for the Tsarina Alexandra, a first cousin of Victoria Eugenie, and her four daughters to be brought to Spain, not having realized that they had also been murdered.
Alfonso became gravely ill during the 1918 flu pandemic.
Spain was neutral and thus under no wartime censorship restrictions, so his illness and subsequent recovery were reported to the world, while flu outbreaks in the belligerent countries were concealed.
This gave the misleading impression that Spain was the most affected area and led to the pandemic being dubbed "the Spanish Flu".
Cracking of the system and dictatorship

Following World War I, Spain entered the lengthy yet victorious Rif War (1920–1926) to preserve its colonial rule over northern Morocco.
Critics of the monarchy thought the war was an unforgivable loss of money and lives, and nicknamed Alfonso el Africano ("the African").
Alfonso had not acted as a strict constitutional monarch, and supported the Africanists who wanted to conquer for Spain a new empire in Africa to compensate for the lost empire in the Americas and elsewhere.
Alfonso liked to play favourites with his generals, and one of his most favoured generals was Manuel Fernández Silvestre.
In 1921, when Silvestre advanced up into the Rif mountains of Morocco, Alfonso sent him a telegram whose first line read "Hurrah for real men!", urging Silvestre not to retreat at a time when Silvestre was experiencing major difficulties.
Silvestre stayed the course, leading his men into the Battle of Annual, one of Spain's worst defeats.
Alfonso, who was on holiday in the south of France at the time, was informed of the "Disaster of the Annual" while he was playing golf.
Reportedly, Alfonso's response to the news was to shrug his shoulders and say "Chicken meat is cheap", before resuming his game.
Alfonso remained in France and did not return to Spain to comfort the families of the soldiers lost in the battle, which many people at the time saw as a callous and cold act, a sign that the King was indifferent over the lives of his soldiers.
After the "Disaster of the Annual", Spain's war in the Rif went from bad to worse, and as the Spanish were barely hanging on to Morocco, support for the abandonistas grew as many people could see no point to the war.
These generals were associated with the innermost military clique of Alfonso XIII and wanted to prevent investigations about Annual from tarnishing the monarch, even if Primo de Rivera had embraced Abandonista positions prior to that point.
In 1925, Alfonso was the target of an assassination plot by Catalan separatists while in Barcelona.
On 28 January 1930, amid economic problems, general unpopularity and a putschist plot led by General Manuel Goded in motion, of which Alfonso XIII was most probably aware, Miguel Primo de Rivera was forced to resign, exiling to Paris, only to die a few weeks later of the complications from diabetes in combination with the effects of a flu.
Alfonso XIII appointed General Dámaso Berenguer as the new prime minister.
Back in 1926, Alfonso XIII had appointed Berenguer as Chief of Staff of the Military House of the King, a post conventionally fit for burned-out generals in order to move them away from the spotlight for a time in a show of affection.
Alfonso XIII fled the country and the Second Spanish Republic was peacefully proclaimed on 14 April 1931.
Some of the grievances against the actions of Alfonso XIII as a king included interference in state institutions to reinforce his personal power, bargaining personal support from the military clique with rewards and merits, his abuse of the power to dissolve the legislature, rendering the co-sovereignty between the Nation and the Crown a total fiction; that he had disproportionately fostered the Armed forces (often to contain internal protest), had used the armed forces abroad with imperialist aims alien to the interests of the nation but his own, that he had personally devised the military operation of Annual behind the back of the Council of Ministers, and that following the massacre of Annual that "cost the lives of thousands of Spanish lads", he had decided to launch a coup with the help of a few generals rather than facing scrutiny in the legislature.
The debate ended with an eloquent speech by Prime Minister Manuel Azaña pleading for the unanimity of the house "to condemn and exclude D. Alfonso de Borbón from the law, proclaiming the majesty of our republic, the unbreakable will of our civism and the permanence of the Spanish glories framed by the institutions freely given by the Nation".
The house passed the act brought forward by the Commission of Responsibilities, summarizing Alfonso de Borbón's responsibilities as being guilty of high treason.
Involved in anti-Republican plots from his exile, and keen to draw support from the Carlists in the context of the uneasy and competing relations between the Carlist and Alfonsist factions within the radicalised monarchist camp, in the aftermath of so-called Pact of Territet he issued a statement dated 23 January 1932 endorsing the manifesto launched by Carlist claimant Alfonso Carlos (in which the latter hinted at the cession of dynastic rights should the former king accept "those fundamental principles which in our traditional regime have been demanded of all Kings with precedence of personal rights"), with the dethroned king likewise accusing in the document the reformist Republic to be "inspired and sponsored by communism, freemasonry and judaism".
In 1933, his two eldest sons, Alfonso and Jaime, renounced their claims to the defunct throne on the same day, and in 1934 his youngest son Gonzalo died.
After the July 1936 attempted coup d'état against the democratically elected Republican government a war broke out in Spain.
On 30 July 1936, Alfonso's son Juan took the initiative of leaving Cannes to go to Spain to join the rebel faction, with the former king (then in a hunting trip in Czechoslovakia) reportedly giving consent, so Juan de Borbón crossed the border set to join the front in Somosierra dressed in a blue jumpsuit and red beret under the fake name "Juan López".
In September 1936, the general who had emerged as leader of the rebel faction, Francisco Franco, declared that he would not restore Alfonso as king.
Death

On 15 January 1941, Alfonso XIII renounced his rights to the defunct Spanish throne in favour of Juan.
In Spain, dictator Francisco Franco ordered three days of national mourning.
The ex-king's funeral was held in Rome in the Church of Santa Maria degli Angeli e dei Martiri.
He was buried in the Church of Santa Maria in Monserrato degli Spagnoli, the Spanish national church in Rome, immediately below the tombs of Popes Callixtus III and Alexander VI.
In January 1980 his remains were transferred to El Escorial in Spain.
Legacy

Alfonso was a promoter of tourism in Spain.
He also supported the creation of a network of state-run lodges, Paradores, in historic buildings of Spain.
An avenue in the northern Madrid neighbourhood of Chamartín, Avenida de Alfonso XIII, is named after him.
A plaza or town centre in Iloilo City, Philippines (now Plaza Libertad) was named in his honour called Plaza Alfonso XIII.
A street in Merthyr Tydfil, in Wales, was built especially to house Spanish immigrants in the mining industry and named Alphonso Street after Alfonso XIII.
Ratoncito Pérez first appeared as the Spanish equivalent to the Tooth Fairy in a 1894 tale written by Luis Coloma for King Alfonso XIII, who had just lost a milk tooth at the age of eight, with the King appearing in the tale as "King Buby".
The tradition of Ratoncito Pérez replacing the lost milk teeth with a small payment or gift while the child sleeps is almost universally followed today in Spain and Hispanic America.
Alfonso XIII is also mentioned on the plaque that the City Council of Madrid dedicated in 2003 to Ratoncito Pérez on the second floor of number eight of Calle del Arenal , where the mouse was said to have lived.
Personal life

Legitimate and illegitimate children

Alfonso and his wife Princess Victoria Eugenie of Battenberg (Ena) had seven children:


Alfonso also had a number of reported illegitimate children that are known, including: 


Attitude towards Jews

Alfonso was known for his friendly attitude towards Jews and publicly praised them.
In 1917, Alfonso instructed the Spanish consul in Jerusalem, Antonio de la Cierva y Lewita, Count of Ballobar, to help protect Palestinian Jews.
On another occasion, after a high official in Tetuan had committed onslaughts against Jews, a delegation composed of Catholics, Jews, and Muslims appealed to Alfonso.
According to the Jewish Professor Abraham S.E. Yahuda, Alfonso told Yahuda in private conversations that he would issue no policies of discrimination towards Jews, believing all of his Spanish subjects to be entitled to equal rights and protection.
Pornographic cinema

Alfonso is occasionally referred to as "the playboy king", due in part to his promotion and collection of Spanish pornographic films, as well as his extramarital affairs.
Alfonso commissioned pornographic films through the Barcelona production company Royal Films, with the Count of Romanones acting as an intermediary figure between him and the company.
Between forty and seventy pornographic films are said to have been shot in total (three of which have been preserved) and were screened in Barcelona's Chinatown, as well as during Alfonso's private screenings.
These films featured content considered immoral and degenerate, including sexual relationships involving Catholic priests and "women with enormous breasts" (the last of which is said to have been Alfonso's passion).
This has led some to speculate that Alfonso may have possessed a sexual addiction.



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
  AssignClass (0a0f92e3-b29e-4a61-a4a0-b469f6e8afdb)
 Call ID: 0a0f92e3-b29e-4a61-a4a0-b469f6e8afdb
  Args:
    source: Alfonso_XIII
    type: :Man
  AssignClass (5a5cc01e-2989-4689-bff9-d3f337106d7e)
 Call ID: 5a5cc01e-2989-4689-bff9-d3f337106d7e
  Args:
    source: Alfonso_XIII
    type: :Person
  AssignClass (8f37bd15-8044-4575-bcd8-2f8ac3ee86ad)
 Call ID: 8f37bd15-8044-4575-bcd8-2f8ac3ee86ad
  Args:
    source: Alfonso_XII
    type: :Man
  AssignClass (384a7b1d-9292-4030-97e2-78e3f7e6a86b)
 Call ID: 384a7b1d-9292-4030-97e2-78e3f7e6a86b
  Args:
    source: Alfonso_XII
    type: :Person
  AssignClass (3d110d57-eef9-47d2-a401-dc9ab9b0d0ec)
 Call ID: 3d110d57-eef9-47d2-a401-dc9ab9b0d0ec
  Args:
    source: Maria_Christina_of_Austria
    type: :Woman
  AssignClass (2b47d588-196d-45a6-9d59-7dcd7832acd0)
 Call ID: 2b47d588-196d-45a6-9d59-7dcd7832acd0
  Args:
    source: Maria_Christina_of_Austria
    type: :Person
  AssignClass (bcac9d10-6c93-41c6-9207-7fe1f024daff)
 Call ID: bcac9d10-6c93-41c6-9207-7fe1f024daff
  Args:
    source: Victoria_Eugenie_of_Battenberg
    type: :Woman
  AssignClass (8735cbd9-dc58-4978-9c29-2405785edc06)
 Call ID: 8735cbd9-dc58-4978-9c29-2405785edc06
  Args:
    source: Victoria_Eugenie_of_Battenberg
    type: :Person
  AssignClass (a0482048-d6e0-4427-a778-5c660f23c6ce)
 Call ID: a0482048-d6e0-4427-a778-5c660f23c6ce
  Args:
    source: Alfonso_Prince_of_Asturias
    type: :Man
  AssignClass (68526eda-d60b-4c17-9a88-87207f72d2fa)
 Call ID: 68526eda-d60b-4c17-9a88-87207f72d2fa
  Args:
    source: Alfonso_Prince_of_Asturias
    type: :Person
  AssignClass (53b2d5fe-6eda-4281-a4ac-97f7f13e3203)
 Call ID: 53b2d5fe-6eda-4281-a4ac-97f7f13e3203
  Args:
    source: Jaime
    type: :Man
  AssignClass (a26dcd48-31fa-4c24-a8de-d7e94d960630)
 Call ID: a26dcd48-31fa-4c24-a8de-d7e94d960630
  Args:
    source: Jaime
    type: :Person
  AssignClass (98b01941-6d9b-4af9-83ec-dd00a331af1f)
 Call ID: 98b01941-6d9b-4af9-83ec-dd00a331af1f
  Args:
    source: Gonzalo
    type: :Man
  AssignClass (36f43661-d8f0-417d-9939-316258c674be)
 Call ID: 36f43661-d8f0-417d-9939-316258c674be
  Args:
    source: Gonzalo
    type: :Person
  AssignClass (929e5b1f-4b2f-4c9f-a857-99d1be0de175)
 Call ID: 929e5b1f-4b2f-4c9f-a857-99d1be0de175
  Args:
    source: Juan_de_Borbon
    type: :Man
  AssignClass (bc8cd840-3478-4e9b-9304-9c1b00829e61)
 Call ID: bc8cd840-3478-4e9b-9304-9c1b00829e61
  Args:
    source: Juan_de_Borbon
    type: :Person
  AddLiteral (f4808bc8-cd36-4992-9a66-a10863bec775)
 Call ID: f4808bc8-cd36-4992-9a66-a10863bec775
  Args:
    source: Alfonso_XIII
    literal_value: 1886
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (f8b348c4-b46b-4d8b-bced-0ed08ed6b666)
 Call ID: f8b348c4-b46b-4d8b-bced-0ed08ed6b666
  Args:
    literal_value: 1941
    source: Alfonso_XIII
    relation: :hasDeathYear
    literal_type: xsd:integer
  AddTriple (2ed94bf7-7791-4e15-8b10-d849841877e8)
 Call ID: 2ed94bf7-7791-4e15-8b10-d849841877e8
  Args:
    target: Alfonso_XII
    relation: :hasFather
    source: Alfonso_XIII
  AddTriple (5266e73d-612b-42fe-9296-723617a2960d)
 Call ID: 5266e73d-612b-42fe-9296-723617a2960d
  Args:
    relation: :hasMother
    target: Maria_Christina_of_Austria
    source: Alfonso_XIII
  AddTriple (0238aa31-68b5-4a0e-adc2-feb1ff506a19)
 Call ID: 0238aa31-68b5-4a0e-adc2-feb1ff506a19
  Args:
    target: Alfonso_XIII
    relation: :hasFather
    source: Alfonso_Prince_of_Asturias
  AddTriple (c9ea15a2-5e33-45ea-89cc-bf39864454cd)
 Call ID: c9ea15a2-5e33-45ea-89cc-bf39864454cd
  Args:
    relation: :hasMother
    target: Victoria_Eugenie_of_Battenberg
    source: Alfonso_Prince_of_Asturias
  AddTriple (34859172-1ba5-4205-b6fa-00c80b49df18)
 Call ID: 34859172-1ba5-4205-b6fa-00c80b49df18
  Args:
    source: Jaime
    relation: :hasFather
    target: Alfonso_XIII
  AddTriple (b5e175f5-00cc-410d-99ba-90aaa39a28f4)
 Call ID: b5e175f5-00cc-410d-99ba-90aaa39a28f4
  Args:
    source: Jaime
    target: Victoria_Eugenie_of_Battenberg
    relation: :hasMother
  AddTriple (ac1bde58-a6de-4441-96cb-28486031d799)
 Call ID: ac1bde58-a6de-4441-96cb-28486031d799
  Args:
    source: Gonzalo
    relation: :hasFather
    target: Alfonso_XIII
  AddTriple (772cb27d-1967-4a6c-a941-7eedc03936d3)
 Call ID: 772cb27d-1967-4a6c-a941-7eedc03936d3
  Args:
    source: Gonzalo
    target: Victoria_Eugenie_of_Battenberg
    relation: :hasMother
  AddTriple (0610c253-343d-43cb-8893-c7f7fb79c479)
 Call ID: 0610c253-343d-43cb-8893-c7f7fb79c479
  Args:
    relation: :hasFather
    target: Alfonso_XIII
    source: Juan_de_Borbon
  AddTriple (32e15553-60b0-4dfb-8134-dc81fd92fb59)
 Call ID: 32e15553-60b0-4dfb-8134-dc81fd92fb59
  Args:
    source: Juan_de_Borbon
    target: Victoria_Eugenie_of_Battenberg
    relation: :hasMother
  AddLiteral (005500a7-3887-417f-9e10-144afa149a34)
 Call ID: 005500a7-3887-417f-9e10-144afa149a34
  Args:
    relation: :hasMarriageYear
    literal_value: 1906
    source: Alfonso_XIII
    literal_type: xsd:integer
  AddTriple (2a10cb5f-937b-4911-b8fd-0c9b029b5902)
 Call ID: 2a10cb5f-937b-4911-b8fd-0c9b029b5902
  Args:
    source: Alfonso_XIII
    relation: :hasRelation
    target: Victoria_Eugenie_of_Battenberg
  AddLiteral (fbff1955-4b42-4871-8992-b586026cce28)
 Call ID: fbff1955-4b42-4871-8992-b586026cce28
  Args:
    literal_type: xsd:string
    relation: :alsoKnownAs
    source: Alfonso_XIII
    literal_value: El Africano
  AddLiteral (cb42f0d4-97d9-428b-b659-fa33a18ead51)
 Call ID: cb42f0d4-97d9-428b-b659-fa33a18ead51
  Args:
    literal_type: xsd:string
    literal_value: the African
    source: Alfonso_XIII
    relation: :alsoKnownAs
  Finish (acb0a447-f69b-48b4-bcb7-07cc55d03a3d)
 Call ID: acb0a447-f69b-48b4-bcb7-07cc55d03a3d
  Args: