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
  AssignClass (72193b9d-d45a-4eae-b7d8-44c0be28f852)
 Call ID: 72193b9d-d45a-4eae-b7d8-44c0be28f852
  Args:
    source: Maria_Cristina_of_Spain
    type: :Woman
  AssignClass (76948865-a952-4ae7-8cff-ee343dac02cc)
 Call ID: 76948865-a952-4ae7-8cff-ee343dac02cc
  Args:
    source: Maria_Cristina_of_Spain
    type: :Person
  AddLiteral (a35f63fd-0eae-43e9-b999-e4bbe0869c3f)
 Call ID: a35f63fd-0eae-43e9-b999-e4bbe0869c3f
  Args:
    relation: :knownAs
    literal_type: xsd:string
    literal_value: Infanta Maria Cristina of Spain, Countess Marone-Cinzano
    source: Maria_Cristina_of_Spain
  AddLiteral (1fd6cc5d-6834-4b61-87e0-bfd637e719a7)
 Call ID: 1fd6cc5d-6834-4b61-87e0-bfd637e719a7
  Args:
    literal_value: 1911
    literal_type: xsd:integer
    source: Maria_Cristina_of_Spain
    relation: :hasBirthYear
  AddLiteral (f44a91e5-0b16-4fff-8c48-2dc54a9dac3a)
 Call ID: f44a91e5-0b16-4fff-8c48-2dc54a9dac3a
  Args:
    relation: :hasDeathYear
    literal_value: 1996
    literal_type: xsd:integer
    source: Maria_Cristina_of_Spain
  AssignClass (a6006964-943b-499d-b5c1-0431f2a90a11)
 Call ID: a6006964-943b-499d-b5c1-0431f2a90a11
  Args:
    type: :Man
    source: Alfonso_XIII_of_Spain
  AssignClass (90bd59a0-82df-4832-a521-8c04c61ea75c)
 Call ID: 90bd59a0-82df-4832-a521-8c04c61ea75c
  Args:
    source: Alfonso_XIII_of_Spain
    type: :Person
  AssignClass (7f95eedd-55ef-4fcd-87fa-dad67766f1f1)
 Call ID: 7f95eedd-55ef-4fcd-87fa-dad67766f1f1
  Args:
    type: :Woman
    source: Victoria_Eugenie_of_Battenberg
  AssignClass (a3a7a366-0ec1-486c-95dc-4425f15d9698)
 Call ID: a3a7a366-0ec1-486c-95dc-4425f15d9698
  Args:
    type: :Person
    source: Victoria_Eugenie_of_Battenberg
  AddTriple (a4be8c08-8f80-4a50-bac0-6cdc80772f6a)
 Call ID: a4be8c08-8f80-4a50-bac0-6cdc80772f6a
  Args:
    target: Alfonso_XIII_of_Spain
    source: Maria_Cristina_of_Spain
    relation: :hasFather
  AddTriple (c2141cbb-b14e-41ee-8072-9eb27ebae39c)
 Call ID: c2141cbb-b14e-41ee-8072-9eb27ebae39c
  Args:
    target: Victoria_Eugenie_of_Battenberg
    source: Maria_Cristina_of_Spain
    relation: :hasMother
  AssignClass (28449b62-88d3-4352-aeb5-2fa944652783)
 Call ID: 28449b62-88d3-4352-aeb5-2fa944652783
  Args:
    type: :Man
    source: Juan_Carlos_I_of_Spain
  AssignClass (55b102f0-de70-4180-b8c7-c2a325e6bcdb)
 Call ID: 55b102f0-de70-4180-b8c7-c2a325e6bcdb
  Args:
    source: Juan_Carlos_I_of_Spain
    type: :Person
  AddTriple (e288b966-1616-4af9-b112-a197a0395f19)
 Call ID: e288b966-1616-4af9-b112-a197a0395f19
  Args:
    target: Juan_Carlos_I_of_Spain
    source: Maria_Cristina_of_Spain
    relation: :isAuntOf
  AssignClass (c9db8da6-bc81-4b2e-aa00-5992eaaf5ede)
 Call ID: c9db8da6-bc81-4b2e-aa00-5992eaaf5ede
  Args:
    source: Infanta_Beatriz_of_Spain
    type: :Woman
  AssignClass (dcec9e15-83c8-4964-8a96-d61cc4b4ae2c)
 Call ID: dcec9e15-83c8-4964-8a96-d61cc4b4ae2c
  Args:
    type: :Person
    source: Infanta_Beatriz_of_Spain
  AddTriple (7b6ad17d-1707-4b0d-a683-93b720375394)
 Call ID: 7b6ad17d-1707-4b0d-a683-93b720375394
  Args:
    target: Infanta_Beatriz_of_Spain
    source: Maria_Cristina_of_Spain
    relation: :isSiblingOf
  AssignClass (f9dabc5c-e84f-4192-8552-1e1840e01663)
 Call ID: f9dabc5c-e84f-4192-8552-1e1840e01663
  Args:
    type: :Man
    source: Alfonso_of_Spain
  AssignClass (f4a31b5a-d8d1-4a45-814f-c153805c748f)
 Call ID: f4a31b5a-d8d1-4a45-814f-c153805c748f
  Args:
    type: :Person
    source: Alfonso_of_Spain
  AddTriple (668c8ef8-8fa6-48ea-96c9-d53aaffefe9d)
 Call ID: 668c8ef8-8fa6-48ea-96c9-d53aaffefe9d
  Args:
    relation: :isSiblingOf
    target: Alfonso_of_Spain
    source: Maria_Cristina_of_Spain
  AssignClass (f2799566-6c33-43f6-b4ba-001dbde65812)
 Call ID: f2799566-6c33-43f6-b4ba-001dbde65812
  Args:
    type: :Man
    source: Gonzalo_of_Spain
  AssignClass (d26e265d-6f55-4897-9cd3-c520bb65fd13)
 Call ID: d26e265d-6f55-4897-9cd3-c520bb65fd13
  Args:
    source: Gonzalo_of_Spain
    type: :Person
  AddTriple (c71df450-ab98-466e-b0ab-a4f2e9616247)
 Call ID: c71df450-ab98-466e-b0ab-a4f2e9616247
  Args:
    relation: :isSiblingOf
    source: Maria_Cristina_of_Spain
    target: Gonzalo_of_Spain
  AssignClass (a9dc2c42-36f5-4e0b-a5e9-40838cb8a3c3)
 Call ID: a9dc2c42-36f5-4e0b-a5e9-40838cb8a3c3
  Args:
    source: Enrico_Eugenio
    type: :Man
  AssignClass (1db3a032-7228-4cd3-aed3-0c518a487703)
 Call ID: 1db3a032-7228-4cd3-aed3-0c518a487703
  Args:
    source: Enrico_Eugenio
    type: :Person
  AssignClass (47a3768a-0bdf-4316-86ed-2e276998dad0)
 Call ID: 47a3768a-0bdf-4316-86ed-2e276998dad0
  Args:
    source: Noemi_Rosa_de_Alcorta_y_Garcia_Mansilla
    type: :Woman
  AssignClass (bc9c3391-eff3-41df-a4d6-730f3a5f958c)
 Call ID: bc9c3391-eff3-41df-a4d6-730f3a5f958c
  Args:
    type: :Person
    source: Noemi_Rosa_de_Alcorta_y_Garcia_Mansilla
  AssignClass (f58b5303-cac1-4ba6-b451-8a3617adbab4)
 Call ID: f58b5303-cac1-4ba6-b451-8a3617adbab4
  Args:
    type: :Man
    source: StepSon_of_Maria_Cristina
  AssignClass (ba232c00-71dd-44cf-98e9-264662b9a65b)
 Call ID: ba232c00-71dd-44cf-98e9-264662b9a65b
  Args:
    type: :Person
    source: StepSon_of_Maria_Cristina
  AddTriple (f33493be-c748-4f42-aeca-9c9ff491f52c)
 Call ID: f33493be-c748-4f42-aeca-9c9ff491f52c
  Args:
    target: Enrico_Eugenio
    source: StepSon_of_Maria_Cristina
    relation: :hasFather
  AddTriple (2d66af42-b58a-4161-a54a-c061de27c225)
 Call ID: 2d66af42-b58a-4161-a54a-c061de27c225
  Args:
    target: Noemi_Rosa_de_Alcorta_y_Garcia_Mansilla
    source: StepSon_of_Maria_Cristina
    relation: :hasMother
  Finish (82fbab9f-3dc5-4a6f-98f8-9d18d4ec1ebc)
 Call ID: 82fbab9f-3dc5-4a6f-98f8-9d18d4ec1ebc
  Args: