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
Prince Wilhelm Victor of Prussia (German: Wilhelm Viktor Ernst Freund Friedrich Georg Adalbert; 15 February 1919 – 7 February 1989) was a German royal, soldier and diplomat.
Life

Prince Wilhelm Victor was a grandson of Emperor Wilhelm II and the youngest child of Prince Adalbert of Prussia (1884–1948) and Princess Adelheid "Adi" of Saxe-Meiningen (1891–1971).
His father, Prince Adalbert carried also the title "Graf von Lingen".
His only surviving sister, Princess Viktoria Marina (1917–1981) married Kirby William Patterson (1907–1984).
Marriage

Prince Wilhelm Victor married at Donaueschingen 20 July 1944 Marie Antoinette, Countess of Hoyos-Stichsenstein (Hohenthurm, 27 June 1920 – Marbella 1 March 2004),  daughter of Friedrich, Count of Hoyos-Stichsenstein (1876–1951) and Countess Wilhelmine von Wuthenau-Hohenthurm (1895–1983), niece of Sophie, Duchess of Hohenberg.
They had the following issue:


Death

Prince Wilhelm Viktor died on 7 February 1989 at age 69.



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
  AssignClass (9768a0b6-2681-4006-a949-b7c47822d1fe)
 Call ID: 9768a0b6-2681-4006-a949-b7c47822d1fe
  Args:
    source: Prince_Wilhelm_Victor_of_Prussia
    type: :Man
  AssignClass (303e47bb-6662-4533-a12a-414c280534a8)
 Call ID: 303e47bb-6662-4533-a12a-414c280534a8
  Args:
    type: :Person
    source: Prince_Wilhelm_Victor_of_Prussia
  AddLiteral (0f4becbd-5114-4879-9ec8-b54e0a379dc1)
 Call ID: 0f4becbd-5114-4879-9ec8-b54e0a379dc1
  Args:
    literal_type: xsd:integer
    source: Prince_Wilhelm_Victor_of_Prussia
    relation: :hasBirthYear
    literal_value: 1919
  AddLiteral (1f1654ea-e6bf-4142-b347-139dff98fd48)
 Call ID: 1f1654ea-e6bf-4142-b347-139dff98fd48
  Args:
    literal_value: 1989
    source: Prince_Wilhelm_Victor_of_Prussia
    relation: :hasDeathYear
    literal_type: xsd:integer
  AssignClass (6d4312fa-4678-4ba2-9b3f-dd259824e80c)
 Call ID: 6d4312fa-4678-4ba2-9b3f-dd259824e80c
  Args:
    source: Emperor_Wilhelm_II
    type: :Man
  AssignClass (5c2aaafb-7fe1-463c-b65a-1b7a1f6d00e8)
 Call ID: 5c2aaafb-7fe1-463c-b65a-1b7a1f6d00e8
  Args:
    source: Emperor_Wilhelm_II
    type: :Person
  AddTriple (3322362e-c9c3-4779-98d1-cb750cb4acfc)
 Call ID: 3322362e-c9c3-4779-98d1-cb750cb4acfc
  Args:
    target: Prince_Wilhelm_Victor_of_Prussia
    source: Emperor_Wilhelm_II
    relation: :isAncestorOf
  AssignClass (a7229335-f6c7-47f1-83e1-c5a6794dfaba)
 Call ID: a7229335-f6c7-47f1-83e1-c5a6794dfaba
  Args:
    source: Prince_Adalbert_of_Prussia
    type: :Man
  AssignClass (a274e8ca-521b-48c7-9558-7b4690f0e1cd)
 Call ID: a274e8ca-521b-48c7-9558-7b4690f0e1cd
  Args:
    type: :Person
    source: Prince_Adalbert_of_Prussia
  AddLiteral (496ab285-eaef-4e8d-a064-d2e73d74ea07)
 Call ID: 496ab285-eaef-4e8d-a064-d2e73d74ea07
  Args:
    literal_type: xsd:integer
    literal_value: 1884
    source: Prince_Adalbert_of_Prussia
    relation: :hasBirthYear
  AddLiteral (36a5bb34-6a45-432e-80fd-cf49360fdde1)
 Call ID: 36a5bb34-6a45-432e-80fd-cf49360fdde1
  Args:
    source: Prince_Adalbert_of_Prussia
    relation: :hasDeathYear
    literal_value: 1948
    literal_type: xsd:integer
  AddTriple (67602f0d-2acf-4657-95fd-22fd2449b52f)
 Call ID: 67602f0d-2acf-4657-95fd-22fd2449b52f
  Args:
    target: Prince_Adalbert_of_Prussia
    source: Prince_Wilhelm_Victor_of_Prussia
    relation: :hasFather
  AssignClass (51dbf079-44bd-4bae-98ae-3beae40156fd)
 Call ID: 51dbf079-44bd-4bae-98ae-3beae40156fd
  Args:
    source: Princess_Adelheid_of_Saxe-Meiningen
    type: :Woman
  AssignClass (1a136cb8-f660-4644-a483-1966c78acc17)
 Call ID: 1a136cb8-f660-4644-a483-1966c78acc17
  Args:
    type: :Person
    source: Princess_Adelheid_of_Saxe-Meiningen
  AddLiteral (7255bf32-dda8-4cbb-a699-fd208b50fa83)
 Call ID: 7255bf32-dda8-4cbb-a699-fd208b50fa83
  Args:
    literal_value: 1891
    source: Princess_Adelheid_of_Saxe-Meiningen
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (719ab721-b199-4ec9-8fe6-6af87f153d55)
 Call ID: 719ab721-b199-4ec9-8fe6-6af87f153d55
  Args:
    source: Princess_Adelheid_of_Saxe-Meiningen
    relation: :hasDeathYear
    literal_value: 1971
    literal_type: xsd:integer
  AddTriple (422ca33f-fb9f-49ff-b0e3-71a5bbb95f4f)
 Call ID: 422ca33f-fb9f-49ff-b0e3-71a5bbb95f4f
  Args:
    target: Princess_Adelheid_of_Saxe-Meiningen
    relation: :hasMother
    source: Prince_Wilhelm_Victor_of_Prussia
  AssignClass (7cc2bd63-4d35-4c5b-9fdc-32438961ca65)
 Call ID: 7cc2bd63-4d35-4c5b-9fdc-32438961ca65
  Args:
    type: :Woman
    source: Princess_Viktoria_Marina
  AssignClass (a37718ca-9b6c-45d0-b27a-c59cb68884a7)
 Call ID: a37718ca-9b6c-45d0-b27a-c59cb68884a7
  Args:
    source: Princess_Viktoria_Marina
    type: :Person
  AddLiteral (3b931a61-ad8d-4909-b821-85f9efbe5c97)
 Call ID: 3b931a61-ad8d-4909-b821-85f9efbe5c97
  Args:
    literal_value: 1917
    relation: :hasBirthYear
    source: Princess_Viktoria_Marina
    literal_type: xsd:integer
  AddLiteral (3ca299af-b5a6-48fc-bf05-50d88e687a2e)
 Call ID: 3ca299af-b5a6-48fc-bf05-50d88e687a2e
  Args:
    literal_type: xsd:integer
    source: Princess_Viktoria_Marina
    relation: :hasDeathYear
    literal_value: 1981
  AddTriple (c124acb8-53dd-43f2-8a1c-d8239d2f13ce)
 Call ID: c124acb8-53dd-43f2-8a1c-d8239d2f13ce
  Args:
    relation: :hasSister
    source: Prince_Wilhelm_Victor_of_Prussia
    target: Princess_Viktoria_Marina
  AssignClass (2cac174a-8ec6-4021-93a5-e318872eb68b)
 Call ID: 2cac174a-8ec6-4021-93a5-e318872eb68b
  Args:
    type: :Man
    source: Kirby_William_Patterson
  AssignClass (d73d5c07-80fe-4294-b60f-58a3931882ec)
 Call ID: d73d5c07-80fe-4294-b60f-58a3931882ec
  Args:
    type: :Person
    source: Kirby_William_Patterson
  AddLiteral (6d5ac503-0004-4011-9173-ffd2c2b61667)
 Call ID: 6d5ac503-0004-4011-9173-ffd2c2b61667
  Args:
    source: Kirby_William_Patterson
    relation: :hasBirthYear
    literal_value: 1907
    literal_type: xsd:integer
  AddLiteral (fbd4d721-58e8-47f7-9688-d8688af2b803)
 Call ID: fbd4d721-58e8-47f7-9688-d8688af2b803
  Args:
    literal_type: xsd:integer
    source: Kirby_William_Patterson
    relation: :hasDeathYear
    literal_value: 1984
  AddTriple (37dad157-04f5-43fd-8b16-da1878ce0e0f)
 Call ID: 37dad157-04f5-43fd-8b16-da1878ce0e0f
  Args:
    target: Kirby_William_Patterson
    relation: :hasRelation
    source: Princess_Viktoria_Marina
  AssignClass (6d669048-831f-46aa-b894-1a8e1f9888ed)
 Call ID: 6d669048-831f-46aa-b894-1a8e1f9888ed
  Args:
    type: :Woman
    source: Marie_Antoinette_Countess_of_Hoyos-Stichsenstein
  AssignClass (695bae77-d3b2-4b8c-8bc5-dbf7291d6100)
 Call ID: 695bae77-d3b2-4b8c-8bc5-dbf7291d6100
  Args:
    source: Marie_Antoinette_Countess_of_Hoyos-Stichsenstein
    type: :Person
  AddLiteral (c4076ad3-7a48-47d3-8d8a-46cbc42cf38c)
 Call ID: c4076ad3-7a48-47d3-8d8a-46cbc42cf38c
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Marie_Antoinette_Countess_of_Hoyos-Stichsenstein
    literal_value: 1920
  AddLiteral (8f39da05-7dd4-4ef7-b930-076043cbe86a)
 Call ID: 8f39da05-7dd4-4ef7-b930-076043cbe86a
  Args:
    literal_type: xsd:integer
    literal_value: 2004
    source: Marie_Antoinette_Countess_of_Hoyos-Stichsenstein
    relation: :hasDeathYear
  AddLiteral (b592af33-1edc-45ad-9683-b200a7a8c1a6)
 Call ID: b592af33-1edc-45ad-9683-b200a7a8c1a6
  Args:
    literal_type: xsd:integer
    literal_value: 1944
    source: Prince_Wilhelm_Victor_of_Prussia
    relation: :hasMarriageYear
  AddTriple (8059074a-697b-4cae-a6c1-a999f7b422df)
 Call ID: 8059074a-697b-4cae-a6c1-a999f7b422df
  Args:
    target: Marie_Antoinette_Countess_of_Hoyos-Stichsenstein
    relation: :hasRelation
    source: Prince_Wilhelm_Victor_of_Prussia
  AssignClass (f59a22c8-f3fa-4578-b570-be021dae2f04)
 Call ID: f59a22c8-f3fa-4578-b570-be021dae2f04
  Args:
    type: :Man
    source: Friedrich_Count_of_Hoyos-Stichsenstein
  AssignClass (16410f16-50a8-444e-8a23-2a916977b5ca)
 Call ID: 16410f16-50a8-444e-8a23-2a916977b5ca
  Args:
    type: :Person
    source: Friedrich_Count_of_Hoyos-Stichsenstein
  AddLiteral (97ca3b69-3ab4-4818-b7f8-e4cbaf5e278d)
 Call ID: 97ca3b69-3ab4-4818-b7f8-e4cbaf5e278d
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Friedrich_Count_of_Hoyos-Stichsenstein
    literal_value: 1876
  AddLiteral (b8351204-d201-4d0a-814b-094de9aca706)
 Call ID: b8351204-d201-4d0a-814b-094de9aca706
  Args:
    relation: :hasDeathYear
    source: Friedrich_Count_of_Hoyos-Stichsenstein
    literal_value: 1951
    literal_type: xsd:integer
  AddTriple (11777952-ba8a-4380-b41d-3217c183be3c)
 Call ID: 11777952-ba8a-4380-b41d-3217c183be3c
  Args:
    relation: :hasFather
    source: Marie_Antoinette_Countess_of_Hoyos-Stichsenstein
    target: Friedrich_Count_of_Hoyos-Stichsenstein
  AssignClass (014f24fc-8d62-47c0-b002-ff65dee3df27)
 Call ID: 014f24fc-8d62-47c0-b002-ff65dee3df27
  Args:
    type: :Woman
    source: Countess_Wilhelmine_von_Wuthenau-Hohenthurm
  AssignClass (98c7e720-222b-48aa-84a0-c1d102c3c221)
 Call ID: 98c7e720-222b-48aa-84a0-c1d102c3c221
  Args:
    source: Countess_Wilhelmine_von_Wuthenau-Hohenthurm
    type: :Person
  AddLiteral (06d94970-e89b-4612-8071-4a191d61f02f)
 Call ID: 06d94970-e89b-4612-8071-4a191d61f02f
  Args:
    literal_type: xsd:integer
    literal_value: 1895
    source: Countess_Wilhelmine_von_Wuthenau-Hohenthurm
    relation: :hasBirthYear
  AddLiteral (3f93c2ae-2239-411a-b077-2c450a5b884c)
 Call ID: 3f93c2ae-2239-411a-b077-2c450a5b884c
  Args:
    relation: :hasDeathYear
    source: Countess_Wilhelmine_von_Wuthenau-Hohenthurm
    literal_value: 1983
    literal_type: xsd:integer
  AddTriple (df082226-5029-4fe2-ae28-91ab7c0b80ee)
 Call ID: df082226-5029-4fe2-ae28-91ab7c0b80ee
  Args:
    target: Countess_Wilhelmine_von_Wuthenau-Hohenthurm
    source: Marie_Antoinette_Countess_of_Hoyos-Stichsenstein
    relation: :hasMother
  AssignClass (2726224e-8f8e-43a0-b4ea-fd52841aba73)
 Call ID: 2726224e-8f8e-43a0-b4ea-fd52841aba73
  Args:
    type: :Woman
    source: Sophie_Duchess_of_Hohenberg
  AssignClass (2c5259c3-34e1-4bb6-bad9-d5c54f265ff6)
 Call ID: 2c5259c3-34e1-4bb6-bad9-d5c54f265ff6
  Args:
    type: :Person
    source: Sophie_Duchess_of_Hohenberg
  AddTriple (f24f8583-75bf-4245-8a6f-1a09296aad11)
 Call ID: f24f8583-75bf-4245-8a6f-1a09296aad11
  Args:
    target: Sophie_Duchess_of_Hohenberg
    source: Countess_Wilhelmine_von_Wuthenau-Hohenthurm
    relation: :hasRelation
  Finish (90ee3888-6413-487b-8ac5-a74102998ef1)
 Call ID: 90ee3888-6413-487b-8ac5-a74102998ef1
  Args: