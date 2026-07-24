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
  AssignClass (ec31c092-9260-4ef3-b4d0-658ab8167448)
 Call ID: ec31c092-9260-4ef3-b4d0-658ab8167448
  Args:
    type: :Woman
    source: Dolores_of_Bourbon-Two_Sicilies
  AssignClass (272f60d3-2ce3-4243-8ae6-604aa18b75cf)
 Call ID: 272f60d3-2ce3-4243-8ae6-604aa18b75cf
  Args:
    type: :Man
    source: Carlos_of_Bourbon-Two_Sicilies
  AssignClass (96ee9e89-abfe-441d-97a4-1e380ea69bdc)
 Call ID: 96ee9e89-abfe-441d-97a4-1e380ea69bdc
  Args:
    type: :Woman
    source: Louise_of_Orléans
  AssignClass (f0e3909c-b043-4fd3-9089-9898c54dc2b9)
 Call ID: f0e3909c-b043-4fd3-9089-9898c54dc2b9
  Args:
    type: :Man
    source: Augustyn_Józef_Czartoryski
  AssignClass (411b6883-caf6-46bb-affc-cb9876879c9a)
 Call ID: 411b6883-caf6-46bb-affc-cb9876879c9a
  Args:
    type: :Man
    source: Adam_Ludwik_Czartoryski
  AssignClass (95c56db6-1078-4c2e-ae75-e5168cb9f9bc)
 Call ID: 95c56db6-1078-4c2e-ae75-e5168cb9f9bc
  Args:
    type: :Woman
    source: Maria_Ludwika_Krasińska
  AssignClass (9c301611-6b00-40b3-bdae-1bd8d0398f9c)
 Call ID: 9c301611-6b00-40b3-bdae-1bd8d0398f9c
  Args:
    type: :Man
    source: Adam_Karol_Czartoryski
  AssignClass (5c188300-9a66-40e1-85d4-8b55258cc14e)
 Call ID: 5c188300-9a66-40e1-85d4-8b55258cc14e
  Args:
    type: :Man
    source: Ludwik_Piotr_Czartoryski
  AssignClass (bbc0674d-02b0-4bfa-92e0-01a0e5351df6)
 Call ID: bbc0674d-02b0-4bfa-92e0-01a0e5351df6
  Args:
    type: :Man
    source: Carlos_Chías_Osorio
  AssignClass (80349408-151a-4196-a1ab-305ff9342a14)
 Call ID: 80349408-151a-4196-a1ab-305ff9342a14
  Args:
    type: :Woman
    source: María_de_las_Mercedes_of_Bourbon-Two_Sicilies
  AssignClass (1f649869-9b6a-4070-9cd7-7a2d05f02d92)
 Call ID: 1f649869-9b6a-4070-9cd7-7a2d05f02d92
  Args:
    type: :Man
    source: Juan_Carlos_I_of_Spain
  AssignClass (0b446848-8686-417b-a09c-c05e5d9eb924)
 Call ID: 0b446848-8686-417b-a09c-c05e5d9eb924
  Args:
    type: :Woman
    source: Esperanza_of_Bourbon-Two_Sicilies
  AddLiteral (2174b74c-6f11-486e-939b-391abd6cc195)
 Call ID: 2174b74c-6f11-486e-939b-391abd6cc195
  Args:
    literal_value: 1909
    relation: :hasBirthYear
    source: Dolores_of_Bourbon-Two_Sicilies
    literal_type: xsd:integer
  AddLiteral (7d7981bb-9760-498d-b457-8f126b8b9f73)
 Call ID: 7d7981bb-9760-498d-b457-8f126b8b9f73
  Args:
    literal_type: xsd:integer
    source: Dolores_of_Bourbon-Two_Sicilies
    literal_value: 1996
    relation: :hasDeathYear
  AddTriple (82d773aa-c181-4b22-9884-61fa1c70214e)
 Call ID: 82d773aa-c181-4b22-9884-61fa1c70214e
  Args:
    relation: :hasFather
    source: Dolores_of_Bourbon-Two_Sicilies
    target: Carlos_of_Bourbon-Two_Sicilies
  AddTriple (c01ad9c6-49fc-4681-ae31-ed3f26d37ec0)
 Call ID: c01ad9c6-49fc-4681-ae31-ed3f26d37ec0
  Args:
    target: Louise_of_Orléans
    source: Dolores_of_Bourbon-Two_Sicilies
    relation: :hasMother
  AddTriple (0be585ba-7c16-41f5-b749-f6e527b9082a)
 Call ID: 0be585ba-7c16-41f5-b749-f6e527b9082a
  Args:
    target: Adam_Ludwik_Czartoryski
    relation: :hasFather
    source: Augustyn_Józef_Czartoryski
  AddTriple (762b0862-5031-4add-838a-438def301dc4)
 Call ID: 762b0862-5031-4add-838a-438def301dc4
  Args:
    target: Maria_Ludwika_Krasińska
    relation: :hasMother
    source: Augustyn_Józef_Czartoryski
  AddTriple (7e0518cd-1249-4ed2-ba0d-8bc0a404113e)
 Call ID: 7e0518cd-1249-4ed2-ba0d-8bc0a404113e
  Args:
    target: Augustyn_Józef_Czartoryski
    relation: :hasFather
    source: Adam_Karol_Czartoryski
  AddTriple (8d268f4c-3414-43dc-8e3b-2a83925f4a66)
 Call ID: 8d268f4c-3414-43dc-8e3b-2a83925f4a66
  Args:
    source: Adam_Karol_Czartoryski
    relation: :hasMother
    target: Dolores_of_Bourbon-Two_Sicilies
  AddTriple (36fb6e4a-da0a-472b-b5d3-82da58136e73)
 Call ID: 36fb6e4a-da0a-472b-b5d3-82da58136e73
  Args:
    target: Augustyn_Józef_Czartoryski
    relation: :hasFather
    source: Ludwik_Piotr_Czartoryski
  AddTriple (3c6a38a0-b370-436c-b09c-1ede47a024e3)
 Call ID: 3c6a38a0-b370-436c-b09c-1ede47a024e3
  Args:
    target: Dolores_of_Bourbon-Two_Sicilies
    relation: :hasMother
    source: Ludwik_Piotr_Czartoryski
  AddTriple (27446531-f4bb-43ee-a765-aa22c0ff8067)
 Call ID: 27446531-f4bb-43ee-a765-aa22c0ff8067
  Args:
    relation: :hasFather
    source: Juan_Carlos_I_of_Spain
    target: María_de_las_Mercedes_of_Bourbon-Two_Sicilies
  AddTriple (88d28c99-0493-43e5-b578-4b5b1daed8a5)
 Call ID: 88d28c99-0493-43e5-b578-4b5b1daed8a5
  Args:
    relation: :hasSister
    source: Dolores_of_Bourbon-Two_Sicilies
    target: María_de_las_Mercedes_of_Bourbon-Two_Sicilies
  AddTriple (95070696-e597-4b85-8184-23c8cbb621cf)
 Call ID: 95070696-e597-4b85-8184-23c8cbb621cf
  Args:
    target: Esperanza_of_Bourbon-Two_Sicilies
    relation: :hasSister
    source: Dolores_of_Bourbon-Two_Sicilies
  AddTriple (1c5b6324-9a08-438d-b8c1-054c37ced2b1)
 Call ID: 1c5b6324-9a08-438d-b8c1-054c37ced2b1
  Args:
    target: Carlos_of_Bourbon-Two_Sicilies
    source: María_de_las_Mercedes_of_Bourbon-Two_Sicilies
    relation: :hasFather
  AddTriple (a60d449a-fb2e-4eb7-952f-5794f5381aa8)
 Call ID: a60d449a-fb2e-4eb7-952f-5794f5381aa8
  Args:
    target: Louise_of_Orléans
    relation: :hasMother
    source: María_de_las_Mercedes_of_Bourbon-Two_Sicilies
  AddTriple (ea37a9f0-91e1-485f-8c49-86842df5df20)
 Call ID: ea37a9f0-91e1-485f-8c49-86842df5df20
  Args:
    relation: :hasFather
    source: Esperanza_of_Bourbon-Two_Sicilies
    target: Carlos_of_Bourbon-Two_Sicilies
  AddTriple (f05e262a-7d30-4c8e-ac20-0318e2f7ec07)
 Call ID: f05e262a-7d30-4c8e-ac20-0318e2f7ec07
  Args:
    target: Louise_of_Orléans
    source: Esperanza_of_Bourbon-Two_Sicilies
    relation: :hasMother
  Finish (dc1dd4d3-ec46-438a-81f2-94ddcd4653fb)
 Call ID: dc1dd4d3-ec46-438a-81f2-94ddcd4653fb
  Args: