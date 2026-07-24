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
  AssignClass (db21d1d1-09ee-4fb9-91eb-d8207f17a690)
 Call ID: db21d1d1-09ee-4fb9-91eb-d8207f17a690
  Args:
    type: :Woman
    source: :Princess_Alexandra_of_Hanover
  AssignClass (25b52bda-91c0-434e-8086-e9a5015e093b)
 Call ID: 25b52bda-91c0-434e-8086-e9a5015e093b
  Args:
    type: :Person
    source: :Princess_Alexandra_of_Hanover
  AddLiteral (b8fa1071-76f8-481c-903a-5c452b59cc7f)
 Call ID: b8fa1071-76f8-481c-903a-5c452b59cc7f
  Args:
    source: :Princess_Alexandra_of_Hanover
    literal_value: 1882
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (ef29bec1-6d25-479d-bf0f-ed45ef81b1aa)
 Call ID: ef29bec1-6d25-479d-bf0f-ed45ef81b1aa
  Args:
    relation: :hasDeathYear
    literal_value: 1963
    literal_type: xsd:integer
    source: :Princess_Alexandra_of_Hanover
  AssignClass (3709c8f1-23e1-4f09-904b-67e5e73f579b)
 Call ID: 3709c8f1-23e1-4f09-904b-67e5e73f579b
  Args:
    type: :Man
    source: :Ernest_Augustus_Crown_Prince_of_Hanover
  AssignClass (183c5ca2-a4b8-42fa-ae26-155e37a6f680)
 Call ID: 183c5ca2-a4b8-42fa-ae26-155e37a6f680
  Args:
    type: :Person
    source: :Ernest_Augustus_Crown_Prince_of_Hanover
  AddLiteral (46b7a55a-8d47-40d3-a30c-dbbb06d5f940)
 Call ID: 46b7a55a-8d47-40d3-a30c-dbbb06d5f940
  Args:
    relation: :hasBirthYear
    literal_value: 1845
    literal_type: xsd:integer
    source: :Ernest_Augustus_Crown_Prince_of_Hanover
  AddLiteral (02cabe47-19d8-4514-a341-ec043a01fba1)
 Call ID: 02cabe47-19d8-4514-a341-ec043a01fba1
  Args:
    source: :Ernest_Augustus_Crown_Prince_of_Hanover
    literal_value: 1923
    literal_type: xsd:integer
    relation: :hasDeathYear
  AssignClass (e84c6e7b-9374-4bc8-a1ce-43be42aa65c6)
 Call ID: e84c6e7b-9374-4bc8-a1ce-43be42aa65c6
  Args:
    type: :Woman
    source: :Princess_Thyra_of_Denmark
  AssignClass (fd125c2a-8ed8-415c-b67d-7ac1bf2ddb79)
 Call ID: fd125c2a-8ed8-415c-b67d-7ac1bf2ddb79
  Args:
    type: :Person
    source: :Princess_Thyra_of_Denmark
  AddLiteral (48c0d8d7-9c96-47bc-a095-99198f1144ce)
 Call ID: 48c0d8d7-9c96-47bc-a095-99198f1144ce
  Args:
    literal_value: 1853
    literal_type: xsd:integer
    source: :Princess_Thyra_of_Denmark
    relation: :hasBirthYear
  AddLiteral (531fb232-1da3-496d-8dab-715a58bb195b)
 Call ID: 531fb232-1da3-496d-8dab-715a58bb195b
  Args:
    literal_value: 1933
    literal_type: xsd:integer
    source: :Princess_Thyra_of_Denmark
    relation: :hasDeathYear
  AddTriple (83f672c2-4308-455a-98f8-5d26d8eed204)
 Call ID: 83f672c2-4308-455a-98f8-5d26d8eed204
  Args:
    relation: :hasFather
    target: :Ernest_Augustus_Crown_Prince_of_Hanover
    source: :Princess_Alexandra_of_Hanover
  AddTriple (8297d580-75e0-4d21-b5a3-02c7d66ceccb)
 Call ID: 8297d580-75e0-4d21-b5a3-02c7d66ceccb
  Args:
    source: :Princess_Alexandra_of_Hanover
    relation: :hasMother
    target: :Princess_Thyra_of_Denmark
  AssignClass (e9673b21-9338-49fe-a5bb-77b6c26b2c6a)
 Call ID: e9673b21-9338-49fe-a5bb-77b6c26b2c6a
  Args:
    type: :Man
    source: :Frederick_Francis_IV_Grand_Duke_of_Mecklenburg_Schwerin
  AssignClass (3de89d23-7dee-44b8-bce8-2a141a922297)
 Call ID: 3de89d23-7dee-44b8-bce8-2a141a922297
  Args:
    type: :Person
    source: :Frederick_Francis_IV_Grand_Duke_of_Mecklenburg_Schwerin
  AddLiteral (b30c1433-f983-4ec8-83c9-340a4d6c252d)
 Call ID: b30c1433-f983-4ec8-83c9-340a4d6c252d
  Args:
    source: :Frederick_Francis_IV_Grand_Duke_of_Mecklenburg_Schwerin
    literal_value: 1882
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (18cf29ac-2a38-4251-8775-59b488e50dd6)
 Call ID: 18cf29ac-2a38-4251-8775-59b488e50dd6
  Args:
    relation: :hasDeathYear
    literal_value: 1945
    literal_type: xsd:integer
    source: :Frederick_Francis_IV_Grand_Duke_of_Mecklenburg_Schwerin
  AddTriple (f0828550-1101-42d5-b375-1e83a7438199)
 Call ID: f0828550-1101-42d5-b375-1e83a7438199
  Args:
    relation: :hasRelation
    target: :Frederick_Francis_IV_Grand_Duke_of_Mecklenburg_Schwerin
    source: :Princess_Alexandra_of_Hanover
  AddLiteral (9d3416a9-8426-46d5-bdbe-146823570a03)
 Call ID: 9d3416a9-8426-46d5-bdbe-146823570a03
  Args:
    source: :Princess_Alexandra_of_Hanover
    literal_value: 1904
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AssignClass (96503810-c55a-4de8-89f7-9efaa594eb34)
 Call ID: 96503810-c55a-4de8-89f7-9efaa594eb34
  Args:
    type: :Man
    source: :Christian_IX_of_Denmark
  AssignClass (84f55f47-3560-4959-8c7a-31099bc088b1)
 Call ID: 84f55f47-3560-4959-8c7a-31099bc088b1
  Args:
    type: :Person
    source: :Christian_IX_of_Denmark
  AddLiteral (1d40c29d-7096-4bd5-ba41-63767acf4ac3)
 Call ID: 1d40c29d-7096-4bd5-ba41-63767acf4ac3
  Args:
    relation: :hasBirthYear
    source: :Christian_IX_of_Denmark
    literal_value: 1818
    literal_type: xsd:integer
  AddLiteral (b672cf72-57c1-418e-866e-cd63ef3a8c21)
 Call ID: b672cf72-57c1-418e-866e-cd63ef3a8c21
  Args:
    literal_value: 1906
    literal_type: xsd:integer
    source: :Christian_IX_of_Denmark
    relation: :hasDeathYear
  AssignClass (f5643b52-b17c-408b-8986-e2d97260fcfd)
 Call ID: f5643b52-b17c-408b-8986-e2d97260fcfd
  Args:
    type: :Woman
    source: :Louise_of_Hesse_Kassel
  AssignClass (4d0c0c59-cc43-4a8a-a6cf-c80a04fb14c0)
 Call ID: 4d0c0c59-cc43-4a8a-a6cf-c80a04fb14c0
  Args:
    type: :Person
    source: :Louise_of_Hesse_Kassel
  AddLiteral (3dabf008-0dc2-48ce-8287-89bda9e1ad2d)
 Call ID: 3dabf008-0dc2-48ce-8287-89bda9e1ad2d
  Args:
    source: :Louise_of_Hesse_Kassel
    literal_value: 1817
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (a3a0b51f-a359-44b0-8975-b60f801a9943)
 Call ID: a3a0b51f-a359-44b0-8975-b60f801a9943
  Args:
    source: :Louise_of_Hesse_Kassel
    literal_value: 1898
    literal_type: xsd:integer
    relation: :hasDeathYear
  AddTriple (48c1133e-09d6-4435-97d4-a334b90f22c9)
 Call ID: 48c1133e-09d6-4435-97d4-a334b90f22c9
  Args:
    relation: :hasFather
    target: :Christian_IX_of_Denmark
    source: :Princess_Thyra_of_Denmark
  AddTriple (d90c2e68-a799-4961-8aeb-be4c5e74153a)
 Call ID: d90c2e68-a799-4961-8aeb-be4c5e74153a
  Args:
    relation: :hasMother
    target: :Louise_of_Hesse_Kassel
    source: :Princess_Thyra_of_Denmark
  AssignClass (a8e37ad5-9c8d-4a99-b44e-5f896f6b7faa)
 Call ID: a8e37ad5-9c8d-4a99-b44e-5f896f6b7faa
  Args:
    type: :Man
    source: :George_III_of_the_United_Kingdom
  AssignClass (9f539e1a-66fa-4fe5-a557-dc5fa8634483)
 Call ID: 9f539e1a-66fa-4fe5-a557-dc5fa8634483
  Args:
    type: :Person
    source: :George_III_of_the_United_Kingdom
  AddLiteral (8784a1fd-5756-4ecc-a24b-2fa7a05c142f)
 Call ID: 8784a1fd-5756-4ecc-a24b-2fa7a05c142f
  Args:
    literal_value: 1738
    literal_type: xsd:integer
    source: :George_III_of_the_United_Kingdom
    relation: :hasBirthYear
  AddLiteral (bbbfdce7-c72b-413a-94d6-151faf0c205f)
 Call ID: bbbfdce7-c72b-413a-94d6-151faf0c205f
  Args:
    relation: :hasDeathYear
    source: :George_III_of_the_United_Kingdom
    literal_value: 1820
    literal_type: xsd:integer
  AssignClass (2cd64afc-255d-41cb-8d5b-b4a22cc6a9f3)
 Call ID: 2cd64afc-255d-41cb-8d5b-b4a22cc6a9f3
  Args:
    type: :Woman
    source: :Charlotte_of_Mecklenburg_Strelitz
  AssignClass (ac1d722c-8b2b-4405-9404-1e10349dbe53)
 Call ID: ac1d722c-8b2b-4405-9404-1e10349dbe53
  Args:
    type: :Person
    source: :Charlotte_of_Mecklenburg_Strelitz
  AddLiteral (0d32ccee-033d-4e81-a665-656488fb02eb)
 Call ID: 0d32ccee-033d-4e81-a665-656488fb02eb
  Args:
    literal_value: 1744
    literal_type: xsd:integer
    source: :Charlotte_of_Mecklenburg_Strelitz
    relation: :hasBirthYear
  AddLiteral (d8229f03-c724-4343-893f-bc0d747b3f4f)
 Call ID: d8229f03-c724-4343-893f-bc0d747b3f4f
  Args:
    source: :Charlotte_of_Mecklenburg_Strelitz
    literal_value: 1818
    literal_type: xsd:integer
    relation: :hasDeathYear
  AssignClass (129b9b43-a208-46fe-9e28-8d5adf80fc19)
 Call ID: 129b9b43-a208-46fe-9e28-8d5adf80fc19
  Args:
    type: :Man
    source: :Frederick_Francis_III_Grand_Duke_of_Mecklenburg_Schwerin
  AssignClass (9106043e-7d1c-48cf-87cc-323bda2b5b90)
 Call ID: 9106043e-7d1c-48cf-87cc-323bda2b5b90
  Args:
    type: :Person
    source: :Frederick_Francis_III_Grand_Duke_of_Mecklenburg_Schwerin
  AssignClass (f3324b14-5645-4a70-b75b-29a054bf5906)
 Call ID: f3324b14-5645-4a70-b75b-29a054bf5906
  Args:
    type: :Woman
    source: :Grand_Duchess_Anastasia_Mikhailovna_of_Russia
  AssignClass (702c8f0b-da2c-4b3e-85e7-a3e81ce6207b)
 Call ID: 702c8f0b-da2c-4b3e-85e7-a3e81ce6207b
  Args:
    type: :Person
    source: :Grand_Duchess_Anastasia_Mikhailovna_of_Russia
  AddTriple (c2612980-6044-4eb5-91d7-079023cef3e2)
 Call ID: c2612980-6044-4eb5-91d7-079023cef3e2
  Args:
    source: :Frederick_Francis_IV_Grand_Duke_of_Mecklenburg_Schwerin
    relation: :hasFather
    target: :Frederick_Francis_III_Grand_Duke_of_Mecklenburg_Schwerin
  AddTriple (8d1f07c9-2def-4fcc-8eea-0ec3d63b97c6)
 Call ID: 8d1f07c9-2def-4fcc-8eea-0ec3d63b97c6
  Args:
    target: :Grand_Duchess_Anastasia_Mikhailovna_of_Russia
    relation: :hasMother
    source: :Frederick_Francis_IV_Grand_Duke_of_Mecklenburg_Schwerin
  Finish (25c16f1c-9afe-44d7-a68c-e3307afd4926)
 Call ID: 25c16f1c-9afe-44d7-a68c-e3307afd4926
  Args: