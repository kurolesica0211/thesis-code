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
  AssignClass (e1b9a3ad-a349-45e3-bdd3-9225c3a74e3e)
 Call ID: e1b9a3ad-a349-45e3-bdd3-9225c3a74e3e
  Args:
    type: :Woman
    source: LadyMargaritaArmstrong-Jones
  AssignClass (26e1f46a-4be4-4e1e-880d-462386f71cc9)
 Call ID: 26e1f46a-4be4-4e1e-880d-462386f71cc9
  Args:
    type: :Person
    source: LadyMargaritaArmstrong-Jones
  AddLiteral (187a002d-d659-4fcf-87cd-e4998f0f2c2c)
 Call ID: 187a002d-d659-4fcf-87cd-e4998f0f2c2c
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 2002
    source: LadyMargaritaArmstrong-Jones
  AssignClass (27731539-f34e-4f86-9da7-f15763a81bcf)
 Call ID: 27731539-f34e-4f86-9da7-f15763a81bcf
  Args:
    type: :Woman
    source: PrincessMargaret
  AssignClass (a0ea36f3-0fd5-4301-9209-78beefa42a08)
 Call ID: a0ea36f3-0fd5-4301-9209-78beefa42a08
  Args:
    type: :Ancestor
    source: PrincessMargaret
  AssignClass (2156664b-9bc7-40cb-8291-32f25bb06fe8)
 Call ID: 2156664b-9bc7-40cb-8291-32f25bb06fe8
  Args:
    type: :Person
    source: PrincessMargaret
  AssignClass (69960d01-6c72-4f46-b955-1cdc5a4c8557)
 Call ID: 69960d01-6c72-4f46-b955-1cdc5a4c8557
  Args:
    type: :Man
    source: DavidArmstrong-Jones
  AssignClass (e8a950b6-f18c-467c-8566-5a790db9df97)
 Call ID: e8a950b6-f18c-467c-8566-5a790db9df97
  Args:
    type: :Ancestor
    source: DavidArmstrong-Jones
  AssignClass (302c2f4a-6780-4d15-9a8c-96a46fe06d64)
 Call ID: 302c2f4a-6780-4d15-9a8c-96a46fe06d64
  Args:
    type: :Person
    source: DavidArmstrong-Jones
  AssignClass (05bcf75a-1432-4f2a-96f0-252ee84681f7)
 Call ID: 05bcf75a-1432-4f2a-96f0-252ee84681f7
  Args:
    type: :Woman
    source: SerenaStanhope
  AssignClass (8b76a37c-3121-4653-9710-758f9f479f96)
 Call ID: 8b76a37c-3121-4653-9710-758f9f479f96
  Args:
    type: :Person
    source: SerenaStanhope
  AddTriple (b2cbaf3f-03a8-417f-9004-cc0a2b56da98)
 Call ID: b2cbaf3f-03a8-417f-9004-cc0a2b56da98
  Args:
    relation: :isDaughterOf
    target: DavidArmstrong-Jones
    source: LadyMargaritaArmstrong-Jones
  AddTriple (1f5734a0-5942-406e-a6fb-c69f844216c4)
 Call ID: 1f5734a0-5942-406e-a6fb-c69f844216c4
  Args:
    relation: :isDaughterOf
    source: LadyMargaritaArmstrong-Jones
    target: SerenaStanhope
  AddTriple (d82e228d-8339-43d9-9db4-26cc26330ee4)
 Call ID: d82e228d-8339-43d9-9db4-26cc26330ee4
  Args:
    relation: :isDaughterOf
    target: PrincessMargaret
    source: DavidArmstrong-Jones
  AssignClass (ab28fdd3-2c9b-4075-ae14-2020270adb88)
 Call ID: ab28fdd3-2c9b-4075-ae14-2020270adb88
  Args:
    type: :Man
    source: AntonyArmstrong-Jones
  AssignClass (ee91eb8f-0352-4dc5-aaca-e4f6fa11c62b)
 Call ID: ee91eb8f-0352-4dc5-aaca-e4f6fa11c62b
  Args:
    type: :Ancestor
    source: AntonyArmstrong-Jones
  AssignClass (b93f549d-3af2-45ee-9882-68caa6aa1074)
 Call ID: b93f549d-3af2-45ee-9882-68caa6aa1074
  Args:
    type: :Person
    source: AntonyArmstrong-Jones
  AddTriple (b0095aa1-b824-485a-8569-8b1992230bbb)
 Call ID: b0095aa1-b824-485a-8569-8b1992230bbb
  Args:
    relation: :isSonOf
    target: AntonyArmstrong-Jones
    source: DavidArmstrong-Jones
  AssignClass (8aa08937-e499-4cd3-8a07-6d0eefba84db)
 Call ID: 8aa08937-e499-4cd3-8a07-6d0eefba84db
  Args:
    type: :Man
    source: CharlesStanhope
  AssignClass (bd2a083f-37a2-4d82-90fa-3f5583383113)
 Call ID: bd2a083f-37a2-4d82-90fa-3f5583383113
  Args:
    type: :Ancestor
    source: CharlesStanhope
  AssignClass (588a7ae5-a229-4639-88f1-1b650f785d32)
 Call ID: 588a7ae5-a229-4639-88f1-1b650f785d32
  Args:
    type: :Person
    source: CharlesStanhope
  AddTriple (4ab1b349-65de-4858-866a-18ad2a0b02ef)
 Call ID: 4ab1b349-65de-4858-866a-18ad2a0b02ef
  Args:
    target: SerenaStanhope
    source: CharlesStanhope
    relation: :isFatherOf
  AssignClass (dfb848b6-4816-4ae6-9b6d-fa8f35f3409f)
 Call ID: dfb848b6-4816-4ae6-9b6d-fa8f35f3409f
  Args:
    type: :Woman
    source: LadySarahChatto
  AssignClass (76948b4b-7768-4573-8a1e-7f613bf7404d)
 Call ID: 76948b4b-7768-4573-8a1e-7f613bf7404d
  Args:
    type: :Person
    source: LadySarahChatto
  AddTriple (75c555ce-fffd-40f3-9988-2e1a4a470e2d)
 Call ID: 75c555ce-fffd-40f3-9988-2e1a4a470e2d
  Args:
    source: LadySarahChatto
    target: DavidArmstrong-Jones
    relation: :isSisterOf
  AssignClass (f38a289e-9f18-4656-a157-0ad05e78a582)
 Call ID: f38a289e-9f18-4656-a157-0ad05e78a582
  Args:
    type: :Man
    source: ViscountLinley
  AssignClass (c19c6741-ac8e-40d5-bc80-c2f2ead4b4ed)
 Call ID: c19c6741-ac8e-40d5-bc80-c2f2ead4b4ed
  Args:
    type: :Person
    source: ViscountLinley
  AddTriple (c75bde9c-2d27-4a4b-bfb5-69db73282d86)
 Call ID: c75bde9c-2d27-4a4b-bfb5-69db73282d86
  Args:
    relation: :isBrotherOf
    target: LadyMargaritaArmstrong-Jones
    source: ViscountLinley
  Finish (0e025fc4-27ea-4783-9f15-2697ed6a327e)
 Call ID: 0e025fc4-27ea-4783-9f15-2697ed6a327e
  Args: