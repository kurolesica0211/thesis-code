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
  AssignClass (d0dee4a0-7da5-4690-b0b1-824d9fd52790)
 Call ID: d0dee4a0-7da5-4690-b0b1-824d9fd52790
  Args:
    type: :Person
    source: :Olga_of_Greece
  AssignClass (6466e6ef-44f6-491d-b77f-9ffa23656bed)
 Call ID: 6466e6ef-44f6-491d-b77f-9ffa23656bed
  Args:
    type: :Woman
    source: :Olga_of_Greece
  AddLiteral (0c7b07be-b912-417e-a431-f5897646aca7)
 Call ID: 0c7b07be-b912-417e-a431-f5897646aca7
  Args:
    relation: :hasBirthYear
    source: :Olga_of_Greece
    literal_value: 1971
    literal_type: xsd:integer
  AssignClass (425eb880-902a-4e17-a5f2-c1dcc5e32fb5)
 Call ID: 425eb880-902a-4e17-a5f2-c1dcc5e32fb5
  Args:
    type: :Person
    source: :Prince_Michael_of_Greece_and_Denmark
  AssignClass (3ed63505-effe-46de-8ce4-e7b49a54724f)
 Call ID: 3ed63505-effe-46de-8ce4-e7b49a54724f
  Args:
    type: :Man
    source: :Prince_Michael_of_Greece_and_Denmark
  AddTriple (5a5efbad-2d24-4b36-befd-d3a221582d47)
 Call ID: 5a5efbad-2d24-4b36-befd-d3a221582d47
  Args:
    relation: :hasFather
    target: :Prince_Michael_of_Greece_and_Denmark
    source: :Olga_of_Greece
  AssignClass (f596f2bb-70d9-45c4-bd4b-752b1ba8c6da)
 Call ID: f596f2bb-70d9-45c4-bd4b-752b1ba8c6da
  Args:
    type: :Person
    source: :Marina_Karella
  AssignClass (b604f656-8a1d-440a-863d-f7036360cdf3)
 Call ID: b604f656-8a1d-440a-863d-f7036360cdf3
  Args:
    type: :Woman
    source: :Marina_Karella
  AddTriple (66324a3a-05ca-457f-beeb-375ba35f2cf1)
 Call ID: 66324a3a-05ca-457f-beeb-375ba35f2cf1
  Args:
    target: :Marina_Karella
    relation: :hasMother
    source: :Olga_of_Greece
  AssignClass (804e8f96-a2e4-4ba1-9e23-a9f69fecb69a)
 Call ID: 804e8f96-a2e4-4ba1-9e23-a9f69fecb69a
  Args:
    type: :Person
    source: :Theodoros_Karellas
  AssignClass (045971f5-d537-40e8-b0a1-a5b686207f0c)
 Call ID: 045971f5-d537-40e8-b0a1-a5b686207f0c
  Args:
    type: :Man
    source: :Theodoros_Karellas
  AddTriple (aa05bc5d-96a3-43b2-85b7-556281f20112)
 Call ID: aa05bc5d-96a3-43b2-85b7-556281f20112
  Args:
    source: :Marina_Karella
    target: :Theodoros_Karellas
    relation: :hasFather
  AssignClass (83b57942-3166-4d0f-9615-7a1be1a9a501)
 Call ID: 83b57942-3166-4d0f-9615-7a1be1a9a501
  Args:
    type: :Person
    source: :Prince_Aimone_Duke_of_Aosta
  AssignClass (c05184a2-485f-4ad4-99eb-4537e8ab7b4f)
 Call ID: c05184a2-485f-4ad4-99eb-4537e8ab7b4f
  Args:
    type: :Man
    source: :Prince_Aimone_Duke_of_Aosta
  AddTriple (627f7b1e-5ddb-49a8-8bec-f712f9671fc4)
 Call ID: 627f7b1e-5ddb-49a8-8bec-f712f9671fc4
  Args:
    source: :Olga_of_Greece
    relation: :hasRelation
    target: :Prince_Aimone_Duke_of_Aosta
  AssignClass (535f3d65-931f-424d-865f-e663080498d4)
 Call ID: 535f3d65-931f-424d-865f-e663080498d4
  Args:
    type: :Person
    source: :Alexandra_of_Greece
  AssignClass (a4ff6df0-3970-4ab0-bf45-c5158e0483da)
 Call ID: a4ff6df0-3970-4ab0-bf45-c5158e0483da
  Args:
    type: :Woman
    source: :Alexandra_of_Greece
  AddTriple (53c10f2f-de20-4651-b84b-5c27db6aa511)
 Call ID: 53c10f2f-de20-4651-b84b-5c27db6aa511
  Args:
    target: :Alexandra_of_Greece
    relation: :hasSister
    source: :Olga_of_Greece
  AssignClass (19728e7f-eb68-410f-b127-894a29b0e421)
 Call ID: 19728e7f-eb68-410f-b127-894a29b0e421
  Args:
    type: :Person
    source: :Amedeo_5th_Duke_of_Aosta
  AssignClass (4a84784b-cec2-4e4b-a099-67a32d4c9d73)
 Call ID: 4a84784b-cec2-4e4b-a099-67a32d4c9d73
  Args:
    type: :Man
    source: :Amedeo_5th_Duke_of_Aosta
  AddTriple (aee99c50-b185-4f1b-9113-fd1f45564fe1)
 Call ID: aee99c50-b185-4f1b-9113-fd1f45564fe1
  Args:
    relation: :hasFather
    target: :Amedeo_5th_Duke_of_Aosta
    source: :Prince_Aimone_Duke_of_Aosta
  AssignClass (fe8a7174-8837-4e93-9ccf-57d0107d94f5)
 Call ID: fe8a7174-8837-4e93-9ccf-57d0107d94f5
  Args:
    type: :Person
    source: :Umberto_of_Savoy_Aosta
  AssignClass (eac9b12e-3b47-497c-a6f9-77cb92c45be6)
 Call ID: eac9b12e-3b47-497c-a6f9-77cb92c45be6
  Args:
    type: :Man
    source: :Umberto_of_Savoy_Aosta
  AddTriple (91a2ee84-71aa-4a31-99ce-fd7ceb760008)
 Call ID: 91a2ee84-71aa-4a31-99ce-fd7ceb760008
  Args:
    target: :Prince_Aimone_Duke_of_Aosta
    relation: :hasFather
    source: :Umberto_of_Savoy_Aosta
  AddTriple (66435e5d-3896-4439-a4b2-81ce242cfa30)
 Call ID: 66435e5d-3896-4439-a4b2-81ce242cfa30
  Args:
    source: :Umberto_of_Savoy_Aosta
    target: :Olga_of_Greece
    relation: :hasMother
  AssignClass (4f0209d3-89d1-4470-9ddb-b7a2f91319b6)
 Call ID: 4f0209d3-89d1-4470-9ddb-b7a2f91319b6
  Args:
    type: :Person
    source: :Amedeo_Michele_of_Savoy_Aosta
  AssignClass (2f846596-7ab2-4a43-b468-22d53678bb77)
 Call ID: 2f846596-7ab2-4a43-b468-22d53678bb77
  Args:
    type: :Man
    source: :Amedeo_Michele_of_Savoy_Aosta
  AddTriple (8a177a0b-2fee-4158-a07c-2bda07d4fce6)
 Call ID: 8a177a0b-2fee-4158-a07c-2bda07d4fce6
  Args:
    source: :Amedeo_Michele_of_Savoy_Aosta
    relation: :hasFather
    target: :Prince_Aimone_Duke_of_Aosta
  AddTriple (6a3df959-f1f1-4d7d-842d-1cd2763e76ae)
 Call ID: 6a3df959-f1f1-4d7d-842d-1cd2763e76ae
  Args:
    source: :Amedeo_Michele_of_Savoy_Aosta
    relation: :hasMother
    target: :Olga_of_Greece
  AssignClass (94bdf5b9-4be7-4c2f-a480-496c66b3c067)
 Call ID: 94bdf5b9-4be7-4c2f-a480-496c66b3c067
  Args:
    type: :Person
    source: :Isabella_Vita_Marina_of_Savoy_Aosta
  AssignClass (c3a930c3-b791-47af-a0b9-1a9055b18326)
 Call ID: c3a930c3-b791-47af-a0b9-1a9055b18326
  Args:
    type: :Woman
    source: :Isabella_Vita_Marina_of_Savoy_Aosta
  AddTriple (495ef108-1e51-485a-8251-8ba70e0c31b8)
 Call ID: 495ef108-1e51-485a-8251-8ba70e0c31b8
  Args:
    source: :Isabella_Vita_Marina_of_Savoy_Aosta
    target: :Prince_Aimone_Duke_of_Aosta
    relation: :hasFather
  AddTriple (076e14b9-1415-4d52-9425-73efe1d29955)
 Call ID: 076e14b9-1415-4d52-9425-73efe1d29955
  Args:
    relation: :hasMother
    target: :Olga_of_Greece
    source: :Isabella_Vita_Marina_of_Savoy_Aosta
  Finish (28ab82bd-fbd6-4af5-9a20-dedb65cf7bfe)
 Call ID: 28ab82bd-fbd6-4af5-9a20-dedb65cf7bfe
  Args: