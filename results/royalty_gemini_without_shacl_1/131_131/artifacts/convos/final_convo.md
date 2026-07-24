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
King Juan Carlos IQueen Sofía


The Duchess of Soria and HernaniThe Duke of Soria and Hernani


The Dowager Duchess of Calabria


Leonor, Princess of Asturias
(Leonor de Todos los Santos de Borbón y Ortiz; born 31 October 2005) is the heir presumptive to the Spanish throne.
She is the elder daughter of King Felipe VI and Queen Letizia.
Leonor was born during the reign of her paternal grandfather, King Juan Carlos I.
On 17 August 2023, Leonor joined the General Military Academy to start her 3-year military education.
In 2014, following her father's accession to the throne after the abdication of her grandfather, Leonor was granted all the traditional titles of the heir to the Spanish crown.
These are Princess of Asturias, Princess of Girona, Princess of Viana, Duchess of Montblanc, Countess of Cervera, and Lady of Balaguer.
Leonor was formally proclaimed heir before the Cortes on 31 October 2023, her 18th birthday.
Should Leonor ascend to the throne as expected, she will be Spain's first queen regnant since her fourth great-grandmother Isabella II, who reigned from 1833 to 1868.
Early life and education

Leonor was born on 31 October 2005 at 01:46, three weeks before her due date, to Felipe and Letizia, then the Prince and Princess of Asturias, during the reign of her paternal grandfather, King Juan Carlos I, in the Ruber International Hospital in Madrid using a caesarean section necessitated by non-progression of labour.
Shortly after her birth, Leonor's umbilical cord stem cells were sent to a blood bank in Tucson, Arizona.
This decision sparked public debate in Spain, as the blood bank was private and located abroad.
Leonor left the Ruber International Hospital with her parents on 7 November 2005.
Like her father, Leonor was baptised – with water from the Jordan River – in a Romanesque baptismal font that has been used to christen Spanish princes since the 17th century.
Her godparents were her paternal grandparents, King Juan Carlos I and Queen Sofía.
She received the name of Leonor de Todos los Santos.
During her early months, Leonor developed a small angioma, a benign tumor of blood vessels, on her nose.
Leonor's education began at Escuela Infantil Guardia Real, the daycare for the children of the Spanish Royal Guard.
Leonor was reported to have good grades during her studies in Rosales.
In September 2021, Leonor began studying a 2-year International Baccalaureate program at the UWC Atlantic College in the Llantwit Major, Wales.
Leonor also attended summer camps in the United States.
She is fluent in Spanish, Catalan and English (the latter learnt from her British nanny and also from her grandmother, Queen Sofía) and has studied French, Galician, Basque, Arabic and Mandarin.
Military service

In preparation for her role as Spain's commander-in-chief, following her father's footsteps, Leonor is currently spending three years of army, naval and air force training at the General Military Academy in Zaragoza, the Naval Military Academy in Marín and the General Air Academy in Murcia, respectively.
In this sense, in March 2023, the minister of defense, Margarita Robles, announced that the government had approved a royal decree for Leonor to begin a 3-year military training education program.
Leonor chose to use both of her parents surnames "Borbón Ortiz" in her military career.
Also, whilst attending the military academies, Leonor will renounce her salary and any money that cadets receive.
Leonor swore an oath of allegiance to the Spanish flag at the General Military Academy on 7 October 2023, in the presence of her parents.
In January 2024, Leonor participated in the 24th Sports Championship of Military Academies for Officers, competing in fencing and volleyball as one of the representatives of the General Military Academy.
Leonor was promoted to the rank of Cadet Ensign (Spanish: Alférez) and awarded the Grand Cross of Military Merit by her father King Felipe VI on 3 July 2024.
In September 2024, Leonor and other students from the Naval School conducted seamanship instruction activities in the Pontevedra Estuary.
On 8 January 2025, she boarded the training ship Juan Sebastián de Elcano, beginning three days later a five-month voyage in which she trained as a sailor and visited many Latin American countries, as well as New York City.
After disembarking at this last port, the heir to the Crown returned to Spain by plane to embark for a month on the frigate Blas de Lezo, where she participated in naval maneuvers with live fire.
On 16 July 2025, Leonor was promoted to the rank of as Midshipman of 2nd grade and awarded the Grand Cross of Naval Merit by her father.
On 1 September 2025, Leonor started her third and final year of military training in the General Air and Space Academy in San Javier.
On 25 April 2026, Leonor participated in the 25th Inter-University Canoeing Regatta held in Santiago de la Ribera, on the Mar Menor.
Princess of Asturias

Early years

In May 2014, Leonor made her first official visit to the San Javier Air Force base in Murcia.
On 18 June 2014, King Juan Carlos signed the Abdication Act, and the following day at the stroke of midnight (18–19 June 2014)
Leonor's father ascended the throne becoming King Felipe VI, and Leonor became his heir presumptive and Princess of Asturias.
In October 2014, a wax figure of Leonor was unveiled at the Museo de Cera in Madrid.
On 20 May 2015, Leonor received First Communion as per Catholic custom.
According to the Spanish constitution of 1978, the succession to the Spanish throne is under a system of male-preference cognatic primogeniture, meaning that Leonor, as the elder of Felipe's two daughters, is first in line to inherit the throne.
Under the current law, however, if her father has a legitimate son while still king, Leonor would be displaced in the line of succession and again become an infanta of Spain.
There have been discussions about changing the succession law to absolute primogeniture, allowing for the inheritance of the eldest child, regardless of sex; however, the birth of Leonor, followed by that of her younger sister Sofía, stalled these plans.
Coinciding with the 50th birthday of King Felipe, in January 2018, the King officially gave Leonor the collar of the Golden Fleece in a ceremony at the Royal Palace of Madrid.
In September 2018, Leonor conducted her first public engagement outside the palace by accompanying her parents to Covadonga to celebrate the 1300th anniversary of the Kingdom of Asturias.
On 31 October 2018, Leonor gave her first public speech, held at the Instituto Cervantes in Madrid, where she read the first article of the Constitution of Spain.
She made her first significant speech at Premio Princesa de Asturias on 18 October 2019.
She made her first speech on 4 November 2019 at the Princess of Girona Foundation awards in Barcelona, in which she spoke in Spanish, Catalan, English and Arabic.
Leonor carried out her first public solo engagement on 24 March 2021 by attending a ceremony to mark the 30th anniversary of the Instituto Cervantes.
Leonor made her first official international trip on 16 July 2022.
She did it without the presence of her parents, although she was accompanied by her younger sister, Infanta Sofía.
Together, they attended a match between Spain and Denmark at the UEFA Women's Euro 2022.
In December 2022, Leonor visited the Spanish Red Cross headquarters in Madrid where she met young volunteers of The Red Cross Youth, the youth section of the Spanish Red Cross.
In July 2025 she alongside Infanta Sofía attended the match between England and Spain for the UEFA Women’s Euro 2025.
Heir's oath

The Royal Household made public on 22 September 2023 that, as required under the Spanish Constitution, the princess would swear allegiance to the Constitution and the King upon reaching the age of majority.
At the  Palacio de las Cortes the royal family received state honors, and the Princess of Asturias took her oath before a joint session of the Spanish Parliament, which received her oath with an ovation of more than four minutes.
After this ceremony, the royal family and the main authorities of the country went to the Royal Palace, where her father, King Felipe, awarded her with the Collar of the Order of Charles III, the highest civil honor in Spain.
The entire paternal and maternal family attended this private event, as well as the Greek royal family, represented by Queen Anne-Marie and Princess Alexia and her husband, some members of the House of Bourbon-Two Sicilies including Prince Pedro, Duke of Calabria, representatives of the Bulgarian royal family, and Princess Miriam Ghazi.
Official agenda

On 6 January 2024, Leonor attended the Pascua Militar for the first time, a more than two-centuries-old Spanish military celebration.
On 12 July 2024, Leonor made her first official foreign visit.
In this trip, Leonor, who was accompanied by the Portuguese leader, the Spanish foreign minister, José Manuel Albares, and the private secretary to the king, Camilo Villarino, focused her activities on environmental protection and ocean conservation, visiting the Lisbon Oceanarium and attending a debate on ocean protection.
She also visited the Jerónimos Monastery, where she paid tribute to the poet Luís de Camões, and later went to Belém Palace, where delegations from both countries met and had a lunch, and where President Rebelo de Sousa awarded Leonor the Grand Cross of the Military Order of Christ.
On 25 October 2024, she attended the Princess of Asturias Awards ceremony for the first time as an adult, being in charge of giving the speech to the winners and, later, declaring the event closed and convening the awards for its next edition.
On 4 August 2025, Leonor along with her sister Infanta Sofía attended the annual reception at Marivent Palace for authorities and relevant citizens of the Balearic Islands.
The reception was also attended by King Felipe VI, Queen Letizia, and Queen Sofía.
This event marked the first reception attended by Leonor and Sofía.
From 26 to 27 September 2025, Leonor made an official visit —with her parents— to the Chartered Community of Navarre.
The two-day trip was made to celebrate the 600th anniversary of the title of Princess of Viana, one of the titles of the heir to the Crown —as heir of the ancient Kingdom of Navarre—.
On 24 October 2025, she presided over the seventh edition of the Princess of Asturias Awards.
As Leonor is the heir to the throne, King Felipe confessed the 2026 ceremony would only be her presiding over it.
Titles, styles, honours and arms

As children of the prince of Asturias, Leonor was born infanta and initially styled "Her Royal Highness Infanta Doña Leonor".
Upon her father's accession to the throne, Leonor became the heir presumptive to the Spanish throne, and she inherited the traditional titles of the heir:
Princess of Asturias, Princess of Girona, Princess of Viana, Duchess of Montblanc, Countess of Cervera and Lady of Balaguer.
Leonor is the 36th person to bear the title of princess of Asturias since its creation in 1388.
Since then, Leonor is generally styled as "Her Royal Highness The Princess of Asturias", although depending on the province of the country, another title may be added.
For example, when visiting the territories of the former Crown of Aragon, she is usually titled "Her Royal Highness the Princess of Asturias and Girona" and, in Navarre, she is referred as "Her Royal Highness the Princess of Asturias and Viana".
Honours

As heir to the throne, she is the nominal chairwoman of the Princess of Asturias Foundation and the Princess of Girona Foundation.
Coins

On 31 October 2023, the Royal Mint of Spain minted a gold-silver coin which depicts Leonor, to commemorate her coming of age as an emblematic event.
Other

A collector stamp was made in her honor alongside her father King Felipe, to commemorate 50 years since the end of the dictatorship of former leader Francisco Franco.



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
  AssignClass (a6975abd-1b16-46e2-b6e0-f2c254dad0e6)
 Call ID: a6975abd-1b16-46e2-b6e0-f2c254dad0e6
  Args:
    source: King Juan Carlos I
    type: :Man
  AssignClass (42fb3f2a-37ff-462b-b065-d4eb210cb4d7)
 Call ID: 42fb3f2a-37ff-462b-b065-d4eb210cb4d7
  Args:
    source: Queen Sofía
    type: :Woman
  AssignClass (975ef055-42fc-454b-9c63-f9be49f075af)
 Call ID: 975ef055-42fc-454b-9c63-f9be49f075af
  Args:
    type: :Man
    source: King Felipe VI
  AssignClass (6c1d2a58-be48-40de-8835-fddb1ad9a45a)
 Call ID: 6c1d2a58-be48-40de-8835-fddb1ad9a45a
  Args:
    type: :Woman
    source: Queen Letizia
  AssignClass (91a8b62d-6dbf-4413-bad4-dbfab3a536ba)
 Call ID: 91a8b62d-6dbf-4413-bad4-dbfab3a536ba
  Args:
    source: Leonor, Princess of Asturias
    type: :Woman
  AssignClass (2ec66014-531f-415d-a012-5530dc01a4fe)
 Call ID: 2ec66014-531f-415d-a012-5530dc01a4fe
  Args:
    type: :Woman
    source: Infanta Sofía
  AddLiteral (614e057a-6be2-49e5-8911-1ec0f5ee18a9)
 Call ID: 614e057a-6be2-49e5-8911-1ec0f5ee18a9
  Args:
    source: Leonor, Princess of Asturias
    literal_value: 2005
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddTriple (a32014b6-46d7-416d-809b-0ab8e519c514)
 Call ID: a32014b6-46d7-416d-809b-0ab8e519c514
  Args:
    source: Leonor, Princess of Asturias
    target: King Felipe VI
    relation: :hasFather
  AddTriple (4da2e206-a244-4bb1-8902-d4743393bf62)
 Call ID: 4da2e206-a244-4bb1-8902-d4743393bf62
  Args:
    relation: :hasMother
    target: Queen Letizia
    source: Leonor, Princess of Asturias
  AddTriple (8906a72c-a51a-4ded-80db-2ce8405636c8)
 Call ID: 8906a72c-a51a-4ded-80db-2ce8405636c8
  Args:
    source: King Felipe VI
    target: King Juan Carlos I
    relation: :hasFather
  AddTriple (30049702-1404-4446-aed9-38fa8198e906)
 Call ID: 30049702-1404-4446-aed9-38fa8198e906
  Args:
    relation: :hasMother
    target: Queen Sofía
    source: King Felipe VI
  AddTriple (3e74528b-eae1-4160-b8ba-aee30de5dea9)
 Call ID: 3e74528b-eae1-4160-b8ba-aee30de5dea9
  Args:
    source: Infanta Sofía
    target: King Felipe VI
    relation: :hasFather
  AddTriple (23a361cd-fc60-451d-aa50-73ae996e58e3)
 Call ID: 23a361cd-fc60-451d-aa50-73ae996e58e3
  Args:
    relation: :hasMother
    target: Queen Letizia
    source: Infanta Sofía
  Finish (297e5193-ebca-447c-9edf-810311bb2287)
 Call ID: 297e5193-ebca-447c-9edf-810311bb2287
  Args: