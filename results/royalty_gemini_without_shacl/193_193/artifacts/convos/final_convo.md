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
  AssignClass (bd76532c-e715-4ea4-a4c9-dbf35e76c60a)
 Call ID: bd76532c-e715-4ea4-a4c9-dbf35e76c60a
  Args:
    type: :Person
    source: :Adelaide_of_Saxe-Meiningen
  AssignClass (942ef936-f3f2-4291-a287-32b3a48d027f)
 Call ID: 942ef936-f3f2-4291-a287-32b3a48d027f
  Args:
    type: :Woman
    source: :Adelaide_of_Saxe-Meiningen
  AddLiteral (b0b6d04c-eac4-4875-b8df-c24e0b6c34db)
 Call ID: b0b6d04c-eac4-4875-b8df-c24e0b6c34db
  Args:
    literal_type: xsd:integer
    literal_value: 1891
    relation: :hasBirthYear
    source: :Adelaide_of_Saxe-Meiningen
  AddLiteral (debc9c85-8c85-4e40-9657-4c7cb85822ab)
 Call ID: debc9c85-8c85-4e40-9657-4c7cb85822ab
  Args:
    source: :Adelaide_of_Saxe-Meiningen
    relation: :hasDeathYear
    literal_value: 1971
    literal_type: xsd:integer
  AddLiteral (a3201cb5-aea7-4413-a5c8-9b241d05d8db)
 Call ID: a3201cb5-aea7-4413-a5c8-9b241d05d8db
  Args:
    source: :Adelaide_of_Saxe-Meiningen
    relation: :alsoKnownAs
    literal_value: Adelaide Erna Caroline Marie Elisabeth
    literal_type: xsd:string
  AddLiteral (ab8f00e2-4dc9-4aa8-b040-d411d73bf477)
 Call ID: ab8f00e2-4dc9-4aa8-b040-d411d73bf477
  Args:
    literal_value: Adelheid
    relation: :alsoKnownAs
    literal_type: xsd:string
    source: :Adelaide_of_Saxe-Meiningen
  AssignClass (90c8ad3b-76ad-494d-8862-123942add2e2)
 Call ID: 90c8ad3b-76ad-494d-8862-123942add2e2
  Args:
    type: :Person
    source: :Prince_Frederick_John_of_Saxe-Meiningen
  AssignClass (64fb9c4b-07c7-4589-9a9f-27bff95980e2)
 Call ID: 64fb9c4b-07c7-4589-9a9f-27bff95980e2
  Args:
    type: :Man
    source: :Prince_Frederick_John_of_Saxe-Meiningen
  AddTriple (db6c0032-7c99-431d-bb7e-89dd396b6a38)
 Call ID: db6c0032-7c99-431d-bb7e-89dd396b6a38
  Args:
    target: :Prince_Frederick_John_of_Saxe-Meiningen
    relation: :hasFather
    source: :Adelaide_of_Saxe-Meiningen
  AddLiteral (da152c99-fe8e-4fe2-9f5a-7545bb7bd89a)
 Call ID: da152c99-fe8e-4fe2-9f5a-7545bb7bd89a
  Args:
    literal_type: xsd:integer
    literal_value: 1914
    relation: :hasDeathYear
    source: :Prince_Frederick_John_of_Saxe-Meiningen
  AssignClass (fb52a7c6-63a9-4e53-aeec-643b05fb685c)
 Call ID: fb52a7c6-63a9-4e53-aeec-643b05fb685c
  Args:
    source: :Countess_Adelaide_of_Lippe-Biesterfeld
    type: :Person
  AssignClass (cad8fb21-306c-4579-b681-e657d5512476)
 Call ID: cad8fb21-306c-4579-b681-e657d5512476
  Args:
    source: :Countess_Adelaide_of_Lippe-Biesterfeld
    type: :Woman
  AddTriple (5d18ccd3-e625-4017-993d-14bab2cc8869)
 Call ID: 5d18ccd3-e625-4017-993d-14bab2cc8869
  Args:
    source: :Adelaide_of_Saxe-Meiningen
    target: :Countess_Adelaide_of_Lippe-Biesterfeld
    relation: :hasMother
  AssignClass (0c1359cc-7b61-4ddf-8256-4073886b4a0f)
 Call ID: 0c1359cc-7b61-4ddf-8256-4073886b4a0f
  Args:
    type: :Person
    source: :George_II_of_Saxe-Meiningen
  AssignClass (dcb93cc0-1380-4fbb-be38-70ae88da6579)
 Call ID: dcb93cc0-1380-4fbb-be38-70ae88da6579
  Args:
    type: :Man
    source: :George_II_of_Saxe-Meiningen
  AddTriple (72b363b4-47ef-4d92-bab3-16478ff15853)
 Call ID: 72b363b4-47ef-4d92-bab3-16478ff15853
  Args:
    target: :George_II_of_Saxe-Meiningen
    relation: :hasFather
    source: :Prince_Frederick_John_of_Saxe-Meiningen
  AssignClass (5246a5d9-9054-45d9-9663-1d2f23ae2acc)
 Call ID: 5246a5d9-9054-45d9-9663-1d2f23ae2acc
  Args:
    source: :Feodora_of_Hohenlohe-Langenburg
    type: :Person
  AssignClass (08afc9d8-04a9-4218-b1b6-3f5029596ca7)
 Call ID: 08afc9d8-04a9-4218-b1b6-3f5029596ca7
  Args:
    type: :Woman
    source: :Feodora_of_Hohenlohe-Langenburg
  AddTriple (df8d0c06-da3b-4486-96e5-3f81ae871d13)
 Call ID: df8d0c06-da3b-4486-96e5-3f81ae871d13
  Args:
    relation: :hasMother
    target: :Feodora_of_Hohenlohe-Langenburg
    source: :Prince_Frederick_John_of_Saxe-Meiningen
  AssignClass (ccfd2c04-6814-4ef6-8168-ce8ff1e49b41)
 Call ID: ccfd2c04-6814-4ef6-8168-ce8ff1e49b41
  Args:
    type: :Person
    source: :Prince_George
  AssignClass (f58322fa-838d-48aa-a834-8eb42b67c60d)
 Call ID: f58322fa-838d-48aa-a834-8eb42b67c60d
  Args:
    type: :Man
    source: :Prince_George
  AddTriple (977ea8e6-1dcb-4045-b549-506722dc45d8)
 Call ID: 977ea8e6-1dcb-4045-b549-506722dc45d8
  Args:
    source: :Adelaide_of_Saxe-Meiningen
    relation: :isSiblingOf
    target: :Prince_George
  AssignClass (3f1eb066-f97c-4aea-8881-ceb5eb609abf)
 Call ID: 3f1eb066-f97c-4aea-8881-ceb5eb609abf
  Args:
    source: :Prince_Bernard
    type: :Person
  AssignClass (27ddb642-9770-4028-a4ab-5c5f9591801c)
 Call ID: 27ddb642-9770-4028-a4ab-5c5f9591801c
  Args:
    type: :Man
    source: :Prince_Bernard
  AddTriple (d45b4071-eb48-48f6-91bd-ae39fad4aca8)
 Call ID: d45b4071-eb48-48f6-91bd-ae39fad4aca8
  Args:
    source: :Adelaide_of_Saxe-Meiningen
    target: :Prince_Bernard
    relation: :isSiblingOf
  AssignClass (0ac73d45-6ac0-4893-bc0c-f3adade3e4ee)
 Call ID: 0ac73d45-6ac0-4893-bc0c-f3adade3e4ee
  Args:
    type: :Person
    source: :Ernst_Count_of_Lippe-Biesterfeld
  AssignClass (3c7fb1e3-b0d7-4f04-9688-655a3b4f7250)
 Call ID: 3c7fb1e3-b0d7-4f04-9688-655a3b4f7250
  Args:
    type: :Man
    source: :Ernst_Count_of_Lippe-Biesterfeld
  AddTriple (3c8e3b36-f2d7-4d7e-aeec-dd846c82499f)
 Call ID: 3c8e3b36-f2d7-4d7e-aeec-dd846c82499f
  Args:
    source: :Countess_Adelaide_of_Lippe-Biesterfeld
    relation: :hasFather
    target: :Ernst_Count_of_Lippe-Biesterfeld
  AssignClass (1251e6f7-1445-4f6d-8d3b-5b01f9b22da2)
 Call ID: 1251e6f7-1445-4f6d-8d3b-5b01f9b22da2
  Args:
    type: :Person
    source: :Prince_Adalbert_of_Prussia
  AssignClass (f185b294-2642-41d0-acf4-fb0158695385)
 Call ID: f185b294-2642-41d0-acf4-fb0158695385
  Args:
    source: :Prince_Adalbert_of_Prussia
    type: :Man
  AddTriple (45b62613-2156-44d5-8475-a6e991c8ef3b)
 Call ID: 45b62613-2156-44d5-8475-a6e991c8ef3b
  Args:
    source: :Adelaide_of_Saxe-Meiningen
    relation: :hasRelation
    target: :Prince_Adalbert_of_Prussia
  AddLiteral (121b7969-8881-4107-b3a8-1fed26e94e42)
 Call ID: 121b7969-8881-4107-b3a8-1fed26e94e42
  Args:
    source: :Adelaide_of_Saxe-Meiningen
    literal_type: xsd:integer
    literal_value: 1914
    relation: :hasMarriageYear
  AssignClass (60a29eac-4fe6-467b-ae3f-62931cffb705)
 Call ID: 60a29eac-4fe6-467b-ae3f-62931cffb705
  Args:
    source: :Kaiser_William_II_of_Germany
    type: :Person
  AssignClass (2143c3c4-fbd2-42cd-aadb-1ee5ba055a42)
 Call ID: 2143c3c4-fbd2-42cd-aadb-1ee5ba055a42
  Args:
    source: :Kaiser_William_II_of_Germany
    type: :Man
  AddTriple (840592e8-6024-4b22-8160-2cf7acc75cf7)
 Call ID: 840592e8-6024-4b22-8160-2cf7acc75cf7
  Args:
    relation: :hasFather
    target: :Kaiser_William_II_of_Germany
    source: :Prince_Adalbert_of_Prussia
  AssignClass (68d90be4-be20-431a-b625-5b1626ef1f78)
 Call ID: 68d90be4-be20-431a-b625-5b1626ef1f78
  Args:
    type: :Person
    source: :Prince_Henry_of_Bavaria
  AssignClass (f48d2167-106a-475f-8b0f-60b28e8adac9)
 Call ID: f48d2167-106a-475f-8b0f-60b28e8adac9
  Args:
    type: :Man
    source: :Prince_Henry_of_Bavaria
  AssignClass (663c9e56-2701-4158-b27d-05aceb5e686f)
 Call ID: 663c9e56-2701-4158-b27d-05aceb5e686f
  Args:
    source: :Ludwig_III_of_Bavaria
    type: :Person
  AssignClass (12697abd-e503-4f40-8ca1-b2aca1cf3a6f)
 Call ID: 12697abd-e503-4f40-8ca1-b2aca1cf3a6f
  Args:
    source: :Ludwig_III_of_Bavaria
    type: :Man
  AddTriple (63526e17-c27c-4cb2-a4b5-bb0c82a244bf)
 Call ID: 63526e17-c27c-4cb2-a4b5-bb0c82a244bf
  Args:
    source: :Prince_Henry_of_Bavaria
    relation: :hasFather
    target: :Ludwig_III_of_Bavaria
  Finish (765b9d9f-d266-4128-9cdb-f33b92abda36)
 Call ID: 765b9d9f-d266-4128-9cdb-f33b92abda36
  Args: