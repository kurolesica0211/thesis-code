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
John Alexander Elphinstone, 17th Lord Elphinstone and 3rd Baron Elphinstone (22 March 1914 – 15 November 1975) was a British nobleman and serviceman during World War II.
He was a first cousin of Queen Elizabeth II.
He was a son of Sidney Elphinstone, 16th Lord Elphinstone, and Lady Mary Bowes-Lyon.
Andrew Charles Victor Elphinstone (the aide-de-camp to the Viceroy of India from 1941 to 1943) and the Hon.
Margaret Elphinstone, wife of writer Denys Rhodes.
His paternal grandparents were William Elphinstone, 15th Lord Elphinstone (the 1st Baron Elphinstone) and the former Lady Constance Euphemia Woronzow Murray (second daughter of Alexander Murray, 6th Earl of Dunmore).
He was a nephew of Queen Elizabeth
The Queen Mother and a first cousin of Queen Elizabeth II and Princess Margaret, Countess of Snowdon.
Lord Elphinstone served as president of the Scottish Association of Boys' Clubs, chairman of council of the Scottish branch of British Red Cross Society, and president of the Royal Zoological Society of Scotland.
Personal life

In 1970, during Manitoba's centennial, he was invited by the community of Elphinstone and gave a silver map case, which is today located at the Elphinstone post office, all named in his family's honor.



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
  AssignClass (e9de47a9-c248-423d-ac28-a5968d5409a5)
 Call ID: e9de47a9-c248-423d-ac28-a5968d5409a5
  Args:
    type: :Man
    source: John Alexander Elphinstone
  AssignClass (10f1b6be-f1cd-4ff3-abbe-57567ebbdb2e)
 Call ID: 10f1b6be-f1cd-4ff3-abbe-57567ebbdb2e
  Args:
    type: :Person
    source: John Alexander Elphinstone
  AddLiteral (aadcd3cd-dc8f-4ae4-8e18-7d06ca3d543d)
 Call ID: aadcd3cd-dc8f-4ae4-8e18-7d06ca3d543d
  Args:
    relation: :hasBirthYear
    source: John Alexander Elphinstone
    literal_value: 1914
    literal_type: xsd:integer
  AddLiteral (b010c89a-f139-493e-939b-b6c8596422cd)
 Call ID: b010c89a-f139-493e-939b-b6c8596422cd
  Args:
    literal_type: xsd:integer
    literal_value: 1975
    source: John Alexander Elphinstone
    relation: :hasDeathYear
  AssignClass (a9fffb59-d5a8-4072-ba89-ca4f6fc70e98)
 Call ID: a9fffb59-d5a8-4072-ba89-ca4f6fc70e98
  Args:
    type: :Man
    source: Sidney Elphinstone
  AssignClass (5336c3ef-e4ee-46d6-b41f-9fdab7064d76)
 Call ID: 5336c3ef-e4ee-46d6-b41f-9fdab7064d76
  Args:
    type: :Person
    source: Sidney Elphinstone
  AssignClass (fdc466c5-a2b7-40cd-ae78-c432c6ef6990)
 Call ID: fdc466c5-a2b7-40cd-ae78-c432c6ef6990
  Args:
    type: :Woman
    source: Lady Mary Bowes-Lyon
  AssignClass (c94554a1-3644-4a9a-bf17-05b4d46f5d98)
 Call ID: c94554a1-3644-4a9a-bf17-05b4d46f5d98
  Args:
    type: :Person
    source: Lady Mary Bowes-Lyon
  AddTriple (6c1aa34f-3c1f-40d4-b829-7347cca3d5f3)
 Call ID: 6c1aa34f-3c1f-40d4-b829-7347cca3d5f3
  Args:
    source: John Alexander Elphinstone
    relation: :hasFather
    target: Sidney Elphinstone
  AddTriple (c53d2359-76a4-4c4e-903a-d4f8ed487f26)
 Call ID: c53d2359-76a4-4c4e-903a-d4f8ed487f26
  Args:
    relation: :hasMother
    source: John Alexander Elphinstone
    target: Lady Mary Bowes-Lyon
  AssignClass (a1c2e321-fe72-41e7-837d-468a42a5e53b)
 Call ID: a1c2e321-fe72-41e7-837d-468a42a5e53b
  Args:
    type: :Man
    source: Andrew Charles Victor Elphinstone
  AssignClass (9dcb7326-f5e6-40d9-8dd7-2d97bd2425a6)
 Call ID: 9dcb7326-f5e6-40d9-8dd7-2d97bd2425a6
  Args:
    type: :Person
    source: Andrew Charles Victor Elphinstone
  AddTriple (79c302e3-ee25-49a3-b01c-2b7ddcf33be2)
 Call ID: 79c302e3-ee25-49a3-b01c-2b7ddcf33be2
  Args:
    source: John Alexander Elphinstone
    relation: :hasBrother
    target: Andrew Charles Victor Elphinstone
  AssignClass (9271979b-2021-4172-850a-24e8ea14c3e3)
 Call ID: 9271979b-2021-4172-850a-24e8ea14c3e3
  Args:
    type: :Woman
    source: Margaret Elphinstone
  AssignClass (17264b3c-9ef6-49a1-ac52-1d1bbf440b43)
 Call ID: 17264b3c-9ef6-49a1-ac52-1d1bbf440b43
  Args:
    type: :Person
    source: Margaret Elphinstone
  AddTriple (a8765cd4-b099-45cb-99bc-1a57fc47ce6e)
 Call ID: a8765cd4-b099-45cb-99bc-1a57fc47ce6e
  Args:
    target: Margaret Elphinstone
    relation: :hasSister
    source: John Alexander Elphinstone
  AssignClass (bd7993bb-4850-49ca-8e05-9f8ea8112433)
 Call ID: bd7993bb-4850-49ca-8e05-9f8ea8112433
  Args:
    type: :Man
    source: William Elphinstone
  AssignClass (dd2d8263-400b-4515-be1c-589272cf1d22)
 Call ID: dd2d8263-400b-4515-be1c-589272cf1d22
  Args:
    type: :Person
    source: William Elphinstone
  AssignClass (b98fbbc7-fa67-4da6-b488-d9fb4de47043)
 Call ID: b98fbbc7-fa67-4da6-b488-d9fb4de47043
  Args:
    type: :Woman
    source: Lady Constance Euphemia Woronzow Murray
  AssignClass (41f040f3-fc8f-4842-80e3-11889f2a3855)
 Call ID: 41f040f3-fc8f-4842-80e3-11889f2a3855
  Args:
    type: :Person
    source: Lady Constance Euphemia Woronzow Murray
  AddTriple (1372174b-bfd9-4c64-80a9-610237caeffc)
 Call ID: 1372174b-bfd9-4c64-80a9-610237caeffc
  Args:
    target: William Elphinstone
    source: Sidney Elphinstone
    relation: :hasFather
  AddTriple (750efd01-1a72-4f97-bfb5-a7f869370835)
 Call ID: 750efd01-1a72-4f97-bfb5-a7f869370835
  Args:
    target: Lady Constance Euphemia Woronzow Murray
    source: Sidney Elphinstone
    relation: :hasMother
  AssignClass (bff47d32-d703-4d5d-bbab-16dd8fa9b6ba)
 Call ID: bff47d32-d703-4d5d-bbab-16dd8fa9b6ba
  Args:
    type: :Man
    source: Alexander Murray
  AssignClass (898f9c15-ca05-4fa1-b0f7-e151ede7759c)
 Call ID: 898f9c15-ca05-4fa1-b0f7-e151ede7759c
  Args:
    type: :Person
    source: Alexander Murray
  AddTriple (1894e461-d274-4e91-bcd3-05ca654c783a)
 Call ID: 1894e461-d274-4e91-bcd3-05ca654c783a
  Args:
    relation: :hasFather
    source: Lady Constance Euphemia Woronzow Murray
    target: Alexander Murray
  AssignClass (2c1c3755-d72b-42f7-9a16-af479cec4b8d)
 Call ID: 2c1c3755-d72b-42f7-9a16-af479cec4b8d
  Args:
    type: :Woman
    source: Queen Elizabeth II
  AssignClass (6996f2f0-a9d0-4af7-9813-d40390c689a5)
 Call ID: 6996f2f0-a9d0-4af7-9813-d40390c689a5
  Args:
    type: :Person
    source: Queen Elizabeth II
  AssignClass (eadca78e-2925-47d6-9ffc-3fed05d2c8f7)
 Call ID: eadca78e-2925-47d6-9ffc-3fed05d2c8f7
  Args:
    type: :Woman
    source: Princess Margaret
  AssignClass (d509fc68-71c9-42e3-9ad0-6127ca916c49)
 Call ID: d509fc68-71c9-42e3-9ad0-6127ca916c49
  Args:
    type: :Person
    source: Princess Margaret
  AssignClass (9f3bf7f2-6392-4703-8e64-3309065d05a5)
 Call ID: 9f3bf7f2-6392-4703-8e64-3309065d05a5
  Args:
    type: :Woman
    source: Queen Elizabeth The Queen Mother
  AssignClass (aec81927-a84f-431f-a2d4-05a1205982d1)
 Call ID: aec81927-a84f-431f-a2d4-05a1205982d1
  Args:
    type: :Person
    source: Queen Elizabeth The Queen Mother
  Finish (a145f59f-83ed-479c-b2bd-22b0a8198aa6)
 Call ID: a145f59f-83ed-479c-b2bd-22b0a8198aa6
  Args: