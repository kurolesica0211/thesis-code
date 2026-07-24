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
@prefix ns1: <http://www.w3.org/2003/11/swrl#> .
@prefix ns2: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
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

:hasDeathYear a owl:AnnotationProperty .

:hasMarriageYear a owl:AnnotationProperty .

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

ns2:isRuleEnabled a owl:AnnotationProperty .

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

:isAncestorOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation .

:isSisterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf .

:hasChild a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:inverseOf :isChildOf .

:hasParent a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Person ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:equivalentProperty :isChildOf ;
    owl:inverseOf :isParentOf .

:isSiblingOf a owl:ObjectProperty,
        owl:SymmetricProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isBloodrelationOf ;
    owl:propertyChainAxiom ( :hasParent :isParentOf ) .

:Sex a owl:Class ;
    rdfs:subClassOf :DomainEntity ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Female :Male ) ] .

:isChildOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:propertyDisjointWith :isSisterOf .

:x a ns1:Variable .

:Man a owl:Class ;
    owl:disjointWith :Sex,
        :Woman ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Male ] ) ] .

:isParentOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:propertyDisjointWith :isSisterOf .

:Woman a owl:Class ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Female ] ) ] .

:y a ns1:Variable .

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

[] a ns1:Imp ;
    rdfs:label "infer hasSon" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasBrother" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasSister" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (27bbfe83-0f43-4297-bdeb-63e4273c0d59)
 Call ID: 27bbfe83-0f43-4297-bdeb-63e4273c0d59
  Args:
    type: :Woman
    source: Catherine_Oxenberg
  AssignClass (627c321d-ed47-4731-975f-058e26160e28)
 Call ID: 627c321d-ed47-4731-975f-058e26160e28
  Args:
    type: :Woman
    source: Princess_Elizabeth_of_Yugoslavia
  AssignClass (1bef8b15-0455-4e42-a998-ae92c0fb1c0f)
 Call ID: 1bef8b15-0455-4e42-a998-ae92c0fb1c0f
  Args:
    type: :Man
    source: Howard_Oxenberg
  AssignClass (f618812c-c94b-40d5-8c68-89b33ca00140)
 Call ID: f618812c-c94b-40d5-8c68-89b33ca00140
  Args:
    type: :Woman
    source: Christina_Oxenberg
  AssignClass (3c631358-efd2-44c6-bcc8-3e5c7c7968ce)
 Call ID: 3c631358-efd2-44c6-bcc8-3e5c7c7968ce
  Args:
    type: :Man
    source: Prince_Paul_of_Yugoslavia
  AssignClass (ae15e59f-6b80-4a16-b6e8-98d21df93a43)
 Call ID: ae15e59f-6b80-4a16-b6e8-98d21df93a43
  Args:
    type: :Woman
    source: Princess_Olga_of_Greece_and_Denmark
  AssignClass (44659896-6708-43bd-bf3a-58eef2651577)
 Call ID: 44659896-6708-43bd-bf3a-58eef2651577
  Args:
    type: :Woman
    source: India_Riven_Oxenberg
  AssignClass (7f939eaf-a146-4d39-a918-176a876827bf)
 Call ID: 7f939eaf-a146-4d39-a918-176a876827bf
  Args:
    type: :Man
    source: William_Weitz_Shaffer
  AssignClass (8e48de39-5714-4a1f-9319-a4a91035b7b1)
 Call ID: 8e48de39-5714-4a1f-9319-a4a91035b7b1
  Args:
    type: :Man
    source: Robert_Evans
  AssignClass (a3860066-9812-478e-9756-196d087727d3)
 Call ID: a3860066-9812-478e-9756-196d087727d3
  Args:
    type: :Man
    source: Casper_Van_Dien
  AssignClass (c23974f4-550e-483d-a278-be208ba98ca5)
 Call ID: c23974f4-550e-483d-a278-be208ba98ca5
  Args:
    type: :Man
    source: Ellis_Jones
  AddLiteral (2e4d5397-da12-48b9-ad4f-3653029c8c81)
 Call ID: 2e4d5397-da12-48b9-ad4f-3653029c8c81
  Args:
    literal_value: 1961
    literal_type: xsd:string
    source: Catherine_Oxenberg
    relation: :hasBirthYear
  AddLiteral (81c386b4-025b-4265-a7b3-2ec4afc2bced)
 Call ID: 81c386b4-025b-4265-a7b3-2ec4afc2bced
  Args:
    relation: :hasBirthYear
    source: Princess_Elizabeth_of_Yugoslavia
    literal_value: 1936
    literal_type: xsd:string
  AddLiteral (6496e2b7-affe-42b1-98c5-9454a80b5348)
 Call ID: 6496e2b7-affe-42b1-98c5-9454a80b5348
  Args:
    relation: :hasBirthYear
    source: Howard_Oxenberg
    literal_type: xsd:string
    literal_value: 1919
  AddLiteral (d7d26c87-a889-4951-89e4-d9c53f69b0f3)
 Call ID: d7d26c87-a889-4951-89e4-d9c53f69b0f3
  Args:
    literal_value: 2010
    literal_type: xsd:string
    source: Howard_Oxenberg
    relation: :hasDeathYear
  AddTriple (cd2a6d57-728a-413d-afea-9be9524b325f)
 Call ID: cd2a6d57-728a-413d-afea-9be9524b325f
  Args:
    target: Princess_Elizabeth_of_Yugoslavia
    relation: :isChildOf
    source: Catherine_Oxenberg
  AddTriple (5e453036-1c5a-4e80-8a7b-062707438df5)
 Call ID: 5e453036-1c5a-4e80-8a7b-062707438df5
  Args:
    target: Howard_Oxenberg
    source: Catherine_Oxenberg
    relation: :isChildOf
  AddTriple (9a7c5a2b-a28b-4319-9995-6fd397520edc)
 Call ID: 9a7c5a2b-a28b-4319-9995-6fd397520edc
  Args:
    relation: :isSiblingOf
    source: Catherine_Oxenberg
    target: Christina_Oxenberg
  AddTriple (b684e91d-ad00-453d-98d1-53d56d584eb8)
 Call ID: b684e91d-ad00-453d-98d1-53d56d584eb8
  Args:
    relation: :isChildOf
    source: Princess_Elizabeth_of_Yugoslavia
    target: Prince_Paul_of_Yugoslavia
  AddTriple (8378c46c-1b02-425f-bffa-f5a0723a21d2)
 Call ID: 8378c46c-1b02-425f-bffa-f5a0723a21d2
  Args:
    source: Princess_Elizabeth_of_Yugoslavia
    relation: :isChildOf
    target: Princess_Olga_of_Greece_and_Denmark
  AddTriple (cd50b470-27ad-4e50-94ec-eebe8f9651e2)
 Call ID: cd50b470-27ad-4e50-94ec-eebe8f9651e2
  Args:
    relation: :isChildOf
    source: India_Riven_Oxenberg
    target: Catherine_Oxenberg
  AddTriple (2dd7c620-88ca-433d-ba34-ee0f78c50668)
 Call ID: 2dd7c620-88ca-433d-ba34-ee0f78c50668
  Args:
    target: William_Weitz_Shaffer
    source: India_Riven_Oxenberg
    relation: :isChildOf
  AddLiteral (20be64f9-ec58-4b5b-a13a-b72ee6bc675a)
 Call ID: 20be64f9-ec58-4b5b-a13a-b72ee6bc675a
  Args:
    literal_type: xsd:string
    literal_value: 1998
    relation: :hasMarriageYear
    source: Robert_Evans
  Finish (ae668f07-287b-4f3a-b510-491776b40678)
 Call ID: ae668f07-287b-4f3a-b510-491776b40678
  Args: