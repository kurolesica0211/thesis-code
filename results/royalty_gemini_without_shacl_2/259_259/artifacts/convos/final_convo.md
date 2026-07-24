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
@prefix ns1: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
@prefix ns2: <http://www.w3.org/2003/11/swrl#> .
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

ns1:isRuleEnabled a owl:AnnotationProperty .

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

:x a ns2:Variable .

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

:y a ns2:Variable .

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

[] a ns2:Imp ;
    rdfs:label "infer hasSon" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasBrother" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasSister" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (aa170cb9-2975-4850-b90c-96ca085924fe)
 Call ID: aa170cb9-2975-4850-b90c-96ca085924fe
  Args:
    type: :Man
    source: :PrincePedroOfBourbonTwoSicilies
  AssignClass (20d3205d-f9b0-4804-97c9-f06d0ed31231)
 Call ID: 20d3205d-f9b0-4804-97c9-f06d0ed31231
  Args:
    type: :Person
    source: :PrincePedroOfBourbonTwoSicilies
  AddLiteral (2d0ea3a1-28f9-4a4b-ba74-bf57222f8d75)
 Call ID: 2d0ea3a1-28f9-4a4b-ba74-bf57222f8d75
  Args:
    source: :PrincePedroOfBourbonTwoSicilies
    literal_type: xsd:string
    literal_value: Pedro Juan María Alejo Saturnino de Todos los Santos
    relation: :alsoKnownAs
  AddLiteral (9d132367-d694-4c66-acf9-7ceeeef6129e)
 Call ID: 9d132367-d694-4c66-acf9-7ceeeef6129e
  Args:
    relation: :hasBirthYear
    literal_value: 1968
    source: :PrincePedroOfBourbonTwoSicilies
    literal_type: xsd:integer
  AssignClass (3adbccd6-d41e-47eb-a041-6c476eebe534)
 Call ID: 3adbccd6-d41e-47eb-a041-6c476eebe534
  Args:
    type: :Man
    source: :InfanteCarlosDukeOfCalabria
  AssignClass (c3abcb31-9c19-4567-852f-3e23fc32ff29)
 Call ID: c3abcb31-9c19-4567-852f-3e23fc32ff29
  Args:
    type: :Person
    source: :InfanteCarlosDukeOfCalabria
  AddLiteral (4c3878e0-9c5b-4273-b218-6b246c419d6d)
 Call ID: 4c3878e0-9c5b-4273-b218-6b246c419d6d
  Args:
    literal_type: xsd:integer
    source: :InfanteCarlosDukeOfCalabria
    literal_value: 1938
    relation: :hasBirthYear
  AddLiteral (16af5150-3944-4a55-aa0d-e7ee3c6f95b1)
 Call ID: 16af5150-3944-4a55-aa0d-e7ee3c6f95b1
  Args:
    literal_type: xsd:integer
    source: :InfanteCarlosDukeOfCalabria
    relation: :hasDeathYear
    literal_value: 2015
  AssignClass (df6ab5be-5825-4de9-aad2-caaa6d5c1f42)
 Call ID: df6ab5be-5825-4de9-aad2-caaa6d5c1f42
  Args:
    type: :Woman
    source: :PrincessAnneOfOrleans
  AssignClass (1a16147e-e102-441c-88a1-f2fc98f8f010)
 Call ID: 1a16147e-e102-441c-88a1-f2fc98f8f010
  Args:
    type: :Person
    source: :PrincessAnneOfOrleans
  AddTriple (ab3debdf-034e-4dc8-858e-1f04d602874e)
 Call ID: ab3debdf-034e-4dc8-858e-1f04d602874e
  Args:
    relation: :hasFather
    target: :InfanteCarlosDukeOfCalabria
    source: :PrincePedroOfBourbonTwoSicilies
  AddTriple (e8ad7fc1-d9b4-427e-9ee7-ffc7824f8dcc)
 Call ID: e8ad7fc1-d9b4-427e-9ee7-ffc7824f8dcc
  Args:
    source: :PrincePedroOfBourbonTwoSicilies
    target: :PrincessAnneOfOrleans
    relation: :hasMother
  AssignClass (70a92141-12c3-4dbd-8bef-3c76874a5ae5)
 Call ID: 70a92141-12c3-4dbd-8bef-3c76874a5ae5
  Args:
    type: :Woman
    source: :SofiaLandaluceYMelgarejo
  AssignClass (f6b68bcb-b997-49bf-9e56-f9d417bf6feb)
 Call ID: f6b68bcb-b997-49bf-9e56-f9d417bf6feb
  Args:
    type: :Person
    source: :SofiaLandaluceYMelgarejo
  AddLiteral (a678c624-44b9-4bf3-b9d2-c24fed97ab18)
 Call ID: a678c624-44b9-4bf3-b9d2-c24fed97ab18
  Args:
    literal_value: 1973
    relation: :hasBirthYear
    source: :SofiaLandaluceYMelgarejo
    literal_type: xsd:integer
  AddTriple (d144ed6a-4fbc-4fa2-ae4e-303cddcb66f0)
 Call ID: d144ed6a-4fbc-4fa2-ae4e-303cddcb66f0
  Args:
    target: :SofiaLandaluceYMelgarejo
    source: :PrincePedroOfBourbonTwoSicilies
    relation: :hasMarriageYear
  AddLiteral (5d40ad76-7b35-4c52-b229-79c0e5b6bfdc)
 Call ID: 5d40ad76-7b35-4c52-b229-79c0e5b6bfdc
  Args:
    literal_value: 2001
    relation: :hasMarriageYear
    source: :PrincePedroOfBourbonTwoSicilies
    literal_type: xsd:integer
  AssignClass (5a245ca3-923f-4b7e-a947-7074846f0529)
 Call ID: 5a245ca3-923f-4b7e-a947-7074846f0529
  Args:
    type: :Man
    source: :JoseManuelLandaluceYDominguez
  AssignClass (c22c5dd7-ea89-4d40-9a15-2379d1c999b8)
 Call ID: c22c5dd7-ea89-4d40-9a15-2379d1c999b8
  Args:
    type: :Person
    source: :JoseManuelLandaluceYDominguez
  AssignClass (6f88f927-f38d-4060-87aa-d5cf5670add7)
 Call ID: 6f88f927-f38d-4060-87aa-d5cf5670add7
  Args:
    type: :Woman
    source: :MariaDeLasNievesBlancaMelgarejoYGonzalez
  AssignClass (02a42989-d315-4c18-92a5-6bbd6e8886a5)
 Call ID: 02a42989-d315-4c18-92a5-6bbd6e8886a5
  Args:
    type: :Person
    source: :MariaDeLasNievesBlancaMelgarejoYGonzalez
  AddTriple (9b475cc8-af6f-4015-9861-df85410d78c3)
 Call ID: 9b475cc8-af6f-4015-9861-df85410d78c3
  Args:
    target: :JoseManuelLandaluceYDominguez
    source: :SofiaLandaluceYMelgarejo
    relation: :hasFather
  AddTriple (d0076b98-6f55-4c82-8569-0df4fa396539)
 Call ID: d0076b98-6f55-4c82-8569-0df4fa396539
  Args:
    target: :MariaDeLasNievesBlancaMelgarejoYGonzalez
    source: :SofiaLandaluceYMelgarejo
    relation: :hasMother
  AssignClass (cdd331db-1414-4875-9d5d-a7a62ba90ab8)
 Call ID: cdd331db-1414-4875-9d5d-a7a62ba90ab8
  Args:
    type: :Man
    source: :PrinceCarlosDukeOfCalabria1900
  AssignClass (b2ee0a0f-1291-4e15-969c-90c21777cf5a)
 Call ID: b2ee0a0f-1291-4e15-969c-90c21777cf5a
  Args:
    type: :Person
    source: :PrinceCarlosDukeOfCalabria1900
  AssignClass (4d65eb55-65b8-4008-ae5c-a59d972f807b)
 Call ID: 4d65eb55-65b8-4008-ae5c-a59d972f807b
  Args:
    type: :Man
    source: :PrinceFerdinand
  AssignClass (710cdde0-6b70-4d73-8cf0-5c603b0fb9b5)
 Call ID: 710cdde0-6b70-4d73-8cf0-5c603b0fb9b5
  Args:
    type: :Person
    source: :PrinceFerdinand
  AddTriple (82427821-5418-42ab-bd93-c65597d6c72e)
 Call ID: 82427821-5418-42ab-bd93-c65597d6c72e
  Args:
    source: :PrinceCarlosDukeOfCalabria1900
    target: :PrinceFerdinand
    relation: :isBrotherOf
  AssignClass (50b80b65-50ea-43dd-b807-476bef015537)
 Call ID: 50b80b65-50ea-43dd-b807-476bef015537
  Args:
    type: :Woman
    source: :MariaDeLasMercedesPrincessOfAsturias
  AssignClass (a1c97c9b-3b57-45b7-8f44-a59271a2dcb8)
 Call ID: a1c97c9b-3b57-45b7-8f44-a59271a2dcb8
  Args:
    type: :Person
    source: :MariaDeLasMercedesPrincessOfAsturias
  AddTriple (ccbfa250-3ae8-4921-893c-d721014448e1)
 Call ID: ccbfa250-3ae8-4921-893c-d721014448e1
  Args:
    target: :MariaDeLasMercedesPrincessOfAsturias
    source: :PrinceCarlosDukeOfCalabria1900
    relation: :hasRelation
  AssignClass (f79efce2-8f2e-4f73-9a8e-27b8d33d18ac)
 Call ID: f79efce2-8f2e-4f73-9a8e-27b8d33d18ac
  Args:
    type: :Man
    source: :PrinceCarloDukeOfCastro
  AssignClass (952e0f06-75b5-4824-84b9-107e4e878338)
 Call ID: 952e0f06-75b5-4824-84b9-107e4e878338
  Args:
    type: :Person
    source: :PrinceCarloDukeOfCastro
  Finish (60d7de9c-7e75-4b60-9f20-9d5e807a89a6)
 Call ID: 60d7de9c-7e75-4b60-9f20-9d5e807a89a6
  Args: