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
India Amanda Caroline Hicks (born 5 September 1967) is a British designer, writer, businesswoman and former fashion model.
After graduating from the New England School of Photography, Hicks became an interior designer and a model for Ralph Lauren, among others.
She moved to the Bahamas in 1996, where she published books, promoted home and beauty products, and introduced a line of jewellery.
Hicks travels frequently to disaster sites in her role with the non-profit organisation Global Empowerment Mission.
A daughter of Lady Pamela Hicks, she is a maternal descendant of the House of Mountbatten and a relative of the British royal family.
Early life

India Amanda Caroline Hicks was born on 5 September 1967 in Lambeth, London.
Hicks is the third child of Lady Pamela Mountbatten and David Nightingale Hicks.
Her mother was a lady-in-waiting to Queen Elizabeth II and her father was a famous interior designer.
She is the granddaughter of the 1st Earl and Countess Mountbatten of Burma and the second cousin and goddaughter of Charles III.
Hicks grew up in Oxfordshire, England.
Hicks was exposed to design at an early age through her father and brother, who were both architects.
The 11-year-old Hicks was on holiday in Ireland in 1979 when her grandfather was killed by a bomb planted on his boat.
In 1981, she served as bridesmaid to Lady Diana Spencer at her wedding to Prince Charles.
Hicks went to boarding school in Scotland at Gordonstoun, from which she was expelled for having boys in her room.
She then backpacked across India.
Hicks moved to Boston, Massachusetts at age 18 to study photography at the New England School of Photography, where she graduated in 1990.
Career

After graduating college, Hicks' father introduced her to Emilio Pucci in Florence, Italy, where she modelled swimsuits.
Hicks moved to the Bahamas in 1996.
In the Bahamas, Hicks restored homes, invested and remodelled a hotel, and published several books on design and lifestyle.
Her first book called Island Life was a design book with photographs of Hibiscus Hill, a house she designed.
Hicks also started a boutique shop in the Bahamas called the Sugar Mill Trading Company with business partner Linda Griffin.
From 2005 to 2014, Hicks worked with Crabtree & Evelyn as a spokeswoman and creative consultant for home and skincare products.
The company created the India Hicks Island Living and India Hicks Island Night lines of soaps, candles, and perfumes.
In 2008, Hicks co-hosted the second season of the Bravo interior design show Top Design in Los Angeles, California.
She introduced her own line of jewellery in 2011.
Hicks also became a public commentator on events surrounding the royal family and the 2011 wedding of Prince William and Catherine Middleton.
In 2015, Hicks created an e-commerce venture called India Hicks Inc. with partners Nicholas Keuper and HauteLook.
Hicks also worked with the Home Shopping Network on a line of bedding products called India Hicks Island Living.
Personal life

Hicks met her husband David Flint Wood as a child.
He was previously in a relationship with her cousin, Lady Helen Windsor and then Susannah Constantine, a fashion journalist and the former girlfriend of her other cousin, David Armstrong-Jones, 2nd Earl of Snowdon.
India and David re-connected as adults during a holiday in the Bahamas.
The couple have a house, "America Farm" in Ewelme, Oxfordshire, built on land that Hicks had inherited and replacing two redundant farm workers' cottages.
Hicks' book about the project, India Hicks:
The Story of Four Houses – A Slice of England, was published by  Rizzoli International Publications in 2018.
Hicks has competed in several marathons.
In 2020, Hicks pleaded guilty at Uxbridge Magistrates' Court to shoplifting a coat and was ordered to pay costs and a victim surcharge.
Her spokesperson stated: "The court accepted that at the time of taking the coat, India had simply been absent-minded and hadn't intended to leave without paying for it".



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
  AssignClass (4da8bc9d-0353-4298-bd9d-febe96bf9b34)
 Call ID: 4da8bc9d-0353-4298-bd9d-febe96bf9b34
  Args:
    type: :Person
    source: India_Hicks
  AssignClass (2f678997-376f-4017-833d-601db074e2be)
 Call ID: 2f678997-376f-4017-833d-601db074e2be
  Args:
    type: :Woman
    source: India_Hicks
  AssignClass (5dcf9fd1-7cbf-49af-9b59-cbd76d828b01)
 Call ID: 5dcf9fd1-7cbf-49af-9b59-cbd76d828b01
  Args:
    source: Lady_Pamela_Mountbatten
    type: :Person
  AssignClass (e6d71ec7-805e-4c07-bb38-dc77a01d5e51)
 Call ID: e6d71ec7-805e-4c07-bb38-dc77a01d5e51
  Args:
    source: Lady_Pamela_Mountbatten
    type: :Woman
  AssignClass (c764e8a4-d1d1-45d9-abf9-cc6a56fc0c54)
 Call ID: c764e8a4-d1d1-45d9-abf9-cc6a56fc0c54
  Args:
    source: David_Nightingale_Hicks
    type: :Person
  AssignClass (36b24dec-4294-47f4-8e0c-ccb85cb54761)
 Call ID: 36b24dec-4294-47f4-8e0c-ccb85cb54761
  Args:
    source: David_Nightingale_Hicks
    type: :Man
  AddTriple (1055e7fa-06e9-4e65-acb4-c59b06004f97)
 Call ID: 1055e7fa-06e9-4e65-acb4-c59b06004f97
  Args:
    source: India_Hicks
    target: Lady_Pamela_Mountbatten
    relation: :hasMother
  AddTriple (8b57409a-6234-48bf-87db-fee1638cb539)
 Call ID: 8b57409a-6234-48bf-87db-fee1638cb539
  Args:
    source: India_Hicks
    relation: :hasFather
    target: David_Nightingale_Hicks
  AddLiteral (03c967db-39dc-4560-ac0b-5ff977ca4c0d)
 Call ID: 03c967db-39dc-4560-ac0b-5ff977ca4c0d
  Args:
    literal_type: xsd:integer
    literal_value: 1967
    source: India_Hicks
    relation: :hasBirthYear
  AssignClass (78107fad-90db-4cef-a66f-5d0a18174b20)
 Call ID: 78107fad-90db-4cef-a66f-5d0a18174b20
  Args:
    source: David_Flint_Wood
    type: :Person
  AssignClass (7bddf910-2af9-4046-a27c-3d3489acf249)
 Call ID: 7bddf910-2af9-4046-a27c-3d3489acf249
  Args:
    type: :Man
    source: David_Flint_Wood
  AddTriple (0fc47930-4d4a-4035-b3b9-348ba79ae8ed)
 Call ID: 0fc47930-4d4a-4035-b3b9-348ba79ae8ed
  Args:
    target: David_Flint_Wood
    relation: :hasRelation
    source: India_Hicks
  Finish (a79f1bfa-ed82-4510-89a2-061e02b4989b)
 Call ID: a79f1bfa-ed82-4510-89a2-061e02b4989b
  Args: