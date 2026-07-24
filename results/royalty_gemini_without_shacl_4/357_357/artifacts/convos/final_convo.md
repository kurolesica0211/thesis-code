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
  AssignClass (20f9d18c-8219-406f-874d-e4799a3d0018)
 Call ID: 20f9d18c-8219-406f-874d-e4799a3d0018
  Args:
    type: :Man
    source: Jean_d_Orleans
  AssignClass (1f3fb08a-5e9a-45bb-90c0-d988d24a337b)
 Call ID: 1f3fb08a-5e9a-45bb-90c0-d988d24a337b
  Args:
    type: :Person
    source: Jean_d_Orleans
  AddLiteral (2365bfe9-9b9b-41bf-8bcf-c383aa6444ca)
 Call ID: 2365bfe9-9b9b-41bf-8bcf-c383aa6444ca
  Args:
    literal_type: xsd:nonNegativeInteger
    relation: :hasBirthYear
    literal_value: 1965
    source: Jean_d_Orleans
  AssignClass (d4083111-782e-4a8f-a92c-c6d073032639)
 Call ID: d4083111-782e-4a8f-a92c-c6d073032639
  Args:
    source: Henri_Count_of_Paris
    type: :Man
  AssignClass (91cfeae7-f33b-4f15-bc6b-d5cd5b1c6d20)
 Call ID: 91cfeae7-f33b-4f15-bc6b-d5cd5b1c6d20
  Args:
    source: Henri_Count_of_Paris
    type: :Person
  AddLiteral (d7c102df-8113-45bf-ae98-c05750f92cf8)
 Call ID: d7c102df-8113-45bf-ae98-c05750f92cf8
  Args:
    source: Henri_Count_of_Paris
    literal_value: 1933
    literal_type: xsd:nonNegativeInteger
    relation: :hasBirthYear
  AddLiteral (eea52a45-e2e0-426a-8a0d-f0ddb27d9939)
 Call ID: eea52a45-e2e0-426a-8a0d-f0ddb27d9939
  Args:
    source: Henri_Count_of_Paris
    literal_value: 2019
    relation: :hasDeathYear
    literal_type: xsd:nonNegativeInteger
  AssignClass (b1c409a8-8bcd-43d9-a63f-36112c813bde)
 Call ID: b1c409a8-8bcd-43d9-a63f-36112c813bde
  Args:
    type: :Woman
    source: Marie_Therese_of_Wurttemberg
  AssignClass (fc34f8e1-c467-4dac-a75a-76643a3cf239)
 Call ID: fc34f8e1-c467-4dac-a75a-76643a3cf239
  Args:
    type: :Person
    source: Marie_Therese_of_Wurttemberg
  AddLiteral (04eab2e0-0481-4d9a-9d9f-4faef5e0c611)
 Call ID: 04eab2e0-0481-4d9a-9d9f-4faef5e0c611
  Args:
    relation: :hasBirthYear
    literal_type: xsd:nonNegativeInteger
    literal_value: 1934
    source: Marie_Therese_of_Wurttemberg
  AddTriple (199f2a02-6d9e-41c0-9fc8-8217423cd11a)
 Call ID: 199f2a02-6d9e-41c0-9fc8-8217423cd11a
  Args:
    relation: :hasFather
    target: Henri_Count_of_Paris
    source: Jean_d_Orleans
  AddTriple (8e364962-6310-4b09-8703-d6b6cfc44b09)
 Call ID: 8e364962-6310-4b09-8703-d6b6cfc44b09
  Args:
    source: Jean_d_Orleans
    target: Marie_Therese_of_Wurttemberg
    relation: :hasMother
  AssignClass (3a38fda2-ea50-4d47-b02e-3b4551d895a7)
 Call ID: 3a38fda2-ea50-4d47-b02e-3b4551d895a7
  Args:
    type: :Man
    source: Carl_of_Wurttemberg
  AssignClass (185d57bb-d1cf-4da8-90b5-2e06ba38d2f5)
 Call ID: 185d57bb-d1cf-4da8-90b5-2e06ba38d2f5
  Args:
    type: :Person
    source: Carl_of_Wurttemberg
  AssignClass (f2ab675f-a51b-4f70-a37a-05d5039c0af9)
 Call ID: f2ab675f-a51b-4f70-a37a-05d5039c0af9
  Args:
    source: Princess_Chantal_of_Orleans
    type: :Woman
  AssignClass (d02e3995-520a-48af-8cf8-e982051267fd)
 Call ID: d02e3995-520a-48af-8cf8-e982051267fd
  Args:
    source: Princess_Chantal_of_Orleans
    type: :Person
  AssignClass (dbcd5aef-b7ef-4661-af5c-2260d91cc91e)
 Call ID: dbcd5aef-b7ef-4661-af5c-2260d91cc91e
  Args:
    type: :Woman
    source: Philomena_de_Tornos_y_Steinhart
  AssignClass (b9354091-f791-4bc1-a05f-41e5f51bd0ea)
 Call ID: b9354091-f791-4bc1-a05f-41e5f51bd0ea
  Args:
    type: :Person
    source: Philomena_de_Tornos_y_Steinhart
  AddLiteral (f5aea227-d999-48da-8a87-95c2441d3a6e)
 Call ID: f5aea227-d999-48da-8a87-95c2441d3a6e
  Args:
    source: Philomena_de_Tornos_y_Steinhart
    literal_value: 1977
    relation: :hasBirthYear
    literal_type: xsd:nonNegativeInteger
  AddTriple (725fc967-b652-43e3-9806-8f13037baf5e)
 Call ID: 725fc967-b652-43e3-9806-8f13037baf5e
  Args:
    source: Jean_d_Orleans
    relation: :hasRelation
    target: Philomena_de_Tornos_y_Steinhart
  AssignClass (c645a547-ca9e-491e-9fe0-3dbab85d8683)
 Call ID: c645a547-ca9e-491e-9fe0-3dbab85d8683
  Args:
    type: :Man
    source: Henri_VI_Count_of_Paris
  AssignClass (fa67ffe9-d6b3-4914-b17a-a6f94477d172)
 Call ID: fa67ffe9-d6b3-4914-b17a-a6f94477d172
  Args:
    source: Henri_VI_Count_of_Paris
    type: :Person
  AssignClass (f5b381a0-3304-4ca2-8604-0efe70656ace)
 Call ID: f5b381a0-3304-4ca2-8604-0efe70656ace
  Args:
    source: Louis_Philippe_I
    type: :Man
  AssignClass (7c9dda06-2bb8-4dfe-bc01-9da6cfb1d6d0)
 Call ID: 7c9dda06-2bb8-4dfe-bc01-9da6cfb1d6d0
  Args:
    type: :Person
    source: Louis_Philippe_I
  AssignClass (04e82b55-da25-4d9e-86c0-c0b82b225208)
 Call ID: 04e82b55-da25-4d9e-86c0-c0b82b225208
  Args:
    source: Philippe_I_Duke_of_Orleans
    type: :Man
  AssignClass (651292c6-e3ac-4d41-9dcf-47655cd791a9)
 Call ID: 651292c6-e3ac-4d41-9dcf-47655cd791a9
  Args:
    source: Philippe_I_Duke_of_Orleans
    type: :Person
  AssignClass (69b143e1-bcb3-40ab-bd59-dfbe4d420b4e)
 Call ID: 69b143e1-bcb3-40ab-bd59-dfbe4d420b4e
  Args:
    source: Louis_XIV
    type: :Man
  AssignClass (565831e6-a4fd-419e-bd98-d745d0ae5fd8)
 Call ID: 565831e6-a4fd-419e-bd98-d745d0ae5fd8
  Args:
    source: Louis_XIV
    type: :Person
  AssignClass (0e0cd2ee-9e57-46b4-acb2-eb234518117d)
 Call ID: 0e0cd2ee-9e57-46b4-acb2-eb234518117d
  Args:
    source: Charles_X
    type: :Man
  AssignClass (f472ad5f-2875-43f6-abc8-5d139ecbd98c)
 Call ID: f472ad5f-2875-43f6-abc8-5d139ecbd98c
  Args:
    type: :Person
    source: Charles_X
  AssignClass (d2a38f2e-bde3-4f11-80be-882ff59f6339)
 Call ID: d2a38f2e-bde3-4f11-80be-882ff59f6339
  Args:
    type: :Man
    source: Louis_XVI
  AssignClass (84d296a1-e835-46e4-a53f-7afc072205e9)
 Call ID: 84d296a1-e835-46e4-a53f-7afc072205e9
  Args:
    source: Louis_XVI
    type: :Person
  AddTriple (84c9dfba-dcbf-4ecd-a604-19a2be8a57f5)
 Call ID: 84c9dfba-dcbf-4ecd-a604-19a2be8a57f5
  Args:
    source: Philippe_I_Duke_of_Orleans
    target: Louis_XIV
    relation: :isBrotherOf
  AddTriple (37e6248e-73f4-4490-99af-8a5457438d9e)
 Call ID: 37e6248e-73f4-4490-99af-8a5457438d9e
  Args:
    source: Charles_X
    target: Louis_XVI
    relation: :isBrotherOf
  Finish (067976e6-fd6e-4a56-ae13-ba2f7d3f35c7)
 Call ID: 067976e6-fd6e-4a56-ae13-ba2f7d3f35c7
  Args: