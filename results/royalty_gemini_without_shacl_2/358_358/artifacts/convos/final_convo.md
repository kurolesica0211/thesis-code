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
  AssignClass (1919d8be-9d20-4f9c-b9c3-5e473f89fbbf)
 Call ID: 1919d8be-9d20-4f9c-b9c3-5e473f89fbbf
  Args:
    source: Prince_Peter_of_Greece_and_Denmark
    type: :Man
  AssignClass (61327e70-ee58-4559-8fe0-8e8a43e0da55)
 Call ID: 61327e70-ee58-4559-8fe0-8e8a43e0da55
  Args:
    type: :Person
    source: Prince_Peter_of_Greece_and_Denmark
  AddLiteral (cca631af-b4cd-4023-822a-855728bf2cfd)
 Call ID: cca631af-b4cd-4023-822a-855728bf2cfd
  Args:
    literal_value: 1908
    relation: :hasBirthYear
    source: Prince_Peter_of_Greece_and_Denmark
    literal_type: xsd:string
  AddLiteral (54c3cea5-f7a4-4fc8-9718-7ab48799e354)
 Call ID: 54c3cea5-f7a4-4fc8-9718-7ab48799e354
  Args:
    source: Prince_Peter_of_Greece_and_Denmark
    literal_type: xsd:string
    literal_value: 1980
    relation: :hasDeathYear
  AssignClass (7c47b4ff-47b1-4311-866c-e6b463abf5d7)
 Call ID: 7c47b4ff-47b1-4311-866c-e6b463abf5d7
  Args:
    type: :Man
    source: Prince_George_of_Greece_and_Denmark
  AssignClass (dd321a55-b8b7-45ff-bb43-9c3d6687d38d)
 Call ID: dd321a55-b8b7-45ff-bb43-9c3d6687d38d
  Args:
    type: :Person
    source: Prince_George_of_Greece_and_Denmark
  AssignClass (57a9a09e-ef27-4846-9421-648bee37c2ba)
 Call ID: 57a9a09e-ef27-4846-9421-648bee37c2ba
  Args:
    source: Princess_Marie_Bonaparte
    type: :Woman
  AssignClass (703f8a69-8093-44f1-b5b1-762ccd30a235)
 Call ID: 703f8a69-8093-44f1-b5b1-762ccd30a235
  Args:
    source: Princess_Marie_Bonaparte
    type: :Person
  AddTriple (e29d7106-d072-4d1c-adb8-12ff9fb3f9ac)
 Call ID: e29d7106-d072-4d1c-adb8-12ff9fb3f9ac
  Args:
    relation: :hasFather
    target: Prince_George_of_Greece_and_Denmark
    source: Prince_Peter_of_Greece_and_Denmark
  AddTriple (a02d11f5-aab5-407a-8f8e-cedc12269a44)
 Call ID: a02d11f5-aab5-407a-8f8e-cedc12269a44
  Args:
    target: Princess_Marie_Bonaparte
    relation: :hasMother
    source: Prince_Peter_of_Greece_and_Denmark
  AssignClass (4fb48ea7-de5c-4093-82b4-543605680b63)
 Call ID: 4fb48ea7-de5c-4093-82b4-543605680b63
  Args:
    source: Eugenie
    type: :Woman
  AssignClass (632e3c9b-3cdb-4984-afcc-b70a1ab2acbc)
 Call ID: 632e3c9b-3cdb-4984-afcc-b70a1ab2acbc
  Args:
    source: Eugenie
    type: :Person
  AddTriple (0f94a9e0-76bf-4e83-8e7b-c300c99251b1)
 Call ID: 0f94a9e0-76bf-4e83-8e7b-c300c99251b1
  Args:
    source: Prince_Peter_of_Greece_and_Denmark
    relation: :isSiblingOf
    target: Eugenie
  AddTriple (8cfaaf21-6475-4bd1-b872-2890984a7af8)
 Call ID: 8cfaaf21-6475-4bd1-b872-2890984a7af8
  Args:
    target: Prince_George_of_Greece_and_Denmark
    relation: :hasFather
    source: Eugenie
  AddTriple (16b6a0b4-7387-4d94-87b0-8415a1800c5e)
 Call ID: 16b6a0b4-7387-4d94-87b0-8415a1800c5e
  Args:
    source: Eugenie
    target: Princess_Marie_Bonaparte
    relation: :hasMother
  AssignClass (84fd8b35-d5b7-42d1-893b-b80a3bc4cadf)
 Call ID: 84fd8b35-d5b7-42d1-893b-b80a3bc4cadf
  Args:
    type: :Man
    source: King_George_I_of_Greece
  AssignClass (e3ebdd23-3212-4132-a1ad-6891e5642ece)
 Call ID: e3ebdd23-3212-4132-a1ad-6891e5642ece
  Args:
    type: :Person
    source: King_George_I_of_Greece
  AddTriple (5cd2e26a-7d91-4859-926a-53dd8f1f05a3)
 Call ID: 5cd2e26a-7d91-4859-926a-53dd8f1f05a3
  Args:
    source: Prince_George_of_Greece_and_Denmark
    target: King_George_I_of_Greece
    relation: :hasFather
  AssignClass (f1fe7c1e-358d-41a6-92dc-60e6c991f102)
 Call ID: f1fe7c1e-358d-41a6-92dc-60e6c991f102
  Args:
    type: :Man
    source: Prince_Roland_Bonaparte
  AssignClass (fb80c0cf-5161-4474-aef1-74010eaeb6a0)
 Call ID: fb80c0cf-5161-4474-aef1-74010eaeb6a0
  Args:
    type: :Person
    source: Prince_Roland_Bonaparte
  AssignClass (d91df1df-1f9b-456f-9f3e-2a7c7667e59b)
 Call ID: d91df1df-1f9b-456f-9f3e-2a7c7667e59b
  Args:
    source: Marie-Felix_Blanc
    type: :Woman
  AssignClass (ce452d55-f358-48e9-9a05-9aed6e3a0d7a)
 Call ID: ce452d55-f358-48e9-9a05-9aed6e3a0d7a
  Args:
    type: :Person
    source: Marie-Felix_Blanc
  AddTriple (ca103e8f-44a1-4e51-bf34-e2de71c39a0d)
 Call ID: ca103e8f-44a1-4e51-bf34-e2de71c39a0d
  Args:
    target: Prince_Roland_Bonaparte
    relation: :hasFather
    source: Princess_Marie_Bonaparte
  AddTriple (f0ce2333-35c8-41da-93e2-be7af4329bb7)
 Call ID: f0ce2333-35c8-41da-93e2-be7af4329bb7
  Args:
    relation: :hasMother
    target: Marie-Felix_Blanc
    source: Princess_Marie_Bonaparte
  AssignClass (7c9910e8-2905-4c28-9ee6-7ba783cc1809)
 Call ID: 7c9910e8-2905-4c28-9ee6-7ba783cc1809
  Args:
    source: Irina_Aleksandrovna_Ovtchinnikova
    type: :Woman
  AssignClass (bb46f1f8-2042-459d-bf6c-fcddb6ca6834)
 Call ID: bb46f1f8-2042-459d-bf6c-fcddb6ca6834
  Args:
    source: Irina_Aleksandrovna_Ovtchinnikova
    type: :Person
  AssignClass (6a39a674-2117-4380-aa5c-205688941211)
 Call ID: 6a39a674-2117-4380-aa5c-205688941211
  Args:
    source: Jehan_de_Monleon
    type: :Man
  AssignClass (42315e6f-f1a5-4266-b007-eecf235bac21)
 Call ID: 42315e6f-f1a5-4266-b007-eecf235bac21
  Args:
    type: :Person
    source: Jehan_de_Monleon
  AssignClass (905121e1-7425-4617-ada0-ad8bf26a6908)
 Call ID: 905121e1-7425-4617-ada0-ad8bf26a6908
  Args:
    type: :Man
    source: Lewis_Sloden
  AssignClass (2f5a48c6-3d02-4f2b-8226-0d55276f95e8)
 Call ID: 2f5a48c6-3d02-4f2b-8226-0d55276f95e8
  Args:
    type: :Person
    source: Lewis_Sloden
  AssignClass (c05deb5f-4bb6-4a87-aca5-69368bf7829e)
 Call ID: c05deb5f-4bb6-4a87-aca5-69368bf7829e
  Args:
    source: Princess_Tatiana_Radziwill
    type: :Woman
  AssignClass (7993c155-9795-4a84-97af-17939c652595)
 Call ID: 7993c155-9795-4a84-97af-17939c652595
  Args:
    source: Princess_Tatiana_Radziwill
    type: :Person
  AssignClass (98782d97-8e47-42e7-8929-977e0c085379)
 Call ID: 98782d97-8e47-42e7-8929-977e0c085379
  Args:
    type: :Man
    source: King_George_II
  AssignClass (79b0ac10-d2f9-4eb6-a61b-bae21f5649ec)
 Call ID: 79b0ac10-d2f9-4eb6-a61b-bae21f5649ec
  Args:
    type: :Person
    source: King_George_II
  AssignClass (f256b54c-324a-4541-a34c-b2ed770d14a1)
 Call ID: f256b54c-324a-4541-a34c-b2ed770d14a1
  Args:
    type: :Man
    source: King_Constantine_I
  AssignClass (7de1ecec-4f60-4866-8a9c-ed1bc3984f49)
 Call ID: 7de1ecec-4f60-4866-8a9c-ed1bc3984f49
  Args:
    source: King_Constantine_I
    type: :Person
  AssignClass (fbbd1c55-bf53-4493-8d37-b39485b8155e)
 Call ID: fbbd1c55-bf53-4493-8d37-b39485b8155e
  Args:
    type: :Woman
    source: Queen_Olga
  AssignClass (4017ed81-3a8b-4127-a00d-b99b44d2f1a1)
 Call ID: 4017ed81-3a8b-4127-a00d-b99b44d2f1a1
  Args:
    type: :Person
    source: Queen_Olga
  AssignClass (cd7dc734-ad28-437d-a121-63eac8f34f6e)
 Call ID: cd7dc734-ad28-437d-a121-63eac8f34f6e
  Args:
    type: :Woman
    source: Queen_Sophia
  AssignClass (6799b2c2-c212-4059-882c-1dd5de810bfc)
 Call ID: 6799b2c2-c212-4059-882c-1dd5de810bfc
  Args:
    type: :Person
    source: Queen_Sophia
  AssignClass (ca3184be-a339-45dd-a114-169120428274)
 Call ID: ca3184be-a339-45dd-a114-169120428274
  Args:
    type: :Woman
    source: Princess_Frederica_of_Hanover
  AssignClass (c3ab1d0c-514d-4c25-8b0c-cc37cfa03d23)
 Call ID: c3ab1d0c-514d-4c25-8b0c-cc37cfa03d23
  Args:
    source: Princess_Frederica_of_Hanover
    type: :Person
  AssignClass (9a44ac31-5518-4322-b993-ac6e27859c20)
 Call ID: 9a44ac31-5518-4322-b993-ac6e27859c20
  Args:
    source: Prince_Paul
    type: :Man
  AssignClass (52d40a66-eb77-470f-a486-a0978a7c7e1d)
 Call ID: 52d40a66-eb77-470f-a486-a0978a7c7e1d
  Args:
    type: :Person
    source: Prince_Paul
  AssignClass (e625eb2c-a843-4f10-8f0a-edf1a376341c)
 Call ID: e625eb2c-a843-4f10-8f0a-edf1a376341c
  Args:
    source: Prince_Valdemar_of_Denmark
    type: :Man
  AssignClass (dc0cc12c-2b17-4414-ab73-59ff0e6af292)
 Call ID: dc0cc12c-2b17-4414-ab73-59ff0e6af292
  Args:
    type: :Person
    source: Prince_Valdemar_of_Denmark
  AssignClass (a7b7c716-0a34-4a2f-a648-6ab89e3cf3bc)
 Call ID: a7b7c716-0a34-4a2f-a648-6ab89e3cf3bc
  Args:
    type: :Man
    source: Prince_Axel_of_Denmark
  AssignClass (820b348b-ee1c-4874-9d97-28a0748875e8)
 Call ID: 820b348b-ee1c-4874-9d97-28a0748875e8
  Args:
    source: Prince_Axel_of_Denmark
    type: :Person
  AssignClass (cdc24257-3dfd-48cc-a6a3-fb897da78db6)
 Call ID: cdc24257-3dfd-48cc-a6a3-fb897da78db6
  Args:
    type: :Man
    source: King_Constantine_II
  AssignClass (cf70291c-6e6a-47fc-a770-0461bd17e753)
 Call ID: cf70291c-6e6a-47fc-a770-0461bd17e753
  Args:
    type: :Person
    source: King_Constantine_II
  AssignClass (071fe350-1c95-4922-b776-367e21052644)
 Call ID: 071fe350-1c95-4922-b776-367e21052644
  Args:
    source: Princess_Irene
    type: :Woman
  AssignClass (f3abc85f-0e61-4a8a-94e6-15a3136c3c74)
 Call ID: f3abc85f-0e61-4a8a-94e6-15a3136c3c74
  Args:
    type: :Person
    source: Princess_Irene
  AssignClass (d58e3289-d57a-4600-a6da-d12f6a6068a2)
 Call ID: d58e3289-d57a-4600-a6da-d12f6a6068a2
  Args:
    type: :Woman
    source: Princess_Sophia_of_Spain
  AssignClass (605312ab-dd0e-4389-82a9-bbd717aeef07)
 Call ID: 605312ab-dd0e-4389-82a9-bbd717aeef07
  Args:
    source: Princess_Sophia_of_Spain
    type: :Person
  AssignClass (90f1353e-eb13-40c7-97ba-73df1e23314e)
 Call ID: 90f1353e-eb13-40c7-97ba-73df1e23314e
  Args:
    type: :Woman
    source: Princess_Anne-Marie_of_Denmark
  AssignClass (778c7b6c-03b2-450c-8649-f0351ea64a8a)
 Call ID: 778c7b6c-03b2-450c-8649-f0351ea64a8a
  Args:
    source: Princess_Anne-Marie_of_Denmark
    type: :Person
  AssignClass (28e00769-f3e9-4a31-a5b5-c40a1e1b158d)
 Call ID: 28e00769-f3e9-4a31-a5b5-c40a1e1b158d
  Args:
    type: :Woman
    source: Princess_Alexia
  AssignClass (19e7e1ec-8459-4c03-a907-4eaaa3e37365)
 Call ID: 19e7e1ec-8459-4c03-a907-4eaaa3e37365
  Args:
    type: :Person
    source: Princess_Alexia
  Finish (af79ac0c-aa09-46a6-8459-aef5e5cc682d)
 Call ID: af79ac0c-aa09-46a6-8459-aef5e5cc682d
  Args: