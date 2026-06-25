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
Wilhelm Karl Adalbert Erich Detloff Prinz von Preussen (30 January 1922 in Potsdam – 9 April 2007 in Holzminden) was the third son of Prince Oskar of Prussia, and the last surviving grandson of Wilhelm II, the last German Emperor.
Biography

Wilhelm-Karl was the youngest of Prince Oskar of Prussia and Countess Ina Marie von Bassewitz's four children.
Wilhelm-Karl worked tirelessly to keep the Order intact during the Cold War and helped to reunite its membership after the fall of East Germany.
Amongst other orders and awards, Wilhelm-Karl received the Grand Merit Cross (with star) of the Order of Merit of the Federal Republic of Germany and the Grand Cross of the Order pro merito Melitensi of the Sovereign Military Order of Malta.
Marriage and issue

In 1952, Wilhelm-Karl married Armgard Else Helene von Veltheim (17 February 1926 - 1 November 2019), daughter of Friedrich von Veltheim (1881–1955) and his wife, Ottonie von Alvensleben (1883–1960).



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
  AssignClass (ba1fd71d-b862-402d-9585-8d8be526be15)
 Call ID: ba1fd71d-b862-402d-9585-8d8be526be15
  Args:
    source: Wilhelm_Karl_Prinz_von_Preussen
    type: :Man
  AssignClass (e9a22901-8aa6-4bd4-9e2e-040f4ba2fb57)
 Call ID: e9a22901-8aa6-4bd4-9e2e-040f4ba2fb57
  Args:
    type: :Person
    source: Wilhelm_Karl_Prinz_von_Preussen
  AddLiteral (cea1202f-a2a6-488c-a7fd-0bc37a555d47)
 Call ID: cea1202f-a2a6-488c-a7fd-0bc37a555d47
  Args:
    source: Wilhelm_Karl_Prinz_von_Preussen
    literal_value: 1922
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (f3c76a10-636e-4dd6-8ed7-3489b217fc3a)
 Call ID: f3c76a10-636e-4dd6-8ed7-3489b217fc3a
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 2007
    source: Wilhelm_Karl_Prinz_von_Preussen
  AssignClass (9cef71fb-286c-4627-bb54-8cc535241e61)
 Call ID: 9cef71fb-286c-4627-bb54-8cc535241e61
  Args:
    source: Prince_Oskar_of_Prussia
    type: :Man
  AssignClass (11e7ddb4-2d8b-4a92-be64-ac66b62897a0)
 Call ID: 11e7ddb4-2d8b-4a92-be64-ac66b62897a0
  Args:
    type: :Person
    source: Prince_Oskar_of_Prussia
  AddTriple (1748bd27-72b4-438e-8133-4d3510ed2d45)
 Call ID: 1748bd27-72b4-438e-8133-4d3510ed2d45
  Args:
    source: Wilhelm_Karl_Prinz_von_Preussen
    relation: :hasFather
    target: Prince_Oskar_of_Prussia
  AssignClass (5afd73f1-4fd6-49e8-abcf-c26e18ae23d4)
 Call ID: 5afd73f1-4fd6-49e8-abcf-c26e18ae23d4
  Args:
    type: :Woman
    source: Ina_Marie_von_Bassewitz
  AssignClass (9c7f2e5c-12c8-4136-b71f-987eaf6f08ce)
 Call ID: 9c7f2e5c-12c8-4136-b71f-987eaf6f08ce
  Args:
    source: Ina_Marie_von_Bassewitz
    type: :Person
  AddTriple (e9ce55fa-5144-403d-8e68-d1fcc2810cdc)
 Call ID: e9ce55fa-5144-403d-8e68-d1fcc2810cdc
  Args:
    relation: :hasMother
    target: Ina_Marie_von_Bassewitz
    source: Wilhelm_Karl_Prinz_von_Preussen
  AssignClass (00a89a4e-b59f-4d1e-a3b2-1dcc6798e250)
 Call ID: 00a89a4e-b59f-4d1e-a3b2-1dcc6798e250
  Args:
    type: :Man
    source: Wilhelm_II
  AssignClass (32d4684c-c1c6-4b44-817a-6a1601d5f1be)
 Call ID: 32d4684c-c1c6-4b44-817a-6a1601d5f1be
  Args:
    source: Wilhelm_II
    type: :Person
  AssignClass (4aea82c4-83c1-4c10-ac11-c86f08c72fa2)
 Call ID: 4aea82c4-83c1-4c10-ac11-c86f08c72fa2
  Args:
    type: :Woman
    source: Armgard_Else_Helene_von_Veltheim
  AssignClass (3458dc22-0c32-4619-880e-faa135f86675)
 Call ID: 3458dc22-0c32-4619-880e-faa135f86675
  Args:
    type: :Person
    source: Armgard_Else_Helene_von_Veltheim
  AddLiteral (20006484-57aa-42e2-8191-0fbd5d90e61b)
 Call ID: 20006484-57aa-42e2-8191-0fbd5d90e61b
  Args:
    source: Wilhelm_Karl_Prinz_von_Preussen
    literal_value: 1952
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AddTriple (a64fee11-e377-4e87-9dea-1dd439177433)
 Call ID: a64fee11-e377-4e87-9dea-1dd439177433
  Args:
    relation: :hasRelation
    target: Armgard_Else_Helene_von_Veltheim
    source: Wilhelm_Karl_Prinz_von_Preussen
  AddLiteral (68ca06b7-6c52-4f32-82b6-5bcecaececb6)
 Call ID: 68ca06b7-6c52-4f32-82b6-5bcecaececb6
  Args:
    literal_type: xsd:integer
    literal_value: 1926
    relation: :hasBirthYear
    source: Armgard_Else_Helene_von_Veltheim
  AddLiteral (17d38cd9-be9d-4e1e-9476-2ac8493505be)
 Call ID: 17d38cd9-be9d-4e1e-9476-2ac8493505be
  Args:
    source: Armgard_Else_Helene_von_Veltheim
    relation: :hasDeathYear
    literal_value: 2019
    literal_type: xsd:integer
  AssignClass (749eba94-457b-498d-8b37-ef69640fbbdc)
 Call ID: 749eba94-457b-498d-8b37-ef69640fbbdc
  Args:
    source: Friedrich_von_Veltheim
    type: :Man
  AssignClass (e36a62c3-0e21-44f9-bb0c-60305907e05d)
 Call ID: e36a62c3-0e21-44f9-bb0c-60305907e05d
  Args:
    type: :Person
    source: Friedrich_von_Veltheim
  AddLiteral (8c999e92-9984-4da4-97df-302603b33bd6)
 Call ID: 8c999e92-9984-4da4-97df-302603b33bd6
  Args:
    source: Friedrich_von_Veltheim
    relation: :hasBirthYear
    literal_value: 1881
    literal_type: xsd:integer
  AddLiteral (c735b6ff-384f-42c0-b0bc-5cc8180bca80)
 Call ID: c735b6ff-384f-42c0-b0bc-5cc8180bca80
  Args:
    source: Friedrich_von_Veltheim
    literal_type: xsd:integer
    literal_value: 1955
    relation: :hasDeathYear
  AddTriple (02fd143d-cfae-4e2e-84e2-768268989133)
 Call ID: 02fd143d-cfae-4e2e-84e2-768268989133
  Args:
    relation: :hasFather
    target: Friedrich_von_Veltheim
    source: Armgard_Else_Helene_von_Veltheim
  AssignClass (f2a97326-63e6-4e8d-944b-1f6af17a998e)
 Call ID: f2a97326-63e6-4e8d-944b-1f6af17a998e
  Args:
    source: Ottonie_von_Alvensleben
    type: :Woman
  AssignClass (4bf64afd-0709-4040-af69-3bde3b6b1ca9)
 Call ID: 4bf64afd-0709-4040-af69-3bde3b6b1ca9
  Args:
    type: :Person
    source: Ottonie_von_Alvensleben
  AddLiteral (cddf938c-3cd4-4a27-aabf-f611a1b84c5e)
 Call ID: cddf938c-3cd4-4a27-aabf-f611a1b84c5e
  Args:
    source: Ottonie_von_Alvensleben
    literal_type: xsd:integer
    literal_value: 1883
    relation: :hasBirthYear
  AddLiteral (b14c7f77-3347-4f51-9c39-e363dad459de)
 Call ID: b14c7f77-3347-4f51-9c39-e363dad459de
  Args:
    relation: :hasDeathYear
    literal_value: 1960
    literal_type: xsd:integer
    source: Ottonie_von_Alvensleben
  AddTriple (af03f088-7af4-414d-9fbb-e3dc9a597169)
 Call ID: af03f088-7af4-414d-9fbb-e3dc9a597169
  Args:
    relation: :hasMother
    target: Ottonie_von_Alvensleben
    source: Armgard_Else_Helene_von_Veltheim
  Finish (815fcb04-1fcf-4c18-8129-1e268cba58fd)
 Call ID: 815fcb04-1fcf-4c18-8129-1e268cba58fd
  Args: