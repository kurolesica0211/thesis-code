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
  AssignClass (6a45e8c4-e18a-4341-8fbf-1bbdfaf838d6)
 Call ID: 6a45e8c4-e18a-4341-8fbf-1bbdfaf838d6
  Args:
    source: Princess Urraca of Bourbon-Two Sicilies
    type: :Woman
  AssignClass (384ce296-9990-4183-9ba6-6fc2ebc18b1b)
 Call ID: 384ce296-9990-4183-9ba6-6fc2ebc18b1b
  Args:
    type: :Person
    source: Princess Urraca of Bourbon-Two Sicilies
  AddLiteral (ca9fb639-cc04-40a7-ab7d-58faaa9aa850)
 Call ID: ca9fb639-cc04-40a7-ab7d-58faaa9aa850
  Args:
    relation: :hasBirthYear
    literal_value: 1913
    source: Princess Urraca of Bourbon-Two Sicilies
    literal_type: xsd:integer
  AddLiteral (2944720d-00dd-455d-a0a1-179c382d960f)
 Call ID: 2944720d-00dd-455d-a0a1-179c382d960f
  Args:
    literal_type: xsd:integer
    source: Princess Urraca of Bourbon-Two Sicilies
    literal_value: 1999
    relation: :hasDeathYear
  AssignClass (6351e03c-6e2e-48c8-8fe3-8c07de36eb85)
 Call ID: 6351e03c-6e2e-48c8-8fe3-8c07de36eb85
  Args:
    source: Prince Ferdinand Pius of Bourbon-Two Sicilies
    type: :Man
  AssignClass (abe52e30-05ff-4be3-aae9-2f9d3dee9443)
 Call ID: abe52e30-05ff-4be3-aae9-2f9d3dee9443
  Args:
    source: Prince Ferdinand Pius of Bourbon-Two Sicilies
    type: :Person
  AssignClass (65a37b01-077b-4bf4-8b5b-77960a60ce8f)
 Call ID: 65a37b01-077b-4bf4-8b5b-77960a60ce8f
  Args:
    source: Prince Ferdinand Pius of Bourbon-Two Sicilies
    type: :Ancestor
  AddLiteral (033952ce-d3e6-4859-9285-219247631d40)
 Call ID: 033952ce-d3e6-4859-9285-219247631d40
  Args:
    source: Prince Ferdinand Pius of Bourbon-Two Sicilies
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1869
  AddLiteral (5612088c-15fd-4983-9c96-df55a6d6581d)
 Call ID: 5612088c-15fd-4983-9c96-df55a6d6581d
  Args:
    relation: :hasDeathYear
    literal_value: 1960
    source: Prince Ferdinand Pius of Bourbon-Two Sicilies
    literal_type: xsd:integer
  AssignClass (1e248378-f9bf-4240-aad0-55c5ef509d16)
 Call ID: 1e248378-f9bf-4240-aad0-55c5ef509d16
  Args:
    type: :Woman
    source: Princess Maria Ludwiga Theresia of Bavaria
  AssignClass (2cf88bfd-ec60-4a68-9174-47d0fcd7401c)
 Call ID: 2cf88bfd-ec60-4a68-9174-47d0fcd7401c
  Args:
    source: Princess Maria Ludwiga Theresia of Bavaria
    type: :Person
  AssignClass (e368627e-09e0-4311-b67c-b5a140cc6735)
 Call ID: e368627e-09e0-4311-b67c-b5a140cc6735
  Args:
    source: Princess Maria Ludwiga Theresia of Bavaria
    type: :Ancestor
  AddLiteral (c93b173b-24f4-46e5-9e8b-fb6b16b80669)
 Call ID: c93b173b-24f4-46e5-9e8b-fb6b16b80669
  Args:
    literal_type: xsd:integer
    source: Princess Maria Ludwiga Theresia of Bavaria
    literal_value: 1872
    relation: :hasBirthYear
  AddLiteral (80120c02-db56-45bd-823a-37cac3481ad3)
 Call ID: 80120c02-db56-45bd-823a-37cac3481ad3
  Args:
    source: Princess Maria Ludwiga Theresia of Bavaria
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1954
  AddTriple (d8235e00-153c-455b-a9b8-a8e5a7bc0b3e)
 Call ID: d8235e00-153c-455b-a9b8-a8e5a7bc0b3e
  Args:
    source: Princess Urraca of Bourbon-Two Sicilies
    target: Prince Ferdinand Pius of Bourbon-Two Sicilies
    relation: :hasFather
  AddTriple (6f0aeed2-111c-4acd-9e3f-1fe652f4172b)
 Call ID: 6f0aeed2-111c-4acd-9e3f-1fe652f4172b
  Args:
    relation: :hasMother
    source: Princess Urraca of Bourbon-Two Sicilies
    target: Princess Maria Ludwiga Theresia of Bavaria
  AssignClass (32d7f379-e381-4173-98dd-94ae5be19081)
 Call ID: 32d7f379-e381-4173-98dd-94ae5be19081
  Args:
    type: :Woman
    source: Princess Maria Antonietta
  AssignClass (46a5e9cd-5605-4838-835d-ba3924dd45cd)
 Call ID: 46a5e9cd-5605-4838-835d-ba3924dd45cd
  Args:
    type: :Person
    source: Princess Maria Antonietta
  AssignClass (64f768b3-48cb-48e8-abe7-e1d93b48acdd)
 Call ID: 64f768b3-48cb-48e8-abe7-e1d93b48acdd
  Args:
    source: Princess Maria Cristina
    type: :Woman
  AssignClass (9badebaf-5181-4efa-8545-ed89ab78174a)
 Call ID: 9badebaf-5181-4efa-8545-ed89ab78174a
  Args:
    source: Princess Maria Cristina
    type: :Person
  AssignClass (4932faa3-f727-4a95-b865-c87f982a3919)
 Call ID: 4932faa3-f727-4a95-b865-c87f982a3919
  Args:
    source: Prince Ruggiero Maria
    type: :Man
  AssignClass (a6c46bb2-0724-45e8-a612-4b8c97f8a8ee)
 Call ID: a6c46bb2-0724-45e8-a612-4b8c97f8a8ee
  Args:
    type: :Person
    source: Prince Ruggiero Maria
  AssignClass (83f5b5a4-d23f-44c1-91c4-2ce3ea1c6db9)
 Call ID: 83f5b5a4-d23f-44c1-91c4-2ce3ea1c6db9
  Args:
    source: Princess Barbara Maria
    type: :Woman
  AssignClass (eff178ac-f3bc-48b4-aaac-c347e1213e43)
 Call ID: eff178ac-f3bc-48b4-aaac-c347e1213e43
  Args:
    type: :Person
    source: Princess Barbara Maria
  AssignClass (764f5049-deb7-453b-bd77-21dabd6fd6c2)
 Call ID: 764f5049-deb7-453b-bd77-21dabd6fd6c2
  Args:
    type: :Woman
    source: Princess Lucia
  AssignClass (f44ea4df-48ff-42ea-85a4-7b21060888e6)
 Call ID: f44ea4df-48ff-42ea-85a4-7b21060888e6
  Args:
    type: :Person
    source: Princess Lucia
  AddTriple (ac396f31-02d2-4b30-b843-e027b93aab80)
 Call ID: ac396f31-02d2-4b30-b843-e027b93aab80
  Args:
    source: Princess Urraca of Bourbon-Two Sicilies
    target: Princess Maria Antonietta
    relation: :isSiblingOf
  AddTriple (81c0b30d-e2f4-40c7-b4ec-34c14d9ba340)
 Call ID: 81c0b30d-e2f4-40c7-b4ec-34c14d9ba340
  Args:
    relation: :isSiblingOf
    source: Princess Urraca of Bourbon-Two Sicilies
    target: Princess Maria Cristina
  AddTriple (b3f6b2cb-5af6-424b-8704-b0b8ed54b369)
 Call ID: b3f6b2cb-5af6-424b-8704-b0b8ed54b369
  Args:
    relation: :isSiblingOf
    source: Princess Urraca of Bourbon-Two Sicilies
    target: Prince Ruggiero Maria
  AddTriple (c2c05b36-c8f4-4ea4-aaf2-615a851a773c)
 Call ID: c2c05b36-c8f4-4ea4-aaf2-615a851a773c
  Args:
    source: Princess Urraca of Bourbon-Two Sicilies
    target: Princess Barbara Maria
    relation: :isSiblingOf
  AddTriple (9b7a72bb-cde1-4c5b-8670-d37c02c7ece0)
 Call ID: 9b7a72bb-cde1-4c5b-8670-d37c02c7ece0
  Args:
    source: Princess Urraca of Bourbon-Two Sicilies
    target: Princess Lucia
    relation: :isSiblingOf
  AddLiteral (05402802-2da8-4a2a-8bb3-f81065f254ef)
 Call ID: 05402802-2da8-4a2a-8bb3-f81065f254ef
  Args:
    literal_value: 1898
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Princess Maria Antonietta
  AddLiteral (37b56775-f550-412c-a9fb-83aa849f735e)
 Call ID: 37b56775-f550-412c-a9fb-83aa849f735e
  Args:
    literal_type: xsd:integer
    source: Princess Maria Antonietta
    literal_value: 1957
    relation: :hasDeathYear
  AddLiteral (070e3e29-2e53-4a10-8599-098652940ebb)
 Call ID: 070e3e29-2e53-4a10-8599-098652940ebb
  Args:
    relation: :hasBirthYear
    literal_value: 1899
    source: Princess Maria Cristina
    literal_type: xsd:integer
  AddLiteral (2e07420b-c499-4ba0-92e8-032f43c73deb)
 Call ID: 2e07420b-c499-4ba0-92e8-032f43c73deb
  Args:
    literal_type: xsd:integer
    source: Princess Maria Cristina
    literal_value: 1985
    relation: :hasDeathYear
  AddLiteral (9453014c-54dc-4b55-98e9-d7049484700d)
 Call ID: 9453014c-54dc-4b55-98e9-d7049484700d
  Args:
    literal_value: 1901
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Prince Ruggiero Maria
  AddLiteral (83a09c6a-8933-42f3-8aa9-d1255eca1f5b)
 Call ID: 83a09c6a-8933-42f3-8aa9-d1255eca1f5b
  Args:
    source: Prince Ruggiero Maria
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1914
  AddLiteral (159aac01-fc8f-40fe-bd2c-5496dd88e9e1)
 Call ID: 159aac01-fc8f-40fe-bd2c-5496dd88e9e1
  Args:
    relation: :hasBirthYear
    literal_value: 1902
    source: Princess Barbara Maria
    literal_type: xsd:integer
  AddLiteral (274c6fb1-d679-4fd6-a11d-7f923680bd3a)
 Call ID: 274c6fb1-d679-4fd6-a11d-7f923680bd3a
  Args:
    literal_value: 1927
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: Princess Barbara Maria
  AddLiteral (86bd90f9-1d68-4ced-b2e2-cc747a407da5)
 Call ID: 86bd90f9-1d68-4ced-b2e2-cc747a407da5
  Args:
    relation: :hasBirthYear
    literal_value: 1908
    source: Princess Lucia
    literal_type: xsd:integer
  AddLiteral (d1e04075-5201-4346-843e-3d67f6755600)
 Call ID: d1e04075-5201-4346-843e-3d67f6755600
  Args:
    literal_type: xsd:integer
    source: Princess Lucia
    literal_value: 2001
    relation: :hasDeathYear
  Finish (5dfa593b-4c3f-4189-9816-b490aae9494f)
 Call ID: 5dfa593b-4c3f-4189-9816-b490aae9494f
  Args: