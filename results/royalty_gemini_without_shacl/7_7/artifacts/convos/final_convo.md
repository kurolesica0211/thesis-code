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
Earl of Lichfield is a title that has been created three times, twice in the  Peerage of England (1645 and 1674) and once in the Peerage of the United Kingdom (1831).
Following his father's death in 1960, Patrick Anson, 5th Earl of Lichfield, decided to give Shugborough Hall up to the National Trust in lieu of death duties, an arrangement finalized in 1966.
For his own burial, he chose the Anson vault at Colwich and was buried there in 2005.
Earls of Lichfield, third creation (1831)

The third creation, in the Peerage of the United Kingdom, came in William IV's coronation honours of 1831 in favour of Thomas Anson, 2nd Viscount Anson (1795–1854), a landowner and Whig politician from the Anson family who served as Master of the Buckhounds from 1830 to 1834 and as Postmaster General from 1835 to 1841.
The 1st Earl was the eldest son of Thomas Anson, 1st Viscount Anson, who on 17 February 1806 had been created Baron Soberton, of Soberton in the County of Southampton, and Viscount Anson, of Shugborough and Orgreave in the County of Stafford, both in the Peerage of the United Kingdom.
Also in 1831, the 1st Earl's cousin William Anson was made a baronet (see Anson Baronets).
The earldom of Lichfield continued to descend within the Anson family from father to son until the death of the 4th Earl, in 1960.
He was succeeded by his grandson, the 5th Earl, the only son of Lieutenant-Colonel Thomas William Arnold Anson, Viscount Anson (1913–1958), eldest son of the 4th Earl.
Known professionally as Patrick Lichfield, he was a successful photographer.
As of 2017 the titles are held by the 6th Earl, only son of the 5th Earl and Lady Leonora Grosvenor, daughter of the 5th Duke of Westminster.
He succeeded as the 6th Earl of Lichfield upon his father's death on 11 November 2005.
The 6th Earl married in December 2009 Lady Henrietta Conyngham, daughter of Henry Conyngham, 8th Marquess Conyngham.
List of title holders

Earls of Lichfield (1645)

Earls of Lichfield (1674)

Earls of Lichfield (1831)
Present peer

Thomas William Robert Hugh Anson, 6th Earl of Lichfield (born 19 July 1978) is the son of the 5th Earl and his wife Lady Leonora Mary Grosvenor.
Styled as Viscount Anson from birth, on 11 November 2005 he succeeded his father as Earl of Lichfield (UK, 1831), Viscount Anson, of Shugborough (UK, 1806), and Baron Soberton (UK, 1806).
They have two children, Thomas Ossian Patrick Wolfe Anson, Viscount Anson (born 2011), and the Hon.
Finnian Anson (born 2014).



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
  AssignClass (892b0c39-f38b-4a52-a85f-3229a649c0e9)
 Call ID: 892b0c39-f38b-4a52-a85f-3229a649c0e9
  Args:
    type: :Man
    source: ThomasAnson_2ndViscountAnson
  AssignClass (de6cd17b-7cf2-4f40-b796-1b856337175d)
 Call ID: de6cd17b-7cf2-4f40-b796-1b856337175d
  Args:
    type: :Person
    source: ThomasAnson_2ndViscountAnson
  AddLiteral (4c6ad2c6-2586-4374-bffb-ccdd7476287f)
 Call ID: 4c6ad2c6-2586-4374-bffb-ccdd7476287f
  Args:
    relation: :hasBirthYear
    literal_value: 1795
    source: ThomasAnson_2ndViscountAnson
    literal_type: xsd:integer
  AddLiteral (33459303-a0fb-4e7d-a40e-01df2c1063f4)
 Call ID: 33459303-a0fb-4e7d-a40e-01df2c1063f4
  Args:
    literal_value: 1854
    literal_type: xsd:integer
    source: ThomasAnson_2ndViscountAnson
    relation: :hasDeathYear
  AddLiteral (8cebbc16-1072-48a2-8e20-7ece1c788a08)
 Call ID: 8cebbc16-1072-48a2-8e20-7ece1c788a08
  Args:
    relation: :knownAs
    literal_value: 1st Earl of Lichfield
    literal_type: xsd:string
    source: ThomasAnson_2ndViscountAnson
  AssignClass (bccdac5b-dfe3-4a22-b9e7-049f27ea9e87)
 Call ID: bccdac5b-dfe3-4a22-b9e7-049f27ea9e87
  Args:
    type: :Man
    source: ThomasAnson_1stViscountAnson
  AssignClass (172244c5-837e-49e9-b8dd-64e6312d514b)
 Call ID: 172244c5-837e-49e9-b8dd-64e6312d514b
  Args:
    type: :Person
    source: ThomasAnson_1stViscountAnson
  AddTriple (408f2bb3-6625-4b98-8d85-3e772291c2c9)
 Call ID: 408f2bb3-6625-4b98-8d85-3e772291c2c9
  Args:
    source: ThomasAnson_1stViscountAnson
    target: ThomasAnson_2ndViscountAnson
    relation: :isFatherOf
  AssignClass (9144ad4e-0b3b-4ee5-aecc-e13c1471e945)
 Call ID: 9144ad4e-0b3b-4ee5-aecc-e13c1471e945
  Args:
    source: ThomasWilliamArnoldAnson_ViscountAnson
    type: :Man
  AssignClass (6a49fdc2-b9e2-42b6-a9d5-903d6cd0a2d6)
 Call ID: 6a49fdc2-b9e2-42b6-a9d5-903d6cd0a2d6
  Args:
    type: :Person
    source: ThomasWilliamArnoldAnson_ViscountAnson
  AddLiteral (69e12f02-d117-4262-9133-c77dca49a704)
 Call ID: 69e12f02-d117-4262-9133-c77dca49a704
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: ThomasWilliamArnoldAnson_ViscountAnson
    literal_value: 1913
  AddLiteral (3d776217-4fe5-4e6a-9bef-aeb0fb3c84ae)
 Call ID: 3d776217-4fe5-4e6a-9bef-aeb0fb3c84ae
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: ThomasWilliamArnoldAnson_ViscountAnson
    literal_value: 1958
  AssignClass (18c4c056-d1d1-486a-aa3c-795bae2a13ef)
 Call ID: 18c4c056-d1d1-486a-aa3c-795bae2a13ef
  Args:
    source: PatrickAnson_5thEarlOfLichfield
    type: :Man
  AssignClass (1249a9a3-13a7-4518-bb8a-86a79ce26ea5)
 Call ID: 1249a9a3-13a7-4518-bb8a-86a79ce26ea5
  Args:
    source: PatrickAnson_5thEarlOfLichfield
    type: :Person
  AddTriple (648a6aa2-90ce-45be-a2ba-2f0fd7c5237f)
 Call ID: 648a6aa2-90ce-45be-a2ba-2f0fd7c5237f
  Args:
    target: ThomasWilliamArnoldAnson_ViscountAnson
    relation: :hasFather
    source: PatrickAnson_5thEarlOfLichfield
  AddLiteral (138ee568-595f-4ed1-bf1d-ba8e57d55e22)
 Call ID: 138ee568-595f-4ed1-bf1d-ba8e57d55e22
  Args:
    literal_value: 2005
    source: PatrickAnson_5thEarlOfLichfield
    literal_type: xsd:integer
    relation: :hasDeathYear
  AddLiteral (d69c728c-966e-4f43-a443-76be9bfe8d93)
 Call ID: d69c728c-966e-4f43-a443-76be9bfe8d93
  Args:
    relation: :knownAs
    literal_value: Patrick Lichfield
    literal_type: xsd:string
    source: PatrickAnson_5thEarlOfLichfield
  AssignClass (6a9b0b35-dd4b-486d-9ec8-f3c875f0baf8)
 Call ID: 6a9b0b35-dd4b-486d-9ec8-f3c875f0baf8
  Args:
    source: ThomasWilliamRobertHughAnson_6thEarlOfLichfield
    type: :Man
  AssignClass (016602cb-8f74-4566-8393-70bbc4e2cd9d)
 Call ID: 016602cb-8f74-4566-8393-70bbc4e2cd9d
  Args:
    type: :Person
    source: ThomasWilliamRobertHughAnson_6thEarlOfLichfield
  AddLiteral (ed5f73f8-0171-4ac9-b310-b6d567041791)
 Call ID: ed5f73f8-0171-4ac9-b310-b6d567041791
  Args:
    literal_value: 1978
    source: ThomasWilliamRobertHughAnson_6thEarlOfLichfield
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddTriple (a02dfbfc-e6f3-4e0a-a599-211a8a775f95)
 Call ID: a02dfbfc-e6f3-4e0a-a599-211a8a775f95
  Args:
    relation: :hasFather
    target: PatrickAnson_5thEarlOfLichfield
    source: ThomasWilliamRobertHughAnson_6thEarlOfLichfield
  AssignClass (501d62c4-b894-41d9-8e6a-bab8a3c0b1a8)
 Call ID: 501d62c4-b894-41d9-8e6a-bab8a3c0b1a8
  Args:
    type: :Woman
    source: LadyLeonoraMaryGrosvenor
  AssignClass (4f7cd160-cc03-46ea-8129-f933aec14000)
 Call ID: 4f7cd160-cc03-46ea-8129-f933aec14000
  Args:
    type: :Person
    source: LadyLeonoraMaryGrosvenor
  AddTriple (e5401b77-f87a-4f40-9c8d-452acea04f95)
 Call ID: e5401b77-f87a-4f40-9c8d-452acea04f95
  Args:
    relation: :hasMother
    target: LadyLeonoraMaryGrosvenor
    source: ThomasWilliamRobertHughAnson_6thEarlOfLichfield
  AssignClass (9bea386c-474b-4a35-96a2-27f3b71a0f29)
 Call ID: 9bea386c-474b-4a35-96a2-27f3b71a0f29
  Args:
    type: :Man
    source: ThomasOssianPatrickWolfeAnson_ViscountAnson
  AssignClass (eaf62c97-c9f0-48e2-b946-6bfe47a2d0ba)
 Call ID: eaf62c97-c9f0-48e2-b946-6bfe47a2d0ba
  Args:
    type: :Person
    source: ThomasOssianPatrickWolfeAnson_ViscountAnson
  AddLiteral (bdfb6af6-1131-45f5-a62c-32763ca4e050)
 Call ID: bdfb6af6-1131-45f5-a62c-32763ca4e050
  Args:
    source: ThomasOssianPatrickWolfeAnson_ViscountAnson
    literal_type: xsd:integer
    literal_value: 2011
    relation: :hasBirthYear
  AddTriple (b52c1edb-6860-4d9c-a633-23e46bae7abb)
 Call ID: b52c1edb-6860-4d9c-a633-23e46bae7abb
  Args:
    source: ThomasOssianPatrickWolfeAnson_ViscountAnson
    relation: :hasFather
    target: ThomasWilliamRobertHughAnson_6thEarlOfLichfield
  AssignClass (82c3c715-e991-472f-996e-c1f7419591c4)
 Call ID: 82c3c715-e991-472f-996e-c1f7419591c4
  Args:
    type: :Man
    source: FinnianAnson
  AssignClass (6ec5f1de-20ae-4497-a3b0-8578c8a64f0c)
 Call ID: 6ec5f1de-20ae-4497-a3b0-8578c8a64f0c
  Args:
    type: :Person
    source: FinnianAnson
  AddLiteral (e2874e79-86a8-4cfc-8194-1b459cc0d3dd)
 Call ID: e2874e79-86a8-4cfc-8194-1b459cc0d3dd
  Args:
    relation: :hasBirthYear
    literal_value: 2014
    literal_type: xsd:integer
    source: FinnianAnson
  AddTriple (270e38ab-3788-48f9-b041-0e87ca93fce1)
 Call ID: 270e38ab-3788-48f9-b041-0e87ca93fce1
  Args:
    source: FinnianAnson
    relation: :hasFather
    target: ThomasWilliamRobertHughAnson_6thEarlOfLichfield
  AssignClass (a682363a-fad5-4102-82f4-d040743b5c02)
 Call ID: a682363a-fad5-4102-82f4-d040743b5c02
  Args:
    type: :Woman
    source: LadyHenriettaConyngham
  AssignClass (a2e34fa9-2696-4dac-947f-55f256cd6d73)
 Call ID: a2e34fa9-2696-4dac-947f-55f256cd6d73
  Args:
    type: :Person
    source: LadyHenriettaConyngham
  AddTriple (97673e61-5b9d-49c2-b7d0-e07f72774750)
 Call ID: 97673e61-5b9d-49c2-b7d0-e07f72774750
  Args:
    source: ThomasOssianPatrickWolfeAnson_ViscountAnson
    target: LadyHenriettaConyngham
    relation: :hasMother
  AddTriple (0ac4366e-6ef4-4795-a3df-c7e02d3a7830)
 Call ID: 0ac4366e-6ef4-4795-a3df-c7e02d3a7830
  Args:
    relation: :hasMother
    target: LadyHenriettaConyngham
    source: FinnianAnson
  Finish (9cdaecf5-a370-43bc-b3c3-fd7218e4e409)
 Call ID: 9cdaecf5-a370-43bc-b3c3-fd7218e4e409
  Args: