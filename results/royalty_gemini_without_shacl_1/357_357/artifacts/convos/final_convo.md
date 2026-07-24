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
  AssignClass (911defab-5a07-4639-9a99-221af84ed877)
 Call ID: 911defab-5a07-4639-9a99-221af84ed877
  Args:
    source: Jean_dOrleans
    type: :Man
  AssignClass (c3d44a1e-ed3f-483d-a96a-0aa647d3c3ff)
 Call ID: c3d44a1e-ed3f-483d-a96a-0aa647d3c3ff
  Args:
    type: :Person
    source: Jean_dOrleans
  AddLiteral (c699a82c-dcfd-44de-a284-960d079972b9)
 Call ID: c699a82c-dcfd-44de-a284-960d079972b9
  Args:
    source: Jean_dOrleans
    literal_type: xsd:integer
    literal_value: 1965
    relation: :hasBirthYear
  AssignClass (22883a7d-29b6-4e45-b4c3-57e2547993b8)
 Call ID: 22883a7d-29b6-4e45-b4c3-57e2547993b8
  Args:
    source: Henri_Count_of_Paris_1933
    type: :Man
  AssignClass (afbef940-205b-4fc4-87b4-3fef7ee9541c)
 Call ID: afbef940-205b-4fc4-87b4-3fef7ee9541c
  Args:
    source: Henri_Count_of_Paris_1933
    type: :Person
  AddLiteral (8a19e44b-9d24-4d96-bced-c9186f590eda)
 Call ID: 8a19e44b-9d24-4d96-bced-c9186f590eda
  Args:
    literal_value: 1933
    source: Henri_Count_of_Paris_1933
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (823f93e2-2dff-4958-813a-ada522137638)
 Call ID: 823f93e2-2dff-4958-813a-ada522137638
  Args:
    relation: :hasDeathYear
    literal_value: 2019
    literal_type: xsd:integer
    source: Henri_Count_of_Paris_1933
  AssignClass (f2ae67c7-4ca7-41d6-974f-e36ab8fac46c)
 Call ID: f2ae67c7-4ca7-41d6-974f-e36ab8fac46c
  Args:
    source: MarieTherese_of_Wurttemberg
    type: :Woman
  AssignClass (f14885ab-09d7-40f9-857f-4fc82d684c92)
 Call ID: f14885ab-09d7-40f9-857f-4fc82d684c92
  Args:
    type: :Person
    source: MarieTherese_of_Wurttemberg
  AddLiteral (7160c73f-83d0-4082-9e10-0594bd35f106)
 Call ID: 7160c73f-83d0-4082-9e10-0594bd35f106
  Args:
    relation: :hasBirthYear
    literal_value: 1934
    literal_type: xsd:integer
    source: MarieTherese_of_Wurttemberg
  AddTriple (da5116d2-4b8e-4a7b-a81e-9e7622779812)
 Call ID: da5116d2-4b8e-4a7b-a81e-9e7622779812
  Args:
    target: Henri_Count_of_Paris_1933
    relation: :hasFather
    source: Jean_dOrleans
  AddTriple (d9e0bf2a-c259-4246-9842-01e17e7a18b1)
 Call ID: d9e0bf2a-c259-4246-9842-01e17e7a18b1
  Args:
    target: MarieTherese_of_Wurttemberg
    relation: :hasMother
    source: Jean_dOrleans
  AssignClass (ccae1d62-8685-4b3c-89ab-827e341af183)
 Call ID: ccae1d62-8685-4b3c-89ab-827e341af183
  Args:
    type: :Woman
    source: Philomena_de_Tornos_y_Steinhart
  AssignClass (47c2f533-998a-4ec0-add1-a21e58b426cd)
 Call ID: 47c2f533-998a-4ec0-add1-a21e58b426cd
  Args:
    source: Philomena_de_Tornos_y_Steinhart
    type: :Person
  AddLiteral (fc2facf6-800d-4ac9-a313-cdf96ff1e0b2)
 Call ID: fc2facf6-800d-4ac9-a313-cdf96ff1e0b2
  Args:
    relation: :hasBirthYear
    literal_value: 1977
    source: Philomena_de_Tornos_y_Steinhart
    literal_type: xsd:integer
  AddTriple (33831162-6b1b-4769-840e-e726442bd385)
 Call ID: 33831162-6b1b-4769-840e-e726442bd385
  Args:
    target: Philomena_de_Tornos_y_Steinhart
    relation: :hasRelation
    source: Jean_dOrleans
  AssignClass (16b40852-ba92-4981-961e-d2c0da25349e)
 Call ID: 16b40852-ba92-4981-961e-d2c0da25349e
  Args:
    type: :Man
    source: Henri_VI_Count_of_Paris
  AssignClass (b33baf4c-1c5e-44f0-8744-d88779ae9065)
 Call ID: b33baf4c-1c5e-44f0-8744-d88779ae9065
  Args:
    source: Henri_VI_Count_of_Paris
    type: :Person
  AddTriple (63af43b6-8a09-4757-a960-58198215733f)
 Call ID: 63af43b6-8a09-4757-a960-58198215733f
  Args:
    source: Henri_Count_of_Paris_1933
    relation: :hasFather
    target: Henri_VI_Count_of_Paris
  AssignClass (1549cd03-18f3-488b-a7f0-25b32688c8c9)
 Call ID: 1549cd03-18f3-488b-a7f0-25b32688c8c9
  Args:
    source: Chantal_of_Orleans
    type: :Woman
  AssignClass (d01d98bb-cfef-41fa-bde4-321c13383298)
 Call ID: d01d98bb-cfef-41fa-bde4-321c13383298
  Args:
    source: Chantal_of_Orleans
    type: :Person
  AddTriple (fe0afeff-f2f2-442b-8b3a-aa27d196c880)
 Call ID: fe0afeff-f2f2-442b-8b3a-aa27d196c880
  Args:
    source: Henri_Count_of_Paris_1933
    relation: :hasSister
    target: Chantal_of_Orleans
  AssignClass (aff03724-7ade-41d4-90a4-b44cd8259cda)
 Call ID: aff03724-7ade-41d4-90a4-b44cd8259cda
  Args:
    type: :Man
    source: Carl_of_Wurttemberg
  AssignClass (86ca7227-865b-43d6-a932-1878358b8d6e)
 Call ID: 86ca7227-865b-43d6-a932-1878358b8d6e
  Args:
    source: Carl_of_Wurttemberg
    type: :Person
  AddTriple (65a73d4b-b8ba-402d-9a00-a0617aed4a91)
 Call ID: 65a73d4b-b8ba-402d-9a00-a0617aed4a91
  Args:
    source: Carl_of_Wurttemberg
    relation: :hasRelation
    target: MarieTherese_of_Wurttemberg
  Finish (07b3c019-e0ba-4f2e-9a16-7118e05a13db)
 Call ID: 07b3c019-e0ba-4f2e-9a16-7118e05a13db
  Args: