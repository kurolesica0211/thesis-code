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
Prince Wilhelm Friedrich Franz Joseph Christian Olaf of Prussia (4 July 1906 – 26 May 1940) was the eldest child of Wilhelm, German Crown Prince, and Duchess Cecilie of Mecklenburg-Schwerin.
At his birth, he was second in line to the German throne and was expected to succeed to the throne after the deaths of his grandfather, Emperor Wilhelm II, and his father, Crown Prince Wilhelm, although both outlived him.
In any case, the German monarchy was abolished in 1918 when he was twelve.
He later enlisted to serve in the Wehrmacht and died in active service during the German invasion of France in 1940.
Early life and childhood

Wilhelm was born on 4 July 1906 at the Hohenzollern family's private summer residence, Marmorpalais, or Marble Palace, near Potsdam, where his parents were residing until their own home, Schloss Cecilienhof, could be completed.
His father was Crown Prince Wilhelm, the eldest son and heir to the German Emperor, Wilhelm II.
His mother was Duchess Cecilie of Mecklenburg-Schwerin.
Emperor Franz Joseph of Austria was one of the Prince's godfathers.
The selection of a nanny for Wilhelm and his younger brother, Louis Ferdinand (born in 1907) caused considerable distress within the family.
On his tenth birthday in 1916, Wilhelm was made a lieutenant in the 1st Guards Regiment, and was given the Order of the Black Eagle by his grandfather.
Two years later, when he was twelve, the German monarchy was abolished.
Wilhelm and his family remained in Germany, though his grandfather, the former Emperor, went into exile in the Netherlands.
The former Crown Prince and his family remained in Potsdam, where Wilhelm and his younger brothers attended the local gymnasium.
After graduating from secondary school, Wilhelm went on to study at the Universities of Königsberg, Munich and Bonn.
In 1926, while a student at the University of Bonn, Wilhelm joined the Borussia Corps, a student organization of which his father, grandfather, and other members of the Prussian royal family were members.
Marriage and children

While a student at Bonn, Wilhelm fell in love with a fellow student, Dorothea von Salviati (10 September 1907 – 7 May 1972).
Wilhelm's grandfather did not approve of the marriage of the heir apparent in line to the German throne to a member of the minor nobility.
Wilhelm told his grandson, "Remember, there is every possible form of horse.
However, Wilhelm was determined to marry Dorothea.
Wilhelm and Dorothea married on 3 June 1933 in Bonn.
In 1940, the ex-Emperor recognized the marriage as dynastic and the girls were accorded the style of Princesses of Prussia (although their father was not restored to his former place in the putative line of succession, his renunciation of his rights remaining valid):


Military services

During the Weimar Republic, Wilhelm inadvertently caused a public scandal by attending Army manoeuvres in the uniform of the old Imperial First Foot Guards without first seeking government approval.
The Oster conspiracy of 1938 sought to restore Wilhelm to the throne.
At the beginning of World War II, Wilhelm was among a number of princes from the former German monarchies who enlisted to serve in the Wehrmacht, the unified armed forces of Germany.
Death and reaction

In May 1940, Wilhelm took part in the invasion of France.
Shortly after Wilhelm's death, a decree known as the Prinzenerlaß, or Prince's Decree, was issued, barring all members of the former German royal houses from service in the Wehrmacht.



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
  AssignClass (93119010-13a6-4cd5-a54d-c8601fc6a857)
 Call ID: 93119010-13a6-4cd5-a54d-c8601fc6a857
  Args:
    source: Wilhelm_of_Prussia
    type: :Man
  AssignClass (02ee94b3-3512-41a6-bdd6-7c06d487c495)
 Call ID: 02ee94b3-3512-41a6-bdd6-7c06d487c495
  Args:
    type: :Person
    source: Wilhelm_of_Prussia
  AddLiteral (f65783e7-57a4-455b-9da0-1f27eaa67003)
 Call ID: f65783e7-57a4-455b-9da0-1f27eaa67003
  Args:
    literal_value: 1906
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Wilhelm_of_Prussia
  AddLiteral (519a01cb-896d-4397-a3e5-1beec09bf20c)
 Call ID: 519a01cb-896d-4397-a3e5-1beec09bf20c
  Args:
    literal_type: xsd:integer
    source: Wilhelm_of_Prussia
    relation: :hasDeathYear
    literal_value: 1940
  AddTriple (a57716cc-e2f0-4775-be5b-ffd9ac318893)
 Call ID: a57716cc-e2f0-4775-be5b-ffd9ac318893
  Args:
    target: Crown_Prince_Wilhelm
    relation: :hasFather
    source: Wilhelm_of_Prussia
  AssignClass (f3cf1f1a-cb72-4f8a-b4ee-1bb676b07420)
 Call ID: f3cf1f1a-cb72-4f8a-b4ee-1bb676b07420
  Args:
    source: Crown_Prince_Wilhelm
    type: :Man
  AssignClass (6c36fe35-3940-4919-8e76-42e612fa58bb)
 Call ID: 6c36fe35-3940-4919-8e76-42e612fa58bb
  Args:
    type: :Person
    source: Crown_Prince_Wilhelm
  AddTriple (bc511e54-5309-4618-bbf1-60b04fec649d)
 Call ID: bc511e54-5309-4618-bbf1-60b04fec649d
  Args:
    source: Wilhelm_of_Prussia
    relation: :hasMother
    target: Cecilie_of_Mecklenburg-Schwerin
  AssignClass (406da9db-2222-4c58-a2dc-bb6c678f7b9d)
 Call ID: 406da9db-2222-4c58-a2dc-bb6c678f7b9d
  Args:
    source: Cecilie_of_Mecklenburg-Schwerin
    type: :Woman
  AssignClass (6e039694-81ba-4faf-b5f2-228d006fc33a)
 Call ID: 6e039694-81ba-4faf-b5f2-228d006fc33a
  Args:
    source: Cecilie_of_Mecklenburg-Schwerin
    type: :Person
  AddTriple (4e3f7a28-e222-4e4a-bde4-6b639fc97a94)
 Call ID: 4e3f7a28-e222-4e4a-bde4-6b639fc97a94
  Args:
    source: Crown_Prince_Wilhelm
    target: Wilhelm_II
    relation: :hasFather
  AssignClass (fafe6cb9-6cb6-4cbf-a834-77749350a73e)
 Call ID: fafe6cb9-6cb6-4cbf-a834-77749350a73e
  Args:
    source: Wilhelm_II
    type: :Man
  AssignClass (bc03938e-65fc-467e-a368-e51d4a16a3a3)
 Call ID: bc03938e-65fc-467e-a368-e51d4a16a3a3
  Args:
    source: Wilhelm_II
    type: :Person
  AddTriple (22738c36-4c95-4358-a2dc-6af61da35c56)
 Call ID: 22738c36-4c95-4358-a2dc-6af61da35c56
  Args:
    target: Louis_Ferdinand
    relation: :hasBrother
    source: Wilhelm_of_Prussia
  AssignClass (0cf8b289-45c0-47ae-99ff-a15a569f10f2)
 Call ID: 0cf8b289-45c0-47ae-99ff-a15a569f10f2
  Args:
    source: Louis_Ferdinand
    type: :Man
  AssignClass (9e2003ab-700a-49e3-b8bc-f71e4d75b3ce)
 Call ID: 9e2003ab-700a-49e3-b8bc-f71e4d75b3ce
  Args:
    source: Louis_Ferdinand
    type: :Person
  AddLiteral (7beeb521-9181-4e8a-966f-0fd112f54e3a)
 Call ID: 7beeb521-9181-4e8a-966f-0fd112f54e3a
  Args:
    literal_value: 1907
    relation: :hasBirthYear
    source: Louis_Ferdinand
    literal_type: xsd:integer
  AddTriple (76972ac4-4ba2-4dca-8eae-695f66cc7820)
 Call ID: 76972ac4-4ba2-4dca-8eae-695f66cc7820
  Args:
    source: Louis_Ferdinand
    relation: :hasFather
    target: Crown_Prince_Wilhelm
  AddTriple (5681d2e6-2eec-4453-9446-596351618cda)
 Call ID: 5681d2e6-2eec-4453-9446-596351618cda
  Args:
    source: Louis_Ferdinand
    relation: :hasMother
    target: Cecilie_of_Mecklenburg-Schwerin
  AssignClass (0d15cee2-a294-4420-b9f5-8603a9caf48d)
 Call ID: 0d15cee2-a294-4420-b9f5-8603a9caf48d
  Args:
    type: :Woman
    source: Dorothea_von_Salviati
  AssignClass (a10ab597-d830-4888-a016-4834b1b167f4)
 Call ID: a10ab597-d830-4888-a016-4834b1b167f4
  Args:
    type: :Person
    source: Dorothea_von_Salviati
  AddLiteral (9e7c3ddb-d0ed-4806-9df1-3581589764d5)
 Call ID: 9e7c3ddb-d0ed-4806-9df1-3581589764d5
  Args:
    literal_value: 1907
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Dorothea_von_Salviati
  AddLiteral (9f8e9725-575e-40cc-ab35-1e46085cbfda)
 Call ID: 9f8e9725-575e-40cc-ab35-1e46085cbfda
  Args:
    literal_type: xsd:integer
    source: Dorothea_von_Salviati
    literal_value: 1972
    relation: :hasDeathYear
  AddTriple (b78433de-8cbd-4da6-a7e0-e472072c50a3)
 Call ID: b78433de-8cbd-4da6-a7e0-e472072c50a3
  Args:
    relation: :hasMarriageYear
    target: 1933
    source: Wilhelm_of_Prussia
  AddTriple (e94b8144-f0be-461c-8390-757fb0f6ad44)
 Call ID: e94b8144-f0be-461c-8390-757fb0f6ad44
  Args:
    target: Dorothea_von_Salviati
    relation: :hasRelation
    source: Wilhelm_of_Prussia
  Finish (5e6c7c6e-c126-4c11-b012-3525df683708)
 Call ID: 5e6c7c6e-c126-4c11-b012-3525df683708
  Args:

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

The final data graph after all the edits:
  @prefix : <http://example.com/family_TBOX.ttl#> .
  @prefix data: <http://example.org/data/> .
  @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

  data:Wilhelm_of_Prussia a :Man,
          :Person ;
      :hasBirthYear 1906 ;
      :hasBrother data:Louis_Ferdinand ;
      :hasDeathYear 1940 ;
      :hasFather data:Crown_Prince_Wilhelm ;
      :hasMarriageYear data:1933 ;
      :hasMother data:Cecilie_of_Mecklenburg-Schwerin ;
      :hasRelation data:Dorothea_von_Salviati .

  data:Dorothea_von_Salviati a :Person,
          :Woman ;
      :hasBirthYear 1907 ;
      :hasDeathYear 1972 .

  data:Louis_Ferdinand a :Man,
          :Person ;
      :hasBirthYear 1907 ;
      :hasFather data:Crown_Prince_Wilhelm ;
      :hasMother data:Cecilie_of_Mecklenburg-Schwerin .

  data:Wilhelm_II a :Man,
          :Person .

  data:Cecilie_of_Mecklenburg-Schwerin a :Person,
          :Woman .

  data:Crown_Prince_Wilhelm a :Man,
          :Person ;
      :hasFather data:Wilhelm_II .



================================= Tool Message =================================

### Validation Error: Missing Node Types
Your request to `Finish` has been declined. The following nodes in the Data Graph are missing a class assignment (`rdf:type`):

**Classless Nodes:**
['1933']

### Required Correction
According to the pipeline rules, **every node must have a class assigned to it** to ensure the graph is semantically valid. 

Please perform the following steps:
1. Review the input text and ontology to determine the most appropriate class for each node listed above.
2. Use the `AssignClass` tool for each node to assign its correct type.
3. Once all nodes have been assigned a class, you may attempt to `Finish` again or run `ValidateShacl` to verify the final state.

Proceed with the necessary tool calls now.

================================== Ai Message ==================================

[]
Tool Calls:
  RemoveLiteral (e7c32b4b-2103-4ea5-9d63-febb49c4c8f9)
 Call ID: e7c32b4b-2103-4ea5-9d63-febb49c4c8f9
  Args:
    source: Wilhelm_of_Prussia
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 1933
  AddLiteral (677a865e-727f-432d-a3b9-e9a37e0d1285)
 Call ID: 677a865e-727f-432d-a3b9-e9a37e0d1285
  Args:
    literal_value: 1933
    relation: :hasMarriageYear
    literal_type: xsd:string
    source: Wilhelm_of_Prussia
  AssignClass (28a72edb-80cc-4bae-8170-1720972f31f0)
 Call ID: 28a72edb-80cc-4bae-8170-1720972f31f0
  Args:
    type: :DomainEntity
    source: 1933
  Finish (0f40e48c-71bd-449f-9d19-ac3844306a08)
 Call ID: 0f40e48c-71bd-449f-9d19-ac3844306a08
  Args: