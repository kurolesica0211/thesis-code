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
Bernhard, Prince of Saxe-Meiningen (German: Bernhard, Prinz von Sachsen-Meiningen; 30 June 1901 – 4 October 1984) was the head of the House of Saxe-Meiningen from 1946 until his death.
Prince of Saxe-Meiningen

Bernhard was born in Köln the third son of Prince Frederick Johann of Saxe-Meiningen and Countess Adelaide of Lippe-Biesterfeld.
His father was the second son of Georg II, Duke of Saxe-Meiningen and his mother a daughter of Count Ernst of Lippe-Biesterfeld.
After the death of his older brother Prince Georg in 1946 his nephew Prince Frederick Alfred renounced his succession rights and so Bernhard succeeded to the headship of the house of Saxe-Meiningen and the nominal title of Duke of Saxe-Meiningen (as Bernhard IV).
As his first marriage was morganatic his second son Prince Frederick Konrad succeeded him as head of the ducal house following his death in Bad Krozingen.
Bernhard and his first wife were declared guilty of a Nazi conspiracy against Austria in 1933; he was sentenced to six weeks in prison, while she was placed under house arrest.
Family

Bernhard was married morganatically to Margot Grössler (1911–1998), from Wrocław, daughter of Friedrich Grössler, a merchant, and Erika Wägner, in Eichenhof
They had two children, both of whom had no succession rights:


Bernhard married secondly in Ziegenberg über Bad Nauheim on 11 August 1948 to Baroness Vera Schäffer von Bernstein (1914–1994), daughter of Baron Friedrich "Fritz" Schäffer von Bernstein (1868–1958) and Emma Carola, née Passavant (1884–1971).
They had three children, including a son, Konrad, with full rights to the succession to the house of Saxe-Meiningen:


Ancestry

References



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
  AssignClass (dc7a267f-64fa-4b25-91e5-f0ed208789a1)
 Call ID: dc7a267f-64fa-4b25-91e5-f0ed208789a1
  Args:
    source: Bernhard_Prince_of_Saxe-Meiningen
    type: :Man
  AssignClass (1416f680-1f96-4391-8a26-e9d982f2d0ab)
 Call ID: 1416f680-1f96-4391-8a26-e9d982f2d0ab
  Args:
    source: Bernhard_Prince_of_Saxe-Meiningen
    type: :Person
  AddLiteral (fdb39503-d022-4452-9661-3536e192e407)
 Call ID: fdb39503-d022-4452-9661-3536e192e407
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1901
    source: Bernhard_Prince_of_Saxe-Meiningen
  AddLiteral (23dcb61f-5910-4f29-a85c-3cdc6a3ef1db)
 Call ID: 23dcb61f-5910-4f29-a85c-3cdc6a3ef1db
  Args:
    literal_value: 1984
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: Bernhard_Prince_of_Saxe-Meiningen
  AssignClass (adba8165-db35-4d41-aa1f-3ccbc7d8b8a7)
 Call ID: adba8165-db35-4d41-aa1f-3ccbc7d8b8a7
  Args:
    source: Prince_Frederick_Johann_of_Saxe-Meiningen
    type: :Man
  AssignClass (87675750-d2cc-4e46-8fb7-072342e19e3d)
 Call ID: 87675750-d2cc-4e46-8fb7-072342e19e3d
  Args:
    type: :Person
    source: Prince_Frederick_Johann_of_Saxe-Meiningen
  AssignClass (6089ea20-dff4-4370-a29b-133714db7806)
 Call ID: 6089ea20-dff4-4370-a29b-133714db7806
  Args:
    type: :Woman
    source: Countess_Adelaide_of_Lippe-Biesterfeld
  AssignClass (ab3cdf9f-42a4-473c-9422-7ba7eaf4a331)
 Call ID: ab3cdf9f-42a4-473c-9422-7ba7eaf4a331
  Args:
    type: :Person
    source: Countess_Adelaide_of_Lippe-Biesterfeld
  AddTriple (7f21b554-7627-4cdf-8891-1dca5b2271cb)
 Call ID: 7f21b554-7627-4cdf-8891-1dca5b2271cb
  Args:
    source: Bernhard_Prince_of_Saxe-Meiningen
    relation: :hasFather
    target: Prince_Frederick_Johann_of_Saxe-Meiningen
  AddTriple (89ab4e31-3916-4cf0-9f22-6d33f2381b4c)
 Call ID: 89ab4e31-3916-4cf0-9f22-6d33f2381b4c
  Args:
    source: Bernhard_Prince_of_Saxe-Meiningen
    target: Countess_Adelaide_of_Lippe-Biesterfeld
    relation: :hasMother
  AssignClass (8bad3241-5921-4b8e-993d-01d63644ad58)
 Call ID: 8bad3241-5921-4b8e-993d-01d63644ad58
  Args:
    type: :Man
    source: Georg_II_Duke_of_Saxe-Meiningen
  AssignClass (3dc644bf-fd11-4bf9-8284-bbc5de3d90e3)
 Call ID: 3dc644bf-fd11-4bf9-8284-bbc5de3d90e3
  Args:
    source: Georg_II_Duke_of_Saxe-Meiningen
    type: :Person
  AddTriple (7599da11-30a8-4648-b12b-a9868054571a)
 Call ID: 7599da11-30a8-4648-b12b-a9868054571a
  Args:
    source: Prince_Frederick_Johann_of_Saxe-Meiningen
    relation: :hasFather
    target: Georg_II_Duke_of_Saxe-Meiningen
  AssignClass (39282cf7-ff37-42d1-9164-37582017567d)
 Call ID: 39282cf7-ff37-42d1-9164-37582017567d
  Args:
    source: Count_Ernst_of_Lippe-Biesterfeld
    type: :Man
  AssignClass (665f414a-16c5-4c73-8529-939c45a960de)
 Call ID: 665f414a-16c5-4c73-8529-939c45a960de
  Args:
    type: :Person
    source: Count_Ernst_of_Lippe-Biesterfeld
  AddTriple (561b6e85-fe8e-4c98-a382-875b995997c1)
 Call ID: 561b6e85-fe8e-4c98-a382-875b995997c1
  Args:
    relation: :hasFather
    target: Count_Ernst_of_Lippe-Biesterfeld
    source: Countess_Adelaide_of_Lippe-Biesterfeld
  AssignClass (6c79ad4d-c511-49e6-a941-e0a4fff93c91)
 Call ID: 6c79ad4d-c511-49e6-a941-e0a4fff93c91
  Args:
    type: :Man
    source: Prince_Georg
  AssignClass (14a097ad-b8cd-4750-9aed-f9b2d095584a)
 Call ID: 14a097ad-b8cd-4750-9aed-f9b2d095584a
  Args:
    type: :Person
    source: Prince_Georg
  AddTriple (000b7bad-b84b-4d90-8533-7aa91cbd9b5b)
 Call ID: 000b7bad-b84b-4d90-8533-7aa91cbd9b5b
  Args:
    relation: :hasBrother
    target: Prince_Georg
    source: Bernhard_Prince_of_Saxe-Meiningen
  AssignClass (391c09fd-e404-464a-8b2e-499ba209cc11)
 Call ID: 391c09fd-e404-464a-8b2e-499ba209cc11
  Args:
    source: Prince_Frederick_Alfred
    type: :Man
  AssignClass (2a2d5257-a7f5-406c-8dea-3a5613f123dc)
 Call ID: 2a2d5257-a7f5-406c-8dea-3a5613f123dc
  Args:
    type: :Person
    source: Prince_Frederick_Alfred
  AddTriple (7d5301ee-81a3-4a68-8e95-ec7a78860d04)
 Call ID: 7d5301ee-81a3-4a68-8e95-ec7a78860d04
  Args:
    target: Prince_Georg
    relation: :hasFather
    source: Prince_Frederick_Alfred
  AssignClass (d61f8c01-ebc1-4b40-b0bb-3083fc6cbb46)
 Call ID: d61f8c01-ebc1-4b40-b0bb-3083fc6cbb46
  Args:
    source: Margot_Grössler
    type: :Woman
  AssignClass (e885d1b8-a204-47f5-bd0d-2ac6e8d0b71b)
 Call ID: e885d1b8-a204-47f5-bd0d-2ac6e8d0b71b
  Args:
    source: Margot_Grössler
    type: :Person
  AddLiteral (a82c1dfd-d416-41a6-98c8-3ef1cf53ebf2)
 Call ID: a82c1dfd-d416-41a6-98c8-3ef1cf53ebf2
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1911
    source: Margot_Grössler
  AddLiteral (9d9c1f0a-9c60-4f49-9c4b-4db9c683c0ad)
 Call ID: 9d9c1f0a-9c60-4f49-9c4b-4db9c683c0ad
  Args:
    source: Margot_Grössler
    literal_value: 1998
    literal_type: xsd:integer
    relation: :hasDeathYear
  AssignClass (85cce0a8-bb1f-41fd-95b0-b331a1d87913)
 Call ID: 85cce0a8-bb1f-41fd-95b0-b331a1d87913
  Args:
    source: Friedrich_Grössler
    type: :Man
  AssignClass (03b64469-af2c-4ac8-a897-d7492be332f5)
 Call ID: 03b64469-af2c-4ac8-a897-d7492be332f5
  Args:
    type: :Person
    source: Friedrich_Grössler
  AssignClass (ee450784-45c1-4ace-b996-f10da376379a)
 Call ID: ee450784-45c1-4ace-b996-f10da376379a
  Args:
    type: :Woman
    source: Erika_Wägner
  AssignClass (88349355-829b-417e-8b49-03da184f5d99)
 Call ID: 88349355-829b-417e-8b49-03da184f5d99
  Args:
    source: Erika_Wägner
    type: :Person
  AddTriple (9d91b7d8-84b2-40a6-9c9f-811c5a541d43)
 Call ID: 9d91b7d8-84b2-40a6-9c9f-811c5a541d43
  Args:
    target: Friedrich_Grössler
    relation: :hasFather
    source: Margot_Grössler
  AddTriple (273fe51e-7ff7-4e9a-8cc4-7f51748a750e)
 Call ID: 273fe51e-7ff7-4e9a-8cc4-7f51748a750e
  Args:
    relation: :hasMother
    target: Erika_Wägner
    source: Margot_Grössler
  AssignClass (2531259b-5bc2-42b6-a0c8-2ea928eacc6f)
 Call ID: 2531259b-5bc2-42b6-a0c8-2ea928eacc6f
  Args:
    type: :Man
    source: Prince_Frederick_Konrad
  AssignClass (e4c32dfa-cc7f-4f83-8a60-9ca0c5d184d4)
 Call ID: e4c32dfa-cc7f-4f83-8a60-9ca0c5d184d4
  Args:
    source: Prince_Frederick_Konrad
    type: :Person
  AddTriple (19a62a7a-13c8-4b38-a20a-4ae5a579a061)
 Call ID: 19a62a7a-13c8-4b38-a20a-4ae5a579a061
  Args:
    target: Bernhard_Prince_of_Saxe-Meiningen
    relation: :hasFather
    source: Prince_Frederick_Konrad
  AddTriple (e75749ef-dd86-4894-87cd-7dc0de27a69b)
 Call ID: e75749ef-dd86-4894-87cd-7dc0de27a69b
  Args:
    relation: :hasMother
    target: Margot_Grössler
    source: Prince_Frederick_Konrad
  AssignClass (c1ad618f-d86c-45ba-a300-6ba659d9b08d)
 Call ID: c1ad618f-d86c-45ba-a300-6ba659d9b08d
  Args:
    source: Baroness_Vera_Schäffer_von_Bernstein
    type: :Woman
  AssignClass (eae8d876-5ccd-4bb1-a559-2d232091338f)
 Call ID: eae8d876-5ccd-4bb1-a559-2d232091338f
  Args:
    source: Baroness_Vera_Schäffer_von_Bernstein
    type: :Person
  AddLiteral (5e46f641-10f8-4fc1-9bf2-79dba65d089f)
 Call ID: 5e46f641-10f8-4fc1-9bf2-79dba65d089f
  Args:
    source: Baroness_Vera_Schäffer_von_Bernstein
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1914
  AddLiteral (c28c7bd7-1d79-409c-8406-37c900819612)
 Call ID: c28c7bd7-1d79-409c-8406-37c900819612
  Args:
    source: Baroness_Vera_Schäffer_von_Bernstein
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 1994
  AddLiteral (90e6830c-116e-4092-a4c6-dc23b122bb9f)
 Call ID: 90e6830c-116e-4092-a4c6-dc23b122bb9f
  Args:
    source: Bernhard_Prince_of_Saxe-Meiningen
    literal_value: 1948
    relation: :hasMarriageYear
    literal_type: xsd:integer
  AddTriple (0dbfe5eb-0777-4a61-90c2-5008773a69a7)
 Call ID: 0dbfe5eb-0777-4a61-90c2-5008773a69a7
  Args:
    relation: :hasRelation
    target: Baroness_Vera_Schäffer_von_Bernstein
    source: Bernhard_Prince_of_Saxe-Meiningen
  AssignClass (80d507d0-0e19-4cb6-8cb2-34cfcd71bce9)
 Call ID: 80d507d0-0e19-4cb6-8cb2-34cfcd71bce9
  Args:
    source: Baron_Friedrich_Schäffer_von_Bernstein
    type: :Man
  AssignClass (256e0a46-9abd-4a4a-9bcd-4b170e8d6807)
 Call ID: 256e0a46-9abd-4a4a-9bcd-4b170e8d6807
  Args:
    type: :Person
    source: Baron_Friedrich_Schäffer_von_Bernstein
  AddLiteral (55c68c93-76e5-4d16-ab9b-2686d379b41c)
 Call ID: 55c68c93-76e5-4d16-ab9b-2686d379b41c
  Args:
    source: Baron_Friedrich_Schäffer_von_Bernstein
    literal_value: 1868
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (0e2eb0bb-05b0-4d0e-9dc2-e7f4819f599b)
 Call ID: 0e2eb0bb-05b0-4d0e-9dc2-e7f4819f599b
  Args:
    source: Baron_Friedrich_Schäffer_von_Bernstein
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 1958
  AssignClass (ebcd23c7-6485-42c6-926b-dba95e5128cd)
 Call ID: ebcd23c7-6485-42c6-926b-dba95e5128cd
  Args:
    source: Emma_Carola_Passavant
    type: :Woman
  AssignClass (c7e9f777-3faa-4965-9f0b-379f6b30e681)
 Call ID: c7e9f777-3faa-4965-9f0b-379f6b30e681
  Args:
    source: Emma_Carola_Passavant
    type: :Person
  AddLiteral (92ebdb81-6afb-4528-8573-dc4d3c49acf3)
 Call ID: 92ebdb81-6afb-4528-8573-dc4d3c49acf3
  Args:
    literal_value: 1884
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Emma_Carola_Passavant
  AddLiteral (1b8cd912-66e0-4c95-aef6-7716d9ec292d)
 Call ID: 1b8cd912-66e0-4c95-aef6-7716d9ec292d
  Args:
    literal_value: 1971
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: Emma_Carola_Passavant
  AddTriple (341d62c9-2ed6-40b2-bc93-17cbb242753f)
 Call ID: 341d62c9-2ed6-40b2-bc93-17cbb242753f
  Args:
    target: Baron_Friedrich_Schäffer_von_Bernstein
    relation: :hasFather
    source: Baroness_Vera_Schäffer_von_Bernstein
  AddTriple (9d621563-b8db-4105-882c-fe0a5e8eb9e3)
 Call ID: 9d621563-b8db-4105-882c-fe0a5e8eb9e3
  Args:
    source: Baroness_Vera_Schäffer_von_Bernstein
    target: Emma_Carola_Passavant
    relation: :hasMother
  AssignClass (b6fcf026-481b-4d30-927a-951a4964010d)
 Call ID: b6fcf026-481b-4d30-927a-951a4964010d
  Args:
    type: :Man
    source: Konrad
  AssignClass (372ab059-506d-4d00-8857-29d6f117c42a)
 Call ID: 372ab059-506d-4d00-8857-29d6f117c42a
  Args:
    source: Konrad
    type: :Person
  AddTriple (3d615c20-676f-417e-ab1f-7c2f46b1d289)
 Call ID: 3d615c20-676f-417e-ab1f-7c2f46b1d289
  Args:
    source: Konrad
    relation: :hasFather
    target: Bernhard_Prince_of_Saxe-Meiningen
  AddTriple (cef0eecb-9ef4-4493-9b69-a4ff8f381885)
 Call ID: cef0eecb-9ef4-4493-9b69-a4ff8f381885
  Args:
    target: Baroness_Vera_Schäffer_von_Bernstein
    relation: :hasMother
    source: Konrad
  Finish (e90196cb-a1e5-430d-b845-1caa1cd28e54)
 Call ID: e90196cb-a1e5-430d-b845-1caa1cd28e54
  Args: