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
Princess Elisabeth of Denmark (Elisabeth Caroline-Mathilde Alexandrine Helena Olga Thyra Feodora Estrid Margrethe Désirée; 8 May 1935 – 19 June 2018) was a member of the Danish royal family.
The only daughter and eldest child of Knud, Hereditary Prince of Denmark, and Princess Caroline-Mathilde of Denmark, she was a granddaughter of Christian X, niece of Frederik IX, and first cousin of Margrethe II.
In addition to undertaking occasionally royal duties, she was a career diplomat with the Ministry of Foreign Affairs of Denmark.
Early life and education

Elisabeth was born on 8 May 1935 in Copenhagen to Prince Knud and Princess Caroline-Mathilde of Denmark.
Her father was the second son of Christian X.
The family resided at Sorgenfri Palace in Kongens Lyngby, where she was raised with her two younger brothers Prince Ingolf and Prince Christian.
During the 1938-39 Mørkefjord expedition, paleontologist Eigil Nielsen named the Princess Elisabeth Alps in northeastern Greenland after her.
Elisabeth began her education privately at Sorgenfri.
In 1953, when  succession to the Danish throne switched from agnatic primogeniture to male-preference primogeniture, Elisabeth gained succession rights and became seventh in line to the throne.
She was titled of Prinsesse til Danmark (literally translated as "Princess to Denmark", reserved for members of the Royal Family in the line of succession) with the style of Highness.
She was the only one of her siblings to retain her title and succession rights, as her younger brothers married commoners without the permission of their uncle, Frederik IX.
Career

In 1956, Elisabeth began her career with the Danish Ministry of Foreign Affairs.
She was posted to the Embassy of Denmark, Washington, D.C. from 1973 to 1976 and again from 1981 to 1985.
In addition to her diplomatic career, Elisabeth occasionally undertook royal duties on behalf of her uncle and later cousin.
Personal life and death

Elisabeth never married nor had children.
After a long period of ill health, Elisabeth died on 19 June 2018, at the age of 83.



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
  AssignClass (84d4981d-ddd1-411f-84f8-8e7c00d55285)
 Call ID: 84d4981d-ddd1-411f-84f8-8e7c00d55285
  Args:
    source: Elisabeth_of_Denmark
    type: :Woman
  AssignClass (a67a355c-4822-40a3-b8b5-1488e505b589)
 Call ID: a67a355c-4822-40a3-b8b5-1488e505b589
  Args:
    source: Elisabeth_of_Denmark
    type: :Person
  AddLiteral (fd3371f5-32e3-413d-a146-c363fcd1e45b)
 Call ID: fd3371f5-32e3-413d-a146-c363fcd1e45b
  Args:
    literal_value: 1935
    relation: :hasBirthYear
    source: Elisabeth_of_Denmark
    literal_type: xsd:integer
  AddLiteral (96a65ea7-1335-44e1-96de-2621649fe4aa)
 Call ID: 96a65ea7-1335-44e1-96de-2621649fe4aa
  Args:
    literal_value: 2018
    literal_type: xsd:integer
    source: Elisabeth_of_Denmark
    relation: :hasDeathYear
  AssignClass (1a0a2274-1974-42e6-857f-1f59ec3ccfca)
 Call ID: 1a0a2274-1974-42e6-857f-1f59ec3ccfca
  Args:
    type: :Man
    source: Knud_Hereditary_Prince_of_Denmark
  AssignClass (b56cc50e-69db-49a6-a404-4961f3c7cef4)
 Call ID: b56cc50e-69db-49a6-a404-4961f3c7cef4
  Args:
    type: :Person
    source: Knud_Hereditary_Prince_of_Denmark
  AssignClass (4047c7a4-692c-4c3f-b35e-7e838175d72d)
 Call ID: 4047c7a4-692c-4c3f-b35e-7e838175d72d
  Args:
    source: Knud_Hereditary_Prince_of_Denmark
    type: :Ancestor
  AssignClass (2af23963-77ad-41c9-b5de-ce2e82cc2377)
 Call ID: 2af23963-77ad-41c9-b5de-ce2e82cc2377
  Args:
    type: :Woman
    source: Caroline-Mathilde_of_Denmark
  AssignClass (115e51c7-d28d-408d-8bd9-e112b0274710)
 Call ID: 115e51c7-d28d-408d-8bd9-e112b0274710
  Args:
    source: Caroline-Mathilde_of_Denmark
    type: :Person
  AssignClass (a2f3aafc-b232-4cd9-8dd1-cfc12a19fe7f)
 Call ID: a2f3aafc-b232-4cd9-8dd1-cfc12a19fe7f
  Args:
    source: Caroline-Mathilde_of_Denmark
    type: :Ancestor
  AddTriple (bc764e3e-c092-4849-8651-615b3942e5dd)
 Call ID: bc764e3e-c092-4849-8651-615b3942e5dd
  Args:
    target: Knud_Hereditary_Prince_of_Denmark
    source: Elisabeth_of_Denmark
    relation: :hasFather
  AddTriple (cd2d96e6-92f8-4868-888a-eb1d47f0b9d0)
 Call ID: cd2d96e6-92f8-4868-888a-eb1d47f0b9d0
  Args:
    target: Caroline-Mathilde_of_Denmark
    source: Elisabeth_of_Denmark
    relation: :hasMother
  AssignClass (431f6fdf-bfe8-4c14-a76f-9a1d32f40f53)
 Call ID: 431f6fdf-bfe8-4c14-a76f-9a1d32f40f53
  Args:
    source: Christian_X
    type: :Man
  AssignClass (378983de-9937-4d5d-aebf-43a45ee3a58d)
 Call ID: 378983de-9937-4d5d-aebf-43a45ee3a58d
  Args:
    source: Christian_X
    type: :Person
  AssignClass (c4d1e954-174e-49e6-853e-bee77cd5475c)
 Call ID: c4d1e954-174e-49e6-853e-bee77cd5475c
  Args:
    type: :Ancestor
    source: Christian_X
  AddTriple (5e6e5cac-ea13-40f4-b2da-b17f2e03acf7)
 Call ID: 5e6e5cac-ea13-40f4-b2da-b17f2e03acf7
  Args:
    relation: :hasFather
    source: Knud_Hereditary_Prince_of_Denmark
    target: Christian_X
  AssignClass (e39dfbec-5f71-489c-af73-c58856096c9b)
 Call ID: e39dfbec-5f71-489c-af73-c58856096c9b
  Args:
    type: :Man
    source: Ingolf_of_Denmark
  AssignClass (3efe3516-682f-4c14-a761-4b353df8b309)
 Call ID: 3efe3516-682f-4c14-a761-4b353df8b309
  Args:
    type: :Person
    source: Ingolf_of_Denmark
  AssignClass (cca51b5a-389a-4248-a560-20b2e3926429)
 Call ID: cca51b5a-389a-4248-a560-20b2e3926429
  Args:
    source: Christian_of_Denmark
    type: :Man
  AssignClass (236795ba-5d59-4cad-ac0b-eb528882f21f)
 Call ID: 236795ba-5d59-4cad-ac0b-eb528882f21f
  Args:
    source: Christian_of_Denmark
    type: :Person
  AddTriple (4e5f9491-5897-47b6-bb67-8bb7d5ebe218)
 Call ID: 4e5f9491-5897-47b6-bb67-8bb7d5ebe218
  Args:
    target: Ingolf_of_Denmark
    source: Elisabeth_of_Denmark
    relation: :hasBrother
  AddTriple (7e00438d-083e-49fa-927b-3a0c9b864aed)
 Call ID: 7e00438d-083e-49fa-927b-3a0c9b864aed
  Args:
    relation: :hasBrother
    source: Elisabeth_of_Denmark
    target: Christian_of_Denmark
  AddTriple (aa14bbcc-48d6-4a30-abd4-63363204db7a)
 Call ID: aa14bbcc-48d6-4a30-abd4-63363204db7a
  Args:
    source: Ingolf_of_Denmark
    relation: :hasFather
    target: Knud_Hereditary_Prince_of_Denmark
  AddTriple (1e1063cd-87fb-464c-9686-c92df5ef5253)
 Call ID: 1e1063cd-87fb-464c-9686-c92df5ef5253
  Args:
    target: Caroline-Mathilde_of_Denmark
    source: Ingolf_of_Denmark
    relation: :hasMother
  AddTriple (62b9abda-9868-4817-97ad-5f19685a242f)
 Call ID: 62b9abda-9868-4817-97ad-5f19685a242f
  Args:
    source: Christian_of_Denmark
    relation: :hasFather
    target: Knud_Hereditary_Prince_of_Denmark
  AddTriple (a403f4c9-4c2f-4b8a-87b4-949ae6a066b5)
 Call ID: a403f4c9-4c2f-4b8a-87b4-949ae6a066b5
  Args:
    target: Caroline-Mathilde_of_Denmark
    relation: :hasMother
    source: Christian_of_Denmark
  AssignClass (a0b40fc1-14a5-498d-b6be-63375ad2b6de)
 Call ID: a0b40fc1-14a5-498d-b6be-63375ad2b6de
  Args:
    source: Frederik_IX
    type: :Man
  AssignClass (03105f98-41df-41a6-b3eb-4471d5b21e4f)
 Call ID: 03105f98-41df-41a6-b3eb-4471d5b21e4f
  Args:
    type: :Person
    source: Frederik_IX
  AssignClass (f96e30f3-2d6e-4532-b9c3-d6a94bd1353e)
 Call ID: f96e30f3-2d6e-4532-b9c3-d6a94bd1353e
  Args:
    source: Margrethe_II
    type: :Woman
  AssignClass (78f7009e-4f6c-48c1-bd12-77d4025e9f38)
 Call ID: 78f7009e-4f6c-48c1-bd12-77d4025e9f38
  Args:
    source: Margrethe_II
    type: :Person
  Finish (3c59d0ec-30cb-40e0-ae49-120c381f316e)
 Call ID: 3c59d0ec-30cb-40e0-ae49-120c381f316e
  Args: