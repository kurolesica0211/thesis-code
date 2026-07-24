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
Bernhard, Prince of Saxe-Meiningen (German: Bernhard, Prinz von Sachsen-Meiningen; 30 June 1901 – 4 October 1984) was the head of the House of Saxe-Meiningen from 1946 until his death.
Prince of Saxe-Meiningen

Bernhard was born in Köln the third son of Prince Frederick Johann of Saxe-Meiningen and Countess Adelaide of Lippe-Biesterfeld.
His father was the second son of Georg II, Duke of Saxe-Meiningen and his mother a daughter of Count Ernst of Lippe-Biesterfeld.
After the death of his older brother Prince Georg in 1946 his nephew Prince Frederick Alfred renounced his succession rights and so Bernhard succeeded to the headship of the house of Saxe-Meiningen and the nominal title of Duke of Saxe-Meiningen (as Bernhard IV).
As his first marriage was morganatic his second son Prince Frederick Konrad succeeded him as head of the ducal house following his death in Bad Krozingen.
Bernhard and his first wife were declared guilty of a Nazi conspiracy against Austria in 1933; he was sentenced to six weeks in prison, while she was placed under house arrest.
Family

Bernhard was married morganatically to Margot Grössler (1911–1998), from Wrocław, daughter of Friedrich Grössler, a merchant, and Erika Wägner, in Eichenhof
They had two children, both of whom had no succession rights:


Bernhard married secondly in Ziegenberg über Bad Nauheim on 11 August 1948 to Baroness Vera Schäffer von Bernstein (1914–1994), daughter of Baron Friedrich "Fritz" Schäffer von Bernstein (1868–1958) and Emma Carola, née Passavant (1884–1971).
They had three children, including a son, Konrad, with full rights to the succession to the house of Saxe-Meiningen:


Ancestry

References



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
  AssignClass (cc696d74-8596-44f0-bb4b-f0c5d062c2e4)
 Call ID: cc696d74-8596-44f0-bb4b-f0c5d062c2e4
  Args:
    type: :Man
    source: Bernhard_Prince_of_Saxe-Meiningen
  AddLiteral (900d10fc-5d5d-4679-8100-d5ba424a4d89)
 Call ID: 900d10fc-5d5d-4679-8100-d5ba424a4d89
  Args:
    source: Bernhard_Prince_of_Saxe-Meiningen
    relation: :hasBirthYear
    literal_value: 1901
    literal_type: xsd:integer
  AddLiteral (ad457c03-a5e8-490a-b008-3826354b271b)
 Call ID: ad457c03-a5e8-490a-b008-3826354b271b
  Args:
    source: Bernhard_Prince_of_Saxe-Meiningen
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 1984
  AssignClass (4f61c150-6507-42c8-b9d2-9e7a32bd9b1a)
 Call ID: 4f61c150-6507-42c8-b9d2-9e7a32bd9b1a
  Args:
    type: :Man
    source: Prince_Frederick_Johann_of_Saxe-Meiningen
  AssignClass (8b6a8556-9e1a-4a63-9184-98a8c2696c9b)
 Call ID: 8b6a8556-9e1a-4a63-9184-98a8c2696c9b
  Args:
    type: :Woman
    source: Countess_Adelaide_of_Lippe-Biesterfeld
  AddTriple (2d3c5693-cbe1-4d49-ab57-044cda908b65)
 Call ID: 2d3c5693-cbe1-4d49-ab57-044cda908b65
  Args:
    relation: :hasFather
    target: Prince_Frederick_Johann_of_Saxe-Meiningen
    source: Bernhard_Prince_of_Saxe-Meiningen
  AddTriple (d42a1b14-e848-46e3-b07c-4801cbc4995c)
 Call ID: d42a1b14-e848-46e3-b07c-4801cbc4995c
  Args:
    source: Bernhard_Prince_of_Saxe-Meiningen
    target: Countess_Adelaide_of_Lippe-Biesterfeld
    relation: :hasMother
  AssignClass (80cb64c3-bbf1-48f0-97c1-6a2036025f41)
 Call ID: 80cb64c3-bbf1-48f0-97c1-6a2036025f41
  Args:
    type: :Man
    source: Georg_II_Duke_of_Saxe-Meiningen
  AddTriple (da9fb73b-46b3-45f2-8e2e-c623a3034fa1)
 Call ID: da9fb73b-46b3-45f2-8e2e-c623a3034fa1
  Args:
    target: Georg_II_Duke_of_Saxe-Meiningen
    source: Prince_Frederick_Johann_of_Saxe-Meiningen
    relation: :hasFather
  AssignClass (bc67cfd5-3239-4b2f-9f18-aec5775f4a03)
 Call ID: bc67cfd5-3239-4b2f-9f18-aec5775f4a03
  Args:
    type: :Man
    source: Count_Ernst_of_Lippe-Biesterfeld
  AddTriple (aec14a6f-40c7-40c8-bbc5-bb4a147af51c)
 Call ID: aec14a6f-40c7-40c8-bbc5-bb4a147af51c
  Args:
    source: Countess_Adelaide_of_Lippe-Biesterfeld
    target: Count_Ernst_of_Lippe-Biesterfeld
    relation: :hasFather
  AssignClass (be6de5fc-3806-4b05-86f7-d3486d574f7b)
 Call ID: be6de5fc-3806-4b05-86f7-d3486d574f7b
  Args:
    type: :Man
    source: Prince_Georg
  AddTriple (5bf42241-ca82-4813-a9ef-48f91939f110)
 Call ID: 5bf42241-ca82-4813-a9ef-48f91939f110
  Args:
    target: Prince_Georg
    source: Bernhard_Prince_of_Saxe-Meiningen
    relation: :isSiblingOf
  AssignClass (fca270b0-f31e-4b62-9316-a6a807132d3b)
 Call ID: fca270b0-f31e-4b62-9316-a6a807132d3b
  Args:
    type: :Woman
    source: Margot_Grössler
  AddLiteral (573c5bde-dac7-409b-83e4-12ece5d9ea9d)
 Call ID: 573c5bde-dac7-409b-83e4-12ece5d9ea9d
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1911
    source: Margot_Grössler
  AddLiteral (c97119c9-44b1-4399-b8a7-e1e394685526)
 Call ID: c97119c9-44b1-4399-b8a7-e1e394685526
  Args:
    source: Margot_Grössler
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 1998
  AddTriple (1c78999e-0c13-442a-9054-f099ab17d42f)
 Call ID: 1c78999e-0c13-442a-9054-f099ab17d42f
  Args:
    source: Bernhard_Prince_of_Saxe-Meiningen
    target: Margot_Grössler
    relation: :hasRelation
  AssignClass (9d8c40c6-023e-4c71-ab56-f094f0b69352)
 Call ID: 9d8c40c6-023e-4c71-ab56-f094f0b69352
  Args:
    type: :Man
    source: Friedrich_Grössler
  AssignClass (b5ccc2a3-b930-4852-bc4b-b9c4a4426751)
 Call ID: b5ccc2a3-b930-4852-bc4b-b9c4a4426751
  Args:
    type: :Woman
    source: Erika_Wägner
  AddTriple (76b8cad8-4dea-4e6d-bcb5-677dbce8d0de)
 Call ID: 76b8cad8-4dea-4e6d-bcb5-677dbce8d0de
  Args:
    target: Friedrich_Grössler
    source: Margot_Grössler
    relation: :hasFather
  AddTriple (1baac25a-0499-4b89-94ff-7733d31e51e7)
 Call ID: 1baac25a-0499-4b89-94ff-7733d31e51e7
  Args:
    relation: :hasMother
    source: Margot_Grössler
    target: Erika_Wägner
  AssignClass (54bd9628-d723-494f-ba9a-300eb6e9a50e)
 Call ID: 54bd9628-d723-494f-ba9a-300eb6e9a50e
  Args:
    type: :Man
    source: Prince_Frederick_Konrad
  AddTriple (eb9e3b17-5047-4a7c-9f51-57f0ca3d0270)
 Call ID: eb9e3b17-5047-4a7c-9f51-57f0ca3d0270
  Args:
    target: Bernhard_Prince_of_Saxe-Meiningen
    source: Prince_Frederick_Konrad
    relation: :hasFather
  AddTriple (a7457731-d649-4889-a463-8b70d4fe5f49)
 Call ID: a7457731-d649-4889-a463-8b70d4fe5f49
  Args:
    relation: :hasMother
    target: Margot_Grössler
    source: Prince_Frederick_Konrad
  AssignClass (c7edd3ed-a0fc-4c52-9eb0-7744b5087eef)
 Call ID: c7edd3ed-a0fc-4c52-9eb0-7744b5087eef
  Args:
    type: :Woman
    source: Vera_Schäffer_von_Bernstein
  AddLiteral (7d885797-f5ab-4f2e-8783-366758968ef1)
 Call ID: 7d885797-f5ab-4f2e-8783-366758968ef1
  Args:
    source: Vera_Schäffer_von_Bernstein
    literal_type: xsd:integer
    literal_value: 1914
    relation: :hasBirthYear
  AddLiteral (0dac6935-65c2-4518-94f9-b6b63c653313)
 Call ID: 0dac6935-65c2-4518-94f9-b6b63c653313
  Args:
    literal_value: 1994
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: Vera_Schäffer_von_Bernstein
  AddTriple (22e91230-9849-4b48-93f1-1544e71e8c3c)
 Call ID: 22e91230-9849-4b48-93f1-1544e71e8c3c
  Args:
    target: Vera_Schäffer_von_Bernstein
    source: Bernhard_Prince_of_Saxe-Meiningen
    relation: :hasRelation
  AddLiteral (23d23237-2b43-48a6-8ad4-c677bc6f31b2)
 Call ID: 23d23237-2b43-48a6-8ad4-c677bc6f31b2
  Args:
    literal_type: xsd:integer
    literal_value: 1948
    relation: :hasMarriageYear
    source: Vera_Schäffer_von_Bernstein
  AssignClass (92593499-cdc2-4271-97a6-276694cc2757)
 Call ID: 92593499-cdc2-4271-97a6-276694cc2757
  Args:
    type: :Man
    source: Baron_Friedrich_Fritz_Schäffer_von_Bernstein
  AssignClass (b182b19e-3270-41e0-9706-2fc7f71db519)
 Call ID: b182b19e-3270-41e0-9706-2fc7f71db519
  Args:
    type: :Woman
    source: Emma_Carola_Passavant
  AddTriple (ccb71669-ad91-4d60-9195-4be3558ff3eb)
 Call ID: ccb71669-ad91-4d60-9195-4be3558ff3eb
  Args:
    relation: :hasFather
    target: Baron_Friedrich_Fritz_Schäffer_von_Bernstein
    source: Vera_Schäffer_von_Bernstein
  AddTriple (97d23555-6bdd-4a8c-92aa-923be23e8d3e)
 Call ID: 97d23555-6bdd-4a8c-92aa-923be23e8d3e
  Args:
    target: Emma_Carola_Passavant
    source: Vera_Schäffer_von_Bernstein
    relation: :hasMother
  AssignClass (718e779a-9b04-4f61-aae2-ccb54e31d30e)
 Call ID: 718e779a-9b04-4f61-aae2-ccb54e31d30e
  Args:
    type: :Man
    source: Konrad
  AddTriple (21cf1bca-8a94-47ff-9530-afac55878f74)
 Call ID: 21cf1bca-8a94-47ff-9530-afac55878f74
  Args:
    relation: :hasFather
    source: Konrad
    target: Bernhard_Prince_of_Saxe-Meiningen
  AddTriple (2bcbf7d6-3004-4435-b0aa-e5fe50c1e996)
 Call ID: 2bcbf7d6-3004-4435-b0aa-e5fe50c1e996
  Args:
    target: Vera_Schäffer_von_Bernstein
    source: Konrad
    relation: :hasMother
  Finish (15fe5a52-f723-4b08-8201-72a5655ae0e8)
 Call ID: 15fe5a52-f723-4b08-8201-72a5655ae0e8
  Args: