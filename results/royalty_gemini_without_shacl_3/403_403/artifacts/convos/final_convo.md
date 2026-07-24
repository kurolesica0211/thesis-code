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
  AssignClass (cb9ce630-9225-4cd1-a7c3-1d7ed0210025)
 Call ID: cb9ce630-9225-4cd1-a7c3-1d7ed0210025
  Args:
    source: Feodora_of_Saxe-Meiningen
    type: :Woman
  AssignClass (d4dd6cd8-5db7-458a-a6a3-5ac6997f663f)
 Call ID: d4dd6cd8-5db7-458a-a6a3-5ac6997f663f
  Args:
    type: :Person
    source: Feodora_of_Saxe-Meiningen
  AddLiteral (d3269e55-8b0b-4d5f-8426-ae800bb3b415)
 Call ID: d3269e55-8b0b-4d5f-8426-ae800bb3b415
  Args:
    literal_value: 1890
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Feodora_of_Saxe-Meiningen
  AddLiteral (15eaef33-8e4b-4fe6-931d-e89d73dd66d6)
 Call ID: 15eaef33-8e4b-4fe6-931d-e89d73dd66d6
  Args:
    literal_type: xsd:integer
    literal_value: 1972
    source: Feodora_of_Saxe-Meiningen
    relation: :hasDeathYear
  AddLiteral (57e9dcd9-76e5-4449-a192-aee8194bab54)
 Call ID: 57e9dcd9-76e5-4449-a192-aee8194bab54
  Args:
    literal_value: Grand Duchess of Saxe-Weimar-Eisenach
    literal_type: xsd:string
    relation: :knownAs
    source: Feodora_of_Saxe-Meiningen
  AssignClass (7795b7c0-18d4-4b89-bce4-38d799e61072)
 Call ID: 7795b7c0-18d4-4b89-bce4-38d799e61072
  Args:
    source: Friedrich_Johann_of_Saxe-Meiningen
    type: :Man
  AssignClass (ff926e15-2f6f-428d-a565-7bc6937ba9a8)
 Call ID: ff926e15-2f6f-428d-a565-7bc6937ba9a8
  Args:
    type: :Person
    source: Friedrich_Johann_of_Saxe-Meiningen
  AddTriple (69d6f78b-ab79-47be-8ae0-982af5d51e28)
 Call ID: 69d6f78b-ab79-47be-8ae0-982af5d51e28
  Args:
    relation: :hasFather
    target: Friedrich_Johann_of_Saxe-Meiningen
    source: Feodora_of_Saxe-Meiningen
  AssignClass (c9723ec0-9401-48ef-87e1-75a127eb043c)
 Call ID: c9723ec0-9401-48ef-87e1-75a127eb043c
  Args:
    type: :Man
    source: Georg_II_Duke_of_Saxe-Meiningen
  AssignClass (009b06e1-b2fa-4654-8dcf-69c1837864a5)
 Call ID: 009b06e1-b2fa-4654-8dcf-69c1837864a5
  Args:
    type: :Person
    source: Georg_II_Duke_of_Saxe-Meiningen
  AddTriple (00a99e1a-b293-4579-8a93-646288b3df48)
 Call ID: 00a99e1a-b293-4579-8a93-646288b3df48
  Args:
    source: Friedrich_Johann_of_Saxe-Meiningen
    relation: :hasFather
    target: Georg_II_Duke_of_Saxe-Meiningen
  AssignClass (21cf735b-88f6-4a0c-8273-f64e81bd39d9)
 Call ID: 21cf735b-88f6-4a0c-8273-f64e81bd39d9
  Args:
    type: :Woman
    source: Adelaide_of_Lippe-Biesterfeld
  AssignClass (e17610fc-d42d-498d-8790-c0de9515cf2d)
 Call ID: e17610fc-d42d-498d-8790-c0de9515cf2d
  Args:
    type: :Person
    source: Adelaide_of_Lippe-Biesterfeld
  AddTriple (cf4a41d5-5e33-46a9-80a1-1b94aadb2bfd)
 Call ID: cf4a41d5-5e33-46a9-80a1-1b94aadb2bfd
  Args:
    relation: :hasMother
    target: Adelaide_of_Lippe-Biesterfeld
    source: Feodora_of_Saxe-Meiningen
  AssignClass (b4f4b6ca-f53b-49b9-9d00-789f2e20827f)
 Call ID: b4f4b6ca-f53b-49b9-9d00-789f2e20827f
  Args:
    type: :Man
    source: Ernst_Count_of_Lippe-Biesterfeld
  AssignClass (799f9368-a919-400c-b7c7-e371b28971cf)
 Call ID: 799f9368-a919-400c-b7c7-e371b28971cf
  Args:
    type: :Person
    source: Ernst_Count_of_Lippe-Biesterfeld
  AddTriple (8cfa1e80-6e72-47da-939d-4ab4c16b9334)
 Call ID: 8cfa1e80-6e72-47da-939d-4ab4c16b9334
  Args:
    target: Ernst_Count_of_Lippe-Biesterfeld
    relation: :hasFather
    source: Adelaide_of_Lippe-Biesterfeld
  AssignClass (8d1ccc0b-52c5-41e7-96f3-48f1cdf34eac)
 Call ID: 8d1ccc0b-52c5-41e7-96f3-48f1cdf34eac
  Args:
    type: :Man
    source: Wilhelm_Ernst_Grand_Duke_of_Saxe-Weimar-Eisenach
  AssignClass (90253f86-af54-4128-b508-7a15eeb8c09a)
 Call ID: 90253f86-af54-4128-b508-7a15eeb8c09a
  Args:
    source: Wilhelm_Ernst_Grand_Duke_of_Saxe-Weimar-Eisenach
    type: :Person
  AddLiteral (8e4a934b-1e6e-4800-81be-e7c4034ae408)
 Call ID: 8e4a934b-1e6e-4800-81be-e7c4034ae408
  Args:
    source: Feodora_of_Saxe-Meiningen
    relation: :hasMarriageYear
    literal_value: 1910
    literal_type: xsd:integer
  AddTriple (7ec431bb-8d76-44b0-9b5a-9f7f6dfb07d6)
 Call ID: 7ec431bb-8d76-44b0-9b5a-9f7f6dfb07d6
  Args:
    source: Feodora_of_Saxe-Meiningen
    relation: :hasRelation
    target: Wilhelm_Ernst_Grand_Duke_of_Saxe-Weimar-Eisenach
  AssignClass (bc053fc7-f36f-4de1-a40a-23f212016dbd)
 Call ID: bc053fc7-f36f-4de1-a40a-23f212016dbd
  Args:
    source: Caroline_Reuss_Elder_Line
    type: :Woman
  AssignClass (c5048704-49d8-490c-af70-3a400dcaa835)
 Call ID: c5048704-49d8-490c-af70-3a400dcaa835
  Args:
    type: :Person
    source: Caroline_Reuss_Elder_Line
  AddTriple (5992326f-fab9-4282-acc8-654a2e363a4c)
 Call ID: 5992326f-fab9-4282-acc8-654a2e363a4c
  Args:
    relation: :hasRelation
    target: Caroline_Reuss_Elder_Line
    source: Wilhelm_Ernst_Grand_Duke_of_Saxe-Weimar-Eisenach
  AssignClass (26ec228b-470b-43b1-857b-7954832e905b)
 Call ID: 26ec228b-470b-43b1-857b-7954832e905b
  Args:
    source: Ellen_Franz
    type: :Woman
  AssignClass (1f34e30e-5284-41cb-9c60-81ac971c20e7)
 Call ID: 1f34e30e-5284-41cb-9c60-81ac971c20e7
  Args:
    source: Ellen_Franz
    type: :Person
  AddTriple (810c78c3-3964-46c0-b0dd-116875fd0dc6)
 Call ID: 810c78c3-3964-46c0-b0dd-116875fd0dc6
  Args:
    relation: :hasRelation
    target: Ellen_Franz
    source: Georg_II_Duke_of_Saxe-Meiningen
  AssignClass (fff364a8-95dc-4a8c-9e2d-4d0f6e719669)
 Call ID: fff364a8-95dc-4a8c-9e2d-4d0f6e719669
  Args:
    source: Emperor_Wilhelm_II
    type: :Man
  AssignClass (88d7daeb-c6b0-412b-943a-05726674f64c)
 Call ID: 88d7daeb-c6b0-412b-943a-05726674f64c
  Args:
    source: Emperor_Wilhelm_II
    type: :Person
  AssignClass (f9b1ccc5-7900-459e-88d6-0ac6240315d4)
 Call ID: f9b1ccc5-7900-459e-88d6-0ac6240315d4
  Args:
    type: :Man
    source: Prince_Frederick_William_of_Prussia
  AssignClass (a997ed04-2eaf-4b30-b03f-d661f1362ff4)
 Call ID: a997ed04-2eaf-4b30-b03f-d661f1362ff4
  Args:
    type: :Person
    source: Prince_Frederick_William_of_Prussia
  AssignClass (a97ddc9c-10ac-422f-a7bf-5915165ae6fa)
 Call ID: a97ddc9c-10ac-422f-a7bf-5915165ae6fa
  Args:
    type: :Woman
    source: Princess_Agatha_of_Hohenlohe-Schillingsfürst
  AssignClass (dde9fb76-a5f2-485d-9815-e0e05091740e)
 Call ID: dde9fb76-a5f2-485d-9815-e0e05091740e
  Args:
    type: :Person
    source: Princess_Agatha_of_Hohenlohe-Schillingsfürst
  AddTriple (069e1fe0-fe5b-463e-8793-4f9c68c0ab7f)
 Call ID: 069e1fe0-fe5b-463e-8793-4f9c68c0ab7f
  Args:
    relation: :hasRelation
    target: Princess_Agatha_of_Hohenlohe-Schillingsfürst
    source: Prince_Frederick_William_of_Prussia
  Finish (edeb51ca-cb0a-4cab-a251-88e3fb3b2850)
 Call ID: edeb51ca-cb0a-4cab-a251-88e3fb3b2850
  Args: