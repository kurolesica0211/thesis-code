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
  AssignClass (cb868f09-9000-4440-ad28-ac5b5efb6a5e)
 Call ID: cb868f09-9000-4440-ad28-ac5b5efb6a5e
  Args:
    type: :Man
    source: John_Ulick_Knatchbull
  AssignClass (28103078-db58-499d-9cb9-1d27ce269309)
 Call ID: 28103078-db58-499d-9cb9-1d27ce269309
  Args:
    type: :Person
    source: John_Ulick_Knatchbull
  AddLiteral (46b71690-ec82-4daf-99a1-8ff26a862f41)
 Call ID: 46b71690-ec82-4daf-99a1-8ff26a862f41
  Args:
    literal_type: xsd:string
    source: John_Ulick_Knatchbull
    literal_value: John Brabourne
    relation: :knownAs
  AddLiteral (e157b94e-2f84-4b7b-b4e8-f46ec4da1e64)
 Call ID: e157b94e-2f84-4b7b-b4e8-f46ec4da1e64
  Args:
    source: John_Ulick_Knatchbull
    literal_value: 1924
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (06a55ceb-9fc3-4b71-93fa-3771cb3b8e8a)
 Call ID: 06a55ceb-9fc3-4b71-93fa-3771cb3b8e8a
  Args:
    relation: :hasDeathYear
    source: John_Ulick_Knatchbull
    literal_type: xsd:integer
    literal_value: 2005
  AssignClass (d3ceb866-07fc-4388-8f84-b7e27e89b8a4)
 Call ID: d3ceb866-07fc-4388-8f84-b7e27e89b8a4
  Args:
    type: :Man
    source: Michael_Knatchbull
  AssignClass (642e53bf-dca5-4e48-9d8b-87a316a7e5f6)
 Call ID: 642e53bf-dca5-4e48-9d8b-87a316a7e5f6
  Args:
    type: :Person
    source: Michael_Knatchbull
  AddTriple (881e4ffe-5306-4b91-9d7a-4d343feace6e)
 Call ID: 881e4ffe-5306-4b91-9d7a-4d343feace6e
  Args:
    target: John_Ulick_Knatchbull
    relation: :isFatherOf
    source: Michael_Knatchbull
  AssignClass (58b6700a-97df-49b6-8519-2b3207270eef)
 Call ID: 58b6700a-97df-49b6-8519-2b3207270eef
  Args:
    type: :Woman
    source: Lady_Doreen_Browne
  AssignClass (fd39304c-2870-497f-b23b-3fcbae749e08)
 Call ID: fd39304c-2870-497f-b23b-3fcbae749e08
  Args:
    type: :Person
    source: Lady_Doreen_Browne
  AddTriple (04178bf4-8ef3-4079-a679-f2d031f9a5ac)
 Call ID: 04178bf4-8ef3-4079-a679-f2d031f9a5ac
  Args:
    source: Lady_Doreen_Browne
    relation: :isMotherOf
    target: John_Ulick_Knatchbull
  AssignClass (9087f1d5-af65-4437-9d98-b19bef34c081)
 Call ID: 9087f1d5-af65-4437-9d98-b19bef34c081
  Args:
    type: :Woman
    source: Patricia_Mountbatten
  AssignClass (fcaeefbc-02f4-4986-82fb-2bf9e0034298)
 Call ID: fcaeefbc-02f4-4986-82fb-2bf9e0034298
  Args:
    type: :Person
    source: Patricia_Mountbatten
  AddTriple (8d674042-6dd0-4857-9f55-716631334bad)
 Call ID: 8d674042-6dd0-4857-9f55-716631334bad
  Args:
    target: Patricia_Mountbatten
    relation: :hasRelation
    source: John_Ulick_Knatchbull
  AddLiteral (7d86a4c7-f3b3-4ac6-9d09-303f06d30325)
 Call ID: 7d86a4c7-f3b3-4ac6-9d09-303f06d30325
  Args:
    literal_value: 1946
    source: John_Ulick_Knatchbull
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AssignClass (d82902fb-4b38-4b1e-b25e-87ff26dd4bae)
 Call ID: d82902fb-4b38-4b1e-b25e-87ff26dd4bae
  Args:
    type: :Man
    source: Louis_Mountbatten
  AssignClass (738a0c91-a85b-4d09-be73-75e790c5d832)
 Call ID: 738a0c91-a85b-4d09-be73-75e790c5d832
  Args:
    type: :Person
    source: Louis_Mountbatten
  AddTriple (a3cf1a06-35ca-40d8-8d6f-39aa74c26d04)
 Call ID: a3cf1a06-35ca-40d8-8d6f-39aa74c26d04
  Args:
    source: Louis_Mountbatten
    target: Patricia_Mountbatten
    relation: :isFatherOf
  AssignClass (c66e2afb-2884-4a1e-be84-040d8ebc5ee1)
 Call ID: c66e2afb-2884-4a1e-be84-040d8ebc5ee1
  Args:
    type: :Man
    source: Norton_Louis_Philip_Knatchbull
  AssignClass (ea41b19f-d73c-4525-a782-60cd8f824208)
 Call ID: ea41b19f-d73c-4525-a782-60cd8f824208
  Args:
    type: :Person
    source: Norton_Louis_Philip_Knatchbull
  AddTriple (6701e879-f23e-4dd4-9306-7bf96f147cad)
 Call ID: 6701e879-f23e-4dd4-9306-7bf96f147cad
  Args:
    source: Norton_Louis_Philip_Knatchbull
    relation: :isSonOf
    target: John_Ulick_Knatchbull
  AddTriple (d973cb80-af4f-4e42-99cf-b9daaedb3bbf)
 Call ID: d973cb80-af4f-4e42-99cf-b9daaedb3bbf
  Args:
    source: Norton_Louis_Philip_Knatchbull
    relation: :isSonOf
    target: Patricia_Mountbatten
  AssignClass (7d90e4fc-d13a-4a59-805b-7bcc58fd0daf)
 Call ID: 7d90e4fc-d13a-4a59-805b-7bcc58fd0daf
  Args:
    type: :Woman
    source: Lady_Amanda_Patricia_Victoria_Knatchbull
  AssignClass (b648190e-ace9-4aea-80a3-ff9fbeaf5ee9)
 Call ID: b648190e-ace9-4aea-80a3-ff9fbeaf5ee9
  Args:
    type: :Person
    source: Lady_Amanda_Patricia_Victoria_Knatchbull
  AddTriple (0bb589de-3867-4790-aba9-30f482f90006)
 Call ID: 0bb589de-3867-4790-aba9-30f482f90006
  Args:
    target: John_Ulick_Knatchbull
    relation: :isDaughterOf
    source: Lady_Amanda_Patricia_Victoria_Knatchbull
  AddTriple (2a6b4ee4-101d-46d9-9cd3-9b3e582abc82)
 Call ID: 2a6b4ee4-101d-46d9-9cd3-9b3e582abc82
  Args:
    source: Lady_Amanda_Patricia_Victoria_Knatchbull
    relation: :isDaughterOf
    target: Patricia_Mountbatten
  AssignClass (2610772c-ccc8-4789-8703-5ebdaaa876d4)
 Call ID: 2610772c-ccc8-4789-8703-5ebdaaa876d4
  Args:
    type: :Man
    source: Nicholas_Timothy_Charles_Knatchbull
  AssignClass (df7e5bb6-6d89-4473-935d-bf9dca5edfc7)
 Call ID: df7e5bb6-6d89-4473-935d-bf9dca5edfc7
  Args:
    type: :Person
    source: Nicholas_Timothy_Charles_Knatchbull
  AddTriple (979d0044-e501-44c0-a697-09b9f2cc0a2c)
 Call ID: 979d0044-e501-44c0-a697-09b9f2cc0a2c
  Args:
    target: John_Ulick_Knatchbull
    relation: :isSonOf
    source: Nicholas_Timothy_Charles_Knatchbull
  AddTriple (024ca362-eba4-4acb-9682-32b770591366)
 Call ID: 024ca362-eba4-4acb-9682-32b770591366
  Args:
    source: Nicholas_Timothy_Charles_Knatchbull
    relation: :isSonOf
    target: Patricia_Mountbatten
  AssignClass (aefb78d6-b2e5-4ded-aff3-2d7af0ccde41)
 Call ID: aefb78d6-b2e5-4ded-aff3-2d7af0ccde41
  Args:
    type: :Man
    source: Timothy_Knatchbull
  AssignClass (0c764a3e-cd96-4ca2-803d-dfb46ecb09e2)
 Call ID: 0c764a3e-cd96-4ca2-803d-dfb46ecb09e2
  Args:
    type: :Person
    source: Timothy_Knatchbull
  AddTriple (6c5c9b22-205d-488a-9c65-457df28d4f03)
 Call ID: 6c5c9b22-205d-488a-9c65-457df28d4f03
  Args:
    target: John_Ulick_Knatchbull
    relation: :isSonOf
    source: Timothy_Knatchbull
  AddTriple (a923b89b-4c62-4002-876a-6b665eaedb7c)
 Call ID: a923b89b-4c62-4002-876a-6b665eaedb7c
  Args:
    relation: :isSonOf
    target: Patricia_Mountbatten
    source: Timothy_Knatchbull
  AssignClass (2f432e81-545f-4683-bd4e-fa7050f61c0a)
 Call ID: 2f432e81-545f-4683-bd4e-fa7050f61c0a
  Args:
    type: :Woman
    source: Louise_Mountbatten
  AssignClass (96ab2fd7-d650-4589-8335-efde75ce37a4)
 Call ID: 96ab2fd7-d650-4589-8335-efde75ce37a4
  Args:
    type: :Person
    source: Louise_Mountbatten
  AddTriple (c54cb516-a912-4277-96f2-762f3fe4b110)
 Call ID: c54cb516-a912-4277-96f2-762f3fe4b110
  Args:
    target: Louis_Mountbatten
    relation: :isSisterOf
    source: Louise_Mountbatten
  Finish (73f9f6bc-456b-43b4-b823-cd7b79551929)
 Call ID: 73f9f6bc-456b-43b4-b823-cd7b79551929
  Args: