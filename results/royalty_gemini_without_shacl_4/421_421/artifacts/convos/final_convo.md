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
Friedrich Wilhelm of Lippe (German: Friedrich Wilhelm Ernst Viktor Alexander Prinz zur Lippe; born 7 September 1947) is a claimant to the headship of the House of Lippe.
Early life

Friedrich Wilhelm was born out of wedlock at Neuwied, West Germany, the first child of Prince Ernst August of Lippe (1917–1990; son of Prince Julius Ernst of Lippe and Duchess Marie of Mecklenburg-Strelitz) and his wife, Christa von Arnim (b. 1923; daughter of Curt David von Arnim and his wife, Stephanie von Stechow).
Marriage

Friedrich Wilhelm married on 18 September 1991 in Munich to Andrea Messner (b. 1966), daughter of Günther Messner, and his wife, Lieselotte Trzoska.
House of Lippe

On 30 December 1949 his father's first cousin Prince Armin succeeded his father, Leopold IV as head of the House of Lippe.
On 22 March 1953, he renounced his position in favour of his older half-brother, Prince Leopold.
Prince Leopold later in 1958 renounced the headship in favour of his older brother, Hereditary Prince Ernst.
Later in that year the Hereditary Prince called a family council where it was agreed by the princes in attendance that the oldest prince living in Germany would be head of the house.
Therefore, the position went to Prince Simon Casimir (1900–1980).
His father died in 1990 and Friedrich Wilhelm continued the claim, despite his illegitimate birth.
Prince Armin, who has said he did not think his decision in 1953 was irrevocable, also claimed to be head of the house until his death in 2015, with his son Stephan, Prince of Lippe continuing his claim.



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
  AssignClass (5992d699-0ec3-476f-bd4a-497a194f3966)
 Call ID: 5992d699-0ec3-476f-bd4a-497a194f3966
  Args:
    source: FriedrichWilhelmOfLippe
    type: :Man
  AssignClass (601accff-d013-4ad6-bfa7-135c26f2eaa5)
 Call ID: 601accff-d013-4ad6-bfa7-135c26f2eaa5
  Args:
    type: :Person
    source: FriedrichWilhelmOfLippe
  AddLiteral (480f0fa0-876b-4212-a1c4-9ea3ba66625a)
 Call ID: 480f0fa0-876b-4212-a1c4-9ea3ba66625a
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1947
    source: FriedrichWilhelmOfLippe
  AssignClass (4cbb692e-210e-4589-b7a1-d1db631c3ca5)
 Call ID: 4cbb692e-210e-4589-b7a1-d1db631c3ca5
  Args:
    source: ErnstAugustOfLippe
    type: :Man
  AssignClass (13ad834b-9283-4260-a978-d1ef14b30435)
 Call ID: 13ad834b-9283-4260-a978-d1ef14b30435
  Args:
    type: :Person
    source: ErnstAugustOfLippe
  AddLiteral (3e3c9e21-d633-488f-a3f8-166c9ca1bf4a)
 Call ID: 3e3c9e21-d633-488f-a3f8-166c9ca1bf4a
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1917
    source: ErnstAugustOfLippe
  AddLiteral (44ee4615-8cd3-4a7e-bbd0-aeef88c2f3e9)
 Call ID: 44ee4615-8cd3-4a7e-bbd0-aeef88c2f3e9
  Args:
    relation: :hasDeathYear
    literal_value: 1990
    source: ErnstAugustOfLippe
    literal_type: xsd:integer
  AssignClass (8923d3a0-5a38-4e2f-8eb3-c6684eec120e)
 Call ID: 8923d3a0-5a38-4e2f-8eb3-c6684eec120e
  Args:
    source: ChristaVonArnim
    type: :Woman
  AssignClass (1f9d4597-7163-4ba2-b59c-187e031ddc86)
 Call ID: 1f9d4597-7163-4ba2-b59c-187e031ddc86
  Args:
    source: ChristaVonArnim
    type: :Person
  AddLiteral (ca73a519-13cc-4daa-942a-b41315fc6b26)
 Call ID: ca73a519-13cc-4daa-942a-b41315fc6b26
  Args:
    relation: :hasBirthYear
    literal_value: 1923
    source: ChristaVonArnim
    literal_type: xsd:integer
  AddTriple (e718e5ea-637f-4943-bce1-41b6e99a05c8)
 Call ID: e718e5ea-637f-4943-bce1-41b6e99a05c8
  Args:
    source: FriedrichWilhelmOfLippe
    target: ErnstAugustOfLippe
    relation: :hasFather
  AddTriple (b1cc08e8-c33b-44c8-b4cc-71b8531b6337)
 Call ID: b1cc08e8-c33b-44c8-b4cc-71b8531b6337
  Args:
    relation: :hasMother
    source: FriedrichWilhelmOfLippe
    target: ChristaVonArnim
  AssignClass (ce1ab98c-a309-455a-b06d-082137b0dbf1)
 Call ID: ce1ab98c-a309-455a-b06d-082137b0dbf1
  Args:
    source: JuliusErnstOfLippe
    type: :Man
  AssignClass (024e5721-ba2c-4885-baa7-ae58d55e1b94)
 Call ID: 024e5721-ba2c-4885-baa7-ae58d55e1b94
  Args:
    source: JuliusErnstOfLippe
    type: :Person
  AssignClass (e15cdbb1-70aa-41b7-beb4-65be3c2cf114)
 Call ID: e15cdbb1-70aa-41b7-beb4-65be3c2cf114
  Args:
    source: MarieOfMecklenburgStrelitz
    type: :Woman
  AssignClass (3a62995a-3fb0-4f1a-bcaa-993734f9978f)
 Call ID: 3a62995a-3fb0-4f1a-bcaa-993734f9978f
  Args:
    source: MarieOfMecklenburgStrelitz
    type: :Person
  AddTriple (92f3f94f-410f-4321-8638-3ee4d84915d8)
 Call ID: 92f3f94f-410f-4321-8638-3ee4d84915d8
  Args:
    source: ErnstAugustOfLippe
    target: JuliusErnstOfLippe
    relation: :hasFather
  AddTriple (3d254bb3-d417-4702-ba77-fc57c57e86e9)
 Call ID: 3d254bb3-d417-4702-ba77-fc57c57e86e9
  Args:
    source: ErnstAugustOfLippe
    target: MarieOfMecklenburgStrelitz
    relation: :hasMother
  AssignClass (72f0214d-05de-4baf-88a7-a6cefee59959)
 Call ID: 72f0214d-05de-4baf-88a7-a6cefee59959
  Args:
    type: :Man
    source: CurtDavidVonArnim
  AssignClass (ebf79eea-ce11-4e0f-90e5-c2011017188b)
 Call ID: ebf79eea-ce11-4e0f-90e5-c2011017188b
  Args:
    source: CurtDavidVonArnim
    type: :Person
  AssignClass (9947c4c5-9995-42b8-9f3c-04f6df953c52)
 Call ID: 9947c4c5-9995-42b8-9f3c-04f6df953c52
  Args:
    type: :Woman
    source: StephanieVonStechow
  AssignClass (f78fdfc7-66e5-4500-9499-8d820a54d727)
 Call ID: f78fdfc7-66e5-4500-9499-8d820a54d727
  Args:
    type: :Person
    source: StephanieVonStechow
  AddTriple (678f450b-b894-4ee8-9b90-eb6c9ad202c5)
 Call ID: 678f450b-b894-4ee8-9b90-eb6c9ad202c5
  Args:
    relation: :hasFather
    source: ChristaVonArnim
    target: CurtDavidVonArnim
  AddTriple (4ba12265-29ff-48fc-9ea0-970556ae6f23)
 Call ID: 4ba12265-29ff-48fc-9ea0-970556ae6f23
  Args:
    target: StephanieVonStechow
    source: ChristaVonArnim
    relation: :hasMother
  AssignClass (49474ba8-90fd-4534-add7-4f01a4bd4d1d)
 Call ID: 49474ba8-90fd-4534-add7-4f01a4bd4d1d
  Args:
    source: AndreaMessner
    type: :Woman
  AssignClass (16cb9d33-a9eb-40d9-b12e-f78bf8a65738)
 Call ID: 16cb9d33-a9eb-40d9-b12e-f78bf8a65738
  Args:
    source: AndreaMessner
    type: :Person
  AddLiteral (d86400d8-f86d-4b31-869d-c4ff76ae6b1f)
 Call ID: d86400d8-f86d-4b31-869d-c4ff76ae6b1f
  Args:
    literal_type: xsd:integer
    source: AndreaMessner
    literal_value: 1966
    relation: :hasBirthYear
  AddLiteral (db61e2fa-66ff-4a0f-b409-77730b9f5618)
 Call ID: db61e2fa-66ff-4a0f-b409-77730b9f5618
  Args:
    relation: :hasMarriageYear
    literal_value: 1991
    source: FriedrichWilhelmOfLippe
    literal_type: xsd:integer
  AddTriple (8f2afca2-9d7b-419f-8752-7c9e270c2da3)
 Call ID: 8f2afca2-9d7b-419f-8752-7c9e270c2da3
  Args:
    relation: :hasRelation
    source: FriedrichWilhelmOfLippe
    target: AndreaMessner
  AssignClass (dc90f2c6-e3ea-4ada-a0f4-fab243493c00)
 Call ID: dc90f2c6-e3ea-4ada-a0f4-fab243493c00
  Args:
    source: GuntherMessner
    type: :Man
  AssignClass (1a49f3fe-dbe0-4cc8-b841-6d4f2813cf65)
 Call ID: 1a49f3fe-dbe0-4cc8-b841-6d4f2813cf65
  Args:
    source: GuntherMessner
    type: :Person
  AssignClass (9c8ed570-5e53-4d51-8d25-9160a14719b9)
 Call ID: 9c8ed570-5e53-4d51-8d25-9160a14719b9
  Args:
    source: LieselotteTrzoska
    type: :Woman
  AssignClass (bd19b1d6-273e-4fe1-b092-890c41f41790)
 Call ID: bd19b1d6-273e-4fe1-b092-890c41f41790
  Args:
    source: LieselotteTrzoska
    type: :Person
  AddTriple (8f06f30b-ee8d-4a40-8b6c-527c6621b93b)
 Call ID: 8f06f30b-ee8d-4a40-8b6c-527c6621b93b
  Args:
    source: AndreaMessner
    target: GuntherMessner
    relation: :hasFather
  AddTriple (e4cd3a89-bda2-4716-bb0e-5d22b59ae814)
 Call ID: e4cd3a89-bda2-4716-bb0e-5d22b59ae814
  Args:
    source: AndreaMessner
    target: LieselotteTrzoska
    relation: :hasMother
  AssignClass (14e7126b-50f6-46f3-9b9e-45f5e08d2d5a)
 Call ID: 14e7126b-50f6-46f3-9b9e-45f5e08d2d5a
  Args:
    type: :Man
    source: PrinceArmin
  AssignClass (ccc3ca91-7393-4fbf-9041-8eb9285633a2)
 Call ID: ccc3ca91-7393-4fbf-9041-8eb9285633a2
  Args:
    source: PrinceArmin
    type: :Person
  AssignClass (121c40cc-b62c-4670-941c-074c59b5f222)
 Call ID: 121c40cc-b62c-4670-941c-074c59b5f222
  Args:
    source: LeopoldIV
    type: :Man
  AssignClass (33c6cd5d-d225-4dd1-b8d6-69c9db9f1539)
 Call ID: 33c6cd5d-d225-4dd1-b8d6-69c9db9f1539
  Args:
    source: LeopoldIV
    type: :Person
  AssignClass (232c89de-4923-404a-8f58-8589de8f77ab)
 Call ID: 232c89de-4923-404a-8f58-8589de8f77ab
  Args:
    type: :Man
    source: PrinceLeopold
  AssignClass (f68ad567-e528-4548-86cb-a95ed0793438)
 Call ID: f68ad567-e528-4548-86cb-a95ed0793438
  Args:
    type: :Person
    source: PrinceLeopold
  AssignClass (8f6d31f5-1bdd-4906-8a22-331a2be3578e)
 Call ID: 8f6d31f5-1bdd-4906-8a22-331a2be3578e
  Args:
    source: HereditaryPrinceErnst
    type: :Man
  AssignClass (5452168e-c500-4d43-9c2c-0e259c728a6b)
 Call ID: 5452168e-c500-4d43-9c2c-0e259c728a6b
  Args:
    source: HereditaryPrinceErnst
    type: :Person
  AssignClass (bffcbdf7-e2b8-4cc7-a8d3-1bd7c10f63bc)
 Call ID: bffcbdf7-e2b8-4cc7-a8d3-1bd7c10f63bc
  Args:
    source: PrinceSimonCasimir
    type: :Man
  AssignClass (08debd26-78d6-4e53-a77c-794d983fdc13)
 Call ID: 08debd26-78d6-4e53-a77c-794d983fdc13
  Args:
    source: PrinceSimonCasimir
    type: :Person
  AddLiteral (8bdc8e9f-bd8c-4bad-864d-54ef617e2ac0)
 Call ID: 8bdc8e9f-bd8c-4bad-864d-54ef617e2ac0
  Args:
    literal_type: xsd:integer
    literal_value: 1900
    source: PrinceSimonCasimir
    relation: :hasBirthYear
  AddLiteral (6493cde1-3659-4256-8556-e6f2ff0a8ba5)
 Call ID: 6493cde1-3659-4256-8556-e6f2ff0a8ba5
  Args:
    relation: :hasDeathYear
    literal_value: 1980
    source: PrinceSimonCasimir
    literal_type: xsd:integer
  AssignClass (093a99e9-a46e-4653-a114-7700a72d24ad)
 Call ID: 093a99e9-a46e-4653-a114-7700a72d24ad
  Args:
    type: :Man
    source: StephanPrinceOfLippe
  AssignClass (4e46a135-95ee-47b5-a242-eb614f5182d7)
 Call ID: 4e46a135-95ee-47b5-a242-eb614f5182d7
  Args:
    type: :Person
    source: StephanPrinceOfLippe
  AddTriple (4e760660-2031-48ae-992a-2913db52caa4)
 Call ID: 4e760660-2031-48ae-992a-2913db52caa4
  Args:
    relation: :hasFather
    target: PrinceArmin
    source: StephanPrinceOfLippe
  Finish (031d320e-4c8a-4cc3-ad29-ccc425a89964)
 Call ID: 031d320e-4c8a-4cc3-ad29-ccc425a89964
  Args: