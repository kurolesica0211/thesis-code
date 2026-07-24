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
  AssignClass (5f197aef-3918-4075-aa0b-052cfc766b70)
 Call ID: 5f197aef-3918-4075-aa0b-052cfc766b70
  Args:
    source: Princess_Maria_de_las_Mercedes_of_Bavaria
    type: :Woman
  AssignClass (13addfeb-fbcf-4b14-a00e-a580f7e07107)
 Call ID: 13addfeb-fbcf-4b14-a00e-a580f7e07107
  Args:
    type: :Person
    source: Princess_Maria_de_las_Mercedes_of_Bavaria
  AddLiteral (c7e48e33-9f53-4c49-966c-85402dc56729)
 Call ID: c7e48e33-9f53-4c49-966c-85402dc56729
  Args:
    source: Princess_Maria_de_las_Mercedes_of_Bavaria
    relation: :hasBirthYear
    literal_value: 1911
    literal_type: xsd:integer
  AddLiteral (b42ef2f7-91a7-4947-af1b-38101861c163)
 Call ID: b42ef2f7-91a7-4947-af1b-38101861c163
  Args:
    literal_type: xsd:integer
    source: Princess_Maria_de_las_Mercedes_of_Bavaria
    relation: :hasDeathYear
    literal_value: 1953
  AssignClass (721049d9-a7bf-46e2-b248-b252e45931b1)
 Call ID: 721049d9-a7bf-46e2-b248-b252e45931b1
  Args:
    source: Prince_Irakli_Bagration_of_Mukhrani
    type: :Man
  AssignClass (246daea5-9a5d-428f-bd92-97195dbd7441)
 Call ID: 246daea5-9a5d-428f-bd92-97195dbd7441
  Args:
    source: Prince_Irakli_Bagration_of_Mukhrani
    type: :Person
  AddLiteral (5007fce6-58a6-4d79-afcd-4161ad34e971)
 Call ID: 5007fce6-58a6-4d79-afcd-4161ad34e971
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    source: Princess_Maria_de_las_Mercedes_of_Bavaria
    literal_value: 1946
  AddTriple (0deae3c0-248e-40f3-afe5-3ea4033ebb1f)
 Call ID: 0deae3c0-248e-40f3-afe5-3ea4033ebb1f
  Args:
    target: Prince_Irakli_Bagration_of_Mukhrani
    relation: :hasRelation
    source: Princess_Maria_de_las_Mercedes_of_Bavaria
  AssignClass (5ba26a0c-5cee-46f4-804c-3c0aac405ede)
 Call ID: 5ba26a0c-5cee-46f4-804c-3c0aac405ede
  Args:
    source: Prince_Ferdinand_of_Bavaria
    type: :Man
  AssignClass (d2bedb89-278b-460b-861a-27dc6992de45)
 Call ID: d2bedb89-278b-460b-861a-27dc6992de45
  Args:
    source: Prince_Ferdinand_of_Bavaria
    type: :Person
  AssignClass (f5efed7d-7adf-4033-a0db-dd7f9cfa7b62)
 Call ID: f5efed7d-7adf-4033-a0db-dd7f9cfa7b62
  Args:
    type: :Woman
    source: Infanta_Maria_Teresa_of_Spain
  AssignClass (4f128881-a101-4e29-aeff-6aefd1420f3c)
 Call ID: 4f128881-a101-4e29-aeff-6aefd1420f3c
  Args:
    source: Infanta_Maria_Teresa_of_Spain
    type: :Person
  AddTriple (2209c47a-d088-4ef1-bac2-a4e1436c4e0f)
 Call ID: 2209c47a-d088-4ef1-bac2-a4e1436c4e0f
  Args:
    source: Princess_Maria_de_las_Mercedes_of_Bavaria
    relation: :hasFather
    target: Prince_Ferdinand_of_Bavaria
  AddTriple (003768b8-f425-4ca7-94fd-4fbfe24b1a44)
 Call ID: 003768b8-f425-4ca7-94fd-4fbfe24b1a44
  Args:
    source: Princess_Maria_de_las_Mercedes_of_Bavaria
    relation: :hasMother
    target: Infanta_Maria_Teresa_of_Spain
  AssignClass (d7d894c6-e50d-4509-837d-08e22046e021)
 Call ID: d7d894c6-e50d-4509-837d-08e22046e021
  Args:
    source: Luis_Alfonso
    type: :Man
  AssignClass (b4d49a93-974c-4900-b572-e1b50802f222)
 Call ID: b4d49a93-974c-4900-b572-e1b50802f222
  Args:
    source: Luis_Alfonso
    type: :Person
  AddLiteral (3b4d2b6a-94e0-4c17-8f67-5252e5d20593)
 Call ID: 3b4d2b6a-94e0-4c17-8f67-5252e5d20593
  Args:
    literal_value: 1906
    source: Luis_Alfonso
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (b30caaad-5532-49b3-a734-1c92d858a623)
 Call ID: b30caaad-5532-49b3-a734-1c92d858a623
  Args:
    source: Luis_Alfonso
    relation: :hasDeathYear
    literal_value: 1983
    literal_type: xsd:integer
  AssignClass (dda81162-5302-4b5c-a257-6c7d02f2246a)
 Call ID: dda81162-5302-4b5c-a257-6c7d02f2246a
  Args:
    type: :Man
    source: Jose_Eugenio
  AssignClass (6d8f9020-76fe-4541-8cf7-d2b5ecbbea0b)
 Call ID: 6d8f9020-76fe-4541-8cf7-d2b5ecbbea0b
  Args:
    type: :Person
    source: Jose_Eugenio
  AddLiteral (28f512ee-6fa0-4142-99dc-9247072936af)
 Call ID: 28f512ee-6fa0-4142-99dc-9247072936af
  Args:
    literal_type: xsd:integer
    literal_value: 1909
    source: Jose_Eugenio
    relation: :hasBirthYear
  AddLiteral (3e93862d-5a02-40ac-803c-c42e85a9e6d5)
 Call ID: 3e93862d-5a02-40ac-803c-c42e85a9e6d5
  Args:
    literal_type: xsd:integer
    literal_value: 1966
    source: Jose_Eugenio
    relation: :hasDeathYear
  AssignClass (17ccfc1d-06d3-4684-aa26-03548cc57235)
 Call ID: 17ccfc1d-06d3-4684-aa26-03548cc57235
  Args:
    source: Maria_del_Pilar
    type: :Woman
  AssignClass (cd8c9dca-9e11-4a45-a9b2-ddc8807ec9ed)
 Call ID: cd8c9dca-9e11-4a45-a9b2-ddc8807ec9ed
  Args:
    type: :Person
    source: Maria_del_Pilar
  AddLiteral (61e43f4a-e9b8-49a0-99c7-6552f04d4576)
 Call ID: 61e43f4a-e9b8-49a0-99c7-6552f04d4576
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Maria_del_Pilar
    literal_value: 1912
  AddLiteral (e4763f32-64ae-43ca-86a3-090797c7d17d)
 Call ID: e4763f32-64ae-43ca-86a3-090797c7d17d
  Args:
    literal_type: xsd:integer
    literal_value: 1918
    relation: :hasDeathYear
    source: Maria_del_Pilar
  AddTriple (331612ef-53b9-411f-984e-27fdd1597e0d)
 Call ID: 331612ef-53b9-411f-984e-27fdd1597e0d
  Args:
    relation: :hasBrother
    source: Princess_Maria_de_las_Mercedes_of_Bavaria
    target: Luis_Alfonso
  AddTriple (fa16a1f8-97a4-4b8c-92a9-794b0c533be7)
 Call ID: fa16a1f8-97a4-4b8c-92a9-794b0c533be7
  Args:
    relation: :hasBrother
    source: Princess_Maria_de_las_Mercedes_of_Bavaria
    target: Jose_Eugenio
  AddTriple (358f420b-26fd-4a01-84d2-b483ff673248)
 Call ID: 358f420b-26fd-4a01-84d2-b483ff673248
  Args:
    relation: :hasSister
    source: Princess_Maria_de_las_Mercedes_of_Bavaria
    target: Maria_del_Pilar
  AssignClass (36cc1f14-8c58-448b-b9e6-c01bc5ae42ec)
 Call ID: 36cc1f14-8c58-448b-b9e6-c01bc5ae42ec
  Args:
    type: :Man
    source: Alfonso_XII
  AssignClass (c65e9dae-606b-4d00-b092-b9f1cfa160c8)
 Call ID: c65e9dae-606b-4d00-b092-b9f1cfa160c8
  Args:
    type: :Person
    source: Alfonso_XII
  AssignClass (9e22bcfe-9053-408d-85a5-40b977ccca59)
 Call ID: 9e22bcfe-9053-408d-85a5-40b977ccca59
  Args:
    type: :Man
    source: Alfonso_XIII
  AssignClass (d4fd9244-cac8-45f5-ae7d-d7197f009065)
 Call ID: d4fd9244-cac8-45f5-ae7d-d7197f009065
  Args:
    source: Alfonso_XIII
    type: :Person
  AssignClass (db5b35ac-bef3-42e6-9af3-fcaebf56f10f)
 Call ID: db5b35ac-bef3-42e6-9af3-fcaebf56f10f
  Args:
    source: Isabella_II_of_Spain
    type: :Woman
  AssignClass (0771eecd-d655-41d7-83ed-0913d3720d15)
 Call ID: 0771eecd-d655-41d7-83ed-0913d3720d15
  Args:
    source: Isabella_II_of_Spain
    type: :Person
  AssignClass (342b05b3-a302-46db-9a00-626acf568165)
 Call ID: 342b05b3-a302-46db-9a00-626acf568165
  Args:
    source: Infanta_Maria_de_la_Paz_of_Spain
    type: :Woman
  AssignClass (cbd96a9d-80d1-48bd-ba30-287339d20623)
 Call ID: cbd96a9d-80d1-48bd-ba30-287339d20623
  Args:
    type: :Person
    source: Infanta_Maria_de_la_Paz_of_Spain
  AssignClass (d0644a4f-477c-4c3e-902f-a5e59ecc8eb6)
 Call ID: d0644a4f-477c-4c3e-902f-a5e59ecc8eb6
  Args:
    type: :Man
    source: Prince_Adalbert_of_Bavaria
  AssignClass (c657e4d0-8ca8-434b-9426-c09eaf82c3be)
 Call ID: c657e4d0-8ca8-434b-9426-c09eaf82c3be
  Args:
    type: :Person
    source: Prince_Adalbert_of_Bavaria
  AssignClass (6784e583-7411-45dd-9770-01a9c8e7b13f)
 Call ID: 6784e583-7411-45dd-9770-01a9c8e7b13f
  Args:
    type: :Man
    source: Prince_Carlos_of_Bourbon_Two_Sicilies
  AssignClass (b73509ba-2ac8-42a9-8000-51a6b68bae62)
 Call ID: b73509ba-2ac8-42a9-8000-51a6b68bae62
  Args:
    type: :Person
    source: Prince_Carlos_of_Bourbon_Two_Sicilies
  AssignClass (ee529f4b-9155-42fa-a1ed-e47f4dcb8728)
 Call ID: ee529f4b-9155-42fa-a1ed-e47f4dcb8728
  Args:
    source: Leonida
    type: :Woman
  AssignClass (b064cea3-620b-4d8c-a516-f54cc5138ae2)
 Call ID: b064cea3-620b-4d8c-a516-f54cc5138ae2
  Args:
    type: :Person
    source: Leonida
  AssignClass (8bdb3ea7-f24b-4b7c-ab9c-9be82f7cf034)
 Call ID: 8bdb3ea7-f24b-4b7c-ab9c-9be82f7cf034
  Args:
    type: :Man
    source: Grand_Duke_Vladimir
  AssignClass (a151cdaa-fbc2-4b62-b814-b4e7e9c1e845)
 Call ID: a151cdaa-fbc2-4b62-b814-b4e7e9c1e845
  Args:
    type: :Person
    source: Grand_Duke_Vladimir
  AddTriple (de939460-c138-4d67-baf0-ee990551c90c)
 Call ID: de939460-c138-4d67-baf0-ee990551c90c
  Args:
    relation: :hasRelation
    source: Leonida
    target: Grand_Duke_Vladimir
  AddTriple (b59ad3d0-b835-40d3-a6ed-b59792da1615)
 Call ID: b59ad3d0-b835-40d3-a6ed-b59792da1615
  Args:
    source: Prince_Irakli_Bagration_of_Mukhrani
    relation: :hasSister
    target: Leonida
  Finish (738763ec-cd84-4cbd-88da-db03be5e5b0a)
 Call ID: 738763ec-cd84-4cbd-88da-db03be5e5b0a
  Args: