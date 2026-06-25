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
  AssignClass (f7c48bf7-3666-4a02-91a9-4d641d8600a1)
 Call ID: f7c48bf7-3666-4a02-91a9-4d641d8600a1
  Args:
    type: :Man
    source: Georg_Prince_of_Saxe-Meiningen
  AssignClass (9a141517-4e78-4a52-8ab7-228b9e79e402)
 Call ID: 9a141517-4e78-4a52-8ab7-228b9e79e402
  Args:
    type: :Person
    source: Georg_Prince_of_Saxe-Meiningen
  AddLiteral (ffb319d8-a0a8-4a9c-9b38-a11ef1681102)
 Call ID: ffb319d8-a0a8-4a9c-9b38-a11ef1681102
  Args:
    literal_type: xsd:integer
    source: Georg_Prince_of_Saxe-Meiningen
    relation: :hasBirthYear
    literal_value: 1892
  AddLiteral (5933fc2f-f464-42e1-aaa5-20bd6c6d4c00)
 Call ID: 5933fc2f-f464-42e1-aaa5-20bd6c6d4c00
  Args:
    literal_value: 1946
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: Georg_Prince_of_Saxe-Meiningen
  AssignClass (3a3f36b9-12aa-4d36-ab66-79d9a7087645)
 Call ID: 3a3f36b9-12aa-4d36-ab66-79d9a7087645
  Args:
    type: :Man
    source: Prince_Frederick_Johann_of_Saxe-Meiningen
  AssignClass (3c5b3228-b106-4560-bad6-010c3e12690e)
 Call ID: 3c5b3228-b106-4560-bad6-010c3e12690e
  Args:
    source: Prince_Frederick_Johann_of_Saxe-Meiningen
    type: :Person
  AddLiteral (155bde4b-32bd-49ff-b462-848deb401801)
 Call ID: 155bde4b-32bd-49ff-b462-848deb401801
  Args:
    literal_value: 1861
    relation: :hasBirthYear
    source: Prince_Frederick_Johann_of_Saxe-Meiningen
    literal_type: xsd:integer
  AddLiteral (60ff1d45-7d9c-4271-9ddb-23c22ef8fc1c)
 Call ID: 60ff1d45-7d9c-4271-9ddb-23c22ef8fc1c
  Args:
    relation: :hasDeathYear
    literal_value: 1914
    source: Prince_Frederick_Johann_of_Saxe-Meiningen
    literal_type: xsd:integer
  AssignClass (ef306e93-8bd3-4b8b-8556-e91a88d890fb)
 Call ID: ef306e93-8bd3-4b8b-8556-e91a88d890fb
  Args:
    type: :Woman
    source: Countess_Adelaide_of_Lippe-Biesterfeld
  AssignClass (af1ba258-5708-4af3-a859-d37b396b67a9)
 Call ID: af1ba258-5708-4af3-a859-d37b396b67a9
  Args:
    type: :Person
    source: Countess_Adelaide_of_Lippe-Biesterfeld
  AddLiteral (69851cfc-28be-454e-9916-6b0881e52a4b)
 Call ID: 69851cfc-28be-454e-9916-6b0881e52a4b
  Args:
    literal_type: xsd:integer
    source: Countess_Adelaide_of_Lippe-Biesterfeld
    relation: :hasBirthYear
    literal_value: 1870
  AddLiteral (bd63fdc6-4e42-4ed2-984f-04d5d3ab0525)
 Call ID: bd63fdc6-4e42-4ed2-984f-04d5d3ab0525
  Args:
    literal_value: 1948
    relation: :hasDeathYear
    source: Countess_Adelaide_of_Lippe-Biesterfeld
    literal_type: xsd:integer
  AddTriple (7f37848b-c78e-41d3-a288-54ef34be5af4)
 Call ID: 7f37848b-c78e-41d3-a288-54ef34be5af4
  Args:
    source: Georg_Prince_of_Saxe-Meiningen
    relation: :hasFather
    target: Prince_Frederick_Johann_of_Saxe-Meiningen
  AddTriple (682e9aea-551a-41c5-ada2-1d0452d65ce1)
 Call ID: 682e9aea-551a-41c5-ada2-1d0452d65ce1
  Args:
    target: Countess_Adelaide_of_Lippe-Biesterfeld
    relation: :hasMother
    source: Georg_Prince_of_Saxe-Meiningen
  AssignClass (b0127fc3-977c-4ae5-adf3-5b50b5cdfb39)
 Call ID: b0127fc3-977c-4ae5-adf3-5b50b5cdfb39
  Args:
    source: Georg_II_Duke_of_Saxe-Meiningen
    type: :Man
  AssignClass (ece0cca1-adf3-47d9-85ec-4b71d984801a)
 Call ID: ece0cca1-adf3-47d9-85ec-4b71d984801a
  Args:
    source: Georg_II_Duke_of_Saxe-Meiningen
    type: :Person
  AddTriple (32a9dd9a-3963-4f21-bb87-b82664d6f30e)
 Call ID: 32a9dd9a-3963-4f21-bb87-b82664d6f30e
  Args:
    target: Georg_II_Duke_of_Saxe-Meiningen
    relation: :hasFather
    source: Prince_Frederick_Johann_of_Saxe-Meiningen
  AssignClass (a812a025-12f2-48f7-b50e-3c53f03147b0)
 Call ID: a812a025-12f2-48f7-b50e-3c53f03147b0
  Args:
    source: Count_Ernst_of_Lippe-Biesterfeld
    type: :Man
  AssignClass (44743299-fb56-48ab-9499-019537248762)
 Call ID: 44743299-fb56-48ab-9499-019537248762
  Args:
    source: Count_Ernst_of_Lippe-Biesterfeld
    type: :Person
  AddTriple (18bcf386-069c-4d53-a84b-5282fdb4b552)
 Call ID: 18bcf386-069c-4d53-a84b-5282fdb4b552
  Args:
    source: Countess_Adelaide_of_Lippe-Biesterfeld
    target: Count_Ernst_of_Lippe-Biesterfeld
    relation: :hasFather
  AssignClass (2f7bb5ef-133d-4044-ba46-e779355e941c)
 Call ID: 2f7bb5ef-133d-4044-ba46-e779355e941c
  Args:
    type: :Man
    source: Prince_Frederick_Alfred
  AssignClass (26d7fec8-eaac-48d6-b768-52fb4f470803)
 Call ID: 26d7fec8-eaac-48d6-b768-52fb4f470803
  Args:
    source: Prince_Frederick_Alfred
    type: :Person
  AddTriple (2dcb337d-dd0e-4cfd-93d7-cc9b3a162dc2)
 Call ID: 2dcb337d-dd0e-4cfd-93d7-cc9b3a162dc2
  Args:
    source: Prince_Frederick_Alfred
    relation: :hasFather
    target: Georg_Prince_of_Saxe-Meiningen
  AssignClass (2d0f4122-4799-4f0b-9225-45745819dddc)
 Call ID: 2d0f4122-4799-4f0b-9225-45745819dddc
  Args:
    type: :Man
    source: Bernhard
  AssignClass (221b5c11-1806-46dc-9c04-32856ccdaa96)
 Call ID: 221b5c11-1806-46dc-9c04-32856ccdaa96
  Args:
    source: Bernhard
    type: :Person
  AssignClass (eb119752-114e-4ba2-a86d-5bf316b9fe6c)
 Call ID: eb119752-114e-4ba2-a86d-5bf316b9fe6c
  Args:
    type: :Woman
    source: Countess_Klara_Marie_von_Korff_genannt_Schmising-Kerssenbrock
  AssignClass (87c05ea3-aa54-4df0-a5e1-364bf9bf591b)
 Call ID: 87c05ea3-aa54-4df0-a5e1-364bf9bf591b
  Args:
    type: :Person
    source: Countess_Klara_Marie_von_Korff_genannt_Schmising-Kerssenbrock
  AddLiteral (ce74371f-13cb-4e83-bfcd-1213680f4f58)
 Call ID: ce74371f-13cb-4e83-bfcd-1213680f4f58
  Args:
    literal_type: xsd:integer
    source: Countess_Klara_Marie_von_Korff_genannt_Schmising-Kerssenbrock
    literal_value: 1895
    relation: :hasBirthYear
  AddTriple (47eb91f2-3a5d-4c75-a8f7-630754cac533)
 Call ID: 47eb91f2-3a5d-4c75-a8f7-630754cac533
  Args:
    relation: :hasRelation
    target: Countess_Klara_Marie_von_Korff_genannt_Schmising-Kerssenbrock
    source: Georg_Prince_of_Saxe-Meiningen
  AddLiteral (60d10a46-07b4-48a9-af6f-c3519c8f4632)
 Call ID: 60d10a46-07b4-48a9-af6f-c3519c8f4632
  Args:
    literal_type: xsd:integer
    source: Georg_Prince_of_Saxe-Meiningen
    literal_value: 1919
    relation: :hasMarriageYear
  Finish (f48f464b-5c5d-4b73-a5ba-14bd20def26e)
 Call ID: f48f464b-5c5d-4b73-a5ba-14bd20def26e
  Args: