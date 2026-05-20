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
The Duchess of Montpensier


The Count of ÉvreuxThe Countess of Évreux


Princess Béatrice


The Duke of OrléansThe Duchess of Orléans


The Dowager Countess of La Marche


The Countess of Schönborn-Buchheim


Princess Hélène, Countess of Limburg Stirum


The Dowager Duchess of Calabria


The Dowager Duchess of Württemberg


Princess Claude, Mrs. Gandolfi


Princess Chantal, Baroness of Sambucy de Sorgue


Prince Jean Carl Pierre Marie d'Orléans, Count of Paris (born 19 May 1965) is the current head of the House of Orléans.
Jean is the senior male descendant by primogeniture in the male-line of Louis Philippe I, King of the French, and thus according to the Orléanists the legitimate claimant to the defunct throne of France as Jean IV.
Jean is the second son of Henri, Count of Paris (1933–2019) and his former wife Duchess Marie-Thérèse of Württemberg (born 1934).
Biography

Early life and education

Jean d'Orléans was born on 19 May 1965 in Boulogne-Billancourt, the son of Henri of Orleans and Maria Theresa of Württemberg.
He received as godfather, his maternal uncle, Carl of Württemberg, and as godmother, his paternal aunt, Princess Chantal of Orleans.
Jean completed his national service as an officer, first taking four months of classes at the Saumur Cavalry School.
Jean is multilingual, speaking French, English, and German.
First engagement

Prince Jean was due to marry Duchess Tatjana of Oldenburg (b. 1974) in 2001.
However, the wedding was cancelled at the last moment because of a dispute over religious denomination: Jean's father, Henri, feared the Orléans claim to the throne would be compromised if there were to be a Protestant heir.
Second engagement and marriage

On 29 November 2008, Henri, then Count of Paris, announced the engagement of Jean, the then Duke of Vendôme, to Maria Magdalena Philomena Juliana Johanna de Tornos y Steinhart, born in Vienna on 19 June 1977.
Lawsuit

In 2021, Jean filed a lawsuit against the Saint-Louis foundation, demanding €1 million in damages and the return of five properties, including the Château d'Amboise.
In 1886, the château was bequeathed to the Institute of France by Jean's ancestor Henri d’Orléans, with the caveat that the property would never be altered by the institute.
The Saint-Louis foundation was later founded by Jean's grandfather, Henri VI, Count of Paris, in 1974.
Jean's lawsuit alleges that the Institute violated their contract to never alter the property, after they announced plans to transform the Pavillon d’Enghien into a €760-a-night luxury hotel, containing a spa and gastronomic restaurant.
Jean had previously lived in the château from 2001 to September 2021 rent-free, but was forcefully evicted by the institute after they began to demand he pay rent, which Jean viewed as a violation of their contract.
Family

Jean and his wife Philomena have six children: 


Politics

Jean believes that the people of France are "monarchist at heart" and argues that they long for a non-partisan figurehead.
Jean has also expressed his opposition to same-sex marriage, having participated in the La Manif pour tous protests, as well as abortion.
In May 2019, Jean met with French President Emmanuel Macron, Brigitte Macron, and Italian President Sergio Mattarella in his then-home in the Château d'Amboise.


Titles, styles and honours

Titles in pretense

He was created Duke of Vendôme (French: Duc de Vendôme) by his paternal grandfather, on 27 September 1987.
Following the death of his father, it was initially thought that Prince Jean would not assume the title of Count of Paris for several months after his father's death, and possibly not for as much as one year.
Honours

National

Dynastic

Ancestry

Jean is a direct male-line descendant of Louis Philippe I, the last French king, who in turn was a descendant of Philippe I, Duke of Orléans, the younger brother of Louis XIV.
Jean is also descended from Charles X, brother of Louis XVI; and the Bourbons of Spain, the Two Sicilies and Parma.



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
  AssignClass (99294aff-edea-4c18-bdd6-a688a59c9a7f)
 Call ID: 99294aff-edea-4c18-bdd6-a688a59c9a7f
  Args:
    source: Jean_dOrleans
    type: :Man
  AssignClass (e4d9bdb4-161a-49db-a9b6-ac6cd3d49e90)
 Call ID: e4d9bdb4-161a-49db-a9b6-ac6cd3d49e90
  Args:
    type: :Person
    source: Jean_dOrleans
  AddLiteral (56b8f7cc-91bf-4e60-83de-67291ce1649e)
 Call ID: 56b8f7cc-91bf-4e60-83de-67291ce1649e
  Args:
    literal_type: xsd:integer
    literal_value: 1965
    relation: :hasBirthYear
    source: Jean_dOrleans
  AssignClass (cf5e519d-6282-4e71-8f70-bb54ca3d4ad7)
 Call ID: cf5e519d-6282-4e71-8f70-bb54ca3d4ad7
  Args:
    type: :Man
    source: Henri_Count_of_Paris
  AssignClass (bf708b01-e961-4579-847f-501194d7f4f7)
 Call ID: bf708b01-e961-4579-847f-501194d7f4f7
  Args:
    source: Henri_Count_of_Paris
    type: :Person
  AddLiteral (2098f69f-fc3f-42cf-a9a8-6d0aa750c093)
 Call ID: 2098f69f-fc3f-42cf-a9a8-6d0aa750c093
  Args:
    literal_type: xsd:integer
    literal_value: 1933
    source: Henri_Count_of_Paris
    relation: :hasBirthYear
  AddLiteral (6aa523f9-61cd-4693-98ac-488a59b407a5)
 Call ID: 6aa523f9-61cd-4693-98ac-488a59b407a5
  Args:
    source: Henri_Count_of_Paris
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 2019
  AssignClass (4dcbdb24-211e-427e-8db5-cf974c15eba1)
 Call ID: 4dcbdb24-211e-427e-8db5-cf974c15eba1
  Args:
    source: Marie-Therese_of_Wurttemberg
    type: :Woman
  AssignClass (04d0c69c-7ee6-4fa1-8814-f634d2982d78)
 Call ID: 04d0c69c-7ee6-4fa1-8814-f634d2982d78
  Args:
    source: Marie-Therese_of_Wurttemberg
    type: :Person
  AddLiteral (02734c74-3682-4b37-b55a-a4be0f496974)
 Call ID: 02734c74-3682-4b37-b55a-a4be0f496974
  Args:
    relation: :hasBirthYear
    source: Marie-Therese_of_Wurttemberg
    literal_type: xsd:integer
    literal_value: 1934
  AddTriple (fe1e24a4-0702-4559-b944-363af923381d)
 Call ID: fe1e24a4-0702-4559-b944-363af923381d
  Args:
    target: Henri_Count_of_Paris
    source: Jean_dOrleans
    relation: :hasFather
  AddTriple (5f8cc413-bfdf-490b-b2f7-dda56c9ed732)
 Call ID: 5f8cc413-bfdf-490b-b2f7-dda56c9ed732
  Args:
    source: Jean_dOrleans
    relation: :hasMother
    target: Marie-Therese_of_Wurttemberg
  AssignClass (d619e6aa-6b38-4535-9e6e-f9fe8b7a7b9a)
 Call ID: d619e6aa-6b38-4535-9e6e-f9fe8b7a7b9a
  Args:
    source: Philomena_de_Tornos_y_Steinhart
    type: :Woman
  AssignClass (16dc03f1-ed40-49f2-829a-fee64f85deb6)
 Call ID: 16dc03f1-ed40-49f2-829a-fee64f85deb6
  Args:
    source: Philomena_de_Tornos_y_Steinhart
    type: :Person
  AddLiteral (b9fd4ebb-ae71-46b3-b1f6-b5aad205954f)
 Call ID: b9fd4ebb-ae71-46b3-b1f6-b5aad205954f
  Args:
    source: Philomena_de_Tornos_y_Steinhart
    relation: :hasBirthYear
    literal_value: 1977
    literal_type: xsd:integer
  AddTriple (ba0a86b9-90ea-4e19-ada0-a68f3980db66)
 Call ID: ba0a86b9-90ea-4e19-ada0-a68f3980db66
  Args:
    source: Jean_dOrleans
    relation: :hasRelation
    target: Philomena_de_Tornos_y_Steinhart
  AssignClass (adf613a3-bc40-4453-8966-cd42869dbe4f)
 Call ID: adf613a3-bc40-4453-8966-cd42869dbe4f
  Args:
    type: :Man
    source: Carl_of_Wurttemberg
  AssignClass (1f9a7662-2f25-4298-af4a-5a605e861bd4)
 Call ID: 1f9a7662-2f25-4298-af4a-5a605e861bd4
  Args:
    source: Carl_of_Wurttemberg
    type: :Person
  AddTriple (518d5091-b8ac-4937-8b0d-75265904e4c1)
 Call ID: 518d5091-b8ac-4937-8b0d-75265904e4c1
  Args:
    target: Marie-Therese_of_Wurttemberg
    source: Carl_of_Wurttemberg
    relation: :isBrotherOf
  AssignClass (60cfe44f-8da0-4480-ab4f-d6981a5bafc6)
 Call ID: 60cfe44f-8da0-4480-ab4f-d6981a5bafc6
  Args:
    type: :Woman
    source: Princess_Chantal_of_Orleans
  AssignClass (337de3b3-0da9-4de8-aaef-16218424fdba)
 Call ID: 337de3b3-0da9-4de8-aaef-16218424fdba
  Args:
    source: Princess_Chantal_of_Orleans
    type: :Person
  AddTriple (25b79a99-fc67-42e2-aa04-209b11e4ce23)
 Call ID: 25b79a99-fc67-42e2-aa04-209b11e4ce23
  Args:
    relation: :isSisterOf
    source: Princess_Chantal_of_Orleans
    target: Henri_Count_of_Paris
  AssignClass (d1b448da-8d8b-4053-ac6e-a0747d81dd72)
 Call ID: d1b448da-8d8b-4053-ac6e-a0747d81dd72
  Args:
    type: :Man
    source: Henri_VI_Count_of_Paris
  AssignClass (d2dccba0-9e59-4c1b-9c23-61e75d0b8093)
 Call ID: d2dccba0-9e59-4c1b-9c23-61e75d0b8093
  Args:
    source: Henri_VI_Count_of_Paris
    type: :Person
  AddTriple (f3f18aef-c3bb-43de-8eef-eec8b8f46685)
 Call ID: f3f18aef-c3bb-43de-8eef-eec8b8f46685
  Args:
    target: Henri_Count_of_Paris
    source: Henri_VI_Count_of_Paris
    relation: :isFatherOf
  AssignClass (151271bc-ebb0-443a-867d-f49c0de79c36)
 Call ID: 151271bc-ebb0-443a-867d-f49c0de79c36
  Args:
    source: Louis_Philippe_I
    type: :Man
  AssignClass (277f7e37-5784-401b-a762-414719c4970a)
 Call ID: 277f7e37-5784-401b-a762-414719c4970a
  Args:
    source: Louis_Philippe_I
    type: :Person
  AddTriple (daa57dc1-720b-4baa-b036-e6e7569b8885)
 Call ID: daa57dc1-720b-4baa-b036-e6e7569b8885
  Args:
    relation: :isAncestorOf
    source: Louis_Philippe_I
    target: Jean_dOrleans
  AssignClass (ecea4b7b-fd67-49ca-89db-65bcc82b7984)
 Call ID: ecea4b7b-fd67-49ca-89db-65bcc82b7984
  Args:
    type: :Man
    source: Philippe_I_Duke_of_Orleans
  AssignClass (4b12360f-4232-43f9-8a6f-1370fba4adbf)
 Call ID: 4b12360f-4232-43f9-8a6f-1370fba4adbf
  Args:
    type: :Person
    source: Philippe_I_Duke_of_Orleans
  AddTriple (97eace41-29bd-4794-8693-ff21945d31a9)
 Call ID: 97eace41-29bd-4794-8693-ff21945d31a9
  Args:
    target: Louis_Philippe_I
    relation: :isAncestorOf
    source: Philippe_I_Duke_of_Orleans
  AssignClass (c656ed5d-9bd0-4722-abbb-a757f0ffecf8)
 Call ID: c656ed5d-9bd0-4722-abbb-a757f0ffecf8
  Args:
    type: :Man
    source: Louis_XIV
  AssignClass (c041ba75-8459-40e0-a339-2ac6404916e6)
 Call ID: c041ba75-8459-40e0-a339-2ac6404916e6
  Args:
    source: Louis_XIV
    type: :Person
  AddTriple (856b99cf-7dc3-4b69-8c90-ad92c4a9f938)
 Call ID: 856b99cf-7dc3-4b69-8c90-ad92c4a9f938
  Args:
    target: Louis_XIV
    relation: :isBrotherOf
    source: Philippe_I_Duke_of_Orleans
  AssignClass (540f0617-951d-4b4f-80a5-cacf1b52497d)
 Call ID: 540f0617-951d-4b4f-80a5-cacf1b52497d
  Args:
    source: Charles_X
    type: :Man
  AssignClass (d825c80b-a416-439e-a317-ee1afbe10461)
 Call ID: d825c80b-a416-439e-a317-ee1afbe10461
  Args:
    source: Charles_X
    type: :Person
  AssignClass (2730ccb1-3677-4539-9297-424c4249670f)
 Call ID: 2730ccb1-3677-4539-9297-424c4249670f
  Args:
    type: :Man
    source: Louis_XVI
  AssignClass (ebd9fc7a-6c86-42dd-bbca-06dad6cb5c8a)
 Call ID: ebd9fc7a-6c86-42dd-bbca-06dad6cb5c8a
  Args:
    source: Louis_XVI
    type: :Person
  AddTriple (662d4a6b-4dab-43a4-b37e-59bc1f8b5569)
 Call ID: 662d4a6b-4dab-43a4-b37e-59bc1f8b5569
  Args:
    relation: :isBrotherOf
    source: Charles_X
    target: Louis_XVI
  AddTriple (ce4ae5f8-7b3f-4329-ba88-a6c9d6addd25)
 Call ID: ce4ae5f8-7b3f-4329-ba88-a6c9d6addd25
  Args:
    target: Jean_dOrleans
    source: Charles_X
    relation: :isAncestorOf
  AssignClass (d1689cc6-f1b8-4f87-a6e0-dc9f83051549)
 Call ID: d1689cc6-f1b8-4f87-a6e0-dc9f83051549
  Args:
    source: Duchess_Tatjana_of_Oldenburg
    type: :Woman
  AssignClass (40bc01be-bb7f-4b9a-ad59-ac5304df6450)
 Call ID: 40bc01be-bb7f-4b9a-ad59-ac5304df6450
  Args:
    source: Duchess_Tatjana_of_Oldenburg
    type: :Person
  AddLiteral (727040b7-1658-42dc-9c47-d818d6310d88)
 Call ID: 727040b7-1658-42dc-9c47-d818d6310d88
  Args:
    literal_value: 1974
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Duchess_Tatjana_of_Oldenburg
  AddTriple (8748746a-2b48-4b59-89ac-cebfc600749e)
 Call ID: 8748746a-2b48-4b59-89ac-cebfc600749e
  Args:
    relation: :hasRelation
    source: Jean_dOrleans
    target: Duchess_Tatjana_of_Oldenburg
  Finish (f177ef15-21c7-4edc-99d1-70ad7b7fe83e)
 Call ID: f177ef15-21c7-4edc-99d1-70ad7b7fe83e
  Args: