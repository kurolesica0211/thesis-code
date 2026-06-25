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
  AssignClass (8bb89348-8060-4b77-8117-ed719f174aca)
 Call ID: 8bb89348-8060-4b77-8117-ed719f174aca
  Args:
    type: :Woman
    source: :Grand_Duchess_Elena_Vladimirovna_of_Russia
  AssignClass (fc36fdd9-c9b2-4c2d-87b5-4f83d09f9b59)
 Call ID: fc36fdd9-c9b2-4c2d-87b5-4f83d09f9b59
  Args:
    source: :Grand_Duchess_Elena_Vladimirovna_of_Russia
    type: :Person
  AddLiteral (6e68de4d-5613-497a-976d-cf5eddb0cf67)
 Call ID: 6e68de4d-5613-497a-976d-cf5eddb0cf67
  Args:
    relation: :hasBirthYear
    source: :Grand_Duchess_Elena_Vladimirovna_of_Russia
    literal_value: 1882
    literal_type: xsd:integer
  AddLiteral (0c4fd0d5-31bc-465a-87b0-5adf4cad691b)
 Call ID: 0c4fd0d5-31bc-465a-87b0-5adf4cad691b
  Args:
    source: :Grand_Duchess_Elena_Vladimirovna_of_Russia
    relation: :hasDeathYear
    literal_value: 1957
    literal_type: xsd:integer
  AssignClass (5a11dc7f-681f-49d6-88cf-066dd899edfe)
 Call ID: 5a11dc7f-681f-49d6-88cf-066dd899edfe
  Args:
    type: :Man
    source: :Grand_Duke_Vladimir_Alexandrovich_of_Russia
  AssignClass (b45066a2-d2ad-43b0-9bc2-71ad0d46c69d)
 Call ID: b45066a2-d2ad-43b0-9bc2-71ad0d46c69d
  Args:
    source: :Grand_Duke_Vladimir_Alexandrovich_of_Russia
    type: :Person
  AssignClass (3dae58ce-8c0c-4151-b42d-8f624df1d034)
 Call ID: 3dae58ce-8c0c-4151-b42d-8f624df1d034
  Args:
    type: :Woman
    source: :Duchess_Marie_of_Mecklenburg_Schwerin
  AssignClass (24691e8c-3ecc-4ddc-9318-061fae6561b1)
 Call ID: 24691e8c-3ecc-4ddc-9318-061fae6561b1
  Args:
    source: :Duchess_Marie_of_Mecklenburg_Schwerin
    type: :Person
  AddTriple (58090ed3-fa2f-41b8-9d25-b269cafee9ac)
 Call ID: 58090ed3-fa2f-41b8-9d25-b269cafee9ac
  Args:
    source: :Grand_Duchess_Elena_Vladimirovna_of_Russia
    target: :Grand_Duke_Vladimir_Alexandrovich_of_Russia
    relation: :hasFather
  AddTriple (61c68d60-84c8-4bb3-81d1-3e476f6b2901)
 Call ID: 61c68d60-84c8-4bb3-81d1-3e476f6b2901
  Args:
    target: :Duchess_Marie_of_Mecklenburg_Schwerin
    source: :Grand_Duchess_Elena_Vladimirovna_of_Russia
    relation: :hasMother
  AssignClass (3257f762-448c-4a25-aa1f-7f364f09e3c6)
 Call ID: 3257f762-448c-4a25-aa1f-7f364f09e3c6
  Args:
    source: :Prince_Nicholas_of_Greece_and_Denmark
    type: :Man
  AssignClass (952ed32e-b334-4494-a562-7459d7375bef)
 Call ID: 952ed32e-b334-4494-a562-7459d7375bef
  Args:
    source: :Prince_Nicholas_of_Greece_and_Denmark
    type: :Person
  AddTriple (1ee7f72e-b98c-4516-9ef6-36fc557b2851)
 Call ID: 1ee7f72e-b98c-4516-9ef6-36fc557b2851
  Args:
    relation: :hasRelation
    target: :Prince_Nicholas_of_Greece_and_Denmark
    source: :Grand_Duchess_Elena_Vladimirovna_of_Russia
  AddLiteral (9aa4aa07-2e3e-4f39-968e-7354b61a9f98)
 Call ID: 9aa4aa07-2e3e-4f39-968e-7354b61a9f98
  Args:
    source: :Grand_Duchess_Elena_Vladimirovna_of_Russia
    relation: :hasMarriageYear
    literal_type: xsd:integer
    literal_value: 1902
  AssignClass (e7baaca1-e5de-4c60-ac2f-7704def5032e)
 Call ID: e7baaca1-e5de-4c60-ac2f-7704def5032e
  Args:
    type: :Man
    source: :Kirill
  AssignClass (68bdd287-125a-4c04-9e3b-7dfd3bfc410c)
 Call ID: 68bdd287-125a-4c04-9e3b-7dfd3bfc410c
  Args:
    source: :Kirill
    type: :Person
  AssignClass (4f1c74d5-dc5f-42d8-8a0a-3c80778bdad6)
 Call ID: 4f1c74d5-dc5f-42d8-8a0a-3c80778bdad6
  Args:
    type: :Man
    source: :Boris
  AssignClass (0c35828c-d330-4de0-9383-f3fb7d507f65)
 Call ID: 0c35828c-d330-4de0-9383-f3fb7d507f65
  Args:
    source: :Boris
    type: :Person
  AssignClass (96073b21-5f8e-47ab-ae47-eb34aa49f5fa)
 Call ID: 96073b21-5f8e-47ab-ae47-eb34aa49f5fa
  Args:
    source: :Andrei
    type: :Man
  AssignClass (888c485f-e4c2-4c76-b230-855bef7e5ef6)
 Call ID: 888c485f-e4c2-4c76-b230-855bef7e5ef6
  Args:
    source: :Andrei
    type: :Person
  AddTriple (87b496fe-a1e0-41e1-9829-2237eada8961)
 Call ID: 87b496fe-a1e0-41e1-9829-2237eada8961
  Args:
    relation: :hasBrother
    target: :Kirill
    source: :Grand_Duchess_Elena_Vladimirovna_of_Russia
  AddTriple (01051c94-a948-4be5-ba44-53603c9f606a)
 Call ID: 01051c94-a948-4be5-ba44-53603c9f606a
  Args:
    target: :Boris
    source: :Grand_Duchess_Elena_Vladimirovna_of_Russia
    relation: :hasBrother
  AddTriple (be0a62bb-1a3e-4d7c-8040-bf9e19c037e0)
 Call ID: be0a62bb-1a3e-4d7c-8040-bf9e19c037e0
  Args:
    target: :Andrei
    source: :Grand_Duchess_Elena_Vladimirovna_of_Russia
    relation: :hasBrother
  AssignClass (420afd3d-b719-4925-b189-ba68649dc497)
 Call ID: 420afd3d-b719-4925-b189-ba68649dc497
  Args:
    source: :Princess_Olga_of_Greece
    type: :Woman
  AssignClass (925a9c42-8137-49d7-8923-69d9d6ea25aa)
 Call ID: 925a9c42-8137-49d7-8923-69d9d6ea25aa
  Args:
    source: :Princess_Olga_of_Greece
    type: :Person
  AssignClass (ac754a1a-7dbc-44df-b3b6-a3909e0b60d8)
 Call ID: ac754a1a-7dbc-44df-b3b6-a3909e0b60d8
  Args:
    type: :Woman
    source: :Princess_Elizabeth_of_Greece
  AssignClass (acc162a0-e4c8-41f4-94e9-4847be9d3057)
 Call ID: acc162a0-e4c8-41f4-94e9-4847be9d3057
  Args:
    type: :Person
    source: :Princess_Elizabeth_of_Greece
  AssignClass (2ff244c1-4227-49fe-a957-065b0cab1b12)
 Call ID: 2ff244c1-4227-49fe-a957-065b0cab1b12
  Args:
    source: :Princess_Marina_of_Greece
    type: :Woman
  AssignClass (7bff6c3d-94bf-4179-993c-eece5afaee30)
 Call ID: 7bff6c3d-94bf-4179-993c-eece5afaee30
  Args:
    source: :Princess_Marina_of_Greece
    type: :Person
  AddTriple (d2e0ef08-42ef-4c37-a2df-7e94b5d6e507)
 Call ID: d2e0ef08-42ef-4c37-a2df-7e94b5d6e507
  Args:
    target: :Princess_Olga_of_Greece
    source: :Grand_Duchess_Elena_Vladimirovna_of_Russia
    relation: :hasDaughter
  AddTriple (8ac75d72-7655-4755-9816-e4dea43dbba0)
 Call ID: 8ac75d72-7655-4755-9816-e4dea43dbba0
  Args:
    target: :Princess_Olga_of_Greece
    source: :Prince_Nicholas_of_Greece_and_Denmark
    relation: :hasDaughter
  AddTriple (1815fc74-5f14-4c0b-98e1-c904543eb821)
 Call ID: 1815fc74-5f14-4c0b-98e1-c904543eb821
  Args:
    target: :Princess_Elizabeth_of_Greece
    source: :Grand_Duchess_Elena_Vladimirovna_of_Russia
    relation: :hasDaughter
  AddTriple (81896a86-94a4-4da8-9b50-a3b3eabbff5b)
 Call ID: 81896a86-94a4-4da8-9b50-a3b3eabbff5b
  Args:
    target: :Princess_Elizabeth_of_Greece
    source: :Prince_Nicholas_of_Greece_and_Denmark
    relation: :hasDaughter
  AddTriple (2c3ec24c-b59c-491d-a5d1-0893925fec6e)
 Call ID: 2c3ec24c-b59c-491d-a5d1-0893925fec6e
  Args:
    source: :Grand_Duchess_Elena_Vladimirovna_of_Russia
    target: :Princess_Marina_of_Greece
    relation: :hasDaughter
  AddTriple (55aebdcd-cab3-45be-90f9-e680616ac54d)
 Call ID: 55aebdcd-cab3-45be-90f9-e680616ac54d
  Args:
    relation: :hasDaughter
    source: :Prince_Nicholas_of_Greece_and_Denmark
    target: :Princess_Marina_of_Greece
  Finish (08f9a744-18ed-4ceb-a497-7643bc5ecb3d)
 Call ID: 08f9a744-18ed-4ceb-a497-7643bc5ecb3d
  Args: