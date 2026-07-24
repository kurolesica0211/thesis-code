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
Prince Henry Victor Louis Frederick of Prussia (German: Heinrich Viktor Ludwig Friedrich; 9 January 1900 – 26 February 1904), was the third son and youngest child of Prince Henry of Prussia and Princess Irene of Hesse and by Rhine.
He was a grandson of Frederick III, German Emperor, through his father and a great-grandson of Queen Victoria.
Life

Prince Heinrich was born on 9 January 1900, in Kiel.
His father was pleased by the birth of yet another son, especially such a handsome one, as the Prince had blonde hair.
The newborn Prince immediately received the title Prince of Prussia with the style Royal Highness, and was baptised
His older brothers were Prince Waldemar, a namesake of his uncle, and Prince Sigismund, a namesake of his other deceased uncle.
The Prince was diagnosed with haemophilia as a young child, but, despite this, was a very cheerful and lively boy who liked to play a lot.
As Henry grew older he became more aware of his condition.
Death

On 25 February, Princess Irene left Heinrich unsupervised for a few minutes while she went to fetch something.
The playful Prince climbed a chair, and then he climbed onto the table.
He started to scream, which immediately attracted the Princess' attention.
However, experiencing this condition, it was certain the young Prince would die.
Aftermath

Prince Heinrich's premature death would later very much affect the Princess, who would withdraw into herself.
One of his older brothers, Prince Waldemar, also had haemophilia.
The middle sibling, Prince Sigismund, was unaffected by the disease.



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
  AssignClass (8ae4296f-dcf8-4aa1-87c1-19387aec36a8)
 Call ID: 8ae4296f-dcf8-4aa1-87c1-19387aec36a8
  Args:
    type: :Man
    source: Prince_Henry_Victor_Louis_Frederick_of_Prussia
  AssignClass (1894059b-49af-40af-985c-3e570fbd5c65)
 Call ID: 1894059b-49af-40af-985c-3e570fbd5c65
  Args:
    type: :Person
    source: Prince_Henry_Victor_Louis_Frederick_of_Prussia
  AssignClass (573303a4-a4aa-4e9f-89fe-2c0a8110a31c)
 Call ID: 573303a4-a4aa-4e9f-89fe-2c0a8110a31c
  Args:
    type: :Man
    source: Prince_Henry_of_Prussia
  AssignClass (4851b388-12a6-4842-8b13-40fda9e43eac)
 Call ID: 4851b388-12a6-4842-8b13-40fda9e43eac
  Args:
    type: :Person
    source: Prince_Henry_of_Prussia
  AssignClass (089ac32f-a695-4c5b-8632-42484b7e6c69)
 Call ID: 089ac32f-a695-4c5b-8632-42484b7e6c69
  Args:
    type: :Woman
    source: Princess_Irene_of_Hesse_and_by_Rhine
  AssignClass (d73f9003-70c3-4ebd-b6ce-1056ca629a6b)
 Call ID: d73f9003-70c3-4ebd-b6ce-1056ca629a6b
  Args:
    type: :Person
    source: Princess_Irene_of_Hesse_and_by_Rhine
  AssignClass (0da7f9b9-1d81-4c06-b8ea-7ff59cd7241b)
 Call ID: 0da7f9b9-1d81-4c06-b8ea-7ff59cd7241b
  Args:
    type: :Man
    source: Frederick_III_German_Emperor
  AssignClass (af06b4e0-1ce2-429f-841a-dbd6e125b846)
 Call ID: af06b4e0-1ce2-429f-841a-dbd6e125b846
  Args:
    type: :Person
    source: Frederick_III_German_Emperor
  AssignClass (c81d6a31-d7bc-4928-a738-7b86f70a1747)
 Call ID: c81d6a31-d7bc-4928-a738-7b86f70a1747
  Args:
    type: :Woman
    source: Queen_Victoria
  AssignClass (73f9ee3b-735d-4c87-8ddf-331b8b19d0bb)
 Call ID: 73f9ee3b-735d-4c87-8ddf-331b8b19d0bb
  Args:
    type: :Person
    source: Queen_Victoria
  AssignClass (1d6ad229-00a0-4c7f-ac6e-0d90f68562eb)
 Call ID: 1d6ad229-00a0-4c7f-ac6e-0d90f68562eb
  Args:
    type: :Man
    source: Prince_Waldemar
  AssignClass (f8847a7b-611b-4edf-96ef-9d75bf0bcccd)
 Call ID: f8847a7b-611b-4edf-96ef-9d75bf0bcccd
  Args:
    type: :Person
    source: Prince_Waldemar
  AssignClass (cfac6a1b-4023-4332-a776-1fca9d2a5e5b)
 Call ID: cfac6a1b-4023-4332-a776-1fca9d2a5e5b
  Args:
    type: :Man
    source: Prince_Sigismund
  AssignClass (4d86d3c7-a7de-459d-a01a-0e644e84cef3)
 Call ID: 4d86d3c7-a7de-459d-a01a-0e644e84cef3
  Args:
    type: :Person
    source: Prince_Sigismund
  AddLiteral (eccab517-967f-44c6-a205-b952b6f98d77)
 Call ID: eccab517-967f-44c6-a205-b952b6f98d77
  Args:
    literal_type: xsd:nonNegativeInteger
    literal_value: 1900
    relation: :hasBirthYear
    source: Prince_Henry_Victor_Louis_Frederick_of_Prussia
  AddLiteral (0250e2c8-46a7-47e7-aa8e-9f3a33a965ed)
 Call ID: 0250e2c8-46a7-47e7-aa8e-9f3a33a965ed
  Args:
    source: Prince_Henry_Victor_Louis_Frederick_of_Prussia
    literal_type: xsd:nonNegativeInteger
    relation: :hasDeathYear
    literal_value: 1904
  AddTriple (b4a8114f-7298-4399-8dd8-4e85fd7b6b91)
 Call ID: b4a8114f-7298-4399-8dd8-4e85fd7b6b91
  Args:
    relation: :hasFather
    source: Prince_Henry_Victor_Louis_Frederick_of_Prussia
    target: Prince_Henry_of_Prussia
  AddTriple (4613263d-c372-423f-800c-29500ff59d76)
 Call ID: 4613263d-c372-423f-800c-29500ff59d76
  Args:
    source: Prince_Henry_Victor_Louis_Frederick_of_Prussia
    target: Princess_Irene_of_Hesse_and_by_Rhine
    relation: :hasMother
  AddTriple (ed9c8ef6-b83d-47ed-86a0-33d7bcfd355b)
 Call ID: ed9c8ef6-b83d-47ed-86a0-33d7bcfd355b
  Args:
    relation: :hasFather
    source: Prince_Henry_of_Prussia
    target: Frederick_III_German_Emperor
  AddTriple (48fd4a22-8038-4019-8109-88bca5fef76a)
 Call ID: 48fd4a22-8038-4019-8109-88bca5fef76a
  Args:
    source: Prince_Henry_Victor_Louis_Frederick_of_Prussia
    target: Queen_Victoria
    relation: :hasAncestor
  AddTriple (20259998-4f64-46e0-bdea-bae789e80ef9)
 Call ID: 20259998-4f64-46e0-bdea-bae789e80ef9
  Args:
    source: Prince_Henry_Victor_Louis_Frederick_of_Prussia
    target: Prince_Waldemar
    relation: :isSiblingOf
  AddTriple (b8b98414-edfc-4c9f-8bbd-981e3995a1d8)
 Call ID: b8b98414-edfc-4c9f-8bbd-981e3995a1d8
  Args:
    relation: :isSiblingOf
    target: Prince_Sigismund
    source: Prince_Henry_Victor_Louis_Frederick_of_Prussia
  AddTriple (884d6f59-66c5-40b7-b4ad-1d54cfd9046b)
 Call ID: 884d6f59-66c5-40b7-b4ad-1d54cfd9046b
  Args:
    target: Prince_Sigismund
    source: Prince_Waldemar
    relation: :isSiblingOf
  Finish (b35d7fb6-3660-4156-83c3-6fe83e571f36)
 Call ID: b35d7fb6-3660-4156-83c3-6fe83e571f36
  Args: