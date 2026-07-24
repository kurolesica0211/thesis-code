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
Prince Ernst August of Lippe (German: Prinz Ernst August Bernhard Alexander Eduard Friedrich Wilhelm zur Lippe; 1 April 1917 – 15 June 1990) was a claimant to the headship of the House of Lippe.
Early life

Prince Ernst August was born at Dresden, Kingdom of Saxony, the second child and first son of Prince Julius Ernst of Lippe  (1873–1952; son of Ernst, Count of Lippe-Biesterfeld and Countess Caroline von Wartensleben) and his wife, Duchess Marie of Mecklenburg-Strelitz (1878–1948; daughter of Adolphus Frederick V, Grand Duke of Mecklenburg-Strelitz and his wife Princess Elisabeth of Anhalt).
Through his father he was first cousin of Prince Bernhard, consort to Queen Juliana of the Netherlands, and was a guest at their 1937 wedding.
Marriage

Ernst August married on 3 March 1948 in Oberkassel, Bonn to Christa von Arnim (b. 2 July 1923-20 February 2020), elder daughter of Curt David von Arnim, and his wife, Stephanie von Stechow.
They had four children:


House of Lippe

On 30 December 1949 his younger half-brother Prince Armin succeeded his father Leopold IV as head of the House of Lippe.
On 22 March 1953, he renounced his position in favour of his older half brother Prince Leopold.
Prince Leopold later in 1958 renounced the headship in favour of his older brother Hereditary Prince Ernst.
Later that year the Hereditary Prince called a family council where it was agreed by the princes in attendance that the oldest prince living in Germany would be head of the house.
So the position was taken by Prince Simon Casimir (1900–1980).
Prince Ernst August changed his mind, believing all princes of the house, not just those living in Germany, should be considered.
Ernst August died in 1990 and his son Prince Friedrich Wilhelm has continued his claim.
Prince Armin, who said he did not think his decision in 1953 was irrevocable, also claimed to be head of the house until his death in 2015, with his son Stephan, Prince of Lippe continuing his claim.
Prince Ernst August grew up and lived at Lippesches Palais in Oberkassel, Bonn, which had been home to the Lippe-Biesterfeld family for the past 209 years.
In 1970 he also acquired Syburg castle at Bergen, Middle Franconia, which however he was forced to auction in 1977, followed by the sale of Lippe House in 1979.



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
  AssignClass (9091376e-cd67-468b-b350-694a8cf7bee1)
 Call ID: 9091376e-cd67-468b-b350-694a8cf7bee1
  Args:
    type: :Man
    source: Ernst_August_of_Lippe
  AssignClass (99d65130-4e2e-40de-a797-ede34073c82d)
 Call ID: 99d65130-4e2e-40de-a797-ede34073c82d
  Args:
    type: :Person
    source: Ernst_August_of_Lippe
  AddLiteral (ad865846-2789-4c41-ad7b-631685a6677c)
 Call ID: ad865846-2789-4c41-ad7b-631685a6677c
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1917
    source: Ernst_August_of_Lippe
  AddLiteral (068c9087-6f81-4cc9-af70-030d29ede6e0)
 Call ID: 068c9087-6f81-4cc9-af70-030d29ede6e0
  Args:
    literal_value: 1990
    source: Ernst_August_of_Lippe
    relation: :hasDeathYear
    literal_type: xsd:integer
  AssignClass (2b92f777-aa4d-42bc-b496-fc51f25797a6)
 Call ID: 2b92f777-aa4d-42bc-b496-fc51f25797a6
  Args:
    type: :Man
    source: Julius_Ernst_of_Lippe
  AssignClass (ff463f79-b39a-4f8e-971e-8b0a4f3e930b)
 Call ID: ff463f79-b39a-4f8e-971e-8b0a4f3e930b
  Args:
    type: :Ancestor
    source: Julius_Ernst_of_Lippe
  AddLiteral (4577775a-cb4a-46ee-ab30-64a418494d20)
 Call ID: 4577775a-cb4a-46ee-ab30-64a418494d20
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1873
    source: Julius_Ernst_of_Lippe
  AddLiteral (420031a6-9567-43a5-bc34-4be73a5dd4b3)
 Call ID: 420031a6-9567-43a5-bc34-4be73a5dd4b3
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: Julius_Ernst_of_Lippe
    literal_value: 1952
  AddTriple (f75c2c85-4132-4416-bf2a-53ebe0f3d6f7)
 Call ID: f75c2c85-4132-4416-bf2a-53ebe0f3d6f7
  Args:
    relation: :isSonOf
    target: Julius_Ernst_of_Lippe
    source: Ernst_August_of_Lippe
  AssignClass (abd619d1-aa4d-4b31-ab37-7e42ab920567)
 Call ID: abd619d1-aa4d-4b31-ab37-7e42ab920567
  Args:
    type: :Woman
    source: Marie_of_Mecklenburg-Strelitz
  AssignClass (9490502a-10a7-4d25-a525-2853eee5d227)
 Call ID: 9490502a-10a7-4d25-a525-2853eee5d227
  Args:
    type: :Ancestor
    source: Marie_of_Mecklenburg-Strelitz
  AddLiteral (55283c68-9729-4ec0-8605-98763edd66ac)
 Call ID: 55283c68-9729-4ec0-8605-98763edd66ac
  Args:
    source: Marie_of_Mecklenburg-Strelitz
    literal_value: 1878
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (2b9b8ae3-d18f-4d7a-bfb7-bc90a0e138fb)
 Call ID: 2b9b8ae3-d18f-4d7a-bfb7-bc90a0e138fb
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: Marie_of_Mecklenburg-Strelitz
    literal_value: 1948
  AddTriple (6a447e0f-ee54-4826-81c1-3f0d2b336dc3)
 Call ID: 6a447e0f-ee54-4826-81c1-3f0d2b336dc3
  Args:
    relation: :isChildOf
    target: Marie_of_Mecklenburg-Strelitz
    source: Ernst_August_of_Lippe
  AssignClass (34ed616f-ff5e-46ec-a65b-fb6201e52617)
 Call ID: 34ed616f-ff5e-46ec-a65b-fb6201e52617
  Args:
    type: :Man
    source: Ernst_Count_of_Lippe-Biesterfeld
  AssignClass (8bd08057-aa50-427f-b7cf-ab42ece2674c)
 Call ID: 8bd08057-aa50-427f-b7cf-ab42ece2674c
  Args:
    type: :Ancestor
    source: Ernst_Count_of_Lippe-Biesterfeld
  AddTriple (852d8e2a-a76a-4a99-9a12-f2325f327b13)
 Call ID: 852d8e2a-a76a-4a99-9a12-f2325f327b13
  Args:
    source: Ernst_Count_of_Lippe-Biesterfeld
    target: Julius_Ernst_of_Lippe
    relation: :isFatherOf
  AssignClass (4815919f-974c-4b2d-afcb-4a0d32f5026e)
 Call ID: 4815919f-974c-4b2d-afcb-4a0d32f5026e
  Args:
    type: :Woman
    source: Caroline_von_Wartensleben
  AssignClass (5c7f3e98-3981-44d9-b528-cc2620fc8769)
 Call ID: 5c7f3e98-3981-44d9-b528-cc2620fc8769
  Args:
    type: :Ancestor
    source: Caroline_von_Wartensleben
  AddTriple (2f1753b6-cd98-4b10-8b65-8f49377271ee)
 Call ID: 2f1753b6-cd98-4b10-8b65-8f49377271ee
  Args:
    source: Caroline_von_Wartensleben
    target: Julius_Ernst_of_Lippe
    relation: :isMotherOf
  AssignClass (f0d232aa-283d-483c-b886-54c9784ef53b)
 Call ID: f0d232aa-283d-483c-b886-54c9784ef53b
  Args:
    type: :Man
    source: Adolphus_Frederick_V_Grand_Duke_of_Mecklenburg-Strelitz
  AssignClass (4115875f-3927-402f-8f4b-b6549156ca44)
 Call ID: 4115875f-3927-402f-8f4b-b6549156ca44
  Args:
    type: :Ancestor
    source: Adolphus_Frederick_V_Grand_Duke_of_Mecklenburg-Strelitz
  AddTriple (1a2c9e2b-a43c-4d22-99a5-26a24cfa6d7e)
 Call ID: 1a2c9e2b-a43c-4d22-99a5-26a24cfa6d7e
  Args:
    relation: :isFatherOf
    target: Marie_of_Mecklenburg-Strelitz
    source: Adolphus_Frederick_V_Grand_Duke_of_Mecklenburg-Strelitz
  AssignClass (bfc6e2cc-f264-427d-856e-ca4aacce3077)
 Call ID: bfc6e2cc-f264-427d-856e-ca4aacce3077
  Args:
    type: :Woman
    source: Elisabeth_of_Anhalt
  AssignClass (68563e9a-7b5f-43e2-b81b-3cd03b5aa725)
 Call ID: 68563e9a-7b5f-43e2-b81b-3cd03b5aa725
  Args:
    type: :Ancestor
    source: Elisabeth_of_Anhalt
  AddTriple (a55acad4-0176-4066-82a2-3a8ae14694f2)
 Call ID: a55acad4-0176-4066-82a2-3a8ae14694f2
  Args:
    target: Marie_of_Mecklenburg-Strelitz
    source: Elisabeth_of_Anhalt
    relation: :isMotherOf
  AssignClass (f67786cb-3bfb-494b-a690-e19dccd806e8)
 Call ID: f67786cb-3bfb-494b-a690-e19dccd806e8
  Args:
    type: :Woman
    source: Christa_von_Arnim
  AssignClass (e089a678-2a4c-429e-b321-2a37b01654dc)
 Call ID: e089a678-2a4c-429e-b321-2a37b01654dc
  Args:
    type: :Person
    source: Christa_von_Arnim
  AddLiteral (2f8581f2-c735-4e8c-bea8-36e4f1e487c5)
 Call ID: 2f8581f2-c735-4e8c-bea8-36e4f1e487c5
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 1948
    source: Ernst_August_of_Lippe
  AddTriple (62e9ec9a-d046-4efd-a51b-0aabb35c7abb)
 Call ID: 62e9ec9a-d046-4efd-a51b-0aabb35c7abb
  Args:
    relation: :hasRelation
    target: Christa_von_Arnim
    source: Ernst_August_of_Lippe
  AssignClass (155de0ce-5303-425d-9c8b-29cbd93ebba1)
 Call ID: 155de0ce-5303-425d-9c8b-29cbd93ebba1
  Args:
    type: :Man
    source: Curt_David_von_Arnim
  AssignClass (85406d1d-1d60-479c-b168-766a55eddce2)
 Call ID: 85406d1d-1d60-479c-b168-766a55eddce2
  Args:
    type: :Ancestor
    source: Curt_David_von_Arnim
  AddTriple (563af583-904a-4e3e-905b-e41442e10fd9)
 Call ID: 563af583-904a-4e3e-905b-e41442e10fd9
  Args:
    target: Christa_von_Arnim
    source: Curt_David_von_Arnim
    relation: :isFatherOf
  AssignClass (086c9f71-05a2-46d5-bef0-54f28b12c501)
 Call ID: 086c9f71-05a2-46d5-bef0-54f28b12c501
  Args:
    type: :Woman
    source: Stephanie_von_Stechow
  AssignClass (4773c4d7-890f-4e6a-8c7f-6b124375b5b6)
 Call ID: 4773c4d7-890f-4e6a-8c7f-6b124375b5b6
  Args:
    type: :Ancestor
    source: Stephanie_von_Stechow
  AddTriple (2913003a-3cdb-4fd4-876e-8721c0114134)
 Call ID: 2913003a-3cdb-4fd4-876e-8721c0114134
  Args:
    target: Christa_von_Arnim
    source: Stephanie_von_Stechow
    relation: :isMotherOf
  AssignClass (273b157d-1215-4092-aec5-c3821a7ec464)
 Call ID: 273b157d-1215-4092-aec5-c3821a7ec464
  Args:
    type: :Man
    source: Armin_of_Lippe
  AssignClass (2f4b2f3e-af09-405c-976a-0eab8392e814)
 Call ID: 2f4b2f3e-af09-405c-976a-0eab8392e814
  Args:
    type: :Person
    source: Armin_of_Lippe
  AddTriple (2b3a9074-19b5-445a-a2c6-c44cadbd63b7)
 Call ID: 2b3a9074-19b5-445a-a2c6-c44cadbd63b7
  Args:
    source: Armin_of_Lippe
    target: Ernst_August_of_Lippe
    relation: :isSiblingOf
  AssignClass (e258d7e5-41cd-4cff-b051-584d658a4148)
 Call ID: e258d7e5-41cd-4cff-b051-584d658a4148
  Args:
    type: :Man
    source: Leopold_IV_of_Lippe
  AssignClass (37fe8601-59de-4898-a96f-a2a91bb9708c)
 Call ID: 37fe8601-59de-4898-a96f-a2a91bb9708c
  Args:
    type: :Ancestor
    source: Leopold_IV_of_Lippe
  AddTriple (df22e671-134e-47c6-a215-7d83b0fc4319)
 Call ID: df22e671-134e-47c6-a215-7d83b0fc4319
  Args:
    relation: :isFatherOf
    source: Leopold_IV_of_Lippe
    target: Armin_of_Lippe
  AssignClass (5cc2d627-a1d9-4b93-be50-7b5130cb5ff5)
 Call ID: 5cc2d627-a1d9-4b93-be50-7b5130cb5ff5
  Args:
    type: :Man
    source: Leopold_of_Lippe
  AssignClass (38389333-daec-4047-a56d-42eae0c041f2)
 Call ID: 38389333-daec-4047-a56d-42eae0c041f2
  Args:
    type: :Person
    source: Leopold_of_Lippe
  AddTriple (ba253df9-8739-421c-8410-cd48615d6e9f)
 Call ID: ba253df9-8739-421c-8410-cd48615d6e9f
  Args:
    relation: :isSiblingOf
    target: Ernst_August_of_Lippe
    source: Leopold_of_Lippe
  AssignClass (e8713e5a-f33e-4cd5-8a46-f5828f8c618e)
 Call ID: e8713e5a-f33e-4cd5-8a46-f5828f8c618e
  Args:
    type: :Man
    source: Simon_Casimir_of_Lippe
  AssignClass (619ca38a-6470-4a83-bfce-e95367e1264d)
 Call ID: 619ca38a-6470-4a83-bfce-e95367e1264d
  Args:
    type: :Person
    source: Simon_Casimir_of_Lippe
  AssignClass (cf3f82cc-7931-48da-a551-c84d319f0fde)
 Call ID: cf3f82cc-7931-48da-a551-c84d319f0fde
  Args:
    type: :Man
    source: Friedrich_Wilhelm_of_Lippe
  AssignClass (f942efad-1905-4d8e-9709-8c05fec2fe8d)
 Call ID: f942efad-1905-4d8e-9709-8c05fec2fe8d
  Args:
    type: :Person
    source: Friedrich_Wilhelm_of_Lippe
  AddTriple (959b3779-7434-4fd7-9bbe-9e0d07e3eeca)
 Call ID: 959b3779-7434-4fd7-9bbe-9e0d07e3eeca
  Args:
    relation: :isSonOf
    target: Ernst_August_of_Lippe
    source: Friedrich_Wilhelm_of_Lippe
  AssignClass (8219c1a7-d5bf-411c-b773-f2e18b3b4d8e)
 Call ID: 8219c1a7-d5bf-411c-b773-f2e18b3b4d8e
  Args:
    type: :Man
    source: Stephan_of_Lippe
  AssignClass (9d558169-c4fc-4edf-9d39-bf1cd962902b)
 Call ID: 9d558169-c4fc-4edf-9d39-bf1cd962902b
  Args:
    type: :Person
    source: Stephan_of_Lippe
  AddTriple (0ef17d3f-a09e-4522-a27a-d5da8dd02455)
 Call ID: 0ef17d3f-a09e-4522-a27a-d5da8dd02455
  Args:
    source: Stephan_of_Lippe
    target: Armin_of_Lippe
    relation: :isSonOf
  Finish (12b5f424-bf77-491b-850a-105457f6b0f0)
 Call ID: 12b5f424-bf77-491b-850a-105457f6b0f0
  Args: