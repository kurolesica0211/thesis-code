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
John David James Dalrymple, 14th Earl of Stair (born 4 September 1961) is a British politician and a former crossbench member of the House of Lords.
Background

Stair is the eldest child of John Dalrymple, 13th
Earl of Stair and Davina Katherine Bowes-Lyon (2 May 1930 – 1 November 2017), daughter of David Bowes-Lyon, brother of Queen Elizabeth
Lord Stair's mother, Davina, therefore, was a first cousin of Queen Elizabeth II and he is a second cousin of The King, The Princess Royal, Andrew Mountbatten-Windsor, and The Duke of Edinburgh.
Through his mother, he is descended from the Bowes-Lyon, Astor, and Cavendish-Bentinck families.
Through his paternal-grandmother, Violet Evelyn Dalrymple (Née Harford), he is a direct descendent of Frederick Calvert, 6th Baron Baltimore, the Calvert family were the founders and Proprietors of Province of Maryland.
Political career

Upon inheriting his peerage in 1996, Lord Stair entered the House of Lords and sat as a crossbencher.
Following the death of Davina Ingrams, 18th Baroness Darcy de Knayth in 2008, Lord Stair was elected to the Lords.
Family

Lord Stair married Emily Mary Julia Stonor (daughter of Ralph Stonor, 7th Baron Camoys, and Elizabeth Mary Hyde Parker) in 2006.



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
  AssignClass (2835804c-396e-4234-9e01-fa07729c6151)
 Call ID: 2835804c-396e-4234-9e01-fa07729c6151
  Args:
    type: :Man
    source: John_David_James_Dalrymple
  AssignClass (3df8d3d1-cda0-4e7c-9251-a609224b2ba2)
 Call ID: 3df8d3d1-cda0-4e7c-9251-a609224b2ba2
  Args:
    type: :Person
    source: John_David_James_Dalrymple
  AddLiteral (cbbce169-6fe7-4f40-930b-9a000887c099)
 Call ID: cbbce169-6fe7-4f40-930b-9a000887c099
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1961
    source: John_David_James_Dalrymple
  AssignClass (b267f0cb-5c62-4c2e-bae5-18d9159c78ba)
 Call ID: b267f0cb-5c62-4c2e-bae5-18d9159c78ba
  Args:
    type: :Man
    source: John_Dalrymple_13th_Earl_of_Stair
  AssignClass (288dde11-6bc4-4bcc-9c54-a917880591bc)
 Call ID: 288dde11-6bc4-4bcc-9c54-a917880591bc
  Args:
    type: :Person
    source: John_Dalrymple_13th_Earl_of_Stair
  AddTriple (aecaf386-175b-4e59-9c49-2b069b88d115)
 Call ID: aecaf386-175b-4e59-9c49-2b069b88d115
  Args:
    relation: :hasFather
    source: John_David_James_Dalrymple
    target: John_Dalrymple_13th_Earl_of_Stair
  AssignClass (a06561af-94e8-4508-9cf2-49264b25fe80)
 Call ID: a06561af-94e8-4508-9cf2-49264b25fe80
  Args:
    type: :Woman
    source: Davina_Katherine_Bowes-Lyon
  AssignClass (9d80e9eb-df06-4e06-929e-add498fdcfcc)
 Call ID: 9d80e9eb-df06-4e06-929e-add498fdcfcc
  Args:
    type: :Person
    source: Davina_Katherine_Bowes-Lyon
  AddLiteral (352a570c-fb36-4135-b97c-e6b435c2c975)
 Call ID: 352a570c-fb36-4135-b97c-e6b435c2c975
  Args:
    source: Davina_Katherine_Bowes-Lyon
    literal_value: 1930
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (83878f97-dfe5-45a9-b011-7ee3680df2c5)
 Call ID: 83878f97-dfe5-45a9-b011-7ee3680df2c5
  Args:
    source: Davina_Katherine_Bowes-Lyon
    literal_value: 2017
    relation: :hasDeathYear
    literal_type: xsd:integer
  AddTriple (cb937ac5-a658-4a25-8788-6c73bb3ab8fb)
 Call ID: cb937ac5-a658-4a25-8788-6c73bb3ab8fb
  Args:
    relation: :hasMother
    target: Davina_Katherine_Bowes-Lyon
    source: John_David_James_Dalrymple
  AssignClass (7587ff22-2081-4328-9b3b-9668f80cb1c7)
 Call ID: 7587ff22-2081-4328-9b3b-9668f80cb1c7
  Args:
    type: :Man
    source: David_Bowes-Lyon
  AssignClass (a28eadc2-b57d-4e4a-a31d-2987439c98d8)
 Call ID: a28eadc2-b57d-4e4a-a31d-2987439c98d8
  Args:
    type: :Person
    source: David_Bowes-Lyon
  AddTriple (32f2e2b0-c1e4-4c54-b3d7-649003daaf41)
 Call ID: 32f2e2b0-c1e4-4c54-b3d7-649003daaf41
  Args:
    target: David_Bowes-Lyon
    source: Davina_Katherine_Bowes-Lyon
    relation: :hasFather
  AssignClass (ef58ad6b-fc12-49b9-8289-2e99b47a405b)
 Call ID: ef58ad6b-fc12-49b9-8289-2e99b47a405b
  Args:
    type: :Woman
    source: Emily_Mary_Julia_Stonor
  AssignClass (a6013cc5-1440-42e6-b200-45a83704e6ef)
 Call ID: a6013cc5-1440-42e6-b200-45a83704e6ef
  Args:
    type: :Person
    source: Emily_Mary_Julia_Stonor
  AddTriple (7a8f07b6-d41f-43b0-a6aa-74e8e8177f86)
 Call ID: 7a8f07b6-d41f-43b0-a6aa-74e8e8177f86
  Args:
    source: John_David_James_Dalrymple
    target: Emily_Mary_Julia_Stonor
    relation: :hasRelation
  AddLiteral (889f7a1e-1383-426f-8440-87eb235d9bc9)
 Call ID: 889f7a1e-1383-426f-8440-87eb235d9bc9
  Args:
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: John_David_James_Dalrymple
    literal_value: 2006
  AssignClass (2cd45ffd-654a-4980-9773-acfe6179fedd)
 Call ID: 2cd45ffd-654a-4980-9773-acfe6179fedd
  Args:
    type: :Man
    source: Ralph_Stonor_7th_Baron_Camoys
  AssignClass (f9804c12-4329-4225-b730-b1d15033e0bc)
 Call ID: f9804c12-4329-4225-b730-b1d15033e0bc
  Args:
    type: :Person
    source: Ralph_Stonor_7th_Baron_Camoys
  AddTriple (f0beb7de-4e8f-4181-af0f-25e40cf39d1f)
 Call ID: f0beb7de-4e8f-4181-af0f-25e40cf39d1f
  Args:
    target: Ralph_Stonor_7th_Baron_Camoys
    source: Emily_Mary_Julia_Stonor
    relation: :hasFather
  AssignClass (91e697cf-8cdf-426a-9e0d-c1bd72977b4e)
 Call ID: 91e697cf-8cdf-426a-9e0d-c1bd72977b4e
  Args:
    type: :Woman
    source: Elizabeth_Mary_Hyde_Parker
  AssignClass (c67247f9-dc33-4953-9941-d9bcbc7a1fc8)
 Call ID: c67247f9-dc33-4953-9941-d9bcbc7a1fc8
  Args:
    type: :Person
    source: Elizabeth_Mary_Hyde_Parker
  AddTriple (f627060c-bc2f-4cbb-a174-87cb85f631ac)
 Call ID: f627060c-bc2f-4cbb-a174-87cb85f631ac
  Args:
    relation: :hasMother
    target: Elizabeth_Mary_Hyde_Parker
    source: Emily_Mary_Julia_Stonor
  AssignClass (e27c7611-3968-4997-b773-60bed7b23078)
 Call ID: e27c7611-3968-4997-b773-60bed7b23078
  Args:
    type: :Woman
    source: Violet_Evelyn_Dalrymple
  AssignClass (daad3851-2306-4215-86fc-5ca54cbd74d7)
 Call ID: daad3851-2306-4215-86fc-5ca54cbd74d7
  Args:
    type: :Person
    source: Violet_Evelyn_Dalrymple
  AddTriple (5e0cd94b-691d-4635-a223-8419f3132aca)
 Call ID: 5e0cd94b-691d-4635-a223-8419f3132aca
  Args:
    relation: :hasMother
    source: John_Dalrymple_13th_Earl_of_Stair
    target: Violet_Evelyn_Dalrymple
  AssignClass (58314c4a-aa99-4966-83b5-247f210c0a81)
 Call ID: 58314c4a-aa99-4966-83b5-247f210c0a81
  Args:
    type: :Man
    source: Frederick_Calvert_6th_Baron_Baltimore
  AssignClass (789ae550-e873-4f00-9f08-2599b40e6a51)
 Call ID: 789ae550-e873-4f00-9f08-2599b40e6a51
  Args:
    type: :Person
    source: Frederick_Calvert_6th_Baron_Baltimore
  AddTriple (37fc39d3-6545-4841-89dc-4bff8676a687)
 Call ID: 37fc39d3-6545-4841-89dc-4bff8676a687
  Args:
    relation: :hasAncestor
    source: John_David_James_Dalrymple
    target: Frederick_Calvert_6th_Baron_Baltimore
  Finish (d12f2c5f-1713-4390-88d2-324f9c8e94ac)
 Call ID: d12f2c5f-1713-4390-88d2-324f9c8e94ac
  Args: