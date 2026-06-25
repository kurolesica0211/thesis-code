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
  AssignClass (5f152549-f18a-486e-b374-7f085dff2a95)
 Call ID: 5f152549-f18a-486e-b374-7f085dff2a95
  Args:
    type: :Woman
    source: Marie_Alix_of_Schaumburg-Lippe
  AssignClass (7b67e3a6-0777-47e4-8ce2-8cbc88c30039)
 Call ID: 7b67e3a6-0777-47e4-8ce2-8cbc88c30039
  Args:
    type: :Person
    source: Marie_Alix_of_Schaumburg-Lippe
  AddLiteral (a2c4a6fd-86d2-48b5-a057-46c6babc7822)
 Call ID: a2c4a6fd-86d2-48b5-a057-46c6babc7822
  Args:
    literal_type: xsd:integer
    literal_value: 1923
    source: Marie_Alix_of_Schaumburg-Lippe
    relation: :hasBirthYear
  AddLiteral (685b358f-895a-4e49-aff3-a0b77b9d89a5)
 Call ID: 685b358f-895a-4e49-aff3-a0b77b9d89a5
  Args:
    relation: :hasDeathYear
    source: Marie_Alix_of_Schaumburg-Lippe
    literal_value: 2021
    literal_type: xsd:integer
  AssignClass (70195bf9-fa9d-4a1a-9d9f-b9bb9022b8bf)
 Call ID: 70195bf9-fa9d-4a1a-9d9f-b9bb9022b8bf
  Args:
    source: Peter_Duke_of_Schleswig-Holstein
    type: :Man
  AssignClass (a5e7d285-e4f3-4ca6-8109-ef4495851c04)
 Call ID: a5e7d285-e4f3-4ca6-8109-ef4495851c04
  Args:
    source: Peter_Duke_of_Schleswig-Holstein
    type: :Person
  AddLiteral (76efc875-20d6-4bab-8b7f-89214025d65e)
 Call ID: 76efc875-20d6-4bab-8b7f-89214025d65e
  Args:
    relation: :hasMarriageYear
    literal_value: 1947
    source: Marie_Alix_of_Schaumburg-Lippe
    literal_type: xsd:integer
  AddTriple (30e6dff7-91eb-43b4-bb93-799c67f61844)
 Call ID: 30e6dff7-91eb-43b4-bb93-799c67f61844
  Args:
    source: Marie_Alix_of_Schaumburg-Lippe
    relation: :hasRelation
    target: Peter_Duke_of_Schleswig-Holstein
  AssignClass (c00beaf2-290e-4f84-aa17-519210d5a177)
 Call ID: c00beaf2-290e-4f84-aa17-519210d5a177
  Args:
    source: Prince_Stefan_of_Schaumburg-Lippe
    type: :Man
  AssignClass (fd3b4c81-d130-4531-b859-d89603bb0517)
 Call ID: fd3b4c81-d130-4531-b859-d89603bb0517
  Args:
    source: Prince_Stefan_of_Schaumburg-Lippe
    type: :Person
  AssignClass (9b3a543f-b4b5-489b-b021-176fad7a7e74)
 Call ID: 9b3a543f-b4b5-489b-b021-176fad7a7e74
  Args:
    source: Ingeborg_Alix
    type: :Woman
  AssignClass (655bd8f3-8f17-467c-8b0f-b2ca4a265f69)
 Call ID: 655bd8f3-8f17-467c-8b0f-b2ca4a265f69
  Args:
    source: Ingeborg_Alix
    type: :Person
  AddTriple (3c6507dc-e278-4012-b1da-63934dcf53f4)
 Call ID: 3c6507dc-e278-4012-b1da-63934dcf53f4
  Args:
    source: Marie_Alix_of_Schaumburg-Lippe
    relation: :hasFather
    target: Prince_Stefan_of_Schaumburg-Lippe
  AddTriple (a57439c9-1568-498a-a5a8-93639106624b)
 Call ID: a57439c9-1568-498a-a5a8-93639106624b
  Args:
    relation: :hasMother
    target: Ingeborg_Alix
    source: Marie_Alix_of_Schaumburg-Lippe
  AssignClass (2592736e-493f-4cbf-b976-baef1323c7ce)
 Call ID: 2592736e-493f-4cbf-b976-baef1323c7ce
  Args:
    type: :Man
    source: Adolf_II_of_Schaumburg-Lippe
  AssignClass (2d8194f3-6d4a-4518-a0be-c56587158c37)
 Call ID: 2d8194f3-6d4a-4518-a0be-c56587158c37
  Args:
    source: Adolf_II_of_Schaumburg-Lippe
    type: :Person
  AssignClass (15b58da3-6948-4012-bf4c-daca10b10d95)
 Call ID: 15b58da3-6948-4012-bf4c-daca10b10d95
  Args:
    type: :Man
    source: Prince_Georg_Moritz_of_Schaumburg-Lippe
  AssignClass (7ab3af02-8106-4d06-b355-8f6ea49ad3f5)
 Call ID: 7ab3af02-8106-4d06-b355-8f6ea49ad3f5
  Args:
    type: :Person
    source: Prince_Georg_Moritz_of_Schaumburg-Lippe
  AddTriple (8b648939-0685-4e62-801b-5db7f6377b44)
 Call ID: 8b648939-0685-4e62-801b-5db7f6377b44
  Args:
    source: Marie_Alix_of_Schaumburg-Lippe
    relation: :hasBrother
    target: Prince_Georg_Moritz_of_Schaumburg-Lippe
  AssignClass (3507c846-ec0d-45d1-ab83-ed47098d59f6)
 Call ID: 3507c846-ec0d-45d1-ab83-ed47098d59f6
  Args:
    type: :Man
    source: Wilhelm_Friedrich_Duke_of_Schleswig-Holstein
  AssignClass (71671b4a-0930-4560-9031-6456c0039c27)
 Call ID: 71671b4a-0930-4560-9031-6456c0039c27
  Args:
    source: Wilhelm_Friedrich_Duke_of_Schleswig-Holstein
    type: :Person
  AssignClass (bb43fe38-08d9-40cc-b637-d290fd800d8a)
 Call ID: bb43fe38-08d9-40cc-b637-d290fd800d8a
  Args:
    type: :Woman
    source: Princess_Marie_Melita_of_Hohenlohe-Langenburg
  AssignClass (6f1344c1-0cb6-4a72-bcc2-e8ebc7d2c359)
 Call ID: 6f1344c1-0cb6-4a72-bcc2-e8ebc7d2c359
  Args:
    source: Princess_Marie_Melita_of_Hohenlohe-Langenburg
    type: :Person
  AddTriple (982966a7-0762-4c6f-9a88-adcb3e852383)
 Call ID: 982966a7-0762-4c6f-9a88-adcb3e852383
  Args:
    target: Wilhelm_Friedrich_Duke_of_Schleswig-Holstein
    relation: :hasFather
    source: Peter_Duke_of_Schleswig-Holstein
  AddTriple (c1592955-2045-4773-818a-a26fb787f6c6)
 Call ID: c1592955-2045-4773-818a-a26fb787f6c6
  Args:
    source: Peter_Duke_of_Schleswig-Holstein
    relation: :hasMother
    target: Princess_Marie_Melita_of_Hohenlohe-Langenburg
  Finish (e60d1a0b-126d-419a-94ab-e9840e444a0c)
 Call ID: e60d1a0b-126d-419a-94ab-e9840e444a0c
  Args: