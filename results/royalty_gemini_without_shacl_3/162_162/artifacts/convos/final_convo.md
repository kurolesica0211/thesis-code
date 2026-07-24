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
  AssignClass (34a80c3a-8c89-42dd-9d08-0c1f2f560101)
 Call ID: 34a80c3a-8c89-42dd-9d08-0c1f2f560101
  Args:
    source: Amélie_of_Orléans
    type: :Woman
  AssignClass (8cfde512-ad0f-44ca-9ee7-3afd028a3fa1)
 Call ID: 8cfde512-ad0f-44ca-9ee7-3afd028a3fa1
  Args:
    source: Amélie_of_Orléans
    type: :Person
  AddLiteral (7127adec-ff1a-45e1-95fb-b16c4826dc65)
 Call ID: 7127adec-ff1a-45e1-95fb-b16c4826dc65
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1865
    source: Amélie_of_Orléans
  AddLiteral (092f4a39-bb8d-4ea8-9a48-a228bee1436d)
 Call ID: 092f4a39-bb8d-4ea8-9a48-a228bee1436d
  Args:
    source: Amélie_of_Orléans
    literal_value: 1951
    relation: :hasDeathYear
    literal_type: xsd:integer
  AssignClass (0931d3a6-af62-44da-bbbf-6562a44f6e2b)
 Call ID: 0931d3a6-af62-44da-bbbf-6562a44f6e2b
  Args:
    source: Carlos_I_of_Portugal
    type: :Man
  AssignClass (cd85c5c9-b85c-450a-9417-1cede76f8d41)
 Call ID: cd85c5c9-b85c-450a-9417-1cede76f8d41
  Args:
    source: Carlos_I_of_Portugal
    type: :Person
  AddTriple (3e6f520b-bef6-45ec-abd8-0abde177dd6d)
 Call ID: 3e6f520b-bef6-45ec-abd8-0abde177dd6d
  Args:
    relation: :hasRelation
    source: Amélie_of_Orléans
    target: Carlos_I_of_Portugal
  AddLiteral (6a7eb061-206b-4fe9-91c9-b54ab60a2785)
 Call ID: 6a7eb061-206b-4fe9-91c9-b54ab60a2785
  Args:
    source: Amélie_of_Orléans
    literal_value: 1886
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AssignClass (e38e5ecc-2e30-47b8-abb3-b60538dcaebc)
 Call ID: e38e5ecc-2e30-47b8-abb3-b60538dcaebc
  Args:
    type: :Man
    source: Prince_Philippe_Count_of_Paris
  AssignClass (af501569-1558-400f-a4fc-2e9cc323faaf)
 Call ID: af501569-1558-400f-a4fc-2e9cc323faaf
  Args:
    type: :Person
    source: Prince_Philippe_Count_of_Paris
  AssignClass (7b8e0f4f-9923-4909-8568-cc08129c38a8)
 Call ID: 7b8e0f4f-9923-4909-8568-cc08129c38a8
  Args:
    source: Princess_Marie_Isabelle_dOrléans
    type: :Woman
  AssignClass (0af5166c-4730-45b6-bfb1-d39a136574d4)
 Call ID: 0af5166c-4730-45b6-bfb1-d39a136574d4
  Args:
    type: :Person
    source: Princess_Marie_Isabelle_dOrléans
  AddTriple (0495b101-6f0f-45a1-987c-eacdbef011f9)
 Call ID: 0495b101-6f0f-45a1-987c-eacdbef011f9
  Args:
    source: Amélie_of_Orléans
    target: Prince_Philippe_Count_of_Paris
    relation: :hasFather
  AddTriple (3d679d2b-d525-4948-a844-785528956f7e)
 Call ID: 3d679d2b-d525-4948-a844-785528956f7e
  Args:
    source: Amélie_of_Orléans
    target: Princess_Marie_Isabelle_dOrléans
    relation: :hasMother
  AssignClass (24b062ad-5713-4fe9-a7f8-3d8594acaff3)
 Call ID: 24b062ad-5713-4fe9-a7f8-3d8594acaff3
  Args:
    source: Prince_Ferdinand_Philippe_Duke_of_Orléans
    type: :Man
  AssignClass (fa911692-4f5c-4c5c-8617-3216c2ac7b94)
 Call ID: fa911692-4f5c-4c5c-8617-3216c2ac7b94
  Args:
    source: Prince_Ferdinand_Philippe_Duke_of_Orléans
    type: :Person
  AssignClass (21b002bd-be72-4a01-960c-366a46de14a2)
 Call ID: 21b002bd-be72-4a01-960c-366a46de14a2
  Args:
    source: Duchess_Helena_of_Mecklenburg_Schwerin
    type: :Woman
  AssignClass (7b25d8cd-5397-4035-af35-46f817255dff)
 Call ID: 7b25d8cd-5397-4035-af35-46f817255dff
  Args:
    type: :Person
    source: Duchess_Helena_of_Mecklenburg_Schwerin
  AddTriple (67b9c98a-f9b5-49e3-a83a-1029ac8b7b25)
 Call ID: 67b9c98a-f9b5-49e3-a83a-1029ac8b7b25
  Args:
    source: Prince_Philippe_Count_of_Paris
    target: Prince_Ferdinand_Philippe_Duke_of_Orléans
    relation: :hasFather
  AddTriple (6e163c78-11e7-4159-85e5-2ce5fc97c53a)
 Call ID: 6e163c78-11e7-4159-85e5-2ce5fc97c53a
  Args:
    relation: :hasMother
    target: Duchess_Helena_of_Mecklenburg_Schwerin
    source: Prince_Philippe_Count_of_Paris
  AssignClass (cad82023-95e7-43ca-8bf7-1c2197d10200)
 Call ID: cad82023-95e7-43ca-8bf7-1c2197d10200
  Args:
    source: Prince_Antoine_Duke_of_Montpensier
    type: :Man
  AssignClass (657b8d1d-caf9-4c86-88b6-ac57b84e8c84)
 Call ID: 657b8d1d-caf9-4c86-88b6-ac57b84e8c84
  Args:
    source: Prince_Antoine_Duke_of_Montpensier
    type: :Person
  AssignClass (f1ee615d-41b2-44fd-b1f0-c28296845a8e)
 Call ID: f1ee615d-41b2-44fd-b1f0-c28296845a8e
  Args:
    type: :Woman
    source: Infanta_Luisa_Fernanda_of_Spain
  AssignClass (43eb8927-587d-4a9f-ac1a-2ef88323ccf4)
 Call ID: 43eb8927-587d-4a9f-ac1a-2ef88323ccf4
  Args:
    source: Infanta_Luisa_Fernanda_of_Spain
    type: :Person
  AddTriple (6a75b738-dff9-4565-bb9c-040d43092299)
 Call ID: 6a75b738-dff9-4565-bb9c-040d43092299
  Args:
    relation: :hasFather
    source: Princess_Marie_Isabelle_dOrléans
    target: Prince_Antoine_Duke_of_Montpensier
  AddTriple (fc7fc3e3-ee1b-44db-886f-e80aef21f6e1)
 Call ID: fc7fc3e3-ee1b-44db-886f-e80aef21f6e1
  Args:
    relation: :hasMother
    source: Princess_Marie_Isabelle_dOrléans
    target: Infanta_Luisa_Fernanda_of_Spain
  AssignClass (7145c7f5-7b04-4570-bc74-cb4aa8f4255a)
 Call ID: 7145c7f5-7b04-4570-bc74-cb4aa8f4255a
  Args:
    type: :Man
    source: King_Louis_Philippe_I_of_France
  AssignClass (c1083620-7c6d-4952-aa3b-e137077a71b9)
 Call ID: c1083620-7c6d-4952-aa3b-e137077a71b9
  Args:
    source: King_Louis_Philippe_I_of_France
    type: :Person
  AssignClass (773cb26a-5257-47fb-8b8e-24d8906ef48d)
 Call ID: 773cb26a-5257-47fb-8b8e-24d8906ef48d
  Args:
    source: Maria_Amalia_of_the_Two_Sicilies
    type: :Woman
  AssignClass (263569a0-f625-43b0-a617-741a5bc5f3e2)
 Call ID: 263569a0-f625-43b0-a617-741a5bc5f3e2
  Args:
    type: :Person
    source: Maria_Amalia_of_the_Two_Sicilies
  AddTriple (46c8ce45-fbe6-48be-98f8-e4d28d1229a2)
 Call ID: 46c8ce45-fbe6-48be-98f8-e4d28d1229a2
  Args:
    relation: :hasFather
    source: Prince_Ferdinand_Philippe_Duke_of_Orléans
    target: King_Louis_Philippe_I_of_France
  AddTriple (6553259d-9e22-496e-aa99-911a9f89e806)
 Call ID: 6553259d-9e22-496e-aa99-911a9f89e806
  Args:
    target: Maria_Amalia_of_the_Two_Sicilies
    source: Prince_Ferdinand_Philippe_Duke_of_Orléans
    relation: :hasMother
  AddTriple (7ff0fb2c-352f-454a-8ab8-b29b7c87656b)
 Call ID: 7ff0fb2c-352f-454a-8ab8-b29b7c87656b
  Args:
    relation: :hasFather
    target: King_Louis_Philippe_I_of_France
    source: Prince_Antoine_Duke_of_Montpensier
  AddTriple (4f3dce4a-5bd7-421f-9ae0-283850e28ade)
 Call ID: 4f3dce4a-5bd7-421f-9ae0-283850e28ade
  Args:
    relation: :hasMother
    source: Prince_Antoine_Duke_of_Montpensier
    target: Maria_Amalia_of_the_Two_Sicilies
  AssignClass (6d5ac7af-9d47-4531-9b19-9c71fa308cb7)
 Call ID: 6d5ac7af-9d47-4531-9b19-9c71fa308cb7
  Args:
    type: :Man
    source: King_Luís_I_of_Portugal
  AssignClass (9a33a5c4-a777-4047-b6c1-3a06f5803843)
 Call ID: 9a33a5c4-a777-4047-b6c1-3a06f5803843
  Args:
    source: King_Luís_I_of_Portugal
    type: :Person
  AssignClass (9bd0f5f7-3f45-4c82-a771-f66a79273aba)
 Call ID: 9bd0f5f7-3f45-4c82-a771-f66a79273aba
  Args:
    type: :Woman
    source: Maria_Pia_of_Savoy
  AssignClass (8eab9c18-db17-4736-9c08-e15bc33cd75d)
 Call ID: 8eab9c18-db17-4736-9c08-e15bc33cd75d
  Args:
    type: :Person
    source: Maria_Pia_of_Savoy
  AddTriple (990ca496-e162-461b-a2b6-f5ec4a993899)
 Call ID: 990ca496-e162-461b-a2b6-f5ec4a993899
  Args:
    target: King_Luís_I_of_Portugal
    source: Carlos_I_of_Portugal
    relation: :hasFather
  AddTriple (df3122ff-f65e-4f95-a06f-8eea1bd72e51)
 Call ID: df3122ff-f65e-4f95-a06f-8eea1bd72e51
  Args:
    relation: :hasMother
    target: Maria_Pia_of_Savoy
    source: Carlos_I_of_Portugal
  AssignClass (efbc4a4b-a4a7-4b99-983b-07d687c5c0c8)
 Call ID: efbc4a4b-a4a7-4b99-983b-07d687c5c0c8
  Args:
    source: Prince_Dom_Luís_Filipe
    type: :Man
  AssignClass (70a15565-7022-44e8-a593-cced8f71d9a0)
 Call ID: 70a15565-7022-44e8-a593-cced8f71d9a0
  Args:
    source: Prince_Dom_Luís_Filipe
    type: :Person
  AssignClass (2a7f4f6f-301a-4b73-a53f-bff60190b4f1)
 Call ID: 2a7f4f6f-301a-4b73-a53f-bff60190b4f1
  Args:
    source: Infante_Dom_Manuel_Manuel_II
    type: :Man
  AssignClass (c4acac96-763f-4d1a-aa0a-f83ef1ef4eff)
 Call ID: c4acac96-763f-4d1a-aa0a-f83ef1ef4eff
  Args:
    type: :Person
    source: Infante_Dom_Manuel_Manuel_II
  AddTriple (db81d4b9-dad8-4622-8206-a12ea7db693a)
 Call ID: db81d4b9-dad8-4622-8206-a12ea7db693a
  Args:
    relation: :hasFather
    source: Prince_Dom_Luís_Filipe
    target: Carlos_I_of_Portugal
  AddTriple (153350fe-9432-4482-b5a2-1a51a8226a26)
 Call ID: 153350fe-9432-4482-b5a2-1a51a8226a26
  Args:
    relation: :hasMother
    source: Prince_Dom_Luís_Filipe
    target: Amélie_of_Orléans
  AddTriple (7962b1d6-c36e-439c-bb3f-1ece0a7da1b3)
 Call ID: 7962b1d6-c36e-439c-bb3f-1ece0a7da1b3
  Args:
    relation: :hasFather
    target: Carlos_I_of_Portugal
    source: Infante_Dom_Manuel_Manuel_II
  AddTriple (700c6cbe-5511-4c54-800a-0d2d35157b9f)
 Call ID: 700c6cbe-5511-4c54-800a-0d2d35157b9f
  Args:
    target: Amélie_of_Orléans
    source: Infante_Dom_Manuel_Manuel_II
    relation: :hasMother
  Finish (3d61c96a-5065-423c-bc82-703e569955ac)
 Call ID: 3d61c96a-5065-423c-bc82-703e569955ac
  Args: