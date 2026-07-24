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
Princess Beatrix*


Princess Margriet*Pieter van Vollenhoven*


Prince Floris Frederik Martijn of Orange-Nassau, van Vollenhoven (born 10 April 1975) is the fourth and youngest son of Princess Margriet of the Netherlands and Pieter van Vollenhoven.
Prince Floris has three older brothers: Prince Maurits, Prince Bernhard, Prince Pieter-Christiaan


Marriage and children

Prince Floris announced his engagement to Aimée Söhngen, the daughter of Hans Söhngen and Eleonoor Stammeijer, on 25 February 2005.
Prince Floris had been 10th in the line of succession to the Dutch throne but decided not to seek parliamentary approval for his marriage, as would be required in the Netherlands.
Prince Floris and Princess Aimée's first child, Magali Margriet Eleonoor van Vollenhoven, was born at VU University Medical Center in Amsterdam on 9 October 2007.
She is named for Aimée's sister, Magali Söhngen, and her mother Eleonoor, as well as Princess Margriet.
Their second child, Eliane Sophia Carolina van Vollenhoven, was born at VU University Medical Center in Amsterdam on 5 July 2009.
Their third child, a son named Willem Jan Johannes Pieter Floris, was born at HMC Bronovo  in The Hague on 1 July 2013.
Ancestry

References

2 gave up the title "Prince of the Netherlands, but still held the title "Prince of Orange-Nassau"
3 title granted by Royal Decree to descendants of Princess Irene



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
  AssignClass (597dd628-0d46-4ee5-9fb0-1c6d09f4e1df)
 Call ID: 597dd628-0d46-4ee5-9fb0-1c6d09f4e1df
  Args:
    type: :Woman
    source: Princess_Beatrix
  AssignClass (72164050-f1ce-4e14-8799-25ec9e77f6d1)
 Call ID: 72164050-f1ce-4e14-8799-25ec9e77f6d1
  Args:
    source: Princess_Margriet
    type: :Woman
  AssignClass (8317e2f5-de5e-47c8-b127-7f73db05a870)
 Call ID: 8317e2f5-de5e-47c8-b127-7f73db05a870
  Args:
    source: Pieter_van_Vollenhoven
    type: :Man
  AssignClass (18811f05-766f-4166-8ccd-99e4e6e469fd)
 Call ID: 18811f05-766f-4166-8ccd-99e4e6e469fd
  Args:
    source: Prince_Floris
    type: :Man
  AddLiteral (9243e44c-10e5-45b3-87ae-d85700d50a7f)
 Call ID: 9243e44c-10e5-45b3-87ae-d85700d50a7f
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Prince_Floris
    literal_value: 1975
  AddTriple (9226403a-f958-49b0-99eb-7dc03bde20a7)
 Call ID: 9226403a-f958-49b0-99eb-7dc03bde20a7
  Args:
    relation: :hasMother
    target: Princess_Margriet
    source: Prince_Floris
  AddTriple (7637e6fe-af35-4fe0-ad82-557b7da61733)
 Call ID: 7637e6fe-af35-4fe0-ad82-557b7da61733
  Args:
    relation: :hasFather
    source: Prince_Floris
    target: Pieter_van_Vollenhoven
  AssignClass (79336c79-dfce-41f6-9d72-d51edf24088e)
 Call ID: 79336c79-dfce-41f6-9d72-d51edf24088e
  Args:
    source: Prince_Maurits
    type: :Man
  AssignClass (54f1220c-a3d8-407f-a403-d580e3d90751)
 Call ID: 54f1220c-a3d8-407f-a403-d580e3d90751
  Args:
    type: :Man
    source: Prince_Bernhard
  AssignClass (2aa1623c-3404-413c-ace4-29c0d086c2c9)
 Call ID: 2aa1623c-3404-413c-ace4-29c0d086c2c9
  Args:
    source: Prince_Pieter_Christiaan
    type: :Man
  AddTriple (0d9c6d89-046c-453d-aae2-383c58c87ecb)
 Call ID: 0d9c6d89-046c-453d-aae2-383c58c87ecb
  Args:
    source: Prince_Maurits
    target: Prince_Floris
    relation: :isBrotherOf
  AddTriple (7e7d8c91-c545-4398-8ebd-33941e2ade3a)
 Call ID: 7e7d8c91-c545-4398-8ebd-33941e2ade3a
  Args:
    target: Prince_Floris
    source: Prince_Bernhard
    relation: :isBrotherOf
  AddTriple (7670634d-473a-4095-96dd-1353ac139456)
 Call ID: 7670634d-473a-4095-96dd-1353ac139456
  Args:
    relation: :isBrotherOf
    source: Prince_Pieter_Christiaan
    target: Prince_Floris
  AssignClass (ca1015f5-bfd4-4a8d-9e7c-399134baad90)
 Call ID: ca1015f5-bfd4-4a8d-9e7c-399134baad90
  Args:
    type: :Woman
    source: Aimee_Sohngen
  AssignClass (460cf2bf-8507-435f-9579-8f925f6a54eb)
 Call ID: 460cf2bf-8507-435f-9579-8f925f6a54eb
  Args:
    type: :Man
    source: Hans_Sohngen
  AssignClass (9bc54197-5e2c-4d0f-9e50-014029b9c7e9)
 Call ID: 9bc54197-5e2c-4d0f-9e50-014029b9c7e9
  Args:
    type: :Woman
    source: Eleonoor_Stammeijer
  AddTriple (dd943ee4-13c8-4474-905b-2889964b4e0d)
 Call ID: dd943ee4-13c8-4474-905b-2889964b4e0d
  Args:
    source: Aimee_Sohngen
    target: Hans_Sohngen
    relation: :hasFather
  AddTriple (1bc45128-c663-43f3-988d-4286c3a5851b)
 Call ID: 1bc45128-c663-43f3-988d-4286c3a5851b
  Args:
    relation: :hasMother
    source: Aimee_Sohngen
    target: Eleonoor_Stammeijer
  AssignClass (fdf8c81d-2f8f-4586-833b-b31e666453ac)
 Call ID: fdf8c81d-2f8f-4586-833b-b31e666453ac
  Args:
    type: :Woman
    source: Magali_Margriet_Eleonoor_van_Vollenhoven
  AddTriple (9ce97aa0-e03a-4a31-89bc-aa6213062af2)
 Call ID: 9ce97aa0-e03a-4a31-89bc-aa6213062af2
  Args:
    target: Prince_Floris
    source: Magali_Margriet_Eleonoor_van_Vollenhoven
    relation: :hasFather
  AddTriple (e13282f6-9bd6-4def-a524-cae2cd068d26)
 Call ID: e13282f6-9bd6-4def-a524-cae2cd068d26
  Args:
    target: Aimee_Sohngen
    source: Magali_Margriet_Eleonoor_van_Vollenhoven
    relation: :hasMother
  AssignClass (e859b47a-6063-44b3-87e2-eb5e9a088852)
 Call ID: e859b47a-6063-44b3-87e2-eb5e9a088852
  Args:
    type: :Woman
    source: Eliane_Sophia_Carolina_van_Vollenhoven
  AddTriple (e98ba748-926f-43e5-b818-45b527a82fc0)
 Call ID: e98ba748-926f-43e5-b818-45b527a82fc0
  Args:
    relation: :hasFather
    target: Prince_Floris
    source: Eliane_Sophia_Carolina_van_Vollenhoven
  AddTriple (a0be4a81-988d-4ad0-a492-a7fb6892ad50)
 Call ID: a0be4a81-988d-4ad0-a492-a7fb6892ad50
  Args:
    relation: :hasMother
    source: Eliane_Sophia_Carolina_van_Vollenhoven
    target: Aimee_Sohngen
  AssignClass (22146283-28da-4eec-ad04-171afe0960cf)
 Call ID: 22146283-28da-4eec-ad04-171afe0960cf
  Args:
    type: :Man
    source: Willem_Jan_Johannes_Pieter_Floris_van_Vollenhoven
  AddTriple (4c8f4b3d-9ca0-475c-88f0-8e581485322c)
 Call ID: 4c8f4b3d-9ca0-475c-88f0-8e581485322c
  Args:
    source: Willem_Jan_Johannes_Pieter_Floris_van_Vollenhoven
    target: Prince_Floris
    relation: :hasFather
  AddTriple (d3556426-ec60-4195-b13a-d1b538db4653)
 Call ID: d3556426-ec60-4195-b13a-d1b538db4653
  Args:
    source: Willem_Jan_Johannes_Pieter_Floris_van_Vollenhoven
    target: Aimee_Sohngen
    relation: :hasMother
  AssignClass (e5d2a473-255a-44c5-87ee-b0da012e04c9)
 Call ID: e5d2a473-255a-44c5-87ee-b0da012e04c9
  Args:
    type: :Woman
    source: Magali_Sohngen
  AddTriple (e257b48f-812a-43fe-a670-e7ad0d799c2c)
 Call ID: e257b48f-812a-43fe-a670-e7ad0d799c2c
  Args:
    source: Magali_Sohngen
    target: Aimee_Sohngen
    relation: :isSisterOf
  Finish (d371a2b3-ff37-413b-97b4-cba247a65571)
 Call ID: d371a2b3-ff37-413b-97b4-cba247a65571
  Args: