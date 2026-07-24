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
  AssignClass (b8186085-6c9a-402f-9ea3-1a6be3cb1c0b)
 Call ID: b8186085-6c9a-402f-9ea3-1a6be3cb1c0b
  Args:
    type: :Man
    source: Ingolf_of_Rosenborg
  AssignClass (ab64a1fd-0c2b-4184-ae69-a317c713cbaf)
 Call ID: ab64a1fd-0c2b-4184-ae69-a317c713cbaf
  Args:
    type: :Person
    source: Ingolf_of_Rosenborg
  AddLiteral (fd2b035c-8f8a-4c53-8429-aa271c49b905)
 Call ID: fd2b035c-8f8a-4c53-8429-aa271c49b905
  Args:
    relation: :hasBirthYear
    source: Ingolf_of_Rosenborg
    literal_type: xsd:integer
    literal_value: 1940
  AddLiteral (98b342dc-9db0-4223-9bb8-6feddcccef3b)
 Call ID: 98b342dc-9db0-4223-9bb8-6feddcccef3b
  Args:
    literal_value: Prince Ingolf of Denmark
    literal_type: xsd:string
    source: Ingolf_of_Rosenborg
    relation: :formerlyKnownAs
  AssignClass (528751d3-ae5b-40cc-8421-f731942f8e4e)
 Call ID: 528751d3-ae5b-40cc-8421-f731942f8e4e
  Args:
    type: :Man
    source: Christian_X_of_Denmark
  AssignClass (7e4fbabf-d341-4468-b14a-0a8a99f5353c)
 Call ID: 7e4fbabf-d341-4468-b14a-0a8a99f5353c
  Args:
    type: :Person
    source: Christian_X_of_Denmark
  AssignClass (16523e71-7498-4bbe-9724-42f376333ee4)
 Call ID: 16523e71-7498-4bbe-9724-42f376333ee4
  Args:
    type: :Man
    source: Prince_Knud
  AssignClass (e9896b1a-3cba-45d3-b023-9d418a83c416)
 Call ID: e9896b1a-3cba-45d3-b023-9d418a83c416
  Args:
    type: :Person
    source: Prince_Knud
  AddTriple (987d5ff5-9d39-4e16-bd3d-2f43ff370fc4)
 Call ID: 987d5ff5-9d39-4e16-bd3d-2f43ff370fc4
  Args:
    source: Prince_Knud
    relation: :isFatherOf
    target: Ingolf_of_Rosenborg
  AddTriple (618e15f8-6fcc-4fb0-b9bf-7c635e4861e4)
 Call ID: 618e15f8-6fcc-4fb0-b9bf-7c635e4861e4
  Args:
    target: Prince_Knud
    relation: :isFatherOf
    source: Christian_X_of_Denmark
  AssignClass (bd7b5417-17fe-48e4-96ec-b67482abc907)
 Call ID: bd7b5417-17fe-48e4-96ec-b67482abc907
  Args:
    type: :Man
    source: King_Frederik_IX
  AssignClass (419e6835-e7f8-4ce4-8b19-294ec0d5d915)
 Call ID: 419e6835-e7f8-4ce4-8b19-294ec0d5d915
  Args:
    type: :Person
    source: King_Frederik_IX
  AddTriple (d21ca376-92c2-452a-b70c-167604fd9c93)
 Call ID: d21ca376-92c2-452a-b70c-167604fd9c93
  Args:
    relation: :isBrotherOf
    source: Prince_Knud
    target: King_Frederik_IX
  AssignClass (06dda938-37aa-44cc-917e-449975191de4)
 Call ID: 06dda938-37aa-44cc-917e-449975191de4
  Args:
    type: :Man
    source: Christian_of_Rosenborg
  AssignClass (2b4a8c41-7eb1-420a-b998-087613a8de04)
 Call ID: 2b4a8c41-7eb1-420a-b998-087613a8de04
  Args:
    type: :Person
    source: Christian_of_Rosenborg
  AddTriple (398b1c83-27b4-48f7-a515-94500ab64a15)
 Call ID: 398b1c83-27b4-48f7-a515-94500ab64a15
  Args:
    target: Ingolf_of_Rosenborg
    relation: :isBrotherOf
    source: Christian_of_Rosenborg
  AddTriple (441a0c9d-9815-4bc3-bac8-c5ccc3fe1e1a)
 Call ID: 441a0c9d-9815-4bc3-bac8-c5ccc3fe1e1a
  Args:
    relation: :hasFather
    source: Christian_of_Rosenborg
    target: Prince_Knud
  AssignClass (d5f31a5b-45db-4e04-91d8-50ffa9e95435)
 Call ID: d5f31a5b-45db-4e04-91d8-50ffa9e95435
  Args:
    type: :Woman
    source: Inge_Terney
  AssignClass (02a93a42-0c46-48ba-b699-de943f850f3f)
 Call ID: 02a93a42-0c46-48ba-b699-de943f850f3f
  Args:
    type: :Person
    source: Inge_Terney
  AddLiteral (27267253-82b9-49b4-aa94-be1128b865e6)
 Call ID: 27267253-82b9-49b4-aa94-be1128b865e6
  Args:
    literal_value: 1968
    literal_type: xsd:integer
    source: Ingolf_of_Rosenborg
    relation: :hasMarriageYear
  AddTriple (709568dd-274b-460b-af64-92bf778fef71)
 Call ID: 709568dd-274b-460b-af64-92bf778fef71
  Args:
    target: Inge_Terney
    relation: :hasRelation
    source: Ingolf_of_Rosenborg
  AssignClass (5ad1e1df-4fd5-4189-86d9-9ede6ff7eeea)
 Call ID: 5ad1e1df-4fd5-4189-86d9-9ede6ff7eeea
  Args:
    type: :Man
    source: Georg_Terney
  AssignClass (bcfc091e-c2a3-4ba5-b675-a6522f40b833)
 Call ID: bcfc091e-c2a3-4ba5-b675-a6522f40b833
  Args:
    type: :Person
    source: Georg_Terney
  AssignClass (14c060e9-1f89-4c1a-a412-517323128c6f)
 Call ID: 14c060e9-1f89-4c1a-a412-517323128c6f
  Args:
    type: :Woman
    source: Jenny_Kamilla_Hansen
  AssignClass (8dc8bec8-13b3-4f95-8b28-ec9c91fc210b)
 Call ID: 8dc8bec8-13b3-4f95-8b28-ec9c91fc210b
  Args:
    type: :Person
    source: Jenny_Kamilla_Hansen
  AddTriple (a771e916-758c-4d38-9181-2cc499bbb9ee)
 Call ID: a771e916-758c-4d38-9181-2cc499bbb9ee
  Args:
    target: Inge_Terney
    source: Georg_Terney
    relation: :isFatherOf
  AddTriple (358e995b-2228-4f12-a769-9cdc5215da01)
 Call ID: 358e995b-2228-4f12-a769-9cdc5215da01
  Args:
    target: Inge_Terney
    relation: :isMotherOf
    source: Jenny_Kamilla_Hansen
  AssignClass (87f118a8-0caf-4072-a1d6-5d38e823847e)
 Call ID: 87f118a8-0caf-4072-a1d6-5d38e823847e
  Args:
    type: :Woman
    source: Sussie_Hjorhoy-Pedersen
  AssignClass (7982af3e-8989-46b8-b118-2b325ffe57c8)
 Call ID: 7982af3e-8989-46b8-b118-2b325ffe57c8
  Args:
    type: :Person
    source: Sussie_Hjorhoy-Pedersen
  AddLiteral (ce59accd-82fe-4d0d-8836-0f6454e81c88)
 Call ID: ce59accd-82fe-4d0d-8836-0f6454e81c88
  Args:
    literal_type: xsd:integer
    literal_value: 1998
    relation: :hasMarriageYear
    source: Ingolf_of_Rosenborg
  AddTriple (1ee967f2-2b0b-4ac5-b604-9b4a1c603152)
 Call ID: 1ee967f2-2b0b-4ac5-b604-9b4a1c603152
  Args:
    target: Sussie_Hjorhoy-Pedersen
    source: Ingolf_of_Rosenborg
    relation: :hasRelation
  AssignClass (0a6986fa-c93b-4d9e-9188-64c1d20d057a)
 Call ID: 0a6986fa-c93b-4d9e-9188-64c1d20d057a
  Args:
    type: :Man
    source: Frederick_Walter_Pedersen
  AssignClass (c5850db9-b88f-4c06-a488-b67bf3ddf1c9)
 Call ID: c5850db9-b88f-4c06-a488-b67bf3ddf1c9
  Args:
    type: :Person
    source: Frederick_Walter_Pedersen
  AssignClass (6457275a-c435-4053-9ac9-94aab77a999b)
 Call ID: 6457275a-c435-4053-9ac9-94aab77a999b
  Args:
    type: :Woman
    source: Ruth_Hjorhoy
  AssignClass (e036f4ec-b3ff-409d-9d57-2fd585fb9ab4)
 Call ID: e036f4ec-b3ff-409d-9d57-2fd585fb9ab4
  Args:
    type: :Person
    source: Ruth_Hjorhoy
  AddTriple (f436daf7-2b2b-4171-9d53-e0cbaf4b9bd1)
 Call ID: f436daf7-2b2b-4171-9d53-e0cbaf4b9bd1
  Args:
    target: Sussie_Hjorhoy-Pedersen
    relation: :isFatherOf
    source: Frederick_Walter_Pedersen
  AddTriple (63a54a2e-afea-412b-9ca6-38044bfb1872)
 Call ID: 63a54a2e-afea-412b-9ca6-38044bfb1872
  Args:
    target: Sussie_Hjorhoy-Pedersen
    source: Ruth_Hjorhoy
    relation: :isMotherOf
  AssignClass (2a9d2793-7dc7-4729-8610-87d321a65807)
 Call ID: 2a9d2793-7dc7-4729-8610-87d321a65807
  Args:
    type: :Man
    source: Leopold_Rosanes_af_Rosenborg
  AssignClass (3dd5796c-b481-48be-9edc-8180019a9dee)
 Call ID: 3dd5796c-b481-48be-9edc-8180019a9dee
  Args:
    type: :Person
    source: Leopold_Rosanes_af_Rosenborg
  AddTriple (dd51ab90-bfa0-4c3c-8dfe-d988f0fe17c9)
 Call ID: dd51ab90-bfa0-4c3c-8dfe-d988f0fe17c9
  Args:
    target: Christian_of_Rosenborg
    relation: :isSonOf
    source: Leopold_Rosanes_af_Rosenborg
  AssignClass (c5a8e9c0-812b-4b7b-9811-2b88ad88a1a1)
 Call ID: c5a8e9c0-812b-4b7b-9811-2b88ad88a1a1
  Args:
    type: :Woman
    source: Princess_Elisabeth_of_Denmark
  AssignClass (dd1e0b7d-6c0f-4eea-82d5-7cd5b89fa641)
 Call ID: dd1e0b7d-6c0f-4eea-82d5-7cd5b89fa641
  Args:
    type: :Person
    source: Princess_Elisabeth_of_Denmark
  AddTriple (7dbdc718-c5f5-45ac-96c1-bd8f72e9e829)
 Call ID: 7dbdc718-c5f5-45ac-96c1-bd8f72e9e829
  Args:
    target: Ingolf_of_Rosenborg
    source: Princess_Elisabeth_of_Denmark
    relation: :isSisterOf
  Finish (70e833fc-e15c-4d0a-a0a3-2e7c11afd5e5)
 Call ID: 70e833fc-e15c-4d0a-a0a3-2e7c11afd5e5
  Args: