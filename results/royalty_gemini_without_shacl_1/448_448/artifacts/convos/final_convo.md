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
  AssignClass (6601e46e-bcda-4891-b679-edc9b05d1f48)
 Call ID: 6601e46e-bcda-4891-b679-edc9b05d1f48
  Args:
    source: John_Ulick_Knatchbull
    type: :Man
  AssignClass (b3dbaf15-989a-49fd-8e4d-ea01f43915a3)
 Call ID: b3dbaf15-989a-49fd-8e4d-ea01f43915a3
  Args:
    source: John_Ulick_Knatchbull
    type: :Person
  AddLiteral (7556b6c7-256d-4aa1-952f-97677786bd43)
 Call ID: 7556b6c7-256d-4aa1-952f-97677786bd43
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: John_Ulick_Knatchbull
    literal_value: 1924
  AddLiteral (f4a06d63-e00c-4694-af89-03d2f91876ae)
 Call ID: f4a06d63-e00c-4694-af89-03d2f91876ae
  Args:
    literal_value: 2005
    source: John_Ulick_Knatchbull
    literal_type: xsd:integer
    relation: :hasDeathYear
  AddLiteral (ea40306e-6242-4032-82ef-8a1777259ce4)
 Call ID: ea40306e-6242-4032-82ef-8a1777259ce4
  Args:
    literal_type: xsd:string
    relation: :knownAs
    source: John_Ulick_Knatchbull
    literal_value: John Brabourne
  AssignClass (d048cbc8-634f-4652-a9b0-edea9befcfd1)
 Call ID: d048cbc8-634f-4652-a9b0-edea9befcfd1
  Args:
    type: :Man
    source: Michael_Knatchbull
  AssignClass (44d37a1c-1515-4c06-b0ba-2ac5a5376a80)
 Call ID: 44d37a1c-1515-4c06-b0ba-2ac5a5376a80
  Args:
    source: Michael_Knatchbull
    type: :Person
  AddTriple (f97918f2-f2a7-45b8-9f7d-26f35bc0591a)
 Call ID: f97918f2-f2a7-45b8-9f7d-26f35bc0591a
  Args:
    source: Michael_Knatchbull
    relation: :isFatherOf
    target: John_Ulick_Knatchbull
  AssignClass (eea5bd81-4840-400b-b4d9-74ddd53f43bf)
 Call ID: eea5bd81-4840-400b-b4d9-74ddd53f43bf
  Args:
    source: Lady_Doreen_Browne
    type: :Woman
  AssignClass (36b3fcc6-33fd-4633-9ec4-2a5a2fcaa095)
 Call ID: 36b3fcc6-33fd-4633-9ec4-2a5a2fcaa095
  Args:
    source: Lady_Doreen_Browne
    type: :Person
  AddTriple (263ecef8-404d-46a4-a2bc-2f947eb2af86)
 Call ID: 263ecef8-404d-46a4-a2bc-2f947eb2af86
  Args:
    source: Lady_Doreen_Browne
    target: John_Ulick_Knatchbull
    relation: :isMotherOf
  AssignClass (5b3665b5-5033-40e4-a618-ae10ea786a62)
 Call ID: 5b3665b5-5033-40e4-a618-ae10ea786a62
  Args:
    source: Patricia_Mountbatten
    type: :Woman
  AssignClass (5ba4adbe-0165-47e1-a022-81ac611e6f6e)
 Call ID: 5ba4adbe-0165-47e1-a022-81ac611e6f6e
  Args:
    source: Patricia_Mountbatten
    type: :Person
  AddLiteral (3b20748a-d59f-47fa-bcc1-1d2fe3ccfac0)
 Call ID: 3b20748a-d59f-47fa-bcc1-1d2fe3ccfac0
  Args:
    literal_value: 1946
    source: John_Ulick_Knatchbull
    relation: :hasMarriageYear
    literal_type: xsd:integer
  AddTriple (f96975f3-0279-450e-938e-7f6206fa73e8)
 Call ID: f96975f3-0279-450e-938e-7f6206fa73e8
  Args:
    source: John_Ulick_Knatchbull
    target: Patricia_Mountbatten
    relation: :hasRelation
  AssignClass (677985eb-26d3-47f2-8b51-f4bbc474c354)
 Call ID: 677985eb-26d3-47f2-8b51-f4bbc474c354
  Args:
    type: :Man
    source: Louis_Mountbatten
  AssignClass (626ef653-2d81-4f43-8df9-6687bf7a59f7)
 Call ID: 626ef653-2d81-4f43-8df9-6687bf7a59f7
  Args:
    type: :Person
    source: Louis_Mountbatten
  AddTriple (d5f16187-a023-4860-a10b-97a55c72d249)
 Call ID: d5f16187-a023-4860-a10b-97a55c72d249
  Args:
    target: Patricia_Mountbatten
    relation: :isFatherOf
    source: Louis_Mountbatten
  AssignClass (a98fbbc1-51bf-4294-9eb6-065b9e5524a8)
 Call ID: a98fbbc1-51bf-4294-9eb6-065b9e5524a8
  Args:
    source: Norton_Louis_Philip_Knatchbull
    type: :Man
  AssignClass (8f73eb57-4c01-49cc-a38e-109d68f8ece3)
 Call ID: 8f73eb57-4c01-49cc-a38e-109d68f8ece3
  Args:
    type: :Person
    source: Norton_Louis_Philip_Knatchbull
  AddTriple (4c3e9f93-6bef-4144-987f-1bdae85dae80)
 Call ID: 4c3e9f93-6bef-4144-987f-1bdae85dae80
  Args:
    target: John_Ulick_Knatchbull
    relation: :isSonOf
    source: Norton_Louis_Philip_Knatchbull
  AddTriple (f3a886cd-e5cb-446e-b202-e014f60d5491)
 Call ID: f3a886cd-e5cb-446e-b202-e014f60d5491
  Args:
    source: Norton_Louis_Philip_Knatchbull
    relation: :isSonOf
    target: Patricia_Mountbatten
  AssignClass (a0cfbcf5-56c2-4c0f-878d-ad88a9b83c08)
 Call ID: a0cfbcf5-56c2-4c0f-878d-ad88a9b83c08
  Args:
    type: :Woman
    source: Lady_Amanda_Patricia_Victoria_Knatchbull
  AssignClass (4f391f17-72bc-44d2-8a9c-90ba5f316b5d)
 Call ID: 4f391f17-72bc-44d2-8a9c-90ba5f316b5d
  Args:
    source: Lady_Amanda_Patricia_Victoria_Knatchbull
    type: :Person
  AddTriple (77bf156d-4641-40b0-95b2-1470dc146282)
 Call ID: 77bf156d-4641-40b0-95b2-1470dc146282
  Args:
    target: John_Ulick_Knatchbull
    relation: :isDaughterOf
    source: Lady_Amanda_Patricia_Victoria_Knatchbull
  AddTriple (f6dd9789-28a7-4bd4-8599-b502aeb96182)
 Call ID: f6dd9789-28a7-4bd4-8599-b502aeb96182
  Args:
    source: Lady_Amanda_Patricia_Victoria_Knatchbull
    relation: :isDaughterOf
    target: Patricia_Mountbatten
  AssignClass (20d3a952-caa3-40f8-9a57-2dd79d5ce528)
 Call ID: 20d3a952-caa3-40f8-9a57-2dd79d5ce528
  Args:
    type: :Man
    source: Nicholas_Timothy_Charles_Knatchbull
  AssignClass (6b3d2876-062a-4f1a-b84b-b02263e51687)
 Call ID: 6b3d2876-062a-4f1a-b84b-b02263e51687
  Args:
    type: :Person
    source: Nicholas_Timothy_Charles_Knatchbull
  AddTriple (9fa0ebfa-e019-4b42-968d-7e41779a3765)
 Call ID: 9fa0ebfa-e019-4b42-968d-7e41779a3765
  Args:
    relation: :isSonOf
    target: John_Ulick_Knatchbull
    source: Nicholas_Timothy_Charles_Knatchbull
  AddTriple (12a17786-8db3-4077-997d-a36bf0dae69d)
 Call ID: 12a17786-8db3-4077-997d-a36bf0dae69d
  Args:
    target: Patricia_Mountbatten
    relation: :isSonOf
    source: Nicholas_Timothy_Charles_Knatchbull
  AssignClass (aa946ab4-f23e-41cf-bcae-706636e0870e)
 Call ID: aa946ab4-f23e-41cf-bcae-706636e0870e
  Args:
    source: Timothy_Knatchbull
    type: :Man
  AssignClass (68f65770-dd32-48c9-98a4-be41a97d5b5f)
 Call ID: 68f65770-dd32-48c9-98a4-be41a97d5b5f
  Args:
    source: Timothy_Knatchbull
    type: :Person
  AddTriple (a72aa58b-2477-4e48-8979-b6ffd09b8b33)
 Call ID: a72aa58b-2477-4e48-8979-b6ffd09b8b33
  Args:
    relation: :isSonOf
    target: John_Ulick_Knatchbull
    source: Timothy_Knatchbull
  AddTriple (8b15f74a-114d-4bbd-8681-415bfd76e2ea)
 Call ID: 8b15f74a-114d-4bbd-8681-415bfd76e2ea
  Args:
    source: Timothy_Knatchbull
    target: Patricia_Mountbatten
    relation: :isSonOf
  AssignClass (7e40c569-0dca-4aa5-9d12-074bf6e03f76)
 Call ID: 7e40c569-0dca-4aa5-9d12-074bf6e03f76
  Args:
    source: Louise_Mountbatten
    type: :Woman
  AssignClass (a450115f-b640-4e37-bb02-a8f03c200d01)
 Call ID: a450115f-b640-4e37-bb02-a8f03c200d01
  Args:
    source: Louise_Mountbatten
    type: :Person
  AddTriple (18f0f448-2806-413c-ba3c-4d87d61df03c)
 Call ID: 18f0f448-2806-413c-ba3c-4d87d61df03c
  Args:
    source: Louise_Mountbatten
    target: Patricia_Mountbatten
    relation: :isAuntOf
  Finish (26441e4e-9628-420a-980a-4607d8ef840d)
 Call ID: 26441e4e-9628-420a-980a-4607d8ef840d
  Args: