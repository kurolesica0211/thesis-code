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
  AssignClass (9d19a7d8-f98f-4d7f-b566-50ec05070f2b)
 Call ID: 9d19a7d8-f98f-4d7f-b566-50ec05070f2b
  Args:
    type: :Woman
    source: :MargaretaOfRomania
  AssignClass (e2a714ee-3670-4cfb-959e-cbd9fcddb8cf)
 Call ID: e2a714ee-3670-4cfb-959e-cbd9fcddb8cf
  Args:
    source: :KingMichaelI
    type: :Man
  AssignClass (de75c329-ced2-4937-abe1-d539a866a742)
 Call ID: de75c329-ced2-4937-abe1-d539a866a742
  Args:
    source: :QueenAnneOfRomania
    type: :Woman
  AssignClass (2db5d5e7-de3b-4775-810e-4093d0112e05)
 Call ID: 2db5d5e7-de3b-4775-810e-4093d0112e05
  Args:
    source: :PrincessElena
    type: :Woman
  AssignClass (fbb349cd-000d-452c-8d67-25de430d5b50)
 Call ID: fbb349cd-000d-452c-8d67-25de430d5b50
  Args:
    source: :PrincessIrina
    type: :Woman
  AssignClass (1a5a243f-9d27-4b18-96ce-bb7d699bd15a)
 Call ID: 1a5a243f-9d27-4b18-96ce-bb7d699bd15a
  Args:
    source: :PrincessSophie
    type: :Woman
  AssignClass (4fee5bdd-aeb4-4a6c-9041-63069ac107bd)
 Call ID: 4fee5bdd-aeb4-4a6c-9041-63069ac107bd
  Args:
    type: :Woman
    source: :PrincessMaria
  AssignClass (70732b47-b0de-423f-9883-21a0c7a3d1f0)
 Call ID: 70732b47-b0de-423f-9883-21a0c7a3d1f0
  Args:
    type: :Man
    source: :PrinceRadu
  AddLiteral (7a35fec8-fdb9-4b97-b59a-5956491becf6)
 Call ID: 7a35fec8-fdb9-4b97-b59a-5956491becf6
  Args:
    literal_value: 1949
    source: :MargaretaOfRomania
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddTriple (d3583755-902d-4028-943e-6a0d2961ca98)
 Call ID: d3583755-902d-4028-943e-6a0d2961ca98
  Args:
    relation: :hasFather
    source: :MargaretaOfRomania
    target: :KingMichaelI
  AddTriple (14c50794-8290-4434-8e75-234f113b0068)
 Call ID: 14c50794-8290-4434-8e75-234f113b0068
  Args:
    source: :MargaretaOfRomania
    target: :QueenAnneOfRomania
    relation: :hasMother
  AddTriple (3efeb25c-1235-4002-8a58-30bfc8a9428e)
 Call ID: 3efeb25c-1235-4002-8a58-30bfc8a9428e
  Args:
    relation: :isDaughterOf
    target: :KingMichaelI
    source: :PrincessElena
  AddTriple (cf090d92-15c2-4d05-8e65-7276f2f9d6ae)
 Call ID: cf090d92-15c2-4d05-8e65-7276f2f9d6ae
  Args:
    relation: :isDaughterOf
    source: :PrincessElena
    target: :QueenAnneOfRomania
  AddTriple (f033fd50-402c-40c2-945c-52d8c6d417b3)
 Call ID: f033fd50-402c-40c2-945c-52d8c6d417b3
  Args:
    target: :KingMichaelI
    source: :PrincessIrina
    relation: :isDaughterOf
  AddTriple (e09b27cf-2755-495f-93c7-89c32bbb5e47)
 Call ID: e09b27cf-2755-495f-93c7-89c32bbb5e47
  Args:
    relation: :isDaughterOf
    source: :PrincessIrina
    target: :QueenAnneOfRomania
  AddTriple (3b4f554f-574d-4cb1-ba12-ef7bc97f09eb)
 Call ID: 3b4f554f-574d-4cb1-ba12-ef7bc97f09eb
  Args:
    relation: :isDaughterOf
    target: :KingMichaelI
    source: :PrincessSophie
  AddTriple (fb825020-b002-4c87-b85e-8a3d33e8be56)
 Call ID: fb825020-b002-4c87-b85e-8a3d33e8be56
  Args:
    relation: :isDaughterOf
    target: :QueenAnneOfRomania
    source: :PrincessSophie
  AddTriple (b1226baf-c582-4d21-bb47-5aa6c191f7a4)
 Call ID: b1226baf-c582-4d21-bb47-5aa6c191f7a4
  Args:
    relation: :isDaughterOf
    source: :PrincessMaria
    target: :KingMichaelI
  AddTriple (6c0cb1c9-f3ac-48dc-972f-87ba3948bb95)
 Call ID: 6c0cb1c9-f3ac-48dc-972f-87ba3948bb95
  Args:
    target: :QueenAnneOfRomania
    source: :PrincessMaria
    relation: :isDaughterOf
  AddTriple (835606c1-0820-4118-921a-fa599cc4b566)
 Call ID: 835606c1-0820-4118-921a-fa599cc4b566
  Args:
    source: :MargaretaOfRomania
    target: :PrinceRadu
    relation: :hasRelation
  Finish (4ccf5d82-d213-4ad4-b599-acbca0470247)
 Call ID: 4ccf5d82-d213-4ad4-b599-acbca0470247
  Args: