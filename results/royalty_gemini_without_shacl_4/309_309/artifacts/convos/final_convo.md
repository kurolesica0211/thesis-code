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
The Duke of Castro  The Duchess of Castro


Princess Béatrice Marie Caroline Louise Françoise of Bourbon-Two Sicilies (born 16 June 1950 in Saint-Raphaël, Var, France) is the eldest daughter of Prince Ferdinand, Duke of Castro, Castro-line claimant to the headship of the House of Bourbon-Two Sicilies, and his wife, Chantal de Chevron-Villette.
Her younger brother, Prince Carlo, Duke of Castro, is the current Castro-line claimant to the headship of the House of Bourbon-Two Sicilies.
Marriage and issue

Béatrice married Charles Napoléon Bonaparte, eldest son of Louis, Prince Napoléon and his wife, Alix de Foresta, on 19 December 1978 in Paris, France.
Charles was the great-great-grandnephew of Napoleon I of France, founder of the Imperial House of France.
Béatrice and Charles had two children:


Title, styles and honours

Title and styles

Honours

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
  AssignClass (5e34b5c6-13ad-4520-b56a-a8b168e0c3e8)
 Call ID: 5e34b5c6-13ad-4520-b56a-a8b168e0c3e8
  Args:
    type: :Woman
    source: Princess Béatrice Marie Caroline Louise Françoise of Bourbon-Two Sicilies
  AssignClass (37693ee0-be10-42b9-b5c2-6f99225a1fd5)
 Call ID: 37693ee0-be10-42b9-b5c2-6f99225a1fd5
  Args:
    source: Princess Béatrice Marie Caroline Louise Françoise of Bourbon-Two Sicilies
    type: :Person
  AddLiteral (a8c04242-bc46-49d6-9e94-954609b83b26)
 Call ID: a8c04242-bc46-49d6-9e94-954609b83b26
  Args:
    relation: :hasBirthYear
    literal_value: 1950
    literal_type: xsd:integer
    source: Princess Béatrice Marie Caroline Louise Françoise of Bourbon-Two Sicilies
  AssignClass (8991a3b7-dcbc-453e-bd4a-9f02f2e30963)
 Call ID: 8991a3b7-dcbc-453e-bd4a-9f02f2e30963
  Args:
    source: Prince Ferdinand, Duke of Castro
    type: :Man
  AssignClass (8c8af9a5-5f78-4e73-b550-a58f48ecf365)
 Call ID: 8c8af9a5-5f78-4e73-b550-a58f48ecf365
  Args:
    source: Prince Ferdinand, Duke of Castro
    type: :Person
  AssignClass (1b35d2a6-5c65-42fa-8a56-b78cb79edca4)
 Call ID: 1b35d2a6-5c65-42fa-8a56-b78cb79edca4
  Args:
    type: :Woman
    source: Chantal de Chevron-Villette
  AssignClass (f4f1d26e-0355-476d-8320-1b1e52503685)
 Call ID: f4f1d26e-0355-476d-8320-1b1e52503685
  Args:
    source: Chantal de Chevron-Villette
    type: :Person
  AddTriple (95ab4ca6-e718-4e8f-911b-65275cd34f9a)
 Call ID: 95ab4ca6-e718-4e8f-911b-65275cd34f9a
  Args:
    target: Prince Ferdinand, Duke of Castro
    source: Princess Béatrice Marie Caroline Louise Françoise of Bourbon-Two Sicilies
    relation: :hasFather
  AddTriple (b3ac531d-3e1f-4913-ae6d-60ab9be6aea9)
 Call ID: b3ac531d-3e1f-4913-ae6d-60ab9be6aea9
  Args:
    source: Princess Béatrice Marie Caroline Louise Françoise of Bourbon-Two Sicilies
    relation: :hasMother
    target: Chantal de Chevron-Villette
  AssignClass (a64c1371-0bea-4040-a6b6-44e9755e740e)
 Call ID: a64c1371-0bea-4040-a6b6-44e9755e740e
  Args:
    source: Prince Carlo, Duke of Castro
    type: :Man
  AssignClass (6ac14d29-ee75-4091-9418-ab9d3defeadd)
 Call ID: 6ac14d29-ee75-4091-9418-ab9d3defeadd
  Args:
    type: :Person
    source: Prince Carlo, Duke of Castro
  AddTriple (946b16ad-893a-48f2-a2ef-972e531abcff)
 Call ID: 946b16ad-893a-48f2-a2ef-972e531abcff
  Args:
    target: Princess Béatrice Marie Caroline Louise Françoise of Bourbon-Two Sicilies
    source: Prince Carlo, Duke of Castro
    relation: :isBrotherOf
  AddTriple (c005274a-3ae4-4194-b4c0-d848d369eecc)
 Call ID: c005274a-3ae4-4194-b4c0-d848d369eecc
  Args:
    source: Prince Carlo, Duke of Castro
    relation: :hasFather
    target: Prince Ferdinand, Duke of Castro
  AddTriple (dedfbfed-d485-4c5d-9fb6-fe9c061c51fa)
 Call ID: dedfbfed-d485-4c5d-9fb6-fe9c061c51fa
  Args:
    target: Chantal de Chevron-Villette
    relation: :hasMother
    source: Prince Carlo, Duke of Castro
  AssignClass (2b902c87-b027-475c-ac6f-beed2a3cba0c)
 Call ID: 2b902c87-b027-475c-ac6f-beed2a3cba0c
  Args:
    source: Charles Napoléon Bonaparte
    type: :Man
  AssignClass (af8c315f-61b8-4401-877b-127255952b18)
 Call ID: af8c315f-61b8-4401-877b-127255952b18
  Args:
    source: Charles Napoléon Bonaparte
    type: :Person
  AddLiteral (6e9785b4-6f9b-469d-bec7-109e69ca9d83)
 Call ID: 6e9785b4-6f9b-469d-bec7-109e69ca9d83
  Args:
    relation: :hasMarriageYear
    literal_value: 1978
    source: Princess Béatrice Marie Caroline Louise Françoise of Bourbon-Two Sicilies
    literal_type: xsd:integer
  AddTriple (f88b218a-ccdb-4a15-9bd9-12b701594ee6)
 Call ID: f88b218a-ccdb-4a15-9bd9-12b701594ee6
  Args:
    target: Charles Napoléon Bonaparte
    relation: :hasRelation
    source: Princess Béatrice Marie Caroline Louise Françoise of Bourbon-Two Sicilies
  AssignClass (7a969ef3-a371-439c-a575-964d97943515)
 Call ID: 7a969ef3-a371-439c-a575-964d97943515
  Args:
    type: :Man
    source: Louis, Prince Napoléon
  AssignClass (d345bf3b-8012-4d36-9581-130dc9a74a7b)
 Call ID: d345bf3b-8012-4d36-9581-130dc9a74a7b
  Args:
    source: Louis, Prince Napoléon
    type: :Person
  AssignClass (26827463-139c-4c49-aac1-02c0c9bbe65f)
 Call ID: 26827463-139c-4c49-aac1-02c0c9bbe65f
  Args:
    source: Alix de Foresta
    type: :Woman
  AssignClass (89b581ea-016c-4690-bec2-57b3eb82d577)
 Call ID: 89b581ea-016c-4690-bec2-57b3eb82d577
  Args:
    source: Alix de Foresta
    type: :Person
  AddTriple (39910c8b-adf0-4ab8-9a0d-683787e14a5c)
 Call ID: 39910c8b-adf0-4ab8-9a0d-683787e14a5c
  Args:
    target: Louis, Prince Napoléon
    source: Charles Napoléon Bonaparte
    relation: :hasFather
  AddTriple (b4f058df-e7b6-42a4-b4f2-ebea8f617c0d)
 Call ID: b4f058df-e7b6-42a4-b4f2-ebea8f617c0d
  Args:
    target: Alix de Foresta
    relation: :hasMother
    source: Charles Napoléon Bonaparte
  Finish (76958be3-2e31-4036-96da-2cbad0e86781)
 Call ID: 76958be3-2e31-4036-96da-2cbad0e86781
  Args: