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
  AssignClass (16e0198c-8d6f-4bb5-846d-05c392899269)
 Call ID: 16e0198c-8d6f-4bb5-846d-05c392899269
  Args:
    type: :Person
    source: :Marie_Alix_of_Schaumburg-Lippe
  AssignClass (088af11e-af4b-4d65-8eea-adf273904b65)
 Call ID: 088af11e-af4b-4d65-8eea-adf273904b65
  Args:
    type: :Woman
    source: :Marie_Alix_of_Schaumburg-Lippe
  AddLiteral (2094d54e-19fc-4698-8ba0-c8b8f3d80ddf)
 Call ID: 2094d54e-19fc-4698-8ba0-c8b8f3d80ddf
  Args:
    literal_value: Marie Alix of Schaumburg-Lippe
    literal_type: xsd:string
    source: :Marie_Alix_of_Schaumburg-Lippe
    relation: :knownAs
  AddLiteral (c17bba6a-876f-4db3-816a-a04a992a0f02)
 Call ID: c17bba6a-876f-4db3-816a-a04a992a0f02
  Args:
    relation: :hasBirthYear
    source: :Marie_Alix_of_Schaumburg-Lippe
    literal_type: xsd:integer
    literal_value: 1923
  AddLiteral (1cc22bfc-ca06-49e8-a7b5-9b5fd8501437)
 Call ID: 1cc22bfc-ca06-49e8-a7b5-9b5fd8501437
  Args:
    literal_value: 2021
    literal_type: xsd:integer
    source: :Marie_Alix_of_Schaumburg-Lippe
    relation: :hasDeathYear
  AssignClass (ec14c438-f2a3-42b0-af7d-9f92a9371a42)
 Call ID: ec14c438-f2a3-42b0-af7d-9f92a9371a42
  Args:
    type: :Person
    source: :Prince_Stefan_of_Schaumburg-Lippe
  AssignClass (44a4a952-51f9-49df-ab12-018adb819ab8)
 Call ID: 44a4a952-51f9-49df-ab12-018adb819ab8
  Args:
    type: :Man
    source: :Prince_Stefan_of_Schaumburg-Lippe
  AddTriple (bbf81788-5256-4347-8a51-fead87667cd0)
 Call ID: bbf81788-5256-4347-8a51-fead87667cd0
  Args:
    source: :Prince_Stefan_of_Schaumburg-Lippe
    relation: :isFatherOf
    target: :Marie_Alix_of_Schaumburg-Lippe
  AssignClass (a53c5392-07e8-4c81-8db5-f5cb26cf71ee)
 Call ID: a53c5392-07e8-4c81-8db5-f5cb26cf71ee
  Args:
    type: :Person
    source: :Ingeborg_Alix_of_Schaumburg-Lippe
  AssignClass (48939688-9291-48d4-b77c-6d99b92272af)
 Call ID: 48939688-9291-48d4-b77c-6d99b92272af
  Args:
    type: :Woman
    source: :Ingeborg_Alix_of_Schaumburg-Lippe
  AddTriple (e0396fc9-fda5-4336-ac86-68e84fcc73c3)
 Call ID: e0396fc9-fda5-4336-ac86-68e84fcc73c3
  Args:
    target: :Marie_Alix_of_Schaumburg-Lippe
    source: :Ingeborg_Alix_of_Schaumburg-Lippe
    relation: :isMotherOf
  AssignClass (e98771a2-a69e-4455-b491-15b342ff939a)
 Call ID: e98771a2-a69e-4455-b491-15b342ff939a
  Args:
    type: :Person
    source: :Prince_Georg_Moritz_of_Schaumburg-Lippe
  AssignClass (1c3aebcf-d1d5-4ce4-8858-f4d81f911493)
 Call ID: 1c3aebcf-d1d5-4ce4-8858-f4d81f911493
  Args:
    type: :Man
    source: :Prince_Georg_Moritz_of_Schaumburg-Lippe
  AddTriple (bfbf83b4-85b6-4e16-a52d-19f5e921748b)
 Call ID: bfbf83b4-85b6-4e16-a52d-19f5e921748b
  Args:
    source: :Marie_Alix_of_Schaumburg-Lippe
    relation: :isSiblingOf
    target: :Prince_Georg_Moritz_of_Schaumburg-Lippe
  AssignClass (4aaba046-e1ba-4bde-8394-81519cf074a0)
 Call ID: 4aaba046-e1ba-4bde-8394-81519cf074a0
  Args:
    type: :Person
    source: :Peter_Duke_of_Schleswig-Holstein
  AssignClass (f8848e30-269e-47f5-8857-ea43457b15c8)
 Call ID: f8848e30-269e-47f5-8857-ea43457b15c8
  Args:
    type: :Man
    source: :Peter_Duke_of_Schleswig-Holstein
  AddLiteral (d7a53885-3183-41da-b4a2-2e048cd20445)
 Call ID: d7a53885-3183-41da-b4a2-2e048cd20445
  Args:
    literal_type: xsd:integer
    literal_value: 1947
    relation: :hasMarriageYear
    source: :Marie_Alix_of_Schaumburg-Lippe
  AddTriple (a74f24e9-950f-49e6-aed6-706ff76dd34c)
 Call ID: a74f24e9-950f-49e6-aed6-706ff76dd34c
  Args:
    relation: :hasRelation
    source: :Marie_Alix_of_Schaumburg-Lippe
    target: :Peter_Duke_of_Schleswig-Holstein
  AssignClass (3f3c7d7c-82bd-4426-abc9-e860d38c857a)
 Call ID: 3f3c7d7c-82bd-4426-abc9-e860d38c857a
  Args:
    type: :Person
    source: :Wilhelm_Friedrich_Duke_of_Schleswig-Holstein
  AssignClass (5aaf7cf2-9df3-4821-9f41-5d47009bad63)
 Call ID: 5aaf7cf2-9df3-4821-9f41-5d47009bad63
  Args:
    type: :Man
    source: :Wilhelm_Friedrich_Duke_of_Schleswig-Holstein
  AddTriple (ecba4d24-b095-4433-861c-1e272f4bd1f0)
 Call ID: ecba4d24-b095-4433-861c-1e272f4bd1f0
  Args:
    relation: :isFatherOf
    source: :Wilhelm_Friedrich_Duke_of_Schleswig-Holstein
    target: :Peter_Duke_of_Schleswig-Holstein
  AssignClass (ceec5235-3941-4da6-b0ad-1e16b2bd92f6)
 Call ID: ceec5235-3941-4da6-b0ad-1e16b2bd92f6
  Args:
    type: :Person
    source: :Princess_Marie_Melita_of_Hohenlohe-Langenburg
  AssignClass (7b29177b-bf97-47ce-bc86-67c1cb4461b5)
 Call ID: 7b29177b-bf97-47ce-bc86-67c1cb4461b5
  Args:
    type: :Woman
    source: :Princess_Marie_Melita_of_Hohenlohe-Langenburg
  AddTriple (81365ce1-df08-4174-948a-d26752e7dc84)
 Call ID: 81365ce1-df08-4174-948a-d26752e7dc84
  Args:
    relation: :isMotherOf
    source: :Princess_Marie_Melita_of_Hohenlohe-Langenburg
    target: :Peter_Duke_of_Schleswig-Holstein
  Finish (9af4f587-18d9-48ed-a4bd-3ba24d604836)
 Call ID: 9af4f587-18d9-48ed-a4bd-3ba24d604836
  Args: