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
Prince Vincent of Denmark, Count of Monpezat RE (Vincent Frederik Minik Alexander; born 8 January 2011) is a member of the Danish royal family.
He is the third child and younger son of King Frederik X and Queen Mary, the sixth grandchild and youngest grandson of Queen Margrethe II and Prince Henrik, and the older twin brother of Princess Josephine.
Vincent is third in line to the Danish throne, after his older brother, Crown Prince Christian, and older sister, Princess Isabella.
Birth and early life

Queen Margrethe II


Vincent was born on 8 January 2011 at Rigshospitalet, the Copenhagen University Hospital, in Copenhagen, at 10:30 am local time, 26 minutes before his twin sister.
Shortly after the birth, while speaking to the press, the Crown Prince joked about calling his newborn son Elvis, as the twins share a birthday with Elvis Presley.
Vincent and his sister were baptised by the royal confessor, the Bishop of Copenhagen Erik Norman Svendsen, on 14 April at the Church of Holmen in central Copenhagen.
The twins were baptised at the royal baptismal font which has been used for the baptism of royal children in Denmark since 1671.
Prince Vincent wore the royal christening gown which was made for his great-great-grandfather, King Christian X, in 1870, while his sister wore a gown found among Queen Ingrid's belongings.
His name was announced as Vincent Frederik Minik Alexander.
His godparents are his maternal uncle, John Stuart Donaldson; his father's first cousin, the Prince of Sayn-Wittgenstein-Berleburg (then the Hereditary Prince); his mother's lady-in-waiting, Caroline Heering; and friends of his parents, the King of Spain (then the Prince of Asturias), Count Michael Ahlefeldt-Laurvig-Bille and Baroness Helle Reedtz-Thott.
Under the old system of male-preference primogeniture, Vincent would have displaced his elder sister Isabella in the line of succession; with the new law, he comes directly after her instead.
On 15 August 2017, Vincent and his younger twin sister started school at Tranegårdsskolen in Gentofte – the same public school as their elder siblings.
Titles, styles, and honours

Vincent is styled as His Royal Highness Prince Vincent of Denmark, Count of Monpezat.



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
  AssignClass (48372d74-9410-4bdc-94e9-e4df1a3fbdb6)
 Call ID: 48372d74-9410-4bdc-94e9-e4df1a3fbdb6
  Args:
    type: :Man
    source: :Prince_Vincent_of_Denmark
  AssignClass (7de9d41b-a7af-4304-964a-54382bea5c66)
 Call ID: 7de9d41b-a7af-4304-964a-54382bea5c66
  Args:
    source: :Prince_Vincent_of_Denmark
    type: :Person
  AddLiteral (4bacf6dc-7daf-4248-ba41-a2e641b21c4f)
 Call ID: 4bacf6dc-7daf-4248-ba41-a2e641b21c4f
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: :Prince_Vincent_of_Denmark
    literal_value: 2011
  AssignClass (4a1828f0-74c7-4a3a-9354-7601f555b474)
 Call ID: 4a1828f0-74c7-4a3a-9354-7601f555b474
  Args:
    type: :Man
    source: :King_Frederik_X
  AssignClass (ea09b958-43a5-461b-991f-e3a749d54306)
 Call ID: ea09b958-43a5-461b-991f-e3a749d54306
  Args:
    source: :King_Frederik_X
    type: :Person
  AssignClass (58600927-cc8e-4f66-9adf-c5130653e0f5)
 Call ID: 58600927-cc8e-4f66-9adf-c5130653e0f5
  Args:
    type: :Woman
    source: :Queen_Mary
  AssignClass (7f8ffc09-8d2e-4c67-bfec-41ab3d0ff413)
 Call ID: 7f8ffc09-8d2e-4c67-bfec-41ab3d0ff413
  Args:
    source: :Queen_Mary
    type: :Person
  AddTriple (66d7bacf-e1cb-4412-9d0b-9d4d39fc24aa)
 Call ID: 66d7bacf-e1cb-4412-9d0b-9d4d39fc24aa
  Args:
    relation: :hasFather
    target: :King_Frederik_X
    source: :Prince_Vincent_of_Denmark
  AddTriple (9c8178e4-2f70-4bd5-8b39-d5fd1fbf0eb7)
 Call ID: 9c8178e4-2f70-4bd5-8b39-d5fd1fbf0eb7
  Args:
    source: :Prince_Vincent_of_Denmark
    target: :Queen_Mary
    relation: :hasMother
  AssignClass (ad5b0e29-49fb-4acf-8fac-23b7005ad2c5)
 Call ID: ad5b0e29-49fb-4acf-8fac-23b7005ad2c5
  Args:
    type: :Woman
    source: :Princess_Josephine
  AssignClass (634a7818-a2d3-4037-a170-12766c094e22)
 Call ID: 634a7818-a2d3-4037-a170-12766c094e22
  Args:
    source: :Princess_Josephine
    type: :Person
  AddTriple (a69c8372-5933-477c-a170-ad856e352bd4)
 Call ID: a69c8372-5933-477c-a170-ad856e352bd4
  Args:
    source: :Prince_Vincent_of_Denmark
    target: :Princess_Josephine
    relation: :hasSister
  AssignClass (189d0d6d-592e-4528-b5da-9386b57275fa)
 Call ID: 189d0d6d-592e-4528-b5da-9386b57275fa
  Args:
    source: :Queen_Margrethe_II
    type: :Woman
  AssignClass (428bc99a-1e79-417c-9eff-36b9bd05ea12)
 Call ID: 428bc99a-1e79-417c-9eff-36b9bd05ea12
  Args:
    type: :Person
    source: :Queen_Margrethe_II
  AssignClass (842e4ca5-14ab-4195-a4be-059bc5c01102)
 Call ID: 842e4ca5-14ab-4195-a4be-059bc5c01102
  Args:
    type: :Man
    source: :Prince_Henrik
  AssignClass (0d2ef5d7-169b-43f8-a60e-d03a2cb57953)
 Call ID: 0d2ef5d7-169b-43f8-a60e-d03a2cb57953
  Args:
    type: :Person
    source: :Prince_Henrik
  AssignClass (a16dc157-699b-4418-9979-c2be30c340ee)
 Call ID: a16dc157-699b-4418-9979-c2be30c340ee
  Args:
    source: :Crown_Prince_Christian
    type: :Man
  AssignClass (dab29f78-875d-4ba3-84e3-0ced25a75c09)
 Call ID: dab29f78-875d-4ba3-84e3-0ced25a75c09
  Args:
    source: :Crown_Prince_Christian
    type: :Person
  AddTriple (cc72c90f-da1e-452f-b0a2-b2f1208142bd)
 Call ID: cc72c90f-da1e-452f-b0a2-b2f1208142bd
  Args:
    source: :Prince_Vincent_of_Denmark
    target: :Crown_Prince_Christian
    relation: :hasBrother
  AssignClass (a5a8af85-44ec-42be-88ec-baa20b07e429)
 Call ID: a5a8af85-44ec-42be-88ec-baa20b07e429
  Args:
    type: :Woman
    source: :Princess_Isabella
  AssignClass (e2e05f95-205f-4305-b4f6-df061477a69d)
 Call ID: e2e05f95-205f-4305-b4f6-df061477a69d
  Args:
    source: :Princess_Isabella
    type: :Person
  AddTriple (eefa3287-aa29-47d6-ab23-f83536e3de50)
 Call ID: eefa3287-aa29-47d6-ab23-f83536e3de50
  Args:
    relation: :hasSister
    source: :Prince_Vincent_of_Denmark
    target: :Princess_Isabella
  AssignClass (d15c6b07-a10d-4fab-afb9-06cbdd79c1be)
 Call ID: d15c6b07-a10d-4fab-afb9-06cbdd79c1be
  Args:
    source: :King_Christian_X
    type: :Man
  AssignClass (7a9e7ccf-176b-4d86-a148-cfe731c52584)
 Call ID: 7a9e7ccf-176b-4d86-a148-cfe731c52584
  Args:
    type: :Person
    source: :King_Christian_X
  AssignClass (cd821b86-0682-42ba-9408-0a0c613054d1)
 Call ID: cd821b86-0682-42ba-9408-0a0c613054d1
  Args:
    source: :Queen_Ingrid
    type: :Woman
  AssignClass (63b1ba22-91ba-467b-a635-2f336d97c72a)
 Call ID: 63b1ba22-91ba-467b-a635-2f336d97c72a
  Args:
    source: :Queen_Ingrid
    type: :Person
  Finish (e45a5e20-3da5-4407-9a0c-ef4eade1ec9e)
 Call ID: e45a5e20-3da5-4407-9a0c-ef4eade1ec9e
  Args: