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
Princess Nuria


Princess Françoise


Princess Mariam


Princess Monique


Prince Don Bagrat de Bagration y de Baviera, also Prince Bagrat Bagrationi-Mukhraneli and Prince Bagrat Bagration-Moukhransky (12 January 1949 – 20 March 2017) was a member of the Bagration dynasty which once ruled the Kingdom of Georgia and a relative of the royal family of Spain.
Background

He was born in Madrid, Spain on 12 January 1949 and named Bagrat Juan María de Fátima de Todos los Santos, the third child of Prince Irakli Bagration-Mukhrani (1909-1977) by his third wife, Infanta Doña María de las Mercedes de Baviera y Borbón (1911-1953), a niece of King Alfonso XIII of Spain.
His maternal great-grandfather was King Alfonso XII.
Prince Jorge de Bagration, a Spanish race car driver and pretender to the throne of Georgia, was his elder half brother.
His mother had been born in Madrid, and although part of her youth was spent in exile in the Basses Pyrénées of France, Bagrat was raised, along with Jorge and his elder sister Princess Mariam (born 1947), by his widowed father in Madrid and at the Palacio de Santillana del Mar in Santander.
Marriage and issue

Bagrat married Doña María del Carmen de Ulloa y Suelves (b. 6 May 1953) on 12 November 1976 at San Jerónimo el
The couple were divorced on 16 September 2005, and Bagrat remarried in a civil ceremony to Mme.



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
  AssignClass (743995fe-aa9e-4527-82af-fd410a6d5041)
 Call ID: 743995fe-aa9e-4527-82af-fd410a6d5041
  Args:
    source: Prince_Bagrat_Bagration_y_de_Baviera
    type: :Man
  AssignClass (e679d325-a58f-49df-a5cb-413e2a5d527b)
 Call ID: e679d325-a58f-49df-a5cb-413e2a5d527b
  Args:
    type: :Person
    source: Prince_Bagrat_Bagration_y_de_Baviera
  AddLiteral (e4e4cbed-6f79-423d-b3d9-2cb01042e802)
 Call ID: e4e4cbed-6f79-423d-b3d9-2cb01042e802
  Args:
    literal_value: 1949
    source: Prince_Bagrat_Bagration_y_de_Baviera
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (cd1f9782-5e87-4c1f-a698-42e39c6c421c)
 Call ID: cd1f9782-5e87-4c1f-a698-42e39c6c421c
  Args:
    literal_value: 2017
    source: Prince_Bagrat_Bagration_y_de_Baviera
    relation: :hasDeathYear
    literal_type: xsd:integer
  AddLiteral (1d67c87d-52b1-48c8-881e-6e294e7e6924)
 Call ID: 1d67c87d-52b1-48c8-881e-6e294e7e6924
  Args:
    literal_type: xsd:string
    relation: :alsoKnownAs
    literal_value: Prince Bagrat Bagrationi-Mukhraneli
    source: Prince_Bagrat_Bagration_y_de_Baviera
  AddLiteral (85800653-c45a-4922-9535-ab63669a04eb)
 Call ID: 85800653-c45a-4922-9535-ab63669a04eb
  Args:
    source: Prince_Bagrat_Bagration_y_de_Baviera
    literal_value: Prince Bagrat Bagration-Moukhransky
    relation: :alsoKnownAs
    literal_type: xsd:string
  AssignClass (2d0bc9f4-4cd7-4d09-988b-3cdf4883f795)
 Call ID: 2d0bc9f4-4cd7-4d09-988b-3cdf4883f795
  Args:
    source: Prince_Irakli_Bagration_Mukhrani
    type: :Man
  AssignClass (4884afb6-c1ed-4c8c-aabb-c93b631863ba)
 Call ID: 4884afb6-c1ed-4c8c-aabb-c93b631863ba
  Args:
    source: Prince_Irakli_Bagration_Mukhrani
    type: :Person
  AddTriple (5b7fd327-1b7f-4698-a9d6-b2b95b356b4d)
 Call ID: 5b7fd327-1b7f-4698-a9d6-b2b95b356b4d
  Args:
    target: Prince_Irakli_Bagration_Mukhrani
    source: Prince_Bagrat_Bagration_y_de_Baviera
    relation: :hasFather
  AssignClass (fb7fcce7-335e-48fa-957f-e892e89e1545)
 Call ID: fb7fcce7-335e-48fa-957f-e892e89e1545
  Args:
    type: :Woman
    source: Infanta_Doña_María_de_las_Mercedes_de_Baviera_y_Borbón
  AssignClass (6081483f-e339-4757-83db-794f26288833)
 Call ID: 6081483f-e339-4757-83db-794f26288833
  Args:
    source: Infanta_Doña_María_de_las_Mercedes_de_Baviera_y_Borbón
    type: :Person
  AddTriple (a45a2a50-deec-4ab4-859c-3adb4f049b9f)
 Call ID: a45a2a50-deec-4ab4-859c-3adb4f049b9f
  Args:
    source: Prince_Bagrat_Bagration_y_de_Baviera
    target: Infanta_Doña_María_de_las_Mercedes_de_Baviera_y_Borbón
    relation: :hasMother
  AssignClass (6eeef418-58ff-4f41-b143-81a3c4d6fc1d)
 Call ID: 6eeef418-58ff-4f41-b143-81a3c4d6fc1d
  Args:
    source: King_Alfonso_XIII_of_Spain
    type: :Man
  AssignClass (6f82511a-5c81-4c8e-9324-f57553ec4ae4)
 Call ID: 6f82511a-5c81-4c8e-9324-f57553ec4ae4
  Args:
    type: :Person
    source: King_Alfonso_XIII_of_Spain
  AssignClass (0fe50db3-76f7-4367-bcf4-b4807c8f2fac)
 Call ID: 0fe50db3-76f7-4367-bcf4-b4807c8f2fac
  Args:
    source: King_Alfonso_XII
    type: :Man
  AssignClass (6158ebad-4b3b-4580-b529-d58723abe698)
 Call ID: 6158ebad-4b3b-4580-b529-d58723abe698
  Args:
    type: :Person
    source: King_Alfonso_XII
  AssignClass (8c5ff8d9-9d0d-4370-a358-e99c08c1be74)
 Call ID: 8c5ff8d9-9d0d-4370-a358-e99c08c1be74
  Args:
    source: Prince_Jorge_de_Bagration
    type: :Man
  AssignClass (fa550c97-9dbb-4c40-a7e7-6bc52927bed0)
 Call ID: fa550c97-9dbb-4c40-a7e7-6bc52927bed0
  Args:
    source: Prince_Jorge_de_Bagration
    type: :Person
  AddTriple (988545ee-d7b1-44cc-a679-f340b4bb74f2)
 Call ID: 988545ee-d7b1-44cc-a679-f340b4bb74f2
  Args:
    relation: :isBrotherOf
    target: Prince_Bagrat_Bagration_y_de_Baviera
    source: Prince_Jorge_de_Bagration
  AssignClass (fa0673c1-f418-415a-9fe4-8062cdec7def)
 Call ID: fa0673c1-f418-415a-9fe4-8062cdec7def
  Args:
    type: :Woman
    source: Princess_Mariam
  AssignClass (3e6b18cc-d309-4fbb-904b-d1b9263533b5)
 Call ID: 3e6b18cc-d309-4fbb-904b-d1b9263533b5
  Args:
    source: Princess_Mariam
    type: :Person
  AddTriple (d1b63875-9ed0-4fd3-9fd6-a22f13c3422e)
 Call ID: d1b63875-9ed0-4fd3-9fd6-a22f13c3422e
  Args:
    source: Princess_Mariam
    target: Prince_Bagrat_Bagration_y_de_Baviera
    relation: :isSisterOf
  AssignClass (716c5802-99af-437a-b121-d0fe71414eb9)
 Call ID: 716c5802-99af-437a-b121-d0fe71414eb9
  Args:
    source: Doña_María_del_Carmen_de_Ulloa_y_Suelves
    type: :Woman
  AssignClass (29c4fb8d-60b8-4772-90cd-b742db7fb5ff)
 Call ID: 29c4fb8d-60b8-4772-90cd-b742db7fb5ff
  Args:
    source: Doña_María_del_Carmen_de_Ulloa_y_Suelves
    type: :Person
  AddLiteral (e9a0b545-03e1-48a5-948b-bc5bb7662f00)
 Call ID: e9a0b545-03e1-48a5-948b-bc5bb7662f00
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    source: Prince_Bagrat_Bagration_y_de_Baviera
    literal_value: 1976
  Finish (45cda761-77a8-404c-8e66-4b402906cffb)
 Call ID: 45cda761-77a8-404c-8e66-4b402906cffb
  Args: