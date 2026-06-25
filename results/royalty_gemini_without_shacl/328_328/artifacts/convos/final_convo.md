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
  AssignClass (a9a8ec85-9f0b-480c-9814-6569a408c3dc)
 Call ID: a9a8ec85-9f0b-480c-9814-6569a408c3dc
  Args:
    type: :Man
    source: :Bagrat_Bagration_Mukhraneli
  AssignClass (efec5d52-54cd-43aa-b888-7494ccf26b6b)
 Call ID: efec5d52-54cd-43aa-b888-7494ccf26b6b
  Args:
    type: :Person
    source: :Bagrat_Bagration_Mukhraneli
  AddLiteral (99a4845d-81b1-4aa0-b9a0-d701afa38851)
 Call ID: 99a4845d-81b1-4aa0-b9a0-d701afa38851
  Args:
    literal_value: 1949
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: :Bagrat_Bagration_Mukhraneli
  AddLiteral (ffe5bcc3-79fa-4df9-a607-77ddf8754801)
 Call ID: ffe5bcc3-79fa-4df9-a607-77ddf8754801
  Args:
    source: :Bagrat_Bagration_Mukhraneli
    literal_value: 2017
    relation: :hasDeathYear
    literal_type: xsd:integer
  AddLiteral (2604858f-665e-4ef5-99fd-2f88ccbf7145)
 Call ID: 2604858f-665e-4ef5-99fd-2f88ccbf7145
  Args:
    source: :Bagrat_Bagration_Mukhraneli
    literal_value: Prince Bagrat Bagrationi-Mukhraneli
    literal_type: xsd:string
    relation: :alsoKnownAs
  AddLiteral (d3921f53-9059-42df-826c-b7a49062b410)
 Call ID: d3921f53-9059-42df-826c-b7a49062b410
  Args:
    literal_value: Prince Bagrat Bagration-Moukhransky
    relation: :alsoKnownAs
    literal_type: xsd:string
    source: :Bagrat_Bagration_Mukhraneli
  AssignClass (98492c30-e6f1-4bf6-8f5a-b572d8c76377)
 Call ID: 98492c30-e6f1-4bf6-8f5a-b572d8c76377
  Args:
    source: :Irakli_Bagration_Mukhrani
    type: :Man
  AssignClass (c38e60c4-ce47-4909-9c7d-6aceb9ea9739)
 Call ID: c38e60c4-ce47-4909-9c7d-6aceb9ea9739
  Args:
    type: :Person
    source: :Irakli_Bagration_Mukhrani
  AddTriple (a7961147-5a9f-4b55-b870-56f97d9eac03)
 Call ID: a7961147-5a9f-4b55-b870-56f97d9eac03
  Args:
    source: :Irakli_Bagration_Mukhrani
    target: :Bagrat_Bagration_Mukhraneli
    relation: :isFatherOf
  AssignClass (9895e8bc-0070-49f8-b6ec-30e28dfa6c5b)
 Call ID: 9895e8bc-0070-49f8-b6ec-30e28dfa6c5b
  Args:
    source: :Maria_de_las_Mercedes_de_Baviera_y_Borbon
    type: :Woman
  AssignClass (1fd54a59-eee7-46ff-acb1-fa4f0bf50c80)
 Call ID: 1fd54a59-eee7-46ff-acb1-fa4f0bf50c80
  Args:
    source: :Maria_de_las_Mercedes_de_Baviera_y_Borbon
    type: :Person
  AddTriple (b8495b29-10af-4aba-895c-ffa9be1ffc3b)
 Call ID: b8495b29-10af-4aba-895c-ffa9be1ffc3b
  Args:
    relation: :isMotherOf
    source: :Maria_de_las_Mercedes_de_Baviera_y_Borbon
    target: :Bagrat_Bagration_Mukhraneli
  AssignClass (93cc84fd-f6a2-4b95-8b49-714b91e0e950)
 Call ID: 93cc84fd-f6a2-4b95-8b49-714b91e0e950
  Args:
    type: :Man
    source: :Jorge_de_Bagration
  AssignClass (6c727edd-aeaa-4388-a851-ffb9a757d7a0)
 Call ID: 6c727edd-aeaa-4388-a851-ffb9a757d7a0
  Args:
    source: :Jorge_de_Bagration
    type: :Person
  AddTriple (00bd8d79-2b5f-4a9f-8827-780c05f5c3f9)
 Call ID: 00bd8d79-2b5f-4a9f-8827-780c05f5c3f9
  Args:
    relation: :isBrotherOf
    source: :Jorge_de_Bagration
    target: :Bagrat_Bagration_Mukhraneli
  AssignClass (10c1b3f1-215e-456b-99aa-ee04dfaaf0d3)
 Call ID: 10c1b3f1-215e-456b-99aa-ee04dfaaf0d3
  Args:
    source: :Princess_Mariam
    type: :Woman
  AssignClass (4b78ad56-c9ae-4cbb-ad97-a531cdc396d2)
 Call ID: 4b78ad56-c9ae-4cbb-ad97-a531cdc396d2
  Args:
    type: :Person
    source: :Princess_Mariam
  AddTriple (46120eee-9811-4164-b320-30c52b9134a2)
 Call ID: 46120eee-9811-4164-b320-30c52b9134a2
  Args:
    relation: :isSisterOf
    source: :Princess_Mariam
    target: :Bagrat_Bagration_Mukhraneli
  AssignClass (dc2590a5-c2e4-427a-a25e-2f7e4db74b9a)
 Call ID: dc2590a5-c2e4-427a-a25e-2f7e4db74b9a
  Args:
    type: :Woman
    source: :Maria_del_Carmen_de_Ulloa_y_Suelves
  AssignClass (8fe0d8b7-ab42-4eda-987e-aeeb06e8e604)
 Call ID: 8fe0d8b7-ab42-4eda-987e-aeeb06e8e604
  Args:
    type: :Person
    source: :Maria_del_Carmen_de_Ulloa_y_Suelves
  AddLiteral (a9f3bfb5-fff1-4031-83f0-a2101fed3f79)
 Call ID: a9f3bfb5-fff1-4031-83f0-a2101fed3f79
  Args:
    source: :Bagrat_Bagration_Mukhraneli
    literal_value: 1976
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AddTriple (b0be0204-d53c-42e7-8105-d26f4e3a39ea)
 Call ID: b0be0204-d53c-42e7-8105-d26f4e3a39ea
  Args:
    relation: :hasRelation
    target: :Maria_del_Carmen_de_Ulloa_y_Suelves
    source: :Bagrat_Bagration_Mukhraneli
  Finish (08830490-4b0b-4a67-b092-50c77c839f4f)
 Call ID: 08830490-4b0b-4a67-b092-50c77c839f4f
  Args: