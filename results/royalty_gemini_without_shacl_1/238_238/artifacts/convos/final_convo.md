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
Franz Ulrich, 11th Prince Kinsky of Wchinitz and Tettau (German: Franz Ulrich Johannes Clemens Christophorus Antonius Bonaventura Maria Fürst Kinsky von Wchinitz und Tettau; 7 October 1936 – 2 April 2009) was the titular Prince Kinsky of Wchinitz and Tettau as well the head of an ancient House of Kinsky.
Early life

Franz Ulrich was born at Vienna, Federal State of Austria, as the youngest son of Ulrich, 10th Prince Kinsky of Wchinitz and Tettau by his second marriage to Baroness Marie Julia Mathilde von dem Bussche-Haddenhausen (1900–1974), the eldest daughter of Baron Hilmar von dem Bussche-Haddenhausen.
Franz Ulrich became the titular Prince upon the death of his father in 1938.
He was first cousin of Countess Marie Aglaë Kinsky of Wchinitz and Tettau who later became Princess consort of Liechtenstein, and second cousin of Claus von Amsberg, Prince consort of Queen Beatrix of the Netherlands, both descendants of Baron Julius von dem Bussche-Haddenhausen.
In 1942, Franz Ulrich inherited several estates from the Kinsky family, including the Kinsky Palace in Old Town Square in Prague.
Starting in 2003, Franz Ulrich complained against various Czech courts for the return of the assets.
Marriage and family

Franz Ulrich married on 14 April 1965 in Buenos Aires to Roberta Cavanagh (1942–2002), daughter of Roberto Cavanagh and his wife, Anne Rowell.
After Kinsky's death, his son and his widow, Countess Helena Victoria Hutten-Czapska entered a legal dispute over Kinsky's properties.
Later life

The Prince died on 2 April 2009, aged 72.



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
  AssignClass (c3cba326-6e81-4901-a4a1-f50f8cf8ab8f)
 Call ID: c3cba326-6e81-4901-a4a1-f50f8cf8ab8f
  Args:
    type: :Man
    source: Franz_Ulrich_Kinsky
  AssignClass (ee3d146d-58d1-4012-b171-ce68abf2d5dc)
 Call ID: ee3d146d-58d1-4012-b171-ce68abf2d5dc
  Args:
    type: :Man
    source: Ulrich_Kinsky
  AssignClass (41e62385-2465-4e0b-af76-698b0e0eb5bf)
 Call ID: 41e62385-2465-4e0b-af76-698b0e0eb5bf
  Args:
    type: :Woman
    source: Marie_Julia_Mathilde_von_dem_Bussche-Haddenhausen
  AssignClass (60095059-56c4-4f7a-9ff5-865c8b6d9452)
 Call ID: 60095059-56c4-4f7a-9ff5-865c8b6d9452
  Args:
    type: :Man
    source: Hilmar_von_dem_Bussche-Haddenhausen
  AssignClass (22bff3bd-1869-4da8-9e69-38d86729cd4f)
 Call ID: 22bff3bd-1869-4da8-9e69-38d86729cd4f
  Args:
    type: :Woman
    source: Roberta_Cavanagh
  AssignClass (32460a15-f35c-4e14-aea5-2dcdd9e5fa17)
 Call ID: 32460a15-f35c-4e14-aea5-2dcdd9e5fa17
  Args:
    type: :Man
    source: Roberto_Cavanagh
  AssignClass (b9e05ae7-ab16-4613-bab9-93b252b9d19d)
 Call ID: b9e05ae7-ab16-4613-bab9-93b252b9d19d
  Args:
    type: :Woman
    source: Anne_Rowell
  AssignClass (2bb0fc35-b93a-4301-82a2-6d4172e8b10d)
 Call ID: 2bb0fc35-b93a-4301-82a2-6d4172e8b10d
  Args:
    type: :Woman
    source: Helena_Victoria_Hutten-Czapska
  AddLiteral (094a5bd4-a29d-40e1-8c46-921b7b3a48f5)
 Call ID: 094a5bd4-a29d-40e1-8c46-921b7b3a48f5
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1936
    source: Franz_Ulrich_Kinsky
  AddLiteral (5a631cfe-d3b4-4336-b22c-e5574c689cc4)
 Call ID: 5a631cfe-d3b4-4336-b22c-e5574c689cc4
  Args:
    source: Franz_Ulrich_Kinsky
    literal_type: xsd:integer
    literal_value: 2009
    relation: :hasDeathYear
  AddLiteral (e6855474-538f-44a3-8d8f-4589814aaf56)
 Call ID: e6855474-538f-44a3-8d8f-4589814aaf56
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1900
    source: Marie_Julia_Mathilde_von_dem_Bussche-Haddenhausen
  AddLiteral (856e9494-52cc-4978-bb53-9e7e64d9b30d)
 Call ID: 856e9494-52cc-4978-bb53-9e7e64d9b30d
  Args:
    source: Marie_Julia_Mathilde_von_dem_Bussche-Haddenhausen
    literal_type: xsd:integer
    literal_value: 1974
    relation: :hasDeathYear
  AddLiteral (48f4ad8c-9be6-494c-b9af-a092128afa27)
 Call ID: 48f4ad8c-9be6-494c-b9af-a092128afa27
  Args:
    relation: :hasBirthYear
    source: Roberta_Cavanagh
    literal_type: xsd:integer
    literal_value: 1942
  AddLiteral (876b4d95-ee91-45e2-a99d-f87ab360d942)
 Call ID: 876b4d95-ee91-45e2-a99d-f87ab360d942
  Args:
    relation: :hasDeathYear
    source: Roberta_Cavanagh
    literal_type: xsd:integer
    literal_value: 2002
  AddLiteral (f3ce1e4e-b584-424d-911c-0d23dfefbda9)
 Call ID: f3ce1e4e-b584-424d-911c-0d23dfefbda9
  Args:
    literal_type: xsd:integer
    literal_value: 1965
    source: Franz_Ulrich_Kinsky
    relation: :hasMarriageYear
  AddTriple (f57459c8-8c19-4777-af69-d622f0e77e09)
 Call ID: f57459c8-8c19-4777-af69-d622f0e77e09
  Args:
    target: Ulrich_Kinsky
    source: Franz_Ulrich_Kinsky
    relation: :hasFather
  AddTriple (cd6c4c00-96c3-4a93-8aac-77155bf7ca6e)
 Call ID: cd6c4c00-96c3-4a93-8aac-77155bf7ca6e
  Args:
    relation: :hasMother
    target: Marie_Julia_Mathilde_von_dem_Bussche-Haddenhausen
    source: Franz_Ulrich_Kinsky
  AddTriple (3f8fc4de-bcc4-4e54-af9d-09b9e488967f)
 Call ID: 3f8fc4de-bcc4-4e54-af9d-09b9e488967f
  Args:
    relation: :hasFather
    source: Marie_Julia_Mathilde_von_dem_Bussche-Haddenhausen
    target: Hilmar_von_dem_Bussche-Haddenhausen
  AddTriple (830fc6cd-137e-4bc9-b2fe-4193f082b0f9)
 Call ID: 830fc6cd-137e-4bc9-b2fe-4193f082b0f9
  Args:
    relation: :hasFather
    source: Roberta_Cavanagh
    target: Roberto_Cavanagh
  AddTriple (18e14557-fd53-4a62-a182-b5851f7713f9)
 Call ID: 18e14557-fd53-4a62-a182-b5851f7713f9
  Args:
    source: Roberta_Cavanagh
    target: Anne_Rowell
    relation: :hasMother
  AddTriple (6406384f-6857-4261-a177-8997d84135e3)
 Call ID: 6406384f-6857-4261-a177-8997d84135e3
  Args:
    relation: :hasRelation
    target: Roberta_Cavanagh
    source: Franz_Ulrich_Kinsky
  AddTriple (14dd9c6e-82b1-4ddb-b03b-670d2a04f366)
 Call ID: 14dd9c6e-82b1-4ddb-b03b-670d2a04f366
  Args:
    source: Franz_Ulrich_Kinsky
    target: Helena_Victoria_Hutten-Czapska
    relation: :hasRelation
  Finish (4e99566d-0fb2-48df-8ca8-d54133fa0555)
 Call ID: 4e99566d-0fb2-48df-8ca8-d54133fa0555
  Args: