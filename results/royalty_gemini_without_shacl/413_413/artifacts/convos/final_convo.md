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
Infante Jaime of Spain, Duke of Segovia  (Spanish: Don Jaime Leopoldo Isabelino Enrique Alejandro Alberto Alfonso Víctor Acacio Pedro Pablo María de Borbón y Battenberg; French: Jacques Léopold Isabellin Henri Alexandre Albért Alphonse Victor Acace Pierre Paul Marie de Bourbon; 23 June 1908 – 20 March 1975), was the second son of King Alfonso XIII of Spain and his wife, Princess Victoria Eugenie of Battenberg.
Early life

Infante Jaime was born 23 June 1908 at the Royal Palace of La Granja de San Ildefonso, the second son of King Alfonso XIII and his Hessian wife, Victoria Eugenie of Battenberg, the youngest granddaughter of Queen Victoria.
He had three brothers, Alfonso, Prince of Asturias (1907–1938), Infante Juan, Count of Barcelona (1913–1993), and  Infante Gonzalo (1914–1934); and two younger sisters, Infanta Beatriz (1909–2002) and Infanta María Cristina (1911–1996).
His elder brother, the Prince of Asturias, and his youngest brother, Gonzalo, both had the bleeding disorder hemophilia, the genetic condition that plagued many descendants of Queen Victoria.
Infante Jaime was born with an infection of the inner ear that progressively worsened, causing him to gradually lose his hearing.
On 11 June 1933, his elder brother and heir to the defunct throne, Alfonso, renounced his title of Prince of Asturias in order to marry a Cuban commoner.
Infante Jaime then held the title of Prince of Asturias, as successor to the throne of Spain, for only ten days before under pressure from his father, he was forced also to renounce his rights and the rights of his heirs, in favor of his younger, healthier brother Infante Juan.
He was then granted the title "Duke of Segovia" by King Alfonso XIII.
Don Jaime and Donna Emanuela had two sons, named after Jaime's brothers, Alfonso and Gonzalo:


Don Jaime and Emmanuelle de Dampierre divorced on 6 May 1947 in Bucharest (recognized by the Italian courts on 3 June 1949 in Turin but never recognized in Spain) and, on 3 August 1949 in Innsbruck, Don Jaime remarried civilly to divorced singer Charlotte Luise Auguste Tiedemann (2 January 1919 in Königsberg – 3 July 1979 in Berlin), daughter of Otto Eugen Tiedemann and wife Luise Amalia Klein.
In the eyes of the Roman Catholic Church and of the French legitimists, Emmanuelle de Dampierre remained always his wife.
On 3 May 1964, he took the title "Duke of Madrid" as head of a Carlist branch of the Spanish succession (recognized by the legitimist group of Carlists who did not support the Bourbon-Parma claim after Alfonso Carlos, Duke of San Jaime died in 1936).
On 19 July 1969, Don Jaime definitively renounced the Spanish succession in favour of his nephew, the future King Juan Carlos I, at the request of his elder son, Alfonso de Borbón.



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
  AssignClass (26deb154-cc22-44a0-b781-673b96dca00e)
 Call ID: 26deb154-cc22-44a0-b781-673b96dca00e
  Args:
    type: :Man
    source: Jaime_of_Spain
  AssignClass (aedd8ed6-0739-4d66-95f8-0e1ce08dd769)
 Call ID: aedd8ed6-0739-4d66-95f8-0e1ce08dd769
  Args:
    source: Jaime_of_Spain
    type: :Person
  AddLiteral (103d2db4-bf60-4b9d-b440-819281666ac5)
 Call ID: 103d2db4-bf60-4b9d-b440-819281666ac5
  Args:
    literal_value: 1908
    relation: :hasBirthYear
    source: Jaime_of_Spain
    literal_type: xsd:integer
  AddLiteral (fdc643f2-9a96-4909-857c-769618791fca)
 Call ID: fdc643f2-9a96-4909-857c-769618791fca
  Args:
    source: Jaime_of_Spain
    literal_type: xsd:integer
    literal_value: 1975
    relation: :hasDeathYear
  AssignClass (e2f58713-2050-496f-b407-e4b5847822b3)
 Call ID: e2f58713-2050-496f-b407-e4b5847822b3
  Args:
    source: Alfonso_XIII
    type: :Man
  AssignClass (00442c33-121c-49ce-900b-ebedf090f8a7)
 Call ID: 00442c33-121c-49ce-900b-ebedf090f8a7
  Args:
    type: :Person
    source: Alfonso_XIII
  AssignClass (ae3cf508-3ae6-4f59-bf64-8f6ceb5396e3)
 Call ID: ae3cf508-3ae6-4f59-bf64-8f6ceb5396e3
  Args:
    source: Victoria_Eugenie_of_Battenberg
    type: :Woman
  AssignClass (ca0775e0-8ce2-4c65-a17f-3a9b2a9b7688)
 Call ID: ca0775e0-8ce2-4c65-a17f-3a9b2a9b7688
  Args:
    source: Victoria_Eugenie_of_Battenberg
    type: :Person
  AddTriple (1105b41f-a14f-4216-9719-ac0b8dfcdc8e)
 Call ID: 1105b41f-a14f-4216-9719-ac0b8dfcdc8e
  Args:
    target: Alfonso_XIII
    source: Jaime_of_Spain
    relation: :hasFather
  AddTriple (b0d890e7-0fea-4bce-9047-9a3110e7ed75)
 Call ID: b0d890e7-0fea-4bce-9047-9a3110e7ed75
  Args:
    relation: :hasMother
    target: Victoria_Eugenie_of_Battenberg
    source: Jaime_of_Spain
  AssignClass (bedbf38a-730e-47d4-b54b-4fdf68ce4079)
 Call ID: bedbf38a-730e-47d4-b54b-4fdf68ce4079
  Args:
    source: Alfonso_Prince_of_Asturias
    type: :Man
  AssignClass (1bad0065-a992-4f96-82b5-d27f4cafe8d3)
 Call ID: 1bad0065-a992-4f96-82b5-d27f4cafe8d3
  Args:
    type: :Person
    source: Alfonso_Prince_of_Asturias
  AssignClass (2c1567d6-20b0-40c4-aedc-718b7726b85e)
 Call ID: 2c1567d6-20b0-40c4-aedc-718b7726b85e
  Args:
    source: Juan_Count_of_Barcelona
    type: :Man
  AssignClass (732601a9-1d13-48e7-9af9-f0cb4331232a)
 Call ID: 732601a9-1d13-48e7-9af9-f0cb4331232a
  Args:
    type: :Person
    source: Juan_Count_of_Barcelona
  AssignClass (f5a45667-2762-4b2e-a1ff-2ae90d7d44d0)
 Call ID: f5a45667-2762-4b2e-a1ff-2ae90d7d44d0
  Args:
    type: :Man
    source: Gonzalo_of_Spain
  AssignClass (c7256713-a6dd-4a74-831c-62631a881c58)
 Call ID: c7256713-a6dd-4a74-831c-62631a881c58
  Args:
    source: Gonzalo_of_Spain
    type: :Person
  AssignClass (b2a34404-9ea2-4983-b4c9-915426bfcaaf)
 Call ID: b2a34404-9ea2-4983-b4c9-915426bfcaaf
  Args:
    source: Beatriz_of_Spain
    type: :Woman
  AssignClass (328fc639-a007-4775-a9bb-1f8214ade3e6)
 Call ID: 328fc639-a007-4775-a9bb-1f8214ade3e6
  Args:
    type: :Person
    source: Beatriz_of_Spain
  AssignClass (6c0d45de-6720-42f1-a945-79913f66a5d6)
 Call ID: 6c0d45de-6720-42f1-a945-79913f66a5d6
  Args:
    source: Maria_Cristina_of_Spain
    type: :Woman
  AssignClass (12a4339b-3c02-4bdd-b754-dfc4dfbde759)
 Call ID: 12a4339b-3c02-4bdd-b754-dfc4dfbde759
  Args:
    type: :Person
    source: Maria_Cristina_of_Spain
  AddTriple (70c21c78-341f-4b6f-b737-9c2563275c4e)
 Call ID: 70c21c78-341f-4b6f-b737-9c2563275c4e
  Args:
    target: Jaime_of_Spain
    source: Alfonso_Prince_of_Asturias
    relation: :isBrotherOf
  AddTriple (ee68cf11-a4ef-423c-b36c-d78e75d2b46c)
 Call ID: ee68cf11-a4ef-423c-b36c-d78e75d2b46c
  Args:
    relation: :isBrotherOf
    target: Jaime_of_Spain
    source: Juan_Count_of_Barcelona
  AddTriple (38e753bb-683a-4e41-90d2-5a34aa6665f3)
 Call ID: 38e753bb-683a-4e41-90d2-5a34aa6665f3
  Args:
    source: Gonzalo_of_Spain
    target: Jaime_of_Spain
    relation: :isBrotherOf
  AddTriple (df5b4460-cb3a-4af7-a8cc-4398f05c685a)
 Call ID: df5b4460-cb3a-4af7-a8cc-4398f05c685a
  Args:
    relation: :isSisterOf
    target: Jaime_of_Spain
    source: Beatriz_of_Spain
  AddTriple (88a602a9-ca80-4eb1-b0fb-1d23f4f01c3b)
 Call ID: 88a602a9-ca80-4eb1-b0fb-1d23f4f01c3b
  Args:
    relation: :isSisterOf
    source: Maria_Cristina_of_Spain
    target: Jaime_of_Spain
  AssignClass (7dae05a5-7e99-4de2-b522-d36da9cdf7ea)
 Call ID: 7dae05a5-7e99-4de2-b522-d36da9cdf7ea
  Args:
    source: Emanuela_de_Dampierre
    type: :Woman
  AssignClass (22154592-d7bf-4bb3-b16c-97aca16037fd)
 Call ID: 22154592-d7bf-4bb3-b16c-97aca16037fd
  Args:
    type: :Person
    source: Emanuela_de_Dampierre
  AddTriple (31ab2f3a-89d1-4b10-ac6d-a0861c1589b4)
 Call ID: 31ab2f3a-89d1-4b10-ac6d-a0861c1589b4
  Args:
    target: Alfonso_de_Borbon
    source: Jaime_of_Spain
    relation: :hasChild
  AddTriple (6bca66e4-1ef9-4bad-a978-d5a01b890c93)
 Call ID: 6bca66e4-1ef9-4bad-a978-d5a01b890c93
  Args:
    relation: :hasChild
    target: Alfonso_de_Borbon
    source: Emanuela_de_Dampierre
  AddTriple (bd26656f-a529-4b49-acbb-6850b32a1fa5)
 Call ID: bd26656f-a529-4b49-acbb-6850b32a1fa5
  Args:
    source: Jaime_of_Spain
    target: Gonzalo_de_Borbon
    relation: :hasChild
  AddTriple (a2de3271-fec1-423a-878d-91f841b6c588)
 Call ID: a2de3271-fec1-423a-878d-91f841b6c588
  Args:
    relation: :hasChild
    target: Gonzalo_de_Borbon
    source: Emanuela_de_Dampierre
  AssignClass (d99843ab-64e8-4aab-82d9-b6cab5f34e9d)
 Call ID: d99843ab-64e8-4aab-82d9-b6cab5f34e9d
  Args:
    source: Alfonso_de_Borbon
    type: :Man
  AssignClass (e79ccef5-e202-4ae6-8f91-fe86ad42e3d7)
 Call ID: e79ccef5-e202-4ae6-8f91-fe86ad42e3d7
  Args:
    source: Alfonso_de_Borbon
    type: :Person
  AssignClass (25d99aa2-e3d0-48b6-a927-94d35d685e15)
 Call ID: 25d99aa2-e3d0-48b6-a927-94d35d685e15
  Args:
    type: :Man
    source: Gonzalo_de_Borbon
  AssignClass (ae3c9138-ce1d-4a1a-bd68-3f2f837843c7)
 Call ID: ae3c9138-ce1d-4a1a-bd68-3f2f837843c7
  Args:
    source: Gonzalo_de_Borbon
    type: :Person
  AssignClass (3735f468-eae3-4487-9c3f-7898cf1129c1)
 Call ID: 3735f468-eae3-4487-9c3f-7898cf1129c1
  Args:
    source: Charlotte_Luise_Auguste_Tiedemann
    type: :Woman
  AssignClass (5df0e81c-d319-4e07-8bd8-f16c3e121c7c)
 Call ID: 5df0e81c-d319-4e07-8bd8-f16c3e121c7c
  Args:
    source: Charlotte_Luise_Auguste_Tiedemann
    type: :Person
  AddLiteral (9b43f87d-b42f-44e7-9f8d-66f7799c1f8f)
 Call ID: 9b43f87d-b42f-44e7-9f8d-66f7799c1f8f
  Args:
    relation: :hasMarriageYear
    literal_value: 1949
    literal_type: xsd:integer
    source: Jaime_of_Spain
  AssignClass (4b05b65d-e54a-40ce-8e00-dfa65c9e9f45)
 Call ID: 4b05b65d-e54a-40ce-8e00-dfa65c9e9f45
  Args:
    type: :Man
    source: Otto_Eugen_Tiedemann
  AssignClass (84354034-ef83-40ee-8c39-273ccee665f2)
 Call ID: 84354034-ef83-40ee-8c39-273ccee665f2
  Args:
    source: Otto_Eugen_Tiedemann
    type: :Person
  AssignClass (90e6d2b9-a7b2-4c43-8a8a-badf1fd28d07)
 Call ID: 90e6d2b9-a7b2-4c43-8a8a-badf1fd28d07
  Args:
    source: Luise_Amalia_Klein
    type: :Woman
  AssignClass (19bc3710-d90c-4b36-adb8-ef76df2b6ddb)
 Call ID: 19bc3710-d90c-4b36-adb8-ef76df2b6ddb
  Args:
    type: :Person
    source: Luise_Amalia_Klein
  AddTriple (f64583f8-a260-45b4-a45c-f4ff5b14fa3a)
 Call ID: f64583f8-a260-45b4-a45c-f4ff5b14fa3a
  Args:
    target: Otto_Eugen_Tiedemann
    source: Charlotte_Luise_Auguste_Tiedemann
    relation: :hasFather
  AddTriple (fb061012-fce8-4767-a837-1cfc22442a1f)
 Call ID: fb061012-fce8-4767-a837-1cfc22442a1f
  Args:
    relation: :hasMother
    target: Luise_Amalia_Klein
    source: Charlotte_Luise_Auguste_Tiedemann
  Finish (4322eba8-0c08-47a0-9fe2-8641afa3a2e7)
 Call ID: 4322eba8-0c08-47a0-9fe2-8641afa3a2e7
  Args: