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
  AssignClass (0b51ec00-330b-4422-9965-abdb8dcd22eb)
 Call ID: 0b51ec00-330b-4422-9965-abdb8dcd22eb
  Args:
    source: Filip_Karadjordjevic
    type: :Man
  AssignClass (908c72fc-0aff-4e67-a938-f9a0e017be5a)
 Call ID: 908c72fc-0aff-4e67-a938-f9a0e017be5a
  Args:
    type: :Person
    source: Filip_Karadjordjevic
  AddLiteral (04543585-95f5-47e0-be87-0a5928055626)
 Call ID: 04543585-95f5-47e0-be87-0a5928055626
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Filip_Karadjordjevic
    literal_value: 1982
  AssignClass (8fa03e33-3fc4-45f6-a733-dc90c62a65cb)
 Call ID: 8fa03e33-3fc4-45f6-a733-dc90c62a65cb
  Args:
    type: :Man
    source: Alexander_Karadjordjevic
  AssignClass (0c19e882-5c0a-4eb0-9d28-fd7e44de7d1e)
 Call ID: 0c19e882-5c0a-4eb0-9d28-fd7e44de7d1e
  Args:
    type: :Person
    source: Alexander_Karadjordjevic
  AssignClass (a504e34a-775d-4923-840b-5c7070aa3229)
 Call ID: a504e34a-775d-4923-840b-5c7070aa3229
  Args:
    source: Maria_da_Gloria
    type: :Woman
  AssignClass (76eb8dec-13c7-46c3-ab7f-c131d837b202)
 Call ID: 76eb8dec-13c7-46c3-ab7f-c131d837b202
  Args:
    type: :Person
    source: Maria_da_Gloria
  AddTriple (06316dae-d7b5-4fd8-a36b-7a50b6b055db)
 Call ID: 06316dae-d7b5-4fd8-a36b-7a50b6b055db
  Args:
    relation: :hasFather
    target: Alexander_Karadjordjevic
    source: Filip_Karadjordjevic
  AddTriple (87a3533b-10ee-4fbf-bd48-383c769659b4)
 Call ID: 87a3533b-10ee-4fbf-bd48-383c769659b4
  Args:
    relation: :hasMother
    source: Filip_Karadjordjevic
    target: Maria_da_Gloria
  AssignClass (8c455a51-a880-4fc1-a145-219cdff2ddbd)
 Call ID: 8c455a51-a880-4fc1-a145-219cdff2ddbd
  Args:
    type: :Man
    source: Peter_Karadjordjevic
  AssignClass (03d2830b-2136-4b3f-a66e-d2569c42f7af)
 Call ID: 03d2830b-2136-4b3f-a66e-d2569c42f7af
  Args:
    type: :Person
    source: Peter_Karadjordjevic
  AddTriple (a3d99393-dfd0-4e21-9f2f-bcf503233195)
 Call ID: a3d99393-dfd0-4e21-9f2f-bcf503233195
  Args:
    source: Filip_Karadjordjevic
    target: Peter_Karadjordjevic
    relation: :isBrotherOf
  AssignClass (6590bc03-d177-4782-b8ac-44534c9990d7)
 Call ID: 6590bc03-d177-4782-b8ac-44534c9990d7
  Args:
    source: Danica_Marinkovic
    type: :Woman
  AssignClass (8d79248a-44bc-484c-aea0-bae692dc3668)
 Call ID: 8d79248a-44bc-484c-aea0-bae692dc3668
  Args:
    source: Danica_Marinkovic
    type: :Person
  AddTriple (87e725a3-b515-4650-b2bc-88025ca0d933)
 Call ID: 87e725a3-b515-4650-b2bc-88025ca0d933
  Args:
    target: Danica_Marinkovic
    source: Filip_Karadjordjevic
    relation: :hasRelation
  AddLiteral (ce98c0f8-d5e9-46a9-b831-2e941e5fc0cc)
 Call ID: ce98c0f8-d5e9-46a9-b831-2e941e5fc0cc
  Args:
    literal_value: 2017
    source: Filip_Karadjordjevic
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AssignClass (114d5d5a-7243-463a-8d26-23f04e24bdbe)
 Call ID: 114d5d5a-7243-463a-8d26-23f04e24bdbe
  Args:
    source: Stefan_Karadjordjevic
    type: :Man
  AssignClass (41d6bb49-f818-49b5-a334-eebda8222c85)
 Call ID: 41d6bb49-f818-49b5-a334-eebda8222c85
  Args:
    type: :Person
    source: Stefan_Karadjordjevic
  AddTriple (ff363617-5ff3-4b3c-bdd6-c2e9417a2e8c)
 Call ID: ff363617-5ff3-4b3c-bdd6-c2e9417a2e8c
  Args:
    source: Stefan_Karadjordjevic
    target: Filip_Karadjordjevic
    relation: :isSonOf
  AddTriple (2d2f9e04-7f35-46b4-ac50-7d907fcb15ac)
 Call ID: 2d2f9e04-7f35-46b4-ac50-7d907fcb15ac
  Args:
    relation: :isSonOf
    target: Danica_Marinkovic
    source: Stefan_Karadjordjevic
  AssignClass (ffc4c89a-3206-41bd-afee-31ccf2633090)
 Call ID: ffc4c89a-3206-41bd-afee-31ccf2633090
  Args:
    type: :Woman
    source: Marija_Karadjordjevic
  AssignClass (496f1e08-27ee-4738-9f0d-669f2693f65c)
 Call ID: 496f1e08-27ee-4738-9f0d-669f2693f65c
  Args:
    source: Marija_Karadjordjevic
    type: :Person
  AddTriple (7bc4483c-1b88-4fc3-9031-a106fd77e520)
 Call ID: 7bc4483c-1b88-4fc3-9031-a106fd77e520
  Args:
    relation: :isDaughterOf
    target: Filip_Karadjordjevic
    source: Marija_Karadjordjevic
  AddTriple (e1fa03aa-7203-497a-b177-6860ec74f6ac)
 Call ID: e1fa03aa-7203-497a-b177-6860ec74f6ac
  Args:
    relation: :isDaughterOf
    target: Danica_Marinkovic
    source: Marija_Karadjordjevic
  AssignClass (596b62de-7b5d-4b8a-9dd1-d206e1f2b363)
 Call ID: 596b62de-7b5d-4b8a-9dd1-d206e1f2b363
  Args:
    source: Katherine_Clairy_Batis
    type: :Woman
  AssignClass (0b89ffac-2f74-4aa9-840d-2857a49c2e21)
 Call ID: 0b89ffac-2f74-4aa9-840d-2857a49c2e21
  Args:
    type: :Person
    source: Katherine_Clairy_Batis
  AssignClass (d8838e41-c5e3-4533-9a46-844f2daee3e4)
 Call ID: d8838e41-c5e3-4533-9a46-844f2daee3e4
  Args:
    source: Ignacio_Duke_of_Segorbe
    type: :Man
  AssignClass (0f10fbb8-e713-4f02-bd85-34a8016cfa59)
 Call ID: 0f10fbb8-e713-4f02-bd85-34a8016cfa59
  Args:
    type: :Person
    source: Ignacio_Duke_of_Segorbe
  AssignClass (3d3cce99-7555-43ae-8b7d-273aa5de250f)
 Call ID: 3d3cce99-7555-43ae-8b7d-273aa5de250f
  Args:
    type: :Woman
    source: Sol_Maria_de_la_Blanca_Medina_y_Orleans_Braganza
  AssignClass (7532326f-5b4f-4ccc-979e-df74c6eb64b7)
 Call ID: 7532326f-5b4f-4ccc-979e-df74c6eb64b7
  Args:
    type: :Person
    source: Sol_Maria_de_la_Blanca_Medina_y_Orleans_Braganza
  AssignClass (6cceeefb-658f-48dc-9b6a-0b5256d41cf7)
 Call ID: 6cceeefb-658f-48dc-9b6a-0b5256d41cf7
  Args:
    source: Ana_Luna_Medina_y_Orleans_Braganza
    type: :Woman
  AssignClass (07f5917e-c0f9-459f-b280-dc7f6ca0ef2b)
 Call ID: 07f5917e-c0f9-459f-b280-dc7f6ca0ef2b
  Args:
    source: Ana_Luna_Medina_y_Orleans_Braganza
    type: :Person
  AddTriple (33b15b5d-c3cb-4b3e-8322-8d187b9be65b)
 Call ID: 33b15b5d-c3cb-4b3e-8322-8d187b9be65b
  Args:
    source: Sol_Maria_de_la_Blanca_Medina_y_Orleans_Braganza
    target: Maria_da_Gloria
    relation: :hasMother
  AddTriple (3b0e6ba2-1f95-4bbd-9679-ce773e4ac43e)
 Call ID: 3b0e6ba2-1f95-4bbd-9679-ce773e4ac43e
  Args:
    target: Maria_da_Gloria
    source: Ana_Luna_Medina_y_Orleans_Braganza
    relation: :hasMother
  AddTriple (80f7a5a5-33ee-4137-95d5-709278db3086)
 Call ID: 80f7a5a5-33ee-4137-95d5-709278db3086
  Args:
    relation: :hasFather
    target: Ignacio_Duke_of_Segorbe
    source: Sol_Maria_de_la_Blanca_Medina_y_Orleans_Braganza
  AddTriple (e3ebb15f-e854-4c61-8117-8666385ccb8d)
 Call ID: e3ebb15f-e854-4c61-8117-8666385ccb8d
  Args:
    relation: :hasFather
    target: Ignacio_Duke_of_Segorbe
    source: Ana_Luna_Medina_y_Orleans_Braganza
  Finish (a3c053eb-173b-48ef-8d6f-b149eeb44e89)
 Call ID: a3c053eb-173b-48ef-8d6f-b149eeb44e89
  Args: