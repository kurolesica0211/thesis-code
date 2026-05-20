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
Prince Richard of Hesse (Richard Wilhelm Leopold; 14
May 1901 – 11 February 1969) was a German prince and politician.
Early life

Prince Richard and his twin brother Christoph were born on 14 May 1901 in Frankfurt am Main, in Prussian Hesse as the fifth son Prince Frederick Charles of Hesse and his wife Princess Margaret of Prussia.
His great-grandmother was Queen Victoria, his mother was the youngest sister of Emperor Wilhelm II.
Richard, affectionately nicknamed "Ri" by his family, grew up in a loving and close-knit family.
Career and later life

The First World War and the fall of the imperial regime

Too young to be mobilized when the First World War broke out, Richard and Prince Christoph of Hesse-Kassel spent most of the conflict in Kronberg, where they were educated at the Reform Realgymnasium.
Unlike his twin brother, who did not take the exam, Richard obtained the abitur in 1920.
Closely linked to the former Kaiser Wilhelm II, whose sister was Princess Margaret, the Hesse-Kassel were then attacked by the revolutionaries.
In this unstable context, Richard and Christoph engage as auxiliaries (hilfsdient) to protect the transports passing through Kronberg while awaiting the arrival of the French occupation troops.
Training and love life

After World War I, Richard studied civil engineering and mechanical engineering at the Darmstadt University of Technology.
From a sentimental point of view, Richard fell in love with Princess Sophie of Greece and Denmark, met around 1927.
However, she fell in love with Richard's twin brother Prince Christoph of Hesse-Kassel, and it is the latter that she married, in 1930.
Adherence to Nazism

Like his three brothers, Richard was enthusiastic about Nazism.
In 1932, the prince thus joined simultaneously the SA and the NSDAP.
Subsequently, Richard became a general (Obergruppenführer) in the Nationalsozialistisches Kraftfahrkorps (NSKK), a special unit of the SA corps, and obtained leadership of the Motorgruppe Hessen in 1935.
From a more political point of view, the prince ran, without success, in the German parliamentary elections of March 1936 and April 1938.
The Second World War and its consequences

Prince Richard enlisted in the German Army shortly after the outbreak of the Second World War.
HAS following the strengthening of the "decree of the princes", Richard was however informed of his dismissal from the army by the Reichsleiter Martin Bormann in October 1943.
At the same time, his older brother Philippe and his sister-in-law Mafalda of Italy were arrested by the Hitler regime while his twin brother, Prince Christoph of Hesse-Kassel, died in a plane crash.
Post-war and its consequences

The defeat of Germany and its occupation by the Allies brought new difficulties to Richard's life.
Arrested by the Americans shortly after the capitulation of his country, the prince was interned for sixteen months in the camp of Moosburg, in Bavaria.
Several months later, the prince underwent a denazification trial.
Meanwhile, the jewels of the House of Hesse-Kassel were stolen by American officers in 1946 and only 10% of the stolen objects were finally returned to their rightful owners, in 1951.
Later years

After the Second World War, Richard assisted his brother Prince Wolfgang of Hesse for a while in the management of the Hessische Hausstiftung.
Subsequently, he was appointed to the traffic surveillance of the state of Hesse.
In the same years, Richard of Hesse-Kassel joined the spiritual movement of “Moral Rearmament”, founded by the Lutheran pastor Frank Buchman.
Prince Richard died in 1969.



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
  AssignClass (78165027-200b-4723-826b-ff0e52743b0c)
 Call ID: 78165027-200b-4723-826b-ff0e52743b0c
  Args:
    type: :Man
    source: Richard_of_Hesse
  AssignClass (dc083a30-1712-4c00-8214-a00a590c631f)
 Call ID: dc083a30-1712-4c00-8214-a00a590c631f
  Args:
    type: :Person
    source: Richard_of_Hesse
  AssignClass (b092e544-6230-469a-ac20-d721d6c029ef)
 Call ID: b092e544-6230-469a-ac20-d721d6c029ef
  Args:
    type: :Man
    source: Christoph_of_Hesse-Kassel
  AssignClass (bf439da6-0255-407b-82b3-5a714a913eb4)
 Call ID: bf439da6-0255-407b-82b3-5a714a913eb4
  Args:
    source: Christoph_of_Hesse-Kassel
    type: :Person
  AssignClass (12bf1e47-5cc2-4950-8919-bd867b55cad9)
 Call ID: 12bf1e47-5cc2-4950-8919-bd867b55cad9
  Args:
    source: Frederick_Charles_of_Hesse
    type: :Man
  AssignClass (0225a0e2-045c-41f1-8715-ebbe3bde9cda)
 Call ID: 0225a0e2-045c-41f1-8715-ebbe3bde9cda
  Args:
    source: Frederick_Charles_of_Hesse
    type: :Person
  AssignClass (2861342f-1804-487d-a9d8-14d9079bf3a5)
 Call ID: 2861342f-1804-487d-a9d8-14d9079bf3a5
  Args:
    type: :Woman
    source: Margaret_of_Prussia
  AssignClass (2d730658-7140-4045-8cd9-d0158ad41121)
 Call ID: 2d730658-7140-4045-8cd9-d0158ad41121
  Args:
    type: :Person
    source: Margaret_of_Prussia
  AssignClass (260592a0-e3e0-4987-bf9d-fc7fd834f0de)
 Call ID: 260592a0-e3e0-4987-bf9d-fc7fd834f0de
  Args:
    source: Sophie_of_Greece_and_Denmark
    type: :Woman
  AssignClass (cf7bfc38-d519-4d06-ad15-a9a7aca01c42)
 Call ID: cf7bfc38-d519-4d06-ad15-a9a7aca01c42
  Args:
    type: :Person
    source: Sophie_of_Greece_and_Denmark
  AssignClass (1dd291c0-5da0-40b4-b840-3a7fb878ebad)
 Call ID: 1dd291c0-5da0-40b4-b840-3a7fb878ebad
  Args:
    source: Philippe_of_Hesse
    type: :Man
  AssignClass (04c6654b-e885-418e-8075-1d623ce89b0d)
 Call ID: 04c6654b-e885-418e-8075-1d623ce89b0d
  Args:
    source: Philippe_of_Hesse
    type: :Person
  AssignClass (54303b45-0724-4c00-8b55-d6872f31c8f8)
 Call ID: 54303b45-0724-4c00-8b55-d6872f31c8f8
  Args:
    type: :Man
    source: Wolfgang_of_Hesse
  AssignClass (7192f85e-f03f-40fc-88fe-68a66c635790)
 Call ID: 7192f85e-f03f-40fc-88fe-68a66c635790
  Args:
    source: Wolfgang_of_Hesse
    type: :Person
  AssignClass (7e7abf42-86a9-4b8c-8d8f-024d631f450d)
 Call ID: 7e7abf42-86a9-4b8c-8d8f-024d631f450d
  Args:
    type: :Sex
    source: Male
  AssignClass (e9304d88-4b9e-484d-8ff7-f212b330afe3)
 Call ID: e9304d88-4b9e-484d-8ff7-f212b330afe3
  Args:
    type: :Sex
    source: Female
  AddLiteral (0a6b5e2a-73e5-4c30-920d-8de606e5bf92)
 Call ID: 0a6b5e2a-73e5-4c30-920d-8de606e5bf92
  Args:
    literal_type: xsd:string
    literal_value: Richard Wilhelm Leopold
    relation: :alsoKnownAs
    source: Richard_of_Hesse
  AddLiteral (d6d62363-643e-4821-ab37-4e0b135e3b0e)
 Call ID: d6d62363-643e-4821-ab37-4e0b135e3b0e
  Args:
    relation: :knownAs
    literal_value: Ri
    literal_type: xsd:string
    source: Richard_of_Hesse
  AddLiteral (931c84dc-18c5-4983-ad4f-13297f5a377f)
 Call ID: 931c84dc-18c5-4983-ad4f-13297f5a377f
  Args:
    literal_value: 1901
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Richard_of_Hesse
  AddLiteral (43fa972e-d4b3-458a-b2a4-1e186c92ba97)
 Call ID: 43fa972e-d4b3-458a-b2a4-1e186c92ba97
  Args:
    source: Richard_of_Hesse
    relation: :hasDeathYear
    literal_value: 1969
    literal_type: xsd:integer
  AddTriple (9fe13136-3fd3-4db2-b122-2ff05e47be68)
 Call ID: 9fe13136-3fd3-4db2-b122-2ff05e47be68
  Args:
    relation: :hasFather
    target: Frederick_Charles_of_Hesse
    source: Richard_of_Hesse
  AddTriple (469e0d15-d6d7-4a96-9647-107791910e42)
 Call ID: 469e0d15-d6d7-4a96-9647-107791910e42
  Args:
    relation: :hasMother
    target: Margaret_of_Prussia
    source: Richard_of_Hesse
  AddTriple (bb6863f0-ca67-4270-9253-dcd98c2d9b4b)
 Call ID: bb6863f0-ca67-4270-9253-dcd98c2d9b4b
  Args:
    relation: :isBrotherOf
    target: Christoph_of_Hesse-Kassel
    source: Richard_of_Hesse
  AddTriple (35a95217-0360-4870-9f2f-e51b5dc7d0e0)
 Call ID: 35a95217-0360-4870-9f2f-e51b5dc7d0e0
  Args:
    relation: :isBrotherOf
    source: Richard_of_Hesse
    target: Philippe_of_Hesse
  AddTriple (ed42d50d-3337-4add-95f3-60c8e2dab270)
 Call ID: ed42d50d-3337-4add-95f3-60c8e2dab270
  Args:
    relation: :isBrotherOf
    source: Richard_of_Hesse
    target: Wolfgang_of_Hesse
  AddTriple (02cfd405-2af7-4f80-8fe8-d64583b5f0a9)
 Call ID: 02cfd405-2af7-4f80-8fe8-d64583b5f0a9
  Args:
    relation: :hasSex
    target: Male
    source: Richard_of_Hesse
  AddTriple (7d94f0fe-547c-479a-955a-33922870718d)
 Call ID: 7d94f0fe-547c-479a-955a-33922870718d
  Args:
    target: Male
    source: Christoph_of_Hesse-Kassel
    relation: :hasSex
  AddTriple (01584468-432c-419f-98ae-34b6c4a2060b)
 Call ID: 01584468-432c-419f-98ae-34b6c4a2060b
  Args:
    relation: :hasSex
    target: Male
    source: Frederick_Charles_of_Hesse
  AddTriple (22494ae5-ac86-4622-9e26-70455a62d282)
 Call ID: 22494ae5-ac86-4622-9e26-70455a62d282
  Args:
    source: Margaret_of_Prussia
    target: Female
    relation: :hasSex
  AddTriple (f92e73e8-95a6-4707-b20b-a5c8d88b0e98)
 Call ID: f92e73e8-95a6-4707-b20b-a5c8d88b0e98
  Args:
    target: Female
    source: Sophie_of_Greece_and_Denmark
    relation: :hasSex
  AddTriple (631fb5f6-2a21-41c6-a027-cb07666a6ded)
 Call ID: 631fb5f6-2a21-41c6-a027-cb07666a6ded
  Args:
    target: Male
    source: Philippe_of_Hesse
    relation: :hasSex
  AddTriple (47c7b48d-9153-4bcb-9a38-8604a9216c8a)
 Call ID: 47c7b48d-9153-4bcb-9a38-8604a9216c8a
  Args:
    target: Male
    source: Wolfgang_of_Hesse
    relation: :hasSex
  AddTriple (eba599f6-9bdc-4655-ba3b-374d6f66a44a)
 Call ID: eba599f6-9bdc-4655-ba3b-374d6f66a44a
  Args:
    relation: :hasFather
    source: Christoph_of_Hesse-Kassel
    target: Frederick_Charles_of_Hesse
  AddTriple (23aadb35-6b0f-47f8-be11-e82219bcbbee)
 Call ID: 23aadb35-6b0f-47f8-be11-e82219bcbbee
  Args:
    relation: :hasMother
    target: Margaret_of_Prussia
    source: Christoph_of_Hesse-Kassel
  AddLiteral (071ffeaf-f4ce-4902-8879-fc934edab5f9)
 Call ID: 071ffeaf-f4ce-4902-8879-fc934edab5f9
  Args:
    source: Christoph_of_Hesse-Kassel
    relation: :hasMarriageYear
    literal_value: 1930
    literal_type: xsd:integer
  AddTriple (5f426374-2122-43bc-bade-425e01dc37d5)
 Call ID: 5f426374-2122-43bc-bade-425e01dc37d5
  Args:
    target: Sophie_of_Greece_and_Denmark
    source: Christoph_of_Hesse-Kassel
    relation: :hasRelation
  Finish (d1460d6e-4fea-40a7-9a63-441ba87cc054)
 Call ID: d1460d6e-4fea-40a7-9a63-441ba87cc054
  Args: