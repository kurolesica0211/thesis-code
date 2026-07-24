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
Ernst August, Hereditary Prince of Brunswick, Prince of Hanover (German: Ernst August Prinz von Hannover; 18 March 1914 – 9 December 1987) was head of the House of Hanover from 1953 until his death in 1987.
From his birth until the German Revolution of 1918–1919 he was the heir apparent to the Duchy of Brunswick, a state of the German Empire.
He was born at Braunschweig, Germany, the eldest son of Ernest Augustus, Duke of Brunswick and Princess Viktoria Luise of Prussia, the only daughter of Emperor Wilhelm II, Ernest Augustus's third cousin in descent from George III the United Kingdom.
Ernst August's parents were, therefore, third cousins, once removed.
From his birth, he was the Hereditary Prince of Brunswick.
He was also, shortly after birth in 1914, made a British prince by King George V of the United Kingdom, and was heir to the titles Duke of Cumberland and Teviotdale and Earl of Armagh.
Nonetheless, he held title of Prince of the United Kingdom of Great Britain and Ireland, granted ad personam to the children of the then-Duke of Brunswick by the letters patent of 1914, which remained unrevoked.
Life

He ceased being heir to the duchy of Brunswick at the age of four, when his father abdicated in 1918.
After his father's death in 1953, he became head of the House of Hanover.
In 1938 his sister, Princess Frederica had married the later King Paul of Greece and in 1946 his younger brother Prince George William married Princess Sophie of Greece and Denmark, thus becoming the brother-in-law of Prince Philip, Duke of Edinburgh and Queen Elizabeth II of the United Kingdom.
Ernest Augustus was himself an heir to the British titles of Prince of Great Britain and Ireland, recognised ad personam for Ernst August's father as well as for him and his siblings by King George V of the United Kingdom on 17 June 1914, Duke of Cumberland and Teviotdale, Earl of Armagh, which however were all suspended under the Titles Deprivation Act 1917.
In addition to being a German, he also held British nationality, after successfully claiming it under the Sophia Naturalization Act 1705 in the case of Attorney-General v. Prince Ernest Augustus of Hanover.
Nonetheless, a problem arose as foreign royal titles cannot be entered into a British passport.
Therefore, the titles Prince of Hanover, Duke of Brunswick and Lüneburg could not be mentioned there, nor could the British titles due to the Titles Deprivation Act 1917.
The name which was finally entered into his British documents, was thus Ernest Augustus Guelph, with the addition of His Royal Highness.
Guelph is thus also the British last name of his siblings and children, all styled Royal Highnesses in the United Kingdom.
Ernest Augustus converted Marienburg Castle into a museum in 1954, after having moved to nearby Calenberg Demesne, which caused a row with his mother, who was forced to move out.
He also sold the family's exile seat, Cumberland Castle at Gmunden, Austria, to the state of Upper Austria in 1979, but his family foundation based in Liechtenstein kept vast forests, a game park, a hunting lodge, The Queen's Villa and other property at Gmunden.
The family property is now managed by his grandson Ernst August.
Marriage and children

In 1941 during the Second World War, his cousin Prince Hubertus of Prussia married the noted society beauty and aristocrat Baroness Maria Anna von Humboldt-Dachroeden (1916–2003).
The couple, however, divorced in 1943, after her affair with Ernest Augustus resulted in the birth of a son.
Ernest Augustus however did not marry Maria Anna because his parents would not have approved, since she was considered of inadequate birth and was also a divorcée, and the marriage would have made his younger brother Prince George William heir to the headship of the House of Hanover.
The child, christened Christian Ernst August Hubertus, Freiherr von Humboldt-Dachroeden, was born in 1943 and is currently a bank consultant.
On 5 September 1951, Ernest Augustus married Princess Ortrud of Schleswig-Holstein-Sonderburg-Glücksburg (1925–1980).
The wedding was attended by many important royal figures, including his sister Queen Frederica and her husband King Paul of Greece, and the heads of the houses of Saxony, Hesse, Mecklenburg, Oldenburg, and Baden.
The wedding was followed with a reception in the Gallery Building at Herrenhausen Gardens, the only part of the House of Hanover's former summer palace still intact, as the palace itself had been burned down during World War II.
In 1954, the couple, together with Ernest Augustus's three younger brothers, took part in the ship tour organized by his sister, Queen Frederica, and her husband King Paul of Greece, which became known as the "Cruise of the Kings" and was attended by over 100 royals from all over Europe.
Princess Ortrud died in 1980.
Ernest Augustus married again in 1981, Countess Monika zu Solms-Laubach (1929–2015), daughter of Georg, 9th Count of Solms-Laubach (1899–1969) and his wife, Princess Johanna of Solms-Hohensolms-Lich (1905–1982).
He died at Schulenburg, Pattensen, Lower Saxony, Germany, aged 73, and was buried next to his first wife on a round bastion of Marienburg Castle (Hanover).



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
  AssignClass (db53ea58-8f05-414f-8bfb-1a1a73066419)
 Call ID: db53ea58-8f05-414f-8bfb-1a1a73066419
  Args:
    type: :Man
    source: Ernst_August_Hereditary_Prince_of_Brunswick
  AssignClass (e49b121d-22e4-49f3-a290-f2e64bb25d3d)
 Call ID: e49b121d-22e4-49f3-a290-f2e64bb25d3d
  Args:
    type: :Person
    source: Ernst_August_Hereditary_Prince_of_Brunswick
  AddLiteral (4b3988fb-a146-465f-a0f7-d701e617038b)
 Call ID: 4b3988fb-a146-465f-a0f7-d701e617038b
  Args:
    source: Ernst_August_Hereditary_Prince_of_Brunswick
    literal_value: 1914
    literal_type: xsd:positiveInteger
    relation: :hasBirthYear
  AddLiteral (8d470c48-1c37-4788-a17d-3d3d11a397dd)
 Call ID: 8d470c48-1c37-4788-a17d-3d3d11a397dd
  Args:
    literal_value: 1987
    relation: :hasDeathYear
    literal_type: xsd:positiveInteger
    source: Ernst_August_Hereditary_Prince_of_Brunswick
  AssignClass (c4c11810-090f-472b-9688-39f20e41af21)
 Call ID: c4c11810-090f-472b-9688-39f20e41af21
  Args:
    type: :Man
    source: Ernest_August_Duke_of_Brunswick
  AssignClass (966e22da-c0b1-41b6-b5f2-d8d50b7162e9)
 Call ID: 966e22da-c0b1-41b6-b5f2-d8d50b7162e9
  Args:
    type: :Person
    source: Ernest_August_Duke_of_Brunswick
  AssignClass (89de0031-085e-476f-9ef9-98cfb80a56aa)
 Call ID: 89de0031-085e-476f-9ef9-98cfb80a56aa
  Args:
    type: :Woman
    source: Princess_Viktoria_Luise_of_Prussia
  AssignClass (707de04c-1a16-4e95-b8ce-93f13bd4b5c0)
 Call ID: 707de04c-1a16-4e95-b8ce-93f13bd4b5c0
  Args:
    type: :Person
    source: Princess_Viktoria_Luise_of_Prussia
  AddTriple (db0a95b5-222f-4d32-846d-5826e56327ae)
 Call ID: db0a95b5-222f-4d32-846d-5826e56327ae
  Args:
    source: Ernst_August_Hereditary_Prince_of_Brunswick
    target: Ernest_August_Duke_of_Brunswick
    relation: :hasFather
  AddTriple (acc4c368-1e74-4fe0-88c7-38ef5e636e36)
 Call ID: acc4c368-1e74-4fe0-88c7-38ef5e636e36
  Args:
    target: Princess_Viktoria_Luise_of_Prussia
    source: Ernst_August_Hereditary_Prince_of_Brunswick
    relation: :hasMother
  AssignClass (da72cb37-0f9f-4c41-a695-53ff8fe32cbb)
 Call ID: da72cb37-0f9f-4c41-a695-53ff8fe32cbb
  Args:
    type: :Woman
    source: Princess_Frederica
  AssignClass (b4e49a2e-322a-4697-a06e-f72de1c3b49c)
 Call ID: b4e49a2e-322a-4697-a06e-f72de1c3b49c
  Args:
    type: :Person
    source: Princess_Frederica
  AddTriple (40f60e2b-8881-49e4-aad2-8eaa91f32bc3)
 Call ID: 40f60e2b-8881-49e4-aad2-8eaa91f32bc3
  Args:
    target: Princess_Frederica
    source: Ernst_August_Hereditary_Prince_of_Brunswick
    relation: :hasSister
  AssignClass (8300b353-6221-4801-adc2-9a10a476839f)
 Call ID: 8300b353-6221-4801-adc2-9a10a476839f
  Args:
    type: :Man
    source: Prince_George_William
  AssignClass (daeb7b00-0f92-4d35-af8f-7ddc585f96a4)
 Call ID: daeb7b00-0f92-4d35-af8f-7ddc585f96a4
  Args:
    type: :Person
    source: Prince_George_William
  AddTriple (1f254c83-4414-4e04-987c-64d5203f7161)
 Call ID: 1f254c83-4414-4e04-987c-64d5203f7161
  Args:
    target: Prince_George_William
    source: Ernst_August_Hereditary_Prince_of_Brunswick
    relation: :hasBrother
  AssignClass (590e8ba5-4085-42aa-8260-9beb59de0536)
 Call ID: 590e8ba5-4085-42aa-8260-9beb59de0536
  Args:
    type: :Man
    source: Christian_Ernst_August_Hubertus_Freiherr_von_Humboldt-Dachroeden
  AssignClass (5a6dcf7f-b2ac-414d-80b0-8817d38bae6c)
 Call ID: 5a6dcf7f-b2ac-414d-80b0-8817d38bae6c
  Args:
    type: :Person
    source: Christian_Ernst_August_Hubertus_Freiherr_von_Humboldt-Dachroeden
  AddTriple (d7d2db1c-d76e-47df-9380-631a9e7a2a18)
 Call ID: d7d2db1c-d76e-47df-9380-631a9e7a2a18
  Args:
    relation: :hasSon
    source: Ernst_August_Hereditary_Prince_of_Brunswick
    target: Christian_Ernst_August_Hubertus_Freiherr_von_Humboldt-Dachroeden
  AssignClass (74ac532c-60e6-4a64-8ff3-b55fd4c1f7e2)
 Call ID: 74ac532c-60e6-4a64-8ff3-b55fd4c1f7e2
  Args:
    type: :Woman
    source: Princess_Ortrud_of_Schleswig-Holstein-Sonderburg-Glücksburg
  AssignClass (93831563-bf5d-416d-bac7-53af9285a015)
 Call ID: 93831563-bf5d-416d-bac7-53af9285a015
  Args:
    type: :Person
    source: Princess_Ortrud_of_Schleswig-Holstein-Sonderburg-Glücksburg
  AddLiteral (9250f2fb-7521-41dd-ac41-6fbd635bd194)
 Call ID: 9250f2fb-7521-41dd-ac41-6fbd635bd194
  Args:
    source: Ernst_August_Hereditary_Prince_of_Brunswick
    relation: :hasMarriageYear
    literal_type: xsd:positiveInteger
    literal_value: 1951
  AssignClass (8bc1bc2c-1f5f-4b8b-be03-7ae40a9f1008)
 Call ID: 8bc1bc2c-1f5f-4b8b-be03-7ae40a9f1008
  Args:
    type: :Woman
    source: Countess_Monika_zu_Solms-Laubach
  AssignClass (bfd05d4c-2fc0-4b22-a822-e503cfacea5b)
 Call ID: bfd05d4c-2fc0-4b22-a822-e503cfacea5b
  Args:
    type: :Person
    source: Countess_Monika_zu_Solms-Laubach
  AddLiteral (ce58b607-1466-436e-b103-accb8c10a9ad)
 Call ID: ce58b607-1466-436e-b103-accb8c10a9ad
  Args:
    relation: :hasMarriageYear
    literal_type: xsd:positiveInteger
    literal_value: 1981
    source: Ernst_August_Hereditary_Prince_of_Brunswick
  AssignClass (3b52bd0f-e15a-402e-9202-5f994fccfbf8)
 Call ID: 3b52bd0f-e15a-402e-9202-5f994fccfbf8
  Args:
    type: :Man
    source: Georg_9th_Count_of_Solms-Laubach
  AssignClass (e0b92fea-4270-4ba3-bdc4-559b0ae950e0)
 Call ID: e0b92fea-4270-4ba3-bdc4-559b0ae950e0
  Args:
    type: :Person
    source: Georg_9th_Count_of_Solms-Laubach
  AssignClass (653ab5ff-21fb-4492-b704-409727d84fc8)
 Call ID: 653ab5ff-21fb-4492-b704-409727d84fc8
  Args:
    type: :Woman
    source: Princess_Johanna_of_Solms-Hohensolms-Lich
  AssignClass (a6c6972d-71b0-44f3-8916-0536ddb6774e)
 Call ID: a6c6972d-71b0-44f3-8916-0536ddb6774e
  Args:
    type: :Person
    source: Princess_Johanna_of_Solms-Hohensolms-Lich
  AddTriple (e0ff2fe5-2909-43e0-9e02-fc689862b5c1)
 Call ID: e0ff2fe5-2909-43e0-9e02-fc689862b5c1
  Args:
    target: Georg_9th_Count_of_Solms-Laubach
    source: Countess_Monika_zu_Solms-Laubach
    relation: :hasFather
  AddTriple (5d6d2fe2-ebc3-47dd-9c84-4b3af823516d)
 Call ID: 5d6d2fe2-ebc3-47dd-9c84-4b3af823516d
  Args:
    relation: :hasMother
    target: Princess_Johanna_of_Solms-Hohensolms-Lich
    source: Countess_Monika_zu_Solms-Laubach
  Finish (1d4dba68-c587-4423-917b-93fd6859bb8a)
 Call ID: 1d4dba68-c587-4423-917b-93fd6859bb8a
  Args: