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
  AssignClass (bbd2759a-c9a8-4db3-98f2-6bacaac77f85)
 Call ID: bbd2759a-c9a8-4db3-98f2-6bacaac77f85
  Args:
    source: Franz_Ulrich_Kinsky
    type: :Man
  AssignClass (7fec0be4-456a-407a-8d01-11f58d808e08)
 Call ID: 7fec0be4-456a-407a-8d01-11f58d808e08
  Args:
    type: :Person
    source: Franz_Ulrich_Kinsky
  AddLiteral (914e9b33-d14e-4deb-95db-55fe68fcfeed)
 Call ID: 914e9b33-d14e-4deb-95db-55fe68fcfeed
  Args:
    source: Franz_Ulrich_Kinsky
    relation: :hasBirthYear
    literal_value: 1936
    literal_type: xsd:integer
  AddLiteral (ffa86cdc-153c-4e61-a693-0165d2f2273e)
 Call ID: ffa86cdc-153c-4e61-a693-0165d2f2273e
  Args:
    relation: :hasDeathYear
    source: Franz_Ulrich_Kinsky
    literal_value: 2009
    literal_type: xsd:integer
  AssignClass (0cc41d10-07e5-442d-a063-03d33c2bc17f)
 Call ID: 0cc41d10-07e5-442d-a063-03d33c2bc17f
  Args:
    type: :Man
    source: Ulrich_Kinsky
  AssignClass (b729d30f-ca80-4974-af71-4d79c45cfce6)
 Call ID: b729d30f-ca80-4974-af71-4d79c45cfce6
  Args:
    type: :Person
    source: Ulrich_Kinsky
  AssignClass (0d344ad2-6086-42da-b753-28564bc244ac)
 Call ID: 0d344ad2-6086-42da-b753-28564bc244ac
  Args:
    type: :Woman
    source: Marie_Julia_Mathilde_von_dem_Bussche-Haddenhausen
  AssignClass (025ee4c7-af35-47c0-a8b1-4b55c55c70cd)
 Call ID: 025ee4c7-af35-47c0-a8b1-4b55c55c70cd
  Args:
    type: :Person
    source: Marie_Julia_Mathilde_von_dem_Bussche-Haddenhausen
  AddTriple (1aff3083-893c-407d-9d2a-6e523f0569bc)
 Call ID: 1aff3083-893c-407d-9d2a-6e523f0569bc
  Args:
    relation: :hasFather
    source: Franz_Ulrich_Kinsky
    target: Ulrich_Kinsky
  AddTriple (e9ac6067-eb36-474f-b088-26e623df95d0)
 Call ID: e9ac6067-eb36-474f-b088-26e623df95d0
  Args:
    target: Marie_Julia_Mathilde_von_dem_Bussche-Haddenhausen
    relation: :hasMother
    source: Franz_Ulrich_Kinsky
  AssignClass (0a0cab73-35b7-4559-9f7e-4d29ff0e4803)
 Call ID: 0a0cab73-35b7-4559-9f7e-4d29ff0e4803
  Args:
    type: :Man
    source: Hilmar_von_dem_Bussche-Haddenhausen
  AssignClass (e0fe947f-034f-41ca-87b6-499049e701c3)
 Call ID: e0fe947f-034f-41ca-87b6-499049e701c3
  Args:
    source: Hilmar_von_dem_Bussche-Haddenhausen
    type: :Person
  AddTriple (f248f378-89b2-48f3-bef8-53c9f58937fa)
 Call ID: f248f378-89b2-48f3-bef8-53c9f58937fa
  Args:
    source: Marie_Julia_Mathilde_von_dem_Bussche-Haddenhausen
    relation: :hasFather
    target: Hilmar_von_dem_Bussche-Haddenhausen
  AssignClass (46d81dba-801c-4dc6-8491-8ff390bd9414)
 Call ID: 46d81dba-801c-4dc6-8491-8ff390bd9414
  Args:
    type: :Woman
    source: Roberta_Cavanagh
  AssignClass (f3bddda1-222e-49db-a097-caf94d2ada62)
 Call ID: f3bddda1-222e-49db-a097-caf94d2ada62
  Args:
    source: Roberta_Cavanagh
    type: :Person
  AddLiteral (e1bbdf92-f686-4bb1-990b-0af6100515ac)
 Call ID: e1bbdf92-f686-4bb1-990b-0af6100515ac
  Args:
    source: Franz_Ulrich_Kinsky
    relation: :hasMarriageYear
    literal_value: 1965
    literal_type: xsd:integer
  AddTriple (2ff7c941-85bb-4727-baee-bcca2535d9ca)
 Call ID: 2ff7c941-85bb-4727-baee-bcca2535d9ca
  Args:
    relation: :hasRelation
    source: Franz_Ulrich_Kinsky
    target: Roberta_Cavanagh
  AssignClass (0ae40294-fb03-42d0-b6c0-ff2a8aa251e6)
 Call ID: 0ae40294-fb03-42d0-b6c0-ff2a8aa251e6
  Args:
    type: :Man
    source: Roberto_Cavanagh
  AssignClass (549da279-476b-44f4-9064-0a7c23210472)
 Call ID: 549da279-476b-44f4-9064-0a7c23210472
  Args:
    source: Roberto_Cavanagh
    type: :Person
  AssignClass (40b2d43f-2add-4a8f-ac03-32631c37652d)
 Call ID: 40b2d43f-2add-4a8f-ac03-32631c37652d
  Args:
    type: :Woman
    source: Anne_Rowell
  AssignClass (d799c45d-297d-4987-a61a-5c0cd3ec9a1a)
 Call ID: d799c45d-297d-4987-a61a-5c0cd3ec9a1a
  Args:
    type: :Person
    source: Anne_Rowell
  AddTriple (997aeb70-142a-4b9d-a9c3-16519a00fb0b)
 Call ID: 997aeb70-142a-4b9d-a9c3-16519a00fb0b
  Args:
    target: Roberto_Cavanagh
    relation: :hasFather
    source: Roberta_Cavanagh
  AddTriple (ec3b05e9-88de-4518-a744-7d6bc659f471)
 Call ID: ec3b05e9-88de-4518-a744-7d6bc659f471
  Args:
    relation: :hasMother
    source: Roberta_Cavanagh
    target: Anne_Rowell
  AssignClass (f5e88d2b-c8b2-4883-8f6c-71b80c13ed8e)
 Call ID: f5e88d2b-c8b2-4883-8f6c-71b80c13ed8e
  Args:
    source: Helena_Victoria_Hutten-Czapska
    type: :Woman
  AssignClass (bc0c6729-01fc-4f8e-8d12-9ac9afad2a0d)
 Call ID: bc0c6729-01fc-4f8e-8d12-9ac9afad2a0d
  Args:
    type: :Person
    source: Helena_Victoria_Hutten-Czapska
  Finish (5b01974c-0dd3-417a-b892-861fb6cfe3c4)
 Call ID: 5b01974c-0dd3-417a-b892-861fb6cfe3c4
  Args: