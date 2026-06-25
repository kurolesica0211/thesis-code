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
  AssignClass (edbb221f-d263-4caf-825e-64672619a605)
 Call ID: edbb221f-d263-4caf-825e-64672619a605
  Args:
    type: :Man
    source: :KarlAdolfAndreasOfHesse
  AssignClass (895ff726-f668-45ca-becf-d6d6601e0ac7)
 Call ID: 895ff726-f668-45ca-becf-d6d6601e0ac7
  Args:
    type: :Person
    source: :KarlAdolfAndreasOfHesse
  AddLiteral (17c0adbe-43aa-44c8-b28b-fb1f5e501acd)
 Call ID: 17c0adbe-43aa-44c8-b28b-fb1f5e501acd
  Args:
    source: :KarlAdolfAndreasOfHesse
    literal_value: 1937
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (d224fd82-a314-4aa4-823b-1bc4ccc98260)
 Call ID: d224fd82-a314-4aa4-823b-1bc4ccc98260
  Args:
    literal_value: 2022
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: :KarlAdolfAndreasOfHesse
  AssignClass (a6e0e23d-e722-4f8d-aa1b-1b66025e3770)
 Call ID: a6e0e23d-e722-4f8d-aa1b-1b66025e3770
  Args:
    source: :PrinceChristophOfHesse
    type: :Man
  AssignClass (20912adb-a074-4e9e-a92f-596ae91e104c)
 Call ID: 20912adb-a074-4e9e-a92f-596ae91e104c
  Args:
    type: :Person
    source: :PrinceChristophOfHesse
  AssignClass (55117533-bcb3-44ae-8bae-daa1007c4532)
 Call ID: 55117533-bcb3-44ae-8bae-daa1007c4532
  Args:
    source: :PrincessSophieOfGreeceAndDenmark
    type: :Woman
  AssignClass (c59bbaa0-2502-45d0-9fe8-95b619b2859b)
 Call ID: c59bbaa0-2502-45d0-9fe8-95b619b2859b
  Args:
    type: :Person
    source: :PrincessSophieOfGreeceAndDenmark
  AddTriple (31c844e9-f3e5-4a46-a897-d8ff7b9443db)
 Call ID: 31c844e9-f3e5-4a46-a897-d8ff7b9443db
  Args:
    source: :KarlAdolfAndreasOfHesse
    relation: :hasFather
    target: :PrinceChristophOfHesse
  AddTriple (5e446d11-982a-45bf-81dc-c57ed3d20b98)
 Call ID: 5e446d11-982a-45bf-81dc-c57ed3d20b98
  Args:
    source: :KarlAdolfAndreasOfHesse
    target: :PrincessSophieOfGreeceAndDenmark
    relation: :hasMother
  AssignClass (2bf9d775-508f-442d-a2e3-018bd236e731)
 Call ID: 2bf9d775-508f-442d-a2e3-018bd236e731
  Args:
    source: :PrincePhilipDukeOfEdinburgh
    type: :Man
  AssignClass (09d723d6-f721-4f0e-8dce-5fe20b20ecbf)
 Call ID: 09d723d6-f721-4f0e-8dce-5fe20b20ecbf
  Args:
    type: :Person
    source: :PrincePhilipDukeOfEdinburgh
  AddTriple (3a1c6264-6a05-45b0-b429-6c9c1826d7dc)
 Call ID: 3a1c6264-6a05-45b0-b429-6c9c1826d7dc
  Args:
    relation: :isSisterOf
    target: :PrincePhilipDukeOfEdinburgh
    source: :PrincessSophieOfGreeceAndDenmark
  AssignClass (a158b0c2-9f9a-4ea3-aa29-157f721e8801)
 Call ID: a158b0c2-9f9a-4ea3-aa29-157f721e8801
  Args:
    type: :Man
    source: :PrinceWolfgangOfHesse
  AssignClass (ed7fb145-d8ee-4e64-bb04-19d34383273a)
 Call ID: ed7fb145-d8ee-4e64-bb04-19d34383273a
  Args:
    source: :PrinceWolfgangOfHesse
    type: :Person
  AddTriple (23d1b632-3735-42c1-8870-66f9d3782492)
 Call ID: 23d1b632-3735-42c1-8870-66f9d3782492
  Args:
    target: :PrinceChristophOfHesse
    relation: :isBrotherOf
    source: :PrinceWolfgangOfHesse
  AssignClass (dee5f83c-2b65-4db5-afb2-79a41171eecd)
 Call ID: dee5f83c-2b65-4db5-afb2-79a41171eecd
  Args:
    source: :PrinceGeorgeWilliamOfHanover
    type: :Man
  AssignClass (92bd2844-567a-44f0-8be3-a595f2c82fdb)
 Call ID: 92bd2844-567a-44f0-8be3-a595f2c82fdb
  Args:
    source: :PrinceGeorgeWilliamOfHanover
    type: :Person
  AddLiteral (13b829e0-582c-4733-b9a9-fa2791176e52)
 Call ID: 13b829e0-582c-4733-b9a9-fa2791176e52
  Args:
    literal_value: 1946
    literal_type: xsd:integer
    relation: :hasMarriageYear
    source: :PrincessSophieOfGreeceAndDenmark
  AddTriple (03b76e99-e6b2-455f-a85b-93b1ce62f8b0)
 Call ID: 03b76e99-e6b2-455f-a85b-93b1ce62f8b0
  Args:
    target: :PrinceGeorgeWilliamOfHanover
    relation: :hasRelation
    source: :PrincessSophieOfGreeceAndDenmark
  AssignClass (33e1aec7-3876-49e2-9898-ead3aaad66e9)
 Call ID: 33e1aec7-3876-49e2-9898-ead3aaad66e9
  Args:
    type: :Man
    source: :KingPaulOfGreece
  AssignClass (104545c7-7a86-4f19-a478-73fbe90c016d)
 Call ID: 104545c7-7a86-4f19-a478-73fbe90c016d
  Args:
    type: :Person
    source: :KingPaulOfGreece
  AssignClass (614506fd-01a8-4c81-913f-66ecd718212a)
 Call ID: 614506fd-01a8-4c81-913f-66ecd718212a
  Args:
    type: :Woman
    source: :QueenFrederica
  AssignClass (58df755c-f3f4-4001-bcf8-c70c9837aac3)
 Call ID: 58df755c-f3f4-4001-bcf8-c70c9837aac3
  Args:
    type: :Person
    source: :QueenFrederica
  AssignClass (49a747cb-64f5-42be-a85c-100329ec1e1d)
 Call ID: 49a747cb-64f5-42be-a85c-100329ec1e1d
  Args:
    source: :KingCharlesIII
    type: :Man
  AssignClass (5ee4df64-ca5a-45aa-8d99-1ed75df39ff4)
 Call ID: 5ee4df64-ca5a-45aa-8d99-1ed75df39ff4
  Args:
    source: :KingCharlesIII
    type: :Person
  Finish (cbdcc5ad-421f-47f2-9ea1-d166b0c5cb74)
 Call ID: cbdcc5ad-421f-47f2-9ea1-d166b0c5cb74
  Args: