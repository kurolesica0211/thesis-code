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
Captain George Louis Victor Henry Serge Mountbatten, 2nd Marquess of Milford Haven (6 November 1892 – 8 April 1938), born Prince George of Battenberg, styled Earl of Medina between 1917 and 1921, was a Royal Navy officer and the elder son of Louis Mountbatten, 1st Marquess of Milford Haven (Prince Louis of Battenberg), and Princess Victoria of Hesse and by Rhine.
Biography

George was born 6 November 1892 in Darmstadt in the Grand Duchy of Hesse, then ruled by his maternal uncle Ernest Louis, Grand Duke of Hesse.
From birth, he was a prince of the Hessian royal family, albeit of a morganatic branch.
His siblings were Princess Alice (mother of Prince Philip, Duke of Edinburgh, to whom he was a mentor in Philip's adolescence), Queen Louise of Sweden and Louis Mountbatten, 1st
Earl Mountbatten of Burma (who assumed the role of Philip's mentor after George's death).
George followed his father into the Royal Navy, and after passing out from the Royal Naval College at Dartmouth, was promoted to sub-lieutenant on 15 January 1913.
In 1917, his father and several of his relations relinquished their German names, styles and titles in exchange for British peerages at the behest of George V. Accordingly, Prince George dropped the style of Serene Highness and his surname was anglicised to "Mountbatten."
When his father was created Marquess of Milford Haven in late 1917, George received the courtesy title of Earl of Medina, succeeding to his father's peerage after his death in September 1921.
Lord Milford Haven, as George was now known, remained in the Royal Navy after the war; he was promoted to lieutenant-commander on 15 February 1922 and to commander on 31 December 1926.
An accomplished mathematician, the Marquess "could work out complicated gunnery problems in his head" and "read books on calculus casually on trains".
Marriage and issue

Prince George of Battenberg, as he then was known, married Countess Nadejda Mikhailovna de Torby (daughter of Russian Grand Duke Michael Mikhailovich Romanov and his morganatic wife, Countess Sophie von Merenberg) on 15 November 1916 at the Russian Embassy, Welbeck Street, London.
They lived at Lynden Manor at Holyport in Berkshire and had two children:


Death

Lord Milford Haven died in London on 8 April 1938 of bone marrow cancer, aged 45.
His funeral took place at St Michael's Church, Bray, Berkshire, and he was buried in Bray Parish Cemetery.
Legacy to the British Museum

Lord Milford Haven left a collection of pornography, including artificial sex organs, to the British Museum.



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
  AssignClass (64ee7903-9b90-4072-a9a8-8efb1bf5cbce)
 Call ID: 64ee7903-9b90-4072-a9a8-8efb1bf5cbce
  Args:
    type: :Man
    source: GeorgeMountbatten
  AssignClass (01f39cc4-936a-41a0-8e04-f849bef1c7ae)
 Call ID: 01f39cc4-936a-41a0-8e04-f849bef1c7ae
  Args:
    type: :Person
    source: GeorgeMountbatten
  AssignClass (031dec6b-48b4-4cb1-869b-07f358967f41)
 Call ID: 031dec6b-48b4-4cb1-869b-07f358967f41
  Args:
    type: :Man
    source: LouisMountbatten1stMarquess
  AssignClass (074f43c9-2f06-4b49-9a7b-0b323a8575f4)
 Call ID: 074f43c9-2f06-4b49-9a7b-0b323a8575f4
  Args:
    type: :Ancestor
    source: LouisMountbatten1stMarquess
  AssignClass (5a676d13-3d23-4a26-ada4-0f765a0a56fc)
 Call ID: 5a676d13-3d23-4a26-ada4-0f765a0a56fc
  Args:
    type: :Woman
    source: VictoriaOfHesse
  AssignClass (61369d0c-a8b1-44ba-aed6-768bd8ad5767)
 Call ID: 61369d0c-a8b1-44ba-aed6-768bd8ad5767
  Args:
    type: :Ancestor
    source: VictoriaOfHesse
  AssignClass (4f3138af-db83-47d3-b1bf-9ce058205292)
 Call ID: 4f3138af-db83-47d3-b1bf-9ce058205292
  Args:
    type: :Woman
    source: PrincessAlice
  AssignClass (e47e4fa9-b0d7-499e-8383-b96896a933fc)
 Call ID: e47e4fa9-b0d7-499e-8383-b96896a933fc
  Args:
    type: :Woman
    source: QueenLouiseOfSweden
  AssignClass (686aa89e-749a-499c-be72-f24df4c5d7e5)
 Call ID: 686aa89e-749a-499c-be72-f24df4c5d7e5
  Args:
    type: :Man
    source: LouisMountbatten1stEarl
  AssignClass (80e343cf-7a48-4b59-86a9-2ad61c2e999c)
 Call ID: 80e343cf-7a48-4b59-86a9-2ad61c2e999c
  Args:
    type: :Woman
    source: NadejdaMikhailovnaDeTorby
  AssignClass (dc466aab-5fc4-4d8a-8ae8-597b5c5bd593)
 Call ID: dc466aab-5fc4-4d8a-8ae8-597b5c5bd593
  Args:
    type: :Man
    source: MichaelMikhailovichRomanov
  AssignClass (2ccab4c8-2856-4aef-a180-5ad23189e4bd)
 Call ID: 2ccab4c8-2856-4aef-a180-5ad23189e4bd
  Args:
    type: :Woman
    source: SophieVonMerenberg
  AddLiteral (0e033061-c078-4a39-accb-ed72a271c3f8)
 Call ID: 0e033061-c078-4a39-accb-ed72a271c3f8
  Args:
    source: GeorgeMountbatten
    relation: :hasBirthYear
    literal_value: 1892
    literal_type: xsd:integer
  AddLiteral (759fa954-4544-4e9f-b647-1c6306e35fd6)
 Call ID: 759fa954-4544-4e9f-b647-1c6306e35fd6
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1938
    source: GeorgeMountbatten
  AddTriple (fa3ad3d4-76b7-47cc-ab1f-75996db412b9)
 Call ID: fa3ad3d4-76b7-47cc-ab1f-75996db412b9
  Args:
    relation: :hasFather
    target: LouisMountbatten1stMarquess
    source: GeorgeMountbatten
  AddTriple (7f5dfce7-58a8-4707-afa6-1f650cf228e3)
 Call ID: 7f5dfce7-58a8-4707-afa6-1f650cf228e3
  Args:
    source: GeorgeMountbatten
    target: VictoriaOfHesse
    relation: :hasMother
  AddTriple (9378cc9d-d992-432a-bb8f-3a52b0b1cd90)
 Call ID: 9378cc9d-d992-432a-bb8f-3a52b0b1cd90
  Args:
    source: GeorgeMountbatten
    target: PrincessAlice
    relation: :isSiblingOf
  AddTriple (364dd9c9-2d41-4e61-a1a1-68f3088c92db)
 Call ID: 364dd9c9-2d41-4e61-a1a1-68f3088c92db
  Args:
    relation: :isSiblingOf
    target: QueenLouiseOfSweden
    source: GeorgeMountbatten
  AddTriple (b21af267-b401-4b74-8ac3-362ae3c5a536)
 Call ID: b21af267-b401-4b74-8ac3-362ae3c5a536
  Args:
    target: LouisMountbatten1stEarl
    relation: :isSiblingOf
    source: GeorgeMountbatten
  AddLiteral (ef92e073-ef7a-4103-8fb9-c53867f244b7)
 Call ID: ef92e073-ef7a-4103-8fb9-c53867f244b7
  Args:
    source: GeorgeMountbatten
    literal_value: 1916
    relation: :hasMarriageYear
    literal_type: xsd:integer
  AddTriple (ca311e2f-3e5a-46de-8101-1418c3911db9)
 Call ID: ca311e2f-3e5a-46de-8101-1418c3911db9
  Args:
    relation: :hasRelation
    target: NadejdaMikhailovnaDeTorby
    source: GeorgeMountbatten
  AddTriple (3ba372e9-7efc-4be8-879c-f59cdf347807)
 Call ID: 3ba372e9-7efc-4be8-879c-f59cdf347807
  Args:
    source: NadejdaMikhailovnaDeTorby
    relation: :hasFather
    target: MichaelMikhailovichRomanov
  AddTriple (98d7621d-5d02-4505-8cfd-cf9a243196b8)
 Call ID: 98d7621d-5d02-4505-8cfd-cf9a243196b8
  Args:
    source: NadejdaMikhailovnaDeTorby
    target: SophieVonMerenberg
    relation: :hasMother
  Finish (743d04e6-4ef5-45b9-aad7-7335c32c2d7d)
 Call ID: 743d04e6-4ef5-45b9-aad7-7335c32c2d7d
  Args: