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
Prince Archie of Sussex (Archie Harrison Mountbatten-Windsor; born 6 May 2019) is a member of the British royal family.
He is the son of Prince Harry, Duke of Sussex, and Meghan, Duchess of Sussex.
A grandson of King Charles III, he is sixth in the line of succession to the British throne.
Birth, family and infancy

Archie Harrison Mountbatten-Windsor was born at 05:26 (BST) (04:26 UTC) on 6 May 2019 at Portland Hospital in London.
He is the first child of Prince Harry, Duke of Sussex and Meghan, Duchess of Sussex.
Archie has mixed-race ancestry, with African-American and European-American maternal lineage, and holds dual citizenship of the United Kingdom and the United States.
Archie's parents brought him to meet his great-grandparents Queen Elizabeth II and Prince Philip for the first time when he was two days old.
Four of the godparents were later reported to be Charlie van Straubenzee, Tiggy Pettifer, Mark Dyer, and the 7th Duke of Westminster.
In early 2020, Archie's parents stepped down from their roles as working members of the royal family.
Public appearances

In September and October 2019, Archie accompanied his parents on a Southern African tour to Malawi, Angola, South Africa and Botswana.
Title and styles

As heir apparent to his father's dukedom of Sussex, earldom of Dumbarton, and barony of Kilkeel, Archie was at birth and by custom entitled to use Prince Harry's senior subsidiary title, Earl of Dumbarton, as a courtesy.
However, the media reported that the Duke and Duchess decided, instead, that Archie would be styled as Master Archie Harrison Mountbatten-Windsor, in accordance with their reported wish that he grow up as a private citizen.
Upon the accession of Charles III, Archie became entitled to use the title prince and style Royal Highness, as the child of a son of the monarch, pursuant to letters patent issued by King George V in 1917.
In the interview Oprah with Meghan and Harry, the Duchess of Sussex said that she had been told that changes would be made to remove that entitlement; Charles III's plans for a scaled-down royal family dated back to the 1990s.
The official website of the royal family was updated to refer to him as "Prince Archie of Sussex" on 9 March 2023.



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
  AssignClass (0540e4e8-d809-4439-86ff-4c049400f484)
 Call ID: 0540e4e8-d809-4439-86ff-4c049400f484
  Args:
    source: Archie_Harrison_Mountbatten-Windsor
    type: :Person
  AssignClass (51536011-27f9-46a8-a087-6a95e57ad73e)
 Call ID: 51536011-27f9-46a8-a087-6a95e57ad73e
  Args:
    type: :Man
    source: Archie_Harrison_Mountbatten-Windsor
  AddLiteral (8031b1e3-4ff1-4926-ae91-dfcdb51cfa77)
 Call ID: 8031b1e3-4ff1-4926-ae91-dfcdb51cfa77
  Args:
    source: Archie_Harrison_Mountbatten-Windsor
    literal_type: xsd:string
    relation: :knownAs
    literal_value: Prince Archie of Sussex
  AssignClass (ef1ee16a-f28e-4488-acb4-e76e2abb13fc)
 Call ID: ef1ee16a-f28e-4488-acb4-e76e2abb13fc
  Args:
    source: Prince_Harry_Duke_of_Sussex
    type: :Person
  AssignClass (a9a8cd8b-54ac-422d-bd2d-94ea17d7222e)
 Call ID: a9a8cd8b-54ac-422d-bd2d-94ea17d7222e
  Args:
    source: Prince_Harry_Duke_of_Sussex
    type: :Man
  AssignClass (d3a1b9d1-6a56-4017-a240-65e478c139f4)
 Call ID: d3a1b9d1-6a56-4017-a240-65e478c139f4
  Args:
    source: Meghan_Duchess_of_Sussex
    type: :Person
  AssignClass (5244e694-c7dc-41db-a1c1-2882cbe9f8a6)
 Call ID: 5244e694-c7dc-41db-a1c1-2882cbe9f8a6
  Args:
    type: :Woman
    source: Meghan_Duchess_of_Sussex
  AddTriple (701780d9-637d-4eb5-a8c2-f2616130ebc3)
 Call ID: 701780d9-637d-4eb5-a8c2-f2616130ebc3
  Args:
    relation: :hasFather
    source: Archie_Harrison_Mountbatten-Windsor
    target: Prince_Harry_Duke_of_Sussex
  AddTriple (9a3f153e-99d8-4a0c-8567-f95a1176ecf6)
 Call ID: 9a3f153e-99d8-4a0c-8567-f95a1176ecf6
  Args:
    target: Meghan_Duchess_of_Sussex
    relation: :hasMother
    source: Archie_Harrison_Mountbatten-Windsor
  AssignClass (29c1b2ef-abf6-4bb8-b88f-7c4db50cb3bd)
 Call ID: 29c1b2ef-abf6-4bb8-b88f-7c4db50cb3bd
  Args:
    type: :Person
    source: King_Charles_III
  AssignClass (5bbf1b85-457a-46e5-b7bd-50afa580b5cc)
 Call ID: 5bbf1b85-457a-46e5-b7bd-50afa580b5cc
  Args:
    type: :Man
    source: King_Charles_III
  AddTriple (348801dc-4b74-4663-9ca3-34b1d1c6f30d)
 Call ID: 348801dc-4b74-4663-9ca3-34b1d1c6f30d
  Args:
    target: King_Charles_III
    source: Prince_Harry_Duke_of_Sussex
    relation: :hasFather
  AddTriple (6d69649e-6381-4a0a-8340-d6e23c957f91)
 Call ID: 6d69649e-6381-4a0a-8340-d6e23c957f91
  Args:
    relation: :hasFather
    source: King_Charles_III
    target: Archie_Harrison_Mountbatten-Windsor
  RemoveTriple (c2f9b0ed-1b3c-4486-854d-52e188b43ec9)
 Call ID: c2f9b0ed-1b3c-4486-854d-52e188b43ec9
  Args:
    relation: :hasFather
    source: King_Charles_III
    target: Archie_Harrison_Mountbatten-Windsor
  AddTriple (11a16148-f379-4307-8497-434b264f4b1a)
 Call ID: 11a16148-f379-4307-8497-434b264f4b1a
  Args:
    target: King_Charles_III
    source: Archie_Harrison_Mountbatten-Windsor
    relation: :hasAncestor
  AssignClass (772f8177-49db-481b-8ed1-026643dbf710)
 Call ID: 772f8177-49db-481b-8ed1-026643dbf710
  Args:
    source: Queen_Elizabeth_II
    type: :Person
  AssignClass (3fdd7680-8d6e-4e9c-b649-d944fba5e384)
 Call ID: 3fdd7680-8d6e-4e9c-b649-d944fba5e384
  Args:
    source: Queen_Elizabeth_II
    type: :Woman
  AssignClass (f31fcb26-93b8-409d-88ad-5d2a3eb31f9f)
 Call ID: f31fcb26-93b8-409d-88ad-5d2a3eb31f9f
  Args:
    source: Prince_Philip
    type: :Person
  AssignClass (b5ab4472-3ce8-47d4-b1fb-e65293eb9de5)
 Call ID: b5ab4472-3ce8-47d4-b1fb-e65293eb9de5
  Args:
    source: Prince_Philip
    type: :Man
  AddTriple (39b38b2b-6f83-4247-a318-887c6c3e3770)
 Call ID: 39b38b2b-6f83-4247-a318-887c6c3e3770
  Args:
    relation: :hasAncestor
    source: Archie_Harrison_Mountbatten-Windsor
    target: Queen_Elizabeth_II
  AddTriple (c87d32bb-e15e-4d61-a01e-29a26ae29e99)
 Call ID: c87d32bb-e15e-4d61-a01e-29a26ae29e99
  Args:
    target: Prince_Philip
    relation: :hasAncestor
    source: Archie_Harrison_Mountbatten-Windsor
  Finish (8df7e7e7-cb52-41a4-8f1f-a9ecbe81f945)
 Call ID: 8df7e7e7-cb52-41a4-8f1f-a9ecbe81f945
  Args: