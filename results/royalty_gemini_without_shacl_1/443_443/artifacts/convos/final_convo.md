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


Prince Jaime of Bourbon-Two Sicilies, Duke of Noto (born 26 June 1993) is a Spanish aristocrat and heir to the headship of the House of Bourbon-Two Sicilies as eldest son of Prince Pedro, Duke of Calabria.
Biography

Jaime was born on 26 June 1993 in Madrid, Spain, as the illegitimate son of Prince Pedro, then Duke of Noto (born 16 October 1968), and Sofia Landaluce y Melgarejo (born 23 November 1973).
His paternal grandparents are Infante Carlos, Duke of Calabria (1938–2015), and his wife, Princess Anne of Orléans.
The Duke of Noto was educated at the Centro Universitario Villanueva (with a degree in law) and then obtained a master's degree in management from the IE University Business School.
Claim to the throne

Jaime's grandfather, Infante Don Carlos of Spain, Duke of Calabria, had to consider whether the future marriage of Prince Pedro to Sofía Landaluce y Melgarejo would meet the conditions established in the Sovereign Act that was signed in Naples on 7 April 1829, Law no. 2362, which gave the "head of Our House of Bourbon... such authority as is necessary to protect the purity and splendour of the throne", by requiring all members of the dynasty to have formal permission to marry.
The marriages of all members of the dynasty that had been considered capable of transmitting dynastic rights had been to royal princesses until the marriage of Prince Ranieri to Countess Carolina Zamoyska in 1929.
The ultimate decision of Infante Carlos to permit his son's marriage to be considered dynastic followed the marriages of the daughters of King Juan Carlos without them being required to renounce their right of succession to the Spanish throne, and a change in the marriage rules of the House of Austria.
Infante Carlos and his wife attended the marriage of Prince Pedro on 30 March 2001, and the marriage is treated as a dynastic marriage transmitting full rights of succession to all the children of Prince Pedro and his wife.
It was made clear by the date of the marriage of the future King Felipe VI in 2004 that the children of Prince Pedro and his wife had full dynastic rights, and the children bear the style of Royal Highness and the title of Prince(ss) of Bourbon-Two Sicilies.
Marriage and issue

On 25 September 2021 at Monreale Cathedral in Palermo, Jaime married Lady Charlotte Lindesay-Bethune, youngest daughter of James Lindesay-Bethune, 16th Earl of Lindsay, and his wife, Diana Mary Chamberlayne-Macdonald.
On 13 October 2023, the Duke and Duchess of Noto had their first child in London – a daughter named Francesca Sofía.
On 19 November 2025, the Duke and Duchess of Noto had their second child in London – a daughter named Ines.



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
  AssignClass (4fee5f75-da38-4878-8740-78b7ef0ebdf5)
 Call ID: 4fee5f75-da38-4878-8740-78b7ef0ebdf5
  Args:
    source: :Prince_Jaime_of_Bourbon_Two_Sicilies
    type: :Man
  AssignClass (daaa973e-5619-4071-b38f-1934467df0c8)
 Call ID: daaa973e-5619-4071-b38f-1934467df0c8
  Args:
    source: :Prince_Jaime_of_Bourbon_Two_Sicilies
    type: :Person
  AddLiteral (5fcf3082-a466-4601-95ab-f992b3622970)
 Call ID: 5fcf3082-a466-4601-95ab-f992b3622970
  Args:
    relation: :hasBirthYear
    source: :Prince_Jaime_of_Bourbon_Two_Sicilies
    literal_type: xsd:integer
    literal_value: 1993
  AssignClass (a756bc32-f520-45bd-9d45-124be7a990ed)
 Call ID: a756bc32-f520-45bd-9d45-124be7a990ed
  Args:
    source: :Prince_Pedro_Duke_of_Calabria
    type: :Man
  AssignClass (c9ba6aaa-a43e-4e8b-944f-922f15486a6a)
 Call ID: c9ba6aaa-a43e-4e8b-944f-922f15486a6a
  Args:
    source: :Prince_Pedro_Duke_of_Calabria
    type: :Person
  AddLiteral (1617bac3-9c96-4133-8e54-8adf8c733c1f)
 Call ID: 1617bac3-9c96-4133-8e54-8adf8c733c1f
  Args:
    relation: :hasBirthYear
    source: :Prince_Pedro_Duke_of_Calabria
    literal_value: 1968
    literal_type: xsd:integer
  AssignClass (d2ce3f07-9264-41a7-a053-4e7c7020bf18)
 Call ID: d2ce3f07-9264-41a7-a053-4e7c7020bf18
  Args:
    type: :Woman
    source: :Sofia_Landaluce_y_Melgarejo
  AssignClass (2b8f3d41-4a3b-4ac1-b000-029e96d09cdd)
 Call ID: 2b8f3d41-4a3b-4ac1-b000-029e96d09cdd
  Args:
    type: :Person
    source: :Sofia_Landaluce_y_Melgarejo
  AddLiteral (3b5658d6-26e5-41ae-8c2a-bcf0a8df089c)
 Call ID: 3b5658d6-26e5-41ae-8c2a-bcf0a8df089c
  Args:
    literal_value: 1973
    literal_type: xsd:integer
    source: :Sofia_Landaluce_y_Melgarejo
    relation: :hasBirthYear
  AddTriple (00206fbe-b8c9-4fe7-be8d-e7a01e8d11bc)
 Call ID: 00206fbe-b8c9-4fe7-be8d-e7a01e8d11bc
  Args:
    target: :Prince_Pedro_Duke_of_Calabria
    relation: :hasFather
    source: :Prince_Jaime_of_Bourbon_Two_Sicilies
  AddTriple (35b1101f-5693-4e37-8b4e-8f6beb7588d0)
 Call ID: 35b1101f-5693-4e37-8b4e-8f6beb7588d0
  Args:
    target: :Sofia_Landaluce_y_Melgarejo
    relation: :hasMother
    source: :Prince_Jaime_of_Bourbon_Two_Sicilies
  AssignClass (0cb9f425-16fe-4559-8edb-a50f5961afb3)
 Call ID: 0cb9f425-16fe-4559-8edb-a50f5961afb3
  Args:
    source: :Infante_Carlos_Duke_of_Calabria
    type: :Man
  AssignClass (317eb236-d7e5-4fcb-9f27-33877faf4e65)
 Call ID: 317eb236-d7e5-4fcb-9f27-33877faf4e65
  Args:
    source: :Infante_Carlos_Duke_of_Calabria
    type: :Person
  AddLiteral (598a17be-484a-4324-be56-4a8ec7d94d73)
 Call ID: 598a17be-484a-4324-be56-4a8ec7d94d73
  Args:
    relation: :hasBirthYear
    source: :Infante_Carlos_Duke_of_Calabria
    literal_value: 1938
    literal_type: xsd:integer
  AddLiteral (c3eddd45-e87d-430a-b98d-37d844e0ed18)
 Call ID: c3eddd45-e87d-430a-b98d-37d844e0ed18
  Args:
    relation: :hasDeathYear
    source: :Infante_Carlos_Duke_of_Calabria
    literal_type: xsd:integer
    literal_value: 2015
  AssignClass (0971f89c-a160-458c-854c-10f7f6771c54)
 Call ID: 0971f89c-a160-458c-854c-10f7f6771c54
  Args:
    source: :Princess_Anne_of_Orleans
    type: :Woman
  AssignClass (15cf4798-b52f-420b-80cf-2790003b24f9)
 Call ID: 15cf4798-b52f-420b-80cf-2790003b24f9
  Args:
    source: :Princess_Anne_of_Orleans
    type: :Person
  AddTriple (b3718714-c331-4238-8aa6-7023e72cdaa6)
 Call ID: b3718714-c331-4238-8aa6-7023e72cdaa6
  Args:
    target: :Infante_Carlos_Duke_of_Calabria
    source: :Prince_Pedro_Duke_of_Calabria
    relation: :hasFather
  AddTriple (2624b510-cd4a-43ea-bb11-197bdc3b06be)
 Call ID: 2624b510-cd4a-43ea-bb11-197bdc3b06be
  Args:
    relation: :hasMother
    source: :Prince_Pedro_Duke_of_Calabria
    target: :Princess_Anne_of_Orleans
  AssignClass (bb47b5e5-3eb5-417f-bf42-9a1dca0d103b)
 Call ID: bb47b5e5-3eb5-417f-bf42-9a1dca0d103b
  Args:
    type: :Woman
    source: :Lady_Charlotte_Lindesay_Bethune
  AssignClass (c1038ce3-601f-4b8e-9ba7-c4d0a3fb8433)
 Call ID: c1038ce3-601f-4b8e-9ba7-c4d0a3fb8433
  Args:
    source: :Lady_Charlotte_Lindesay_Bethune
    type: :Person
  AddTriple (2ed79914-0d81-4045-8aed-b2635b227a71)
 Call ID: 2ed79914-0d81-4045-8aed-b2635b227a71
  Args:
    target: :Lady_Charlotte_Lindesay_Bethune
    source: :Prince_Jaime_of_Bourbon_Two_Sicilies
    relation: :hasRelation
  AddLiteral (f724f259-2e4e-405e-a9fd-16ba7f7444ad)
 Call ID: f724f259-2e4e-405e-a9fd-16ba7f7444ad
  Args:
    literal_value: 2021
    literal_type: xsd:integer
    relation: :hasMarriageYear
    source: :Prince_Jaime_of_Bourbon_Two_Sicilies
  AssignClass (c74e5c0f-7e41-4f73-8f0a-8dde7a5b02d0)
 Call ID: c74e5c0f-7e41-4f73-8f0a-8dde7a5b02d0
  Args:
    source: :Francesca_Sofia
    type: :Woman
  AssignClass (62d9d103-acf0-42ff-ba04-68de7ecc45b0)
 Call ID: 62d9d103-acf0-42ff-ba04-68de7ecc45b0
  Args:
    source: :Francesca_Sofia
    type: :Person
  AddTriple (300675c9-f776-405d-8412-bb12ab11b553)
 Call ID: 300675c9-f776-405d-8412-bb12ab11b553
  Args:
    target: :Prince_Jaime_of_Bourbon_Two_Sicilies
    relation: :hasFather
    source: :Francesca_Sofia
  AddTriple (b22ad3b6-a932-4fe5-bc51-75c356ebb263)
 Call ID: b22ad3b6-a932-4fe5-bc51-75c356ebb263
  Args:
    relation: :hasMother
    source: :Francesca_Sofia
    target: :Lady_Charlotte_Lindesay_Bethune
  AssignClass (3cda09bc-8ffe-4d63-a4db-65599a2cad21)
 Call ID: 3cda09bc-8ffe-4d63-a4db-65599a2cad21
  Args:
    type: :Woman
    source: :Ines
  AssignClass (a2d6b753-4f62-420c-890a-1e31185134ba)
 Call ID: a2d6b753-4f62-420c-890a-1e31185134ba
  Args:
    type: :Person
    source: :Ines
  AddTriple (8ebd85ce-cff1-4e33-89d4-cb3b700fb24a)
 Call ID: 8ebd85ce-cff1-4e33-89d4-cb3b700fb24a
  Args:
    source: :Ines
    relation: :hasFather
    target: :Prince_Jaime_of_Bourbon_Two_Sicilies
  AddTriple (9a752436-9d7a-43e3-b9a4-8dedbe0d67bb)
 Call ID: 9a752436-9d7a-43e3-b9a4-8dedbe0d67bb
  Args:
    target: :Lady_Charlotte_Lindesay_Bethune
    relation: :hasMother
    source: :Ines
  AssignClass (f7285d6c-38f3-4c73-8645-ff626e35b5d4)
 Call ID: f7285d6c-38f3-4c73-8645-ff626e35b5d4
  Args:
    source: :James_Lindesay_Bethune_16th_Earl_of_Lindsay
    type: :Man
  AssignClass (b0ee3fae-b5ab-4759-9076-eb103138cdfe)
 Call ID: b0ee3fae-b5ab-4759-9076-eb103138cdfe
  Args:
    source: :James_Lindesay_Bethune_16th_Earl_of_Lindsay
    type: :Person
  AssignClass (28fbbf69-44a0-4243-8b84-8c39a995a91e)
 Call ID: 28fbbf69-44a0-4243-8b84-8c39a995a91e
  Args:
    source: :Diana_Mary_Chamberlayne_Macdonald
    type: :Woman
  AssignClass (521d312f-a6b7-44fc-82e5-464d3e1ba5da)
 Call ID: 521d312f-a6b7-44fc-82e5-464d3e1ba5da
  Args:
    type: :Person
    source: :Diana_Mary_Chamberlayne_Macdonald
  AddTriple (aab0dd97-21a3-40f6-bb17-55afea04a186)
 Call ID: aab0dd97-21a3-40f6-bb17-55afea04a186
  Args:
    target: :James_Lindesay_Bethune_16th_Earl_of_Lindsay
    relation: :hasFather
    source: :Lady_Charlotte_Lindesay_Bethune
  AddTriple (6804800f-a9fa-4598-a5cd-9840c133ef4e)
 Call ID: 6804800f-a9fa-4598-a5cd-9840c133ef4e
  Args:
    target: :Diana_Mary_Chamberlayne_Macdonald
    source: :Lady_Charlotte_Lindesay_Bethune
    relation: :hasMother
  Finish (e3078d7f-d814-4715-8b1f-e8120f340b60)
 Call ID: e3078d7f-d814-4715-8b1f-e8120f340b60
  Args: