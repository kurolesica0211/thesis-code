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
Princess María de las Mercedes of Bavaria, Infanta of Spain (3 October 1911 – 11 September 1953) was a German-Spanish princess.
She was the third wife of Georgian Prince Irakli Bagration of Mukhrani.
Through her father, Prince Ferdinand of Bavaria, she was a member of the Bavarian House of Wittelsbach.
Through her mother, Infanta María Teresa of Spain, she was a granddaughter of Alfonso XII and niece of Alfonso XIII.
Early life

Princess María de las Mercedes of Bavaria, Infanta of Spain, was born on 3 October 1911 at the Palace of the Cuesta de la Vega, Madrid, to Prince Ferdinand of Bavaria and Infanta María Teresa of Spain.
Her parents were first cousins, both grandchildren of Isabella II of Spain.
Prior to her birth, her uncle, King Alfonso XIII, declared that any children born of her parents' marriage would be Infantes or Infantas of Spain.
She was christened María de las Mercedes Teresa María de la
Her godparents were Infanta María de la Paz of Spain (her paternal grandmother) and Prince Adalbert of Bavaria (her paternal uncle, for whom Prince Carlos of Bourbon-Two Sicilies stood proxy).
She had two elder brothers, Luis Alfonso (1906–1983) and José Eugenio (1909–1966), and one younger sister, María del Pilar (1912–1918).
Marriage and issue

On 29 August 1946, Infanta María de las Mercedes married Prince Irakli Bagration of Mukhrani at the Miramar Palace in San Sebastián.
In 1948, Irakli's sister Leonida married Grand Duke Vladimir.



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
  AssignClass (f7f98e57-7033-400f-a334-fe84242ff3f2)
 Call ID: f7f98e57-7033-400f-a334-fe84242ff3f2
  Args:
    type: :Woman
    source: María_de_las_Mercedes_of_Bavaria
  AssignClass (9ec276b3-a8af-440b-8a15-36430a3f0ba0)
 Call ID: 9ec276b3-a8af-440b-8a15-36430a3f0ba0
  Args:
    type: :Person
    source: María_de_las_Mercedes_of_Bavaria
  AddLiteral (cd05220c-4640-4e4b-80a2-c5bc3e4e0037)
 Call ID: cd05220c-4640-4e4b-80a2-c5bc3e4e0037
  Args:
    source: María_de_las_Mercedes_of_Bavaria
    literal_type: xsd:positiveInteger
    literal_value: 1911
    relation: :hasBirthYear
  AddLiteral (8d31fc2e-977f-4916-8404-26c0c2cb4525)
 Call ID: 8d31fc2e-977f-4916-8404-26c0c2cb4525
  Args:
    relation: :hasDeathYear
    literal_value: 1953
    literal_type: xsd:positiveInteger
    source: María_de_las_Mercedes_of_Bavaria
  AssignClass (c96b4439-902f-4dcc-9916-4cf7ee1c1435)
 Call ID: c96b4439-902f-4dcc-9916-4cf7ee1c1435
  Args:
    source: Irakli_Bagration_of_Mukhrani
    type: :Man
  AssignClass (3e7a3b00-f378-4108-bc8c-48f44c05fc60)
 Call ID: 3e7a3b00-f378-4108-bc8c-48f44c05fc60
  Args:
    type: :Person
    source: Irakli_Bagration_of_Mukhrani
  AddTriple (6fba4cc8-3d24-4f1c-9c11-ea181ea9cc88)
 Call ID: 6fba4cc8-3d24-4f1c-9c11-ea181ea9cc88
  Args:
    source: María_de_las_Mercedes_of_Bavaria
    relation: :hasRelation
    target: Irakli_Bagration_of_Mukhrani
  AddLiteral (bb54b8b7-9b5f-4743-aebe-22ec2f1ed684)
 Call ID: bb54b8b7-9b5f-4743-aebe-22ec2f1ed684
  Args:
    literal_value: 1946
    literal_type: xsd:positiveInteger
    relation: :hasMarriageYear
    source: María_de_las_Mercedes_of_Bavaria
  AssignClass (b99096fc-0066-4a57-9623-8de6843d1896)
 Call ID: b99096fc-0066-4a57-9623-8de6843d1896
  Args:
    source: Ferdinand_of_Bavaria
    type: :Man
  AssignClass (3064e4a0-fff4-4c6f-8fbc-d3286fc4dcd4)
 Call ID: 3064e4a0-fff4-4c6f-8fbc-d3286fc4dcd4
  Args:
    type: :Ancestor
    source: Ferdinand_of_Bavaria
  AssignClass (5e80c385-d405-4cab-ae7d-6bc474613fc0)
 Call ID: 5e80c385-d405-4cab-ae7d-6bc474613fc0
  Args:
    source: Ferdinand_of_Bavaria
    type: :Person
  AddTriple (61330fd0-f747-4633-8139-753bb39203f0)
 Call ID: 61330fd0-f747-4633-8139-753bb39203f0
  Args:
    source: María_de_las_Mercedes_of_Bavaria
    target: Ferdinand_of_Bavaria
    relation: :hasFather
  AssignClass (e55475fb-8f47-480d-bd58-419b28c609cd)
 Call ID: e55475fb-8f47-480d-bd58-419b28c609cd
  Args:
    source: María_Teresa_of_Spain
    type: :Woman
  AssignClass (0c849936-cacb-481a-8ed4-3a6deb083b20)
 Call ID: 0c849936-cacb-481a-8ed4-3a6deb083b20
  Args:
    type: :Ancestor
    source: María_Teresa_of_Spain
  AssignClass (0e58bb8d-d6b0-481c-8107-6d6b443ed5fa)
 Call ID: 0e58bb8d-d6b0-481c-8107-6d6b443ed5fa
  Args:
    type: :Person
    source: María_Teresa_of_Spain
  AddTriple (cf8c1dcf-b826-4370-bfa1-96aaab6d625c)
 Call ID: cf8c1dcf-b826-4370-bfa1-96aaab6d625c
  Args:
    relation: :hasMother
    target: María_Teresa_of_Spain
    source: María_de_las_Mercedes_of_Bavaria
  AssignClass (2c05cafb-3753-44d3-817a-7ef0d7ea1c1a)
 Call ID: 2c05cafb-3753-44d3-817a-7ef0d7ea1c1a
  Args:
    source: Luis_Alfonso
    type: :Man
  AssignClass (e6f1a9fe-3b59-4bdd-9dda-e4afea5a6fae)
 Call ID: e6f1a9fe-3b59-4bdd-9dda-e4afea5a6fae
  Args:
    type: :Person
    source: Luis_Alfonso
  AddTriple (446a0faa-3542-4129-81d4-5f3c6db8a2fb)
 Call ID: 446a0faa-3542-4129-81d4-5f3c6db8a2fb
  Args:
    source: María_de_las_Mercedes_of_Bavaria
    target: Luis_Alfonso
    relation: :hasBrother
  AddLiteral (91fc6a2a-5433-41c5-97dc-bc60b4aead1d)
 Call ID: 91fc6a2a-5433-41c5-97dc-bc60b4aead1d
  Args:
    literal_value: 1906
    literal_type: xsd:positiveInteger
    relation: :hasBirthYear
    source: Luis_Alfonso
  AddLiteral (c33d4b66-1092-407a-b578-19e6fc52d657)
 Call ID: c33d4b66-1092-407a-b578-19e6fc52d657
  Args:
    source: Luis_Alfonso
    relation: :hasDeathYear
    literal_type: xsd:positiveInteger
    literal_value: 1983
  AssignClass (bd94b281-ea8c-485f-bc78-caf5ae01845f)
 Call ID: bd94b281-ea8c-485f-bc78-caf5ae01845f
  Args:
    source: José_Eugenio
    type: :Man
  AssignClass (41634c44-cbea-4736-80cc-c3176d10b162)
 Call ID: 41634c44-cbea-4736-80cc-c3176d10b162
  Args:
    source: José_Eugenio
    type: :Person
  AddTriple (e98f8d37-457a-4619-9281-764fedd29257)
 Call ID: e98f8d37-457a-4619-9281-764fedd29257
  Args:
    source: María_de_las_Mercedes_of_Bavaria
    relation: :hasBrother
    target: José_Eugenio
  AddLiteral (7ff95a9e-0e06-412d-840a-06a26b414819)
 Call ID: 7ff95a9e-0e06-412d-840a-06a26b414819
  Args:
    literal_value: 1909
    literal_type: xsd:positiveInteger
    relation: :hasBirthYear
    source: José_Eugenio
  AddLiteral (75114b87-ef91-4aa4-81c9-a78311154bc0)
 Call ID: 75114b87-ef91-4aa4-81c9-a78311154bc0
  Args:
    source: José_Eugenio
    relation: :hasDeathYear
    literal_value: 1966
    literal_type: xsd:positiveInteger
  AssignClass (3e5ce545-1ab6-4e20-9201-754f7b9cb7dc)
 Call ID: 3e5ce545-1ab6-4e20-9201-754f7b9cb7dc
  Args:
    type: :Woman
    source: María_del_Pilar
  AssignClass (e6e1130e-27c2-453d-bd51-e717c30c5e72)
 Call ID: e6e1130e-27c2-453d-bd51-e717c30c5e72
  Args:
    type: :Person
    source: María_del_Pilar
  AddTriple (f8e41ae8-268b-4e8d-812b-fc2d1815bc79)
 Call ID: f8e41ae8-268b-4e8d-812b-fc2d1815bc79
  Args:
    relation: :hasSister
    target: María_del_Pilar
    source: María_de_las_Mercedes_of_Bavaria
  AddLiteral (c81e3e5f-4818-43ed-93ed-41fcba808857)
 Call ID: c81e3e5f-4818-43ed-93ed-41fcba808857
  Args:
    source: María_del_Pilar
    literal_type: xsd:positiveInteger
    literal_value: 1912
    relation: :hasBirthYear
  AddLiteral (f99b7fd6-21cb-4ab6-9ece-7ba9cb6c3cc4)
 Call ID: f99b7fd6-21cb-4ab6-9ece-7ba9cb6c3cc4
  Args:
    source: María_del_Pilar
    relation: :hasDeathYear
    literal_value: 1918
    literal_type: xsd:positiveInteger
  AssignClass (ef17b3a2-9e12-4d51-ac87-b3c503fa99e2)
 Call ID: ef17b3a2-9e12-4d51-ac87-b3c503fa99e2
  Args:
    source: Leonida
    type: :Woman
  AssignClass (8ce0d4c1-a5c6-476c-baf7-97e03bd6b645)
 Call ID: 8ce0d4c1-a5c6-476c-baf7-97e03bd6b645
  Args:
    type: :Person
    source: Leonida
  AddTriple (0df57de8-630b-4fcd-b0cf-d2e5be0fdb21)
 Call ID: 0df57de8-630b-4fcd-b0cf-d2e5be0fdb21
  Args:
    source: Irakli_Bagration_of_Mukhrani
    relation: :hasSister
    target: Leonida
  AssignClass (dc1ee596-8fa8-4640-8f5c-41f262b6178b)
 Call ID: dc1ee596-8fa8-4640-8f5c-41f262b6178b
  Args:
    type: :Man
    source: Vladimir
  AssignClass (29a8919e-6044-4cc0-9e28-470afff3a4a0)
 Call ID: 29a8919e-6044-4cc0-9e28-470afff3a4a0
  Args:
    type: :Person
    source: Vladimir
  AddTriple (ca645626-81af-481f-948a-c89ceb678253)
 Call ID: ca645626-81af-481f-948a-c89ceb678253
  Args:
    target: Vladimir
    relation: :hasRelation
    source: Leonida
  Finish (40de0701-bd5f-42cf-891e-cc4866cac8a5)
 Call ID: 40de0701-bd5f-42cf-891e-cc4866cac8a5
  Args: