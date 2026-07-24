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
  AssignClass (bfb4dd93-422b-4fbc-bda0-d68a91b004db)
 Call ID: bfb4dd93-422b-4fbc-bda0-d68a91b004db
  Args:
    source: Kirill_Vladimirovich_Romanov
    type: :Man
  AssignClass (928c16b3-f590-4d2e-8b94-64ae18df54d2)
 Call ID: 928c16b3-f590-4d2e-8b94-64ae18df54d2
  Args:
    source: Kirill_Vladimirovich_Romanov
    type: :Person
  AddLiteral (3f0b8d16-6334-42cf-b837-a75a36cec9db)
 Call ID: 3f0b8d16-6334-42cf-b837-a75a36cec9db
  Args:
    source: Kirill_Vladimirovich_Romanov
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1876
  AddLiteral (b786e2b2-07c5-4462-8bf4-482340fa5814)
 Call ID: b786e2b2-07c5-4462-8bf4-482340fa5814
  Args:
    relation: :hasDeathYear
    source: Kirill_Vladimirovich_Romanov
    literal_value: 1938
    literal_type: xsd:integer
  AssignClass (4228e32c-361b-40be-8b57-74ab8e04aa36)
 Call ID: 4228e32c-361b-40be-8b57-74ab8e04aa36
  Args:
    source: Vladimir_Alexandrovich
    type: :Man
  AssignClass (0b70fad6-604c-4bb6-bec6-ddea44901c76)
 Call ID: 0b70fad6-604c-4bb6-bec6-ddea44901c76
  Args:
    source: Vladimir_Alexandrovich
    type: :Person
  AssignClass (4aad8946-8ea6-4f0e-9a38-a76a9ff9cffb)
 Call ID: 4aad8946-8ea6-4f0e-9a38-a76a9ff9cffb
  Args:
    source: Alexander_II
    type: :Man
  AssignClass (03f222a8-7eb0-432a-a44b-6feab6c5e141)
 Call ID: 03f222a8-7eb0-432a-a44b-6feab6c5e141
  Args:
    type: :Person
    source: Alexander_II
  AddTriple (43284c19-177e-4190-bcf5-f4efa3796908)
 Call ID: 43284c19-177e-4190-bcf5-f4efa3796908
  Args:
    target: Vladimir_Alexandrovich
    relation: :hasFather
    source: Kirill_Vladimirovich_Romanov
  AddTriple (b63387fe-29d3-4d77-b9d7-5abfe1a2b842)
 Call ID: b63387fe-29d3-4d77-b9d7-5abfe1a2b842
  Args:
    relation: :hasFather
    source: Vladimir_Alexandrovich
    target: Alexander_II
  AssignClass (7bbae068-85a4-4df9-b10a-8c5629ea5e0c)
 Call ID: 7bbae068-85a4-4df9-b10a-8c5629ea5e0c
  Args:
    source: Maria_Pavlovna
    type: :Woman
  AssignClass (f686c206-5354-43cd-99f1-d85b46ba4cdc)
 Call ID: f686c206-5354-43cd-99f1-d85b46ba4cdc
  Args:
    type: :Person
    source: Maria_Pavlovna
  AddTriple (b02722c7-f55f-434a-84e9-da754b8cec8d)
 Call ID: b02722c7-f55f-434a-84e9-da754b8cec8d
  Args:
    source: Kirill_Vladimirovich_Romanov
    relation: :hasMother
    target: Maria_Pavlovna
  AssignClass (361c3ff6-4ee2-4a0f-9a5d-6eeccece1b50)
 Call ID: 361c3ff6-4ee2-4a0f-9a5d-6eeccece1b50
  Args:
    source: Alexander_brother_of_Kirill
    type: :Man
  AssignClass (077c621f-ef72-4651-9e8d-0a1a71019be8)
 Call ID: 077c621f-ef72-4651-9e8d-0a1a71019be8
  Args:
    type: :Person
    source: Alexander_brother_of_Kirill
  AddTriple (81a1f864-5cfc-4277-9545-d17fc38e58c3)
 Call ID: 81a1f864-5cfc-4277-9545-d17fc38e58c3
  Args:
    target: Alexander_brother_of_Kirill
    relation: :isSiblingOf
    source: Kirill_Vladimirovich_Romanov
  AssignClass (7fc745ac-cabf-4859-ae40-90b5f9a63190)
 Call ID: 7fc745ac-cabf-4859-ae40-90b5f9a63190
  Args:
    source: Victoria_Melita
    type: :Woman
  AssignClass (f2d67af6-4f6f-4495-8f50-4a5f3f41f98e)
 Call ID: f2d67af6-4f6f-4495-8f50-4a5f3f41f98e
  Args:
    type: :Person
    source: Victoria_Melita
  AddLiteral (a5ac2251-730f-414c-80f6-d7da12e35ea9)
 Call ID: a5ac2251-730f-414c-80f6-d7da12e35ea9
  Args:
    literal_type: xsd:integer
    literal_value: 1905
    source: Kirill_Vladimirovich_Romanov
    relation: :hasMarriageYear
  AddTriple (0981c7cd-9415-4277-8d66-e395c9623c56)
 Call ID: 0981c7cd-9415-4277-8d66-e395c9623c56
  Args:
    relation: :hasRelation
    source: Kirill_Vladimirovich_Romanov
    target: Victoria_Melita
  AssignClass (29b380cc-a7f4-4e0d-8fc2-60afbd67b438)
 Call ID: 29b380cc-a7f4-4e0d-8fc2-60afbd67b438
  Args:
    source: Alfred_Duke_of_Saxe_Coburg_and_Gotha
    type: :Man
  AssignClass (96a2cbd8-2eda-4510-a000-5e285c7a25d9)
 Call ID: 96a2cbd8-2eda-4510-a000-5e285c7a25d9
  Args:
    source: Alfred_Duke_of_Saxe_Coburg_and_Gotha
    type: :Person
  AddTriple (73611629-bf14-471f-892f-6a63ad0ae076)
 Call ID: 73611629-bf14-471f-892f-6a63ad0ae076
  Args:
    relation: :hasFather
    source: Victoria_Melita
    target: Alfred_Duke_of_Saxe_Coburg_and_Gotha
  AssignClass (09d7cfb5-b03a-437b-af8c-0cd9c35d2e19)
 Call ID: 09d7cfb5-b03a-437b-af8c-0cd9c35d2e19
  Args:
    type: :Woman
    source: Maria_Alexandrovna_of_Russia
  AssignClass (31640f5e-f6bf-472e-9bbd-dbd1a0515587)
 Call ID: 31640f5e-f6bf-472e-9bbd-dbd1a0515587
  Args:
    source: Maria_Alexandrovna_of_Russia
    type: :Person
  AddTriple (83bb5d7c-dc89-4433-962d-e4468391493a)
 Call ID: 83bb5d7c-dc89-4433-962d-e4468391493a
  Args:
    source: Victoria_Melita
    relation: :hasMother
    target: Maria_Alexandrovna_of_Russia
  AddTriple (cdc8b1d2-7881-4741-86b3-c20e10394731)
 Call ID: cdc8b1d2-7881-4741-86b3-c20e10394731
  Args:
    relation: :hasFather
    source: Maria_Alexandrovna_of_Russia
    target: Alexander_II
  AssignClass (550ebaec-6fab-44bf-ab47-dbc695b76f31)
 Call ID: 550ebaec-6fab-44bf-ab47-dbc695b76f31
  Args:
    source: Vladimir_Kirillovich
    type: :Man
  AssignClass (5cb52952-5658-48da-8a22-4f1f9c4f547c)
 Call ID: 5cb52952-5658-48da-8a22-4f1f9c4f547c
  Args:
    source: Vladimir_Kirillovich
    type: :Person
  AddTriple (caf6f27a-5980-4fc3-953a-2981ac22979d)
 Call ID: caf6f27a-5980-4fc3-953a-2981ac22979d
  Args:
    relation: :isSonOf
    source: Vladimir_Kirillovich
    target: Kirill_Vladimirovich_Romanov
  AddTriple (59f44e3c-9f4c-44c9-9f56-c5e4c70ea738)
 Call ID: 59f44e3c-9f4c-44c9-9f56-c5e4c70ea738
  Args:
    relation: :isSonOf
    source: Vladimir_Kirillovich
    target: Victoria_Melita
  Finish (3d81ca0c-5169-47a5-bfc7-509cfbffeed4)
 Call ID: 3d81ca0c-5169-47a5-bfc7-509cfbffeed4
  Args: