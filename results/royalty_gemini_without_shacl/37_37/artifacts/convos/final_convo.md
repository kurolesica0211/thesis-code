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
María de las Mercedes, Princess of Asturias (María de las Mercedes de Borbón y Habsburgo-Lorena; 11 September 1880 – 17 October 1904) was the eldest child of King Alfonso XII of Spain and his second wife, Maria Christina of Austria.
She was Princess of Asturias, the heiress presumptive to the Crown of Spain, for all 24 years of her life.
Had her younger sibling, unborn at the death of Alfonso XII, been a daughter, Mercedes would have been Queen of Spain.
The sibling proved to be a boy, Alfonso XIII, and upon his birth in 1886, he was King, and Mercedes turned out not to be queen.
She resumed the position of heiress presumptive, which she held until her own death (aged 24), and was succeeded in it by her own infant son Alfonso, Alfonso XIII having not yet married and fathered a legitimate child.
Mercedes married in Madrid on 14 February 1901, her second cousin, Prince Carlos of Bourbon-Two Sicilies, a nephew of the King of the then-defunct Kingdom of the Two Sicilies, who was elevated to the rank of Infante of Spain.
Early life

Born on 11 September 1880 at the Royal Palace of Madrid, Mercedes was the first child of King Alfonso XII and his second wife, Maria Christina of Austria.
She was christened María de las Mercedes Isabel Teresa Cristina Alfonsa.
To smooth things out, Queen Maria Christina suggested giving their new daughter the name Mercedes in honor of her husband's first wife and Queen, Mercedes of Orléans.
Mercedes was heiress presumptive at birth, but the disappointment was so great that she was initially treated only as an infanta.
Antonio Cánovas del Castillo, then head of the government, who disliked Maria Christina and did not want the crown to pass again to a female after the disastrous reign of Isabella II, decided functionally to ignore the newborn.
Mercedes's paternal aunt Isabella retained the title of Princess of Asturias until Práxedes Mateo Sagasta, President of the government that had replaced Cánovas, pressured King Alfonso XII to accord the title to Mercedes, which he did on 10 March 1881.
On 12 November 1882, Mercedes gained a sister, Infanta Maria Teresa.
Alfonso had married Maria Christina in order to secure the succession to the throne.
In July 1883, Maria Christina left the Spanish court and traveled with her daughters to visit her own family in Austria.
By the summer of 1884, Alfonso XII's health had deteriorated: he had tuberculosis.
Given the nascent pregnancy, Mercedes was not declared queen because she would be displaced if a son was born — instead, there was a six month interregnum until the birth of her brother Alfonso XIII on 17 May 1886, who assumed the throne as king immediately upon birth.
Had the pregnancy been lost or resulted in another daughter, Mercedes would have been declared queen regnant and been retroactively recognized as having assumed the throne at the death of her father (there would have been no interregnum).
Instead, with the late king's new issue arriving, and being a boy, Mercedes resumed the position of heiress presumptive, a title she would continue to hold for the rest of her short life.
Education

Mercedes made her first public appearance at the royal court by the hand of her mother when Queen Maria Christina was declared regent.
The education of the Princess of Asturias and her younger sister Infanta Maria Teresa was confined to the Royal Palace of Madrid in an austere environment headed by two widows: their mother and their paternal aunt Isabella (herself formerly Princess of Asturias).
Despite her constitutional status, Mercedes was not given an education that would have prepared her to govern the nation.
Mercedes grew up to be a serious young woman, shy and unprepossessing.
In her adolescence, Mercedes accompanied her mother on trips abroad visiting her paternal grandmother in Paris, her paternal aunt Paz in Munich, and her maternal grandmother Elisabeth Franziska in Vienna.
The situation in Spain became more complicated with the Spanish–American War in 1898.
Mercedes and her sister lived a restricted life.
At the dance, Mercedes fell in love with her cousin Prince Carlos of Bourbon-Two Sicilies, and the two were frequently seen together.
Marriage

Prince Carlos, Queen Maria Christina's first cousin once removed, belonged to the deposed royal family of the Two Sicilies and had arrived in Spain years earlier in order to follow a military career in the Spanish army.
The pairing of the princess and Prince Carlos was not accidental.
He had been chosen as a prospective husband by both Queen Maria Christina and Infanta Isabella, who was his aunt as well.
It was considered paramount to marry Mercedes to a member of the Bourbon family in order to avoid a change of the dynasty in case she succeeded her brother.
Prince Carlos offered other advantages as groom to the Princess of Asturias.
As he did not belong to a reigning royal family, he could settle permanently in Spain and adopt the necessary Spanish nationality.
Carlos was of serious character, shy, handsome, and Mercedes was attracted to him.
It was feared that Caserta's son marrying Mercedes would bring the Carlist party too close to the Spanish throne.
Even the Prince's name – Carlos – aroused suspicion.
There were bitter attacks against Mercedes's marriage in the newspapers and protest on the streets in Madrid, Seville and Granada.
The Archbishop of Valladolid, one of Spain’s most prominent prelates, wrote a letter to the Queen warning her against the dire consequences if the marriage would take place.
Mercedes herself expressed her frustration to the strong opposition to her choice of groom in a letter to her aunt Paz: "I am happy to marry him, but I am also upset at those who have created such a fuss and made mother suffer for this... all because his father fought alongside don Carlos.
Death

The couple lived at the Royal Palace of Madrid in close proximity to Queen Maria Christina, who wished for such proximity.
The union was happy and two children were born in quick succession: Prince Alfonso (1901–1964) and Prince Fernando (1903–1905).
Pregnant for the third time, Mercedes longed for a daughter after having two sons.
The following month, twenty days before her due day, Mercedes fell seriously ill.
Peritonitis set in and on the early hours on 16 October 1904 Mercedes gave birth prematurely to her third child, Princess Isabella Alfonsa (1904–1985).
The health of the mother was so seriously compromised that little attention was given to the child, who was believed to have been stillborn until the young King Alfonso realized the baby was alive.
Mercedes died the following day, on 17 October 1904, surrounded by her family.
Mercedes' three children were left in the care of Queen Maria Christina and raised in the court of King Alfonso XIII.
The elder son was not given the title of Prince of Asturias, but replaced his mother as heir presumptive.



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
  AssignClass (bc125a30-45d6-4961-9913-a6dc93a6e847)
 Call ID: bc125a30-45d6-4961-9913-a6dc93a6e847
  Args:
    type: :Woman
    source: Mercedes
  AssignClass (f2d412a0-25bd-4ce1-a8de-9e1e657882cb)
 Call ID: f2d412a0-25bd-4ce1-a8de-9e1e657882cb
  Args:
    source: Mercedes
    type: :Ancestor
  AddLiteral (7613f1f3-9715-45e7-9bdc-78dd078d2118)
 Call ID: 7613f1f3-9715-45e7-9bdc-78dd078d2118
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1880
    source: Mercedes
  AddLiteral (9b1ed9c9-f39d-47a1-a664-90e3bdb25149)
 Call ID: 9b1ed9c9-f39d-47a1-a664-90e3bdb25149
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: Mercedes
    literal_value: 1904
  AssignClass (e4351b68-f2f7-411b-9b7b-d5af00138b05)
 Call ID: e4351b68-f2f7-411b-9b7b-d5af00138b05
  Args:
    source: Alfonso_XII
    type: :Man
  AssignClass (f4cfe117-f227-46e0-8742-5237eeb79a7b)
 Call ID: f4cfe117-f227-46e0-8742-5237eeb79a7b
  Args:
    type: :Ancestor
    source: Alfonso_XII
  AssignClass (ec867e9a-d12e-4abc-b3da-83bef7dd73c4)
 Call ID: ec867e9a-d12e-4abc-b3da-83bef7dd73c4
  Args:
    source: Maria_Christina
    type: :Woman
  AssignClass (d92d461f-40fb-4396-9292-f6dec1508efb)
 Call ID: d92d461f-40fb-4396-9292-f6dec1508efb
  Args:
    type: :Ancestor
    source: Maria_Christina
  AddTriple (d0a90dee-42a4-49e2-96bb-35084c8a50c1)
 Call ID: d0a90dee-42a4-49e2-96bb-35084c8a50c1
  Args:
    target: Alfonso_XII
    source: Mercedes
    relation: :hasFather
  AddTriple (ca592dba-8d6b-4746-9259-f522202c0fc9)
 Call ID: ca592dba-8d6b-4746-9259-f522202c0fc9
  Args:
    relation: :hasMother
    source: Mercedes
    target: Maria_Christina
  AssignClass (9106b079-a60c-4e0d-8826-33c0e2e2392d)
 Call ID: 9106b079-a60c-4e0d-8826-33c0e2e2392d
  Args:
    source: Alfonso_XIII
    type: :Man
  AssignClass (cbdd8cf5-161a-4ffc-ba53-299cdd0f2afc)
 Call ID: cbdd8cf5-161a-4ffc-ba53-299cdd0f2afc
  Args:
    type: :Ancestor
    source: Alfonso_XIII
  AddTriple (73e9966a-8b6e-4253-bdcc-b5e6a517e40e)
 Call ID: 73e9966a-8b6e-4253-bdcc-b5e6a517e40e
  Args:
    source: Alfonso_XIII
    target: Alfonso_XII
    relation: :hasFather
  AddTriple (2e54c6ac-a34b-40fc-8950-a8c13d332ac2)
 Call ID: 2e54c6ac-a34b-40fc-8950-a8c13d332ac2
  Args:
    source: Alfonso_XIII
    target: Maria_Christina
    relation: :hasMother
  AddTriple (b3804842-c558-40bf-a43f-761099dd7412)
 Call ID: b3804842-c558-40bf-a43f-761099dd7412
  Args:
    relation: :isBrotherOf
    source: Alfonso_XIII
    target: Mercedes
  AssignClass (72661d94-afff-4031-8bf0-9fa63dab6af6)
 Call ID: 72661d94-afff-4031-8bf0-9fa63dab6af6
  Args:
    source: Maria_Teresa
    type: :Woman
  AssignClass (5ee8f662-a6ea-4374-a5e5-1745c90c2608)
 Call ID: 5ee8f662-a6ea-4374-a5e5-1745c90c2608
  Args:
    source: Maria_Teresa
    type: :Ancestor
  AddTriple (f2fda7bb-82a8-4b47-a4ef-0ef12eefd29f)
 Call ID: f2fda7bb-82a8-4b47-a4ef-0ef12eefd29f
  Args:
    target: Alfonso_XII
    source: Maria_Teresa
    relation: :hasFather
  AddTriple (35de1cc0-cb50-4797-8500-c9383ec3a167)
 Call ID: 35de1cc0-cb50-4797-8500-c9383ec3a167
  Args:
    relation: :hasMother
    source: Maria_Teresa
    target: Maria_Christina
  AddTriple (828fd9e8-efe1-48d2-8b99-f9301b665db1)
 Call ID: 828fd9e8-efe1-48d2-8b99-f9301b665db1
  Args:
    relation: :isSisterOf
    target: Mercedes
    source: Maria_Teresa
  AssignClass (7207df51-097c-46c4-b0a0-7862be94d4d6)
 Call ID: 7207df51-097c-46c4-b0a0-7862be94d4d6
  Args:
    source: Carlos_of_Bourbon_Two_Sicilies
    type: :Man
  AssignClass (f02c9083-e64b-4eb6-830d-25913ae81a67)
 Call ID: f02c9083-e64b-4eb6-830d-25913ae81a67
  Args:
    source: Carlos_of_Bourbon_Two_Sicilies
    type: :Ancestor
  AddLiteral (5cd2c346-bf6e-4a4c-88b8-79c368581a55)
 Call ID: 5cd2c346-bf6e-4a4c-88b8-79c368581a55
  Args:
    source: Mercedes
    literal_value: 1901
    relation: :hasMarriageYear
    literal_type: xsd:integer
  AddTriple (18888377-32b6-4c87-a340-a8cc6581a5a5)
 Call ID: 18888377-32b6-4c87-a340-a8cc6581a5a5
  Args:
    source: Mercedes
    target: Carlos_of_Bourbon_Two_Sicilies
    relation: :hasRelation
  AssignClass (1af68337-1682-4769-b629-0cc336916078)
 Call ID: 1af68337-1682-4769-b629-0cc336916078
  Args:
    source: Alfonso_son_of_Mercedes
    type: :Man
  AssignClass (4f9c78e6-381e-4166-b32f-c078c33294b2)
 Call ID: 4f9c78e6-381e-4166-b32f-c078c33294b2
  Args:
    source: Alfonso_son_of_Mercedes
    type: :Ancestor
  AddTriple (83789604-632a-46ca-a115-626a3606aedb)
 Call ID: 83789604-632a-46ca-a115-626a3606aedb
  Args:
    target: Carlos_of_Bourbon_Two_Sicilies
    source: Alfonso_son_of_Mercedes
    relation: :hasFather
  AddTriple (56c2a04e-30b1-472e-afaa-e827608ef4c8)
 Call ID: 56c2a04e-30b1-472e-afaa-e827608ef4c8
  Args:
    relation: :hasMother
    target: Mercedes
    source: Alfonso_son_of_Mercedes
  AssignClass (f120aa99-5329-4854-8290-1acc754fd83a)
 Call ID: f120aa99-5329-4854-8290-1acc754fd83a
  Args:
    source: Fernando_son_of_Mercedes
    type: :Man
  AssignClass (c6ebcf66-7ed8-43c3-b8d5-514b7152c5ee)
 Call ID: c6ebcf66-7ed8-43c3-b8d5-514b7152c5ee
  Args:
    type: :Ancestor
    source: Fernando_son_of_Mercedes
  AddTriple (8ed30b4f-1bd4-4ab0-b719-2c08ec2d3c76)
 Call ID: 8ed30b4f-1bd4-4ab0-b719-2c08ec2d3c76
  Args:
    target: Carlos_of_Bourbon_Two_Sicilies
    source: Fernando_son_of_Mercedes
    relation: :hasFather
  AddTriple (a9d81efc-6446-41c1-b174-1c0deb8b3ace)
 Call ID: a9d81efc-6446-41c1-b174-1c0deb8b3ace
  Args:
    relation: :hasMother
    target: Mercedes
    source: Fernando_son_of_Mercedes
  AssignClass (94155d62-2a5b-468c-9e19-a20f8a463421)
 Call ID: 94155d62-2a5b-468c-9e19-a20f8a463421
  Args:
    source: Isabella_Alfonsa
    type: :Woman
  AssignClass (efb6e7a8-bed8-4b77-8814-5171cc712f86)
 Call ID: efb6e7a8-bed8-4b77-8814-5171cc712f86
  Args:
    type: :Ancestor
    source: Isabella_Alfonsa
  AddTriple (4a41d458-ffb9-4db1-88d9-a522e52021f1)
 Call ID: 4a41d458-ffb9-4db1-88d9-a522e52021f1
  Args:
    relation: :hasFather
    target: Carlos_of_Bourbon_Two_Sicilies
    source: Isabella_Alfonsa
  AddTriple (43eb0876-279c-4dd3-8879-6312364d77c3)
 Call ID: 43eb0876-279c-4dd3-8879-6312364d77c3
  Args:
    relation: :hasMother
    target: Mercedes
    source: Isabella_Alfonsa
  Finish (0d0df91a-4272-400d-963b-d4194beb2c4b)
 Call ID: 0d0df91a-4272-400d-963b-d4194beb2c4b
  Args: