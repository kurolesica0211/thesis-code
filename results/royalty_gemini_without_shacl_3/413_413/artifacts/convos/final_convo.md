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
  AssignClass (2ee8cf37-e5db-4662-b477-0f4e65dfb2e6)
 Call ID: 2ee8cf37-e5db-4662-b477-0f4e65dfb2e6
  Args:
    type: :Man
    source: :Jaime_of_Spain
  AssignClass (bfc991c5-1070-432b-ab3a-5df6242c2fbb)
 Call ID: bfc991c5-1070-432b-ab3a-5df6242c2fbb
  Args:
    type: :Person
    source: :Jaime_of_Spain
  AssignClass (02ac1f89-023c-4a7c-9281-cb5ec9604b05)
 Call ID: 02ac1f89-023c-4a7c-9281-cb5ec9604b05
  Args:
    type: :Man
    source: :Alfonso_XIII_of_Spain
  AssignClass (f9e440c3-89e8-4ebc-9234-01da01ac6869)
 Call ID: f9e440c3-89e8-4ebc-9234-01da01ac6869
  Args:
    type: :Person
    source: :Alfonso_XIII_of_Spain
  AssignClass (0a7d0b80-e34c-4050-a5a4-31ed40fead5e)
 Call ID: 0a7d0b80-e34c-4050-a5a4-31ed40fead5e
  Args:
    type: :Woman
    source: :Victoria_Eugenie_of_Battenberg
  AssignClass (7783c023-70e7-46f7-b246-4a112e547e5b)
 Call ID: 7783c023-70e7-46f7-b246-4a112e547e5b
  Args:
    type: :Person
    source: :Victoria_Eugenie_of_Battenberg
  AddLiteral (4621ead2-55ea-410e-872c-1096dc219588)
 Call ID: 4621ead2-55ea-410e-872c-1096dc219588
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1908
    source: :Jaime_of_Spain
  AddLiteral (cf14b6b2-249d-45fc-939b-418c772a84cb)
 Call ID: cf14b6b2-249d-45fc-939b-418c772a84cb
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1975
    source: :Jaime_of_Spain
  AddTriple (99a2e1ba-941c-44ab-b8b4-35a816ab6b2d)
 Call ID: 99a2e1ba-941c-44ab-b8b4-35a816ab6b2d
  Args:
    target: :Alfonso_XIII_of_Spain
    source: :Jaime_of_Spain
    relation: :hasFather
  AddTriple (b427e0fe-839d-49e8-9fdd-f74981edfff3)
 Call ID: b427e0fe-839d-49e8-9fdd-f74981edfff3
  Args:
    relation: :hasMother
    source: :Jaime_of_Spain
    target: :Victoria_Eugenie_of_Battenberg
  AssignClass (4b99f454-ee54-46c3-8a63-976a6f393f1c)
 Call ID: 4b99f454-ee54-46c3-8a63-976a6f393f1c
  Args:
    type: :Man
    source: :Alfonso_Prince_of_Asturias
  AssignClass (e11f2ca2-2160-48e1-99fb-267b4a24c641)
 Call ID: e11f2ca2-2160-48e1-99fb-267b4a24c641
  Args:
    type: :Person
    source: :Alfonso_Prince_of_Asturias
  AssignClass (8c6e4999-84c3-4abb-b94e-ec92e3331e12)
 Call ID: 8c6e4999-84c3-4abb-b94e-ec92e3331e12
  Args:
    type: :Man
    source: :Juan_Count_of_Barcelona
  AssignClass (4884aa74-edf0-4550-9a72-cf76b6fc135f)
 Call ID: 4884aa74-edf0-4550-9a72-cf76b6fc135f
  Args:
    type: :Person
    source: :Juan_Count_of_Barcelona
  AssignClass (5ad3a415-8e5d-4a65-8b84-85ecffc0920f)
 Call ID: 5ad3a415-8e5d-4a65-8b84-85ecffc0920f
  Args:
    type: :Man
    source: :Gonzalo_of_Spain
  AssignClass (ee04abcd-2e9b-4825-bbaa-7b88ad7a67af)
 Call ID: ee04abcd-2e9b-4825-bbaa-7b88ad7a67af
  Args:
    type: :Person
    source: :Gonzalo_of_Spain
  AssignClass (dc57e59f-b0c8-4e4f-9238-0851e53af198)
 Call ID: dc57e59f-b0c8-4e4f-9238-0851e53af198
  Args:
    type: :Woman
    source: :Beatriz_of_Spain
  AssignClass (20dfaf53-60ef-41e6-a1ee-3fc28efc4aca)
 Call ID: 20dfaf53-60ef-41e6-a1ee-3fc28efc4aca
  Args:
    type: :Person
    source: :Beatriz_of_Spain
  AssignClass (e93d7e6f-bb43-4bb6-8448-a726d8b2ef4b)
 Call ID: e93d7e6f-bb43-4bb6-8448-a726d8b2ef4b
  Args:
    type: :Woman
    source: :Maria_Cristina_of_Spain
  AssignClass (aced59ba-1a0a-4e19-93b9-fa797cc85cb9)
 Call ID: aced59ba-1a0a-4e19-93b9-fa797cc85cb9
  Args:
    type: :Person
    source: :Maria_Cristina_of_Spain
  AddTriple (0eeee6a5-a786-46c2-8a57-b74376ba8ca7)
 Call ID: 0eeee6a5-a786-46c2-8a57-b74376ba8ca7
  Args:
    target: :Alfonso_XIII_of_Spain
    relation: :hasFather
    source: :Alfonso_Prince_of_Asturias
  AddTriple (6ba7be8b-863c-4b8b-acd4-7a4f1e5c03c3)
 Call ID: 6ba7be8b-863c-4b8b-acd4-7a4f1e5c03c3
  Args:
    relation: :hasMother
    source: :Alfonso_Prince_of_Asturias
    target: :Victoria_Eugenie_of_Battenberg
  AddTriple (28552b59-0fb2-461f-8dc5-6a1e0ed87e1d)
 Call ID: 28552b59-0fb2-461f-8dc5-6a1e0ed87e1d
  Args:
    target: :Alfonso_XIII_of_Spain
    relation: :hasFather
    source: :Juan_Count_of_Barcelona
  AddTriple (a974e37b-38df-42f7-9070-0138d757b6a9)
 Call ID: a974e37b-38df-42f7-9070-0138d757b6a9
  Args:
    relation: :hasMother
    source: :Juan_Count_of_Barcelona
    target: :Victoria_Eugenie_of_Battenberg
  AddTriple (2f8cb4bd-cc10-43dc-a0f7-dc33d5a607f9)
 Call ID: 2f8cb4bd-cc10-43dc-a0f7-dc33d5a607f9
  Args:
    relation: :hasFather
    source: :Gonzalo_of_Spain
    target: :Alfonso_XIII_of_Spain
  AddTriple (c29a59bf-0278-409b-904c-bac1ee892c5f)
 Call ID: c29a59bf-0278-409b-904c-bac1ee892c5f
  Args:
    target: :Victoria_Eugenie_of_Battenberg
    source: :Gonzalo_of_Spain
    relation: :hasMother
  AddTriple (1a14627d-457b-44fd-b4e6-7e87af606ae7)
 Call ID: 1a14627d-457b-44fd-b4e6-7e87af606ae7
  Args:
    target: :Alfonso_XIII_of_Spain
    relation: :hasFather
    source: :Beatriz_of_Spain
  AddTriple (3e23b241-8cc6-4fe6-b0df-7d33a7b6af93)
 Call ID: 3e23b241-8cc6-4fe6-b0df-7d33a7b6af93
  Args:
    source: :Beatriz_of_Spain
    relation: :hasMother
    target: :Victoria_Eugenie_of_Battenberg
  AddTriple (39155ffe-d7cf-4afc-b03a-b906071934a4)
 Call ID: 39155ffe-d7cf-4afc-b03a-b906071934a4
  Args:
    target: :Alfonso_XIII_of_Spain
    source: :Maria_Cristina_of_Spain
    relation: :hasFather
  AddTriple (68490d0f-bd4c-423b-abd5-e023a31d9edd)
 Call ID: 68490d0f-bd4c-423b-abd5-e023a31d9edd
  Args:
    target: :Victoria_Eugenie_of_Battenberg
    source: :Maria_Cristina_of_Spain
    relation: :hasMother
  AssignClass (8943edc9-83ff-4df8-bd01-6f54e79f3c66)
 Call ID: 8943edc9-83ff-4df8-bd01-6f54e79f3c66
  Args:
    type: :Woman
    source: :Emanuela_de_Dampierre
  AssignClass (4f3f4625-7543-4251-9c22-56f30a35493d)
 Call ID: 4f3f4625-7543-4251-9c22-56f30a35493d
  Args:
    type: :Person
    source: :Emanuela_de_Dampierre
  AssignClass (1a28c237-2f74-42b8-9d5a-cc2ba3108a82)
 Call ID: 1a28c237-2f74-42b8-9d5a-cc2ba3108a82
  Args:
    type: :Man
    source: :Alfonso_de_Borbon_son_of_Jaime
  AssignClass (f39a3c24-3f41-4da0-ab1f-b0f77e801879)
 Call ID: f39a3c24-3f41-4da0-ab1f-b0f77e801879
  Args:
    type: :Person
    source: :Alfonso_de_Borbon_son_of_Jaime
  AssignClass (a11342f0-95c7-4490-b470-05f42d5be914)
 Call ID: a11342f0-95c7-4490-b470-05f42d5be914
  Args:
    type: :Man
    source: :Gonzalo_de_Borbon_son_of_Jaime
  AssignClass (f0e5abe3-764c-4496-a43a-cad2f59040af)
 Call ID: f0e5abe3-764c-4496-a43a-cad2f59040af
  Args:
    type: :Person
    source: :Gonzalo_de_Borbon_son_of_Jaime
  AddTriple (9e1ce85a-da1e-40be-901f-9844788dd5f3)
 Call ID: 9e1ce85a-da1e-40be-901f-9844788dd5f3
  Args:
    target: :Jaime_of_Spain
    relation: :hasFather
    source: :Alfonso_de_Borbon_son_of_Jaime
  AddTriple (aac69184-c4a2-4c38-b922-f7cbb3ad97dd)
 Call ID: aac69184-c4a2-4c38-b922-f7cbb3ad97dd
  Args:
    target: :Emanuela_de_Dampierre
    relation: :hasMother
    source: :Alfonso_de_Borbon_son_of_Jaime
  AddTriple (289591b6-8832-458b-9c04-effe9a34a359)
 Call ID: 289591b6-8832-458b-9c04-effe9a34a359
  Args:
    target: :Jaime_of_Spain
    relation: :hasFather
    source: :Gonzalo_de_Borbon_son_of_Jaime
  AddTriple (279e04df-1e1e-46be-a613-32e2b33a0be6)
 Call ID: 279e04df-1e1e-46be-a613-32e2b33a0be6
  Args:
    target: :Emanuela_de_Dampierre
    source: :Gonzalo_de_Borbon_son_of_Jaime
    relation: :hasMother
  AssignClass (00b8e294-cd7b-42f6-9a1e-bb3de29a21ff)
 Call ID: 00b8e294-cd7b-42f6-9a1e-bb3de29a21ff
  Args:
    type: :Woman
    source: :Charlotte_Luise_Auguste_Tiedemann
  AssignClass (c3a71e4e-9f74-4825-9c50-1e22a9db6205)
 Call ID: c3a71e4e-9f74-4825-9c50-1e22a9db6205
  Args:
    type: :Person
    source: :Charlotte_Luise_Auguste_Tiedemann
  AddLiteral (7c504cca-5afb-4b3e-8605-9d8a66f9dae4)
 Call ID: 7c504cca-5afb-4b3e-8605-9d8a66f9dae4
  Args:
    relation: :hasBirthYear
    literal_value: 1919
    source: :Charlotte_Luise_Auguste_Tiedemann
    literal_type: xsd:integer
  AddLiteral (3fa8461d-4fef-4db2-9ee3-1f0868ca2a38)
 Call ID: 3fa8461d-4fef-4db2-9ee3-1f0868ca2a38
  Args:
    relation: :hasDeathYear
    source: :Charlotte_Luise_Auguste_Tiedemann
    literal_value: 1979
    literal_type: xsd:integer
  AssignClass (2e39734e-7997-4108-8344-fa4456cc251a)
 Call ID: 2e39734e-7997-4108-8344-fa4456cc251a
  Args:
    type: :Man
    source: :Otto_Eugen_Tiedemann
  AssignClass (1449e6cc-896f-460e-aa83-146b9f64ff59)
 Call ID: 1449e6cc-896f-460e-aa83-146b9f64ff59
  Args:
    type: :Person
    source: :Otto_Eugen_Tiedemann
  AssignClass (94ea9b2d-a147-4eeb-bf09-ae058ece0828)
 Call ID: 94ea9b2d-a147-4eeb-bf09-ae058ece0828
  Args:
    type: :Woman
    source: :Luise_Amalia_Klein
  AssignClass (f27608db-c1ab-4cc2-8226-84823ea053fb)
 Call ID: f27608db-c1ab-4cc2-8226-84823ea053fb
  Args:
    type: :Person
    source: :Luise_Amalia_Klein
  AddTriple (856e17f7-3514-4dcb-8afa-259144f964de)
 Call ID: 856e17f7-3514-4dcb-8afa-259144f964de
  Args:
    target: :Otto_Eugen_Tiedemann
    relation: :hasFather
    source: :Charlotte_Luise_Auguste_Tiedemann
  AddTriple (dd314102-d18d-4b14-81eb-4dbe03d95817)
 Call ID: dd314102-d18d-4b14-81eb-4dbe03d95817
  Args:
    source: :Charlotte_Luise_Auguste_Tiedemann
    relation: :hasMother
    target: :Luise_Amalia_Klein
  Finish (6c8995b9-2739-488a-aa27-8fbd500cc6fb)
 Call ID: 6c8995b9-2739-488a-aa27-8fbd500cc6fb
  Args: