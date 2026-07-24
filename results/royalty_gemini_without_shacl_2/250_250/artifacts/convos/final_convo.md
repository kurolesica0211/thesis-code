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
Prince Ludwig Rudolf of Hanover, of Great Britain and Ireland, Duke of Brunswick and Lüneburg (German: Ludwig Rudolf Georg Wilhelm Philipp Friedrich Wolrad Maximilian Prinz von Hannover) (21 November 1955 – 29 November 1988) was a member of the House of Hanover and a music producer.
Early life and career

Ludwig Rudolf was born in Hanover, Lower Saxony, Germany, the third child and second son of Ernst August, Prince of Hanover, Hereditary Prince of Brunswick (1914–1987) and his wife, Princess Ortrud of Schleswig-Holstein-Sonderburg-Glücksburg (1925–1980).
Ludwig Rudolf was a great-great-great-great-grandson of George III of the United Kingdom and a great-grandson of Wilhelm II, German Emperor.
Ludwig Rudolf had trained to become a music producer in Los Angeles and London.
Marriage and death

Having obtained the consent of Elizabeth II by Order in Council on 15 September 1987 pursuant to the Royal Marriages Act 1772, Ludwig Rudolf, a Lutheran, married the Roman Catholic Countess Isabella Maria von Thurn und Valsassina-Como-Vercelli (born September 8 1962 in Gmunden, Upper Austria), a former fashion model at her father's ancestral Austrian estate, Bleiburg Castle, Carinthia on 4 October 1987.
She was the daughter of Count Ariprand von Thurn und Valsassina-Como-Vercelli (1925–1996), whose family, an Austrian branch of the Della Torre dynasty, ruled Milan in the 13th and 14th century, and his wife, Princess Maria Perpetua Euphemia von Auersperg (born 1929).
In the early hours of 29 November 1988, after the couple had entertained guests at their home, Königinvilla (The Queen's Villa) in Gmunden, a house left to them by Ludwig Rudolf's elder brother Ernst August, the prince went to the bedroom where his wife had retired before midnight, and found Isabella sprawled fully dressed across their bed.
Ludwig Rudolf, who had been investigated previously on suspicion of illegal drug purchases, placed a call to his brother, Ernst August, in London, imploring him to take care of the couple's 10-month-old son.
As authorities removed Isabella's body and investigated the scene, discovering syringes, cocaine and heroin, Ludwig Rudolf slipped away.
Hours later, the prince was found in his car near his family's hunting lodge several miles away, on Lake Traun.
Ludwig Rudolf and Isabelle were interred on 2 December 1988 at Grünau
Custody of their infant son Otto Heinrich was awarded, contrary to the expressed wishes of Ludwig Rudolf, to the child's maternal grandparents.
He grew up at their castle, Schloss Bleiburg, in Austria, and then studied art at Braunschweig University of Art in Brunswick (Braunschweig).



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
  AssignClass (c806aa26-f7b2-4941-ad8c-1d4059bd8f54)
 Call ID: c806aa26-f7b2-4941-ad8c-1d4059bd8f54
  Args:
    type: :Man
    source: Ludwig_Rudolf_of_Hanover
  AssignClass (df600586-65b2-4f09-804a-04b597bfbf41)
 Call ID: df600586-65b2-4f09-804a-04b597bfbf41
  Args:
    source: Ludwig_Rudolf_of_Hanover
    type: :Person
  AddLiteral (47f3a2f9-9b9c-4663-a756-73d9dcce7180)
 Call ID: 47f3a2f9-9b9c-4663-a756-73d9dcce7180
  Args:
    source: Ludwig_Rudolf_of_Hanover
    literal_value: 1955
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (435b5857-7bb0-4528-8131-fb5c914bf68b)
 Call ID: 435b5857-7bb0-4528-8131-fb5c914bf68b
  Args:
    literal_value: 1988
    source: Ludwig_Rudolf_of_Hanover
    literal_type: xsd:integer
    relation: :hasDeathYear
  AssignClass (715960c4-bfe6-4015-b108-dadbd25228ba)
 Call ID: 715960c4-bfe6-4015-b108-dadbd25228ba
  Args:
    type: :Man
    source: Ernst_August_Prince_of_Hanover
  AssignClass (b4a8c69d-316c-45a6-8970-031b368d34dc)
 Call ID: b4a8c69d-316c-45a6-8970-031b368d34dc
  Args:
    source: Ernst_August_Prince_of_Hanover
    type: :Person
  AddLiteral (dec6defa-9fa2-4553-ad7a-0eeca4ad8a97)
 Call ID: dec6defa-9fa2-4553-ad7a-0eeca4ad8a97
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1914
    source: Ernst_August_Prince_of_Hanover
  AddLiteral (8eed1ec7-928b-4989-97d6-395f15653694)
 Call ID: 8eed1ec7-928b-4989-97d6-395f15653694
  Args:
    literal_value: 1987
    source: Ernst_August_Prince_of_Hanover
    literal_type: xsd:integer
    relation: :hasDeathYear
  AssignClass (eda6ea18-d1c3-4d4b-9ccf-0469845676fd)
 Call ID: eda6ea18-d1c3-4d4b-9ccf-0469845676fd
  Args:
    source: Ortrud_of_Schleswig-Holstein-Sonderburg-Glücksburg
    type: :Woman
  AssignClass (1546eb89-d087-4bba-9e33-de8e3a0d442f)
 Call ID: 1546eb89-d087-4bba-9e33-de8e3a0d442f
  Args:
    type: :Person
    source: Ortrud_of_Schleswig-Holstein-Sonderburg-Glücksburg
  AddLiteral (7bea8efb-fc91-4626-a543-907fbb9ac349)
 Call ID: 7bea8efb-fc91-4626-a543-907fbb9ac349
  Args:
    source: Ortrud_of_Schleswig-Holstein-Sonderburg-Glücksburg
    literal_value: 1925
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (28e69383-67c9-4dc3-b4ca-7b0568466538)
 Call ID: 28e69383-67c9-4dc3-b4ca-7b0568466538
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1980
    source: Ortrud_of_Schleswig-Holstein-Sonderburg-Glücksburg
  AddTriple (03a0b130-5630-434e-8d1f-cbd0014fc61e)
 Call ID: 03a0b130-5630-434e-8d1f-cbd0014fc61e
  Args:
    relation: :hasFather
    target: Ernst_August_Prince_of_Hanover
    source: Ludwig_Rudolf_of_Hanover
  AddTriple (8b94f689-8574-4553-8ef9-62a89ac08aa1)
 Call ID: 8b94f689-8574-4553-8ef9-62a89ac08aa1
  Args:
    source: Ludwig_Rudolf_of_Hanover
    target: Ortrud_of_Schleswig-Holstein-Sonderburg-Glücksburg
    relation: :hasMother
  AssignClass (5c000f38-40d7-456c-998f-1396a0bcfea5)
 Call ID: 5c000f38-40d7-456c-998f-1396a0bcfea5
  Args:
    source: Isabella_Maria_von_Thurn_und_Valsassina-Como-Vercelli
    type: :Woman
  AssignClass (d47698b8-e4c7-4e29-a7bf-97e74a18d872)
 Call ID: d47698b8-e4c7-4e29-a7bf-97e74a18d872
  Args:
    source: Isabella_Maria_von_Thurn_und_Valsassina-Como-Vercelli
    type: :Person
  AddLiteral (e8af9b9e-144c-4cda-9ae6-60c67b597ed8)
 Call ID: e8af9b9e-144c-4cda-9ae6-60c67b597ed8
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1962
    source: Isabella_Maria_von_Thurn_und_Valsassina-Como-Vercelli
  AddLiteral (2d7d97b4-be84-49ce-b7ce-ccbde69ccc4a)
 Call ID: 2d7d97b4-be84-49ce-b7ce-ccbde69ccc4a
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: Isabella_Maria_von_Thurn_und_Valsassina-Como-Vercelli
    literal_value: 1988
  AddLiteral (1c7498c9-ffd3-4434-813d-5e73dc899e1d)
 Call ID: 1c7498c9-ffd3-4434-813d-5e73dc899e1d
  Args:
    literal_value: 1987
    source: Ludwig_Rudolf_of_Hanover
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AddTriple (38083e23-d785-45ab-ad3e-74fb4227132b)
 Call ID: 38083e23-d785-45ab-ad3e-74fb4227132b
  Args:
    target: Isabella_Maria_von_Thurn_und_Valsassina-Como-Vercelli
    source: Ludwig_Rudolf_of_Hanover
    relation: :hasRelation
  AssignClass (92b353a7-f358-4e3c-a64b-fcffd4ace96a)
 Call ID: 92b353a7-f358-4e3c-a64b-fcffd4ace96a
  Args:
    type: :Man
    source: Ariprand_von_Thurn_und_Valsassina-Como-Vercelli
  AssignClass (615fb541-5b76-4277-9f11-78940d10ed30)
 Call ID: 615fb541-5b76-4277-9f11-78940d10ed30
  Args:
    source: Ariprand_von_Thurn_und_Valsassina-Como-Vercelli
    type: :Person
  AddLiteral (5e3c6bbb-d53e-4fad-b479-48764c421763)
 Call ID: 5e3c6bbb-d53e-4fad-b479-48764c421763
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1925
    source: Ariprand_von_Thurn_und_Valsassina-Como-Vercelli
  AddLiteral (72864585-172b-4763-97ce-a0c455f31573)
 Call ID: 72864585-172b-4763-97ce-a0c455f31573
  Args:
    literal_value: 1996
    source: Ariprand_von_Thurn_und_Valsassina-Como-Vercelli
    literal_type: xsd:integer
    relation: :hasDeathYear
  AssignClass (ede493cf-2af7-48d7-9251-5cadcf96cf8b)
 Call ID: ede493cf-2af7-48d7-9251-5cadcf96cf8b
  Args:
    source: Maria_Perpetua_Euphemia_von_Auersperg
    type: :Woman
  AssignClass (e6c2a4b0-2321-4da1-b1a9-19abc9d6ff70)
 Call ID: e6c2a4b0-2321-4da1-b1a9-19abc9d6ff70
  Args:
    source: Maria_Perpetua_Euphemia_von_Auersperg
    type: :Person
  AddLiteral (53930fed-6642-4233-91cf-62a937ad4b6e)
 Call ID: 53930fed-6642-4233-91cf-62a937ad4b6e
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1929
    source: Maria_Perpetua_Euphemia_von_Auersperg
  AddTriple (7105e0a4-d686-4f17-8629-8e4a60814d65)
 Call ID: 7105e0a4-d686-4f17-8629-8e4a60814d65
  Args:
    relation: :hasFather
    source: Isabella_Maria_von_Thurn_und_Valsassina-Como-Vercelli
    target: Ariprand_von_Thurn_und_Valsassina-Como-Vercelli
  AddTriple (51895d8f-e5e5-46fd-aaa5-71643aa1b5e6)
 Call ID: 51895d8f-e5e5-46fd-aaa5-71643aa1b5e6
  Args:
    source: Isabella_Maria_von_Thurn_und_Valsassina-Como-Vercelli
    target: Maria_Perpetua_Euphemia_von_Auersperg
    relation: :hasMother
  AssignClass (b5d14a32-2b62-466b-89db-dd986ff8fabd)
 Call ID: b5d14a32-2b62-466b-89db-dd986ff8fabd
  Args:
    source: Ernst_August_brother
    type: :Man
  AssignClass (d663c9c7-d244-4bb2-8efc-c090c9df0aa9)
 Call ID: d663c9c7-d244-4bb2-8efc-c090c9df0aa9
  Args:
    type: :Person
    source: Ernst_August_brother
  AddTriple (13c13822-faf8-4f1f-89ce-dfd4aeb42818)
 Call ID: 13c13822-faf8-4f1f-89ce-dfd4aeb42818
  Args:
    target: Ernst_August_brother
    source: Ludwig_Rudolf_of_Hanover
    relation: :isSiblingOf
  AssignClass (b2933026-3fcc-4b40-8f6d-b9537d4a7656)
 Call ID: b2933026-3fcc-4b40-8f6d-b9537d4a7656
  Args:
    source: Otto_Heinrich
    type: :Man
  AssignClass (1b39c463-7822-447a-8579-eb83e8ecfadf)
 Call ID: 1b39c463-7822-447a-8579-eb83e8ecfadf
  Args:
    source: Otto_Heinrich
    type: :Person
  AddTriple (e9ad976a-d8f6-4582-8468-f00f8a985453)
 Call ID: e9ad976a-d8f6-4582-8468-f00f8a985453
  Args:
    relation: :isSonOf
    source: Otto_Heinrich
    target: Ludwig_Rudolf_of_Hanover
  AddTriple (77c04165-2436-4700-b118-f72a2b26c8c4)
 Call ID: 77c04165-2436-4700-b118-f72a2b26c8c4
  Args:
    relation: :isSonOf
    target: Isabella_Maria_von_Thurn_und_Valsassina-Como-Vercelli
    source: Otto_Heinrich
  Finish (336346a8-305b-40ae-a75a-3818966e1864)
 Call ID: 336346a8-305b-40ae-a75a-3818966e1864
  Args: