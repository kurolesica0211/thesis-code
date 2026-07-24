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
  AssignClass (2e3d17fc-5430-4db1-a232-900b77c21034)
 Call ID: 2e3d17fc-5430-4db1-a232-900b77c21034
  Args:
    type: :Woman
    source: Elena_Vladimirovna_of_Russia
  AssignClass (69de6f93-0d68-4e8e-9d40-52eb290a136c)
 Call ID: 69de6f93-0d68-4e8e-9d40-52eb290a136c
  Args:
    type: :Person
    source: Elena_Vladimirovna_of_Russia
  AddLiteral (2656be24-7ac1-478c-b555-89a6e8e41517)
 Call ID: 2656be24-7ac1-478c-b555-89a6e8e41517
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1882
    source: Elena_Vladimirovna_of_Russia
  AddLiteral (be730692-0e5f-4e13-b60b-405c2343089e)
 Call ID: be730692-0e5f-4e13-b60b-405c2343089e
  Args:
    relation: :hasDeathYear
    source: Elena_Vladimirovna_of_Russia
    literal_value: 1957
    literal_type: xsd:integer
  AssignClass (8cae69e3-b547-47f8-bd5f-f56322b291ed)
 Call ID: 8cae69e3-b547-47f8-bd5f-f56322b291ed
  Args:
    type: :Man
    source: Vladimir_Alexandrovich_of_Russia
  AssignClass (b3595c78-7c6a-4dcb-8bc4-509a899b8ef1)
 Call ID: b3595c78-7c6a-4dcb-8bc4-509a899b8ef1
  Args:
    type: :Person
    source: Vladimir_Alexandrovich_of_Russia
  AssignClass (456557d7-d579-48aa-9b62-4a0b2e3670a6)
 Call ID: 456557d7-d579-48aa-9b62-4a0b2e3670a6
  Args:
    type: :Woman
    source: Marie_of_Mecklenburg-Schwerin
  AssignClass (f1039b1a-e0de-48b1-817b-7d6075c71c2f)
 Call ID: f1039b1a-e0de-48b1-817b-7d6075c71c2f
  Args:
    type: :Person
    source: Marie_of_Mecklenburg-Schwerin
  AddTriple (53f8dbc1-4452-4520-a21d-4966cced4453)
 Call ID: 53f8dbc1-4452-4520-a21d-4966cced4453
  Args:
    relation: :hasFather
    target: Vladimir_Alexandrovich_of_Russia
    source: Elena_Vladimirovna_of_Russia
  AddTriple (04a55ef1-ce55-40a0-a589-4ff62c1c5904)
 Call ID: 04a55ef1-ce55-40a0-a589-4ff62c1c5904
  Args:
    target: Marie_of_Mecklenburg-Schwerin
    source: Elena_Vladimirovna_of_Russia
    relation: :hasMother
  AssignClass (838604aa-d474-4195-a30b-6f8a670b6d3a)
 Call ID: 838604aa-d474-4195-a30b-6f8a670b6d3a
  Args:
    type: :Man
    source: Nicholas_of_Greece_and_Denmark
  AssignClass (56dbf89f-8c62-444d-8fac-69b5d6ed27e2)
 Call ID: 56dbf89f-8c62-444d-8fac-69b5d6ed27e2
  Args:
    type: :Person
    source: Nicholas_of_Greece_and_Denmark
  AddTriple (f4322c3c-eef2-42ce-877a-7c705993ccf5)
 Call ID: f4322c3c-eef2-42ce-877a-7c705993ccf5
  Args:
    source: Elena_Vladimirovna_of_Russia
    target: Nicholas_of_Greece_and_Denmark
    relation: :hasRelation
  AddLiteral (bf8148db-2c35-4407-8a75-4e6c6de4a95d)
 Call ID: bf8148db-2c35-4407-8a75-4e6c6de4a95d
  Args:
    source: Elena_Vladimirovna_of_Russia
    literal_type: xsd:integer
    literal_value: 1902
    relation: :hasMarriageYear
  AssignClass (a785c5ef-e240-4367-aa8a-354307d099a5)
 Call ID: a785c5ef-e240-4367-aa8a-354307d099a5
  Args:
    type: :Man
    source: Kirill_of_Russia
  AssignClass (6d11e656-c230-44a5-b73e-fcd7f6c9433d)
 Call ID: 6d11e656-c230-44a5-b73e-fcd7f6c9433d
  Args:
    type: :Person
    source: Kirill_of_Russia
  AssignClass (1366a1ae-8cd9-4752-a6bf-f25f1f17b9ae)
 Call ID: 1366a1ae-8cd9-4752-a6bf-f25f1f17b9ae
  Args:
    type: :Man
    source: Boris_of_Russia
  AssignClass (1d5f2eb2-d2b4-472c-a4db-05f7c03e53f4)
 Call ID: 1d5f2eb2-d2b4-472c-a4db-05f7c03e53f4
  Args:
    type: :Person
    source: Boris_of_Russia
  AssignClass (5071f5e3-bf16-44fc-9e25-361f8b8a8611)
 Call ID: 5071f5e3-bf16-44fc-9e25-361f8b8a8611
  Args:
    type: :Man
    source: Andrei_of_Russia
  AssignClass (c1e4c728-0248-47a3-923d-54e35b2c1d37)
 Call ID: c1e4c728-0248-47a3-923d-54e35b2c1d37
  Args:
    type: :Person
    source: Andrei_of_Russia
  AddTriple (b89a9670-efc7-40fb-9b4c-a284ef96b344)
 Call ID: b89a9670-efc7-40fb-9b4c-a284ef96b344
  Args:
    source: Elena_Vladimirovna_of_Russia
    target: Kirill_of_Russia
    relation: :isSiblingOf
  AddTriple (9ee48f77-933a-45c6-8a1b-078bb8340742)
 Call ID: 9ee48f77-933a-45c6-8a1b-078bb8340742
  Args:
    source: Elena_Vladimirovna_of_Russia
    target: Boris_of_Russia
    relation: :isSiblingOf
  AddTriple (3d649055-b663-4e64-b89f-dd60166ec69f)
 Call ID: 3d649055-b663-4e64-b89f-dd60166ec69f
  Args:
    source: Elena_Vladimirovna_of_Russia
    target: Andrei_of_Russia
    relation: :isSiblingOf
  AssignClass (afa15afa-392a-4dca-9b38-da5a53b025bc)
 Call ID: afa15afa-392a-4dca-9b38-da5a53b025bc
  Args:
    type: :Woman
    source: Olga_of_Greece
  AssignClass (0f33c74c-f628-43fd-a106-a4c1705ab2f9)
 Call ID: 0f33c74c-f628-43fd-a106-a4c1705ab2f9
  Args:
    type: :Person
    source: Olga_of_Greece
  AssignClass (2358f2f9-985b-4d06-9fbf-5ff6ce448bd1)
 Call ID: 2358f2f9-985b-4d06-9fbf-5ff6ce448bd1
  Args:
    type: :Woman
    source: Elizabeth_of_Greece
  AssignClass (4cf4e6ee-242f-43e0-9bf7-cae279b9d166)
 Call ID: 4cf4e6ee-242f-43e0-9bf7-cae279b9d166
  Args:
    type: :Person
    source: Elizabeth_of_Greece
  AssignClass (f3eabf32-66e1-45a9-a1f7-24917abc12af)
 Call ID: f3eabf32-66e1-45a9-a1f7-24917abc12af
  Args:
    type: :Woman
    source: Marina_of_Greece
  AssignClass (99aba53c-ef08-4975-9830-19a08a37a55a)
 Call ID: 99aba53c-ef08-4975-9830-19a08a37a55a
  Args:
    type: :Person
    source: Marina_of_Greece
  AddTriple (03509c2d-c3ac-4c70-b302-cac4b97cb6e7)
 Call ID: 03509c2d-c3ac-4c70-b302-cac4b97cb6e7
  Args:
    target: Olga_of_Greece
    source: Elena_Vladimirovna_of_Russia
    relation: :hasDaughter
  AddTriple (a704a938-14b4-41b6-ab25-ed652c9a1893)
 Call ID: a704a938-14b4-41b6-ab25-ed652c9a1893
  Args:
    source: Elena_Vladimirovna_of_Russia
    target: Elizabeth_of_Greece
    relation: :hasDaughter
  AddTriple (1be90a96-befd-4a27-afc8-a3eb28c3abb7)
 Call ID: 1be90a96-befd-4a27-afc8-a3eb28c3abb7
  Args:
    source: Elena_Vladimirovna_of_Russia
    target: Marina_of_Greece
    relation: :hasDaughter
  AddTriple (9ff126c7-045a-40c3-96a1-4e57a90cbdad)
 Call ID: 9ff126c7-045a-40c3-96a1-4e57a90cbdad
  Args:
    source: Olga_of_Greece
    target: Nicholas_of_Greece_and_Denmark
    relation: :hasFather
  AddTriple (896a278f-1cca-4247-8b64-b18b6e6d9784)
 Call ID: 896a278f-1cca-4247-8b64-b18b6e6d9784
  Args:
    relation: :hasFather
    target: Nicholas_of_Greece_and_Denmark
    source: Elizabeth_of_Greece
  AddTriple (9ddeb358-9a03-4d98-9448-fbc084142e0d)
 Call ID: 9ddeb358-9a03-4d98-9448-fbc084142e0d
  Args:
    relation: :hasFather
    source: Marina_of_Greece
    target: Nicholas_of_Greece_and_Denmark
  Finish (f2fcabb8-e414-42c7-8c2c-3e93bebd2131)
 Call ID: f2fcabb8-e414-42c7-8c2c-3e93bebd2131
  Args: