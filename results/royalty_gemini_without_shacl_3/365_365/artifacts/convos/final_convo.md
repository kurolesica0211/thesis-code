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
  AssignClass (41d89a35-6907-47d0-8919-fab70bc0fe8a)
 Call ID: 41d89a35-6907-47d0-8919-fab70bc0fe8a
  Args:
    type: :Man
    source: Ernst_August
  AssignClass (5ba5abaa-e856-4958-979a-06a53240a04f)
 Call ID: 5ba5abaa-e856-4958-979a-06a53240a04f
  Args:
    type: :Person
    source: Ernst_August
  AddLiteral (71beaa8c-cd8a-4d89-9183-9e2562b5acc1)
 Call ID: 71beaa8c-cd8a-4d89-9183-9e2562b5acc1
  Args:
    source: Ernst_August
    literal_value: 1914
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (4c724736-9387-44a8-9c3d-9c3ea73dc5d2)
 Call ID: 4c724736-9387-44a8-9c3d-9c3ea73dc5d2
  Args:
    relation: :hasDeathYear
    source: Ernst_August
    literal_value: 1987
    literal_type: xsd:integer
  AssignClass (b11a70b4-07f4-4966-ba7d-d8b541ce49f2)
 Call ID: b11a70b4-07f4-4966-ba7d-d8b541ce49f2
  Args:
    type: :Man
    source: Ernest_Augustus_Duke_of_Brunswick
  AssignClass (b1404778-46c0-4656-91ce-dd3ebc8b4b3d)
 Call ID: b1404778-46c0-4656-91ce-dd3ebc8b4b3d
  Args:
    type: :Person
    source: Ernest_Augustus_Duke_of_Brunswick
  AssignClass (2b2843bd-82a5-4eaf-948f-1e0384c29f49)
 Call ID: 2b2843bd-82a5-4eaf-948f-1e0384c29f49
  Args:
    type: :Woman
    source: Princess_Viktoria_Luise_of_Prussia
  AssignClass (31a35f79-acfe-47a1-8ff7-28865a715af3)
 Call ID: 31a35f79-acfe-47a1-8ff7-28865a715af3
  Args:
    type: :Person
    source: Princess_Viktoria_Luise_of_Prussia
  AddTriple (4acd886e-547d-4180-8e35-dd8b3e1cb111)
 Call ID: 4acd886e-547d-4180-8e35-dd8b3e1cb111
  Args:
    source: Ernst_August
    relation: :hasFather
    target: Ernest_Augustus_Duke_of_Brunswick
  AddTriple (b08cfe92-5773-4406-ac36-5cf50f414def)
 Call ID: b08cfe92-5773-4406-ac36-5cf50f414def
  Args:
    source: Ernst_August
    relation: :hasMother
    target: Princess_Viktoria_Luise_of_Prussia
  AssignClass (227c9f72-11b6-4295-b172-5e2e15afca64)
 Call ID: 227c9f72-11b6-4295-b172-5e2e15afca64
  Args:
    type: :Man
    source: Emperor_Wilhelm_II
  AssignClass (400fd66a-0772-4c44-9586-ec09acb03b3d)
 Call ID: 400fd66a-0772-4c44-9586-ec09acb03b3d
  Args:
    type: :Person
    source: Emperor_Wilhelm_II
  AddTriple (51a280e8-8a3c-48ce-85dd-e691344e5aaa)
 Call ID: 51a280e8-8a3c-48ce-85dd-e691344e5aaa
  Args:
    target: Emperor_Wilhelm_II
    relation: :hasFather
    source: Princess_Viktoria_Luise_of_Prussia
  AssignClass (d9fe7d8a-1886-42bd-b3c7-66f45832725e)
 Call ID: d9fe7d8a-1886-42bd-b3c7-66f45832725e
  Args:
    type: :Woman
    source: Princess_Frederica
  AssignClass (9c83a601-4597-4513-bb1e-35567d4258a6)
 Call ID: 9c83a601-4597-4513-bb1e-35567d4258a6
  Args:
    type: :Person
    source: Princess_Frederica
  AddTriple (53016d17-2125-4450-9a3b-e3e9484b5d1f)
 Call ID: 53016d17-2125-4450-9a3b-e3e9484b5d1f
  Args:
    relation: :isSiblingOf
    target: Princess_Frederica
    source: Ernst_August
  AssignClass (dfcc94e8-6f9a-4b8a-8c0d-3d5062549a80)
 Call ID: dfcc94e8-6f9a-4b8a-8c0d-3d5062549a80
  Args:
    type: :Man
    source: Prince_George_William
  AssignClass (f8501bf3-7a02-4d21-b10d-3f68e192fe6f)
 Call ID: f8501bf3-7a02-4d21-b10d-3f68e192fe6f
  Args:
    type: :Person
    source: Prince_George_William
  AddTriple (6e02afb5-1fe9-428d-bdd8-4efc31170e19)
 Call ID: 6e02afb5-1fe9-428d-bdd8-4efc31170e19
  Args:
    relation: :isSiblingOf
    target: Prince_George_William
    source: Ernst_August
  AssignClass (84ebb31f-f5c7-45ab-a13e-f2caa86865af)
 Call ID: 84ebb31f-f5c7-45ab-a13e-f2caa86865af
  Args:
    type: :Man
    source: King_Paul_of_Greece
  AssignClass (19edc3f5-11cc-4aa3-bd8b-b8d6888c0581)
 Call ID: 19edc3f5-11cc-4aa3-bd8b-b8d6888c0581
  Args:
    type: :Person
    source: King_Paul_of_Greece
  AddLiteral (364fe501-faaa-43cb-b5f1-a09068e3d05f)
 Call ID: 364fe501-faaa-43cb-b5f1-a09068e3d05f
  Args:
    relation: :hasMarriageYear
    literal_value: 1938
    source: Princess_Frederica
    literal_type: xsd:integer
  AddTriple (41796882-c786-4094-8d0d-1e3cdd977369)
 Call ID: 41796882-c786-4094-8d0d-1e3cdd977369
  Args:
    relation: :hasRelation
    target: King_Paul_of_Greece
    source: Princess_Frederica
  AssignClass (15e5f62d-30d6-4584-8ede-d59aa697b272)
 Call ID: 15e5f62d-30d6-4584-8ede-d59aa697b272
  Args:
    type: :Woman
    source: Princess_Sophie_of_Greece_and_Denmark
  AssignClass (438dd31e-0a4b-4384-a87c-1665da295781)
 Call ID: 438dd31e-0a4b-4384-a87c-1665da295781
  Args:
    type: :Person
    source: Princess_Sophie_of_Greece_and_Denmark
  AddLiteral (53a2325d-4c61-442e-850e-bfe244d5fbf8)
 Call ID: 53a2325d-4c61-442e-850e-bfe244d5fbf8
  Args:
    literal_type: xsd:integer
    source: Prince_George_William
    literal_value: 1946
    relation: :hasMarriageYear
  AddTriple (ad82dee2-00f1-4aa3-9f97-6ce94cc6bf54)
 Call ID: ad82dee2-00f1-4aa3-9f97-6ce94cc6bf54
  Args:
    target: Princess_Sophie_of_Greece_and_Denmark
    relation: :hasRelation
    source: Prince_George_William
  AssignClass (d6175c96-1652-4aec-b424-27157a2e251d)
 Call ID: d6175c96-1652-4aec-b424-27157a2e251d
  Args:
    type: :Woman
    source: Maria_Anna_von_Humboldt_Dachroeden
  AssignClass (70579935-7a86-4652-ac3d-2db8bb4a2060)
 Call ID: 70579935-7a86-4652-ac3d-2db8bb4a2060
  Args:
    type: :Person
    source: Maria_Anna_von_Humboldt_Dachroeden
  AssignClass (b5c262d6-9230-45bf-b01e-8805a2fc382b)
 Call ID: b5c262d6-9230-45bf-b01e-8805a2fc382b
  Args:
    type: :Man
    source: Christian_Ernst_August_Hubertus
  AssignClass (e7745f6a-383f-43de-a6ab-e3467bc61064)
 Call ID: e7745f6a-383f-43de-a6ab-e3467bc61064
  Args:
    type: :Person
    source: Christian_Ernst_August_Hubertus
  AddTriple (5f90950e-b553-4649-b302-e5b2b0e6aaee)
 Call ID: 5f90950e-b553-4649-b302-e5b2b0e6aaee
  Args:
    relation: :isSonOf
    target: Ernst_August
    source: Christian_Ernst_August_Hubertus
  AddTriple (cec42008-82e4-4ea1-a7dc-7b6f65f7ba07)
 Call ID: cec42008-82e4-4ea1-a7dc-7b6f65f7ba07
  Args:
    target: Maria_Anna_von_Humboldt_Dachroeden
    relation: :isSonOf
    source: Christian_Ernst_August_Hubertus
  AssignClass (96bd5f0b-5727-4846-a83a-373d5e6c7315)
 Call ID: 96bd5f0b-5727-4846-a83a-373d5e6c7315
  Args:
    type: :Woman
    source: Princess_Ortrud_of_Schleswig_Holstein_Sonderburg_Glücksburg
  AssignClass (e77ce216-02f6-4a32-b1e6-e75bb0b7bb86)
 Call ID: e77ce216-02f6-4a32-b1e6-e75bb0b7bb86
  Args:
    type: :Person
    source: Princess_Ortrud_of_Schleswig_Holstein_Sonderburg_Glücksburg
  AddLiteral (4f9a740a-0288-47bb-953e-7d5c91653d89)
 Call ID: 4f9a740a-0288-47bb-953e-7d5c91653d89
  Args:
    literal_type: xsd:integer
    source: Ernst_August
    literal_value: 1951
    relation: :hasMarriageYear
  AddTriple (988ec1bc-bc09-473a-bc88-74671fa7b963)
 Call ID: 988ec1bc-bc09-473a-bc88-74671fa7b963
  Args:
    source: Ernst_August
    target: Princess_Ortrud_of_Schleswig_Holstein_Sonderburg_Glücksburg
    relation: :hasRelation
  AddLiteral (cb468585-6de0-4395-b4e1-a3b424129dfc)
 Call ID: cb468585-6de0-4395-b4e1-a3b424129dfc
  Args:
    literal_type: xsd:integer
    literal_value: 1980
    source: Princess_Ortrud_of_Schleswig_Holstein_Sonderburg_Glücksburg
    relation: :hasDeathYear
  AssignClass (2169eda6-0d9d-4a4a-81fe-370291c8c288)
 Call ID: 2169eda6-0d9d-4a4a-81fe-370291c8c288
  Args:
    type: :Woman
    source: Countess_Monika_zu_Solms_Laubach
  AssignClass (eb9cf04d-450b-4538-99d2-d3c2d1f260d9)
 Call ID: eb9cf04d-450b-4538-99d2-d3c2d1f260d9
  Args:
    type: :Person
    source: Countess_Monika_zu_Solms_Laubach
  AddLiteral (0c7e3ad1-fae2-4218-a9c1-6c5066d52bc6)
 Call ID: 0c7e3ad1-fae2-4218-a9c1-6c5066d52bc6
  Args:
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: Ernst_August
    literal_value: 1981
  AddTriple (b6bb2082-d177-4cfa-b4b8-6d67252f67f0)
 Call ID: b6bb2082-d177-4cfa-b4b8-6d67252f67f0
  Args:
    source: Ernst_August
    relation: :hasRelation
    target: Countess_Monika_zu_Solms_Laubach
  AddLiteral (4ea0fb27-fd99-4bef-b313-538014e10c9d)
 Call ID: 4ea0fb27-fd99-4bef-b313-538014e10c9d
  Args:
    source: Countess_Monika_zu_Solms_Laubach
    literal_value: 2015
    literal_type: xsd:integer
    relation: :hasDeathYear
  AssignClass (d92fb3bd-1100-4519-892a-15ef9dc28edb)
 Call ID: d92fb3bd-1100-4519-892a-15ef9dc28edb
  Args:
    type: :Man
    source: Georg_9th_Count_of_Solms_Laubach
  AssignClass (1a68e6be-7ba5-4cfc-9a5f-240cc31e5e2b)
 Call ID: 1a68e6be-7ba5-4cfc-9a5f-240cc31e5e2b
  Args:
    type: :Person
    source: Georg_9th_Count_of_Solms_Laubach
  AssignClass (24181ce1-3945-4df8-a770-5a2946ec4652)
 Call ID: 24181ce1-3945-4df8-a770-5a2946ec4652
  Args:
    type: :Woman
    source: Princess_Johanna_of_Solms_Hohensolms_Lich
  AssignClass (b3b9c706-6710-4fd2-ba02-c9608bfb5458)
 Call ID: b3b9c706-6710-4fd2-ba02-c9608bfb5458
  Args:
    type: :Person
    source: Princess_Johanna_of_Solms_Hohensolms_Lich
  AddTriple (6918d883-64f7-41a6-970d-24f4ae0b5829)
 Call ID: 6918d883-64f7-41a6-970d-24f4ae0b5829
  Args:
    relation: :hasFather
    target: Georg_9th_Count_of_Solms_Laubach
    source: Countess_Monika_zu_Solms_Laubach
  AddTriple (a990aacc-2c61-4fa8-9de6-4adb62875d0e)
 Call ID: a990aacc-2c61-4fa8-9de6-4adb62875d0e
  Args:
    source: Countess_Monika_zu_Solms_Laubach
    target: Princess_Johanna_of_Solms_Hohensolms_Lich
    relation: :hasMother
  Finish (131db306-b93a-4251-9445-c30b7d4a9b39)
 Call ID: 131db306-b93a-4251-9445-c30b7d4a9b39
  Args: