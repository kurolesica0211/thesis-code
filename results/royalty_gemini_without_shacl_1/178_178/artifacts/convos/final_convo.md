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
Klaus Felix von Amsberg (German: Klaus Felix Friedrich Leopold Gabriel Archim Julius August von Amsberg; 1 September 1890 – 19 December 1953) was a member of the German Niederer Adel (lower nobility) and father of Prince Claus of the Netherlands.
Early life

He was born at Rehna, Mecklenburg-Schwerin, German Empire (now Mecklenburg-Vorpommern, Germany), the first child of Wilhelm von Amsberg (1856–1929), by his marriage to Elise von Vieregg (1866–1951), member of an old aristocratic family.
Claus was from 1917 the steward of an estate after a failed venture in Africa as a planter.
Marriage

Claus married on 4 September 1924 at Hitzacker to Baroness Gösta von dem Bussche-Haddenhausen (26 January 1902 –
13 June 1996), daughter of Baron Georg von dem Bussche-Haddenhausen (1869–1923) and Baroness Gabriele von dem Bussche-Ippenburg (1877–1973).



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix ns1: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
@prefix ns2: <http://www.w3.org/2003/11/swrl#> .
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

ns1:isRuleEnabled a owl:AnnotationProperty .

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

:x a ns2:Variable .

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

:y a ns2:Variable .

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

[] a ns2:Imp ;
    rdfs:label "infer hasSon" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasBrother" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasSister" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (a45afe12-364e-48f7-a4ff-32ff360cb866)
 Call ID: a45afe12-364e-48f7-a4ff-32ff360cb866
  Args:
    source: Klaus_Felix_von_Amsberg
    type: :Man
  AssignClass (d338abfa-17b5-40d2-866c-1d3c7773ba98)
 Call ID: d338abfa-17b5-40d2-866c-1d3c7773ba98
  Args:
    source: Klaus_Felix_von_Amsberg
    type: :Person
  AddLiteral (922d8688-b92c-49c6-b943-a9d7001da52e)
 Call ID: 922d8688-b92c-49c6-b943-a9d7001da52e
  Args:
    source: Klaus_Felix_von_Amsberg
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1890
  AddLiteral (ac3fb91e-04a0-4bba-9c05-f54f139bb03a)
 Call ID: ac3fb91e-04a0-4bba-9c05-f54f139bb03a
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 1953
    source: Klaus_Felix_von_Amsberg
  AssignClass (c828e6cb-7232-4967-9c2e-b6f782859d2f)
 Call ID: c828e6cb-7232-4967-9c2e-b6f782859d2f
  Args:
    source: Wilhelm_von_Amsberg
    type: :Man
  AssignClass (f0b69139-5421-4461-9387-5dc44d11038d)
 Call ID: f0b69139-5421-4461-9387-5dc44d11038d
  Args:
    source: Wilhelm_von_Amsberg
    type: :Person
  AddLiteral (1cfb6415-1cdf-4d13-9e9b-47792df59d3c)
 Call ID: 1cfb6415-1cdf-4d13-9e9b-47792df59d3c
  Args:
    source: Wilhelm_von_Amsberg
    relation: :hasBirthYear
    literal_value: 1856
    literal_type: xsd:integer
  AddLiteral (d10fb5c7-4bb2-4c5b-8803-1fd0879e212f)
 Call ID: d10fb5c7-4bb2-4c5b-8803-1fd0879e212f
  Args:
    source: Wilhelm_von_Amsberg
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 1929
  AssignClass (aa5ca6f0-7684-4940-86e6-0979aaeeb564)
 Call ID: aa5ca6f0-7684-4940-86e6-0979aaeeb564
  Args:
    source: Elise_von_Vieregg
    type: :Woman
  AssignClass (bd257a51-6d4c-4d04-9deb-4e7f01373b8a)
 Call ID: bd257a51-6d4c-4d04-9deb-4e7f01373b8a
  Args:
    source: Elise_von_Vieregg
    type: :Person
  AddLiteral (b56dd282-d43d-4f47-81b6-6eef4cd45425)
 Call ID: b56dd282-d43d-4f47-81b6-6eef4cd45425
  Args:
    literal_type: xsd:integer
    literal_value: 1866
    relation: :hasBirthYear
    source: Elise_von_Vieregg
  AddLiteral (bea27317-26cf-4da9-8ee8-7ab73ed5b917)
 Call ID: bea27317-26cf-4da9-8ee8-7ab73ed5b917
  Args:
    source: Elise_von_Vieregg
    literal_type: xsd:integer
    literal_value: 1951
    relation: :hasDeathYear
  AddTriple (592ea102-4037-48bf-a1b6-6299c6ed37aa)
 Call ID: 592ea102-4037-48bf-a1b6-6299c6ed37aa
  Args:
    source: Klaus_Felix_von_Amsberg
    target: Wilhelm_von_Amsberg
    relation: :hasFather
  AddTriple (87d97136-7860-4c32-ac11-88481c8a83ae)
 Call ID: 87d97136-7860-4c32-ac11-88481c8a83ae
  Args:
    target: Elise_von_Vieregg
    source: Klaus_Felix_von_Amsberg
    relation: :hasMother
  AssignClass (f549ab6a-80cb-46f9-af23-7b12aa32a260)
 Call ID: f549ab6a-80cb-46f9-af23-7b12aa32a260
  Args:
    type: :Man
    source: Prince_Claus_of_the_Netherlands
  AssignClass (e6dcae19-135f-4f90-8b54-46597ee98463)
 Call ID: e6dcae19-135f-4f90-8b54-46597ee98463
  Args:
    source: Prince_Claus_of_the_Netherlands
    type: :Person
  AddTriple (b108fb4d-8e28-4354-b357-713ef61cb629)
 Call ID: b108fb4d-8e28-4354-b357-713ef61cb629
  Args:
    source: Prince_Claus_of_the_Netherlands
    target: Klaus_Felix_von_Amsberg
    relation: :hasFather
  AssignClass (fe93e3ab-636c-477b-bfda-7b8be10d3934)
 Call ID: fe93e3ab-636c-477b-bfda-7b8be10d3934
  Args:
    source: Gosta_von_dem_Bussche-Haddenhausen
    type: :Woman
  AssignClass (cf447fc5-6aaa-4a4f-84bc-fc51ec9362ce)
 Call ID: cf447fc5-6aaa-4a4f-84bc-fc51ec9362ce
  Args:
    source: Gosta_von_dem_Bussche-Haddenhausen
    type: :Person
  AddLiteral (3742c1a9-31c2-4044-b0bc-c6fea6809e3d)
 Call ID: 3742c1a9-31c2-4044-b0bc-c6fea6809e3d
  Args:
    literal_type: xsd:integer
    literal_value: 1902
    relation: :hasBirthYear
    source: Gosta_von_dem_Bussche-Haddenhausen
  AddLiteral (87f0a971-096f-43cf-bfe4-93a7d0c724da)
 Call ID: 87f0a971-096f-43cf-bfe4-93a7d0c724da
  Args:
    source: Gosta_von_dem_Bussche-Haddenhausen
    literal_type: xsd:integer
    literal_value: 1996
    relation: :hasDeathYear
  AddTriple (3bdbf0e3-67c9-4194-801a-5bf37500651c)
 Call ID: 3bdbf0e3-67c9-4194-801a-5bf37500651c
  Args:
    relation: :hasMarriageYear
    target: Gosta_von_dem_Bussche-Haddenhausen
    source: Klaus_Felix_von_Amsberg
  AddLiteral (56d8272b-c00d-4e57-9036-28141447378a)
 Call ID: 56d8272b-c00d-4e57-9036-28141447378a
  Args:
    literal_type: xsd:integer
    literal_value: 1924
    relation: :hasMarriageYear
    source: Klaus_Felix_von_Amsberg
  AssignClass (1a226315-3a67-4658-890e-512d560f99a3)
 Call ID: 1a226315-3a67-4658-890e-512d560f99a3
  Args:
    type: :Man
    source: Georg_von_dem_Bussche-Haddenhausen
  AssignClass (a40f553b-4097-4ba0-b2fb-c2e4c5f67b10)
 Call ID: a40f553b-4097-4ba0-b2fb-c2e4c5f67b10
  Args:
    source: Georg_von_dem_Bussche-Haddenhausen
    type: :Person
  AddLiteral (859f52ef-1fcf-4f81-9998-7914ba4a8e71)
 Call ID: 859f52ef-1fcf-4f81-9998-7914ba4a8e71
  Args:
    relation: :hasBirthYear
    literal_value: 1869
    literal_type: xsd:integer
    source: Georg_von_dem_Bussche-Haddenhausen
  AddLiteral (3082e034-3fec-4a78-842d-82e9718eee3e)
 Call ID: 3082e034-3fec-4a78-842d-82e9718eee3e
  Args:
    relation: :hasDeathYear
    literal_value: 1923
    literal_type: xsd:integer
    source: Georg_von_dem_Bussche-Haddenhausen
  AssignClass (aa92c091-b76a-466c-bcd0-fcc3675436ca)
 Call ID: aa92c091-b76a-466c-bcd0-fcc3675436ca
  Args:
    source: Gabriele_von_dem_Bussche-Ippenburg
    type: :Woman
  AssignClass (a6a16a96-61e7-4163-b653-3639eb448b1d)
 Call ID: a6a16a96-61e7-4163-b653-3639eb448b1d
  Args:
    type: :Person
    source: Gabriele_von_dem_Bussche-Ippenburg
  AddLiteral (9b89259c-18cb-4283-8188-2aed4be03e3e)
 Call ID: 9b89259c-18cb-4283-8188-2aed4be03e3e
  Args:
    literal_type: xsd:integer
    literal_value: 1877
    relation: :hasBirthYear
    source: Gabriele_von_dem_Bussche-Ippenburg
  AddLiteral (a6e5cf4d-848b-4098-a90f-e49bc167900e)
 Call ID: a6e5cf4d-848b-4098-a90f-e49bc167900e
  Args:
    relation: :hasDeathYear
    literal_value: 1973
    literal_type: xsd:integer
    source: Gabriele_von_dem_Bussche-Ippenburg
  AddTriple (338783f6-87d3-4fad-baac-42c512309094)
 Call ID: 338783f6-87d3-4fad-baac-42c512309094
  Args:
    relation: :hasFather
    target: Georg_von_dem_Bussche-Haddenhausen
    source: Gosta_von_dem_Bussche-Haddenhausen
  AddTriple (48dfd730-75cc-41d2-8d80-887c92746aa9)
 Call ID: 48dfd730-75cc-41d2-8d80-887c92746aa9
  Args:
    relation: :hasMother
    target: Gabriele_von_dem_Bussche-Ippenburg
    source: Gosta_von_dem_Bussche-Haddenhausen
  Finish (53c22532-882b-4573-9cf9-b3b21237fc5d)
 Call ID: 53c22532-882b-4573-9cf9-b3b21237fc5d
  Args: