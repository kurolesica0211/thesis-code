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
  AssignClass (66850bf5-a3e2-4502-a5a6-39e2e06d0fc6)
 Call ID: 66850bf5-a3e2-4502-a5a6-39e2e06d0fc6
  Args:
    source: Infante_Jaime
    type: :Man
  AssignClass (884a3be1-e41f-4433-b470-aa611b882ff6)
 Call ID: 884a3be1-e41f-4433-b470-aa611b882ff6
  Args:
    type: :Person
    source: Infante_Jaime
  AddLiteral (8beb26cd-61a7-412f-b6c2-69e90b4b3537)
 Call ID: 8beb26cd-61a7-412f-b6c2-69e90b4b3537
  Args:
    relation: :hasBirthYear
    source: Infante_Jaime
    literal_type: xsd:integer
    literal_value: 1908
  AddLiteral (1268365c-ec4a-401a-8567-5ca3847739db)
 Call ID: 1268365c-ec4a-401a-8567-5ca3847739db
  Args:
    literal_value: 1975
    source: Infante_Jaime
    literal_type: xsd:integer
    relation: :hasDeathYear
  AssignClass (d2a86cd7-6a23-4ca9-b9c2-af9611920811)
 Call ID: d2a86cd7-6a23-4ca9-b9c2-af9611920811
  Args:
    type: :Man
    source: Alfonso_XIII
  AssignClass (7d825553-b247-44ac-8033-536bc41cebea)
 Call ID: 7d825553-b247-44ac-8033-536bc41cebea
  Args:
    source: Alfonso_XIII
    type: :Person
  AssignClass (b316476e-dfc8-4e44-8097-504114b97fde)
 Call ID: b316476e-dfc8-4e44-8097-504114b97fde
  Args:
    type: :Woman
    source: Victoria_Eugenie
  AssignClass (66249c72-9bc4-4721-afb2-346e6b8c330d)
 Call ID: 66249c72-9bc4-4721-afb2-346e6b8c330d
  Args:
    type: :Person
    source: Victoria_Eugenie
  AddTriple (93aa04f7-fbaa-4b4a-9019-3eebfdd1400a)
 Call ID: 93aa04f7-fbaa-4b4a-9019-3eebfdd1400a
  Args:
    relation: :hasFather
    target: Alfonso_XIII
    source: Infante_Jaime
  AddTriple (8db064be-f1df-485e-ad39-aa0431c66c8e)
 Call ID: 8db064be-f1df-485e-ad39-aa0431c66c8e
  Args:
    source: Infante_Jaime
    relation: :hasMother
    target: Victoria_Eugenie
  AssignClass (986d28a9-047a-496e-a20e-3e7172218f84)
 Call ID: 986d28a9-047a-496e-a20e-3e7172218f84
  Args:
    type: :Man
    source: Alfonso_Prince_of_Asturias
  AssignClass (58993063-30ba-4417-b845-0169ed345163)
 Call ID: 58993063-30ba-4417-b845-0169ed345163
  Args:
    type: :Person
    source: Alfonso_Prince_of_Asturias
  AssignClass (0ec241dc-4ca4-447f-b25a-3753c9e7ca61)
 Call ID: 0ec241dc-4ca4-447f-b25a-3753c9e7ca61
  Args:
    source: Infante_Juan
    type: :Man
  AssignClass (628de794-800e-42ec-9ebd-eac1dcca2b79)
 Call ID: 628de794-800e-42ec-9ebd-eac1dcca2b79
  Args:
    source: Infante_Juan
    type: :Person
  AssignClass (8dc610de-bb7f-4da3-85a4-117d864481c8)
 Call ID: 8dc610de-bb7f-4da3-85a4-117d864481c8
  Args:
    source: Infante_Gonzalo
    type: :Man
  AssignClass (806df8ae-88c5-4acc-b31a-8d945df3e50a)
 Call ID: 806df8ae-88c5-4acc-b31a-8d945df3e50a
  Args:
    source: Infante_Gonzalo
    type: :Person
  AssignClass (60594a7b-423d-4211-be16-7ea0f349dcbe)
 Call ID: 60594a7b-423d-4211-be16-7ea0f349dcbe
  Args:
    type: :Woman
    source: Infanta_Beatriz
  AssignClass (efbc3bd7-b945-4727-8c61-9c51a8e17553)
 Call ID: efbc3bd7-b945-4727-8c61-9c51a8e17553
  Args:
    type: :Person
    source: Infanta_Beatriz
  AssignClass (5cff52e8-9d26-4f45-a4d4-736178244edf)
 Call ID: 5cff52e8-9d26-4f45-a4d4-736178244edf
  Args:
    type: :Woman
    source: Infanta_Maria_Cristina
  AssignClass (f3f98a84-2936-4bff-b55b-f509ccc37578)
 Call ID: f3f98a84-2936-4bff-b55b-f509ccc37578
  Args:
    source: Infanta_Maria_Cristina
    type: :Person
  AddTriple (ca0bc30f-d312-4024-ab20-59570de859b4)
 Call ID: ca0bc30f-d312-4024-ab20-59570de859b4
  Args:
    source: Infante_Jaime
    target: Alfonso_Prince_of_Asturias
    relation: :isSiblingOf
  AddTriple (3470d2ca-8f0d-40bd-9a86-d2316e77d269)
 Call ID: 3470d2ca-8f0d-40bd-9a86-d2316e77d269
  Args:
    relation: :isSiblingOf
    target: Infante_Juan
    source: Infante_Jaime
  AddTriple (6980650d-1466-4fce-a6b6-ffa61e96bc1d)
 Call ID: 6980650d-1466-4fce-a6b6-ffa61e96bc1d
  Args:
    source: Infante_Jaime
    relation: :isSiblingOf
    target: Infante_Gonzalo
  AddTriple (eb8adbea-54a4-4e6c-baca-3241a04f4183)
 Call ID: eb8adbea-54a4-4e6c-baca-3241a04f4183
  Args:
    source: Infante_Jaime
    target: Infanta_Beatriz
    relation: :isSiblingOf
  AddTriple (de7d23ea-754f-4c9d-ae4d-e13e263fa6ba)
 Call ID: de7d23ea-754f-4c9d-ae4d-e13e263fa6ba
  Args:
    relation: :isSiblingOf
    target: Infanta_Maria_Cristina
    source: Infante_Jaime
  AssignClass (9188d855-ee85-460f-88d5-31484cd07bf0)
 Call ID: 9188d855-ee85-460f-88d5-31484cd07bf0
  Args:
    source: Donna_Emanuela
    type: :Woman
  AssignClass (dbabca45-d41e-44ca-bdb9-abcc8a006f1b)
 Call ID: dbabca45-d41e-44ca-bdb9-abcc8a006f1b
  Args:
    type: :Person
    source: Donna_Emanuela
  AssignClass (05b5b7ec-3c7f-4af1-b1b1-53c1396b9c15)
 Call ID: 05b5b7ec-3c7f-4af1-b1b1-53c1396b9c15
  Args:
    type: :Man
    source: Alfonso_de_Borbon_son
  AssignClass (f659d9df-bcb7-4d1b-a894-8142b72677af)
 Call ID: f659d9df-bcb7-4d1b-a894-8142b72677af
  Args:
    source: Alfonso_de_Borbon_son
    type: :Person
  AssignClass (cc19531c-6752-46e0-a7f9-2579e5487af4)
 Call ID: cc19531c-6752-46e0-a7f9-2579e5487af4
  Args:
    source: Gonzalo_de_Borbon_son
    type: :Man
  AssignClass (3fc57abd-5332-418a-bc60-e0eb4475a733)
 Call ID: 3fc57abd-5332-418a-bc60-e0eb4475a733
  Args:
    source: Gonzalo_de_Borbon_son
    type: :Person
  AddTriple (9f6a6b72-76ed-4778-bbc6-3ae39d07c8ec)
 Call ID: 9f6a6b72-76ed-4778-bbc6-3ae39d07c8ec
  Args:
    target: Alfonso_de_Borbon_son
    relation: :hasChild
    source: Infante_Jaime
  AddTriple (59585f57-1102-4660-955b-540cd2dd022b)
 Call ID: 59585f57-1102-4660-955b-540cd2dd022b
  Args:
    relation: :hasChild
    target: Gonzalo_de_Borbon_son
    source: Infante_Jaime
  AddTriple (a0f5fa47-509d-4702-af12-b64477e61c65)
 Call ID: a0f5fa47-509d-4702-af12-b64477e61c65
  Args:
    relation: :hasChild
    target: Alfonso_de_Borbon_son
    source: Donna_Emanuela
  AddTriple (fecae519-bbac-4a22-ae41-0b6335fe7082)
 Call ID: fecae519-bbac-4a22-ae41-0b6335fe7082
  Args:
    source: Donna_Emanuela
    relation: :hasChild
    target: Gonzalo_de_Borbon_son
  AssignClass (a30a3c0a-3084-4965-ae05-31770d267bcc)
 Call ID: a30a3c0a-3084-4965-ae05-31770d267bcc
  Args:
    source: Charlotte_Luise_Auguste_Tiedemann
    type: :Woman
  AssignClass (59c6493c-3a51-4e2b-9c2a-96b855b10a4f)
 Call ID: 59c6493c-3a51-4e2b-9c2a-96b855b10a4f
  Args:
    type: :Person
    source: Charlotte_Luise_Auguste_Tiedemann
  AddLiteral (bb13e236-00b7-400a-ae11-f98e87548f33)
 Call ID: bb13e236-00b7-400a-ae11-f98e87548f33
  Args:
    literal_value: 1949
    source: Infante_Jaime
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AssignClass (00397386-9655-4ae6-a2fa-ed2ad46e454a)
 Call ID: 00397386-9655-4ae6-a2fa-ed2ad46e454a
  Args:
    type: :Man
    source: Otto_Eugen_Tiedemann
  AssignClass (a6a4f03c-481e-4a9b-9b21-f2c03c1f3c13)
 Call ID: a6a4f03c-481e-4a9b-9b21-f2c03c1f3c13
  Args:
    source: Otto_Eugen_Tiedemann
    type: :Person
  AssignClass (5081d533-a56b-436d-a023-94f196a948ea)
 Call ID: 5081d533-a56b-436d-a023-94f196a948ea
  Args:
    type: :Woman
    source: Luise_Amalia_Klein
  AssignClass (dd3b84f4-30e6-4613-8933-5ea58d129bb3)
 Call ID: dd3b84f4-30e6-4613-8933-5ea58d129bb3
  Args:
    source: Luise_Amalia_Klein
    type: :Person
  AddTriple (d397107e-5a2d-40f9-9ae0-d777fb4e39fe)
 Call ID: d397107e-5a2d-40f9-9ae0-d777fb4e39fe
  Args:
    source: Charlotte_Luise_Auguste_Tiedemann
    relation: :hasFather
    target: Otto_Eugen_Tiedemann
  AddTriple (fe3a9068-026e-40f1-b13d-adfc8c41cf9b)
 Call ID: fe3a9068-026e-40f1-b13d-adfc8c41cf9b
  Args:
    relation: :hasMother
    target: Luise_Amalia_Klein
    source: Charlotte_Luise_Auguste_Tiedemann
  AssignClass (08260ec6-66e7-42a8-b132-cb6a431c56e5)
 Call ID: 08260ec6-66e7-42a8-b132-cb6a431c56e5
  Args:
    type: :Man
    source: Juan_Carlos_I
  AssignClass (6f763dc4-a16c-46bb-85ee-0645e7dad911)
 Call ID: 6f763dc4-a16c-46bb-85ee-0645e7dad911
  Args:
    type: :Person
    source: Juan_Carlos_I
  AddTriple (93d3e99d-6840-4dc8-9ea9-c5d44e46456d)
 Call ID: 93d3e99d-6840-4dc8-9ea9-c5d44e46456d
  Args:
    source: Juan_Carlos_I
    relation: :isSiblingOf
    target: Infante_Juan
  Finish (32eeb892-f9ec-49e7-a7da-def0ed877aba)
 Call ID: 32eeb892-f9ec-49e7-a7da-def0ed877aba
  Args: