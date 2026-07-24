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
Emich Kyrill, Prince of Leiningen (German: Emich Kirill Ferdinand Hermann Fürst zu Leiningen; 18 October 1926 – 30 October 1991) was a German entrepreneur and son of Karl, Prince of Leiningen.
Early life

Emich was born at Coburg, Weimar Republic, the first child of Karl, Prince of Leiningen (1898–1946), (son of Emich, 5th Prince of Leiningen and Princess Feodore of Hohenlohe-Langenburg) and his wife, Grand Duchess Maria Kirillovna of Russia (1907–1951), (daughter of Grand Duke Kirill Vladimirovich of Russia and Princess Victoria Melita of Edinburgh).
Through his mother, he was a descendant of Queen Victoria and Tsar Alexander II.
Through his father, he was a descendant of the Vasa kings of Sweden and of both of Queen Victoria's half-siblings, Carl, Prince of Leiningen and Feodora, Princess of Hohenlohe-Langenburg.
As a result, Emich was the first descendant of all three of Princess Victoria of Saxe-Coburg-Saalfeld's children.
Marriage

Emich married on 10 August 1950 in Rastede to Duchess Eilika of Oldenburg (2 February 1928 – 26 January 2016), fourth child and second daughter of Nikolaus, Hereditary Grand Duke of Oldenburg and Princess Helena of Waldeck and Pyrmont.



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
  AssignClass (4aee4571-6ac0-4cfb-b895-72a4c8fc846f)
 Call ID: 4aee4571-6ac0-4cfb-b895-72a4c8fc846f
  Args:
    type: :Man
    source: Emich_Kyrill_Prince_of_Leiningen
  AddLiteral (dd8037e6-b6ac-4415-ac73-3c827465eb50)
 Call ID: dd8037e6-b6ac-4415-ac73-3c827465eb50
  Args:
    source: Emich_Kyrill_Prince_of_Leiningen
    relation: :hasBirthYear
    literal_value: 1926
    literal_type: xsd:integer
  AddLiteral (e2beaea4-63e8-48cd-8375-cbc9715e845f)
 Call ID: e2beaea4-63e8-48cd-8375-cbc9715e845f
  Args:
    relation: :hasDeathYear
    source: Emich_Kyrill_Prince_of_Leiningen
    literal_type: xsd:integer
    literal_value: 1991
  AssignClass (3067dd95-7848-4692-8147-a71187656511)
 Call ID: 3067dd95-7848-4692-8147-a71187656511
  Args:
    type: :Man
    source: Karl_Prince_of_Leiningen
  AddLiteral (2c149586-b4e5-4451-ba57-845cbc68c2a2)
 Call ID: 2c149586-b4e5-4451-ba57-845cbc68c2a2
  Args:
    literal_type: xsd:integer
    literal_value: 1898
    source: Karl_Prince_of_Leiningen
    relation: :hasBirthYear
  AddLiteral (b6d12eab-1985-45d6-8361-a062bcce51f1)
 Call ID: b6d12eab-1985-45d6-8361-a062bcce51f1
  Args:
    literal_type: xsd:integer
    literal_value: 1946
    relation: :hasDeathYear
    source: Karl_Prince_of_Leiningen
  AddTriple (af114bcc-03d4-4c97-8374-bb5bb5fb6655)
 Call ID: af114bcc-03d4-4c97-8374-bb5bb5fb6655
  Args:
    target: Karl_Prince_of_Leiningen
    source: Emich_Kyrill_Prince_of_Leiningen
    relation: :hasFather
  AssignClass (2bcfc5d3-bf93-4ea4-8c1a-a1b01a8cddec)
 Call ID: 2bcfc5d3-bf93-4ea4-8c1a-a1b01a8cddec
  Args:
    type: :Woman
    source: Maria_Kirillovna_of_Russia
  AddLiteral (ff735646-141d-491f-bd0b-be58e578eb5d)
 Call ID: ff735646-141d-491f-bd0b-be58e578eb5d
  Args:
    literal_type: xsd:integer
    literal_value: 1907
    relation: :hasBirthYear
    source: Maria_Kirillovna_of_Russia
  AddLiteral (27098a8c-f54c-46a1-b8ae-e59eb12b8ceb)
 Call ID: 27098a8c-f54c-46a1-b8ae-e59eb12b8ceb
  Args:
    literal_type: xsd:integer
    literal_value: 1951
    source: Maria_Kirillovna_of_Russia
    relation: :hasDeathYear
  AddTriple (9c19a184-d0f1-4dce-afbb-b71244e92930)
 Call ID: 9c19a184-d0f1-4dce-afbb-b71244e92930
  Args:
    source: Emich_Kyrill_Prince_of_Leiningen
    relation: :hasMother
    target: Maria_Kirillovna_of_Russia
  AssignClass (3e4804d4-51fe-4fe2-8c28-3bc44a3b8d91)
 Call ID: 3e4804d4-51fe-4fe2-8c28-3bc44a3b8d91
  Args:
    type: :Man
    source: Emich_5th_Prince_of_Leiningen
  AddTriple (91348a84-6a06-4bff-918c-e91a830eabc3)
 Call ID: 91348a84-6a06-4bff-918c-e91a830eabc3
  Args:
    source: Karl_Prince_of_Leiningen
    relation: :hasFather
    target: Emich_5th_Prince_of_Leiningen
  AssignClass (d61ab977-5069-4b01-aa74-7ac14497b992)
 Call ID: d61ab977-5069-4b01-aa74-7ac14497b992
  Args:
    type: :Woman
    source: Princess_Feodore_of_Hohenlohe_Langenburg
  AddTriple (592bc50d-a824-4ad7-ad1e-9af83a57f0ba)
 Call ID: 592bc50d-a824-4ad7-ad1e-9af83a57f0ba
  Args:
    relation: :hasMother
    source: Karl_Prince_of_Leiningen
    target: Princess_Feodore_of_Hohenlohe_Langenburg
  AssignClass (b533143c-2afd-4e4c-9c77-0b4acddcc922)
 Call ID: b533143c-2afd-4e4c-9c77-0b4acddcc922
  Args:
    type: :Man
    source: Grand_Duke_Kirill_Vladimirovich_of_Russia
  AddTriple (99310039-b3aa-4448-ae39-1e933a95df49)
 Call ID: 99310039-b3aa-4448-ae39-1e933a95df49
  Args:
    target: Grand_Duke_Kirill_Vladimirovich_of_Russia
    source: Maria_Kirillovna_of_Russia
    relation: :hasFather
  AssignClass (743388cc-69bb-40f1-b18b-9566f8665d1e)
 Call ID: 743388cc-69bb-40f1-b18b-9566f8665d1e
  Args:
    type: :Woman
    source: Princess_Victoria_Melita_of_Edinburgh
  AddTriple (acc58773-bbe3-4d3f-a107-ae38beca8388)
 Call ID: acc58773-bbe3-4d3f-a107-ae38beca8388
  Args:
    source: Maria_Kirillovna_of_Russia
    relation: :hasMother
    target: Princess_Victoria_Melita_of_Edinburgh
  AssignClass (ee70b1ca-7cd8-4615-b286-fd2321d9957a)
 Call ID: ee70b1ca-7cd8-4615-b286-fd2321d9957a
  Args:
    type: :Woman
    source: Duchess_Eilika_of_Oldenburg
  AddLiteral (e241dc0c-2c98-47da-abc6-0dd0e49cb93c)
 Call ID: e241dc0c-2c98-47da-abc6-0dd0e49cb93c
  Args:
    literal_type: xsd:integer
    literal_value: 1928
    source: Duchess_Eilika_of_Oldenburg
    relation: :hasBirthYear
  AddLiteral (df8979dc-f298-4e0c-90b0-9bf7436e8413)
 Call ID: df8979dc-f298-4e0c-90b0-9bf7436e8413
  Args:
    relation: :hasDeathYear
    source: Duchess_Eilika_of_Oldenburg
    literal_value: 2016
    literal_type: xsd:integer
  AddTriple (debc8566-240d-4864-9281-e0269f024a17)
 Call ID: debc8566-240d-4864-9281-e0269f024a17
  Args:
    relation: :hasRelation
    source: Emich_Kyrill_Prince_of_Leiningen
    target: Duchess_Eilika_of_Oldenburg
  AddLiteral (f6490c90-201c-4a49-b3f5-d0bce2b0efa2)
 Call ID: f6490c90-201c-4a49-b3f5-d0bce2b0efa2
  Args:
    literal_value: 1950
    literal_type: xsd:integer
    relation: :hasMarriageYear
    source: Emich_Kyrill_Prince_of_Leiningen
  AssignClass (0af25815-fde1-4cf2-80de-e5375965be2e)
 Call ID: 0af25815-fde1-4cf2-80de-e5375965be2e
  Args:
    type: :Man
    source: Nikolaus_Hereditary_Grand_Duke_of_Oldenburg
  AddTriple (82f12d4f-30b3-4504-941c-617511c2dc57)
 Call ID: 82f12d4f-30b3-4504-941c-617511c2dc57
  Args:
    relation: :hasFather
    source: Duchess_Eilika_of_Oldenburg
    target: Nikolaus_Hereditary_Grand_Duke_of_Oldenburg
  AssignClass (1804a74c-87bd-4516-852e-0c86157658b5)
 Call ID: 1804a74c-87bd-4516-852e-0c86157658b5
  Args:
    type: :Woman
    source: Princess_Helena_of_Waldeck_and_Pyrmont
  AddTriple (22c9ffc4-c82c-4f66-852e-f57192180f11)
 Call ID: 22c9ffc4-c82c-4f66-852e-f57192180f11
  Args:
    target: Princess_Helena_of_Waldeck_and_Pyrmont
    relation: :hasMother
    source: Duchess_Eilika_of_Oldenburg
  Finish (118f79b4-18e3-45df-adcd-c87a202bcc48)
 Call ID: 118f79b4-18e3-45df-adcd-c87a202bcc48
  Args: