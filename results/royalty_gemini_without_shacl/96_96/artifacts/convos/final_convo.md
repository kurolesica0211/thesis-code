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
Patrick Bowes-Lyon, 15th and 2nd Earl of Strathmore and Kinghorne (22 September 1884 – 25 May 1949), styled as Master of Glamis until 1904 and Lord Glamis until 1944, was a British landowner, peer and British Army officer.
He was the eldest brother of Queen Elizabeth the Queen Mother, thus a maternal uncle of Queen Elizabeth II.
Life

Patrick Bowes-Lyon was born on 22 September 1884 at St Paul's Walden Bury, Hertfordshire to Claude, Lord Glamis, and Cecilia Cavendish-Bentinck.
Strathmore and three of his three surviving brothers all served in World War I.
He succeeded his father as 15th and 2nd Earl of Strathmore and Kinghorne (15th earl in the peerage of Scotland and 2nd earl in the peerage of the United Kingdom) on 7 November 1944.
He was the eldest brother of Lady Elizabeth Bowes-Lyon (later Queen Elizabeth the Queen Mother), and thus an uncle of Queen Elizabeth II and Princess Margaret.
As an uncle of the bride, Strathmore was a leading guest at the 1947 wedding of Princess Elizabeth and Philip Mountbatten.
Marriage and issue

He married Lady Dorothy Beatrix Godolphin Osborne (3 December 1888 – 18 June 1946), daughter of George, 10th Duke of Leeds, on 21 November 1908 in London.
They had four children:


Death

Strathmore died on 25 May 1949 in Angus, surviving his wife by almost three years, aged 64.



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
  AssignClass (f7de60b3-6887-45ce-84fa-6e9776895b1a)
 Call ID: f7de60b3-6887-45ce-84fa-6e9776895b1a
  Args:
    source: :Patrick_Bowes-Lyon
    type: :Man
  AssignClass (16e059fe-8845-4ff3-aad0-f7b444b40b41)
 Call ID: 16e059fe-8845-4ff3-aad0-f7b444b40b41
  Args:
    source: :Patrick_Bowes-Lyon
    type: :Person
  AddLiteral (b0f398ad-4f40-4702-ac63-a3c90957ed33)
 Call ID: b0f398ad-4f40-4702-ac63-a3c90957ed33
  Args:
    literal_type: xsd:integer
    literal_value: 1884
    source: :Patrick_Bowes-Lyon
    relation: :hasBirthYear
  AddLiteral (17420211-1502-4dee-b0bc-47c19342d60e)
 Call ID: 17420211-1502-4dee-b0bc-47c19342d60e
  Args:
    source: :Patrick_Bowes-Lyon
    literal_value: 1949
    literal_type: xsd:integer
    relation: :hasDeathYear
  AssignClass (2e645607-28f6-41e4-ba96-83c42e0db130)
 Call ID: 2e645607-28f6-41e4-ba96-83c42e0db130
  Args:
    source: :Claude_Lord_Glamis
    type: :Man
  AssignClass (7738cce2-1c58-4e06-a796-7dc5d1245eca)
 Call ID: 7738cce2-1c58-4e06-a796-7dc5d1245eca
  Args:
    source: :Claude_Lord_Glamis
    type: :Person
  AssignClass (98e73c96-0125-43de-97b2-dfdcdf92726f)
 Call ID: 98e73c96-0125-43de-97b2-dfdcdf92726f
  Args:
    source: :Cecilia_Cavendish-Bentinck
    type: :Woman
  AssignClass (9c498a83-d83d-49c4-a11f-b37dd7d3381c)
 Call ID: 9c498a83-d83d-49c4-a11f-b37dd7d3381c
  Args:
    source: :Cecilia_Cavendish-Bentinck
    type: :Person
  AddTriple (8e9a1596-6236-43a8-acb6-a61bd53c16ee)
 Call ID: 8e9a1596-6236-43a8-acb6-a61bd53c16ee
  Args:
    relation: :hasFather
    source: :Patrick_Bowes-Lyon
    target: :Claude_Lord_Glamis
  AddTriple (55a7a3e9-daed-4a3f-a9e4-4dab6d033b68)
 Call ID: 55a7a3e9-daed-4a3f-a9e4-4dab6d033b68
  Args:
    source: :Patrick_Bowes-Lyon
    relation: :hasMother
    target: :Cecilia_Cavendish-Bentinck
  AssignClass (5d0bf6bd-e3e4-4130-9230-2bed4db5159b)
 Call ID: 5d0bf6bd-e3e4-4130-9230-2bed4db5159b
  Args:
    source: :Lady_Elizabeth_Bowes-Lyon
    type: :Woman
  AssignClass (40b2fdf5-99d2-42d4-a8d0-516a4ab119eb)
 Call ID: 40b2fdf5-99d2-42d4-a8d0-516a4ab119eb
  Args:
    source: :Lady_Elizabeth_Bowes-Lyon
    type: :Person
  AddTriple (6dd51098-9af7-44ed-bf27-2421f04e1e28)
 Call ID: 6dd51098-9af7-44ed-bf27-2421f04e1e28
  Args:
    target: :Lady_Elizabeth_Bowes-Lyon
    source: :Patrick_Bowes-Lyon
    relation: :hasSister
  AssignClass (0628b2f3-38d6-446a-9152-0fd3000d0329)
 Call ID: 0628b2f3-38d6-446a-9152-0fd3000d0329
  Args:
    source: :Queen_Elizabeth_II
    type: :Woman
  AssignClass (14fa5499-2202-4ea0-b35c-e5d8314a028d)
 Call ID: 14fa5499-2202-4ea0-b35c-e5d8314a028d
  Args:
    source: :Queen_Elizabeth_II
    type: :Person
  AssignClass (d6554c1b-f6bf-4fb9-ae0f-2c822d4ff561)
 Call ID: d6554c1b-f6bf-4fb9-ae0f-2c822d4ff561
  Args:
    source: :Princess_Margaret
    type: :Woman
  AssignClass (3f8f95da-9260-4a3a-ba0f-7b80f2a510c3)
 Call ID: 3f8f95da-9260-4a3a-ba0f-7b80f2a510c3
  Args:
    source: :Princess_Margaret
    type: :Person
  AssignClass (abdb0deb-32ae-40bb-baf4-540a7b4f657b)
 Call ID: abdb0deb-32ae-40bb-baf4-540a7b4f657b
  Args:
    source: :Lady_Dorothy_Beatrix_Godolphin_Osborne
    type: :Woman
  AssignClass (155dc700-e570-4ed0-a7d2-df503e04daca)
 Call ID: 155dc700-e570-4ed0-a7d2-df503e04daca
  Args:
    source: :Lady_Dorothy_Beatrix_Godolphin_Osborne
    type: :Person
  AddLiteral (aa7503e7-7148-4097-8d38-d1101d3b3862)
 Call ID: aa7503e7-7148-4097-8d38-d1101d3b3862
  Args:
    relation: :hasMarriageYear
    literal_type: xsd:integer
    literal_value: 1908
    source: :Patrick_Bowes-Lyon
  AddTriple (58cffbb3-94ce-4f98-bfd4-f0b01c4f6be2)
 Call ID: 58cffbb3-94ce-4f98-bfd4-f0b01c4f6be2
  Args:
    target: :Lady_Dorothy_Beatrix_Godolphin_Osborne
    source: :Patrick_Bowes-Lyon
    relation: :hasRelation
  AddLiteral (0deddac5-6b9a-477f-92a0-e72c068b2104)
 Call ID: 0deddac5-6b9a-477f-92a0-e72c068b2104
  Args:
    literal_type: xsd:integer
    source: :Lady_Dorothy_Beatrix_Godolphin_Osborne
    literal_value: 1888
    relation: :hasBirthYear
  AddLiteral (7965c9ef-bf86-47d2-b89d-ffaa830061ad)
 Call ID: 7965c9ef-bf86-47d2-b89d-ffaa830061ad
  Args:
    literal_type: xsd:integer
    source: :Lady_Dorothy_Beatrix_Godolphin_Osborne
    literal_value: 1946
    relation: :hasDeathYear
  AssignClass (69a00a3b-2d7f-49f8-b6a4-a620d613cc3c)
 Call ID: 69a00a3b-2d7f-49f8-b6a4-a620d613cc3c
  Args:
    source: :George_10th_Duke_of_Leeds
    type: :Man
  AssignClass (17a83ddd-a0df-41da-9d5a-3de30fac6864)
 Call ID: 17a83ddd-a0df-41da-9d5a-3de30fac6864
  Args:
    source: :George_10th_Duke_of_Leeds
    type: :Person
  AddTriple (1cd1b50a-6eaf-460c-8878-7db69b818152)
 Call ID: 1cd1b50a-6eaf-460c-8878-7db69b818152
  Args:
    source: :Lady_Dorothy_Beatrix_Godolphin_Osborne
    relation: :hasFather
    target: :George_10th_Duke_of_Leeds
  Finish (2df7c6d1-0eb4-4222-8361-df4c38747a65)
 Call ID: 2df7c6d1-0eb4-4222-8361-df4c38747a65
  Args: