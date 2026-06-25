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
Prince Wilhelm Victor of Prussia (German: Wilhelm Viktor Ernst Freund Friedrich Georg Adalbert; 15 February 1919 – 7 February 1989) was a German royal, soldier and diplomat.
Life

Prince Wilhelm Victor was a grandson of Emperor Wilhelm II and the youngest child of Prince Adalbert of Prussia (1884–1948) and Princess Adelheid "Adi" of Saxe-Meiningen (1891–1971).
His father, Prince Adalbert carried also the title "Graf von Lingen".
His only surviving sister, Princess Viktoria Marina (1917–1981) married Kirby William Patterson (1907–1984).
Marriage

Prince Wilhelm Victor married at Donaueschingen 20 July 1944 Marie Antoinette, Countess of Hoyos-Stichsenstein (Hohenthurm, 27 June 1920 – Marbella 1 March 2004),  daughter of Friedrich, Count of Hoyos-Stichsenstein (1876–1951) and Countess Wilhelmine von Wuthenau-Hohenthurm (1895–1983), niece of Sophie, Duchess of Hohenberg.
They had the following issue:


Death

Prince Wilhelm Viktor died on 7 February 1989 at age 69.



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
  AssignClass (006fd46c-eefe-44b6-8b64-11f6e0531d82)
 Call ID: 006fd46c-eefe-44b6-8b64-11f6e0531d82
  Args:
    source: :Wilhelm_Victor_of_Prussia
    type: :Man
  AssignClass (156867c8-05e7-480c-91b6-f4c7be64f454)
 Call ID: 156867c8-05e7-480c-91b6-f4c7be64f454
  Args:
    source: :Wilhelm_Victor_of_Prussia
    type: :Person
  AddLiteral (1a7cb102-8401-40ef-9ae1-14b323c1c9cf)
 Call ID: 1a7cb102-8401-40ef-9ae1-14b323c1c9cf
  Args:
    literal_value: 1919
    source: :Wilhelm_Victor_of_Prussia
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (0eafa638-776c-4d8d-87fc-53844faa3768)
 Call ID: 0eafa638-776c-4d8d-87fc-53844faa3768
  Args:
    source: :Wilhelm_Victor_of_Prussia
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 1989
  AssignClass (572c102e-4453-4546-90f6-ca252e6ab7b3)
 Call ID: 572c102e-4453-4546-90f6-ca252e6ab7b3
  Args:
    source: :Wilhelm_II
    type: :Man
  AssignClass (a19e494c-e5e7-480b-83c0-1b6981f80d55)
 Call ID: a19e494c-e5e7-480b-83c0-1b6981f80d55
  Args:
    source: :Wilhelm_II
    type: :Person
  AddTriple (05b54d61-84af-46a2-93d9-5f0e1067f3e0)
 Call ID: 05b54d61-84af-46a2-93d9-5f0e1067f3e0
  Args:
    relation: :hasAncestor
    source: :Wilhelm_Victor_of_Prussia
    target: :Wilhelm_II
  AssignClass (590e0dd0-3ca7-47ee-8c09-fd427a3989a3)
 Call ID: 590e0dd0-3ca7-47ee-8c09-fd427a3989a3
  Args:
    source: :Adalbert_of_Prussia
    type: :Man
  AssignClass (3140f2d2-3673-486b-9358-456cda5f7b52)
 Call ID: 3140f2d2-3673-486b-9358-456cda5f7b52
  Args:
    source: :Adalbert_of_Prussia
    type: :Person
  AddLiteral (09731971-224b-48b0-b6e7-ca8913f58113)
 Call ID: 09731971-224b-48b0-b6e7-ca8913f58113
  Args:
    literal_value: 1884
    relation: :hasBirthYear
    source: :Adalbert_of_Prussia
    literal_type: xsd:integer
  AddLiteral (a2bd54eb-0b03-419c-86ff-a96aa47a14ac)
 Call ID: a2bd54eb-0b03-419c-86ff-a96aa47a14ac
  Args:
    literal_value: 1948
    relation: :hasDeathYear
    source: :Adalbert_of_Prussia
    literal_type: xsd:integer
  AddTriple (84e2b59c-145f-464d-a121-c8c3be3eae13)
 Call ID: 84e2b59c-145f-464d-a121-c8c3be3eae13
  Args:
    source: :Wilhelm_Victor_of_Prussia
    relation: :hasFather
    target: :Adalbert_of_Prussia
  AssignClass (39bdc6e7-a423-40c5-af4c-77765a84be6f)
 Call ID: 39bdc6e7-a423-40c5-af4c-77765a84be6f
  Args:
    source: :Adelheid_of_Saxe-Meiningen
    type: :Woman
  AssignClass (5b58b602-bb92-4a10-b2cd-7dda41925acb)
 Call ID: 5b58b602-bb92-4a10-b2cd-7dda41925acb
  Args:
    source: :Adelheid_of_Saxe-Meiningen
    type: :Person
  AddLiteral (6373c5e3-6963-413d-aab4-299e563df7f4)
 Call ID: 6373c5e3-6963-413d-aab4-299e563df7f4
  Args:
    relation: :hasBirthYear
    source: :Adelheid_of_Saxe-Meiningen
    literal_type: xsd:integer
    literal_value: 1891
  AddLiteral (fb9d6714-989a-4feb-88f6-7c547f786c2f)
 Call ID: fb9d6714-989a-4feb-88f6-7c547f786c2f
  Args:
    relation: :hasDeathYear
    source: :Adelheid_of_Saxe-Meiningen
    literal_type: xsd:integer
    literal_value: 1971
  AddTriple (f23b1b50-0f72-4664-9d81-feb4cf54460c)
 Call ID: f23b1b50-0f72-4664-9d81-feb4cf54460c
  Args:
    target: :Adelheid_of_Saxe-Meiningen
    relation: :hasMother
    source: :Wilhelm_Victor_of_Prussia
  AssignClass (f1ac4ce6-7b9b-4917-beba-b7ae11eb3272)
 Call ID: f1ac4ce6-7b9b-4917-beba-b7ae11eb3272
  Args:
    source: :Viktoria_Marina
    type: :Woman
  AssignClass (26f4c486-1427-4960-b7f0-0cc6b66d0689)
 Call ID: 26f4c486-1427-4960-b7f0-0cc6b66d0689
  Args:
    source: :Viktoria_Marina
    type: :Person
  AddLiteral (d1e92b86-5fe3-4c3b-b7f9-a80919a0e855)
 Call ID: d1e92b86-5fe3-4c3b-b7f9-a80919a0e855
  Args:
    source: :Viktoria_Marina
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1917
  AddLiteral (707984d1-1682-4731-ba28-b0c4acbd43b9)
 Call ID: 707984d1-1682-4731-ba28-b0c4acbd43b9
  Args:
    literal_value: 1981
    relation: :hasDeathYear
    source: :Viktoria_Marina
    literal_type: xsd:integer
  AddTriple (e42a83d1-3db4-4b66-8e69-835dc17668a7)
 Call ID: e42a83d1-3db4-4b66-8e69-835dc17668a7
  Args:
    target: :Viktoria_Marina
    relation: :hasSister
    source: :Wilhelm_Victor_of_Prussia
  AssignClass (9d9fd124-f217-4667-82a7-d04631e7822e)
 Call ID: 9d9fd124-f217-4667-82a7-d04631e7822e
  Args:
    source: :Kirby_William_Patterson
    type: :Man
  AssignClass (735fbc3b-b93f-42a9-8cb9-794f0834e1f2)
 Call ID: 735fbc3b-b93f-42a9-8cb9-794f0834e1f2
  Args:
    source: :Kirby_William_Patterson
    type: :Person
  AddLiteral (1b3a1583-5dfd-4257-a38d-2e7ee38c0c54)
 Call ID: 1b3a1583-5dfd-4257-a38d-2e7ee38c0c54
  Args:
    source: :Kirby_William_Patterson
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1907
  AddLiteral (e9d46eec-81ea-4e28-b6c8-d22cb0e1b1b1)
 Call ID: e9d46eec-81ea-4e28-b6c8-d22cb0e1b1b1
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: :Kirby_William_Patterson
    literal_value: 1984
  AddTriple (999f20c5-4c81-4dba-8f95-a329ba1849c1)
 Call ID: 999f20c5-4c81-4dba-8f95-a329ba1849c1
  Args:
    target: :Kirby_William_Patterson
    relation: :hasRelation
    source: :Viktoria_Marina
  AssignClass (b8ee7c53-8071-43f6-a251-f80e52a9563f)
 Call ID: b8ee7c53-8071-43f6-a251-f80e52a9563f
  Args:
    source: :Marie_Antoinette_of_Hoyos-Stichsenstein
    type: :Woman
  AssignClass (780c69ff-8f73-4be1-9a32-d45a2d64644a)
 Call ID: 780c69ff-8f73-4be1-9a32-d45a2d64644a
  Args:
    source: :Marie_Antoinette_of_Hoyos-Stichsenstein
    type: :Person
  AddLiteral (a5a28702-f1f2-4974-976e-2ef2aa0076b5)
 Call ID: a5a28702-f1f2-4974-976e-2ef2aa0076b5
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: :Marie_Antoinette_of_Hoyos-Stichsenstein
    literal_value: 1920
  AddLiteral (853ad624-f21b-4ae2-8806-6344e7c0ec6b)
 Call ID: 853ad624-f21b-4ae2-8806-6344e7c0ec6b
  Args:
    source: :Marie_Antoinette_of_Hoyos-Stichsenstein
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 2004
  AddLiteral (0e97de46-45bd-48e4-b38e-81c9499b1dbd)
 Call ID: 0e97de46-45bd-48e4-b38e-81c9499b1dbd
  Args:
    literal_type: xsd:integer
    source: :Wilhelm_Victor_of_Prussia
    relation: :hasMarriageYear
    literal_value: 1944
  AddTriple (2b91998b-b481-40a1-a53c-4cf1d8a1a57c)
 Call ID: 2b91998b-b481-40a1-a53c-4cf1d8a1a57c
  Args:
    relation: :hasRelation
    source: :Wilhelm_Victor_of_Prussia
    target: :Marie_Antoinette_of_Hoyos-Stichsenstein
  AssignClass (8f58e251-4678-4f72-b042-cf06bba6218b)
 Call ID: 8f58e251-4678-4f72-b042-cf06bba6218b
  Args:
    source: :Friedrich_Count_of_Hoyos-Stichsenstein
    type: :Man
  AssignClass (959e4c08-ae9b-465f-b9bf-f565d29f013d)
 Call ID: 959e4c08-ae9b-465f-b9bf-f565d29f013d
  Args:
    source: :Friedrich_Count_of_Hoyos-Stichsenstein
    type: :Person
  AddLiteral (3a980c86-78e9-40e1-a612-c96ffec38c07)
 Call ID: 3a980c86-78e9-40e1-a612-c96ffec38c07
  Args:
    literal_value: 1876
    literal_type: xsd:integer
    source: :Friedrich_Count_of_Hoyos-Stichsenstein
    relation: :hasBirthYear
  AddLiteral (64f75df5-ddd4-49ba-8968-b12f49a1e28f)
 Call ID: 64f75df5-ddd4-49ba-8968-b12f49a1e28f
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: :Friedrich_Count_of_Hoyos-Stichsenstein
    literal_value: 1951
  AddTriple (085924e4-04be-490a-91f1-82c7b3a52f87)
 Call ID: 085924e4-04be-490a-91f1-82c7b3a52f87
  Args:
    target: :Friedrich_Count_of_Hoyos-Stichsenstein
    source: :Marie_Antoinette_of_Hoyos-Stichsenstein
    relation: :hasFather
  AssignClass (464fa324-6652-4c47-a0af-1f39f2a6a9ed)
 Call ID: 464fa324-6652-4c47-a0af-1f39f2a6a9ed
  Args:
    source: :Wilhelmine_von_Wuthenau-Hohenthurm
    type: :Woman
  AssignClass (ca58049a-a61e-400c-a2f8-16f96da20439)
 Call ID: ca58049a-a61e-400c-a2f8-16f96da20439
  Args:
    source: :Wilhelmine_von_Wuthenau-Hohenthurm
    type: :Person
  AddLiteral (a4e462b2-d4cb-4d51-90e7-d7ca12af8a4b)
 Call ID: a4e462b2-d4cb-4d51-90e7-d7ca12af8a4b
  Args:
    literal_value: 1895
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: :Wilhelmine_von_Wuthenau-Hohenthurm
  AddLiteral (3837f4da-fb71-493f-9459-00c1799dab2b)
 Call ID: 3837f4da-fb71-493f-9459-00c1799dab2b
  Args:
    source: :Wilhelmine_von_Wuthenau-Hohenthurm
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 1983
  AddTriple (866e8d5d-e282-44fd-ab28-11311c40a254)
 Call ID: 866e8d5d-e282-44fd-ab28-11311c40a254
  Args:
    target: :Wilhelmine_von_Wuthenau-Hohenthurm
    source: :Marie_Antoinette_of_Hoyos-Stichsenstein
    relation: :hasMother
  Finish (59979b1b-6962-4234-bb45-2793f9d0c808)
 Call ID: 59979b1b-6962-4234-bb45-2793f9d0c808
  Args: