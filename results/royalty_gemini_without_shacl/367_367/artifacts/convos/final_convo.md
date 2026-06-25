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
Princess Alexandra of Hanover (Alexandra Louise Marie Olga Elisabeth Therese Vera; 29 September 1882 – 30 August 1963) was Grand Duchess of Mecklenburg-Schwerin as the wife of Grand Duke Frederick Francis IV from their marriage on 7 June 1904 until the Grand Duke abdicated on 14 November 1918, following the German Revolution of 1918.
Alexandra was the daughter of Ernest Augustus, Crown Prince of Hanover, and Princess Thyra of Denmark.
Family

Alexandra was the second eldest daughter and third child of Ernest Augustus, Crown Prince of Hanover (1845–1923) and Princess Thyra of Denmark (1853–1933), the youngest daughter of Christian IX of Denmark (1818–1906) and Louise of Hesse-Kassel (1817–1898).
Alexandra was a great-great-granddaughter of George III of the United Kingdom (1738–1820) and Charlotte of Mecklenburg-Strelitz (1744–1818).
Marriage and issue

Alexandra married on 7 June 1904 in Gmunden, Austria-Hungary to Frederick Francis IV, Grand Duke of Mecklenburg-Schwerin (1882–1945), son of Frederick Francis III, Grand Duke of Mecklenburg-Schwerin and his wife Grand Duchess Anastasia Mikhailovna of Russia.
The bridegroom gave Alexandra a diamond and aquamarine tiara by Faberge.
Alexandra and Frederick Francis had five children:


Grand Duchess of Mecklenburg-Schwerin

In 1913, a fire broke out at Schwerin Castle while the Grand Duke and Duchess were dining there with guests.
Everyone was able to make it out safely, although the grand ducal couple had to apparently rush through flying sparks when making their escape.
Later life

After the Grand Duke's forced abdication in 1918, the family briefly went into exile in Denmark, the native country of Alexandra's mother, Princess Thyra.
After his death in 1945, the widowed Alexandra retired to the Glucksburg family estates in Schleswig-Holstein.



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
  AssignClass (8934a872-bc14-4348-b98a-600640bf5d9d)
 Call ID: 8934a872-bc14-4348-b98a-600640bf5d9d
  Args:
    source: Alexandra_of_Hanover
    type: :Woman
  AssignClass (9c9b40e4-8cc2-43f5-b337-c9aa29769eae)
 Call ID: 9c9b40e4-8cc2-43f5-b337-c9aa29769eae
  Args:
    type: :Person
    source: Alexandra_of_Hanover
  AddLiteral (dae9bc28-177f-421a-96b9-2489c7374f84)
 Call ID: dae9bc28-177f-421a-96b9-2489c7374f84
  Args:
    source: Alexandra_of_Hanover
    literal_value: 1882
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (c9648c6f-7810-489a-bf20-2bc79782bc29)
 Call ID: c9648c6f-7810-489a-bf20-2bc79782bc29
  Args:
    literal_type: xsd:integer
    literal_value: 1963
    source: Alexandra_of_Hanover
    relation: :hasDeathYear
  AssignClass (feec5210-282d-4df1-b8ad-7c5a78a831bb)
 Call ID: feec5210-282d-4df1-b8ad-7c5a78a831bb
  Args:
    source: Ernest_Augustus_of_Hanover
    type: :Man
  AssignClass (ed1d4582-da57-4c80-a03b-01a00ead2ab9)
 Call ID: ed1d4582-da57-4c80-a03b-01a00ead2ab9
  Args:
    source: Ernest_Augustus_of_Hanover
    type: :Person
  AddLiteral (7f4aefd2-6f16-40cf-ad91-a10cd6475927)
 Call ID: 7f4aefd2-6f16-40cf-ad91-a10cd6475927
  Args:
    literal_value: 1845
    source: Ernest_Augustus_of_Hanover
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (6460ee27-8111-4c3f-8908-0e53d904ffdc)
 Call ID: 6460ee27-8111-4c3f-8908-0e53d904ffdc
  Args:
    relation: :hasDeathYear
    source: Ernest_Augustus_of_Hanover
    literal_value: 1923
    literal_type: xsd:integer
  AssignClass (56e04ced-cf82-4bec-8801-af6599967fb5)
 Call ID: 56e04ced-cf82-4bec-8801-af6599967fb5
  Args:
    source: Thyra_of_Denmark
    type: :Woman
  AssignClass (22cd6720-2f74-47c4-a834-255437a8a31b)
 Call ID: 22cd6720-2f74-47c4-a834-255437a8a31b
  Args:
    source: Thyra_of_Denmark
    type: :Person
  AddLiteral (24a9abcb-03d1-4595-81c8-3b1be938a7b2)
 Call ID: 24a9abcb-03d1-4595-81c8-3b1be938a7b2
  Args:
    relation: :hasBirthYear
    literal_value: 1853
    source: Thyra_of_Denmark
    literal_type: xsd:integer
  AddLiteral (3ed482e5-163b-4fd2-b54a-3bd9c50bc5cb)
 Call ID: 3ed482e5-163b-4fd2-b54a-3bd9c50bc5cb
  Args:
    relation: :hasDeathYear
    source: Thyra_of_Denmark
    literal_value: 1933
    literal_type: xsd:integer
  AddTriple (139cb390-ad01-4e0d-ae41-35020393d124)
 Call ID: 139cb390-ad01-4e0d-ae41-35020393d124
  Args:
    relation: :hasFather
    target: Ernest_Augustus_of_Hanover
    source: Alexandra_of_Hanover
  AddTriple (7a13c46a-74b5-4fdc-89e1-704181636a56)
 Call ID: 7a13c46a-74b5-4fdc-89e1-704181636a56
  Args:
    source: Alexandra_of_Hanover
    relation: :hasMother
    target: Thyra_of_Denmark
  AssignClass (72ed845e-719d-4418-aa7e-a266cb5069e8)
 Call ID: 72ed845e-719d-4418-aa7e-a266cb5069e8
  Args:
    source: Christian_IX_of_Denmark
    type: :Man
  AssignClass (1d5d3b9b-3766-4162-8037-3d5332341b0c)
 Call ID: 1d5d3b9b-3766-4162-8037-3d5332341b0c
  Args:
    source: Christian_IX_of_Denmark
    type: :Person
  AddLiteral (8b54374f-3edc-4bfe-9060-3afa08c1142b)
 Call ID: 8b54374f-3edc-4bfe-9060-3afa08c1142b
  Args:
    literal_type: xsd:integer
    literal_value: 1818
    source: Christian_IX_of_Denmark
    relation: :hasBirthYear
  AddLiteral (71b25dc6-f764-4ad5-af07-36f43cd1b5e2)
 Call ID: 71b25dc6-f764-4ad5-af07-36f43cd1b5e2
  Args:
    relation: :hasDeathYear
    source: Christian_IX_of_Denmark
    literal_value: 1906
    literal_type: xsd:integer
  AssignClass (09ca3c03-7643-4d2e-818b-a8c7c2db7c4b)
 Call ID: 09ca3c03-7643-4d2e-818b-a8c7c2db7c4b
  Args:
    type: :Woman
    source: Louise_of_Hesse-Kassel
  AssignClass (bec692b2-291a-4932-be45-cfddc13c291c)
 Call ID: bec692b2-291a-4932-be45-cfddc13c291c
  Args:
    source: Louise_of_Hesse-Kassel
    type: :Person
  AddLiteral (a0db6080-0dc3-4b2c-94e2-e17837ba554d)
 Call ID: a0db6080-0dc3-4b2c-94e2-e17837ba554d
  Args:
    literal_type: xsd:integer
    source: Louise_of_Hesse-Kassel
    literal_value: 1817
    relation: :hasBirthYear
  AddLiteral (b0d7af4c-68e7-46ca-8fad-e21afe312704)
 Call ID: b0d7af4c-68e7-46ca-8fad-e21afe312704
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1898
    source: Louise_of_Hesse-Kassel
  AddTriple (763af266-7109-4e65-8fb0-f36c50537438)
 Call ID: 763af266-7109-4e65-8fb0-f36c50537438
  Args:
    relation: :hasFather
    target: Christian_IX_of_Denmark
    source: Thyra_of_Denmark
  AddTriple (7175649f-8636-4995-bf5a-3ce863b7f56f)
 Call ID: 7175649f-8636-4995-bf5a-3ce863b7f56f
  Args:
    target: Louise_of_Hesse-Kassel
    relation: :hasMother
    source: Thyra_of_Denmark
  AssignClass (a729c46f-def2-47d9-b017-6e08045960f1)
 Call ID: a729c46f-def2-47d9-b017-6e08045960f1
  Args:
    source: Frederick_Francis_IV_of_Mecklenburg-Schwerin
    type: :Man
  AssignClass (de58cf93-8a5b-4751-9871-79d5849c51d6)
 Call ID: de58cf93-8a5b-4751-9871-79d5849c51d6
  Args:
    type: :Person
    source: Frederick_Francis_IV_of_Mecklenburg-Schwerin
  AddLiteral (e4faeb2d-b695-4ea4-b398-a1d8254958b5)
 Call ID: e4faeb2d-b695-4ea4-b398-a1d8254958b5
  Args:
    source: Frederick_Francis_IV_of_Mecklenburg-Schwerin
    literal_value: 1882
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (285ec1c5-4109-49eb-857a-6f861977870e)
 Call ID: 285ec1c5-4109-49eb-857a-6f861977870e
  Args:
    literal_type: xsd:integer
    literal_value: 1945
    source: Frederick_Francis_IV_of_Mecklenburg-Schwerin
    relation: :hasDeathYear
  AddTriple (45e682da-dd08-4c6b-b925-42700e285e88)
 Call ID: 45e682da-dd08-4c6b-b925-42700e285e88
  Args:
    source: Alexandra_of_Hanover
    relation: :hasMarriageYear
    target: Frederick_Francis_IV_of_Mecklenburg-Schwerin
  AddLiteral (ef4958b7-f251-4d8f-8dd0-7f0e14564248)
 Call ID: ef4958b7-f251-4d8f-8dd0-7f0e14564248
  Args:
    literal_value: 1904
    source: Alexandra_of_Hanover
    relation: :hasMarriageYear
    literal_type: xsd:integer
  AssignClass (cebcb693-db57-46f1-9cc0-3cafbe5d6157)
 Call ID: cebcb693-db57-46f1-9cc0-3cafbe5d6157
  Args:
    type: :Man
    source: Frederick_Francis_III_of_Mecklenburg-Schwerin
  AssignClass (0fe7137a-02a8-4024-b618-7e1563eef376)
 Call ID: 0fe7137a-02a8-4024-b618-7e1563eef376
  Args:
    source: Frederick_Francis_III_of_Mecklenburg-Schwerin
    type: :Person
  AssignClass (5d82e68e-0cb9-4f15-91d9-fbdc37c0862f)
 Call ID: 5d82e68e-0cb9-4f15-91d9-fbdc37c0862f
  Args:
    source: Anastasia_Mikhailovna_of_Russia
    type: :Woman
  AssignClass (40064301-3da4-4bd7-bb40-7796d887105d)
 Call ID: 40064301-3da4-4bd7-bb40-7796d887105d
  Args:
    source: Anastasia_Mikhailovna_of_Russia
    type: :Person
  AddTriple (751c8387-7926-431e-9c76-5d329124ef77)
 Call ID: 751c8387-7926-431e-9c76-5d329124ef77
  Args:
    source: Frederick_Francis_IV_of_Mecklenburg-Schwerin
    target: Frederick_Francis_III_of_Mecklenburg-Schwerin
    relation: :hasFather
  AddTriple (3f631d50-cdcb-4e44-8044-dad33d5fdc75)
 Call ID: 3f631d50-cdcb-4e44-8044-dad33d5fdc75
  Args:
    relation: :hasMother
    target: Anastasia_Mikhailovna_of_Russia
    source: Frederick_Francis_IV_of_Mecklenburg-Schwerin
  AssignClass (a5498790-bd3a-472b-bcd2-01ec966d1d46)
 Call ID: a5498790-bd3a-472b-bcd2-01ec966d1d46
  Args:
    type: :Man
    source: George_III_of_the_United_Kingdom
  AssignClass (ee731ae6-aa3e-4f25-b7ba-9df33d58234a)
 Call ID: ee731ae6-aa3e-4f25-b7ba-9df33d58234a
  Args:
    source: George_III_of_the_United_Kingdom
    type: :Person
  AddLiteral (80e6d09a-535b-4436-a96d-857ca87abf41)
 Call ID: 80e6d09a-535b-4436-a96d-857ca87abf41
  Args:
    literal_type: xsd:integer
    literal_value: 1738
    source: George_III_of_the_United_Kingdom
    relation: :hasBirthYear
  AddLiteral (831cc49b-ba54-47e0-bdbd-6357ab1fa3b3)
 Call ID: 831cc49b-ba54-47e0-bdbd-6357ab1fa3b3
  Args:
    literal_type: xsd:integer
    source: George_III_of_the_United_Kingdom
    literal_value: 1820
    relation: :hasDeathYear
  AssignClass (5ab2dedf-fcc7-4ce1-9f22-6cfddc704167)
 Call ID: 5ab2dedf-fcc7-4ce1-9f22-6cfddc704167
  Args:
    source: Charlotte_of_Mecklenburg-Strelitz
    type: :Woman
  AssignClass (2c6a8bc3-274d-4907-b064-e647fb16acea)
 Call ID: 2c6a8bc3-274d-4907-b064-e647fb16acea
  Args:
    type: :Person
    source: Charlotte_of_Mecklenburg-Strelitz
  AddLiteral (3815fa1e-332b-4b83-acb1-a53a84f78afd)
 Call ID: 3815fa1e-332b-4b83-acb1-a53a84f78afd
  Args:
    literal_value: 1744
    source: Charlotte_of_Mecklenburg-Strelitz
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (2a2a0446-6e81-4eb8-b97f-e1c4565007d9)
 Call ID: 2a2a0446-6e81-4eb8-b97f-e1c4565007d9
  Args:
    literal_type: xsd:integer
    literal_value: 1818
    source: Charlotte_of_Mecklenburg-Strelitz
    relation: :hasDeathYear
  Finish (530365fd-8a26-45bc-9f36-b89b7f93e9fe)
 Call ID: 530365fd-8a26-45bc-9f36-b89b7f93e9fe
  Args: