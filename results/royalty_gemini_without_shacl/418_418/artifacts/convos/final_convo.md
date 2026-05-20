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
Donatus, Prince and Landgrave of Hesse (legally Heinrich Donatus Philipp Umberto Prinz und Landgraf von Hessen; born 17 October 1966) is a German businessman and the head of the House of Brabant and the House of Hesse.
He is the eldest son and successor of German aristocrat Moritz, Landgrave of Hesse, and his former wife, Princess Tatiana of Sayn-Wittgenstein-Berleburg (b. 1940).
Donatus's father became the head of the Hesse-Cassel line on the death of his own father, Landgrave Philipp in 1980.
Having also been the adopted son and heir of his distant cousin, Louis, Prince of Hesse and by Rhine, the latter's death in 1968 as the last male of the Hesse-Darmstadt branch left Moritz head of the entire House of Hesse, to which Donatus succeeded.
Profession

Donatus directs the Hessische Hausstiftung (Foundation of the House of Hesse), a foundation (see below) established to curate and showcase the cultural heritage and history of the House of Hesse, a dynasty which ruled the Electorate of Hesse-Cassel until 1866, the Grand Duchy of Hesse and by Rhine until 1918, and whose male-line antecedents and co-lateral ties include the Protestant leader Philip the Magnanimous, the Swedish king Frederick I, Russia's last tsarina Alexandra Feodorovna, the exiled Spanish queen Victoria Eugenie of Battenberg, and Britain's last viceroy of India, the assassinated Louis, Earl Mountbatten of Burma.
Donatus also manages Prinz von Hessen, a winery specializing in production of varietal vintages on his 45 hectare vineyard.
Marriage and issue

Donatus married the daughter of German industrial heir and Chinese honorary citizen Count Hubertus von Faber-Castell, Countess Floria Franziska Marie-Luisa Erika von Faber-Castell (born 14 October 1974, Düsseldorf), in a civil ceremony in Wiesbaden on 25 April 2003.
Prince Donatus and Floria Franziska are 6th cousins, as both descended from Frederick II, Landgrave of Hesse-Kassel and his first wife Princess Mary of Great Britain.
Held at the Johanneskirche and followed by a grand ball in the Green Salon, state room of the former Friedrichshof palace in Kronberg (now a luxury hotel and golf course owned by the House of Hesse's family foundation) where Donatus's ancestress, the German Empress Frederick, Princess Royal, lived in widowhood, more than 300 guests were present.
Among them were Caroline, Princess of Hanover, Princess Benedikte of Denmark, and Gloria, Princess of Thurn and Taxis.
Representative appearances

In 2021, Donatus was one of only 30 mourners at Prince Philip, the Duke of Edinburgh's, funeral at St George's Chapel, Windsor Castle.
King Charles III appointed Donatus his personal representative to the funeral of his first cousin Maximilian, Margrave of Baden, on 13 January 2023.
Although, as a descendant of Queen Victoria, he is only a distant relative of today's British royals who are more closely related to some other princes of Hesse, descendants of Prince Philip's sister Sophie, there is a close connection to the British royal family through Donatus' adoptive grandparents, Louis, Prince of Hesse and by Rhine, and his wife Margaret Campbell Geddes, who were relatives and close friends of Queen Elizabeth II and Prince Philip, as Philip's sister Cecilie had been married to Louis' elder brother Georg Donatus, Hereditary Grand Duke of Hesse.
The late Queen, Prince Philip and Charles (then Prince of Wales) have visited Wolfsgarten on several occasions.
Ancestry

Foundation of the House of Hesse

Founded in 1928, the Foundation of the House of Hesse is the successor institution of a family trust that had been established in 1830, confiscated by the Kingdom of Prussia in 1866, and re-established after partial restitution in 1878.
The latter is mainly shown at Fasanerie Palace in Eichenzell, Hesse, a former summer palace of the Prince Abbots of Fulda that had been taken over by the Landgraves of Hesse after the secularization and mediatisation of the Prince-bishopric of Fulda in 1803.
The Landgrave and his family live in Wolfsgarten and Panker.



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
  AssignClass (4787c449-5775-415e-8edc-6b6400a67e21)
 Call ID: 4787c449-5775-415e-8edc-6b6400a67e21
  Args:
    type: :Man
    source: Donatus
  AssignClass (11cd7700-1f6f-4c0a-aed8-f5159aab7dc2)
 Call ID: 11cd7700-1f6f-4c0a-aed8-f5159aab7dc2
  Args:
    type: :Man
    source: Moritz
  AssignClass (bd428053-e105-4eb7-93b0-a7a38d7c85e8)
 Call ID: bd428053-e105-4eb7-93b0-a7a38d7c85e8
  Args:
    type: :Woman
    source: Tatiana
  AssignClass (a0add781-24ff-40ad-934b-134678302c98)
 Call ID: a0add781-24ff-40ad-934b-134678302c98
  Args:
    type: :Man
    source: Philipp
  AssignClass (d278405d-98f7-481d-93a1-af1194de4a44)
 Call ID: d278405d-98f7-481d-93a1-af1194de4a44
  Args:
    type: :Man
    source: Louis
  AssignClass (eebbf5ef-84d0-48e6-8e2f-5aeb0754a7b2)
 Call ID: eebbf5ef-84d0-48e6-8e2f-5aeb0754a7b2
  Args:
    type: :Woman
    source: FloriaFranziska
  AssignClass (2d48ab0c-b46b-4caa-8d05-18195af614b2)
 Call ID: 2d48ab0c-b46b-4caa-8d05-18195af614b2
  Args:
    type: :Man
    source: Hubertus
  AssignClass (375cc268-8e07-4486-9b35-955ffebaef5d)
 Call ID: 375cc268-8e07-4486-9b35-955ffebaef5d
  Args:
    type: :Man
    source: FrederickII
  AssignClass (359d9627-0f3f-4b0c-8cb1-4cdd426a40cc)
 Call ID: 359d9627-0f3f-4b0c-8cb1-4cdd426a40cc
  Args:
    type: :Woman
    source: Mary
  AddLiteral (e60dcf23-c1d4-4694-9ffa-de691631526f)
 Call ID: e60dcf23-c1d4-4694-9ffa-de691631526f
  Args:
    literal_value: 1966
    source: Donatus
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (42c10ed0-2647-48cc-ad56-b1c9144c679c)
 Call ID: 42c10ed0-2647-48cc-ad56-b1c9144c679c
  Args:
    source: Tatiana
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1940
  AddLiteral (9fbee8f7-2748-44f5-87fc-371bdabb47de)
 Call ID: 9fbee8f7-2748-44f5-87fc-371bdabb47de
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: FloriaFranziska
    literal_value: 1974
  AddLiteral (6c907368-52ae-4ea3-ab93-957e936e5eb4)
 Call ID: 6c907368-52ae-4ea3-ab93-957e936e5eb4
  Args:
    literal_value: 2003
    literal_type: xsd:integer
    relation: :hasMarriageYear
    source: Donatus
  AddTriple (1ef534e2-30b3-4aff-86b0-19b778f62a28)
 Call ID: 1ef534e2-30b3-4aff-86b0-19b778f62a28
  Args:
    source: Donatus
    relation: :hasFather
    target: Moritz
  AddTriple (c74dbe41-6ba9-4547-9c1e-ea45318977b6)
 Call ID: c74dbe41-6ba9-4547-9c1e-ea45318977b6
  Args:
    target: Tatiana
    relation: :hasMother
    source: Donatus
  AddTriple (92c4b757-b1ed-40ed-844e-584362465a28)
 Call ID: 92c4b757-b1ed-40ed-844e-584362465a28
  Args:
    target: Philipp
    relation: :hasFather
    source: Moritz
  AddTriple (b77b88aa-7847-4e65-a21c-e0dd4786b7ce)
 Call ID: b77b88aa-7847-4e65-a21c-e0dd4786b7ce
  Args:
    target: Hubertus
    relation: :hasFather
    source: FloriaFranziska
  AddTriple (f1ebaa7d-74d3-4659-a5d6-4bdad1de89da)
 Call ID: f1ebaa7d-74d3-4659-a5d6-4bdad1de89da
  Args:
    relation: :isAncestorOf
    source: FrederickII
    target: Donatus
  AddTriple (ce6d842a-acbc-4a91-a458-f9bb1e7bfa06)
 Call ID: ce6d842a-acbc-4a91-a458-f9bb1e7bfa06
  Args:
    relation: :isAncestorOf
    source: FrederickII
    target: FloriaFranziska
  AddTriple (2d1b65db-95fe-4d40-97a5-777318907541)
 Call ID: 2d1b65db-95fe-4d40-97a5-777318907541
  Args:
    target: Donatus
    relation: :isAncestorOf
    source: Mary
  AddTriple (c37fd2a5-21bf-4d31-8ece-91a093232916)
 Call ID: c37fd2a5-21bf-4d31-8ece-91a093232916
  Args:
    target: FloriaFranziska
    relation: :isAncestorOf
    source: Mary
  Finish (cb3aa7d1-5bf0-4615-974e-047fad33a474)
 Call ID: cb3aa7d1-5bf0-4615-974e-047fad33a474
  Args: