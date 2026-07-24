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
  AssignClass (7b422989-b4a0-4997-8c80-1d0918d4eae2)
 Call ID: 7b422989-b4a0-4997-8c80-1d0918d4eae2
  Args:
    type: :Woman
    source: :Amélie_of_Orléans
  AssignClass (8a6d6403-bc1e-41e4-994d-06387dd5bded)
 Call ID: 8a6d6403-bc1e-41e4-994d-06387dd5bded
  Args:
    source: :Amélie_of_Orléans
    type: :Person
  AddLiteral (539b31b6-6e0c-4b6b-bd00-1e23cfd29225)
 Call ID: 539b31b6-6e0c-4b6b-bd00-1e23cfd29225
  Args:
    literal_type: xsd:integer
    literal_value: 1865
    source: :Amélie_of_Orléans
    relation: :hasBirthYear
  AddLiteral (c47cbc98-0c46-4197-823c-37f64a180399)
 Call ID: c47cbc98-0c46-4197-823c-37f64a180399
  Args:
    source: :Amélie_of_Orléans
    relation: :hasDeathYear
    literal_value: 1951
    literal_type: xsd:integer
  AssignClass (e07dd6c5-37a4-4326-9ce2-3d0beb4f4317)
 Call ID: e07dd6c5-37a4-4326-9ce2-3d0beb4f4317
  Args:
    source: :Carlos_I_of_Portugal
    type: :Man
  AssignClass (7ad31b97-87e1-444d-b2e0-9c1912c5fc4a)
 Call ID: 7ad31b97-87e1-444d-b2e0-9c1912c5fc4a
  Args:
    type: :Person
    source: :Carlos_I_of_Portugal
  AddLiteral (f211debc-e0aa-4e0c-8baa-99f9ccf11096)
 Call ID: f211debc-e0aa-4e0c-8baa-99f9ccf11096
  Args:
    relation: :hasMarriageYear
    source: :Amélie_of_Orléans
    literal_value: 1886
    literal_type: xsd:integer
  AddTriple (468c883c-5f42-4479-bdd2-96eea2fcd0be)
 Call ID: 468c883c-5f42-4479-bdd2-96eea2fcd0be
  Args:
    target: :Carlos_I_of_Portugal
    relation: :hasRelation
    source: :Amélie_of_Orléans
  AssignClass (210816d8-557c-4da1-a3e4-bf5789dadb39)
 Call ID: 210816d8-557c-4da1-a3e4-bf5789dadb39
  Args:
    type: :Man
    source: :Prince_Philippe_Count_of_Paris
  AssignClass (3d0995d3-fd77-41e7-b2fc-8fd3617ccf3c)
 Call ID: 3d0995d3-fd77-41e7-b2fc-8fd3617ccf3c
  Args:
    source: :Prince_Philippe_Count_of_Paris
    type: :Person
  AssignClass (02270071-ecd3-4e53-ab59-5d3f8ef482b2)
 Call ID: 02270071-ecd3-4e53-ab59-5d3f8ef482b2
  Args:
    type: :Woman
    source: :Princess_Marie_Isabelle_dOrléans
  AssignClass (2b913685-a39b-4953-8224-dfd8c19b4b25)
 Call ID: 2b913685-a39b-4953-8224-dfd8c19b4b25
  Args:
    type: :Person
    source: :Princess_Marie_Isabelle_dOrléans
  AddTriple (03b2e965-fc2f-47d1-8b8c-f2210ad58099)
 Call ID: 03b2e965-fc2f-47d1-8b8c-f2210ad58099
  Args:
    source: :Amélie_of_Orléans
    relation: :hasFather
    target: :Prince_Philippe_Count_of_Paris
  AddTriple (55e0b32e-2fa0-4e8c-8e3c-780dfc732290)
 Call ID: 55e0b32e-2fa0-4e8c-8e3c-780dfc732290
  Args:
    target: :Princess_Marie_Isabelle_dOrléans
    relation: :hasMother
    source: :Amélie_of_Orléans
  AssignClass (a582d3e5-d036-4f08-bb80-782c80431ea2)
 Call ID: a582d3e5-d036-4f08-bb80-782c80431ea2
  Args:
    type: :Man
    source: :Prince_Ferdinand_Philippe_Duke_of_Orléans
  AssignClass (b6b92be1-e127-4ced-a249-10f116b07527)
 Call ID: b6b92be1-e127-4ced-a249-10f116b07527
  Args:
    source: :Duchess_Helena_of_Mecklenburg-Schwerin
    type: :Woman
  AddTriple (789fef6a-1cff-4c37-b440-db3121462776)
 Call ID: 789fef6a-1cff-4c37-b440-db3121462776
  Args:
    relation: :hasFather
    source: :Prince_Philippe_Count_of_Paris
    target: :Prince_Ferdinand_Philippe_Duke_of_Orléans
  AddTriple (00fefc24-3c03-4160-a16b-eb66e64bde8c)
 Call ID: 00fefc24-3c03-4160-a16b-eb66e64bde8c
  Args:
    source: :Prince_Philippe_Count_of_Paris
    relation: :hasMother
    target: :Duchess_Helena_of_Mecklenburg-Schwerin
  AssignClass (aaa090da-b0b6-4d2d-9a4e-1bff656ac07d)
 Call ID: aaa090da-b0b6-4d2d-9a4e-1bff656ac07d
  Args:
    type: :Man
    source: :Prince_Antoine_Duke_of_Montpensier
  AssignClass (fb46cf4b-74b0-44c8-b4b4-2a3b6143220d)
 Call ID: fb46cf4b-74b0-44c8-b4b4-2a3b6143220d
  Args:
    type: :Woman
    source: :Infanta_Luisa_Fernanda_of_Spain
  AddTriple (5b275248-ba7f-480e-b4ce-fd5d5c823d90)
 Call ID: 5b275248-ba7f-480e-b4ce-fd5d5c823d90
  Args:
    target: :Prince_Antoine_Duke_of_Montpensier
    source: :Princess_Marie_Isabelle_dOrléans
    relation: :hasFather
  AddTriple (7f42e62f-ac71-4095-b772-316ebbb935dd)
 Call ID: 7f42e62f-ac71-4095-b772-316ebbb935dd
  Args:
    target: :Infanta_Luisa_Fernanda_of_Spain
    relation: :hasMother
    source: :Princess_Marie_Isabelle_dOrléans
  AssignClass (6feeb85d-dad3-4ce8-b7eb-996bb7cf2759)
 Call ID: 6feeb85d-dad3-4ce8-b7eb-996bb7cf2759
  Args:
    type: :Man
    source: :King_Louis-Philippe_I_of_France
  AssignClass (2c5e0977-8a67-4359-941a-391fae0df1cd)
 Call ID: 2c5e0977-8a67-4359-941a-391fae0df1cd
  Args:
    source: :Maria_Amalia_of_the_Two_Sicilies
    type: :Woman
  AddTriple (59501158-cc22-4b88-8ebc-5fda4d9ca7d0)
 Call ID: 59501158-cc22-4b88-8ebc-5fda4d9ca7d0
  Args:
    relation: :hasFather
    source: :Prince_Ferdinand_Philippe_Duke_of_Orléans
    target: :King_Louis-Philippe_I_of_France
  AddTriple (35ee0542-7897-4268-9582-b9308f9c4090)
 Call ID: 35ee0542-7897-4268-9582-b9308f9c4090
  Args:
    relation: :hasMother
    source: :Prince_Ferdinand_Philippe_Duke_of_Orléans
    target: :Maria_Amalia_of_the_Two_Sicilies
  AddTriple (a9d34636-bdf4-4668-a029-68b10c57d0b8)
 Call ID: a9d34636-bdf4-4668-a029-68b10c57d0b8
  Args:
    target: :King_Louis-Philippe_I_of_France
    relation: :hasFather
    source: :Prince_Antoine_Duke_of_Montpensier
  AddTriple (5e77d94a-889d-49cc-9c4d-1a02996feb62)
 Call ID: 5e77d94a-889d-49cc-9c4d-1a02996feb62
  Args:
    target: :Maria_Amalia_of_the_Two_Sicilies
    source: :Prince_Antoine_Duke_of_Montpensier
    relation: :hasMother
  AssignClass (7b6210ab-f6a0-4ca3-833d-926ac69bc774)
 Call ID: 7b6210ab-f6a0-4ca3-833d-926ac69bc774
  Args:
    type: :Man
    source: :King_Luís_I_of_Portugal
  AssignClass (814c6ca3-f4d5-4c4d-8e6f-fdb5c3abf1cd)
 Call ID: 814c6ca3-f4d5-4c4d-8e6f-fdb5c3abf1cd
  Args:
    type: :Woman
    source: :Maria_Pia_of_Savoy
  AddTriple (e9d7ff3f-098e-43d9-9efd-01fee9f62e53)
 Call ID: e9d7ff3f-098e-43d9-9efd-01fee9f62e53
  Args:
    relation: :hasFather
    source: :Carlos_I_of_Portugal
    target: :King_Luís_I_of_Portugal
  AddTriple (a056d3b4-91f4-41ce-a946-0b59065fbd95)
 Call ID: a056d3b4-91f4-41ce-a946-0b59065fbd95
  Args:
    target: :Maria_Pia_of_Savoy
    relation: :hasMother
    source: :Carlos_I_of_Portugal
  Finish (bdb067f4-09b3-4863-a8f3-a1b340737657)
 Call ID: bdb067f4-09b3-4863-a8f3-a1b340737657
  Args: