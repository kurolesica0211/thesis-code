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
  AssignClass (75cfe9e4-516b-4abe-a207-a4799939f005)
 Call ID: 75cfe9e4-516b-4abe-a207-a4799939f005
  Args:
    type: :Man
    source: Prince_Peter_of_Greece_and_Denmark
  AssignClass (0ae4de1d-a7b3-4af1-bbbe-abfe04afee73)
 Call ID: 0ae4de1d-a7b3-4af1-bbbe-abfe04afee73
  Args:
    source: Prince_Peter_of_Greece_and_Denmark
    type: :Person
  AddLiteral (c0194813-3af8-4cdd-9285-ca4e850f20da)
 Call ID: c0194813-3af8-4cdd-9285-ca4e850f20da
  Args:
    relation: :hasBirthYear
    source: Prince_Peter_of_Greece_and_Denmark
    literal_type: xsd:integer
    literal_value: 1908
  AddLiteral (1001ee28-8653-4a14-8f69-7ebd64b11a7e)
 Call ID: 1001ee28-8653-4a14-8f69-7ebd64b11a7e
  Args:
    relation: :hasDeathYear
    source: Prince_Peter_of_Greece_and_Denmark
    literal_type: xsd:integer
    literal_value: 1980
  AssignClass (7122e650-2519-4dd1-a913-740421584251)
 Call ID: 7122e650-2519-4dd1-a913-740421584251
  Args:
    source: Prince_George_of_Greece_and_Denmark
    type: :Man
  AssignClass (9e83481b-e03d-4fa5-8ce1-66eb3ad68019)
 Call ID: 9e83481b-e03d-4fa5-8ce1-66eb3ad68019
  Args:
    source: Prince_George_of_Greece_and_Denmark
    type: :Person
  AssignClass (d6f269c7-2e8e-4703-84b1-c4292a21d13f)
 Call ID: d6f269c7-2e8e-4703-84b1-c4292a21d13f
  Args:
    source: Princess_Marie_Bonaparte
    type: :Woman
  AssignClass (68113daf-9080-4332-b922-d4e4cc93809b)
 Call ID: 68113daf-9080-4332-b922-d4e4cc93809b
  Args:
    source: Princess_Marie_Bonaparte
    type: :Person
  AddTriple (131d25fe-3666-4f7d-aade-79c4b5321041)
 Call ID: 131d25fe-3666-4f7d-aade-79c4b5321041
  Args:
    source: Prince_Peter_of_Greece_and_Denmark
    relation: :hasFather
    target: Prince_George_of_Greece_and_Denmark
  AddTriple (3896e388-cb57-4040-8ab0-e234ce145906)
 Call ID: 3896e388-cb57-4040-8ab0-e234ce145906
  Args:
    source: Prince_Peter_of_Greece_and_Denmark
    relation: :hasMother
    target: Princess_Marie_Bonaparte
  AssignClass (e6aa597d-ceb1-4582-a50d-227e9b75e059)
 Call ID: e6aa597d-ceb1-4582-a50d-227e9b75e059
  Args:
    source: King_George_I_of_Greece
    type: :Man
  AssignClass (34d0d311-e944-44b2-8695-e321dcc4246f)
 Call ID: 34d0d311-e944-44b2-8695-e321dcc4246f
  Args:
    type: :Person
    source: King_George_I_of_Greece
  AddTriple (8c755141-9e57-49dd-8ef7-b875748617fc)
 Call ID: 8c755141-9e57-49dd-8ef7-b875748617fc
  Args:
    source: Prince_George_of_Greece_and_Denmark
    relation: :hasFather
    target: King_George_I_of_Greece
  AssignClass (33694546-695c-4069-85d6-526dd9f7fe42)
 Call ID: 33694546-695c-4069-85d6-526dd9f7fe42
  Args:
    source: Prince_Roland_Bonaparte
    type: :Man
  AssignClass (66921a16-b7b8-40ed-bf6c-dedfe6e69413)
 Call ID: 66921a16-b7b8-40ed-bf6c-dedfe6e69413
  Args:
    source: Prince_Roland_Bonaparte
    type: :Person
  AssignClass (e2f5b900-d70b-4327-ae68-37b625fa5451)
 Call ID: e2f5b900-d70b-4327-ae68-37b625fa5451
  Args:
    type: :Woman
    source: Marie-Félix_Blanc
  AssignClass (5270211f-718f-4056-a878-a90652e02f9e)
 Call ID: 5270211f-718f-4056-a878-a90652e02f9e
  Args:
    type: :Person
    source: Marie-Félix_Blanc
  AddTriple (aa18f7d8-ae87-4855-bc4c-6f327957a1c0)
 Call ID: aa18f7d8-ae87-4855-bc4c-6f327957a1c0
  Args:
    source: Princess_Marie_Bonaparte
    target: Prince_Roland_Bonaparte
    relation: :hasFather
  AddTriple (05922362-ccae-4e07-a65d-ee21bc762bde)
 Call ID: 05922362-ccae-4e07-a65d-ee21bc762bde
  Args:
    source: Princess_Marie_Bonaparte
    relation: :hasMother
    target: Marie-Félix_Blanc
  AssignClass (fe17730e-e9e3-4ed3-a9c4-e94218955796)
 Call ID: fe17730e-e9e3-4ed3-a9c4-e94218955796
  Args:
    type: :Woman
    source: Eugénie_of_Greece_and_Denmark
  AssignClass (d55117a3-fd3b-4fc3-8f0c-8b0956b46970)
 Call ID: d55117a3-fd3b-4fc3-8f0c-8b0956b46970
  Args:
    type: :Person
    source: Eugénie_of_Greece_and_Denmark
  AddTriple (85c213c6-4a68-4672-a538-125f4d9292e4)
 Call ID: 85c213c6-4a68-4672-a538-125f4d9292e4
  Args:
    target: Eugénie_of_Greece_and_Denmark
    relation: :isSiblingOf
    source: Prince_Peter_of_Greece_and_Denmark
  AddTriple (c7a71816-334e-45ef-8541-038ba2c6ddf4)
 Call ID: c7a71816-334e-45ef-8541-038ba2c6ddf4
  Args:
    target: Prince_George_of_Greece_and_Denmark
    relation: :hasFather
    source: Eugénie_of_Greece_and_Denmark
  AddTriple (07003762-a678-4dd3-824c-36d02f78bedd)
 Call ID: 07003762-a678-4dd3-824c-36d02f78bedd
  Args:
    source: Eugénie_of_Greece_and_Denmark
    relation: :hasMother
    target: Princess_Marie_Bonaparte
  AssignClass (b4dd55a6-af4e-4c6f-9f16-f7dadc611850)
 Call ID: b4dd55a6-af4e-4c6f-9f16-f7dadc611850
  Args:
    type: :Woman
    source: Irina_Aleksandrovna_Ovtchinnikova
  AssignClass (19b11d36-253f-4a90-84da-3cd22252c1aa)
 Call ID: 19b11d36-253f-4a90-84da-3cd22252c1aa
  Args:
    source: Irina_Aleksandrovna_Ovtchinnikova
    type: :Person
  AssignClass (7611686d-cdab-445f-83ad-b35bb08b90fd)
 Call ID: 7611686d-cdab-445f-83ad-b35bb08b90fd
  Args:
    source: Prince_Valdemar_of_Denmark
    type: :Man
  AssignClass (cf0ac954-b045-4a4c-b35c-2a6872d05f2b)
 Call ID: cf0ac954-b045-4a4c-b35c-2a6872d05f2b
  Args:
    source: Prince_Valdemar_of_Denmark
    type: :Person
  AssignClass (9d0f443a-739a-4ae4-9a4a-d8e1a4622d14)
 Call ID: 9d0f443a-739a-4ae4-9a4a-d8e1a4622d14
  Args:
    type: :Man
    source: King_George_II_of_Greece
  AssignClass (c7b6a174-251b-4156-a23d-4d902080db39)
 Call ID: c7b6a174-251b-4156-a23d-4d902080db39
  Args:
    type: :Person
    source: King_George_II_of_Greece
  AssignClass (27956053-898a-4145-9539-fc2f665c5fd7)
 Call ID: 27956053-898a-4145-9539-fc2f665c5fd7
  Args:
    type: :Man
    source: King_Constantine_I_of_Greece
  AssignClass (378cce4b-a63d-4af1-8a3d-db86bbe1aafc)
 Call ID: 378cce4b-a63d-4af1-8a3d-db86bbe1aafc
  Args:
    type: :Person
    source: King_Constantine_I_of_Greece
  AssignClass (ef70bb51-8ebb-42a4-b896-a249361dae99)
 Call ID: ef70bb51-8ebb-42a4-b896-a249361dae99
  Args:
    type: :Woman
    source: Queen_Olga_of_Greece
  AssignClass (b7672a8b-7163-443e-aba7-828ec025b0a1)
 Call ID: b7672a8b-7163-443e-aba7-828ec025b0a1
  Args:
    source: Queen_Olga_of_Greece
    type: :Person
  AssignClass (fff673b8-e90c-40c7-a692-f53d3dcede3f)
 Call ID: fff673b8-e90c-40c7-a692-f53d3dcede3f
  Args:
    source: Queen_Sophia_of_Greece
    type: :Woman
  AssignClass (28dcb0b5-970d-42c9-847b-c1dba4c8ebbb)
 Call ID: 28dcb0b5-970d-42c9-847b-c1dba4c8ebbb
  Args:
    source: Queen_Sophia_of_Greece
    type: :Person
  AssignClass (70cc8b1f-bcd5-4775-9f09-c951d25fa441)
 Call ID: 70cc8b1f-bcd5-4775-9f09-c951d25fa441
  Args:
    type: :Woman
    source: Princess_Frederica_of_Hanover
  AssignClass (108bbc78-104b-43da-9a13-a64ae442755b)
 Call ID: 108bbc78-104b-43da-9a13-a64ae442755b
  Args:
    type: :Person
    source: Princess_Frederica_of_Hanover
  AssignClass (86c6f2e2-d77f-4bed-a18b-aa005b4ebf5d)
 Call ID: 86c6f2e2-d77f-4bed-a18b-aa005b4ebf5d
  Args:
    type: :Man
    source: King_Paul_of_Greece
  AssignClass (e1833d4b-cf55-4417-aa70-8ddfec846eeb)
 Call ID: e1833d4b-cf55-4417-aa70-8ddfec846eeb
  Args:
    type: :Person
    source: King_Paul_of_Greece
  AssignClass (e7d63062-08d7-4fe5-9588-d0aa56d5f3b0)
 Call ID: e7d63062-08d7-4fe5-9588-d0aa56d5f3b0
  Args:
    type: :Man
    source: Jehan_de_Monléon
  AssignClass (602183ea-c129-4a29-8846-d003c865df41)
 Call ID: 602183ea-c129-4a29-8846-d003c865df41
  Args:
    source: Jehan_de_Monléon
    type: :Person
  AssignClass (9ce6b388-4e52-410e-a27c-30f814fe32a0)
 Call ID: 9ce6b388-4e52-410e-a27c-30f814fe32a0
  Args:
    source: Lewis_Sloden
    type: :Man
  AssignClass (960bb1a5-9471-4f4d-8329-34da3dc1ca10)
 Call ID: 960bb1a5-9471-4f4d-8329-34da3dc1ca10
  Args:
    source: Lewis_Sloden
    type: :Person
  AssignClass (71b3ca11-c547-477c-a26f-3b924906d8f1)
 Call ID: 71b3ca11-c547-477c-a26f-3b924906d8f1
  Args:
    type: :Woman
    source: Princess_Tatiana_Radziwill
  AssignClass (774e769f-7bbf-4266-ac11-453952dc292f)
 Call ID: 774e769f-7bbf-4266-ac11-453952dc292f
  Args:
    source: Princess_Tatiana_Radziwill
    type: :Person
  AssignClass (bd6cc615-c815-4251-bcd1-831feda84802)
 Call ID: bd6cc615-c815-4251-bcd1-831feda84802
  Args:
    source: Prince_Axel_of_Denmark
    type: :Man
  AssignClass (3a5a4829-2a12-4a2a-a7e6-9c7e65db3bfa)
 Call ID: 3a5a4829-2a12-4a2a-a7e6-9c7e65db3bfa
  Args:
    source: Prince_Axel_of_Denmark
    type: :Person
  AssignClass (3ee4eda8-33b6-44f9-b722-bb0d65455097)
 Call ID: 3ee4eda8-33b6-44f9-b722-bb0d65455097
  Args:
    type: :Man
    source: King_Constantine_II_of_Greece
  AssignClass (d8f1a538-9fc9-4b4d-a90a-c8d5d8e31bd0)
 Call ID: d8f1a538-9fc9-4b4d-a90a-c8d5d8e31bd0
  Args:
    type: :Person
    source: King_Constantine_II_of_Greece
  AssignClass (7ef242d5-f8a4-4701-9d5b-aeb1966c6060)
 Call ID: 7ef242d5-f8a4-4701-9d5b-aeb1966c6060
  Args:
    source: Princess_Irene_of_Greece
    type: :Woman
  AssignClass (fc5c6378-259d-4452-bf68-341807bf89e7)
 Call ID: fc5c6378-259d-4452-bf68-341807bf89e7
  Args:
    type: :Person
    source: Princess_Irene_of_Greece
  AssignClass (39254e0a-9cd9-4973-bd2f-b48c99c24036)
 Call ID: 39254e0a-9cd9-4973-bd2f-b48c99c24036
  Args:
    source: Princess_Sophia_of_Greece
    type: :Woman
  AssignClass (640206e9-b10d-45a3-818c-0be0533cba6a)
 Call ID: 640206e9-b10d-45a3-818c-0be0533cba6a
  Args:
    source: Princess_Sophia_of_Greece
    type: :Person
  AssignClass (3d69328a-bd05-4b62-9aa6-1646d5265f29)
 Call ID: 3d69328a-bd05-4b62-9aa6-1646d5265f29
  Args:
    type: :Woman
    source: Princess_Anne-Marie_of_Denmark
  AssignClass (f37f0e34-810c-439a-b67b-d975c02d16a8)
 Call ID: f37f0e34-810c-439a-b67b-d975c02d16a8
  Args:
    source: Princess_Anne-Marie_of_Denmark
    type: :Person
  AssignClass (87298d44-4876-4d83-b64d-943c4bc0e19b)
 Call ID: 87298d44-4876-4d83-b64d-943c4bc0e19b
  Args:
    type: :Woman
    source: Princess_Alexia_of_Greece
  AssignClass (afbe8b92-4573-47db-aba8-4e79b35e7a65)
 Call ID: afbe8b92-4573-47db-aba8-4e79b35e7a65
  Args:
    type: :Person
    source: Princess_Alexia_of_Greece
  Finish (d6c290c9-bba5-4519-8688-576f5df26415)
 Call ID: d6c290c9-bba5-4519-8688-576f5df26415
  Args: