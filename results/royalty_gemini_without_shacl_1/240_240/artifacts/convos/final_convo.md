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
Victoria Federica de Todos los Santos de Marichalar y Borbón, Lady of Tejada GE (born 9 September 2000) is the younger child and only daughter of Infanta Elena, Duchess of Lugo, and Jaime de Marichalar.
She is a granddaughter of King Juan Carlos I and Queen Sofía of Spain and a niece of King Felipe VI.
Victoria is fifth in the line of succession to the Spanish throne after her cousins, King Felipe's daughters Leonor, Princess of Asturias, and Infanta Sofía; her mother; and her brother, Felipe.
Early life and education

Victoria de Marichalar y Borbón was born 9 September 2000 at 13:00 in Ruber International Hospital in Madrid.
She made her first Holy Communion on 27 May 2009 at the Dominicos Church in Alcobendas, Spain.
Then she studied at a British boarding school for 3 years before returning to Spain at St. George's de La Moraleja.
Victoria studied ballet and horse riding.
Career

Marichalar has been reported to be working in the fashion industry and is quoted as saying that fashion is her "true calling".



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
  AssignClass (65fe165a-ee15-4602-aae7-83f30383f78f)
 Call ID: 65fe165a-ee15-4602-aae7-83f30383f78f
  Args:
    source: Victoria_Federica_de_Marichalar_y_Borbon
    type: :Person
  AssignClass (b765e7ef-9896-4da1-b427-f9ba7eeb2004)
 Call ID: b765e7ef-9896-4da1-b427-f9ba7eeb2004
  Args:
    source: Victoria_Federica_de_Marichalar_y_Borbon
    type: :Woman
  AddLiteral (cb3b1aee-fafd-4b9a-923a-ac961f687061)
 Call ID: cb3b1aee-fafd-4b9a-923a-ac961f687061
  Args:
    literal_type: xsd:integer
    source: Victoria_Federica_de_Marichalar_y_Borbon
    literal_value: 2000
    relation: :hasBirthYear
  AssignClass (7ad82855-e4aa-4b70-93bf-e471d73eee65)
 Call ID: 7ad82855-e4aa-4b70-93bf-e471d73eee65
  Args:
    source: Infanta_Elena_Duchess_of_Lugo
    type: :Person
  AssignClass (38c43eb1-c219-4481-9df6-1e4a46fa8ae5)
 Call ID: 38c43eb1-c219-4481-9df6-1e4a46fa8ae5
  Args:
    type: :Woman
    source: Infanta_Elena_Duchess_of_Lugo
  AssignClass (bd8647b4-f0dd-49b4-a784-4e3c9dee85b2)
 Call ID: bd8647b4-f0dd-49b4-a784-4e3c9dee85b2
  Args:
    source: Jaime_de_Marichalar
    type: :Person
  AssignClass (763be9f0-f07f-4e84-afde-6cfd74c17204)
 Call ID: 763be9f0-f07f-4e84-afde-6cfd74c17204
  Args:
    source: Jaime_de_Marichalar
    type: :Man
  AddTriple (b5b72504-0c39-459d-a3fe-474c0001ee21)
 Call ID: b5b72504-0c39-459d-a3fe-474c0001ee21
  Args:
    source: Victoria_Federica_de_Marichalar_y_Borbon
    relation: :hasMother
    target: Infanta_Elena_Duchess_of_Lugo
  AddTriple (2d275e34-05cb-4654-b025-361277a26912)
 Call ID: 2d275e34-05cb-4654-b025-361277a26912
  Args:
    source: Victoria_Federica_de_Marichalar_y_Borbon
    relation: :hasFather
    target: Jaime_de_Marichalar
  AssignClass (47fc6a13-a4f0-4d33-99d3-f64250db3995)
 Call ID: 47fc6a13-a4f0-4d33-99d3-f64250db3995
  Args:
    type: :Person
    source: King_Juan_Carlos_I
  AssignClass (0ea283f6-09fb-455c-8960-a1eb03078fa4)
 Call ID: 0ea283f6-09fb-455c-8960-a1eb03078fa4
  Args:
    source: King_Juan_Carlos_I
    type: :Man
  AssignClass (7b173cfc-ba87-4a41-b801-4edd5b911997)
 Call ID: 7b173cfc-ba87-4a41-b801-4edd5b911997
  Args:
    type: :Person
    source: Queen_Sofia_of_Spain
  AssignClass (159c94a7-f5ed-4235-b07f-4fd4c0fe229d)
 Call ID: 159c94a7-f5ed-4235-b07f-4fd4c0fe229d
  Args:
    source: Queen_Sofia_of_Spain
    type: :Woman
  AddTriple (f9bf46a7-706b-411a-a3c6-a3b68951299e)
 Call ID: f9bf46a7-706b-411a-a3c6-a3b68951299e
  Args:
    target: King_Juan_Carlos_I
    relation: :hasParent
    source: Infanta_Elena_Duchess_of_Lugo
  AddTriple (ce1d303b-b5a4-4f43-8118-fda586f5ad5f)
 Call ID: ce1d303b-b5a4-4f43-8118-fda586f5ad5f
  Args:
    relation: :hasParent
    source: Infanta_Elena_Duchess_of_Lugo
    target: Queen_Sofia_of_Spain
  AssignClass (c41216ed-6491-489e-be9c-3c442dd201c3)
 Call ID: c41216ed-6491-489e-be9c-3c442dd201c3
  Args:
    type: :Person
    source: King_Felipe_VI
  AssignClass (e6ed2f99-10ba-40ba-920b-22834ac80734)
 Call ID: e6ed2f99-10ba-40ba-920b-22834ac80734
  Args:
    type: :Man
    source: King_Felipe_VI
  AssignClass (db9e3fdf-6efd-4160-9740-e9bedcec098f)
 Call ID: db9e3fdf-6efd-4160-9740-e9bedcec098f
  Args:
    source: Felipe_de_Marichalar
    type: :Person
  AssignClass (a30160c3-bd66-43e1-a478-20f99078c520)
 Call ID: a30160c3-bd66-43e1-a478-20f99078c520
  Args:
    source: Felipe_de_Marichalar
    type: :Man
  AddTriple (5e6e4eb2-0f85-46bc-a5a9-0b01bf6cd8ee)
 Call ID: 5e6e4eb2-0f85-46bc-a5a9-0b01bf6cd8ee
  Args:
    target: Infanta_Elena_Duchess_of_Lugo
    relation: :hasMother
    source: Felipe_de_Marichalar
  AddTriple (154f8ce4-a2e1-4beb-b439-1481fb357ec0)
 Call ID: 154f8ce4-a2e1-4beb-b439-1481fb357ec0
  Args:
    source: Felipe_de_Marichalar
    relation: :hasFather
    target: Jaime_de_Marichalar
  AssignClass (5cadff3e-b280-4b6e-8565-6e929c7200a9)
 Call ID: 5cadff3e-b280-4b6e-8565-6e929c7200a9
  Args:
    source: Leonor_Princess_of_Asturias
    type: :Person
  AssignClass (d7e7f8a7-09d5-48bc-82cd-929fce60f77b)
 Call ID: d7e7f8a7-09d5-48bc-82cd-929fce60f77b
  Args:
    source: Leonor_Princess_of_Asturias
    type: :Woman
  AssignClass (06b088c1-c473-448e-992e-335cbf094aba)
 Call ID: 06b088c1-c473-448e-992e-335cbf094aba
  Args:
    source: Infanta_Sofia
    type: :Person
  AssignClass (dbb62489-a910-46f0-951f-01db5ad37542)
 Call ID: dbb62489-a910-46f0-951f-01db5ad37542
  Args:
    source: Infanta_Sofia
    type: :Woman
  AddTriple (27935452-bed4-4791-8ca9-d05e4523d695)
 Call ID: 27935452-bed4-4791-8ca9-d05e4523d695
  Args:
    target: King_Felipe_VI
    relation: :hasFather
    source: Leonor_Princess_of_Asturias
  AddTriple (1e375402-8c2b-497d-be89-e94c15ac79d3)
 Call ID: 1e375402-8c2b-497d-be89-e94c15ac79d3
  Args:
    source: Infanta_Sofia
    relation: :hasFather
    target: King_Felipe_VI
  Finish (d6992593-ad49-4dd3-9e11-2b2afc3459ad)
 Call ID: d6992593-ad49-4dd3-9e11-2b2afc3459ad
  Args: