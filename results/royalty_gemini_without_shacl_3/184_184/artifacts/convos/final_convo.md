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
Grand Duchess Maria Vladimirovna of Russia


Grand Duke George Mikhailovich of Russia (Russian: Георгий Михайлович Романов, romanized: Gěorgij Mihajlovič Romanov, also spelled Romanoff;
German: Georg Michailowitsch Romanow; born 13 March 1981) is the heir apparent to Maria Vladimirovna, a claimant to the disputed Headship of the Imperial Family of Russia.
He is the only child of Maria and her former husband, Prince Franz Wilhelm of Prussia.
George's mother attributes to him the title of Tsesarevich and he bears the prefix of "Grand Duke" with the style of Imperial Highness which is still being questioned.
As the son of a cadet member of the branch of the House of Hohenzollern which formerly ruled the German Empire and Kingdom of Prussia, he is also sometimes entitled "Prince of Prussia" with the style of Royal Highness.
Early life

George was born in Madrid in 1981, the son of Grand Duchess Maria Vladimirovna of Russia (daughter and heir of Vladimir Cyrillovich, Grand Duke of Russia) and Prince Franz Wilhelm of Prussia (titled at the time Grand Duke Michael Pavlovich, son of Prince Karl Franz of Prussia and Princess Henriette of Schönaich-Carolath).
George was baptised on 6 May 1981, in Madrid; his godfather is Constantine II of Greece.
The announcement that George Mikhailovich would be known as a Russian Grand Duke prompted Prince Vasili Alexandrovich, then president of the Romanov Family Association, to respond in writing that "The Romanov Family Association hereby declares that the joyful event in the Prussian Royal House does not concern the Romanov Family Association since the newborn prince is not a member of either the Russian Imperial House or of the Romanov family".
This response was ignored by Grand Duke Vladimir as he had already selected his daughter to succeed him according to the Pauline laws, and because the marriage between her and Prince Franz Wilhelm of Prussia was deemed dynastic.
Prior to their wedding, the Grand Duke and his first cousin, then Head of the House of Hohenzollern, Prince Louis Ferdinand of Prussia, had made a dynastic agreement that any child born from this marriage should be raised as a Romanov.
Therefore, George is considered a dynast of both houses (Romanov and Hohenzollern), as his father has never renounced his Prussian royal title.
It says he is Prince George of Prussia".
George spent the first years of his life in France before moving to Spain.
Education and career

George was educated at International School of Madrid in Madrid, D'Overbroeck's College, Oxford and at St Benet's Hall, Oxford.
Heir to his mother

On 21 April 1992, upon the death of his maternal grandfather Grand Duke Vladimir Cyrillovich, George's mother claimed to have succeeded as the sovereign and Curatrix of the Throne of Russia, making him, to supporters of his mother, heir apparent and tsesarevich.
He visited Russia for the first time shortly thereafter to attend the funeral of his grandfather.
In 1996, when he, his mother, and his grandmother Leonida returned to Russia after living in Madrid, one of President Boris Yeltsin's former bodyguards was assigned as tutor to the 15-year-old prince.
Marriage and children

In January 2021, the family announced that George was engaged to marry Victoria Romanovna Bettarini (born Rebecca Virginia Bettarini in Rome on 18 May 1982), having received the permission of Grand Duchess Maria.
His mother decreed that Bettarini would have the title of Princess, with the predicate "Her Serene Highness" and the right to use the surname Romanova from her marriage, which therefore implies that theirs is a morganatic union.
Victoria Bettarini is the Director of the Russian Imperial Foundation.
Around 1500 guests attended the ceremony, including King Simeon II of Bulgaria and his wife Queen Margarita, King Fuad II of Egypt, Prince Mohammed bin Hamad of Qatar, Duarte Pio, Duke of Braganza and his wife Isabel, Duchess of Braganza, Prince Emanuele Filiberto, Prince of Piedmont, Leka, Prince of Albania and his wife Crown Princess Elia, Xavier Bettel, Prime Minister of Luxembourg and his husband Gauthier Destenay, Prince Louis, Duke of Anjou and his wife Princess Marie Marguerite, Duchess of Anjou, Prince Aimone, 6th Duke of Aosta and his wife, born Princess Olga of Greece, Russian monarchist and billionaire Konstantin Malofeev, Sarah Fabergé, French journalist and socialite Stéphane Bern, as well as many members of Russian, Spanish and European nobility.
The 500 guests included members of the royal houses of Albania, Afghanistan, Austria, Belgium, Bulgaria, Egypt, France, Greece, Italy, Liechtenstein, Portugal, Prussia, Qatar, and Spain.
The following day, a Wedding breakfast "à la Russe" was hosted by George's mother, the Grand Duchess Maria, held at Constantine Palace and was attended by a smaller number of 700 guests before their departures.
Children

The Grand Duke and Princess Victoria had a son, born in Moscow on 21 October 2022, who is named Alexander Georgievich Romanov.
Grand Duchess Maria Vladimirovna, a claimant to the throne of the Imperial House of Russia, announced that her first grandchild will be called "His Serene Highness Prince Alexander Georgievich Romanov".
Prince Alexander was baptized on 6 December 2022.
Prince Alexander's godparents are:
Alexander's baptisim marks the first time a descendant of the House of Romanov has been baptized in Russia since the Russian Revolution.
The Grand Duke and Princess Victoria had a daughter, born in Rome on 2 June 2025, Her Serene Highness Princess Kira Leonida Georgievna Romanova.
Princess Kira was baptized on 13 July 2025 in the Cathedral of Christ the Saviour in Moscow.
Princess Kira's godparents are Prince Emanuele Filiberto of Savoy, Prince Boris of Bulgaria, Prince David VII of Georgia, Archduke Maximilian of Austria, as well as the Russian Ambassador to the Seychelles, Artem Kozhin, his wife, Elena, and Oksana Hoffman Girey.



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
  AssignClass (734cf221-e0ff-4ba2-ac09-6e4cbdfac401)
 Call ID: 734cf221-e0ff-4ba2-ac09-6e4cbdfac401
  Args:
    type: :Woman
    source: Maria_Vladimirovna
  AssignClass (bfb889e5-da83-4e4d-8462-dc069a91d63d)
 Call ID: bfb889e5-da83-4e4d-8462-dc069a91d63d
  Args:
    type: :Man
    source: George_Mikhailovich
  AssignClass (88f56bcf-7221-42c4-992e-dde9dfa0cc9a)
 Call ID: 88f56bcf-7221-42c4-992e-dde9dfa0cc9a
  Args:
    type: :Man
    source: Franz_Wilhelm_of_Prussia
  AssignClass (385e33a3-3e02-4239-a107-a76ed325cfc0)
 Call ID: 385e33a3-3e02-4239-a107-a76ed325cfc0
  Args:
    type: :Man
    source: Vladimir_Cyrillovich
  AssignClass (36946d44-4bde-4c01-afc5-a077eedbfebd)
 Call ID: 36946d44-4bde-4c01-afc5-a077eedbfebd
  Args:
    type: :Man
    source: Karl_Franz_of_Prussia
  AssignClass (0e722ea3-b366-47cf-9540-b98cbbeef175)
 Call ID: 0e722ea3-b366-47cf-9540-b98cbbeef175
  Args:
    type: :Woman
    source: Henriette_of_Schoenaich-Carolath
  AssignClass (ca2e5b36-ec88-4c11-953c-67903e75f1bf)
 Call ID: ca2e5b36-ec88-4c11-953c-67903e75f1bf
  Args:
    type: :Woman
    source: Leonida
  AssignClass (9824e8f0-6979-4975-957b-40e3186a97ae)
 Call ID: 9824e8f0-6979-4975-957b-40e3186a97ae
  Args:
    type: :Woman
    source: Victoria_Romanovna_Bettarini
  AssignClass (019c1684-0a2e-49fd-a105-cb09fdb54f43)
 Call ID: 019c1684-0a2e-49fd-a105-cb09fdb54f43
  Args:
    type: :Man
    source: Alexander_Georgievich_Romanov
  AssignClass (d2fe16b1-706f-411f-a9c5-57a49d0af8a5)
 Call ID: d2fe16b1-706f-411f-a9c5-57a49d0af8a5
  Args:
    type: :Woman
    source: Kira_Leonida_Georgievna_Romanova
  AddTriple (fd550b21-e00a-4764-bf8f-b9dbcf1066b0)
 Call ID: fd550b21-e00a-4764-bf8f-b9dbcf1066b0
  Args:
    target: Franz_Wilhelm_of_Prussia
    relation: :hasFather
    source: George_Mikhailovich
  AddTriple (ba3d344a-757a-41b2-b195-0be12e95ab7c)
 Call ID: ba3d344a-757a-41b2-b195-0be12e95ab7c
  Args:
    target: Maria_Vladimirovna
    relation: :hasMother
    source: George_Mikhailovich
  AddTriple (ca10c543-ca8c-4be5-9263-a296d6db4bbf)
 Call ID: ca10c543-ca8c-4be5-9263-a296d6db4bbf
  Args:
    target: Vladimir_Cyrillovich
    source: Maria_Vladimirovna
    relation: :hasFather
  AddTriple (da7f0aef-910b-4c0a-8586-01168b5a3a61)
 Call ID: da7f0aef-910b-4c0a-8586-01168b5a3a61
  Args:
    target: Karl_Franz_of_Prussia
    source: Franz_Wilhelm_of_Prussia
    relation: :hasFather
  AddTriple (dfa53458-7754-40fe-94ef-102a56408945)
 Call ID: dfa53458-7754-40fe-94ef-102a56408945
  Args:
    source: Franz_Wilhelm_of_Prussia
    relation: :hasMother
    target: Henriette_of_Schoenaich-Carolath
  AddTriple (56c54580-3536-4ad2-832e-582114c93890)
 Call ID: 56c54580-3536-4ad2-832e-582114c93890
  Args:
    target: Maria_Vladimirovna
    source: George_Mikhailovich
    relation: :hasMother
  AddTriple (d635ccba-dd55-458c-aa4e-b042070a0ba1)
 Call ID: d635ccba-dd55-458c-aa4e-b042070a0ba1
  Args:
    target: Maria_Vladimirovna
    relation: :hasMother
    source: George_Mikhailovich
  AddTriple (766c4da8-ccfd-4424-bb94-677382770523)
 Call ID: 766c4da8-ccfd-4424-bb94-677382770523
  Args:
    target: Leonida
    source: Maria_Vladimirovna
    relation: :hasMother
  AddTriple (221618c5-e74a-4568-b518-1608d2201729)
 Call ID: 221618c5-e74a-4568-b518-1608d2201729
  Args:
    source: Alexander_Georgievich_Romanov
    relation: :hasFather
    target: George_Mikhailovich
  AddTriple (20970d15-4290-4852-8bb3-b54fff77e04c)
 Call ID: 20970d15-4290-4852-8bb3-b54fff77e04c
  Args:
    source: Alexander_Georgievich_Romanov
    relation: :hasMother
    target: Victoria_Romanovna_Bettarini
  AddTriple (49b788f6-9560-4b0d-ba2e-9968fc3ebca2)
 Call ID: 49b788f6-9560-4b0d-ba2e-9968fc3ebca2
  Args:
    target: George_Mikhailovich
    source: Kira_Leonida_Georgievna_Romanova
    relation: :hasFather
  AddTriple (e1a891fc-c1a6-4b49-b73d-6be31ccb2fd7)
 Call ID: e1a891fc-c1a6-4b49-b73d-6be31ccb2fd7
  Args:
    target: Victoria_Romanovna_Bettarini
    relation: :hasMother
    source: Kira_Leonida_Georgievna_Romanova
  AddLiteral (c40fbae3-61ee-4129-aa49-8c4680c35d98)
 Call ID: c40fbae3-61ee-4129-aa49-8c4680c35d98
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: George_Mikhailovich
    literal_value: 1981
  AddLiteral (3a7e0a63-0a2e-434a-9d6f-2d26c6955d41)
 Call ID: 3a7e0a63-0a2e-434a-9d6f-2d26c6955d41
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Victoria_Romanovna_Bettarini
    literal_value: 1982
  AddLiteral (51e29e15-847d-4572-897a-ef31ddc00c83)
 Call ID: 51e29e15-847d-4572-897a-ef31ddc00c83
  Args:
    source: Alexander_Georgievich_Romanov
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 2022
  AddLiteral (529f9bf9-526a-4d57-9957-daebcb4277a5)
 Call ID: 529f9bf9-526a-4d57-9957-daebcb4277a5
  Args:
    source: Kira_Leonida_Georgievna_Romanova
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 2025
  Finish (d8e9b14c-5c52-4744-936d-de91340d330e)
 Call ID: d8e9b14c-5c52-4744-936d-de91340d330e
  Args: