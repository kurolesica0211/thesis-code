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
  AssignClass (a8f6e98c-a08f-45d2-8be9-ff0751fb47e0)
 Call ID: a8f6e98c-a08f-45d2-8be9-ff0751fb47e0
  Args:
    source: David_Albert_Charles_Armstrong-Jones
    type: :Man
  AssignClass (147f310a-b7f1-4c73-83b5-99c770c4deef)
 Call ID: 147f310a-b7f1-4c73-83b5-99c770c4deef
  Args:
    source: David_Albert_Charles_Armstrong-Jones
    type: :Person
  AddLiteral (9bf01905-4671-445c-8248-c64fb608588f)
 Call ID: 9bf01905-4671-445c-8248-c64fb608588f
  Args:
    literal_value: 1961
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: David_Albert_Charles_Armstrong-Jones
  AddLiteral (ca3eceb2-5f1c-4a48-ae93-e124c8247642)
 Call ID: ca3eceb2-5f1c-4a48-ae93-e124c8247642
  Args:
    source: David_Albert_Charles_Armstrong-Jones
    literal_value: David Linley
    literal_type: xsd:string
    relation: :knownAs
  AddLiteral (dc12f37d-3bbc-4fbe-8544-3ce8dcb09221)
 Call ID: dc12f37d-3bbc-4fbe-8544-3ce8dcb09221
  Args:
    source: David_Albert_Charles_Armstrong-Jones
    literal_type: xsd:string
    relation: :formerlyKnownAs
    literal_value: Viscount Linley
  AssignClass (931ed5ff-c4d8-43d7-90a9-a6abb34931c0)
 Call ID: 931ed5ff-c4d8-43d7-90a9-a6abb34931c0
  Args:
    source: Antony_Armstrong-Jones
    type: :Man
  AssignClass (3945aa7c-faa8-4b33-b2c4-9566ef8f0ebc)
 Call ID: 3945aa7c-faa8-4b33-b2c4-9566ef8f0ebc
  Args:
    source: Antony_Armstrong-Jones
    type: :Person
  AddLiteral (bc5e12ad-f8cf-4561-b967-84000fadcb25)
 Call ID: bc5e12ad-f8cf-4561-b967-84000fadcb25
  Args:
    source: Antony_Armstrong-Jones
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 2017
  AssignClass (726b087a-c1b7-4423-84cb-12951e875f9f)
 Call ID: 726b087a-c1b7-4423-84cb-12951e875f9f
  Args:
    source: Princess_Margaret
    type: :Woman
  AssignClass (08c06d60-becb-490c-abce-024ca5599d7c)
 Call ID: 08c06d60-becb-490c-abce-024ca5599d7c
  Args:
    source: Princess_Margaret
    type: :Person
  AddTriple (8241922e-8194-4744-bf42-5aaaa185cdf3)
 Call ID: 8241922e-8194-4744-bf42-5aaaa185cdf3
  Args:
    source: David_Albert_Charles_Armstrong-Jones
    target: Antony_Armstrong-Jones
    relation: :hasFather
  AddTriple (019976e2-302d-43bc-9b57-e7af38e12f7d)
 Call ID: 019976e2-302d-43bc-9b57-e7af38e12f7d
  Args:
    source: David_Albert_Charles_Armstrong-Jones
    relation: :hasMother
    target: Princess_Margaret
  AssignClass (85a3b87c-c298-4ac4-9d20-38426c0a860f)
 Call ID: 85a3b87c-c298-4ac4-9d20-38426c0a860f
  Args:
    source: Lady_Sarah_Chatto
    type: :Woman
  AssignClass (01095f75-ccd7-469a-bd2c-a9f6c4294782)
 Call ID: 01095f75-ccd7-469a-bd2c-a9f6c4294782
  Args:
    source: Lady_Sarah_Chatto
    type: :Person
  AddTriple (254ff756-188b-4d41-b572-26097c64141d)
 Call ID: 254ff756-188b-4d41-b572-26097c64141d
  Args:
    source: David_Albert_Charles_Armstrong-Jones
    target: Lady_Sarah_Chatto
    relation: :hasSister
  AssignClass (d07a3da4-61ce-4159-8f80-900e3832d8ed)
 Call ID: d07a3da4-61ce-4159-8f80-900e3832d8ed
  Args:
    source: Lady_Frances_von_Hofmannsthal
    type: :Woman
  AssignClass (bb1be22d-b67c-4929-934f-33d80f15a0aa)
 Call ID: bb1be22d-b67c-4929-934f-33d80f15a0aa
  Args:
    source: Lady_Frances_von_Hofmannsthal
    type: :Person
  AddTriple (771afb90-9ffb-403b-88f9-095434c53277)
 Call ID: 771afb90-9ffb-403b-88f9-095434c53277
  Args:
    source: David_Albert_Charles_Armstrong-Jones
    target: Lady_Frances_von_Hofmannsthal
    relation: :hasSister
  AssignClass (aaf1aaf2-2beb-40c7-9a50-81bf0ec46f15)
 Call ID: aaf1aaf2-2beb-40c7-9a50-81bf0ec46f15
  Args:
    source: Polly_Fry
    type: :Woman
  AssignClass (7811f8a1-8c12-4cf9-9cdb-ab1c9e01080c)
 Call ID: 7811f8a1-8c12-4cf9-9cdb-ab1c9e01080c
  Args:
    source: Polly_Fry
    type: :Person
  AddTriple (dcbd2191-ef38-45eb-9f60-bb13a95350ec)
 Call ID: dcbd2191-ef38-45eb-9f60-bb13a95350ec
  Args:
    source: David_Albert_Charles_Armstrong-Jones
    relation: :hasSister
    target: Polly_Fry
  AssignClass (9e5c1889-f7a2-42d8-bb47-5eb36883361e)
 Call ID: 9e5c1889-f7a2-42d8-bb47-5eb36883361e
  Args:
    source: Serena_Alleyne_Stanhope
    type: :Woman
  AssignClass (3a207773-916d-4b87-8871-cfdc56c57ef6)
 Call ID: 3a207773-916d-4b87-8871-cfdc56c57ef6
  Args:
    source: Serena_Alleyne_Stanhope
    type: :Person
  AddLiteral (57790e41-a263-477b-95ef-09c6090d47db)
 Call ID: 57790e41-a263-477b-95ef-09c6090d47db
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1970
    source: Serena_Alleyne_Stanhope
  AssignClass (2e7a5203-8a7a-427f-af93-5d70b9b6744e)
 Call ID: 2e7a5203-8a7a-427f-af93-5d70b9b6744e
  Args:
    source: Lady_Margarita_Armstrong-Jones
    type: :Woman
  AssignClass (6c3a86a2-a486-4308-a077-6c810215d568)
 Call ID: 6c3a86a2-a486-4308-a077-6c810215d568
  Args:
    source: Lady_Margarita_Armstrong-Jones
    type: :Person
  AddTriple (5205ae88-32bf-4736-bbe2-248fd9bcee43)
 Call ID: 5205ae88-32bf-4736-bbe2-248fd9bcee43
  Args:
    source: Lady_Margarita_Armstrong-Jones
    relation: :hasMother
    target: Serena_Alleyne_Stanhope
  AddTriple (949f31df-fd72-402b-82f5-7b1ca61c09ff)
 Call ID: 949f31df-fd72-402b-82f5-7b1ca61c09ff
  Args:
    source: Lady_Margarita_Armstrong-Jones
    target: David_Albert_Charles_Armstrong-Jones
    relation: :hasFather
  AssignClass (c84d4e8e-a3c4-4406-8e0d-93f37b0be5e4)
 Call ID: c84d4e8e-a3c4-4406-8e0d-93f37b0be5e4
  Args:
    source: Viscount_Linley_Son
    type: :Man
  AssignClass (90f666da-22f3-44ef-b742-4f3a16b9bade)
 Call ID: 90f666da-22f3-44ef-b742-4f3a16b9bade
  Args:
    source: Viscount_Linley_Son
    type: :Person
  AddTriple (44751a51-7ea7-43c8-9369-916f6a51aacc)
 Call ID: 44751a51-7ea7-43c8-9369-916f6a51aacc
  Args:
    relation: :hasMother
    target: Serena_Alleyne_Stanhope
    source: Viscount_Linley_Son
  AddTriple (c553872d-ba4d-462b-83cc-334dd0713b62)
 Call ID: c553872d-ba4d-462b-83cc-334dd0713b62
  Args:
    target: David_Albert_Charles_Armstrong-Jones
    relation: :hasFather
    source: Viscount_Linley_Son
  AssignClass (c6935c91-eeed-4f96-829f-67c9cdf611f9)
 Call ID: c6935c91-eeed-4f96-829f-67c9cdf611f9
  Args:
    source: Queen_Elizabeth_II
    type: :Woman
  AssignClass (0c95b380-0d31-4231-b8a4-ad8b645d9d1f)
 Call ID: 0c95b380-0d31-4231-b8a4-ad8b645d9d1f
  Args:
    source: Queen_Elizabeth_II
    type: :Person
  AddTriple (f5297a88-91cc-43d6-ae4f-b334c73a89e3)
 Call ID: f5297a88-91cc-43d6-ae4f-b334c73a89e3
  Args:
    source: Queen_Elizabeth_II
    relation: :isSisterOf
    target: Princess_Margaret
  Finish (a3b8aa97-7117-4c02-a2dc-6b1509df8879)
 Call ID: a3b8aa97-7117-4c02-a2dc-6b1509df8879
  Args: