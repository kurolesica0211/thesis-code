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
Prince Claus of the Netherlands, Jonkheer van Amsberg (born Klaus-Georg Wilhelm Otto Friedrich Gerd von Amsberg; 6 September 1926 – 6 October 2002) was Prince of the Netherlands from 30 April 1980 until his death on 6 October 2002, as the husband of Queen Beatrix.
Initially a diplomat in the service of West Germany and West German deputy ambassador to Ivory Coast, Claus met Beatrix on New Year's Eve 1963 and married her in 1966.
When his wife ascended to the throne in 1980, Claus took his place as Prince of the Netherlands, which he held until his death in 2002.
Biography

Klaus-Georg Wilhelm Otto Friedrich Gerd von Amsberg was born on his mother's family's estate, Schloss Dötzingen, Hitzacker, Germany, on 6 September 1926.
He was the second child and only son of Claus Felix von Amsberg and his wife, Baroness Gösta von dem Bussche-Haddenhausen.
His father, by birth a member of House of Amsberg which belonged to the untitled German nobility from Mecklenburg, operated a large farm in Tanganyika (formerly German East Africa) from 1928 until World War II.
His mother belonged to the ancient von dem Bussche noble family which originated from the County of Ravensberg.
From 1938, Claus and his six sisters grew up on their maternal grandmother's estate in Lower Saxony; he attended the Friderico-Francisceum-Gymnasium in Bad Doberan from 1933 to 1936 and a boarding school in Tanganyika from 1936 to 1938.
Claus was a member of such Nazi youth organisations as Deutsches Jungvolk and the Hitler Youth.
In 1944, Claus was conscripted into the German Wehrmacht, becoming a soldier in the German 90th Panzergrenadier Division in Italy in March 1945.
Claus met Princess Beatrix for the first time on New Year's Eve 1963 in Bad Driburg at a dinner hosted by the Count von Oeynhausen-Sierstorpff, who was a distant relative of both of them.
Claus and Beatrix were also distantly related (5th cousins twice removed), as both being descendants from von dem Bussche family.
With memories of German oppression still very strong 20 years after the war, sections of the Dutch population were unhappy that Beatrix's fiancé was a German and former member of the Hitler Youth.
The engagement was approved by the States-General—a necessary step for Beatrix to remain in the line of succession to the throne—in 1965.
They included such memorable slogans as "Claus, 'raus!"
(Claus, get out!)
For a time, it was thought that Beatrix would be the last monarch of the Netherlands.
However, over time, Claus became accepted by the public, so much so that during the last part of his life he was considered by some to be the most popular member of the royal family.
This change in Dutch opinion was brought about by Claus's strong motivation to contribute to public causes (especially Third World development, on which he was considered an expert), his sincere modesty and his candor (within but sometimes on the edge of royal protocol).
The public also sympathised with Claus for his efforts to give meaning to his life beyond the restrictions that Dutch law imposed on the royal family's freedom of speech and action.
However, these restrictions were gradually loosened; Claus was even appointed as senior staff member at the Department of Developing Aid, albeit in an advisory role.
In 1998, after presenting the annual Prince Claus Awards to three African fashion designers, Claus told "workers of all nations to unite and cast away the new shackles they have voluntarily cast upon themselves", meaning the necktie, that "snake around my neck," and encouraged the audience to "venture into open-collar paradise".
Claus battled depression for a number of years, and underwent surgery in 1998 to remove his prostate.
Activities

As a husband of the heir, Claus was a member of the National Advisory Council for Development Cooperation and its Bureau, and was a chair of the National Committee for Development Strategy 1970‐1980 and the Netherlands Development Organization.
On 30 April 1980, Claus' mother-in-law, Queen Juliana, abdicated in favour of Princess Beatrix, who became Queen of the Netherlands.
After the investiture, the couple visited the Netherlands Antilles and Aruba.
As a prince consort, Prince Claus frequently visited public organisations, commercial and industrial enterprises, and companies in the agriculture and fisheries sector.
In 1984, Claus became the Inspector General for Development Cooperation, member of the Board of Directors of De Nederlandsche Bank N.V. (until 1998), member of the Board of Directors of Royal PTT Nederland, and Chair of the Transport and Public Works Platform.
Claus was an honorary chair of the National Coordinating Committee for the Protection of Monuments and Historic Buildings and the King William I Foundation.
He was also a patron of the Concertgebouw Orchestra and Scouting Netherlands.
On Claus' seventieth birthday, the Prince Claus Fund for Culture and Development was established on the initiative of the Dutch government.
Declining health and death

Claus suffered various health problems, such as depression, cancer and Parkinson's disease.
Claus is interred in the royal family's tomb in Delft on 15 October.
Titles, styles, honours, and arms

Titles

Honours

National

Foreign

Academic awards

Prince Claus was also appointed Honorary Fellow of the International Institute of Social Studies (ISS) in 1988.
Prince Claus was a prominent member of the international development cooperation community.
Ancestry

Issue

References

External links

2 gave up the title "Prince of the Netherlands, but still held the title "Prince of Orange-Nassau"
3 title granted by Royal Decree to descendants of Princess Irene



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
  AssignClass (f01745a7-6a5b-4476-94c3-971adfee6bf4)
 Call ID: f01745a7-6a5b-4476-94c3-971adfee6bf4
  Args:
    source: Prince_Claus_of_the_Netherlands
    type: :Man
  AssignClass (458013ff-c88c-4cfc-b109-eed2fcc128ec)
 Call ID: 458013ff-c88c-4cfc-b109-eed2fcc128ec
  Args:
    type: :Woman
    source: Queen_Beatrix
  AssignClass (bbda2622-e08a-4497-b13f-af0cbc17531a)
 Call ID: bbda2622-e08a-4497-b13f-af0cbc17531a
  Args:
    type: :Man
    source: Claus_Felix_von_Amsberg
  AssignClass (9c21f767-4a67-4620-a93c-e51423c6b6b8)
 Call ID: 9c21f767-4a67-4620-a93c-e51423c6b6b8
  Args:
    type: :Woman
    source: Baroness_Gosta_von_dem_Bussche-Haddenhausen
  AssignClass (520e7500-bd4c-4e1a-9daf-9267a2b8b3d0)
 Call ID: 520e7500-bd4c-4e1a-9daf-9267a2b8b3d0
  Args:
    type: :Woman
    source: Queen_Juliana
  AddLiteral (afd04b57-f66b-493a-8cdd-5bc9d171ceb1)
 Call ID: afd04b57-f66b-493a-8cdd-5bc9d171ceb1
  Args:
    relation: :hasBirthYear
    literal_value: 1926
    source: Prince_Claus_of_the_Netherlands
    literal_type: xsd:integer
  AddLiteral (4a4a6495-0484-4caa-bb96-e19dc34cfb6c)
 Call ID: 4a4a6495-0484-4caa-bb96-e19dc34cfb6c
  Args:
    literal_value: 2002
    relation: :hasDeathYear
    source: Prince_Claus_of_the_Netherlands
    literal_type: xsd:integer
  AddTriple (ed598246-e73e-40e3-b3d4-447686502eaf)
 Call ID: ed598246-e73e-40e3-b3d4-447686502eaf
  Args:
    target: Claus_Felix_von_Amsberg
    relation: :hasFather
    source: Prince_Claus_of_the_Netherlands
  AddTriple (f6d6f7a1-4bb0-41cf-8d7f-ea563d413432)
 Call ID: f6d6f7a1-4bb0-41cf-8d7f-ea563d413432
  Args:
    target: Baroness_Gosta_von_dem_Bussche-Haddenhausen
    relation: :hasMother
    source: Prince_Claus_of_the_Netherlands
  AddTriple (fdcc7b1d-128a-4d3d-a6bc-9ae673237074)
 Call ID: fdcc7b1d-128a-4d3d-a6bc-9ae673237074
  Args:
    source: Queen_Beatrix
    relation: :hasMother
    target: Queen_Juliana
  AddLiteral (04ee963a-b3a6-46e4-9c7d-f87107d7c5c2)
 Call ID: 04ee963a-b3a6-46e4-9c7d-f87107d7c5c2
  Args:
    source: Prince_Claus_of_the_Netherlands
    literal_value: 1966
    relation: :hasMarriageYear
    literal_type: xsd:integer
  AddTriple (1ce56487-6a83-41d1-ad8b-7b61eba069a8)
 Call ID: 1ce56487-6a83-41d1-ad8b-7b61eba069a8
  Args:
    relation: :hasRelation
    target: Queen_Beatrix
    source: Prince_Claus_of_the_Netherlands
  Finish (d5f898d0-c3da-4803-9341-d39a0efe432e)
 Call ID: d5f898d0-c3da-4803-9341-d39a0efe432e
  Args: