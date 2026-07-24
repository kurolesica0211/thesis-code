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
Don Carlos, Prince of Bourbon-Two Sicilies, Infante of Spain (Full Italian name: Carlo Maria Francesco d'Assisi Pasquale Ferdinando Antonio di Padova Francesco de Paola Alfonso Andrea Avelino Tancredi, Principe di Borbone delle Due Sicilie, Infante di Spagna; 10 November 1870 – 11 November 1949) was the son of Prince Alfonso of the Two Sicilies, Count of Caserta and Princess Maria Antonietta of Bourbon-Two Sicilies, and nephew of the last King of the Two Sicilies, Francis II.


Marriages and children

On 14 February 1901 in Madrid, Carlos married Mercedes, Princess of Asturias, elder daughter of the late King Alfonso XII of Spain and of his wife Archduchess Maria Christina of Austria.
Mercedes was the elder sister and heir presumptive to King Alfonso XIII of Spain, an unmarried teenager.
A week before the wedding, on 7 February, Carlos was given the title of Infante of Spain.
In 1907, Carlos married secondly to Princess Louise of Orléans, daughter of Prince Philippe, Count of Paris.
The couple had four children:


Prince Carlos's descendants include King Felipe VI of Spain, Prince Pedro, Duke of Calabria, Prince Pedro Carlos of Orléans-Braganza, and Philip, Hereditary Prince of Yugoslavia, among others.
Military service

Carlos served in the Spanish Army in the Spanish–American War and received the Military Order of Maria Cristina.
Two Sicilies succession

In 1894, Carlos's father Alfonso became the head of the House of Bourbon-Two Sicilies.
On marrying his first wife, Carlos renounced on 14 December 1900 his future rights of succession to the non-existent Crown of Two Sicilies in an official document, known as the Act of Cannes, subject to a requirement in the Treaty of Naples of 1759 and the Pragmatic Decree of 6 October 1759 that the Crown of Spain should not be combined with the "Italian Sovereignty".
In 1960, Carlos' elder brother Ferdinand died without male issue, and a dispute arose between Carlos' son Alfonso and Carlos' younger brother Ranieri on the headship of the house, this with competing claims: by the law of primogeniture, Carlos' son Alfonso was considered the heir, but Ranieri claimed that Carlos had renounced his rights and those of his descendants according to the Act of Cannes.
Alfonso refuted that claim by stating that it was only a promise from his father to relinquish this right if the crown of the Kingdom of the Two Sicilies were to be united with the Spanish Crown.
Since this did not happen, the act had no effect and Carlos' son Alfonso reclaimed his rights.
Alfonso's claim was recognised by the heads of the different lines of the House of Bourbon, although not by the head of the Orleans family, and in 1983 the Spanish Council of State, following an investigation by the Ministries of Justice and Foreign Affairs, the Royal Academy of Jurisprudence and Legislation and the Institute Salazar y Castro concluded unanimously in favour of Infante Don Alfonso's only son, Prince and Infante Don Carlos, a position shared by the Spanish Royal House.



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
  AssignClass (53c3aff6-7d53-432b-99dd-74561a0249e1)
 Call ID: 53c3aff6-7d53-432b-99dd-74561a0249e1
  Args:
    source: Don_Carlos
    type: :Man
  AssignClass (8387c5a7-20f7-45e7-8a89-b174ab21501e)
 Call ID: 8387c5a7-20f7-45e7-8a89-b174ab21501e
  Args:
    source: Don_Carlos
    type: :Person
  AddLiteral (dbab8eb4-53c7-4753-bd3a-cc37fdde0190)
 Call ID: dbab8eb4-53c7-4753-bd3a-cc37fdde0190
  Args:
    literal_value: 1870
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Don_Carlos
  AddLiteral (d13e982a-0296-471c-b762-e5edf731b1b7)
 Call ID: d13e982a-0296-471c-b762-e5edf731b1b7
  Args:
    literal_value: 1949
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: Don_Carlos
  AssignClass (d829f875-0968-4c20-856e-16da8b167fda)
 Call ID: d829f875-0968-4c20-856e-16da8b167fda
  Args:
    source: Alfonso_Two_Sicilies
    type: :Man
  AssignClass (0b0f2046-0c2b-488f-841a-cd92828dd01c)
 Call ID: 0b0f2046-0c2b-488f-841a-cd92828dd01c
  Args:
    type: :Person
    source: Alfonso_Two_Sicilies
  AssignClass (ba2225e4-580f-4462-bb69-94b41e3cd445)
 Call ID: ba2225e4-580f-4462-bb69-94b41e3cd445
  Args:
    type: :Woman
    source: Maria_Antonietta
  AssignClass (d2b19f20-a4b7-4b24-8aeb-f014e98e2bd1)
 Call ID: d2b19f20-a4b7-4b24-8aeb-f014e98e2bd1
  Args:
    source: Maria_Antonietta
    type: :Person
  AddTriple (0f92a94c-83ff-46e7-86d1-842adf146506)
 Call ID: 0f92a94c-83ff-46e7-86d1-842adf146506
  Args:
    relation: :hasFather
    source: Don_Carlos
    target: Alfonso_Two_Sicilies
  AddTriple (70ce2545-eb6d-4ef1-b9d0-d9718c4f3525)
 Call ID: 70ce2545-eb6d-4ef1-b9d0-d9718c4f3525
  Args:
    target: Maria_Antonietta
    source: Don_Carlos
    relation: :hasMother
  AssignClass (6169e147-cb66-4b1d-ac13-a8260f433c8c)
 Call ID: 6169e147-cb66-4b1d-ac13-a8260f433c8c
  Args:
    type: :Man
    source: Francis_II
  AssignClass (2b4a99c3-b414-4d05-80c7-424ce0484c14)
 Call ID: 2b4a99c3-b414-4d05-80c7-424ce0484c14
  Args:
    type: :Person
    source: Francis_II
  AddTriple (1e5d0be5-0881-4580-8402-81670c755fa7)
 Call ID: 1e5d0be5-0881-4580-8402-81670c755fa7
  Args:
    target: Francis_II
    source: Don_Carlos
    relation: :isBloodrelationOf
  AssignClass (6a94fd36-1ccb-4293-b80c-69d798c45f4b)
 Call ID: 6a94fd36-1ccb-4293-b80c-69d798c45f4b
  Args:
    type: :Woman
    source: Mercedes_Asturias
  AssignClass (4ccc2be6-fd18-42cb-ad24-0d4179355859)
 Call ID: 4ccc2be6-fd18-42cb-ad24-0d4179355859
  Args:
    source: Mercedes_Asturias
    type: :Person
  AddTriple (5e6d2c05-5e65-48f3-806a-55d6482416b2)
 Call ID: 5e6d2c05-5e65-48f3-806a-55d6482416b2
  Args:
    source: Don_Carlos
    target: Mercedes_Asturias
    relation: :hasRelation
  AddLiteral (d8b8120e-cf1f-40cd-a830-d075b637bcf8)
 Call ID: d8b8120e-cf1f-40cd-a830-d075b637bcf8
  Args:
    literal_type: xsd:integer
    source: Don_Carlos
    relation: :hasMarriageYear
    literal_value: 1901
  AssignClass (c22b9138-339f-4c6f-8181-d01d2d3bd446)
 Call ID: c22b9138-339f-4c6f-8181-d01d2d3bd446
  Args:
    type: :Man
    source: Alfonso_XII_Spain
  AssignClass (46b3a7e9-8212-478a-afce-bdb1d35ed7cd)
 Call ID: 46b3a7e9-8212-478a-afce-bdb1d35ed7cd
  Args:
    source: Alfonso_XII_Spain
    type: :Person
  AssignClass (ad159af1-8451-4fcf-b831-d5d0794a034f)
 Call ID: ad159af1-8451-4fcf-b831-d5d0794a034f
  Args:
    source: Maria_Christina_Austria
    type: :Woman
  AssignClass (0882daaf-7a41-49aa-8ea8-824ba5e46cf6)
 Call ID: 0882daaf-7a41-49aa-8ea8-824ba5e46cf6
  Args:
    type: :Person
    source: Maria_Christina_Austria
  AddTriple (12ab7c34-1ae0-4437-8340-081f99584a6c)
 Call ID: 12ab7c34-1ae0-4437-8340-081f99584a6c
  Args:
    target: Alfonso_XII_Spain
    source: Mercedes_Asturias
    relation: :hasFather
  AddTriple (d9629334-ac10-4c5b-8dae-7babdaab47f0)
 Call ID: d9629334-ac10-4c5b-8dae-7babdaab47f0
  Args:
    target: Maria_Christina_Austria
    source: Mercedes_Asturias
    relation: :hasMother
  AssignClass (fd2b89b5-4107-4276-8c1e-3a7cf058d708)
 Call ID: fd2b89b5-4107-4276-8c1e-3a7cf058d708
  Args:
    type: :Man
    source: Alfonso_XIII_Spain
  AssignClass (16700d45-0e54-4213-9e4e-e7b2db335985)
 Call ID: 16700d45-0e54-4213-9e4e-e7b2db335985
  Args:
    source: Alfonso_XIII_Spain
    type: :Person
  AddTriple (e842d5e0-d7d5-4677-8092-800b691c922d)
 Call ID: e842d5e0-d7d5-4677-8092-800b691c922d
  Args:
    target: Alfonso_XIII_Spain
    source: Mercedes_Asturias
    relation: :isSisterOf
  AssignClass (ee6d75b0-82d1-4f6c-ae29-0ed26afbd612)
 Call ID: ee6d75b0-82d1-4f6c-ae29-0ed26afbd612
  Args:
    type: :Woman
    source: Louise_Orleans
  AssignClass (4adb71e3-e22f-4565-bcbb-aabd3d35d55b)
 Call ID: 4adb71e3-e22f-4565-bcbb-aabd3d35d55b
  Args:
    type: :Person
    source: Louise_Orleans
  AddTriple (70267561-403c-4726-857a-d5a157b90230)
 Call ID: 70267561-403c-4726-857a-d5a157b90230
  Args:
    relation: :hasRelation
    target: Louise_Orleans
    source: Don_Carlos
  AddLiteral (998c7d4c-286b-4a32-8cb4-743560e40028)
 Call ID: 998c7d4c-286b-4a32-8cb4-743560e40028
  Args:
    relation: :hasMarriageYear
    source: Don_Carlos
    literal_type: xsd:integer
    literal_value: 1907
  AssignClass (9da60d27-8c28-4b09-88c8-f7ab889ee392)
 Call ID: 9da60d27-8c28-4b09-88c8-f7ab889ee392
  Args:
    source: Philippe_Count_Paris
    type: :Man
  AssignClass (7747e31d-1d1b-4878-9a5c-b2fdc513c404)
 Call ID: 7747e31d-1d1b-4878-9a5c-b2fdc513c404
  Args:
    type: :Person
    source: Philippe_Count_Paris
  AddTriple (7b498417-7324-46f8-9f29-964c05b9ab3b)
 Call ID: 7b498417-7324-46f8-9f29-964c05b9ab3b
  Args:
    target: Philippe_Count_Paris
    source: Louise_Orleans
    relation: :hasFather
  AssignClass (ad1a1073-7519-489b-99a5-7498d4adeece)
 Call ID: ad1a1073-7519-489b-99a5-7498d4adeece
  Args:
    type: :Man
    source: Ferdinand_Two_Sicilies
  AssignClass (7fa9a450-aa56-4481-bd32-3d027e3ae477)
 Call ID: 7fa9a450-aa56-4481-bd32-3d027e3ae477
  Args:
    type: :Person
    source: Ferdinand_Two_Sicilies
  AddTriple (e2e3b587-3ebf-4850-86e4-d9cd3de6a9c2)
 Call ID: e2e3b587-3ebf-4850-86e4-d9cd3de6a9c2
  Args:
    target: Ferdinand_Two_Sicilies
    source: Don_Carlos
    relation: :isBrotherOf
  AssignClass (e93bef89-71ff-4c70-b1e6-8f1cb7316ac3)
 Call ID: e93bef89-71ff-4c70-b1e6-8f1cb7316ac3
  Args:
    source: Ranieri_Two_Sicilies
    type: :Man
  AssignClass (8a778520-65cc-4e18-b26a-422ca0686480)
 Call ID: 8a778520-65cc-4e18-b26a-422ca0686480
  Args:
    source: Ranieri_Two_Sicilies
    type: :Person
  AddTriple (76f947f7-a26c-4ff2-aa61-2def46cbb06f)
 Call ID: 76f947f7-a26c-4ff2-aa61-2def46cbb06f
  Args:
    target: Ranieri_Two_Sicilies
    source: Don_Carlos
    relation: :isBrotherOf
  AssignClass (94cd5aeb-2aa5-4fb6-91b0-e2deb2bb26f6)
 Call ID: 94cd5aeb-2aa5-4fb6-91b0-e2deb2bb26f6
  Args:
    type: :Man
    source: Alfonso_Son_of_Carlos
  AssignClass (baa8cf23-c540-4aba-b78c-201e831b0f14)
 Call ID: baa8cf23-c540-4aba-b78c-201e831b0f14
  Args:
    type: :Person
    source: Alfonso_Son_of_Carlos
  AddTriple (6aa87d35-2368-4a8d-a668-a7a1544c0068)
 Call ID: 6aa87d35-2368-4a8d-a668-a7a1544c0068
  Args:
    relation: :isSonOf
    target: Don_Carlos
    source: Alfonso_Son_of_Carlos
  Finish (0b3e6052-0b35-4b34-b48b-a63008144784)
 Call ID: 0b3e6052-0b35-4b34-b48b-a63008144784
  Args: