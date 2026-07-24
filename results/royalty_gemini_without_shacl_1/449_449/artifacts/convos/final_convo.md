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
  AssignClass (530d7e60-8a7b-47d2-83f7-d757b2136541)
 Call ID: 530d7e60-8a7b-47d2-83f7-d757b2136541
  Args:
    source: John_Ulick_Knatchbull
    type: :Person
  AssignClass (8a595f9d-232e-46d5-852f-5b399e9f0007)
 Call ID: 8a595f9d-232e-46d5-852f-5b399e9f0007
  Args:
    source: John_Ulick_Knatchbull
    type: :Man
  AddLiteral (a72f7e99-6f94-4636-8c8b-9939272626d9)
 Call ID: a72f7e99-6f94-4636-8c8b-9939272626d9
  Args:
    literal_type: xsd:integer
    literal_value: 1924
    relation: :hasBirthYear
    source: John_Ulick_Knatchbull
  AddLiteral (f2cdce98-4eb6-4abc-a2af-9f0f5b293225)
 Call ID: f2cdce98-4eb6-4abc-a2af-9f0f5b293225
  Args:
    literal_value: 2005
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: John_Ulick_Knatchbull
  AddLiteral (ee2bb4bc-c261-402e-ae90-db6c60ddfd44)
 Call ID: ee2bb4bc-c261-402e-ae90-db6c60ddfd44
  Args:
    source: John_Ulick_Knatchbull
    relation: :knownAs
    literal_type: xsd:string
    literal_value: John Brabourne
  AssignClass (e982af08-cea7-4f47-868c-b1a3eaf4196f)
 Call ID: e982af08-cea7-4f47-868c-b1a3eaf4196f
  Args:
    source: Michael_Knatchbull
    type: :Person
  AssignClass (104a7fd3-e605-434d-b8a2-705e7e089341)
 Call ID: 104a7fd3-e605-434d-b8a2-705e7e089341
  Args:
    type: :Man
    source: Michael_Knatchbull
  AssignClass (bb8dba18-06a4-4938-b825-99b038f8c8c4)
 Call ID: bb8dba18-06a4-4938-b825-99b038f8c8c4
  Args:
    type: :Person
    source: Lady_Doreen_Browne
  AssignClass (778b9d94-dd55-4dca-9b32-47700ccfa36f)
 Call ID: 778b9d94-dd55-4dca-9b32-47700ccfa36f
  Args:
    type: :Woman
    source: Lady_Doreen_Browne
  AddTriple (807f1713-2563-41fc-a99a-067bd0000124)
 Call ID: 807f1713-2563-41fc-a99a-067bd0000124
  Args:
    source: John_Ulick_Knatchbull
    target: Michael_Knatchbull
    relation: :hasFather
  AddTriple (2e98fb65-8610-441d-83e5-62d5016cb40b)
 Call ID: 2e98fb65-8610-441d-83e5-62d5016cb40b
  Args:
    relation: :hasMother
    target: Lady_Doreen_Browne
    source: John_Ulick_Knatchbull
  AssignClass (a3363a9c-2564-4e9b-a690-9e865ab29c6e)
 Call ID: a3363a9c-2564-4e9b-a690-9e865ab29c6e
  Args:
    type: :Person
    source: Patricia_Mountbatten
  AssignClass (609fc164-d7b9-4516-a6d2-9aa9b4bec1be)
 Call ID: 609fc164-d7b9-4516-a6d2-9aa9b4bec1be
  Args:
    type: :Woman
    source: Patricia_Mountbatten
  AddTriple (6b9cefb8-0033-4097-9d7f-795824b4f289)
 Call ID: 6b9cefb8-0033-4097-9d7f-795824b4f289
  Args:
    source: John_Ulick_Knatchbull
    target: Patricia_Mountbatten
    relation: :hasRelation
  AddLiteral (aa603440-54fe-4d90-91d6-8344169911eb)
 Call ID: aa603440-54fe-4d90-91d6-8344169911eb
  Args:
    relation: :hasMarriageYear
    source: John_Ulick_Knatchbull
    literal_type: xsd:integer
    literal_value: 1946
  AssignClass (00aedd82-5df4-47d6-85d1-cf62f2f21cd6)
 Call ID: 00aedd82-5df4-47d6-85d1-cf62f2f21cd6
  Args:
    type: :Person
    source: Louis_Mountbatten
  AssignClass (b4ffe1a0-7974-4541-ba70-9ad5ba8606f4)
 Call ID: b4ffe1a0-7974-4541-ba70-9ad5ba8606f4
  Args:
    type: :Man
    source: Louis_Mountbatten
  AddTriple (c30440af-19d0-41b6-88c7-4b077f0d3733)
 Call ID: c30440af-19d0-41b6-88c7-4b077f0d3733
  Args:
    source: Patricia_Mountbatten
    relation: :isDaughterOf
    target: Louis_Mountbatten
  AssignClass (bfe9c395-a81f-489d-9f2b-83ea72bbfdbd)
 Call ID: bfe9c395-a81f-489d-9f2b-83ea72bbfdbd
  Args:
    source: Norton_Louis_Philip_Knatchbull
    type: :Person
  AssignClass (ed31bf8c-2ebd-43c6-aff0-fb1b4e61849a)
 Call ID: ed31bf8c-2ebd-43c6-aff0-fb1b4e61849a
  Args:
    source: Norton_Louis_Philip_Knatchbull
    type: :Man
  AddTriple (37b43c6d-e477-4ce9-82c8-45918439e7c9)
 Call ID: 37b43c6d-e477-4ce9-82c8-45918439e7c9
  Args:
    target: John_Ulick_Knatchbull
    relation: :isSonOf
    source: Norton_Louis_Philip_Knatchbull
  AddTriple (709660a3-d0ce-4051-b4ff-905a85904eff)
 Call ID: 709660a3-d0ce-4051-b4ff-905a85904eff
  Args:
    relation: :isSonOf
    target: Patricia_Mountbatten
    source: Norton_Louis_Philip_Knatchbull
  AssignClass (a7236eab-fbc2-4c66-9938-4dbafb744bbb)
 Call ID: a7236eab-fbc2-4c66-9938-4dbafb744bbb
  Args:
    source: Lady_Amanda_Patricia_Victoria_Knatchbull
    type: :Person
  AssignClass (b07aa036-a94b-424e-9431-4af0ecb36505)
 Call ID: b07aa036-a94b-424e-9431-4af0ecb36505
  Args:
    type: :Woman
    source: Lady_Amanda_Patricia_Victoria_Knatchbull
  AddTriple (389319ac-88e6-49b4-9cb7-06cc1c009d3a)
 Call ID: 389319ac-88e6-49b4-9cb7-06cc1c009d3a
  Args:
    target: John_Ulick_Knatchbull
    relation: :isDaughterOf
    source: Lady_Amanda_Patricia_Victoria_Knatchbull
  AddTriple (1a388d11-98eb-4a8e-9121-bdd21bd87239)
 Call ID: 1a388d11-98eb-4a8e-9121-bdd21bd87239
  Args:
    source: Lady_Amanda_Patricia_Victoria_Knatchbull
    relation: :isDaughterOf
    target: Patricia_Mountbatten
  AssignClass (a4dbf65a-8ebf-4d22-9c6a-187a227d93d1)
 Call ID: a4dbf65a-8ebf-4d22-9c6a-187a227d93d1
  Args:
    source: Nicholas_Timothy_Charles_Knatchbull
    type: :Person
  AssignClass (3640b228-d636-4a71-bb97-48bd2a0d4003)
 Call ID: 3640b228-d636-4a71-bb97-48bd2a0d4003
  Args:
    source: Nicholas_Timothy_Charles_Knatchbull
    type: :Man
  AddTriple (1dbafd02-4b22-49ab-8684-df5e22fad703)
 Call ID: 1dbafd02-4b22-49ab-8684-df5e22fad703
  Args:
    source: Nicholas_Timothy_Charles_Knatchbull
    target: John_Ulick_Knatchbull
    relation: :isSonOf
  AddTriple (a2ab49cb-fba7-4867-a70d-5b0939ad65c4)
 Call ID: a2ab49cb-fba7-4867-a70d-5b0939ad65c4
  Args:
    source: Nicholas_Timothy_Charles_Knatchbull
    relation: :isSonOf
    target: Patricia_Mountbatten
  AssignClass (43ab0fa8-89b2-4461-a29a-f602d07177a2)
 Call ID: 43ab0fa8-89b2-4461-a29a-f602d07177a2
  Args:
    source: Timothy_Knatchbull
    type: :Person
  AssignClass (4a54bfa7-a09c-4156-8f89-a381f0b826e9)
 Call ID: 4a54bfa7-a09c-4156-8f89-a381f0b826e9
  Args:
    source: Timothy_Knatchbull
    type: :Man
  AddTriple (b7cc1fb0-dfe2-4e4b-b3b0-ee4adcdbe0f2)
 Call ID: b7cc1fb0-dfe2-4e4b-b3b0-ee4adcdbe0f2
  Args:
    source: Timothy_Knatchbull
    relation: :isSonOf
    target: John_Ulick_Knatchbull
  AddTriple (c01378a4-3a70-43b4-a6b5-3ea22645164d)
 Call ID: c01378a4-3a70-43b4-a6b5-3ea22645164d
  Args:
    source: Timothy_Knatchbull
    relation: :isSonOf
    target: Patricia_Mountbatten
  AssignClass (bc2a8918-9641-433e-a596-f33c988f869d)
 Call ID: bc2a8918-9641-433e-a596-f33c988f869d
  Args:
    type: :Person
    source: Louise_Mountbatten
  AssignClass (5ffbde27-e043-45c6-92bc-481a83e54a80)
 Call ID: 5ffbde27-e043-45c6-92bc-481a83e54a80
  Args:
    source: Louise_Mountbatten
    type: :Woman
  AddTriple (da3d767d-014b-4f01-8d55-6550d5429a28)
 Call ID: da3d767d-014b-4f01-8d55-6550d5429a28
  Args:
    relation: :isSisterOf
    target: Louis_Mountbatten
    source: Louise_Mountbatten
  Finish (b936a478-0dc7-45fe-86c9-881b36870b0e)
 Call ID: b936a478-0dc7-45fe-86c9-881b36870b0e
  Args: