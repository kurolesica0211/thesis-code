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
Queen Anne-Marie


Queen Sofía of Spain


Marina, consort of Prince Michael


Princess Maria-Olympia of Greece and Denmark (Greek: Μαρία Ολυμπία Ντε Γκρες, romanized: María-Olympía de Grèce; born 25 July 1996) is a fashion model, socialite and member of the former Greek royal family.
She is the oldest child and only daughter of Pavlos, Crown Prince of Greece, and his wife, Marie-Chantal Miller.
Her paternal grandparents are Constantine II of Greece and Anne-Marie of Denmark, who were the last King and Queen of the Hellenes, while her maternal grandfather is duty free entrepreneur Robert Warren Miller.
Early life

Princess Maria-Olympia of Greece and Denmark was born on 25 July 1996 at Weill Cornell Medical Center in Lenox Hill, New York in Manhattan to Pavlos, Crown Prince of Greece, and his wife, Marie-Chantal.
Her godparents are her paternal aunt Princess Alexia of Greece and Denmark, her maternal aunt Pia Getty, her grandfather's second cousin Charles III, and Prince Michael of Greece and Denmark.
She is the older sister of Prince Constantine-Alexios, Prince Achileas-Andreas, Prince Odysseas Kimon, and Prince Aristidis-Stavros.
She uses the name Olympia in everyday life.
Olympia attended her first couture show around the age of 11 in Rome together with her parents.
Maria-Olympia registered at college in New York in the fall of 2015.
Fashion career

In April 2016, Maria-Olympia posed alongside two of her first cousins, Isabel Getty and Princess Talita
She has modeled for Teen Vogue, Town & Country, Tatler, Hello!, ¡Hola!, and W. In June 2017, Maria-Olympia walked the runway for Dolce & Gabbana.
Using her name Olympia the Saks Potts S/S 2019 show during Copenhagen Fashion Week in August 2018 was named OLYMPIA after her and opened by the princess herself as the first model on the stage.
Personal life

It was reported in May 2016 that Maria-Olympia was romantically involved with her godfather's son and third cousin once removed Prince Harry, but a representative of the British royal family denied the rumors.
On 28 September 2024, she served as a bridesmaid at the wedding of her aunt Princess Theodora of Greece and Denmark and Matthew Kumar at the Metropolitan Cathedral in Athens.
Οn 20 December 2024, Maria-Olympia acquired Greek citizenship, along with other members of the former Greek royal family, under the surname de Grèce.



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
  AssignClass (f5e37391-9777-4e57-afba-2f2b5a79b525)
 Call ID: f5e37391-9777-4e57-afba-2f2b5a79b525
  Args:
    type: :Woman
    source: Maria-Olympia
  AssignClass (bd040abb-4840-4516-82e8-f14398839689)
 Call ID: bd040abb-4840-4516-82e8-f14398839689
  Args:
    type: :Person
    source: Maria-Olympia
  AddLiteral (aa3f03f0-3aa8-46a2-ae83-20a54ca944aa)
 Call ID: aa3f03f0-3aa8-46a2-ae83-20a54ca944aa
  Args:
    relation: :hasBirthYear
    literal_value: 1996
    source: Maria-Olympia
    literal_type: xsd:integer
  AddLiteral (b0992831-fc22-4c79-aeb1-75ab5cc6e041)
 Call ID: b0992831-fc22-4c79-aeb1-75ab5cc6e041
  Args:
    relation: :knownAs
    literal_value: Olympia
    literal_type: xsd:string
    source: Maria-Olympia
  AssignClass (3b85e61d-fe35-479e-a64b-b537e79da8dd)
 Call ID: 3b85e61d-fe35-479e-a64b-b537e79da8dd
  Args:
    source: Pavlos
    type: :Man
  AssignClass (e03ecf6a-be67-4cc6-a3ff-ef1e55412385)
 Call ID: e03ecf6a-be67-4cc6-a3ff-ef1e55412385
  Args:
    type: :Person
    source: Pavlos
  AssignClass (ab40fa28-6c08-438f-8cd0-435f3f640ebf)
 Call ID: ab40fa28-6c08-438f-8cd0-435f3f640ebf
  Args:
    type: :Woman
    source: Marie-Chantal
  AssignClass (e5dcae53-aa66-412e-a8f3-270d75ce2be8)
 Call ID: e5dcae53-aa66-412e-a8f3-270d75ce2be8
  Args:
    type: :Person
    source: Marie-Chantal
  AddTriple (a05b4f22-83b8-4329-b55a-7db0da6109c6)
 Call ID: a05b4f22-83b8-4329-b55a-7db0da6109c6
  Args:
    source: Maria-Olympia
    relation: :isChildOf
    target: Pavlos
  AddTriple (0bab7b31-db6b-4e75-a89e-5b2dc85de7ce)
 Call ID: 0bab7b31-db6b-4e75-a89e-5b2dc85de7ce
  Args:
    source: Maria-Olympia
    relation: :isChildOf
    target: Marie-Chantal
  AssignClass (bedcb6fd-636c-40b1-91c4-a2610e4edef8)
 Call ID: bedcb6fd-636c-40b1-91c4-a2610e4edef8
  Args:
    source: Constantine-II
    type: :Man
  AssignClass (fab1af64-1d8b-4a6f-8c99-e4cb49f813b1)
 Call ID: fab1af64-1d8b-4a6f-8c99-e4cb49f813b1
  Args:
    type: :Person
    source: Constantine-II
  AssignClass (073ba235-d050-49dd-945f-e827a86a93f2)
 Call ID: 073ba235-d050-49dd-945f-e827a86a93f2
  Args:
    type: :Woman
    source: Anne-Marie
  AssignClass (e483c687-6a6a-4bd6-bee8-998044200143)
 Call ID: e483c687-6a6a-4bd6-bee8-998044200143
  Args:
    source: Anne-Marie
    type: :Person
  AddTriple (9b121a5a-c04e-4a9e-bf7c-229dff6e38b5)
 Call ID: 9b121a5a-c04e-4a9e-bf7c-229dff6e38b5
  Args:
    target: Pavlos
    relation: :isFatherOf
    source: Constantine-II
  AddTriple (f2b2f4bf-9046-4111-a78a-0c054da6568f)
 Call ID: f2b2f4bf-9046-4111-a78a-0c054da6568f
  Args:
    relation: :isMotherOf
    source: Anne-Marie
    target: Pavlos
  AssignClass (7d448113-80bd-45fc-a8c3-fb65f25655aa)
 Call ID: 7d448113-80bd-45fc-a8c3-fb65f25655aa
  Args:
    type: :Man
    source: Robert-Warren-Miller
  AssignClass (2cb181b3-c5db-491c-8af5-a5f934922902)
 Call ID: 2cb181b3-c5db-491c-8af5-a5f934922902
  Args:
    type: :Person
    source: Robert-Warren-Miller
  AddTriple (75229f93-e44a-4a33-8577-6dc881ce5b94)
 Call ID: 75229f93-e44a-4a33-8577-6dc881ce5b94
  Args:
    target: Marie-Chantal
    relation: :isFatherOf
    source: Robert-Warren-Miller
  AssignClass (7bb98956-4d45-4963-a69d-707e6c1e1653)
 Call ID: 7bb98956-4d45-4963-a69d-707e6c1e1653
  Args:
    source: Constantine-Alexios
    type: :Man
  AssignClass (c19acb5f-50e6-458e-9ac7-585a4a7e94f5)
 Call ID: c19acb5f-50e6-458e-9ac7-585a4a7e94f5
  Args:
    source: Constantine-Alexios
    type: :Person
  AssignClass (ddbd41a9-30ec-4ecb-b2b3-fab23e6777c7)
 Call ID: ddbd41a9-30ec-4ecb-b2b3-fab23e6777c7
  Args:
    source: Achileas-Andreas
    type: :Man
  AssignClass (53ded78c-0beb-4059-a63d-6d556beae254)
 Call ID: 53ded78c-0beb-4059-a63d-6d556beae254
  Args:
    source: Achileas-Andreas
    type: :Person
  AssignClass (9d2198c3-50e9-4856-b99c-2ad57fd07080)
 Call ID: 9d2198c3-50e9-4856-b99c-2ad57fd07080
  Args:
    type: :Man
    source: Odysseas-Kimon
  AssignClass (9d18601a-80ed-40ec-b190-dc4240b9a5c8)
 Call ID: 9d18601a-80ed-40ec-b190-dc4240b9a5c8
  Args:
    source: Odysseas-Kimon
    type: :Person
  AssignClass (7d3d1142-7dfd-4a02-9a71-3166e238b1ac)
 Call ID: 7d3d1142-7dfd-4a02-9a71-3166e238b1ac
  Args:
    type: :Man
    source: Aristidis-Stavros
  AssignClass (d8905a1a-eca2-4126-9f59-7f59e3ed8778)
 Call ID: d8905a1a-eca2-4126-9f59-7f59e3ed8778
  Args:
    type: :Person
    source: Aristidis-Stavros
  AddTriple (dbce7b68-ec60-4f7d-b415-a3dc9fdc1d09)
 Call ID: dbce7b68-ec60-4f7d-b415-a3dc9fdc1d09
  Args:
    target: Constantine-Alexios
    relation: :isSiblingOf
    source: Maria-Olympia
  AddTriple (a4fa1fcd-f178-4a5a-908c-6c57cbf7e51a)
 Call ID: a4fa1fcd-f178-4a5a-908c-6c57cbf7e51a
  Args:
    target: Achileas-Andreas
    source: Maria-Olympia
    relation: :isSiblingOf
  AddTriple (7f6281e7-f4b0-4484-9c42-7da226bef427)
 Call ID: 7f6281e7-f4b0-4484-9c42-7da226bef427
  Args:
    relation: :isSiblingOf
    source: Maria-Olympia
    target: Odysseas-Kimon
  AddTriple (ea823aee-74e8-4327-afd9-769a8308468c)
 Call ID: ea823aee-74e8-4327-afd9-769a8308468c
  Args:
    relation: :isSiblingOf
    source: Maria-Olympia
    target: Aristidis-Stavros
  AssignClass (4bbfb51a-f633-4160-b796-f45cc93a4eda)
 Call ID: 4bbfb51a-f633-4160-b796-f45cc93a4eda
  Args:
    source: Alexia
    type: :Woman
  AssignClass (a99b0da6-3d0c-4fb5-9699-9872e7fe03ea)
 Call ID: a99b0da6-3d0c-4fb5-9699-9872e7fe03ea
  Args:
    type: :Person
    source: Alexia
  AddTriple (add517a1-335e-4c74-9e09-ff26c7029e64)
 Call ID: add517a1-335e-4c74-9e09-ff26c7029e64
  Args:
    target: Pavlos
    source: Alexia
    relation: :isSisterOf
  AssignClass (962db019-033c-42d3-8ae1-ff8d0fe37948)
 Call ID: 962db019-033c-42d3-8ae1-ff8d0fe37948
  Args:
    source: Pia-Getty
    type: :Woman
  AssignClass (6b54e7fb-6b88-4f0f-aa31-429fc48243d4)
 Call ID: 6b54e7fb-6b88-4f0f-aa31-429fc48243d4
  Args:
    type: :Person
    source: Pia-Getty
  AddTriple (a264458f-c000-4738-80c1-e2ceef927e03)
 Call ID: a264458f-c000-4738-80c1-e2ceef927e03
  Args:
    target: Marie-Chantal
    relation: :isSisterOf
    source: Pia-Getty
  AssignClass (bdb1de99-e5e3-412b-ba38-7bd65d73fd93)
 Call ID: bdb1de99-e5e3-412b-ba38-7bd65d73fd93
  Args:
    source: Charles-III
    type: :Man
  AssignClass (3d43443a-1810-4b34-a3db-b56ff8ed65d3)
 Call ID: 3d43443a-1810-4b34-a3db-b56ff8ed65d3
  Args:
    source: Charles-III
    type: :Person
  AssignClass (6ada6915-e8c4-4e2d-a623-0dd06aaaead8)
 Call ID: 6ada6915-e8c4-4e2d-a623-0dd06aaaead8
  Args:
    type: :Man
    source: Michael
  AssignClass (e6afd946-462f-4848-82c4-eeb16e6f25c0)
 Call ID: e6afd946-462f-4848-82c4-eeb16e6f25c0
  Args:
    source: Michael
    type: :Person
  AssignClass (76cbec80-403e-424c-b761-108717f76212)
 Call ID: 76cbec80-403e-424c-b761-108717f76212
  Args:
    type: :Woman
    source: Theodora
  AssignClass (7674c4d3-6528-4978-bb51-d371672fb9d5)
 Call ID: 7674c4d3-6528-4978-bb51-d371672fb9d5
  Args:
    source: Theodora
    type: :Person
  AddTriple (fd5815ae-6460-4275-ad0b-50b3138f6ab7)
 Call ID: fd5815ae-6460-4275-ad0b-50b3138f6ab7
  Args:
    target: Pavlos
    relation: :isSisterOf
    source: Theodora
  AssignClass (21f33ba9-0424-401f-8a7f-bab232eb0648)
 Call ID: 21f33ba9-0424-401f-8a7f-bab232eb0648
  Args:
    type: :Man
    source: Matthew-Kumar
  AssignClass (c4edc91d-973e-4aec-a93e-674565e133b7)
 Call ID: c4edc91d-973e-4aec-a93e-674565e133b7
  Args:
    type: :Person
    source: Matthew-Kumar
  AssignClass (b689efed-9f7e-4b0a-a59c-e22f697664b8)
 Call ID: b689efed-9f7e-4b0a-a59c-e22f697664b8
  Args:
    type: :Woman
    source: Isabel-Getty
  AssignClass (5796d1e1-dc78-4b5f-9c4a-8e78b5779cd6)
 Call ID: 5796d1e1-dc78-4b5f-9c4a-8e78b5779cd6
  Args:
    source: Isabel-Getty
    type: :Person
  AssignClass (90049005-ceff-4efa-8222-fe33b2e1b02b)
 Call ID: 90049005-ceff-4efa-8222-fe33b2e1b02b
  Args:
    type: :Woman
    source: Talita
  AssignClass (3ed6f79b-e2d4-44ee-aa30-6c8ed3a33d83)
 Call ID: 3ed6f79b-e2d4-44ee-aa30-6c8ed3a33d83
  Args:
    type: :Person
    source: Talita
  AssignClass (845c79a7-0816-4655-b57f-8e00e5f891af)
 Call ID: 845c79a7-0816-4655-b57f-8e00e5f891af
  Args:
    source: Harry
    type: :Man
  AssignClass (99fa57e2-150c-43c9-a8ec-ebab2ff2e94b)
 Call ID: 99fa57e2-150c-43c9-a8ec-ebab2ff2e94b
  Args:
    type: :Person
    source: Harry
  AssignClass (13505b4f-5b08-4fd9-a234-2d64f17eb4ad)
 Call ID: 13505b4f-5b08-4fd9-a234-2d64f17eb4ad
  Args:
    type: :Woman
    source: Sofia
  AssignClass (3def9128-bae1-4a8d-8f31-7d59b328650e)
 Call ID: 3def9128-bae1-4a8d-8f31-7d59b328650e
  Args:
    type: :Person
    source: Sofia
  AssignClass (5d1dd9d5-13ab-4e5c-8b25-b37270ef672c)
 Call ID: 5d1dd9d5-13ab-4e5c-8b25-b37270ef672c
  Args:
    source: Marina
    type: :Woman
  AssignClass (a6d03bfc-ced3-4850-9858-9eba0e0076e6)
 Call ID: a6d03bfc-ced3-4850-9858-9eba0e0076e6
  Args:
    type: :Person
    source: Marina
  Finish (a304c65c-862b-422e-92e1-5ae6b901a427)
 Call ID: a304c65c-862b-422e-92e1-5ae6b901a427
  Args: