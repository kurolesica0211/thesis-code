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
Princess Tatiana Maria Renata Eugenia Elisabeth Margarete Radziwiłł (28 August 1939 – 19 December 2025) was a French-Polish aristocrat, bacteriologist and nurse.
The eldest daughter of Prince Dominik Rainer Radziwiłł and Princess Eugénie of Greece and Denmark, she was a member of the House of Radziwiłł and a close relative to the Greek, Romanian, Spanish,  Danish, British, and Serbian royal families and the former imperial families of Austria, France, and Russia.
Radziwiłł served as a bridesmaid at the Wedding of Prince Juan Carlos of Spain and Princess Sophia of Greece and Denmark in 1962 and at the wedding of Constantine II of Greece and Princess Anne-Marie of Denmark in 1964.
Early life and family

Radziwiłł was born in Rouen, Normandy on 28 August 1939 to Prince Dominik Rainer Radziwiłł, an officer in the Polish Army, and Princess Eugénie of Greece and Denmark, a member of the Greek royal family.
By birth, she was a member of the House of Radziwill, one of the wealthiest and most important Polish-Lithuanian magnate families, and was the granddaughter of Prince Hieronim Mikołaj Radziwiłł and Archduchess Renata of Austria.
Her maternal grandparents were Prince George of Greece and Denmark, second son of George I of Greece and Olga Constantinovna of Russia, and Princess Marie Bonaparte, daughter of Roland Napoléon Bonaparte, 6th Prince of Canino and Musignano and Marie-Félix Blanc.
Radziwiłł's parents divorced in 1946.
Her father remarried in 1947 to Lida Lacey Bloodgood, daughter of Lida Fleitmann Bloodgood, and her mother remarried in 1949 to Prince Raimondo della Torre e Tasso, Duke of Castel Duino.
Radziwiłł and her parents fled their home in 1940 after the Fall of France, taking refuge in Saint-Tropez before going in to exile in South Africa, then part of the British Empire.
They were later joined by her grandparents, Prince George of Greece and Denmark and Princess Marie Bonaparte, as well as other members of the Greek royal family, including Crown Princess Frederika and her children.
Throughout her childhood, Radziwiłł became close friend with her second cousin, Princess Sophia of Greece and Denmark (the future Queen of Spain).
She also spent a lot of her childhood with her maternal grandmother, Princess Marie, who was a psychoanalyst and authored Le Livre de Tatiana shortly after Tatiana's birth.
Radziwiłł returned to France in 1945 following the end of the war, just three years after the birth of her brother, Prince George.
She was educated in schools in France and in Greece, studying music and languages.
She took part in the ship tour organized by Queen Frederica and her husband King Paul of Greece in 1954, which became known as the “Cruise of the Kings” and was attended by over 100 royals from all over Europe.
Public life and royal duties

As a relative of many reigning royal families in Europe, Radziwiłł attended various events across the continent including the Coronation of Elizabeth II in 1953 and the Royal Cruise Agamemnon in 1954.
As a young woman, Radziwiłł was considered as a potential wife for the future Harald V of Norway.
In 1956, she was part of the official entourage at a reception for King Paul of Greece in Bois de Boulogne and at the Hôtel de Ville, Paris.
She remained close to the Greek royal family, serving as a bridesmaid for her cousin, Princess Sophia, when she married the future King of Spain in 1962.
Radziwiłł  served alongside Princess Irene of Greece and Denmark, Princess Irene of the Netherlands, Princess Alexandra of Kent, Princess Anne d'Orléans, Infanta Pilar of Spain, Princess Anne-Marie of Denmark, and Princess Benedikte of Denmark.
In March 1963, Tatiana Radziwiłł attended the festivities celebrating the 100th Anniversary of the Greek Monarchy.
She was present at the doxology service, a parade, and a gala performance at the National Theatre of Greece.
In August 1963, she accompanied the Crown Prince of Greece while he hosted the 11th World Scout Jamboree.
In 1964, she served as a bridesmaid in the wedding of her cousins, Constantine II of Greece and Princess Anne-Marie of Denmark.
In 2021, she attended the wedding of Prince Philippos of Greece and Denmark and Nina Flohr.
In 2024, she attended the wedding of Princess Theodora of Greece and Denmark and Matthew Kumar.
Personal life and death

While studying nursing and bacteriology at the University of Paris, Radziwiłł met a French cardiologist, Dr. Jean Henri Fruchard, the son of Colonel Dr. Henri Fruchard and his second wife, Eunice McCooey.
Their wedding was attended by members of the Greek and Danish royal families, including King Constantine II of Greece, Queen Anne-Marie of Greece, Dowager Queen Frederica of Greece, Queen Ingrid of Denmark, Princess Alice of Greece, Princess Irene of Greece, and Princess Sophia of Greece.
Radziwiłł and Fruchaud had two children, Fabiola (born 1967) and Alexis (born 1969).
A close friend and second cousin of Queen Sofía of Spain, Radziwiłł accompanied the Queen on international trips and attended events at Zarzuela Palace and Marivent Palace.
Radziwiłł died on 19 December 2025 in Paris, at the age of 86.
Her funeral took place on 10 January 2026 at Saint-Thomas-d'Aquin, Paris and was attended by members of the Spanish and Greek royal families and their relatives, including King Felipe VI and Queen Sofia of Spain as well as Queen Anne-Marie and Crown Prince Pavlos of Greece.
Popular culture

Radziwiłł is portrayed by Paloma Bloyd in Antonio Hernández's 2011 Spanish television film directed Sofía.
She was also portrayed in Benoît Jacquot's 2004 television film Princesse Marie.
In his 2013 book, La récréation, Frédéric Mitterrand writes about attending an exhibition on Princess Marie Bonaparte with Radziwiłł.



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
  AssignClass (f072660b-6298-435f-88f1-b70ddf98c1b7)
 Call ID: f072660b-6298-435f-88f1-b70ddf98c1b7
  Args:
    source: :TatianaRadziwill
    type: :Woman
  AssignClass (0edd03c3-ae64-4547-9390-a6dc723a9552)
 Call ID: 0edd03c3-ae64-4547-9390-a6dc723a9552
  Args:
    source: :TatianaRadziwill
    type: :Person
  AddLiteral (36463b78-ec0e-46fa-8f2e-6e9367c29864)
 Call ID: 36463b78-ec0e-46fa-8f2e-6e9367c29864
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: :TatianaRadziwill
    literal_value: 1939
  AddLiteral (d952c033-4fc7-45b2-a393-f1460fb40bf5)
 Call ID: d952c033-4fc7-45b2-a393-f1460fb40bf5
  Args:
    literal_value: 2025
    literal_type: xsd:integer
    source: :TatianaRadziwill
    relation: :hasDeathYear
  AssignClass (ba93be13-6bd0-416a-a25a-3f2f21b1e2a1)
 Call ID: ba93be13-6bd0-416a-a25a-3f2f21b1e2a1
  Args:
    source: :DominikRainerRadziwill
    type: :Man
  AssignClass (58951858-2a07-4249-9dcd-9ee75f61bc13)
 Call ID: 58951858-2a07-4249-9dcd-9ee75f61bc13
  Args:
    type: :Person
    source: :DominikRainerRadziwill
  AssignClass (1491d589-aab3-4e16-833d-b49597f0c439)
 Call ID: 1491d589-aab3-4e16-833d-b49597f0c439
  Args:
    source: :EugenieOfGreeceAndDenmark
    type: :Woman
  AssignClass (27378592-23e4-417a-85a0-c5c0bca4c5ee)
 Call ID: 27378592-23e4-417a-85a0-c5c0bca4c5ee
  Args:
    type: :Person
    source: :EugenieOfGreeceAndDenmark
  AddTriple (bf37f5f1-eb78-437e-96d4-b558310cdef5)
 Call ID: bf37f5f1-eb78-437e-96d4-b558310cdef5
  Args:
    source: :TatianaRadziwill
    relation: :hasFather
    target: :DominikRainerRadziwill
  AddTriple (9b945db8-2d71-4049-b734-74a93028ed38)
 Call ID: 9b945db8-2d71-4049-b734-74a93028ed38
  Args:
    target: :EugenieOfGreeceAndDenmark
    relation: :hasMother
    source: :TatianaRadziwill
  AssignClass (98d24b77-abbc-4854-af9b-3d584d4815ac)
 Call ID: 98d24b77-abbc-4854-af9b-3d584d4815ac
  Args:
    source: :HieronimMikolajRadziwill
    type: :Man
  AssignClass (7dfe3641-2edd-4acd-a952-5ec492e781f8)
 Call ID: 7dfe3641-2edd-4acd-a952-5ec492e781f8
  Args:
    type: :Person
    source: :HieronimMikolajRadziwill
  AssignClass (7a868cdb-3dae-4d1e-992f-6ed1df903587)
 Call ID: 7a868cdb-3dae-4d1e-992f-6ed1df903587
  Args:
    type: :Woman
    source: :RenataOfAustria
  AssignClass (96028141-f0f2-48e2-a626-a4b493e620c0)
 Call ID: 96028141-f0f2-48e2-a626-a4b493e620c0
  Args:
    type: :Person
    source: :RenataOfAustria
  AddTriple (d469a8ca-f832-47ac-881e-da425eb40789)
 Call ID: d469a8ca-f832-47ac-881e-da425eb40789
  Args:
    target: :HieronimMikolajRadziwill
    source: :DominikRainerRadziwill
    relation: :hasFather
  AddTriple (bb7a2ed7-9448-4987-ab90-a4a3ba26cb82)
 Call ID: bb7a2ed7-9448-4987-ab90-a4a3ba26cb82
  Args:
    target: :RenataOfAustria
    source: :DominikRainerRadziwill
    relation: :hasMother
  AssignClass (35bf3460-154e-4ab5-90e7-92f43eea3009)
 Call ID: 35bf3460-154e-4ab5-90e7-92f43eea3009
  Args:
    type: :Man
    source: :GeorgeOfGreeceAndDenmark
  AssignClass (cd9e2b78-7725-4719-9186-20cf752b8b73)
 Call ID: cd9e2b78-7725-4719-9186-20cf752b8b73
  Args:
    type: :Person
    source: :GeorgeOfGreeceAndDenmark
  AssignClass (15c8b576-46d7-45da-86b7-e30b66c6c738)
 Call ID: 15c8b576-46d7-45da-86b7-e30b66c6c738
  Args:
    type: :Woman
    source: :MarieBonaparte
  AssignClass (72d8d3a8-0b2b-4977-a10f-25045181cb9b)
 Call ID: 72d8d3a8-0b2b-4977-a10f-25045181cb9b
  Args:
    type: :Person
    source: :MarieBonaparte
  AddTriple (4ccf54e9-57af-41c5-9c15-91c1c799c86a)
 Call ID: 4ccf54e9-57af-41c5-9c15-91c1c799c86a
  Args:
    source: :EugenieOfGreeceAndDenmark
    relation: :hasFather
    target: :GeorgeOfGreeceAndDenmark
  AddTriple (7c9cb8e0-8465-45d9-9297-96d50f9ba279)
 Call ID: 7c9cb8e0-8465-45d9-9297-96d50f9ba279
  Args:
    source: :EugenieOfGreeceAndDenmark
    relation: :hasMother
    target: :MarieBonaparte
  AssignClass (a551a88b-a573-4d3f-84bd-15de9a26ad05)
 Call ID: a551a88b-a573-4d3f-84bd-15de9a26ad05
  Args:
    source: :GeorgeOfGreece
    type: :Man
  AssignClass (429d2562-6e72-45b7-8ca2-ef39178e911c)
 Call ID: 429d2562-6e72-45b7-8ca2-ef39178e911c
  Args:
    source: :GeorgeOfGreece
    type: :Person
  AssignClass (797563e8-0075-45e3-a002-ec5da9c0789d)
 Call ID: 797563e8-0075-45e3-a002-ec5da9c0789d
  Args:
    type: :Woman
    source: :OlgaConstantinovnaOfRussia
  AssignClass (0936cba8-d00a-42a2-b7ac-f0888aa95f9a)
 Call ID: 0936cba8-d00a-42a2-b7ac-f0888aa95f9a
  Args:
    type: :Person
    source: :OlgaConstantinovnaOfRussia
  AddTriple (b3f2832f-91bd-4622-950b-c86d4d25d081)
 Call ID: b3f2832f-91bd-4622-950b-c86d4d25d081
  Args:
    target: :GeorgeOfGreece
    relation: :hasFather
    source: :GeorgeOfGreeceAndDenmark
  AddTriple (83c5a76d-1e0a-4c98-bb98-1357e6a395b5)
 Call ID: 83c5a76d-1e0a-4c98-bb98-1357e6a395b5
  Args:
    target: :OlgaConstantinovnaOfRussia
    source: :GeorgeOfGreeceAndDenmark
    relation: :hasMother
  AssignClass (218f34c8-7c77-44fb-afc5-eb4f8450c2a6)
 Call ID: 218f34c8-7c77-44fb-afc5-eb4f8450c2a6
  Args:
    source: :RolandNapoleonBonaparte
    type: :Man
  AssignClass (6837c853-b91a-47bd-ba56-2539ff4a4ac2)
 Call ID: 6837c853-b91a-47bd-ba56-2539ff4a4ac2
  Args:
    source: :RolandNapoleonBonaparte
    type: :Person
  AssignClass (c0c3f9a0-3de0-4570-b8c8-5971a3e0221d)
 Call ID: c0c3f9a0-3de0-4570-b8c8-5971a3e0221d
  Args:
    source: :MarieFelixBlanc
    type: :Woman
  AssignClass (78f0406d-a8f8-40b4-a807-5310147e9f4e)
 Call ID: 78f0406d-a8f8-40b4-a807-5310147e9f4e
  Args:
    source: :MarieFelixBlanc
    type: :Person
  AddTriple (e896464c-cfb7-44ce-b8fc-d15d43582b0c)
 Call ID: e896464c-cfb7-44ce-b8fc-d15d43582b0c
  Args:
    source: :MarieBonaparte
    relation: :hasFather
    target: :RolandNapoleonBonaparte
  AddTriple (72982ab7-3b4e-4e97-88f0-007208b53026)
 Call ID: 72982ab7-3b4e-4e97-88f0-007208b53026
  Args:
    target: :MarieFelixBlanc
    relation: :hasMother
    source: :MarieBonaparte
  AssignClass (6ed21a5c-4db2-4e8b-85cc-832562c37613)
 Call ID: 6ed21a5c-4db2-4e8b-85cc-832562c37613
  Args:
    type: :Man
    source: :GeorgeRadziwill
  AssignClass (b5f10125-649a-48eb-904d-00ad7e327f5d)
 Call ID: b5f10125-649a-48eb-904d-00ad7e327f5d
  Args:
    type: :Person
    source: :GeorgeRadziwill
  AddTriple (070593eb-ca91-4e9f-a459-c63c3a5e90fe)
 Call ID: 070593eb-ca91-4e9f-a459-c63c3a5e90fe
  Args:
    target: :DominikRainerRadziwill
    relation: :hasFather
    source: :GeorgeRadziwill
  AddTriple (76758933-b804-4da9-b957-7c23b8278202)
 Call ID: 76758933-b804-4da9-b957-7c23b8278202
  Args:
    target: :EugenieOfGreeceAndDenmark
    relation: :hasMother
    source: :GeorgeRadziwill
  AssignClass (d8ffabfe-9f05-48cf-a49e-b4e30f92678c)
 Call ID: d8ffabfe-9f05-48cf-a49e-b4e30f92678c
  Args:
    type: :Man
    source: :JeanHenriFruchaud
  AssignClass (dde461ff-5a43-45b8-a0db-0964814b918f)
 Call ID: dde461ff-5a43-45b8-a0db-0964814b918f
  Args:
    type: :Person
    source: :JeanHenriFruchaud
  AssignClass (d1bd17c2-ac59-4b75-97b1-6a4b41741d64)
 Call ID: d1bd17c2-ac59-4b75-97b1-6a4b41741d64
  Args:
    type: :Man
    source: :HenriFruchaud
  AssignClass (f7ee0742-3b97-4cee-931a-ba329bae0792)
 Call ID: f7ee0742-3b97-4cee-931a-ba329bae0792
  Args:
    type: :Person
    source: :HenriFruchaud
  AssignClass (a44994ec-ae98-4eab-9be7-ab06958172bc)
 Call ID: a44994ec-ae98-4eab-9be7-ab06958172bc
  Args:
    source: :EuniceMcCooey
    type: :Woman
  AssignClass (cf104a39-1eb0-4c61-b406-520de39a9d86)
 Call ID: cf104a39-1eb0-4c61-b406-520de39a9d86
  Args:
    type: :Person
    source: :EuniceMcCooey
  AddTriple (54fdf041-c675-4b2c-be7d-04f1fa8fa482)
 Call ID: 54fdf041-c675-4b2c-be7d-04f1fa8fa482
  Args:
    target: :HenriFruchaud
    relation: :hasFather
    source: :JeanHenriFruchaud
  AddTriple (783adf92-07e5-4e64-9dc8-1e6d9ef1cb2b)
 Call ID: 783adf92-07e5-4e64-9dc8-1e6d9ef1cb2b
  Args:
    source: :JeanHenriFruchaud
    relation: :hasMother
    target: :EuniceMcCooey
  AssignClass (220a4607-eb10-4db4-9052-c7c59e638b88)
 Call ID: 220a4607-eb10-4db4-9052-c7c59e638b88
  Args:
    source: :FabiolaFruchaud
    type: :Woman
  AssignClass (669ff831-3565-47da-a05c-4a6b49cd4b29)
 Call ID: 669ff831-3565-47da-a05c-4a6b49cd4b29
  Args:
    type: :Person
    source: :FabiolaFruchaud
  AddLiteral (1e459702-8816-4608-a326-e03b8dca8d50)
 Call ID: 1e459702-8816-4608-a326-e03b8dca8d50
  Args:
    literal_value: 1967
    literal_type: xsd:integer
    source: :FabiolaFruchaud
    relation: :hasBirthYear
  AddTriple (722612e6-3c89-4c13-87bc-704cbc2eaaf5)
 Call ID: 722612e6-3c89-4c13-87bc-704cbc2eaaf5
  Args:
    relation: :hasFather
    source: :FabiolaFruchaud
    target: :JeanHenriFruchaud
  AddTriple (76e32879-3293-4c59-b4e5-8140d4ae114a)
 Call ID: 76e32879-3293-4c59-b4e5-8140d4ae114a
  Args:
    relation: :hasMother
    source: :FabiolaFruchaud
    target: :TatianaRadziwill
  AssignClass (8b762412-e7d0-44ac-b2f0-9810ed5ce781)
 Call ID: 8b762412-e7d0-44ac-b2f0-9810ed5ce781
  Args:
    type: :Man
    source: :AlexisFruchaud
  AssignClass (115c7516-16f7-442c-9586-818605237cf7)
 Call ID: 115c7516-16f7-442c-9586-818605237cf7
  Args:
    type: :Person
    source: :AlexisFruchaud
  AddLiteral (b9672b59-1165-4887-b4cc-31bd0a86f3d9)
 Call ID: b9672b59-1165-4887-b4cc-31bd0a86f3d9
  Args:
    literal_value: 1969
    relation: :hasBirthYear
    source: :AlexisFruchaud
    literal_type: xsd:integer
  AddTriple (45bf4d9a-3ee3-4e34-8eba-7132aa3e2b8b)
 Call ID: 45bf4d9a-3ee3-4e34-8eba-7132aa3e2b8b
  Args:
    target: :JeanHenriFruchaud
    source: :AlexisFruchaud
    relation: :hasFather
  AddTriple (b34d44a0-1555-47ef-aa5d-514cc8fe4c67)
 Call ID: b34d44a0-1555-47ef-aa5d-514cc8fe4c67
  Args:
    source: :AlexisFruchaud
    relation: :hasMother
    target: :TatianaRadziwill
  Finish (172703c1-0656-4c4f-8922-2714af8b0081)
 Call ID: 172703c1-0656-4c4f-8922-2714af8b0081
  Args: