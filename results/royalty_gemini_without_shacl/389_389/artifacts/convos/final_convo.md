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
  AssignClass (00182472-6efb-4110-b74d-333d4d1777b9)
 Call ID: 00182472-6efb-4110-b74d-333d4d1777b9
  Args:
    type: :Man
    source: Michael_Claude_Hamilton_Bowes-Lyon
  AssignClass (c0c2bd54-52b2-493a-a879-decddc2446e4)
 Call ID: c0c2bd54-52b2-493a-a879-decddc2446e4
  Args:
    source: Michael_Claude_Hamilton_Bowes-Lyon
    type: :Person
  AddLiteral (d8372989-26a9-4487-b1a2-9441f1a42000)
 Call ID: d8372989-26a9-4487-b1a2-9441f1a42000
  Args:
    source: Michael_Claude_Hamilton_Bowes-Lyon
    literal_value: 1893
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (4b40b919-0584-431c-9f82-418d4b198df2)
 Call ID: 4b40b919-0584-431c-9f82-418d4b198df2
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: Michael_Claude_Hamilton_Bowes-Lyon
    literal_value: 1953
  AddLiteral (a797ec6d-59ce-42f4-99a7-2a8853283831)
 Call ID: a797ec6d-59ce-42f4-99a7-2a8853283831
  Args:
    source: Michael_Claude_Hamilton_Bowes-Lyon
    literal_value: Mickie Bowes-Lyon
    literal_type: xsd:string
    relation: :knownAs
  AssignClass (afaabd0b-6278-4ded-a26a-0c44cb49f329)
 Call ID: afaabd0b-6278-4ded-a26a-0c44cb49f329
  Args:
    source: Claude_Bowes-Lyon
    type: :Man
  AssignClass (8cb4a730-5e57-4593-9178-b206a44f6b2d)
 Call ID: 8cb4a730-5e57-4593-9178-b206a44f6b2d
  Args:
    source: Claude_Bowes-Lyon
    type: :Person
  AddTriple (d561f7b1-ec2b-470d-b60b-4228368df582)
 Call ID: d561f7b1-ec2b-470d-b60b-4228368df582
  Args:
    source: Michael_Claude_Hamilton_Bowes-Lyon
    target: Claude_Bowes-Lyon
    relation: :hasFather
  AssignClass (fc8f621b-0cd9-41ee-a215-5aee90f21ec2)
 Call ID: fc8f621b-0cd9-41ee-a215-5aee90f21ec2
  Args:
    type: :Woman
    source: Elizabeth_Margaret_Cator
  AssignClass (9c69956c-e2a2-43ae-93f4-084f43171819)
 Call ID: 9c69956c-e2a2-43ae-93f4-084f43171819
  Args:
    type: :Person
    source: Elizabeth_Margaret_Cator
  AddTriple (e1db8ecd-8d2e-4bd7-823b-7bed2f008a2b)
 Call ID: e1db8ecd-8d2e-4bd7-823b-7bed2f008a2b
  Args:
    target: Elizabeth_Margaret_Cator
    source: Michael_Claude_Hamilton_Bowes-Lyon
    relation: :hasRelation
  AddLiteral (e761a81f-1638-4b6a-afc1-b4dccd0f4e84)
 Call ID: e761a81f-1638-4b6a-afc1-b4dccd0f4e84
  Args:
    literal_value: 1928
    source: Michael_Claude_Hamilton_Bowes-Lyon
    relation: :hasMarriageYear
    literal_type: xsd:integer
  AssignClass (66965f57-19e4-49e8-aaec-4985a8d2948d)
 Call ID: 66965f57-19e4-49e8-aaec-4985a8d2948d
  Args:
    type: :Man
    source: John_Cator
  AssignClass (a640aaa2-67c4-4859-a9f0-1cf4245cbfeb)
 Call ID: a640aaa2-67c4-4859-a9f0-1cf4245cbfeb
  Args:
    source: John_Cator
    type: :Person
  AddTriple (44bfbd40-5f61-43a0-9821-173319738880)
 Call ID: 44bfbd40-5f61-43a0-9821-173319738880
  Args:
    relation: :hasFather
    source: Elizabeth_Margaret_Cator
    target: John_Cator
  AssignClass (5df44a62-c93d-4af6-a2ba-ec1565dd708d)
 Call ID: 5df44a62-c93d-4af6-a2ba-ec1565dd708d
  Args:
    type: :Man
    source: Fergus_Bowes-Lyon
  AssignClass (4d9e8b0a-b5d6-4a54-9a5f-d7717c5546c9)
 Call ID: 4d9e8b0a-b5d6-4a54-9a5f-d7717c5546c9
  Args:
    source: Fergus_Bowes-Lyon
    type: :Person
  AddTriple (de8dbe06-e8b3-4089-807f-baf91639e8e1)
 Call ID: de8dbe06-e8b3-4089-807f-baf91639e8e1
  Args:
    source: Michael_Claude_Hamilton_Bowes-Lyon
    target: Fergus_Bowes-Lyon
    relation: :hasSon
  AssignClass (6674f82d-e7ff-47aa-869a-2194dd1644f3)
 Call ID: 6674f82d-e7ff-47aa-869a-2194dd1644f3
  Args:
    type: :Woman
    source: Queen_Elizabeth_The_Queen_Mother
  AssignClass (5306c790-1ec1-4bb0-ab68-85e45feb447b)
 Call ID: 5306c790-1ec1-4bb0-ab68-85e45feb447b
  Args:
    source: Queen_Elizabeth_The_Queen_Mother
    type: :Person
  AddTriple (7afbdeee-2bae-46e1-892b-326347b9396c)
 Call ID: 7afbdeee-2bae-46e1-892b-326347b9396c
  Args:
    target: Queen_Elizabeth_The_Queen_Mother
    source: Michael_Claude_Hamilton_Bowes-Lyon
    relation: :hasSister
  AssignClass (154ae6db-7d88-4d9e-ba5c-0b1bff56fdea)
 Call ID: 154ae6db-7d88-4d9e-ba5c-0b1bff56fdea
  Args:
    type: :Woman
    source: Queen_Elizabeth_II
  AssignClass (e691a772-a9c5-4e04-8bd8-467a131e0506)
 Call ID: e691a772-a9c5-4e04-8bd8-467a131e0506
  Args:
    source: Queen_Elizabeth_II
    type: :Person
  AddTriple (2192d2c3-7fbf-42c3-b309-cc08632175f4)
 Call ID: 2192d2c3-7fbf-42c3-b309-cc08632175f4
  Args:
    source: Michael_Claude_Hamilton_Bowes-Lyon
    target: Queen_Elizabeth_II
    relation: :isUncleOf
  Finish (211d1083-a6c1-483f-a4c6-3916a0545946)
 Call ID: 211d1083-a6c1-483f-a4c6-3916a0545946
  Args: