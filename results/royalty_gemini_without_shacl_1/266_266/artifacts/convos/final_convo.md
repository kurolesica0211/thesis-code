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
  AssignClass (5bc2c056-29c3-458a-b81f-6802ada1406c)
 Call ID: 5bc2c056-29c3-458a-b81f-6802ada1406c
  Args:
    source: LuísFilipe
    type: :Man
  AssignClass (30fedb16-d651-4318-a810-8cabed7c8508)
 Call ID: 30fedb16-d651-4318-a810-8cabed7c8508
  Args:
    type: :Person
    source: LuísFilipe
  AddLiteral (106ab615-0c7e-476f-bfe0-a67ce5d1c292)
 Call ID: 106ab615-0c7e-476f-bfe0-a67ce5d1c292
  Args:
    relation: :hasBirthYear
    source: LuísFilipe
    literal_value: 1887
    literal_type: xsd:integer
  AddLiteral (a30a1c82-8569-4907-b3a7-52d1b8ffe5f0)
 Call ID: a30a1c82-8569-4907-b3a7-52d1b8ffe5f0
  Args:
    literal_type: xsd:integer
    literal_value: 1908
    relation: :hasDeathYear
    source: LuísFilipe
  AssignClass (810b0c69-9aa4-47b5-9a58-e32806de67f7)
 Call ID: 810b0c69-9aa4-47b5-9a58-e32806de67f7
  Args:
    type: :Man
    source: CarlosI
  AssignClass (2286f66b-00e2-4e53-8fc6-260747d443cd)
 Call ID: 2286f66b-00e2-4e53-8fc6-260747d443cd
  Args:
    source: CarlosI
    type: :Person
  AssignClass (81de5be3-fb1c-4160-8a29-3429db41fa07)
 Call ID: 81de5be3-fb1c-4160-8a29-3429db41fa07
  Args:
    source: AmélieDOrléans
    type: :Woman
  AssignClass (2cabfbdb-c03c-4c68-b8c5-bc5c6520458d)
 Call ID: 2cabfbdb-c03c-4c68-b8c5-bc5c6520458d
  Args:
    type: :Person
    source: AmélieDOrléans
  AddTriple (ec8e78b2-42fa-4a7a-8abc-dcff7737ff7e)
 Call ID: ec8e78b2-42fa-4a7a-8abc-dcff7737ff7e
  Args:
    target: CarlosI
    source: LuísFilipe
    relation: :hasFather
  AddTriple (93aee625-6166-4c15-ae03-7c8615dbdccf)
 Call ID: 93aee625-6166-4c15-ae03-7c8615dbdccf
  Args:
    target: AmélieDOrléans
    source: LuísFilipe
    relation: :hasMother
  AssignClass (5f931db6-c6e5-4a69-8e73-accc2fac87af)
 Call ID: 5f931db6-c6e5-4a69-8e73-accc2fac87af
  Args:
    source: LuísI
    type: :Man
  AssignClass (b40e31c1-e627-4f46-bf47-94220804c633)
 Call ID: b40e31c1-e627-4f46-bf47-94220804c633
  Args:
    source: LuísI
    type: :Person
  AddTriple (107aa6f7-919c-45d7-9b8c-f87d249225d5)
 Call ID: 107aa6f7-919c-45d7-9b8c-f87d249225d5
  Args:
    relation: :hasFather
    source: CarlosI
    target: LuísI
  AssignClass (82793008-bdb4-4b00-ad54-fd9aad9ec468)
 Call ID: 82793008-bdb4-4b00-ad54-fd9aad9ec468
  Args:
    type: :Man
    source: ManuelII
  AssignClass (6bb9f2cf-d966-4fa9-8f5b-18d286ca2cd4)
 Call ID: 6bb9f2cf-d966-4fa9-8f5b-18d286ca2cd4
  Args:
    type: :Person
    source: ManuelII
  AddTriple (2afbe9bc-8f70-4872-b8ee-5c7a877367c0)
 Call ID: 2afbe9bc-8f70-4872-b8ee-5c7a877367c0
  Args:
    source: ManuelII
    relation: :hasFather
    target: CarlosI
  AddTriple (04804b8a-64c5-4c29-b198-5d57d15ae0ea)
 Call ID: 04804b8a-64c5-4c29-b198-5d57d15ae0ea
  Args:
    source: ManuelII
    relation: :hasMother
    target: AmélieDOrléans
  AssignClass (03d77183-9ef9-48d1-8c63-fa6ac7ea0d11)
 Call ID: 03d77183-9ef9-48d1-8c63-fa6ac7ea0d11
  Args:
    source: PatriciaOfConnaught
    type: :Woman
  AssignClass (398b9a1a-00f9-44b5-9902-8e24e9e19382)
 Call ID: 398b9a1a-00f9-44b5-9902-8e24e9e19382
  Args:
    source: PatriciaOfConnaught
    type: :Person
  AssignClass (e837265f-03e7-4b9d-98b6-90c41dc955d0)
 Call ID: e837265f-03e7-4b9d-98b6-90c41dc955d0
  Args:
    type: :Woman
    source: QueenVictoria
  AssignClass (625fbe02-b0c7-46e3-ae86-12d68b2d238d)
 Call ID: 625fbe02-b0c7-46e3-ae86-12d68b2d238d
  Args:
    type: :Person
    source: QueenVictoria
  AssignClass (f5b1616c-3772-45ab-a13b-077028970044)
 Call ID: f5b1616c-3772-45ab-a13b-077028970044
  Args:
    source: PrinceAlbert
    type: :Man
  AssignClass (451a9776-b9cb-4fc0-8084-3560ce0d6f16)
 Call ID: 451a9776-b9cb-4fc0-8084-3560ce0d6f16
  Args:
    source: PrinceAlbert
    type: :Person
  AssignClass (9e9a1abc-f4a3-4c09-a422-f271ba9849e4)
 Call ID: 9e9a1abc-f4a3-4c09-a422-f271ba9849e4
  Args:
    source: PrinceArthur
    type: :Man
  AssignClass (78c27bd3-898f-4146-8691-f3b9babce7c5)
 Call ID: 78c27bd3-898f-4146-8691-f3b9babce7c5
  Args:
    type: :Person
    source: PrinceArthur
  AssignClass (177d9e70-ad19-483a-9b91-bb369bcd6dc3)
 Call ID: 177d9e70-ad19-483a-9b91-bb369bcd6dc3
  Args:
    type: :Woman
    source: LouiseMargaretOfPrussia
  AssignClass (6eefcfdb-1543-4fc6-bd2d-d5df28265c1a)
 Call ID: 6eefcfdb-1543-4fc6-bd2d-d5df28265c1a
  Args:
    source: LouiseMargaretOfPrussia
    type: :Person
  AddTriple (092fd974-9d9b-4647-a55a-b9116369f4da)
 Call ID: 092fd974-9d9b-4647-a55a-b9116369f4da
  Args:
    source: PatriciaOfConnaught
    relation: :hasFather
    target: PrinceArthur
  AddTriple (f71c6a7c-196e-44de-9450-d9325c263bbc)
 Call ID: f71c6a7c-196e-44de-9450-d9325c263bbc
  Args:
    source: PatriciaOfConnaught
    relation: :hasMother
    target: LouiseMargaretOfPrussia
  Finish (67b581a9-d441-4fc8-b90f-62faeeea3c24)
 Call ID: 67b581a9-d441-4fc8-b90f-62faeeea3c24
  Args: