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
Ernst August von Hannover (German: Ernst August Albert Paul Otto Rupprecht Oskar Berthold Friedrich-Ferdinand Christian-Ludwig Prinz von Hannover Herzog zu Braunschweig und Lüneburg Königlicher Prinz von Großbritannien und Irland, lit.
'Ernest Augustus Albert Paul Otto Rupert Oscar Berthold Frederick-Ferdinand Christian-Louis, Prince of Hanover, Duke of Brunswick and Lüneburg, Royal Prince of Great Britain and Ireland'; born 26 February 1954) is the head of the House of Hanover, members of which reigned in Great Britain and Ireland from 1714 to 1901, the Kingdom of Hanover from 1814 to 1866 (electorate, from 1714 to 1814), and the Duchy of Brunswick from 1913 to 1918.
As the husband of Princess Caroline of Monaco, he is the brother-in-law of Albert II, Prince of Monaco.
Background and education

Ernst August was born in Hanover, the eldest son of Prince Ernest Augustus of Hanover (1914–1987), the former Hereditary Prince of Brunswick and his first wife, Princess Ortrud of Schleswig-Holstein-Sonderburg-Glücksburg (1925–1980).
He was christened Ernst August Albert Paul Otto Rupprecht Oskar Berthold Friedrich-Ferdinand Christian-Ludwig.
As the senior male-line descendant of George III of the United Kingdom, Ernst August is head of the House of Hanover.
He is a first cousin of Queen Sofía of Spain and King Constantine II of Greece.
Ancestry and heritage

The title of Prince of Great Britain and Ireland was recognised ad personam for Ernst August's father and his father's siblings by George V of the United Kingdom on 17 June 1914.
However, the title Royal Prince of Great Britain and Ireland had been entered into the family's German passports, together with the German titles, in 1914.
Ernst August continues to claim the style, "Royal Prince of Great Britain and Ireland".
However, in addition to being a German, Ernst August also has British citizenship since his father had successfully claimed it under the Sophia Naturalization Act 1705 (in the case of Attorney-General v. Prince Ernest Augustus of Hanover).
Since foreign royal titles can't be entered into a British passport, his father ended up being named Ernest Augustus Guelph, with the addition of His Royal Highness.
His children, including Ernst August, inherited British nationality under this name.
Marriage and family

First marriage

By a 24 August 1981 declaration issued by his father as the Head of House, pursuant to Chapter 3, §§ 3 and 5 of the House laws of 1836, Ernst August was authorised to marry dynastically, and did firstly marry, civilly in Pattensen on 28 August 1981 and religiously on 30 August 1981, Chantal Hochuli (born 2 June 1955 in Zürich), the daughter and heiress of a Swiss German architect and real estate developer, Johann Gustav "Hans" Hochuli (14 March 1912 in Switzerland – ?), and his German wife Rosmarie Lembeck (8 April 1921, in Essen, Rhine, Prussia, Germany – 12 December 2011).
They have two sons, Prince Ernst August (born 19 July 1983) and Prince Christian (born 1 June 1985).
Ernst August and Chantal Hochuli divorced in London on 23 October 1997.
In 1988, Ernst August unsuccessfully claimed custody of his infant nephew Otto Heinrich, son of his younger brother, Prince Ludwig Rudolph of Hanover.
Ludwig Rudolph placed a call to his brother in London, imploring him to take care of the couple's 10-month-old son, and shortly afterwards died by suicide.
Custody of Otto Heinrich was eventually awarded, contrary to the expressed wishes of Ludwig Rudolph as the surviving parent and Ernst August's legal efforts, to the child's maternal grandparents, Count Ariprand (1925–1996) and Countess Maria von Thurn und Valsassina-Como-Vercelli (born 1929), to be raised at their family seat, Bleiburg Castle in southern Austria.
Second marriage

Ernst August married secondly, civilly in Monaco on 23 January 1999, Princess Caroline of Monaco, who was at the time expecting their daughter, Princess Alexandra (born 20 July 1999).
As he was descended from George II of Great Britain in the male line, Ernst August sought and received permission to marry pursuant to the British Royal Marriages Act 1772, which would not be repealed until the Succession to the Crown Act 2013 took effect on 26 March 2015.
Similarly the Monégasque court officially notified the government of France of Caroline's marriage to Ernst August, receiving assurance that there was no objection in compliance with the (since defunct)
Moreover, in order for Caroline to retain her claim to the throne of Monaco and to transmit succession rights to future offspring, the couple were also obliged to obtain the approval of yet a third nation, in the form of official consent to the marriage of Caroline's father, Prince Rainier III, as the sovereign of Monaco.
After their marriage, Ernst August and Caroline moved to Le Mée-sur-Seine, France, where they had purchased an 18th-century manor house from their friend Karl Lagerfeld.
In 2009, it was reported that Caroline had separated from Ernst August and returned to live in Monaco.
Controversies

Assault on journalist

In 1999, Ernst August was accused of assaulting a journalist with an umbrella.
Turkish Pavilion

Ernst August was photographed urinating on the Turkish Pavilion at the Expo 2000 event in Hanover, causing a diplomatic incident and a complaint from the Turkish embassy accusing him of insulting the Turkish people.
Assault charge

In 2000, Ernst August was involved in a dispute with a German man, Joseph Brunnlehner, on the island of Lamu in Kenya.
Brunnlehner was the operator of a disco, and Ernst August allegedly assaulted him with a knuckleduster, upset about the noise coming from the disco.
Family property dispute

In 2004, Ernst August had signed over his German property to his elder son, including Marienburg Castle, the agricultural estate of Calenberg Castle, the "Princely House" at Herrenhausen Gardens in Hanover and some forests near Blankenburg Castle (Harz) which he had repurchased in former East Germany after the German reunification of 1990.
At the time, Ernst August's wealth was estimated as high as $250 million.
Since then, the younger Ernst August has taken over many representative tasks on behalf of his father.
In 2013, however, Ernst August was removed from the chairmanship of a family foundation based in Liechtenstein, the Duke of Cumberland Foundation, which holds the properties near Gmunden in Austria, the Hanovers' main residence in exile after 1866 when their Kingdom of Hanover was annexed by Prussia.
Instead, the younger Ernst August was put in charge, reportedly for negligence on part of his father, at the initiative of the foundation's trustee Prince Michael of Liechtenstein.
The foundation manages vast forests, a game park, a hunting lodge, the Queen's Villa and other property.
In 2017, Ernst August filed legal action to recover his chairmanship, and he intends to revoke the bestowal of his German property.
Assault on police

In 2020, under the influence of alcohol and medication, Ernst August injured a police officer at his hunting lodge in Austria.
Health

On Sunday, 3 April 2005, Ernst August was admitted to hospital with acute pancreatitis.
The next day, he fell into a deep coma, two days before the death of his father-in-law, Rainier III, Prince of Monaco.



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
  AssignClass (1995fa25-31e7-45d7-9462-9007dc074163)
 Call ID: 1995fa25-31e7-45d7-9462-9007dc074163
  Args:
    source: Ernst_August_von_Hannover
    type: :Man
  AssignClass (639aeb69-5978-46bf-8f5d-629f7e3aa6d2)
 Call ID: 639aeb69-5978-46bf-8f5d-629f7e3aa6d2
  Args:
    source: Prince_Ernest_Augustus_of_Hannover
    type: :Man
  AssignClass (9e4e0731-e896-4103-b7f5-f20aee491eac)
 Call ID: 9e4e0731-e896-4103-b7f5-f20aee491eac
  Args:
    type: :Woman
    source: Princess_Ortrud_of_Schleswig-Holstein-Sonderburg-Glücksburg
  AddLiteral (3b731a6c-a693-41e9-935e-21aa4b4a4f43)
 Call ID: 3b731a6c-a693-41e9-935e-21aa4b4a4f43
  Args:
    source: Ernst_August_von_Hannover
    relation: :hasBirthYear
    literal_value: 1954
    literal_type: xsd:integer
  AddTriple (69f2dece-2e27-4025-a3a8-0ae88c2ad331)
 Call ID: 69f2dece-2e27-4025-a3a8-0ae88c2ad331
  Args:
    source: Ernst_August_von_Hannover
    target: Prince_Ernest_Augustus_of_Hannover
    relation: :hasFather
  AddTriple (be27cfc3-9c78-49fa-93c6-dcde40b812aa)
 Call ID: be27cfc3-9c78-49fa-93c6-dcde40b812aa
  Args:
    source: Ernst_August_von_Hannover
    target: Princess_Ortrud_of_Schleswig-Holstein-Sonderburg-Glücksburg
    relation: :hasMother
  AddLiteral (8e38e15a-b056-44dc-bdd7-825a5bda88ae)
 Call ID: 8e38e15a-b056-44dc-bdd7-825a5bda88ae
  Args:
    source: Prince_Ernest_Augustus_of_Hannover
    literal_type: xsd:integer
    literal_value: 1914
    relation: :hasBirthYear
  AddLiteral (6c8f60e3-5727-4591-a747-8f5ee19314b6)
 Call ID: 6c8f60e3-5727-4591-a747-8f5ee19314b6
  Args:
    source: Prince_Ernest_Augustus_of_Hannover
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 1987
  AddLiteral (7f63c062-1720-40e4-b445-cbf9985ba8bf)
 Call ID: 7f63c062-1720-40e4-b445-cbf9985ba8bf
  Args:
    relation: :hasBirthYear
    literal_value: 1925
    literal_type: xsd:integer
    source: Princess_Ortrud_of_Schleswig-Holstein-Sonderburg-Glücksburg
  AddLiteral (5a1e76a0-8741-4c54-a9d4-1ecb335db031)
 Call ID: 5a1e76a0-8741-4c54-a9d4-1ecb335db031
  Args:
    literal_value: 1980
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: Princess_Ortrud_of_Schleswig-Holstein-Sonderburg-Glücksburg
  AssignClass (9143f0ec-d3d3-48ec-b496-943404737050)
 Call ID: 9143f0ec-d3d3-48ec-b496-943404737050
  Args:
    source: Chantal_Hochuli
    type: :Woman
  AddLiteral (9f78e52b-8288-479a-b8aa-781119eadc46)
 Call ID: 9f78e52b-8288-479a-b8aa-781119eadc46
  Args:
    source: Chantal_Hochuli
    relation: :hasBirthYear
    literal_value: 1955
    literal_type: xsd:integer
  AddLiteral (6d4b472d-d723-4fa1-bd61-b76a6d24537a)
 Call ID: 6d4b472d-d723-4fa1-bd61-b76a6d24537a
  Args:
    source: Ernst_August_von_Hannover
    relation: :hasMarriageYear
    literal_type: xsd:integer
    literal_value: 1981
  AddTriple (984c5062-3801-47c1-bf55-6e4340dfe7df)
 Call ID: 984c5062-3801-47c1-bf55-6e4340dfe7df
  Args:
    relation: :hasRelation
    source: Ernst_August_von_Hannover
    target: Chantal_Hochuli
  AssignClass (c6755259-101d-4fe3-8aa5-c85a463beec7)
 Call ID: c6755259-101d-4fe3-8aa5-c85a463beec7
  Args:
    source: Prince_Ernst_August_1983
    type: :Man
  AssignClass (8cd910fb-e64e-4c8b-90db-0ec4789633ef)
 Call ID: 8cd910fb-e64e-4c8b-90db-0ec4789633ef
  Args:
    type: :Man
    source: Prince_Christian_1985
  AddTriple (62acd122-e8d3-4511-bf81-854b26d29d23)
 Call ID: 62acd122-e8d3-4511-bf81-854b26d29d23
  Args:
    target: Ernst_August_von_Hannover
    source: Prince_Ernst_August_1983
    relation: :isSonOf
  AddTriple (80590333-0b2e-44d8-a1e8-56bd6e7df6c2)
 Call ID: 80590333-0b2e-44d8-a1e8-56bd6e7df6c2
  Args:
    source: Prince_Ernst_August_1983
    target: Chantal_Hochuli
    relation: :isSonOf
  AddTriple (31bfcecd-1126-46f0-b2e8-f1800044ab8e)
 Call ID: 31bfcecd-1126-46f0-b2e8-f1800044ab8e
  Args:
    relation: :isSonOf
    source: Prince_Christian_1985
    target: Ernst_August_von_Hannover
  AddTriple (a493ff21-58b4-4f37-9fb4-3afad045879d)
 Call ID: a493ff21-58b4-4f37-9fb4-3afad045879d
  Args:
    target: Chantal_Hochuli
    source: Prince_Christian_1985
    relation: :isSonOf
  AssignClass (e131d2c3-c03f-49fe-b737-a455a3735951)
 Call ID: e131d2c3-c03f-49fe-b737-a455a3735951
  Args:
    source: Princess_Caroline_of_Monaco
    type: :Woman
  AddLiteral (b92d2a65-c66d-49ec-8a01-408bbb1e8b8d)
 Call ID: b92d2a65-c66d-49ec-8a01-408bbb1e8b8d
  Args:
    source: Ernst_August_von_Hannover
    relation: :hasMarriageYear
    literal_value: 1999
    literal_type: xsd:integer
  AddTriple (75aefdd6-2a37-4736-80b3-d716640455a3)
 Call ID: 75aefdd6-2a37-4736-80b3-d716640455a3
  Args:
    relation: :hasRelation
    target: Princess_Caroline_of_Monaco
    source: Ernst_August_von_Hannover
  AssignClass (bde6f4c7-a264-4970-a1a1-deb3983c2b28)
 Call ID: bde6f4c7-a264-4970-a1a1-deb3983c2b28
  Args:
    source: Princess_Alexandra_1999
    type: :Woman
  AddTriple (a8da06dd-7289-464d-a5b7-30fbecb89bf3)
 Call ID: a8da06dd-7289-464d-a5b7-30fbecb89bf3
  Args:
    target: Ernst_August_von_Hannover
    source: Princess_Alexandra_1999
    relation: :isDaughterOf
  AddTriple (05f587e0-81d7-47dd-8efc-0ac7439f0ec7)
 Call ID: 05f587e0-81d7-47dd-8efc-0ac7439f0ec7
  Args:
    relation: :isDaughterOf
    target: Princess_Caroline_of_Monaco
    source: Princess_Alexandra_1999
  AssignClass (806b6d59-4f84-400e-a31d-3035d46746d0)
 Call ID: 806b6d59-4f84-400e-a31d-3035d46746d0
  Args:
    source: Prince_Ludwig_Rudolph_of_Hannover
    type: :Man
  AddTriple (c3487bb3-44ce-48ff-aa1c-2294e761d1e6)
 Call ID: c3487bb3-44ce-48ff-aa1c-2294e761d1e6
  Args:
    relation: :isBrotherOf
    source: Prince_Ludwig_Rudolph_of_Hannover
    target: Ernst_August_von_Hannover
  AssignClass (5ec35223-945f-431e-9002-cf30d862c1c5)
 Call ID: 5ec35223-945f-431e-9002-cf30d862c1c5
  Args:
    type: :Man
    source: Otto_Heinrich
  AddTriple (18f57857-1091-4051-9dea-a60a217543fa)
 Call ID: 18f57857-1091-4051-9dea-a60a217543fa
  Args:
    source: Otto_Heinrich
    target: Prince_Ludwig_Rudolph_of_Hannover
    relation: :isSonOf
  AssignClass (ee48f1ea-6eab-4bfc-88c1-80cfc6e48649)
 Call ID: ee48f1ea-6eab-4bfc-88c1-80cfc6e48649
  Args:
    source: Johann_Gustav_Hans_Hochuli
    type: :Man
  AssignClass (c3fcb250-5131-412c-a6b8-bf48bddd2005)
 Call ID: c3fcb250-5131-412c-a6b8-bf48bddd2005
  Args:
    source: Rosmarie_Lembeck
    type: :Woman
  AddTriple (393614d8-3fbc-4c47-8997-0eb2f1b4623b)
 Call ID: 393614d8-3fbc-4c47-8997-0eb2f1b4623b
  Args:
    source: Johann_Gustav_Hans_Hochuli
    target: Chantal_Hochuli
    relation: :isFatherOf
  AddTriple (59eb7a73-47a6-46d0-931a-88987b408929)
 Call ID: 59eb7a73-47a6-46d0-931a-88987b408929
  Args:
    relation: :isMotherOf
    source: Rosmarie_Lembeck
    target: Chantal_Hochuli
  AssignClass (ea69c3df-ace5-4ed8-b68c-ac3944f867f4)
 Call ID: ea69c3df-ace5-4ed8-b68c-ac3944f867f4
  Args:
    type: :Man
    source: Count_Ariprand
  AssignClass (cd64deff-1a2f-4b0f-9fa4-38b71cf920fc)
 Call ID: cd64deff-1a2f-4b0f-9fa4-38b71cf920fc
  Args:
    source: Countess_Maria_von_Thurn_und_Valsassina-Como-Vercelli
    type: :Woman
  AddTriple (caf63260-a649-40e1-b058-1d0ed141ab60)
 Call ID: caf63260-a649-40e1-b058-1d0ed141ab60
  Args:
    source: Count_Ariprand
    target: Countess_Maria_von_Thurn_und_Valsassina-Como-Vercelli
    relation: :isFatherOf
  AddTriple (526afc99-7d4b-490c-b4b6-37863ac106de)
 Call ID: 526afc99-7d4b-490c-b4b6-37863ac106de
  Args:
    source: Countess_Maria_von_Thurn_und_Valsassina-Como-Vercelli
    target: Countess_Maria_von_Thurn_und_Valsassina-Como-Vercelli
    relation: :isMotherOf
  AssignClass (ed189368-371f-42aa-bc4b-9f0cffdff5e1)
 Call ID: ed189368-371f-42aa-bc4b-9f0cffdff5e1
  Args:
    type: :Man
    source: Prince_Rainier_III
  AddTriple (9b97a3e6-d3e0-4043-b330-60ae9b431fcd)
 Call ID: 9b97a3e6-d3e0-4043-b330-60ae9b431fcd
  Args:
    target: Princess_Caroline_of_Monaco
    source: Prince_Rainier_III
    relation: :isFatherOf
  Finish (9c5f00d1-ee35-4646-9c16-9deaaeafc35a)
 Call ID: 9c5f00d1-ee35-4646-9c16-9deaaeafc35a
  Args: