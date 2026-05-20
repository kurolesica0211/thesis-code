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
Peter Mark Andrew Phillips (born 15 November 1977) is a British businessman and member of the British royal family.
He is the son of Anne, Princess Royal, and Mark Phillips, and a nephew of King Charles III.
Born during the reign of his maternal grandmother Queen Elizabeth II, Phillips was fifth in the line of succession to the British throne; as of 2026, he is 19th.
Phillips attended the University of Exeter and later worked for Jaguar Racing.
In 2008, he married Canadian management consultant Autumn Kelly at St George's Chapel, Windsor Castle; they have two children.
Early life and education

Peter Mark Andrew Phillips was born at 10:46 am on 15 November 1977 at St Mary's Hospital, London.
He was the first child of Princess Anne and Mark Phillips, who had married in 1973, and the first grandchild of Queen Elizabeth II and Prince Philip, Duke of Edinburgh.
His godparents were his maternal uncle, Prince Charles; Geoffrey Tiarks; Captain Hamish Lochore; Lady Cecil Cameron of Lochiel and Jane Holderness-Roddam.
Phillips was fifth in line to the throne at birth and remained so until the birth of his cousin William, Prince of Wales in 1982.
Phillips was the first legitimate grandchild of a monarch in more than 500 years to be born without a title or courtesy title.
Phillips has a younger sister, Zara Tindall (née Phillips; born 1981), and two younger half-sisters, Felicity Wade (née Tonkin; born 1985), the daughter of Mark Phillips and his former mistress Heather Tonkin; and Stephanie Phillips (born 1997), the daughter from his father's second marriage to Sandy Pflueger.
Phillips went to Port Regis Prep School in Shaftesbury, Dorset before following some of his family by attending Gordonstoun School in Moray, Scotland.
Phillips represented Scotland at rugby union at youth and junior level in the mid-1990s.
Career

After his graduation in 2000, Phillips worked for Jaguar as corporate hospitality manager and then for Williams racing team, where he was sponsorship accounts manager.
He left Williams in September 2005, for a job as a manager at the Royal Bank of Scotland in Edinburgh.
In the year leading up to June 2016, Phillips was responsible for organising the "Patron's Lunch", in celebration of the Queen's 90th birthday.
In January 2020, Phillips appeared in an advertisement for Chinese company Bright Food.
In the video, he uses his status as a "British royal family member" to promote the company's milk, while surrounded by luxury.
Royal funeral participation

On 17 September 2022, during the period of official mourning for Queen Elizabeth II, Phillips joined his sister and six cousins to mount a 15-minute vigil around the coffin of their grandmother as it lay in state at Westminster Hall.
On 19 September 2022, he joined the Queen's children and other senior members of the royal family in walking behind the cortege in the state funeral procession.
Personal life

Relationships

Elizabeth Iorio and Tara Swain

Phillips dated Elizabeth Iorio, a cod liver oil heiress from the United States, for two years.
Autumn Kelly

In 2003, Phillips met Autumn Kelly, a Canadian management consultant, at the Formula 1 Canadian Grand Prix in Montreal.
If she had been Roman Catholic at the time of the marriage, Phillips would have lost his place in the line of the succession to the throne because of since-repealed terms of the Act of Settlement 1701.
Shortly before their wedding, the couple were interviewed and photographed by Hello! magazine, and were reported to have been paid £500,000, resulting in some concern in royal circles.
The couple lived in Hong Kong after Phillips changed positions within the Royal Bank of Scotland and became head of their sponsorships activities in the region.
Their first child, and the Queen's first great-grandchild, a daughter named Savannah Anne Kathleen, was born on 29 December 2010 at Gloucestershire Royal Hospital.
The Queen was present for the baby's baptism, which took place on 23 April 2011 at Church of the Holy Cross in Avening, Gloucestershire, near Gatcombe Park, the home of Phillips' mother.
On 29 March 2012, the couple's second daughter, Isla Elizabeth, was born at Gloucestershire Royal Hospital.
On 11 February 2020, Phillips and his wife confirmed that they had separated in 2019 and announced they were planning to divorce.
Lindsay Wallace

After his divorce, Phillips began a relationship with Lindsay Wallace in 2021, with whom he made his official debut as a couple at the Epsom Derby in June 2022.
Harriet Sperling

By June 2024, Phillips had introduced his partner, NHS paediatric nurse and freelance writer Harriet Sperling (née Sanders; born 1980), to King Charles III and Queen Camilla.



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
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

:hasDeathYear a owl:AnnotationProperty .

:hasMarriageYear a owl:AnnotationProperty .

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

:hasChild a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:inverseOf :isChildOf .

:isAncestorOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation .

:isSiblingOf a owl:ObjectProperty,
        owl:SymmetricProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isBloodrelationOf ;
    owl:propertyChainAxiom ( :hasParent :isParentOf ) .

:isSisterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf .

:hasParent a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Person ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:equivalentProperty :isChildOf ;
    owl:inverseOf :isParentOf .

:Sex a owl:Class ;
    rdfs:subClassOf :DomainEntity ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Female :Male ) ] .

:isChildOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:propertyDisjointWith :isSisterOf .

:Man a owl:Class ;
    owl:disjointWith :Sex,
        :Woman ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Male ] ) ] .

:Woman a owl:Class ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Female ] ) ] .

:isParentOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:propertyDisjointWith :isSisterOf .

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



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (6646e1d4-094f-48d5-8f37-01bf2914b24d)
 Call ID: 6646e1d4-094f-48d5-8f37-01bf2914b24d
  Args:
    type: :Man
    source: Peter_Mark_Andrew_Phillips
  AssignClass (3a5cf813-6e2a-43a2-ae07-8fbf4e841062)
 Call ID: 3a5cf813-6e2a-43a2-ae07-8fbf4e841062
  Args:
    type: :Woman
    source: Anne_Princess_Royal
  AssignClass (28047754-9510-4998-8cb3-c71bba7ff835)
 Call ID: 28047754-9510-4998-8cb3-c71bba7ff835
  Args:
    type: :Man
    source: Mark_Phillips
  AssignClass (508d929e-78dd-4b5b-ae3a-3b893d651d38)
 Call ID: 508d929e-78dd-4b5b-ae3a-3b893d651d38
  Args:
    type: :Woman
    source: Queen_Elizabeth_II
  AssignClass (bbbc034d-add7-40ad-8154-d152ca75ac70)
 Call ID: bbbc034d-add7-40ad-8154-d152ca75ac70
  Args:
    type: :Man
    source: Prince_Philip
  AssignClass (f9bea4f4-a499-404e-98b3-f8c178841eab)
 Call ID: f9bea4f4-a499-404e-98b3-f8c178841eab
  Args:
    type: :Woman
    source: Zara_Tindall
  AssignClass (bd5218e2-ad2c-4dc2-824d-39dbc5811a94)
 Call ID: bd5218e2-ad2c-4dc2-824d-39dbc5811a94
  Args:
    type: :Woman
    source: Felicity_Wade
  AssignClass (6cdfd7cb-0010-49ff-a0f8-face5dbbd2c7)
 Call ID: 6cdfd7cb-0010-49ff-a0f8-face5dbbd2c7
  Args:
    type: :Woman
    source: Stephanie_Phillips
  AssignClass (9a8522b0-7bd9-4b3e-bf11-b0e358967e11)
 Call ID: 9a8522b0-7bd9-4b3e-bf11-b0e358967e11
  Args:
    type: :Woman
    source: Heather_Tonkin
  AssignClass (b296049e-76cc-4d06-b75e-36ffd46dbe20)
 Call ID: b296049e-76cc-4d06-b75e-36ffd46dbe20
  Args:
    type: :Woman
    source: Sandy_Pflueger
  AssignClass (e635f602-2715-4b7d-97b5-ea717e6ca119)
 Call ID: e635f602-2715-4b7d-97b5-ea717e6ca119
  Args:
    type: :Woman
    source: Autumn_Kelly
  AssignClass (fb6e7a77-d67b-4e2b-a382-03930ee6cdf2)
 Call ID: fb6e7a77-d67b-4e2b-a382-03930ee6cdf2
  Args:
    type: :Woman
    source: Savannah_Anne_Kathleen
  AssignClass (8770104c-82fc-4345-b48d-b30572914a7c)
 Call ID: 8770104c-82fc-4345-b48d-b30572914a7c
  Args:
    type: :Woman
    source: Isla_Elizabeth
  AssignClass (af9e45cf-ef85-4112-a4a9-f1fdc334031a)
 Call ID: af9e45cf-ef85-4112-a4a9-f1fdc334031a
  Args:
    type: :Man
    source: King_Charles_III
  AssignClass (3ac0cf81-9aa6-4bd6-b87f-41bb3d07630a)
 Call ID: 3ac0cf81-9aa6-4bd6-b87f-41bb3d07630a
  Args:
    type: :Woman
    source: Lindsay_Wallace
  AssignClass (c8cb5e09-549a-488a-b9a0-bdd44e3634b0)
 Call ID: c8cb5e09-549a-488a-b9a0-bdd44e3634b0
  Args:
    type: :Woman
    source: Harriet_Sperling
  AddTriple (0ee2dc11-a8bf-4e96-ae16-8d853c9c49dd)
 Call ID: 0ee2dc11-a8bf-4e96-ae16-8d853c9c49dd
  Args:
    target: Mark_Phillips
    relation: :hasFather
    source: Peter_Mark_Andrew_Phillips
  AddTriple (51f66875-ca67-43ee-b61f-5d1f1e430561)
 Call ID: 51f66875-ca67-43ee-b61f-5d1f1e430561
  Args:
    source: Peter_Mark_Andrew_Phillips
    target: Anne_Princess_Royal
    relation: :hasMother
  AddTriple (c3a3700a-3320-49bc-a146-09d4b52de831)
 Call ID: c3a3700a-3320-49bc-a146-09d4b52de831
  Args:
    source: Zara_Tindall
    relation: :hasFather
    target: Mark_Phillips
  AddTriple (3f1b6798-c153-4e23-98aa-fd91b31e4a87)
 Call ID: 3f1b6798-c153-4e23-98aa-fd91b31e4a87
  Args:
    target: Anne_Princess_Royal
    relation: :hasMother
    source: Zara_Tindall
  AddTriple (8e86ed93-b4ed-400b-a93b-a000b3ac8c38)
 Call ID: 8e86ed93-b4ed-400b-a93b-a000b3ac8c38
  Args:
    relation: :hasFather
    target: Mark_Phillips
    source: Felicity_Wade
  AddTriple (4cb47414-01a3-4f71-8d3b-e389e227d82b)
 Call ID: 4cb47414-01a3-4f71-8d3b-e389e227d82b
  Args:
    relation: :hasMother
    target: Heather_Tonkin
    source: Felicity_Wade
  AddTriple (eec8cac4-e32a-4ae2-a1ba-8537a075843c)
 Call ID: eec8cac4-e32a-4ae2-a1ba-8537a075843c
  Args:
    target: Mark_Phillips
    relation: :hasFather
    source: Stephanie_Phillips
  AddTriple (414fda8f-028f-4468-8214-b12fd33e465b)
 Call ID: 414fda8f-028f-4468-8214-b12fd33e465b
  Args:
    source: Stephanie_Phillips
    relation: :hasMother
    target: Sandy_Pflueger
  AddTriple (c1f4f5e3-3b0a-4d33-b6e9-3aa40ca0d7b2)
 Call ID: c1f4f5e3-3b0a-4d33-b6e9-3aa40ca0d7b2
  Args:
    source: Savannah_Anne_Kathleen
    target: Peter_Mark_Andrew_Phillips
    relation: :hasFather
  AddTriple (378125dd-b07b-4166-8b59-fa4e4a4a5667)
 Call ID: 378125dd-b07b-4166-8b59-fa4e4a4a5667
  Args:
    source: Savannah_Anne_Kathleen
    relation: :hasMother
    target: Autumn_Kelly
  AddTriple (490cef8f-254a-4ce6-b781-3ad8e21ce9f0)
 Call ID: 490cef8f-254a-4ce6-b781-3ad8e21ce9f0
  Args:
    source: Isla_Elizabeth
    relation: :hasFather
    target: Peter_Mark_Andrew_Phillips
  AddTriple (42267017-f4d4-45a6-92d8-ece06587aa5e)
 Call ID: 42267017-f4d4-45a6-92d8-ece06587aa5e
  Args:
    source: Isla_Elizabeth
    target: Autumn_Kelly
    relation: :hasMother
  AddLiteral (b99d071e-a398-4e08-b949-dd2cefa76cbe)
 Call ID: b99d071e-a398-4e08-b949-dd2cefa76cbe
  Args:
    relation: :hasBirthYear
    literal_type: xsd:string
    literal_value: 1977
    source: Peter_Mark_Andrew_Phillips
  AddLiteral (fcdfe348-79a6-4fad-ad01-64a92d30c477)
 Call ID: fcdfe348-79a6-4fad-ad01-64a92d30c477
  Args:
    source: Zara_Tindall
    literal_value: 1981
    relation: :hasBirthYear
    literal_type: xsd:string
  AddLiteral (6c24fe89-d691-46ea-bc26-cfed09005c5a)
 Call ID: 6c24fe89-d691-46ea-bc26-cfed09005c5a
  Args:
    source: Felicity_Wade
    literal_type: xsd:string
    relation: :hasBirthYear
    literal_value: 1985
  AddLiteral (3a469d85-137d-4773-a28b-db2240e3dc01)
 Call ID: 3a469d85-137d-4773-a28b-db2240e3dc01
  Args:
    literal_type: xsd:string
    relation: :hasBirthYear
    literal_value: 1997
    source: Stephanie_Phillips
  AddLiteral (ac15ca84-6dfe-4ded-a96a-39784fb89980)
 Call ID: ac15ca84-6dfe-4ded-a96a-39784fb89980
  Args:
    source: Peter_Mark_Andrew_Phillips
    literal_value: 2008
    relation: :hasMarriageYear
    literal_type: xsd:string
  AddTriple (bd477063-22b5-4cfc-9512-7324dd360dc4)
 Call ID: bd477063-22b5-4cfc-9512-7324dd360dc4
  Args:
    relation: :hasRelation
    target: Autumn_Kelly
    source: Peter_Mark_Andrew_Phillips
  AddTriple (135b11e5-ebbf-41bc-b358-db0a980de6b7)
 Call ID: 135b11e5-ebbf-41bc-b358-db0a980de6b7
  Args:
    source: Peter_Mark_Andrew_Phillips
    relation: :hasRelation
    target: Lindsay_Wallace
  AddTriple (6cc1dff8-6c3a-493f-92f9-dc2daf5fbe09)
 Call ID: 6cc1dff8-6c3a-493f-92f9-dc2daf5fbe09
  Args:
    source: Peter_Mark_Andrew_Phillips
    target: Harriet_Sperling
    relation: :hasRelation
  Finish (08e16531-f966-4aba-8ce7-8d9ca6aaf389)
 Call ID: 08e16531-f966-4aba-8ce7-8d9ca6aaf389
  Args: