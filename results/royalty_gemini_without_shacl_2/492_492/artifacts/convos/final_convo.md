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
Philipp, Prince of Hohenlohe-Langenburg (Philipp Gottfried Alexander; born 20 January 1970), is the head of the House of Hohenlohe-Langenburg, since the death of his father in 2004.
Early life and ancestry

He was born in Crailsheim, West Germany, the middle child and only son of Kraft, Prince of Hohenlohe-Langenburg (1935–2004) and his first wife, Princess Charlotte of Croÿ (b. 1938).
Paternally, he is a grandson of Princess Margarita of Greece and Denmark, and a grandnephew of Prince Philip, Duke of Edinburgh, whose funeral he attended.
Anne, Princess Royal is one of his godmothers.
Maternally, he is the grandson of Prince Alexander of Croy (1912–2002) and his Scottish wife, Anna Elspeth Campbell (1917–1986), granddaughter of Archibald Campbell, 6th of Glendaruel.
He sought public support from (then) Charles, Prince of Wales, the current King Charles III, and from former vice chancellor and foreign minister Joschka Fischer of the Green Party, who both attended a conference at Langenburg Castle in 2013.
Together with Fischer he founded the Langenburg Forum for Sustainability which cooperates with Charles' International Sustainability Unit


Langenburg castle is partially open to the public, including the state rooms and a museum of classic cars.
Marriage and issue

He married Saskia Binder (b. 15 January 1973 in Munich), daughter of former Deutsche Bank Munich director Hans Peter Binder, on 6 September 2003 in a civil ceremony at Langenburg.



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
  AssignClass (f50291bd-1592-43b0-ab9a-625dfd8747a4)
 Call ID: f50291bd-1592-43b0-ab9a-625dfd8747a4
  Args:
    source: Philipp_Prince_of_Hohenlohe_Langenburg
    type: :Man
  AssignClass (cff449d6-5a9d-4a93-babd-6aeb86910c95)
 Call ID: cff449d6-5a9d-4a93-babd-6aeb86910c95
  Args:
    source: Philipp_Prince_of_Hohenlohe_Langenburg
    type: :Person
  AddLiteral (73ef7f65-c767-4f16-a653-49d28242f1e0)
 Call ID: 73ef7f65-c767-4f16-a653-49d28242f1e0
  Args:
    source: Philipp_Prince_of_Hohenlohe_Langenburg
    relation: :hasBirthYear
    literal_value: 1970
    literal_type: xsd:integer
  AssignClass (5c5c2f49-d528-4b20-b25f-3b5c49b4d312)
 Call ID: 5c5c2f49-d528-4b20-b25f-3b5c49b4d312
  Args:
    source: Kraft_Prince_of_Hohenlohe_Langenburg
    type: :Man
  AssignClass (e7bea614-7684-48f0-9ed7-e9dc9749cc12)
 Call ID: e7bea614-7684-48f0-9ed7-e9dc9749cc12
  Args:
    source: Kraft_Prince_of_Hohenlohe_Langenburg
    type: :Person
  AddLiteral (3ac7fc19-9ea3-490c-8024-e33edaec3ccc)
 Call ID: 3ac7fc19-9ea3-490c-8024-e33edaec3ccc
  Args:
    source: Kraft_Prince_of_Hohenlohe_Langenburg
    relation: :hasBirthYear
    literal_value: 1935
    literal_type: xsd:integer
  AddLiteral (f7435a7d-fa66-4388-b4d2-c2511f60c05e)
 Call ID: f7435a7d-fa66-4388-b4d2-c2511f60c05e
  Args:
    relation: :hasDeathYear
    source: Kraft_Prince_of_Hohenlohe_Langenburg
    literal_type: xsd:integer
    literal_value: 2004
  AddTriple (a7b805cd-de81-4c69-80c3-b3a5ee45c6bb)
 Call ID: a7b805cd-de81-4c69-80c3-b3a5ee45c6bb
  Args:
    target: Kraft_Prince_of_Hohenlohe_Langenburg
    source: Philipp_Prince_of_Hohenlohe_Langenburg
    relation: :hasFather
  AssignClass (b8f8d857-36eb-4d21-9d7d-7e89421835df)
 Call ID: b8f8d857-36eb-4d21-9d7d-7e89421835df
  Args:
    source: Princess_Charlotte_of_Croy
    type: :Woman
  AssignClass (65ed1d67-fc1c-47a2-b1c4-3d5f61493165)
 Call ID: 65ed1d67-fc1c-47a2-b1c4-3d5f61493165
  Args:
    type: :Person
    source: Princess_Charlotte_of_Croy
  AddLiteral (7ac9a329-a2a6-456c-be7c-ecf31b14d5d3)
 Call ID: 7ac9a329-a2a6-456c-be7c-ecf31b14d5d3
  Args:
    literal_type: xsd:integer
    literal_value: 1938
    relation: :hasBirthYear
    source: Princess_Charlotte_of_Croy
  AddTriple (7a614d6f-9b79-44d2-a236-dfa6ead56f38)
 Call ID: 7a614d6f-9b79-44d2-a236-dfa6ead56f38
  Args:
    relation: :hasMother
    source: Philipp_Prince_of_Hohenlohe_Langenburg
    target: Princess_Charlotte_of_Croy
  AssignClass (c5877529-1c6d-4267-8f26-7c08ff8a2493)
 Call ID: c5877529-1c6d-4267-8f26-7c08ff8a2493
  Args:
    source: Princess_Margarita_of_Greece_and_Denmark
    type: :Woman
  AssignClass (12b316b3-0d6e-451d-8fa1-805255f1c291)
 Call ID: 12b316b3-0d6e-451d-8fa1-805255f1c291
  Args:
    source: Princess_Margarita_of_Greece_and_Denmark
    type: :Person
  AddTriple (2df90f49-d306-49a3-98b3-a70e5eac065b)
 Call ID: 2df90f49-d306-49a3-98b3-a70e5eac065b
  Args:
    target: Princess_Margarita_of_Greece_and_Denmark
    relation: :hasAncestor
    source: Philipp_Prince_of_Hohenlohe_Langenburg
  AssignClass (fd6bfcc1-00d4-4946-89c0-d97bef67ca04)
 Call ID: fd6bfcc1-00d4-4946-89c0-d97bef67ca04
  Args:
    type: :Man
    source: Prince_Alexander_of_Croy
  AssignClass (cca5aa51-0510-431b-ade6-42c37be8fbd4)
 Call ID: cca5aa51-0510-431b-ade6-42c37be8fbd4
  Args:
    type: :Person
    source: Prince_Alexander_of_Croy
  AddLiteral (e942ca07-3329-4ffc-b17d-5081c33a6a6b)
 Call ID: e942ca07-3329-4ffc-b17d-5081c33a6a6b
  Args:
    source: Prince_Alexander_of_Croy
    relation: :hasBirthYear
    literal_value: 1912
    literal_type: xsd:integer
  AddLiteral (2d3fe25d-21a7-48a9-b0da-e746fc62195f)
 Call ID: 2d3fe25d-21a7-48a9-b0da-e746fc62195f
  Args:
    literal_type: xsd:integer
    literal_value: 2002
    relation: :hasDeathYear
    source: Prince_Alexander_of_Croy
  AddTriple (274c94dc-f757-4e58-a2fe-9ca805ce24d9)
 Call ID: 274c94dc-f757-4e58-a2fe-9ca805ce24d9
  Args:
    target: Prince_Alexander_of_Croy
    relation: :hasAncestor
    source: Philipp_Prince_of_Hohenlohe_Langenburg
  AssignClass (6b7efbca-d87f-444b-b8c1-f6c181b6bda5)
 Call ID: 6b7efbca-d87f-444b-b8c1-f6c181b6bda5
  Args:
    type: :Woman
    source: Anna_Elspeth_Campbell
  AssignClass (8b320826-c57b-482e-9e49-613083b98522)
 Call ID: 8b320826-c57b-482e-9e49-613083b98522
  Args:
    type: :Person
    source: Anna_Elspeth_Campbell
  AddLiteral (9d2b2744-508d-49af-9e80-fcb90ca463fb)
 Call ID: 9d2b2744-508d-49af-9e80-fcb90ca463fb
  Args:
    relation: :hasBirthYear
    source: Anna_Elspeth_Campbell
    literal_type: xsd:integer
    literal_value: 1917
  AddLiteral (7d01529e-bd0f-4041-bc0a-10ff2c099170)
 Call ID: 7d01529e-bd0f-4041-bc0a-10ff2c099170
  Args:
    source: Anna_Elspeth_Campbell
    relation: :hasDeathYear
    literal_value: 1986
    literal_type: xsd:integer
  AddTriple (53d74fe8-8993-45e4-b0fe-a934fa888421)
 Call ID: 53d74fe8-8993-45e4-b0fe-a934fa888421
  Args:
    target: Anna_Elspeth_Campbell
    relation: :hasAncestor
    source: Philipp_Prince_of_Hohenlohe_Langenburg
  AssignClass (d20e7be5-a9c5-4c10-a779-70b63fdac02e)
 Call ID: d20e7be5-a9c5-4c10-a779-70b63fdac02e
  Args:
    type: :Woman
    source: Saskia_Binder
  AssignClass (fd2e3bec-16c9-428e-be3c-c9e8581156c1)
 Call ID: fd2e3bec-16c9-428e-be3c-c9e8581156c1
  Args:
    type: :Person
    source: Saskia_Binder
  AddLiteral (04fb2b97-10b2-4cc2-ad1b-687abe4fc845)
 Call ID: 04fb2b97-10b2-4cc2-ad1b-687abe4fc845
  Args:
    relation: :hasBirthYear
    source: Saskia_Binder
    literal_type: xsd:integer
    literal_value: 1973
  AddTriple (34d831ce-bb1b-4b9a-bec9-bbc66f1c0dcf)
 Call ID: 34d831ce-bb1b-4b9a-bec9-bbc66f1c0dcf
  Args:
    target: Saskia_Binder
    relation: :hasRelation
    source: Philipp_Prince_of_Hohenlohe_Langenburg
  AddLiteral (b81c4b98-5e12-4089-9615-ae6683df8971)
 Call ID: b81c4b98-5e12-4089-9615-ae6683df8971
  Args:
    relation: :hasMarriageYear
    source: Philipp_Prince_of_Hohenlohe_Langenburg
    literal_type: xsd:integer
    literal_value: 2003
  AssignClass (701f8290-976d-4369-9453-114c61a28763)
 Call ID: 701f8290-976d-4369-9453-114c61a28763
  Args:
    source: Hans_Peter_Binder
    type: :Man
  AssignClass (f9e5f875-33ed-407a-b4f0-ad1af60e3171)
 Call ID: f9e5f875-33ed-407a-b4f0-ad1af60e3171
  Args:
    source: Hans_Peter_Binder
    type: :Person
  AddTriple (6a9bcf83-f67b-4eee-9800-55444ad8c433)
 Call ID: 6a9bcf83-f67b-4eee-9800-55444ad8c433
  Args:
    relation: :hasFather
    source: Saskia_Binder
    target: Hans_Peter_Binder
  Finish (e4d30f12-fe18-4b07-9818-8640101f03ce)
 Call ID: e4d30f12-fe18-4b07-9818-8640101f03ce
  Args: