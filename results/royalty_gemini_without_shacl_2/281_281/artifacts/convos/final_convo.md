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
  AssignClass (816c1d67-d124-48df-815d-908301dceddb)
 Call ID: 816c1d67-d124-48df-815d-908301dceddb
  Args:
    type: :Woman
    source: Maria_de_las_Mercedes_of_Bavaria
  AssignClass (3565e0b8-8ba1-4708-81a3-ff2e0d78292b)
 Call ID: 3565e0b8-8ba1-4708-81a3-ff2e0d78292b
  Args:
    type: :Person
    source: Maria_de_las_Mercedes_of_Bavaria
  AddLiteral (c5fdfc18-cfa8-4ce2-9ec7-c867950269c4)
 Call ID: c5fdfc18-cfa8-4ce2-9ec7-c867950269c4
  Args:
    relation: :hasBirthYear
    source: Maria_de_las_Mercedes_of_Bavaria
    literal_type: xsd:integer
    literal_value: 1911
  AddLiteral (e05cd9a5-a3fd-462f-b9cf-5d5bc71b8d06)
 Call ID: e05cd9a5-a3fd-462f-b9cf-5d5bc71b8d06
  Args:
    literal_type: xsd:integer
    literal_value: 1953
    relation: :hasDeathYear
    source: Maria_de_las_Mercedes_of_Bavaria
  AssignClass (7015e2a5-9f74-42c5-861b-0734f30743f1)
 Call ID: 7015e2a5-9f74-42c5-861b-0734f30743f1
  Args:
    type: :Man
    source: Irakli_Bagration_of_Mukhrani
  AssignClass (a0065de6-ec2f-4825-b692-22df423b5f07)
 Call ID: a0065de6-ec2f-4825-b692-22df423b5f07
  Args:
    type: :Person
    source: Irakli_Bagration_of_Mukhrani
  AddLiteral (c730cb68-6ae2-4364-84fc-4839389c8676)
 Call ID: c730cb68-6ae2-4364-84fc-4839389c8676
  Args:
    literal_type: xsd:integer
    literal_value: 1946
    relation: :hasMarriageYear
    source: Maria_de_las_Mercedes_of_Bavaria
  AddTriple (06fe6bd9-7d73-48eb-a932-1bac98dc1474)
 Call ID: 06fe6bd9-7d73-48eb-a932-1bac98dc1474
  Args:
    target: Irakli_Bagration_of_Mukhrani
    source: Maria_de_las_Mercedes_of_Bavaria
    relation: :hasRelation
  AssignClass (c1ab814a-f115-4f1c-bf9e-187f216095fc)
 Call ID: c1ab814a-f115-4f1c-bf9e-187f216095fc
  Args:
    type: :Man
    source: Ferdinand_of_Bavaria
  AssignClass (25b6e938-0a51-455b-a57e-0755c0f54fd4)
 Call ID: 25b6e938-0a51-455b-a57e-0755c0f54fd4
  Args:
    type: :Person
    source: Ferdinand_of_Bavaria
  AssignClass (9cbeda7a-fca1-410f-8d36-48ae623554cb)
 Call ID: 9cbeda7a-fca1-410f-8d36-48ae623554cb
  Args:
    type: :Woman
    source: Maria_Teresa_of_Spain
  AssignClass (1194596d-5b87-458f-8887-bec7e44a6e0e)
 Call ID: 1194596d-5b87-458f-8887-bec7e44a6e0e
  Args:
    type: :Person
    source: Maria_Teresa_of_Spain
  AddTriple (25d637e0-5910-4acf-9998-abaafda07180)
 Call ID: 25d637e0-5910-4acf-9998-abaafda07180
  Args:
    source: Maria_de_las_Mercedes_of_Bavaria
    relation: :hasFather
    target: Ferdinand_of_Bavaria
  AddTriple (de0a2f7b-e6c8-4cc7-a395-ca899b386ff2)
 Call ID: de0a2f7b-e6c8-4cc7-a395-ca899b386ff2
  Args:
    relation: :hasMother
    source: Maria_de_las_Mercedes_of_Bavaria
    target: Maria_Teresa_of_Spain
  AssignClass (166b1d92-9e80-4d8b-9da5-c74445839906)
 Call ID: 166b1d92-9e80-4d8b-9da5-c74445839906
  Args:
    type: :Man
    source: Alfonso_XII
  AssignClass (5917e5b5-5bb0-49eb-bf10-6d2a4c6f8d8b)
 Call ID: 5917e5b5-5bb0-49eb-bf10-6d2a4c6f8d8b
  Args:
    type: :Person
    source: Alfonso_XII
  AssignClass (a54d359d-e8a5-4e6b-9262-d3402ec5117a)
 Call ID: a54d359d-e8a5-4e6b-9262-d3402ec5117a
  Args:
    type: :Man
    source: Alfonso_XIII
  AssignClass (e27d311d-09d0-4f89-963f-e977235a2f04)
 Call ID: e27d311d-09d0-4f89-963f-e977235a2f04
  Args:
    type: :Person
    source: Alfonso_XIII
  AssignClass (eb1bc4b9-4cfe-470c-b697-394d44e05af3)
 Call ID: eb1bc4b9-4cfe-470c-b697-394d44e05af3
  Args:
    type: :Woman
    source: Isabella_II_of_Spain
  AssignClass (06cee88d-e25e-4dab-b6c5-915cb659b5fa)
 Call ID: 06cee88d-e25e-4dab-b6c5-915cb659b5fa
  Args:
    type: :Person
    source: Isabella_II_of_Spain
  AssignClass (8b5338fa-4ab3-447c-900e-73fddac9d10c)
 Call ID: 8b5338fa-4ab3-447c-900e-73fddac9d10c
  Args:
    type: :Man
    source: Luis_Alfonso
  AssignClass (75fb60f3-afdb-449e-a0d4-b79f361fd185)
 Call ID: 75fb60f3-afdb-449e-a0d4-b79f361fd185
  Args:
    type: :Person
    source: Luis_Alfonso
  AddLiteral (4106abae-3c59-4883-9872-18879aa0d3bb)
 Call ID: 4106abae-3c59-4883-9872-18879aa0d3bb
  Args:
    source: Luis_Alfonso
    relation: :hasBirthYear
    literal_value: 1906
    literal_type: xsd:integer
  AddLiteral (861414f9-34c1-427f-8c9e-20349cb688dc)
 Call ID: 861414f9-34c1-427f-8c9e-20349cb688dc
  Args:
    relation: :hasDeathYear
    source: Luis_Alfonso
    literal_type: xsd:integer
    literal_value: 1983
  AssignClass (61e63fc8-b291-4a14-a1cb-e7a664c16308)
 Call ID: 61e63fc8-b291-4a14-a1cb-e7a664c16308
  Args:
    type: :Man
    source: Jose_Eugenio
  AssignClass (7606c8a9-b07e-445b-bfb0-657a53c6d2f4)
 Call ID: 7606c8a9-b07e-445b-bfb0-657a53c6d2f4
  Args:
    type: :Person
    source: Jose_Eugenio
  AddLiteral (6da79447-3ef8-4f69-962f-c9a884ce38a0)
 Call ID: 6da79447-3ef8-4f69-962f-c9a884ce38a0
  Args:
    literal_type: xsd:integer
    literal_value: 1909
    relation: :hasBirthYear
    source: Jose_Eugenio
  AddLiteral (7616d5ea-e77d-4bf0-96a6-9eb95a0913d2)
 Call ID: 7616d5ea-e77d-4bf0-96a6-9eb95a0913d2
  Args:
    relation: :hasDeathYear
    source: Jose_Eugenio
    literal_type: xsd:integer
    literal_value: 1966
  AssignClass (697f16ae-30e5-4d5d-905a-7490e751dc39)
 Call ID: 697f16ae-30e5-4d5d-905a-7490e751dc39
  Args:
    type: :Woman
    source: Maria_del_Pilar
  AssignClass (b57330c5-62e6-442f-9239-2c57110b1061)
 Call ID: b57330c5-62e6-442f-9239-2c57110b1061
  Args:
    type: :Person
    source: Maria_del_Pilar
  AddLiteral (28286934-8b5d-48e8-9be6-f2c49f1005aa)
 Call ID: 28286934-8b5d-48e8-9be6-f2c49f1005aa
  Args:
    literal_value: 1912
    literal_type: xsd:integer
    source: Maria_del_Pilar
    relation: :hasBirthYear
  AddLiteral (cee3c363-f4d8-4167-93ed-597af3dd7048)
 Call ID: cee3c363-f4d8-4167-93ed-597af3dd7048
  Args:
    source: Maria_del_Pilar
    relation: :hasDeathYear
    literal_value: 1918
    literal_type: xsd:integer
  AddTriple (9d5dfbef-aac5-4d69-8da9-254ca61663a0)
 Call ID: 9d5dfbef-aac5-4d69-8da9-254ca61663a0
  Args:
    relation: :isSiblingOf
    source: Maria_de_las_Mercedes_of_Bavaria
    target: Luis_Alfonso
  AddTriple (61b3d0ff-459e-4e33-b902-4297078d0c51)
 Call ID: 61b3d0ff-459e-4e33-b902-4297078d0c51
  Args:
    target: Jose_Eugenio
    source: Maria_de_las_Mercedes_of_Bavaria
    relation: :isSiblingOf
  AddTriple (d198cb69-dba7-4308-8ff1-5071fc7a3ca3)
 Call ID: d198cb69-dba7-4308-8ff1-5071fc7a3ca3
  Args:
    relation: :isSiblingOf
    source: Maria_de_las_Mercedes_of_Bavaria
    target: Maria_del_Pilar
  AssignClass (2e79f9f6-9044-4933-b2b6-3acf6b8de448)
 Call ID: 2e79f9f6-9044-4933-b2b6-3acf6b8de448
  Args:
    type: :Woman
    source: Leonida
  AssignClass (0c052351-3140-4d6f-a4ed-9afa60427649)
 Call ID: 0c052351-3140-4d6f-a4ed-9afa60427649
  Args:
    type: :Person
    source: Leonida
  AddTriple (b0946e4f-e93d-4646-bfab-1c5b391d81bd)
 Call ID: b0946e4f-e93d-4646-bfab-1c5b391d81bd
  Args:
    target: Leonida
    source: Irakli_Bagration_of_Mukhrani
    relation: :isSiblingOf
  AssignClass (5dda3ec3-bc87-41db-a2a0-641a1d3aa233)
 Call ID: 5dda3ec3-bc87-41db-a2a0-641a1d3aa233
  Args:
    type: :Man
    source: Vladimir
  AssignClass (9ff11f20-a10c-4d6a-ac88-ef66dc14f47a)
 Call ID: 9ff11f20-a10c-4d6a-ac88-ef66dc14f47a
  Args:
    type: :Person
    source: Vladimir
  AddTriple (23760988-ee5d-4d5b-ba5e-95ed3a8c3a5a)
 Call ID: 23760988-ee5d-4d5b-ba5e-95ed3a8c3a5a
  Args:
    relation: :hasRelation
    source: Leonida
    target: Vladimir
  Finish (0471d827-5007-406d-82af-3ba4fb280ea1)
 Call ID: 0471d827-5007-406d-82af-3ba4fb280ea1
  Args: