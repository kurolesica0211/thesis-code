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
  AssignClass (e54a3ac1-596b-4b5b-8afd-9045f3364fc2)
 Call ID: e54a3ac1-596b-4b5b-8afd-9045f3364fc2
  Args:
    type: :Man
    source: Ernst_August_of_Lippe
  AssignClass (91a2d652-4692-42aa-bf09-8ec9ff5d07bb)
 Call ID: 91a2d652-4692-42aa-bf09-8ec9ff5d07bb
  Args:
    type: :Person
    source: Ernst_August_of_Lippe
  AddLiteral (51b7ea9d-7d6c-4109-9099-ccc58dc27e39)
 Call ID: 51b7ea9d-7d6c-4109-9099-ccc58dc27e39
  Args:
    source: Ernst_August_of_Lippe
    literal_value: 1917
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (4349e2c5-a1d8-4c8e-ab69-7cc68ed58e4d)
 Call ID: 4349e2c5-a1d8-4c8e-ab69-7cc68ed58e4d
  Args:
    literal_type: xsd:integer
    source: Ernst_August_of_Lippe
    relation: :hasDeathYear
    literal_value: 1990
  AssignClass (9028199b-ea39-4edc-8926-9a72e49fba54)
 Call ID: 9028199b-ea39-4edc-8926-9a72e49fba54
  Args:
    type: :Man
    source: Julius_Ernst_of_Lippe
  AssignClass (884619ee-94aa-40a8-9cd5-3a0fe9a07a12)
 Call ID: 884619ee-94aa-40a8-9cd5-3a0fe9a07a12
  Args:
    type: :Person
    source: Julius_Ernst_of_Lippe
  AddLiteral (a8835adf-f53c-410b-9efc-681d7a097b6b)
 Call ID: a8835adf-f53c-410b-9efc-681d7a097b6b
  Args:
    source: Julius_Ernst_of_Lippe
    relation: :hasBirthYear
    literal_value: 1873
    literal_type: xsd:integer
  AddLiteral (1a1264a6-449e-4355-99f0-1c23fd550f30)
 Call ID: 1a1264a6-449e-4355-99f0-1c23fd550f30
  Args:
    source: Julius_Ernst_of_Lippe
    relation: :hasDeathYear
    literal_value: 1952
    literal_type: xsd:integer
  AssignClass (7e1ba4df-98db-4ed5-b09d-f0631eea8b78)
 Call ID: 7e1ba4df-98db-4ed5-b09d-f0631eea8b78
  Args:
    type: :Woman
    source: Marie_of_Mecklenburg-Strelitz
  AssignClass (57cd8fab-e793-429c-a3bf-eede3cf360f5)
 Call ID: 57cd8fab-e793-429c-a3bf-eede3cf360f5
  Args:
    type: :Person
    source: Marie_of_Mecklenburg-Strelitz
  AddLiteral (717afc0f-f60c-4931-8162-9e0169e0d159)
 Call ID: 717afc0f-f60c-4931-8162-9e0169e0d159
  Args:
    literal_type: xsd:integer
    literal_value: 1878
    relation: :hasBirthYear
    source: Marie_of_Mecklenburg-Strelitz
  AddLiteral (bb0dbad2-506d-4d24-9c7c-7adc6f33d69e)
 Call ID: bb0dbad2-506d-4d24-9c7c-7adc6f33d69e
  Args:
    literal_type: xsd:integer
    source: Marie_of_Mecklenburg-Strelitz
    literal_value: 1948
    relation: :hasDeathYear
  AddTriple (2b3a18ae-08d5-4c67-bc9f-2e07747442d9)
 Call ID: 2b3a18ae-08d5-4c67-bc9f-2e07747442d9
  Args:
    relation: :hasFather
    source: Ernst_August_of_Lippe
    target: Julius_Ernst_of_Lippe
  AddTriple (7dd9023e-4750-4667-bba0-390d267dc5a1)
 Call ID: 7dd9023e-4750-4667-bba0-390d267dc5a1
  Args:
    target: Marie_of_Mecklenburg-Strelitz
    source: Ernst_August_of_Lippe
    relation: :hasMother
  AssignClass (0530350a-d048-4fa1-855a-b5aad14026a9)
 Call ID: 0530350a-d048-4fa1-855a-b5aad14026a9
  Args:
    type: :Man
    source: Ernst_Count_of_Lippe-Biesterfeld
  AssignClass (27db26ee-3beb-4597-b350-97365e7740b7)
 Call ID: 27db26ee-3beb-4597-b350-97365e7740b7
  Args:
    type: :Person
    source: Ernst_Count_of_Lippe-Biesterfeld
  AssignClass (245231db-977f-4d17-8f90-facd690ad831)
 Call ID: 245231db-977f-4d17-8f90-facd690ad831
  Args:
    type: :Woman
    source: Caroline_von_Wartensleben
  AssignClass (02af4a6f-152a-4899-b53c-25032b9df662)
 Call ID: 02af4a6f-152a-4899-b53c-25032b9df662
  Args:
    type: :Person
    source: Caroline_von_Wartensleben
  AddTriple (105e52d9-1b14-4a7e-9c84-43cfebef1571)
 Call ID: 105e52d9-1b14-4a7e-9c84-43cfebef1571
  Args:
    target: Ernst_Count_of_Lippe-Biesterfeld
    source: Julius_Ernst_of_Lippe
    relation: :hasFather
  AddTriple (7593072c-2a41-4c87-a6e7-46bd971e9b29)
 Call ID: 7593072c-2a41-4c87-a6e7-46bd971e9b29
  Args:
    target: Caroline_von_Wartensleben
    source: Julius_Ernst_of_Lippe
    relation: :hasMother
  AssignClass (e3e07cae-fd7f-4230-85a6-d5030d7a0c0e)
 Call ID: e3e07cae-fd7f-4230-85a6-d5030d7a0c0e
  Args:
    type: :Man
    source: Adolphus_Frederick_V_Grand_Duke_of_Mecklenburg-Strelitz
  AssignClass (8857697b-6f3a-45f7-8e09-2df91bb5d74b)
 Call ID: 8857697b-6f3a-45f7-8e09-2df91bb5d74b
  Args:
    type: :Person
    source: Adolphus_Frederick_V_Grand_Duke_of_Mecklenburg-Strelitz
  AssignClass (f41ba589-15f0-4423-b6e9-700361be7b1d)
 Call ID: f41ba589-15f0-4423-b6e9-700361be7b1d
  Args:
    type: :Woman
    source: Elisabeth_of_Anhalt
  AssignClass (1359b210-49d6-4d60-bc18-fab5c17e6c45)
 Call ID: 1359b210-49d6-4d60-bc18-fab5c17e6c45
  Args:
    type: :Person
    source: Elisabeth_of_Anhalt
  AddTriple (924ba5c7-95dd-44c6-a961-1721c192dec3)
 Call ID: 924ba5c7-95dd-44c6-a961-1721c192dec3
  Args:
    target: Adolphus_Frederick_V_Grand_Duke_of_Mecklenburg-Strelitz
    source: Marie_of_Mecklenburg-Strelitz
    relation: :hasFather
  AddTriple (16b991e2-ddeb-47ad-8c65-5de4810a0b1c)
 Call ID: 16b991e2-ddeb-47ad-8c65-5de4810a0b1c
  Args:
    target: Elisabeth_of_Anhalt
    relation: :hasMother
    source: Marie_of_Mecklenburg-Strelitz
  AssignClass (ee948f67-aa47-42a6-a586-fac9b3ca6600)
 Call ID: ee948f67-aa47-42a6-a586-fac9b3ca6600
  Args:
    type: :Woman
    source: Christa_von_Arnim
  AssignClass (016cad53-83ad-430e-9eb2-e2fe240c7641)
 Call ID: 016cad53-83ad-430e-9eb2-e2fe240c7641
  Args:
    type: :Person
    source: Christa_von_Arnim
  AddLiteral (4311fc26-ece6-42e0-9354-242cede65b8d)
 Call ID: 4311fc26-ece6-42e0-9354-242cede65b8d
  Args:
    relation: :hasMarriageYear
    literal_value: 1948
    source: Ernst_August_of_Lippe
    literal_type: xsd:integer
  AddTriple (53caea2d-8149-4d57-bff4-9056e8cb97c8)
 Call ID: 53caea2d-8149-4d57-bff4-9056e8cb97c8
  Args:
    relation: :hasRelation
    source: Ernst_August_of_Lippe
    target: Christa_von_Arnim
  AssignClass (9a8e548b-3d90-45dc-a599-e060ed2bfd96)
 Call ID: 9a8e548b-3d90-45dc-a599-e060ed2bfd96
  Args:
    type: :Man
    source: Curt_David_von_Arnim
  AssignClass (99fe368c-b046-4250-b3cb-7bca7a188bb1)
 Call ID: 99fe368c-b046-4250-b3cb-7bca7a188bb1
  Args:
    type: :Person
    source: Curt_David_von_Arnim
  AssignClass (8e393832-9a06-4401-ab9e-32a81066cdaf)
 Call ID: 8e393832-9a06-4401-ab9e-32a81066cdaf
  Args:
    type: :Woman
    source: Stephanie_von_Stechow
  AssignClass (8e696378-23a3-468d-998e-2caf6bbaaf49)
 Call ID: 8e696378-23a3-468d-998e-2caf6bbaaf49
  Args:
    type: :Person
    source: Stephanie_von_Stechow
  AddTriple (e226a695-1020-47fa-9bde-961cb913fba5)
 Call ID: e226a695-1020-47fa-9bde-961cb913fba5
  Args:
    target: Curt_David_von_Arnim
    source: Christa_von_Arnim
    relation: :hasFather
  AddTriple (9a7bc0c1-312e-4123-8bdb-257624627d7f)
 Call ID: 9a7bc0c1-312e-4123-8bdb-257624627d7f
  Args:
    target: Stephanie_von_Stechow
    source: Christa_von_Arnim
    relation: :hasMother
  AssignClass (6471df80-3c88-432e-912a-38369529a337)
 Call ID: 6471df80-3c88-432e-912a-38369529a337
  Args:
    type: :Man
    source: Armin_of_Lippe
  AssignClass (96adc585-828b-4605-8530-e803a9cb5d06)
 Call ID: 96adc585-828b-4605-8530-e803a9cb5d06
  Args:
    type: :Person
    source: Armin_of_Lippe
  AddTriple (31fa4ba6-c706-470b-9e80-2341653eec35)
 Call ID: 31fa4ba6-c706-470b-9e80-2341653eec35
  Args:
    target: Armin_of_Lippe
    source: Ernst_August_of_Lippe
    relation: :isSiblingOf
  AssignClass (8d1702ca-e7bf-49f1-ac4e-32488c0dbd3a)
 Call ID: 8d1702ca-e7bf-49f1-ac4e-32488c0dbd3a
  Args:
    type: :Man
    source: Leopold_IV_of_Lippe
  AssignClass (ba204d82-28f7-4035-aa81-92c425e0e84e)
 Call ID: ba204d82-28f7-4035-aa81-92c425e0e84e
  Args:
    type: :Person
    source: Leopold_IV_of_Lippe
  AddTriple (a0d326ed-3f75-48c5-9337-881b49ed4e93)
 Call ID: a0d326ed-3f75-48c5-9337-881b49ed4e93
  Args:
    target: Armin_of_Lippe
    relation: :isFatherOf
    source: Leopold_IV_of_Lippe
  AssignClass (56bd4a98-9ecc-49b2-83fa-df74c6f2a04f)
 Call ID: 56bd4a98-9ecc-49b2-83fa-df74c6f2a04f
  Args:
    type: :Man
    source: Leopold_of_Lippe
  AssignClass (1b675e8f-10f9-44e8-a8c9-1d0740fd2cef)
 Call ID: 1b675e8f-10f9-44e8-a8c9-1d0740fd2cef
  Args:
    type: :Person
    source: Leopold_of_Lippe
  AddTriple (7c5fae1a-02a8-45d0-8c24-3f13fb326b3c)
 Call ID: 7c5fae1a-02a8-45d0-8c24-3f13fb326b3c
  Args:
    source: Ernst_August_of_Lippe
    relation: :isSiblingOf
    target: Leopold_of_Lippe
  AssignClass (da4cb4a7-2b19-4791-82d3-efd960ea3b26)
 Call ID: da4cb4a7-2b19-4791-82d3-efd960ea3b26
  Args:
    type: :Man
    source: Simon_Casimir_of_Lippe
  AssignClass (3f7ecd1a-0d83-49af-950d-6e286a2e5887)
 Call ID: 3f7ecd1a-0d83-49af-950d-6e286a2e5887
  Args:
    type: :Person
    source: Simon_Casimir_of_Lippe
  AddLiteral (d199bfe8-4508-4d27-a52f-93dd059a6d54)
 Call ID: d199bfe8-4508-4d27-a52f-93dd059a6d54
  Args:
    source: Simon_Casimir_of_Lippe
    literal_value: 1900
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (66c59ac7-00ea-4348-af21-fe05987ede60)
 Call ID: 66c59ac7-00ea-4348-af21-fe05987ede60
  Args:
    literal_type: xsd:integer
    literal_value: 1980
    relation: :hasDeathYear
    source: Simon_Casimir_of_Lippe
  AssignClass (8bc09dd2-b3ba-4449-8e8f-6ccef2379b17)
 Call ID: 8bc09dd2-b3ba-4449-8e8f-6ccef2379b17
  Args:
    type: :Man
    source: Friedrich_Wilhelm_of_Lippe
  AssignClass (8a47a514-cee3-4ae9-80fd-41b5ab2fbad1)
 Call ID: 8a47a514-cee3-4ae9-80fd-41b5ab2fbad1
  Args:
    type: :Person
    source: Friedrich_Wilhelm_of_Lippe
  AddTriple (cd942de3-da23-4f2a-9bf5-4561eae0e524)
 Call ID: cd942de3-da23-4f2a-9bf5-4561eae0e524
  Args:
    source: Friedrich_Wilhelm_of_Lippe
    relation: :isSonOf
    target: Ernst_August_of_Lippe
  AssignClass (3b6ef766-343f-4c1a-8b00-a098374f50ca)
 Call ID: 3b6ef766-343f-4c1a-8b00-a098374f50ca
  Args:
    type: :Man
    source: Stephan_of_Lippe
  AssignClass (196da780-f7ca-49dd-84f2-e5bd4ea87b5d)
 Call ID: 196da780-f7ca-49dd-84f2-e5bd4ea87b5d
  Args:
    type: :Person
    source: Stephan_of_Lippe
  AddTriple (b6875d5c-f0c9-4bf2-8ee0-44f591b18252)
 Call ID: b6875d5c-f0c9-4bf2-8ee0-44f591b18252
  Args:
    target: Armin_of_Lippe
    relation: :isSonOf
    source: Stephan_of_Lippe
  Finish (f913a802-dbe7-4a15-ba2b-8c4951bfcafc)
 Call ID: f913a802-dbe7-4a15-ba2b-8c4951bfcafc
  Args: