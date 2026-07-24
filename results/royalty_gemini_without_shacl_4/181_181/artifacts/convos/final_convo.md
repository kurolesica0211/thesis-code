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
  AssignClass (6111f43f-1d87-4410-8c14-b1326f0f05db)
 Call ID: 6111f43f-1d87-4410-8c14-b1326f0f05db
  Args:
    type: :Man
    source: Karl_Adolf_Andreas_Prinz_von_Hesse
  AssignClass (19535c7c-c8c0-41c4-bcaf-2630e9f2ca05)
 Call ID: 19535c7c-c8c0-41c4-bcaf-2630e9f2ca05
  Args:
    type: :Person
    source: Karl_Adolf_Andreas_Prinz_von_Hesse
  AddLiteral (b97d38ca-39d8-4062-b59d-4d3eab68bd16)
 Call ID: b97d38ca-39d8-4062-b59d-4d3eab68bd16
  Args:
    relation: :hasBirthYear
    literal_value: 1937
    source: Karl_Adolf_Andreas_Prinz_von_Hesse
    literal_type: xsd:integer
  AddLiteral (f43c7f96-46e4-4530-8013-5fbcd6362eda)
 Call ID: f43c7f96-46e4-4530-8013-5fbcd6362eda
  Args:
    literal_type: xsd:integer
    source: Karl_Adolf_Andreas_Prinz_von_Hesse
    literal_value: 2022
    relation: :hasDeathYear
  AssignClass (a2bdf2fc-e121-4769-aaf4-50ddc181a2c6)
 Call ID: a2bdf2fc-e121-4769-aaf4-50ddc181a2c6
  Args:
    type: :Man
    source: Christoph_of_Hesse
  AssignClass (0b34f1a1-c550-4a0d-a7bb-fdd6ce7cf325)
 Call ID: 0b34f1a1-c550-4a0d-a7bb-fdd6ce7cf325
  Args:
    type: :Person
    source: Christoph_of_Hesse
  AssignClass (e5f9f37e-099e-4dfb-97bf-3af5f864b387)
 Call ID: e5f9f37e-099e-4dfb-97bf-3af5f864b387
  Args:
    type: :Woman
    source: Sophie_of_Greece_and_Denmark
  AssignClass (f3055fa4-8e07-44fe-893c-1f5a0375b682)
 Call ID: f3055fa4-8e07-44fe-893c-1f5a0375b682
  Args:
    type: :Person
    source: Sophie_of_Greece_and_Denmark
  AddTriple (e12b31d7-69fc-4a85-b0a1-e9c9f7f46900)
 Call ID: e12b31d7-69fc-4a85-b0a1-e9c9f7f46900
  Args:
    source: Karl_Adolf_Andreas_Prinz_von_Hesse
    target: Christoph_of_Hesse
    relation: :hasFather
  AddTriple (c73a3ee8-7b89-4cbc-b35b-3d5a8ecfe1ee)
 Call ID: c73a3ee8-7b89-4cbc-b35b-3d5a8ecfe1ee
  Args:
    relation: :hasMother
    source: Karl_Adolf_Andreas_Prinz_von_Hesse
    target: Sophie_of_Greece_and_Denmark
  AssignClass (be77de68-80f8-4ccf-ba4c-4f97cbc6c98a)
 Call ID: be77de68-80f8-4ccf-ba4c-4f97cbc6c98a
  Args:
    type: :Man
    source: Prince_Philip
  AssignClass (21e867d4-da19-4b1f-a039-8edd2d481791)
 Call ID: 21e867d4-da19-4b1f-a039-8edd2d481791
  Args:
    type: :Person
    source: Prince_Philip
  AddTriple (aca5e81d-98db-47c6-b7e3-72259f4057f8)
 Call ID: aca5e81d-98db-47c6-b7e3-72259f4057f8
  Args:
    target: Sophie_of_Greece_and_Denmark
    source: Prince_Philip
    relation: :hasSister
  AssignClass (1d9365b3-01d4-4e2c-8b17-689ecaf8b70c)
 Call ID: 1d9365b3-01d4-4e2c-8b17-689ecaf8b70c
  Args:
    type: :Man
    source: George_William_of_Hanover
  AssignClass (95400700-b60b-4092-8aa2-eea0c954a0aa)
 Call ID: 95400700-b60b-4092-8aa2-eea0c954a0aa
  Args:
    type: :Person
    source: George_William_of_Hanover
  AssignClass (12e5bc5a-e723-474f-bc46-43346f8009cf)
 Call ID: 12e5bc5a-e723-474f-bc46-43346f8009cf
  Args:
    type: :Man
    source: Wolfgang_of_Hesse
  AssignClass (fc886ac7-7995-4fa4-bdd1-9dbfa378bf2e)
 Call ID: fc886ac7-7995-4fa4-bdd1-9dbfa378bf2e
  Args:
    type: :Person
    source: Wolfgang_of_Hesse
  AssignClass (737b99e9-da57-4ffb-a7a7-2f9886a89d29)
 Call ID: 737b99e9-da57-4ffb-a7a7-2f9886a89d29
  Args:
    type: :Man
    source: King_Charles_III
  AssignClass (5c4cd21b-076c-4842-9ce8-94750052e7c8)
 Call ID: 5c4cd21b-076c-4842-9ce8-94750052e7c8
  Args:
    type: :Person
    source: King_Charles_III
  AssignClass (699f0a50-3414-43c7-b9b6-d716a7e77c61)
 Call ID: 699f0a50-3414-43c7-b9b6-d716a7e77c61
  Args:
    type: :Man
    source: Wilhelm_II
  AssignClass (b2f55bcd-d3eb-4abc-ad92-a96f7a9ac203)
 Call ID: b2f55bcd-d3eb-4abc-ad92-a96f7a9ac203
  Args:
    type: :Person
    source: Wilhelm_II
  AssignClass (a6c18473-9248-48ba-a7eb-12580dadcae4)
 Call ID: a6c18473-9248-48ba-a7eb-12580dadcae4
  Args:
    type: :Man
    source: King_Paul_of_Greece
  AssignClass (24cd4fad-9f50-4383-b8ba-cdb3fb928a2f)
 Call ID: 24cd4fad-9f50-4383-b8ba-cdb3fb928a2f
  Args:
    type: :Person
    source: King_Paul_of_Greece
  AssignClass (bc326a6a-cbf9-4b1e-8b4f-87885616cb98)
 Call ID: bc326a6a-cbf9-4b1e-8b4f-87885616cb98
  Args:
    type: :Woman
    source: Queen_Frederica
  AssignClass (d0855d43-bee9-4f12-8bc3-8b7fa00d31e7)
 Call ID: d0855d43-bee9-4f12-8bc3-8b7fa00d31e7
  Args:
    type: :Person
    source: Queen_Frederica
  Finish (59973fd8-3b79-4ae8-9d31-1541ef72cefc)
 Call ID: 59973fd8-3b79-4ae8-9d31-1541ef72cefc
  Args: