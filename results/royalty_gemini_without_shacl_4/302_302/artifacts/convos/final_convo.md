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
Prince Nikola of Yugoslavia (29 June 1928 – 12 April 1954), also known in Britain as Prince Nicholas and in Serbia as Nikola Karađorđević (Serbian Cyrillic: Никола Карађорђевић), was the younger son of Prince Paul of Yugoslavia by his wife Princess Olga of Greece and Denmark.
Biography

Prince Nikola was born into the House of Karađorđević, the dynasty that ruled Serbia and later the Kingdom of Yugoslavia.
Known as "Nicky", he was educated in England at Oxford University and was a frequent social escort to Princess Margaret, sister of Queen Elizabeth II.
Prince Nikola died unmarried in 1954, survived by his parents, Prince Paul and Princess Olga of Yugoslavia; older brother Prince Alexander and younger sister, Princess Elizabeth; also his maternal grandmother, Grand Duchess Elena Vladimirovna of Russia (Princess Nicholas of Greece and Denmark) and his maternal aunts, Princess Elizabeth, Countess of Toerring-Jettenbach, and Princess Marina, Duchess of Kent.
Death

Nikola died in a road accident at Datchet, now in Berkshire, England, some five miles from the home of his aunt, the Duchess of Kent.
He was
driving himself alone towards London, on his way to a meeting with Princess Margaret the same evening, to attend a full-dress rehearsal of a play being performed by a group of young socialites.
He was a paternal grandson of Arsen Karađorđević, Prince of Serbia and Princess Aurora Pavlovna Demidova di San Donato.
He was a maternal grandson of Prince Nicholas of Greece and Denmark and Grand Duchess Elena Vladimirovna of Russia.



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
  AssignClass (50dea4a6-a4c9-4d20-bfa7-3d416a83db36)
 Call ID: 50dea4a6-a4c9-4d20-bfa7-3d416a83db36
  Args:
    source: Prince_Nikola_of_Yugoslavia
    type: :Man
  AddLiteral (52a73ce9-0468-4a21-92f4-673e42e74355)
 Call ID: 52a73ce9-0468-4a21-92f4-673e42e74355
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Prince_Nikola_of_Yugoslavia
    literal_value: 1928
  AddLiteral (a60fa3a4-3deb-4fba-ab1d-967615c4c44a)
 Call ID: a60fa3a4-3deb-4fba-ab1d-967615c4c44a
  Args:
    source: Prince_Nikola_of_Yugoslavia
    literal_value: 1954
    relation: :hasDeathYear
    literal_type: xsd:integer
  AddLiteral (7a415ee2-aa90-4272-84e6-9430263ad8be)
 Call ID: 7a415ee2-aa90-4272-84e6-9430263ad8be
  Args:
    literal_value: Prince Nicholas
    source: Prince_Nikola_of_Yugoslavia
    literal_type: xsd:string
    relation: :alsoKnownAs
  AddLiteral (f2ea11b6-941e-4468-a30b-8ebc4d61bbbb)
 Call ID: f2ea11b6-941e-4468-a30b-8ebc4d61bbbb
  Args:
    literal_type: xsd:string
    relation: :alsoKnownAs
    source: Prince_Nikola_of_Yugoslavia
    literal_value: Nikola Karađorđević
  AddLiteral (a7b77206-07a6-49a0-8dd6-c95354e6e3cc)
 Call ID: a7b77206-07a6-49a0-8dd6-c95354e6e3cc
  Args:
    literal_type: xsd:string
    relation: :knownAs
    source: Prince_Nikola_of_Yugoslavia
    literal_value: Nicky
  AssignClass (3280b769-e9cb-4739-9058-941c24181652)
 Call ID: 3280b769-e9cb-4739-9058-941c24181652
  Args:
    source: Prince_Paul_of_Yugoslavia
    type: :Man
  AssignClass (26be6151-86ec-42ba-90fe-9ef8f563912c)
 Call ID: 26be6151-86ec-42ba-90fe-9ef8f563912c
  Args:
    source: Princess_Olga_of_Greece_and_Denmark
    type: :Woman
  AddTriple (20dcac4e-298c-45b4-aa69-0621e6ee0ab9)
 Call ID: 20dcac4e-298c-45b4-aa69-0621e6ee0ab9
  Args:
    relation: :hasFather
    target: Prince_Paul_of_Yugoslavia
    source: Prince_Nikola_of_Yugoslavia
  AddTriple (04fd2aad-6d17-4642-9455-63516afacfa0)
 Call ID: 04fd2aad-6d17-4642-9455-63516afacfa0
  Args:
    relation: :hasMother
    target: Princess_Olga_of_Greece_and_Denmark
    source: Prince_Nikola_of_Yugoslavia
  AssignClass (79db30af-07db-403b-8e95-9fcba11c8867)
 Call ID: 79db30af-07db-403b-8e95-9fcba11c8867
  Args:
    source: Prince_Alexander_of_Yugoslavia
    type: :Man
  AssignClass (2486e237-ba68-446e-bcba-b9ebf079e188)
 Call ID: 2486e237-ba68-446e-bcba-b9ebf079e188
  Args:
    source: Princess_Elizabeth_of_Yugoslavia
    type: :Woman
  AddTriple (605075a8-f489-4687-a1ad-910e858b6217)
 Call ID: 605075a8-f489-4687-a1ad-910e858b6217
  Args:
    target: Prince_Alexander_of_Yugoslavia
    source: Prince_Nikola_of_Yugoslavia
    relation: :hasBrother
  AddTriple (0fb60377-1046-459a-bff5-73147ac08a69)
 Call ID: 0fb60377-1046-459a-bff5-73147ac08a69
  Args:
    source: Prince_Nikola_of_Yugoslavia
    target: Princess_Elizabeth_of_Yugoslavia
    relation: :hasSister
  AssignClass (435a0e8e-3c8b-4398-a1f2-7845a6e5d9a0)
 Call ID: 435a0e8e-3c8b-4398-a1f2-7845a6e5d9a0
  Args:
    source: Grand_Duchess_Elena_Vladimirovna_of_Russia
    type: :Woman
  AddTriple (c6e84687-6eb4-49e0-8974-409b71445197)
 Call ID: c6e84687-6eb4-49e0-8974-409b71445197
  Args:
    source: Princess_Olga_of_Greece_and_Denmark
    target: Grand_Duchess_Elena_Vladimirovna_of_Russia
    relation: :hasMother
  AssignClass (64bab3bb-fcfd-4576-a8d8-e45ef3c00876)
 Call ID: 64bab3bb-fcfd-4576-a8d8-e45ef3c00876
  Args:
    source: Princess_Elizabeth_Countess_of_Toerring_Jettenbach
    type: :Woman
  AssignClass (5f05136d-ce52-4793-8ded-d274f2fe3095)
 Call ID: 5f05136d-ce52-4793-8ded-d274f2fe3095
  Args:
    type: :Woman
    source: Princess_Marina_Duchess_of_Kent
  AddTriple (6383d547-b580-40d3-8d49-11da6a7a9455)
 Call ID: 6383d547-b580-40d3-8d49-11da6a7a9455
  Args:
    relation: :hasMother
    source: Princess_Elizabeth_Countess_of_Toerring_Jettenbach
    target: Grand_Duchess_Elena_Vladimirovna_of_Russia
  AddTriple (91d1d67b-4844-44d9-92cb-30c238dd1f96)
 Call ID: 91d1d67b-4844-44d9-92cb-30c238dd1f96
  Args:
    relation: :hasMother
    source: Princess_Marina_Duchess_of_Kent
    target: Grand_Duchess_Elena_Vladimirovna_of_Russia
  AssignClass (6da933e5-57c4-4f2b-8d44-e7ebc6befcb0)
 Call ID: 6da933e5-57c4-4f2b-8d44-e7ebc6befcb0
  Args:
    type: :Man
    source: Arsen_Karađorđević_Prince_of_Serbia
  AssignClass (f7a42ad6-a916-4df0-b6c9-5e3a7a181a12)
 Call ID: f7a42ad6-a916-4df0-b6c9-5e3a7a181a12
  Args:
    type: :Woman
    source: Princess_Aurora_Pavlovna_Demidova_di_San_Donato
  AddTriple (e71baf68-9055-4242-8ec6-863c5afdc5c3)
 Call ID: e71baf68-9055-4242-8ec6-863c5afdc5c3
  Args:
    relation: :hasFather
    target: Arsen_Karađorđević_Prince_of_Serbia
    source: Prince_Paul_of_Yugoslavia
  AddTriple (8975434e-d6a1-4f9a-8a83-a1dd269ec53a)
 Call ID: 8975434e-d6a1-4f9a-8a83-a1dd269ec53a
  Args:
    source: Prince_Paul_of_Yugoslavia
    target: Princess_Aurora_Pavlovna_Demidova_di_San_Donato
    relation: :hasMother
  AssignClass (dc9d43da-972c-40de-8bc8-7a80296eb599)
 Call ID: dc9d43da-972c-40de-8bc8-7a80296eb599
  Args:
    source: Prince_Nicholas_of_Greece_and_Denmark
    type: :Man
  AddTriple (6212072b-a0d5-4f97-9579-f9eb2a4f1e6f)
 Call ID: 6212072b-a0d5-4f97-9579-f9eb2a4f1e6f
  Args:
    relation: :hasFather
    source: Princess_Olga_of_Greece_and_Denmark
    target: Prince_Nicholas_of_Greece_and_Denmark
  AddTriple (dcfb2391-9e09-4ec6-8a59-70dc439ad7e1)
 Call ID: dcfb2391-9e09-4ec6-8a59-70dc439ad7e1
  Args:
    source: Princess_Olga_of_Greece_and_Denmark
    target: Grand_Duchess_Elena_Vladimirovna_of_Russia
    relation: :hasMother
  Finish (153fb29a-0f5b-4693-8804-a34773c17ee0)
 Call ID: 153fb29a-0f5b-4693-8804-a34773c17ee0
  Args: