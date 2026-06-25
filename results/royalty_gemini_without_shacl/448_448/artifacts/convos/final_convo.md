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
  AssignClass (ca651b69-2206-4119-bee5-9de85756e352)
 Call ID: ca651b69-2206-4119-bee5-9de85756e352
  Args:
    source: John_Ulick_Knatchbull
    type: :Man
  AssignClass (bf473ddc-0430-446d-ac82-91c1be0970f2)
 Call ID: bf473ddc-0430-446d-ac82-91c1be0970f2
  Args:
    type: :Person
    source: John_Ulick_Knatchbull
  AddLiteral (d835e36d-95b9-43f4-a7a0-a4ee918eee9d)
 Call ID: d835e36d-95b9-43f4-a7a0-a4ee918eee9d
  Args:
    literal_value: 1924
    source: John_Ulick_Knatchbull
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (3b83b7a4-7ac8-41af-8a8d-845990a6746b)
 Call ID: 3b83b7a4-7ac8-41af-8a8d-845990a6746b
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 2005
    source: John_Ulick_Knatchbull
  AddLiteral (63b3ad50-63d6-4feb-8b6c-12b391e281ee)
 Call ID: 63b3ad50-63d6-4feb-8b6c-12b391e281ee
  Args:
    literal_type: xsd:string
    relation: :knownAs
    literal_value: John Brabourne
    source: John_Ulick_Knatchbull
  AssignClass (82487fdb-a30b-4b01-a98b-d97850bcd6db)
 Call ID: 82487fdb-a30b-4b01-a98b-d97850bcd6db
  Args:
    source: Michael_Knatchbull
    type: :Man
  AssignClass (6dc7ae81-63b3-4aa8-b471-e8c6049cf5b6)
 Call ID: 6dc7ae81-63b3-4aa8-b471-e8c6049cf5b6
  Args:
    source: Michael_Knatchbull
    type: :Person
  AssignClass (d5f80779-9e49-4188-ba46-c34623529816)
 Call ID: d5f80779-9e49-4188-ba46-c34623529816
  Args:
    type: :Woman
    source: Lady_Doreen_Browne
  AssignClass (ebce2ff9-5349-471b-b276-fb48803fded3)
 Call ID: ebce2ff9-5349-471b-b276-fb48803fded3
  Args:
    source: Lady_Doreen_Browne
    type: :Person
  AddTriple (d86ae000-698e-45e0-85c8-e63087cb88fd)
 Call ID: d86ae000-698e-45e0-85c8-e63087cb88fd
  Args:
    source: John_Ulick_Knatchbull
    relation: :hasFather
    target: Michael_Knatchbull
  AddTriple (f88fc6a0-6036-40ed-a89e-16c21f7d3029)
 Call ID: f88fc6a0-6036-40ed-a89e-16c21f7d3029
  Args:
    target: Lady_Doreen_Browne
    relation: :hasMother
    source: John_Ulick_Knatchbull
  AssignClass (87d19628-d9ba-4b48-8cb3-9ca429fe5d82)
 Call ID: 87d19628-d9ba-4b48-8cb3-9ca429fe5d82
  Args:
    type: :Woman
    source: Patricia_Mountbatten
  AssignClass (20bbf180-ef8d-4054-9331-3800a551dcd1)
 Call ID: 20bbf180-ef8d-4054-9331-3800a551dcd1
  Args:
    type: :Person
    source: Patricia_Mountbatten
  AddTriple (68cdabeb-49c5-47c9-8334-9bb83e51edbe)
 Call ID: 68cdabeb-49c5-47c9-8334-9bb83e51edbe
  Args:
    source: John_Ulick_Knatchbull
    relation: :hasRelation
    target: Patricia_Mountbatten
  AddLiteral (4ce94f9e-862a-4121-96f1-29ea2bf90c82)
 Call ID: 4ce94f9e-862a-4121-96f1-29ea2bf90c82
  Args:
    source: John_Ulick_Knatchbull
    literal_value: 1946
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AssignClass (9ec1ddfe-c65f-455f-8974-284efac28f47)
 Call ID: 9ec1ddfe-c65f-455f-8974-284efac28f47
  Args:
    type: :Man
    source: Louis_Mountbatten
  AssignClass (502a6235-18de-4442-baf4-1f8c74e8f5bf)
 Call ID: 502a6235-18de-4442-baf4-1f8c74e8f5bf
  Args:
    source: Louis_Mountbatten
    type: :Person
  AddTriple (4b458711-a242-42a9-b5c0-dd1e578dfb32)
 Call ID: 4b458711-a242-42a9-b5c0-dd1e578dfb32
  Args:
    source: Patricia_Mountbatten
    target: Louis_Mountbatten
    relation: :hasFather
  AssignClass (cf6eb4b7-0aec-41a3-9603-a452883c7e1c)
 Call ID: cf6eb4b7-0aec-41a3-9603-a452883c7e1c
  Args:
    type: :Man
    source: Norton_Louis_Philip_Knatchbull
  AssignClass (82ac6c23-4fd0-425b-bb5e-b61a88dd8af5)
 Call ID: 82ac6c23-4fd0-425b-bb5e-b61a88dd8af5
  Args:
    type: :Person
    source: Norton_Louis_Philip_Knatchbull
  AddTriple (625c40fa-25fd-4b52-a16e-9384e6efbee6)
 Call ID: 625c40fa-25fd-4b52-a16e-9384e6efbee6
  Args:
    target: John_Ulick_Knatchbull
    relation: :hasFather
    source: Norton_Louis_Philip_Knatchbull
  AddTriple (6cde36c1-a65a-4d3a-9eb1-c4f041d81e45)
 Call ID: 6cde36c1-a65a-4d3a-9eb1-c4f041d81e45
  Args:
    target: Patricia_Mountbatten
    relation: :hasMother
    source: Norton_Louis_Philip_Knatchbull
  AssignClass (ab42788e-df97-4370-acf9-514dd68e019d)
 Call ID: ab42788e-df97-4370-acf9-514dd68e019d
  Args:
    source: Lady_Amanda_Patricia_Victoria_Knatchbull
    type: :Woman
  AssignClass (4a0dc404-b44f-4331-bf4c-daf4dc9e3216)
 Call ID: 4a0dc404-b44f-4331-bf4c-daf4dc9e3216
  Args:
    source: Lady_Amanda_Patricia_Victoria_Knatchbull
    type: :Person
  AddTriple (d4f6d72a-c033-4cf6-ba91-d721037d8400)
 Call ID: d4f6d72a-c033-4cf6-ba91-d721037d8400
  Args:
    target: John_Ulick_Knatchbull
    relation: :hasFather
    source: Lady_Amanda_Patricia_Victoria_Knatchbull
  AddTriple (4b2e81b7-9035-4064-87cd-ebe7553d1def)
 Call ID: 4b2e81b7-9035-4064-87cd-ebe7553d1def
  Args:
    target: Patricia_Mountbatten
    relation: :hasMother
    source: Lady_Amanda_Patricia_Victoria_Knatchbull
  AssignClass (46951a54-b177-44a1-b61c-3b808f82a97e)
 Call ID: 46951a54-b177-44a1-b61c-3b808f82a97e
  Args:
    type: :Man
    source: Nicholas_Timothy_Charles_Knatchbull
  AssignClass (1fee4bd8-972a-4550-9872-30c1c65a0b82)
 Call ID: 1fee4bd8-972a-4550-9872-30c1c65a0b82
  Args:
    source: Nicholas_Timothy_Charles_Knatchbull
    type: :Person
  AddTriple (26970305-5617-4b2f-bf81-114e4fa91052)
 Call ID: 26970305-5617-4b2f-bf81-114e4fa91052
  Args:
    source: Nicholas_Timothy_Charles_Knatchbull
    relation: :hasFather
    target: John_Ulick_Knatchbull
  AddTriple (46468e0f-3d76-4c3f-aa0c-5feed44a0f1a)
 Call ID: 46468e0f-3d76-4c3f-aa0c-5feed44a0f1a
  Args:
    relation: :hasMother
    target: Patricia_Mountbatten
    source: Nicholas_Timothy_Charles_Knatchbull
  AssignClass (45681c3f-f711-4c33-96f6-6ac69d1fb846)
 Call ID: 45681c3f-f711-4c33-96f6-6ac69d1fb846
  Args:
    type: :Man
    source: Timothy_Knatchbull
  AssignClass (1dac27d1-3d75-4bbb-b48c-cec2dd2dcd1c)
 Call ID: 1dac27d1-3d75-4bbb-b48c-cec2dd2dcd1c
  Args:
    type: :Person
    source: Timothy_Knatchbull
  AddTriple (c8d62caa-9cd7-465f-a75e-edd1e5cb191a)
 Call ID: c8d62caa-9cd7-465f-a75e-edd1e5cb191a
  Args:
    source: Timothy_Knatchbull
    target: John_Ulick_Knatchbull
    relation: :hasFather
  AddTriple (c36d105c-86fd-477f-ab7e-9e198a660766)
 Call ID: c36d105c-86fd-477f-ab7e-9e198a660766
  Args:
    source: Timothy_Knatchbull
    target: Patricia_Mountbatten
    relation: :hasMother
  AssignClass (36c77d05-77a3-4524-b149-72968bbe9ca7)
 Call ID: 36c77d05-77a3-4524-b149-72968bbe9ca7
  Args:
    type: :Woman
    source: Louise_Mountbatten
  AssignClass (9a9ab11b-a15d-470e-b4b0-57d4830a6ee4)
 Call ID: 9a9ab11b-a15d-470e-b4b0-57d4830a6ee4
  Args:
    source: Louise_Mountbatten
    type: :Person
  AddTriple (4e667158-87b9-452a-8f80-29dcb42ec4c4)
 Call ID: 4e667158-87b9-452a-8f80-29dcb42ec4c4
  Args:
    source: Louise_Mountbatten
    target: Patricia_Mountbatten
    relation: :isAuntOf
  AssignClass (d3c1331f-4765-4da3-9ed7-867b67e101f0)
 Call ID: d3c1331f-4765-4da3-9ed7-867b67e101f0
  Args:
    source: Philip_Duke_of_Edinburgh
    type: :Man
  AssignClass (8b07579e-70cf-4137-a910-ff02c39cde72)
 Call ID: 8b07579e-70cf-4137-a910-ff02c39cde72
  Args:
    type: :Person
    source: Philip_Duke_of_Edinburgh
  AddTriple (148ec56b-96fd-4759-928a-d0e5e6838f3c)
 Call ID: 148ec56b-96fd-4759-928a-d0e5e6838f3c
  Args:
    target: Patricia_Mountbatten
    relation: :isBloodrelationOf
    source: Philip_Duke_of_Edinburgh
  Finish (c5b25944-0d5e-492f-af66-704652dd6af6)
 Call ID: c5b25944-0d5e-492f-af66-704652dd6af6
  Args: