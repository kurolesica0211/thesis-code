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
@prefix ns1: <http://www.w3.org/2003/11/swrl#> .
@prefix ns2: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
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

:hasDeathYear a owl:AnnotationProperty .

:hasMarriageYear a owl:AnnotationProperty .

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

ns2:isRuleEnabled a owl:AnnotationProperty .

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

:isAncestorOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation .

:isSisterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf .

:hasChild a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:inverseOf :isChildOf .

:hasParent a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Person ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:equivalentProperty :isChildOf ;
    owl:inverseOf :isParentOf .

:isSiblingOf a owl:ObjectProperty,
        owl:SymmetricProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isBloodrelationOf ;
    owl:propertyChainAxiom ( :hasParent :isParentOf ) .

:Sex a owl:Class ;
    rdfs:subClassOf :DomainEntity ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Female :Male ) ] .

:isChildOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:propertyDisjointWith :isSisterOf .

:x a ns1:Variable .

:Man a owl:Class ;
    owl:disjointWith :Sex,
        :Woman ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Male ] ) ] .

:isParentOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:propertyDisjointWith :isSisterOf .

:Woman a owl:Class ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Female ] ) ] .

:y a ns1:Variable .

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

[] a ns1:Imp ;
    rdfs:label "infer hasSon" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasBrother" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasSister" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (abbc5256-701f-42f0-b3d8-80f0fcd8bb95)
 Call ID: abbc5256-701f-42f0-b3d8-80f0fcd8bb95
  Args:
    type: :Person
    source: Theodora
  AssignClass (3af2dda8-c99a-4951-97ac-e7ea0fcd40df)
 Call ID: 3af2dda8-c99a-4951-97ac-e7ea0fcd40df
  Args:
    type: :Woman
    source: Theodora
  AssignClass (c957d625-c68a-49e7-9a8e-60921899c483)
 Call ID: c957d625-c68a-49e7-9a8e-60921899c483
  Args:
    source: Constantine_II_of_Greece
    type: :Person
  AssignClass (771732ca-e829-43d5-9042-d2bc7321123d)
 Call ID: 771732ca-e829-43d5-9042-d2bc7321123d
  Args:
    type: :Man
    source: Constantine_II_of_Greece
  AssignClass (fe0b0545-8982-4046-bac1-c81675ce9ab6)
 Call ID: fe0b0545-8982-4046-bac1-c81675ce9ab6
  Args:
    source: Anne-Marie_of_Greece
    type: :Person
  AssignClass (fc9aa52b-d7d8-4423-b76e-712978835122)
 Call ID: fc9aa52b-d7d8-4423-b76e-712978835122
  Args:
    type: :Woman
    source: Anne-Marie_of_Greece
  AddLiteral (9bd2d014-471e-4636-8637-cb03444f58d0)
 Call ID: 9bd2d014-471e-4636-8637-cb03444f58d0
  Args:
    relation: :hasBirthYear
    source: Theodora
    literal_value: 1983
    literal_type: xsd:integer
  AddLiteral (2d5bdf89-7d56-45f8-b1ba-ba447dfdb7c5)
 Call ID: 2d5bdf89-7d56-45f8-b1ba-ba447dfdb7c5
  Args:
    literal_type: xsd:string
    literal_value: Theodora Greece
    source: Theodora
    relation: :knownAs
  AddTriple (a06b3099-88a1-42ca-a003-9d9e9c0c7cc6)
 Call ID: a06b3099-88a1-42ca-a003-9d9e9c0c7cc6
  Args:
    source: Theodora
    relation: :hasFather
    target: Constantine_II_of_Greece
  AddTriple (55174972-76db-4176-b833-6d380b21b63d)
 Call ID: 55174972-76db-4176-b833-6d380b21b63d
  Args:
    target: Anne-Marie_of_Greece
    relation: :hasMother
    source: Theodora
  AssignClass (c22ba8ff-db10-4023-8225-ac6173f04857)
 Call ID: c22ba8ff-db10-4023-8225-ac6173f04857
  Args:
    type: :Person
    source: Matthew_Jeremiah_Kumar
  AssignClass (4a275aec-bf1a-4bc5-bbd1-e3aee3014e54)
 Call ID: 4a275aec-bf1a-4bc5-bbd1-e3aee3014e54
  Args:
    source: Matthew_Jeremiah_Kumar
    type: :Man
  AddTriple (a0293729-5979-46de-a055-870810dc6ad4)
 Call ID: a0293729-5979-46de-a055-870810dc6ad4
  Args:
    target: Matthew_Jeremiah_Kumar
    relation: :hasRelation
    source: Theodora
  AddLiteral (1ad431ef-865a-4d71-8cdc-58dcabd62b4c)
 Call ID: 1ad431ef-865a-4d71-8cdc-58dcabd62b4c
  Args:
    literal_type: xsd:integer
    literal_value: 2024
    source: Theodora
    relation: :hasMarriageYear
  AssignClass (f0da696e-ee2d-48bf-ace3-bc238ab31c43)
 Call ID: f0da696e-ee2d-48bf-ace3-bc238ab31c43
  Args:
    type: :Person
    source: Paul_of_Greece
  AssignClass (1df066b4-0bac-4f6d-9051-77e77ad03016)
 Call ID: 1df066b4-0bac-4f6d-9051-77e77ad03016
  Args:
    type: :Man
    source: Paul_of_Greece
  AssignClass (f0384ce4-5e70-4ac7-ad82-f7e4b596dc3a)
 Call ID: f0384ce4-5e70-4ac7-ad82-f7e4b596dc3a
  Args:
    source: Frederica_of_Hanover
    type: :Person
  AssignClass (2495a211-a6f5-489d-a15a-e77e336f9382)
 Call ID: 2495a211-a6f5-489d-a15a-e77e336f9382
  Args:
    source: Frederica_of_Hanover
    type: :Woman
  AssignClass (3ba26103-bbf5-413d-9f98-a8852c0a85d9)
 Call ID: 3ba26103-bbf5-413d-9f98-a8852c0a85d9
  Args:
    source: Frederik_IX_of_Denmark
    type: :Person
  AssignClass (244ba902-bbd4-4f31-9937-9ec7167892f3)
 Call ID: 244ba902-bbd4-4f31-9937-9ec7167892f3
  Args:
    source: Frederik_IX_of_Denmark
    type: :Man
  AssignClass (7a3b3056-10d0-4273-a934-000747e7f6b1)
 Call ID: 7a3b3056-10d0-4273-a934-000747e7f6b1
  Args:
    source: Ingrid_of_Sweden
    type: :Person
  AssignClass (ea52c725-e4fb-4f80-ba35-717d637bbc98)
 Call ID: ea52c725-e4fb-4f80-ba35-717d637bbc98
  Args:
    type: :Woman
    source: Ingrid_of_Sweden
  AddTriple (f76cd441-d083-4eac-bd25-ce3c68a2e8c3)
 Call ID: f76cd441-d083-4eac-bd25-ce3c68a2e8c3
  Args:
    relation: :hasFather
    source: Constantine_II_of_Greece
    target: Paul_of_Greece
  AddTriple (086c1e94-1247-484c-85f6-3ecb64cb5a1c)
 Call ID: 086c1e94-1247-484c-85f6-3ecb64cb5a1c
  Args:
    relation: :hasMother
    source: Constantine_II_of_Greece
    target: Frederica_of_Hanover
  AddTriple (6d05f81c-1809-4e08-831c-0f82f8e1996a)
 Call ID: 6d05f81c-1809-4e08-831c-0f82f8e1996a
  Args:
    target: Frederik_IX_of_Denmark
    relation: :hasFather
    source: Anne-Marie_of_Greece
  AddTriple (9942caf2-f480-44ee-9a23-ea379d015658)
 Call ID: 9942caf2-f480-44ee-9a23-ea379d015658
  Args:
    relation: :hasMother
    source: Anne-Marie_of_Greece
    target: Ingrid_of_Sweden
  AssignClass (c24ad91a-cabb-4e5a-9e14-ee2202802431)
 Call ID: c24ad91a-cabb-4e5a-9e14-ee2202802431
  Args:
    type: :Person
    source: Sofia_of_Spain
  AssignClass (0dabc38f-51b6-44f9-947b-83cd164b5deb)
 Call ID: 0dabc38f-51b6-44f9-947b-83cd164b5deb
  Args:
    source: Sofia_of_Spain
    type: :Woman
  AddTriple (4f7282cd-375e-4a47-b4be-9df39c44c7b0)
 Call ID: 4f7282cd-375e-4a47-b4be-9df39c44c7b0
  Args:
    relation: :isAuntOf
    source: Sofia_of_Spain
    target: Theodora
  Finish (61e8c685-656d-452c-8a1d-e1e687e09100)
 Call ID: 61e8c685-656d-452c-8a1d-e1e687e09100
  Args: