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
  AssignClass (9a16cbce-ca30-4bf8-9b88-01cb1b3bc931)
 Call ID: 9a16cbce-ca30-4bf8-9b88-01cb1b3bc931
  Args:
    type: :Man
    source: Ernst_August_Hereditary_Prince_of_Brunswick
  AssignClass (d2e1b8f3-d76d-4fa6-b18c-c5b2ae61d200)
 Call ID: d2e1b8f3-d76d-4fa6-b18c-c5b2ae61d200
  Args:
    type: :Person
    source: Ernst_August_Hereditary_Prince_of_Brunswick
  AssignClass (3c9d2801-0cfc-4be4-98c5-2fdbce6c29f0)
 Call ID: 3c9d2801-0cfc-4be4-98c5-2fdbce6c29f0
  Args:
    type: :Man
    source: Ernest_Augustus_Duke_of_Brunswick
  AssignClass (84900679-95d2-44ec-a1bf-771572e78b92)
 Call ID: 84900679-95d2-44ec-a1bf-771572e78b92
  Args:
    type: :Person
    source: Ernest_Augustus_Duke_of_Brunswick
  AssignClass (eef2c3d7-214f-4101-a185-a73bef6194fc)
 Call ID: eef2c3d7-214f-4101-a185-a73bef6194fc
  Args:
    type: :Woman
    source: Princess_Viktoria_Luise_of_Prussia
  AssignClass (538b12df-4211-4de7-a541-ff09f74adf82)
 Call ID: 538b12df-4211-4de7-a541-ff09f74adf82
  Args:
    type: :Person
    source: Princess_Viktoria_Luise_of_Prussia
  AssignClass (cfd01999-9b18-4ba3-9d25-42ae2de54231)
 Call ID: cfd01999-9b18-4ba3-9d25-42ae2de54231
  Args:
    type: :Man
    source: Emperor_Wilhelm_II
  AssignClass (a7e677bd-d173-46c0-9562-65eca1146541)
 Call ID: a7e677bd-d173-46c0-9562-65eca1146541
  Args:
    type: :Person
    source: Emperor_Wilhelm_II
  AssignClass (410c44c1-f664-495e-a551-99bfa111ecea)
 Call ID: 410c44c1-f664-495e-a551-99bfa111ecea
  Args:
    type: :Woman
    source: Princess_Frederica
  AssignClass (e00edc9e-e83d-4e78-8794-6891075811dc)
 Call ID: e00edc9e-e83d-4e78-8794-6891075811dc
  Args:
    type: :Person
    source: Princess_Frederica
  AssignClass (6f82078d-2d42-48fb-92a1-52a14d2d93c9)
 Call ID: 6f82078d-2d42-48fb-92a1-52a14d2d93c9
  Args:
    type: :Man
    source: Prince_George_William
  AssignClass (595c2731-70dc-4477-92b4-01d1180c8f5d)
 Call ID: 595c2731-70dc-4477-92b4-01d1180c8f5d
  Args:
    type: :Person
    source: Prince_George_William
  AssignClass (37df05c6-e77e-41fe-9a28-35de50246bd8)
 Call ID: 37df05c6-e77e-41fe-9a28-35de50246bd8
  Args:
    type: :Woman
    source: Princess_Ortrud_of_Schleswig-Holstein-Sonderburg-Glücksburg
  AssignClass (a7fd3fde-b5c6-4678-8977-2497dfae2512)
 Call ID: a7fd3fde-b5c6-4678-8977-2497dfae2512
  Args:
    type: :Person
    source: Princess_Ortrud_of_Schleswig-Holstein-Sonderburg-Glücksburg
  AssignClass (68e6483b-1fc7-4770-a474-370a149b158b)
 Call ID: 68e6483b-1fc7-4770-a474-370a149b158b
  Args:
    type: :Woman
    source: Countess_Monika_zu_Solms-Laubach
  AssignClass (8ded82e4-a7f6-471a-8b46-191d6ed4c613)
 Call ID: 8ded82e4-a7f6-471a-8b46-191d6ed4c613
  Args:
    type: :Person
    source: Countess_Monika_zu_Solms-Laubach
  AssignClass (fc078ab0-6e41-44fe-8914-61b3419865ac)
 Call ID: fc078ab0-6e41-44fe-8914-61b3419865ac
  Args:
    type: :Man
    source: Georg_9th_Count_of_Solms-Laubach
  AssignClass (e2f9abf0-397e-49c5-b1d9-b21a1052b851)
 Call ID: e2f9abf0-397e-49c5-b1d9-b21a1052b851
  Args:
    type: :Person
    source: Georg_9th_Count_of_Solms-Laubach
  AssignClass (a6248106-d256-44c5-beb2-c4b4a77ec5fd)
 Call ID: a6248106-d256-44c5-beb2-c4b4a77ec5fd
  Args:
    type: :Woman
    source: Princess_Johanna_of_Solms-Hohensolms-Lich
  AssignClass (dfe179f6-28ad-4ffc-9a32-bba72a2aa964)
 Call ID: dfe179f6-28ad-4ffc-9a32-bba72a2aa964
  Args:
    type: :Person
    source: Princess_Johanna_of_Solms-Hohensolms-Lich
  AssignClass (2f073616-d2c9-433a-b3bf-19eb56a54bc0)
 Call ID: 2f073616-d2c9-433a-b3bf-19eb56a54bc0
  Args:
    type: :Man
    source: Christian_Ernst_August_Hubertus_Freiherr_von_Humboldt-Dachroeden
  AssignClass (8ded83bf-5dd3-4635-8c96-a497caf6122c)
 Call ID: 8ded83bf-5dd3-4635-8c96-a497caf6122c
  Args:
    type: :Person
    source: Christian_Ernst_August_Hubertus_Freiherr_von_Humboldt-Dachroeden
  AssignClass (ef49610e-9ff7-4aa9-93bb-bc863449f2b7)
 Call ID: ef49610e-9ff7-4aa9-93bb-bc863449f2b7
  Args:
    type: :Woman
    source: Maria_Anna_von_Humboldt-Dachroeden
  AssignClass (b1095c7b-643b-4745-8cb7-f7d099e03f7b)
 Call ID: b1095c7b-643b-4745-8cb7-f7d099e03f7b
  Args:
    type: :Person
    source: Maria_Anna_von_Humboldt-Dachroeden
  AddLiteral (7d87ee13-872e-4bf2-aeb6-918b4060145d)
 Call ID: 7d87ee13-872e-4bf2-aeb6-918b4060145d
  Args:
    source: Ernst_August_Hereditary_Prince_of_Brunswick
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1914
  AddLiteral (d7320446-32b2-4cc7-9ef7-f08ebf056f69)
 Call ID: d7320446-32b2-4cc7-9ef7-f08ebf056f69
  Args:
    source: Ernst_August_Hereditary_Prince_of_Brunswick
    relation: :hasDeathYear
    literal_value: 1987
    literal_type: xsd:integer
  AddTriple (ecc8ee65-f96e-46be-825e-f7525a9c04fe)
 Call ID: ecc8ee65-f96e-46be-825e-f7525a9c04fe
  Args:
    target: Ernest_Augustus_Duke_of_Brunswick
    relation: :hasFather
    source: Ernst_August_Hereditary_Prince_of_Brunswick
  AddTriple (c0d27411-bb61-428e-bcd0-9b6d66ee2c86)
 Call ID: c0d27411-bb61-428e-bcd0-9b6d66ee2c86
  Args:
    relation: :hasMother
    source: Ernst_August_Hereditary_Prince_of_Brunswick
    target: Princess_Viktoria_Luise_of_Prussia
  AddTriple (640aa41b-2078-4ddd-a3fe-4484d4861fc8)
 Call ID: 640aa41b-2078-4ddd-a3fe-4484d4861fc8
  Args:
    target: Emperor_Wilhelm_II
    source: Princess_Viktoria_Luise_of_Prussia
    relation: :hasFather
  AddTriple (f9206b54-da6c-45d2-be2c-3e0d9a104075)
 Call ID: f9206b54-da6c-45d2-be2c-3e0d9a104075
  Args:
    target: Ernest_Augustus_Duke_of_Brunswick
    relation: :hasFather
    source: Ernst_August_Hereditary_Prince_of_Brunswick
  AddTriple (48f5ea01-8db2-4ef7-ac36-d8922a391d58)
 Call ID: 48f5ea01-8db2-4ef7-ac36-d8922a391d58
  Args:
    source: Princess_Frederica
    relation: :hasMother
    target: Princess_Viktoria_Luise_of_Prussia
  AddTriple (9626d9e2-7eb7-49ab-a9b4-1a3b5545f45c)
 Call ID: 9626d9e2-7eb7-49ab-a9b4-1a3b5545f45c
  Args:
    target: Ernest_Augustus_Duke_of_Brunswick
    source: Princess_Frederica
    relation: :hasFather
  AddTriple (d72f2b8f-1b3b-40e3-81db-44adecba7dfe)
 Call ID: d72f2b8f-1b3b-40e3-81db-44adecba7dfe
  Args:
    target: Princess_Viktoria_Luise_of_Prussia
    relation: :hasMother
    source: Prince_George_William
  AddTriple (fe4655f5-23ae-4466-91b2-489ccec67cd7)
 Call ID: fe4655f5-23ae-4466-91b2-489ccec67cd7
  Args:
    source: Prince_George_William
    relation: :hasFather
    target: Ernest_Augustus_Duke_of_Brunswick
  AddTriple (63c9ec0c-9dd3-4597-9277-e5656ec3c979)
 Call ID: 63c9ec0c-9dd3-4597-9277-e5656ec3c979
  Args:
    relation: :hasMother
    source: Christian_Ernst_August_Hubertus_Freiherr_von_Humboldt-Dachroeden
    target: Maria_Anna_von_Humboldt-Dachroeden
  AddTriple (372e7fed-f73b-49b6-bce1-183f8e18344d)
 Call ID: 372e7fed-f73b-49b6-bce1-183f8e18344d
  Args:
    relation: :hasFather
    source: Christian_Ernst_August_Hubertus_Freiherr_von_Humboldt-Dachroeden
    target: Ernst_August_Hereditary_Prince_of_Brunswick
  AddTriple (31248874-98b3-4509-820a-fc10191c56c7)
 Call ID: 31248874-98b3-4509-820a-fc10191c56c7
  Args:
    target: Georg_9th_Count_of_Solms-Laubach
    source: Countess_Monika_zu_Solms-Laubach
    relation: :hasFather
  AddTriple (384a3410-3ade-41ef-8b86-6e4e4347841f)
 Call ID: 384a3410-3ade-41ef-8b86-6e4e4347841f
  Args:
    target: Princess_Johanna_of_Solms-Hohensolms-Lich
    source: Countess_Monika_zu_Solms-Laubach
    relation: :hasMother
  AddLiteral (69d96acf-8228-444d-b21b-e1038836087b)
 Call ID: 69d96acf-8228-444d-b21b-e1038836087b
  Args:
    source: Ernst_August_Hereditary_Prince_of_Brunswick
    relation: :hasMarriageYear
    literal_value: 1951
    literal_type: xsd:integer
  AddTriple (d7e98791-37a4-49b3-a415-99d8c1944033)
 Call ID: d7e98791-37a4-49b3-a415-99d8c1944033
  Args:
    target: Princess_Ortrud_of_Schleswig-Holstein-Sonderburg-Glücksburg
    relation: :hasRelation
    source: Ernst_August_Hereditary_Prince_of_Brunswick
  AddLiteral (b9bcaadd-ef26-4d4b-9301-e39b3d1f0760)
 Call ID: b9bcaadd-ef26-4d4b-9301-e39b3d1f0760
  Args:
    literal_type: xsd:integer
    literal_value: 1981
    relation: :hasMarriageYear
    source: Ernst_August_Hereditary_Prince_of_Brunswick
  AddTriple (b20eb295-6656-4465-b320-6dc54473c5bc)
 Call ID: b20eb295-6656-4465-b320-6dc54473c5bc
  Args:
    relation: :hasRelation
    source: Ernst_August_Hereditary_Prince_of_Brunswick
    target: Countess_Monika_zu_Solms-Laubach
  Finish (0634e0d4-eda4-4884-837a-754d96799707)
 Call ID: 0634e0d4-eda4-4884-837a-754d96799707
  Args: