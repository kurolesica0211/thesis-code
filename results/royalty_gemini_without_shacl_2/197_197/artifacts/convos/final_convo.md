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
  AssignClass (1e4a604b-b0df-4fb6-9574-7f8a432f0f9a)
 Call ID: 1e4a604b-b0df-4fb6-9574-7f8a432f0f9a
  Args:
    type: :Woman
    source: Dolores_of_Bourbon-Two_Sicilies
  AssignClass (53f91641-615a-4735-922d-0a75ffd2a8bd)
 Call ID: 53f91641-615a-4735-922d-0a75ffd2a8bd
  Args:
    source: Dolores_of_Bourbon-Two_Sicilies
    type: :Person
  AddLiteral (57d6954c-3719-42e3-95de-464f1a824e48)
 Call ID: 57d6954c-3719-42e3-95de-464f1a824e48
  Args:
    literal_value: 1909
    relation: :hasBirthYear
    source: Dolores_of_Bourbon-Two_Sicilies
    literal_type: xsd:integer
  AddLiteral (97cd4a69-b8a5-49ed-84af-6fa97ee7a490)
 Call ID: 97cd4a69-b8a5-49ed-84af-6fa97ee7a490
  Args:
    literal_type: xsd:integer
    source: Dolores_of_Bourbon-Two_Sicilies
    relation: :hasDeathYear
    literal_value: 1996
  AssignClass (4e7b4d43-c684-4e7e-ab9a-52e03892f6cf)
 Call ID: 4e7b4d43-c684-4e7e-ab9a-52e03892f6cf
  Args:
    source: Carlos_of_Bourbon-Two_Sicilies
    type: :Man
  AssignClass (090bc1b3-f6ec-4ca7-8450-15d11949b31b)
 Call ID: 090bc1b3-f6ec-4ca7-8450-15d11949b31b
  Args:
    type: :Person
    source: Carlos_of_Bourbon-Two_Sicilies
  AssignClass (c25f05bf-23b5-4a81-a2a3-a280a74bd146)
 Call ID: c25f05bf-23b5-4a81-a2a3-a280a74bd146
  Args:
    type: :Woman
    source: Louise_of_Orleans
  AssignClass (46f89f4f-69dc-45d1-9fde-f684ebdbb5c0)
 Call ID: 46f89f4f-69dc-45d1-9fde-f684ebdbb5c0
  Args:
    type: :Person
    source: Louise_of_Orleans
  AddTriple (75d89638-cb24-4ff7-a0ed-54211a47af01)
 Call ID: 75d89638-cb24-4ff7-a0ed-54211a47af01
  Args:
    relation: :hasFather
    target: Carlos_of_Bourbon-Two_Sicilies
    source: Dolores_of_Bourbon-Two_Sicilies
  AddTriple (5ebdf6b2-f46e-483b-90f1-652f67cf37c2)
 Call ID: 5ebdf6b2-f46e-483b-90f1-652f67cf37c2
  Args:
    source: Dolores_of_Bourbon-Two_Sicilies
    target: Louise_of_Orleans
    relation: :hasMother
  AssignClass (937e43ab-7f2e-445c-a5e3-3cdfb5e8ba1d)
 Call ID: 937e43ab-7f2e-445c-a5e3-3cdfb5e8ba1d
  Args:
    type: :Man
    source: Augustyn_Jozef_Czartoryski
  AssignClass (8efa8052-9bda-472b-89c8-bce503eb8156)
 Call ID: 8efa8052-9bda-472b-89c8-bce503eb8156
  Args:
    source: Augustyn_Jozef_Czartoryski
    type: :Person
  AddTriple (06a0c681-e0ad-43af-877c-819d0a59f3ca)
 Call ID: 06a0c681-e0ad-43af-877c-819d0a59f3ca
  Args:
    relation: :hasRelation
    source: Dolores_of_Bourbon-Two_Sicilies
    target: Augustyn_Jozef_Czartoryski
  AssignClass (cdf72413-2605-4799-bec7-ec6a1659a269)
 Call ID: cdf72413-2605-4799-bec7-ec6a1659a269
  Args:
    source: Adam_Ludwik_Czartoryski
    type: :Man
  AssignClass (330fd412-40a5-4bd4-9b59-0472248e091b)
 Call ID: 330fd412-40a5-4bd4-9b59-0472248e091b
  Args:
    type: :Person
    source: Adam_Ludwik_Czartoryski
  AssignClass (c7590682-71ae-4e80-aee0-c6669916d505)
 Call ID: c7590682-71ae-4e80-aee0-c6669916d505
  Args:
    type: :Woman
    source: Maria_Ludwika_Krasinska
  AssignClass (d2850642-1d2b-4cf3-b27b-210c88338b11)
 Call ID: d2850642-1d2b-4cf3-b27b-210c88338b11
  Args:
    source: Maria_Ludwika_Krasinska
    type: :Person
  AddTriple (38df08cd-d8f9-4501-869d-2dc7ca34e190)
 Call ID: 38df08cd-d8f9-4501-869d-2dc7ca34e190
  Args:
    relation: :hasFather
    target: Adam_Ludwik_Czartoryski
    source: Augustyn_Jozef_Czartoryski
  AddTriple (50d544f7-2641-48b6-baf3-7ce6d2d53091)
 Call ID: 50d544f7-2641-48b6-baf3-7ce6d2d53091
  Args:
    relation: :hasMother
    source: Augustyn_Jozef_Czartoryski
    target: Maria_Ludwika_Krasinska
  AssignClass (cbe7bae4-d844-4351-af60-7bcb476ec6d2)
 Call ID: cbe7bae4-d844-4351-af60-7bcb476ec6d2
  Args:
    source: Juan_Carlos_I_of_Spain
    type: :Man
  AssignClass (593289cd-454a-486b-9f24-5c3aec68240e)
 Call ID: 593289cd-454a-486b-9f24-5c3aec68240e
  Args:
    source: Juan_Carlos_I_of_Spain
    type: :Person
  AssignClass (cfdb09e3-ff66-47d6-a8b0-c9a6b8fb3d5d)
 Call ID: cfdb09e3-ff66-47d6-a8b0-c9a6b8fb3d5d
  Args:
    type: :Woman
    source: Maria_de_las_Mercedes_of_Bourbon-Two_Sicilies
  AssignClass (4271ce19-835e-421f-b544-b93f42203b29)
 Call ID: 4271ce19-835e-421f-b544-b93f42203b29
  Args:
    source: Maria_de_las_Mercedes_of_Bourbon-Two_Sicilies
    type: :Person
  AddTriple (5b528c88-c2c3-4a7b-bcbb-f42c7c1043f6)
 Call ID: 5b528c88-c2c3-4a7b-bcbb-f42c7c1043f6
  Args:
    relation: :isMotherOf
    target: Juan_Carlos_I_of_Spain
    source: Maria_de_las_Mercedes_of_Bourbon-Two_Sicilies
  AddTriple (912011cd-2f01-4fe1-b961-92635a3bf59c)
 Call ID: 912011cd-2f01-4fe1-b961-92635a3bf59c
  Args:
    relation: :isSisterOf
    source: Maria_de_las_Mercedes_of_Bourbon-Two_Sicilies
    target: Dolores_of_Bourbon-Two_Sicilies
  AddTriple (95f0ba37-9227-4337-aff2-06f10871b571)
 Call ID: 95f0ba37-9227-4337-aff2-06f10871b571
  Args:
    target: Juan_Carlos_I_of_Spain
    source: Dolores_of_Bourbon-Two_Sicilies
    relation: :isAuntOf
  AssignClass (8672cd08-caae-415d-8182-c4cb87ea7334)
 Call ID: 8672cd08-caae-415d-8182-c4cb87ea7334
  Args:
    type: :Man
    source: Adam_Karol_Czartoryski
  AssignClass (6b8294c9-6826-4825-a2a2-7a06221ef4a3)
 Call ID: 6b8294c9-6826-4825-a2a2-7a06221ef4a3
  Args:
    source: Adam_Karol_Czartoryski
    type: :Person
  AddTriple (be837d78-611f-4fd3-91ad-2583e665f67b)
 Call ID: be837d78-611f-4fd3-91ad-2583e665f67b
  Args:
    relation: :hasFather
    target: Augustyn_Jozef_Czartoryski
    source: Adam_Karol_Czartoryski
  AddTriple (dabd684d-9496-4425-952e-8a405fd29340)
 Call ID: dabd684d-9496-4425-952e-8a405fd29340
  Args:
    target: Dolores_of_Bourbon-Two_Sicilies
    source: Adam_Karol_Czartoryski
    relation: :hasMother
  AddLiteral (940f744a-f9ff-4485-8a76-c21ef836a2d7)
 Call ID: 940f744a-f9ff-4485-8a76-c21ef836a2d7
  Args:
    literal_value: 1940
    relation: :hasBirthYear
    source: Adam_Karol_Czartoryski
    literal_type: xsd:integer
  AssignClass (18269fdc-39b1-4b29-a3bc-a759c8346749)
 Call ID: 18269fdc-39b1-4b29-a3bc-a759c8346749
  Args:
    source: Ludwik_Piotr_Czartoryski
    type: :Man
  AssignClass (2506b92c-f18f-4756-96e4-8ab363205b9c)
 Call ID: 2506b92c-f18f-4756-96e4-8ab363205b9c
  Args:
    type: :Person
    source: Ludwik_Piotr_Czartoryski
  AddTriple (48f3d1b2-bdd1-48fa-85ce-806ad3a836eb)
 Call ID: 48f3d1b2-bdd1-48fa-85ce-806ad3a836eb
  Args:
    relation: :hasFather
    target: Augustyn_Jozef_Czartoryski
    source: Ludwik_Piotr_Czartoryski
  AddTriple (a43cbfd1-87d5-4afa-b90a-4de2a27b7dc7)
 Call ID: a43cbfd1-87d5-4afa-b90a-4de2a27b7dc7
  Args:
    relation: :hasMother
    target: Dolores_of_Bourbon-Two_Sicilies
    source: Ludwik_Piotr_Czartoryski
  AddLiteral (37528b2e-6b08-40f7-bc56-678215c13753)
 Call ID: 37528b2e-6b08-40f7-bc56-678215c13753
  Args:
    source: Ludwik_Piotr_Czartoryski
    literal_type: xsd:integer
    literal_value: 1945
    relation: :hasBirthYear
  AddLiteral (6bcb54cd-cb15-470b-a173-c43508222583)
 Call ID: 6bcb54cd-cb15-470b-a173-c43508222583
  Args:
    relation: :hasDeathYear
    literal_value: 1946
    literal_type: xsd:integer
    source: Ludwik_Piotr_Czartoryski
  AddLiteral (9f85af11-f006-4724-a4b4-4ef37ba5968c)
 Call ID: 9f85af11-f006-4724-a4b4-4ef37ba5968c
  Args:
    literal_type: xsd:integer
    source: Augustyn_Jozef_Czartoryski
    relation: :hasDeathYear
    literal_value: 1946
  AssignClass (c47e86dd-0dcf-47ac-afd7-151368ddb894)
 Call ID: c47e86dd-0dcf-47ac-afd7-151368ddb894
  Args:
    type: :Man
    source: Carlos_Chias_Osorio
  AssignClass (dbf8d5e9-415e-4813-a8f2-358642757951)
 Call ID: dbf8d5e9-415e-4813-a8f2-358642757951
  Args:
    source: Carlos_Chias_Osorio
    type: :Person
  AddTriple (c0791a0c-7b07-497a-a67e-a8369251542d)
 Call ID: c0791a0c-7b07-497a-a67e-a8369251542d
  Args:
    relation: :hasRelation
    target: Carlos_Chias_Osorio
    source: Dolores_of_Bourbon-Two_Sicilies
  AddLiteral (25b9343c-ebfe-4005-a82f-d26e0e4281c7)
 Call ID: 25b9343c-ebfe-4005-a82f-d26e0e4281c7
  Args:
    literal_value: 1925
    relation: :hasBirthYear
    source: Carlos_Chias_Osorio
    literal_type: xsd:integer
  Finish (e0568938-2a24-4592-b49c-541342763c99)
 Call ID: e0568938-2a24-4592-b49c-541342763c99
  Args: