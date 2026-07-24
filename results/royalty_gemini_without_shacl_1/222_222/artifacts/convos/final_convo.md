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
@prefix ns1: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
@prefix ns2: <http://www.w3.org/2003/11/swrl#> .
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

ns1:isRuleEnabled a owl:AnnotationProperty .

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

:x a ns2:Variable .

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

:y a ns2:Variable .

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

[] a ns2:Imp ;
    rdfs:label "infer hasSon" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasBrother" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasSister" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (27a42522-0d75-4f44-b24b-ff6a78060fac)
 Call ID: 27a42522-0d75-4f44-b24b-ff6a78060fac
  Args:
    source: Princess_Theodora_of_Greece_and_Denmark
    type: :Woman
  AssignClass (84a42cea-f556-4660-80f6-8f32939d304e)
 Call ID: 84a42cea-f556-4660-80f6-8f32939d304e
  Args:
    type: :Person
    source: Princess_Theodora_of_Greece_and_Denmark
  AddLiteral (346db01a-60a4-4e7b-8365-fa1fc70f8855)
 Call ID: 346db01a-60a4-4e7b-8365-fa1fc70f8855
  Args:
    literal_value: 1983
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Princess_Theodora_of_Greece_and_Denmark
  AddLiteral (61cd70b7-0e73-4181-872c-d70227ea26c3)
 Call ID: 61cd70b7-0e73-4181-872c-d70227ea26c3
  Args:
    literal_type: xsd:string
    relation: :alsoKnownAs
    source: Princess_Theodora_of_Greece_and_Denmark
    literal_value: Theodora Greece
  AssignClass (a5acc3bd-57f3-453d-a437-d8f2154e3fd6)
 Call ID: a5acc3bd-57f3-453d-a437-d8f2154e3fd6
  Args:
    source: Constantine_II_of_Greece
    type: :Man
  AssignClass (ed66aee9-e8d0-4a6b-9c24-9291d02679e1)
 Call ID: ed66aee9-e8d0-4a6b-9c24-9291d02679e1
  Args:
    type: :Ancestor
    source: Constantine_II_of_Greece
  AssignClass (569426ec-ff46-412c-ab91-60c86b51b84d)
 Call ID: 569426ec-ff46-412c-ab91-60c86b51b84d
  Args:
    type: :Woman
    source: Anne-Marie_of_Denmark
  AssignClass (aedd58c2-9b16-457b-9d7e-bc080e5c2999)
 Call ID: aedd58c2-9b16-457b-9d7e-bc080e5c2999
  Args:
    source: Anne-Marie_of_Denmark
    type: :Ancestor
  AddTriple (7503abe1-8bbd-4318-97c9-d81768cc97c6)
 Call ID: 7503abe1-8bbd-4318-97c9-d81768cc97c6
  Args:
    source: Princess_Theodora_of_Greece_and_Denmark
    relation: :hasFather
    target: Constantine_II_of_Greece
  AddTriple (e91a5bf3-5579-4cbb-a802-060d41136741)
 Call ID: e91a5bf3-5579-4cbb-a802-060d41136741
  Args:
    source: Princess_Theodora_of_Greece_and_Denmark
    relation: :hasMother
    target: Anne-Marie_of_Denmark
  AssignClass (5f54c6ca-9175-4f3e-b214-94b0bde2a699)
 Call ID: 5f54c6ca-9175-4f3e-b214-94b0bde2a699
  Args:
    type: :Man
    source: Matthew_Jeremiah_Kumar
  AssignClass (aab4cc62-ab34-47d2-9e0a-791b1a5bef37)
 Call ID: aab4cc62-ab34-47d2-9e0a-791b1a5bef37
  Args:
    type: :Person
    source: Matthew_Jeremiah_Kumar
  AddLiteral (60141be8-c4a3-47e8-98c3-37d2013b5de4)
 Call ID: 60141be8-c4a3-47e8-98c3-37d2013b5de4
  Args:
    literal_value: 2024
    literal_type: xsd:integer
    relation: :hasMarriageYear
    source: Princess_Theodora_of_Greece_and_Denmark
  AddTriple (178eef3a-6023-4d5b-b985-6a27d9863ec0)
 Call ID: 178eef3a-6023-4d5b-b985-6a27d9863ec0
  Args:
    source: Princess_Theodora_of_Greece_and_Denmark
    relation: :hasRelation
    target: Matthew_Jeremiah_Kumar
  AssignClass (d70a58ec-3e33-4105-8308-535b200cb288)
 Call ID: d70a58ec-3e33-4105-8308-535b200cb288
  Args:
    type: :Woman
    source: Queen_Sofia_of_Spain
  AssignClass (0cb83bfd-0672-44f1-9301-d07ed7e00fa4)
 Call ID: 0cb83bfd-0672-44f1-9301-d07ed7e00fa4
  Args:
    source: Queen_Sofia_of_Spain
    type: :Person
  AddTriple (f9b1aedf-32ce-4bc8-8d44-430cf39b0173)
 Call ID: f9b1aedf-32ce-4bc8-8d44-430cf39b0173
  Args:
    relation: :isAuntOf
    target: Princess_Theodora_of_Greece_and_Denmark
    source: Queen_Sofia_of_Spain
  AssignClass (a74e561d-f9b4-4709-b1a1-197a3896e956)
 Call ID: a74e561d-f9b4-4709-b1a1-197a3896e956
  Args:
    type: :Man
    source: Paul_of_Greece
  AssignClass (7b43b77a-5ef3-4c28-be0d-eae08adc71a9)
 Call ID: 7b43b77a-5ef3-4c28-be0d-eae08adc71a9
  Args:
    type: :Ancestor
    source: Paul_of_Greece
  AssignClass (4548693c-8e2b-4ebc-adc3-346b44ccea31)
 Call ID: 4548693c-8e2b-4ebc-adc3-346b44ccea31
  Args:
    type: :Woman
    source: Frederica_of_Hanover
  AssignClass (6d9010e8-11a2-449e-93b5-e345eab9eaa3)
 Call ID: 6d9010e8-11a2-449e-93b5-e345eab9eaa3
  Args:
    type: :Ancestor
    source: Frederica_of_Hanover
  AddTriple (cd74b2ed-d17b-49c0-9fb7-601dd73ed859)
 Call ID: cd74b2ed-d17b-49c0-9fb7-601dd73ed859
  Args:
    source: Constantine_II_of_Greece
    target: Paul_of_Greece
    relation: :hasFather
  AddTriple (316f8cd3-98d8-4970-a475-a814abc2dfb3)
 Call ID: 316f8cd3-98d8-4970-a475-a814abc2dfb3
  Args:
    source: Constantine_II_of_Greece
    target: Frederica_of_Hanover
    relation: :hasMother
  AssignClass (d03a3bdf-815b-4c72-af4b-57ba16467c46)
 Call ID: d03a3bdf-815b-4c72-af4b-57ba16467c46
  Args:
    type: :Man
    source: Frederik_IX_of_Denmark
  AssignClass (0ab176e7-2b55-48da-8f44-f19fbeb17fe4)
 Call ID: 0ab176e7-2b55-48da-8f44-f19fbeb17fe4
  Args:
    type: :Ancestor
    source: Frederik_IX_of_Denmark
  AssignClass (b012e63c-2989-4ebe-8acd-3da95cb6e74a)
 Call ID: b012e63c-2989-4ebe-8acd-3da95cb6e74a
  Args:
    source: Ingrid_of_Sweden
    type: :Woman
  AssignClass (c499d2b7-1c87-489d-b70a-b1274f335e61)
 Call ID: c499d2b7-1c87-489d-b70a-b1274f335e61
  Args:
    type: :Ancestor
    source: Ingrid_of_Sweden
  AddTriple (02891d7a-f965-4086-8f3f-dd2fb11c635a)
 Call ID: 02891d7a-f965-4086-8f3f-dd2fb11c635a
  Args:
    source: Anne-Marie_of_Denmark
    target: Frederik_IX_of_Denmark
    relation: :hasFather
  AddTriple (3ae0a2b0-ed79-48bb-887a-f8933d40aa44)
 Call ID: 3ae0a2b0-ed79-48bb-887a-f8933d40aa44
  Args:
    source: Anne-Marie_of_Denmark
    relation: :hasMother
    target: Ingrid_of_Sweden
  Finish (a08a2cf7-111f-4521-951d-748c568dd278)
 Call ID: a08a2cf7-111f-4521-951d-748c568dd278
  Args: