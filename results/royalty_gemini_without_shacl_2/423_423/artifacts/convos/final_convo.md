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
  AssignClass (abf8d542-56e7-4ae6-b79d-1d133bd8f057)
 Call ID: abf8d542-56e7-4ae6-b79d-1d133bd8f057
  Args:
    type: :Man
    source: Prince_Wilhelm_Victor_of_Prussia
  AssignClass (5bef67d8-c1ba-4813-af63-55e709f5d5c1)
 Call ID: 5bef67d8-c1ba-4813-af63-55e709f5d5c1
  Args:
    source: Prince_Wilhelm_Victor_of_Prussia
    type: :Person
  AddLiteral (ce57409d-0bb8-4bf6-b4c6-f5b374c47826)
 Call ID: ce57409d-0bb8-4bf6-b4c6-f5b374c47826
  Args:
    source: Prince_Wilhelm_Victor_of_Prussia
    literal_value: 1919
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (bdd57020-99ac-4cfd-822a-cf4eb2062785)
 Call ID: bdd57020-99ac-4cfd-822a-cf4eb2062785
  Args:
    literal_type: xsd:integer
    source: Prince_Wilhelm_Victor_of_Prussia
    literal_value: 1989
    relation: :hasDeathYear
  AssignClass (f86ec8de-fe70-41c0-b34c-b12355fe89c8)
 Call ID: f86ec8de-fe70-41c0-b34c-b12355fe89c8
  Args:
    source: Emperor_Wilhelm_II
    type: :Man
  AssignClass (bcd36b4d-570c-4a88-bbee-bd0de4e3c1e7)
 Call ID: bcd36b4d-570c-4a88-bbee-bd0de4e3c1e7
  Args:
    source: Emperor_Wilhelm_II
    type: :Person
  AddTriple (04447df7-516d-4b23-84fe-d8abdfee3883)
 Call ID: 04447df7-516d-4b23-84fe-d8abdfee3883
  Args:
    target: Prince_Wilhelm_Victor_of_Prussia
    relation: :isAncestorOf
    source: Emperor_Wilhelm_II
  AssignClass (904bbfe9-1e75-44f2-a3d7-3ded822efcda)
 Call ID: 904bbfe9-1e75-44f2-a3d7-3ded822efcda
  Args:
    source: Prince_Adalbert_of_Prussia
    type: :Man
  AssignClass (d10e98b3-d7ce-46f3-9f23-3091555d249a)
 Call ID: d10e98b3-d7ce-46f3-9f23-3091555d249a
  Args:
    type: :Person
    source: Prince_Adalbert_of_Prussia
  AddLiteral (6eb31966-cbc1-42e1-bbbf-e4499657b021)
 Call ID: 6eb31966-cbc1-42e1-bbbf-e4499657b021
  Args:
    relation: :hasBirthYear
    literal_value: 1884
    source: Prince_Adalbert_of_Prussia
    literal_type: xsd:integer
  AddLiteral (d9e5ad71-652a-49a3-b50e-7dce3e74e8ca)
 Call ID: d9e5ad71-652a-49a3-b50e-7dce3e74e8ca
  Args:
    literal_type: xsd:integer
    literal_value: 1948
    source: Prince_Adalbert_of_Prussia
    relation: :hasDeathYear
  AddTriple (4db5a3ec-2f0c-4c56-b4d9-2e61cb4509f1)
 Call ID: 4db5a3ec-2f0c-4c56-b4d9-2e61cb4509f1
  Args:
    target: Prince_Wilhelm_Victor_of_Prussia
    source: Prince_Adalbert_of_Prussia
    relation: :isFatherOf
  AssignClass (cd567257-1da3-4394-bdce-fcf014b72e18)
 Call ID: cd567257-1da3-4394-bdce-fcf014b72e18
  Args:
    source: Princess_Adelheid_of_Saxe-Meiningen
    type: :Woman
  AssignClass (47938fe0-da4c-4761-942c-e17c544f209d)
 Call ID: 47938fe0-da4c-4761-942c-e17c544f209d
  Args:
    type: :Person
    source: Princess_Adelheid_of_Saxe-Meiningen
  AddLiteral (a9241fb7-b794-45f5-8c4e-3c38d0492f61)
 Call ID: a9241fb7-b794-45f5-8c4e-3c38d0492f61
  Args:
    literal_type: xsd:integer
    literal_value: 1891
    source: Princess_Adelheid_of_Saxe-Meiningen
    relation: :hasBirthYear
  AddLiteral (5c975294-5d55-4937-b480-6e6e3906d298)
 Call ID: 5c975294-5d55-4937-b480-6e6e3906d298
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: Princess_Adelheid_of_Saxe-Meiningen
    literal_value: 1971
  AddTriple (42456bc2-9ffa-4c76-b4e3-153b7b54d973)
 Call ID: 42456bc2-9ffa-4c76-b4e3-153b7b54d973
  Args:
    target: Prince_Wilhelm_Victor_of_Prussia
    source: Princess_Adelheid_of_Saxe-Meiningen
    relation: :isMotherOf
  AssignClass (19c3f625-a56a-46e4-ae0c-bdc7a60da310)
 Call ID: 19c3f625-a56a-46e4-ae0c-bdc7a60da310
  Args:
    type: :Woman
    source: Princess_Viktoria_Marina
  AssignClass (c4817b43-e1a9-4079-b558-dde4d03cda25)
 Call ID: c4817b43-e1a9-4079-b558-dde4d03cda25
  Args:
    source: Princess_Viktoria_Marina
    type: :Person
  AddLiteral (cef2fc84-d81a-48e4-a941-91a06a101a92)
 Call ID: cef2fc84-d81a-48e4-a941-91a06a101a92
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1917
    source: Princess_Viktoria_Marina
  AddLiteral (29c13841-36f4-44e6-9f7a-cbb95766641c)
 Call ID: 29c13841-36f4-44e6-9f7a-cbb95766641c
  Args:
    relation: :hasDeathYear
    literal_value: 1981
    source: Princess_Viktoria_Marina
    literal_type: xsd:integer
  AddTriple (1440f3ce-5792-495b-ad9e-2c87c099910b)
 Call ID: 1440f3ce-5792-495b-ad9e-2c87c099910b
  Args:
    target: Prince_Wilhelm_Victor_of_Prussia
    source: Princess_Viktoria_Marina
    relation: :isSisterOf
  AssignClass (368dc118-9a0b-4b1d-bb8b-ffd6f6b4f65a)
 Call ID: 368dc118-9a0b-4b1d-bb8b-ffd6f6b4f65a
  Args:
    source: Kirby_William_Patterson
    type: :Man
  AssignClass (66588ef8-f5b0-4f6c-98ba-8f23188aefb9)
 Call ID: 66588ef8-f5b0-4f6c-98ba-8f23188aefb9
  Args:
    source: Kirby_William_Patterson
    type: :Person
  AddLiteral (18f97e46-561f-4a62-9fa1-dcaf2a39874e)
 Call ID: 18f97e46-561f-4a62-9fa1-dcaf2a39874e
  Args:
    literal_type: xsd:integer
    literal_value: 1907
    source: Kirby_William_Patterson
    relation: :hasBirthYear
  AddLiteral (ec27bde8-4113-452e-a8fd-84a511709ef1)
 Call ID: ec27bde8-4113-452e-a8fd-84a511709ef1
  Args:
    relation: :hasDeathYear
    literal_value: 1984
    source: Kirby_William_Patterson
    literal_type: xsd:integer
  AssignClass (1bf6a9e7-c72c-4b2d-8f45-b162a79ec9f5)
 Call ID: 1bf6a9e7-c72c-4b2d-8f45-b162a79ec9f5
  Args:
    source: Marie_Antoinette_Countess_of_Hoyos-Stichsenstein
    type: :Woman
  AssignClass (66fd9e9e-e705-468e-99a6-20d444b93b4a)
 Call ID: 66fd9e9e-e705-468e-99a6-20d444b93b4a
  Args:
    type: :Person
    source: Marie_Antoinette_Countess_of_Hoyos-Stichsenstein
  AddLiteral (76087350-0493-450a-b0ef-f78b3cb17c1e)
 Call ID: 76087350-0493-450a-b0ef-f78b3cb17c1e
  Args:
    relation: :hasBirthYear
    source: Marie_Antoinette_Countess_of_Hoyos-Stichsenstein
    literal_value: 1920
    literal_type: xsd:integer
  AddLiteral (4f868460-cefb-4256-a37a-1c64c03823cb)
 Call ID: 4f868460-cefb-4256-a37a-1c64c03823cb
  Args:
    literal_type: xsd:integer
    source: Marie_Antoinette_Countess_of_Hoyos-Stichsenstein
    literal_value: 2004
    relation: :hasDeathYear
  AddLiteral (c146d327-d434-445b-86e1-132f5b48d12e)
 Call ID: c146d327-d434-445b-86e1-132f5b48d12e
  Args:
    relation: :hasMarriageYear
    literal_value: 1944
    source: Prince_Wilhelm_Victor_of_Prussia
    literal_type: xsd:integer
  AddTriple (acf7ee44-69b4-44d8-94bc-2431260a716a)
 Call ID: acf7ee44-69b4-44d8-94bc-2431260a716a
  Args:
    target: Marie_Antoinette_Countess_of_Hoyos-Stichsenstein
    relation: :hasRelation
    source: Prince_Wilhelm_Victor_of_Prussia
  AssignClass (78e85fbb-7c48-482c-83a1-98041596585f)
 Call ID: 78e85fbb-7c48-482c-83a1-98041596585f
  Args:
    type: :Man
    source: Friedrich_Count_of_Hoyos-Stichsenstein
  AssignClass (8eada33a-3169-4ec2-a2e0-739a39d70f71)
 Call ID: 8eada33a-3169-4ec2-a2e0-739a39d70f71
  Args:
    source: Friedrich_Count_of_Hoyos-Stichsenstein
    type: :Person
  AddLiteral (58e977a9-af1c-4f28-bee3-cf948d8c53ba)
 Call ID: 58e977a9-af1c-4f28-bee3-cf948d8c53ba
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Friedrich_Count_of_Hoyos-Stichsenstein
    literal_value: 1876
  AddLiteral (6dcaead2-47e6-4461-9775-facb02569bb7)
 Call ID: 6dcaead2-47e6-4461-9775-facb02569bb7
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1951
    source: Friedrich_Count_of_Hoyos-Stichsenstein
  AddTriple (850e4693-c134-4242-b330-5d8629259e80)
 Call ID: 850e4693-c134-4242-b330-5d8629259e80
  Args:
    relation: :isFatherOf
    source: Friedrich_Count_of_Hoyos-Stichsenstein
    target: Marie_Antoinette_Countess_of_Hoyos-Stichsenstein
  AssignClass (10f2a5bc-4f1d-47e1-8563-377ad56417fa)
 Call ID: 10f2a5bc-4f1d-47e1-8563-377ad56417fa
  Args:
    type: :Woman
    source: Countess_Wilhelmine_von_Wuthenau-Hohenthurm
  AssignClass (e87167f7-782f-4db9-98e9-1e04a5dfec80)
 Call ID: e87167f7-782f-4db9-98e9-1e04a5dfec80
  Args:
    type: :Person
    source: Countess_Wilhelmine_von_Wuthenau-Hohenthurm
  AddLiteral (f25f4cfd-32b2-4a1c-a1a1-fa2f8e782769)
 Call ID: f25f4cfd-32b2-4a1c-a1a1-fa2f8e782769
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Countess_Wilhelmine_von_Wuthenau-Hohenthurm
    literal_value: 1895
  AddLiteral (184251bc-ee1b-4085-ba99-92fca415041b)
 Call ID: 184251bc-ee1b-4085-ba99-92fca415041b
  Args:
    source: Countess_Wilhelmine_von_Wuthenau-Hohenthurm
    literal_value: 1983
    relation: :hasDeathYear
    literal_type: xsd:integer
  AddTriple (68a911d8-bb99-45d8-9606-55c3960e6a9f)
 Call ID: 68a911d8-bb99-45d8-9606-55c3960e6a9f
  Args:
    target: Marie_Antoinette_Countess_of_Hoyos-Stichsenstein
    relation: :isMotherOf
    source: Countess_Wilhelmine_von_Wuthenau-Hohenthurm
  AssignClass (dc9a879b-7eb4-4883-b5f3-3cb0148ad581)
 Call ID: dc9a879b-7eb4-4883-b5f3-3cb0148ad581
  Args:
    source: Sophie_Duchess_of_Hohenberg
    type: :Woman
  AssignClass (b35eacb9-8ed5-44f8-b31f-af18efae8d0d)
 Call ID: b35eacb9-8ed5-44f8-b31f-af18efae8d0d
  Args:
    source: Sophie_Duchess_of_Hohenberg
    type: :Person
  Finish (828def53-1868-4251-a242-094271e055c0)
 Call ID: 828def53-1868-4251-a242-094271e055c0
  Args: