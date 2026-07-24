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
  AssignClass (f2c07116-54f1-4417-a808-aa46aa67cc63)
 Call ID: f2c07116-54f1-4417-a808-aa46aa67cc63
  Args:
    type: :Man
    source: Don_Carlos
  AssignClass (90cb5a4c-137d-456c-9a5b-97edd36002a8)
 Call ID: 90cb5a4c-137d-456c-9a5b-97edd36002a8
  Args:
    source: Don_Carlos
    type: :Person
  AddLiteral (5c55e8c2-b1be-4738-ac4b-b054d8daf0c2)
 Call ID: 5c55e8c2-b1be-4738-ac4b-b054d8daf0c2
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1870
    source: Don_Carlos
  AddLiteral (2247c1e3-e443-4f99-8c3b-db937921ed3a)
 Call ID: 2247c1e3-e443-4f99-8c3b-db937921ed3a
  Args:
    source: Don_Carlos
    literal_value: 1949
    relation: :hasDeathYear
    literal_type: xsd:integer
  AssignClass (774d6458-0811-45de-acf8-08e69db8cde2)
 Call ID: 774d6458-0811-45de-acf8-08e69db8cde2
  Args:
    type: :Man
    source: Prince_Alfonso_of_the_Two_Sicilies
  AssignClass (b9f2307d-1c8b-4fff-b0f5-22fce7a5a95b)
 Call ID: b9f2307d-1c8b-4fff-b0f5-22fce7a5a95b
  Args:
    source: Prince_Alfonso_of_the_Two_Sicilies
    type: :Person
  AssignClass (3c0fe87a-4d1b-41aa-a1e3-56ed6ef5ea5c)
 Call ID: 3c0fe87a-4d1b-41aa-a1e3-56ed6ef5ea5c
  Args:
    type: :Woman
    source: Princess_Maria_Antonietta_of_Bourbon-Two_Sicilies
  AssignClass (f99d6692-29bf-45a1-a3df-8ab794242a15)
 Call ID: f99d6692-29bf-45a1-a3df-8ab794242a15
  Args:
    source: Princess_Maria_Antonietta_of_Bourbon-Two_Sicilies
    type: :Person
  AddTriple (bbac3c2f-6979-4423-ac24-6c81efff31df)
 Call ID: bbac3c2f-6979-4423-ac24-6c81efff31df
  Args:
    relation: :hasFather
    target: Prince_Alfonso_of_the_Two_Sicilies
    source: Don_Carlos
  AddTriple (fa610656-2b61-4764-922c-298b41ca8f35)
 Call ID: fa610656-2b61-4764-922c-298b41ca8f35
  Args:
    relation: :hasMother
    target: Princess_Maria_Antonietta_of_Bourbon-Two_Sicilies
    source: Don_Carlos
  AssignClass (efeb3d0b-e735-4ff2-a05e-d84ff9b44e29)
 Call ID: efeb3d0b-e735-4ff2-a05e-d84ff9b44e29
  Args:
    type: :Man
    source: Francis_II
  AssignClass (878e9def-3095-46f7-9ef5-307a53af4fd1)
 Call ID: 878e9def-3095-46f7-9ef5-307a53af4fd1
  Args:
    source: Francis_II
    type: :Person
  AssignClass (3972709c-1584-4fde-be29-bf8df3c5acba)
 Call ID: 3972709c-1584-4fde-be29-bf8df3c5acba
  Args:
    source: Mercedes_Princess_of_Asturias
    type: :Woman
  AssignClass (b6e1a3f3-fa05-48b5-a834-aab8967ec07e)
 Call ID: b6e1a3f3-fa05-48b5-a834-aab8967ec07e
  Args:
    type: :Person
    source: Mercedes_Princess_of_Asturias
  AssignClass (9eadc798-5d90-43b3-a587-f11fe8951cd7)
 Call ID: 9eadc798-5d90-43b3-a587-f11fe8951cd7
  Args:
    type: :Man
    source: King_Alfonso_XII_of_Spain
  AssignClass (20677cc9-f324-4e12-a0f3-5c3ac3aa593a)
 Call ID: 20677cc9-f324-4e12-a0f3-5c3ac3aa593a
  Args:
    type: :Person
    source: King_Alfonso_XII_of_Spain
  AssignClass (c9256203-5522-4e3a-87d9-953b7a04ef8f)
 Call ID: c9256203-5522-4e3a-87d9-953b7a04ef8f
  Args:
    source: Archduchess_Maria_Christina_of_Austria
    type: :Woman
  AssignClass (32910424-0a5a-4fc4-8ec1-681024389252)
 Call ID: 32910424-0a5a-4fc4-8ec1-681024389252
  Args:
    type: :Person
    source: Archduchess_Maria_Christina_of_Austria
  AddTriple (306e8b2e-b688-4587-97b4-bd792ff79573)
 Call ID: 306e8b2e-b688-4587-97b4-bd792ff79573
  Args:
    source: Mercedes_Princess_of_Asturias
    target: King_Alfonso_XII_of_Spain
    relation: :hasFather
  AddTriple (2ad782bf-6d13-413f-a5dc-61da5093ba55)
 Call ID: 2ad782bf-6d13-413f-a5dc-61da5093ba55
  Args:
    target: Archduchess_Maria_Christina_of_Austria
    relation: :hasMother
    source: Mercedes_Princess_of_Asturias
  AddTriple (f04e166a-141f-4074-83a6-3066c70e5a80)
 Call ID: f04e166a-141f-4074-83a6-3066c70e5a80
  Args:
    relation: :hasRelation
    target: Mercedes_Princess_of_Asturias
    source: Don_Carlos
  AddLiteral (04d55e30-0e6e-4f01-a093-74967e7a5652)
 Call ID: 04d55e30-0e6e-4f01-a093-74967e7a5652
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 1901
    source: Don_Carlos
  AssignClass (cbe932c2-eaaa-467e-abff-6774b9c3af38)
 Call ID: cbe932c2-eaaa-467e-abff-6774b9c3af38
  Args:
    type: :Man
    source: King_Alfonso_XIII_of_Spain
  AssignClass (6829bd66-d860-40d5-a7c6-1f0ae8a1e3b3)
 Call ID: 6829bd66-d860-40d5-a7c6-1f0ae8a1e3b3
  Args:
    source: King_Alfonso_XIII_of_Spain
    type: :Person
  AddTriple (c891f2f1-7c27-481d-b321-414b4f5e0077)
 Call ID: c891f2f1-7c27-481d-b321-414b4f5e0077
  Args:
    relation: :isSiblingOf
    target: King_Alfonso_XIII_of_Spain
    source: Mercedes_Princess_of_Asturias
  AssignClass (ef9dc7a6-c0a2-44f8-9cb7-1733ca00a7fc)
 Call ID: ef9dc7a6-c0a2-44f8-9cb7-1733ca00a7fc
  Args:
    source: Princess_Louise_of_Orleans
    type: :Woman
  AssignClass (9619c49c-8f60-4aed-9e9a-35e4eb3416c9)
 Call ID: 9619c49c-8f60-4aed-9e9a-35e4eb3416c9
  Args:
    source: Princess_Louise_of_Orleans
    type: :Person
  AssignClass (7d30150d-cc98-4e2d-8be3-6c5a1b056b5b)
 Call ID: 7d30150d-cc98-4e2d-8be3-6c5a1b056b5b
  Args:
    source: Prince_Philippe_Count_of_Paris
    type: :Man
  AssignClass (cb8ae6cd-4167-4896-95ff-c04a0f97f125)
 Call ID: cb8ae6cd-4167-4896-95ff-c04a0f97f125
  Args:
    source: Prince_Philippe_Count_of_Paris
    type: :Person
  AddTriple (de5ab1d2-608e-400e-9a18-37cbeec32f7c)
 Call ID: de5ab1d2-608e-400e-9a18-37cbeec32f7c
  Args:
    target: Prince_Philippe_Count_of_Paris
    relation: :hasFather
    source: Princess_Louise_of_Orleans
  AddTriple (ea4e8f0f-0e04-41ac-be99-a4741437d682)
 Call ID: ea4e8f0f-0e04-41ac-be99-a4741437d682
  Args:
    source: Don_Carlos
    target: Princess_Louise_of_Orleans
    relation: :hasRelation
  AddLiteral (e4896272-6290-4602-960b-e8e739ff68c4)
 Call ID: e4896272-6290-4602-960b-e8e739ff68c4
  Args:
    literal_value: 1907
    source: Don_Carlos
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AssignClass (eb5bd482-1e50-4e45-8dd9-cb966c417879)
 Call ID: eb5bd482-1e50-4e45-8dd9-cb966c417879
  Args:
    source: Ferdinand
    type: :Man
  AssignClass (23a0f9f0-99a4-48f7-8971-17f339b2e9b8)
 Call ID: 23a0f9f0-99a4-48f7-8971-17f339b2e9b8
  Args:
    type: :Person
    source: Ferdinand
  AddTriple (9e217c61-f371-4797-b128-b588cc5008fe)
 Call ID: 9e217c61-f371-4797-b128-b588cc5008fe
  Args:
    relation: :isSiblingOf
    target: Ferdinand
    source: Don_Carlos
  AssignClass (cd15d18e-862c-4a04-ae05-645ea5642dd7)
 Call ID: cd15d18e-862c-4a04-ae05-645ea5642dd7
  Args:
    type: :Man
    source: Alfonso_son_of_Carlos
  AssignClass (228baecf-7d14-485d-baab-4f5a0fe3ab5f)
 Call ID: 228baecf-7d14-485d-baab-4f5a0fe3ab5f
  Args:
    type: :Person
    source: Alfonso_son_of_Carlos
  AddTriple (d93420b5-f9ff-46f6-8b6c-e52f1d749ad5)
 Call ID: d93420b5-f9ff-46f6-8b6c-e52f1d749ad5
  Args:
    relation: :isSonOf
    target: Don_Carlos
    source: Alfonso_son_of_Carlos
  AssignClass (c83ba830-6a70-4b85-88ce-37f8e1def3ad)
 Call ID: c83ba830-6a70-4b85-88ce-37f8e1def3ad
  Args:
    source: Ranieri
    type: :Man
  AssignClass (7d4109f0-06ca-4c80-aeca-37277e2c3a0f)
 Call ID: 7d4109f0-06ca-4c80-aeca-37277e2c3a0f
  Args:
    source: Ranieri
    type: :Person
  AddTriple (1535676e-72de-48b2-8dc5-acada85adfe8)
 Call ID: 1535676e-72de-48b2-8dc5-acada85adfe8
  Args:
    target: Ranieri
    relation: :isSiblingOf
    source: Don_Carlos
  Finish (8e9e7b9a-ee02-4bed-b5af-c3ae71a5174a)
 Call ID: 8e9e7b9a-ee02-4bed-b5af-c3ae71a5174a
  Args: