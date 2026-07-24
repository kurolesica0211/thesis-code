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
  AssignClass (48b1032a-c68e-40d1-b832-f8b2f2574323)
 Call ID: 48b1032a-c68e-40d1-b832-f8b2f2574323
  Args:
    type: :Man
    source: Prince_Peter_of_Greece_and_Denmark
  AssignClass (11e5f70d-f0ad-40b1-92fd-aac8e90e9f68)
 Call ID: 11e5f70d-f0ad-40b1-92fd-aac8e90e9f68
  Args:
    source: Prince_Peter_of_Greece_and_Denmark
    type: :Person
  AddLiteral (32155539-20b2-4833-9926-050d2f97002c)
 Call ID: 32155539-20b2-4833-9926-050d2f97002c
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Prince_Peter_of_Greece_and_Denmark
    literal_value: 1908
  AddLiteral (77a41f6c-f2b3-4a42-81fb-b4d842cd7f41)
 Call ID: 77a41f6c-f2b3-4a42-81fb-b4d842cd7f41
  Args:
    literal_type: xsd:integer
    literal_value: 1980
    source: Prince_Peter_of_Greece_and_Denmark
    relation: :hasDeathYear
  AssignClass (69a4cad1-fd61-4852-bbfa-91655dcfda1d)
 Call ID: 69a4cad1-fd61-4852-bbfa-91655dcfda1d
  Args:
    type: :Person
    source: Irina_Aleksandrovna_Ovtchinnikova
  AssignClass (24b6006f-449a-4226-b77c-14e27c2d9d64)
 Call ID: 24b6006f-449a-4226-b77c-14e27c2d9d64
  Args:
    source: Irina_Aleksandrovna_Ovtchinnikova
    type: :Woman
  AssignClass (e1a0a8c2-812f-42a1-afc4-2908c540f898)
 Call ID: e1a0a8c2-812f-42a1-afc4-2908c540f898
  Args:
    source: Prince_George_of_Greece_and_Denmark
    type: :Ancestor
  AssignClass (6242bbdd-a779-4298-ba98-9adb37b99073)
 Call ID: 6242bbdd-a779-4298-ba98-9adb37b99073
  Args:
    type: :Man
    source: Prince_George_of_Greece_and_Denmark
  AssignClass (1641a843-68a3-479f-b4b7-32ebf46dea47)
 Call ID: 1641a843-68a3-479f-b4b7-32ebf46dea47
  Args:
    source: Prince_George_of_Greece_and_Denmark
    type: :Person
  AssignClass (c7284cc3-5804-4045-bda9-b548d90bf5a5)
 Call ID: c7284cc3-5804-4045-bda9-b548d90bf5a5
  Args:
    type: :Ancestor
    source: Princess_Marie_Bonaparte
  AssignClass (76d77186-a79f-4fea-bdb1-846030feef67)
 Call ID: 76d77186-a79f-4fea-bdb1-846030feef67
  Args:
    type: :Person
    source: Princess_Marie_Bonaparte
  AssignClass (a5a75425-821b-4ef1-9a8c-9c7fcde41a04)
 Call ID: a5a75425-821b-4ef1-9a8c-9c7fcde41a04
  Args:
    type: :Woman
    source: Princess_Marie_Bonaparte
  AddTriple (276d93a3-fa37-4b80-87f1-9d87c29add81)
 Call ID: 276d93a3-fa37-4b80-87f1-9d87c29add81
  Args:
    target: Prince_George_of_Greece_and_Denmark
    source: Prince_Peter_of_Greece_and_Denmark
    relation: :hasFather
  AddTriple (26d1666e-302e-4961-83cc-12ee2093248c)
 Call ID: 26d1666e-302e-4961-83cc-12ee2093248c
  Args:
    target: Princess_Marie_Bonaparte
    source: Prince_Peter_of_Greece_and_Denmark
    relation: :hasMother
  AssignClass (8492165b-50f4-4732-a5e2-eea91c0c3568)
 Call ID: 8492165b-50f4-4732-a5e2-eea91c0c3568
  Args:
    type: :Ancestor
    source: King_George_I_of_Greece
  AssignClass (8949ed19-5c99-4506-85ba-65c6ae245721)
 Call ID: 8949ed19-5c99-4506-85ba-65c6ae245721
  Args:
    source: King_George_I_of_Greece
    type: :Man
  AssignClass (44391c19-4c1b-4ab2-a3b6-e6321adce70f)
 Call ID: 44391c19-4c1b-4ab2-a3b6-e6321adce70f
  Args:
    source: King_George_I_of_Greece
    type: :Person
  AddTriple (8f5157bd-b1f7-4fda-9803-08bb20455fa8)
 Call ID: 8f5157bd-b1f7-4fda-9803-08bb20455fa8
  Args:
    target: King_George_I_of_Greece
    source: Prince_George_of_Greece_and_Denmark
    relation: :hasFather
  AssignClass (1d3265dc-78c1-4350-8239-15b5a68ca06a)
 Call ID: 1d3265dc-78c1-4350-8239-15b5a68ca06a
  Args:
    type: :Ancestor
    source: Prince_Roland_Bonaparte
  AssignClass (2967aca6-fa62-4e2f-ae4f-f78fccc09f7a)
 Call ID: 2967aca6-fa62-4e2f-ae4f-f78fccc09f7a
  Args:
    type: :Man
    source: Prince_Roland_Bonaparte
  AssignClass (72b78a28-56cb-4323-9d8e-73f7bdc15eb3)
 Call ID: 72b78a28-56cb-4323-9d8e-73f7bdc15eb3
  Args:
    type: :Person
    source: Prince_Roland_Bonaparte
  AssignClass (15409741-a60d-47a9-a1f1-584d72e1f5b4)
 Call ID: 15409741-a60d-47a9-a1f1-584d72e1f5b4
  Args:
    source: Marie-Félix_Blanc
    type: :Ancestor
  AssignClass (b8dfbbf5-a0d7-457f-9b5c-1806840d9e93)
 Call ID: b8dfbbf5-a0d7-457f-9b5c-1806840d9e93
  Args:
    source: Marie-Félix_Blanc
    type: :Person
  AssignClass (b996f913-7d0b-4e3d-8117-0b1b35758122)
 Call ID: b996f913-7d0b-4e3d-8117-0b1b35758122
  Args:
    source: Marie-Félix_Blanc
    type: :Woman
  AddTriple (149acf40-78a1-46d2-a720-0cc51851f492)
 Call ID: 149acf40-78a1-46d2-a720-0cc51851f492
  Args:
    relation: :hasFather
    source: Princess_Marie_Bonaparte
    target: Prince_Roland_Bonaparte
  AddTriple (c20b5017-1e5c-4d5d-bc84-dfe987d85a93)
 Call ID: c20b5017-1e5c-4d5d-bc84-dfe987d85a93
  Args:
    relation: :hasMother
    target: Marie-Félix_Blanc
    source: Princess_Marie_Bonaparte
  AssignClass (0282c0cb-cbf6-4f95-a266-e6b437dd962d)
 Call ID: 0282c0cb-cbf6-4f95-a266-e6b437dd962d
  Args:
    source: Eugénie
    type: :Person
  AssignClass (bf608358-9894-4d2c-963b-22058951ad60)
 Call ID: bf608358-9894-4d2c-963b-22058951ad60
  Args:
    source: Eugénie_of_Greece_and_Denmark
    type: :Woman
  AddTriple (eb2196f6-1fe5-45b7-aa7a-d74c154d98d5)
 Call ID: eb2196f6-1fe5-45b7-aa7a-d74c154d98d5
  Args:
    source: Prince_Peter_of_Greece_and_Denmark
    target: Eugénie_of_Greece_and_Denmark
    relation: :hasSister
  AssignClass (9344573d-4e2c-4234-a095-e21c850f70e4)
 Call ID: 9344573d-4e2c-4234-a095-e21c850f70e4
  Args:
    source: Prince_Valdemar_of_Denmark
    type: :Ancestor
  AssignClass (2110779d-4bcf-43f0-b90c-b45d6a2c8596)
 Call ID: 2110779d-4bcf-43f0-b90c-b45d6a2c8596
  Args:
    type: :Man
    source: Prince_Valdemar_of_Denmark
  AssignClass (0020ec16-666e-408e-b2d6-df051501ec11)
 Call ID: 0020ec16-666e-408e-b2d6-df051501ec11
  Args:
    source: Prince_Valdemar_of_Denmark
    type: :Person
  AssignClass (b666a514-21e1-452a-9195-21b0d88e01ba)
 Call ID: b666a514-21e1-452a-9195-21b0d88e01ba
  Args:
    type: :Person
    source: Princess_Tatiana_Radziwill
  AssignClass (c64aea5b-3c5e-4276-b8a9-58f535810c36)
 Call ID: c64aea5b-3c5e-4276-b8a9-58f535810c36
  Args:
    type: :Woman
    source: Princess_Tatiana_Radziwill
  AddTriple (2fce0027-f981-4aad-bfb7-3297ccb90e6f)
 Call ID: 2fce0027-f981-4aad-bfb7-3297ccb90e6f
  Args:
    relation: :hasMother
    target: Eugénie_of_Greece_and_Denmark
    source: Princess_Tatiana_Radziwill
  AssignClass (94cb9a2c-e9a8-46f6-89f7-1f891af3c54b)
 Call ID: 94cb9a2c-e9a8-46f6-89f7-1f891af3c54b
  Args:
    source: King_George_II_of_Greece
    type: :Person
  AssignClass (fb77aad2-e106-4ad3-936a-ff038e9cf353)
 Call ID: fb77aad2-e106-4ad3-936a-ff038e9cf353
  Args:
    type: :Man
    source: King_George_II_of_Greece
  AssignClass (94cf4d42-0604-4dee-9b5d-782b860416e4)
 Call ID: 94cf4d42-0604-4dee-9b5d-782b860416e4
  Args:
    type: :Ancestor
    source: King_Constantine_I_of_Greece
  AssignClass (c84ca3b3-9dc2-476e-850f-c59d2b0ff4de)
 Call ID: c84ca3b3-9dc2-476e-850f-c59d2b0ff4de
  Args:
    source: King_Constantine_I_of_Greece
    type: :Man
  AssignClass (f4510b76-053b-446c-8910-a4e74482b324)
 Call ID: f4510b76-053b-446c-8910-a4e74482b324
  Args:
    source: King_Constantine_I_of_Greece
    type: :Person
  AssignClass (96025396-015a-4fc5-9806-7537ebe0f602)
 Call ID: 96025396-015a-4fc5-9806-7537ebe0f602
  Args:
    source: Queen_Olga_of_Greece
    type: :Ancestor
  AssignClass (1cc66893-f5b7-4a41-a416-60b805894d6a)
 Call ID: 1cc66893-f5b7-4a41-a416-60b805894d6a
  Args:
    type: :Person
    source: Queen_Olga_of_Greece
  AssignClass (60658024-8c57-4401-a8e6-78fd9ff04c4d)
 Call ID: 60658024-8c57-4401-a8e6-78fd9ff04c4d
  Args:
    type: :Woman
    source: Queen_Olga_of_Greece
  AssignClass (0104d40e-276f-49ea-9a6c-c52a622f00b0)
 Call ID: 0104d40e-276f-49ea-9a6c-c52a622f00b0
  Args:
    type: :Ancestor
    source: Queen_Sophia_of_Greece
  AssignClass (f942ee99-520b-42bb-b881-080f4bfb28bb)
 Call ID: f942ee99-520b-42bb-b881-080f4bfb28bb
  Args:
    type: :Person
    source: Queen_Sophia_of_Greece
  AssignClass (a9b42f6a-cbc6-434f-939d-eeb531688d99)
 Call ID: a9b42f6a-cbc6-434f-939d-eeb531688d99
  Args:
    type: :Woman
    source: Queen_Sophia_of_Greece
  AssignClass (db9e333c-57c7-4398-983d-9ae601a9362a)
 Call ID: db9e333c-57c7-4398-983d-9ae601a9362a
  Args:
    source: Princess_Frederica_of_Hanover
    type: :Woman
  AssignClass (8ab9bf3a-e1c8-4684-8e3b-e87035e51351)
 Call ID: 8ab9bf3a-e1c8-4684-8e3b-e87035e51351
  Args:
    type: :Person
    source: Princess_Frederica_of_Hanover
  AssignClass (4a3ed236-b363-41a2-a36c-69fca289810d)
 Call ID: 4a3ed236-b363-41a2-a36c-69fca289810d
  Args:
    type: :Man
    source: King_Paul_of_Greece
  AssignClass (ea7ebf41-2c10-47d0-9156-1a0fbda26763)
 Call ID: ea7ebf41-2c10-47d0-9156-1a0fbda26763
  Args:
    source: King_Paul_of_Greece
    type: :Person
  AssignClass (610af2b4-6dd4-479a-84fd-c904c30612a7)
 Call ID: 610af2b4-6dd4-479a-84fd-c904c30612a7
  Args:
    source: Jehan_de_Monléon
    type: :Man
  AssignClass (27c0bf6b-68fd-438b-b202-b0329a64bcaa)
 Call ID: 27c0bf6b-68fd-438b-b202-b0329a64bcaa
  Args:
    source: Jehan_de_Monléon
    type: :Person
  AssignClass (e511552e-459b-4238-9c2e-018d3b6056fe)
 Call ID: e511552e-459b-4238-9c2e-018d3b6056fe
  Args:
    source: Lewis_Sloden
    type: :Man
  AssignClass (1edcfcdd-27aa-456a-be55-76fc808b159e)
 Call ID: 1edcfcdd-27aa-456a-be55-76fc808b159e
  Args:
    type: :Person
    source: Lewis_Sloden
  AssignClass (bd57f1ea-502b-45c2-a49b-c45f1f132fe5)
 Call ID: bd57f1ea-502b-45c2-a49b-c45f1f132fe5
  Args:
    source: King_Edward_VIII_of_the_United_Kingdom
    type: :Man
  AssignClass (dcc97799-d3db-47bf-8164-f7aaf717a62b)
 Call ID: dcc97799-d3db-47bf-8164-f7aaf717a62b
  Args:
    source: King_Edward_VIII_of_the_United_Kingdom
    type: :Person
  AssignClass (bc0e5518-815e-4b12-9de8-2d4107add88a)
 Call ID: bc0e5518-815e-4b12-9de8-2d4107add88a
  Args:
    source: Wallis_Simpson
    type: :Woman
  AssignClass (783e32e5-8c9d-44a9-a414-cf564ca0f557)
 Call ID: 783e32e5-8c9d-44a9-a414-cf564ca0f557
  Args:
    source: Wallis_Simpson
    type: :Person
  AssignClass (cbcaa40b-c907-40a3-a793-6382e0ad7d7f)
 Call ID: cbcaa40b-c907-40a3-a793-6382e0ad7d7f
  Args:
    source: King_Constantine_II_of_Greece
    type: :Man
  AssignClass (c0eb1afc-f7f9-470f-8810-8d5fe564f35e)
 Call ID: c0eb1afc-f7f9-470f-8810-8d5fe564f35e
  Args:
    type: :Person
    source: King_Constantine_II_of_Greece
  AssignClass (9ff47742-ffc1-4d8a-8b73-fa67bc8e983e)
 Call ID: 9ff47742-ffc1-4d8a-8b73-fa67bc8e983e
  Args:
    source: Princess_Irene_of_Greece
    type: :Woman
  AssignClass (413b6353-87a4-4f60-95b4-96fc469df699)
 Call ID: 413b6353-87a4-4f60-95b4-96fc469df699
  Args:
    source: Princess_Irene_of_Greece
    type: :Person
  AssignClass (72a8f647-a516-41fc-af04-bcc2ca97855c)
 Call ID: 72a8f647-a516-41fc-af04-bcc2ca97855c
  Args:
    source: Princess_Sophia_of_Greece
    type: :Woman
  AssignClass (eb1b174d-10a4-4fed-9c95-e0d011956490)
 Call ID: eb1b174d-10a4-4fed-9c95-e0d011956490
  Args:
    type: :Person
    source: Princess_Sophia_of_Greece
  AssignClass (188011c4-8b12-4123-af0f-3584df3add28)
 Call ID: 188011c4-8b12-4123-af0f-3584df3add28
  Args:
    source: Princess_Anne-Marie_of_Denmark
    type: :Woman
  AssignClass (f9d70860-e307-440b-bdb7-1b5c44307347)
 Call ID: f9d70860-e307-440b-bdb7-1b5c44307347
  Args:
    type: :Person
    source: Princess_Anne-Marie_of_Denmark
  AssignClass (80e22b49-1c76-4049-ad36-43ed6f5d861b)
 Call ID: 80e22b49-1c76-4049-ad36-43ed6f5d861b
  Args:
    type: :Woman
    source: Princess_Alexia_of_Greece
  AssignClass (376b451d-4f56-4a88-806e-3fdead6ef36e)
 Call ID: 376b451d-4f56-4a88-806e-3fdead6ef36e
  Args:
    source: Princess_Alexia_of_Greece
    type: :Person
  AssignClass (8771eb46-db79-4306-a52a-a2d52cbe839d)
 Call ID: 8771eb46-db79-4306-a52a-a2d52cbe839d
  Args:
    source: Prince_Axel_of_Denmark
    type: :Man
  AssignClass (3ff92c18-35fe-4b6a-a2ed-e6e43ef4fce4)
 Call ID: 3ff92c18-35fe-4b6a-a2ed-e6e43ef4fce4
  Args:
    source: Prince_Axel_of_Denmark
    type: :Person
  Finish (70827e1c-2b0f-4f08-96d9-143a41bd597b)
 Call ID: 70827e1c-2b0f-4f08-96d9-143a41bd597b
  Args: