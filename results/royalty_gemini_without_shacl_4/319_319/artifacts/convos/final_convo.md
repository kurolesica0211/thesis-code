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
Don Carlos, Prince of Bourbon-Two Sicilies, Infante of Spain (Full Italian name: Carlo Maria Francesco d'Assisi Pasquale Ferdinando Antonio di Padova Francesco de Paola Alfonso Andrea Avelino Tancredi, Principe di Borbone delle Due Sicilie, Infante di Spagna; 10 November 1870 – 11 November 1949) was the son of Prince Alfonso of the Two Sicilies, Count of Caserta and Princess Maria Antonietta of Bourbon-Two Sicilies, and nephew of the last King of the Two Sicilies, Francis II.


Marriages and children

On 14 February 1901 in Madrid, Carlos married Mercedes, Princess of Asturias, elder daughter of the late King Alfonso XII of Spain and of his wife Archduchess Maria Christina of Austria.
Mercedes was the elder sister and heir presumptive to King Alfonso XIII of Spain, an unmarried teenager.
A week before the wedding, on 7 February, Carlos was given the title of Infante of Spain.
In 1907, Carlos married secondly to Princess Louise of Orléans, daughter of Prince Philippe, Count of Paris.
The couple had four children:


Prince Carlos's descendants include King Felipe VI of Spain, Prince Pedro, Duke of Calabria, Prince Pedro Carlos of Orléans-Braganza, and Philip, Hereditary Prince of Yugoslavia, among others.
Military service

Carlos served in the Spanish Army in the Spanish–American War and received the Military Order of Maria Cristina.
Two Sicilies succession

In 1894, Carlos's father Alfonso became the head of the House of Bourbon-Two Sicilies.
On marrying his first wife, Carlos renounced on 14 December 1900 his future rights of succession to the non-existent Crown of Two Sicilies in an official document, known as the Act of Cannes, subject to a requirement in the Treaty of Naples of 1759 and the Pragmatic Decree of 6 October 1759 that the Crown of Spain should not be combined with the "Italian Sovereignty".
In 1960, Carlos' elder brother Ferdinand died without male issue, and a dispute arose between Carlos' son Alfonso and Carlos' younger brother Ranieri on the headship of the house, this with competing claims: by the law of primogeniture, Carlos' son Alfonso was considered the heir, but Ranieri claimed that Carlos had renounced his rights and those of his descendants according to the Act of Cannes.
Alfonso refuted that claim by stating that it was only a promise from his father to relinquish this right if the crown of the Kingdom of the Two Sicilies were to be united with the Spanish Crown.
Since this did not happen, the act had no effect and Carlos' son Alfonso reclaimed his rights.
Alfonso's claim was recognised by the heads of the different lines of the House of Bourbon, although not by the head of the Orleans family, and in 1983 the Spanish Council of State, following an investigation by the Ministries of Justice and Foreign Affairs, the Royal Academy of Jurisprudence and Legislation and the Institute Salazar y Castro concluded unanimously in favour of Infante Don Alfonso's only son, Prince and Infante Don Carlos, a position shared by the Spanish Royal House.



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
  AssignClass (7cfd036c-9819-4fb6-b1b0-977eb9cb7274)
 Call ID: 7cfd036c-9819-4fb6-b1b0-977eb9cb7274
  Args:
    source: DonCarlos
    type: :Man
  AssignClass (e751fa23-053c-4112-8e82-8516ffbf41a0)
 Call ID: e751fa23-053c-4112-8e82-8516ffbf41a0
  Args:
    source: DonCarlos
    type: :Person
  AddLiteral (765db323-6501-4c24-95d7-42312ab2348f)
 Call ID: 765db323-6501-4c24-95d7-42312ab2348f
  Args:
    literal_type: xsd:integer
    literal_value: 1870
    relation: :hasBirthYear
    source: DonCarlos
  AddLiteral (42a7cfd7-dcc6-4902-84dc-3387dd5addd2)
 Call ID: 42a7cfd7-dcc6-4902-84dc-3387dd5addd2
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 1949
    source: DonCarlos
  AssignClass (32db6abb-4456-460b-a496-2b00358cafc8)
 Call ID: 32db6abb-4456-460b-a496-2b00358cafc8
  Args:
    source: PrinceAlfonsoTwoSicilies
    type: :Man
  AssignClass (50908944-7279-4a47-8498-678a5ef0709e)
 Call ID: 50908944-7279-4a47-8498-678a5ef0709e
  Args:
    source: PrinceAlfonsoTwoSicilies
    type: :Person
  AssignClass (519fd216-23c9-4da4-bca4-55891130cdbf)
 Call ID: 519fd216-23c9-4da4-bca4-55891130cdbf
  Args:
    source: PrincessMariaAntonietta
    type: :Woman
  AssignClass (4ac8518c-0ffe-410a-99f5-2756231a8de4)
 Call ID: 4ac8518c-0ffe-410a-99f5-2756231a8de4
  Args:
    type: :Person
    source: PrincessMariaAntonietta
  AddTriple (5db95400-229c-4b29-80a5-d772c566dcc9)
 Call ID: 5db95400-229c-4b29-80a5-d772c566dcc9
  Args:
    target: PrinceAlfonsoTwoSicilies
    relation: :hasFather
    source: DonCarlos
  AddTriple (c4df97e3-2cb0-4de7-b95f-a75e23d94562)
 Call ID: c4df97e3-2cb0-4de7-b95f-a75e23d94562
  Args:
    target: PrincessMariaAntonietta
    relation: :hasMother
    source: DonCarlos
  AssignClass (0885fdb5-3bfe-42bb-b251-7d1b730e8d70)
 Call ID: 0885fdb5-3bfe-42bb-b251-7d1b730e8d70
  Args:
    source: FrancisII
    type: :Man
  AssignClass (6e7ecb17-dd4e-47d2-888c-7c75e854dc10)
 Call ID: 6e7ecb17-dd4e-47d2-888c-7c75e854dc10
  Args:
    source: FrancisII
    type: :Person
  AssignClass (7be2994f-648d-4066-a988-c302bd91374a)
 Call ID: 7be2994f-648d-4066-a988-c302bd91374a
  Args:
    type: :Woman
    source: MercedesPrincessAsturias
  AssignClass (b73cd352-c628-4141-ab87-5cfa43f7ebdf)
 Call ID: b73cd352-c628-4141-ab87-5cfa43f7ebdf
  Args:
    type: :Person
    source: MercedesPrincessAsturias
  AddTriple (3028ea70-e88e-4e2b-9c79-a0c3496a3a31)
 Call ID: 3028ea70-e88e-4e2b-9c79-a0c3496a3a31
  Args:
    source: DonCarlos
    relation: :hasRelation
    target: MercedesPrincessAsturias
  AssignClass (f2467e1e-9fb2-4e36-a612-57da363fa8b5)
 Call ID: f2467e1e-9fb2-4e36-a612-57da363fa8b5
  Args:
    source: AlfonsoXII
    type: :Man
  AssignClass (2a3bba99-14d8-4616-9e9f-5288932e4a75)
 Call ID: 2a3bba99-14d8-4616-9e9f-5288932e4a75
  Args:
    source: AlfonsoXII
    type: :Person
  AssignClass (c01cdabe-4e18-4347-9fdc-03f19cb71894)
 Call ID: c01cdabe-4e18-4347-9fdc-03f19cb71894
  Args:
    type: :Woman
    source: MariaChristinaAustria
  AssignClass (aefd29b2-1884-47e8-ac8d-9869ee835a0a)
 Call ID: aefd29b2-1884-47e8-ac8d-9869ee835a0a
  Args:
    type: :Person
    source: MariaChristinaAustria
  AddTriple (d61acd9a-4258-4f32-b445-57a415d6b265)
 Call ID: d61acd9a-4258-4f32-b445-57a415d6b265
  Args:
    target: AlfonsoXII
    relation: :hasFather
    source: MercedesPrincessAsturias
  AddTriple (daa1884b-a8b8-4336-9a12-660686956896)
 Call ID: daa1884b-a8b8-4336-9a12-660686956896
  Args:
    target: MariaChristinaAustria
    relation: :hasMother
    source: MercedesPrincessAsturias
  AssignClass (3fb8750d-efaa-4b2b-9b1c-3a1ee6290acc)
 Call ID: 3fb8750d-efaa-4b2b-9b1c-3a1ee6290acc
  Args:
    source: AlfonsoXIII
    type: :Man
  AssignClass (3589a309-6fa1-4333-b594-090658c01ce4)
 Call ID: 3589a309-6fa1-4333-b594-090658c01ce4
  Args:
    type: :Person
    source: AlfonsoXIII
  AddTriple (7236c1c1-a4e1-40ef-b9a1-f7147df34a3e)
 Call ID: 7236c1c1-a4e1-40ef-b9a1-f7147df34a3e
  Args:
    source: MercedesPrincessAsturias
    target: AlfonsoXIII
    relation: :isSisterOf
  AssignClass (acaf9283-567c-4c37-b6d8-1649b5795c4b)
 Call ID: acaf9283-567c-4c37-b6d8-1649b5795c4b
  Args:
    type: :Woman
    source: PrincessLouiseOrleans
  AssignClass (c3f50d16-d191-48b3-9f2c-9b1304b5d411)
 Call ID: c3f50d16-d191-48b3-9f2c-9b1304b5d411
  Args:
    type: :Person
    source: PrincessLouiseOrleans
  AddTriple (d82bb30f-892c-453f-b737-56e0adba805f)
 Call ID: d82bb30f-892c-453f-b737-56e0adba805f
  Args:
    source: DonCarlos
    relation: :hasRelation
    target: PrincessLouiseOrleans
  AssignClass (18cea416-e489-48cf-906e-f8b826e9faa5)
 Call ID: 18cea416-e489-48cf-906e-f8b826e9faa5
  Args:
    source: PrincePhilippeCountParis
    type: :Man
  AssignClass (3409e92d-dd42-4e41-a9f0-57239dafdb33)
 Call ID: 3409e92d-dd42-4e41-a9f0-57239dafdb33
  Args:
    source: PrincePhilippeCountParis
    type: :Person
  AddTriple (82f71bc3-c07b-4b6d-8d52-b22a011b5388)
 Call ID: 82f71bc3-c07b-4b6d-8d52-b22a011b5388
  Args:
    target: PrincePhilippeCountParis
    relation: :hasFather
    source: PrincessLouiseOrleans
  AssignClass (58a0a7a2-1351-4057-b6c7-9184386b9067)
 Call ID: 58a0a7a2-1351-4057-b6c7-9184386b9067
  Args:
    source: FerdinandTwoSicilies
    type: :Man
  AssignClass (d7fc71d2-0021-407c-a0fc-40e2cb92c279)
 Call ID: d7fc71d2-0021-407c-a0fc-40e2cb92c279
  Args:
    type: :Person
    source: FerdinandTwoSicilies
  AddTriple (efb3fc1d-e0d8-43a0-b42d-566ccec0f6d5)
 Call ID: efb3fc1d-e0d8-43a0-b42d-566ccec0f6d5
  Args:
    source: FerdinandTwoSicilies
    relation: :isBrotherOf
    target: DonCarlos
  AssignClass (7e4a014d-7e8c-4f9b-84e9-9cceb1800a6f)
 Call ID: 7e4a014d-7e8c-4f9b-84e9-9cceb1800a6f
  Args:
    type: :Man
    source: AlfonsoSonOfCarlos
  AssignClass (ae750006-e371-4454-a2a0-c9a5f482282f)
 Call ID: ae750006-e371-4454-a2a0-c9a5f482282f
  Args:
    source: AlfonsoSonOfCarlos
    type: :Person
  AddTriple (54c2132c-b92b-4ab5-a7d6-152dff9ab452)
 Call ID: 54c2132c-b92b-4ab5-a7d6-152dff9ab452
  Args:
    source: AlfonsoSonOfCarlos
    relation: :isSonOf
    target: DonCarlos
  AssignClass (640f503d-9a3c-41e6-b7ab-92098cf1119a)
 Call ID: 640f503d-9a3c-41e6-b7ab-92098cf1119a
  Args:
    source: RanieriTwoSicilies
    type: :Man
  AssignClass (32850efe-35e2-4ba9-bc8d-ec41dda5dc24)
 Call ID: 32850efe-35e2-4ba9-bc8d-ec41dda5dc24
  Args:
    source: RanieriTwoSicilies
    type: :Person
  AddTriple (73ae72da-7760-4c29-bd8f-c377be5e8ed7)
 Call ID: 73ae72da-7760-4c29-bd8f-c377be5e8ed7
  Args:
    source: RanieriTwoSicilies
    relation: :isBrotherOf
    target: DonCarlos
  Finish (7a458834-c0c8-4801-9436-827fef9239c4)
 Call ID: 7a458834-c0c8-4801-9436-827fef9239c4
  Args: