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
  AssignClass (da7f3524-1ac8-4041-8d00-5e94e6e96a97)
 Call ID: da7f3524-1ac8-4041-8d00-5e94e6e96a97
  Args:
    type: :Woman
    source: Urraca_of_Bourbon-Two_Sicilies
  AssignClass (a2ea0489-339d-40aa-8280-197ee69ce3ae)
 Call ID: a2ea0489-339d-40aa-8280-197ee69ce3ae
  Args:
    type: :Person
    source: Urraca_of_Bourbon-Two_Sicilies
  AddLiteral (75e96beb-3dfd-4fbc-bdeb-9c586e484d71)
 Call ID: 75e96beb-3dfd-4fbc-bdeb-9c586e484d71
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Urraca_of_Bourbon-Two_Sicilies
    literal_value: 1913
  AddLiteral (714854ed-3fb2-4e0e-aa16-a10ac766062a)
 Call ID: 714854ed-3fb2-4e0e-aa16-a10ac766062a
  Args:
    source: Urraca_of_Bourbon-Two_Sicilies
    literal_type: xsd:integer
    literal_value: 1999
    relation: :hasDeathYear
  AssignClass (575e2eba-3f56-4e4f-9379-2559347a51d8)
 Call ID: 575e2eba-3f56-4e4f-9379-2559347a51d8
  Args:
    type: :Man
    source: Ferdinand_Pius_of_Bourbon-Two_Sicilies
  AssignClass (e94fa3b8-2842-42db-972c-3fb678761640)
 Call ID: e94fa3b8-2842-42db-972c-3fb678761640
  Args:
    source: Ferdinand_Pius_of_Bourbon-Two_Sicilies
    type: :Person
  AddLiteral (ef708138-305d-4d73-87a0-6e6ff617d5e5)
 Call ID: ef708138-305d-4d73-87a0-6e6ff617d5e5
  Args:
    relation: :hasBirthYear
    literal_value: 1869
    source: Ferdinand_Pius_of_Bourbon-Two_Sicilies
    literal_type: xsd:integer
  AddLiteral (dd703930-c669-4c49-aef2-0783a369c92d)
 Call ID: dd703930-c669-4c49-aef2-0783a369c92d
  Args:
    relation: :hasDeathYear
    literal_value: 1960
    source: Ferdinand_Pius_of_Bourbon-Two_Sicilies
    literal_type: xsd:integer
  AssignClass (3cae748a-6232-4063-a42e-6afe9fadcf40)
 Call ID: 3cae748a-6232-4063-a42e-6afe9fadcf40
  Args:
    source: Maria_Ludwiga_Theresia_of_Bavaria
    type: :Woman
  AssignClass (5c9add69-76ee-47a4-867d-021c89884cc2)
 Call ID: 5c9add69-76ee-47a4-867d-021c89884cc2
  Args:
    type: :Person
    source: Maria_Ludwiga_Theresia_of_Bavaria
  AddLiteral (ade7611f-a83a-4951-97c1-e5c373fa1529)
 Call ID: ade7611f-a83a-4951-97c1-e5c373fa1529
  Args:
    relation: :hasBirthYear
    source: Maria_Ludwiga_Theresia_of_Bavaria
    literal_type: xsd:integer
    literal_value: 1872
  AddLiteral (68b92b98-7b64-4cff-abfa-62bd4db0653e)
 Call ID: 68b92b98-7b64-4cff-abfa-62bd4db0653e
  Args:
    relation: :hasDeathYear
    literal_value: 1954
    literal_type: xsd:integer
    source: Maria_Ludwiga_Theresia_of_Bavaria
  AddTriple (ed04b481-51cf-456d-8e41-6654cba75c30)
 Call ID: ed04b481-51cf-456d-8e41-6654cba75c30
  Args:
    target: Ferdinand_Pius_of_Bourbon-Two_Sicilies
    source: Urraca_of_Bourbon-Two_Sicilies
    relation: :hasFather
  AddTriple (b5f42692-9d2b-4275-86c5-0ee08a3d2e50)
 Call ID: b5f42692-9d2b-4275-86c5-0ee08a3d2e50
  Args:
    relation: :hasMother
    target: Maria_Ludwiga_Theresia_of_Bavaria
    source: Urraca_of_Bourbon-Two_Sicilies
  AssignClass (b9575d48-4a5a-4348-be88-47adf3819c37)
 Call ID: b9575d48-4a5a-4348-be88-47adf3819c37
  Args:
    type: :Woman
    source: Maria_Antonietta_of_Bourbon-Two_Sicilies_1898
  AssignClass (abf0bcc9-5b15-4365-9181-bf74505f8d73)
 Call ID: abf0bcc9-5b15-4365-9181-bf74505f8d73
  Args:
    type: :Person
    source: Maria_Antonietta_of_Bourbon-Two_Sicilies_1898
  AddTriple (78c6b307-d407-417a-8c3d-893173a1e7c7)
 Call ID: 78c6b307-d407-417a-8c3d-893173a1e7c7
  Args:
    relation: :hasSister
    source: Urraca_of_Bourbon-Two_Sicilies
    target: Maria_Antonietta_of_Bourbon-Two_Sicilies_1898
  AssignClass (cd28fc3c-7b90-46c7-b448-d531a078fb82)
 Call ID: cd28fc3c-7b90-46c7-b448-d531a078fb82
  Args:
    type: :Woman
    source: Maria_Cristina_of_Bourbon-Two_Sicilies
  AssignClass (5a627d56-db09-4d89-9599-ef3851a549cd)
 Call ID: 5a627d56-db09-4d89-9599-ef3851a549cd
  Args:
    type: :Person
    source: Maria_Cristina_of_Bourbon-Two_Sicilies
  AddTriple (02a1a7f3-5edb-474f-8e81-ec9a43c7e734)
 Call ID: 02a1a7f3-5edb-474f-8e81-ec9a43c7e734
  Args:
    target: Maria_Cristina_of_Bourbon-Two_Sicilies
    source: Urraca_of_Bourbon-Two_Sicilies
    relation: :hasSister
  AssignClass (81e64175-6600-40b2-9298-eb723974b3b6)
 Call ID: 81e64175-6600-40b2-9298-eb723974b3b6
  Args:
    source: Ruggiero_Maria_of_Bourbon-Two_Sicilies
    type: :Man
  AssignClass (4ed75f30-05eb-4d40-9ac0-a9aac452ef40)
 Call ID: 4ed75f30-05eb-4d40-9ac0-a9aac452ef40
  Args:
    type: :Person
    source: Ruggiero_Maria_of_Bourbon-Two_Sicilies
  AddTriple (7f4070d9-f039-4227-b483-7b5fb3996650)
 Call ID: 7f4070d9-f039-4227-b483-7b5fb3996650
  Args:
    relation: :hasBrother
    source: Urraca_of_Bourbon-Two_Sicilies
    target: Ruggiero_Maria_of_Bourbon-Two_Sicilies
  AssignClass (677d2894-e621-45ce-b0d7-ef6490c47cea)
 Call ID: 677d2894-e621-45ce-b0d7-ef6490c47cea
  Args:
    source: Barbara_Maria_of_Bourbon-Two_Sicilies
    type: :Woman
  AssignClass (733cebca-9c70-437f-9988-eb62bf1d9afa)
 Call ID: 733cebca-9c70-437f-9988-eb62bf1d9afa
  Args:
    type: :Person
    source: Barbara_Maria_of_Bourbon-Two_Sicilies
  AddTriple (fb858fe7-9a2c-4755-97d3-958c8d89b08a)
 Call ID: fb858fe7-9a2c-4755-97d3-958c8d89b08a
  Args:
    source: Urraca_of_Bourbon-Two_Sicilies
    target: Barbara_Maria_of_Bourbon-Two_Sicilies
    relation: :hasSister
  AssignClass (4209b028-b462-4534-ae2c-6398fc59ac86)
 Call ID: 4209b028-b462-4534-ae2c-6398fc59ac86
  Args:
    source: Lucia_of_Bourbon-Two_Sicilies
    type: :Woman
  AssignClass (c52bd852-c198-41ea-b0ce-0055caee4c35)
 Call ID: c52bd852-c198-41ea-b0ce-0055caee4c35
  Args:
    type: :Person
    source: Lucia_of_Bourbon-Two_Sicilies
  AddTriple (c8b5ae06-d3e6-4172-bad7-154faccf5956)
 Call ID: c8b5ae06-d3e6-4172-bad7-154faccf5956
  Args:
    source: Urraca_of_Bourbon-Two_Sicilies
    target: Lucia_of_Bourbon-Two_Sicilies
    relation: :hasSister
  Finish (a2b27c46-6124-4ace-946e-c70ae83b4936)
 Call ID: a2b27c46-6124-4ace-946e-c70ae83b4936
  Args: