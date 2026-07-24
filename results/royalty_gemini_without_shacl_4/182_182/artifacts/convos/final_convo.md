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
Princess Maria Immaculata Cristina Pia Isabella of Bourbon-Two Sicilies (Full Italian name: Maria Immacolata Speranza Pia Teresa Cristina Filomena Lucia Anna Isabella Cecilia Apollonia Barbara Agnese Zenobia, Principessa di Borbone delle
Due Sicilie,) (30 October 1874 – 28 November 1947) was the fourth child and eldest daughter of Prince Alfonso of Bourbon-Two Sicilies, Count of Caserta, and his wife Princess Maria Antonietta of Bourbon-Two Sicilies.
Marriage

Maria Immaculata married Prince Johann Georg of Saxony, sixth child and second-eldest son of George of Saxony and his wife Maria Anna of Portugal, on 30 October 1906 in Cannes.
Her mother-in-law, Maria Anna, was the daughter of Maria II of Portugal and her husband Ferdinand II of Portugal.
The couple did not have children, but Maria Immaculata cared for the children of her brother-in-law Frederick Augustus III of Saxony.



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
  AssignClass (f006c94e-4f4d-490e-bef6-60e03fcd27cb)
 Call ID: f006c94e-4f4d-490e-bef6-60e03fcd27cb
  Args:
    source: Maria_Immaculata_of_Bourbon-Two_Sicilies
    type: :Woman
  AssignClass (fdf65ec7-ab39-4a0d-b823-2639528fe911)
 Call ID: fdf65ec7-ab39-4a0d-b823-2639528fe911
  Args:
    source: Maria_Immaculata_of_Bourbon-Two_Sicilies
    type: :Person
  AddLiteral (c152be4f-6505-4876-9ad2-07f523535200)
 Call ID: c152be4f-6505-4876-9ad2-07f523535200
  Args:
    source: Maria_Immaculata_of_Bourbon-Two_Sicilies
    literal_value: 1874
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (755e8094-3f1b-4f4d-a408-3d5d9e87e51f)
 Call ID: 755e8094-3f1b-4f4d-a408-3d5d9e87e51f
  Args:
    relation: :hasDeathYear
    literal_value: 1947
    literal_type: xsd:integer
    source: Maria_Immaculata_of_Bourbon-Two_Sicilies
  AssignClass (15ac89e6-8f62-444c-93f1-64a68bc43c83)
 Call ID: 15ac89e6-8f62-444c-93f1-64a68bc43c83
  Args:
    type: :Man
    source: Alfonso_of_Bourbon-Two_Sicilies
  AssignClass (77bdbff5-049e-43cf-b6e9-c54f849617c0)
 Call ID: 77bdbff5-049e-43cf-b6e9-c54f849617c0
  Args:
    source: Alfonso_of_Bourbon-Two_Sicilies
    type: :Person
  AssignClass (3856e63d-104c-40e4-ae0c-1edab3092895)
 Call ID: 3856e63d-104c-40e4-ae0c-1edab3092895
  Args:
    source: Maria_Antonietta_of_Bourbon-Two_Sicilies
    type: :Woman
  AssignClass (2c65e6d6-fe07-4a40-b693-b427548c0f3f)
 Call ID: 2c65e6d6-fe07-4a40-b693-b427548c0f3f
  Args:
    source: Maria_Antonietta_of_Bourbon-Two_Sicilies
    type: :Person
  AddTriple (ba11e082-4f07-493e-9265-033e6a3c2e2b)
 Call ID: ba11e082-4f07-493e-9265-033e6a3c2e2b
  Args:
    target: Alfonso_of_Bourbon-Two_Sicilies
    relation: :hasFather
    source: Maria_Immaculata_of_Bourbon-Two_Sicilies
  AddTriple (2743afa7-1d4e-4e02-87b5-a0f04a815bd5)
 Call ID: 2743afa7-1d4e-4e02-87b5-a0f04a815bd5
  Args:
    target: Maria_Antonietta_of_Bourbon-Two_Sicilies
    relation: :hasMother
    source: Maria_Immaculata_of_Bourbon-Two_Sicilies
  AssignClass (e3c040a4-0663-4394-a18b-75afd64b2c39)
 Call ID: e3c040a4-0663-4394-a18b-75afd64b2c39
  Args:
    type: :Man
    source: Johann_Georg_of_Saxony
  AssignClass (a5150b0f-eb2e-4257-a8aa-4ae53f6f6020)
 Call ID: a5150b0f-eb2e-4257-a8aa-4ae53f6f6020
  Args:
    type: :Person
    source: Johann_Georg_of_Saxony
  AddLiteral (e1bb2b16-a28b-457d-a8f4-8e50b13723a2)
 Call ID: e1bb2b16-a28b-457d-a8f4-8e50b13723a2
  Args:
    relation: :hasMarriageYear
    source: Maria_Immaculata_of_Bourbon-Two_Sicilies
    literal_type: xsd:integer
    literal_value: 1906
  AddTriple (ee6bc07c-513f-452c-a219-970d898a21d5)
 Call ID: ee6bc07c-513f-452c-a219-970d898a21d5
  Args:
    source: Maria_Immaculata_of_Bourbon-Two_Sicilies
    target: Johann_Georg_of_Saxony
    relation: :hasRelation
  AssignClass (0f04f7a2-b823-49a3-a0f0-f54b2a36f802)
 Call ID: 0f04f7a2-b823-49a3-a0f0-f54b2a36f802
  Args:
    source: George_of_Saxony
    type: :Man
  AssignClass (118d1097-45b7-40af-ad3d-34b60a960872)
 Call ID: 118d1097-45b7-40af-ad3d-34b60a960872
  Args:
    source: George_of_Saxony
    type: :Person
  AssignClass (c3f200ec-1a83-4aad-9fd3-5b9723e9cef8)
 Call ID: c3f200ec-1a83-4aad-9fd3-5b9723e9cef8
  Args:
    source: Maria_Anna_of_Portugal
    type: :Woman
  AssignClass (0a6434d6-f412-490b-a447-6e59f51f1b57)
 Call ID: 0a6434d6-f412-490b-a447-6e59f51f1b57
  Args:
    type: :Person
    source: Maria_Anna_of_Portugal
  AddTriple (7355034f-7db2-4990-a51d-94817feb2898)
 Call ID: 7355034f-7db2-4990-a51d-94817feb2898
  Args:
    source: Johann_Georg_of_Saxony
    target: George_of_Saxony
    relation: :hasFather
  AddTriple (6617ff54-88e0-47d9-8802-9f29dd2cd609)
 Call ID: 6617ff54-88e0-47d9-8802-9f29dd2cd609
  Args:
    source: Johann_Georg_of_Saxony
    target: Maria_Anna_of_Portugal
    relation: :hasMother
  AssignClass (cb08a75c-f1b2-4b37-9c09-a797b7d4b798)
 Call ID: cb08a75c-f1b2-4b37-9c09-a797b7d4b798
  Args:
    source: Maria_II_of_Portugal
    type: :Woman
  AssignClass (26cb9965-dab2-49ba-a696-19ac11d85c02)
 Call ID: 26cb9965-dab2-49ba-a696-19ac11d85c02
  Args:
    type: :Person
    source: Maria_II_of_Portugal
  AssignClass (2ee4eb51-6f99-4b5b-ae50-a7eec573a8bd)
 Call ID: 2ee4eb51-6f99-4b5b-ae50-a7eec573a8bd
  Args:
    source: Ferdinand_II_of_Portugal
    type: :Man
  AssignClass (d66d9dbe-b90d-4d7d-802b-e76641e02692)
 Call ID: d66d9dbe-b90d-4d7d-802b-e76641e02692
  Args:
    type: :Person
    source: Ferdinand_II_of_Portugal
  AddTriple (d37eadeb-fafd-4a7c-8fa4-3006d16fe974)
 Call ID: d37eadeb-fafd-4a7c-8fa4-3006d16fe974
  Args:
    source: Maria_Anna_of_Portugal
    target: Maria_II_of_Portugal
    relation: :hasMother
  AddTriple (87b6386d-d5c1-499c-980f-01d2901f3d26)
 Call ID: 87b6386d-d5c1-499c-980f-01d2901f3d26
  Args:
    relation: :hasFather
    target: Ferdinand_II_of_Portugal
    source: Maria_Anna_of_Portugal
  AssignClass (c3c85af9-2232-41cd-8fb2-8081246e2075)
 Call ID: c3c85af9-2232-41cd-8fb2-8081246e2075
  Args:
    source: Frederick_Augustus_III_of_Saxony
    type: :Man
  AssignClass (9efc0a66-f86e-4e77-bce9-325fca88fb72)
 Call ID: 9efc0a66-f86e-4e77-bce9-325fca88fb72
  Args:
    type: :Person
    source: Frederick_Augustus_III_of_Saxony
  AddTriple (599b7d94-61e2-4f01-bed4-b17c53b79e68)
 Call ID: 599b7d94-61e2-4f01-bed4-b17c53b79e68
  Args:
    source: Frederick_Augustus_III_of_Saxony
    relation: :isBrotherOf
    target: Johann_Georg_of_Saxony
  Finish (95d5b4c5-b948-4b16-ac28-84f1f7c5b40a)
 Call ID: 95d5b4c5-b948-4b16-ac28-84f1f7c5b40a
  Args: