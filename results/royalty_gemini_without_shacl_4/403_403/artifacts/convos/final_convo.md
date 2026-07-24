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
Princess Feodora of Saxe-Meiningen (Feodora Karola Charlotte Marie Adelheid Auguste Mathilde; 29 May 1890 – 12 March 1972) was the eldest child of Prince Friedrich Johann of Saxe-Meiningen, a younger son of Georg II, Duke of Saxe-Meiningen, and Countess Adelaide of Lippe-Biesterfeld, a daughter of Ernst, Count of Lippe-Biesterfeld.
By marriage, she was known as Grand Duchess of Saxe-Weimar-Eisenach.
Biography

Marriage

During a summer visit to the palace Wilhelmshöhe, Feodora was urged by her kinsman Emperor Wilhelm II to make a match with the widowed Wilhelm Ernst, Grand Duke of Saxe-Weimar-Eisenach.
This was seen by many to be due to mutual ill will between Wilhelm and Feodora's grandfather Georg II, Duke of Saxe-Meiningen, whose morganatic wedding to Ellen Franz had displeased many royal personages like Wilhelm.
Wilhelm's disapproval was even more surprising in that he had recently allowed the marriage between a Hohenzollern dynast (Prince Frederick William of Prussia) with a much lower-ranked member of the nobility (Princess Agatha of Hohenlohe-Schillingsfürst); it was considered odd that he refused to recognize one equal marriage yet acknowledged another lesser match, especially when the latter was within his own family and subject to the rigid Hohenzollern house laws.
The Emperor's boycott of the wedding was so strongly resented in Saxe-Meiningen that, when newspapers announced that Wilhelm would not be attending the wedding, the official communication from the royal palace declared that he had never been invited.
On 14 January 1910 in Meiningen, Feodora was married to Wilhelm Ernst.
She was his second wife (his first wife Princess Caroline Reuss, Elder Line had died childless after eighteen months of marriage in 1905).
Court life


Feodora's marriage was unhappy; the Weimar court was generally considered to be one of the most stifling and etiquette-driven in Germany.
Feodora was unhappy in such an environment; at the age of 23, reports leaked out that she was staying at a sanatorium for her health.
Feodora was very popular among the middle and lower classes of Weimar; this was largely attributed to her charm and kindness to the poor and suffering.
Feodora died on 12 March 1972 in Freiburg
Issue

Feodora and her husband had four children:


Ancestry

References



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
  AssignClass (8b580d89-c541-4952-9695-b3342b3e1d19)
 Call ID: 8b580d89-c541-4952-9695-b3342b3e1d19
  Args:
    type: :Woman
    source: Feodora_of_Saxe-Meiningen
  AssignClass (7be8e73b-2561-4ceb-b13b-44db20d65ca7)
 Call ID: 7be8e73b-2561-4ceb-b13b-44db20d65ca7
  Args:
    type: :Person
    source: Feodora_of_Saxe-Meiningen
  AddLiteral (3fab5f19-c14a-4a31-88ec-d4bffbf1a69e)
 Call ID: 3fab5f19-c14a-4a31-88ec-d4bffbf1a69e
  Args:
    literal_type: xsd:integer
    literal_value: 1890
    relation: :hasBirthYear
    source: Feodora_of_Saxe-Meiningen
  AddLiteral (46b6d5ab-2668-48eb-b679-52308f08fa21)
 Call ID: 46b6d5ab-2668-48eb-b679-52308f08fa21
  Args:
    literal_value: 1972
    literal_type: xsd:integer
    source: Feodora_of_Saxe-Meiningen
    relation: :hasDeathYear
  AddLiteral (d2d42f88-f599-49a1-9026-8d0039bdfcbd)
 Call ID: d2d42f88-f599-49a1-9026-8d0039bdfcbd
  Args:
    relation: :alsoKnownAs
    source: Feodora_of_Saxe-Meiningen
    literal_type: xsd:string
    literal_value: Grand Duchess of Saxe-Weimar-Eisenach
  AssignClass (91498acb-0b3d-46c2-bbbb-b07e008918c1)
 Call ID: 91498acb-0b3d-46c2-bbbb-b07e008918c1
  Args:
    type: :Man
    source: Friedrich_Johann_of_Saxe-Meiningen
  AssignClass (7eef4033-8c8d-4322-b301-ccb347fb541b)
 Call ID: 7eef4033-8c8d-4322-b301-ccb347fb541b
  Args:
    type: :Person
    source: Friedrich_Johann_of_Saxe-Meiningen
  AssignClass (e8f26f4e-ca0d-40fd-bd6b-06eeed758b6b)
 Call ID: e8f26f4e-ca0d-40fd-bd6b-06eeed758b6b
  Args:
    type: :Ancestor
    source: Friedrich_Johann_of_Saxe-Meiningen
  AddTriple (2cc797af-9da8-483d-9929-f1b9fa33fba6)
 Call ID: 2cc797af-9da8-483d-9929-f1b9fa33fba6
  Args:
    target: Friedrich_Johann_of_Saxe-Meiningen
    relation: :hasFather
    source: Feodora_of_Saxe-Meiningen
  AssignClass (5cf62c55-4197-40ab-8d96-6dcd78c51c5a)
 Call ID: 5cf62c55-4197-40ab-8d96-6dcd78c51c5a
  Args:
    type: :Man
    source: Georg_II_Duke_of_Saxe-Meiningen
  AssignClass (c26ee7e5-8ddf-4d7d-a910-7ed466bcd4ba)
 Call ID: c26ee7e5-8ddf-4d7d-a910-7ed466bcd4ba
  Args:
    type: :Person
    source: Georg_II_Duke_of_Saxe-Meiningen
  AssignClass (2f5e7a05-2a14-4e95-afca-ab4964159513)
 Call ID: 2f5e7a05-2a14-4e95-afca-ab4964159513
  Args:
    type: :Ancestor
    source: Georg_II_Duke_of_Saxe-Meiningen
  AddTriple (5f850f00-7b47-49c1-acad-ea314ff9b130)
 Call ID: 5f850f00-7b47-49c1-acad-ea314ff9b130
  Args:
    target: Georg_II_Duke_of_Saxe-Meiningen
    relation: :hasFather
    source: Friedrich_Johann_of_Saxe-Meiningen
  AssignClass (e524766f-62e9-48db-a5a5-5710b2c6635f)
 Call ID: e524766f-62e9-48db-a5a5-5710b2c6635f
  Args:
    type: :Woman
    source: Adelaide_of_Lippe-Biesterfeld
  AssignClass (352fca9f-d907-4a21-9805-1cafd828b92e)
 Call ID: 352fca9f-d907-4a21-9805-1cafd828b92e
  Args:
    type: :Person
    source: Adelaide_of_Lippe-Biesterfeld
  AssignClass (6ca256d2-265d-497e-bf25-061c6fc91e2a)
 Call ID: 6ca256d2-265d-497e-bf25-061c6fc91e2a
  Args:
    type: :Ancestor
    source: Adelaide_of_Lippe-Biesterfeld
  AddTriple (52b47315-8ea5-4884-92a0-a6b670aa7ea0)
 Call ID: 52b47315-8ea5-4884-92a0-a6b670aa7ea0
  Args:
    target: Adelaide_of_Lippe-Biesterfeld
    relation: :hasMother
    source: Feodora_of_Saxe-Meiningen
  AssignClass (6ada1b96-e430-4ec8-9c0b-9e1efa84178f)
 Call ID: 6ada1b96-e430-4ec8-9c0b-9e1efa84178f
  Args:
    type: :Man
    source: Ernst_Count_of_Lippe-Biesterfeld
  AssignClass (ed1ebfa7-561d-412a-94d1-f6136783bc0e)
 Call ID: ed1ebfa7-561d-412a-94d1-f6136783bc0e
  Args:
    type: :Person
    source: Ernst_Count_of_Lippe-Biesterfeld
  AssignClass (17a5be25-dbe4-43d3-80ce-edf626f7fbba)
 Call ID: 17a5be25-dbe4-43d3-80ce-edf626f7fbba
  Args:
    type: :Ancestor
    source: Ernst_Count_of_Lippe-Biesterfeld
  AddTriple (9323e574-29b2-4d1e-ab20-457d058d5a5d)
 Call ID: 9323e574-29b2-4d1e-ab20-457d058d5a5d
  Args:
    target: Ernst_Count_of_Lippe-Biesterfeld
    source: Adelaide_of_Lippe-Biesterfeld
    relation: :hasFather
  AssignClass (72843769-0fef-499d-9c14-2c864d7b8901)
 Call ID: 72843769-0fef-499d-9c14-2c864d7b8901
  Args:
    type: :Man
    source: Wilhelm_Ernst_Grand_Duke_of_Saxe-Weimar-Eisenach
  AssignClass (a64a0686-df53-4243-b4cb-16715e0f29b7)
 Call ID: a64a0686-df53-4243-b4cb-16715e0f29b7
  Args:
    type: :Person
    source: Wilhelm_Ernst_Grand_Duke_of_Saxe-Weimar-Eisenach
  AddLiteral (2d64bc9e-7880-4bd6-9b4b-2ec837e33cff)
 Call ID: 2d64bc9e-7880-4bd6-9b4b-2ec837e33cff
  Args:
    literal_value: 1910
    literal_type: xsd:integer
    source: Feodora_of_Saxe-Meiningen
    relation: :hasMarriageYear
  AddTriple (35825ea3-68ed-4090-aba3-1549808ec4fd)
 Call ID: 35825ea3-68ed-4090-aba3-1549808ec4fd
  Args:
    target: Wilhelm_Ernst_Grand_Duke_of_Saxe-Weimar-Eisenach
    relation: :hasRelation
    source: Feodora_of_Saxe-Meiningen
  AssignClass (6bc8b3bd-9a89-42d7-9b3a-e108eda0afd1)
 Call ID: 6bc8b3bd-9a89-42d7-9b3a-e108eda0afd1
  Args:
    type: :Woman
    source: Caroline_Reuss_Elder_Line
  AssignClass (a14e815d-e598-49ea-afa9-79bbca8667bc)
 Call ID: a14e815d-e598-49ea-afa9-79bbca8667bc
  Args:
    type: :Person
    source: Caroline_Reuss_Elder_Line
  AddTriple (263b52ca-23f7-4e15-8072-f9418a33574a)
 Call ID: 263b52ca-23f7-4e15-8072-f9418a33574a
  Args:
    target: Caroline_Reuss_Elder_Line
    relation: :hasRelation
    source: Wilhelm_Ernst_Grand_Duke_of_Saxe-Weimar-Eisenach
  Finish (7f7ad103-d32e-43ac-aba9-841b7a2bef43)
 Call ID: 7f7ad103-d32e-43ac-aba9-841b7a2bef43
  Args: