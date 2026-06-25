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
Fergus Bowes-Lyon (18 April 1889 – 27 September 1915) was a British officer and older brother of Elizabeth Bowes-Lyon, who later became the queen consort of King George VI.
He was a maternal uncle of Queen Elizabeth II.
Early life and marriage

Fergus Bowes-Lyon was born at Forbes House in Ham, Surrey, the son of Claude Bowes-Lyon, 14th
Bowes-Lyon had his early education at Ludgrove School.
On 17 September 1914, Bowes-Lyon married Lady Christian Norah Dawson-Damer (7 August 1890 – 29 March 1959), daughter of the 5th Earl of Portarlington.
Rosemary was only two months old when Fergus died in the line of duty on 27 September 1915, only 10 days after the first anniversary of his wedding.
His issue:


World War I

In the First World War, Bowes-Lyon served with the 8th Battalion, Black Watch: as a lieutenant since 19 August 1914, and as temporary captain since 17 November.
Bowes-Lyon was killed in action on 27 September 1915, during the Battle of the Hohenzollern Redoubt in the Battle of Loos.
At the time of Bowes-Lyon's death, his brother John was also serving with the Black Watch.
His mother, Cecilia Bowes-Lyon, Countess of Strathmore and Kinghorne, was severely affected by the loss of her son, and after his death became an invalid, withdrawn from public life until the marriage of her daughter Elizabeth to the future king George VI in 1923.
Fergus's widow later married Captain William Frederick Martin (d. 6 October 1947).
In November 2011, Bowes-Lyon's grandson supplied family records to the Commonwealth War Graves Commission detailing his original burial place, and showing that it had remained marked until the end of the war.



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
  AssignClass (174486c1-ff50-46ef-a4a7-f95aa76d114c)
 Call ID: 174486c1-ff50-46ef-a4a7-f95aa76d114c
  Args:
    type: :Man
    source: Fergus Bowes-Lyon
  AssignClass (8e8b68bb-64b4-4c29-86bd-f37bdd94a0f5)
 Call ID: 8e8b68bb-64b4-4c29-86bd-f37bdd94a0f5
  Args:
    source: Fergus Bowes-Lyon
    type: :Person
  AddLiteral (8ad78414-ee79-43e9-8218-1e5b75901b4a)
 Call ID: 8ad78414-ee79-43e9-8218-1e5b75901b4a
  Args:
    literal_value: 1889
    relation: :hasBirthYear
    source: Fergus Bowes-Lyon
    literal_type: xsd:integer
  AddLiteral (f8a95986-6f21-4d8e-8f66-c4932bbd64a4)
 Call ID: f8a95986-6f21-4d8e-8f66-c4932bbd64a4
  Args:
    literal_type: xsd:integer
    literal_value: 1915
    relation: :hasDeathYear
    source: Fergus Bowes-Lyon
  AssignClass (1a0fcc66-6b30-4165-9e3c-b26362ff5c52)
 Call ID: 1a0fcc66-6b30-4165-9e3c-b26362ff5c52
  Args:
    source: Elizabeth Bowes-Lyon
    type: :Woman
  AssignClass (1827e3cf-ab14-4994-89ba-652f3de6c17a)
 Call ID: 1827e3cf-ab14-4994-89ba-652f3de6c17a
  Args:
    source: Elizabeth Bowes-Lyon
    type: :Person
  AddTriple (0e77367f-29ad-4e66-a439-882310d1fa57)
 Call ID: 0e77367f-29ad-4e66-a439-882310d1fa57
  Args:
    relation: :isSiblingOf
    target: Elizabeth Bowes-Lyon
    source: Fergus Bowes-Lyon
  AssignClass (671000fe-c0c7-45ff-9370-0e5b9bda7f96)
 Call ID: 671000fe-c0c7-45ff-9370-0e5b9bda7f96
  Args:
    source: Queen Elizabeth II
    type: :Woman
  AssignClass (116d2fca-d618-46a3-969d-77b1d61d151a)
 Call ID: 116d2fca-d618-46a3-969d-77b1d61d151a
  Args:
    type: :Person
    source: Queen Elizabeth II
  AddTriple (7a6dde1e-a8e2-4619-b2cd-af153006241f)
 Call ID: 7a6dde1e-a8e2-4619-b2cd-af153006241f
  Args:
    source: Fergus Bowes-Lyon
    relation: :isUncleOf
    target: Queen Elizabeth II
  AssignClass (f05bb07e-dcbc-499a-9eea-f5d59b0959b6)
 Call ID: f05bb07e-dcbc-499a-9eea-f5d59b0959b6
  Args:
    type: :Man
    source: Claude Bowes-Lyon, 14th
  AssignClass (63828d79-c225-403a-ab44-24997f1d82a2)
 Call ID: 63828d79-c225-403a-ab44-24997f1d82a2
  Args:
    source: Claude Bowes-Lyon, 14th
    type: :Person
  AddTriple (ca3b18f2-ace5-4690-a97c-60229dc4ce58)
 Call ID: ca3b18f2-ace5-4690-a97c-60229dc4ce58
  Args:
    source: Fergus Bowes-Lyon
    relation: :hasFather
    target: Claude Bowes-Lyon, 14th
  AssignClass (ce6e580c-179c-4d3f-a608-1ac889c01d89)
 Call ID: ce6e580c-179c-4d3f-a608-1ac889c01d89
  Args:
    source: Lady Christian Norah Dawson-Damer
    type: :Woman
  AssignClass (158c342e-ebfd-4841-92b5-fb863090447b)
 Call ID: 158c342e-ebfd-4841-92b5-fb863090447b
  Args:
    type: :Person
    source: Lady Christian Norah Dawson-Damer
  AddTriple (3d7d15af-aec3-4624-b29c-ce0e2b219b15)
 Call ID: 3d7d15af-aec3-4624-b29c-ce0e2b219b15
  Args:
    relation: :hasRelation
    target: Lady Christian Norah Dawson-Damer
    source: Fergus Bowes-Lyon
  AddLiteral (78bd2927-e54d-4412-bfa7-c50d0e96869a)
 Call ID: 78bd2927-e54d-4412-bfa7-c50d0e96869a
  Args:
    literal_type: xsd:integer
    source: Fergus Bowes-Lyon
    literal_value: 1914
    relation: :hasMarriageYear
  AssignClass (8cec9b4e-5d0c-44e0-925d-9945c76abb3e)
 Call ID: 8cec9b4e-5d0c-44e0-925d-9945c76abb3e
  Args:
    source: Rosemary
    type: :Woman
  AssignClass (6a01bfa3-0d4a-472e-ad38-c31d100e2e49)
 Call ID: 6a01bfa3-0d4a-472e-ad38-c31d100e2e49
  Args:
    type: :Person
    source: Rosemary
  AddTriple (3f332227-0306-4ba3-bc24-fd5a8e07ea71)
 Call ID: 3f332227-0306-4ba3-bc24-fd5a8e07ea71
  Args:
    relation: :isDaughterOf
    target: Fergus Bowes-Lyon
    source: Rosemary
  AddTriple (6c7d017c-d9ed-47d6-a761-209fcf8444d1)
 Call ID: 6c7d017c-d9ed-47d6-a761-209fcf8444d1
  Args:
    target: Lady Christian Norah Dawson-Damer
    relation: :isDaughterOf
    source: Rosemary
  AssignClass (688606cc-f0f5-4dd8-b0ee-d70b00a00be7)
 Call ID: 688606cc-f0f5-4dd8-b0ee-d70b00a00be7
  Args:
    type: :Man
    source: John
  AssignClass (d6987c3d-3cff-4c50-9c3d-f942546a03ff)
 Call ID: d6987c3d-3cff-4c50-9c3d-f942546a03ff
  Args:
    source: John
    type: :Person
  AddTriple (42e0640a-4ca3-4177-9b4d-b9cd3c077a1b)
 Call ID: 42e0640a-4ca3-4177-9b4d-b9cd3c077a1b
  Args:
    relation: :isSiblingOf
    target: John
    source: Fergus Bowes-Lyon
  AssignClass (04c9e544-4b06-41a8-abad-74c7257ab6b8)
 Call ID: 04c9e544-4b06-41a8-abad-74c7257ab6b8
  Args:
    source: Cecilia Bowes-Lyon, Countess of Strathmore and Kinghorne
    type: :Woman
  AssignClass (d9a1990a-4d94-4c1f-8746-53bd285cc759)
 Call ID: d9a1990a-4d94-4c1f-8746-53bd285cc759
  Args:
    type: :Person
    source: Cecilia Bowes-Lyon, Countess of Strathmore and Kinghorne
  AddTriple (0c317384-d410-466e-98b4-e98ebd05f55e)
 Call ID: 0c317384-d410-466e-98b4-e98ebd05f55e
  Args:
    source: Fergus Bowes-Lyon
    relation: :hasMother
    target: Cecilia Bowes-Lyon, Countess of Strathmore and Kinghorne
  AssignClass (4dad0291-1f3a-418d-a916-60a6ca20eda7)
 Call ID: 4dad0291-1f3a-418d-a916-60a6ca20eda7
  Args:
    type: :Man
    source: Captain William Frederick Martin
  AssignClass (0b9069c3-df73-4dc1-a29b-9de69fd32443)
 Call ID: 0b9069c3-df73-4dc1-a29b-9de69fd32443
  Args:
    source: Captain William Frederick Martin
    type: :Person
  AddTriple (7eb924ee-a739-4331-8323-d25d940e22b7)
 Call ID: 7eb924ee-a739-4331-8323-d25d940e22b7
  Args:
    source: Lady Christian Norah Dawson-Damer
    relation: :hasRelation
    target: Captain William Frederick Martin
  Finish (872aa4c0-d5b6-4e7f-a404-8423fdf45352)
 Call ID: 872aa4c0-d5b6-4e7f-a404-8423fdf45352
  Args: