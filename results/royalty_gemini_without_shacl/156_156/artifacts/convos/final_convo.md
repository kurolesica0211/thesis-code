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
With him, she made several official stays abroad and notably met the dictators Benito Mussolini and Adolf Hitler in Rome and Berlin in April and June 1939, respectively.
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

:hasDeathYear a owl:AnnotationProperty .

:hasMarriageYear a owl:AnnotationProperty .

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

:hasChild a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:inverseOf :isChildOf .

:isAncestorOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation .

:isSiblingOf a owl:ObjectProperty,
        owl:SymmetricProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isBloodrelationOf ;
    owl:propertyChainAxiom ( :hasParent :isParentOf ) .

:isSisterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf .

:hasParent a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Person ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:equivalentProperty :isChildOf ;
    owl:inverseOf :isParentOf .

:Sex a owl:Class ;
    rdfs:subClassOf :DomainEntity ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Female :Male ) ] .

:isChildOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:propertyDisjointWith :isSisterOf .

:Man a owl:Class ;
    owl:disjointWith :Sex,
        :Woman ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Male ] ) ] .

:Woman a owl:Class ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Female ] ) ] .

:isParentOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:propertyDisjointWith :isSisterOf .

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



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (db76d9b8-b194-4909-9937-36a2973b07f8)
 Call ID: db76d9b8-b194-4909-9937-36a2973b07f8
  Args:
    type: :Woman
    source: Olga_of_Greece_and_Denmark
  AssignClass (62ed33d0-5db6-4bdb-9068-e78c16c21b8d)
 Call ID: 62ed33d0-5db6-4bdb-9068-e78c16c21b8d
  Args:
    type: :Person
    source: Olga_of_Greece_and_Denmark
  AddLiteral (4c10a4e4-1dba-4980-9b7f-fd654c3334aa)
 Call ID: 4c10a4e4-1dba-4980-9b7f-fd654c3334aa
  Args:
    source: Olga_of_Greece_and_Denmark
    literal_type: xsd:integer
    literal_value: 1903
    relation: :hasBirthYear
  AddLiteral (2a689b15-788a-4d1b-93a9-47091d7bfe28)
 Call ID: 2a689b15-788a-4d1b-93a9-47091d7bfe28
  Args:
    source: Olga_of_Greece_and_Denmark
    literal_type: xsd:integer
    literal_value: 1997
    relation: :hasDeathYear
  AddLiteral (01073b12-a11f-4d59-b83e-264e91a1a85a)
 Call ID: 01073b12-a11f-4d59-b83e-264e91a1a85a
  Args:
    source: Olga_of_Greece_and_Denmark
    literal_value: Princess Paul of Yugoslavia
    literal_type: xsd:string
    relation: :alsoKnownAs
  AssignClass (7bbf9cac-bba7-494c-91f1-7a20be7a9043)
 Call ID: 7bbf9cac-bba7-494c-91f1-7a20be7a9043
  Args:
    source: Prince_Paul_of_Yugoslavia
    type: :Man
  AssignClass (b6e3e1e3-2914-4ddf-a303-49b1b7615fad)
 Call ID: b6e3e1e3-2914-4ddf-a303-49b1b7615fad
  Args:
    source: Prince_Paul_of_Yugoslavia
    type: :Person
  AddLiteral (3690e1cb-4ebd-4699-8f26-1d53179605fc)
 Call ID: 3690e1cb-4ebd-4699-8f26-1d53179605fc
  Args:
    literal_type: xsd:integer
    literal_value: 1923
    relation: :hasMarriageYear
    source: Olga_of_Greece_and_Denmark
  AddTriple (32f468bb-8c0f-4a93-add5-3c01cedc22c3)
 Call ID: 32f468bb-8c0f-4a93-add5-3c01cedc22c3
  Args:
    source: Olga_of_Greece_and_Denmark
    relation: :hasRelation
    target: Prince_Paul_of_Yugoslavia
  AssignClass (e71e2d0c-45c2-4d3e-891c-82842b501670)
 Call ID: e71e2d0c-45c2-4d3e-891c-82842b501670
  Args:
    source: Prince_Nicholas_of_Greece_and_Denmark
    type: :Man
  AssignClass (ee644464-9f92-4720-b570-e02765e967c6)
 Call ID: ee644464-9f92-4720-b570-e02765e967c6
  Args:
    type: :Ancestor
    source: Prince_Nicholas_of_Greece_and_Denmark
  AssignClass (7dcfc9c0-8d19-4b7c-b9e7-9c73b5cf449e)
 Call ID: 7dcfc9c0-8d19-4b7c-b9e7-9c73b5cf449e
  Args:
    type: :Woman
    source: Grand_Duchess_Elena_Vladimirovna_of_Russia
  AssignClass (3ccc691a-3ddc-417c-8c87-694c963b57e9)
 Call ID: 3ccc691a-3ddc-417c-8c87-694c963b57e9
  Args:
    type: :Ancestor
    source: Grand_Duchess_Elena_Vladimirovna_of_Russia
  AddTriple (82ef3af6-cff2-4920-af9a-fa0f6f331011)
 Call ID: 82ef3af6-cff2-4920-af9a-fa0f6f331011
  Args:
    source: Olga_of_Greece_and_Denmark
    relation: :hasFather
    target: Prince_Nicholas_of_Greece_and_Denmark
  AddTriple (29556f9c-b954-4b9e-9297-2350d2adc8d8)
 Call ID: 29556f9c-b954-4b9e-9297-2350d2adc8d8
  Args:
    source: Olga_of_Greece_and_Denmark
    target: Grand_Duchess_Elena_Vladimirovna_of_Russia
    relation: :hasMother
  AssignClass (f7f83688-1542-4da7-982f-ce1543f269da)
 Call ID: f7f83688-1542-4da7-982f-ce1543f269da
  Args:
    type: :Man
    source: King_George_I_of_Greece
  AssignClass (b54bc26c-e124-4f5b-b311-2455eedbec4a)
 Call ID: b54bc26c-e124-4f5b-b311-2455eedbec4a
  Args:
    type: :Ancestor
    source: King_George_I_of_Greece
  AddTriple (4f16785b-99f8-4a4b-a1ec-59c0155e6c3f)
 Call ID: 4f16785b-99f8-4a4b-a1ec-59c0155e6c3f
  Args:
    source: Olga_of_Greece_and_Denmark
    relation: :hasAncestor
    target: King_George_I_of_Greece
  AssignClass (00a65810-9f3d-4921-9648-960fb8b0bb60)
 Call ID: 00a65810-9f3d-4921-9648-960fb8b0bb60
  Args:
    type: :Woman
    source: Princess_Elizabeth_of_Greece_and_Denmark
  AssignClass (e083f936-3d60-4d87-ba04-e485e79d4f98)
 Call ID: e083f936-3d60-4d87-ba04-e485e79d4f98
  Args:
    type: :Person
    source: Princess_Elizabeth_of_Greece_and_Denmark
  AssignClass (1b5ca4b2-90ee-44e9-bed9-cd4398f6997c)
 Call ID: 1b5ca4b2-90ee-44e9-bed9-cd4398f6997c
  Args:
    source: Princess_Marina_of_Greece_and_Denmark
    type: :Woman
  AssignClass (792041f3-c9f2-44cd-9251-26c5a9f35f55)
 Call ID: 792041f3-c9f2-44cd-9251-26c5a9f35f55
  Args:
    type: :Person
    source: Princess_Marina_of_Greece_and_Denmark
  AddTriple (ee3dc5b0-a9e5-4071-93be-b672096620d7)
 Call ID: ee3dc5b0-a9e5-4071-93be-b672096620d7
  Args:
    target: Princess_Elizabeth_of_Greece_and_Denmark
    relation: :hasSister
    source: Olga_of_Greece_and_Denmark
  AddTriple (026a4a17-f44b-4464-94af-0051ba30e132)
 Call ID: 026a4a17-f44b-4464-94af-0051ba30e132
  Args:
    source: Olga_of_Greece_and_Denmark
    relation: :hasSister
    target: Princess_Marina_of_Greece_and_Denmark
  AssignClass (05d14244-6fe0-4741-b499-6612ffa1bbc4)
 Call ID: 05d14244-6fe0-4741-b499-6612ffa1bbc4
  Args:
    type: :Man
    source: Prince_Alexander_of_Yugoslavia
  AssignClass (0390b700-6958-471e-9d67-6d32b3efd2b3)
 Call ID: 0390b700-6958-471e-9d67-6d32b3efd2b3
  Args:
    type: :Person
    source: Prince_Alexander_of_Yugoslavia
  AssignClass (31d8242a-8101-4de6-82a2-a49b7e39fec3)
 Call ID: 31d8242a-8101-4de6-82a2-a49b7e39fec3
  Args:
    type: :Man
    source: Prince_Nikola_of_Yugoslavia
  AssignClass (192ec64e-c11b-4f55-a33c-73c2e81f7bc6)
 Call ID: 192ec64e-c11b-4f55-a33c-73c2e81f7bc6
  Args:
    type: :Person
    source: Prince_Nikola_of_Yugoslavia
  AssignClass (49b51191-963d-4777-ad22-067049afb7f2)
 Call ID: 49b51191-963d-4777-ad22-067049afb7f2
  Args:
    source: Princess_Elizabeth_of_Yugoslavia
    type: :Woman
  AssignClass (af9af08e-c774-45e5-b5b5-0d7a7a2d16aa)
 Call ID: af9af08e-c774-45e5-b5b5-0d7a7a2d16aa
  Args:
    type: :Person
    source: Princess_Elizabeth_of_Yugoslavia
  AddTriple (5d24f49e-2d9b-4ed2-ae74-8621fc24c61f)
 Call ID: 5d24f49e-2d9b-4ed2-ae74-8621fc24c61f
  Args:
    source: Olga_of_Greece_and_Denmark
    target: Prince_Alexander_of_Yugoslavia
    relation: :hasSon
  AddTriple (8c25a849-bc37-41d6-b1a1-b945332b090d)
 Call ID: 8c25a849-bc37-41d6-b1a1-b945332b090d
  Args:
    target: Prince_Nikola_of_Yugoslavia
    relation: :hasSon
    source: Olga_of_Greece_and_Denmark
  AddTriple (f7ee0a03-c3f9-483f-86f8-1cdf7afe0433)
 Call ID: f7ee0a03-c3f9-483f-86f8-1cdf7afe0433
  Args:
    target: Princess_Elizabeth_of_Yugoslavia
    relation: :hasDaughter
    source: Olga_of_Greece_and_Denmark
  Finish (922bda26-94f4-4d99-b5c3-a5914dfb7fde)
 Call ID: 922bda26-94f4-4d99-b5c3-a5914dfb7fde
  Args: