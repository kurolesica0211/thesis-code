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
Dom Manuel II (15 November 1889 – 2 July 1932), sometimes known as the Unfortunate (o Desaventurado) or the Patriot (o Patriota), was the last king of Portugal, reigning from 1908 until 1910.
Manuel was born in the Palace of Belém, Lisbon, during the reign of his father, Carlos I.
Manuel entered the naval school in 1907.
After the regicide in 1908, which killed the King and the Prince Royal, Manuel, then 18 years old, became king.
Manuel also ended some traditions, like the traditional hand-kissing ceremony.
During a period of unsustainable political instability the monarchy was overthrown in 1910, which converted Portugal into a republic.
Manuel and his family subsequently fled to exile in the UK.
Manuel died in 1932 aged 42 at Twickenham, Middlesex.
Early life

Manuel was born in the Palace of Belém, Lisbon, less than a month after his father King Carlos I ascended the Portuguese throne.
He was the third child and second son of Carlos and Amélie of Orléans.
The former Emperor Pedro II of Brazil, Manuel II's paternal great-granduncle, who had been deposed from the Brazilian throne on the day of Manuel's birth, attended the ceremony.
Although Manuel was raised as a member of the upper class he took a more populist tone after ascending to the throne, and abandoned many of the court protocols.
Manuel's upbringing included horse riding, fencing, rowing, tennis and gardening.
As a child, Manuel played with the children of Count of Figueiró, Count of Galveias and with other families of the Court.
In 1903, Manuel travelled with his mother and his brother to Egypt, on board the royal yacht Amélia.
According to R. Benton, the trip "may have been decisive in Manuel's decision to enter the Portuguese navy and make it a career."
Lisbon regicide

Manuel's future in the Portuguese Navy was abruptly shelved on 1 February 1908.
On their way to the royal palace, the carriage carrying King Carlos and his family passed through the Terreiro do Paço plaza where shots were fired by at least two Portuguese republican activist revolutionaries: Alfredo Luis da Costa and Manuel Buiça.
The King was killed; Prince Luís Filipe was mortally wounded; Prince Manuel was hit in the arm; Queen Amélie was unharmed.
It was Amélie's quick thinking that saved her younger son.
Days later, Manuel II was proclaimed King of Portugal.
The ambitions of various political parties made Manuel's short reign a turbulent one.
He was protected by his mother, Amélie, and sought out the support of the experienced politician José Luciano de Castro.
In Portugal, owing to lower levels of industrialisation, this was not an important question, but it was exacerbated by an economic crisis and the Republican Party, who believed a republic would resolve the problems.
In 1909, Manuel invited the French sociologist, Léon Poinsard, to examine the social environment and report back to him.
For their part, the Socialists were enthusiastic about Royal support between Manuel and Aquiles Monteverde.
Manuel II informed the government, through the Minister of Public Works, that he agreed with the establishment of the Instituto de Trabalho Nacional, but by September, it was too late for the constitutional monarchy.
During his reign he visited many parts of northern Portugal, in addition to Spain, France, and the United Kingdom, where he was appointed Knight of the Order of the Garter, in November 1909.
During the waning days of King Manuel II's reign, Prior Sardo besought the monarch to bestow Gafanha da Nazaré with a parish, achieving royal recognition, marking the last town to receive such acknowledgment.
The Palace of Necessidades (then official residence of the young King) was bombarded, forcing Manuel to move to the Mafra National Palace, where he rendezvoused with his mother, Queen Amélia, and his grandmother, the Queen Mother Maria Pia of Savoy.
One day later, once it was clear that the Republicans had taken the country, Manuel decided to embark from Ericeira on the royal yacht Amélia IV for Porto, with armed Republicans arriving as the ship departed.
It is unclear whether his advisers motivated Manuel to change his intentions or whether he was forced to change his destination en route, but the Royal Family disembarked in Gibraltar after they received notice that Porto had fallen to the Republicans.
The coup d'état was complete, and the Royal Family departed for exile, arriving in the United Kingdom, where they were received by King George V.


Exile

In exile, Manuel resided in Fulwell Park, Twickenham, now in London (where his mother had been born).
His influence is also recalled by a number of toponymic references in the area: Manuel Road, Lisbon Avenue, and Portugal Gardens.
He followed political events in Portugal, and was concerned with the anarchy of the First Republic, fearing that it could provoke a Spanish intervention and risk the country's independence.
As the ambassador was to negotiate the liquidation of the Portuguese debt to the United Kingdom, the Minister of Foreign Affairs asked Manuel to straighten out the situation.
Even in exile Manuel continued to be a patriot, going as far as declaring in his 1915 testament his intention to transfer his possessions to the Portuguese State for the creation of a museum, and showing his interest in being buried in Portugal.
World War I

Manuel defended the entry of Portugal into the First World War and its active participation.
Manuel believed that supporting Great Britain would guarantee the retention of overseas colonies, which would have been lost to German aggression even if the Germans were supported in the conflict.
Manuel attempted to make himself available to the Allied Powers, wherever they saw use, but was disappointed when he was assigned a post in the British Red Cross.
Manuel's visits to the front were perceived as causing some political embarrassment to the French government, but his friendship with George V was sufficient to alleviate their concerns.
Monarchy and its status

Since 1911, the Portuguese monarchists-in-exile had concentrated in Galicia, Spain, in order to enter Portugal and restore the monarchy but without the tacit approval of the Spanish government.
For his part, Manuel supported these incursions the best way he could, but his financial resources were limited.
Manuel was never able to restore his kingdom by force and always defended that the monarchists should organise internally in order to reach power legally (by elections).
His preoccupation worsened at the beginning of the Great War: Manuel was fearful that the United Kingdom would ally with Spain, in light of Portugal's instability, and that Spain would want to annex Portugal, as the price for Spain's entry into the War.
Dover Pact

After the failure of the first monarchist incursion, and with Manuel II appearing relatively unenthusiastic for a restoration of the monarchy (and entirely against armed counter-revolution), another group of royalists attempted to legitimise the claims of the descendants of Miguel I to the throne.
In order to counter this, the King allegedly entered into direct negotiations with the Duke of Braganza's representatives: he attempted to establish himself as the rightful king and, according to the Integralismo Lusitano group, he recognised the descendants of Miguel as being in line to the throne of Portugal.
There is no proof of an encounter between Manuel II and Miguel in Dover on 30 January 1912.
The results of the supposed meeting remain controversial: although there was an accord on challenging the republic, there remained no clear agreement on hereditary lines of succession, and Manuel II still retained his claim to the throne.
Manuel continued to plead for calm at the end of the War; while not abandoning the possibility of taking action in the future, he insisted on waiting to the end of peace negotiations in Paris: he was fearful that continued anarchy in Portugal would prejudice its negotiating position.
On 19 January 1919 a thousand soldiers, including some artillery, under the command of Paiva Couceiro occupied Porto, in order to restore the Constitutional Monarchy, and its King Manuel II.
Although it is not likely that such a pact took place, it is said that in 1922, with cooling of relations between monarchists of the Integralismo Lusitano and the King, and mindful that his marriage to Augusta Victória had not produced heirs, Manuel, in a Paris meeting in April 1922, represented by his adjunct Aires de Ornelas, and Miguelist representatives Infanta Adelgundes, who was by now calling herself Duchess of Guimarães, and tutor to Duarte Nuno, agreed that owing to an heir, the rights of succession would pass to Duarte Nuno.
Integralismo Lusitano withheld their support, and in September 1925, Aldegundes, in a letter to Manuel, repudiated the agreement owing the continue operation of the Constitutional Newspaper (the Integralist paper was closed as part of the accord) and the lack of Integralist participation.
Death

King Manuel died unexpectedly in his residence on 2 July 1932, via suffocation following an attack of "acute oedema of the glottis", a swelling of the narrow opening at the upper end of the larynx, or tracheal oedema.
After King Manuel's death, the Portuguese National Assembly, under António de Oliveira Salazar's dictatorship, authorised the return of the banned branch of the Braganzas (ex-King Miguel's descendants) on 27 May 1950, repealing the laws of exile of 19 December 1834 and 15 October 1910, and founded, with the sale of the King's English estate and some of his remaining personal possessions, the Foundation of the House of Braganza, according to King Manuel's desire to leave his personal fortune to the Portuguese people.
Legacy

Given the Portuguese tradition of nicknaming their monarchs, king Manuel II was given several of them which differed from each other according to political ideology, the monarchists gave him more positive nicknames such as O Patriota ('The Patriot') for his preoccupation with the national identity, or O Rei-Saudade ('The Missed King'), for the longing that was felt when the monarchy was abolished.
Personal life

In the spring of 1912, Manuel visited Switzerland, where he met Princess Augusta Victoria of Hohenzollern (1890–1966), daughter of William, Prince of Hohenzollern, and was deeply impressed by her.
In the following year, on 4 September 1913, Manuel married Augusta Victoria.
During the Mass, which was celebrated in the Chapel of Sigmaringen Castle, Manuel, wearing his Order of the Garter Star and the sash of the Three Portuguese Orders, stood on a crate containing soil brought from Portugal.
The ceremony was conducted by Cardinal José Sebastião de Almeida Neto, Patriarch of Lisbon, then exiled in Seville, who had baptised Manuel as a young prince; Manuel was also assisted by the Prince of Wales (Edward VIII) and King Alfonso XIII of Spain, as well as representatives of the royal houses of Europe (including Spain, Germany, Italy, France and Romania, in addition to the principalities and German kingdoms).
Bibliographer

Manuel was always an avid reader and, during his exile, dedicated himself to the study of literature, penning treatises on Medieval and Renaissance literature in Portugal.
Initially, he was interested in writing a biography, and began research on a biography of Manuel I of Portugal, who he believed was badly treated by other historians.
By 1926, Manuel had abandoned the idea of a biography and concentrated on descriptions of older books in his library (itself, a complete library of older works).
More than a simple list, the work allowed Manuel to write of the glories of Portugal, writing not just a bibliography but also an examination of the authors and the context of their writings.
The first volume of the work Livros Antigos Portuguezes 1489–1600, da Bibliotheca de Sua Magestade Fidelíssima Descriptos por S. M. El-Rey D. Manuel em Três volumes was published in 1929.
Manuel delivered, by hand, a copy of his work to his friend George V at Windsor Castle.
But the project was terminated prematurely in 1932, when Manuel died unexpectedly: the third volume was posthumously published under the supervision of his librarian, Margery Winters.



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
  AssignClass (52239053-9036-4410-98eb-ae4d129d2cde)
 Call ID: 52239053-9036-4410-98eb-ae4d129d2cde
  Args:
    type: :Man
    source: Manuel_II
  AssignClass (55015ece-6811-47b1-b9f1-9e678f275c9d)
 Call ID: 55015ece-6811-47b1-b9f1-9e678f275c9d
  Args:
    source: Manuel_II
    type: :Person
  AddLiteral (ffa16503-fc0c-4f3e-813f-22463b8bb0ec)
 Call ID: ffa16503-fc0c-4f3e-813f-22463b8bb0ec
  Args:
    literal_type: xsd:integer
    literal_value: 1889
    relation: :hasBirthYear
    source: Manuel_II
  AddLiteral (6179bf5a-e8aa-4260-8d2a-15d293f33bac)
 Call ID: 6179bf5a-e8aa-4260-8d2a-15d293f33bac
  Args:
    literal_type: xsd:integer
    literal_value: 1932
    source: Manuel_II
    relation: :hasDeathYear
  AssignClass (8db9a261-21b1-4ea7-a238-a152049b24a6)
 Call ID: 8db9a261-21b1-4ea7-a238-a152049b24a6
  Args:
    type: :Man
    source: Carlos_I
  AssignClass (56e9e033-ddd1-4605-a1cc-6de472e2f19d)
 Call ID: 56e9e033-ddd1-4605-a1cc-6de472e2f19d
  Args:
    type: :Person
    source: Carlos_I
  AssignClass (c4e46114-d716-48f2-aa72-219fb96df70a)
 Call ID: c4e46114-d716-48f2-aa72-219fb96df70a
  Args:
    type: :Woman
    source: Amelie_of_Orleans
  AssignClass (1fe1a54d-bd2c-4adc-8741-27b63302154a)
 Call ID: 1fe1a54d-bd2c-4adc-8741-27b63302154a
  Args:
    type: :Person
    source: Amelie_of_Orleans
  AddTriple (06f81b29-567e-4ae9-902c-573eb509b4ed)
 Call ID: 06f81b29-567e-4ae9-902c-573eb509b4ed
  Args:
    target: Carlos_I
    source: Manuel_II
    relation: :hasFather
  AddTriple (955d8ecd-55f7-46ba-9891-12f5dbd25a80)
 Call ID: 955d8ecd-55f7-46ba-9891-12f5dbd25a80
  Args:
    target: Amelie_of_Orleans
    relation: :hasMother
    source: Manuel_II
  AssignClass (1a28d1e5-2b6c-414c-a2cd-0f4d4ecf1f21)
 Call ID: 1a28d1e5-2b6c-414c-a2cd-0f4d4ecf1f21
  Args:
    type: :Man
    source: Luis_Filipe
  AssignClass (a9723311-654e-44b5-aa93-81deea8697bc)
 Call ID: a9723311-654e-44b5-aa93-81deea8697bc
  Args:
    type: :Person
    source: Luis_Filipe
  AddTriple (192724e6-fa50-4ff3-9ade-888a6f074ee4)
 Call ID: 192724e6-fa50-4ff3-9ade-888a6f074ee4
  Args:
    source: Luis_Filipe
    relation: :hasFather
    target: Carlos_I
  AddTriple (1be12e88-33f3-48a0-90ae-d7da426f0914)
 Call ID: 1be12e88-33f3-48a0-90ae-d7da426f0914
  Args:
    target: Amelie_of_Orleans
    source: Luis_Filipe
    relation: :hasMother
  AddTriple (9a67a029-e569-4f0e-8351-98be1a43d91f)
 Call ID: 9a67a029-e569-4f0e-8351-98be1a43d91f
  Args:
    target: Luis_Filipe
    relation: :isSiblingOf
    source: Manuel_II
  AssignClass (9b3ec2d8-6d02-4ab4-8f03-00a787c36e2b)
 Call ID: 9b3ec2d8-6d02-4ab4-8f03-00a787c36e2b
  Args:
    type: :Woman
    source: Augusta_Victoria
  AssignClass (597ce5d5-354e-49d6-af2e-a5a49cd5cc93)
 Call ID: 597ce5d5-354e-49d6-af2e-a5a49cd5cc93
  Args:
    type: :Person
    source: Augusta_Victoria
  AddLiteral (fc6cb54c-cddd-45fc-939b-9ca1f957e01e)
 Call ID: fc6cb54c-cddd-45fc-939b-9ca1f957e01e
  Args:
    source: Manuel_II
    relation: :hasMarriageYear
    literal_value: 1913
    literal_type: xsd:integer
  AddTriple (4057d896-8449-4966-92ad-22a875694e61)
 Call ID: 4057d896-8449-4966-92ad-22a875694e61
  Args:
    relation: :hasRelation
    source: Manuel_II
    target: Augusta_Victoria
  AssignClass (c1954535-da10-49d9-9e14-1e777a7ab06f)
 Call ID: c1954535-da10-49d9-9e14-1e777a7ab06f
  Args:
    type: :Man
    source: Pedro_II_of_Brazil
  AssignClass (02d67f2a-1da4-49e2-9a99-40c8f429b111)
 Call ID: 02d67f2a-1da4-49e2-9a99-40c8f429b111
  Args:
    type: :Person
    source: Pedro_II_of_Brazil
  AssignClass (b35baf0a-e9bb-4c57-8f10-1fe61af454f0)
 Call ID: b35baf0a-e9bb-4c57-8f10-1fe61af454f0
  Args:
    source: Maria_Pia_of_Savoy
    type: :Woman
  AssignClass (73728f13-2cf4-4e2b-8330-b6a0601784fe)
 Call ID: 73728f13-2cf4-4e2b-8330-b6a0601784fe
  Args:
    source: Maria_Pia_of_Savoy
    type: :Person
  Finish (e4e27b3d-85f0-4362-9070-a6e0c1c8e214)
 Call ID: e4e27b3d-85f0-4362-9070-a6e0c1c8e214
  Args: