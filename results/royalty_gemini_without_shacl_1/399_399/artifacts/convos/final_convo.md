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
Georg, Prince of Saxe-Meiningen (11 October 1892 – 6 January 1946) was the head of the house of Saxe-Meiningen from 1941 until his death.
He was born in Kassel as the eldest son of Prince Frederick Johann of Saxe-Meiningen (1861-1914) and Countess Adelaide of Lippe-Biesterfeld (1870–1948).
His father was a son of Georg II, Duke of Saxe-Meiningen and his mother a daughter of Count Ernst of Lippe-Biesterfeld.
Georg studied law at the Universities of Munich and Jena.
Georg suspended his studies to serve in World War I and saw action as a captain in a cavalry regiment.
After the death of his uncle Ernst on 29 December 1941, Georg succeeded to the headship of the house of Saxe-Meiningen and assumed the title of Duke of Saxe-Meiningen and style Georg III.
Georg and his family were expropriated without compensation in 1945.
Georg, who served as a major in the Wehrmacht died in the Russian prisoner of war camp near Cherepovets (Tscherepowetz in German) in Northern Russia.
His heir was his second and only surviving son Prince Frederick Alfred who renounced the succession, being a monk in 1953, allowing it to pass to his uncle Bernhard.
Marriage and children

He was married in Freiburg im Breisgau on 22 February 1919 to Countess Klara Marie von Korff genannt Schmising-Kerssenbrock (Darmstadt, 31 May 1895



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
  AssignClass (3768e62e-a1c6-4374-886f-7d84e5a77e3f)
 Call ID: 3768e62e-a1c6-4374-886f-7d84e5a77e3f
  Args:
    type: :Man
    source: Georg_Prince_of_Saxe-Meiningen
  AssignClass (7f0851b1-258c-4382-86a0-215091f38f9d)
 Call ID: 7f0851b1-258c-4382-86a0-215091f38f9d
  Args:
    type: :Man
    source: Prince_Frederick_Johann_of_Saxe-Meiningen
  AssignClass (e865dd1f-b392-4e1c-ac6c-dd7f9456d4bd)
 Call ID: e865dd1f-b392-4e1c-ac6c-dd7f9456d4bd
  Args:
    source: Countess_Adelaide_of_Lippe-Biesterfeld
    type: :Woman
  AssignClass (22afb56b-166d-4c05-96d7-07fd5a108a19)
 Call ID: 22afb56b-166d-4c05-96d7-07fd5a108a19
  Args:
    source: Georg_II_Duke_of_Saxe-Meiningen
    type: :Man
  AssignClass (626c88d3-3998-4a9d-b367-de27ea22639f)
 Call ID: 626c88d3-3998-4a9d-b367-de27ea22639f
  Args:
    type: :Man
    source: Count_Ernst_of_Lippe-Biesterfeld
  AssignClass (9f86bc7d-f499-41f5-9348-0d8a37e7478d)
 Call ID: 9f86bc7d-f499-41f5-9348-0d8a37e7478d
  Args:
    type: :Man
    source: Prince_Frederick_Alfred
  AssignClass (9557ed7e-79fb-4497-8ee9-02927f5b466f)
 Call ID: 9557ed7e-79fb-4497-8ee9-02927f5b466f
  Args:
    source: Bernhard
    type: :Man
  AssignClass (23927c06-24ea-416b-8b08-784a01f1257a)
 Call ID: 23927c06-24ea-416b-8b08-784a01f1257a
  Args:
    source: Countess_Klara_Marie_von_Korff_genannt_Schmising-Kerssenbrock
    type: :Woman
  AddLiteral (98d9e20c-2399-4a38-a994-8e041eefb409)
 Call ID: 98d9e20c-2399-4a38-a994-8e041eefb409
  Args:
    literal_type: xsd:integer
    literal_value: 1892
    source: Georg_Prince_of_Saxe-Meiningen
    relation: :hasBirthYear
  AddLiteral (626dd0ad-3626-48b3-b8f8-ee7c490b7817)
 Call ID: 626dd0ad-3626-48b3-b8f8-ee7c490b7817
  Args:
    literal_type: xsd:integer
    source: Georg_Prince_of_Saxe-Meiningen
    literal_value: 1946
    relation: :hasDeathYear
  AddLiteral (c9c38d5e-cbdd-41e0-b3b6-e259bf46913c)
 Call ID: c9c38d5e-cbdd-41e0-b3b6-e259bf46913c
  Args:
    relation: :hasBirthYear
    literal_value: 1861
    literal_type: xsd:integer
    source: Prince_Frederick_Johann_of_Saxe-Meiningen
  AddLiteral (dd54c344-0f2b-48f2-bf87-14fc093ca16a)
 Call ID: dd54c344-0f2b-48f2-bf87-14fc093ca16a
  Args:
    source: Prince_Frederick_Johann_of_Saxe-Meiningen
    literal_type: xsd:integer
    literal_value: 1914
    relation: :hasDeathYear
  AddLiteral (d8efd7f1-1aba-4607-a5fc-1cc255ce2d52)
 Call ID: d8efd7f1-1aba-4607-a5fc-1cc255ce2d52
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Countess_Adelaide_of_Lippe-Biesterfeld
    literal_value: 1870
  AddLiteral (e4eccda2-422e-41e8-aea4-9805779a700f)
 Call ID: e4eccda2-422e-41e8-aea4-9805779a700f
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: Countess_Adelaide_of_Lippe-Biesterfeld
    literal_value: 1948
  AddLiteral (efa89de6-79e2-466d-b835-126d8ed08d80)
 Call ID: efa89de6-79e2-466d-b835-126d8ed08d80
  Args:
    relation: :hasMarriageYear
    source: Georg_Prince_of_Saxe-Meiningen
    literal_type: xsd:integer
    literal_value: 1919
  AddTriple (ef5cdb60-df4d-4b40-a860-f176c25a4908)
 Call ID: ef5cdb60-df4d-4b40-a860-f176c25a4908
  Args:
    source: Georg_Prince_of_Saxe-Meiningen
    relation: :hasFather
    target: Prince_Frederick_Johann_of_Saxe-Meiningen
  AddTriple (c673b176-d28d-402d-bb8f-3bc57477642b)
 Call ID: c673b176-d28d-402d-bb8f-3bc57477642b
  Args:
    source: Georg_Prince_of_Saxe-Meiningen
    relation: :hasMother
    target: Countess_Adelaide_of_Lippe-Biesterfeld
  AddTriple (41b3f9e9-d7e2-4870-917c-5d187707ce91)
 Call ID: 41b3f9e9-d7e2-4870-917c-5d187707ce91
  Args:
    target: Georg_II_Duke_of_Saxe-Meiningen
    source: Prince_Frederick_Johann_of_Saxe-Meiningen
    relation: :hasFather
  AddTriple (c5866675-695f-4ba6-a31b-148fcab14db3)
 Call ID: c5866675-695f-4ba6-a31b-148fcab14db3
  Args:
    target: Count_Ernst_of_Lippe-Biesterfeld
    relation: :hasFather
    source: Countess_Adelaide_of_Lippe-Biesterfeld
  AddTriple (cc0d0513-f9dd-4059-9e1e-6efad0fef1d5)
 Call ID: cc0d0513-f9dd-4059-9e1e-6efad0fef1d5
  Args:
    source: Georg_Prince_of_Saxe-Meiningen
    relation: :hasSon
    target: Prince_Frederick_Alfred
  AddTriple (88a2bffe-4bae-4631-bf6b-8506106ed768)
 Call ID: 88a2bffe-4bae-4631-bf6b-8506106ed768
  Args:
    target: Bernhard
    source: Georg_Prince_of_Saxe-Meiningen
    relation: :hasRelation
  AddTriple (44dcecca-843b-4f81-9a1e-bf5f4759e276)
 Call ID: 44dcecca-843b-4f81-9a1e-bf5f4759e276
  Args:
    source: Georg_Prince_of_Saxe-Meiningen
    relation: :hasRelation
    target: Countess_Klara_Marie_von_Korff_genannt_Schmising-Kerssenbrock
  Finish (5f243176-5290-4dde-a3ae-81b883626689)
 Call ID: 5f243176-5290-4dde-a3ae-81b883626689
  Args: