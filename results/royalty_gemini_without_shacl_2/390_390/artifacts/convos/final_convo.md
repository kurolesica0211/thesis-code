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
Franz Wilhelm Victor Christoph Stephan Prinz von Preussen (born 3 September 1943) is a German businessman and member of the House of Hohenzollern, the former ruling German imperial house and royal house of Prussia.
He is also the great-grandson of German Emperor Wilhelm II.
Biography

Franz Wilhelm Prince of Prussia was born in Grünberg, Silesia, as the son of Prince Karl Franz of Prussia and his first wife Princess Henriette von Schönaich-Carolath.
He had a twin brother, Prince Friedrich Christian, who died three weeks after his birth.
Prince Franz Wilhelm is a grandson of Prince Joachim of Prussia, the youngest son of Emperor Wilhelm II.
In 2002 Franz Wilhelm with Theodor Tantzen founded the Prinz von Preußen Grundbesitz AG, a project development and project management company which restores old buildings in Germany.
Personal life

Franz Wilhelm married his third cousin once removed, Grand Duchess Maria Vladimirovna of Russia, great-great-granddaughter of Queen Victoria, civilly on 4 September 1976 at Dinard and religiously on 22 September at the Russian Orthodox Chapel in Madrid.
Before his marriage, he converted to the Russian Orthodox faith and was created a Grand Duke of Russia with the name Mikhail Pavlovich by his father-in-law Grand Duke Vladimir of Russia.
Franz Wilhelm and Grand Duchess Maria had one son before divorcing on 19 June 1985 (they separated in 1982), at which point he reverted to his previous title.
He married Nadia Nour El Etreby (born 2 August 1949) on 14 March 2019, to whom was bestowed upon marriage the courtesy style and title of Her Royal Highness Princess Franz Wilhelm of Prussia.



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
  AssignClass (240e1244-b4ab-4cf8-811d-84483bceac40)
 Call ID: 240e1244-b4ab-4cf8-811d-84483bceac40
  Args:
    source: Franz_Wilhelm_Prinz_von_Preussen
    type: :Man
  AssignClass (b5e9a484-6f27-4a79-b815-3f739d0ce108)
 Call ID: b5e9a484-6f27-4a79-b815-3f739d0ce108
  Args:
    type: :Person
    source: Franz_Wilhelm_Prinz_von_Preussen
  AddLiteral (d3ceeab3-cca4-4025-9968-e3793350b3f7)
 Call ID: d3ceeab3-cca4-4025-9968-e3793350b3f7
  Args:
    source: Franz_Wilhelm_Prinz_von_Preussen
    literal_value: 1943
    relation: :hasBirthYear
    literal_type: xsd:integer
  AssignClass (81724fed-a269-4d95-a61c-34f6709d0a29)
 Call ID: 81724fed-a269-4d95-a61c-34f6709d0a29
  Args:
    type: :Man
    source: Karl_Franz_of_Prussia
  AssignClass (d1a67775-0edc-4055-897a-506884fba15e)
 Call ID: d1a67775-0edc-4055-897a-506884fba15e
  Args:
    type: :Person
    source: Karl_Franz_of_Prussia
  AssignClass (a3180743-bea1-42ed-8b78-a0fd5dc9f5d7)
 Call ID: a3180743-bea1-42ed-8b78-a0fd5dc9f5d7
  Args:
    source: Henriette_von_Schoenaich-Carolath
    type: :Woman
  AssignClass (51217ba9-e9d4-4c4b-b0b0-a0a4b701bcf7)
 Call ID: 51217ba9-e9d4-4c4b-b0b0-a0a4b701bcf7
  Args:
    type: :Person
    source: Henriette_von_Schoenaich-Carolath
  AddTriple (a15ce92b-d8fa-497c-b3a4-881e1745187e)
 Call ID: a15ce92b-d8fa-497c-b3a4-881e1745187e
  Args:
    relation: :hasFather
    target: Karl_Franz_of_Prussia
    source: Franz_Wilhelm_Prinz_von_Preussen
  AddTriple (668b12a3-077f-4ed5-a54c-0821d8a18d3d)
 Call ID: 668b12a3-077f-4ed5-a54c-0821d8a18d3d
  Args:
    relation: :hasMother
    source: Franz_Wilhelm_Prinz_von_Preussen
    target: Henriette_von_Schoenaich-Carolath
  AssignClass (befac9de-8587-41ed-89f7-724d7eea5bdf)
 Call ID: befac9de-8587-41ed-89f7-724d7eea5bdf
  Args:
    type: :Man
    source: Friedrich_Christian_of_Prussia
  AssignClass (2807e484-9b29-48f2-89df-9f032106fdcd)
 Call ID: 2807e484-9b29-48f2-89df-9f032106fdcd
  Args:
    type: :Person
    source: Friedrich_Christian_of_Prussia
  AddTriple (bc046734-8d13-46c0-b4b5-c4c000be1bb2)
 Call ID: bc046734-8d13-46c0-b4b5-c4c000be1bb2
  Args:
    relation: :isSiblingOf
    source: Franz_Wilhelm_Prinz_von_Preussen
    target: Friedrich_Christian_of_Prussia
  AssignClass (efdbbc18-b279-4b04-a02f-b2dad484c8f0)
 Call ID: efdbbc18-b279-4b04-a02f-b2dad484c8f0
  Args:
    source: Joachim_of_Prussia
    type: :Man
  AssignClass (6ed7b50f-ae72-45ae-bc7c-82de47910dde)
 Call ID: 6ed7b50f-ae72-45ae-bc7c-82de47910dde
  Args:
    type: :Person
    source: Joachim_of_Prussia
  AddTriple (60b45b00-eeb2-43ba-b8d4-114fdee53695)
 Call ID: 60b45b00-eeb2-43ba-b8d4-114fdee53695
  Args:
    target: Joachim_of_Prussia
    source: Franz_Wilhelm_Prinz_von_Preussen
    relation: :hasAncestor
  AssignClass (66e92631-4093-45b3-a42e-8ac8db204460)
 Call ID: 66e92631-4093-45b3-a42e-8ac8db204460
  Args:
    source: Wilhelm_II
    type: :Man
  AssignClass (806c2048-c6de-482f-a95a-3d5e413f1e03)
 Call ID: 806c2048-c6de-482f-a95a-3d5e413f1e03
  Args:
    type: :Person
    source: Wilhelm_II
  AddTriple (392ccc55-a2bd-45d9-b592-1daf096e3561)
 Call ID: 392ccc55-a2bd-45d9-b592-1daf096e3561
  Args:
    relation: :hasAncestor
    source: Franz_Wilhelm_Prinz_von_Preussen
    target: Wilhelm_II
  AddTriple (09feb38f-a094-448c-ae51-c4b10d907812)
 Call ID: 09feb38f-a094-448c-ae51-c4b10d907812
  Args:
    relation: :isFatherOf
    source: Wilhelm_II
    target: Joachim_of_Prussia
  AssignClass (3fe3fca9-8b13-4e85-bf67-848aa5c7fc04)
 Call ID: 3fe3fca9-8b13-4e85-bf67-848aa5c7fc04
  Args:
    type: :Woman
    source: Maria_Vladimirovna_of_Russia
  AssignClass (c0ad9cd6-106d-41c2-9393-83204c751c0f)
 Call ID: c0ad9cd6-106d-41c2-9393-83204c751c0f
  Args:
    source: Maria_Vladimirovna_of_Russia
    type: :Person
  AddLiteral (0a274272-b55b-464c-9870-cd4c6d6aa526)
 Call ID: 0a274272-b55b-464c-9870-cd4c6d6aa526
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    source: Franz_Wilhelm_Prinz_von_Preussen
    literal_value: 1976
  AssignClass (4aa81d95-c7af-4d9b-b4cb-1540aebffe14)
 Call ID: 4aa81d95-c7af-4d9b-b4cb-1540aebffe14
  Args:
    type: :Man
    source: Vladimir_of_Russia
  AssignClass (b2a81c46-bed3-48d6-9b72-e141f949e2a8)
 Call ID: b2a81c46-bed3-48d6-9b72-e141f949e2a8
  Args:
    type: :Person
    source: Vladimir_of_Russia
  AssignClass (6766130e-7431-49a9-a197-124c95966947)
 Call ID: 6766130e-7431-49a9-a197-124c95966947
  Args:
    source: Nadia_Nour_El_Etreby
    type: :Woman
  AssignClass (f368332b-8686-47eb-991e-f9217ebe5db6)
 Call ID: f368332b-8686-47eb-991e-f9217ebe5db6
  Args:
    source: Nadia_Nour_El_Etreby
    type: :Person
  AddLiteral (2722b01c-8cb9-4117-818e-7fb4c82eee1e)
 Call ID: 2722b01c-8cb9-4117-818e-7fb4c82eee1e
  Args:
    literal_value: 1949
    source: Nadia_Nour_El_Etreby
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (a5b4b0c1-1a8d-4a29-879c-1fa5d832ce01)
 Call ID: a5b4b0c1-1a8d-4a29-879c-1fa5d832ce01
  Args:
    source: Franz_Wilhelm_Prinz_von_Preussen
    literal_value: 2019
    relation: :hasMarriageYear
    literal_type: xsd:integer
  Finish (39d0b0d9-9a1a-4e1d-8754-0f08ec09f173)
 Call ID: 39d0b0d9-9a1a-4e1d-8754-0f08ec09f173
  Args: