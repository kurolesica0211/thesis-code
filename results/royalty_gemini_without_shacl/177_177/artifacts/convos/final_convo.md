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
  AssignClass (6bf6bc64-e01b-4389-ac0e-4c01da610b8a)
 Call ID: 6bf6bc64-e01b-4389-ac0e-4c01da610b8a
  Args:
    source: PrincessElisabethOfDenmark
    type: :Woman
  AssignClass (33b2665f-622e-4235-8e8c-dd3bbc4e837d)
 Call ID: 33b2665f-622e-4235-8e8c-dd3bbc4e837d
  Args:
    source: PrincessElisabethOfDenmark
    type: :Person
  AddLiteral (94742dc4-3678-4e79-a773-aa22194ace8b)
 Call ID: 94742dc4-3678-4e79-a773-aa22194ace8b
  Args:
    literal_type: xsd:integer
    literal_value: 1935
    relation: :hasBirthYear
    source: PrincessElisabethOfDenmark
  AddLiteral (b076c88f-bb44-46b4-a087-9a9bce03dba4)
 Call ID: b076c88f-bb44-46b4-a087-9a9bce03dba4
  Args:
    literal_type: xsd:integer
    literal_value: 2018
    relation: :hasDeathYear
    source: PrincessElisabethOfDenmark
  AssignClass (15d71d2b-f3ee-4b63-9762-eb1eec88b35f)
 Call ID: 15d71d2b-f3ee-4b63-9762-eb1eec88b35f
  Args:
    source: KnudHereditaryPrinceOfDenmark
    type: :Man
  AssignClass (38bd050b-93fe-4e17-bd39-37da87f6a6c4)
 Call ID: 38bd050b-93fe-4e17-bd39-37da87f6a6c4
  Args:
    source: KnudHereditaryPrinceOfDenmark
    type: :Person
  AssignClass (5ec7742a-991b-4633-9099-88a98199d44e)
 Call ID: 5ec7742a-991b-4633-9099-88a98199d44e
  Args:
    source: PrincessCarolineMathildeOfDenmark
    type: :Woman
  AssignClass (a6f06ec0-5f91-44c9-b145-91dde3060709)
 Call ID: a6f06ec0-5f91-44c9-b145-91dde3060709
  Args:
    type: :Person
    source: PrincessCarolineMathildeOfDenmark
  AddTriple (04ca5ad2-b944-4857-a992-b63e53a1a9ad)
 Call ID: 04ca5ad2-b944-4857-a992-b63e53a1a9ad
  Args:
    target: KnudHereditaryPrinceOfDenmark
    relation: :hasFather
    source: PrincessElisabethOfDenmark
  AddTriple (e14058cd-7b73-4b44-9133-43756118e926)
 Call ID: e14058cd-7b73-4b44-9133-43756118e926
  Args:
    source: PrincessElisabethOfDenmark
    relation: :hasMother
    target: PrincessCarolineMathildeOfDenmark
  AssignClass (22f8e40c-f9b1-4c94-9db2-392a62585cd4)
 Call ID: 22f8e40c-f9b1-4c94-9db2-392a62585cd4
  Args:
    source: ChristianX
    type: :Man
  AssignClass (21fb213d-48fb-45e4-9ead-b8c94e716ee3)
 Call ID: 21fb213d-48fb-45e4-9ead-b8c94e716ee3
  Args:
    source: ChristianX
    type: :Person
  AddTriple (7f759191-8e12-4095-81bc-e08a0d1161eb)
 Call ID: 7f759191-8e12-4095-81bc-e08a0d1161eb
  Args:
    source: KnudHereditaryPrinceOfDenmark
    relation: :hasFather
    target: ChristianX
  AssignClass (3926ada5-8a81-4607-a4f7-7c27ad4dcbe2)
 Call ID: 3926ada5-8a81-4607-a4f7-7c27ad4dcbe2
  Args:
    type: :Man
    source: PrinceIngolf
  AssignClass (d27c33c3-df1a-4390-9623-44f72ff8a3e3)
 Call ID: d27c33c3-df1a-4390-9623-44f72ff8a3e3
  Args:
    source: PrinceIngolf
    type: :Person
  AssignClass (00f99f75-d141-44a5-b16f-6858358a8b67)
 Call ID: 00f99f75-d141-44a5-b16f-6858358a8b67
  Args:
    type: :Man
    source: PrinceChristian
  AssignClass (389c45d0-cff8-481e-90c3-bd21dde1e727)
 Call ID: 389c45d0-cff8-481e-90c3-bd21dde1e727
  Args:
    source: PrinceChristian
    type: :Person
  AddTriple (19716898-9eb7-4376-b40d-0413997fdcf9)
 Call ID: 19716898-9eb7-4376-b40d-0413997fdcf9
  Args:
    target: PrinceIngolf
    relation: :isSiblingOf
    source: PrincessElisabethOfDenmark
  AddTriple (380e9d31-0f42-4f5f-be22-4884da7a5e63)
 Call ID: 380e9d31-0f42-4f5f-be22-4884da7a5e63
  Args:
    target: PrinceChristian
    relation: :isSiblingOf
    source: PrincessElisabethOfDenmark
  AssignClass (dee4ee1b-36bd-406b-beea-754102067551)
 Call ID: dee4ee1b-36bd-406b-beea-754102067551
  Args:
    source: FrederikIX
    type: :Man
  AssignClass (a0365fef-5447-47b9-83f5-0ef1ffc1ba40)
 Call ID: a0365fef-5447-47b9-83f5-0ef1ffc1ba40
  Args:
    type: :Person
    source: FrederikIX
  AssignClass (386c8fa8-c02d-4afb-8923-142c5d26a375)
 Call ID: 386c8fa8-c02d-4afb-8923-142c5d26a375
  Args:
    source: MargretheII
    type: :Woman
  AssignClass (89f1e799-207c-4aa1-b872-d59d27c2644f)
 Call ID: 89f1e799-207c-4aa1-b872-d59d27c2644f
  Args:
    type: :Person
    source: MargretheII
  Finish (abd7384c-55fb-4da6-a208-93d3a8ea70de)
 Call ID: abd7384c-55fb-4da6-a208-93d3a8ea70de
  Args: