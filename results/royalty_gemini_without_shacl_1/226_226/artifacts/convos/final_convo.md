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
Gerald David Lascelles (/ˈlæsəls/ LASS-əlss; 21 August 1924 – 27 February 1998) was the younger son of Henry Lascelles, 6th Earl of Harewood, and Mary, Princess Royal, the only daughter of King George V and Queen Mary.
He was styled The Honourable Gerald Lascelles.
Life

Gerald David Lascelles was born at Goldsborough Hall, near Knaresborough, West Riding of Yorkshire, and was baptised in October 1924 with the Prince of Wales and the Duchess of York (later King Edward VIII and Queen Elizabeth) as his godparents represented there by proxies.
The baptism was held in private at St. Mary's Church in the village of Goldsborough.
In 1955, the family moved to Fort Belvedere, Surrey, the former country home of Gerald Lascelles's uncle, Edward VIII (the Duke of Windsor).
On 17 November 1978, Lascelles married his second wife, actress Elizabeth Colvin (née Elizabeth Evelyn Collingwood, 23 April 1924 – 14 January 2006), in Vienna, Austria.
They had a son: 


Interests and positions

Lascelles was the president of the British Racing Drivers' Club from 1964 to 1991, after the 5th Earl Howe died.
Lord Howe had asked Lascelles to replace him, who was briefly a driver before this.
In his role as BRDC president, Lascelles was invited by the Australian Racing Drivers Club, promoters of the Bathurst 1000 Touring car race, to be the Grand Marshal for the 1985 race.
Death

Lascelles died in Bergerac, France, on 27 February 1998 at the age of 73.



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
  AssignClass (59b3e8cd-36ff-483d-856d-4c97aa21d339)
 Call ID: 59b3e8cd-36ff-483d-856d-4c97aa21d339
  Args:
    type: :Man
    source: Gerald_David_Lascelles
  AssignClass (78481e5a-6797-4707-bcb4-7d68bd103b02)
 Call ID: 78481e5a-6797-4707-bcb4-7d68bd103b02
  Args:
    source: Gerald_David_Lascelles
    type: :Person
  AddLiteral (54b656d6-3832-47b6-922e-c43254ed9a82)
 Call ID: 54b656d6-3832-47b6-922e-c43254ed9a82
  Args:
    source: Gerald_David_Lascelles
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1924
  AddLiteral (31ef4aeb-1c0d-486c-9618-6425c8c86d07)
 Call ID: 31ef4aeb-1c0d-486c-9618-6425c8c86d07
  Args:
    source: Gerald_David_Lascelles
    relation: :hasDeathYear
    literal_value: 1998
    literal_type: xsd:integer
  AssignClass (fb31a9c6-ef53-4c92-846c-96b5b447c0ae)
 Call ID: fb31a9c6-ef53-4c92-846c-96b5b447c0ae
  Args:
    source: Henry_Lascelles_6th_Earl_of_Harewood
    type: :Man
  AssignClass (407cde48-3307-4875-84a7-eda6eea6c6e6)
 Call ID: 407cde48-3307-4875-84a7-eda6eea6c6e6
  Args:
    type: :Person
    source: Henry_Lascelles_6th_Earl_of_Harewood
  AssignClass (126bf1f5-5b99-4dad-9256-fcc1cb44d654)
 Call ID: 126bf1f5-5b99-4dad-9256-fcc1cb44d654
  Args:
    type: :Woman
    source: Mary_Princess_Royal
  AssignClass (6f309fb8-e8cb-4966-8fec-a388229d9ae6)
 Call ID: 6f309fb8-e8cb-4966-8fec-a388229d9ae6
  Args:
    source: Mary_Princess_Royal
    type: :Person
  AddTriple (c64aa79d-ce09-4b52-89d7-de71f5071f9a)
 Call ID: c64aa79d-ce09-4b52-89d7-de71f5071f9a
  Args:
    source: Gerald_David_Lascelles
    target: Henry_Lascelles_6th_Earl_of_Harewood
    relation: :hasFather
  AddTriple (309ae8c1-6140-48e6-8e23-b12c08a4b072)
 Call ID: 309ae8c1-6140-48e6-8e23-b12c08a4b072
  Args:
    relation: :hasMother
    target: Mary_Princess_Royal
    source: Gerald_David_Lascelles
  AssignClass (128a3bbd-c270-4d3e-9919-52b2c3a8dd18)
 Call ID: 128a3bbd-c270-4d3e-9919-52b2c3a8dd18
  Args:
    type: :Man
    source: King_George_V
  AssignClass (42884194-ac2a-4ba3-ade3-f6946eea0454)
 Call ID: 42884194-ac2a-4ba3-ade3-f6946eea0454
  Args:
    type: :Person
    source: King_George_V
  AssignClass (9d05b724-ae4a-4c35-92ac-eefbfb3fdd10)
 Call ID: 9d05b724-ae4a-4c35-92ac-eefbfb3fdd10
  Args:
    type: :Woman
    source: Queen_Mary
  AssignClass (db571292-6007-4870-a77d-4a915b7aab73)
 Call ID: db571292-6007-4870-a77d-4a915b7aab73
  Args:
    type: :Person
    source: Queen_Mary
  AddTriple (b9ea831a-b906-4a1c-9aa1-d76d4fdf7b64)
 Call ID: b9ea831a-b906-4a1c-9aa1-d76d4fdf7b64
  Args:
    target: King_George_V
    source: Mary_Princess_Royal
    relation: :hasFather
  AddTriple (fef92e87-1d55-481e-ba0d-bbd4b8816bf6)
 Call ID: fef92e87-1d55-481e-ba0d-bbd4b8816bf6
  Args:
    relation: :hasMother
    source: Mary_Princess_Royal
    target: Queen_Mary
  AssignClass (b0ba0e08-f8e6-4e0d-b69c-c9bff4e67eae)
 Call ID: b0ba0e08-f8e6-4e0d-b69c-c9bff4e67eae
  Args:
    type: :Man
    source: Edward_VIII
  AssignClass (a50e8af9-4525-4d77-aaf3-4a5b49a5fbf4)
 Call ID: a50e8af9-4525-4d77-aaf3-4a5b49a5fbf4
  Args:
    type: :Person
    source: Edward_VIII
  AddTriple (9a66b97b-d0f0-4526-8c47-e6621288245b)
 Call ID: 9a66b97b-d0f0-4526-8c47-e6621288245b
  Args:
    target: Edward_VIII
    source: Gerald_David_Lascelles
    relation: :hasRelation
  AssignClass (9bebf61e-7043-478a-8b66-038eb1ceda10)
 Call ID: 9bebf61e-7043-478a-8b66-038eb1ceda10
  Args:
    type: :Woman
    source: Elizabeth_Colvin
  AssignClass (602fd94d-87ef-4a51-b386-5b613c08d260)
 Call ID: 602fd94d-87ef-4a51-b386-5b613c08d260
  Args:
    source: Elizabeth_Colvin
    type: :Person
  AddLiteral (2fd290a5-1a91-4975-a676-3216c4e2a8b7)
 Call ID: 2fd290a5-1a91-4975-a676-3216c4e2a8b7
  Args:
    literal_type: xsd:integer
    literal_value: 1978
    relation: :hasMarriageYear
    source: Gerald_David_Lascelles
  AddTriple (30dfc9e1-e4e1-46cf-9667-cbb6f2f1d869)
 Call ID: 30dfc9e1-e4e1-46cf-9667-cbb6f2f1d869
  Args:
    target: Elizabeth_Colvin
    source: Gerald_David_Lascelles
    relation: :hasRelation
  AddLiteral (a8d611f5-8c5e-4d82-85f4-2d94d7aba3da)
 Call ID: a8d611f5-8c5e-4d82-85f4-2d94d7aba3da
  Args:
    literal_type: xsd:integer
    literal_value: 1924
    relation: :hasBirthYear
    source: Elizabeth_Colvin
  AddLiteral (70cc2814-69da-472c-9061-876b5c7c29a0)
 Call ID: 70cc2814-69da-472c-9061-876b5c7c29a0
  Args:
    source: Elizabeth_Colvin
    literal_value: 2006
    relation: :hasDeathYear
    literal_type: xsd:integer
  Finish (7fefc4d7-ec49-428b-a6a8-32187d6dcb4d)
 Call ID: 7fefc4d7-ec49-428b-a6a8-32187d6dcb4d
  Args: