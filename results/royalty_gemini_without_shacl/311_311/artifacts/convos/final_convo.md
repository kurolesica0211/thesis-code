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
The Crown PrinceThe Crown Princess


Princess Tomislav


Princess Alexander


Princess Elizabeth


Filip Karađorđević (Serbian Cyrillic: Филип Карађорђевић; born 15 January 1982), sometimes referred to in English as Prince Philip Karageorgevitch and unofficially titled Philip, Hereditary Prince of Serbia and Yugoslavia (Serbian Cyrillic: Филип, принц наследник од Србије и Југославије, Filip, princ naslednik od Srbije i Jugoslavije), is a Serbian business manager, a member of the House of Karađorđević, and heir apparent to Crown Prince Alexander.
In 2020, he moved to his homeland Serbia and took a more active role in public life, often travelling across Serbia, Kosovo, Montenegro, and Bosnia.
In 2022, he became the hereditary prince, following his elder brother's renunciation.
Early life and education

Prince Philip was born on 15 January 1982 in Vienna, Virginia, as the second son and second child of the last Crown Prince of the former Kingdom of Yugoslavia, Alexander, and his first wife, Princess Maria da Gloria of Orléans-Braganza, the eldest daughter of Pedro Gastão of Orléans-Braganza, a claimant to the defunct Brazilian throne, and Princess Maria de la Esperanza of Bourbon-Two Sicilies (1914–2005), a maternal aunt of King Juan Carlos I of Spain.
Philip is the fraternal twin of Alexander.
His godparents are Queen Sofía of Spain, King Constantine II of Greece (both first cousins of his paternal grandmother), and Princess Anne, Duchess of Calabria (first cousin of his mother).
Philip lived in Virginia until 1984.
Philip's parents divorced in 1985.
After the divorce, his father remarried Katherine Clairy Batis later that year, while his mother remarried Ignacio, Duke of Segorbe, member of the House of Medinaceli, later that year.
Philip has two younger half-sisters through his mother, Sol María de la Blanca Medina y Orléans-Braganza, 54th Countess of Ampurias (b. 1986) and Ana Luna Medina y Orléans-Braganza, 17th Countess of Ricla (b. 1988).
Together with his twin brother, Philip was educated in London and Canterbury.
In June 2000, Philip completed sixth form at The King's School, Canterbury, obtaining three A levels and ten GCSEs.
In 1991, Philip, with his father and brothers, briefly visited Belgrade, Yugoslavia.
In February 2001, the Parliament of FR Yugoslavia passed legislation conferring citizenship on members of the Karađorđević family, making Philip eligible for Yugoslav citizenship.
In July 2001, his father and step-mother moved to Belgrade, Serbia, FR Yugoslavia.
After the dissolution of FR Yugoslavia (later renamed Serbia and Montenegro), Philip obtained citizenship of Serbia.
Personal life

After completing his studies, Philip started to work for financial institutions in the City of London.
Most recently, Philip has been working with a renowned global asset manager in London.
Philip lived and worked in London until 2020, when he relocated to Serbia and started to work remotely following the COVID-19 pandemic in Europe.
Philip completed the 2010 Athens Marathon, the 2011 Belgrade Half-marathon, and the 2014 London Marathon.
Marriage and children

On 24 July 2017, his parents announced his engagement to Danica Marinković.
Philip married Danica Marinković on 7 October 2017 at the Cathedral Church of Saint Michael the Archangel in Belgrade, Serbia.
Their witnesses were Victoria, the Crown Princess of Sweden and his brother Peter.
His two godmothers, Queen Sofía of Spain and Princess Anne, Duchess of Calabria, attended the wedding.
It was the first royal wedding in Serbia since the 1922 wedding of his great-grandfather King Alexander I and Princess Maria of Romania.
Several members of royal families also attended, including Prince Guillaume of Luxembourg with his wife, Prince Amyn Aga Khan, Princess Jeet Nabha Khemka, and guests of the Karađorđević Royal Family and the Marinković family, including the president of the National Assembly of Serbia Maja Gojković among others.
Princess Danica gave birth to their son, Prince Stefan, in Belgrade on 25 February 2018 at 10:30 am.
Stefan is the first male child born to the royal family on Serbian soil for 90 years, the last such birth being that of Prince Tomislav in Belgrade in 1928.
On 5 November 2023 in Belgrade, Philip and Danica welcomed their second child, a daughter.
They named her Princess Marija.
Public life

Prince Philip attended the reburial of his grandparents, King Peter II and Queen Alexandra, great-grandmother Queen Maria, and granduncle Prince Andrew in the Royal Family Mausoleum at Oplenac on 26 May 2013.
The Serbian Royal Regalia were placed over King Peter's coffin, having Philip placed the Royal Orb and Sceptre near the Karađorđević Crown.
On 17 July 2015, Prince Philip and his brothers attended their father's 70th birthday celebration in Royal Compound, Belgrade.
Prince in Serbia (2020–2022)
Philip used to live in London with his family, a wife and a son, but as of July 2020, they relocated and currently live in Belgrade, Serbia.
With his relocation to Serbia, Philip fulfilled the promise he gave to Serbian Patriarch Irinej to do so.
In January 2020, Prince Philip voiced support for the clerical protests in Montenegro.
On 22 November 2020, Philip and his wife, Princess Danica, were the only members of the House of Karađorđević who attended the funeral service of Patriarch Irinej at the Church of Saint Sava.
Prince Philip and his wife were also the only members of the House of Karađorđević who attended the enthronement of newly elected Patriarch Porfirije  on 19 February 2021 in St. Michael's Cathedral in Belgrade.
In April 2021, before Easter, Philip visited Kosovo to support the Serbian community there.
On 13 September 2021, Philip and his wife, Princess Danica, attended Holy Liturgy led by Patriarch Porfirije in the Jasenovac Monastery in Croatia and visited the Jasenovac concentration camp and Stone Flower sculpture, becoming the first members of the House of Karađorđević who visited this memorial site from World War II.
In December 2021, Philip voiced support for the environmental protests in Serbia.
In February 2022, Philip and his wife travelled to Han Pijesak, Bosnia and Herzegovina.
Devastated by time, the summer house will be rebuilt and renovated as Prince Philip has agreed with local authorities and the Government of Republika Srpska to fund it.
Furthermore, on 10 February, Prince Philip and his wife met with Milorad Dodik, a Serb member of the Presidency of Bosnia and Herzegovina.
On 21 March 2022, Philip and his wife signed the People's initiative to ban the exploitation of lithium and boron in Serbia.
Hereditary Prince (2022–present)

On 27 April 2022, his elder brother Prince Peter renounced the title of a hereditary prince – for himself and his descendants.
Philip became the Hereditary Prince of Serbia and Yugoslavia, heir apparent to his father, Alexander.
The ceremony took place at Casa de Pilatos in Seville, Spain, in the presence of his mother, Princess Maria da Gloria, his stepfather Duke Ignacio, his wife Princess Danica, his half-sister Countess Sol, Ljubodrag Grujić, a member of the Crown Council, Chancellor of the Orders and the Herald of the House of Karađorđević and Nikola Stanković, Chief of Staff of the Crown Prince.
His father, Crown Prince Alexander, did not attend the event.
The Crown Prince was dissatisfied with Peter's renunciation.
A grandson of King Alexander I of Yugoslavia, Prince Michael, supported the act.
On 5 May 2022, Philip and his wife attended mass at the Cathedral of Saint-Louis des Invalides in Paris in honour of Napoleon I and soldiers of the Grande Armée who died for France, by invitation from his cousin Jean-Christophe, Prince Napoléon, a descendant of Napoleon, and his wife, Princess Olympia.
Afterwards, they travelled to Mileševa Monastery in southwest Serbia and Pljevlja, Montenegro, attending the Holy Liturgy in Mileševa led by Patriarch Porfirije and Metropolitan Joanikije II of Montenegro and the Littoral.
In the first week of June 2022, Philip and his family travelled to Kosovo, visiting Gazimestan, Gračanica Monastery, Prizren (Church of the Holy Saviour and Monastery of the Holy Archangels), Priština (St. Nicholas Church), and Visoki Dečani Monastery.
Furthermore, Prince Philip gave a copy of Prince Peter's renunciation paper to the library of Visoki Dečani Monastery.
On 11 September 2022, Philip and his wife attended a march from Loznica to the top of Gučevo mountain in honour of soldiers fallen in the Battle of the Drina in September 1914.
In May 2023, Philip and his wife attended the Serbia Against Violence protests in Belgrade, following the Belgrade school shooting and a mass murder near Mladenovac and Smederevo.
Arms

Ancestry

Philip is a member of the House of Karađorđević.
Through his father, Philip descends from kings Nicholas I of Montenegro, Ferdinand I of Romania, Christian IX of Denmark, and Alexander of Greece, and furthermore from emperors Nicholas I of Russia and Frederick III of the Germans and Queen Victoria of the United Kingdom of Great Britain and Ireland.
Through his mother, Philip descends from the Emperor Pedro II of Brazil, and kings Louis Philippe I of France and Francis I of the Two Sicilies, and furthermore from Francis I, Holy Roman Emperor and his Empress Maria Theresa, and king Charles III of Spain.



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
  AssignClass (aefd02fe-8e02-4b97-a266-03f48ee3844e)
 Call ID: aefd02fe-8e02-4b97-a266-03f48ee3844e
  Args:
    source: Philip_Karađorđević
    type: :Man
  AssignClass (6593337c-3bf5-4a18-8c09-911d285f3f4a)
 Call ID: 6593337c-3bf5-4a18-8c09-911d285f3f4a
  Args:
    type: :Person
    source: Philip_Karađorđević
  AddLiteral (d8b23a44-fbb4-4fab-bf3d-47c0a042eb87)
 Call ID: d8b23a44-fbb4-4fab-bf3d-47c0a042eb87
  Args:
    relation: :hasBirthYear
    literal_value: 1982
    literal_type: xsd:integer
    source: Philip_Karađorđević
  AssignClass (32d7f7ab-a199-4335-b9ba-9cf117c03a9b)
 Call ID: 32d7f7ab-a199-4335-b9ba-9cf117c03a9b
  Args:
    source: Alexander_Karađorđević
    type: :Man
  AssignClass (7bc78b3d-ab30-4d06-92e8-481d9e375078)
 Call ID: 7bc78b3d-ab30-4d06-92e8-481d9e375078
  Args:
    type: :Person
    source: Alexander_Karađorđević
  AssignClass (a1aed534-b455-4a68-af28-dfe2d3bf122b)
 Call ID: a1aed534-b455-4a68-af28-dfe2d3bf122b
  Args:
    source: Maria_da_Gloria
    type: :Woman
  AssignClass (1039689b-b26f-45f1-9f0c-3198a19dcc4e)
 Call ID: 1039689b-b26f-45f1-9f0c-3198a19dcc4e
  Args:
    type: :Person
    source: Maria_da_Gloria
  AddTriple (5573e65e-12ea-490b-b27b-9c901c0fa332)
 Call ID: 5573e65e-12ea-490b-b27b-9c901c0fa332
  Args:
    relation: :hasFather
    target: Alexander_Karađorđević
    source: Philip_Karađorđević
  AddTriple (ddd38a14-ad01-4c38-94a7-4784117da3cc)
 Call ID: ddd38a14-ad01-4c38-94a7-4784117da3cc
  Args:
    relation: :hasMother
    target: Maria_da_Gloria
    source: Philip_Karađorđević
  AssignClass (2985202f-9f0b-41f0-9e25-e9ac5854999a)
 Call ID: 2985202f-9f0b-41f0-9e25-e9ac5854999a
  Args:
    source: Danica_Marinković
    type: :Woman
  AssignClass (ed2522c9-66a4-41f5-b8fb-015d915752e6)
 Call ID: ed2522c9-66a4-41f5-b8fb-015d915752e6
  Args:
    source: Danica_Marinković
    type: :Person
  AddTriple (47579199-613d-4375-b57f-b812c1895962)
 Call ID: 47579199-613d-4375-b57f-b812c1895962
  Args:
    source: Philip_Karađorđević
    target: Danica_Marinković
    relation: :hasRelation
  AssignClass (4bca9788-9f27-4999-9284-4cc3541da26d)
 Call ID: 4bca9788-9f27-4999-9284-4cc3541da26d
  Args:
    type: :Man
    source: Stefan_Karađorđević
  AssignClass (dc49c1d6-6cad-46ad-b2f6-d8675685156d)
 Call ID: dc49c1d6-6cad-46ad-b2f6-d8675685156d
  Args:
    source: Stefan_Karađorđević
    type: :Person
  AddTriple (11f57960-c11f-4629-a805-c25f5e24134e)
 Call ID: 11f57960-c11f-4629-a805-c25f5e24134e
  Args:
    relation: :hasFather
    source: Stefan_Karađorđević
    target: Philip_Karađorđević
  AddTriple (09caa6e7-ac70-4cb6-9536-9759def3b0ab)
 Call ID: 09caa6e7-ac70-4cb6-9536-9759def3b0ab
  Args:
    relation: :hasMother
    target: Danica_Marinković
    source: Stefan_Karađorđević
  AssignClass (ffaa369d-17ac-493d-8616-a7e646ab88ea)
 Call ID: ffaa369d-17ac-493d-8616-a7e646ab88ea
  Args:
    type: :Woman
    source: Marija_Karađorđević
  AssignClass (dd2b0f1d-349e-4195-8d44-ba20831395c8)
 Call ID: dd2b0f1d-349e-4195-8d44-ba20831395c8
  Args:
    type: :Person
    source: Marija_Karađorđević
  AddTriple (92c4b124-a607-49b3-9cfd-cfae0b95a8be)
 Call ID: 92c4b124-a607-49b3-9cfd-cfae0b95a8be
  Args:
    relation: :hasFather
    target: Philip_Karađorđević
    source: Marija_Karađorđević
  AddTriple (dd66b60f-ded8-4f30-98f5-f9df9af8415a)
 Call ID: dd66b60f-ded8-4f30-98f5-f9df9af8415a
  Args:
    relation: :hasMother
    source: Marija_Karađorđević
    target: Danica_Marinković
  AssignClass (ead14525-95da-4e9c-b6b8-61cdad669e7c)
 Call ID: ead14525-95da-4e9c-b6b8-61cdad669e7c
  Args:
    type: :Man
    source: Peter_Karađorđević
  AssignClass (65883634-4299-4c41-a33b-69952fe08427)
 Call ID: 65883634-4299-4c41-a33b-69952fe08427
  Args:
    source: Peter_Karađorđević
    type: :Person
  AddTriple (8cb7a2fe-1076-4245-9758-c00e65640b11)
 Call ID: 8cb7a2fe-1076-4245-9758-c00e65640b11
  Args:
    relation: :hasBrother
    source: Philip_Karađorđević
    target: Peter_Karađorđević
  AddTriple (0e045347-e546-426f-ac10-03a7d3d9de42)
 Call ID: 0e045347-e546-426f-ac10-03a7d3d9de42
  Args:
    source: Peter_Karađorđević
    target: Alexander_Karađorđević
    relation: :hasFather
  AddTriple (120b244d-8aa6-4464-8ac0-ae4e1a5aac9f)
 Call ID: 120b244d-8aa6-4464-8ac0-ae4e1a5aac9f
  Args:
    target: Maria_da_Gloria
    source: Peter_Karađorđević
    relation: :hasMother
  AssignClass (92df9ef6-1044-4532-ae88-6acd09ee851a)
 Call ID: 92df9ef6-1044-4532-ae88-6acd09ee851a
  Args:
    source: Sol_María_de_la_Blanca_Medina_y_Orléans-Braganza
    type: :Woman
  AssignClass (367f4d37-35a6-443b-b851-9a0bb51a397b)
 Call ID: 367f4d37-35a6-443b-b851-9a0bb51a397b
  Args:
    source: Sol_María_de_la_Blanca_Medina_y_Orléans-Braganza
    type: :Person
  AssignClass (45d643f7-f598-4e6e-baa2-2686d76184ff)
 Call ID: 45d643f7-f598-4e6e-baa2-2686d76184ff
  Args:
    type: :Woman
    source: Ana_Luna_Medina_y_Orléans-Braganza
  AssignClass (be738a2c-496f-4684-825a-f5fcbc996a3c)
 Call ID: be738a2c-496f-4684-825a-f5fcbc996a3c
  Args:
    source: Ana_Luna_Medina_y_Orléans-Braganza
    type: :Person
  AddTriple (0865cf31-8546-45c4-a640-e322e22b7e36)
 Call ID: 0865cf31-8546-45c4-a640-e322e22b7e36
  Args:
    relation: :hasMother
    target: Maria_da_Gloria
    source: Sol_María_de_la_Blanca_Medina_y_Orléans-Braganza
  AddTriple (3b2a19f1-85e1-4117-be6d-202b8effd9b1)
 Call ID: 3b2a19f1-85e1-4117-be6d-202b8effd9b1
  Args:
    relation: :hasMother
    source: Ana_Luna_Medina_y_Orléans-Braganza
    target: Maria_da_Gloria
  Finish (01266e9b-a1de-4ea3-8491-3f41ec415b17)
 Call ID: 01266e9b-a1de-4ea3-8491-3f41ec415b17
  Args: