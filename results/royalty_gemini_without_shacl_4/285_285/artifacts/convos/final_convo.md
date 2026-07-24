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
Princess Urraca of Bourbon-Two Sicilies (Italian: Urraca Maria Isabella Carolina Aldegonda Carmela, Principessa di Borbone delle
Due Sicilie; 14 July 1913, Nymphenburg Palace, Munich, Kingdom of Bavaria – 3 May 1999, Sigmaringen, Baden-Württemberg, Germany) was a member of the House of Bourbon-Two Sicilies and a Princess of Bourbon-Two Sicilies.
Early life and family

Princess Urraca of Bourbon-Two Sicilies was born on 14 July 1913, at Nymphenburg Palace in Munich, Kingdom of Bavaria.
She was the sixth and youngest child of Prince Ferdinand Pius of Bourbon-Two Sicilies, Duke of Castro (1869–1960) and his wife Princess Maria Ludwiga Theresia of Bavaria (1872–1954).
Ferdinand Pius was the Head of the House of Bourbon-Two Sicilies and pretender to the defunct throne of the Kingdom of the Two Sicilies from 26 May 1934 to 7 January 1960.
Urraca had five older siblings, four sisters and one brother: Princess Maria Antonietta (1898–1957), Princess Maria Cristina (1899–1985), Prince Ruggiero Maria, Duke of Noto (1901–1914), Princess Barbara Maria (1902–1927), and Princess Lucia (1908–2001).
Through her father, Urraca was a granddaughter of Prince Alfonso of Bourbon-Two Sicilies, Count of Caserta (1841–1934) and his wife Princess Maria Antonietta of Bourbon-Two Sicilies (1851–1938).
Urraca was descended from King Francis I of the Two Sicilies (1777–1830) through her paternal great-grandfathers, King Ferdinand II of the Two Sicilies (1810–1859) and Prince Francis of Bourbon-Two Sicilies, Count of Trapani (1827–1892).
Through her mother, she was a granddaughter of King Ludwig III of Bavaria (1845– 1921) and his wife Archduchess Maria Theresa of Austria-Este (1849–1919).
Urraca chose not to celebrate her birthday, stating: "How can a Bourbon celebrate on the day of the Bastille's taking?
"


Adult life

As the daughter of the heir-apparent, then head of the House of Bourbon-Two Sicilies, Urraca regularly represented her family at royal and aristocratic functions and charitable events.
She attended the funeral of her great-uncle Prince Leopold of Bavaria on 3 October 1930, at St. Michael's Church in Munich.
Urraca, her mother, and her sister Lucia attended an afternoon dance tea at the Hotel Vier Jahreszeiten and the Hungarian Aid Association's Hungarian Ball in Munich in January 1934.
On 16 April 1936, Urraca attended the wedding of her first cousin Infante Alfonso of Spain, Prince of Bourbon-Two Sicilies to Princess Alicia of Bourbon-Parma at the Minoritenkirche in Vienna.
She was a guest of honor at the Austrian Armed Forces' Spring Parade in April 1936, along with Alfonso XIII of Spain, Princess Maria Anna of Bourbon-Parma, and Prince Elias of Bourbon-Parma.
Urraca attended the Baltic Red Cross Ball and the ball of Countess Adelheid Arco-Valley in the Cherubinsälen of the Hotel Vier Jahreszeiten in February 1938.
On 23 October 1957, she attended the wedding of her first cousin Princess Marie Gabrielle of Bavaria and Georg, Prince of Waldburg zu Zeil und Trauchburg in Munich.
On the night of 10 January 1957, Urraca was driving her eldest sister Maria Antonietta to her home in Lindau, Germany, when their automobile collided with a truck that had skid on ice near Winterthur, Switzerland.
Maria Antonietta was killed in the accident and Urraca was seriously injured.
Urraca was also an active supporter of Duosicilian historical societies and other royalty and nobility organizations.
Her first cousin once removed and claimant to the Duosicilian throne, Infante Carlos, Duke of Calabria, was also in attendance.
In February 1994, Urraca traveled to Gaeta where she participated in a tribute to the centenary of the death of Francis II, King of the Two Sicilies and an observation of the 133rd anniversary of the conclusion of the Siege of Gaeta which marked the victory of the Kingdom of Sardinia over Two Sicilies.
Death

Urraca died on 3 May 1999, in Sigmaringen, Baden-Württemberg, Germany.



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
  AssignClass (817c43f1-ae61-44b3-b6b6-2ea9d98d62c8)
 Call ID: 817c43f1-ae61-44b3-b6b6-2ea9d98d62c8
  Args:
    type: :Woman
    source: Princess_Urraca_of_Bourbon-Two_Sicilies
  AssignClass (d904b277-ab1d-4c31-8643-af61c94b786e)
 Call ID: d904b277-ab1d-4c31-8643-af61c94b786e
  Args:
    type: :Man
    source: Prince_Ferdinand_Pius_of_Bourbon-Two_Sicilies
  AssignClass (90fe1141-54d1-4971-bc72-52d113841395)
 Call ID: 90fe1141-54d1-4971-bc72-52d113841395
  Args:
    source: Princess_Maria_Ludwiga_Theresia_of_Bavaria
    type: :Woman
  AddLiteral (9dc59e82-9893-4595-9f91-a2ea530120c8)
 Call ID: 9dc59e82-9893-4595-9f91-a2ea530120c8
  Args:
    literal_value: 1913
    relation: :hasBirthYear
    source: Princess_Urraca_of_Bourbon-Two_Sicilies
    literal_type: xsd:positiveInteger
  AddLiteral (4a587db2-87e4-4824-82f0-d3611fa32552)
 Call ID: 4a587db2-87e4-4824-82f0-d3611fa32552
  Args:
    source: Princess_Urraca_of_Bourbon-Two_Sicilies
    literal_type: xsd:positiveInteger
    literal_value: 1999
    relation: :hasDeathYear
  AddTriple (b7701683-87bb-4181-a759-c9e51ddd2524)
 Call ID: b7701683-87bb-4181-a759-c9e51ddd2524
  Args:
    source: Princess_Urraca_of_Bourbon-Two_Sicilies
    relation: :hasFather
    target: Prince_Ferdinand_Pius_of_Bourbon-Two_Sicilies
  AddTriple (49bd0712-ea9b-44f0-b027-e5838463dc9d)
 Call ID: 49bd0712-ea9b-44f0-b027-e5838463dc9d
  Args:
    relation: :hasMother
    target: Princess_Maria_Ludwiga_Theresia_of_Bavaria
    source: Princess_Urraca_of_Bourbon-Two_Sicilies
  AssignClass (47ecf53f-69c8-4643-bfd0-6a42c2164636)
 Call ID: 47ecf53f-69c8-4643-bfd0-6a42c2164636
  Args:
    source: Princess_Maria_Antonietta
    type: :Woman
  AssignClass (4443073f-461d-446a-acd6-a20d1c5b63d0)
 Call ID: 4443073f-461d-446a-acd6-a20d1c5b63d0
  Args:
    source: Princess_Maria_Cristina
    type: :Woman
  AssignClass (2067f521-ecfc-402b-b3bc-fb66ed6a6ee8)
 Call ID: 2067f521-ecfc-402b-b3bc-fb66ed6a6ee8
  Args:
    source: Prince_Ruggiero_Maria
    type: :Man
  AssignClass (36e61a19-3298-4bcf-b667-79295728177a)
 Call ID: 36e61a19-3298-4bcf-b667-79295728177a
  Args:
    source: Princess_Barbara_Maria
    type: :Woman
  AssignClass (d5a10600-20ec-4b14-8bf0-508ff6bae335)
 Call ID: d5a10600-20ec-4b14-8bf0-508ff6bae335
  Args:
    type: :Woman
    source: Princess_Lucia
  AddTriple (28971222-f8eb-4482-a0fb-bfb3bd1263dc)
 Call ID: 28971222-f8eb-4482-a0fb-bfb3bd1263dc
  Args:
    source: Princess_Urraca_of_Bourbon-Two_Sicilies
    relation: :isSisterOf
    target: Princess_Maria_Antonietta
  AddTriple (779c2d36-ef77-430b-8123-02c116d7acbc)
 Call ID: 779c2d36-ef77-430b-8123-02c116d7acbc
  Args:
    relation: :isSisterOf
    target: Princess_Maria_Cristina
    source: Princess_Urraca_of_Bourbon-Two_Sicilies
  AddTriple (dc9d12a6-ebcc-4948-9dd7-83e2ecd78b8c)
 Call ID: dc9d12a6-ebcc-4948-9dd7-83e2ecd78b8c
  Args:
    source: Princess_Urraca_of_Bourbon-Two_Sicilies
    target: Prince_Ruggiero_Maria
    relation: :isBrotherOf
  AddTriple (cccd158c-3ac1-4092-9ece-f8e60e277e77)
 Call ID: cccd158c-3ac1-4092-9ece-f8e60e277e77
  Args:
    relation: :isSisterOf
    target: Princess_Barbara_Maria
    source: Princess_Urraca_of_Bourbon-Two_Sicilies
  AddTriple (102a7126-8431-4ba9-a1ed-2c127150a275)
 Call ID: 102a7126-8431-4ba9-a1ed-2c127150a275
  Args:
    target: Princess_Lucia
    relation: :isSisterOf
    source: Princess_Urraca_of_Bourbon-Two_Sicilies
  AssignClass (0066119f-3d2a-4912-b58f-ce549a48bd1c)
 Call ID: 0066119f-3d2a-4912-b58f-ce549a48bd1c
  Args:
    type: :Man
    source: Prince_Alfonso_of_Bourbon-Two_Sicilies
  AssignClass (2b09bac3-8900-4509-b74d-fbae6eddb674)
 Call ID: 2b09bac3-8900-4509-b74d-fbae6eddb674
  Args:
    source: Princess_Maria_Antonietta_of_Bourbon-Two_Sicilies
    type: :Woman
  AddTriple (238aeeaa-6e4e-4c31-8981-99df73b24d37)
 Call ID: 238aeeaa-6e4e-4c31-8981-99df73b24d37
  Args:
    source: Prince_Ferdinand_Pius_of_Bourbon-Two_Sicilies
    relation: :hasFather
    target: Prince_Alfonso_of_Bourbon-Two_Sicilies
  AddTriple (16feddbb-5bb6-4b2d-8d75-54d50897aed5)
 Call ID: 16feddbb-5bb6-4b2d-8d75-54d50897aed5
  Args:
    relation: :hasMother
    target: Princess_Maria_Antonietta_of_Bourbon-Two_Sicilies
    source: Prince_Ferdinand_Pius_of_Bourbon-Two_Sicilies
  AssignClass (6428fefe-f148-44d3-ba4a-7e47ed9703a5)
 Call ID: 6428fefe-f148-44d3-ba4a-7e47ed9703a5
  Args:
    type: :Man
    source: King_Ludwig_III_of_Bavaria
  AssignClass (5146acbc-930c-4922-8be5-0c901735f657)
 Call ID: 5146acbc-930c-4922-8be5-0c901735f657
  Args:
    source: Archduchess_Maria_Theresa_of_Austria-Este
    type: :Woman
  AddTriple (7dcf3525-54b4-45de-8bb7-02f52a0371d4)
 Call ID: 7dcf3525-54b4-45de-8bb7-02f52a0371d4
  Args:
    relation: :hasFather
    target: King_Ludwig_III_of_Bavaria
    source: Princess_Maria_Ludwiga_Theresia_of_Bavaria
  AddTriple (dcc38a54-d63b-4d49-8d28-6420fc30c29d)
 Call ID: dcc38a54-d63b-4d49-8d28-6420fc30c29d
  Args:
    relation: :hasMother
    target: Archduchess_Maria_Theresa_of_Austria-Este
    source: Princess_Maria_Ludwiga_Theresia_of_Bavaria
  Finish (b2293528-6eb6-4ee5-ae67-6cfca169e51b)
 Call ID: b2293528-6eb6-4ee5-ae67-6cfca169e51b
  Args: