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
  AssignClass (9ba02cf3-b509-4d01-8bd6-95d5aa6cbb97)
 Call ID: 9ba02cf3-b509-4d01-8bd6-95d5aa6cbb97
  Args:
    source: Alexandra_Mirzayantz
    type: :Woman
  AssignClass (ee6e1997-e94d-41e2-b46e-3aa3fce99d12)
 Call ID: ee6e1997-e94d-41e2-b46e-3aa3fce99d12
  Args:
    type: :Person
    source: Alexandra_Mirzayantz
  AddLiteral (35c9b0c1-dd41-46b2-997f-b12680127d84)
 Call ID: 35c9b0c1-dd41-46b2-997f-b12680127d84
  Args:
    literal_type: xsd:string
    source: Alexandra_Mirzayantz
    relation: :knownAs
    literal_value: Alexandra Mirzayantz
  AddLiteral (3f0763e8-59a3-4394-b930-f9f04db56920)
 Call ID: 3f0763e8-59a3-4394-b930-f9f04db56920
  Args:
    literal_value: 1968
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Alexandra_Mirzayantz
  AssignClass (fa611851-f678-4a16-9078-cd1fe6ed0bd5)
 Call ID: fa611851-f678-4a16-9078-cd1fe6ed0bd5
  Args:
    source: Prince_Michael_of_Greece_and_Denmark
    type: :Man
  AssignClass (5ffd0bb2-0d75-40d8-883a-2ef49659839e)
 Call ID: 5ffd0bb2-0d75-40d8-883a-2ef49659839e
  Args:
    type: :Person
    source: Prince_Michael_of_Greece_and_Denmark
  AssignClass (e31217e8-84a7-4824-8e65-7965135d7f0e)
 Call ID: e31217e8-84a7-4824-8e65-7965135d7f0e
  Args:
    source: Marina_Karella
    type: :Woman
  AssignClass (e1ea8f8b-db13-4d53-89a4-56ab87f82f45)
 Call ID: e1ea8f8b-db13-4d53-89a4-56ab87f82f45
  Args:
    type: :Person
    source: Marina_Karella
  AddTriple (8516f3ff-cffb-4b35-b8c2-46ee10d10987)
 Call ID: 8516f3ff-cffb-4b35-b8c2-46ee10d10987
  Args:
    source: Alexandra_Mirzayantz
    target: Prince_Michael_of_Greece_and_Denmark
    relation: :hasFather
  AddTriple (71e1ac86-c52e-4bef-a548-e9e66be6371f)
 Call ID: 71e1ac86-c52e-4bef-a548-e9e66be6371f
  Args:
    source: Alexandra_Mirzayantz
    target: Marina_Karella
    relation: :hasMother
  AssignClass (3e6e0c44-52d9-4a29-a8cc-701cc2ec2c5b)
 Call ID: 3e6e0c44-52d9-4a29-a8cc-701cc2ec2c5b
  Args:
    type: :Woman
    source: Princess_Olga
  AssignClass (4d08936d-3867-4961-9fd0-f589820f8ce3)
 Call ID: 4d08936d-3867-4961-9fd0-f589820f8ce3
  Args:
    type: :Person
    source: Princess_Olga
  AddTriple (3728b44c-5ba3-4e03-94f4-584af3cdcdf7)
 Call ID: 3728b44c-5ba3-4e03-94f4-584af3cdcdf7
  Args:
    relation: :hasSister
    source: Alexandra_Mirzayantz
    target: Princess_Olga
  AssignClass (8e0d777e-4c50-4d0f-998f-2abd23d22faf)
 Call ID: 8e0d777e-4c50-4d0f-998f-2abd23d22faf
  Args:
    source: George_I_of_Greece
    type: :Man
  AssignClass (70b6fc47-263c-47b7-abdf-e937e25e23b4)
 Call ID: 70b6fc47-263c-47b7-abdf-e937e25e23b4
  Args:
    type: :Person
    source: George_I_of_Greece
  AssignClass (41d49db3-4770-4442-88db-a01ff24ff4aa)
 Call ID: 41d49db3-4770-4442-88db-a01ff24ff4aa
  Args:
    source: Olga_Constantinovna_of_Russia
    type: :Woman
  AssignClass (dfc14389-d198-4fbf-acb4-5d08cefb6967)
 Call ID: dfc14389-d198-4fbf-acb4-5d08cefb6967
  Args:
    type: :Person
    source: Olga_Constantinovna_of_Russia
  AddTriple (de9e2665-537b-4800-86be-d989fda6e975)
 Call ID: de9e2665-537b-4800-86be-d989fda6e975
  Args:
    source: Alexandra_Mirzayantz
    target: George_I_of_Greece
    relation: :hasAncestor
  AddTriple (7d2ca012-86b8-41dd-9feb-52a14f68af4d)
 Call ID: 7d2ca012-86b8-41dd-9feb-52a14f68af4d
  Args:
    relation: :hasAncestor
    source: Alexandra_Mirzayantz
    target: Olga_Constantinovna_of_Russia
  AssignClass (42f731dc-d8f9-4d2a-9439-72f9117ccb96)
 Call ID: 42f731dc-d8f9-4d2a-9439-72f9117ccb96
  Args:
    source: Prince_Jean_Duke_of_Guise
    type: :Man
  AssignClass (87957376-7894-49d9-8d0c-96c95d1898ad)
 Call ID: 87957376-7894-49d9-8d0c-96c95d1898ad
  Args:
    source: Prince_Jean_Duke_of_Guise
    type: :Person
  AddTriple (7dc2e07e-0e21-47e8-b7ff-60ddd888b1b4)
 Call ID: 7dc2e07e-0e21-47e8-b7ff-60ddd888b1b4
  Args:
    relation: :hasAncestor
    source: Alexandra_Mirzayantz
    target: Prince_Jean_Duke_of_Guise
  AssignClass (215bd5d7-3488-47e6-ac03-dadadd0a731f)
 Call ID: 215bd5d7-3488-47e6-ac03-dadadd0a731f
  Args:
    source: Christian_IX_of_Denmark
    type: :Man
  AssignClass (26aecd15-328b-450c-966c-b6bc5e96b238)
 Call ID: 26aecd15-328b-450c-966c-b6bc5e96b238
  Args:
    type: :Person
    source: Christian_IX_of_Denmark
  AddTriple (8823fc12-dd92-483c-a834-29d985a50765)
 Call ID: 8823fc12-dd92-483c-a834-29d985a50765
  Args:
    relation: :hasAncestor
    source: Alexandra_Mirzayantz
    target: Christian_IX_of_Denmark
  AssignClass (33be031b-be3c-410f-8910-78838300a891)
 Call ID: 33be031b-be3c-410f-8910-78838300a891
  Args:
    source: Prince_Christopher_of_Greece_and_Denmark
    type: :Man
  AssignClass (ba42c783-01d5-49c4-9437-55d35c5e9201)
 Call ID: ba42c783-01d5-49c4-9437-55d35c5e9201
  Args:
    source: Prince_Christopher_of_Greece_and_Denmark
    type: :Person
  AddTriple (c2981aad-806c-4c01-a0fe-c5abdc25ec9e)
 Call ID: c2981aad-806c-4c01-a0fe-c5abdc25ec9e
  Args:
    source: Alexandra_Mirzayantz
    target: Prince_Christopher_of_Greece_and_Denmark
    relation: :hasAncestor
  AssignClass (c928264d-3731-4fdb-af72-48df6c904974)
 Call ID: c928264d-3731-4fdb-af72-48df6c904974
  Args:
    type: :Man
    source: Nicolas_Mirzayantz
  AssignClass (65db9f21-08ba-4fd3-81fa-40e478407f0a)
 Call ID: 65db9f21-08ba-4fd3-81fa-40e478407f0a
  Args:
    source: Nicolas_Mirzayantz
    type: :Person
  AddTriple (fa2f6284-af04-4f6d-8d05-fbf6c87190a4)
 Call ID: fa2f6284-af04-4f6d-8d05-fbf6c87190a4
  Args:
    source: Alexandra_Mirzayantz
    target: Nicolas_Mirzayantz
    relation: :hasRelation
  AddLiteral (3c22060d-0f4d-4a20-81b7-ff91be25fe7a)
 Call ID: 3c22060d-0f4d-4a20-81b7-ff91be25fe7a
  Args:
    literal_value: 1998
    literal_type: xsd:integer
    source: Alexandra_Mirzayantz
    relation: :hasMarriageYear
  AssignClass (11f7c8aa-a35c-4855-8c37-c22d77a90d9d)
 Call ID: 11f7c8aa-a35c-4855-8c37-c22d77a90d9d
  Args:
    source: Constantine_II_of_Greece
    type: :Man
  AssignClass (1618c6db-efae-4372-a5a2-327f141bfc71)
 Call ID: 1618c6db-efae-4372-a5a2-327f141bfc71
  Args:
    type: :Person
    source: Constantine_II_of_Greece
  AssignClass (660c1466-9897-45fe-b601-5fcfaaf0f5da)
 Call ID: 660c1466-9897-45fe-b601-5fcfaaf0f5da
  Args:
    type: :Woman
    source: Queen_Anne-Marie_of_Greece
  AssignClass (d0622af4-25f8-437e-94a2-0955df069416)
 Call ID: d0622af4-25f8-437e-94a2-0955df069416
  Args:
    type: :Person
    source: Queen_Anne-Marie_of_Greece
  AssignClass (5d65389b-a95f-4559-b22b-c7317ff78215)
 Call ID: 5d65389b-a95f-4559-b22b-c7317ff78215
  Args:
    source: Queen_Sofia_of_Spain
    type: :Woman
  AssignClass (0cb7738b-e4b6-4b7e-a7c3-76c145ec9e73)
 Call ID: 0cb7738b-e4b6-4b7e-a7c3-76c145ec9e73
  Args:
    source: Queen_Sofia_of_Spain
    type: :Person
  AssignClass (095b92ed-79bf-4b22-90eb-55df79e84bcb)
 Call ID: 095b92ed-79bf-4b22-90eb-55df79e84bcb
  Args:
    type: :Man
    source: Crown_Prince_Pavlos
  AssignClass (85e6df3c-44ec-45a0-b232-d204bf15eb74)
 Call ID: 85e6df3c-44ec-45a0-b232-d204bf15eb74
  Args:
    type: :Person
    source: Crown_Prince_Pavlos
  Finish (865a0219-f823-4c8c-8e9b-f7e732746dcc)
 Call ID: 865a0219-f823-4c8c-8e9b-f7e732746dcc
  Args: