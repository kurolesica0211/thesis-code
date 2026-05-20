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
Prince Joachim Franz Humbert of Prussia (17 December 1890 – 18 July 1920) was the youngest son and sixth child of Wilhelm II, German Emperor, by his first wife, Augusta Victoria of Schleswig-Holstein.
Prince Joachim was educated as an officer and participated in the First World War.
Early life

Birth and family

Prince Joachim was born on 17 December 1890, two years after his father had become the German Emperor, at the Berlin Palace in central Berlin.
He was the sixth and youngest son of Emperor Wilhelm II, and his first wife, Princess Augusta Victoria of Schleswig-Holstein.
Education

Prince Joachim spent his childhood with his siblings at the New Palace in Potsdam, and his school days at the Prinzenhaus in Plön, in his mother's ancestral Schleswig-Holstein, as his brothers had been before him.
Marriage

On 11 March 1916 in Berlin, Joachim married Princess Marie-Auguste of Anhalt (10 June 1898 – 22 May 1983), the daughter of Eduard, Duke of Anhalt and his wife Princess Luise of Saxe-Altenburg (daughter of Prince Moritz of Saxe-Altenburg).
He and Marie-Auguste had been engaged since 14 October of the previous year.
The wedding was celebrated at Bellevue Palace, and was attended by Joachim's father and mother, the Duke and Duchess of Anhalt, as well as other relatives.
The couple had one son, Prince Karl Franz Josef Wilhelm Friedrich Eduard Paul (15 December 1916 in Potsdam – 22 January 1975 in Arica, Chile).
Their grandson, Prince Franz Wilhelm, married Maria Vladimirovna of Russia, a claimant to the Imperial Russian throne.
Candidate for thrones

Ireland

During the Easter Rising in Dublin in 1916, some republican leaders, including Patrick Pearse and Joseph Plunkett, contemplated giving the throne of an independent Ireland to Prince Joachim.
Pearse and Plunkett thought that if the rising were successful and Germany won the First World War, an independent Ireland would be a monarchy with a German prince as king, like Romania and Bulgaria before it.
The fact that Joachim did not speak English was also considered an advantage, as he might be more disposed to learning and promoting the use of the Irish language.
He would naturally turn to those who were more Irish and Gaelic, as to his friends, for the non-nationalist element in our country had shown themselves to be so bitterly anti-German.
For the first generation or so it would be an advantage, in view of our natural weakness, to have a ruler who linked us with a dominant European power, and thereafter, when we were better prepared to stand alone, or when it might be undesirable that our ruler should turn by personal choice to one power rather than be guided by what was most natural and beneficial for our country, the ruler of that time would have become completely Irish."

Ernest Blythe recalled that in January 1915 he heard Plunkett and Thomas MacDonagh express support for the idea at an Irish Volunteers meeting.
Georgia

After Georgia's declaration of independence following the Russian Revolution of 1917, Joachim was briefly considered by the German representative Count Friedrich Werner von der Schulenburg and Georgian royalists as a candidate for the Georgian throne.
The Germans presented various proposals to incorporate Lithuania into the German Empire, particularly Prussia.
One such proposal offered the crown of Lithuania to Joachim.
On 4 June 1918, they voted to offer the Lithuanian throne to the German noble Wilhelm Karl, Duke of Urach.
Divorce and death

Following the German Revolution in November 1918, the Emperor was forced to abdicate, thus depriving Joachim of his titles, position and prospects for heading any newly established monarchies in Europe.
On 31 May 1918, Joachim was examined by the psychiatrist Robert Gaupp, who submitted a report concluding that he "was incurably ill, both mentally and physically ... was extremely easily emotionally and sexually aroused", and "was inclined to 'violent, uncontrollably exploding outbursts of anger in which all self-control  lost'".
The relationship between Joachim and his wife had already started to deteriorate.
According to one report, Marie-Auguste had previously abandoned her husband and child to run away with another man, had been forcibly brought back home on the orders of the Kaiser, but had filed for divorce as soon as the war ended, when she saw that her husband's family were at their lowest ebb.
According to Hans von Gontard, who served as the Kaiser's Hofmarschall in exile, Joachim was "quite out of control and had beaten his wife".
Following the divorce, Joachim shot himself in Potsdam on 18 July 1920.
His own brother Prince Eitel Friedrich of Prussia commented that he suffered from "a fit of excessive dementia".
Kaiser Wilhelm's reaction to the news of his son's suicide was one of fury, commenting that he was outraged "that the oaf should have done this, too, to us and especially to his mother!"
She desperately wanted to believe that his death had been accidental but she knew better.


Children and grandchildren

The only issue of the marriage of Prince Joachim and Princess Marie-Auguste was their son, Prince Karl Franz Josef Wilhelm Friedrich Eduard of Prussia (15 December 1916 – 22 January 1975).
On 5 October 1940, Prince Karl married Princess Henriette Hermine Wanda Ida Luise von Schönaich-Carolath (25 November 1918 –
They were the parents of three children:


After the divorce, Prince Karl married, morganatically, Luise Dora Hartmann (5 September 1909 – 23 April 1961) on 9 November 1946.
Prince Karl's last marriage was to Eva Maria Herrera y Valdeavellano (10 June 1922 – 6 March 1987) on 20 July 1959 in Lima, Peru.
They were married until Prince Karl's death and had two daughters;


Regimental Commissions

Honours

Prince Joachim received the following orders and decorations:
Ancestry

Portrayal in fiction

Prince Joachim was played by American actor Jesse Plemons and portrayed as the main antagonist in the 2021 Disney fantasy adventure film Jungle Cruise.



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
  AssignClass (f330354c-7293-4a4f-9c85-a6dbed0ec121)
 Call ID: f330354c-7293-4a4f-9c85-a6dbed0ec121
  Args:
    source: Prince_Joachim_of_Prussia
    type: :Man
  AssignClass (6b1e0986-97b4-4ffb-8722-369fadfb0c2a)
 Call ID: 6b1e0986-97b4-4ffb-8722-369fadfb0c2a
  Args:
    source: Prince_Joachim_of_Prussia
    type: :Person
  AssignClass (7fcc6cad-0553-4ce1-b1db-c3e513ceb606)
 Call ID: 7fcc6cad-0553-4ce1-b1db-c3e513ceb606
  Args:
    source: Wilhelm_II_German_Emperor
    type: :Man
  AssignClass (3759857f-bcd0-4edc-a495-d1aac844f60e)
 Call ID: 3759857f-bcd0-4edc-a495-d1aac844f60e
  Args:
    type: :Person
    source: Wilhelm_II_German_Emperor
  AssignClass (1e05306d-9ef6-45c5-98a9-396889fdf974)
 Call ID: 1e05306d-9ef6-45c5-98a9-396889fdf974
  Args:
    source: Augusta_Victoria_of_Schleswig-Holstein
    type: :Woman
  AssignClass (34940c84-821a-45ea-842d-d5cbc7e1bc5b)
 Call ID: 34940c84-821a-45ea-842d-d5cbc7e1bc5b
  Args:
    type: :Person
    source: Augusta_Victoria_of_Schleswig-Holstein
  AddLiteral (5f897a52-db18-40cf-88e5-040b8b7105cf)
 Call ID: 5f897a52-db18-40cf-88e5-040b8b7105cf
  Args:
    literal_type: xsd:integer
    source: Prince_Joachim_of_Prussia
    literal_value: 1890
    relation: :hasBirthYear
  AddLiteral (fcb21110-656d-4d18-838c-38bac3fa7c0d)
 Call ID: fcb21110-656d-4d18-838c-38bac3fa7c0d
  Args:
    relation: :hasDeathYear
    literal_value: 1920
    source: Prince_Joachim_of_Prussia
    literal_type: xsd:integer
  AddTriple (931a1c68-7573-4d6a-b5ec-bbbd59a8cdd1)
 Call ID: 931a1c68-7573-4d6a-b5ec-bbbd59a8cdd1
  Args:
    target: Wilhelm_II_German_Emperor
    source: Prince_Joachim_of_Prussia
    relation: :hasFather
  AddTriple (a83cd02f-97ba-462a-931d-ab60c4313de9)
 Call ID: a83cd02f-97ba-462a-931d-ab60c4313de9
  Args:
    relation: :hasMother
    source: Prince_Joachim_of_Prussia
    target: Augusta_Victoria_of_Schleswig-Holstein
  AssignClass (9ffe3da8-6e9c-4ea1-b733-e598fb57a119)
 Call ID: 9ffe3da8-6e9c-4ea1-b733-e598fb57a119
  Args:
    source: Marie-Auguste_of_Anhalt
    type: :Woman
  AssignClass (7b031648-e185-4d6c-8323-ba455e1e53f8)
 Call ID: 7b031648-e185-4d6c-8323-ba455e1e53f8
  Args:
    type: :Person
    source: Marie-Auguste_of_Anhalt
  AddLiteral (5872b973-a6af-4522-84f5-6b364b667e31)
 Call ID: 5872b973-a6af-4522-84f5-6b364b667e31
  Args:
    relation: :hasMarriageYear
    literal_value: 1916
    source: Prince_Joachim_of_Prussia
    literal_type: xsd:integer
  AddTriple (67ca5520-3b29-4d84-942a-a6e38ecf63ce)
 Call ID: 67ca5520-3b29-4d84-942a-a6e38ecf63ce
  Args:
    source: Prince_Joachim_of_Prussia
    target: Marie-Auguste_of_Anhalt
    relation: :hasRelation
  AssignClass (86af52b6-c694-4cd4-8ac2-b7ffc5dcc28c)
 Call ID: 86af52b6-c694-4cd4-8ac2-b7ffc5dcc28c
  Args:
    source: Eduard_Duke_of_Anhalt
    type: :Man
  AssignClass (766d0a34-b901-4b28-bfe2-90ed8d3a4db8)
 Call ID: 766d0a34-b901-4b28-bfe2-90ed8d3a4db8
  Args:
    type: :Person
    source: Eduard_Duke_of_Anhalt
  AssignClass (e4ce61a3-60d5-4a1b-910f-2b4eeb6f25b2)
 Call ID: e4ce61a3-60d5-4a1b-910f-2b4eeb6f25b2
  Args:
    source: Luise_of_Saxe-Altenburg
    type: :Woman
  AssignClass (3f7e38ba-9c93-4f07-8adf-5ba14ea30eb6)
 Call ID: 3f7e38ba-9c93-4f07-8adf-5ba14ea30eb6
  Args:
    type: :Person
    source: Luise_of_Saxe-Altenburg
  AddTriple (6a532850-81ca-420e-a199-96f273716930)
 Call ID: 6a532850-81ca-420e-a199-96f273716930
  Args:
    source: Marie-Auguste_of_Anhalt
    target: Eduard_Duke_of_Anhalt
    relation: :hasFather
  AddTriple (e2c1b668-9e4f-45a5-9eb6-6ed044b878ba)
 Call ID: e2c1b668-9e4f-45a5-9eb6-6ed044b878ba
  Args:
    relation: :hasMother
    source: Marie-Auguste_of_Anhalt
    target: Luise_of_Saxe-Altenburg
  AssignClass (bdd31e98-2850-4cd8-ac55-361565a262fe)
 Call ID: bdd31e98-2850-4cd8-ac55-361565a262fe
  Args:
    source: Moritz_of_Saxe-Altenburg
    type: :Man
  AssignClass (f199c4c2-0537-4d1a-b4e6-9b26c9e5031e)
 Call ID: f199c4c2-0537-4d1a-b4e6-9b26c9e5031e
  Args:
    type: :Person
    source: Moritz_of_Saxe-Altenburg
  AddTriple (080e8508-bd9f-4608-8b08-2f9c322b75d1)
 Call ID: 080e8508-bd9f-4608-8b08-2f9c322b75d1
  Args:
    relation: :hasFather
    target: Moritz_of_Saxe-Altenburg
    source: Luise_of_Saxe-Altenburg
  AssignClass (ed8ebfa3-a19e-41cb-a1fd-229b2473a6fe)
 Call ID: ed8ebfa3-a19e-41cb-a1fd-229b2473a6fe
  Args:
    source: Karl_Franz_Josef_Wilhelm_Friedrich_Eduard_Paul_of_Prussia
    type: :Man
  AssignClass (86bec0b6-f493-41a3-a8af-c2b2ac595239)
 Call ID: 86bec0b6-f493-41a3-a8af-c2b2ac595239
  Args:
    source: Karl_Franz_Josef_Wilhelm_Friedrich_Eduard_Paul_of_Prussia
    type: :Person
  AddTriple (38811e06-e468-4dc8-bc84-3bee9c2e04e7)
 Call ID: 38811e06-e468-4dc8-bc84-3bee9c2e04e7
  Args:
    relation: :hasFather
    target: Prince_Joachim_of_Prussia
    source: Karl_Franz_Josef_Wilhelm_Friedrich_Eduard_Paul_of_Prussia
  AddTriple (a3017a75-3189-4929-aa13-414b35058d26)
 Call ID: a3017a75-3189-4929-aa13-414b35058d26
  Args:
    source: Karl_Franz_Josef_Wilhelm_Friedrich_Eduard_Paul_of_Prussia
    target: Marie-Auguste_of_Anhalt
    relation: :hasMother
  AssignClass (95d29c02-ca90-44a1-8781-b05c427040cb)
 Call ID: 95d29c02-ca90-44a1-8781-b05c427040cb
  Args:
    type: :Woman
    source: Henriette_Hermine_Wanda_Ida_Luise_von_Schönaich-Carolath
  AssignClass (52810fc7-d0ab-49fe-b9d6-a095ea1dcf4e)
 Call ID: 52810fc7-d0ab-49fe-b9d6-a095ea1dcf4e
  Args:
    type: :Person
    source: Henriette_Hermine_Wanda_Ida_Luise_von_Schönaich-Carolath
  AddTriple (8a53c12a-ed6c-40de-9d63-d7f95c0ad415)
 Call ID: 8a53c12a-ed6c-40de-9d63-d7f95c0ad415
  Args:
    relation: :hasRelation
    source: Karl_Franz_Josef_Wilhelm_Friedrich_Eduard_Paul_of_Prussia
    target: Henriette_Hermine_Wanda_Ida_Luise_von_Schönaich-Carolath
  AssignClass (933000e3-cc76-44ac-abb2-7954f9c93481)
 Call ID: 933000e3-cc76-44ac-abb2-7954f9c93481
  Args:
    source: Luise_Dora_Hartmann
    type: :Woman
  AssignClass (3ccedb3a-b04a-4fbf-8073-e94e2d0b6d8b)
 Call ID: 3ccedb3a-b04a-4fbf-8073-e94e2d0b6d8b
  Args:
    type: :Person
    source: Luise_Dora_Hartmann
  AddTriple (e79b234e-ceee-4a77-b69b-3bae4f6ca0cb)
 Call ID: e79b234e-ceee-4a77-b69b-3bae4f6ca0cb
  Args:
    relation: :hasRelation
    target: Luise_Dora_Hartmann
    source: Karl_Franz_Josef_Wilhelm_Friedrich_Eduard_Paul_of_Prussia
  AssignClass (4e89463f-7a96-4da4-9adb-7958d76764d0)
 Call ID: 4e89463f-7a96-4da4-9adb-7958d76764d0
  Args:
    source: Eva_Maria_Herrera_y_Valdeavellano
    type: :Woman
  AssignClass (40999a8c-589a-4fe8-b976-3f82bd4fa88f)
 Call ID: 40999a8c-589a-4fe8-b976-3f82bd4fa88f
  Args:
    source: Eva_Maria_Herrera_y_Valdeavellano
    type: :Person
  AddTriple (86dbb902-4848-4069-8637-ded5dd9f659f)
 Call ID: 86dbb902-4848-4069-8637-ded5dd9f659f
  Args:
    relation: :hasRelation
    target: Eva_Maria_Herrera_y_Valdeavellano
    source: Karl_Franz_Josef_Wilhelm_Friedrich_Eduard_Paul_of_Prussia
  AssignClass (1f913cbe-dc03-4f88-8cc5-02ae1e1a7c16)
 Call ID: 1f913cbe-dc03-4f88-8cc5-02ae1e1a7c16
  Args:
    type: :Man
    source: Eitel_Friedrich_of_Prussia
  AssignClass (f60042ea-ebfb-42c0-92dd-2c8c7345d7e2)
 Call ID: f60042ea-ebfb-42c0-92dd-2c8c7345d7e2
  Args:
    source: Eitel_Friedrich_of_Prussia
    type: :Person
  AddTriple (abfe119b-48d2-4e0b-a997-9f9500f70b97)
 Call ID: abfe119b-48d2-4e0b-a997-9f9500f70b97
  Args:
    source: Prince_Joachim_of_Prussia
    target: Eitel_Friedrich_of_Prussia
    relation: :isBrotherOf
  Finish (8376b4a7-31a1-41bb-9968-5aaaca66e47a)
 Call ID: 8376b4a7-31a1-41bb-9968-5aaaca66e47a
  Args: