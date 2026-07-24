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
  AssignClass (f4508f8b-853b-4d59-b710-7e1f2b3fd9c3)
 Call ID: f4508f8b-853b-4d59-b710-7e1f2b3fd9c3
  Args:
    type: :Person
    source: Cecilie_of_Mecklenburg-Schwerin
  AssignClass (52f26766-e826-4814-b0aa-c197391d8927)
 Call ID: 52f26766-e826-4814-b0aa-c197391d8927
  Args:
    source: Cecilie_of_Mecklenburg-Schwerin
    type: :Woman
  AssignClass (db592d86-6d0b-447a-b8fc-491324cf134e)
 Call ID: db592d86-6d0b-447a-b8fc-491324cf134e
  Args:
    source: Wilhelm_German_Crown_Prince
    type: :Person
  AssignClass (22376731-72c7-46ed-8916-99d4135fe3db)
 Call ID: 22376731-72c7-46ed-8916-99d4135fe3db
  Args:
    type: :Man
    source: Wilhelm_German_Crown_Prince
  AssignClass (fe2e4c66-be11-44e4-8071-a09e87681e51)
 Call ID: fe2e4c66-be11-44e4-8071-a09e87681e51
  Args:
    type: :Person
    source: Wilhelm_II_German_Emperor
  AssignClass (8c549a28-6b91-42c4-bf67-6b4d9d6952d9)
 Call ID: 8c549a28-6b91-42c4-bf67-6b4d9d6952d9
  Args:
    source: Wilhelm_II_German_Emperor
    type: :Man
  AssignClass (d3c7e061-9ae1-4eaf-9639-2aaf9e814c5d)
 Call ID: d3c7e061-9ae1-4eaf-9639-2aaf9e814c5d
  Args:
    type: :Person
    source: Frederick_Francis_III_Grand_Duke_of_Mecklenburg-Schwerin
  AssignClass (74d39962-6b85-4e34-94e8-ef526b709692)
 Call ID: 74d39962-6b85-4e34-94e8-ef526b709692
  Args:
    type: :Man
    source: Frederick_Francis_III_Grand_Duke_of_Mecklenburg-Schwerin
  AssignClass (14402753-9e28-45be-b406-23d2ac787f14)
 Call ID: 14402753-9e28-45be-b406-23d2ac787f14
  Args:
    source: Anastasia_Mikhailovna_of_Russia
    type: :Person
  AssignClass (bf52fdca-b1e3-406a-9739-291dcf30b9b7)
 Call ID: bf52fdca-b1e3-406a-9739-291dcf30b9b7
  Args:
    type: :Woman
    source: Anastasia_Mikhailovna_of_Russia
  AddLiteral (fe87d53a-0151-410b-8cf7-6b6afc2889b8)
 Call ID: fe87d53a-0151-410b-8cf7-6b6afc2889b8
  Args:
    literal_type: xsd:integer
    literal_value: 1886
    relation: :hasBirthYear
    source: Cecilie_of_Mecklenburg-Schwerin
  AddLiteral (d17eed14-0fd9-4fa4-afae-22a46816c8e1)
 Call ID: d17eed14-0fd9-4fa4-afae-22a46816c8e1
  Args:
    relation: :hasDeathYear
    literal_value: 1954
    source: Cecilie_of_Mecklenburg-Schwerin
    literal_type: xsd:integer
  AddTriple (5ca0a590-e69e-4bf2-abc9-b3f7f7713c8d)
 Call ID: 5ca0a590-e69e-4bf2-abc9-b3f7f7713c8d
  Args:
    source: Cecilie_of_Mecklenburg-Schwerin
    relation: :hasFather
    target: Frederick_Francis_III_Grand_Duke_of_Mecklenburg-Schwerin
  AddTriple (7d66020b-2bb7-415c-aee7-e6977cbeabb8)
 Call ID: 7d66020b-2bb7-415c-aee7-e6977cbeabb8
  Args:
    target: Anastasia_Mikhailovna_of_Russia
    source: Cecilie_of_Mecklenburg-Schwerin
    relation: :hasMother
  AddTriple (46566661-f66f-4956-ab60-9b037845225f)
 Call ID: 46566661-f66f-4956-ab60-9b037845225f
  Args:
    relation: :hasFather
    source: Wilhelm_German_Crown_Prince
    target: Wilhelm_II_German_Emperor
  AddLiteral (e2888ccf-2cb2-43e0-9791-0e9facb9b260)
 Call ID: e2888ccf-2cb2-43e0-9791-0e9facb9b260
  Args:
    literal_value: 1905
    relation: :hasMarriageYear
    source: Cecilie_of_Mecklenburg-Schwerin
    literal_type: xsd:integer
  AddTriple (b9c2316f-43dd-432b-9ef0-9d855a21e33e)
 Call ID: b9c2316f-43dd-432b-9ef0-9d855a21e33e
  Args:
    relation: :hasRelation
    source: Cecilie_of_Mecklenburg-Schwerin
    target: Wilhelm_German_Crown_Prince
  AssignClass (21bab090-b628-45a3-84f8-0e9fb0278ffb)
 Call ID: 21bab090-b628-45a3-84f8-0e9fb0278ffb
  Args:
    source: Alexandrine_of_Mecklenburg-Schwerin
    type: :Person
  AssignClass (e4d044e8-1585-4a51-92bf-7aaf86cd49b8)
 Call ID: e4d044e8-1585-4a51-92bf-7aaf86cd49b8
  Args:
    source: Alexandrine_of_Mecklenburg-Schwerin
    type: :Woman
  AddTriple (a1c16ead-b8fb-4b4c-9466-61650d66e963)
 Call ID: a1c16ead-b8fb-4b4c-9466-61650d66e963
  Args:
    target: Alexandrine_of_Mecklenburg-Schwerin
    source: Cecilie_of_Mecklenburg-Schwerin
    relation: :hasSister
  AssignClass (c5c62480-b988-4956-99f3-0c94aaf58f36)
 Call ID: c5c62480-b988-4956-99f3-0c94aaf58f36
  Args:
    source: Frederick_Francis_IV_Grand_Duke_of_Mecklenburg-Schwerin
    type: :Person
  AssignClass (7dc23d5d-801e-4fa9-8051-cd55dd772abe)
 Call ID: 7dc23d5d-801e-4fa9-8051-cd55dd772abe
  Args:
    source: Frederick_Francis_IV_Grand_Duke_of_Mecklenburg-Schwerin
    type: :Man
  AddTriple (8319a0ad-4216-4ad3-b3fe-a3982488c7e6)
 Call ID: 8319a0ad-4216-4ad3-b3fe-a3982488c7e6
  Args:
    target: Frederick_Francis_IV_Grand_Duke_of_Mecklenburg-Schwerin
    relation: :hasBrother
    source: Cecilie_of_Mecklenburg-Schwerin
  AssignClass (4b3f627a-0c88-43c3-8020-76b87fcba45d)
 Call ID: 4b3f627a-0c88-43c3-8020-76b87fcba45d
  Args:
    type: :Person
    source: Michael_Nikolaevich_of_Russia
  AssignClass (6ce9b3e2-c397-4f85-8c12-eb5c0c88c202)
 Call ID: 6ce9b3e2-c397-4f85-8c12-eb5c0c88c202
  Args:
    source: Michael_Nikolaevich_of_Russia
    type: :Man
  AddTriple (cb648ee0-3273-45de-8e5d-b5694f0ad1c4)
 Call ID: cb648ee0-3273-45de-8e5d-b5694f0ad1c4
  Args:
    target: Michael_Nikolaevich_of_Russia
    relation: :hasFather
    source: Anastasia_Mikhailovna_of_Russia
  AssignClass (e2bde9e1-f44f-4ea9-a342-0ba927fe94d3)
 Call ID: e2bde9e1-f44f-4ea9-a342-0ba927fe94d3
  Args:
    type: :Person
    source: Wilhelm_Prince_of_Prussia_1906
  AssignClass (270d7fd6-47e5-485f-b3f8-2268aa624b6a)
 Call ID: 270d7fd6-47e5-485f-b3f8-2268aa624b6a
  Args:
    type: :Man
    source: Wilhelm_Prince_of_Prussia_1906
  AddTriple (1a7caa88-1934-4869-9d3f-8625ee4fad8e)
 Call ID: 1a7caa88-1934-4869-9d3f-8625ee4fad8e
  Args:
    relation: :hasChild
    source: Cecilie_of_Mecklenburg-Schwerin
    target: Wilhelm_Prince_of_Prussia_1906
  AddTriple (e778ca22-b7b3-4d1e-bf8b-0867b52cc112)
 Call ID: e778ca22-b7b3-4d1e-bf8b-0867b52cc112
  Args:
    relation: :hasChild
    source: Wilhelm_German_Crown_Prince
    target: Wilhelm_Prince_of_Prussia_1906
  AssignClass (9e56fab5-45fc-4985-837a-2c0eb737d408)
 Call ID: 9e56fab5-45fc-4985-837a-2c0eb737d408
  Args:
    source: Louis_Ferdinand_Prince_of_Prussia
    type: :Person
  AssignClass (5e51c707-128c-44af-9e64-68b6ac29c3db)
 Call ID: 5e51c707-128c-44af-9e64-68b6ac29c3db
  Args:
    type: :Man
    source: Louis_Ferdinand_Prince_of_Prussia
  AddTriple (7b9adbd5-4442-4e98-b1fa-c4b831cf1bce)
 Call ID: 7b9adbd5-4442-4e98-b1fa-c4b831cf1bce
  Args:
    source: Cecilie_of_Mecklenburg-Schwerin
    relation: :hasChild
    target: Louis_Ferdinand_Prince_of_Prussia
  AssignClass (a4fa09c1-e7e1-4b85-9db3-e4dd82fedfbe)
 Call ID: a4fa09c1-e7e1-4b85-9db3-e4dd82fedfbe
  Args:
    type: :Person
    source: Hubertus_Prince_of_Prussia
  AssignClass (5e7520a0-21c9-425a-879d-7736ae58f883)
 Call ID: 5e7520a0-21c9-425a-879d-7736ae58f883
  Args:
    type: :Man
    source: Hubertus_Prince_of_Prussia
  AddTriple (38f155a9-f4c0-450f-bb3d-cd794e810790)
 Call ID: 38f155a9-f4c0-450f-bb3d-cd794e810790
  Args:
    source: Cecilie_of_Mecklenburg-Schwerin
    relation: :hasChild
    target: Hubertus_Prince_of_Prussia
  Finish (5c359b5b-2066-4399-a9ff-7534dda18ba8)
 Call ID: 5c359b5b-2066-4399-a9ff-7534dda18ba8
  Args: