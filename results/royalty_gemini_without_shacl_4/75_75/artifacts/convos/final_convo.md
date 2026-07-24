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
Grand Duke Kirill Vladimirovich of Russia (Russian: Кирилл Владимирович Романов; Kirill Vladimirovich Romanov; 12 October  1876 – 12 October 1938) was a Russian grand duke and a claimant to the defunct Russian throne from 1924 until his death.
He was the son of Grand Duke Vladimir Alexandrovich of Russia and a grandson of Emperor Alexander II.
Grand Duke Kirill followed a career in the Imperial Russian Navy serving for 20 years in the Naval Guards.
In 1905, he married his paternal first cousin, Princess Victoria Melita of Saxe-Coburg and Gotha, defying Nicholas II by not obtaining his consent.
They had two daughters and settled in Paris before they were allowed to visit Russia in 1909.
In 1910 they moved to Russia.
In World War I, Grand Duke Kirill was appointed Commander of the Naval Depot of the Guards in 1915.
During the February Revolution of 1917, Kirill marched to the Tauride Palace at the head of the Naval Guards and swore allegiance to the Russian Provisional Government.
During the rule of the Provisional Governmental in the summer of 1917, Kirill escaped to Finland, where his wife gave birth to the couple's only son.
With the death of his cousins Nicholas II and Grand Duke Michael Alexandrovich, Kirill proclaimed himself to be the head of the House of Romanov and, as next in line to the throne, as "Guardian of the Throne" in 1924.
Kirill proclaimed himself emperor-in-exile in 1926.
He wrote a book of memoirs, My Life in Russia's Service, which was published after his death.
Early life

Grand Duke Kirill Vladimirovich of Russia was born on 12 October  1876 in Tsarskoye Selo, at his parents' country residence, the Vladimir Villa.
His father was Grand Duke Vladimir Alexandrovich, the third son of Emperor Alexander II of Russia.
His mother was Grand Duchess Maria Pavlovna, née Duchess Marie Alexandrine of Mecklenburg.
As a grandson in the male line to a Russian Tsar, he was titled Grand Duke.
Kirill's parents, wealthy and sophisticated, were influential figures in Russian society.
Grand Duke Vladimir was cultured and a great patron of the arts, while Grand Duchess Maria Pavlovna was a renowned hostess in the Imperial capital.
Both had imposing personalities and left a big imprint in the lives of Kirill and his siblings.
Grand Duke Kirill was six months old when his eldest brother, Alexander, died in childhood.
Kirill Vladimirovich grew up between his parents' residence in St Petersburg, the Vladimir Palace, and their country retreat, the Vladimir Villa in Tsarskoye Selo.
Until he was fourteen years of age, Grand Duke Kirill was educated at home by private tutors.
During breaks from his daily lessons, he trained in a gym with his brothers at the Vladimir Palace.
Naval career

From an early age, Grand Duke Kirill had a love for the sea and his parents encouraged him to follow a career in the Imperial Navy.
Grand Duke Kirill's uncle, Tsar Alexander III, died on 1 November  1894 and Kirill's cousin, Nicholas II, became the new Tsar.
During the coronation festivities in Moscow, Kirill fell in love with his paternal first cousin,
Princess Victoria Melita of Saxe-Coburg and Gotha.
They flirted with each other at the balls and celebrations, but Victoria Melita was already married to Ernest Louis, Grand Duke of Hesse, the only brother of Tsarina Alexandra.
After graduating from the Naval Cadet Corps and Nikolaev Naval Academy, on 1 January 1904, Kirill was promoted to Chief of Staff to the Russian Pacific Fleet in the Imperial Russian Navy.
Kirill barely escaped with his life, and was invalided out of the service suffering from burns, back injuries and shell shock.
Marriage and children

Grand Duke Kirill married his first cousin, Princess Victoria Melita of Saxe-Coburg and Gotha on 8 October 1905 without any consent from Tsar Nicholas II.
Victoria's father was Alfred, Duke of Saxe-Coburg and Gotha, the second eldest son of Queen Victoria.
Victoria's mother was Grand Duchess Maria Alexandrovna of Russia, a daughter of Tsar Alexander II and Kirill's paternal aunt.
The marriage caused a scandal in the courts of European royalty as Princess Victoria was divorced from her first husband, Grand Duke Ernest Louis of Hesse, also her first cousin.
The Grand Duke of Hesse's sister was Tsarina Alexandra Feodorovna, the wife of Nicholas II.
She was not alone in her opposition, Dowager Empress Maria Feodorovna was also appalled at the effrontery of Kirill's marriage.
Shortly after Kirill's return to Russia, the Tsar stripped Kirill of his imperial allowance and title of Imperial Highness, his honours and decorations, his position in the navy and then banished him from Russia, though the style of Imperial Highness and title of Grand Duke was restored on 5 October 1905, shortly after Kirill left Russia


In 1908, after the death of Grand Duke Alexei Alexandrovich, Nicholas II restored Kirill to his rank of captain in the Imperial Russian Navy and his position as aide de camp to the emperor.
He was given the title Grand Duke of Russia  and from then on his wife was styled as Her Imperial Highness Grand Duchess Viktoria Feodorovna.
From 1909–1912, Kirill served on the cruiser Oleg and was its captain in 1912.
Grand Duke Kirill and Princess Victoria Melita had three children:


All the children were born to the rank of Prince and Princess of Russia, not entitled to the rank of Grand Duke or Grand Duchess as they were not children or grandchildren in the male line of a Russian Emperor according to the Pauline Laws.
In accordance with these laws, Kirill raised his children to the rank of Grand Duke and Grand Duchess after assuming the position of senior male of the Romanov family, and Head of the Imperial House.
This elevation was openly denounced by Grand Duke Nicholas Nikolaevich when he published a private letter of the Dowager Empress in 1924 in which she stated that Kirill's assumption of the position was "premature."
The Dowager Empress believed that her sons and grandsons might still be alive in Russia.
Grand Duke Kirill wrote to Grand Duchess Xenia "Nothing can be compared to what I shall now have to endure on this account, and I know full
"


Revolution

During the February Revolution of 1917, Kirill participated in a plan to establish a constitutional monarchy alongside Grand Duke Paul Alexandrovich and Grand Duke Michael Alexandrovich.
Grand Duke Paul drafted a decree and planned to convince Nicholas to sign it when he disembarked from his train at Tsarskoye Selo on 1 March 1917.
Mikhail and Kirill were supposed to deliver it to the Duma and request its implementation.
However Kirill alone marched to the Tauride Palace at the head of the Garde Equipage (Marine Guard).
Kirill had authorised the flying of a red flag over his palace on Glinka Street in Petrograd and in correspondence with a Romanov relative claimed credit for "saving the situation by my recognition of the Provisional Government".
In June 1917 Kirill and Victoria moved to Finland and then escaped to Coburg in 1920.
The exiled family subsequently moved to a small residence in the tiny French fishing village of Saint-Briac-sur-Mer.


Life abroad

After a London court order in July 1924 recognized Grand Duke Michael to be legally dead, Kirill first declared himself "Guardian of the Throne" on 8 August 1924 and then on 31 August 1924 he assumed the title Emperor of all the Russias.
However, his claim caused division within the family; his principal rival, and the only one to reject his claim was Grand Duke Nicholas.
In 1926 at a (Russian) monarchists congress in Paris the delegates voted to recognize Grand Duke Nicholas as their leader; however, with Nicholas's death in 1929
Kirill became the undisputed leader of the monarchists.
After claiming the throne, Kirill became known as the "Soviet Tsar" because in the event of a restoration of the monarchy, he intended to keep some of the features of the Soviet regime.
While living in exile, he was supported by some émigrés who styled themselves "legitimists" (legitimisti, in Russian легитимисты), underlining the "legitimacy" of Kirill's succession.
The opponents of Kirill were known as the "un-predetermined" (nepredreshentsi, in Russian непредрешенцы); they believed that in the wake of the radical revolutionary events that the convening of a Zemsky Sobor was necessary in order to choose a new monarch for Russia.
Kirill found his strongest support among a group of legitimists known as the Mladorossi, a Russian émigré monarchist organization that ultimately became heavily influenced by fascism – although it distanced itself from other fascist movements.
Kirill became more wary of the organization when he learned that its founder, Alexander Kazem-Bek, was spotted meeting with an OGPU agent.
Kirill accepted Kazem-Bek's voluntary resignation.
Just before he died, he wrote his autobiography, My Life in Russia's Service –
Kirill was succeeded by his son Vladimir Kirillovich who styled himself "Grand Duke and head of the Russian Imperial House".
Kirill was buried at the ducal mausoleum at Friedhof am Glockenberg , Coburg.:
47  Following the Dissolution of the Soviet Union, the remains of Kirill and his spouse were transferred from Coburg to the Grand Ducal Mausoleum of the Peter and Paul Fortress in St. Petersburg, Russia on 7 March 1995 after negotiations conducted by his granddaughter Maria Vladimirovna.
In the 1986 miniseries Anastasia: The Mystery of Anna, Sir Rex Harrison portrayed Kirill as an embittered and dangerous enemy to Anna Anderson, who notoriously claimed to be the Grand Duchess Anastasia.



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
  AssignClass (188550d7-f26c-4130-b39a-81eb653e7118)
 Call ID: 188550d7-f26c-4130-b39a-81eb653e7118
  Args:
    type: :Man
    source: :Kirill_Vladimirovich_Romanov
  AssignClass (1c933552-3988-41b9-8ec5-d22f8922f3c8)
 Call ID: 1c933552-3988-41b9-8ec5-d22f8922f3c8
  Args:
    source: :Kirill_Vladimirovich_Romanov
    type: :Person
  AddLiteral (9af08951-9c40-4624-9ee0-d3befbd9ecf9)
 Call ID: 9af08951-9c40-4624-9ee0-d3befbd9ecf9
  Args:
    relation: :hasBirthYear
    literal_value: 1876
    source: :Kirill_Vladimirovich_Romanov
    literal_type: xsd:integer
  AddLiteral (764f2dd6-6db5-4b44-b834-0b175fe8dd46)
 Call ID: 764f2dd6-6db5-4b44-b834-0b175fe8dd46
  Args:
    relation: :hasDeathYear
    source: :Kirill_Vladimirovich_Romanov
    literal_value: 1938
    literal_type: xsd:integer
  AssignClass (c83071de-b740-49b4-b447-6b5e0b8f2574)
 Call ID: c83071de-b740-49b4-b447-6b5e0b8f2574
  Args:
    type: :Man
    source: :Vladimir_Alexandrovich
  AssignClass (2518cc60-c4e2-4aba-9a6c-22ac1452b501)
 Call ID: 2518cc60-c4e2-4aba-9a6c-22ac1452b501
  Args:
    source: :Vladimir_Alexandrovich
    type: :Person
  AddTriple (cdc0325a-2311-4946-9fc9-2ec689eea434)
 Call ID: cdc0325a-2311-4946-9fc9-2ec689eea434
  Args:
    source: :Kirill_Vladimirovich_Romanov
    relation: :hasFather
    target: :Vladimir_Alexandrovich
  AssignClass (79b3dda8-1d68-490d-997d-184db55be053)
 Call ID: 79b3dda8-1d68-490d-997d-184db55be053
  Args:
    type: :Man
    source: :Alexander_II
  AssignClass (7871c222-be48-4e80-a756-a8692a296898)
 Call ID: 7871c222-be48-4e80-a756-a8692a296898
  Args:
    type: :Person
    source: :Alexander_II
  AddTriple (1c619f0f-85b8-4dca-9c03-7d6f98ad1afc)
 Call ID: 1c619f0f-85b8-4dca-9c03-7d6f98ad1afc
  Args:
    target: :Alexander_II
    relation: :hasFather
    source: :Vladimir_Alexandrovich
  AssignClass (878d637a-461b-4b31-bb2d-033c1aee5367)
 Call ID: 878d637a-461b-4b31-bb2d-033c1aee5367
  Args:
    source: :Maria_Pavlovna
    type: :Woman
  AssignClass (401006b6-681e-4c74-9205-cc3bedfb2273)
 Call ID: 401006b6-681e-4c74-9205-cc3bedfb2273
  Args:
    type: :Person
    source: :Maria_Pavlovna
  AddTriple (9507e63f-f933-48bf-8527-4fb34b579d08)
 Call ID: 9507e63f-f933-48bf-8527-4fb34b579d08
  Args:
    relation: :hasMother
    source: :Kirill_Vladimirovich_Romanov
    target: :Maria_Pavlovna
  AssignClass (f5917649-564e-45a9-b494-5103de0aae13)
 Call ID: f5917649-564e-45a9-b494-5103de0aae13
  Args:
    source: :Victoria_Melita
    type: :Woman
  AssignClass (f13be7a3-29f4-4b15-b689-409879fd9749)
 Call ID: f13be7a3-29f4-4b15-b689-409879fd9749
  Args:
    source: :Victoria_Melita
    type: :Person
  AddLiteral (9be607a2-2fa5-497b-a185-dde073003ef2)
 Call ID: 9be607a2-2fa5-497b-a185-dde073003ef2
  Args:
    relation: :hasMarriageYear
    source: :Kirill_Vladimirovich_Romanov
    literal_value: 1905
    literal_type: xsd:integer
  AddTriple (a6bd8629-8807-4bea-a024-3d0b23812b8f)
 Call ID: a6bd8629-8807-4bea-a024-3d0b23812b8f
  Args:
    relation: :hasRelation
    source: :Kirill_Vladimirovich_Romanov
    target: :Victoria_Melita
  AddTriple (15098b78-522d-45a0-bd66-7bf71438f8e0)
 Call ID: 15098b78-522d-45a0-bd66-7bf71438f8e0
  Args:
    target: :Kirill_Vladimirovich_Romanov
    source: :Victoria_Melita
    relation: :hasRelation
  AssignClass (29265909-7be9-45d4-9e02-ba3c34dcdb32)
 Call ID: 29265909-7be9-45d4-9e02-ba3c34dcdb32
  Args:
    type: :Man
    source: :Alexander_brother
  AssignClass (74e58921-8772-418e-a13a-152a6d450116)
 Call ID: 74e58921-8772-418e-a13a-152a6d450116
  Args:
    type: :Person
    source: :Alexander_brother
  AddTriple (787b0faf-5556-4c92-b925-f46fc310cc4e)
 Call ID: 787b0faf-5556-4c92-b925-f46fc310cc4e
  Args:
    target: :Alexander_brother
    source: :Kirill_Vladimirovich_Romanov
    relation: :hasBrother
  AssignClass (f7ae537d-04dc-4e83-b8ca-e402efc22a49)
 Call ID: f7ae537d-04dc-4e83-b8ca-e402efc22a49
  Args:
    type: :Man
    source: :Vladimir_Kirillovich
  AssignClass (57586239-1f34-4c64-a877-b404a0d1a901)
 Call ID: 57586239-1f34-4c64-a877-b404a0d1a901
  Args:
    source: :Vladimir_Kirillovich
    type: :Person
  AddTriple (7db62991-6379-4c23-a0bf-ae788d268bb6)
 Call ID: 7db62991-6379-4c23-a0bf-ae788d268bb6
  Args:
    target: :Kirill_Vladimirovich_Romanov
    source: :Vladimir_Kirillovich
    relation: :hasFather
  AddTriple (51aac584-c16f-4f60-b70a-251bdbcc93ea)
 Call ID: 51aac584-c16f-4f60-b70a-251bdbcc93ea
  Args:
    target: :Victoria_Melita
    relation: :hasMother
    source: :Vladimir_Kirillovich
  AssignClass (b41c56c7-09a5-4d5d-9fa1-927aeb6c016d)
 Call ID: b41c56c7-09a5-4d5d-9fa1-927aeb6c016d
  Args:
    source: :Maria_Vladimirovna
    type: :Woman
  AssignClass (cab41dcf-ab8b-4245-b0a9-1c20ed581271)
 Call ID: cab41dcf-ab8b-4245-b0a9-1c20ed581271
  Args:
    source: :Maria_Vladimirovna
    type: :Person
  AddTriple (5fc71b60-8103-4b5e-96f7-763f1ed8c996)
 Call ID: 5fc71b60-8103-4b5e-96f7-763f1ed8c996
  Args:
    target: :Vladimir_Kirillovich
    source: :Maria_Vladimirovna
    relation: :hasFather
  Finish (78045fcf-a1a0-43f4-a630-1d2d893a4112)
 Call ID: 78045fcf-a1a0-43f4-a630-1d2d893a4112
  Args: