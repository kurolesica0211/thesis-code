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
Prince Peter of Greece and Denmark (Greek: Πέτρος; 3 December 1908 –  15 October 1980) was a Greek prince, soldier and anthropologist specialising in Tibetan culture and polyandry.
Born in Paris and high in the line of succession to the Greek throne, Prince Peter was deemed to have forfeited his succession rights by marrying a twice-divorced Russian commoner, Irina Aleksandrovna Ovtchinnikova.
Following his first scientific voyage to Asia, Peter served as an officer of the Greek army during the Second World War.
The Prince returned to Asia several more times for his research of Tibetan culture.
Peter eventually separated from his wife and died childless in London.
Early life

A member of the House of Schleswig-Holstein-Sonderburg-Glücksburg, Prince Peter was the elder child and only son of Prince George of Greece and Denmark and the wealthy author and psychoanalyst Princess Marie Bonaparte.
His father was the second son of King George I of Greece and his mother the only daughter of the French botanist Prince Roland Bonaparte and Marie-Félix Blanc.
Peter was born in Paris and spent his childhood in France, and did not set foot in Greece between 1912 and 1935 due to the First World War and the later proclamation of the Second Hellenic Republic.
During that time, he came to know Denmark, the kingdom from which the Greek royal family originated.
He joined the Royal Guards of Denmark in 1932 for basic military service, and was commissioned as a second lieutenant in 1934.
He spent summers at Bernstorff Palace, then owned by his paternal granduncle, Prince Valdemar of Denmark.
Due to their father's long-lasting sexual and emotional relationship with his uncle Valdemar, Peter and his sister Eugénie referred to Valdemar as "Papa Two".
As customary, Princess George took no part in her son's upbringing, and when he reached adolescence, only the counsels of the psychoanalyst Sigmund Freud helped them suppress their incestuous feelings for each other.
Greek restoration

Following the restoration of his cousin, King George II, Prince Peter travelled to the Kingdom to take part in the ceremonial reinterment of the remains of his uncle, King Constantine I, and those of the queens Olga and Sophia, his grandmother and aunt respectively.
In the 1930s, a possible marriage between Prince Peter and Princess Frederica of Hanover may have been discussed, but she eventually married Prince Paul.
Education

Peter attended Lycée Janson de Sailly and received the degree of Doctor of Law from the University of Paris.
Peter joined the 3/40 Evzone Regiment in 1936, becoming an officer.
He proceeded to travel through Greece with his parents and visited Crete in April 1937.
Voyage to Asia and marriage

In 1935, Prince Peter met and started a relationship with Irina Aleksandrovna Ovtchinnikova, a four years older married Russian émigré with an ex-husband, Jehan de Monléon, Marquis de Monléon.
The next year, she obtained divorce from her second husband Lewis (Slodon) Sloden, and her influence over Peter steadily increased.
Peter himself did not want to gain a reputation as bad as that of King Edward VIII of the United Kingdom, who abdicated the same year to marry his own twice divorced foreign lover, the American Wallis Simpson.
Accompanied by Ovtchinnikova and a student of Malinowski, Prince Peter embarked on a voyage to Asia in September 1937.
The party passed through Syria and Persia before reaching British India, in search of a tribe that Peter could study.
They arrived in what is now Pakistan in early 1938, and Peter conducted research in the regions of Lahore, Kulu, Leh, and Srinagar.
Throughout the entire journey, Peter focused his attention on the study of polyandry – an interest that may have resulted from the Oedipus complex.
While in Madras, Peter decided to officialise his relationship with Ovtchinnikova.
Aware of his family's disapproval of the relationship, but also possibly wishing to take advantage of the turmoil created by the recently declared Second World War, the Prince did not bother to inform either the Greek royal court or his parents about the marriage.
Prince George, affronted by his son's decision not to ask him or the King for permission to marry, disowned Peter and henceforward refused contact with him.
Despite her own disappointment, however, Princess George remained in touch with her son and continued to regularly send him money.
However, not all members of the royal family were dissatisfied with Peter's mesalliance and subsequent loss of dynastic rights.
Second World War

Prince Peter and Ovtchinnikova returned to Europe in November 1939.
Prince George refused to see him.
Peter also met with his sister and her newborn daughter, Princess Tatiana Radziwill.
The German invasion of France in 1940 led Peter and his wife to leave Paris and move to Assisi, Italy.
Malinowski, now working at Yale University in the United States of America, was impressed by Peter's research in Asia and offered him a position as research associate in the Anthropology Department of the university.
Peter declined this offer to move to Greece and join his country's infantry in the wake of Greco-Italian War.
King George II believed her to be a plotter, and was also wary of his cousin.
The King suspected that some (particularly leftists) would like to replace him with Peter.
Germany invaded Greece on 6 April 1941.
Peter was not evacuated until 27 April, when the Germans entered Athens.
On Crete, Peter rejoined the King, who was satisfied with his conduct and named him his personal aide de camp.
King George and Prince Paul therefore moved to London, while the majority of the family found refuge in South Africa.
Peter was the only one to remain in Cairo, having been named "Representative of the King of the Hellenes in the Middle East".
The royal family's exile allowed Peter to rejoin Ovtchinnikova in Palestine.
The couple settled in Cairo, where Peter introduced his wife as a princess.
"The Russian", it was rumoured, wished Greece to be Orthodox but Communist and with Peter as king.
Prince Peter's chief task in the Middle East was to reorganise the remnants of the Greek royal army and prepare them to participate in the war alongside the Allies of World War II.
Aftermath of the war

The royal family could not return to Greece immediately after the war ended due to a civil war between the Communists and the Conservatives.
Prince Peter was aware that King George, if allowed to return, would never allow him to move to Greece along with his wife.
On 1 September 1946, a referendum confirmed George II's position.
The King, however, died unexpectedly on 1 April the next year and the Prince was demobilised.
Peter hoped that Paul, George II's successor, would recognise his marriage to Ovtchinnikova.
King Paul agreed but only if Prince Peter officially recognised that the marriage deprived him of his dynastic rights, something the Prince had always refused to do.
Peter turned down the offer and Paul prohibited him from returning to Greece.
Prince Peter and Irene Ovtchinnikova thus decided to move from Egypt to Denmark.
Peter accepted.
The Prince wished to avoid any possible dispute with the Greek government and thus prudently avoided expressing his opinion about the Greek politics.
A few days later, he was relieved when he received a letter from Prince Axel of Denmark, son of Prince Valdemar and first cousin of Peter's father, who informed him that the expedition should still take place.
Tibetan studies

First sojourn

Prince Peter and Ovtchinnikova left the United States in January 1949, travelling from California to Colombo, the capital of Ceylon.
Peter was dismayed to find out that the people lived in poor sanitary conditions and that their culture was on the verge of disappearance.
A large number of Tibetans fled to India, and many found refuge in Kalimpong, enabling Peter to study the people and Tibetan culture.
Peter gathered anthropometric data on 3,284 persons, analysed 198 blood samples, bought clothes, jewellery, books (such as the Tengyur and Kangyur), and various other objects now found at the National Museum of Denmark and the Royal Library.
Having registered their songs, sagas, everyday conversations, oracle prophecies and religious ceremonies, Peter took more than 3,000 photographs of Tibetans.
One man did not understand why the Prince bothered to wear a shirt, given that he already had hair.
The expedition ended in 1952, and the pair went to Copenhagen, where Peter presented his findings.
Despite everything, Peter continued learning Tibetan and by 1954, he learned enough to be able to work without an interpreter.
In mid-1953, the Prince once again left the Himalayas to head a commemorative expedition to Afghanistan in honour of Haslund-Christensen, but returned to the Himalayas within six weeks.
In 1956, Peter was pleased to welcome his mother to his Kalimpong residence.
The more Peter studied the Tibetans, the less he hesitated to criticise the Chinese government and occupying army, who, in turn, suspected him to be a Western spy.
The government of India, on the other hand, feared the wrath of its powerful neighbour and thus proceeded to harass the Prince and Ovtchinnikova to push them out of the country.
The situation was complicated by Ovtchinnikova's progressing tuberculosis, and Peter pleaded with the authorities to allow them to stay until she could travel.
Princess George also tried to intercede on behalf of her son and daughter-in-law, but failed to meet Nehru during his visit to London in June 1956.
During the seven years that Prince Peter spent with his wife in the Himalayas, he was able to collect "...a rich collection of artefacts and books, still and moving photography, sound recordings, ethnographic information as well as an astoundingly large set of physical anthropology data.
"


Final decades

Upon their return to Europe, Prince Peter and Ovtchinnikova settled in the United Kingdom, where the Prince resumed his studies at the London School of Economics.
After King Paul's death, Peter found himself at odds with Paul's son and successor, King Constantine II.
Had he not been deemed excluded from the line of succession due to his unsuitable marriage, Peter would have been heir presumptive to Constantine II according to the original laws of succession.
However, the Parliament of Greece modified the Constitution to replace the original agnatic primogeniture with male-preference cognatic primogeniture, thereby introducing a number of female dynasts and their descendants into the line of succession.
King Constantine II, still unmarried and childless, thus officially recognised his only unmarried sister, Princess Irene, as heir presumptive (excluding the older sister, Princess Sophia, who was due to become Queen of Spain).
Peter remained convinced that the change was illegal and that he would be the rightful heir if the King died without fathering a son.
Shortly after the King's marriage to their cousin, Princess Anne-Marie of Denmark, the uninvited Prince Peter called a press conference in Athens and openly questioned the legality of the constitutional amendment.
King Constantine II and Queen Anne-Marie's first child, Princess Alexia, was born in 1965 and designated as the new heir presumptive, but Peter refused to recognise that either.
Following the rupture between King Constantine and Prime Minister Georgios Papandreou the same year, the Prince openly criticised the King's conduct and suggested himself as an alternative to Constantine II.
However, the abolition of the monarchy and the proclamation of the Third Hellenic Republic in 1974 did not allow Peter to fulfill his dream of ascending the Greek throne.
After the monarchy was abolished, Prince Peter decided to liquidate his possessions in Greece, most notably his residence in Glyfada.
Ovtchinnikova moved to Hong Kong, while Peter took up a relationship with a young Englishwoman who lived with him in Copenhagen.
Prince Peter continued to support the Tibetan cause.
In 1967 he, "...was instrumental in procuring vocational training for young Tibetans in Denmark.
A memorial mass for Prince Peter was held at St Sophia's Cathedral, London, on 22 October.
He compromised by agreeing that the tomb inscription would describe her as "Irina, spouse of Prince Peter, née Alexandrovna Ovtchinnikova" rather than as a Greek princess.
The Greek government, however, refused to allow his burial in Greece.



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
  AssignClass (4462bbd1-1f40-403d-8074-c71bef07b4b6)
 Call ID: 4462bbd1-1f40-403d-8074-c71bef07b4b6
  Args:
    source: Prince Peter of Greece and Denmark
    type: :Man
  AssignClass (60ade10a-d671-4c2e-a5e4-354a5239b2b9)
 Call ID: 60ade10a-d671-4c2e-a5e4-354a5239b2b9
  Args:
    source: Prince Peter of Greece and Denmark
    type: :Person
  AddLiteral (2cc1c62f-caf1-44fb-aed1-bebcfd6480a0)
 Call ID: 2cc1c62f-caf1-44fb-aed1-bebcfd6480a0
  Args:
    literal_value: 1908
    literal_type: xsd:integer
    source: Prince Peter of Greece and Denmark
    relation: :hasBirthYear
  AddLiteral (ad91bba6-171d-4517-ad09-eaf823684097)
 Call ID: ad91bba6-171d-4517-ad09-eaf823684097
  Args:
    source: Prince Peter of Greece and Denmark
    relation: :hasDeathYear
    literal_value: 1980
    literal_type: xsd:integer
  AssignClass (27c8cfbe-9c18-4129-85d8-db02ab8cb953)
 Call ID: 27c8cfbe-9c18-4129-85d8-db02ab8cb953
  Args:
    source: Prince George of Greece and Denmark
    type: :Man
  AssignClass (3870e014-6521-4787-8833-0e02e16ae690)
 Call ID: 3870e014-6521-4787-8833-0e02e16ae690
  Args:
    source: Prince George of Greece and Denmark
    type: :Person
  AssignClass (80ceb70b-32c9-4bc9-8ed0-dae085fb7281)
 Call ID: 80ceb70b-32c9-4bc9-8ed0-dae085fb7281
  Args:
    source: Princess Marie Bonaparte
    type: :Woman
  AssignClass (1dab3a27-3206-4f29-9809-206ccdb8652f)
 Call ID: 1dab3a27-3206-4f29-9809-206ccdb8652f
  Args:
    source: Princess Marie Bonaparte
    type: :Person
  AddTriple (0a4eceb0-e933-40a8-b321-32ff8483a135)
 Call ID: 0a4eceb0-e933-40a8-b321-32ff8483a135
  Args:
    relation: :hasFather
    source: Prince Peter of Greece and Denmark
    target: Prince George of Greece and Denmark
  AddTriple (a6ec7d87-4fe9-4504-ab5e-b1c7d055af08)
 Call ID: a6ec7d87-4fe9-4504-ab5e-b1c7d055af08
  Args:
    target: Princess Marie Bonaparte
    relation: :hasMother
    source: Prince Peter of Greece and Denmark
  AssignClass (10e4f54c-4260-4154-bcba-b1ffd751cb4f)
 Call ID: 10e4f54c-4260-4154-bcba-b1ffd751cb4f
  Args:
    source: King George I of Greece
    type: :Man
  AssignClass (98a7c6e6-58de-440e-b365-1b8d9ce8ce34)
 Call ID: 98a7c6e6-58de-440e-b365-1b8d9ce8ce34
  Args:
    source: King George I of Greece
    type: :Person
  AddTriple (b2b754d3-30f1-4dbe-bb70-9de84b1a7257)
 Call ID: b2b754d3-30f1-4dbe-bb70-9de84b1a7257
  Args:
    target: King George I of Greece
    relation: :hasFather
    source: Prince George of Greece and Denmark
  AssignClass (c29f60aa-01e2-4d02-a9c4-72eacd2e55a9)
 Call ID: c29f60aa-01e2-4d02-a9c4-72eacd2e55a9
  Args:
    source: Prince Roland Bonaparte
    type: :Man
  AssignClass (3c3fc30f-7b1b-475f-899d-1504453b3b30)
 Call ID: 3c3fc30f-7b1b-475f-899d-1504453b3b30
  Args:
    source: Prince Roland Bonaparte
    type: :Person
  AssignClass (87055801-cfd3-4848-9af1-bad285cb281b)
 Call ID: 87055801-cfd3-4848-9af1-bad285cb281b
  Args:
    source: Marie-Félix Blanc
    type: :Woman
  AssignClass (16fd79b5-3220-41b6-8f53-193a796b061d)
 Call ID: 16fd79b5-3220-41b6-8f53-193a796b061d
  Args:
    source: Marie-Félix Blanc
    type: :Person
  AddTriple (56e93a24-547c-45c3-9cbe-b3ba1b5a980c)
 Call ID: 56e93a24-547c-45c3-9cbe-b3ba1b5a980c
  Args:
    target: Prince Roland Bonaparte
    source: Princess Marie Bonaparte
    relation: :hasFather
  AddTriple (a5d9a388-b0af-4a67-91e8-23adfbef08fe)
 Call ID: a5d9a388-b0af-4a67-91e8-23adfbef08fe
  Args:
    target: Marie-Félix Blanc
    relation: :hasMother
    source: Princess Marie Bonaparte
  AssignClass (a8f94810-722c-44bf-ad31-a652c43399dc)
 Call ID: a8f94810-722c-44bf-ad31-a652c43399dc
  Args:
    source: Eugénie
    type: :Woman
  AssignClass (e3403ca2-9aba-4a2f-811d-975f963a4a8f)
 Call ID: e3403ca2-9aba-4a2f-811d-975f963a4a8f
  Args:
    source: Eugénie
    type: :Person
  AddTriple (b3fe2451-f211-48ee-b452-aa75069ccacd)
 Call ID: b3fe2451-f211-48ee-b452-aa75069ccacd
  Args:
    target: Prince Peter of Greece and Denmark
    source: Eugénie
    relation: :isSisterOf
  AddTriple (ec35c2e3-62ac-4c61-9a23-2586f3ae464b)
 Call ID: ec35c2e3-62ac-4c61-9a23-2586f3ae464b
  Args:
    source: Eugénie
    relation: :hasFather
    target: Prince George of Greece and Denmark
  AddTriple (02daa502-dec9-412f-8471-46329abe11bc)
 Call ID: 02daa502-dec9-412f-8471-46329abe11bc
  Args:
    target: Princess Marie Bonaparte
    source: Eugénie
    relation: :hasMother
  AssignClass (4626ee83-aca8-4ac2-8e0d-8860b6328d3f)
 Call ID: 4626ee83-aca8-4ac2-8e0d-8860b6328d3f
  Args:
    source: Irina Aleksandrovna Ovtchinnikova
    type: :Woman
  AssignClass (15bc2519-0d24-4d4c-b0c4-c24605222a16)
 Call ID: 15bc2519-0d24-4d4c-b0c4-c24605222a16
  Args:
    source: Irina Aleksandrovna Ovtchinnikova
    type: :Person
  AssignClass (e009d8ba-27b2-45d6-9f7f-0c458b3d8131)
 Call ID: e009d8ba-27b2-45d6-9f7f-0c458b3d8131
  Args:
    source: Jehan de Monléon
    type: :Man
  AssignClass (650519b1-f578-477a-afe8-24a2792b767e)
 Call ID: 650519b1-f578-477a-afe8-24a2792b767e
  Args:
    source: Jehan de Monléon
    type: :Person
  AssignClass (a119dadc-69f6-4313-98e7-2b96a69f0452)
 Call ID: a119dadc-69f6-4313-98e7-2b96a69f0452
  Args:
    source: Lewis (Slodon) Sloden
    type: :Man
  AssignClass (9f1c0a46-52fe-403e-be7a-ba07f1dbda85)
 Call ID: 9f1c0a46-52fe-403e-be7a-ba07f1dbda85
  Args:
    source: Lewis (Slodon) Sloden
    type: :Person
  AssignClass (1338d9d3-1392-4ee4-ad58-a407fa28abe4)
 Call ID: 1338d9d3-1392-4ee4-ad58-a407fa28abe4
  Args:
    source: Princess Tatiana Radziwill
    type: :Woman
  AssignClass (261859a2-a0e0-44c3-a8f4-598b8db32f55)
 Call ID: 261859a2-a0e0-44c3-a8f4-598b8db32f55
  Args:
    source: Princess Tatiana Radziwill
    type: :Person
  AssignClass (cc1b1863-e157-409c-b0c9-6b894264fe39)
 Call ID: cc1b1863-e157-409c-b0c9-6b894264fe39
  Args:
    source: King George II
    type: :Man
  AssignClass (902af1be-357a-4b57-b411-011c8524951e)
 Call ID: 902af1be-357a-4b57-b411-011c8524951e
  Args:
    source: King George II
    type: :Person
  AssignClass (c7d5e6aa-0c48-49b4-b3a0-2d0a435708cd)
 Call ID: c7d5e6aa-0c48-49b4-b3a0-2d0a435708cd
  Args:
    source: King Constantine I
    type: :Man
  AssignClass (c818948d-22ca-4f99-8d78-6fc2b8b7f216)
 Call ID: c818948d-22ca-4f99-8d78-6fc2b8b7f216
  Args:
    source: King Constantine I
    type: :Person
  AssignClass (3bfb54fa-4d99-43b0-927f-ca957a6cb1ee)
 Call ID: 3bfb54fa-4d99-43b0-927f-ca957a6cb1ee
  Args:
    source: Olga
    type: :Woman
  AssignClass (ef5c4b74-43ce-4760-bf69-bf2bfe919ac5)
 Call ID: ef5c4b74-43ce-4760-bf69-bf2bfe919ac5
  Args:
    source: Olga
    type: :Person
  AssignClass (464b7ca4-c716-45b3-8102-d98d25c74f1d)
 Call ID: 464b7ca4-c716-45b3-8102-d98d25c74f1d
  Args:
    source: Sophia
    type: :Woman
  AssignClass (e3f4c416-69f4-43f3-bbbd-ced6fa3955df)
 Call ID: e3f4c416-69f4-43f3-bbbd-ced6fa3955df
  Args:
    source: Sophia
    type: :Person
  AssignClass (a00149f7-7d14-4921-a11b-87cf764a73ec)
 Call ID: a00149f7-7d14-4921-a11b-87cf764a73ec
  Args:
    source: Princess Frederica of Hanover
    type: :Woman
  AssignClass (ec31e5ad-4db2-41e3-8e38-f744692b959b)
 Call ID: ec31e5ad-4db2-41e3-8e38-f744692b959b
  Args:
    source: Princess Frederica of Hanover
    type: :Person
  AssignClass (af64f2c5-c803-4d5d-994b-d2ee85e774c2)
 Call ID: af64f2c5-c803-4d5d-994b-d2ee85e774c2
  Args:
    source: Prince Paul
    type: :Man
  AssignClass (05709649-e36e-4537-bfe4-d476a5a9da2c)
 Call ID: 05709649-e36e-4537-bfe4-d476a5a9da2c
  Args:
    source: Prince Paul
    type: :Person
  AssignClass (08420958-809b-4049-8890-160fb1e544c9)
 Call ID: 08420958-809b-4049-8890-160fb1e544c9
  Args:
    source: Prince Valdemar of Denmark
    type: :Man
  AssignClass (2c71c627-9c0c-4db2-a995-9a85044bedda)
 Call ID: 2c71c627-9c0c-4db2-a995-9a85044bedda
  Args:
    source: Prince Valdemar of Denmark
    type: :Person
  AssignClass (9de5892f-854a-4ebd-b1b1-729563133b1a)
 Call ID: 9de5892f-854a-4ebd-b1b1-729563133b1a
  Args:
    source: Prince Axel of Denmark
    type: :Man
  AssignClass (36464f1c-0409-4109-8cab-236071370b27)
 Call ID: 36464f1c-0409-4109-8cab-236071370b27
  Args:
    source: Prince Axel of Denmark
    type: :Person
  AddTriple (6453d9af-bed5-4d13-bc52-821f13eb8e89)
 Call ID: 6453d9af-bed5-4d13-bc52-821f13eb8e89
  Args:
    target: Prince Valdemar of Denmark
    source: Prince Axel of Denmark
    relation: :hasFather
  AssignClass (50b9d0cb-541b-45d9-bdc8-c84da98b4221)
 Call ID: 50b9d0cb-541b-45d9-bdc8-c84da98b4221
  Args:
    source: King Constantine II
    type: :Man
  AssignClass (57a8bee3-c16e-4172-8913-9a2f6ffa09b4)
 Call ID: 57a8bee3-c16e-4172-8913-9a2f6ffa09b4
  Args:
    source: King Constantine II
    type: :Person
  AddTriple (fdef1659-e60f-4354-b9fa-ad7a8b4f0525)
 Call ID: fdef1659-e60f-4354-b9fa-ad7a8b4f0525
  Args:
    target: Prince Paul
    relation: :hasFather
    source: King Constantine II
  AssignClass (22a2634b-2b6a-4c8d-8f0e-efe3dfc4e959)
 Call ID: 22a2634b-2b6a-4c8d-8f0e-efe3dfc4e959
  Args:
    source: Princess Irene
    type: :Woman
  AssignClass (7e6c3d10-ff0a-457f-9f2c-54d3f773510e)
 Call ID: 7e6c3d10-ff0a-457f-9f2c-54d3f773510e
  Args:
    source: Princess Irene
    type: :Person
  AddTriple (421b4850-3662-4613-a7c8-0b130fd88bb6)
 Call ID: 421b4850-3662-4613-a7c8-0b130fd88bb6
  Args:
    source: Princess Irene
    relation: :hasFather
    target: Prince Paul
  AssignClass (1c961675-1b63-4014-abc2-99d11d5329ea)
 Call ID: 1c961675-1b63-4014-abc2-99d11d5329ea
  Args:
    source: Princess Sophia
    type: :Woman
  AssignClass (3d73d884-acb3-4c5f-83bc-4e8dd91fda23)
 Call ID: 3d73d884-acb3-4c5f-83bc-4e8dd91fda23
  Args:
    source: Princess Sophia
    type: :Person
  AddTriple (32c6b0ed-d85d-4724-a5c0-2a9999c2f631)
 Call ID: 32c6b0ed-d85d-4724-a5c0-2a9999c2f631
  Args:
    target: Prince Paul
    relation: :hasFather
    source: Princess Sophia
  AssignClass (aaa618aa-3f8f-4510-a841-3cb3b52bd9ee)
 Call ID: aaa618aa-3f8f-4510-a841-3cb3b52bd9ee
  Args:
    source: Princess Anne-Marie of Denmark
    type: :Woman
  AssignClass (537a572b-e222-49ba-85c2-188a77341323)
 Call ID: 537a572b-e222-49ba-85c2-188a77341323
  Args:
    source: Princess Anne-Marie of Denmark
    type: :Person
  AssignClass (52895c27-718d-4f31-bc71-92cbb96c5aae)
 Call ID: 52895c27-718d-4f31-bc71-92cbb96c5aae
  Args:
    source: Princess Alexia
    type: :Woman
  AssignClass (c17e773d-09e9-48db-aec0-caf7279a7960)
 Call ID: c17e773d-09e9-48db-aec0-caf7279a7960
  Args:
    source: Princess Alexia
    type: :Person
  AddTriple (2ae78636-6e9a-4a22-a102-96dcf1fccd0d)
 Call ID: 2ae78636-6e9a-4a22-a102-96dcf1fccd0d
  Args:
    target: King Constantine II
    relation: :hasFather
    source: Princess Alexia
  AddTriple (c3e6fbe3-18e8-49a0-a606-32bce3d1c6cf)
 Call ID: c3e6fbe3-18e8-49a0-a606-32bce3d1c6cf
  Args:
    target: Princess Anne-Marie of Denmark
    relation: :hasMother
    source: Princess Alexia
  Finish (6bf5e014-825e-491c-9054-17677bdbe628)
 Call ID: 6bf5e014-825e-491c-9054-17677bdbe628
  Args: