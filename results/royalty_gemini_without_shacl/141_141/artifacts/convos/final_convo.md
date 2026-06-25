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
  AssignClass (4309f432-57db-4e14-8680-40e84036f972)
 Call ID: 4309f432-57db-4e14-8680-40e84036f972
  Args:
    source: :ErnstAugustOfLippe
    type: :Man
  AssignClass (a9ba9901-9bd0-452a-a23f-79e56761340b)
 Call ID: a9ba9901-9bd0-452a-a23f-79e56761340b
  Args:
    source: :ErnstAugustOfLippe
    type: :Person
  AddLiteral (cc2b42ae-bde5-425c-a84e-8fa28307f006)
 Call ID: cc2b42ae-bde5-425c-a84e-8fa28307f006
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1917
    source: :ErnstAugustOfLippe
  AddLiteral (c9845e0d-3ed5-4cd6-9dc0-d14636690b45)
 Call ID: c9845e0d-3ed5-4cd6-9dc0-d14636690b45
  Args:
    source: :ErnstAugustOfLippe
    literal_value: 1990
    relation: :hasDeathYear
    literal_type: xsd:integer
  AssignClass (b1b81fd4-eb05-42f2-ab38-ff29cccdfa92)
 Call ID: b1b81fd4-eb05-42f2-ab38-ff29cccdfa92
  Args:
    source: :JuliusErnstOfLippe
    type: :Man
  AssignClass (94a1a2f8-f3ed-45af-869e-b18769cad62f)
 Call ID: 94a1a2f8-f3ed-45af-869e-b18769cad62f
  Args:
    source: :JuliusErnstOfLippe
    type: :Person
  AddLiteral (5a812a2a-6049-4b1f-97bf-ca602ab9ef0b)
 Call ID: 5a812a2a-6049-4b1f-97bf-ca602ab9ef0b
  Args:
    source: :JuliusErnstOfLippe
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1873
  AddLiteral (02349afb-cada-4e25-892a-059b180f3c78)
 Call ID: 02349afb-cada-4e25-892a-059b180f3c78
  Args:
    literal_value: 1952
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: :JuliusErnstOfLippe
  AddTriple (20692364-4d5c-452f-91d2-276653a2b7a1)
 Call ID: 20692364-4d5c-452f-91d2-276653a2b7a1
  Args:
    source: :ErnstAugustOfLippe
    relation: :hasFather
    target: :JuliusErnstOfLippe
  AssignClass (58a70609-c50a-4344-b405-93e9ba4a7911)
 Call ID: 58a70609-c50a-4344-b405-93e9ba4a7911
  Args:
    source: :MarieOfMecklenburgStrelitz
    type: :Woman
  AssignClass (7d78e0ce-43cc-4325-9720-a1edb174199d)
 Call ID: 7d78e0ce-43cc-4325-9720-a1edb174199d
  Args:
    source: :MarieOfMecklenburgStrelitz
    type: :Person
  AddLiteral (55b1517f-a724-468c-8d41-9c0e54ab9521)
 Call ID: 55b1517f-a724-468c-8d41-9c0e54ab9521
  Args:
    source: :MarieOfMecklenburgStrelitz
    relation: :hasBirthYear
    literal_value: 1878
    literal_type: xsd:integer
  AddLiteral (50502b3a-8160-468b-a221-44c7d234a419)
 Call ID: 50502b3a-8160-468b-a221-44c7d234a419
  Args:
    relation: :hasDeathYear
    literal_value: 1948
    literal_type: xsd:integer
    source: :MarieOfMecklenburgStrelitz
  AddTriple (9c8a29ce-9f20-40bb-8dbb-2be43731ba2b)
 Call ID: 9c8a29ce-9f20-40bb-8dbb-2be43731ba2b
  Args:
    source: :ErnstAugustOfLippe
    relation: :hasMother
    target: :MarieOfMecklenburgStrelitz
  AssignClass (9fc6f35a-d0eb-4e2c-8e34-d0ffb7d1c26b)
 Call ID: 9fc6f35a-d0eb-4e2c-8e34-d0ffb7d1c26b
  Args:
    source: :ErnstCountOfLippeBiesterfeld
    type: :Man
  AssignClass (80a19505-43a3-491b-86e6-704ded51a617)
 Call ID: 80a19505-43a3-491b-86e6-704ded51a617
  Args:
    source: :ErnstCountOfLippeBiesterfeld
    type: :Person
  AddTriple (806b3615-7aaa-4037-ae3e-2c9fe5b8f034)
 Call ID: 806b3615-7aaa-4037-ae3e-2c9fe5b8f034
  Args:
    target: :ErnstCountOfLippeBiesterfeld
    relation: :hasFather
    source: :JuliusErnstOfLippe
  AssignClass (b405fdfb-3904-45f0-bd29-5dedd42fa4ea)
 Call ID: b405fdfb-3904-45f0-bd29-5dedd42fa4ea
  Args:
    source: :CarolineVonWartensleben
    type: :Woman
  AssignClass (7f312d46-dbe8-4250-bf9a-3f3332dcb81b)
 Call ID: 7f312d46-dbe8-4250-bf9a-3f3332dcb81b
  Args:
    source: :CarolineVonWartensleben
    type: :Person
  AddTriple (30216b6d-8ad7-4a68-a198-2cdb1aa5eec6)
 Call ID: 30216b6d-8ad7-4a68-a198-2cdb1aa5eec6
  Args:
    source: :JuliusErnstOfLippe
    target: :CarolineVonWartensleben
    relation: :hasMother
  AssignClass (3d8709e1-81ed-4ff2-a75a-28f3db9ea684)
 Call ID: 3d8709e1-81ed-4ff2-a75a-28f3db9ea684
  Args:
    source: :AdolphusFrederickV
    type: :Man
  AssignClass (761a7f2c-4638-4163-b3e2-9b0bdf3efdd2)
 Call ID: 761a7f2c-4638-4163-b3e2-9b0bdf3efdd2
  Args:
    source: :AdolphusFrederickV
    type: :Person
  AddTriple (b3d14503-13fa-4d7d-b9a4-9df89da027c3)
 Call ID: b3d14503-13fa-4d7d-b9a4-9df89da027c3
  Args:
    source: :MarieOfMecklenburgStrelitz
    target: :AdolphusFrederickV
    relation: :hasFather
  AssignClass (98aab451-f1db-4136-8d83-666206554a35)
 Call ID: 98aab451-f1db-4136-8d83-666206554a35
  Args:
    source: :ElisabethOfAnhalt
    type: :Woman
  AssignClass (a568cb93-5a6c-48a1-ac40-49893c6eaa60)
 Call ID: a568cb93-5a6c-48a1-ac40-49893c6eaa60
  Args:
    source: :ElisabethOfAnhalt
    type: :Person
  AddTriple (c65e8d16-fe20-4f8b-a2be-c049c5443a0d)
 Call ID: c65e8d16-fe20-4f8b-a2be-c049c5443a0d
  Args:
    source: :MarieOfMecklenburgStrelitz
    relation: :hasMother
    target: :ElisabethOfAnhalt
  AssignClass (6591a727-21bc-4f0c-baca-c9ab28cbff90)
 Call ID: 6591a727-21bc-4f0c-baca-c9ab28cbff90
  Args:
    source: :ChristaVonArnim
    type: :Woman
  AssignClass (0efd1261-1b6b-4854-aa8f-30fe7509e58e)
 Call ID: 0efd1261-1b6b-4854-aa8f-30fe7509e58e
  Args:
    source: :ChristaVonArnim
    type: :Person
  AddLiteral (53f5222b-576c-4423-9084-e9f523da431d)
 Call ID: 53f5222b-576c-4423-9084-e9f523da431d
  Args:
    source: :ChristaVonArnim
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1923
  AddLiteral (cac5acc4-7ed1-402a-b3fc-4892082d29e2)
 Call ID: cac5acc4-7ed1-402a-b3fc-4892082d29e2
  Args:
    source: :ChristaVonArnim
    relation: :hasDeathYear
    literal_value: 2020
    literal_type: xsd:integer
  AddLiteral (62246666-8dab-422a-9996-61858324e155)
 Call ID: 62246666-8dab-422a-9996-61858324e155
  Args:
    literal_value: 1948
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: :ErnstAugustOfLippe
  AddTriple (44758d30-9324-4a44-991f-60689e88e944)
 Call ID: 44758d30-9324-4a44-991f-60689e88e944
  Args:
    relation: :hasRelation
    target: :ChristaVonArnim
    source: :ErnstAugustOfLippe
  AssignClass (d8f7aa84-89ef-4dfa-9eff-168aa9ef9548)
 Call ID: d8f7aa84-89ef-4dfa-9eff-168aa9ef9548
  Args:
    source: :CurtDavidVonArnim
    type: :Man
  AssignClass (c433a59a-5abb-409f-b96f-4d7e8d7327a8)
 Call ID: c433a59a-5abb-409f-b96f-4d7e8d7327a8
  Args:
    source: :CurtDavidVonArnim
    type: :Person
  AddTriple (a32de8de-a830-493d-9dfc-5b618fedf90c)
 Call ID: a32de8de-a830-493d-9dfc-5b618fedf90c
  Args:
    relation: :hasFather
    target: :CurtDavidVonArnim
    source: :ChristaVonArnim
  AssignClass (7f6c5c6f-e852-47d4-929c-6733517bc655)
 Call ID: 7f6c5c6f-e852-47d4-929c-6733517bc655
  Args:
    source: :StephanieVonStechow
    type: :Woman
  AssignClass (6dc0143c-ce76-4b3b-8123-65abdffd0f3e)
 Call ID: 6dc0143c-ce76-4b3b-8123-65abdffd0f3e
  Args:
    source: :StephanieVonStechow
    type: :Person
  AddTriple (7333ffdf-d3e7-4c15-a6a0-c52d1e49ad91)
 Call ID: 7333ffdf-d3e7-4c15-a6a0-c52d1e49ad91
  Args:
    source: :ChristaVonArnim
    relation: :hasMother
    target: :StephanieVonStechow
  AssignClass (6ec13afc-997b-4da4-b041-5e8b9e3ccf80)
 Call ID: 6ec13afc-997b-4da4-b041-5e8b9e3ccf80
  Args:
    source: :ArminOfLippe
    type: :Man
  AssignClass (20b600b9-d204-4bdf-8e0b-f9570ded0942)
 Call ID: 20b600b9-d204-4bdf-8e0b-f9570ded0942
  Args:
    source: :ArminOfLippe
    type: :Person
  AddTriple (448add1c-ebe8-4ff2-8f71-55e5971a72c3)
 Call ID: 448add1c-ebe8-4ff2-8f71-55e5971a72c3
  Args:
    source: :ErnstAugustOfLippe
    relation: :isSiblingOf
    target: :ArminOfLippe
  AssignClass (9d4a9309-3b95-4766-b58c-6b1ab484bee0)
 Call ID: 9d4a9309-3b95-4766-b58c-6b1ab484bee0
  Args:
    source: :LeopoldIV
    type: :Man
  AssignClass (7435e201-027a-406f-9d1a-adcda65dc1f2)
 Call ID: 7435e201-027a-406f-9d1a-adcda65dc1f2
  Args:
    source: :LeopoldIV
    type: :Person
  AddTriple (4023ae09-9814-485c-98f5-c70c6d7ff972)
 Call ID: 4023ae09-9814-485c-98f5-c70c6d7ff972
  Args:
    target: :LeopoldIV
    relation: :hasFather
    source: :ArminOfLippe
  AssignClass (2a7d085c-5aed-4a6d-b271-957de85e5323)
 Call ID: 2a7d085c-5aed-4a6d-b271-957de85e5323
  Args:
    source: :LeopoldOfLippe
    type: :Man
  AssignClass (c30ee8b9-397e-404c-ac8f-ac858a95e278)
 Call ID: c30ee8b9-397e-404c-ac8f-ac858a95e278
  Args:
    source: :LeopoldOfLippe
    type: :Person
  AddTriple (171eee3c-099d-4a56-8c80-b6d1d7069392)
 Call ID: 171eee3c-099d-4a56-8c80-b6d1d7069392
  Args:
    source: :ErnstAugustOfLippe
    target: :LeopoldOfLippe
    relation: :isSiblingOf
  AssignClass (3bdb24f7-10ff-4a61-87a6-721f56524541)
 Call ID: 3bdb24f7-10ff-4a61-87a6-721f56524541
  Args:
    source: :FriedrichWilhelmOfLippe
    type: :Man
  AssignClass (b45e45c9-720e-426b-b26d-4c459920c337)
 Call ID: b45e45c9-720e-426b-b26d-4c459920c337
  Args:
    source: :FriedrichWilhelmOfLippe
    type: :Person
  AddTriple (b7d35584-1696-4c5b-8f0b-58e20e32df37)
 Call ID: b7d35584-1696-4c5b-8f0b-58e20e32df37
  Args:
    source: :FriedrichWilhelmOfLippe
    target: :ErnstAugustOfLippe
    relation: :isSonOf
  AssignClass (891eb279-25b2-4196-9f54-d0c5153382b5)
 Call ID: 891eb279-25b2-4196-9f54-d0c5153382b5
  Args:
    source: :StephanOfLippe
    type: :Man
  AssignClass (9c8ede93-259c-4ce5-8107-8c5171d55517)
 Call ID: 9c8ede93-259c-4ce5-8107-8c5171d55517
  Args:
    source: :StephanOfLippe
    type: :Person
  AddTriple (cfd2f887-a70f-4038-b354-20b7102fd4bb)
 Call ID: cfd2f887-a70f-4038-b354-20b7102fd4bb
  Args:
    source: :StephanOfLippe
    relation: :isSonOf
    target: :ArminOfLippe
  Finish (48432e57-1d12-483c-bdf5-f24acc2fd1e1)
 Call ID: 48432e57-1d12-483c-bdf5-f24acc2fd1e1
  Args: