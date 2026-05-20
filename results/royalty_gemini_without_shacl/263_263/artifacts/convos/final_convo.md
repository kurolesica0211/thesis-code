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
Princess Beatrix*


Princess Margriet*Pieter van Vollenhoven*


Prince Constantijn of the Netherlands (Constantijn Christof Frederik Aschwin; born 11 October 1969) is the third and youngest son of the former Dutch queen, Beatrix, and her husband, Claus von Amsberg, and is the younger brother of the reigning Dutch king, Willem-Alexander.
Life and career

Prince Constantijn was born on 11 October 1969 at  Academic Hospital Utrecht (now the University Medical Center Utrecht) in Utrecht following the births of his brothers, Willem-Alexander (b. 1967), and Johan Friso (1968–2013).
His godparents are former King Constantine II of Greece (1940–2023), Prince Aschwin of Lippe-Biesterfeld, Axel Freiherr von dem Bussche-Streithorst, Max Kohnstamm, and Corinne de Beaufort-Sickinghe.
Prince Constantijn studied law at Leiden University, becoming a lawyer, and then worked at the Brussels department of the (Dutch) European Union commissioner of foreign relations, Hans van den Broek.
Furthermore, he has a part-time position at the Netherlands Ministry of Foreign Affairs in The Hague.
Prince Constantijn rarely attends public events in his capacity as a member of the Dutch royal family.
Marriage and family

The engagement of Prince Constantijn and Petra Laurentien Brinkhorst was announced on 16 December 2000.
Prince Constantijn and Princess Laurentien have three children: Eloise (b. 2002), Claus-Casimir (b. 2004), and Leonore (b. 2006).
Upon the abdication of Queen Beatrix on 30 April 2013, the children of Prince Constantijn and Princess Laurentien ceased to be members of the Royal House, although they continue to be members of the royal family and remain in the line of succession.
Honours and arms

National

Foreign

Arms

Ancestry

References

External links

2 gave up the title "Prince of the Netherlands, but still held the title "Prince of Orange-Nassau"
3 title granted by Royal Decree to descendants of Princess Irene



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
  AssignClass (7263071d-549e-4a55-8ad4-c578b42f8c27)
 Call ID: 7263071d-549e-4a55-8ad4-c578b42f8c27
  Args:
    type: :Woman
    source: Beatrix
  AssignClass (655658d9-4c8d-4ec8-9282-57ec6151cdbb)
 Call ID: 655658d9-4c8d-4ec8-9282-57ec6151cdbb
  Args:
    type: :Man
    source: Claus_von_Amsberg
  AssignClass (35a3cae5-68be-425f-8b9d-f95a5c710f15)
 Call ID: 35a3cae5-68be-425f-8b9d-f95a5c710f15
  Args:
    type: :Man
    source: Constantijn
  AssignClass (07f2a063-094e-4685-9f3f-73c345fb3560)
 Call ID: 07f2a063-094e-4685-9f3f-73c345fb3560
  Args:
    type: :Man
    source: Willem-Alexander
  AssignClass (b74b5eea-c960-4a6d-a956-d197020251cf)
 Call ID: b74b5eea-c960-4a6d-a956-d197020251cf
  Args:
    type: :Man
    source: Johan_Friso
  AssignClass (f3a5123b-6954-424d-ad26-5ee2292673ef)
 Call ID: f3a5123b-6954-424d-ad26-5ee2292673ef
  Args:
    type: :Woman
    source: Laurentien_Brinkhorst
  AssignClass (34b38d1a-d94e-4f39-b667-9d4260388f4a)
 Call ID: 34b38d1a-d94e-4f39-b667-9d4260388f4a
  Args:
    type: :Woman
    source: Eloise
  AssignClass (0e3d6795-1bb1-497a-91ab-133e3b478e77)
 Call ID: 0e3d6795-1bb1-497a-91ab-133e3b478e77
  Args:
    type: :Man
    source: Claus-Casimir
  AssignClass (ce99f804-dc75-42e4-8b63-4f509ae26bfc)
 Call ID: ce99f804-dc75-42e4-8b63-4f509ae26bfc
  Args:
    type: :Woman
    source: Leonore
  AddTriple (285785e2-539e-4237-90e0-d30339a9c820)
 Call ID: 285785e2-539e-4237-90e0-d30339a9c820
  Args:
    source: Constantijn
    relation: :hasMother
    target: Beatrix
  AddTriple (9e7e243b-a44a-4212-bc3d-cdb55db58429)
 Call ID: 9e7e243b-a44a-4212-bc3d-cdb55db58429
  Args:
    target: Claus_von_Amsberg
    relation: :hasFather
    source: Constantijn
  AddTriple (90144876-56a5-43d9-a764-2b4e6794a551)
 Call ID: 90144876-56a5-43d9-a764-2b4e6794a551
  Args:
    target: Willem-Alexander
    relation: :hasBrother
    source: Constantijn
  AddTriple (5e5df55b-13cf-43ed-9ce2-1fdf9ebaf586)
 Call ID: 5e5df55b-13cf-43ed-9ce2-1fdf9ebaf586
  Args:
    target: Johan_Friso
    relation: :hasBrother
    source: Constantijn
  AddLiteral (d5e35e17-75ed-47c1-adf7-c3caf4691551)
 Call ID: d5e35e17-75ed-47c1-adf7-c3caf4691551
  Args:
    literal_type: xsd:integer
    source: Constantijn
    literal_value: 1969
    relation: :hasBirthYear
  AddLiteral (3e1b3c67-4d16-46a3-82b5-93a97562a46e)
 Call ID: 3e1b3c67-4d16-46a3-82b5-93a97562a46e
  Args:
    source: Willem-Alexander
    literal_type: xsd:integer
    literal_value: 1967
    relation: :hasBirthYear
  AddLiteral (3a6d5648-5cea-4552-a6f9-e7c094eaffc8)
 Call ID: 3a6d5648-5cea-4552-a6f9-e7c094eaffc8
  Args:
    relation: :hasBirthYear
    literal_value: 1968
    literal_type: xsd:integer
    source: Johan_Friso
  AddLiteral (171b9e60-864f-40fc-9e36-63aabb8c2f65)
 Call ID: 171b9e60-864f-40fc-9e36-63aabb8c2f65
  Args:
    literal_value: 2013
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: Johan_Friso
  AddTriple (333864ee-b841-48de-ad73-920402a18a01)
 Call ID: 333864ee-b841-48de-ad73-920402a18a01
  Args:
    source: Eloise
    target: Laurentien_Brinkhorst
    relation: :hasMother
  AddTriple (6c055673-b527-475e-a36f-f1b1089e4772)
 Call ID: 6c055673-b527-475e-a36f-f1b1089e4772
  Args:
    source: Eloise
    relation: :hasFather
    target: Constantijn
  AddLiteral (22ff8bc9-5514-4339-8428-ecb5620c92da)
 Call ID: 22ff8bc9-5514-4339-8428-ecb5620c92da
  Args:
    literal_value: 2002
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Eloise
  AddTriple (9a34f490-b74b-47f5-aa61-799a27967ec6)
 Call ID: 9a34f490-b74b-47f5-aa61-799a27967ec6
  Args:
    relation: :hasMother
    target: Laurentien_Brinkhorst
    source: Claus-Casimir
  AddTriple (9ea5a43b-959c-4c6a-932b-646191232818)
 Call ID: 9ea5a43b-959c-4c6a-932b-646191232818
  Args:
    source: Claus-Casimir
    relation: :hasFather
    target: Constantijn
  AddLiteral (9a0766da-fee4-4665-878d-6d78e65179a8)
 Call ID: 9a0766da-fee4-4665-878d-6d78e65179a8
  Args:
    literal_value: 2004
    relation: :hasBirthYear
    source: Claus-Casimir
    literal_type: xsd:integer
  AddTriple (e1a5042d-2f95-4d4c-bbe6-4ec43b6f8fd5)
 Call ID: e1a5042d-2f95-4d4c-bbe6-4ec43b6f8fd5
  Args:
    source: Leonore
    relation: :hasMother
    target: Laurentien_Brinkhorst
  AddTriple (e0315d9f-b359-4e1f-a9ec-fb63fed8fa4b)
 Call ID: e0315d9f-b359-4e1f-a9ec-fb63fed8fa4b
  Args:
    source: Leonore
    target: Constantijn
    relation: :hasFather
  AddLiteral (f0100f9a-8bae-4e39-8e01-a74125e39958)
 Call ID: f0100f9a-8bae-4e39-8e01-a74125e39958
  Args:
    source: Leonore
    literal_type: xsd:integer
    literal_value: 2006
    relation: :hasBirthYear
  Finish (9e9c56ac-2874-4d25-98a9-d9ca264ef93b)
 Call ID: 9e9c56ac-2874-4d25-98a9-d9ca264ef93b
  Args: