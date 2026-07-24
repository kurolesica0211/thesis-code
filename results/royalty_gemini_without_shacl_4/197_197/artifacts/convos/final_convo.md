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
Princess Dolores of Bourbon-Two Sicilies (15 November 1909 – 11 May 1996) was a daughter of Prince Carlos of Bourbon-Two Sicilies and his wife Princess Louise of Orléans.
Princess Dolores was born into the House of Bourbon-Two Sicilies and was a member of the Polish-Lithuanian noble Czartoryski family through her marriage to Prince Augustyn Józef Czartoryski.
She was also an aunt of Juan Carlos I of Spain, son of her sister Princess María de las Mercedes of Bourbon-Two Sicilies.
Early life

Born on 15 November 1909 at the Palace of Villamejor, Princess Dolores of Bourbon-Two Sicilies was the second child of Prince Carlos of Bourbon-Two Sicilies and his second wife Princess Louise of Orléans.
She was christened Maria de los Dolores Victoria Felipa Luisa Mercedes.
Princess Dolores, nicknamed Dola among his relatives, was closely related to the Spanish royal family.
Her father, Prince Carlos of Bourbon-Two Sicilies, had renounced his right to the throne of Two Sicilies becoming a Spanish citizen when he married his first wife, Mercedes, Princess of Asturias, the eldest sister of King Alfonso XIII of Spain.
Dolores’s mother, Princess Louise of Orléans was a first cousin once removed of the Spanish King.
As a result, Dolores and her sibling grew up in close proximity to the Spanish royal family.
Her cousins, the children of King Alfonso XIII and Queen Victoria Eugenie were the same age as Dolores and her younger siblings.
The family lived at the Palace of Villamejor in Madrid, vacations were spent near Seville in the Palace of Villamanrique, property of her maternal grandmother, Isabelle, Countess of Paris.
Princess Dolores studied with her sisters Mercedes  and Esperanza in a school of Irish nuns in Madrid.
Dolores was twelve years old when she moved with her family to Seville when her father was appointed Military Captain General of Andalusia.
The Princess and her sisters continued their studies as boarders at  the school of Irish nuns in Castilleja de la Cueva in Seville.
Marriage and later life

In Paris, Princess Dolores met a wealthy Polish aristocrat Prince Augustyn Józef Czartoryski, 13th Prince Czartoryski, Duke of Klewan and Zuków, son of Prince Adam Ludwik Czartoryski and his wife Countess Maria Ludwika Krasińska.
The couple settled in Kraków, Poland where Dolores’s husband took over the running of the Family Museum.
In September 1939 with the Invasion of Poland bombs fell on Kraków, Prince Augustyn and Princess Dolores, who was pregnant, decided to leave the country and move to Spain.
After reaching Paris, Princess Dolores and her husband moved permanently to Spain.
They settled in Seville where Princess Dolores gave birth to a son: Prince Adam Karol Czartoryski (born 2 January 1940).
In 1943 the couple bought a rural property in Dos Hermanas which they called it Garden of the Princess, the farm was self-sufficient for the subsistence of the family.
The couple had a second son also born in Seville, Prince Ludwik Piotr Czartoryski (13 March 1945 - 3 May 1946), but the child died at only fourteen months.
At the end of the war, the properties of the Czartoryski family were nationalized by the Polish government and the family decided not to return to Kraków, for fear of the Soviet occupation.
Prince Augustyn was in poor health, the troubles and tribulation of the war took a toll on his life and he died on 1 July 1946, aged thirty nine.
The deaths of  both her youngest son and her husband only two months apart in 1946 deeply affected the Princess, who was left a widow with a six-year-old child.
Princess Dolores continued living in Seville, Spain.
Four years into her widowhood, she fell in love with Carlos Chías Osorio (born at Barcelona 26 Feb 1925), an ex seminarist, teacher  and preceptor of her son Adam.
Carlos Chias Osorio quickly became well liked in Dos Hermanas and in spite of the age disparity the marriage was a happy one.
After the death of Princess Dolores's mother in April that year, the couple moved to Madrid.
In the following decades, the princess and her husband lived simply in Madrid.



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
  AssignClass (d7f6dc21-38a9-4b28-9a13-d28264011cf4)
 Call ID: d7f6dc21-38a9-4b28-9a13-d28264011cf4
  Args:
    source: Princess_Dolores_of_Bourbon-Two_Sicilies
    type: :Woman
  AssignClass (8ce936a4-c381-4cab-9f3b-6cf0435807c5)
 Call ID: 8ce936a4-c381-4cab-9f3b-6cf0435807c5
  Args:
    type: :Person
    source: Princess_Dolores_of_Bourbon-Two_Sicilies
  AddLiteral (6c7157d0-fde1-4eb3-a4b6-599b30116cc4)
 Call ID: 6c7157d0-fde1-4eb3-a4b6-599b30116cc4
  Args:
    source: Princess_Dolores_of_Bourbon-Two_Sicilies
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1909
  AddLiteral (fa20086b-07f7-4128-8a43-666f5729f0a0)
 Call ID: fa20086b-07f7-4128-8a43-666f5729f0a0
  Args:
    literal_value: 1996
    literal_type: xsd:integer
    source: Princess_Dolores_of_Bourbon-Two_Sicilies
    relation: :hasDeathYear
  AssignClass (bbc43756-3e37-43f8-aa7a-3125e71d4c1c)
 Call ID: bbc43756-3e37-43f8-aa7a-3125e71d4c1c
  Args:
    type: :Man
    source: Prince_Carlos_of_Bourbon-Two_Sicilies
  AssignClass (f2fcd2a4-5f9b-4c7e-a161-240927c6bc88)
 Call ID: f2fcd2a4-5f9b-4c7e-a161-240927c6bc88
  Args:
    type: :Person
    source: Prince_Carlos_of_Bourbon-Two_Sicilies
  AssignClass (fcfe557f-e8f7-4eb5-9d83-d8587568bc01)
 Call ID: fcfe557f-e8f7-4eb5-9d83-d8587568bc01
  Args:
    type: :Woman
    source: Princess_Louise_of_Orléans
  AssignClass (ef4a78bc-489f-4df3-9f6c-1571a62aec0b)
 Call ID: ef4a78bc-489f-4df3-9f6c-1571a62aec0b
  Args:
    type: :Person
    source: Princess_Louise_of_Orléans
  AddTriple (cf337b35-9cd4-407f-846e-e62beb427f70)
 Call ID: cf337b35-9cd4-407f-846e-e62beb427f70
  Args:
    relation: :hasFather
    source: Princess_Dolores_of_Bourbon-Two_Sicilies
    target: Prince_Carlos_of_Bourbon-Two_Sicilies
  AddTriple (302c8e01-3d42-4986-a94c-41a4aee16d35)
 Call ID: 302c8e01-3d42-4986-a94c-41a4aee16d35
  Args:
    target: Princess_Louise_of_Orléans
    source: Princess_Dolores_of_Bourbon-Two_Sicilies
    relation: :hasMother
  AssignClass (8e4119e3-c137-4df2-97c0-c5b19aaaab39)
 Call ID: 8e4119e3-c137-4df2-97c0-c5b19aaaab39
  Args:
    source: Prince_Augustyn_Józef_Czartoryski
    type: :Man
  AssignClass (94886e98-9202-4e98-9684-f52449d2a21e)
 Call ID: 94886e98-9202-4e98-9684-f52449d2a21e
  Args:
    source: Prince_Augustyn_Józef_Czartoryski
    type: :Person
  AddTriple (40775940-b333-4fdd-adaf-6ff9d0e1dbae)
 Call ID: 40775940-b333-4fdd-adaf-6ff9d0e1dbae
  Args:
    source: Princess_Dolores_of_Bourbon-Two_Sicilies
    relation: :hasRelation
    target: Prince_Augustyn_Józef_Czartoryski
  AssignClass (299e8b2f-e023-46d7-bbce-050a61ff3c14)
 Call ID: 299e8b2f-e023-46d7-bbce-050a61ff3c14
  Args:
    type: :Woman
    source: Princess_María_de_las_Mercedes_of_Bourbon-Two_Sicilies
  AssignClass (2110f9b2-001c-4307-a382-5d4da924506c)
 Call ID: 2110f9b2-001c-4307-a382-5d4da924506c
  Args:
    source: Princess_María_de_las_Mercedes_of_Bourbon-Two_Sicilies
    type: :Person
  AddTriple (dea5abd8-0400-40cd-860c-5a478dada53d)
 Call ID: dea5abd8-0400-40cd-860c-5a478dada53d
  Args:
    target: Princess_María_de_las_Mercedes_of_Bourbon-Two_Sicilies
    relation: :isSisterOf
    source: Princess_Dolores_of_Bourbon-Two_Sicilies
  AssignClass (49032c88-3f98-4557-9ace-9a026bc96c20)
 Call ID: 49032c88-3f98-4557-9ace-9a026bc96c20
  Args:
    source: Juan_Carlos_I_of_Spain
    type: :Man
  AssignClass (ffbb65d0-d2e2-4d1d-8afc-2a83053964c0)
 Call ID: ffbb65d0-d2e2-4d1d-8afc-2a83053964c0
  Args:
    source: Juan_Carlos_I_of_Spain
    type: :Person
  AddTriple (7e96514b-54fa-47fd-86d5-e0bdc36ec56f)
 Call ID: 7e96514b-54fa-47fd-86d5-e0bdc36ec56f
  Args:
    target: Juan_Carlos_I_of_Spain
    relation: :isMotherOf
    source: Princess_María_de_las_Mercedes_of_Bourbon-Two_Sicilies
  AssignClass (5b8d3b2a-6da8-4764-af4b-24b60c2051f3)
 Call ID: 5b8d3b2a-6da8-4764-af4b-24b60c2051f3
  Args:
    source: Prince_Adam_Karol_Czartoryski
    type: :Man
  AssignClass (daf6c830-c390-4818-8efb-598c40b94d53)
 Call ID: daf6c830-c390-4818-8efb-598c40b94d53
  Args:
    source: Prince_Adam_Karol_Czartoryski
    type: :Person
  AddTriple (57ac7c2a-b0a8-4f58-8d32-24e677ac7bc6)
 Call ID: 57ac7c2a-b0a8-4f58-8d32-24e677ac7bc6
  Args:
    target: Princess_Dolores_of_Bourbon-Two_Sicilies
    relation: :isSonOf
    source: Prince_Adam_Karol_Czartoryski
  AddTriple (234c1749-3742-4a67-be62-62cc2e9c500c)
 Call ID: 234c1749-3742-4a67-be62-62cc2e9c500c
  Args:
    relation: :isSonOf
    source: Prince_Adam_Karol_Czartoryski
    target: Prince_Augustyn_Józef_Czartoryski
  AssignClass (d6d45071-5d53-47a1-b730-ecf2bee6dc19)
 Call ID: d6d45071-5d53-47a1-b730-ecf2bee6dc19
  Args:
    type: :Man
    source: Prince_Ludwik_Piotr_Czartoryski
  AssignClass (15435948-21d4-420c-812e-ca727226d94f)
 Call ID: 15435948-21d4-420c-812e-ca727226d94f
  Args:
    source: Prince_Ludwik_Piotr_Czartoryski
    type: :Person
  AddTriple (0d4ecbbc-5aab-4ff2-b288-0c01de5d9f77)
 Call ID: 0d4ecbbc-5aab-4ff2-b288-0c01de5d9f77
  Args:
    target: Princess_Dolores_of_Bourbon-Two_Sicilies
    source: Prince_Ludwik_Piotr_Czartoryski
    relation: :isSonOf
  AddTriple (a8f3b399-7f3e-4091-bbaa-91e45ad3b988)
 Call ID: a8f3b399-7f3e-4091-bbaa-91e45ad3b988
  Args:
    target: Prince_Augustyn_Józef_Czartoryski
    relation: :isSonOf
    source: Prince_Ludwik_Piotr_Czartoryski
  AddLiteral (d3f85aa7-d723-4810-87b9-8b097e87b656)
 Call ID: d3f85aa7-d723-4810-87b9-8b097e87b656
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: Prince_Ludwik_Piotr_Czartoryski
    literal_value: 1946
  AddLiteral (3af8b16b-0a67-4de1-b688-770f3f43ae95)
 Call ID: 3af8b16b-0a67-4de1-b688-770f3f43ae95
  Args:
    relation: :hasDeathYear
    source: Prince_Augustyn_Józef_Czartoryski
    literal_type: xsd:integer
    literal_value: 1946
  AssignClass (d6a04404-cc8e-4fee-ab92-f3e6b1d7533e)
 Call ID: d6a04404-cc8e-4fee-ab92-f3e6b1d7533e
  Args:
    type: :Man
    source: Prince_Adam_Ludwik_Czartoryski
  AssignClass (2f6e7791-41f0-463d-af7e-ed37a09685a6)
 Call ID: 2f6e7791-41f0-463d-af7e-ed37a09685a6
  Args:
    type: :Person
    source: Prince_Adam_Ludwik_Czartoryski
  AssignClass (8cfead6e-7e91-467a-afc4-05871261a9d0)
 Call ID: 8cfead6e-7e91-467a-afc4-05871261a9d0
  Args:
    type: :Woman
    source: Countess_Maria_Ludwika_Krasińska
  AssignClass (8c21f20c-1de5-400e-97bb-7ad213a1f619)
 Call ID: 8c21f20c-1de5-400e-97bb-7ad213a1f619
  Args:
    source: Countess_Maria_Ludwika_Krasińska
    type: :Person
  AddTriple (4bad6c71-df5b-4d17-b5c4-291d0cbdce51)
 Call ID: 4bad6c71-df5b-4d17-b5c4-291d0cbdce51
  Args:
    relation: :hasFather
    source: Prince_Augustyn_Józef_Czartoryski
    target: Prince_Adam_Ludwik_Czartoryski
  AddTriple (fe133feb-aa9a-4910-9416-656622f3f2c2)
 Call ID: fe133feb-aa9a-4910-9416-656622f3f2c2
  Args:
    relation: :hasMother
    source: Prince_Augustyn_Józef_Czartoryski
    target: Countess_Maria_Ludwika_Krasińska
  AssignClass (e84383ae-e9fe-4fcc-bd08-1d52da0c9a65)
 Call ID: e84383ae-e9fe-4fcc-bd08-1d52da0c9a65
  Args:
    type: :Man
    source: Carlos_Chías_Osorio
  AssignClass (45f66a5a-9840-4543-8a2a-cc2e5486b0f3)
 Call ID: 45f66a5a-9840-4543-8a2a-cc2e5486b0f3
  Args:
    source: Carlos_Chías_Osorio
    type: :Person
  AddTriple (f5b85396-cf61-4885-88ce-2ba3d1107dcb)
 Call ID: f5b85396-cf61-4885-88ce-2ba3d1107dcb
  Args:
    target: Carlos_Chías_Osorio
    relation: :hasRelation
    source: Princess_Dolores_of_Bourbon-Two_Sicilies
  AssignClass (ba3cac12-fb57-44b1-8f29-a22efca35ded)
 Call ID: ba3cac12-fb57-44b1-8f29-a22efca35ded
  Args:
    source: Princess_Esperanza_of_Bourbon-Two_Sicilies
    type: :Woman
  AssignClass (34b4f0df-139f-4272-9e51-c55eeaee0616)
 Call ID: 34b4f0df-139f-4272-9e51-c55eeaee0616
  Args:
    source: Princess_Esperanza_of_Bourbon-Two_Sicilies
    type: :Person
  AddTriple (8e2927af-e148-4a56-89d1-c16ac9e645cc)
 Call ID: 8e2927af-e148-4a56-89d1-c16ac9e645cc
  Args:
    target: Princess_Esperanza_of_Bourbon-Two_Sicilies
    relation: :isSisterOf
    source: Princess_Dolores_of_Bourbon-Two_Sicilies
  Finish (bc59e993-6805-4d03-91e6-76379e93ba1f)
 Call ID: bc59e993-6805-4d03-91e6-76379e93ba1f
  Args: