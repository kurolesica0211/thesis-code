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
  AssignClass (c494b9fd-ccf8-40ab-b518-bbf36e8ba969)
 Call ID: c494b9fd-ccf8-40ab-b518-bbf36e8ba969
  Args:
    type: :Man
    source: Prince_Peter_of_Greece_and_Denmark
  AssignClass (3c00dfab-c251-4a45-a6b1-dab571bc8ba1)
 Call ID: 3c00dfab-c251-4a45-a6b1-dab571bc8ba1
  Args:
    type: :Person
    source: Prince_Peter_of_Greece_and_Denmark
  AddLiteral (4f71335d-2574-4e95-9993-8b2e1c02d540)
 Call ID: 4f71335d-2574-4e95-9993-8b2e1c02d540
  Args:
    literal_value: 1908
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Prince_Peter_of_Greece_and_Denmark
  AddLiteral (0748e845-70dc-4021-8ba8-367722e34227)
 Call ID: 0748e845-70dc-4021-8ba8-367722e34227
  Args:
    relation: :hasDeathYear
    literal_value: 1980
    source: Prince_Peter_of_Greece_and_Denmark
    literal_type: xsd:integer
  AssignClass (c1717879-8ba2-4414-83e8-720e9b419388)
 Call ID: c1717879-8ba2-4414-83e8-720e9b419388
  Args:
    source: Prince_George_of_Greece_and_Denmark
    type: :Man
  AssignClass (452f24a5-3ac3-4deb-abe9-0c943b4d0224)
 Call ID: 452f24a5-3ac3-4deb-abe9-0c943b4d0224
  Args:
    type: :Person
    source: Prince_George_of_Greece_and_Denmark
  AssignClass (f84252ca-69ff-4fc2-885d-447a590b0d64)
 Call ID: f84252ca-69ff-4fc2-885d-447a590b0d64
  Args:
    type: :Woman
    source: Princess_Marie_Bonaparte
  AssignClass (3635e2f7-4f78-48a6-9b8a-1e1e702821f7)
 Call ID: 3635e2f7-4f78-48a6-9b8a-1e1e702821f7
  Args:
    source: Princess_Marie_Bonaparte
    type: :Person
  AddTriple (5b3b744e-d82d-4a10-9c92-2fca3d63e10d)
 Call ID: 5b3b744e-d82d-4a10-9c92-2fca3d63e10d
  Args:
    relation: :hasFather
    source: Prince_Peter_of_Greece_and_Denmark
    target: Prince_George_of_Greece_and_Denmark
  AddTriple (61e4ea66-316d-436e-ac27-a7a426168316)
 Call ID: 61e4ea66-316d-436e-ac27-a7a426168316
  Args:
    target: Princess_Marie_Bonaparte
    relation: :hasMother
    source: Prince_Peter_of_Greece_and_Denmark
  AssignClass (ccd3edcc-3a8c-4350-920e-b637fde43c66)
 Call ID: ccd3edcc-3a8c-4350-920e-b637fde43c66
  Args:
    source: Eugénie
    type: :Woman
  AssignClass (1addbdc9-daf4-48e3-9d26-d53d362bd02b)
 Call ID: 1addbdc9-daf4-48e3-9d26-d53d362bd02b
  Args:
    source: Eugénie
    type: :Person
  AddTriple (8b17b860-0d0f-4524-a9d0-df390ebd5154)
 Call ID: 8b17b860-0d0f-4524-a9d0-df390ebd5154
  Args:
    relation: :hasSister
    source: Prince_Peter_of_Greece_and_Denmark
    target: Eugénie
  AddTriple (769499f4-64ec-406a-829a-d18619706257)
 Call ID: 769499f4-64ec-406a-829a-d18619706257
  Args:
    source: Eugénie
    relation: :hasFather
    target: Prince_George_of_Greece_and_Denmark
  AddTriple (8b675247-abae-4f37-ab89-c60b1767611c)
 Call ID: 8b675247-abae-4f37-ab89-c60b1767611c
  Args:
    source: Eugénie
    relation: :hasMother
    target: Princess_Marie_Bonaparte
  AssignClass (534b0040-d15d-4b80-a1f5-afdbf0a5bca3)
 Call ID: 534b0040-d15d-4b80-a1f5-afdbf0a5bca3
  Args:
    type: :Man
    source: King_George_I_of_Greece
  AssignClass (08108e3d-cd1d-4062-ba80-b677a49eed6f)
 Call ID: 08108e3d-cd1d-4062-ba80-b677a49eed6f
  Args:
    type: :Person
    source: King_George_I_of_Greece
  AddTriple (51648de1-a3ce-4ae1-bf84-704ef9cf1f6a)
 Call ID: 51648de1-a3ce-4ae1-bf84-704ef9cf1f6a
  Args:
    source: Prince_George_of_Greece_and_Denmark
    relation: :hasFather
    target: King_George_I_of_Greece
  AssignClass (c25e8af0-aed1-4ed3-98ff-3fb4343e2a2c)
 Call ID: c25e8af0-aed1-4ed3-98ff-3fb4343e2a2c
  Args:
    type: :Man
    source: Prince_Roland_Bonaparte
  AssignClass (2bf174da-316c-41fb-943a-4b284e73675f)
 Call ID: 2bf174da-316c-41fb-943a-4b284e73675f
  Args:
    source: Prince_Roland_Bonaparte
    type: :Person
  AssignClass (23a2f7e0-9bca-4e79-9b12-a45de4396862)
 Call ID: 23a2f7e0-9bca-4e79-9b12-a45de4396862
  Args:
    type: :Woman
    source: Marie-Félix_Blanc
  AssignClass (85ff437b-51e4-4feb-b441-e75a391d3a8a)
 Call ID: 85ff437b-51e4-4feb-b441-e75a391d3a8a
  Args:
    source: Marie-Félix_Blanc
    type: :Person
  AddTriple (458b6ad6-2d7a-4ff4-a090-1b9fab2adb5e)
 Call ID: 458b6ad6-2d7a-4ff4-a090-1b9fab2adb5e
  Args:
    target: Prince_Roland_Bonaparte
    relation: :hasFather
    source: Princess_Marie_Bonaparte
  AddTriple (bfdbfc11-26f1-4b25-9711-d6561d4d1d64)
 Call ID: bfdbfc11-26f1-4b25-9711-d6561d4d1d64
  Args:
    source: Princess_Marie_Bonaparte
    relation: :hasMother
    target: Marie-Félix_Blanc
  AssignClass (47c29546-cc60-4b01-a2e0-9135e5d20389)
 Call ID: 47c29546-cc60-4b01-a2e0-9135e5d20389
  Args:
    source: Irina_Aleksandrovna_Ovtchinnikova
    type: :Woman
  AssignClass (6bd7f402-59a0-48c3-a3da-60ac87c91b5f)
 Call ID: 6bd7f402-59a0-48c3-a3da-60ac87c91b5f
  Args:
    type: :Person
    source: Irina_Aleksandrovna_Ovtchinnikova
  AssignClass (efc2ccdd-6361-477e-abc6-df696c40b927)
 Call ID: efc2ccdd-6361-477e-abc6-df696c40b927
  Args:
    source: Princess_Tatiana_Radziwill
    type: :Woman
  AssignClass (2d09c4d2-a4ba-498e-b816-f5d1f2af426a)
 Call ID: 2d09c4d2-a4ba-498e-b816-f5d1f2af426a
  Args:
    type: :Person
    source: Princess_Tatiana_Radziwill
  AddTriple (dfe36823-e076-490d-868c-e02932edd1cb)
 Call ID: dfe36823-e076-490d-868c-e02932edd1cb
  Args:
    target: Eugénie
    relation: :hasMother
    source: Princess_Tatiana_Radziwill
  AssignClass (df8aafcb-f96c-45ef-9a01-f0c3d620022a)
 Call ID: df8aafcb-f96c-45ef-9a01-f0c3d620022a
  Args:
    type: :Man
    source: Prince_Valdemar_of_Denmark
  AssignClass (caf98e2e-998c-4a76-960c-715158a0ad3e)
 Call ID: caf98e2e-998c-4a76-960c-715158a0ad3e
  Args:
    source: Prince_Valdemar_of_Denmark
    type: :Person
  AssignClass (852388e3-88b8-4229-b320-bb858c9c5886)
 Call ID: 852388e3-88b8-4229-b320-bb858c9c5886
  Args:
    type: :Man
    source: King_George_II
  AssignClass (dd88b9f5-fe99-4b01-b05b-17306f8b8af3)
 Call ID: dd88b9f5-fe99-4b01-b05b-17306f8b8af3
  Args:
    source: King_George_II
    type: :Person
  AssignClass (5783fdc1-7d69-4bf7-b080-6b35eb0d0d9a)
 Call ID: 5783fdc1-7d69-4bf7-b080-6b35eb0d0d9a
  Args:
    type: :Man
    source: King_Constantine_I
  AssignClass (280bd85f-a5a4-4be1-80e4-108d2a198e02)
 Call ID: 280bd85f-a5a4-4be1-80e4-108d2a198e02
  Args:
    source: King_Constantine_I
    type: :Person
  AssignClass (7fd185e6-c82b-4216-8c85-ca2f4f41ede6)
 Call ID: 7fd185e6-c82b-4216-8c85-ca2f4f41ede6
  Args:
    source: Queen_Olga
    type: :Woman
  AssignClass (6991147a-b84f-4c79-83f9-d05b30c98521)
 Call ID: 6991147a-b84f-4c79-83f9-d05b30c98521
  Args:
    source: Queen_Olga
    type: :Person
  AssignClass (6d6e4ba7-51b2-453c-83c3-91c67833a9b2)
 Call ID: 6d6e4ba7-51b2-453c-83c3-91c67833a9b2
  Args:
    type: :Woman
    source: Queen_Sophia
  AssignClass (0fcfcec9-41e1-466f-94c2-7bb43d5031d2)
 Call ID: 0fcfcec9-41e1-466f-94c2-7bb43d5031d2
  Args:
    type: :Person
    source: Queen_Sophia
  AssignClass (5d882741-b43d-4a77-b53f-75a1d0a246bc)
 Call ID: 5d882741-b43d-4a77-b53f-75a1d0a246bc
  Args:
    type: :Man
    source: Prince_Paul
  AssignClass (1b305db3-8560-4d2f-87f0-2fb17e334c61)
 Call ID: 1b305db3-8560-4d2f-87f0-2fb17e334c61
  Args:
    type: :Person
    source: Prince_Paul
  AssignClass (c804ab5c-5ee8-4267-b0b6-c0933c51b53a)
 Call ID: c804ab5c-5ee8-4267-b0b6-c0933c51b53a
  Args:
    type: :Woman
    source: Princess_Frederica_of_Hanover
  AssignClass (94ac66af-d73e-4a85-8247-c668e0be00b2)
 Call ID: 94ac66af-d73e-4a85-8247-c668e0be00b2
  Args:
    type: :Person
    source: Princess_Frederica_of_Hanover
  AssignClass (029f55fe-fd15-4047-8307-f3d920b0d7a4)
 Call ID: 029f55fe-fd15-4047-8307-f3d920b0d7a4
  Args:
    source: Jehan_de_Monléon
    type: :Man
  AssignClass (7e494ab1-8f22-4c90-924f-04c5cdab8b46)
 Call ID: 7e494ab1-8f22-4c90-924f-04c5cdab8b46
  Args:
    source: Jehan_de_Monléon
    type: :Person
  AssignClass (b39116a3-3bad-477d-8709-5df91c34f41f)
 Call ID: b39116a3-3bad-477d-8709-5df91c34f41f
  Args:
    source: Lewis_Sloden
    type: :Man
  AssignClass (feb764d4-cfff-43bd-aed6-5ae8f09681bb)
 Call ID: feb764d4-cfff-43bd-aed6-5ae8f09681bb
  Args:
    type: :Person
    source: Lewis_Sloden
  AssignClass (9e1d8452-08d8-418d-bcbb-15d4749c8227)
 Call ID: 9e1d8452-08d8-418d-bcbb-15d4749c8227
  Args:
    source: Prince_Axel_of_Denmark
    type: :Man
  AssignClass (fcffdba6-4da7-45dd-a163-39c5e4e56291)
 Call ID: fcffdba6-4da7-45dd-a163-39c5e4e56291
  Args:
    type: :Person
    source: Prince_Axel_of_Denmark
  AssignClass (e21b946f-5f08-4493-b8e8-3bcb626464ee)
 Call ID: e21b946f-5f08-4493-b8e8-3bcb626464ee
  Args:
    type: :Man
    source: King_Constantine_II
  AssignClass (be17fc58-a272-4da3-bb7c-31190fd52c05)
 Call ID: be17fc58-a272-4da3-bb7c-31190fd52c05
  Args:
    source: King_Constantine_II
    type: :Person
  AssignClass (832bae4c-9185-461f-a139-3f8c3d011ba2)
 Call ID: 832bae4c-9185-461f-a139-3f8c3d011ba2
  Args:
    type: :Woman
    source: Princess_Irene
  AssignClass (e85d00b0-be4a-42df-9b4c-41e3fbb7c925)
 Call ID: e85d00b0-be4a-42df-9b4c-41e3fbb7c925
  Args:
    type: :Person
    source: Princess_Irene
  AssignClass (c551d1f3-37c3-4bd0-9568-3e3010e3a6f4)
 Call ID: c551d1f3-37c3-4bd0-9568-3e3010e3a6f4
  Args:
    type: :Woman
    source: Princess_Sophia_of_Greece
  AssignClass (585ba8b3-6ef3-4689-8ebf-6ca5cf1a11ef)
 Call ID: 585ba8b3-6ef3-4689-8ebf-6ca5cf1a11ef
  Args:
    source: Princess_Sophia_of_Greece
    type: :Person
  AssignClass (955ddd31-2d41-4205-8cd7-2d751ec8485c)
 Call ID: 955ddd31-2d41-4205-8cd7-2d751ec8485c
  Args:
    source: Princess_Anne-Marie_of_Denmark
    type: :Woman
  AssignClass (6b1a9cbe-d848-4a61-8e40-aabdc39511a7)
 Call ID: 6b1a9cbe-d848-4a61-8e40-aabdc39511a7
  Args:
    type: :Person
    source: Princess_Anne-Marie_of_Denmark
  AssignClass (26cb61b4-3e95-4868-9636-db8a8cb69af1)
 Call ID: 26cb61b4-3e95-4868-9636-db8a8cb69af1
  Args:
    source: Princess_Alexia
    type: :Woman
  AssignClass (13fa1bd2-5ebd-4bc3-b3cc-3d9b46460d1c)
 Call ID: 13fa1bd2-5ebd-4bc3-b3cc-3d9b46460d1c
  Args:
    type: :Person
    source: Princess_Alexia
  Finish (90331ad2-8c1c-4651-8be7-2c6c900eb45f)
 Call ID: 90331ad2-8c1c-4651-8be7-2c6c900eb45f
  Args: