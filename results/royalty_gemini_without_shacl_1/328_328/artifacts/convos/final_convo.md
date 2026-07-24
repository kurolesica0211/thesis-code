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
  AssignClass (c1be7a05-08ec-498f-97f4-f598a9a24ae8)
 Call ID: c1be7a05-08ec-498f-97f4-f598a9a24ae8
  Args:
    source: Prince_Bagrat_de_Bagration_y_de_Baviera
    type: :Man
  AssignClass (7a2e47fd-6038-42d1-bd31-f5d232e10b31)
 Call ID: 7a2e47fd-6038-42d1-bd31-f5d232e10b31
  Args:
    type: :Person
    source: Prince_Bagrat_de_Bagration_y_de_Baviera
  AddLiteral (60bffb4f-0e9d-4d1b-a6f2-5fff04782b6e)
 Call ID: 60bffb4f-0e9d-4d1b-a6f2-5fff04782b6e
  Args:
    relation: :hasBirthYear
    source: Prince_Bagrat_de_Bagration_y_de_Baviera
    literal_value: 1949
    literal_type: xsd:integer
  AddLiteral (8eefbc53-d280-4dc7-89fe-e8070d140bca)
 Call ID: 8eefbc53-d280-4dc7-89fe-e8070d140bca
  Args:
    source: Prince_Bagrat_de_Bagration_y_de_Baviera
    relation: :hasDeathYear
    literal_value: 2017
    literal_type: xsd:integer
  AddLiteral (4f9a5b0e-ea76-4c1d-9899-101ba6e4d331)
 Call ID: 4f9a5b0e-ea76-4c1d-9899-101ba6e4d331
  Args:
    literal_type: xsd:string
    source: Prince_Bagrat_de_Bagration_y_de_Baviera
    relation: :alsoKnownAs
    literal_value: Prince Bagrat Bagrationi-Mukhraneli
  AddLiteral (bed15bbd-2173-41b6-8dff-2f31baf023ab)
 Call ID: bed15bbd-2173-41b6-8dff-2f31baf023ab
  Args:
    literal_value: Prince Bagrat Bagration-Moukhransky
    source: Prince_Bagrat_de_Bagration_y_de_Baviera
    relation: :alsoKnownAs
    literal_type: xsd:string
  AssignClass (2254ff34-e62a-4fbe-9ded-42ebf2f41a8a)
 Call ID: 2254ff34-e62a-4fbe-9ded-42ebf2f41a8a
  Args:
    type: :Man
    source: Prince_Irakli_Bagration-Mukhrani
  AssignClass (45845ee4-edd8-42a3-a1cc-fe27416d912f)
 Call ID: 45845ee4-edd8-42a3-a1cc-fe27416d912f
  Args:
    source: Prince_Irakli_Bagration-Mukhrani
    type: :Person
  AddLiteral (8b5dc86b-d1bf-462d-8667-b68d1a31d10b)
 Call ID: 8b5dc86b-d1bf-462d-8667-b68d1a31d10b
  Args:
    literal_type: xsd:integer
    literal_value: 1909
    relation: :hasBirthYear
    source: Prince_Irakli_Bagration-Mukhrani
  AddLiteral (eddba726-a1b0-4fe8-be85-1dd30a1d5f98)
 Call ID: eddba726-a1b0-4fe8-be85-1dd30a1d5f98
  Args:
    literal_type: xsd:integer
    literal_value: 1977
    source: Prince_Irakli_Bagration-Mukhrani
    relation: :hasDeathYear
  AddTriple (54e7870a-d308-4e87-84de-080f4c152886)
 Call ID: 54e7870a-d308-4e87-84de-080f4c152886
  Args:
    relation: :hasFather
    source: Prince_Bagrat_de_Bagration_y_de_Baviera
    target: Prince_Irakli_Bagration-Mukhrani
  AssignClass (ee52c42b-6fef-48e2-8eb8-4af151eca351)
 Call ID: ee52c42b-6fef-48e2-8eb8-4af151eca351
  Args:
    source: Infanta_Dona_Maria_de_las_Mercedes_de_Baviera_y_Borbon
    type: :Woman
  AssignClass (e43e8f0a-32cd-46f3-815e-e93504f7ef37)
 Call ID: e43e8f0a-32cd-46f3-815e-e93504f7ef37
  Args:
    type: :Person
    source: Infanta_Dona_Maria_de_las_Mercedes_de_Baviera_y_Borbon
  AddLiteral (c1510a93-cd71-4264-b1ed-d7fab2003e36)
 Call ID: c1510a93-cd71-4264-b1ed-d7fab2003e36
  Args:
    literal_value: 1911
    source: Infanta_Dona_Maria_de_las_Mercedes_de_Baviera_y_Borbon
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (573b4559-323d-4a04-b332-42c1b06a4b5b)
 Call ID: 573b4559-323d-4a04-b332-42c1b06a4b5b
  Args:
    literal_type: xsd:integer
    literal_value: 1953
    source: Infanta_Dona_Maria_de_las_Mercedes_de_Baviera_y_Borbon
    relation: :hasDeathYear
  AddTriple (b7e95a28-793b-4fbc-a194-01d7c6ee9882)
 Call ID: b7e95a28-793b-4fbc-a194-01d7c6ee9882
  Args:
    target: Infanta_Dona_Maria_de_las_Mercedes_de_Baviera_y_Borbon
    source: Prince_Bagrat_de_Bagration_y_de_Baviera
    relation: :hasMother
  AssignClass (75c4748d-210d-49dd-be9e-0b402af49010)
 Call ID: 75c4748d-210d-49dd-be9e-0b402af49010
  Args:
    type: :Man
    source: Prince_Jorge_de_Bagration
  AssignClass (a799a377-680f-4357-8c90-dc6f3e9e9d45)
 Call ID: a799a377-680f-4357-8c90-dc6f3e9e9d45
  Args:
    type: :Person
    source: Prince_Jorge_de_Bagration
  AddTriple (2ee04fcd-bddd-48ff-9ee4-4844e89283d3)
 Call ID: 2ee04fcd-bddd-48ff-9ee4-4844e89283d3
  Args:
    source: Prince_Jorge_de_Bagration
    relation: :isBrotherOf
    target: Prince_Bagrat_de_Bagration_y_de_Baviera
  AssignClass (63b3dd2f-bbea-4894-8656-861714fc696d)
 Call ID: 63b3dd2f-bbea-4894-8656-861714fc696d
  Args:
    source: Princess_Mariam
    type: :Woman
  AssignClass (a5943a4f-3efb-428f-8442-f26e1ec42efd)
 Call ID: a5943a4f-3efb-428f-8442-f26e1ec42efd
  Args:
    source: Princess_Mariam
    type: :Person
  AddTriple (b5158a41-928a-4ad8-aa64-906409cf644d)
 Call ID: b5158a41-928a-4ad8-aa64-906409cf644d
  Args:
    relation: :isSisterOf
    source: Princess_Mariam
    target: Prince_Bagrat_de_Bagration_y_de_Baviera
  AssignClass (b1bec40c-1e70-402e-9958-439ab6b2e8d6)
 Call ID: b1bec40c-1e70-402e-9958-439ab6b2e8d6
  Args:
    source: Dona_Maria_del_Carmen_de_Ulloa_y_Suelves
    type: :Woman
  AssignClass (1cbac322-c030-4a47-b447-9e61eeac729a)
 Call ID: 1cbac322-c030-4a47-b447-9e61eeac729a
  Args:
    source: Dona_Maria_del_Carmen_de_Ulloa_y_Suelves
    type: :Person
  AddLiteral (5137d1b5-8b7b-45dc-bb30-0f359be89ec1)
 Call ID: 5137d1b5-8b7b-45dc-bb30-0f359be89ec1
  Args:
    literal_type: xsd:integer
    source: Dona_Maria_del_Carmen_de_Ulloa_y_Suelves
    relation: :hasBirthYear
    literal_value: 1953
  AddLiteral (abc7e0a5-de5e-49a4-9851-b80c32e365fb)
 Call ID: abc7e0a5-de5e-49a4-9851-b80c32e365fb
  Args:
    literal_value: 1976
    source: Prince_Bagrat_de_Bagration_y_de_Baviera
    relation: :hasMarriageYear
    literal_type: xsd:integer
  Finish (8a65ecc2-7b91-4dd8-991c-5f612351ae35)
 Call ID: 8a65ecc2-7b91-4dd8-991c-5f612351ae35
  Args: