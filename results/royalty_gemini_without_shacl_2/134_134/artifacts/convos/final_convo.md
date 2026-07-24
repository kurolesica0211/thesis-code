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
Friedrich Franz, Hereditary Grand Duke of Mecklenburg-Schwerin (German: Friedrich Franz Erbgroßherzog von Mecklenburg-Schwerin; 22 April 1910 – 31 July 2001) was the heir apparent to the throne of Mecklenburg-Schwerin and a member of the Waffen-SS.
Early life

He was born in Schwerin, the eldest child of the reigning Grand Duke of Mecklenburg-Schwerin, Frederick Francis IV, and his wife Princess Alexandra of Hanover, a daughter of Crown Prince Ernest Augustus of Hanover (a first-cousin once removed of Queen Victoria) and Princess Thyra of Denmark, the youngest daughter of King Christian IX of Denmark.
He did not succeed to the throne, as the Grand Duchy was replaced with the Free State of Mecklenburg-Schwerin.
Upon the promulgation of the Weimar Constitution on 11 August 1919, titles of sovereigns such as emperor/empress, king/queen, grand duke/grand duchess, etc. were abolished.
He therefore became known as Friedrich Franz Herzog von Mecklenburg-Schwerin (or Friedrich Franz, Duke of Mecklenburg-Schwerin) de facto since the establishment of the Free State of Mecklenburg-Schwerin.
Post monarchy

In May 1931 against the will of his father, Friedrich Franz joined the SS and by 1936 he had been promoted to the rank of Hauptsturmführer (Captain).
In May 1943, a family council was called by the Grand Ducal family and Friedrich Franz was passed over as heir (of the family estates) in favour of his younger brother Duke Christian Louis, who would instead inherit the family property.
Friedrich Franz married Karin Elisabeth von Schaper (1920–2012), the daughter of Walter von Schaper and his wife Baroness Louise von Münchhausen, on 11 June 1941 at Schloß Wiligrad, near the Lake Schwerin.



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
  AssignClass (f33d3e1f-5187-49ec-b2cd-52a833b69ff8)
 Call ID: f33d3e1f-5187-49ec-b2cd-52a833b69ff8
  Args:
    type: :Man
    source: Friedrich_Franz_Mecklenburg_Schwerin
  AssignClass (5df74693-b08f-4ee7-9b54-de88e199bfac)
 Call ID: 5df74693-b08f-4ee7-9b54-de88e199bfac
  Args:
    type: :Person
    source: Friedrich_Franz_Mecklenburg_Schwerin
  AddLiteral (ebd11763-e3a4-4480-8de2-2927fbb3f179)
 Call ID: ebd11763-e3a4-4480-8de2-2927fbb3f179
  Args:
    literal_value: 1910
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Friedrich_Franz_Mecklenburg_Schwerin
  AddLiteral (bae2b849-81d0-45da-bb2d-52b720a1fd7d)
 Call ID: bae2b849-81d0-45da-bb2d-52b720a1fd7d
  Args:
    source: Friedrich_Franz_Mecklenburg_Schwerin
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 2001
  AssignClass (ecc43b0c-ec7d-4d08-a40d-a87be3c4a478)
 Call ID: ecc43b0c-ec7d-4d08-a40d-a87be3c4a478
  Args:
    type: :Man
    source: Frederick_Francis_IV
  AssignClass (7b00606e-21fd-4ce8-b33e-3a1e28f6951f)
 Call ID: 7b00606e-21fd-4ce8-b33e-3a1e28f6951f
  Args:
    type: :Person
    source: Frederick_Francis_IV
  AssignClass (674e9b21-055d-4f7b-a39c-7de2f6fcbaf5)
 Call ID: 674e9b21-055d-4f7b-a39c-7de2f6fcbaf5
  Args:
    type: :Woman
    source: Alexandra_Hanover
  AssignClass (31ebcc19-3a89-4101-b48f-cda8f5b34fbd)
 Call ID: 31ebcc19-3a89-4101-b48f-cda8f5b34fbd
  Args:
    type: :Person
    source: Alexandra_Hanover
  AddTriple (f4200928-5ffb-4f48-961e-d1db1fba618f)
 Call ID: f4200928-5ffb-4f48-961e-d1db1fba618f
  Args:
    relation: :hasFather
    target: Frederick_Francis_IV
    source: Friedrich_Franz_Mecklenburg_Schwerin
  AddTriple (17035420-33dc-4aca-8e48-edff12fff97a)
 Call ID: 17035420-33dc-4aca-8e48-edff12fff97a
  Args:
    target: Alexandra_Hanover
    relation: :hasMother
    source: Friedrich_Franz_Mecklenburg_Schwerin
  AssignClass (633608ef-34e4-45ca-bc41-3e10938e0658)
 Call ID: 633608ef-34e4-45ca-bc41-3e10938e0658
  Args:
    type: :Man
    source: Ernest_Augustus_Hanover
  AssignClass (e24527fe-7916-49be-84b0-b958cdd2a361)
 Call ID: e24527fe-7916-49be-84b0-b958cdd2a361
  Args:
    type: :Person
    source: Ernest_Augustus_Hanover
  AssignClass (c2dbb706-dc32-481d-9118-d3d3cf570f62)
 Call ID: c2dbb706-dc32-481d-9118-d3d3cf570f62
  Args:
    type: :Woman
    source: Thyra_Denmark
  AssignClass (c4df7dbd-c7ff-4b5b-9bdd-d9b814b2c2f5)
 Call ID: c4df7dbd-c7ff-4b5b-9bdd-d9b814b2c2f5
  Args:
    type: :Person
    source: Thyra_Denmark
  AddTriple (0fabbd1d-6d71-40e4-980e-e91b8f2565c9)
 Call ID: 0fabbd1d-6d71-40e4-980e-e91b8f2565c9
  Args:
    relation: :hasFather
    target: Ernest_Augustus_Hanover
    source: Alexandra_Hanover
  AddTriple (2a8993ce-bf17-4268-9f92-dd4ea5fe2524)
 Call ID: 2a8993ce-bf17-4268-9f92-dd4ea5fe2524
  Args:
    source: Alexandra_Hanover
    target: Thyra_Denmark
    relation: :hasMother
  AssignClass (16fa4ecf-a18e-4c5a-b110-603431eeb2ea)
 Call ID: 16fa4ecf-a18e-4c5a-b110-603431eeb2ea
  Args:
    type: :Man
    source: Christian_IX_Denmark
  AssignClass (e15b7857-1e05-451b-b663-260df1fc3395)
 Call ID: e15b7857-1e05-451b-b663-260df1fc3395
  Args:
    type: :Person
    source: Christian_IX_Denmark
  AddTriple (2683be92-7429-4bae-abda-a0725de77c0e)
 Call ID: 2683be92-7429-4bae-abda-a0725de77c0e
  Args:
    source: Thyra_Denmark
    relation: :hasFather
    target: Christian_IX_Denmark
  AssignClass (f835daa4-1cae-4233-81ff-41409eac7292)
 Call ID: f835daa4-1cae-4233-81ff-41409eac7292
  Args:
    type: :Man
    source: Christian_Louis
  AssignClass (4dbf5fa3-2e4e-4d75-9d3b-b41a398a2416)
 Call ID: 4dbf5fa3-2e4e-4d75-9d3b-b41a398a2416
  Args:
    type: :Person
    source: Christian_Louis
  AddTriple (2b409dd2-feb2-4ceb-8da6-0857f9af24ee)
 Call ID: 2b409dd2-feb2-4ceb-8da6-0857f9af24ee
  Args:
    relation: :isBrotherOf
    target: Friedrich_Franz_Mecklenburg_Schwerin
    source: Christian_Louis
  AssignClass (ad1f6c43-9f76-4607-8b8c-ed07cc39f88d)
 Call ID: ad1f6c43-9f76-4607-8b8c-ed07cc39f88d
  Args:
    type: :Woman
    source: Karin_Elisabeth_von_Schaper
  AssignClass (33fe5cd7-bf4e-4dcd-b32c-83f50ff3819c)
 Call ID: 33fe5cd7-bf4e-4dcd-b32c-83f50ff3819c
  Args:
    type: :Person
    source: Karin_Elisabeth_von_Schaper
  AddLiteral (5d02a339-7cc9-4837-80da-562c28ccaea5)
 Call ID: 5d02a339-7cc9-4837-80da-562c28ccaea5
  Args:
    literal_value: 1920
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Karin_Elisabeth_von_Schaper
  AddLiteral (60254e1b-aa0c-46d2-bbde-2b86854ac282)
 Call ID: 60254e1b-aa0c-46d2-bbde-2b86854ac282
  Args:
    relation: :hasDeathYear
    source: Karin_Elisabeth_von_Schaper
    literal_value: 2012
    literal_type: xsd:integer
  AddLiteral (e4af1a39-6c41-452e-b874-83f39dabb1e1)
 Call ID: e4af1a39-6c41-452e-b874-83f39dabb1e1
  Args:
    literal_value: 1941
    literal_type: xsd:integer
    source: Friedrich_Franz_Mecklenburg_Schwerin
    relation: :hasMarriageYear
  AssignClass (44e9d476-24d2-49dc-93d8-c42bb49bf2fd)
 Call ID: 44e9d476-24d2-49dc-93d8-c42bb49bf2fd
  Args:
    type: :Man
    source: Walter_von_Schaper
  AssignClass (bbffcbfb-1f06-4c5b-aa3f-8bc844bff036)
 Call ID: bbffcbfb-1f06-4c5b-aa3f-8bc844bff036
  Args:
    type: :Person
    source: Walter_von_Schaper
  AssignClass (8fdb2eeb-0c92-4cc5-8031-db3f9a2b08cf)
 Call ID: 8fdb2eeb-0c92-4cc5-8031-db3f9a2b08cf
  Args:
    type: :Woman
    source: Louise_von_Münchhausen
  AssignClass (34173d96-3a91-468c-a1e2-02d5db026899)
 Call ID: 34173d96-3a91-468c-a1e2-02d5db026899
  Args:
    type: :Person
    source: Louise_von_Münchhausen
  AddTriple (92dfbb99-53aa-41b2-8687-c497cfd9923c)
 Call ID: 92dfbb99-53aa-41b2-8687-c497cfd9923c
  Args:
    relation: :hasFather
    target: Walter_von_Schaper
    source: Karin_Elisabeth_von_Schaper
  AddTriple (2ca0b0b7-4845-4886-95e8-6aaaacfc85ce)
 Call ID: 2ca0b0b7-4845-4886-95e8-6aaaacfc85ce
  Args:
    source: Karin_Elisabeth_von_Schaper
    target: Louise_von_Münchhausen
    relation: :hasMother
  Finish (79669bb5-c496-439c-b292-6c568b9717e6)
 Call ID: 79669bb5-c496-439c-b292-6c568b9717e6
  Args: