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
The Duke of Castro  The Duchess of Castro


Prince Carlo of Bourbon-Two Sicilies, Duke of Castro (born 24 February 1963) is one of two claimants to the headship of the House of Bourbon-Two Sicilies.
Early life

Prince Carlo was born in Saint-Raphaël, Var, France, the only son of Prince Ferdinand, Duke of Castro and Chantal de Chevron-Villette.
Marriage and issue

Prince Carlo married Camilla Crociani, daughter of Italian billionaire Camillo Crociani and his second wife, Italian actress Edy Vessel, on 31 October 1998 at the Cathedral of Our Lady Immaculate in the Monaco-Ville ward of Monaco.
The couple were introduced to each other by Albert II, Prince of Monaco.
Notable guests at the wedding included Rainier III, Prince of Monaco, Albert, Hereditary Prince of Monaco (later Prince Albert II of Monaco), and Prince Laurent of Belgium.
Together Carlo and Camilla have two daughters:


Prince Carlo is also a godfather to Princess Josephine of Denmark, the youngest child of King Frederik X and Queen Mary of Denmark, and attended her confirmation in 2026.
He and Princess Camilla are regarded as close friends of the Danish King and Queen.
Claimed headship of the House of Bourbon-Two Sicilies

In 2008, Carlo succeeded to his father's claim as head of the House of the Two Sicilies and the use of the title Duke of Castro.
Carlos married María de las Mercedes, Princess of Asturias, the heir presumptive of Spain, in 1901.
Alfonso's line of the family (today represented by Carlo's rival claimant, Pedro) has been officially recognized as the legitimate line by the Government of Spain, the Spanish royal house, the Parmesan royal house and the Portuguese royal house, whereas Ranieri's line was recognized by many non-ruling European dynasts of former monarchies (no current monarch except the king of Spain has officially stated its view on the matter), namely the Count of Paris, Umberto of Italy, Gottfried of Austria-Tuscany, the Duke of Bavaria, the Duke of Württemberg, the Duke of Aosta, the Duke of Genoa, the Duke of Hohenberg, Prince Luiz of Orléans-Braganza and Prince Michael of Greece, as well as all other members of the Sicilian house itself.
It has been argued by some that the Counts of Paris supported the Castro line simply because their own pretence to the French throne depends entirely on the same principle of renunciation as the Act of Cannes, and so it would be against their own interest to support the Calabrian line.
Interestingly, most of the other outspoken supporters of the Castro line were either sons-in-law of the Count of Paris or closely related to him.
Honours

Dynastic

Ecclesiastical

National

Foreign

In letters dated 21 July 2017, the Governor-General of Antigua and Barbuda issued a notice that the Duke of Castro's 2014 appointment to the Order of the Nation had been annulled.
In 2020, the branch of the Constantinian Order led by Prince Carlo was alleged to have influenced the election of Patricia Scotland as Commonwealth Secretary-General, which a spokesman for the Order denied, saying "These allegations are wholly offensive and wrong".



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
  AssignClass (606b690b-6f53-49da-8047-982d105b245d)
 Call ID: 606b690b-6f53-49da-8047-982d105b245d
  Args:
    type: :Man
    source: Prince_Carlo_of_Bourbon-Two_Sicilies
  AssignClass (24a77a15-fefe-4c8b-a04a-861465e08dfc)
 Call ID: 24a77a15-fefe-4c8b-a04a-861465e08dfc
  Args:
    type: :Man
    source: Prince_Ferdinand_Duke_of_Castro
  AssignClass (6a544ee5-1b28-4fa3-b047-105c683dfb5e)
 Call ID: 6a544ee5-1b28-4fa3-b047-105c683dfb5e
  Args:
    type: :Woman
    source: Chantal_de_Chevron-Villette
  AssignClass (42daa146-23d3-42e6-b446-fb1fbc05361c)
 Call ID: 42daa146-23d3-42e6-b446-fb1fbc05361c
  Args:
    type: :Woman
    source: Camilla_Crociani
  AssignClass (4dfcddf5-0aa4-4157-918a-10e4323b7872)
 Call ID: 4dfcddf5-0aa4-4157-918a-10e4323b7872
  Args:
    type: :Man
    source: Camillo_Crociani
  AssignClass (99de8597-d88e-4c82-87fe-6232045ca3b2)
 Call ID: 99de8597-d88e-4c82-87fe-6232045ca3b2
  Args:
    type: :Woman
    source: Edy_Vessel
  AddLiteral (e4ba2ffe-acdf-4962-bc44-d42468167ecb)
 Call ID: e4ba2ffe-acdf-4962-bc44-d42468167ecb
  Args:
    literal_type: xsd:integer
    source: Prince_Carlo_of_Bourbon-Two_Sicilies
    literal_value: 1963
    relation: :hasBirthYear
  AddTriple (d2cce0f0-a363-497d-9b16-c4899f5cc8f1)
 Call ID: d2cce0f0-a363-497d-9b16-c4899f5cc8f1
  Args:
    target: Prince_Ferdinand_Duke_of_Castro
    source: Prince_Carlo_of_Bourbon-Two_Sicilies
    relation: :hasFather
  AddTriple (14dd6984-bd61-4306-acaf-27e0e90c16dd)
 Call ID: 14dd6984-bd61-4306-acaf-27e0e90c16dd
  Args:
    target: Chantal_de_Chevron-Villette
    source: Prince_Carlo_of_Bourbon-Two_Sicilies
    relation: :hasMother
  AddTriple (86c6023c-48dd-4b49-ab51-42d3bf21d68d)
 Call ID: 86c6023c-48dd-4b49-ab51-42d3bf21d68d
  Args:
    target: Camillo_Crociani
    source: Camilla_Crociani
    relation: :hasFather
  AddTriple (cabb0d63-7a40-4757-a56e-e8966b84a39a)
 Call ID: cabb0d63-7a40-4757-a56e-e8966b84a39a
  Args:
    relation: :hasMother
    target: Edy_Vessel
    source: Camilla_Crociani
  AddLiteral (a3c7fbdd-0bc8-4b0b-af1c-3d3b5be98bba)
 Call ID: a3c7fbdd-0bc8-4b0b-af1c-3d3b5be98bba
  Args:
    literal_value: 1998
    relation: :hasMarriageYear
    source: Prince_Carlo_of_Bourbon-Two_Sicilies
    literal_type: xsd:integer
  AddTriple (0a30358b-2cf2-4024-836c-d67b38625688)
 Call ID: 0a30358b-2cf2-4024-836c-d67b38625688
  Args:
    source: Prince_Carlo_of_Bourbon-Two_Sicilies
    target: Camilla_Crociani
    relation: :hasRelation
  Finish (bed7f22e-672f-412e-85e8-418932f6f339)
 Call ID: bed7f22e-672f-412e-85e8-418932f6f339
  Args: