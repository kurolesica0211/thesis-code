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
  AssignClass (c6edca6d-0423-40c8-a25a-9e14b9936083)
 Call ID: c6edca6d-0423-40c8-a25a-9e14b9936083
  Args:
    type: :Woman
    source: Princess_Olga_of_Greece
  AssignClass (74bbe95f-5b4a-4d05-8741-f9ffb2275d6f)
 Call ID: 74bbe95f-5b4a-4d05-8741-f9ffb2275d6f
  Args:
    type: :Person
    source: Princess_Olga_of_Greece
  AssignClass (a1ede3a4-7d13-4aee-8858-d1cdb2a2e6da)
 Call ID: a1ede3a4-7d13-4aee-8858-d1cdb2a2e6da
  Args:
    type: :Man
    source: Prince_Michael_of_Greece_and_Denmark
  AssignClass (291bc793-6d9c-45dc-928c-ad62f774f132)
 Call ID: 291bc793-6d9c-45dc-928c-ad62f774f132
  Args:
    type: :Person
    source: Prince_Michael_of_Greece_and_Denmark
  AssignClass (c2ae439d-2822-42fa-9ac4-1701eebb76c6)
 Call ID: c2ae439d-2822-42fa-9ac4-1701eebb76c6
  Args:
    type: :Woman
    source: Marina_Karella
  AssignClass (0e36c938-882f-419f-a68f-0dce4c36f79c)
 Call ID: 0e36c938-882f-419f-a68f-0dce4c36f79c
  Args:
    source: Marina_Karella
    type: :Person
  AddTriple (86fe6fcf-cd7c-4325-aa21-186f51abfb05)
 Call ID: 86fe6fcf-cd7c-4325-aa21-186f51abfb05
  Args:
    target: Prince_Michael_of_Greece_and_Denmark
    relation: :hasFather
    source: Princess_Olga_of_Greece
  AddTriple (693578e0-1d2a-42ee-9caa-121af4643298)
 Call ID: 693578e0-1d2a-42ee-9caa-121af4643298
  Args:
    target: Marina_Karella
    relation: :hasMother
    source: Princess_Olga_of_Greece
  AddLiteral (06df7c3e-fd3c-4bf7-b71c-fea821a40ef1)
 Call ID: 06df7c3e-fd3c-4bf7-b71c-fea821a40ef1
  Args:
    relation: :hasBirthYear
    literal_value: 1971
    source: Princess_Olga_of_Greece
    literal_type: xsd:integer
  AssignClass (212ad2ee-c320-403f-a172-c857525a7a5f)
 Call ID: 212ad2ee-c320-403f-a172-c857525a7a5f
  Args:
    type: :Man
    source: Prince_Aimone_Duke_of_Aosta
  AssignClass (8b9a2f63-7e07-4b74-af7f-187cbcf83bd2)
 Call ID: 8b9a2f63-7e07-4b74-af7f-187cbcf83bd2
  Args:
    source: Prince_Aimone_Duke_of_Aosta
    type: :Person
  AddTriple (2cc36840-b0ca-4b3d-9302-34cf36efdf3e)
 Call ID: 2cc36840-b0ca-4b3d-9302-34cf36efdf3e
  Args:
    target: Prince_Aimone_Duke_of_Aosta
    relation: :hasRelation
    source: Princess_Olga_of_Greece
  AssignClass (4e4b19b8-6128-4bc6-ac56-243758f2de62)
 Call ID: 4e4b19b8-6128-4bc6-ac56-243758f2de62
  Args:
    source: Princess_Alexandra
    type: :Woman
  AssignClass (7fb3f32f-a2ec-490b-8bfe-e109d8aabe60)
 Call ID: 7fb3f32f-a2ec-490b-8bfe-e109d8aabe60
  Args:
    source: Princess_Alexandra
    type: :Person
  AddTriple (f880f62e-8493-4806-a8ba-d53f8d4e2796)
 Call ID: f880f62e-8493-4806-a8ba-d53f8d4e2796
  Args:
    target: Princess_Alexandra
    source: Princess_Olga_of_Greece
    relation: :hasSister
  AddTriple (95779da0-38ad-42c5-931e-671c63403ae4)
 Call ID: 95779da0-38ad-42c5-931e-671c63403ae4
  Args:
    target: Prince_Michael_of_Greece_and_Denmark
    source: Princess_Alexandra
    relation: :hasFather
  AddTriple (45e546a9-3946-4140-b1b5-9d0df5dc2547)
 Call ID: 45e546a9-3946-4140-b1b5-9d0df5dc2547
  Args:
    target: Marina_Karella
    source: Princess_Alexandra
    relation: :hasMother
  AssignClass (a23a91a5-db05-4218-8952-82816cad494a)
 Call ID: a23a91a5-db05-4218-8952-82816cad494a
  Args:
    source: Theodoros_Karellas
    type: :Man
  AssignClass (2f680be1-8650-43ca-894f-7b4492dd2911)
 Call ID: 2f680be1-8650-43ca-894f-7b4492dd2911
  Args:
    type: :Person
    source: Theodoros_Karellas
  AddTriple (7f5f7a70-a61a-41cd-aada-a79934e8dd73)
 Call ID: 7f5f7a70-a61a-41cd-aada-a79934e8dd73
  Args:
    target: Theodoros_Karellas
    source: Marina_Karella
    relation: :hasFather
  AssignClass (b4afb72a-573c-430c-877a-a9fef73f8a0e)
 Call ID: b4afb72a-573c-430c-877a-a9fef73f8a0e
  Args:
    source: Umberto_of_Savoy_Aosta
    type: :Man
  AssignClass (15181aeb-0b29-4707-91a6-fc9efbcd4236)
 Call ID: 15181aeb-0b29-4707-91a6-fc9efbcd4236
  Args:
    type: :Person
    source: Umberto_of_Savoy_Aosta
  AddTriple (9c23accf-afeb-48fc-9b3b-fe3ca595e582)
 Call ID: 9c23accf-afeb-48fc-9b3b-fe3ca595e582
  Args:
    relation: :hasFather
    source: Umberto_of_Savoy_Aosta
    target: Prince_Aimone_Duke_of_Aosta
  AddTriple (6f80a26a-1560-4d75-87ed-d362c4d891e6)
 Call ID: 6f80a26a-1560-4d75-87ed-d362c4d891e6
  Args:
    target: Princess_Olga_of_Greece
    source: Umberto_of_Savoy_Aosta
    relation: :hasMother
  AssignClass (8db48d3e-c926-4788-a89d-c067b469a316)
 Call ID: 8db48d3e-c926-4788-a89d-c067b469a316
  Args:
    type: :Man
    source: Amedeo_Michele_of_Savoy_Aosta
  AssignClass (d8fdb8dc-e73c-4ace-adc9-036bc6ddc172)
 Call ID: d8fdb8dc-e73c-4ace-adc9-036bc6ddc172
  Args:
    type: :Person
    source: Amedeo_Michele_of_Savoy_Aosta
  AddTriple (92797c70-37d6-4cad-ad21-e4611e8145e1)
 Call ID: 92797c70-37d6-4cad-ad21-e4611e8145e1
  Args:
    relation: :hasFather
    source: Amedeo_Michele_of_Savoy_Aosta
    target: Prince_Aimone_Duke_of_Aosta
  AddTriple (941e2836-8827-4011-b0d8-8ec8cd029626)
 Call ID: 941e2836-8827-4011-b0d8-8ec8cd029626
  Args:
    target: Princess_Olga_of_Greece
    relation: :hasMother
    source: Amedeo_Michele_of_Savoy_Aosta
  AssignClass (be5492ad-31c3-41e0-a559-dbe23541c6db)
 Call ID: be5492ad-31c3-41e0-a559-dbe23541c6db
  Args:
    type: :Woman
    source: Isabella_Vita_Marina_of_Savoy_Aosta
  AssignClass (5e4314fa-fc54-4940-aa3e-bdb235532186)
 Call ID: 5e4314fa-fc54-4940-aa3e-bdb235532186
  Args:
    source: Isabella_Vita_Marina_of_Savoy_Aosta
    type: :Person
  AddTriple (6d373105-8309-442e-a8f0-2c4887e9a6e2)
 Call ID: 6d373105-8309-442e-a8f0-2c4887e9a6e2
  Args:
    target: Prince_Aimone_Duke_of_Aosta
    relation: :hasFather
    source: Isabella_Vita_Marina_of_Savoy_Aosta
  AddTriple (bcc12079-c467-43f4-bd7f-c989a0bd64f4)
 Call ID: bcc12079-c467-43f4-bd7f-c989a0bd64f4
  Args:
    relation: :hasMother
    source: Isabella_Vita_Marina_of_Savoy_Aosta
    target: Princess_Olga_of_Greece
  AssignClass (09afad08-cbc1-4373-b4bf-178c2faf5527)
 Call ID: 09afad08-cbc1-4373-b4bf-178c2faf5527
  Args:
    type: :Man
    source: Amedeo_5th_Duke_of_Aosta
  AssignClass (5bb01d48-8612-47f8-bcd1-07c8020213f0)
 Call ID: 5bb01d48-8612-47f8-bcd1-07c8020213f0
  Args:
    source: Amedeo_5th_Duke_of_Aosta
    type: :Person
  AddTriple (7ad769ef-e0e7-4f0c-b50a-f730ac049273)
 Call ID: 7ad769ef-e0e7-4f0c-b50a-f730ac049273
  Args:
    relation: :hasFather
    source: Prince_Aimone_Duke_of_Aosta
    target: Amedeo_5th_Duke_of_Aosta
  AssignClass (a52bcab6-0135-4062-b255-6fce6bfac448)
 Call ID: a52bcab6-0135-4062-b255-6fce6bfac448
  Args:
    type: :Woman
    source: Princess_Irene_Duchess_of_Aosta
  AssignClass (aac548b1-d1d9-4a15-9401-3e28669b18cd)
 Call ID: aac548b1-d1d9-4a15-9401-3e28669b18cd
  Args:
    type: :Person
    source: Princess_Irene_Duchess_of_Aosta
  AddTriple (f8f56ae9-0768-43a3-9745-e2d1ec827384)
 Call ID: f8f56ae9-0768-43a3-9745-e2d1ec827384
  Args:
    target: Princess_Irene_Duchess_of_Aosta
    relation: :hasMother
    source: Prince_Aimone_Duke_of_Aosta
  Finish (345208bb-68ef-484b-b8d7-fdfee081a7b2)
 Call ID: 345208bb-68ef-484b-b8d7-fdfee081a7b2
  Args: