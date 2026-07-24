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
  AssignClass (b778ca62-c3bc-48a2-a9f6-bcb3027f1c8b)
 Call ID: b778ca62-c3bc-48a2-a9f6-bcb3027f1c8b
  Args:
    source: :Jaime_of_Bourbon-Two_Sicilies
    type: :Man
  AssignClass (0c44b095-4edf-4916-9d3f-cab48dd18e38)
 Call ID: 0c44b095-4edf-4916-9d3f-cab48dd18e38
  Args:
    source: :Jaime_of_Bourbon-Two_Sicilies
    type: :Person
  AddLiteral (0101b0e1-4048-4dd4-ada7-b9f0b23a9d56)
 Call ID: 0101b0e1-4048-4dd4-ada7-b9f0b23a9d56
  Args:
    source: :Jaime_of_Bourbon-Two_Sicilies
    relation: :hasBirthYear
    literal_value: 1993
    literal_type: xsd:integer
  AssignClass (4e8b2bf9-d74d-4f20-838b-a6cffc4bb005)
 Call ID: 4e8b2bf9-d74d-4f20-838b-a6cffc4bb005
  Args:
    source: :Prince_Pedro
    type: :Man
  AssignClass (c2264983-740d-452d-a843-e4b77cc6ea9b)
 Call ID: c2264983-740d-452d-a843-e4b77cc6ea9b
  Args:
    source: :Prince_Pedro
    type: :Person
  AddLiteral (8d1f85ae-4f8b-4477-90bb-e9da40ee4180)
 Call ID: 8d1f85ae-4f8b-4477-90bb-e9da40ee4180
  Args:
    source: :Prince_Pedro
    relation: :hasBirthYear
    literal_value: 1968
    literal_type: xsd:integer
  AssignClass (6895e9a9-15ff-4fe6-99de-643210680fcd)
 Call ID: 6895e9a9-15ff-4fe6-99de-643210680fcd
  Args:
    source: :Sofia_Landaluce_y_Melgarejo
    type: :Woman
  AssignClass (1c7a13d8-e317-4288-b054-518b3e5b7ac2)
 Call ID: 1c7a13d8-e317-4288-b054-518b3e5b7ac2
  Args:
    type: :Person
    source: :Sofia_Landaluce_y_Melgarejo
  AddLiteral (29168979-632f-4330-bc38-f57ae554cd66)
 Call ID: 29168979-632f-4330-bc38-f57ae554cd66
  Args:
    literal_type: xsd:integer
    literal_value: 1973
    source: :Sofia_Landaluce_y_Melgarejo
    relation: :hasBirthYear
  AddTriple (8bf5985e-7871-4232-99e3-fb0a5ba64be1)
 Call ID: 8bf5985e-7871-4232-99e3-fb0a5ba64be1
  Args:
    source: :Jaime_of_Bourbon-Two_Sicilies
    target: :Prince_Pedro
    relation: :isSonOf
  AddTriple (f781bfcb-2f5b-4195-9d4e-4cedf3cb090c)
 Call ID: f781bfcb-2f5b-4195-9d4e-4cedf3cb090c
  Args:
    target: :Sofia_Landaluce_y_Melgarejo
    relation: :isSonOf
    source: :Jaime_of_Bourbon-Two_Sicilies
  AssignClass (aec5d78e-3fcc-46a2-b803-1253a182e451)
 Call ID: aec5d78e-3fcc-46a2-b803-1253a182e451
  Args:
    type: :Man
    source: :Infante_Carlos
  AssignClass (4ee5edb4-c7c8-4c60-93a9-5bdc09fc07e5)
 Call ID: 4ee5edb4-c7c8-4c60-93a9-5bdc09fc07e5
  Args:
    source: :Infante_Carlos
    type: :Person
  AddLiteral (711cb957-20b1-4875-8805-9f41d3bbab3c)
 Call ID: 711cb957-20b1-4875-8805-9f41d3bbab3c
  Args:
    source: :Infante_Carlos
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1938
  AddLiteral (104415d4-8095-4eed-912d-abf11948c8dd)
 Call ID: 104415d4-8095-4eed-912d-abf11948c8dd
  Args:
    literal_value: 2015
    literal_type: xsd:integer
    source: :Infante_Carlos
    relation: :hasDeathYear
  AssignClass (7806d196-cc99-49ba-b602-75365514a18e)
 Call ID: 7806d196-cc99-49ba-b602-75365514a18e
  Args:
    type: :Woman
    source: :Princess_Anne_of_Orleans
  AssignClass (909fe459-db32-4ab3-8785-94114b6e00de)
 Call ID: 909fe459-db32-4ab3-8785-94114b6e00de
  Args:
    source: :Princess_Anne_of_Orleans
    type: :Person
  AddTriple (697dd5c6-67c6-49b5-970a-9cbb0f372bf6)
 Call ID: 697dd5c6-67c6-49b5-970a-9cbb0f372bf6
  Args:
    relation: :isFatherOf
    target: :Prince_Pedro
    source: :Infante_Carlos
  AddTriple (0508fa54-db6b-49db-b3f6-ec97870df0f6)
 Call ID: 0508fa54-db6b-49db-b3f6-ec97870df0f6
  Args:
    relation: :isMotherOf
    target: :Prince_Pedro
    source: :Princess_Anne_of_Orleans
  AssignClass (4dd796de-9623-42f9-8404-763b85f107d3)
 Call ID: 4dd796de-9623-42f9-8404-763b85f107d3
  Args:
    type: :Woman
    source: :Lady_Charlotte_Lindesay-Bethune
  AssignClass (df5d4384-2060-4802-9494-07ca31be9065)
 Call ID: df5d4384-2060-4802-9494-07ca31be9065
  Args:
    type: :Person
    source: :Lady_Charlotte_Lindesay-Bethune
  AddTriple (d22d5cf3-ec24-447d-b52e-ec8bd907c969)
 Call ID: d22d5cf3-ec24-447d-b52e-ec8bd907c969
  Args:
    target: :Lady_Charlotte_Lindesay-Bethune
    relation: :hasRelation
    source: :Jaime_of_Bourbon-Two_Sicilies
  AddLiteral (7da1c9db-a3d2-4d3d-ad1b-88ba02a802c3)
 Call ID: 7da1c9db-a3d2-4d3d-ad1b-88ba02a802c3
  Args:
    literal_value: 2021
    literal_type: xsd:integer
    relation: :hasMarriageYear
    source: :Jaime_of_Bourbon-Two_Sicilies
  AssignClass (bdaf0279-23cc-4e55-be46-8edce8c57f99)
 Call ID: bdaf0279-23cc-4e55-be46-8edce8c57f99
  Args:
    source: :James_Lindesay-Bethune
    type: :Man
  AssignClass (7cb9b33d-2296-49b7-b9ee-86f276e3881a)
 Call ID: 7cb9b33d-2296-49b7-b9ee-86f276e3881a
  Args:
    source: :James_Lindesay-Bethune
    type: :Person
  AssignClass (38f2612f-de4f-448c-93d9-4276c5f38bad)
 Call ID: 38f2612f-de4f-448c-93d9-4276c5f38bad
  Args:
    type: :Woman
    source: :Diana_Mary_Chamberlayne-Macdonald
  AssignClass (2a2c8de8-4c01-46de-ae66-12fa1cc806bb)
 Call ID: 2a2c8de8-4c01-46de-ae66-12fa1cc806bb
  Args:
    type: :Person
    source: :Diana_Mary_Chamberlayne-Macdonald
  AddTriple (bbfbee33-49b5-463f-89aa-1e3481e7cda5)
 Call ID: bbfbee33-49b5-463f-89aa-1e3481e7cda5
  Args:
    relation: :isFatherOf
    target: :Lady_Charlotte_Lindesay-Bethune
    source: :James_Lindesay-Bethune
  AddTriple (79910ec7-9f39-42aa-8234-8021dcca3790)
 Call ID: 79910ec7-9f39-42aa-8234-8021dcca3790
  Args:
    target: :Lady_Charlotte_Lindesay-Bethune
    relation: :isMotherOf
    source: :Diana_Mary_Chamberlayne-Macdonald
  AssignClass (cd2f7fca-7614-4bec-b453-c4ec86b95ce6)
 Call ID: cd2f7fca-7614-4bec-b453-c4ec86b95ce6
  Args:
    source: :Francesca_Sofia
    type: :Woman
  AssignClass (dabf1cb7-54f5-4628-878d-1288c964847c)
 Call ID: dabf1cb7-54f5-4628-878d-1288c964847c
  Args:
    type: :Person
    source: :Francesca_Sofia
  AddTriple (3cfe3d3d-f218-40c1-9023-22c7df397c23)
 Call ID: 3cfe3d3d-f218-40c1-9023-22c7df397c23
  Args:
    relation: :isDaughterOf
    target: :Jaime_of_Bourbon-Two_Sicilies
    source: :Francesca_Sofia
  AddTriple (e53ed51e-8d58-46bc-8a1e-711ec90ebb2e)
 Call ID: e53ed51e-8d58-46bc-8a1e-711ec90ebb2e
  Args:
    source: :Francesca_Sofia
    target: :Lady_Charlotte_Lindesay-Bethune
    relation: :isDaughterOf
  AssignClass (e1d9ad86-e036-4da7-a61c-58a9b6f067a3)
 Call ID: e1d9ad86-e036-4da7-a61c-58a9b6f067a3
  Args:
    type: :Woman
    source: :Ines
  AssignClass (9bb18b53-7a93-4a7d-a3f2-af9ea1df26d0)
 Call ID: 9bb18b53-7a93-4a7d-a3f2-af9ea1df26d0
  Args:
    type: :Person
    source: :Ines
  AddTriple (6bd4d0b6-602a-4fc3-8ee2-89fe55d4b85f)
 Call ID: 6bd4d0b6-602a-4fc3-8ee2-89fe55d4b85f
  Args:
    source: :Ines
    target: :Jaime_of_Bourbon-Two_Sicilies
    relation: :isDaughterOf
  AddTriple (7de161d5-f1fb-4e3b-8d5b-ea37665938d7)
 Call ID: 7de161d5-f1fb-4e3b-8d5b-ea37665938d7
  Args:
    relation: :isDaughterOf
    target: :Lady_Charlotte_Lindesay-Bethune
    source: :Ines
  Finish (02b0e017-0a38-4e2c-b721-a91877ececbc)
 Call ID: 02b0e017-0a38-4e2c-b721-a91877ececbc
  Args: