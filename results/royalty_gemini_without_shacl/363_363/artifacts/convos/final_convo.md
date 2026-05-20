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
Therefore, the titles Prince of Hanover, Duke of Brunswick and Lüneburg could not be mentioned there, nor could the British titles due to the Titles Deprivation Act 1917.
The name which was finally entered into his British documents, was thus Ernest Augustus Guelph, with the addition of His Royal Highness.
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

:hasDeathYear a owl:AnnotationProperty .

:hasMarriageYear a owl:AnnotationProperty .

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

:hasChild a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:inverseOf :isChildOf .

:isAncestorOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation .

:isSiblingOf a owl:ObjectProperty,
        owl:SymmetricProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isBloodrelationOf ;
    owl:propertyChainAxiom ( :hasParent :isParentOf ) .

:isSisterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf .

:hasParent a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Person ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:equivalentProperty :isChildOf ;
    owl:inverseOf :isParentOf .

:Sex a owl:Class ;
    rdfs:subClassOf :DomainEntity ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Female :Male ) ] .

:isChildOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:propertyDisjointWith :isSisterOf .

:Man a owl:Class ;
    owl:disjointWith :Sex,
        :Woman ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Male ] ) ] .

:Woman a owl:Class ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Female ] ) ] .

:isParentOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:propertyDisjointWith :isSisterOf .

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



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (5f655fb2-fc92-45ac-8844-d04e21079c20)
 Call ID: 5f655fb2-fc92-45ac-8844-d04e21079c20
  Args:
    type: :Man
    source: Ernst_August_of_Hanover
  AssignClass (99eaf1b6-67c7-46ac-afd6-abe04a11a9b4)
 Call ID: 99eaf1b6-67c7-46ac-afd6-abe04a11a9b4
  Args:
    type: :Man
    source: Ernest_Augustus_Duke_of_Brunswick
  AssignClass (3e66936b-59d7-4e08-b134-2ddc09518274)
 Call ID: 3e66936b-59d7-4e08-b134-2ddc09518274
  Args:
    type: :Woman
    source: Viktoria_Luise_of_Prussia
  AssignClass (c8cb3a84-51d5-4cde-84cc-3fcb7c78c55b)
 Call ID: c8cb3a84-51d5-4cde-84cc-3fcb7c78c55b
  Args:
    type: :Woman
    source: Frederica_of_Hanover
  AssignClass (f65ca00e-4d6a-4764-adb5-1fade3191393)
 Call ID: f65ca00e-4d6a-4764-adb5-1fade3191393
  Args:
    type: :Man
    source: George_William_of_Hanover
  AssignClass (1b5ab8ea-27bd-47f3-a313-fa0799e1e46a)
 Call ID: 1b5ab8ea-27bd-47f3-a313-fa0799e1e46a
  Args:
    type: :Man
    source: Christian_Ernst_August_Hubertus_von_Humboldt-Dachroeden
  AssignClass (b4bded5e-8f47-4176-b022-39d0656782e9)
 Call ID: b4bded5e-8f47-4176-b022-39d0656782e9
  Args:
    type: :Woman
    source: Maria_Anna_von_Humboldt-Dachroeden
  AssignClass (aef08f2e-f681-4594-b38e-2e7b716a077e)
 Call ID: aef08f2e-f681-4594-b38e-2e7b716a077e
  Args:
    type: :Woman
    source: Ortrud_of_Schleswig-Holstein-Sonderburg-Glücksburg
  AssignClass (fad0e0da-b9b1-429e-b318-a12da6dbd472)
 Call ID: fad0e0da-b9b1-429e-b318-a12da6dbd472
  Args:
    type: :Woman
    source: Monika_zu_Solms-Laubach
  AssignClass (a33deb04-8cbf-45cf-ab9e-8750e56a862c)
 Call ID: a33deb04-8cbf-45cf-ab9e-8750e56a862c
  Args:
    type: :Man
    source: Georg_9th_Count_of_Solms-Laubach
  AssignClass (0bab4137-2146-4725-9f03-db07dc7b6f0f)
 Call ID: 0bab4137-2146-4725-9f03-db07dc7b6f0f
  Args:
    type: :Woman
    source: Johanna_of_Solms-Hohensolms-Lich
  AddLiteral (fbfab819-254e-4f62-bf2f-6a27644f6532)
 Call ID: fbfab819-254e-4f62-bf2f-6a27644f6532
  Args:
    literal_type: xsd:integer
    source: Ernst_August_of_Hanover
    relation: :hasBirthYear
    literal_value: 1914
  AddLiteral (36202f51-ea1f-4dc9-91e6-040481f6de7c)
 Call ID: 36202f51-ea1f-4dc9-91e6-040481f6de7c
  Args:
    literal_type: xsd:integer
    source: Ernst_August_of_Hanover
    literal_value: 1987
    relation: :hasDeathYear
  AddTriple (356745ac-a9b7-4e3e-9f2a-b7b8ed92b35e)
 Call ID: 356745ac-a9b7-4e3e-9f2a-b7b8ed92b35e
  Args:
    relation: :hasFather
    source: Ernst_August_of_Hanover
    target: Ernest_Augustus_Duke_of_Brunswick
  AddTriple (cabd21bd-6a3b-462b-8e78-6a588610093b)
 Call ID: cabd21bd-6a3b-462b-8e78-6a588610093b
  Args:
    source: Ernst_August_of_Hanover
    target: Viktoria_Luise_of_Prussia
    relation: :hasMother
  AddTriple (512b3099-923b-4cea-8dff-5642cdfdb717)
 Call ID: 512b3099-923b-4cea-8dff-5642cdfdb717
  Args:
    relation: :hasSister
    source: Ernst_August_of_Hanover
    target: Frederica_of_Hanover
  AddTriple (accd6b89-7fc8-47ec-9484-cce30ced4896)
 Call ID: accd6b89-7fc8-47ec-9484-cce30ced4896
  Args:
    source: Ernst_August_of_Hanover
    target: George_William_of_Hanover
    relation: :hasBrother
  AddTriple (6cd7bb3c-cb40-495c-a5ba-b2fa178ec345)
 Call ID: 6cd7bb3c-cb40-495c-a5ba-b2fa178ec345
  Args:
    relation: :hasFather
    target: Ernst_August_of_Hanover
    source: Christian_Ernst_August_Hubertus_von_Humboldt-Dachroeden
  AddTriple (91668fef-4062-4657-8474-bb120d3675de)
 Call ID: 91668fef-4062-4657-8474-bb120d3675de
  Args:
    relation: :hasMother
    target: Maria_Anna_von_Humboldt-Dachroeden
    source: Christian_Ernst_August_Hubertus_von_Humboldt-Dachroeden
  AddLiteral (c3d6c809-906a-485a-8e40-7bd0eb59e738)
 Call ID: c3d6c809-906a-485a-8e40-7bd0eb59e738
  Args:
    source: Ernst_August_of_Hanover
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 1951
  AddTriple (a62006b2-e7fd-4eb0-a9dc-42ddeacce050)
 Call ID: a62006b2-e7fd-4eb0-a9dc-42ddeacce050
  Args:
    relation: :hasRelation
    source: Ernst_August_of_Hanover
    target: Ortrud_of_Schleswig-Holstein-Sonderburg-Glücksburg
  AddLiteral (f671f63d-4a11-49cd-85bb-fbb88d072c06)
 Call ID: f671f63d-4a11-49cd-85bb-fbb88d072c06
  Args:
    relation: :hasMarriageYear
    literal_value: 1981
    source: Ernst_August_of_Hanover
    literal_type: xsd:integer
  AddTriple (5274398d-63d8-4366-88b6-b5f733bc695d)
 Call ID: 5274398d-63d8-4366-88b6-b5f733bc695d
  Args:
    relation: :hasRelation
    source: Ernst_August_of_Hanover
    target: Monika_zu_Solms-Laubach
  AddTriple (d441650b-ab42-407a-b966-96d272e655dc)
 Call ID: d441650b-ab42-407a-b966-96d272e655dc
  Args:
    target: Georg_9th_Count_of_Solms-Laubach
    source: Monika_zu_Solms-Laubach
    relation: :hasFather
  AddTriple (5f6b42c5-0525-463b-a364-2778eda559e3)
 Call ID: 5f6b42c5-0525-463b-a364-2778eda559e3
  Args:
    target: Johanna_of_Solms-Hohensolms-Lich
    source: Monika_zu_Solms-Laubach
    relation: :hasMother
  Finish (f89c01b3-7c45-45d7-bedb-97f00b9a8ff4)
 Call ID: f89c01b3-7c45-45d7-bedb-97f00b9a8ff4
  Args: