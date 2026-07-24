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
  AssignClass (48021f12-83b3-4717-a884-6fa7e081db3c)
 Call ID: 48021f12-83b3-4717-a884-6fa7e081db3c
  Args:
    type: :Woman
    source: Tatiana_Radziwill
  AddLiteral (dd951719-4ace-4a0b-99b9-c1c59c21b289)
 Call ID: dd951719-4ace-4a0b-99b9-c1c59c21b289
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1939
    source: Tatiana_Radziwill
  AddLiteral (c10aca7f-0e5a-4591-8a0f-e2e9a4dc902c)
 Call ID: c10aca7f-0e5a-4591-8a0f-e2e9a4dc902c
  Args:
    source: Tatiana_Radziwill
    literal_value: 2025
    relation: :hasDeathYear
    literal_type: xsd:integer
  AssignClass (7875cda6-6e6f-47e8-87d3-da9e5336342d)
 Call ID: 7875cda6-6e6f-47e8-87d3-da9e5336342d
  Args:
    type: :Man
    source: Dominik_Rainer_Radziwill
  AssignClass (12e331e0-56ee-461a-88cc-cb16d870d57b)
 Call ID: 12e331e0-56ee-461a-88cc-cb16d870d57b
  Args:
    type: :Woman
    source: Eugenie_of_Greece_and_Denmark
  AddTriple (d4e5cbe6-a397-46f8-906e-291c9327fc8d)
 Call ID: d4e5cbe6-a397-46f8-906e-291c9327fc8d
  Args:
    target: Dominik_Rainer_Radziwill
    relation: :hasFather
    source: Tatiana_Radziwill
  AddTriple (805d1209-4ccd-4b1f-8f21-dd1911f13e01)
 Call ID: 805d1209-4ccd-4b1f-8f21-dd1911f13e01
  Args:
    relation: :hasMother
    target: Eugenie_of_Greece_and_Denmark
    source: Tatiana_Radziwill
  AssignClass (88ee5de3-2700-4780-b195-a6b3705dd0e9)
 Call ID: 88ee5de3-2700-4780-b195-a6b3705dd0e9
  Args:
    type: :Man
    source: Hieronim_Mikolaj_Radziwill
  AssignClass (6069ab7b-4ff8-48b8-8db6-8a8b72ed3ec2)
 Call ID: 6069ab7b-4ff8-48b8-8db6-8a8b72ed3ec2
  Args:
    type: :Woman
    source: Renata_of_Austria
  AddTriple (a5f0196f-78a9-497d-8807-9b3095ffa19d)
 Call ID: a5f0196f-78a9-497d-8807-9b3095ffa19d
  Args:
    source: Dominik_Rainer_Radziwill
    target: Hieronim_Mikolaj_Radziwill
    relation: :hasFather
  AddTriple (41157a19-bfdf-4ba1-96be-f7bae9b63d54)
 Call ID: 41157a19-bfdf-4ba1-96be-f7bae9b63d54
  Args:
    source: Dominik_Rainer_Radziwill
    target: Renata_of_Austria
    relation: :hasMother
  AssignClass (77bebc11-5eed-4b87-9c1b-4db7aab37a89)
 Call ID: 77bebc11-5eed-4b87-9c1b-4db7aab37a89
  Args:
    type: :Man
    source: George_of_Greece_and_Denmark
  AssignClass (a7dac7e2-42f7-48e6-93f4-382e9e7ad521)
 Call ID: a7dac7e2-42f7-48e6-93f4-382e9e7ad521
  Args:
    type: :Woman
    source: Marie_Bonaparte
  AddTriple (fb0135c4-c016-46eb-8b7f-e39a4488b59b)
 Call ID: fb0135c4-c016-46eb-8b7f-e39a4488b59b
  Args:
    source: Eugenie_of_Greece_and_Denmark
    target: George_of_Greece_and_Denmark
    relation: :hasFather
  AddTriple (71597d2a-4dd6-4c86-89b8-3195323ca6e7)
 Call ID: 71597d2a-4dd6-4c86-89b8-3195323ca6e7
  Args:
    target: Marie_Bonaparte
    relation: :hasMother
    source: Eugenie_of_Greece_and_Denmark
  AssignClass (9bf26ee9-9743-4356-bdba-c3ccdfe17866)
 Call ID: 9bf26ee9-9743-4356-bdba-c3ccdfe17866
  Args:
    type: :Man
    source: George_I_of_Greece
  AssignClass (c8167498-285a-4d25-841f-873d54b3dd3e)
 Call ID: c8167498-285a-4d25-841f-873d54b3dd3e
  Args:
    type: :Woman
    source: Olga_Constantinovna_of_Russia
  AddTriple (fb8d7da9-ac21-4d08-b190-d051318ea380)
 Call ID: fb8d7da9-ac21-4d08-b190-d051318ea380
  Args:
    relation: :hasFather
    target: George_I_of_Greece
    source: George_of_Greece_and_Denmark
  AddTriple (af62582e-5ad4-41b3-9711-19a683d3307f)
 Call ID: af62582e-5ad4-41b3-9711-19a683d3307f
  Args:
    source: George_of_Greece_and_Denmark
    target: Olga_Constantinovna_of_Russia
    relation: :hasMother
  AssignClass (4aa68fa3-8b50-424b-9aa7-bd54c15f8915)
 Call ID: 4aa68fa3-8b50-424b-9aa7-bd54c15f8915
  Args:
    source: Roland_Napoleon_Bonaparte
    type: :Man
  AssignClass (be69447b-bb16-4b68-9382-a7fcbce8532d)
 Call ID: be69447b-bb16-4b68-9382-a7fcbce8532d
  Args:
    source: Marie_Felix_Blanc
    type: :Woman
  AddTriple (308a7d64-0315-4077-8fe1-a8ad8405f639)
 Call ID: 308a7d64-0315-4077-8fe1-a8ad8405f639
  Args:
    source: Marie_Bonaparte
    target: Roland_Napoleon_Bonaparte
    relation: :hasFather
  AddTriple (47c5ac04-6762-41a3-958f-d7ac721f28c9)
 Call ID: 47c5ac04-6762-41a3-958f-d7ac721f28c9
  Args:
    target: Marie_Felix_Blanc
    relation: :hasMother
    source: Marie_Bonaparte
  AssignClass (747138b1-31a7-491e-843b-6a4745c6f48e)
 Call ID: 747138b1-31a7-491e-843b-6a4745c6f48e
  Args:
    source: George_Radziwill
    type: :Man
  AddTriple (c85f0f8e-fd2a-4342-b448-d1c98d13e4f6)
 Call ID: c85f0f8e-fd2a-4342-b448-d1c98d13e4f6
  Args:
    relation: :isSiblingOf
    target: George_Radziwill
    source: Tatiana_Radziwill
  AssignClass (1efc5758-5846-463c-8331-93ba151572fc)
 Call ID: 1efc5758-5846-463c-8331-93ba151572fc
  Args:
    type: :Woman
    source: Lida_Lacey_Bloodgood
  AssignClass (d535a77e-0f21-4bde-a9d0-33eaf5e171e5)
 Call ID: d535a77e-0f21-4bde-a9d0-33eaf5e171e5
  Args:
    type: :Woman
    source: Lida_Fleitmann_Bloodgood
  AddTriple (be1cfc4a-8257-4b2d-8de2-215f67934711)
 Call ID: be1cfc4a-8257-4b2d-8de2-215f67934711
  Args:
    source: Lida_Lacey_Bloodgood
    target: Lida_Fleitmann_Bloodgood
    relation: :hasMother
  AssignClass (a0d3aeb1-307e-4de3-a622-de336215a085)
 Call ID: a0d3aeb1-307e-4de3-a622-de336215a085
  Args:
    type: :Man
    source: Raimondo_della_Torre_e_Tasso
  AssignClass (05cf27b1-2876-4fe1-b8f0-8a4afd1a2f88)
 Call ID: 05cf27b1-2876-4fe1-b8f0-8a4afd1a2f88
  Args:
    type: :Man
    source: Jean_Henri_Fruchaud
  AssignClass (bd29d6b4-4399-4fa5-b40b-9ae4946d6859)
 Call ID: bd29d6b4-4399-4fa5-b40b-9ae4946d6859
  Args:
    type: :Man
    source: Henri_Fruchard
  AssignClass (27b45f37-f1f4-4eaf-bd8a-ae950d5d6a5f)
 Call ID: 27b45f37-f1f4-4eaf-bd8a-ae950d5d6a5f
  Args:
    type: :Woman
    source: Eunice_McCooey
  AddTriple (8b4f37af-ed31-43a8-9585-2740888697d2)
 Call ID: 8b4f37af-ed31-43a8-9585-2740888697d2
  Args:
    source: Jean_Henri_Fruchaud
    relation: :hasFather
    target: Henri_Fruchard
  AddTriple (74d6810d-74b0-4be3-b007-36a65049447d)
 Call ID: 74d6810d-74b0-4be3-b007-36a65049447d
  Args:
    relation: :hasMother
    target: Eunice_McCooey
    source: Jean_Henri_Fruchaud
  AssignClass (229b0dba-5ae1-46da-a4d2-c350080abb8d)
 Call ID: 229b0dba-5ae1-46da-a4d2-c350080abb8d
  Args:
    type: :Woman
    source: Fabiola_Fruchaud
  AssignClass (ed84133f-d8e1-40b4-99c3-74217f7714d1)
 Call ID: ed84133f-d8e1-40b4-99c3-74217f7714d1
  Args:
    type: :Man
    source: Alexis_Fruchaud
  AddTriple (e76518db-d77c-452d-b858-8584d0abc1f3)
 Call ID: e76518db-d77c-452d-b858-8584d0abc1f3
  Args:
    source: Fabiola_Fruchaud
    relation: :hasFather
    target: Jean_Henri_Fruchaud
  AddTriple (4eab6d8f-e890-4838-a262-bdab7da5b9d5)
 Call ID: 4eab6d8f-e890-4838-a262-bdab7da5b9d5
  Args:
    target: Tatiana_Radziwill
    relation: :hasMother
    source: Fabiola_Fruchaud
  AddTriple (31d9c722-6f0b-452a-9067-0f48f6c6ec2e)
 Call ID: 31d9c722-6f0b-452a-9067-0f48f6c6ec2e
  Args:
    relation: :hasFather
    target: Jean_Henri_Fruchaud
    source: Alexis_Fruchaud
  AddTriple (de101f57-1aad-4ddd-a48d-52266e593d76)
 Call ID: de101f57-1aad-4ddd-a48d-52266e593d76
  Args:
    source: Alexis_Fruchaud
    relation: :hasMother
    target: Tatiana_Radziwill
  Finish (2a7c4a2e-f602-4823-ad3c-e7b6b06c8c3c)
 Call ID: 2a7c4a2e-f602-4823-ad3c-e7b6b06c8c3c
  Args: