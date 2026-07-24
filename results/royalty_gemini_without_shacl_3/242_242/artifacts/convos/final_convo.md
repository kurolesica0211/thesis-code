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
Princess Marie Alexandra of Baden (Marie Alexandra Thyra Victoria Louise Carola Hilda; 1 August 1902 – 29 January 1944) was a Hessian princess by marriage.
Family

She was the only daughter and elder child of Prince Maximilian of Baden (1867–1929) and Princess Marie Louise of Hanover and Cumberland.
Her paternal grandparents were Prince Wilhelm of Baden (1829–97) and Princess Maria Maximilianovna of Leuchtenberg (1841–1914), a daughter of Maximilian, Duke of Leuchtenberg (1817–52) and Grand Duchess Maria Nikolaevna (1819–1876).
Princess Marie-Louise of Hanover (1879–1948) was a daughter of Ernest Augustus, Crown Prince of Hanover, claimant of the annexed Kingdom of Hanover.
Marriage

On 17 September 1924, she married her fourth cousin Prince Wolfgang of Hesse (1896–1989).
Death

Princess Marie Alexandra was killed in an attack by the U.S. Army Air Forces during an air-raid on Frankfurt am Main on 29–30 January 1944 during World War II.
She and seven other women, who were aid workers, were killed when the cellar, in which they had taken refuge, collapsed under the weight of the building, rendering Marie Alexandra's body barely recognisable.



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
  AssignClass (05d85f19-21d2-4618-9a80-da7babfe03a4)
 Call ID: 05d85f19-21d2-4618-9a80-da7babfe03a4
  Args:
    type: :Woman
    source: Marie_Alexandra_of_Baden
  AssignClass (639bcd69-9023-45a7-890a-c5492c4e6fd4)
 Call ID: 639bcd69-9023-45a7-890a-c5492c4e6fd4
  Args:
    type: :Man
    source: Prince_Maximilian_of_Baden
  AssignClass (76e3e59e-17d8-4074-a257-e6f4d6b61b5c)
 Call ID: 76e3e59e-17d8-4074-a257-e6f4d6b61b5c
  Args:
    type: :Woman
    source: Princess_Marie_Louise_of_Hanover_and_Cumberland
  AssignClass (114c6fcf-76f1-4b86-b5f9-8287d9e4d227)
 Call ID: 114c6fcf-76f1-4b86-b5f9-8287d9e4d227
  Args:
    type: :Man
    source: Prince_Wilhelm_of_Baden
  AssignClass (4ebb06f1-8c60-429a-b462-f334474a0396)
 Call ID: 4ebb06f1-8c60-429a-b462-f334474a0396
  Args:
    type: :Woman
    source: Princess_Maria_Maximilianovna_of_Leuchtenberg
  AssignClass (daa488a2-1c46-435c-a904-5180d7b10488)
 Call ID: daa488a2-1c46-435c-a904-5180d7b10488
  Args:
    type: :Man
    source: Maximilian_Duke_of_Leuchtenberg
  AssignClass (fece09d7-6cc0-4fd7-9e7b-3f2ff6821aba)
 Call ID: fece09d7-6cc0-4fd7-9e7b-3f2ff6821aba
  Args:
    type: :Woman
    source: Grand_Duchess_Maria_Nikolaevna
  AssignClass (3a5cd66f-9a52-4745-8275-9aea15c8b7ad)
 Call ID: 3a5cd66f-9a52-4745-8275-9aea15c8b7ad
  Args:
    type: :Man
    source: Ernest_Augustus_Crown_Prince_of_Hanover
  AssignClass (5ff8c94d-03ca-4ded-929a-9206c6e47632)
 Call ID: 5ff8c94d-03ca-4ded-929a-9206c6e47632
  Args:
    type: :Man
    source: Prince_Wolfgang_of_Hesse
  AddLiteral (02b406b9-2be7-4197-b0bf-b68e2a152365)
 Call ID: 02b406b9-2be7-4197-b0bf-b68e2a152365
  Args:
    relation: :hasBirthYear
    literal_value: 1902
    source: Marie_Alexandra_of_Baden
    literal_type: xsd:integer
  AddLiteral (d0931f23-36cc-46f2-9830-e571d53efc57)
 Call ID: d0931f23-36cc-46f2-9830-e571d53efc57
  Args:
    literal_type: xsd:integer
    source: Marie_Alexandra_of_Baden
    literal_value: 1944
    relation: :hasDeathYear
  AddLiteral (5b89123d-3704-4341-a5f7-76bbb1410e19)
 Call ID: 5b89123d-3704-4341-a5f7-76bbb1410e19
  Args:
    literal_type: xsd:integer
    source: Prince_Maximilian_of_Baden
    relation: :hasBirthYear
    literal_value: 1867
  AddLiteral (8afc5732-a679-4ac2-85af-11941ab3cd31)
 Call ID: 8afc5732-a679-4ac2-85af-11941ab3cd31
  Args:
    literal_value: 1929
    relation: :hasDeathYear
    source: Prince_Maximilian_of_Baden
    literal_type: xsd:integer
  AddLiteral (238bc818-bae2-45ed-943e-71e81b8002e1)
 Call ID: 238bc818-bae2-45ed-943e-71e81b8002e1
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1879
    source: Princess_Marie_Louise_of_Hanover_and_Cumberland
  AddLiteral (f4edcda8-91cb-4af1-8a32-b9ab4e4baa81)
 Call ID: f4edcda8-91cb-4af1-8a32-b9ab4e4baa81
  Args:
    source: Princess_Marie_Louise_of_Hanover_and_Cumberland
    literal_value: 1948
    relation: :hasDeathYear
    literal_type: xsd:integer
  AddLiteral (b6ce6868-213d-40bc-90c0-7b3f73e2c0ed)
 Call ID: b6ce6868-213d-40bc-90c0-7b3f73e2c0ed
  Args:
    literal_type: xsd:integer
    literal_value: 1829
    relation: :hasBirthYear
    source: Prince_Wilhelm_of_Baden
  AddLiteral (9433506d-0983-4915-98bf-4f8f2fddde50)
 Call ID: 9433506d-0983-4915-98bf-4f8f2fddde50
  Args:
    literal_value: 1897
    relation: :hasDeathYear
    source: Prince_Wilhelm_of_Baden
    literal_type: xsd:integer
  AddLiteral (56d9e026-ef2a-4057-8776-7338d2599ef5)
 Call ID: 56d9e026-ef2a-4057-8776-7338d2599ef5
  Args:
    source: Princess_Maria_Maximilianovna_of_Leuchtenberg
    literal_value: 1841
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (74274c08-1dff-4fcd-827b-3410e3529fa5)
 Call ID: 74274c08-1dff-4fcd-827b-3410e3529fa5
  Args:
    source: Princess_Maria_Maximilianovna_of_Leuchtenberg
    relation: :hasDeathYear
    literal_value: 1914
    literal_type: xsd:integer
  AddLiteral (a46ed10d-feb1-467f-8543-70e27c48ba89)
 Call ID: a46ed10d-feb1-467f-8543-70e27c48ba89
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1817
    source: Maximilian_Duke_of_Leuchtenberg
  AddLiteral (b490b284-876f-4869-8b43-b9fb3ed06b0a)
 Call ID: b490b284-876f-4869-8b43-b9fb3ed06b0a
  Args:
    source: Maximilian_Duke_of_Leuchtenberg
    literal_value: 1852
    relation: :hasDeathYear
    literal_type: xsd:integer
  AddLiteral (0fcd609f-7e9d-414d-92b3-89ba9e0e6d63)
 Call ID: 0fcd609f-7e9d-414d-92b3-89ba9e0e6d63
  Args:
    literal_type: xsd:integer
    literal_value: 1819
    relation: :hasBirthYear
    source: Grand_Duchess_Maria_Nikolaevna
  AddLiteral (de0f5ca0-c8e3-456a-bcb3-e732a35657f6)
 Call ID: de0f5ca0-c8e3-456a-bcb3-e732a35657f6
  Args:
    literal_type: xsd:integer
    source: Grand_Duchess_Maria_Nikolaevna
    relation: :hasDeathYear
    literal_value: 1876
  AddLiteral (ce67ae22-93f4-4e29-b97f-23b40e13990b)
 Call ID: ce67ae22-93f4-4e29-b97f-23b40e13990b
  Args:
    literal_type: xsd:integer
    literal_value: 1896
    relation: :hasBirthYear
    source: Prince_Wolfgang_of_Hesse
  AddLiteral (4e6ad24d-e231-49d1-bcc2-39164cc713b7)
 Call ID: 4e6ad24d-e231-49d1-bcc2-39164cc713b7
  Args:
    relation: :hasDeathYear
    literal_value: 1989
    source: Prince_Wolfgang_of_Hesse
    literal_type: xsd:integer
  AddLiteral (1c1cbb97-f95b-444f-b633-322dca8ba5c0)
 Call ID: 1c1cbb97-f95b-444f-b633-322dca8ba5c0
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 1924
    source: Marie_Alexandra_of_Baden
  AddTriple (b5a1b3f5-5123-48a2-8c62-cefd62da7741)
 Call ID: b5a1b3f5-5123-48a2-8c62-cefd62da7741
  Args:
    source: Marie_Alexandra_of_Baden
    relation: :isDaughterOf
    target: Prince_Maximilian_of_Baden
  AddTriple (82ff6ffc-5cb4-4133-9f07-ceecfeef6bd5)
 Call ID: 82ff6ffc-5cb4-4133-9f07-ceecfeef6bd5
  Args:
    source: Marie_Alexandra_of_Baden
    relation: :isDaughterOf
    target: Princess_Marie_Louise_of_Hanover_and_Cumberland
  AddTriple (f62a0049-dca4-485b-8702-07b3fddd100f)
 Call ID: f62a0049-dca4-485b-8702-07b3fddd100f
  Args:
    target: Ernest_Augustus_Crown_Prince_of_Hanover
    relation: :isDaughterOf
    source: Princess_Marie_Louise_of_Hanover_and_Cumberland
  AddTriple (c7b74826-b495-49ec-8679-abedd26b77fd)
 Call ID: c7b74826-b495-49ec-8679-abedd26b77fd
  Args:
    relation: :isFatherOf
    target: Prince_Maximilian_of_Baden
    source: Prince_Wilhelm_of_Baden
  AddTriple (5503c0b6-57ad-4195-8d6b-7912a70badd7)
 Call ID: 5503c0b6-57ad-4195-8d6b-7912a70badd7
  Args:
    source: Princess_Maria_Maximilianovna_of_Leuchtenberg
    target: Prince_Maximilian_of_Baden
    relation: :isMotherOf
  AddTriple (5d63a3bf-da28-4c4e-8b2c-00646296e441)
 Call ID: 5d63a3bf-da28-4c4e-8b2c-00646296e441
  Args:
    source: Princess_Maria_Maximilianovna_of_Leuchtenberg
    relation: :isDaughterOf
    target: Maximilian_Duke_of_Leuchtenberg
  AddTriple (ea19bcbe-81df-4a71-8c5a-6ca695b0bc60)
 Call ID: ea19bcbe-81df-4a71-8c5a-6ca695b0bc60
  Args:
    source: Princess_Maria_Maximilianovna_of_Leuchtenberg
    relation: :isDaughterOf
    target: Grand_Duchess_Maria_Nikolaevna
  Finish (057e1fe3-4533-4f80-a2b7-687ba053b23e)
 Call ID: 057e1fe3-4533-4f80-a2b7-687ba053b23e
  Args: