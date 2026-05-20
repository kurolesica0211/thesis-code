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
Alexander Albert Mountbatten, 1st Marquess of Carisbrooke (born Prince Alexander Albert of Battenberg; 23 November 1886 – 23 February 1960) was a British Royal Navy officer, a member of the Hessian princely Battenberg family and the last surviving grandson of Queen Victoria.
Early life

Alexander, known as Drino, was born in 1886 at Windsor Castle in Berkshire and was educated at Wellington College and at the Britannia Royal Naval College.
His father was Prince Henry of Battenberg, the son of Prince Alexander of Hesse and by Rhine and Julie née Countess of Hauke.
His mother was Princess Beatrice of the United Kingdom, the fifth daughter and the youngest child of Queen Victoria and Prince Albert.
Prince Henry of Battenberg was the product of a morganatic marriage and took his style of Prince of Battenberg from his mother, Julia von Hauke, who was created Princess of Battenberg in her own right.
At his birth, Alexander was styled His Serene Highness Prince Alexander of Battenberg because the child of a morganatic marriage is ineligible for "Grand-Ducal Highness" status.
His godparents were Queen Victoria of the United Kingdom (his maternal grandmother), Prince Alexander of Hesse and by Rhine (his paternal grandfather), the Prince of Wales (his maternal uncle), Prince Alexander of Battenberg (his paternal uncle), and Princess Irene of Hesse and by Rhine (his maternal first cousin and paternal second cousin).
Alexander was the brother-in-law to Alfonso XIII of Spain, who married Alexander's sister, Princess Victoria Eugenia, in 1906.
Military service and honours

Alexander passed a qualifying examination to become service cadet in the Royal Navy in March 1902, and subsequently joined the cadet training ship HMS Britannia at Dartmouth on 8 May 1902.
Several of his Mountbatten cousins were also subsequently members, including his first cousins once removed the Marquess of Milford Haven and Duke of Edinburgh.
He held several other foreign orders and decorations: Grand Cross and Collar of Order of Charles III (Spain), Order of Leopold, with swords (Belgium), Order of Saint Alexander Nevsky (Russia), Order of Naval Merit, fourth class (Spain), Order of the Nile (Egypt), Order of the Crown (Romania), and Croix de Guerre, with palms (France).
During World War II, despite being in his mid-fifties, the Marquess joined the Royal Air Force and was commissioned an acting pilot officer on 6 June 1941.
Marquess of Carisbrooke

Anti-German feeling during World War I led George V to change the name of the Royal House in July 1917 from the House of Saxe-Coburg-Gotha to the House of Windsor.
The Battenberg family relinquished their titles of Prince and Princess of Battenberg and the styles of Highness and Serene Highness.
Under royal warrant, they instead took the surname Mountbatten, an Anglicised form of Battenberg.
As such, Prince Alexander became Sir Alexander Mountbatten.
On 7 November 1917, he was created Marquess of Carisbrooke, Earl of Berkhamsted and Viscount Launceston.
In the 1930s, author E. F. Benson dedicated two of his famous novels, Mapp and Lucia and Lucia's Progress, to the Marquess of Carisbrooke.
Marriage

On 19 July 1917, he married Lady Irene Denison (4 July 1890 – 16 July 1956), the only daughter of the 2nd Earl of Londesborough and his wife, Lady Grace Adelaide Fane, at the Chapel Royal of St James's Palace.
Lord and Lady Carisbrooke had one child, a daughter:
Carisbrooke was likely homosexual or bisexual; according to the published diaries of Cecil Beaton, in his later years, Lord Carisbrooke had a longtime male lover, Simon Fleet.
More is written about Lord Carisbrooke and his wife in the published diaries of James Lees-Milne and Henry "Chips" Channon.


Residences

By 1926 Lord and Lady Carisbrooke had established a London residence at No. 4 Belgrave Place, Belgravia, which continued to be their London home until early 1931.
By 1938 Lord and Lady Carisbrooke lived at Kensington Palace.
Following the death of Lady Carisbrooke in 1956, Lord Carisbrooke was granted the use of a grace-and-favour residence, Apartment 10, Kensington Palace, which remained as his home until his death in 1960.
Later career

Lord Carisbrooke, who received no state allowance, became the first member of the British royal family to work in the commercial sector.
Death

Lord Carisbrooke died on 23 February 1960, aged 73, at Kensington Palace.
His ashes were interred within the Battenberg Chapel at St. Mildred's Church, Whippingham, on the Isle of Wight.
As he had no sons, the title Marquess of Carisbrooke became extinct upon his death.



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
  AssignClass (81becd3f-9c61-4c44-acb9-8e0ff9c0e30b)
 Call ID: 81becd3f-9c61-4c44-acb9-8e0ff9c0e30b
  Args:
    source: Alexander_Albert_Mountbatten
    type: :Man
  AssignClass (d511fa93-af9e-4a36-bf61-69aad9f66fc3)
 Call ID: d511fa93-af9e-4a36-bf61-69aad9f66fc3
  Args:
    type: :Person
    source: Alexander_Albert_Mountbatten
  AddLiteral (8b232899-0f6e-4ae7-8c0d-2a5d2b8c5f74)
 Call ID: 8b232899-0f6e-4ae7-8c0d-2a5d2b8c5f74
  Args:
    source: Alexander_Albert_Mountbatten
    literal_value: 1886
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (4dd8e8af-9de2-45c9-8fd2-d39a29d5a129)
 Call ID: 4dd8e8af-9de2-45c9-8fd2-d39a29d5a129
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1960
    source: Alexander_Albert_Mountbatten
  AddLiteral (746f8f83-3c4d-4813-9e7d-b144559354a1)
 Call ID: 746f8f83-3c4d-4813-9e7d-b144559354a1
  Args:
    source: Alexander_Albert_Mountbatten
    literal_type: xsd:string
    relation: :knownAs
    literal_value: Drino
  AssignClass (e8a3adb6-29de-426b-91c6-5fc78fb78eee)
 Call ID: e8a3adb6-29de-426b-91c6-5fc78fb78eee
  Args:
    type: :Man
    source: Prince_Henry_of_Battenberg
  AssignClass (f6385a9e-2c27-4b42-90cf-f24684222432)
 Call ID: f6385a9e-2c27-4b42-90cf-f24684222432
  Args:
    source: Prince_Henry_of_Battenberg
    type: :Ancestor
  AssignClass (1d3c4783-0728-4168-82cc-d84777762570)
 Call ID: 1d3c4783-0728-4168-82cc-d84777762570
  Args:
    source: Prince_Henry_of_Battenberg
    type: :Person
  AddTriple (e90138fd-5940-4451-b032-5ae2da0b68c6)
 Call ID: e90138fd-5940-4451-b032-5ae2da0b68c6
  Args:
    source: Alexander_Albert_Mountbatten
    target: Prince_Henry_of_Battenberg
    relation: :hasFather
  AssignClass (d9a6c7c5-0fbf-4d4c-bf2a-3d5dbf2fa2e4)
 Call ID: d9a6c7c5-0fbf-4d4c-bf2a-3d5dbf2fa2e4
  Args:
    type: :Woman
    source: Princess_Beatrice_of_the_United_Kingdom
  AssignClass (870603f5-523f-48ad-9dbc-12297b295423)
 Call ID: 870603f5-523f-48ad-9dbc-12297b295423
  Args:
    type: :Ancestor
    source: Princess_Beatrice_of_the_United_Kingdom
  AssignClass (2b189103-576e-4418-ab41-581b9759a1df)
 Call ID: 2b189103-576e-4418-ab41-581b9759a1df
  Args:
    source: Princess_Beatrice_of_the_United_Kingdom
    type: :Person
  AddTriple (5531277b-ac0f-4323-bc28-bcea001e9ef4)
 Call ID: 5531277b-ac0f-4323-bc28-bcea001e9ef4
  Args:
    target: Princess_Beatrice_of_the_United_Kingdom
    source: Alexander_Albert_Mountbatten
    relation: :hasMother
  AssignClass (7aa29277-964b-4645-9924-36b894c59140)
 Call ID: 7aa29277-964b-4645-9924-36b894c59140
  Args:
    type: :Man
    source: Prince_Alexander_of_Hesse_and_by_Rhine
  AssignClass (1bd9cb5b-d4b6-48ff-9198-dfa5d58c2e6b)
 Call ID: 1bd9cb5b-d4b6-48ff-9198-dfa5d58c2e6b
  Args:
    source: Prince_Alexander_of_Hesse_and_by_Rhine
    type: :Ancestor
  AssignClass (4bc5adeb-79b5-43ce-b2dd-c7456bf7a7c8)
 Call ID: 4bc5adeb-79b5-43ce-b2dd-c7456bf7a7c8
  Args:
    type: :Person
    source: Prince_Alexander_of_Hesse_and_by_Rhine
  AddTriple (3a8ce59b-ea33-4771-b56c-629a3247f187)
 Call ID: 3a8ce59b-ea33-4771-b56c-629a3247f187
  Args:
    target: Prince_Alexander_of_Hesse_and_by_Rhine
    source: Prince_Henry_of_Battenberg
    relation: :hasFather
  AssignClass (cb91fae8-0944-455c-beac-183bc412aba0)
 Call ID: cb91fae8-0944-455c-beac-183bc412aba0
  Args:
    source: Julie_Countess_of_Hauke
    type: :Woman
  AssignClass (08a1843d-718f-4b8f-99e0-b91e30a2008a)
 Call ID: 08a1843d-718f-4b8f-99e0-b91e30a2008a
  Args:
    type: :Ancestor
    source: Julie_Countess_of_Hauke
  AssignClass (68777e2b-356d-4349-aa9c-804cc5324d2a)
 Call ID: 68777e2b-356d-4349-aa9c-804cc5324d2a
  Args:
    type: :Person
    source: Julie_Countess_of_Hauke
  AddTriple (ba23957d-0c79-4872-987d-a0c4d4336102)
 Call ID: ba23957d-0c79-4872-987d-a0c4d4336102
  Args:
    relation: :hasMother
    target: Julie_Countess_of_Hauke
    source: Prince_Henry_of_Battenberg
  AssignClass (727fb7f3-e832-4e9f-9d55-e41c47b28dd4)
 Call ID: 727fb7f3-e832-4e9f-9d55-e41c47b28dd4
  Args:
    type: :Woman
    source: Queen_Victoria
  AssignClass (675665c9-1461-409f-8d3b-336b437fe959)
 Call ID: 675665c9-1461-409f-8d3b-336b437fe959
  Args:
    type: :Ancestor
    source: Queen_Victoria
  AssignClass (24318d7e-84e2-44f4-bbbf-2e884269d626)
 Call ID: 24318d7e-84e2-44f4-bbbf-2e884269d626
  Args:
    source: Queen_Victoria
    type: :Person
  AddTriple (acf09927-eceb-4240-86b9-c1df7cb7adb2)
 Call ID: acf09927-eceb-4240-86b9-c1df7cb7adb2
  Args:
    target: Queen_Victoria
    source: Princess_Beatrice_of_the_United_Kingdom
    relation: :hasMother
  AssignClass (a8f16846-eb9c-43b6-9b0c-c9320f6e5498)
 Call ID: a8f16846-eb9c-43b6-9b0c-c9320f6e5498
  Args:
    type: :Man
    source: Prince_Albert
  AssignClass (286620b0-5c5d-4f3c-94fe-2be758abef5a)
 Call ID: 286620b0-5c5d-4f3c-94fe-2be758abef5a
  Args:
    source: Prince_Albert
    type: :Ancestor
  AssignClass (d4b1a8f8-c36e-4f05-a862-8fb401e453b1)
 Call ID: d4b1a8f8-c36e-4f05-a862-8fb401e453b1
  Args:
    source: Prince_Albert
    type: :Person
  AddTriple (8a9e05bf-4a9f-4d3e-9ac0-775159051814)
 Call ID: 8a9e05bf-4a9f-4d3e-9ac0-775159051814
  Args:
    target: Prince_Albert
    source: Princess_Beatrice_of_the_United_Kingdom
    relation: :hasFather
  AssignClass (f989b233-92d5-49ba-8a97-a455cfb418ac)
 Call ID: f989b233-92d5-49ba-8a97-a455cfb418ac
  Args:
    source: Lady_Irene_Denison
    type: :Woman
  AssignClass (a0f7cb67-aed5-42ae-ad13-cd4da3926430)
 Call ID: a0f7cb67-aed5-42ae-ad13-cd4da3926430
  Args:
    source: Lady_Irene_Denison
    type: :Person
  AddLiteral (f8dba8da-68e6-46bd-b3ca-95eddae67936)
 Call ID: f8dba8da-68e6-46bd-b3ca-95eddae67936
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 1917
    source: Alexander_Albert_Mountbatten
  AddTriple (004d69f1-b5b0-4527-838f-68495717146d)
 Call ID: 004d69f1-b5b0-4527-838f-68495717146d
  Args:
    relation: :hasRelation
    source: Alexander_Albert_Mountbatten
    target: Lady_Irene_Denison
  AssignClass (4da03381-e4c1-42cb-9261-3096d7d04978)
 Call ID: 4da03381-e4c1-42cb-9261-3096d7d04978
  Args:
    source: Princess_Victoria_Eugenia
    type: :Woman
  AssignClass (99d0a6c8-0acc-417d-a116-69c0fdc3cc3c)
 Call ID: 99d0a6c8-0acc-417d-a116-69c0fdc3cc3c
  Args:
    type: :Person
    source: Princess_Victoria_Eugenia
  AddTriple (e8cc9d4c-1896-44a4-abea-58025f640bac)
 Call ID: e8cc9d4c-1896-44a4-abea-58025f640bac
  Args:
    target: Princess_Victoria_Eugenia
    source: Alexander_Albert_Mountbatten
    relation: :hasSister
  AssignClass (9c85d1be-fa94-467e-afce-a16bfce85ac2)
 Call ID: 9c85d1be-fa94-467e-afce-a16bfce85ac2
  Args:
    source: Alfonso_XIII_of_Spain
    type: :Man
  AssignClass (15a82788-2eb5-4002-99b6-4481bbdd4a50)
 Call ID: 15a82788-2eb5-4002-99b6-4481bbdd4a50
  Args:
    type: :Person
    source: Alfonso_XIII_of_Spain
  AddTriple (c4c6cf40-2b25-43d9-9334-ef1f025fa87e)
 Call ID: c4c6cf40-2b25-43d9-9334-ef1f025fa87e
  Args:
    source: Princess_Victoria_Eugenia
    target: Alfonso_XIII_of_Spain
    relation: :hasRelation
  Finish (78be7e9b-3277-4ce8-aa24-5f4149c0c7c3)
 Call ID: 78be7e9b-3277-4ce8-aa24-5f4149c0c7c3
  Args: