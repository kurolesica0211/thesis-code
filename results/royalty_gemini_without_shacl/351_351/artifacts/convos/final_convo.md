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
Queen Anne-Marie


Queen Sofía of Spain


Marina, consort of Prince Michael


Prince Nikolaos of Greece and Denmark (Greek: Νικόλαος Ντε Γκρες, romanized: Nikólaos de Grèce; born 1 October 1969) is the third child of Constantine II and Anne-Marie, who were the last King and Queen of Greece, from 1964 to 1973.
Early life and education

Nikolaos was born at Casa di Cura Privata Nuova Villa Claudia in Rome, Italy, on October 1, 1969.
He is the first royal child to be born in hospital from Constantine II of Greece and Anne-Marie of Denmark.
His godparents were Queen Sofía, Queen of Spain (his paternal aunt), Princess Irene of Greece and Denmark (another paternal aunt), Margareta of Romania (his paternal second cousin), and Crown Prince Alexander of Yugoslavia (another paternal second cousin).
He is a member of board of the Anna-Maria Foundation, designed to help victims of natural disasters like floods and earthquakes in Greece.
Nikolaos has an older sister Princess Alexia, an older brother Crown Prince Pavlos, a younger sister Princess Theodora, and a younger brother, Prince Philippos.
Personal life

Relationships

The engagement of Nikolaos to Tatiana Ellinka Blatnik, with whom he had been in a long-term relationship, was announced on 28 December 2009 by the office of King Constantine in London.
On 25 August 2010, the couple married at the Orthodox Church of St. Nicholas in Spetses, Greece.
In January 2025, Nikolaos became engaged to Chrysí Vardinogiánni, daughter of Greek businessman Giórgos Vardinogiánnis and Agapi Politi.
Citizenship

Οn 20 December 2024, Nikolaos along with other members of the former royal family acquired Greek citizenship, under the surname de Grèce.



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
  AssignClass (94588be6-aa7f-4066-9b52-3089197dba40)
 Call ID: 94588be6-aa7f-4066-9b52-3089197dba40
  Args:
    source: :Anne-Marie
    type: :Woman
  AssignClass (13b16cee-15fd-40ee-b912-9badc3ca7ebc)
 Call ID: 13b16cee-15fd-40ee-b912-9badc3ca7ebc
  Args:
    source: :Sofia
    type: :Woman
  AssignClass (f204907a-5ffd-4832-aab4-9cd6fdc3b981)
 Call ID: f204907a-5ffd-4832-aab4-9cd6fdc3b981
  Args:
    source: :Marina
    type: :Woman
  AssignClass (2d86cb64-2619-4493-9119-14619f8f415a)
 Call ID: 2d86cb64-2619-4493-9119-14619f8f415a
  Args:
    type: :Man
    source: :Michael
  AssignClass (3527e681-734b-4e6e-ae26-cd76d06e534b)
 Call ID: 3527e681-734b-4e6e-ae26-cd76d06e534b
  Args:
    source: :Nikolaos
    type: :Man
  AssignClass (d5c41b1b-470c-4e18-badc-d9266e0f551d)
 Call ID: d5c41b1b-470c-4e18-badc-d9266e0f551d
  Args:
    source: :ConstantineII
    type: :Man
  AssignClass (c96d8296-7b5d-4e51-a903-c473d23e9c80)
 Call ID: c96d8296-7b5d-4e51-a903-c473d23e9c80
  Args:
    type: :Woman
    source: :Alexia
  AssignClass (0378efd0-f72e-41af-8391-320ba3e2c193)
 Call ID: 0378efd0-f72e-41af-8391-320ba3e2c193
  Args:
    source: :Pavlos
    type: :Man
  AssignClass (f0424482-7b96-476b-a9e9-398cb299b0e9)
 Call ID: f0424482-7b96-476b-a9e9-398cb299b0e9
  Args:
    source: :Theodora
    type: :Woman
  AssignClass (70028c0c-d0f9-4417-8a42-5ed1d656fe8e)
 Call ID: 70028c0c-d0f9-4417-8a42-5ed1d656fe8e
  Args:
    source: :Philippos
    type: :Man
  AssignClass (d984e21e-c65e-4694-9f20-d4700d0d1d85)
 Call ID: d984e21e-c65e-4694-9f20-d4700d0d1d85
  Args:
    type: :Woman
    source: :TatianaBlatnik
  AssignClass (bc73e5c6-a303-4bdf-971e-e5eb45f32e27)
 Call ID: bc73e5c6-a303-4bdf-971e-e5eb45f32e27
  Args:
    source: :ChrysiVardinogianni
    type: :Woman
  AssignClass (4dab8af8-4d0a-4c47-9cd1-e776876867a2)
 Call ID: 4dab8af8-4d0a-4c47-9cd1-e776876867a2
  Args:
    type: :Man
    source: :GiorgosVardinogiannis
  AssignClass (b9e211ff-7397-4fb7-8f72-72db80cd4fdc)
 Call ID: b9e211ff-7397-4fb7-8f72-72db80cd4fdc
  Args:
    source: :AgapiPoliti
    type: :Woman
  AddLiteral (aa95392a-3df4-4d0b-a7ab-26a2f14a7b47)
 Call ID: aa95392a-3df4-4d0b-a7ab-26a2f14a7b47
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1969
    source: :Nikolaos
  AddTriple (64f86fbb-28cd-4646-a728-4ad980c2696f)
 Call ID: 64f86fbb-28cd-4646-a728-4ad980c2696f
  Args:
    relation: :hasFather
    target: :ConstantineII
    source: :Nikolaos
  AddTriple (1b70fa42-97b8-427e-95a8-d268ed665b82)
 Call ID: 1b70fa42-97b8-427e-95a8-d268ed665b82
  Args:
    source: :Nikolaos
    target: :Anne-Marie
    relation: :hasMother
  AddTriple (3f9e66fa-6c59-476d-abb1-3e3aed38335d)
 Call ID: 3f9e66fa-6c59-476d-abb1-3e3aed38335d
  Args:
    source: :Alexia
    target: :Nikolaos
    relation: :isSisterOf
  AddTriple (5661400b-ea66-4e51-8ca8-96e599761072)
 Call ID: 5661400b-ea66-4e51-8ca8-96e599761072
  Args:
    target: :Nikolaos
    relation: :isBrotherOf
    source: :Pavlos
  AddTriple (be689b55-62ee-41c5-8ad3-169e32abbcd7)
 Call ID: be689b55-62ee-41c5-8ad3-169e32abbcd7
  Args:
    source: :Theodora
    target: :Nikolaos
    relation: :isSisterOf
  AddTriple (e685e38c-5345-441f-aa50-dc3e87074e19)
 Call ID: e685e38c-5345-441f-aa50-dc3e87074e19
  Args:
    relation: :isBrotherOf
    target: :Nikolaos
    source: :Philippos
  AddLiteral (04844a57-3a8e-4e76-be9b-4c86753734e1)
 Call ID: 04844a57-3a8e-4e76-be9b-4c86753734e1
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 2010
    source: :Nikolaos
  AddTriple (c8d244c8-3fcb-4292-bb46-dbc1aa5e44c0)
 Call ID: c8d244c8-3fcb-4292-bb46-dbc1aa5e44c0
  Args:
    source: :Nikolaos
    relation: :hasRelation
    target: :TatianaBlatnik
  AddTriple (08fe0b1c-220f-4add-95fa-6bd3640741f2)
 Call ID: 08fe0b1c-220f-4add-95fa-6bd3640741f2
  Args:
    target: :GiorgosVardinogiannis
    relation: :hasFather
    source: :ChrysiVardinogianni
  AddTriple (7ddb3650-3c12-4cfb-915b-46a005162362)
 Call ID: 7ddb3650-3c12-4cfb-915b-46a005162362
  Args:
    target: :AgapiPoliti
    relation: :hasMother
    source: :ChrysiVardinogianni
  Finish (36a6a928-27e9-40e4-9f2c-1407b4cc2de2)
 Call ID: 36a6a928-27e9-40e4-9f2c-1407b4cc2de2
  Args: