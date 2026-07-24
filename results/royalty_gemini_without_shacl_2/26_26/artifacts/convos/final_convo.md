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
  AssignClass (99e97ef2-4746-4adf-a02c-cb57114b59b6)
 Call ID: 99e97ef2-4746-4adf-a02c-cb57114b59b6
  Args:
    type: :Woman
    source: Alice_of_Battenberg
  AssignClass (f68f1fbc-f221-4cc9-a5a9-ef78ebea57de)
 Call ID: f68f1fbc-f221-4cc9-a5a9-ef78ebea57de
  Args:
    type: :Ancestor
    source: Alice_of_Battenberg
  AddLiteral (c7922a1b-6a50-488d-8786-d89443a9c1fd)
 Call ID: c7922a1b-6a50-488d-8786-d89443a9c1fd
  Args:
    source: Alice_of_Battenberg
    relation: :hasBirthYear
    literal_value: 1885
    literal_type: xsd:integer
  AddLiteral (db331412-1d96-43dc-a47d-5e6215fbc4d7)
 Call ID: db331412-1d96-43dc-a47d-5e6215fbc4d7
  Args:
    source: Alice_of_Battenberg
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 1969
  AssignClass (08ab48f6-7181-4ad5-a35c-3c59dba21df2)
 Call ID: 08ab48f6-7181-4ad5-a35c-3c59dba21df2
  Args:
    type: :Man
    source: Prince_Philip
  AssignClass (eb894150-1b46-46df-8ffe-a60d37252fca)
 Call ID: eb894150-1b46-46df-8ffe-a60d37252fca
  Args:
    type: :Person
    source: Prince_Philip
  AddTriple (bde7dcfc-efa8-42dc-8a98-ef67e19035aa)
 Call ID: bde7dcfc-efa8-42dc-8a98-ef67e19035aa
  Args:
    target: Alice_of_Battenberg
    relation: :isSonOf
    source: Prince_Philip
  AddTriple (15e7eb77-0e68-4be6-874f-f79ae026b50d)
 Call ID: 15e7eb77-0e68-4be6-874f-f79ae026b50d
  Args:
    source: Alice_of_Battenberg
    target: Prince_Philip
    relation: :isMotherOf
  AssignClass (48cc28a6-ed68-47ff-a98c-da3024643ee5)
 Call ID: 48cc28a6-ed68-47ff-a98c-da3024643ee5
  Args:
    type: :Man
    source: Prince_Andrew_of_Greece_and_Denmark
  AssignClass (d88b7d94-77dc-445f-b3ff-58b523d1013c)
 Call ID: d88b7d94-77dc-445f-b3ff-58b523d1013c
  Args:
    type: :Ancestor
    source: Prince_Andrew_of_Greece_and_Denmark
  AddLiteral (e1befec4-fa8d-457a-9a10-7c1393d2a35a)
 Call ID: e1befec4-fa8d-457a-9a10-7c1393d2a35a
  Args:
    relation: :hasMarriageYear
    literal_value: 1903
    literal_type: xsd:integer
    source: Alice_of_Battenberg
  AddTriple (7121e50c-8a01-4e67-bdd9-c13e62752b77)
 Call ID: 7121e50c-8a01-4e67-bdd9-c13e62752b77
  Args:
    source: Alice_of_Battenberg
    relation: :hasRelation
    target: Prince_Andrew_of_Greece_and_Denmark
  AssignClass (1587676b-c39e-4d41-a16d-4302f68ccd54)
 Call ID: 1587676b-c39e-4d41-a16d-4302f68ccd54
  Args:
    type: :Man
    source: Prince_Louis_of_Battenberg
  AssignClass (ec3885ab-a3d8-4cda-8603-11927b733680)
 Call ID: ec3885ab-a3d8-4cda-8603-11927b733680
  Args:
    type: :Ancestor
    source: Prince_Louis_of_Battenberg
  AssignClass (be7b314c-b713-4dfc-b0e9-893116c1a499)
 Call ID: be7b314c-b713-4dfc-b0e9-893116c1a499
  Args:
    type: :Woman
    source: Princess_Victoria_of_Hesse_and_by_Rhine
  AssignClass (ade7b1eb-7594-47f5-a957-a4ab93e4d653)
 Call ID: ade7b1eb-7594-47f5-a957-a4ab93e4d653
  Args:
    type: :Ancestor
    source: Princess_Victoria_of_Hesse_and_by_Rhine
  AddTriple (8659bf23-4f4c-4daf-b04b-5fa5b3853f7a)
 Call ID: 8659bf23-4f4c-4daf-b04b-5fa5b3853f7a
  Args:
    source: Alice_of_Battenberg
    target: Prince_Louis_of_Battenberg
    relation: :isDaughterOf
  AddTriple (94e4cf12-4f7c-417e-926a-6a23dd8af8c5)
 Call ID: 94e4cf12-4f7c-417e-926a-6a23dd8af8c5
  Args:
    source: Alice_of_Battenberg
    relation: :isDaughterOf
    target: Princess_Victoria_of_Hesse_and_by_Rhine
  AssignClass (8031fa91-3d35-4023-a898-94d57de2fdec)
 Call ID: 8031fa91-3d35-4023-a898-94d57de2fdec
  Args:
    type: :Woman
    source: Louise_Mountbatten
  AssignClass (94b0edb4-ab13-43f2-aaf0-3651494cb3cd)
 Call ID: 94b0edb4-ab13-43f2-aaf0-3651494cb3cd
  Args:
    type: :Man
    source: George_Mountbatten_2nd_Marquess_of_Milford_Haven
  AssignClass (6991693e-d9e1-43e9-bee2-fe7342802b37)
 Call ID: 6991693e-d9e1-43e9-bee2-fe7342802b37
  Args:
    type: :Man
    source: Louis_Mountbatten_1st_Earl_Mountbatten_of_Burma
  AddTriple (bdea029b-600e-41ca-9d33-1c4dff9f403e)
 Call ID: bdea029b-600e-41ca-9d33-1c4dff9f403e
  Args:
    target: Louise_Mountbatten
    relation: :isSisterOf
    source: Alice_of_Battenberg
  AddTriple (c7a8e0f2-9372-430b-84b6-62d363f0bf4d)
 Call ID: c7a8e0f2-9372-430b-84b6-62d363f0bf4d
  Args:
    source: Alice_of_Battenberg
    target: George_Mountbatten_2nd_Marquess_of_Milford_Haven
    relation: :isSisterOf
  AddTriple (ab5034c6-63cf-4e7f-975b-7732571f8fcd)
 Call ID: ab5034c6-63cf-4e7f-975b-7732571f8fcd
  Args:
    relation: :isSisterOf
    target: Louis_Mountbatten_1st_Earl_Mountbatten_of_Burma
    source: Alice_of_Battenberg
  AssignClass (46aedb24-dcc5-4397-9beb-b70f1cdf018f)
 Call ID: 46aedb24-dcc5-4397-9beb-b70f1cdf018f
  Args:
    type: :Woman
    source: Margarita_of_Greece_and_Denmark
  AssignClass (5402c201-b068-4000-9490-7e0d456bbff1)
 Call ID: 5402c201-b068-4000-9490-7e0d456bbff1
  Args:
    type: :Woman
    source: Theodora_of_Greece_and_Denmark
  AssignClass (529bdde7-add9-4098-8e54-e13d174db9f0)
 Call ID: 529bdde7-add9-4098-8e54-e13d174db9f0
  Args:
    type: :Woman
    source: Cecilie_of_Greece_and_Denmark
  AssignClass (4e2604a5-0412-45fb-8d55-e0eedbdf0189)
 Call ID: 4e2604a5-0412-45fb-8d55-e0eedbdf0189
  Args:
    type: :Woman
    source: Sophie_of_Greece_and_Denmark
  AddTriple (10221d0e-20b9-4625-9c8a-5eb334e66805)
 Call ID: 10221d0e-20b9-4625-9c8a-5eb334e66805
  Args:
    target: Alice_of_Battenberg
    relation: :isDaughterOf
    source: Margarita_of_Greece_and_Denmark
  AddTriple (611693ff-2220-4090-a841-f3c3f8367546)
 Call ID: 611693ff-2220-4090-a841-f3c3f8367546
  Args:
    source: Theodora_of_Greece_and_Denmark
    relation: :isDaughterOf
    target: Alice_of_Battenberg
  AddTriple (e731cf8e-4e64-46e0-b960-7db40bc85bd4)
 Call ID: e731cf8e-4e64-46e0-b960-7db40bc85bd4
  Args:
    target: Alice_of_Battenberg
    relation: :isDaughterOf
    source: Cecilie_of_Greece_and_Denmark
  AddTriple (f29ba21c-43d3-41e9-bdfc-2ad7d1796bd8)
 Call ID: f29ba21c-43d3-41e9-bdfc-2ad7d1796bd8
  Args:
    source: Sophie_of_Greece_and_Denmark
    target: Alice_of_Battenberg
    relation: :isDaughterOf
  Finish (8d2815aa-6e5d-4b2c-b1ec-9461a3d62fad)
 Call ID: 8d2815aa-6e5d-4b2c-b1ec-9461a3d62fad
  Args: