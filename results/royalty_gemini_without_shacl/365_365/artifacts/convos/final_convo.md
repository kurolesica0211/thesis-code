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
  AssignClass (0df53b7e-64eb-4956-bda9-47a14d72e9d3)
 Call ID: 0df53b7e-64eb-4956-bda9-47a14d72e9d3
  Args:
    type: :Man
    source: :Ernst_August_Hereditary_Prince_of_Brunswick
  AssignClass (1fc6cf6f-8d2c-455d-8bdd-1a511d31f455)
 Call ID: 1fc6cf6f-8d2c-455d-8bdd-1a511d31f455
  Args:
    type: :Person
    source: :Ernst_August_Hereditary_Prince_of_Brunswick
  AddLiteral (8e89c74e-d990-4700-b131-4ba55b570f4f)
 Call ID: 8e89c74e-d990-4700-b131-4ba55b570f4f
  Args:
    literal_value: 1914
    relation: :hasBirthYear
    source: :Ernst_August_Hereditary_Prince_of_Brunswick
    literal_type: xsd:integer
  AddLiteral (1ae16daf-49f2-449c-ba9c-5b16c618c063)
 Call ID: 1ae16daf-49f2-449c-ba9c-5b16c618c063
  Args:
    literal_value: 1987
    source: :Ernst_August_Hereditary_Prince_of_Brunswick
    relation: :hasDeathYear
    literal_type: xsd:integer
  AssignClass (f41e223e-32b0-4a20-b446-896fed3aab8b)
 Call ID: f41e223e-32b0-4a20-b446-896fed3aab8b
  Args:
    source: :Ernest_Augustus_Duke_of_Brunswick
    type: :Man
  AssignClass (d4f0233d-358e-4960-b9dd-d1f5667772cf)
 Call ID: d4f0233d-358e-4960-b9dd-d1f5667772cf
  Args:
    type: :Person
    source: :Ernest_Augustus_Duke_of_Brunswick
  AssignClass (504889ac-8821-4751-b87a-130ebda8e7f6)
 Call ID: 504889ac-8821-4751-b87a-130ebda8e7f6
  Args:
    type: :Woman
    source: :Princess_Viktoria_Luise_of_Prussia
  AssignClass (f494c995-d6c5-4322-a5f0-d2f1d1bedea1)
 Call ID: f494c995-d6c5-4322-a5f0-d2f1d1bedea1
  Args:
    source: :Princess_Viktoria_Luise_of_Prussia
    type: :Person
  AddTriple (9bb30ffa-7b4f-4d8b-aede-5c0e9bdd7b24)
 Call ID: 9bb30ffa-7b4f-4d8b-aede-5c0e9bdd7b24
  Args:
    target: :Ernest_Augustus_Duke_of_Brunswick
    source: :Ernst_August_Hereditary_Prince_of_Brunswick
    relation: :hasFather
  AddTriple (775cb458-f65c-482b-bf74-7532017b765a)
 Call ID: 775cb458-f65c-482b-bf74-7532017b765a
  Args:
    relation: :hasMother
    source: :Ernst_August_Hereditary_Prince_of_Brunswick
    target: :Princess_Viktoria_Luise_of_Prussia
  AssignClass (85316126-6ccb-4172-a86b-10ecd07cc66b)
 Call ID: 85316126-6ccb-4172-a86b-10ecd07cc66b
  Args:
    type: :Woman
    source: :Princess_Frederica
  AssignClass (07e6e199-fa11-4308-b2d3-db3a0f505da4)
 Call ID: 07e6e199-fa11-4308-b2d3-db3a0f505da4
  Args:
    type: :Person
    source: :Princess_Frederica
  AddTriple (96ba6fde-c934-4e9d-a383-8a56157bd040)
 Call ID: 96ba6fde-c934-4e9d-a383-8a56157bd040
  Args:
    target: :Princess_Frederica
    source: :Ernst_August_Hereditary_Prince_of_Brunswick
    relation: :hasSister
  AssignClass (de08c43a-4253-4070-8344-c8519c54521b)
 Call ID: de08c43a-4253-4070-8344-c8519c54521b
  Args:
    source: :Prince_George_William
    type: :Man
  AssignClass (6ccf00e6-24bc-4da9-b6ec-e82ff0ef58e9)
 Call ID: 6ccf00e6-24bc-4da9-b6ec-e82ff0ef58e9
  Args:
    source: :Prince_George_William
    type: :Person
  AddTriple (4228cf8e-6242-401e-92c7-dbc521a1c71a)
 Call ID: 4228cf8e-6242-401e-92c7-dbc521a1c71a
  Args:
    target: :Prince_George_William
    source: :Ernst_August_Hereditary_Prince_of_Brunswick
    relation: :hasBrother
  AssignClass (7db505bf-b698-40d3-a130-40a63c0ddf23)
 Call ID: 7db505bf-b698-40d3-a130-40a63c0ddf23
  Args:
    source: :Christian_Ernst_August_Hubertus_Freiherr_von_Humboldt_Dachroeden
    type: :Man
  AssignClass (e0c3c381-bbd0-40c4-884b-7946ab8cd9be)
 Call ID: e0c3c381-bbd0-40c4-884b-7946ab8cd9be
  Args:
    source: :Christian_Ernst_August_Hubertus_Freiherr_von_Humboldt_Dachroeden
    type: :Person
  AddTriple (484c41e9-a55b-4e62-aa8d-c8048683f146)
 Call ID: 484c41e9-a55b-4e62-aa8d-c8048683f146
  Args:
    relation: :hasFather
    source: :Christian_Ernst_August_Hubertus_Freiherr_von_Humboldt_Dachroeden
    target: :Ernst_August_Hereditary_Prince_of_Brunswick
  AssignClass (16d452e0-7e3c-439e-ad27-92f31c99fff6)
 Call ID: 16d452e0-7e3c-439e-ad27-92f31c99fff6
  Args:
    source: :Maria_Anna_von_Humboldt_Dachroeden
    type: :Woman
  AssignClass (c7245905-8e28-4db8-817c-432469b5d824)
 Call ID: c7245905-8e28-4db8-817c-432469b5d824
  Args:
    type: :Person
    source: :Maria_Anna_von_Humboldt_Dachroeden
  AddTriple (ad36f832-e9b7-4d4d-9a14-78f339758675)
 Call ID: ad36f832-e9b7-4d4d-9a14-78f339758675
  Args:
    target: :Maria_Anna_von_Humboldt_Dachroeden
    source: :Christian_Ernst_August_Hubertus_Freiherr_von_Humboldt_Dachroeden
    relation: :hasMother
  AssignClass (49b33f98-c3e3-4c8e-a196-31a289df4d00)
 Call ID: 49b33f98-c3e3-4c8e-a196-31a289df4d00
  Args:
    source: :Princess_Ortrud_of_Schleswig_Holstein_Sonderburg_Glücksburg
    type: :Woman
  AssignClass (2fd255f4-6765-47a7-abf7-7c63a5b1193d)
 Call ID: 2fd255f4-6765-47a7-abf7-7c63a5b1193d
  Args:
    source: :Princess_Ortrud_of_Schleswig_Holstein_Sonderburg_Glücksburg
    type: :Person
  AddLiteral (ae373dcf-8d33-4f65-962a-2f0a98537fc3)
 Call ID: ae373dcf-8d33-4f65-962a-2f0a98537fc3
  Args:
    literal_value: 1951
    literal_type: xsd:integer
    relation: :hasMarriageYear
    source: :Ernst_August_Hereditary_Prince_of_Brunswick
  AssignClass (5e59d1b5-f8e2-43a4-b317-71b6dacfbc38)
 Call ID: 5e59d1b5-f8e2-43a4-b317-71b6dacfbc38
  Args:
    type: :Woman
    source: :Countess_Monika_zu_Solms_Laubach
  AssignClass (89fe35e0-7b5a-438a-bfc4-2eff41736254)
 Call ID: 89fe35e0-7b5a-438a-bfc4-2eff41736254
  Args:
    source: :Countess_Monika_zu_Solms_Laubach
    type: :Person
  AddLiteral (d9f71184-5662-4cd8-a6b5-b786bae68577)
 Call ID: d9f71184-5662-4cd8-a6b5-b786bae68577
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    source: :Ernst_August_Hereditary_Prince_of_Brunswick
    literal_value: 1981
  AssignClass (bfeb5d81-aaec-4a77-8854-42fe0a265a54)
 Call ID: bfeb5d81-aaec-4a77-8854-42fe0a265a54
  Args:
    type: :Man
    source: :Georg_9th_Count_of_Solms_Laubach
  AssignClass (173d4bfc-b4ad-47eb-86ed-e61f9db48c94)
 Call ID: 173d4bfc-b4ad-47eb-86ed-e61f9db48c94
  Args:
    source: :Georg_9th_Count_of_Solms_Laubach
    type: :Person
  AssignClass (a1d50e6c-693f-4df4-a9c1-91b1ce5f978e)
 Call ID: a1d50e6c-693f-4df4-a9c1-91b1ce5f978e
  Args:
    type: :Woman
    source: :Princess_Johanna_of_Solms_Hohensolms_Lich
  AssignClass (e5c8dcb0-a7dd-43b7-9544-2d0902ffe43b)
 Call ID: e5c8dcb0-a7dd-43b7-9544-2d0902ffe43b
  Args:
    source: :Princess_Johanna_of_Solms_Hohensolms_Lich
    type: :Person
  AddTriple (424d22f8-2142-456e-b67d-93eff8ce2a57)
 Call ID: 424d22f8-2142-456e-b67d-93eff8ce2a57
  Args:
    source: :Countess_Monika_zu_Solms_Laubach
    relation: :hasFather
    target: :Georg_9th_Count_of_Solms_Laubach
  AddTriple (572131e6-8ce5-4870-b854-db4bd43c5c5c)
 Call ID: 572131e6-8ce5-4870-b854-db4bd43c5c5c
  Args:
    source: :Countess_Monika_zu_Solms_Laubach
    relation: :hasMother
    target: :Princess_Johanna_of_Solms_Hohensolms_Lich
  Finish (50081e7f-de09-4725-b9fd-ff9bcca05d61)
 Call ID: 50081e7f-de09-4725-b9fd-ff9bcca05d61
  Args: