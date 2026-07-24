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
  AssignClass (86333c75-892c-467e-8bce-8fddb3414be5)
 Call ID: 86333c75-892c-467e-8bce-8fddb3414be5
  Args:
    type: :Man
    source: Don_Carlos
  AssignClass (2db61f14-6ec7-44ed-a32f-d977e9e88033)
 Call ID: 2db61f14-6ec7-44ed-a32f-d977e9e88033
  Args:
    type: :Person
    source: Don_Carlos
  AddLiteral (921ac303-1387-45fb-b811-7a3d9b0b8284)
 Call ID: 921ac303-1387-45fb-b811-7a3d9b0b8284
  Args:
    literal_type: xsd:integer
    source: Don_Carlos
    literal_value: 1870
    relation: :hasBirthYear
  AddLiteral (ea396c55-6106-4f4f-9228-04c3e84eefa6)
 Call ID: ea396c55-6106-4f4f-9228-04c3e84eefa6
  Args:
    source: Don_Carlos
    literal_value: 1949
    relation: :hasDeathYear
    literal_type: xsd:integer
  AssignClass (04a65aeb-b4fb-4990-97f2-d1b402b0aa08)
 Call ID: 04a65aeb-b4fb-4990-97f2-d1b402b0aa08
  Args:
    type: :Man
    source: Alfonso_of_the_Two_Sicilies
  AssignClass (b85de6ac-5525-46a6-8d4e-e0794d821514)
 Call ID: b85de6ac-5525-46a6-8d4e-e0794d821514
  Args:
    type: :Person
    source: Alfonso_of_the_Two_Sicilies
  AssignClass (6cd2f331-b220-4d57-9ca7-c986ab9af8ec)
 Call ID: 6cd2f331-b220-4d57-9ca7-c986ab9af8ec
  Args:
    type: :Woman
    source: Maria_Antonietta_of_Bourbon-Two_Sicilies
  AssignClass (52bb6027-a7d5-425d-8d19-1d408638b728)
 Call ID: 52bb6027-a7d5-425d-8d19-1d408638b728
  Args:
    type: :Person
    source: Maria_Antonietta_of_Bourbon-Two_Sicilies
  AddTriple (dc87ee95-49ba-4d6f-b302-ee42bd35b543)
 Call ID: dc87ee95-49ba-4d6f-b302-ee42bd35b543
  Args:
    source: Don_Carlos
    relation: :hasFather
    target: Alfonso_of_the_Two_Sicilies
  AddTriple (06307231-29a3-476a-8024-cade78e3204f)
 Call ID: 06307231-29a3-476a-8024-cade78e3204f
  Args:
    target: Maria_Antonietta_of_Bourbon-Two_Sicilies
    source: Don_Carlos
    relation: :hasMother
  AssignClass (76443c1f-663d-4066-aaf8-9d774072f011)
 Call ID: 76443c1f-663d-4066-aaf8-9d774072f011
  Args:
    type: :Man
    source: Francis_II
  AssignClass (48f8482c-dc6a-47b0-a059-74c63ce58a75)
 Call ID: 48f8482c-dc6a-47b0-a059-74c63ce58a75
  Args:
    type: :Person
    source: Francis_II
  AddTriple (78e43e39-71ec-4701-b8d0-becc5de48ae9)
 Call ID: 78e43e39-71ec-4701-b8d0-becc5de48ae9
  Args:
    relation: :isBloodrelationOf
    source: Don_Carlos
    target: Francis_II
  AssignClass (d09ed589-f4f5-4aeb-8114-cddb5effcf2d)
 Call ID: d09ed589-f4f5-4aeb-8114-cddb5effcf2d
  Args:
    type: :Woman
    source: Mercedes_Princess_of_Asturias
  AssignClass (fe17859c-3871-4d98-8edf-50ea98029f4f)
 Call ID: fe17859c-3871-4d98-8edf-50ea98029f4f
  Args:
    type: :Person
    source: Mercedes_Princess_of_Asturias
  AddTriple (bbe8778e-34dc-40fc-9bdd-49bf2f01260a)
 Call ID: bbe8778e-34dc-40fc-9bdd-49bf2f01260a
  Args:
    target: Mercedes_Princess_of_Asturias
    relation: :hasRelation
    source: Don_Carlos
  AddLiteral (841614b4-76cb-4d27-ad35-32809cba26c8)
 Call ID: 841614b4-76cb-4d27-ad35-32809cba26c8
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    source: Don_Carlos
    literal_value: 1901
  AssignClass (d6e36b85-6ade-4594-8e50-ecfa43f65e20)
 Call ID: d6e36b85-6ade-4594-8e50-ecfa43f65e20
  Args:
    type: :Man
    source: Alfonso_XII_of_Spain
  AssignClass (f6930413-ba6a-4ef0-8939-23d63eb88bb4)
 Call ID: f6930413-ba6a-4ef0-8939-23d63eb88bb4
  Args:
    type: :Person
    source: Alfonso_XII_of_Spain
  AssignClass (f5c10935-6bae-4b52-a30e-95c61caae737)
 Call ID: f5c10935-6bae-4b52-a30e-95c61caae737
  Args:
    type: :Woman
    source: Maria_Christina_of_Austria
  AssignClass (8d82e42f-53f7-4e83-8511-e5463eb0f457)
 Call ID: 8d82e42f-53f7-4e83-8511-e5463eb0f457
  Args:
    type: :Person
    source: Maria_Christina_of_Austria
  AddTriple (bfdfc2dc-66cd-4cdf-9244-d5dabaa0cf14)
 Call ID: bfdfc2dc-66cd-4cdf-9244-d5dabaa0cf14
  Args:
    relation: :hasFather
    source: Mercedes_Princess_of_Asturias
    target: Alfonso_XII_of_Spain
  AddTriple (9d27ea80-2b4e-42c6-b2b0-dfcc9af926ff)
 Call ID: 9d27ea80-2b4e-42c6-b2b0-dfcc9af926ff
  Args:
    target: Maria_Christina_of_Austria
    relation: :hasMother
    source: Mercedes_Princess_of_Asturias
  AssignClass (ec0ad4d1-839f-4465-9c33-91b3fa7e9f48)
 Call ID: ec0ad4d1-839f-4465-9c33-91b3fa7e9f48
  Args:
    type: :Man
    source: Alfonso_XIII_of_Spain
  AssignClass (db18d45b-95fa-4694-a034-5c0e2ff5e8e3)
 Call ID: db18d45b-95fa-4694-a034-5c0e2ff5e8e3
  Args:
    type: :Person
    source: Alfonso_XIII_of_Spain
  AddTriple (d40570a7-f527-4926-85c6-fe39d2abfcee)
 Call ID: d40570a7-f527-4926-85c6-fe39d2abfcee
  Args:
    target: Alfonso_XIII_of_Spain
    relation: :isSisterOf
    source: Mercedes_Princess_of_Asturias
  AssignClass (93b13d06-21a0-49c2-a0d4-ffd0373dd253)
 Call ID: 93b13d06-21a0-49c2-a0d4-ffd0373dd253
  Args:
    type: :Woman
    source: Louise_of_Orleans
  AssignClass (0d36b9b6-8a92-4da2-a4e6-6e31b6e51be8)
 Call ID: 0d36b9b6-8a92-4da2-a4e6-6e31b6e51be8
  Args:
    type: :Person
    source: Louise_of_Orleans
  AddTriple (f06fcdd5-ef64-45ed-8582-3c11b2e40db5)
 Call ID: f06fcdd5-ef64-45ed-8582-3c11b2e40db5
  Args:
    relation: :hasRelation
    source: Don_Carlos
    target: Louise_of_Orleans
  AddLiteral (0ff859b3-a12c-4b27-89f0-2846af8a0c45)
 Call ID: 0ff859b3-a12c-4b27-89f0-2846af8a0c45
  Args:
    literal_type: xsd:integer
    source: Don_Carlos
    literal_value: 1907
    relation: :hasMarriageYear
  AssignClass (4c2e3d98-8dff-4a49-b8bd-f358935dbf05)
 Call ID: 4c2e3d98-8dff-4a49-b8bd-f358935dbf05
  Args:
    type: :Man
    source: Philippe_Count_of_Paris
  AssignClass (6ada1bf7-ad9b-4115-ba9f-ae6e00d12242)
 Call ID: 6ada1bf7-ad9b-4115-ba9f-ae6e00d12242
  Args:
    type: :Person
    source: Philippe_Count_of_Paris
  AddTriple (55dd0770-e75f-4fea-afb3-e6300273a444)
 Call ID: 55dd0770-e75f-4fea-afb3-e6300273a444
  Args:
    relation: :hasFather
    source: Louise_of_Orleans
    target: Philippe_Count_of_Paris
  AssignClass (0e26468b-6381-470e-8892-7e7c59db8a62)
 Call ID: 0e26468b-6381-470e-8892-7e7c59db8a62
  Args:
    type: :Man
    source: Ferdinand
  AssignClass (8fc166cd-cbc3-433b-aea3-52e7168aac63)
 Call ID: 8fc166cd-cbc3-433b-aea3-52e7168aac63
  Args:
    type: :Person
    source: Ferdinand
  AddTriple (90bce6a1-d3d1-458f-9765-040e1c55e743)
 Call ID: 90bce6a1-d3d1-458f-9765-040e1c55e743
  Args:
    source: Don_Carlos
    relation: :isBrotherOf
    target: Ferdinand
  AssignClass (1abf27e2-0bfd-4433-a6cf-8899760fb03c)
 Call ID: 1abf27e2-0bfd-4433-a6cf-8899760fb03c
  Args:
    type: :Man
    source: Ranieri
  AssignClass (45820c55-3af1-4619-956d-0bd308158f98)
 Call ID: 45820c55-3af1-4619-956d-0bd308158f98
  Args:
    type: :Person
    source: Ranieri
  AddTriple (15124f99-27e6-4042-8bb2-63a19d7df9dc)
 Call ID: 15124f99-27e6-4042-8bb2-63a19d7df9dc
  Args:
    target: Ranieri
    relation: :isBrotherOf
    source: Don_Carlos
  AssignClass (f56fad52-0881-440f-90c9-620d0d641b0d)
 Call ID: f56fad52-0881-440f-90c9-620d0d641b0d
  Args:
    type: :Man
    source: Alfonso_son_of_Carlos
  AssignClass (747ae469-8c65-460c-b1af-6e9284fbad99)
 Call ID: 747ae469-8c65-460c-b1af-6e9284fbad99
  Args:
    type: :Person
    source: Alfonso_son_of_Carlos
  AddTriple (0a88a85f-ccd6-4382-83b8-a41793533ec5)
 Call ID: 0a88a85f-ccd6-4382-83b8-a41793533ec5
  Args:
    target: Don_Carlos
    relation: :isSonOf
    source: Alfonso_son_of_Carlos
  Finish (7793cfa2-92b3-467f-9da4-6d9cfd3c45fa)
 Call ID: 7793cfa2-92b3-467f-9da4-6d9cfd3c45fa
  Args: