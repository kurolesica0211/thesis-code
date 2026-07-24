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
Duchess Elisabeth of Mecklenburg-Schwerin (10 August 1869 – 3 September 1955) was a daughter of Frederick Francis II, Grand Duke of Mecklenburg by his third wife Princess Marie of Schwarzburg-Rudolstadt.
By her marriage to Frederick Augustus II, she became the consort of the last reigning Grand Duke of Oldenburg.
Family

Elisabeth was related to many of Europe's royal families.
She was the eldest child of Frederick Francis II, Grand Duke of Mecklenburg by his third wife, Princess Marie of Schwarzburg-Rudolstadt.
She was an older sister of Hendrik, Prince consort of the Netherlands, husband of Queen Wilhelmina of the Netherlands, making her an aunt of Queen Juliana of the Netherlands.
She was also a younger half-sister of Frederick Francis III, Grand Duke of Mecklenburg-Schwerin.
Through Frederick Francis, she was an aunt of Alexandrine, Queen of Denmark and Cecilie, German Crown Princess.
Elisabeth was also a half sister of Marie, Grand Duchess of Russia, who was the mother of Grand Duke Cyril Vladimirovich of Russia, the pretender to the Russian throne.
Her paternal grandparents were Paul Frederick, Grand Duke of Mecklenburg and Princess Alexandrine of Prussia.
Her maternal grandparents were Prince Adolph of Schwarzburg-Rudolstadt and Princess Mathilde of Schönburg-Waldenburg.
Marriage

On 24 October 1896, Elisabeth married Frederick Augustus, Hereditary Grand Duke of Oldenburg.
His first wife Elisabeth Anna had died the previous year, leaving only one surviving daughter: Duchess Sophia Charlotte of Oldenburg.
Frederick Augustus was thus in need of a male heir.
He succeeded as Grand Duke of Oldenburg in 1900, making Elisabeth Grand Duchess consort of Oldenburg.
They had five children:


Frederick was forced to abdicate his throne at the end of World War I, when the former Grand Duchy of the German Empire joined the post-war German Republic.
A year after his abdication, he asked the Oldenburg Diet for a yearly allowance of 150,000 marks, stating that his financial condition was "extremely precarious".
In 1931, Frederick died in Rastede.
Elisabeth died on 3 September 1955, having been widowed for 24 years.



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
  AssignClass (f6432dba-0fd8-4783-9067-19dac73b52b3)
 Call ID: f6432dba-0fd8-4783-9067-19dac73b52b3
  Args:
    type: :Woman
    source: Elisabeth_of_Mecklenburg-Schwerin
  AssignClass (f6b2e8c1-2d58-4013-a40e-62e2ec72d58e)
 Call ID: f6b2e8c1-2d58-4013-a40e-62e2ec72d58e
  Args:
    type: :Man
    source: Frederick_Francis_II
  AssignClass (f176c43c-fef0-44e1-b3a6-2a67d2ac0305)
 Call ID: f176c43c-fef0-44e1-b3a6-2a67d2ac0305
  Args:
    type: :Woman
    source: Marie_of_Schwarzburg-Rudolstadt
  AddLiteral (abeae40a-4ad2-41d8-a210-46dfc1f9b1ba)
 Call ID: abeae40a-4ad2-41d8-a210-46dfc1f9b1ba
  Args:
    source: Elisabeth_of_Mecklenburg-Schwerin
    literal_value: 1869
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (2c52edd4-7cac-45d3-910c-c4098f039fac)
 Call ID: 2c52edd4-7cac-45d3-910c-c4098f039fac
  Args:
    literal_value: 1955
    source: Elisabeth_of_Mecklenburg-Schwerin
    relation: :hasDeathYear
    literal_type: xsd:integer
  AddTriple (75317b63-0c7d-44eb-8ee4-f46300ee58b9)
 Call ID: 75317b63-0c7d-44eb-8ee4-f46300ee58b9
  Args:
    source: Elisabeth_of_Mecklenburg-Schwerin
    relation: :hasFather
    target: Frederick_Francis_II
  AddTriple (0a10608f-ab44-478e-91a1-4df7709f4d98)
 Call ID: 0a10608f-ab44-478e-91a1-4df7709f4d98
  Args:
    source: Elisabeth_of_Mecklenburg-Schwerin
    relation: :hasMother
    target: Marie_of_Schwarzburg-Rudolstadt
  AssignClass (5a87f46e-4c4a-4945-b017-28ae372144b1)
 Call ID: 5a87f46e-4c4a-4945-b017-28ae372144b1
  Args:
    type: :Man
    source: Frederick_Augustus_II
  AddTriple (6fbd2ab6-64f5-4e2e-bf09-0b2c02a2dab8)
 Call ID: 6fbd2ab6-64f5-4e2e-bf09-0b2c02a2dab8
  Args:
    relation: :hasRelation
    target: Frederick_Augustus_II
    source: Elisabeth_of_Mecklenburg-Schwerin
  AddLiteral (cbd6b879-6767-4390-b299-1b4a013ded42)
 Call ID: cbd6b879-6767-4390-b299-1b4a013ded42
  Args:
    source: Elisabeth_of_Mecklenburg-Schwerin
    literal_value: 1896
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AssignClass (06575c84-54d1-4de3-a4be-5b7522b04f88)
 Call ID: 06575c84-54d1-4de3-a4be-5b7522b04f88
  Args:
    type: :Man
    source: Hendrik_Prince_Consort_of_the_Netherlands
  AddTriple (88cf5782-ac07-4c96-9443-a78c34dadeb4)
 Call ID: 88cf5782-ac07-4c96-9443-a78c34dadeb4
  Args:
    source: Elisabeth_of_Mecklenburg-Schwerin
    relation: :isSisterOf
    target: Hendrik_Prince_Consort_of_the_Netherlands
  AssignClass (d411f939-c893-43fd-84df-7d77e6eaaae1)
 Call ID: d411f939-c893-43fd-84df-7d77e6eaaae1
  Args:
    type: :Woman
    source: Queen_Wilhelmina_of_the_Netherlands
  AddTriple (c3d6951f-6425-4ad8-9da2-432f2eda7d9c)
 Call ID: c3d6951f-6425-4ad8-9da2-432f2eda7d9c
  Args:
    source: Hendrik_Prince_Consort_of_the_Netherlands
    relation: :hasRelation
    target: Queen_Wilhelmina_of_the_Netherlands
  AssignClass (0966db02-d7c5-40f4-885d-7e0eca88b344)
 Call ID: 0966db02-d7c5-40f4-885d-7e0eca88b344
  Args:
    type: :Woman
    source: Queen_Juliana_of_the_Netherlands
  AddTriple (5602e916-00ee-4c49-854c-39956227825c)
 Call ID: 5602e916-00ee-4c49-854c-39956227825c
  Args:
    source: Elisabeth_of_Mecklenburg-Schwerin
    relation: :isAuntOf
    target: Queen_Juliana_of_the_Netherlands
  AssignClass (d3375575-fd74-408d-8b21-1e50d67e3d69)
 Call ID: d3375575-fd74-408d-8b21-1e50d67e3d69
  Args:
    type: :Man
    source: Frederick_Francis_III_of_Mecklenburg-Schwerin
  AddTriple (5799cc2e-6200-4310-9c74-6f986e177be4)
 Call ID: 5799cc2e-6200-4310-9c74-6f986e177be4
  Args:
    relation: :isSisterOf
    target: Frederick_Francis_III_of_Mecklenburg-Schwerin
    source: Elisabeth_of_Mecklenburg-Schwerin
  AssignClass (4ac10bf8-00b8-4fff-9cae-408f15e8d6b0)
 Call ID: 4ac10bf8-00b8-4fff-9cae-408f15e8d6b0
  Args:
    type: :Woman
    source: Alexandrine_Queen_of_Denmark
  AssignClass (aacb87fb-d94e-4803-b3c2-728002365040)
 Call ID: aacb87fb-d94e-4803-b3c2-728002365040
  Args:
    type: :Woman
    source: Cecilie_German_Crown_Princess
  AddTriple (3a0eaa47-d277-4b05-8e0e-b8e40886a865)
 Call ID: 3a0eaa47-d277-4b05-8e0e-b8e40886a865
  Args:
    relation: :isAuntOf
    target: Alexandrine_Queen_of_Denmark
    source: Elisabeth_of_Mecklenburg-Schwerin
  AddTriple (6c63aa96-9e1b-470d-868c-e46a9321479d)
 Call ID: 6c63aa96-9e1b-470d-868c-e46a9321479d
  Args:
    source: Elisabeth_of_Mecklenburg-Schwerin
    relation: :isAuntOf
    target: Cecilie_German_Crown_Princess
  AssignClass (c7e0a31d-e985-42ad-9b5a-535f37e93237)
 Call ID: c7e0a31d-e985-42ad-9b5a-535f37e93237
  Args:
    type: :Woman
    source: Marie_Grand_Duchess_of_Russia
  AddTriple (0667998b-329e-4d45-ad2d-0719298fac7f)
 Call ID: 0667998b-329e-4d45-ad2d-0719298fac7f
  Args:
    source: Elisabeth_of_Mecklenburg-Schwerin
    relation: :isSisterOf
    target: Marie_Grand_Duchess_of_Russia
  AssignClass (701d1338-8d18-4b79-815a-80b896818c2c)
 Call ID: 701d1338-8d18-4b79-815a-80b896818c2c
  Args:
    type: :Man
    source: Grand_Duke_Cyril_Vladimirovich_of_Russia
  AddTriple (455537e7-6ad0-4b88-9e94-f4f2af4c9dde)
 Call ID: 455537e7-6ad0-4b88-9e94-f4f2af4c9dde
  Args:
    relation: :hasMother
    target: Marie_Grand_Duchess_of_Russia
    source: Grand_Duke_Cyril_Vladimirovich_of_Russia
  AssignClass (f161ac97-e0d2-4a02-8631-82aa472a23c9)
 Call ID: f161ac97-e0d2-4a02-8631-82aa472a23c9
  Args:
    type: :Man
    source: Paul_Frederick_Grand_Duke_of_Mecklenburg
  AssignClass (ffad8386-e916-40ce-a0af-96752358008f)
 Call ID: ffad8386-e916-40ce-a0af-96752358008f
  Args:
    type: :Woman
    source: Princess_Alexandrine_of_Prussia
  AddTriple (ef5fb951-922a-4d06-a4b5-da40d49b1d60)
 Call ID: ef5fb951-922a-4d06-a4b5-da40d49b1d60
  Args:
    relation: :hasFather
    target: Paul_Frederick_Grand_Duke_of_Mecklenburg
    source: Frederick_Francis_II
  AddTriple (eea50a24-7b59-431e-9875-c487005b8009)
 Call ID: eea50a24-7b59-431e-9875-c487005b8009
  Args:
    relation: :hasMother
    target: Princess_Alexandrine_of_Prussia
    source: Frederick_Francis_II
  AssignClass (572f09fa-31be-4b83-ac6b-2c384e7b85c6)
 Call ID: 572f09fa-31be-4b83-ac6b-2c384e7b85c6
  Args:
    type: :Man
    source: Prince_Adolph_of_Schwarzburg-Rudolstadt
  AssignClass (79fd7699-83ea-4f69-8e71-110fc11ec994)
 Call ID: 79fd7699-83ea-4f69-8e71-110fc11ec994
  Args:
    type: :Woman
    source: Princess_Mathilde_of_Schönburg-Waldenburg
  AddTriple (d163fdd8-7ea0-42eb-98fc-eb7a439628cc)
 Call ID: d163fdd8-7ea0-42eb-98fc-eb7a439628cc
  Args:
    source: Marie_of_Schwarzburg-Rudolstadt
    relation: :hasFather
    target: Prince_Adolph_of_Schwarzburg-Rudolstadt
  AddTriple (6f4c45b0-effe-4441-a07a-90226763cad6)
 Call ID: 6f4c45b0-effe-4441-a07a-90226763cad6
  Args:
    relation: :hasMother
    target: Princess_Mathilde_of_Schönburg-Waldenburg
    source: Marie_of_Schwarzburg-Rudolstadt
  AssignClass (fea894ad-7b48-4718-8507-657cc79cd776)
 Call ID: fea894ad-7b48-4718-8507-657cc79cd776
  Args:
    type: :Woman
    source: Elisabeth_Anna
  AssignClass (9c05735c-4635-403b-aaca-ba5f462524cc)
 Call ID: 9c05735c-4635-403b-aaca-ba5f462524cc
  Args:
    type: :Woman
    source: Duchess_Sophia_Charlotte_of_Oldenburg
  AddTriple (7a3934b8-8d0d-4518-b3ea-72e34ae2cb08)
 Call ID: 7a3934b8-8d0d-4518-b3ea-72e34ae2cb08
  Args:
    relation: :hasMother
    target: Elisabeth_Anna
    source: Duchess_Sophia_Charlotte_of_Oldenburg
  AddTriple (902a3a23-476f-42a6-9892-93e8470cb14b)
 Call ID: 902a3a23-476f-42a6-9892-93e8470cb14b
  Args:
    source: Duchess_Sophia_Charlotte_of_Oldenburg
    relation: :hasFather
    target: Frederick_Augustus_II
  AddLiteral (3c7d3279-4f5f-4b5d-9af4-8cae97a8d92b)
 Call ID: 3c7d3279-4f5f-4b5d-9af4-8cae97a8d92b
  Args:
    literal_value: 1931
    source: Frederick_Augustus_II
    relation: :hasDeathYear
    literal_type: xsd:integer
  Finish (af709d9c-121b-4dde-a1a2-a9d0d564a991)
 Call ID: af709d9c-121b-4dde-a1a2-a9d0d564a991
  Args: