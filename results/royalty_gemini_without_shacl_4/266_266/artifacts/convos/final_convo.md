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
  AssignClass (2e90c719-e954-474a-a302-b9ce7aa25468)
 Call ID: 2e90c719-e954-474a-a302-b9ce7aa25468
  Args:
    type: :Man
    source: Luís_Filipe
  AssignClass (e2f5a0b3-f450-4b4a-8a59-b23b073e4657)
 Call ID: e2f5a0b3-f450-4b4a-8a59-b23b073e4657
  Args:
    type: :Person
    source: Luís_Filipe
  AddLiteral (596e59fb-eece-4641-b82b-5ace4cbe2a26)
 Call ID: 596e59fb-eece-4641-b82b-5ace4cbe2a26
  Args:
    literal_value: 1887
    source: Luís_Filipe
    literal_type: xsd:nonNegativeInteger
    relation: :hasBirthYear
  AddLiteral (4d57a340-5912-4809-a4cd-c5c2c5bc5679)
 Call ID: 4d57a340-5912-4809-a4cd-c5c2c5bc5679
  Args:
    relation: :hasDeathYear
    literal_value: 1908
    source: Luís_Filipe
    literal_type: xsd:nonNegativeInteger
  AssignClass (347e11a1-2294-4260-9dc0-54c9c5d70f3d)
 Call ID: 347e11a1-2294-4260-9dc0-54c9c5d70f3d
  Args:
    type: :Man
    source: Carlos_I
  AssignClass (47b0a923-2659-40da-ae0a-43f657d73af8)
 Call ID: 47b0a923-2659-40da-ae0a-43f657d73af8
  Args:
    type: :Person
    source: Carlos_I
  AssignClass (a93ef86e-58c8-4607-929a-4432fa14bd05)
 Call ID: a93ef86e-58c8-4607-929a-4432fa14bd05
  Args:
    type: :Woman
    source: Amélie_dOrléans
  AssignClass (b1bb93a3-61de-44a7-9c78-ea7e56cf6c01)
 Call ID: b1bb93a3-61de-44a7-9c78-ea7e56cf6c01
  Args:
    type: :Person
    source: Amélie_dOrléans
  AddTriple (ed38ea57-868a-448d-b470-2f380cb26041)
 Call ID: ed38ea57-868a-448d-b470-2f380cb26041
  Args:
    source: Luís_Filipe
    relation: :hasFather
    target: Carlos_I
  AddTriple (2f5863b2-fbfc-459d-a3f2-b42b49168adb)
 Call ID: 2f5863b2-fbfc-459d-a3f2-b42b49168adb
  Args:
    target: Amélie_dOrléans
    relation: :hasMother
    source: Luís_Filipe
  AssignClass (7a7b8154-4336-47c9-864c-5d6fa68ebb72)
 Call ID: 7a7b8154-4336-47c9-864c-5d6fa68ebb72
  Args:
    type: :Man
    source: Luís_I
  AssignClass (130a4a6c-42b8-404c-b359-956b6144db08)
 Call ID: 130a4a6c-42b8-404c-b359-956b6144db08
  Args:
    type: :Person
    source: Luís_I
  AddTriple (0e4172b4-74f0-423c-be1c-f2713ab3a748)
 Call ID: 0e4172b4-74f0-423c-be1c-f2713ab3a748
  Args:
    source: Carlos_I
    target: Luís_I
    relation: :hasFather
  AssignClass (7c72b8ef-f6b0-43b9-b641-aaddf52ea9a1)
 Call ID: 7c72b8ef-f6b0-43b9-b641-aaddf52ea9a1
  Args:
    type: :Man
    source: Manuel_II
  AssignClass (b1ddd1b5-467f-4c60-9cda-a452bf4a02c3)
 Call ID: b1ddd1b5-467f-4c60-9cda-a452bf4a02c3
  Args:
    type: :Person
    source: Manuel_II
  AddTriple (c301e9a9-df2f-4672-bb76-521f3913248f)
 Call ID: c301e9a9-df2f-4672-bb76-521f3913248f
  Args:
    source: Manuel_II
    target: Carlos_I
    relation: :hasFather
  AddTriple (c9cb8284-1286-4570-af71-0de40f7a4748)
 Call ID: c9cb8284-1286-4570-af71-0de40f7a4748
  Args:
    source: Manuel_II
    target: Amélie_dOrléans
    relation: :hasMother
  AddTriple (b4b96e97-79bc-426f-8085-a1cf9700f8bf)
 Call ID: b4b96e97-79bc-426f-8085-a1cf9700f8bf
  Args:
    source: Luís_Filipe
    target: Manuel_II
    relation: :isSiblingOf
  AssignClass (07b8b633-2c97-4ab1-b62f-1188c1af194d)
 Call ID: 07b8b633-2c97-4ab1-b62f-1188c1af194d
  Args:
    type: :Woman
    source: Patricia_of_Connaught
  AssignClass (af418f43-c0f7-4feb-b99e-c3ae443d08c8)
 Call ID: af418f43-c0f7-4feb-b99e-c3ae443d08c8
  Args:
    type: :Person
    source: Patricia_of_Connaught
  AssignClass (2d291842-6a4c-4d57-91e7-ea70825a3583)
 Call ID: 2d291842-6a4c-4d57-91e7-ea70825a3583
  Args:
    type: :Woman
    source: Queen_Victoria
  AssignClass (cffcb07b-d88f-4320-b7a5-9687e50d1697)
 Call ID: cffcb07b-d88f-4320-b7a5-9687e50d1697
  Args:
    type: :Person
    source: Queen_Victoria
  AssignClass (ddd711ed-afb9-4dae-85fe-b0565fa789bd)
 Call ID: ddd711ed-afb9-4dae-85fe-b0565fa789bd
  Args:
    type: :Man
    source: Prince_Albert
  AssignClass (b6830ab0-2841-4a8c-be87-03fc46e951b0)
 Call ID: b6830ab0-2841-4a8c-be87-03fc46e951b0
  Args:
    type: :Person
    source: Prince_Albert
  AssignClass (c5c13041-2e0d-4ecf-a224-62be0527d598)
 Call ID: c5c13041-2e0d-4ecf-a224-62be0527d598
  Args:
    type: :Man
    source: Prince_Arthur
  AssignClass (d276801d-c92e-451a-abc3-99ef7bc34515)
 Call ID: d276801d-c92e-451a-abc3-99ef7bc34515
  Args:
    type: :Person
    source: Prince_Arthur
  AssignClass (06aad4e5-ed05-44a4-8778-ea073e23cae6)
 Call ID: 06aad4e5-ed05-44a4-8778-ea073e23cae6
  Args:
    type: :Woman
    source: Louise_Margaret_of_Prussia
  AssignClass (ad8fec85-88dd-41c2-adb9-1ac2bb09a06e)
 Call ID: ad8fec85-88dd-41c2-adb9-1ac2bb09a06e
  Args:
    type: :Person
    source: Louise_Margaret_of_Prussia
  AddTriple (05c590a8-c2ef-4a16-b673-6134575fca40)
 Call ID: 05c590a8-c2ef-4a16-b673-6134575fca40
  Args:
    source: Patricia_of_Connaught
    target: Prince_Arthur
    relation: :hasFather
  AddTriple (0b4d32bf-14af-4e0f-b3e0-c553a9e1fb89)
 Call ID: 0b4d32bf-14af-4e0f-b3e0-c553a9e1fb89
  Args:
    source: Patricia_of_Connaught
    relation: :hasMother
    target: Louise_Margaret_of_Prussia
  AddTriple (c58991f8-c72e-4e50-8466-975ca1898f8c)
 Call ID: c58991f8-c72e-4e50-8466-975ca1898f8c
  Args:
    relation: :hasMother
    target: Queen_Victoria
    source: Prince_Arthur
  AddTriple (b62466ee-cb08-4b1a-aa72-52ebf0cf5332)
 Call ID: b62466ee-cb08-4b1a-aa72-52ebf0cf5332
  Args:
    target: Prince_Albert
    relation: :hasFather
    source: Prince_Arthur
  Finish (b857f4bd-1a66-498c-b511-97f5bd51af2e)
 Call ID: b857f4bd-1a66-498c-b511-97f5bd51af2e
  Args: