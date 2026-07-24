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
  AssignClass (02f02511-64dd-40d3-969a-2a0358d6fb80)
 Call ID: 02f02511-64dd-40d3-969a-2a0358d6fb80
  Args:
    type: :Woman
    source: María_de_las_Mercedes_of_Bourbon-Two_Sicilies
  AssignClass (4158e310-b44e-486b-bbd9-6ac3b631b80d)
 Call ID: 4158e310-b44e-486b-bbd9-6ac3b631b80d
  Args:
    type: :Person
    source: María_de_las_Mercedes_of_Bourbon-Two_Sicilies
  AddLiteral (f7b5ae1f-3eb6-4508-b9da-a07e37300f29)
 Call ID: f7b5ae1f-3eb6-4508-b9da-a07e37300f29
  Args:
    source: María_de_las_Mercedes_of_Bourbon-Two_Sicilies
    literal_type: xsd:integer
    literal_value: 1910
    relation: :hasBirthYear
  AddLiteral (944e6df1-acc9-4da7-899e-6b3c4417bb6a)
 Call ID: 944e6df1-acc9-4da7-899e-6b3c4417bb6a
  Args:
    source: María_de_las_Mercedes_of_Bourbon-Two_Sicilies
    literal_type: xsd:integer
    literal_value: 2000
    relation: :hasDeathYear
  AssignClass (cc6c0135-303c-4dcf-863a-8cd42c322c4f)
 Call ID: cc6c0135-303c-4dcf-863a-8cd42c322c4f
  Args:
    type: :Man
    source: Juan_Carlos_I
  AssignClass (25c7a7f7-c0b9-4e57-8cd9-0fb928e79575)
 Call ID: 25c7a7f7-c0b9-4e57-8cd9-0fb928e79575
  Args:
    type: :Person
    source: Juan_Carlos_I
  AddTriple (932cec4a-701e-4b2e-9b4c-f2d121e7baec)
 Call ID: 932cec4a-701e-4b2e-9b4c-f2d121e7baec
  Args:
    source: María_de_las_Mercedes_of_Bourbon-Two_Sicilies
    target: Juan_Carlos_I
    relation: :isMotherOf
  AssignClass (9cce593c-99cd-4037-9be8-59f9991dd365)
 Call ID: 9cce593c-99cd-4037-9be8-59f9991dd365
  Args:
    type: :Man
    source: Prince_Carlos_of_Bourbon-Two_Sicilies
  AssignClass (ca807ef2-c46c-406c-8d2e-ec76cdf76ab1)
 Call ID: ca807ef2-c46c-406c-8d2e-ec76cdf76ab1
  Args:
    type: :Person
    source: Prince_Carlos_of_Bourbon-Two_Sicilies
  AddTriple (96158193-a837-46d2-ac4a-134be3ecd880)
 Call ID: 96158193-a837-46d2-ac4a-134be3ecd880
  Args:
    source: Prince_Carlos_of_Bourbon-Two_Sicilies
    target: María_de_las_Mercedes_of_Bourbon-Two_Sicilies
    relation: :isFatherOf
  AssignClass (a02dfd32-4b07-4abe-854e-66bf82edc267)
 Call ID: a02dfd32-4b07-4abe-854e-66bf82edc267
  Args:
    type: :Woman
    source: Princess_Louise_of_Orléans
  AssignClass (13828fff-04fb-4855-8601-2fb5684845f0)
 Call ID: 13828fff-04fb-4855-8601-2fb5684845f0
  Args:
    type: :Person
    source: Princess_Louise_of_Orléans
  AddTriple (3a204e8b-c2fd-4f27-abb7-c7daeca0fe6a)
 Call ID: 3a204e8b-c2fd-4f27-abb7-c7daeca0fe6a
  Args:
    relation: :isMotherOf
    target: María_de_las_Mercedes_of_Bourbon-Two_Sicilies
    source: Princess_Louise_of_Orléans
  AssignClass (c067be3a-54e4-4767-9ee5-c30ee8dd3fa7)
 Call ID: c067be3a-54e4-4767-9ee5-c30ee8dd3fa7
  Args:
    source: Infante_Juan_Count_of_Barcelona
    type: :Man
  AssignClass (b618938a-d5b5-4e61-aa4e-5d938f17430b)
 Call ID: b618938a-d5b5-4e61-aa4e-5d938f17430b
  Args:
    source: Infante_Juan_Count_of_Barcelona
    type: :Person
  AddTriple (c8855087-16b6-420f-a1e0-38b5cfeee0b1)
 Call ID: c8855087-16b6-420f-a1e0-38b5cfeee0b1
  Args:
    source: María_de_las_Mercedes_of_Bourbon-Two_Sicilies
    target: Infante_Juan_Count_of_Barcelona
    relation: :hasRelation
  AssignClass (e146ea3f-09c2-458b-9091-487b0ee9c09e)
 Call ID: e146ea3f-09c2-458b-9091-487b0ee9c09e
  Args:
    source: King_Ferdinand_II_of_the_Two_Sicilies
    type: :Man
  AssignClass (e990f5a1-706c-41b8-9e81-e2797d57cd5c)
 Call ID: e990f5a1-706c-41b8-9e81-e2797d57cd5c
  Args:
    source: King_Ferdinand_II_of_the_Two_Sicilies
    type: :Person
  AddTriple (ae76fc3e-43c6-49db-8e8f-20774c59a3e3)
 Call ID: ae76fc3e-43c6-49db-8e8f-20774c59a3e3
  Args:
    relation: :isFatherOf
    target: Prince_Carlos_of_Bourbon-Two_Sicilies
    source: King_Ferdinand_II_of_the_Two_Sicilies
  AssignClass (c65096c1-e2b7-4bf0-9a53-28c8ed4d4197)
 Call ID: c65096c1-e2b7-4bf0-9a53-28c8ed4d4197
  Args:
    source: Prince_Philippe_Count_of_Paris
    type: :Man
  AssignClass (978f677e-e5e1-46bb-bd56-a8133b3d1e1f)
 Call ID: 978f677e-e5e1-46bb-bd56-a8133b3d1e1f
  Args:
    type: :Person
    source: Prince_Philippe_Count_of_Paris
  AddTriple (eee5a899-58f8-4a59-a402-8c307ccc6e7e)
 Call ID: eee5a899-58f8-4a59-a402-8c307ccc6e7e
  Args:
    source: Prince_Philippe_Count_of_Paris
    target: Princess_Louise_of_Orléans
    relation: :isFatherOf
  AssignClass (35f0a30d-616d-4163-ac55-cb1b7ad769e3)
 Call ID: 35f0a30d-616d-4163-ac55-cb1b7ad769e3
  Args:
    source: Infanta_Beatriz_of_Spain
    type: :Woman
  AssignClass (4c21b5f6-ba36-4c38-97cc-96690ccabd9e)
 Call ID: 4c21b5f6-ba36-4c38-97cc-96690ccabd9e
  Args:
    source: Infanta_Beatriz_of_Spain
    type: :Person
  AssignClass (a59e9879-e429-4911-aea1-4741cd758823)
 Call ID: a59e9879-e429-4911-aea1-4741cd758823
  Args:
    type: :Man
    source: King_Alfonso_XIII
  AssignClass (0fc2c0dd-8249-471d-b000-bc5ac9f376e4)
 Call ID: 0fc2c0dd-8249-471d-b000-bc5ac9f376e4
  Args:
    source: King_Alfonso_XIII
    type: :Person
  AddTriple (a817529c-5689-400b-bb0b-f7f25bf5f579)
 Call ID: a817529c-5689-400b-bb0b-f7f25bf5f579
  Args:
    target: Infanta_Beatriz_of_Spain
    source: King_Alfonso_XIII
    relation: :isFatherOf
  AddTriple (f3f15431-14f0-46b8-88c7-49ebc11861ad)
 Call ID: f3f15431-14f0-46b8-88c7-49ebc11861ad
  Args:
    source: King_Alfonso_XIII
    target: Infante_Juan_Count_of_Barcelona
    relation: :isFatherOf
  AssignClass (0a069e7c-8995-4ebc-a694-e7071ce0ae3b)
 Call ID: 0a069e7c-8995-4ebc-a694-e7071ce0ae3b
  Args:
    type: :Man
    source: Alessandro_Torlonia
  AssignClass (3ea047ec-038a-49c9-9070-1c4c8f306f65)
 Call ID: 3ea047ec-038a-49c9-9070-1c4c8f306f65
  Args:
    source: Alessandro_Torlonia
    type: :Person
  AddTriple (c9a0fa93-de39-4302-8611-588fc3d44fba)
 Call ID: c9a0fa93-de39-4302-8611-588fc3d44fba
  Args:
    target: Alessandro_Torlonia
    source: Infanta_Beatriz_of_Spain
    relation: :hasRelation
  AssignClass (7da3c50a-8fc2-4401-98bf-6daab601c1b2)
 Call ID: 7da3c50a-8fc2-4401-98bf-6daab601c1b2
  Args:
    type: :Woman
    source: Queen_Victoria_Eugenie
  AssignClass (ab224574-9be4-4486-b539-99890dfbbc76)
 Call ID: ab224574-9be4-4486-b539-99890dfbbc76
  Args:
    type: :Person
    source: Queen_Victoria_Eugenie
  AddTriple (38c3e955-9311-49f5-90d3-79d090380670)
 Call ID: 38c3e955-9311-49f5-90d3-79d090380670
  Args:
    relation: :isMotherOf
    source: Queen_Victoria_Eugenie
    target: Infante_Juan_Count_of_Barcelona
  AssignClass (c44d6961-e1f1-4385-a8ab-caaf25009192)
 Call ID: c44d6961-e1f1-4385-a8ab-caaf25009192
  Args:
    source: Infanta_Elena
    type: :Woman
  AssignClass (fdcdc508-7cf5-4174-9e7f-9d4d550b1d2a)
 Call ID: fdcdc508-7cf5-4174-9e7f-9d4d550b1d2a
  Args:
    source: Infanta_Elena
    type: :Person
  AddTriple (1ad9d44f-e2ec-4978-89d9-3bfcae5fd83a)
 Call ID: 1ad9d44f-e2ec-4978-89d9-3bfcae5fd83a
  Args:
    relation: :isMotherOf
    source: Juan_Carlos_I
    target: Infanta_Elena
  Finish (07879c3b-bfa0-4320-ab34-3cf1a19fc51c)
 Call ID: 07879c3b-bfa0-4320-ab34-3cf1a19fc51c
  Args: