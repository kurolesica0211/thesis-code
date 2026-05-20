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
  AssignClass (9e27108a-a0c1-4d95-8076-5cf38bdf5c3c)
 Call ID: 9e27108a-a0c1-4d95-8076-5cf38bdf5c3c
  Args:
    type: :Man
    source: Kirill_Vladimirovich_Romanov
  AssignClass (f05c0442-f328-43eb-9e43-1e49518c4425)
 Call ID: f05c0442-f328-43eb-9e43-1e49518c4425
  Args:
    source: Kirill_Vladimirovich_Romanov
    type: :Person
  AddLiteral (0e4422f8-49dc-4fcc-af21-ddbd3c0e50e5)
 Call ID: 0e4422f8-49dc-4fcc-af21-ddbd3c0e50e5
  Args:
    source: Kirill_Vladimirovich_Romanov
    literal_value: 1876
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (81d73f2c-b03e-4941-ae85-76ea2b6ee4bc)
 Call ID: 81d73f2c-b03e-4941-ae85-76ea2b6ee4bc
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1938
    source: Kirill_Vladimirovich_Romanov
  AssignClass (4ccf6aba-9968-4d60-b7c8-eb1444ca1f94)
 Call ID: 4ccf6aba-9968-4d60-b7c8-eb1444ca1f94
  Args:
    type: :Man
    source: Vladimir_Alexandrovich_of_Russia
  AssignClass (d931fd50-4357-4e49-a326-570c32c4508e)
 Call ID: d931fd50-4357-4e49-a326-570c32c4508e
  Args:
    source: Vladimir_Alexandrovich_of_Russia
    type: :Person
  AddTriple (cb9ef368-456d-4b09-a58f-b0d30fdd7d15)
 Call ID: cb9ef368-456d-4b09-a58f-b0d30fdd7d15
  Args:
    target: Vladimir_Alexandrovich_of_Russia
    relation: :hasFather
    source: Kirill_Vladimirovich_Romanov
  AssignClass (2de6676c-1b53-43a8-88e5-53664ff9668d)
 Call ID: 2de6676c-1b53-43a8-88e5-53664ff9668d
  Args:
    source: Maria_Pavlovna
    type: :Woman
  AssignClass (840dff7d-9c01-478d-bff2-d9e14bd9ae7f)
 Call ID: 840dff7d-9c01-478d-bff2-d9e14bd9ae7f
  Args:
    source: Maria_Pavlovna
    type: :Person
  AddTriple (d7a575f2-0083-44ee-8064-33ebc59572ee)
 Call ID: d7a575f2-0083-44ee-8064-33ebc59572ee
  Args:
    relation: :hasMother
    target: Maria_Pavlovna
    source: Kirill_Vladimirovich_Romanov
  AssignClass (01d4b616-0793-43aa-ba29-7a485299e6e7)
 Call ID: 01d4b616-0793-43aa-ba29-7a485299e6e7
  Args:
    type: :Man
    source: Alexander_II_of_Russia
  AssignClass (3ff3ee2e-8aac-4b38-a6d8-be4b9f7738a9)
 Call ID: 3ff3ee2e-8aac-4b38-a6d8-be4b9f7738a9
  Args:
    type: :Person
    source: Alexander_II_of_Russia
  AddTriple (ab2aa300-fe75-4060-bb07-3a02d3c2f089)
 Call ID: ab2aa300-fe75-4060-bb07-3a02d3c2f089
  Args:
    relation: :hasFather
    target: Alexander_II_of_Russia
    source: Vladimir_Alexandrovich_of_Russia
  AssignClass (e7d96e22-69e0-4f10-91f7-a90c0314c9c8)
 Call ID: e7d96e22-69e0-4f10-91f7-a90c0314c9c8
  Args:
    source: Victoria_Melita_of_Saxe-Coburg_and_Gotha
    type: :Woman
  AssignClass (b9b6b9b9-c558-4691-8feb-1f2cb6224145)
 Call ID: b9b6b9b9-c558-4691-8feb-1f2cb6224145
  Args:
    type: :Person
    source: Victoria_Melita_of_Saxe-Coburg_and_Gotha
  AddLiteral (ff8e0388-bc82-4724-bb57-251ec306ef58)
 Call ID: ff8e0388-bc82-4724-bb57-251ec306ef58
  Args:
    literal_value: 1905
    source: Kirill_Vladimirovich_Romanov
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AddTriple (1bc81cec-a195-48eb-b648-228746ac32b7)
 Call ID: 1bc81cec-a195-48eb-b648-228746ac32b7
  Args:
    source: Kirill_Vladimirovich_Romanov
    target: Victoria_Melita_of_Saxe-Coburg_and_Gotha
    relation: :hasRelation
  AssignClass (7a4b8ef4-49b1-42a6-888d-9af7a77cd6d1)
 Call ID: 7a4b8ef4-49b1-42a6-888d-9af7a77cd6d1
  Args:
    source: Alfred_Duke_of_Saxe-Coburg_and_Gotha
    type: :Man
  AssignClass (d984f9e1-b559-443c-98d3-c23fe6fc3e6c)
 Call ID: d984f9e1-b559-443c-98d3-c23fe6fc3e6c
  Args:
    type: :Person
    source: Alfred_Duke_of_Saxe-Coburg_and_Gotha
  AddTriple (4b8d1548-f76e-4e0b-9bf7-cfe0df7f22b5)
 Call ID: 4b8d1548-f76e-4e0b-9bf7-cfe0df7f22b5
  Args:
    relation: :hasFather
    target: Alfred_Duke_of_Saxe-Coburg_and_Gotha
    source: Victoria_Melita_of_Saxe-Coburg_and_Gotha
  AssignClass (5194bb18-7c70-44b3-8f84-600da783bf57)
 Call ID: 5194bb18-7c70-44b3-8f84-600da783bf57
  Args:
    type: :Woman
    source: Maria_Alexandrovna_of_Russia
  AssignClass (f89790f7-cd6e-4adc-9e93-c11c1732ca95)
 Call ID: f89790f7-cd6e-4adc-9e93-c11c1732ca95
  Args:
    type: :Person
    source: Maria_Alexandrovna_of_Russia
  AddTriple (e5f5d7a8-ca0c-434d-b3b1-9958cf7b43d6)
 Call ID: e5f5d7a8-ca0c-434d-b3b1-9958cf7b43d6
  Args:
    target: Maria_Alexandrovna_of_Russia
    relation: :hasMother
    source: Victoria_Melita_of_Saxe-Coburg_and_Gotha
  AddTriple (ae2f6b10-1081-482b-a28e-a6b972e31e3c)
 Call ID: ae2f6b10-1081-482b-a28e-a6b972e31e3c
  Args:
    source: Maria_Alexandrovna_of_Russia
    relation: :hasFather
    target: Alexander_II_of_Russia
  AssignClass (29783240-a4b2-4169-ba8c-a67aebbff6ac)
 Call ID: 29783240-a4b2-4169-ba8c-a67aebbff6ac
  Args:
    source: Vladimir_Kirillovich
    type: :Man
  AssignClass (025dc480-d343-4646-8430-9bb46c62694b)
 Call ID: 025dc480-d343-4646-8430-9bb46c62694b
  Args:
    type: :Person
    source: Vladimir_Kirillovich
  AddTriple (355686bd-5a00-4d35-b0b4-18b418870025)
 Call ID: 355686bd-5a00-4d35-b0b4-18b418870025
  Args:
    relation: :hasFather
    target: Kirill_Vladimirovich_Romanov
    source: Vladimir_Kirillovich
  AddTriple (4744f1dc-5674-4af5-bf93-d4f34b81001f)
 Call ID: 4744f1dc-5674-4af5-bf93-d4f34b81001f
  Args:
    source: Vladimir_Kirillovich
    target: Victoria_Melita_of_Saxe-Coburg_and_Gotha
    relation: :hasMother
  AssignClass (0208f5e4-8908-4bf2-9235-ac8b713517d3)
 Call ID: 0208f5e4-8908-4bf2-9235-ac8b713517d3
  Args:
    source: Alexander_brother_of_Kirill
    type: :Man
  AssignClass (30e9273b-21b5-49b6-ace5-9358502f81d9)
 Call ID: 30e9273b-21b5-49b6-ace5-9358502f81d9
  Args:
    source: Alexander_brother_of_Kirill
    type: :Person
  AddTriple (2a3e646e-d241-4d36-9a5e-ea3752a4d831)
 Call ID: 2a3e646e-d241-4d36-9a5e-ea3752a4d831
  Args:
    source: Kirill_Vladimirovich_Romanov
    target: Alexander_brother_of_Kirill
    relation: :hasBrother
  Finish (dc4eb60a-c728-42ae-ab3a-6c008ed42d80)
 Call ID: dc4eb60a-c728-42ae-ab3a-6c008ed42d80
  Args: