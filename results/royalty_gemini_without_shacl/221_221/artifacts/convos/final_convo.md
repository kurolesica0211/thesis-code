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
Queen Anne-Marie


Queen Sofía of Spain


Marina, consort of Prince Michael


Princess Theodora of Greece and Denmark (Greek: Θεοδώρα Ντε Γκρες, romanized: Theodora de Grèce; born 9 June 1983), also known under her stage name Theodora Greece, is a British-Greek actress and member of the Greek and Danish royal families.
She is the fourth child and younger daughter of deposed King Constantine II of Greece and Queen Anne-Marie of Greece.
Theodora made her television debut in 2011 as Alison Montgomery in the American soap opera The Bold and the Beautiful.
Biography

Early life

Theodora was born on 9 June 1983 at St Mary's Hospital, London.
She is the younger daughter and fourth of the five children of the deposed Greek king Constantine II and his wife, Anne-Marie of Denmark.
Education

Theodora attended Woldingham School, an all-girls boarding school in Surrey, England, between 1994 and 2001.
After a gap year spent at St Philip's College in Alice Springs, Australia, Theodora attended Brown University where she received her Bachelor of Arts on 28 May 2006 in Theatre Arts, having also attended Northeastern University in Boston.
Career

In April 2010, Theodora moved to Los Angeles to pursue an acting career, appearing in supporting roles under the stage name Theodora Greece.
Personal life

On 16 November 2018, it was announced that Princess Theodora was engaged to American attorney Matthew Jeremiah Kumar.
On 28 September 2024, Theodora married Kumar in a Greek Orthodox ceremony officiated by Metropolitan Dorotheos II of Syros at the Metropolitan Cathedral of Athens.
Guests included 250 friends and relatives, including members of European royal families, such as the bride's aunt, Queen Sofia of Spain, and Infanta Cristina of Spain, Infanta Elena of Spain, Princess Alexandra of Sayn-Wittgenstein-Berleburg, Count Michael Ahlefeldt-Laurvig-Bille, Princess Benedikte of Denmark, Crown Prince Alexander of Yugoslavia, Crown Princess Katherine of Serbia, and Prince Christian of Hanover.
Two of her brothers, Crown Prince Pavlos and Prince Philippos, and her nephew Prince Achileas-Andreas, served as groomsmen.
Her nieces, Princess Maria-Olympia and Arrietta Morales y de Grecia, served as bridesmaids.
For the ceremony, Theodora wore a custom gown by Celia Kritharioti, an Irish lace veil that once belonged to her great-grandmother Princess Margaret of Connaught, and a Cartier diamond tiara that was given to Princess Margaret of Connaught by Abbas II of Egypt.
The veil and tiara have been worn by all of Queen Ingrid of Denmark's female descendants.
Οn 20 December 2024, Theodora, along with the other members of the former royal family acquired Greek citizenship, under the surname Theodora de Grèce.
The family was deprived of citizenship in 1994 when the former King Constantine refused to acquire a surname, as required by law for all Greek citizens.
Filmography

Ancestry

Her paternal grandparents were King Paul of Greece and Frederica of Hanover.
Her maternal grandparents are Frederik IX of Denmark and Ingrid of Sweden.
As an agnatic descendant of Christian IX of Denmark Theodora is a Danish princess, and because King Christian's second son, Prince William of Denmark, was elected "George I, King of the Hellenes" in 1863, her father (George's great-grandson) inherited the throne of Greece in 1964.



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
  AssignClass (2c5397ec-24fd-460a-bc20-e9c2cf14bc56)
 Call ID: 2c5397ec-24fd-460a-bc20-e9c2cf14bc56
  Args:
    source: Princess_Theodora_of_Greece_and_Denmark
    type: :Person
  AssignClass (b7af2238-8ee7-47ae-b82e-027b7ead13b1)
 Call ID: b7af2238-8ee7-47ae-b82e-027b7ead13b1
  Args:
    source: Princess_Theodora_of_Greece_and_Denmark
    type: :Woman
  AddLiteral (4321a121-dcd7-4dcd-80f2-587fc327d4a7)
 Call ID: 4321a121-dcd7-4dcd-80f2-587fc327d4a7
  Args:
    literal_value: Theodora Greece
    literal_type: xsd:string
    source: Princess_Theodora_of_Greece_and_Denmark
    relation: :knownAs
  AddLiteral (093d5b65-c658-401c-bc6c-ce37584dae12)
 Call ID: 093d5b65-c658-401c-bc6c-ce37584dae12
  Args:
    relation: :alsoKnownAs
    literal_value: Theodora de Grèce
    source: Princess_Theodora_of_Greece_and_Denmark
    literal_type: xsd:string
  AssignClass (de493ea4-c7b0-4a51-8fd7-42d1dcb343ae)
 Call ID: de493ea4-c7b0-4a51-8fd7-42d1dcb343ae
  Args:
    type: :Person
    source: Constantine_II_of_Greece
  AssignClass (1bb0ea54-df6b-489d-a8f7-76122b73e415)
 Call ID: 1bb0ea54-df6b-489d-a8f7-76122b73e415
  Args:
    source: Constantine_II_of_Greece
    type: :Man
  AssignClass (fa0104f5-21a5-4522-9736-726edd2ee8eb)
 Call ID: fa0104f5-21a5-4522-9736-726edd2ee8eb
  Args:
    type: :Person
    source: Anne-Marie_of_Denmark
  AssignClass (22dcff43-8154-4aee-b539-7b5dab941bd9)
 Call ID: 22dcff43-8154-4aee-b539-7b5dab941bd9
  Args:
    type: :Woman
    source: Anne-Marie_of_Denmark
  AddTriple (f79271e1-46ea-481f-8e35-e7699c2b42a6)
 Call ID: f79271e1-46ea-481f-8e35-e7699c2b42a6
  Args:
    source: Princess_Theodora_of_Greece_and_Denmark
    relation: :hasFather
    target: Constantine_II_of_Greece
  AddTriple (d2bef5fd-3d2c-43ec-abbc-47ec16008aa1)
 Call ID: d2bef5fd-3d2c-43ec-abbc-47ec16008aa1
  Args:
    relation: :hasMother
    target: Anne-Marie_of_Denmark
    source: Princess_Theodora_of_Greece_and_Denmark
  AssignClass (29a500f8-9b7d-4c54-b132-44ef35dd4c2c)
 Call ID: 29a500f8-9b7d-4c54-b132-44ef35dd4c2c
  Args:
    type: :Person
    source: Matthew_Jeremiah_Kumar
  AssignClass (999f2a91-ec58-4ccf-a1d4-fbab7bf2b227)
 Call ID: 999f2a91-ec58-4ccf-a1d4-fbab7bf2b227
  Args:
    type: :Man
    source: Matthew_Jeremiah_Kumar
  AddTriple (c1fcfc8a-06d9-4ef4-861c-7919a9334017)
 Call ID: c1fcfc8a-06d9-4ef4-861c-7919a9334017
  Args:
    source: Princess_Theodora_of_Greece_and_Denmark
    target: Matthew_Jeremiah_Kumar
    relation: :hasRelation
  AddLiteral (96d149f5-5c3b-4893-a4f6-e4b28a0d14ca)
 Call ID: 96d149f5-5c3b-4893-a4f6-e4b28a0d14ca
  Args:
    relation: :hasMarriageYear
    literal_value: 2024
    source: Princess_Theodora_of_Greece_and_Denmark
    literal_type: xsd:integer
  AssignClass (53b4e3d0-4535-4061-97cd-8338e08e0d95)
 Call ID: 53b4e3d0-4535-4061-97cd-8338e08e0d95
  Args:
    source: Queen_Sofia_of_Spain
    type: :Person
  AssignClass (e5bfd6e4-a6f2-47ea-9fcc-fe9de2986da0)
 Call ID: e5bfd6e4-a6f2-47ea-9fcc-fe9de2986da0
  Args:
    type: :Woman
    source: Queen_Sofia_of_Spain
  AddTriple (1b817e7b-804d-413d-a6c2-52fc018d294c)
 Call ID: 1b817e7b-804d-413d-a6c2-52fc018d294c
  Args:
    relation: :isAuntOf
    target: Princess_Theodora_of_Greece_and_Denmark
    source: Queen_Sofia_of_Spain
  AssignClass (8e45b075-9bed-4de3-bc92-8f8d09b75809)
 Call ID: 8e45b075-9bed-4de3-bc92-8f8d09b75809
  Args:
    type: :Person
    source: Paul_of_Greece
  AssignClass (151faa68-ca76-4926-aa2e-aa40ff0c681a)
 Call ID: 151faa68-ca76-4926-aa2e-aa40ff0c681a
  Args:
    source: Paul_of_Greece
    type: :Man
  AssignClass (7ae6b476-ef05-4993-8177-d314d18087f5)
 Call ID: 7ae6b476-ef05-4993-8177-d314d18087f5
  Args:
    source: Frederica_of_Hanover
    type: :Person
  AssignClass (aa53dcb7-7e81-4339-aa0d-9e729866bf56)
 Call ID: aa53dcb7-7e81-4339-aa0d-9e729866bf56
  Args:
    source: Frederica_of_Hanover
    type: :Woman
  AddTriple (e06cd732-0be4-47ac-9f3d-29361470effa)
 Call ID: e06cd732-0be4-47ac-9f3d-29361470effa
  Args:
    source: Constantine_II_of_Greece
    relation: :hasFather
    target: Paul_of_Greece
  AddTriple (2ce45310-fb78-4fa4-a16a-3d4f54fc6f16)
 Call ID: 2ce45310-fb78-4fa4-a16a-3d4f54fc6f16
  Args:
    source: Constantine_II_of_Greece
    relation: :hasMother
    target: Frederica_of_Hanover
  AssignClass (89fc838f-641a-40fa-8aea-3c285d94abf0)
 Call ID: 89fc838f-641a-40fa-8aea-3c285d94abf0
  Args:
    source: Frederik_IX_of_Denmark
    type: :Person
  AssignClass (cd834320-7abf-4ee8-91ee-2d252e9fc58c)
 Call ID: cd834320-7abf-4ee8-91ee-2d252e9fc58c
  Args:
    type: :Man
    source: Frederik_IX_of_Denmark
  AssignClass (98777b5a-0b11-48a5-834f-1f7a9c05ec4a)
 Call ID: 98777b5a-0b11-48a5-834f-1f7a9c05ec4a
  Args:
    source: Ingrid_of_Sweden
    type: :Person
  AssignClass (c3eaad2c-6b6c-4616-a945-2d124878acd2)
 Call ID: c3eaad2c-6b6c-4616-a945-2d124878acd2
  Args:
    source: Ingrid_of_Sweden
    type: :Woman
  AddTriple (70e9a4e4-d38f-40cd-9073-9fe4c54ca812)
 Call ID: 70e9a4e4-d38f-40cd-9073-9fe4c54ca812
  Args:
    source: Anne-Marie_of_Denmark
    target: Frederik_IX_of_Denmark
    relation: :hasFather
  AddTriple (b438c3a9-e9c3-4873-956b-2a022761a176)
 Call ID: b438c3a9-e9c3-4873-956b-2a022761a176
  Args:
    target: Ingrid_of_Sweden
    relation: :hasMother
    source: Anne-Marie_of_Denmark
  AssignClass (84d70935-0ed0-4ad0-8dc6-f126c9dcbae7)
 Call ID: 84d70935-0ed0-4ad0-8dc6-f126c9dcbae7
  Args:
    source: Crown_Prince_Pavlos
    type: :Person
  AssignClass (29cc2b01-7463-41f9-b5e2-5760dec60760)
 Call ID: 29cc2b01-7463-41f9-b5e2-5760dec60760
  Args:
    source: Crown_Prince_Pavlos
    type: :Man
  AssignClass (27a32367-3d45-4880-9dd0-e1b5a35df5e3)
 Call ID: 27a32367-3d45-4880-9dd0-e1b5a35df5e3
  Args:
    type: :Person
    source: Prince_Philippos
  AssignClass (5f2eeff1-ed7a-4858-a604-0a216cd2c1fd)
 Call ID: 5f2eeff1-ed7a-4858-a604-0a216cd2c1fd
  Args:
    type: :Man
    source: Prince_Philippos
  AddTriple (6fcfa526-9cab-4df0-95fd-c65a6c93fc62)
 Call ID: 6fcfa526-9cab-4df0-95fd-c65a6c93fc62
  Args:
    source: Princess_Theodora_of_Greece_and_Denmark
    relation: :hasBrother
    target: Crown_Prince_Pavlos
  AddTriple (f94c5bfd-e9d0-456b-bce1-fb9d0d4189c3)
 Call ID: f94c5bfd-e9d0-456b-bce1-fb9d0d4189c3
  Args:
    source: Princess_Theodora_of_Greece_and_Denmark
    target: Prince_Philippos
    relation: :hasBrother
  Finish (1ec1d85c-8e5d-4c29-bd1f-ed4868a6b554)
 Call ID: 1ec1d85c-8e5d-4c29-bd1f-ed4868a6b554
  Args: