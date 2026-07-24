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


Princess Alexandra Elli Francisca Maria of Greece (born 15 October 1968), known professionally as Alexandra Mirzayantz, is a Greek artist, art collector, arts patron, and child life specialist.
As the daughter of Prince Michael of Greece and Denmark, she is a member of the Greek royal family and a relative of the Danish royal family.
A morganatic descendant of the House of Glücksburg, she is not a Danish princess nor is she entitled to the style Royal Highness as other members of the Greek royal family are.
She was born a princess of Greece entitled to the style Your Highness, and was excluded from the line of succession to the Greek throne.
She is a second cousin of Constantine II of Greece, who reigned as King of the Hellenes until the monarchy was abolished in 1973.
Early life and family

Princess Alexandra was born in Athens on 15 October 1968.
She is the daughter of the historian Prince Michael of Greece and Denmark and the artist Marina Karella.
She is the older sister of Princess Olga.
She is a great-granddaughter of George I of Greece and Olga Constantinovna of Russia.
She is also a great-granddaughter of Prince Jean, Duke of Guise and a great-great-granddaughter of Christian IX of Denmark.
As Princess Alexandra's parents' marriage is morganatic, and therefore non-dynastic, she is a Greek princess by birth but not a Danish princess, uses the style Your Highness instead of Her Royal Highness, and is excluded from the line of succession to the former Greek throne.
On 29 July 1973, Princess Alexandra's second cousin, Constantine II of Greece, was deposed and the Greek monarchy was abolished.
Career

Princess Alexandra is a certified child life specialist.
Princess Alexandra and her husband are patrons of the New York art scene.
She owns a portrait of her grandfather, Prince Christopher of Greece and Denmark, painted by Philip de László in 1919, as part of her collection.
Personal life

Princess Alexandra married the perfumer Nicolas Mirzayantz on 27 June 1998 in Torcello.
She attended the funeral of her father, Prince Michael on 1 August 2024, and was seen with other Greek royal family members, including Princess Olga, Queen Anne-Marie of Greece, Queen Sofía of Spain, and Crown Prince Pavlos.



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
  AssignClass (0375238b-3d4d-4f12-9905-64d6a4f6996f)
 Call ID: 0375238b-3d4d-4f12-9905-64d6a4f6996f
  Args:
    source: Alexandra_Mirzayantz
    type: :Person
  AssignClass (a9ee685e-6a19-438f-a399-237d8d1cf0db)
 Call ID: a9ee685e-6a19-438f-a399-237d8d1cf0db
  Args:
    type: :Woman
    source: Alexandra_Mirzayantz
  AddLiteral (48f3dfef-e239-42eb-a312-1aeccdbff689)
 Call ID: 48f3dfef-e239-42eb-a312-1aeccdbff689
  Args:
    literal_value: Alexandra Mirzayantz
    source: Alexandra_Mirzayantz
    literal_type: xsd:string
    relation: :knownAs
  AddLiteral (815dd862-f5b9-4e8a-afc1-f68cd552f4b2)
 Call ID: 815dd862-f5b9-4e8a-afc1-f68cd552f4b2
  Args:
    relation: :alsoKnownAs
    literal_type: xsd:string
    literal_value: Princess Alexandra Elli Francisca Maria of Greece
    source: Alexandra_Mirzayantz
  AddLiteral (42537da7-0366-4f72-bc31-53a1cd113f54)
 Call ID: 42537da7-0366-4f72-bc31-53a1cd113f54
  Args:
    literal_value: 1968
    source: Alexandra_Mirzayantz
    relation: :hasBirthYear
    literal_type: xsd:integer
  AssignClass (02e676c1-00f9-4ccd-be45-5afb66452e8b)
 Call ID: 02e676c1-00f9-4ccd-be45-5afb66452e8b
  Args:
    type: :Person
    source: Prince_Michael_of_Greece_and_Denmark
  AssignClass (b489e130-0ccb-43e1-af85-c1607c9a64b7)
 Call ID: b489e130-0ccb-43e1-af85-c1607c9a64b7
  Args:
    source: Prince_Michael_of_Greece_and_Denmark
    type: :Man
  AddTriple (6278802c-cdef-434e-b43f-5ef9f8fa7bf0)
 Call ID: 6278802c-cdef-434e-b43f-5ef9f8fa7bf0
  Args:
    target: Prince_Michael_of_Greece_and_Denmark
    source: Alexandra_Mirzayantz
    relation: :hasFather
  AssignClass (32f412cf-b28e-452c-ab2e-460ee0a7ece9)
 Call ID: 32f412cf-b28e-452c-ab2e-460ee0a7ece9
  Args:
    source: Marina_Karella
    type: :Person
  AssignClass (8db53b7d-43c0-4050-b6f7-8b383497d619)
 Call ID: 8db53b7d-43c0-4050-b6f7-8b383497d619
  Args:
    source: Marina_Karella
    type: :Woman
  AddTriple (2997dc87-30fa-40c5-81e9-3740b914f4f6)
 Call ID: 2997dc87-30fa-40c5-81e9-3740b914f4f6
  Args:
    relation: :hasMother
    target: Marina_Karella
    source: Alexandra_Mirzayantz
  AssignClass (6d78b63e-2e6b-4e48-924e-151abf4d1526)
 Call ID: 6d78b63e-2e6b-4e48-924e-151abf4d1526
  Args:
    source: Princess_Olga
    type: :Person
  AssignClass (99e4214f-d271-4f09-9b3a-0a735700592c)
 Call ID: 99e4214f-d271-4f09-9b3a-0a735700592c
  Args:
    source: Princess_Olga
    type: :Woman
  AddTriple (6f62ebb5-119c-43f9-8460-778ee0d5da52)
 Call ID: 6f62ebb5-119c-43f9-8460-778ee0d5da52
  Args:
    relation: :hasSister
    target: Princess_Olga
    source: Alexandra_Mirzayantz
  AssignClass (f520537a-7172-485e-a5f8-fe938363a5e0)
 Call ID: f520537a-7172-485e-a5f8-fe938363a5e0
  Args:
    source: Nicolas_Mirzayantz
    type: :Person
  AssignClass (0fb6d9ab-6ca3-43b1-8175-18bc5ec6112a)
 Call ID: 0fb6d9ab-6ca3-43b1-8175-18bc5ec6112a
  Args:
    source: Nicolas_Mirzayantz
    type: :Man
  AddTriple (82a5e4c4-128e-4df9-b835-5eab36dbee1a)
 Call ID: 82a5e4c4-128e-4df9-b835-5eab36dbee1a
  Args:
    relation: :hasRelation
    source: Alexandra_Mirzayantz
    target: Nicolas_Mirzayantz
  AddLiteral (6738f616-ed8b-4d51-b425-e709e6a82354)
 Call ID: 6738f616-ed8b-4d51-b425-e709e6a82354
  Args:
    relation: :hasMarriageYear
    literal_type: xsd:integer
    literal_value: 1998
    source: Alexandra_Mirzayantz
  AssignClass (8b6fa18e-4cc1-4e9c-bd57-8403a76637ec)
 Call ID: 8b6fa18e-4cc1-4e9c-bd57-8403a76637ec
  Args:
    type: :Ancestor
    source: George_I_of_Greece
  AssignClass (709e623d-7f5f-4a5b-be5b-7a90693887b5)
 Call ID: 709e623d-7f5f-4a5b-be5b-7a90693887b5
  Args:
    type: :Ancestor
    source: Olga_Constantinovna_of_Russia
  AssignClass (bb133c36-1084-42b3-aca4-503c3645a30b)
 Call ID: bb133c36-1084-42b3-aca4-503c3645a30b
  Args:
    source: Prince_Jean_Duke_of_Guise
    type: :Ancestor
  AssignClass (3c97b5cc-d8e2-43ea-9467-02ba72d0b444)
 Call ID: 3c97b5cc-d8e2-43ea-9467-02ba72d0b444
  Args:
    source: Christian_IX_of_Denmark
    type: :Ancestor
  AssignClass (ef103a5a-0276-4187-8f61-16959f287e16)
 Call ID: ef103a5a-0276-4187-8f61-16959f287e16
  Args:
    source: Prince_Christopher_of_Greece_and_Denmark
    type: :Ancestor
  AddTriple (a93f5e78-fd16-4077-aba8-bd43f9f9a330)
 Call ID: a93f5e78-fd16-4077-aba8-bd43f9f9a330
  Args:
    target: George_I_of_Greece
    source: Alexandra_Mirzayantz
    relation: :hasAncestor
  AddTriple (4405ca69-7663-4dc0-8d9a-f1e14899deb4)
 Call ID: 4405ca69-7663-4dc0-8d9a-f1e14899deb4
  Args:
    relation: :hasAncestor
    source: Alexandra_Mirzayantz
    target: Olga_Constantinovna_of_Russia
  AddTriple (91ca46fd-41b0-431a-a788-0f96423a364a)
 Call ID: 91ca46fd-41b0-431a-a788-0f96423a364a
  Args:
    source: Alexandra_Mirzayantz
    target: Prince_Jean_Duke_of_Guise
    relation: :hasAncestor
  AddTriple (ace3570d-2336-4b85-8d6b-ee4e49b852f2)
 Call ID: ace3570d-2336-4b85-8d6b-ee4e49b852f2
  Args:
    source: Alexandra_Mirzayantz
    target: Christian_IX_of_Denmark
    relation: :hasAncestor
  AddTriple (43f58ed3-7745-4aac-a35d-53f8c6967f99)
 Call ID: 43f58ed3-7745-4aac-a35d-53f8c6967f99
  Args:
    source: Alexandra_Mirzayantz
    target: Prince_Christopher_of_Greece_and_Denmark
    relation: :hasAncestor
  AssignClass (0b1d666f-1ae7-4f25-976a-885f5b0d699e)
 Call ID: 0b1d666f-1ae7-4f25-976a-885f5b0d699e
  Args:
    source: Constantine_II_of_Greece
    type: :Person
  AssignClass (6b44f509-673b-415b-8d27-c72318edb9cf)
 Call ID: 6b44f509-673b-415b-8d27-c72318edb9cf
  Args:
    type: :Person
    source: Queen_Anne_Marie_of_Greece
  AssignClass (7daf7d8a-0e68-416a-98fa-6b1bac59c5f4)
 Call ID: 7daf7d8a-0e68-416a-98fa-6b1bac59c5f4
  Args:
    source: Queen_Sofia_of_Spain
    type: :Person
  AssignClass (2660e644-6327-4aea-ac48-d2ac739a30c2)
 Call ID: 2660e644-6327-4aea-ac48-d2ac739a30c2
  Args:
    type: :Person
    source: Crown_Prince_Pavlos
  Finish (e6f2dc17-8306-4f13-961c-da47583310cf)
 Call ID: e6f2dc17-8306-4f13-961c-da47583310cf
  Args: