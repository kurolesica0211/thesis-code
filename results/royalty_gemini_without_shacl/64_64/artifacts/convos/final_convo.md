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
Prince Andrew of Greece and Denmark (Greek: Ανδρέας, romanized: Andréas; 2 February  1882 – 3 December 1944) was the seventh child and fourth son of King George I and Queen Olga of Greece.
He was a grandson of King Christian IX of Denmark and the father of Prince Philip, Duke of Edinburgh.
He was a prince of Greece and Denmark, both by virtue of his patrilineal descent.
A career soldier, Andrew began military training at an early age, and was commissioned as an officer in the Greek army.
In 1913, his father was assassinated and Andrew's elder brother Constantine became king.
Constantine's neutrality policy during World War I led to his abdication, and most of the royal family, including Andrew, was exiled.
On their return a few years later, Andrew saw service as Major General in the Greco-Turkish War (1919–1922), but the war went badly for Greece, and Andrew was blamed, in part, for the loss of Greek territory.
He was exiled for a second time in 1922, and spent most of the rest of his life in France.
By 1930, Andrew was estranged from his wife, Princess Alice of Battenberg.
His only son, Philip, served in the British navy during World War II, while all four of his daughters were married to Germans, three of whom had Nazi connections.
Separated from his wife and son by the effects of the war, Andrew died in Monte Carlo in 1944.
Early life

Andrew was born on 2 February 1882 at the Tatoi Palace, just north of Athens.
He was the fourth son of George I of Greece and Olga Constantinovna of Russia.
A member of the House of Schleswig-Holstein-Sonderburg-Glücksburg, Andrew held the title of prince in both Greece and Denmark, as his father was a younger son of Christian IX of Denmark.
He was in the line of succession to the Greek throne.
In addition to his native Greek, Andrew learnt Danish, German, French, English, and Russian.
Despite his near-sightedness, Andrew joined the army as a cavalry officer in May 1901.
Marriage

In 1902, Andrew met Princess Alice of Battenberg during his stay in London on the occasion of the coronation of Edward VII, who was his uncle-by-marriage and her grand-uncle.
Princess Alice was a daughter of Prince Louis of Battenberg and Princess Victoria of Hesse and by Rhine, King Edward's niece.
They fell in love, and the following year, on 6 October 1903, Andrew married Alice in a civil wedding at Darmstadt.
Prince and Princess Andrew had five children, all of whom later had children of their own.
Early career

In 1909, the political situation in Greece led to a coup d'état, as the Athens government refused to support the Cretan parliament, which had called for the union of Crete (still nominally part of the Ottoman Empire) with the Greek mainland.
A group of dissatisfied officers formed a Greek nationalist Military League and demanded, among other reforms, the removal of royal princes from the army, which led to Andrew's resignation from the army and the rise to power of Eleftherios Venizelos.
A few years later, at the outbreak of the Balkan Wars in 1912, Andrew was reinstated in the army as a lieutenant colonel in the 3rd Cavalry Regiment, and placed in command of a field hospital.
During the war, his father was assassinated and Andrew inherited a villa on the island of Corfu, Mon Repos, as well as an annuity of £4,000.
In 1914, Andrew (like many European princes) held honorary military posts in both the German and Russian empires, as well as Prussian, Russian, Danish and Italian knighthoods.
During World War I, Andrew continued to visit Britain, despite veiled accusations in the British House of Commons that he was a German agent.
His brother, King Constantine, who was the Kaiser's brother-in-law, followed a neutrality policy, but the democratically elected government of Venizelos supported the Allies.
By June 1917, the King's neutrality policy had become so untenable that he abdicated and the Greek royal family were forced into exile.
For the next few years, most of the Greek royal family lived in Switzerland.
Exile from Greece

For three years, Constantine's second son, Alexander, was king of Greece, until his early death from an infection due to a monkey bite.
Constantine was restored to the throne, and Andrew was once again reinstated in the army, this time as a major-general.
Andrew was given command of the II Army Corps during the Battle of the Sakarya, which effectively halted the Greek advance in the Greco-Turkish War (1919–1922).
Andrew had little respect for his superior officers, whom he considered incompetent.
Refusing to put his men in undue danger (suffering lack of food and ammunition), Andrew followed his own battle plan, much to the dismay of the commanding general, Anastasios Papoulas.
Relieved of his chief of staff, and given a dressing-down by Papoulas, in September Andrew asked to be removed from command but Papoulas refused.
Andrew's troops were forced to retreat.
The Greek defeat in Asia Minor in August 1922 led to the 11 September 1922 Revolution, during which Andrew was arrested, court-martialed, and found guilty of "disobeying an order" and "acting on his own initiative" during the battle of the previous year.
British diplomats assumed that Andrew was also in mortal danger.
Andrew, though spared, was banished for life and his family fled into exile aboard a British cruiser, HMS Calypso.
The family settled at Saint-Cloud on the outskirts of Paris, in a small house lent to them by Andrew's wealthy sister-in-law, Princess George of Greece.
In 1930, Andrew published a book entitled Towards Disaster: The Greek Army in Asia Minor in 1921, in which he defended his actions during the Battle of the Sakarya, but he essentially lived a life of enforced retirement, despite only being in his forties.
Alice suffered a nervous breakdown and was institutionalised in Switzerland.
Their daughters married and settled in Germany, separated from Andrew, and Philip was sent to school in Britain, where he was brought up by his mother's British relatives.
Andrew went to live in the South of France.
On the French Riviera, Andrew lived in a small apartment, or hotel rooms, or on board a yacht with Countess Andrée de La Bigne.
His marriage to Alice was effectively over, and after her recovery and release, she returned to Greece.
In 1936, his sentence of exile was quashed by emergency laws, which also restored land and annuities to the King.
Andrew returned to Greece for a brief visit that May.
The following year, his pregnant daughter Cecilie, his son-in-law and two of his grandchildren were killed in an air accident at Ostend; he travelled to London to meet up with his sixteen-year-old son Prince Philip and they went together to Darmstadt where he met Alice for the first time in six years at the funeral.
During World War II, he found himself essentially trapped in Vichy France, while his son, Prince Philip, fought on the side of the British.
Andrew's three surviving sons-in-law fought on the German side: Prince Christoph of Hesse was a member of the Nazi Party and the Waffen-SS; Berthold, Margrave of Baden, was invalided out of the Wehrmacht in 1940 after an injury in France; Prince Gottfried of Hohenlohe-Langenburg served on the Eastern Front and was dismissed after the 20 July plot.
For five years, Andrew saw neither his wife nor his son.
Death and burial

Andrew died aged 62 in the closing months of the war in Europe on 3 December 1944 in the Hotel Metropole, Monte Carlo, of heart failure and arteriosclerosis.
He was at first buried in the Russian Orthodox church in Nice, but in 1946 his remains were transferred, by the Greek cruiser Averof, to the royal cemetery at Tatoi Palace, near Athens.
Prince Philip and then-private secretary, Mike Parker, travelled to Monte Carlo to collect items belonging to his father from Andrée de La Bigne; among these items: a signet ring which the Prince wore from then onwards, an ivory shaving brush he took to using, and some clothes that he had altered to fit him.
Andrew left to his only son seven-tenths of his estate, but he also left behind a debt of £17,500, leading Philip's maternal grandmother, Victoria Mountbatten, Marchioness of Milford Haven, to complain bitterly of the extravagance the Greek prince had been led into by his French mistress.



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
  AssignClass (f2b0f873-62ab-439b-be28-ca514e3f14af)
 Call ID: f2b0f873-62ab-439b-be28-ca514e3f14af
  Args:
    type: :Man
    source: Prince Andrew of Greece and Denmark
  AssignClass (5ab4931c-8117-4669-95d4-9239432a3b30)
 Call ID: 5ab4931c-8117-4669-95d4-9239432a3b30
  Args:
    source: King George I of Greece
    type: :Man
  AssignClass (f9fe5d82-a4ff-4f3c-a25b-c88a0bedcc40)
 Call ID: f9fe5d82-a4ff-4f3c-a25b-c88a0bedcc40
  Args:
    type: :Woman
    source: Queen Olga of Greece
  AssignClass (791b1503-a5b9-48a3-b755-28684c2c1b3e)
 Call ID: 791b1503-a5b9-48a3-b755-28684c2c1b3e
  Args:
    type: :Man
    source: King Christian IX of Denmark
  AssignClass (db04c37a-71f5-4520-883f-55a40ec1d6e1)
 Call ID: db04c37a-71f5-4520-883f-55a40ec1d6e1
  Args:
    source: Prince Philip
    type: :Man
  AssignClass (f46c2ef9-1325-4ca5-abe7-e9f99432e4fb)
 Call ID: f46c2ef9-1325-4ca5-abe7-e9f99432e4fb
  Args:
    source: Princess Alice of Battenberg
    type: :Woman
  AssignClass (8a4eb3a2-d3e0-45c5-b2a5-81073aab7e81)
 Call ID: 8a4eb3a2-d3e0-45c5-b2a5-81073aab7e81
  Args:
    source: King Constantine of Greece
    type: :Man
  AssignClass (e48201b6-50f7-46f0-be63-1a400cd06af9)
 Call ID: e48201b6-50f7-46f0-be63-1a400cd06af9
  Args:
    type: :Man
    source: Prince Louis of Battenberg
  AssignClass (1e3cd86b-f3bb-41d9-b36e-83b49723ddf6)
 Call ID: 1e3cd86b-f3bb-41d9-b36e-83b49723ddf6
  Args:
    type: :Woman
    source: Princess Victoria of Hesse and by Rhine
  AssignClass (64a3df94-320f-400c-a66e-f8e980419d3f)
 Call ID: 64a3df94-320f-400c-a66e-f8e980419d3f
  Args:
    type: :Man
    source: King Alexander of Greece
  AssignClass (66ec4bf4-3da3-4910-99b0-b7724864a13f)
 Call ID: 66ec4bf4-3da3-4910-99b0-b7724864a13f
  Args:
    type: :Woman
    source: Princess Cecilie
  AddLiteral (6625b386-6b99-4280-9c95-bb70592f66ed)
 Call ID: 6625b386-6b99-4280-9c95-bb70592f66ed
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Prince Andrew of Greece and Denmark
    literal_value: 1882
  AddLiteral (6aa27ff7-0c07-4a71-9bde-0439b96684ea)
 Call ID: 6aa27ff7-0c07-4a71-9bde-0439b96684ea
  Args:
    literal_value: 1944
    source: Prince Andrew of Greece and Denmark
    literal_type: xsd:integer
    relation: :hasDeathYear
  AddTriple (fbd424d8-ef3f-41f5-ac45-b84f09f47f15)
 Call ID: fbd424d8-ef3f-41f5-ac45-b84f09f47f15
  Args:
    target: King George I of Greece
    source: Prince Andrew of Greece and Denmark
    relation: :hasFather
  AddTriple (130c00d6-dcd0-414c-b589-8955fe38c538)
 Call ID: 130c00d6-dcd0-414c-b589-8955fe38c538
  Args:
    relation: :hasMother
    target: Queen Olga of Greece
    source: Prince Andrew of Greece and Denmark
  AddTriple (37cb74f6-ab50-415e-a09a-71a192f99f14)
 Call ID: 37cb74f6-ab50-415e-a09a-71a192f99f14
  Args:
    relation: :hasFather
    source: Prince Andrew of Greece and Denmark
    target: King Christian IX of Denmark
  AddTriple (3af75fc1-95f2-43c8-a747-174e778b878e)
 Call ID: 3af75fc1-95f2-43c8-a747-174e778b878e
  Args:
    relation: :hasFather
    source: Prince Philip
    target: Prince Andrew of Greece and Denmark
  AddTriple (fc029419-963f-4475-95ea-fc5eb84b6e20)
 Call ID: fc029419-963f-4475-95ea-fc5eb84b6e20
  Args:
    relation: :hasMother
    target: Princess Alice of Battenberg
    source: Prince Philip
  AddTriple (839d2dd6-adcb-4af4-bc35-a85213418603)
 Call ID: 839d2dd6-adcb-4af4-bc35-a85213418603
  Args:
    source: Prince Andrew of Greece and Denmark
    target: King Constantine of Greece
    relation: :hasBrother
  AddTriple (800a043d-5c63-4767-9db7-bcc5d48a3d49)
 Call ID: 800a043d-5c63-4767-9db7-bcc5d48a3d49
  Args:
    relation: :hasFather
    source: King Constantine of Greece
    target: King George I of Greece
  AddTriple (5d887105-1c94-4fbe-acc7-2da47c3c134e)
 Call ID: 5d887105-1c94-4fbe-acc7-2da47c3c134e
  Args:
    relation: :hasFather
    source: Princess Alice of Battenberg
    target: Prince Louis of Battenberg
  AddTriple (39684a50-a776-41e8-9448-6fa83d79faec)
 Call ID: 39684a50-a776-41e8-9448-6fa83d79faec
  Args:
    relation: :hasMother
    source: Princess Alice of Battenberg
    target: Princess Victoria of Hesse and by Rhine
  AddTriple (fba66b7e-08c4-4499-9566-7dd111ff71a8)
 Call ID: fba66b7e-08c4-4499-9566-7dd111ff71a8
  Args:
    source: King Alexander of Greece
    target: King Constantine of Greece
    relation: :hasFather
  AddTriple (de0faafd-0916-4600-81a6-51c096de4aa5)
 Call ID: de0faafd-0916-4600-81a6-51c096de4aa5
  Args:
    relation: :hasFather
    source: Princess Cecilie
    target: Prince Andrew of Greece and Denmark
  AddTriple (4935c8f2-02d8-45bf-b80a-7152d4dbb992)
 Call ID: 4935c8f2-02d8-45bf-b80a-7152d4dbb992
  Args:
    target: Princess Alice of Battenberg
    source: Princess Cecilie
    relation: :hasMother
  AddLiteral (1ee4ea06-178f-4b20-99bd-30876837f554)
 Call ID: 1ee4ea06-178f-4b20-99bd-30876837f554
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    source: Prince Andrew of Greece and Denmark
    literal_value: 1903
  AddTriple (6171c150-d381-4fb2-916b-bf78b2c0a7de)
 Call ID: 6171c150-d381-4fb2-916b-bf78b2c0a7de
  Args:
    source: Prince Andrew of Greece and Denmark
    target: Princess Alice of Battenberg
    relation: :hasRelation
  Finish (62816786-fe8b-4dd4-9440-322a75de30ff)
 Call ID: 62816786-fe8b-4dd4-9440-322a75de30ff
  Args: