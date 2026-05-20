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
Princess Alexandra of Greece and Denmark (Greek: Αλεξάνδρα; romanized: Alexándra), later known as Grand Duchess Alexandra Georgievna of Russia (Russian: Алекса́ндра Гео́ргиевна); 30 August  1870 – 24 September  1891), was a member of the Greek royal family by birth and of the Russian imperial family by marriage.
Alexandra was the daughter of George I of Greece and Olga Constantinovna of Russia, and grew up in Athens.
In 1889, she married Grand Duke Paul Alexandrovich of Russia, her first cousin once removed.
The couple settled in Saint Petersburg and they had two children: Grand Duchess Maria Pavlovna (1890–1958) and Grand Duke Dmitri Pavlovich (1891–1942).
Early life

Princess Alexandra of Greece and Denmark was born on 30 August  1870 at Mon Repos, the summer residence of the Greek royal family on the island of Corfu.
She was the third child and eldest daughter of King George I of Greece and his wife, Grand Duchess Olga Constantinovna of Russia.
Alexandra's father was not a native Greek, but he had been born a Danish prince named Christian Wilhelm of Schleswig-Holstein-Sonderburg-Glücksburg, a son of Christian IX, King of Denmark, and he had been elected to the Greek throne at the age of seventeen.
Five of his sons (Constantine, George, Nicholas, Andrew and Christopher), and two daughters (Alexandra and Maria), attained adulthood.
King George was a taciturn man, but contrary to the general approach of the time, he believed in happy rambunctious children.
The long corridors of the royal palace in Athens were used by Alexandra and her siblings for all types of play and sometimes a "bike ride" would be led by the King himself.
Alexandra, nicknamed "Aline" within her family, or Greek Alix, to distinguish her from her aunt and godmother, Alexandra, Princess of Wales, had a sunny disposition and was much loved by her family.
"She looked young and beautiful, and ever since she was a child, life looked as it had nothing but joy and happiness in store for her.
"


Alexandra's playmates were her brother Nicholas and her sister Maria, who followed her in age.
Alexandra spent many holidays in Denmark visiting her paternal grandparents.
In Denmark, Alexandra and her siblings met their Russian and British cousins in large family gatherings.
Marriage and children

When she was 18 years old, she was married to Grand Duke Paul Alexandrovich of Russia, her maternal first cousin once removed and the youngest child and sixth son of Emperor Alexander II and his first wife, Princess Marie of Hesse and by Rhine.
They had become close when Grand Duke Paul spent winters in Greece due to his frequent respiratory illnesses.
The Greek royal family also frequently spent holidays with the Romanov family on visits to Russia or Denmark.
The wedding took place on 17 June  1889 in St. Petersburg, at the chapel of the Winter Palace.
They had two children:


Death

Seven months into her second pregnancy, Alexandra took a walk with her friends on the bank of the Moskva River and jumped directly into a boat that was permanently moored there, but fell as she got in.
The Grand Duchess was buried in the Peter and Paul Cathedral, St. Petersburg.
Her husband later morganatically remarried Olga Karnovich.
Alexandra's son would be involved in the murder of Grigori Rasputin, a friend of Tsarina Alexandra Feodorovna, in 1916.
In 1939 during the reign of her nephew George II of Greece, the Greek government obtained permission from the Soviet government under Joseph Stalin to rebury Princess Alexandra in Greece.
It was finally laid to rest near the Tatoi Palace.
Alexandra's marble tombstone over an empty tomb is still in its place in the Peter and Paul Cathedral.
The "Alexandra Maternity Hospital" (now "Alexandra General Hospital") in Athens was later named in her memory by another nephew, King Paul; it was affiliated with the University of Athens with a special remit to research and combat postpartum maternal mortality.



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
  AssignClass (636b55e8-52a6-4a89-bdb1-0d72f1209274)
 Call ID: 636b55e8-52a6-4a89-bdb1-0d72f1209274
  Args:
    type: :Woman
    source: Alexandra_of_Greece_and_Denmark
  AssignClass (9a83e90f-9846-4487-a0bb-1d501ceffb48)
 Call ID: 9a83e90f-9846-4487-a0bb-1d501ceffb48
  Args:
    type: :Person
    source: Alexandra_of_Greece_and_Denmark
  AddLiteral (6eaa1897-8ff6-49ff-b035-fdd033beb97b)
 Call ID: 6eaa1897-8ff6-49ff-b035-fdd033beb97b
  Args:
    relation: :knownAs
    source: Alexandra_of_Greece_and_Denmark
    literal_type: xsd:string
    literal_value: Alexandra
  AddLiteral (feac5f92-37f5-4bfd-97e2-3612687220e0)
 Call ID: feac5f92-37f5-4bfd-97e2-3612687220e0
  Args:
    literal_value: Aline
    literal_type: xsd:string
    source: Alexandra_of_Greece_and_Denmark
    relation: :alsoKnownAs
  AddLiteral (89dba22f-888a-4b70-8557-e9deaefa77ab)
 Call ID: 89dba22f-888a-4b70-8557-e9deaefa77ab
  Args:
    literal_value: 1870
    source: Alexandra_of_Greece_and_Denmark
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (109c0ca2-dc99-4aad-aace-4762a4732e41)
 Call ID: 109c0ca2-dc99-4aad-aace-4762a4732e41
  Args:
    literal_value: 1891
    source: Alexandra_of_Greece_and_Denmark
    relation: :hasDeathYear
    literal_type: xsd:integer
  AssignClass (dfedb953-41d8-4159-9503-bd98fdab0ad2)
 Call ID: dfedb953-41d8-4159-9503-bd98fdab0ad2
  Args:
    type: :Man
    source: George_I_of_Greece
  AssignClass (f18f0edb-3207-4502-bed4-63fce4ff0bb2)
 Call ID: f18f0edb-3207-4502-bed4-63fce4ff0bb2
  Args:
    type: :Ancestor
    source: George_I_of_Greece
  AssignClass (e59f67d7-4fd0-44d4-9178-6b79a3409d89)
 Call ID: e59f67d7-4fd0-44d4-9178-6b79a3409d89
  Args:
    type: :Person
    source: George_I_of_Greece
  AssignClass (7ea2695c-49eb-48a9-8a70-6a40745c0bab)
 Call ID: 7ea2695c-49eb-48a9-8a70-6a40745c0bab
  Args:
    type: :Woman
    source: Olga_Constantinovna_of_Russia
  AssignClass (b944a0a7-1ae6-4079-9800-477119c7f00f)
 Call ID: b944a0a7-1ae6-4079-9800-477119c7f00f
  Args:
    type: :Ancestor
    source: Olga_Constantinovna_of_Russia
  AssignClass (eec0f88d-b3f9-49cc-a4f6-eec57562c563)
 Call ID: eec0f88d-b3f9-49cc-a4f6-eec57562c563
  Args:
    type: :Person
    source: Olga_Constantinovna_of_Russia
  AddTriple (b2b3f591-6e54-4c60-8f3b-aa046c8a65b9)
 Call ID: b2b3f591-6e54-4c60-8f3b-aa046c8a65b9
  Args:
    target: George_I_of_Greece
    relation: :hasFather
    source: Alexandra_of_Greece_and_Denmark
  AddTriple (5d336638-a30b-4f07-9c99-62ef977fc76a)
 Call ID: 5d336638-a30b-4f07-9c99-62ef977fc76a
  Args:
    target: Olga_Constantinovna_of_Russia
    relation: :hasMother
    source: Alexandra_of_Greece_and_Denmark
  AssignClass (857f8dd0-7bf2-4971-808a-79ae276df501)
 Call ID: 857f8dd0-7bf2-4971-808a-79ae276df501
  Args:
    type: :Man
    source: Paul_Alexandrovich_of_Russia
  AssignClass (ad08ab3c-3d6b-4304-b70e-9dd0072b54d3)
 Call ID: ad08ab3c-3d6b-4304-b70e-9dd0072b54d3
  Args:
    type: :Person
    source: Paul_Alexandrovich_of_Russia
  AddLiteral (f7129d7a-73b7-47b3-bd98-227fb0fed48b)
 Call ID: f7129d7a-73b7-47b3-bd98-227fb0fed48b
  Args:
    literal_value: 1889
    literal_type: xsd:integer
    relation: :hasMarriageYear
    source: Alexandra_of_Greece_and_Denmark
  AddTriple (048bef6e-08bf-4138-b738-f023d0f1053b)
 Call ID: 048bef6e-08bf-4138-b738-f023d0f1053b
  Args:
    target: Paul_Alexandrovich_of_Russia
    source: Alexandra_of_Greece_and_Denmark
    relation: :hasRelation
  AssignClass (e19e3632-edb8-45af-8599-0633e7ee8454)
 Call ID: e19e3632-edb8-45af-8599-0633e7ee8454
  Args:
    type: :Woman
    source: Maria_Pavlovna
  AssignClass (11d9b78f-05f0-4f5a-905f-e2f2427934b2)
 Call ID: 11d9b78f-05f0-4f5a-905f-e2f2427934b2
  Args:
    type: :Person
    source: Maria_Pavlovna
  AssignClass (4e197a16-e456-45c3-8939-f2873b810758)
 Call ID: 4e197a16-e456-45c3-8939-f2873b810758
  Args:
    type: :Man
    source: Dmitri_Pavlovich
  AssignClass (537f564c-3a53-484f-8c57-e9ca2a61ddb2)
 Call ID: 537f564c-3a53-484f-8c57-e9ca2a61ddb2
  Args:
    type: :Person
    source: Dmitri_Pavlovich
  AddTriple (d8167cc9-ab8e-496a-8fec-df50469b7dcd)
 Call ID: d8167cc9-ab8e-496a-8fec-df50469b7dcd
  Args:
    target: Maria_Pavlovna
    relation: :hasChild
    source: Alexandra_of_Greece_and_Denmark
  AddTriple (51050f58-d9be-45b2-95c8-bf6b817b7f3f)
 Call ID: 51050f58-d9be-45b2-95c8-bf6b817b7f3f
  Args:
    relation: :hasChild
    source: Alexandra_of_Greece_and_Denmark
    target: Dmitri_Pavlovich
  AddTriple (e7010441-e09c-44a1-9c07-e7921e3f2dc6)
 Call ID: e7010441-e09c-44a1-9c07-e7921e3f2dc6
  Args:
    source: Paul_Alexandrovich_of_Russia
    relation: :hasChild
    target: Maria_Pavlovna
  AddTriple (fa6fbfa6-1317-4c43-8621-a8f38f00ed2f)
 Call ID: fa6fbfa6-1317-4c43-8621-a8f38f00ed2f
  Args:
    source: Paul_Alexandrovich_of_Russia
    relation: :hasChild
    target: Dmitri_Pavlovich
  Finish (0a332889-96b4-4481-9e14-623a2ff0bbf5)
 Call ID: 0a332889-96b4-4481-9e14-623a2ff0bbf5
  Args: