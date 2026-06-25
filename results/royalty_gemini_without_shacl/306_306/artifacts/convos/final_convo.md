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
Alexander Edgar Lascelles, Viscount Lascelles (born 13 May 1980) is an English chef, and the third child and second son of David Lascelles, 8th Earl of Harewood, and his first wife Margaret, Viscountess Lascelles.
He is heir apparent to the earldom of Harewood, due to his elder brother having been born before their parents' marriage.
A chef, Lascelles has also taught about food at the John of Gaunt School, Trowbridge.
Personal life

Lascelles has a son, Leo (b. 2008), with his former girlfriend, Laleh Yeganegy.
Lascelles has a daughter, Ivy, and a son, Kit, with his wife Annika Reed (m. 2017), born in 2018 and 2023, respectively.



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
  AssignClass (80d8666a-6c5c-4edb-9cbf-dbda435a8430)
 Call ID: 80d8666a-6c5c-4edb-9cbf-dbda435a8430
  Args:
    source: Alexander_Edgar_Lascelles
    type: :Man
  AssignClass (35d72c3e-6e00-4338-bc67-2436bdaead04)
 Call ID: 35d72c3e-6e00-4338-bc67-2436bdaead04
  Args:
    source: Alexander_Edgar_Lascelles
    type: :Person
  AddLiteral (31a5a0c5-093c-4431-ab05-dc4a8b230d18)
 Call ID: 31a5a0c5-093c-4431-ab05-dc4a8b230d18
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1980
    source: Alexander_Edgar_Lascelles
  AssignClass (796eda42-e4da-476f-a9a1-29810f942abe)
 Call ID: 796eda42-e4da-476f-a9a1-29810f942abe
  Args:
    source: David_Lascelles
    type: :Man
  AssignClass (fe3a9a03-a745-4375-af28-d15c94b64fc0)
 Call ID: fe3a9a03-a745-4375-af28-d15c94b64fc0
  Args:
    source: David_Lascelles
    type: :Person
  AssignClass (dc23bcef-674e-4f7d-8d63-1f697649aed8)
 Call ID: dc23bcef-674e-4f7d-8d63-1f697649aed8
  Args:
    source: Margaret_Lascelles
    type: :Woman
  AssignClass (77c8cb98-754a-4e7b-8ebc-fe2e0e0eaaad)
 Call ID: 77c8cb98-754a-4e7b-8ebc-fe2e0e0eaaad
  Args:
    source: Margaret_Lascelles
    type: :Person
  AddTriple (45892671-b62c-44fb-8719-2bd533f3e278)
 Call ID: 45892671-b62c-44fb-8719-2bd533f3e278
  Args:
    relation: :hasFather
    target: David_Lascelles
    source: Alexander_Edgar_Lascelles
  AddTriple (d82188d3-2bb3-4cb7-af4d-09ab13dd5fae)
 Call ID: d82188d3-2bb3-4cb7-af4d-09ab13dd5fae
  Args:
    source: Alexander_Edgar_Lascelles
    relation: :hasMother
    target: Margaret_Lascelles
  AssignClass (3aa2814f-ba55-4615-86c8-29956f71f7ff)
 Call ID: 3aa2814f-ba55-4615-86c8-29956f71f7ff
  Args:
    source: Leo_Lascelles
    type: :Man
  AssignClass (95a61201-13ce-4f79-a3cf-14a9534d908e)
 Call ID: 95a61201-13ce-4f79-a3cf-14a9534d908e
  Args:
    source: Leo_Lascelles
    type: :Person
  AddLiteral (9ffb85bb-d60e-4f17-9ef1-0d5937679eb1)
 Call ID: 9ffb85bb-d60e-4f17-9ef1-0d5937679eb1
  Args:
    relation: :hasBirthYear
    literal_value: 2008
    literal_type: xsd:integer
    source: Leo_Lascelles
  AddTriple (5a9e0905-970e-4a90-b196-1f4516768f4e)
 Call ID: 5a9e0905-970e-4a90-b196-1f4516768f4e
  Args:
    source: Leo_Lascelles
    target: Alexander_Edgar_Lascelles
    relation: :hasFather
  AssignClass (384a664c-bf40-45a1-977e-0e358c4fa406)
 Call ID: 384a664c-bf40-45a1-977e-0e358c4fa406
  Args:
    source: Laleh_Yeganegy
    type: :Woman
  AssignClass (5824c6aa-a770-4f54-aaf9-39cdbd5245b8)
 Call ID: 5824c6aa-a770-4f54-aaf9-39cdbd5245b8
  Args:
    source: Laleh_Yeganegy
    type: :Person
  AddTriple (99e86bed-7975-4379-9ab6-3e2b8aec56af)
 Call ID: 99e86bed-7975-4379-9ab6-3e2b8aec56af
  Args:
    relation: :hasMother
    target: Laleh_Yeganegy
    source: Leo_Lascelles
  AssignClass (7c3baab7-04f8-452c-b31e-72d4bc48093e)
 Call ID: 7c3baab7-04f8-452c-b31e-72d4bc48093e
  Args:
    source: Ivy_Lascelles
    type: :Woman
  AssignClass (6aa35bf5-e9f3-409e-8d83-a3dc2dc299a1)
 Call ID: 6aa35bf5-e9f3-409e-8d83-a3dc2dc299a1
  Args:
    source: Ivy_Lascelles
    type: :Person
  AddLiteral (afbc2b40-80b9-4f93-8de2-eda0283f9be8)
 Call ID: afbc2b40-80b9-4f93-8de2-eda0283f9be8
  Args:
    source: Ivy_Lascelles
    relation: :hasBirthYear
    literal_value: 2018
    literal_type: xsd:integer
  AddTriple (faf993b8-afd4-4ec6-8af5-4d0783facdc2)
 Call ID: faf993b8-afd4-4ec6-8af5-4d0783facdc2
  Args:
    source: Ivy_Lascelles
    target: Alexander_Edgar_Lascelles
    relation: :hasFather
  AssignClass (6bbdcdc3-d5a8-4f6e-8315-7bbd8fcfa17c)
 Call ID: 6bbdcdc3-d5a8-4f6e-8315-7bbd8fcfa17c
  Args:
    source: Kit_Lascelles
    type: :Man
  AssignClass (193da5f7-ef95-4df2-b2a5-0106226730e7)
 Call ID: 193da5f7-ef95-4df2-b2a5-0106226730e7
  Args:
    source: Kit_Lascelles
    type: :Person
  AddLiteral (17d74db3-d8e9-44b4-a399-d71d1c3f78c4)
 Call ID: 17d74db3-d8e9-44b4-a399-d71d1c3f78c4
  Args:
    literal_type: xsd:integer
    literal_value: 2023
    relation: :hasBirthYear
    source: Kit_Lascelles
  AddTriple (3211c3c1-d7c1-43a7-96f7-5e7a3f4c0abc)
 Call ID: 3211c3c1-d7c1-43a7-96f7-5e7a3f4c0abc
  Args:
    source: Kit_Lascelles
    relation: :hasFather
    target: Alexander_Edgar_Lascelles
  AssignClass (f8cd0058-9bb4-4846-bce5-d6ba6d130096)
 Call ID: f8cd0058-9bb4-4846-bce5-d6ba6d130096
  Args:
    source: Annika_Reed
    type: :Woman
  AssignClass (8427433b-4b58-417c-b5ec-b1036ae974bf)
 Call ID: 8427433b-4b58-417c-b5ec-b1036ae974bf
  Args:
    source: Annika_Reed
    type: :Person
  AddTriple (10d28436-1627-4e53-a09f-6b3cb27afbfa)
 Call ID: 10d28436-1627-4e53-a09f-6b3cb27afbfa
  Args:
    source: Ivy_Lascelles
    target: Annika_Reed
    relation: :hasMother
  AddTriple (95bedd07-2713-444c-9c4e-4ef0b6204cc9)
 Call ID: 95bedd07-2713-444c-9c4e-4ef0b6204cc9
  Args:
    source: Kit_Lascelles
    relation: :hasMother
    target: Annika_Reed
  AddLiteral (c58021a3-980b-43b9-b331-040563544a8b)
 Call ID: c58021a3-980b-43b9-b331-040563544a8b
  Args:
    source: Alexander_Edgar_Lascelles
    literal_type: xsd:integer
    literal_value: 2017
    relation: :hasMarriageYear
  Finish (bdcb1e5b-fb7a-4bea-b39c-8986b07f4df9)
 Call ID: bdcb1e5b-fb7a-4bea-b39c-8986b07f4df9
  Args: