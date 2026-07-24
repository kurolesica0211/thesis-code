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
  AssignClass (64e698f6-2c36-402f-b379-0a3bfc6d4c72)
 Call ID: 64e698f6-2c36-402f-b379-0a3bfc6d4c72
  Args:
    type: :Man
    source: :Friedrich_Franz_of_Mecklenburg-Schwerin
  AssignClass (62cb2bde-c075-4a42-8cc5-ce6f22b9e425)
 Call ID: 62cb2bde-c075-4a42-8cc5-ce6f22b9e425
  Args:
    type: :Person
    source: :Friedrich_Franz_of_Mecklenburg-Schwerin
  AddLiteral (5e64890c-2ce9-4a54-9424-373ad4ebf9be)
 Call ID: 5e64890c-2ce9-4a54-9424-373ad4ebf9be
  Args:
    source: :Friedrich_Franz_of_Mecklenburg-Schwerin
    literal_type: xsd:string
    relation: :hasBirthYear
    literal_value: 1910
  AddLiteral (1982edbe-e16e-4467-a00b-7c4e341d1c3d)
 Call ID: 1982edbe-e16e-4467-a00b-7c4e341d1c3d
  Args:
    source: :Friedrich_Franz_of_Mecklenburg-Schwerin
    literal_value: 2001
    literal_type: xsd:string
    relation: :hasDeathYear
  AssignClass (5841fbda-efae-4842-93fa-4537dbd94b9d)
 Call ID: 5841fbda-efae-4842-93fa-4537dbd94b9d
  Args:
    type: :Man
    source: :Frederick_Francis_IV_of_Mecklenburg-Schwerin
  AssignClass (c18a9396-506f-41e7-943c-35f03aa27c45)
 Call ID: c18a9396-506f-41e7-943c-35f03aa27c45
  Args:
    type: :Person
    source: :Frederick_Francis_IV_of_Mecklenburg-Schwerin
  AddTriple (edb0945c-b78a-4cca-bbd8-96995699b50f)
 Call ID: edb0945c-b78a-4cca-bbd8-96995699b50f
  Args:
    relation: :hasFather
    source: :Friedrich_Franz_of_Mecklenburg-Schwerin
    target: :Frederick_Francis_IV_of_Mecklenburg-Schwerin
  AssignClass (48def94b-9c4c-4741-a31b-bcbee4ec00ca)
 Call ID: 48def94b-9c4c-4741-a31b-bcbee4ec00ca
  Args:
    type: :Woman
    source: :Alexandra_of_Hanover
  AssignClass (c7e6f6de-1333-49dc-8849-1525a83b867a)
 Call ID: c7e6f6de-1333-49dc-8849-1525a83b867a
  Args:
    type: :Person
    source: :Alexandra_of_Hanover
  AddTriple (5f5ab361-1c66-4d4f-ae45-7aa128cc5af8)
 Call ID: 5f5ab361-1c66-4d4f-ae45-7aa128cc5af8
  Args:
    relation: :hasMother
    source: :Friedrich_Franz_of_Mecklenburg-Schwerin
    target: :Alexandra_of_Hanover
  AssignClass (2c656882-3fa1-49f0-b0b2-59a329ed36e4)
 Call ID: 2c656882-3fa1-49f0-b0b2-59a329ed36e4
  Args:
    type: :Man
    source: :Ernest_Augustus_of_Hanover
  AssignClass (a08e2a3a-9923-416b-bb1a-cae3cfcdf6f2)
 Call ID: a08e2a3a-9923-416b-bb1a-cae3cfcdf6f2
  Args:
    type: :Person
    source: :Ernest_Augustus_of_Hanover
  AddTriple (df0f6e1a-dd87-4a99-a070-36a6c418b688)
 Call ID: df0f6e1a-dd87-4a99-a070-36a6c418b688
  Args:
    relation: :hasFather
    source: :Alexandra_of_Hanover
    target: :Ernest_Augustus_of_Hanover
  AssignClass (e9321e59-89dd-4069-83e9-261fa69e2865)
 Call ID: e9321e59-89dd-4069-83e9-261fa69e2865
  Args:
    type: :Woman
    source: :Thyra_of_Denmark
  AssignClass (97bb1b5d-0e0c-470f-ba5b-943bc107626b)
 Call ID: 97bb1b5d-0e0c-470f-ba5b-943bc107626b
  Args:
    type: :Person
    source: :Thyra_of_Denmark
  AddTriple (ca06adba-3aab-4f90-9052-f2ee16706275)
 Call ID: ca06adba-3aab-4f90-9052-f2ee16706275
  Args:
    target: :Thyra_of_Denmark
    source: :Alexandra_of_Hanover
    relation: :hasMother
  AssignClass (d1eadee2-e213-4edb-8e6c-71c964ccdf75)
 Call ID: d1eadee2-e213-4edb-8e6c-71c964ccdf75
  Args:
    type: :Man
    source: :Christian_IX_of_Denmark
  AssignClass (0d88a980-a8b9-4052-87d4-adfc3a645e5f)
 Call ID: 0d88a980-a8b9-4052-87d4-adfc3a645e5f
  Args:
    type: :Person
    source: :Christian_IX_of_Denmark
  AddTriple (06673b61-afda-4518-8ddc-0265f2bad8a6)
 Call ID: 06673b61-afda-4518-8ddc-0265f2bad8a6
  Args:
    target: :Christian_IX_of_Denmark
    source: :Thyra_of_Denmark
    relation: :hasFather
  AssignClass (1107b03c-d3e3-4abc-8d2a-e068e4a869cd)
 Call ID: 1107b03c-d3e3-4abc-8d2a-e068e4a869cd
  Args:
    type: :Man
    source: :Christian_Louis_of_Mecklenburg-Schwerin
  AssignClass (ffd0192f-9082-4f0c-ac1c-1dea6a1928f1)
 Call ID: ffd0192f-9082-4f0c-ac1c-1dea6a1928f1
  Args:
    type: :Person
    source: :Christian_Louis_of_Mecklenburg-Schwerin
  AddTriple (46373b77-ee7e-4987-8566-121efff3e321)
 Call ID: 46373b77-ee7e-4987-8566-121efff3e321
  Args:
    source: :Christian_Louis_of_Mecklenburg-Schwerin
    target: :Friedrich_Franz_of_Mecklenburg-Schwerin
    relation: :isBrotherOf
  AssignClass (633ec568-9448-464d-a5e1-009db4eb6257)
 Call ID: 633ec568-9448-464d-a5e1-009db4eb6257
  Args:
    type: :Woman
    source: :Karin_Elisabeth_von_Schaper
  AssignClass (ff7cee41-fb29-4263-a3f0-963c8ae885ed)
 Call ID: ff7cee41-fb29-4263-a3f0-963c8ae885ed
  Args:
    type: :Person
    source: :Karin_Elisabeth_von_Schaper
  AddLiteral (c494c489-0c62-4617-b1c2-4ca9eb991742)
 Call ID: c494c489-0c62-4617-b1c2-4ca9eb991742
  Args:
    literal_value: 1941
    literal_type: xsd:string
    relation: :hasMarriageYear
    source: :Friedrich_Franz_of_Mecklenburg-Schwerin
  AddLiteral (998fab5f-c102-4139-b6ef-08b55b28588b)
 Call ID: 998fab5f-c102-4139-b6ef-08b55b28588b
  Args:
    literal_value: 1920
    literal_type: xsd:string
    relation: :hasBirthYear
    source: :Karin_Elisabeth_von_Schaper
  AddLiteral (d5199a50-3c69-47c5-af23-1bf388d67063)
 Call ID: d5199a50-3c69-47c5-af23-1bf388d67063
  Args:
    relation: :hasDeathYear
    literal_type: xsd:string
    literal_value: 2012
    source: :Karin_Elisabeth_von_Schaper
  AssignClass (0c16fe7c-8b11-40e9-8ed3-18a7a53fb45d)
 Call ID: 0c16fe7c-8b11-40e9-8ed3-18a7a53fb45d
  Args:
    type: :Man
    source: :Walter_von_Schaper
  AssignClass (3fa5aa8e-e86a-4203-974d-fe45c0dcdc16)
 Call ID: 3fa5aa8e-e86a-4203-974d-fe45c0dcdc16
  Args:
    type: :Person
    source: :Walter_von_Schaper
  AddTriple (ba700882-b7ef-4b99-bf7a-8153f9eb6b20)
 Call ID: ba700882-b7ef-4b99-bf7a-8153f9eb6b20
  Args:
    source: :Karin_Elisabeth_von_Schaper
    target: :Walter_von_Schaper
    relation: :hasFather
  AssignClass (812deb64-3c2b-4a73-b0b8-d1fa804a15e1)
 Call ID: 812deb64-3c2b-4a73-b0b8-d1fa804a15e1
  Args:
    type: :Woman
    source: :Louise_von_Münchhausen
  AssignClass (5e669d33-78d4-4cfd-8568-54048965a481)
 Call ID: 5e669d33-78d4-4cfd-8568-54048965a481
  Args:
    type: :Person
    source: :Louise_von_Münchhausen
  AddTriple (700f7f26-2529-4d66-8aa7-653808565358)
 Call ID: 700f7f26-2529-4d66-8aa7-653808565358
  Args:
    target: :Louise_von_Münchhausen
    source: :Karin_Elisabeth_von_Schaper
    relation: :hasMother
  Finish (92b7acbf-6da7-40d0-b2ff-b1c1319f6d7a)
 Call ID: 92b7acbf-6da7-40d0-b2ff-b1c1319f6d7a
  Args: