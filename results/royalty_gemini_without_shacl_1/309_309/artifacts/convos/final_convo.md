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
  AssignClass (67105620-323b-4c86-81bc-e366bfe5f999)
 Call ID: 67105620-323b-4c86-81bc-e366bfe5f999
  Args:
    source: Princess_Béatrice_of_Bourbon-Two_Sicilies
    type: :Woman
  AssignClass (e01f8701-41c3-4c2c-a703-b6e0ead07ca8)
 Call ID: e01f8701-41c3-4c2c-a703-b6e0ead07ca8
  Args:
    source: Princess_Béatrice_of_Bourbon-Two_Sicilies
    type: :Person
  AssignClass (0d34e082-c682-4cf0-a37c-2a96afd39440)
 Call ID: 0d34e082-c682-4cf0-a37c-2a96afd39440
  Args:
    source: Prince_Ferdinand_Duke_of_Castro
    type: :Man
  AssignClass (daf61964-1d3f-4c3f-a93c-457c25b107a5)
 Call ID: daf61964-1d3f-4c3f-a93c-457c25b107a5
  Args:
    source: Prince_Ferdinand_Duke_of_Castro
    type: :Person
  AssignClass (db730bd6-54f9-480e-9c15-530467052cf5)
 Call ID: db730bd6-54f9-480e-9c15-530467052cf5
  Args:
    type: :Ancestor
    source: Prince_Ferdinand_Duke_of_Castro
  AssignClass (a3b0aab6-132f-49b0-b334-bf15e5017e9c)
 Call ID: a3b0aab6-132f-49b0-b334-bf15e5017e9c
  Args:
    source: Chantal_de_Chevron-Villette
    type: :Woman
  AssignClass (4a1f8288-11ea-4f79-9578-30caa4ccc06d)
 Call ID: 4a1f8288-11ea-4f79-9578-30caa4ccc06d
  Args:
    type: :Person
    source: Chantal_de_Chevron-Villette
  AssignClass (6ba918f8-cb13-4fce-9a87-6c9e393fba34)
 Call ID: 6ba918f8-cb13-4fce-9a87-6c9e393fba34
  Args:
    source: Chantal_de_Chevron-Villette
    type: :Ancestor
  AssignClass (fa80bf60-a0be-4a1a-9544-ed0d05fc315e)
 Call ID: fa80bf60-a0be-4a1a-9544-ed0d05fc315e
  Args:
    source: Prince_Carlo_Duke_of_Castro
    type: :Man
  AssignClass (fa212268-5259-4da6-bdce-5fa2372538fd)
 Call ID: fa212268-5259-4da6-bdce-5fa2372538fd
  Args:
    type: :Person
    source: Prince_Carlo_Duke_of_Castro
  AssignClass (c981a7dc-efdd-4d98-8e21-0c9b2f4bd4a4)
 Call ID: c981a7dc-efdd-4d98-8e21-0c9b2f4bd4a4
  Args:
    type: :Man
    source: Charles_Napoléon_Bonaparte
  AssignClass (6d9068c8-7f3d-4485-97fe-afa497f449f3)
 Call ID: 6d9068c8-7f3d-4485-97fe-afa497f449f3
  Args:
    type: :Person
    source: Charles_Napoléon_Bonaparte
  AssignClass (c99a2577-c9c7-4b1a-b8fe-1808b30addca)
 Call ID: c99a2577-c9c7-4b1a-b8fe-1808b30addca
  Args:
    source: Louis_Prince_Napoléon
    type: :Man
  AssignClass (db27e12d-e405-4648-a7db-74a59fe04063)
 Call ID: db27e12d-e405-4648-a7db-74a59fe04063
  Args:
    source: Louis_Prince_Napoléon
    type: :Person
  AssignClass (fd1bab43-d760-4e33-a060-d840c8553d34)
 Call ID: fd1bab43-d760-4e33-a060-d840c8553d34
  Args:
    type: :Ancestor
    source: Louis_Prince_Napoléon
  AssignClass (c9c2a4e6-bcb1-4a71-a897-3d2731b930de)
 Call ID: c9c2a4e6-bcb1-4a71-a897-3d2731b930de
  Args:
    type: :Woman
    source: Alix_de_Foresta
  AssignClass (4fbee870-190b-4dd1-9682-29e49a4367db)
 Call ID: 4fbee870-190b-4dd1-9682-29e49a4367db
  Args:
    type: :Person
    source: Alix_de_Foresta
  AssignClass (05e2d321-18de-4059-8900-9dfb3b7f4810)
 Call ID: 05e2d321-18de-4059-8900-9dfb3b7f4810
  Args:
    type: :Ancestor
    source: Alix_de_Foresta
  AddLiteral (7fd037d0-8bee-43b2-947c-15b2992fa11e)
 Call ID: 7fd037d0-8bee-43b2-947c-15b2992fa11e
  Args:
    source: Princess_Béatrice_of_Bourbon-Two_Sicilies
    literal_type: xsd:integer
    literal_value: 1950
    relation: :hasBirthYear
  AddTriple (0c5dda0c-0776-45da-92da-5fb38e892ca6)
 Call ID: 0c5dda0c-0776-45da-92da-5fb38e892ca6
  Args:
    target: Prince_Ferdinand_Duke_of_Castro
    relation: :hasFather
    source: Princess_Béatrice_of_Bourbon-Two_Sicilies
  AddTriple (8301fa0e-ccc3-4f28-a30b-1c4fa9ee7e21)
 Call ID: 8301fa0e-ccc3-4f28-a30b-1c4fa9ee7e21
  Args:
    target: Chantal_de_Chevron-Villette
    relation: :hasMother
    source: Princess_Béatrice_of_Bourbon-Two_Sicilies
  AddTriple (156726a5-3ed8-484b-9067-86c1938bfcb4)
 Call ID: 156726a5-3ed8-484b-9067-86c1938bfcb4
  Args:
    relation: :isSiblingOf
    target: Prince_Carlo_Duke_of_Castro
    source: Princess_Béatrice_of_Bourbon-Two_Sicilies
  AddTriple (7621cbdf-b05d-4930-a626-8fcfc7e5cd75)
 Call ID: 7621cbdf-b05d-4930-a626-8fcfc7e5cd75
  Args:
    source: Prince_Carlo_Duke_of_Castro
    relation: :hasFather
    target: Prince_Ferdinand_Duke_of_Castro
  AddTriple (2fa430e3-d570-4a8e-93fa-93da7476cb82)
 Call ID: 2fa430e3-d570-4a8e-93fa-93da7476cb82
  Args:
    source: Prince_Carlo_Duke_of_Castro
    relation: :hasMother
    target: Chantal_de_Chevron-Villette
  AddTriple (e47bbbe0-4006-47a7-b313-4a9a0d814848)
 Call ID: e47bbbe0-4006-47a7-b313-4a9a0d814848
  Args:
    source: Charles_Napoléon_Bonaparte
    relation: :hasFather
    target: Louis_Prince_Napoléon
  AddTriple (c5cc0128-ebe3-4cbe-b060-0523480e51b4)
 Call ID: c5cc0128-ebe3-4cbe-b060-0523480e51b4
  Args:
    relation: :hasMother
    target: Alix_de_Foresta
    source: Charles_Napoléon_Bonaparte
  AddLiteral (902b4384-97b6-4b3f-9768-19c6bdfd43dd)
 Call ID: 902b4384-97b6-4b3f-9768-19c6bdfd43dd
  Args:
    literal_type: xsd:integer
    source: Princess_Béatrice_of_Bourbon-Two_Sicilies
    relation: :hasMarriageYear
    literal_value: 1978
  AddTriple (d8dc86c0-3342-435b-8c9a-bf9b1db05a2d)
 Call ID: d8dc86c0-3342-435b-8c9a-bf9b1db05a2d
  Args:
    source: Princess_Béatrice_of_Bourbon-Two_Sicilies
    relation: :hasRelation
    target: Charles_Napoléon_Bonaparte
  Finish (3b0a271d-5008-4d5e-90d3-d22179ef5557)
 Call ID: 3b0a271d-5008-4d5e-90d3-d22179ef5557
  Args: