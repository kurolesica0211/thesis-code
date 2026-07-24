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
  AssignClass (30c03fc8-2e70-47ed-93ec-96768bfdfa9e)
 Call ID: 30c03fc8-2e70-47ed-93ec-96768bfdfa9e
  Args:
    type: :Woman
    source: ElenaVladimirovna
  AssignClass (28d7d5cb-9ea1-4075-860b-9c8968db06a0)
 Call ID: 28d7d5cb-9ea1-4075-860b-9c8968db06a0
  Args:
    source: ElenaVladimirovna
    type: :Person
  AddLiteral (a616bf51-16f7-46b2-b8a6-abf12130e545)
 Call ID: a616bf51-16f7-46b2-b8a6-abf12130e545
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: ElenaVladimirovna
    literal_value: 1882
  AddLiteral (3333522e-f205-4e24-87bb-4539fc5bf631)
 Call ID: 3333522e-f205-4e24-87bb-4539fc5bf631
  Args:
    source: ElenaVladimirovna
    literal_value: 1957
    literal_type: xsd:integer
    relation: :hasDeathYear
  AssignClass (36cd7011-dbb0-4ab9-8f02-71f34a74f3e0)
 Call ID: 36cd7011-dbb0-4ab9-8f02-71f34a74f3e0
  Args:
    type: :Man
    source: VladimirAlexandrovich
  AssignClass (20089273-6984-4109-8d7e-112a968aa01f)
 Call ID: 20089273-6984-4109-8d7e-112a968aa01f
  Args:
    source: VladimirAlexandrovich
    type: :Person
  AssignClass (d121a66c-4020-40aa-b987-ea1f421a672b)
 Call ID: d121a66c-4020-40aa-b987-ea1f421a672b
  Args:
    type: :Woman
    source: MarieMecklenburgSchwerin
  AssignClass (6caa926d-357a-4825-ad9e-f8bc4463fe33)
 Call ID: 6caa926d-357a-4825-ad9e-f8bc4463fe33
  Args:
    source: MarieMecklenburgSchwerin
    type: :Person
  AddTriple (2314888f-2de7-46dc-9788-3ee62a698d51)
 Call ID: 2314888f-2de7-46dc-9788-3ee62a698d51
  Args:
    target: VladimirAlexandrovich
    source: ElenaVladimirovna
    relation: :hasFather
  AddTriple (a1884bde-5c8e-451e-b653-bbd3f458ed02)
 Call ID: a1884bde-5c8e-451e-b653-bbd3f458ed02
  Args:
    source: ElenaVladimirovna
    target: MarieMecklenburgSchwerin
    relation: :hasMother
  AssignClass (91b7a475-5c1b-4fed-b017-a72801966a47)
 Call ID: 91b7a475-5c1b-4fed-b017-a72801966a47
  Args:
    type: :Man
    source: NicholasGreeceDenmark
  AssignClass (16b67505-97b4-4c44-8d26-a1be0c37266f)
 Call ID: 16b67505-97b4-4c44-8d26-a1be0c37266f
  Args:
    source: NicholasGreeceDenmark
    type: :Person
  AddTriple (4468cb2f-5fd4-4e0c-8edc-ac707c7f68f2)
 Call ID: 4468cb2f-5fd4-4e0c-8edc-ac707c7f68f2
  Args:
    relation: :hasRelation
    source: ElenaVladimirovna
    target: NicholasGreeceDenmark
  AddLiteral (dc942664-5556-4f95-afe0-a99a8f559b69)
 Call ID: dc942664-5556-4f95-afe0-a99a8f559b69
  Args:
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: ElenaVladimirovna
    literal_value: 1902
  AssignClass (dfb793d3-c7f3-42df-bf8d-9ba3451b28ce)
 Call ID: dfb793d3-c7f3-42df-bf8d-9ba3451b28ce
  Args:
    source: Kirill
    type: :Man
  AssignClass (a6401c28-f793-4f11-a93b-ad3c6b849b36)
 Call ID: a6401c28-f793-4f11-a93b-ad3c6b849b36
  Args:
    type: :Person
    source: Kirill
  AssignClass (51298d61-eec4-4549-bed9-87373727de81)
 Call ID: 51298d61-eec4-4549-bed9-87373727de81
  Args:
    source: Boris
    type: :Man
  AssignClass (99c80cfd-6243-4ecf-bb5a-8130a11f0264)
 Call ID: 99c80cfd-6243-4ecf-bb5a-8130a11f0264
  Args:
    source: Boris
    type: :Person
  AssignClass (7c91223a-79e2-4e28-9c07-14b3649c808f)
 Call ID: 7c91223a-79e2-4e28-9c07-14b3649c808f
  Args:
    type: :Man
    source: Andrei
  AssignClass (6c187f93-5e5d-4038-8b25-b9b9a73de37c)
 Call ID: 6c187f93-5e5d-4038-8b25-b9b9a73de37c
  Args:
    source: Andrei
    type: :Person
  AddTriple (64d66b75-b9ce-4837-a5d7-f563409433a9)
 Call ID: 64d66b75-b9ce-4837-a5d7-f563409433a9
  Args:
    target: Kirill
    source: ElenaVladimirovna
    relation: :isSiblingOf
  AddTriple (35fe3637-cc3a-4cd3-95e1-538a12ac70b4)
 Call ID: 35fe3637-cc3a-4cd3-95e1-538a12ac70b4
  Args:
    relation: :isSiblingOf
    target: Boris
    source: ElenaVladimirovna
  AddTriple (96973c82-c91f-4162-8fae-68ef04e42d15)
 Call ID: 96973c82-c91f-4162-8fae-68ef04e42d15
  Args:
    relation: :isSiblingOf
    source: ElenaVladimirovna
    target: Andrei
  AssignClass (c80d4c3b-7b91-4ddf-b247-a2446352f7ba)
 Call ID: c80d4c3b-7b91-4ddf-b247-a2446352f7ba
  Args:
    source: OlgaConstantinovna
    type: :Woman
  AssignClass (5f12e286-fed7-4bd5-b95a-dad20730373b)
 Call ID: 5f12e286-fed7-4bd5-b95a-dad20730373b
  Args:
    source: OlgaConstantinovna
    type: :Person
  AddTriple (5d5eb996-b80f-482b-b6dd-a1b6af562bae)
 Call ID: 5d5eb996-b80f-482b-b6dd-a1b6af562bae
  Args:
    source: NicholasGreeceDenmark
    target: OlgaConstantinovna
    relation: :hasMother
  AssignClass (b5776512-7d21-4474-814d-737c2a67e68e)
 Call ID: b5776512-7d21-4474-814d-737c2a67e68e
  Args:
    source: GeorgeIGreece
    type: :Man
  AssignClass (1e8b915f-25e1-45ef-9898-d14d2e404062)
 Call ID: 1e8b915f-25e1-45ef-9898-d14d2e404062
  Args:
    source: GeorgeIGreece
    type: :Person
  AddTriple (37d28803-eebd-4983-a6ee-d4653fe1a7c8)
 Call ID: 37d28803-eebd-4983-a6ee-d4653fe1a7c8
  Args:
    relation: :hasFather
    source: NicholasGreeceDenmark
    target: GeorgeIGreece
  AssignClass (eb546506-7642-42a6-ad23-f628cc8c432b)
 Call ID: eb546506-7642-42a6-ad23-f628cc8c432b
  Args:
    source: OlgaGreece
    type: :Woman
  AssignClass (479bd74d-c404-492f-9893-7f72fb2dee52)
 Call ID: 479bd74d-c404-492f-9893-7f72fb2dee52
  Args:
    type: :Person
    source: OlgaGreece
  AssignClass (5d92d908-5900-42af-8e4f-c25cd9fdb838)
 Call ID: 5d92d908-5900-42af-8e4f-c25cd9fdb838
  Args:
    type: :Woman
    source: ElizabethGreece
  AssignClass (23114c66-5e7b-4e11-ab3b-65c8267baba5)
 Call ID: 23114c66-5e7b-4e11-ab3b-65c8267baba5
  Args:
    type: :Person
    source: ElizabethGreece
  AssignClass (f84e4919-2a43-4eef-98ad-e575f786c35e)
 Call ID: f84e4919-2a43-4eef-98ad-e575f786c35e
  Args:
    type: :Woman
    source: MarinaGreece
  AssignClass (9f3a27a3-4de6-499f-9edf-4d4dec050b94)
 Call ID: 9f3a27a3-4de6-499f-9edf-4d4dec050b94
  Args:
    type: :Person
    source: MarinaGreece
  AddTriple (f87a755f-d237-47cf-a0fc-9a77b2559d10)
 Call ID: f87a755f-d237-47cf-a0fc-9a77b2559d10
  Args:
    relation: :hasChild
    target: OlgaGreece
    source: ElenaVladimirovna
  AddTriple (fe45c8c2-f5be-4efb-b6f2-c69009be57d1)
 Call ID: fe45c8c2-f5be-4efb-b6f2-c69009be57d1
  Args:
    source: ElenaVladimirovna
    target: ElizabethGreece
    relation: :hasChild
  AddTriple (8ff2fdd8-fb0d-4408-bcf2-a6548793525e)
 Call ID: 8ff2fdd8-fb0d-4408-bcf2-a6548793525e
  Args:
    source: ElenaVladimirovna
    target: MarinaGreece
    relation: :hasChild
  AddTriple (8140f2a8-1ccd-46fa-be06-bb46b745a908)
 Call ID: 8140f2a8-1ccd-46fa-be06-bb46b745a908
  Args:
    relation: :hasChild
    source: NicholasGreeceDenmark
    target: OlgaGreece
  AddTriple (749027fe-0a03-4566-983b-a7888bb2b53e)
 Call ID: 749027fe-0a03-4566-983b-a7888bb2b53e
  Args:
    relation: :hasChild
    source: NicholasGreeceDenmark
    target: ElizabethGreece
  AddTriple (3ac26a1d-7999-4bb5-a5d2-12876a0780a7)
 Call ID: 3ac26a1d-7999-4bb5-a5d2-12876a0780a7
  Args:
    target: MarinaGreece
    source: NicholasGreeceDenmark
    relation: :hasChild
  AddLiteral (566f51e9-4d89-4a86-8729-0bce01bec06e)
 Call ID: 566f51e9-4d89-4a86-8729-0bce01bec06e
  Args:
    literal_value: 1938
    source: NicholasGreeceDenmark
    literal_type: xsd:integer
    relation: :hasDeathYear
  Finish (d67f70a6-38c6-4dcc-9694-efb2075d1f15)
 Call ID: d67f70a6-38c6-4dcc-9694-efb2075d1f15
  Args: