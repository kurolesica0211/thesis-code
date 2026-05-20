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
Grand Duchess Elena Vladimirovna of Russia (Russian: Елена Владимировна Романова, romanized: Yelena Vladimirovna Romanova; 29 January 1882 – 13 March 1957) was the only daughter and youngest child of Grand Duke Vladimir Alexandrovich of Russia and Duchess Marie of Mecklenburg-Schwerin.
Her husband was Prince Nicholas of Greece and Denmark and they were both first cousins of Emperor Nicholas II of Russia.
She was also the first cousin of Alexandrine of Mecklenburg-Schwerin, Queen of Denmark, and the maternal grandmother of Prince Edward, Duke of Kent, Princess Alexandra, and Prince Michael of Kent.
Queen Juliana of the Netherlands was also her half-first cousin.
Early life

Elena and her three surviving older brothers, Kirill, Boris, and Andrei, had an English nanny and spoke English as their first language.
The young Elena had a temper and was sometimes out of control.
Elena, raised by a mother who was highly conscious of her social status, was also considered snobbish by some.
"


Marriage and children

She was engaged to Prince Max of Baden, but Max backed out of the engagement.
Elena's mother was furious and society gossiped about Elena's difficulty in finding a husband.
At one point in 1899, the 17-year-old Elena was reputedly engaged to Archduke Franz Ferdinand of Austria; however, this came to nothing as he fell in love with Countess Sophie Chotek.
Prince Nicholas of Greece and Denmark, the third son of George I of Greece, first proposed in 1900, but Elena's mother was reluctant to allow her daughter to marry a younger son with no real fortune or prospects of inheriting a throne.
She finally agreed to let Elena marry Nicholas, who was Elena's second cousin through his mother Olga Constantinovna of Russia and her father Vladimir Alexandrovich of Russia, in 1902 after it became clear that no other offers were on the horizon.
The couple married on 29 August 1902 in Tsarskoye Selo, Russia.
Like many imperial weddings, it was a grand affair, and was attended by the Emperor and Empress of Russia, the King and Queen of the Hellenes, among other royals and nobility of Russia.
Elena's "grand manner" irritated some people at court.
According to the British diplomat Francis Elliot, there was an incident between Elena and her sister-in-law Princess Marie Bonaparte:
Allegedly, Elena refused to greet Marie and "drew back her skirts as if not to be touched by her."
Elena thought that Marie was beneath her, because her grandfather operated the Monte Carlo Casino.
Elena looked down on another sister-in-law Princess Alice of Battenberg because of the latter's morganatic blood.
The Dowager Empress wrote that Elena "has a very brusque and arrogant tone that can shock people.
"


Wealth and residences

As a Russian grand duchess, Elena had been received an annuity of 15,000 roubles each year from birth, allowing her to accumulate a private fortune of approximately 300,000 roubles.
Upon her marriage her annuity ceased, and instead she received the customary imperial dowry of a Russian Grand Duchess, amounting to 1,000,000 roubles.
The dowry capital was held in Russia, from which Elena was paid an annual income of 50,000 roubles.
After a honeymoon at Ropsha, Elena and Nicholas travelled to the Kingdom of Greece aboard the Amphitrite and settled in a wing of the Royal Palace in Athens whilst their own residence was prepared.
In late 1902 they purchased a large house near the city centre, which was thereafter known as the Nicholas Palace.
Elena commissioned the royal architect Anastasios Metaxas to enlarge it with a Ziller-inspired second block, linked by a glazed atrium that illuminated the mansion’s core works.
Contemporaries described the Nicholas Palace as very modern for its time, with hot and cold running water.
Elena and Nicholas reportedly led a relatively simple but comfortable life in Athens.
Prince and Princess Nicholas took up residence at the newly-renovated Nicholas Palace in 1904.
And as a result, the Nicholas Palace was leased to the Hotel Grande Bretagne during the 1920s, who used the building as a 60-bed luxury annex known as the “Petit Palais”.
The Italian Government later purchased the Nicholas Palace from Elena in 1955; the site has subsequently remained the home of the Italian Embassy in Athens ever since.
Issue

Prince and Princess Nicholas of Greece and Denmark had three daughters:


Grand Duchess Elena suffered from ill health after the birth of Princess Marina, which caused her husband anguish.
According to her niece, Princess Sophie of Greece, Grand Duchess Elena's priorities throughout her life remained as follows: “God first, the Grand Dukes of Russia then and finally everything else.”
Thus, the Grand Duchess and her husband, Prince Nicholas, visited Russia annually to visit their relatives.
Life in exile

The family was later affected by the turmoil of the Russian Revolution of 1917 and the subsequent turmoil in Greece, which became a republic and resulted in the family living in France for a time.
While living in France, Grand Duchess Elena became deeply involved in charity work for Russian exiles, particularly children.
Short of money due to their exile from Greece and the loss of their Russian income, Prince Nicholas and his family lived in reduced circumstances.
Grand Duchess Elena's jewel collection, as well as Prince Nicholas' own artwork, were their sources of income.
Princess Olga of Greece married Prince Paul of Yugoslavia; Princess Elizabeth of Greece married Count Karl Theodor zu Toerring-Jettenbach, son of Duchess Sophie Adelheid in Bavaria and scion of an old and rich Bavarian mediatized family; and Princess Marina of Greece married Prince George, Duke of Kent in November 1934.
Grand Duchess Elena became a widow early in 1938, as Prince Nicholas suffered a heart attack and died suddenly.
She remained in Greece throughout the Second World War, dying there in 1957.



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
  AssignClass (d78b2510-dd18-4e7b-9e62-10e4c4bd163b)
 Call ID: d78b2510-dd18-4e7b-9e62-10e4c4bd163b
  Args:
    type: :Woman
    source: :Elena_Vladimirovna_of_Russia
  AssignClass (c136568d-13d3-4382-9b1e-df6f4dec595f)
 Call ID: c136568d-13d3-4382-9b1e-df6f4dec595f
  Args:
    type: :Person
    source: :Elena_Vladimirovna_of_Russia
  AddLiteral (8ff5f248-b5fd-4cc5-8e69-20ad30a2c128)
 Call ID: 8ff5f248-b5fd-4cc5-8e69-20ad30a2c128
  Args:
    source: :Elena_Vladimirovna_of_Russia
    literal_value: 1882
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (756b61e4-d5e8-429d-bc63-1c5fbcc6ca00)
 Call ID: 756b61e4-d5e8-429d-bc63-1c5fbcc6ca00
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1957
    source: :Elena_Vladimirovna_of_Russia
  AssignClass (f0bf79bb-e640-452c-8888-146224c2988f)
 Call ID: f0bf79bb-e640-452c-8888-146224c2988f
  Args:
    source: :Vladimir_Alexandrovich_of_Russia
    type: :Man
  AssignClass (123bf7ec-4106-431b-adfc-434dd0fdb798)
 Call ID: 123bf7ec-4106-431b-adfc-434dd0fdb798
  Args:
    type: :Ancestor
    source: :Vladimir_Alexandrovich_of_Russia
  AssignClass (17357da5-3862-4607-8690-fb9aef7b35d6)
 Call ID: 17357da5-3862-4607-8690-fb9aef7b35d6
  Args:
    type: :Woman
    source: :Marie_of_Mecklenburg-Schwerin
  AssignClass (8f0eb11c-e33c-42ab-9d94-6d8ca9f681a3)
 Call ID: 8f0eb11c-e33c-42ab-9d94-6d8ca9f681a3
  Args:
    source: :Marie_of_Mecklenburg-Schwerin
    type: :Ancestor
  AddTriple (4aab8cf0-eab0-492f-aac1-f1f3d0b4b1eb)
 Call ID: 4aab8cf0-eab0-492f-aac1-f1f3d0b4b1eb
  Args:
    target: :Vladimir_Alexandrovich_of_Russia
    relation: :hasFather
    source: :Elena_Vladimirovna_of_Russia
  AddTriple (a8047d7d-f3f7-40c9-8e7c-0b0b139754cb)
 Call ID: a8047d7d-f3f7-40c9-8e7c-0b0b139754cb
  Args:
    relation: :hasMother
    target: :Marie_of_Mecklenburg-Schwerin
    source: :Elena_Vladimirovna_of_Russia
  AssignClass (cd5dfd3b-e770-4b75-abeb-f5ac568cc518)
 Call ID: cd5dfd3b-e770-4b75-abeb-f5ac568cc518
  Args:
    type: :Man
    source: :Nicholas_of_Greece_and_Denmark
  AssignClass (66db12fd-4f35-48dc-bb4a-6d7d066f1cd0)
 Call ID: 66db12fd-4f35-48dc-bb4a-6d7d066f1cd0
  Args:
    source: :Nicholas_of_Greece_and_Denmark
    type: :Person
  AddTriple (dac93e59-54cc-437f-8475-c70b641c20f5)
 Call ID: dac93e59-54cc-437f-8475-c70b641c20f5
  Args:
    target: :Nicholas_of_Greece_and_Denmark
    relation: :hasRelation
    source: :Elena_Vladimirovna_of_Russia
  AddLiteral (b6594c2d-2487-4c7a-9b33-5eb29bae425f)
 Call ID: b6594c2d-2487-4c7a-9b33-5eb29bae425f
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 1902
    source: :Elena_Vladimirovna_of_Russia
  AssignClass (7b602254-f688-491d-a09f-98d6e537cb7f)
 Call ID: 7b602254-f688-491d-a09f-98d6e537cb7f
  Args:
    source: :Kirill_of_Russia
    type: :Man
  AssignClass (543c3e98-21f1-428a-9b6e-7fa19002a6d6)
 Call ID: 543c3e98-21f1-428a-9b6e-7fa19002a6d6
  Args:
    source: :Kirill_of_Russia
    type: :Person
  AssignClass (e7f3cd56-569b-494b-b1fb-3588138e16ae)
 Call ID: e7f3cd56-569b-494b-b1fb-3588138e16ae
  Args:
    type: :Man
    source: :Boris_of_Russia
  AssignClass (99ff7aae-ffcb-4b40-983c-0009b8d5b385)
 Call ID: 99ff7aae-ffcb-4b40-983c-0009b8d5b385
  Args:
    source: :Boris_of_Russia
    type: :Person
  AssignClass (95b081e7-40c2-49d9-91c0-a62950975530)
 Call ID: 95b081e7-40c2-49d9-91c0-a62950975530
  Args:
    type: :Man
    source: :Andrei_of_Russia
  AssignClass (73df7f4f-96ba-4adc-8c4e-a8915e63e2b6)
 Call ID: 73df7f4f-96ba-4adc-8c4e-a8915e63e2b6
  Args:
    type: :Person
    source: :Andrei_of_Russia
  AddTriple (b6cf2c27-220c-4775-ac45-851f1be2262a)
 Call ID: b6cf2c27-220c-4775-ac45-851f1be2262a
  Args:
    target: :Kirill_of_Russia
    relation: :hasBrother
    source: :Elena_Vladimirovna_of_Russia
  AddTriple (66613362-687a-4f6a-9b55-b740285673a7)
 Call ID: 66613362-687a-4f6a-9b55-b740285673a7
  Args:
    source: :Elena_Vladimirovna_of_Russia
    target: :Boris_of_Russia
    relation: :hasBrother
  AddTriple (92772417-3c4f-4f70-af75-6490d34d9594)
 Call ID: 92772417-3c4f-4f70-af75-6490d34d9594
  Args:
    target: :Andrei_of_Russia
    relation: :hasBrother
    source: :Elena_Vladimirovna_of_Russia
  AssignClass (22c52a25-db3d-4cab-b04d-c7bbf8b8d225)
 Call ID: 22c52a25-db3d-4cab-b04d-c7bbf8b8d225
  Args:
    type: :Woman
    source: :Olga_of_Greece
  AssignClass (a3407f6f-563d-4fb9-9667-b83c69ca7501)
 Call ID: a3407f6f-563d-4fb9-9667-b83c69ca7501
  Args:
    type: :Person
    source: :Olga_of_Greece
  AssignClass (6dde7f2a-c3d9-47b8-93d8-a4b4b7560ee2)
 Call ID: 6dde7f2a-c3d9-47b8-93d8-a4b4b7560ee2
  Args:
    source: :Elizabeth_of_Greece
    type: :Woman
  AssignClass (f577e276-eaa3-4c65-b87f-b05df8145709)
 Call ID: f577e276-eaa3-4c65-b87f-b05df8145709
  Args:
    type: :Person
    source: :Elizabeth_of_Greece
  AssignClass (e3b299e9-6956-49a4-b9bd-0b0cc2db641f)
 Call ID: e3b299e9-6956-49a4-b9bd-0b0cc2db641f
  Args:
    source: :Marina_of_Greece
    type: :Woman
  AssignClass (4098d623-c475-4327-b5fe-92b15e2447dc)
 Call ID: 4098d623-c475-4327-b5fe-92b15e2447dc
  Args:
    type: :Person
    source: :Marina_of_Greece
  AddTriple (48828179-fc39-441c-ba28-6d6bd9135265)
 Call ID: 48828179-fc39-441c-ba28-6d6bd9135265
  Args:
    source: :Elena_Vladimirovna_of_Russia
    relation: :hasDaughter
    target: :Olga_of_Greece
  AddTriple (36a5472a-efe6-4a60-acb3-68d245157c06)
 Call ID: 36a5472a-efe6-4a60-acb3-68d245157c06
  Args:
    relation: :hasDaughter
    target: :Elizabeth_of_Greece
    source: :Elena_Vladimirovna_of_Russia
  AddTriple (d5623282-e6e3-47ec-9535-a94fd94d0f25)
 Call ID: d5623282-e6e3-47ec-9535-a94fd94d0f25
  Args:
    source: :Elena_Vladimirovna_of_Russia
    relation: :hasDaughter
    target: :Marina_of_Greece
  Finish (5a98bf20-88ad-48fb-8c03-6fd6f2b2df93)
 Call ID: 5a98bf20-88ad-48fb-8c03-6fd6f2b2df93
  Args: