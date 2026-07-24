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
Princess Adelaide of Saxe-Meiningen (Adelaide Erna Caroline Marie Elisabeth; 16 August 1891 – 25 April 1971), later Princess Adalbert of Prussia, was the daughter of Prince Frederick John of Saxe-Meiningen and Countess Adelaide of Lippe-Biesterfeld.
Family

Adelaide (original German: Adelheid)'s father Prince Frederick was a younger son of George II of Saxe-Meiningen by his second wife Feodora of Hohenlohe-Langenburg.
She had five siblings, including Prince George, a prisoner of war killed during World War II, and Prince Bernard.
Adelaide's mother, also named Adelaide, was the eldest child of Ernst, Count of Lippe-Biesterfeld, who was the Regent of the principality of Lippe for seven years (1897–1904).
Marriage

On 3 August 1914, at the beginning of World War I, Adelaide married Prince Adalbert of Prussia at Wilhelmshaven, Schleswig-Holstein, Germany.
He was the third son of Kaiser William II of Germany.
Adelaide's father would die within a month, on 23 August 1914.
Less than a month after their marriage, Prince Adalbert was reported to have been killed in battle in Brussels.
This was only a rumor however, and the prince had been unharmed.
She and Prince Adalbert had three children:


Later life

After William II abdicated in 1918 at the end of World War I, Prince Adalbert sought refuge on his yacht, which had been maintained by a loyal crew.
Princess Adelaide and their children soon attempted to follow, travelling by train from Kiel.
They were delayed however, and eventually came to be staying in southern Bavaria with Prince Henry of Bavaria (a grandson of Ludwig III of Bavaria) and his wife.
She and Prince Adalbert were later reunited.
Princess Adelaide died on 25 April 1971 in La Tour-de-Peilz, Switzerland.



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
  AssignClass (0a94c310-42da-4daf-8b84-62d2e5d5ac20)
 Call ID: 0a94c310-42da-4daf-8b84-62d2e5d5ac20
  Args:
    type: :Woman
    source: :AdelaideOfSaxeMeiningen
  AssignClass (2d7a3d08-74bb-460a-8f8a-f7f2f22beb12)
 Call ID: 2d7a3d08-74bb-460a-8f8a-f7f2f22beb12
  Args:
    source: :AdelaideOfSaxeMeiningen
    type: :Person
  AddLiteral (1d3c7d04-8fa9-4c5b-bd39-766c7ee1609e)
 Call ID: 1d3c7d04-8fa9-4c5b-bd39-766c7ee1609e
  Args:
    literal_value: Adelaide Erna Caroline Marie Elisabeth
    literal_type: xsd:string
    relation: :alsoKnownAs
    source: :AdelaideOfSaxeMeiningen
  AddLiteral (8541d9d9-dc1a-4f23-9b35-17bb155d9ebc)
 Call ID: 8541d9d9-dc1a-4f23-9b35-17bb155d9ebc
  Args:
    literal_value: Adelheid
    literal_type: xsd:string
    source: :AdelaideOfSaxeMeiningen
    relation: :alsoKnownAs
  AddLiteral (0dd05519-006e-4468-9f8f-b523bd7bb25d)
 Call ID: 0dd05519-006e-4468-9f8f-b523bd7bb25d
  Args:
    source: :AdelaideOfSaxeMeiningen
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1891
  AddLiteral (b5f3d0e6-a043-4b12-8804-52fb5d9cef41)
 Call ID: b5f3d0e6-a043-4b12-8804-52fb5d9cef41
  Args:
    literal_value: 1971
    relation: :hasDeathYear
    source: :AdelaideOfSaxeMeiningen
    literal_type: xsd:integer
  AssignClass (d27b359b-1425-4205-9ada-125b18f75956)
 Call ID: d27b359b-1425-4205-9ada-125b18f75956
  Args:
    source: :PrinceFrederickJohnOfSaxeMeiningen
    type: :Man
  AssignClass (29a9d2c3-c200-45d2-ab80-9db275d46b31)
 Call ID: 29a9d2c3-c200-45d2-ab80-9db275d46b31
  Args:
    type: :Person
    source: :PrinceFrederickJohnOfSaxeMeiningen
  AssignClass (be694e9d-3ad9-4388-aec5-1019d76c9cde)
 Call ID: be694e9d-3ad9-4388-aec5-1019d76c9cde
  Args:
    source: :CountessAdelaideOfLippeBiesterfeld
    type: :Woman
  AssignClass (bc98cc48-0653-496c-abd8-0546df98e3cb)
 Call ID: bc98cc48-0653-496c-abd8-0546df98e3cb
  Args:
    source: :CountessAdelaideOfLippeBiesterfeld
    type: :Person
  AddTriple (8a0c740e-a434-4298-86b4-df538307230d)
 Call ID: 8a0c740e-a434-4298-86b4-df538307230d
  Args:
    source: :AdelaideOfSaxeMeiningen
    target: :PrinceFrederickJohnOfSaxeMeiningen
    relation: :hasFather
  AddTriple (1a10185c-f5ae-4dbb-bd67-9c33adbfee31)
 Call ID: 1a10185c-f5ae-4dbb-bd67-9c33adbfee31
  Args:
    target: :CountessAdelaideOfLippeBiesterfeld
    source: :AdelaideOfSaxeMeiningen
    relation: :hasMother
  AssignClass (6efda513-aef2-4404-b9a8-099e817c4a41)
 Call ID: 6efda513-aef2-4404-b9a8-099e817c4a41
  Args:
    type: :Man
    source: :GeorgeIIOfSaxeMeiningen
  AssignClass (a680f171-8670-4c2e-b451-74802841f4e7)
 Call ID: a680f171-8670-4c2e-b451-74802841f4e7
  Args:
    source: :GeorgeIIOfSaxeMeiningen
    type: :Person
  AssignClass (a966a101-9441-4407-bb61-d3f779dd2e02)
 Call ID: a966a101-9441-4407-bb61-d3f779dd2e02
  Args:
    source: :FeodoraOfHohenloheLangenburg
    type: :Woman
  AssignClass (d67327ba-a8b1-4284-b00d-ead5b2c09363)
 Call ID: d67327ba-a8b1-4284-b00d-ead5b2c09363
  Args:
    source: :FeodoraOfHohenloheLangenburg
    type: :Person
  AddTriple (25e6da0b-baed-49f0-a3f4-06b0ff301162)
 Call ID: 25e6da0b-baed-49f0-a3f4-06b0ff301162
  Args:
    target: :GeorgeIIOfSaxeMeiningen
    source: :PrinceFrederickJohnOfSaxeMeiningen
    relation: :hasFather
  AddTriple (970e3b22-54f0-46f4-a019-7c2aa3f5e99d)
 Call ID: 970e3b22-54f0-46f4-a019-7c2aa3f5e99d
  Args:
    relation: :hasMother
    source: :PrinceFrederickJohnOfSaxeMeiningen
    target: :FeodoraOfHohenloheLangenburg
  AssignClass (3187d718-7c5b-4c87-bc73-bd99c5332d77)
 Call ID: 3187d718-7c5b-4c87-bc73-bd99c5332d77
  Args:
    type: :Man
    source: :PrinceGeorge
  AssignClass (897be3b8-a810-401c-a60e-040b8a2c3c9f)
 Call ID: 897be3b8-a810-401c-a60e-040b8a2c3c9f
  Args:
    source: :PrinceGeorge
    type: :Person
  AssignClass (b955a008-c80d-412d-bb8e-d96e00005f3b)
 Call ID: b955a008-c80d-412d-bb8e-d96e00005f3b
  Args:
    source: :PrinceBernard
    type: :Man
  AssignClass (b322fa68-d053-41fd-8b31-ed4c8e29d8bc)
 Call ID: b322fa68-d053-41fd-8b31-ed4c8e29d8bc
  Args:
    type: :Person
    source: :PrinceBernard
  AddTriple (7115e8bb-b7bf-42f7-b279-a0b3be71728d)
 Call ID: 7115e8bb-b7bf-42f7-b279-a0b3be71728d
  Args:
    target: :PrinceGeorge
    source: :AdelaideOfSaxeMeiningen
    relation: :isSiblingOf
  AddTriple (731f2452-3b57-46cc-97f0-93ba1208af79)
 Call ID: 731f2452-3b57-46cc-97f0-93ba1208af79
  Args:
    target: :PrinceBernard
    source: :AdelaideOfSaxeMeiningen
    relation: :isSiblingOf
  AssignClass (bd5770b3-829e-4c2a-94d5-e47fa08e2ef8)
 Call ID: bd5770b3-829e-4c2a-94d5-e47fa08e2ef8
  Args:
    type: :Man
    source: :ErnstCountOfLippeBiesterfeld
  AssignClass (91c06458-049c-4ba1-8d2b-e5cd09479706)
 Call ID: 91c06458-049c-4ba1-8d2b-e5cd09479706
  Args:
    source: :ErnstCountOfLippeBiesterfeld
    type: :Person
  AddTriple (ce339d68-29a8-49be-bd78-aa927dd73d96)
 Call ID: ce339d68-29a8-49be-bd78-aa927dd73d96
  Args:
    relation: :hasFather
    source: :CountessAdelaideOfLippeBiesterfeld
    target: :ErnstCountOfLippeBiesterfeld
  AssignClass (f1b20d4d-14fc-44ba-bfa8-a630c24417a0)
 Call ID: f1b20d4d-14fc-44ba-bfa8-a630c24417a0
  Args:
    type: :Man
    source: :PrinceAdalbertOfPrussia
  AssignClass (18d6ecbe-6ff8-4f94-af03-61ce7d77fb27)
 Call ID: 18d6ecbe-6ff8-4f94-af03-61ce7d77fb27
  Args:
    source: :PrinceAdalbertOfPrussia
    type: :Person
  AddLiteral (61dfc635-c9f6-4ae9-91e4-7dabb8f66652)
 Call ID: 61dfc635-c9f6-4ae9-91e4-7dabb8f66652
  Args:
    source: :AdelaideOfSaxeMeiningen
    relation: :hasMarriageYear
    literal_type: xsd:integer
    literal_value: 1914
  AddTriple (c3be9cf7-0a03-4822-8d58-390d53e48071)
 Call ID: c3be9cf7-0a03-4822-8d58-390d53e48071
  Args:
    target: :PrinceAdalbertOfPrussia
    source: :AdelaideOfSaxeMeiningen
    relation: :hasRelation
  AssignClass (750bb691-be2d-45ea-a560-079752e71f49)
 Call ID: 750bb691-be2d-45ea-a560-079752e71f49
  Args:
    source: :KaiserWilliamIIOfGermany
    type: :Man
  AssignClass (12871557-2376-431f-a653-0a69e6bc81bd)
 Call ID: 12871557-2376-431f-a653-0a69e6bc81bd
  Args:
    source: :KaiserWilliamIIOfGermany
    type: :Person
  AddTriple (f6888ec6-2d41-4268-a273-f6fa23804950)
 Call ID: f6888ec6-2d41-4268-a273-f6fa23804950
  Args:
    relation: :hasFather
    target: :KaiserWilliamIIOfGermany
    source: :PrinceAdalbertOfPrussia
  AssignClass (8d071532-82da-4f70-a5df-e908a9c4b8b3)
 Call ID: 8d071532-82da-4f70-a5df-e908a9c4b8b3
  Args:
    source: :PrinceHenryOfBavaria
    type: :Man
  AssignClass (9ea6f337-1599-4403-b913-cd559911bfe4)
 Call ID: 9ea6f337-1599-4403-b913-cd559911bfe4
  Args:
    source: :PrinceHenryOfBavaria
    type: :Person
  AssignClass (13b7b68b-bf38-4a9d-81f8-d25d4c81e278)
 Call ID: 13b7b68b-bf38-4a9d-81f8-d25d4c81e278
  Args:
    type: :Man
    source: :LudwigIIIOfBavaria
  AssignClass (f3f03e54-b8d0-4f38-bfc8-b8407cb2b12f)
 Call ID: f3f03e54-b8d0-4f38-bfc8-b8407cb2b12f
  Args:
    type: :Person
    source: :LudwigIIIOfBavaria
  AddTriple (fb634b38-4640-4c9b-b4b6-84d2fdd9872f)
 Call ID: fb634b38-4640-4c9b-b4b6-84d2fdd9872f
  Args:
    source: :PrinceHenryOfBavaria
    target: :LudwigIIIOfBavaria
    relation: :hasFather
  Finish (31085cf5-4cfa-4acd-8ae1-6136aeb48946)
 Call ID: 31085cf5-4cfa-4acd-8ae1-6136aeb48946
  Args: