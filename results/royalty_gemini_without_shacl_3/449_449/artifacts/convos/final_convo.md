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
  AssignClass (682b859c-fc63-469a-8bd3-8a8f52baadb0)
 Call ID: 682b859c-fc63-469a-8bd3-8a8f52baadb0
  Args:
    type: :Man
    source: :John_Ulick_Knatchbull
  AssignClass (32b83289-3d14-4ba1-a82b-643bada7f091)
 Call ID: 32b83289-3d14-4ba1-a82b-643bada7f091
  Args:
    type: :Person
    source: :John_Ulick_Knatchbull
  AddLiteral (620172c9-5770-447e-8a04-d106ede5e803)
 Call ID: 620172c9-5770-447e-8a04-d106ede5e803
  Args:
    relation: :hasBirthYear
    literal_value: 1924
    literal_type: xsd:integer
    source: :John_Ulick_Knatchbull
  AddLiteral (3ae7c68b-04b8-426d-b7c0-4e9f0675df01)
 Call ID: 3ae7c68b-04b8-426d-b7c0-4e9f0675df01
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 2005
    source: :John_Ulick_Knatchbull
  AddLiteral (9aeb1c97-4f7e-48d9-aff2-820df491f17d)
 Call ID: 9aeb1c97-4f7e-48d9-aff2-820df491f17d
  Args:
    source: :John_Ulick_Knatchbull
    literal_type: xsd:string
    literal_value: John Brabourne
    relation: :knownAs
  AssignClass (1d3e14e6-6c49-4fd0-bd50-0bfc7aa6044d)
 Call ID: 1d3e14e6-6c49-4fd0-bd50-0bfc7aa6044d
  Args:
    type: :Man
    source: :Michael_Knatchbull
  AssignClass (10dd0cb8-1884-4667-abef-8a4b9a79b497)
 Call ID: 10dd0cb8-1884-4667-abef-8a4b9a79b497
  Args:
    type: :Person
    source: :Michael_Knatchbull
  AddTriple (a8509da4-5960-4257-981a-29da4d37efe1)
 Call ID: a8509da4-5960-4257-981a-29da4d37efe1
  Args:
    source: :Michael_Knatchbull
    relation: :isFatherOf
    target: :John_Ulick_Knatchbull
  AssignClass (5ccba66d-3dee-488c-ad8c-31d4501808b9)
 Call ID: 5ccba66d-3dee-488c-ad8c-31d4501808b9
  Args:
    type: :Woman
    source: :Lady_Doreen_Browne
  AssignClass (ee02ef79-c4bf-4e78-a076-b3aa2c198cd7)
 Call ID: ee02ef79-c4bf-4e78-a076-b3aa2c198cd7
  Args:
    type: :Person
    source: :Lady_Doreen_Browne
  AddTriple (3112d50b-c5a7-48bf-9419-6a20a8b5597d)
 Call ID: 3112d50b-c5a7-48bf-9419-6a20a8b5597d
  Args:
    source: :Lady_Doreen_Browne
    target: :John_Ulick_Knatchbull
    relation: :isMotherOf
  AssignClass (5449107e-fc4e-4974-889d-d6bc351498ec)
 Call ID: 5449107e-fc4e-4974-889d-d6bc351498ec
  Args:
    type: :Woman
    source: :Patricia_Mountbatten
  AssignClass (ed6119e4-fb8a-4ce1-973f-426b88401c24)
 Call ID: ed6119e4-fb8a-4ce1-973f-426b88401c24
  Args:
    type: :Person
    source: :Patricia_Mountbatten
  AddLiteral (5e88004c-40b4-48b1-8e75-b6fbdf6cfbe6)
 Call ID: 5e88004c-40b4-48b1-8e75-b6fbdf6cfbe6
  Args:
    relation: :hasMarriageYear
    source: :John_Ulick_Knatchbull
    literal_type: xsd:integer
    literal_value: 1946
  AddTriple (a6697fc1-d025-464c-9f73-276f6999a5e9)
 Call ID: a6697fc1-d025-464c-9f73-276f6999a5e9
  Args:
    target: :Patricia_Mountbatten
    relation: :hasRelation
    source: :John_Ulick_Knatchbull
  AssignClass (801dbead-55b6-4906-bbf8-35258a630004)
 Call ID: 801dbead-55b6-4906-bbf8-35258a630004
  Args:
    type: :Man
    source: :Louis_Mountbatten
  AssignClass (23912a85-deda-4db8-95a3-33b80bdcdf60)
 Call ID: 23912a85-deda-4db8-95a3-33b80bdcdf60
  Args:
    type: :Person
    source: :Louis_Mountbatten
  AddTriple (e2b96a88-290f-4c7d-904c-816870a52688)
 Call ID: e2b96a88-290f-4c7d-904c-816870a52688
  Args:
    target: :Patricia_Mountbatten
    relation: :isFatherOf
    source: :Louis_Mountbatten
  AssignClass (1c54e4ad-37a0-4d4b-9093-d849b0de41d3)
 Call ID: 1c54e4ad-37a0-4d4b-9093-d849b0de41d3
  Args:
    type: :Man
    source: :Norton_Louis_Philip_Knatchbull
  AssignClass (1ad0fef1-7389-4775-bd49-498b87adcee6)
 Call ID: 1ad0fef1-7389-4775-bd49-498b87adcee6
  Args:
    type: :Person
    source: :Norton_Louis_Philip_Knatchbull
  AddTriple (a596a12a-6717-4839-a70f-c8884255b7b5)
 Call ID: a596a12a-6717-4839-a70f-c8884255b7b5
  Args:
    target: :John_Ulick_Knatchbull
    relation: :isSonOf
    source: :Norton_Louis_Philip_Knatchbull
  AddTriple (986392e8-00ca-4a07-94e5-e92167026f42)
 Call ID: 986392e8-00ca-4a07-94e5-e92167026f42
  Args:
    source: :Norton_Louis_Philip_Knatchbull
    relation: :isSonOf
    target: :Patricia_Mountbatten
  AddLiteral (7c518a22-114d-4363-9ded-ceb3972e82ab)
 Call ID: 7c518a22-114d-4363-9ded-ceb3972e82ab
  Args:
    source: :Norton_Louis_Philip_Knatchbull
    literal_type: xsd:integer
    literal_value: 1947
    relation: :hasBirthYear
  AssignClass (6330c77a-43db-41b3-ba96-24833a2ba75a)
 Call ID: 6330c77a-43db-41b3-ba96-24833a2ba75a
  Args:
    type: :Woman
    source: :Lady_Amanda_Patricia_Victoria_Knatchbull
  AssignClass (0b0f35b8-46b2-4a32-8dfe-d8c7983fd024)
 Call ID: 0b0f35b8-46b2-4a32-8dfe-d8c7983fd024
  Args:
    type: :Person
    source: :Lady_Amanda_Patricia_Victoria_Knatchbull
  AddTriple (77cef9cd-1f13-4746-bb1a-4aacb88dabe8)
 Call ID: 77cef9cd-1f13-4746-bb1a-4aacb88dabe8
  Args:
    source: :Lady_Amanda_Patricia_Victoria_Knatchbull
    relation: :isDaughterOf
    target: :John_Ulick_Knatchbull
  AddTriple (718a774b-b4ac-4250-8520-dd44b918c8d5)
 Call ID: 718a774b-b4ac-4250-8520-dd44b918c8d5
  Args:
    source: :Lady_Amanda_Patricia_Victoria_Knatchbull
    relation: :isDaughterOf
    target: :Patricia_Mountbatten
  AddLiteral (126c48a8-ae56-48ca-9f82-8827fcc1ccca)
 Call ID: 126c48a8-ae56-48ca-9f82-8827fcc1ccca
  Args:
    relation: :hasBirthYear
    source: :Lady_Amanda_Patricia_Victoria_Knatchbull
    literal_value: 1957
    literal_type: xsd:integer
  AssignClass (3c7499b5-07d7-4e32-9264-b2f363833f88)
 Call ID: 3c7499b5-07d7-4e32-9264-b2f363833f88
  Args:
    type: :Man
    source: :Nicholas_Timothy_Charles_Knatchbull
  AssignClass (9804a074-c521-4bc8-80a3-8257ae820162)
 Call ID: 9804a074-c521-4bc8-80a3-8257ae820162
  Args:
    type: :Person
    source: :Nicholas_Timothy_Charles_Knatchbull
  AddTriple (9b5f9e1e-4493-4ca3-ad1b-d6032e683c77)
 Call ID: 9b5f9e1e-4493-4ca3-ad1b-d6032e683c77
  Args:
    source: :Nicholas_Timothy_Charles_Knatchbull
    target: :John_Ulick_Knatchbull
    relation: :isSonOf
  AddTriple (bf6aa9c7-df53-45cc-9988-1f1a26db1c2f)
 Call ID: bf6aa9c7-df53-45cc-9988-1f1a26db1c2f
  Args:
    target: :Patricia_Mountbatten
    relation: :isSonOf
    source: :Nicholas_Timothy_Charles_Knatchbull
  AssignClass (848e10bf-4155-488d-8949-2675324e9b47)
 Call ID: 848e10bf-4155-488d-8949-2675324e9b47
  Args:
    type: :Man
    source: :Timothy_Knatchbull
  AssignClass (1352ceb4-8433-4617-a44b-c3042578a845)
 Call ID: 1352ceb4-8433-4617-a44b-c3042578a845
  Args:
    type: :Person
    source: :Timothy_Knatchbull
  AddTriple (fa41183b-d95e-4807-bf70-d41cf18e5820)
 Call ID: fa41183b-d95e-4807-bf70-d41cf18e5820
  Args:
    source: :Timothy_Knatchbull
    target: :John_Ulick_Knatchbull
    relation: :isSonOf
  AddTriple (6cc57491-fba4-4320-84fe-05e17d48bdcb)
 Call ID: 6cc57491-fba4-4320-84fe-05e17d48bdcb
  Args:
    target: :Patricia_Mountbatten
    relation: :isSonOf
    source: :Timothy_Knatchbull
  AssignClass (f32a7fda-d92f-4e83-9750-c796a76752cb)
 Call ID: f32a7fda-d92f-4e83-9750-c796a76752cb
  Args:
    type: :Woman
    source: :Louise_Mountbatten
  AssignClass (d78bbd0b-1997-403e-9973-c74322fceaf4)
 Call ID: d78bbd0b-1997-403e-9973-c74322fceaf4
  Args:
    type: :Person
    source: :Louise_Mountbatten
  AddTriple (6d67a66b-2fcc-4a15-9606-df44bc3313c7)
 Call ID: 6d67a66b-2fcc-4a15-9606-df44bc3313c7
  Args:
    source: :Louise_Mountbatten
    target: :Patricia_Mountbatten
    relation: :isSisterOf
  Finish (3656a0e2-0c7f-42f0-9083-9aaa70915163)
 Call ID: 3656a0e2-0c7f-42f0-9083-9aaa70915163
  Args: