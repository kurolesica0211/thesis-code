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
  AssignClass (a038032c-07a2-4340-bacf-14063c08c0fd)
 Call ID: a038032c-07a2-4340-bacf-14063c08c0fd
  Args:
    type: :Man
    source: John_Ulick_Knatchbull
  AssignClass (196c122b-c6e2-4567-8144-3d0e63ee9c9f)
 Call ID: 196c122b-c6e2-4567-8144-3d0e63ee9c9f
  Args:
    source: John_Ulick_Knatchbull
    type: :Person
  AddLiteral (cbb9aa1d-371b-47d4-9e5e-c29338a5bffd)
 Call ID: cbb9aa1d-371b-47d4-9e5e-c29338a5bffd
  Args:
    literal_type: xsd:string
    relation: :knownAs
    source: John_Ulick_Knatchbull
    literal_value: John Brabourne
  AddLiteral (1decaccb-f542-490f-a841-8533b21c9b6e)
 Call ID: 1decaccb-f542-490f-a841-8533b21c9b6e
  Args:
    source: John_Ulick_Knatchbull
    literal_value: 1924
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (9b3ae3bc-8fdc-481f-b74f-1234f9a6e41f)
 Call ID: 9b3ae3bc-8fdc-481f-b74f-1234f9a6e41f
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 2005
    source: John_Ulick_Knatchbull
  AssignClass (be52ae63-86a1-4c68-9f23-0868631fd985)
 Call ID: be52ae63-86a1-4c68-9f23-0868631fd985
  Args:
    source: Michael_Knatchbull
    type: :Man
  AssignClass (7497d0ac-0af5-49a9-9fe9-86ad076f54ce)
 Call ID: 7497d0ac-0af5-49a9-9fe9-86ad076f54ce
  Args:
    source: Michael_Knatchbull
    type: :Person
  AssignClass (481da48e-cf2f-4cf8-9578-98b81260174f)
 Call ID: 481da48e-cf2f-4cf8-9578-98b81260174f
  Args:
    source: Lady_Doreen_Browne
    type: :Woman
  AssignClass (dc81ddb8-e4f8-4cd7-ac5a-e9ab53ff58f9)
 Call ID: dc81ddb8-e4f8-4cd7-ac5a-e9ab53ff58f9
  Args:
    source: Lady_Doreen_Browne
    type: :Person
  AddTriple (aa958abb-f19c-4b0d-be7b-16c127843267)
 Call ID: aa958abb-f19c-4b0d-be7b-16c127843267
  Args:
    relation: :hasFather
    target: Michael_Knatchbull
    source: John_Ulick_Knatchbull
  AddTriple (ad953504-39e1-4368-8815-c668d24e996c)
 Call ID: ad953504-39e1-4368-8815-c668d24e996c
  Args:
    relation: :hasMother
    target: Lady_Doreen_Browne
    source: John_Ulick_Knatchbull
  AssignClass (424a93d7-00ff-4dac-806c-925c4d3c012e)
 Call ID: 424a93d7-00ff-4dac-806c-925c4d3c012e
  Args:
    type: :Woman
    source: Patricia_Mountbatten
  AssignClass (d557221e-c08c-48cd-8d72-a0169c76bde5)
 Call ID: d557221e-c08c-48cd-8d72-a0169c76bde5
  Args:
    source: Patricia_Mountbatten
    type: :Person
  AddLiteral (fce2a631-1d4c-42f8-b139-5723ae3d93dd)
 Call ID: fce2a631-1d4c-42f8-b139-5723ae3d93dd
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    source: John_Ulick_Knatchbull
    literal_value: 1946
  AddTriple (93803d25-77b4-4246-90c9-16726fd59234)
 Call ID: 93803d25-77b4-4246-90c9-16726fd59234
  Args:
    target: Patricia_Mountbatten
    relation: :hasRelation
    source: John_Ulick_Knatchbull
  AssignClass (0d0079e2-38f0-4272-95d3-8d7046bb379e)
 Call ID: 0d0079e2-38f0-4272-95d3-8d7046bb379e
  Args:
    source: Louis_Mountbatten
    type: :Man
  AssignClass (740e68e6-6f6d-4b71-bf22-849eadece51f)
 Call ID: 740e68e6-6f6d-4b71-bf22-849eadece51f
  Args:
    type: :Person
    source: Louis_Mountbatten
  AddTriple (4fabced2-3b49-40cb-bb14-5e204fc59333)
 Call ID: 4fabced2-3b49-40cb-bb14-5e204fc59333
  Args:
    target: Louis_Mountbatten
    relation: :hasFather
    source: Patricia_Mountbatten
  AssignClass (5864141a-1ae4-4a82-a427-79b78a845b35)
 Call ID: 5864141a-1ae4-4a82-a427-79b78a845b35
  Args:
    type: :Man
    source: Norton_Louis_Philip_Knatchbull
  AssignClass (5f12d81d-fca5-48bd-85f0-88344e4779dc)
 Call ID: 5f12d81d-fca5-48bd-85f0-88344e4779dc
  Args:
    type: :Person
    source: Norton_Louis_Philip_Knatchbull
  AddTriple (faee3d8e-4418-4d16-90a6-bd83ef42b953)
 Call ID: faee3d8e-4418-4d16-90a6-bd83ef42b953
  Args:
    source: John_Ulick_Knatchbull
    target: Norton_Louis_Philip_Knatchbull
    relation: :hasChild
  AddTriple (048bfda7-f7df-4c13-94b0-4bb382544d54)
 Call ID: 048bfda7-f7df-4c13-94b0-4bb382544d54
  Args:
    target: Norton_Louis_Philip_Knatchbull
    relation: :hasChild
    source: Patricia_Mountbatten
  AssignClass (565ed30e-7940-4c6b-b0bd-ca0b57fe2cd2)
 Call ID: 565ed30e-7940-4c6b-b0bd-ca0b57fe2cd2
  Args:
    type: :Woman
    source: Lady_Amanda_Patricia_Victoria_Knatchbull
  AssignClass (ff4fe9d3-6078-458d-8dbf-a7490f07f4ad)
 Call ID: ff4fe9d3-6078-458d-8dbf-a7490f07f4ad
  Args:
    source: Lady_Amanda_Patricia_Victoria_Knatchbull
    type: :Person
  AddTriple (ac70b384-d50c-48d2-92fd-eacf495c7380)
 Call ID: ac70b384-d50c-48d2-92fd-eacf495c7380
  Args:
    relation: :hasChild
    target: Lady_Amanda_Patricia_Victoria_Knatchbull
    source: John_Ulick_Knatchbull
  AddTriple (54eaea5a-1b6b-4242-81eb-566373f92a81)
 Call ID: 54eaea5a-1b6b-4242-81eb-566373f92a81
  Args:
    source: Patricia_Mountbatten
    target: Lady_Amanda_Patricia_Victoria_Knatchbull
    relation: :hasChild
  AssignClass (30c6587a-8d19-459f-bdc1-1144c1ef644f)
 Call ID: 30c6587a-8d19-459f-bdc1-1144c1ef644f
  Args:
    source: Nicholas_Timothy_Charles_Knatchbull
    type: :Man
  AssignClass (17971246-732c-48ef-90d1-a68fb8a4f72a)
 Call ID: 17971246-732c-48ef-90d1-a68fb8a4f72a
  Args:
    source: Nicholas_Timothy_Charles_Knatchbull
    type: :Person
  AddTriple (35d12d17-8217-4757-8d3d-dd39a639cc3e)
 Call ID: 35d12d17-8217-4757-8d3d-dd39a639cc3e
  Args:
    source: John_Ulick_Knatchbull
    target: Nicholas_Timothy_Charles_Knatchbull
    relation: :hasChild
  AddTriple (2b8ae60c-b53b-4a0c-86f9-beb7071ee69c)
 Call ID: 2b8ae60c-b53b-4a0c-86f9-beb7071ee69c
  Args:
    source: Patricia_Mountbatten
    relation: :hasChild
    target: Nicholas_Timothy_Charles_Knatchbull
  AssignClass (cba4d4c9-49ff-4505-89d0-40ac27d63793)
 Call ID: cba4d4c9-49ff-4505-89d0-40ac27d63793
  Args:
    source: Timothy_Knatchbull
    type: :Man
  AssignClass (ddcfce3a-a836-4214-8b27-1a2e1ffb3c92)
 Call ID: ddcfce3a-a836-4214-8b27-1a2e1ffb3c92
  Args:
    source: Timothy_Knatchbull
    type: :Person
  AddTriple (e93abd4f-f0bf-450e-a62a-a6629c88225d)
 Call ID: e93abd4f-f0bf-450e-a62a-a6629c88225d
  Args:
    relation: :hasChild
    target: Timothy_Knatchbull
    source: John_Ulick_Knatchbull
  AddTriple (124e4487-4ba6-489e-88e5-2d176d2a3ead)
 Call ID: 124e4487-4ba6-489e-88e5-2d176d2a3ead
  Args:
    source: Patricia_Mountbatten
    relation: :hasChild
    target: Timothy_Knatchbull
  AssignClass (f7d6f6a6-21de-4222-835e-e596db80637c)
 Call ID: f7d6f6a6-21de-4222-835e-e596db80637c
  Args:
    source: Louise_Mountbatten
    type: :Woman
  AssignClass (6b447025-840c-4021-9d19-bd83de2c8b82)
 Call ID: 6b447025-840c-4021-9d19-bd83de2c8b82
  Args:
    type: :Person
    source: Louise_Mountbatten
  AddTriple (e1fd023a-a859-4604-9e14-a12592d473a4)
 Call ID: e1fd023a-a859-4604-9e14-a12592d473a4
  Args:
    source: Louise_Mountbatten
    target: Louis_Mountbatten
    relation: :isSisterOf
  Finish (636746b9-7ebb-4a0b-a8a2-15d69db5a1eb)
 Call ID: 636746b9-7ebb-4a0b-a8a2-15d69db5a1eb
  Args: