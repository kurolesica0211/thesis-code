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
Prince Waldemar of Prussia (Joachim Friedrich Ernst Waldemar; 10 February 1868 – 27 March 1879) was the sixth child and youngest son of the German Crown Prince and Crown Princess, later Emperor Frederick III and Empress Victoria.
Prince Waldemar was a grandson of both William I, German Emperor, and Queen Victoria of the United Kingdom.
Biography

Early life

Waldemar was the favourite of both the Princess Royal and her husband.
Waldemar had a "fun loving" character and a great sense of humour and love for animals and sports.
On one occasion, when visiting his grandmother, Queen Victoria, Waldemar let loose his pet crocodile in her study, much to the shock of the middle-aged queen.
The Princess Royal wrote that she would be unhappy when Waldemar went off to school, "as he is my very own boy."
She seemed to prefer Waldemar over his elder brothers Wilhelm and Heinrich.
Death

Less than four months after the deaths of his maternal aunt, Alice, Grand Duchess of Hesse and cousin, Marie, Waldemar became seriously ill with diphtheria and died in Berlin, Germany on 27 March 1879.
He was buried in the royal mausoleum attached to the Friedenskirche at Potsdam, near the main altar and his elder brother Prince Sigismund of Prussia.



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
  AssignClass (d46be526-9145-4c98-9e68-3763244a8b20)
 Call ID: d46be526-9145-4c98-9e68-3763244a8b20
  Args:
    source: Prince Waldemar of Prussia
    type: :Man
  AssignClass (acc77789-fa44-4905-af83-8900c4395697)
 Call ID: acc77789-fa44-4905-af83-8900c4395697
  Args:
    source: Prince Waldemar of Prussia
    type: :Person
  AddLiteral (183564b3-b564-4581-98f4-15ddb2f07270)
 Call ID: 183564b3-b564-4581-98f4-15ddb2f07270
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1868
    source: Prince Waldemar of Prussia
  AddLiteral (ee3bbac2-3e32-47cc-bfcc-ab93b22b2288)
 Call ID: ee3bbac2-3e32-47cc-bfcc-ab93b22b2288
  Args:
    literal_type: xsd:integer
    literal_value: 1879
    source: Prince Waldemar of Prussia
    relation: :hasDeathYear
  AssignClass (b3cd347b-11b8-4e36-86be-3593d0182897)
 Call ID: b3cd347b-11b8-4e36-86be-3593d0182897
  Args:
    source: Frederick III
    type: :Man
  AssignClass (744d576f-9e40-42ea-889c-dbe6b0c97046)
 Call ID: 744d576f-9e40-42ea-889c-dbe6b0c97046
  Args:
    source: Frederick III
    type: :Person
  AssignClass (742f203e-5318-4757-a8f5-1c8570a80a7c)
 Call ID: 742f203e-5318-4757-a8f5-1c8570a80a7c
  Args:
    type: :Woman
    source: Victoria
  AssignClass (47d0c435-f1b4-473e-86a2-9e6980a4310a)
 Call ID: 47d0c435-f1b4-473e-86a2-9e6980a4310a
  Args:
    type: :Person
    source: Victoria
  AddTriple (c557a54d-4ca5-4b47-9a38-df9af96a8831)
 Call ID: c557a54d-4ca5-4b47-9a38-df9af96a8831
  Args:
    source: Prince Waldemar of Prussia
    target: Frederick III
    relation: :hasFather
  AddTriple (bb5035dc-a314-4d7e-bc8d-a96886a2d610)
 Call ID: bb5035dc-a314-4d7e-bc8d-a96886a2d610
  Args:
    target: Victoria
    source: Prince Waldemar of Prussia
    relation: :hasMother
  AssignClass (f9505b6a-d56f-474f-ae49-76b3b8501c75)
 Call ID: f9505b6a-d56f-474f-ae49-76b3b8501c75
  Args:
    type: :Man
    source: William I
  AssignClass (b650a144-6b02-4ab1-b8db-ddea3ce8e145)
 Call ID: b650a144-6b02-4ab1-b8db-ddea3ce8e145
  Args:
    type: :Person
    source: William I
  AssignClass (913b9a2f-837c-470e-8b56-b626c2c2cff3)
 Call ID: 913b9a2f-837c-470e-8b56-b626c2c2cff3
  Args:
    type: :Woman
    source: Queen Victoria
  AssignClass (a51909de-bcc2-48a5-9e17-e4eb403b1b7e)
 Call ID: a51909de-bcc2-48a5-9e17-e4eb403b1b7e
  Args:
    source: Queen Victoria
    type: :Person
  AddTriple (364d9d06-1eb3-4cae-b3ec-8764c9629c06)
 Call ID: 364d9d06-1eb3-4cae-b3ec-8764c9629c06
  Args:
    relation: :hasAncestor
    source: Prince Waldemar of Prussia
    target: William I
  AddTriple (e11b1857-0dc8-44a7-957f-2790a1e9d807)
 Call ID: e11b1857-0dc8-44a7-957f-2790a1e9d807
  Args:
    source: Prince Waldemar of Prussia
    target: Queen Victoria
    relation: :hasAncestor
  AssignClass (33e8171a-4c7f-435b-8041-3ebabf7b73ab)
 Call ID: 33e8171a-4c7f-435b-8041-3ebabf7b73ab
  Args:
    type: :Man
    source: Wilhelm
  AssignClass (4c9ede25-1a08-444c-bad2-f752a01d8e09)
 Call ID: 4c9ede25-1a08-444c-bad2-f752a01d8e09
  Args:
    type: :Person
    source: Wilhelm
  AssignClass (5642730b-8cc5-446c-a836-d8ef641e814b)
 Call ID: 5642730b-8cc5-446c-a836-d8ef641e814b
  Args:
    type: :Man
    source: Heinrich
  AssignClass (0900278f-78c4-443f-b2e2-5e4004dcf9cb)
 Call ID: 0900278f-78c4-443f-b2e2-5e4004dcf9cb
  Args:
    type: :Person
    source: Heinrich
  AddTriple (fbb12cbe-bdf6-4bcc-9f00-c6295bab4160)
 Call ID: fbb12cbe-bdf6-4bcc-9f00-c6295bab4160
  Args:
    target: Wilhelm
    source: Prince Waldemar of Prussia
    relation: :isSiblingOf
  AddTriple (81bd4092-70d5-4481-ade8-04961a297bbb)
 Call ID: 81bd4092-70d5-4481-ade8-04961a297bbb
  Args:
    relation: :isSiblingOf
    target: Heinrich
    source: Prince Waldemar of Prussia
  AssignClass (1e42eab9-e914-4449-9474-ceccc8ecef3a)
 Call ID: 1e42eab9-e914-4449-9474-ceccc8ecef3a
  Args:
    source: Alice
    type: :Woman
  AssignClass (75079cd3-f3fc-46c1-bc0f-b02130a094a4)
 Call ID: 75079cd3-f3fc-46c1-bc0f-b02130a094a4
  Args:
    type: :Person
    source: Alice
  AssignClass (019298f1-c1f2-4357-a715-db5a90ed7a81)
 Call ID: 019298f1-c1f2-4357-a715-db5a90ed7a81
  Args:
    type: :Woman
    source: Marie
  AssignClass (f8e628f3-1a7f-4628-881b-17764ed08a8d)
 Call ID: f8e628f3-1a7f-4628-881b-17764ed08a8d
  Args:
    type: :Person
    source: Marie
  AddTriple (68f92cdc-e720-4a9d-9eed-2552d6d7884d)
 Call ID: 68f92cdc-e720-4a9d-9eed-2552d6d7884d
  Args:
    target: Alice
    source: Prince Waldemar of Prussia
    relation: :hasRelation
  AddTriple (e3e90efa-7ed3-4ea6-beb5-c44258051464)
 Call ID: e3e90efa-7ed3-4ea6-beb5-c44258051464
  Args:
    source: Prince Waldemar of Prussia
    target: Marie
    relation: :hasRelation
  AssignClass (91812588-4343-4b10-abcb-62cb2c154546)
 Call ID: 91812588-4343-4b10-abcb-62cb2c154546
  Args:
    type: :Man
    source: Prince Sigismund of Prussia
  AssignClass (7d29648e-0d5c-405c-bab6-950a99f038e5)
 Call ID: 7d29648e-0d5c-405c-bab6-950a99f038e5
  Args:
    source: Prince Sigismund of Prussia
    type: :Person
  AddTriple (b51e42de-b212-45b2-8ea4-bbe351668e9f)
 Call ID: b51e42de-b212-45b2-8ea4-bbe351668e9f
  Args:
    source: Prince Waldemar of Prussia
    target: Prince Sigismund of Prussia
    relation: :isSiblingOf
  Finish (9ff36a07-70ad-4665-85ef-387bccef3367)
 Call ID: 9ff36a07-70ad-4665-85ef-387bccef3367
  Args: