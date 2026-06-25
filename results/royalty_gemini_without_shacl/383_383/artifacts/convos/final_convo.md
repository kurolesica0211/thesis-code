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
  AssignClass (2c51da11-3e23-4c2e-a30b-be5ac014b7be)
 Call ID: 2c51da11-3e23-4c2e-a30b-be5ac014b7be
  Args:
    type: :Woman
    source: Tatiana_Radziwill
  AssignClass (33bda156-cb50-4066-aa01-08f51173e4dd)
 Call ID: 33bda156-cb50-4066-aa01-08f51173e4dd
  Args:
    type: :Person
    source: Tatiana_Radziwill
  AddLiteral (45f15225-74ae-43f2-942a-eb5ce40ed4ef)
 Call ID: 45f15225-74ae-43f2-942a-eb5ce40ed4ef
  Args:
    source: Tatiana_Radziwill
    literal_value: 1939
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (180897b1-1138-4b10-90c0-44061e2721f7)
 Call ID: 180897b1-1138-4b10-90c0-44061e2721f7
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 2025
    source: Tatiana_Radziwill
  AssignClass (b70908aa-cae5-4b35-8095-cbdfaaa1b223)
 Call ID: b70908aa-cae5-4b35-8095-cbdfaaa1b223
  Args:
    source: Dominik_Rainer_Radziwill
    type: :Man
  AssignClass (8d07c7a7-4ceb-4887-ac20-9177c3819ce7)
 Call ID: 8d07c7a7-4ceb-4887-ac20-9177c3819ce7
  Args:
    type: :Person
    source: Dominik_Rainer_Radziwill
  AssignClass (312c6b36-a133-4ef1-8466-e14213e64503)
 Call ID: 312c6b36-a133-4ef1-8466-e14213e64503
  Args:
    type: :Woman
    source: Eugenie_of_Greece_and_Denmark
  AssignClass (9c3ea024-8aa9-4fda-a889-5498f9f7740e)
 Call ID: 9c3ea024-8aa9-4fda-a889-5498f9f7740e
  Args:
    type: :Person
    source: Eugenie_of_Greece_and_Denmark
  AddTriple (2e97b295-342d-4171-934a-0ec78c2a44a4)
 Call ID: 2e97b295-342d-4171-934a-0ec78c2a44a4
  Args:
    source: Tatiana_Radziwill
    relation: :hasFather
    target: Dominik_Rainer_Radziwill
  AddTriple (5826feeb-8f88-4411-9576-c204df87174c)
 Call ID: 5826feeb-8f88-4411-9576-c204df87174c
  Args:
    relation: :hasMother
    target: Eugenie_of_Greece_and_Denmark
    source: Tatiana_Radziwill
  AssignClass (f31f3d78-68ec-4543-8d46-791c3734dfd9)
 Call ID: f31f3d78-68ec-4543-8d46-791c3734dfd9
  Args:
    source: Hieronim_Mikolaj_Radziwill
    type: :Man
  AssignClass (acb12493-e712-4e6c-bd54-7ecb90537fed)
 Call ID: acb12493-e712-4e6c-bd54-7ecb90537fed
  Args:
    source: Hieronim_Mikolaj_Radziwill
    type: :Person
  AssignClass (4e28e69a-1440-4f36-bc3c-774402a8845a)
 Call ID: 4e28e69a-1440-4f36-bc3c-774402a8845a
  Args:
    source: Renata_of_Austria
    type: :Woman
  AssignClass (426c14a3-b990-45b1-a785-d1f725d4c74c)
 Call ID: 426c14a3-b990-45b1-a785-d1f725d4c74c
  Args:
    type: :Person
    source: Renata_of_Austria
  AddTriple (532397f4-9c5d-4635-8859-a89c7166432a)
 Call ID: 532397f4-9c5d-4635-8859-a89c7166432a
  Args:
    relation: :hasFather
    target: Hieronim_Mikolaj_Radziwill
    source: Dominik_Rainer_Radziwill
  AddTriple (50cbadf6-0140-4c6f-9686-07c9d5d67f7c)
 Call ID: 50cbadf6-0140-4c6f-9686-07c9d5d67f7c
  Args:
    target: Renata_of_Austria
    relation: :hasMother
    source: Dominik_Rainer_Radziwill
  AssignClass (84caa440-cce7-47f5-bc3a-4126a02f86d5)
 Call ID: 84caa440-cce7-47f5-bc3a-4126a02f86d5
  Args:
    type: :Man
    source: George_of_Greece_and_Denmark
  AssignClass (26e11e71-aceb-4b4a-85d0-2160b54b8a77)
 Call ID: 26e11e71-aceb-4b4a-85d0-2160b54b8a77
  Args:
    source: George_of_Greece_and_Denmark
    type: :Person
  AssignClass (347a1221-7a05-4eb8-ba5c-787c89fab863)
 Call ID: 347a1221-7a05-4eb8-ba5c-787c89fab863
  Args:
    source: Marie_Bonaparte
    type: :Woman
  AssignClass (28298e87-7125-4f9e-899d-182b714e5b95)
 Call ID: 28298e87-7125-4f9e-899d-182b714e5b95
  Args:
    type: :Person
    source: Marie_Bonaparte
  AddTriple (6e3223be-ec4e-4f48-8259-9e5843c4eef9)
 Call ID: 6e3223be-ec4e-4f48-8259-9e5843c4eef9
  Args:
    source: Eugenie_of_Greece_and_Denmark
    relation: :hasFather
    target: George_of_Greece_and_Denmark
  AddTriple (27ca96e7-0ccf-4224-b69c-46d0ad9242d7)
 Call ID: 27ca96e7-0ccf-4224-b69c-46d0ad9242d7
  Args:
    target: Marie_Bonaparte
    relation: :hasMother
    source: Eugenie_of_Greece_and_Denmark
  AssignClass (5b004697-fdd1-4736-a529-8bb64afd151a)
 Call ID: 5b004697-fdd1-4736-a529-8bb64afd151a
  Args:
    type: :Man
    source: George_I_of_Greece
  AssignClass (8b0b27a3-abc5-480b-b9be-455a0d7926bf)
 Call ID: 8b0b27a3-abc5-480b-b9be-455a0d7926bf
  Args:
    source: George_I_of_Greece
    type: :Person
  AssignClass (81b24bd7-88f8-4e46-acfe-cb800f834d6f)
 Call ID: 81b24bd7-88f8-4e46-acfe-cb800f834d6f
  Args:
    type: :Woman
    source: Olga_Constantinovna_of_Russia
  AssignClass (08ee701a-f0f9-4690-8c35-62dd96628f28)
 Call ID: 08ee701a-f0f9-4690-8c35-62dd96628f28
  Args:
    type: :Person
    source: Olga_Constantinovna_of_Russia
  AddTriple (d6ec8e40-2447-42fe-b46d-6fecb864b0f2)
 Call ID: d6ec8e40-2447-42fe-b46d-6fecb864b0f2
  Args:
    source: George_of_Greece_and_Denmark
    target: George_I_of_Greece
    relation: :hasFather
  AddTriple (6bf286ad-e941-417a-974f-2138c3ad094f)
 Call ID: 6bf286ad-e941-417a-974f-2138c3ad094f
  Args:
    source: George_of_Greece_and_Denmark
    relation: :hasMother
    target: Olga_Constantinovna_of_Russia
  AssignClass (c6a3914e-c839-49b1-bc08-95fbd62ac80b)
 Call ID: c6a3914e-c839-49b1-bc08-95fbd62ac80b
  Args:
    source: Roland_Napoleon_Bonaparte
    type: :Man
  AssignClass (a81ca5d9-e3aa-4570-a182-46a494ff0f19)
 Call ID: a81ca5d9-e3aa-4570-a182-46a494ff0f19
  Args:
    source: Roland_Napoleon_Bonaparte
    type: :Person
  AssignClass (97e3f8c9-bf48-4c78-b40d-95f19d652b9f)
 Call ID: 97e3f8c9-bf48-4c78-b40d-95f19d652b9f
  Args:
    type: :Woman
    source: Marie_Felix_Blanc
  AssignClass (e78e56fd-a8ca-4946-b5c3-4e7512e4f88d)
 Call ID: e78e56fd-a8ca-4946-b5c3-4e7512e4f88d
  Args:
    source: Marie_Felix_Blanc
    type: :Person
  AddTriple (c68ae5a7-d5d6-4826-820c-d4109c960585)
 Call ID: c68ae5a7-d5d6-4826-820c-d4109c960585
  Args:
    relation: :hasFather
    target: Roland_Napoleon_Bonaparte
    source: Marie_Bonaparte
  AddTriple (69d66a62-527a-4f29-b519-5054118febba)
 Call ID: 69d66a62-527a-4f29-b519-5054118febba
  Args:
    source: Marie_Bonaparte
    relation: :hasMother
    target: Marie_Felix_Blanc
  AssignClass (c7d9f2cf-6a82-4c8d-9a10-eb5fe2275279)
 Call ID: c7d9f2cf-6a82-4c8d-9a10-eb5fe2275279
  Args:
    source: George_Radziwill
    type: :Man
  AssignClass (7aa5e90d-d02d-4f81-843d-50f2e5892aac)
 Call ID: 7aa5e90d-d02d-4f81-843d-50f2e5892aac
  Args:
    source: George_Radziwill
    type: :Person
  AddTriple (1427d34d-510e-4e35-ba4b-5bd1aee41a8c)
 Call ID: 1427d34d-510e-4e35-ba4b-5bd1aee41a8c
  Args:
    target: George_Radziwill
    relation: :hasBrother
    source: Tatiana_Radziwill
  AssignClass (4c225819-6a16-439b-949a-98ea08192a42)
 Call ID: 4c225819-6a16-439b-949a-98ea08192a42
  Args:
    type: :Man
    source: Jean_Henri_Fruchaud
  AssignClass (e44f7a8d-89e1-4a3b-b80c-c4860c2bc440)
 Call ID: e44f7a8d-89e1-4a3b-b80c-c4860c2bc440
  Args:
    source: Jean_Henri_Fruchaud
    type: :Person
  AssignClass (c05c6cb5-0d9b-4527-b70c-0c653dd5684d)
 Call ID: c05c6cb5-0d9b-4527-b70c-0c653dd5684d
  Args:
    type: :Man
    source: Henri_Fruchaud
  AssignClass (a4f5bafb-0693-47c6-a2f1-5f241929a175)
 Call ID: a4f5bafb-0693-47c6-a2f1-5f241929a175
  Args:
    type: :Person
    source: Henri_Fruchaud
  AssignClass (351a3e57-5c39-4fe0-ad73-3fa2f6af784e)
 Call ID: 351a3e57-5c39-4fe0-ad73-3fa2f6af784e
  Args:
    type: :Woman
    source: Eunice_McCooey
  AssignClass (c34a4ed1-6c2a-4381-a93c-5160fa362d0f)
 Call ID: c34a4ed1-6c2a-4381-a93c-5160fa362d0f
  Args:
    source: Eunice_McCooey
    type: :Person
  AddTriple (b334d3fb-4eb9-4b1c-b07d-a6583eb4cd45)
 Call ID: b334d3fb-4eb9-4b1c-b07d-a6583eb4cd45
  Args:
    source: Jean_Henri_Fruchaud
    relation: :hasFather
    target: Henri_Fruchaud
  AddTriple (446edf40-4eac-435f-99be-ab6f3530ea16)
 Call ID: 446edf40-4eac-435f-99be-ab6f3530ea16
  Args:
    target: Eunice_McCooey
    relation: :hasMother
    source: Jean_Henri_Fruchaud
  AssignClass (278e342c-dc1c-4d7a-a143-f3ca249ca745)
 Call ID: 278e342c-dc1c-4d7a-a143-f3ca249ca745
  Args:
    type: :Woman
    source: Fabiola_Fruchaud
  AssignClass (dc97d924-6fd1-48a9-97f7-9bbb2f8d2857)
 Call ID: dc97d924-6fd1-48a9-97f7-9bbb2f8d2857
  Args:
    type: :Person
    source: Fabiola_Fruchaud
  AssignClass (448a97a8-cd59-47c0-8cfd-a74c7f2fe9b6)
 Call ID: 448a97a8-cd59-47c0-8cfd-a74c7f2fe9b6
  Args:
    source: Alexis_Fruchaud
    type: :Man
  AssignClass (41f22818-fed7-483c-9b3f-d41fce6adc61)
 Call ID: 41f22818-fed7-483c-9b3f-d41fce6adc61
  Args:
    type: :Person
    source: Alexis_Fruchaud
  AddTriple (9efe9f3a-5be5-4186-8ca4-3157ef88d314)
 Call ID: 9efe9f3a-5be5-4186-8ca4-3157ef88d314
  Args:
    target: Tatiana_Radziwill
    relation: :hasMother
    source: Fabiola_Fruchaud
  AddTriple (305316c9-a4d2-410f-91bb-32d0d8bb8ed8)
 Call ID: 305316c9-a4d2-410f-91bb-32d0d8bb8ed8
  Args:
    relation: :hasFather
    target: Jean_Henri_Fruchaud
    source: Fabiola_Fruchaud
  AddTriple (ff5945d8-ace7-4c10-b4ab-7fe7260bd6b5)
 Call ID: ff5945d8-ace7-4c10-b4ab-7fe7260bd6b5
  Args:
    source: Alexis_Fruchaud
    target: Tatiana_Radziwill
    relation: :hasMother
  AddTriple (4f3553cd-d571-43c5-8d68-b6ba44992f9d)
 Call ID: 4f3553cd-d571-43c5-8d68-b6ba44992f9d
  Args:
    source: Alexis_Fruchaud
    target: Jean_Henri_Fruchaud
    relation: :hasFather
  AssignClass (243d4a17-8b34-428f-b1e5-ddf4e247ff60)
 Call ID: 243d4a17-8b34-428f-b1e5-ddf4e247ff60
  Args:
    source: Lida_Lacey_Bloodgood
    type: :Woman
  AssignClass (8b7f4eba-86e7-4eae-a27c-414a63f6f0e1)
 Call ID: 8b7f4eba-86e7-4eae-a27c-414a63f6f0e1
  Args:
    type: :Person
    source: Lida_Lacey_Bloodgood
  AssignClass (e176219e-47b3-4521-b6b5-be3955887690)
 Call ID: e176219e-47b3-4521-b6b5-be3955887690
  Args:
    type: :Woman
    source: Lida_Fleitmann_Bloodgood
  AssignClass (86d31892-8ed6-40e5-99b5-ba415a80afe4)
 Call ID: 86d31892-8ed6-40e5-99b5-ba415a80afe4
  Args:
    source: Lida_Fleitmann_Bloodgood
    type: :Person
  AddTriple (9dff2b3e-3ee1-4408-9aaa-6e91d41cd789)
 Call ID: 9dff2b3e-3ee1-4408-9aaa-6e91d41cd789
  Args:
    relation: :hasMother
    target: Lida_Fleitmann_Bloodgood
    source: Lida_Lacey_Bloodgood
  AssignClass (b1288d6d-a258-4193-9124-e7e91cdeb7cc)
 Call ID: b1288d6d-a258-4193-9124-e7e91cdeb7cc
  Args:
    source: Raimondo_della_Torre_e_Tasso
    type: :Man
  AssignClass (d81ec14c-e6aa-4bd3-ba87-9b584c104a50)
 Call ID: d81ec14c-e6aa-4bd3-ba87-9b584c104a50
  Args:
    type: :Person
    source: Raimondo_della_Torre_e_Tasso
  Finish (8f075cdb-6fa5-49a1-b3ff-c641d14a95b6)
 Call ID: 8f075cdb-6fa5-49a1-b3ff-c641d14a95b6
  Args: