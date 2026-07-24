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
  AssignClass (cd31af94-791d-4c33-92f2-679001969451)
 Call ID: cd31af94-791d-4c33-92f2-679001969451
  Args:
    source: Amélie_of_Orléans
    type: :Woman
  AssignClass (37bb6be8-8d35-420c-a085-00fc882515e0)
 Call ID: 37bb6be8-8d35-420c-a085-00fc882515e0
  Args:
    type: :Person
    source: Amélie_of_Orléans
  AddLiteral (5a36f9f3-fc1f-41f1-bda6-db3749305f59)
 Call ID: 5a36f9f3-fc1f-41f1-bda6-db3749305f59
  Args:
    literal_type: xsd:integer
    source: Amélie_of_Orléans
    relation: :hasBirthYear
    literal_value: 1865
  AddLiteral (a16eac4e-92fb-4d14-a5f8-755aca67d7a8)
 Call ID: a16eac4e-92fb-4d14-a5f8-755aca67d7a8
  Args:
    relation: :hasDeathYear
    literal_value: 1951
    source: Amélie_of_Orléans
    literal_type: xsd:integer
  AssignClass (f3d477a9-10d1-4077-8de0-a20e9caaf86e)
 Call ID: f3d477a9-10d1-4077-8de0-a20e9caaf86e
  Args:
    type: :Man
    source: Carlos_I_of_Portugal
  AssignClass (4b7d4b43-db97-4534-8c8e-4b4a727dbc3b)
 Call ID: 4b7d4b43-db97-4534-8c8e-4b4a727dbc3b
  Args:
    source: Carlos_I_of_Portugal
    type: :Person
  AddLiteral (fb2a421e-05d5-4e13-b3ae-7d6d053670f8)
 Call ID: fb2a421e-05d5-4e13-b3ae-7d6d053670f8
  Args:
    literal_value: 1886
    relation: :hasMarriageYear
    source: Amélie_of_Orléans
    literal_type: xsd:integer
  AddTriple (f084c012-54a0-4397-b201-11a63296a29e)
 Call ID: f084c012-54a0-4397-b201-11a63296a29e
  Args:
    source: Amélie_of_Orléans
    relation: :hasRelation
    target: Carlos_I_of_Portugal
  AssignClass (2edcfda2-ee7f-488c-a794-45eada600ca5)
 Call ID: 2edcfda2-ee7f-488c-a794-45eada600ca5
  Args:
    source: Prince_Philippe_Count_of_Paris
    type: :Man
  AssignClass (fc585b42-2fcf-4199-84bc-9aceb1bb54b9)
 Call ID: fc585b42-2fcf-4199-84bc-9aceb1bb54b9
  Args:
    source: Prince_Philippe_Count_of_Paris
    type: :Person
  AssignClass (e3e462d5-ecb8-4297-b304-d80049b2b4cc)
 Call ID: e3e462d5-ecb8-4297-b304-d80049b2b4cc
  Args:
    type: :Woman
    source: Princess_Marie_Isabelle_dOrléans
  AssignClass (9f4781ad-c453-468c-8dbc-d57b5539eb87)
 Call ID: 9f4781ad-c453-468c-8dbc-d57b5539eb87
  Args:
    source: Princess_Marie_Isabelle_dOrléans
    type: :Person
  AddTriple (2a535ac3-e660-4db5-a22b-6338ca94114b)
 Call ID: 2a535ac3-e660-4db5-a22b-6338ca94114b
  Args:
    relation: :hasFather
    target: Prince_Philippe_Count_of_Paris
    source: Amélie_of_Orléans
  AddTriple (b7dd21ba-80d6-4e39-8ffb-bb759971db34)
 Call ID: b7dd21ba-80d6-4e39-8ffb-bb759971db34
  Args:
    target: Princess_Marie_Isabelle_dOrléans
    relation: :hasMother
    source: Amélie_of_Orléans
  AssignClass (62f545df-d188-41d2-8a62-d43b8eb0b737)
 Call ID: 62f545df-d188-41d2-8a62-d43b8eb0b737
  Args:
    source: Prince_Ferdinand_Philippe_Duke_of_Orléans
    type: :Man
  AssignClass (9051f46f-c778-419a-a7ae-9227453aca74)
 Call ID: 9051f46f-c778-419a-a7ae-9227453aca74
  Args:
    type: :Person
    source: Prince_Ferdinand_Philippe_Duke_of_Orléans
  AssignClass (62323445-f88e-41ca-bb7e-e9012704dace)
 Call ID: 62323445-f88e-41ca-bb7e-e9012704dace
  Args:
    source: Duchess_Helena_of_Mecklenburg_Schwerin
    type: :Woman
  AssignClass (15f157c9-61e0-4fe2-8d77-d2c198c02479)
 Call ID: 15f157c9-61e0-4fe2-8d77-d2c198c02479
  Args:
    type: :Person
    source: Duchess_Helena_of_Mecklenburg_Schwerin
  AddTriple (ebaca05e-de1b-452c-8f17-197e12eb1491)
 Call ID: ebaca05e-de1b-452c-8f17-197e12eb1491
  Args:
    relation: :hasFather
    target: Prince_Ferdinand_Philippe_Duke_of_Orléans
    source: Prince_Philippe_Count_of_Paris
  AddTriple (02d7a089-c410-46dd-943b-66207eb2d27f)
 Call ID: 02d7a089-c410-46dd-943b-66207eb2d27f
  Args:
    source: Prince_Philippe_Count_of_Paris
    target: Duchess_Helena_of_Mecklenburg_Schwerin
    relation: :hasMother
  AssignClass (e1c43e85-29c3-4e98-90d9-4b2a0aceaf15)
 Call ID: e1c43e85-29c3-4e98-90d9-4b2a0aceaf15
  Args:
    type: :Man
    source: Prince_Antoine_Duke_of_Montpensier
  AssignClass (01bc800a-4abf-44f8-a5f0-611cf9c53ac3)
 Call ID: 01bc800a-4abf-44f8-a5f0-611cf9c53ac3
  Args:
    source: Prince_Antoine_Duke_of_Montpensier
    type: :Person
  AssignClass (e10a39e8-658f-4606-af13-303072ad069b)
 Call ID: e10a39e8-658f-4606-af13-303072ad069b
  Args:
    type: :Woman
    source: Infanta_Luisa_Fernanda_of_Spain
  AssignClass (9c4b9729-85cd-4e7a-8c5e-9b2ea6582014)
 Call ID: 9c4b9729-85cd-4e7a-8c5e-9b2ea6582014
  Args:
    source: Infanta_Luisa_Fernanda_of_Spain
    type: :Person
  AddTriple (8682a340-4f81-4bee-a2c3-d2d211169a7d)
 Call ID: 8682a340-4f81-4bee-a2c3-d2d211169a7d
  Args:
    source: Princess_Marie_Isabelle_dOrléans
    target: Prince_Antoine_Duke_of_Montpensier
    relation: :hasFather
  AddTriple (bf937379-0cb7-47d0-8e34-51cc657894d3)
 Call ID: bf937379-0cb7-47d0-8e34-51cc657894d3
  Args:
    source: Princess_Marie_Isabelle_dOrléans
    relation: :hasMother
    target: Infanta_Luisa_Fernanda_of_Spain
  AssignClass (b6d508c0-5989-40b9-930c-71fbd0c69032)
 Call ID: b6d508c0-5989-40b9-930c-71fbd0c69032
  Args:
    type: :Man
    source: King_Louis_Philippe_I_of_France
  AssignClass (ec3f5a6a-5ce9-4f84-9dea-b4fb0605eec2)
 Call ID: ec3f5a6a-5ce9-4f84-9dea-b4fb0605eec2
  Args:
    type: :Person
    source: King_Louis_Philippe_I_of_France
  AssignClass (5c6e17c0-243b-4063-8484-48f21c344f4a)
 Call ID: 5c6e17c0-243b-4063-8484-48f21c344f4a
  Args:
    source: Maria_Amalia_of_the_Two_Sicilies
    type: :Woman
  AssignClass (c1b00db1-fe1b-4cf5-b7e6-bbf2fce32251)
 Call ID: c1b00db1-fe1b-4cf5-b7e6-bbf2fce32251
  Args:
    source: Maria_Amalia_of_the_Two_Sicilies
    type: :Person
  AddTriple (34db6919-87d0-4e68-a45d-efdc8ac024ed)
 Call ID: 34db6919-87d0-4e68-a45d-efdc8ac024ed
  Args:
    source: Prince_Ferdinand_Philippe_Duke_of_Orléans
    target: King_Louis_Philippe_I_of_France
    relation: :hasFather
  AddTriple (82d7c064-329c-454e-a8ef-f0192bcd5537)
 Call ID: 82d7c064-329c-454e-a8ef-f0192bcd5537
  Args:
    target: Maria_Amalia_of_the_Two_Sicilies
    relation: :hasMother
    source: Prince_Ferdinand_Philippe_Duke_of_Orléans
  AddTriple (e5accf34-c30d-492c-b349-b6813f16583d)
 Call ID: e5accf34-c30d-492c-b349-b6813f16583d
  Args:
    source: Prince_Antoine_Duke_of_Montpensier
    relation: :hasFather
    target: King_Louis_Philippe_I_of_France
  AddTriple (c402f354-8150-4684-bff3-5c54de3d44cb)
 Call ID: c402f354-8150-4684-bff3-5c54de3d44cb
  Args:
    source: Prince_Antoine_Duke_of_Montpensier
    relation: :hasMother
    target: Maria_Amalia_of_the_Two_Sicilies
  AssignClass (cc45a2a8-690e-4191-b64a-3536c972b4de)
 Call ID: cc45a2a8-690e-4191-b64a-3536c972b4de
  Args:
    source: King_Luís_I_of_Portugal
    type: :Man
  AssignClass (84df30b7-bdc4-474f-9f38-e20751e11ea4)
 Call ID: 84df30b7-bdc4-474f-9f38-e20751e11ea4
  Args:
    type: :Person
    source: King_Luís_I_of_Portugal
  AssignClass (513e8cb7-945e-48a2-83af-a1769d44f8f4)
 Call ID: 513e8cb7-945e-48a2-83af-a1769d44f8f4
  Args:
    source: Maria_Pia_of_Savoy
    type: :Woman
  AssignClass (352d1eae-2515-4e4b-9d06-e54f58de8c23)
 Call ID: 352d1eae-2515-4e4b-9d06-e54f58de8c23
  Args:
    source: Maria_Pia_of_Savoy
    type: :Person
  AddTriple (8a2a17a5-bfd9-423e-b883-3085de35dc4d)
 Call ID: 8a2a17a5-bfd9-423e-b883-3085de35dc4d
  Args:
    relation: :hasFather
    target: King_Luís_I_of_Portugal
    source: Carlos_I_of_Portugal
  AddTriple (1b0df307-9247-4798-b6e0-b78d0d146fb9)
 Call ID: 1b0df307-9247-4798-b6e0-b78d0d146fb9
  Args:
    source: Carlos_I_of_Portugal
    relation: :hasMother
    target: Maria_Pia_of_Savoy
  AssignClass (09cc9252-8929-4aa9-b50b-64361f36681e)
 Call ID: 09cc9252-8929-4aa9-b50b-64361f36681e
  Args:
    source: Prince_Dom_Luís_Filipe
    type: :Man
  AssignClass (d77ebb12-78a1-40c1-bd4e-2e575ad5f220)
 Call ID: d77ebb12-78a1-40c1-bd4e-2e575ad5f220
  Args:
    source: Prince_Dom_Luís_Filipe
    type: :Person
  AssignClass (d22b0b23-079c-4aa4-ac39-f8e99a39d89f)
 Call ID: d22b0b23-079c-4aa4-ac39-f8e99a39d89f
  Args:
    source: Infante_Dom_Manuel_II
    type: :Man
  AssignClass (c8e81969-b41a-4099-ba46-886499a880bd)
 Call ID: c8e81969-b41a-4099-ba46-886499a880bd
  Args:
    source: Infante_Dom_Manuel_II
    type: :Person
  AddTriple (97dd9a99-01fe-408e-bea7-d3bb99d8c548)
 Call ID: 97dd9a99-01fe-408e-bea7-d3bb99d8c548
  Args:
    source: Prince_Dom_Luís_Filipe
    target: Carlos_I_of_Portugal
    relation: :hasFather
  AddTriple (1010a85d-af78-41e6-baca-5606721a9893)
 Call ID: 1010a85d-af78-41e6-baca-5606721a9893
  Args:
    source: Prince_Dom_Luís_Filipe
    target: Amélie_of_Orléans
    relation: :hasMother
  AddTriple (17267813-5c2a-4885-91d0-656e70f07099)
 Call ID: 17267813-5c2a-4885-91d0-656e70f07099
  Args:
    source: Infante_Dom_Manuel_II
    target: Carlos_I_of_Portugal
    relation: :hasFather
  AddTriple (ba89b9f9-55ba-4af7-93c3-e94b2aa7caa9)
 Call ID: ba89b9f9-55ba-4af7-93c3-e94b2aa7caa9
  Args:
    target: Amélie_of_Orléans
    relation: :hasMother
    source: Infante_Dom_Manuel_II
  Finish (af0daa33-9726-4dac-981d-c8346d10ede9)
 Call ID: af0daa33-9726-4dac-981d-c8346d10ede9
  Args: