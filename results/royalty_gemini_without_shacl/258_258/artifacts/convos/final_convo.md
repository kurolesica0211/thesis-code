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
The Duke of CalabriaThe Duchess of Calabria


Prince Pedro of Bourbon-Two Sicilies, Duke of Calabria, Grandee of Spain (Spanish: Pedro Juan María Alejo Saturnino de Todos los Santos; born 16 October 1968), is the only son of Infante Carlos, Duke of Calabria, and Princess Anne of Orléans.
Claim

He is the only son of Infante Carlos, Duke of Calabria (1938–2015), and his wife, Princess Anne of Orléans.
The other claimant is Prince Carlo, Duke of Castro.
He is also a grandee of Spain, as the son of an infante of Spain.
On 14 December 1900, Prince Carlos, next oldest brother to the childless Prince Ferdinand, head of the House of Bourbon-Two Sicilies and immediate heir of their father, claimant to the former throne of the Two Sicilies, signed a private agreement purporting to renounce the "future succession" to the former crown before his marriage to María de las Mercedes, Princess of Asturias, heiress presumptive to the throne of Spain.
This document, known as the Act of Cannes, was signed in purported obedience to the 1759 Pragmatic Sanction signed by Charles III of Spain where it was established that the thrones of Spain and Naples should never be united in the person of the same monarch, separating them forever to preserve the European balance of power.
The Act of Cannes states:


Before Us, Don Alfonso de Borbón, Count of Caserta... Head of the Royal House and Dynasty of the Two Sicilies...
His Royal Highness Prince Don Carlos, our beloved Son, appears and declares that, preparing to marry HRH Infanta María de las Mercedes, Princess of Asturias, and assuming by such marriage the nationality and quality of Spanish Prince, undertakes to renounce by this Act and solemnly renounces, for himself and for his heirs and successors, all the right and reason to the eventual succession to the Crown of the Two Sicilies and to all the assets of the Royal House that are in Italy and elsewhere, and this according to our Laws, constitutions and Family customs, in execution of the Pragmatic Sanction of King Charles III, our Augustus ancestor, of October 6, 1759, the prescriptions of which he freely and spontaneously declares to subscribe and obey.
He also declares, in particular, to renounce for himself, his heirs and successors to the assets and values existing in Italy, Vienna and Munich and destined by His Majesty King Francis II (may God have welcomed his soul), to the foundation of a majorat for the Head of the Dynasty and of the Family of the Two Sicilies and for the constitution of an endowment fund in favor of the Royal Princesses and granddaughters of our August Father King Ferdinand (may God have welcomed his soul), of marriageable age; but preserving his rights to the part of the assets that were bequeathed to him by his late uncle King Francis II, in the event that the Italian Government, which improperly retains them, makes the due restitution and the same everything that may arrive to him by other testamentary legacies.
— Cannes, 14 December 1900

Supporters of the other claimant to the headship of the House of Bourbon-Two Sicilies, sometimes referred to as the Castrist faction, argue that because Prince Carlos signed this agreement, he relinquished all of his rights and those of his descendants to both the headship of the family and the Sacred Military Constantinian Order of Saint George, and so the rights currently fall on Prince Carlo, Duke of Castro.
However, supporters of Pedro, also known as the legitimists, argue that the Act of Cannes was subject to a condition that never arose and its terms would have only applied if the wife of Prince Carlos had inherited the throne of Spain, and he had become king of the Two Sicilies, which never happened and was furthermore highly unlikely at the time the document was created.
In due course, Prince Carlos inherited his share of properties of the royal family in Italy, despite the purported renunciation, with no objection by his brothers and sisters.
Marriage and issue

Pedro married Sofía Landaluce y Melgarejo (born 23
November 1973 in Madrid), daughter of José Manuel Landaluce y Domínguez and his wife María de las Nieves Blanca Melgarejo y González (granddaughter of the Dukes of San Fernando de Quiroga), on 30 March 2001 at Real Club de la Puerta de Hierro in Madrid.
Pedro and Sofía have seven children:


Honours

Dynastic




National

Other activities

Arms

Ancestors

Notes

References

Bibliography

External links



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
  AssignClass (b91b539c-b9a6-43e2-b7e5-43e9047c8bd5)
 Call ID: b91b539c-b9a6-43e2-b7e5-43e9047c8bd5
  Args:
    source: Prince_Pedro
    type: :Man
  AssignClass (774fdc36-0b41-47a1-a956-c84bb4068d2a)
 Call ID: 774fdc36-0b41-47a1-a956-c84bb4068d2a
  Args:
    source: Prince_Pedro
    type: :Person
  AssignClass (d0d539de-ef3f-44bf-844f-fa494f4461e9)
 Call ID: d0d539de-ef3f-44bf-844f-fa494f4461e9
  Args:
    source: Infante_Carlos
    type: :Man
  AssignClass (5f84d9e2-2f6d-4e1b-833c-9b64033040cd)
 Call ID: 5f84d9e2-2f6d-4e1b-833c-9b64033040cd
  Args:
    source: Infante_Carlos
    type: :Person
  AssignClass (9cb7650e-9616-484e-b963-608cc44f994c)
 Call ID: 9cb7650e-9616-484e-b963-608cc44f994c
  Args:
    type: :Woman
    source: Princess_Anne_of_Orleans
  AssignClass (f4b3f66a-0a5f-40cf-8344-9374bc2083c5)
 Call ID: f4b3f66a-0a5f-40cf-8344-9374bc2083c5
  Args:
    type: :Person
    source: Princess_Anne_of_Orleans
  AssignClass (f2064a13-691f-4b8b-a0a5-82c848fa73b3)
 Call ID: f2064a13-691f-4b8b-a0a5-82c848fa73b3
  Args:
    source: Sofia_Landaluce_y_Melgarejo
    type: :Woman
  AssignClass (bbbf906e-0fbf-43a9-9fa1-196a67a5e18e)
 Call ID: bbbf906e-0fbf-43a9-9fa1-196a67a5e18e
  Args:
    type: :Person
    source: Sofia_Landaluce_y_Melgarejo
  AssignClass (7d546578-a6f8-47a3-b1a3-0f7cf2d4c5fb)
 Call ID: 7d546578-a6f8-47a3-b1a3-0f7cf2d4c5fb
  Args:
    type: :Man
    source: Jose_Manuel_Landaluce_y_Dominguez
  AssignClass (5e2c70ef-7ca4-472f-a186-11b2315c0392)
 Call ID: 5e2c70ef-7ca4-472f-a186-11b2315c0392
  Args:
    source: Jose_Manuel_Landaluce_y_Dominguez
    type: :Person
  AssignClass (eadfd4c9-575c-4bd0-a30e-deae36557a91)
 Call ID: eadfd4c9-575c-4bd0-a30e-deae36557a91
  Args:
    type: :Woman
    source: Maria_de_las_Nieves_Blanca_Melgarejo_y_Gonzalez
  AssignClass (f109d9a8-7861-499c-9d03-8d5b4532fab6)
 Call ID: f109d9a8-7861-499c-9d03-8d5b4532fab6
  Args:
    type: :Person
    source: Maria_de_las_Nieves_Blanca_Melgarejo_y_Gonzalez
  AddTriple (1a97b1e1-a1b4-4b17-9c08-e7a7f645b26c)
 Call ID: 1a97b1e1-a1b4-4b17-9c08-e7a7f645b26c
  Args:
    relation: :hasFather
    source: Prince_Pedro
    target: Infante_Carlos
  AddTriple (77b77342-e200-4715-beab-0a6c420af400)
 Call ID: 77b77342-e200-4715-beab-0a6c420af400
  Args:
    relation: :hasMother
    target: Princess_Anne_of_Orleans
    source: Prince_Pedro
  AddTriple (30768709-0a08-4cb9-ac61-c0a5241e4b9b)
 Call ID: 30768709-0a08-4cb9-ac61-c0a5241e4b9b
  Args:
    relation: :hasFather
    source: Sofia_Landaluce_y_Melgarejo
    target: Jose_Manuel_Landaluce_y_Dominguez
  AddTriple (7e4c0067-ea18-48f4-9781-02557829a3ce)
 Call ID: 7e4c0067-ea18-48f4-9781-02557829a3ce
  Args:
    target: Maria_de_las_Nieves_Blanca_Melgarejo_y_Gonzalez
    source: Sofia_Landaluce_y_Melgarejo
    relation: :hasMother
  AddLiteral (dc8d0995-0639-40f0-86e4-3e246596ce8c)
 Call ID: dc8d0995-0639-40f0-86e4-3e246596ce8c
  Args:
    literal_type: xsd:integer
    literal_value: 1968
    source: Prince_Pedro
    relation: :hasBirthYear
  AddLiteral (9636d555-4681-4d07-95c1-2dfdede39a85)
 Call ID: 9636d555-4681-4d07-95c1-2dfdede39a85
  Args:
    relation: :hasBirthYear
    source: Infante_Carlos
    literal_value: 1938
    literal_type: xsd:integer
  AddLiteral (5b5c447a-ff05-41a2-9266-9d46da03f46a)
 Call ID: 5b5c447a-ff05-41a2-9266-9d46da03f46a
  Args:
    literal_type: xsd:integer
    literal_value: 2015
    source: Infante_Carlos
    relation: :hasDeathYear
  AddLiteral (134b0a80-991f-437d-9558-c9bc34cc4d58)
 Call ID: 134b0a80-991f-437d-9558-c9bc34cc4d58
  Args:
    literal_value: 1973
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Sofia_Landaluce_y_Melgarejo
  AddLiteral (415dcb8e-d553-469d-b49e-5f2c878071f4)
 Call ID: 415dcb8e-d553-469d-b49e-5f2c878071f4
  Args:
    source: Prince_Pedro
    relation: :hasMarriageYear
    literal_type: xsd:integer
    literal_value: 2001
  Finish (b558decb-5d03-4c4e-be63-0be24d98108f)
 Call ID: b558decb-5d03-4c4e-be63-0be24d98108f
  Args: