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
Dom Luís Filipe, Prince Royal of Portugal, Duke of Braganza (.mw-parser-output .IPA-label-small{font-size:85%}.mw-parser-output .references .IPA-label-small,.mw-parser-output .infobox .IPA-label-small,.mw-parser-output .navbox .IPA-label-small{font-size:100%}Portuguese pronunciation: ; 21 March 1887 – 1 February 1908) was the eldest son and heir apparent of King Carlos I of Portugal until his assassination.
Born in 1887, when his father was still Prince Royal, he was styled Prince of Beira at birth.
After his paternal grandfather King Luís I of Portugal died, he became Prince Royal of Portugal and Duke of Braganza as heir apparent to the throne.
Following the Lisbon Regicide that saw him and his father killed, his younger brother Manuel II became King of Portugal.
Early life

Luís Filipe Maria Carlos Amélio Fernando Víctor Manuel António Lourenço Miguel Rafael Gabriel Gonzaga Xavier Francisco de Assis Bento was born in Lisbon, the elder son of Carlos, Prince Royal of Portugal (later King Carlos I of Portugal), and Princess Amélie d'Orléans, a member of the House of Braganza.
Two years after his birth, Dom Luís Filipe inherited all his father's royal princely titles when his father became king.
He was himself re-styled Prince Royal, and at the same time inherited the Dukedom of Braganza (as 21st Duke), which brought with it the largest private fortune in Portugal at that time, completely at the disposal of the heir to the Portuguese crown.
In 1907, the Prince Royal acted as regent of the kingdom while his father was outside the country.
The same year he made a very successful official visit to the Portuguese colonies in Africa, the first member of the royal family ever to visit them.
Dom Luís Filipe was the pupil of the African war hero Mouzinho de Albuquerque, and like all the Braganzas, showed many aptitudes in the arts, besides his pursuing a military education.
Around the time of Dom Luís Filipe's assassination, negotiations for marriage to his cousin Princess Patricia of Connaught were underway.
Princess Patricia was the granddaughter of Queen Victoria of the United Kingdom and Prince Albert of Saxe-Coburg and Gotha, the daughter of British Prince Arthur, Duke of Connaught and Strathearn, and Princess Louise Margaret of Prussia.
Lisbon Regicide

On 1 February 1908, Luís Filipe and his family were returning to Lisbon from Vila Viçosa Palace.
Alfredo Luís da Costa and Manuel Buiça, two members of a revolutionary society called the Carbonária, shot at all the royal family, hitting his father King Carlos, Luís Filipe, and his younger brother Infante Manuel, Duke of Beja.
Carlos I died immediately, while Luís Filipe lived for another twenty minutes.
Manuel survived the attack, having only been shot in the arm, while the queen was unharmed.
Manuel succeeded to the throne as Manuel II.
Luís Filipe is buried next to his father and forefathers in the Royal Pantheon of the House of Braganza in Lisbon.
His younger brother, King Manuel II of Portugal, and his mother, Queen Maria Amélia, are buried opposite.
On 5 October 1910, the monarchy under the reign of his surviving younger brother, Manuel II, was overthrown in a military coup and the First Portuguese Republic was established.
Honours

Domestic

Foreign

Arms

Luis Filipe bore as heir to the throne the arms of his father; differenced by a Label of three points Or.



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
  AssignClass (7628a87b-d7fd-4f54-ac4a-614d3e63c2fc)
 Call ID: 7628a87b-d7fd-4f54-ac4a-614d3e63c2fc
  Args:
    source: :LuisFilipe
    type: :Man
  AssignClass (11e25aa5-7d40-410e-8dbe-4bce9a1f1361)
 Call ID: 11e25aa5-7d40-410e-8dbe-4bce9a1f1361
  Args:
    type: :Person
    source: :LuisFilipe
  AddLiteral (b32610b7-213e-4488-bd61-2550c06beea1)
 Call ID: b32610b7-213e-4488-bd61-2550c06beea1
  Args:
    literal_value: 1887
    literal_type: xsd:integer
    source: :LuisFilipe
    relation: :hasBirthYear
  AddLiteral (cc644cd0-e466-44c2-a372-ef4bcfa16ab2)
 Call ID: cc644cd0-e466-44c2-a372-ef4bcfa16ab2
  Args:
    relation: :hasDeathYear
    source: :LuisFilipe
    literal_type: xsd:integer
    literal_value: 1908
  AssignClass (3b620f17-d7a2-426c-ba9a-a57d69c34326)
 Call ID: 3b620f17-d7a2-426c-ba9a-a57d69c34326
  Args:
    source: :CarlosI
    type: :Man
  AssignClass (811d57e9-ebed-406a-af46-0440f8adef4f)
 Call ID: 811d57e9-ebed-406a-af46-0440f8adef4f
  Args:
    source: :CarlosI
    type: :Person
  AssignClass (a27c00a8-23ad-43ce-bb12-3ad1f30075ec)
 Call ID: a27c00a8-23ad-43ce-bb12-3ad1f30075ec
  Args:
    type: :Woman
    source: :AmelieOrleans
  AssignClass (07b36a2e-f2cd-4794-84a8-d71b13c0c154)
 Call ID: 07b36a2e-f2cd-4794-84a8-d71b13c0c154
  Args:
    source: :AmelieOrleans
    type: :Person
  AddTriple (de2463a6-609a-4631-b3de-050a86bfb155)
 Call ID: de2463a6-609a-4631-b3de-050a86bfb155
  Args:
    source: :LuisFilipe
    target: :CarlosI
    relation: :hasFather
  AddTriple (05487d93-e37b-477c-bb7f-946c87aed160)
 Call ID: 05487d93-e37b-477c-bb7f-946c87aed160
  Args:
    source: :LuisFilipe
    relation: :hasMother
    target: :AmelieOrleans
  AssignClass (f6f0c812-decc-4439-b638-5349aca6726c)
 Call ID: f6f0c812-decc-4439-b638-5349aca6726c
  Args:
    type: :Man
    source: :ManuelII
  AssignClass (93bc9f70-9869-4ca6-a057-c0ad373f4163)
 Call ID: 93bc9f70-9869-4ca6-a057-c0ad373f4163
  Args:
    type: :Person
    source: :ManuelII
  AddTriple (feb6e7ba-5523-49d1-8bd2-85301f5341b3)
 Call ID: feb6e7ba-5523-49d1-8bd2-85301f5341b3
  Args:
    relation: :hasFather
    target: :CarlosI
    source: :ManuelII
  AddTriple (8b08a5c9-a708-4f2d-8c16-e7fbbe33c1ef)
 Call ID: 8b08a5c9-a708-4f2d-8c16-e7fbbe33c1ef
  Args:
    source: :ManuelII
    target: :AmelieOrleans
    relation: :hasMother
  AddTriple (b7abf9c3-b647-434d-8791-fad845b3a24d)
 Call ID: b7abf9c3-b647-434d-8791-fad845b3a24d
  Args:
    source: :LuisFilipe
    target: :ManuelII
    relation: :isBrotherOf
  AssignClass (8aed265a-3ffa-475c-a4de-1564eaca6a2c)
 Call ID: 8aed265a-3ffa-475c-a4de-1564eaca6a2c
  Args:
    type: :Man
    source: :LuisI
  AssignClass (71ca237a-9c74-4b6f-8d24-4e317efd2af9)
 Call ID: 71ca237a-9c74-4b6f-8d24-4e317efd2af9
  Args:
    type: :Person
    source: :LuisI
  AddTriple (e7add23e-cc15-4ea4-a23b-a048a8b824d0)
 Call ID: e7add23e-cc15-4ea4-a23b-a048a8b824d0
  Args:
    source: :CarlosI
    target: :LuisI
    relation: :hasFather
  AssignClass (33ae6fb4-558c-4ca7-bbda-c74ab1cdeb2f)
 Call ID: 33ae6fb4-558c-4ca7-bbda-c74ab1cdeb2f
  Args:
    type: :Woman
    source: :PatriciaConnaught
  AssignClass (5458f348-f7d4-4df1-b090-8320cae12b1a)
 Call ID: 5458f348-f7d4-4df1-b090-8320cae12b1a
  Args:
    type: :Person
    source: :PatriciaConnaught
  AssignClass (42af602d-2209-4743-91cd-4435745e1930)
 Call ID: 42af602d-2209-4743-91cd-4435745e1930
  Args:
    type: :Woman
    source: :Victoria
  AssignClass (f25467ee-9422-4f40-bb98-1485aae8d8da)
 Call ID: f25467ee-9422-4f40-bb98-1485aae8d8da
  Args:
    source: :Victoria
    type: :Person
  AssignClass (1dcfbea8-acb7-491f-a912-800a355f9fe3)
 Call ID: 1dcfbea8-acb7-491f-a912-800a355f9fe3
  Args:
    source: :AlbertSaxeCoburgGotha
    type: :Man
  AssignClass (7b53a2a7-1636-4fee-a7bd-528f3420e220)
 Call ID: 7b53a2a7-1636-4fee-a7bd-528f3420e220
  Args:
    source: :AlbertSaxeCoburgGotha
    type: :Person
  AssignClass (9b8a34f0-cf07-418f-b1bd-cc001eeeccff)
 Call ID: 9b8a34f0-cf07-418f-b1bd-cc001eeeccff
  Args:
    source: :ArthurConnaught
    type: :Man
  AssignClass (ad4172dc-5081-4bc4-b543-95a3e5e107b7)
 Call ID: ad4172dc-5081-4bc4-b543-95a3e5e107b7
  Args:
    type: :Person
    source: :ArthurConnaught
  AssignClass (8ce7761f-8200-42eb-a460-5216bfc44bc8)
 Call ID: 8ce7761f-8200-42eb-a460-5216bfc44bc8
  Args:
    source: :LouiseMargaretPrussia
    type: :Woman
  AssignClass (509d87f5-84c5-4c92-91b9-41602f3d285a)
 Call ID: 509d87f5-84c5-4c92-91b9-41602f3d285a
  Args:
    source: :LouiseMargaretPrussia
    type: :Person
  AddTriple (827cafae-44a6-4b05-8ff5-063099d17b4e)
 Call ID: 827cafae-44a6-4b05-8ff5-063099d17b4e
  Args:
    source: :PatriciaConnaught
    relation: :hasFather
    target: :ArthurConnaught
  AddTriple (537c265b-e764-4a57-80a4-4eda01a55256)
 Call ID: 537c265b-e764-4a57-80a4-4eda01a55256
  Args:
    relation: :hasMother
    target: :LouiseMargaretPrussia
    source: :PatriciaConnaught
  AddTriple (8997cea1-5a09-4f53-aa83-088a4fff31d8)
 Call ID: 8997cea1-5a09-4f53-aa83-088a4fff31d8
  Args:
    target: :AlbertSaxeCoburgGotha
    relation: :hasFather
    source: :ArthurConnaught
  AddTriple (2cf6a648-29ab-4473-81fc-1899ad46346b)
 Call ID: 2cf6a648-29ab-4473-81fc-1899ad46346b
  Args:
    source: :ArthurConnaught
    relation: :hasMother
    target: :Victoria
  Finish (4a382efe-c1a7-47c8-9806-a6187fdb532c)
 Call ID: 4a382efe-c1a7-47c8-9806-a6187fdb532c
  Args: