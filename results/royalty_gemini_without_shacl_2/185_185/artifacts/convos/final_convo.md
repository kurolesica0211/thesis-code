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
Queen Anne-Marie


Queen Sofía of Spain


Marina, consort of Prince Michael


The Duke of AostaThe Duchess of Aosta


The Dowager Duchess of Aosta


Princess Olga Isabelle of Savoy-Aosta, Duchess of Aosta (née Princess Olga of Greece;
Greek: Πριγκίπισσα Όλγα της Ελλάδας; born 11 November 1971), is the younger daughter of author Prince Michael of Greece and Denmark and Marina Karella, an artist and daughter of the Greek business magnate Theódoros Karéllas.
Olga is married to her second cousin Prince Aimone, Duke of Aosta.
Early life

Princess Olga was born on 11 November 1971 in Athens, Greece.
She is the younger sister of Princess Alexandra and grew up in Paris and New York, spending summers at the family's island retreat at Patmos, Greece.
Although Olga worked for a while in interior decoration, she went to Panama to photograph and study phalaena.
As Princess Olga's parents' marriage is morganatic, and therefore non-dynastic, she is a Greek princess by birth but not a Danish princess, used the style Her Highness instead of Her Royal Highness (until her marriage), and is excluded from the line of succession to the former Greek throne.
Engagement, marriage and children

Olga's engagement to Prince Aimone of Savoy, son of Amedeo, 5th Duke of Aosta, was announced in May 2005.
Aimone and Olga are second cousins; both being great-grandchildren of the French pretender Jean d'Orléans, duc de Guise.
They are also second cousins once removed as George I of Greece is Aimone's great-great-grandfather and Olga's great-grandfather.
Olga's father, Prince Michael of Greece and Denmark, Aimone's paternal grandmother, Princess Irene, Duchess of Aosta (née Princess Irene of Greece and Denmark), and Prince Philip, Duke of Edinburgh (born Prince Philip of Greece and Denmark), were all first cousins.
A canonical dispensation was obtained from the Catholic Archbishop of Moscow, Monsignor Paolo Pezzi, who was the local Ordinary of prince Aimone.
On 7 March 2009, Princess Olga gave birth to a son named Umberto in Paris, France.
On 24 May 2011 in Paris, Olga gave birth to another son, named Amedeo Michele.
On 14 December 2012, Olga gave birth to a baby daughter, Isabella Vita Marina, in Paris, France.



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
  AssignClass (aadadfa1-5a53-4569-bf07-5fa65301a234)
 Call ID: aadadfa1-5a53-4569-bf07-5fa65301a234
  Args:
    type: :Woman
    source: Princess_Olga_of_Greece
  AssignClass (b600a34e-cf00-4297-a825-075b7953e709)
 Call ID: b600a34e-cf00-4297-a825-075b7953e709
  Args:
    type: :Person
    source: Princess_Olga_of_Greece
  AddLiteral (0905228b-b6de-4c34-a5db-e1460edb4a6a)
 Call ID: 0905228b-b6de-4c34-a5db-e1460edb4a6a
  Args:
    literal_value: 1971-11-11
    literal_type: xsd:date
    relation: :hasBirthYear
    source: Princess_Olga_of_Greece
  AssignClass (64dc49f2-ea36-4aee-a0ef-75717bbdc6cb)
 Call ID: 64dc49f2-ea36-4aee-a0ef-75717bbdc6cb
  Args:
    source: Prince_Michael_of_Greece_and_Denmark
    type: :Man
  AssignClass (16ad632a-88fc-468f-a132-3b1c6c214dfe)
 Call ID: 16ad632a-88fc-468f-a132-3b1c6c214dfe
  Args:
    source: Prince_Michael_of_Greece_and_Denmark
    type: :Person
  AssignClass (62d83b33-efeb-4e33-b1d7-65e80e78b328)
 Call ID: 62d83b33-efeb-4e33-b1d7-65e80e78b328
  Args:
    type: :Woman
    source: Marina_Karella
  AssignClass (ae154ea9-4e47-4b76-92f0-74ec66180823)
 Call ID: ae154ea9-4e47-4b76-92f0-74ec66180823
  Args:
    source: Marina_Karella
    type: :Person
  AddTriple (36b50fa1-caa7-464a-9722-d5259d3c8eb7)
 Call ID: 36b50fa1-caa7-464a-9722-d5259d3c8eb7
  Args:
    source: Princess_Olga_of_Greece
    target: Prince_Michael_of_Greece_and_Denmark
    relation: :hasFather
  AddTriple (59fa4c51-387e-4af2-bf1f-f09bea2b62db)
 Call ID: 59fa4c51-387e-4af2-bf1f-f09bea2b62db
  Args:
    relation: :hasMother
    target: Marina_Karella
    source: Princess_Olga_of_Greece
  AssignClass (2c0e8a1d-733f-4854-ac0e-b426cc2efb1a)
 Call ID: 2c0e8a1d-733f-4854-ac0e-b426cc2efb1a
  Args:
    source: Theodoros_Karellas
    type: :Man
  AssignClass (37abf210-d97c-4a35-aa08-5924bfa83b86)
 Call ID: 37abf210-d97c-4a35-aa08-5924bfa83b86
  Args:
    type: :Person
    source: Theodoros_Karellas
  AddTriple (403f49ff-ec9e-421d-b9ed-825af171b72a)
 Call ID: 403f49ff-ec9e-421d-b9ed-825af171b72a
  Args:
    source: Marina_Karella
    target: Theodoros_Karellas
    relation: :hasFather
  AssignClass (5d6050dc-4df8-43d4-bc2e-12152340e1f7)
 Call ID: 5d6050dc-4df8-43d4-bc2e-12152340e1f7
  Args:
    type: :Woman
    source: Princess_Alexandra_of_Greece
  AssignClass (89c0ec23-137c-4c7e-b5be-b1e441bb7f66)
 Call ID: 89c0ec23-137c-4c7e-b5be-b1e441bb7f66
  Args:
    type: :Person
    source: Princess_Alexandra_of_Greece
  AddTriple (78b4bdb6-0bfd-4de1-9f56-2a2f4ce18b8a)
 Call ID: 78b4bdb6-0bfd-4de1-9f56-2a2f4ce18b8a
  Args:
    relation: :hasSister
    source: Princess_Olga_of_Greece
    target: Princess_Alexandra_of_Greece
  AssignClass (50f8c8b1-8fcb-4f95-bc28-967c92c8f6f2)
 Call ID: 50f8c8b1-8fcb-4f95-bc28-967c92c8f6f2
  Args:
    source: Prince_Aimone_Duke_of_Aosta
    type: :Man
  AssignClass (3175edcc-574d-4f3d-bc87-c991da9bdda5)
 Call ID: 3175edcc-574d-4f3d-bc87-c991da9bdda5
  Args:
    type: :Person
    source: Prince_Aimone_Duke_of_Aosta
  AddTriple (0151ce52-feb5-4333-bb58-84eb19842cd6)
 Call ID: 0151ce52-feb5-4333-bb58-84eb19842cd6
  Args:
    relation: :hasRelation
    source: Princess_Olga_of_Greece
    target: Prince_Aimone_Duke_of_Aosta
  AssignClass (d9615e2a-5e29-4af4-82be-6fb99d517309)
 Call ID: d9615e2a-5e29-4af4-82be-6fb99d517309
  Args:
    source: Amedeo_5th_Duke_of_Aosta
    type: :Man
  AssignClass (f36ecd00-eae5-43d7-896d-f66d79bf1bb2)
 Call ID: f36ecd00-eae5-43d7-896d-f66d79bf1bb2
  Args:
    type: :Person
    source: Amedeo_5th_Duke_of_Aosta
  AddTriple (50a7452d-cf3f-4806-9d95-d228a5c84a80)
 Call ID: 50a7452d-cf3f-4806-9d95-d228a5c84a80
  Args:
    source: Prince_Aimone_Duke_of_Aosta
    target: Amedeo_5th_Duke_of_Aosta
    relation: :hasFather
  AssignClass (61b19775-ef8a-4da2-b736-3fd70a292164)
 Call ID: 61b19775-ef8a-4da2-b736-3fd70a292164
  Args:
    type: :Man
    source: Umberto_of_Savoy-Aosta
  AssignClass (1f6fe26d-e675-4adf-b940-231bcd4ea6e3)
 Call ID: 1f6fe26d-e675-4adf-b940-231bcd4ea6e3
  Args:
    type: :Person
    source: Umberto_of_Savoy-Aosta
  AddTriple (0fc49dd6-4774-40c2-b4e9-a5224a61edff)
 Call ID: 0fc49dd6-4774-40c2-b4e9-a5224a61edff
  Args:
    source: Umberto_of_Savoy-Aosta
    target: Prince_Aimone_Duke_of_Aosta
    relation: :hasFather
  AddTriple (04f042a4-f89e-4bbe-beaa-df5ad097ab31)
 Call ID: 04f042a4-f89e-4bbe-beaa-df5ad097ab31
  Args:
    target: Princess_Olga_of_Greece
    source: Umberto_of_Savoy-Aosta
    relation: :hasMother
  AssignClass (1d4127cb-a3bc-468e-8b61-5c07e801b0ba)
 Call ID: 1d4127cb-a3bc-468e-8b61-5c07e801b0ba
  Args:
    source: Amedeo_Michele_of_Savoy-Aosta
    type: :Man
  AssignClass (8af14a71-7def-441e-8050-d90afa24e5e4)
 Call ID: 8af14a71-7def-441e-8050-d90afa24e5e4
  Args:
    type: :Person
    source: Amedeo_Michele_of_Savoy-Aosta
  AddTriple (825cc368-b200-42c2-8c1e-a42a427152dc)
 Call ID: 825cc368-b200-42c2-8c1e-a42a427152dc
  Args:
    target: Prince_Aimone_Duke_of_Aosta
    source: Amedeo_Michele_of_Savoy-Aosta
    relation: :hasFather
  AddTriple (bac398f9-02fc-4bb8-af57-b2b1bf3a1fed)
 Call ID: bac398f9-02fc-4bb8-af57-b2b1bf3a1fed
  Args:
    target: Princess_Olga_of_Greece
    source: Amedeo_Michele_of_Savoy-Aosta
    relation: :hasMother
  AssignClass (9a6eacb5-c49e-44ab-be2e-0801ca5fe78b)
 Call ID: 9a6eacb5-c49e-44ab-be2e-0801ca5fe78b
  Args:
    type: :Woman
    source: Isabella_Vita_Marina_of_Savoy-Aosta
  AssignClass (57b61229-c770-49d9-bc87-1b08485cd00b)
 Call ID: 57b61229-c770-49d9-bc87-1b08485cd00b
  Args:
    source: Isabella_Vita_Marina_of_Savoy-Aosta
    type: :Person
  AddTriple (7b4e01ab-511d-43d5-8b7c-5450b1e9642c)
 Call ID: 7b4e01ab-511d-43d5-8b7c-5450b1e9642c
  Args:
    source: Isabella_Vita_Marina_of_Savoy-Aosta
    target: Prince_Aimone_Duke_of_Aosta
    relation: :hasFather
  AddTriple (35bbe693-08ca-461c-8890-455b0b5cc491)
 Call ID: 35bbe693-08ca-461c-8890-455b0b5cc491
  Args:
    relation: :hasMother
    source: Isabella_Vita_Marina_of_Savoy-Aosta
    target: Princess_Olga_of_Greece
  AssignClass (25233c62-059a-4be9-b2ea-1808d3640d2d)
 Call ID: 25233c62-059a-4be9-b2ea-1808d3640d2d
  Args:
    source: Princess_Irene_Duchess_of_Aosta
    type: :Woman
  AssignClass (721ad665-8c89-49d0-b493-fb5c0fc70b07)
 Call ID: 721ad665-8c89-49d0-b493-fb5c0fc70b07
  Args:
    source: Princess_Irene_Duchess_of_Aosta
    type: :Person
  AddTriple (bea398ac-023e-4c36-81c0-381286316c5b)
 Call ID: bea398ac-023e-4c36-81c0-381286316c5b
  Args:
    relation: :hasMother
    target: Princess_Irene_Duchess_of_Aosta
    source: Amedeo_5th_Duke_of_Aosta
  Finish (fedece8c-0447-4326-be8b-ef890dd169fc)
 Call ID: fedece8c-0447-4326-be8b-ef890dd169fc
  Args: