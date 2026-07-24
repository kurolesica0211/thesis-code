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
  AssignClass (e6bccbd6-b5e3-47b5-b78c-a6521d4d710a)
 Call ID: e6bccbd6-b5e3-47b5-b78c-a6521d4d710a
  Args:
    source: Prince_Peter_of_Greece_and_Denmark
    type: :Man
  AssignClass (6dfb9097-af91-41f4-9248-46715dd5c66d)
 Call ID: 6dfb9097-af91-41f4-9248-46715dd5c66d
  Args:
    source: Prince_Peter_of_Greece_and_Denmark
    type: :Person
  AddLiteral (bfbd443f-98a9-45db-b5f5-f53c24ce1e17)
 Call ID: bfbd443f-98a9-45db-b5f5-f53c24ce1e17
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Prince_Peter_of_Greece_and_Denmark
    literal_value: 1908
  AddLiteral (264bae93-0197-4819-88f6-85ee442acb75)
 Call ID: 264bae93-0197-4819-88f6-85ee442acb75
  Args:
    literal_value: 1980
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: Prince_Peter_of_Greece_and_Denmark
  AssignClass (8171afd1-6c36-47a3-9dd3-56d5c54b24b9)
 Call ID: 8171afd1-6c36-47a3-9dd3-56d5c54b24b9
  Args:
    source: Irina_Aleksandrovna_Ovtchinnikova
    type: :Woman
  AssignClass (34c21305-4efc-42aa-86ba-f8cd40fa295b)
 Call ID: 34c21305-4efc-42aa-86ba-f8cd40fa295b
  Args:
    type: :Person
    source: Irina_Aleksandrovna_Ovtchinnikova
  AssignClass (c6447ca8-4d47-4af8-8acb-25b413e75dad)
 Call ID: c6447ca8-4d47-4af8-8acb-25b413e75dad
  Args:
    source: Prince_George_of_Greece_and_Denmark
    type: :Man
  AssignClass (e2b2e70b-3ec4-4dfe-9b7b-ed147c510d64)
 Call ID: e2b2e70b-3ec4-4dfe-9b7b-ed147c510d64
  Args:
    source: Prince_George_of_Greece_and_Denmark
    type: :Person
  AssignClass (70eca6fa-082e-4012-af6f-d9069c334624)
 Call ID: 70eca6fa-082e-4012-af6f-d9069c334624
  Args:
    type: :Woman
    source: Princess_Marie_Bonaparte
  AssignClass (e007fdd3-a143-4cf0-b917-0b6b38e8c82f)
 Call ID: e007fdd3-a143-4cf0-b917-0b6b38e8c82f
  Args:
    source: Princess_Marie_Bonaparte
    type: :Person
  AddTriple (4f90f245-ad97-4ffc-b5b5-b15b5aedc8cf)
 Call ID: 4f90f245-ad97-4ffc-b5b5-b15b5aedc8cf
  Args:
    relation: :hasFather
    target: Prince_George_of_Greece_and_Denmark
    source: Prince_Peter_of_Greece_and_Denmark
  AddTriple (60b69888-e28e-49eb-8f80-7902bd5c9ba7)
 Call ID: 60b69888-e28e-49eb-8f80-7902bd5c9ba7
  Args:
    source: Prince_Peter_of_Greece_and_Denmark
    relation: :hasMother
    target: Princess_Marie_Bonaparte
  AssignClass (f3e791e7-e1b8-4790-8299-5f0ffdbc94a2)
 Call ID: f3e791e7-e1b8-4790-8299-5f0ffdbc94a2
  Args:
    type: :Man
    source: King_George_I_of_Greece
  AssignClass (608408f3-9715-432d-a703-aa0d6883281b)
 Call ID: 608408f3-9715-432d-a703-aa0d6883281b
  Args:
    type: :Person
    source: King_George_I_of_Greece
  AddTriple (21ffc4f5-7ac2-4ff6-9e57-ca6383ca6c1e)
 Call ID: 21ffc4f5-7ac2-4ff6-9e57-ca6383ca6c1e
  Args:
    source: Prince_George_of_Greece_and_Denmark
    target: King_George_I_of_Greece
    relation: :hasFather
  AssignClass (ceb126dd-5928-405e-b363-17711f3e58c7)
 Call ID: ceb126dd-5928-405e-b363-17711f3e58c7
  Args:
    source: Prince_Roland_Bonaparte
    type: :Man
  AssignClass (2973b85e-eb1f-4a57-8bfd-1d589afc2f32)
 Call ID: 2973b85e-eb1f-4a57-8bfd-1d589afc2f32
  Args:
    type: :Person
    source: Prince_Roland_Bonaparte
  AssignClass (cf302482-c0e8-431e-bb20-86aa46f80346)
 Call ID: cf302482-c0e8-431e-bb20-86aa46f80346
  Args:
    type: :Woman
    source: Marie-Felix_Blanc
  AssignClass (1e213319-7f5f-4e96-a93d-2786383cdfce)
 Call ID: 1e213319-7f5f-4e96-a93d-2786383cdfce
  Args:
    source: Marie-Felix_Blanc
    type: :Person
  AddTriple (1c3b03cd-7192-4113-92e4-887399aefa40)
 Call ID: 1c3b03cd-7192-4113-92e4-887399aefa40
  Args:
    source: Princess_Marie_Bonaparte
    relation: :hasFather
    target: Prince_Roland_Bonaparte
  AddTriple (3b11e42e-b2d9-4eaa-acb8-3259fe0c1834)
 Call ID: 3b11e42e-b2d9-4eaa-acb8-3259fe0c1834
  Args:
    source: Princess_Marie_Bonaparte
    relation: :hasMother
    target: Marie-Felix_Blanc
  AssignClass (e7563823-d6fe-4bd5-9aab-009a29476080)
 Call ID: e7563823-d6fe-4bd5-9aab-009a29476080
  Args:
    type: :Woman
    source: Eugenie
  AssignClass (1e626704-e7ad-4cca-a681-491cde4f8bca)
 Call ID: 1e626704-e7ad-4cca-a681-491cde4f8bca
  Args:
    type: :Person
    source: Eugenie
  AddTriple (8d739bc8-9633-4489-b1bd-13cf9098f311)
 Call ID: 8d739bc8-9633-4489-b1bd-13cf9098f311
  Args:
    target: Eugenie
    relation: :isSiblingOf
    source: Prince_Peter_of_Greece_and_Denmark
  AddTriple (13295ad5-65d6-4816-87d3-ad5b15872387)
 Call ID: 13295ad5-65d6-4816-87d3-ad5b15872387
  Args:
    source: Eugenie
    relation: :hasFather
    target: Prince_George_of_Greece_and_Denmark
  AddTriple (220442f1-5d29-4d6f-ac6a-0cb07c6d7e25)
 Call ID: 220442f1-5d29-4d6f-ac6a-0cb07c6d7e25
  Args:
    relation: :hasMother
    target: Princess_Marie_Bonaparte
    source: Eugenie
  AssignClass (0610c8f9-102f-4a77-8a86-b4e4fa32304f)
 Call ID: 0610c8f9-102f-4a77-8a86-b4e4fa32304f
  Args:
    source: Prince_Valdemar_of_Denmark
    type: :Man
  AssignClass (a91a6373-1681-4211-8a15-4979cbd90200)
 Call ID: a91a6373-1681-4211-8a15-4979cbd90200
  Args:
    type: :Person
    source: Prince_Valdemar_of_Denmark
  AssignClass (53194b53-189b-4e69-9a2c-8bed66e15761)
 Call ID: 53194b53-189b-4e69-9a2c-8bed66e15761
  Args:
    source: King_George_II
    type: :Man
  AssignClass (8356011f-2e37-49c3-8f92-6a998df0f38d)
 Call ID: 8356011f-2e37-49c3-8f92-6a998df0f38d
  Args:
    type: :Person
    source: King_George_II
  AssignClass (49d26cc0-9e93-49d9-9536-e9a2c514703b)
 Call ID: 49d26cc0-9e93-49d9-9536-e9a2c514703b
  Args:
    type: :Man
    source: King_Constantine_I
  AssignClass (849f414c-bee0-4efd-a206-59a3c1f11097)
 Call ID: 849f414c-bee0-4efd-a206-59a3c1f11097
  Args:
    type: :Person
    source: King_Constantine_I
  AssignClass (331349b7-45d0-4e5f-9f56-e247ec1043f1)
 Call ID: 331349b7-45d0-4e5f-9f56-e247ec1043f1
  Args:
    source: Queen_Olga
    type: :Woman
  AssignClass (006b868e-747b-409f-937d-829da09de2e9)
 Call ID: 006b868e-747b-409f-937d-829da09de2e9
  Args:
    type: :Person
    source: Queen_Olga
  AssignClass (196a5af7-bb59-4878-80e2-9219c236e036)
 Call ID: 196a5af7-bb59-4878-80e2-9219c236e036
  Args:
    source: Queen_Sophia
    type: :Woman
  AssignClass (5d7570e0-f366-4316-98e9-68da404db051)
 Call ID: 5d7570e0-f366-4316-98e9-68da404db051
  Args:
    source: Queen_Sophia
    type: :Person
  AssignClass (6e1228ca-487e-4150-bf14-3efe09fe4dbf)
 Call ID: 6e1228ca-487e-4150-bf14-3efe09fe4dbf
  Args:
    source: Princess_Frederica_of_Hanover
    type: :Woman
  AssignClass (85b45044-e427-43f2-9660-f91c8f3f4ac7)
 Call ID: 85b45044-e427-43f2-9660-f91c8f3f4ac7
  Args:
    source: Princess_Frederica_of_Hanover
    type: :Person
  AssignClass (3d748f9f-afba-4a93-a992-d20cb38d29ba)
 Call ID: 3d748f9f-afba-4a93-a992-d20cb38d29ba
  Args:
    source: Prince_Paul
    type: :Man
  AssignClass (0a640d87-29c4-4ccd-b5d2-ae018bedc037)
 Call ID: 0a640d87-29c4-4ccd-b5d2-ae018bedc037
  Args:
    source: Prince_Paul
    type: :Person
  AssignClass (db503093-9b31-4b85-b30e-97114e2b7931)
 Call ID: db503093-9b31-4b85-b30e-97114e2b7931
  Args:
    source: Jehan_de_Monleon
    type: :Man
  AssignClass (8eba42a8-494d-4a91-9b81-a7872b550fbb)
 Call ID: 8eba42a8-494d-4a91-9b81-a7872b550fbb
  Args:
    type: :Person
    source: Jehan_de_Monleon
  AssignClass (13ddc367-abd0-42f4-ba32-75a31ce8b32d)
 Call ID: 13ddc367-abd0-42f4-ba32-75a31ce8b32d
  Args:
    type: :Man
    source: Lewis_Sloden
  AssignClass (63ccca28-eed3-4b55-9c88-c018ea20c76b)
 Call ID: 63ccca28-eed3-4b55-9c88-c018ea20c76b
  Args:
    type: :Person
    source: Lewis_Sloden
  AssignClass (0b85ad24-1842-48c3-b840-f1409edecff1)
 Call ID: 0b85ad24-1842-48c3-b840-f1409edecff1
  Args:
    type: :Woman
    source: Princess_Tatiana_Radziwill
  AssignClass (0d52eb2d-d394-47b0-9218-0f068d249765)
 Call ID: 0d52eb2d-d394-47b0-9218-0f068d249765
  Args:
    source: Princess_Tatiana_Radziwill
    type: :Person
  AssignClass (ce08c6d8-1da3-4f7d-9901-1a7946264d89)
 Call ID: ce08c6d8-1da3-4f7d-9901-1a7946264d89
  Args:
    source: Prince_Axel_of_Denmark
    type: :Man
  AssignClass (a578242d-8492-43e1-b961-a6c03b9634f5)
 Call ID: a578242d-8492-43e1-b961-a6c03b9634f5
  Args:
    source: Prince_Axel_of_Denmark
    type: :Person
  AssignClass (58dece69-1f49-4a9a-a932-02314f3c95a6)
 Call ID: 58dece69-1f49-4a9a-a932-02314f3c95a6
  Args:
    type: :Man
    source: Haslund-Christensen
  AssignClass (f84ce2b2-e278-4225-874e-14047e279342)
 Call ID: f84ce2b2-e278-4225-874e-14047e279342
  Args:
    source: Haslund-Christensen
    type: :Person
  AssignClass (5e86415c-9b89-4598-b4d6-f181d0e02e81)
 Call ID: 5e86415c-9b89-4598-b4d6-f181d0e02e81
  Args:
    type: :Man
    source: King_Constantine_II
  AssignClass (329d5f56-38a3-4fe0-93ff-3a6b374a3e57)
 Call ID: 329d5f56-38a3-4fe0-93ff-3a6b374a3e57
  Args:
    type: :Person
    source: King_Constantine_II
  AssignClass (d4f70fd3-7f0d-437f-a2d3-2e34dc137876)
 Call ID: d4f70fd3-7f0d-437f-a2d3-2e34dc137876
  Args:
    source: Princess_Irene
    type: :Woman
  AssignClass (b39b288f-939e-4788-b5e3-7870bcfa6dca)
 Call ID: b39b288f-939e-4788-b5e3-7870bcfa6dca
  Args:
    type: :Person
    source: Princess_Irene
  AssignClass (00cd21b8-1f3c-4cfd-9dcf-68a7bac68c92)
 Call ID: 00cd21b8-1f3c-4cfd-9dcf-68a7bac68c92
  Args:
    source: Princess_Sophia_of_Greece
    type: :Woman
  AssignClass (6ba0df51-e213-4ff9-a58f-5d19c3b9d757)
 Call ID: 6ba0df51-e213-4ff9-a58f-5d19c3b9d757
  Args:
    type: :Person
    source: Princess_Sophia_of_Greece
  AssignClass (6ac9bfea-cdca-48b7-9af7-f9d77d061c1a)
 Call ID: 6ac9bfea-cdca-48b7-9af7-f9d77d061c1a
  Args:
    source: Princess_Anne-Marie_of_Denmark
    type: :Woman
  AssignClass (d8014556-fbe4-4241-86e3-2fd2fbd34dbb)
 Call ID: d8014556-fbe4-4241-86e3-2fd2fbd34dbb
  Args:
    source: Princess_Anne-Marie_of_Denmark
    type: :Person
  AssignClass (71a46f29-23ef-4647-83ad-563eeedc3a2d)
 Call ID: 71a46f29-23ef-4647-83ad-563eeedc3a2d
  Args:
    source: Princess_Alexia
    type: :Woman
  AssignClass (4d547ca3-8be5-4da3-a409-c780c6b1fb6d)
 Call ID: 4d547ca3-8be5-4da3-a409-c780c6b1fb6d
  Args:
    source: Princess_Alexia
    type: :Person
  Finish (f3175e33-72c3-4f1d-aa83-86d21d0d481f)
 Call ID: f3175e33-72c3-4f1d-aa83-86d21d0d481f
  Args: