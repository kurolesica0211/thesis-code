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
  AssignClass (93c17c10-a75e-4b93-b20b-a3b1ce42fb66)
 Call ID: 93c17c10-a75e-4b93-b20b-a3b1ce42fb66
  Args:
    type: :Man
    source: Friedrich_Wilhelm_of_Lippe
  AssignClass (faf48c34-658a-4539-beef-bb33e112bb89)
 Call ID: faf48c34-658a-4539-beef-bb33e112bb89
  Args:
    type: :Person
    source: Friedrich_Wilhelm_of_Lippe
  AddLiteral (3d08e880-9b4c-40f4-a9ca-6e2874691056)
 Call ID: 3d08e880-9b4c-40f4-a9ca-6e2874691056
  Args:
    literal_type: xsd:integer
    literal_value: 1947
    relation: :hasBirthYear
    source: Friedrich_Wilhelm_of_Lippe
  AssignClass (c722ab46-7dbb-416c-8c1e-936e19f22cd9)
 Call ID: c722ab46-7dbb-416c-8c1e-936e19f22cd9
  Args:
    type: :Man
    source: Prince_Ernst_August_of_Lippe
  AssignClass (2e1abffc-5ed7-4934-9ad9-9239a86ceb7a)
 Call ID: 2e1abffc-5ed7-4934-9ad9-9239a86ceb7a
  Args:
    type: :Person
    source: Prince_Ernst_August_of_Lippe
  AssignClass (2d6d7589-db88-488f-9b7d-fb036f4028d2)
 Call ID: 2d6d7589-db88-488f-9b7d-fb036f4028d2
  Args:
    type: :Ancestor
    source: Prince_Ernst_August_of_Lippe
  AddLiteral (c9ded5fe-5265-47af-a0e4-7b6092b602b7)
 Call ID: c9ded5fe-5265-47af-a0e4-7b6092b602b7
  Args:
    source: Prince_Ernst_August_of_Lippe
    relation: :hasBirthYear
    literal_value: 1917
    literal_type: xsd:integer
  AddLiteral (8f6c9b0b-16e6-4f9b-940e-83ff9c6632e2)
 Call ID: 8f6c9b0b-16e6-4f9b-940e-83ff9c6632e2
  Args:
    literal_value: 1990
    literal_type: xsd:integer
    source: Prince_Ernst_August_of_Lippe
    relation: :hasDeathYear
  AddTriple (d873be18-1e2c-4aa6-9852-75d9de6b4a11)
 Call ID: d873be18-1e2c-4aa6-9852-75d9de6b4a11
  Args:
    relation: :hasFather
    source: Friedrich_Wilhelm_of_Lippe
    target: Prince_Ernst_August_of_Lippe
  AssignClass (40278651-f7e0-470a-9d6d-e88fa9ae4dad)
 Call ID: 40278651-f7e0-470a-9d6d-e88fa9ae4dad
  Args:
    type: :Woman
    source: Christa_von_Arnim
  AssignClass (07459247-410b-457a-a2a1-be5ad9fbc102)
 Call ID: 07459247-410b-457a-a2a1-be5ad9fbc102
  Args:
    type: :Person
    source: Christa_von_Arnim
  AssignClass (8a04e547-3cbc-431d-aa95-91f90dcf499e)
 Call ID: 8a04e547-3cbc-431d-aa95-91f90dcf499e
  Args:
    type: :Ancestor
    source: Christa_von_Arnim
  AddLiteral (b22be89f-3570-4826-976d-d8b3b2119a94)
 Call ID: b22be89f-3570-4826-976d-d8b3b2119a94
  Args:
    literal_value: 1923
    literal_type: xsd:integer
    source: Christa_von_Arnim
    relation: :hasBirthYear
  AddTriple (554c2add-032e-4468-bfc5-f72c52400e5c)
 Call ID: 554c2add-032e-4468-bfc5-f72c52400e5c
  Args:
    relation: :hasMother
    source: Friedrich_Wilhelm_of_Lippe
    target: Christa_von_Arnim
  AssignClass (430f46f7-6b84-4641-ad66-c644e6009e37)
 Call ID: 430f46f7-6b84-4641-ad66-c644e6009e37
  Args:
    type: :Man
    source: Prince_Julius_Ernst_of_Lippe
  AssignClass (8645b393-6fd7-4fbe-9375-3e1d15be4e90)
 Call ID: 8645b393-6fd7-4fbe-9375-3e1d15be4e90
  Args:
    type: :Person
    source: Prince_Julius_Ernst_of_Lippe
  AssignClass (c30233d8-4816-49e4-b3ef-fd4c39f1ca9d)
 Call ID: c30233d8-4816-49e4-b3ef-fd4c39f1ca9d
  Args:
    type: :Ancestor
    source: Prince_Julius_Ernst_of_Lippe
  AddTriple (f6214a50-9d32-4f7a-8dc8-ca1c8f2b14dc)
 Call ID: f6214a50-9d32-4f7a-8dc8-ca1c8f2b14dc
  Args:
    target: Prince_Julius_Ernst_of_Lippe
    relation: :hasFather
    source: Prince_Ernst_August_of_Lippe
  AssignClass (e8b67835-c6e3-4974-b547-0a28bb10ca6d)
 Call ID: e8b67835-c6e3-4974-b547-0a28bb10ca6d
  Args:
    type: :Woman
    source: Duchess_Marie_of_Mecklenburg-Strelitz
  AssignClass (548efcf9-7b45-470f-a64c-50bae201d01f)
 Call ID: 548efcf9-7b45-470f-a64c-50bae201d01f
  Args:
    type: :Person
    source: Duchess_Marie_of_Mecklenburg-Strelitz
  AssignClass (9d37cef0-bd29-4547-bdb4-796e7ceed452)
 Call ID: 9d37cef0-bd29-4547-bdb4-796e7ceed452
  Args:
    type: :Ancestor
    source: Duchess_Marie_of_Mecklenburg-Strelitz
  AddTriple (72a45573-543b-4ad5-be27-ede47a24abc7)
 Call ID: 72a45573-543b-4ad5-be27-ede47a24abc7
  Args:
    target: Duchess_Marie_of_Mecklenburg-Strelitz
    source: Prince_Ernst_August_of_Lippe
    relation: :hasMother
  AssignClass (2c6862ef-7a46-4e33-9eb6-9b51a86a0652)
 Call ID: 2c6862ef-7a46-4e33-9eb6-9b51a86a0652
  Args:
    type: :Man
    source: Curt_David_von_Arnim
  AssignClass (87854977-b00b-4475-8dc9-913760924b21)
 Call ID: 87854977-b00b-4475-8dc9-913760924b21
  Args:
    type: :Person
    source: Curt_David_von_Arnim
  AssignClass (6f7ccbad-a8f2-4317-b374-af42d0851742)
 Call ID: 6f7ccbad-a8f2-4317-b374-af42d0851742
  Args:
    type: :Ancestor
    source: Curt_David_von_Arnim
  AddTriple (68a680e5-d57c-4140-b61e-b9be2b9cb9cf)
 Call ID: 68a680e5-d57c-4140-b61e-b9be2b9cb9cf
  Args:
    relation: :hasFather
    source: Christa_von_Arnim
    target: Curt_David_von_Arnim
  AssignClass (3ecca8e7-8f5d-4036-9eee-91fc7213522e)
 Call ID: 3ecca8e7-8f5d-4036-9eee-91fc7213522e
  Args:
    type: :Woman
    source: Stephanie_von_Stechow
  AssignClass (42f2b495-0868-476a-bd61-cd21fa4dfe41)
 Call ID: 42f2b495-0868-476a-bd61-cd21fa4dfe41
  Args:
    type: :Person
    source: Stephanie_von_Stechow
  AssignClass (068bfc8e-e3ed-4ef0-907e-3e1bd8aeefde)
 Call ID: 068bfc8e-e3ed-4ef0-907e-3e1bd8aeefde
  Args:
    type: :Ancestor
    source: Stephanie_von_Stechow
  AddTriple (c89c8950-d707-4889-b9f6-b972a7b92f5f)
 Call ID: c89c8950-d707-4889-b9f6-b972a7b92f5f
  Args:
    target: Stephanie_von_Stechow
    source: Christa_von_Arnim
    relation: :hasMother
  AssignClass (7a8acad1-542a-414f-ba9d-9bc1cef1c4ea)
 Call ID: 7a8acad1-542a-414f-ba9d-9bc1cef1c4ea
  Args:
    type: :Woman
    source: Andrea_Messner
  AssignClass (c9c12d5d-779c-48f1-9666-f1fbf218f5cf)
 Call ID: c9c12d5d-779c-48f1-9666-f1fbf218f5cf
  Args:
    type: :Person
    source: Andrea_Messner
  AddLiteral (641ae06f-1cdd-43e5-91fe-e950f73ee197)
 Call ID: 641ae06f-1cdd-43e5-91fe-e950f73ee197
  Args:
    literal_type: xsd:integer
    literal_value: 1966
    relation: :hasBirthYear
    source: Andrea_Messner
  AddLiteral (1185f8d6-e4cf-4e83-9e5c-8611a542de66)
 Call ID: 1185f8d6-e4cf-4e83-9e5c-8611a542de66
  Args:
    source: Friedrich_Wilhelm_of_Lippe
    relation: :hasMarriageYear
    literal_value: 1991
    literal_type: xsd:integer
  AddTriple (75e05922-4bc4-4682-a7f6-86ff8c7b7c93)
 Call ID: 75e05922-4bc4-4682-a7f6-86ff8c7b7c93
  Args:
    relation: :hasRelation
    source: Friedrich_Wilhelm_of_Lippe
    target: Andrea_Messner
  AssignClass (a458f1e2-c906-49e8-9e6b-70c1b6fcc0b5)
 Call ID: a458f1e2-c906-49e8-9e6b-70c1b6fcc0b5
  Args:
    type: :Man
    source: Günther_Messner
  AssignClass (ea5aba5b-b0de-4ffb-9acb-27b0cb2fe12d)
 Call ID: ea5aba5b-b0de-4ffb-9acb-27b0cb2fe12d
  Args:
    type: :Person
    source: Günther_Messner
  AssignClass (40d10c80-54ba-45ed-ac09-f159af5c7c44)
 Call ID: 40d10c80-54ba-45ed-ac09-f159af5c7c44
  Args:
    type: :Ancestor
    source: Günther_Messner
  AddTriple (bc2f63ff-d99e-4abd-a6ec-992bfa07b604)
 Call ID: bc2f63ff-d99e-4abd-a6ec-992bfa07b604
  Args:
    target: Günther_Messner
    relation: :hasFather
    source: Andrea_Messner
  AssignClass (9c8a44dd-ea73-4ed4-b869-756368b10ee1)
 Call ID: 9c8a44dd-ea73-4ed4-b869-756368b10ee1
  Args:
    type: :Woman
    source: Lieselotte_Trzoska
  AssignClass (2b6825ab-83d6-4f7c-9230-0eccdef2eca3)
 Call ID: 2b6825ab-83d6-4f7c-9230-0eccdef2eca3
  Args:
    type: :Person
    source: Lieselotte_Trzoska
  AssignClass (81e45750-819f-4170-9e0f-ff8cb917fb5e)
 Call ID: 81e45750-819f-4170-9e0f-ff8cb917fb5e
  Args:
    type: :Ancestor
    source: Lieselotte_Trzoska
  AddTriple (81b4792f-1638-482c-b407-db564a86b900)
 Call ID: 81b4792f-1638-482c-b407-db564a86b900
  Args:
    target: Lieselotte_Trzoska
    relation: :hasMother
    source: Andrea_Messner
  Finish (83bbe580-1f51-410f-bf15-9cd6cc8198e8)
 Call ID: 83bbe580-1f51-410f-bf15-9cd6cc8198e8
  Args: