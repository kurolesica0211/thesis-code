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
  AssignClass (f65c3173-1508-431c-a53e-7335332c7d1c)
 Call ID: f65c3173-1508-431c-a53e-7335332c7d1c
  Args:
    type: :Woman
    source: Adelaide_of_Saxe-Meiningen
  AssignClass (fc6e6733-f7c3-4f0f-80f2-9c210ffa5fa4)
 Call ID: fc6e6733-f7c3-4f0f-80f2-9c210ffa5fa4
  Args:
    source: Adelaide_of_Saxe-Meiningen
    type: :Person
  AddLiteral (68165e89-989d-49c6-8a8d-56b13ef8398f)
 Call ID: 68165e89-989d-49c6-8a8d-56b13ef8398f
  Args:
    source: Adelaide_of_Saxe-Meiningen
    relation: :hasBirthYear
    literal_value: 1891
    literal_type: xsd:integer
  AddLiteral (9c70c586-c57c-4533-b885-b7c4b636bb99)
 Call ID: 9c70c586-c57c-4533-b885-b7c4b636bb99
  Args:
    literal_type: xsd:integer
    literal_value: 1971
    source: Adelaide_of_Saxe-Meiningen
    relation: :hasDeathYear
  AssignClass (fed55a22-bacb-4188-b759-a561ffe76690)
 Call ID: fed55a22-bacb-4188-b759-a561ffe76690
  Args:
    type: :Man
    source: Prince_Frederick_John_of_Saxe-Meiningen
  AssignClass (7292cc0c-5c6f-4dcb-98ad-e1a4d3713793)
 Call ID: 7292cc0c-5c6f-4dcb-98ad-e1a4d3713793
  Args:
    source: Prince_Frederick_John_of_Saxe-Meiningen
    type: :Person
  AssignClass (9c08c1f2-d6bd-45b5-aaac-446d9025fe2c)
 Call ID: 9c08c1f2-d6bd-45b5-aaac-446d9025fe2c
  Args:
    type: :Woman
    source: Countess_Adelaide_of_Lippe-Biesterfeld
  AssignClass (77006f05-af5c-485b-90c6-92ad957798ac)
 Call ID: 77006f05-af5c-485b-90c6-92ad957798ac
  Args:
    type: :Person
    source: Countess_Adelaide_of_Lippe-Biesterfeld
  AddTriple (9dc08bab-71bd-4858-b120-3d52dc6c9c2a)
 Call ID: 9dc08bab-71bd-4858-b120-3d52dc6c9c2a
  Args:
    target: Prince_Frederick_John_of_Saxe-Meiningen
    source: Adelaide_of_Saxe-Meiningen
    relation: :hasFather
  AddTriple (ef1df57a-8274-48d0-9b51-a71de99bce89)
 Call ID: ef1df57a-8274-48d0-9b51-a71de99bce89
  Args:
    target: Countess_Adelaide_of_Lippe-Biesterfeld
    source: Adelaide_of_Saxe-Meiningen
    relation: :hasMother
  AssignClass (4481fd7f-b4ef-4aea-8fa2-f0677011b562)
 Call ID: 4481fd7f-b4ef-4aea-8fa2-f0677011b562
  Args:
    type: :Man
    source: George_II_of_Saxe-Meiningen
  AssignClass (b0cce0b2-ef89-4a03-907a-a3217597ec09)
 Call ID: b0cce0b2-ef89-4a03-907a-a3217597ec09
  Args:
    source: George_II_of_Saxe-Meiningen
    type: :Person
  AssignClass (d25e9a52-8e2d-4006-aca3-4907790413ee)
 Call ID: d25e9a52-8e2d-4006-aca3-4907790413ee
  Args:
    type: :Woman
    source: Feodora_of_Hohenlohe-Langenburg
  AssignClass (3d2d8707-824d-4346-bb4a-36cef458ba03)
 Call ID: 3d2d8707-824d-4346-bb4a-36cef458ba03
  Args:
    type: :Person
    source: Feodora_of_Hohenlohe-Langenburg
  AddTriple (ef7ef278-3629-4cc3-82c4-0f43afc6c7c0)
 Call ID: ef7ef278-3629-4cc3-82c4-0f43afc6c7c0
  Args:
    source: Prince_Frederick_John_of_Saxe-Meiningen
    relation: :hasFather
    target: George_II_of_Saxe-Meiningen
  AddTriple (724e7bd4-6273-4bbb-8c91-1c45b9b78721)
 Call ID: 724e7bd4-6273-4bbb-8c91-1c45b9b78721
  Args:
    relation: :hasMother
    source: Prince_Frederick_John_of_Saxe-Meiningen
    target: Feodora_of_Hohenlohe-Langenburg
  AssignClass (f79e72ec-125a-4c4b-8b3b-f44e9df8ae3c)
 Call ID: f79e72ec-125a-4c4b-8b3b-f44e9df8ae3c
  Args:
    type: :Man
    source: Prince_George
  AssignClass (495aa471-a6f6-4878-ba8b-d9568ac37230)
 Call ID: 495aa471-a6f6-4878-ba8b-d9568ac37230
  Args:
    type: :Person
    source: Prince_George
  AssignClass (6e0326ae-c585-499f-ae89-ce050daff202)
 Call ID: 6e0326ae-c585-499f-ae89-ce050daff202
  Args:
    source: Prince_Bernard
    type: :Man
  AssignClass (886fdef7-c63c-407a-bb40-393ea8b744a2)
 Call ID: 886fdef7-c63c-407a-bb40-393ea8b744a2
  Args:
    type: :Person
    source: Prince_Bernard
  AddTriple (c825b402-df76-4653-aed7-8eae5b8737a8)
 Call ID: c825b402-df76-4653-aed7-8eae5b8737a8
  Args:
    target: Prince_George
    source: Adelaide_of_Saxe-Meiningen
    relation: :hasBrother
  AddTriple (20d1347b-57b7-4fc8-bc49-79f7e7d6f598)
 Call ID: 20d1347b-57b7-4fc8-bc49-79f7e7d6f598
  Args:
    relation: :hasBrother
    source: Adelaide_of_Saxe-Meiningen
    target: Prince_Bernard
  AssignClass (4e0171b4-ed49-41e2-a9cb-c25b3d8bd8ff)
 Call ID: 4e0171b4-ed49-41e2-a9cb-c25b3d8bd8ff
  Args:
    type: :Man
    source: Ernst_Count_of_Lippe-Biesterfeld
  AssignClass (7c8ddbb0-c10e-4f55-9218-a701f9f4216c)
 Call ID: 7c8ddbb0-c10e-4f55-9218-a701f9f4216c
  Args:
    type: :Person
    source: Ernst_Count_of_Lippe-Biesterfeld
  AddTriple (0a627e72-312f-4c84-821d-26790eaf8982)
 Call ID: 0a627e72-312f-4c84-821d-26790eaf8982
  Args:
    relation: :hasFather
    source: Countess_Adelaide_of_Lippe-Biesterfeld
    target: Ernst_Count_of_Lippe-Biesterfeld
  AssignClass (aa5b9fa6-9cc7-4bfe-80cb-a1a765971afa)
 Call ID: aa5b9fa6-9cc7-4bfe-80cb-a1a765971afa
  Args:
    source: Prince_Adalbert_of_Prussia
    type: :Man
  AssignClass (5c228964-69fd-48fb-b8c4-259c5ad880b2)
 Call ID: 5c228964-69fd-48fb-b8c4-259c5ad880b2
  Args:
    source: Prince_Adalbert_of_Prussia
    type: :Person
  AddLiteral (b98f43c0-c820-4b2f-a99f-8f52465558c6)
 Call ID: b98f43c0-c820-4b2f-a99f-8f52465558c6
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    source: Adelaide_of_Saxe-Meiningen
    literal_value: 1914
  AddTriple (1aedc0ca-0470-47f9-989e-58f8e4773eff)
 Call ID: 1aedc0ca-0470-47f9-989e-58f8e4773eff
  Args:
    target: Prince_Adalbert_of_Prussia
    relation: :hasRelation
    source: Adelaide_of_Saxe-Meiningen
  AssignClass (a499db9f-3125-4821-8d52-67debb159c45)
 Call ID: a499db9f-3125-4821-8d52-67debb159c45
  Args:
    type: :Man
    source: Kaiser_William_II_of_Germany
  AssignClass (b92fb17c-3733-4f66-afa0-2de4533966f1)
 Call ID: b92fb17c-3733-4f66-afa0-2de4533966f1
  Args:
    source: Kaiser_William_II_of_Germany
    type: :Person
  AddTriple (67a3521b-3fb5-4a7c-b776-07bb8c67b87c)
 Call ID: 67a3521b-3fb5-4a7c-b776-07bb8c67b87c
  Args:
    target: Kaiser_William_II_of_Germany
    source: Prince_Adalbert_of_Prussia
    relation: :hasFather
  AddLiteral (24dcde44-2967-442f-81ea-67ca938112ec)
 Call ID: 24dcde44-2967-442f-81ea-67ca938112ec
  Args:
    literal_type: xsd:integer
    source: Prince_Frederick_John_of_Saxe-Meiningen
    relation: :hasDeathYear
    literal_value: 1914
  AssignClass (d1d6a01a-dd93-478f-a567-57d4c8a7aad9)
 Call ID: d1d6a01a-dd93-478f-a567-57d4c8a7aad9
  Args:
    type: :Man
    source: Prince_Henry_of_Bavaria
  AssignClass (78bf2d8b-ad26-4b84-b7cc-acab63af2715)
 Call ID: 78bf2d8b-ad26-4b84-b7cc-acab63af2715
  Args:
    source: Prince_Henry_of_Bavaria
    type: :Person
  AssignClass (207daa6f-76cc-4f1c-8587-c3699b282b75)
 Call ID: 207daa6f-76cc-4f1c-8587-c3699b282b75
  Args:
    source: Ludwig_III_of_Bavaria
    type: :Man
  AssignClass (0a830fd4-21c6-4422-a470-62573b044c0c)
 Call ID: 0a830fd4-21c6-4422-a470-62573b044c0c
  Args:
    type: :Person
    source: Ludwig_III_of_Bavaria
  AddTriple (c7cba920-1a10-4f07-b7b9-3d4f63920591)
 Call ID: c7cba920-1a10-4f07-b7b9-3d4f63920591
  Args:
    target: Ludwig_III_of_Bavaria
    source: Prince_Henry_of_Bavaria
    relation: :hasFather
  Finish (c7a55aa1-1d07-4e25-bf3a-4dc45a5564a9)
 Call ID: c7a55aa1-1d07-4e25-bf3a-4dc45a5564a9
  Args: