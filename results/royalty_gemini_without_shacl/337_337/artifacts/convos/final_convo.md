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
Georg Friedrich Prinz von Preussen (born 10 June 1976, as Georg Friedrich Ferdinand Prinz von Preußen) is a German heir who is the current head of the Prussian branch of the House of Hohenzollern, a dynasty that ruled over the German Empire and the Kingdom of Prussia until near the end of World War I.
He is the great-great-grandson of Wilhelm II, the last German Emperor and last King of Prussia, who abdicated and went into exile upon Germany's defeat in World War I in 1918.
Education and career

Georg Friedrich is the only son and eldest child of Louis Ferdinand Prinz von Preussen (1944–1977) and Countess Donata of Castell-Rüdenhausen (1950–2015).
Born into a mediatised princely family, his mother later became Duchess Donata of Oldenburg when she married secondly Duke Friedrich August of Oldenburg, who had previously been married to her sister-in-law Princess Marie Cécile of Prussia.
Georg Friedrich earned his degree in business economics at the Freiberg University of Mining and Technology.
Georg Friedrich works for a company specialising in helping universities to bring their innovations to market.
He also administered the Princess Kira of Prussia Foundation, founded by his grandmother Grand Duchess Kira of Russia in 1952, now administered by his wife.
Until 30 December 2025, Georg Friedrich owned a two-thirds share of his family's original seat, Hohenzollern Castle, with the head of the Swabian branch, Karl Friedrich, Prince of Hohenzollern, owning the remaining third.
In an agreement taking effect on 31 December 2025, Karl Friedrich transferred his share to Georg Friedrich, giving the latter full responsibility for the operation, maintenance and cultural development of the castle.
Georg Friedrich continues to claim compensation for land and palaces in Berlin expropriated from his family, a claim begun in March 1991 by his grandfather Prince Louis Ferdinand of Prussia under the Compensation Act (EALG).
House of Hohenzollern

Georg Friedrich succeeded his grandfather, Louis Ferdinand, as Head of the Royal House of Prussia, a branch of the House of Hohenzollern, on 26 September 1994.
His position as sole heir to the estate of his grandfather was challenged by his uncles, Friedrich Wilhelm and Michael, who filed a lawsuit claiming that, despite their renunciations as dynasts at the time of their marriages, the loss of their inheritance rights based on their selection of spouse was discriminatory and unconstitutional.
However, the Federal Court of Justice of Germany overturned the original rulings in favour of Georg Friedrich's uncles, the case being remanded to the courts at Hechingen and Stuttgart.
This time both courts ruled in favour of Georg Friedrich.
His uncles then took their case to the Federal Constitutional Court of Germany which overruled the previous court rulings in Georg Friedrich's favour, on 22 March 2004.
On 19 October 2005, a German regional court ruled that Georg Friedrich was indeed the principal heir of his grandfather, Louis Ferdinand (who was the primary beneficiary of the trust set up for the estate of Wilhelm II), but also concluded that each of the children of Louis Ferdinand was entitled to a portion of the Prussian inheritance.
Family

In 2011, Georg Friedrich married Princess Sophie of Isenburg.
On 20 January 2013, Georg Friedrich's wife, Sophie, gave birth to twin sons in Bremen, Carl Friedrich Franz Alexander and Louis Ferdinand Christian Albrecht.
Carl Friedrich, the elder of the two, is his father's heir apparent.
On 17 November 2016, Sophie gave birth to Heinrich Albert Johann Georg, their fourth child.
Property claims

In 2014, Georg Friedrich filed a claim on the property of the Huis Doorn, where Kaiser Wilhelm II spent his last years after abdication, but this was rejected by Minister of Education, Culture and Science Jet Bussemaker.
In mid-2019 it was revealed that, since 2014, Georg Friedrich had filed claims for permanent right of residency for his family in Cecilienhof, or one of two other former Hohenzollern palaces in Potsdam, as well as return of the family library, 266 paintings, an imperial crown and sceptre, and the letters of Empress Augusta Victoria.
This sparked a public debate about the legitimacy of these claims and the role of the Hohenzollern during and before the Nazi regime in Germany, specifically Crown Prince Wilhelm's involvement.
On 9 March 2023, Georg Friedrich dropped the suit, hoping that doing so would "open the way for an unencumbered historical debate on the role of my family in the 20th Century following the end of the monarchy.
"


In June 2019, a claim made by Georg Friedrich that Rheinfels Castle be returned to the Hohenzollern family was dismissed by a court.
}} Media related to Georg Friedrich, Prince of Prussia at Wikimedia Commons



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
  AssignClass (cbdd060a-fd45-4284-9727-e2d5621525a6)
 Call ID: cbdd060a-fd45-4284-9727-e2d5621525a6
  Args:
    type: :Man
    source: Georg_Friedrich_Prinz_von_Preussen
  AssignClass (bd17c12b-e38e-4068-80ec-64c52e388ece)
 Call ID: bd17c12b-e38e-4068-80ec-64c52e388ece
  Args:
    type: :Person
    source: Georg_Friedrich_Prinz_von_Preussen
  AssignClass (fbd10cdf-06ae-49cd-b627-901034f956a3)
 Call ID: fbd10cdf-06ae-49cd-b627-901034f956a3
  Args:
    type: :Man
    source: Louis_Ferdinand_Prinz_von_Preussen
  AssignClass (95bb6f59-d9e0-4044-a655-048351f36365)
 Call ID: 95bb6f59-d9e0-4044-a655-048351f36365
  Args:
    type: :Ancestor
    source: Louis_Ferdinand_Prinz_von_Preussen
  AssignClass (07f6de9c-9f0f-4fa2-a45f-0928802b6cf1)
 Call ID: 07f6de9c-9f0f-4fa2-a45f-0928802b6cf1
  Args:
    type: :Woman
    source: Donata_of_Castell-Rüdenhausen
  AssignClass (5c175f21-5684-4145-9331-32df4c430422)
 Call ID: 5c175f21-5684-4145-9331-32df4c430422
  Args:
    source: Donata_of_Castell-Rüdenhausen
    type: :Person
  AssignClass (c4a565ff-968b-4d3e-9599-bb6e401ede16)
 Call ID: c4a565ff-968b-4d3e-9599-bb6e401ede16
  Args:
    type: :Man
    source: Wilhelm_II
  AssignClass (7f5d5882-8233-4b0e-a979-fea8c77b6082)
 Call ID: 7f5d5882-8233-4b0e-a979-fea8c77b6082
  Args:
    source: Wilhelm_II
    type: :Ancestor
  AssignClass (deed0ffc-5f63-4bff-9333-f20bdbed5cf6)
 Call ID: deed0ffc-5f63-4bff-9333-f20bdbed5cf6
  Args:
    source: Princess_Sophie_of_Isenburg
    type: :Woman
  AssignClass (b07ce37b-ee50-4c6a-9eaf-8466a1cd503a)
 Call ID: b07ce37b-ee50-4c6a-9eaf-8466a1cd503a
  Args:
    type: :Person
    source: Princess_Sophie_of_Isenburg
  AssignClass (7e5a228e-737f-4c68-90f5-f3d73f06740d)
 Call ID: 7e5a228e-737f-4c68-90f5-f3d73f06740d
  Args:
    type: :Man
    source: Carl_Friedrich_Franz_Alexander
  AssignClass (3148b809-3f04-4d3d-9a2c-681c44d9e216)
 Call ID: 3148b809-3f04-4d3d-9a2c-681c44d9e216
  Args:
    type: :Person
    source: Carl_Friedrich_Franz_Alexander
  AssignClass (8b57060f-9e55-4bd0-bd96-7536ce08ab35)
 Call ID: 8b57060f-9e55-4bd0-bd96-7536ce08ab35
  Args:
    source: Louis_Ferdinand_Christian_Albrecht
    type: :Man
  AssignClass (30ef9d67-b18f-4fd4-b4a4-d08a23530a11)
 Call ID: 30ef9d67-b18f-4fd4-b4a4-d08a23530a11
  Args:
    type: :Person
    source: Louis_Ferdinand_Christian_Albrecht
  AssignClass (9f1f3e6a-6c1c-47b9-b7aa-f0ba189f5228)
 Call ID: 9f1f3e6a-6c1c-47b9-b7aa-f0ba189f5228
  Args:
    type: :Man
    source: Heinrich_Albert_Johann_Georg
  AssignClass (81bf2178-3d4d-451a-9d8b-45c0afab8a91)
 Call ID: 81bf2178-3d4d-451a-9d8b-45c0afab8a91
  Args:
    type: :Person
    source: Heinrich_Albert_Johann_Georg
  AddLiteral (c06f9002-48ea-4e03-954f-07a934991e40)
 Call ID: c06f9002-48ea-4e03-954f-07a934991e40
  Args:
    relation: :hasBirthYear
    source: Georg_Friedrich_Prinz_von_Preussen
    literal_type: xsd:integer
    literal_value: 1976
  AddTriple (16417999-66c9-4d66-b364-5f070681105b)
 Call ID: 16417999-66c9-4d66-b364-5f070681105b
  Args:
    target: Louis_Ferdinand_Prinz_von_Preussen
    relation: :hasFather
    source: Georg_Friedrich_Prinz_von_Preussen
  AddTriple (110d82d9-ebb2-42ed-a1dd-00dcd1c33199)
 Call ID: 110d82d9-ebb2-42ed-a1dd-00dcd1c33199
  Args:
    target: Donata_of_Castell-Rüdenhausen
    relation: :hasMother
    source: Georg_Friedrich_Prinz_von_Preussen
  AddTriple (ba8052b3-15cb-4b35-8759-454d1d0c04d6)
 Call ID: ba8052b3-15cb-4b35-8759-454d1d0c04d6
  Args:
    target: Georg_Friedrich_Prinz_von_Preussen
    source: Carl_Friedrich_Franz_Alexander
    relation: :hasFather
  AddTriple (c97fe501-f756-48aa-8101-58bde82c4d4b)
 Call ID: c97fe501-f756-48aa-8101-58bde82c4d4b
  Args:
    relation: :hasMother
    source: Carl_Friedrich_Franz_Alexander
    target: Princess_Sophie_of_Isenburg
  AddTriple (58114f2b-8025-4d26-9d26-8ec388790aa6)
 Call ID: 58114f2b-8025-4d26-9d26-8ec388790aa6
  Args:
    relation: :hasFather
    source: Louis_Ferdinand_Christian_Albrecht
    target: Georg_Friedrich_Prinz_von_Preussen
  AddTriple (b82cb32a-69c3-41b9-b448-4ff75bc08987)
 Call ID: b82cb32a-69c3-41b9-b448-4ff75bc08987
  Args:
    relation: :hasMother
    source: Louis_Ferdinand_Christian_Albrecht
    target: Princess_Sophie_of_Isenburg
  AddTriple (b61ab738-bf0f-471a-a820-3bceff605135)
 Call ID: b61ab738-bf0f-471a-a820-3bceff605135
  Args:
    source: Heinrich_Albert_Johann_Georg
    relation: :hasFather
    target: Georg_Friedrich_Prinz_von_Preussen
  AddTriple (1bb5a800-e280-4d98-b86f-9bf9fad11293)
 Call ID: 1bb5a800-e280-4d98-b86f-9bf9fad11293
  Args:
    target: Princess_Sophie_of_Isenburg
    source: Heinrich_Albert_Johann_Georg
    relation: :hasMother
  Finish (a5f2e9ca-4cd3-4f99-ab78-ca8c79d8f14a)
 Call ID: a5f2e9ca-4cd3-4f99-ab78-ca8c79d8f14a
  Args: