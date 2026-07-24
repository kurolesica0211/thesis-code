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
  AssignClass (c1cdffa5-9d58-4853-9602-b869640e9abc)
 Call ID: c1cdffa5-9d58-4853-9602-b869640e9abc
  Args:
    type: :Person
    source: :Tatiana_Radziwill
  AssignClass (90fce9b8-c7d0-4133-8fbb-c44a01f82b90)
 Call ID: 90fce9b8-c7d0-4133-8fbb-c44a01f82b90
  Args:
    type: :Woman
    source: :Tatiana_Radziwill
  AddLiteral (f293b1e8-72fb-421c-94ce-9ef4ed7c921c)
 Call ID: f293b1e8-72fb-421c-94ce-9ef4ed7c921c
  Args:
    literal_value: 1939
    relation: :hasBirthYear
    source: :Tatiana_Radziwill
    literal_type: xsd:integer
  AddLiteral (5fae4017-5433-4d90-8897-d6ac9efa862a)
 Call ID: 5fae4017-5433-4d90-8897-d6ac9efa862a
  Args:
    literal_value: 2025
    relation: :hasDeathYear
    source: :Tatiana_Radziwill
    literal_type: xsd:integer
  AssignClass (056bb986-f9fb-4c47-ba1b-1c3704e99665)
 Call ID: 056bb986-f9fb-4c47-ba1b-1c3704e99665
  Args:
    type: :Person
    source: :Dominik_Rainer_Radziwill
  AssignClass (996adf25-e2d2-49e0-9344-7ea7d5b1ee1a)
 Call ID: 996adf25-e2d2-49e0-9344-7ea7d5b1ee1a
  Args:
    type: :Man
    source: :Dominik_Rainer_Radziwill
  AssignClass (cd7d0ffc-c6aa-4209-9702-55ca4bd452c7)
 Call ID: cd7d0ffc-c6aa-4209-9702-55ca4bd452c7
  Args:
    type: :Person
    source: :Eugenie_of_Greece_and_Denmark
  AssignClass (5bd65416-3c24-49ab-8332-420a568631ab)
 Call ID: 5bd65416-3c24-49ab-8332-420a568631ab
  Args:
    type: :Woman
    source: :Eugenie_of_Greece_and_Denmark
  AddTriple (d88bf80a-19e3-453b-b848-7c361ec6b676)
 Call ID: d88bf80a-19e3-453b-b848-7c361ec6b676
  Args:
    source: :Tatiana_Radziwill
    relation: :hasFather
    target: :Dominik_Rainer_Radziwill
  AddTriple (b507a8b8-d68d-4e19-9845-b6c7161c875d)
 Call ID: b507a8b8-d68d-4e19-9845-b6c7161c875d
  Args:
    target: :Eugenie_of_Greece_and_Denmark
    relation: :hasMother
    source: :Tatiana_Radziwill
  AssignClass (b96545cb-6733-4432-90b5-db1841069b5b)
 Call ID: b96545cb-6733-4432-90b5-db1841069b5b
  Args:
    type: :Person
    source: :George_Radziwill
  AssignClass (9b831dcf-564f-4cb7-b56c-1fae4d581b1d)
 Call ID: 9b831dcf-564f-4cb7-b56c-1fae4d581b1d
  Args:
    type: :Man
    source: :George_Radziwill
  AddTriple (b116bfde-ec0c-430d-9cee-92fbfacefbd2)
 Call ID: b116bfde-ec0c-430d-9cee-92fbfacefbd2
  Args:
    target: :George_Radziwill
    relation: :hasBrother
    source: :Tatiana_Radziwill
  AssignClass (7cf5ac97-e72c-4609-83af-c9b5ef3fcb3d)
 Call ID: 7cf5ac97-e72c-4609-83af-c9b5ef3fcb3d
  Args:
    type: :Person
    source: :Hieronim_Mikolaj_Radziwill
  AssignClass (4c0ed990-4dbd-4570-b4d4-003eb442530b)
 Call ID: 4c0ed990-4dbd-4570-b4d4-003eb442530b
  Args:
    type: :Man
    source: :Hieronim_Mikolaj_Radziwill
  AssignClass (f519d7db-f8a3-4d9d-8384-72204b8e9415)
 Call ID: f519d7db-f8a3-4d9d-8384-72204b8e9415
  Args:
    type: :Person
    source: :Renata_of_Austria
  AssignClass (ce3a4785-9fc8-4998-a94f-ca2748eb3066)
 Call ID: ce3a4785-9fc8-4998-a94f-ca2748eb3066
  Args:
    type: :Woman
    source: :Renata_of_Austria
  AddTriple (236929b7-51ec-4d0c-ac20-8fe35b643f83)
 Call ID: 236929b7-51ec-4d0c-ac20-8fe35b643f83
  Args:
    source: :Dominik_Rainer_Radziwill
    relation: :hasFather
    target: :Hieronim_Mikolaj_Radziwill
  AddTriple (941d580f-265f-4990-b955-375943533f41)
 Call ID: 941d580f-265f-4990-b955-375943533f41
  Args:
    source: :Dominik_Rainer_Radziwill
    target: :Renata_of_Austria
    relation: :hasMother
  AssignClass (ebe6d530-df68-4ce0-8387-a8045387981e)
 Call ID: ebe6d530-df68-4ce0-8387-a8045387981e
  Args:
    type: :Person
    source: :George_of_Greece_and_Denmark
  AssignClass (99c0bec1-d8ca-4cc3-88ab-f0b78d1d233d)
 Call ID: 99c0bec1-d8ca-4cc3-88ab-f0b78d1d233d
  Args:
    type: :Man
    source: :George_of_Greece_and_Denmark
  AssignClass (cc254abf-b5d9-4758-a57e-8b4ea76049de)
 Call ID: cc254abf-b5d9-4758-a57e-8b4ea76049de
  Args:
    type: :Person
    source: :Marie_Bonaparte
  AssignClass (44e674f9-4812-4d6d-8717-cd0d1b68d475)
 Call ID: 44e674f9-4812-4d6d-8717-cd0d1b68d475
  Args:
    type: :Woman
    source: :Marie_Bonaparte
  AddTriple (643de895-5094-4ab4-bb61-62b41d4544d6)
 Call ID: 643de895-5094-4ab4-bb61-62b41d4544d6
  Args:
    target: :George_of_Greece_and_Denmark
    relation: :hasFather
    source: :Eugenie_of_Greece_and_Denmark
  AddTriple (801c384b-38ac-45f7-b173-ca928b27e0f7)
 Call ID: 801c384b-38ac-45f7-b173-ca928b27e0f7
  Args:
    relation: :hasMother
    target: :Marie_Bonaparte
    source: :Eugenie_of_Greece_and_Denmark
  AssignClass (e474702c-71a6-4ede-9f42-4e8fc6385b44)
 Call ID: e474702c-71a6-4ede-9f42-4e8fc6385b44
  Args:
    type: :Person
    source: :Jean_Henri_Fruchaud
  AssignClass (215b14dc-88e1-48c1-8563-2939883952ef)
 Call ID: 215b14dc-88e1-48c1-8563-2939883952ef
  Args:
    type: :Man
    source: :Jean_Henri_Fruchaud
  AssignClass (d3bd4a93-5370-4ecd-a5f4-83537ab0383e)
 Call ID: d3bd4a93-5370-4ecd-a5f4-83537ab0383e
  Args:
    type: :Person
    source: :Fabiola_Fruchaud
  AssignClass (a661ddba-af95-4224-861b-f01092753fa0)
 Call ID: a661ddba-af95-4224-861b-f01092753fa0
  Args:
    type: :Woman
    source: :Fabiola_Fruchaud
  AssignClass (4829aeb7-57ea-44a3-9787-a33ac9936c3c)
 Call ID: 4829aeb7-57ea-44a3-9787-a33ac9936c3c
  Args:
    type: :Person
    source: :Alexis_Fruchaud
  AssignClass (44203ece-d9d0-434d-96ed-6ef1ceaf047c)
 Call ID: 44203ece-d9d0-434d-96ed-6ef1ceaf047c
  Args:
    type: :Man
    source: :Alexis_Fruchaud
  AddTriple (de990590-4c5d-43b8-adda-984eca44fece)
 Call ID: de990590-4c5d-43b8-adda-984eca44fece
  Args:
    source: :Fabiola_Fruchaud
    target: :Jean_Henri_Fruchaud
    relation: :hasFather
  AddTriple (d345d0b2-df56-4793-b8ef-3dec6d2e9cbe)
 Call ID: d345d0b2-df56-4793-b8ef-3dec6d2e9cbe
  Args:
    source: :Fabiola_Fruchaud
    target: :Tatiana_Radziwill
    relation: :hasMother
  AddTriple (1d3b841a-e04d-4978-ac58-728af5a53f83)
 Call ID: 1d3b841a-e04d-4978-ac58-728af5a53f83
  Args:
    source: :Alexis_Fruchaud
    target: :Jean_Henri_Fruchaud
    relation: :hasFather
  AddTriple (0a908cb8-8307-4c60-ada5-2806eb450197)
 Call ID: 0a908cb8-8307-4c60-ada5-2806eb450197
  Args:
    relation: :hasMother
    target: :Tatiana_Radziwill
    source: :Alexis_Fruchaud
  Finish (49ee6ebc-42d1-46e7-88b5-f44eab7fa423)
 Call ID: 49ee6ebc-42d1-46e7-88b5-f44eab7fa423
  Args: