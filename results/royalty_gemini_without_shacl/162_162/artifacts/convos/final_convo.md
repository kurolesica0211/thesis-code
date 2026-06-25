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
  AssignClass (c2ce5903-8a3a-403e-9663-f6dafc22e1ae)
 Call ID: c2ce5903-8a3a-403e-9663-f6dafc22e1ae
  Args:
    source: Amélie_of_Orléans
    type: :Woman
  AssignClass (2d55f36d-2df3-4ebb-b4c5-e353ec68d683)
 Call ID: 2d55f36d-2df3-4ebb-b4c5-e353ec68d683
  Args:
    type: :Person
    source: Amélie_of_Orléans
  AddLiteral (7153fbec-d5c0-4380-adb1-28fa9872198f)
 Call ID: 7153fbec-d5c0-4380-adb1-28fa9872198f
  Args:
    literal_value: 1865
    source: Amélie_of_Orléans
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (9a92d253-03ac-4f28-ab72-8161d3d5a8fe)
 Call ID: 9a92d253-03ac-4f28-ab72-8161d3d5a8fe
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: Amélie_of_Orléans
    literal_value: 1951
  AssignClass (f47ba2d8-e1ed-4b15-a508-58118961697c)
 Call ID: f47ba2d8-e1ed-4b15-a508-58118961697c
  Args:
    source: Carlos_I_of_Portugal
    type: :Man
  AssignClass (6dd3d0fb-e577-4050-842c-f44e305615da)
 Call ID: 6dd3d0fb-e577-4050-842c-f44e305615da
  Args:
    type: :Person
    source: Carlos_I_of_Portugal
  AddTriple (dfdb2133-1ff0-46fd-814b-5d4a7e296818)
 Call ID: dfdb2133-1ff0-46fd-814b-5d4a7e296818
  Args:
    source: Amélie_of_Orléans
    target: Carlos_I_of_Portugal
    relation: :hasRelation
  AddLiteral (9a95085c-bbe2-441c-8a2f-4a4cb0e65033)
 Call ID: 9a95085c-bbe2-441c-8a2f-4a4cb0e65033
  Args:
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: Amélie_of_Orléans
    literal_value: 1886
  AssignClass (f7b6eb20-832a-4d2f-8b69-7145e838e7fc)
 Call ID: f7b6eb20-832a-4d2f-8b69-7145e838e7fc
  Args:
    source: Philippe_Count_of_Paris
    type: :Man
  AssignClass (dbbcf03c-8298-464e-8b03-160c5fb124d4)
 Call ID: dbbcf03c-8298-464e-8b03-160c5fb124d4
  Args:
    type: :Person
    source: Philippe_Count_of_Paris
  AssignClass (e5b1e6cf-9e33-4ab0-bb39-f299cb4966f5)
 Call ID: e5b1e6cf-9e33-4ab0-bb39-f299cb4966f5
  Args:
    type: :Woman
    source: Marie_Isabelle_dOrléans
  AssignClass (533e5020-00b5-40e8-8b4a-c397737f685c)
 Call ID: 533e5020-00b5-40e8-8b4a-c397737f685c
  Args:
    source: Marie_Isabelle_dOrléans
    type: :Person
  AddTriple (11a5a52a-3756-4a2a-9a02-811cbfbf6d5b)
 Call ID: 11a5a52a-3756-4a2a-9a02-811cbfbf6d5b
  Args:
    target: Philippe_Count_of_Paris
    source: Amélie_of_Orléans
    relation: :hasFather
  AddTriple (27053471-2386-475d-b876-505ab1036682)
 Call ID: 27053471-2386-475d-b876-505ab1036682
  Args:
    relation: :hasMother
    target: Marie_Isabelle_dOrléans
    source: Amélie_of_Orléans
  AssignClass (540d6141-77b1-40c9-a877-5f8d3bf5a419)
 Call ID: 540d6141-77b1-40c9-a877-5f8d3bf5a419
  Args:
    source: Ferdinand_Philippe_Duke_of_Orléans
    type: :Man
  AssignClass (098697c2-917c-4d10-b565-b12b0f42e28f)
 Call ID: 098697c2-917c-4d10-b565-b12b0f42e28f
  Args:
    type: :Person
    source: Ferdinand_Philippe_Duke_of_Orléans
  AssignClass (fe1cb2c6-1bf2-4845-8b3d-a05386b221dd)
 Call ID: fe1cb2c6-1bf2-4845-8b3d-a05386b221dd
  Args:
    source: Helena_of_Mecklenburg_Schwerin
    type: :Woman
  AssignClass (8f1428ad-5e6a-4ef8-a2e9-a2d560a7b74f)
 Call ID: 8f1428ad-5e6a-4ef8-a2e9-a2d560a7b74f
  Args:
    source: Helena_of_Mecklenburg_Schwerin
    type: :Person
  AddTriple (736f732f-55f1-452d-ad52-a357fe89b651)
 Call ID: 736f732f-55f1-452d-ad52-a357fe89b651
  Args:
    target: Ferdinand_Philippe_Duke_of_Orléans
    source: Philippe_Count_of_Paris
    relation: :hasFather
  AddTriple (fca24245-0737-4ed7-ae44-f6e21be179c4)
 Call ID: fca24245-0737-4ed7-ae44-f6e21be179c4
  Args:
    source: Philippe_Count_of_Paris
    target: Helena_of_Mecklenburg_Schwerin
    relation: :hasMother
  AssignClass (dc5ab1ed-4873-4aa4-ab0a-020db0eb6201)
 Call ID: dc5ab1ed-4873-4aa4-ab0a-020db0eb6201
  Args:
    source: Antoine_Duke_of_Montpensier
    type: :Man
  AssignClass (9c537c77-ff8a-49de-9e8f-8f0f65e619b3)
 Call ID: 9c537c77-ff8a-49de-9e8f-8f0f65e619b3
  Args:
    source: Antoine_Duke_of_Montpensier
    type: :Person
  AssignClass (fce367b8-20ed-465e-a76a-0a6ac9ff3c70)
 Call ID: fce367b8-20ed-465e-a76a-0a6ac9ff3c70
  Args:
    source: Luisa_Fernanda_of_Spain
    type: :Woman
  AssignClass (f897fe22-8f87-468b-840d-8df11a533777)
 Call ID: f897fe22-8f87-468b-840d-8df11a533777
  Args:
    source: Luisa_Fernanda_of_Spain
    type: :Person
  AddTriple (b4580e84-9d17-4dc0-9964-d3c07e2b2a99)
 Call ID: b4580e84-9d17-4dc0-9964-d3c07e2b2a99
  Args:
    relation: :hasFather
    source: Marie_Isabelle_dOrléans
    target: Antoine_Duke_of_Montpensier
  AddTriple (4b5c4c72-04c0-4b6a-877f-2350aa2fbef6)
 Call ID: 4b5c4c72-04c0-4b6a-877f-2350aa2fbef6
  Args:
    source: Marie_Isabelle_dOrléans
    target: Luisa_Fernanda_of_Spain
    relation: :hasMother
  AssignClass (5807dc42-0235-44d6-8f76-fb1ce5956d17)
 Call ID: 5807dc42-0235-44d6-8f76-fb1ce5956d17
  Args:
    type: :Man
    source: Louis_Philippe_I_of_France
  AssignClass (7ae97f0f-24af-49e6-b9ba-18ff29f3b2b4)
 Call ID: 7ae97f0f-24af-49e6-b9ba-18ff29f3b2b4
  Args:
    source: Louis_Philippe_I_of_France
    type: :Person
  AssignClass (a5cbf22f-70e7-4b05-bb19-f11361e9cfd5)
 Call ID: a5cbf22f-70e7-4b05-bb19-f11361e9cfd5
  Args:
    source: Maria_Amalia_of_the_Two_Sicilies
    type: :Woman
  AssignClass (fa485c2f-5f67-41d7-8e03-3b2da34b93b5)
 Call ID: fa485c2f-5f67-41d7-8e03-3b2da34b93b5
  Args:
    type: :Person
    source: Maria_Amalia_of_the_Person
  AddTriple (a419ec02-60a0-4391-bc2a-0f1062edca7d)
 Call ID: a419ec02-60a0-4391-bc2a-0f1062edca7d
  Args:
    relation: :isFatherOf
    target: Ferdinand_Philippe_Duke_of_Orléans
    source: Louis_Philippe_I_of_France
  AddTriple (1ba183e9-dc47-483b-9116-c2469014a315)
 Call ID: 1ba183e9-dc47-483b-9116-c2469014a315
  Args:
    source: Louis_Philippe_I_of_France
    target: Antoine_Duke_of_Montpensier
    relation: :isFatherOf
  AddTriple (b5a95bf1-bfc1-4fd2-bccc-b74fd62bd217)
 Call ID: b5a95bf1-bfc1-4fd2-bccc-b74fd62bd217
  Args:
    target: Ferdinand_Philippe_Duke_of_Orléans
    source: Maria_Amalia_of_the_Two_Sicilies
    relation: :isMotherOf
  AddTriple (1c1671fa-e73f-44ed-b031-a0db2b6d4680)
 Call ID: 1c1671fa-e73f-44ed-b031-a0db2b6d4680
  Args:
    relation: :isMotherOf
    target: Antoine_Duke_of_Montpensier
    source: Maria_Amalia_of_the_Two_Sicilies
  AssignClass (e838f8b2-dd89-459c-bf2a-2b6ea71bf292)
 Call ID: e838f8b2-dd89-459c-bf2a-2b6ea71bf292
  Args:
    type: :Man
    source: Luís_I_of_Portugal
  AssignClass (661af91c-89b2-4b93-93e0-73f7c23815f0)
 Call ID: 661af91c-89b2-4b93-93e0-73f7c23815f0
  Args:
    type: :Person
    source: Luís_I_of_Portugal
  AssignClass (282cba6b-57be-42e7-a4c7-7c8224dbf32a)
 Call ID: 282cba6b-57be-42e7-a4c7-7c8224dbf32a
  Args:
    source: Maria_Pia_of_Savoy
    type: :Woman
  AssignClass (c94e0655-2ded-44b5-b45b-00b4cf769e8d)
 Call ID: c94e0655-2ded-44b5-b45b-00b4cf769e8d
  Args:
    type: :Person
    source: Maria_Pia_of_Savoy
  AddTriple (fa420fc9-3c02-4619-b2fe-2a16939a49c7)
 Call ID: fa420fc9-3c02-4619-b2fe-2a16939a49c7
  Args:
    source: Carlos_I_of_Portugal
    target: Luís_I_of_Portugal
    relation: :hasFather
  AddTriple (e5cd1069-321d-44f3-a625-c371b7a35927)
 Call ID: e5cd1069-321d-44f3-a625-c371b7a35927
  Args:
    relation: :hasMother
    target: Maria_Pia_of_Savoy
    source: Carlos_I_of_Portugal
  AssignClass (9af4a4e6-d52f-425e-aa9a-99f4dd14cbe7)
 Call ID: 9af4a4e6-d52f-425e-aa9a-99f4dd14cbe7
  Args:
    source: Luís_Filipe_Prince_Royal_of_Portugal
    type: :Man
  AssignClass (f98131dc-ce32-4d6e-baab-d0d92e563b48)
 Call ID: f98131dc-ce32-4d6e-baab-d0d92e563b48
  Args:
    source: Luís_Filipe_Prince_Royal_of_Portugal
    type: :Person
  AssignClass (e316e54e-a6ca-4920-9560-2140532ae859)
 Call ID: e316e54e-a6ca-4920-9560-2140532ae859
  Args:
    type: :Man
    source: Manuel_II_of_Portugal
  AssignClass (e4042553-fecf-47d8-9e8f-2f731c0da1fe)
 Call ID: e4042553-fecf-47d8-9e8f-2f731c0da1fe
  Args:
    type: :Person
    source: Manuel_II_of_Portugal
  AddTriple (00bdf1fb-2b97-4dc1-8f07-9cb08c70175f)
 Call ID: 00bdf1fb-2b97-4dc1-8f07-9cb08c70175f
  Args:
    relation: :hasFather
    source: Luís_Filipe_Prince_Royal_of_Portugal
    target: Carlos_I_of_Portugal
  AddTriple (5eeaabc8-2f57-4ef1-b4d2-ae1b8783a6b1)
 Call ID: 5eeaabc8-2f57-4ef1-b4d2-ae1b8783a6b1
  Args:
    target: Amélie_of_Orléans
    source: Luís_Filipe_Prince_Royal_of_Portugal
    relation: :hasMother
  AddTriple (88180ef4-51a9-4f5f-9c52-a8d9f4ce2893)
 Call ID: 88180ef4-51a9-4f5f-9c52-a8d9f4ce2893
  Args:
    relation: :hasFather
    source: Manuel_II_of_Portugal
    target: Carlos_I_of_Portugal
  AddTriple (9bc92bdd-a0a0-437a-b64c-d5f8766ec192)
 Call ID: 9bc92bdd-a0a0-437a-b64c-d5f8766ec192
  Args:
    target: Amélie_of_Orléans
    source: Manuel_II_of_Portugal
    relation: :hasMother
  Finish (ec174c87-8220-4784-b44f-865a3e8c4b81)
 Call ID: ec174c87-8220-4784-b44f-865a3e8c4b81
  Args: