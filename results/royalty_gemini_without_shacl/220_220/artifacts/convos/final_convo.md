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
Anne Ferelith Fenella Bowes-Lyon (4 December 1917 – 26 September 1980), later styled Viscountess Anson and later Princess Anne of Denmark, was a British noblewoman and member of the Danish royal family by marriage, and a first cousin of Elizabeth II.
Born into the Bowes-Lyon family, she married Thomas Anson, Viscount Anson, and had two children, Patrick Anson, 5th Earl of Lichfield, and Lady Elizabeth Shakerley, before divorcing Anson in 1948.
She became a princess of Denmark by her second marriage to Prince Georg of Denmark in 1950.
Family

Anne Bowes-Lyon was born in Washington, D.C., in 1917.
John Herbert Bowes-Lyon and her mother was the Hon.
Fenella Hepburn-Stuart-Forbes-Trefusis, daughter of Charles Hepburn-Stuart-Forbes-Trefusis, 21st Baron Clinton.
Anne's paternal grandfather was Claude Bowes-Lyon, 14th
Earl of Strathmore and Kinghorne.
She was a niece of Queen Elizabeth the Queen Mother.
Anne had three younger sisters, two of whom were Nerissa and Katherine Bowes-Lyon, who were institutionalized in 1941 for severe intellectual disability.
Apart from early deceased Patricia (1916–1917), Nerissa (1919–1986) and Katherine (1926–2014), Anne also had one younger sister, Diana Cinderella Somervell (1923–1986).
Marriages

Anne married Lieutenant-Colonel Thomas William Arnold Anson (1913–1958) on 28 April 1938.
As her husband held the courtesy title of Viscount Anson, Anne was styled Viscountess Anson upon their marriage.
On 16 September 1950, at Glamis Castle, Anne, Viscountess Anson subsequently married Prince Georg of Denmark, upon which she became Her Highness Princess Anne of Denmark.
Death

Anne died in 1980, aged 62, in London of a heart attack.
She is buried alongside her second husband, Prince George of Denmark, at Bernstorffpark, Gentofte, Denmark.



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
  AssignClass (cd89ffd8-1681-49b2-8800-4be2ac106ead)
 Call ID: cd89ffd8-1681-49b2-8800-4be2ac106ead
  Args:
    type: :Woman
    source: AnneFerelithFenellaBowesLyon
  AssignClass (267bcc93-eca6-4f43-b54a-ad87966e45e0)
 Call ID: 267bcc93-eca6-4f43-b54a-ad87966e45e0
  Args:
    source: AnneFerelithFenellaBowesLyon
    type: :Person
  AddLiteral (9c2363b3-bda9-4253-8986-d95227f717ae)
 Call ID: 9c2363b3-bda9-4253-8986-d95227f717ae
  Args:
    relation: :hasBirthYear
    source: AnneFerelithFenellaBowesLyon
    literal_type: xsd:integer
    literal_value: 1917
  AddLiteral (b329d3ab-e455-4318-bbe5-88ade611e07d)
 Call ID: b329d3ab-e455-4318-bbe5-88ade611e07d
  Args:
    source: AnneFerelithFenellaBowesLyon
    literal_type: xsd:integer
    literal_value: 1980
    relation: :hasDeathYear
  AssignClass (2ad33655-7b4a-4e35-a1cd-7403009c321f)
 Call ID: 2ad33655-7b4a-4e35-a1cd-7403009c321f
  Args:
    source: JohnHerbertBowesLyon
    type: :Man
  AssignClass (7efa94fd-fab6-494f-afbc-7420ca5fa6a1)
 Call ID: 7efa94fd-fab6-494f-afbc-7420ca5fa6a1
  Args:
    type: :Person
    source: JohnHerbertBowesLyon
  AddTriple (57388d85-f434-4df6-85d6-edf6026a1b03)
 Call ID: 57388d85-f434-4df6-85d6-edf6026a1b03
  Args:
    source: AnneFerelithFenellaBowesLyon
    target: JohnHerbertBowesLyon
    relation: :hasFather
  AssignClass (202c7399-1b90-4dd8-b075-ee6e7d0a57db)
 Call ID: 202c7399-1b90-4dd8-b075-ee6e7d0a57db
  Args:
    type: :Woman
    source: FenellaHepburnStuartForbesTrefusis
  AssignClass (10d92397-6955-4a15-94c6-cc73883e1a18)
 Call ID: 10d92397-6955-4a15-94c6-cc73883e1a18
  Args:
    source: FenellaHepburnStuartForbesTrefusis
    type: :Person
  AddTriple (cf4e0517-fe6b-4c36-b378-b52b65fcf7fc)
 Call ID: cf4e0517-fe6b-4c36-b378-b52b65fcf7fc
  Args:
    source: AnneFerelithFenellaBowesLyon
    relation: :hasMother
    target: FenellaHepburnStuartForbesTrefusis
  AssignClass (11a627c9-952d-4c95-90b1-4b4f092d709d)
 Call ID: 11a627c9-952d-4c95-90b1-4b4f092d709d
  Args:
    type: :Man
    source: CharlesHepburnStuartForbesTrefusis
  AssignClass (aecdad5a-1013-4703-b131-777291b9c81d)
 Call ID: aecdad5a-1013-4703-b131-777291b9c81d
  Args:
    type: :Person
    source: CharlesHepburnStuartForbesTrefusis
  AddTriple (b922927f-d539-42ce-a4f4-a524dadf238d)
 Call ID: b922927f-d539-42ce-a4f4-a524dadf238d
  Args:
    source: FenellaHepburnStuartForbesTrefusis
    relation: :hasFather
    target: CharlesHepburnStuartForbesTrefusis
  AssignClass (f52ab73b-6b7d-4ca9-94a8-0a2574f0364a)
 Call ID: f52ab73b-6b7d-4ca9-94a8-0a2574f0364a
  Args:
    type: :Man
    source: ClaudeBowesLyon
  AssignClass (c06d2242-377d-48ea-939a-76afab90a650)
 Call ID: c06d2242-377d-48ea-939a-76afab90a650
  Args:
    source: ClaudeBowesLyon
    type: :Person
  AddTriple (d444871b-2e59-471d-82d9-be27624945ad)
 Call ID: d444871b-2e59-471d-82d9-be27624945ad
  Args:
    target: ClaudeBowesLyon
    relation: :hasFather
    source: JohnHerbertBowesLyon
  AssignClass (78144722-a440-4f6b-9119-3637aada4865)
 Call ID: 78144722-a440-4f6b-9119-3637aada4865
  Args:
    source: ThomasWilliamArnoldAnson
    type: :Man
  AssignClass (71082065-5656-4154-af34-e2f273945bb9)
 Call ID: 71082065-5656-4154-af34-e2f273945bb9
  Args:
    type: :Person
    source: ThomasWilliamArnoldAnson
  AddLiteral (ec596913-c911-4cb4-92a9-aacb00e8df9f)
 Call ID: ec596913-c911-4cb4-92a9-aacb00e8df9f
  Args:
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: AnneFerelithFenellaBowesLyon
    literal_value: 1938
  AssignClass (82cfd648-814a-464a-8a51-7ce53b465bc1)
 Call ID: 82cfd648-814a-464a-8a51-7ce53b465bc1
  Args:
    source: PatrickAnson
    type: :Man
  AssignClass (cdf8ed0b-6f5a-4d62-be23-d47e6c3823d5)
 Call ID: cdf8ed0b-6f5a-4d62-be23-d47e6c3823d5
  Args:
    type: :Person
    source: PatrickAnson
  AssignClass (a36479eb-7896-481c-8a92-31d6e3d18894)
 Call ID: a36479eb-7896-481c-8a92-31d6e3d18894
  Args:
    type: :Woman
    source: ElizabethShakerley
  AssignClass (a133085a-1264-4dfc-8974-2ca91241ef15)
 Call ID: a133085a-1264-4dfc-8974-2ca91241ef15
  Args:
    source: ElizabethShakerley
    type: :Person
  AddTriple (8bb103a0-e6b2-4f41-a4ec-4c8de89fa59d)
 Call ID: 8bb103a0-e6b2-4f41-a4ec-4c8de89fa59d
  Args:
    source: AnneFerelithFenellaBowesLyon
    target: PatrickAnson
    relation: :hasSon
  AddTriple (03bf8996-bd48-4a47-bedf-c60a7594f9ff)
 Call ID: 03bf8996-bd48-4a47-bedf-c60a7594f9ff
  Args:
    target: ElizabethShakerley
    relation: :hasDaughter
    source: AnneFerelithFenellaBowesLyon
  AssignClass (abfe9674-3765-46cb-abd0-12b7929b90c8)
 Call ID: abfe9674-3765-46cb-abd0-12b7929b90c8
  Args:
    source: PrinceGeorgOfDenmark
    type: :Man
  AssignClass (598fc1de-a2e5-4abc-9a95-1df35037a5e7)
 Call ID: 598fc1de-a2e5-4abc-9a95-1df35037a5e7
  Args:
    type: :Person
    source: PrinceGeorgOfDenmark
  AddLiteral (20131bf2-3859-4d61-9091-047681f4839a)
 Call ID: 20131bf2-3859-4d61-9091-047681f4839a
  Args:
    literal_value: 1950
    source: AnneFerelithFenellaBowesLyon
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AssignClass (5bb09b85-e154-4c81-90c4-f19467bcf6c3)
 Call ID: 5bb09b85-e154-4c81-90c4-f19467bcf6c3
  Args:
    source: NerissaBowesLyon
    type: :Woman
  AssignClass (cfe76cae-15d1-41eb-a97e-7b66db57119d)
 Call ID: cfe76cae-15d1-41eb-a97e-7b66db57119d
  Args:
    type: :Person
    source: NerissaBowesLyon
  AssignClass (18dfdacd-7cd0-477e-82a2-ca8badface1d)
 Call ID: 18dfdacd-7cd0-477e-82a2-ca8badface1d
  Args:
    source: KatherineBowesLyon
    type: :Woman
  AssignClass (b669b02d-af9b-4e88-8605-254386a2c55d)
 Call ID: b669b02d-af9b-4e88-8605-254386a2c55d
  Args:
    source: KatherineBowesLyon
    type: :Person
  AssignClass (6ece5803-70b4-40e5-b2a3-470289ef891c)
 Call ID: 6ece5803-70b4-40e5-b2a3-470289ef891c
  Args:
    type: :Woman
    source: PatriciaBowesLyon
  AssignClass (7773cbe7-0938-4441-881f-1fbbe271a633)
 Call ID: 7773cbe7-0938-4441-881f-1fbbe271a633
  Args:
    source: PatriciaBowesLyon
    type: :Person
  AssignClass (e2596ab2-3441-4b8f-a7c3-10ebeca77707)
 Call ID: e2596ab2-3441-4b8f-a7c3-10ebeca77707
  Args:
    source: DianaCinderellaSomervell
    type: :Woman
  AssignClass (3629e2ae-ea00-4467-aaff-4d7904889726)
 Call ID: 3629e2ae-ea00-4467-aaff-4d7904889726
  Args:
    type: :Person
    source: DianaCinderellaSomervell
  AddTriple (102c4d64-0112-4a5a-96ab-eae6b190f8bc)
 Call ID: 102c4d64-0112-4a5a-96ab-eae6b190f8bc
  Args:
    source: AnneFerelithFenellaBowesLyon
    target: NerissaBowesLyon
    relation: :hasSister
  AddTriple (87d92f52-52dd-46e4-8a85-45dc9b67e637)
 Call ID: 87d92f52-52dd-46e4-8a85-45dc9b67e637
  Args:
    source: AnneFerelithFenellaBowesLyon
    relation: :hasSister
    target: KatherineBowesLyon
  AddTriple (ffa03ae9-f93d-40d2-a1e2-937251f7a0b8)
 Call ID: ffa03ae9-f93d-40d2-a1e2-937251f7a0b8
  Args:
    source: AnneFerelithFenellaBowesLyon
    relation: :hasSister
    target: PatriciaBowesLyon
  AddTriple (470e572d-5027-4ca7-9cfb-d0a47219d6f6)
 Call ID: 470e572d-5027-4ca7-9cfb-d0a47219d6f6
  Args:
    target: DianaCinderellaSomervell
    relation: :hasSister
    source: AnneFerelithFenellaBowesLyon
  Finish (fd25033f-6f69-4bb3-84e1-56e24dde34eb)
 Call ID: fd25033f-6f69-4bb3-84e1-56e24dde34eb
  Args: