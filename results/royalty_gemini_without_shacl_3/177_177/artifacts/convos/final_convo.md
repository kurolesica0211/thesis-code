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
  AssignClass (1de09fc2-eaa2-4c56-b628-cb7a3c5fbf2c)
 Call ID: 1de09fc2-eaa2-4c56-b628-cb7a3c5fbf2c
  Args:
    type: :Woman
    source: Elisabeth_of_Denmark
  AssignClass (04addd45-9150-4efa-bcc7-87ec865e965a)
 Call ID: 04addd45-9150-4efa-bcc7-87ec865e965a
  Args:
    type: :Person
    source: Elisabeth_of_Denmark
  AddLiteral (702b8786-90a9-4c3d-bd92-b998e06140d7)
 Call ID: 702b8786-90a9-4c3d-bd92-b998e06140d7
  Args:
    source: Elisabeth_of_Denmark
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1935
  AddLiteral (a4d8c0bd-935c-4e50-a3b7-d64b4faac1f8)
 Call ID: a4d8c0bd-935c-4e50-a3b7-d64b4faac1f8
  Args:
    literal_value: 2018
    source: Elisabeth_of_Denmark
    literal_type: xsd:integer
    relation: :hasDeathYear
  AssignClass (62113605-0305-4b02-849b-7b5161368f84)
 Call ID: 62113605-0305-4b02-849b-7b5161368f84
  Args:
    type: :Man
    source: Knud_Hereditary_Prince_of_Denmark
  AssignClass (3933218e-85de-4ffb-9902-e17ad5f5a4ff)
 Call ID: 3933218e-85de-4ffb-9902-e17ad5f5a4ff
  Args:
    type: :Person
    source: Knud_Hereditary_Prince_of_Denmark
  AssignClass (807ca00c-390b-4f29-9679-fd52f9b5d6b7)
 Call ID: 807ca00c-390b-4f29-9679-fd52f9b5d6b7
  Args:
    type: :Woman
    source: Caroline-Mathilde_of_Denmark
  AssignClass (2556c7b7-d54f-4a31-9a14-574d4973051a)
 Call ID: 2556c7b7-d54f-4a31-9a14-574d4973051a
  Args:
    type: :Person
    source: Caroline-Mathilde_of_Denmark
  AddTriple (37a2e16e-c93e-4577-b795-30e1aabcd13d)
 Call ID: 37a2e16e-c93e-4577-b795-30e1aabcd13d
  Args:
    target: Knud_Hereditary_Prince_of_Denmark
    relation: :hasFather
    source: Elisabeth_of_Denmark
  AddTriple (0c7c82f3-015a-4d32-b897-89995acab009)
 Call ID: 0c7c82f3-015a-4d32-b897-89995acab009
  Args:
    relation: :hasMother
    source: Elisabeth_of_Denmark
    target: Caroline-Mathilde_of_Denmark
  AssignClass (072e9210-0472-4c66-ab65-c3553220e50e)
 Call ID: 072e9210-0472-4c66-ab65-c3553220e50e
  Args:
    type: :Man
    source: Christian_X
  AssignClass (81f70023-3342-4b2c-9ba4-561897202718)
 Call ID: 81f70023-3342-4b2c-9ba4-561897202718
  Args:
    type: :Person
    source: Christian_X
  AddTriple (42d7a1ac-d758-40ee-b4a3-0cdc80ccf8e8)
 Call ID: 42d7a1ac-d758-40ee-b4a3-0cdc80ccf8e8
  Args:
    target: Christian_X
    relation: :hasFather
    source: Knud_Hereditary_Prince_of_Denmark
  AssignClass (fb6e4692-5dd5-4426-acfb-51e7d3a70d91)
 Call ID: fb6e4692-5dd5-4426-acfb-51e7d3a70d91
  Args:
    type: :Man
    source: Ingolf_of_Denmark
  AssignClass (9b0087c6-ff88-4415-9c34-88bdcd844943)
 Call ID: 9b0087c6-ff88-4415-9c34-88bdcd844943
  Args:
    type: :Person
    source: Ingolf_of_Denmark
  AssignClass (137220c7-41fa-4bba-ae91-764405f0c7c8)
 Call ID: 137220c7-41fa-4bba-ae91-764405f0c7c8
  Args:
    type: :Man
    source: Christian_of_Denmark
  AssignClass (eb194559-c601-4c45-8f7b-d73a572834b5)
 Call ID: eb194559-c601-4c45-8f7b-d73a572834b5
  Args:
    type: :Person
    source: Christian_of_Denmark
  AddTriple (30c8368c-7972-440a-ad41-b47876c1cfc0)
 Call ID: 30c8368c-7972-440a-ad41-b47876c1cfc0
  Args:
    target: Ingolf_of_Denmark
    source: Elisabeth_of_Denmark
    relation: :hasBrother
  AddTriple (4edbba19-fe39-49e3-81d8-be53237dc92b)
 Call ID: 4edbba19-fe39-49e3-81d8-be53237dc92b
  Args:
    target: Christian_of_Denmark
    relation: :hasBrother
    source: Elisabeth_of_Denmark
  AddTriple (5b8a5d2c-856d-43ae-9428-7ad302cc5b94)
 Call ID: 5b8a5d2c-856d-43ae-9428-7ad302cc5b94
  Args:
    target: Knud_Hereditary_Prince_of_Denmark
    relation: :hasFather
    source: Ingolf_of_Denmark
  AddTriple (b2ea71f1-bb17-4153-a4ac-c071e0f375d0)
 Call ID: b2ea71f1-bb17-4153-a4ac-c071e0f375d0
  Args:
    source: Christian_of_Denmark
    relation: :hasFather
    target: Knud_Hereditary_Prince_of_Denmark
  AddTriple (ce4e3ca7-9346-4e0b-830b-b65c5f1de39e)
 Call ID: ce4e3ca7-9346-4e0b-830b-b65c5f1de39e
  Args:
    target: Caroline-Mathilde_of_Denmark
    relation: :hasMother
    source: Ingolf_of_Denmark
  AddTriple (d3d30662-170e-4364-8603-88a21a60c2d1)
 Call ID: d3d30662-170e-4364-8603-88a21a60c2d1
  Args:
    relation: :hasMother
    source: Christian_of_Denmark
    target: Caroline-Mathilde_of_Denmark
  AssignClass (62183784-3ce0-408c-88dc-70f5493228ae)
 Call ID: 62183784-3ce0-408c-88dc-70f5493228ae
  Args:
    type: :Man
    source: Frederik_IX
  AssignClass (b8a7dae2-2216-49a7-9175-01d1f214c2d7)
 Call ID: b8a7dae2-2216-49a7-9175-01d1f214c2d7
  Args:
    type: :Person
    source: Frederik_IX
  AssignClass (4b70b71e-862f-4b69-82d4-353bd463dd0b)
 Call ID: 4b70b71e-862f-4b69-82d4-353bd463dd0b
  Args:
    type: :Woman
    source: Margrethe_II
  AssignClass (da6e29f1-a751-4005-bc82-bf75337d512e)
 Call ID: da6e29f1-a751-4005-bc82-bf75337d512e
  Args:
    type: :Person
    source: Margrethe_II
  Finish (2e8d2818-56f3-45ba-ac0c-00cdd2228c28)
 Call ID: 2e8d2818-56f3-45ba-ac0c-00cdd2228c28
  Args: