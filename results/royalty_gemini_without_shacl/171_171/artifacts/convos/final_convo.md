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
Infanta Maria Cristina of Spain, Countess Marone-Cinzano (María Cristina Teresa Alejandra María de Guadalupe María de la Concepción Ildefonsa Victoria Eugenia de Borbón y Battenberg; 12 December 1911 – 23 December 1996) was the fourth surviving child and youngest daughter of Alfonso XIII of Spain and Victoria Eugenie of Battenberg and paternal aunt of King Juan Carlos I.


Biography

Early life

Infanta Maria Cristina was born at the Palacio Real in Madrid, Spain.
By 1933 King Alfonso and his daughters, the Infantas Beatriz and Maria Cristina, had moved to Rome.
Their father warned would-be suitors of the inherent dangers of hemophilia, from which two of the king's sons, Alfonso and Gonzalo, suffered.
Maria Cristina had one step-son, from Enrico's previous marriage to Noemí Rosa de Alcorta y García-Mansilla (1907-1929):


The marriage of Maria Cristina and Enrico Eugenio produced four daughters:


Death

Infanta Maria Cristina returned to Spain and spent periods of time there, but never lived there permanently.
A funeral service for the Infanta was held in the chapel of the Royal Palace of Madrid on 24 December and a burial service was held on 26 December in the Marone-Cinzano Pantheon in Turin.



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
  AssignClass (b21d7501-fc3a-4ee7-ac45-56d2a913a5f8)
 Call ID: b21d7501-fc3a-4ee7-ac45-56d2a913a5f8
  Args:
    source: Maria_Cristina_of_Spain
    type: :Woman
  AssignClass (944de5ae-a593-4cac-b0d5-4f8ca8f9f8b7)
 Call ID: 944de5ae-a593-4cac-b0d5-4f8ca8f9f8b7
  Args:
    source: Maria_Cristina_of_Spain
    type: :Person
  AddLiteral (9fb184a1-27dd-48ef-bd20-6fa5d9759bc3)
 Call ID: 9fb184a1-27dd-48ef-bd20-6fa5d9759bc3
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1911
    source: Maria_Cristina_of_Spain
  AddLiteral (07fac28a-a5f5-475d-a43f-b75ec2d198b2)
 Call ID: 07fac28a-a5f5-475d-a43f-b75ec2d198b2
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: Maria_Cristina_of_Spain
    literal_value: 1996
  AssignClass (e4a4b953-e4ea-4244-87ec-8288c56d710c)
 Call ID: e4a4b953-e4ea-4244-87ec-8288c56d710c
  Args:
    type: :Man
    source: Alfonso_XIII_of_Spain
  AssignClass (15a52596-c825-4862-8051-c3a7b42cb81e)
 Call ID: 15a52596-c825-4862-8051-c3a7b42cb81e
  Args:
    type: :Person
    source: Alfonso_XIII_of_Spain
  AssignClass (43fa386e-b717-41ea-9f20-0f266217a551)
 Call ID: 43fa386e-b717-41ea-9f20-0f266217a551
  Args:
    source: Victoria_Eugenie_of_Battenberg
    type: :Woman
  AssignClass (ecdc2e2c-b605-4ba3-9b11-bb71aafd2632)
 Call ID: ecdc2e2c-b605-4ba3-9b11-bb71aafd2632
  Args:
    source: Victoria_Eugenie_of_Battenberg
    type: :Person
  AddTriple (4613e0d9-d46e-400a-b9a1-abe913f78d03)
 Call ID: 4613e0d9-d46e-400a-b9a1-abe913f78d03
  Args:
    target: Alfonso_XIII_of_Spain
    relation: :isDaughterOf
    source: Maria_Cristina_of_Spain
  AddTriple (f8947444-3859-4ff1-8069-39a072ea0fcf)
 Call ID: f8947444-3859-4ff1-8069-39a072ea0fcf
  Args:
    source: Maria_Cristina_of_Spain
    relation: :isDaughterOf
    target: Victoria_Eugenie_of_Battenberg
  AssignClass (f5f8d86f-7c79-4ec1-8b18-4c5c1516269e)
 Call ID: f5f8d86f-7c79-4ec1-8b18-4c5c1516269e
  Args:
    source: Juan_Carlos_I
    type: :Man
  AssignClass (9ef3fb1e-588a-4659-8d52-3e3b203803d4)
 Call ID: 9ef3fb1e-588a-4659-8d52-3e3b203803d4
  Args:
    type: :Person
    source: Juan_Carlos_I
  AddTriple (57921e00-4954-408a-b3c8-b808a615c84e)
 Call ID: 57921e00-4954-408a-b3c8-b808a615c84e
  Args:
    source: Maria_Cristina_of_Spain
    target: Juan_Carlos_I
    relation: :isAuntOf
  AssignClass (d8acfa5f-b4d1-4d8d-9c80-a4580bf6af07)
 Call ID: d8acfa5f-b4d1-4d8d-9c80-a4580bf6af07
  Args:
    type: :Woman
    source: Beatriz_of_Spain
  AssignClass (1ee45ed7-1f50-441d-afc4-b45b60585b32)
 Call ID: 1ee45ed7-1f50-441d-afc4-b45b60585b32
  Args:
    type: :Person
    source: Beatriz_of_Spain
  AddTriple (045d7b98-1ea2-4bb5-ac02-6f31d054c5d3)
 Call ID: 045d7b98-1ea2-4bb5-ac02-6f31d054c5d3
  Args:
    relation: :isSiblingOf
    target: Beatriz_of_Spain
    source: Maria_Cristina_of_Spain
  AssignClass (34527b5c-fbdb-44ce-8132-e45c7cef8c4f)
 Call ID: 34527b5c-fbdb-44ce-8132-e45c7cef8c4f
  Args:
    type: :Man
    source: Alfonso_son_of_Alfonso_XIII
  AssignClass (ffacb931-0be7-48af-9bcb-4f2813c8277e)
 Call ID: ffacb931-0be7-48af-9bcb-4f2813c8277e
  Args:
    source: Alfonso_son_of_Alfonso_XIII
    type: :Person
  AssignClass (dd298e49-d689-4138-a635-44d7cd5ee414)
 Call ID: dd298e49-d689-4138-a635-44d7cd5ee414
  Args:
    source: Gonzalo_son_of_Alfonso_XIII
    type: :Man
  AssignClass (4342d344-ce4e-4760-9822-e5589be9383e)
 Call ID: 4342d344-ce4e-4760-9822-e5589be9383e
  Args:
    source: Gonzalo_son_of_Alfonso_XIII
    type: :Person
  AddTriple (2b78c7b8-c2a0-4b6d-9bd2-ed94319e8309)
 Call ID: 2b78c7b8-c2a0-4b6d-9bd2-ed94319e8309
  Args:
    source: Maria_Cristina_of_Spain
    relation: :isSiblingOf
    target: Alfonso_son_of_Alfonso_XIII
  AddTriple (edf2d027-c828-4975-be7a-83c209e1b422)
 Call ID: edf2d027-c828-4975-be7a-83c209e1b422
  Args:
    source: Maria_Cristina_of_Spain
    relation: :isSiblingOf
    target: Gonzalo_son_of_Alfonso_XIII
  AssignClass (c541c92d-11e9-4137-bdbb-ac99ac58fc3a)
 Call ID: c541c92d-11e9-4137-bdbb-ac99ac58fc3a
  Args:
    source: Enrico_Eugenio
    type: :Man
  AssignClass (9c27627b-adac-4d31-9246-e021437403f8)
 Call ID: 9c27627b-adac-4d31-9246-e021437403f8
  Args:
    type: :Person
    source: Enrico_Eugenio
  AssignClass (930dca6e-ef25-4dd1-871f-e4e3f8915e92)
 Call ID: 930dca6e-ef25-4dd1-871f-e4e3f8915e92
  Args:
    source: Noemi_Rosa_de_Alcorta_y_Garcia_Mansilla
    type: :Woman
  AssignClass (ad8ee278-0255-48e9-8bca-8d8dfc2e84ca)
 Call ID: ad8ee278-0255-48e9-8bca-8d8dfc2e84ca
  Args:
    type: :Person
    source: Noemi_Rosa_de_Alcorta_y_Garcia_Mansilla
  AssignClass (ed11bfa8-83eb-47e6-a8dc-8fbffd7d2606)
 Call ID: ed11bfa8-83eb-47e6-a8dc-8fbffd7d2606
  Args:
    source: Step_son_of_Maria_Cristina
    type: :Man
  AssignClass (f7d3f579-54f6-4f3f-ac8b-ee3c582f5c7f)
 Call ID: f7d3f579-54f6-4f3f-ac8b-ee3c582f5c7f
  Args:
    source: Step_son_of_Maria_Cristina
    type: :Person
  AddTriple (be1897a7-9f3a-4f88-86cd-62633b00da90)
 Call ID: be1897a7-9f3a-4f88-86cd-62633b00da90
  Args:
    relation: :hasChild
    target: Step_son_of_Maria_Cristina
    source: Enrico_Eugenio
  AddTriple (034a1241-97de-4e05-8407-f0b61cf9686b)
 Call ID: 034a1241-97de-4e05-8407-f0b61cf9686b
  Args:
    source: Noemi_Rosa_de_Alcorta_y_Garcia_Mansilla
    relation: :hasChild
    target: Step_son_of_Maria_Cristina
  Finish (ec406b11-4bcb-4408-b0c6-6f3bbc3aa3c2)
 Call ID: ec406b11-4bcb-4408-b0c6-6f3bbc3aa3c2
  Args: