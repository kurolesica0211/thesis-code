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
  AssignClass (6e438032-a1cf-45e6-8598-117daa0ff538)
 Call ID: 6e438032-a1cf-45e6-8598-117daa0ff538
  Args:
    source: Urraca_of_Bourbon-Two_Sicilies
    type: :Woman
  AssignClass (5dc0496f-f279-44a8-bed9-38ad8c395fc2)
 Call ID: 5dc0496f-f279-44a8-bed9-38ad8c395fc2
  Args:
    source: Urraca_of_Bourbon-Two_Sicilies
    type: :Person
  AddLiteral (e7625a38-ce96-4aae-a2fa-87c0f62ad147)
 Call ID: e7625a38-ce96-4aae-a2fa-87c0f62ad147
  Args:
    literal_type: xsd:integer
    source: Urraca_of_Bourbon-Two_Sicilies
    literal_value: 1913
    relation: :hasBirthYear
  AddLiteral (6e19440c-5808-4533-9956-ab645cce793f)
 Call ID: 6e19440c-5808-4533-9956-ab645cce793f
  Args:
    source: Urraca_of_Bourbon-Two_Sicilies
    literal_type: xsd:integer
    literal_value: 1999
    relation: :hasDeathYear
  AssignClass (adf7cd5d-95e7-470e-89c7-d82d45248c62)
 Call ID: adf7cd5d-95e7-470e-89c7-d82d45248c62
  Args:
    source: Ferdinand_Pius_of_Bourbon-Two_Sicilies
    type: :Man
  AssignClass (6b02995e-da2c-4bd2-932a-4fb73f38c4e6)
 Call ID: 6b02995e-da2c-4bd2-932a-4fb73f38c4e6
  Args:
    source: Ferdinand_Pius_of_Bourbon-Two_Sicilies
    type: :Person
  AssignClass (4ace9469-12c9-4533-b024-fe2877f36b5a)
 Call ID: 4ace9469-12c9-4533-b024-fe2877f36b5a
  Args:
    source: Ferdinand_Pius_of_Bourbon-Two_Sicilies
    type: :Ancestor
  AssignClass (01ac1ef0-a4f9-4808-96d8-affc1767424b)
 Call ID: 01ac1ef0-a4f9-4808-96d8-affc1767424b
  Args:
    source: Maria_Ludwiga_Theresia_of_Bavaria
    type: :Woman
  AssignClass (7211ddf7-90e0-4d39-b4b3-8f5d6fa531a1)
 Call ID: 7211ddf7-90e0-4d39-b4b3-8f5d6fa531a1
  Args:
    source: Maria_Ludwiga_Theresia_of_Bavaria
    type: :Person
  AssignClass (e8082eb6-9a03-4503-a073-80ef9a78bb99)
 Call ID: e8082eb6-9a03-4503-a073-80ef9a78bb99
  Args:
    source: Maria_Ludwiga_Theresia_of_Bavaria
    type: :Ancestor
  AddTriple (0153f7ff-811b-4f21-9161-76eb8ad38bff)
 Call ID: 0153f7ff-811b-4f21-9161-76eb8ad38bff
  Args:
    relation: :hasFather
    target: Ferdinand_Pius_of_Bourbon-Two_Sicilies
    source: Urraca_of_Bourbon-Two_Sicilies
  AddTriple (fcbfa709-9cd1-4d65-946b-978a2f810c47)
 Call ID: fcbfa709-9cd1-4d65-946b-978a2f810c47
  Args:
    target: Maria_Ludwiga_Theresia_of_Bavaria
    source: Urraca_of_Bourbon-Two_Sicilies
    relation: :hasMother
  AssignClass (c4986c23-161c-4bdd-9a05-91ee3da79d67)
 Call ID: c4986c23-161c-4bdd-9a05-91ee3da79d67
  Args:
    source: Maria_Antonietta_of_Bourbon-Two_Sicilies_1898
    type: :Woman
  AssignClass (cedaf51e-c33c-4567-984f-6df01b0dc413)
 Call ID: cedaf51e-c33c-4567-984f-6df01b0dc413
  Args:
    source: Maria_Antonietta_of_Bourbon-Two_Sicilies_1898
    type: :Person
  AssignClass (5fa41295-3d3a-487d-9095-ede2972ff978)
 Call ID: 5fa41295-3d3a-487d-9095-ede2972ff978
  Args:
    source: Maria_Cristina_of_Bourbon-Two_Sicilies
    type: :Woman
  AssignClass (0d699e1e-eaea-46ea-a391-8dd740aa550d)
 Call ID: 0d699e1e-eaea-46ea-a391-8dd740aa550d
  Args:
    source: Maria_Cristina_of_Bourbon-Two_Sicilies
    type: :Person
  AssignClass (0e1dba72-a3b6-400d-88f4-5803d3c72cae)
 Call ID: 0e1dba72-a3b6-400d-88f4-5803d3c72cae
  Args:
    source: Ruggiero_Maria_of_Bourbon-Two_Sicilies
    type: :Man
  AssignClass (ed499baf-1918-4a21-9243-63e9aac8d6cb)
 Call ID: ed499baf-1918-4a21-9243-63e9aac8d6cb
  Args:
    source: Ruggiero_Maria_of_Bourbon-Two_Sicilies
    type: :Person
  AssignClass (88196c26-6b0c-4997-9138-c8b571eb6b8d)
 Call ID: 88196c26-6b0c-4997-9138-c8b571eb6b8d
  Args:
    source: Barbara_Maria_of_Bourbon-Two_Sicilies
    type: :Woman
  AssignClass (f42c5bec-841b-4eb2-828d-0a9f71118b1a)
 Call ID: f42c5bec-841b-4eb2-828d-0a9f71118b1a
  Args:
    source: Barbara_Maria_of_Bourbon-Two_Sicilies
    type: :Person
  AssignClass (31d37b6b-585b-484c-b075-a3c9bc775a44)
 Call ID: 31d37b6b-585b-484c-b075-a3c9bc775a44
  Args:
    source: Lucia_of_Bourbon-Two_Sicilies
    type: :Woman
  AssignClass (47666c87-fe40-4721-a070-585c01805510)
 Call ID: 47666c87-fe40-4721-a070-585c01805510
  Args:
    source: Lucia_of_Bourbon-Two_Sicilies
    type: :Person
  AddTriple (dce989cf-5ac0-43ff-a831-972e467a763d)
 Call ID: dce989cf-5ac0-43ff-a831-972e467a763d
  Args:
    source: Urraca_of_Bourbon-Two_Sicilies
    target: Maria_Antonietta_of_Bourbon-Two_Sicilies_1898
    relation: :isSiblingOf
  AddTriple (cbf7198a-4cd7-428f-ba98-071d67ed409a)
 Call ID: cbf7198a-4cd7-428f-ba98-071d67ed409a
  Args:
    target: Maria_Cristina_of_Bourbon-Two_Sicilies
    source: Urraca_of_Bourbon-Two_Sicilies
    relation: :isSiblingOf
  AddTriple (baa28a63-9bf7-4472-b7fb-5476063e2c57)
 Call ID: baa28a63-9bf7-4472-b7fb-5476063e2c57
  Args:
    relation: :isSiblingOf
    source: Urraca_of_Bourbon-Two_Sicilies
    target: Ruggiero_Maria_of_Bourbon-Two_Sicilies
  AddTriple (1cd52a34-aaed-4779-b288-4bb3dc7dd27e)
 Call ID: 1cd52a34-aaed-4779-b288-4bb3dc7dd27e
  Args:
    relation: :isSiblingOf
    source: Urraca_of_Bourbon-Two_Sicilies
    target: Barbara_Maria_of_Bourbon-Two_Sicilies
  AddTriple (209c34b2-9115-4a58-af85-495602070751)
 Call ID: 209c34b2-9115-4a58-af85-495602070751
  Args:
    relation: :isSiblingOf
    source: Urraca_of_Bourbon-Two_Sicilies
    target: Lucia_of_Bourbon-Two_Sicilies
  AssignClass (8f11b800-b051-4a23-b319-3f637f166e45)
 Call ID: 8f11b800-b051-4a23-b319-3f637f166e45
  Args:
    source: Alfonso_of_Bourbon-Two_Sicilies_Count_of_Caserta
    type: :Man
  AssignClass (0aeac9a6-d1ce-4d04-b1a7-6a66758c1caf)
 Call ID: 0aeac9a6-d1ce-4d04-b1a7-6a66758c1caf
  Args:
    source: Alfonso_of_Bourbon-Two_Sicilies_Count_of_Caserta
    type: :Ancestor
  AssignClass (ba394a40-cfa0-419e-97e4-97aeeb4e8b76)
 Call ID: ba394a40-cfa0-419e-97e4-97aeeb4e8b76
  Args:
    source: Alfonso_of_Bourbon-Two_Sicilies_Count_of_Caserta
    type: :Person
  AssignClass (54902a4e-bc2c-403b-8657-077923352857)
 Call ID: 54902a4e-bc2c-403b-8657-077923352857
  Args:
    source: Maria_Antonietta_of_Bourbon-Two_Sicilies_1851
    type: :Woman
  AssignClass (f17e3177-fffc-464f-9bac-09f7400ef078)
 Call ID: f17e3177-fffc-464f-9bac-09f7400ef078
  Args:
    source: Maria_Antonietta_of_Bourbon-Two_Sicilies_1851
    type: :Ancestor
  AssignClass (d0e85af7-fc37-4ec6-8c9a-fb9e9e157d5f)
 Call ID: d0e85af7-fc37-4ec6-8c9a-fb9e9e157d5f
  Args:
    source: Maria_Antonietta_of_Bourbon-Two_Sicilies_1851
    type: :Person
  AddTriple (a9d5b1a8-1be8-4b80-b574-976190048a47)
 Call ID: a9d5b1a8-1be8-4b80-b574-976190048a47
  Args:
    relation: :hasFather
    target: Alfonso_of_Bourbon-Two_Sicilies_Count_of_Caserta
    source: Ferdinand_Pius_of_Bourbon-Two_Sicilies
  AddTriple (505d0a9c-8e02-4360-afe4-e389df85d314)
 Call ID: 505d0a9c-8e02-4360-afe4-e389df85d314
  Args:
    relation: :hasMother
    target: Maria_Antonietta_of_Bourbon-Two_Sicilies_1851
    source: Ferdinand_Pius_of_Bourbon-Two_Sicilies
  AssignClass (93c5215b-3a80-4ef3-b7e8-7a580daed5bb)
 Call ID: 93c5215b-3a80-4ef3-b7e8-7a580daed5bb
  Args:
    source: Ludwig_III_of_Bavaria
    type: :Man
  AssignClass (ed0262cd-2d0f-429c-846e-fba838ea574f)
 Call ID: ed0262cd-2d0f-429c-846e-fba838ea574f
  Args:
    source: Ludwig_III_of_Bavaria
    type: :Ancestor
  AssignClass (5fa51c03-6f59-4042-ad30-1e1b50415f4e)
 Call ID: 5fa51c03-6f59-4042-ad30-1e1b50415f4e
  Args:
    source: Ludwig_III_of_Bavaria
    type: :Person
  AssignClass (b09c0d18-b596-4810-81a8-ffea2e7ef008)
 Call ID: b09c0d18-b596-4810-81a8-ffea2e7ef008
  Args:
    source: Maria_Theresa_of_Austria-Este
    type: :Woman
  AssignClass (0d4b48ef-d739-4ab1-907c-785e5930ebac)
 Call ID: 0d4b48ef-d739-4ab1-907c-785e5930ebac
  Args:
    source: Maria_Theresa_of_Austria-Este
    type: :Ancestor
  AssignClass (730f7fe7-6e2b-45af-b578-0417ad0f9d3d)
 Call ID: 730f7fe7-6e2b-45af-b578-0417ad0f9d3d
  Args:
    source: Maria_Theresa_of_Austria-Este
    type: :Person
  AddTriple (28e1ce6c-f847-451f-97cf-769b38074e03)
 Call ID: 28e1ce6c-f847-451f-97cf-769b38074e03
  Args:
    source: Maria_Ludwiga_Theresia_of_Bavaria
    target: Ludwig_III_of_Bavaria
    relation: :hasFather
  AddTriple (6d36ae2e-1a27-45d5-93a0-03029536b78d)
 Call ID: 6d36ae2e-1a27-45d5-93a0-03029536b78d
  Args:
    relation: :hasMother
    target: Maria_Theresa_of_Austria-Este
    source: Maria_Ludwiga_Theresia_of_Bavaria
  Finish (05990e6c-8f36-49c2-a956-3db526fe0065)
 Call ID: 05990e6c-8f36-49c2-a956-3db526fe0065
  Args: