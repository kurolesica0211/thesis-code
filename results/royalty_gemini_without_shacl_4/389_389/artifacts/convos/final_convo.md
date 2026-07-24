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
Michael Claude Hamilton Bowes-Lyon (1 October 1893 – 1 May 1953), known as Mickie Bowes-Lyon, was an elder brother of Queen Elizabeth the Queen Mother and maternal uncle of Queen Elizabeth II.
Biography

Bowes-Lyon was born on 1 October 1893, the fifth son and eighth child of Claude Bowes-Lyon, Lord Glamis, later 14th
During World War I, Bowes-Lyon served in France in The Royal Scots (Lothian Regiment).
After the war, Bowes-Lyon was a justice of the peace and deputy lieutenant of Bedfordshire.
In 1928, Bowes-Lyon married Elizabeth Margaret Cator (1899–1959), daughter of John Cator, at St George's, Hanover Square.
Cator had been a bridesmaid at his sister Elizabeth's wedding to Prince Albert, Duke of York, in 1923.
Bowes-Lyon predeceased him and the earldom was inherited by his eldest son, Fergus, in 1972.
Bowes-Lyon died on 1 May 1953 at his home in Biggleswade as the result of asthma.



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
  AssignClass (9e4e8762-0f5d-42a1-a0de-4c712426d53d)
 Call ID: 9e4e8762-0f5d-42a1-a0de-4c712426d53d
  Args:
    source: MichaelClaudeHamiltonBowes-Lyon
    type: :Man
  AssignClass (2b3b3e2f-94f4-43f2-a2e4-8d002ca0e65c)
 Call ID: 2b3b3e2f-94f4-43f2-a2e4-8d002ca0e65c
  Args:
    source: MichaelClaudeHamiltonBowes-Lyon
    type: :Person
  AddLiteral (ffc5f662-7ee9-4fb8-9e50-127e3549e0ad)
 Call ID: ffc5f662-7ee9-4fb8-9e50-127e3549e0ad
  Args:
    source: MichaelClaudeHamiltonBowes-Lyon
    literal_type: xsd:string
    literal_value: Mickie Bowes-Lyon
    relation: :knownAs
  AddLiteral (78da3946-5c56-40c9-908a-5c701a2ed972)
 Call ID: 78da3946-5c56-40c9-908a-5c701a2ed972
  Args:
    literal_type: xsd:integer
    source: MichaelClaudeHamiltonBowes-Lyon
    relation: :hasBirthYear
    literal_value: 1893
  AddLiteral (4b014bb6-e944-4f8d-9ef2-576b02ad34d4)
 Call ID: 4b014bb6-e944-4f8d-9ef2-576b02ad34d4
  Args:
    relation: :hasDeathYear
    literal_value: 1953
    literal_type: xsd:integer
    source: MichaelClaudeHamiltonBowes-Lyon
  AssignClass (2a66cf46-1297-4270-bd39-1bc02c5a243f)
 Call ID: 2a66cf46-1297-4270-bd39-1bc02c5a243f
  Args:
    source: ClaudeBowes-Lyon
    type: :Man
  AssignClass (72113803-2938-41ec-a19b-d0ae426d0a77)
 Call ID: 72113803-2938-41ec-a19b-d0ae426d0a77
  Args:
    type: :Person
    source: ClaudeBowes-Lyon
  AddTriple (99f2a194-76cf-465a-aff5-95e44c6dd5e3)
 Call ID: 99f2a194-76cf-465a-aff5-95e44c6dd5e3
  Args:
    relation: :hasFather
    target: ClaudeBowes-Lyon
    source: MichaelClaudeHamiltonBowes-Lyon
  AssignClass (5be41f49-6a0b-462d-bd0b-8a6d5659756c)
 Call ID: 5be41f49-6a0b-462d-bd0b-8a6d5659756c
  Args:
    source: ElizabethQueenMother
    type: :Woman
  AssignClass (14b398ed-839d-4dee-82fe-3bbaa3430e63)
 Call ID: 14b398ed-839d-4dee-82fe-3bbaa3430e63
  Args:
    type: :Person
    source: ElizabethQueenMother
  AddTriple (36cf0a54-b535-4444-b267-2b9cd86f0c77)
 Call ID: 36cf0a54-b535-4444-b267-2b9cd86f0c77
  Args:
    source: MichaelClaudeHamiltonBowes-Lyon
    target: ElizabethQueenMother
    relation: :isSiblingOf
  AssignClass (c4d420ec-9e39-452a-8099-2c80a02a0362)
 Call ID: c4d420ec-9e39-452a-8099-2c80a02a0362
  Args:
    source: QueenElizabethII
    type: :Woman
  AssignClass (47307a42-999e-462f-a5dc-f5b3d9703327)
 Call ID: 47307a42-999e-462f-a5dc-f5b3d9703327
  Args:
    type: :Person
    source: QueenElizabethII
  AddTriple (104dfeaa-cdcb-4c2d-8c5c-415d8b803f93)
 Call ID: 104dfeaa-cdcb-4c2d-8c5c-415d8b803f93
  Args:
    target: QueenElizabethII
    relation: :isUncleOf
    source: MichaelClaudeHamiltonBowes-Lyon
  AssignClass (cdaad259-c113-444c-8e6d-30cb63229dc1)
 Call ID: cdaad259-c113-444c-8e6d-30cb63229dc1
  Args:
    source: ElizabethMargaretCator
    type: :Woman
  AssignClass (01012e62-0be8-4ae4-9c7e-d224718a3a76)
 Call ID: 01012e62-0be8-4ae4-9c7e-d224718a3a76
  Args:
    type: :Person
    source: ElizabethMargaretCator
  AddLiteral (ad224143-d328-4bbb-a6c8-f427f60dbf5f)
 Call ID: ad224143-d328-4bbb-a6c8-f427f60dbf5f
  Args:
    source: ElizabethMargaretCator
    literal_type: xsd:integer
    literal_value: 1899
    relation: :hasBirthYear
  AddLiteral (7a92d0f3-8e25-4826-9d28-24cfced3cf2c)
 Call ID: 7a92d0f3-8e25-4826-9d28-24cfced3cf2c
  Args:
    source: ElizabethMargaretCator
    literal_type: xsd:integer
    literal_value: 1959
    relation: :hasDeathYear
  AddLiteral (e84d7342-5cd2-45b5-ba36-e196e9622b8e)
 Call ID: e84d7342-5cd2-45b5-ba36-e196e9622b8e
  Args:
    relation: :hasMarriageYear
    literal_value: 1928
    literal_type: xsd:integer
    source: MichaelClaudeHamiltonBowes-Lyon
  AddTriple (f89ebe4e-ff8a-42fd-832b-650621b11ba1)
 Call ID: f89ebe4e-ff8a-42fd-832b-650621b11ba1
  Args:
    target: ElizabethMargaretCator
    relation: :hasRelation
    source: MichaelClaudeHamiltonBowes-Lyon
  AssignClass (1af250df-c29d-4b15-b0f9-b87a21021143)
 Call ID: 1af250df-c29d-4b15-b0f9-b87a21021143
  Args:
    type: :Man
    source: JohnCator
  AssignClass (0c90ba58-6cf6-4bc7-ad6f-f00d30f5e832)
 Call ID: 0c90ba58-6cf6-4bc7-ad6f-f00d30f5e832
  Args:
    source: JohnCator
    type: :Person
  AddTriple (d36fe71c-ab0c-4f5e-888d-8e1712442a09)
 Call ID: d36fe71c-ab0c-4f5e-888d-8e1712442a09
  Args:
    source: ElizabethMargaretCator
    relation: :hasFather
    target: JohnCator
  AssignClass (c6f308e1-4e55-4e7e-8a55-fb2d500311df)
 Call ID: c6f308e1-4e55-4e7e-8a55-fb2d500311df
  Args:
    source: PrinceAlbertDukeOfYork
    type: :Man
  AssignClass (bb2372f9-e756-4153-943f-23bd0081ab0a)
 Call ID: bb2372f9-e756-4153-943f-23bd0081ab0a
  Args:
    type: :Person
    source: PrinceAlbertDukeOfYork
  AddTriple (4ad00034-2e7b-4a44-b568-dd6540c515bc)
 Call ID: 4ad00034-2e7b-4a44-b568-dd6540c515bc
  Args:
    relation: :hasRelation
    target: PrinceAlbertDukeOfYork
    source: ElizabethQueenMother
  AssignClass (deb2d142-7d70-4219-88a0-c64c35e84f48)
 Call ID: deb2d142-7d70-4219-88a0-c64c35e84f48
  Args:
    source: FergusBowes-Lyon
    type: :Man
  AssignClass (d9ed172b-ecfd-4488-b010-beeb17ddeb85)
 Call ID: d9ed172b-ecfd-4488-b010-beeb17ddeb85
  Args:
    type: :Person
    source: FergusBowes-Lyon
  AddTriple (9a11a1a6-0e9d-40f9-8d2d-e26d886f3abc)
 Call ID: 9a11a1a6-0e9d-40f9-8d2d-e26d886f3abc
  Args:
    source: MichaelClaudeHamiltonBowes-Lyon
    relation: :hasSon
    target: FergusBowes-Lyon
  Finish (8f9a7ba6-aa68-4e19-a5ee-8124f7731523)
 Call ID: 8f9a7ba6-aa68-4e19-a5ee-8124f7731523
  Args: