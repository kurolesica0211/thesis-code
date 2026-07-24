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
  AssignClass (882c4b55-4022-4df6-8378-27485ebc2e79)
 Call ID: 882c4b55-4022-4df6-8378-27485ebc2e79
  Args:
    type: :Man
    source: PhilipKarađorđević
  AssignClass (68658344-0274-4d52-89ed-b39c25abcb31)
 Call ID: 68658344-0274-4d52-89ed-b39c25abcb31
  Args:
    type: :Person
    source: PhilipKarađorđević
  AddLiteral (1aa9fd37-244a-4ace-b6b9-1bc50df9dfd9)
 Call ID: 1aa9fd37-244a-4ace-b6b9-1bc50df9dfd9
  Args:
    source: PhilipKarađorđević
    relation: :hasBirthYear
    literal_value: 1982
    literal_type: xsd:integer
  AssignClass (57c2a13f-05a9-4403-b917-74ff506cf6dc)
 Call ID: 57c2a13f-05a9-4403-b917-74ff506cf6dc
  Args:
    type: :Man
    source: AlexanderKarađorđević
  AssignClass (23edd351-63b7-431c-9dd4-44f76223d333)
 Call ID: 23edd351-63b7-431c-9dd4-44f76223d333
  Args:
    type: :Person
    source: AlexanderKarađorđević
  AssignClass (2f17cea4-adf9-447b-9ef7-de5e91305ee6)
 Call ID: 2f17cea4-adf9-447b-9ef7-de5e91305ee6
  Args:
    type: :Woman
    source: MariaDaGloria
  AssignClass (d1dd84cf-943e-40b3-92b4-2b5915dd6b20)
 Call ID: d1dd84cf-943e-40b3-92b4-2b5915dd6b20
  Args:
    type: :Person
    source: MariaDaGloria
  AddTriple (3677e2f6-b595-4528-9153-1394c4d9d297)
 Call ID: 3677e2f6-b595-4528-9153-1394c4d9d297
  Args:
    relation: :hasFather
    source: PhilipKarađorđević
    target: AlexanderKarađorđević
  AddTriple (781187e4-1a65-460f-9cbc-cd1bab14ba37)
 Call ID: 781187e4-1a65-460f-9cbc-cd1bab14ba37
  Args:
    source: PhilipKarađorđević
    target: MariaDaGloria
    relation: :hasMother
  AssignClass (2580fb29-f027-483a-92d0-8bea8912b5da)
 Call ID: 2580fb29-f027-483a-92d0-8bea8912b5da
  Args:
    type: :Man
    source: PeterKarađorđević
  AssignClass (64cb2255-7dfa-4e8e-a58e-0f0e97b3e585)
 Call ID: 64cb2255-7dfa-4e8e-a58e-0f0e97b3e585
  Args:
    type: :Person
    source: PeterKarađorđević
  AddTriple (97a4e953-48a1-43a3-9ffe-cd64b2c07653)
 Call ID: 97a4e953-48a1-43a3-9ffe-cd64b2c07653
  Args:
    relation: :isBrotherOf
    target: PeterKarađorđević
    source: PhilipKarađorđević
  AssignClass (8629ddbf-24c9-49f2-8a88-018a2b608603)
 Call ID: 8629ddbf-24c9-49f2-8a88-018a2b608603
  Args:
    type: :Woman
    source: DanicaMarinković
  AssignClass (73673b3f-365e-4a3e-9f31-097333c2cc89)
 Call ID: 73673b3f-365e-4a3e-9f31-097333c2cc89
  Args:
    type: :Person
    source: DanicaMarinković
  AddTriple (61ac472f-7892-478e-9445-724aabe0c3e2)
 Call ID: 61ac472f-7892-478e-9445-724aabe0c3e2
  Args:
    relation: :hasRelation
    source: PhilipKarađorđević
    target: DanicaMarinković
  AddLiteral (2e4317a5-e98b-4c3e-bd8c-6ce95f968359)
 Call ID: 2e4317a5-e98b-4c3e-bd8c-6ce95f968359
  Args:
    source: PhilipKarađorđević
    relation: :hasMarriageYear
    literal_value: 2017
    literal_type: xsd:integer
  AssignClass (857edf4c-a8df-4160-b68c-fd4e41fc8690)
 Call ID: 857edf4c-a8df-4160-b68c-fd4e41fc8690
  Args:
    type: :Man
    source: StefanKarađorđević
  AssignClass (804971a2-63cf-41d9-8e0c-77854a753232)
 Call ID: 804971a2-63cf-41d9-8e0c-77854a753232
  Args:
    type: :Person
    source: StefanKarađorđević
  AddTriple (30a31446-245e-4e7f-b32b-714a85d7a12f)
 Call ID: 30a31446-245e-4e7f-b32b-714a85d7a12f
  Args:
    relation: :hasFather
    source: StefanKarađorđević
    target: PhilipKarađorđević
  AddTriple (98ae8e58-517e-4817-8aff-d99641b5a138)
 Call ID: 98ae8e58-517e-4817-8aff-d99641b5a138
  Args:
    source: StefanKarađorđević
    target: DanicaMarinković
    relation: :hasMother
  AssignClass (715b24ae-7518-49c1-8119-d7735b42a0e0)
 Call ID: 715b24ae-7518-49c1-8119-d7735b42a0e0
  Args:
    type: :Woman
    source: MarijaKarađorđević
  AssignClass (9be84e05-a6be-4232-97d4-b2f964f3e331)
 Call ID: 9be84e05-a6be-4232-97d4-b2f964f3e331
  Args:
    type: :Person
    source: MarijaKarađorđević
  AddTriple (d878c6c7-68f5-4b00-a12b-c10a4644db67)
 Call ID: d878c6c7-68f5-4b00-a12b-c10a4644db67
  Args:
    relation: :hasFather
    source: MarijaKarađorđević
    target: PhilipKarađorđević
  AddTriple (2025ba9f-6264-4ca3-a52c-7e92523b4724)
 Call ID: 2025ba9f-6264-4ca3-a52c-7e92523b4724
  Args:
    relation: :hasMother
    source: MarijaKarađorđević
    target: DanicaMarinković
  Finish (46050019-ed07-4ba7-b85b-8058b152695e)
 Call ID: 46050019-ed07-4ba7-b85b-8058b152695e
  Args: