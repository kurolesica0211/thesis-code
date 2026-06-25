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
  AssignClass (40f871e3-c1be-40bb-b534-0f9f600350d1)
 Call ID: 40f871e3-c1be-40bb-b534-0f9f600350d1
  Args:
    type: :Woman
    source: :Theodora_of_Greece_and_Denmark
  AssignClass (f3311e36-54fe-4ac3-8154-d89ef905ad64)
 Call ID: f3311e36-54fe-4ac3-8154-d89ef905ad64
  Args:
    source: :Theodora_of_Greece_and_Denmark
    type: :Person
  AddLiteral (d22d129c-9775-4b3d-9947-e8699accbc13)
 Call ID: d22d129c-9775-4b3d-9947-e8699accbc13
  Args:
    relation: :knownAs
    literal_type: xsd:string
    source: :Theodora_of_Greece_and_Denmark
    literal_value: Theodora Greece
  AddLiteral (0848d431-b736-4c81-a724-18c1c050cb91)
 Call ID: 0848d431-b736-4c81-a724-18c1c050cb91
  Args:
    relation: :alsoKnownAs
    literal_type: xsd:string
    source: :Theodora_of_Greece_and_Denmark
    literal_value: Theodora de Grèce
  AddLiteral (282f9e92-8ebe-4563-a747-ca60e1b7b8b6)
 Call ID: 282f9e92-8ebe-4563-a747-ca60e1b7b8b6
  Args:
    source: :Theodora_of_Greece_and_Denmark
    literal_type: xsd:integer
    literal_value: 1983
    relation: :hasBirthYear
  AssignClass (432216bb-a749-443b-baec-17a3ab7646f7)
 Call ID: 432216bb-a749-443b-baec-17a3ab7646f7
  Args:
    source: :Constantine_II_of_Greece
    type: :Man
  AssignClass (0854b3f4-b6d0-46d7-b7b5-071f130faae4)
 Call ID: 0854b3f4-b6d0-46d7-b7b5-071f130faae4
  Args:
    source: :Constantine_II_of_Greece
    type: :Person
  AssignClass (a32c5720-d107-475b-ad55-18bc596323c2)
 Call ID: a32c5720-d107-475b-ad55-18bc596323c2
  Args:
    type: :Woman
    source: :Anne-Marie_of_Denmark
  AssignClass (477ab4b9-1701-496f-8f1a-04a8c9146d6a)
 Call ID: 477ab4b9-1701-496f-8f1a-04a8c9146d6a
  Args:
    source: :Anne-Marie_of_Denmark
    type: :Person
  AddTriple (ed24dd98-bbad-46af-8c2e-e1c78269bd0b)
 Call ID: ed24dd98-bbad-46af-8c2e-e1c78269bd0b
  Args:
    target: :Constantine_II_of_Greece
    relation: :hasFather
    source: :Theodora_of_Greece_and_Denmark
  AddTriple (33dab734-a25d-4bad-ad92-febb9e1aa5b7)
 Call ID: 33dab734-a25d-4bad-ad92-febb9e1aa5b7
  Args:
    relation: :hasMother
    target: :Anne-Marie_of_Denmark
    source: :Theodora_of_Greece_and_Denmark
  AssignClass (4a2365b2-aae2-4101-af5c-a5336343e30e)
 Call ID: 4a2365b2-aae2-4101-af5c-a5336343e30e
  Args:
    source: :Matthew_Jeremiah_Kumar
    type: :Man
  AssignClass (6e59ee05-43b0-49d4-aff4-52c146ceb0c3)
 Call ID: 6e59ee05-43b0-49d4-aff4-52c146ceb0c3
  Args:
    type: :Person
    source: :Matthew_Jeremiah_Kumar
  AddLiteral (ee9c5416-8f35-4eee-b1df-8873f3b9c2cf)
 Call ID: ee9c5416-8f35-4eee-b1df-8873f3b9c2cf
  Args:
    literal_type: xsd:integer
    source: :Theodora_of_Greece_and_Denmark
    literal_value: 2024
    relation: :hasMarriageYear
  AddTriple (40f37f15-cfb7-4564-ac9a-409d82e68b15)
 Call ID: 40f37f15-cfb7-4564-ac9a-409d82e68b15
  Args:
    target: :Matthew_Jeremiah_Kumar
    relation: :hasRelation
    source: :Theodora_of_Greece_and_Denmark
  AssignClass (dce0da59-e2d0-4719-afee-0dd80ed4adef)
 Call ID: dce0da59-e2d0-4719-afee-0dd80ed4adef
  Args:
    source: :Sofia_of_Spain
    type: :Woman
  AssignClass (70b15320-2676-4499-a5a8-8c4f06bbd3ec)
 Call ID: 70b15320-2676-4499-a5a8-8c4f06bbd3ec
  Args:
    type: :Person
    source: :Sofia_of_Spain
  AddTriple (f29ceea4-7150-485e-af55-d623ee4fcbeb)
 Call ID: f29ceea4-7150-485e-af55-d623ee4fcbeb
  Args:
    source: :Sofia_of_Spain
    target: :Theodora_of_Greece_and_Denmark
    relation: :hasRelation
  AddLiteral (338a7a67-a735-4a28-9587-ec53ef71b2e1)
 Call ID: 338a7a67-a735-4a28-9587-ec53ef71b2e1
  Args:
    literal_value: Queen Sofia of Spain
    literal_type: xsd:string
    source: :Sofia_of_Spain
    relation: :knownAs
  AssignClass (7e4b6813-287e-45a7-bcbb-7a78afb45cb5)
 Call ID: 7e4b6813-287e-45a7-bcbb-7a78afb45cb5
  Args:
    type: :Man
    source: :Paul_of_Greece
  AssignClass (1ab6e473-5dcf-4402-bc62-c9c767948cfc)
 Call ID: 1ab6e473-5dcf-4402-bc62-c9c767948cfc
  Args:
    source: :Paul_of_Greece
    type: :Person
  AssignClass (997c9526-133a-4fab-8b8b-103d3e73bebc)
 Call ID: 997c9526-133a-4fab-8b8b-103d3e73bebc
  Args:
    type: :Woman
    source: :Frederica_of_Hanover
  AssignClass (8135a9e8-bc0e-4f89-963a-885c28b89270)
 Call ID: 8135a9e8-bc0e-4f89-963a-885c28b89270
  Args:
    type: :Person
    source: :Frederica_of_Hanover
  AddTriple (b70e4948-def6-49e7-aef6-a45892645524)
 Call ID: b70e4948-def6-49e7-aef6-a45892645524
  Args:
    target: :Paul_of_Greece
    relation: :hasFather
    source: :Constantine_II_of_Greece
  AddTriple (fcabdb3e-cc42-4242-85ff-f113ed496d48)
 Call ID: fcabdb3e-cc42-4242-85ff-f113ed496d48
  Args:
    source: :Constantine_II_of_Greece
    target: :Frederica_of_Hanover
    relation: :hasMother
  AssignClass (e4ba5361-03e5-44be-8729-47f13317a1ff)
 Call ID: e4ba5361-03e5-44be-8729-47f13317a1ff
  Args:
    type: :Man
    source: :Frederik_IX_of_Denmark
  AssignClass (0059a0ce-a35f-4b1a-9910-a897a223ac1b)
 Call ID: 0059a0ce-a35f-4b1a-9910-a897a223ac1b
  Args:
    source: :Frederik_IX_of_Denmark
    type: :Person
  AssignClass (91821a12-4319-4432-a4db-6fc5e93ea688)
 Call ID: 91821a12-4319-4432-a4db-6fc5e93ea688
  Args:
    source: :Ingrid_of_Sweden
    type: :Woman
  AssignClass (776a6c40-209e-4e61-b0bd-028865f5c350)
 Call ID: 776a6c40-209e-4e61-b0bd-028865f5c350
  Args:
    type: :Person
    source: :Ingrid_of_Sweden
  AddTriple (abaeb5e2-7cdc-4415-a0e6-540785a2ac3c)
 Call ID: abaeb5e2-7cdc-4415-a0e6-540785a2ac3c
  Args:
    target: :Frederik_IX_of_Denmark
    relation: :hasFather
    source: :Anne-Marie_of_Denmark
  AddTriple (31512f42-4dde-4b88-999b-4667f5903baa)
 Call ID: 31512f42-4dde-4b88-999b-4667f5903baa
  Args:
    source: :Anne-Marie_of_Denmark
    target: :Ingrid_of_Sweden
    relation: :hasMother
  Finish (9ff4c05d-80c4-4f61-abf4-11129908af5a)
 Call ID: 9ff4c05d-80c4-4f61-abf4-11129908af5a
  Args: