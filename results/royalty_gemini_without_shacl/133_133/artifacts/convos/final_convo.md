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
Friedrich Franz, Hereditary Grand Duke of Mecklenburg-Schwerin (German: Friedrich Franz Erbgroßherzog von Mecklenburg-Schwerin; 22 April 1910 – 31 July 2001) was the heir apparent to the throne of Mecklenburg-Schwerin and a member of the Waffen-SS.
Early life

He was born in Schwerin, the eldest child of the reigning Grand Duke of Mecklenburg-Schwerin, Frederick Francis IV, and his wife Princess Alexandra of Hanover, a daughter of Crown Prince Ernest Augustus of Hanover (a first-cousin once removed of Queen Victoria) and Princess Thyra of Denmark, the youngest daughter of King Christian IX of Denmark.
He did not succeed to the throne, as the Grand Duchy was replaced with the Free State of Mecklenburg-Schwerin.
Upon the promulgation of the Weimar Constitution on 11 August 1919, titles of sovereigns such as emperor/empress, king/queen, grand duke/grand duchess, etc. were abolished.
He therefore became known as Friedrich Franz Herzog von Mecklenburg-Schwerin (or Friedrich Franz, Duke of Mecklenburg-Schwerin) de facto since the establishment of the Free State of Mecklenburg-Schwerin.
Post monarchy

In May 1931 against the will of his father, Friedrich Franz joined the SS and by 1936 he had been promoted to the rank of Hauptsturmführer (Captain).
In May 1943, a family council was called by the Grand Ducal family and Friedrich Franz was passed over as heir (of the family estates) in favour of his younger brother Duke Christian Louis, who would instead inherit the family property.
Friedrich Franz married Karin Elisabeth von Schaper (1920–2012), the daughter of Walter von Schaper and his wife Baroness Louise von Münchhausen, on 11 June 1941 at Schloß Wiligrad, near the Lake Schwerin.



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
  AssignClass (86ccae97-0fa3-4a26-a03b-1845aada8050)
 Call ID: 86ccae97-0fa3-4a26-a03b-1845aada8050
  Args:
    source: Friedrich_Franz_Hereditary_Grand_Duke_of_Mecklenburg_Schwerin
    type: :Man
  AssignClass (82c6961d-1b8d-4e10-946c-1f0ba69ef282)
 Call ID: 82c6961d-1b8d-4e10-946c-1f0ba69ef282
  Args:
    source: Frederick_Francis_IV_Grand_Duke_of_Mecklenburg_Schwerin
    type: :Man
  AssignClass (fd81e1a8-a47b-4b0a-a834-a4f4eff6daca)
 Call ID: fd81e1a8-a47b-4b0a-a834-a4f4eff6daca
  Args:
    source: Princess_Alexandra_of_Hanover
    type: :Woman
  AssignClass (f1568e9a-55f7-412e-8efb-31dc7aff0911)
 Call ID: f1568e9a-55f7-412e-8efb-31dc7aff0911
  Args:
    source: Crown_Prince_Ernest_Augustus_of_Hanover
    type: :Man
  AssignClass (025f8f33-4196-469c-b3c1-65f75cf01a6d)
 Call ID: 025f8f33-4196-469c-b3c1-65f75cf01a6d
  Args:
    type: :Woman
    source: Princess_Thyra_of_Denmark
  AssignClass (e8fe9417-85bc-46cb-b246-f9dabc83cc0f)
 Call ID: e8fe9417-85bc-46cb-b246-f9dabc83cc0f
  Args:
    source: King_Christian_IX_of_Denmark
    type: :Man
  AssignClass (178bb946-d325-4e3f-9c88-5d811b980d4d)
 Call ID: 178bb946-d325-4e3f-9c88-5d811b980d4d
  Args:
    type: :Man
    source: Duke_Christian_Louis
  AssignClass (a94de0f3-cc4b-4780-b11f-78344352a938)
 Call ID: a94de0f3-cc4b-4780-b11f-78344352a938
  Args:
    type: :Woman
    source: Karin_Elisabeth_von_Schaper
  AssignClass (10298f1a-0293-466c-873a-bd5d72f755e4)
 Call ID: 10298f1a-0293-466c-873a-bd5d72f755e4
  Args:
    source: Walter_von_Schaper
    type: :Man
  AssignClass (a60a12da-cc06-496f-9e31-ebab822841b8)
 Call ID: a60a12da-cc06-496f-9e31-ebab822841b8
  Args:
    source: Baroness_Louise_von_Münchhausen
    type: :Woman
  AddLiteral (a643eb97-1d87-4843-845e-ef7008842712)
 Call ID: a643eb97-1d87-4843-845e-ef7008842712
  Args:
    literal_value: 1910
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Friedrich_Franz_Hereditary_Grand_Duke_of_Mecklenburg_Schwerin
  AddLiteral (414e1f27-b7ad-4e26-a548-1de02974c503)
 Call ID: 414e1f27-b7ad-4e26-a548-1de02974c503
  Args:
    source: Friedrich_Franz_Hereditary_Grand_Duke_of_Mecklenburg_Schwerin
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 2001
  AddTriple (94958ae2-31e0-4362-92ad-fc752d996c1d)
 Call ID: 94958ae2-31e0-4362-92ad-fc752d996c1d
  Args:
    target: Frederick_Francis_IV_Grand_Duke_of_Mecklenburg_Schwerin
    relation: :hasFather
    source: Friedrich_Franz_Hereditary_Grand_Duke_of_Mecklenburg_Schwerin
  AddTriple (184b7213-6ddf-461c-90ca-76722b52c534)
 Call ID: 184b7213-6ddf-461c-90ca-76722b52c534
  Args:
    source: Friedrich_Franz_Hereditary_Grand_Duke_of_Mecklenburg_Schwerin
    relation: :hasMother
    target: Princess_Alexandra_of_Hanover
  AddTriple (ad430701-59f3-4c82-8683-312ce60bc721)
 Call ID: ad430701-59f3-4c82-8683-312ce60bc721
  Args:
    target: Crown_Prince_Ernest_Augustus_of_Hanover
    relation: :hasFather
    source: Princess_Alexandra_of_Hanover
  AddTriple (52978f9e-9957-415b-9f2e-2cd6c49d1cd4)
 Call ID: 52978f9e-9957-415b-9f2e-2cd6c49d1cd4
  Args:
    target: Princess_Thyra_of_Denmark
    relation: :hasMother
    source: Princess_Alexandra_of_Hanover
  AddTriple (dd4cf835-ae0d-4647-ac3d-16df2185acba)
 Call ID: dd4cf835-ae0d-4647-ac3d-16df2185acba
  Args:
    relation: :hasFather
    source: Princess_Thyra_of_Denmark
    target: King_Christian_IX_of_Denmark
  AddTriple (c009b1ea-03e3-4f53-bad9-7c116267e927)
 Call ID: c009b1ea-03e3-4f53-bad9-7c116267e927
  Args:
    target: Duke_Christian_Louis
    source: Friedrich_Franz_Hereditary_Grand_Duke_of_Mecklenburg_Schwerin
    relation: :hasBrother
  AddTriple (203c7bc6-2d50-4cd5-afd9-7720b305a2a3)
 Call ID: 203c7bc6-2d50-4cd5-afd9-7720b305a2a3
  Args:
    relation: :hasFather
    source: Duke_Christian_Louis
    target: Frederick_Francis_IV_Grand_Duke_of_Mecklenburg_Schwerin
  AddTriple (02028c94-c8a9-491c-9e66-de5a02a129bc)
 Call ID: 02028c94-c8a9-491c-9e66-de5a02a129bc
  Args:
    target: Princess_Alexandra_of_Hanover
    source: Duke_Christian_Louis
    relation: :hasMother
  AddLiteral (bd1767bf-a252-40ec-be00-13178a41be3f)
 Call ID: bd1767bf-a252-40ec-be00-13178a41be3f
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    source: Friedrich_Franz_Hereditary_Grand_Duke_of_Mecklenburg_Schwerin
    literal_value: 1941
  AddTriple (ff7cc04b-be63-4278-a9e9-237a53286112)
 Call ID: ff7cc04b-be63-4278-a9e9-237a53286112
  Args:
    target: Karin_Elisabeth_von_Schaper
    relation: :hasRelation
    source: Friedrich_Franz_Hereditary_Grand_Duke_of_Mecklenburg_Schwerin
  AddLiteral (c7017a3f-3898-4a1d-bcc5-acc14e95709b)
 Call ID: c7017a3f-3898-4a1d-bcc5-acc14e95709b
  Args:
    literal_value: 1920
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Karin_Elisabeth_von_Schaper
  AddLiteral (f8746a3c-5a59-48b9-bfdb-eb04ae9d38e5)
 Call ID: f8746a3c-5a59-48b9-bfdb-eb04ae9d38e5
  Args:
    literal_type: xsd:integer
    source: Karin_Elisabeth_von_Schaper
    relation: :hasDeathYear
    literal_value: 2012
  AddTriple (6f6b4346-b90c-4a4a-8a16-9227da6ab174)
 Call ID: 6f6b4346-b90c-4a4a-8a16-9227da6ab174
  Args:
    target: Walter_von_Schaper
    relation: :hasFather
    source: Karin_Elisabeth_von_Schaper
  AddTriple (760693c9-7a59-4d40-8457-3f98d0be31a9)
 Call ID: 760693c9-7a59-4d40-8457-3f98d0be31a9
  Args:
    target: Baroness_Louise_von_Münchhausen
    source: Karin_Elisabeth_von_Schaper
    relation: :hasMother
  Finish (ed5f2f97-cd34-41d3-a6ac-0d51ec57637e)
 Call ID: ed5f2f97-cd34-41d3-a6ac-0d51ec57637e
  Args: