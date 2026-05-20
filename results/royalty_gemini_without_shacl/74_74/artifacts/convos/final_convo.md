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
Prince George, Duke of Kent (George Edward Alexander Edmund; 20 December 1902 – 25 August 1942), was a member of the British royal family, the fourth son of King George V and Queen Mary, and a younger brother of Kings Edward VIII and George VI.
He served in the Royal Navy during the 1920s before briefly working as a civil servant, and in 1934 was created Duke of Kent.
That same year he married Princess Marina of Greece and Denmark, with whom he had three children:
Edward, Alexandra and Michael.
George was killed in an air crash in Scotland in 1942, aged 39, becoming the first member of the royal family in more than four centuries to die on active service.
Early life

George was born at 7:35 pm on 20 December 1902 at York Cottage on the Sandringham Estate in Norfolk, England.
His father was the Prince of Wales (later King George V), the only surviving son of King Edward VII and Queen Alexandra.
His mother was the Princess of Wales, later Queen Mary, the eldest child and only daughter of the Duke and Duchess of Teck.
Edward, Albert, and Henry.
He was baptised in the Private Chapel at Windsor Castle on 26 January 1903 by Francis Paget, the  Bishop of Oxford.
His godparents were King Edward VII (his paternal grandfather); Prince Valdemar of Denmark (his paternal granduncle, represented by Prince Carl of Denmark, his paternal uncle and first cousin once removed); Prince Louis of Battenberg (husband of his father's cousin); Queen Alexandra (his paternal grandmother); Empress Dowager Maria Feodorovna (his paternal grandaunt, represented by Princess Victoria of the United Kingdom, his paternal aunt); and Princess Christian of Schleswig-Holstein (his paternal grandaunt).
Education and career

George received his early education from a tutor and later followed his elder brother, Henry, to St Peter's Court, a preparatory school at Broadstairs, Kent.
At the age of 13, like his elder brothers – the Prince of Wales (later Edward VIII) and Albert, (later George VI) – he entered naval college, first at Osborne and subsequently at Dartmouth.
He remained on active service in the Royal Navy until March 1929, serving on HMS Iron Duke and later on the flagship of the Atlantic Fleet (renamed the Home Fleet in 1932), HMS Nelson.
He served on the latter as a lieutenant on the admiral's staff before transferring in 1928 to HMS Durban on the America and West Indies Station, based at the Royal Naval Dockyard in Bermuda.
After leaving the navy, he briefly held posts at the Foreign Office and later the Home Office, becoming the first member of the royal family to work as a civil servant.
From January to April 1931, George and his elder brother, the Prince of Wales, undertook an 18,000‐mile tour of South America.
The princes travelled back via Paris and an Imperial Airways flight from Paris–Le Bourget Airport that landed specially in Windsor Great Park.
On 23 June 1936, George was appointed a personal aide-de-camp to his eldest brother, the new king, Edward VIII.
Following Edward's abdication, he was appointed a personal naval aide-de-camp to his elder brother, now George VI.
On 12 March 1937, he was commissioned as a colonel in the British Army and as a group captain in the Royal Air Force (RAF).
He was also appointed Colonel-in-Chief of the Royal Fusiliers from the same date.
In October 1938, George was appointed Governor-General of Australia in succession to Lord Gowrie, with effect from November 1939.
On 8 June 1939, he was promoted to rear admiral in the Royal Navy, major-general in the British Army, and air vice-marshal in the Royal Air Force.
Personal life

Marriage and children

On 9 October 1934, in anticipation of his forthcoming marriage to his second cousin, Princess Marina of Greece and Denmark, he was created Duke of Kent, Earl of St Andrews, and Baron Downpatrick.
They had three children:


Relationships

George was rumoured to have had affairs with the musical star Jessie Matthews, the writer Cecil Roberts, and Noël Coward, a suggestion which Coward's long-term partner, Graham Payn, denied.
His first significant relationship was with Gladys Jean Combe, younger daughter of Captain Christian Combe of the Royal Horse Guards and Lady Jane Combe, daughter of George Conyngham, 3rd Marquess Conyngham.
George met her while serving as a sub-lieutenant on HMS Mackay during one of his trips ashore.
George was also linked to a ménage à trois involving Preston and José Uriburu, the bisexual son of the Argentine ambassador to the United Kingdom, José Uriburu Tezanos.
According to the memoirs of Loelia, Duchess of Westminster, George's brother Edward VIII believed that the child was Michael Temple Canfield (1926–1969), the adopted son of the American publisher Cass Canfield and the first husband of Lee Radziwill, sister of Jacqueline Kennedy Onassis.
After being sent by the King to the Far East, George began a relationship in Singapore in 1926 with Leila Devitt, a hostess and wife of a commodities magnate who was 10 years his senior.
He was also associated with several other women during his life, including Poppy Baring (whom the King and Queen considered unsuitable as a royal bride), Lois Sturt, Paula Gellibrand, Audrey Coats, Edythe d'Erlanger, Myrtle Farquharson, Florence Mills, and Adelaide Hall.
In an article published in June of 2024, the Daily Telegraph provided a list of the Duke's known and suspected romantic partners, while casting doubt on others who have been widely named.
The article directly called into question the factual accuracy of some elements of the article about the Duke in the English language Wikipedia at that time, specifically relating to his private life and romantic relationships.
RAF career

As a young man, George became convinced that the future lay in aviation.
He was the first member of the royal family to cross the Atlantic Ocean by air.
Before his flying career, he had entered the Royal Navy and received intelligence training while stationed at Rosyth.
In March 1937, he was granted a commission in the Royal Air Force as a group captain.
He was appointed Honorary Air Commodore of No. 500 (County of Kent) Squadron, Auxiliary Air Force, in August 1938.
He was promoted to air vice-marshal in June 1939, alongside corresponding promotions to flag and general officer rank in the Royal Navy and British Army.
In 1939 he returned to active service as a rear admiral in the Royal Navy, but in April 1940 transferred to the Royal Air Force.
Freemasonry

George was initiated into freemasonry on 12 April 1928 in Navy Lodge No. 2612.
He served as master of Navy Lodge in 1931, and was also a member of Prince of Wales's Lodge No. 259 and Royal Alpha Lodge No. 16, of which he became master in 1940.
Death

On 25 August 1942, George and 14 others took off in RAF Short Sunderland flying boat W4026 from Invergordon, Ross and Cromarty, for a non‐operational flight to Iceland.
George and all but one of those on board were killed.
His death in RAF service marked the first time in more than 450 years that a member of the royal family had died on active service.
George's body was interred initially in the Royal Vault of St George's Chapel, Windsor; in 1968 he was reburied in the Royal Burial Ground, Frogmore, directly behind Queen Victoria's mausoleum.
His elder son, six-year-old Edward, succeeded him as Duke of Kent.
Marina, his wife, had given birth to their third child, Michael, only seven weeks before George's death.
One RAF crew member survived the crash: Flight Sergeant Andrew Jack, the Sunderland's rear gunner.
Jack's niece has claimed that he told his brother that George had been at the controls of the aircraft, that Jack had dragged him from the pilot's seat after the crash, and that there was an additional person on board whose identity has never been revealed.
In popular culture

George's early life is dramatised in Stephen Poliakoff's television serial The Lost Prince (2003), a biography of his younger brother John.
In the production, the teenage Prince 'Georgie' is portrayed as sensitive, intelligent, artistic, and unusually sympathetic to John's difficulties.
He is shown as detesting his time at the Royal Naval College and as having a strained relationship with his austere father.
In May 2008, the BBC aired the Radio 4 comedy Hut 33, Series 2, Episode 1, titled "The Royal Visit".
The main guest character in the episode is the Duke of Kent, played by Michael Fenton-Stevens.
Set at Bletchley Park, the programme depicts a team of codebreakers instructed to conceal the nature of their work during an impromptu royal visit.
Within the episode's comic narrative, the Duke is described as a Nazi spy and is portrayed as promiscuous and bisexual, attempting to obtain sexual favours from a male member of staff, while a female character recalls a previous liaison with him.
Much of George's later life was outlined in the documentary film The Queen's Lost Uncle.
George and his eldest brother, the Prince of Wales (later Edward VIII), appear in Poliakoff's BBC serial Dancing on the Edge (2013), in which they are shown as supporters of jazz and encouragers of Louis Lester's Jazz Band.
A sexual attraction to Lester on George's part is also suggested.
Honours and arms

letters


Appointments

Military

Civic

Arms

Around the time of his elder brother Prince Henry's twenty-first birthday, Prince George was granted the use of the Royal Arms, differenced by a label argent of three points, each bearing an anchor azure.



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
  AssignClass (aabe64b5-6019-474b-8825-cf667c18473c)
 Call ID: aabe64b5-6019-474b-8825-cf667c18473c
  Args:
    source: George_Duke_of_Kent
    type: :Man
  AssignClass (fbdb6432-27f8-46a8-8cb6-1e1f480dbe23)
 Call ID: fbdb6432-27f8-46a8-8cb6-1e1f480dbe23
  Args:
    type: :Man
    source: George_V
  AssignClass (998ac072-ca80-43ed-a8ba-76775b8fefcf)
 Call ID: 998ac072-ca80-43ed-a8ba-76775b8fefcf
  Args:
    source: Queen_Mary
    type: :Woman
  AssignClass (d775ddbc-6f9b-46c4-b949-b18519ed677f)
 Call ID: d775ddbc-6f9b-46c4-b949-b18519ed677f
  Args:
    type: :Man
    source: Edward_VIII
  AssignClass (6db19eb9-1f7b-4049-b4fe-716a5dc5f616)
 Call ID: 6db19eb9-1f7b-4049-b4fe-716a5dc5f616
  Args:
    type: :Man
    source: George_VI
  AssignClass (4fb4bc83-0046-48ec-ab43-e6419762e99d)
 Call ID: 4fb4bc83-0046-48ec-ab43-e6419762e99d
  Args:
    source: Princess_Marina
    type: :Woman
  AssignClass (69bb2af4-a402-4fec-830e-161573c161aa)
 Call ID: 69bb2af4-a402-4fec-830e-161573c161aa
  Args:
    type: :Man
    source: Edward_Duke_of_Kent
  AssignClass (fd05099b-c822-4a4f-8906-dc61b7ccb4fe)
 Call ID: fd05099b-c822-4a4f-8906-dc61b7ccb4fe
  Args:
    type: :Woman
    source: Alexandra_of_Kent
  AssignClass (c1274a83-7133-40e0-9dc6-f4f423a0345f)
 Call ID: c1274a83-7133-40e0-9dc6-f4f423a0345f
  Args:
    type: :Man
    source: Michael_of_Kent
  AddTriple (8a28651c-a241-4512-9949-da0e27c21894)
 Call ID: 8a28651c-a241-4512-9949-da0e27c21894
  Args:
    target: George_V
    relation: :hasFather
    source: George_Duke_of_Kent
  AddTriple (3a22b481-0769-4d9e-b54e-e552d8f0cf37)
 Call ID: 3a22b481-0769-4d9e-b54e-e552d8f0cf37
  Args:
    source: George_Duke_of_Kent
    relation: :hasMother
    target: Queen_Mary
  AddTriple (82d8994c-72c1-4f93-ad8d-311c0ef531f3)
 Call ID: 82d8994c-72c1-4f93-ad8d-311c0ef531f3
  Args:
    source: George_Duke_of_Kent
    target: Edward_VIII
    relation: :isBrotherOf
  AddTriple (83bda037-f712-41b8-a285-7926b2f2299b)
 Call ID: 83bda037-f712-41b8-a285-7926b2f2299b
  Args:
    target: George_VI
    relation: :isBrotherOf
    source: George_Duke_of_Kent
  AddTriple (0301308c-6188-4d07-9972-eeb8824e92c3)
 Call ID: 0301308c-6188-4d07-9972-eeb8824e92c3
  Args:
    relation: :hasFather
    target: George_Duke_of_Kent
    source: Edward_Duke_of_Kent
  AddTriple (b2197909-4246-4f70-bb0b-6bad606f0023)
 Call ID: b2197909-4246-4f70-bb0b-6bad606f0023
  Args:
    source: Alexandra_of_Kent
    target: George_Duke_of_Kent
    relation: :hasFather
  AddTriple (82fece60-f82b-4edb-b6ee-fcaf95a00c93)
 Call ID: 82fece60-f82b-4edb-b6ee-fcaf95a00c93
  Args:
    source: Michael_of_Kent
    relation: :hasFather
    target: George_Duke_of_Kent
  AddTriple (b40f2faf-d982-48ba-aaa7-e0e04d8f03da)
 Call ID: b40f2faf-d982-48ba-aaa7-e0e04d8f03da
  Args:
    relation: :hasMother
    target: Princess_Marina
    source: Edward_Duke_of_Kent
  AddTriple (1c99b1ae-15a8-4fc1-b28d-7c268c0896ed)
 Call ID: 1c99b1ae-15a8-4fc1-b28d-7c268c0896ed
  Args:
    target: Princess_Marina
    relation: :hasMother
    source: Alexandra_of_Kent
  AddTriple (94c8f980-eb5e-4ef5-b321-a7ea60f05fbf)
 Call ID: 94c8f980-eb5e-4ef5-b321-a7ea60f05fbf
  Args:
    source: Michael_of_Kent
    relation: :hasMother
    target: Princess_Marina
  AddLiteral (6cde0409-4b2e-443e-86a3-fa8a458029a0)
 Call ID: 6cde0409-4b2e-443e-86a3-fa8a458029a0
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1902
    source: George_Duke_of_Kent
  AddLiteral (ba81387f-969c-4548-a225-9be6fa8fb891)
 Call ID: ba81387f-969c-4548-a225-9be6fa8fb891
  Args:
    source: George_Duke_of_Kent
    relation: :hasDeathYear
    literal_value: 1942
    literal_type: xsd:integer
  Finish (2820b750-e868-4670-a9f5-74b8643051d8)
 Call ID: 2820b750-e868-4670-a9f5-74b8643051d8
  Args: