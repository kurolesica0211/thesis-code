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
  AssignClass (d7a08bab-e30a-4a39-8392-94f524f567c8)
 Call ID: d7a08bab-e30a-4a39-8392-94f524f567c8
  Args:
    type: :Person
    source: Marie_Louise_of_Hanover_and_Cumberland
  AssignClass (d68b94d0-65b0-43bc-b438-283830d29f65)
 Call ID: d68b94d0-65b0-43bc-b438-283830d29f65
  Args:
    type: :Woman
    source: Marie_Louise_of_Hanover_and_Cumberland
  AddLiteral (dbcfef55-8867-4d2c-850a-5506005cbb6d)
 Call ID: dbcfef55-8867-4d2c-850a-5506005cbb6d
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Marie_Louise_of_Hanover_and_Cumberland
    literal_value: 1879
  AddLiteral (0676fb00-8e30-45d8-9e28-4019b96867da)
 Call ID: 0676fb00-8e30-45d8-9e28-4019b96867da
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1948
    source: Marie_Louise_of_Hanover_and_Cumberland
  AssignClass (fc90f0f6-71de-40da-9bdd-3dbbdc1515ae)
 Call ID: fc90f0f6-71de-40da-9bdd-3dbbdc1515ae
  Args:
    type: :Person
    source: Ernest_Augustus_Crown_Prince_of_Hanover
  AssignClass (9ad548c5-83ae-45fe-bbe4-3aca866eb328)
 Call ID: 9ad548c5-83ae-45fe-bbe4-3aca866eb328
  Args:
    type: :Man
    source: Ernest_Augustus_Crown_Prince_of_Hanover
  AssignClass (eae0396a-174d-49b8-9a88-730cc2f91dcf)
 Call ID: eae0396a-174d-49b8-9a88-730cc2f91dcf
  Args:
    type: :Person
    source: Princess_Thyra_of_Denmark
  AssignClass (ec11211c-2c77-4386-b6a5-2b6755e159fc)
 Call ID: ec11211c-2c77-4386-b6a5-2b6755e159fc
  Args:
    type: :Woman
    source: Princess_Thyra_of_Denmark
  AddTriple (2efbfa6f-4265-48f4-b05d-a12a1bdee8c1)
 Call ID: 2efbfa6f-4265-48f4-b05d-a12a1bdee8c1
  Args:
    relation: :hasFather
    target: Ernest_Augustus_Crown_Prince_of_Hanover
    source: Marie_Louise_of_Hanover_and_Cumberland
  AddTriple (a4fdba32-d4f2-45fa-8c30-c5ae86d22a35)
 Call ID: a4fdba32-d4f2-45fa-8c30-c5ae86d22a35
  Args:
    relation: :hasMother
    target: Princess_Thyra_of_Denmark
    source: Marie_Louise_of_Hanover_and_Cumberland
  AssignClass (3a920c15-6dc1-42b6-bcdc-7010ef411cf7)
 Call ID: 3a920c15-6dc1-42b6-bcdc-7010ef411cf7
  Args:
    type: :Person
    source: Christian_IX_of_Denmark
  AssignClass (cc37797d-d9e4-4d74-a726-1b46355205e9)
 Call ID: cc37797d-d9e4-4d74-a726-1b46355205e9
  Args:
    type: :Man
    source: Christian_IX_of_Denmark
  AssignClass (2f85c188-9cf0-4f03-8195-35ae36fa401c)
 Call ID: 2f85c188-9cf0-4f03-8195-35ae36fa401c
  Args:
    type: :Person
    source: Louise_of_Hesse-Kassel
  AssignClass (708c1cc2-cc22-420b-8b26-4e4745edc773)
 Call ID: 708c1cc2-cc22-420b-8b26-4e4745edc773
  Args:
    type: :Woman
    source: Louise_of_Hesse-Kassel
  AddTriple (1c4e99f1-fd0d-4e4f-9060-34abbf9a60bc)
 Call ID: 1c4e99f1-fd0d-4e4f-9060-34abbf9a60bc
  Args:
    target: Christian_IX_of_Denmark
    source: Princess_Thyra_of_Denmark
    relation: :hasFather
  AddTriple (378dfd19-bd81-4e16-bec8-0133851ac9f1)
 Call ID: 378dfd19-bd81-4e16-bec8-0133851ac9f1
  Args:
    relation: :hasMother
    target: Louise_of_Hesse-Kassel
    source: Princess_Thyra_of_Denmark
  AssignClass (45c52a4c-9a32-4513-b14f-bf3a29ad7b31)
 Call ID: 45c52a4c-9a32-4513-b14f-bf3a29ad7b31
  Args:
    type: :Person
    source: George_III_of_the_United_Kingdom
  AssignClass (05b7b5bc-f484-4369-8d49-7341681e8693)
 Call ID: 05b7b5bc-f484-4369-8d49-7341681e8693
  Args:
    type: :Man
    source: George_III_of_the_United_Kingdom
  AssignClass (84914cde-832f-4fbc-91d7-7df018648579)
 Call ID: 84914cde-832f-4fbc-91d7-7df018648579
  Args:
    type: :Person
    source: Charlotte_of_Mecklenburg-Strelitz
  AssignClass (711845e3-b7d1-41c8-ab74-e2c5b7693ab8)
 Call ID: 711845e3-b7d1-41c8-ab74-e2c5b7693ab8
  Args:
    type: :Woman
    source: Charlotte_of_Mecklenburg-Strelitz
  AddTriple (ecf57d7a-51da-4265-b6d2-983615a67c41)
 Call ID: ecf57d7a-51da-4265-b6d2-983615a67c41
  Args:
    source: Marie_Louise_of_Hanover_and_Cumberland
    target: George_III_of_the_United_Kingdom
    relation: :hasAncestor
  AddTriple (93667161-1ae8-475c-a3fc-984d5590dc70)
 Call ID: 93667161-1ae8-475c-a3fc-984d5590dc70
  Args:
    target: Charlotte_of_Mecklenburg-Strelitz
    source: Marie_Louise_of_Hanover_and_Cumberland
    relation: :hasAncestor
  AssignClass (84e5dee1-a469-4276-8c3b-5c2229f5548e)
 Call ID: 84e5dee1-a469-4276-8c3b-5c2229f5548e
  Args:
    type: :Person
    source: Maximilian_of_Baden
  AssignClass (7cf356e6-6acd-41d9-a4e2-8693603248fd)
 Call ID: 7cf356e6-6acd-41d9-a4e2-8693603248fd
  Args:
    type: :Man
    source: Maximilian_of_Baden
  AddLiteral (d9107167-c32c-42b5-8b30-60c216ed56aa)
 Call ID: d9107167-c32c-42b5-8b30-60c216ed56aa
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Maximilian_of_Baden
    literal_value: 1867
  AddLiteral (4deb2b52-3ec8-4cae-bd8b-c56a160cfb4e)
 Call ID: 4deb2b52-3ec8-4cae-bd8b-c56a160cfb4e
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: Maximilian_of_Baden
    literal_value: 1929
  AddLiteral (6b01e8ef-6e87-4e4d-9d87-5334d246e18a)
 Call ID: 6b01e8ef-6e87-4e4d-9d87-5334d246e18a
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    source: Marie_Louise_of_Hanover_and_Cumberland
    literal_value: 1900
  AddTriple (abf7d8dd-d4eb-4cbe-853d-b4a9f007f5b9)
 Call ID: abf7d8dd-d4eb-4cbe-853d-b4a9f007f5b9
  Args:
    source: Marie_Louise_of_Hanover_and_Cumberland
    target: Maximilian_of_Baden
    relation: :hasRelation
  AssignClass (f27b7c2b-6aad-4ed6-8a9f-66141954aa85)
 Call ID: f27b7c2b-6aad-4ed6-8a9f-66141954aa85
  Args:
    type: :Person
    source: Wilhelm_of_Baden
  AssignClass (77070bae-82a9-468f-a6ed-3f7eed3685c6)
 Call ID: 77070bae-82a9-468f-a6ed-3f7eed3685c6
  Args:
    type: :Man
    source: Wilhelm_of_Baden
  AssignClass (134132a0-54fc-4a5d-b4d2-5d551a08defa)
 Call ID: 134132a0-54fc-4a5d-b4d2-5d551a08defa
  Args:
    type: :Person
    source: Maria_Maximilianovna_of_Leuchtenberg
  AssignClass (2afa5933-6a02-42b2-a488-09bd5b7915e8)
 Call ID: 2afa5933-6a02-42b2-a488-09bd5b7915e8
  Args:
    type: :Woman
    source: Maria_Maximilianovna_of_Leuchtenberg
  AddTriple (e72ff9a2-4f58-46b6-a61f-3386e6ed9e33)
 Call ID: e72ff9a2-4f58-46b6-a61f-3386e6ed9e33
  Args:
    source: Maximilian_of_Baden
    target: Wilhelm_of_Baden
    relation: :hasFather
  AddTriple (8f6b5190-f8da-4260-a091-abc4a7690b23)
 Call ID: 8f6b5190-f8da-4260-a091-abc4a7690b23
  Args:
    relation: :hasMother
    target: Maria_Maximilianovna_of_Leuchtenberg
    source: Maximilian_of_Baden
  AssignClass (ce8fbbdd-7013-4fef-85e5-cad38577180d)
 Call ID: ce8fbbdd-7013-4fef-85e5-cad38577180d
  Args:
    type: :Person
    source: Napoleon_III_of_France
  AssignClass (59081c13-df35-4215-92f2-aff5a6d7e755)
 Call ID: 59081c13-df35-4215-92f2-aff5a6d7e755
  Args:
    type: :Man
    source: Napoleon_III_of_France
  Finish (aae471e0-35de-4a9b-ad8a-87244de7c9f2)
 Call ID: aae471e0-35de-4a9b-ad8a-87244de7c9f2
  Args: