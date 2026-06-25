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
Princess Beatrix*


Princess Margriet*Pieter van Vollenhoven*


Prince Constantijn of the Netherlands (Constantijn Christof Frederik Aschwin; born 11 October 1969) is the third and youngest son of the former Dutch queen, Beatrix, and her husband, Claus von Amsberg, and is the younger brother of the reigning Dutch king, Willem-Alexander.
Life and career

Prince Constantijn was born on 11 October 1969 at  Academic Hospital Utrecht (now the University Medical Center Utrecht) in Utrecht following the births of his brothers, Willem-Alexander (b. 1967), and Johan Friso (1968–2013).
His godparents are former King Constantine II of Greece (1940–2023), Prince Aschwin of Lippe-Biesterfeld, Axel Freiherr von dem Bussche-Streithorst, Max Kohnstamm, and Corinne de Beaufort-Sickinghe.
Prince Constantijn studied law at Leiden University, becoming a lawyer, and then worked at the Brussels department of the (Dutch) European Union commissioner of foreign relations, Hans van den Broek.
Furthermore, he has a part-time position at the Netherlands Ministry of Foreign Affairs in The Hague.
Prince Constantijn rarely attends public events in his capacity as a member of the Dutch royal family.
Marriage and family

The engagement of Prince Constantijn and Petra Laurentien Brinkhorst was announced on 16 December 2000.
Prince Constantijn and Princess Laurentien have three children: Eloise (b. 2002), Claus-Casimir (b. 2004), and Leonore (b. 2006).
Upon the abdication of Queen Beatrix on 30 April 2013, the children of Prince Constantijn and Princess Laurentien ceased to be members of the Royal House, although they continue to be members of the royal family and remain in the line of succession.
Honours and arms

National

Foreign

Arms

Ancestry

References

External links

2 gave up the title "Prince of the Netherlands, but still held the title "Prince of Orange-Nassau"
3 title granted by Royal Decree to descendants of Princess Irene



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
  AssignClass (da275520-9844-4396-ba24-6816c9f82c02)
 Call ID: da275520-9844-4396-ba24-6816c9f82c02
  Args:
    source: Beatrix
    type: :Woman
  AssignClass (8e91bb76-365c-4e42-ba4e-5cdf7f7a4dd3)
 Call ID: 8e91bb76-365c-4e42-ba4e-5cdf7f7a4dd3
  Args:
    source: Beatrix
    type: :Person
  AssignClass (02bc7a3b-1b33-4538-aff3-f34d4c61ff67)
 Call ID: 02bc7a3b-1b33-4538-aff3-f34d4c61ff67
  Args:
    source: Claus_von_Amsberg
    type: :Man
  AssignClass (34c55d08-05d9-4ad9-8d51-74f11fe38202)
 Call ID: 34c55d08-05d9-4ad9-8d51-74f11fe38202
  Args:
    source: Claus_von_Amsberg
    type: :Person
  AssignClass (98d45cb4-7104-4522-817b-6841355ca2e6)
 Call ID: 98d45cb4-7104-4522-817b-6841355ca2e6
  Args:
    source: Constantijn
    type: :Man
  AssignClass (ba84d888-b1d4-4ebe-9216-e0cb13d5b51d)
 Call ID: ba84d888-b1d4-4ebe-9216-e0cb13d5b51d
  Args:
    source: Constantijn
    type: :Person
  AddLiteral (58d77a9f-0d1f-471a-918c-a1470a454b30)
 Call ID: 58d77a9f-0d1f-471a-918c-a1470a454b30
  Args:
    relation: :hasBirthYear
    source: Constantijn
    literal_type: xsd:integer
    literal_value: 1969
  AddTriple (b3aa2d39-3d50-4d1c-aca6-cf098520c166)
 Call ID: b3aa2d39-3d50-4d1c-aca6-cf098520c166
  Args:
    relation: :hasFather
    target: Claus_von_Amsberg
    source: Constantijn
  AddTriple (e9cfba8d-b4e0-4870-8aaf-2171c88d2c78)
 Call ID: e9cfba8d-b4e0-4870-8aaf-2171c88d2c78
  Args:
    relation: :hasMother
    target: Beatrix
    source: Constantijn
  AssignClass (a9cf8546-d482-46ee-911c-0ad08ab64be6)
 Call ID: a9cf8546-d482-46ee-911c-0ad08ab64be6
  Args:
    source: Willem-Alexander
    type: :Man
  AssignClass (41b8082e-ea9e-4c7c-8d7a-ba0021b7b166)
 Call ID: 41b8082e-ea9e-4c7c-8d7a-ba0021b7b166
  Args:
    source: Willem-Alexander
    type: :Person
  AddTriple (992cd5e3-6d96-4da8-8e71-75ce9d38be76)
 Call ID: 992cd5e3-6d96-4da8-8e71-75ce9d38be76
  Args:
    target: Willem-Alexander
    source: Constantijn
    relation: :hasBrother
  AssignClass (83335f26-889c-4890-bf34-27c8d0878c10)
 Call ID: 83335f26-889c-4890-bf34-27c8d0878c10
  Args:
    source: Johan_Friso
    type: :Man
  AssignClass (0e40754d-62b4-4587-93b3-6f598391362c)
 Call ID: 0e40754d-62b4-4587-93b3-6f598391362c
  Args:
    source: Johan_Friso
    type: :Person
  AddLiteral (f3798245-9228-4f23-aebd-5f1cbc1bcf54)
 Call ID: f3798245-9228-4f23-aebd-5f1cbc1bcf54
  Args:
    source: Johan_Friso
    relation: :hasBirthYear
    literal_value: 1968
    literal_type: xsd:integer
  AddLiteral (f27a776c-a6f5-4037-afc4-0018af3155fd)
 Call ID: f27a776c-a6f5-4037-afc4-0018af3155fd
  Args:
    relation: :hasDeathYear
    source: Johan_Friso
    literal_type: xsd:integer
    literal_value: 2013
  AddTriple (7dac13b7-a411-44cc-8539-b954a96fa73a)
 Call ID: 7dac13b7-a411-44cc-8539-b954a96fa73a
  Args:
    relation: :hasBrother
    source: Constantijn
    target: Johan_Friso
  AssignClass (b703b5cb-38ad-425b-90b8-559d1e2476a2)
 Call ID: b703b5cb-38ad-425b-90b8-559d1e2476a2
  Args:
    source: Laurentien_Brinkhorst
    type: :Woman
  AssignClass (d413c18f-4469-4abe-a742-7034d3ebc5ab)
 Call ID: d413c18f-4469-4abe-a742-7034d3ebc5ab
  Args:
    source: Laurentien_Brinkhorst
    type: :Person
  AssignClass (4ea82ca6-23f8-4bee-b333-e8cf0f89d74b)
 Call ID: 4ea82ca6-23f8-4bee-b333-e8cf0f89d74b
  Args:
    source: Eloise
    type: :Woman
  AssignClass (efdb3dcf-2366-43f6-a95c-58554d8bf00b)
 Call ID: efdb3dcf-2366-43f6-a95c-58554d8bf00b
  Args:
    source: Eloise
    type: :Person
  AddLiteral (b1f66c69-a7e4-45bb-a2b2-a88b3972624a)
 Call ID: b1f66c69-a7e4-45bb-a2b2-a88b3972624a
  Args:
    literal_value: 2002
    literal_type: xsd:integer
    source: Eloise
    relation: :hasBirthYear
  AddTriple (f9dcdff8-771a-4a7b-838e-c18e9824f2d5)
 Call ID: f9dcdff8-771a-4a7b-838e-c18e9824f2d5
  Args:
    relation: :hasMother
    target: Laurentien_Brinkhorst
    source: Eloise
  AddTriple (a4efb556-3d6e-4e18-a1f5-739dfee0fae7)
 Call ID: a4efb556-3d6e-4e18-a1f5-739dfee0fae7
  Args:
    relation: :hasFather
    source: Eloise
    target: Constantijn
  AssignClass (292cd317-e695-4688-86e8-cedfbe22f7be)
 Call ID: 292cd317-e695-4688-86e8-cedfbe22f7be
  Args:
    source: Claus-Casimir
    type: :Man
  AssignClass (28d2cb76-60dc-47d7-a41d-b0ba03ffa6df)
 Call ID: 28d2cb76-60dc-47d7-a41d-b0ba03ffa6df
  Args:
    source: Claus-Casimir
    type: :Person
  AddLiteral (258e5620-d925-4c59-a5eb-d9e37aa8adfe)
 Call ID: 258e5620-d925-4c59-a5eb-d9e37aa8adfe
  Args:
    literal_type: xsd:integer
    literal_value: 2004
    relation: :hasBirthYear
    source: Claus-Casimir
  AddTriple (d47c9e8b-36b8-4a3e-b6b3-c7f0adc825b1)
 Call ID: d47c9e8b-36b8-4a3e-b6b3-c7f0adc825b1
  Args:
    source: Claus-Casimir
    target: Laurentien_Brinkhorst
    relation: :hasMother
  AddTriple (0518e195-4653-4a21-a4b1-9843af505fbe)
 Call ID: 0518e195-4653-4a21-a4b1-9843af505fbe
  Args:
    relation: :hasFather
    target: Constantijn
    source: Claus-Casimir
  AssignClass (26e7c455-d349-4675-9286-071c6b958157)
 Call ID: 26e7c455-d349-4675-9286-071c6b958157
  Args:
    source: Leonore
    type: :Woman
  AssignClass (d27fd596-2f33-47d9-96b5-7b2f88a48738)
 Call ID: d27fd596-2f33-47d9-96b5-7b2f88a48738
  Args:
    source: Leonore
    type: :Person
  AddLiteral (a1c762bc-659b-40b7-be7c-0fb717923aa7)
 Call ID: a1c762bc-659b-40b7-be7c-0fb717923aa7
  Args:
    literal_type: xsd:integer
    literal_value: 2006
    relation: :hasBirthYear
    source: Leonore
  AddTriple (ea7e3744-98dd-4b0f-a963-09bcf519c0a6)
 Call ID: ea7e3744-98dd-4b0f-a963-09bcf519c0a6
  Args:
    target: Laurentien_Brinkhorst
    source: Leonore
    relation: :hasMother
  AddTriple (2dc02699-e89d-45f0-b9aa-d4fb0701c4ff)
 Call ID: 2dc02699-e89d-45f0-b9aa-d4fb0701c4ff
  Args:
    target: Constantijn
    source: Leonore
    relation: :hasFather
  Finish (49a703ee-55e1-4d9d-ae58-66ef3c31b08a)
 Call ID: 49a703ee-55e1-4d9d-ae58-66ef3c31b08a
  Args: