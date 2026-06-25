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
While there, she talked with her aunt Grand Duchess Elizabeth Feodorovna, who was formulating plans for the foundation of a religious order of nurses.
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
Prince Andrew, who had served as commander of the Second Army Corps during the war, was arrested.
Several former ministers and generals arrested at the same time were shot following a brief trial, and British diplomats assumed that Prince Andrew was also in mortal danger.
After a show trial, he was sentenced to banishment, and Prince and Princess Andrew and their children fled Greece aboard a British cruiser, HMS Calypso, under the protection of the British naval attaché, Commander Gerald Talbot.
Illness

The family settled in a small house loaned to them by Princess George of Greece and Denmark at Saint-Cloud, on the outskirts of Paris, where Princess Andrew helped in a charity shop for Greek refugees.
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
In a letter to her son, she admitted that in the last week before liberation she had had no food except bread and butter, and no meat for several months.
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
  AssignClass (126697e7-67b1-4b8b-b534-448893956905)
 Call ID: 126697e7-67b1-4b8b-b534-448893956905
  Args:
    source: :PrincessAliceOfBattenberg
    type: :Woman
  AssignClass (20744af9-e600-4873-ae0c-e66c5eec86e5)
 Call ID: 20744af9-e600-4873-ae0c-e66c5eec86e5
  Args:
    type: :Person
    source: :PrincessAliceOfBattenberg
  AddLiteral (6ae77646-b777-48b0-a5fe-08d46b0436f9)
 Call ID: 6ae77646-b777-48b0-a5fe-08d46b0436f9
  Args:
    source: :PrincessAliceOfBattenberg
    relation: :hasBirthYear
    literal_value: 1885
    literal_type: xsd:integer
  AddLiteral (dfadee63-82ea-4ee3-858c-e40963dee3ad)
 Call ID: dfadee63-82ea-4ee3-858c-e40963dee3ad
  Args:
    relation: :hasDeathYear
    source: :PrincessAliceOfBattenberg
    literal_value: 1969
    literal_type: xsd:integer
  AssignClass (3203dce1-a459-4a19-98d0-2641fa8efe69)
 Call ID: 3203dce1-a459-4a19-98d0-2641fa8efe69
  Args:
    type: :Man
    source: :PrincePhilip
  AssignClass (a8a1f776-719e-43d3-8926-07a6ec17308b)
 Call ID: a8a1f776-719e-43d3-8926-07a6ec17308b
  Args:
    source: :PrincePhilip
    type: :Person
  AddTriple (da307bfb-aaef-4162-88ea-9af316ca52a1)
 Call ID: da307bfb-aaef-4162-88ea-9af316ca52a1
  Args:
    relation: :isMotherOf
    source: :PrincessAliceOfBattenberg
    target: :PrincePhilip
  AssignClass (21f65cd4-da83-4f9a-8488-1a1f23d039d2)
 Call ID: 21f65cd4-da83-4f9a-8488-1a1f23d039d2
  Args:
    type: :Woman
    source: :QueenElizabethII
  AssignClass (33f50921-ed42-4a5d-92b6-14ece4f30cc1)
 Call ID: 33f50921-ed42-4a5d-92b6-14ece4f30cc1
  Args:
    source: :QueenElizabethII
    type: :Person
  AssignClass (d0bc8000-1f6f-4bd9-b3f8-11e8a0b53b28)
 Call ID: d0bc8000-1f6f-4bd9-b3f8-11e8a0b53b28
  Args:
    type: :Man
    source: :KingCharlesIII
  AssignClass (2d1f3935-1c44-4f8e-b93b-91a5f6df6ab4)
 Call ID: 2d1f3935-1c44-4f8e-b93b-91a5f6df6ab4
  Args:
    source: :KingCharlesIII
    type: :Person
  AddTriple (78335edc-df2f-4871-bf4e-59b8f71ccdf2)
 Call ID: 78335edc-df2f-4871-bf4e-59b8f71ccdf2
  Args:
    target: :KingCharlesIII
    source: :QueenElizabethII
    relation: :isMotherOf
  AddTriple (82fae061-bd7e-47d7-b4bd-0c1ff41bb70e)
 Call ID: 82fae061-bd7e-47d7-b4bd-0c1ff41bb70e
  Args:
    source: :PrincessAliceOfBattenberg
    relation: :isMotherOf
    target: :PrincePhilip
  AddTriple (ac8b738c-25ca-4f61-9846-22a87673a37b)
 Call ID: ac8b738c-25ca-4f61-9846-22a87673a37b
  Args:
    target: :PrincePhilip
    source: :KingCharlesIII
    relation: :hasFather
  AssignClass (cf24349f-78d7-4d49-98e7-988dc009abd8)
 Call ID: cf24349f-78d7-4d49-98e7-988dc009abd8
  Args:
    type: :Man
    source: :PrinceAndrewOfGreeceAndDenmark
  AssignClass (0aca23b4-f1da-4b08-913f-9e4d8dd557eb)
 Call ID: 0aca23b4-f1da-4b08-913f-9e4d8dd557eb
  Args:
    source: :PrinceAndrewOfGreeceAndDenmark
    type: :Person
  AddLiteral (808fd263-4f8d-4ea6-af15-10fa59141bca)
 Call ID: 808fd263-4f8d-4ea6-af15-10fa59141bca
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    source: :PrincessAliceOfBattenberg
    literal_value: 1903
  AddTriple (7857bb3d-a2e2-46af-af05-32fa06d4d93d)
 Call ID: 7857bb3d-a2e2-46af-af05-32fa06d4d93d
  Args:
    source: :PrincessAliceOfBattenberg
    relation: :isMotherOf
    target: :Margarita
  AddTriple (e8987625-8f38-4406-b264-25ca97d6f213)
 Call ID: e8987625-8f38-4406-b264-25ca97d6f213
  Args:
    target: :Theodora
    relation: :isMotherOf
    source: :PrincessAliceOfBattenberg
  AddTriple (223cd2df-6de2-4fc8-9ad8-98be2f708456)
 Call ID: 223cd2df-6de2-4fc8-9ad8-98be2f708456
  Args:
    target: :Cecilie
    source: :PrincessAliceOfBattenberg
    relation: :isMotherOf
  AddTriple (7802c792-35a5-4098-ad7a-66348d0ee882)
 Call ID: 7802c792-35a5-4098-ad7a-66348d0ee882
  Args:
    relation: :isMotherOf
    source: :PrincessAliceOfBattenberg
    target: :Sophie
  AddTriple (19f0806e-cb9e-4941-809c-fdc409309043)
 Call ID: 19f0806e-cb9e-4941-809c-fdc409309043
  Args:
    source: :PrincessAliceOfBattenberg
    relation: :isMotherOf
    target: :PrincePhilip
  AssignClass (624ac6e6-108e-4544-887e-8c3c3c2613e4)
 Call ID: 624ac6e6-108e-4544-887e-8c3c3c2613e4
  Args:
    type: :Woman
    source: :Margarita
  AssignClass (7b638b41-f70c-43c0-844a-241dd50661f1)
 Call ID: 7b638b41-f70c-43c0-844a-241dd50661f1
  Args:
    source: :Margarita
    type: :Person
  AssignClass (4aa5ff43-ba47-4676-8729-42752125d535)
 Call ID: 4aa5ff43-ba47-4676-8729-42752125d535
  Args:
    source: :Theodora
    type: :Woman
  AssignClass (f4187a7b-8da3-4af6-ba8f-36d95f18e82d)
 Call ID: f4187a7b-8da3-4af6-ba8f-36d95f18e82d
  Args:
    type: :Person
    source: :Theodora
  AssignClass (2da4762a-4d5e-4c30-ba58-56994b5b4262)
 Call ID: 2da4762a-4d5e-4c30-ba58-56994b5b4262
  Args:
    source: :Cecilie
    type: :Woman
  AssignClass (e4a1b672-471c-463d-8b9b-76aba108d28b)
 Call ID: e4a1b672-471c-463d-8b9b-76aba108d28b
  Args:
    source: :Cecilie
    type: :Person
  AssignClass (038df7ef-e07f-4384-b1ba-93bee28a19a0)
 Call ID: 038df7ef-e07f-4384-b1ba-93bee28a19a0
  Args:
    type: :Woman
    source: :Sophie
  AssignClass (7721e4f0-346f-4579-9749-600b48773d1b)
 Call ID: 7721e4f0-346f-4579-9749-600b48773d1b
  Args:
    source: :Sophie
    type: :Person
  AssignClass (ef41fe87-418a-4f4d-af8b-ee2ecbc01d9c)
 Call ID: ef41fe87-418a-4f4d-af8b-ee2ecbc01d9c
  Args:
    source: :PrinceLouisOfBattenberg
    type: :Man
  AssignClass (46f72678-1c9b-47ea-9573-b215bc88936d)
 Call ID: 46f72678-1c9b-47ea-9573-b215bc88936d
  Args:
    type: :Person
    source: :PrinceLouisOfBattenberg
  AssignClass (bf918177-31fe-463b-8e45-a169e759a623)
 Call ID: bf918177-31fe-463b-8e45-a169e759a623
  Args:
    type: :Woman
    source: :PrincessVictoriaOfHesseAndByRhine
  AssignClass (e6553071-e8b4-4457-b00c-95944bb92f83)
 Call ID: e6553071-e8b4-4457-b00c-95944bb92f83
  Args:
    source: :PrincessVictoriaOfHesseAndByRhine
    type: :Person
  AddTriple (3882e40d-15a8-4717-ba0f-4aba8961e77f)
 Call ID: 3882e40d-15a8-4717-ba0f-4aba8961e77f
  Args:
    source: :PrinceLouisOfBattenberg
    relation: :isFatherOf
    target: :PrincessAliceOfBattenberg
  AddTriple (96e10a80-a2f6-4a66-b881-b7ae702486ac)
 Call ID: 96e10a80-a2f6-4a66-b881-b7ae702486ac
  Args:
    target: :PrincessAliceOfBattenberg
    relation: :isMotherOf
    source: :PrincessVictoriaOfHesseAndByRhine
  AssignClass (25b10ce2-8705-4f00-80b2-6f0e02a7a872)
 Call ID: 25b10ce2-8705-4f00-80b2-6f0e02a7a872
  Args:
    type: :Woman
    source: :Louise
  AssignClass (86faadb8-fd05-4e3d-a94c-f1949ea52037)
 Call ID: 86faadb8-fd05-4e3d-a94c-f1949ea52037
  Args:
    source: :Louise
    type: :Person
  AssignClass (a83a4b88-5781-4a3c-aefe-3dce76eb6c05)
 Call ID: a83a4b88-5781-4a3c-aefe-3dce76eb6c05
  Args:
    type: :Man
    source: :George
  AssignClass (282fe2f5-eda1-43b2-9952-bb207c02dadb)
 Call ID: 282fe2f5-eda1-43b2-9952-bb207c02dadb
  Args:
    type: :Person
    source: :George
  AssignClass (f90c29fb-3fca-495d-9502-0f967b387976)
 Call ID: f90c29fb-3fca-495d-9502-0f967b387976
  Args:
    source: :Louis
    type: :Man
  AssignClass (7b6e858e-6136-46c3-96ea-7861bb551849)
 Call ID: 7b6e858e-6136-46c3-96ea-7861bb551849
  Args:
    type: :Person
    source: :Louis
  AddTriple (caa1f814-5677-4a15-bdf7-911dfd8762ed)
 Call ID: caa1f814-5677-4a15-bdf7-911dfd8762ed
  Args:
    target: :Louise
    source: :PrinceLouisOfBattenberg
    relation: :isFatherOf
  AddTriple (b136d3ab-03c7-48f9-bc8d-7a90ff515275)
 Call ID: b136d3ab-03c7-48f9-bc8d-7a90ff515275
  Args:
    target: :George
    relation: :isFatherOf
    source: :PrinceLouisOfBattenberg
  AddTriple (936ed23e-346f-4ea4-8ec3-d498f766ef93)
 Call ID: 936ed23e-346f-4ea4-8ec3-d498f766ef93
  Args:
    target: :Louis
    source: :PrinceLouisOfBattenberg
    relation: :isFatherOf
  AddTriple (76479088-40bb-479b-9f07-02d70776f7e1)
 Call ID: 76479088-40bb-479b-9f07-02d70776f7e1
  Args:
    relation: :isMotherOf
    source: :PrincessVictoriaOfHesseAndByRhine
    target: :Louise
  AddTriple (fdb6dcb4-c7b4-453e-a7c7-596a5e496f1c)
 Call ID: fdb6dcb4-c7b4-453e-a7c7-596a5e496f1c
  Args:
    source: :PrincessVictoriaOfHesseAndByRhine
    relation: :isMotherOf
    target: :George
  AddTriple (a3184b07-930e-4b69-9660-8910e15c601f)
 Call ID: a3184b07-930e-4b69-9660-8910e15c601f
  Args:
    source: :PrincessVictoriaOfHesseAndByRhine
    relation: :isMotherOf
    target: :Louis
  Finish (42cd4080-6c60-45da-b8a8-838350b55fcc)
 Call ID: 42cd4080-6c60-45da-b8a8-838350b55fcc
  Args: