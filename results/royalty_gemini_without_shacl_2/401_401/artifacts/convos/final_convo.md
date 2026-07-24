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
The Custodian of the Crown  Prince Radu


Princess Elena 
Princess Irina 
Princess Sophie 
Princess Maria 


Margareta of Romania, self-styled as Custodian of the Romanian Crown, (Romanian: Custode al Coroanei române; born 26 March 1949) is the eldest daughter of King Michael I and Queen Anne of Romania.
She assumed her father's duties in March 2016, upon his retirement, and has claimed the headship of the House of Romania since his death on 5 December 2017.
She also heads the Margareta of Romania Royal Foundation.
Until 2011, Margareta also used the style of a princess of Hohenzollern.
Margareta has four sisters and no brothers or children.
Her heir presumptive is her next sister, Princess Elena of Romania.
Under the defunct royal constitutions of 1923 and 1938 which followed agnatic primogeniture, Margareta and her sisters would not have been in the line of succession to the throne.
On 30 December 2007, King Michael designated Margareta as heir presumptive to the defunct throne by an act that is not recognized by the Romanian government and lacks legal validity without approval by Romania's Parliament.
On the same occasion, Michael also requested that, should the Romanian Parliament consider restoring the monarchy, the Salic law of succession not be reinstated, allowing female succession.
According to the new statute of the Romanian Royal House as declared by Michael, no illegitimate descendants or collateral lines may claim dynastic privileges, titles or rank and any such are excluded from the Royal House of Romania and from the line of succession to the throne.
Early life

Birth

Margareta was born on 26 March 1949 at Clinique de Montchoisi in Lausanne, Switzerland, as the first of King Michael I and Queen Anne's five daughters.
Her godmother was her maternal grandmother Princess Margaret of Denmark who was also her namesake.
She was followed by four sisters: Princess Elena (born 1950), Princess Irina (born 1953), Princess Sophie (born 1957) and Princess Maria (born 1964).
Childhood

Margareta spent her childhood at family homes in Lausanne and at Ayot House, St Lawrence, in Hertfordshire, England.
During holidays she and her sisters spent time with their grandparents; paternally with Helen, Queen Mother, at Villa Sparta in Italy and maternally, with Princess Margaret and her husband Prince René of Bourbon-Parma in Copenhagen.
Margareta met Queen Elizabeth II of the United Kingdom for the first time in the summer of 1952 at Balmoral Castle, when she was three years old.
In her childhood, she spent holidays with Prince Charles and his sister, Princess Anne, who were close to Margareta, as well as Prince Amedeo, Duke of Aosta (her cousin), and the Greek, Danish and Luxembourg royal families.
Queen Helen's interest in horses influenced Margareta to become an equestrian.
In 1964, along with five other princesses, Margareta was a bridesmaid at the wedding of Princess Anne-Marie of Denmark to King Constantine II of Greece.
Education

Early education

In 1956, Margareta lived with Queen Helen for six months at her villa in Florence, attending kindergarten until returning to Switzerland, where she attended a primary school, with Princess Sophie, from age six to nine.
Margareta said in an interview in 2007.
Further education

Margareta studied sociology, political science and public international law at the University of Edinburgh in Scotland, graduating in 1974.
Known there as "Margareta de Roumanie", for the first few weeks she felt a depressing "sense of foreignness" but later became active in campus politics, becoming a member of the students' representative council.
"


While at the university during her twenties, Margareta was involved in a five-year romantic relationship with Gordon Brown, who would serve as Prime Minister of the United Kingdom from 2007 to 2010; in 2007, she was interviewed by an editor of The Daily Telegraph: "It was a very solid and romantic story; I never stopped loving him, but one day it didn't seem right any more, it was politics, politics, politics, and I needed nurturing," she said.
In the summer of 1989 Margareta resigned from her job as civil unrest started in Romania.
Romania

Romanian revolution

In mid 1989, civil and governmental unrest started arising in the Eastern Bloc as the loosening of control of Eastern Europe by the Soviet Union had triggered most of the impact for the former states which started a Revolutionary wave leading to the Revolutions of 1989.
On 25 December, Ceaușescu and his wife Deputy Prime Minister Elena Ceaușescu were deposed, captured and executed by orders from a Drumhead military tribunal; 42 years of the Socialist Republic of Romania had ended.
The revolution was the first overthrow of the ruling governmental system since King Michael's coup which he successfully staged in 1944 by arresting members of the military government which supported Nazi Germany.
During the Revolution, all members of the Royal Family took a part to console the situation outside of Romania.
Arrival in Romania

While she was visiting one orphanage, a child in a filthy cot died in front of her.
It spurred her to establish the Princess Margareta of Romania Foundation in 1990.
A 25th anniversary celebration of Margareta's return to Romania was held at the Romanian Athenaeum, followed by a dinner at the CEC Palace with Romania's Prime Minister Victor Ponta and Senate President Călin Popescu-Tăriceanu; around 200 other prominent guests participated in the festivities.
Margareta also hosted a March 2015 gala at the dynasty's historical family seat, Peleș Castle, in honour of the Romanian Rugby Union, attended by Klaus Johannis, the first incumbent Romanian president to pay an official visit to the former royal family.
Romanian Red Cross

On 15 May 2015, the General Assembly of the Romanian Red Cross elected Margareta as President of the Romanian Red Cross.
The Red Cross was instituted as a Romanian branch of the International Red Cross in 1876, under the reign of her great-great-granduncle King Carol I of Romania.
Although at Margareta's birth she was not expected to inherit the defunct Romanian throne and the headship of the Romanian royal family, the birth of four younger sisters and no brother meant that without a change in the royal family's succession laws, male members of the House of Hohenzollern-Sigmaringen would succeed her father as pretenders to the Romanian throne, in accordance with the Salic law enshrined in both the defunct royal Romanian Constitution of 1923 and the defunct Statute of the Romanian royal house, dated 1884.
In 1997 King Michael designated Margareta as successor to "all prerogatives and rights" of his, indicating his desire for a gender-blind succession to the throne; although there was much consideration of altering the line of succession, no actions were taken until 30 December 2007, when King Michael I issued the statutes for the Royal House, called The Fundamental Rules of the Royal House of Romania.
Following the announcement of The Fundamental Rules, King Michael asked the Romanian Government that, should it consider restoring the monarchy, it should also abolish the Salic law of succession.
Margareta does not use the title of queen; instead she claims the title "Custodian of the Romanian Crown", with the style "Her Majesty", a title that Michael offered her.
Paul-Philippe Hohenzollern (son of King Michael's illegitimate half-brother, Carol Lambrino) denounced King Michael's actions of creating The Fundamental Rules and severing ties with the House of Hohenzollern-Sigmaringen.
Although Margareta has no official role within the politics of Romania to maintain ties with other countries, she has fostered diplomatic relationships with numerous foreign dignitaries in her capacity as a head of the House of Romania.
Marriage

In 1994, Margareta met Radu Duda, a Romanian citizen and part-time actor, through the work of the Princess Margareta Foundation.
Radu Duda was accorded the style "Radu, Prince of Hohenzollern-Veringen" on 1 January 1999, and was subsequently styled "His Royal Highness Radu, Prince of Romania", being referred to by King Michael on 30 December 2007, as future "Prince Consort of Romania".
In Margareta's company and, more often alone, he has represented the former royal family publicly on various occasions.
Controversies

BAE Systems, one of the donors to the Princess Margareta of Romania Foundation, and its representatives have been involved in a corruption scandal involving purchase by the Romanian government of two decommissioned UK Royal Navy frigates (Coventry and London) refurbished by BAE, for which an alleged £7 million bribe was paid, some of which, it has also been alleged, ended up in the pockets of the Hohenzollern royal family to which Margareta belongs.
The "Gardianul" newspaper, noting that both Margareta and her husband, as Special Representative of the Government, had met a number of times with the BAE Systems representatives before and after the signing of the governmental contract, inquired whether the royal family was involved in any lobbying on behalf of the company.
Political support

The main pro-monarchist party PNŢCD, currently extra-parliamentary, is ambiguous in its support for Margareta.
Prior to his death, King Michael had not given up the hope for the restoration of the throne: "We are trying to make people understand what Romanian monarchy was and what it can still do.
"


In a July 2013 survey about a potential restoration of monarchy in Romania, 19% of respondents gave Margareta as their favorite, while 29.9% supported her father.
In December 2017, on the backdrop of the increased capital of trust in the Royal House of Romania, re-emerging with the death of King Michael, the executive chairman of the ruling Social Democratic Party Nicolae Bădălau said that one could organize a referendum on the transition to the monarchical ruling form, arguing that "it is not a bad thing, considering that the countries that have the monarchs are developed countries", being a project of the future.
At the same time, the leader of the coalition party and the president of the Senate of Romania, Călin Popescu-Tăriceanu, reinforced this idea, claiming that he is a convinced monarchist and "constitutional monarchy has the advantage of placing the monarch over political games, case: the president, instead of being an arbitrator, prefers to be a player.
"


Honours and awards

Honours

Dynastic

Ecclesiastical

Foreign

Honorary titles and medals

In Romania

Outside Romania

Publications

See also

References

External links



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
  AssignClass (dda00e5c-b81d-4a8b-8518-cd4cccb36425)
 Call ID: dda00e5c-b81d-4a8b-8518-cd4cccb36425
  Args:
    source: Margareta of Romania
    type: :Woman
  AssignClass (eb232f89-2592-4640-9c9e-58b8bbbfbdd7)
 Call ID: eb232f89-2592-4640-9c9e-58b8bbbfbdd7
  Args:
    source: King Michael I
    type: :Man
  AssignClass (59233b3d-5583-4c30-b71f-b3d00840d60d)
 Call ID: 59233b3d-5583-4c30-b71f-b3d00840d60d
  Args:
    source: Queen Anne of Romania
    type: :Woman
  AssignClass (d48a87a7-1d9a-46ad-b902-6340471f8ff5)
 Call ID: d48a87a7-1d9a-46ad-b902-6340471f8ff5
  Args:
    type: :Woman
    source: Princess Elena of Romania
  AssignClass (2eb88170-732f-4625-96e1-06145000d7fc)
 Call ID: 2eb88170-732f-4625-96e1-06145000d7fc
  Args:
    type: :Woman
    source: Princess Irina
  AssignClass (8539b944-e5ed-4ce4-8716-11623209b56a)
 Call ID: 8539b944-e5ed-4ce4-8716-11623209b56a
  Args:
    type: :Woman
    source: Princess Sophie
  AssignClass (598cb292-3e50-4895-94bd-a939960b8083)
 Call ID: 598cb292-3e50-4895-94bd-a939960b8083
  Args:
    type: :Woman
    source: Princess Maria
  AssignClass (b442fa55-b8e7-4953-9118-2f2444958612)
 Call ID: b442fa55-b8e7-4953-9118-2f2444958612
  Args:
    type: :Man
    source: Prince Radu
  AddTriple (c0131899-4f20-429b-869d-8d8dd035b5b6)
 Call ID: c0131899-4f20-429b-869d-8d8dd035b5b6
  Args:
    relation: :isDaughterOf
    target: King Michael I
    source: Margareta of Romania
  AddTriple (2a31cd98-819c-4721-9761-eaffafae75fa)
 Call ID: 2a31cd98-819c-4721-9761-eaffafae75fa
  Args:
    relation: :isDaughterOf
    target: Queen Anne of Romania
    source: Margareta of Romania
  AddTriple (230a5f19-8647-4d63-9228-2b8d6dad943f)
 Call ID: 230a5f19-8647-4d63-9228-2b8d6dad943f
  Args:
    source: Princess Elena of Romania
    target: King Michael I
    relation: :isDaughterOf
  AddTriple (cac48c0f-51b0-4dd1-9b66-ed0acf5b1b60)
 Call ID: cac48c0f-51b0-4dd1-9b66-ed0acf5b1b60
  Args:
    source: Princess Elena of Romania
    relation: :isDaughterOf
    target: Queen Anne of Romania
  AddTriple (c511c20f-59ac-42dd-a8a6-1d39b9a21d2c)
 Call ID: c511c20f-59ac-42dd-a8a6-1d39b9a21d2c
  Args:
    source: Princess Irina
    target: King Michael I
    relation: :isDaughterOf
  AddTriple (7b5dcd02-b0f9-4f2a-bdfc-d89191bc6ab2)
 Call ID: 7b5dcd02-b0f9-4f2a-bdfc-d89191bc6ab2
  Args:
    source: Princess Irina
    target: Queen Anne of Romania
    relation: :isDaughterOf
  AddTriple (7ffe153a-ccdd-4135-86bb-b306ac8e763b)
 Call ID: 7ffe153a-ccdd-4135-86bb-b306ac8e763b
  Args:
    target: King Michael I
    relation: :isDaughterOf
    source: Princess Sophie
  AddTriple (03616660-973b-4aee-bb7c-9ed1b1f428d7)
 Call ID: 03616660-973b-4aee-bb7c-9ed1b1f428d7
  Args:
    source: Princess Sophie
    relation: :isDaughterOf
    target: Queen Anne of Romania
  AddTriple (a01dd5e3-1dad-4aad-9fca-c728d6be0299)
 Call ID: a01dd5e3-1dad-4aad-9fca-c728d6be0299
  Args:
    relation: :isDaughterOf
    target: King Michael I
    source: Princess Maria
  AddTriple (ed0c50fb-52b2-4746-8636-d7d82984c639)
 Call ID: ed0c50fb-52b2-4746-8636-d7d82984c639
  Args:
    relation: :isDaughterOf
    target: Queen Anne of Romania
    source: Princess Maria
  AddLiteral (c5fa1fc2-d5a2-46e4-af0a-8c3d65a06a73)
 Call ID: c5fa1fc2-d5a2-46e4-af0a-8c3d65a06a73
  Args:
    literal_type: xsd:positiveInteger
    literal_value: 1949
    source: Margareta of Romania
    relation: :hasBirthYear
  AddLiteral (ea9afcdf-68ae-4058-bfe6-29eaa4edec45)
 Call ID: ea9afcdf-68ae-4058-bfe6-29eaa4edec45
  Args:
    relation: :hasBirthYear
    literal_type: xsd:positiveInteger
    source: Princess Elena of Romania
    literal_value: 1950
  AddLiteral (65069d35-1ad5-4af3-89d6-b702cd4eeaf2)
 Call ID: 65069d35-1ad5-4af3-89d6-b702cd4eeaf2
  Args:
    literal_value: 1953
    source: Princess Irina
    literal_type: xsd:positiveInteger
    relation: :hasBirthYear
  AddLiteral (75731fda-f0b3-461d-b28b-85884a54c7b7)
 Call ID: 75731fda-f0b3-461d-b28b-85884a54c7b7
  Args:
    literal_value: 1957
    source: Princess Sophie
    literal_type: xsd:positiveInteger
    relation: :hasBirthYear
  AddLiteral (2b1bf43d-7151-449e-a750-b5934c94cb44)
 Call ID: 2b1bf43d-7151-449e-a750-b5934c94cb44
  Args:
    literal_value: 1964
    source: Princess Maria
    literal_type: xsd:positiveInteger
    relation: :hasBirthYear
  AddLiteral (02ab5719-7049-4d13-92ac-afecff3c25d9)
 Call ID: 02ab5719-7049-4d13-92ac-afecff3c25d9
  Args:
    literal_value: 2017
    source: King Michael I
    literal_type: xsd:positiveInteger
    relation: :hasDeathYear
  Finish (18b1a26b-fa6e-450f-93ff-860efb9ac402)
 Call ID: 18b1a26b-fa6e-450f-93ff-860efb9ac402
  Args: