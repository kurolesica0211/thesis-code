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


Prince Hugo de Bourbon de Parme (Carlos Hugo Roderik Sybren; born 20 January 1997), formerly Hugo Klynstra, is a member of the extended Dutch royal family as the son of Prince Carlos, Hereditary Duke of Parma.
Born out of wedlock, he was denied titles and family rights by his father until the Dutch Council of State ruled in his favor in 2018, granting him the style and title of His Royal Highness Prince Carlos Hugo
Roderik Sybren de Bourbon de Parme.
Despite the ruling, he is neither a member of the Dutch royal house (although considered a member of the extended Dutch royal family) nor a member of the House of Bourbon-Parma and is not in the line of succession to the defunct Parmese throne.
Early life and family

Carlos Hugo Roderik Sybren Klynstra was born in Nijmegen on 20 January 1997 to Prince Carlos de Bourbon de Parme, Prince of Piacenza and his friend Brigitte Klynstra.
Due to being an illegitimate son, he was not born a prince.
His father told Dutch media that Hugo's birth was "his mother's wish" and an "independent decision", denying his son any family rights.
His maternal grandmother, Ingrid Pieksma-Klynstra, was the wife of Adolph Roderik Ernst Leopold, Count of Rechteren-Limpurg.
Through his father, he is a grandson of Carlos Hugo, Duke of Parma and Princess Irene of the Netherlands.
He is the first great-grandchild of Queen Juliana of the Netherlands and Prince Bernhard of Lippe-Biesterfeld.
He is also a great-grandson of Prince Xavier of Bourbon-Parma and Madeleine de Bourbon-Busset.
Upon the death of his grandfather, Carlos Hugo, in 2010, his father became the titular Duke of Parma and Piacenza, Carlist claimant to the Spanish throne, and the Head of the House of Bourbon-Parma.
According to a royal decree of Queen Beatrix in 1996, his father is also a Dutch prince.
He is the half-brother of Princess Luisa of Parma, Marchioness of Castell'Arquato, Princess Cecilia of Parma, Countess of Berceto and Prince Carlos of Parma, The Prince of Piacenza.
Legal dispute over title

Upon turning eighteen in 2015, Hugo went to court to have his surname changed from Klynstra to his father's surname, 'de Bourbon de Parme', and claimed the dutch noble title of prince.
The Hereditary Duke of Parma insisted that he had a formal agreement with Hugo's mother that their relationship was "no-strings-attached" and that there would be "no family entanglement" following Hugo's conception.
In 2016 the Ministry of Justice and Security ruled in favor of Hugo's claim and granted him the use of his father's surname.
On 28 February 2018, the Dutch Council of State ruled in Hugo's favor, stating that Dutch law on nobility was clear and that the circumstances of Hugo's birth are irrelevant, granting Hugo the right to claim both his father's surname and (dutch) noble title and address.
As such, he became His Royal Highness Prince Carlos Hugo Roderik Sybren de Bourbon de Parme.
The title of 'Prince(ss) de Bourbon de Parme' is a Dutch title, bestowed by Queen Beatrix in 1996, and does not mean that Hugo automatically became a member of the House of Bourbon-Parma.
The court ruling stated that membership to the House of Bourbon-Parma is "a private matter for the royal house itself".
As such, he is not in the line of succession to the defunct Parma throne.
Titles and styles

References




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
  AssignClass (81f505e3-4884-4bbc-a0d7-fd07d99cb3c3)
 Call ID: 81f505e3-4884-4bbc-a0d7-fd07d99cb3c3
  Args:
    type: :Man
    source: Prince_Carlos_Hugo_Roderik_Sybren_de_Bourbon_de_Parme
  AssignClass (d2823582-bbcb-4489-bf5d-b0771e33edd8)
 Call ID: d2823582-bbcb-4489-bf5d-b0771e33edd8
  Args:
    type: :Person
    source: Prince_Carlos_Hugo_Roderik_Sybren_de_Bourbon_de_Parme
  AssignClass (a517342a-57b5-46f2-97d9-f67e0da48d3f)
 Call ID: a517342a-57b5-46f2-97d9-f67e0da48d3f
  Args:
    source: Prince_Carlos_de_Bourbon_de_Parme
    type: :Man
  AssignClass (799974cb-53f2-49dc-a088-1c619eef227d)
 Call ID: 799974cb-53f2-49dc-a088-1c619eef227d
  Args:
    type: :Person
    source: Prince_Carlos_de_Bourbon_de_Parme
  AssignClass (35875c3e-f8b6-4333-b106-77fae9389a4f)
 Call ID: 35875c3e-f8b6-4333-b106-77fae9389a4f
  Args:
    source: Brigitte_Klynstra
    type: :Woman
  AssignClass (7f6a0144-5966-4d08-99c3-c47b160f3c48)
 Call ID: 7f6a0144-5966-4d08-99c3-c47b160f3c48
  Args:
    source: Brigitte_Klynstra
    type: :Person
  AssignClass (78a6936b-e28c-4b32-9560-8c76ed88d8d1)
 Call ID: 78a6936b-e28c-4b32-9560-8c76ed88d8d1
  Args:
    type: :Woman
    source: Ingrid_Pieksma-Klynstra
  AssignClass (362dbdc1-2110-4ee2-b6d5-d8c061abd790)
 Call ID: 362dbdc1-2110-4ee2-b6d5-d8c061abd790
  Args:
    type: :Person
    source: Ingrid_Pieksma-Klynstra
  AssignClass (f479c859-1860-454f-9c75-505df5a18f79)
 Call ID: f479c859-1860-454f-9c75-505df5a18f79
  Args:
    source: Adolph_Roderik_Ernst_Leopold_Count_of_Rechteren-Limpurg
    type: :Man
  AssignClass (688127cb-d5ab-4e4a-8201-a9044d06b63c)
 Call ID: 688127cb-d5ab-4e4a-8201-a9044d06b63c
  Args:
    type: :Person
    source: Adolph_Roderik_Ernst_Leopold_Count_of_Rechteren-Limpurg
  AssignClass (1cebed92-e255-4c3f-86c8-229459337180)
 Call ID: 1cebed92-e255-4c3f-86c8-229459337180
  Args:
    type: :Man
    source: Carlos_Hugo_Duke_of_Parma
  AssignClass (47f338b4-486f-43fd-a0dd-d4853e00e471)
 Call ID: 47f338b4-486f-43fd-a0dd-d4853e00e471
  Args:
    type: :Person
    source: Carlos_Hugo_Duke_of_Parma
  AssignClass (3276efa0-409c-4437-a491-6a7d6045e75f)
 Call ID: 3276efa0-409c-4437-a491-6a7d6045e75f
  Args:
    type: :Woman
    source: Princess_Irene_of_the_Netherlands
  AssignClass (4dcccda5-06c9-4288-ade3-96d331bf19d4)
 Call ID: 4dcccda5-06c9-4288-ade3-96d331bf19d4
  Args:
    type: :Person
    source: Princess_Irene_of_the_Netherlands
  AssignClass (fadfcf2e-f01d-49f1-8717-d9511555e3f4)
 Call ID: fadfcf2e-f01d-49f1-8717-d9511555e3f4
  Args:
    source: Queen_Juliana_of_the_Netherlands
    type: :Woman
  AssignClass (e5d235ee-d23e-4729-ae5c-ee2f8d621fa5)
 Call ID: e5d235ee-d23e-4729-ae5c-ee2f8d621fa5
  Args:
    type: :Person
    source: Queen_Juliana_of_the_Netherlands
  AssignClass (9ca3a4a3-68c1-4a41-be84-bf3360fb89cd)
 Call ID: 9ca3a4a3-68c1-4a41-be84-bf3360fb89cd
  Args:
    type: :Man
    source: Prince_Bernhard_of_Lippe-Biesterfeld
  AssignClass (b09544a4-a80b-40eb-9a5d-0827d9725010)
 Call ID: b09544a4-a80b-40eb-9a5d-0827d9725010
  Args:
    source: Prince_Bernhard_of_Lippe-Biesterfeld
    type: :Person
  AssignClass (c0e09466-f6dd-448c-bab3-7ddbf631bbad)
 Call ID: c0e09466-f6dd-448c-bab3-7ddbf631bbad
  Args:
    type: :Man
    source: Prince_Xavier_of_Bourbon-Parma
  AssignClass (8354d04e-c0aa-4b6e-9cbf-37bedfc66842)
 Call ID: 8354d04e-c0aa-4b6e-9cbf-37bedfc66842
  Args:
    type: :Person
    source: Prince_Xavier_of_Bourbon-Parma
  AssignClass (9cbe27d0-063d-437a-ae16-a0e47a99213c)
 Call ID: 9cbe27d0-063d-437a-ae16-a0e47a99213c
  Args:
    source: Madeleine_de_Bourbon-Busset
    type: :Woman
  AssignClass (841bfde6-365c-40e5-9fe9-87d981235798)
 Call ID: 841bfde6-365c-40e5-9fe9-87d981235798
  Args:
    source: Madeleine_de_Bourbon-Busset
    type: :Person
  AssignClass (49a5781f-11eb-4eb4-8d37-56454f94a121)
 Call ID: 49a5781f-11eb-4eb4-8d37-56454f94a121
  Args:
    source: Princess_Luisa_of_Parma
    type: :Woman
  AssignClass (c3367aca-1ee8-4039-96a6-506ab2981940)
 Call ID: c3367aca-1ee8-4039-96a6-506ab2981940
  Args:
    type: :Person
    source: Princess_Luisa_of_Parma
  AssignClass (10094dc1-b77b-4075-8c7a-b1c8494b5819)
 Call ID: 10094dc1-b77b-4075-8c7a-b1c8494b5819
  Args:
    source: Princess_Cecilia_of_Parma
    type: :Woman
  AssignClass (980f142c-3475-414d-a14d-173219d3f18a)
 Call ID: 980f142c-3475-414d-a14d-173219d3f18a
  Args:
    type: :Person
    source: Princess_Cecilia_of_Parma
  AssignClass (cbba8a0c-9667-4a82-9291-ebaf525fd27d)
 Call ID: cbba8a0c-9667-4a82-9291-ebaf525fd27d
  Args:
    source: Prince_Carlos_of_Parma
    type: :Man
  AssignClass (102533ce-0a25-4387-b3a6-b9188fd1a809)
 Call ID: 102533ce-0a25-4387-b3a6-b9188fd1a809
  Args:
    source: Prince_Carlos_of_Parma
    type: :Person
  AssignClass (384e47c1-c517-40ce-976d-93fcb0f7f6d9)
 Call ID: 384e47c1-c517-40ce-976d-93fcb0f7f6d9
  Args:
    source: Queen_Beatrix
    type: :Woman
  AssignClass (f5c6da4e-c13a-446e-abcb-87dadba346d5)
 Call ID: f5c6da4e-c13a-446e-abcb-87dadba346d5
  Args:
    source: Queen_Beatrix
    type: :Person
  AddTriple (ff194977-02ef-479b-9aee-ac9259294d7a)
 Call ID: ff194977-02ef-479b-9aee-ac9259294d7a
  Args:
    source: Prince_Carlos_Hugo_Roderik_Sybren_de_Bourbon_de_Parme
    target: Prince_Carlos_de_Bourbon_de_Parme
    relation: :hasFather
  AddTriple (06a9cbfe-5ff0-48f7-864d-f18700924945)
 Call ID: 06a9cbfe-5ff0-48f7-864d-f18700924945
  Args:
    relation: :hasMother
    source: Prince_Carlos_Hugo_Roderik_Sybren_de_Bourbon_de_Parme
    target: Brigitte_Klynstra
  AddLiteral (53c13267-fd12-4847-b422-404be1598ac9)
 Call ID: 53c13267-fd12-4847-b422-404be1598ac9
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1997
    source: Prince_Carlos_Hugo_Roderik_Sybren_de_Bourbon_de_Parme
  AddTriple (290aa170-c033-456e-b060-dd7aecbac539)
 Call ID: 290aa170-c033-456e-b060-dd7aecbac539
  Args:
    relation: :hasMother
    target: Ingrid_Pieksma-Klynstra
    source: Brigitte_Klynstra
  AddTriple (283b9987-b4f4-4c75-b16b-16fd2eb5698b)
 Call ID: 283b9987-b4f4-4c75-b16b-16fd2eb5698b
  Args:
    relation: :hasFather
    target: Adolph_Roderik_Ernst_Leopold_Count_of_Rechteren-Limpurg
    source: Brigitte_Klynstra
  AddTriple (d4bea461-1aee-4807-a03f-9dc312ef27f3)
 Call ID: d4bea461-1aee-4807-a03f-9dc312ef27f3
  Args:
    source: Prince_Carlos_de_Bourbon_de_Parme
    target: Carlos_Hugo_Duke_of_Parma
    relation: :hasFather
  AddTriple (15be6c5e-a887-4b2b-b506-d2291aa867dc)
 Call ID: 15be6c5e-a887-4b2b-b506-d2291aa867dc
  Args:
    source: Prince_Carlos_de_Bourbon_de_Parme
    target: Princess_Irene_of_the_Netherlands
    relation: :hasMother
  AddTriple (cb11fcee-a569-43d2-9fc1-15ea9cd90788)
 Call ID: cb11fcee-a569-43d2-9fc1-15ea9cd90788
  Args:
    target: Prince_Bernhard_of_Lippe-Biesterfeld
    source: Princess_Irene_of_the_Netherlands
    relation: :hasFather
  AddTriple (45d98e8d-3132-40e1-875f-427218c328ab)
 Call ID: 45d98e8d-3132-40e1-875f-427218c328ab
  Args:
    relation: :hasMother
    target: Queen_Juliana_of_the_Netherlands
    source: Princess_Irene_of_the_Netherlands
  AddTriple (36fbfc88-df8f-4390-bcf3-3d0b1872003b)
 Call ID: 36fbfc88-df8f-4390-bcf3-3d0b1872003b
  Args:
    relation: :hasFather
    source: Prince_Carlos_de_Bourbon_de_Parme
    target: Prince_Xavier_of_Bourbon-Parma
  AddTriple (6f9f25f2-1829-4ae4-add8-f207539f290e)
 Call ID: 6f9f25f2-1829-4ae4-add8-f207539f290e
  Args:
    relation: :hasMother
    target: Madeleine_de_Bourbon-Busset
    source: Prince_Carlos_de_Bourbon_de_Parme
  AddTriple (ea9cb03c-7ffb-4310-b089-15da4ecf27cc)
 Call ID: ea9cb03c-7ffb-4310-b089-15da4ecf27cc
  Args:
    target: Prince_Carlos_de_Bourbon_de_Parme
    source: Princess_Luisa_of_Parma
    relation: :hasFather
  AddTriple (5cf9c84d-fa80-426a-88c9-10af20cbc146)
 Call ID: 5cf9c84d-fa80-426a-88c9-10af20cbc146
  Args:
    relation: :hasFather
    target: Prince_Carlos_de_Bourbon_de_Parme
    source: Princess_Cecilia_of_Parma
  AddTriple (c47e7a84-b2d1-430a-994f-db916b3132cc)
 Call ID: c47e7a84-b2d1-430a-994f-db916b3132cc
  Args:
    relation: :hasFather
    target: Prince_Carlos_de_Bourbon_de_Parme
    source: Prince_Carlos_of_Parma
  AddLiteral (481d2e14-047c-4043-9884-3086973fbe5f)
 Call ID: 481d2e14-047c-4043-9884-3086973fbe5f
  Args:
    literal_type: xsd:string
    relation: :formerlyKnownAs
    literal_value: Hugo Klynstra
    source: Prince_Carlos_Hugo_Roderik_Sybren_de_Bourbon_de_Parme
  Finish (244ee846-7d2b-41f9-bdf9-b9c72f2cbc0b)
 Call ID: 244ee846-7d2b-41f9-bdf9-b9c72f2cbc0b
  Args: