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
  AssignClass (32f7d1f4-e801-4090-b800-1b671c9a47db)
 Call ID: 32f7d1f4-e801-4090-b800-1b671c9a47db
  Args:
    source: Alexandra_Mirzayantz
    type: :Woman
  AssignClass (22c7b67b-71ba-4ac7-9c52-2044a6c3b13d)
 Call ID: 22c7b67b-71ba-4ac7-9c52-2044a6c3b13d
  Args:
    type: :Person
    source: Alexandra_Mirzayantz
  AddLiteral (77ca6fee-9e5b-4cbf-adb0-f1b57a2cbf04)
 Call ID: 77ca6fee-9e5b-4cbf-adb0-f1b57a2cbf04
  Args:
    source: Alexandra_Mirzayantz
    literal_type: xsd:string
    literal_value: Alexandra Mirzayantz
    relation: :knownAs
  AddLiteral (af853b6c-9afa-482f-a253-2b37a1803313)
 Call ID: af853b6c-9afa-482f-a253-2b37a1803313
  Args:
    literal_type: xsd:integer
    source: Alexandra_Mirzayantz
    relation: :hasBirthYear
    literal_value: 1968
  AssignClass (f376cc05-f779-4ace-a631-afd1251ad012)
 Call ID: f376cc05-f779-4ace-a631-afd1251ad012
  Args:
    type: :Man
    source: Prince_Michael_of_Greece_and_Denmark
  AssignClass (cf2fadac-2d98-4fb9-9a12-322a7ced5cfe)
 Call ID: cf2fadac-2d98-4fb9-9a12-322a7ced5cfe
  Args:
    type: :Person
    source: Prince_Michael_of_Greece_and_Denmark
  AssignClass (d5b2cdc0-7b81-447d-b21e-e3aff68bc08c)
 Call ID: d5b2cdc0-7b81-447d-b21e-e3aff68bc08c
  Args:
    source: Marina_Karella
    type: :Woman
  AssignClass (4a7d80b7-e918-480a-bc50-1325dfc4e872)
 Call ID: 4a7d80b7-e918-480a-bc50-1325dfc4e872
  Args:
    source: Marina_Karella
    type: :Person
  AddTriple (3c4b3116-f719-49c5-9ed3-caee94d14f9f)
 Call ID: 3c4b3116-f719-49c5-9ed3-caee94d14f9f
  Args:
    relation: :hasFather
    target: Prince_Michael_of_Greece_and_Denmark
    source: Alexandra_Mirzayantz
  AddTriple (591a8930-0993-4fe1-99d2-b4d3e0d241a2)
 Call ID: 591a8930-0993-4fe1-99d2-b4d3e0d241a2
  Args:
    source: Alexandra_Mirzayantz
    target: Marina_Karella
    relation: :hasMother
  AssignClass (5d555e05-7169-42b5-af57-bce3af48ec38)
 Call ID: 5d555e05-7169-42b5-af57-bce3af48ec38
  Args:
    type: :Woman
    source: Princess_Olga
  AssignClass (d14be36e-1026-4060-bb21-1eac79e382ff)
 Call ID: d14be36e-1026-4060-bb21-1eac79e382ff
  Args:
    source: Princess_Olga
    type: :Person
  AddTriple (7c2a3631-9906-4726-8fd1-e1cb629a6c6d)
 Call ID: 7c2a3631-9906-4726-8fd1-e1cb629a6c6d
  Args:
    relation: :isSisterOf
    source: Alexandra_Mirzayantz
    target: Princess_Olga
  AssignClass (6644e330-daac-42f5-9206-0ddaaa9873e2)
 Call ID: 6644e330-daac-42f5-9206-0ddaaa9873e2
  Args:
    type: :Man
    source: Nicolas_Mirzayantz
  AssignClass (7a1e8523-a2f0-421b-a69d-37c91680458a)
 Call ID: 7a1e8523-a2f0-421b-a69d-37c91680458a
  Args:
    source: Nicolas_Mirzayantz
    type: :Person
  AddLiteral (18d2a266-3406-489c-8212-671258ed7454)
 Call ID: 18d2a266-3406-489c-8212-671258ed7454
  Args:
    source: Alexandra_Mirzayantz
    literal_type: xsd:integer
    literal_value: 1998
    relation: :hasMarriageYear
  AddTriple (0008be78-9fd8-4ebe-b372-10d81722d141)
 Call ID: 0008be78-9fd8-4ebe-b372-10d81722d141
  Args:
    source: Alexandra_Mirzayantz
    target: Nicolas_Mirzayantz
    relation: :hasRelation
  AssignClass (b9e8b207-289f-4127-bcd1-835747a3d492)
 Call ID: b9e8b207-289f-4127-bcd1-835747a3d492
  Args:
    source: George_I_of_Greece
    type: :Man
  AssignClass (9a3f7b0a-236b-46ee-adae-7ddf465f69ce)
 Call ID: 9a3f7b0a-236b-46ee-adae-7ddf465f69ce
  Args:
    type: :Person
    source: George_I_of_Greece
  AssignClass (2fd14129-8fe6-40a9-8af4-81284fa25fe5)
 Call ID: 2fd14129-8fe6-40a9-8af4-81284fa25fe5
  Args:
    source: Olga_Constantinovna_of_Russia
    type: :Woman
  AssignClass (2c2806e0-d60f-49bb-bcba-8ddf4617b1d0)
 Call ID: 2c2806e0-d60f-49bb-bcba-8ddf4617b1d0
  Args:
    source: Olga_Constantinovna_of_Russia
    type: :Person
  AssignClass (600a43f7-b416-4a0c-ba5f-ac82eb3d5355)
 Call ID: 600a43f7-b416-4a0c-ba5f-ac82eb3d5355
  Args:
    type: :Man
    source: Prince_Jean_Duke_of_Guise
  AssignClass (f1b1134e-f221-4904-ae24-b3cc6af4f672)
 Call ID: f1b1134e-f221-4904-ae24-b3cc6af4f672
  Args:
    type: :Person
    source: Prince_Jean_Duke_of_Guise
  AssignClass (a7b6f9a3-b230-416b-8080-663b760595f3)
 Call ID: a7b6f9a3-b230-416b-8080-663b760595f3
  Args:
    source: Christian_IX_of_Denmark
    type: :Man
  AssignClass (c901f6c4-7422-4ee9-bcfb-a15abf6cc868)
 Call ID: c901f6c4-7422-4ee9-bcfb-a15abf6cc868
  Args:
    source: Christian_IX_of_Denmark
    type: :Person
  AddTriple (b391bd57-9650-40ca-9f7a-efbd49fc0271)
 Call ID: b391bd57-9650-40ca-9f7a-efbd49fc0271
  Args:
    target: George_I_of_Greece
    source: Alexandra_Mirzayantz
    relation: :hasAncestor
  AddTriple (62a3450d-9739-42ca-967e-fc345b857d55)
 Call ID: 62a3450d-9739-42ca-967e-fc345b857d55
  Args:
    target: Olga_Constantinovna_of_Russia
    source: Alexandra_Mirzayantz
    relation: :hasAncestor
  AddTriple (89c4c4ec-c7b6-4907-a67f-a0314c6155c7)
 Call ID: 89c4c4ec-c7b6-4907-a67f-a0314c6155c7
  Args:
    source: Alexandra_Mirzayantz
    target: Prince_Jean_Duke_of_Guise
    relation: :hasAncestor
  AddTriple (191d5b2a-2377-4c92-acce-2c7312125967)
 Call ID: 191d5b2a-2377-4c92-acce-2c7312125967
  Args:
    relation: :hasAncestor
    target: Christian_IX_of_Denmark
    source: Alexandra_Mirzayantz
  AssignClass (4b2d4532-b43d-44a5-b8fd-0dc99f84dc47)
 Call ID: 4b2d4532-b43d-44a5-b8fd-0dc99f84dc47
  Args:
    type: :Man
    source: Prince_Christopher_of_Greece_and_Denmark
  AssignClass (906f2e66-57d2-4995-b04a-07e1899d7141)
 Call ID: 906f2e66-57d2-4995-b04a-07e1899d7141
  Args:
    source: Prince_Christopher_of_Greece_and_Denmark
    type: :Person
  AddTriple (33e5d808-76df-4e3c-badd-640a1b4b3188)
 Call ID: 33e5d808-76df-4e3c-badd-640a1b4b3188
  Args:
    target: Prince_Michael_of_Greece_and_Denmark
    source: Alexandra_Mirzayantz
    relation: :hasFather
  AddTriple (9b4a7b4b-a1e0-4ea7-9363-1d405e21de3e)
 Call ID: 9b4a7b4b-a1e0-4ea7-9363-1d405e21de3e
  Args:
    relation: :hasFather
    source: Prince_Michael_of_Greece_and_Denmark
    target: Prince_Christopher_of_Greece_and_Denmark
  AssignClass (5d63762a-eeca-451d-8115-59220c31a9cc)
 Call ID: 5d63762a-eeca-451d-8115-59220c31a9cc
  Args:
    type: :Man
    source: Constantine_II_of_Greece
  AssignClass (64bff451-732c-494b-a6cc-e625a899f471)
 Call ID: 64bff451-732c-494b-a6cc-e625a899f471
  Args:
    source: Constantine_II_of_Greece
    type: :Person
  AssignClass (17691195-6148-4da1-8a22-5e30fcb2bc79)
 Call ID: 17691195-6148-4da1-8a22-5e30fcb2bc79
  Args:
    source: Queen_Anne-Marie
    type: :Woman
  AssignClass (4134cbdc-fad5-4c28-90e6-9be7debdc512)
 Call ID: 4134cbdc-fad5-4c28-90e6-9be7debdc512
  Args:
    type: :Person
    source: Queen_Anne-Marie
  AssignClass (4e5d7639-b1fd-4860-ab83-35d85f5929f8)
 Call ID: 4e5d7639-b1fd-4860-ab83-35d85f5929f8
  Args:
    source: Queen_Sofia_of_Spain
    type: :Woman
  AssignClass (1031a4c0-d4f8-4040-8d80-f665175ffab8)
 Call ID: 1031a4c0-d4f8-4040-8d80-f665175ffab8
  Args:
    source: Queen_Sofia_of_Spain
    type: :Person
  AssignClass (033a749f-8139-43c7-8fab-b5ec835b7f6d)
 Call ID: 033a749f-8139-43c7-8fab-b5ec835b7f6d
  Args:
    type: :Man
    source: Crown_Prince_Pavlos
  AssignClass (232a2091-4222-44b8-b1da-58069055e2f1)
 Call ID: 232a2091-4222-44b8-b1da-58069055e2f1
  Args:
    source: Crown_Prince_Pavlos
    type: :Person
  Finish (8cf5fa58-39ac-4d54-b0d2-b83229152009)
 Call ID: 8cf5fa58-39ac-4d54-b0d2-b83229152009
  Args: