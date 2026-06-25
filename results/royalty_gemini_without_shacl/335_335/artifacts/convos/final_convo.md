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
  AssignClass (d94a51e9-5b37-4394-8bfb-3cd61769f975)
 Call ID: d94a51e9-5b37-4394-8bfb-3cd61769f975
  Args:
    type: :Man
    source: Ingolf_of_Rosenborg
  AssignClass (60d77800-ecdc-4583-a140-e91c3090320f)
 Call ID: 60d77800-ecdc-4583-a140-e91c3090320f
  Args:
    source: Ingolf_of_Rosenborg
    type: :Person
  AddLiteral (b0a04fbf-3d86-437f-8c03-41a202809e8a)
 Call ID: b0a04fbf-3d86-437f-8c03-41a202809e8a
  Args:
    literal_value: 1940
    literal_type: xsd:integer
    source: Ingolf_of_Rosenborg
    relation: :hasBirthYear
  AddLiteral (e45444d5-5d51-458e-85d1-6777defb9fad)
 Call ID: e45444d5-5d51-458e-85d1-6777defb9fad
  Args:
    relation: :knownAs
    source: Ingolf_of_Rosenborg
    literal_value: Count Ingolf of Rosenborg
    literal_type: xsd:string
  AssignClass (dd6f50fd-b682-46a1-b620-36e14ae4fed2)
 Call ID: dd6f50fd-b682-46a1-b620-36e14ae4fed2
  Args:
    source: Knud_of_Denmark
    type: :Man
  AssignClass (f8b3588a-7dd6-4e11-815c-c6ae6044fcea)
 Call ID: f8b3588a-7dd6-4e11-815c-c6ae6044fcea
  Args:
    type: :Person
    source: Knud_of_Denmark
  AddTriple (90e4d91d-26d2-4144-9bd4-002b2c636dcc)
 Call ID: 90e4d91d-26d2-4144-9bd4-002b2c636dcc
  Args:
    target: Knud_of_Denmark
    relation: :hasFather
    source: Ingolf_of_Rosenborg
  AssignClass (e9e68b90-bf8b-4acf-9d03-d8d9e41ae582)
 Call ID: e9e68b90-bf8b-4acf-9d03-d8d9e41ae582
  Args:
    type: :Man
    source: Christian_X_of_Denmark
  AssignClass (cf2ac6ff-b8e7-48b1-816b-88318b5e95e4)
 Call ID: cf2ac6ff-b8e7-48b1-816b-88318b5e95e4
  Args:
    source: Christian_X_of_Denmark
    type: :Person
  AddTriple (386609c4-94e9-4c85-8349-831a9544b037)
 Call ID: 386609c4-94e9-4c85-8349-831a9544b037
  Args:
    source: Knud_of_Denmark
    relation: :hasFather
    target: Christian_X_of_Denmark
  AssignClass (ea0d83c7-9bbf-4c2e-9b0c-f87ce947119d)
 Call ID: ea0d83c7-9bbf-4c2e-9b0c-f87ce947119d
  Args:
    type: :Man
    source: Christian_of_Rosenborg
  AssignClass (ab11ee42-6e16-486d-9f18-da3d793563ea)
 Call ID: ab11ee42-6e16-486d-9f18-da3d793563ea
  Args:
    source: Christian_of_Rosenborg
    type: :Person
  AddTriple (bc7af22a-9b3d-4759-bceb-62d84ebdfb20)
 Call ID: bc7af22a-9b3d-4759-bceb-62d84ebdfb20
  Args:
    source: Christian_of_Rosenborg
    target: Ingolf_of_Rosenborg
    relation: :isBrotherOf
  AssignClass (f3381db1-968c-4739-8762-a0e5d085fc88)
 Call ID: f3381db1-968c-4739-8762-a0e5d085fc88
  Args:
    source: Elisabeth_of_Denmark
    type: :Woman
  AssignClass (4c42619f-5639-4620-aead-e50d4192f03e)
 Call ID: 4c42619f-5639-4620-aead-e50d4192f03e
  Args:
    type: :Person
    source: Elisabeth_of_Denmark
  AddTriple (16cf07b5-1b78-4524-a035-8c6af65c7107)
 Call ID: 16cf07b5-1b78-4524-a035-8c6af65c7107
  Args:
    source: Elisabeth_of_Denmark
    target: Ingolf_of_Rosenborg
    relation: :isSisterOf
  AssignClass (3d548eeb-93b5-42bf-9a4c-cc469ff85eaf)
 Call ID: 3d548eeb-93b5-42bf-9a4c-cc469ff85eaf
  Args:
    type: :Woman
    source: Inge_Terney
  AssignClass (5a3e5ec2-105c-4a14-a7b9-0e3c73e42a1b)
 Call ID: 5a3e5ec2-105c-4a14-a7b9-0e3c73e42a1b
  Args:
    source: Inge_Terney
    type: :Person
  AddLiteral (5ef70e4a-e812-454e-959c-26cd9b74274e)
 Call ID: 5ef70e4a-e812-454e-959c-26cd9b74274e
  Args:
    relation: :hasBirthYear
    source: Inge_Terney
    literal_type: xsd:integer
    literal_value: 1938
  AddLiteral (e17d05f3-9d20-4ffc-b4f4-b48c9601c9ca)
 Call ID: e17d05f3-9d20-4ffc-b4f4-b48c9601c9ca
  Args:
    literal_type: xsd:integer
    literal_value: 1996
    relation: :hasDeathYear
    source: Inge_Terney
  AddLiteral (53e21051-b78a-401a-9a77-6ec9c728e927)
 Call ID: 53e21051-b78a-401a-9a77-6ec9c728e927
  Args:
    literal_value: 1968
    literal_type: xsd:integer
    relation: :hasMarriageYear
    source: Ingolf_of_Rosenborg
  AssignClass (1a8f43c3-6a07-4712-8bb2-e5bb779effc4)
 Call ID: 1a8f43c3-6a07-4712-8bb2-e5bb779effc4
  Args:
    source: Georg_Terney
    type: :Man
  AssignClass (9adb7411-a678-4bce-ad50-129008f18b4c)
 Call ID: 9adb7411-a678-4bce-ad50-129008f18b4c
  Args:
    type: :Person
    source: Georg_Terney
  AddLiteral (860aacb5-aab4-4102-856e-0daab375471b)
 Call ID: 860aacb5-aab4-4102-856e-0daab375471b
  Args:
    literal_type: xsd:integer
    literal_value: 1906
    source: Georg_Terney
    relation: :hasBirthYear
  AddLiteral (5f0f8906-3f31-4222-8737-d6bd587a0750)
 Call ID: 5f0f8906-3f31-4222-8737-d6bd587a0750
  Args:
    literal_type: xsd:integer
    literal_value: 1977
    source: Georg_Terney
    relation: :hasDeathYear
  AddTriple (fec832b0-c160-4385-b4eb-30a52fbb24d8)
 Call ID: fec832b0-c160-4385-b4eb-30a52fbb24d8
  Args:
    source: Georg_Terney
    relation: :isFatherOf
    target: Inge_Terney
  AssignClass (8a4a0286-1680-4de4-82d4-b9557cbf2a4d)
 Call ID: 8a4a0286-1680-4de4-82d4-b9557cbf2a4d
  Args:
    type: :Woman
    source: Jenny_Kamilla_Hansen
  AssignClass (2500d468-639c-4e19-8849-dc841fbe68e9)
 Call ID: 2500d468-639c-4e19-8849-dc841fbe68e9
  Args:
    source: Jenny_Kamilla_Hansen
    type: :Person
  AddLiteral (199af902-4209-49c2-bfb2-6abb4823d0de)
 Call ID: 199af902-4209-49c2-bfb2-6abb4823d0de
  Args:
    relation: :hasBirthYear
    source: Jenny_Kamilla_Hansen
    literal_type: xsd:integer
    literal_value: 1908
  AddLiteral (f299d30c-93ab-4302-a1ba-fd51feb854d9)
 Call ID: f299d30c-93ab-4302-a1ba-fd51feb854d9
  Args:
    literal_type: xsd:integer
    literal_value: 1990
    relation: :hasDeathYear
    source: Jenny_Kamilla_Hansen
  AddTriple (7f1b4044-5d80-4d9b-9ecc-edb1ad56696c)
 Call ID: 7f1b4044-5d80-4d9b-9ecc-edb1ad56696c
  Args:
    target: Inge_Terney
    relation: :isMotherOf
    source: Jenny_Kamilla_Hansen
  AssignClass (65aaa4c0-23a4-4d4f-9b48-bff7f7ba8efd)
 Call ID: 65aaa4c0-23a4-4d4f-9b48-bff7f7ba8efd
  Args:
    source: Sussie_Hjorhøy-Pedersen
    type: :Woman
  AssignClass (43037298-d697-45f8-94b7-a9dabe812db9)
 Call ID: 43037298-d697-45f8-94b7-a9dabe812db9
  Args:
    source: Sussie_Hjorhøy-Pedersen
    type: :Person
  AddLiteral (a8085545-8cc2-45d3-99e3-920a5e1f9007)
 Call ID: a8085545-8cc2-45d3-99e3-920a5e1f9007
  Args:
    source: Sussie_Hjorhøy-Pedersen
    relation: :hasBirthYear
    literal_value: 1950
    literal_type: xsd:integer
  AssignClass (9a85ccc7-72dd-43d1-a7b5-58fbfdd96880)
 Call ID: 9a85ccc7-72dd-43d1-a7b5-58fbfdd96880
  Args:
    type: :Man
    source: Frederick_Walter_Pedersen
  AssignClass (cf2d25c2-4ef4-471d-88cf-f4c17f18c458)
 Call ID: cf2d25c2-4ef4-471d-88cf-f4c17f18c458
  Args:
    source: Frederick_Walter_Pedersen
    type: :Person
  AddTriple (9344014d-ac55-4e62-8fdd-4a20fd5c22ec)
 Call ID: 9344014d-ac55-4e62-8fdd-4a20fd5c22ec
  Args:
    source: Frederick_Walter_Pedersen
    target: Sussie_Hjorhøy-Pedersen
    relation: :isFatherOf
  AssignClass (b35ae92a-b3ac-49de-95b9-b88a701b2993)
 Call ID: b35ae92a-b3ac-49de-95b9-b88a701b2993
  Args:
    type: :Woman
    source: Ruth_Hjorhøy
  AssignClass (a15cb929-6f6a-4712-996c-204f4fe51163)
 Call ID: a15cb929-6f6a-4712-996c-204f4fe51163
  Args:
    source: Ruth_Hjorhøy
    type: :Person
  AddTriple (99351263-bb04-4ece-b762-58237fb99a6e)
 Call ID: 99351263-bb04-4ece-b762-58237fb99a6e
  Args:
    relation: :isMotherOf
    target: Sussie_Hjorhøy-Pedersen
    source: Ruth_Hjorhøy
  AssignClass (7c29b552-5795-422e-aa11-7c8b481bcacb)
 Call ID: 7c29b552-5795-422e-aa11-7c8b481bcacb
  Args:
    type: :Man
    source: Leopold_Rosanes_af_Rosenborg
  AssignClass (ce5a9eb8-03df-4720-b2ca-c8e29ead35b6)
 Call ID: ce5a9eb8-03df-4720-b2ca-c8e29ead35b6
  Args:
    type: :Person
    source: Leopold_Rosanes_af_Rosenborg
  Finish (660696ae-8002-4d0d-94b1-c0a2add7c1ca)
 Call ID: 660696ae-8002-4d0d-94b1-c0a2add7c1ca
  Args: