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
  AssignClass (411eb115-1c9e-4b8c-88b9-d9fbad4c95f4)
 Call ID: 411eb115-1c9e-4b8c-88b9-d9fbad4c95f4
  Args:
    source: John_Ulick_Knatchbull
    type: :Man
  AssignClass (9833f2f9-a480-4f98-991a-1221b137fe9a)
 Call ID: 9833f2f9-a480-4f98-991a-1221b137fe9a
  Args:
    source: John_Ulick_Knatchbull
    type: :Person
  AddLiteral (b023ef13-4f7e-4e03-8b43-0ce33a4c82fe)
 Call ID: b023ef13-4f7e-4e03-8b43-0ce33a4c82fe
  Args:
    literal_type: xsd:integer
    literal_value: 1924
    source: John_Ulick_Knatchbull
    relation: :hasBirthYear
  AddLiteral (f0de394a-9bf1-48bf-abc8-7cc786bf9f66)
 Call ID: f0de394a-9bf1-48bf-abc8-7cc786bf9f66
  Args:
    source: John_Ulick_Knatchbull
    literal_value: 2005
    relation: :hasDeathYear
    literal_type: xsd:integer
  AddLiteral (1fd5bfad-7418-4b98-91d4-2b9da833e3e5)
 Call ID: 1fd5bfad-7418-4b98-91d4-2b9da833e3e5
  Args:
    literal_type: xsd:string
    relation: :knownAs
    source: John_Ulick_Knatchbull
    literal_value: John Brabourne
  AssignClass (e3909f13-a0d7-47de-ab2c-e46d2e894c81)
 Call ID: e3909f13-a0d7-47de-ab2c-e46d2e894c81
  Args:
    source: Michael_Knatchbull
    type: :Man
  AssignClass (6f63166e-a326-49cc-ae7d-e35ba83e8a1e)
 Call ID: 6f63166e-a326-49cc-ae7d-e35ba83e8a1e
  Args:
    source: Michael_Knatchbull
    type: :Person
  AddTriple (49c84f00-7df0-4fdc-820c-bdfa2dd82062)
 Call ID: 49c84f00-7df0-4fdc-820c-bdfa2dd82062
  Args:
    relation: :hasFather
    source: John_Ulick_Knatchbull
    target: Michael_Knatchbull
  AssignClass (ec7056f8-0447-4792-b84b-230ea7c05b70)
 Call ID: ec7056f8-0447-4792-b84b-230ea7c05b70
  Args:
    source: Lady_Doreen_Browne
    type: :Woman
  AssignClass (1a88ac5d-0388-4e6a-ac69-9093c7dec361)
 Call ID: 1a88ac5d-0388-4e6a-ac69-9093c7dec361
  Args:
    source: Lady_Doreen_Browne
    type: :Person
  AddTriple (32dfa5d1-71c8-4ddc-8fd6-2bc0a8385614)
 Call ID: 32dfa5d1-71c8-4ddc-8fd6-2bc0a8385614
  Args:
    relation: :hasMother
    target: Lady_Doreen_Browne
    source: John_Ulick_Knatchbull
  AssignClass (b1909b9a-5251-4f5d-bdf2-6119e87b1914)
 Call ID: b1909b9a-5251-4f5d-bdf2-6119e87b1914
  Args:
    source: Patricia_Mountbatten
    type: :Woman
  AssignClass (68938429-2acc-474a-8053-93f3bb203ed2)
 Call ID: 68938429-2acc-474a-8053-93f3bb203ed2
  Args:
    source: Patricia_Mountbatten
    type: :Person
  AddTriple (44644f61-0022-4b50-8888-60bd8e6332e2)
 Call ID: 44644f61-0022-4b50-8888-60bd8e6332e2
  Args:
    source: John_Ulick_Knatchbull
    target: Patricia_Mountbatten
    relation: :hasRelation
  AddLiteral (80c935a5-ae49-4c0d-aa91-b0427dfd95c0)
 Call ID: 80c935a5-ae49-4c0d-aa91-b0427dfd95c0
  Args:
    relation: :hasMarriageYear
    source: John_Ulick_Knatchbull
    literal_value: 1946
    literal_type: xsd:integer
  AssignClass (9fd8edee-7c5d-439f-a83e-cd89d623977d)
 Call ID: 9fd8edee-7c5d-439f-a83e-cd89d623977d
  Args:
    source: Louis_Mountbatten
    type: :Man
  AssignClass (d931418a-0003-4b28-a4e9-6327c57b8429)
 Call ID: d931418a-0003-4b28-a4e9-6327c57b8429
  Args:
    source: Louis_Mountbatten
    type: :Person
  AddTriple (108bf423-e354-48b3-8b53-16305e18eaf9)
 Call ID: 108bf423-e354-48b3-8b53-16305e18eaf9
  Args:
    relation: :hasFather
    source: Patricia_Mountbatten
    target: Louis_Mountbatten
  AssignClass (6883aba6-778e-47af-8d02-735c7e817651)
 Call ID: 6883aba6-778e-47af-8d02-735c7e817651
  Args:
    source: Norton_Louis_Philip_Knatchbull
    type: :Man
  AssignClass (ac28910e-1932-4ff8-8e11-062663e4b663)
 Call ID: ac28910e-1932-4ff8-8e11-062663e4b663
  Args:
    source: Norton_Louis_Philip_Knatchbull
    type: :Person
  AddTriple (d504f492-97b2-42c4-91de-06b4617fbd51)
 Call ID: d504f492-97b2-42c4-91de-06b4617fbd51
  Args:
    relation: :isSonOf
    source: Norton_Louis_Philip_Knatchbull
    target: John_Ulick_Knatchbull
  AddTriple (c531ac72-1c76-4dbe-964c-da6b9784100c)
 Call ID: c531ac72-1c76-4dbe-964c-da6b9784100c
  Args:
    source: Norton_Louis_Philip_Knatchbull
    target: Patricia_Mountbatten
    relation: :isSonOf
  AssignClass (3358491f-17eb-4657-8335-2fdd83f3cb53)
 Call ID: 3358491f-17eb-4657-8335-2fdd83f3cb53
  Args:
    source: Lady_Amanda_Patricia_Victoria_Knatchbull
    type: :Woman
  AssignClass (2bc93654-434c-4f86-8654-7b754dc5354a)
 Call ID: 2bc93654-434c-4f86-8654-7b754dc5354a
  Args:
    source: Lady_Amanda_Patricia_Victoria_Knatchbull
    type: :Person
  AddTriple (39c1feff-01b8-47e0-9309-dddf149ad11f)
 Call ID: 39c1feff-01b8-47e0-9309-dddf149ad11f
  Args:
    source: Lady_Amanda_Patricia_Victoria_Knatchbull
    target: John_Ulick_Knatchbull
    relation: :isDaughterOf
  AddTriple (b82ae595-5d11-4670-a702-b3c5962ea9d8)
 Call ID: b82ae595-5d11-4670-a702-b3c5962ea9d8
  Args:
    source: Lady_Amanda_Patricia_Victoria_Knatchbull
    target: Patricia_Mountbatten
    relation: :isDaughterOf
  AssignClass (ce6e2bec-26b0-4adc-9e7d-2249f4c4361d)
 Call ID: ce6e2bec-26b0-4adc-9e7d-2249f4c4361d
  Args:
    source: Nicholas_Timothy_Charles_Knatchbull
    type: :Man
  AssignClass (eb29454e-03ad-4551-bcab-ab48c8baf98a)
 Call ID: eb29454e-03ad-4551-bcab-ab48c8baf98a
  Args:
    source: Nicholas_Timothy_Charles_Knatchbull
    type: :Person
  AddTriple (e37ba99a-55cc-41f7-a695-a64674ff34a2)
 Call ID: e37ba99a-55cc-41f7-a695-a64674ff34a2
  Args:
    relation: :isSonOf
    source: Nicholas_Timothy_Charles_Knatchbull
    target: John_Ulick_Knatchbull
  AddTriple (3f73fe17-0f03-4306-8b4d-85d5c2fdd177)
 Call ID: 3f73fe17-0f03-4306-8b4d-85d5c2fdd177
  Args:
    source: Nicholas_Timothy_Charles_Knatchbull
    target: Patricia_Mountbatten
    relation: :isSonOf
  AssignClass (9bad70d9-73dc-4306-9adf-a2f5ebf822cd)
 Call ID: 9bad70d9-73dc-4306-9adf-a2f5ebf822cd
  Args:
    source: Timothy_Knatchbull
    type: :Man
  AssignClass (856c3ff4-f49c-45ee-b96e-0ce31768bbb2)
 Call ID: 856c3ff4-f49c-45ee-b96e-0ce31768bbb2
  Args:
    source: Timothy_Knatchbull
    type: :Person
  AddTriple (fd0b657b-8551-4dbe-bb06-f98a395c4be5)
 Call ID: fd0b657b-8551-4dbe-bb06-f98a395c4be5
  Args:
    relation: :isSonOf
    target: John_Ulick_Knatchbull
    source: Timothy_Knatchbull
  AddTriple (8fe555f1-0b7f-4a52-a531-e8abcf78f01b)
 Call ID: 8fe555f1-0b7f-4a52-a531-e8abcf78f01b
  Args:
    relation: :isSonOf
    source: Timothy_Knatchbull
    target: Patricia_Mountbatten
  AssignClass (de09d763-195a-417b-96f6-d60e1a34a547)
 Call ID: de09d763-195a-417b-96f6-d60e1a34a547
  Args:
    source: Louise_Mountbatten
    type: :Woman
  AssignClass (c0b71545-da13-40b8-8a2e-9b1b5f7d324b)
 Call ID: c0b71545-da13-40b8-8a2e-9b1b5f7d324b
  Args:
    source: Louise_Mountbatten
    type: :Person
  AddTriple (f175399a-88e7-4b53-80c4-bc7f1cc6744e)
 Call ID: f175399a-88e7-4b53-80c4-bc7f1cc6744e
  Args:
    target: Patricia_Mountbatten
    source: Louise_Mountbatten
    relation: :isAuntOf
  Finish (b10fc58d-4fd0-4ab6-a1f2-990215de510a)
 Call ID: b10fc58d-4fd0-4ab6-a1f2-990215de510a
  Args: