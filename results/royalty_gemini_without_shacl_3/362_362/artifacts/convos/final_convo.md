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
Don Alessandro Torlonia, 5th Prince of Civitella-Cesi (7 December 1911 – 1 May/12 May 1986) was an Italian banking heir and a member of the House of Torlonia.
About

Born in Rome on 7 December 1911, Torlonia was the son of Marino Torlonia, 4th Prince di Civitella-Cesi and his American wife, Mary Elsie Moore.
Don Alessandro's youngest sister was Donna Marina Torlonia di Civitella-Cesi, grandmother of the American actress Brooke Shields.
In 1941, when his mother was dying in New York City, Torlonia took a high speed boat from Portugal and was arrested in error by FBI, thinking he was an enemy of the state and taken to Ellis Island.
Not to be confused with his cousin with the same name, Alessandro Torlonia (1925–2017), Prince of Fucino and Prince assistant to the papal throne, head of another branch of the family.
In the 1980s, this cousin Torlonia held the title as the "richest man in Rome", as he was the heir to a banking fortune and owner of the famous Torlonia Collection of ancient art.
He died in the Palazzo Nuñez-Torlonia, Rome, in 1986.
Marriage and children

On 14 January 1935, Don Alessandro morganatically married in Rome the Infanta Beatriz of Spain (1909–2002), a daughter of King Alfonso XIII of Spain and of Princess Victoria Eugenie of Battenberg.



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
  AssignClass (cf564a2b-0b20-4c78-92fa-ed991eed12f2)
 Call ID: cf564a2b-0b20-4c78-92fa-ed991eed12f2
  Args:
    type: :Man
    source: :AlessandroTorlonia
  AssignClass (467ea433-1a43-4c9c-833c-af06558b4782)
 Call ID: 467ea433-1a43-4c9c-833c-af06558b4782
  Args:
    source: :AlessandroTorlonia
    type: :Person
  AddLiteral (cc412685-eebc-4593-96bd-a5d1646f2824)
 Call ID: cc412685-eebc-4593-96bd-a5d1646f2824
  Args:
    source: :AlessandroTorlonia
    literal_type: xsd:integer
    literal_value: 1911
    relation: :hasBirthYear
  AddLiteral (fd810c43-cafa-4cde-ac66-292c917fb690)
 Call ID: fd810c43-cafa-4cde-ac66-292c917fb690
  Args:
    literal_value: 1986
    relation: :hasDeathYear
    source: :AlessandroTorlonia
    literal_type: xsd:integer
  AssignClass (7c5e894e-822e-453d-b6c4-45b74e90067a)
 Call ID: 7c5e894e-822e-453d-b6c4-45b74e90067a
  Args:
    type: :Man
    source: :MarinoTorlonia
  AssignClass (f68d7b5c-0c82-4e77-b953-ec5e563a0c1b)
 Call ID: f68d7b5c-0c82-4e77-b953-ec5e563a0c1b
  Args:
    type: :Person
    source: :MarinoTorlonia
  AssignClass (6a0600e9-b2fc-4d94-8114-e0de8fd283e5)
 Call ID: 6a0600e9-b2fc-4d94-8114-e0de8fd283e5
  Args:
    source: :MaryElsieMoore
    type: :Woman
  AssignClass (184572f2-d7b5-4627-bc3d-b549b5ed0eff)
 Call ID: 184572f2-d7b5-4627-bc3d-b549b5ed0eff
  Args:
    source: :MaryElsieMoore
    type: :Person
  AddTriple (951a59af-4c03-4bfd-a6e0-e110acb13140)
 Call ID: 951a59af-4c03-4bfd-a6e0-e110acb13140
  Args:
    target: :MarinoTorlonia
    source: :AlessandroTorlonia
    relation: :hasFather
  AddTriple (1db138c2-a049-402a-9ffa-e5a5969214e4)
 Call ID: 1db138c2-a049-402a-9ffa-e5a5969214e4
  Args:
    target: :MaryElsieMoore
    source: :AlessandroTorlonia
    relation: :hasMother
  AssignClass (92543931-21ad-4e99-9627-6b7fe7f14858)
 Call ID: 92543931-21ad-4e99-9627-6b7fe7f14858
  Args:
    type: :Woman
    source: :MarinaTorlonia
  AssignClass (2651667f-4231-488e-aecb-f527eefe120c)
 Call ID: 2651667f-4231-488e-aecb-f527eefe120c
  Args:
    source: :MarinaTorlonia
    type: :Person
  AddTriple (dae4d638-5f23-4146-b431-82566769dd34)
 Call ID: dae4d638-5f23-4146-b431-82566769dd34
  Args:
    relation: :hasSister
    target: :MarinaTorlonia
    source: :AlessandroTorlonia
  AddTriple (29b79011-a02d-45f6-9134-60b313c1a3e1)
 Call ID: 29b79011-a02d-45f6-9134-60b313c1a3e1
  Args:
    relation: :hasFather
    target: :MarinoTorlonia
    source: :MarinaTorlonia
  AddTriple (68632f09-5991-4cd7-a743-0d3c6837df73)
 Call ID: 68632f09-5991-4cd7-a743-0d3c6837df73
  Args:
    relation: :hasMother
    target: :MaryElsieMoore
    source: :MarinaTorlonia
  AssignClass (fd189f24-010c-4ad0-b5a7-55ac70290b5b)
 Call ID: fd189f24-010c-4ad0-b5a7-55ac70290b5b
  Args:
    type: :Woman
    source: :BeatrizOfSpain
  AssignClass (6b8fadd5-f6bd-4408-a6a1-d02a50158ec8)
 Call ID: 6b8fadd5-f6bd-4408-a6a1-d02a50158ec8
  Args:
    type: :Person
    source: :BeatrizOfSpain
  AddLiteral (37b33c72-e4b5-4d52-b5bf-f4b8319a3a7a)
 Call ID: 37b33c72-e4b5-4d52-b5bf-f4b8319a3a7a
  Args:
    literal_type: xsd:integer
    source: :AlessandroTorlonia
    relation: :hasMarriageYear
    literal_value: 1935
  AddTriple (9b895447-a6d6-4976-8f76-7328cfded0fa)
 Call ID: 9b895447-a6d6-4976-8f76-7328cfded0fa
  Args:
    target: :BeatrizOfSpain
    source: :AlessandroTorlonia
    relation: :hasRelation
  AssignClass (b69d1f76-b1d0-416a-aa36-39e529712b99)
 Call ID: b69d1f76-b1d0-416a-aa36-39e529712b99
  Args:
    source: :AlfonsoXIIIOfSpain
    type: :Man
  AssignClass (d80be4be-4506-4f77-b42d-8e52422e9b36)
 Call ID: d80be4be-4506-4f77-b42d-8e52422e9b36
  Args:
    source: :AlfonsoXIIIOfSpain
    type: :Person
  AssignClass (f224534c-4c93-45fa-a41b-7f05a6d1fa18)
 Call ID: f224534c-4c93-45fa-a41b-7f05a6d1fa18
  Args:
    source: :VictoriaEugenieOfBattenberg
    type: :Woman
  AssignClass (a8c60c9d-c15d-4f43-88c9-2de62c56aee4)
 Call ID: a8c60c9d-c15d-4f43-88c9-2de62c56aee4
  Args:
    type: :Person
    source: :VictoriaEugenieOfBattenberg
  AddTriple (c3c0d2fd-79c8-46e8-938d-41b4ec9911c5)
 Call ID: c3c0d2fd-79c8-46e8-938d-41b4ec9911c5
  Args:
    source: :BeatrizOfSpain
    target: :AlfonsoXIIIOfSpain
    relation: :hasFather
  AddTriple (9448d46c-3f35-4691-a0a0-e8f056cb2085)
 Call ID: 9448d46c-3f35-4691-a0a0-e8f056cb2085
  Args:
    source: :BeatrizOfSpain
    target: :VictoriaEugenieOfBattenberg
    relation: :hasMother
  Finish (78197ceb-0928-49f3-9cd4-7847d03259e0)
 Call ID: 78197ceb-0928-49f3-9cd4-7847d03259e0
  Args: