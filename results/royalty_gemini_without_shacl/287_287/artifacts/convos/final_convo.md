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
The Duchess of Montpensier


The Count of ÉvreuxThe Countess of Évreux


Princess Béatrice


The Duke of OrléansThe Duchess of Orléans


The Dowager Countess of La Marche


The Countess of Schönborn-Buchheim


Princess Hélène, Countess of Limburg Stirum


The Dowager Duchess of Calabria


The Dowager Duchess of Württemberg


Princess Claude, Mrs. Gandolfi


Princess Chantal, Baroness of Sambucy de Sorgue


Prince Jean Carl Pierre Marie d'Orléans, Count of Paris (born 19 May 1965) is the current head of the House of Orléans.
Jean is the senior male descendant by primogeniture in the male-line of Louis Philippe I, King of the French, and thus according to the Orléanists the legitimate claimant to the defunct throne of France as Jean IV.
Jean is the second son of Henri, Count of Paris (1933–2019) and his former wife Duchess Marie-Thérèse of Württemberg (born 1934).
Biography

Early life and education

Jean d'Orléans was born on 19 May 1965 in Boulogne-Billancourt, the son of Henri of Orleans and Maria Theresa of Württemberg.
He received as godfather, his maternal uncle, Carl of Württemberg, and as godmother, his paternal aunt, Princess Chantal of Orleans.
Jean completed his national service as an officer, first taking four months of classes at the Saumur Cavalry School.
Jean is multilingual, speaking French, English, and German.
First engagement

Prince Jean was due to marry Duchess Tatjana of Oldenburg (b. 1974) in 2001.
However, the wedding was cancelled at the last moment because of a dispute over religious denomination: Jean's father, Henri, feared the Orléans claim to the throne would be compromised if there were to be a Protestant heir.
Second engagement and marriage

On 29 November 2008, Henri, then Count of Paris, announced the engagement of Jean, the then Duke of Vendôme, to Maria Magdalena Philomena Juliana Johanna de Tornos y Steinhart, born in Vienna on 19 June 1977.
Lawsuit

In 2021, Jean filed a lawsuit against the Saint-Louis foundation, demanding €1 million in damages and the return of five properties, including the Château d'Amboise.
In 1886, the château was bequeathed to the Institute of France by Jean's ancestor Henri d’Orléans, with the caveat that the property would never be altered by the institute.
The Saint-Louis foundation was later founded by Jean's grandfather, Henri VI, Count of Paris, in 1974.
Jean's lawsuit alleges that the Institute violated their contract to never alter the property, after they announced plans to transform the Pavillon d’Enghien into a €760-a-night luxury hotel, containing a spa and gastronomic restaurant.
Jean had previously lived in the château from 2001 to September 2021 rent-free, but was forcefully evicted by the institute after they began to demand he pay rent, which Jean viewed as a violation of their contract.
Family

Jean and his wife Philomena have six children: 


Politics

Jean believes that the people of France are "monarchist at heart" and argues that they long for a non-partisan figurehead.
Jean has also expressed his opposition to same-sex marriage, having participated in the La Manif pour tous protests, as well as abortion.
In May 2019, Jean met with French President Emmanuel Macron, Brigitte Macron, and Italian President Sergio Mattarella in his then-home in the Château d'Amboise.


Titles, styles and honours

Titles in pretense

He was created Duke of Vendôme (French: Duc de Vendôme) by his paternal grandfather, on 27 September 1987.
Following the death of his father, it was initially thought that Prince Jean would not assume the title of Count of Paris for several months after his father's death, and possibly not for as much as one year.
Honours

National

Dynastic

Ancestry

Jean is a direct male-line descendant of Louis Philippe I, the last French king, who in turn was a descendant of Philippe I, Duke of Orléans, the younger brother of Louis XIV.
Jean is also descended from Charles X, brother of Louis XVI; and the Bourbons of Spain, the Two Sicilies and Parma.



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
  AssignClass (1223e1c9-b1af-4d66-b96d-3dc3851513c4)
 Call ID: 1223e1c9-b1af-4d66-b96d-3dc3851513c4
  Args:
    type: :Man
    source: :Jean_dOrleans
  AssignClass (cfc54445-e378-4dd2-84ff-0157504d91e4)
 Call ID: cfc54445-e378-4dd2-84ff-0157504d91e4
  Args:
    source: :Jean_dOrleans
    type: :Person
  AddLiteral (6a88a444-57e0-4a4e-83d9-1d4d9eebf1ac)
 Call ID: 6a88a444-57e0-4a4e-83d9-1d4d9eebf1ac
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1965
    source: :Jean_dOrleans
  AssignClass (a89567d3-859b-4ed4-ac03-3b5b0e2c3fb6)
 Call ID: a89567d3-859b-4ed4-ac03-3b5b0e2c3fb6
  Args:
    type: :Man
    source: :Henri_Count_of_Paris
  AssignClass (49bd87ed-37aa-480f-bb04-971098af2cd2)
 Call ID: 49bd87ed-37aa-480f-bb04-971098af2cd2
  Args:
    source: :Henri_Count_of_Paris
    type: :Person
  AddLiteral (1f6940a8-85b5-433d-b343-48b5f29f7902)
 Call ID: 1f6940a8-85b5-433d-b343-48b5f29f7902
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1933
    source: :Henri_Count_of_Paris
  AddLiteral (a08b9840-5d29-48a5-8c43-82198fd53d66)
 Call ID: a08b9840-5d29-48a5-8c43-82198fd53d66
  Args:
    relation: :hasDeathYear
    literal_value: 2019
    source: :Henri_Count_of_Paris
    literal_type: xsd:integer
  AssignClass (b7e27406-f441-4b8b-8654-64863d4cf068)
 Call ID: b7e27406-f441-4b8b-8654-64863d4cf068
  Args:
    source: :Marie_Therese_of_Wurttemberg
    type: :Woman
  AssignClass (e26bdf20-a293-43e8-92e6-4030173760c4)
 Call ID: e26bdf20-a293-43e8-92e6-4030173760c4
  Args:
    source: :Marie_Therese_of_Wurttemberg
    type: :Person
  AddLiteral (84fe858a-747d-4c73-a97f-5de30540bacf)
 Call ID: 84fe858a-747d-4c73-a97f-5de30540bacf
  Args:
    relation: :hasBirthYear
    source: :Marie_Therese_of_Wurttemberg
    literal_value: 1934
    literal_type: xsd:integer
  AddTriple (a9d64b93-733c-46cd-bf51-8d098f55c82c)
 Call ID: a9d64b93-733c-46cd-bf51-8d098f55c82c
  Args:
    source: :Jean_dOrleans
    relation: :hasFather
    target: :Henri_Count_of_Paris
  AddTriple (ba241415-091e-49b0-82f4-4caa1cc1b6c2)
 Call ID: ba241415-091e-49b0-82f4-4caa1cc1b6c2
  Args:
    source: :Jean_dOrleans
    target: :Marie_Therese_of_Wurttemberg
    relation: :hasMother
  AssignClass (d8a81b4a-e501-49b5-9be7-ae09873f7819)
 Call ID: d8a81b4a-e501-49b5-9be7-ae09873f7819
  Args:
    source: :Philomena_de_Tornos_y_Steinhart
    type: :Woman
  AssignClass (46003fd9-0b69-43d6-b14c-217569342e5a)
 Call ID: 46003fd9-0b69-43d6-b14c-217569342e5a
  Args:
    type: :Person
    source: :Philomena_de_Tornos_y_Steinhart
  AddLiteral (da08896a-b9e8-42c2-9108-8b64d03232be)
 Call ID: da08896a-b9e8-42c2-9108-8b64d03232be
  Args:
    source: :Philomena_de_Tornos_y_Steinhart
    literal_value: 1977
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddTriple (20a8a74d-5af5-4eea-b230-05ec1c578f91)
 Call ID: 20a8a74d-5af5-4eea-b230-05ec1c578f91
  Args:
    target: :Philomena_de_Tornos_y_Steinhart
    relation: :hasRelation
    source: :Jean_dOrleans
  AssignClass (0da9d8a3-cff7-4646-8d53-b7baed5b6b72)
 Call ID: 0da9d8a3-cff7-4646-8d53-b7baed5b6b72
  Args:
    source: :Carl_of_Wurttemberg
    type: :Man
  AssignClass (20313370-5156-4b9c-a641-914b827a588a)
 Call ID: 20313370-5156-4b9c-a641-914b827a588a
  Args:
    source: :Carl_of_Wurttemberg
    type: :Person
  AddTriple (2413bc51-7683-4fc9-a173-aa41035d67d5)
 Call ID: 2413bc51-7683-4fc9-a173-aa41035d67d5
  Args:
    source: :Carl_of_Wurttemberg
    target: :Jean_dOrleans
    relation: :isUncleOf
  AssignClass (5fc6fac0-bb93-44e1-ab95-67c1be707c65)
 Call ID: 5fc6fac0-bb93-44e1-ab95-67c1be707c65
  Args:
    source: :Princess_Chantal_of_Orleans
    type: :Woman
  AssignClass (8fd35678-a74b-4119-8cf6-9c1b8e79d9a4)
 Call ID: 8fd35678-a74b-4119-8cf6-9c1b8e79d9a4
  Args:
    type: :Person
    source: :Princess_Chantal_of_Orleans
  AddTriple (2afa74ff-cef3-42a8-ac2c-7a1c595153ed)
 Call ID: 2afa74ff-cef3-42a8-ac2c-7a1c595153ed
  Args:
    relation: :isAuntOf
    target: :Jean_dOrleans
    source: :Princess_Chantal_of_Orleans
  AssignClass (c5f0d53a-f7a6-4ba7-be7f-44980d971227)
 Call ID: c5f0d53a-f7a6-4ba7-be7f-44980d971227
  Args:
    source: :Louis_Philippe_I
    type: :Man
  AssignClass (c9609086-5a9d-4175-a352-6641a38022d3)
 Call ID: c9609086-5a9d-4175-a352-6641a38022d3
  Args:
    type: :Person
    source: :Louis_Philippe_I
  AddTriple (d81dfcfd-c621-4419-85d8-8c7fbe9eab80)
 Call ID: d81dfcfd-c621-4419-85d8-8c7fbe9eab80
  Args:
    relation: :hasAncestor
    target: :Louis_Philippe_I
    source: :Jean_dOrleans
  AssignClass (c7d5cfe2-c046-4075-a6c3-e5f0fa67f20f)
 Call ID: c7d5cfe2-c046-4075-a6c3-e5f0fa67f20f
  Args:
    source: :Philippe_I_Duke_of_Orleans
    type: :Man
  AssignClass (14508edf-3ce9-4011-8f62-ae547b7f6068)
 Call ID: 14508edf-3ce9-4011-8f62-ae547b7f6068
  Args:
    type: :Person
    source: :Philippe_I_Duke_of_Orleans
  AddTriple (7a870ea5-8a6e-4b8b-beb6-e45a25aa2601)
 Call ID: 7a870ea5-8a6e-4b8b-beb6-e45a25aa2601
  Args:
    source: :Louis_Philippe_I
    target: :Philippe_I_Duke_of_Orleans
    relation: :hasAncestor
  AssignClass (a5971b50-6b4a-4e5d-a3f1-aa806dc133aa)
 Call ID: a5971b50-6b4a-4e5d-a3f1-aa806dc133aa
  Args:
    source: :Henri_VI_Count_of_Paris
    type: :Man
  AssignClass (dc7956dd-1364-47fb-8984-b801fa6c6179)
 Call ID: dc7956dd-1364-47fb-8984-b801fa6c6179
  Args:
    type: :Person
    source: :Henri_VI_Count_of_Paris
  AddTriple (ec06b477-42f4-4622-8c51-3b194e361928)
 Call ID: ec06b477-42f4-4622-8c51-3b194e361928
  Args:
    source: :Jean_dOrleans
    relation: :hasAncestor
    target: :Henri_VI_Count_of_Paris
  AssignClass (a62c486c-d581-46d1-b24e-9536a6c7e4af)
 Call ID: a62c486c-d581-46d1-b24e-9536a6c7e4af
  Args:
    source: :Henri_dOrleans_Ancestor
    type: :Man
  AssignClass (7895b7b9-9543-4bd3-b991-781fa4432161)
 Call ID: 7895b7b9-9543-4bd3-b991-781fa4432161
  Args:
    type: :Person
    source: :Henri_dOrleans_Ancestor
  AddTriple (2222ffe3-d39e-4a84-bf14-c944a00634a9)
 Call ID: 2222ffe3-d39e-4a84-bf14-c944a00634a9
  Args:
    source: :Jean_dOrleans
    relation: :hasAncestor
    target: :Henri_dOrleans_Ancestor
  AssignClass (b48cd33a-a31d-4d8a-a17b-d72d1fb807c5)
 Call ID: b48cd33a-a31d-4d8a-a17b-d72d1fb807c5
  Args:
    source: :Charles_X
    type: :Man
  AssignClass (500f7ab9-8ee7-4e52-94d1-9e37700cc157)
 Call ID: 500f7ab9-8ee7-4e52-94d1-9e37700cc157
  Args:
    type: :Person
    source: :Charles_X
  AddTriple (3952c77b-ec20-4c27-9744-6418800a6a75)
 Call ID: 3952c77b-ec20-4c27-9744-6418800a6a75
  Args:
    source: :Jean_dOrleans
    target: :Charles_X
    relation: :hasAncestor
  Finish (e0bd45d7-1678-404e-a1b2-a06c97070504)
 Call ID: e0bd45d7-1678-404e-a1b2-a06c97070504
  Args: