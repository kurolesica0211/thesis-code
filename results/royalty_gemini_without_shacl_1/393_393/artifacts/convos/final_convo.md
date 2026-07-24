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
Princess Marie Alix of Schaumburg-Lippe (Marie Alix zu Schaumburg-Lippe; 2 April 1923 – 1 November 2021) was Duchess of Schleswig-Holstein as the wife of Peter, Duke of Schleswig-Holstein from 1965 to 1980.
Biography

Family

Marie Alix was the only daughter of Prince Stefan of Schaumburg-Lippe  and Ingeborg Alix, Princess Stephan Alexander of Schaumburg-Lippe .
She was the niece of Adolf II, the last ruler of the Principality of Schaumburg-Lippe, who abdicated following the German Revolution of 1918–1919.
Marie Alix's younger brother, Prince Georg Moritz of Schaumburg-Lippe, was killed in a car accident in 1970 without marrying or having children.
Marriage and issue

Marie Alix married Peter, Duke of Schleswig-Holstein, third son of Wilhelm Friedrich, Duke of Schleswig-Holstein, and Princess Marie Melita of Hohenlohe-Langenburg, in Glücksburg on 9 October 1947.
They had four children:


Work

She was a co-founder of the Stiftung Louisenlund, which runs an eponymous boarding school in Güby, Schleswig-Holstein, Germany.
Death and funeral

Princess Marie Alix of Schaumburg-Lippe died in Thumby on 1 November 2021 at the age of 98.
Her funeral was held 11 November 2021 in Schleswig Cathedral and she was buried in a family crypt at the family home, Louisenlund.



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix ns1: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
@prefix ns2: <http://www.w3.org/2003/11/swrl#> .
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

ns1:isRuleEnabled a owl:AnnotationProperty .

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

:x a ns2:Variable .

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

:y a ns2:Variable .

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

[] a ns2:Imp ;
    rdfs:label "infer hasSon" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasBrother" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasSister" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (fbe74067-5b78-461d-af46-2f599cf90fab)
 Call ID: fbe74067-5b78-461d-af46-2f599cf90fab
  Args:
    type: :Woman
    source: Marie_Alix_of_Schaumburg-Lippe
  AssignClass (bdb29950-36b8-429a-b6e6-f15271c8d940)
 Call ID: bdb29950-36b8-429a-b6e6-f15271c8d940
  Args:
    type: :Person
    source: Marie_Alix_of_Schaumburg-Lippe
  AddLiteral (e22ca44e-3526-47e6-b243-082ee25ef34e)
 Call ID: e22ca44e-3526-47e6-b243-082ee25ef34e
  Args:
    literal_value: 1923
    source: Marie_Alix_of_Schaumburg-Lippe
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (9075acb2-09df-49e0-aac0-3ac94c3441ef)
 Call ID: 9075acb2-09df-49e0-aac0-3ac94c3441ef
  Args:
    literal_type: xsd:integer
    source: Marie_Alix_of_Schaumburg-Lippe
    literal_value: 2021
    relation: :hasDeathYear
  AssignClass (944fd04c-6850-4b6f-9747-f1104eb1d380)
 Call ID: 944fd04c-6850-4b6f-9747-f1104eb1d380
  Args:
    source: Stefan_of_Schaumburg-Lippe
    type: :Man
  AssignClass (2670143b-6476-4813-9549-07388c7ee210)
 Call ID: 2670143b-6476-4813-9549-07388c7ee210
  Args:
    source: Stefan_of_Schaumburg-Lippe
    type: :Person
  AssignClass (6dc25529-9610-4e1d-b67e-c720720c6297)
 Call ID: 6dc25529-9610-4e1d-b67e-c720720c6297
  Args:
    source: Ingeborg_Alix_of_Schaumburg-Lippe
    type: :Woman
  AssignClass (8554ec8e-b93d-4a6c-b953-469236223f3a)
 Call ID: 8554ec8e-b93d-4a6c-b953-469236223f3a
  Args:
    source: Ingeborg_Alix_of_Schaumburg-Lippe
    type: :Person
  AddTriple (952697ed-8d34-41f0-8345-46da6fe3b3bb)
 Call ID: 952697ed-8d34-41f0-8345-46da6fe3b3bb
  Args:
    target: Stefan_of_Schaumburg-Lippe
    source: Marie_Alix_of_Schaumburg-Lippe
    relation: :hasFather
  AddTriple (4688e14f-b4a5-4649-a592-397cfb9f2958)
 Call ID: 4688e14f-b4a5-4649-a592-397cfb9f2958
  Args:
    target: Ingeborg_Alix_of_Schaumburg-Lippe
    relation: :hasMother
    source: Marie_Alix_of_Schaumburg-Lippe
  AssignClass (9ffd0a73-db56-4cab-9257-3da56fe55e0b)
 Call ID: 9ffd0a73-db56-4cab-9257-3da56fe55e0b
  Args:
    type: :Man
    source: Adolf_II_of_Schaumburg-Lippe
  AssignClass (8cc3e493-330f-4c24-96e0-a50cbf823b73)
 Call ID: 8cc3e493-330f-4c24-96e0-a50cbf823b73
  Args:
    source: Adolf_II_of_Schaumburg-Lippe
    type: :Person
  AssignClass (646152d0-c905-4d5d-9e4c-a16480c689e5)
 Call ID: 646152d0-c905-4d5d-9e4c-a16480c689e5
  Args:
    source: Georg_Moritz_of_Schaumburg-Lippe
    type: :Man
  AssignClass (f8eb6bf3-5159-442b-92dc-5f646d193608)
 Call ID: f8eb6bf3-5159-442b-92dc-5f646d193608
  Args:
    source: Georg_Moritz_of_Schaumburg-Lippe
    type: :Person
  AddTriple (402197f7-a7e6-4bb7-ab38-fc0d816166b7)
 Call ID: 402197f7-a7e6-4bb7-ab38-fc0d816166b7
  Args:
    relation: :hasBrother
    source: Marie_Alix_of_Schaumburg-Lippe
    target: Georg_Moritz_of_Schaumburg-Lippe
  AssignClass (608ceeed-0137-4770-87f5-50f73135c89f)
 Call ID: 608ceeed-0137-4770-87f5-50f73135c89f
  Args:
    source: Peter_of_Schleswig-Holstein
    type: :Man
  AssignClass (989ddcd7-e1c6-450a-92b4-2dcdd450344f)
 Call ID: 989ddcd7-e1c6-450a-92b4-2dcdd450344f
  Args:
    type: :Person
    source: Peter_of_Schleswig-Holstein
  AddLiteral (ae649c73-5c5b-478f-9ec2-8a05760bbb99)
 Call ID: ae649c73-5c5b-478f-9ec2-8a05760bbb99
  Args:
    literal_value: 1947
    literal_type: xsd:integer
    source: Marie_Alix_of_Schaumburg-Lippe
    relation: :hasMarriageYear
  AddTriple (243e0045-518b-4641-a94b-f94890593bab)
 Call ID: 243e0045-518b-4641-a94b-f94890593bab
  Args:
    target: Peter_of_Schleswig-Holstein
    source: Marie_Alix_of_Schaumburg-Lippe
    relation: :hasRelation
  AssignClass (985d25c4-c21b-4045-b247-5a849c39a1b4)
 Call ID: 985d25c4-c21b-4045-b247-5a849c39a1b4
  Args:
    type: :Man
    source: Wilhelm_Friedrich_of_Schleswig-Holstein
  AssignClass (b7ccd875-a07d-4bf7-8966-ad2df7ef5d74)
 Call ID: b7ccd875-a07d-4bf7-8966-ad2df7ef5d74
  Args:
    source: Wilhelm_Friedrich_of_Schleswig-Holstein
    type: :Person
  AssignClass (59cd8a66-6282-44c7-b42d-fae2a7ec9763)
 Call ID: 59cd8a66-6282-44c7-b42d-fae2a7ec9763
  Args:
    type: :Woman
    source: Marie_Melita_of_Hohenlohe-Langenburg
  AssignClass (deaaa923-27a6-43bc-82f1-cfad8dc14ce3)
 Call ID: deaaa923-27a6-43bc-82f1-cfad8dc14ce3
  Args:
    source: Marie_Melita_of_Hohenlohe-Langenburg
    type: :Person
  AddTriple (f29780bf-6b19-4594-85f3-afee8ad6951d)
 Call ID: f29780bf-6b19-4594-85f3-afee8ad6951d
  Args:
    source: Peter_of_Schleswig-Holstein
    relation: :hasFather
    target: Wilhelm_Friedrich_of_Schleswig-Holstein
  AddTriple (d240a71d-4416-4cfe-a245-8cff6f9374b1)
 Call ID: d240a71d-4416-4cfe-a245-8cff6f9374b1
  Args:
    source: Peter_of_Schleswig-Holstein
    relation: :hasMother
    target: Marie_Melita_of_Hohenlohe-Langenburg
  Finish (d92eedc9-01b7-4ec7-a944-f13c4e45a591)
 Call ID: d92eedc9-01b7-4ec7-a944-f13c4e45a591
  Args: