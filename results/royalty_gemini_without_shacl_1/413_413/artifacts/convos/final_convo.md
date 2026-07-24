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
  AssignClass (887973a7-9212-4b9d-a1dd-cd36f9ee1ad3)
 Call ID: 887973a7-9212-4b9d-a1dd-cd36f9ee1ad3
  Args:
    source: Infante_Jaime
    type: :Man
  AssignClass (389bae84-97ee-4c85-920d-ac54f8a74287)
 Call ID: 389bae84-97ee-4c85-920d-ac54f8a74287
  Args:
    type: :Man
    source: Alfonso_XIII
  AssignClass (706dd34b-3436-48c3-ad47-c8969b2fa735)
 Call ID: 706dd34b-3436-48c3-ad47-c8969b2fa735
  Args:
    type: :Woman
    source: Victoria_Eugenie_of_Battenberg
  AddLiteral (1d641c2c-b3f1-42f1-a93d-3a776dd8daf6)
 Call ID: 1d641c2c-b3f1-42f1-a93d-3a776dd8daf6
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1908
    source: Infante_Jaime
  AddLiteral (7ae31bea-62f0-4200-a33e-05e82c4a6de3)
 Call ID: 7ae31bea-62f0-4200-a33e-05e82c4a6de3
  Args:
    literal_type: xsd:integer
    literal_value: 1975
    source: Infante_Jaime
    relation: :hasDeathYear
  AddTriple (8e923936-b1f1-4802-8789-e2ed68808b8e)
 Call ID: 8e923936-b1f1-4802-8789-e2ed68808b8e
  Args:
    target: Alfonso_XIII
    relation: :hasFather
    source: Infante_Jaime
  AddTriple (dcda0214-5132-4426-8e3f-3b24f6aebb8e)
 Call ID: dcda0214-5132-4426-8e3f-3b24f6aebb8e
  Args:
    target: Victoria_Eugenie_of_Battenberg
    relation: :hasMother
    source: Infante_Jaime
  AssignClass (ba73ba15-e396-45e9-a0ae-bff96b10339f)
 Call ID: ba73ba15-e396-45e9-a0ae-bff96b10339f
  Args:
    source: Alfonso_Prince_of_Asturias
    type: :Man
  AssignClass (8408423c-086a-4225-940c-d1cf24dd0ff3)
 Call ID: 8408423c-086a-4225-940c-d1cf24dd0ff3
  Args:
    source: Infante_Juan
    type: :Man
  AssignClass (1a226366-1b40-464a-9d24-f0eafccaaf86)
 Call ID: 1a226366-1b40-464a-9d24-f0eafccaaf86
  Args:
    type: :Man
    source: Infante_Gonzalo
  AssignClass (f28d5793-296c-4221-a81b-9ba1795b198c)
 Call ID: f28d5793-296c-4221-a81b-9ba1795b198c
  Args:
    type: :Woman
    source: Infanta_Beatriz
  AssignClass (39d974bb-8161-45dd-b278-9d7a40d87c52)
 Call ID: 39d974bb-8161-45dd-b278-9d7a40d87c52
  Args:
    source: Infanta_Maria_Cristina
    type: :Woman
  AddTriple (8c08bfd6-eddf-4ca7-944e-a76d507d09d3)
 Call ID: 8c08bfd6-eddf-4ca7-944e-a76d507d09d3
  Args:
    target: Alfonso_Prince_of_Asturias
    source: Infante_Jaime
    relation: :isSiblingOf
  AddTriple (5527e7e3-e526-438b-8039-ce8efc7dc2f3)
 Call ID: 5527e7e3-e526-438b-8039-ce8efc7dc2f3
  Args:
    relation: :isSiblingOf
    source: Infante_Jaime
    target: Infante_Juan
  AddTriple (3b57c8f2-8a84-449f-9a20-49da98e89d7f)
 Call ID: 3b57c8f2-8a84-449f-9a20-49da98e89d7f
  Args:
    source: Infante_Jaime
    relation: :isSiblingOf
    target: Infante_Gonzalo
  AddTriple (4fe73999-ec11-4dd2-8596-cc1c1ec46193)
 Call ID: 4fe73999-ec11-4dd2-8596-cc1c1ec46193
  Args:
    target: Infanta_Beatriz
    relation: :isSiblingOf
    source: Infante_Jaime
  AddTriple (46b71506-e01f-44fe-a65d-56aabf0c2fcf)
 Call ID: 46b71506-e01f-44fe-a65d-56aabf0c2fcf
  Args:
    target: Infanta_Maria_Cristina
    source: Infante_Jaime
    relation: :isSiblingOf
  AssignClass (c12595aa-4831-4efc-8100-13a2197e1c03)
 Call ID: c12595aa-4831-4efc-8100-13a2197e1c03
  Args:
    type: :Woman
    source: Emmanuelle_de_Dampierre
  AssignClass (6c2edbd4-3580-4dee-99cb-031f82217d7d)
 Call ID: 6c2edbd4-3580-4dee-99cb-031f82217d7d
  Args:
    type: :Man
    source: Alfonso_de_Borbon_son
  AssignClass (84d03e74-0057-4613-bd25-9034a159129e)
 Call ID: 84d03e74-0057-4613-bd25-9034a159129e
  Args:
    type: :Man
    source: Gonzalo_de_Borbon_son
  AddTriple (29437367-323c-47b6-b296-33d4b64a9645)
 Call ID: 29437367-323c-47b6-b296-33d4b64a9645
  Args:
    target: Infante_Jaime
    relation: :hasFather
    source: Alfonso_de_Borbon_son
  AddTriple (4dc2e086-255d-4315-ab21-cfa70a1b096a)
 Call ID: 4dc2e086-255d-4315-ab21-cfa70a1b096a
  Args:
    relation: :hasMother
    source: Alfonso_de_Borbon_son
    target: Emmanuelle_de_Dampierre
  AddTriple (964e19ec-3ed2-4c0a-9308-cc18b4b5cc65)
 Call ID: 964e19ec-3ed2-4c0a-9308-cc18b4b5cc65
  Args:
    source: Gonzalo_de_Borbon_son
    relation: :hasFather
    target: Infante_Jaime
  AddTriple (f61fb291-dae3-4fb8-a887-8e4ab1b0534d)
 Call ID: f61fb291-dae3-4fb8-a887-8e4ab1b0534d
  Args:
    target: Emmanuelle_de_Dampierre
    source: Gonzalo_de_Borbon_son
    relation: :hasMother
  AssignClass (85736670-6ac7-4ce9-9455-4c00f390f93e)
 Call ID: 85736670-6ac7-4ce9-9455-4c00f390f93e
  Args:
    type: :Woman
    source: Charlotte_Luise_Auguste_Tiedemann
  AddLiteral (99a510f2-f25f-4081-8122-578254d138a3)
 Call ID: 99a510f2-f25f-4081-8122-578254d138a3
  Args:
    literal_type: xsd:integer
    source: Charlotte_Luise_Auguste_Tiedemann
    literal_value: 1919
    relation: :hasBirthYear
  AddLiteral (a605c0ce-0642-4808-92ad-c374d50bf2a2)
 Call ID: a605c0ce-0642-4808-92ad-c374d50bf2a2
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 1979
    source: Charlotte_Luise_Auguste_Tiedemann
  AssignClass (25d33d40-47b2-4795-a461-ea3f39773909)
 Call ID: 25d33d40-47b2-4795-a461-ea3f39773909
  Args:
    source: Otto_Eugen_Tiedemann
    type: :Man
  AssignClass (d6df9900-bff7-4daf-8b50-38cde1d1b252)
 Call ID: d6df9900-bff7-4daf-8b50-38cde1d1b252
  Args:
    source: Luise_Amalia_Klein
    type: :Woman
  AddTriple (9d228d9d-f734-439f-9e53-66ab602500e0)
 Call ID: 9d228d9d-f734-439f-9e53-66ab602500e0
  Args:
    relation: :hasFather
    source: Charlotte_Luise_Auguste_Tiedemann
    target: Otto_Eugen_Tiedemann
  AddTriple (4cf9087e-f9e1-4ccd-b9a2-527e2507f7cd)
 Call ID: 4cf9087e-f9e1-4ccd-b9a2-527e2507f7cd
  Args:
    target: Luise_Amalia_Klein
    relation: :hasMother
    source: Charlotte_Luise_Auguste_Tiedemann
  AssignClass (c07c918e-0945-4247-bfe1-baae8ef9b8a2)
 Call ID: c07c918e-0945-4247-bfe1-baae8ef9b8a2
  Args:
    source: Juan_Carlos_I
    type: :Man
  AddTriple (4e9596dc-f341-46b3-9998-a4747869ad4a)
 Call ID: 4e9596dc-f341-46b3-9998-a4747869ad4a
  Args:
    target: Juan_Carlos_I
    source: Infante_Jaime
    relation: :hasRelation
  Finish (a2c8a6b1-b8e5-4937-a295-cc8b33886e71)
 Call ID: a2c8a6b1-b8e5-4937-a295-cc8b33886e71
  Args: