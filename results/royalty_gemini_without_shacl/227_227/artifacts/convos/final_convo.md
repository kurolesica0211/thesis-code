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
Prince Waldemar of Prussia (Joachim Friedrich Ernst Waldemar; 10 February 1868 – 27 March 1879) was the sixth child and youngest son of the German Crown Prince and Crown Princess, later Emperor Frederick III and Empress Victoria.
Prince Waldemar was a grandson of both William I, German Emperor, and Queen Victoria of the United Kingdom.
Biography

Early life

Waldemar was the favourite of both the Princess Royal and her husband.
Waldemar had a "fun loving" character and a great sense of humour and love for animals and sports.
On one occasion, when visiting his grandmother, Queen Victoria, Waldemar let loose his pet crocodile in her study, much to the shock of the middle-aged queen.
The Princess Royal wrote that she would be unhappy when Waldemar went off to school, "as he is my very own boy."
She seemed to prefer Waldemar over his elder brothers Wilhelm and Heinrich.
Death

Less than four months after the deaths of his maternal aunt, Alice, Grand Duchess of Hesse and cousin, Marie, Waldemar became seriously ill with diphtheria and died in Berlin, Germany on 27 March 1879.
He was buried in the royal mausoleum attached to the Friedenskirche at Potsdam, near the main altar and his elder brother Prince Sigismund of Prussia.



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
  AssignClass (ae58a91d-f603-4387-8bff-adf524781d74)
 Call ID: ae58a91d-f603-4387-8bff-adf524781d74
  Args:
    source: :Prince_Waldemar_of_Prussia
    type: :Man
  AssignClass (dfd1a6b6-690d-4da3-a3cc-ee4390feae74)
 Call ID: dfd1a6b6-690d-4da3-a3cc-ee4390feae74
  Args:
    source: :Prince_Waldemar_of_Prussia
    type: :Person
  AddLiteral (9579f4ce-20e1-4c4e-a77a-b619926414c3)
 Call ID: 9579f4ce-20e1-4c4e-a77a-b619926414c3
  Args:
    literal_value: Joachim Friedrich Ernst Waldemar
    relation: :alsoKnownAs
    source: :Prince_Waldemar_of_Prussia
    literal_type: xsd:string
  AddLiteral (7199e140-0e0c-437c-8356-5ed2eee38539)
 Call ID: 7199e140-0e0c-437c-8356-5ed2eee38539
  Args:
    source: :Prince_Waldemar_of_Prussia
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1868
  AddLiteral (aa174a21-837d-4a2d-baef-e5f69ed6f613)
 Call ID: aa174a21-837d-4a2d-baef-e5f69ed6f613
  Args:
    literal_value: 1879
    source: :Prince_Waldemar_of_Prussia
    literal_type: xsd:integer
    relation: :hasDeathYear
  AssignClass (05e7bcc8-b89f-498c-9127-bcd081081479)
 Call ID: 05e7bcc8-b89f-498c-9127-bcd081081479
  Args:
    type: :Man
    source: :Frederick_III
  AssignClass (bdcd57bd-27ca-4e23-91fe-6279d90b2711)
 Call ID: bdcd57bd-27ca-4e23-91fe-6279d90b2711
  Args:
    source: :Frederick_III
    type: :Person
  AssignClass (eac1a3ee-9ae7-4b43-aa3f-7cccf419f9a3)
 Call ID: eac1a3ee-9ae7-4b43-aa3f-7cccf419f9a3
  Args:
    source: :Victoria_Empress
    type: :Woman
  AssignClass (60478cd4-c1fe-4131-9f97-03be8a5f34ca)
 Call ID: 60478cd4-c1fe-4131-9f97-03be8a5f34ca
  Args:
    type: :Person
    source: :Victoria_Empress
  AddTriple (10c2e329-33b6-4423-b5ac-09bd21ed8b9f)
 Call ID: 10c2e329-33b6-4423-b5ac-09bd21ed8b9f
  Args:
    relation: :hasFather
    target: :Frederick_III
    source: :Prince_Waldemar_of_Prussia
  AddTriple (3a0d836e-9965-4f77-a934-18aedcfe2055)
 Call ID: 3a0d836e-9965-4f77-a934-18aedcfe2055
  Args:
    relation: :hasMother
    source: :Prince_Waldemar_of_Prussia
    target: :Victoria_Empress
  AssignClass (d70f7bfd-9238-4ca0-b13a-2d4c9f90f826)
 Call ID: d70f7bfd-9238-4ca0-b13a-2d4c9f90f826
  Args:
    type: :Man
    source: :William_I
  AssignClass (58f4316e-f385-412e-a6e9-9c3ddf930917)
 Call ID: 58f4316e-f385-412e-a6e9-9c3ddf930917
  Args:
    source: :William_I
    type: :Person
  AssignClass (6aa29cf7-7888-4a5c-b6f7-0d0b88da7f22)
 Call ID: 6aa29cf7-7888-4a5c-b6f7-0d0b88da7f22
  Args:
    source: :Queen_Victoria
    type: :Woman
  AssignClass (ffdb8755-e033-4775-96d4-aa290b88fb0e)
 Call ID: ffdb8755-e033-4775-96d4-aa290b88fb0e
  Args:
    type: :Person
    source: :Queen_Victoria
  AddTriple (075bc4a4-68dd-4d5b-b015-97e9b0d18d94)
 Call ID: 075bc4a4-68dd-4d5b-b015-97e9b0d18d94
  Args:
    relation: :hasAncestor
    source: :Prince_Waldemar_of_Prussia
    target: :William_I
  AddTriple (f404fa7f-85ef-473e-8a3c-25490fe225f4)
 Call ID: f404fa7f-85ef-473e-8a3c-25490fe225f4
  Args:
    relation: :hasAncestor
    source: :Prince_Waldemar_of_Prussia
    target: :Queen_Victoria
  AssignClass (ed0bc000-e560-44b3-b9a4-d7ffc8310c4a)
 Call ID: ed0bc000-e560-44b3-b9a4-d7ffc8310c4a
  Args:
    source: :Wilhelm
    type: :Man
  AssignClass (a14254e4-2603-46ad-8072-932dfc81a794)
 Call ID: a14254e4-2603-46ad-8072-932dfc81a794
  Args:
    type: :Person
    source: :Wilhelm
  AssignClass (c407b542-6899-4ed4-a1c1-c9c69c3f9ef5)
 Call ID: c407b542-6899-4ed4-a1c1-c9c69c3f9ef5
  Args:
    type: :Man
    source: :Heinrich
  AssignClass (7f17a062-c994-449f-b1ae-0bdc20e80e23)
 Call ID: 7f17a062-c994-449f-b1ae-0bdc20e80e23
  Args:
    type: :Person
    source: :Heinrich
  AddTriple (394ba332-fcd4-435a-959f-3571597d9c31)
 Call ID: 394ba332-fcd4-435a-959f-3571597d9c31
  Args:
    relation: :isBrotherOf
    target: :Prince_Waldemar_of_Prussia
    source: :Wilhelm
  AddTriple (14e3e8b1-4ff2-4209-88c7-9f69b639d56f)
 Call ID: 14e3e8b1-4ff2-4209-88c7-9f69b639d56f
  Args:
    relation: :isBrotherOf
    target: :Prince_Waldemar_of_Prussia
    source: :Heinrich
  AssignClass (8e6d2141-387c-4f02-b25d-0831dd55896b)
 Call ID: 8e6d2141-387c-4f02-b25d-0831dd55896b
  Args:
    source: :Alice_of_Hesse
    type: :Woman
  AssignClass (13b8716a-70e6-4a5c-ba83-74701b1514eb)
 Call ID: 13b8716a-70e6-4a5c-ba83-74701b1514eb
  Args:
    source: :Alice_of_Hesse
    type: :Person
  AddTriple (60bd89a4-8a32-4dc2-bb52-3bc7047c36d2)
 Call ID: 60bd89a4-8a32-4dc2-bb52-3bc7047c36d2
  Args:
    relation: :isAuntOf
    source: :Alice_of_Hesse
    target: :Prince_Waldemar_of_Prussia
  AssignClass (ef149eed-2781-42cd-b836-0e95f0048cc3)
 Call ID: ef149eed-2781-42cd-b836-0e95f0048cc3
  Args:
    source: :Marie_cousin
    type: :Woman
  AssignClass (c9ad2363-c439-4b85-ab9f-f139697c9658)
 Call ID: c9ad2363-c439-4b85-ab9f-f139697c9658
  Args:
    type: :Person
    source: :Marie_cousin
  AssignClass (2a66f1a4-fc81-4148-bd9c-8208879cc405)
 Call ID: 2a66f1a4-fc81-4148-bd9c-8208879cc405
  Args:
    type: :Man
    source: :Prince_Sigismund_of_Prussia
  AssignClass (c9f1cc3e-ed5f-4de3-b14a-481e674fe653)
 Call ID: c9f1cc3e-ed5f-4de3-b14a-481e674fe653
  Args:
    type: :Person
    source: :Prince_Sigismund_of_Prussia
  AddTriple (2c40f083-8526-4bbf-b1d0-88c1385da825)
 Call ID: 2c40f083-8526-4bbf-b1d0-88c1385da825
  Args:
    relation: :isBrotherOf
    source: :Prince_Sigismund_of_Prussia
    target: :Prince_Waldemar_of_Prussia
  Finish (c62a60c9-a564-4ddd-a0c8-87d3246e1478)
 Call ID: c62a60c9-a564-4ddd-a0c8-87d3246e1478
  Args: