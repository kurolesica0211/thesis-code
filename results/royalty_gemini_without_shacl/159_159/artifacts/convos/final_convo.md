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
Duchess Cecilie Auguste Marie of Mecklenburg-Schwerin (20 September 1886 – 6 May 1954) was the last German Crown Princess and Crown Princess of Prussia as the wife of Wilhelm, German Crown Prince, the son of Wilhelm II, German Emperor.
Cecilie was a daughter of Frederick Francis III, Grand Duke of Mecklenburg-Schwerin and Grand Duchess Anastasia Mikhailovna of Russia.
She was brought up with simplicity, and her early life was peripatetic, spending summers in Mecklenburg and the rest of the year in Southern France.
After the death of her father, she traveled every summer between 1898 and 1904 to her mother's native Russia.
On 6 June 1905, she married German Crown Prince Wilhelm.
Cecilie, tall and statuesque, became popular in Germany for her sense of style.
After the fall of the German monarchy, at the end of World War I, Cecilie and her husband lived mostly apart.
During the Weimar Republic and the Nazi period, Cecilie lived a private life mainly at Cecilienhof Palace in Potsdam.
Early years

Born on 20 September 1886 in Schwerin, Cecilie was the youngest daughter of Frederick Francis III, Grand Duke of Mecklenburg-Schwerin and Grand Duchess Anastasia Mikhailovna of Russia.
She spent most of her childhood in Schwerin, at the royal residences of Ludwigslust Palace and the Gelbensande hunting lodge, only a few kilometres from the Baltic Sea coast.
Her father suffered badly from asthma and the wet damp cold climate of Mecklenburg was not good for his health.
As a result, Cecilie spent a large amount of time with her family in Cannes in the south of France, favoured at the time by European royalty, including some whom Cecilie met such as Empress Eugénie and her future husband's great-uncle, Edward VII.
During the winter visit of 1897, Cecilie's sister, Alexandrine, met her future husband, Crown Prince Christian, later Christian X of Denmark, shortly before the death of their father at the age of 46.
After returning to Schwerin, Cecilie spent time with her widowed mother in Denmark.
After the death of her father, she traveled every summer, from 1898 to 1904, visiting her relatives in Russia.
Cecilie lived there in Mikhailovskoe on Kronstadt Bay, the country home of her maternal grandfather, Grand Duke Michael Nikolaevich of Russia.
Engagement

During the wedding festivities of her brother Frederick Francis IV, Grand Duke of Mecklenburg-Schwerin in Schwerin in June 1904, the 17-year-old Duchess Cecilie got to know her future husband, Wilhelm, German Crown Prince.
Kaiser Wilhelm II had sent his eldest son to the festivities as his personal representative.
Taller than most women of her time at 182 centimetres (over 5'11"), Cecilie was as tall as the German Crown Prince.
Wilhelm was struck by her great beauty, and her dark hair and eyes.
On 4 September 1904, the young couple celebrated their engagement at the Mecklenburg-Schwerin hunting lodge, Gelbensande.
Wedding

The wedding of Duchess Cecilie of Mecklenburg-Schwerin and the German Crown Prince Wilhelm took place on 6 June 1905 in Berlin.
Arriving from Schwerin at Berlin's Lehrter Station, the future Crown Princess was greeted on the platform with a gift of dark red roses.
She was greeted at Bellevue Palace by the entire German imperial family and later made a joyeuse entrée through the Brandenburg Gate to a gun salute in the Tiergarten.
Kaiser Wilhelm II greeted her at the palace and conducted her to the Knight's Hall where over fifty guests from different European royal houses awaited the young bride including Grand Duke Michael Alexandrovich of Russia, Archduke Franz Ferdinand, as well as representatives from Denmark, Italy, Belgium, Portugal and the Netherlands.
On her wedding day, Kaiser Wilhelm II presented his daughter-in-law with the Order of Louise.
On her wedding day, Duchess Cecilie of Mecklenburg-Schwerin became Her Imperial and Royal Highness The German Crown Princess and Crown Princess of Prussia.
She was expected to one day become German empress and queen of Prussia.
German Crown Princess

As German crown princess, Cecilie quickly became one of the most beloved members of the German imperial house.
It was not long before her fashion style was copied by many women throughout the German Empire.
After the end of the wedding festivities, the crown princely couple made their summer residence at the Marble Palace in Potsdam.
Every year at the beginning of the court season in January, the couple would return to the Crown Prince Palace in Berlin on Unter den Linden.
Cecilie's first child was born on 4 July 1906 and given the traditional Hohenzollern name of Wilhelm.
At the time, the German monarchy appeared to be very secure.
Although in public the marriage of the crown prince and princess appeared to be perfect, cracks quickly appeared due to the crown prince's wandering eye and controlling behaviour.
In spite of her husband's unfaithfulness, however, Cecilie had given birth to six children by 1917.
On discovering that Dungern was also having an affair with another woman at court, she confessed to her husband who told him to resign with the words: "Only my consideration for his imperial majesty (his father, Kaiser William II) prevents me from grinding you into the dust.
"


Impact as German Crown Princess

Cecilie made considerable impact in a number of areas including women's education.
On 6 December 1906, at AG Vulcan Stettin's shipyard, she christened  the Norddeutscher Lloyd steamship SS Kronprinzessin Cecilie.
For Cecilie, who had a great passion for the sea since childhood, the gesture brought her great joy and honour.
Cecilie's life in Berlin was a constant round of royal duties: attending military parades, gala state banquets, official ceremonies, and other courtly activities.
In May 1911, Cecilie and the crown prince visited the Russian imperial court in Saint Petersburg.
Queen Mary was particularly fond of the imperial couple and maintained contact with Cecilie until her death in 1953.
The 1911 visit to London was Cecilie's last as representative of the German Empire.
Revolution and the overthrow of the German monarchy

The political and economic situation in the last year of the war became more and more hopeless.
On 6 November 1918, the new German imperial Chancellor, Prince Maximilian of Baden, met with Minister Wilhelm Solf to discuss the future of the German Empire.
They were both of the opinion that the monarchy could only survive with the removal of the kaiser and his son the crown prince and the setting up of a regency under the nominal rule of the young son of Crown Princess Cecilie.
Both the kaiser and the crown prince crossed the border to seek exile in the neutral Netherlands.
Cecilie with her young children was living in Potsdam during the revolutionary period.
It was here that the Empress Auguste Viktoria informed her daughter-in-law, "The revolution has broken out.
"


Life under the republic

The former crown princess was nothing but realistic about the new political situation confronting her family and Germany.
The crown princess was quite prepared to do the same, but wanted to stay in Germany with her children if at all possible.
As a result of a change of circumstances, Cecilie reduced her household staff by 50%.
Her children's tutor also left her service and as a result her two eldest sons, Princes Wilhelm and Louis Ferdinand, for the first time attended as day students at a nearby school.
Cecilie had considerable sympathy for the plight of the German people.
In reply to an address from the German Women's Union in Berlin, the former crown princess stated, "I need no sympathy.
I have the beautiful situation that can befall any German woman, the education of my children as good German citizens.
"


Wilhelm was only allowed to return to Germany from his enforced exile in 1923.
Castle Oels, a castle with 10,000 hectares of workable land in Silesia, now in modern day Poland, provided substantial income for Cecilie's family.
In the absence of her husband, Cecilie became the leading figure in the once ruling House of Hohenzollern.
The former crown princess was under no illusions that the empire would be restored, unlike her father-in-law exiled in Doorn in the Netherlands.
With the election of Gustav Stresemann as chancellor of the Weimar Republic in August 1923, negotiations for the former crown prince commenced.
On the evening of 13 November 1923, Cecilie met her husband at Castle Oels.
The years of separation and the behavior of Wilhelm had made the marriage now merely one in name only, but Cecilie was determined to keep things together even at a distance.
Cecilie remained active within several charity organizations such as the Queen Louise Fund, Chair of the Fatherland's Women Union and the Ladies of the Order of St. John, while keeping clear of any political involvement.
Under Nazi German rule 1933-1939

During 1933–1945, Cecilie lived a private life at Cecilienhof.
Her eldest son Wilhelm forfeited his position as possible heir when he married Dorothea von Salviati on 3 June 1933.
The former crown prince and princess were more understanding of their son than the exiled kaiser.
Cecilie was not perturbed and made the best of the situation and was delighted when she became a grandmother for the first time on 7 June 1934.
In 1935, Cecilie's second son worked, after studying economics and working for a time in the United States as a mechanic for Ford Motor Company, then with Lufthansa.
Her third son, Hubertus, after spending a period of time farming joined the military and then the air force to become a pilot.
In May 1938, Prince Louis Ferdinand married Grand Duchess Kira Kirillovna of Russia, daughter of the pretender to the Russian throne, Grand Duke Cyril Vladimirovich, at Cecilienhof.
World War II

A period of relative calm for Cecilie's family and for Germany came to an end with the outbreak of World War II in September 1939.
Cecilie's 24-year-old nephew, Prince Oskar, fell as a casualty five days after the start of the invasion of Poland.
More personal tragedy occurred when Wilhelm was mortally wounded in battle at Valenciennes in France on 23 May 1940.
Over 50,000 people lined the way to his final resting place in the Antique Temple near the remains of his grandmother, former Empress Auguste Viktoria.
The huge turnout in respect for a prince, who had died a hero's death, from the former ruling dynasty, alarmed and infuriated Adolf Hitler.
As a result, no prince from a former German dynasty was allowed to serve at the front and in 1943 Hitler ordered that they all be discharged from the armed forces.
In 1941, the former Kaiser Wilhelm II died.
At the age of 55, Cecilie's husband became Head of the House of Hohenzollern.
While under the monarchy this would have meant a great change for Cecilie and her husband, the change was potentially dangerous because of the leader of the Nazi German state.
During this time, Cecilie and her husband increasingly retreated to Castle Oels to live a quiet life, far away from the dangers of Berlin.
With the war going badly, Cecilie and her family left the advancing danger of the Soviet Army to return to Potsdam where they celebrated Christmas in December 1944.
In February 1945, Cecilie left Cecilienhof for the last time.
Final years

Cecilie fled the Soviet Army in February 1945 to the sanatorium of Dr. Paul Sotier (personal physician of Kaiser Wilhelm II) Fürstenhof in Bad Kissingen in Bavaria.
Wilhelm had settled into a small house in Hechingen.
Tragedy struck again when yet another son, Hubertus, died from appendicitis on 8 April 1950.
In early 1951, the health of the former Crown Prince deteriorated and on 20 July he died.
On 26 July, his funeral took place at Castle Hohenzollern where he was buried in the ground near an urn containing the ashes of the late Hubertus.
On the arm of her son, Louis Ferdinand, Cecilie bade a final farewell to her husband.
In 1952, Cecilie's memoirs, 'Remembrances' were published.
In an act of healing and friendship, the former Crown Princess Cecilie was received by King George V's widow, Queen Mary, in May 1952 during a visit to England.
Cecilie visited for the first time to attend the christening of her granddaughter, Princess Victoria Marina of Prussia, the daughter of her son Frederick.
Tragedy once again struck when Cecilie's sister, the Danish Queen Mother, Queen Alexandrine, died on 28 December of the same year.
On 3 January 1953, Cecilie attended her funeral at Roskilde Cathedral in Denmark.
From this time on, the former crown princess never fully recovered.
On 12 May 1954, her funeral took place and her remains were interred next to Crown Prince Wilhelm in the grounds of Castle Hohenzollern.
}} Media related to Cecilie of Mecklenburg-Schwerin, German Crown Princess at Wikimedia Commons



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix ns1: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
@prefix ns2: <http://www.w3.org/2003/11/swrl#> .
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

ns1:isRuleEnabled a owl:AnnotationProperty .

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

:x a ns2:Variable .

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

:y a ns2:Variable .

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

[] a ns2:Imp ;
    rdfs:label "infer hasSon" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasBrother" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasSister" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (efe32b96-7225-4fcb-880b-ed4f477de459)
 Call ID: efe32b96-7225-4fcb-880b-ed4f477de459
  Args:
    source: Cecilie_of_Mecklenburg-Schwerin
    type: :Woman
  AddLiteral (e05c5994-1a1b-43d3-a0eb-a7638f9bd192)
 Call ID: e05c5994-1a1b-43d3-a0eb-a7638f9bd192
  Args:
    source: Cecilie_of_Mecklenburg-Schwerin
    relation: :hasBirthYear
    literal_value: 1886
    literal_type: xsd:integer
  AddLiteral (e9a8cd95-111f-48fc-b517-95e9d4e41a17)
 Call ID: e9a8cd95-111f-48fc-b517-95e9d4e41a17
  Args:
    source: Cecilie_of_Mecklenburg-Schwerin
    relation: :hasDeathYear
    literal_value: 1954
    literal_type: xsd:integer
  AssignClass (557047f4-8ff5-451c-ae84-90ee549b60b4)
 Call ID: 557047f4-8ff5-451c-ae84-90ee549b60b4
  Args:
    source: Frederick_Francis_III_of_Mecklenburg-Schwerin
    type: :Man
  AssignClass (7b7a5ad9-ebf7-4d79-bb62-8993bb6ef231)
 Call ID: 7b7a5ad9-ebf7-4d79-bb62-8993bb6ef231
  Args:
    source: Anastasia_Mikhailovna_of_Russia
    type: :Woman
  AddTriple (2f34889f-21b6-46ca-a48c-1c1593589d51)
 Call ID: 2f34889f-21b6-46ca-a48c-1c1593589d51
  Args:
    relation: :hasFather
    source: Cecilie_of_Mecklenburg-Schwerin
    target: Frederick_Francis_III_of_Mecklenburg-Schwerin
  AddTriple (9b9c2ed2-9acd-44ce-bb5f-0af9bf62f892)
 Call ID: 9b9c2ed2-9acd-44ce-bb5f-0af9bf62f892
  Args:
    source: Cecilie_of_Mecklenburg-Schwerin
    relation: :hasMother
    target: Anastasia_Mikhailovna_of_Russia
  AssignClass (ef278004-55d8-4a52-a54f-7275aef43520)
 Call ID: ef278004-55d8-4a52-a54f-7275aef43520
  Args:
    source: Wilhelm_German_Crown_Prince
    type: :Man
  AddTriple (69209940-84b0-43c3-8001-52acff3d4d92)
 Call ID: 69209940-84b0-43c3-8001-52acff3d4d92
  Args:
    target: Wilhelm_German_Crown_Prince
    relation: :hasRelation
    source: Cecilie_of_Mecklenburg-Schwerin
  AddLiteral (75c23582-9592-47f6-ba5d-22d0db295fc2)
 Call ID: 75c23582-9592-47f6-ba5d-22d0db295fc2
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 1905
    source: Cecilie_of_Mecklenburg-Schwerin
  AssignClass (591c8a60-467e-4f9c-bef3-b3c0f2103763)
 Call ID: 591c8a60-467e-4f9c-bef3-b3c0f2103763
  Args:
    source: Wilhelm_II_German_Emperor
    type: :Man
  AddTriple (928c0287-9ea3-4ede-a0d9-b2981f5b308b)
 Call ID: 928c0287-9ea3-4ede-a0d9-b2981f5b308b
  Args:
    source: Wilhelm_German_Crown_Prince
    relation: :hasFather
    target: Wilhelm_II_German_Emperor
  AssignClass (74e047e6-bd88-4987-acac-99f4bb8abace)
 Call ID: 74e047e6-bd88-4987-acac-99f4bb8abace
  Args:
    source: Alexandrine_of_Mecklenburg-Schwerin
    type: :Woman
  AddTriple (845396df-2187-41e6-a53b-17d91462b0a2)
 Call ID: 845396df-2187-41e6-a53b-17d91462b0a2
  Args:
    source: Cecilie_of_Mecklenburg-Schwerin
    relation: :hasSister
    target: Alexandrine_of_Mecklenburg-Schwerin
  AssignClass (a4eff420-abf1-46b8-af6c-7d01d216be96)
 Call ID: a4eff420-abf1-46b8-af6c-7d01d216be96
  Args:
    source: Frederick_Francis_IV_of_Mecklenburg-Schwerin
    type: :Man
  AddTriple (867ac1d8-b5aa-4a15-870c-457492c5e735)
 Call ID: 867ac1d8-b5aa-4a15-870c-457492c5e735
  Args:
    source: Cecilie_of_Mecklenburg-Schwerin
    relation: :hasBrother
    target: Frederick_Francis_IV_of_Mecklenburg-Schwerin
  AssignClass (d88db4e4-f03f-4764-a5b1-2ad9199a3fd7)
 Call ID: d88db4e4-f03f-4764-a5b1-2ad9199a3fd7
  Args:
    source: Michael_Nikolaevich_of_Russia
    type: :Man
  AddTriple (b0931b55-a6bf-4a13-8f2e-ececddc1e7de)
 Call ID: b0931b55-a6bf-4a13-8f2e-ececddc1e7de
  Args:
    target: Michael_Nikolaevich_of_Russia
    relation: :hasFather
    source: Anastasia_Mikhailovna_of_Russia
  AssignClass (b5e2906a-8b8b-4d7a-80d1-e74078976c68)
 Call ID: b5e2906a-8b8b-4d7a-80d1-e74078976c68
  Args:
    source: Wilhelm_son_of_Cecilie
    type: :Man
  AddTriple (4ad6a532-3ed2-4c02-95fd-c3787316b79c)
 Call ID: 4ad6a532-3ed2-4c02-95fd-c3787316b79c
  Args:
    relation: :hasChild
    source: Cecilie_of_Mecklenburg-Schwerin
    target: Wilhelm_son_of_Cecilie
  AssignClass (76977d00-d31a-4f17-87d0-730258db7100)
 Call ID: 76977d00-d31a-4f17-87d0-730258db7100
  Args:
    source: Louis_Ferdinand_son_of_Cecilie
    type: :Man
  AddTriple (b5a3ea88-b8b7-4420-90f6-40b8cfb45a00)
 Call ID: b5a3ea88-b8b7-4420-90f6-40b8cfb45a00
  Args:
    relation: :hasChild
    source: Cecilie_of_Mecklenburg-Schwerin
    target: Louis_Ferdinand_son_of_Cecilie
  AssignClass (ea035b08-c6ce-4100-8c8c-cf1398c3aa44)
 Call ID: ea035b08-c6ce-4100-8c8c-cf1398c3aa44
  Args:
    source: Hubertus_son_of_Cecilie
    type: :Man
  AddTriple (e70c7a2a-989f-4c41-944b-e26402028645)
 Call ID: e70c7a2a-989f-4c41-944b-e26402028645
  Args:
    source: Cecilie_of_Mecklenburg-Schwerin
    relation: :hasChild
    target: Hubertus_son_of_Cecilie
  AssignClass (e2da16b4-6307-4898-a198-cc9ed78acb34)
 Call ID: e2da16b4-6307-4898-a198-cc9ed78acb34
  Args:
    source: Dorothea_von_Salviati
    type: :Woman
  AddTriple (d3bb9c66-301d-48cc-a0ac-783cbf46c4f1)
 Call ID: d3bb9c66-301d-48cc-a0ac-783cbf46c4f1
  Args:
    target: Dorothea_von_Salviati
    source: Wilhelm_son_of_Cecilie
    relation: :hasRelation
  AssignClass (29c0c00f-1cc5-4ffb-9b84-60f5cb7b4a80)
 Call ID: 29c0c00f-1cc5-4ffb-9b84-60f5cb7b4a80
  Args:
    source: Kira_Kirillovna_of_Russia
    type: :Woman
  AddTriple (56fd7c4e-a83c-4bda-bfc2-7b07f57269b1)
 Call ID: 56fd7c4e-a83c-4bda-bfc2-7b07f57269b1
  Args:
    relation: :hasRelation
    source: Louis_Ferdinand_son_of_Cecilie
    target: Kira_Kirillovna_of_Russia
  AssignClass (e6c1766c-6f42-4cd1-b4f9-4bbf1ed0f0d3)
 Call ID: e6c1766c-6f42-4cd1-b4f9-4bbf1ed0f0d3
  Args:
    source: Cyril_Vladimirovich_of_Russia
    type: :Man
  AddTriple (82a7d283-887c-40d4-9f4b-7db1db9d1ca4)
 Call ID: 82a7d283-887c-40d4-9f4b-7db1db9d1ca4
  Args:
    source: Kira_Kirillovna_of_Russia
    relation: :hasFather
    target: Cyril_Vladimirovich_of_Russia
  AssignClass (ba4d0826-fb87-4765-bd4b-74ce8f9e43ed)
 Call ID: ba4d0826-fb87-4765-bd4b-74ce8f9e43ed
  Args:
    source: Auguste_Viktoria
    type: :Woman
  AssignClass (e41845cf-a602-4b5b-a33e-fed4475d3c3e)
 Call ID: e41845cf-a602-4b5b-a33e-fed4475d3c3e
  Args:
    source: Victoria_Marina_of_Prussia
    type: :Woman
  AssignClass (411e1fec-a7ea-4ff8-ae2a-a1c1d46c3889)
 Call ID: 411e1fec-a7ea-4ff8-ae2a-a1c1d46c3889
  Args:
    source: Frederick_son_of_Cecilie
    type: :Man
  AddTriple (a4ba20a3-b457-4ec9-a574-089040bc9512)
 Call ID: a4ba20a3-b457-4ec9-a574-089040bc9512
  Args:
    source: Cecilie_of_Mecklenburg-Schwerin
    relation: :hasChild
    target: Frederick_son_of_Cecilie
  AddTriple (4857c514-65e1-4b50-b33d-ecf255591084)
 Call ID: 4857c514-65e1-4b50-b33d-ecf255591084
  Args:
    target: Victoria_Marina_of_Prussia
    source: Frederick_son_of_Cecilie
    relation: :hasChild
  Finish (20086c4e-f6c4-4be5-a589-4b7d62a7b54d)
 Call ID: 20086c4e-f6c4-4be5-a589-4b7d62a7b54d
  Args: