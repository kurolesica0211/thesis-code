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
Princess Alice of Battenberg (Victoria Alice Elizabeth Julia Marie; 25 February 1885 – 5 December 1969) was the mother of Prince Philip, Duke of Edinburgh, mother-in-law of Queen Elizabeth II, and paternal grandmother of King Charles III.
After marrying Prince Andrew of Greece and Denmark in 1903, she adopted the style of her husband, becoming Princess Andrew of Greece and Denmark.
A great-granddaughter of Queen Victoria, Alice was born at Windsor Castle and grew up in the United Kingdom, Germany and Malta.
A Hessian princess by birth, she was a member of the Battenberg family, a morganatic branch of the House of Hesse-Darmstadt.
She lived in Greece until the exile of most of the Greek royal family in 1917.
On returning to Greece a few years later, her husband was blamed in part for the country's defeat in the Greco-Turkish War (1919–1922), and the family was once again forced into exile until the restoration of the Greek monarchy in 1935.
In 1930, Princess Andrew was diagnosed with schizophrenia and committed to a sanatorium in Switzerland; thereafter, she lived separately from her husband.
After her recovery, she devoted most of her remaining years to charity work in Greece.
After the war, she stayed in Greece and founded a Greek Orthodox nursing order of nuns known as the Christian Sisterhood of Martha and Mary.
After the fall of King Constantine II of Greece and the imposition of military rule in Greece in 1967, Princess Andrew was invited by her son and daughter-in-law to live at Buckingham Palace in London, where she died two years later.
In 1988, her remains were transferred from a vault in her birthplace, Windsor Castle, to the Church of Mary Magdalene at the Russian Orthodox convent of the same name on the Mount of Olives in Jerusalem.
Early life

Alice was born at 4:40 pm on 25 February 1885 in the Tapestry Room at Windsor Castle, Berkshire, in the presence of her great-grandmother Queen Victoria.
She was the eldest child of Prince Louis of Battenberg and his wife, Princess Victoria of Hesse and by Rhine.
Her mother was the eldest daughter of Louis IV, Grand Duke of Hesse, and Princess Alice of the United Kingdom, the Queen's second daughter.
Her father was the eldest son of Prince Alexander of Hesse and by Rhine through his morganatic marriage to Countess Julia Hauke, who was created Princess of Battenberg in 1858 by Louis III, Grand Duke of Hesse.
Her three younger siblings, Louise, George, and Louis, later became Queen of Sweden, Marquess of Milford Haven, and Earl Mountbatten of Burma, respectively.
Alice was christened Victoria Alice Elizabeth Julia Marie in Darmstadt on 25 April.
She had six godparents: her three surviving grandparents, Grand Duke Louis IV of Hesse, Prince Alexander of Hesse and by Rhine, and Julia, Princess of Battenberg; her maternal aunt Grand Duchess Elizabeth Feodorovna of Russia; her paternal aunt Princess Marie of Erbach-Schönberg; and her maternal great-grandmother Queen Victoria.
Alice spent her childhood between Darmstadt, London, Jugenheim, and Malta (where her naval officer father was occasionally stationed).
Eventually, she was diagnosed with congenital deafness after her grandmother, the Princess of Battenberg, identified the problem and took her to see an ear specialist.
With encouragement from her mother, Alice learned to both lip-read and speak in English and German.
Her early years were spent in the company of her royal relatives, and she was a bridesmaid at the wedding of Prince George, Duke of York, and Princess Mary of Teck (later King George V and Queen Mary) in 1893.
A few weeks before her 16th birthday, she attended Queen Victoria's funeral in St George's Chapel, Windsor Castle, and shortly afterward she was confirmed in the Anglican faith.
Marriage

Alice met Prince Andrew of Greece and Denmark (known as Andrea within the family), the fourth son of King George I of Greece and Olga Constantinovna of Russia, while in London for King Edward VII's coronation in 1902.
She adopted the style of her husband, becoming "Princess Andrew".
The bride and groom were closely related to the ruling houses of the United Kingdom, Germany, Russia, Denmark, and Greece, and their wedding was one of the great gatherings of the descendants of Queen Victoria and King Christian IX held before World War I. Prince and Princess Andrew had five children: Margarita, Theodora, Cecilie, Sophie, and Philip.
After their wedding, Prince Andrew continued his career in the military and Princess Andrew became involved in charity work.
In 1908, she visited Russia for the wedding of Grand Duchess Marie of Russia and Prince William of Sweden.
Princess Andrew attended the laying of the foundation stone for her aunt's new church.
Later in the year, Elizabeth began giving away all her possessions in preparation for a more spiritual life.
On their return to Greece, Prince and Princess Andrew found the political situation worsening, as the Athens government had refused to support the Cretan parliament, which had called for the union of Crete (still nominally part of the Ottoman Empire) with the Greek mainland.
A group of dissatisfied officers formed a Greek nationalist Military League that eventually led to Prince Andrew's resignation from the army and the rise to power of Eleftherios Venizelos.
Successive life crises

With the advent of the Balkan Wars, Prince Andrew was reinstated in the army, and Princess Andrew acted as a nurse, assisting at operations and setting up field hospitals, work for which King George V awarded her the Royal Red Cross in 1913.
During World War I, her brother-in-law King Constantine I of Greece followed a neutrality policy despite the democratically elected government of Venizelos supporting the Allies.
Princess Andrew and her children were forced to shelter in the palace cellars during the French bombardment of Athens on 1 December 1916.
By June 1917, the King's neutrality policy had become so untenable that she and other members of the Greek royal family were forced into exile when King Constantine abdicated.
For the next few years, most of the Greek royal family lived in Switzerland.
The naval career of Princess Andrew's father, Prince Louis of Battenberg, had collapsed at the beginning of the war in the face of anti-German sentiment in Britain.
At the request of King George V, he relinquished the Hessian title Prince of Battenberg and the style of Serene Highness on 14 July 1917, and anglicized the family name to Mountbatten.
The following year, two of Princess Andrew's aunts, Empress Alexandra Feodorovna of Russia and Grand Duchess Elizabeth Feodorovna, were murdered by Bolsheviks after the Russian Revolution.
At the end of the war the Russian, German and Austro-Hungarian empires had fallen, and Princess Andrew's uncle Ernest Louis, Grand Duke of Hesse, was deposed.
On Constantine's restoration in 1920, Prince and Princess Andrew briefly returned to Greece, taking up residence on Corfu at Mon Repos (inherited by Prince Andrew on his father's assassination in 1913).
But after the defeat of the Hellenic Army in the Greco-Turkish War, a Revolutionary Committee under the leadership of Colonels Nikolaos Plastiras and Stylianos Gonatas seized power and forced King Constantine into exile once again.
Prince Andrew, who had served as commander of the Second Army Corps during the war, was arrested.
Several former ministers and generals arrested at the same time were shot following a brief trial, and British diplomats assumed that Prince Andrew was also in mortal danger.
After a show trial, he was sentenced to banishment, and Prince and Princess Andrew and their children fled Greece aboard a British cruiser, HMS Calypso, under the protection of the British naval attaché, Commander Gerald Talbot.
Illness

The family settled in a small house loaned to them by Princess George of Greece and Denmark at Saint-Cloud, on the outskirts of Paris, where Princess Andrew helped in a charity shop for Greek refugees.
In 1930, her behaviour became increasingly erratic, and she asserted that she was in communication with the Buddha and Christ.
She was diagnosed with paranoid schizophrenia, first by Thomas Ross, a psychiatrist specialising in the treatment of shell shock, and subsequently by Sir Maurice Craig, who had treated the future King George VI before he had speech therapy.
It was a famous and well-respected institution with several celebrity patients, including Vaslav Nijinsky, the ballet dancer and choreographer, who was there at the same time as the princess.
Both he and Simmel sought advice from Sigmund Freud, who concluded that the delusions derived from sexual frustration and suggested "X-raying her ovaries in order to kill off her libido."
During Princess Andrew's long convalescence, she and Prince Andrew drifted apart, her daughters all married German princes in 1930 and 1931 (she did not attend any of the weddings), and Prince Philip went to the United Kingdom to stay with his maternal uncles, Lord Louis Mountbatten and George Mountbatten, 2nd Marquess of Milford Haven, and his maternal grandmother, the Dowager Marchioness of Milford Haven.
Princess Andrew remained at Kreuzlingen for two years, but after a brief stay at a clinic in Merano in northern Italy, was released and began an itinerant, incognito existence in Central Europe.
In 1937, her daughter Cecilie, her son-in-law Georg, and two of her grandchildren were killed in an air accident at Ostend; she and Prince Andrew met for the first time in six years at the funeral.
(Prince Philip and Lord Louis Mountbatten also attended.)
She resumed contact with her family, and in 1938 returned to Athens alone to work with the poor, while living in a two-bedroom flat near the Benaki Museum.
World War II

During World War II, Princess Andrew was in the difficult situation of having sons-in-law fighting on the German side and a son in the British Royal Navy.
Her cousin, Prince Victor zu Erbach-Schönberg, was the German ambassador in Greece until the occupation of Athens by Axis forces in April 1941.
She and her sister-in-law, Princess Nicholas of Greece, lived in Athens for the duration of the war, while most of the Greek royal family remained in exile in South Africa.
She moved out of her small flat and into her brother-in-law George's three-storey house in the centre of Athens.
She worked for the Red Cross, helped organise soup kitchens for the starving populace and flew to Sweden to bring back medical supplies on the pretext of visiting her sister, Crown Princess Louise.
The occupying forces apparently presumed Princess Andrew was pro-German, as one of her sons-in-law, Prince Christoph of Hesse, was a member of the NSDAP and the Waffen-SS, and another, Berthold, Margrave of Baden, had been invalided out of the German army in 1940 after an injury in France.
During this period, Princess Andrew hid Jewish widow Rachel Cohen and two of her five children, who sought to evade the Gestapo and deportation to the death camps.
In 1913, Rachel's husband, Haimaki Cohen, had aided King George I of Greece.
In return, King George had offered him any service that he could perform should Cohen ever need it.
Years later, during the Nazi threat, Cohen's son remembered this, and appealed to Princess Andrew, who, with Princess Nicholas, was one of only two remaining members of the royal family left in Greece.
Princess Andrew honoured the promise and saved the Cohen family.
When Athens was liberated in October 1944, Harold Macmillan visited Princess Andrew and described her as "living in humble, not to say somewhat squalid conditions".
As the fighting continued, Princess Andrew was informed that her husband had died, just as hopes of a post-war reunion of the couple were rising.
So, why worry about that?"


Widowhood

Princess Andrew returned to the United Kingdom in April 1947 to attend the November wedding of her only son, Philip, to Princess Elizabeth, the elder daughter and heir presumptive of King George VI.
She had some of her remaining jewels used in Princess Elizabeth's engagement ring.
On the day of the wedding, her son was created Duke of Edinburgh by George VI.
For the wedding ceremony, Princess Andrew sat at the head of her family on the north side of Westminster Abbey, opposite the King, Queen Elizabeth and Queen Mary.
Princess Andrew's daughters were not invited to the wedding because of anti-German sentiment in Britain following World War II.
In January 1949, the princess founded a nursing order of Greek Orthodox nuns, the Christian Sisterhood of Martha and Mary, modelled after the convent that her aunt, the martyr Grand Duchess Elizabeth Feodorovna, had founded in Russia in 1909.
Princess Andrew's daughter-in-law became queen of the Commonwealth realms in 1952, and the princess attended the new queen's coronation in June 1953 wearing a two-tone grey dress and wimple in the style of a nun's habit.
In 1960, she visited India at the invitation of Rajkumari Amrit Kaur, who had been impressed by Princess Andrew's interest in Indian religious thought, and for her own spiritual quest.
The trip was cut short when she unexpectedly took ill, and her sister-in-law, Edwina Mountbatten, Countess Mountbatten of Burma, who happened to be passing through Delhi on her own tour, had to smooth things with the Indian hosts who were taken aback at Princess Andrew's sudden change of plans.
Edwina continued her own tour, and died the following month.
Increasingly deaf and in failing health, Princess Andrew left Greece for the last time following the 21 April 1967 Colonels' Coup.
Queen Elizabeth II and Prince Philip invited Princess Andrew to reside permanently at Buckingham Palace in London.
King Constantine II and Queen Anne-Marie of Greece went into exile that December after a failed royalist counter-coup.
Death and burial

Despite suggestions of senility in later life, Princess Andrew remained lucid but physically frail.
She died at Buckingham Palace on 5 December 1969, aged 84.
Initially her remains were placed in the Royal Crypt in St George's Chapel at Windsor Castle on 10 December, but before she died she had expressed her wish to be buried at the Convent of Saint Mary Magdalene in Gethsemane on the Mount of Olives in Jerusalem (near her aunt Grand Duchess Elizabeth Feodorovna).
When her daughter Princess George William of Hanover complained that it would be too far away for them to visit her grave, Princess Andrew jested, "Nonsense, there's a perfectly good bus service!"
On 31 October 1994, Princess Andrew's two surviving children, the Duke of Edinburgh and Princess George of Hanover, went to Yad Vashem (the Holocaust Memorial) in Jerusalem to witness a ceremony honouring her as "Righteous Among the Nations" for having hidden the Cohens in her house in Athens during the Second World War.
Prince Philip said of his mother's sheltering of persecuted Jews, "I suspect that it never occurred to her that her action was in any way special.
In 2010, the princess was posthumously named a Hero of the Holocaust by the British Government.



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
  AssignClass (c6f27215-9e91-4538-8bf8-7c90e0806acb)
 Call ID: c6f27215-9e91-4538-8bf8-7c90e0806acb
  Args:
    source: Alice_of_Battenberg
    type: :Woman
  AssignClass (0b97c291-3491-4fb8-a115-4bfc623ce5fe)
 Call ID: 0b97c291-3491-4fb8-a115-4bfc623ce5fe
  Args:
    type: :Person
    source: Alice_of_Battenberg
  AssignClass (9ccd9b9d-2d41-431b-8308-af5260509c7e)
 Call ID: 9ccd9b9d-2d41-431b-8308-af5260509c7e
  Args:
    type: :Ancestor
    source: Alice_of_Battenberg
  AssignClass (05149c61-b97d-436d-82f3-d33d23fde27f)
 Call ID: 05149c61-b97d-436d-82f3-d33d23fde27f
  Args:
    type: :Man
    source: Philip_Duke_of_Edinburgh
  AssignClass (f302fe3e-6a9a-4329-beaa-dc19bc03a290)
 Call ID: f302fe3e-6a9a-4329-beaa-dc19bc03a290
  Args:
    type: :Person
    source: Philip_Duke_of_Edinburgh
  AssignClass (e1725820-10c4-4ed4-a3bc-264c59646c5d)
 Call ID: e1725820-10c4-4ed4-a3bc-264c59646c5d
  Args:
    type: :Man
    source: Andrew_of_Greece_and_Denmark
  AssignClass (8676aad9-090e-4d68-9c2d-2505134cc78c)
 Call ID: 8676aad9-090e-4d68-9c2d-2505134cc78c
  Args:
    source: Andrew_of_Greece_and_Denmark
    type: :Person
  AssignClass (ebda3842-6615-4f4f-aebc-9cdb9d96f2a8)
 Call ID: ebda3842-6615-4f4f-aebc-9cdb9d96f2a8
  Args:
    type: :Ancestor
    source: Andrew_of_Greece_and_Denmark
  AssignClass (6a6fc38c-5ef0-4ad1-b4d5-61eaa0dd9285)
 Call ID: 6a6fc38c-5ef0-4ad1-b4d5-61eaa0dd9285
  Args:
    source: Louis_of_Battenberg
    type: :Man
  AssignClass (147769e4-8b07-488c-a250-78fb4a2edfb3)
 Call ID: 147769e4-8b07-488c-a250-78fb4a2edfb3
  Args:
    type: :Person
    source: Louis_of_Battenberg
  AssignClass (f26d0493-ad20-4315-938e-40363b1d810c)
 Call ID: f26d0493-ad20-4315-938e-40363b1d810c
  Args:
    type: :Ancestor
    source: Louis_of_Battenberg
  AssignClass (0f5b6c47-8634-443b-bce6-0883bd995a8c)
 Call ID: 0f5b6c47-8634-443b-bce6-0883bd995a8c
  Args:
    type: :Woman
    source: Victoria_of_Hesse_and_by_Rhine
  AssignClass (773608a2-022b-4a94-a547-2fa647f4a930)
 Call ID: 773608a2-022b-4a94-a547-2fa647f4a930
  Args:
    source: Victoria_of_Hesse_and_by_Rhine
    type: :Person
  AssignClass (e0199ff8-43e1-44ae-b62d-bca535058774)
 Call ID: e0199ff8-43e1-44ae-b62d-bca535058774
  Args:
    source: Victoria_of_Hesse_and_by_Rhine
    type: :Ancestor
  AssignClass (7ec483d2-0f58-48c0-91f1-40235ad60ccb)
 Call ID: 7ec483d2-0f58-48c0-91f1-40235ad60ccb
  Args:
    source: Louis_IV_Grand_Duke_of_Hesse
    type: :Man
  AssignClass (d155874e-f1fb-4829-b1b0-41dad2c81872)
 Call ID: d155874e-f1fb-4829-b1b0-41dad2c81872
  Args:
    source: Louis_IV_Grand_Duke_of_Hesse
    type: :Person
  AssignClass (ffb89093-14a8-403d-b595-216d65ecddac)
 Call ID: ffb89093-14a8-403d-b595-216d65ecddac
  Args:
    source: Louis_IV_Grand_Duke_of_Hesse
    type: :Ancestor
  AssignClass (1b78ca89-8593-4081-919a-1d87a2ac8fda)
 Call ID: 1b78ca89-8593-4081-919a-1d87a2ac8fda
  Args:
    source: Alice_of_the_United_Kingdom
    type: :Woman
  AssignClass (741cf884-32d8-4f29-89f3-19ea047b4872)
 Call ID: 741cf884-32d8-4f29-89f3-19ea047b4872
  Args:
    source: Alice_of_the_United_Kingdom
    type: :Person
  AssignClass (c7c70023-d398-4585-a6a2-4ef9cc256c8f)
 Call ID: c7c70023-d398-4585-a6a2-4ef9cc256c8f
  Args:
    source: Alice_of_the_United_Kingdom
    type: :Ancestor
  AssignClass (e03d041c-9472-4d7c-bc10-36e5d800d3f8)
 Call ID: e03d041c-9472-4d7c-bc10-36e5d800d3f8
  Args:
    source: Alexander_of_Hesse_and_by_Rhine
    type: :Man
  AssignClass (f5fdce54-1cae-42f6-9da0-037081170f59)
 Call ID: f5fdce54-1cae-42f6-9da0-037081170f59
  Args:
    source: Alexander_of_Hesse_and_by_Rhine
    type: :Person
  AssignClass (104b0332-e628-42a1-8ef1-f06244ff84d4)
 Call ID: 104b0332-e628-42a1-8ef1-f06244ff84d4
  Args:
    source: Alexander_of_Hesse_and_by_Rhine
    type: :Ancestor
  AssignClass (3a1a7ba8-0ad9-4f4f-9902-66cdccb54d4a)
 Call ID: 3a1a7ba8-0ad9-4f4f-9902-66cdccb54d4a
  Args:
    type: :Woman
    source: Julia_Hauke
  AssignClass (dc0be6e6-466f-45f5-af69-93d11cf57427)
 Call ID: dc0be6e6-466f-45f5-af69-93d11cf57427
  Args:
    type: :Person
    source: Julia_Hauke
  AssignClass (17687afd-c67f-403e-ab78-7e2752fb08b4)
 Call ID: 17687afd-c67f-403e-ab78-7e2752fb08b4
  Args:
    type: :Ancestor
    source: Julia_Hauke
  AssignClass (d5ab7523-bc45-4fbd-a5ff-a9cb8fbb6a61)
 Call ID: d5ab7523-bc45-4fbd-a5ff-a9cb8fbb6a61
  Args:
    type: :Woman
    source: Louise_of_Battenberg
  AssignClass (dbf978a5-dc35-4375-a872-a84d08ea00c4)
 Call ID: dbf978a5-dc35-4375-a872-a84d08ea00c4
  Args:
    source: Louise_of_Battenberg
    type: :Person
  AssignClass (bd525ad6-402a-4565-aa88-82edb94a4ee0)
 Call ID: bd525ad6-402a-4565-aa88-82edb94a4ee0
  Args:
    source: George_of_Battenberg
    type: :Man
  AssignClass (0d0f9310-2b02-4061-baed-280fdb84f3f7)
 Call ID: 0d0f9310-2b02-4061-baed-280fdb84f3f7
  Args:
    source: George_of_Battenberg
    type: :Person
  AssignClass (573c2e1b-992d-47c8-b59f-ba5814756c81)
 Call ID: 573c2e1b-992d-47c8-b59f-ba5814756c81
  Args:
    type: :Man
    source: Louis_Mountbatten
  AssignClass (9c5a6306-703c-40d6-863b-3e61def23ed3)
 Call ID: 9c5a6306-703c-40d6-863b-3e61def23ed3
  Args:
    source: Louis_Mountbatten
    type: :Person
  AssignClass (e71ba3cf-d35a-4084-b6ce-654ae0fb0120)
 Call ID: e71ba3cf-d35a-4084-b6ce-654ae0fb0120
  Args:
    type: :Woman
    source: Margarita_of_Greece_and_Denmark
  AssignClass (d9033989-b355-41db-b104-3fa7de3e2e24)
 Call ID: d9033989-b355-41db-b104-3fa7de3e2e24
  Args:
    type: :Person
    source: Margarita_of_Greece_and_Denmark
  AssignClass (9b27f04f-ab06-41a0-8cf8-68a4ab97cab6)
 Call ID: 9b27f04f-ab06-41a0-8cf8-68a4ab97cab6
  Args:
    source: Theodora_of_Greece_and_Denmark
    type: :Woman
  AssignClass (9288f776-d94b-4c0a-91cd-1f74cc399b21)
 Call ID: 9288f776-d94b-4c0a-91cd-1f74cc399b21
  Args:
    type: :Person
    source: Theodora_of_Greece_and_Denmark
  AssignClass (5989827f-df83-496e-84fb-df6b77d6cc21)
 Call ID: 5989827f-df83-496e-84fb-df6b77d6cc21
  Args:
    source: Cecilie_of_Greece_and_Denmark
    type: :Woman
  AssignClass (3fbba7be-6984-4d4a-b46f-bd88c2c98be2)
 Call ID: 3fbba7be-6984-4d4a-b46f-bd88c2c98be2
  Args:
    source: Cecilie_of_Greece_and_Denmark
    type: :Person
  AssignClass (3d7d9678-c5e2-4853-9f9b-c642510b2a26)
 Call ID: 3d7d9678-c5e2-4853-9f9b-c642510b2a26
  Args:
    source: Sophie_of_Greece_and_Denmark
    type: :Woman
  AssignClass (c1b4b1dd-0447-4340-8b3f-87958521f473)
 Call ID: c1b4b1dd-0447-4340-8b3f-87958521f473
  Args:
    source: Sophie_of_Greece_and_Denmark
    type: :Person
  AssignClass (73d43307-58f8-4748-910f-c79c2c4d5017)
 Call ID: 73d43307-58f8-4748-910f-c79c2c4d5017
  Args:
    source: George_I_of_Greece
    type: :Man
  AssignClass (e73b1ec2-b3b2-4e9a-9d43-393728b487e3)
 Call ID: e73b1ec2-b3b2-4e9a-9d43-393728b487e3
  Args:
    type: :Person
    source: George_I_of_Greece
  AssignClass (c103a472-5ef2-495b-8ff4-248db410c9f3)
 Call ID: c103a472-5ef2-495b-8ff4-248db410c9f3
  Args:
    source: George_I_of_Greece
    type: :Ancestor
  AssignClass (2999d1f2-8d5b-46d8-ae04-879b31e689b9)
 Call ID: 2999d1f2-8d5b-46d8-ae04-879b31e689b9
  Args:
    type: :Woman
    source: Olga_Constantinovna_of_Russia
  AssignClass (bad03fd1-c06d-4bfb-9115-bc06c6ac0a88)
 Call ID: bad03fd1-c06d-4bfb-9115-bc06c6ac0a88
  Args:
    type: :Person
    source: Olga_Constantinovna_of_Russia
  AssignClass (c3ddfdf7-edea-432b-9f3a-eafc9ce07ded)
 Call ID: c3ddfdf7-edea-432b-9f3a-eafc9ce07ded
  Args:
    type: :Ancestor
    source: Olga_Constantinovna_of_Russia
  AddLiteral (1761b92d-fa45-4b26-9c0d-10b22423d981)
 Call ID: 1761b92d-fa45-4b26-9c0d-10b22423d981
  Args:
    literal_value: Female
    relation: :hasSex
    source: Alice_of_Battenberg
    literal_type: xsd:string
  AddLiteral (ab47a92b-4c7c-4882-8f80-2f31e49bc575)
 Call ID: ab47a92b-4c7c-4882-8f80-2f31e49bc575
  Args:
    literal_value: 1885
    source: Alice_of_Battenberg
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (7e8558d1-b51c-40f8-845c-78d69028782d)
 Call ID: 7e8558d1-b51c-40f8-845c-78d69028782d
  Args:
    literal_value: 1969
    source: Alice_of_Battenberg
    relation: :hasDeathYear
    literal_type: xsd:integer
  AddLiteral (afc446e4-5bc3-4bbf-8f55-efe1442ea30b)
 Call ID: afc446e4-5bc3-4bbf-8f55-efe1442ea30b
  Args:
    literal_type: xsd:integer
    source: Alice_of_Battenberg
    relation: :hasMarriageYear
    literal_value: 1903
  AddTriple (4f3db388-225c-454b-a705-4ecec0b6cced)
 Call ID: 4f3db388-225c-454b-a705-4ecec0b6cced
  Args:
    source: Alice_of_Battenberg
    relation: :hasFather
    target: Louis_of_Battenberg
  AddTriple (1b64a6e1-c4e9-455a-80f0-503ff3e2fc45)
 Call ID: 1b64a6e1-c4e9-455a-80f0-503ff3e2fc45
  Args:
    target: Victoria_of_Hesse_and_by_Rhine
    source: Alice_of_Battenberg
    relation: :hasMother
  AddTriple (db4277d1-6733-4df3-8747-445a21fcd138)
 Call ID: db4277d1-6733-4df3-8747-445a21fcd138
  Args:
    relation: :hasFather
    source: Victoria_of_Hesse_and_by_Rhine
    target: Louis_IV_Grand_Duke_of_Hesse
  AddTriple (b7d89ab9-21f9-48fb-aec8-3b15ee1b4756)
 Call ID: b7d89ab9-21f9-48fb-aec8-3b15ee1b4756
  Args:
    target: Alice_of_the_United_Kingdom
    relation: :hasMother
    source: Victoria_of_Hesse_and_by_Rhine
  AddTriple (6eeb9553-9565-4727-a9b8-fea50fca78b4)
 Call ID: 6eeb9553-9565-4727-a9b8-fea50fca78b4
  Args:
    source: Louis_of_Battenberg
    relation: :hasFather
    target: Alexander_of_Hesse_and_by_Rhine
  AddTriple (ece0018f-87ba-41b5-88e5-209eae02afb5)
 Call ID: ece0018f-87ba-41b5-88e5-209eae02afb5
  Args:
    target: Julia_Hauke
    source: Louis_of_Battenberg
    relation: :hasMother
  AddTriple (8dc02c3a-7609-46ff-b86f-0a4ef5945e30)
 Call ID: 8dc02c3a-7609-46ff-b86f-0a4ef5945e30
  Args:
    relation: :hasBrother
    source: Alice_of_Battenberg
    target: George_of_Battenberg
  AddTriple (40b7058c-da9a-4314-accf-9ad7ad357242)
 Call ID: 40b7058c-da9a-4314-accf-9ad7ad357242
  Args:
    target: Louis_Mountbatten
    relation: :hasBrother
    source: Alice_of_Battenberg
  AddTriple (14e7bd73-0778-40a5-bf19-ff8747579e20)
 Call ID: 14e7bd73-0778-40a5-bf19-ff8747579e20
  Args:
    target: Louise_of_Battenberg
    relation: :hasSister
    source: Alice_of_Battenberg
  AddTriple (71d4a663-6e6e-449c-b90e-3112f41a9b42)
 Call ID: 71d4a663-6e6e-449c-b90e-3112f41a9b42
  Args:
    target: Philip_Duke_of_Edinburgh
    source: Alice_of_Battenberg
    relation: :hasSon
  AddTriple (cce3a6d2-c836-4516-af78-841d7b0cd25a)
 Call ID: cce3a6d2-c836-4516-af78-841d7b0cd25a
  Args:
    target: Margarita_of_Greece_and_Denmark
    source: Alice_of_Battenberg
    relation: :hasDaughter
  AddTriple (bac9364e-770d-4ddb-9590-bf7f44febdd1)
 Call ID: bac9364e-770d-4ddb-9590-bf7f44febdd1
  Args:
    relation: :hasDaughter
    source: Alice_of_Battenberg
    target: Theodora_of_Greece_and_Denmark
  AddTriple (a982f63f-a89d-4687-b023-fecfe5498f42)
 Call ID: a982f63f-a89d-4687-b023-fecfe5498f42
  Args:
    relation: :hasDaughter
    source: Alice_of_Battenberg
    target: Cecilie_of_Greece_and_Denmark
  AddTriple (f280c821-d25c-4248-8bab-77ab5ca95c2e)
 Call ID: f280c821-d25c-4248-8bab-77ab5ca95c2e
  Args:
    source: Alice_of_Battenberg
    relation: :hasDaughter
    target: Sophie_of_Greece_and_Denmark
  AddTriple (0b17db20-01a3-448b-94e2-b3b6aef87e8b)
 Call ID: 0b17db20-01a3-448b-94e2-b3b6aef87e8b
  Args:
    target: Andrew_of_Greece_and_Denmark
    relation: :hasFather
    source: Philip_Duke_of_Edinburgh
  AddTriple (aab8fa01-84e5-4f45-b4db-4cdb635c9989)
 Call ID: aab8fa01-84e5-4f45-b4db-4cdb635c9989
  Args:
    target: Alice_of_Battenberg
    source: Philip_Duke_of_Edinburgh
    relation: :hasMother
  AddTriple (35ddcf34-d822-486c-8808-724f89f6b0c8)
 Call ID: 35ddcf34-d822-486c-8808-724f89f6b0c8
  Args:
    target: George_I_of_Greece
    relation: :hasFather
    source: Andrew_of_Greece_and_Denmark
  AddTriple (bd2d55bb-0005-42ce-91b4-7c1adf5a4f35)
 Call ID: bd2d55bb-0005-42ce-91b4-7c1adf5a4f35
  Args:
    relation: :hasMother
    source: Andrew_of_Greece_and_Denmark
    target: Olga_Constantinovna_of_Russia
  Finish (d49d3202-3e74-41b0-bd8b-98f5ec72188a)
 Call ID: d49d3202-3e74-41b0-bd8b-98f5ec72188a
  Args: