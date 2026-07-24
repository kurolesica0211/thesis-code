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
  AssignClass (67327941-61ac-443f-ac45-9734a5a9b693)
 Call ID: 67327941-61ac-443f-ac45-9734a5a9b693
  Args:
    type: :Person
    source: Princess Maria-Olympia of Greece and Denmark
  AssignClass (d797da38-d1c7-40ee-8109-4710455e1740)
 Call ID: d797da38-d1c7-40ee-8109-4710455e1740
  Args:
    source: Princess Maria-Olympia of Greece and Denmark
    type: :Woman
  AddLiteral (2305e4a9-a893-43c8-a4b3-1267f33cb6e0)
 Call ID: 2305e4a9-a893-43c8-a4b3-1267f33cb6e0
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1996
    source: Princess Maria-Olympia of Greece and Denmark
  AddLiteral (562f5e90-8ce7-4212-be6f-0a260030b3ce)
 Call ID: 562f5e90-8ce7-4212-be6f-0a260030b3ce
  Args:
    source: Princess Maria-Olympia of Greece and Denmark
    literal_type: xsd:string
    literal_value: Olympia
    relation: :knownAs
  AssignClass (9e47c267-bc85-48f7-a077-f55c597323e8)
 Call ID: 9e47c267-bc85-48f7-a077-f55c597323e8
  Args:
    type: :Person
    source: Pavlos, Crown Prince of Greece
  AssignClass (5d360b3d-999e-4971-8594-eebd59c35de9)
 Call ID: 5d360b3d-999e-4971-8594-eebd59c35de9
  Args:
    source: Pavlos, Crown Prince of Greece
    type: :Man
  AddTriple (59598cbf-1c41-400c-8935-d5d3b270700e)
 Call ID: 59598cbf-1c41-400c-8935-d5d3b270700e
  Args:
    target: Pavlos, Crown Prince of Greece
    source: Princess Maria-Olympia of Greece and Denmark
    relation: :hasFather
  AssignClass (42088fba-30f1-4be7-b4d0-7eadcc2b15c1)
 Call ID: 42088fba-30f1-4be7-b4d0-7eadcc2b15c1
  Args:
    type: :Person
    source: Marie-Chantal Miller
  AssignClass (cfafc7a6-9246-4ba6-a34c-15b79bdf5d48)
 Call ID: cfafc7a6-9246-4ba6-a34c-15b79bdf5d48
  Args:
    source: Marie-Chantal Miller
    type: :Woman
  AddTriple (78aafd27-29fd-44a9-bba7-accef8ef5981)
 Call ID: 78aafd27-29fd-44a9-bba7-accef8ef5981
  Args:
    relation: :hasMother
    target: Marie-Chantal Miller
    source: Princess Maria-Olympia of Greece and Denmark
  AssignClass (4a8d7c13-f50a-45d6-a758-065b9ccff620)
 Call ID: 4a8d7c13-f50a-45d6-a758-065b9ccff620
  Args:
    source: Constantine II of Greece
    type: :Person
  AssignClass (7d2539fa-b394-4f8d-af8e-df4ba5a58d4f)
 Call ID: 7d2539fa-b394-4f8d-af8e-df4ba5a58d4f
  Args:
    source: Constantine II of Greece
    type: :Man
  AssignClass (c4ef072f-2924-43d6-acb6-3c46bca73824)
 Call ID: c4ef072f-2924-43d6-acb6-3c46bca73824
  Args:
    type: :Person
    source: Anne-Marie of Denmark
  AssignClass (32251900-131d-4023-9a8c-f81fbb52f4a2)
 Call ID: 32251900-131d-4023-9a8c-f81fbb52f4a2
  Args:
    type: :Woman
    source: Anne-Marie of Denmark
  AddTriple (9f2db849-9c74-4fb5-b2dd-415a9151c3ae)
 Call ID: 9f2db849-9c74-4fb5-b2dd-415a9151c3ae
  Args:
    relation: :hasFather
    target: Constantine II of Greece
    source: Pavlos, Crown Prince of Greece
  AddTriple (e3db31b8-cec8-400f-a649-fe00a925bc74)
 Call ID: e3db31b8-cec8-400f-a649-fe00a925bc74
  Args:
    target: Anne-Marie of Denmark
    source: Pavlos, Crown Prince of Greece
    relation: :hasMother
  AssignClass (abac6c14-ae24-4d76-8068-1d0aeda548c1)
 Call ID: abac6c14-ae24-4d76-8068-1d0aeda548c1
  Args:
    source: Robert Warren Miller
    type: :Person
  AssignClass (aae11ed3-d0a3-423a-b4c2-311f29d2a7d6)
 Call ID: aae11ed3-d0a3-423a-b4c2-311f29d2a7d6
  Args:
    source: Robert Warren Miller
    type: :Man
  AddTriple (7330dd1b-f23b-457e-b8a2-bc27f412e781)
 Call ID: 7330dd1b-f23b-457e-b8a2-bc27f412e781
  Args:
    source: Marie-Chantal Miller
    target: Robert Warren Miller
    relation: :hasFather
  AssignClass (f49ae974-7c11-4ccd-96cb-85cb726318d5)
 Call ID: f49ae974-7c11-4ccd-96cb-85cb726318d5
  Args:
    type: :Person
    source: Prince Constantine-Alexios
  AssignClass (775c436f-37cb-4f2a-8af8-786c4084ecb1)
 Call ID: 775c436f-37cb-4f2a-8af8-786c4084ecb1
  Args:
    type: :Man
    source: Prince Constantine-Alexios
  AssignClass (14e3f231-0553-41e0-b411-5c57c3bcae3b)
 Call ID: 14e3f231-0553-41e0-b411-5c57c3bcae3b
  Args:
    type: :Person
    source: Prince Achileas-Andreas
  AssignClass (fc0df2e3-f37e-4dbe-a243-ab5a4102d3cb)
 Call ID: fc0df2e3-f37e-4dbe-a243-ab5a4102d3cb
  Args:
    type: :Man
    source: Prince Achileas-Andreas
  AssignClass (70ba6b0b-b574-49d9-a6fa-63a0490d5fd2)
 Call ID: 70ba6b0b-b574-49d9-a6fa-63a0490d5fd2
  Args:
    type: :Person
    source: Prince Odysseas Kimon
  AssignClass (382a521a-b231-463b-9bdb-4380539d162a)
 Call ID: 382a521a-b231-463b-9bdb-4380539d162a
  Args:
    source: Prince Odysseas Kimon
    type: :Man
  AssignClass (d3a57fbf-7e19-4a2f-8e26-7ad0990dc58d)
 Call ID: d3a57fbf-7e19-4a2f-8e26-7ad0990dc58d
  Args:
    type: :Person
    source: Prince Aristidis-Stavros
  AssignClass (7d3a2efe-8adb-424a-b058-7719944733da)
 Call ID: 7d3a2efe-8adb-424a-b058-7719944733da
  Args:
    type: :Man
    source: Prince Aristidis-Stavros
  AddTriple (dfde3d91-efde-46e5-beca-6c17f37f0d52)
 Call ID: dfde3d91-efde-46e5-beca-6c17f37f0d52
  Args:
    target: Prince Constantine-Alexios
    source: Princess Maria-Olympia of Greece and Denmark
    relation: :isSiblingOf
  AddTriple (46a92954-1f44-48a1-9016-92ccdc5cd396)
 Call ID: 46a92954-1f44-48a1-9016-92ccdc5cd396
  Args:
    relation: :isSiblingOf
    source: Princess Maria-Olympia of Greece and Denmark
    target: Prince Achileas-Andreas
  AddTriple (e3282499-aac1-4e6d-9cd3-f6264476b104)
 Call ID: e3282499-aac1-4e6d-9cd3-f6264476b104
  Args:
    source: Princess Maria-Olympia of Greece and Denmark
    target: Prince Odysseas Kimon
    relation: :isSiblingOf
  AddTriple (7e6f9a1c-8977-4c64-9dcf-9cb7dd290a44)
 Call ID: 7e6f9a1c-8977-4c64-9dcf-9cb7dd290a44
  Args:
    source: Princess Maria-Olympia of Greece and Denmark
    target: Prince Aristidis-Stavros
    relation: :isSiblingOf
  AssignClass (d14216aa-db17-48e9-8687-fe13a7c224d2)
 Call ID: d14216aa-db17-48e9-8687-fe13a7c224d2
  Args:
    source: Princess Alexia of Greece and Denmark
    type: :Person
  AssignClass (4813021d-7ad8-4a44-a097-1d7a52f921cf)
 Call ID: 4813021d-7ad8-4a44-a097-1d7a52f921cf
  Args:
    source: Princess Alexia of Greece and Denmark
    type: :Woman
  AddTriple (25a7f160-0296-4f77-979d-6380de918e45)
 Call ID: 25a7f160-0296-4f77-979d-6380de918e45
  Args:
    relation: :isSisterOf
    target: Pavlos, Crown Prince of Greece
    source: Princess Alexia of Greece and Denmark
  AssignClass (389f43ff-7c5c-472c-a54b-49d1dade5be6)
 Call ID: 389f43ff-7c5c-472c-a54b-49d1dade5be6
  Args:
    source: Princess Theodora of Greece and Denmark
    type: :Person
  AssignClass (8c138539-ed6e-493d-bd14-271f55e3ffeb)
 Call ID: 8c138539-ed6e-493d-bd14-271f55e3ffeb
  Args:
    source: Princess Theodora of Greece and Denmark
    type: :Woman
  AddTriple (202dd971-31e4-447c-912a-71173bdf6aa6)
 Call ID: 202dd971-31e4-447c-912a-71173bdf6aa6
  Args:
    relation: :isSisterOf
    source: Princess Theodora of Greece and Denmark
    target: Pavlos, Crown Prince of Greece
  AssignClass (596d7d47-cc44-4fbd-964b-c4e9ff5c917e)
 Call ID: 596d7d47-cc44-4fbd-964b-c4e9ff5c917e
  Args:
    type: :Person
    source: Matthew Kumar
  AssignClass (42fe92a6-6c76-45f3-b9b5-79c554867382)
 Call ID: 42fe92a6-6c76-45f3-b9b5-79c554867382
  Args:
    type: :Man
    source: Matthew Kumar
  AssignClass (ba2f90ae-ffe1-4b8a-a82d-cf2b173534f4)
 Call ID: ba2f90ae-ffe1-4b8a-a82d-cf2b173534f4
  Args:
    type: :Person
    source: Prince Michael of Greece and Denmark
  AssignClass (47eeb236-1023-414b-b837-0cb20e2da181)
 Call ID: 47eeb236-1023-414b-b837-0cb20e2da181
  Args:
    type: :Man
    source: Prince Michael of Greece and Denmark
  Finish (6d9b9524-9a20-4893-8aeb-239a996371d4)
 Call ID: 6d9b9524-9a20-4893-8aeb-239a996371d4
  Args: