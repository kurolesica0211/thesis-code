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
Charles Augustus, Hereditary Grand Duke of Saxe-Weimar-Eisenach (Carl August Wilhelm Ernst Friedrich Georg Johann Albrecht; 28 July 1912 – 14 October 1988), was a German prince and head of the grand ducal house of Saxe-Weimar-Eisenach.
Life

He was born in Schloss Wilhelmsthal as the eldest son and heir of Wilhelm Ernst, Grand Duke of Saxe-Weimar-Eisenach, and his second wife, Princess Feodora of Saxe-Meiningen.
When his father died on 24 April 1923, Charles Augustus succeeded him as head of the House of Saxe-Weimar-Eisenach.
Charles Augustus died at Schienen and was succeeded as head of the grand ducal house by his son, Michael.
Marriage and issue

Charles Augustus was married at the Wartburg Castle on 5 October 1944 to Baroness Elisabeth of Wangenheim-Winterstein (Tübingen, 16 January 1912 – Munich, 15 March 2010), daughter of Othmar Baron von Wangenheim-Winterstein and wife, Baroness Maud von Trützschler.



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
  AssignClass (bfc76325-078b-410d-8efc-a360a822e011)
 Call ID: bfc76325-078b-410d-8efc-a360a822e011
  Args:
    type: :Man
    source: Charles_Augustus
  AssignClass (a5004aae-eab3-4957-9fb4-fc948a5822bd)
 Call ID: a5004aae-eab3-4957-9fb4-fc948a5822bd
  Args:
    type: :Person
    source: Charles_Augustus
  AddLiteral (6c2822f3-6098-4eeb-9dc4-92300f52cad1)
 Call ID: 6c2822f3-6098-4eeb-9dc4-92300f52cad1
  Args:
    source: Charles_Augustus
    literal_value: Male
    literal_type: xsd:string
    relation: :hasSex
  AddLiteral (82d96d56-70b0-4eb1-9fe0-3082798d05df)
 Call ID: 82d96d56-70b0-4eb1-9fe0-3082798d05df
  Args:
    source: Charles_Augustus
    literal_value: 1912
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (de8fb996-5d06-4d73-95f3-66cf30d44738)
 Call ID: de8fb996-5d06-4d73-95f3-66cf30d44738
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: Charles_Augustus
    literal_value: 1988
  AssignClass (8d3892b7-1ae9-4a18-99c6-daa1ec1e4df7)
 Call ID: 8d3892b7-1ae9-4a18-99c6-daa1ec1e4df7
  Args:
    type: :Man
    source: Wilhelm_Ernst
  AssignClass (dc207aa8-0626-49a9-a5ba-893f288e4dc7)
 Call ID: dc207aa8-0626-49a9-a5ba-893f288e4dc7
  Args:
    type: :Person
    source: Wilhelm_Ernst
  AssignClass (cca89efb-9275-4505-b810-e3f9df65648c)
 Call ID: cca89efb-9275-4505-b810-e3f9df65648c
  Args:
    type: :Woman
    source: Feodora_of_Saxe-Meiningen
  AssignClass (4405c1c0-903a-4fe0-bbbe-b1bbfb124369)
 Call ID: 4405c1c0-903a-4fe0-bbbe-b1bbfb124369
  Args:
    type: :Person
    source: Feodora_of_Saxe-Meiningen
  AddTriple (110d5457-17ba-446f-b8ed-8eb6c1ff0528)
 Call ID: 110d5457-17ba-446f-b8ed-8eb6c1ff0528
  Args:
    source: Charles_Augustus
    target: Wilhelm_Ernst
    relation: :hasFather
  AddTriple (376a093a-1ace-4520-99ea-5f0831b61c9e)
 Call ID: 376a093a-1ace-4520-99ea-5f0831b61c9e
  Args:
    target: Feodora_of_Saxe-Meiningen
    source: Charles_Augustus
    relation: :hasMother
  AssignClass (71e101b4-78c4-468b-8387-155bad1d8f59)
 Call ID: 71e101b4-78c4-468b-8387-155bad1d8f59
  Args:
    type: :Man
    source: Michael
  AssignClass (d8c5684a-758f-42ea-ac1e-56504d236fef)
 Call ID: d8c5684a-758f-42ea-ac1e-56504d236fef
  Args:
    type: :Person
    source: Michael
  AddTriple (e6d9b8bb-0251-42e8-9f80-3cd343e37eb2)
 Call ID: e6d9b8bb-0251-42e8-9f80-3cd343e37eb2
  Args:
    relation: :isFatherOf
    source: Charles_Augustus
    target: Michael
  AssignClass (56311a3f-d24b-441d-95df-cd4d0e15e17b)
 Call ID: 56311a3f-d24b-441d-95df-cd4d0e15e17b
  Args:
    type: :Woman
    source: Elisabeth_of_Wangenheim-Winterstein
  AssignClass (2871b1df-4b1d-4740-9acd-488dc4603305)
 Call ID: 2871b1df-4b1d-4740-9acd-488dc4603305
  Args:
    type: :Person
    source: Elisabeth_of_Wangenheim-Winterstein
  AddLiteral (83bda11a-e1cb-4c4b-806e-c22b664091f2)
 Call ID: 83bda11a-e1cb-4c4b-806e-c22b664091f2
  Args:
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: Charles_Augustus
    literal_value: 1944
  AddTriple (a2dbee14-3c3b-42d5-a7bc-a5ec6fdd3621)
 Call ID: a2dbee14-3c3b-42d5-a7bc-a5ec6fdd3621
  Args:
    relation: :hasRelation
    target: Elisabeth_of_Wangenheim-Winterstein
    source: Charles_Augustus
  AddLiteral (8497fe2a-44cd-4e3d-bcfa-3ee1d47449b7)
 Call ID: 8497fe2a-44cd-4e3d-bcfa-3ee1d47449b7
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1912
    source: Elisabeth_of_Wangenheim-Winterstein
  AddLiteral (404fcc8a-dca5-4e3d-aa18-6d7279973cfd)
 Call ID: 404fcc8a-dca5-4e3d-aa18-6d7279973cfd
  Args:
    source: Elisabeth_of_Wangenheim-Winterstein
    literal_value: 2010
    literal_type: xsd:integer
    relation: :hasDeathYear
  AssignClass (a2636c29-35d0-4b67-9dfc-8bd369aa1177)
 Call ID: a2636c29-35d0-4b67-9dfc-8bd369aa1177
  Args:
    type: :Man
    source: Othmar_Baron_von_Wangenheim-Winterstein
  AssignClass (d58c2303-6e6a-4da4-85bc-a08f4c562d22)
 Call ID: d58c2303-6e6a-4da4-85bc-a08f4c562d22
  Args:
    type: :Person
    source: Othmar_Baron_von_Wangenheim-Winterstein
  AssignClass (679c0c4a-a4aa-409e-948d-fdb66e7d7c37)
 Call ID: 679c0c4a-a4aa-409e-948d-fdb66e7d7c37
  Args:
    type: :Woman
    source: Maud_von_Trützschler
  AssignClass (287b6e73-b1f9-46a0-9218-2913a0eff3ca)
 Call ID: 287b6e73-b1f9-46a0-9218-2913a0eff3ca
  Args:
    type: :Person
    source: Maud_von_Trützschler
  AddTriple (5906a756-0cf1-4d04-a135-7c8cd3e015d7)
 Call ID: 5906a756-0cf1-4d04-a135-7c8cd3e015d7
  Args:
    source: Elisabeth_of_Wangenheim-Winterstein
    target: Othmar_Baron_von_Wangenheim-Winterstein
    relation: :hasFather
  AddTriple (a67b2e90-6089-4102-ac00-b7a393fc967f)
 Call ID: a67b2e90-6089-4102-ac00-b7a393fc967f
  Args:
    relation: :hasMother
    target: Maud_von_Trützschler
    source: Elisabeth_of_Wangenheim-Winterstein
  Finish (374e18f1-31d7-4369-ab85-d96efe10e26e)
 Call ID: 374e18f1-31d7-4369-ab85-d96efe10e26e
  Args: