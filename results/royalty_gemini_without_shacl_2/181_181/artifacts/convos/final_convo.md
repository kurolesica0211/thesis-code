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
  AssignClass (8c0d138d-df3d-4633-83cc-6bfb738ae722)
 Call ID: 8c0d138d-df3d-4633-83cc-6bfb738ae722
  Args:
    source: Karl_Adolf_Andreas_Prinz_von_Hesse
    type: :Man
  AssignClass (470b0549-9249-45bf-a49e-2ebb12ea674e)
 Call ID: 470b0549-9249-45bf-a49e-2ebb12ea674e
  Args:
    type: :Person
    source: Karl_Adolf_Andreas_Prinz_von_Hesse
  AddLiteral (0cd795fc-7c41-45b1-a519-a0e305b11560)
 Call ID: 0cd795fc-7c41-45b1-a519-a0e305b11560
  Args:
    source: Karl_Adolf_Andreas_Prinz_von_Hesse
    literal_type: xsd:integer
    literal_value: 1937
    relation: :hasBirthYear
  AddLiteral (3ef40ee2-1536-4c8d-9de3-f2f0121ed0d1)
 Call ID: 3ef40ee2-1536-4c8d-9de3-f2f0121ed0d1
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 2022
    source: Karl_Adolf_Andreas_Prinz_von_Hesse
  AssignClass (0a76e5e6-a15d-4655-9b51-4625772d1537)
 Call ID: 0a76e5e6-a15d-4655-9b51-4625772d1537
  Args:
    type: :Man
    source: Prince_Christoph_of_Hesse
  AssignClass (3e2c6a82-ed12-48e6-840e-b46d56380685)
 Call ID: 3e2c6a82-ed12-48e6-840e-b46d56380685
  Args:
    type: :Person
    source: Prince_Christoph_of_Hesse
  AssignClass (de0e5351-81a1-49d5-b079-4af4ff49420f)
 Call ID: de0e5351-81a1-49d5-b079-4af4ff49420f
  Args:
    type: :Woman
    source: Princess_Sophie_of_Greece_and_Denmark
  AssignClass (a4351e95-02ee-4b4d-9ed1-043f3368f8dd)
 Call ID: a4351e95-02ee-4b4d-9ed1-043f3368f8dd
  Args:
    type: :Person
    source: Princess_Sophie_of_Greece_and_Denmark
  AddTriple (bac9fdf7-9ec6-4728-88c7-8dc4961bc009)
 Call ID: bac9fdf7-9ec6-4728-88c7-8dc4961bc009
  Args:
    target: Prince_Christoph_of_Hesse
    relation: :hasFather
    source: Karl_Adolf_Andreas_Prinz_von_Hesse
  AddTriple (4f088188-09b9-4ee8-af40-3b522b9c4749)
 Call ID: 4f088188-09b9-4ee8-af40-3b522b9c4749
  Args:
    relation: :hasMother
    source: Karl_Adolf_Andreas_Prinz_von_Hesse
    target: Princess_Sophie_of_Greece_and_Denmark
  AssignClass (721fc797-2c5a-4c5f-8209-9b8df77a0f88)
 Call ID: 721fc797-2c5a-4c5f-8209-9b8df77a0f88
  Args:
    type: :Man
    source: Prince_Philip_Duke_of_Edinburgh
  AssignClass (4fbca565-27f7-4016-b412-2c1ed4ddc546)
 Call ID: 4fbca565-27f7-4016-b412-2c1ed4ddc546
  Args:
    type: :Person
    source: Prince_Philip_Duke_of_Edinburgh
  AddTriple (77043d50-5d09-4c71-93ce-8b670bc2f237)
 Call ID: 77043d50-5d09-4c71-93ce-8b670bc2f237
  Args:
    relation: :hasSister
    source: Prince_Philip_Duke_of_Edinburgh
    target: Princess_Sophie_of_Greece_and_Denmark
  AssignClass (3b9dca2c-249c-464e-ae93-6f47a27f300a)
 Call ID: 3b9dca2c-249c-464e-ae93-6f47a27f300a
  Args:
    source: Prince_George_William_of_Hanover
    type: :Man
  AssignClass (26210157-3e3e-4f95-a348-5e4624e6e603)
 Call ID: 26210157-3e3e-4f95-a348-5e4624e6e603
  Args:
    type: :Person
    source: Prince_George_William_of_Hanover
  AssignClass (0d33a2eb-92c7-4db6-a623-5dd307d95ece)
 Call ID: 0d33a2eb-92c7-4db6-a623-5dd307d95ece
  Args:
    source: Prince_Wolfgang_of_Hesse
    type: :Man
  AssignClass (f13bbbc0-61a9-4d49-af1c-8d84780753c6)
 Call ID: f13bbbc0-61a9-4d49-af1c-8d84780753c6
  Args:
    type: :Person
    source: Prince_Wolfgang_of_Hesse
  AssignClass (8add536a-c023-4e91-9d47-d221f319c044)
 Call ID: 8add536a-c023-4e91-9d47-d221f319c044
  Args:
    source: King_Charles_III_of_the_United_Kingdom
    type: :Man
  AssignClass (0b352f4b-f5bc-49be-9757-a40e7b98b3ec)
 Call ID: 0b352f4b-f5bc-49be-9757-a40e7b98b3ec
  Args:
    type: :Person
    source: King_Charles_III_of_the_United_Kingdom
  AssignClass (e9ab72b3-62a2-4635-989a-e6eedbd2910d)
 Call ID: e9ab72b3-62a2-4635-989a-e6eedbd2910d
  Args:
    source: King_Paul_of_Greece
    type: :Man
  AssignClass (f1177948-ac8a-48d5-9e74-43bd3cce81d5)
 Call ID: f1177948-ac8a-48d5-9e74-43bd3cce81d5
  Args:
    source: King_Paul_of_Greece
    type: :Person
  AssignClass (96ae5981-56d9-4015-82c7-007ea214058d)
 Call ID: 96ae5981-56d9-4015-82c7-007ea214058d
  Args:
    type: :Woman
    source: Queen_Frederica_of_Greece
  AssignClass (68eecbe5-7a1d-4287-91fc-4e001f602a16)
 Call ID: 68eecbe5-7a1d-4287-91fc-4e001f602a16
  Args:
    type: :Person
    source: Queen_Frederica_of_Greece
  Finish (49cceae3-6802-49c8-9a28-d9f6687cce12)
 Call ID: 49cceae3-6802-49c8-9a28-d9f6687cce12
  Args: