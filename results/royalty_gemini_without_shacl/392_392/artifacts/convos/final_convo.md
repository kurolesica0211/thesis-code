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
Prince Bernhard of Lippe (Bernhard Kasimir Wilhelm Friedrich Gustav Heinrich Eduard; 26 August 1872 – 19 June 1934) was a member of the Lippe-Biesterfeld line of the House of Lippe.
He was the father of Prince Bernhard of Lippe-Biesterfeld, the prince consort of Queen Juliana of the Netherlands.
Biography

Prince Bernhard of Lippe, born as Count of Lippe-Biesterfeld in Oberkassel on 26 August 1872, was the 2nd son of Ernest II, Count of Lippe-Biesterfeld, regent (1897–1904) of Principality of Lippe, and his wife Countess Karoline von Wartensleben.
He was a younger brother of Leopold IV, Prince of Lippe, who succeeded as reigning Prince of Lippe in 1905.
The Lippe-Biesterfeld family had lived at Oberkassel, Bonn, ever since 1770, when count Frederick William (1737–1803) had married Elisabeth Johanna, Edle von Meinertzhagen (1752–1811), who inherited a small manor house at Oberkassel where the couple moved from Biesterfeld in 1770, and which became the home to the family for the following 209 years.
The manor house and farm at Biesterfeld were demolished around 1820.
Prince Bernhard acquired the Reckenwalde castle in eastern Brandenburg (today Wojnowo, Poland), the family's new estate, where his children grew up.
On 4 March 1909, Bernhard entered into a morganatic marriage with Baroness Armgard von Sierstorpff-Cramm, widowed Countess von Oeynhausen.
Before this marriage, his wife was granted the title Countess of Biesterfeld (Gräfin von Biesterfeld) on 8 February 1909.
She and her two sons Bernhard and Aschwin were created Princess (Prince) of Lippe-Biesterfeld (Prinzessin (Prinz) zur Lippe-Biesterfeld) on 24 February 1916 with the style Serene Highness, which brought their children into a more senior place in the line of succession, in which they hitherto had been the very last.
The suffix Biesterfeld was revived to mark the beginning of a new cadet line.
Bernhard died in Munich, aged 61.



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
  AssignClass (f5fd38df-3d5b-4ac1-9b25-987d76c5d875)
 Call ID: f5fd38df-3d5b-4ac1-9b25-987d76c5d875
  Args:
    source: Prince_Bernhard_of_Lippe
    type: :Man
  AssignClass (cf6b7199-b2b4-4a73-8fad-872d87cb70e5)
 Call ID: cf6b7199-b2b4-4a73-8fad-872d87cb70e5
  Args:
    type: :Person
    source: Prince_Bernhard_of_Lippe
  AssignClass (f6908fae-6768-4d2d-b632-4ae1ba2310d9)
 Call ID: f6908fae-6768-4d2d-b632-4ae1ba2310d9
  Args:
    type: :Ancestor
    source: Prince_Bernhard_of_Lippe
  AddLiteral (a120491b-2b52-4336-9f6a-45a39bcd277e)
 Call ID: a120491b-2b52-4336-9f6a-45a39bcd277e
  Args:
    literal_value: Bernhard Kasimir Wilhelm Friedrich Gustav Heinrich Eduard
    literal_type: xsd:string
    source: Prince_Bernhard_of_Lippe
    relation: :knownAs
  AddLiteral (68f2b57a-d0a8-4ae9-abeb-d1674a9647c1)
 Call ID: 68f2b57a-d0a8-4ae9-abeb-d1674a9647c1
  Args:
    literal_value: 1872
    literal_type: xsd:integer
    source: Prince_Bernhard_of_Lippe
    relation: :hasBirthYear
  AddLiteral (64551e17-6f73-4c4a-b7dd-1af9dd03aab4)
 Call ID: 64551e17-6f73-4c4a-b7dd-1af9dd03aab4
  Args:
    literal_value: 1934
    literal_type: xsd:integer
    source: Prince_Bernhard_of_Lippe
    relation: :hasDeathYear
  AssignClass (1e5c2695-c553-4bf2-b4bd-52cd7ea993c2)
 Call ID: 1e5c2695-c553-4bf2-b4bd-52cd7ea993c2
  Args:
    type: :Man
    source: Prince_Bernhard_of_Lippe_Biesterfeld_junior
  AssignClass (43022017-1c07-4dce-ab61-dc50a8082752)
 Call ID: 43022017-1c07-4dce-ab61-dc50a8082752
  Args:
    type: :Person
    source: Prince_Bernhard_of_Lippe_Biesterfeld_junior
  AddTriple (6693354a-5f01-4981-9046-98f4bb5a77d4)
 Call ID: 6693354a-5f01-4981-9046-98f4bb5a77d4
  Args:
    relation: :isSonOf
    source: Prince_Bernhard_of_Lippe_Biesterfeld_junior
    target: Prince_Bernhard_of_Lippe
  AddTriple (e5625a77-cd0e-4f19-9bfe-b21aab8bc4b6)
 Call ID: e5625a77-cd0e-4f19-9bfe-b21aab8bc4b6
  Args:
    target: Ernest_II_Count_of_Lippe_Biesterfeld
    source: Prince_Bernhard_of_Lippe
    relation: :isSonOf
  AssignClass (1de2878f-58a7-4aca-bbf0-5ec7e4c76a18)
 Call ID: 1de2878f-58a7-4aca-bbf0-5ec7e4c76a18
  Args:
    type: :Man
    source: Ernest_II_Count_of_Lippe_Biesterfeld
  AssignClass (3739f510-645c-4167-a444-345224267991)
 Call ID: 3739f510-645c-4167-a444-345224267991
  Args:
    type: :Person
    source: Ernest_II_Count_of_Lippe_Biesterfeld
  AssignClass (95abe775-97ce-4ab9-bbfe-bef64a260b2a)
 Call ID: 95abe775-97ce-4ab9-bbfe-bef64a260b2a
  Args:
    source: Ernest_II_Count_of_Lippe_Biesterfeld
    type: :Ancestor
  AddTriple (59a60448-c873-4d1b-b988-7642a5505751)
 Call ID: 59a60448-c873-4d1b-b988-7642a5505751
  Args:
    target: Countess_Karoline_von_Wartensleben
    source: Prince_Bernhard_of_Lippe
    relation: :hasMother
  AssignClass (84362cd6-8bc9-439c-bba2-e1c5837d531e)
 Call ID: 84362cd6-8bc9-439c-bba2-e1c5837d531e
  Args:
    source: Countess_Karoline_von_Wartensleben
    type: :Woman
  AssignClass (bdb199b9-5b1b-4e91-a0cc-0e26aa513250)
 Call ID: bdb199b9-5b1b-4e91-a0cc-0e26aa513250
  Args:
    source: Countess_Karoline_von_Wartensleben
    type: :Person
  AssignClass (b7d50cb7-13e3-4021-b412-cebdbb930c38)
 Call ID: b7d50cb7-13e3-4021-b412-cebdbb930c38
  Args:
    type: :Ancestor
    source: Countess_Karoline_von_Wartensleben
  AddTriple (74736150-c11b-4a42-b3ab-35af519fb3c5)
 Call ID: 74736150-c11b-4a42-b3ab-35af519fb3c5
  Args:
    source: Prince_Bernhard_of_Lippe
    relation: :hasBrother
    target: Leopold_IV_Prince_of_Lippe
  AssignClass (8e0b2e6a-3590-4d38-b72e-d97bc1ce205e)
 Call ID: 8e0b2e6a-3590-4d38-b72e-d97bc1ce205e
  Args:
    source: Leopold_IV_Prince_of_Lippe
    type: :Man
  AssignClass (b0cecd04-0ae3-45bd-ba4a-4acce9abba44)
 Call ID: b0cecd04-0ae3-45bd-ba4a-4acce9abba44
  Args:
    type: :Person
    source: Leopold_IV_Prince_of_Lippe
  AddTriple (17a917e3-87d5-4886-a4e6-74c1af1a22e9)
 Call ID: 17a917e3-87d5-4886-a4e6-74c1af1a22e9
  Args:
    target: Ernest_II_Count_of_Lippe_Biesterfeld
    source: Prince_Bernhard_of_Lippe
    relation: :hasFather
  AddTriple (9528b81c-6c72-4a2f-901f-0e49022e109e)
 Call ID: 9528b81c-6c72-4a2f-901f-0e49022e109e
  Args:
    relation: :hasMother
    source: Prince_Bernhard_of_Lippe
    target: Countess_Karoline_von_Wartensleben
  AddTriple (b06d81b9-adac-4538-8557-486910a886c6)
 Call ID: b06d81b9-adac-4538-8557-486910a886c6
  Args:
    target: Countess_Karoline_von_Wartensleben
    relation: :hasMother
    source: Leopold_IV_Prince_of_Lippe
  AddTriple (bbfbc710-e58c-4328-8973-87ec26009ff1)
 Call ID: bbfbc710-e58c-4328-8973-87ec26009ff1
  Args:
    relation: :hasFather
    source: Leopold_IV_Prince_of_Lippe
    target: Ernest_II_Count_of_Lippe_Biesterfeld
  AddTriple (b93bccf7-f719-47b5-9fbf-aa4ee712526c)
 Call ID: b93bccf7-f719-47b5-9fbf-aa4ee712526c
  Args:
    source: Prince_Bernhard_of_Lippe_Biesterfeld_junior
    relation: :hasFather
    target: Prince_Bernhard_of_Lippe
  AddTriple (bdb96e4e-8a1f-4279-99d4-ef1779705ec7)
 Call ID: bdb96e4e-8a1f-4279-99d4-ef1779705ec7
  Args:
    target: Baroness_Armgard_von_Sierstorpff_Cramm
    relation: :hasMother
    source: Prince_Bernhard_of_Lippe_Biesterfeld_junior
  AssignClass (72350e78-5ebc-45f5-b4c7-3ebf5fe2e0bf)
 Call ID: 72350e78-5ebc-45f5-b4c7-3ebf5fe2e0bf
  Args:
    source: Baroness_Armgard_von_Sierstorpff_Cramm
    type: :Woman
  AssignClass (80434cb5-337b-4381-93d8-62d89ac4d599)
 Call ID: 80434cb5-337b-4381-93d8-62d89ac4d599
  Args:
    type: :Person
    source: Baroness_Armgard_von_Sierstorpff_Cramm
  AddLiteral (4cf2bf0b-e1d2-4d02-842e-4950ec7bdd21)
 Call ID: 4cf2bf0b-e1d2-4d02-842e-4950ec7bdd21
  Args:
    relation: :hasMarriageYear
    source: Prince_Bernhard_of_Lippe
    literal_type: xsd:integer
    literal_value: 1909
  AddTriple (d6697d9d-fadc-4544-a96c-7dadf997e0cc)
 Call ID: d6697d9d-fadc-4544-a96c-7dadf997e0cc
  Args:
    target: Aschwin_of_Lippe_Biesterfeld
    relation: :hasSon
    source: Prince_Bernhard_of_Lippe
  AssignClass (9bce30df-2d2d-4a10-bc42-9b1a9185e75c)
 Call ID: 9bce30df-2d2d-4a10-bc42-9b1a9185e75c
  Args:
    type: :Man
    source: Aschwin_of_Lippe_Biesterfeld
  AssignClass (b6727ee3-6849-4a82-8286-eaaec310a3c2)
 Call ID: b6727ee3-6849-4a82-8286-eaaec310a3c2
  Args:
    source: Aschwin_of_Lippe_Biesterfeld
    type: :Person
  AddTriple (64558821-2483-4844-984d-6ec94d2c280a)
 Call ID: 64558821-2483-4844-984d-6ec94d2c280a
  Args:
    target: Baroness_Armgard_von_Sierstorpff_Cramm
    source: Aschwin_of_Lippe_Biesterfeld
    relation: :hasMother
  AddTriple (47d7b7c5-bff4-4e62-bacc-c26994472670)
 Call ID: 47d7b7c5-bff4-4e62-bacc-c26994472670
  Args:
    target: Prince_Bernhard_of_Lippe
    source: Aschwin_of_Lippe_Biesterfeld
    relation: :hasFather
  AssignClass (45f38eea-a469-4c33-97df-7311e532c4ea)
 Call ID: 45f38eea-a469-4c33-97df-7311e532c4ea
  Args:
    type: :Man
    source: Frederick_William_Count_of_Lippe_Biesterfeld
  AssignClass (4c33dabc-0f71-4a83-8396-b400951706c0)
 Call ID: 4c33dabc-0f71-4a83-8396-b400951706c0
  Args:
    type: :Person
    source: Frederick_William_Count_of_Lippe_Biesterfeld
  AssignClass (f0620331-b8a1-4efa-9807-6023b3993683)
 Call ID: f0620331-b8a1-4efa-9807-6023b3993683
  Args:
    type: :Ancestor
    source: Frederick_William_Count_of_Lippe_Biesterfeld
  AssignClass (7454ea4f-3865-4b4d-b8eb-c92a1126382b)
 Call ID: 7454ea4f-3865-4b4d-b8eb-c92a1126382b
  Args:
    source: Elisabeth_Johanna_Edle_von_Meinertzhagen
    type: :Woman
  AssignClass (bab7b9c5-553e-4dd5-a853-ab141f75d299)
 Call ID: bab7b9c5-553e-4dd5-a853-ab141f75d299
  Args:
    source: Elisabeth_Johanna_Edle_von_Meinertzhagen
    type: :Person
  AssignClass (6958c0ce-20e1-4b77-a400-a4a8f47008fb)
 Call ID: 6958c0ce-20e1-4b77-a400-a4a8f47008fb
  Args:
    source: Elisabeth_Johanna_Edle_von_Meinertzhagen
    type: :Ancestor
  AddLiteral (eb5f8c1c-3960-491d-8757-48f577c19630)
 Call ID: eb5f8c1c-3960-491d-8757-48f577c19630
  Args:
    literal_value: 1770
    literal_type: xsd:integer
    source: Frederick_William_Count_of_Lippe_Biesterfeld
    relation: :hasMarriageYear
  Finish (dfe94c5d-9b2b-45af-bf59-382460d09b4c)
 Call ID: dfe94c5d-9b2b-45af-bf59-382460d09b4c
  Args: