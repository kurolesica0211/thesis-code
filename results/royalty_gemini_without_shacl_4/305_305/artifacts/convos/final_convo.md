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
Alexander Mountstuart Elphinstone, 19th Lord Elphinstone, 5th Baron Elphinstone (born 15 April 1980), is a Scottish peer in both the Peerage of Scotland and the Peerage of the United Kingdom.
Early life and family

Lord Elphinstone is the son of James Elphinstone, 18th Lord Elphinstone, and Willa Mary Gabrielle Chetwode.
His mother is the daughter of Major George Chetwode and Lady Willa Elliot-Murray-Kynynmound, daughter of Victor Elliot-Murray-Kynynmound, 5th Earl of Minto.
Lord Elphinstone's paternal grandfather, Rev. Hon.
Andrew Elphinstone, was a first cousin of Elizabeth II through his mother, the former Lady Mary Bowes-Lyon, who was an elder sister of Queen Elizabeth The Queen Mother.
Notes

References




This biography of a Lord of Parliament in the Peerage of Scotland is a stub.



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
  AssignClass (57e584b0-f573-466e-b729-26fc4ef118bc)
 Call ID: 57e584b0-f573-466e-b729-26fc4ef118bc
  Args:
    type: :Man
    source: Alexander_Mountstuart_Elphinstone
  AssignClass (b72c21f6-91f7-4b5b-98af-122b9d641ba5)
 Call ID: b72c21f6-91f7-4b5b-98af-122b9d641ba5
  Args:
    type: :Person
    source: Alexander_Mountstuart_Elphinstone
  AddLiteral (3e887c9d-ecda-435c-a958-dff52fd55c28)
 Call ID: 3e887c9d-ecda-435c-a958-dff52fd55c28
  Args:
    source: Alexander_Mountstuart_Elphinstone
    literal_type: xsd:date
    literal_value: 1980-04-15
    relation: :hasBirthYear
  AssignClass (40ffc852-8346-4f18-b3be-09f695e4204e)
 Call ID: 40ffc852-8346-4f18-b3be-09f695e4204e
  Args:
    type: :Man
    source: James_Elphinstone
  AssignClass (9e315274-a92e-4ae5-bf12-a99b187dbc01)
 Call ID: 9e315274-a92e-4ae5-bf12-a99b187dbc01
  Args:
    type: :Person
    source: James_Elphinstone
  AddTriple (2df6a22f-170e-4a1a-b0f6-b8481ad35000)
 Call ID: 2df6a22f-170e-4a1a-b0f6-b8481ad35000
  Args:
    relation: :hasFather
    source: Alexander_Mountstuart_Elphinstone
    target: James_Elphinstone
  AssignClass (1ee14822-b2e7-4978-8c8e-ed2650c60d20)
 Call ID: 1ee14822-b2e7-4978-8c8e-ed2650c60d20
  Args:
    type: :Woman
    source: Willa_Mary_Gabrielle_Chetwode
  AssignClass (0414ca60-d72c-40ab-95bd-03c7d6dfe1e2)
 Call ID: 0414ca60-d72c-40ab-95bd-03c7d6dfe1e2
  Args:
    type: :Person
    source: Willa_Mary_Gabrielle_Chetwode
  AddTriple (f1c0d98f-b535-4256-84f3-f5bc27133e9e)
 Call ID: f1c0d98f-b535-4256-84f3-f5bc27133e9e
  Args:
    target: Willa_Mary_Gabrielle_Chetwode
    source: Alexander_Mountstuart_Elphinstone
    relation: :hasMother
  AddTriple (907fa912-c85b-4394-8dd8-1541215d5f8c)
 Call ID: 907fa912-c85b-4394-8dd8-1541215d5f8c
  Args:
    relation: :hasMother
    source: Willa_Mary_Gabrielle_Chetwode
    target: Lady_Willa_Elliot-Murray-Kynynmound
  AssignClass (f459e0e0-065a-4d18-892e-7bdc79f5d697)
 Call ID: f459e0e0-065a-4d18-892e-7bdc79f5d697
  Args:
    type: :Man
    source: Major_George_Chetwode
  AssignClass (85ed9ad1-b142-473e-ad4f-09f0b0e3f937)
 Call ID: 85ed9ad1-b142-473e-ad4f-09f0b0e3f937
  Args:
    type: :Person
    source: Major_George_Chetwode
  AddTriple (2be72cdc-73c9-48f0-8ff2-2ec871a04f32)
 Call ID: 2be72cdc-73c9-48f0-8ff2-2ec871a04f32
  Args:
    target: Major_George_Chetwode
    source: Willa_Mary_Gabrielle_Chetwode
    relation: :hasFather
  AssignClass (2db7315e-d86a-4539-ad2a-c9a5420dfb6f)
 Call ID: 2db7315e-d86a-4539-ad2a-c9a5420dfb6f
  Args:
    type: :Woman
    source: Lady_Willa_Elliot-Murray-Kynynmound
  AssignClass (8660caac-788d-4ea0-a858-e32cb326030b)
 Call ID: 8660caac-788d-4ea0-a858-e32cb326030b
  Args:
    type: :Person
    source: Lady_Willa_Elliot-Murray-Kynynmound
  AddTriple (aa9c4286-f298-47c4-9a2c-c641ea167ce3)
 Call ID: aa9c4286-f298-47c4-9a2c-c641ea167ce3
  Args:
    relation: :hasMother
    target: Lady_Willa_Elliot-Murray-Kynynmound
    source: Willa_Mary_Gabrielle_Chetwode
  AssignClass (09e7139b-b5cd-450b-aeff-adb5693bd9ed)
 Call ID: 09e7139b-b5cd-450b-aeff-adb5693bd9ed
  Args:
    type: :Man
    source: Victor_Elliot-Murray-Kynynmound
  AssignClass (01254c75-2a10-48ee-bbda-cc8ab04276b8)
 Call ID: 01254c75-2a10-48ee-bbda-cc8ab04276b8
  Args:
    type: :Person
    source: Victor_Elliot-Murray-Kynynmound
  AddTriple (9b7fbc03-6c40-4eb7-b5f1-27a9e1eff924)
 Call ID: 9b7fbc03-6c40-4eb7-b5f1-27a9e1eff924
  Args:
    target: Victor_Elliot-Murray-Kynynmound
    source: Lady_Willa_Elliot-Murray-Kynynmound
    relation: :hasFather
  AssignClass (05f04074-ef66-4a7d-b49e-e17950344d49)
 Call ID: 05f04074-ef66-4a7d-b49e-e17950344d49
  Args:
    type: :Man
    source: Andrew_Elphinstone
  AssignClass (80d5293f-b036-4b72-845b-50a97bc29202)
 Call ID: 80d5293f-b036-4b72-845b-50a97bc29202
  Args:
    type: :Person
    source: Andrew_Elphinstone
  AddTriple (bc3606b0-579f-4d6b-adfc-fd2ecf20f51e)
 Call ID: bc3606b0-579f-4d6b-adfc-fd2ecf20f51e
  Args:
    relation: :hasFather
    source: James_Elphinstone
    target: Andrew_Elphinstone
  AssignClass (e8a2252c-fef9-430a-8c2c-e889998995b3)
 Call ID: e8a2252c-fef9-430a-8c2c-e889998995b3
  Args:
    type: :Woman
    source: Lady_Mary_Bowes-Lyon
  AssignClass (7bc9718d-e8ea-4802-a207-17b144829f11)
 Call ID: 7bc9718d-e8ea-4802-a207-17b144829f11
  Args:
    type: :Person
    source: Lady_Mary_Bowes-Lyon
  AddTriple (19af056b-84d1-44b6-8b80-633d8b8f649b)
 Call ID: 19af056b-84d1-44b6-8b80-633d8b8f649b
  Args:
    target: Lady_Mary_Bowes-Lyon
    source: Andrew_Elphinstone
    relation: :hasMother
  AssignClass (342fc345-dec7-4741-8fc4-e9419c73d9c6)
 Call ID: 342fc345-dec7-4741-8fc4-e9419c73d9c6
  Args:
    type: :Woman
    source: Queen_Elizabeth_The_Queen_Mother
  AssignClass (6059885b-5b50-4822-8047-584eb3f05e62)
 Call ID: 6059885b-5b50-4822-8047-584eb3f05e62
  Args:
    type: :Person
    source: Queen_Elizabeth_The_Queen_Mother
  AddTriple (7171d81f-3bb8-4b4d-b692-ca48352d0be6)
 Call ID: 7171d81f-3bb8-4b4d-b692-ca48352d0be6
  Args:
    target: Queen_Elizabeth_The_Queen_Mother
    source: Lady_Mary_Bowes-Lyon
    relation: :isSisterOf
  AssignClass (73da0913-9553-4572-989f-6bb669c00900)
 Call ID: 73da0913-9553-4572-989f-6bb669c00900
  Args:
    type: :Woman
    source: Elizabeth_II
  AssignClass (81a8a53d-5579-40c4-a098-08672756cd85)
 Call ID: 81a8a53d-5579-40c4-a098-08672756cd85
  Args:
    type: :Person
    source: Elizabeth_II
  Finish (7fd66d8f-9836-41fe-9e19-7d7dd52123ad)
 Call ID: 7fd66d8f-9836-41fe-9e19-7d7dd52123ad
  Args: