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
Frederick Francis III (German: Friedrich Franz Paul Nikolaus Ernst Heinrich; 19 March 1851 – 10 April 1897) was the penultimate Grand Duke of Mecklenburg-Schwerin.
He was born in Schloss Ludwigslust as the son of Frederick Francis II, Grand Duke of Mecklenburg-Schwerin and his first wife Princess Augusta Reuss of Köstritz.
From an early age Frederick Francis suffered from asthma and severe breathing difficulties.
Frederick Francis' death in Cannes on 10 April 1897 is shrouded in mystery, as he was originally reported to have committed suicide by throwing himself off a parapet of a bridge.
He was succeeded by his son Frederick Francis IV, who would be the last Grand Duke of Mecklenburg-Schwerin.
Marriage and children

Frederick Francis married Grand Duchess Anastasia Mikhailovna of Russia, his second cousin once removed, he being the great-great-grandson and she great-granddaughter of Paul I of Russia.
"

Honours

He received the following orders and decorations:


Ancestry

Literature

References

External links

@media screen{html.skin-theme-clientpref-night .mw-parser-output .sister-inline-image img{filter:invert(1)brightness(55%)contrast(250%)hue-rotate(180deg)}}@media screen and (prefers-color-scheme:dark){html.skin-theme-clientpref-os .mw-parser-output .sister-inline-image img{filter:invert(1)brightness(55%)contrast(250%)hue-rotate(180deg)}} Media related to Frederick Francis III, Grand Duke of Mecklenburg-Schwerin at Wikimedia Commons



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
  AssignClass (fba5e1af-3fea-456b-a6e9-e42362dc97a7)
 Call ID: fba5e1af-3fea-456b-a6e9-e42362dc97a7
  Args:
    type: :Man
    source: :Frederick_Francis_III
  AssignClass (ee57bb68-82e6-4c63-b35e-3c6253295bf0)
 Call ID: ee57bb68-82e6-4c63-b35e-3c6253295bf0
  Args:
    type: :Man
    source: :Frederick_Francis_II
  AssignClass (c6c8c58d-ed8d-49fc-b6d4-1ad879a87920)
 Call ID: c6c8c58d-ed8d-49fc-b6d4-1ad879a87920
  Args:
    source: :Augusta_Reuss_of_Kostritz
    type: :Woman
  AssignClass (19519be7-11dd-4a86-9e2a-8ae1ca48444a)
 Call ID: 19519be7-11dd-4a86-9e2a-8ae1ca48444a
  Args:
    type: :Man
    source: :Frederick_Francis_IV
  AssignClass (6187870f-0598-4fcd-9a02-0bf3aab14c09)
 Call ID: 6187870f-0598-4fcd-9a02-0bf3aab14c09
  Args:
    type: :Woman
    source: :Anastasia_Mikhailovna_of_Russia
  AssignClass (058f7b34-56d4-4be6-9aff-dfbcfba3c404)
 Call ID: 058f7b34-56d4-4be6-9aff-dfbcfba3c404
  Args:
    source: :Paul_I_of_Russia
    type: :Man
  AddLiteral (46a64c63-4e88-45b7-a421-9c8f2dfa7150)
 Call ID: 46a64c63-4e88-45b7-a421-9c8f2dfa7150
  Args:
    source: :Frederick_Francis_III
    literal_value: Friedrich Franz Paul Nikolaus Ernst Heinrich
    literal_type: xsd:string
    relation: :alsoKnownAs
  AddLiteral (29e0d903-f63f-4591-a091-810ac0b01c3b)
 Call ID: 29e0d903-f63f-4591-a091-810ac0b01c3b
  Args:
    literal_value: 1851
    source: :Frederick_Francis_III
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (d3a1240f-128f-4ba4-abdb-2f97a1accba4)
 Call ID: d3a1240f-128f-4ba4-abdb-2f97a1accba4
  Args:
    relation: :hasDeathYear
    source: :Frederick_Francis_III
    literal_value: 1897
    literal_type: xsd:integer
  AddTriple (977c26f6-e9c4-4cc3-bb1f-d14bdc389f0a)
 Call ID: 977c26f6-e9c4-4cc3-bb1f-d14bdc389f0a
  Args:
    target: :Frederick_Francis_II
    source: :Frederick_Francis_III
    relation: :hasFather
  AddTriple (3036b9a5-a5e7-45ad-8bfd-ad5dc670feb9)
 Call ID: 3036b9a5-a5e7-45ad-8bfd-ad5dc670feb9
  Args:
    relation: :hasMother
    target: :Augusta_Reuss_of_Kostritz
    source: :Frederick_Francis_III
  AddTriple (5ee1432a-9ce5-4eb3-8187-f11ac8c2217c)
 Call ID: 5ee1432a-9ce5-4eb3-8187-f11ac8c2217c
  Args:
    relation: :isFatherOf
    target: :Frederick_Francis_IV
    source: :Frederick_Francis_III
  AddTriple (ae4106da-2a84-46e1-a80f-8e54c48ef64e)
 Call ID: ae4106da-2a84-46e1-a80f-8e54c48ef64e
  Args:
    relation: :hasSex
    source: :Frederick_Francis_III
    target: :Male
  AddTriple (86793fc0-bed9-472a-ac36-403b654fe098)
 Call ID: 86793fc0-bed9-472a-ac36-403b654fe098
  Args:
    target: :Male
    source: :Frederick_Francis_II
    relation: :hasSex
  AddTriple (2e60eb00-160c-480f-84db-5a99783d591e)
 Call ID: 2e60eb00-160c-480f-84db-5a99783d591e
  Args:
    target: :Female
    source: :Augusta_Reuss_of_Kostritz
    relation: :hasSex
  AddTriple (396b1921-3ddf-4d67-b047-b4bb0e52254b)
 Call ID: 396b1921-3ddf-4d67-b047-b4bb0e52254b
  Args:
    source: :Frederick_Francis_IV
    target: :Male
    relation: :hasSex
  AddTriple (ac455839-c252-4f93-aa23-ee6c2b551cbe)
 Call ID: ac455839-c252-4f93-aa23-ee6c2b551cbe
  Args:
    relation: :hasSex
    source: :Anastasia_Mikhailovna_of_Russia
    target: :Female
  AddTriple (83ddff8e-8782-44dd-bbef-0e1a52d305fa)
 Call ID: 83ddff8e-8782-44dd-bbef-0e1a52d305fa
  Args:
    target: :Male
    source: :Paul_I_of_Russia
    relation: :hasSex
  Finish (f7ae8bbb-ce01-4dea-be0d-603f46f92c71)
 Call ID: f7ae8bbb-ce01-4dea-be0d-603f46f92c71
  Args:

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

The final data graph after all the edits:
  @prefix : <http://example.com/family_TBOX.ttl#> .
  @prefix data: <http://example.org/data/> .
  @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

  data:Anastasia_Mikhailovna_of_Russia a :Woman ;
      :hasSex data:Female .

  data:Frederick_Francis_III a :Man ;
      :alsoKnownAs "Friedrich Franz Paul Nikolaus Ernst Heinrich"^^xsd:string ;
      :hasBirthYear 1851 ;
      :hasDeathYear 1897 ;
      :hasFather data:Frederick_Francis_II ;
      :hasMother data:Augusta_Reuss_of_Kostritz ;
      :hasSex data:Male ;
      :isFatherOf data:Frederick_Francis_IV .

  data:Paul_I_of_Russia a :Man ;
      :hasSex data:Male .

  data:Augusta_Reuss_of_Kostritz a :Woman ;
      :hasSex data:Female .

  data:Frederick_Francis_II a :Man ;
      :hasSex data:Male .

  data:Frederick_Francis_IV a :Man ;
      :hasSex data:Male .



================================= Tool Message =================================

### Validation Error: Missing Node Types
Your request to `Finish` has been declined. The following nodes in the Data Graph are missing a class assignment (`rdf:type`):

**Classless Nodes:**
['Male', 'Female']

### Required Correction
According to the pipeline rules, **every node must have a class assigned to it** to ensure the graph is semantically valid. 

Please perform the following steps:
1. Review the input text and ontology to determine the most appropriate class for each node listed above.
2. Use the `AssignClass` tool for each node to assign its correct type.
3. Once all nodes have been assigned a class, you may attempt to `Finish` again or run `ValidateShacl` to verify the final state.

Proceed with the necessary tool calls now.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (d21d5f08-a492-4b91-b655-d839bce31c5a)
 Call ID: d21d5f08-a492-4b91-b655-d839bce31c5a
  Args:
    type: :Sex
    source: :Male
  AssignClass (22064f8d-33e5-4d9f-b77e-bfd740a7747c)
 Call ID: 22064f8d-33e5-4d9f-b77e-bfd740a7747c
  Args:
    type: :Sex
    source: :Female
  Finish (cd971313-c727-420e-ac9b-086c9734a465)
 Call ID: cd971313-c727-420e-ac9b-086c9734a465
  Args: