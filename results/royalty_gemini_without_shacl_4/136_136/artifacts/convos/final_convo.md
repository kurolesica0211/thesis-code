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
Prince Alexander Ferdinand Albrecht Achilles Wilhelm Joseph Viktor Karl Feodor of Prussia (26 December 1912 – 12 June 1985) was the only son of Prince August Wilhelm of Prussia and Princess Alexandra Victoria of Schleswig-Holstein-Sonderburg-Glücksburg.
Family and early life

Prince Alexander of Prussia was born on 26 December 1912 to Prince August Wilhelm of Prussia and his wife Princess Alexandra Victoria of Schleswig-Holstein-Sonderburg-Glücksburg.
August Wilhelm was a younger son of Kaiser Wilhelm II.
His parents divorced in 1920 and his mother remarried less than two years later; custody of the young prince was awarded to Alexander's father.
Alexander attended the 1932 wedding of the Swedish prince Gustaf Adolf, Duke of Västerbotten with Princess Sibylla of Saxe-Coburg-Gotha in the former duchy of Coburg; it was the first time that a member of the German imperial family had entered the duchy since it became a republic, or specifically a part of Bavaria in November 1919 after the ruling duke, Carl Eduard, had ended his reign on 14 November 1918.
Nazi Party and military career

As of November 1939, Prince Alexander was a first lieutenant in the Air Force Signal Corps, stationed in Wiesbaden.
Like his father, who became a prominent supporter of the Nazi Party, Alexander became an early supporter.
Prince August had secret hopes that Chancellor Adolf Hitler "would one day hoist him or his son Alexander up to the vacant throne of the Kaiser".
The support that father and son gave to the emerging party caused strong disagreements among the Hohenzollerns, with Wilhelm II urging them both to leave the party.
In 1933, Alexander quit the SA and became a private in the German regular army.
Unlike many other German princes, who became the targets of Hitler's mistrust and were removed from their commands in the military, Alexander was the only Hohenzollern allowed to remain at his post.
Marriage

On 19 December 1938 in the Dresden garrison church, Alexander non-dynastically married Armgard Weygand (22 August 1912 – 3 December 2001), daughter of Major Friedrich Weygand and Karla Franziska Oheim.
She was married from 1928 to 1933 to Werner Rosendorff, airman in the German Air Force, and was originally from Wiesbaden, where Alexander Ferdinand was stationed.
They had one son:


Death

Prince Alexander Ferdinand died on 12 June 1985 at Wiesbaden.
}} Media related to Prince Alexander Ferdinand of Prussia at Wikimedia Commons



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
  AssignClass (a7b3025e-8e47-408b-9fa3-36548ec87f5c)
 Call ID: a7b3025e-8e47-408b-9fa3-36548ec87f5c
  Args:
    type: :Man
    source: Prince_Alexander_Ferdinand_of_Prussia
  AssignClass (2b114686-a0ad-4c4e-a31c-500360541bb2)
 Call ID: 2b114686-a0ad-4c4e-a31c-500360541bb2
  Args:
    type: :Person
    source: Prince_Alexander_Ferdinand_of_Prussia
  AddLiteral (f2a1f419-dfd2-4b58-ab9d-135099284800)
 Call ID: f2a1f419-dfd2-4b58-ab9d-135099284800
  Args:
    source: Prince_Alexander_Ferdinand_of_Prussia
    literal_value: 1912
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (781430f5-9783-42e2-8227-d85957cbe604)
 Call ID: 781430f5-9783-42e2-8227-d85957cbe604
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1985
    source: Prince_Alexander_Ferdinand_of_Prussia
  AssignClass (46205114-410f-4bc1-858e-7e4a551c48f1)
 Call ID: 46205114-410f-4bc1-858e-7e4a551c48f1
  Args:
    type: :Man
    source: Prince_August_Wilhelm_of_Prussia
  AssignClass (093dd21d-13c0-42c3-82f9-3b32b2c58485)
 Call ID: 093dd21d-13c0-42c3-82f9-3b32b2c58485
  Args:
    type: :Person
    source: Prince_August_Wilhelm_of_Prussia
  AssignClass (92640b36-c8d5-43d6-a69f-08df0e42c3c9)
 Call ID: 92640b36-c8d5-43d6-a69f-08df0e42c3c9
  Args:
    source: Princess_Alexandra_Victoria_of_Schleswig-Holstein-Sonderburg-Glücksburg
    type: :Woman
  AssignClass (372e3030-ce22-4c4a-a52e-0e46fd213067)
 Call ID: 372e3030-ce22-4c4a-a52e-0e46fd213067
  Args:
    type: :Person
    source: Princess_Alexandra_Victoria_of_Schleswig-Holstein-Sonderburg-Glücksburg
  AddTriple (6eec75e3-b887-4eb9-b12e-6e57ae9f3a11)
 Call ID: 6eec75e3-b887-4eb9-b12e-6e57ae9f3a11
  Args:
    relation: :hasFather
    target: Prince_August_Wilhelm_of_Prussia
    source: Prince_Alexander_Ferdinand_of_Prussia
  AddTriple (564092a0-8db4-4c3d-85e4-539f06627bf5)
 Call ID: 564092a0-8db4-4c3d-85e4-539f06627bf5
  Args:
    target: Princess_Alexandra_Victoria_of_Schleswig-Holstein-Sonderburg-Glücksburg
    source: Prince_Alexander_Ferdinand_of_Prussia
    relation: :hasMother
  AssignClass (b708f838-2e45-443f-8edc-e0d6a6f9c65b)
 Call ID: b708f838-2e45-443f-8edc-e0d6a6f9c65b
  Args:
    type: :Man
    source: Kaiser_Wilhelm_II
  AssignClass (99312cd2-dd69-444b-9e6e-d66fd1f027c5)
 Call ID: 99312cd2-dd69-444b-9e6e-d66fd1f027c5
  Args:
    type: :Person
    source: Kaiser_Wilhelm_II
  AddTriple (e838d2bb-3e8b-4618-bc54-0e75d7cc8c15)
 Call ID: e838d2bb-3e8b-4618-bc54-0e75d7cc8c15
  Args:
    target: Kaiser_Wilhelm_II
    source: Prince_August_Wilhelm_of_Prussia
    relation: :hasFather
  AssignClass (beb5d6d9-c39d-4c4a-a897-0ccf677e33f0)
 Call ID: beb5d6d9-c39d-4c4a-a897-0ccf677e33f0
  Args:
    type: :Woman
    source: Armgard_Weygand
  AssignClass (1fefe7bd-02b4-4943-9622-1941b8d38850)
 Call ID: 1fefe7bd-02b4-4943-9622-1941b8d38850
  Args:
    type: :Person
    source: Armgard_Weygand
  AddLiteral (206a46ac-a22c-4636-a858-4d33a0e07b43)
 Call ID: 206a46ac-a22c-4636-a858-4d33a0e07b43
  Args:
    relation: :hasMarriageYear
    literal_type: xsd:integer
    literal_value: 1938
    source: Prince_Alexander_Ferdinand_of_Prussia
  AddTriple (eb59f9c3-3e57-47ee-851c-688355ba7aed)
 Call ID: eb59f9c3-3e57-47ee-851c-688355ba7aed
  Args:
    relation: :hasRelation
    source: Prince_Alexander_Ferdinand_of_Prussia
    target: Armgard_Weygand
  AssignClass (c813d4a2-4717-4eee-bcd9-5ff1eabbfd2a)
 Call ID: c813d4a2-4717-4eee-bcd9-5ff1eabbfd2a
  Args:
    source: Major_Friedrich_Weygand
    type: :Man
  AssignClass (68a885fc-4d82-4c34-bcb6-78ad9a61b426)
 Call ID: 68a885fc-4d82-4c34-bcb6-78ad9a61b426
  Args:
    source: Major_Friedrich_Weygand
    type: :Person
  AssignClass (79c6d01e-a249-4f84-8dd0-1950c6c4dbb6)
 Call ID: 79c6d01e-a249-4f84-8dd0-1950c6c4dbb6
  Args:
    source: Karla_Franziska_Oheim
    type: :Woman
  AssignClass (547f8a2f-46f0-40a2-b1f9-50de5e93edda)
 Call ID: 547f8a2f-46f0-40a2-b1f9-50de5e93edda
  Args:
    type: :Person
    source: Karla_Franziska_Oheim
  AddTriple (3e79d595-e3c3-4772-9a29-6998f270ea09)
 Call ID: 3e79d595-e3c3-4772-9a29-6998f270ea09
  Args:
    source: Armgard_Weygand
    target: Major_Friedrich_Weygand
    relation: :hasFather
  AddTriple (c6293851-fcdd-487e-9dd1-12e39db41ed0)
 Call ID: c6293851-fcdd-487e-9dd1-12e39db41ed0
  Args:
    relation: :hasMother
    source: Armgard_Weygand
    target: Karla_Franziska_Oheim
  AssignClass (f613cc9d-bbb9-473c-8730-a07038cfe653)
 Call ID: f613cc9d-bbb9-473c-8730-a07038cfe653
  Args:
    type: :Man
    source: Werner_Rosendorff
  AssignClass (86f1afd9-a94e-4b3c-8982-e82c59c7d6d1)
 Call ID: 86f1afd9-a94e-4b3c-8982-e82c59c7d6d1
  Args:
    source: Werner_Rosendorff
    type: :Person
  AddTriple (2996ebee-216f-4003-8a66-3ed0afad9426)
 Call ID: 2996ebee-216f-4003-8a66-3ed0afad9426
  Args:
    target: Werner_Rosendorff
    source: Armgard_Weygand
    relation: :hasRelation
  Finish (543f7582-1ddc-4998-91c0-223a7b77feee)
 Call ID: 543f7582-1ddc-4998-91c0-223a7b77feee
  Args: