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
  AssignClass (44326bc4-cad2-4c9d-b961-067f30d3e731)
 Call ID: 44326bc4-cad2-4c9d-b961-067f30d3e731
  Args:
    type: :Man
    source: Jaime_de_Borbón_y_Battenberg
  AssignClass (d88f536c-72b3-4435-96a0-7393c6f62b88)
 Call ID: d88f536c-72b3-4435-96a0-7393c6f62b88
  Args:
    type: :Man
    source: Alfonso_XIII_of_Spain
  AssignClass (55ef130c-f511-4626-a1c6-80cd2e4cdf34)
 Call ID: 55ef130c-f511-4626-a1c6-80cd2e4cdf34
  Args:
    type: :Woman
    source: Victoria_Eugenie_of_Battenberg
  AddLiteral (2e24b1c0-dd90-4254-b508-1860b456c13d)
 Call ID: 2e24b1c0-dd90-4254-b508-1860b456c13d
  Args:
    literal_type: xsd:integer
    literal_value: 1908
    source: Jaime_de_Borbón_y_Battenberg
    relation: :hasBirthYear
  AddLiteral (d4488c61-14b4-4b41-a66c-7963d415a8c9)
 Call ID: d4488c61-14b4-4b41-a66c-7963d415a8c9
  Args:
    relation: :hasDeathYear
    source: Jaime_de_Borbón_y_Battenberg
    literal_value: 1975
    literal_type: xsd:integer
  AddTriple (52f556c6-3342-4e9a-b48c-231690effbce)
 Call ID: 52f556c6-3342-4e9a-b48c-231690effbce
  Args:
    relation: :hasFather
    target: Alfonso_XIII_of_Spain
    source: Jaime_de_Borbón_y_Battenberg
  AddTriple (c7099db4-df5a-426b-ae54-41e839193e16)
 Call ID: c7099db4-df5a-426b-ae54-41e839193e16
  Args:
    source: Jaime_de_Borbón_y_Battenberg
    target: Victoria_Eugenie_of_Battenberg
    relation: :hasMother
  AssignClass (1c8f8dad-29a5-4ca4-b9e7-79fd7ac474c7)
 Call ID: 1c8f8dad-29a5-4ca4-b9e7-79fd7ac474c7
  Args:
    type: :Man
    source: Alfonso_Prince_of_Asturias
  AssignClass (5079ddba-77bf-4754-8ff3-d877da788682)
 Call ID: 5079ddba-77bf-4754-8ff3-d877da788682
  Args:
    type: :Man
    source: Juan_Count_of_Barcelona
  AssignClass (da5225eb-1266-4db7-9bbe-59fbad605af0)
 Call ID: da5225eb-1266-4db7-9bbe-59fbad605af0
  Args:
    type: :Man
    source: Gonzalo_de_Borbón
  AssignClass (ae4c5431-dc35-4066-96ee-fd0a3db727bb)
 Call ID: ae4c5431-dc35-4066-96ee-fd0a3db727bb
  Args:
    type: :Woman
    source: Beatriz_de_Borbón
  AssignClass (edc812c6-ee0a-4dc7-a112-18fb4f910a65)
 Call ID: edc812c6-ee0a-4dc7-a112-18fb4f910a65
  Args:
    type: :Woman
    source: María_Cristina_de_Borbón
  AddTriple (fb03dda5-b26a-4bfd-8f07-b17a26087f2e)
 Call ID: fb03dda5-b26a-4bfd-8f07-b17a26087f2e
  Args:
    relation: :hasFather
    target: Alfonso_XIII_of_Spain
    source: Alfonso_Prince_of_Asturias
  AddTriple (32891b46-00a8-4d1c-9109-fef917b6b50a)
 Call ID: 32891b46-00a8-4d1c-9109-fef917b6b50a
  Args:
    source: Alfonso_Prince_of_Asturias
    target: Victoria_Eugenie_of_Battenberg
    relation: :hasMother
  AddTriple (d45d05df-4ca3-47a4-a0ce-a275c79a3f18)
 Call ID: d45d05df-4ca3-47a4-a0ce-a275c79a3f18
  Args:
    relation: :hasFather
    target: Alfonso_XIII_of_Spain
    source: Juan_Count_of_Barcelona
  AddTriple (bb2fdbfa-be40-4138-9eef-1ef1f4e39c6f)
 Call ID: bb2fdbfa-be40-4138-9eef-1ef1f4e39c6f
  Args:
    source: Juan_Count_of_Barcelona
    relation: :hasMother
    target: Victoria_Eugenie_of_Battenberg
  AddTriple (c5cd6916-3cc1-48f4-9e4c-1b6af2483e50)
 Call ID: c5cd6916-3cc1-48f4-9e4c-1b6af2483e50
  Args:
    target: Alfonso_XIII_of_Spain
    relation: :hasFather
    source: Gonzalo_de_Borbón
  AddTriple (101c41b5-74f4-4a50-af86-407664c05471)
 Call ID: 101c41b5-74f4-4a50-af86-407664c05471
  Args:
    source: Gonzalo_de_Borbón
    relation: :hasMother
    target: Victoria_Eugenie_of_Battenberg
  AddTriple (6b7f0de1-61e1-4992-9382-9ef36d1521ae)
 Call ID: 6b7f0de1-61e1-4992-9382-9ef36d1521ae
  Args:
    source: Beatriz_de_Borbón
    relation: :hasFather
    target: Alfonso_XIII_of_Spain
  AddTriple (6fbdd222-9e12-47ca-91ca-bfb018434276)
 Call ID: 6fbdd222-9e12-47ca-91ca-bfb018434276
  Args:
    relation: :hasMother
    target: Victoria_Eugenie_of_Battenberg
    source: Beatriz_de_Borbón
  AddTriple (59f471a2-e77b-449f-99b9-74943a8901b1)
 Call ID: 59f471a2-e77b-449f-99b9-74943a8901b1
  Args:
    relation: :hasFather
    target: Alfonso_XIII_of_Spain
    source: María_Cristina_de_Borbón
  AddTriple (ed995ecb-cae2-457a-87e9-2c27861245e9)
 Call ID: ed995ecb-cae2-457a-87e9-2c27861245e9
  Args:
    source: María_Cristina_de_Borbón
    target: Victoria_Eugenie_of_Battenberg
    relation: :hasMother
  AssignClass (e7154f5b-47f5-42e5-8a72-f8f3ff6ec0ae)
 Call ID: e7154f5b-47f5-42e5-8a72-f8f3ff6ec0ae
  Args:
    type: :Woman
    source: Emanuela_de_Dampierre
  AssignClass (394deb20-b6a0-4994-b549-388df3fe4289)
 Call ID: 394deb20-b6a0-4994-b549-388df3fe4289
  Args:
    type: :Man
    source: Alfonso_de_Borbón_son_of_Jaime
  AssignClass (cc7ce0d1-68ae-4a8a-8162-a9d3ee15dbfa)
 Call ID: cc7ce0d1-68ae-4a8a-8162-a9d3ee15dbfa
  Args:
    type: :Man
    source: Gonzalo_de_Borbón_son_of_Jaime
  AddTriple (ef797d0e-3089-46a6-945e-1705c26533e0)
 Call ID: ef797d0e-3089-46a6-945e-1705c26533e0
  Args:
    target: Jaime_de_Borbón_y_Battenberg
    relation: :hasFather
    source: Alfonso_de_Borbón_son_of_Jaime
  AddTriple (a0e5ddf7-d00e-4259-9a42-346a008c3388)
 Call ID: a0e5ddf7-d00e-4259-9a42-346a008c3388
  Args:
    source: Alfonso_de_Borbón_son_of_Jaime
    target: Emanuela_de_Dampierre
    relation: :hasMother
  AddTriple (521b8c63-37d7-42a3-9c61-bbf5e08e70f1)
 Call ID: 521b8c63-37d7-42a3-9c61-bbf5e08e70f1
  Args:
    source: Gonzalo_de_Borbón_son_of_Jaime
    relation: :hasFather
    target: Jaime_de_Borbón_y_Battenberg
  AddTriple (9bb740e5-68f3-44ce-89bc-d52cc14798d0)
 Call ID: 9bb740e5-68f3-44ce-89bc-d52cc14798d0
  Args:
    source: Gonzalo_de_Borbón_son_of_Jaime
    relation: :hasMother
    target: Emanuela_de_Dampierre
  AssignClass (63a984c9-0ef8-42bd-8878-a49a11a5b54f)
 Call ID: 63a984c9-0ef8-42bd-8878-a49a11a5b54f
  Args:
    type: :Woman
    source: Charlotte_Luise_Auguste_Tiedemann
  AssignClass (ced251a6-5d60-42db-b281-2e5fa1283e89)
 Call ID: ced251a6-5d60-42db-b281-2e5fa1283e89
  Args:
    type: :Man
    source: Otto_Eugen_Tiedemann
  AssignClass (57e540d9-3aa4-4794-a71b-da703f7f30e6)
 Call ID: 57e540d9-3aa4-4794-a71b-da703f7f30e6
  Args:
    type: :Woman
    source: Luise_Amalia_Klein
  AddTriple (c2e04315-db0e-487c-ba47-1593fd386788)
 Call ID: c2e04315-db0e-487c-ba47-1593fd386788
  Args:
    target: Otto_Eugen_Tiedemann
    relation: :hasFather
    source: Charlotte_Luise_Auguste_Tiedemann
  AddTriple (77ae739f-8abe-4f03-b9bf-32c5f4295894)
 Call ID: 77ae739f-8abe-4f03-b9bf-32c5f4295894
  Args:
    source: Charlotte_Luise_Auguste_Tiedemann
    relation: :hasMother
    target: Luise_Amalia_Klein
  AssignClass (dec60646-27ce-4e84-9957-f24db9dfeb90)
 Call ID: dec60646-27ce-4e84-9957-f24db9dfeb90
  Args:
    type: :Man
    source: Juan_Carlos_I
  Finish (be17abb9-f09e-43d7-911b-e95a7ab7986c)
 Call ID: be17abb9-f09e-43d7-911b-e95a7ab7986c
  Args: