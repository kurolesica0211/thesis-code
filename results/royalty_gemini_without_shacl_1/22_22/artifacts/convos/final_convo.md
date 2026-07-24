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
  AssignClass (81f4d29d-3580-419b-a524-943e5ec8709a)
 Call ID: 81f4d29d-3580-419b-a524-943e5ec8709a
  Args:
    source: Princess_Maria-Olympia_of_Greece_and_Denmark
    type: :Woman
  AssignClass (6372f2f0-1084-4d37-9b7f-bb6781302574)
 Call ID: 6372f2f0-1084-4d37-9b7f-bb6781302574
  Args:
    type: :Person
    source: Princess_Maria-Olympia_of_Greece_and_Denmark
  AddLiteral (2989a1f0-f8f5-44fa-b065-3c46ef2ae869)
 Call ID: 2989a1f0-f8f5-44fa-b065-3c46ef2ae869
  Args:
    source: Princess_Maria-Olympia_of_Greece_and_Denmark
    literal_type: xsd:string
    relation: :knownAs
    literal_value: Olympia
  AddLiteral (b3bca1dd-7ce2-45f9-8591-89f390e8949a)
 Call ID: b3bca1dd-7ce2-45f9-8591-89f390e8949a
  Args:
    literal_type: xsd:integer
    literal_value: 1996
    relation: :hasBirthYear
    source: Princess_Maria-Olympia_of_Greece_and_Denmark
  AssignClass (b9b38b15-0653-4c8f-aeed-cba6da58aed2)
 Call ID: b9b38b15-0653-4c8f-aeed-cba6da58aed2
  Args:
    type: :Man
    source: Pavlos_Crown_Prince_of_Greece
  AssignClass (822aa4a8-3d2a-4e08-aa3d-1161c00e78d3)
 Call ID: 822aa4a8-3d2a-4e08-aa3d-1161c00e78d3
  Args:
    source: Pavlos_Crown_Prince_of_Greece
    type: :Person
  AssignClass (ca644e19-e530-4392-9e71-b69efd66828a)
 Call ID: ca644e19-e530-4392-9e71-b69efd66828a
  Args:
    type: :Woman
    source: Marie-Chantal_Miller
  AssignClass (e9dd663d-b282-4e0c-ba8d-200cde7d6b3d)
 Call ID: e9dd663d-b282-4e0c-ba8d-200cde7d6b3d
  Args:
    source: Marie-Chantal_Miller
    type: :Person
  AddTriple (4d108e6c-d003-4020-a898-fed7b299c666)
 Call ID: 4d108e6c-d003-4020-a898-fed7b299c666
  Args:
    target: Pavlos_Crown_Prince_of_Greece
    relation: :hasFather
    source: Princess_Maria-Olympia_of_Greece_and_Denmark
  AddTriple (e0299381-8af8-4700-98ec-eecfa55863d7)
 Call ID: e0299381-8af8-4700-98ec-eecfa55863d7
  Args:
    source: Princess_Maria-Olympia_of_Greece_and_Denmark
    target: Marie-Chantal_Miller
    relation: :hasMother
  AssignClass (0ef06c7a-3627-4a9c-86eb-bb0abe3f1dcd)
 Call ID: 0ef06c7a-3627-4a9c-86eb-bb0abe3f1dcd
  Args:
    type: :Man
    source: Constantine_II_of_Greece
  AssignClass (f23ec29a-c685-4ebd-805a-6ba48e65d0e8)
 Call ID: f23ec29a-c685-4ebd-805a-6ba48e65d0e8
  Args:
    source: Constantine_II_of_Greece
    type: :Person
  AssignClass (7c217e2b-e7fa-4cbc-b7ac-e061fe90c68c)
 Call ID: 7c217e2b-e7fa-4cbc-b7ac-e061fe90c68c
  Args:
    source: Anne-Marie_of_Denmark
    type: :Woman
  AssignClass (a6ca3bac-4d12-4503-a619-bd2fee37db10)
 Call ID: a6ca3bac-4d12-4503-a619-bd2fee37db10
  Args:
    type: :Person
    source: Anne-Marie_of_Denmark
  AddTriple (760fc20c-feb6-4fa6-8b02-99368dd74164)
 Call ID: 760fc20c-feb6-4fa6-8b02-99368dd74164
  Args:
    source: Pavlos_Crown_Prince_of_Greece
    target: Constantine_II_of_Greece
    relation: :hasFather
  AddTriple (79532ea8-1e88-4edc-965a-d92832a11682)
 Call ID: 79532ea8-1e88-4edc-965a-d92832a11682
  Args:
    relation: :hasMother
    target: Anne-Marie_of_Denmark
    source: Pavlos_Crown_Prince_of_Greece
  AssignClass (73f9cef7-e45a-41d3-bb23-8f20a6d40d59)
 Call ID: 73f9cef7-e45a-41d3-bb23-8f20a6d40d59
  Args:
    type: :Man
    source: Robert_Warren_Miller
  AssignClass (00be2dc3-6e74-461d-9e16-5a30f8d1ed3d)
 Call ID: 00be2dc3-6e74-461d-9e16-5a30f8d1ed3d
  Args:
    type: :Person
    source: Robert_Warren_Miller
  AddTriple (737757d7-bf46-456f-ace3-0b16dfcb417d)
 Call ID: 737757d7-bf46-456f-ace3-0b16dfcb417d
  Args:
    source: Marie-Chantal_Miller
    target: Robert_Warren_Miller
    relation: :hasFather
  AssignClass (1fde26cc-6fee-4b57-ab14-9dca93735d0a)
 Call ID: 1fde26cc-6fee-4b57-ab14-9dca93735d0a
  Args:
    source: Prince_Constantine-Alexios
    type: :Man
  AssignClass (7f6e52b6-369d-4b79-bc74-076a74be3090)
 Call ID: 7f6e52b6-369d-4b79-bc74-076a74be3090
  Args:
    source: Prince_Constantine-Alexios
    type: :Person
  AssignClass (e37c4f25-9f6d-4273-8cfa-edb372bd906e)
 Call ID: e37c4f25-9f6d-4273-8cfa-edb372bd906e
  Args:
    source: Prince_Achileas-Andreas
    type: :Man
  AssignClass (581a0f9c-b6ee-4424-ac95-81b76caa7011)
 Call ID: 581a0f9c-b6ee-4424-ac95-81b76caa7011
  Args:
    source: Prince_Achileas-Andreas
    type: :Person
  AssignClass (81ac83ea-d3e6-4f83-801a-0ddfbd4be32e)
 Call ID: 81ac83ea-d3e6-4f83-801a-0ddfbd4be32e
  Args:
    type: :Man
    source: Prince_Odysseas_Kimon
  AssignClass (cd2b1b3d-0fc6-4abd-a8d2-53a4d698d1a2)
 Call ID: cd2b1b3d-0fc6-4abd-a8d2-53a4d698d1a2
  Args:
    type: :Person
    source: Prince_Odysseas_Kimon
  AssignClass (417a988f-93bc-4752-a85f-ac29a8647c27)
 Call ID: 417a988f-93bc-4752-a85f-ac29a8647c27
  Args:
    type: :Man
    source: Prince_Aristidis-Stavros
  AssignClass (8bfb05fc-cc1f-4830-b99d-f5d71dc9a513)
 Call ID: 8bfb05fc-cc1f-4830-b99d-f5d71dc9a513
  Args:
    source: Prince_Aristidis-Stavros
    type: :Person
  AddTriple (3cbcb738-930f-42b7-92ca-a5a5432dc922)
 Call ID: 3cbcb738-930f-42b7-92ca-a5a5432dc922
  Args:
    source: Princess_Maria-Olympia_of_Greece_and_Denmark
    relation: :isSiblingOf
    target: Prince_Constantine-Alexios
  AddTriple (8c71b91a-74ae-4251-9e83-82fd6f46e811)
 Call ID: 8c71b91a-74ae-4251-9e83-82fd6f46e811
  Args:
    relation: :isSiblingOf
    target: Prince_Achileas-Andreas
    source: Princess_Maria-Olympia_of_Greece_and_Denmark
  AddTriple (5682383d-e1de-4a03-aa8e-3f186412bdf0)
 Call ID: 5682383d-e1de-4a03-aa8e-3f186412bdf0
  Args:
    relation: :isSiblingOf
    target: Prince_Odysseas_Kimon
    source: Princess_Maria-Olympia_of_Greece_and_Denmark
  AddTriple (b24d8a1f-30da-4851-b85d-6399b85586e2)
 Call ID: b24d8a1f-30da-4851-b85d-6399b85586e2
  Args:
    target: Prince_Aristidis-Stavros
    relation: :isSiblingOf
    source: Princess_Maria-Olympia_of_Greece_and_Denmark
  AssignClass (9bd734e8-9878-4125-b29d-17cad82f6d7e)
 Call ID: 9bd734e8-9878-4125-b29d-17cad82f6d7e
  Args:
    source: Princess_Alexia_of_Greece_and_Denmark
    type: :Woman
  AssignClass (60359ed7-63cb-4240-a564-464b2b5ae106)
 Call ID: 60359ed7-63cb-4240-a564-464b2b5ae106
  Args:
    type: :Person
    source: Princess_Alexia_of_Greece_and_Denmark
  AssignClass (df9bc549-fdbb-4e71-b128-89ac4c5d5641)
 Call ID: df9bc549-fdbb-4e71-b128-89ac4c5d5641
  Args:
    type: :Woman
    source: Pia_Getty
  AssignClass (6ea450a2-4734-4d91-9dd7-5dc7e8c5d25d)
 Call ID: 6ea450a2-4734-4d91-9dd7-5dc7e8c5d25d
  Args:
    type: :Person
    source: Pia_Getty
  AssignClass (b289e646-dc33-439f-9ffc-1f40dc3b1889)
 Call ID: b289e646-dc33-439f-9ffc-1f40dc3b1889
  Args:
    type: :Man
    source: Charles_III
  AssignClass (e4d5eb02-c16f-41e2-b70f-7a91c359d9f9)
 Call ID: e4d5eb02-c16f-41e2-b70f-7a91c359d9f9
  Args:
    source: Charles_III
    type: :Person
  AssignClass (d9a28093-75d7-4104-a45d-496d3e4b0840)
 Call ID: d9a28093-75d7-4104-a45d-496d3e4b0840
  Args:
    source: Prince_Michael_of_Greece_and_Denmark
    type: :Man
  AssignClass (1977cbe3-18a6-4d53-a1bd-e97653ed32f7)
 Call ID: 1977cbe3-18a6-4d53-a1bd-e97653ed32f7
  Args:
    type: :Person
    source: Prince_Michael_of_Greece_and_Denmark
  AssignClass (ab4a5ab0-3c4a-4af4-b9f3-b521505d81f3)
 Call ID: ab4a5ab0-3c4a-4af4-b9f3-b521505d81f3
  Args:
    source: Queen_Sofia_of_Spain
    type: :Woman
  AssignClass (bb230a88-ec3a-4c16-8a03-6f4dc6081830)
 Call ID: bb230a88-ec3a-4c16-8a03-6f4dc6081830
  Args:
    source: Queen_Sofia_of_Spain
    type: :Person
  AssignClass (90d2157a-3869-4cd0-aaaa-a43fa10bc6e7)
 Call ID: 90d2157a-3869-4cd0-aaaa-a43fa10bc6e7
  Args:
    type: :Woman
    source: Marina_consort_of_Prince_Michael
  AssignClass (458e818e-ee66-4ffe-8021-3d88e5b78572)
 Call ID: 458e818e-ee66-4ffe-8021-3d88e5b78572
  Args:
    source: Marina_consort_of_Prince_Michael
    type: :Person
  AssignClass (78787564-3a40-4496-8ccd-863842dd7206)
 Call ID: 78787564-3a40-4496-8ccd-863842dd7206
  Args:
    source: Princess_Theodora_of_Greece_and_Denmark
    type: :Woman
  AssignClass (f7548ca3-8f1e-4a6f-8ef8-32b898680ae4)
 Call ID: f7548ca3-8f1e-4a6f-8ef8-32b898680ae4
  Args:
    source: Princess_Theodora_of_Greece_and_Denmark
    type: :Person
  AssignClass (b923648b-df02-4125-a0fd-981346cbb3cb)
 Call ID: b923648b-df02-4125-a0fd-981346cbb3cb
  Args:
    type: :Man
    source: Matthew_Kumar
  AssignClass (6bf72d6d-c046-4cf3-8d70-57b8e2848791)
 Call ID: 6bf72d6d-c046-4cf3-8d70-57b8e2848791
  Args:
    type: :Person
    source: Matthew_Kumar
  Finish (98dd4921-a7a5-44fa-b754-0913f89a65a4)
 Call ID: 98dd4921-a7a5-44fa-b754-0913f89a65a4
  Args: