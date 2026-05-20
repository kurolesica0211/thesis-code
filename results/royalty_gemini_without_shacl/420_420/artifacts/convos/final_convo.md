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
Prince Nikolai Kirillovich Romanov   Princess Yekaterina Fyodorovna


Prince Karl Emich of Leiningen (German: Karl Emich Nikolaus Friedrich Hermann Prinz zu Leiningen; Russian: Карл Эмих Николаус Фридрих Герман цу Лейнинген; born 12 June 1952), also known by his Orthodox Russian name Nikolai Kirillovich Romanov (Николай Кириллович Романов), and recognized with the regnal name Emperor Nicholas III by Monarchist Party supporters of the Imperial Throne, is the eldest son of Emich, 7th Prince of Leiningen, and Duchess Eilika of the Grand Duchy of Oldenburg, and is an elder brother of Andreas, 8th Prince of Leiningen.
He is a claimant to the defunct throne of the Russian Empire, held until 1917 by the Imperial House of Romanov, as a grandson of Grand Duchess Maria Kirillovna (1907–1951), eldest child of Grand Duke Kirill Vladimirovich, who claimed the Russian crown from exile in 1924.
He is a great-great-great-grandson of Emperor Alexander II of Russia and grandnephew of Grand Duke Vladimir Kirillovich of Russia.
In 2013, the Monarchist Party of Russia declared him the primary heir to the Russian throne upon his conversion from Lutheranism to Eastern Orthodox Christianity, and in 2014 announced the formation of the Imperial Throne, wherein Karl Emich had agreed to assume imperial dignity as Emperor Nicholas III.
As such, however, he came into competition with the widely recognized pretender to the throne, Grand Duchess Maria Vladimirovna of Russia, who is recognized by the Patriarch of Moscow.
He also claimed the headship of the House of Leiningen in the past.
He had one daughter by this marriage, Princess Cécilia Marie Stephanie Margarita of Leiningen (born 10 June 1988).
On 24 May 1991, Prince Karl Emich married morganatically Gabriele Renate Thyssen.
After an inheritance dispute, he desisted claim to the family's legacy in favour of his younger brother Andreas, 8th Prince of Leiningen.
The couple had one daughter, Princess Theresa Anna Elisabeth of Leiningen (born 16 April 1992)
In 1998, Karl Emich and Gabriele were divorced and she became the second wife of the Aga Khan IV.
On 12 April 2010, they had a son, Prince Emich Albrecht Karl of Leiningen.
Because his marriage to Countess Isabelle would not have been deemed equal according to the Pauline Laws, their son, Prince Emich, though considered a dynast of the House of Leiningen, cannot inherit his claim to the headship of the House of Romanov, which shall pass to his brother, Prince Andreas (b. 1955 ), and the latter's descendants born of equal marriages upon the death of Karl Emich, and on the condition that they should convert to Orthodoxy.
Lawsuit


In 2000, Karl Emich began the final round of a lawsuit to inherit £100 million worth of castles, property, and a Mediterranean island that had been denied him by his family because he chose to marry Gabriele Renate Thyssen.
Karl Emich was disinherited shortly after his 1991 wedding, as his mother, father, and brother Andreas withheld approval, contending that the bride did not meet the mediatized family's traditional standard for aristocratic lineage.
The marriage was therefore deemed to constitute a violation of an 1897 Leiningen family edict requiring that dynastically valid marriages be authorised by the head of the Leiningen family (or by successful appeal to a panel of mediatized nobles), such permission historically being granted for brides descended from royalty or the titled nobility.
Karl remarked about the whole affair, 

"From the very beginning of our marriage I was turned into an enemy.
Karl Emich maintained that the stress this feud put upon his marriage is the reason why Thyssen left him, converted to Islam, and eloped with Aga Khan IV.
Claim to the Russian throne

Karl Emich and his supporters argue that the marriage of Maria Vladimirovna's parents was in contravention of the Pauline Laws.
They maintain that the House of Bagration-Mukhrani did not possess sovereign status and was not recognized as equal by Nicholas II for the purpose of dynastic marriages at the time of the union of Princess Tatiana Constantinovna of Russia and Prince Constantine Bagration-Mukhransky in 1911, thirty seven years prior to that of Princess Leonida and Grand Duke Vladimir Kirillovich.
Therefore, as the next of kin to Vladimir (in the exclusion of his daughter), the Russian Monarchist Party recognises Karl Emich as the heir to the Russian throne, since he and his wife converted on 1 June 2013, from Lutheranism to Eastern Orthodox Christianity, enabling his accession.
The couple received Orthodox names of Nikolai Kirillovich and Yekaterina Fyodorovna.


Nicholas III and the Imperial Throne

In early 2014 Russian Monarchist Party leader Anton Bakov announced he views the "Imperial Throne" from the point of international law as a subject of state sovereignty regardless of any other attributes, referring to analogies with the Holy See.
He outlined that Karl Emich, upon adhering to the Orthodox denomination, obtained a right to take this see according to pre-Revolution Fundamental Laws of the Russian Empire.
Bakov proposed that the Prince accept the throne, thereby forming a new independent state and incorporate it into Bakov's promotional projects such as the Monarchist Party's Imperial Throne micronation and several others.
In April 2014 Bakov and Karl Emich appeared in a newspaper textual and photo report declaring that the Prince accepted the proposals as well as the title of "Emperor Nicholas III" (as successor to Nicholas II).
In the report Bakov emphasized that Karl Emich has long been an entrepreneur but henceforth he would refrain from all non-royalist related public activities.
He also announced that Russian President Vladimir Putin declined to grant such a plot in Yekaterinburg (Bakov's residence and site of the 1918 Romanov assassination) in response to Karl Emich's request, transmitted to Putin by Bakov, a former MP.
In June 2021 Karl Emich, or Nikolai Kirillovich (Nicholas III) gave his first-ever interview in Russian language where he clarified his civil and political attitude and told some details about history of his family.



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
  AssignClass (c7212d3a-dc37-4eef-a0a2-9a8118506f4f)
 Call ID: c7212d3a-dc37-4eef-a0a2-9a8118506f4f
  Args:
    type: :Man
    source: Karl_Emich_of_Leiningen
  AssignClass (1a54c279-069d-4f19-bd65-7c6112300087)
 Call ID: 1a54c279-069d-4f19-bd65-7c6112300087
  Args:
    source: Karl_Emich_of_Leiningen
    type: :Person
  AddLiteral (37b45bdd-49e3-4249-b7e3-7d55d80baaba)
 Call ID: 37b45bdd-49e3-4249-b7e3-7d55d80baaba
  Args:
    source: Karl_Emich_of_Leiningen
    relation: :alsoKnownAs
    literal_value: Nikolai Kirillovich Romanov
    literal_type: xsd:string
  AddLiteral (7ecb8ee4-7ea3-46f1-9b8d-2741f25a5adb)
 Call ID: 7ecb8ee4-7ea3-46f1-9b8d-2741f25a5adb
  Args:
    literal_type: xsd:integer
    source: Karl_Emich_of_Leiningen
    literal_value: 1952
    relation: :hasBirthYear
  AssignClass (70296a8b-779f-469d-a2b6-e12f42463014)
 Call ID: 70296a8b-779f-469d-a2b6-e12f42463014
  Args:
    source: Emich_7th_Prince_of_Leiningen
    type: :Man
  AssignClass (618eef59-7cff-48a8-a61f-c20af2f8da67)
 Call ID: 618eef59-7cff-48a8-a61f-c20af2f8da67
  Args:
    source: Emich_7th_Prince_of_Leiningen
    type: :Person
  AssignClass (f8419237-1296-4544-8bac-afb6a11a0bd3)
 Call ID: f8419237-1296-4544-8bac-afb6a11a0bd3
  Args:
    source: Duchess_Eilika_of_Oldenburg
    type: :Woman
  AssignClass (10d42bb7-700d-4c47-9eb4-6509660cb646)
 Call ID: 10d42bb7-700d-4c47-9eb4-6509660cb646
  Args:
    source: Duchess_Eilika_of_Oldenburg
    type: :Person
  AddTriple (e0406864-47a6-4f6b-b08c-35c7ee34bb2b)
 Call ID: e0406864-47a6-4f6b-b08c-35c7ee34bb2b
  Args:
    source: Karl_Emich_of_Leiningen
    relation: :hasFather
    target: Emich_7th_Prince_of_Leiningen
  AddTriple (9b969ce9-f15b-4b11-a752-bc323b0b4f8a)
 Call ID: 9b969ce9-f15b-4b11-a752-bc323b0b4f8a
  Args:
    target: Duchess_Eilika_of_Oldenburg
    source: Karl_Emich_of_Leiningen
    relation: :hasMother
  AssignClass (a751fb2b-5a7e-4093-8b17-4a2d43879193)
 Call ID: a751fb2b-5a7e-4093-8b17-4a2d43879193
  Args:
    source: Andreas_8th_Prince_of_Leiningen
    type: :Man
  AssignClass (0d446c3e-cea8-443c-a420-c6b97a928277)
 Call ID: 0d446c3e-cea8-443c-a420-c6b97a928277
  Args:
    source: Andreas_8th_Prince_of_Leiningen
    type: :Person
  AddTriple (0a70d977-fbe8-4a37-9d4d-4a4e129099da)
 Call ID: 0a70d977-fbe8-4a37-9d4d-4a4e129099da
  Args:
    relation: :hasBrother
    source: Karl_Emich_of_Leiningen
    target: Andreas_8th_Prince_of_Leiningen
  AssignClass (4d3030b4-7b44-49de-8f35-801f2f17e06d)
 Call ID: 4d3030b4-7b44-49de-8f35-801f2f17e06d
  Args:
    source: Princess_Cecilia_Marie_Stephanie_Margarita_of_Leiningen
    type: :Woman
  AssignClass (0745c6b7-1a7c-4bc7-a8c4-0f855a278ad8)
 Call ID: 0745c6b7-1a7c-4bc7-a8c4-0f855a278ad8
  Args:
    type: :Person
    source: Princess_Cecilia_Marie_Stephanie_Margarita_of_Leiningen
  AddTriple (a180f8cd-5d62-4e17-8a48-225a1d1f3da7)
 Call ID: a180f8cd-5d62-4e17-8a48-225a1d1f3da7
  Args:
    target: Princess_Cecilia_Marie_Stephanie_Margarita_of_Leiningen
    source: Karl_Emich_of_Leiningen
    relation: :hasDaughter
  AssignClass (8d885b54-b299-4ab7-89cc-771c777bb4f8)
 Call ID: 8d885b54-b299-4ab7-89cc-771c777bb4f8
  Args:
    source: Gabriele_Renate_Thyssen
    type: :Woman
  AssignClass (620d0251-b8f9-4a4a-8ad7-4f093f0549a0)
 Call ID: 620d0251-b8f9-4a4a-8ad7-4f093f0549a0
  Args:
    source: Gabriele_Renate_Thyssen
    type: :Person
  AssignClass (c503cfd9-1096-43af-95fb-6f67f669ea16)
 Call ID: c503cfd9-1096-43af-95fb-6f67f669ea16
  Args:
    source: Princess_Theresa_Anna_Elisabeth_of_Leiningen
    type: :Woman
  AssignClass (3a14fffd-d3c1-4baa-af52-3037e75e6504)
 Call ID: 3a14fffd-d3c1-4baa-af52-3037e75e6504
  Args:
    source: Princess_Theresa_Anna_Elisabeth_of_Leiningen
    type: :Person
  AddTriple (2ecc0bee-a5c7-4c09-b60d-0574712cf0b2)
 Call ID: 2ecc0bee-a5c7-4c09-b60d-0574712cf0b2
  Args:
    target: Princess_Theresa_Anna_Elisabeth_of_Leiningen
    source: Karl_Emich_of_Leiningen
    relation: :hasDaughter
  AddTriple (a3fe685d-0e4d-4f91-b4ed-e6d95b2021d0)
 Call ID: a3fe685d-0e4d-4f91-b4ed-e6d95b2021d0
  Args:
    source: Princess_Theresa_Anna_Elisabeth_of_Leiningen
    relation: :hasMother
    target: Gabriele_Renate_Thyssen
  AssignClass (6f50bcfd-e620-4531-ac3b-ecc7f3304d75)
 Call ID: 6f50bcfd-e620-4531-ac3b-ecc7f3304d75
  Args:
    type: :Man
    source: Prince_Emich_Albrecht_Karl_of_Leiningen
  AssignClass (f538bc55-8224-42d0-bbb0-e70c93147721)
 Call ID: f538bc55-8224-42d0-bbb0-e70c93147721
  Args:
    type: :Person
    source: Prince_Emich_Albrecht_Karl_of_Leiningen
  AddTriple (bc3d4475-505b-4fb8-8163-259f5fd23ed5)
 Call ID: bc3d4475-505b-4fb8-8163-259f5fd23ed5
  Args:
    target: Prince_Emich_Albrecht_Karl_of_Leiningen
    source: Karl_Emich_of_Leiningen
    relation: :hasSon
  AddTriple (42612fcb-3700-4f19-917d-8b19d0b8ec6b)
 Call ID: 42612fcb-3700-4f19-917d-8b19d0b8ec6b
  Args:
    target: Gabriele_Renate_Thyssen
    source: Prince_Emich_Albrecht_Karl_of_Leiningen
    relation: :hasMother
  Finish (009d2d60-f423-4851-be58-56d639916054)
 Call ID: 009d2d60-f423-4851-be58-56d639916054
  Args: