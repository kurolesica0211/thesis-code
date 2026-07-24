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
Princess Beatrix*


Princess Margriet*Pieter van Vollenhoven*


Countess Leonore of Orange-Nassau, Jonkvrouwe van Amsberg (Leonore Marie Irene Enrica; born 3 June 2006), is a member of the Dutch royal family.
She is the third child and second daughter of Prince Constantijn of the Netherlands and Princess Laurentien of the Netherlands.
Life and education

Countess Leonore was born on 3 June 2006 at HMC Bronovo in The Hague, Netherlands, as the third child and second daughter of Prince Constantijn and Princess Laurentien.
She was baptised on 8 October 2006 in the chapel of Het Loo Palace in Apeldoorn; her godparents included her paternal aunt, Queen Máxima; her maternal uncle, Marius Brinkhorst; her father’s first cousin, Juliana Guillermo; and Count Jean‐Charles Ullens de Schooten Whettnall.
After spending the early years of her life partly in Belgium where her family lived while her parents worked, Countess Leonore later relocated with her family to the Netherlands in 2015.
Since September 2022, she has been studying at UWC Atlantic College in Wales, a United World College known for its international education programme, the same school attended by her cousin, Princess Alexia.
Titles and styles

By royal decree of 11 May 2001 (nr. 227), it was determined that the children born from the marriage of Prince Constantijn and Princess Laurentien of the Netherlands would bear the title Count/Countess of Orange‐Nassau and the honorific Jonkheer/Jonkvrouwe van Amsberg with the surname Van Oranje-Nassau van Amsberg.
Upon the abdication of Queen Beatrix on 30 April 2013, the children of Prince Constantijn and Princess Laurentien ceased to be members of the Royal House, although continue to be members of the royal family.



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
  AssignClass (87ea3a80-2379-4468-b286-0b5e7c5f2268)
 Call ID: 87ea3a80-2379-4468-b286-0b5e7c5f2268
  Args:
    type: :Person
    source: :Princess_Beatrix
  AssignClass (0d0041db-8571-4c81-8101-315c856e0e7a)
 Call ID: 0d0041db-8571-4c81-8101-315c856e0e7a
  Args:
    type: :Woman
    source: :Princess_Beatrix
  AssignClass (2653cee1-3cce-45c7-a7b5-cf1c489c030b)
 Call ID: 2653cee1-3cce-45c7-a7b5-cf1c489c030b
  Args:
    type: :Person
    source: :Princess_Margriet
  AssignClass (806952a9-3e0d-4f47-b3f1-75f315eae70a)
 Call ID: 806952a9-3e0d-4f47-b3f1-75f315eae70a
  Args:
    type: :Woman
    source: :Princess_Margriet
  AssignClass (d29762c9-0972-46ea-b7d0-c30b1b4b803c)
 Call ID: d29762c9-0972-46ea-b7d0-c30b1b4b803c
  Args:
    type: :Person
    source: :Pieter_van_Vollenhoven
  AssignClass (056a1f83-dfd8-4021-b435-84113ca0cbf8)
 Call ID: 056a1f83-dfd8-4021-b435-84113ca0cbf8
  Args:
    type: :Man
    source: :Pieter_van_Vollenhoven
  AssignClass (92793b58-992f-4d97-a173-14cb394a449f)
 Call ID: 92793b58-992f-4d97-a173-14cb394a449f
  Args:
    type: :Person
    source: :Countess_Leonore
  AssignClass (06fd6d35-267b-4aca-a32e-8a8fe27b7efb)
 Call ID: 06fd6d35-267b-4aca-a32e-8a8fe27b7efb
  Args:
    type: :Woman
    source: :Countess_Leonore
  AddLiteral (96a280c0-44a8-418b-ab33-a75dd8021db4)
 Call ID: 96a280c0-44a8-418b-ab33-a75dd8021db4
  Args:
    relation: :hasBirthYear
    source: :Countess_Leonore
    literal_value: 2006
    literal_type: xsd:integer
  AssignClass (51f21ce7-39eb-4168-840a-deeaa8a82895)
 Call ID: 51f21ce7-39eb-4168-840a-deeaa8a82895
  Args:
    type: :Person
    source: :Prince_Constantijn
  AssignClass (5ddbf5f1-91cd-419d-a813-767350a129ad)
 Call ID: 5ddbf5f1-91cd-419d-a813-767350a129ad
  Args:
    type: :Man
    source: :Prince_Constantijn
  AssignClass (4b968908-e0b7-42e3-a338-96c5ca8fe456)
 Call ID: 4b968908-e0b7-42e3-a338-96c5ca8fe456
  Args:
    type: :Person
    source: :Princess_Laurentien
  AssignClass (8a223d73-c6d2-46fd-bc93-eaed035fee9c)
 Call ID: 8a223d73-c6d2-46fd-bc93-eaed035fee9c
  Args:
    type: :Woman
    source: :Princess_Laurentien
  AddTriple (28eea2a9-23b6-41ca-8df9-52a434842ea4)
 Call ID: 28eea2a9-23b6-41ca-8df9-52a434842ea4
  Args:
    source: :Countess_Leonore
    target: :Prince_Constantijn
    relation: :hasFather
  AddTriple (93db764e-fdc2-40f6-9f8d-c6c9bc47e3cf)
 Call ID: 93db764e-fdc2-40f6-9f8d-c6c9bc47e3cf
  Args:
    target: :Princess_Laurentien
    source: :Countess_Leonore
    relation: :hasMother
  AssignClass (b35284b3-d7f9-4343-ad3b-9e16891f9cc4)
 Call ID: b35284b3-d7f9-4343-ad3b-9e16891f9cc4
  Args:
    type: :Person
    source: :Queen_Maxima
  AssignClass (89a7f9a1-6d6e-4baa-bb15-38cff214bfc2)
 Call ID: 89a7f9a1-6d6e-4baa-bb15-38cff214bfc2
  Args:
    type: :Woman
    source: :Queen_Maxima
  AssignClass (fad88bfd-271b-4a12-bf3b-c3f6e6a17550)
 Call ID: fad88bfd-271b-4a12-bf3b-c3f6e6a17550
  Args:
    type: :Person
    source: :Marius_Brinkhorst
  AssignClass (be1432a3-1cda-44b1-9d7a-a623f99402f2)
 Call ID: be1432a3-1cda-44b1-9d7a-a623f99402f2
  Args:
    type: :Man
    source: :Marius_Brinkhorst
  AssignClass (d54ec4bc-7af3-4a49-a82f-b0c59f174cc4)
 Call ID: d54ec4bc-7af3-4a49-a82f-b0c59f174cc4
  Args:
    type: :Person
    source: :Juliana_Guillermo
  AssignClass (5931a01c-8a12-4c7f-a5b0-e52dcd2b69d4)
 Call ID: 5931a01c-8a12-4c7f-a5b0-e52dcd2b69d4
  Args:
    type: :Woman
    source: :Juliana_Guillermo
  AssignClass (bc4ca504-14e7-4b6b-b973-3c755b8bc0e6)
 Call ID: bc4ca504-14e7-4b6b-b973-3c755b8bc0e6
  Args:
    type: :Person
    source: :Count_Jean_Charles_Ullens_de_Schooten_Whettnall
  AssignClass (8e88487e-fc2c-44bb-98a7-b2815b96ff55)
 Call ID: 8e88487e-fc2c-44bb-98a7-b2815b96ff55
  Args:
    type: :Man
    source: :Count_Jean_Charles_Ullens_de_Schooten_Whettnall
  AssignClass (e2e1187d-0bfc-44d1-9bad-8c543e65c063)
 Call ID: e2e1187d-0bfc-44d1-9bad-8c543e65c063
  Args:
    type: :Person
    source: :Princess_Alexia
  AssignClass (a8962b70-9928-4ddb-92cc-908e62604b27)
 Call ID: a8962b70-9928-4ddb-92cc-908e62604b27
  Args:
    type: :Woman
    source: :Princess_Alexia
  Finish (54aa3822-ba0b-47e2-8e98-bff1238196a0)
 Call ID: 54aa3822-ba0b-47e2-8e98-bff1238196a0
  Args: