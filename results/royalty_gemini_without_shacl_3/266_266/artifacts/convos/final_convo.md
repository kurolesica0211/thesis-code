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
  AssignClass (29dd8675-4e90-4a75-9a9d-c4544b56c1a7)
 Call ID: 29dd8675-4e90-4a75-9a9d-c4544b56c1a7
  Args:
    type: :Person
    source: :Luís_Filipe
  AssignClass (0393f732-4b6a-4d02-bdc5-564d08a5cabb)
 Call ID: 0393f732-4b6a-4d02-bdc5-564d08a5cabb
  Args:
    source: :Luís_Filipe
    type: :Man
  AddLiteral (20420329-1d28-4bd2-a78b-f3e65e04b006)
 Call ID: 20420329-1d28-4bd2-a78b-f3e65e04b006
  Args:
    literal_value: 1887
    source: :Luís_Filipe
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (56467553-d775-4694-959d-e67d6055703e)
 Call ID: 56467553-d775-4694-959d-e67d6055703e
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: :Luís_Filipe
    literal_value: 1908
  AssignClass (a17a5313-f56f-482c-b32c-942cf5a802a3)
 Call ID: a17a5313-f56f-482c-b32c-942cf5a802a3
  Args:
    type: :Person
    source: :Carlos_I
  AssignClass (e24f6b75-3e60-469e-be08-040cab0dc0c1)
 Call ID: e24f6b75-3e60-469e-be08-040cab0dc0c1
  Args:
    type: :Man
    source: :Carlos_I
  AddTriple (40625c68-c142-4cd1-863a-748f794fee46)
 Call ID: 40625c68-c142-4cd1-863a-748f794fee46
  Args:
    source: :Luís_Filipe
    target: :Carlos_I
    relation: :hasFather
  AssignClass (babc90df-639f-423a-a4be-cbc267b101aa)
 Call ID: babc90df-639f-423a-a4be-cbc267b101aa
  Args:
    type: :Person
    source: :Amélie_dOrléans
  AssignClass (96406533-89b6-47dd-8582-e26acbb4649f)
 Call ID: 96406533-89b6-47dd-8582-e26acbb4649f
  Args:
    type: :Woman
    source: :Amélie_dOrléans
  AddTriple (41a6b934-5158-4e8a-b46a-8b64170d88e7)
 Call ID: 41a6b934-5158-4e8a-b46a-8b64170d88e7
  Args:
    target: :Amélie_dOrléans
    relation: :hasMother
    source: :Luís_Filipe
  AssignClass (9d0a4e96-9d65-4bb8-b0c8-49639534895b)
 Call ID: 9d0a4e96-9d65-4bb8-b0c8-49639534895b
  Args:
    type: :Person
    source: :Luís_I
  AssignClass (9c2bdea3-e2ae-4100-8bb1-857b506f6e43)
 Call ID: 9c2bdea3-e2ae-4100-8bb1-857b506f6e43
  Args:
    source: :Luís_I
    type: :Man
  AddTriple (b1c9eb8e-9ca4-4294-94da-e5af1be40821)
 Call ID: b1c9eb8e-9ca4-4294-94da-e5af1be40821
  Args:
    source: :Carlos_I
    target: :Luís_I
    relation: :hasFather
  AssignClass (2cd1fb3b-92b3-485b-9e26-3cc939476439)
 Call ID: 2cd1fb3b-92b3-485b-9e26-3cc939476439
  Args:
    type: :Person
    source: :Manuel_II
  AssignClass (4c4808f2-4851-4887-89db-070dedb9e529)
 Call ID: 4c4808f2-4851-4887-89db-070dedb9e529
  Args:
    source: :Manuel_II
    type: :Man
  AddTriple (ee4eb104-fc66-41da-b7fb-19caf443e00e)
 Call ID: ee4eb104-fc66-41da-b7fb-19caf443e00e
  Args:
    target: :Luís_Filipe
    relation: :isBrotherOf
    source: :Manuel_II
  AddTriple (99ff74fc-6c73-40b7-89f8-b3fb537f8d26)
 Call ID: 99ff74fc-6c73-40b7-89f8-b3fb537f8d26
  Args:
    source: :Manuel_II
    relation: :hasFather
    target: :Carlos_I
  AddTriple (c9fe26ab-3532-4544-afb6-443b7b43559d)
 Call ID: c9fe26ab-3532-4544-afb6-443b7b43559d
  Args:
    relation: :hasMother
    target: :Amélie_dOrléans
    source: :Manuel_II
  AssignClass (ecd6e4d0-4dca-4bdc-b69f-c6012d13891c)
 Call ID: ecd6e4d0-4dca-4bdc-b69f-c6012d13891c
  Args:
    type: :Person
    source: :Patricia_of_Connaught
  AssignClass (e0b7fe2f-b36e-461b-85e9-145325250a66)
 Call ID: e0b7fe2f-b36e-461b-85e9-145325250a66
  Args:
    type: :Woman
    source: :Patricia_of_Connaught
  AssignClass (4a9ae233-ee42-4847-bb2c-9cbb2835c4bd)
 Call ID: 4a9ae233-ee42-4847-bb2c-9cbb2835c4bd
  Args:
    type: :Person
    source: :Victoria_of_the_United_Kingdom
  AssignClass (ed2c4b0f-e900-4b31-8118-b485a63c78e4)
 Call ID: ed2c4b0f-e900-4b31-8118-b485a63c78e4
  Args:
    type: :Woman
    source: :Victoria_of_the_United_Kingdom
  AssignClass (ac1a6ce2-a26c-4048-b6f5-624c4855a0cd)
 Call ID: ac1a6ce2-a26c-4048-b6f5-624c4855a0cd
  Args:
    source: :Albert_of_Saxe-Coburg_and_Gotha
    type: :Person
  AssignClass (fa34614a-dfb6-46d3-9e91-a269b712efa8)
 Call ID: fa34614a-dfb6-46d3-9e91-a269b712efa8
  Args:
    source: :Albert_of_Saxe-Coburg_and_Gotha
    type: :Man
  AssignClass (82a9d22f-4f82-47b0-9e9c-4a281c486bee)
 Call ID: 82a9d22f-4f82-47b0-9e9c-4a281c486bee
  Args:
    type: :Person
    source: :Arthur_Duke_of_Connaught_and_Strathearn
  AssignClass (1da16486-0619-4ba8-8aca-e403867879d4)
 Call ID: 1da16486-0619-4ba8-8aca-e403867879d4
  Args:
    type: :Man
    source: :Arthur_Duke_of_Connaught_and_Strathearn
  AssignClass (10dc0dbf-a507-4354-86cd-9bd7536b21df)
 Call ID: 10dc0dbf-a507-4354-86cd-9bd7536b21df
  Args:
    source: :Louise_Margaret_of_Prussia
    type: :Person
  AssignClass (aa7e33a9-f658-40ed-9e58-60d237737344)
 Call ID: aa7e33a9-f658-40ed-9e58-60d237737344
  Args:
    type: :Woman
    source: :Louise_Margaret_of_Prussia
  AddTriple (82da9a02-868a-4757-83bb-ba713e888a8e)
 Call ID: 82da9a02-868a-4757-83bb-ba713e888a8e
  Args:
    source: :Patricia_of_Connaught
    relation: :hasFather
    target: :Arthur_Duke_of_Connaught_and_Strathearn
  AddTriple (26b27ee9-0b61-4552-a02d-2e85f766d461)
 Call ID: 26b27ee9-0b61-4552-a02d-2e85f766d461
  Args:
    source: :Patricia_of_Connaught
    relation: :hasMother
    target: :Louise_Margaret_of_Prussia
  Finish (50d5d40a-9f57-4725-8dae-8e36303c9fc3)
 Call ID: 50d5d40a-9f57-4725-8dae-8e36303c9fc3
  Args: