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
Kraft, 9th Prince of Hohenlohe-Langenburg (German: Kraft Alexander Ernst Ludwig Georg Emich Fürst zu Hohenlohe-Langenburg; 25 June 1935 – 16 March 2004), was a German prince and landowner who was titular head of the House of Hohenlohe-Langenburg.
He was a nephew of Prince Philip, Duke of Edinburgh, a nephew-in-law of Queen Elizabeth II, and thus a first cousin of King Charles III.
Early life

Kraft was born on 25 June 1935 in Schwäbisch Hall to Gottfried, Hereditary Prince of Hohenlohe-Langenburg, and Princess Margarita of Greece and Denmark, the eldest sister of Prince Philip, Duke of Edinburgh.
The family was not invited to Philip's wedding to Princess Elizabeth of the United Kingdom in 1947, due to his parents' membership of the Nazi Party.
Six years later, however and his parents and sister, Princess Beatrix, were seated in the royal box at  his aunt's coronation in Westminster Abbey.
Activities

In 1960, Kraft succeeded his father as titular Prince of Hohenlohe-Langenburg.
In 1965, he received his aunt and uncle, Queen Elizabeth II and Prince Philip, Duke of Edinburgh, at the damaged castle during their state visit to West Germany.
He sold Weikersheim Palace to the state of Baden-Württemberg in 1967 to cover the cost of the restoration.
Marriage and family

Kraft married, firstly, Princess Charlotte of Croÿ (born 1938) on 5 June 1965.
He and Charlotte were divorced in 1990.
He maintained relations with his British royal relatives, attending family events such as the wedding of Prince Charles and Lady Diana Spencer in 1981 and the wedding of Prince Andrew and Sarah Ferguson in 1986.



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
  AssignClass (0d464b98-2921-46f3-b16d-cfad83c32645)
 Call ID: 0d464b98-2921-46f3-b16d-cfad83c32645
  Args:
    source: Kraft_Prince_of_Hohenlohe-Langenburg
    type: :Man
  AssignClass (86a8b84c-9dea-4660-9b89-b8f1e6f41ec4)
 Call ID: 86a8b84c-9dea-4660-9b89-b8f1e6f41ec4
  Args:
    source: Kraft_Prince_of_Hohenlohe-Langenburg
    type: :Person
  AddLiteral (3976727c-a087-4c77-afd7-719e4171d9b9)
 Call ID: 3976727c-a087-4c77-afd7-719e4171d9b9
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Kraft_Prince_of_Hohenlohe-Langenburg
    literal_value: 1935
  AddLiteral (0a6538c9-5ad4-48ce-b3b9-9e7d46b87cf2)
 Call ID: 0a6538c9-5ad4-48ce-b3b9-9e7d46b87cf2
  Args:
    literal_type: xsd:integer
    source: Kraft_Prince_of_Hohenlohe-Langenburg
    literal_value: 2004
    relation: :hasDeathYear
  AssignClass (d1cd65ea-cb10-4750-8d74-1cd9b61d5994)
 Call ID: d1cd65ea-cb10-4750-8d74-1cd9b61d5994
  Args:
    source: Gottfried_Hereditary_Prince_of_Hohenlohe-Langenburg
    type: :Man
  AssignClass (97b4edc6-cf00-4e7d-9f48-89ec83218052)
 Call ID: 97b4edc6-cf00-4e7d-9f48-89ec83218052
  Args:
    type: :Person
    source: Gottfried_Hereditary_Prince_of_Hohenlohe-Langenburg
  AssignClass (5e39ee55-9310-41da-a086-7cdd24ccf005)
 Call ID: 5e39ee55-9310-41da-a086-7cdd24ccf005
  Args:
    source: Princess_Margarita_of_Greece_and_Denmark
    type: :Woman
  AssignClass (74f0abb0-9a35-4302-9a0f-1cbfd37a31ec)
 Call ID: 74f0abb0-9a35-4302-9a0f-1cbfd37a31ec
  Args:
    source: Princess_Margarita_of_Greece_and_Denmark
    type: :Person
  AddTriple (9cec957b-0a42-4ea6-a626-8aa8f498f1d1)
 Call ID: 9cec957b-0a42-4ea6-a626-8aa8f498f1d1
  Args:
    target: Gottfried_Hereditary_Prince_of_Hohenlohe-Langenburg
    source: Kraft_Prince_of_Hohenlohe-Langenburg
    relation: :hasFather
  AddTriple (9358a56f-5a52-4779-9e1d-908d1919c6a4)
 Call ID: 9358a56f-5a52-4779-9e1d-908d1919c6a4
  Args:
    target: Princess_Margarita_of_Greece_and_Denmark
    relation: :hasMother
    source: Kraft_Prince_of_Hohenlohe-Langenburg
  AssignClass (2a925409-cfe1-403d-b006-618b2dd5e0b6)
 Call ID: 2a925409-cfe1-403d-b006-618b2dd5e0b6
  Args:
    source: Prince_Philip_Duke_of_Edinburgh
    type: :Man
  AssignClass (dc8004de-3efa-4ff0-8bee-86360ff99ba0)
 Call ID: dc8004de-3efa-4ff0-8bee-86360ff99ba0
  Args:
    source: Prince_Philip_Duke_of_Edinburgh
    type: :Person
  AddTriple (4ffe0c85-61a0-4816-98fe-c9c83d65c1a2)
 Call ID: 4ffe0c85-61a0-4816-98fe-c9c83d65c1a2
  Args:
    source: Prince_Philip_Duke_of_Edinburgh
    relation: :hasSister
    target: Princess_Margarita_of_Greece_and_Denmark
  AssignClass (4161661c-e1ed-47ae-b26f-8de6d7a7c680)
 Call ID: 4161661c-e1ed-47ae-b26f-8de6d7a7c680
  Args:
    source: Princess_Beatrix_of_Hohenlohe-Langenburg
    type: :Woman
  AssignClass (4816f7c9-3109-4e33-a314-81d39bf2b152)
 Call ID: 4816f7c9-3109-4e33-a314-81d39bf2b152
  Args:
    source: Princess_Beatrix_of_Hohenlohe-Langenburg
    type: :Person
  AddTriple (2c68afa2-7576-4ea5-b9f6-7d045dffb6b9)
 Call ID: 2c68afa2-7576-4ea5-b9f6-7d045dffb6b9
  Args:
    source: Princess_Beatrix_of_Hohenlohe-Langenburg
    relation: :hasMother
    target: Princess_Margarita_of_Greece_and_Denmark
  AddTriple (15deaee7-fcb0-436e-a8bc-c1afed8b0f64)
 Call ID: 15deaee7-fcb0-436e-a8bc-c1afed8b0f64
  Args:
    target: Gottfried_Hereditary_Prince_of_Hohenlohe-Langenburg
    relation: :hasFather
    source: Princess_Beatrix_of_Hohenlohe-Langenburg
  AssignClass (d8b02d84-ddcc-4d3f-a01a-f6ee463408fa)
 Call ID: d8b02d84-ddcc-4d3f-a01a-f6ee463408fa
  Args:
    source: Princess_Charlotte_of_Croy
    type: :Woman
  AssignClass (acdf1022-1ba5-4434-bc7a-d4c80e2c8683)
 Call ID: acdf1022-1ba5-4434-bc7a-d4c80e2c8683
  Args:
    source: Princess_Charlotte_of_Croy
    type: :Person
  AddTriple (509bd606-c754-4ee3-83db-a93ddf525659)
 Call ID: 509bd606-c754-4ee3-83db-a93ddf525659
  Args:
    relation: :hasRelation
    source: Kraft_Prince_of_Hohenlohe-Langenburg
    target: Princess_Charlotte_of_Croy
  AddLiteral (b67ef372-ba02-4532-9dd8-a65839b544f6)
 Call ID: b67ef372-ba02-4532-9dd8-a65839b544f6
  Args:
    source: Kraft_Prince_of_Hohenlohe-Langenburg
    literal_value: 1965
    relation: :hasMarriageYear
    literal_type: xsd:integer
  Finish (439817fe-1351-43ac-a990-3cb4490f876f)
 Call ID: 439817fe-1351-43ac-a990-3cb4490f876f
  Args: