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
Catherine Oxenberg (born September 22, 1961) is an American actress.
Oxenberg is the daughter of Princess Elizabeth of Yugoslavia and her first husband, Howard Oxenberg (1919–2010).
She twice played Diana, Princess of Wales on screen, in The Royal Romance of Charles and Diana (1982) and Charles and Diana: Unhappily Ever After (1992), and has appeared in many other films.
Early life and education

Oxenberg was born in New York City, and grew up in London.
She is the eldest daughter of Princess Elizabeth of Yugoslavia (born 1936), a member of the House of Karađorđević, and her first husband Howard Oxenberg (1919–2010), a Jewish self-made textile and clothing tycoon and close friend of the Kennedy family.
Her sister is Christina Oxenberg.
Princess Elizabeth is the only daughter of Prince Paul of Yugoslavia (who served as regent for his cousin's eldest son King Peter II of Yugoslavia) and Princess Olga of Greece and Denmark.
Through her maternal grandmother, Catherine is a first cousin once removed of: Prince Edward, Duke of Kent, Princess Alexandra, The Honourable Lady Ogilvy and Prince Michael of Kent.
Oxenberg is a second cousin once removed of Queen Sofía of Spain and Charles III of the United Kingdom, making Catherine a third cousin of Felipe VI of Spain and William, Prince of Wales.
She is also a third cousin once removed of Margrethe II of Denmark and Harald V of Norway; and a fourth cousin to Grand Duke Henri of Luxembourg and King Philippe of Belgium.
Oxenberg was educated at the Lycée Français Charles de Gaulle in Kensington, London, St. Paul's School, and Columbia University, though she did not finish college.
Ancestry

Through her maternal grandfather, Prince Paul of Yugoslavia of the House of Karađorđević, Catherine Oxenberg is a great-great-great-granddaughter of Karađorđe, who started the First Serbian Uprising against the Ottoman Empire in 1804.
Her maternal grandmother, Princess Olga, was the daughter of Grand Duchess Elena Vladimirovna of Russia and Prince Nicholas of Greece and Denmark, himself the son of another Romanov grand duchess, Queen Olga Konstantinovna of the Hellenes and her Danish-born husband King George of Greece, brother of Queen Alexandra of the United Kingdom and the Empress Maria Fyodorovna.
Career

Oxenberg made her acting debut in the 1982 made-for-television film The Royal Romance of Charles and Diana, in which she played Diana, Princess of Wales.
In 1984, Oxenberg joined the hit ABC prime time soap opera Dynasty—then at its height of popularity—in the role of Amanda Carrington.
Oxenberg left Dynasty in 1986, following a salary dispute after the end of her second season, and the role was recast with Karen Cellini.
Though Oxenberg's publicist insisted that the actress left Dynasty voluntarily, several media outlets reported that she was fired.
Oxenberg was the guest host on the May 10, 1986, episode of Saturday Night Live, making her the only descendant of a royal family to host the show.
Oxenberg starred as Princess Elysa in the 1987 television film Roman Holiday.
She also appeared in The Lair of the White Worm in 1988, and reprised the role of Diana, Princess of Wales in the TV film Charles and Diana: Unhappily Ever After in 1992.
From 1993 to 1994, she starred in the short-lived series Acapulco H.E.A.T.


Oxenberg was portrayed by Rachael Taylor in the 2005 telemovie Dynasty: The Making of a Guilty Pleasure, a fictionalized retelling of the behind-the-scenes goings-on during the production of Dynasty.
In 2006, Oxenberg appeared in the TV special, Dynasty Reunion: Catfights & Caviar, in which she was reunited with her former Dynasty castmates to reminisce about the series.
In 2019, Catherine Oxenberg produced and narrated Escaping the NXIVM Cult: A Mother's Fight to Save Her Daughter in which Andrea Roth portrayed her.
Personal life

In June 1991, Oxenberg had a daughter, India Riven Oxenberg, whose father was later revealed to be the convicted drug smuggler William Weitz Shaffer.
In December 1992, Oxenberg was living with her daughter in Coldwater Canyon, Los Angeles, California.
Oxenberg's first marriage was to the producer Robert Evans, in Beverly Hills, California, on July 12, 1998, but the marriage was annulled nine days later.
Oxenberg met the actor Casper Van Dien during the filming of the 1999 TV movie The Collectors, and they worked together again the same year in the Evangelical Christian thriller The Omega Code.
Van Dien and Oxenberg have two daughters.
In 2005, the couple appeared in their own reality series, I Married a Princess, which aired on the Lifetime Television channel in the United States and on LIVINGtv in the United Kingdom.
Van Dien filed for divorce from Oxenberg in 2015.
While Oxenberg and Van Dien were married, and before India joined NXIVM, Oxenberg and Van Dien were celebrity ambassadors for the non-profit organization Childhelp.
In June 2023, Oxenberg revealed her engagement to businessman Ellis Jones.
They began dating shortly after Jones offered Oxenberg a place to stay following her losing her home in the 2018 California wildfires.
NXIVM

Oxenberg acknowledged in November 2017 that she had had interactions with Keith Raniere and his NXIVM organization, bringing her daughter India into NXIVM in 2011 for what she thought would be "a self-help, business-oriented program."
Oxenberg confirmed that her daughter became heavily involved in the cult and that she had initiated what proved to be a failed intervention for India.
In August 2018, Oxenberg revealed that India had left NXIVM in June, after the arrest of Raniere, and they were working on their relationship.
In August 2018, Oxenberg's book Captive: A Mother's Crusade to Save Her Daughter from a Terrifying Cult co-written by former People magazine writer Natasha Stoynoff was published.
In 2020, Oxenberg was featured in The Vow, a documentary series for HBO, directed by Jehane Noujaim and Karim Amer, which follows Oxenberg's attempts to rescue her daughter India.
Oxenberg also appears in Seduced: Inside the NXIVM Cult a documentary series for Starz, directed by Cecilia Peck and Inbal B. Lessner, which features India speaking out about her experiences for the first time.
Filmography

Film

Television

Accolades

For playing Amanda Carrington, Oxenberg won two Soap Opera Digest Awards in 1985, for Outstanding Supporting Actress and Outstanding Female Newcomer.



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
  AssignClass (d9abf002-83cb-4262-bdff-f83efe872279)
 Call ID: d9abf002-83cb-4262-bdff-f83efe872279
  Args:
    source: Catherine Oxenberg
    type: :Woman
  AssignClass (5f355e96-cf8f-422c-adca-1d514792a6b7)
 Call ID: 5f355e96-cf8f-422c-adca-1d514792a6b7
  Args:
    type: :Person
    source: Catherine Oxenberg
  AddLiteral (bf674383-4434-41b9-97ad-e32091880b95)
 Call ID: bf674383-4434-41b9-97ad-e32091880b95
  Args:
    relation: :hasBirthYear
    literal_value: 1961
    source: Catherine Oxenberg
    literal_type: xsd:integer
  AssignClass (01f196f3-7de2-42ba-904e-b521a83aee1a)
 Call ID: 01f196f3-7de2-42ba-904e-b521a83aee1a
  Args:
    source: Princess Elizabeth of Yugoslavia
    type: :Woman
  AssignClass (9e358a98-031f-41dd-bf17-622257ef4c8c)
 Call ID: 9e358a98-031f-41dd-bf17-622257ef4c8c
  Args:
    source: Princess Elizabeth of Yugoslavia
    type: :Person
  AssignClass (cd0caa08-016e-4490-b6a5-a65adff0d958)
 Call ID: cd0caa08-016e-4490-b6a5-a65adff0d958
  Args:
    type: :Man
    source: Howard Oxenberg
  AssignClass (95f07606-4362-4622-a640-b21c29cdc197)
 Call ID: 95f07606-4362-4622-a640-b21c29cdc197
  Args:
    type: :Person
    source: Howard Oxenberg
  AddLiteral (7c25d564-b6bb-4ca9-bedd-c79720ed6841)
 Call ID: 7c25d564-b6bb-4ca9-bedd-c79720ed6841
  Args:
    source: Howard Oxenberg
    literal_value: 1919
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (04b509ae-a9d7-47c9-ab61-18f18b1aba8f)
 Call ID: 04b509ae-a9d7-47c9-ab61-18f18b1aba8f
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 2010
    source: Howard Oxenberg
  AddTriple (d278387b-0cc2-45ec-83ca-b30a076cf609)
 Call ID: d278387b-0cc2-45ec-83ca-b30a076cf609
  Args:
    target: Princess Elizabeth of Yugoslavia
    relation: :hasMother
    source: Catherine Oxenberg
  AddTriple (645c0c81-ce99-4ba9-8139-794dca612125)
 Call ID: 645c0c81-ce99-4ba9-8139-794dca612125
  Args:
    relation: :hasFather
    target: Howard Oxenberg
    source: Catherine Oxenberg
  AssignClass (a533e9c2-dc23-429b-926e-284f57208a05)
 Call ID: a533e9c2-dc23-429b-926e-284f57208a05
  Args:
    type: :Woman
    source: Christina Oxenberg
  AssignClass (5060a3d6-859a-4b1a-af03-862a7a61edfd)
 Call ID: 5060a3d6-859a-4b1a-af03-862a7a61edfd
  Args:
    type: :Person
    source: Christina Oxenberg
  AddTriple (38a62428-7b6a-4d6d-b16e-273f69a72405)
 Call ID: 38a62428-7b6a-4d6d-b16e-273f69a72405
  Args:
    source: Catherine Oxenberg
    target: Christina Oxenberg
    relation: :hasSister
  AssignClass (fd1baff7-2330-4848-8c3e-d05d1e550170)
 Call ID: fd1baff7-2330-4848-8c3e-d05d1e550170
  Args:
    type: :Man
    source: Prince Paul of Yugoslavia
  AssignClass (b36893cc-6bce-40cd-b47f-e7097208f58d)
 Call ID: b36893cc-6bce-40cd-b47f-e7097208f58d
  Args:
    type: :Person
    source: Prince Paul of Yugoslavia
  AssignClass (f559019a-b053-4a53-95ad-025b746b9437)
 Call ID: f559019a-b053-4a53-95ad-025b746b9437
  Args:
    type: :Woman
    source: Princess Olga of Greece and Denmark
  AssignClass (a29af3a2-442e-47c6-ae85-7dbff2b34bbd)
 Call ID: a29af3a2-442e-47c6-ae85-7dbff2b34bbd
  Args:
    source: Princess Olga of Greece and Denmark
    type: :Person
  AddTriple (4d29bc89-d5fe-466a-8906-e91f7ec3830d)
 Call ID: 4d29bc89-d5fe-466a-8906-e91f7ec3830d
  Args:
    target: Prince Paul of Yugoslavia
    relation: :hasFather
    source: Princess Elizabeth of Yugoslavia
  AddTriple (36e13270-c9d6-4470-9e9e-4a9ceb8e162e)
 Call ID: 36e13270-c9d6-4470-9e9e-4a9ceb8e162e
  Args:
    relation: :hasMother
    target: Princess Olga of Greece and Denmark
    source: Princess Elizabeth of Yugoslavia
  AssignClass (cee64b32-cb9b-4f37-9ca5-1823e9a660c4)
 Call ID: cee64b32-cb9b-4f37-9ca5-1823e9a660c4
  Args:
    source: India Riven Oxenberg
    type: :Woman
  AssignClass (9552f41a-6657-44f3-8e25-00f663ca335e)
 Call ID: 9552f41a-6657-44f3-8e25-00f663ca335e
  Args:
    type: :Person
    source: India Riven Oxenberg
  AddTriple (83487e0f-659f-4ebb-907f-bf83f815ebb9)
 Call ID: 83487e0f-659f-4ebb-907f-bf83f815ebb9
  Args:
    relation: :hasMother
    target: Catherine Oxenberg
    source: India Riven Oxenberg
  AssignClass (a0b60a2f-ae80-40e6-8bd4-06e4c9dea3f5)
 Call ID: a0b60a2f-ae80-40e6-8bd4-06e4c9dea3f5
  Args:
    type: :Man
    source: William Weitz Shaffer
  AssignClass (a05501dd-8cde-472c-839a-a98aa933dbf1)
 Call ID: a05501dd-8cde-472c-839a-a98aa933dbf1
  Args:
    source: William Weitz Shaffer
    type: :Person
  AddTriple (4a7ee7cf-b3e0-47db-aa4f-f2f0ebfbeac3)
 Call ID: 4a7ee7cf-b3e0-47db-aa4f-f2f0ebfbeac3
  Args:
    source: India Riven Oxenberg
    relation: :hasFather
    target: William Weitz Shaffer
  AssignClass (9f175e91-fbdf-4424-a343-d65eb7573e29)
 Call ID: 9f175e91-fbdf-4424-a343-d65eb7573e29
  Args:
    source: Robert Evans
    type: :Man
  AssignClass (a5c07a97-0f0b-4515-b0dc-67deca08f897)
 Call ID: a5c07a97-0f0b-4515-b0dc-67deca08f897
  Args:
    type: :Person
    source: Robert Evans
  AddLiteral (0eb8c826-ad11-4d2f-9af7-e8c08e8e63df)
 Call ID: 0eb8c826-ad11-4d2f-9af7-e8c08e8e63df
  Args:
    relation: :hasMarriageYear
    source: Catherine Oxenberg
    literal_value: 1998
    literal_type: xsd:integer
  AssignClass (e11bf2fd-568d-47f7-a272-e77fc6622bd3)
 Call ID: e11bf2fd-568d-47f7-a272-e77fc6622bd3
  Args:
    source: Casper Van Dien
    type: :Man
  AssignClass (6ca5dba1-c502-4291-bc15-7d3ad0a2b400)
 Call ID: 6ca5dba1-c502-4291-bc15-7d3ad0a2b400
  Args:
    source: Casper Van Dien
    type: :Person
  AssignClass (f8a5970a-7a54-4305-b50b-a477db474f61)
 Call ID: f8a5970a-7a54-4305-b50b-a477db474f61
  Args:
    source: Ellis Jones
    type: :Man
  AssignClass (44cdb6bf-f0b1-485d-b87d-8a0d01252a64)
 Call ID: 44cdb6bf-f0b1-485d-b87d-8a0d01252a64
  Args:
    type: :Person
    source: Ellis Jones
  Finish (bd860854-c46d-471f-97b5-16266a62cfea)
 Call ID: bd860854-c46d-471f-97b5-16266a62cfea
  Args: