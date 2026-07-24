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
John Ulick Knatchbull, 7th Baron Brabourne, CBE (9 November 1924 – 23 September 2005), professionally known as John Brabourne, was a British peer, television producer and Oscar-nominated film producer.
Married to the elder daughter of 1st Earl Mountbatten, Brabourne was a survivor of the bombing which killed his father-in-law, mother and son.
Biography

Brabourne was born in 1924, the second son of Michael Knatchbull, 5th Baron Brabourne, and his wife, Lady Doreen Browne.
Marriage

At the end of the war, Brabourne returned to England and settled in the family seat, Mersham in Kent.
On 26 October 1946, at Romsey Abbey in Hampshire, at the age of 21, he married Patricia Mountbatten, elder daughter of Louis Mountbatten, 1st Viscount Mountbatten, later 1st
Earl Mountbatten of Burma.
Brabourne's best man at the wedding was Squadron Leader Charles Harris-St. John.
Lady Brabourne was to inherit her father's peerages in due course.
This would make Lord and Lady Brabourne among the few married couples to each hold peerages in their own right.
Also, Lady Brabourne was related to the British royal family, and her aunt Louise Mountbatten was at that time the Crown Princess (later Queen) of Sweden.
In February 1947, only months after the wedding, Brabourne's father-in-law was appointed Viceroy of India.
In November the same year, Lady Brabourne's first cousin Philip, Duke of Edinburgh, wed Princess Elizabeth, future queen of the United Kingdom.
Lord and Lady Brabourne had eight children, including Norton Louis Philip Knatchbull, 3rd Earl Mountbatten of Burma (born 8 October 1947), Lady Amanda Patricia Victoria Knatchbull (born 26 June 1957), and Nicholas Timothy Charles Knatchbull.
Career and service

In the late 1940s, shortly after leaving the army, Brabourne began working as an assistant production manager for certain television productions, mostly based on war-related themes.
John Brabourne received two Academy Award nominations for Best Picture, as producer of Romeo and Juliet (1968) and A Passage to India (1984).
In 1985, Brabourne was invested as a Fellow of the British Film Institute, an organisation he also served as a Governor.
Brabourne served as a governor of various schools, including Norton Knatchbull School (founded by an ancestor c. 1630 AD) from 1947 to 2000; Wye College in Kent from 1955 to 2000, and Gordonstoun School from 1964 to 1994.
IRA bombing

On 27 August 1979, while the family was on holiday in Mullaghmore, County Sligo, Lord Brabourne's father-in-law, Earl Mountbatten of Burma, took a number of family members out lobstering on his motorboat, Shadow V, in Donegal Bay.
Having planned to murder Mountbatten, the Irish Republican Army (IRA) placed a bomb inside the boat on the night of the 26th.
Mountbatten and several members of the party were killed the next morning when the bomb was triggered by an IRA observer onshore who was armed with a radio detonator.
The dead included Brabourne's 83-year-old mother, the Dowager Baroness Brabourne; one of his twin 14-year-old sons, Nicholas Knatchbull; and 15-year-old Paul Maxwell from County Fermanagh who had been hired for the summer as Mountbatten's boat boy.
Brabourne, his wife Patricia, and their other twin son Timothy were severely injured, but survived the attack.
Lord Brabourne died on 23 September 2005 at his home in Kent, aged 80.
His wife Patricia, Countess Mountbatten of Burma, died in June 2017.



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
  AssignClass (2939babf-fb22-4bc8-87ea-c1834a69d041)
 Call ID: 2939babf-fb22-4bc8-87ea-c1834a69d041
  Args:
    type: :Man
    source: John_Ulick_Knatchbull
  AssignClass (1c6ab0d9-2c1e-47f6-a8cf-f329408d707d)
 Call ID: 1c6ab0d9-2c1e-47f6-a8cf-f329408d707d
  Args:
    source: John_Ulick_Knatchbull
    type: :Person
  AddLiteral (1c68617d-3c26-46ae-8d4f-4bdab4a03c22)
 Call ID: 1c68617d-3c26-46ae-8d4f-4bdab4a03c22
  Args:
    literal_type: xsd:integer
    source: John_Ulick_Knatchbull
    literal_value: 1924
    relation: :hasBirthYear
  AddLiteral (c73ddf75-7c75-49d5-a69e-a166ef070764)
 Call ID: c73ddf75-7c75-49d5-a69e-a166ef070764
  Args:
    literal_type: xsd:integer
    literal_value: 2005
    source: John_Ulick_Knatchbull
    relation: :hasDeathYear
  AddLiteral (4cbbcb40-323b-4bba-abe2-4baabaf63013)
 Call ID: 4cbbcb40-323b-4bba-abe2-4baabaf63013
  Args:
    relation: :knownAs
    source: John_Ulick_Knatchbull
    literal_value: John Brabourne
    literal_type: xsd:string
  AssignClass (95dc73a4-2673-490c-9736-961923e6dace)
 Call ID: 95dc73a4-2673-490c-9736-961923e6dace
  Args:
    type: :Man
    source: Michael_Knatchbull
  AssignClass (cd508ff5-0d52-4a0b-a953-f774bb45a267)
 Call ID: cd508ff5-0d52-4a0b-a953-f774bb45a267
  Args:
    type: :Person
    source: Michael_Knatchbull
  AssignClass (a32c2d68-2d7f-483c-877f-3a773751480f)
 Call ID: a32c2d68-2d7f-483c-877f-3a773751480f
  Args:
    type: :Woman
    source: Lady_Doreen_Browne
  AssignClass (ade3dcc8-d778-4d0c-afd6-1dd52be440a0)
 Call ID: ade3dcc8-d778-4d0c-afd6-1dd52be440a0
  Args:
    type: :Person
    source: Lady_Doreen_Browne
  AddTriple (f1200a23-bd74-44bd-a7dc-9093b30ef104)
 Call ID: f1200a23-bd74-44bd-a7dc-9093b30ef104
  Args:
    relation: :hasFather
    target: Michael_Knatchbull
    source: John_Ulick_Knatchbull
  AddTriple (46dc8afc-39b9-4559-ba96-9d672b752ce8)
 Call ID: 46dc8afc-39b9-4559-ba96-9d672b752ce8
  Args:
    relation: :hasMother
    target: Lady_Doreen_Browne
    source: John_Ulick_Knatchbull
  AssignClass (b33a6629-be58-40bc-944a-6242fa8bcd98)
 Call ID: b33a6629-be58-40bc-944a-6242fa8bcd98
  Args:
    type: :Woman
    source: Patricia_Mountbatten
  AssignClass (7dcfbe88-bab6-4f9b-aa86-f3729fdb9f64)
 Call ID: 7dcfbe88-bab6-4f9b-aa86-f3729fdb9f64
  Args:
    source: Patricia_Mountbatten
    type: :Person
  AddTriple (5d77ffc9-5c45-4f1a-9ad2-4d1f8a219e3f)
 Call ID: 5d77ffc9-5c45-4f1a-9ad2-4d1f8a219e3f
  Args:
    target: Louis_Mountbatten
    relation: :hasFather
    source: Patricia_Mountbatten
  AssignClass (c3d073ab-9c84-4eb7-b79b-510c1447bb8b)
 Call ID: c3d073ab-9c84-4eb7-b79b-510c1447bb8b
  Args:
    type: :Man
    source: Louis_Mountbatten
  AssignClass (351885b0-6f24-44b6-b550-ee79a9fb8794)
 Call ID: 351885b0-6f24-44b6-b550-ee79a9fb8794
  Args:
    source: Louis_Mountbatten
    type: :Person
  AddLiteral (9510fc26-7df4-4090-92d8-1f17cc2ff98a)
 Call ID: 9510fc26-7df4-4090-92d8-1f17cc2ff98a
  Args:
    source: John_Ulick_Knatchbull
    literal_value: 1946
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AddTriple (743be83f-236b-47ce-8a29-6f16f6669411)
 Call ID: 743be83f-236b-47ce-8a29-6f16f6669411
  Args:
    target: Patricia_Mountbatten
    relation: :hasRelation
    source: John_Ulick_Knatchbull
  AssignClass (58bc4e42-674a-49bf-bd0c-38ac8947dd8a)
 Call ID: 58bc4e42-674a-49bf-bd0c-38ac8947dd8a
  Args:
    source: Norton_Louis_Philip_Knatchbull
    type: :Man
  AssignClass (1ea1fdcc-a902-415c-8c99-e79da9627166)
 Call ID: 1ea1fdcc-a902-415c-8c99-e79da9627166
  Args:
    type: :Person
    source: Norton_Louis_Philip_Knatchbull
  AddTriple (521d2486-b5b9-4dcf-8f07-5b96381e7e62)
 Call ID: 521d2486-b5b9-4dcf-8f07-5b96381e7e62
  Args:
    relation: :isSonOf
    target: John_Ulick_Knatchbull
    source: Norton_Louis_Philip_Knatchbull
  AddTriple (fd2915ab-6b37-45a6-8ee5-e432af3c61c1)
 Call ID: fd2915ab-6b37-45a6-8ee5-e432af3c61c1
  Args:
    source: Norton_Louis_Philip_Knatchbull
    relation: :isSonOf
    target: Patricia_Mountbatten
  AssignClass (9c846665-8fb8-4aa6-98e5-2928dcf8bce6)
 Call ID: 9c846665-8fb8-4aa6-98e5-2928dcf8bce6
  Args:
    source: Lady_Amanda_Patricia_Victoria_Knatchbull
    type: :Woman
  AssignClass (f8c23245-9ab5-4b96-bf0f-6cdd834fb8ca)
 Call ID: f8c23245-9ab5-4b96-bf0f-6cdd834fb8ca
  Args:
    type: :Person
    source: Lady_Amanda_Patricia_Victoria_Knatchbull
  AddTriple (10c23c8c-c15e-4b54-b3b0-b3809059632d)
 Call ID: 10c23c8c-c15e-4b54-b3b0-b3809059632d
  Args:
    target: John_Ulick_Knatchbull
    relation: :isDaughterOf
    source: Lady_Amanda_Patricia_Victoria_Knatchbull
  AddTriple (dca0d472-57a9-4492-8305-f8bd5c950ae0)
 Call ID: dca0d472-57a9-4492-8305-f8bd5c950ae0
  Args:
    relation: :isDaughterOf
    target: Patricia_Mountbatten
    source: Lady_Amanda_Patricia_Victoria_Knatchbull
  AssignClass (8bf57ffb-3d3d-4c12-a675-aeb785f67828)
 Call ID: 8bf57ffb-3d3d-4c12-a675-aeb785f67828
  Args:
    source: Nicholas_Timothy_Charles_Knatchbull
    type: :Man
  AssignClass (107fe386-4206-47ff-bd1b-e79636f69424)
 Call ID: 107fe386-4206-47ff-bd1b-e79636f69424
  Args:
    type: :Person
    source: Nicholas_Timothy_Charles_Knatchbull
  AddTriple (5f1cf843-1598-4be6-b6c0-3e6357bf8ee7)
 Call ID: 5f1cf843-1598-4be6-b6c0-3e6357bf8ee7
  Args:
    target: John_Ulick_Knatchbull
    relation: :isSonOf
    source: Nicholas_Timothy_Charles_Knatchbull
  AddTriple (378182b3-c22a-437f-9024-84cf85ba69bd)
 Call ID: 378182b3-c22a-437f-9024-84cf85ba69bd
  Args:
    target: Patricia_Mountbatten
    relation: :isSonOf
    source: Nicholas_Timothy_Charles_Knatchbull
  AssignClass (2f32fc1a-f9c8-49b2-af07-58df705c9743)
 Call ID: 2f32fc1a-f9c8-49b2-af07-58df705c9743
  Args:
    source: Timothy_Knatchbull
    type: :Man
  AssignClass (e604fe2e-cdd5-480d-b881-50882e29257c)
 Call ID: e604fe2e-cdd5-480d-b881-50882e29257c
  Args:
    source: Timothy_Knatchbull
    type: :Person
  AddTriple (40c707b9-ac07-48ac-ad93-894e2e8e6c73)
 Call ID: 40c707b9-ac07-48ac-ad93-894e2e8e6c73
  Args:
    relation: :isSonOf
    target: John_Ulick_Knatchbull
    source: Timothy_Knatchbull
  AddTriple (a48841f8-541c-4954-98d1-99e0905fc07e)
 Call ID: a48841f8-541c-4954-98d1-99e0905fc07e
  Args:
    relation: :isSonOf
    target: Patricia_Mountbatten
    source: Timothy_Knatchbull
  AssignClass (0dab1791-de22-4020-8633-b35bed421ebc)
 Call ID: 0dab1791-de22-4020-8633-b35bed421ebc
  Args:
    source: Louise_Mountbatten
    type: :Woman
  AssignClass (bb80e28e-aff4-4cff-a626-c0b4e5c6cdf7)
 Call ID: bb80e28e-aff4-4cff-a626-c0b4e5c6cdf7
  Args:
    source: Louise_Mountbatten
    type: :Person
  AddTriple (ac294640-0f3c-4377-8ea1-77ad0c68ab2b)
 Call ID: ac294640-0f3c-4377-8ea1-77ad0c68ab2b
  Args:
    source: Louise_Mountbatten
    target: Patricia_Mountbatten
    relation: :isAuntOf
  Finish (7fad6ecc-2587-4d8c-b57b-bc41d7e319d8)
 Call ID: 7fad6ecc-2587-4d8c-b57b-bc41d7e319d8
  Args: