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
The Custodian of the Crown  Prince Radu


Princess Elena 
Princess Irina 
Princess Sophie 
Princess Maria 


Princess Maria of Romania (born 13 July 1964) is the fifth and youngest daughter of King Michael I and Queen Anne of Romania.
Since 2015 Maria has lived in Romania and carried out a public role on behalf of the Romanian royal family.
Early life

Maria was born on 13 July 1964 at Copenhagen University Hospital Gentofte in Gentofte, Copenhagen, Denmark as the youngest of five daughters of King Michael I and Queen Anne.
Maria was born while her father was in the United States on business for the New York Stock Exchange.
Michael was informed by telephone that he'd become a father for the fifth time.
Maria was baptised by the Orthodox Church, with her eldest sister, Princess Margareta, as godmother.
Queen Marie, her paternal great-grandmother, was her namesake.
As a young girl, Maria and her sisters were told "fascinating tales of a homeland they couldn't visit" by their father.
Maria was educated at public school Rydal Penrhos (then Penrhos College) and in Switzerland where the family lived during exile, and spent most her early adult life living and working in the United States, including New York and New Mexico.
Careers

Maria's teenage years were spent in Switzerland with her family, where she received her primary and secondary education.
After completing her studies, Maria worked briefly in the childcare field.
After Maria's brief career in childcare, she pursued a career in New York, doing public relations for private companies.
When the situation in Romania eventually calmed down she left her public relations career and moved to New Mexico where she worked in private consulting until she moved to Romania in 2015.
Activities in Romania

Maria visited Romania with her parents and other members of the family in 1997, and from this point onwards began visiting the country regularly for Christmas or family events such as her parents' 60th Wedding Anniversary and King Michael's 90th Birthday celebrations.
On 7 May 2014, Maria was invested with the Grand Cross of the Order of the Crown in a ceremony conducted by Crown Princess Margareta at the Elisabeta Palace to mark Maria's upcoming 50th birthday.
This was followed by a dinner at the Palace attended by the Prime Minister of Romania (Victor Ponta) and other guests.
On 21 April 2015 it was announced by the Romanian cosmetic company Farmec that Maria is an official ambassador of the company, where she will participate in projects to promote products created in the research lab of the company, as well as social responsibility activities undertaken by Farmec.
In January 2015 it was announced that Maria would move to Romania permanently to take on activities in support of the royal family, and she was present in the public commemorations in Bucharest of 25 years since the royal family's return later the same month.
Maria has represented the royal family at events across the country, acted in support of Margareta, Custodian of the Crown and taken on a number of patronages including Concordia Humanitarian Organisation.
During her father's illnesses, Maria and her elder sisters took turns to be with him at his home in Switzerland and it was during her stay that King Michael died.
Marriage and divorce

On 16 September 1995, Maria married Kazimierz Wiesław Mystkowski (b. 13 September 1958 in Łaś-Toczyłowo), a Polish nobleman from the Mystkowski family and a computer engineer.
The wedding celebration was held at the Greek Orthodox Holy Trinity Cathedral in New York, and was attended by the Romanian royal family, the parents of Kazimierz, the newly married Crown Prince and Crown Princess of Greece.
King Michael I served as the couple's koumbaros (the best man who, during a Greek Orthodox wedding, exchanges the crowns over the couple’s heads).
In December 2003, the couple subsequently divorced without producing any children.


Legal issues

In July 2005, the princess was sued by her landlord, Donald Yates.
During this court case, her name was given as "Mia Mystkowski."
The next legal dispute in which the princess became entangled involved her HOA, the Sierra Madre Homeowners Association.
On 5 December 2008, the homeowner's association filed a general civil complaint against "Marie de Roumanie"; this was followed the next day by a civil summons being issued to the princess.
On 12 January 2009, Princess Maria of Romania was booked in Santa Fe County, New Mexico, on the charge of "failure to appear."
The princess was released the same day on a $200.00 bond.



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
  AssignClass (f6260e92-8a7c-4312-8ef0-8fa110b5a108)
 Call ID: f6260e92-8a7c-4312-8ef0-8fa110b5a108
  Args:
    type: :Woman
    source: Princess_Maria_of_Romania
  AssignClass (be2d00ec-6118-406a-871f-198c4b6c41f4)
 Call ID: be2d00ec-6118-406a-871f-198c4b6c41f4
  Args:
    source: Princess_Maria_of_Romania
    type: :Person
  AssignClass (6ba85af9-8f4d-4385-b2dc-da0c4331ef25)
 Call ID: 6ba85af9-8f4d-4385-b2dc-da0c4331ef25
  Args:
    type: :Man
    source: King_Michael_I
  AssignClass (5863d933-5cd3-415a-b3f8-68a42d556120)
 Call ID: 5863d933-5cd3-415a-b3f8-68a42d556120
  Args:
    type: :Ancestor
    source: King_Michael_I
  AssignClass (47937a2b-26a1-4b6a-8748-e1300b348345)
 Call ID: 47937a2b-26a1-4b6a-8748-e1300b348345
  Args:
    source: King_Michael_I
    type: :Person
  AssignClass (e4b21b33-d112-43fd-9798-5a41ed261310)
 Call ID: e4b21b33-d112-43fd-9798-5a41ed261310
  Args:
    type: :Woman
    source: Queen_Anne_of_Romania
  AssignClass (3aa50de2-7ef6-40d5-86eb-e772cde2b631)
 Call ID: 3aa50de2-7ef6-40d5-86eb-e772cde2b631
  Args:
    source: Queen_Anne_of_Romania
    type: :Ancestor
  AssignClass (419e7588-0c69-40a8-8fc0-a825f2674ec3)
 Call ID: 419e7588-0c69-40a8-8fc0-a825f2674ec3
  Args:
    source: Queen_Anne_of_Romania
    type: :Person
  AssignClass (68e732ff-eea5-4b96-8da1-2e435570428f)
 Call ID: 68e732ff-eea5-4b96-8da1-2e435570428f
  Args:
    type: :Woman
    source: Princess_Margareta
  AssignClass (887cb1dc-1c4b-439d-9ab4-ea14859a7a2c)
 Call ID: 887cb1dc-1c4b-439d-9ab4-ea14859a7a2c
  Args:
    source: Princess_Margareta
    type: :Person
  AssignClass (aaffad13-50cf-4caa-a565-b24720c3bab1)
 Call ID: aaffad13-50cf-4caa-a565-b24720c3bab1
  Args:
    type: :Woman
    source: Princess_Elena
  AssignClass (70c320a5-8c49-4638-9927-636f0035221d)
 Call ID: 70c320a5-8c49-4638-9927-636f0035221d
  Args:
    type: :Person
    source: Princess_Elena
  AssignClass (f4de91ba-a42e-466e-aac2-99a2f2146dc0)
 Call ID: f4de91ba-a42e-466e-aac2-99a2f2146dc0
  Args:
    source: Princess_Irina
    type: :Woman
  AssignClass (c8e8f65c-8cb9-4abf-a1ec-e43632065dff)
 Call ID: c8e8f65c-8cb9-4abf-a1ec-e43632065dff
  Args:
    source: Princess_Irina
    type: :Person
  AssignClass (c322400b-bfd8-40d9-9c35-794fe8dfb9db)
 Call ID: c322400b-bfd8-40d9-9c35-794fe8dfb9db
  Args:
    type: :Woman
    source: Princess_Sophie
  AssignClass (c5e32424-dbaa-4fbb-95ad-a3cdecde36a1)
 Call ID: c5e32424-dbaa-4fbb-95ad-a3cdecde36a1
  Args:
    type: :Person
    source: Princess_Sophie
  AssignClass (edd1f97c-62df-4cb2-a268-939323115135)
 Call ID: edd1f97c-62df-4cb2-a268-939323115135
  Args:
    source: Kazimierz_Wiesław_Mystkowski
    type: :Man
  AssignClass (f726e25d-59ef-44af-84e2-fb9fdbbba38d)
 Call ID: f726e25d-59ef-44af-84e2-fb9fdbbba38d
  Args:
    type: :Person
    source: Kazimierz_Wiesław_Mystkowski
  AddTriple (e9c9ee60-26af-4bb9-b010-fa0a68c670eb)
 Call ID: e9c9ee60-26af-4bb9-b010-fa0a68c670eb
  Args:
    source: Princess_Maria_of_Romania
    relation: :isChildOf
    target: King_Michael_I
  AddTriple (84457890-dd0a-43ce-bf9b-a9e27b77a9c0)
 Call ID: 84457890-dd0a-43ce-bf9b-a9e27b77a9c0
  Args:
    source: Princess_Maria_of_Romania
    relation: :isChildOf
    target: Queen_Anne_of_Romania
  AddLiteral (303e13e6-bf1d-4e95-84db-14d7d0507d22)
 Call ID: 303e13e6-bf1d-4e95-84db-14d7d0507d22
  Args:
    literal_type: xsd:integer
    source: Princess_Maria_of_Romania
    literal_value: 1964
    relation: :hasBirthYear
  AddLiteral (e7d6f0ed-eb29-4ddf-a4a9-3bfa573d69f0)
 Call ID: e7d6f0ed-eb29-4ddf-a4a9-3bfa573d69f0
  Args:
    literal_value: Mia Mystkowski
    source: Princess_Maria_of_Romania
    relation: :alsoKnownAs
    literal_type: xsd:string
  AddLiteral (b1a27f98-efdf-4a42-a799-7de25bdf9e28)
 Call ID: b1a27f98-efdf-4a42-a799-7de25bdf9e28
  Args:
    literal_type: xsd:string
    relation: :alsoKnownAs
    literal_value: Marie de Roumanie
    source: Princess_Maria_of_Romania
  AddTriple (50805258-61b5-478b-bfe1-ca6f06eee8d3)
 Call ID: 50805258-61b5-478b-bfe1-ca6f06eee8d3
  Args:
    source: Princess_Maria_of_Romania
    relation: :isSisterOf
    target: Princess_Margareta
  AddTriple (fd2c8cc4-d889-469a-8033-93c8008c2041)
 Call ID: fd2c8cc4-d889-469a-8033-93c8008c2041
  Args:
    source: Princess_Maria_of_Romania
    relation: :isSisterOf
    target: Princess_Elena
  AddTriple (216ab609-3d8a-494e-bf1d-27daed5e1748)
 Call ID: 216ab609-3d8a-494e-bf1d-27daed5e1748
  Args:
    target: Princess_Irina
    relation: :isSisterOf
    source: Princess_Maria_of_Romania
  AddTriple (7b0ccafc-5d7a-405c-b727-43ef5db6b623)
 Call ID: 7b0ccafc-5d7a-405c-b727-43ef5db6b623
  Args:
    relation: :isSisterOf
    source: Princess_Maria_of_Romania
    target: Princess_Sophie
  AddLiteral (0783d37c-43c8-4a7b-bf21-2d7fee0c5ade)
 Call ID: 0783d37c-43c8-4a7b-bf21-2d7fee0c5ade
  Args:
    literal_type: xsd:integer
    source: Princess_Maria_of_Romania
    literal_value: 1995
    relation: :hasMarriageYear
  AddTriple (a1dd5586-2700-4957-9eaa-03dd9bee5b16)
 Call ID: a1dd5586-2700-4957-9eaa-03dd9bee5b16
  Args:
    target: Kazimierz_Wiesław_Mystkowski
    source: Princess_Maria_of_Romania
    relation: :hasRelation
  AddLiteral (ca91b921-d73b-4cde-803f-5c5297859fac)
 Call ID: ca91b921-d73b-4cde-803f-5c5297859fac
  Args:
    literal_type: xsd:integer
    literal_value: 1958
    source: Kazimierz_Wiesław_Mystkowski
    relation: :hasBirthYear
  Finish (0c55121b-f57b-4bd5-8f11-da85c130fe4c)
 Call ID: 0c55121b-f57b-4bd5-8f11-da85c130fe4c
  Args: