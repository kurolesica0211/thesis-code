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
Lady Charlotte Anne Santo Domingo (née Wellesley; 8 October 1990) is an English aristocrat and socialite and photography producer.
Early life and family

Lady Charlotte Wellesley was born at St Mary's Hospital, London on 8 October 1990 to Princess Antonia of Prussia and Charles Wellesley, Marquess of Douro.
After the death of her paternal grandfather, Valerian Wellesley, 8th Duke of Wellington, in 2014, her father succeeded him as the 9th Duke of Wellington, the 9th Prince of Waterloo, the 9th Duke of Victoria, and the 10th Duke of Ciudad Rodrigo.
Her mother, Princess Antonia, is the youngest child of Prince Frederick of Prussia and Lady Brigid Guinness.
Through her mother, Lady Charlotte is a great-great-granddaughter of Wilhelm II, German Emperor and a great-great-great-great-granddaughter of Queen Victoria.
Lady Charlotte grew up at Stratfield Saye House, her family's estate in Hampshire.
She is the younger sister of Arthur Wellesley, Earl of Mornington and Lady Mary Wellesley.
Education and career

Lady Charlotte attended Wycombe Abbey, an all-girls boarding school in Buckinghamshire.
Personal life

Lady Charlotte married Colombian-American financier Alejandro Santo Domingo in Íllora, Spain, on 28 May 2016.



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
  AssignClass (705403e6-b1af-4429-ba55-f462c5c9492a)
 Call ID: 705403e6-b1af-4429-ba55-f462c5c9492a
  Args:
    type: :Woman
    source: Charlotte_Wellesley
  AssignClass (7b9aac34-1ffa-4427-8379-e2dfcdfc1098)
 Call ID: 7b9aac34-1ffa-4427-8379-e2dfcdfc1098
  Args:
    source: Charlotte_Wellesley
    type: :Person
  AddLiteral (937426a9-8608-440d-90ea-8e0979adb022)
 Call ID: 937426a9-8608-440d-90ea-8e0979adb022
  Args:
    relation: :hasBirthYear
    literal_value: 1990
    literal_type: xsd:integer
    source: Charlotte_Wellesley
  AssignClass (2e5dfe42-2024-470e-ba7b-de48f74048d9)
 Call ID: 2e5dfe42-2024-470e-ba7b-de48f74048d9
  Args:
    type: :Woman
    source: Antonia_of_Prussia
  AssignClass (7e5204fb-d288-498c-870b-a478ccea2d4b)
 Call ID: 7e5204fb-d288-498c-870b-a478ccea2d4b
  Args:
    source: Antonia_of_Prussia
    type: :Person
  AssignClass (d15e0b52-ab8f-4966-b6d8-c1d6449477bd)
 Call ID: d15e0b52-ab8f-4966-b6d8-c1d6449477bd
  Args:
    source: Charles_Wellesley
    type: :Man
  AssignClass (2accdf8c-73e9-443b-af36-d53fca210685)
 Call ID: 2accdf8c-73e9-443b-af36-d53fca210685
  Args:
    type: :Person
    source: Charles_Wellesley
  AddTriple (5e7314b4-0872-4b34-96b5-0a641c653402)
 Call ID: 5e7314b4-0872-4b34-96b5-0a641c653402
  Args:
    relation: :hasFather
    target: Charles_Wellesley
    source: Charlotte_Wellesley
  AddTriple (aa203ce1-2917-456c-a5fa-8db152b1a51e)
 Call ID: aa203ce1-2917-456c-a5fa-8db152b1a51e
  Args:
    target: Antonia_of_Prussia
    source: Charlotte_Wellesley
    relation: :hasMother
  AssignClass (d2d3ff4f-672b-4f55-b40c-e63207c4b87b)
 Call ID: d2d3ff4f-672b-4f55-b40c-e63207c4b87b
  Args:
    source: Valerian_Wellesley
    type: :Man
  AssignClass (3f4548ed-e4da-4c92-a556-67aab20b4ef1)
 Call ID: 3f4548ed-e4da-4c92-a556-67aab20b4ef1
  Args:
    source: Valerian_Wellesley
    type: :Person
  AddLiteral (5cb9823c-030c-4bd5-8588-ee1197fd9554)
 Call ID: 5cb9823c-030c-4bd5-8588-ee1197fd9554
  Args:
    relation: :hasDeathYear
    literal_value: 2014
    literal_type: xsd:integer
    source: Valerian_Wellesley
  AddTriple (9fe9e41b-928c-459b-84e6-97bfabe3aa08)
 Call ID: 9fe9e41b-928c-459b-84e6-97bfabe3aa08
  Args:
    relation: :hasFather
    source: Charles_Wellesley
    target: Valerian_Wellesley
  AssignClass (ebd49246-24a2-4486-a92c-108b75e48b81)
 Call ID: ebd49246-24a2-4486-a92c-108b75e48b81
  Args:
    type: :Man
    source: Frederick_of_Prussia
  AssignClass (12d13e6e-485d-4d91-9baa-55569976a7ca)
 Call ID: 12d13e6e-485d-4d91-9baa-55569976a7ca
  Args:
    source: Frederick_of_Prussia
    type: :Person
  AssignClass (d195bc30-3769-49b2-8caf-147ef21d7019)
 Call ID: d195bc30-3769-49b2-8caf-147ef21d7019
  Args:
    source: Brigid_Guinness
    type: :Woman
  AssignClass (57c4cc0c-64eb-4957-bdeb-ffee277d99fd)
 Call ID: 57c4cc0c-64eb-4957-bdeb-ffee277d99fd
  Args:
    type: :Person
    source: Brigid_Guinness
  AddTriple (71632265-f573-42ec-b5f9-4f22e7f29f0a)
 Call ID: 71632265-f573-42ec-b5f9-4f22e7f29f0a
  Args:
    relation: :hasFather
    target: Frederick_of_Prussia
    source: Antonia_of_Prussia
  AddTriple (04419ca5-1b98-464d-8af3-e02be7ef2b0d)
 Call ID: 04419ca5-1b98-464d-8af3-e02be7ef2b0d
  Args:
    relation: :hasMother
    source: Antonia_of_Prussia
    target: Brigid_Guinness
  AssignClass (fa91d053-234e-4de4-b42c-3553579b8ef6)
 Call ID: fa91d053-234e-4de4-b42c-3553579b8ef6
  Args:
    type: :Man
    source: Arthur_Wellesley
  AssignClass (302a13a1-a613-40f0-99dc-34a836d6e236)
 Call ID: 302a13a1-a613-40f0-99dc-34a836d6e236
  Args:
    source: Arthur_Wellesley
    type: :Person
  AssignClass (d6a68529-8d8e-4b59-ae4b-4009802c0e2e)
 Call ID: d6a68529-8d8e-4b59-ae4b-4009802c0e2e
  Args:
    type: :Woman
    source: Mary_Wellesley
  AssignClass (6b7ddfaf-9480-42e6-aa43-c05fbc881256)
 Call ID: 6b7ddfaf-9480-42e6-aa43-c05fbc881256
  Args:
    type: :Person
    source: Mary_Wellesley
  AddTriple (07ee7d1c-c2e2-4c55-b7e7-537564f86cb4)
 Call ID: 07ee7d1c-c2e2-4c55-b7e7-537564f86cb4
  Args:
    relation: :hasBrother
    source: Charlotte_Wellesley
    target: Arthur_Wellesley
  AddTriple (ae0620e5-d82d-4b11-946d-84074752a94b)
 Call ID: ae0620e5-d82d-4b11-946d-84074752a94b
  Args:
    relation: :hasSister
    target: Mary_Wellesley
    source: Charlotte_Wellesley
  AssignClass (f0e670cb-eb68-4343-bba3-cbbc45ece7c2)
 Call ID: f0e670cb-eb68-4343-bba3-cbbc45ece7c2
  Args:
    source: Alejandro_Santo_Domingo
    type: :Man
  AssignClass (dbaaa72b-9de7-46a5-81f8-6d8230fda3f2)
 Call ID: dbaaa72b-9de7-46a5-81f8-6d8230fda3f2
  Args:
    source: Alejandro_Santo_Domingo
    type: :Person
  AddLiteral (2297a98d-2dda-48fd-a968-ac1c80cd9e5c)
 Call ID: 2297a98d-2dda-48fd-a968-ac1c80cd9e5c
  Args:
    source: Charlotte_Wellesley
    relation: :hasMarriageYear
    literal_value: 2016
    literal_type: xsd:integer
  AddTriple (9f49cca0-a502-4dc1-98c0-75a7fd112aae)
 Call ID: 9f49cca0-a502-4dc1-98c0-75a7fd112aae
  Args:
    relation: :hasRelation
    source: Charlotte_Wellesley
    target: Alejandro_Santo_Domingo
  Finish (814ea095-c747-4794-ae76-249e37fde1f7)
 Call ID: 814ea095-c747-4794-ae76-249e37fde1f7
  Args: