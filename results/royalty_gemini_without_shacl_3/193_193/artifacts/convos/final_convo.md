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
  AssignClass (34140c6f-3531-4838-8166-203bc4621ee9)
 Call ID: 34140c6f-3531-4838-8166-203bc4621ee9
  Args:
    source: :PrincessAdelaideOfSaxeMeiningen
    type: :Woman
  AssignClass (f7501f44-3edd-4cf0-976d-1c72978e4689)
 Call ID: f7501f44-3edd-4cf0-976d-1c72978e4689
  Args:
    type: :Person
    source: :PrincessAdelaideOfSaxeMeiningen
  AddLiteral (67661e17-5706-420f-a084-768bea0dfdaf)
 Call ID: 67661e17-5706-420f-a084-768bea0dfdaf
  Args:
    relation: :hasBirthYear
    literal_value: 1891
    literal_type: xsd:integer
    source: :PrincessAdelaideOfSaxeMeiningen
  AddLiteral (f7c8f373-c345-4987-ab70-c2b5151fe830)
 Call ID: f7c8f373-c345-4987-ab70-c2b5151fe830
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: :PrincessAdelaideOfSaxeMeiningen
    literal_value: 1971
  AssignClass (6b34d122-6689-473d-8263-30ed61a4a5d9)
 Call ID: 6b34d122-6689-473d-8263-30ed61a4a5d9
  Args:
    source: :PrinceFrederickJohnOfSaxeMeiningen
    type: :Man
  AssignClass (4ef40d4e-700b-4296-af48-d74058b6ac11)
 Call ID: 4ef40d4e-700b-4296-af48-d74058b6ac11
  Args:
    source: :PrinceFrederickJohnOfSaxeMeiningen
    type: :Person
  AssignClass (0fb2db93-1140-4ff6-b07f-56eef26bda8a)
 Call ID: 0fb2db93-1140-4ff6-b07f-56eef26bda8a
  Args:
    type: :Woman
    source: :CountessAdelaideOfLippeBiesterfeld
  AssignClass (f269ed8c-e694-4179-aa5a-1237faa22371)
 Call ID: f269ed8c-e694-4179-aa5a-1237faa22371
  Args:
    source: :CountessAdelaideOfLippeBiesterfeld
    type: :Person
  AddTriple (443b9548-80fe-4937-9d6e-10f978077e5f)
 Call ID: 443b9548-80fe-4937-9d6e-10f978077e5f
  Args:
    target: :PrinceFrederickJohnOfSaxeMeiningen
    source: :PrincessAdelaideOfSaxeMeiningen
    relation: :hasFather
  AddTriple (8f5d1f5c-60b4-4b7f-a59b-9e94bcb65028)
 Call ID: 8f5d1f5c-60b4-4b7f-a59b-9e94bcb65028
  Args:
    relation: :hasMother
    target: :CountessAdelaideOfLippeBiesterfeld
    source: :PrincessAdelaideOfSaxeMeiningen
  AssignClass (0e9a3e82-abde-4754-ac12-146a001d6c97)
 Call ID: 0e9a3e82-abde-4754-ac12-146a001d6c97
  Args:
    type: :Man
    source: :GeorgeIIOfSaxeMeiningen
  AssignClass (dd00f7a8-6215-44ca-88b3-af38dc622f62)
 Call ID: dd00f7a8-6215-44ca-88b3-af38dc622f62
  Args:
    type: :Person
    source: :GeorgeIIOfSaxeMeiningen
  AssignClass (75753853-e715-44c6-aea9-6ff8753a128d)
 Call ID: 75753853-e715-44c6-aea9-6ff8753a128d
  Args:
    type: :Woman
    source: :FeodoraOfHohenloheLangenburg
  AssignClass (f2c6c4c5-621d-413e-a154-52a2697e96db)
 Call ID: f2c6c4c5-621d-413e-a154-52a2697e96db
  Args:
    source: :FeodoraOfHohenloheLangenburg
    type: :Person
  AddTriple (6313a8e3-0ad5-4e5b-9386-52649c1bc5ad)
 Call ID: 6313a8e3-0ad5-4e5b-9386-52649c1bc5ad
  Args:
    source: :PrinceFrederickJohnOfSaxeMeiningen
    target: :GeorgeIIOfSaxeMeiningen
    relation: :hasFather
  AddTriple (18e6e52e-dbad-4ab0-8a0e-6c667e23f451)
 Call ID: 18e6e52e-dbad-4ab0-8a0e-6c667e23f451
  Args:
    relation: :hasMother
    target: :FeodoraOfHohenloheLangenburg
    source: :PrinceFrederickJohnOfSaxeMeiningen
  AssignClass (33de0c4c-9041-45d0-b6aa-a33a26388937)
 Call ID: 33de0c4c-9041-45d0-b6aa-a33a26388937
  Args:
    type: :Man
    source: :PrinceGeorge
  AssignClass (891ea2cd-ca86-47ee-9e9e-8403431ff04a)
 Call ID: 891ea2cd-ca86-47ee-9e9e-8403431ff04a
  Args:
    type: :Person
    source: :PrinceGeorge
  AddTriple (35138c15-1398-406e-8f16-ffc26684f213)
 Call ID: 35138c15-1398-406e-8f16-ffc26684f213
  Args:
    target: :PrinceGeorge
    source: :PrincessAdelaideOfSaxeMeiningen
    relation: :isSiblingOf
  AssignClass (ed0eaf98-0db9-4a00-af0d-40902711f10d)
 Call ID: ed0eaf98-0db9-4a00-af0d-40902711f10d
  Args:
    type: :Man
    source: :PrinceBernard
  AssignClass (6f1602a6-68ce-4023-8036-be69a25fa1f2)
 Call ID: 6f1602a6-68ce-4023-8036-be69a25fa1f2
  Args:
    type: :Person
    source: :PrinceBernard
  AddTriple (744ad256-2717-4067-94c8-ee51611ff8aa)
 Call ID: 744ad256-2717-4067-94c8-ee51611ff8aa
  Args:
    source: :PrincessAdelaideOfSaxeMeiningen
    target: :PrinceBernard
    relation: :isSiblingOf
  AssignClass (dcba1e87-ca56-4dd2-a753-c290c20e2494)
 Call ID: dcba1e87-ca56-4dd2-a753-c290c20e2494
  Args:
    type: :Man
    source: :ErnstCountOfLippeBiesterfeld
  AssignClass (049cabb8-927f-4b9f-a45b-4e655d5747e3)
 Call ID: 049cabb8-927f-4b9f-a45b-4e655d5747e3
  Args:
    source: :ErnstCountOfLippeBiesterfeld
    type: :Person
  AddTriple (821a9d02-7410-4eb4-82fd-6bf559fad55d)
 Call ID: 821a9d02-7410-4eb4-82fd-6bf559fad55d
  Args:
    source: :ErnstCountOfLippeBiesterfeld
    target: :CountessAdelaideOfLippeBiesterfeld
    relation: :isFatherOf
  AssignClass (b434723c-c1ba-4653-a033-e83ce0f6a504)
 Call ID: b434723c-c1ba-4653-a033-e83ce0f6a504
  Args:
    source: :PrinceAdalbertOfPrussia
    type: :Man
  AssignClass (00e63d6c-a7d7-4ab6-ae20-7e4201d26ff7)
 Call ID: 00e63d6c-a7d7-4ab6-ae20-7e4201d26ff7
  Args:
    source: :PrinceAdalbertOfPrussia
    type: :Person
  AddLiteral (69023bf3-128a-459b-9962-f799f8b279cb)
 Call ID: 69023bf3-128a-459b-9962-f799f8b279cb
  Args:
    literal_value: 1914
    source: :PrincessAdelaideOfSaxeMeiningen
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AddTriple (05a6592f-a2e1-4a64-9ac7-ffb3e015dac1)
 Call ID: 05a6592f-a2e1-4a64-9ac7-ffb3e015dac1
  Args:
    relation: :hasRelation
    target: :PrinceAdalbertOfPrussia
    source: :PrincessAdelaideOfSaxeMeiningen
  AssignClass (b65275a8-75bf-450e-9166-9bdb0dc37eec)
 Call ID: b65275a8-75bf-450e-9166-9bdb0dc37eec
  Args:
    type: :Man
    source: :KaiserWilliamIIOfGermany
  AssignClass (aa071e44-422b-4a74-a321-1d88e3ac5ab2)
 Call ID: aa071e44-422b-4a74-a321-1d88e3ac5ab2
  Args:
    type: :Person
    source: :KaiserWilliamIIOfGermany
  AddTriple (47326ef7-e93c-4b1e-be64-02e7fc5e8efc)
 Call ID: 47326ef7-e93c-4b1e-be64-02e7fc5e8efc
  Args:
    relation: :hasFather
    source: :PrinceAdalbertOfPrussia
    target: :KaiserWilliamIIOfGermany
  AddLiteral (68e268c4-6a7b-4b3a-9ce1-f5f454727e57)
 Call ID: 68e268c4-6a7b-4b3a-9ce1-f5f454727e57
  Args:
    literal_value: 1914
    literal_type: xsd:integer
    source: :PrinceFrederickJohnOfSaxeMeiningen
    relation: :hasDeathYear
  AssignClass (760ea77d-b2d1-47c4-b729-e481107eee47)
 Call ID: 760ea77d-b2d1-47c4-b729-e481107eee47
  Args:
    source: :PrinceHenryOfBavaria
    type: :Man
  AssignClass (300cb755-410c-49f6-bdf3-22059ad0b4b7)
 Call ID: 300cb755-410c-49f6-bdf3-22059ad0b4b7
  Args:
    source: :PrinceHenryOfBavaria
    type: :Person
  AssignClass (d464e2a7-99ac-4924-b601-9eb465bf6aeb)
 Call ID: d464e2a7-99ac-4924-b601-9eb465bf6aeb
  Args:
    source: :LudwigIIIOfBavaria
    type: :Man
  AssignClass (847a879c-a47b-4e08-aeef-39383bb64ddb)
 Call ID: 847a879c-a47b-4e08-aeef-39383bb64ddb
  Args:
    type: :Person
    source: :LudwigIIIOfBavaria
  AddTriple (0e6071ab-a5b8-4fd6-a62a-be2a9c5cca46)
 Call ID: 0e6071ab-a5b8-4fd6-a62a-be2a9c5cca46
  Args:
    target: :LudwigIIIOfBavaria
    source: :PrinceHenryOfBavaria
    relation: :hasAncestor
  Finish (602e8470-35fd-4c55-ad7f-3c7215fb4aa9)
 Call ID: 602e8470-35fd-4c55-ad7f-3c7215fb4aa9
  Args: