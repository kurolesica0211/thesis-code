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
  AssignClass (84a1c1ec-1b1c-479c-a566-077cc51f6ea6)
 Call ID: 84a1c1ec-1b1c-479c-a566-077cc51f6ea6
  Args:
    source: Don_Carlos
    type: :Man
  AssignClass (f56bfdd1-afb6-4a02-9960-76e3cee807a1)
 Call ID: f56bfdd1-afb6-4a02-9960-76e3cee807a1
  Args:
    source: Alfonso_Two_Sicilies
    type: :Man
  AssignClass (02a31dc5-f88f-4a36-80b5-20b44e03982d)
 Call ID: 02a31dc5-f88f-4a36-80b5-20b44e03982d
  Args:
    source: Maria_Antonietta
    type: :Woman
  AssignClass (8ad017f7-efe5-4ce6-9ce1-7c00b8f7cc8f)
 Call ID: 8ad017f7-efe5-4ce6-9ce1-7c00b8f7cc8f
  Args:
    source: Francis_II
    type: :Man
  AssignClass (40018c71-4375-4af1-baa0-f47453fe58aa)
 Call ID: 40018c71-4375-4af1-baa0-f47453fe58aa
  Args:
    source: Mercedes_Princess_Asturias
    type: :Woman
  AssignClass (54e76bfe-a825-46ea-8b56-f5c2e3ed645f)
 Call ID: 54e76bfe-a825-46ea-8b56-f5c2e3ed645f
  Args:
    source: Alfonso_XII_Spain
    type: :Man
  AssignClass (b5fdd919-94a3-4893-9c95-6fc13658c98f)
 Call ID: b5fdd919-94a3-4893-9c95-6fc13658c98f
  Args:
    source: Maria_Christina_Austria
    type: :Woman
  AssignClass (d8dce22e-7ec6-4e21-bc6f-5fe1a511a6b6)
 Call ID: d8dce22e-7ec6-4e21-bc6f-5fe1a511a6b6
  Args:
    source: Alfonso_XIII_Spain
    type: :Man
  AssignClass (9461f661-26cd-448e-89ec-543856ebaed2)
 Call ID: 9461f661-26cd-448e-89ec-543856ebaed2
  Args:
    source: Louise_Orleans
    type: :Woman
  AssignClass (4461257b-1473-420b-b7f6-addea81c5c8f)
 Call ID: 4461257b-1473-420b-b7f6-addea81c5c8f
  Args:
    source: Philippe_Count_Paris
    type: :Man
  AssignClass (e097e1a1-f209-4380-a7b9-af1c5f5e1105)
 Call ID: e097e1a1-f209-4380-a7b9-af1c5f5e1105
  Args:
    source: Ferdinand_Two_Sicilies
    type: :Man
  AssignClass (99be4ae6-92a9-4947-a984-3c92ebae593d)
 Call ID: 99be4ae6-92a9-4947-a984-3c92ebae593d
  Args:
    source: Alfonso_son_of_Carlos
    type: :Man
  AssignClass (6debfe1d-7dd6-497f-a770-632e23802fe7)
 Call ID: 6debfe1d-7dd6-497f-a770-632e23802fe7
  Args:
    source: Ranieri_Two_Sicilies
    type: :Man
  AddLiteral (3cf894e7-49e1-4f05-b586-dec85570fe8b)
 Call ID: 3cf894e7-49e1-4f05-b586-dec85570fe8b
  Args:
    literal_value: 1870
    relation: :hasBirthYear
    source: Don_Carlos
    literal_type: xsd:integer
  AddLiteral (a5eba568-ddd4-4705-a3eb-bcbe9c53be6e)
 Call ID: a5eba568-ddd4-4705-a3eb-bcbe9c53be6e
  Args:
    literal_value: 1949
    relation: :hasDeathYear
    source: Don_Carlos
    literal_type: xsd:integer
  AddTriple (9e804fcc-a251-45fa-9547-a1c0e624a57b)
 Call ID: 9e804fcc-a251-45fa-9547-a1c0e624a57b
  Args:
    target: Alfonso_Two_Sicilies
    source: Don_Carlos
    relation: :hasFather
  AddTriple (29375a31-1102-47a2-91f1-90f6a58720bd)
 Call ID: 29375a31-1102-47a2-91f1-90f6a58720bd
  Args:
    relation: :hasMother
    target: Maria_Antonietta
    source: Don_Carlos
  AddTriple (c37a99c0-17ac-49a5-adec-a77077617b35)
 Call ID: c37a99c0-17ac-49a5-adec-a77077617b35
  Args:
    relation: :isBrotherOf
    source: Don_Carlos
    target: Ferdinand_Two_Sicilies
  AddTriple (ca8687e1-0850-41a2-9855-505fd8e5261e)
 Call ID: ca8687e1-0850-41a2-9855-505fd8e5261e
  Args:
    relation: :isBrotherOf
    source: Don_Carlos
    target: Ranieri_Two_Sicilies
  AddTriple (8eaa67e9-3cbf-4312-9d3d-418403e97982)
 Call ID: 8eaa67e9-3cbf-4312-9d3d-418403e97982
  Args:
    relation: :hasFather
    target: Alfonso_XII_Spain
    source: Mercedes_Princess_Asturias
  AddTriple (126e77ad-efa3-4377-9146-5c7572fd80f3)
 Call ID: 126e77ad-efa3-4377-9146-5c7572fd80f3
  Args:
    relation: :hasMother
    source: Mercedes_Princess_Asturias
    target: Maria_Christina_Austria
  AddTriple (a26cccdd-9ff6-4c5e-835b-37884b190ffb)
 Call ID: a26cccdd-9ff6-4c5e-835b-37884b190ffb
  Args:
    relation: :isSisterOf
    source: Mercedes_Princess_Asturias
    target: Alfonso_XIII_Spain
  AddTriple (ff910b0a-4fe1-4689-ac07-584fe8db5ac7)
 Call ID: ff910b0a-4fe1-4689-ac07-584fe8db5ac7
  Args:
    relation: :hasFather
    source: Louise_Orleans
    target: Philippe_Count_Paris
  AddTriple (1989e305-75d5-4ac2-a8c6-2d5e781a2d0b)
 Call ID: 1989e305-75d5-4ac2-a8c6-2d5e781a2d0b
  Args:
    source: Alfonso_son_of_Carlos
    target: Don_Carlos
    relation: :hasFather
  AddLiteral (c1d5c19f-a9ad-4ca1-9197-70b3b41125ed)
 Call ID: c1d5c19f-a9ad-4ca1-9197-70b3b41125ed
  Args:
    source: Don_Carlos
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 1901
  AddTriple (dc6de670-c51d-4d97-a5fd-136fe1d94cea)
 Call ID: dc6de670-c51d-4d97-a5fd-136fe1d94cea
  Args:
    target: Mercedes_Princess_Asturias
    source: Don_Carlos
    relation: :hasRelation
  AddLiteral (5eff8cad-c389-477d-a4cb-13109bad59ee)
 Call ID: 5eff8cad-c389-477d-a4cb-13109bad59ee
  Args:
    literal_type: xsd:integer
    source: Don_Carlos
    literal_value: 1907
    relation: :hasMarriageYear
  AddTriple (d0ef5e8c-28a9-4282-b9ce-6a5363abaf1b)
 Call ID: d0ef5e8c-28a9-4282-b9ce-6a5363abaf1b
  Args:
    relation: :hasRelation
    source: Don_Carlos
    target: Louise_Orleans
  Finish (8b1d97eb-1ae3-4623-86e5-29ca868d7c10)
 Call ID: 8b1d97eb-1ae3-4623-86e5-29ca868d7c10
  Args: