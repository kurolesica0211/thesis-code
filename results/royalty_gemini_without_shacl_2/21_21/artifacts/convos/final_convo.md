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
Norton Louis Philip Knatchbull, 3rd Earl Mountbatten of Burma (born 8 October 1947), known until 2005 as Lord Romsey and until 2017 as the Lord Brabourne, is a British peer.
Life and education

Mountbatten was born at King's College Hospital in London as the eldest son of Patricia Knatchbull, née Mountbatten, later 2nd Countess Mountbatten of Burma, and film producer John Knatchbull, 7th Baron Brabourne.
Mountbatten was educated at the Dragon School, in Oxford, and Gordonstoun School, Elgin, Moray, Scotland.
On the death of his father on 23 September 2005, he became the 8th Baron Brabourne, of Brabourne in the County of Kent, in the peerage of the United Kingdom.
He also succeeded to the Knatchbull Baronetcy, of Mersham Hatch in the County of Kent, in the baronetage of England.
On the death of his mother on 13 June 2017, he became Earl Mountbatten of Burma, also a title in the peerage of the United Kingdom created for his grandfather, Admiral of the Fleet Lord Louis Mountbatten.
Mountbatten is the godfather of Philip's grandson, the Prince of Wales.
He is also related to author Jane Austen, as his father, John Knatchbull, 7th Baron Brabourne, was a direct descendant of her brother Edward Austen Knight.
Marriage and children

Mountbatten is married to Penelope Meredith Eastwood (born 16 April 1953), a daughter of Reginald Wray Frank Eastwood (1912–1980), a self-made millionaire former butcher who founded the Angus Steakhouse chain, and Marian Elizabeth (1926–2020), née Hood.
They were wed on 20 October 1979 at Romsey Abbey, less than two months after the IRA murdered his 79-year-old maternal grandfather, Louis Mountbatten, 1st
Earl Mountbatten of Burma; his 14-year-old younger brother, Nicholas Knatchbull; and his 83-year-old paternal grandmother, Doreen Knatchbull, Dowager Lady Brabourne.
The 3rd Earl Mountbatten of Burma and his wife have three children and three grandsons:


From 2010 to 2014, Mountbatten was in an extramarital relationship with Eugenie, Lady Nuttall, widow of Sir Nicholas Nuttall, 3rd Baronet, who was heir to the Edmund Nuttall Limited construction company.



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
  AssignClass (6ee6b761-3958-4677-87ac-9aa4f9a3e617)
 Call ID: 6ee6b761-3958-4677-87ac-9aa4f9a3e617
  Args:
    source: Norton_Louis_Philip_Knatchbull
    type: :Man
  AssignClass (cf2e186a-0a94-41dc-86a0-465c38c522ab)
 Call ID: cf2e186a-0a94-41dc-86a0-465c38c522ab
  Args:
    type: :Person
    source: Norton_Louis_Philip_Knatchbull
  AddLiteral (4a768f6e-4dc4-4418-9ec1-f11940d9eb41)
 Call ID: 4a768f6e-4dc4-4418-9ec1-f11940d9eb41
  Args:
    literal_value: 1947
    source: Norton_Louis_Philip_Knatchbull
    literal_type: xsd:integer
    relation: :hasBirthYear
  AssignClass (8e6b7133-6dbf-4549-8e0e-38fb981ff8ab)
 Call ID: 8e6b7133-6dbf-4549-8e0e-38fb981ff8ab
  Args:
    type: :Woman
    source: Patricia_Knatchbull
  AssignClass (8092e736-d04e-4945-b064-b09ce59ffee9)
 Call ID: 8092e736-d04e-4945-b064-b09ce59ffee9
  Args:
    type: :Person
    source: Patricia_Knatchbull
  AssignClass (98e3021b-ff68-45e5-adde-6e5d1a2830c5)
 Call ID: 98e3021b-ff68-45e5-adde-6e5d1a2830c5
  Args:
    source: John_Knatchbull
    type: :Man
  AssignClass (2d490c41-4ffa-495c-99c2-9ae9988b112b)
 Call ID: 2d490c41-4ffa-495c-99c2-9ae9988b112b
  Args:
    source: John_Knatchbull
    type: :Person
  AddTriple (1039fbf7-e0da-4812-95a7-287973a16c41)
 Call ID: 1039fbf7-e0da-4812-95a7-287973a16c41
  Args:
    relation: :hasMother
    source: Norton_Louis_Philip_Knatchbull
    target: Patricia_Knatchbull
  AddTriple (d435bcf7-5f5b-4aaf-8ed3-a9ae5fc8b794)
 Call ID: d435bcf7-5f5b-4aaf-8ed3-a9ae5fc8b794
  Args:
    relation: :hasFather
    source: Norton_Louis_Philip_Knatchbull
    target: John_Knatchbull
  AssignClass (d9704ddd-8dcc-4586-acdf-29c58236036c)
 Call ID: d9704ddd-8dcc-4586-acdf-29c58236036c
  Args:
    source: Louis_Mountbatten
    type: :Man
  AssignClass (bba1ec21-0fbd-46c1-afdc-792c4eeb4a27)
 Call ID: bba1ec21-0fbd-46c1-afdc-792c4eeb4a27
  Args:
    source: Louis_Mountbatten
    type: :Person
  AddTriple (31aab594-3e75-4730-a2f3-d8c54f515f39)
 Call ID: 31aab594-3e75-4730-a2f3-d8c54f515f39
  Args:
    relation: :hasMother
    source: Patricia_Knatchbull
    target: Louis_Mountbatten
  AssignClass (4661e7d5-b249-435e-810b-5db36dec797c)
 Call ID: 4661e7d5-b249-435e-810b-5db36dec797c
  Args:
    source: Nicholas_Knatchbull
    type: :Man
  AssignClass (c557876b-5541-4bdc-b275-65a82c298951)
 Call ID: c557876b-5541-4bdc-b275-65a82c298951
  Args:
    source: Nicholas_Knatchbull
    type: :Person
  AddTriple (b77f7664-2f6b-4b28-834f-400eb13b5a11)
 Call ID: b77f7664-2f6b-4b28-834f-400eb13b5a11
  Args:
    relation: :hasBrother
    source: Norton_Louis_Philip_Knatchbull
    target: Nicholas_Knatchbull
  AssignClass (ed4d8da3-e576-4885-93f7-5104843182bd)
 Call ID: ed4d8da3-e576-4885-93f7-5104843182bd
  Args:
    type: :Woman
    source: Doreen_Knatchbull
  AssignClass (b4d8ce9f-6289-441e-a391-83a8cdf42f7c)
 Call ID: b4d8ce9f-6289-441e-a391-83a8cdf42f7c
  Args:
    type: :Person
    source: Doreen_Knatchbull
  AddTriple (f25ccf86-6a57-4a59-b321-2a4b998326ff)
 Call ID: f25ccf86-6a57-4a59-b321-2a4b998326ff
  Args:
    target: Doreen_Knatchbull
    source: John_Knatchbull
    relation: :hasMother
  AssignClass (abc442db-aa6c-4db6-8dc3-8328d1105f18)
 Call ID: abc442db-aa6c-4db6-8dc3-8328d1105f18
  Args:
    source: Penelope_Meredith_Eastwood
    type: :Woman
  AssignClass (43115e19-9f06-4c8f-9378-6507881bcd9e)
 Call ID: 43115e19-9f06-4c8f-9378-6507881bcd9e
  Args:
    type: :Person
    source: Penelope_Meredith_Eastwood
  AddLiteral (d0f79675-235c-47f1-93d5-c1af27cae5ab)
 Call ID: d0f79675-235c-47f1-93d5-c1af27cae5ab
  Args:
    literal_value: 1953
    relation: :hasBirthYear
    source: Penelope_Meredith_Eastwood
    literal_type: xsd:integer
  AddTriple (73618936-7e8a-4671-bc01-7b25d0e54a06)
 Call ID: 73618936-7e8a-4671-bc01-7b25d0e54a06
  Args:
    target: Penelope_Meredith_Eastwood
    source: Norton_Louis_Philip_Knatchbull
    relation: :hasRelation
  AddLiteral (ce90b1a2-6155-46b5-8d25-76e8cd129491)
 Call ID: ce90b1a2-6155-46b5-8d25-76e8cd129491
  Args:
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: Norton_Louis_Philip_Knatchbull
    literal_value: 1979
  AssignClass (6c52f8e3-f158-496a-a7c7-919c01c0fcae)
 Call ID: 6c52f8e3-f158-496a-a7c7-919c01c0fcae
  Args:
    type: :Man
    source: Reginald_Wray_Frank_Eastwood
  AssignClass (f6670c95-ef27-48c2-a0c1-945391c46e69)
 Call ID: f6670c95-ef27-48c2-a0c1-945391c46e69
  Args:
    source: Reginald_Wray_Frank_Eastwood
    type: :Person
  AddLiteral (8377a257-e269-44ec-88f4-6a0e5460485d)
 Call ID: 8377a257-e269-44ec-88f4-6a0e5460485d
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Reginald_Wray_Frank_Eastwood
    literal_value: 1912
  AddLiteral (d27b1e5f-ed13-49c2-a552-75a9f6fbe86b)
 Call ID: d27b1e5f-ed13-49c2-a552-75a9f6fbe86b
  Args:
    source: Reginald_Wray_Frank_Eastwood
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1980
  AssignClass (8026f63d-949f-40d7-ade7-b2d371e455e6)
 Call ID: 8026f63d-949f-40d7-ade7-b2d371e455e6
  Args:
    type: :Woman
    source: Marian_Elizabeth
  AssignClass (69406764-64a4-476b-8085-163d9a573946)
 Call ID: 69406764-64a4-476b-8085-163d9a573946
  Args:
    type: :Person
    source: Marian_Elizabeth
  AddLiteral (c98173f5-7738-40df-8055-7c437b7bab32)
 Call ID: c98173f5-7738-40df-8055-7c437b7bab32
  Args:
    relation: :hasBirthYear
    source: Marian_Elizabeth
    literal_type: xsd:integer
    literal_value: 1926
  AddLiteral (64b093c3-1082-4cf4-8386-9c56d75b305f)
 Call ID: 64b093c3-1082-4cf4-8386-9c56d75b305f
  Args:
    literal_type: xsd:integer
    source: Marian_Elizabeth
    relation: :hasDeathYear
    literal_value: 2020
  AddTriple (5f1b0cbd-27e7-46d9-8bfe-40ad6c10ec79)
 Call ID: 5f1b0cbd-27e7-46d9-8bfe-40ad6c10ec79
  Args:
    relation: :hasFather
    source: Penelope_Meredith_Eastwood
    target: Reginald_Wray_Frank_Eastwood
  AddTriple (e969ad52-2b84-4c0e-8058-5348a8bfd859)
 Call ID: e969ad52-2b84-4c0e-8058-5348a8bfd859
  Args:
    target: Marian_Elizabeth
    source: Penelope_Meredith_Eastwood
    relation: :hasMother
  Finish (a48ace19-3e8e-407b-a59a-476370719f25)
 Call ID: a48ace19-3e8e-407b-a59a-476370719f25
  Args: