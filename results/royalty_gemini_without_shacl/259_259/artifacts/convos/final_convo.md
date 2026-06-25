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
  AssignClass (cf0ca696-7352-4406-9563-7a471c6cfb85)
 Call ID: cf0ca696-7352-4406-9563-7a471c6cfb85
  Args:
    type: :Man
    source: Prince_Pedro_of_Bourbon-Two_Sicilies
  AssignClass (d96336e3-c3d8-447e-ba97-5764ae8f6c1a)
 Call ID: d96336e3-c3d8-447e-ba97-5764ae8f6c1a
  Args:
    source: Prince_Pedro_of_Bourbon-Two_Sicilies
    type: :Person
  AddLiteral (f6f20711-6bd6-4e8f-a325-d1de12267d8d)
 Call ID: f6f20711-6bd6-4e8f-a325-d1de12267d8d
  Args:
    source: Prince_Pedro_of_Bourbon-Two_Sicilies
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1968
  AssignClass (7c32769f-596e-4da2-8a01-495c6cb7761e)
 Call ID: 7c32769f-596e-4da2-8a01-495c6cb7761e
  Args:
    source: Infante_Carlos_Duke_of_Calabria
    type: :Man
  AssignClass (3c0a1e46-2621-43a5-ad72-924669de2d41)
 Call ID: 3c0a1e46-2621-43a5-ad72-924669de2d41
  Args:
    source: Infante_Carlos_Duke_of_Calabria
    type: :Person
  AddLiteral (694378d7-19b0-4792-8b84-8abc632750d4)
 Call ID: 694378d7-19b0-4792-8b84-8abc632750d4
  Args:
    literal_value: 1938
    relation: :hasBirthYear
    source: Infante_Carlos_Duke_of_Calabria
    literal_type: xsd:integer
  AddLiteral (1c0e06b9-8e01-4aa1-9321-386a3d019963)
 Call ID: 1c0e06b9-8e01-4aa1-9321-386a3d019963
  Args:
    source: Infante_Carlos_Duke_of_Calabria
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 2015
  AssignClass (67e68832-8811-4efe-ba3f-b2d2a247335f)
 Call ID: 67e68832-8811-4efe-ba3f-b2d2a247335f
  Args:
    source: Princess_Anne_of_Orléans
    type: :Woman
  AssignClass (beefe510-8691-47df-a758-8df45d10abb5)
 Call ID: beefe510-8691-47df-a758-8df45d10abb5
  Args:
    source: Princess_Anne_of_Orléans
    type: :Person
  AddTriple (3154347c-df14-43d2-a4ee-7946dab2e71f)
 Call ID: 3154347c-df14-43d2-a4ee-7946dab2e71f
  Args:
    source: Prince_Pedro_of_Bourbon-Two_Sicilies
    relation: :hasFather
    target: Infante_Carlos_Duke_of_Calabria
  AddTriple (ee425511-348f-4e85-98bc-634bc3792208)
 Call ID: ee425511-348f-4e85-98bc-634bc3792208
  Args:
    target: Princess_Anne_of_Orléans
    relation: :hasMother
    source: Prince_Pedro_of_Bourbon-Two_Sicilies
  AssignClass (9e5b36ec-aa8e-4ff0-8ded-209135e65e34)
 Call ID: 9e5b36ec-aa8e-4ff0-8ded-209135e65e34
  Args:
    source: Sofía_Landaluce_y_Melgarejo
    type: :Woman
  AssignClass (1b077144-7243-4f0d-aa3f-3fd7a8b5cab2)
 Call ID: 1b077144-7243-4f0d-aa3f-3fd7a8b5cab2
  Args:
    source: Sofía_Landaluce_y_Melgarejo
    type: :Person
  AddLiteral (c7737e5f-51cc-4d4d-b739-6bcc5df5f7e0)
 Call ID: c7737e5f-51cc-4d4d-b739-6bcc5df5f7e0
  Args:
    relation: :hasBirthYear
    source: Sofía_Landaluce_y_Melgarejo
    literal_type: xsd:integer
    literal_value: 1973
  AddLiteral (ee274931-1616-422c-9c41-73122f0b732d)
 Call ID: ee274931-1616-422c-9c41-73122f0b732d
  Args:
    source: Prince_Pedro_of_Bourbon-Two_Sicilies
    relation: :hasMarriageYear
    literal_type: xsd:integer
    literal_value: 2001
  AssignClass (9e45b4ea-7e01-4a57-9466-36ebb6faea55)
 Call ID: 9e45b4ea-7e01-4a57-9466-36ebb6faea55
  Args:
    source: José_Manuel_Landaluce_y_Domínguez
    type: :Man
  AssignClass (96a3fed7-bf20-4154-b499-5c80fa00f863)
 Call ID: 96a3fed7-bf20-4154-b499-5c80fa00f863
  Args:
    type: :Person
    source: José_Manuel_Landaluce_y_Domínguez
  AssignClass (a44cc0af-2924-4c46-a556-cbbccf30060b)
 Call ID: a44cc0af-2924-4c46-a556-cbbccf30060b
  Args:
    type: :Woman
    source: María_de_las_Nieves_Blanca_Melgarejo_y_González
  AssignClass (1be03249-7eb3-47f0-87af-95fbe7246db5)
 Call ID: 1be03249-7eb3-47f0-87af-95fbe7246db5
  Args:
    source: María_de_las_Nieves_Blanca_Melgarejo_y_González
    type: :Person
  AddTriple (721a4523-9efa-4832-ab0a-d6ade0381f5c)
 Call ID: 721a4523-9efa-4832-ab0a-d6ade0381f5c
  Args:
    source: Sofía_Landaluce_y_Melgarejo
    relation: :hasFather
    target: José_Manuel_Landaluce_y_Domínguez
  AddTriple (7c7f4e4d-03a6-4be9-95dc-28e08a6c6205)
 Call ID: 7c7f4e4d-03a6-4be9-95dc-28e08a6c6205
  Args:
    target: María_de_las_Nieves_Blanca_Melgarejo_y_González
    source: Sofía_Landaluce_y_Melgarejo
    relation: :hasMother
  AssignClass (4d77f5ca-032f-4ab1-bec8-05cff2df7800)
 Call ID: 4d77f5ca-032f-4ab1-bec8-05cff2df7800
  Args:
    source: Prince_Carlos_of_Bourbon-Two_Sicilies
    type: :Man
  AssignClass (d1e16b69-092b-4bc7-9e14-496c62c4e36c)
 Call ID: d1e16b69-092b-4bc7-9e14-496c62c4e36c
  Args:
    source: Prince_Carlos_of_Bourbon-Two_Sicilies
    type: :Person
  AssignClass (3dbbd669-6dd1-42be-9c21-9be6d826a19b)
 Call ID: 3dbbd669-6dd1-42be-9c21-9be6d826a19b
  Args:
    type: :Man
    source: Prince_Ferdinand_of_Bourbon-Two_Sicilies
  AssignClass (92e1f9ef-2d1c-4150-9469-cc8a93f19c83)
 Call ID: 92e1f9ef-2d1c-4150-9469-cc8a93f19c83
  Args:
    source: Prince_Ferdinand_of_Bourbon-Two_Sicilies
    type: :Person
  AddTriple (e5b76a5c-3332-432e-a9d6-c0d76382a59b)
 Call ID: e5b76a5c-3332-432e-a9d6-c0d76382a59b
  Args:
    relation: :isBrotherOf
    source: Prince_Carlos_of_Bourbon-Two_Sicilies
    target: Prince_Ferdinand_of_Bourbon-Two_Sicilies
  AssignClass (8471fd68-996f-4561-bb85-840a2049fe59)
 Call ID: 8471fd68-996f-4561-bb85-840a2049fe59
  Args:
    type: :Man
    source: Don_Alfonso_de_Borbón_Count_of_Caserta
  AssignClass (616a5c54-2a98-47d6-a9f4-63cf1c30583d)
 Call ID: 616a5c54-2a98-47d6-a9f4-63cf1c30583d
  Args:
    type: :Person
    source: Don_Alfonso_de_Borbón_Count_of_Caserta
  AddTriple (b3c70ba7-0b89-45b5-a0b5-7f516a248476)
 Call ID: b3c70ba7-0b89-45b5-a0b5-7f516a248476
  Args:
    source: Don_Alfonso_de_Borbón_Count_of_Caserta
    relation: :isFatherOf
    target: Prince_Carlos_of_Bourbon-Two_Sicilies
  AssignClass (cd82da09-bf30-41ef-8756-9b28d0ce5b66)
 Call ID: cd82da09-bf30-41ef-8756-9b28d0ce5b66
  Args:
    type: :Woman
    source: María_de_las_Mercedes_Princess_of_Asturias
  AssignClass (62a80527-fc4a-441c-ad96-08f2b14df804)
 Call ID: 62a80527-fc4a-441c-ad96-08f2b14df804
  Args:
    source: María_de_las_Mercedes_Princess_of_Asturias
    type: :Person
  Finish (0f781c57-bb1f-487b-9ce6-f41ec2ae58f7)
 Call ID: 0f781c57-bb1f-487b-9ce6-f41ec2ae58f7
  Args: