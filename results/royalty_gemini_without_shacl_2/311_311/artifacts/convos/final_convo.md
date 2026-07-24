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
  AssignClass (7184b2f8-7965-4e97-b4d0-db1cad8173a7)
 Call ID: 7184b2f8-7965-4e97-b4d0-db1cad8173a7
  Args:
    source: Don_Carlos
    type: :Man
  AssignClass (2b656d45-bafa-4891-b1ec-334b6eaa64b8)
 Call ID: 2b656d45-bafa-4891-b1ec-334b6eaa64b8
  Args:
    source: Don_Carlos
    type: :Person
  AddLiteral (763c9203-9d81-4f05-b30f-9af1deacb8b0)
 Call ID: 763c9203-9d81-4f05-b30f-9af1deacb8b0
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Don_Carlos
    literal_value: 1870
  AddLiteral (bf8757ab-ad91-4ea4-83f4-0d112a8d1e3b)
 Call ID: bf8757ab-ad91-4ea4-83f4-0d112a8d1e3b
  Args:
    literal_type: xsd:integer
    literal_value: 1949
    source: Don_Carlos
    relation: :hasDeathYear
  AssignClass (47ef215c-5dce-4819-8335-6fbf6b5371f9)
 Call ID: 47ef215c-5dce-4819-8335-6fbf6b5371f9
  Args:
    type: :Man
    source: Alfonso_of_the_Two_Sicilies
  AssignClass (b91754b2-1850-4f96-adab-30e643e5ff01)
 Call ID: b91754b2-1850-4f96-adab-30e643e5ff01
  Args:
    type: :Person
    source: Alfonso_of_the_Two_Sicilies
  AssignClass (133c082c-1fd1-47c2-9760-456e45ee904f)
 Call ID: 133c082c-1fd1-47c2-9760-456e45ee904f
  Args:
    type: :Woman
    source: Maria_Antonietta_of_Bourbon-Two_Sicilies
  AssignClass (d65813cc-043e-4f0f-826b-6851a69c64d0)
 Call ID: d65813cc-043e-4f0f-826b-6851a69c64d0
  Args:
    source: Maria_Antonietta_of_Bourbon-Two_Sicilies
    type: :Person
  AddTriple (cf4abb1e-ee78-454a-98c7-edb5374909a2)
 Call ID: cf4abb1e-ee78-454a-98c7-edb5374909a2
  Args:
    relation: :hasFather
    source: Don_Carlos
    target: Alfonso_of_the_Two_Sicilies
  AddTriple (5c168b3b-4147-4c22-8a4f-7ab3ab456c42)
 Call ID: 5c168b3b-4147-4c22-8a4f-7ab3ab456c42
  Args:
    target: Maria_Antonietta_of_Bourbon-Two_Sicilies
    relation: :hasMother
    source: Don_Carlos
  AssignClass (8059fbf1-02a4-41c7-a075-f7073e10bc5f)
 Call ID: 8059fbf1-02a4-41c7-a075-f7073e10bc5f
  Args:
    type: :Man
    source: Francis_II_of_the_Two_Sicilies
  AssignClass (fdde1c1e-fbd6-42f8-85e7-04458d168a9a)
 Call ID: fdde1c1e-fbd6-42f8-85e7-04458d168a9a
  Args:
    source: Francis_II_of_the_Two_Sicilies
    type: :Person
  AddTriple (7d9fc26d-3ede-42b1-89b0-1479cb8083bf)
 Call ID: 7d9fc26d-3ede-42b1-89b0-1479cb8083bf
  Args:
    source: Francis_II_of_the_Two_Sicilies
    relation: :isUncleOf
    target: Don_Carlos
  AssignClass (5c81b7c4-9fc7-462f-8876-02594b025f4d)
 Call ID: 5c81b7c4-9fc7-462f-8876-02594b025f4d
  Args:
    type: :Woman
    source: Mercedes_Princess_of_Asturias
  AssignClass (b49d3540-daf3-49db-85a3-ea0bc5e78cfc)
 Call ID: b49d3540-daf3-49db-85a3-ea0bc5e78cfc
  Args:
    source: Mercedes_Princess_of_Asturias
    type: :Person
  AddTriple (e246bb8b-e8f1-4f48-a491-55fd5413a38c)
 Call ID: e246bb8b-e8f1-4f48-a491-55fd5413a38c
  Args:
    relation: :hasRelation
    source: Don_Carlos
    target: Mercedes_Princess_of_Asturias
  AddLiteral (c662ca9e-30a7-403f-8970-6af710f8532b)
 Call ID: c662ca9e-30a7-403f-8970-6af710f8532b
  Args:
    literal_type: xsd:integer
    literal_value: 1901
    relation: :hasMarriageYear
    source: Don_Carlos
  AssignClass (d0d279f6-73b0-4a97-a66f-5fdf9d679f4a)
 Call ID: d0d279f6-73b0-4a97-a66f-5fdf9d679f4a
  Args:
    source: Alfonso_XII_of_Spain
    type: :Man
  AssignClass (33d76644-d084-44f4-8cc9-e71dda9bf518)
 Call ID: 33d76644-d084-44f4-8cc9-e71dda9bf518
  Args:
    type: :Person
    source: Alfonso_XII_of_Spain
  AssignClass (b2707b3e-de7f-4dce-889a-e7bfbfd9a84c)
 Call ID: b2707b3e-de7f-4dce-889a-e7bfbfd9a84c
  Args:
    type: :Woman
    source: Maria_Christina_of_Austria
  AssignClass (71592f62-b28b-46a3-901f-0656d9b7edd3)
 Call ID: 71592f62-b28b-46a3-901f-0656d9b7edd3
  Args:
    type: :Person
    source: Maria_Christina_of_Austria
  AddTriple (59903a4a-a9c1-4f43-acae-f3ebfae59b5c)
 Call ID: 59903a4a-a9c1-4f43-acae-f3ebfae59b5c
  Args:
    target: Alfonso_XII_of_Spain
    relation: :hasFather
    source: Mercedes_Princess_of_Asturias
  AddTriple (ef1348ea-1c5f-4fb9-a418-6c86fdd0730e)
 Call ID: ef1348ea-1c5f-4fb9-a418-6c86fdd0730e
  Args:
    target: Maria_Christina_of_Austria
    relation: :hasMother
    source: Mercedes_Princess_of_Asturias
  AssignClass (fe5693f9-e85b-4629-bb9e-d7b4a3134843)
 Call ID: fe5693f9-e85b-4629-bb9e-d7b4a3134843
  Args:
    type: :Man
    source: Alfonso_XIII_of_Spain
  AssignClass (bb854e17-9a50-4668-aff9-b3b3b10bd342)
 Call ID: bb854e17-9a50-4668-aff9-b3b3b10bd342
  Args:
    type: :Person
    source: Alfonso_XIII_of_Spain
  AddTriple (55d7dc52-2309-40ee-850e-38623778ebdf)
 Call ID: 55d7dc52-2309-40ee-850e-38623778ebdf
  Args:
    relation: :isSisterOf
    source: Mercedes_Princess_of_Asturias
    target: Alfonso_XIII_of_Spain
  AssignClass (53b0d2dd-aa37-4983-a7eb-dd7ec40b811b)
 Call ID: 53b0d2dd-aa37-4983-a7eb-dd7ec40b811b
  Args:
    type: :Woman
    source: Louise_of_Orleans
  AssignClass (0ea816ea-1b1d-48ef-8d36-d2411a8a5daa)
 Call ID: 0ea816ea-1b1d-48ef-8d36-d2411a8a5daa
  Args:
    type: :Person
    source: Louise_of_Orleans
  AddTriple (1118e48d-b3d6-4e18-beb5-d848e694aacd)
 Call ID: 1118e48d-b3d6-4e18-beb5-d848e694aacd
  Args:
    relation: :hasRelation
    source: Don_Carlos
    target: Louise_of_Orleans
  AddLiteral (eba2007a-7ce2-4ee2-b7b8-186574313d7d)
 Call ID: eba2007a-7ce2-4ee2-b7b8-186574313d7d
  Args:
    source: Don_Carlos
    relation: :hasMarriageYear
    literal_value: 1907
    literal_type: xsd:integer
  AssignClass (eb3e3da7-da64-4934-bf4a-e5cb858e63e4)
 Call ID: eb3e3da7-da64-4934-bf4a-e5cb858e63e4
  Args:
    source: Philippe_Count_of_Paris
    type: :Man
  AssignClass (021edc9e-a5ef-424a-9e3b-73057a4b00e7)
 Call ID: 021edc9e-a5ef-424a-9e3b-73057a4b00e7
  Args:
    source: Philippe_Count_of_Paris
    type: :Person
  AddTriple (2873bbbc-0045-4a21-a44e-3f4be57a0094)
 Call ID: 2873bbbc-0045-4a21-a44e-3f4be57a0094
  Args:
    target: Philippe_Count_of_Paris
    source: Louise_of_Orleans
    relation: :hasFather
  AssignClass (7f35f628-3c7c-48ce-b486-5470518ca22e)
 Call ID: 7f35f628-3c7c-48ce-b486-5470518ca22e
  Args:
    source: Ferdinand_of_the_Two_Sicilies
    type: :Man
  AssignClass (59a7bb50-088c-499c-acf0-cf04a2bf60e2)
 Call ID: 59a7bb50-088c-499c-acf0-cf04a2bf60e2
  Args:
    type: :Person
    source: Ferdinand_of_the_Two_Sicilies
  AddTriple (9e15baba-3f7a-4870-9561-7639a9192415)
 Call ID: 9e15baba-3f7a-4870-9561-7639a9192415
  Args:
    source: Don_Carlos
    relation: :hasBrother
    target: Ferdinand_of_the_Two_Sicilies
  AssignClass (f6e38825-8b85-43ef-8a7c-a16e75bdf1f8)
 Call ID: f6e38825-8b85-43ef-8a7c-a16e75bdf1f8
  Args:
    source: Alfonso_son_of_Carlos
    type: :Man
  AssignClass (239dbb3a-732d-4783-8778-0556891cf2b9)
 Call ID: 239dbb3a-732d-4783-8778-0556891cf2b9
  Args:
    type: :Person
    source: Alfonso_son_of_Carlos
  AddTriple (4c7d7e21-c1da-4170-8ed7-fad4aa181536)
 Call ID: 4c7d7e21-c1da-4170-8ed7-fad4aa181536
  Args:
    relation: :hasFather
    source: Alfonso_son_of_Carlos
    target: Don_Carlos
  AssignClass (5c7a399b-188f-4665-a690-99cc6f0b3798)
 Call ID: 5c7a399b-188f-4665-a690-99cc6f0b3798
  Args:
    type: :Man
    source: Ranieri_of_the_Two_Sicilies
  AssignClass (a802a013-2101-461c-b86c-61779d56bac9)
 Call ID: a802a013-2101-461c-b86c-61779d56bac9
  Args:
    source: Ranieri_of_the_Two_Sicilies
    type: :Person
  AddTriple (59846b2a-1a22-4a24-82ac-9decb2696d06)
 Call ID: 59846b2a-1a22-4a24-82ac-9decb2696d06
  Args:
    target: Ranieri_of_the_Two_Sicilies
    relation: :hasBrother
    source: Don_Carlos
  Finish (5e8cebcd-13e4-41e1-8a6d-38db7ed9f2a5)
 Call ID: 5e8cebcd-13e4-41e1-8a6d-38db7ed9f2a5
  Args: