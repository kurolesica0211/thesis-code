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
  AssignClass (e1774568-2436-4622-a53c-0d278c16956e)
 Call ID: e1774568-2436-4622-a53c-0d278c16956e
  Args:
    source: Friedrich_Franz
    type: :Man
  AssignClass (b66d4964-11e7-45ec-8646-dc6eca8a784a)
 Call ID: b66d4964-11e7-45ec-8646-dc6eca8a784a
  Args:
    source: Friedrich_Franz
    type: :Person
  AddLiteral (dfe19095-4405-4c7b-9aa8-2cdd955d99f7)
 Call ID: dfe19095-4405-4c7b-9aa8-2cdd955d99f7
  Args:
    literal_type: xsd:integer
    source: Friedrich_Franz
    relation: :hasBirthYear
    literal_value: 1910
  AddLiteral (8e411626-7618-4737-8d19-a14f9b1a06a1)
 Call ID: 8e411626-7618-4737-8d19-a14f9b1a06a1
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: Friedrich_Franz
    literal_value: 2001
  AssignClass (c4d9b200-4041-4fb7-b532-53528e5181db)
 Call ID: c4d9b200-4041-4fb7-b532-53528e5181db
  Args:
    source: Frederick_Francis_IV
    type: :Man
  AssignClass (494a7f7f-c74e-4609-b1c4-d5fb7e4b94fb)
 Call ID: 494a7f7f-c74e-4609-b1c4-d5fb7e4b94fb
  Args:
    source: Frederick_Francis_IV
    type: :Person
  AssignClass (c3664f58-b18a-4172-9c47-2236003ce895)
 Call ID: c3664f58-b18a-4172-9c47-2236003ce895
  Args:
    source: Alexandra_of_Hanover
    type: :Woman
  AssignClass (f2e9c2c4-09d3-4884-ad1a-f44a56302275)
 Call ID: f2e9c2c4-09d3-4884-ad1a-f44a56302275
  Args:
    source: Alexandra_of_Hanover
    type: :Person
  AddTriple (2b298855-f464-49a4-8a90-b81cec2ff34e)
 Call ID: 2b298855-f464-49a4-8a90-b81cec2ff34e
  Args:
    target: Frederick_Francis_IV
    relation: :hasFather
    source: Friedrich_Franz
  AddTriple (62574699-a4ec-437a-8fbf-70467cd4f00d)
 Call ID: 62574699-a4ec-437a-8fbf-70467cd4f00d
  Args:
    source: Friedrich_Franz
    relation: :hasMother
    target: Alexandra_of_Hanover
  AssignClass (47f20c8e-b00b-4d56-bee2-e2415a3e23c9)
 Call ID: 47f20c8e-b00b-4d56-bee2-e2415a3e23c9
  Args:
    source: Ernest_Augustus_of_Hanover
    type: :Man
  AssignClass (96c520ec-f41c-41ab-b586-84d01af413e6)
 Call ID: 96c520ec-f41c-41ab-b586-84d01af413e6
  Args:
    source: Ernest_Augustus_of_Hanover
    type: :Person
  AssignClass (36158880-082d-41d3-9bfd-b5f1953a12f3)
 Call ID: 36158880-082d-41d3-9bfd-b5f1953a12f3
  Args:
    source: Thyra_of_Denmark
    type: :Woman
  AssignClass (0078f428-97bb-4fb4-8293-9bd4c917f01f)
 Call ID: 0078f428-97bb-4fb4-8293-9bd4c917f01f
  Args:
    source: Thyra_of_Denmark
    type: :Person
  AddTriple (f3255a36-9e67-4f3d-a214-32f77eee7d9b)
 Call ID: f3255a36-9e67-4f3d-a214-32f77eee7d9b
  Args:
    source: Alexandra_of_Hanover
    relation: :hasFather
    target: Ernest_Augustus_of_Hanover
  AddTriple (4335c36d-dbb5-422c-a3d0-8901693bb3e2)
 Call ID: 4335c36d-dbb5-422c-a3d0-8901693bb3e2
  Args:
    target: Thyra_of_Denmark
    source: Alexandra_of_Hanover
    relation: :hasMother
  AssignClass (fca05703-24c9-478f-9239-830124c14304)
 Call ID: fca05703-24c9-478f-9239-830124c14304
  Args:
    source: Christian_IX_of_Denmark
    type: :Man
  AssignClass (d9192ace-63c4-4b04-a494-14095b507fa2)
 Call ID: d9192ace-63c4-4b04-a494-14095b507fa2
  Args:
    source: Christian_IX_of_Denmark
    type: :Person
  AddTriple (9495a3e1-a04c-408a-8614-37a51d8bf163)
 Call ID: 9495a3e1-a04c-408a-8614-37a51d8bf163
  Args:
    source: Thyra_of_Denmark
    relation: :hasFather
    target: Christian_IX_of_Denmark
  AssignClass (2d338cfd-3ed0-44cf-b94e-0a0df6a4f6e6)
 Call ID: 2d338cfd-3ed0-44cf-b94e-0a0df6a4f6e6
  Args:
    source: Christian_Louis
    type: :Man
  AssignClass (34f12f92-dd73-4899-9eb9-75dc88db2799)
 Call ID: 34f12f92-dd73-4899-9eb9-75dc88db2799
  Args:
    source: Christian_Louis
    type: :Person
  AddTriple (dfd2c938-c94f-45be-b920-cb49d9eebb58)
 Call ID: dfd2c938-c94f-45be-b920-cb49d9eebb58
  Args:
    target: Friedrich_Franz
    source: Christian_Louis
    relation: :isBrotherOf
  AssignClass (7cc27962-232b-498b-b1c8-d392a377a5d9)
 Call ID: 7cc27962-232b-498b-b1c8-d392a377a5d9
  Args:
    source: Karin_Elisabeth_von_Schaper
    type: :Woman
  AssignClass (d8ef0cee-612d-43cf-b792-58fd195014a1)
 Call ID: d8ef0cee-612d-43cf-b792-58fd195014a1
  Args:
    source: Karin_Elisabeth_von_Schaper
    type: :Person
  AddLiteral (56bdf104-f5b7-419b-bbd2-bd1b74f122f0)
 Call ID: 56bdf104-f5b7-419b-bbd2-bd1b74f122f0
  Args:
    relation: :hasBirthYear
    source: Karin_Elisabeth_von_Schaper
    literal_type: xsd:integer
    literal_value: 1920
  AddLiteral (19a70124-d3a4-4e13-a817-413e8016a28c)
 Call ID: 19a70124-d3a4-4e13-a817-413e8016a28c
  Args:
    literal_type: xsd:integer
    source: Karin_Elisabeth_von_Schaper
    relation: :hasDeathYear
    literal_value: 2012
  AddLiteral (00e7f32a-2852-46e2-a5b2-2d8d93850128)
 Call ID: 00e7f32a-2852-46e2-a5b2-2d8d93850128
  Args:
    literal_type: xsd:integer
    source: Friedrich_Franz
    relation: :hasMarriageYear
    literal_value: 1941
  AddTriple (a5934882-9f64-477a-9f4a-7988a928b598)
 Call ID: a5934882-9f64-477a-9f4a-7988a928b598
  Args:
    target: Karin_Elisabeth_von_Schaper
    source: Friedrich_Franz
    relation: :hasRelation
  AssignClass (c6d5e4ec-857c-4aeb-b4e7-4c6143e90034)
 Call ID: c6d5e4ec-857c-4aeb-b4e7-4c6143e90034
  Args:
    source: Walter_von_Schaper
    type: :Man
  AssignClass (5ca223bb-d5db-47dc-b66a-2ddeb2574ada)
 Call ID: 5ca223bb-d5db-47dc-b66a-2ddeb2574ada
  Args:
    source: Walter_von_Schaper
    type: :Person
  AssignClass (d1530145-4055-4a1d-8d87-6a4f3c12492d)
 Call ID: d1530145-4055-4a1d-8d87-6a4f3c12492d
  Args:
    source: Louise_von_Münchhausen
    type: :Woman
  AssignClass (631439c5-00fc-454f-a828-cbbfb41f855b)
 Call ID: 631439c5-00fc-454f-a828-cbbfb41f855b
  Args:
    source: Louise_von_Münchhausen
    type: :Person
  AddTriple (92960703-35bd-4c74-b899-ee6a042f7006)
 Call ID: 92960703-35bd-4c74-b899-ee6a042f7006
  Args:
    relation: :hasFather
    source: Karin_Elisabeth_von_Schaper
    target: Walter_von_Schaper
  AddTriple (c5078143-6320-47b7-a6d5-14c6015282e1)
 Call ID: c5078143-6320-47b7-a6d5-14c6015282e1
  Args:
    target: Louise_von_Münchhausen
    source: Karin_Elisabeth_von_Schaper
    relation: :hasMother
  Finish (fc2ed560-7058-4963-b31f-95edc7b2fb45)
 Call ID: fc2ed560-7058-4963-b31f-95edc7b2fb45
  Args: