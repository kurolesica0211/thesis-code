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
  AssignClass (03310739-f9e2-4ac7-bbcf-85cacfd0929d)
 Call ID: 03310739-f9e2-4ac7-bbcf-85cacfd0929d
  Args:
    type: :Woman
    source: Elisabeth_of_Mecklenburg-Schwerin
  AssignClass (49b3da49-2f2d-4705-a94e-bf2034e6e55e)
 Call ID: 49b3da49-2f2d-4705-a94e-bf2034e6e55e
  Args:
    type: :Person
    source: Elisabeth_of_Mecklenburg-Schwerin
  AddLiteral (8529e8c3-7214-40d4-b383-72b5e8c60d22)
 Call ID: 8529e8c3-7214-40d4-b383-72b5e8c60d22
  Args:
    literal_value: 1869
    source: Elisabeth_of_Mecklenburg-Schwerin
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (439b894d-f4b7-4d00-b600-5ad9c34f9c99)
 Call ID: 439b894d-f4b7-4d00-b600-5ad9c34f9c99
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: Elisabeth_of_Mecklenburg-Schwerin
    literal_value: 1955
  AssignClass (03411173-5ef8-4ca5-a356-417dc5a3d308)
 Call ID: 03411173-5ef8-4ca5-a356-417dc5a3d308
  Args:
    type: :Man
    source: Frederick_Francis_II
  AssignClass (226fa769-b712-43fd-9ab3-c4c9431789a8)
 Call ID: 226fa769-b712-43fd-9ab3-c4c9431789a8
  Args:
    type: :Ancestor
    source: Frederick_Francis_II
  AssignClass (f5786ff0-f650-4d14-b76b-c8738d5977a0)
 Call ID: f5786ff0-f650-4d14-b76b-c8738d5977a0
  Args:
    type: :Woman
    source: Marie_of_Schwarzburg-Rudolstadt
  AssignClass (c430c852-43da-43c7-9e7f-7b5a8e4d82cf)
 Call ID: c430c852-43da-43c7-9e7f-7b5a8e4d82cf
  Args:
    type: :Ancestor
    source: Marie_of_Schwarzburg-Rudolstadt
  AddTriple (ac62d7c2-b742-4c11-acbc-47b78433003c)
 Call ID: ac62d7c2-b742-4c11-acbc-47b78433003c
  Args:
    target: Frederick_Francis_II
    source: Elisabeth_of_Mecklenburg-Schwerin
    relation: :hasFather
  AddTriple (75690e05-1f30-4022-a0cf-a6a8ba957c04)
 Call ID: 75690e05-1f30-4022-a0cf-a6a8ba957c04
  Args:
    relation: :hasMother
    source: Elisabeth_of_Mecklenburg-Schwerin
    target: Marie_of_Schwarzburg-Rudolstadt
  AssignClass (894b5865-1436-4e9a-a46f-f6a330e0f4c5)
 Call ID: 894b5865-1436-4e9a-a46f-f6a330e0f4c5
  Args:
    type: :Man
    source: Frederick_Augustus_II
  AssignClass (53452474-d93d-48d9-b860-8050d6e543b9)
 Call ID: 53452474-d93d-48d9-b860-8050d6e543b9
  Args:
    type: :Person
    source: Frederick_Augustus_II
  AddLiteral (806335e7-cf91-4c8c-86fc-e6b26895c0c5)
 Call ID: 806335e7-cf91-4c8c-86fc-e6b26895c0c5
  Args:
    source: Elisabeth_of_Mecklenburg-Schwerin
    literal_value: 1896
    relation: :hasMarriageYear
    literal_type: xsd:integer
  AddTriple (8fe72be8-1111-4bb3-bbb1-50e83d35ec15)
 Call ID: 8fe72be8-1111-4bb3-bbb1-50e83d35ec15
  Args:
    relation: :hasRelation
    target: Frederick_Augustus_II
    source: Elisabeth_of_Mecklenburg-Schwerin
  AssignClass (a5209fac-8afc-4ec7-8c33-cd618fc5433b)
 Call ID: a5209fac-8afc-4ec7-8c33-cd618fc5433b
  Args:
    type: :Man
    source: Hendrik_of_the_Netherlands
  AssignClass (586eefe9-8cbe-4bd1-bbd2-3cfa0e45c53b)
 Call ID: 586eefe9-8cbe-4bd1-bbd2-3cfa0e45c53b
  Args:
    type: :Person
    source: Hendrik_of_the_Netherlands
  AddTriple (2962c397-6ea0-4b36-b891-a4d809be681a)
 Call ID: 2962c397-6ea0-4b36-b891-a4d809be681a
  Args:
    relation: :isSiblingOf
    target: Hendrik_of_the_Netherlands
    source: Elisabeth_of_Mecklenburg-Schwerin
  AssignClass (ccecee2c-5e6b-4be7-9d47-f10448831dfd)
 Call ID: ccecee2c-5e6b-4be7-9d47-f10448831dfd
  Args:
    type: :Woman
    source: Wilhelmina_of_the_Netherlands
  AssignClass (c727634f-2b32-400d-8a18-2417f3788944)
 Call ID: c727634f-2b32-400d-8a18-2417f3788944
  Args:
    type: :Person
    source: Wilhelmina_of_the_Netherlands
  AddTriple (fe71dc52-03bc-4e9e-891d-583b5626ea02)
 Call ID: fe71dc52-03bc-4e9e-891d-583b5626ea02
  Args:
    target: Wilhelmina_of_the_Netherlands
    source: Hendrik_of_the_Netherlands
    relation: :hasRelation
  AssignClass (9ecc030a-7362-41d1-9346-8761ee5b95f6)
 Call ID: 9ecc030a-7362-41d1-9346-8761ee5b95f6
  Args:
    type: :Woman
    source: Juliana_of_the_Netherlands
  AssignClass (ace20774-e059-4820-a65c-47a568eeda6e)
 Call ID: ace20774-e059-4820-a65c-47a568eeda6e
  Args:
    type: :Person
    source: Juliana_of_the_Netherlands
  AddTriple (b714fa02-dd3e-4692-870d-6a8de3ed6e98)
 Call ID: b714fa02-dd3e-4692-870d-6a8de3ed6e98
  Args:
    relation: :isAuntOf
    source: Elisabeth_of_Mecklenburg-Schwerin
    target: Juliana_of_the_Netherlands
  AssignClass (d5af0b7c-09a7-4175-8931-b3089c4a55bb)
 Call ID: d5af0b7c-09a7-4175-8931-b3089c4a55bb
  Args:
    type: :Man
    source: Frederick_Francis_III
  AssignClass (589c787a-2b86-4781-9a21-4069b3333e8c)
 Call ID: 589c787a-2b86-4781-9a21-4069b3333e8c
  Args:
    type: :Person
    source: Frederick_Francis_III
  AddTriple (9df535b6-2014-4814-8d28-733db913b9ed)
 Call ID: 9df535b6-2014-4814-8d28-733db913b9ed
  Args:
    source: Elisabeth_of_Mecklenburg-Schwerin
    target: Frederick_Francis_III
    relation: :isSiblingOf
  AssignClass (f786e9c7-6e43-4ca4-8d74-ff49920e1b18)
 Call ID: f786e9c7-6e43-4ca4-8d74-ff49920e1b18
  Args:
    type: :Woman
    source: Alexandrine_of_Denmark
  AssignClass (9e7cf44e-4036-4c1c-acc7-698c83bbe4c5)
 Call ID: 9e7cf44e-4036-4c1c-acc7-698c83bbe4c5
  Args:
    type: :Person
    source: Alexandrine_of_Denmark
  AssignClass (301cf4fe-be77-4a0a-be7c-d85b5bbabdf7)
 Call ID: 301cf4fe-be77-4a0a-be7c-d85b5bbabdf7
  Args:
    type: :Woman
    source: Cecilie_of_Mecklenburg-Schwerin
  AssignClass (eb37b091-dc13-4d7a-81bf-d3063df870d4)
 Call ID: eb37b091-dc13-4d7a-81bf-d3063df870d4
  Args:
    type: :Person
    source: Cecilie_of_Mecklenburg-Schwerin
  AddTriple (f248be2e-2022-42be-b946-764aaceb42a8)
 Call ID: f248be2e-2022-42be-b946-764aaceb42a8
  Args:
    relation: :isAuntOf
    source: Elisabeth_of_Mecklenburg-Schwerin
    target: Alexandrine_of_Denmark
  AddTriple (ebc7ad92-bbf2-4735-82d3-57dca03103c4)
 Call ID: ebc7ad92-bbf2-4735-82d3-57dca03103c4
  Args:
    relation: :isAuntOf
    source: Elisabeth_of_Mecklenburg-Schwerin
    target: Cecilie_of_Mecklenburg-Schwerin
  AssignClass (accdae83-53b6-476e-b33a-5d5908e34e52)
 Call ID: accdae83-53b6-476e-b33a-5d5908e34e52
  Args:
    type: :Woman
    source: Marie_of_Russia
  AssignClass (334560b5-4dce-47fb-b92c-5889ef159e60)
 Call ID: 334560b5-4dce-47fb-b92c-5889ef159e60
  Args:
    type: :Person
    source: Marie_of_Russia
  AddTriple (f1cb6860-ba81-4adf-8573-e20fb787862e)
 Call ID: f1cb6860-ba81-4adf-8573-e20fb787862e
  Args:
    relation: :isSiblingOf
    source: Elisabeth_of_Mecklenburg-Schwerin
    target: Marie_of_Russia
  AssignClass (5d195b83-c543-4e79-b31d-65d7d69d9e4b)
 Call ID: 5d195b83-c543-4e79-b31d-65d7d69d9e4b
  Args:
    type: :Man
    source: Cyril_Vladimirovich_of_Russia
  AssignClass (eb608c92-0a4e-453e-ade8-c02ed728f738)
 Call ID: eb608c92-0a4e-453e-ade8-c02ed728f738
  Args:
    type: :Person
    source: Cyril_Vladimirovich_of_Russia
  AddTriple (044268d2-aa51-4d4f-9940-4f6be59d790a)
 Call ID: 044268d2-aa51-4d4f-9940-4f6be59d790a
  Args:
    relation: :isMotherOf
    source: Marie_of_Russia
    target: Cyril_Vladimirovich_of_Russia
  AssignClass (c87ff538-f8ad-460e-a7ac-8353a0a56ff3)
 Call ID: c87ff538-f8ad-460e-a7ac-8353a0a56ff3
  Args:
    type: :Man
    source: Paul_Frederick_of_Mecklenburg
  AssignClass (04b8d9dd-44f9-414d-8f1a-1ac815d5791a)
 Call ID: 04b8d9dd-44f9-414d-8f1a-1ac815d5791a
  Args:
    type: :Ancestor
    source: Paul_Frederick_of_Mecklenburg
  AssignClass (adfb4d81-269e-4dfa-b714-a05f4355011d)
 Call ID: adfb4d81-269e-4dfa-b714-a05f4355011d
  Args:
    type: :Woman
    source: Alexandrine_of_Prussia
  AssignClass (67057132-d866-4a68-9562-45905f0c5510)
 Call ID: 67057132-d866-4a68-9562-45905f0c5510
  Args:
    type: :Ancestor
    source: Alexandrine_of_Prussia
  AddTriple (172bc6c9-73b5-43c5-a38e-895ccd8293ae)
 Call ID: 172bc6c9-73b5-43c5-a38e-895ccd8293ae
  Args:
    relation: :hasFather
    source: Frederick_Francis_II
    target: Paul_Frederick_of_Mecklenburg
  AddTriple (a6a40f7d-b1da-43c8-83a9-78a813e632a1)
 Call ID: a6a40f7d-b1da-43c8-83a9-78a813e632a1
  Args:
    relation: :hasMother
    target: Alexandrine_of_Prussia
    source: Frederick_Francis_II
  AssignClass (7701085f-43cd-441f-b14b-45686cc8853a)
 Call ID: 7701085f-43cd-441f-b14b-45686cc8853a
  Args:
    type: :Man
    source: Adolph_of_Schwarzburg-Rudolstadt
  AssignClass (c357eff1-cdf2-4d56-92fc-3ceaa8c4e664)
 Call ID: c357eff1-cdf2-4d56-92fc-3ceaa8c4e664
  Args:
    type: :Ancestor
    source: Adolph_of_Schwarzburg-Rudolstadt
  AssignClass (94ba9e3f-92df-4e0a-8de9-fe0db6c05f14)
 Call ID: 94ba9e3f-92df-4e0a-8de9-fe0db6c05f14
  Args:
    type: :Woman
    source: Mathilde_of_Schönburg-Waldenburg
  AssignClass (20f202aa-77c7-4f6e-a3ef-a32df01bee1e)
 Call ID: 20f202aa-77c7-4f6e-a3ef-a32df01bee1e
  Args:
    type: :Ancestor
    source: Mathilde_of_Schönburg-Waldenburg
  AddTriple (81a09ae8-616b-441b-bff2-c5605993547c)
 Call ID: 81a09ae8-616b-441b-bff2-c5605993547c
  Args:
    relation: :hasFather
    target: Adolph_of_Schwarzburg-Rudolstadt
    source: Marie_of_Schwarzburg-Rudolstadt
  AddTriple (09e1158e-784c-4e61-a846-9ebb84b2c142)
 Call ID: 09e1158e-784c-4e61-a846-9ebb84b2c142
  Args:
    source: Marie_of_Schwarzburg-Rudolstadt
    target: Mathilde_of_Schönburg-Waldenburg
    relation: :hasMother
  AssignClass (6d34b5a5-11bc-4dde-aacf-d58b5a2e4a22)
 Call ID: 6d34b5a5-11bc-4dde-aacf-d58b5a2e4a22
  Args:
    type: :Woman
    source: Elisabeth_Anna_of_Oldenburg
  AssignClass (acc26959-485b-4888-9544-42e3768b0e8f)
 Call ID: acc26959-485b-4888-9544-42e3768b0e8f
  Args:
    type: :Person
    source: Elisabeth_Anna_of_Oldenburg
  AssignClass (6b7f585c-42ee-40f6-b5e7-6cae87ced4c5)
 Call ID: 6b7f585c-42ee-40f6-b5e7-6cae87ced4c5
  Args:
    type: :Woman
    source: Sophia_Charlotte_of_Oldenburg
  AssignClass (8c234bee-9c00-4633-8b98-9cc9d21e0ac5)
 Call ID: 8c234bee-9c00-4633-8b98-9cc9d21e0ac5
  Args:
    type: :Person
    source: Sophia_Charlotte_of_Oldenburg
  AddTriple (5d9efb7e-5b53-4029-bd3b-abff99842385)
 Call ID: 5d9efb7e-5b53-4029-bd3b-abff99842385
  Args:
    target: Sophia_Charlotte_of_Oldenburg
    source: Elisabeth_Anna_of_Oldenburg
    relation: :isMotherOf
  AddTriple (69b7f211-50bb-4e6c-b297-279d68371d3b)
 Call ID: 69b7f211-50bb-4e6c-b297-279d68371d3b
  Args:
    target: Sophia_Charlotte_of_Oldenburg
    source: Frederick_Augustus_II
    relation: :isFatherOf
  AddLiteral (09d993a1-9161-4c49-af65-089ba8fc5d25)
 Call ID: 09d993a1-9161-4c49-af65-089ba8fc5d25
  Args:
    literal_value: 1931
    source: Frederick_Augustus_II
    literal_type: xsd:integer
    relation: :hasDeathYear
  Finish (5e9ef861-fe1a-48c6-bcce-4864687e49ca)
 Call ID: 5e9ef861-fe1a-48c6-bcce-4864687e49ca
  Args: