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
  AssignClass (9a81eeac-e3f8-4717-adf9-682086c1722b)
 Call ID: 9a81eeac-e3f8-4717-adf9-682086c1722b
  Args:
    type: :Woman
    source: Lady_Margarita_Armstrong-Jones
  AssignClass (fd4c83e6-3301-4ede-9584-84225a9db205)
 Call ID: fd4c83e6-3301-4ede-9584-84225a9db205
  Args:
    type: :Person
    source: Lady_Margarita_Armstrong-Jones
  AddLiteral (fa5faabe-4fb8-4208-83b8-7992db8fc590)
 Call ID: fa5faabe-4fb8-4208-83b8-7992db8fc590
  Args:
    relation: :hasBirthYear
    source: Lady_Margarita_Armstrong-Jones
    literal_type: xsd:integer
    literal_value: 2002
  AssignClass (bc9b710e-6aa0-4d7c-8c55-5158c48e45c1)
 Call ID: bc9b710e-6aa0-4d7c-8c55-5158c48e45c1
  Args:
    type: :Man
    source: David_Armstrong-Jones
  AssignClass (ed0ed9c0-b1e6-4353-acf6-41504c47fb9a)
 Call ID: ed0ed9c0-b1e6-4353-acf6-41504c47fb9a
  Args:
    type: :Person
    source: David_Armstrong-Jones
  AssignClass (61274107-52f8-407f-b0c1-1a7267039277)
 Call ID: 61274107-52f8-407f-b0c1-1a7267039277
  Args:
    type: :Woman
    source: Serena_Stanhope
  AssignClass (ab4c6ad0-7ea1-45d7-8bcd-ab92a04a450c)
 Call ID: ab4c6ad0-7ea1-45d7-8bcd-ab92a04a450c
  Args:
    type: :Person
    source: Serena_Stanhope
  AddTriple (8f6b8a7e-e59d-45c2-bc2e-c01c53b95146)
 Call ID: 8f6b8a7e-e59d-45c2-bc2e-c01c53b95146
  Args:
    relation: :hasFather
    source: Lady_Margarita_Armstrong-Jones
    target: David_Armstrong-Jones
  AddTriple (aa7ba09e-06f4-4d7c-a26e-7d254f37b2f0)
 Call ID: aa7ba09e-06f4-4d7c-a26e-7d254f37b2f0
  Args:
    target: Serena_Stanhope
    relation: :hasMother
    source: Lady_Margarita_Armstrong-Jones
  AssignClass (872765ac-ad4e-4ba2-8b0f-cf82b607a206)
 Call ID: 872765ac-ad4e-4ba2-8b0f-cf82b607a206
  Args:
    type: :Woman
    source: Princess_Margaret
  AssignClass (4da81304-57b4-4dab-b776-2186345d1a69)
 Call ID: 4da81304-57b4-4dab-b776-2186345d1a69
  Args:
    type: :Person
    source: Princess_Margaret
  AssignClass (2132fafc-aa64-450b-a949-d1f3a8514553)
 Call ID: 2132fafc-aa64-450b-a949-d1f3a8514553
  Args:
    type: :Man
    source: Antony_Armstrong-Jones
  AssignClass (21054583-1a16-45ae-97c8-be92ce737dde)
 Call ID: 21054583-1a16-45ae-97c8-be92ce737dde
  Args:
    type: :Person
    source: Antony_Armstrong-Jones
  AddTriple (cf46ebf0-bb35-482f-aa1b-982f290476b8)
 Call ID: cf46ebf0-bb35-482f-aa1b-982f290476b8
  Args:
    target: Princess_Margaret
    relation: :hasMother
    source: David_Armstrong-Jones
  AddTriple (9499ee85-5209-4c59-85e8-5fc113b14158)
 Call ID: 9499ee85-5209-4c59-85e8-5fc113b14158
  Args:
    relation: :hasFather
    source: David_Armstrong-Jones
    target: Antony_Armstrong-Jones
  AssignClass (f546c5e7-68d8-4de9-8fe3-100afc11729f)
 Call ID: f546c5e7-68d8-4de9-8fe3-100afc11729f
  Args:
    type: :Man
    source: Charles_Stanhope
  AssignClass (e19f107e-0d92-4020-9487-a7e1acfcfb4a)
 Call ID: e19f107e-0d92-4020-9487-a7e1acfcfb4a
  Args:
    type: :Person
    source: Charles_Stanhope
  AddTriple (6588ca78-5614-4167-882b-fcac5b8bb5ce)
 Call ID: 6588ca78-5614-4167-882b-fcac5b8bb5ce
  Args:
    relation: :hasFather
    source: Serena_Stanhope
    target: Charles_Stanhope
  AssignClass (1cfd3c44-901b-4800-919c-b6dadae85a8c)
 Call ID: 1cfd3c44-901b-4800-919c-b6dadae85a8c
  Args:
    type: :Man
    source: Viscount_Linley
  AssignClass (b19c014b-0540-4476-8173-bd1b609b66f1)
 Call ID: b19c014b-0540-4476-8173-bd1b609b66f1
  Args:
    type: :Person
    source: Viscount_Linley
  AddTriple (4eda0200-123b-41e2-831c-d0eac5fb86fe)
 Call ID: 4eda0200-123b-41e2-831c-d0eac5fb86fe
  Args:
    source: Viscount_Linley
    relation: :isBrotherOf
    target: Lady_Margarita_Armstrong-Jones
  AssignClass (62d7d407-d5aa-4bc1-aab3-bc9f6ac2d30e)
 Call ID: 62d7d407-d5aa-4bc1-aab3-bc9f6ac2d30e
  Args:
    type: :Woman
    source: Lady_Sarah_Chatto
  AssignClass (56bd2e3f-93c4-423a-8f96-b35eef3d168f)
 Call ID: 56bd2e3f-93c4-423a-8f96-b35eef3d168f
  Args:
    type: :Person
    source: Lady_Sarah_Chatto
  AddTriple (fba43de1-8cea-4a03-ad52-af07f4bb5384)
 Call ID: fba43de1-8cea-4a03-ad52-af07f4bb5384
  Args:
    relation: :isSisterOf
    source: Lady_Sarah_Chatto
    target: David_Armstrong-Jones
  Finish (0ac407e3-c79a-4e20-9543-b6a489b7aa07)
 Call ID: 0ac407e3-c79a-4e20-9543-b6a489b7aa07
  Args: