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
  AssignClass (f0c46a81-369e-4099-8d98-659fabcd7c62)
 Call ID: f0c46a81-369e-4099-8d98-659fabcd7c62
  Args:
    type: :Woman
    source: Elena_Vladimirovna
  AssignClass (b5433062-f4d7-4835-9ad3-b746f17b4e83)
 Call ID: b5433062-f4d7-4835-9ad3-b746f17b4e83
  Args:
    source: Elena_Vladimirovna
    type: :Person
  AddLiteral (ade149d5-e3fd-425a-9415-9800798e0fbe)
 Call ID: ade149d5-e3fd-425a-9415-9800798e0fbe
  Args:
    literal_value: 1882
    literal_type: xsd:integer
    source: Elena_Vladimirovna
    relation: :hasBirthYear
  AddLiteral (932e1649-f6d1-43ec-a1c0-a475772f9534)
 Call ID: 932e1649-f6d1-43ec-a1c0-a475772f9534
  Args:
    relation: :hasDeathYear
    source: Elena_Vladimirovna
    literal_value: 1957
    literal_type: xsd:integer
  AssignClass (8e3bedf4-00f8-4cac-ac8b-1026133d92c1)
 Call ID: 8e3bedf4-00f8-4cac-ac8b-1026133d92c1
  Args:
    source: Vladimir_Alexandrovich
    type: :Man
  AssignClass (722cfd54-013d-448d-ac41-fefaaf2ae1dd)
 Call ID: 722cfd54-013d-448d-ac41-fefaaf2ae1dd
  Args:
    source: Vladimir_Alexandrovich
    type: :Person
  AssignClass (95899611-72ad-48b6-a388-16fd922c30ad)
 Call ID: 95899611-72ad-48b6-a388-16fd922c30ad
  Args:
    type: :Woman
    source: Marie_of_Mecklenburg_Schwerin
  AssignClass (7e7e2b4b-8e5e-4d41-88d2-7b96f7bba45d)
 Call ID: 7e7e2b4b-8e5e-4d41-88d2-7b96f7bba45d
  Args:
    source: Marie_of_Mecklenburg_Schwerin
    type: :Person
  AddTriple (40fd162c-3b9d-47b8-8fc2-0b6aff4186af)
 Call ID: 40fd162c-3b9d-47b8-8fc2-0b6aff4186af
  Args:
    relation: :hasFather
    source: Elena_Vladimirovna
    target: Vladimir_Alexandrovich
  AddTriple (6dfa587b-a0e3-4550-946b-2b9b7da07566)
 Call ID: 6dfa587b-a0e3-4550-946b-2b9b7da07566
  Args:
    target: Marie_of_Mecklenburg_Schwerin
    source: Elena_Vladimirovna
    relation: :hasMother
  AssignClass (1d9f639f-0bcd-48f1-b4e4-95d85e873b57)
 Call ID: 1d9f639f-0bcd-48f1-b4e4-95d85e873b57
  Args:
    source: Nicholas_of_Greece_and_Denmark
    type: :Man
  AssignClass (3ef5ef86-bab2-4c5f-9768-3200467af51a)
 Call ID: 3ef5ef86-bab2-4c5f-9768-3200467af51a
  Args:
    type: :Person
    source: Nicholas_of_Greece_and_Denmark
  AddTriple (df07f2a4-9b52-4adb-a8f3-7bc965305a4e)
 Call ID: df07f2a4-9b52-4adb-a8f3-7bc965305a4e
  Args:
    source: Elena_Vladimirovna
    relation: :hasRelation
    target: Nicholas_of_Greece_and_Denmark
  AddLiteral (54811121-45b1-4856-b800-c14d9bd4f8ca)
 Call ID: 54811121-45b1-4856-b800-c14d9bd4f8ca
  Args:
    source: Elena_Vladimirovna
    relation: :hasMarriageYear
    literal_type: xsd:integer
    literal_value: 1902
  AssignClass (0e8d8c95-f3b3-40ad-9dbe-8cb65221ff98)
 Call ID: 0e8d8c95-f3b3-40ad-9dbe-8cb65221ff98
  Args:
    source: Kirill
    type: :Man
  AssignClass (1c948e14-a517-404d-af53-0bd9a68c5a0b)
 Call ID: 1c948e14-a517-404d-af53-0bd9a68c5a0b
  Args:
    type: :Person
    source: Kirill
  AssignClass (6f657728-3bad-4b2b-8ba8-39f2f296fa19)
 Call ID: 6f657728-3bad-4b2b-8ba8-39f2f296fa19
  Args:
    type: :Man
    source: Boris
  AssignClass (96d75e12-d8fa-43ac-a95e-1baba069a4c3)
 Call ID: 96d75e12-d8fa-43ac-a95e-1baba069a4c3
  Args:
    type: :Person
    source: Boris
  AssignClass (4ccb6fad-bb80-4b61-a924-f2d90be25815)
 Call ID: 4ccb6fad-bb80-4b61-a924-f2d90be25815
  Args:
    source: Andrei
    type: :Man
  AssignClass (406856ac-9d17-4de3-8ef5-0991c58a4c96)
 Call ID: 406856ac-9d17-4de3-8ef5-0991c58a4c96
  Args:
    type: :Person
    source: Andrei
  AddTriple (7c4bacfd-ebbc-410d-aa07-1a9612fda962)
 Call ID: 7c4bacfd-ebbc-410d-aa07-1a9612fda962
  Args:
    relation: :hasBrother
    source: Elena_Vladimirovna
    target: Kirill
  AddTriple (46583f4a-3049-4259-a49b-fa3b13143d64)
 Call ID: 46583f4a-3049-4259-a49b-fa3b13143d64
  Args:
    target: Boris
    source: Elena_Vladimirovna
    relation: :hasBrother
  AddTriple (6096f3a7-9560-4893-b6dc-3c33383a59c9)
 Call ID: 6096f3a7-9560-4893-b6dc-3c33383a59c9
  Args:
    target: Andrei
    relation: :hasBrother
    source: Elena_Vladimirovna
  AssignClass (f66fb0e9-ed81-499f-b13d-ff56f22a6373)
 Call ID: f66fb0e9-ed81-499f-b13d-ff56f22a6373
  Args:
    source: Olga_Constantinovna_of_Russia
    type: :Woman
  AssignClass (e9c12c1b-1adf-45a2-a9dc-2fb7fc16f0bd)
 Call ID: e9c12c1b-1adf-45a2-a9dc-2fb7fc16f0bd
  Args:
    source: Olga_Constantinovna_of_Russia
    type: :Person
  AddTriple (391e6192-85f1-4641-960e-fd03c1ceb6cd)
 Call ID: 391e6192-85f1-4641-960e-fd03c1ceb6cd
  Args:
    source: Nicholas_of_Greece_and_Denmark
    relation: :hasMother
    target: Olga_Constantinovna_of_Russia
  AssignClass (c851b78a-88a0-4af8-928a-f993899dd961)
 Call ID: c851b78a-88a0-4af8-928a-f993899dd961
  Args:
    type: :Man
    source: George_I_of_Greece
  AssignClass (dd50016c-1235-4ceb-83e9-97e14878a882)
 Call ID: dd50016c-1235-4ceb-83e9-97e14878a882
  Args:
    type: :Person
    source: George_I_of_Greece
  AddTriple (a6fa01a4-a6ec-466c-b3fe-35e4bd9b9b42)
 Call ID: a6fa01a4-a6ec-466c-b3fe-35e4bd9b9b42
  Args:
    target: George_I_of_Greece
    relation: :hasFather
    source: Nicholas_of_Greece_and_Denmark
  AssignClass (3aeb7039-ad19-4a0c-9d38-963b429936eb)
 Call ID: 3aeb7039-ad19-4a0c-9d38-963b429936eb
  Args:
    source: Princess_Olga_of_Greece
    type: :Woman
  AssignClass (49e27ccc-7794-46cb-b8ac-58ccd7588c80)
 Call ID: 49e27ccc-7794-46cb-b8ac-58ccd7588c80
  Args:
    source: Princess_Olga_of_Greece
    type: :Person
  AssignClass (58532886-8cf7-4961-ae90-409455bbbd61)
 Call ID: 58532886-8cf7-4961-ae90-409455bbbd61
  Args:
    source: Princess_Elizabeth_of_Greece
    type: :Woman
  AssignClass (87285b70-40bb-41db-8a0b-f7f8073b525a)
 Call ID: 87285b70-40bb-41db-8a0b-f7f8073b525a
  Args:
    type: :Person
    source: Princess_Elizabeth_of_Greece
  AssignClass (d749cfaf-180a-4633-9ffe-9e38a4f55520)
 Call ID: d749cfaf-180a-4633-9ffe-9e38a4f55520
  Args:
    source: Princess_Marina_of_Greece
    type: :Woman
  AssignClass (36809f28-1043-4d54-830e-bf7cd5634772)
 Call ID: 36809f28-1043-4d54-830e-bf7cd5634772
  Args:
    source: Princess_Marina_of_Greece
    type: :Person
  AddTriple (0a2c13e1-2c23-43ad-9034-1a93c70fa122)
 Call ID: 0a2c13e1-2c23-43ad-9034-1a93c70fa122
  Args:
    source: Elena_Vladimirovna
    relation: :hasDaughter
    target: Princess_Olga_of_Greece
  AddTriple (bb1596d2-0cde-4e70-8c33-2530e1c08af8)
 Call ID: bb1596d2-0cde-4e70-8c33-2530e1c08af8
  Args:
    source: Elena_Vladimirovna
    relation: :hasDaughter
    target: Princess_Elizabeth_of_Greece
  AddTriple (dfd6854a-78d2-446a-a0b7-30b4e9ac505e)
 Call ID: dfd6854a-78d2-446a-a0b7-30b4e9ac505e
  Args:
    relation: :hasDaughter
    source: Elena_Vladimirovna
    target: Princess_Marina_of_Greece
  AddTriple (6e00ed75-592c-42c8-9213-994666954581)
 Call ID: 6e00ed75-592c-42c8-9213-994666954581
  Args:
    target: Elena_Vladimirovna
    relation: :hasMother
    source: Princess_Olga_of_Greece
  AddTriple (c0299355-ccca-4e50-939f-83832950f9ff)
 Call ID: c0299355-ccca-4e50-939f-83832950f9ff
  Args:
    source: Princess_Elizabeth_of_Greece
    relation: :hasMother
    target: Elena_Vladimirovna
  AddTriple (1bd4ba1a-1276-4ee9-866a-30ba087b9b4a)
 Call ID: 1bd4ba1a-1276-4ee9-866a-30ba087b9b4a
  Args:
    relation: :hasMother
    source: Princess_Marina_of_Greece
    target: Elena_Vladimirovna
  AddTriple (4012e2a6-1a3d-4ef6-aec3-141b5a14b583)
 Call ID: 4012e2a6-1a3d-4ef6-aec3-141b5a14b583
  Args:
    relation: :hasFather
    source: Princess_Olga_of_Greece
    target: Nicholas_of_Greece_and_Denmark
  AddTriple (550cff6a-f684-44c4-af47-bce54c241413)
 Call ID: 550cff6a-f684-44c4-af47-bce54c241413
  Args:
    target: Nicholas_of_Greece_and_Denmark
    relation: :hasFather
    source: Princess_Elizabeth_of_Greece
  AddTriple (bbc7cc5c-bd38-4cf9-9143-500e5662e5a7)
 Call ID: bbc7cc5c-bd38-4cf9-9143-500e5662e5a7
  Args:
    relation: :hasFather
    source: Princess_Marina_of_Greece
    target: Nicholas_of_Greece_and_Denmark
  Finish (0b62d7c4-c742-409a-aae8-ccfe27f9b87a)
 Call ID: 0b62d7c4-c742-409a-aae8-ccfe27f9b87a
  Args: