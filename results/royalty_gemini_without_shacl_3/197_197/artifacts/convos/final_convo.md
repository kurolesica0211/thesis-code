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
  AssignClass (07173c29-2e77-4b07-b818-aabe89ed4af9)
 Call ID: 07173c29-2e77-4b07-b818-aabe89ed4af9
  Args:
    type: :Woman
    source: Dolores_of_Bourbon-Two_Sicilies
  AssignClass (d79e63a4-8c93-4c43-ac50-35f13114429f)
 Call ID: d79e63a4-8c93-4c43-ac50-35f13114429f
  Args:
    type: :Person
    source: Dolores_of_Bourbon-Two_Sicilies
  AddLiteral (0b4621b4-79e5-4a95-ae3e-92e5fff7a2de)
 Call ID: 0b4621b4-79e5-4a95-ae3e-92e5fff7a2de
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1909
    source: Dolores_of_Bourbon-Two_Sicilies
  AddLiteral (6a78289a-71db-4c86-b3a8-3bf09b5cb80c)
 Call ID: 6a78289a-71db-4c86-b3a8-3bf09b5cb80c
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1996
    source: Dolores_of_Bourbon-Two_Sicilies
  AssignClass (57841039-e57f-4c2c-9663-3ee2b4770e3a)
 Call ID: 57841039-e57f-4c2c-9663-3ee2b4770e3a
  Args:
    type: :Man
    source: Carlos_of_Bourbon-Two_Sicilies
  AssignClass (c240675b-b4f1-4548-86e3-328c28468439)
 Call ID: c240675b-b4f1-4548-86e3-328c28468439
  Args:
    type: :Person
    source: Carlos_of_Bourbon-Two_Sicilies
  AssignClass (ee92c51f-3403-432b-90f0-adc5a57e1f89)
 Call ID: ee92c51f-3403-432b-90f0-adc5a57e1f89
  Args:
    type: :Woman
    source: Louise_of_Orléans
  AssignClass (0892d0d2-a42a-4d23-96b2-92edd6152b4e)
 Call ID: 0892d0d2-a42a-4d23-96b2-92edd6152b4e
  Args:
    type: :Person
    source: Louise_of_Orléans
  AddTriple (ac14b645-e5f4-48b4-874b-db663bc9c286)
 Call ID: ac14b645-e5f4-48b4-874b-db663bc9c286
  Args:
    source: Dolores_of_Bourbon-Two_Sicilies
    target: Carlos_of_Bourbon-Two_Sicilies
    relation: :hasFather
  AddTriple (baa593c8-a27f-40a1-b13a-512c1c872494)
 Call ID: baa593c8-a27f-40a1-b13a-512c1c872494
  Args:
    target: Louise_of_Orléans
    relation: :hasMother
    source: Dolores_of_Bourbon-Two_Sicilies
  AssignClass (f611435d-e455-4f41-97b5-4c64c34cc793)
 Call ID: f611435d-e455-4f41-97b5-4c64c34cc793
  Args:
    type: :Man
    source: Augustyn_Józef_Czartoryski
  AssignClass (326edfc6-2f82-4d34-829e-e5fbd8b7b00b)
 Call ID: 326edfc6-2f82-4d34-829e-e5fbd8b7b00b
  Args:
    type: :Person
    source: Augustyn_Józef_Czartoryski
  AddTriple (674e624e-9e34-4a48-b84d-b1d98d198961)
 Call ID: 674e624e-9e34-4a48-b84d-b1d98d198961
  Args:
    source: Dolores_of_Bourbon-Two_Sicilies
    relation: :hasRelation
    target: Augustyn_Józef_Czartoryski
  AssignClass (5b1d7554-ea68-4e96-a098-071b7ed0d79a)
 Call ID: 5b1d7554-ea68-4e96-a098-071b7ed0d79a
  Args:
    type: :Man
    source: Juan_Carlos_I_of_Spain
  AssignClass (eec74e41-85c9-49ec-879f-f87b9b924409)
 Call ID: eec74e41-85c9-49ec-879f-f87b9b924409
  Args:
    type: :Person
    source: Juan_Carlos_I_of_Spain
  AssignClass (07bd6bfd-038b-47f5-a76c-b72d067a3827)
 Call ID: 07bd6bfd-038b-47f5-a76c-b72d067a3827
  Args:
    type: :Woman
    source: María_de_las_Mercedes_of_Bourbon-Two_Sicilies
  AssignClass (e102bae7-adb4-4d50-a6fe-fabd66498d02)
 Call ID: e102bae7-adb4-4d50-a6fe-fabd66498d02
  Args:
    type: :Person
    source: María_de_las_Mercedes_of_Bourbon-Two_Sicilies
  AddTriple (813600be-1ff9-4acd-ade4-3e12d3bf8e59)
 Call ID: 813600be-1ff9-4acd-ade4-3e12d3bf8e59
  Args:
    source: María_de_las_Mercedes_of_Bourbon-Two_Sicilies
    relation: :isSisterOf
    target: Dolores_of_Bourbon-Two_Sicilies
  AddTriple (5b528bfa-5d1d-4790-abf1-478a79f6bd84)
 Call ID: 5b528bfa-5d1d-4790-abf1-478a79f6bd84
  Args:
    relation: :isMotherOf
    target: Juan_Carlos_I_of_Spain
    source: María_de_las_Mercedes_of_Bourbon-Two_Sicilies
  AssignClass (a586c4ab-894a-4cf0-9f34-d25efc4ccd1c)
 Call ID: a586c4ab-894a-4cf0-9f34-d25efc4ccd1c
  Args:
    type: :Man
    source: Adam_Ludwik_Czartoryski
  AssignClass (71a8b842-1413-4b8f-99e3-53991615ba65)
 Call ID: 71a8b842-1413-4b8f-99e3-53991615ba65
  Args:
    type: :Person
    source: Adam_Ludwik_Czartoryski
  AssignClass (2a1be068-8709-4f7c-bfb9-d1002d10bb0a)
 Call ID: 2a1be068-8709-4f7c-bfb9-d1002d10bb0a
  Args:
    type: :Woman
    source: Maria_Ludwika_Krasińska
  AssignClass (7a337f39-2ccf-43b3-bcaa-b3483a370fbc)
 Call ID: 7a337f39-2ccf-43b3-bcaa-b3483a370fbc
  Args:
    type: :Person
    source: Maria_Ludwika_Krasińska
  AddTriple (5faab3c3-13f5-4ad9-be1c-9880d521e4e1)
 Call ID: 5faab3c3-13f5-4ad9-be1c-9880d521e4e1
  Args:
    relation: :hasFather
    target: Adam_Ludwik_Czartoryski
    source: Augustyn_Józef_Czartoryski
  AddTriple (166f1811-ab43-4fa3-8c31-b3aa6e776bc8)
 Call ID: 166f1811-ab43-4fa3-8c31-b3aa6e776bc8
  Args:
    source: Augustyn_Józef_Czartoryski
    target: Maria_Ludwika_Krasińska
    relation: :hasMother
  AssignClass (3bb865a4-c7f0-4b2a-9a0f-9d30df1d23ce)
 Call ID: 3bb865a4-c7f0-4b2a-9a0f-9d30df1d23ce
  Args:
    type: :Man
    source: Adam_Karol_Czartoryski
  AssignClass (14bef81a-448f-4a4c-9a39-6813a3ac2aca)
 Call ID: 14bef81a-448f-4a4c-9a39-6813a3ac2aca
  Args:
    type: :Person
    source: Adam_Karol_Czartoryski
  AddTriple (4f6400e7-1849-4732-a70a-b08d0a8b9bc2)
 Call ID: 4f6400e7-1849-4732-a70a-b08d0a8b9bc2
  Args:
    source: Adam_Karol_Czartoryski
    target: Dolores_of_Bourbon-Two_Sicilies
    relation: :isSonOf
  AddTriple (f16deef9-f1a4-43d5-9aaa-78853cefe46a)
 Call ID: f16deef9-f1a4-43d5-9aaa-78853cefe46a
  Args:
    target: Augustyn_Józef_Czartoryski
    relation: :isSonOf
    source: Adam_Karol_Czartoryski
  AssignClass (136700ce-134c-4f19-b9c5-5952ead94b65)
 Call ID: 136700ce-134c-4f19-b9c5-5952ead94b65
  Args:
    type: :Man
    source: Ludwik_Piotr_Czartoryski
  AssignClass (e26f2c91-9138-40b3-bfc5-5a544d67a6b1)
 Call ID: e26f2c91-9138-40b3-bfc5-5a544d67a6b1
  Args:
    type: :Person
    source: Ludwik_Piotr_Czartoryski
  AddTriple (bb04ce94-7b00-4a36-959f-24c92951ed69)
 Call ID: bb04ce94-7b00-4a36-959f-24c92951ed69
  Args:
    source: Ludwik_Piotr_Czartoryski
    target: Dolores_of_Bourbon-Two_Sicilies
    relation: :isSonOf
  AddTriple (556382b7-bace-4c53-b707-b2c436f9e327)
 Call ID: 556382b7-bace-4c53-b707-b2c436f9e327
  Args:
    source: Ludwik_Piotr_Czartoryski
    relation: :isSonOf
    target: Augustyn_Józef_Czartoryski
  AddLiteral (f839074e-2bda-4174-9222-ecc99627a49b)
 Call ID: f839074e-2bda-4174-9222-ecc99627a49b
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Ludwik_Piotr_Czartoryski
    literal_value: 1945
  AddLiteral (aec209a0-7e22-49ca-9afe-0d6b6d372ab2)
 Call ID: aec209a0-7e22-49ca-9afe-0d6b6d372ab2
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1946
    source: Ludwik_Piotr_Czartoryski
  AddLiteral (930aa68a-0ae7-46c2-8e35-224151b81e18)
 Call ID: 930aa68a-0ae7-46c2-8e35-224151b81e18
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1946
    source: Augustyn_Józef_Czartoryski
  AssignClass (deda467e-5818-48c4-9035-0052570cffee)
 Call ID: deda467e-5818-48c4-9035-0052570cffee
  Args:
    type: :Man
    source: Carlos_Chías_Osorio
  AssignClass (ed7d2ae4-2f95-4cc7-b903-7c586a058c0d)
 Call ID: ed7d2ae4-2f95-4cc7-b903-7c586a058c0d
  Args:
    type: :Person
    source: Carlos_Chías_Osorio
  AddTriple (e178181d-bd40-40bd-b592-378fbde8be0e)
 Call ID: e178181d-bd40-40bd-b592-378fbde8be0e
  Args:
    source: Dolores_of_Bourbon-Two_Sicilies
    target: Carlos_Chías_Osorio
    relation: :hasRelation
  Finish (862350cb-49ed-40f0-8fef-7ed1ceab765a)
 Call ID: 862350cb-49ed-40f0-8fef-7ed1ceab765a
  Args: