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
Count Christian of Rosenborg  (Christian Frederik Franz Knud Harald Carl Oluf Gustav Georg Erik; 22 October 1942 – 21 May 2013) was a member of the Danish royal family.
Born Prince Christian of Denmark, from 1947 he was third in the line of line of succession until the constitution was changed in 1953 to allow females to inherit the crown, placing his branch of the dynasty behind that of his cousin Margrethe and her two younger sisters.
Family

He was born at Sorgenfri Palace, Sorgenfri, as the younger son of Hereditary Prince Knud by his wife and first cousin, Princess Caroline-Mathilde of Denmark.
Loss of place in succession

From the death of his grandfather in 1947, Christian stood only behind his father and elder brother Prince Ingolf in the order of hereditary succession to the throne, with only future children of Ingolf possibly taking a place ahead of him.
His father Prince Knud was then the heir presumptive, due to succeed Christian's uncle King Frederik IX, who had three daughters but no sons.
In 1953, the Constitution of Denmark was amended to allow cognatic primogeniture.
The new law made thirteen-year-old Princess Margrethe the new heir presumptive, placing her and her two sisters before Prince Knud and his family in the succession.
Christian was thus relegated to sixth in the line of succession to the Danish throne, but more importantly, he then ranked behind Margrethe and others who were likely to have dynastic children of their own (as has, in fact, happened).
The princess became Queen Margrethe II in 1972 and reigned until her abdication in 2024.
Christian's place in the line of succession, if he had been still eligible, would have been no higher than thirteenth in 2013.
Marriage, loss of dynastic rights and children

By 1971, Princess Margrethe had produced two children, pushing Christian to 8th in the line of succession.
The king's permission to marry was not sought because it was expected to be denied, since Christian's fiancée was an untitled commoner.
Prior to his elder son's wedding in 1968, Prince Knud sought to convince his brother that Ingolf should be allowed to retain his royal title after his non-dynastic marriage, a privilege which might have been subsequently extended to Christian.
But the king refused, on the grounds that other males of the dynasty, who had been demoted to counts of Rosenborg upon marriage, might try to re-claim their royal rank if Ingolf were allowed to do so despite his marrying a commoner as they had done.
So, in 1971, Christian renounced his rights to the throne and took the title count of Rosenborg.
On 27 February 1971, at Kongens Lyngby Kirke, Kongens Lyngby, Denmark, Christian married Anne Dorte Maltoft-Nielsen (3 October 1947 in Frederikssund – 2 January 2014 in Copenhagen) who thus became Her Excellency Countess Anne Dorte of Rosenborg.
Although lacking the prior royal assent of the monarch given in the Council of State that the law required, the king expressed no personal opposition to his nephew's choice of bride and, according to Christian, the king's private consent later had to be formally registered by the King-in-Council.
In a 1985 interview with Billed-Bladet, Count Christian had explained (translated from Danish):
As protocol dictates, I had to ask my uncle, King Frederik IX, if he had any objections to my getting engaged...
I was number four in the line of succession after Princess Margrethe, Princess Benedikte, and my father.
Count Christian and Countess Anne Dorte had three daughters: 


All three were born “Komtesser” a lower title than “Grevinde” which translates to “Countess” from birth.
And a title that all daughters of Counts in Denmark are given.
Public life

Count Christian took part in some major public events associated with the royal family, in 2004, he and Countess Anne Dorte attended the wedding on 14 May 2004 of Crown Prince Frederik at Copenhagen Cathedral, Copenhagen and the subsequent reception at Fredensborg Palace.
Death

Count Christian died on 21 May 2013 (aged 70) at Gentofte Hospital, Copenhagen in Denmark.
A number of members of the Danish royal family, led by Queen Margrethe, attended Count Christian's funeral, held at Lyngby Church on 29 May 2013.
His wife Countess Anne Dorte of Rosenborg died just 7 months later on 2 January 2014 in Copenhagen.



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
  AssignClass (02f48192-be1f-4cbf-a6f1-94886ae6092e)
 Call ID: 02f48192-be1f-4cbf-a6f1-94886ae6092e
  Args:
    source: :Christian_of_Rosenborg
    type: :Man
  AssignClass (c97252d1-1a73-4372-ad55-ddea83d87a6a)
 Call ID: c97252d1-1a73-4372-ad55-ddea83d87a6a
  Args:
    type: :Person
    source: :Christian_of_Rosenborg
  AddLiteral (95065d3e-3fa8-4481-a52e-43264b7a1a32)
 Call ID: 95065d3e-3fa8-4481-a52e-43264b7a1a32
  Args:
    source: :Christian_of_Rosenborg
    literal_value: 1942
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (d7e1ed02-c411-4399-82e3-87e07f151251)
 Call ID: d7e1ed02-c411-4399-82e3-87e07f151251
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 2013
    source: :Christian_of_Rosenborg
  AssignClass (6c96ff8a-d0ec-4134-a929-a80a76209f92)
 Call ID: 6c96ff8a-d0ec-4134-a929-a80a76209f92
  Args:
    type: :Man
    source: :Hereditary_Prince_Knud
  AssignClass (a47d5b1b-a445-4686-9850-e6e19eb2ce1d)
 Call ID: a47d5b1b-a445-4686-9850-e6e19eb2ce1d
  Args:
    type: :Person
    source: :Hereditary_Prince_Knud
  AssignClass (96bedbe4-8ce4-4436-af6b-48b754b075bb)
 Call ID: 96bedbe4-8ce4-4436-af6b-48b754b075bb
  Args:
    type: :Woman
    source: :Princess_Caroline-Mathilde
  AssignClass (670d64d1-9f95-42c2-91eb-6a20b6a3c3d5)
 Call ID: 670d64d1-9f95-42c2-91eb-6a20b6a3c3d5
  Args:
    source: :Princess_Caroline-Mathilde
    type: :Person
  AddTriple (5657ad1b-69c1-4ef0-8ee9-64b94d4df530)
 Call ID: 5657ad1b-69c1-4ef0-8ee9-64b94d4df530
  Args:
    relation: :isFatherOf
    target: :Christian_of_Rosenborg
    source: :Hereditary_Prince_Knud
  AddTriple (0acaaffb-227d-4d6b-b3d0-7f2bd6ce8529)
 Call ID: 0acaaffb-227d-4d6b-b3d0-7f2bd6ce8529
  Args:
    source: :Princess_Caroline-Mathilde
    target: :Christian_of_Rosenborg
    relation: :isMotherOf
  AssignClass (4daa540d-4a8c-4cda-98d9-101f41eec06f)
 Call ID: 4daa540d-4a8c-4cda-98d9-101f41eec06f
  Args:
    source: :Prince_Ingolf
    type: :Man
  AssignClass (1d35ea4d-7a97-416c-bea4-cbcc9d85c6f5)
 Call ID: 1d35ea4d-7a97-416c-bea4-cbcc9d85c6f5
  Args:
    source: :Prince_Ingolf
    type: :Person
  AddTriple (8790e96e-9f88-4789-b3cc-62d10c4ec333)
 Call ID: 8790e96e-9f88-4789-b3cc-62d10c4ec333
  Args:
    relation: :isBrotherOf
    source: :Prince_Ingolf
    target: :Christian_of_Rosenborg
  AssignClass (3a7382f4-87a4-4921-85c9-d5592f1f8d3e)
 Call ID: 3a7382f4-87a4-4921-85c9-d5592f1f8d3e
  Args:
    type: :Woman
    source: :Anne_Dorte_of_Rosenborg
  AssignClass (300b23a7-8c27-4a72-91b7-8d34f0715438)
 Call ID: 300b23a7-8c27-4a72-91b7-8d34f0715438
  Args:
    source: :Anne_Dorte_of_Rosenborg
    type: :Person
  AddLiteral (c9239aef-0267-4349-ad24-e4b4636ff4e0)
 Call ID: c9239aef-0267-4349-ad24-e4b4636ff4e0
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 1971
    source: :Christian_of_Rosenborg
  AddTriple (36d81213-8730-4bc2-a0cd-564eed3ba352)
 Call ID: 36d81213-8730-4bc2-a0cd-564eed3ba352
  Args:
    relation: :hasRelation
    source: :Christian_of_Rosenborg
    target: :Anne_Dorte_of_Rosenborg
  AddLiteral (20b27ddc-622a-42ae-8357-7d232be4f254)
 Call ID: 20b27ddc-622a-42ae-8357-7d232be4f254
  Args:
    source: :Anne_Dorte_of_Rosenborg
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1947
  AddLiteral (7defad6c-201d-4bc1-ac95-829c83b9c31b)
 Call ID: 7defad6c-201d-4bc1-ac95-829c83b9c31b
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 2014
    source: :Anne_Dorte_of_Rosenborg
  AssignClass (ca3af15e-6682-40db-bd8b-83fb9e062cfd)
 Call ID: ca3af15e-6682-40db-bd8b-83fb9e062cfd
  Args:
    source: :King_Frederik_IX
    type: :Man
  AssignClass (988ea74f-6bc3-456c-946d-eacb27210290)
 Call ID: 988ea74f-6bc3-456c-946d-eacb27210290
  Args:
    source: :King_Frederik_IX
    type: :Person
  AddTriple (2472f9c1-95fb-42fb-af1d-06083d5b59bc)
 Call ID: 2472f9c1-95fb-42fb-af1d-06083d5b59bc
  Args:
    relation: :isBrotherOf
    source: :King_Frederik_IX
    target: :Hereditary_Prince_Knud
  Finish (a3a51023-52d5-4654-bbc9-2c329d757403)
 Call ID: a3a51023-52d5-4654-bbc9-2c329d757403
  Args: