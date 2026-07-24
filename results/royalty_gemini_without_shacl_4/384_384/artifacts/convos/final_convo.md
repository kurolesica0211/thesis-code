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
Moritz, Landgrave of Hesse (legally Moritz Friedrich Karl Emanuel Humbert Prinz und Landgraf von Hessen; 6 August 1926 – 23 May 2013) was the son of Prince Philip, Landgrave of Hesse, and the head of the House of Hesse, also known as the House of Brabant.
Life

Landgrave Moritz was born at Racconigi Castle, in Italy.
During the Second World War, Moritz's mother, Princess Mafalda of Savoy, was arrested by the Nazis for alleged subversive activities and died in the Buchenwald concentration camp in 1944 as a result of a U.S. bombing raid on the camp.
Moritz and his siblings (Heinrich, Otto and Elisabeth) were given sanctuary in the Vatican under the care of their uncle Louis, Prince of Hesse and by Rhine and aunt Margaret Campbell Geddes who adopted them.
Prince Louis of Hesse and by Rhine, the last head of the Hesse-Darmstadt line, died in 1968, at which time Moritz's father succeeded him as head of the entire house.
Moritz became the head of the House of Hesse after the death of his father Philip on 25 October 1980.
Moritz was a world-famous art collector.
He presided over the Foundation of the House of Hesse which is the proprietor of the Kronberg Palace Hotel and several manor estates and palaces.
Marriage and children

Moritz married Princess Tatiana of Sayn-Wittgenstein-Berleburg, daughter of Prince Gustav Albrecht.



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
  AssignClass (9a7d20ce-ef41-4960-9731-3c7af777596f)
 Call ID: 9a7d20ce-ef41-4960-9731-3c7af777596f
  Args:
    type: :Man
    source: Moritz_of_Hesse
  AssignClass (3b44c7b4-9b99-47fe-a646-4f84574380f5)
 Call ID: 3b44c7b4-9b99-47fe-a646-4f84574380f5
  Args:
    type: :Person
    source: Moritz_of_Hesse
  AddLiteral (c6525323-b906-4d69-a79f-8416db765259)
 Call ID: c6525323-b906-4d69-a79f-8416db765259
  Args:
    source: Moritz_of_Hesse
    literal_value: 1926
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (85b6217e-ba6e-4be2-9b96-4fd827d0ee77)
 Call ID: 85b6217e-ba6e-4be2-9b96-4fd827d0ee77
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 2013
    source: Moritz_of_Hesse
  AssignClass (f0c95cde-5b32-438c-8785-1ad183d60955)
 Call ID: f0c95cde-5b32-438c-8785-1ad183d60955
  Args:
    source: Philip_of_Hesse
    type: :Man
  AssignClass (24fafe03-a9c9-47f6-9fb6-f3b514534aa6)
 Call ID: 24fafe03-a9c9-47f6-9fb6-f3b514534aa6
  Args:
    source: Philip_of_Hesse
    type: :Person
  AddTriple (1e0c392d-3135-45e9-b213-23496f0807aa)
 Call ID: 1e0c392d-3135-45e9-b213-23496f0807aa
  Args:
    source: Moritz_of_Hesse
    relation: :hasFather
    target: Philip_of_Hesse
  AssignClass (c6b90827-ca5f-49d6-a857-9647144d1b1a)
 Call ID: c6b90827-ca5f-49d6-a857-9647144d1b1a
  Args:
    source: Mafalda_of_Savoy
    type: :Woman
  AssignClass (49892438-7f2d-4bc1-ab7f-2e066b0efccd)
 Call ID: 49892438-7f2d-4bc1-ab7f-2e066b0efccd
  Args:
    source: Mafalda_of_Savoy
    type: :Person
  AddTriple (26d632d8-7489-4175-91d9-ec803962d370)
 Call ID: 26d632d8-7489-4175-91d9-ec803962d370
  Args:
    target: Mafalda_of_Savoy
    relation: :hasMother
    source: Moritz_of_Hesse
  AssignClass (a637d90c-edbc-48d4-9570-404be8082d93)
 Call ID: a637d90c-edbc-48d4-9570-404be8082d93
  Args:
    source: Heinrich_of_Hesse
    type: :Man
  AssignClass (c3423c4e-a11b-4c9b-a47a-c5dd32b40587)
 Call ID: c3423c4e-a11b-4c9b-a47a-c5dd32b40587
  Args:
    source: Heinrich_of_Hesse
    type: :Person
  AssignClass (bf453b8b-3ffc-46a7-a903-a898396a27ea)
 Call ID: bf453b8b-3ffc-46a7-a903-a898396a27ea
  Args:
    type: :Man
    source: Otto_of_Hesse
  AssignClass (50f267e9-db6c-400d-b48d-ea26923bd866)
 Call ID: 50f267e9-db6c-400d-b48d-ea26923bd866
  Args:
    type: :Person
    source: Otto_of_Hesse
  AssignClass (a9d92ad1-e824-42f7-ac1d-a124e4eb0c3a)
 Call ID: a9d92ad1-e824-42f7-ac1d-a124e4eb0c3a
  Args:
    type: :Woman
    source: Elisabeth_of_Hesse
  AssignClass (3d34edc6-5124-480f-bba8-08f4e2689151)
 Call ID: 3d34edc6-5124-480f-bba8-08f4e2689151
  Args:
    source: Elisabeth_of_Hesse
    type: :Person
  AddTriple (801197c3-7a6b-4b28-9e64-173ecd1f511b)
 Call ID: 801197c3-7a6b-4b28-9e64-173ecd1f511b
  Args:
    target: Heinrich_of_Hesse
    relation: :isSiblingOf
    source: Moritz_of_Hesse
  AddTriple (6c221bd5-4edc-4a96-a832-a52212e31526)
 Call ID: 6c221bd5-4edc-4a96-a832-a52212e31526
  Args:
    relation: :isSiblingOf
    target: Otto_of_Hesse
    source: Moritz_of_Hesse
  AddTriple (3a9e80d2-23a4-459a-9ff4-73288bbcc50e)
 Call ID: 3a9e80d2-23a4-459a-9ff4-73288bbcc50e
  Args:
    source: Moritz_of_Hesse
    relation: :isSiblingOf
    target: Elisabeth_of_Hesse
  AssignClass (49312784-7e4b-42d0-9d6f-a9183a387ee5)
 Call ID: 49312784-7e4b-42d0-9d6f-a9183a387ee5
  Args:
    source: Louis_of_Hesse_and_by_Rhine
    type: :Man
  AssignClass (7e0dcc52-7613-457b-9ab9-3e67010bec87)
 Call ID: 7e0dcc52-7613-457b-9ab9-3e67010bec87
  Args:
    type: :Person
    source: Louis_of_Hesse_and_by_Rhine
  AssignClass (c7b9c7c8-1dd5-413a-b4b4-7ca8bb4d0aa6)
 Call ID: c7b9c7c8-1dd5-413a-b4b4-7ca8bb4d0aa6
  Args:
    source: Margaret_Campbell_Geddes
    type: :Woman
  AssignClass (6aa65eaf-ab9c-4411-8cee-98ca849159ac)
 Call ID: 6aa65eaf-ab9c-4411-8cee-98ca849159ac
  Args:
    source: Margaret_Campbell_Geddes
    type: :Person
  AssignClass (b70ac7f1-29e3-4f3f-9cd5-2af1351e8216)
 Call ID: b70ac7f1-29e3-4f3f-9cd5-2af1351e8216
  Args:
    source: Tatiana_of_Sayn-Wittgenstein-Berleburg
    type: :Woman
  AssignClass (b40253a5-9393-443e-8dcd-e71fcae27fec)
 Call ID: b40253a5-9393-443e-8dcd-e71fcae27fec
  Args:
    source: Tatiana_of_Sayn-Wittgenstein-Berleburg
    type: :Person
  AddTriple (29fcee94-a258-47d5-8b48-10899b065e27)
 Call ID: 29fcee94-a258-47d5-8b48-10899b065e27
  Args:
    source: Moritz_of_Hesse
    target: Tatiana_of_Sayn-Wittgenstein-Berleburg
    relation: :hasRelation
  AssignClass (86ce6e58-bb57-4d69-8a3b-64ecbc4d1bf2)
 Call ID: 86ce6e58-bb57-4d69-8a3b-64ecbc4d1bf2
  Args:
    type: :Man
    source: Gustav_Albrecht
  AssignClass (090eae20-fa56-4176-bc55-5bd76f49747e)
 Call ID: 090eae20-fa56-4176-bc55-5bd76f49747e
  Args:
    type: :Person
    source: Gustav_Albrecht
  AddTriple (d518d275-0af4-4693-853a-cbb02b5c4bb4)
 Call ID: d518d275-0af4-4693-853a-cbb02b5c4bb4
  Args:
    source: Tatiana_of_Sayn-Wittgenstein-Berleburg
    relation: :hasFather
    target: Gustav_Albrecht
  Finish (68ba95e8-f74a-495d-a657-8d50f243a4e0)
 Call ID: 68ba95e8-f74a-495d-a657-8d50f243a4e0
  Args: