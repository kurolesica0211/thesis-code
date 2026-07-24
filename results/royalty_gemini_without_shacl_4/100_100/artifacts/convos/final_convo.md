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
The Crown PrinceThe Crown Princess


Princess Tomislav


Princess Alexander


Princess Elizabeth


Prince Dimitri Nicholas Paul George Maria of Yugoslavia (born 18 June 1958), also known as Dimitri Karageorgevich or Dimitrije Karađorđević, is a gemologist and member of the Royal House of Yugoslavia.
He founded the jewellery firm bearing his name, Prince Dimitri Company, and continues to serve as its president and creative director.
Life and career

Born in Boulogne-Billancourt, France, Prince Dimitri was raised in Versailles, attending boarding schools in France and Switzerland.
Prince Dimitri began designing jewellery in 1999, with a collection of gemstone cufflinks that was sold at Bergdorf Goodman and Saks Fifth Avenue.
In 2007, he and business partner Todd Morley founded the Prince Dimitri Company, which opened a salon in Manhattan.
Family

Prince Dimitri and Prince Michael of Yugoslavia are the first set of twins born to Prince Alexander of Yugoslavia and his first wife, Princess Maria Pia of Savoy, the eldest daughter of Umberto II of Italy in 1958.
Maria Pia had a second set of twins, Prince Serge and Princess Helene of Yugoslavia in 1963.
They have a younger half-brother, Prince Dushan of Yugoslavia, from their father's second marriage to Princess Barbara of Liechtenstein.
Prince Dimitri belongs to the cadet branch of the Royal House of Yugoslavia, descending from Prince Regent Paul of Yugoslavia.
He is a third cousin of Alexander, Crown Prince of Yugoslavia.
Honours

Ancestry

Dimitri is a member of the House of Karađorđević cadet branch.
He is a great-great-grandson of Prince Alexander of Serbia (reigned 1842–1858).
Through his father, Dimitri descends from kings George I of Greece and Christian IX of Denmark, as well as emperor Alexander II of Russia.
Through his mother, Dimitri descends from kings Umberto II of Italy, Albert I of Belgium, and furthermore from Nicholas I of Montenegro and Miguel I of Portugal.



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
  AssignClass (811c27cc-ecb4-459b-bc8f-d43ed3dd83e1)
 Call ID: 811c27cc-ecb4-459b-bc8f-d43ed3dd83e1
  Args:
    source: Prince_Dimitri_of_Yugoslavia
    type: :Man
  AssignClass (fc0f2db6-8c10-4b18-94a0-971e1c9d3558)
 Call ID: fc0f2db6-8c10-4b18-94a0-971e1c9d3558
  Args:
    source: Prince_Dimitri_of_Yugoslavia
    type: :Person
  AddLiteral (b3e1e480-27ef-4783-82cb-7faeed3020c0)
 Call ID: b3e1e480-27ef-4783-82cb-7faeed3020c0
  Args:
    literal_value: 1958
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Prince_Dimitri_of_Yugoslavia
  AddLiteral (8ef41634-15d7-4a8c-b0bb-32814847b63b)
 Call ID: 8ef41634-15d7-4a8c-b0bb-32814847b63b
  Args:
    literal_value: Dimitri Karageorgevich
    relation: :alsoKnownAs
    literal_type: xsd:string
    source: Prince_Dimitri_of_Yugoslavia
  AddLiteral (09d3745d-7a26-4c81-83ee-1f749edbefc5)
 Call ID: 09d3745d-7a26-4c81-83ee-1f749edbefc5
  Args:
    literal_value: Dimitrije Karađorđević
    relation: :alsoKnownAs
    literal_type: xsd:string
    source: Prince_Dimitri_of_Yugoslavia
  AssignClass (40b27ae7-f046-4d16-a7c8-588e52c046a2)
 Call ID: 40b27ae7-f046-4d16-a7c8-588e52c046a2
  Args:
    source: Prince_Michael_of_Yugoslavia
    type: :Man
  AssignClass (fb1d4e08-deb3-4580-a780-16c936005c8b)
 Call ID: fb1d4e08-deb3-4580-a780-16c936005c8b
  Args:
    type: :Person
    source: Prince_Michael_of_Yugoslavia
  AssignClass (52aeaf2c-2903-4c0b-9207-92d4bb9d3d19)
 Call ID: 52aeaf2c-2903-4c0b-9207-92d4bb9d3d19
  Args:
    source: Prince_Alexander_of_Yugoslavia
    type: :Man
  AssignClass (780b32f3-752f-4ce7-a67a-33bf7f5f95ed)
 Call ID: 780b32f3-752f-4ce7-a67a-33bf7f5f95ed
  Args:
    type: :Person
    source: Prince_Alexander_of_Yugoslavia
  AssignClass (d734e59d-7f69-4f01-a41a-9b74499e11e5)
 Call ID: d734e59d-7f69-4f01-a41a-9b74499e11e5
  Args:
    type: :Woman
    source: Princess_Maria_Pia_of_Savoy
  AssignClass (2e55ad0f-549e-4d2c-8966-d67b8a9d52a9)
 Call ID: 2e55ad0f-549e-4d2c-8966-d67b8a9d52a9
  Args:
    source: Princess_Maria_Pia_of_Savoy
    type: :Person
  AddTriple (2b284cc8-c907-4ac9-bbcc-b78e967acf41)
 Call ID: 2b284cc8-c907-4ac9-bbcc-b78e967acf41
  Args:
    target: Prince_Alexander_of_Yugoslavia
    source: Prince_Dimitri_of_Yugoslavia
    relation: :hasFather
  AddTriple (212cbf01-a93c-479d-bbf4-3684879c0571)
 Call ID: 212cbf01-a93c-479d-bbf4-3684879c0571
  Args:
    relation: :hasMother
    source: Prince_Dimitri_of_Yugoslavia
    target: Princess_Maria_Pia_of_Savoy
  AddTriple (3e363d07-aa69-4b17-a981-823db2b06f50)
 Call ID: 3e363d07-aa69-4b17-a981-823db2b06f50
  Args:
    relation: :hasFather
    target: Prince_Alexander_of_Yugoslavia
    source: Prince_Michael_of_Yugoslavia
  AddTriple (010fbb5e-59b3-42a0-82ee-9d759dc007fa)
 Call ID: 010fbb5e-59b3-42a0-82ee-9d759dc007fa
  Args:
    target: Princess_Maria_Pia_of_Savoy
    source: Prince_Michael_of_Yugoslavia
    relation: :hasMother
  AssignClass (4bc258da-1a8f-42cc-8de8-1232885f8238)
 Call ID: 4bc258da-1a8f-42cc-8de8-1232885f8238
  Args:
    type: :Man
    source: Prince_Serge_of_Yugoslavia
  AssignClass (ba21ae7d-2a07-4184-9350-e5b30bbe33d5)
 Call ID: ba21ae7d-2a07-4184-9350-e5b30bbe33d5
  Args:
    source: Prince_Serge_of_Yugoslavia
    type: :Person
  AssignClass (c260ced1-c4c0-460c-a047-7be1d8cf5e7c)
 Call ID: c260ced1-c4c0-460c-a047-7be1d8cf5e7c
  Args:
    source: Princess_Helene_of_Yugoslavia
    type: :Woman
  AssignClass (997e7b47-3f32-46db-81a2-16d4ef2c574f)
 Call ID: 997e7b47-3f32-46db-81a2-16d4ef2c574f
  Args:
    source: Princess_Helene_of_Yugoslavia
    type: :Person
  AddTriple (93734239-42b3-4ca6-8d79-1f737d9ee29a)
 Call ID: 93734239-42b3-4ca6-8d79-1f737d9ee29a
  Args:
    source: Prince_Serge_of_Yugoslavia
    target: Princess_Maria_Pia_of_Savoy
    relation: :hasMother
  AddTriple (547db9cb-49b6-48ce-9b41-cd77b9e4ba8d)
 Call ID: 547db9cb-49b6-48ce-9b41-cd77b9e4ba8d
  Args:
    target: Princess_Maria_Pia_of_Savoy
    source: Princess_Helene_of_Yugoslavia
    relation: :hasMother
  AssignClass (566f7371-74c9-4485-8c5c-71229914cece)
 Call ID: 566f7371-74c9-4485-8c5c-71229914cece
  Args:
    type: :Man
    source: Prince_Dushan_of_Yugoslavia
  AssignClass (72e3bbf7-c32d-4286-a6bf-30d696e2e3d7)
 Call ID: 72e3bbf7-c32d-4286-a6bf-30d696e2e3d7
  Args:
    source: Prince_Dushan_of_Yugoslavia
    type: :Person
  AddTriple (fd483bb6-b730-4a90-bc35-06b5d0240f05)
 Call ID: fd483bb6-b730-4a90-bc35-06b5d0240f05
  Args:
    relation: :hasFather
    source: Prince_Dushan_of_Yugoslavia
    target: Prince_Alexander_of_Yugoslavia
  AssignClass (f776d02b-aabc-47e9-a969-9fc4668faa0d)
 Call ID: f776d02b-aabc-47e9-a969-9fc4668faa0d
  Args:
    type: :Woman
    source: Princess_Barbara_of_Liechtenstein
  AssignClass (ad3ce135-75bb-4876-94c5-8106215f42d1)
 Call ID: ad3ce135-75bb-4876-94c5-8106215f42d1
  Args:
    source: Princess_Barbara_of_Liechtenstein
    type: :Person
  AddTriple (370e952f-26ed-470f-8854-015ea3718468)
 Call ID: 370e952f-26ed-470f-8854-015ea3718468
  Args:
    target: Princess_Barbara_of_Liechtenstein
    source: Prince_Dushan_of_Yugoslavia
    relation: :hasMother
  AssignClass (09ba066d-c1f9-4c6c-8994-ee58672fb764)
 Call ID: 09ba066d-c1f9-4c6c-8994-ee58672fb764
  Args:
    source: Umberto_II_of_Italy
    type: :Man
  AssignClass (7c3dda61-3d17-4736-bc74-f4a0d591a659)
 Call ID: 7c3dda61-3d17-4736-bc74-f4a0d591a659
  Args:
    source: Umberto_II_of_Italy
    type: :Person
  AddTriple (a85edcb7-4f17-4a6d-b344-93b446d914a0)
 Call ID: a85edcb7-4f17-4a6d-b344-93b446d914a0
  Args:
    relation: :hasFather
    source: Princess_Maria_Pia_of_Savoy
    target: Umberto_II_of_Italy
  Finish (d5ee13ba-ff1a-4f6a-8263-ca7370c4a01e)
 Call ID: d5ee13ba-ff1a-4f6a-8263-ca7370c4a01e
  Args: