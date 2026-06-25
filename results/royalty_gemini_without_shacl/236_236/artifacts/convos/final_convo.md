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
Princess Josephine of Denmark, Countess of Monpezat RE (Josephine Sophia Ivalo Mathilda; born 8 January 2011) is a member of the Danish royal family.
She is the fourth and youngest child of King Frederik X and Queen Mary, and the seventh grandchild of Queen Margrethe II and Prince Henrik.
She is the twin sister of Prince Vincent.
Josephine is fourth in line to the Danish throne, after her older siblings, Crown Prince Christian and Princess Isabella, and her elder twin brother, Prince Vincent.
Birth and christening

Queen Margrethe II


Josephine was born on 8 January 2011 at Rigshospitalet, the Copenhagen University Hospital, in Copenhagen, at 10:56 am local time, 26 minutes after her twin brother.
Josephine and Vincent were baptised on 14 April at the Church of Holmen in central Copenhagen by the royal confessor, the Bishop of Copenhagen Erik Norman Svendsen.
The twins were baptised at the royal baptismal font which has been used for the baptism of royal children in Denmark since 1671.
Princess Josephine wore a christening gown found among her great-grandmother Queen Ingrid's belongings, making her the first child of a future Danish monarch not to wear the Danish royal family's traditional christening gown (which was worn by her twin brother) since it was taken into use in 1870.
The Princess's name was announced as Josephine Sophia Ivalo Mathilda.
Her godparents are her paternal aunt, Princess Marie of Denmark; her maternal aunt, Patricia Bailey; as well as her parents' friends Prince Carlo, Duke of Castro, Count Bendt Wedell, Birgitte Handwerk and Josephine Rechner.
Public appearances and education

On 3 August 2014, during the family's official visit to Greenland, Josephine, her parents and siblings, took part in a tree planting in Qaqortoq's new poplar grove, Ivalos og Miniks Poppellund, named after Josephine and her brother who are known by their Greenlandic middle names in Greenland.
On 15 August 2017, Josephine and her twin brother started school at Tranegårdsskolen in Gentofte – the same public school as her older siblings.
In August 2023, the Royal House announced that Josephine would be starting at Kildegård Privatskole in Hellerup in September 2023.
Both Josephine and her twin brother were confirmed on 18 April 2026.
Titles, styles, and honours

Josephine is styled as Her Royal Highness Princess Josephine of Denmark, Countess of Monpezat.



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
  AssignClass (fb101e4f-c4db-42b3-b719-4a9afab70c18)
 Call ID: fb101e4f-c4db-42b3-b719-4a9afab70c18
  Args:
    source: :Princess_Josephine_of_Denmark
    type: :Woman
  AssignClass (16eec8e1-cd39-4973-91ec-33c7e325e23a)
 Call ID: 16eec8e1-cd39-4973-91ec-33c7e325e23a
  Args:
    type: :Person
    source: :Princess_Josephine_of_Denmark
  AddLiteral (4a3a8cf2-776b-4bc0-a3bd-83bda4f4c524)
 Call ID: 4a3a8cf2-776b-4bc0-a3bd-83bda4f4c524
  Args:
    literal_value: 2011
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: :Princess_Josephine_of_Denmark
  AssignClass (de8517ec-d005-4bb4-b65a-eb2bb407313f)
 Call ID: de8517ec-d005-4bb4-b65a-eb2bb407313f
  Args:
    source: :King_Frederik_X
    type: :Man
  AssignClass (72fd9d09-802e-47cb-9645-bb3e41f14c11)
 Call ID: 72fd9d09-802e-47cb-9645-bb3e41f14c11
  Args:
    type: :Person
    source: :King_Frederik_X
  AssignClass (d53331ee-00c1-44af-abeb-9836ef615225)
 Call ID: d53331ee-00c1-44af-abeb-9836ef615225
  Args:
    source: :Queen_Mary
    type: :Woman
  AssignClass (243f5743-2bb6-4eb0-97c6-421e87a52c37)
 Call ID: 243f5743-2bb6-4eb0-97c6-421e87a52c37
  Args:
    type: :Person
    source: :Queen_Mary
  AddTriple (2fb95ea0-d180-44fd-b7c2-c88d43120ed7)
 Call ID: 2fb95ea0-d180-44fd-b7c2-c88d43120ed7
  Args:
    source: :Princess_Josephine_of_Denmark
    target: :King_Frederik_X
    relation: :hasFather
  AddTriple (7ca92aa3-8762-4a4d-8408-1d8d421b39df)
 Call ID: 7ca92aa3-8762-4a4d-8408-1d8d421b39df
  Args:
    source: :Princess_Josephine_of_Denmark
    target: :Queen_Mary
    relation: :hasMother
  AssignClass (6b109563-4ca9-4ee5-9508-05993f53a08a)
 Call ID: 6b109563-4ca9-4ee5-9508-05993f53a08a
  Args:
    type: :Woman
    source: :Queen_Margrethe_II
  AssignClass (c8fae057-9b29-46df-a55a-cb0b77a36865)
 Call ID: c8fae057-9b29-46df-a55a-cb0b77a36865
  Args:
    source: :Queen_Margrethe_II
    type: :Person
  AssignClass (74bcff33-7cbc-4476-b5c0-16eda3b26932)
 Call ID: 74bcff33-7cbc-4476-b5c0-16eda3b26932
  Args:
    type: :Man
    source: :Prince_Henrik
  AssignClass (6ded8a2a-696b-430a-9ad8-17204bd34bad)
 Call ID: 6ded8a2a-696b-430a-9ad8-17204bd34bad
  Args:
    type: :Person
    source: :Prince_Henrik
  AssignClass (113bb7b7-c217-4ebe-82f8-b1b729e80771)
 Call ID: 113bb7b7-c217-4ebe-82f8-b1b729e80771
  Args:
    source: :Prince_Vincent
    type: :Man
  AssignClass (4f3393e4-32d5-46ab-b9ce-6cde4b59471f)
 Call ID: 4f3393e4-32d5-46ab-b9ce-6cde4b59471f
  Args:
    type: :Person
    source: :Prince_Vincent
  AddTriple (c0c4f429-3076-4afd-bbfd-a05762419e89)
 Call ID: c0c4f429-3076-4afd-bbfd-a05762419e89
  Args:
    source: :Princess_Josephine_of_Denmark
    target: :Prince_Vincent
    relation: :isSiblingOf
  AssignClass (52e11747-786c-4dcb-9de1-5b18db11df2c)
 Call ID: 52e11747-786c-4dcb-9de1-5b18db11df2c
  Args:
    source: :Crown_Prince_Christian
    type: :Man
  AssignClass (c04c7532-37c3-4a6f-aa63-2a429473e771)
 Call ID: c04c7532-37c3-4a6f-aa63-2a429473e771
  Args:
    type: :Person
    source: :Crown_Prince_Christian
  AssignClass (5f85e1c4-6889-436c-a1d8-79cd711c6832)
 Call ID: 5f85e1c4-6889-436c-a1d8-79cd711c6832
  Args:
    type: :Woman
    source: :Princess_Isabella
  AssignClass (dece663d-cd16-4600-b801-4d34553401a0)
 Call ID: dece663d-cd16-4600-b801-4d34553401a0
  Args:
    source: :Princess_Isabella
    type: :Person
  AddTriple (32d9ba7f-1adb-4c93-92f6-e0d7bf935ebf)
 Call ID: 32d9ba7f-1adb-4c93-92f6-e0d7bf935ebf
  Args:
    source: :Princess_Josephine_of_Denmark
    target: :Crown_Prince_Christian
    relation: :isSiblingOf
  AddTriple (d35aa975-34f8-4baf-882f-5eaf22e86fad)
 Call ID: d35aa975-34f8-4baf-882f-5eaf22e86fad
  Args:
    source: :Princess_Josephine_of_Denmark
    target: :Princess_Isabella
    relation: :isSiblingOf
  AssignClass (76ba4e94-eb95-48b6-a0f1-5fa585ee155f)
 Call ID: 76ba4e94-eb95-48b6-a0f1-5fa585ee155f
  Args:
    type: :Woman
    source: :Queen_Ingrid
  AssignClass (b38f3d87-aff6-46e7-aec7-f604f23d8f1d)
 Call ID: b38f3d87-aff6-46e7-aec7-f604f23d8f1d
  Args:
    source: :Queen_Ingrid
    type: :Person
  AssignClass (b51a85ca-4519-407c-972d-6090a62e5235)
 Call ID: b51a85ca-4519-407c-972d-6090a62e5235
  Args:
    type: :Woman
    source: :Princess_Marie_of_Denmark
  AssignClass (e2ba4a4d-b99c-4a04-9e48-1abdd922c1a5)
 Call ID: e2ba4a4d-b99c-4a04-9e48-1abdd922c1a5
  Args:
    source: :Princess_Marie_of_Denmark
    type: :Person
  AssignClass (d0238734-8819-4233-babb-03c2e76d34f6)
 Call ID: d0238734-8819-4233-babb-03c2e76d34f6
  Args:
    type: :Woman
    source: :Patricia_Bailey
  AssignClass (c01fed10-1a59-45f6-b750-17d12ff0163d)
 Call ID: c01fed10-1a59-45f6-b750-17d12ff0163d
  Args:
    source: :Patricia_Bailey
    type: :Person
  Finish (063b1ddd-7b65-4bd2-88a8-9f98fe2e6a2a)
 Call ID: 063b1ddd-7b65-4bd2-88a8-9f98fe2e6a2a
  Args: