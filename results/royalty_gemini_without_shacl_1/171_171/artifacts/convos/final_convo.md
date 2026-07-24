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
  AssignClass (4e610f3b-98bf-46c7-9d30-05c4b7c36dd6)
 Call ID: 4e610f3b-98bf-46c7-9d30-05c4b7c36dd6
  Args:
    source: Infanta_Maria_Cristina_of_Spain
    type: :Woman
  AssignClass (bfa22be9-7b82-4200-87c1-f2b5e2e4d80f)
 Call ID: bfa22be9-7b82-4200-87c1-f2b5e2e4d80f
  Args:
    type: :Person
    source: Infanta_Maria_Cristina_of_Spain
  AddLiteral (0d609228-7f32-4598-92ad-a6d21fed3766)
 Call ID: 0d609228-7f32-4598-92ad-a6d21fed3766
  Args:
    literal_value: 1911
    relation: :hasBirthYear
    source: Infanta_Maria_Cristina_of_Spain
    literal_type: xsd:integer
  AddLiteral (203e3533-1cae-4c4d-ae3f-5a795249f288)
 Call ID: 203e3533-1cae-4c4d-ae3f-5a795249f288
  Args:
    source: Infanta_Maria_Cristina_of_Spain
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1996
  AssignClass (db172ef6-bfe0-4e30-808c-7cab50105806)
 Call ID: db172ef6-bfe0-4e30-808c-7cab50105806
  Args:
    type: :Man
    source: Alfonso_XIII_of_Spain
  AssignClass (d01ad364-0261-46cc-a98c-6827531aaf7d)
 Call ID: d01ad364-0261-46cc-a98c-6827531aaf7d
  Args:
    source: Alfonso_XIII_of_Spain
    type: :Person
  AssignClass (c3ac633a-1e20-4875-9230-38a22109bd5e)
 Call ID: c3ac633a-1e20-4875-9230-38a22109bd5e
  Args:
    type: :Woman
    source: Victoria_Eugenie_of_Battenberg
  AssignClass (c1b215b3-1f03-4330-9353-9a32a9e09958)
 Call ID: c1b215b3-1f03-4330-9353-9a32a9e09958
  Args:
    source: Victoria_Eugenie_of_Battenberg
    type: :Person
  AddTriple (ec9771d9-7575-40ff-89b0-f86f5dcee0ba)
 Call ID: ec9771d9-7575-40ff-89b0-f86f5dcee0ba
  Args:
    target: Alfonso_XIII_of_Spain
    source: Infanta_Maria_Cristina_of_Spain
    relation: :hasFather
  AddTriple (5995c296-f618-44a6-a5f1-79098a9436a2)
 Call ID: 5995c296-f618-44a6-a5f1-79098a9436a2
  Args:
    target: Victoria_Eugenie_of_Battenberg
    relation: :hasMother
    source: Infanta_Maria_Cristina_of_Spain
  AssignClass (4ed25978-fd3a-4d08-8c17-3c83cd25e977)
 Call ID: 4ed25978-fd3a-4d08-8c17-3c83cd25e977
  Args:
    type: :Man
    source: Juan_Carlos_I_of_Spain
  AssignClass (b209afad-d351-4a68-960b-9c4c1c015669)
 Call ID: b209afad-d351-4a68-960b-9c4c1c015669
  Args:
    source: Juan_Carlos_I_of_Spain
    type: :Person
  AddTriple (cf4b0eb7-cabf-465c-8d9b-f38e1afa2b63)
 Call ID: cf4b0eb7-cabf-465c-8d9b-f38e1afa2b63
  Args:
    relation: :isAuntOf
    source: Infanta_Maria_Cristina_of_Spain
    target: Juan_Carlos_I_of_Spain
  AssignClass (1361a346-94b9-4ef7-86c6-b1a6be2b34bd)
 Call ID: 1361a346-94b9-4ef7-86c6-b1a6be2b34bd
  Args:
    type: :Man
    source: Alfonso_son_of_Alfonso_XIII
  AssignClass (689e1284-9208-4769-bdad-d0b26126d5ac)
 Call ID: 689e1284-9208-4769-bdad-d0b26126d5ac
  Args:
    type: :Person
    source: Alfonso_son_of_Alfonso_XIII
  AddTriple (7ecdd9f8-e532-4a45-b4ff-7ded9add3ced)
 Call ID: 7ecdd9f8-e532-4a45-b4ff-7ded9add3ced
  Args:
    target: Alfonso_XIII_of_Spain
    relation: :hasFather
    source: Alfonso_son_of_Alfonso_XIII
  AssignClass (d74df031-8388-4d90-b40a-287b67212be0)
 Call ID: d74df031-8388-4d90-b40a-287b67212be0
  Args:
    type: :Man
    source: Gonzalo_son_of_Alfonso_XIII
  AssignClass (781f1ac1-307d-4e0d-82eb-053c48eb748a)
 Call ID: 781f1ac1-307d-4e0d-82eb-053c48eb748a
  Args:
    type: :Person
    source: Gonzalo_son_of_Alfonso_XIII
  AddTriple (5e16e472-a2e6-443d-896e-1ba5825026a4)
 Call ID: 5e16e472-a2e6-443d-896e-1ba5825026a4
  Args:
    target: Alfonso_XIII_of_Spain
    source: Gonzalo_son_of_Alfonso_XIII
    relation: :hasFather
  AssignClass (5e94f93e-99c0-4009-a59b-f3038db037bd)
 Call ID: 5e94f93e-99c0-4009-a59b-f3038db037bd
  Args:
    source: Beatriz_of_Spain
    type: :Woman
  AssignClass (3ac87ea8-fdc8-46eb-a28b-88b9b9f35b7a)
 Call ID: 3ac87ea8-fdc8-46eb-a28b-88b9b9f35b7a
  Args:
    source: Beatriz_of_Spain
    type: :Person
  AddTriple (b224f2fa-2a30-4969-af44-bf19a74d67a9)
 Call ID: b224f2fa-2a30-4969-af44-bf19a74d67a9
  Args:
    source: Beatriz_of_Spain
    relation: :hasFather
    target: Alfonso_XIII_of_Spain
  AssignClass (6004bc59-7499-4bdc-9699-a8bf1731e090)
 Call ID: 6004bc59-7499-4bdc-9699-a8bf1731e090
  Args:
    source: Enrico_Eugenio
    type: :Man
  AssignClass (d1666e8f-0c8e-476b-87fe-21b06d7019e1)
 Call ID: d1666e8f-0c8e-476b-87fe-21b06d7019e1
  Args:
    source: Enrico_Eugenio
    type: :Person
  AssignClass (305ab615-1a3c-4f5c-b725-2507e5203c6f)
 Call ID: 305ab615-1a3c-4f5c-b725-2507e5203c6f
  Args:
    type: :Woman
    source: Noemi_Rosa_de_Alcorta_y_Garcia_Mansilla
  AssignClass (84ed61c1-24a8-4ee1-ba87-6dcb0d75546e)
 Call ID: 84ed61c1-24a8-4ee1-ba87-6dcb0d75546e
  Args:
    source: Noemi_Rosa_de_Alcorta_y_Garcia_Mansilla
    type: :Person
  AddTriple (be25e910-fee1-409b-b0d8-a31f9dacaf1e)
 Call ID: be25e910-fee1-409b-b0d8-a31f9dacaf1e
  Args:
    target: Enrico_Eugenio
    source: Infanta_Maria_Cristina_of_Spain
    relation: :hasRelation
  Finish (a3059fe0-7677-4d67-866c-15341d3d4a7a)
 Call ID: a3059fe0-7677-4d67-866c-15341d3d4a7a
  Args: