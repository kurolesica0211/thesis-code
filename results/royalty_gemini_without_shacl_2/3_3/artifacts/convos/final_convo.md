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
George Philip Nicholas Windsor, Earl of St Andrews (born 26 June 1962), is a British philanthropist, former diplomat and a member of the extended British royal family.
St Andrews became chancellor of the University of Bolton in 2017.
He is the elder son of Prince Edward, Duke of Kent, and Katharine, Duchess of Kent, and heir apparent to the dukedom of Kent.
Early life and career

George Philip Nicholas Windsor was born on 26 June 1962 at Coppins, Iver, Buckinghamshire, the eldest child of Prince Edward, Duke of Kent, and Katharine, Duchess of Kent (née Worsley, a daughter of Sir William Worsley, 4th Baronet).
Royal obstetrician Sir John Peel assisted at his birth, at which time Lord St Andrews was 10th in line of succession to the throne.
His godparents were Prince Philip, Duke of Edinburgh; his aunt Princess Alexandra of Kent, his uncle Oliver Worsley, and Lady Lily Serena Lumley (daughter of the 11th Earl of Scarbrough).
St Andrews served in the Diplomatic Service in New York and Budapest.
, George married Sylvana Tomaselli, a Canadian-born academic, at Leith Registration Office in Edinburgh at a civil ceremony.



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
  AssignClass (14230b65-5d18-4d08-8958-98a99fd221cd)
 Call ID: 14230b65-5d18-4d08-8958-98a99fd221cd
  Args:
    type: :Man
    source: George_Philip_Nicholas_Windsor
  AssignClass (9c0481bd-66ae-44e9-a1e7-0d88d7eaefe8)
 Call ID: 9c0481bd-66ae-44e9-a1e7-0d88d7eaefe8
  Args:
    type: :Person
    source: George_Philip_Nicholas_Windsor
  AddLiteral (f5dc3895-2b0d-43cb-9f6b-0eab01b2d132)
 Call ID: f5dc3895-2b0d-43cb-9f6b-0eab01b2d132
  Args:
    literal_value: 1962
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: George_Philip_Nicholas_Windsor
  AssignClass (e1c456c9-c1cb-4f96-a661-ed452acbe624)
 Call ID: e1c456c9-c1cb-4f96-a661-ed452acbe624
  Args:
    type: :Man
    source: Prince_Edward_Duke_of_Kent
  AssignClass (22d16f3a-e8c9-4811-99e7-879693862d2f)
 Call ID: 22d16f3a-e8c9-4811-99e7-879693862d2f
  Args:
    type: :Person
    source: Prince_Edward_Duke_of_Kent
  AssignClass (67985e21-a3ea-49ba-ba52-ab662bee037b)
 Call ID: 67985e21-a3ea-49ba-ba52-ab662bee037b
  Args:
    type: :Woman
    source: Katharine_Duchess_of_Kent
  AssignClass (09d80111-1799-43b0-931d-4eb1249f0d3f)
 Call ID: 09d80111-1799-43b0-931d-4eb1249f0d3f
  Args:
    type: :Person
    source: Katharine_Duchess_of_Kent
  AddTriple (3e8aca78-88e7-48de-8f1d-90804a231fdd)
 Call ID: 3e8aca78-88e7-48de-8f1d-90804a231fdd
  Args:
    relation: :hasFather
    source: George_Philip_Nicholas_Windsor
    target: Prince_Edward_Duke_of_Kent
  AddTriple (5828fc14-9189-40fe-9313-b18a6fc6ff0c)
 Call ID: 5828fc14-9189-40fe-9313-b18a6fc6ff0c
  Args:
    target: Katharine_Duchess_of_Kent
    source: George_Philip_Nicholas_Windsor
    relation: :hasMother
  AssignClass (5f5712bf-1c09-4a2c-8b4d-9ad56713a6b0)
 Call ID: 5f5712bf-1c09-4a2c-8b4d-9ad56713a6b0
  Args:
    type: :Man
    source: Sir_William_Worsley
  AssignClass (b28baf49-d665-4dfa-9cc0-41c0a17aacc6)
 Call ID: b28baf49-d665-4dfa-9cc0-41c0a17aacc6
  Args:
    type: :Person
    source: Sir_William_Worsley
  AddTriple (b543e889-1c51-49d7-9158-6e406fa7ca31)
 Call ID: b543e889-1c51-49d7-9158-6e406fa7ca31
  Args:
    target: Sir_William_Worsley
    source: Katharine_Duchess_of_Kent
    relation: :hasFather
  AssignClass (4837cd0f-4c97-42e1-902b-38849c0499ab)
 Call ID: 4837cd0f-4c97-42e1-902b-38849c0499ab
  Args:
    type: :Woman
    source: Sylvana_Tomaselli
  AssignClass (12af3e50-907a-41b4-bf93-1e4f56b6b0ac)
 Call ID: 12af3e50-907a-41b4-bf93-1e4f56b6b0ac
  Args:
    type: :Person
    source: Sylvana_Tomaselli
  AddTriple (17f24b82-ec32-4774-984e-27ad2b530a5c)
 Call ID: 17f24b82-ec32-4774-984e-27ad2b530a5c
  Args:
    relation: :hasRelation
    source: George_Philip_Nicholas_Windsor
    target: Sylvana_Tomaselli
  AssignClass (2244767d-b7f8-4016-af19-51dd99c3b79f)
 Call ID: 2244767d-b7f8-4016-af19-51dd99c3b79f
  Args:
    type: :Man
    source: Prince_Philip_Duke_of_Edinburgh
  AssignClass (946e2de7-77e0-483b-b923-a75318c38a66)
 Call ID: 946e2de7-77e0-483b-b923-a75318c38a66
  Args:
    type: :Person
    source: Prince_Philip_Duke_of_Edinburgh
  AssignClass (47598979-cf92-4489-998b-47763248798d)
 Call ID: 47598979-cf92-4489-998b-47763248798d
  Args:
    type: :Woman
    source: Princess_Alexandra_of_Kent
  AssignClass (78c32872-bfac-4514-a5d4-f3fee4225550)
 Call ID: 78c32872-bfac-4514-a5d4-f3fee4225550
  Args:
    type: :Person
    source: Princess_Alexandra_of_Kent
  AssignClass (a161f9dc-ca05-4fb0-9760-36033673a09b)
 Call ID: a161f9dc-ca05-4fb0-9760-36033673a09b
  Args:
    type: :Man
    source: Oliver_Worsley
  AssignClass (45f11c6f-131f-40ec-8e54-bf236d9f9e14)
 Call ID: 45f11c6f-131f-40ec-8e54-bf236d9f9e14
  Args:
    type: :Person
    source: Oliver_Worsley
  AssignClass (4ab182fd-dbef-49ab-a975-ba77f5c3bd49)
 Call ID: 4ab182fd-dbef-49ab-a975-ba77f5c3bd49
  Args:
    type: :Woman
    source: Lady_Lily_Serena_Lumley
  AssignClass (2cf6c826-906b-4f68-b794-63d4a4dbb5e3)
 Call ID: 2cf6c826-906b-4f68-b794-63d4a4dbb5e3
  Args:
    type: :Person
    source: Lady_Lily_Serena_Lumley
  AssignClass (374d4083-053a-4d7b-a05c-53142a1a2bdc)
 Call ID: 374d4083-053a-4d7b-a05c-53142a1a2bdc
  Args:
    type: :Man
    source: Earl_of_Scarbrough
  AssignClass (4f2313ec-3541-4956-886d-c574f6c82dd2)
 Call ID: 4f2313ec-3541-4956-886d-c574f6c82dd2
  Args:
    type: :Person
    source: Earl_of_Scarbrough
  AddTriple (2063cae5-330f-4326-a4d2-e05c8e006c1d)
 Call ID: 2063cae5-330f-4326-a4d2-e05c8e006c1d
  Args:
    relation: :hasFather
    source: Lady_Lily_Serena_Lumley
    target: Earl_of_Scarbrough
  Finish (2a42dafc-63cc-43eb-8404-aad6528da9b1)
 Call ID: 2a42dafc-63cc-43eb-8404-aad6528da9b1
  Args: