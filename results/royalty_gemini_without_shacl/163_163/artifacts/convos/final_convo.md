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
Grand Duchess Kira Kirillovna of Russia (9 May 1909 – 8 September 1967) was the second daughter of Grand Duke Kirill Vladimirovich of Russia and Princess Victoria Melita of Saxe-Coburg and Gotha.
She married Prince Louis Ferdinand of Prussia, grandson of the last German Emperor Wilhelm II.
Early life

Grand Duchess Kira Kirilovna of Russia was born on 9 May 1909, at her parents' house on Avenue Henri Martin in Paris.
Named after her father, she was the second child of Grand Duke Kirill Vladimirovich of Russia, and his wife, Princess Victoria Melita of Saxe-Coburg and Gotha.
In addition, her mother had divorced her former husband, Ernest Louis, Grand Duke of Hesse, the brother of the Tsarina Alexandra Feodorovna.
In 1908, after the death of Grand Duke Alexei Alexandrovich and before Kira's birth, Nicholas II restored Kirill to his rank of captain in the Imperial Russian Navy and his position as aide de camp to the emperor.
He was given the title Grand Duke of Russia and from then on his wife was styled as Her Imperial Highness Grand Duchess Viktoria Feodorovna.
Kira and her elder sister, Maria, had a privileged childhood.
Kira's early years were spent in luxury at her father's palace at 13 Glinka Street in Saint Petersburg, where her parents entertained their guests lavishly.
During World War I, Kira's father served as the commander of a unit of the Naval Guards, while her mother oversaw a motorized ambulance.
At the outbreak of the Russian revolution, Kira's father marched to the Tauride Palace at the head of the Naval Guards before the establishment of the Russian Provisional Government.
In June, Kira's father obtained permission from the provisional government to move to Finland.
Kira, eight at the time, recalled that they rode on a public train.
The family waited in Finland, hoping that the White guard would defeat the Bolsheviks and they could return to Russia.
Kira, then age nine, amused herself by taking long walks hunting for mushrooms, and as a treat went to the cinema every Friday.
Grand Duke Kirill's family stayed in Finland until May 1920.
Family

The family eventually left Finland and headed first to Coburg and then to Saint-Briac, France.
Kira was born Princess Kira Kirillovna of Russia, but her father later gave her illegally the title "Grand Duchess" when he declared himself Guardian of the Throne in 1924.
Dowager Empress Maria Feodorovna openly mocked Kirill's pretension.
Blonde-haired, blue-eyed Kira, high-spirited and straightforward also had an even temper.
Kira also frequently visited her cousins at various royal courts or attended house parties in the United Kingdom.
Princess Kira had some difficulty finding a suitable husband.
She was interested in the hemophiliac Alfonso, Prince of Asturias, son of Alfonso XIII of Spain, but was disappointed when the prince showed more interest in one of the daughters of Prince Nicholas of Greece.
Later, she was fond of Prince Constantine "Teddy" Soutzo, a Romanian aristocrat.
Finally, Kira married Prince Louis Ferdinand of Prussia in 1938.
After World War II

Kira was called upon to testify in the case of Anna Anderson, the woman who claimed to be Grand Duchess Anastasia Nikolaevna of Russia.
Kira had met Anderson briefly in 1952 at the urging of her mother-in-law, Crown Princess Cecilie of Prussia, who believed Anderson's claim.
Kira was not convinced.
Kira had last seen Anastasia when she was a child of seven.
Kira's uncle, Grand Duke Andrei Vladimirovich of Russia had been convinced Anderson was Anastasia, but her father and mother were unconvinced by Anderson's claim.
In later years, Kira was disappointed when her eldest son, Friedrich Wilhelm, renounced his rights to the title and married a commoner.
She was in good spirits on a visit to her brother Grand Duke Vladimir of Russia at Saint-Briac in September 1967, where she ate well and dumped several spoonfuls of sugar into her coffee, commenting, "God forbid I should eat anything healthy!"



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
  AssignClass (00071db3-a40d-4235-ac13-115555dd0139)
 Call ID: 00071db3-a40d-4235-ac13-115555dd0139
  Args:
    type: :Woman
    source: Kira_Kirillovna_of_Russia
  AssignClass (46c52bc3-4410-419a-8174-d92e672f0001)
 Call ID: 46c52bc3-4410-419a-8174-d92e672f0001
  Args:
    type: :Person
    source: Kira_Kirillovna_of_Russia
  AddLiteral (688b5079-d45e-4528-86da-19e5eae15734)
 Call ID: 688b5079-d45e-4528-86da-19e5eae15734
  Args:
    literal_value: 1909
    source: Kira_Kirillovna_of_Russia
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (43f99164-8c55-42cb-adf8-bb21ce0124f4)
 Call ID: 43f99164-8c55-42cb-adf8-bb21ce0124f4
  Args:
    literal_value: 1967
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: Kira_Kirillovna_of_Russia
  AssignClass (7f00cf81-d70d-49ef-b6c6-75eda57123cf)
 Call ID: 7f00cf81-d70d-49ef-b6c6-75eda57123cf
  Args:
    type: :Man
    source: Kirill_Vladimirovich_of_Russia
  AssignClass (72a013e2-9032-480d-819d-f900da94c1a0)
 Call ID: 72a013e2-9032-480d-819d-f900da94c1a0
  Args:
    type: :Ancestor
    source: Kirill_Vladimirovich_of_Russia
  AssignClass (098d3db7-7cc1-4ce6-91f0-06807f958c4c)
 Call ID: 098d3db7-7cc1-4ce6-91f0-06807f958c4c
  Args:
    type: :Woman
    source: Victoria_Melita_of_Saxe-Coburg_and_Gotha
  AssignClass (8ba95c2d-1710-4eb5-bae8-5d11ccd905c3)
 Call ID: 8ba95c2d-1710-4eb5-bae8-5d11ccd905c3
  Args:
    type: :Ancestor
    source: Victoria_Melita_of_Saxe-Coburg_and_Gotha
  AddTriple (828423af-d882-4eed-aea8-00ba66f0afb4)
 Call ID: 828423af-d882-4eed-aea8-00ba66f0afb4
  Args:
    relation: :hasFather
    source: Kira_Kirillovna_of_Russia
    target: Kirill_Vladimirovich_of_Russia
  AddTriple (e0004767-1582-4f85-ba4e-cd5a80e66701)
 Call ID: e0004767-1582-4f85-ba4e-cd5a80e66701
  Args:
    target: Victoria_Melita_of_Saxe-Coburg_and_Gotha
    relation: :hasMother
    source: Kira_Kirillovna_of_Russia
  AssignClass (84d588e9-343f-44b8-99df-edf78338fc24)
 Call ID: 84d588e9-343f-44b8-99df-edf78338fc24
  Args:
    type: :Man
    source: Louis_Ferdinand_of_Prussia
  AddTriple (7ed1e987-fb9e-47ff-91cd-6695d4692239)
 Call ID: 7ed1e987-fb9e-47ff-91cd-6695d4692239
  Args:
    target: Louis_Ferdinand_of_Prussia
    relation: :hasRelation
    source: Kira_Kirillovna_of_Russia
  AddLiteral (a8379145-6e29-4c3c-b09a-f5d8044a0153)
 Call ID: a8379145-6e29-4c3c-b09a-f5d8044a0153
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    source: Kira_Kirillovna_of_Russia
    literal_value: 1938
  AssignClass (4e39b19a-9610-40b0-be9d-35a899c0b593)
 Call ID: 4e39b19a-9610-40b0-be9d-35a899c0b593
  Args:
    type: :Woman
    source: Maria_of_Russia
  AddTriple (01b1e812-f783-48b9-8c2b-772147096d06)
 Call ID: 01b1e812-f783-48b9-8c2b-772147096d06
  Args:
    target: Maria_of_Russia
    source: Kira_Kirillovna_of_Russia
    relation: :hasSister
  AssignClass (9e1988bb-253a-4018-a613-0c6cd507a73d)
 Call ID: 9e1988bb-253a-4018-a613-0c6cd507a73d
  Args:
    type: :Man
    source: Vladimir_of_Russia
  AddTriple (cd27f4b8-cfa2-46b6-b044-2abb745f09a1)
 Call ID: cd27f4b8-cfa2-46b6-b044-2abb745f09a1
  Args:
    relation: :hasBrother
    source: Kira_Kirillovna_of_Russia
    target: Vladimir_of_Russia
  AssignClass (64bf7f57-fca6-411d-9a7b-d44c2377d242)
 Call ID: 64bf7f57-fca6-411d-9a7b-d44c2377d242
  Args:
    type: :Man
    source: Friedrich_Wilhelm_of_Prussia
  AddTriple (9703d77f-8f21-484c-9292-4162ec957076)
 Call ID: 9703d77f-8f21-484c-9292-4162ec957076
  Args:
    target: Friedrich_Wilhelm_of_Prussia
    relation: :hasSon
    source: Kira_Kirillovna_of_Russia
  Finish (b464b3de-1648-4e5b-b34d-eb40cd868513)
 Call ID: b464b3de-1648-4e5b-b34d-eb40cd868513
  Args: