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
Count Ingolf of Rosenborg RE (born 17 February 1940) is a Danish count and former prince.
Born Prince Ingolf of Denmark (Danish: Prins
Ingolf Christian Frederik Knud Harald Gorm Gustav Viggo Valdemar Aage til Danmark), he appeared likely to some day become king until the constitution was changed in 1953 to allow females to inherit the crown, placing his branch of the dynasty behind that of his first cousin Princess Margrethe and her two younger sisters.
Family

Ingolf was born at Sorgenfri Palace, Sorgenfri, as His Highness Prince Ingolf of Denmark.
Loss of place in succession

From the 1947 death of his grandfather, Christian X of Denmark, Ingolf stood only behind his father in the order of hereditary succession to the throne and was expected to become king in his turn.
His father, Prince Knud, was then the heir presumptive, due to succeed Ingolf's uncle King Frederik IX, who had three daughters but no sons.
In 1953, the Constitution of Denmark was amended to allow cognatic primogeniture.
Ingolf was thus relegated to fifth in the line of succession to the Danish throne, but more importantly, he now ranked behind Margrethe and others who were likely to have dynastic children of their own (as has, in fact, happened).
Ingolf's place in the line of succession, were he still eligible, would be no higher than eleventh today.
Loss of dynastic rights

In 1968, now with little hope of ascending the throne, Ingolf chose to forfeit his right of succession to the throne by marrying without having received the royal assent of the monarch in the Council of State.
The king's permission to marry was not sought because it was expected to be denied, since Ingolf's fiancée was an untitled commoner.
Though Frederik IX had liberalized traditional practice by allowing royal spouses who were not themselves royal, but who claimed noble blood and were known by courtesy titles (Anne Bowes-Lyon was the granddaughter of an earl and through her first marriage to the son of an earl bore the title of viscountess; Henri de Laborde de Monpezat used the title of count, though his family's claim to nobility was later acknowledged to be flawed), it would not be until 1995 that Margrethe II would allow her children to marry commoners with neither title nor claim to noble blood.
Ingolf was given the title count of Rosenborg and the style of Excellency, as was customary in the 20th century for Danish princes who forfeited their dynastic rights.
Prior to his son's wedding, Prince Knud sought to convince his brother that Ingolf should be allowed to retain his royal title after marriage.
But the king refused, on the grounds that other males of the dynasty who had been demoted to counts of Rosenborg upon marriage might try to reclaim their royal rank if Ingolf were allowed to do so, despite marrying a commoner as they had done.
So, in 1968, Ingolf forfeited his rights to the throne and took the title count of Rosenborg.
His younger brother Christian did the same three years later.
Ingolf married firstly Inge Terney (21 January 1938 in Copenhagen – 21 July 1996 in Velje), daughter of Georg Terney (1906–1977), hardware storer, and wife Jenny Kamilla Hansen (1908–1990), on 13 January 1968, at Kongens Lyngby Kirke, Kongens Lyngby, Denmark.
After being widowed, he married secondly Sussie Hjorhøy-Pedersen (born 20 February 1950 in Copenhagen), daughter of Frederick Walter Pedersen and wife Ruth Hjorhøy, who thus became "Her Excellency Countess Sussie of Rosenborg" on 7 March 1998, at Egtved, Denmark.
Ingolf is godfather to his grandnephew, Leopold Rosanes af Rosenborg, who is the grandson of his brother Christian.
Public role

Count Ingolf usually takes part in major public events associated with the royal family; he and Countess Sussie attended the May 2004 wedding of Crown Prince Frederik at Copenhagen Cathedral, and the subsequent reception at Fredensborg Palace.
On some occasions, they are listed as members of the royal family, such as when they attended the wedding of Prince Joachim in 2008 and the luncheon to celebrate the 75th birthday of Prince Henrik at Fredensborg Palace on 11 June 2009 On other occasions, such as the celebrations for the Queen's 70th birthday, they are listed along with non-royal guests, but even in these cases at the ceremonies themselves they are usually given precedence immediately after his sister Princess Elisabeth of Denmark.
Count Ingolf and Countess Sussie attended the Queen's ruby-jubilee (40th-anniversary) celebrations.
In 1964, when still Prince Ingolf, he acted as groomsman to his third cousin, Constantine II of Greece, on his marriage to Princess Anne-Marie of Denmark (also Ingolf's first cousin).
Ingolf receives an annual allowance of 1.4 million kroner according to the Danish Royal House website.
His sister, Princess Elisabeth, did not receive such an allowance, though she remained in the line of succession.



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
  AssignClass (b5aad039-0bb4-4c38-a5b8-f50c7854c798)
 Call ID: b5aad039-0bb4-4c38-a5b8-f50c7854c798
  Args:
    source: Ingolf_of_Rosenborg
    type: :Man
  AssignClass (8e2fdb48-72a5-4206-9a6c-e342d4a8c5c0)
 Call ID: 8e2fdb48-72a5-4206-9a6c-e342d4a8c5c0
  Args:
    source: Ingolf_of_Rosenborg
    type: :Person
  AddLiteral (be124912-b18c-4902-9540-bca34fe34f5a)
 Call ID: be124912-b18c-4902-9540-bca34fe34f5a
  Args:
    source: Ingolf_of_Rosenborg
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1940
  AddTriple (ecdeff4d-7299-4821-876f-2a582e4e9d97)
 Call ID: ecdeff4d-7299-4821-876f-2a582e4e9d97
  Args:
    target: :Male
    relation: :hasSex
    source: Ingolf_of_Rosenborg
  AssignClass (e21ef7b0-be2f-40d5-a9da-274eb993a3c1)
 Call ID: e21ef7b0-be2f-40d5-a9da-274eb993a3c1
  Args:
    type: :Male
    source: :Male
  AssignClass (45dd9b71-ec46-4b5b-aff4-3c503d49fcf8)
 Call ID: 45dd9b71-ec46-4b5b-aff4-3c503d49fcf8
  Args:
    type: :Sex
    source: :Male
  AssignClass (6cde5deb-9854-486c-a523-89b3dcc8ed09)
 Call ID: 6cde5deb-9854-486c-a523-89b3dcc8ed09
  Args:
    source: Christian_X_of_Denmark
    type: :Person
  AssignClass (5e1f0cde-94b5-48b3-b491-d5c1040cd37b)
 Call ID: 5e1f0cde-94b5-48b3-b491-d5c1040cd37b
  Args:
    type: :Man
    source: Christian_X_of_Denmark
  AddTriple (f403a29d-9253-4fc2-ae4c-ee9799da3d40)
 Call ID: f403a29d-9253-4fc2-ae4c-ee9799da3d40
  Args:
    source: Christian_X_of_Denmark
    target: :Knud_of_Denmark
    relation: :isFatherOf
  AssignClass (78320e68-afde-4091-9f76-cd514af2748e)
 Call ID: 78320e68-afde-4091-9f76-cd514af2748e
  Args:
    source: Knud_of_Denmark
    type: :Person
  AssignClass (6c9b98dd-214b-4ad3-bb20-214f0d61b0c6)
 Call ID: 6c9b98dd-214b-4ad3-bb20-214f0d61b0c6
  Args:
    source: Knud_of_Denmark
    type: :Man
  AddTriple (014269f5-efa5-4313-9acd-a1694c0cbcf5)
 Call ID: 014269f5-efa5-4313-9acd-a1694c0cbcf5
  Args:
    source: Knud_of_Denmark
    target: :Ingolf_of_Rosenborg
    relation: :isFatherOf
  AddTriple (bf4d74e2-f6f5-4a63-ab83-f3a6374c4e12)
 Call ID: bf4d74e2-f6f5-4a63-ab83-f3a6374c4e12
  Args:
    source: Knud_of_Denmark
    target: :Christian_of_Rosenborg
    relation: :isFatherOf
  AssignClass (144739eb-3d54-4c97-8019-9f7854c76311)
 Call ID: 144739eb-3d54-4c97-8019-9f7854c76311
  Args:
    source: Christian_of_Rosenborg
    type: :Person
  AssignClass (835aabf9-fac1-461c-9dda-93e47edf2772)
 Call ID: 835aabf9-fac1-461c-9dda-93e47edf2772
  Args:
    source: Christian_of_Rosenborg
    type: :Man
  AssignClass (9a1542c1-6453-4779-956d-ff40aac9b77c)
 Call ID: 9a1542c1-6453-4779-956d-ff40aac9b77c
  Args:
    type: :Person
    source: Elisabeth_of_Denmark
  AssignClass (be1857a5-2f39-4efe-9031-b3025e6d24a7)
 Call ID: be1857a5-2f39-4efe-9031-b3025e6d24a7
  Args:
    type: :Woman
    source: Elisabeth_of_Denmark
  AddTriple (a75bac1f-af26-4480-ad0d-3b97cc26ee99)
 Call ID: a75bac1f-af26-4480-ad0d-3b97cc26ee99
  Args:
    target: :Elisabeth_of_Denmark
    relation: :isFatherOf
    source: Knud_of_Denmark
  AssignClass (335ceff5-59e3-45e2-b739-27491f6b50c3)
 Call ID: 335ceff5-59e3-45e2-b739-27491f6b50c3
  Args:
    type: :Person
    source: Inge_Terney
  AssignClass (74e110ff-470d-46ac-84ed-7970fa6d1f80)
 Call ID: 74e110ff-470d-46ac-84ed-7970fa6d1f80
  Args:
    type: :Woman
    source: Inge_Terney
  AddTriple (278e26d4-229f-47d2-9202-f27b1ac051d4)
 Call ID: 278e26d4-229f-47d2-9202-f27b1ac051d4
  Args:
    relation: :hasRelation
    target: :Inge_Terney
    source: Ingolf_of_Rosenborg
  AddLiteral (4f812fe0-e4ce-4975-bd8f-46b15844eb7a)
 Call ID: 4f812fe0-e4ce-4975-bd8f-46b15844eb7a
  Args:
    source: Ingolf_of_Rosenborg
    literal_type: xsd:integer
    literal_value: 1968
    relation: :hasMarriageYear
  AssignClass (1c627d0a-070a-4d9a-b2e9-4861fdfc7ec4)
 Call ID: 1c627d0a-070a-4d9a-b2e9-4861fdfc7ec4
  Args:
    type: :Person
    source: Sussie_Hjorhoy-Pedersen
  AssignClass (b67f9dcf-4109-41f0-ae3e-04ba70a8a838)
 Call ID: b67f9dcf-4109-41f0-ae3e-04ba70a8a838
  Args:
    source: Sussie_Hjorhoy-Pedersen
    type: :Woman
  AddTriple (3db45d15-76db-48cd-b0ed-94ed693f21ec)
 Call ID: 3db45d15-76db-48cd-b0ed-94ed693f21ec
  Args:
    relation: :hasRelation
    target: :Sussie_Hjorhoy-Pedersen
    source: Ingolf_of_Rosenborg
  AddLiteral (f2257d85-9c5c-4bdf-9e41-136566ae3c31)
 Call ID: f2257d85-9c5c-4bdf-9e41-136566ae3c31
  Args:
    source: Ingolf_of_Rosenborg
    relation: :hasMarriageYear
    literal_value: 1998
    literal_type: xsd:integer
  AssignClass (81ee8277-84bf-4ec5-8e8c-40f60a1b3d31)
 Call ID: 81ee8277-84bf-4ec5-8e8c-40f60a1b3d31
  Args:
    type: :Person
    source: Georg_Terney
  AssignClass (39e6dcdc-f4b3-443a-bec8-c683d80b390d)
 Call ID: 39e6dcdc-f4b3-443a-bec8-c683d80b390d
  Args:
    source: Georg_Terney
    type: :Man
  AssignClass (95cd2977-291c-4b12-add3-82c8d17cde7c)
 Call ID: 95cd2977-291c-4b12-add3-82c8d17cde7c
  Args:
    type: :Person
    source: Jenny_Kamilla_Hansen
  AssignClass (045c0672-0c3c-4a51-acf3-fec5f6ae18f1)
 Call ID: 045c0672-0c3c-4a51-acf3-fec5f6ae18f1
  Args:
    type: :Woman
    source: Jenny_Kamilla_Hansen
  AddTriple (a59cb5b0-d65e-457b-be01-38563d5b159e)
 Call ID: a59cb5b0-d65e-457b-be01-38563d5b159e
  Args:
    relation: :isFatherOf
    target: :Inge_Terney
    source: Georg_Terney
  AddTriple (7186dfb8-3248-41a9-bb18-ede12a2f8fa7)
 Call ID: 7186dfb8-3248-41a9-bb18-ede12a2f8fa7
  Args:
    relation: :isMotherOf
    target: :Inge_Terney
    source: Jenny_Kamilla_Hansen
  AssignClass (9c422cae-09e6-49a3-a408-83779c245de2)
 Call ID: 9c422cae-09e6-49a3-a408-83779c245de2
  Args:
    type: :Person
    source: Frederick_Walter_Pedersen
  AssignClass (04ca3326-2b5a-41cf-8a50-61c456c0e859)
 Call ID: 04ca3326-2b5a-41cf-8a50-61c456c0e859
  Args:
    type: :Man
    source: Frederick_Walter_Pedersen
  AssignClass (87a87f02-7baf-41a6-9a77-4e533868fb24)
 Call ID: 87a87f02-7baf-41a6-9a77-4e533868fb24
  Args:
    source: Ruth_Hjorhoy
    type: :Person
  AssignClass (d7b59c2a-fc8c-4999-8aff-406dcb69d546)
 Call ID: d7b59c2a-fc8c-4999-8aff-406dcb69d546
  Args:
    source: Ruth_Hjorhoy
    type: :Woman
  AddTriple (19b677fc-6f64-470d-8734-2558cfb73187)
 Call ID: 19b677fc-6f64-470d-8734-2558cfb73187
  Args:
    source: Frederick_Walter_Pedersen
    target: :Sussie_Hjorhoy-Pedersen
    relation: :isFatherOf
  AddTriple (077d87d0-9f7e-4037-9897-2d7a50e20ad7)
 Call ID: 077d87d0-9f7e-4037-9897-2d7a50e20ad7
  Args:
    source: Ruth_Hjorhoy
    target: :Sussie_Hjorhoy-Pedersen
    relation: :isMotherOf
  AssignClass (1ada15ad-4e8d-4121-966e-0c3e7257e74a)
 Call ID: 1ada15ad-4e8d-4121-966e-0c3e7257e74a
  Args:
    type: :Person
    source: Leopold_Rosanes_af_Rosenborg
  AssignClass (38d50a01-d6a4-493d-8d7e-861357bd8e01)
 Call ID: 38d50a01-d6a4-493d-8d7e-861357bd8e01
  Args:
    type: :Man
    source: Leopold_Rosanes_af_Rosenborg
  AddTriple (6372ecf9-bed9-4414-a0fa-5da765f455b9)
 Call ID: 6372ecf9-bed9-4414-a0fa-5da765f455b9
  Args:
    relation: :isSonOf
    target: :Christian_of_Rosenborg
    source: Leopold_Rosanes_af_Rosenborg
  Finish (ce174aa2-0928-48b0-ade6-15d9621ac625)
 Call ID: ce174aa2-0928-48b0-ade6-15d9621ac625
  Args: