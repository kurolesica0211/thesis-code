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
Prince Karl Adolf Andreas Prinz von Hesse (German: Karl Adolf Andreas Prinz Von Hessen; 26 March 1937 – 23 March 2022) was a member of the German electoral House of Hesse-Kassel.
He was a first cousin of King Charles III of the United Kingdom through his uncle Prince Philip.
Early life and ancestry

Born on 26  March 1937 in Berlin, into an elder line of the House of Hesse, a house directly descended from the House of Brabant, Karl Adolf Andreas was the eldest son of Prince Christoph of Hesse and his wife, Princess Sophie of Greece and Denmark, youngest sister of Prince Philip, Duke of Edinburgh.
In 1946, his mother was married again to Prince George William of Hanover, maternal grandson of Wilhelm II.
Orphaned by his father at an early age, Karl was later adopted by one of his paternal uncles, Prince Wolfgang of Hesse, in 1952.
Related to most European dynasties, Karl participated in the major events of the gotha.
In 1954, he and his family were invited to take part in the Cruise of the Kings, organized by King Paul of Greece and his wife Queen Frederica.
Karl briefly discussed his mother's childhood and her ties to the Nazi regime in a documentary in 2015 about his uncle, Prince Philip:
Death

Prince Karl of Hesse died in Munich, at the age of 84 years, on March 23, 2022.
}} Media related to Karl Adolf Andreas of Hesse at Wikimedia Commons



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
  AssignClass (73b5e963-8a3f-422f-ac3d-c6c539c828ea)
 Call ID: 73b5e963-8a3f-422f-ac3d-c6c539c828ea
  Args:
    source: Prince_Karl_Adolf_Andreas_Prinz_von_Hesse
    type: :Man
  AssignClass (6bbb594c-89a1-47ec-b8d2-60c86c105078)
 Call ID: 6bbb594c-89a1-47ec-b8d2-60c86c105078
  Args:
    source: Prince_Karl_Adolf_Andreas_Prinz_von_Hesse
    type: :Person
  AddLiteral (05ae5115-27b4-41c5-8fb8-4cbf26704b2b)
 Call ID: 05ae5115-27b4-41c5-8fb8-4cbf26704b2b
  Args:
    relation: :hasBirthYear
    source: Prince_Karl_Adolf_Andreas_Prinz_von_Hesse
    literal_type: xsd:integer
    literal_value: 1937
  AddLiteral (7dd26e96-4c8c-4692-89b1-9cc79137de18)
 Call ID: 7dd26e96-4c8c-4692-89b1-9cc79137de18
  Args:
    relation: :hasDeathYear
    literal_value: 2022
    literal_type: xsd:integer
    source: Prince_Karl_Adolf_Andreas_Prinz_von_Hesse
  AssignClass (85333da2-d3d4-45c2-aa24-6a78b8599e77)
 Call ID: 85333da2-d3d4-45c2-aa24-6a78b8599e77
  Args:
    source: Prince_Christoph_of_Hesse
    type: :Man
  AssignClass (92d090ad-8524-4fd0-91a8-0ddd6d55824f)
 Call ID: 92d090ad-8524-4fd0-91a8-0ddd6d55824f
  Args:
    type: :Person
    source: Prince_Christoph_of_Hesse
  AssignClass (3f45701a-e8d5-44d1-b404-4754cc3f7b12)
 Call ID: 3f45701a-e8d5-44d1-b404-4754cc3f7b12
  Args:
    type: :Woman
    source: Princess_Sophie_of_Greece_and_Denmark
  AssignClass (db133ae1-8f5b-4d1c-8916-0e7417227f26)
 Call ID: db133ae1-8f5b-4d1c-8916-0e7417227f26
  Args:
    type: :Person
    source: Princess_Sophie_of_Greece_and_Denmark
  AddTriple (6500e749-cb35-461e-83b8-c133938c5f34)
 Call ID: 6500e749-cb35-461e-83b8-c133938c5f34
  Args:
    relation: :hasFather
    source: Prince_Karl_Adolf_Andreas_Prinz_von_Hesse
    target: Prince_Christoph_of_Hesse
  AddTriple (3b286f65-e2fa-4918-a6b0-92b252985c84)
 Call ID: 3b286f65-e2fa-4918-a6b0-92b252985c84
  Args:
    relation: :hasMother
    target: Princess_Sophie_of_Greece_and_Denmark
    source: Prince_Karl_Adolf_Andreas_Prinz_von_Hesse
  AssignClass (4390538f-d1b6-4e82-a318-cdd506fd62d0)
 Call ID: 4390538f-d1b6-4e82-a318-cdd506fd62d0
  Args:
    type: :Man
    source: Prince_Philip_Duke_of_Edinburgh
  AssignClass (919d4992-a08a-4c90-9188-a30744cafd1f)
 Call ID: 919d4992-a08a-4c90-9188-a30744cafd1f
  Args:
    type: :Person
    source: Prince_Philip_Duke_of_Edinburgh
  AddTriple (7786e14c-0494-4acf-ad59-07fbfe443953)
 Call ID: 7786e14c-0494-4acf-ad59-07fbfe443953
  Args:
    relation: :hasSister
    source: Prince_Philip_Duke_of_Edinburgh
    target: Princess_Sophie_of_Greece_and_Denmark
  AssignClass (b3385b60-de06-46b4-9249-ab8acda9f68d)
 Call ID: b3385b60-de06-46b4-9249-ab8acda9f68d
  Args:
    source: Prince_George_William_of_Hanover
    type: :Man
  AssignClass (62151228-063e-4378-aa92-7b9721211092)
 Call ID: 62151228-063e-4378-aa92-7b9721211092
  Args:
    source: Prince_George_William_of_Hanover
    type: :Person
  AddLiteral (3d065b13-86ad-46b8-b7a1-9be6e141a123)
 Call ID: 3d065b13-86ad-46b8-b7a1-9be6e141a123
  Args:
    literal_type: xsd:integer
    literal_value: 1946
    source: Princess_Sophie_of_Greece_and_Denmark
    relation: :hasMarriageYear
  AddTriple (a30480fe-ad17-4822-96f3-acc4b2c5678c)
 Call ID: a30480fe-ad17-4822-96f3-acc4b2c5678c
  Args:
    relation: :hasRelation
    target: Prince_George_William_of_Hanover
    source: Princess_Sophie_of_Greece_and_Denmark
  AssignClass (4dac7074-a12c-4586-9347-15b7f39544b1)
 Call ID: 4dac7074-a12c-4586-9347-15b7f39544b1
  Args:
    type: :Man
    source: Prince_Wolfgang_of_Hesse
  AssignClass (ae3a734a-1cf5-49c7-a63b-8fd4a25c99bf)
 Call ID: ae3a734a-1cf5-49c7-a63b-8fd4a25c99bf
  Args:
    source: Prince_Wolfgang_of_Hesse
    type: :Person
  AssignClass (8d2fff2e-e535-4839-a19f-1b61e0aa4ebe)
 Call ID: 8d2fff2e-e535-4839-a19f-1b61e0aa4ebe
  Args:
    type: :Man
    source: King_Charles_III_of_the_United_Kingdom
  AssignClass (402d6958-106c-4365-8611-59ea7f157e54)
 Call ID: 402d6958-106c-4365-8611-59ea7f157e54
  Args:
    type: :Person
    source: King_Charles_III_of_the_United_Kingdom
  AssignClass (02f75984-d661-420b-a62a-7628617f3549)
 Call ID: 02f75984-d661-420b-a62a-7628617f3549
  Args:
    type: :Man
    source: King_Paul_of_Greece
  AssignClass (4a2fd49a-108e-4a19-94d3-c2ef61c1ef02)
 Call ID: 4a2fd49a-108e-4a19-94d3-c2ef61c1ef02
  Args:
    source: King_Paul_of_Greece
    type: :Person
  AssignClass (716ba222-b523-469e-bdb4-18753e7c5fac)
 Call ID: 716ba222-b523-469e-bdb4-18753e7c5fac
  Args:
    source: Queen_Frederica_of_Greece
    type: :Woman
  AssignClass (e68fee8d-85f6-4a7e-8894-3e1bc08dde3f)
 Call ID: e68fee8d-85f6-4a7e-8894-3e1bc08dde3f
  Args:
    type: :Person
    source: Queen_Frederica_of_Greece
  Finish (fe0c21de-e136-48ba-88a5-efca1df0bef3)
 Call ID: fe0c21de-e136-48ba-88a5-efca1df0bef3
  Args: