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
  AssignClass (a9138e10-db2f-40f7-a64c-3ef23b40de16)
 Call ID: a9138e10-db2f-40f7-a64c-3ef23b40de16
  Args:
    type: :Man
    source: AlexanderMountstuartElphinstone
  AssignClass (3a302386-4086-469c-93a7-2e9c0ce37fa3)
 Call ID: 3a302386-4086-469c-93a7-2e9c0ce37fa3
  Args:
    type: :Person
    source: AlexanderMountstuartElphinstone
  AddLiteral (295973de-c8d5-432a-85be-2f7e2ead4d5a)
 Call ID: 295973de-c8d5-432a-85be-2f7e2ead4d5a
  Args:
    literal_value: 1980
    literal_type: xsd:integer
    source: AlexanderMountstuartElphinstone
    relation: :hasBirthYear
  AssignClass (2642afc5-2fba-49a5-897a-1a09e78a2cba)
 Call ID: 2642afc5-2fba-49a5-897a-1a09e78a2cba
  Args:
    type: :Man
    source: JamesElphinstone
  AssignClass (61415ca5-ed7b-472a-a97f-fbde6023b04d)
 Call ID: 61415ca5-ed7b-472a-a97f-fbde6023b04d
  Args:
    type: :Person
    source: JamesElphinstone
  AddTriple (d40c27b0-29fb-41f0-95f6-abba8fe55ff6)
 Call ID: d40c27b0-29fb-41f0-95f6-abba8fe55ff6
  Args:
    target: JamesElphinstone
    source: AlexanderMountstuartElphinstone
    relation: :hasFather
  AssignClass (214008af-8753-484a-ad2e-77ed67823086)
 Call ID: 214008af-8753-484a-ad2e-77ed67823086
  Args:
    type: :Woman
    source: WillaMaryGabrielleChetwode
  AssignClass (42f4fe42-c33d-4a0a-b431-074b36d4c5fd)
 Call ID: 42f4fe42-c33d-4a0a-b431-074b36d4c5fd
  Args:
    source: WillaMaryGabrielleChetwode
    type: :Person
  AddTriple (a612efa7-dba5-4177-9a40-e3b48e78eea7)
 Call ID: a612efa7-dba5-4177-9a40-e3b48e78eea7
  Args:
    source: AlexanderMountstuartElphinstone
    target: WillaMaryGabrielleChetwode
    relation: :hasMother
  AssignClass (10bb8c95-f4c1-4b32-9965-c7c6eaa7e975)
 Call ID: 10bb8c95-f4c1-4b32-9965-c7c6eaa7e975
  Args:
    type: :Man
    source: GeorgeChetwode
  AssignClass (05a436fe-383d-46e7-9724-a8995bc38f2f)
 Call ID: 05a436fe-383d-46e7-9724-a8995bc38f2f
  Args:
    type: :Person
    source: GeorgeChetwode
  AddTriple (d39040d3-943f-4061-bae9-d383442de30f)
 Call ID: d39040d3-943f-4061-bae9-d383442de30f
  Args:
    target: WillaMaryGabrielleChetwode
    source: GeorgeChetwode
    relation: :isFatherOf
  AssignClass (2eb5e6ac-f303-45a6-9ee2-123faf267b51)
 Call ID: 2eb5e6ac-f303-45a6-9ee2-123faf267b51
  Args:
    source: WillaElliotMurrayKynynmound
    type: :Woman
  AssignClass (48c84e08-a3a0-4340-a96e-c174f2a69d2e)
 Call ID: 48c84e08-a3a0-4340-a96e-c174f2a69d2e
  Args:
    type: :Person
    source: WillaElliotMurrayKynynmound
  AddTriple (592fbc2f-340c-4ac3-92bc-83a0cb0e4785)
 Call ID: 592fbc2f-340c-4ac3-92bc-83a0cb0e4785
  Args:
    relation: :isMotherOf
    source: WillaElliotMurrayKynynmound
    target: WillaMaryGabrielleChetwode
  AssignClass (3c89aeb8-810e-455f-a4ec-a9e632907e7d)
 Call ID: 3c89aeb8-810e-455f-a4ec-a9e632907e7d
  Args:
    source: VictorElliotMurrayKynynmound
    type: :Man
  AssignClass (808e9158-512e-42e0-ab7a-01f3f261fa6a)
 Call ID: 808e9158-512e-42e0-ab7a-01f3f261fa6a
  Args:
    type: :Person
    source: VictorElliotMurrayKynynmound
  AddTriple (48ef1ebc-6b4e-4407-adf8-081bda2bf38c)
 Call ID: 48ef1ebc-6b4e-4407-adf8-081bda2bf38c
  Args:
    source: VictorElliotMurrayKynynmound
    target: WillaElliotMurrayKynynmound
    relation: :isFatherOf
  AssignClass (85ee29c1-9b14-4bd2-b4f6-c64312e04d17)
 Call ID: 85ee29c1-9b14-4bd2-b4f6-c64312e04d17
  Args:
    type: :Man
    source: AndrewElphinstone
  AssignClass (2c1e0740-10e8-471d-9d4c-90674e0a7ca8)
 Call ID: 2c1e0740-10e8-471d-9d4c-90674e0a7ca8
  Args:
    type: :Person
    source: AndrewElphinstone
  AddTriple (1b1f6687-25ab-42e4-b98d-fb7b5c6ae202)
 Call ID: 1b1f6687-25ab-42e4-b98d-fb7b5c6ae202
  Args:
    relation: :hasFather
    target: AndrewElphinstone
    source: JamesElphinstone
  AssignClass (1008e698-d231-4a0b-84d2-ea52f025b3c1)
 Call ID: 1008e698-d231-4a0b-84d2-ea52f025b3c1
  Args:
    source: MaryBowesLyon
    type: :Woman
  AssignClass (74032018-49ac-4193-8afd-3918fa221d2c)
 Call ID: 74032018-49ac-4193-8afd-3918fa221d2c
  Args:
    source: MaryBowesLyon
    type: :Person
  AddTriple (c74507b0-4c17-4797-9d26-782ada0bb191)
 Call ID: c74507b0-4c17-4797-9d26-782ada0bb191
  Args:
    relation: :isMotherOf
    target: AndrewElphinstone
    source: MaryBowesLyon
  AssignClass (63396f93-4306-424c-b733-d3fc116d03d4)
 Call ID: 63396f93-4306-424c-b733-d3fc116d03d4
  Args:
    type: :Woman
    source: ElizabethQueenMother
  AssignClass (5f5ac2c1-1ca5-4033-ad4d-9656c804a5c4)
 Call ID: 5f5ac2c1-1ca5-4033-ad4d-9656c804a5c4
  Args:
    type: :Person
    source: ElizabethQueenMother
  AddTriple (326ef3b6-fb7e-477d-8599-bf235c18ecb0)
 Call ID: 326ef3b6-fb7e-477d-8599-bf235c18ecb0
  Args:
    relation: :isSisterOf
    source: MaryBowesLyon
    target: ElizabethQueenMother
  AssignClass (8b16c8cd-057a-42f4-83d5-7e789133e88f)
 Call ID: 8b16c8cd-057a-42f4-83d5-7e789133e88f
  Args:
    type: :Woman
    source: ElizabethII
  AssignClass (8b73c916-b627-4f5f-af45-49a472cc3f56)
 Call ID: 8b73c916-b627-4f5f-af45-49a472cc3f56
  Args:
    source: ElizabethII
    type: :Person
  Finish (05077e79-21bc-4f0c-ae56-7c5a7bb4cde4)
 Call ID: 05077e79-21bc-4f0c-ae56-7c5a7bb4cde4
  Args: