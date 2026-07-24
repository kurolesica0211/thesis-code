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
  AssignClass (d6614ba9-7482-415c-b97d-c139ff7e80c9)
 Call ID: d6614ba9-7482-415c-b97d-c139ff7e80c9
  Args:
    type: :Person
    source: :Josephine_of_Denmark
  AssignClass (260da488-9b58-429d-9f81-01d0c8727083)
 Call ID: 260da488-9b58-429d-9f81-01d0c8727083
  Args:
    type: :Woman
    source: :Josephine_of_Denmark
  AssignClass (1990fcf2-2a81-43b7-8f9a-624f0c5d7776)
 Call ID: 1990fcf2-2a81-43b7-8f9a-624f0c5d7776
  Args:
    type: :Person
    source: :Frederik_X
  AssignClass (fe61a28f-7f65-4b02-8e0a-6cc4a1e14a21)
 Call ID: fe61a28f-7f65-4b02-8e0a-6cc4a1e14a21
  Args:
    type: :Man
    source: :Frederik_X
  AssignClass (a3840475-8022-4db7-8f75-8ff709889681)
 Call ID: a3840475-8022-4db7-8f75-8ff709889681
  Args:
    type: :Person
    source: :Mary_of_Denmark
  AssignClass (3a16bbb4-91ca-4360-9dd5-5e20c9ad1adf)
 Call ID: 3a16bbb4-91ca-4360-9dd5-5e20c9ad1adf
  Args:
    type: :Woman
    source: :Mary_of_Denmark
  AssignClass (135d317b-9c10-40b4-b375-dd10d4f2b3e2)
 Call ID: 135d317b-9c10-40b4-b375-dd10d4f2b3e2
  Args:
    type: :Person
    source: :Margrethe_II
  AssignClass (f9d8048a-c8f6-4dc8-b2b9-bdc9c172e3f6)
 Call ID: f9d8048a-c8f6-4dc8-b2b9-bdc9c172e3f6
  Args:
    type: :Woman
    source: :Margrethe_II
  AssignClass (6fe53fb1-bfd6-4aea-9d54-ab532b040bcc)
 Call ID: 6fe53fb1-bfd6-4aea-9d54-ab532b040bcc
  Args:
    type: :Person
    source: :Henrik_of_Denmark
  AssignClass (33928ef3-c5e2-44a4-9ec5-7eb79fe11944)
 Call ID: 33928ef3-c5e2-44a4-9ec5-7eb79fe11944
  Args:
    type: :Man
    source: :Henrik_of_Denmark
  AssignClass (62e531a2-096f-47b9-ac42-b19f3b8efdbb)
 Call ID: 62e531a2-096f-47b9-ac42-b19f3b8efdbb
  Args:
    type: :Person
    source: :Vincent_of_Denmark
  AssignClass (2c370fad-79ad-48f7-a07e-ce3eeaac9923)
 Call ID: 2c370fad-79ad-48f7-a07e-ce3eeaac9923
  Args:
    type: :Man
    source: :Vincent_of_Denmark
  AssignClass (59cfc7a9-e821-4a6a-a834-228ab7d2f31b)
 Call ID: 59cfc7a9-e821-4a6a-a834-228ab7d2f31b
  Args:
    type: :Person
    source: :Christian_of_Denmark
  AssignClass (88c918c3-2f06-4e3d-970a-b230d1ddf1ec)
 Call ID: 88c918c3-2f06-4e3d-970a-b230d1ddf1ec
  Args:
    type: :Man
    source: :Christian_of_Denmark
  AssignClass (2eaeb9bf-82db-4201-9f57-6bb802cc285d)
 Call ID: 2eaeb9bf-82db-4201-9f57-6bb802cc285d
  Args:
    type: :Person
    source: :Isabella_of_Denmark
  AssignClass (41278ac5-1ef5-409e-85cc-783fb67ff84e)
 Call ID: 41278ac5-1ef5-409e-85cc-783fb67ff84e
  Args:
    type: :Woman
    source: :Isabella_of_Denmark
  AssignClass (553b36a8-6f7e-4437-ad38-14077305da9d)
 Call ID: 553b36a8-6f7e-4437-ad38-14077305da9d
  Args:
    type: :Person
    source: :Ingrid_of_Denmark
  AssignClass (42fd08dd-e799-45dd-949d-b07f3f481e86)
 Call ID: 42fd08dd-e799-45dd-949d-b07f3f481e86
  Args:
    type: :Woman
    source: :Ingrid_of_Denmark
  AddLiteral (3700147d-9b15-4140-890e-e471bacb94bb)
 Call ID: 3700147d-9b15-4140-890e-e471bacb94bb
  Args:
    relation: :hasBirthYear
    literal_value: 2011
    source: :Josephine_of_Denmark
    literal_type: xsd:integer
  AddTriple (5b28e62d-fc9d-4962-8959-9fecf3a06e8f)
 Call ID: 5b28e62d-fc9d-4962-8959-9fecf3a06e8f
  Args:
    target: :Frederik_X
    source: :Josephine_of_Denmark
    relation: :hasFather
  AddTriple (f1f11f63-ca15-41ad-8601-5c5f06e8d6fc)
 Call ID: f1f11f63-ca15-41ad-8601-5c5f06e8d6fc
  Args:
    relation: :hasMother
    target: :Mary_of_Denmark
    source: :Josephine_of_Denmark
  AddTriple (220ee709-2151-49aa-8e1a-e9dd2591b612)
 Call ID: 220ee709-2151-49aa-8e1a-e9dd2591b612
  Args:
    relation: :isSisterOf
    target: :Vincent_of_Denmark
    source: :Josephine_of_Denmark
  AddTriple (7d06e336-3d1a-41d4-ac46-b9a38add7d26)
 Call ID: 7d06e336-3d1a-41d4-ac46-b9a38add7d26
  Args:
    source: :Josephine_of_Denmark
    target: :Christian_of_Denmark
    relation: :isSisterOf
  AddTriple (d15d3fc1-0126-4718-854c-85755b988d27)
 Call ID: d15d3fc1-0126-4718-854c-85755b988d27
  Args:
    target: :Isabella_of_Denmark
    source: :Josephine_of_Denmark
    relation: :isSisterOf
  AddTriple (c6131ad1-3c37-4658-9e0e-cda2f1ba5c78)
 Call ID: c6131ad1-3c37-4658-9e0e-cda2f1ba5c78
  Args:
    target: :Josephine_of_Denmark
    source: :Vincent_of_Denmark
    relation: :isBrotherOf
  AddTriple (b1c6b7af-9adc-4d83-8fce-9382e2fd428b)
 Call ID: b1c6b7af-9adc-4d83-8fce-9382e2fd428b
  Args:
    source: :Josephine_of_Denmark
    target: :Margrethe_II
    relation: :hasAncestor
  AddTriple (1188796b-7af7-44f2-b46d-11f07bc1f83f)
 Call ID: 1188796b-7af7-44f2-b46d-11f07bc1f83f
  Args:
    relation: :hasAncestor
    target: :Henrik_of_Denmark
    source: :Josephine_of_Denmark
  AddTriple (41e6a72a-4b00-4a3b-ad37-48d7ebc7a96a)
 Call ID: 41e6a72a-4b00-4a3b-ad37-48d7ebc7a96a
  Args:
    relation: :hasAncestor
    source: :Josephine_of_Denmark
    target: :Ingrid_of_Denmark
  Finish (04538aa7-76ef-4247-9860-81fc62a1b410)
 Call ID: 04538aa7-76ef-4247-9860-81fc62a1b410
  Args: