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
Prince Philippe, Duke of Orléans (French: Louis Philippe Robert; 6 February 1869 – 28 March 1926) was the Orléanist pretender to the throne of France from 1894 to 1926 as Philippe VIII.
Early life

Philippe was born at York House, Twickenham, near London, the son of Philippe, Count of Paris, by his wife (and first cousin), Princess Isabelle of Orléans.
He was baptised with the names Louis-Philippe-Robert, and was called Philippe.
His family lived in the United Kingdom from the abdication and banishment of his great-grandfather Louis Philippe I, King of the French, in 1848, and returned to France in 1871 following the fall of the Second French Empire.
However, they again took refuge in England in 1886, when the French Republic exiled them following the wedding in Paris of Philippe's sister Amélie of Orléans to Crown Prince Carlos of Portugal.
Returning therefore to France in 1871 with his parents, Philippe was educated at home at the Château d'Eu and at the Collège Stanislas de Paris.
In 1880 Philippe's father granted him the title Duc d'Orléans.
Military career

Philippe began his military education at the École spéciale militaire de Saint-Cyr.
In October 1889, Philippe went to Switzerland to complete a course in military theory.
While there he fathered a son, Philippe Debien, by Nina, an actress working in the casino at Lausanne.
Drawn to explore the "unknown", Philippe asked Prince George, Duke of Cambridge, to send him to a military post in the Himalayas.
While in the East, he undertook a hunting and exploratory expedition in Nepal with his cousin Prince Henri of Orléans, went mountain-climbing in Tibet, and visited Afghanistan, Ceylon, and the Persian Gulf, before being posted back to Britain.
Prior to his imprisonment in France, Philippe had been unofficially engaged to his first cousin Princess Marguerite of Orléans, but the engagement was cancelled when Philippe's involvement with the Australian opera singer Nellie Melba was revealed.
Armstrong filed for divorce from Melba on the grounds of adultery, naming Philippe as co-respondent; the case was eventually dropped.
In September 1890, Philippe accompanied his father on a two-month trip to the United States and Canada.
On 12 November 1890, while in Philadelphia, Philippe joined the Pennsylvania Commandery of the Military Order of the Loyal Legion of the United States (MOLLUS) - a military society composed of officers who had served the Union in the American Civil War and their descendants - by right of his father's service in the Union Army.
In December 1890, Philippe applied unsuccessfully to serve in the Russian Army.
In March 1894, Philippe went to Egypt and Palestine with his sister Hélène, Duchess of Aosta.
Claimant to the defunct throne

Upon the death of his father on 8 September 1894, Philippe became the Orléanist claimant to the defunct French throne.
He was known to monarchists as Philippe VIII.
In October 1895, Philippe was named as co-respondent in the divorce case of Woolston v. Woolston.
Unlike his great grandfather, Louis Philippe I, Philippe claimed grand mastership of the Order of the Holy Spirit as intrinsic to his dynastic claim to the throne, and sometimes wore the breast star of the order.
On 5 November 1896, in Vienna, Philippe married Archduchess Maria Dorothea of Austria (1867–1932), a daughter of Archduke Joseph Karl of Austria, Palatine of Hungary, and granddaughter of Princess Clémentine of Orléans, as well as a niece of Marie Henriette of Austria, Queen Consort of the Belgians.
While travelling in Geneva in 1898, Philippe narrowly missed being assassinated by Luigi Lucheni, an anarchist, who vowed to kill the next member of a royal family that he saw.
He explored parts of the northeastern coast of Greenland, Denmark, in 1905 during his Duke of Orléans Arctic Expedition on ship Belgica.
Philippe continued to reside in the United Kingdom until 1912, when he moved his primary residence to Belgium.
In 1914, Philippe and his wife Maria Dorothea were legally separated.
At the outbreak of the First World War, Philippe again tried unsuccessfully to join the French army.
In 1926, Philippe died of pneumonia at the Palais d'Orléans in Palermo, Sicily, Italy.
Having no legitimate issue, he was succeeded as pretender to the defunct throne of France by his cousin and brother in law, Jean, Duke of Guise.
Publications

Philippe wrote a number of works based on his many travels: 


He also published a collection of the papers of his father and of the Henri, comte de Chambord:
Honours

In popular culture

Duke Philippe of Orleans briefly appears in an urban fantasy novel for children, The Master Key (1901) by L. Frank Baum.



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
  AssignClass (93248aae-c3bb-4ff4-82b8-f3ac26ce740e)
 Call ID: 93248aae-c3bb-4ff4-82b8-f3ac26ce740e
  Args:
    type: :Man
    source: Philippe_Duke_of_Orleans
  AssignClass (9ecb4502-6d17-4633-be4d-02e1d4b05913)
 Call ID: 9ecb4502-6d17-4633-be4d-02e1d4b05913
  Args:
    type: :Person
    source: Philippe_Duke_of_Orleans
  AddLiteral (aad96a7b-5512-47b6-837f-d1a7f40874a1)
 Call ID: aad96a7b-5512-47b6-837f-d1a7f40874a1
  Args:
    literal_value: 1869
    source: Philippe_Duke_of_Orleans
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (605fc61f-bd93-498b-897f-cf913c90ce6e)
 Call ID: 605fc61f-bd93-498b-897f-cf913c90ce6e
  Args:
    literal_value: 1926
    source: Philippe_Duke_of_Orleans
    relation: :hasDeathYear
    literal_type: xsd:integer
  AssignClass (945b2470-8712-47d3-9007-9887ecf79e83)
 Call ID: 945b2470-8712-47d3-9007-9887ecf79e83
  Args:
    type: :Man
    source: Philippe_Count_of_Paris
  AssignClass (bb68dbde-572d-44a0-969a-2594bbaf44e4)
 Call ID: bb68dbde-572d-44a0-969a-2594bbaf44e4
  Args:
    type: :Person
    source: Philippe_Count_of_Paris
  AddTriple (10cd3972-c062-472d-9ae7-f66876abe798)
 Call ID: 10cd3972-c062-472d-9ae7-f66876abe798
  Args:
    relation: :hasFather
    source: Philippe_Duke_of_Orleans
    target: Philippe_Count_of_Paris
  AssignClass (c92594e5-26d5-4001-8756-3a7f49b3837a)
 Call ID: c92594e5-26d5-4001-8756-3a7f49b3837a
  Args:
    type: :Woman
    source: Isabelle_of_Orleans
  AssignClass (2d27034f-7167-4b07-a427-4b0a3ab6dd61)
 Call ID: 2d27034f-7167-4b07-a427-4b0a3ab6dd61
  Args:
    source: Isabelle_of_Orleans
    type: :Person
  AddTriple (5840fbfa-4505-4a13-843f-1ded444d9132)
 Call ID: 5840fbfa-4505-4a13-843f-1ded444d9132
  Args:
    target: Isabelle_of_Orleans
    source: Philippe_Duke_of_Orleans
    relation: :hasMother
  AddTriple (7869efea-6d8c-4ded-bc92-101b507526ec)
 Call ID: 7869efea-6d8c-4ded-bc92-101b507526ec
  Args:
    target: Louis_Philippe_I
    relation: :hasFather
    source: Philippe_Count_of_Paris
  AssignClass (2efe78da-a295-45db-8849-c5f1eaa57415)
 Call ID: 2efe78da-a295-45db-8849-c5f1eaa57415
  Args:
    source: Louis_Philippe_I
    type: :Man
  AssignClass (7c27dfef-6060-42af-be51-25c793b5df60)
 Call ID: 7c27dfef-6060-42af-be51-25c793b5df60
  Args:
    type: :Person
    source: Louis_Philippe_I
  AssignClass (45b2e9fc-f6b3-4d54-bc00-6ab0fe464e70)
 Call ID: 45b2e9fc-f6b3-4d54-bc00-6ab0fe464e70
  Args:
    type: :Woman
    source: Amelie_of_Orleans
  AssignClass (70b5d6bd-c1c5-4985-918e-8d72f0e5f91f)
 Call ID: 70b5d6bd-c1c5-4985-918e-8d72f0e5f91f
  Args:
    source: Amelie_of_Orleans
    type: :Person
  AddTriple (00eb4e19-946f-426e-b257-3c3a807115b7)
 Call ID: 00eb4e19-946f-426e-b257-3c3a807115b7
  Args:
    target: Amelie_of_Orleans
    relation: :hasSister
    source: Philippe_Duke_of_Orleans
  AssignClass (63d3309a-855a-4882-81e7-d82a92765095)
 Call ID: 63d3309a-855a-4882-81e7-d82a92765095
  Args:
    type: :Man
    source: Philippe_Debien
  AssignClass (08e361f3-5fef-4d06-a3ef-2727053c7dc8)
 Call ID: 08e361f3-5fef-4d06-a3ef-2727053c7dc8
  Args:
    source: Philippe_Debien
    type: :Person
  AddTriple (ad1fcb26-0f27-4fcf-8b37-22536b35b289)
 Call ID: ad1fcb26-0f27-4fcf-8b37-22536b35b289
  Args:
    target: Philippe_Debien
    source: Philippe_Duke_of_Orleans
    relation: :hasSon
  AssignClass (1a9499c6-019a-456a-8d12-2babd454f549)
 Call ID: 1a9499c6-019a-456a-8d12-2babd454f549
  Args:
    type: :Woman
    source: Nina
  AssignClass (e0a8a3cb-59c1-4641-a873-f8dedc187463)
 Call ID: e0a8a3cb-59c1-4641-a873-f8dedc187463
  Args:
    type: :Person
    source: Nina
  AddTriple (3e6deb1c-c2e1-495d-8d65-307da45f1a94)
 Call ID: 3e6deb1c-c2e1-495d-8d65-307da45f1a94
  Args:
    source: Philippe_Debien
    relation: :hasMother
    target: Nina
  AssignClass (91537f3b-a318-4c7b-b140-10ce2610ef9b)
 Call ID: 91537f3b-a318-4c7b-b140-10ce2610ef9b
  Args:
    source: Helene_Duchess_of_Aosta
    type: :Woman
  AssignClass (b226f598-86d1-4385-a306-1b50a2fe940e)
 Call ID: b226f598-86d1-4385-a306-1b50a2fe940e
  Args:
    source: Helene_Duchess_of_Aosta
    type: :Person
  AddTriple (83f7159b-5591-4cd1-bc3d-255a5cc2fdb6)
 Call ID: 83f7159b-5591-4cd1-bc3d-255a5cc2fdb6
  Args:
    target: Helene_Duchess_of_Aosta
    relation: :hasSister
    source: Philippe_Duke_of_Orleans
  AssignClass (9323b1dd-0643-4935-a73c-b2c904bfd659)
 Call ID: 9323b1dd-0643-4935-a73c-b2c904bfd659
  Args:
    source: Maria_Dorothea_of_Austria
    type: :Woman
  AssignClass (7a1b64c7-3f99-4109-8a58-9416b6055aec)
 Call ID: 7a1b64c7-3f99-4109-8a58-9416b6055aec
  Args:
    source: Maria_Dorothea_of_Austria
    type: :Person
  AddLiteral (302a270d-795f-49a2-a3f3-60e5af78bdee)
 Call ID: 302a270d-795f-49a2-a3f3-60e5af78bdee
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    source: Philippe_Duke_of_Orleans
    literal_value: 1896
  AddTriple (7a148b25-5436-49eb-9484-21ecbc6fb7fd)
 Call ID: 7a148b25-5436-49eb-9484-21ecbc6fb7fd
  Args:
    relation: :hasRelation
    source: Philippe_Duke_of_Orleans
    target: Maria_Dorothea_of_Austria
  AssignClass (7d8ccfa2-0b3f-4bf4-b7f6-2b5009c233d7)
 Call ID: 7d8ccfa2-0b3f-4bf4-b7f6-2b5009c233d7
  Args:
    type: :Man
    source: Joseph_Karl_of_Austria
  AssignClass (43a48dca-9969-4cef-9b99-8ec176fc2f87)
 Call ID: 43a48dca-9969-4cef-9b99-8ec176fc2f87
  Args:
    source: Joseph_Karl_of_Austria
    type: :Person
  AddTriple (8bb56aa4-4121-4c71-93c9-77aa182bf630)
 Call ID: 8bb56aa4-4121-4c71-93c9-77aa182bf630
  Args:
    target: Joseph_Karl_of_Austria
    source: Maria_Dorothea_of_Austria
    relation: :hasFather
  AssignClass (4a9117da-04bf-4c70-999f-0c2bfe546664)
 Call ID: 4a9117da-04bf-4c70-999f-0c2bfe546664
  Args:
    source: Clementine_of_Orleans
    type: :Woman
  AssignClass (716a9aac-0c79-49bc-a5a6-44e8a20e11e9)
 Call ID: 716a9aac-0c79-49bc-a5a6-44e8a20e11e9
  Args:
    source: Clementine_of_Orleans
    type: :Person
  AddTriple (4552f195-255d-4ff6-9431-c2ca86827d64)
 Call ID: 4552f195-255d-4ff6-9431-c2ca86827d64
  Args:
    target: Clementine_of_Orleans
    source: Maria_Dorothea_of_Austria
    relation: :hasMother
  AssignClass (1ddc1ec7-dede-43b6-a02a-d2a3a1a1b792)
 Call ID: 1ddc1ec7-dede-43b6-a02a-d2a3a1a1b792
  Args:
    type: :Man
    source: Jean_Duke_of_Guise
  AssignClass (4dd733c9-39a7-4cb9-a984-c46b9fcea001)
 Call ID: 4dd733c9-39a7-4cb9-a984-c46b9fcea001
  Args:
    source: Jean_Duke_of_Guise
    type: :Person
  AddTriple (fe860ec3-1625-4437-b63d-4615d7108827)
 Call ID: fe860ec3-1625-4437-b63d-4615d7108827
  Args:
    target: Jean_Duke_of_Guise
    source: Philippe_Duke_of_Orleans
    relation: :isSiblingOf
  Finish (3d67998e-399c-42b2-84a6-646d19db1ccc)
 Call ID: 3d67998e-399c-42b2-84a6-646d19db1ccc
  Args: