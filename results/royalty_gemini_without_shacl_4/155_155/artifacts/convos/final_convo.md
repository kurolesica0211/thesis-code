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
  AssignClass (443681ad-f327-4252-86be-d16c041a060c)
 Call ID: 443681ad-f327-4252-86be-d16c041a060c
  Args:
    type: :Woman
    source: Catherine_Oxenberg
  AssignClass (163b66af-f62d-49f8-8164-da65402a5c34)
 Call ID: 163b66af-f62d-49f8-8164-da65402a5c34
  Args:
    type: :Woman
    source: Princess_Elizabeth_of_Yugoslavia
  AssignClass (08c37490-6fe8-4575-9bab-6c86b9dc7ba9)
 Call ID: 08c37490-6fe8-4575-9bab-6c86b9dc7ba9
  Args:
    type: :Man
    source: Howard_Oxenberg
  AssignClass (55173047-12c0-4f18-901e-ceb3b23b7839)
 Call ID: 55173047-12c0-4f18-901e-ceb3b23b7839
  Args:
    type: :Woman
    source: Christina_Oxenberg
  AssignClass (1589928b-974a-46d1-b964-f56687e9852d)
 Call ID: 1589928b-974a-46d1-b964-f56687e9852d
  Args:
    type: :Man
    source: Prince_Paul_of_Yugoslavia
  AssignClass (1a34125f-c59f-4d1b-986d-9b4545313fe0)
 Call ID: 1a34125f-c59f-4d1b-986d-9b4545313fe0
  Args:
    type: :Woman
    source: Princess_Olga_of_Greece_and_Denmark
  AssignClass (613f7401-ca3b-4979-8466-6bba62fc525b)
 Call ID: 613f7401-ca3b-4979-8466-6bba62fc525b
  Args:
    type: :Woman
    source: India_Riven_Oxenberg
  AssignClass (740b4c49-ef9b-4dd5-8f47-12753d7bd2b6)
 Call ID: 740b4c49-ef9b-4dd5-8f47-12753d7bd2b6
  Args:
    type: :Man
    source: William_Weitz_Shaffer
  AssignClass (352f9c12-6712-4aa5-bb7f-2af1966e1c7a)
 Call ID: 352f9c12-6712-4aa5-bb7f-2af1966e1c7a
  Args:
    type: :Man
    source: Robert_Evans
  AssignClass (87d70526-2f7f-492b-981c-bbbd0768436d)
 Call ID: 87d70526-2f7f-492b-981c-bbbd0768436d
  Args:
    type: :Man
    source: Casper_Van_Dien
  AssignClass (25abe424-b753-4f01-8d4b-82eee82ff1f3)
 Call ID: 25abe424-b753-4f01-8d4b-82eee82ff1f3
  Args:
    type: :Man
    source: Ellis_Jones
  AddLiteral (9fc94551-85ef-4bbe-84a9-3397df251f71)
 Call ID: 9fc94551-85ef-4bbe-84a9-3397df251f71
  Args:
    literal_type: xsd:integer
    source: Catherine_Oxenberg
    literal_value: 1961
    relation: :hasBirthYear
  AddTriple (86ee7bee-ca3e-4e24-9ab3-a80e7c0e461c)
 Call ID: 86ee7bee-ca3e-4e24-9ab3-a80e7c0e461c
  Args:
    source: Catherine_Oxenberg
    relation: :hasMother
    target: Princess_Elizabeth_of_Yugoslavia
  AddTriple (c52b80be-8935-469f-91ca-7a5de14dd40d)
 Call ID: c52b80be-8935-469f-91ca-7a5de14dd40d
  Args:
    source: Catherine_Oxenberg
    relation: :hasFather
    target: Howard_Oxenberg
  AddLiteral (bcf780af-c94d-4559-8ada-1eb1f6a8fb58)
 Call ID: bcf780af-c94d-4559-8ada-1eb1f6a8fb58
  Args:
    literal_value: 1919
    relation: :hasBirthYear
    source: Howard_Oxenberg
    literal_type: xsd:integer
  AddLiteral (0fd98081-bea3-4512-9560-74d1505b455e)
 Call ID: 0fd98081-bea3-4512-9560-74d1505b455e
  Args:
    relation: :hasDeathYear
    literal_value: 2010
    literal_type: xsd:integer
    source: Howard_Oxenberg
  AddLiteral (6208ab6f-8f7d-4615-9096-d91b5b753a4a)
 Call ID: 6208ab6f-8f7d-4615-9096-d91b5b753a4a
  Args:
    relation: :hasBirthYear
    literal_value: 1936
    source: Princess_Elizabeth_of_Yugoslavia
    literal_type: xsd:integer
  AddTriple (cc325b8f-96b7-4300-972e-f003ed700de0)
 Call ID: cc325b8f-96b7-4300-972e-f003ed700de0
  Args:
    target: Christina_Oxenberg
    relation: :isSisterOf
    source: Catherine_Oxenberg
  AddTriple (4984f2a7-787e-4bde-9429-cc79365df7fa)
 Call ID: 4984f2a7-787e-4bde-9429-cc79365df7fa
  Args:
    target: Prince_Paul_of_Yugoslavia
    relation: :hasFather
    source: Princess_Elizabeth_of_Yugoslavia
  AddTriple (22181f0f-98a9-4e2e-a9cf-0d2555b1179c)
 Call ID: 22181f0f-98a9-4e2e-a9cf-0d2555b1179c
  Args:
    source: Princess_Elizabeth_of_Yugoslavia
    target: Princess_Olga_of_Greece_and_Denmark
    relation: :hasMother
  AddTriple (e3b86727-434a-49e0-a6ca-23184495793b)
 Call ID: e3b86727-434a-49e0-a6ca-23184495793b
  Args:
    source: Catherine_Oxenberg
    relation: :hasMother
    target: India_Riven_Oxenberg
  AddTriple (d6816cd7-618b-43b4-aa8e-697a65bbf48f)
 Call ID: d6816cd7-618b-43b4-aa8e-697a65bbf48f
  Args:
    target: William_Weitz_Shaffer
    relation: :hasFather
    source: India_Riven_Oxenberg
  AddLiteral (b13c2a76-cf13-4a9f-9cd0-fdfe634499a8)
 Call ID: b13c2a76-cf13-4a9f-9cd0-fdfe634499a8
  Args:
    literal_value: 1998
    relation: :hasMarriageYear
    source: Catherine_Oxenberg
    literal_type: xsd:integer
  AddTriple (78c99351-eec4-4006-b286-58e2574aeab2)
 Call ID: 78c99351-eec4-4006-b286-58e2574aeab2
  Args:
    source: Catherine_Oxenberg
    target: Robert_Evans
    relation: :hasRelation
  AddTriple (a17d4d14-7817-4980-a46f-8e25e49dac70)
 Call ID: a17d4d14-7817-4980-a46f-8e25e49dac70
  Args:
    target: Casper_Van_Dien
    relation: :hasRelation
    source: Catherine_Oxenberg
  Finish (45bfe769-209b-4959-8ab6-9e60c5e14297)
 Call ID: 45bfe769-209b-4959-8ab6-9e60c5e14297
  Args: