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
Alexandrine of Mecklenburg-Schwerin (Alexandrine Auguste; 24 December 1879 – 28 December 1952) was Queen of Denmark from 1912 to 1947, as well as Queen of Iceland from 1918 to 1944 as the wife of King Christian X.


Alexandrine was the daughter of Frederick Francis III, Grand Duke of Mecklenburg-Schwerin, and Grand Duchess Anastasia Mikhailovna of Russia.
She was brought up with simplicity, and her early life was peripatetic, spending summers in Mecklenburg and the rest of the year in the south of France.
She married Prince Christian of Denmark in 1898.
Alexandrine became crown princess in 1906 and queen consort of Denmark in 1912.
Early life

Birth and family

Alexandrine was born a Duchess of Mecklenburg-Schwerin on Christmas Eve of 1879, in the city of Schwerin, the capital of the vast Grand Duchy of Mecklenburg-Schwerin in Northern Germany.
Her father was Frederick Francis, Hereditary Grand Duke of Mecklenburg-Schwerin; who was the eldest son of and heir to the reigning Grand Duke Frederick Francis II.
Her mother was Grand Duchess Anastasia Mikhailovna of Russia, who was a granddaughter of Emperor Nicholas I of Russia.
Alexandrine was her parents' first child, and was born eleven months after their wedding in St. Petersburg.
She was born in the Neustadt Palace (New Town Palace) in Schwerin, which was her parents' residence in the city at the time.
Duchess Alexandrine had two younger siblings: her only brother was Duke Frederick Francis, who in 1897 succeeded their father as Grand Duke of Mecklenburg-Schwerin, and her only sister was Duchess Cecilie, who in 1906 married the German Crown Prince Wilhelm of Prussia, eldest son of German Emperor William II.
She was also a paternal first cousin of Juliana of the Netherlands.
Her mother was the paternal aunt of Princess Irina Alexandrovna of Russia, the wife of Felix Yusupov, one of the murderers of Rasputin.
Childhood and early adulthood

After their father's succession as Grand Duke upon the death of his father on 15 April 1883, Alexandrine grew up with her brother and sister at the Castle in Schwerin, at the royal residences of Ludwigslust Palace and the Gelbensande hunting lodge, only a few kilometres from the Baltic Sea coast.
The wet, damp, and cold Northern European climate of Mecklenburg was not good for his health, and as a result, Alexandrine spent a large amount of time with her family away from Mecklenburg, by the Lake Geneva, and in Palermo, Baden-Baden and Cannes in the south of France, where the family owned a large estate, the Villa Wenden.
Cannes was favoured at the time by European royalty, including some whom Alexandrine personally met, such as Empress Eugénie of France and her future husband's uncle, Edward VII of the United Kingdom.
First years in Denmark

Engagement and marriage

It was also in Cannes during the winter visit of 1897 that Duchess Alexandrine met her future husband, Prince Christian of Denmark, the eldest son of Crown Prince Frederik and Crown Princess Louise of Denmark.
The two young royals were engaged in Schwerin on 24 March 1897.
In April 1897, shortly after the engagement was announced, her father the Grand Duke died suddenly at the age of just 46 years.
The wedding of Duchess Alexandrine and Prince Christian was celebrated on 26 April 1898 in Cannes, when she was 18 years old.
They had two children:


Early years in Denmark

Upon their arrival in Denmark, the couple were given Christian VIII's Palace at the Amalienborg palace complex in central Copenhagen as their principal residence and Sorgenfri Palace in Kongens Lyngby north of Copenhagen as a summer residence.
On 29 January 1906, her husband's grandfather King Christian IX died, and Christian's father ascended the throne as King Frederik VIII.
Christian himself became crown prince, and Alexandrine became crown princess.
Alexandrine's husband acceded to the throne as Christian X, and Alexandrine became queen consort of Denmark.
The revolution in Russia brought much heartbreak for Alexandrine as three of her uncles, Nicholas, George and Sergey, were killed by the Bolsheviks.
Her rejection of Major General Kurt Himer, Chief of Staff to General Kaupisch on 9 April 1940 became a symbol for her loyalty toward Denmark before her birth country Germany and was diplomatically obliged to receive the German General commander at her castle.
Then, after a pause, she added: "I am a German, that's right, but today I'm ashamed of it."
When General Himer asked for an audience with the monarch, Christian was persuaded to receive him by his daughter-in-law as he would any other, which was supported by Alexandrine.
He asked to do so alone, but Alexandrine told him she would interrupt them.
"


It was reported, that although Alexandrine was seen as shy and disliked official ceremonies, she had a "sharp" intelligence, and she was, together with her daughter-in-law, Ingrid of Sweden, a true support of the monarch and a driving force for the resistance toward the occupation within the royal house.
It was also reported, that in contrast to the monarch himself and the Crown Prince, the Queen and the Crown Princess never lost their calm when the nation was attacked.
Her first years in Denmark were afflicted by the prevailing anti-German attitude of the Danes, but she won them over.
Kaj Munk is quoted to describe the public appreciation of her during World War II with his comment: "Protect our Queen, the only German we would like to keep!"


Later life

In 1947, she was widowed; she became the first queen dowager of Denmark to opt not to use that title.
In her later years, Alexandrine spent most of her widowhood at Marselisborg Castle in Jutland.
Queen Alexandrine died on 28 December 1952 in her sleep, four days after her birthday.



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
  AssignClass (7b918dba-d5b6-4a9d-8f34-92437cb928ae)
 Call ID: 7b918dba-d5b6-4a9d-8f34-92437cb928ae
  Args:
    source: Alexandrine_of_Mecklenburg-Schwerin
    type: :Woman
  AssignClass (0313751f-abfd-4057-98d9-e3232d12e56a)
 Call ID: 0313751f-abfd-4057-98d9-e3232d12e56a
  Args:
    type: :Person
    source: Alexandrine_of_Mecklenburg-Schwerin
  AddLiteral (6c2daee7-4875-4c30-98a8-a854ad1b019b)
 Call ID: 6c2daee7-4875-4c30-98a8-a854ad1b019b
  Args:
    literal_value: 1879
    source: Alexandrine_of_Mecklenburg-Schwerin
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (c55b0ec3-5cc3-42bc-84f7-4145cb0d9667)
 Call ID: c55b0ec3-5cc3-42bc-84f7-4145cb0d9667
  Args:
    source: Alexandrine_of_Mecklenburg-Schwerin
    literal_value: 1952
    literal_type: xsd:integer
    relation: :hasDeathYear
  AssignClass (e1d48c57-b93e-4025-a82e-a27da716f957)
 Call ID: e1d48c57-b93e-4025-a82e-a27da716f957
  Args:
    source: Frederick_Francis_III
    type: :Man
  AssignClass (213c50f1-6e71-415f-8014-c67712725ed5)
 Call ID: 213c50f1-6e71-415f-8014-c67712725ed5
  Args:
    source: Frederick_Francis_III
    type: :Person
  AssignClass (fadd98d9-46c7-44fc-9428-4b46fc6225b2)
 Call ID: fadd98d9-46c7-44fc-9428-4b46fc6225b2
  Args:
    source: Frederick_Francis_III
    type: :Ancestor
  AddTriple (28e9c861-d076-430d-804e-71a1290f6e37)
 Call ID: 28e9c861-d076-430d-804e-71a1290f6e37
  Args:
    source: Alexandrine_of_Mecklenburg-Schwerin
    target: Frederick_Francis_III
    relation: :hasFather
  AssignClass (0f5e86c2-7c07-48f1-a8f5-2d532dd0af4c)
 Call ID: 0f5e86c2-7c07-48f1-a8f5-2d532dd0af4c
  Args:
    source: Anastasia_Mikhailovna
    type: :Woman
  AssignClass (4cd9e971-16b3-4de5-a18d-89dd3bf28e55)
 Call ID: 4cd9e971-16b3-4de5-a18d-89dd3bf28e55
  Args:
    type: :Person
    source: Anastasia_Mikhailovna
  AssignClass (a1cca3f5-d11f-47e3-a07a-9854655197ea)
 Call ID: a1cca3f5-d11f-47e3-a07a-9854655197ea
  Args:
    type: :Ancestor
    source: Anastasia_Mikhailovna
  AddTriple (2ad0c8da-5e09-421c-b793-69e1c75290a6)
 Call ID: 2ad0c8da-5e09-421c-b793-69e1c75290a6
  Args:
    relation: :hasMother
    target: Anastasia_Mikhailovna
    source: Alexandrine_of_Mecklenburg-Schwerin
  AssignClass (b4ff863e-43d0-4428-b8be-ac2bf756f763)
 Call ID: b4ff863e-43d0-4428-b8be-ac2bf756f763
  Args:
    source: Christian_X
    type: :Man
  AssignClass (535584da-b65c-49a4-b8d2-037234823d14)
 Call ID: 535584da-b65c-49a4-b8d2-037234823d14
  Args:
    source: Christian_X
    type: :Person
  AddLiteral (3bee5d5c-f99c-4c28-bf37-13de42fad0d6)
 Call ID: 3bee5d5c-f99c-4c28-bf37-13de42fad0d6
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    source: Alexandrine_of_Mecklenburg-Schwerin
    literal_value: 1898
  AddTriple (ef2b27b3-77e3-4d5d-b7df-9f3d37fe237b)
 Call ID: ef2b27b3-77e3-4d5d-b7df-9f3d37fe237b
  Args:
    relation: :hasRelation
    target: Christian_X
    source: Alexandrine_of_Mecklenburg-Schwerin
  AssignClass (542c8a55-a28d-4af1-b003-48aacb3c125e)
 Call ID: 542c8a55-a28d-4af1-b003-48aacb3c125e
  Args:
    source: Frederick_Francis_Mecklenburg-Schwerin
    type: :Man
  AssignClass (308bb238-6c97-42f8-abea-7ac3e0978e97)
 Call ID: 308bb238-6c97-42f8-abea-7ac3e0978e97
  Args:
    source: Frederick_Francis_Mecklenburg-Schwerin
    type: :Person
  AddTriple (e4e30c6f-3ebe-40ee-9ca6-7479a5e4e15a)
 Call ID: e4e30c6f-3ebe-40ee-9ca6-7479a5e4e15a
  Args:
    target: Frederick_Francis_Mecklenburg-Schwerin
    source: Alexandrine_of_Mecklenburg-Schwerin
    relation: :hasBrother
  AssignClass (da326bc8-ff8e-4306-9ab9-727eca27c85c)
 Call ID: da326bc8-ff8e-4306-9ab9-727eca27c85c
  Args:
    type: :Woman
    source: Cecilie_of_Mecklenburg-Schwerin
  AssignClass (3ba52107-027d-4c89-878c-b81bfd6e3c4c)
 Call ID: 3ba52107-027d-4c89-878c-b81bfd6e3c4c
  Args:
    type: :Person
    source: Cecilie_of_Mecklenburg-Schwerin
  AddTriple (314f0fbe-8a77-4f73-87f0-e4fa8a48c436)
 Call ID: 314f0fbe-8a77-4f73-87f0-e4fa8a48c436
  Args:
    source: Alexandrine_of_Mecklenburg-Schwerin
    target: Cecilie_of_Mecklenburg-Schwerin
    relation: :hasSister
  AssignClass (ba60d121-eb72-4b50-bac5-2b479749be5d)
 Call ID: ba60d121-eb72-4b50-bac5-2b479749be5d
  Args:
    type: :Man
    source: Frederick_Francis_II
  AssignClass (2246ac11-8573-48fd-bf06-e8a60c523f48)
 Call ID: 2246ac11-8573-48fd-bf06-e8a60c523f48
  Args:
    type: :Person
    source: Frederick_Francis_II
  AssignClass (78fe1070-98df-4b56-9f50-9fddcfb74ff7)
 Call ID: 78fe1070-98df-4b56-9f50-9fddcfb74ff7
  Args:
    source: Frederick_Francis_II
    type: :Ancestor
  AddTriple (11bf91ef-8880-461f-ad2e-9f79b9e9e910)
 Call ID: 11bf91ef-8880-461f-ad2e-9f79b9e9e910
  Args:
    relation: :hasFather
    target: Frederick_Francis_II
    source: Frederick_Francis_III
  Finish (a102f550-eab7-4aa3-8a64-5d08bc677b15)
 Call ID: a102f550-eab7-4aa3-8a64-5d08bc677b15
  Args: