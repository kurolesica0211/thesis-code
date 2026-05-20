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
Infante Jaime of Spain, Duke of Segovia  (Spanish: Don Jaime Leopoldo Isabelino Enrique Alejandro Alberto Alfonso Víctor Acacio Pedro Pablo María de Borbón y Battenberg; French: Jacques Léopold Isabellin Henri Alexandre Albért Alphonse Victor Acace Pierre Paul Marie de Bourbon; 23 June 1908 – 20 March 1975), was the second son of King Alfonso XIII of Spain and his wife, Princess Victoria Eugenie of Battenberg.
Early life

Infante Jaime was born 23 June 1908 at the Royal Palace of La Granja de San Ildefonso, the second son of King Alfonso XIII and his Hessian wife, Victoria Eugenie of Battenberg, the youngest granddaughter of Queen Victoria.
He had three brothers, Alfonso, Prince of Asturias (1907–1938), Infante Juan, Count of Barcelona (1913–1993), and  Infante Gonzalo (1914–1934); and two younger sisters, Infanta Beatriz (1909–2002) and Infanta María Cristina (1911–1996).
His elder brother, the Prince of Asturias, and his youngest brother, Gonzalo, both had the bleeding disorder hemophilia, the genetic condition that plagued many descendants of Queen Victoria.
Infante Jaime was born with an infection of the inner ear that progressively worsened, causing him to gradually lose his hearing.
On 11 June 1933, his elder brother and heir to the defunct throne, Alfonso, renounced his title of Prince of Asturias in order to marry a Cuban commoner.
Infante Jaime then held the title of Prince of Asturias, as successor to the throne of Spain, for only ten days before under pressure from his father, he was forced also to renounce his rights and the rights of his heirs, in favor of his younger, healthier brother Infante Juan.
He was then granted the title "Duke of Segovia" by King Alfonso XIII.
Don Jaime and Donna Emanuela had two sons, named after Jaime's brothers, Alfonso and Gonzalo:


Don Jaime and Emmanuelle de Dampierre divorced on 6 May 1947 in Bucharest (recognized by the Italian courts on 3 June 1949 in Turin but never recognized in Spain) and, on 3 August 1949 in Innsbruck, Don Jaime remarried civilly to divorced singer Charlotte Luise Auguste Tiedemann (2 January 1919 in Königsberg – 3 July 1979 in Berlin), daughter of Otto Eugen Tiedemann and wife Luise Amalia Klein.
In the eyes of the Roman Catholic Church and of the French legitimists, Emmanuelle de Dampierre remained always his wife.
On 3 May 1964, he took the title "Duke of Madrid" as head of a Carlist branch of the Spanish succession (recognized by the legitimist group of Carlists who did not support the Bourbon-Parma claim after Alfonso Carlos, Duke of San Jaime died in 1936).
On 19 July 1969, Don Jaime definitively renounced the Spanish succession in favour of his nephew, the future King Juan Carlos I, at the request of his elder son, Alfonso de Borbón.



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
  AssignClass (669dd883-d49a-431c-abfd-cd2a9e768da6)
 Call ID: 669dd883-d49a-431c-abfd-cd2a9e768da6
  Args:
    type: :Man
    source: Infante_Jaime_of_Spain
  AssignClass (2cf5efe9-f751-4659-8465-f969ca7cc8a3)
 Call ID: 2cf5efe9-f751-4659-8465-f969ca7cc8a3
  Args:
    type: :Man
    source: King_Alfonso_XIII_of_Spain
  AssignClass (a7cbb6c8-e933-4c6d-ac86-779308730d87)
 Call ID: a7cbb6c8-e933-4c6d-ac86-779308730d87
  Args:
    type: :Woman
    source: Princess_Victoria_Eugenie_of_Battenberg
  AssignClass (9a8b4e9d-d3f2-442b-99c5-e999753a28f5)
 Call ID: 9a8b4e9d-d3f2-442b-99c5-e999753a28f5
  Args:
    source: Alfonso_Prince_of_Asturias
    type: :Man
  AssignClass (02edee0f-f289-4a4b-a6b4-cc0acb6551ee)
 Call ID: 02edee0f-f289-4a4b-a6b4-cc0acb6551ee
  Args:
    source: Infante_Juan_Count_of_Barcelona
    type: :Man
  AssignClass (50d848cb-51a4-44e2-b82a-cb72699e86c5)
 Call ID: 50d848cb-51a4-44e2-b82a-cb72699e86c5
  Args:
    type: :Man
    source: Infante_Gonzalo
  AssignClass (d5a432f3-c42b-49b4-834c-1651ae9bfba6)
 Call ID: d5a432f3-c42b-49b4-834c-1651ae9bfba6
  Args:
    type: :Woman
    source: Infanta_Beatriz
  AssignClass (6f35b372-7d07-4265-95d3-788ea45696ae)
 Call ID: 6f35b372-7d07-4265-95d3-788ea45696ae
  Args:
    type: :Woman
    source: Infanta_Maria_Cristina
  AssignClass (a0687c91-c5be-496b-b88b-0403cc01b9aa)
 Call ID: a0687c91-c5be-496b-b88b-0403cc01b9aa
  Args:
    type: :Woman
    source: Donna_Emanuela_de_Dampierre
  AssignClass (7c421249-2b04-4168-9685-d153331b4abd)
 Call ID: 7c421249-2b04-4168-9685-d153331b4abd
  Args:
    type: :Man
    source: Alfonso_de_Borbon_son_of_Jaime
  AssignClass (d1ef5611-db4e-4a7c-a74c-0b67f5b51355)
 Call ID: d1ef5611-db4e-4a7c-a74c-0b67f5b51355
  Args:
    type: :Man
    source: Gonzalo_son_of_Jaime
  AssignClass (415a0969-3187-4b9d-85da-a5a18724f1ef)
 Call ID: 415a0969-3187-4b9d-85da-a5a18724f1ef
  Args:
    source: Charlotte_Luise_Auguste_Tiedemann
    type: :Woman
  AssignClass (34324f75-73ba-4245-9b62-63a1a6095a42)
 Call ID: 34324f75-73ba-4245-9b62-63a1a6095a42
  Args:
    type: :Man
    source: Otto_Eugen_Tiedemann
  AssignClass (753b5436-cb2e-42bb-aca4-9f11cb3d2c49)
 Call ID: 753b5436-cb2e-42bb-aca4-9f11cb3d2c49
  Args:
    type: :Woman
    source: Luise_Amalia_Klein
  AddTriple (1a3af346-0181-4155-937e-6e8d9afbbc31)
 Call ID: 1a3af346-0181-4155-937e-6e8d9afbbc31
  Args:
    source: Infante_Jaime_of_Spain
    target: King_Alfonso_XIII_of_Spain
    relation: :hasFather
  AddTriple (ff812691-f52a-406c-9669-2b1c71e639c4)
 Call ID: ff812691-f52a-406c-9669-2b1c71e639c4
  Args:
    relation: :hasMother
    target: Princess_Victoria_Eugenie_of_Battenberg
    source: Infante_Jaime_of_Spain
  AddTriple (e28ad8f7-611e-463b-b3b7-fe0469b6c738)
 Call ID: e28ad8f7-611e-463b-b3b7-fe0469b6c738
  Args:
    source: Infante_Jaime_of_Spain
    target: Alfonso_Prince_of_Asturias
    relation: :hasBrother
  AddTriple (cb49c0ab-c307-44ed-a1e9-05cc6175a5e6)
 Call ID: cb49c0ab-c307-44ed-a1e9-05cc6175a5e6
  Args:
    relation: :hasBrother
    source: Infante_Jaime_of_Spain
    target: Infante_Juan_Count_of_Barcelona
  AddTriple (c9dee716-76b6-43f1-875e-05b1ad8decce)
 Call ID: c9dee716-76b6-43f1-875e-05b1ad8decce
  Args:
    target: Infante_Gonzalo
    source: Infante_Jaime_of_Spain
    relation: :hasBrother
  AddTriple (245ec4f7-0d22-4bed-b294-c696c9efa44b)
 Call ID: 245ec4f7-0d22-4bed-b294-c696c9efa44b
  Args:
    source: Infante_Jaime_of_Spain
    target: Infanta_Beatriz
    relation: :hasSister
  AddTriple (8db482b7-1f2e-4e73-a96c-5f3f30bc3be3)
 Call ID: 8db482b7-1f2e-4e73-a96c-5f3f30bc3be3
  Args:
    source: Infante_Jaime_of_Spain
    target: Infanta_Maria_Cristina
    relation: :hasSister
  AddTriple (266ef726-e85b-4c72-b0d8-37427592bfc6)
 Call ID: 266ef726-e85b-4c72-b0d8-37427592bfc6
  Args:
    target: Alfonso_de_Borbon_son_of_Jaime
    source: Infante_Jaime_of_Spain
    relation: :hasSon
  AddTriple (31f64c6d-7713-4b6c-9bd2-a3cc529fc81c)
 Call ID: 31f64c6d-7713-4b6c-9bd2-a3cc529fc81c
  Args:
    relation: :hasSon
    source: Infante_Jaime_of_Spain
    target: Gonzalo_son_of_Jaime
  AddTriple (3ac06931-6944-4ca5-8458-d0c4596b8e06)
 Call ID: 3ac06931-6944-4ca5-8458-d0c4596b8e06
  Args:
    relation: :hasFather
    source: Charlotte_Luise_Auguste_Tiedemann
    target: Otto_Eugen_Tiedemann
  AddTriple (bb0de3a8-0ccd-41a4-a239-28999df603fe)
 Call ID: bb0de3a8-0ccd-41a4-a239-28999df603fe
  Args:
    relation: :hasMother
    source: Charlotte_Luise_Auguste_Tiedemann
    target: Luise_Amalia_Klein
  AddLiteral (33ed98d9-3a01-4c25-8c7f-a30dcf0fe7a7)
 Call ID: 33ed98d9-3a01-4c25-8c7f-a30dcf0fe7a7
  Args:
    literal_type: xsd:integer
    source: Infante_Jaime_of_Spain
    relation: :hasBirthYear
    literal_value: 1908
  AddLiteral (ae4466ba-93c1-4b4d-9e64-304c6d4a3fd4)
 Call ID: ae4466ba-93c1-4b4d-9e64-304c6d4a3fd4
  Args:
    literal_type: xsd:integer
    source: Infante_Jaime_of_Spain
    relation: :hasDeathYear
    literal_value: 1975
  AddLiteral (e18e4392-ae0d-462a-847e-f7d6c153c665)
 Call ID: e18e4392-ae0d-462a-847e-f7d6c153c665
  Args:
    source: Charlotte_Luise_Auguste_Tiedemann
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1919
  AddLiteral (ec28f393-ad29-4fff-89af-179feb5d5748)
 Call ID: ec28f393-ad29-4fff-89af-179feb5d5748
  Args:
    source: Charlotte_Luise_Auguste_Tiedemann
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1979
  Finish (46e54798-34a0-47d9-806d-824aa3bb5d21)
 Call ID: 46e54798-34a0-47d9-806d-824aa3bb5d21
  Args: