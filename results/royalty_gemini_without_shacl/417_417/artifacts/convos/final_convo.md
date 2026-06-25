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
Wittekind Adolf Heinrich Georg-Wilhelm, Prince of Waldeck and Pyrmont (Wittekind Adolf Heinrich Georg-Wilhelm Fürst zu Waldeck und Pyrmont; 9 March 1936 – 16 December 2024), was a member of the German nobility who from 1967 to 2024 was head of the House of Waldeck and Pyrmont.
Biography

Born in Arolsen (now Bad Arolsen) in Hesse, Germany, Wittekind was the only son of Josias Georg Wilhelm Adolf, Hereditary Prince of Waldeck and Pyrmont (1896−1967), an SS officer later found guilty of war crimes, and Duchess Altburg Marie Mathilde von Oldenburg (1903–2001), daughter of Frederick Augustus II, Grand Duke of Oldenburg.
He was the great-nephew of Emma of Waldeck and Pyrmont (later Queen of the Netherlands and Grand Duchess of Luxembourg) and thus a second cousin of Queen Beatrix of the Netherlands, whom he welcomed to Arolsen Castle in both 2008, on the 150th anniversary of Queen Emma's birth, and 2016, to celebrate his own 80th birthday.
Wittekind became head of the House of Waldeck and Pyrmont on his father's death in 1967.
Marriage and family

On 19 May 1988, in Frohnleiten, Wittekind married Countess Cecilia von Goëss-Saurau (born 1956), with whom he had three sons, including Carl-Anton, who succeeded him as Prince of Waldeck and Pyrmont.



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix ns1: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
@prefix ns2: <http://www.w3.org/2003/11/swrl#> .
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

ns1:isRuleEnabled a owl:AnnotationProperty .

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

:x a ns2:Variable .

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

:y a ns2:Variable .

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

[] a ns2:Imp ;
    rdfs:label "infer hasSon" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasBrother" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasSister" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (74310181-e53a-4dfe-934d-994cb7bafdac)
 Call ID: 74310181-e53a-4dfe-934d-994cb7bafdac
  Args:
    source: Wittekind_Adolf_Heinrich_Georg-Wilhelm
    type: :Man
  AssignClass (00756e19-6c0b-496c-9af5-d444d49bfd0a)
 Call ID: 00756e19-6c0b-496c-9af5-d444d49bfd0a
  Args:
    source: Wittekind_Adolf_Heinrich_Georg-Wilhelm
    type: :Person
  AddLiteral (d5481793-7e5e-47aa-9b55-d0011265aba2)
 Call ID: d5481793-7e5e-47aa-9b55-d0011265aba2
  Args:
    literal_value: 1936
    relation: :hasBirthYear
    source: Wittekind_Adolf_Heinrich_Georg-Wilhelm
    literal_type: xsd:integer
  AddLiteral (20ec67fb-41d9-459f-bccc-802670de42ea)
 Call ID: 20ec67fb-41d9-459f-bccc-802670de42ea
  Args:
    source: Wittekind_Adolf_Heinrich_Georg-Wilhelm
    relation: :hasDeathYear
    literal_value: 2024
    literal_type: xsd:integer
  AssignClass (ce4e7477-46d1-4dab-bbbc-1998c04fcab6)
 Call ID: ce4e7477-46d1-4dab-bbbc-1998c04fcab6
  Args:
    source: Josias_Georg_Wilhelm_Adolf
    type: :Man
  AssignClass (71fc0148-9a45-499b-a1ba-8d85a92ffdf6)
 Call ID: 71fc0148-9a45-499b-a1ba-8d85a92ffdf6
  Args:
    type: :Person
    source: Josias_Georg_Wilhelm_Adolf
  AddLiteral (7c885469-1c62-407a-83af-f54c73a477a4)
 Call ID: 7c885469-1c62-407a-83af-f54c73a477a4
  Args:
    source: Josias_Georg_Wilhelm_Adolf
    literal_value: 1896
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (7ee36a76-c5fd-46e8-9a78-e86cd5115e6f)
 Call ID: 7ee36a76-c5fd-46e8-9a78-e86cd5115e6f
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1967
    source: Josias_Georg_Wilhelm_Adolf
  AssignClass (77f37789-a22d-4a84-a3e3-ed2c25927992)
 Call ID: 77f37789-a22d-4a84-a3e3-ed2c25927992
  Args:
    type: :Woman
    source: Altburg_Marie_Mathilde_von_Oldenburg
  AssignClass (f6f3adea-2779-4ea3-96f5-c6650b5a0e1d)
 Call ID: f6f3adea-2779-4ea3-96f5-c6650b5a0e1d
  Args:
    source: Altburg_Marie_Mathilde_von_Oldenburg
    type: :Person
  AddLiteral (026d86a5-56f6-4bea-aa7c-9fc2ea75d30c)
 Call ID: 026d86a5-56f6-4bea-aa7c-9fc2ea75d30c
  Args:
    relation: :hasBirthYear
    literal_value: 1903
    source: Altburg_Marie_Mathilde_von_Oldenburg
    literal_type: xsd:integer
  AddLiteral (a58cc49b-345a-4130-84bc-a2f30d2318df)
 Call ID: a58cc49b-345a-4130-84bc-a2f30d2318df
  Args:
    literal_type: xsd:integer
    source: Altburg_Marie_Mathilde_von_Oldenburg
    literal_value: 2001
    relation: :hasDeathYear
  AddTriple (481cd4f0-4057-4601-aded-dca67704c8ef)
 Call ID: 481cd4f0-4057-4601-aded-dca67704c8ef
  Args:
    source: Wittekind_Adolf_Heinrich_Georg-Wilhelm
    target: Josias_Georg_Wilhelm_Adolf
    relation: :hasFather
  AddTriple (5573c828-fde9-4b0e-9812-f96840e928a3)
 Call ID: 5573c828-fde9-4b0e-9812-f96840e928a3
  Args:
    source: Wittekind_Adolf_Heinrich_Georg-Wilhelm
    relation: :hasMother
    target: Altburg_Marie_Mathilde_von_Oldenburg
  AssignClass (a0881f9b-328f-465e-b8de-a9095e6f1dcc)
 Call ID: a0881f9b-328f-465e-b8de-a9095e6f1dcc
  Args:
    source: Frederick_Augustus_II
    type: :Man
  AssignClass (b2ac60aa-70ec-45fb-bd57-d5e37e9242f1)
 Call ID: b2ac60aa-70ec-45fb-bd57-d5e37e9242f1
  Args:
    type: :Person
    source: Frederick_Augustus_II
  AddTriple (8363270c-593a-4f2c-8b1e-cdac41e6c523)
 Call ID: 8363270c-593a-4f2c-8b1e-cdac41e6c523
  Args:
    source: Altburg_Marie_Mathilde_von_Oldenburg
    relation: :hasFather
    target: Frederick_Augustus_II
  AssignClass (934305c0-5970-40a9-9b83-17a14821cab4)
 Call ID: 934305c0-5970-40a9-9b83-17a14821cab4
  Args:
    type: :Woman
    source: Cecilia_von_Goëss-Saurau
  AssignClass (04718258-0535-44b2-8e18-573bd3a52dbb)
 Call ID: 04718258-0535-44b2-8e18-573bd3a52dbb
  Args:
    source: Cecilia_von_Goëss-Saurau
    type: :Person
  AddLiteral (068793f6-c08e-4379-a8cc-535ae6cff70f)
 Call ID: 068793f6-c08e-4379-a8cc-535ae6cff70f
  Args:
    literal_value: 1956
    relation: :hasBirthYear
    source: Cecilia_von_Goëss-Saurau
    literal_type: xsd:integer
  AddLiteral (e6f12c2e-003c-4752-b72e-31527ee68a11)
 Call ID: e6f12c2e-003c-4752-b72e-31527ee68a11
  Args:
    literal_value: 1988
    relation: :hasMarriageYear
    source: Wittekind_Adolf_Heinrich_Georg-Wilhelm
    literal_type: xsd:integer
  AddTriple (a228cd06-3b0a-42a3-ab2a-3fb76cc48669)
 Call ID: a228cd06-3b0a-42a3-ab2a-3fb76cc48669
  Args:
    relation: :hasRelation
    target: Cecilia_von_Goëss-Saurau
    source: Wittekind_Adolf_Heinrich_Georg-Wilhelm
  AssignClass (df162252-c3f0-4dbe-bb0b-acdae342fbae)
 Call ID: df162252-c3f0-4dbe-bb0b-acdae342fbae
  Args:
    source: Carl-Anton
    type: :Man
  AssignClass (e9546e8b-0c96-41b8-9713-20c36afc9973)
 Call ID: e9546e8b-0c96-41b8-9713-20c36afc9973
  Args:
    type: :Person
    source: Carl-Anton
  AddTriple (b8c02c48-8ed7-4672-8494-fab434c22c40)
 Call ID: b8c02c48-8ed7-4672-8494-fab434c22c40
  Args:
    target: Wittekind_Adolf_Heinrich_Georg-Wilhelm
    relation: :hasFather
    source: Carl-Anton
  AddTriple (f3ccb2d8-11e7-4823-9bf2-cb99401adc22)
 Call ID: f3ccb2d8-11e7-4823-9bf2-cb99401adc22
  Args:
    target: Cecilia_von_Goëss-Saurau
    relation: :hasMother
    source: Carl-Anton
  Finish (1c779f6d-ebd1-4072-83b2-17ca2b7cfa3b)
 Call ID: 1c779f6d-ebd1-4072-83b2-17ca2b7cfa3b
  Args: