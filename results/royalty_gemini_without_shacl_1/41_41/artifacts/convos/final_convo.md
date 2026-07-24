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
Infante Alfonso of Spain, Prince of the Two Sicilies, Duke of Calabria (30 November 1901 – 3 February 1964) was one of two claimants to the title of the head of the House of Bourbon-Two Sicilies from 1960 until his death in 1964.
He was the son of Prince Carlos of Bourbon-Two Sicilies and María de las Mercedes, Princess of Asturias.
He was born and died in Madrid, Spain.
Alfonso's mother was María de las Mercedes, Princess of Asturias, but she died in childbirth in 1904.
Alfonso XIII, King of Spain, was unmarried at the time so as the Princess of the Asturias's eldest son, the young infante became heir presumptive to the Spanish crown, though, unlike his mother, he never held the title of Prince of Asturias.
He was heir presumptive until the birth of his cousin, Alfonso, to Alfonso XIII and Queen Victoria Eugenie in 1907.
Marriage and issue

Alfonso married Princess Alice of Bourbon-Parma (1917–2017), his second cousin, daughter of Elias, Duke of Parma and Piacenza, and Archduchess Maria Anna of Austria, on 16 April 1936 in Vienna, Austria.



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
  AssignClass (328d58b7-271d-44f4-8632-562552b7e733)
 Call ID: 328d58b7-271d-44f4-8632-562552b7e733
  Args:
    type: :Man
    source: Alfonso_of_Spain
  AssignClass (82be06a6-2038-447e-858c-999074519acb)
 Call ID: 82be06a6-2038-447e-858c-999074519acb
  Args:
    source: Alfonso_of_Spain
    type: :Person
  AddLiteral (d94e072f-0741-4a21-9cd8-baf66e173161)
 Call ID: d94e072f-0741-4a21-9cd8-baf66e173161
  Args:
    literal_value: 1901
    literal_type: xsd:integer
    source: Alfonso_of_Spain
    relation: :hasBirthYear
  AddLiteral (d1ef97a7-bc04-478b-bd3b-08a364419044)
 Call ID: d1ef97a7-bc04-478b-bd3b-08a364419044
  Args:
    literal_value: 1964
    literal_type: xsd:integer
    source: Alfonso_of_Spain
    relation: :hasDeathYear
  AssignClass (f105a066-a289-4a8b-8a02-59ac435ffdda)
 Call ID: f105a066-a289-4a8b-8a02-59ac435ffdda
  Args:
    source: Carlos_of_Bourbon-Two_Sicilies
    type: :Man
  AssignClass (8d6d5d22-186f-48e3-a093-af3e1f5e575d)
 Call ID: 8d6d5d22-186f-48e3-a093-af3e1f5e575d
  Args:
    type: :Person
    source: Carlos_of_Bourbon-Two_Sicilies
  AssignClass (537a700b-3374-4768-af42-c3b9e009d510)
 Call ID: 537a700b-3374-4768-af42-c3b9e009d510
  Args:
    source: Maria_de_las_Mercedes
    type: :Woman
  AssignClass (25ce1d70-b9f1-42c6-80a1-3f1004130039)
 Call ID: 25ce1d70-b9f1-42c6-80a1-3f1004130039
  Args:
    source: Maria_de_las_Mercedes
    type: :Person
  AddTriple (713266da-8482-48e2-8ee6-5dc4de04c59b)
 Call ID: 713266da-8482-48e2-8ee6-5dc4de04c59b
  Args:
    relation: :hasFather
    target: Carlos_of_Bourbon-Two_Sicilies
    source: Alfonso_of_Spain
  AddTriple (ee2c9a0e-2c0e-4c04-bc62-ef7e067fb627)
 Call ID: ee2c9a0e-2c0e-4c04-bc62-ef7e067fb627
  Args:
    target: Maria_de_las_Mercedes
    source: Alfonso_of_Spain
    relation: :hasMother
  AssignClass (c056768a-ca11-4966-9f7d-4bdd2ca147ba)
 Call ID: c056768a-ca11-4966-9f7d-4bdd2ca147ba
  Args:
    type: :Woman
    source: Alice_of_Bourbon-Parma
  AssignClass (8ae09b28-434d-49cf-ac41-a89fbd1842e2)
 Call ID: 8ae09b28-434d-49cf-ac41-a89fbd1842e2
  Args:
    source: Alice_of_Bourbon-Parma
    type: :Person
  AddTriple (d0d33343-ec30-45db-9266-3edf9c30ac37)
 Call ID: d0d33343-ec30-45db-9266-3edf9c30ac37
  Args:
    relation: :hasRelation
    target: Alice_of_Bourbon-Parma
    source: Alfonso_of_Spain
  AddLiteral (79c19d86-065c-4b77-8c62-c5087973b337)
 Call ID: 79c19d86-065c-4b77-8c62-c5087973b337
  Args:
    literal_type: xsd:integer
    literal_value: 1936
    source: Alfonso_of_Spain
    relation: :hasMarriageYear
  AssignClass (623fa536-b924-4480-9210-8a84ab4e28b7)
 Call ID: 623fa536-b924-4480-9210-8a84ab4e28b7
  Args:
    source: Elias_of_Parma
    type: :Man
  AssignClass (f075f34f-134a-4cce-aeda-532a8adb02bc)
 Call ID: f075f34f-134a-4cce-aeda-532a8adb02bc
  Args:
    type: :Person
    source: Elias_of_Parma
  AssignClass (74c6bbec-e798-4899-ad97-9a2c58ef7449)
 Call ID: 74c6bbec-e798-4899-ad97-9a2c58ef7449
  Args:
    type: :Woman
    source: Maria_Anna_of_Austria
  AssignClass (37428e7a-eb5c-4cbf-8c68-f191321a6685)
 Call ID: 37428e7a-eb5c-4cbf-8c68-f191321a6685
  Args:
    source: Maria_Anna_of_Austria
    type: :Person
  AddTriple (2cebf3f8-273f-40c9-b169-3c978e06e4bc)
 Call ID: 2cebf3f8-273f-40c9-b169-3c978e06e4bc
  Args:
    source: Alice_of_Bourbon-Parma
    target: Elias_of_Parma
    relation: :hasFather
  AddTriple (550cb166-fbe3-4523-a61c-a5d2ae3d2723)
 Call ID: 550cb166-fbe3-4523-a61c-a5d2ae3d2723
  Args:
    source: Alice_of_Bourbon-Parma
    target: Maria_Anna_of_Austria
    relation: :hasMother
  AssignClass (90776355-f18e-4afc-bafa-f21ce7665f9e)
 Call ID: 90776355-f18e-4afc-bafa-f21ce7665f9e
  Args:
    type: :Man
    source: Alfonso_XIII
  AssignClass (a4060857-4b16-4cc3-979a-be22baebf336)
 Call ID: a4060857-4b16-4cc3-979a-be22baebf336
  Args:
    type: :Person
    source: Alfonso_XIII
  AssignClass (2b3938e1-6a15-4f52-a47c-b0ce1bf93df1)
 Call ID: 2b3938e1-6a15-4f52-a47c-b0ce1bf93df1
  Args:
    source: Victoria_Eugenie
    type: :Woman
  AssignClass (6043368d-58a3-4035-947f-94acb2f0993a)
 Call ID: 6043368d-58a3-4035-947f-94acb2f0993a
  Args:
    source: Victoria_Eugenie
    type: :Person
  AssignClass (49d8106e-2102-404b-abe2-73af4c35a26d)
 Call ID: 49d8106e-2102-404b-abe2-73af4c35a26d
  Args:
    source: Alfonso_cousin
    type: :Man
  AssignClass (0c7b23ed-a5d2-4615-8063-419da221c27b)
 Call ID: 0c7b23ed-a5d2-4615-8063-419da221c27b
  Args:
    source: Alfonso_cousin
    type: :Person
  AddTriple (9776e8d0-b4a4-40eb-993c-3b2113dde079)
 Call ID: 9776e8d0-b4a4-40eb-993c-3b2113dde079
  Args:
    relation: :hasFather
    source: Alfonso_cousin
    target: Alfonso_XIII
  AddTriple (245df201-6d78-4bc4-b26c-14dfa565268b)
 Call ID: 245df201-6d78-4bc4-b26c-14dfa565268b
  Args:
    relation: :hasMother
    source: Alfonso_cousin
    target: Victoria_Eugenie
  Finish (33f3bb2b-2205-48ab-86cc-f7d51e787352)
 Call ID: 33f3bb2b-2205-48ab-86cc-f7d51e787352
  Args: