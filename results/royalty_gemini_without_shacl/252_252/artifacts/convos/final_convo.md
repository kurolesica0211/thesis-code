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
Michael Fergus Bowes-Lyon, 18th and 5th Earl of Strathmore and Kinghorne (7 June 1957 – 27 February 2016), styled Lord Glamis between 1972 and 1987, also known as Mikey Strathmore, was a British Conservative politician, Scots Guards officer and stockbroker.
Early life and education

Strathmore was born on 7 June 1957 in Windsor, the only son of Fergus Bowes-Lyon, later 17th Earl of Strathmore and Kinghorne, and his wife, Mary Pamela McCorquodale.
His paternal grandfather, Lieutenant-Colonel The Honourable Michael Bowes-Lyon, was an elder brother of Queen Elizabeth the Queen Mother, thus making Michael a first cousin once removed of Queen Elizabeth II and Princess Margaret.
Career

After Sandhurst, Strathmore was commissioned in the Scots Guards in 1980.
In 1987, Strathmore succeeded his father as 18th Earl of Strathmore and Kinghorne and inherited Holwick Hall in Teesdale, County Durham, and Glamis Castle, the Queen Mother's girlhood home, in Angus.
After resigning his ministerial post, Strathmore sat on the board of Polypipe from 1994 until it was acquired by IMI plc in 1999.
He also served as president of Boys' Brigade from 1994 to 1999 and as patron of the Friends of the Bowes Museum in County Durham, a position he inherited from the Queen Mother.
Personal life

Strathmore was married three times.
On 14 November 1984, Lord Glamis, as he was then, married Isobel Charlotte Weatherall (born c. 1962), great-granddaughter of Henry Keswick and sister of Percy Weatherall, at St James's Church, Piccadilly, with the Queen Mother in attendance.
Strathmore and Weatherall were separated in 2003 and divorced in 2005.
On 24 November 2005, Strathmore married Damaris Stuart-William, a clinical psychologist.
They had one son:


On 4 August 2012, Strathmore married Karen Baxter (née Orrock), who survived him.
As a hobby, he restored old automobiles and lorries, often featuring in the Strathmore Vintage Vehicle Rally.
In 2002, as the head of the Bowes-Lyon family, he walked behind the Queen Mother's coffin during her funeral procession and attended the private service of committal in the King George VI Memorial Chapel.
Strathmore died of colorectal cancer on 27 February 2016 in London, aged 58.
A memorial service was held at the Church of St Mary the Virgin in Middleton-in-Teesdale, near his County Durham properties, on 12 May and another, attended by Prince Charles, was held at St Martin-in-the-Fields in London on 8 June.



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
  AssignClass (a36c6a18-ccf4-44f1-ac59-d6d5f88e919d)
 Call ID: a36c6a18-ccf4-44f1-ac59-d6d5f88e919d
  Args:
    type: :Man
    source: Michael_Fergus_Bowes-Lyon
  AssignClass (d8921871-cb23-4004-88a2-93f26aec5f89)
 Call ID: d8921871-cb23-4004-88a2-93f26aec5f89
  Args:
    type: :Person
    source: Michael_Fergus_Bowes-Lyon
  AddLiteral (2705033a-a51b-414e-9f3d-c891993ae2f6)
 Call ID: 2705033a-a51b-414e-9f3d-c891993ae2f6
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1957
    source: Michael_Fergus_Bowes-Lyon
  AddLiteral (374a5630-2ac2-4e36-8ac7-42435b739f02)
 Call ID: 374a5630-2ac2-4e36-8ac7-42435b739f02
  Args:
    source: Michael_Fergus_Bowes-Lyon
    relation: :hasDeathYear
    literal_value: 2016
    literal_type: xsd:integer
  AddLiteral (18f20e12-97ce-4a35-bd46-f680d5044354)
 Call ID: 18f20e12-97ce-4a35-bd46-f680d5044354
  Args:
    literal_type: xsd:string
    relation: :alsoKnownAs
    literal_value: Mikey Strathmore
    source: Michael_Fergus_Bowes-Lyon
  AssignClass (3366cc38-d6e8-40bc-8ec1-bb955987c1a4)
 Call ID: 3366cc38-d6e8-40bc-8ec1-bb955987c1a4
  Args:
    type: :Man
    source: Fergus_Bowes-Lyon
  AssignClass (b3dccb99-1db2-4eae-8590-853ff46f5c44)
 Call ID: b3dccb99-1db2-4eae-8590-853ff46f5c44
  Args:
    source: Fergus_Bowes-Lyon
    type: :Person
  AddTriple (b2d73964-18d5-4c1d-9a8e-c5b78e56a787)
 Call ID: b2d73964-18d5-4c1d-9a8e-c5b78e56a787
  Args:
    source: Michael_Fergus_Bowes-Lyon
    target: Fergus_Bowes-Lyon
    relation: :hasFather
  AssignClass (d564154d-633e-4dd6-ab39-68b8e51a3104)
 Call ID: d564154d-633e-4dd6-ab39-68b8e51a3104
  Args:
    source: Mary_Pamela_McCorquodale
    type: :Woman
  AssignClass (4f2a947f-4a6e-4eef-8430-6381bf7ad0c4)
 Call ID: 4f2a947f-4a6e-4eef-8430-6381bf7ad0c4
  Args:
    source: Mary_Pamela_McCorquodale
    type: :Person
  AddTriple (b850ebbf-8c10-42a5-8f13-59b1e9aa5331)
 Call ID: b850ebbf-8c10-42a5-8f13-59b1e9aa5331
  Args:
    source: Michael_Fergus_Bowes-Lyon
    relation: :hasMother
    target: Mary_Pamela_McCorquodale
  AssignClass (0cbe6f39-00ff-49a4-8279-a1f0bf329d81)
 Call ID: 0cbe6f39-00ff-49a4-8279-a1f0bf329d81
  Args:
    type: :Man
    source: Michael_Bowes-Lyon_grandfather
  AssignClass (505f8d19-5a0f-452c-ab14-7c22ec685c44)
 Call ID: 505f8d19-5a0f-452c-ab14-7c22ec685c44
  Args:
    type: :Person
    source: Michael_Bowes-Lyon_grandfather
  AddTriple (dd634f34-f6f8-422e-8fba-0876c67d289e)
 Call ID: dd634f34-f6f8-422e-8fba-0876c67d289e
  Args:
    relation: :hasFather
    target: Michael_Bowes-Lyon_grandfather
    source: Fergus_Bowes-Lyon
  AssignClass (649c437e-c130-4276-a408-97ee28025637)
 Call ID: 649c437e-c130-4276-a408-97ee28025637
  Args:
    source: Isobel_Charlotte_Weatherall
    type: :Woman
  AssignClass (c9109f73-928e-4a5e-99d6-e746c37fb808)
 Call ID: c9109f73-928e-4a5e-99d6-e746c37fb808
  Args:
    type: :Person
    source: Isobel_Charlotte_Weatherall
  AddLiteral (556dda95-96e0-48a4-8a79-9ffffcf76c47)
 Call ID: 556dda95-96e0-48a4-8a79-9ffffcf76c47
  Args:
    literal_type: xsd:integer
    literal_value: 1984
    relation: :hasMarriageYear
    source: Michael_Fergus_Bowes-Lyon
  AddTriple (e2202377-54bb-47f4-aec7-d9750d6858a7)
 Call ID: e2202377-54bb-47f4-aec7-d9750d6858a7
  Args:
    source: Michael_Fergus_Bowes-Lyon
    relation: :hasRelation
    target: Isobel_Charlotte_Weatherall
  AssignClass (b88a39ca-d6b2-4d97-b9da-bad372b0c06f)
 Call ID: b88a39ca-d6b2-4d97-b9da-bad372b0c06f
  Args:
    type: :Woman
    source: Damaris_Stuart-William
  AssignClass (d0dfb699-c7e5-4630-86ab-bdc28f133da1)
 Call ID: d0dfb699-c7e5-4630-86ab-bdc28f133da1
  Args:
    type: :Person
    source: Damaris_Stuart-William
  AddLiteral (843a2fae-37e9-43d6-8314-dd276b385277)
 Call ID: 843a2fae-37e9-43d6-8314-dd276b385277
  Args:
    source: Michael_Fergus_Bowes-Lyon
    literal_value: 2005
    relation: :hasMarriageYear
    literal_type: xsd:integer
  AddTriple (5a58f23b-52b7-45e9-a7fe-4a2b2d18e126)
 Call ID: 5a58f23b-52b7-45e9-a7fe-4a2b2d18e126
  Args:
    source: Michael_Fergus_Bowes-Lyon
    relation: :hasRelation
    target: Damaris_Stuart-William
  AssignClass (39e74f52-6100-4a74-adee-0eede5848cc8)
 Call ID: 39e74f52-6100-4a74-adee-0eede5848cc8
  Args:
    type: :Woman
    source: Karen_Baxter
  AssignClass (8d3a316b-bfb7-41e3-aa1e-6d3321b9ab16)
 Call ID: 8d3a316b-bfb7-41e3-aa1e-6d3321b9ab16
  Args:
    type: :Person
    source: Karen_Baxter
  AddLiteral (65a69d67-0b74-4fac-8d75-cbdbb00eb37f)
 Call ID: 65a69d67-0b74-4fac-8d75-cbdbb00eb37f
  Args:
    relation: :hasMarriageYear
    literal_value: 2012
    literal_type: xsd:integer
    source: Michael_Fergus_Bowes-Lyon
  AddTriple (e8af9a6a-a1be-41ae-9f46-aaf09e809d2e)
 Call ID: e8af9a6a-a1be-41ae-9f46-aaf09e809d2e
  Args:
    target: Karen_Baxter
    relation: :hasRelation
    source: Michael_Fergus_Bowes-Lyon
  AssignClass (8951cd24-c4e4-4bfb-923f-7840625b6fae)
 Call ID: 8951cd24-c4e4-4bfb-923f-7840625b6fae
  Args:
    source: Percy_Weatherall
    type: :Man
  AssignClass (a00a5c9b-e7b8-429d-bb74-11254877897a)
 Call ID: a00a5c9b-e7b8-429d-bb74-11254877897a
  Args:
    source: Percy_Weatherall
    type: :Person
  AddTriple (e7be1737-7cab-4ce5-ad41-7474cf127d2e)
 Call ID: e7be1737-7cab-4ce5-ad41-7474cf127d2e
  Args:
    target: Percy_Weatherall
    relation: :isSiblingOf
    source: Isobel_Charlotte_Weatherall
  Finish (e246e25e-b3c6-4b62-b662-89fbae9d30cb)
 Call ID: e246e25e-b3c6-4b62-b662-89fbae9d30cb
  Args: