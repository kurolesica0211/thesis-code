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
  AssignClass (3fefb15d-73a0-41ec-9022-c7333796ac87)
 Call ID: 3fefb15d-73a0-41ec-9022-c7333796ac87
  Args:
    type: :Person
    source: Princess_Theodora_of_Greece_and_Denmark
  AssignClass (7adbbe3f-fe13-45b0-9d5e-017cd5d5dbc8)
 Call ID: 7adbbe3f-fe13-45b0-9d5e-017cd5d5dbc8
  Args:
    type: :Woman
    source: Princess_Theodora_of_Greece_and_Denmark
  AddLiteral (98ad8279-4416-4daa-81ce-c42da9391930)
 Call ID: 98ad8279-4416-4daa-81ce-c42da9391930
  Args:
    source: Princess_Theodora_of_Greece_and_Denmark
    literal_type: xsd:string
    relation: :knownAs
    literal_value: Theodora Greece
  AddLiteral (3afe5e41-f436-4fa1-9859-64f10dc64302)
 Call ID: 3afe5e41-f436-4fa1-9859-64f10dc64302
  Args:
    source: Princess_Theodora_of_Greece_and_Denmark
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1983
  AssignClass (636e8a90-96ef-4774-aef5-919d2c583c38)
 Call ID: 636e8a90-96ef-4774-aef5-919d2c583c38
  Args:
    type: :Person
    source: Constantine_II_of_Greece
  AssignClass (3186f78a-768d-485a-9ff0-1c7bc5665849)
 Call ID: 3186f78a-768d-485a-9ff0-1c7bc5665849
  Args:
    type: :Man
    source: Constantine_II_of_Greece
  AssignClass (ac2b8546-b36a-47a0-8019-47bb817aac54)
 Call ID: ac2b8546-b36a-47a0-8019-47bb817aac54
  Args:
    type: :Person
    source: Anne-Marie_of_Greece
  AssignClass (571a848e-05c8-419c-bbc0-df47b7a22b17)
 Call ID: 571a848e-05c8-419c-bbc0-df47b7a22b17
  Args:
    type: :Woman
    source: Anne-Marie_of_Greece
  AddTriple (82f5172f-65fb-41af-9729-7bd93dcc50ee)
 Call ID: 82f5172f-65fb-41af-9729-7bd93dcc50ee
  Args:
    source: Princess_Theodora_of_Greece_and_Denmark
    relation: :hasFather
    target: Constantine_II_of_Greece
  AddTriple (1f598e97-3dad-4cd7-b56a-84bd27df0f28)
 Call ID: 1f598e97-3dad-4cd7-b56a-84bd27df0f28
  Args:
    source: Princess_Theodora_of_Greece_and_Denmark
    relation: :hasMother
    target: Anne-Marie_of_Greece
  AssignClass (5aa9f6f6-039c-4eaf-aad2-1ce3f89e1829)
 Call ID: 5aa9f6f6-039c-4eaf-aad2-1ce3f89e1829
  Args:
    type: :Person
    source: Matthew_Jeremiah_Kumar
  AssignClass (791c4d1c-ea75-4a64-afa4-1696cc6be097)
 Call ID: 791c4d1c-ea75-4a64-afa4-1696cc6be097
  Args:
    type: :Man
    source: Matthew_Jeremiah_Kumar
  AddTriple (1cd76fbb-f3e5-4198-983d-e162893781ba)
 Call ID: 1cd76fbb-f3e5-4198-983d-e162893781ba
  Args:
    relation: :hasRelation
    source: Princess_Theodora_of_Greece_and_Denmark
    target: Matthew_Jeremiah_Kumar
  AddLiteral (a7c1fc2a-bc5b-4c35-8c34-2d76ff987672)
 Call ID: a7c1fc2a-bc5b-4c35-8c34-2d76ff987672
  Args:
    literal_value: 2024
    source: Princess_Theodora_of_Greece_and_Denmark
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AssignClass (1ab3857f-c3d3-4440-be59-d373207253fd)
 Call ID: 1ab3857f-c3d3-4440-be59-d373207253fd
  Args:
    type: :Person
    source: Queen_Sofia_of_Spain
  AssignClass (60bd02b5-ac8e-4970-8f32-05dbb80e40fe)
 Call ID: 60bd02b5-ac8e-4970-8f32-05dbb80e40fe
  Args:
    type: :Woman
    source: Queen_Sofia_of_Spain
  AddTriple (51c830ed-7965-4a71-aedb-fb8fcecc6f67)
 Call ID: 51c830ed-7965-4a71-aedb-fb8fcecc6f67
  Args:
    target: Princess_Theodora_of_Greece_and_Denmark
    source: Queen_Sofia_of_Spain
    relation: :isAuntOf
  AssignClass (b57a5f95-73e4-4b9c-8386-d864f5d0a47e)
 Call ID: b57a5f95-73e4-4b9c-8386-d864f5d0a47e
  Args:
    type: :Person
    source: Paul_of_Greece
  AssignClass (ee655f8b-5147-4b0e-9514-c0944a8ce86a)
 Call ID: ee655f8b-5147-4b0e-9514-c0944a8ce86a
  Args:
    type: :Man
    source: Paul_of_Greece
  AssignClass (6843065d-d3a1-4dee-97cd-a639bedaa736)
 Call ID: 6843065d-d3a1-4dee-97cd-a639bedaa736
  Args:
    type: :Person
    source: Frederica_of_Hanover
  AssignClass (947a6f7d-516b-4d8e-9372-df503aaa4dd1)
 Call ID: 947a6f7d-516b-4d8e-9372-df503aaa4dd1
  Args:
    type: :Woman
    source: Frederica_of_Hanover
  AddTriple (9db3bf60-2bbb-495d-a1b7-e2a19c45ccc7)
 Call ID: 9db3bf60-2bbb-495d-a1b7-e2a19c45ccc7
  Args:
    target: Paul_of_Greece
    relation: :hasFather
    source: Constantine_II_of_Greece
  AddTriple (01fe3b65-9f89-4a20-a929-8b15eae37136)
 Call ID: 01fe3b65-9f89-4a20-a929-8b15eae37136
  Args:
    relation: :hasMother
    source: Constantine_II_of_Greece
    target: Frederica_of_Hanover
  AssignClass (0c6e61d1-47ec-40a9-be90-07e1e6fd9a5a)
 Call ID: 0c6e61d1-47ec-40a9-be90-07e1e6fd9a5a
  Args:
    type: :Person
    source: Frederik_IX_of_Denmark
  AssignClass (806ea5af-2108-418b-a84a-993ae271263c)
 Call ID: 806ea5af-2108-418b-a84a-993ae271263c
  Args:
    type: :Man
    source: Frederik_IX_of_Denmark
  AssignClass (add89808-eddb-43aa-834a-42fc46f46dde)
 Call ID: add89808-eddb-43aa-834a-42fc46f46dde
  Args:
    type: :Person
    source: Ingrid_of_Sweden
  AssignClass (2d559a2f-0f43-464b-b993-a82b7ad526d4)
 Call ID: 2d559a2f-0f43-464b-b993-a82b7ad526d4
  Args:
    type: :Woman
    source: Ingrid_of_Sweden
  AddTriple (98ab694c-2621-4895-9bbd-d39dd6df87cb)
 Call ID: 98ab694c-2621-4895-9bbd-d39dd6df87cb
  Args:
    target: Frederik_IX_of_Denmark
    relation: :hasFather
    source: Anne-Marie_of_Greece
  AddTriple (1b48b5a0-5386-472e-9dee-79b1194393f0)
 Call ID: 1b48b5a0-5386-472e-9dee-79b1194393f0
  Args:
    relation: :hasMother
    source: Anne-Marie_of_Greece
    target: Ingrid_of_Sweden
  Finish (5f1fb5a6-1360-41f6-b68f-c635b6402068)
 Call ID: 5f1fb5a6-1360-41f6-b68f-c635b6402068
  Args: