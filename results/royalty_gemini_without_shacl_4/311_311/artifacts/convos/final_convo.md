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
  AssignClass (3afa6627-a841-4ceb-9484-97842c4d8113)
 Call ID: 3afa6627-a841-4ceb-9484-97842c4d8113
  Args:
    type: :Man
    source: Don_Carlos
  AssignClass (8d0391ff-448d-44d5-ba1e-aba6556a57c5)
 Call ID: 8d0391ff-448d-44d5-ba1e-aba6556a57c5
  Args:
    type: :Person
    source: Don_Carlos
  AddLiteral (bf78fa99-c68a-49a5-93be-b577f4b8e4a0)
 Call ID: bf78fa99-c68a-49a5-93be-b577f4b8e4a0
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1870
    source: Don_Carlos
  AddLiteral (fb1922ad-2e3d-4c82-a070-8056e1ad7fc5)
 Call ID: fb1922ad-2e3d-4c82-a070-8056e1ad7fc5
  Args:
    literal_type: xsd:integer
    literal_value: 1949
    source: Don_Carlos
    relation: :hasDeathYear
  AssignClass (a7667af3-a7fb-4921-92a6-dc3e2a135332)
 Call ID: a7667af3-a7fb-4921-92a6-dc3e2a135332
  Args:
    type: :Man
    source: Alfonso_of_the_Two_Sicilies
  AssignClass (2276c1bd-c682-4c15-89dd-a9b886e8ffad)
 Call ID: 2276c1bd-c682-4c15-89dd-a9b886e8ffad
  Args:
    type: :Person
    source: Alfonso_of_the_Two_Sicilies
  AssignClass (f05bb6b9-6a70-4dc4-98b8-4b8a4a37e80f)
 Call ID: f05bb6b9-6a70-4dc4-98b8-4b8a4a37e80f
  Args:
    type: :Woman
    source: Maria_Antonietta_of_Bourbon-Two_Sicilies
  AssignClass (2c41348f-ce63-4e0f-ac5c-a9e62a440d08)
 Call ID: 2c41348f-ce63-4e0f-ac5c-a9e62a440d08
  Args:
    type: :Person
    source: Maria_Antonietta_of_Bourbon-Two_Sicilies
  AddTriple (3b6fcaf8-ed26-4e9a-84a7-4d4ae360e92f)
 Call ID: 3b6fcaf8-ed26-4e9a-84a7-4d4ae360e92f
  Args:
    relation: :hasFather
    target: Alfonso_of_the_Two_Sicilies
    source: Don_Carlos
  AddTriple (64f057ab-4bd7-4759-a617-8d39ce36c532)
 Call ID: 64f057ab-4bd7-4759-a617-8d39ce36c532
  Args:
    source: Don_Carlos
    relation: :hasMother
    target: Maria_Antonietta_of_Bourbon-Two_Sicilies
  AssignClass (288c4414-c8aa-4e07-b70f-166b79b522e0)
 Call ID: 288c4414-c8aa-4e07-b70f-166b79b522e0
  Args:
    type: :Man
    source: Francis_II
  AssignClass (0f384f23-a8bf-440e-8d6f-16489acf8caa)
 Call ID: 0f384f23-a8bf-440e-8d6f-16489acf8caa
  Args:
    type: :Person
    source: Francis_II
  AssignClass (3263c2f2-ec9a-4cf6-9ab2-f99b3788248f)
 Call ID: 3263c2f2-ec9a-4cf6-9ab2-f99b3788248f
  Args:
    type: :Woman
    source: Mercedes_Princess_of_Asturias
  AssignClass (26f1f31e-3c97-4e5f-92f5-95ff20524bd2)
 Call ID: 26f1f31e-3c97-4e5f-92f5-95ff20524bd2
  Args:
    type: :Person
    source: Mercedes_Princess_of_Asturias
  AddTriple (c554d7da-b5a1-4cb2-b888-958fe31a4dc3)
 Call ID: c554d7da-b5a1-4cb2-b888-958fe31a4dc3
  Args:
    source: Mercedes_Princess_of_Asturias
    target: Alfonso_XII_of_Spain
    relation: :hasFather
  AddTriple (80a6ddd9-059d-470d-aebf-b7462610aca0)
 Call ID: 80a6ddd9-059d-470d-aebf-b7462610aca0
  Args:
    source: Mercedes_Princess_of_Asturias
    relation: :hasMother
    target: Maria_Christina_of_Austria
  AssignClass (10b8cca3-aa5c-428f-8678-35b10b117345)
 Call ID: 10b8cca3-aa5c-428f-8678-35b10b117345
  Args:
    type: :Man
    source: Alfonso_XII_of_Spain
  AssignClass (98aeea36-f37e-4420-80bb-cd64e0d9ea92)
 Call ID: 98aeea36-f37e-4420-80bb-cd64e0d9ea92
  Args:
    type: :Person
    source: Alfonso_XII_of_Spain
  AssignClass (d1680b39-f8cb-4ff8-b9d1-5ff253eb228d)
 Call ID: d1680b39-f8cb-4ff8-b9d1-5ff253eb228d
  Args:
    type: :Woman
    source: Maria_Christina_of_Austria
  AssignClass (6fa49de8-fcd3-4b1f-99cf-33ef4909976c)
 Call ID: 6fa49de8-fcd3-4b1f-99cf-33ef4909976c
  Args:
    type: :Person
    source: Maria_Christina_of_Austria
  AddLiteral (3c1d784c-d6a2-4425-8c6f-c902a57cf791)
 Call ID: 3c1d784c-d6a2-4425-8c6f-c902a57cf791
  Args:
    relation: :hasMarriageYear
    literal_value: 1901
    source: Don_Carlos
    literal_type: xsd:integer
  AddTriple (4fb6d2f6-f0ab-4974-af3c-ab498f66930b)
 Call ID: 4fb6d2f6-f0ab-4974-af3c-ab498f66930b
  Args:
    source: Don_Carlos
    relation: :hasRelation
    target: Mercedes_Princess_of_Asturias
  AssignClass (9ce863a1-2542-4083-bf5b-c0604ee7d262)
 Call ID: 9ce863a1-2542-4083-bf5b-c0604ee7d262
  Args:
    type: :Man
    source: Alfonso_XIII_of_Spain
  AssignClass (c975dec6-532b-4a3f-aa72-1c60cdb5cecc)
 Call ID: c975dec6-532b-4a3f-aa72-1c60cdb5cecc
  Args:
    type: :Person
    source: Alfonso_XIII_of_Spain
  AddTriple (2a529a6e-81d1-4de1-8dd3-7f501ec76887)
 Call ID: 2a529a6e-81d1-4de1-8dd3-7f501ec76887
  Args:
    source: Mercedes_Princess_of_Asturias
    target: Alfonso_XIII_of_Spain
    relation: :isSiblingOf
  AssignClass (a10556a5-c9bc-4914-af68-abe9e807938d)
 Call ID: a10556a5-c9bc-4914-af68-abe9e807938d
  Args:
    type: :Woman
    source: Louise_of_Orleans
  AssignClass (714c3355-a5f6-4dd3-bfa4-867f41e9b40f)
 Call ID: 714c3355-a5f6-4dd3-bfa4-867f41e9b40f
  Args:
    type: :Person
    source: Louise_of_Orleans
  AddLiteral (63a2fd28-8bd0-4c84-9bce-067865e9105b)
 Call ID: 63a2fd28-8bd0-4c84-9bce-067865e9105b
  Args:
    relation: :hasMarriageYear
    source: Don_Carlos
    literal_value: 1907
    literal_type: xsd:integer
  AddTriple (efc5dd2a-ed74-4615-9c1f-94323b39e4c7)
 Call ID: efc5dd2a-ed74-4615-9c1f-94323b39e4c7
  Args:
    source: Louise_of_Orleans
    relation: :hasFather
    target: Philippe_Count_of_Paris
  AssignClass (d3e72d06-3b84-4f2f-8a69-63abdb0a8a6e)
 Call ID: d3e72d06-3b84-4f2f-8a69-63abdb0a8a6e
  Args:
    type: :Man
    source: Philippe_Count_of_Paris
  AssignClass (f6da1314-ac78-43fa-84cc-23e583116604)
 Call ID: f6da1314-ac78-43fa-84cc-23e583116604
  Args:
    type: :Person
    source: Philippe_Count_of_Paris
  AssignClass (adc1805e-f5f7-4f7d-a55f-1fd636126776)
 Call ID: adc1805e-f5f7-4f7d-a55f-1fd636126776
  Args:
    type: :Man
    source: Ferdinand
  AssignClass (a03f0499-49d6-40b1-bbf9-7d7408de56da)
 Call ID: a03f0499-49d6-40b1-bbf9-7d7408de56da
  Args:
    type: :Person
    source: Ferdinand
  AddTriple (55bf23eb-bb44-4f7a-a789-6ff33ab24a24)
 Call ID: 55bf23eb-bb44-4f7a-a789-6ff33ab24a24
  Args:
    relation: :isBrotherOf
    target: Don_Carlos
    source: Ferdinand
  AssignClass (1dd85c6b-de07-4e36-9109-2c3cdaa2538b)
 Call ID: 1dd85c6b-de07-4e36-9109-2c3cdaa2538b
  Args:
    type: :Man
    source: Alfonso_son_of_Carlos
  AssignClass (2b72a3e5-2afd-45c0-9e98-acd8381e1271)
 Call ID: 2b72a3e5-2afd-45c0-9e98-acd8381e1271
  Args:
    type: :Person
    source: Alfonso_son_of_Carlos
  AddTriple (b494db48-a71d-496e-90bd-71626b79a4e3)
 Call ID: b494db48-a71d-496e-90bd-71626b79a4e3
  Args:
    target: Don_Carlos
    relation: :isSonOf
    source: Alfonso_son_of_Carlos
  AssignClass (140f4dda-1ba9-45f0-9fa3-16e2a974d7b7)
 Call ID: 140f4dda-1ba9-45f0-9fa3-16e2a974d7b7
  Args:
    type: :Man
    source: Ranieri
  AssignClass (d921cf0f-118f-4f06-9335-7ed14a971743)
 Call ID: d921cf0f-118f-4f06-9335-7ed14a971743
  Args:
    type: :Person
    source: Ranieri
  AddTriple (3af34ab6-8b3a-47d6-a253-cb0500d97792)
 Call ID: 3af34ab6-8b3a-47d6-a253-cb0500d97792
  Args:
    source: Ranieri
    relation: :isBrotherOf
    target: Don_Carlos
  Finish (876863f8-a690-4fe4-8b1d-75975d62638f)
 Call ID: 876863f8-a690-4fe4-8b1d-75975d62638f
  Args: