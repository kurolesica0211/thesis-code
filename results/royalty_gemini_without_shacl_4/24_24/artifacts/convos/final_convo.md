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
Duchess Marie Antoinette of Mecklenburg-Schwerin, also Manette (Marie Antoinette Margarethe Mathilde; 28 May 1884 – 26 October 1944) was the Duchess of Mecklenburg-Schwerin by birth and potential bride for King Alfonso XIII of Spain.
Early life

Marie Antoinette was born in Venice, into the House of Mecklenburg, as the third child and the second daughter of Duke Paul Frederick of Mecklenburg and Princess Marie of Windisch-Graetz.
Her brothers and sisters were Duke Paul Friedrich of Mecklenburg, Duchess Maria Luise of Mecklenburg-Schwerin (1883–1883), Duke Heinrich Borwin of Mecklenburg-Schwerin (1885–1942), and Duke Joseph of Mecklenburg-Schwerin (1889–1889).
She had a difficult relationship with her cousin Frederick Francis IV, Grand Duke of Mecklenburg-Schwerin, who regularly had to amortize her debts.
So, Marie Antoinette regularly had to sell archaeological artifacts belonging to her mother, excavated in Austria and Carniola, including Hallstatt Archaeological Site in Vače.
Potential bride for the King of Spain

She was German Kaiser Wilhelm II's candidate for a bride for King Alfonso XIII of Spain although he would marry the Kaiser's maternal first cousin, Princess Victoria Eugenie, niece of British King Edward VII.



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
  AssignClass (852d04c3-5cd2-4a9a-aedc-78d8f7867e1f)
 Call ID: 852d04c3-5cd2-4a9a-aedc-78d8f7867e1f
  Args:
    type: :Woman
    source: Marie_Antoinette_of_Mecklenburg-Schwerin
  AssignClass (40ca8505-b546-4d47-abce-0d756a4f4d91)
 Call ID: 40ca8505-b546-4d47-abce-0d756a4f4d91
  Args:
    source: Marie_Antoinette_of_Mecklenburg-Schwerin
    type: :Person
  AddLiteral (7e84fde9-f75b-45c0-9304-be149dd6e2b2)
 Call ID: 7e84fde9-f75b-45c0-9304-be149dd6e2b2
  Args:
    literal_value: Manette
    source: Marie_Antoinette_of_Mecklenburg-Schwerin
    relation: :alsoKnownAs
    literal_type: xsd:string
  AddLiteral (0d1d2d4b-0f5d-4eaa-9080-7a52dc094050)
 Call ID: 0d1d2d4b-0f5d-4eaa-9080-7a52dc094050
  Args:
    literal_value: 1884
    source: Marie_Antoinette_of_Mecklenburg-Schwerin
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (04ee74d9-5ff6-45b0-9d0a-31bb377526b7)
 Call ID: 04ee74d9-5ff6-45b0-9d0a-31bb377526b7
  Args:
    literal_value: 1944
    source: Marie_Antoinette_of_Mecklenburg-Schwerin
    relation: :hasDeathYear
    literal_type: xsd:integer
  AssignClass (7de10348-cddf-464c-959c-a4706972f469)
 Call ID: 7de10348-cddf-464c-959c-a4706972f469
  Args:
    source: Duke_Paul_Frederick_of_Mecklenburg
    type: :Man
  AssignClass (cfe6d99f-dbc6-4e1f-8a6f-125aa54a4cd3)
 Call ID: cfe6d99f-dbc6-4e1f-8a6f-125aa54a4cd3
  Args:
    source: Duke_Paul_Frederick_of_Mecklenburg
    type: :Person
  AssignClass (08fc55bd-dfb3-4b07-82d8-c28b103c8e85)
 Call ID: 08fc55bd-dfb3-4b07-82d8-c28b103c8e85
  Args:
    source: Princess_Marie_of_Windisch-Graetz
    type: :Woman
  AssignClass (86c27574-7244-4635-ab79-9ad5320992ab)
 Call ID: 86c27574-7244-4635-ab79-9ad5320992ab
  Args:
    type: :Person
    source: Princess_Marie_of_Windisch-Graetz
  AddTriple (be1d4c4a-b139-4b97-8329-374408efa108)
 Call ID: be1d4c4a-b139-4b97-8329-374408efa108
  Args:
    target: Duke_Paul_Frederick_of_Mecklenburg
    source: Marie_Antoinette_of_Mecklenburg-Schwerin
    relation: :hasFather
  AddTriple (e0975d88-2833-4b90-9164-8cb0190c2d7d)
 Call ID: e0975d88-2833-4b90-9164-8cb0190c2d7d
  Args:
    relation: :hasMother
    source: Marie_Antoinette_of_Mecklenburg-Schwerin
    target: Princess_Marie_of_Windisch-Graetz
  AssignClass (52e0048d-4c59-414b-9ce8-a3f067e436de)
 Call ID: 52e0048d-4c59-414b-9ce8-a3f067e436de
  Args:
    source: Duke_Paul_Friedrich_of_Mecklenburg
    type: :Man
  AssignClass (3e0eddbd-800c-4523-86a7-392be161d097)
 Call ID: 3e0eddbd-800c-4523-86a7-392be161d097
  Args:
    source: Duke_Paul_Friedrich_of_Mecklenburg
    type: :Person
  AddTriple (0fcb8f55-9c82-415a-bd40-559333e2f2df)
 Call ID: 0fcb8f55-9c82-415a-bd40-559333e2f2df
  Args:
    relation: :isSiblingOf
    source: Marie_Antoinette_of_Mecklenburg-Schwerin
    target: Duke_Paul_Friedrich_of_Mecklenburg
  AssignClass (925cffa7-42ad-40e3-815d-007f174aceae)
 Call ID: 925cffa7-42ad-40e3-815d-007f174aceae
  Args:
    source: Duchess_Maria_Luise_of_Mecklenburg-Schwerin
    type: :Woman
  AssignClass (ef111460-dea4-4fdb-99e7-33bb628b0235)
 Call ID: ef111460-dea4-4fdb-99e7-33bb628b0235
  Args:
    type: :Person
    source: Duchess_Maria_Luise_of_Mecklenburg-Schwerin
  AddLiteral (3f7be44b-a769-48d1-bd40-41d776ac5938)
 Call ID: 3f7be44b-a769-48d1-bd40-41d776ac5938
  Args:
    source: Duchess_Maria_Luise_of_Mecklenburg-Schwerin
    literal_value: 1883
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (4e4b04ef-2c79-4260-bd6b-45276a1f2fb2)
 Call ID: 4e4b04ef-2c79-4260-bd6b-45276a1f2fb2
  Args:
    source: Duchess_Maria_Luise_of_Mecklenburg-Schwerin
    literal_value: 1883
    relation: :hasDeathYear
    literal_type: xsd:integer
  AddTriple (9efb8a70-82cf-4128-9f37-74030daaaed4)
 Call ID: 9efb8a70-82cf-4128-9f37-74030daaaed4
  Args:
    target: Duchess_Maria_Luise_of_Mecklenburg-Schwerin
    source: Marie_Antoinette_of_Mecklenburg-Schwerin
    relation: :isSiblingOf
  AssignClass (51ea4a9a-1eb2-483e-83a4-29af19e30143)
 Call ID: 51ea4a9a-1eb2-483e-83a4-29af19e30143
  Args:
    source: Duke_Heinrich_Borwin_of_Mecklenburg-Schwerin
    type: :Man
  AssignClass (44628fc3-2aef-4f2f-ad61-8be235454c6f)
 Call ID: 44628fc3-2aef-4f2f-ad61-8be235454c6f
  Args:
    source: Duke_Heinrich_Borwin_of_Mecklenburg-Schwerin
    type: :Person
  AddLiteral (82693fd4-9100-4781-a716-3d8e387dc12c)
 Call ID: 82693fd4-9100-4781-a716-3d8e387dc12c
  Args:
    literal_value: 1885
    source: Duke_Heinrich_Borwin_of_Mecklenburg-Schwerin
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (2a4028eb-0b4a-42e9-9e5b-006fdc6b28c9)
 Call ID: 2a4028eb-0b4a-42e9-9e5b-006fdc6b28c9
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1942
    source: Duke_Heinrich_Borwin_of_Mecklenburg-Schwerin
  AddTriple (32e7457c-2719-4b73-894a-8401d8dbe44c)
 Call ID: 32e7457c-2719-4b73-894a-8401d8dbe44c
  Args:
    relation: :isSiblingOf
    target: Duke_Heinrich_Borwin_of_Mecklenburg-Schwerin
    source: Marie_Antoinette_of_Mecklenburg-Schwerin
  AssignClass (1bf1db8c-4ab9-46e8-a6cf-bc365ddded44)
 Call ID: 1bf1db8c-4ab9-46e8-a6cf-bc365ddded44
  Args:
    source: Duke_Joseph_of_Mecklenburg-Schwerin
    type: :Man
  AssignClass (aa25a097-5f26-4f59-9c71-6aa0d9aaf9f4)
 Call ID: aa25a097-5f26-4f59-9c71-6aa0d9aaf9f4
  Args:
    source: Duke_Joseph_of_Mecklenburg-Schwerin
    type: :Person
  AddLiteral (f85efc16-1e0c-4053-af89-5f869c86dd48)
 Call ID: f85efc16-1e0c-4053-af89-5f869c86dd48
  Args:
    literal_value: 1889
    source: Duke_Joseph_of_Mecklenburg-Schwerin
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (058aae70-24e4-422d-a70c-2e3db221a233)
 Call ID: 058aae70-24e4-422d-a70c-2e3db221a233
  Args:
    literal_value: 1889
    source: Duke_Joseph_of_Mecklenburg-Schwerin
    literal_type: xsd:integer
    relation: :hasDeathYear
  AddTriple (c22a377e-d5f9-4783-9b6a-6e5b69795964)
 Call ID: c22a377e-d5f9-4783-9b6a-6e5b69795964
  Args:
    source: Marie_Antoinette_of_Mecklenburg-Schwerin
    target: Duke_Joseph_of_Mecklenburg-Schwerin
    relation: :isSiblingOf
  AssignClass (39c9f9e5-4d29-48ac-abc3-aa6fc5c96caa)
 Call ID: 39c9f9e5-4d29-48ac-abc3-aa6fc5c96caa
  Args:
    source: Frederick_Francis_IV_Grand_Duke_of_Mecklenburg-Schwerin
    type: :Man
  AssignClass (fd354099-47bb-484c-9aa6-8879ef249233)
 Call ID: fd354099-47bb-484c-9aa6-8879ef249233
  Args:
    type: :Person
    source: Frederick_Francis_IV_Grand_Duke_of_Mecklenburg-Schwerin
  AddTriple (b67b090f-fabe-4693-8b7a-76d5a900e590)
 Call ID: b67b090f-fabe-4693-8b7a-76d5a900e590
  Args:
    target: Frederick_Francis_IV_Grand_Duke_of_Mecklenburg-Schwerin
    source: Marie_Antoinette_of_Mecklenburg-Schwerin
    relation: :isBloodrelationOf
  Finish (bae7329a-19d9-41d9-8ef9-c6f1dc9a0f1d)
 Call ID: bae7329a-19d9-41d9-8ef9-c6f1dc9a0f1d
  Args: