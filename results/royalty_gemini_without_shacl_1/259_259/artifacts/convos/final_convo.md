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
The Duke of CalabriaThe Duchess of Calabria


Prince Pedro of Bourbon-Two Sicilies, Duke of Calabria, Grandee of Spain (Spanish: Pedro Juan María Alejo Saturnino de Todos los Santos; born 16 October 1968), is the only son of Infante Carlos, Duke of Calabria, and Princess Anne of Orléans.
Claim

He is the only son of Infante Carlos, Duke of Calabria (1938–2015), and his wife, Princess Anne of Orléans.
The other claimant is Prince Carlo, Duke of Castro.
He is also a grandee of Spain, as the son of an infante of Spain.
On 14 December 1900, Prince Carlos, next oldest brother to the childless Prince Ferdinand, head of the House of Bourbon-Two Sicilies and immediate heir of their father, claimant to the former throne of the Two Sicilies, signed a private agreement purporting to renounce the "future succession" to the former crown before his marriage to María de las Mercedes, Princess of Asturias, heiress presumptive to the throne of Spain.
This document, known as the Act of Cannes, was signed in purported obedience to the 1759 Pragmatic Sanction signed by Charles III of Spain where it was established that the thrones of Spain and Naples should never be united in the person of the same monarch, separating them forever to preserve the European balance of power.
The Act of Cannes states:


Before Us, Don Alfonso de Borbón, Count of Caserta... Head of the Royal House and Dynasty of the Two Sicilies...
His Royal Highness Prince Don Carlos, our beloved Son, appears and declares that, preparing to marry HRH Infanta María de las Mercedes, Princess of Asturias, and assuming by such marriage the nationality and quality of Spanish Prince, undertakes to renounce by this Act and solemnly renounces, for himself and for his heirs and successors, all the right and reason to the eventual succession to the Crown of the Two Sicilies and to all the assets of the Royal House that are in Italy and elsewhere, and this according to our Laws, constitutions and Family customs, in execution of the Pragmatic Sanction of King Charles III, our Augustus ancestor, of October 6, 1759, the prescriptions of which he freely and spontaneously declares to subscribe and obey.
He also declares, in particular, to renounce for himself, his heirs and successors to the assets and values existing in Italy, Vienna and Munich and destined by His Majesty King Francis II (may God have welcomed his soul), to the foundation of a majorat for the Head of the Dynasty and of the Family of the Two Sicilies and for the constitution of an endowment fund in favor of the Royal Princesses and granddaughters of our August Father King Ferdinand (may God have welcomed his soul), of marriageable age; but preserving his rights to the part of the assets that were bequeathed to him by his late uncle King Francis II, in the event that the Italian Government, which improperly retains them, makes the due restitution and the same everything that may arrive to him by other testamentary legacies.
— Cannes, 14 December 1900

Supporters of the other claimant to the headship of the House of Bourbon-Two Sicilies, sometimes referred to as the Castrist faction, argue that because Prince Carlos signed this agreement, he relinquished all of his rights and those of his descendants to both the headship of the family and the Sacred Military Constantinian Order of Saint George, and so the rights currently fall on Prince Carlo, Duke of Castro.
However, supporters of Pedro, also known as the legitimists, argue that the Act of Cannes was subject to a condition that never arose and its terms would have only applied if the wife of Prince Carlos had inherited the throne of Spain, and he had become king of the Two Sicilies, which never happened and was furthermore highly unlikely at the time the document was created.
In due course, Prince Carlos inherited his share of properties of the royal family in Italy, despite the purported renunciation, with no objection by his brothers and sisters.
Marriage and issue

Pedro married Sofía Landaluce y Melgarejo (born 23
November 1973 in Madrid), daughter of José Manuel Landaluce y Domínguez and his wife María de las Nieves Blanca Melgarejo y González (granddaughter of the Dukes of San Fernando de Quiroga), on 30 March 2001 at Real Club de la Puerta de Hierro in Madrid.
Pedro and Sofía have seven children:


Honours

Dynastic




National

Other activities

Arms

Ancestors

Notes

References

Bibliography

External links



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
  AssignClass (e03b5b42-42f2-4725-ae62-8b8ef5b5fd9c)
 Call ID: e03b5b42-42f2-4725-ae62-8b8ef5b5fd9c
  Args:
    type: :Man
    source: :Prince_Pedro_of_Bourbon-Two_Sicilies
  AssignClass (efd4ff60-beb5-4a67-82ac-5fa5df1e1d79)
 Call ID: efd4ff60-beb5-4a67-82ac-5fa5df1e1d79
  Args:
    type: :Person
    source: :Prince_Pedro_of_Bourbon-Two_Sicilies
  AddLiteral (da177318-9488-4f32-8238-b4229ab877a1)
 Call ID: da177318-9488-4f32-8238-b4229ab877a1
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: :Prince_Pedro_of_Bourbon-Two_Sicilies
    literal_value: 1968
  AssignClass (5e90139d-43e5-4e91-8daf-3ed8c16f0d6a)
 Call ID: 5e90139d-43e5-4e91-8daf-3ed8c16f0d6a
  Args:
    type: :Man
    source: :Infante_Carlos_Duke_of_Calabria
  AssignClass (794588a9-2720-49e1-9b99-4930673192cd)
 Call ID: 794588a9-2720-49e1-9b99-4930673192cd
  Args:
    type: :Person
    source: :Infante_Carlos_Duke_of_Calabria
  AddLiteral (44dc8aad-cd82-40b9-9796-b700037682c2)
 Call ID: 44dc8aad-cd82-40b9-9796-b700037682c2
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1938
    source: :Infante_Carlos_Duke_of_Calabria
  AddLiteral (d6038009-b275-4987-9ee6-b83fe50417bb)
 Call ID: d6038009-b275-4987-9ee6-b83fe50417bb
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: :Infante_Carlos_Duke_of_Calabria
    literal_value: 2015
  AssignClass (91d8beea-69af-48a4-9470-6c66067c14a5)
 Call ID: 91d8beea-69af-48a4-9470-6c66067c14a5
  Args:
    type: :Woman
    source: :Princess_Anne_of_Orleans
  AssignClass (3e660d17-c780-414c-b33c-3279903c67e4)
 Call ID: 3e660d17-c780-414c-b33c-3279903c67e4
  Args:
    type: :Person
    source: :Princess_Anne_of_Orleans
  AddTriple (b8871749-32f1-421f-996b-280a6cb99c98)
 Call ID: b8871749-32f1-421f-996b-280a6cb99c98
  Args:
    source: :Prince_Pedro_of_Bourbon-Two_Sicilies
    relation: :hasFather
    target: :Infante_Carlos_Duke_of_Calabria
  AddTriple (79c2e3b2-d7ed-460e-92ba-5f6af4ad4c24)
 Call ID: 79c2e3b2-d7ed-460e-92ba-5f6af4ad4c24
  Args:
    target: :Princess_Anne_of_Orleans
    relation: :hasMother
    source: :Prince_Pedro_of_Bourbon-Two_Sicilies
  AssignClass (265031c9-226b-4d08-872d-7c1795cd0ba0)
 Call ID: 265031c9-226b-4d08-872d-7c1795cd0ba0
  Args:
    type: :Woman
    source: :Sofia_Landaluce_y_Melgarejo
  AssignClass (ef5a965c-9a8b-4ec8-91c3-9551d8b24846)
 Call ID: ef5a965c-9a8b-4ec8-91c3-9551d8b24846
  Args:
    type: :Person
    source: :Sofia_Landaluce_y_Melgarejo
  AddLiteral (2b919be2-9463-4a21-b33a-7892f84ad26d)
 Call ID: 2b919be2-9463-4a21-b33a-7892f84ad26d
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1973
    source: :Sofia_Landaluce_y_Melgarejo
  AddTriple (48802083-bafc-4f58-8de5-398e5afa7f8f)
 Call ID: 48802083-bafc-4f58-8de5-398e5afa7f8f
  Args:
    target: :Sofia_Landaluce_y_Melgarejo
    relation: :hasRelation
    source: :Prince_Pedro_of_Bourbon-Two_Sicilies
  AddLiteral (3f56227d-c1b8-4879-a5a7-c3477266de66)
 Call ID: 3f56227d-c1b8-4879-a5a7-c3477266de66
  Args:
    literal_value: 2001
    source: :Prince_Pedro_of_Bourbon-Two_Sicilies
    relation: :hasMarriageYear
    literal_type: xsd:integer
  AssignClass (097bba3a-64a0-48f9-a227-7a3f3755b620)
 Call ID: 097bba3a-64a0-48f9-a227-7a3f3755b620
  Args:
    type: :Man
    source: :Jose_Manuel_Landaluce_y_Dominguez
  AssignClass (56c18d70-d725-438b-9f67-07f31595e4e9)
 Call ID: 56c18d70-d725-438b-9f67-07f31595e4e9
  Args:
    type: :Person
    source: :Jose_Manuel_Landaluce_y_Dominguez
  AssignClass (8ff10ce9-1bce-4d5e-90e7-6d4cd5141dd4)
 Call ID: 8ff10ce9-1bce-4d5e-90e7-6d4cd5141dd4
  Args:
    type: :Woman
    source: :Maria_de_las_Nieves_Blanca_Melgarejo_y_Gonzalez
  AssignClass (38a7fab6-ba3b-43d2-9778-8921822181ed)
 Call ID: 38a7fab6-ba3b-43d2-9778-8921822181ed
  Args:
    type: :Person
    source: :Maria_de_las_Nieves_Blanca_Melgarejo_y_Gonzalez
  AddTriple (1a45f041-2145-48dd-8854-6e4cf9288521)
 Call ID: 1a45f041-2145-48dd-8854-6e4cf9288521
  Args:
    source: :Sofia_Landaluce_y_Melgarejo
    target: :Jose_Manuel_Landaluce_y_Dominguez
    relation: :hasFather
  AddTriple (d5f38134-4b15-420a-8ad8-741a54eeccef)
 Call ID: d5f38134-4b15-420a-8ad8-741a54eeccef
  Args:
    target: :Maria_de_las_Nieves_Blanca_Melgarejo_y_Gonzalez
    relation: :hasMother
    source: :Sofia_Landaluce_y_Melgarejo
  AssignClass (f34c0e15-ec7f-4694-b183-28b7c6e4426a)
 Call ID: f34c0e15-ec7f-4694-b183-28b7c6e4426a
  Args:
    type: :Man
    source: :Prince_Carlos_1900
  AssignClass (81590358-76da-4c49-9e50-c7a058d55d48)
 Call ID: 81590358-76da-4c49-9e50-c7a058d55d48
  Args:
    type: :Person
    source: :Prince_Carlos_1900
  AssignClass (49f69412-8874-4414-9e4e-f77437c378fa)
 Call ID: 49f69412-8874-4414-9e4e-f77437c378fa
  Args:
    type: :Man
    source: :Prince_Ferdinand
  AssignClass (1acb79c4-d353-40ba-93f9-bf20cee28da2)
 Call ID: 1acb79c4-d353-40ba-93f9-bf20cee28da2
  Args:
    type: :Person
    source: :Prince_Ferdinand
  AddTriple (b87fdc08-2c04-447a-b349-8c9f94d038ca)
 Call ID: b87fdc08-2c04-447a-b349-8c9f94d038ca
  Args:
    source: :Prince_Carlos_1900
    target: :Prince_Ferdinand
    relation: :isSiblingOf
  AssignClass (3275b6c9-8735-43d9-ad74-1ba1fc8fc17f)
 Call ID: 3275b6c9-8735-43d9-ad74-1ba1fc8fc17f
  Args:
    type: :Man
    source: :Alfonso_de_Borbon_Count_of_Caserta
  AssignClass (b5f05226-5908-401d-9748-57b37972cc32)
 Call ID: b5f05226-5908-401d-9748-57b37972cc32
  Args:
    type: :Person
    source: :Alfonso_de_Borbon_Count_of_Caserta
  AddTriple (ca269e42-0018-4769-8a61-7f3941b63593)
 Call ID: ca269e42-0018-4769-8a61-7f3941b63593
  Args:
    relation: :isFatherOf
    target: :Prince_Carlos_1900
    source: :Alfonso_de_Borbon_Count_of_Caserta
  Finish (72249341-e681-496e-9f38-be128cee4094)
 Call ID: 72249341-e681-496e-9f38-be128cee4094
  Args: