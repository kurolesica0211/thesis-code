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
Lord Ivar Alexander Michael Mountbatten, DL (born 9 March 1963) is a British aristocrat, farmer, geologist, businessman, and reality television personality.
Early life and family

Ivar
Alexander Michael Mountbatten was born in London, to David Mountbatten, 3rd Marquess of Milford Haven, and the former Janet Mercedes Bryce.
His elder brother is George Mountbatten, 4th Marquess of Milford Haven.
His paternal grandfather was Prince George of Battenberg, through whom he is a morganatic descendant of the House of Hesse-Darmstadt.
Mountbatten grew up at Moyns Park in Essex.
In a June 2022 interview with Tatler Mountbatten commented on the 1930s Gloria Vanderbilt child custody trial, where a maid made an allegation of a lesbian affair between the child's mother Gloria Morgan Vanderbilt and the Marchioness of Milford Haven, Mountbatten's grandmother.
Mountbatten was educated at Gordonstoun School, the same school attended by Prince Philip and Charles III, and he graduated from Middlebury College in Vermont with a BA degree.
Career

Mountbatten began his career as a geologist and spent significant time working in South America during his early career.
Starting in 1995, Mountbatten began his involvement in business pursuits, including being the director of the UK subsidiary of DMX Music and being involved with Coldharbour Mill Working Wool Museum.
Mountbatten was later involved with SCL Group, the parent company of the now-defunct data analytics firm Cambridge Analytica.
Mountbatten also serves as a Deputy Lieutenant of Devon.
In 2019, Mountbatten began a career in reality television by starring in the sixth series of Treasure Island with Bear Grylls.
In October 2024, Mountbatten was announced to be part of the third season of the American reality competition series The Traitors, which premiered on 9 January 2025.
Personal life

Mountbatten married Penelope Anne Vere Thompson (born Salisbury, Wiltshire, 17 March 1966), only daughter of Colin Graham Thompson of Old Manor House, Sutton Veny, Wiltshire, and Rosemary Vere Edwardes.
In September 2016, Mountbatten revealed that he was in a relationship with James Coyle, an airline cabin services director whom he met while at a ski resort in Verbier.
Mountbatten's former wife walked him down the aisle and 'gave him away' at the suggestion of their daughters.
Mountbatten is a godparent of Lady Louise Windsor (born 2003), the daughter of Prince Edward and Sophie.
Mountbatten inherited Moyns Park in 1992 along with his brother, George Mountbatten, 4th Marquess of Milford Haven, but in 1997 moved to Bridwell Park in Uffculme, Devon.



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix ns1: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
@prefix ns2: <http://www.w3.org/2003/11/swrl#> .
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

ns1:isRuleEnabled a owl:AnnotationProperty .

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

:x a ns2:Variable .

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

:y a ns2:Variable .

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

[] a ns2:Imp ;
    rdfs:label "infer hasSon" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasBrother" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasSister" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (08c294d6-c0e0-4a53-b9c9-474b2104cf8f)
 Call ID: 08c294d6-c0e0-4a53-b9c9-474b2104cf8f
  Args:
    source: IvarMountbatten
    type: :Man
  AssignClass (abbb6653-0c47-4710-a0dc-2410aea5282f)
 Call ID: abbb6653-0c47-4710-a0dc-2410aea5282f
  Args:
    type: :Person
    source: IvarMountbatten
  AddLiteral (2cd92bd9-d6e7-49f5-863f-a796bdc5e8c8)
 Call ID: 2cd92bd9-d6e7-49f5-863f-a796bdc5e8c8
  Args:
    literal_value: 1963
    relation: :hasBirthYear
    source: IvarMountbatten
    literal_type: xsd:integer
  AssignClass (49865694-0cb5-40e6-8d20-4d486ba2b0ac)
 Call ID: 49865694-0cb5-40e6-8d20-4d486ba2b0ac
  Args:
    type: :Man
    source: DavidMountbatten
  AssignClass (bf557745-c7a6-4c8d-aa46-f6833f42237c)
 Call ID: bf557745-c7a6-4c8d-aa46-f6833f42237c
  Args:
    type: :Person
    source: DavidMountbatten
  AssignClass (3e8af365-acce-480f-91de-c99d1518b9a2)
 Call ID: 3e8af365-acce-480f-91de-c99d1518b9a2
  Args:
    type: :Woman
    source: JanetMercedesBryce
  AssignClass (f84f4caa-d696-48a0-a19f-f123eb1d77bc)
 Call ID: f84f4caa-d696-48a0-a19f-f123eb1d77bc
  Args:
    source: JanetMercedesBryce
    type: :Person
  AddTriple (9717e30f-cb01-42bd-bdfa-dc968b421fc4)
 Call ID: 9717e30f-cb01-42bd-bdfa-dc968b421fc4
  Args:
    relation: :hasFather
    target: DavidMountbatten
    source: IvarMountbatten
  AddTriple (f408c263-6c61-4364-81d5-fabc6dfa100c)
 Call ID: f408c263-6c61-4364-81d5-fabc6dfa100c
  Args:
    source: IvarMountbatten
    relation: :hasMother
    target: JanetMercedesBryce
  AssignClass (63d82750-e9eb-4481-9c10-2be05dc4f060)
 Call ID: 63d82750-e9eb-4481-9c10-2be05dc4f060
  Args:
    type: :Man
    source: GeorgeMountbatten
  AssignClass (7f4824fe-449c-4270-a0b9-b861e5522b7d)
 Call ID: 7f4824fe-449c-4270-a0b9-b861e5522b7d
  Args:
    type: :Person
    source: GeorgeMountbatten
  AddTriple (48d37260-0a86-4813-8c9a-c93119620570)
 Call ID: 48d37260-0a86-4813-8c9a-c93119620570
  Args:
    relation: :hasBrother
    target: GeorgeMountbatten
    source: IvarMountbatten
  AssignClass (b7d37d6a-eefa-436d-b251-4ce72b207b32)
 Call ID: b7d37d6a-eefa-436d-b251-4ce72b207b32
  Args:
    type: :Woman
    source: PenelopeAnneVereThompson
  AssignClass (37bcd051-fff9-475c-9e6c-aaf699a148c3)
 Call ID: 37bcd051-fff9-475c-9e6c-aaf699a148c3
  Args:
    source: PenelopeAnneVereThompson
    type: :Person
  AddLiteral (a3b54602-a61d-45ec-b7dd-b43dae596ce4)
 Call ID: a3b54602-a61d-45ec-b7dd-b43dae596ce4
  Args:
    relation: :hasBirthYear
    literal_value: 1966
    literal_type: xsd:integer
    source: PenelopeAnneVereThompson
  AssignClass (421f5a35-0fe7-421f-8ef5-22bbbd1ba48d)
 Call ID: 421f5a35-0fe7-421f-8ef5-22bbbd1ba48d
  Args:
    source: ColinGrahamThompson
    type: :Man
  AssignClass (c3cf4ec9-12d9-4a98-b4be-aadf567bc7ee)
 Call ID: c3cf4ec9-12d9-4a98-b4be-aadf567bc7ee
  Args:
    type: :Person
    source: ColinGrahamThompson
  AssignClass (cb292eeb-c6c0-4a25-91be-0925f8da0fd0)
 Call ID: cb292eeb-c6c0-4a25-91be-0925f8da0fd0
  Args:
    type: :Woman
    source: RosemaryVereEdwardes
  AssignClass (909f3f4c-12bc-4853-82ae-33b99d93dd7c)
 Call ID: 909f3f4c-12bc-4853-82ae-33b99d93dd7c
  Args:
    source: RosemaryVereEdwardes
    type: :Person
  AddTriple (23db9aaf-1575-4d3b-85cb-ea637b532280)
 Call ID: 23db9aaf-1575-4d3b-85cb-ea637b532280
  Args:
    relation: :hasFather
    target: ColinGrahamThompson
    source: PenelopeAnneVereThompson
  AddTriple (28822390-acfe-41f1-8869-5aee530f1112)
 Call ID: 28822390-acfe-41f1-8869-5aee530f1112
  Args:
    source: PenelopeAnneVereThompson
    relation: :hasMother
    target: RosemaryVereEdwardes
  AssignClass (23337259-18d9-4424-b0a5-ce9a14cab390)
 Call ID: 23337259-18d9-4424-b0a5-ce9a14cab390
  Args:
    source: PrinceGeorgeOfBattenberg
    type: :Man
  AssignClass (14cd8147-da07-478a-8d39-9118ed025b62)
 Call ID: 14cd8147-da07-478a-8d39-9118ed025b62
  Args:
    type: :Person
    source: PrinceGeorgeOfBattenberg
  AddTriple (e2f00ccf-a61d-4bf5-882e-cafc7718d2c8)
 Call ID: e2f00ccf-a61d-4bf5-882e-cafc7718d2c8
  Args:
    source: DavidMountbatten
    relation: :hasFather
    target: PrinceGeorgeOfBattenberg
  Finish (0d9363e2-bab9-4cb5-a92a-7e0e6fbf18f7)
 Call ID: 0d9363e2-bab9-4cb5-a92a-7e0e6fbf18f7
  Args: