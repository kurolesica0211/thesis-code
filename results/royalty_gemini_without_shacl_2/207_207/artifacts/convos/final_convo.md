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
Princess Marie Louise of Hanover and Cumberland (11 October 1879 – 31 January 1948) was the eldest child of Ernest Augustus, Crown Prince of Hanover, and Princess Thyra of Denmark, the youngest daughter of Christian IX of Denmark and Louise of Hesse-Kassel.
Through her father, Marie Louise was a great-great-granddaughter of George III of the United Kingdom and Charlotte of Mecklenburg-Strelitz.
Marriage and children

Marie Louise married Prince Maximilian of Baden (1867–1929), her third cousin twice removed, on 10 July 1900 in Gmunden, Austria-Hungary.
He was the son of Prince Wilhelm of Baden and Princess Maria Maximilianovna of Leuchtenberg and became a first cousin twice removed of Napoleon III of France.
Marie Louise and Maximilian had one daughter and one son:


Ancestry

References

External links



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
  AssignClass (2e54bba0-b9e2-4932-9f15-d537b2adc09d)
 Call ID: 2e54bba0-b9e2-4932-9f15-d537b2adc09d
  Args:
    source: Marie_Louise_of_Hanover_and_Cumberland
    type: :Woman
  AssignClass (7e097f37-f4a2-45d6-8924-8906ff52f877)
 Call ID: 7e097f37-f4a2-45d6-8924-8906ff52f877
  Args:
    type: :Person
    source: Marie_Louise_of_Hanover_and_Cumberland
  AddLiteral (8c00b9a2-f9df-4f07-a117-fdf90d3b886c)
 Call ID: 8c00b9a2-f9df-4f07-a117-fdf90d3b886c
  Args:
    source: Marie_Louise_of_Hanover_and_Cumberland
    literal_type: xsd:integer
    literal_value: 1879
    relation: :hasBirthYear
  AddLiteral (3a1d2e4e-caea-4186-88c4-f381b2ad9ca0)
 Call ID: 3a1d2e4e-caea-4186-88c4-f381b2ad9ca0
  Args:
    source: Marie_Louise_of_Hanover_and_Cumberland
    literal_type: xsd:integer
    literal_value: 1948
    relation: :hasDeathYear
  AssignClass (69fc6c77-36d5-4322-8c35-75c0e63a3524)
 Call ID: 69fc6c77-36d5-4322-8c35-75c0e63a3524
  Args:
    type: :Man
    source: Ernest_Augustus_Crown_Prince_of_Hanover
  AssignClass (0f0c9baf-81e2-4c1b-a507-498bd2d57e25)
 Call ID: 0f0c9baf-81e2-4c1b-a507-498bd2d57e25
  Args:
    type: :Person
    source: Ernest_Augustus_Crown_Prince_of_Hanover
  AssignClass (d1217168-ecbd-4e02-8286-ce2a4fa7cca8)
 Call ID: d1217168-ecbd-4e02-8286-ce2a4fa7cca8
  Args:
    type: :Woman
    source: Princess_Thyra_of_Denmark
  AssignClass (0becd0b9-375d-4777-89ab-16fe2a094956)
 Call ID: 0becd0b9-375d-4777-89ab-16fe2a094956
  Args:
    type: :Person
    source: Princess_Thyra_of_Denmark
  AddTriple (879eb312-53f5-4458-941a-663dcb2cb3f7)
 Call ID: 879eb312-53f5-4458-941a-663dcb2cb3f7
  Args:
    relation: :hasFather
    target: Ernest_Augustus_Crown_Prince_of_Hanover
    source: Marie_Louise_of_Hanover_and_Cumberland
  AddTriple (079de89d-67f0-485a-91b1-da9e1df5611f)
 Call ID: 079de89d-67f0-485a-91b1-da9e1df5611f
  Args:
    relation: :hasMother
    target: Princess_Thyra_of_Denmark
    source: Marie_Louise_of_Hanover_and_Cumberland
  AssignClass (3b89fd71-4eb6-44b2-a1a8-fa69a336df1b)
 Call ID: 3b89fd71-4eb6-44b2-a1a8-fa69a336df1b
  Args:
    source: Christian_IX_of_Denmark
    type: :Man
  AssignClass (dc42b0ac-b3ce-4393-9754-61ff8f82bf6a)
 Call ID: dc42b0ac-b3ce-4393-9754-61ff8f82bf6a
  Args:
    type: :Person
    source: Christian_IX_of_Denmark
  AssignClass (7663afae-a919-426a-870f-eaeefc20a68d)
 Call ID: 7663afae-a919-426a-870f-eaeefc20a68d
  Args:
    type: :Woman
    source: Louise_of_Hesse_Kassel
  AssignClass (3de554be-b84c-4636-8292-d9e5e4b7f311)
 Call ID: 3de554be-b84c-4636-8292-d9e5e4b7f311
  Args:
    type: :Person
    source: Louise_of_Hesse_Kassel
  AddTriple (5c8e79ec-fd0d-4546-8493-d1b7893d5e36)
 Call ID: 5c8e79ec-fd0d-4546-8493-d1b7893d5e36
  Args:
    source: Princess_Thyra_of_Denmark
    relation: :hasFather
    target: Christian_IX_of_Denmark
  AddTriple (36c9c3b9-cf7b-4d72-9f36-baa75bd15f53)
 Call ID: 36c9c3b9-cf7b-4d72-9f36-baa75bd15f53
  Args:
    source: Princess_Thyra_of_Denmark
    target: Louise_of_Hesse_Kassel
    relation: :hasMother
  AssignClass (84ae1443-efbf-416a-a45d-e74faa892ab8)
 Call ID: 84ae1443-efbf-416a-a45d-e74faa892ab8
  Args:
    type: :Man
    source: George_III_of_the_United_Kingdom
  AssignClass (ca6f111e-4f38-493d-9c99-e1694b01bd37)
 Call ID: ca6f111e-4f38-493d-9c99-e1694b01bd37
  Args:
    source: George_III_of_the_United_Kingdom
    type: :Person
  AssignClass (3f22ef4d-959e-496c-b7c1-b7716e570b2f)
 Call ID: 3f22ef4d-959e-496c-b7c1-b7716e570b2f
  Args:
    source: Charlotte_of_Mecklenburg_Strelitz
    type: :Woman
  AssignClass (06f63590-e821-4ee1-8968-1dd1ec610494)
 Call ID: 06f63590-e821-4ee1-8968-1dd1ec610494
  Args:
    source: Charlotte_of_Mecklenburg_Strelitz
    type: :Person
  AddTriple (b29c58c4-df80-4034-9e69-71fe1f4ad0be)
 Call ID: b29c58c4-df80-4034-9e69-71fe1f4ad0be
  Args:
    source: Marie_Louise_of_Hanover_and_Cumberland
    relation: :hasAncestor
    target: George_III_of_the_United_Kingdom
  AddTriple (6fb20ea0-1547-4d06-85fc-4eff2bb659a0)
 Call ID: 6fb20ea0-1547-4d06-85fc-4eff2bb659a0
  Args:
    source: Marie_Louise_of_Hanover_and_Cumberland
    target: Charlotte_of_Mecklenburg_Strelitz
    relation: :hasAncestor
  AssignClass (ae4bc699-0442-420c-a1fa-1b68d0ee49b2)
 Call ID: ae4bc699-0442-420c-a1fa-1b68d0ee49b2
  Args:
    type: :Man
    source: Prince_Maximilian_of_Baden
  AssignClass (fff257d6-a485-4d73-8822-603b70abe4ab)
 Call ID: fff257d6-a485-4d73-8822-603b70abe4ab
  Args:
    type: :Person
    source: Prince_Maximilian_of_Baden
  AddLiteral (989b139d-6593-424d-aaf8-18715cf89716)
 Call ID: 989b139d-6593-424d-aaf8-18715cf89716
  Args:
    source: Prince_Maximilian_of_Baden
    literal_value: 1867
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (b3df6836-7c51-4d48-8d5f-909b409f9af3)
 Call ID: b3df6836-7c51-4d48-8d5f-909b409f9af3
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 1929
    source: Prince_Maximilian_of_Baden
  AddLiteral (4369d792-70ca-4a7a-be12-548ff048b56a)
 Call ID: 4369d792-70ca-4a7a-be12-548ff048b56a
  Args:
    source: Marie_Louise_of_Hanover_and_Cumberland
    literal_type: xsd:integer
    literal_value: 1900
    relation: :hasMarriageYear
  AddTriple (80fe4116-d29b-4806-b8bf-992ac3240604)
 Call ID: 80fe4116-d29b-4806-b8bf-992ac3240604
  Args:
    source: Marie_Louise_of_Hanover_and_Cumberland
    target: Prince_Maximilian_of_Baden
    relation: :hasRelation
  AssignClass (838253fd-12a6-4877-a24e-78120341f814)
 Call ID: 838253fd-12a6-4877-a24e-78120341f814
  Args:
    type: :Man
    source: Prince_Wilhelm_of_Baden
  AssignClass (9a35cc2a-de8e-4349-a193-e9bb71f34d0a)
 Call ID: 9a35cc2a-de8e-4349-a193-e9bb71f34d0a
  Args:
    type: :Person
    source: Prince_Wilhelm_of_Baden
  AssignClass (f58aa76d-0a41-4b09-8dbd-9662984cf2f0)
 Call ID: f58aa76d-0a41-4b09-8dbd-9662984cf2f0
  Args:
    source: Princess_Maria_Maximilianovna_of_Leuchtenberg
    type: :Woman
  AssignClass (72f131fe-2c06-43fe-8c24-49f3d022b78e)
 Call ID: 72f131fe-2c06-43fe-8c24-49f3d022b78e
  Args:
    source: Princess_Maria_Maximilianovna_of_Leuchtenberg
    type: :Person
  AddTriple (33d9c51d-8c99-473e-a432-8b502125e64c)
 Call ID: 33d9c51d-8c99-473e-a432-8b502125e64c
  Args:
    target: Prince_Wilhelm_of_Baden
    relation: :hasFather
    source: Prince_Maximilian_of_Baden
  AddTriple (e913681f-d067-42ea-acba-8a9bb2d7cee5)
 Call ID: e913681f-d067-42ea-acba-8a9bb2d7cee5
  Args:
    source: Prince_Maximilian_of_Baden
    relation: :hasMother
    target: Princess_Maria_Maximilianovna_of_Leuchtenberg
  AssignClass (f59b0bdf-0027-47a2-85ec-a0bdd89863dd)
 Call ID: f59b0bdf-0027-47a2-85ec-a0bdd89863dd
  Args:
    source: Napoleon_III_of_France
    type: :Man
  AssignClass (c5f9c315-8f96-40cc-8411-28bea33953f3)
 Call ID: c5f9c315-8f96-40cc-8411-28bea33953f3
  Args:
    type: :Person
    source: Napoleon_III_of_France
  Finish (77841660-24bc-406b-a107-4454add5f443)
 Call ID: 77841660-24bc-406b-a107-4454add5f443
  Args: