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
Princess Olga of Greece and Denmark (Greek: Όλγα; 11 June 1903 – 16 October 1997) was a Greek and Danish princess who married Prince Paul, Regent of the Kingdom of Yugoslavia.
After her marriage, she was known as Princess Paul of Yugoslavia.
Princess Olga was a daughter of Prince Nicholas of Greece and Denmark and Grand Duchess Elena Vladimirovna of Russia, and a granddaughter of King George I of Greece.
After a brief engagement in 1922 to Crown Prince Frederik of Denmark, she married Prince Paul of Yugoslavia in 1923.
In 1934, after the assassination of King Alexander I, Prince Paul was appointed regent of Yugoslavia on behalf of King Peter II, and Princess Olga became the senior lady of the court and acted as first lady of Yugoslavia, working side by side with her husband on representation duties.
In 1941, during the Second World War, Prince Paul was forcibly removed from power after signing the Tripartite Pact, which took Yugoslavia into the Axis with Germany and Italy.
Paul, Olga, and their three children were arrested and given as prisoners to the British.
The couple and their children eventually settled in Paris, France, where Paul died in 1976.
Having become a widow, Olga spent more and more time in the United Kingdom, the adopted country of her sister, Marina.
Struck by Alzheimer's disease at the end of her life, Olga died in Paris in 1997.
Biography

Early life

Childhood

A granddaughter of King George I of Greece, Princess Olga was born at Tatoi Palace, the second home of the Greek royal family, in 1903 to Prince Nicholas of Greece and Denmark (1872–1938) and his wife Grand Duchess Elena Vladimirovna of Russia (1882–1957).
As was the Greek tradition, she was then named after her paternal grandmother, Queen Olga.
She grew up alongside her parents and younger sisters, Princesses Elizabeth (1904–1955) and Marina (1906–1968), at the Nicholas Palace, the current seat of the Italian Embassy in Athens.
Olga was brought up in relative simplicity and her early education was overseen by an English Norland nurse by the name of Miss Fox.
Once a year, Olga and her family travelled to Russia, where they were regularly received by their Romanov cousins.
The princess and her sisters thus had the opportunity to play with the daughters of Tsar Nicholas II, who were roughly the same age as them.
After the fallout between King Constantine I and his prime minister Eleftherios Venizelos over whether Greece should enter the conflict, a virtual civil war shook the Hellenic kingdom, which was partially occupied by the Allies from 1915.
Finally, on 10 June 1917, King Constantine was forced to leave power by the ultimatum of the French High Commissioner Charles Jonnart and he went into exile with his wife and children in German-speaking Switzerland.
Described as the "evil genius behind the monarchy" by the Venizelists, Prince Nicolas was quickly forced to leave Athens in turn and join his brother abroad.
Olga and her family then settled in St. Moritz, when Greece fell into a financial crisis for the first time during her lifetime.
The restoration of Constantine I in 1920 allowed Olga to return to her native country for a brief period, but the king's final abdication in 1922 forced the young princess and her relatives to resume their life in exile.
The princess then settled successively in Sanremo, Paris and London, where she lived with members of her family.
Broken engagement

Considered, along with her sister Marina, to be "one of the most beautiful young women of her time", Princess Olga had, according to biographer Ricardo Mateos Sainz de Medrano, a "discreet, romantic and fragile personality".
Prior to her departure into exile, she was linked to the future Frederik IX of Denmark and the engagement of the pair was announced publicly in 1922.
However, the awkwardness of the Danish prince, who held the hand of one of Olga's sisters instead of hers during the official presentation of the young couple to the Athenian crowd, lastingly humiliated the future bride.
Shortly after the event, Olga decided to return her ring to the heir to the Danish throne and called off their engagement.
After moving to the UK, Olga's love life was the subject of much speculation.
Public rumors and claims circulated about her romantic relationships and she was linked to the Prince of Wales (later Edward VIII) for some time.
Neither Edward nor Olga confirmed the rumors.
A frequent guest of the British upper class, the Greek princess met Prince Paul of Yugoslavia, a grandson of Alexander Karađorđević, Prince of Serbia, at a ball given by her cousin Lady Zia Wernher.
Immediately impressed by the beauty of Olga, Paul sought to win the favor of the princess, but she was rather indifferent to him.
However, other encounters followed, notably at Buckingham Palace, and Prince Paul finally managed to catch her attention.
In Yugoslavia

Marriage and settlement in Yugoslavia

Once Olga and Paul's engagement was announced on 26 July 1923, the young princess' trousseau was purchased and prepared in Paris.
However, it was in Belgrade, in the prince's homeland, that the wedding was organized the following October.
Now Princess of Yugoslavia, Olga began learning Serbo-Croatian, which she quickly mastered though with a heavy Greek accent.
Dividing her life between the White Palace in Belgrade, a magnificent chalet in the Bohinj valley and a villa on Rumunska Ulica (now Užička Ulica), Olga benefited from the fortune that her husband partly inherited from his maternal family.
However, accustomed to a less provincial lifestyle, the princess found her daily life more monotonous and boring.
Her relationship with King Alexander I of Yugoslavia and his wife were not warm.
Olga, however, received regular visits from her sisters and other family members.
She gave birth to three children between 1924 and 1936, Prince Alexander (1924–2016), Prince Nikola (1928–1954), and Princess Elizabeth (born 1936), and spent a lot of time caring for them while her husband devoted himself to his art collections.
Regency of Paul

On 9 October 1934 King Alexander I of Yugoslavia was assassinated during an official visit to Marseille by a Macedonian nationalist member of IMRO.
His successor, the young Peter II was eleven years old, and a Council of Regency was set up under the leadership of Prince Paul.
Although she had never aspired to a political life, Olga's husband had no choice but to accept the responsibility that fell to him and took control of state affairs.
Having become in essence the "first lady" of Yugoslavia, Olga had to more than ever represent her country alongside her husband.
In the tense context of the late 1930s, the strongly-Anglophile Prince Paul gradually committed his country to a policy of alliance with the Axis powers.
It would seem, moreover, that the family ties between Olga and various members of the German upper class who embraced the Nazi ideology (including her cousin, Prince Philip of Hesse) had an effect on the political development of Prince Paul.
In 1938, Olga left Yugoslavia for a long time to look after several elderly relatives.
She stayed in Athens to witness the final days of her father, Prince Nicolas, and to take care of her mother, the Grand Duchess Elena Vladimirovna.
A few months later, the princess travelled to Paris, where she reunited with her father-in-law, Prince Arsen of Yugoslavia, who died shortly afterward.
Second World War

After the outbreak of the Second World War, Prince Paul signed a treaty of alliance on 25 March 1941 and brought his country into the Axis camp.
Paul, Olga and their three children were then arrested and handed over to the British, who deported them to Greece (where they were welcomed by King George II) then to Egypt (under the pretext of intrigue).
Olga and her family were next sent to Kenya, where they arrived after three days of travel, on 28 April 1941.
Condemned to inactivity, Olga therefore devoted her days to maintaining the residence, learning to cook and supervising the education of her children, while her husband sank into melancholy and depression.
In September 1942, the death of Prince George, Duke of Kent, in an air crash left his wife, Princess Marina, inconsolable and the British government had to allow Olga to stay in the United Kingdom to keep her sister's company.
Olga took advantage of her stay in Britain to plead her husband's cause to the government but without much success.
Back in Kenya in January 1943, the princess found her husband severely affected by depression.
As Paul's condition did not improve, the British government finally allowed Olga's family to settle in South Africa in June 1943.
Olga and her family were finally allowed to return to Europe in 1948.
Later life

Return to Europe

In 1948, Paul, Olga and their three children were finally granted permission to leave South Africa, but Yugoslavia had adopted a communist regime in 1945 and they could not return to their country.
Olga also made frequent trips to London and Florence, where Paul owned Villa di Pratolino located not far from thumb|upright=1.2|Villa Sparta.
In Tuscany, Olga had the pleasure of reuniting with her cousin and friend Helen, Queen Mother of Romania, while in the United Kingdom she was always welcomed by her sister Marina, Duchess of Kent, and the rest of the British royal family.
In 1954, Olga and Paul's second son, Nikola, was killed in a car accident in England.
In 1957, Olga's mother Elena Vladimirovna died in Athens, Greece.
Final years

Widowed in 1976, Olga stayed for longer periods in Great Britain.
With her sister Marina's death in 1968, she was accommodated at Kensington Palace, with Princess Alice, Countess of Athlone, and after the latter's death, directly at Clarence House with Queen Elizabeth
The Greek princess then acquired the reputation of being a demanding guest.
As she aged, Olga's health began to deteriorate.
However, she continued to attend the great events of European royalty, such as the weddings of Crown Prince Alexander of Yugoslavia in 1972, her nephew Prince Michael of Kent in 1978, and Prince Charles and Lady Diana Spencer in 1981.
At the wedding of the Yugoslav pretender, it was also Princess Olga who accompanied him to the altar, as the prince's mother and grandmother were not able to attend the ceremony due to health issues.
Illness and death

Affected by Alzheimer's disease at the end of her life, Princess Olga was hospitalized for a long time in Meudon.
However, with Olga being heavily affected by the disease, the project of her daughter caused a scandal.
Prince Alexander brought a complaint against his sister Elizabeth before the French courts for damage to the image of their mother and claimed, in her name, $107,000 in damages.
Princess Olga died in Paris on 16 October 1997.
On 28 September 2012, the remains of Princess Olga, her husband and their son Nikola were exhumed and then transported to Belgrade, Serbia.
On 4 October, an official ceremony was held at St. Michael's Cathedral in Belgrade by Irinej, Serbian Patriarch.
The children and grandchildren of the couple, as well as Crown Prince Alexander and his wife Princess Katherine, and Serbian President Tomislav Nikolić and his government participated in the event.
Notes and references

Notes

References

Bibliography

Biographies of the princess

About the princess and her family

Memoirs by family members

External links

@media screen{html.skin-theme-clientpref-night .mw-parser-output .sister-inline-image img{filter:invert(1)brightness(55%)contrast(250%)hue-rotate(180deg)}}@media screen and (prefers-color-scheme:dark){html.skin-theme-clientpref-os .mw-parser-output .sister-inline-image img{filter:invert(1)brightness(55%)contrast(250%)hue-rotate(180deg)
}} Media related to Princess Olga of Greece and Denmark at Wikimedia Commons



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
  AssignClass (47dacd22-be34-487d-8283-6116b0f759e4)
 Call ID: 47dacd22-be34-487d-8283-6116b0f759e4
  Args:
    source: :Princess_Olga_of_Greece_and_Denmark
    type: :Woman
  AssignClass (92b442a1-9f41-4a61-b208-3d77efb8c713)
 Call ID: 92b442a1-9f41-4a61-b208-3d77efb8c713
  Args:
    source: :Princess_Olga_of_Greece_and_Denmark
    type: :Person
  AddLiteral (7bc18779-2615-472c-9e8b-a2b3050a7d7c)
 Call ID: 7bc18779-2615-472c-9e8b-a2b3050a7d7c
  Args:
    relation: :hasBirthYear
    literal_value: 1903
    literal_type: xsd:integer
    source: :Princess_Olga_of_Greece_and_Denmark
  AddLiteral (745c32b5-203c-45b3-a95d-5bb03ce9b9cf)
 Call ID: 745c32b5-203c-45b3-a95d-5bb03ce9b9cf
  Args:
    relation: :hasDeathYear
    source: :Princess_Olga_of_Greece_and_Denmark
    literal_type: xsd:integer
    literal_value: 1997
  AddLiteral (ce0fac20-4be8-4f0b-8e9d-bae421c2a445)
 Call ID: ce0fac20-4be8-4f0b-8e9d-bae421c2a445
  Args:
    source: :Princess_Olga_of_Greece_and_Denmark
    literal_value: Princess Paul of Yugoslavia
    literal_type: xsd:string
    relation: :alsoKnownAs
  AssignClass (a672d3b7-9bbe-4182-a1c0-227cc59811c0)
 Call ID: a672d3b7-9bbe-4182-a1c0-227cc59811c0
  Args:
    source: :Prince_Paul_of_Yugoslavia
    type: :Man
  AssignClass (80c65fa4-fef1-4a84-a75a-f1588cd14832)
 Call ID: 80c65fa4-fef1-4a84-a75a-f1588cd14832
  Args:
    type: :Person
    source: :Prince_Paul_of_Yugoslavia
  AddLiteral (02b8eade-d22d-48bf-8cd8-d923b1961d77)
 Call ID: 02b8eade-d22d-48bf-8cd8-d923b1961d77
  Args:
    relation: :hasDeathYear
    literal_value: 1976
    literal_type: xsd:integer
    source: :Prince_Paul_of_Yugoslavia
  AddLiteral (7dbb60b3-7cb2-4025-b957-9055e34a1989)
 Call ID: 7dbb60b3-7cb2-4025-b957-9055e34a1989
  Args:
    relation: :hasMarriageYear
    source: :Princess_Olga_of_Greece_and_Denmark
    literal_value: 1923
    literal_type: xsd:integer
  AddTriple (f8da06fb-2e04-484c-b701-1fb2ccd72b5c)
 Call ID: f8da06fb-2e04-484c-b701-1fb2ccd72b5c
  Args:
    relation: :hasRelation
    target: :Prince_Paul_of_Yugoslavia
    source: :Princess_Olga_of_Greece_and_Denmark
  AssignClass (ad64cab1-3ae2-45bc-b4a2-f8cfd96d6705)
 Call ID: ad64cab1-3ae2-45bc-b4a2-f8cfd96d6705
  Args:
    source: :Prince_Nicholas_of_Greece_and_Denmark
    type: :Man
  AssignClass (de13e3f3-13cb-4e6d-9c59-b115d50576e6)
 Call ID: de13e3f3-13cb-4e6d-9c59-b115d50576e6
  Args:
    type: :Person
    source: :Prince_Nicholas_of_Greece_and_Denmark
  AddTriple (479a3517-b3c6-400d-8652-b5c20ac53152)
 Call ID: 479a3517-b3c6-400d-8652-b5c20ac53152
  Args:
    source: :Princess_Olga_of_Greece_and_Denmark
    target: :Prince_Nicholas_of_Greece_and_Denmark
    relation: :hasFather
  AssignClass (e32e0d61-4a1d-4d87-9cdf-9ef83b4ef26c)
 Call ID: e32e0d61-4a1d-4d87-9cdf-9ef83b4ef26c
  Args:
    source: :Grand_Duchess_Elena_Vladimirovna_of_Russia
    type: :Woman
  AssignClass (29080953-4e84-403f-832d-0c8309de23f8)
 Call ID: 29080953-4e84-403f-832d-0c8309de23f8
  Args:
    source: :Grand_Duchess_Elena_Vladimirovna_of_Russia
    type: :Person
  AddTriple (1b4046d5-86f4-4cbb-a9eb-f35cb1bd5040)
 Call ID: 1b4046d5-86f4-4cbb-a9eb-f35cb1bd5040
  Args:
    relation: :hasMother
    source: :Princess_Olga_of_Greece_and_Denmark
    target: :Grand_Duchess_Elena_Vladimirovna_of_Russia
  AssignClass (a7971b36-4cb6-4837-8012-8929500fd073)
 Call ID: a7971b36-4cb6-4837-8012-8929500fd073
  Args:
    source: :King_George_I_of_Greece
    type: :Man
  AssignClass (6c040e87-c488-42e6-998d-8b9403ca059d)
 Call ID: 6c040e87-c488-42e6-998d-8b9403ca059d
  Args:
    type: :Person
    source: :King_George_I_of_Greece
  AddTriple (0bc9f68f-38f6-4b03-8859-24d53a64e22f)
 Call ID: 0bc9f68f-38f6-4b03-8859-24d53a64e22f
  Args:
    source: :Princess_Olga_of_Greece_and_Denmark
    target: :King_George_I_of_Greece
    relation: :hasAncestor
  AssignClass (31d1f9cc-a7f9-4b0a-87d8-2f7a04106489)
 Call ID: 31d1f9cc-a7f9-4b0a-87d8-2f7a04106489
  Args:
    source: :Princess_Elizabeth_of_Greece_and_Denmark
    type: :Woman
  AssignClass (e069befe-b232-4a7d-bbbc-bff01ee031f2)
 Call ID: e069befe-b232-4a7d-bbbc-bff01ee031f2
  Args:
    type: :Person
    source: :Princess_Elizabeth_of_Greece_and_Denmark
  AddTriple (2d40f8cb-79e1-41e8-a73b-777abba495b8)
 Call ID: 2d40f8cb-79e1-41e8-a73b-777abba495b8
  Args:
    relation: :hasSister
    target: :Princess_Elizabeth_of_Greece_and_Denmark
    source: :Princess_Olga_of_Greece_and_Denmark
  AssignClass (18259968-d782-4b31-a2ba-dc8f37cc3fab)
 Call ID: 18259968-d782-4b31-a2ba-dc8f37cc3fab
  Args:
    source: :Princess_Marina_of_Greece_and_Denmark
    type: :Woman
  AssignClass (be4bc635-02db-45d6-88dd-38588f547abc)
 Call ID: be4bc635-02db-45d6-88dd-38588f547abc
  Args:
    source: :Princess_Marina_of_Greece_and_Denmark
    type: :Person
  AddTriple (f932c2f5-f712-42d8-af59-26c5ed41eae5)
 Call ID: f932c2f5-f712-42d8-af59-26c5ed41eae5
  Args:
    source: :Princess_Olga_of_Greece_and_Denmark
    target: :Princess_Marina_of_Greece_and_Denmark
    relation: :hasSister
  AssignClass (9ac7b9da-9fca-4f2d-9099-586f8c06a177)
 Call ID: 9ac7b9da-9fca-4f2d-9099-586f8c06a177
  Args:
    type: :Man
    source: :Prince_Alexander_of_Yugoslavia
  AssignClass (508233cb-0b50-47b4-805e-08706dc83c0d)
 Call ID: 508233cb-0b50-47b4-805e-08706dc83c0d
  Args:
    type: :Person
    source: :Prince_Alexander_of_Yugoslavia
  AddTriple (fe6eecf1-0942-4a36-a137-d84f240868da)
 Call ID: fe6eecf1-0942-4a36-a137-d84f240868da
  Args:
    relation: :hasSon
    target: :Prince_Alexander_of_Yugoslavia
    source: :Princess_Olga_of_Greece_and_Denmark
  AddTriple (673449dd-62ca-471c-9b88-97c708995603)
 Call ID: 673449dd-62ca-471c-9b88-97c708995603
  Args:
    source: :Prince_Alexander_of_Yugoslavia
    target: :Prince_Paul_of_Yugoslavia
    relation: :hasFather
  AssignClass (5c8d81ae-0c4f-4b5e-bf59-03253f52094a)
 Call ID: 5c8d81ae-0c4f-4b5e-bf59-03253f52094a
  Args:
    type: :Man
    source: :Prince_Nikola_of_Yugoslavia
  AssignClass (6e29bc51-6579-463a-8806-274d72b88ba2)
 Call ID: 6e29bc51-6579-463a-8806-274d72b88ba2
  Args:
    type: :Person
    source: :Prince_Nikola_of_Yugoslavia
  AddTriple (cf01269f-1677-4175-b954-a54fd40336e1)
 Call ID: cf01269f-1677-4175-b954-a54fd40336e1
  Args:
    source: :Princess_Olga_of_Greece_and_Denmark
    target: :Prince_Nikola_of_Yugoslavia
    relation: :hasSon
  AddTriple (4fcb26a0-7337-438f-bfea-f8f51bef7eb1)
 Call ID: 4fcb26a0-7337-438f-bfea-f8f51bef7eb1
  Args:
    relation: :hasFather
    target: :Prince_Paul_of_Yugoslavia
    source: :Prince_Nikola_of_Yugoslavia
  AssignClass (b0eb8010-f97b-4452-86e2-5dbbc0881692)
 Call ID: b0eb8010-f97b-4452-86e2-5dbbc0881692
  Args:
    source: :Princess_Elizabeth_of_Yugoslavia
    type: :Woman
  AssignClass (b21c643b-0982-4006-82db-2f92f3a51b40)
 Call ID: b21c643b-0982-4006-82db-2f92f3a51b40
  Args:
    type: :Person
    source: :Princess_Elizabeth_of_Yugoslavia
  AddTriple (c9cfdcd9-ad33-4f23-82c8-360d1aacd817)
 Call ID: c9cfdcd9-ad33-4f23-82c8-360d1aacd817
  Args:
    source: :Princess_Olga_of_Greece_and_Denmark
    target: :Princess_Elizabeth_of_Yugoslavia
    relation: :hasDaughter
  AddTriple (29b6daa5-b4fb-477a-b5c3-7755a0c16ff8)
 Call ID: 29b6daa5-b4fb-477a-b5c3-7755a0c16ff8
  Args:
    source: :Princess_Elizabeth_of_Yugoslavia
    target: :Prince_Paul_of_Yugoslavia
    relation: :hasFather
  Finish (55dacb62-9993-41ec-900f-13fd2fc61bad)
 Call ID: 55dacb62-9993-41ec-900f-13fd2fc61bad
  Args: