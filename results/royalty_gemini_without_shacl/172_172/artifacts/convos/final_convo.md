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
Lady Margarita Elizabeth Rose Alleyne Armstrong-Jones (born 14 May 2002) is a member of the British royal family.
She is the granddaughter of Princess Margaret and the grandniece of Queen Elizabeth II.
Lady Margarita is a jewellery designer and the creator of the bespoke jewellery label Matita.
Early life and family

Lady Margarita was born The Honourable Margarita Armstrong-Jones on 14 May 2002 at Portland Hospital in London.
She is the daughter of David Armstrong-Jones, 2nd Earl of Snowdon, who was styled as Viscount Linley at the time of her birth, and The Honourable Serena Stanhope.
On her father's side, she is the granddaughter of Princess Margaret, Countess of Snowdon and Antony Armstrong-Jones, 1st Earl of Snowdon and a great-granddaughter of King George VI.
On her mother's side, she is the granddaughter of Charles Stanhope, 12th Earl of Harrington and a descendant of Charles II.
She was baptised Margarita Elizabeth Rose Alleyne, and was named after her grandmother and great-grandmother, Queen Elizabeth The Queen Mother.
Her father succeeded his father as the Earl of Snowdon in 2017, which entitled her to use the title Lady.
Lady Margarita's parents separated in 2020.
Education

Lady Margarita was first educated at Garden House School, a private school in the Royal Borough of Kensington and Chelsea before attending St Mary's School Ascot, a Catholic all-girls boarding school.
Lady Margarita took life drawing, pottery, and watercolour painting courses at a small art school in Oxford.
In September 2022, Lady Margarita enrolled as a student at La Haute École de Joaillerie in Paris to study jewellery design, stonesetting, and wax carving.
Public role and royal appearances

In 2008, she attended the wedding of Peter Phillips, son of the Princess Royal, to Autumn Kelly at St George's Chapel, Windsor and appeared with the royal family for photographs the following day.
That same year, she accompanied her aunt, Lady Sarah Chatto, to the 60th birthday brunch for Charles, Prince of Wales at the Goring Hotel.
In 2011, Lady Margarita served as a bridesmaid at the wedding of Prince William and Catherine Middleton alongside Lady Louise Windsor, Eliza Lopes, and Grace van Cutsem.
Her elder brother, Viscount Linley, served as a page of honour to Elizabeth II.
On 30 March 2012, she attended a Service of Thanksgiving for the Queen Mother and Princess Margaret at St George's Chapel.
In 2018, Lady Margarita attended the wedding of Prince Harry and Meghan Markle and the wedding of Princess Eugenie and Jack Brooksbank.
Along with other members of the extended royal family, she attended the funeral of Prince Philip, Duke of Edinburgh in 2021 and the state funeral of Elizabeth II in 2022.
Lady Margarita was present at the Coronation of Charles III and Camilla on 6 May 2023.
Lady Margarita also attends the annual Trooping of the Colour, having accompanied Elizabeth II in the past.
She attends Christmas services with the royal family at St Mary Magdalene Church, Sandringham, and attended the annual Queen's Christmas Lunch at Buckingham Palace.
Career

Lady Margarita made her modelling debut in 2011 for Kids Company.
Personal life

In September 2022, Lady Margarita moved to Paris, renting a flat near the Bastille where she lives with her two best friends.



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
  AssignClass (2c7ae0cb-b2ff-4a03-a739-93be7d56e863)
 Call ID: 2c7ae0cb-b2ff-4a03-a739-93be7d56e863
  Args:
    type: :Woman
    source: Lady_Margarita_Armstrong-Jones
  AssignClass (085b7914-2b94-4111-910a-e8286c999da5)
 Call ID: 085b7914-2b94-4111-910a-e8286c999da5
  Args:
    type: :Person
    source: Lady_Margarita_Armstrong-Jones
  AddLiteral (a99760bb-d45d-4685-b009-a1b7c1d2aad4)
 Call ID: a99760bb-d45d-4685-b009-a1b7c1d2aad4
  Args:
    literal_type: xsd:integer
    source: Lady_Margarita_Armstrong-Jones
    relation: :hasBirthYear
    literal_value: 2002
  AssignClass (1d424300-66a5-4d99-a229-69728c9ecbd9)
 Call ID: 1d424300-66a5-4d99-a229-69728c9ecbd9
  Args:
    source: Princess_Margaret
    type: :Woman
  AssignClass (83fd6a6e-af0e-416a-87e1-bb1de8039c73)
 Call ID: 83fd6a6e-af0e-416a-87e1-bb1de8039c73
  Args:
    source: Princess_Margaret
    type: :Ancestor
  AssignClass (da055846-e9aa-441c-a4d8-34f9b7b118a4)
 Call ID: da055846-e9aa-441c-a4d8-34f9b7b118a4
  Args:
    type: :Person
    source: Princess_Margaret
  AssignClass (0d48fd8a-eb9c-45a4-84ce-1591be081f26)
 Call ID: 0d48fd8a-eb9c-45a4-84ce-1591be081f26
  Args:
    source: Queen_Elizabeth_II
    type: :Woman
  AssignClass (8d51f14c-97f8-4ca1-97fd-aec903c8bd4b)
 Call ID: 8d51f14c-97f8-4ca1-97fd-aec903c8bd4b
  Args:
    type: :Person
    source: Queen_Elizabeth_II
  AssignClass (0340d639-ce02-4da6-882d-7a9dff809c5b)
 Call ID: 0340d639-ce02-4da6-882d-7a9dff809c5b
  Args:
    source: David_Armstrong-Jones
    type: :Man
  AssignClass (a8302f1f-2e1e-4fe8-8df9-33229a9add1b)
 Call ID: a8302f1f-2e1e-4fe8-8df9-33229a9add1b
  Args:
    type: :Ancestor
    source: David_Armstrong-Jones
  AssignClass (b7b80546-1197-4dec-8c53-6ec5d8ee83bf)
 Call ID: b7b80546-1197-4dec-8c53-6ec5d8ee83bf
  Args:
    source: David_Armstrong-Jones
    type: :Person
  AssignClass (b0a30bee-31cd-4d96-b0a9-c078be24f1e8)
 Call ID: b0a30bee-31cd-4d96-b0a9-c078be24f1e8
  Args:
    type: :Woman
    source: Serena_Stanhope
  AssignClass (8f46e43f-d5c0-47b7-836b-4cbca757dfce)
 Call ID: 8f46e43f-d5c0-47b7-836b-4cbca757dfce
  Args:
    type: :Person
    source: Serena_Stanhope
  AssignClass (7d90630c-e21b-46c8-af01-49e63db6be80)
 Call ID: 7d90630c-e21b-46c8-af01-49e63db6be80
  Args:
    source: Antony_Armstrong-Jones
    type: :Man
  AssignClass (3e0e30da-f22b-43c0-865d-eafbabf5a965)
 Call ID: 3e0e30da-f22b-43c0-865d-eafbabf5a965
  Args:
    type: :Ancestor
    source: Antony_Armstrong-Jones
  AssignClass (bacf4396-f787-4ddb-bce6-496af3d73b1f)
 Call ID: bacf4396-f787-4ddb-bce6-496af3d73b1f
  Args:
    source: Antony_Armstrong-Jones
    type: :Person
  AssignClass (807b4310-0df0-4915-ae8d-9f87d8a2864c)
 Call ID: 807b4310-0df0-4915-ae8d-9f87d8a2864c
  Args:
    type: :Man
    source: King_George_VI
  AssignClass (4763c765-4894-4849-a137-7430cc3e7277)
 Call ID: 4763c765-4894-4849-a137-7430cc3e7277
  Args:
    source: King_George_VI
    type: :Ancestor
  AssignClass (7c1a70cb-3ce1-4a01-9a7b-a44667c1a447)
 Call ID: 7c1a70cb-3ce1-4a01-9a7b-a44667c1a447
  Args:
    type: :Person
    source: King_George_VI
  AssignClass (228f15f7-f5f5-4c4d-afe8-75c9b6be5b68)
 Call ID: 228f15f7-f5f5-4c4d-afe8-75c9b6be5b68
  Args:
    source: Charles_Stanhope
    type: :Man
  AssignClass (299dc6f0-6561-4b17-9647-f93cd08854e0)
 Call ID: 299dc6f0-6561-4b17-9647-f93cd08854e0
  Args:
    source: Charles_Stanhope
    type: :Ancestor
  AssignClass (d951a68b-5622-4fb5-a078-73d32017a957)
 Call ID: d951a68b-5622-4fb5-a078-73d32017a957
  Args:
    source: Charles_Stanhope
    type: :Person
  AssignClass (ecf1db13-e786-4a46-be0f-e4ff97239bc8)
 Call ID: ecf1db13-e786-4a46-be0f-e4ff97239bc8
  Args:
    source: Charles_II
    type: :Man
  AssignClass (a46809f3-e2cb-410c-ad2e-cf3093635f31)
 Call ID: a46809f3-e2cb-410c-ad2e-cf3093635f31
  Args:
    type: :Ancestor
    source: Charles_II
  AssignClass (07d2f3cd-a7fc-4a1b-9d69-45ef703c9a42)
 Call ID: 07d2f3cd-a7fc-4a1b-9d69-45ef703c9a42
  Args:
    type: :Person
    source: Charles_II
  AssignClass (2a72b68a-ab23-40ff-95a9-9c3120162016)
 Call ID: 2a72b68a-ab23-40ff-95a9-9c3120162016
  Args:
    type: :Woman
    source: Queen_Elizabeth_The_Queen_Mother
  AssignClass (4df7d50e-05b2-4f19-bbfc-51a28fd5d440)
 Call ID: 4df7d50e-05b2-4f19-bbfc-51a28fd5d440
  Args:
    type: :Ancestor
    source: Queen_Elizabeth_The_Queen_Mother
  AssignClass (844d71e7-13d1-4359-af83-bf8b88675868)
 Call ID: 844d71e7-13d1-4359-af83-bf8b88675868
  Args:
    source: Queen_Elizabeth_The_Queen_Mother
    type: :Person
  AssignClass (2bc8d3c4-dc14-4204-8512-9d2706149b98)
 Call ID: 2bc8d3c4-dc14-4204-8512-9d2706149b98
  Args:
    type: :Man
    source: Viscount_Linley_brother
  AssignClass (0b905e45-11af-496c-abe4-ce6ea3475a36)
 Call ID: 0b905e45-11af-496c-abe4-ce6ea3475a36
  Args:
    type: :Person
    source: Viscount_Linley_brother
  AssignClass (6101c66e-529d-4c19-8d30-e24f48a1309e)
 Call ID: 6101c66e-529d-4c19-8d30-e24f48a1309e
  Args:
    source: Lady_Sarah_Chatto
    type: :Woman
  AssignClass (1f593519-91bd-4bc4-b65f-480b267054c7)
 Call ID: 1f593519-91bd-4bc4-b65f-480b267054c7
  Args:
    source: Lady_Sarah_Chatto
    type: :Person
  AddTriple (f76938ca-0f40-4b69-8147-b06ac8a7f07e)
 Call ID: f76938ca-0f40-4b69-8147-b06ac8a7f07e
  Args:
    target: David_Armstrong-Jones
    relation: :hasFather
    source: Lady_Margarita_Armstrong-Jones
  AddTriple (f054c983-8da7-4880-bd08-ca67cc25b7f6)
 Call ID: f054c983-8da7-4880-bd08-ca67cc25b7f6
  Args:
    relation: :hasMother
    source: Lady_Margarita_Armstrong-Jones
    target: Serena_Stanhope
  AddTriple (2678c082-cecd-44da-8b02-eee9d736503a)
 Call ID: 2678c082-cecd-44da-8b02-eee9d736503a
  Args:
    target: Antony_Armstrong-Jones
    source: David_Armstrong-Jones
    relation: :hasFather
  AddTriple (49eb4f24-b156-4e09-bccc-349f68dd3814)
 Call ID: 49eb4f24-b156-4e09-bccc-349f68dd3814
  Args:
    source: David_Armstrong-Jones
    relation: :hasMother
    target: Princess_Margaret
  AddTriple (b46245d2-f204-4e21-a4ec-b68ae2bf3425)
 Call ID: b46245d2-f204-4e21-a4ec-b68ae2bf3425
  Args:
    target: King_George_VI
    relation: :hasFather
    source: Princess_Margaret
  AddTriple (b1bb057c-6e1f-4b46-8f29-e1471cb34ee8)
 Call ID: b1bb057c-6e1f-4b46-8f29-e1471cb34ee8
  Args:
    relation: :hasMother
    source: Princess_Margaret
    target: Queen_Elizabeth_The_Queen_Mother
  AddTriple (c0600141-1016-40ec-993a-e135392c791e)
 Call ID: c0600141-1016-40ec-993a-e135392c791e
  Args:
    source: Lady_Margarita_Armstrong-Jones
    relation: :hasFather
    target: Viscount_Linley_brother
  AddTriple (786afa45-dd4c-4a0a-8715-8d284bed5090)
 Call ID: 786afa45-dd4c-4a0a-8715-8d284bed5090
  Args:
    target: Lady_Margarita_Armstrong-Jones
    relation: :hasSister
    source: Viscount_Linley_brother
  AddTriple (a09b7d86-3bd3-40bc-8906-d0a7fe57df79)
 Call ID: a09b7d86-3bd3-40bc-8906-d0a7fe57df79
  Args:
    source: Charles_Stanhope
    relation: :hasFather
    target: Charles_II
  Finish (e3ab1eb7-7de3-4c66-a04d-7ba6400e9de4)
 Call ID: e3ab1eb7-7de3-4c66-a04d-7ba6400e9de4
  Args: