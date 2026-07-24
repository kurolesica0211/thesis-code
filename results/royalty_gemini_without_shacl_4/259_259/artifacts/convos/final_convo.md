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
  AssignClass (320cdbd6-39b9-4ff4-9344-276806d19981)
 Call ID: 320cdbd6-39b9-4ff4-9344-276806d19981
  Args:
    source: Prince_Pedro_of_Bourbon-Two_Sicilies
    type: :Man
  AssignClass (e4857740-4b43-440d-9882-fbe31aa43793)
 Call ID: e4857740-4b43-440d-9882-fbe31aa43793
  Args:
    type: :Person
    source: Prince_Pedro_of_Bourbon-Two_Sicilies
  AddLiteral (d3b547d4-c6a3-4e2d-b606-6b455720a44f)
 Call ID: d3b547d4-c6a3-4e2d-b606-6b455720a44f
  Args:
    literal_value: 1968
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Prince_Pedro_of_Bourbon-Two_Sicilies
  AssignClass (89d86993-b021-48ab-8736-325b3fe9e1c1)
 Call ID: 89d86993-b021-48ab-8736-325b3fe9e1c1
  Args:
    type: :Man
    source: Infante_Carlos_Duke_of_Calabria
  AssignClass (716cf219-2375-44ea-8c64-8daf743d6f70)
 Call ID: 716cf219-2375-44ea-8c64-8daf743d6f70
  Args:
    source: Infante_Carlos_Duke_of_Calabria
    type: :Person
  AddLiteral (2013cfb2-68fe-4585-b90d-1300b049d9e4)
 Call ID: 2013cfb2-68fe-4585-b90d-1300b049d9e4
  Args:
    literal_value: 1938
    literal_type: xsd:integer
    source: Infante_Carlos_Duke_of_Calabria
    relation: :hasBirthYear
  AddLiteral (866864fa-f3f6-4ad5-9174-d5562dc46c24)
 Call ID: 866864fa-f3f6-4ad5-9174-d5562dc46c24
  Args:
    relation: :hasDeathYear
    source: Infante_Carlos_Duke_of_Calabria
    literal_value: 2015
    literal_type: xsd:integer
  AssignClass (e1160b54-fbeb-4805-8143-83ab2a5f285b)
 Call ID: e1160b54-fbeb-4805-8143-83ab2a5f285b
  Args:
    type: :Woman
    source: Princess_Anne_of_Orleans
  AssignClass (24949776-9fc6-49d8-af11-3eafd5d13ae6)
 Call ID: 24949776-9fc6-49d8-af11-3eafd5d13ae6
  Args:
    type: :Person
    source: Princess_Anne_of_Orleans
  AddTriple (11583302-5a9d-4ede-840e-99b85502daaa)
 Call ID: 11583302-5a9d-4ede-840e-99b85502daaa
  Args:
    source: Prince_Pedro_of_Bourbon-Two_Sicilies
    relation: :hasFather
    target: Infante_Carlos_Duke_of_Calabria
  AddTriple (61ddb9ec-6293-439f-bba4-7f97fc0d4c46)
 Call ID: 61ddb9ec-6293-439f-bba4-7f97fc0d4c46
  Args:
    target: Princess_Anne_of_Orleans
    relation: :hasMother
    source: Prince_Pedro_of_Bourbon-Two_Sicilies
  AssignClass (1d09115c-c372-4169-8111-92bec5b1a0f8)
 Call ID: 1d09115c-c372-4169-8111-92bec5b1a0f8
  Args:
    type: :Woman
    source: Sofia_Landaluce_y_Melgarejo
  AssignClass (aa0cfcdf-f5f1-44ee-8aa2-2881d43dc5c1)
 Call ID: aa0cfcdf-f5f1-44ee-8aa2-2881d43dc5c1
  Args:
    source: Sofia_Landaluce_y_Melgarejo
    type: :Person
  AddLiteral (b1ca3815-417d-4910-9677-3d7631f566df)
 Call ID: b1ca3815-417d-4910-9677-3d7631f566df
  Args:
    literal_type: xsd:integer
    literal_value: 1973
    source: Sofia_Landaluce_y_Melgarejo
    relation: :hasBirthYear
  AddTriple (74159344-681a-4ea6-9b8e-fc412396f06a)
 Call ID: 74159344-681a-4ea6-9b8e-fc412396f06a
  Args:
    target: Sofia_Landaluce_y_Melgarejo
    source: Prince_Pedro_of_Bourbon-Two_Sicilies
    relation: :hasRelation
  AddLiteral (a2720db4-5479-4bee-8074-36b2ca6b18e6)
 Call ID: a2720db4-5479-4bee-8074-36b2ca6b18e6
  Args:
    literal_value: 2001
    literal_type: xsd:integer
    source: Prince_Pedro_of_Bourbon-Two_Sicilies
    relation: :hasMarriageYear
  AssignClass (b1f0b82d-a9d3-477e-9a2d-89351a25f437)
 Call ID: b1f0b82d-a9d3-477e-9a2d-89351a25f437
  Args:
    type: :Man
    source: Jose_Manuel_Landaluce_y_Dominguez
  AssignClass (b5f4e6c6-eded-40e9-bb17-6c90ab2692e1)
 Call ID: b5f4e6c6-eded-40e9-bb17-6c90ab2692e1
  Args:
    type: :Person
    source: Jose_Manuel_Landaluce_y_Dominguez
  AssignClass (38f95e30-146c-485e-9dd0-7fa597de149a)
 Call ID: 38f95e30-146c-485e-9dd0-7fa597de149a
  Args:
    source: Maria_de_las_Nieves_Blanca_Melgarejo_y_Gonzalez
    type: :Woman
  AssignClass (7d78eac2-a0fc-477e-9508-54b34f82808c)
 Call ID: 7d78eac2-a0fc-477e-9508-54b34f82808c
  Args:
    source: Maria_de_las_Nieves_Blanca_Melgarejo_y_Gonzalez
    type: :Person
  AddTriple (c8134ad2-7768-4434-a444-44afb0d5017c)
 Call ID: c8134ad2-7768-4434-a444-44afb0d5017c
  Args:
    source: Sofia_Landaluce_y_Melgarejo
    relation: :hasFather
    target: Jose_Manuel_Landaluce_y_Dominguez
  AddTriple (5126ae5e-63d4-43c4-8153-1c0ddfc0c080)
 Call ID: 5126ae5e-63d4-43c4-8153-1c0ddfc0c080
  Args:
    relation: :hasMother
    source: Sofia_Landaluce_y_Melgarejo
    target: Maria_de_las_Nieves_Blanca_Melgarejo_y_Gonzalez
  Finish (2a074b2a-0bc7-4895-83a9-6df77064d459)
 Call ID: 2a074b2a-0bc7-4895-83a9-6df77064d459
  Args: