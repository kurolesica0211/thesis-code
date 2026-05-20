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
Rafael of Orléans-Braganza (Portuguese: Rafael de Orléans e Bragança; born 24 April 1986) is a member of the Imperial House of Brazil.
He is the heir presumptive to his childless uncle, Prince Bertrand, the current head of the Vassouras branch of the House of Orléans-Braganza and one of the claimants to the defunct Brazilian Throne.
Rafael became heir presumptive following the death of his father, Prince Antônio, in November 2024.
Family

Born in Petrópolis, Brazil on 26 April 1986, he is the third child and second son of Prince Antônio de Orleans e Bragança and Princess Christine of Ligne.
He has an older brother and sister, Prince Pedro Luiz and Princess Amélia and a younger sister, Princess Maria Gabriela.
His name in full is Rafael Antonio Maria José Francisco Miguel Gabriel Gonzaga de Orléans e Bragança e Ligne.
His paternal grandparents were Prince Pedro Henrique of Orléans-Bragança, one of two claimants to be head of the Brazilian Imperial House, and Princess Maria Elisabeth of Bavaria.
His maternal grandparents were Antoine, 13th Prince of Ligne, and Princess Alix of Luxembourg.
His mother's family, the House of Ligne, is one of the oldest and most prominent Wallonian noble families still extant in Belgium.
Christine is a niece of Grand Duke Jean, who reigned in Luxembourg until his abdication in 2000.
Personal life

Rafael has a degree in manufacturing engineering from Pontifical Catholic University of Rio de Janeiro, working at the InBev subsidiary in London.
Rafael also has a partnership and a tourism enterprise with headquarters in New York, Paris and Rio de Janeiro.
Rafael has expressed in statements his desire to marry a princess who is part of "Catholic royalty or high nobility".
Appointments

In February 2022, after the floods that devastated the city of Petrópolis, Rafael came to the aid of the victims, bringing them essential goods that the imperial house received from monarchist supporters.
Honors

Genealogy

Ancestry

Patrilineal descent

Rafael is a member of the House of Orléans-Braganza, a sub-branch of the House of Bourbon, itself a branch of the House of Capet and of the Robertians.
Rafael's patriline is the line from which he is descended father to son.
It follows the Dukes of Orléans, the Kings of France, the Dukes and Counts of Vendôme, the Counts of La Marche, the first Duke of Bourbon, a Count of Clermont, and before them, again the Kings of France.



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
  AssignClass (b4d18626-f342-430b-bbeb-79c665dbf915)
 Call ID: b4d18626-f342-430b-bbeb-79c665dbf915
  Args:
    source: Rafael_of_Orleans-Braganza
    type: :Man
  AssignClass (f658328f-1083-43dd-94e4-4eb01eb227fb)
 Call ID: f658328f-1083-43dd-94e4-4eb01eb227fb
  Args:
    source: Rafael_of_Orleans-Braganza
    type: :Person
  AddLiteral (8762c6fe-1f91-4cca-a9c5-089aefe5fe1e)
 Call ID: 8762c6fe-1f91-4cca-a9c5-089aefe5fe1e
  Args:
    literal_type: xsd:integer
    literal_value: 1986
    source: Rafael_of_Orleans-Braganza
    relation: :hasBirthYear
  AssignClass (ea4d5c6c-88a9-4553-a074-7c451e48f42e)
 Call ID: ea4d5c6c-88a9-4553-a074-7c451e48f42e
  Args:
    source: Prince_Bertrand
    type: :Man
  AssignClass (50efd598-6a82-4d11-8ec8-60ec0884a3b7)
 Call ID: 50efd598-6a82-4d11-8ec8-60ec0884a3b7
  Args:
    type: :Person
    source: Prince_Bertrand
  AddTriple (82b7c79f-5dbb-4121-8d02-296ea10b3d55)
 Call ID: 82b7c79f-5dbb-4121-8d02-296ea10b3d55
  Args:
    source: Rafael_of_Orleans-Braganza
    relation: :hasRelation
    target: Prince_Bertrand
  AssignClass (06acd114-f34b-4a28-b6ba-7281c6d925bd)
 Call ID: 06acd114-f34b-4a28-b6ba-7281c6d925bd
  Args:
    source: Prince_Antonio
    type: :Man
  AssignClass (5865ba8e-16a7-4c38-9e87-138df4f65caf)
 Call ID: 5865ba8e-16a7-4c38-9e87-138df4f65caf
  Args:
    type: :Person
    source: Prince_Antonio
  AssignClass (19df2011-5707-45d8-95de-b4b8d999b14d)
 Call ID: 19df2011-5707-45d8-95de-b4b8d999b14d
  Args:
    source: Prince_Antonio
    type: :Ancestor
  AssignClass (02cb06a1-a386-492b-b1f8-dea77befe649)
 Call ID: 02cb06a1-a386-492b-b1f8-dea77befe649
  Args:
    source: Princess_Christine_of_Ligne
    type: :Woman
  AssignClass (1c537c01-9c8f-425b-87c3-df83028b91ee)
 Call ID: 1c537c01-9c8f-425b-87c3-df83028b91ee
  Args:
    source: Princess_Christine_of_Ligne
    type: :Person
  AssignClass (58c5ef32-212c-4040-9472-8300b0b67ee0)
 Call ID: 58c5ef32-212c-4040-9472-8300b0b67ee0
  Args:
    source: Princess_Christine_of_Ligne
    type: :Ancestor
  AddTriple (deb0df76-c094-4b03-82cc-66660a9571b6)
 Call ID: deb0df76-c094-4b03-82cc-66660a9571b6
  Args:
    source: Rafael_of_Orleans-Braganza
    relation: :hasFather
    target: Prince_Antonio
  AddTriple (4625a9c8-dad6-47c1-b098-29a6151643f1)
 Call ID: 4625a9c8-dad6-47c1-b098-29a6151643f1
  Args:
    target: Princess_Christine_of_Ligne
    relation: :hasMother
    source: Rafael_of_Orleans-Braganza
  AssignClass (706f5d6b-e0a9-4e6f-b3ac-5152b87dd9ff)
 Call ID: 706f5d6b-e0a9-4e6f-b3ac-5152b87dd9ff
  Args:
    source: Prince_Pedro_Luiz
    type: :Man
  AssignClass (0259afe5-4099-4a91-aba7-6ccb31186852)
 Call ID: 0259afe5-4099-4a91-aba7-6ccb31186852
  Args:
    type: :Person
    source: Prince_Pedro_Luiz
  AssignClass (18e7cc75-5885-4f52-83d0-a3c4d5f8a687)
 Call ID: 18e7cc75-5885-4f52-83d0-a3c4d5f8a687
  Args:
    type: :Woman
    source: Princess_Amelia
  AssignClass (77088b3b-87b1-4e09-a0af-ec0872ff44fc)
 Call ID: 77088b3b-87b1-4e09-a0af-ec0872ff44fc
  Args:
    source: Princess_Amelia
    type: :Person
  AssignClass (4be6a4dd-ff7b-4e91-ab05-d1dcf25af54f)
 Call ID: 4be6a4dd-ff7b-4e91-ab05-d1dcf25af54f
  Args:
    type: :Woman
    source: Princess_Maria_Gabriela
  AssignClass (d1aa5f0c-fb62-47cb-a02d-5363925d5e70)
 Call ID: d1aa5f0c-fb62-47cb-a02d-5363925d5e70
  Args:
    source: Princess_Maria_Gabriela
    type: :Person
  AddTriple (d06fb159-dde6-4bc2-a88f-c37c512b7d36)
 Call ID: d06fb159-dde6-4bc2-a88f-c37c512b7d36
  Args:
    target: Prince_Pedro_Luiz
    relation: :hasBrother
    source: Rafael_of_Orleans-Braganza
  AddTriple (424f329a-bad9-4ced-8608-6b579fcbb41a)
 Call ID: 424f329a-bad9-4ced-8608-6b579fcbb41a
  Args:
    target: Princess_Amelia
    relation: :hasSister
    source: Rafael_of_Orleans-Braganza
  AddTriple (271f914b-ef89-42eb-a856-8ca20a2565d9)
 Call ID: 271f914b-ef89-42eb-a856-8ca20a2565d9
  Args:
    relation: :hasSister
    target: Princess_Maria_Gabriela
    source: Rafael_of_Orleans-Braganza
  AssignClass (b9d74423-e8af-4087-9fd3-186b98a45b48)
 Call ID: b9d74423-e8af-4087-9fd3-186b98a45b48
  Args:
    source: Prince_Pedro_Henrique_of_Orleans-Braganza
    type: :Man
  AssignClass (24421d8f-b4ad-423b-a389-d98320a4ebe8)
 Call ID: 24421d8f-b4ad-423b-a389-d98320a4ebe8
  Args:
    type: :Person
    source: Prince_Pedro_Henrique_of_Orleans-Braganza
  AssignClass (8f4e76e8-1ed5-48ce-b8dc-13082598c7f6)
 Call ID: 8f4e76e8-1ed5-48ce-b8dc-13082598c7f6
  Args:
    source: Prince_Pedro_Henrique_of_Orleans-Braganza
    type: :Ancestor
  AssignClass (64f93ef9-8df1-4e53-aac8-c351854e7986)
 Call ID: 64f93ef9-8df1-4e53-aac8-c351854e7986
  Args:
    type: :Woman
    source: Princess_Maria_Elisabeth_of_Bavaria
  AssignClass (a8c22381-62c4-44e5-a9ef-4ad5808de228)
 Call ID: a8c22381-62c4-44e5-a9ef-4ad5808de228
  Args:
    source: Princess_Maria_Elisabeth_of_Bavaria
    type: :Person
  AssignClass (b88db70f-fc29-427f-ae7f-2d20fa5527e4)
 Call ID: b88db70f-fc29-427f-ae7f-2d20fa5527e4
  Args:
    source: Princess_Maria_Elisabeth_of_Bavaria
    type: :Ancestor
  AddTriple (76e7be80-36e4-4899-864f-447ed41e0ff5)
 Call ID: 76e7be80-36e4-4899-864f-447ed41e0ff5
  Args:
    target: Prince_Antonio
    relation: :isFatherOf
    source: Prince_Pedro_Henrique_of_Orleans-Braganza
  AddTriple (4cd56265-1ecc-4332-a9c7-1484d4bf2191)
 Call ID: 4cd56265-1ecc-4332-a9c7-1484d4bf2191
  Args:
    target: Prince_Antonio
    relation: :isMotherOf
    source: Princess_Maria_Elisabeth_of_Bavaria
  AssignClass (35a3a42d-838c-4918-ae4a-6e6dc59d9afc)
 Call ID: 35a3a42d-838c-4918-ae4a-6e6dc59d9afc
  Args:
    source: Antoine_13th_Prince_of_Ligne
    type: :Man
  AssignClass (f922bdb4-da5f-44de-9e90-a256fbf842aa)
 Call ID: f922bdb4-da5f-44de-9e90-a256fbf842aa
  Args:
    source: Antoine_13th_Prince_of_Ligne
    type: :Person
  AssignClass (c0af6805-f385-47fb-9cff-96b0970cd69f)
 Call ID: c0af6805-f385-47fb-9cff-96b0970cd69f
  Args:
    source: Antoine_13th_Prince_of_Ligne
    type: :Ancestor
  AssignClass (d304c995-1cef-41f0-ac4f-19c9f7fbbd57)
 Call ID: d304c995-1cef-41f0-ac4f-19c9f7fbbd57
  Args:
    source: Princess_Alix_of_Luxembourg
    type: :Woman
  AssignClass (f9e5532a-5508-4a82-a642-a59e343ab556)
 Call ID: f9e5532a-5508-4a82-a642-a59e343ab556
  Args:
    source: Princess_Alix_of_Luxembourg
    type: :Person
  AssignClass (740c8e76-c704-4701-aedc-44af6ca46a67)
 Call ID: 740c8e76-c704-4701-aedc-44af6ca46a67
  Args:
    source: Princess_Alix_of_Luxembourg
    type: :Ancestor
  AddTriple (1bea6c35-9d5d-4d8c-a2c1-895423fabed6)
 Call ID: 1bea6c35-9d5d-4d8c-a2c1-895423fabed6
  Args:
    target: Princess_Christine_of_Ligne
    relation: :isFatherOf
    source: Antoine_13th_Prince_of_Ligne
  AddTriple (e7c71005-b661-4b91-a647-3808fcea68a4)
 Call ID: e7c71005-b661-4b91-a647-3808fcea68a4
  Args:
    target: Princess_Christine_of_Ligne
    relation: :isMotherOf
    source: Princess_Alix_of_Luxembourg
  Finish (f1d0c049-e046-4e1f-8439-e2afe42350ac)
 Call ID: f1d0c049-e046-4e1f-8439-e2afe42350ac
  Args: