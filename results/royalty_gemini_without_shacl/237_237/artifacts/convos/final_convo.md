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
Duke Friedrich August of Oldenburg (11 January 1936 – 9 July 2017) was a member of the House of Holstein-Gottorp.
He is a son of Nikolaus, Hereditary Grand Duke of Oldenburg and Princess Helena of Waldeck and Pyrmont.
Family and early life

Frederich August is the sixth child and fourth son of Nikolaus, Hereditary Grand Duke of Oldenburg and his first wife Princess Helena of Waldeck and Pyrmont.
His paternal grandparents are Frederick Augustus II, Grand Duke of Oldenburg and Duchess Elisabeth Alexandrine of Mecklenburg-Schwerin.
His maternal grandparents are Friedrich, Prince of Waldeck and Pyrmont and Princess Bathildis of Schaumburg-Lippe.
His grandfather was overthrown as Grand Duke of Oldenburg in 1918, at the end of World War I.
His father Nikolaus thus never legally succeeded to the title when the deposed Grand Duke died in 1931.
Friedrich is an uncle of Christian, Duke of Oldenburg, the current head of the House of Oldenburg.
Marriage and issue

Friedrich August's first wife was Princess Marie Cécile of Prussia, a daughter of Louis Ferdinand, Prince of Prussia (second son of William, German Crown Prince) and his wife, Grand Duchess Kira Kirillovna of Russia.
Friedrich August and Marie-Cécile have three children: a son, and two daughters.
Marie-Cécile and Friedrich August divorced on 23 November 1989.
On 9 February 1991, Friedrich August was remarried to Donata Countess of Castell-Rüdenhausen in Rüdenhausen, Germany.



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
  AssignClass (85834099-1e2b-4e99-8adf-2d866b4db0fe)
 Call ID: 85834099-1e2b-4e99-8adf-2d866b4db0fe
  Args:
    source: Friedrich_August_of_Oldenburg
    type: :Man
  AssignClass (02259e83-8d87-4130-8fdf-a002411d68dd)
 Call ID: 02259e83-8d87-4130-8fdf-a002411d68dd
  Args:
    source: Friedrich_August_of_Oldenburg
    type: :Person
  AddLiteral (07e6964b-1c92-4f2d-9396-7316819d0f2f)
 Call ID: 07e6964b-1c92-4f2d-9396-7316819d0f2f
  Args:
    relation: :hasBirthYear
    literal_value: 1936
    source: Friedrich_August_of_Oldenburg
    literal_type: xsd:integer
  AddLiteral (bb1db423-91b3-4393-a47b-fa6a53240575)
 Call ID: bb1db423-91b3-4393-a47b-fa6a53240575
  Args:
    relation: :hasDeathYear
    literal_value: 2017
    source: Friedrich_August_of_Oldenburg
    literal_type: xsd:integer
  AssignClass (8a845794-b481-4489-b194-2e557e5b0154)
 Call ID: 8a845794-b481-4489-b194-2e557e5b0154
  Args:
    source: Nikolaus_of_Oldenburg
    type: :Man
  AssignClass (b1ade980-2b54-4cd8-b41e-24e8bcac5caf)
 Call ID: b1ade980-2b54-4cd8-b41e-24e8bcac5caf
  Args:
    type: :Person
    source: Nikolaus_of_Oldenburg
  AssignClass (796b04c4-7c27-43e6-8419-767df3255a4c)
 Call ID: 796b04c4-7c27-43e6-8419-767df3255a4c
  Args:
    type: :Woman
    source: Helena_of_Waldeck_and_Pyrmont
  AssignClass (0e1538c0-99c2-4416-a444-95626e3fba24)
 Call ID: 0e1538c0-99c2-4416-a444-95626e3fba24
  Args:
    type: :Person
    source: Helena_of_Waldeck_and_Pyrmont
  AddTriple (e3537012-c7dc-4156-8add-50ca67d444a8)
 Call ID: e3537012-c7dc-4156-8add-50ca67d444a8
  Args:
    target: Nikolaus_of_Oldenburg
    source: Friedrich_August_of_Oldenburg
    relation: :hasFather
  AddTriple (4cfeab93-3b42-4dcc-83cd-2976294a3fae)
 Call ID: 4cfeab93-3b42-4dcc-83cd-2976294a3fae
  Args:
    relation: :hasMother
    source: Friedrich_August_of_Oldenburg
    target: Helena_of_Waldeck_and_Pyrmont
  AssignClass (0983c5ed-75af-4238-9d63-968ec6c7664f)
 Call ID: 0983c5ed-75af-4238-9d63-968ec6c7664f
  Args:
    source: Frederick_Augustus_II_of_Oldenburg
    type: :Man
  AssignClass (5c817440-cfca-431a-8f7c-d0e882f43f47)
 Call ID: 5c817440-cfca-431a-8f7c-d0e882f43f47
  Args:
    type: :Person
    source: Frederick_Augustus_II_of_Oldenburg
  AssignClass (8c40e360-7f46-421e-a2a4-dbe089fd4feb)
 Call ID: 8c40e360-7f46-421e-a2a4-dbe089fd4feb
  Args:
    type: :Woman
    source: Elisabeth_Alexandrine_of_Mecklenburg_Schwerin
  AssignClass (a4ff28f7-4fbf-4b83-894f-61d278ba5438)
 Call ID: a4ff28f7-4fbf-4b83-894f-61d278ba5438
  Args:
    source: Elisabeth_Alexandrine_of_Mecklenburg_Schwerin
    type: :Person
  AddTriple (0498f8b0-87b0-40b9-9e5e-9b7bb6a3478b)
 Call ID: 0498f8b0-87b0-40b9-9e5e-9b7bb6a3478b
  Args:
    relation: :hasFather
    target: Frederick_Augustus_II_of_Oldenburg
    source: Nikolaus_of_Oldenburg
  AddTriple (1e852960-4ebf-45d0-a0a2-97dfb9666e73)
 Call ID: 1e852960-4ebf-45d0-a0a2-97dfb9666e73
  Args:
    relation: :hasMother
    target: Elisabeth_Alexandrine_of_Mecklenburg_Schwerin
    source: Nikolaus_of_Oldenburg
  AssignClass (f2085a4a-8a53-45a7-a275-acc2e7b55393)
 Call ID: f2085a4a-8a53-45a7-a275-acc2e7b55393
  Args:
    type: :Man
    source: Friedrich_of_Waldeck_and_Pyrmont
  AssignClass (4374f658-cdc5-4a44-b20d-657ac7307428)
 Call ID: 4374f658-cdc5-4a44-b20d-657ac7307428
  Args:
    type: :Person
    source: Friedrich_of_Waldeck_and_Pyrmont
  AssignClass (fc208f97-b591-446c-9219-dca72f12783d)
 Call ID: fc208f97-b591-446c-9219-dca72f12783d
  Args:
    source: Bathildis_of_Schaumburg_Lippe
    type: :Woman
  AssignClass (0fe00856-d2c4-4fdb-8e21-faae6e70265a)
 Call ID: 0fe00856-d2c4-4fdb-8e21-faae6e70265a
  Args:
    type: :Person
    source: Bathildis_of_Schaumburg_Lippe
  AddTriple (bbf1fb00-4422-4cc9-873b-00aff4fe4a83)
 Call ID: bbf1fb00-4422-4cc9-873b-00aff4fe4a83
  Args:
    relation: :hasFather
    target: Friedrich_of_Waldeck_and_Pyrmont
    source: Helena_of_Waldeck_and_Pyrmont
  AddTriple (ff0694c1-7be6-476b-9814-908bc4ea5f4b)
 Call ID: ff0694c1-7be6-476b-9814-908bc4ea5f4b
  Args:
    source: Helena_of_Waldeck_and_Pyrmont
    target: Bathildis_of_Schaumburg_Lippe
    relation: :hasMother
  AssignClass (50ad67c6-2697-4238-a087-c24bb0c7571b)
 Call ID: 50ad67c6-2697-4238-a087-c24bb0c7571b
  Args:
    source: Christian_of_Oldenburg
    type: :Man
  AssignClass (73503c9a-7a89-4595-8d04-44cbf318bea8)
 Call ID: 73503c9a-7a89-4595-8d04-44cbf318bea8
  Args:
    source: Christian_of_Oldenburg
    type: :Person
  AddTriple (37ab84e1-fdea-43f1-9c31-4670a237e73b)
 Call ID: 37ab84e1-fdea-43f1-9c31-4670a237e73b
  Args:
    relation: :isUncleOf
    source: Friedrich_August_of_Oldenburg
    target: Christian_of_Oldenburg
  AssignClass (666bf844-46f7-489a-b108-9a869ff58dbf)
 Call ID: 666bf844-46f7-489a-b108-9a869ff58dbf
  Args:
    source: Marie_Cecile_of_Prussia
    type: :Woman
  AssignClass (9c51d860-bc75-4323-91fe-29297e609ab4)
 Call ID: 9c51d860-bc75-4323-91fe-29297e609ab4
  Args:
    source: Marie_Cecile_of_Prussia
    type: :Person
  AddTriple (928ebf1b-a104-4f76-8dd6-feed543b495e)
 Call ID: 928ebf1b-a104-4f76-8dd6-feed543b495e
  Args:
    target: Marie_Cecile_of_Prussia
    source: Friedrich_August_of_Oldenburg
    relation: :hasRelation
  AssignClass (f41c9d4a-3453-4610-b94d-6c9de80cee6f)
 Call ID: f41c9d4a-3453-4610-b94d-6c9de80cee6f
  Args:
    source: Louis_Ferdinand_of_Prussia
    type: :Man
  AssignClass (b97090c3-cfdd-4306-884a-efdb22ad8300)
 Call ID: b97090c3-cfdd-4306-884a-efdb22ad8300
  Args:
    source: Louis_Ferdinand_of_Prussia
    type: :Person
  AssignClass (249d3b7b-c984-40a6-aff0-ce13124f69d4)
 Call ID: 249d3b7b-c984-40a6-aff0-ce13124f69d4
  Args:
    source: Kira_Kirillovna_of_Russia
    type: :Woman
  AssignClass (1d7aa614-165e-4661-9017-ef79e1ac0459)
 Call ID: 1d7aa614-165e-4661-9017-ef79e1ac0459
  Args:
    type: :Person
    source: Kira_Kirillovna_of_Russia
  AddTriple (454bcfeb-80f3-4c5e-abf5-812943391630)
 Call ID: 454bcfeb-80f3-4c5e-abf5-812943391630
  Args:
    source: Marie_Cecile_of_Prussia
    target: Louis_Ferdinand_of_Prussia
    relation: :hasFather
  AddTriple (cf30d856-f382-41e0-b338-087818a492ce)
 Call ID: cf30d856-f382-41e0-b338-087818a492ce
  Args:
    relation: :hasMother
    source: Marie_Cecile_of_Prussia
    target: Kira_Kirillovna_of_Russia
  AssignClass (8f46657b-5cfe-4a69-b4de-47e1e3f30e2e)
 Call ID: 8f46657b-5cfe-4a69-b4de-47e1e3f30e2e
  Args:
    type: :Woman
    source: Donata_of_Castell_Rudenhausen
  AssignClass (1bbb2e59-870c-4173-8f49-cbd3892c177c)
 Call ID: 1bbb2e59-870c-4173-8f49-cbd3892c177c
  Args:
    source: Donata_of_Castell_Rudenhausen
    type: :Person
  AddTriple (491b718a-7d5c-45d0-8466-a55ee79d271e)
 Call ID: 491b718a-7d5c-45d0-8466-a55ee79d271e
  Args:
    relation: :hasRelation
    target: Donata_of_Castell_Rudenhausen
    source: Friedrich_August_of_Oldenburg
  Finish (e28db52f-d614-4384-88c0-dca988ffdb84)
 Call ID: e28db52f-d614-4384-88c0-dca988ffdb84
  Args: