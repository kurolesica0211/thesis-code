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
Prince Luís of Orléans-Braganza (26 January 1878 – 26 March 1920), nicknamed "the Perfect Prince", was the second son of Isabel, Princess Imperial of Brazil and Prince Gaston, Count of Eu, and patriarch of the Vassouras branch of the House of Orléans-Braganza.
In 1908, the year he married, his older brother Pedro renounced his claim to succeed his mother in her claim to the imperial throne, leaving Dom Luís as her heir.
Childhood

Luís was born at Petrópolis on 26 January 1878, to Prince Gaston d'Orléans, Count of Eu, and Isabel, Princess Imperial of Brazil.
His name in full was Luís Maria Filipe Pedro de Alcântara Gastão Miguel Rafael Gonzaga.
While on a trip to Europe with his family, an earthquake occurred on 23 February 1887, and while his older brother Pedro appeared very nervous and cried, Luís simply stood calm and showed no emotions.
Although Pedro was gentle and likeable, he did not like to study and was often clumsy, while Luís had a strong will, was active and apparently intelligent.
Gaston affirmed in another letter, written in March 1890, that "Baby Pedro  always notable for laziness and ineptness," while "Luís does the identical course work all by himself with admirable distinction and capacity."
Luís was always impelled to action thanks to his restless spirit that would take him in his childhood to sports and as an adult to politics.
When the coup that replaced the monarchy with the republic occurred on 15 November 1889, Isabel preferred to send her children to Petrópolis, where later Luís would remember that "locked up in the palace, they had left us during two long days in the most complete ignorance of what was happening out there" until they were sent back to their parents and then left for forced exile.
In 1890, fifteen-year-old Pedro, thirteen-year-old Luís, and their younger brother Antônio (nicknamed "Totó"), moved along with their parents to the outskirts of Versailles.
Luís's older brother, Pedro, reached the age of majority in 1893, but he had no capacity or desire to assume the monarchist cause.
Luís and his brother Antônio followed their older brother at the same military school.
Meanwhile, Luís was ambitious and active, eager to make his mark on the world.
Luís was seen by his parents as the only member of the Imperial family capable of helping the monarchist movement in Brazil.
However, Luís was prevented from disembarking and was not allowed to set foot on his native land by the republican government.
Luís became engaged to his cousin Maria Pia of Bourbon-Two Sicilies, a granddaughter of a brother of Luís's maternal grandmother, Teresa Cristina.
I Prince Pedro de Alcântara Luís Filipe Maria Gastão Miguel Gabriel Rafael Gonzaga of Orléans and Braganza, having maturely reflected, have resolved to renounce the right that, by the Constitution of the Empire of Brazil, promulgated on March 25, 1824, accords to me the Crown of that nation.
Cannes October 30, 1908 signed: Pedro de Alcântara of Orléans-Braganza


This renunciation was followed by a letter from Isabel to royalists in Brazil:

November 9, 1908,  Eu

Most Excellent Gentlemen Members of the Monarchist Directory,

With all my heart I thank you for the congratulations upon the marriages of my dear children Pedro and Luís.
Luís' took place in Cannes on day 4 with the brilliance that is desired for so solemn an act in the life of my successor to the Throne of Brazil.
Before the marriage of Luís he signed his resignation to the crown of Brazil, and here I send it to you, while keeping here an identical copy.
Luís will engage actively in everything with respect to the monarchy and any good for our land.
I give you all my friendship and confidence,

The marriage of Luís and Maria Pia was celebrated on 4 November at Cannes, and that of Pedro and Elizabeth ten days later at Versailles.
From the union of Luís and Maria Pia three children were born: Pedro Henrique, who became the direct successor to Princess Isabel and Head of the Imperial House of Brazil after her death in 1921; Luís Gastão, and Pia Maria.
Isabel did not take long to reveal her opinion about her grandchildren and wrote in a letter in 1914: "I am sending enclosed a photograph of myself with my grandchildren by Luís.
"


Political activity

With the renunciation of the throne by his brother, Luís could finally collaborate effectively with the Brazilian monarchic movement, assuming clearly his position as heir to the throne (after his mother) and trying to assume the leadership of the restoration campaign.
Luís defended ideas that were well ahead of his time and the necessity to guarantee worthy conditions of subsistence for the Brazilian workers would only be observed thirty years later during the dictatorship of Getúlio Vargas.
The progressive vision of Luís made him a target for accusations of being a "socialist" and a "radical" when, in reality, his intent was to hinder the work force from adhering to socialism, communism, or even anarchism.
The start of World War I in August 1914 and the invasion of France by Germany made it possible for Luís to once more prove his idealism and activism as, in his own words, he was a "soldier heart and soul".
Luís joined the army while Antônio served as an air force pilot.
While fighting in the trenches of Flanders in 1915 Luís contracted an aggressive type of bone rheumatism that left him very weak and incapable of walking.
As a consequence of his actions in the conflict and for his bravery, Luís received several decorations: Military medal of the Yser, from King Albert I of Belgium; Legion of Honour, in the degree of knight, and the Cross of War from the French government; the British War Medal, the Victory Medal and Star from the Great Britain.
As his mother lived until 1921, her successor in pretense to the throne of Brazil was her grandson, Pedro Henrique, Luís's son.
"He died, unexpectedly, in Cannes, D. Luiz de Orléans e Bragança, died in exile where he was purging the crime of being Pedro II grandson.
Their presence would shame our phrygian cap..."

— Revista do Brasil

Legacy

Prince Luís is largely unknown to Brazilians today.
The authors dedicated the work to His Imperial Highness the Sire Dom Luiz de Orléans-Braganza.
The Municipality of Pimenta Bueno, in the State of Rondônia (Brazil), honored Dom Luís and the entire Brazilian imperial family in 2010 by renaming one of its streets "Príncipe Dom Luiz de Órleans e Bragança".



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
  AssignClass (54cd50f3-711f-4ac2-a056-be80ec66b9c8)
 Call ID: 54cd50f3-711f-4ac2-a056-be80ec66b9c8
  Args:
    type: :Man
    source: Luís_of_Orléans-Braganza
  AssignClass (cbc6b9fd-8dc0-4d4b-a90b-5d52dff2eaba)
 Call ID: cbc6b9fd-8dc0-4d4b-a90b-5d52dff2eaba
  Args:
    source: Luís_of_Orléans-Braganza
    type: :Person
  AssignClass (27e2902a-2278-4964-84e7-f2c1e03074ce)
 Call ID: 27e2902a-2278-4964-84e7-f2c1e03074ce
  Args:
    type: :Woman
    source: Isabel_Princess_Imperial_of_Brazil
  AssignClass (7a520964-96a9-401b-b5cc-edcfe6a77706)
 Call ID: 7a520964-96a9-401b-b5cc-edcfe6a77706
  Args:
    type: :Person
    source: Isabel_Princess_Imperial_of_Brazil
  AssignClass (73efbb8b-bc46-4def-a2c0-bc95b6960bee)
 Call ID: 73efbb8b-bc46-4def-a2c0-bc95b6960bee
  Args:
    type: :Man
    source: Gaston_Count_of_Eu
  AssignClass (4aaaf233-10e6-474f-afac-4616f0453528)
 Call ID: 4aaaf233-10e6-474f-afac-4616f0453528
  Args:
    type: :Person
    source: Gaston_Count_of_Eu
  AssignClass (03d238c0-ed2c-4793-ae60-aa215a744418)
 Call ID: 03d238c0-ed2c-4793-ae60-aa215a744418
  Args:
    type: :Man
    source: Pedro_of_Orléans-Braganza
  AssignClass (e93bc9fd-a9b5-4764-b0f0-f51c8508d104)
 Call ID: e93bc9fd-a9b5-4764-b0f0-f51c8508d104
  Args:
    type: :Person
    source: Pedro_of_Orléans-Braganza
  AssignClass (8f1c00be-f07c-493c-a45f-c8664589860e)
 Call ID: 8f1c00be-f07c-493c-a45f-c8664589860e
  Args:
    source: Antônio_of_Orléans-Braganza
    type: :Man
  AssignClass (d113b477-4906-47fd-9d5e-e6be75f8ef20)
 Call ID: d113b477-4906-47fd-9d5e-e6be75f8ef20
  Args:
    type: :Person
    source: Antônio_of_Orléans-Braganza
  AssignClass (12d424b9-fa5a-4eb0-b032-fcee81dea4da)
 Call ID: 12d424b9-fa5a-4eb0-b032-fcee81dea4da
  Args:
    source: Maria_Pia_of_Bourbon-Two_Sicilies
    type: :Woman
  AssignClass (5ab5c5ed-ec1f-4aaa-8788-75d82bf2996f)
 Call ID: 5ab5c5ed-ec1f-4aaa-8788-75d82bf2996f
  Args:
    type: :Person
    source: Maria_Pia_of_Bourbon-Two_Sicilies
  AssignClass (1de1a927-66c5-4f2c-a47d-730678ae9d9d)
 Call ID: 1de1a927-66c5-4f2c-a47d-730678ae9d9d
  Args:
    type: :Man
    source: Pedro_Henrique_of_Orléans-Braganza
  AssignClass (0df2e414-5657-48ff-b08f-f21a25c8b5db)
 Call ID: 0df2e414-5657-48ff-b08f-f21a25c8b5db
  Args:
    source: Pedro_Henrique_of_Orléans-Braganza
    type: :Person
  AssignClass (62022a7c-5d0c-4ff3-a4bb-ba9b50fb817c)
 Call ID: 62022a7c-5d0c-4ff3-a4bb-ba9b50fb817c
  Args:
    type: :Man
    source: Luís_Gastão_of_Orléans-Braganza
  AssignClass (58477b33-b5d3-478f-901c-c455fae00785)
 Call ID: 58477b33-b5d3-478f-901c-c455fae00785
  Args:
    type: :Person
    source: Luís_Gastão_of_Orléans-Braganza
  AssignClass (0a82e4cb-cb7d-4387-a6be-528c2589a192)
 Call ID: 0a82e4cb-cb7d-4387-a6be-528c2589a192
  Args:
    type: :Woman
    source: Pia_Maria_of_Orléans-Braganza
  AssignClass (f93ca13d-0a15-4a54-b117-90961c246b78)
 Call ID: f93ca13d-0a15-4a54-b117-90961c246b78
  Args:
    source: Pia_Maria_of_Orléans-Braganza
    type: :Person
  AddLiteral (e03a252b-989d-44d6-bc2f-f612df8eb00d)
 Call ID: e03a252b-989d-44d6-bc2f-f612df8eb00d
  Args:
    literal_value: 1878
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Luís_of_Orléans-Braganza
  AddLiteral (436fa1cf-7352-4e70-bc43-36fa342e83f7)
 Call ID: 436fa1cf-7352-4e70-bc43-36fa342e83f7
  Args:
    literal_type: xsd:integer
    source: Luís_of_Orléans-Braganza
    relation: :hasDeathYear
    literal_value: 1920
  AddTriple (076cd7e8-54e3-44f6-bf19-ff02c65492e2)
 Call ID: 076cd7e8-54e3-44f6-bf19-ff02c65492e2
  Args:
    target: Gaston_Count_of_Eu
    source: Luís_of_Orléans-Braganza
    relation: :hasFather
  AddTriple (d78a029c-3e86-4fe5-8f2a-d85ccc279b46)
 Call ID: d78a029c-3e86-4fe5-8f2a-d85ccc279b46
  Args:
    target: Isabel_Princess_Imperial_of_Brazil
    relation: :hasMother
    source: Luís_of_Orléans-Braganza
  AddTriple (c7e759c5-1f22-4b55-a9d3-51e169e67efc)
 Call ID: c7e759c5-1f22-4b55-a9d3-51e169e67efc
  Args:
    target: Pedro_of_Orléans-Braganza
    source: Luís_of_Orléans-Braganza
    relation: :isBrotherOf
  AddTriple (8a81208e-c3d6-4c78-9e95-0ca9ea1710fd)
 Call ID: 8a81208e-c3d6-4c78-9e95-0ca9ea1710fd
  Args:
    relation: :isBrotherOf
    source: Luís_of_Orléans-Braganza
    target: Antônio_of_Orléans-Braganza
  AddTriple (0f28f8b2-7d72-4eb7-9838-612905dd65c2)
 Call ID: 0f28f8b2-7d72-4eb7-9838-612905dd65c2
  Args:
    target: Gaston_Count_of_Eu
    source: Pedro_of_Orléans-Braganza
    relation: :hasFather
  AddTriple (985df99c-6516-40c7-aeb1-7cc1cb25aa04)
 Call ID: 985df99c-6516-40c7-aeb1-7cc1cb25aa04
  Args:
    source: Pedro_of_Orléans-Braganza
    relation: :hasMother
    target: Isabel_Princess_Imperial_of_Brazil
  AddTriple (360ab40d-df91-434f-b6a2-44850030bf0d)
 Call ID: 360ab40d-df91-434f-b6a2-44850030bf0d
  Args:
    target: Gaston_Count_of_Eu
    source: Antônio_of_Orléans-Braganza
    relation: :hasFather
  AddTriple (f3a0069f-56ad-4d48-92ab-c4713232b0a7)
 Call ID: f3a0069f-56ad-4d48-92ab-c4713232b0a7
  Args:
    target: Isabel_Princess_Imperial_of_Brazil
    relation: :hasMother
    source: Antônio_of_Orléans-Braganza
  AddTriple (ffba2aa8-aa85-4d2c-b745-88f595453ba6)
 Call ID: ffba2aa8-aa85-4d2c-b745-88f595453ba6
  Args:
    target: Luís_of_Orléans-Braganza
    relation: :hasFather
    source: Pedro_Henrique_of_Orléans-Braganza
  AddTriple (0b14a4ad-e0ef-421b-b272-dd70a1e8eef9)
 Call ID: 0b14a4ad-e0ef-421b-b272-dd70a1e8eef9
  Args:
    source: Pedro_Henrique_of_Orléans-Braganza
    relation: :hasMother
    target: Maria_Pia_of_Bourbon-Two_Sicilies
  AddTriple (93ba923e-76bf-489c-ae12-3a95f6546471)
 Call ID: 93ba923e-76bf-489c-ae12-3a95f6546471
  Args:
    source: Luís_Gastão_of_Orléans-Braganza
    relation: :hasFather
    target: Luís_of_Orléans-Braganza
  AddTriple (e8ba3bc8-cf51-4675-8cdc-6f93374c7d78)
 Call ID: e8ba3bc8-cf51-4675-8cdc-6f93374c7d78
  Args:
    relation: :hasMother
    source: Luís_Gastão_of_Orléans-Braganza
    target: Maria_Pia_of_Bourbon-Two_Sicilies
  AddTriple (b54648b4-fb68-4710-94a7-bf0aa3a539d4)
 Call ID: b54648b4-fb68-4710-94a7-bf0aa3a539d4
  Args:
    target: Luís_of_Orléans-Braganza
    source: Pia_Maria_of_Orléans-Braganza
    relation: :hasFather
  AddTriple (e83c908d-9243-449d-923b-ff20fed95df9)
 Call ID: e83c908d-9243-449d-923b-ff20fed95df9
  Args:
    target: Maria_Pia_of_Bourbon-Two_Sicilies
    source: Pia_Maria_of_Orléans-Braganza
    relation: :hasMother
  AddLiteral (5ea6fbb7-c40e-4c33-8ae8-9d5bc1161191)
 Call ID: 5ea6fbb7-c40e-4c33-8ae8-9d5bc1161191
  Args:
    literal_value: 1908
    relation: :hasMarriageYear
    source: Luís_of_Orléans-Braganza
    literal_type: xsd:integer
  Finish (edff6363-5b32-40a5-a59c-3a46846ad5e0)
 Call ID: edff6363-5b32-40a5-a59c-3a46846ad5e0
  Args: