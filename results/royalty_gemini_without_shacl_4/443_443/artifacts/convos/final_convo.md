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
  AssignClass (99c0cd01-36c7-4829-af6b-a0f2fd8e68ee)
 Call ID: 99c0cd01-36c7-4829-af6b-a0f2fd8e68ee
  Args:
    source: Jaime_of_Bourbon-Two_Sicilies
    type: :Man
  AssignClass (07ffc315-be8f-4f2b-8b58-2fd4ceef265a)
 Call ID: 07ffc315-be8f-4f2b-8b58-2fd4ceef265a
  Args:
    type: :Person
    source: Jaime_of_Bourbon-Two_Sicilies
  AddLiteral (9d3cb186-b24a-4fb2-a136-e6774ba8bc9a)
 Call ID: 9d3cb186-b24a-4fb2-a136-e6774ba8bc9a
  Args:
    literal_value: 1993
    literal_type: xsd:integer
    source: Jaime_of_Bourbon-Two_Sicilies
    relation: :hasBirthYear
  AssignClass (1264427c-4986-4e6c-a5f7-4bec01510446)
 Call ID: 1264427c-4986-4e6c-a5f7-4bec01510446
  Args:
    source: Pedro_of_Bourbon-Two_Sicilies
    type: :Man
  AssignClass (3a41fa41-466d-4f2a-830e-b0b619c9a461)
 Call ID: 3a41fa41-466d-4f2a-830e-b0b619c9a461
  Args:
    source: Pedro_of_Bourbon-Two_Sicilies
    type: :Person
  AddLiteral (73e88a21-ccf3-474c-b53f-0841b9ddb5d7)
 Call ID: 73e88a21-ccf3-474c-b53f-0841b9ddb5d7
  Args:
    literal_value: 1968
    source: Pedro_of_Bourbon-Two_Sicilies
    literal_type: xsd:integer
    relation: :hasBirthYear
  AssignClass (be9ee57d-9e13-493b-83ef-74ac3c706fb5)
 Call ID: be9ee57d-9e13-493b-83ef-74ac3c706fb5
  Args:
    type: :Woman
    source: Sofia_Landaluce_y_Melgarejo
  AssignClass (3964c827-232e-4fa3-b0f9-bdb61ef23b66)
 Call ID: 3964c827-232e-4fa3-b0f9-bdb61ef23b66
  Args:
    type: :Person
    source: Sofia_Landaluce_y_Melgarejo
  AddLiteral (b40e8b04-0b64-4f18-8a54-6823f612957a)
 Call ID: b40e8b04-0b64-4f18-8a54-6823f612957a
  Args:
    literal_value: 1973
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Sofia_Landaluce_y_Melgarejo
  AddTriple (ae3d5e31-c19c-493c-8095-10fdb54962d3)
 Call ID: ae3d5e31-c19c-493c-8095-10fdb54962d3
  Args:
    target: Pedro_of_Bourbon-Two_Sicilies
    source: Jaime_of_Bourbon-Two_Sicilies
    relation: :hasFather
  AddTriple (6c6beac6-9570-489f-a056-dbd3178cc9dd)
 Call ID: 6c6beac6-9570-489f-a056-dbd3178cc9dd
  Args:
    relation: :hasMother
    source: Jaime_of_Bourbon-Two_Sicilies
    target: Sofia_Landaluce_y_Melgarejo
  AssignClass (a9bba6b3-ea74-4132-8e3d-d3d040c8cd62)
 Call ID: a9bba6b3-ea74-4132-8e3d-d3d040c8cd62
  Args:
    source: Carlos_of_Bourbon-Two_Sicilies
    type: :Man
  AssignClass (92c4f4f1-ab76-4260-ac9f-d2199bb0358c)
 Call ID: 92c4f4f1-ab76-4260-ac9f-d2199bb0358c
  Args:
    type: :Person
    source: Carlos_of_Bourbon-Two_Sicilies
  AddLiteral (5640aad8-8ec0-4579-a963-469096d74330)
 Call ID: 5640aad8-8ec0-4579-a963-469096d74330
  Args:
    source: Carlos_of_Bourbon-Two_Sicilies
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1938
  AddLiteral (60da8865-6c53-4626-a09b-33616b8642e4)
 Call ID: 60da8865-6c53-4626-a09b-33616b8642e4
  Args:
    literal_value: 2015
    source: Carlos_of_Bourbon-Two_Sicilies
    literal_type: xsd:integer
    relation: :hasDeathYear
  AssignClass (d721fadf-d927-431a-b92d-d08a900fc34f)
 Call ID: d721fadf-d927-431a-b92d-d08a900fc34f
  Args:
    type: :Woman
    source: Anne_of_Orleans
  AssignClass (48a2ded4-924e-4ac4-9504-0058317138a6)
 Call ID: 48a2ded4-924e-4ac4-9504-0058317138a6
  Args:
    source: Anne_of_Orleans
    type: :Person
  AddTriple (3ef5563d-f41b-411b-b1b0-bc86329ec764)
 Call ID: 3ef5563d-f41b-411b-b1b0-bc86329ec764
  Args:
    target: Carlos_of_Bourbon-Two_Sicilies
    source: Pedro_of_Bourbon-Two_Sicilies
    relation: :hasFather
  AddTriple (f1efcb39-b95f-4446-b6d5-d953e8a3ddb3)
 Call ID: f1efcb39-b95f-4446-b6d5-d953e8a3ddb3
  Args:
    target: Anne_of_Orleans
    source: Pedro_of_Bourbon-Two_Sicilies
    relation: :hasMother
  AssignClass (c68e297a-5d36-4d68-8e71-835d61cc23ee)
 Call ID: c68e297a-5d36-4d68-8e71-835d61cc23ee
  Args:
    source: Charlotte_Lindesay-Bethune
    type: :Woman
  AssignClass (f5f73dd7-c3c7-4497-b33a-e5c5c6fbcce7)
 Call ID: f5f73dd7-c3c7-4497-b33a-e5c5c6fbcce7
  Args:
    type: :Person
    source: Charlotte_Lindesay-Bethune
  AddTriple (a667b4d7-c747-4edc-9e75-c4d5ca413292)
 Call ID: a667b4d7-c747-4edc-9e75-c4d5ca413292
  Args:
    relation: :hasRelation
    source: Jaime_of_Bourbon-Two_Sicilies
    target: Charlotte_Lindesay-Bethune
  AddLiteral (64086ef4-01ae-4cb2-b467-c8f66363e72c)
 Call ID: 64086ef4-01ae-4cb2-b467-c8f66363e72c
  Args:
    literal_value: 2021
    literal_type: xsd:integer
    source: Jaime_of_Bourbon-Two_Sicilies
    relation: :hasMarriageYear
  AssignClass (1c0fa421-f485-4951-aad4-98571d94d2c1)
 Call ID: 1c0fa421-f485-4951-aad4-98571d94d2c1
  Args:
    type: :Man
    source: James_Lindesay-Bethune
  AssignClass (3e3b1b0e-e02c-48e8-93fb-5efe440ac694)
 Call ID: 3e3b1b0e-e02c-48e8-93fb-5efe440ac694
  Args:
    type: :Person
    source: James_Lindesay-Bethune
  AssignClass (a6515fe0-94bc-49bb-b91a-c560f0cd4a9d)
 Call ID: a6515fe0-94bc-49bb-b91a-c560f0cd4a9d
  Args:
    source: Diana_Mary_Chamberlayne-Macdonald
    type: :Woman
  AssignClass (696a6909-2f61-47d9-a595-a502ac791805)
 Call ID: 696a6909-2f61-47d9-a595-a502ac791805
  Args:
    source: Diana_Mary_Chamberlayne-Macdonald
    type: :Person
  AddTriple (04a8e6cb-16ae-402f-8d58-ddf93efd428f)
 Call ID: 04a8e6cb-16ae-402f-8d58-ddf93efd428f
  Args:
    relation: :hasFather
    source: Charlotte_Lindesay-Bethune
    target: James_Lindesay-Bethune
  AddTriple (b7312404-ed2f-474e-9968-f3759dbfb5b2)
 Call ID: b7312404-ed2f-474e-9968-f3759dbfb5b2
  Args:
    relation: :hasMother
    source: Charlotte_Lindesay-Bethune
    target: Diana_Mary_Chamberlayne-Macdonald
  AssignClass (3b3a72e5-b533-428c-9b52-37c7cdf5395a)
 Call ID: 3b3a72e5-b533-428c-9b52-37c7cdf5395a
  Args:
    source: Francesca_Sofia_of_Bourbon-Two_Sicilies
    type: :Woman
  AssignClass (82d20131-8203-4e1f-a715-299a9368091d)
 Call ID: 82d20131-8203-4e1f-a715-299a9368091d
  Args:
    source: Francesca_Sofia_of_Bourbon-Two_Sicilies
    type: :Person
  AddTriple (60a6cad3-e727-4dfb-b495-f44d3ffa82c2)
 Call ID: 60a6cad3-e727-4dfb-b495-f44d3ffa82c2
  Args:
    source: Francesca_Sofia_of_Bourbon-Two_Sicilies
    target: Jaime_of_Bourbon-Two_Sicilies
    relation: :hasFather
  AddTriple (e485b020-c500-496d-9273-dbeccceade08)
 Call ID: e485b020-c500-496d-9273-dbeccceade08
  Args:
    target: Charlotte_Lindesay-Bethune
    source: Francesca_Sofia_of_Bourbon-Two_Sicilies
    relation: :hasMother
  AssignClass (504e1967-c683-4e82-baac-6579d493f5ab)
 Call ID: 504e1967-c683-4e82-baac-6579d493f5ab
  Args:
    type: :Woman
    source: Ines_of_Bourbon-Two_Sicilies
  AssignClass (7163ece6-0934-4f46-a56b-acffc9301eeb)
 Call ID: 7163ece6-0934-4f46-a56b-acffc9301eeb
  Args:
    source: Ines_of_Bourbon-Two_Sicilies
    type: :Person
  AddTriple (2e8bddec-6614-4566-aa73-92ade7cda43c)
 Call ID: 2e8bddec-6614-4566-aa73-92ade7cda43c
  Args:
    target: Jaime_of_Bourbon-Two_Sicilies
    source: Ines_of_Bourbon-Two_Sicilies
    relation: :hasFather
  AddTriple (1fa9aefc-2031-4942-8062-a70f7642a153)
 Call ID: 1fa9aefc-2031-4942-8062-a70f7642a153
  Args:
    relation: :hasMother
    target: Charlotte_Lindesay-Bethune
    source: Ines_of_Bourbon-Two_Sicilies
  Finish (ef38e391-e564-4604-a6c6-bcf1b91013af)
 Call ID: ef38e391-e564-4604-a6c6-bcf1b91013af
  Args: