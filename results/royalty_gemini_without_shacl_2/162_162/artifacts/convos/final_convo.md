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
Amélie of Orléans (French: Marie Amélie Louise Hélène; 28 September 1865 – 25 October 1951) was the last Queen of Portugal as the wife of Carlos I of Portugal.
She was regent of Portugal during the absence of her husband in 1895.
She was the eldest daughter of Prince Philippe, Count of Paris, and Princess Marie Isabelle d'Orléans, and a "Princess of Orléans" by birth.
Amélie's paternal grandparents were Prince Ferdinand Philippe, Duke of Orléans, and Duchess Helena of Mecklenburg-Schwerin.
Her maternal grandparents were Prince Antoine, Duke of Montpensier, and the Infanta Luisa Fernanda of Spain.
The Dukes of Orléans and Montpensier were siblings, both sons of King Louis-Philippe I of France, and Maria Amalia of the Two Sicilies.
Marriage and issue

On 22 May 1886, Amélie married Carlos, Prince Royal of Portugal.
He was the eldest son of King Luís I of Portugal and Maria Pia of Savoy.
At first, the marriage was not popular and Queen Maria Pia was expecting to marry Carlos to Archduchess Marie Valerie of Austria, Princess Mathilde of Saxony, Princess Viktoria of Prussia or Princess Victoria of Wales.
However, Amélie and Carlos came to live quite harmoniously with each other.
They had three children:


Queen consort

On 19 October 1889, King Luís died and Carlos succeeded him on the throne.
Amélie became the new Queen consort of Portugal.
Amélie played an active role as a queen, and somewhat softened the growing criticism towards the monarchy with her personal popularity, though she did receive some criticism for her expenses.
In 1892, Pope Leo XIII gave a Golden Rose to Amélie.
On their way to the Palace of Necessidades, the carriage carrying Carlos and his family passed through the Rua do Arsenal.
The King died immediately, his heir Prince Dom Luís Filipe was mortally wounded and Infante Dom Manuel was hit in the arm.
Queen Amélie remained unharmed as she tried to defend her youngest son, the new king Manuel II, with the flower bouquet she kept in her hand.
About twenty minutes later, Prince Luís Filipe died and the next day Manuel was acclaimed King of Portugal, the last of the Braganza dynasty.
Manuel II was deposed in a military coup, later known as the 5 October 1910 revolution, which resulted in the establishment of the Portuguese First Republic.
Queen Amélie left Portugal with the rest of the royal family and went into exile.
During the Second World War, the Portuguese government invited her to return to Portugal, but she declined the offer.
She visited Portugal for the last time in 1945.
Later years and death

In 1949, Amélie left her Portuguese possessions to her godson, Duarte Pio, Duke of Braganza, at the request of Prime Minister António de Oliveira Salazar.
She was given a state funeral and buried at the Pantheon of the Braganzas located in the Monastery of São Vicente de Fora, in Lisbon, Portugal.



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
  AssignClass (5a3ae4f2-8e13-449c-8c0b-e7ca4ede763d)
 Call ID: 5a3ae4f2-8e13-449c-8c0b-e7ca4ede763d
  Args:
    type: :Woman
    source: Amélie_of_Orléans
  AssignClass (dc84157c-d9a6-4d92-9d1a-3478f36b0229)
 Call ID: dc84157c-d9a6-4d92-9d1a-3478f36b0229
  Args:
    type: :Person
    source: Amélie_of_Orléans
  AddLiteral (45f6e54f-e3ec-4239-b424-ba1eb116d76c)
 Call ID: 45f6e54f-e3ec-4239-b424-ba1eb116d76c
  Args:
    literal_value: Marie Amélie Louise Hélène
    source: Amélie_of_Orléans
    literal_type: xsd:string
    relation: :alsoKnownAs
  AddLiteral (8fe7337c-edf6-4e26-8a08-5bd696b5bc1c)
 Call ID: 8fe7337c-edf6-4e26-8a08-5bd696b5bc1c
  Args:
    relation: :hasBirthYear
    literal_value: 1865
    source: Amélie_of_Orléans
    literal_type: xsd:integer
  AddLiteral (1c7ebeb4-006f-4e2f-8c33-5c7b45166513)
 Call ID: 1c7ebeb4-006f-4e2f-8c33-5c7b45166513
  Args:
    literal_value: 1951
    source: Amélie_of_Orléans
    literal_type: xsd:integer
    relation: :hasDeathYear
  AssignClass (41ebe0f4-3338-4d60-953d-ea286625ba10)
 Call ID: 41ebe0f4-3338-4d60-953d-ea286625ba10
  Args:
    type: :Man
    source: Carlos_I_of_Portugal
  AssignClass (2049c0ff-9537-4162-ace7-7a7320f6e7b3)
 Call ID: 2049c0ff-9537-4162-ace7-7a7320f6e7b3
  Args:
    type: :Person
    source: Carlos_I_of_Portugal
  AddLiteral (66238faa-bd9b-40c8-8370-213d4a33252f)
 Call ID: 66238faa-bd9b-40c8-8370-213d4a33252f
  Args:
    literal_type: xsd:integer
    literal_value: 1886
    source: Amélie_of_Orléans
    relation: :hasMarriageYear
  AddTriple (6d1d7ef1-72a6-42cc-a701-5391c6ae0c89)
 Call ID: 6d1d7ef1-72a6-42cc-a701-5391c6ae0c89
  Args:
    source: Amélie_of_Orléans
    target: Carlos_I_of_Portugal
    relation: :hasRelation
  AssignClass (f162e3d0-593a-4441-92b9-74d9181445e9)
 Call ID: f162e3d0-593a-4441-92b9-74d9181445e9
  Args:
    type: :Man
    source: Philippe_Count_of_Paris
  AssignClass (5d3ed0d1-18dd-4e02-b2a0-881c0736fec3)
 Call ID: 5d3ed0d1-18dd-4e02-b2a0-881c0736fec3
  Args:
    type: :Person
    source: Philippe_Count_of_Paris
  AssignClass (d2b7145d-c2e3-428b-80e6-aa7176ee921a)
 Call ID: d2b7145d-c2e3-428b-80e6-aa7176ee921a
  Args:
    type: :Woman
    source: Marie_Isabelle_dOrléans
  AssignClass (c358f1c9-5df2-4797-88e3-b192567aab94)
 Call ID: c358f1c9-5df2-4797-88e3-b192567aab94
  Args:
    type: :Person
    source: Marie_Isabelle_dOrléans
  AddTriple (e51af343-a103-40f7-a056-1cc784a31f6b)
 Call ID: e51af343-a103-40f7-a056-1cc784a31f6b
  Args:
    relation: :isDaughterOf
    target: Philippe_Count_of_Paris
    source: Amélie_of_Orléans
  AddTriple (29d0d441-a107-493b-b8c8-b1af7d08386d)
 Call ID: 29d0d441-a107-493b-b8c8-b1af7d08386d
  Args:
    relation: :isDaughterOf
    source: Amélie_of_Orléans
    target: Marie_Isabelle_dOrléans
  AssignClass (0b3e4280-8b6b-40bb-8122-d6abf6ff0c80)
 Call ID: 0b3e4280-8b6b-40bb-8122-d6abf6ff0c80
  Args:
    type: :Man
    source: Ferdinand_Philippe_Duke_of_Orléans
  AssignClass (168f84fb-6073-4e18-a9e9-ac014f9fc784)
 Call ID: 168f84fb-6073-4e18-a9e9-ac014f9fc784
  Args:
    type: :Person
    source: Ferdinand_Philippe_Duke_of_Orléans
  AssignClass (cc9dc893-5f1c-4d64-a160-21ffca9ac4c5)
 Call ID: cc9dc893-5f1c-4d64-a160-21ffca9ac4c5
  Args:
    type: :Woman
    source: Helena_of_Mecklenburg-Schwerin
  AssignClass (2dd0f8c0-4294-4362-90a7-3396ffc77e72)
 Call ID: 2dd0f8c0-4294-4362-90a7-3396ffc77e72
  Args:
    type: :Person
    source: Helena_of_Mecklenburg-Schwerin
  AddTriple (660c155f-9197-4607-a94f-a8037fa2310d)
 Call ID: 660c155f-9197-4607-a94f-a8037fa2310d
  Args:
    relation: :hasFather
    target: Ferdinand_Philippe_Duke_of_Orléans
    source: Philippe_Count_of_Paris
  AddTriple (59c60616-6be3-41f4-9971-5606c7858421)
 Call ID: 59c60616-6be3-41f4-9971-5606c7858421
  Args:
    relation: :hasMother
    target: Helena_of_Mecklenburg-Schwerin
    source: Philippe_Count_of_Paris
  AssignClass (f576aedc-df22-4121-8182-8a909b2731ef)
 Call ID: f576aedc-df22-4121-8182-8a909b2731ef
  Args:
    type: :Man
    source: Antoine_Duke_of_Montpensier
  AssignClass (825a3668-9c39-4cdd-af55-77725f54ff63)
 Call ID: 825a3668-9c39-4cdd-af55-77725f54ff63
  Args:
    type: :Person
    source: Antoine_Duke_of_Montpensier
  AssignClass (686f27e2-ac63-41dd-98da-14a3e0093b92)
 Call ID: 686f27e2-ac63-41dd-98da-14a3e0093b92
  Args:
    type: :Woman
    source: Luisa_Fernanda_of_Spain
  AssignClass (361607ae-b371-47df-ba3e-7a6c737e63b5)
 Call ID: 361607ae-b371-47df-ba3e-7a6c737e63b5
  Args:
    type: :Person
    source: Luisa_Fernanda_of_Spain
  AddTriple (946d3d8f-8454-4048-be53-463aa22ce27c)
 Call ID: 946d3d8f-8454-4048-be53-463aa22ce27c
  Args:
    relation: :hasFather
    source: Marie_Isabelle_dOrléans
    target: Antoine_Duke_of_Montpensier
  AddTriple (a963f8a3-dce0-49a2-b5e7-7b895e2a2481)
 Call ID: a963f8a3-dce0-49a2-b5e7-7b895e2a2481
  Args:
    relation: :hasMother
    source: Marie_Isabelle_dOrléans
    target: Luisa_Fernanda_of_Spain
  AssignClass (9b5c7281-e153-4059-8fde-8310dcc2273d)
 Call ID: 9b5c7281-e153-4059-8fde-8310dcc2273d
  Args:
    type: :Man
    source: Louis-Philippe_I_of_France
  AssignClass (6cd029a6-267e-4975-850c-6a2b191a8cb2)
 Call ID: 6cd029a6-267e-4975-850c-6a2b191a8cb2
  Args:
    type: :Person
    source: Louis-Philippe_I_of_France
  AssignClass (f80fa6b1-d6a9-473a-9f65-9a3f877ead7b)
 Call ID: f80fa6b1-d6a9-473a-9f65-9a3f877ead7b
  Args:
    type: :Woman
    source: Maria_Amalia_of_the_Two_Sicilies
  AssignClass (58e3ed5b-451c-4ba2-94b5-6c6e0a439efb)
 Call ID: 58e3ed5b-451c-4ba2-94b5-6c6e0a439efb
  Args:
    type: :Person
    source: Maria_Amalia_of_the_Two_Sicilies
  AddTriple (64afdc00-e09c-4332-9858-06e1e2fc8578)
 Call ID: 64afdc00-e09c-4332-9858-06e1e2fc8578
  Args:
    relation: :isFatherOf
    source: Louis-Philippe_I_of_France
    target: Ferdinand_Philippe_Duke_of_Orléans
  AddTriple (de13279f-243c-4ad5-9f87-05ca9054602c)
 Call ID: de13279f-243c-4ad5-9f87-05ca9054602c
  Args:
    relation: :isFatherOf
    target: Antoine_Duke_of_Montpensier
    source: Louis-Philippe_I_of_France
  AddTriple (f10a30b4-d517-454b-9944-802bd869de6f)
 Call ID: f10a30b4-d517-454b-9944-802bd869de6f
  Args:
    relation: :isMotherOf
    target: Ferdinand_Philippe_Duke_of_Orléans
    source: Maria_Amalia_of_the_Two_Sicilies
  AddTriple (2f3d6815-f18b-4f26-94a6-7c9716fc6526)
 Call ID: 2f3d6815-f18b-4f26-94a6-7c9716fc6526
  Args:
    relation: :isMotherOf
    source: Maria_Amalia_of_the_Two_Sicilies
    target: Antoine_Duke_of_Montpensier
  AssignClass (4b6590fa-dacd-4db9-8381-590df7934dfd)
 Call ID: 4b6590fa-dacd-4db9-8381-590df7934dfd
  Args:
    type: :Man
    source: Luís_I_of_Portugal
  AssignClass (6a93edb5-5e9d-40d3-a53f-7abf8861a6b1)
 Call ID: 6a93edb5-5e9d-40d3-a53f-7abf8861a6b1
  Args:
    type: :Person
    source: Luís_I_of_Portugal
  AssignClass (34378f4b-729c-4007-9920-93c04aaba05c)
 Call ID: 34378f4b-729c-4007-9920-93c04aaba05c
  Args:
    type: :Woman
    source: Maria_Pia_of_Savoy
  AssignClass (955a6c1b-c338-4ee5-94ee-eccbafee2d55)
 Call ID: 955a6c1b-c338-4ee5-94ee-eccbafee2d55
  Args:
    type: :Person
    source: Maria_Pia_of_Savoy
  AddTriple (03d4ec12-078e-4f21-821f-1f9b4cab17f5)
 Call ID: 03d4ec12-078e-4f21-821f-1f9b4cab17f5
  Args:
    target: Luís_I_of_Portugal
    source: Carlos_I_of_Portugal
    relation: :hasFather
  AddTriple (fd17131e-81d2-4ab6-bfb4-098e8b870599)
 Call ID: fd17131e-81d2-4ab6-bfb4-098e8b870599
  Args:
    relation: :hasMother
    source: Carlos_I_of_Portugal
    target: Maria_Pia_of_Savoy
  AssignClass (580b98da-35af-4b02-9d81-c4786c9d156d)
 Call ID: 580b98da-35af-4b02-9d81-c4786c9d156d
  Args:
    type: :Man
    source: Luís_Filipe_Prince_Royal
  AssignClass (74a2a85c-ac01-4bb5-bf97-64b671fd7300)
 Call ID: 74a2a85c-ac01-4bb5-bf97-64b671fd7300
  Args:
    type: :Person
    source: Luís_Filipe_Prince_Royal
  AssignClass (2147a1bf-9370-46a2-84a7-e6d1e68799c2)
 Call ID: 2147a1bf-9370-46a2-84a7-e6d1e68799c2
  Args:
    type: :Man
    source: Manuel_II_of_Portugal
  AssignClass (e6199166-959f-4bc0-aca2-31455fc0cd02)
 Call ID: e6199166-959f-4bc0-aca2-31455fc0cd02
  Args:
    type: :Person
    source: Manuel_II_of_Portugal
  AddTriple (2caf13e8-452a-4212-b8ac-3afe6eafdd5e)
 Call ID: 2caf13e8-452a-4212-b8ac-3afe6eafdd5e
  Args:
    relation: :isSonOf
    target: Amélie_of_Orléans
    source: Luís_Filipe_Prince_Royal
  AddTriple (c0c53484-d901-49bd-a744-521ebe2aee7c)
 Call ID: c0c53484-d901-49bd-a744-521ebe2aee7c
  Args:
    relation: :isSonOf
    target: Carlos_I_of_Portugal
    source: Luís_Filipe_Prince_Royal
  AddTriple (68f8fe2a-a669-4631-aa12-db7b684ba995)
 Call ID: 68f8fe2a-a669-4631-aa12-db7b684ba995
  Args:
    relation: :isSonOf
    source: Manuel_II_of_Portugal
    target: Amélie_of_Orléans
  AddTriple (e4d686e7-3642-453d-8efb-023778dc3dc9)
 Call ID: e4d686e7-3642-453d-8efb-023778dc3dc9
  Args:
    target: Carlos_I_of_Portugal
    source: Manuel_II_of_Portugal
    relation: :isSonOf
  AssignClass (5670c1af-3362-44eb-9fa6-f1b65d4c95d2)
 Call ID: 5670c1af-3362-44eb-9fa6-f1b65d4c95d2
  Args:
    type: :Man
    source: Duarte_Pio_Duke_of_Braganza
  AssignClass (48ed5a9e-4bf2-45f6-b704-6662c01c69cf)
 Call ID: 48ed5a9e-4bf2-45f6-b704-6662c01c69cf
  Args:
    type: :Person
    source: Duarte_Pio_Duke_of_Braganza
  Finish (1d42ab89-32ef-46a0-9d2d-80e5314c59a9)
 Call ID: 1d42ab89-32ef-46a0-9d2d-80e5314c59a9
  Args: