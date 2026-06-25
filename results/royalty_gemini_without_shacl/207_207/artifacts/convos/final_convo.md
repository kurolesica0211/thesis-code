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
  AssignClass (5207ed44-374a-4fb7-a92c-f8845bbd38fe)
 Call ID: 5207ed44-374a-4fb7-a92c-f8845bbd38fe
  Args:
    type: :Woman
    source: :Marie_Louise_of_Hanover_and_Cumberland
  AssignClass (60f1482b-9ddb-4043-8090-3551c0093eaf)
 Call ID: 60f1482b-9ddb-4043-8090-3551c0093eaf
  Args:
    source: :Marie_Louise_of_Hanover_and_Cumberland
    type: :Person
  AddLiteral (ea9a21da-f9d6-46f3-8b5d-eeae42b42c49)
 Call ID: ea9a21da-f9d6-46f3-8b5d-eeae42b42c49
  Args:
    literal_type: xsd:integer
    source: :Marie_Louise_of_Hanover_and_Cumberland
    literal_value: 1879
    relation: :hasBirthYear
  AddLiteral (137258a3-66e4-4266-984f-5d72a670c9bf)
 Call ID: 137258a3-66e4-4266-984f-5d72a670c9bf
  Args:
    relation: :hasDeathYear
    source: :Marie_Louise_of_Hanover_and_Cumberland
    literal_value: 1948
    literal_type: xsd:integer
  AssignClass (167d87ac-7c26-417e-913e-8e3a068bb048)
 Call ID: 167d87ac-7c26-417e-913e-8e3a068bb048
  Args:
    source: :Ernest_Augustus_Crown_Prince_of_Hanover
    type: :Man
  AssignClass (887d6ade-385f-4e4e-81bb-40e2567dbe50)
 Call ID: 887d6ade-385f-4e4e-81bb-40e2567dbe50
  Args:
    type: :Person
    source: :Ernest_Augustus_Crown_Prince_of_Hanover
  AssignClass (50b6a681-5b23-4e43-b38b-7c92830341db)
 Call ID: 50b6a681-5b23-4e43-b38b-7c92830341db
  Args:
    source: :Princess_Thyra_of_Denmark
    type: :Woman
  AssignClass (0c2f018b-6dfd-4bc5-85dc-da1781740468)
 Call ID: 0c2f018b-6dfd-4bc5-85dc-da1781740468
  Args:
    source: :Princess_Thyra_of_Denmark
    type: :Person
  AddTriple (6d95acbc-45bd-46fe-a324-3a769ddecb9f)
 Call ID: 6d95acbc-45bd-46fe-a324-3a769ddecb9f
  Args:
    relation: :hasFather
    source: :Marie_Louise_of_Hanover_and_Cumberland
    target: :Ernest_Augustus_Crown_Prince_of_Hanover
  AddTriple (2a6a902f-1f81-4827-9e2f-04d047b575b9)
 Call ID: 2a6a902f-1f81-4827-9e2f-04d047b575b9
  Args:
    source: :Marie_Louise_of_Hanover_and_Cumberland
    relation: :hasMother
    target: :Princess_Thyra_of_Denmark
  AssignClass (bb7e42ba-3c93-47c1-877c-4ce5943cadf0)
 Call ID: bb7e42ba-3c93-47c1-877c-4ce5943cadf0
  Args:
    type: :Man
    source: :Christian_IX_of_Denmark
  AssignClass (6129b567-85be-4e73-9a65-5a5bd4f93468)
 Call ID: 6129b567-85be-4e73-9a65-5a5bd4f93468
  Args:
    source: :Christian_IX_of_Denmark
    type: :Person
  AssignClass (7f87df29-2e1a-49ad-a0dd-27a3b67e3aeb)
 Call ID: 7f87df29-2e1a-49ad-a0dd-27a3b67e3aeb
  Args:
    source: :Louise_of_Hesse_Kassel
    type: :Woman
  AssignClass (12685c22-be15-44df-8ff6-353b1bdd0c8a)
 Call ID: 12685c22-be15-44df-8ff6-353b1bdd0c8a
  Args:
    source: :Louise_of_Hesse_Kassel
    type: :Person
  AddTriple (684afac0-faed-4ec5-a6df-d0cb0243f17d)
 Call ID: 684afac0-faed-4ec5-a6df-d0cb0243f17d
  Args:
    source: :Princess_Thyra_of_Denmark
    relation: :hasFather
    target: :Christian_IX_of_Denmark
  AddTriple (f9216f3f-43cb-450c-b7b3-4168755b627a)
 Call ID: f9216f3f-43cb-450c-b7b3-4168755b627a
  Args:
    target: :Louise_of_Hesse_Kassel
    relation: :hasMother
    source: :Princess_Thyra_of_Denmark
  AssignClass (967a2e71-21e8-4867-b08b-fe6110a70ac0)
 Call ID: 967a2e71-21e8-4867-b08b-fe6110a70ac0
  Args:
    type: :Man
    source: :George_III_of_the_United_Kingdom
  AssignClass (64d63926-6760-4ae1-bdb8-dd942602bb4b)
 Call ID: 64d63926-6760-4ae1-bdb8-dd942602bb4b
  Args:
    type: :Person
    source: :George_III_of_the_United_Kingdom
  AssignClass (ff8a0753-e48d-413e-8795-7e9b7eabb8d5)
 Call ID: ff8a0753-e48d-413e-8795-7e9b7eabb8d5
  Args:
    source: :Charlotte_of_Mecklenburg_Strelitz
    type: :Woman
  AssignClass (fde8730e-7947-43fd-b824-f52052d5c26d)
 Call ID: fde8730e-7947-43fd-b824-f52052d5c26d
  Args:
    source: :Charlotte_of_Mecklenburg_Strelitz
    type: :Person
  AddTriple (1485e9ed-2335-4c3d-9821-408d10efc533)
 Call ID: 1485e9ed-2335-4c3d-9821-408d10efc533
  Args:
    relation: :hasAncestor
    source: :Marie_Louise_of_Hanover_and_Cumberland
    target: :George_III_of_the_United_Kingdom
  AddTriple (02ab6b35-613f-481f-99f7-977151e4d615)
 Call ID: 02ab6b35-613f-481f-99f7-977151e4d615
  Args:
    target: :Charlotte_of_Mecklenburg_Strelitz
    source: :Marie_Louise_of_Hanover_and_Cumberland
    relation: :hasAncestor
  AssignClass (157d1ad5-1f8f-4993-a03c-c32c5c0ab240)
 Call ID: 157d1ad5-1f8f-4993-a03c-c32c5c0ab240
  Args:
    source: :Maximilian_of_Baden
    type: :Man
  AssignClass (e30dd2b1-bce9-471d-b6fb-8bbb8deaa252)
 Call ID: e30dd2b1-bce9-471d-b6fb-8bbb8deaa252
  Args:
    type: :Person
    source: :Maximilian_of_Baden
  AddLiteral (845b37bb-90b5-4093-85d1-e8c7b4dfa5b1)
 Call ID: 845b37bb-90b5-4093-85d1-e8c7b4dfa5b1
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1867
    source: :Maximilian_of_Baden
  AddLiteral (ca35caaa-6a66-4e14-ae2a-19fc19715cf7)
 Call ID: ca35caaa-6a66-4e14-ae2a-19fc19715cf7
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1929
    source: :Maximilian_of_Baden
  AddLiteral (6a474a17-a7b4-4f23-b0cf-e176a4d12820)
 Call ID: 6a474a17-a7b4-4f23-b0cf-e176a4d12820
  Args:
    literal_type: xsd:integer
    source: :Marie_Louise_of_Hanover_and_Cumberland
    literal_value: 1900
    relation: :hasMarriageYear
  AddTriple (5a638b66-01d1-4b95-bb45-f46ee0e494cc)
 Call ID: 5a638b66-01d1-4b95-bb45-f46ee0e494cc
  Args:
    relation: :hasRelation
    source: :Marie_Louise_of_Hanover_and_Cumberland
    target: :Maximilian_of_Baden
  AssignClass (f4273d93-3305-4ade-8332-410cf5413920)
 Call ID: f4273d93-3305-4ade-8332-410cf5413920
  Args:
    source: :Wilhelm_of_Baden
    type: :Man
  AssignClass (068d99ee-b934-4cb1-9b3a-8b02ec438089)
 Call ID: 068d99ee-b934-4cb1-9b3a-8b02ec438089
  Args:
    source: :Wilhelm_of_Baden
    type: :Person
  AssignClass (d2845884-b503-47b0-884a-7b28b5b76432)
 Call ID: d2845884-b503-47b0-884a-7b28b5b76432
  Args:
    type: :Woman
    source: :Maria_Maximilianovna_of_Leuchtenberg
  AssignClass (9b9fd7e4-8794-4f37-8a1f-41af86b6ed09)
 Call ID: 9b9fd7e4-8794-4f37-8a1f-41af86b6ed09
  Args:
    source: :Maria_Maximilianovna_of_Leuchtenberg
    type: :Person
  AddTriple (1b0290c9-e23c-4857-84d9-5f874810d9fa)
 Call ID: 1b0290c9-e23c-4857-84d9-5f874810d9fa
  Args:
    source: :Maximilian_of_Baden
    relation: :hasFather
    target: :Wilhelm_of_Baden
  AddTriple (6911988d-bfdd-4bde-a3e9-fa66138a7758)
 Call ID: 6911988d-bfdd-4bde-a3e9-fa66138a7758
  Args:
    relation: :hasMother
    source: :Maximilian_of_Baden
    target: :Maria_Maximilianovna_of_Leuchtenberg
  AssignClass (ced53c43-43f4-42fc-aefe-ec27073d54f9)
 Call ID: ced53c43-43f4-42fc-aefe-ec27073d54f9
  Args:
    type: :Man
    source: :Napoleon_III_of_France
  AssignClass (c80200c5-b893-4a3d-bffa-58ec2db6a3ca)
 Call ID: c80200c5-b893-4a3d-bffa-58ec2db6a3ca
  Args:
    type: :Person
    source: :Napoleon_III_of_France
  Finish (a3cde0c2-cf90-4be7-a45a-f26472d5707c)
 Call ID: a3cde0c2-cf90-4be7-a45a-f26472d5707c
  Args: