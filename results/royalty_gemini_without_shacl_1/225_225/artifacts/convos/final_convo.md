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


Charles Philippe Marie Louis d'Orléans (born 3 March 1973) is a member of the House of Orléans.
He is the elder of two sons of Prince Michel d'Orléans and his former wife Béatrice Pasquier de Franclieu.
His paternal grandfather was Prince Henri d'Orléans, the Orléanist pretender to the French throne.
The couple's only child, Princess Isabelle d'Orléans, was born on 22 February 2012 in Lisbon, Portugal.
Her godparents are Princess Maria Theodora zu Löwenstein-Wertheim-Freudenberg and Felipe VI of Spain (then Prince of Asturias).
Charles-Philippe and Naomi-Valeska's child, Princess Élisabeth Victoire Jeanne Marie d'Orléans, was born on 15 April 2026 in Monaco.
His acceptance of this role placed the order under the sanction of a dynastic prince of the House of Bourbon, in what is said to be a continuation of a tradition established since the 13th century when the Order of Saint Lazarus came under the protection of King Philippe le Bel.
Title controversy

On 8 December 2004, he received the title "Duke of Anjou" from his uncle Prince Henri d'Orléans, head of the House of Orléans.
There is some controversy in the use of this title by an Orléans prince.



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
  AssignClass (116177b7-e957-4d8b-a713-5a1d99bca6ac)
 Call ID: 116177b7-e957-4d8b-a713-5a1d99bca6ac
  Args:
    type: :Man
    source: Charles_Philippe_d_Orleans
  AssignClass (8dc29ebf-b592-4aa3-8164-b839977cd791)
 Call ID: 8dc29ebf-b592-4aa3-8164-b839977cd791
  Args:
    type: :Person
    source: Charles_Philippe_d_Orleans
  AddLiteral (29cc539d-9c25-4415-98c9-dcac17fcec96)
 Call ID: 29cc539d-9c25-4415-98c9-dcac17fcec96
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1973
    source: Charles_Philippe_d_Orleans
  AssignClass (80364713-7fb9-4899-ae40-fc3ebe911251)
 Call ID: 80364713-7fb9-4899-ae40-fc3ebe911251
  Args:
    type: :Man
    source: Prince_Michel_d_Orleans
  AssignClass (5f4e628f-a7f7-4fb3-834d-7a3f6b86ed44)
 Call ID: 5f4e628f-a7f7-4fb3-834d-7a3f6b86ed44
  Args:
    type: :Person
    source: Prince_Michel_d_Orleans
  AssignClass (b0193d76-ed8b-481b-8e01-f6f01afae891)
 Call ID: b0193d76-ed8b-481b-8e01-f6f01afae891
  Args:
    type: :Woman
    source: Beatrice_Pasquier_de_Franclieu
  AssignClass (37ee3e33-a2db-4156-9e1a-4f899c14e4ef)
 Call ID: 37ee3e33-a2db-4156-9e1a-4f899c14e4ef
  Args:
    type: :Person
    source: Beatrice_Pasquier_de_Franclieu
  AddTriple (707dad54-844d-4138-b502-626993b96238)
 Call ID: 707dad54-844d-4138-b502-626993b96238
  Args:
    target: Prince_Michel_d_Orleans
    source: Charles_Philippe_d_Orleans
    relation: :hasFather
  AddTriple (f80bef30-6d23-4abb-8cae-b1c222d0f6f8)
 Call ID: f80bef30-6d23-4abb-8cae-b1c222d0f6f8
  Args:
    relation: :hasMother
    target: Beatrice_Pasquier_de_Franclieu
    source: Charles_Philippe_d_Orleans
  AssignClass (47366d71-7cb2-4bd3-a590-3ff4b1daf95a)
 Call ID: 47366d71-7cb2-4bd3-a590-3ff4b1daf95a
  Args:
    type: :Man
    source: Prince_Henri_d_Orleans
  AssignClass (e45a4d5e-3e04-42c8-a593-3aaceed44769)
 Call ID: e45a4d5e-3e04-42c8-a593-3aaceed44769
  Args:
    type: :Person
    source: Prince_Henri_d_Orleans
  AddTriple (53feef42-dacc-443f-9ca9-fe828f37b38c)
 Call ID: 53feef42-dacc-443f-9ca9-fe828f37b38c
  Args:
    relation: :hasFather
    target: Prince_Henri_d_Orleans
    source: Prince_Michel_d_Orleans
  AssignClass (144ac603-080d-423b-8fd7-93c372f9040b)
 Call ID: 144ac603-080d-423b-8fd7-93c372f9040b
  Args:
    type: :Woman
    source: Princess_Isabelle_d_Orleans
  AssignClass (29cdee28-eae9-4f48-9d99-661f131351aa)
 Call ID: 29cdee28-eae9-4f48-9d99-661f131351aa
  Args:
    type: :Person
    source: Princess_Isabelle_d_Orleans
  AddTriple (924abafa-4de8-41b9-ba5e-c22924222bd3)
 Call ID: 924abafa-4de8-41b9-ba5e-c22924222bd3
  Args:
    relation: :hasFather
    source: Princess_Isabelle_d_Orleans
    target: Prince_Michel_d_Orleans
  AddTriple (057fda43-52c5-4e5c-8028-f43b7554a7ca)
 Call ID: 057fda43-52c5-4e5c-8028-f43b7554a7ca
  Args:
    relation: :hasMother
    target: Beatrice_Pasquier_de_Franclieu
    source: Princess_Isabelle_d_Orleans
  AddLiteral (59552392-0302-4063-808f-ee90285ca733)
 Call ID: 59552392-0302-4063-808f-ee90285ca733
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Princess_Isabelle_d_Orleans
    literal_value: 2012
  AssignClass (8a5981eb-64eb-463b-a7e0-463e09f6c659)
 Call ID: 8a5981eb-64eb-463b-a7e0-463e09f6c659
  Args:
    type: :Woman
    source: Princess_Elisabeth_Victoire_Jeanne_Marie_d_Orleans
  AssignClass (cec8f719-cc3c-4211-85e7-582bcfde1c03)
 Call ID: cec8f719-cc3c-4211-85e7-582bcfde1c03
  Args:
    type: :Person
    source: Princess_Elisabeth_Victoire_Jeanne_Marie_d_Orleans
  AssignClass (48d76ce1-2098-4b4e-9ca9-3814d7aada9a)
 Call ID: 48d76ce1-2098-4b4e-9ca9-3814d7aada9a
  Args:
    type: :Woman
    source: Naomi_Valeska
  AssignClass (cb82a62f-0ba2-4043-a49e-9e1b902d0b7b)
 Call ID: cb82a62f-0ba2-4043-a49e-9e1b902d0b7b
  Args:
    type: :Person
    source: Naomi_Valeska
  AddTriple (0ffa51ac-f151-405a-9a32-6d7a4f1ca6a2)
 Call ID: 0ffa51ac-f151-405a-9a32-6d7a4f1ca6a2
  Args:
    relation: :hasFather
    target: Charles_Philippe_d_Orleans
    source: Princess_Elisabeth_Victoire_Jeanne_Marie_d_Orleans
  AddTriple (16b12c7a-cd09-4319-a0f8-e38f5aac2dd9)
 Call ID: 16b12c7a-cd09-4319-a0f8-e38f5aac2dd9
  Args:
    relation: :hasMother
    source: Princess_Elisabeth_Victoire_Jeanne_Marie_d_Orleans
    target: Naomi_Valeska
  AddLiteral (3d4871b4-0f66-41cb-ba4e-7882aa5de092)
 Call ID: 3d4871b4-0f66-41cb-ba4e-7882aa5de092
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 2026
    source: Princess_Elisabeth_Victoire_Jeanne_Marie_d_Orleans
  Finish (963c8830-197b-4526-ad4e-7a3ba493ad8c)
 Call ID: 963c8830-197b-4526-ad4e-7a3ba493ad8c
  Args: