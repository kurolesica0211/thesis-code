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
  AssignClass (2e56b910-c242-4f8e-901e-aacb8f234872)
 Call ID: 2e56b910-c242-4f8e-901e-aacb8f234872
  Args:
    type: :Person
    source: Catherine Oxenberg
  AssignClass (758e4867-0f2a-406c-9d3c-94cc39ed0934)
 Call ID: 758e4867-0f2a-406c-9d3c-94cc39ed0934
  Args:
    type: :Woman
    source: Catherine Oxenberg
  AddLiteral (54380d14-9ea3-4903-8421-d921be42e5fa)
 Call ID: 54380d14-9ea3-4903-8421-d921be42e5fa
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Catherine Oxenberg
    literal_value: 1961
  AssignClass (fd9d8fa2-7797-471b-8a50-e22e3e6c25a5)
 Call ID: fd9d8fa2-7797-471b-8a50-e22e3e6c25a5
  Args:
    type: :Person
    source: Princess Elizabeth of Yugoslavia
  AssignClass (617f10b0-39c2-4283-83c5-df8f9e1c141e)
 Call ID: 617f10b0-39c2-4283-83c5-df8f9e1c141e
  Args:
    type: :Woman
    source: Princess Elizabeth of Yugoslavia
  AssignClass (aa955962-ee5b-4a0b-a09c-6a52148b99d7)
 Call ID: aa955962-ee5b-4a0b-a09c-6a52148b99d7
  Args:
    type: :Person
    source: Howard Oxenberg
  AssignClass (c73d7b65-6c8e-4e43-a313-beaa18d4d65d)
 Call ID: c73d7b65-6c8e-4e43-a313-beaa18d4d65d
  Args:
    type: :Man
    source: Howard Oxenberg
  AddTriple (9b54d772-97a0-4f18-b735-5135c75f7f92)
 Call ID: 9b54d772-97a0-4f18-b735-5135c75f7f92
  Args:
    target: Princess Elizabeth of Yugoslavia
    relation: :hasMother
    source: Catherine Oxenberg
  AddTriple (3b20731f-7327-47fe-a9a3-c6bdb5721029)
 Call ID: 3b20731f-7327-47fe-a9a3-c6bdb5721029
  Args:
    source: Catherine Oxenberg
    target: Howard Oxenberg
    relation: :hasFather
  AddLiteral (d5f587e7-8c71-48a9-a64f-5cc75135a9cd)
 Call ID: d5f587e7-8c71-48a9-a64f-5cc75135a9cd
  Args:
    source: Howard Oxenberg
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1919
  AddLiteral (a05cc2ce-4292-4b17-8d41-a30242495360)
 Call ID: a05cc2ce-4292-4b17-8d41-a30242495360
  Args:
    literal_value: 2010
    source: Howard Oxenberg
    literal_type: xsd:integer
    relation: :hasDeathYear
  AddLiteral (1189be27-e6f7-41cd-8747-862884461e5d)
 Call ID: 1189be27-e6f7-41cd-8747-862884461e5d
  Args:
    literal_value: 1936
    source: Princess Elizabeth of Yugoslavia
    relation: :hasBirthYear
    literal_type: xsd:integer
  AssignClass (bd060ed1-1fe8-4cee-b351-74cf1ace0d2a)
 Call ID: bd060ed1-1fe8-4cee-b351-74cf1ace0d2a
  Args:
    type: :Person
    source: Christina Oxenberg
  AssignClass (f7291072-71ec-4e1c-8145-8216559af3a0)
 Call ID: f7291072-71ec-4e1c-8145-8216559af3a0
  Args:
    type: :Woman
    source: Christina Oxenberg
  AddTriple (65655966-c13a-404f-8c90-8a620630c2a6)
 Call ID: 65655966-c13a-404f-8c90-8a620630c2a6
  Args:
    target: Christina Oxenberg
    relation: :hasSister
    source: Catherine Oxenberg
  AssignClass (ee83d1d0-6615-4043-bc14-e135cbe5a4f2)
 Call ID: ee83d1d0-6615-4043-bc14-e135cbe5a4f2
  Args:
    type: :Person
    source: Prince Paul of Yugoslavia
  AssignClass (cbc6928d-ccae-4e18-8ec1-0a9337af129f)
 Call ID: cbc6928d-ccae-4e18-8ec1-0a9337af129f
  Args:
    type: :Man
    source: Prince Paul of Yugoslavia
  AssignClass (b2265d5f-1cec-4bc9-9793-ac658bef3f77)
 Call ID: b2265d5f-1cec-4bc9-9793-ac658bef3f77
  Args:
    type: :Person
    source: Princess Olga of Greece and Denmark
  AssignClass (d69d106a-6e05-4539-a222-ca37466fc08c)
 Call ID: d69d106a-6e05-4539-a222-ca37466fc08c
  Args:
    type: :Woman
    source: Princess Olga of Greece and Denmark
  AddTriple (3bd88028-8ce0-4380-854d-3d56393d1291)
 Call ID: 3bd88028-8ce0-4380-854d-3d56393d1291
  Args:
    source: Princess Elizabeth of Yugoslavia
    relation: :hasFather
    target: Prince Paul of Yugoslavia
  AddTriple (d3c5bdb9-c725-483d-9bb9-cd7036fbd869)
 Call ID: d3c5bdb9-c725-483d-9bb9-cd7036fbd869
  Args:
    source: Princess Elizabeth of Yugoslavia
    relation: :hasMother
    target: Princess Olga of Greece and Denmark
  AssignClass (cd45c4b8-107e-49aa-bff8-997d7eb38861)
 Call ID: cd45c4b8-107e-49aa-bff8-997d7eb38861
  Args:
    type: :Person
    source: India Riven Oxenberg
  AssignClass (4ef136b0-d96c-4615-9b3c-0434d6555ad1)
 Call ID: 4ef136b0-d96c-4615-9b3c-0434d6555ad1
  Args:
    type: :Woman
    source: India Riven Oxenberg
  AddTriple (e6b9db57-7adc-4570-87bd-01968825644c)
 Call ID: e6b9db57-7adc-4570-87bd-01968825644c
  Args:
    source: India Riven Oxenberg
    target: Catherine Oxenberg
    relation: :hasMother
  AssignClass (941f2a2f-9406-427c-a514-ea7b41a73dd4)
 Call ID: 941f2a2f-9406-427c-a514-ea7b41a73dd4
  Args:
    type: :Person
    source: William Weitz Shaffer
  AssignClass (1b115231-79fc-4063-a9f7-85e18ea6fb0e)
 Call ID: 1b115231-79fc-4063-a9f7-85e18ea6fb0e
  Args:
    type: :Man
    source: William Weitz Shaffer
  AddTriple (69110a4f-45ac-42fa-9abf-6c4e04b3c485)
 Call ID: 69110a4f-45ac-42fa-9abf-6c4e04b3c485
  Args:
    source: India Riven Oxenberg
    target: William Weitz Shaffer
    relation: :hasFather
  AssignClass (6593cb98-d08c-4422-a478-53cbd1f7ccd6)
 Call ID: 6593cb98-d08c-4422-a478-53cbd1f7ccd6
  Args:
    type: :Person
    source: Robert Evans
  AssignClass (24f3548b-bdad-487f-8f3d-e147b1677367)
 Call ID: 24f3548b-bdad-487f-8f3d-e147b1677367
  Args:
    type: :Man
    source: Robert Evans
  AddTriple (58cfacc7-eb73-4cc8-a47d-d36619bfe8e1)
 Call ID: 58cfacc7-eb73-4cc8-a47d-d36619bfe8e1
  Args:
    relation: :hasMarriageYear
    target: Robert Evans
    source: Catherine Oxenberg
  AddLiteral (22137840-d374-4d84-bb36-c0446b84bb0c)
 Call ID: 22137840-d374-4d84-bb36-c0446b84bb0c
  Args:
    source: Catherine Oxenberg
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 1998
  AssignClass (d56336b4-5716-4a7d-8cc2-4525fbfc20a6)
 Call ID: d56336b4-5716-4a7d-8cc2-4525fbfc20a6
  Args:
    type: :Person
    source: Casper Van Dien
  AssignClass (b6f947e6-a0fa-4617-a552-5495a9916e5a)
 Call ID: b6f947e6-a0fa-4617-a552-5495a9916e5a
  Args:
    type: :Man
    source: Casper Van Dien
  AssignClass (bdd4868c-d020-4f3e-a65a-d28be44a3660)
 Call ID: bdd4868c-d020-4f3e-a65a-d28be44a3660
  Args:
    type: :Person
    source: Ellis Jones
  AssignClass (937229b6-f958-4e5b-935d-973aef59cd37)
 Call ID: 937229b6-f958-4e5b-935d-973aef59cd37
  Args:
    type: :Man
    source: Ellis Jones
  AssignClass (0af08e93-4538-4003-8ecb-6c5330bc0bb1)
 Call ID: 0af08e93-4538-4003-8ecb-6c5330bc0bb1
  Args:
    type: :Person
    source: Grand Duchess Elena Vladimirovna of Russia
  AssignClass (bb925d5a-d394-477d-92ba-e06a0cd986a9)
 Call ID: bb925d5a-d394-477d-92ba-e06a0cd986a9
  Args:
    type: :Woman
    source: Grand Duchess Elena Vladimirovna of Russia
  AssignClass (fbd0cf2b-0d3e-4139-a05b-821adf3eff70)
 Call ID: fbd0cf2b-0d3e-4139-a05b-821adf3eff70
  Args:
    type: :Person
    source: Prince Nicholas of Greece and Denmark
  AssignClass (ff64c608-7341-4b76-8a57-7abc01812f12)
 Call ID: ff64c608-7341-4b76-8a57-7abc01812f12
  Args:
    type: :Man
    source: Prince Nicholas of Greece and Denmark
  AddTriple (1f33318c-fe84-479f-8ada-8e01aa561fd9)
 Call ID: 1f33318c-fe84-479f-8ada-8e01aa561fd9
  Args:
    relation: :hasMother
    target: Grand Duchess Elena Vladimirovna of Russia
    source: Princess Olga of Greece and Denmark
  AddTriple (82c9ab3b-b5b7-4392-b60e-9e8a4acb4058)
 Call ID: 82c9ab3b-b5b7-4392-b60e-9e8a4acb4058
  Args:
    target: Prince Nicholas of Greece and Denmark
    relation: :hasFather
    source: Princess Olga of Greece and Denmark
  AssignClass (548f1627-5787-47a3-b326-5ed585722a20)
 Call ID: 548f1627-5787-47a3-b326-5ed585722a20
  Args:
    type: :Person
    source: Queen Olga Konstantinovna of the Hellenes
  AssignClass (72cc8331-d463-476f-8bf4-21bdf09efe41)
 Call ID: 72cc8331-d463-476f-8bf4-21bdf09efe41
  Args:
    type: :Woman
    source: Queen Olga Konstantinovna of the Hellenes
  AssignClass (5f951988-ea94-4ca3-ae8f-86c7359fde84)
 Call ID: 5f951988-ea94-4ca3-ae8f-86c7359fde84
  Args:
    type: :Person
    source: King George of Greece
  AssignClass (5038263f-d926-4ae5-bc9b-7ccaf5374878)
 Call ID: 5038263f-d926-4ae5-bc9b-7ccaf5374878
  Args:
    type: :Man
    source: King George of Greece
  AddTriple (5faeb19b-ae2a-4570-ad1e-d3cb8619d10f)
 Call ID: 5faeb19b-ae2a-4570-ad1e-d3cb8619d10f
  Args:
    relation: :hasMother
    target: Queen Olga Konstantinovna of the Hellenes
    source: Prince Nicholas of Greece and Denmark
  AddTriple (1cac0d9a-9c80-47b7-b34e-d671648f685b)
 Call ID: 1cac0d9a-9c80-47b7-b34e-d671648f685b
  Args:
    relation: :hasFather
    target: King George of Greece
    source: Prince Nicholas of Greece and Denmark
  Finish (d30b26d1-9d1f-4dc0-a574-ce1547fb2e3d)
 Call ID: d30b26d1-9d1f-4dc0-a574-ce1547fb2e3d
  Args: