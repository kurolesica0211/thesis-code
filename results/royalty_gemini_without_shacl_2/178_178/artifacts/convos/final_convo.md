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
Klaus Felix von Amsberg (German: Klaus Felix Friedrich Leopold Gabriel Archim Julius August von Amsberg; 1 September 1890 – 19 December 1953) was a member of the German Niederer Adel (lower nobility) and father of Prince Claus of the Netherlands.
Early life

He was born at Rehna, Mecklenburg-Schwerin, German Empire (now Mecklenburg-Vorpommern, Germany), the first child of Wilhelm von Amsberg (1856–1929), by his marriage to Elise von Vieregg (1866–1951), member of an old aristocratic family.
Claus was from 1917 the steward of an estate after a failed venture in Africa as a planter.
Marriage

Claus married on 4 September 1924 at Hitzacker to Baroness Gösta von dem Bussche-Haddenhausen (26 January 1902 –
13 June 1996), daughter of Baron Georg von dem Bussche-Haddenhausen (1869–1923) and Baroness Gabriele von dem Bussche-Ippenburg (1877–1973).



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix ns1: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
@prefix ns2: <http://www.w3.org/2003/11/swrl#> .
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

ns1:isRuleEnabled a owl:AnnotationProperty .

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

:x a ns2:Variable .

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

:y a ns2:Variable .

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

[] a ns2:Imp ;
    rdfs:label "infer hasSon" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasBrother" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasSister" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (fa417660-1185-495d-97e1-5795a1a86af8)
 Call ID: fa417660-1185-495d-97e1-5795a1a86af8
  Args:
    source: Klaus_Felix_von_Amsberg
    type: :Man
  AssignClass (f61aaf8f-2b61-44fa-8e80-ded5584852f8)
 Call ID: f61aaf8f-2b61-44fa-8e80-ded5584852f8
  Args:
    type: :Person
    source: Klaus_Felix_von_Amsberg
  AddLiteral (125259b0-fffc-4df9-9777-8bd6ded8273c)
 Call ID: 125259b0-fffc-4df9-9777-8bd6ded8273c
  Args:
    literal_type: xsd:string
    source: Klaus_Felix_von_Amsberg
    relation: :alsoKnownAs
    literal_value: Klaus Felix Friedrich Leopold Gabriel Archim Julius August von Amsberg
  AddLiteral (6d3b55ce-036e-4ff7-9019-b978f4533918)
 Call ID: 6d3b55ce-036e-4ff7-9019-b978f4533918
  Args:
    literal_type: xsd:integer
    source: Klaus_Felix_von_Amsberg
    literal_value: 1890
    relation: :hasBirthYear
  AddLiteral (a25e33ce-41c8-49c5-a2b6-f3200453b073)
 Call ID: a25e33ce-41c8-49c5-a2b6-f3200453b073
  Args:
    relation: :hasDeathYear
    literal_value: 1953
    source: Klaus_Felix_von_Amsberg
    literal_type: xsd:integer
  AssignClass (eff092f7-beef-408b-be4b-6a13889375ea)
 Call ID: eff092f7-beef-408b-be4b-6a13889375ea
  Args:
    type: :Man
    source: Wilhelm_von_Amsberg
  AssignClass (2f3d5185-bbc2-42d3-b76a-45fe43ba91a8)
 Call ID: 2f3d5185-bbc2-42d3-b76a-45fe43ba91a8
  Args:
    type: :Person
    source: Wilhelm_von_Amsberg
  AddLiteral (c228db68-da2c-4b7d-bed0-1518d59e35c7)
 Call ID: c228db68-da2c-4b7d-bed0-1518d59e35c7
  Args:
    relation: :hasBirthYear
    literal_value: 1856
    source: Wilhelm_von_Amsberg
    literal_type: xsd:integer
  AddLiteral (d54b6166-ab37-4851-8d42-de21483be1d2)
 Call ID: d54b6166-ab37-4851-8d42-de21483be1d2
  Args:
    literal_type: xsd:integer
    source: Wilhelm_von_Amsberg
    relation: :hasDeathYear
    literal_value: 1929
  AssignClass (b0d96d70-81bb-4d59-a12c-e12ab72b5a6f)
 Call ID: b0d96d70-81bb-4d59-a12c-e12ab72b5a6f
  Args:
    type: :Woman
    source: Elise_von_Vieregg
  AssignClass (5a193cec-f8dd-43e1-b5ba-d24793a7c795)
 Call ID: 5a193cec-f8dd-43e1-b5ba-d24793a7c795
  Args:
    type: :Person
    source: Elise_von_Vieregg
  AddLiteral (669c84ce-35ea-4ce7-9f94-6a93151e51d9)
 Call ID: 669c84ce-35ea-4ce7-9f94-6a93151e51d9
  Args:
    literal_value: 1866
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Elise_von_Vieregg
  AddLiteral (61ff88a9-35a8-41ec-8763-a88975822b80)
 Call ID: 61ff88a9-35a8-41ec-8763-a88975822b80
  Args:
    source: Elise_von_Vieregg
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1951
  AddTriple (c84c848c-04f5-4b49-ac0b-f27d109a8b47)
 Call ID: c84c848c-04f5-4b49-ac0b-f27d109a8b47
  Args:
    target: Wilhelm_von_Amsberg
    relation: :hasFather
    source: Klaus_Felix_von_Amsberg
  AddTriple (c1935be1-8172-4293-b0a8-b8fbe6a6eab3)
 Call ID: c1935be1-8172-4293-b0a8-b8fbe6a6eab3
  Args:
    source: Klaus_Felix_von_Amsberg
    relation: :hasMother
    target: Elise_von_Vieregg
  AssignClass (f60a5e91-4a6a-4366-8ce3-af3f2b7a2c99)
 Call ID: f60a5e91-4a6a-4366-8ce3-af3f2b7a2c99
  Args:
    source: Prince_Claus_of_the_Netherlands
    type: :Man
  AssignClass (9b7811ec-8340-41ed-914f-6a6adbe80074)
 Call ID: 9b7811ec-8340-41ed-914f-6a6adbe80074
  Args:
    type: :Person
    source: Prince_Claus_of_the_Netherlands
  AddTriple (0f0f29ef-0d98-4619-8bdd-4db7a5e7e512)
 Call ID: 0f0f29ef-0d98-4619-8bdd-4db7a5e7e512
  Args:
    source: Prince_Claus_of_the_Netherlands
    relation: :hasFather
    target: Klaus_Felix_von_Amsberg
  AssignClass (bc63ce0d-ada3-4fff-9651-901aed1f296c)
 Call ID: bc63ce0d-ada3-4fff-9651-901aed1f296c
  Args:
    source: Gosta_von_dem_Bussche-Haddenhausen
    type: :Woman
  AssignClass (8b4516c9-0c77-4a1f-916b-5f405cb3a87f)
 Call ID: 8b4516c9-0c77-4a1f-916b-5f405cb3a87f
  Args:
    source: Gosta_von_dem_Bussche-Haddenhausen
    type: :Person
  AddLiteral (e1e30911-b283-4d7f-8d54-031cbdb2550a)
 Call ID: e1e30911-b283-4d7f-8d54-031cbdb2550a
  Args:
    literal_type: xsd:integer
    source: Gosta_von_dem_Bussche-Haddenhausen
    literal_value: 1902
    relation: :hasBirthYear
  AddLiteral (c737d8cd-9658-476e-8f5d-d385c41d1b1e)
 Call ID: c737d8cd-9658-476e-8f5d-d385c41d1b1e
  Args:
    literal_value: 1996
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: Gosta_von_dem_Bussche-Haddenhausen
  AddTriple (65137a54-fea0-4f03-9a06-061b8d18c079)
 Call ID: 65137a54-fea0-4f03-9a06-061b8d18c079
  Args:
    target: Gosta_von_dem_Bussche-Haddenhausen
    relation: :hasMarriageYear
    source: Klaus_Felix_von_Amsberg
  AddLiteral (7cdbaa6a-3cec-4fbf-affb-bccdb2d10084)
 Call ID: 7cdbaa6a-3cec-4fbf-affb-bccdb2d10084
  Args:
    literal_value: 1924
    relation: :hasMarriageYear
    source: Klaus_Felix_von_Amsberg
    literal_type: xsd:integer
  AssignClass (e8b1db9f-53ef-41b1-b1f5-41bdecc97db0)
 Call ID: e8b1db9f-53ef-41b1-b1f5-41bdecc97db0
  Args:
    source: Georg_von_dem_Bussche-Haddenhausen
    type: :Man
  AssignClass (15fa2e48-6d8f-4556-be64-9ed7f2b1dc5f)
 Call ID: 15fa2e48-6d8f-4556-be64-9ed7f2b1dc5f
  Args:
    source: Georg_von_dem_Bussche-Haddenhausen
    type: :Person
  AddLiteral (c243e09c-00fa-4b02-aec1-8c70ed0c07b6)
 Call ID: c243e09c-00fa-4b02-aec1-8c70ed0c07b6
  Args:
    literal_type: xsd:integer
    source: Georg_von_dem_Bussche-Haddenhausen
    literal_value: 1869
    relation: :hasBirthYear
  AddLiteral (122fd6a3-80ac-47c7-abfd-d878cff70bd0)
 Call ID: 122fd6a3-80ac-47c7-abfd-d878cff70bd0
  Args:
    literal_type: xsd:integer
    source: Georg_von_dem_Bussche-Haddenhausen
    relation: :hasDeathYear
    literal_value: 1923
  AssignClass (1dd05f8a-28b2-4f69-9a4a-a63c9569a4d6)
 Call ID: 1dd05f8a-28b2-4f69-9a4a-a63c9569a4d6
  Args:
    source: Gabriele_von_dem_Bussche-Ippenburg
    type: :Woman
  AssignClass (562c3806-91b2-48b6-9eb1-7f44ef06791a)
 Call ID: 562c3806-91b2-48b6-9eb1-7f44ef06791a
  Args:
    type: :Person
    source: Gabriele_von_dem_Bussche-Ippenburg
  AddLiteral (0a420153-9a18-4f97-81dd-81dbd0de027f)
 Call ID: 0a420153-9a18-4f97-81dd-81dbd0de027f
  Args:
    literal_type: xsd:integer
    source: Gabriele_von_dem_Bussche-Ippenburg
    literal_value: 1877
    relation: :hasBirthYear
  AddLiteral (1c344354-a942-4783-b434-e188e559b6ec)
 Call ID: 1c344354-a942-4783-b434-e188e559b6ec
  Args:
    literal_type: xsd:integer
    source: Gabriele_von_dem_Bussche-Ippenburg
    relation: :hasDeathYear
    literal_value: 1973
  AddTriple (b29d5d92-fdda-4459-8f96-b9f5463126a2)
 Call ID: b29d5d92-fdda-4459-8f96-b9f5463126a2
  Args:
    relation: :hasFather
    target: Georg_von_dem_Bussche-Haddenhausen
    source: Gosta_von_dem_Bussche-Haddenhausen
  AddTriple (c8ceaa2f-449c-4eab-a92f-0a5a586bfb77)
 Call ID: c8ceaa2f-449c-4eab-a92f-0a5a586bfb77
  Args:
    relation: :hasMother
    target: Gabriele_von_dem_Bussche-Ippenburg
    source: Gosta_von_dem_Bussche-Haddenhausen
  Finish (4a258f41-73b8-43a8-9d6f-ba13d201915a)
 Call ID: 4a258f41-73b8-43a8-9d6f-ba13d201915a
  Args: