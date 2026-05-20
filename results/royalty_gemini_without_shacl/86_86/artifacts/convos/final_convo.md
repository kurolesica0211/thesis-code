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
Prince Aimone, 4th Duke of Aosta (Aimone Roberto Margherita Maria Giuseppe Torino; 9 March 1900 – 29 January 1948), was a prince of Italy's reigning House of Savoy and an officer of the Royal Italian Navy.
The second son of Prince Emanuele Filiberto, Duke of Aosta, he was granted the title Duke of Spoleto on 22 September 1904.
He inherited the title Duke of Aosta on 3 March 1942 following the death of his brother Prince Amedeo in a British prisoner of war camp in Nairobi.
From 18 May 1941 to 31 July 1943, Aimone was designated king of the Independent State of Croatia (Croatian: Nezavisna Država Hrvatska, NDH), even though he never ruled there.
After the dismissal of Mussolini on 25 July 1943, Aimone abdicated on 31 July as king on the orders of Victor Emmanuel III.
Early life

Prince Aimone Roberto Margherita Maria Giuseppe Torino of Savoy-Aosta was born in Turin the second son of Prince Emanuele Filiberto, Duke of Aosta (eldest son of Prince Amedeo, 1st Duke of Aosta (and sometime "King Amadeo I of Spain") by his wife, née Vittoria dal Pozzo, Principessa della Cisterna) and Princess Hélène of Orléans (daughter of Philippe, comte de Paris, and Princess Marie Isabelle of Orléans).
As his patrilinal great-grandfather was King Victor Emmanuel II of Italy, he was a member of the House of Savoy.
With his brother Amedeo, he was educated at St  David's College, Reigate, Surrey, England, and Aimone later went to study at the naval academy in Livorno.
On 1 April 1921, Prince Aimone became a member of the Italian Senate.
In 1929, twenty years after his uncle Prince Luigi Amedeo, Duke of the Abruzzi had attempted to climb K2 in Karakoram, Prince Aimone led an expedition to Karakorum.
Due to the failure to climb K2 twenty years earlier, Prince Aimone's expedition concentrated solely on scientific work.
Marriage and issue

After being romantically linked with Infanta Beatriz of Spain, the daughter of King Alfonso XIII, he married, on 1 July 1939 at the church of Santa Maria del Fiore, Florence, Princess Irene of Greece and Denmark, daughter of King Constantine I and Princess Sophie of Prussia.
They had one son, Prince Amedeo, Duke of Aosta, born in 1943.
Aimone was then officially named king by his cousin Victor Emmanuel III.
The Italian Foreign Minister and Benito Mussolini's son in law Count Ciano's informants said of Aimone "The Duke doesn't give a damn about Croatia and wants only money, money and more money."
Ciano's diary noted a conversation between Aimone and himself, where Aimone was "proud of having been chosen King of Croatia, but has no exact idea of what he is supposed to do and is vaguely uneasy about it".
Aimone felt that Dalmatia "was a land that could never be Italianized" and was an obstacle to Italo-Croatian reconciliation.
Prince Aimone also established a Croatian office in Rome where he received confidential reports, official documents, and military, political and economic information from Croatia.
After the fall of the Fascist regime in Italy, Aimone abdicated as king of Croatia on 31 July 1943 on the orders of Victor Emmanuel III.
Prince Aimone succeeded to the title duke of Aosta on 3 March 1942, following the death of his elder brother Prince Amedeo, 3rd Duke of Aosta, in a British prisoner of war camp in Kenya.
In the autumn of 1942, Aimone contacted Allied forces via his courier, the consul general Alessandro Marieni, about the possibility of a peace settlement between Italy and Allied forces.
Death

In 1947, following the birth of the Italian Republic the previous year, Prince Aimone left Italy for South America.
The claim to the Aosta ducal title passed to his son Prince Amedeo.
}} Media related to Prince Aimone, Duke of Aosta at Wikimedia Commons



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
  AssignClass (27bce1c5-92a2-4468-b4ba-64509dcd0140)
 Call ID: 27bce1c5-92a2-4468-b4ba-64509dcd0140
  Args:
    type: :Man
    source: Prince_Aimone_4th_Duke_of_Aosta
  AssignClass (ed56189d-ee40-4477-9753-3f8587100114)
 Call ID: ed56189d-ee40-4477-9753-3f8587100114
  Args:
    source: Prince_Emanuele_Filiberto_Duke_of_Aosta
    type: :Man
  AssignClass (1c4362fb-8e16-4cda-8eca-9a77538dd5ed)
 Call ID: 1c4362fb-8e16-4cda-8eca-9a77538dd5ed
  Args:
    type: :Man
    source: Prince_Amedeo_1st_Duke_of_Aosta
  AssignClass (9363641e-b72a-410d-951d-44df10e5d6ea)
 Call ID: 9363641e-b72a-410d-951d-44df10e5d6ea
  Args:
    source: Vittoria_dal_Pozzo
    type: :Woman
  AssignClass (f6de9fba-c51a-4637-ab82-22b26956360d)
 Call ID: f6de9fba-c51a-4637-ab82-22b26956360d
  Args:
    source: Princess_Helene_of_Orleans
    type: :Woman
  AssignClass (889f002a-6530-432c-bb63-f8adc1df097e)
 Call ID: 889f002a-6530-432c-bb63-f8adc1df097e
  Args:
    source: Philippe_comte_de_Paris
    type: :Man
  AssignClass (090bdea6-0f8c-41f5-9f90-128bd1f5c47b)
 Call ID: 090bdea6-0f8c-41f5-9f90-128bd1f5c47b
  Args:
    type: :Woman
    source: Princess_Marie_Isabelle_of_Orleans
  AssignClass (484952d8-0583-4c84-919e-58449f58dd61)
 Call ID: 484952d8-0583-4c84-919e-58449f58dd61
  Args:
    type: :Man
    source: King_Victor_Emmanuel_II_of_Italy
  AssignClass (a248f8dc-a9da-4dab-ac55-d7198c5ea309)
 Call ID: a248f8dc-a9da-4dab-ac55-d7198c5ea309
  Args:
    type: :Man
    source: Prince_Amedeo_3rd_Duke_of_Aosta
  AssignClass (0e1f3249-ab7e-484a-88da-c9baec1aa53e)
 Call ID: 0e1f3249-ab7e-484a-88da-c9baec1aa53e
  Args:
    type: :Woman
    source: Princess_Irene_of_Greece_and_Denmark
  AssignClass (32a4a4fb-3812-4878-bec3-d668d238011b)
 Call ID: 32a4a4fb-3812-4878-bec3-d668d238011b
  Args:
    source: King_Constantine_I
    type: :Man
  AssignClass (045fdad9-de5c-4476-9554-419d21247059)
 Call ID: 045fdad9-de5c-4476-9554-419d21247059
  Args:
    source: Princess_Sophie_of_Prussia
    type: :Woman
  AssignClass (19c0f2dd-dfac-43c0-89b1-6a2a8affc558)
 Call ID: 19c0f2dd-dfac-43c0-89b1-6a2a8affc558
  Args:
    type: :Man
    source: Prince_Amedeo_son_of_Aimone
  AddLiteral (7eea0ad1-ebb7-431c-96b7-151083926fec)
 Call ID: 7eea0ad1-ebb7-431c-96b7-151083926fec
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Prince_Aimone_4th_Duke_of_Aosta
    literal_value: 1900
  AddLiteral (6499b19b-c31c-47a6-b0c6-6dee74f0df5b)
 Call ID: 6499b19b-c31c-47a6-b0c6-6dee74f0df5b
  Args:
    literal_value: 1948
    source: Prince_Aimone_4th_Duke_of_Aosta
    relation: :hasDeathYear
    literal_type: xsd:integer
  AddTriple (676accb3-c60e-4c6f-b9de-7f59be70ddfb)
 Call ID: 676accb3-c60e-4c6f-b9de-7f59be70ddfb
  Args:
    target: Prince_Emanuele_Filiberto_Duke_of_Aosta
    relation: :hasFather
    source: Prince_Aimone_4th_Duke_of_Aosta
  AddTriple (b645b53c-769e-4265-95b4-fe60b2198fd2)
 Call ID: b645b53c-769e-4265-95b4-fe60b2198fd2
  Args:
    source: Prince_Aimone_4th_Duke_of_Aosta
    relation: :hasMother
    target: Princess_Helene_of_Orleans
  AddTriple (6c2a2978-f1f1-4f94-9f55-e1f24fd5ece3)
 Call ID: 6c2a2978-f1f1-4f94-9f55-e1f24fd5ece3
  Args:
    target: Prince_Amedeo_1st_Duke_of_Aosta
    source: Prince_Emanuele_Filiberto_Duke_of_Aosta
    relation: :hasFather
  AddTriple (cfa968c2-5a15-4b0e-b2b6-0e31737c63cf)
 Call ID: cfa968c2-5a15-4b0e-b2b6-0e31737c63cf
  Args:
    source: Prince_Emanuele_Filiberto_Duke_of_Aosta
    relation: :hasMother
    target: Vittoria_dal_Pozzo
  AddTriple (40582d6b-e0a1-4c31-b619-f0058c41a111)
 Call ID: 40582d6b-e0a1-4c31-b619-f0058c41a111
  Args:
    target: Philippe_comte_de_Paris
    relation: :hasFather
    source: Princess_Helene_of_Orleans
  AddTriple (f568fe65-0bb2-4bda-b755-538539a9eaed)
 Call ID: f568fe65-0bb2-4bda-b755-538539a9eaed
  Args:
    target: Princess_Marie_Isabelle_of_Orleans
    source: Princess_Helene_of_Orleans
    relation: :hasMother
  AddTriple (732ad8b7-eadb-4db4-8901-c673b85399e9)
 Call ID: 732ad8b7-eadb-4db4-8901-c673b85399e9
  Args:
    target: Prince_Amedeo_3rd_Duke_of_Aosta
    source: Prince_Aimone_4th_Duke_of_Aosta
    relation: :hasBrother
  AddTriple (6205b1e9-912d-4565-8c9a-316120e3cc4a)
 Call ID: 6205b1e9-912d-4565-8c9a-316120e3cc4a
  Args:
    target: Prince_Emanuele_Filiberto_Duke_of_Aosta
    source: Prince_Amedeo_3rd_Duke_of_Aosta
    relation: :hasFather
  AddTriple (ec9721f0-5439-46f9-8345-d90bf2c9da8e)
 Call ID: ec9721f0-5439-46f9-8345-d90bf2c9da8e
  Args:
    target: Princess_Helene_of_Orleans
    relation: :hasMother
    source: Prince_Amedeo_3rd_Duke_of_Aosta
  AddTriple (28803137-7b62-423e-a0bf-f0c61d49dbbb)
 Call ID: 28803137-7b62-423e-a0bf-f0c61d49dbbb
  Args:
    relation: :hasFather
    source: Prince_Aimone_4th_Duke_of_Aosta
    target: Prince_Amedeo_son_of_Aimone
  AddTriple (aff2063b-7330-429f-8a2b-bd2cd161ddc5)
 Call ID: aff2063b-7330-429f-8a2b-bd2cd161ddc5
  Args:
    target: Princess_Irene_of_Greece_and_Denmark
    source: Prince_Amedeo_son_of_Aimone
    relation: :hasMother
  AddTriple (0647fdee-0dcd-40b5-b5bb-faf86963ac81)
 Call ID: 0647fdee-0dcd-40b5-b5bb-faf86963ac81
  Args:
    source: Princess_Irene_of_Greece_and_Denmark
    relation: :hasFather
    target: King_Constantine_I
  AddTriple (1c9b7dce-c040-4b6e-b9e2-1fa4cc04e90f)
 Call ID: 1c9b7dce-c040-4b6e-b9e2-1fa4cc04e90f
  Args:
    source: Princess_Irene_of_Greece_and_Denmark
    relation: :hasMother
    target: Princess_Sophie_of_Prussia
  AddLiteral (f8457047-a8b6-4e26-b2f9-78f22e5343a3)
 Call ID: f8457047-a8b6-4e26-b2f9-78f22e5343a3
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    source: Prince_Aimone_4th_Duke_of_Aosta
    literal_value: 1939
  Finish (2d166103-c14f-4c51-9ea2-5a42449ed2c8)
 Call ID: 2d166103-c14f-4c51-9ea2-5a42449ed2c8
  Args: