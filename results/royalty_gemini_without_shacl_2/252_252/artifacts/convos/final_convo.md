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
  AssignClass (a477220c-65ca-4791-b598-5d034b7d0be6)
 Call ID: a477220c-65ca-4791-b598-5d034b7d0be6
  Args:
    type: :Man
    source: :Michael_Fergus_Bowes-Lyon
  AssignClass (672baa11-28d8-4d31-9f8f-443e689c06da)
 Call ID: 672baa11-28d8-4d31-9f8f-443e689c06da
  Args:
    type: :Person
    source: :Michael_Fergus_Bowes-Lyon
  AddLiteral (d9b07d79-8ff0-4225-a736-6d51c83822bf)
 Call ID: d9b07d79-8ff0-4225-a736-6d51c83822bf
  Args:
    relation: :hasBirthYear
    literal_value: 1957
    source: :Michael_Fergus_Bowes-Lyon
    literal_type: xsd:integer
  AddLiteral (20d0efcc-8293-4cc4-9d43-fffcdb3186ed)
 Call ID: 20d0efcc-8293-4cc4-9d43-fffcdb3186ed
  Args:
    literal_value: 2016
    literal_type: xsd:integer
    source: :Michael_Fergus_Bowes-Lyon
    relation: :hasDeathYear
  AddLiteral (3d4ea73d-47bc-4e3a-bd76-8af809babdb7)
 Call ID: 3d4ea73d-47bc-4e3a-bd76-8af809babdb7
  Args:
    relation: :knownAs
    literal_value: Mikey Strathmore
    literal_type: xsd:string
    source: :Michael_Fergus_Bowes-Lyon
  AssignClass (553e77a9-7eed-4f60-b262-b966c7952535)
 Call ID: 553e77a9-7eed-4f60-b262-b966c7952535
  Args:
    source: :Fergus_Bowes-Lyon
    type: :Man
  AssignClass (7061e383-6f7b-46c2-8125-6896872428eb)
 Call ID: 7061e383-6f7b-46c2-8125-6896872428eb
  Args:
    type: :Person
    source: :Fergus_Bowes-Lyon
  AssignClass (9a06ce5d-0a19-47c7-984c-3c6699039fce)
 Call ID: 9a06ce5d-0a19-47c7-984c-3c6699039fce
  Args:
    source: :Mary_Pamela_McCorquodale
    type: :Woman
  AssignClass (4a031282-b16a-431e-8023-6f5a40917c8e)
 Call ID: 4a031282-b16a-431e-8023-6f5a40917c8e
  Args:
    type: :Person
    source: :Mary_Pamela_McCorquodale
  AddTriple (ade2b43b-db0f-40d8-ae0d-3428478294ce)
 Call ID: ade2b43b-db0f-40d8-ae0d-3428478294ce
  Args:
    source: :Michael_Fergus_Bowes-Lyon
    target: :Fergus_Bowes-Lyon
    relation: :hasFather
  AddTriple (ad8da9fc-cadd-446d-bd24-3b17a357e650)
 Call ID: ad8da9fc-cadd-446d-bd24-3b17a357e650
  Args:
    relation: :hasMother
    target: :Mary_Pamela_McCorquodale
    source: :Michael_Fergus_Bowes-Lyon
  AssignClass (f18faf25-feb1-469f-be2e-867a9bdc568a)
 Call ID: f18faf25-feb1-469f-be2e-867a9bdc568a
  Args:
    source: :Michael_Bowes-Lyon
    type: :Man
  AssignClass (8e05489d-d41b-4c66-b3f5-fa2df38e089d)
 Call ID: 8e05489d-d41b-4c66-b3f5-fa2df38e089d
  Args:
    source: :Michael_Bowes-Lyon
    type: :Person
  AddTriple (c857ce95-5cfd-4d68-bfa0-667cf6e80eaa)
 Call ID: c857ce95-5cfd-4d68-bfa0-667cf6e80eaa
  Args:
    source: :Fergus_Bowes-Lyon
    target: :Michael_Bowes-Lyon
    relation: :hasFather
  AssignClass (ecf17ffa-17b8-488a-9589-1f4f3e953281)
 Call ID: ecf17ffa-17b8-488a-9589-1f4f3e953281
  Args:
    type: :Woman
    source: :Isobel_Charlotte_Weatherall
  AssignClass (f19c187c-4f55-431e-8f48-e56966f09b6a)
 Call ID: f19c187c-4f55-431e-8f48-e56966f09b6a
  Args:
    type: :Person
    source: :Isobel_Charlotte_Weatherall
  AddTriple (d2f6579c-26a0-400e-874e-66e187b94539)
 Call ID: d2f6579c-26a0-400e-874e-66e187b94539
  Args:
    relation: :hasRelation
    source: :Michael_Fergus_Bowes-Lyon
    target: :Isobel_Charlotte_Weatherall
  AddLiteral (2d243a47-77f5-445b-ab76-c60c1e29fee2)
 Call ID: 2d243a47-77f5-445b-ab76-c60c1e29fee2
  Args:
    relation: :hasMarriageYear
    literal_value: 1984
    literal_type: xsd:integer
    source: :Michael_Fergus_Bowes-Lyon
  AssignClass (55a22761-a82b-4170-88d4-410c4c9e9db6)
 Call ID: 55a22761-a82b-4170-88d4-410c4c9e9db6
  Args:
    source: :Damaris_Stuart-William
    type: :Woman
  AssignClass (a4cab1bb-acbb-40e6-86a2-fb0ca26b65ce)
 Call ID: a4cab1bb-acbb-40e6-86a2-fb0ca26b65ce
  Args:
    type: :Person
    source: :Damaris_Stuart-William
  AddTriple (98345ccc-3174-4e4e-adf5-6842d2ac911b)
 Call ID: 98345ccc-3174-4e4e-adf5-6842d2ac911b
  Args:
    source: :Michael_Fergus_Bowes-Lyon
    target: :Damaris_Stuart-William
    relation: :hasRelation
  AddLiteral (6a8106ef-c496-4ee1-8dd6-ab2a2c318693)
 Call ID: 6a8106ef-c496-4ee1-8dd6-ab2a2c318693
  Args:
    relation: :hasMarriageYear
    source: :Michael_Fergus_Bowes-Lyon
    literal_type: xsd:integer
    literal_value: 2005
  AssignClass (b6ae02b0-b2b2-43d2-8b92-93f4515df7ba)
 Call ID: b6ae02b0-b2b2-43d2-8b92-93f4515df7ba
  Args:
    type: :Woman
    source: :Karen_Baxter
  AssignClass (d8bd1e0a-6f27-4e50-89d0-db57fa57d555)
 Call ID: d8bd1e0a-6f27-4e50-89d0-db57fa57d555
  Args:
    source: :Karen_Baxter
    type: :Person
  AddTriple (3ec45813-a066-4c61-8090-b5c55fb22b3b)
 Call ID: 3ec45813-a066-4c61-8090-b5c55fb22b3b
  Args:
    relation: :hasRelation
    target: :Karen_Baxter
    source: :Michael_Fergus_Bowes-Lyon
  AddLiteral (3e174221-762f-488e-9cda-31ac4f7b83b0)
 Call ID: 3e174221-762f-488e-9cda-31ac4f7b83b0
  Args:
    literal_value: 2012
    source: :Michael_Fergus_Bowes-Lyon
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AssignClass (f9d5d3b0-82bd-48d1-9309-51f484ae74cf)
 Call ID: f9d5d3b0-82bd-48d1-9309-51f484ae74cf
  Args:
    source: :Percy_Weatherall
    type: :Man
  AssignClass (6255fc1e-dda9-48e6-997c-599ac15c6bd9)
 Call ID: 6255fc1e-dda9-48e6-997c-599ac15c6bd9
  Args:
    type: :Person
    source: :Percy_Weatherall
  AddTriple (ae6bc9f2-44a1-408c-8188-ee4f45f837c4)
 Call ID: ae6bc9f2-44a1-408c-8188-ee4f45f837c4
  Args:
    relation: :hasSister
    target: :Isobel_Charlotte_Weatherall
    source: :Percy_Weatherall
  Finish (3232abf3-84f4-4be1-aedc-48e258751ec5)
 Call ID: 3232abf3-84f4-4be1-aedc-48e258751ec5
  Args: