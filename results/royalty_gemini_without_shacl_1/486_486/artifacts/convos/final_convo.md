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
Prince Heinrich Wilhelm Konstantin Viktor Franz of Hesse-Kassel (30 October 1927 – 18 November 1999), also known as Enrico d'Assia, was the second child of Prince Philipp of Hesse and Princess Mafalda of Savoy.
Heinrich became an artist, set designer, and memoirist after World War II.
Life

Prince Heinrich was born in Rome, Italy, as the second son of Prince Philipp of Hesse and Princess Mafalda of Savoy, daughter of King Victor Emmanuel III of Italy.
During the Second World War, Heinrich's father, an important former aristocratic Nazi party member, was arrested by the Gestapo.
Heinrich and his siblings (Moritz, Otto and Elisabeth) were given sanctuary in the Vatican under the care of their aunt and uncle, Margaret Campbell Geddes and Louis, Prince of Hesse and by Rhine, who adopted them.
Heinrich was an artist and set designer, active mainly in Italy under the name Enrico d'Assia.



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
  AssignClass (b3b9d2c8-864f-4868-bac6-993335db09c8)
 Call ID: b3b9d2c8-864f-4868-bac6-993335db09c8
  Args:
    source: Prince_Heinrich_of_Hesse-Kassel
    type: :Man
  AssignClass (08cb9fef-7ec4-4c65-86c8-841f042068c8)
 Call ID: 08cb9fef-7ec4-4c65-86c8-841f042068c8
  Args:
    type: :Person
    source: Prince_Heinrich_of_Hesse-Kassel
  AddLiteral (b548cf72-257e-48cf-88f5-4fa80efcb6e9)
 Call ID: b548cf72-257e-48cf-88f5-4fa80efcb6e9
  Args:
    literal_type: xsd:string
    relation: :alsoKnownAs
    literal_value: Enrico d'Assia
    source: Prince_Heinrich_of_Hesse-Kassel
  AddLiteral (7a997cdf-4351-4ac9-9542-b53752045e00)
 Call ID: 7a997cdf-4351-4ac9-9542-b53752045e00
  Args:
    relation: :hasBirthYear
    literal_type: xsd:nonNegativeInteger
    source: Prince_Heinrich_of_Hesse-Kassel
    literal_value: 1927
  AddLiteral (542f9db9-3f6a-44fb-9be1-ec556f95d680)
 Call ID: 542f9db9-3f6a-44fb-9be1-ec556f95d680
  Args:
    source: Prince_Heinrich_of_Hesse-Kassel
    literal_value: 1999
    literal_type: xsd:nonNegativeInteger
    relation: :hasDeathYear
  AssignClass (47e14864-a4b5-499a-a569-986d948e23cc)
 Call ID: 47e14864-a4b5-499a-a569-986d948e23cc
  Args:
    type: :Man
    source: Prince_Philipp_of_Hesse
  AssignClass (b54700f1-8c14-4de3-ac07-1a5df3c03729)
 Call ID: b54700f1-8c14-4de3-ac07-1a5df3c03729
  Args:
    source: Prince_Philipp_of_Hesse
    type: :Person
  AssignClass (16842091-1ef5-41aa-b2fb-a89708912e9b)
 Call ID: 16842091-1ef5-41aa-b2fb-a89708912e9b
  Args:
    source: Princess_Mafalda_of_Savoy
    type: :Woman
  AssignClass (ae6f28ad-d6eb-4c06-9875-ee51847fa936)
 Call ID: ae6f28ad-d6eb-4c06-9875-ee51847fa936
  Args:
    source: Princess_Mafalda_of_Savoy
    type: :Person
  AddTriple (7dcd2787-44a9-451b-9c81-c6f65c6203b3)
 Call ID: 7dcd2787-44a9-451b-9c81-c6f65c6203b3
  Args:
    relation: :hasFather
    target: Prince_Philipp_of_Hesse
    source: Prince_Heinrich_of_Hesse-Kassel
  AddTriple (2d633bff-56f0-4cd8-9d28-769ab3ddc4fe)
 Call ID: 2d633bff-56f0-4cd8-9d28-769ab3ddc4fe
  Args:
    target: Princess_Mafalda_of_Savoy
    source: Prince_Heinrich_of_Hesse-Kassel
    relation: :hasMother
  AssignClass (6a8b43f1-5371-4ac7-954d-6268467ba130)
 Call ID: 6a8b43f1-5371-4ac7-954d-6268467ba130
  Args:
    source: King_Victor_Emmanuel_III_of_Italy
    type: :Man
  AssignClass (8f646711-959a-49c8-830f-e2fdea0e115b)
 Call ID: 8f646711-959a-49c8-830f-e2fdea0e115b
  Args:
    source: King_Victor_Emmanuel_III_of_Italy
    type: :Person
  AddTriple (ee9d50b6-732a-49bc-b3eb-5a258d09cc2b)
 Call ID: ee9d50b6-732a-49bc-b3eb-5a258d09cc2b
  Args:
    source: Princess_Mafalda_of_Savoy
    target: King_Victor_Emmanuel_III_of_Italy
    relation: :hasFather
  AssignClass (fcde704e-3884-4852-9389-f5ce1e81e24b)
 Call ID: fcde704e-3884-4852-9389-f5ce1e81e24b
  Args:
    type: :Man
    source: Moritz_of_Hesse
  AssignClass (27aadef8-745e-44a4-b2e4-7ebbc5213c25)
 Call ID: 27aadef8-745e-44a4-b2e4-7ebbc5213c25
  Args:
    type: :Person
    source: Moritz_of_Hesse
  AssignClass (d90890f3-0aa8-4c61-b1b0-b2d6b5cfbe32)
 Call ID: d90890f3-0aa8-4c61-b1b0-b2d6b5cfbe32
  Args:
    type: :Man
    source: Otto_of_Hesse
  AssignClass (ed6a199c-3055-4482-92bd-415059b16789)
 Call ID: ed6a199c-3055-4482-92bd-415059b16789
  Args:
    source: Otto_of_Hesse
    type: :Person
  AssignClass (81b0c7d5-0408-4ca0-b9a6-afe6b95f222c)
 Call ID: 81b0c7d5-0408-4ca0-b9a6-afe6b95f222c
  Args:
    source: Elisabeth_of_Hesse
    type: :Woman
  AssignClass (50ff0058-5978-43b1-ba0c-3c7116236974)
 Call ID: 50ff0058-5978-43b1-ba0c-3c7116236974
  Args:
    source: Elisabeth_of_Hesse
    type: :Person
  AddTriple (5657daa7-0332-4ad3-9889-3f86e8e4b86d)
 Call ID: 5657daa7-0332-4ad3-9889-3f86e8e4b86d
  Args:
    target: Moritz_of_Hesse
    source: Prince_Heinrich_of_Hesse-Kassel
    relation: :isSiblingOf
  AddTriple (42f88d89-168c-426c-913f-2b9276697eaa)
 Call ID: 42f88d89-168c-426c-913f-2b9276697eaa
  Args:
    target: Otto_of_Hesse
    source: Prince_Heinrich_of_Hesse-Kassel
    relation: :isSiblingOf
  AddTriple (f185774a-51f0-4490-9b7c-987a0be9a4fc)
 Call ID: f185774a-51f0-4490-9b7c-987a0be9a4fc
  Args:
    target: Elisabeth_of_Hesse
    source: Prince_Heinrich_of_Hesse-Kassel
    relation: :isSiblingOf
  AssignClass (599bb3c0-5310-43db-a18c-03309974cf48)
 Call ID: 599bb3c0-5310-43db-a18c-03309974cf48
  Args:
    source: Margaret_Campbell_Geddes
    type: :Woman
  AssignClass (f4c98759-d4dc-4fbd-a7ca-5aa7ec955231)
 Call ID: f4c98759-d4dc-4fbd-a7ca-5aa7ec955231
  Args:
    type: :Person
    source: Margaret_Campbell_Geddes
  AssignClass (5b07544c-cb6b-493d-be9c-3a40c3e32339)
 Call ID: 5b07544c-cb6b-493d-be9c-3a40c3e32339
  Args:
    source: Louis_Prince_of_Hesse_and_by_Rhine
    type: :Man
  AssignClass (3f27b7ac-0f44-4c56-9df9-b7e4f23e1faf)
 Call ID: 3f27b7ac-0f44-4c56-9df9-b7e4f23e1faf
  Args:
    type: :Person
    source: Louis_Prince_of_Hesse_and_by_Rhine
  Finish (8c5fdc08-cf23-4c40-8703-23ec2b5b7ca8)
 Call ID: 8c5fdc08-cf23-4c40-8703-23ec2b5b7ca8
  Args: