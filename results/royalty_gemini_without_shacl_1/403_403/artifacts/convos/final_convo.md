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
  AssignClass (2d38c444-9a8b-4ef4-ba44-d7b46e063832)
 Call ID: 2d38c444-9a8b-4ef4-ba44-d7b46e063832
  Args:
    type: :Woman
    source: Princess_Feodora_of_Saxe-Meiningen
  AssignClass (28b1082c-4202-463e-bedf-fb6f6601fb1e)
 Call ID: 28b1082c-4202-463e-bedf-fb6f6601fb1e
  Args:
    type: :Person
    source: Princess_Feodora_of_Saxe-Meiningen
  AddLiteral (cbe97bec-ee91-4a9d-a49b-c36d49330041)
 Call ID: cbe97bec-ee91-4a9d-a49b-c36d49330041
  Args:
    relation: :alsoKnownAs
    literal_value: Feodora Karola Charlotte Marie Adelheid Auguste Mathilde
    source: Princess_Feodora_of_Saxe-Meiningen
    literal_type: xsd:string
  AddLiteral (3eb76819-ee3c-4c24-bdf7-bd9295862567)
 Call ID: 3eb76819-ee3c-4c24-bdf7-bd9295862567
  Args:
    literal_type: xsd:integer
    source: Princess_Feodora_of_Saxe-Meiningen
    literal_value: 1890
    relation: :hasBirthYear
  AddLiteral (84b3d2ac-5b96-4dfb-832d-b63cdc4c86a3)
 Call ID: 84b3d2ac-5b96-4dfb-832d-b63cdc4c86a3
  Args:
    literal_type: xsd:integer
    literal_value: 1972
    relation: :hasDeathYear
    source: Princess_Feodora_of_Saxe-Meiningen
  AddLiteral (ad847606-c8ef-40d4-9c32-2836dde3f3ca)
 Call ID: ad847606-c8ef-40d4-9c32-2836dde3f3ca
  Args:
    source: Princess_Feodora_of_Saxe-Meiningen
    literal_value: Grand Duchess of Saxe-Weimar-Eisenach
    relation: :knownAs
    literal_type: xsd:string
  AssignClass (0928ee23-42ed-4d9a-ad30-bd8d0fbee000)
 Call ID: 0928ee23-42ed-4d9a-ad30-bd8d0fbee000
  Args:
    type: :Man
    source: Prince_Friedrich_Johann_of_Saxe-Meiningen
  AssignClass (26b61a42-a60e-45ce-9e9d-406750c88e82)
 Call ID: 26b61a42-a60e-45ce-9e9d-406750c88e82
  Args:
    type: :Person
    source: Prince_Friedrich_Johann_of_Saxe-Meiningen
  AddTriple (f152602b-63dc-4865-9cb7-22e7c5332aba)
 Call ID: f152602b-63dc-4865-9cb7-22e7c5332aba
  Args:
    target: Prince_Friedrich_Johann_of_Saxe-Meiningen
    source: Princess_Feodora_of_Saxe-Meiningen
    relation: :hasFather
  AssignClass (3c9d0d77-8169-46ac-96d0-9cfac6aa2c4e)
 Call ID: 3c9d0d77-8169-46ac-96d0-9cfac6aa2c4e
  Args:
    type: :Man
    source: Georg_II_Duke_of_Saxe-Meiningen
  AssignClass (cf472188-af70-4ed8-9f27-ec2d04c00508)
 Call ID: cf472188-af70-4ed8-9f27-ec2d04c00508
  Args:
    type: :Person
    source: Georg_II_Duke_of_Saxe-Meiningen
  AddTriple (a254fff9-d0da-4f6d-8cb3-4b07bf2daea2)
 Call ID: a254fff9-d0da-4f6d-8cb3-4b07bf2daea2
  Args:
    target: Georg_II_Duke_of_Saxe-Meiningen
    source: Prince_Friedrich_Johann_of_Saxe-Meiningen
    relation: :hasFather
  AssignClass (585c6245-9500-4e1c-a7be-bdecf254bd1c)
 Call ID: 585c6245-9500-4e1c-a7be-bdecf254bd1c
  Args:
    type: :Woman
    source: Countess_Adelaide_of_Lippe-Biesterfeld
  AssignClass (642881ca-5d38-4160-b657-0c9bf1dece84)
 Call ID: 642881ca-5d38-4160-b657-0c9bf1dece84
  Args:
    type: :Person
    source: Countess_Adelaide_of_Lippe-Biesterfeld
  AddTriple (3a9dc9a3-751e-4a57-870c-3d787b64b365)
 Call ID: 3a9dc9a3-751e-4a57-870c-3d787b64b365
  Args:
    target: Countess_Adelaide_of_Lippe-Biesterfeld
    relation: :hasMother
    source: Princess_Feodora_of_Saxe-Meiningen
  AssignClass (2f90335f-f08a-477a-9e22-f1b5de5cd464)
 Call ID: 2f90335f-f08a-477a-9e22-f1b5de5cd464
  Args:
    type: :Man
    source: Ernst_Count_of_Lippe-Biesterfeld
  AssignClass (3fa143cd-0395-4a7e-8624-069ffe4de92e)
 Call ID: 3fa143cd-0395-4a7e-8624-069ffe4de92e
  Args:
    type: :Person
    source: Ernst_Count_of_Lippe-Biesterfeld
  AddTriple (8fab07b6-829a-4c55-a080-85e5bc427048)
 Call ID: 8fab07b6-829a-4c55-a080-85e5bc427048
  Args:
    source: Countess_Adelaide_of_Lippe-Biesterfeld
    relation: :hasFather
    target: Ernst_Count_of_Lippe-Biesterfeld
  AssignClass (59450a67-def9-4eb5-bc4a-1b9d3e82753b)
 Call ID: 59450a67-def9-4eb5-bc4a-1b9d3e82753b
  Args:
    type: :Man
    source: Wilhelm_Ernst_Grand_Duke_of_Saxe-Weimar-Eisenach
  AssignClass (1e18a58e-9fa5-4d79-acc6-06ec89f36213)
 Call ID: 1e18a58e-9fa5-4d79-acc6-06ec89f36213
  Args:
    type: :Person
    source: Wilhelm_Ernst_Grand_Duke_of_Saxe-Weimar-Eisenach
  AddLiteral (bb8980cf-f2d1-414f-ab71-33b7cc9efe74)
 Call ID: bb8980cf-f2d1-414f-ab71-33b7cc9efe74
  Args:
    source: Princess_Feodora_of_Saxe-Meiningen
    literal_value: 1910
    relation: :hasMarriageYear
    literal_type: xsd:integer
  AddTriple (30e2de6f-898d-4158-bd40-5240503f1fca)
 Call ID: 30e2de6f-898d-4158-bd40-5240503f1fca
  Args:
    relation: :hasRelation
    source: Princess_Feodora_of_Saxe-Meiningen
    target: Wilhelm_Ernst_Grand_Duke_of_Saxe-Weimar-Eisenach
  AssignClass (4d6e148e-a345-4c66-a43a-7fd975cbe59c)
 Call ID: 4d6e148e-a345-4c66-a43a-7fd975cbe59c
  Args:
    type: :Woman
    source: Princess_Caroline_Reuss_Elder_Line
  AssignClass (16a4b071-2fea-4ffa-b726-9398a435c5f4)
 Call ID: 16a4b071-2fea-4ffa-b726-9398a435c5f4
  Args:
    type: :Person
    source: Princess_Caroline_Reuss_Elder_Line
  AddTriple (85abc69e-3a46-469d-9c7f-2cfec30c413b)
 Call ID: 85abc69e-3a46-469d-9c7f-2cfec30c413b
  Args:
    source: Wilhelm_Ernst_Grand_Duke_of_Saxe-Weimar-Eisenach
    relation: :hasRelation
    target: Princess_Caroline_Reuss_Elder_Line
  AssignClass (7f8fffc3-cc3d-4033-9619-fa96b6447a33)
 Call ID: 7f8fffc3-cc3d-4033-9619-fa96b6447a33
  Args:
    type: :Woman
    source: Ellen_Franz
  AssignClass (8c07a754-a287-4ff8-8eff-86f5268a6258)
 Call ID: 8c07a754-a287-4ff8-8eff-86f5268a6258
  Args:
    type: :Person
    source: Ellen_Franz
  AddTriple (47766820-dee3-4656-9aca-8c82edd18481)
 Call ID: 47766820-dee3-4656-9aca-8c82edd18481
  Args:
    source: Georg_II_Duke_of_Saxe-Meiningen
    relation: :hasRelation
    target: Ellen_Franz
  AssignClass (11d9c8bc-6ba1-4a6b-9fa1-ed07cbe97225)
 Call ID: 11d9c8bc-6ba1-4a6b-9fa1-ed07cbe97225
  Args:
    type: :Man
    source: Prince_Frederick_William_of_Prussia
  AssignClass (2a334004-1e2a-46b6-939a-c0bfe84cb15b)
 Call ID: 2a334004-1e2a-46b6-939a-c0bfe84cb15b
  Args:
    type: :Person
    source: Prince_Frederick_William_of_Prussia
  AssignClass (838805c6-6631-4477-b090-8ed27ec3da70)
 Call ID: 838805c6-6631-4477-b090-8ed27ec3da70
  Args:
    type: :Woman
    source: Princess_Agatha_of_Hohenlohe-Schillingsfürst
  AssignClass (2fdd1fcc-39ab-492c-be9e-9f2f038cdaf9)
 Call ID: 2fdd1fcc-39ab-492c-be9e-9f2f038cdaf9
  Args:
    type: :Person
    source: Princess_Agatha_of_Hohenlohe-Schillingsfürst
  AddTriple (e1f4c07e-8f22-4330-af2d-e52cdf1c70ef)
 Call ID: e1f4c07e-8f22-4330-af2d-e52cdf1c70ef
  Args:
    target: Princess_Agatha_of_Hohenlohe-Schillingsfürst
    relation: :hasRelation
    source: Prince_Frederick_William_of_Prussia
  Finish (68b468bb-8360-4fad-95cf-dc0320bf32a5)
 Call ID: 68b468bb-8360-4fad-95cf-dc0320bf32a5
  Args: