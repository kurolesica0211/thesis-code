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
Granville James Leveson-Gower, 5th Earl Granville MC (6 December 1918 – 31 October 1996) was a British soldier, banker, peer, and landowner, a member of the House of Lords from 1953 until his death.
Early life

The son of Vice-Admiral William Leveson-Gower, 4th Earl Granville, and his wife Lady Rose Bowes-Lyon, a daughter of Claude Bowes-Lyon, 14th
Earl of Strathmore and Kinghorne, he was educated at Eton College.
Known formally as Lord Leveson until 1953, he was commissioned into the Coldstream Guards and saw active service during the Second World War, in which he was twice wounded and mentioned in despatches.
Later career

After the war, Lord Leveson joined Coutts & Co., a private bank.
On 25 June 1953, he succeeded his father as Earl Granville (created 1833), Viscount Granville (1814), and Baron Leveson of Stone (1814), giving him a seat in the House of Lords.
In 1958, Granville married Doon Aileen Plunket, daughter of Brindsley Sheridan Bushe Plunket and granddaughter of William Plunket, 5th Baron Plunket.
Her mother was Aileen Sibell Mary Guinness, a granddaughter of Edward Guinness, 1st Earl of Iveagh.
In 1960, shortly after the birth of his first child, Granville bought the island of North Uist in the Outer Hebrides from the Duke of Hamilton, becoming its laird.
In 1974 Granville was appointed as a Deputy Lieutenant of Inverness-shire and was Vice-Lord-Lieutenant of the Western Isles between January 1976 and 1983, then Lord-Lieutenant from 1983 to December 1993, when he was succeeded by Viscount Dunrossil.



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
  AssignClass (ab3df404-751b-4175-8e58-24e752a383a6)
 Call ID: ab3df404-751b-4175-8e58-24e752a383a6
  Args:
    type: :Man
    source: Granville_James_Leveson-Gower
  AssignClass (c2cff209-08c1-4d87-b7c6-83f5811f7e7f)
 Call ID: c2cff209-08c1-4d87-b7c6-83f5811f7e7f
  Args:
    type: :Person
    source: Granville_James_Leveson-Gower
  AddLiteral (ac4f5627-00da-4baa-bafe-50eb7dbd9220)
 Call ID: ac4f5627-00da-4baa-bafe-50eb7dbd9220
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1918
    source: Granville_James_Leveson-Gower
  AddLiteral (82205e62-8f15-49c4-8930-daaf78ecd318)
 Call ID: 82205e62-8f15-49c4-8930-daaf78ecd318
  Args:
    source: Granville_James_Leveson-Gower
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1996
  AssignClass (5faba57e-1e98-463c-b81c-acf302dc79ce)
 Call ID: 5faba57e-1e98-463c-b81c-acf302dc79ce
  Args:
    type: :Man
    source: William_Leveson-Gower
  AssignClass (76f9c0c0-c952-4d65-a99f-ff058622f6c9)
 Call ID: 76f9c0c0-c952-4d65-a99f-ff058622f6c9
  Args:
    type: :Person
    source: William_Leveson-Gower
  AddTriple (48634f89-f958-4eef-8de2-250a6d1d2dab)
 Call ID: 48634f89-f958-4eef-8de2-250a6d1d2dab
  Args:
    relation: :hasFather
    source: Granville_James_Leveson-Gower
    target: William_Leveson-Gower
  AssignClass (302ec172-3394-471d-aace-7b179a616168)
 Call ID: 302ec172-3394-471d-aace-7b179a616168
  Args:
    type: :Woman
    source: Lady_Rose_Bowes-Lyon
  AssignClass (23424966-c47c-4d86-afe4-ac80a08e1ca8)
 Call ID: 23424966-c47c-4d86-afe4-ac80a08e1ca8
  Args:
    type: :Person
    source: Lady_Rose_Bowes-Lyon
  AddTriple (cd0302f9-4355-4f48-9618-386a15960661)
 Call ID: cd0302f9-4355-4f48-9618-386a15960661
  Args:
    source: Granville_James_Leveson-Gower
    target: Lady_Rose_Bowes-Lyon
    relation: :hasMother
  AssignClass (34876427-3b6a-487e-813e-e00ee5bdf60b)
 Call ID: 34876427-3b6a-487e-813e-e00ee5bdf60b
  Args:
    type: :Man
    source: Claude_Bowes-Lyon
  AssignClass (42c59267-59de-451a-80d7-f096200bc4d6)
 Call ID: 42c59267-59de-451a-80d7-f096200bc4d6
  Args:
    type: :Person
    source: Claude_Bowes-Lyon
  AddTriple (0f2f75b4-1575-422f-9948-59d1bf782524)
 Call ID: 0f2f75b4-1575-422f-9948-59d1bf782524
  Args:
    source: Lady_Rose_Bowes-Lyon
    target: Claude_Bowes-Lyon
    relation: :hasFather
  AssignClass (de5160fe-3c53-47b7-aa25-6d569a6ff587)
 Call ID: de5160fe-3c53-47b7-aa25-6d569a6ff587
  Args:
    type: :Woman
    source: Doon_Aileen_Plunket
  AssignClass (95999bea-f83c-4982-b8c7-feeb1f8890e5)
 Call ID: 95999bea-f83c-4982-b8c7-feeb1f8890e5
  Args:
    type: :Person
    source: Doon_Aileen_Plunket
  AddLiteral (68f7bf12-9ffb-46ea-8787-8f65f74a854a)
 Call ID: 68f7bf12-9ffb-46ea-8787-8f65f74a854a
  Args:
    source: Granville_James_Leveson-Gower
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 1958
  AddTriple (fe567310-d3fe-4fee-8a59-935e776f310c)
 Call ID: fe567310-d3fe-4fee-8a59-935e776f310c
  Args:
    relation: :hasRelation
    source: Granville_James_Leveson-Gower
    target: Doon_Aileen_Plunket
  AssignClass (db76b905-22c3-43fe-911f-5c20ef5f5a32)
 Call ID: db76b905-22c3-43fe-911f-5c20ef5f5a32
  Args:
    type: :Man
    source: Brindsley_Sheridan_Bushe_Plunket
  AssignClass (28ca7419-08e2-4757-b3b8-aa3b2a6f14c8)
 Call ID: 28ca7419-08e2-4757-b3b8-aa3b2a6f14c8
  Args:
    type: :Person
    source: Brindsley_Sheridan_Bushe_Plunket
  AddTriple (d383da57-8f40-4505-b320-a2d34a50d82a)
 Call ID: d383da57-8f40-4505-b320-a2d34a50d82a
  Args:
    relation: :hasFather
    source: Doon_Aileen_Plunket
    target: Brindsley_Sheridan_Bushe_Plunket
  AssignClass (1d55306f-3e65-4ebe-b98f-e33e628d81c3)
 Call ID: 1d55306f-3e65-4ebe-b98f-e33e628d81c3
  Args:
    type: :Man
    source: William_Plunket
  AssignClass (83395af5-6d14-439a-881c-d6f0ed2ce6b3)
 Call ID: 83395af5-6d14-439a-881c-d6f0ed2ce6b3
  Args:
    type: :Person
    source: William_Plunket
  AddTriple (b6d3664b-8d42-432b-9210-71b0bae27ebd)
 Call ID: b6d3664b-8d42-432b-9210-71b0bae27ebd
  Args:
    source: Brindsley_Sheridan_Bushe_Plunket
    target: William_Plunket
    relation: :hasFather
  AssignClass (2dbe813a-eebf-495e-8d4e-1b3dee9550f5)
 Call ID: 2dbe813a-eebf-495e-8d4e-1b3dee9550f5
  Args:
    type: :Woman
    source: Aileen_Sibell_Mary_Guinness
  AssignClass (8f7a542b-d028-4f43-8b4d-b0bc705c8d3b)
 Call ID: 8f7a542b-d028-4f43-8b4d-b0bc705c8d3b
  Args:
    type: :Person
    source: Aileen_Sibell_Mary_Guinness
  AddTriple (c652b2ec-a80a-45a6-9eca-bbdd4b732ed2)
 Call ID: c652b2ec-a80a-45a6-9eca-bbdd4b732ed2
  Args:
    relation: :hasMother
    target: Aileen_Sibell_Mary_Guinness
    source: Doon_Aileen_Plunket
  AssignClass (e9c0a823-6233-48a7-9d7e-afb0e045ccee)
 Call ID: e9c0a823-6233-48a7-9d7e-afb0e045ccee
  Args:
    type: :Man
    source: Edward_Guinness
  AssignClass (0670b1a2-6a0d-42da-bf08-e0651a9b09ec)
 Call ID: 0670b1a2-6a0d-42da-bf08-e0651a9b09ec
  Args:
    type: :Person
    source: Edward_Guinness
  AddTriple (4bf6446f-1e28-41e3-a6a7-ded1f872eac2)
 Call ID: 4bf6446f-1e28-41e3-a6a7-ded1f872eac2
  Args:
    relation: :hasFather
    target: Edward_Guinness
    source: Aileen_Sibell_Mary_Guinness
  Finish (c4eb54fd-ae65-44e5-b263-01cb3ddcd132)
 Call ID: c4eb54fd-ae65-44e5-b263-01cb3ddcd132
  Args: