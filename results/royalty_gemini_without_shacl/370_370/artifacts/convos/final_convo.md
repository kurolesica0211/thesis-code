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
Frederica of Hanover (German: Friederike Luise;
Greek: Φρειδερίκη Λουΐζα, romanized: Phreideríkē Louḯza; 18 April 1917 – 6 February 1981) was Queen of Greece from 1 April 1947 until 6 March 1964 as the wife of King Paul and Queen Mother of Greece from 6 March 1964, when her son Constantine II became King, until 8 December 1974, when the monarchy was officially abolished after a referendum.
Granddaughter of Kaiser Wilhelm II and daughter of Duke Ernest Augustus of Brunswick, Frederica was born a few months before the fall of the German Empire.
In Florence, she was received by Princess Helen of Greece and Denmark, at whose house she met the Crown Prince of Greece, Paul.
The two fell in love and married two years after the restoration of the monarchy in Greece.
In the years that followed, she gave birth to three children, Sophia in 1938, Constantine in 1940 and Irene in 1942.
During the Second World War, Greece was occupied by the Axis powers.
The Greek royal family left the country and Frederica and her children settled first in South Africa and from 1943 in Egypt.
The changing political situation in Greece, with the rise of the EAM and the KKE, challenged the institution of the monarchy.
In the period of civil war that followed, Frederica developed a strong social activity to support the efforts of the government and the Crown.
However, according to the prevailing historiographical view, she continued to influence the fate of the country through her son, now King Constantine II.
Frederica was widely regarded as Constantine's éminence grise and continued to be attacked by the opposition, who blamed her for the tensions between the palace and the government of Georgios Papandreou (1964–1965).
Early life

Born Her Royal Highness Friederike Luise, Princess of Hanover, Princess of Great Britain and Ireland, and Princess of Brunswick-Lüneburg on 18 April 1917 in Blankenburg am Harz, in the German Duchy of Brunswick, she was the only daughter and third child of Ernest Augustus, then reigning Duke of Brunswick, and his wife Princess Viktoria Luise of Prussia, herself the only daughter of the German Emperor Wilhelm II.
Both her father and maternal grandfather abdicated their thrones in November 1918 following Germany's defeat in World War I, while her paternal grandfather had been stripped of his British royal dukedom the previous year.
In 1933 Frederica joined the Jungmädelbund, the Nazi organisation for girls aged 10–14.
In 1934, Adolf Hitler, in his ambition to link the British and German royal houses, asked for Frederica's parents to arrange for the marriage of their seventeen-year-old daughter to the Prince of Wales.
In her memoirs, Frederica's mother described that she and her husband were "shattered" and such a possibility "had never entered our minds".
Victoria Louise herself had once been considered as a potential bride for the very same person prior to her marriage.
Moreover, the age difference was too great (the Prince of Wales was twenty-three years Frederica's senior), and her parents were unwilling to "put any such pressure" on their daughter.
Marriage

Prince Paul of Greece proposed to her during the summer of 1936, while he was in Berlin attending the 1936 Summer Olympics.
Paul was a son of King Constantine I and Frederica's great aunt Sophia.
Their engagement was announced officially on 28 September 1937, and Britain's King George VI gave his consent pursuant to the Royal Marriages Act 1772 on 26 December 1937.
Frederica became Hereditary Princess of Greece, her husband being heir presumptive to his childless elder brother, King George II.
Ten months after their marriage, their first child, the future Queen Sofía of Spain (and future mother of Felipe VI), was born on 2 November 1938.
On 2 June 1940, Frederica gave birth to the future King Constantine II.
War and exile

At the peak of World War II, in April 1941, the Greek royal family was evacuated to Crete in a Sunderland flying boat.
Frederica and her family were evacuated again, setting up a government-in-exile office in London.
In exile, King George II and the rest of the Greek royal family settled in South Africa.
Here Frederica's last child, Princess Irene, was born on 11 May 1942.
The Hereditary Prince and Princess returned to their villa in Psychiko.
Queen consort

On 1 April 1947, George II died and Frederica's husband ascended the throne as Paul I, with Frederica as queen consort.
A Communist insurgency in Northern Greece led to the Greek Civil War.
The King and Queen toured Northern Greece under tight security to appeal for loyalty in the summer of 1947.
Queen Frederica was constantly attacked for her German ancestry.
Left-wing politicians in Greece repeatedly used the fact that the Kaiser was her grandfather, and that she had brothers who were members of the SS, as propaganda against her.
When she was in London representing her sick husband at the wedding of his first cousin Prince Philip of Greece and Denmark to King George VI's elder daughter Princess Elizabeth in November 1947, Winston Churchill remarked on the Kaiser being her grandfather.
Queen Frederica had replied acknowledging the fact, but reminding him that she was also descended from Queen Victoria, and that her father would be the British king if the country had operated under Salic Law (allowing only males to inherit the crown).
In fact, Frederica held the title Princess of the United Kingdom of Great Britain and Ireland, granted ad personam to the children of the then-Duke of Brunswick by George V's letters patent of 1914, which remained unrevoked.
During the civil war, Queen Frederica set up the Queen's Camps or Child Cities (translation of: Παιδο(υ)πόλεις / Paidopoleis or Paidupoleis), a network of 53 camps around Greece where she would rescue children of members of the Democratic Army and former partisans.
The Greek Civil War ended in August 1949.
The King and Queen took this opportunity to strengthen the monarchy, and paid official visits to Marshal Josip Broz Tito in Belgrade, Presidents Luigi Einaudi of Italy in Rome, Theodor Heuss of West Germany, and Bechara El Khoury of Lebanon, Emperor Haile Selassie I of Ethiopia, Governor-General Chakravarthi Rajagopalachari of India, King George VI of the United Kingdom, and the United States as guest of President Dwight D. Eisenhower.
However, at home in Greece and abroad in the United Kingdom, Queen Frederica was targeted by the opposition, because as a girl she had belonged to the Bund Deutscher Mädel (League of German Girls), a branch of the Hitler Youth group for young women; her supporters argued that evading membership in the group would be difficult under the existing political climate in Nazi Germany at the time.
Unlike her meek husband, in post-War Greece Frederica was one of the most hated public figures.
Frederica has been described as "inherently undemocratic".
At home in Greece and abroad in the United Kingdom, she was targeted by the opposition.
Frederica's 16 November 1953 appearance in Life as America's guest was taken on one of the many state visits she paid around the world.
On 14 May 1962, her eldest daughter Sofía married Prince Juan Carlos of Spain (later King Juan Carlos I of Spain) in Athens.
Queen dowager

On 6 March 1964, King Paul died of cancer.
When her son, King Constantine II, married Princess Anne-Marie of Denmark later that year on 18 September, Queen Frederica stepped back from the majority of her public duties in favor of her daughter-in-law.
However, she continued to attend royal events that were family-oriented, such as the baptisms of her grandchildren in both Spain and Greece.
Exile

 King Constantine II's clashes with the democratically elected Prime Minister George Papandreou Sr. were blamed by critics for causing the destabilisation that led to a military coup on 21 April 1967 and the rise of the regime of the colonels.
Faced with a difficult situation, King Constantine initially collaborated with the military dictatorship,  swearing in their government under a royalist prime minister.
In 1971, Frederica published an autobiography, A Measure of Understanding.
The head of the junta became the new head-of-state as President of Greece George Papadopoulos.
A plebiscite was held on 8 December 1974 in which Constantine (who was able to campaign only from outside the country) freely admitted past errors, and promised to support democracy.
However, 69% of Greeks freely voted to make Greece a democratic republic.
Death

Frederica died on 6 February 1981 in exile in Madrid of heart failure, reportedly following eyelid surgery (blepharoplasty), although a biographer has claimed the surgery was cataract removal.
She was interred at Tatoi (the royal family's palace and burial ground in Greece).



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
  AssignClass (5027f3ed-fe9b-4ba6-aa59-0702575d00af)
 Call ID: 5027f3ed-fe9b-4ba6-aa59-0702575d00af
  Args:
    source: :Frederica_of_Hanover
    type: :Woman
  AssignClass (615a077c-c72c-483e-979e-c60eff58e672)
 Call ID: 615a077c-c72c-483e-979e-c60eff58e672
  Args:
    source: :Frederica_of_Hanover
    type: :Person
  AddLiteral (9f90034a-c089-4011-8e87-f4313078e8a5)
 Call ID: 9f90034a-c089-4011-8e87-f4313078e8a5
  Args:
    relation: :hasBirthYear
    source: :Frederica_of_Hanover
    literal_type: xsd:integer
    literal_value: 1917
  AddLiteral (aa8734a8-46c6-449c-b15e-a80521336519)
 Call ID: aa8734a8-46c6-449c-b15e-a80521336519
  Args:
    source: :Frederica_of_Hanover
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 1981
  AssignClass (b6ca9936-2a98-4fe9-99fa-f64ab3a95984)
 Call ID: b6ca9936-2a98-4fe9-99fa-f64ab3a95984
  Args:
    source: :Ernest_Augustus_of_Brunswick
    type: :Man
  AssignClass (8697ab4b-cad3-46ff-a769-20acab4ed8e3)
 Call ID: 8697ab4b-cad3-46ff-a769-20acab4ed8e3
  Args:
    source: :Ernest_Augustus_of_Brunswick
    type: :Person
  AssignClass (badc07d0-d059-4bd5-baee-97ecb4858349)
 Call ID: badc07d0-d059-4bd5-baee-97ecb4858349
  Args:
    source: :Viktoria_Luise_of_Prussia
    type: :Woman
  AssignClass (ee6466f8-a558-4fd5-b226-ae346d7c74ff)
 Call ID: ee6466f8-a558-4fd5-b226-ae346d7c74ff
  Args:
    source: :Viktoria_Luise_of_Prussia
    type: :Person
  AddTriple (2996bcf2-16f8-4f83-8eca-9fb3708cfdfb)
 Call ID: 2996bcf2-16f8-4f83-8eca-9fb3708cfdfb
  Args:
    target: :Ernest_Augustus_of_Brunswick
    source: :Frederica_of_Hanover
    relation: :hasFather
  AddTriple (40338e2c-893b-443e-961e-f9ad2197d95f)
 Call ID: 40338e2c-893b-443e-961e-f9ad2197d95f
  Args:
    target: :Viktoria_Luise_of_Prussia
    relation: :hasMother
    source: :Frederica_of_Hanover
  AssignClass (b7ec2725-5bfe-4bac-8127-505351039e71)
 Call ID: b7ec2725-5bfe-4bac-8127-505351039e71
  Args:
    source: :Wilhelm_II
    type: :Man
  AssignClass (94842ab3-3c34-455e-8a53-f8792c0d1cf8)
 Call ID: 94842ab3-3c34-455e-8a53-f8792c0d1cf8
  Args:
    source: :Wilhelm_II
    type: :Person
  AddTriple (02632a65-0017-498f-b961-2149068be08c)
 Call ID: 02632a65-0017-498f-b961-2149068be08c
  Args:
    target: :Wilhelm_II
    source: :Viktoria_Luise_of_Prussia
    relation: :hasFather
  AssignClass (8172c666-02c3-4396-bb2f-cc4ee12b5d20)
 Call ID: 8172c666-02c3-4396-bb2f-cc4ee12b5d20
  Args:
    source: :Paul_of_Greece
    type: :Man
  AssignClass (b70dbe2e-a61e-48c6-8490-ce0ad1a66dd7)
 Call ID: b70dbe2e-a61e-48c6-8490-ce0ad1a66dd7
  Args:
    source: :Paul_of_Greece
    type: :Person
  AddTriple (05c86808-949f-4b6e-ac35-35d97ed4c04c)
 Call ID: 05c86808-949f-4b6e-ac35-35d97ed4c04c
  Args:
    source: :Frederica_of_Hanover
    relation: :hasRelation
    target: :Paul_of_Greece
  AssignClass (0b7b4b8d-536b-45f4-a877-a86568d6b54b)
 Call ID: 0b7b4b8d-536b-45f4-a877-a86568d6b54b
  Args:
    source: :Sophia_of_Greece_and_Denmark
    type: :Woman
  AssignClass (9dd380c0-2929-4782-a62b-7d92cf3f37cc)
 Call ID: 9dd380c0-2929-4782-a62b-7d92cf3f37cc
  Args:
    source: :Sophia_of_Greece_and_Denmark
    type: :Person
  AddTriple (54c557ff-c69d-49ab-9638-b6a5ecb8ab2e)
 Call ID: 54c557ff-c69d-49ab-9638-b6a5ecb8ab2e
  Args:
    target: :Sophia_of_Greece_and_Denmark
    relation: :hasChild
    source: :Frederica_of_Hanover
  AddTriple (f3dd9903-426d-4b2f-80b1-824e58453cc6)
 Call ID: f3dd9903-426d-4b2f-80b1-824e58453cc6
  Args:
    relation: :hasMother
    source: :Sophia_of_Greece_and_Denmark
    target: :Frederica_of_Hanover
  AddTriple (8473fdfc-51aa-4f1d-b57d-97e0b338068b)
 Call ID: 8473fdfc-51aa-4f1d-b57d-97e0b338068b
  Args:
    target: :Paul_of_Greece
    source: :Sophia_of_Greece_and_Denmark
    relation: :hasFather
  AssignClass (abb437e7-2a82-48e5-bd98-5f15657b597d)
 Call ID: abb437e7-2a82-48e5-bd98-5f15657b597d
  Args:
    source: :Constantine_II_of_Greece
    type: :Man
  AssignClass (5074fa72-8223-41a8-b9d7-764e423e1ce7)
 Call ID: 5074fa72-8223-41a8-b9d7-764e423e1ce7
  Args:
    source: :Constantine_II_of_Greece
    type: :Person
  AddTriple (eb7d94c3-f323-450e-8303-6820d2e5a655)
 Call ID: eb7d94c3-f323-450e-8303-6820d2e5a655
  Args:
    relation: :hasChild
    source: :Frederica_of_Hanover
    target: :Constantine_II_of_Greece
  AddTriple (948d16ad-a2c0-4d26-8edc-a2d777241e21)
 Call ID: 948d16ad-a2c0-4d26-8edc-a2d777241e21
  Args:
    source: :Constantine_II_of_Greece
    relation: :hasMother
    target: :Frederica_of_Hanover
  AddTriple (e187f7ff-66c5-491d-a7b4-f2ca8a0ce5b3)
 Call ID: e187f7ff-66c5-491d-a7b4-f2ca8a0ce5b3
  Args:
    relation: :hasFather
    source: :Constantine_II_of_Greece
    target: :Paul_of_Greece
  AssignClass (0cef042f-6dd9-4d90-bb53-c081684584ee)
 Call ID: 0cef042f-6dd9-4d90-bb53-c081684584ee
  Args:
    source: :Irene_of_Greece_and_Denmark
    type: :Woman
  AssignClass (989dcb0e-f4c5-4437-87e1-b4ab6df2134a)
 Call ID: 989dcb0e-f4c5-4437-87e1-b4ab6df2134a
  Args:
    source: :Irene_of_Greece_and_Denmark
    type: :Person
  AddTriple (e84b30a3-6f7e-4c7c-b913-5832f4fc2157)
 Call ID: e84b30a3-6f7e-4c7c-b913-5832f4fc2157
  Args:
    source: :Frederica_of_Hanover
    relation: :hasChild
    target: :Irene_of_Greece_and_Denmark
  AddTriple (d4e95a1d-6664-4b1b-bbac-1f1688db5d1f)
 Call ID: d4e95a1d-6664-4b1b-bbac-1f1688db5d1f
  Args:
    relation: :hasMother
    source: :Irene_of_Greece_and_Denmark
    target: :Frederica_of_Hanover
  AddTriple (eefb2fbb-0991-41ca-8104-c4c4d3b6f56d)
 Call ID: eefb2fbb-0991-41ca-8104-c4c4d3b6f56d
  Args:
    target: :Paul_of_Greece
    relation: :hasFather
    source: :Irene_of_Greece_and_Denmark
  AssignClass (02de45c3-16e8-48c6-ad5b-ffde881c829f)
 Call ID: 02de45c3-16e8-48c6-ad5b-ffde881c829f
  Args:
    source: :Constantine_I_of_Greece
    type: :Man
  AssignClass (676e7ee4-3385-4583-b882-e5204237fe73)
 Call ID: 676e7ee4-3385-4583-b882-e5204237fe73
  Args:
    source: :Constantine_I_of_Greece
    type: :Person
  AddTriple (fb240431-9830-4514-9b39-27fb97d7fb4e)
 Call ID: fb240431-9830-4514-9b39-27fb97d7fb4e
  Args:
    target: :Constantine_I_of_Greece
    relation: :hasFather
    source: :Paul_of_Greece
  AssignClass (7aecf696-fa12-4a4e-a1ea-9a60e0589fa3)
 Call ID: 7aecf696-fa12-4a4e-a1ea-9a60e0589fa3
  Args:
    source: :Sophia_of_Prussia
    type: :Woman
  AssignClass (e6bb240c-4e44-454d-9c62-8097fa83b72d)
 Call ID: e6bb240c-4e44-454d-9c62-8097fa83b72d
  Args:
    source: :Sophia_of_Prussia
    type: :Person
  AddTriple (7f2a9034-1314-4005-8595-4599cd67080c)
 Call ID: 7f2a9034-1314-4005-8595-4599cd67080c
  Args:
    source: :Paul_of_Greece
    relation: :hasMother
    target: :Sophia_of_Prussia
  Finish (cda23450-5737-4e1d-9bdb-56b11791e035)
 Call ID: cda23450-5737-4e1d-9bdb-56b11791e035
  Args: