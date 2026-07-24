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
Lady Amanda Patricia Victoria Ellingworth (née Knatchbull; born 26 June 1957), styled The Honourable Amanda Knatchbull between 1957 and 1979, is a British voluntary sector executive.
The granddaughter of Admiral of the Fleet Louis Mountbatten, 1st Earl Mountbatten of Burma, she is a descendant of Queen Victoria through her daughter Princess Alice, Mountbatten's grandmother.
Ancestry

Early life and education

Born as The Honourable Amanda Patricia Victoria Knatchbull, on 26 June 1957, in London, she was the fifth of eight children of the 7th Baron Brabourne and the 2nd Countess Mountbatten of Burma.
Earl Mountbatten of Burma, who was an uncle of Prince Philip, Duke of Edinburgh and a second cousin once removed of Queen Elizabeth II.
Ellingworth earned a BA Hons degree from the University of Kent, a CQSW qualification from Goldsmiths College, London, and a Certificate in Mandarin Language from the Beijing Language Institute.
, Ellingworth worked at a senior level in health services, children's services, adult social care and affordable housing.
Personal life

Marriage and family

Lady Amanda married novelist and property entrepreneur Charles Vincent Ellingworth on 31 October 1987.
Relationship with Prince of Wales

Ellingworth's grandfather Lord Mountbatten recommended her as a potential bride for his grandnephew, Charles, Prince of Wales.
According to his biographer, Jonathan Dimbleby, "In 1974, following his correspondence with Mountbatten on the subject, the Prince had tentatively raised the question of marriage to Amanda with her mother (and his godmother)
"


Mountbatten intended for himself and Lady Amanda to accompany Prince Charles on his planned 1980 tour of India.
Before Prince Charles was to depart, Mountbatten was assassinated by the IRA in August 1979.
When Prince Charles returned, he proposed to Lady Amanda.



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
  AssignClass (e358e6d9-be5c-441f-80cb-e56ab9c5466b)
 Call ID: e358e6d9-be5c-441f-80cb-e56ab9c5466b
  Args:
    source: Amanda_Ellingworth
    type: :Woman
  AssignClass (3a5633cb-715b-4f49-aee5-879ea04aac68)
 Call ID: 3a5633cb-715b-4f49-aee5-879ea04aac68
  Args:
    source: Amanda_Ellingworth
    type: :Person
  AddLiteral (c8f63cd7-0d04-4899-b249-65058a059560)
 Call ID: c8f63cd7-0d04-4899-b249-65058a059560
  Args:
    source: Amanda_Ellingworth
    relation: :knownAs
    literal_type: xsd:string
    literal_value: Lady Amanda Patricia Victoria Ellingworth
  AddLiteral (d605ccb8-8717-4180-a538-746a6ebbff74)
 Call ID: d605ccb8-8717-4180-a538-746a6ebbff74
  Args:
    relation: :formerlyKnownAs
    literal_type: xsd:string
    literal_value: The Honourable Amanda Knatchbull
    source: Amanda_Ellingworth
  AddLiteral (e90162a0-1601-4056-9a91-f8e01ca88f5e)
 Call ID: e90162a0-1601-4056-9a91-f8e01ca88f5e
  Args:
    source: Amanda_Ellingworth
    literal_value: 1957
    relation: :hasBirthYear
    literal_type: xsd:integer
  AssignClass (700c811d-7800-4095-a4c2-ad229fb2b5ef)
 Call ID: 700c811d-7800-4095-a4c2-ad229fb2b5ef
  Args:
    type: :Man
    source: Louis_Mountbatten
  AssignClass (9f60e2ff-be33-4d9b-ac96-45233aee5cfb)
 Call ID: 9f60e2ff-be33-4d9b-ac96-45233aee5cfb
  Args:
    type: :Person
    source: Louis_Mountbatten
  AddTriple (5dcb0148-721a-4d2b-ade6-d6dd6a1ef74e)
 Call ID: 5dcb0148-721a-4d2b-ade6-d6dd6a1ef74e
  Args:
    relation: :isAncestorOf
    target: Amanda_Ellingworth
    source: Louis_Mountbatten
  AssignClass (38ff7af9-73d8-467d-9827-141af8dd8ab2)
 Call ID: 38ff7af9-73d8-467d-9827-141af8dd8ab2
  Args:
    source: Baron_Brabourne_7th
    type: :Man
  AssignClass (8b866521-dcd8-4083-9f2d-f2b68447e3c2)
 Call ID: 8b866521-dcd8-4083-9f2d-f2b68447e3c2
  Args:
    source: Baron_Brabourne_7th
    type: :Person
  AssignClass (5ac67cba-35a1-4793-bdac-c8e626626e5c)
 Call ID: 5ac67cba-35a1-4793-bdac-c8e626626e5c
  Args:
    source: Countess_Mountbatten_2nd
    type: :Woman
  AssignClass (d3b93cdc-e7de-4d45-9ba9-37e2e640fc51)
 Call ID: d3b93cdc-e7de-4d45-9ba9-37e2e640fc51
  Args:
    source: Countess_Mountbatten_2nd
    type: :Person
  AddTriple (b15d2d04-862a-473c-acaf-3cd4529f78de)
 Call ID: b15d2d04-862a-473c-acaf-3cd4529f78de
  Args:
    source: Amanda_Ellingworth
    target: Baron_Brabourne_7th
    relation: :hasFather
  AddTriple (56952898-a18a-421d-be9b-f2140a6b4304)
 Call ID: 56952898-a18a-421d-be9b-f2140a6b4304
  Args:
    source: Amanda_Ellingworth
    target: Countess_Mountbatten_2nd
    relation: :hasMother
  AssignClass (aa79e734-4576-4242-8add-824162fcad4f)
 Call ID: aa79e734-4576-4242-8add-824162fcad4f
  Args:
    source: Charles_Vincent_Ellingworth
    type: :Man
  AssignClass (7685f9c5-05ed-4aa4-87e8-14c6162efd92)
 Call ID: 7685f9c5-05ed-4aa4-87e8-14c6162efd92
  Args:
    source: Charles_Vincent_Ellingworth
    type: :Person
  AddLiteral (0340ae4c-a770-4dcc-8d2d-e9d5ad1f1817)
 Call ID: 0340ae4c-a770-4dcc-8d2d-e9d5ad1f1817
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 1987
    source: Amanda_Ellingworth
  AddTriple (0a699c2e-a8fb-481d-bd5e-55fa953fea4d)
 Call ID: 0a699c2e-a8fb-481d-bd5e-55fa953fea4d
  Args:
    relation: :hasRelation
    target: Charles_Vincent_Ellingworth
    source: Amanda_Ellingworth
  AssignClass (62450409-18df-4dc7-a4a2-af0b0a19e274)
 Call ID: 62450409-18df-4dc7-a4a2-af0b0a19e274
  Args:
    source: Prince_Philip
    type: :Man
  AssignClass (93741f2c-04e0-49a1-806a-a991d09207a6)
 Call ID: 93741f2c-04e0-49a1-806a-a991d09207a6
  Args:
    type: :Person
    source: Prince_Philip
  AddTriple (c6e3b6b5-3aa1-486e-ba1d-0df951e2784d)
 Call ID: c6e3b6b5-3aa1-486e-ba1d-0df951e2784d
  Args:
    target: Prince_Philip
    relation: :isUncleOf
    source: Louis_Mountbatten
  AssignClass (1b637d22-4232-4988-aa2b-b9147a07f3e4)
 Call ID: 1b637d22-4232-4988-aa2b-b9147a07f3e4
  Args:
    source: Queen_Elizabeth_II
    type: :Woman
  AssignClass (d03c12be-5512-4a5a-9072-5fea926ba6c1)
 Call ID: d03c12be-5512-4a5a-9072-5fea926ba6c1
  Args:
    source: Queen_Elizabeth_II
    type: :Person
  AssignClass (8ee01da7-8f05-48c2-85bf-cf16ff622a31)
 Call ID: 8ee01da7-8f05-48c2-85bf-cf16ff622a31
  Args:
    source: Charles_Prince_of_Wales
    type: :Man
  AssignClass (3b006e55-5427-4fa0-bcbc-0f4942531928)
 Call ID: 3b006e55-5427-4fa0-bcbc-0f4942531928
  Args:
    source: Charles_Prince_of_Wales
    type: :Person
  AddTriple (981e7c88-0dfe-4c13-b330-8fb57f39c7e8)
 Call ID: 981e7c88-0dfe-4c13-b330-8fb57f39c7e8
  Args:
    target: Charles_Prince_of_Wales
    relation: :isAncestorOf
    source: Louis_Mountbatten
  Finish (f121010e-cff0-4ac5-a8d5-3da3ce29a6be)
 Call ID: f121010e-cff0-4ac5-a8d5-3da3ce29a6be
  Args: