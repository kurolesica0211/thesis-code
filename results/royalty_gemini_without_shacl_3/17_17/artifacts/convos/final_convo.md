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
David Albert Charles Armstrong-Jones, 2nd Earl of Snowdon (born 3 November 1961), styled as Viscount Linley until 2017 and known professionally as David Linley, is a member of the British royal family, an English furniture maker, and honorary chairman of the auction house Christie's.
He is the only son of Antony Armstrong-Jones, 1st Earl of Snowdon and Princess Margaret, and through his mother a grandson of King George VI and first cousin of King Charles III.
When he was born, he was 5th in the line of succession to the British throne; as of 2025, he is 26th, and the highest who is not a descendant of Queen Elizabeth II, his aunt.
Early life and education

David Albert Charles Armstrong-Jones was born at 10:45 am on 3 November 1961, at Clarence House, London, the son of Princess Margaret and Antony Armstrong-Jones, 1st Earl of Snowdon.
His godparents were his aunt Queen Elizabeth II, Lady Elizabeth Cavendish, Patrick Plunket, 7th Baron Plunket, Lord Rupert Nevill, and Simon Phipps.
He has one full sister, Lady Sarah Chatto (née Armstrong-Jones), and two paternal half-sisters, Lady Frances von Hofmannsthal (née Armstrong-Jones) and Polly Fry.
Professional life

Linley opened a workshop in Dorking, where he designed and made furniture for three years before setting up his own company, David Linley Furniture Limited (now known as Linley), where he makes bespoke furniture, upholstery, and interior design products known for their neoclassical appearance and use of inlaid woods.
Accordingly, the first Earl Snowdon was also created Baron Armstrong-Jones, and retained his seat in the Lords until his death in 2017, whereupon his son inherited the earldom but not the life peerage or the seat.
Serena Alleyne Stanhope (born 1 March 1970, Limerick, Ireland), daughter of Viscount Petersham (later the 12th Earl of Harrington) at St. Margaret's Church, Westminster.
He and his wife have two children:


From 2000 until 2002, Linley, his wife and son lived at Kensington Palace with his mother, Princess Margaret, in her declining years.
On 8 April 2002, Linley, along with the Prince of Wales, the Duke of York, and the Earl of Wessex, "stood guard" at the lying-in-state of their grandmother, Queen Elizabeth the Queen Mother.
This Vigil of the Princes had taken place only once before, during the lying-in-state of George V in 1936.
The first confirmation that the royal in the extortion attempt was Viscount Linley came from the journalist Nicholas Davies.
In 2011, Linley's daughter, Lady Margarita Armstrong-Jones, was a bridesmaid at the wedding of Prince William and Catherine Middleton.
In 2012, his son, styled by courtesy as Viscount Linley since January 2017, was appointed by the Queen as a page of honour.



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
  AssignClass (9f9da506-2886-42a9-8a07-12b5a4b153f1)
 Call ID: 9f9da506-2886-42a9-8a07-12b5a4b153f1
  Args:
    source: David_Albert_Charles_Armstrong-Jones
    type: :Man
  AssignClass (03b38e71-e7b6-4d09-9b84-8326826ae6e2)
 Call ID: 03b38e71-e7b6-4d09-9b84-8326826ae6e2
  Args:
    source: David_Albert_Charles_Armstrong-Jones
    type: :Person
  AddLiteral (d750639a-7366-4f3f-b4f9-c0ad1ad0c3e2)
 Call ID: d750639a-7366-4f3f-b4f9-c0ad1ad0c3e2
  Args:
    source: David_Albert_Charles_Armstrong-Jones
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1961
  AddLiteral (113ce2f5-1770-4f6a-a043-a37c7adc59ec)
 Call ID: 113ce2f5-1770-4f6a-a043-a37c7adc59ec
  Args:
    source: David_Albert_Charles_Armstrong-Jones
    relation: :knownAs
    literal_type: xsd:string
    literal_value: David Linley
  AssignClass (affad0f3-20ef-4040-95dc-701f5dedc0c7)
 Call ID: affad0f3-20ef-4040-95dc-701f5dedc0c7
  Args:
    source: Antony_Armstrong-Jones
    type: :Man
  AssignClass (9d68669d-155a-41e4-abdf-7956ea407cfe)
 Call ID: 9d68669d-155a-41e4-abdf-7956ea407cfe
  Args:
    source: Antony_Armstrong-Jones
    type: :Person
  AssignClass (ca24ab5d-f312-4a76-9c6b-0d2ee0f12ab0)
 Call ID: ca24ab5d-f312-4a76-9c6b-0d2ee0f12ab0
  Args:
    source: Princess_Margaret
    type: :Woman
  AssignClass (92c9e8ce-3f26-4d0f-9f44-ec953199a969)
 Call ID: 92c9e8ce-3f26-4d0f-9f44-ec953199a969
  Args:
    source: Princess_Margaret
    type: :Person
  AddTriple (4455cf2c-8565-4ffb-8f12-087bae91ad45)
 Call ID: 4455cf2c-8565-4ffb-8f12-087bae91ad45
  Args:
    target: Antony_Armstrong-Jones
    source: David_Albert_Charles_Armstrong-Jones
    relation: :hasFather
  AddTriple (9ff334f0-32fe-483d-a1b4-bac9e2d799e2)
 Call ID: 9ff334f0-32fe-483d-a1b4-bac9e2d799e2
  Args:
    relation: :hasMother
    target: Princess_Margaret
    source: David_Albert_Charles_Armstrong-Jones
  AssignClass (793b71f6-a6e7-4311-9f52-107e231b4253)
 Call ID: 793b71f6-a6e7-4311-9f52-107e231b4253
  Args:
    type: :Man
    source: King_George_VI
  AssignClass (980b3150-b8ba-400c-a3ff-2a0f24c09f4b)
 Call ID: 980b3150-b8ba-400c-a3ff-2a0f24c09f4b
  Args:
    source: King_George_VI
    type: :Person
  AddTriple (9ce868dd-849b-4349-b2d7-7cb20a7d6565)
 Call ID: 9ce868dd-849b-4349-b2d7-7cb20a7d6565
  Args:
    target: King_George_VI
    source: Princess_Margaret
    relation: :hasFather
  AssignClass (3b1b2d7c-87d9-4669-9ca6-7c2500c1def2)
 Call ID: 3b1b2d7c-87d9-4669-9ca6-7c2500c1def2
  Args:
    source: King_Charles_III
    type: :Man
  AssignClass (afa657bd-a45c-4403-a11c-114839ecec4f)
 Call ID: afa657bd-a45c-4403-a11c-114839ecec4f
  Args:
    type: :Person
    source: King_Charles_III
  AssignClass (b15fadb6-eca7-449d-9815-f985b608cd28)
 Call ID: b15fadb6-eca7-449d-9815-f985b608cd28
  Args:
    source: Queen_Elizabeth_II
    type: :Woman
  AssignClass (b67a206b-e0aa-44b0-931b-c3e38917142f)
 Call ID: b67a206b-e0aa-44b0-931b-c3e38917142f
  Args:
    source: Queen_Elizabeth_II
    type: :Person
  AssignClass (025d5f95-b1d7-4076-9c57-78bb6c6a0dab)
 Call ID: 025d5f95-b1d7-4076-9c57-78bb6c6a0dab
  Args:
    type: :Woman
    source: Lady_Sarah_Chatto
  AssignClass (b9c30017-91e0-412d-9300-8e99979444f7)
 Call ID: b9c30017-91e0-412d-9300-8e99979444f7
  Args:
    source: Lady_Sarah_Chatto
    type: :Person
  AddTriple (80a17dcb-460c-4cf1-b856-a292746bcd56)
 Call ID: 80a17dcb-460c-4cf1-b856-a292746bcd56
  Args:
    target: Lady_Sarah_Chatto
    source: David_Albert_Charles_Armstrong-Jones
    relation: :hasSister
  AssignClass (1b399f68-6031-43c3-bc66-5f8b64ba6a74)
 Call ID: 1b399f68-6031-43c3-bc66-5f8b64ba6a74
  Args:
    type: :Woman
    source: Lady_Frances_von_Hofmannsthal
  AssignClass (22e36038-3ad4-447a-9777-3fd9bd0cacd2)
 Call ID: 22e36038-3ad4-447a-9777-3fd9bd0cacd2
  Args:
    type: :Person
    source: Lady_Frances_von_Hofmannsthal
  AssignClass (aa074f8f-eb91-46e9-9a3d-14388e5667ef)
 Call ID: aa074f8f-eb91-46e9-9a3d-14388e5667ef
  Args:
    source: Polly_Fry
    type: :Woman
  AssignClass (d9e25473-2d3f-4dee-95a9-d2662aadb7c6)
 Call ID: d9e25473-2d3f-4dee-95a9-d2662aadb7c6
  Args:
    source: Polly_Fry
    type: :Person
  AddTriple (e22672c0-c037-4085-a01b-ab790bfbd066)
 Call ID: e22672c0-c037-4085-a01b-ab790bfbd066
  Args:
    source: Lady_Frances_von_Hofmannsthal
    target: Antony_Armstrong-Jones
    relation: :hasFather
  AddTriple (28770794-0f1b-45f4-addd-e90c85aa8b52)
 Call ID: 28770794-0f1b-45f4-addd-e90c85aa8b52
  Args:
    relation: :hasFather
    target: Antony_Armstrong-Jones
    source: Polly_Fry
  AssignClass (d9b1f914-32ba-4b33-a10c-3c8e96dbdf7e)
 Call ID: d9b1f914-32ba-4b33-a10c-3c8e96dbdf7e
  Args:
    type: :Woman
    source: Serena_Alleyne_Stanhope
  AssignClass (fd1b99f2-732f-4b1e-ab5a-a11e68c2be9c)
 Call ID: fd1b99f2-732f-4b1e-ab5a-a11e68c2be9c
  Args:
    source: Serena_Alleyne_Stanhope
    type: :Person
  AddLiteral (d1ca06a9-af1f-40b6-aea2-97da00e25baf)
 Call ID: d1ca06a9-af1f-40b6-aea2-97da00e25baf
  Args:
    source: Serena_Alleyne_Stanhope
    relation: :hasBirthYear
    literal_value: 1970
    literal_type: xsd:integer
  AssignClass (8ff13676-2b71-4597-b6b4-94b40a903a95)
 Call ID: 8ff13676-2b71-4597-b6b4-94b40a903a95
  Args:
    source: Lady_Margarita_Armstrong-Jones
    type: :Woman
  AssignClass (69834841-f5e6-4357-956f-f07e802d15b2)
 Call ID: 69834841-f5e6-4357-956f-f07e802d15b2
  Args:
    source: Lady_Margarita_Armstrong-Jones
    type: :Person
  AddTriple (1b9f0167-75c4-4048-b1a1-ad2f2aa9f48a)
 Call ID: 1b9f0167-75c4-4048-b1a1-ad2f2aa9f48a
  Args:
    target: Serena_Alleyne_Stanhope
    source: Lady_Margarita_Armstrong-Jones
    relation: :hasMother
  AddTriple (096aa8a4-15c5-48a5-81c5-91fe56d78332)
 Call ID: 096aa8a4-15c5-48a5-81c5-91fe56d78332
  Args:
    source: Lady_Margarita_Armstrong-Jones
    target: David_Albert_Charles_Armstrong-Jones
    relation: :hasFather
  AssignClass (7125f73f-5b33-4f34-b065-c7b7b9dfd3f7)
 Call ID: 7125f73f-5b33-4f34-b065-c7b7b9dfd3f7
  Args:
    source: Viscount_Linley_Son
    type: :Man
  AssignClass (1da749b3-3cd3-4da2-8f14-89d01bbe2f0f)
 Call ID: 1da749b3-3cd3-4da2-8f14-89d01bbe2f0f
  Args:
    source: Viscount_Linley_Son
    type: :Person
  AddTriple (03442d4f-9143-44ee-a8fa-f85ea2ba3238)
 Call ID: 03442d4f-9143-44ee-a8fa-f85ea2ba3238
  Args:
    relation: :hasMother
    source: Viscount_Linley_Son
    target: Serena_Alleyne_Stanhope
  AddTriple (92f069f3-c5e5-4cfd-af64-d5a7215c851a)
 Call ID: 92f069f3-c5e5-4cfd-af64-d5a7215c851a
  Args:
    source: Viscount_Linley_Son
    target: David_Albert_Charles_Armstrong-Jones
    relation: :hasFather
  Finish (2fdbc453-f60a-4b1c-884b-64c4bc55cb56)
 Call ID: 2fdbc453-f60a-4b1c-884b-64c4bc55cb56
  Args: