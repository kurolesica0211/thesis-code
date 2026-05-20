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
Princess Nina Georgievna of Russia (Russian: Нина Георгиевна) (20 June 1901 – 27 February 1974), was the elder daughter of Grand Duke George Mikhailovich and Grand Duchess Maria Georgievna of Russia.
A great-granddaughter of Tsar Nicholas I of Russia, she left her native country in 1914, before World War I, finished her education in England, and spent the rest of her life in exile.
In London in 1922, she married Prince Paul Chavchavadze, a descendant of the last king of Georgia.
They had one child, Prince David Chavchavadze, born there two years later.
Princess Nina was an artist, her husband worked as an author; he wrote five books and translated several others.
Their son, Prince David Chavchavadze, served with the U.S. Army during World War II and, thanks in part to his knowledge of Russian, eventually became a CIA officer.
After his retirement, he wrote his memoirs and published those of his grandmother, Grand Duchess George, as well as a book about the grand dukes of Russia.
Early life

Princess Nina was born on June 20  1901 in the New Mikhailovsky Palace on the Palace Embankment in Saint Petersburg, the residence of her paternal grandfather, Grand Duke Michael Nicolaievich of Russia.
She was the elder daughter of Grand Duke George Mikhailovich and Grand Duchess Maria Georgievna of Russia.
Through her father, she was a member of the Romanov family, and princess of the Imperial blood as a great-granddaughter of Tsar Nicholas I of Russia.
Nina's mother was a princess of Greece and Denmark, and on her maternal side, Nina was a granddaughter of King George I of Greece, great-granddaughter of King Christian IX of Denmark and related to members of many European royal families.
Princess Nina spent the first years of her life in the family's apartments at the New Mikhailovsky Palace.
A contemporary of Tsar Nicholas II two youngest daughters, Princess Nina and her only sibling Princess Xenia, played sometimes with them, while they were in the Imperial capital.
The marriage of Nina's parents was unhappy.
Grand Duke George was a devoted father, and the two sisters were close to him, but Grand Duchess Maria Georgievna never liked Russia and eventually became estranged from her husband.
When the war broke out a month after her arrival, the Grand Duchess did not rush back to Russia and later it was too dangerous to attempt a return.
Princess Nina and her sister never saw their father again.
During the turbulent years of World War I and the Russian Revolution, Princess Nina remained living safely in London with her mother and her sister.
Marriage

Princess Nina married Prince Paul Alexandrovich Chavchavadze (1899–1971) on 3 September 1922 in London.
Paul descended from the House of Chavchavadze of the Kakheti province in Georgia, and also, in a direct line, from the last King of Georgia, George XII.
By the time they were married, the world they knew had changed radically, with the collapse of the feudal system in Russia, the rise of the Bolsheviks, and annexation of Georgia by the Soviet Union.
Prince Paul, who also lost his father at the hands of the Bolsheviks, served in the military service on two continents.
The couple had an only child, Prince David Chavchavadze, born in 1924 in London.
In 1927, Princess Nina moved with her family to the United States, where they settled in New York.
Princess Nina was an artist, her husband worked as an author; he wrote five books and translated several others.
Their son, Prince David Chavchavadze, thanks in part to his knowledge of Russian, eventually became a CIA officer.
After his retirement, he wrote a book about the Grand Dukes of Russia.
Princess Nina's husband died in 1971, she outlived him for only a couple of years.



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
  AssignClass (68f7ca58-5186-4301-b85a-0d4e70902a01)
 Call ID: 68f7ca58-5186-4301-b85a-0d4e70902a01
  Args:
    type: :Woman
    source: Nina_Georgievna
  AssignClass (52c3a27f-bc8b-471b-803d-38f2ae5bcc09)
 Call ID: 52c3a27f-bc8b-471b-803d-38f2ae5bcc09
  Args:
    source: George_Mikhailovich
    type: :Man
  AssignClass (f75bad56-f13e-4c46-83d3-485c81acab7b)
 Call ID: f75bad56-f13e-4c46-83d3-485c81acab7b
  Args:
    source: Maria_Georgievna
    type: :Woman
  AssignClass (cc17fcf5-303b-42b9-a80b-2b69b71d0ef9)
 Call ID: cc17fcf5-303b-42b9-a80b-2b69b71d0ef9
  Args:
    type: :Man
    source: Paul_Chavchavadze
  AssignClass (6bd7b2cf-dd10-4c50-8086-0e73b92f7c6f)
 Call ID: 6bd7b2cf-dd10-4c50-8086-0e73b92f7c6f
  Args:
    source: David_Chavchavadze
    type: :Man
  AssignClass (3c580f0f-2d3b-4755-be82-610ca4841564)
 Call ID: 3c580f0f-2d3b-4755-be82-610ca4841564
  Args:
    type: :Woman
    source: Xenia
  AddLiteral (63600852-c8ac-41c8-b3f3-526672bda68b)
 Call ID: 63600852-c8ac-41c8-b3f3-526672bda68b
  Args:
    literal_value: 1901
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Nina_Georgievna
  AddLiteral (14678f39-2081-4d43-93bf-168e55461ee3)
 Call ID: 14678f39-2081-4d43-93bf-168e55461ee3
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: Nina_Georgievna
    literal_value: 1974
  AddTriple (e87a7d65-60e8-449a-876c-2c49b1cd1617)
 Call ID: e87a7d65-60e8-449a-876c-2c49b1cd1617
  Args:
    source: Nina_Georgievna
    relation: :hasFather
    target: George_Mikhailovich
  AddTriple (d4f4f554-f4a2-4ef2-b02e-bcbeddcd2f2f)
 Call ID: d4f4f554-f4a2-4ef2-b02e-bcbeddcd2f2f
  Args:
    target: Maria_Georgievna
    relation: :hasMother
    source: Nina_Georgievna
  AddTriple (12ca1d94-0a2b-4405-bcca-03b0bf49ff4a)
 Call ID: 12ca1d94-0a2b-4405-bcca-03b0bf49ff4a
  Args:
    target: Xenia
    source: Nina_Georgievna
    relation: :hasSister
  AddTriple (ee851fd9-6de1-47d4-86f1-b58d04863719)
 Call ID: ee851fd9-6de1-47d4-86f1-b58d04863719
  Args:
    target: Nina_Georgievna
    source: Xenia
    relation: :hasSister
  AddTriple (0a8c9484-49ea-466d-8417-a643adc1eeac)
 Call ID: 0a8c9484-49ea-466d-8417-a643adc1eeac
  Args:
    target: George_Mikhailovich
    relation: :hasFather
    source: Xenia
  AddTriple (7283885d-719d-4f51-989c-75eba5c1fffd)
 Call ID: 7283885d-719d-4f51-989c-75eba5c1fffd
  Args:
    source: Xenia
    relation: :hasMother
    target: Maria_Georgievna
  AddLiteral (c1be8315-7bb5-4bdf-8348-bebdf0036cca)
 Call ID: c1be8315-7bb5-4bdf-8348-bebdf0036cca
  Args:
    literal_value: 1922
    literal_type: xsd:integer
    relation: :hasMarriageYear
    source: Nina_Georgievna
  AddTriple (1a997c37-65c6-439f-ac65-1d0880046c8b)
 Call ID: 1a997c37-65c6-439f-ac65-1d0880046c8b
  Args:
    relation: :hasRelation
    source: Nina_Georgievna
    target: Paul_Chavchavadze
  AddLiteral (3ab57591-c474-4758-844b-074b971e6c7f)
 Call ID: 3ab57591-c474-4758-844b-074b971e6c7f
  Args:
    literal_value: 1899
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Paul_Chavchavadze
  AddLiteral (84f23c2c-aafc-404c-9032-8d9b700dff2b)
 Call ID: 84f23c2c-aafc-404c-9032-8d9b700dff2b
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: Paul_Chavchavadze
    literal_value: 1971
  AddTriple (f63ab184-1bd9-46c3-a3a7-12cd2c127ab5)
 Call ID: f63ab184-1bd9-46c3-a3a7-12cd2c127ab5
  Args:
    source: David_Chavchavadze
    relation: :hasFather
    target: Paul_Chavchavadze
  AddTriple (dab1d682-4ee8-4643-9346-8c90843f3e8e)
 Call ID: dab1d682-4ee8-4643-9346-8c90843f3e8e
  Args:
    target: Nina_Georgievna
    source: David_Chavchavadze
    relation: :hasMother
  AddLiteral (c0b6be1c-a782-4b27-9e63-37a2f3ca2a2c)
 Call ID: c0b6be1c-a782-4b27-9e63-37a2f3ca2a2c
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: David_Chavchavadze
    literal_value: 1924
  Finish (45cadb82-cc7a-4c10-9aa8-eda6a2330128)
 Call ID: 45cadb82-cc7a-4c10-9aa8-eda6a2330128
  Args: