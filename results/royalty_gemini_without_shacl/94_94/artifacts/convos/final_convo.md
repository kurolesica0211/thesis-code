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
Wilhelm Herzog von Württemberg (born Wilhelm Friedrich Carl Philipp Albert Nikolaus Erich Maria; 13 August 1994) is the head of the House of Württemberg and a German businessman.
He is Chair of the Hofkammer des Hauses Württemberg, the company which manages the forests, farms, wineries, and housing estates of the former royal family of the Kingdom of Württemberg.
Life

Wilhelm is the eldest child of Friedrich, Hereditary Duke of Württemberg (1961–2018) and Princess Marie Wilhelmine of Wied (born 1973).
He was baptised in September 1994,  with his uncles Erich, Prince of Waldburg zu Zeil und Trauchburg, and Prince Wilhelm of Wied, as his godfathers.
On 9 May 2018, Wilhelm's father died in a car accident while driving on his way home to Friedrichshafen.
Upon the death of his father, Wilhelm became the heir apparent to his grandfather, Carl, Duke of Württemberg as Head of the House of Württemberg.
In July 2019, it was also announced that Wilhelm would be the future head of the Württemberg Hofkammer, the administrative offices of the family business.
On 7 June 2022, Wilhelm succeeded as Head of the House of Württemberg upon the death of his grandfather, Carl, Duke of Württemberg.
Wilhelm is unmarried.
With the headship of the house passing through the male line, the heir presumptive of the House of Württemberg is Wilhelm's paternal uncle Duke Eberhard of Württemberg, who married Gaby Maier on 15 July 2023.



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
  AssignClass (a3cf333b-8c08-4131-beec-e102df82af6c)
 Call ID: a3cf333b-8c08-4131-beec-e102df82af6c
  Args:
    type: :Man
    source: Wilhelm_Herzog_von_Württemberg
  AssignClass (264a0383-c6b3-40de-b7db-80a09ca5c001)
 Call ID: 264a0383-c6b3-40de-b7db-80a09ca5c001
  Args:
    source: Friedrich_Hereditary_Duke_of_Württemberg
    type: :Man
  AssignClass (fd04567f-d1cc-4ac6-a8c2-bb7bf5366cf7)
 Call ID: fd04567f-d1cc-4ac6-a8c2-bb7bf5366cf7
  Args:
    source: Princess_Marie_Wilhelmine_of_Wied
    type: :Woman
  AssignClass (5d3ddbc3-aecf-4c46-bb73-60e5ce9f0028)
 Call ID: 5d3ddbc3-aecf-4c46-bb73-60e5ce9f0028
  Args:
    source: Carl_Duke_of_Württemberg
    type: :Man
  AssignClass (5da66b95-6e45-4e17-9b59-a138791363c3)
 Call ID: 5da66b95-6e45-4e17-9b59-a138791363c3
  Args:
    source: Erich_Prince_of_Waldburg_zu_Zeil_und_Trauchburg
    type: :Man
  AssignClass (429019da-ae17-4bd6-ac4c-6bd2c097b1a1)
 Call ID: 429019da-ae17-4bd6-ac4c-6bd2c097b1a1
  Args:
    type: :Man
    source: Prince_Wilhelm_of_Wied
  AssignClass (a428454c-9823-48e5-81c5-bc920b4312fb)
 Call ID: a428454c-9823-48e5-81c5-bc920b4312fb
  Args:
    type: :Man
    source: Duke_Eberhard_of_Württemberg
  AssignClass (51345a68-31f8-4ac3-9ff2-ac427ac10763)
 Call ID: 51345a68-31f8-4ac3-9ff2-ac427ac10763
  Args:
    type: :Woman
    source: Gaby_Maier
  AddLiteral (6e379a84-ce51-4199-8a5a-b85e34d1bc01)
 Call ID: 6e379a84-ce51-4199-8a5a-b85e34d1bc01
  Args:
    literal_type: xsd:integer
    source: Wilhelm_Herzog_von_Württemberg
    literal_value: 1994
    relation: :hasBirthYear
  AddLiteral (7de6c73f-4ea4-4ad7-8fdb-c750152fe5f1)
 Call ID: 7de6c73f-4ea4-4ad7-8fdb-c750152fe5f1
  Args:
    relation: :hasBirthYear
    source: Friedrich_Hereditary_Duke_of_Württemberg
    literal_type: xsd:integer
    literal_value: 1961
  AddLiteral (1da0c147-7db5-4312-93c4-e9f823ecf0e9)
 Call ID: 1da0c147-7db5-4312-93c4-e9f823ecf0e9
  Args:
    relation: :hasDeathYear
    literal_value: 2018
    literal_type: xsd:integer
    source: Friedrich_Hereditary_Duke_of_Württemberg
  AddLiteral (66e21094-322d-4924-99e6-3e44aa172311)
 Call ID: 66e21094-322d-4924-99e6-3e44aa172311
  Args:
    relation: :hasBirthYear
    literal_value: 1973
    source: Princess_Marie_Wilhelmine_of_Wied
    literal_type: xsd:integer
  AddLiteral (21227200-153c-4ee5-8dba-8cd46cbb4a5f)
 Call ID: 21227200-153c-4ee5-8dba-8cd46cbb4a5f
  Args:
    relation: :hasDeathYear
    literal_value: 2022
    source: Carl_Duke_of_Württemberg
    literal_type: xsd:integer
  AddLiteral (0846b0f9-caca-499b-b9a5-f61d1ec995f8)
 Call ID: 0846b0f9-caca-499b-b9a5-f61d1ec995f8
  Args:
    relation: :hasMarriageYear
    source: Gaby_Maier
    literal_type: xsd:integer
    literal_value: 2023
  AddTriple (c4c9c415-1430-451b-be64-ac7c187a9fef)
 Call ID: c4c9c415-1430-451b-be64-ac7c187a9fef
  Args:
    relation: :hasFather
    source: Wilhelm_Herzog_von_Württemberg
    target: Friedrich_Hereditary_Duke_of_Württemberg
  AddTriple (287974a4-1d02-4bba-813d-692f9a8b6176)
 Call ID: 287974a4-1d02-4bba-813d-692f9a8b6176
  Args:
    target: Princess_Marie_Wilhelmine_of_Wied
    source: Wilhelm_Herzog_von_Württemberg
    relation: :hasMother
  AddTriple (c8ea7a0c-9fff-4997-bfb3-b8b8aa8d7563)
 Call ID: c8ea7a0c-9fff-4997-bfb3-b8b8aa8d7563
  Args:
    target: Friedrich_Hereditary_Duke_of_Württemberg
    source: Carl_Duke_of_Württemberg
    relation: :isFatherOf
  AddTriple (8f89a025-93e1-41cb-abb4-c2c1677817e6)
 Call ID: 8f89a025-93e1-41cb-abb4-c2c1677817e6
  Args:
    source: Duke_Eberhard_of_Württemberg
    target: Friedrich_Hereditary_Duke_of_Württemberg
    relation: :isBrotherOf
  AddTriple (8ca3c0de-da9e-4736-a1bd-8a593408ec56)
 Call ID: 8ca3c0de-da9e-4736-a1bd-8a593408ec56
  Args:
    relation: :hasMarriageYear
    target: Duke_Eberhard_of_Württemberg
    source: Gaby_Maier
  Finish (2aaae288-51b9-4d38-82af-6327cd40efe4)
 Call ID: 2aaae288-51b9-4d38-82af-6327cd40efe4
  Args: