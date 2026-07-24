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
  AssignClass (33594b0b-8bac-4b34-a71d-59175a072a13)
 Call ID: 33594b0b-8bac-4b34-a71d-59175a072a13
  Args:
    type: :Man
    source: :Jean_dOrleans
  AssignClass (25d8efe7-b887-4ca8-9769-a6f3d010f699)
 Call ID: 25d8efe7-b887-4ca8-9769-a6f3d010f699
  Args:
    source: :Jean_dOrleans
    type: :Person
  AddLiteral (7ef48ef9-e565-4f06-9a9d-1cff012e2764)
 Call ID: 7ef48ef9-e565-4f06-9a9d-1cff012e2764
  Args:
    relation: :hasBirthYear
    literal_value: 1965
    source: :Jean_dOrleans
    literal_type: xsd:integer
  AssignClass (43fafb99-d142-4dd4-9dd2-c8b75af284ad)
 Call ID: 43fafb99-d142-4dd4-9dd2-c8b75af284ad
  Args:
    type: :Man
    source: :Henri_Count_of_Paris
  AssignClass (62b4631d-2701-497d-82b9-443e7fe2ee0b)
 Call ID: 62b4631d-2701-497d-82b9-443e7fe2ee0b
  Args:
    source: :Henri_Count_of_Paris
    type: :Person
  AddLiteral (f382dc26-7992-4214-aff1-80fa5e5aa931)
 Call ID: f382dc26-7992-4214-aff1-80fa5e5aa931
  Args:
    relation: :hasBirthYear
    literal_value: 1933
    source: :Henri_Count_of_Paris
    literal_type: xsd:integer
  AddLiteral (594b1095-0b31-4281-b4de-47ac9470c1f1)
 Call ID: 594b1095-0b31-4281-b4de-47ac9470c1f1
  Args:
    relation: :hasDeathYear
    literal_value: 2019
    source: :Henri_Count_of_Paris
    literal_type: xsd:integer
  AssignClass (aa8cf9a0-1a91-49af-a825-516088e0dc7a)
 Call ID: aa8cf9a0-1a91-49af-a825-516088e0dc7a
  Args:
    type: :Woman
    source: :Marie_Therese_of_Wurttemberg
  AssignClass (655f82d5-ca52-4f2e-ab81-c3b9ff85ef18)
 Call ID: 655f82d5-ca52-4f2e-ab81-c3b9ff85ef18
  Args:
    type: :Person
    source: :Marie_Therese_of_Wurttemberg
  AddLiteral (4d5f5929-9a68-42a1-8d25-ae119b7a09e7)
 Call ID: 4d5f5929-9a68-42a1-8d25-ae119b7a09e7
  Args:
    relation: :hasBirthYear
    literal_value: 1934
    source: :Marie_Therese_of_Wurttemberg
    literal_type: xsd:integer
  AddTriple (c9cadc6f-1eee-46a5-9ef2-5949da6d1749)
 Call ID: c9cadc6f-1eee-46a5-9ef2-5949da6d1749
  Args:
    relation: :hasFather
    source: :Jean_dOrleans
    target: :Henri_Count_of_Paris
  AddTriple (9a793191-a29b-4bb8-ae8a-935d4aa366c7)
 Call ID: 9a793191-a29b-4bb8-ae8a-935d4aa366c7
  Args:
    relation: :hasMother
    source: :Jean_dOrleans
    target: :Marie_Therese_of_Wurttemberg
  AssignClass (d58508ba-7840-4326-9262-ee9e13a9e93d)
 Call ID: d58508ba-7840-4326-9262-ee9e13a9e93d
  Args:
    source: :Philomena_de_Tornos_y_Steinhart
    type: :Woman
  AssignClass (64589929-d453-4781-bdd8-57ce6e14b69d)
 Call ID: 64589929-d453-4781-bdd8-57ce6e14b69d
  Args:
    source: :Philomena_de_Tornos_y_Steinhart
    type: :Person
  AddLiteral (17e4485b-a39d-4098-9fbf-39cf0bdd41ed)
 Call ID: 17e4485b-a39d-4098-9fbf-39cf0bdd41ed
  Args:
    literal_type: xsd:integer
    source: :Philomena_de_Tornos_y_Steinhart
    literal_value: 1977
    relation: :hasBirthYear
  AssignClass (86eedbc3-4112-44e4-897d-940d051c1ba6)
 Call ID: 86eedbc3-4112-44e4-897d-940d051c1ba6
  Args:
    type: :Man
    source: :Carl_of_Wurttemberg
  AssignClass (0d64106d-3541-42d5-984b-49ded5acec89)
 Call ID: 0d64106d-3541-42d5-984b-49ded5acec89
  Args:
    type: :Person
    source: :Carl_of_Wurttemberg
  AddTriple (0f06a7d5-3ae3-4f88-b5b5-4522fb153c6f)
 Call ID: 0f06a7d5-3ae3-4f88-b5b5-4522fb153c6f
  Args:
    relation: :isUncleOf
    source: :Carl_of_Wurttemberg
    target: :Jean_dOrleans
  AssignClass (8167ea99-160b-49fd-9c9a-1819dff19f7c)
 Call ID: 8167ea99-160b-49fd-9c9a-1819dff19f7c
  Args:
    type: :Woman
    source: :Chantal_of_Orleans
  AssignClass (1feda09f-2153-4c23-8fae-835b9ed22a4c)
 Call ID: 1feda09f-2153-4c23-8fae-835b9ed22a4c
  Args:
    source: :Chantal_of_Orleans
    type: :Person
  AddTriple (e30e116b-ad40-4128-8bf4-a5e9b3b76f68)
 Call ID: e30e116b-ad40-4128-8bf4-a5e9b3b76f68
  Args:
    relation: :isAuntOf
    source: :Chantal_of_Orleans
    target: :Jean_dOrleans
  AssignClass (a98195b0-c89f-42a3-9ae1-548929d8173b)
 Call ID: a98195b0-c89f-42a3-9ae1-548929d8173b
  Args:
    type: :Man
    source: :Louis_Philippe_I
  AssignClass (14d72ae7-b6da-4b47-a98f-4bca411283e9)
 Call ID: 14d72ae7-b6da-4b47-a98f-4bca411283e9
  Args:
    source: :Louis_Philippe_I
    type: :Person
  AddTriple (dd45293f-031c-43e3-8ba2-a6ba3c9d799f)
 Call ID: dd45293f-031c-43e3-8ba2-a6ba3c9d799f
  Args:
    relation: :hasAncestor
    source: :Jean_dOrleans
    target: :Louis_Philippe_I
  AssignClass (16224cda-e9de-4b89-b750-0d9a2142880a)
 Call ID: 16224cda-e9de-4b89-b750-0d9a2142880a
  Args:
    type: :Man
    source: :Philippe_I_Duke_of_Orleans
  AssignClass (925f2908-f012-43bf-857d-913af870c3d8)
 Call ID: 925f2908-f012-43bf-857d-913af870c3d8
  Args:
    type: :Person
    source: :Philippe_I_Duke_of_Orleans
  AddTriple (6b3a34d3-8e58-45fc-b014-858d6a08f805)
 Call ID: 6b3a34d3-8e58-45fc-b014-858d6a08f805
  Args:
    relation: :hasAncestor
    target: :Philippe_I_Duke_of_Orleans
    source: :Louis_Philippe_I
  AssignClass (1db752b9-ba02-457f-b251-2b435b4892b3)
 Call ID: 1db752b9-ba02-457f-b251-2b435b4892b3
  Args:
    source: :Charles_X
    type: :Man
  AssignClass (982932cd-2813-4fc4-acf7-53291a962b94)
 Call ID: 982932cd-2813-4fc4-acf7-53291a962b94
  Args:
    source: :Charles_X
    type: :Person
  AddTriple (56a84902-6d3d-42d0-a168-7b653b3b279e)
 Call ID: 56a84902-6d3d-42d0-a168-7b653b3b279e
  Args:
    relation: :hasAncestor
    target: :Charles_X
    source: :Jean_dOrleans
  AssignClass (c468c0fc-c21e-46c2-98c2-bd8f7fa8d88d)
 Call ID: c468c0fc-c21e-46c2-98c2-bd8f7fa8d88d
  Args:
    type: :Man
    source: :Henri_VI_Count_of_Paris
  AssignClass (61694dfb-829f-42d2-9972-07c5c792b85d)
 Call ID: 61694dfb-829f-42d2-9972-07c5c792b85d
  Args:
    source: :Henri_VI_Count_of_Paris
    type: :Person
  AddTriple (1a49f5b2-b189-4dc3-8d1c-6ebced27ea72)
 Call ID: 1a49f5b2-b189-4dc3-8d1c-6ebced27ea72
  Args:
    relation: :hasAncestor
    target: :Henri_VI_Count_of_Paris
    source: :Jean_dOrleans
  AssignClass (348f7809-b0ef-4410-b8c3-17d41dfe2592)
 Call ID: 348f7809-b0ef-4410-b8c3-17d41dfe2592
  Args:
    source: :Tatjana_of_Oldenburg
    type: :Woman
  AssignClass (8e059494-2e5c-4295-ba4a-df70a170f889)
 Call ID: 8e059494-2e5c-4295-ba4a-df70a170f889
  Args:
    source: :Tatjana_of_Oldenburg
    type: :Person
  AddLiteral (8fc18eb2-01b2-4b17-83ac-e34774610bf7)
 Call ID: 8fc18eb2-01b2-4b17-83ac-e34774610bf7
  Args:
    source: :Tatjana_of_Oldenburg
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1974
  Finish (29238f46-b631-4994-8a1b-f308397233cf)
 Call ID: 29238f46-b631-4994-8a1b-f308397233cf
  Args: