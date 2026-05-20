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
Frederica of Hanover (German: Friederike Luise;
Greek: Φρειδερίκη Λουΐζα, romanized: Phreideríkē Louḯza; 18 April 1917 – 6 February 1981) was Queen of Greece from 1 April 1947 until 6 March 1964 as the wife of King Paul and Queen Mother of Greece from 6 March 1964, when her son Constantine II became King, until 8 December 1974, when the monarchy was officially abolished after a referendum.
Granddaughter of Kaiser Wilhelm II and daughter of Duke Ernest Augustus of Brunswick, Frederica was born a few months before the fall of the German Empire.
In Florence, she was received by Princess Helen of Greece and Denmark, at whose house she met the Crown Prince of Greece, Paul.
The two fell in love and married two years after the restoration of the monarchy in Greece.
In the years that followed, she gave birth to three children, Sophia in 1938, Constantine in 1940 and Irene in 1942.
During the Second World War, Greece was occupied by the Axis powers.
The Greek royal family left the country and Frederica and her children settled first in South Africa and from 1943 in Egypt.
The changing political situation in Greece, with the rise of the EAM and the KKE, challenged the institution of the monarchy.
In the period of civil war that followed, Frederica developed a strong social activity to support the efforts of the government and the Crown.
However, according to the prevailing historiographical view, she continued to influence the fate of the country through her son, now King Constantine II.
Frederica was widely regarded as Constantine's éminence grise and continued to be attacked by the opposition, who blamed her for the tensions between the palace and the government of Georgios Papandreou (1964–1965).
Early life

Born Her Royal Highness Friederike Luise, Princess of Hanover, Princess of Great Britain and Ireland, and Princess of Brunswick-Lüneburg on 18 April 1917 in Blankenburg am Harz, in the German Duchy of Brunswick, she was the only daughter and third child of Ernest Augustus, then reigning Duke of Brunswick, and his wife Princess Viktoria Luise of Prussia, herself the only daughter of the German Emperor Wilhelm II.
In 1933 Frederica joined the Jungmädelbund, the Nazi organisation for girls aged 10–14.
In 1934, Adolf Hitler, in his ambition to link the British and German royal houses, asked for Frederica's parents to arrange for the marriage of their seventeen-year-old daughter to the Prince of Wales.
In her memoirs, Frederica's mother described that she and her husband were "shattered" and such a possibility "had never entered our minds".
Moreover, the age difference was too great (the Prince of Wales was twenty-three years Frederica's senior), and her parents were unwilling to "put any such pressure" on their daughter.
Marriage

Prince Paul of Greece proposed to her during the summer of 1936, while he was in Berlin attending the 1936 Summer Olympics.
Paul was a son of King Constantine I and Frederica's great aunt Sophia.
They were also paternal second cousins as great-grandchildren of Christian IX of Denmark.
Frederica became Hereditary Princess of Greece, her husband being heir presumptive to his childless elder brother, King George II.
Ten months after their marriage, their first child, the future Queen Sofía of Spain (and future mother of Felipe VI), was born on 2 November 1938.
On 2 June 1940, Frederica gave birth to the future King Constantine II.
Frederica and her family were evacuated again, setting up a government-in-exile office in London.
Here Frederica's last child, Princess Irene, was born on 11 May 1942.
The Hereditary Prince and Princess returned to their villa in Psychiko.
Queen consort

On 1 April 1947, George II died and Frederica's husband ascended the throne as Paul I, with Frederica as queen consort.
A Communist insurgency in Northern Greece led to the Greek Civil War.
The King and Queen toured Northern Greece under tight security to appeal for loyalty in the summer of 1947.
Queen Frederica was constantly attacked for her German ancestry.
Left-wing politicians in Greece repeatedly used the fact that the Kaiser was her grandfather, and that she had brothers who were members of the SS, as propaganda against her.
When she was in London representing her sick husband at the wedding of his first cousin Prince Philip of Greece and Denmark to King George VI's elder daughter Princess Elizabeth in November 1947, Winston Churchill remarked on the Kaiser being her grandfather.
Queen Frederica had replied acknowledging the fact, but reminding him that she was also descended from Queen Victoria, and that her father would be the British king if the country had operated under Salic Law (allowing only males to inherit the crown).
In fact, Frederica held the title Princess of the United Kingdom of Great Britain and Ireland, granted ad personam to the children of the then-Duke of Brunswick by George V's letters patent of 1914, which remained unrevoked.
During the civil war, Queen Frederica set up the Queen's Camps or Child Cities (translation of: Παιδο(υ)πόλεις / Paidopoleis or Paidupoleis), a network of 53 camps around Greece where she would rescue children of members of the Democratic Army and former partisans.
The Greek Civil War ended in August 1949.
The King and Queen took this opportunity to strengthen the monarchy, and paid official visits to Marshal Josip Broz Tito in Belgrade, Presidents Luigi Einaudi of Italy in Rome, Theodor Heuss of West Germany, and Bechara El Khoury of Lebanon, Emperor Haile Selassie I of Ethiopia, Governor-General Chakravarthi Rajagopalachari of India, King George VI of the United Kingdom, and the United States as guest of President Dwight D. Eisenhower.
However, at home in Greece and abroad in the United Kingdom, Queen Frederica was targeted by the opposition, because as a girl she had belonged to the Bund Deutscher Mädel (League of German Girls), a branch of the Hitler Youth group for young women; her supporters argued that evading membership in the group would be difficult under the existing political climate in Nazi Germany at the time.
Unlike her meek husband, in post-War Greece Frederica was one of the most hated public figures.
Frederica has been described as "inherently undemocratic".
At home in Greece and abroad in the United Kingdom, she was targeted by the opposition.
Frederica's 16 November 1953 appearance in Life as America's guest was taken on one of the many state visits she paid around the world.
On 14 May 1962, her eldest daughter Sofía married Prince Juan Carlos of Spain (later King Juan Carlos I of Spain) in Athens.
Queen dowager

On 6 March 1964, King Paul died of cancer.
When her son, King Constantine II, married Princess Anne-Marie of Denmark later that year on 18 September, Queen Frederica stepped back from the majority of her public duties in favor of her daughter-in-law.
However, she continued to attend royal events that were family-oriented, such as the baptisms of her grandchildren in both Spain and Greece.
Exile

 King Constantine II's clashes with the democratically elected Prime Minister George Papandreou Sr. were blamed by critics for causing the destabilisation that led to a military coup on 21 April 1967 and the rise of the regime of the colonels.
Faced with a difficult situation, King Constantine initially collaborated with the military dictatorship,  swearing in their government under a royalist prime minister.
In 1971, Frederica published an autobiography, A Measure of Understanding.
The head of the junta became the new head-of-state as President of Greece George Papadopoulos.
A plebiscite was held on 8 December 1974 in which Constantine (who was able to campaign only from outside the country) freely admitted past errors, and promised to support democracy.
However, 69% of Greeks freely voted to make Greece a democratic republic.
Death

Frederica died on 6 February 1981 in exile in Madrid of heart failure, reportedly following eyelid surgery (blepharoplasty), although a biographer has claimed the surgery was cataract removal.
She was interred at Tatoi (the royal family's palace and burial ground in Greece).



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
  AssignClass (ffdd9b7b-e37b-472f-9c65-e66a84331dbd)
 Call ID: ffdd9b7b-e37b-472f-9c65-e66a84331dbd
  Args:
    type: :Woman
    source: Frederica_of_Hanover
  AssignClass (846eb72a-c675-4a04-af62-03e030200268)
 Call ID: 846eb72a-c675-4a04-af62-03e030200268
  Args:
    type: :Person
    source: Frederica_of_Hanover
  AssignClass (361a2cb8-b930-41c5-917b-c407f46e2b89)
 Call ID: 361a2cb8-b930-41c5-917b-c407f46e2b89
  Args:
    source: Frederica_of_Hanover
    type: :Ancestor
  AddLiteral (0c9b0535-f81c-4d45-8096-4e09c40f0adf)
 Call ID: 0c9b0535-f81c-4d45-8096-4e09c40f0adf
  Args:
    relation: :hasBirthYear
    source: Frederica_of_Hanover
    literal_type: xsd:integer
    literal_value: 1917
  AddLiteral (0629b200-bb49-4f9c-b486-ff4a0243b9b6)
 Call ID: 0629b200-bb49-4f9c-b486-ff4a0243b9b6
  Args:
    relation: :hasDeathYear
    source: Frederica_of_Hanover
    literal_type: xsd:integer
    literal_value: 1981
  AssignClass (fcdf3e03-94e9-400b-8278-ec32d5d810b4)
 Call ID: fcdf3e03-94e9-400b-8278-ec32d5d810b4
  Args:
    type: :Man
    source: Paul_I_of_Greece
  AssignClass (d8d65cd3-389d-4b32-8770-c3e67b3052ee)
 Call ID: d8d65cd3-389d-4b32-8770-c3e67b3052ee
  Args:
    type: :Person
    source: Paul_I_of_Greece
  AssignClass (a616f6d0-342a-4b1c-a7e1-aea1424edf87)
 Call ID: a616f6d0-342a-4b1c-a7e1-aea1424edf87
  Args:
    source: Paul_I_of_Greece
    type: :Ancestor
  AssignClass (be32a8b9-229f-4000-a525-beb086fe246c)
 Call ID: be32a8b9-229f-4000-a525-beb086fe246c
  Args:
    type: :Man
    source: Ernest_Augustus_of_Brunswick
  AssignClass (4fca138e-5578-49db-b4d8-d896042dfe77)
 Call ID: 4fca138e-5578-49db-b4d8-d896042dfe77
  Args:
    type: :Person
    source: Ernest_Augustus_of_Brunswick
  AssignClass (cca39b57-6be7-41bb-9ef4-0678361822d3)
 Call ID: cca39b57-6be7-41bb-9ef4-0678361822d3
  Args:
    source: Ernest_Augustus_of_Brunswick
    type: :Ancestor
  AssignClass (7ab517a7-c283-4ba0-8c90-291c23d27b77)
 Call ID: 7ab517a7-c283-4ba0-8c90-291c23d27b77
  Args:
    source: Viktoria_Luise_of_Prussia
    type: :Woman
  AssignClass (216d8632-08c7-4e24-bee8-984e4b859290)
 Call ID: 216d8632-08c7-4e24-bee8-984e4b859290
  Args:
    type: :Person
    source: Viktoria_Luise_of_Prussia
  AssignClass (e9bde997-63f0-40fb-a1dd-765da0e9c3bc)
 Call ID: e9bde997-63f0-40fb-a1dd-765da0e9c3bc
  Args:
    type: :Ancestor
    source: Viktoria_Luise_of_Prussia
  AssignClass (abbb6474-7a6f-4798-ae93-c37899cbff30)
 Call ID: abbb6474-7a6f-4798-ae93-c37899cbff30
  Args:
    source: Wilhelm_II
    type: :Man
  AssignClass (576a5a41-9810-4769-b49b-20446753a070)
 Call ID: 576a5a41-9810-4769-b49b-20446753a070
  Args:
    type: :Person
    source: Wilhelm_II
  AssignClass (92a1567f-f1b4-44f0-b1bb-0fadba6be4e9)
 Call ID: 92a1567f-f1b4-44f0-b1bb-0fadba6be4e9
  Args:
    source: Wilhelm_II
    type: :Ancestor
  AssignClass (7dc7f21e-c433-48a8-b496-afd6cf21c500)
 Call ID: 7dc7f21e-c433-48a8-b496-afd6cf21c500
  Args:
    type: :Man
    source: Constantine_I_of_Greece
  AssignClass (29e058b8-4dab-442f-8e5e-22cdbf9b4dec)
 Call ID: 29e058b8-4dab-442f-8e5e-22cdbf9b4dec
  Args:
    type: :Person
    source: Constantine_I_of_Greece
  AssignClass (6cffa634-2cc7-4f2f-b0c3-4c203bc78c01)
 Call ID: 6cffa634-2cc7-4f2f-b0c3-4c203bc78c01
  Args:
    source: Constantine_I_of_Greece
    type: :Ancestor
  AssignClass (ed9009c1-1ef9-45aa-ae87-a781c525f83c)
 Call ID: ed9009c1-1ef9-45aa-ae87-a781c525f83c
  Args:
    type: :Woman
    source: Sophia_of_Prussia
  AssignClass (5c535b4a-da6a-4be7-80f3-078b188e78e3)
 Call ID: 5c535b4a-da6a-4be7-80f3-078b188e78e3
  Args:
    source: Sophia_of_Prussia
    type: :Person
  AssignClass (4db4f13c-4c67-41af-967b-cafa40fa722b)
 Call ID: 4db4f13c-4c67-41af-967b-cafa40fa722b
  Args:
    type: :Ancestor
    source: Sophia_of_Prussia
  AssignClass (15f9dea1-2c9f-434f-a062-6466c5e9d965)
 Call ID: 15f9dea1-2c9f-434f-a062-6466c5e9d965
  Args:
    type: :Woman
    source: Sophia_of_Greece
  AssignClass (f2f8c6b7-6995-410b-a645-cfa241cdb971)
 Call ID: f2f8c6b7-6995-410b-a645-cfa241cdb971
  Args:
    source: Sophia_of_Greece
    type: :Person
  AssignClass (dafbfbec-977a-49b2-a1d0-a0b76ee2cb4a)
 Call ID: dafbfbec-977a-49b2-a1d0-a0b76ee2cb4a
  Args:
    type: :Ancestor
    source: Sophia_of_Greece
  AssignClass (4d1b54d4-25fd-4683-ad2f-fdfc9d9d279a)
 Call ID: 4d1b54d4-25fd-4683-ad2f-fdfc9d9d279a
  Args:
    type: :Man
    source: Constantine_II_of_Greece
  AssignClass (a6d4da6c-b9cf-4659-a035-eb3a8327d8fe)
 Call ID: a6d4da6c-b9cf-4659-a035-eb3a8327d8fe
  Args:
    type: :Person
    source: Constantine_II_of_Greece
  AssignClass (0326b097-0d35-4e31-9e53-5a03661e7bc8)
 Call ID: 0326b097-0d35-4e31-9e53-5a03661e7bc8
  Args:
    type: :Ancestor
    source: Constantine_II_of_Greece
  AssignClass (7fdc9e22-1b44-4b94-af3e-ad1407580beb)
 Call ID: 7fdc9e22-1b44-4b94-af3e-ad1407580beb
  Args:
    type: :Woman
    source: Irene_of_Greece
  AssignClass (423ce31e-2645-4214-b677-c7c65d24b3fb)
 Call ID: 423ce31e-2645-4214-b677-c7c65d24b3fb
  Args:
    type: :Person
    source: Irene_of_Greece
  AddTriple (841550e4-8992-4837-bd88-97540e5630ac)
 Call ID: 841550e4-8992-4837-bd88-97540e5630ac
  Args:
    target: Ernest_Augustus_of_Brunswick
    relation: :hasFather
    source: Frederica_of_Hanover
  AddTriple (b5e18172-e012-45d0-b2fe-c541033da22a)
 Call ID: b5e18172-e012-45d0-b2fe-c541033da22a
  Args:
    target: Viktoria_Luise_of_Prussia
    relation: :hasMother
    source: Frederica_of_Hanover
  AddTriple (d31d5d9e-3ce1-46d1-8e5f-02bbc515e604)
 Call ID: d31d5d9e-3ce1-46d1-8e5f-02bbc515e604
  Args:
    target: Wilhelm_II
    relation: :hasFather
    source: Viktoria_Luise_of_Prussia
  AddTriple (522e774b-7753-4aa2-80e2-4d734bc2f04d)
 Call ID: 522e774b-7753-4aa2-80e2-4d734bc2f04d
  Args:
    source: Paul_I_of_Greece
    relation: :hasFather
    target: Constantine_I_of_Greece
  AddTriple (0ec06c8a-a908-4d4f-b304-6df4b35b3a20)
 Call ID: 0ec06c8a-a908-4d4f-b304-6df4b35b3a20
  Args:
    target: Sophia_of_Prussia
    relation: :hasMother
    source: Paul_I_of_Greece
  AddTriple (2cdb32b0-6bc7-41bc-9486-98d3c0c70800)
 Call ID: 2cdb32b0-6bc7-41bc-9486-98d3c0c70800
  Args:
    source: Frederica_of_Hanover
    relation: :hasMother
    target: Sophia_of_Prussia
  AddTriple (6f029c71-2e2f-4e58-8f39-a59c15261bbb)
 Call ID: 6f029c71-2e2f-4e58-8f39-a59c15261bbb
  Args:
    source: Sophia_of_Greece
    target: Frederica_of_Hanover
    relation: :hasMother
  AddTriple (48a513e3-b75e-47f7-89e0-e67c8458d637)
 Call ID: 48a513e3-b75e-47f7-89e0-e67c8458d637
  Args:
    target: Paul_I_of_Greece
    relation: :hasFather
    source: Sophia_of_Greece
  AddTriple (86dd4b85-4a25-476d-be80-a14867ccad07)
 Call ID: 86dd4b85-4a25-476d-be80-a14867ccad07
  Args:
    relation: :hasMother
    target: Frederica_of_Hanover
    source: Constantine_II_of_Greece
  AddTriple (189c0286-1b22-42ae-893b-af5c2f4bb487)
 Call ID: 189c0286-1b22-42ae-893b-af5c2f4bb487
  Args:
    relation: :hasFather
    target: Paul_I_of_Greece
    source: Constantine_II_of_Greece
  AddTriple (cf0b2bcc-e4ff-48ba-90fc-d1b8a689c6fe)
 Call ID: cf0b2bcc-e4ff-48ba-90fc-d1b8a689c6fe
  Args:
    source: Irene_of_Greece
    target: Frederica_of_Hanover
    relation: :hasMother
  AddTriple (515e88d9-d406-49ca-9c37-322e615bd4f1)
 Call ID: 515e88d9-d406-49ca-9c37-322e615bd4f1
  Args:
    target: Paul_I_of_Greece
    relation: :hasFather
    source: Irene_of_Greece
  AddLiteral (35516d86-ab8d-4498-9808-089fb69e4d3e)
 Call ID: 35516d86-ab8d-4498-9808-089fb69e4d3e
  Args:
    literal_type: xsd:string
    literal_value: Friederike Luise
    relation: :knownAs
    source: Frederica_of_Hanover
  Finish (246ca35a-0e94-4419-86cb-aaf5708ae88d)
 Call ID: 246ca35a-0e94-4419-86cb-aaf5708ae88d
  Args: