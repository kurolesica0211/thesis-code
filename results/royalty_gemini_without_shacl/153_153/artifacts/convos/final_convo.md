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
Princess María de las Mercedes of Bourbon-Two Sicilies (.mw-parser-output .IPA-label-small{font-size:85%}.mw-parser-output .references .IPA-label-small,.mw-parser-output .infobox .IPA-label-small,.mw-parser-output .navbox .IPA-label-small{font-size:100%}Spanish: ; María de las Mercedes Cristina Genara Isabel Luisa Carolina Victoria y Todos los Santos de Borbón y Orléans; 23 December 1910 – 2 January 2000) was a member of the Spanish royal family and the mother of King Juan Carlos I.


The daughter of Prince Carlos of Bourbon-Two Sicilies and Princess Louise of Orléans, she married Infante Juan, Count of Barcelona, claimant to the Spanish throne.
Biography

María was born in Madrid, daughter of Prince Carlos of Bourbon-Two Sicilies, Infante of Spain, a grandson of King Ferdinand II of the Two Sicilies, and his second wife, Princess Louise of Orléans, daughter of Prince Philippe, Count of Paris, a pretender to the French throne.
She was granted, at birth, the rank and precedence of an infanta of Spain, although not the actual use of the title, her own being Princess of Bourbon-Two Sicilies.
When the Second Spanish Republic forced them into exile, they lived in Cannes and later in Paris, where she studied art at the Louvre.
On 14 January 1935, she attended the wedding, in Rome, of Infanta Beatriz of Spain, daughter of King Alfonso XIII, to Alessandro Torlonia, 5th Prince of Civitella-Cesi.
There she met the brother of the bride, her third cousin and future husband, the Infante Juan, fourth son and designated heir of Alfonso XIII.
When her husband took up Count of Barcelona as a title of pretence on 8 March 1941, María became the Countess of Barcelona.
They lived in Cannes and Rome, and, with the outbreak of World War II, they moved to Lausanne to live with Queen Victoria Eugenie, the mother of Infante Juan.
In 1953, the Countess represented the Spanish Royal Family at the coronation of Queen Elizabeth II.
In 1976, one year after the monarchy was restored in Spain in the person of her son, Juan Carlos, they returned to Spain.
She mediated between her son and her husband, estranged since Juan Carlos had been designated heir by Franco.
In 1977, Juan renounced his rights in favour of their son, who officially allowed him to retain the title of Count of Barcelona.
In 1995, her granddaughter Infanta Elena married in Seville in part because the Countess' love for the city.



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
  AssignClass (dd018914-3d78-46aa-8caf-bc2eac995ba5)
 Call ID: dd018914-3d78-46aa-8caf-bc2eac995ba5
  Args:
    type: :Woman
    source: Maria_de_las_Mercedes_of_Bourbon-Two_Sicilies
  AssignClass (7a05260e-244b-40ec-b835-93eadfd75fb5)
 Call ID: 7a05260e-244b-40ec-b835-93eadfd75fb5
  Args:
    source: Maria_de_las_Mercedes_of_Bourbon-Two_Sicilies
    type: :Person
  AddLiteral (b26d9d8c-a681-419c-95fb-1c5ce04367cc)
 Call ID: b26d9d8c-a681-419c-95fb-1c5ce04367cc
  Args:
    relation: :hasBirthYear
    source: Maria_de_las_Mercedes_of_Bourbon-Two_Sicilies
    literal_type: xsd:integer
    literal_value: 1910
  AddLiteral (30b3cc1e-b5f9-48f4-b871-fe4413fb3b0d)
 Call ID: 30b3cc1e-b5f9-48f4-b871-fe4413fb3b0d
  Args:
    relation: :hasDeathYear
    literal_value: 2000
    literal_type: xsd:integer
    source: Maria_de_las_Mercedes_of_Bourbon-Two_Sicilies
  AssignClass (271e826e-2d35-4729-972d-fbcad1786401)
 Call ID: 271e826e-2d35-4729-972d-fbcad1786401
  Args:
    type: :Man
    source: Juan_Carlos_I
  AssignClass (b4319d97-8726-405a-8660-5d1fd67ce0ad)
 Call ID: b4319d97-8726-405a-8660-5d1fd67ce0ad
  Args:
    type: :Person
    source: Juan_Carlos_I
  AddTriple (2ec508a0-a611-405d-a3c1-f3be86546c0b)
 Call ID: 2ec508a0-a611-405d-a3c1-f3be86546c0b
  Args:
    target: Juan_Carlos_I
    relation: :isMotherOf
    source: Maria_de_las_Mercedes_of_Bourbon-Two_Sicilies
  AssignClass (a7c46425-6bd4-4b8e-b8e3-8bee5c6adc60)
 Call ID: a7c46425-6bd4-4b8e-b8e3-8bee5c6adc60
  Args:
    type: :Man
    source: Carlos_of_Bourbon-Two_Sicilies
  AssignClass (142faed7-97df-45d3-86b9-9e2e92f288e4)
 Call ID: 142faed7-97df-45d3-86b9-9e2e92f288e4
  Args:
    type: :Person
    source: Carlos_of_Bourbon-Two_Sicilies
  AssignClass (f6f2d1d8-dd27-4176-954a-eaae608d1557)
 Call ID: f6f2d1d8-dd27-4176-954a-eaae608d1557
  Args:
    source: Louise_of_Orleans
    type: :Woman
  AssignClass (65a36423-0f28-462b-93c1-cd9a64805dc5)
 Call ID: 65a36423-0f28-462b-93c1-cd9a64805dc5
  Args:
    source: Louise_of_Orleans
    type: :Person
  AddTriple (83b0a716-f769-4f89-a764-805dfcd74e61)
 Call ID: 83b0a716-f769-4f89-a764-805dfcd74e61
  Args:
    relation: :isFatherOf
    source: Carlos_of_Bourbon-Two_Sicilies
    target: Maria_de_las_Mercedes_of_Bourbon-Two_Sicilies
  AddTriple (92b289f7-697e-4101-919c-a4ea76d9f0f1)
 Call ID: 92b289f7-697e-4101-919c-a4ea76d9f0f1
  Args:
    target: Maria_de_las_Mercedes_of_Bourbon-Two_Sicilies
    source: Louise_of_Orleans
    relation: :isMotherOf
  AssignClass (ae6e5ad6-49c8-4b48-b135-251a382e73db)
 Call ID: ae6e5ad6-49c8-4b48-b135-251a382e73db
  Args:
    type: :Man
    source: Juan_Count_of_Barcelona
  AssignClass (c85552f7-0a4b-436f-b0ab-00fc70dc2032)
 Call ID: c85552f7-0a4b-436f-b0ab-00fc70dc2032
  Args:
    source: Juan_Count_of_Barcelona
    type: :Person
  AddTriple (cdf4b12e-fdb2-448d-8e12-a14123e0974d)
 Call ID: cdf4b12e-fdb2-448d-8e12-a14123e0974d
  Args:
    target: Juan_Count_of_Barcelona
    relation: :hasRelation
    source: Maria_de_las_Mercedes_of_Bourbon-Two_Sicilies
  AssignClass (0388a589-7fac-4bb2-b5a2-0f3187ceb003)
 Call ID: 0388a589-7fac-4bb2-b5a2-0f3187ceb003
  Args:
    source: Ferdinand_II_of_the_Two_Sicilies
    type: :Man
  AssignClass (573212bf-cdcd-41aa-93ea-3cb97a9c869d)
 Call ID: 573212bf-cdcd-41aa-93ea-3cb97a9c869d
  Args:
    type: :Person
    source: Ferdinand_II_of_the_Two_Sicilies
  AssignClass (ff308571-8607-4c4d-8e94-f2dd9867a801)
 Call ID: ff308571-8607-4c4d-8e94-f2dd9867a801
  Args:
    source: Philippe_Count_of_Paris
    type: :Man
  AssignClass (02a8579e-af03-4906-aed6-673a0d36a3b9)
 Call ID: 02a8579e-af03-4906-aed6-673a0d36a3b9
  Args:
    source: Philippe_Count_of_Paris
    type: :Person
  AddTriple (faa3b02f-481a-4889-9914-e5ec536ee346)
 Call ID: faa3b02f-481a-4889-9914-e5ec536ee346
  Args:
    target: Louise_of_Orleans
    source: Philippe_Count_of_Paris
    relation: :isFatherOf
  AssignClass (56d07382-c856-4ab3-a95a-b5d6c233e08a)
 Call ID: 56d07382-c856-4ab3-a95a-b5d6c233e08a
  Args:
    source: Beatriz_of_Spain
    type: :Woman
  AssignClass (8fc336ca-d0c7-4280-8d0d-7850354aef37)
 Call ID: 8fc336ca-d0c7-4280-8d0d-7850354aef37
  Args:
    source: Beatriz_of_Spain
    type: :Person
  AssignClass (9dde311d-2ab6-4697-bf3f-0781461e3318)
 Call ID: 9dde311d-2ab6-4697-bf3f-0781461e3318
  Args:
    source: Alfonso_XIII
    type: :Man
  AssignClass (8be73efe-49fc-4661-8d1e-da5cfd4eb504)
 Call ID: 8be73efe-49fc-4661-8d1e-da5cfd4eb504
  Args:
    type: :Person
    source: Alfonso_XIII
  AddTriple (064f6211-6c3f-4f88-86a1-8612ba2d705d)
 Call ID: 064f6211-6c3f-4f88-86a1-8612ba2d705d
  Args:
    relation: :isFatherOf
    source: Alfonso_XIII
    target: Beatriz_of_Spain
  AddTriple (819224e3-353a-4e27-927b-c15e4648108a)
 Call ID: 819224e3-353a-4e27-927b-c15e4648108a
  Args:
    target: Juan_Count_of_Barcelona
    relation: :isFatherOf
    source: Alfonso_XIII
  AssignClass (d6d549b6-5a4d-4b77-b468-866b72965c7a)
 Call ID: d6d549b6-5a4d-4b77-b468-866b72965c7a
  Args:
    source: Alessandro_Torlonia
    type: :Man
  AssignClass (d4a2bace-3274-44b1-903b-f09bd8002ae2)
 Call ID: d4a2bace-3274-44b1-903b-f09bd8002ae2
  Args:
    type: :Person
    source: Alessandro_Torlonia
  AssignClass (a19af1be-5391-48a7-8cf7-3d1e19e8c473)
 Call ID: a19af1be-5391-48a7-8cf7-3d1e19e8c473
  Args:
    type: :Woman
    source: Victoria_Eugenie
  AssignClass (5f792014-3c63-49f3-8804-a0d385f8bda2)
 Call ID: 5f792014-3c63-49f3-8804-a0d385f8bda2
  Args:
    source: Victoria_Eugenie
    type: :Person
  AddTriple (28217c28-5173-4082-ab2c-b019976ac782)
 Call ID: 28217c28-5173-4082-ab2c-b019976ac782
  Args:
    relation: :isMotherOf
    source: Victoria_Eugenie
    target: Juan_Count_of_Barcelona
  AssignClass (b3aa0031-dc60-4cd6-be6b-087d7d9bea72)
 Call ID: b3aa0031-dc60-4cd6-be6b-087d7d9bea72
  Args:
    type: :Woman
    source: Elena
  AssignClass (8fd73578-dc29-4ba5-bc61-2914855ed69a)
 Call ID: 8fd73578-dc29-4ba5-bc61-2914855ed69a
  Args:
    type: :Person
    source: Elena
  AddTriple (33716072-5638-4f61-a178-327ec78f952c)
 Call ID: 33716072-5638-4f61-a178-327ec78f952c
  Args:
    source: Juan_Carlos_I
    relation: :isFatherOf
    target: Elena
  Finish (6bc7d546-4f9c-4d71-837f-862528dcadff)
 Call ID: 6bc7d546-4f9c-4d71-837f-862528dcadff
  Args: