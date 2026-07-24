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
  AssignClass (4b487294-548e-4038-a0b5-3537b5d85c9b)
 Call ID: 4b487294-548e-4038-a0b5-3537b5d85c9b
  Args:
    type: :Man
    source: :Michael_Fergus_Bowes-Lyon
  AssignClass (c6202f50-ad15-410e-82ec-afbb34a25ab5)
 Call ID: c6202f50-ad15-410e-82ec-afbb34a25ab5
  Args:
    type: :Person
    source: :Michael_Fergus_Bowes-Lyon
  AddLiteral (5d62897c-a710-433f-aa0e-57d89ddf5b5c)
 Call ID: 5d62897c-a710-433f-aa0e-57d89ddf5b5c
  Args:
    literal_value: 1957
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: :Michael_Fergus_Bowes-Lyon
  AddLiteral (fba41c2e-9ba7-4727-aa90-81886062dbe5)
 Call ID: fba41c2e-9ba7-4727-aa90-81886062dbe5
  Args:
    relation: :hasDeathYear
    source: :Michael_Fergus_Bowes-Lyon
    literal_value: 2016
    literal_type: xsd:integer
  AddLiteral (b5e8f2e3-08eb-41ab-8408-e48de6d206ae)
 Call ID: b5e8f2e3-08eb-41ab-8408-e48de6d206ae
  Args:
    literal_value: Mikey Strathmore
    literal_type: xsd:string
    relation: :alsoKnownAs
    source: :Michael_Fergus_Bowes-Lyon
  AssignClass (e313ba11-3709-421e-b3c7-baa5f07a5477)
 Call ID: e313ba11-3709-421e-b3c7-baa5f07a5477
  Args:
    source: :Fergus_Bowes-Lyon
    type: :Man
  AssignClass (b3dacd08-f9b1-4e3a-8a4e-7ed000df01f9)
 Call ID: b3dacd08-f9b1-4e3a-8a4e-7ed000df01f9
  Args:
    type: :Person
    source: :Fergus_Bowes-Lyon
  AddTriple (665ab7ff-8b67-487a-99a1-e04eb8b3aa0e)
 Call ID: 665ab7ff-8b67-487a-99a1-e04eb8b3aa0e
  Args:
    source: :Michael_Fergus_Bowes-Lyon
    relation: :hasFather
    target: :Fergus_Bowes-Lyon
  AssignClass (ff9ab8c1-c94d-4f8b-b866-0a3652a3ca81)
 Call ID: ff9ab8c1-c94d-4f8b-b866-0a3652a3ca81
  Args:
    source: :Mary_Pamela_McCorquodale
    type: :Woman
  AssignClass (4e087e66-43f9-4399-abaf-221fd0cee84d)
 Call ID: 4e087e66-43f9-4399-abaf-221fd0cee84d
  Args:
    type: :Person
    source: :Mary_Pamela_McCorquodale
  AddTriple (508ebf2c-1a49-4e2c-8440-de43641071de)
 Call ID: 508ebf2c-1a49-4e2c-8440-de43641071de
  Args:
    relation: :hasMother
    source: :Michael_Fergus_Bowes-Lyon
    target: :Mary_Pamela_McCorquodale
  AssignClass (f779af60-03fe-4078-9aaf-ccafae39f67c)
 Call ID: f779af60-03fe-4078-9aaf-ccafae39f67c
  Args:
    type: :Man
    source: :Michael_Bowes-Lyon_Grandfather
  AssignClass (8e14d75a-388e-44e7-b7b3-d1c9200ee187)
 Call ID: 8e14d75a-388e-44e7-b7b3-d1c9200ee187
  Args:
    type: :Person
    source: :Michael_Bowes-Lyon_Grandfather
  AddTriple (1b5f58e1-d404-4419-8bc8-b5d9a530399d)
 Call ID: 1b5f58e1-d404-4419-8bc8-b5d9a530399d
  Args:
    source: :Fergus_Bowes-Lyon
    relation: :hasFather
    target: :Michael_Bowes-Lyon_Grandfather
  AssignClass (4aac8ee9-79da-4f5a-81fc-1ffc16757319)
 Call ID: 4aac8ee9-79da-4f5a-81fc-1ffc16757319
  Args:
    type: :Woman
    source: :Queen_Elizabeth_The_Queen_Mother
  AssignClass (5e308db9-dd4c-4ec6-bf20-13ec8ba6ba2c)
 Call ID: 5e308db9-dd4c-4ec6-bf20-13ec8ba6ba2c
  Args:
    source: :Queen_Elizabeth_The_Queen_Mother
    type: :Person
  AddTriple (6976b361-ff4c-4878-8c6c-5549c921a9df)
 Call ID: 6976b361-ff4c-4878-8c6c-5549c921a9df
  Args:
    target: :Queen_Elizabeth_The_Queen_Mother
    relation: :hasSister
    source: :Michael_Bowes-Lyon_Grandfather
  AssignClass (05dcdee3-a735-483a-9cdf-d94e9253cf67)
 Call ID: 05dcdee3-a735-483a-9cdf-d94e9253cf67
  Args:
    source: :Isobel_Charlotte_Weatherall
    type: :Woman
  AssignClass (71e030f3-7078-4b26-a7b8-0c7c656cde66)
 Call ID: 71e030f3-7078-4b26-a7b8-0c7c656cde66
  Args:
    type: :Person
    source: :Isobel_Charlotte_Weatherall
  AddLiteral (d6735851-93b2-4f19-a113-f3d1a4b8ad56)
 Call ID: d6735851-93b2-4f19-a113-f3d1a4b8ad56
  Args:
    literal_value: 1984
    literal_type: xsd:integer
    relation: :hasMarriageYear
    source: :Michael_Fergus_Bowes-Lyon
  AssignClass (90f13b59-96d2-4e9a-8964-bef07d3e64be)
 Call ID: 90f13b59-96d2-4e9a-8964-bef07d3e64be
  Args:
    source: :Damaris_Stuart-William
    type: :Woman
  AssignClass (4db24c64-0f21-4961-9bcc-035022d83dd9)
 Call ID: 4db24c64-0f21-4961-9bcc-035022d83dd9
  Args:
    source: :Damaris_Stuart-William
    type: :Person
  AddLiteral (7b383ac6-ac1b-4b25-b375-e4947c986181)
 Call ID: 7b383ac6-ac1b-4b25-b375-e4947c986181
  Args:
    relation: :hasMarriageYear
    source: :Michael_Fergus_Bowes-Lyon
    literal_value: 2005
    literal_type: xsd:integer
  AssignClass (1e8da962-becc-4d61-8d4f-c9d890fb5c70)
 Call ID: 1e8da962-becc-4d61-8d4f-c9d890fb5c70
  Args:
    type: :Woman
    source: :Karen_Baxter
  AssignClass (1cf611a4-f81b-4606-92e6-57c4bde2a3d9)
 Call ID: 1cf611a4-f81b-4606-92e6-57c4bde2a3d9
  Args:
    source: :Karen_Baxter
    type: :Person
  AddLiteral (74778707-a15f-4841-856a-76de770ff9da)
 Call ID: 74778707-a15f-4841-856a-76de770ff9da
  Args:
    literal_value: 2012
    literal_type: xsd:integer
    relation: :hasMarriageYear
    source: :Michael_Fergus_Bowes-Lyon
  AssignClass (254c19a9-91d9-4248-9ad2-8a4d3f0c7c18)
 Call ID: 254c19a9-91d9-4248-9ad2-8a4d3f0c7c18
  Args:
    type: :Man
    source: :Percy_Weatherall
  AssignClass (7663583e-9571-4a84-b6ac-130a903a086c)
 Call ID: 7663583e-9571-4a84-b6ac-130a903a086c
  Args:
    type: :Person
    source: :Percy_Weatherall
  AddTriple (12ab0a9c-e5cd-4532-a951-d503848e88af)
 Call ID: 12ab0a9c-e5cd-4532-a951-d503848e88af
  Args:
    target: :Isobel_Charlotte_Weatherall
    source: :Percy_Weatherall
    relation: :hasSister
  Finish (94e85372-b5db-498b-acc6-fdee35e68b98)
 Call ID: 94e85372-b5db-498b-acc6-fdee35e68b98
  Args: