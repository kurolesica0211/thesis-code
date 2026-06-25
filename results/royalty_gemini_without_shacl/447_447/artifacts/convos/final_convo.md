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
Lady Charlotte Anne Santo Domingo (née Wellesley; 8 October 1990) is an English aristocrat and socialite and photography producer.
Early life and family

Lady Charlotte Wellesley was born at St Mary's Hospital, London on 8 October 1990 to Princess Antonia of Prussia and Charles Wellesley, Marquess of Douro.
After the death of her paternal grandfather, Valerian Wellesley, 8th Duke of Wellington, in 2014, her father succeeded him as the 9th Duke of Wellington, the 9th Prince of Waterloo, the 9th Duke of Victoria, and the 10th Duke of Ciudad Rodrigo.
Her mother, Princess Antonia, is the youngest child of Prince Frederick of Prussia and Lady Brigid Guinness.
Through her mother, Lady Charlotte is a great-great-granddaughter of Wilhelm II, German Emperor and a great-great-great-great-granddaughter of Queen Victoria.
Lady Charlotte grew up at Stratfield Saye House, her family's estate in Hampshire.
She is the younger sister of Arthur Wellesley, Earl of Mornington and Lady Mary Wellesley.
Education and career

Lady Charlotte attended Wycombe Abbey, an all-girls boarding school in Buckinghamshire.
Personal life

Lady Charlotte married Colombian-American financier Alejandro Santo Domingo in Íllora, Spain, on 28 May 2016.



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
  AssignClass (e7ec3030-d2bf-42d6-af1a-6b3dd2afba92)
 Call ID: e7ec3030-d2bf-42d6-af1a-6b3dd2afba92
  Args:
    source: :Lady_Charlotte_Wellesley
    type: :Woman
  AssignClass (ea15d8b9-fd34-44d2-81b9-21e93630b4e5)
 Call ID: ea15d8b9-fd34-44d2-81b9-21e93630b4e5
  Args:
    source: :Lady_Charlotte_Wellesley
    type: :Person
  AddLiteral (f62d0986-bc7e-4759-b2c1-1dd6dd505fe8)
 Call ID: f62d0986-bc7e-4759-b2c1-1dd6dd505fe8
  Args:
    source: :Lady_Charlotte_Wellesley
    literal_value: 1990
    literal_type: xsd:integer
    relation: :hasBirthYear
  AssignClass (cdfce44e-9d53-4b61-aaef-1206887f80ec)
 Call ID: cdfce44e-9d53-4b61-aaef-1206887f80ec
  Args:
    source: :Princess_Antonia_of_Prussia
    type: :Woman
  AssignClass (78731fd0-7e61-4023-a302-b257d6a9b6ff)
 Call ID: 78731fd0-7e61-4023-a302-b257d6a9b6ff
  Args:
    source: :Princess_Antonia_of_Prussia
    type: :Person
  AssignClass (11a0f2f6-f40c-45fc-b09f-e48e41fc22c1)
 Call ID: 11a0f2f6-f40c-45fc-b09f-e48e41fc22c1
  Args:
    type: :Man
    source: :Charles_Wellesley
  AssignClass (9646f441-ae27-458b-9f4f-6043a7001bed)
 Call ID: 9646f441-ae27-458b-9f4f-6043a7001bed
  Args:
    source: :Charles_Wellesley
    type: :Person
  AddTriple (605c8ca1-d4c1-4f50-a1d9-d3da22712a29)
 Call ID: 605c8ca1-d4c1-4f50-a1d9-d3da22712a29
  Args:
    target: :Princess_Antonia_of_Prussia
    source: :Lady_Charlotte_Wellesley
    relation: :hasMother
  AddTriple (8ceed2fe-c917-490c-bd68-c6ce00c159c6)
 Call ID: 8ceed2fe-c917-490c-bd68-c6ce00c159c6
  Args:
    target: :Charles_Wellesley
    source: :Lady_Charlotte_Wellesley
    relation: :hasFather
  AssignClass (47bca16b-489e-499a-ad65-db8e55137ece)
 Call ID: 47bca16b-489e-499a-ad65-db8e55137ece
  Args:
    type: :Man
    source: :Valerian_Wellesley
  AssignClass (9360c43c-5d51-48f2-9414-e4066a07afb8)
 Call ID: 9360c43c-5d51-48f2-9414-e4066a07afb8
  Args:
    source: :Valerian_Wellesley
    type: :Person
  AddTriple (f2476efa-607c-43dc-b7bd-5e5884efc58e)
 Call ID: f2476efa-607c-43dc-b7bd-5e5884efc58e
  Args:
    relation: :hasFather
    target: :Valerian_Wellesley
    source: :Charles_Wellesley
  AddLiteral (a17b5a69-3f2d-4d11-82b7-2cd04c839029)
 Call ID: a17b5a69-3f2d-4d11-82b7-2cd04c839029
  Args:
    source: :Valerian_Wellesley
    literal_value: 2014
    literal_type: xsd:integer
    relation: :hasDeathYear
  AssignClass (50982035-3948-47d8-b7a4-6f6171c9cf1f)
 Call ID: 50982035-3948-47d8-b7a4-6f6171c9cf1f
  Args:
    type: :Man
    source: :Prince_Frederick_of_Prussia
  AssignClass (92f5705e-9cbf-4720-8a4f-c16ddf54996d)
 Call ID: 92f5705e-9cbf-4720-8a4f-c16ddf54996d
  Args:
    type: :Person
    source: :Prince_Frederick_of_Prussia
  AssignClass (c05596ca-40e7-4a3a-aa5f-a42db3db5dbb)
 Call ID: c05596ca-40e7-4a3a-aa5f-a42db3db5dbb
  Args:
    source: :Lady_Brigid_Guinness
    type: :Woman
  AssignClass (eb0459c1-021a-4d46-8048-71f1a8b90e00)
 Call ID: eb0459c1-021a-4d46-8048-71f1a8b90e00
  Args:
    source: :Lady_Brigid_Guinness
    type: :Person
  AddTriple (7a3509c5-73c7-4bcb-9125-82b27a048ee6)
 Call ID: 7a3509c5-73c7-4bcb-9125-82b27a048ee6
  Args:
    target: :Prince_Frederick_of_Prussia
    source: :Princess_Antonia_of_Prussia
    relation: :hasFather
  AddTriple (ebce83e0-fb00-43c4-adff-8415aa751bdd)
 Call ID: ebce83e0-fb00-43c4-adff-8415aa751bdd
  Args:
    relation: :hasMother
    target: :Lady_Brigid_Guinness
    source: :Princess_Antonia_of_Prussia
  AssignClass (911f0ab7-8d25-4484-b859-15553b9ac248)
 Call ID: 911f0ab7-8d25-4484-b859-15553b9ac248
  Args:
    source: :Arthur_Wellesley
    type: :Man
  AssignClass (0a91985b-0f56-44d8-bfbe-b0395cc42694)
 Call ID: 0a91985b-0f56-44d8-bfbe-b0395cc42694
  Args:
    type: :Person
    source: :Arthur_Wellesley
  AssignClass (8b77999c-55ac-43b8-8d0f-bc9f4aa9649d)
 Call ID: 8b77999c-55ac-43b8-8d0f-bc9f4aa9649d
  Args:
    source: :Lady_Mary_Wellesley
    type: :Woman
  AssignClass (6101908f-4c80-4c8b-b7bf-3b421c1c8fdd)
 Call ID: 6101908f-4c80-4c8b-b7bf-3b421c1c8fdd
  Args:
    source: :Lady_Mary_Wellesley
    type: :Person
  AddTriple (f41ce478-e285-48b0-8d52-4b42bcbbf7a0)
 Call ID: f41ce478-e285-48b0-8d52-4b42bcbbf7a0
  Args:
    source: :Lady_Charlotte_Wellesley
    target: :Arthur_Wellesley
    relation: :hasBrother
  AddTriple (62ce6298-fa81-4c81-b787-08f2039434ca)
 Call ID: 62ce6298-fa81-4c81-b787-08f2039434ca
  Args:
    target: :Lady_Mary_Wellesley
    source: :Lady_Charlotte_Wellesley
    relation: :hasSister
  AssignClass (27c0282c-6a95-4538-9294-edd645c784e7)
 Call ID: 27c0282c-6a95-4538-9294-edd645c784e7
  Args:
    source: :Alejandro_Santo_Domingo
    type: :Man
  AssignClass (ef9467b2-ac4b-4137-8bac-3883a267dfad)
 Call ID: ef9467b2-ac4b-4137-8bac-3883a267dfad
  Args:
    source: :Alejandro_Santo_Domingo
    type: :Person
  AddLiteral (45bd0637-dc08-4252-9cda-af9743c86d5e)
 Call ID: 45bd0637-dc08-4252-9cda-af9743c86d5e
  Args:
    literal_value: 2016
    source: :Lady_Charlotte_Wellesley
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AddTriple (a4543ff3-4a05-44d6-96d7-73513da56b46)
 Call ID: a4543ff3-4a05-44d6-96d7-73513da56b46
  Args:
    source: :Lady_Charlotte_Wellesley
    target: :Alejandro_Santo_Domingo
    relation: :hasRelation
  Finish (2ec2e259-1a48-4334-8457-c04a2b425f18)
 Call ID: 2ec2e259-1a48-4334-8457-c04a2b425f18
  Args: