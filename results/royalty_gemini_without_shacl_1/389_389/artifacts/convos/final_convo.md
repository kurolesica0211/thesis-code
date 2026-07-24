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
Michael Claude Hamilton Bowes-Lyon (1 October 1893 – 1 May 1953), known as Mickie Bowes-Lyon, was an elder brother of Queen Elizabeth the Queen Mother and maternal uncle of Queen Elizabeth II.
Biography

Bowes-Lyon was born on 1 October 1893, the fifth son and eighth child of Claude Bowes-Lyon, Lord Glamis, later 14th
During World War I, Bowes-Lyon served in France in The Royal Scots (Lothian Regiment).
After the war, Bowes-Lyon was a justice of the peace and deputy lieutenant of Bedfordshire.
In 1928, Bowes-Lyon married Elizabeth Margaret Cator (1899–1959), daughter of John Cator, at St George's, Hanover Square.
Cator had been a bridesmaid at his sister Elizabeth's wedding to Prince Albert, Duke of York, in 1923.
Bowes-Lyon predeceased him and the earldom was inherited by his eldest son, Fergus, in 1972.
Bowes-Lyon died on 1 May 1953 at his home in Biggleswade as the result of asthma.



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
  AssignClass (82018570-622b-4a3d-9548-4db3828916bc)
 Call ID: 82018570-622b-4a3d-9548-4db3828916bc
  Args:
    type: :Man
    source: :Michael_Claude_Hamilton_Bowes-Lyon
  AssignClass (73d83935-2320-4a9f-adc2-dbc25c76dee5)
 Call ID: 73d83935-2320-4a9f-adc2-dbc25c76dee5
  Args:
    source: :Michael_Claude_Hamilton_Bowes-Lyon
    type: :Person
  AddLiteral (6f4c7cb3-c369-4af5-9a39-c854436cc9d2)
 Call ID: 6f4c7cb3-c369-4af5-9a39-c854436cc9d2
  Args:
    literal_value: Mickie Bowes-Lyon
    source: :Michael_Claude_Hamilton_Bowes-Lyon
    relation: :knownAs
    literal_type: xsd:string
  AddLiteral (86542aa4-977d-4ed2-9bb4-aa603f3ae04e)
 Call ID: 86542aa4-977d-4ed2-9bb4-aa603f3ae04e
  Args:
    literal_type: xsd:integer
    literal_value: 1893
    source: :Michael_Claude_Hamilton_Bowes-Lyon
    relation: :hasBirthYear
  AddLiteral (5f96367a-82db-41b3-a47e-86a2beab55f9)
 Call ID: 5f96367a-82db-41b3-a47e-86a2beab55f9
  Args:
    literal_type: xsd:integer
    literal_value: 1953
    source: :Michael_Claude_Hamilton_Bowes-Lyon
    relation: :hasDeathYear
  AssignClass (158e7061-f13a-4daf-b130-6f43d6b0bba4)
 Call ID: 158e7061-f13a-4daf-b130-6f43d6b0bba4
  Args:
    source: :Claude_Bowes-Lyon
    type: :Man
  AssignClass (356c7167-f96d-4ddd-9b98-9c228324362a)
 Call ID: 356c7167-f96d-4ddd-9b98-9c228324362a
  Args:
    type: :Person
    source: :Claude_Bowes-Lyon
  AddTriple (8eb99aae-48cf-4b7f-abc0-142f74cdd5f8)
 Call ID: 8eb99aae-48cf-4b7f-abc0-142f74cdd5f8
  Args:
    source: :Michael_Claude_Hamilton_Bowes-Lyon
    relation: :hasFather
    target: :Claude_Bowes-Lyon
  AssignClass (8fffb882-9e4a-40a7-a1a0-056b720ce9db)
 Call ID: 8fffb882-9e4a-40a7-a1a0-056b720ce9db
  Args:
    source: :Elizabeth_the_Queen_Mother
    type: :Woman
  AssignClass (dde559ae-f8d6-41b3-87b4-01d32ebe511e)
 Call ID: dde559ae-f8d6-41b3-87b4-01d32ebe511e
  Args:
    source: :Elizabeth_the_Queen_Mother
    type: :Person
  AddTriple (09f6f7e1-d2ab-4606-8346-718a986c07bb)
 Call ID: 09f6f7e1-d2ab-4606-8346-718a986c07bb
  Args:
    target: :Elizabeth_the_Queen_Mother
    source: :Michael_Claude_Hamilton_Bowes-Lyon
    relation: :isBrotherOf
  AssignClass (1859c38c-455c-4e99-bbce-bc004a8b3ae0)
 Call ID: 1859c38c-455c-4e99-bbce-bc004a8b3ae0
  Args:
    type: :Woman
    source: :Queen_Elizabeth_II
  AssignClass (dcf0cb4f-8707-4719-b2d2-182d2697ac56)
 Call ID: dcf0cb4f-8707-4719-b2d2-182d2697ac56
  Args:
    source: :Queen_Elizabeth_II
    type: :Person
  AddTriple (453fd4f2-a2c6-45a7-9480-248ef26955f7)
 Call ID: 453fd4f2-a2c6-45a7-9480-248ef26955f7
  Args:
    target: :Queen_Elizabeth_II
    source: :Michael_Claude_Hamilton_Bowes-Lyon
    relation: :isUncleOf
  AssignClass (15863858-9982-491e-b954-88d4e6291b16)
 Call ID: 15863858-9982-491e-b954-88d4e6291b16
  Args:
    source: :Elizabeth_Margaret_Cator
    type: :Woman
  AssignClass (3bc46e93-7591-468b-99de-49e07adbe043)
 Call ID: 3bc46e93-7591-468b-99de-49e07adbe043
  Args:
    source: :Elizabeth_Margaret_Cator
    type: :Person
  AddLiteral (3f82e582-9a4f-4059-ac4d-6f0ed1ed6b86)
 Call ID: 3f82e582-9a4f-4059-ac4d-6f0ed1ed6b86
  Args:
    source: :Michael_Claude_Hamilton_Bowes-Lyon
    relation: :hasMarriageYear
    literal_value: 1928
    literal_type: xsd:integer
  AddTriple (34b2f22e-f36a-4864-b52f-0f699d295f77)
 Call ID: 34b2f22e-f36a-4864-b52f-0f699d295f77
  Args:
    source: :Michael_Claude_Hamilton_Bowes-Lyon
    relation: :hasRelation
    target: :Elizabeth_Margaret_Cator
  AssignClass (0010f728-fcbe-42ac-96e8-196dd3883b8c)
 Call ID: 0010f728-fcbe-42ac-96e8-196dd3883b8c
  Args:
    source: :John_Cator
    type: :Man
  AssignClass (d2b4b31f-3060-4eb3-a67e-935c0f19a314)
 Call ID: d2b4b31f-3060-4eb3-a67e-935c0f19a314
  Args:
    type: :Person
    source: :John_Cator
  AddTriple (7f5e546e-7d62-4a15-9daf-46332371b53a)
 Call ID: 7f5e546e-7d62-4a15-9daf-46332371b53a
  Args:
    source: :Elizabeth_Margaret_Cator
    relation: :hasFather
    target: :John_Cator
  AssignClass (3880710b-b0da-4d79-9eba-f1287fba5859)
 Call ID: 3880710b-b0da-4d79-9eba-f1287fba5859
  Args:
    type: :Man
    source: :Fergus_Bowes-Lyon
  AssignClass (2b24ce93-2113-47e6-a65d-009ae83ab083)
 Call ID: 2b24ce93-2113-47e6-a65d-009ae83ab083
  Args:
    source: :Fergus_Bowes-Lyon
    type: :Person
  AddTriple (4c45926f-2b42-4711-ab9b-b6336021c89c)
 Call ID: 4c45926f-2b42-4711-ab9b-b6336021c89c
  Args:
    source: :Michael_Claude_Hamilton_Bowes-Lyon
    relation: :hasSon
    target: :Fergus_Bowes-Lyon
  Finish (31774495-24d2-4866-9339-7586878e6074)
 Call ID: 31774495-24d2-4866-9339-7586878e6074
  Args: