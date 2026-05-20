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
Oskar Karl Gustav Adolf Prince of Prussia (27 July 1888 – 27 January 1958) was the fifth son of German Emperor Wilhelm II and Augusta Victoria of Schleswig-Holstein-Sonderburg-Augustenburg.
Biography

Birth and family

Prinz Oskar of Prussia was born on 27 July 1888 at his parents' residence in the Marmorpalais of Potsdam in the Province of Brandenburg.
He was the fifth son of the German Emperor Wilhelm II, and his first wife, Princess Augusta Victoria of Schleswig-Holstein, and was born in the so-called Year of the Three Emperors, just a month after his 29-year-old father had become German Emperor and King of Prussia.
Prince Oskar had five brothers: Crown Prince Wilhelm, Prince Eitel Friedrich, Prince Adalbert, Prince August Wilhelm, Prince Joachim and one sister: Princess Viktoria Luise.
Education

Prince Oskar was educated as a cadet at the Prinzenhaus in Plön, in his mother's ancestral Schleswig-Holstein, as his brothers had been before him.
Military career

During the early months of the First World War, he commanded Grenadierregiment "König Wilhelm I." (2.
Future fighter ace Manfred von Richthofen witnessed the 22 August 1914, attack on Virton, Belgium, and wrote of Prinz Oskar's bravery and his inspirational leadership at the front of his regiment as they went into combat.
For this action, Oskar earned the Iron Cross, Second Class.
A month later, at Verdun, Oskar again led his men in a successful assault into heavy combat, and was awarded the Iron Cross, First Class.
In the early 1920s, his name was listed with other members of the general staff or the royal family accused of war crimes, and was condemned in the Press for applying for a colonel's pension from the Weimar Republic.
During the 1930s, when the Hohenzollern family attempted to test the waters for a return to power through Nationalist Socialism, Oskar appears to have played along, and eventually was commissioned at Generalmajor zur Verfügung (rank equivalent to brigadier general, "available for assignment"), circa 1 March 1940.
As the family fell out of favour with Hitler (with the exception of Oskar's middle brother, August Wilhelm), it became evident that there would be no restoration of the monarchy through the Nazis.
With the early battlefield deaths of Oskar's son (also named Oskar, killed in Poland, September 1939) and his nephew (Wilhelm, son of the Crown Prince, died of wounds received in France, May 1940)
the German people harboured a newfound sentiment for the royal family amidst the totalitarian regime that was Nazi Germany.
As a consequence, the majority of royals serving in the German Armed Forces appear to have had their commissions canceled, including Prinz Oskar.
Master of Knights, Protestant Order of Saint John

The Johanniterorden (The Order of Saint John (Bailiwick of Brandenburg)) was a favourite of the Hohenzollerns, historically, and of Prince Oskar's immediate family specifically.
His father and uncle were members, and his brother, Eitel Friedrich, served as its Master of Knights (Herrenmeister), from 1907 to 1926.
Prinz Oskar served as the thirty-fifth Master of Knights from Eitel Friedrich's resignation in 1926 until his death in 1958.
Modern historians credit Prinz Oskar for saving the ancient order from oblivion during the cultural purges of the Nazi regime.
It is from this struggle that he held his anti-Nazi sentiments.
After his death in 1958, his youngest son, Prinz Wilhelm Karl, became his permanent successor.
Prinz Oskar's grandson, to whom he is namesake, Dr. Oskar Hohenzollern, is the current (thirty-seventh) Master of Knights.
Marriage and issue

Prinz Oskar was married on 31 July 1914 to Countess Ina-Marie Helene Adele Elise von Bassewitz (27 January 1888 – 17 September 1973).
On 27 July 1914, prior to the wedding, Ina Marie was granted the title "Countess von Ruppin".
Both the civil and religious ceremonies took place at Schloß Bellevue near Berlin, Prussia.
Initially the union was a morganatic marriage, but on 3 November 1919 was decreed to be dynastic in accordance with the house laws of the Royal House of Hohenzollern.
Henceforth, from 21 June 1920, his wife was titled "Princess of Prussia" with the style Royal Highness.
The couple had four children:


Death

Prince Oskar, whose health declined during the final years of his life, died of stomach cancer in a clinic in Munich on 27 January 1958, on his wife's 70th birthday and what would have been his father's 99th birthday.
He was the last surviving son of Wilhelm II.



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
  AssignClass (7472a404-5774-4adb-9b64-b8f7bad41922)
 Call ID: 7472a404-5774-4adb-9b64-b8f7bad41922
  Args:
    type: :Man
    source: Oskar_Prince_of_Prussia
  AssignClass (60fde709-73ef-459b-8468-f4d346927da3)
 Call ID: 60fde709-73ef-459b-8468-f4d346927da3
  Args:
    source: Wilhelm_II
    type: :Man
  AssignClass (c1ea7e45-40f1-45f1-8a4d-97fd7c7d99f3)
 Call ID: c1ea7e45-40f1-45f1-8a4d-97fd7c7d99f3
  Args:
    source: Augusta_Victoria_of_Schleswig-Holstein
    type: :Woman
  AddLiteral (43018c45-a2fc-4681-a8d7-b2af113ab366)
 Call ID: 43018c45-a2fc-4681-a8d7-b2af113ab366
  Args:
    literal_type: xsd:integer
    source: Oskar_Prince_of_Prussia
    relation: :hasBirthYear
    literal_value: 1888
  AddLiteral (98ee34d9-a8a8-4c19-a56d-1abd296e6d7a)
 Call ID: 98ee34d9-a8a8-4c19-a56d-1abd296e6d7a
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: Oskar_Prince_of_Prussia
    literal_value: 1958
  AddTriple (bdd53478-3f7c-4fa4-a009-81e3856f27b7)
 Call ID: bdd53478-3f7c-4fa4-a009-81e3856f27b7
  Args:
    target: Wilhelm_II
    relation: :hasFather
    source: Oskar_Prince_of_Prussia
  AddTriple (bb7b7231-34e9-4dd1-97df-04b6fcaac873)
 Call ID: bb7b7231-34e9-4dd1-97df-04b6fcaac873
  Args:
    relation: :hasMother
    source: Oskar_Prince_of_Prussia
    target: Augusta_Victoria_of_Schleswig-Holstein
  AssignClass (e559284f-6465-4e9a-b70b-fae990c8d84e)
 Call ID: e559284f-6465-4e9a-b70b-fae990c8d84e
  Args:
    type: :Man
    source: Crown_Prince_Wilhelm
  AssignClass (72e8f6d2-5228-404b-8fd8-db10afdf3532)
 Call ID: 72e8f6d2-5228-404b-8fd8-db10afdf3532
  Args:
    source: Prince_Eitel_Friedrich
    type: :Man
  AssignClass (7b2f503c-8760-4042-acf9-50d32c1b5bba)
 Call ID: 7b2f503c-8760-4042-acf9-50d32c1b5bba
  Args:
    type: :Man
    source: Prince_Adalbert
  AssignClass (6d7fc569-ff68-4a05-8386-05f8716d32e6)
 Call ID: 6d7fc569-ff68-4a05-8386-05f8716d32e6
  Args:
    type: :Man
    source: Prince_August_Wilhelm
  AssignClass (ac010750-f706-4205-93b9-4efb8a3cbe3c)
 Call ID: ac010750-f706-4205-93b9-4efb8a3cbe3c
  Args:
    source: Prince_Joachim
    type: :Man
  AssignClass (ae778739-b7cd-4d00-b431-2918aeab404f)
 Call ID: ae778739-b7cd-4d00-b431-2918aeab404f
  Args:
    source: Princess_Viktoria_Luise
    type: :Woman
  AddTriple (47f61ccd-3944-4f12-ab6c-57ec175b6016)
 Call ID: 47f61ccd-3944-4f12-ab6c-57ec175b6016
  Args:
    source: Oskar_Prince_of_Prussia
    relation: :hasBrother
    target: Crown_Prince_Wilhelm
  AddTriple (819ef4ac-b988-4351-89e6-51024aaf691b)
 Call ID: 819ef4ac-b988-4351-89e6-51024aaf691b
  Args:
    target: Prince_Eitel_Friedrich
    relation: :hasBrother
    source: Oskar_Prince_of_Prussia
  AddTriple (972f6372-4e72-4280-8807-c9a4398d4566)
 Call ID: 972f6372-4e72-4280-8807-c9a4398d4566
  Args:
    target: Prince_Adalbert
    source: Oskar_Prince_of_Prussia
    relation: :hasBrother
  AddTriple (41e6529e-dac9-4452-972f-7a6d1c829f40)
 Call ID: 41e6529e-dac9-4452-972f-7a6d1c829f40
  Args:
    relation: :hasBrother
    source: Oskar_Prince_of_Prussia
    target: Prince_August_Wilhelm
  AddTriple (267424ef-63f2-4091-ad7d-1a859488756f)
 Call ID: 267424ef-63f2-4091-ad7d-1a859488756f
  Args:
    target: Prince_Joachim
    relation: :hasBrother
    source: Oskar_Prince_of_Prussia
  AddTriple (7139e5da-f650-4ead-b102-5ec4ad84d25d)
 Call ID: 7139e5da-f650-4ead-b102-5ec4ad84d25d
  Args:
    target: Princess_Viktoria_Luise
    source: Oskar_Prince_of_Prussia
    relation: :hasSister
  AssignClass (898a2b07-363d-4cde-a903-31137b7de5c8)
 Call ID: 898a2b07-363d-4cde-a903-31137b7de5c8
  Args:
    source: Ina-Marie_von_Bassewitz
    type: :Woman
  AddTriple (f1e2155d-375a-49a7-8ef2-bf225966cff8)
 Call ID: f1e2155d-375a-49a7-8ef2-bf225966cff8
  Args:
    target: Ina-Marie_von_Bassewitz
    source: Oskar_Prince_of_Prussia
    relation: :hasMarriageYear
  AddLiteral (a4d8b301-8821-4ec2-af49-d5afe5a39a34)
 Call ID: a4d8b301-8821-4ec2-af49-d5afe5a39a34
  Args:
    literal_value: 1914
    relation: :hasMarriageYear
    source: Oskar_Prince_of_Prussia
    literal_type: xsd:integer
  AssignClass (c186f260-532f-48ba-b54e-a7f4964d294e)
 Call ID: c186f260-532f-48ba-b54e-a7f4964d294e
  Args:
    source: Oskar_the_younger
    type: :Man
  AddTriple (78d8ff06-409f-4a39-9c95-27eac279261d)
 Call ID: 78d8ff06-409f-4a39-9c95-27eac279261d
  Args:
    target: Oskar_the_younger
    source: Oskar_Prince_of_Prussia
    relation: :hasSon
  AssignClass (6f115e58-aafe-444e-82ef-0060ccb4eab8)
 Call ID: 6f115e58-aafe-444e-82ef-0060ccb4eab8
  Args:
    source: Wilhelm_Karl
    type: :Man
  AddTriple (b66fd392-049f-45c6-b518-e825b174aeac)
 Call ID: b66fd392-049f-45c6-b518-e825b174aeac
  Args:
    target: Wilhelm_Karl
    source: Oskar_Prince_of_Prussia
    relation: :hasSon
  Finish (315eeb62-51fe-47bd-83f0-29705b7fc436)
 Call ID: 315eeb62-51fe-47bd-83f0-29705b7fc436
  Args: