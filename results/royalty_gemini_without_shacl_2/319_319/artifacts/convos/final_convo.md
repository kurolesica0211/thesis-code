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
  AssignClass (749d04df-f509-4339-aaad-3de083881c6d)
 Call ID: 749d04df-f509-4339-aaad-3de083881c6d
  Args:
    type: :Man
    source: Don_Carlos
  AssignClass (95a623ef-b0de-4311-9510-485503a07dd1)
 Call ID: 95a623ef-b0de-4311-9510-485503a07dd1
  Args:
    source: Don_Carlos
    type: :Person
  AddLiteral (214429c0-35ed-4716-8c43-342cc1301090)
 Call ID: 214429c0-35ed-4716-8c43-342cc1301090
  Args:
    literal_value: 1870
    source: Don_Carlos
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (09d0fc50-1eb9-464c-a98a-37aff332cc90)
 Call ID: 09d0fc50-1eb9-464c-a98a-37aff332cc90
  Args:
    source: Don_Carlos
    literal_value: 1949
    relation: :hasDeathYear
    literal_type: xsd:integer
  AssignClass (c29e8d6d-f645-4c1a-b4c5-b44f906b96da)
 Call ID: c29e8d6d-f645-4c1a-b4c5-b44f906b96da
  Args:
    source: Alfonso_Two_Sicilies
    type: :Man
  AssignClass (a113cf87-398b-4be6-878e-70b72c2f53f9)
 Call ID: a113cf87-398b-4be6-878e-70b72c2f53f9
  Args:
    source: Alfonso_Two_Sicilies
    type: :Person
  AssignClass (59cff762-b30f-439d-94a0-e768c514d432)
 Call ID: 59cff762-b30f-439d-94a0-e768c514d432
  Args:
    source: Maria_Antonietta
    type: :Woman
  AssignClass (98a6ea6c-536d-4607-8742-3600df9f1a1b)
 Call ID: 98a6ea6c-536d-4607-8742-3600df9f1a1b
  Args:
    source: Maria_Antonietta
    type: :Person
  AddTriple (62b30362-b2f5-4ad1-9226-3ead60b34b34)
 Call ID: 62b30362-b2f5-4ad1-9226-3ead60b34b34
  Args:
    relation: :hasFather
    target: Alfonso_Two_Sicilies
    source: Don_Carlos
  AddTriple (739d0090-c4ad-44fa-b84c-f61931483df1)
 Call ID: 739d0090-c4ad-44fa-b84c-f61931483df1
  Args:
    target: Maria_Antonietta
    source: Don_Carlos
    relation: :hasMother
  AssignClass (26aacd3c-361b-4e9f-964a-a1f71118b6f4)
 Call ID: 26aacd3c-361b-4e9f-964a-a1f71118b6f4
  Args:
    source: Francis_II
    type: :Man
  AssignClass (01d4b468-5757-4989-bfc2-5b5c82063827)
 Call ID: 01d4b468-5757-4989-bfc2-5b5c82063827
  Args:
    source: Francis_II
    type: :Person
  AssignClass (33695d1c-3e9c-443b-aea3-314ce0712ac0)
 Call ID: 33695d1c-3e9c-443b-aea3-314ce0712ac0
  Args:
    type: :Woman
    source: Mercedes_Princess_Asturias
  AssignClass (12088feb-f295-4dbc-964b-68e0b1fc80a3)
 Call ID: 12088feb-f295-4dbc-964b-68e0b1fc80a3
  Args:
    source: Mercedes_Princess_Asturias
    type: :Person
  AssignClass (c94dc302-a887-49fc-b508-198b886bc0f5)
 Call ID: c94dc302-a887-49fc-b508-198b886bc0f5
  Args:
    source: Alfonso_XII
    type: :Man
  AssignClass (549b7c70-f9a0-4e60-aed0-9e14e70d494e)
 Call ID: 549b7c70-f9a0-4e60-aed0-9e14e70d494e
  Args:
    source: Alfonso_XII
    type: :Person
  AssignClass (828e1ede-36c3-4ba6-91d8-73ead4593cb7)
 Call ID: 828e1ede-36c3-4ba6-91d8-73ead4593cb7
  Args:
    source: Maria_Christina_Austria
    type: :Woman
  AssignClass (fd2b85f2-955e-452c-a7f3-aa942b1cc071)
 Call ID: fd2b85f2-955e-452c-a7f3-aa942b1cc071
  Args:
    type: :Person
    source: Maria_Christina_Austria
  AddTriple (0c5b8b87-7e89-48af-814a-93971ff46a9a)
 Call ID: 0c5b8b87-7e89-48af-814a-93971ff46a9a
  Args:
    relation: :hasFather
    source: Mercedes_Princess_Asturias
    target: Alfonso_XII
  AddTriple (2178b598-545d-400e-aa79-d3777e7d421b)
 Call ID: 2178b598-545d-400e-aa79-d3777e7d421b
  Args:
    relation: :hasMother
    target: Maria_Christina_Austria
    source: Mercedes_Princess_Asturias
  AddLiteral (6f223fd2-0445-4ed8-89e7-92b35e9ea75c)
 Call ID: 6f223fd2-0445-4ed8-89e7-92b35e9ea75c
  Args:
    literal_value: 1901
    source: Don_Carlos
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AssignClass (721c4a01-c095-4d8c-8093-337cd095e101)
 Call ID: 721c4a01-c095-4d8c-8093-337cd095e101
  Args:
    source: Louise_Orleans
    type: :Woman
  AssignClass (0f22f8d4-3731-4fcc-bc58-dd497a640b5a)
 Call ID: 0f22f8d4-3731-4fcc-bc58-dd497a640b5a
  Args:
    source: Louise_Orleans
    type: :Person
  AssignClass (46e8e374-6a6d-4eab-9adb-7f0641944c28)
 Call ID: 46e8e374-6a6d-4eab-9adb-7f0641944c28
  Args:
    source: Philippe_Orleans
    type: :Man
  AssignClass (780db234-4715-4cd8-9e69-3eff8131dd18)
 Call ID: 780db234-4715-4cd8-9e69-3eff8131dd18
  Args:
    source: Philippe_Orleans
    type: :Person
  AddTriple (2e011699-d88c-439c-a91b-4b70dcacb720)
 Call ID: 2e011699-d88c-439c-a91b-4b70dcacb720
  Args:
    source: Louise_Orleans
    target: Philippe_Orleans
    relation: :hasFather
  AddLiteral (b6701855-e090-40b7-8bb1-99fd140b5010)
 Call ID: b6701855-e090-40b7-8bb1-99fd140b5010
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 1907
    source: Don_Carlos
  AssignClass (00c220b0-932a-4411-a514-57d2d4445ec3)
 Call ID: 00c220b0-932a-4411-a514-57d2d4445ec3
  Args:
    source: Alfonso_XIII
    type: :Man
  AssignClass (786ebef8-bbe1-4c16-bf66-65f1a598c259)
 Call ID: 786ebef8-bbe1-4c16-bf66-65f1a598c259
  Args:
    source: Alfonso_XIII
    type: :Person
  AssignClass (152a22f3-0a10-4c76-ac69-86af2b765811)
 Call ID: 152a22f3-0a10-4c76-ac69-86af2b765811
  Args:
    type: :Man
    source: Ferdinand_Two_Sicilies
  AssignClass (dc2964fc-0399-4da6-ab14-604e69fd7a79)
 Call ID: dc2964fc-0399-4da6-ab14-604e69fd7a79
  Args:
    source: Ferdinand_Two_Sicilies
    type: :Person
  AddTriple (3eee9e6d-6580-447c-8318-1668e7629c8d)
 Call ID: 3eee9e6d-6580-447c-8318-1668e7629c8d
  Args:
    target: Ferdinand_Two_Sicilies
    source: Don_Carlos
    relation: :isBrotherOf
  AssignClass (1fd281e8-05c5-4177-84ee-7d5af9cc057b)
 Call ID: 1fd281e8-05c5-4177-84ee-7d5af9cc057b
  Args:
    type: :Man
    source: Ranieri_Two_Sicilies
  AssignClass (6bf36eef-6fb6-4473-95e8-7ae11e72e2a6)
 Call ID: 6bf36eef-6fb6-4473-95e8-7ae11e72e2a6
  Args:
    source: Ranieri_Two_Sicilies
    type: :Person
  AddTriple (086bcde6-c08d-4ce5-9674-541e89ac0f35)
 Call ID: 086bcde6-c08d-4ce5-9674-541e89ac0f35
  Args:
    relation: :isBrotherOf
    source: Don_Carlos
    target: Ranieri_Two_Sicilies
  AssignClass (2b6fb534-618a-4b86-a26b-12af5e69bcf2)
 Call ID: 2b6fb534-618a-4b86-a26b-12af5e69bcf2
  Args:
    source: Alfonso_Son_of_Carlos
    type: :Man
  AssignClass (c07255dd-e514-4bd3-9ea8-be84d42d3ff4)
 Call ID: c07255dd-e514-4bd3-9ea8-be84d42d3ff4
  Args:
    type: :Person
    source: Alfonso_Son_of_Carlos
  AddTriple (2279edc0-d358-4ea7-9ff2-1a07fed9fd29)
 Call ID: 2279edc0-d358-4ea7-9ff2-1a07fed9fd29
  Args:
    relation: :hasFather
    source: Alfonso_Son_of_Carlos
    target: Don_Carlos
  Finish (3bf6de99-e45d-496c-b5fd-a38521a82438)
 Call ID: 3bf6de99-e45d-496c-b5fd-a38521a82438
  Args: