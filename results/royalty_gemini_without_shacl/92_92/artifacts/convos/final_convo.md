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
Prince Richard, Duke of Gloucester (Richard Alexander Walter George; born 26 August 1944), is a member of the British royal family.
He is the second son of Prince Henry, Duke of Gloucester, and Princess Alice, Duchess of Gloucester, the youngest of the nine grandchildren of George V, nephew of Edward VIII and George VI, and first cousin of Elizabeth II.
He is 32nd in the line of succession to the British throne, and the highest person on the list who is not a descendant of George VI.
Richard practised as an architect until the death of his elder brother, William, placed him in direct line to inherit his father's dukedom of Gloucester, to which he succeeded in 1974.
Early life

Richard was born at 12:15 pm on 26 August 1944 at St Matthew's Nursing Home in Northampton, the second son of Prince Henry, Duke of Gloucester, and Alice, Duchess of Gloucester.
His father was the third son of King George V and Queen Mary.
His mother was the third daughter of John Montagu Douglas Scott, 7th Duke of Buccleuch, and Lady Margaret Bridgeman.
At the time of his birth, he was second in line to his father's dukedom, behind his elder brother, Prince William of Gloucester, who died in an air crash in 1972 before inheriting the title and having any children of his own.
Richard was baptised at the Royal Chapel of All Saints in Windsor Great Park on 20 October by the retired Archbishop of Canterbury, Cosmo Gordon Lang.
His godparents were his paternal aunt Princess Mary, Queen Elizabeth, Princess Marie Louise (his first cousin twice removed), Princess Alice, Countess of Athlone (his grandaunt and first cousin twice removed, for whom her daughter, Lady May Abel Smith stood proxy), the Duke of Buccleuch (his maternal uncle), the Marquess of Cambridge (his cousin), Lady Sybil Phipps (his maternal aunt), and General the Earl Alexander of Tunis (for whom his wife, then Lady Margaret Alexander, stood proxy).
When Richard was four months old, he accompanied his parents to Australia, where his father served as governor-general from 1945 to 1947.
The family returned to Barnwell Manor in 1947, where Richard spent most of his childhood.
Education and career

Richard's early education took place at home, under the instruction of Rosalind Ramirez, who had also tutored young King Faisal II of Iraq; later, he attended Wellesley House School at Broadstairs and Eton College.
In 1966, Richard joined the Offices Development Group in the Ministry of Public Building and Works for a year of practical work.
Marriage and family




On 8 July 1972, Richard married Danish-born Birgitte van Deurs Henriksen at St Andrew's Church, Barnwell, Northamptonshire; the Duke and Duchess of Gloucester have three children:


The Duke and Duchess of Gloucester's official residence is at Kensington Palace in London.
In September 2022, the Duke put the manor up for sale for £4.75 million.
Activities

Richard ended his architectural career in 1972, after the death of his elder brother Prince William, who was killed in an air crash during a flying competition.
Richard became heir apparent to his father's dukedom and had to take on additional family obligations and royal duties on behalf of the Queen.
He became Duke of Gloucester on his father's death on 10 June 1974.
He has been a corporate member of the Royal Institute of British Architects since 1972.
With his background in architecture, the Duke of Gloucester takes interest in the work of the trust and visits their projects, in addition to giving his name to their long standing Duke of Gloucester Young Achiever's Scheme Awards.
The Duke is vice president of Lepra, a UK-based leprosy charity; as part of this role, he attends national and international events in support of the charity's work.
He is royal patron of the Society of Antiquaries of London (and elected FSA) since 2001, royal patron of the UK branch of the charity Habitat for Humanity, royal patron of the St George's Society of New York, and president of The London Society.
A keen motorist, Richard passed the Advanced Driving Test of the Institute of Advanced Motorists, of which he was president for more than 32 years.
The Duke of Gloucester, accompanied by the Duchess, represented his cousin Elizabeth II at the Seychelles independence ceremonies on 26 June 1976 and again at the Solomon Islands independence celebrations on 7 July 1978.
He served as a judge in Prince Edward's charity television special The Grand Knockout Tournament on 15 June 1987.
On 10 April 2008, the Duke of Gloucester was officially installed as inaugural Chancellor of the University of Worcester during a ceremony at Worcester Cathedral.
The Duke carried out the first of these duties on 5 and 6 November 2008 at the Graduation Award Ceremonies.
The Duke is a patron of the Severn Valley Railway and the Pestalozzi International Village Trust.
He shares a name with an earlier Duke of Gloucester, Richard III, and has been patron of the Richard III Society since 1980.
He is a member of the international advisory board of the Royal United Services Institute.
During 2009, the Duke became patron of the de Havilland Aircraft Heritage Centre in support of its bid to raise funds through private means and through a bid for Heritage Lottery Funding.
In July 2011, the Duke visited the Isle of Man to meet with the representative of Manx National Heritage and the Council of Cancer Charities.
On 19 March 2013, the Duke represented Elizabeth II at the Vatican for the inauguration of Pope Francis.
On 11 March 2015, the Duke visited the Royal School Dungannon in County Tyrone to celebrate the 400th anniversary of the founding of the school; presenting a commemorative plaque and raising an anniversary flag on the grounds.
On 22 and 26 March 2015, the Duke represented the Queen at the ceremonies marking the reburial and commemorations of King Richard III in Leicester Cathedral.
Richard III had held the title Duke of Gloucester before his ascension to the English throne.
In March 2018, the Duke travelled to Malawi to attend the Commonwealth Day celebrations, and visited projects related to health services, wildlife, and climate change.
On 14 September 2022, after the death of Queen Elizabeth II on 8 September, the Duke joined her children, grandsons, nephew, and son-in-law, in walking in the state cortege from Buckingham Palace to Westminster Hall, for her lying in state.
In 2023 the Duke and Duchess of Gloucester attended the coronation of King Charles III and Queen Camilla in Westminster Abbey, and (in common with other working members of the royal family) took part in the Coronation Procession following the service.
Titles, styles, honours and arms

Titles and styles

Richard was originally styled "His Royal Highness Prince Richard of Gloucester".
Since becoming duke in 1974, he has been known as "His Royal Highness The Duke of Gloucester".
Honours

letters


Wear of orders, decorations, and medals

The ribbons worn regularly by Richard in undress uniform are as follows:


Honorary military appointments

Non-national titles and honours

Scholastic

Civic

Arms

Issue

Ancestry

See also

References

External links



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
  AssignClass (2bb7fba7-2217-4b9d-afc2-3261d5b531c8)
 Call ID: 2bb7fba7-2217-4b9d-afc2-3261d5b531c8
  Args:
    source: Prince Richard, Duke of Gloucester
    type: :Man
  AddLiteral (4a47d214-6904-45ed-8f71-15299a320ffe)
 Call ID: 4a47d214-6904-45ed-8f71-15299a320ffe
  Args:
    relation: :alsoKnownAs
    literal_type: xsd:string
    source: Prince Richard, Duke of Gloucester
    literal_value: Richard Alexander Walter George
  AddLiteral (a25a46f2-214e-46ea-a687-edd0706859e4)
 Call ID: a25a46f2-214e-46ea-a687-edd0706859e4
  Args:
    relation: :hasBirthYear
    source: Prince Richard, Duke of Gloucester
    literal_type: xsd:integer
    literal_value: 1944
  AssignClass (aacbbea1-6f2e-4408-812d-d21ba68698d6)
 Call ID: aacbbea1-6f2e-4408-812d-d21ba68698d6
  Args:
    type: :Man
    source: Prince Henry, Duke of Gloucester
  AssignClass (1210273f-553f-472f-9dcb-5fd5d457a844)
 Call ID: 1210273f-553f-472f-9dcb-5fd5d457a844
  Args:
    source: Princess Alice, Duchess of Gloucester
    type: :Woman
  AddTriple (b8eb8d72-5545-4db4-89cd-8eca2386f726)
 Call ID: b8eb8d72-5545-4db4-89cd-8eca2386f726
  Args:
    source: Prince Richard, Duke of Gloucester
    relation: :hasFather
    target: Prince Henry, Duke of Gloucester
  AddTriple (90d9eabe-3624-4439-b4e3-ab0bae9196bb)
 Call ID: 90d9eabe-3624-4439-b4e3-ab0bae9196bb
  Args:
    source: Prince Richard, Duke of Gloucester
    target: Princess Alice, Duchess of Gloucester
    relation: :hasMother
  AssignClass (4b4cfbee-9b96-4e66-943c-038583b2c663)
 Call ID: 4b4cfbee-9b96-4e66-943c-038583b2c663
  Args:
    type: :Man
    source: Prince William of Gloucester
  AddTriple (e7227b2c-2b19-4f17-b0d9-0875eb690fee)
 Call ID: e7227b2c-2b19-4f17-b0d9-0875eb690fee
  Args:
    source: Prince Richard, Duke of Gloucester
    relation: :hasBrother
    target: Prince William of Gloucester
  AddTriple (fa21c51c-2955-426b-9d7c-7c3129993f31)
 Call ID: fa21c51c-2955-426b-9d7c-7c3129993f31
  Args:
    target: Prince Richard, Duke of Gloucester
    relation: :isBrotherOf
    source: Prince William of Gloucester
  AddTriple (c2b193b4-e2fd-4e53-bb1c-6e038c1fe766)
 Call ID: c2b193b4-e2fd-4e53-bb1c-6e038c1fe766
  Args:
    source: Prince William of Gloucester
    relation: :hasFather
    target: Prince Henry, Duke of Gloucester
  AddTriple (f807e4e7-6b8f-40ab-b65c-42da8caa4ff8)
 Call ID: f807e4e7-6b8f-40ab-b65c-42da8caa4ff8
  Args:
    source: Prince William of Gloucester
    relation: :hasMother
    target: Princess Alice, Duchess of Gloucester
  AddLiteral (e4dd227f-bd48-4945-98c6-7428352c07e7)
 Call ID: e4dd227f-bd48-4945-98c6-7428352c07e7
  Args:
    source: Prince William of Gloucester
    literal_type: xsd:integer
    literal_value: 1972
    relation: :hasDeathYear
  AssignClass (eedb74d0-7571-4010-99e0-88e5d38c1740)
 Call ID: eedb74d0-7571-4010-99e0-88e5d38c1740
  Args:
    source: Birgitte van Deurs Henriksen
    type: :Woman
  AddTriple (df82dd59-607f-4ff9-9295-c01abec68ff4)
 Call ID: df82dd59-607f-4ff9-9295-c01abec68ff4
  Args:
    source: Prince Richard, Duke of Gloucester
    relation: :hasRelation
    target: Birgitte van Deurs Henriksen
  AddLiteral (a4692d7b-da1e-43cf-90ed-7a229b7e0c5b)
 Call ID: a4692d7b-da1e-43cf-90ed-7a229b7e0c5b
  Args:
    literal_value: 1972
    source: Prince Richard, Duke of Gloucester
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AssignClass (0d7edb88-b704-46fb-ad70-ae667585dec0)
 Call ID: 0d7edb88-b704-46fb-ad70-ae667585dec0
  Args:
    type: :Man
    source: King George V
  AssignClass (863f1e43-96e4-4e21-897e-43830ed4e75f)
 Call ID: 863f1e43-96e4-4e21-897e-43830ed4e75f
  Args:
    type: :Woman
    source: Queen Mary
  AddTriple (332d644c-898f-4c08-9f9a-7c42ae5cda7b)
 Call ID: 332d644c-898f-4c08-9f9a-7c42ae5cda7b
  Args:
    source: Prince Henry, Duke of Gloucester
    relation: :hasFather
    target: King George V
  AddTriple (2c707eeb-af49-4c18-9c21-33d7a4ff141d)
 Call ID: 2c707eeb-af49-4c18-9c21-33d7a4ff141d
  Args:
    target: Queen Mary
    relation: :hasMother
    source: Prince Henry, Duke of Gloucester
  AssignClass (f36a34f4-2869-4f1c-b553-d5f4af1c0c62)
 Call ID: f36a34f4-2869-4f1c-b553-d5f4af1c0c62
  Args:
    type: :Man
    source: John Montagu Douglas Scott, 7th Duke of Buccleuch
  AssignClass (1b98de27-c966-40c6-93dc-a22712c5f57b)
 Call ID: 1b98de27-c966-40c6-93dc-a22712c5f57b
  Args:
    source: Lady Margaret Bridgeman
    type: :Woman
  AddTriple (ec65b194-984c-4292-84d6-128786499f36)
 Call ID: ec65b194-984c-4292-84d6-128786499f36
  Args:
    source: Princess Alice, Duchess of Gloucester
    relation: :hasFather
    target: John Montagu Douglas Scott, 7th Duke of Buccleuch
  AddTriple (74d8ee99-3ab1-44d9-ade4-fde4ebf32e6f)
 Call ID: 74d8ee99-3ab1-44d9-ade4-fde4ebf32e6f
  Args:
    target: Lady Margaret Bridgeman
    relation: :hasMother
    source: Princess Alice, Duchess of Gloucester
  Finish (dfaa0f5e-6554-4aa2-8d4c-9c6a7fcc56c6)
 Call ID: dfaa0f5e-6554-4aa2-8d4c-9c6a7fcc56c6
  Args: