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
Prince Pedro Henrique of Orléans-Braganza (13 September 1909 – 5 July 1981), nicknamed The Expected Prince (Portuguese: O Príncipe Esperado) was the eldest son of Prince Luís of Orléans-Braganza and Princess Maria di Grazia of Bourbon-Two Sicilies, and head of the Vassouras branch of the Imperial House of Brazil from 1921 until his death in 1981.
Pedro succeeded his grandmother, Princess Isabel of Brazil, as head of the family after her death.
His father, Prince Luiz of Orléans-Braganza, was the second son of the heir to the defunct Brazilian throne, the Princess Imperial Isabel, and Prince Gaston, Count of Eu.
His mother was Princess Maria Pia of Bourbon-Two Sicilies.
His godparents were his paternal grandmother, Princess Isabel of Brazil, and maternal grandfather Prince Alfonso, Count of Caserta, Head of the royal house of the Two Sicilies.
In the same year Brazil's banishment of the Orléans-Braganzas was revoked by the then President Epitácio Pessoa.
Pedro Henrique accompanied Count d'Eu when he led part of the Imperial Family back to Brazil, without the aged and infirm Princess Isabel.
Upon the death of his father in 1920 Pedro Henrique became claimant to the title of Prince Imperial, but on 14 November 1921 Princess Isabel died at the Castle d'Eu.
So, aged 12 Prince Pedro Henrique became the head of the imperial family.
He continued living in France with his mother, Princess Maria Pia, where she thought he could get a better education with his siblings Luiz Gastão and Pia Maria.
Prince Pedro Henrique was only able to return to Brazil in 1945, when the Second World War ended.
His cousin, Prince Pedro Gastão of Orléans-Braganza, the eldest son of Pedro de Alcântara, Prince of Grão-Pará, challenged Pedro Henrique's claim to the succession in 1946, on the basis that his father's renunciation had no legal force.
In 1951, D. Pedro Henrique bought a farm, Fazenda Santa Maria, in the town of Jacarezinho, interior of Paraná.
Pedro Henrique resided at a site called Santa Maria until the end of his life.
Marriage and children

Pedro Henrique married Princess Maria Elisabeth of Bavaria at Nymphenburg Palace, Bavaria, on 19 August 1937.



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
  AssignClass (059878f2-797b-4a14-ac8c-7910b440f095)
 Call ID: 059878f2-797b-4a14-ac8c-7910b440f095
  Args:
    type: :Man
    source: :PedroHenriqueOfOrleansBraganza
  AssignClass (a38ea326-4608-44bb-8854-8bd1676ba3f6)
 Call ID: a38ea326-4608-44bb-8854-8bd1676ba3f6
  Args:
    type: :Person
    source: :PedroHenriqueOfOrleansBraganza
  AddLiteral (d3c9f636-21d0-4ac7-900e-e3d6b4690552)
 Call ID: d3c9f636-21d0-4ac7-900e-e3d6b4690552
  Args:
    source: :PedroHenriqueOfOrleansBraganza
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1909
  AddLiteral (394c1ea6-e732-4e33-b272-aac35b3e1ba8)
 Call ID: 394c1ea6-e732-4e33-b272-aac35b3e1ba8
  Args:
    source: :PedroHenriqueOfOrleansBraganza
    literal_value: 1981
    literal_type: xsd:integer
    relation: :hasDeathYear
  AddLiteral (4d5bbd11-a207-471f-9b0a-80e62a3dd13e)
 Call ID: 4d5bbd11-a207-471f-9b0a-80e62a3dd13e
  Args:
    relation: :knownAs
    literal_value: The Expected Prince
    literal_type: xsd:string
    source: :PedroHenriqueOfOrleansBraganza
  AddLiteral (c34b20bd-e1f9-4340-9117-47eb1d66170f)
 Call ID: c34b20bd-e1f9-4340-9117-47eb1d66170f
  Args:
    source: :PedroHenriqueOfOrleansBraganza
    relation: :alsoKnownAs
    literal_value: O Príncipe Esperado
    literal_type: xsd:string
  AssignClass (f71e17e7-4e47-4237-a5ed-4a8900345d20)
 Call ID: f71e17e7-4e47-4237-a5ed-4a8900345d20
  Args:
    source: :LuisOfOrleansBraganza
    type: :Man
  AssignClass (74920bdc-0ef0-4c7b-baf3-83e589242d09)
 Call ID: 74920bdc-0ef0-4c7b-baf3-83e589242d09
  Args:
    source: :LuisOfOrleansBraganza
    type: :Person
  AssignClass (844443bd-feb3-459f-b00a-98e42ed4f8d1)
 Call ID: 844443bd-feb3-459f-b00a-98e42ed4f8d1
  Args:
    type: :Woman
    source: :MariaDiGraziaOfBourbonTwoSicilies
  AssignClass (50d0c4f3-8014-4073-a0d6-d0dbca946638)
 Call ID: 50d0c4f3-8014-4073-a0d6-d0dbca946638
  Args:
    source: :MariaDiGraziaOfBourbonTwoSicilies
    type: :Person
  AddTriple (f3662e66-214c-4838-bc4f-698748bae168)
 Call ID: f3662e66-214c-4838-bc4f-698748bae168
  Args:
    source: :PedroHenriqueOfOrleansBraganza
    relation: :hasFather
    target: :LuisOfOrleansBraganza
  AddTriple (3da20a59-ca6a-448a-84bd-36045d9c0044)
 Call ID: 3da20a59-ca6a-448a-84bd-36045d9c0044
  Args:
    target: :MariaDiGraziaOfBourbonTwoSicilies
    relation: :hasMother
    source: :PedroHenriqueOfOrleansBraganza
  AssignClass (d9d4f843-e45c-44d8-a7bd-d5833a0002cd)
 Call ID: d9d4f843-e45c-44d8-a7bd-d5833a0002cd
  Args:
    type: :Woman
    source: :IsabelOfBrazil
  AssignClass (e35f22c3-d7be-4ad7-98c1-104b20b42909)
 Call ID: e35f22c3-d7be-4ad7-98c1-104b20b42909
  Args:
    source: :IsabelOfBrazil
    type: :Person
  AddTriple (1fda563e-cf23-4ce5-b9b4-9da49b93063c)
 Call ID: 1fda563e-cf23-4ce5-b9b4-9da49b93063c
  Args:
    source: :LuisOfOrleansBraganza
    relation: :hasFather
    target: :GastonCountOfEu
  AddTriple (14d83d38-2b7c-466f-b628-d51e6c8cac3c)
 Call ID: 14d83d38-2b7c-466f-b628-d51e6c8cac3c
  Args:
    relation: :hasMother
    target: :IsabelOfBrazil
    source: :LuisOfOrleansBraganza
  AssignClass (bac6ff93-2ce7-46ef-be35-98726bcb02a2)
 Call ID: bac6ff93-2ce7-46ef-be35-98726bcb02a2
  Args:
    source: :GastonCountOfEu
    type: :Man
  AssignClass (e7c68066-a881-4a22-9bc1-0b7c83fc79ac)
 Call ID: e7c68066-a881-4a22-9bc1-0b7c83fc79ac
  Args:
    type: :Person
    source: :GastonCountOfEu
  AssignClass (35126815-f4cb-487c-9326-f41dcf447dcd)
 Call ID: 35126815-f4cb-487c-9326-f41dcf447dcd
  Args:
    source: :MariaPiaOfBourbonTwoSicilies
    type: :Woman
  AssignClass (58476ce4-a102-4617-bedb-2801b1f3cb01)
 Call ID: 58476ce4-a102-4617-bedb-2801b1f3cb01
  Args:
    type: :Person
    source: :MariaPiaOfBourbonTwoSicilies
  AssignClass (d6496f25-1d96-4019-9514-d6dad490dcd5)
 Call ID: d6496f25-1d96-4019-9514-d6dad490dcd5
  Args:
    type: :Man
    source: :AlfonsoCountOfCaserta
  AssignClass (e6f0c135-9afe-4aa7-8113-2562b088858a)
 Call ID: e6f0c135-9afe-4aa7-8113-2562b088858a
  Args:
    source: :AlfonsoCountOfCaserta
    type: :Person
  AssignClass (140c52fb-62b9-498b-83b7-7d82ea48a7b2)
 Call ID: 140c52fb-62b9-498b-83b7-7d82ea48a7b2
  Args:
    source: :LuizGastao
    type: :Man
  AssignClass (c3f2f89f-9597-4dd3-b417-4751317c41b7)
 Call ID: c3f2f89f-9597-4dd3-b417-4751317c41b7
  Args:
    source: :LuizGastao
    type: :Person
  AssignClass (cc340fd9-10de-4454-9c34-421f9108ca9f)
 Call ID: cc340fd9-10de-4454-9c34-421f9108ca9f
  Args:
    type: :Woman
    source: :PiaMaria
  AssignClass (2401a40c-9775-4d1b-a2f0-8793f5a80213)
 Call ID: 2401a40c-9775-4d1b-a2f0-8793f5a80213
  Args:
    source: :PiaMaria
    type: :Person
  AddTriple (311e5eb6-e2cc-4a30-a573-baf18fdca7b1)
 Call ID: 311e5eb6-e2cc-4a30-a573-baf18fdca7b1
  Args:
    target: :LuizGastao
    relation: :isSiblingOf
    source: :PedroHenriqueOfOrleansBraganza
  AddTriple (f55e77ff-6b19-4137-ad6e-597370d541b8)
 Call ID: f55e77ff-6b19-4137-ad6e-597370d541b8
  Args:
    source: :PedroHenriqueOfOrleansBraganza
    relation: :isSiblingOf
    target: :PiaMaria
  AssignClass (c9bedfb8-a8bd-4878-a0e9-3bc1158d4a8b)
 Call ID: c9bedfb8-a8bd-4878-a0e9-3bc1158d4a8b
  Args:
    type: :Man
    source: :PedroGastaoOfOrleansBraganza
  AssignClass (d1da81b9-334f-454f-a6e2-d2819b24023c)
 Call ID: d1da81b9-334f-454f-a6e2-d2819b24023c
  Args:
    source: :PedroGastaoOfOrleansBraganza
    type: :Person
  AssignClass (9912d7ec-40fb-409c-b2d6-efa7df4459ef)
 Call ID: 9912d7ec-40fb-409c-b2d6-efa7df4459ef
  Args:
    type: :Man
    source: :PedroDeAlcantaraPrinceOfGraoPara
  AssignClass (230beb8b-d7fa-4d0a-9cf9-7dc4fc30fc4b)
 Call ID: 230beb8b-d7fa-4d0a-9cf9-7dc4fc30fc4b
  Args:
    source: :PedroDeAlcantaraPrinceOfGraoPara
    type: :Person
  AddTriple (bb1019c4-178a-4bc6-a5e1-856cd6aeb3e2)
 Call ID: bb1019c4-178a-4bc6-a5e1-856cd6aeb3e2
  Args:
    target: :PedroDeAlcantaraPrinceOfGraoPara
    relation: :hasFather
    source: :PedroGastaoOfOrleansBraganza
  AssignClass (d5d10858-343f-43a1-a19e-2d8952d69b71)
 Call ID: d5d10858-343f-43a1-a19e-2d8952d69b71
  Args:
    source: :MariaElisabethOfBavaria
    type: :Woman
  AssignClass (fb8a091a-2feb-49ef-9085-09ea2da83367)
 Call ID: fb8a091a-2feb-49ef-9085-09ea2da83367
  Args:
    source: :MariaElisabethOfBavaria
    type: :Person
  AddTriple (8dfb1273-7599-47a8-986d-a263c13c9513)
 Call ID: 8dfb1273-7599-47a8-986d-a263c13c9513
  Args:
    source: :PedroHenriqueOfOrleansBraganza
    relation: :hasRelation
    target: :MariaElisabethOfBavaria
  AddLiteral (bbeca640-87cb-4934-9ac7-e38d88cad7b3)
 Call ID: bbeca640-87cb-4934-9ac7-e38d88cad7b3
  Args:
    literal_type: xsd:integer
    literal_value: 1937
    relation: :hasMarriageYear
    source: :PedroHenriqueOfOrleansBraganza
  Finish (bf95e1cf-1b47-4069-8191-ca3c13c89ffe)
 Call ID: bf95e1cf-1b47-4069-8191-ca3c13c89ffe
  Args: