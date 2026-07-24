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
  AssignClass (be26e090-0ae5-4e49-b91c-998aedbd08d9)
 Call ID: be26e090-0ae5-4e49-b91c-998aedbd08d9
  Args:
    type: :Woman
    source: :MariaImmaculata
  AssignClass (7ac641de-5284-4357-a5d5-72651cfa5634)
 Call ID: 7ac641de-5284-4357-a5d5-72651cfa5634
  Args:
    source: :MariaImmaculata
    type: :Person
  AssignClass (f32ee9d6-ac9b-4761-b95d-6067337f1fed)
 Call ID: f32ee9d6-ac9b-4761-b95d-6067337f1fed
  Args:
    source: :Alfonso
    type: :Man
  AssignClass (c56b11fb-dbda-4fb9-bfa6-8592475a2f85)
 Call ID: c56b11fb-dbda-4fb9-bfa6-8592475a2f85
  Args:
    type: :Person
    source: :Alfonso
  AssignClass (9a90e817-6a58-474e-99ba-2378ae04f68b)
 Call ID: 9a90e817-6a58-474e-99ba-2378ae04f68b
  Args:
    type: :Woman
    source: :MariaAntonietta
  AssignClass (b87a1d7c-6bd3-4a31-bb6d-9d2979d76d6c)
 Call ID: b87a1d7c-6bd3-4a31-bb6d-9d2979d76d6c
  Args:
    type: :Person
    source: :MariaAntonietta
  AssignClass (8369e8a0-1b7a-4e51-bc46-aee02cb794fc)
 Call ID: 8369e8a0-1b7a-4e51-bc46-aee02cb794fc
  Args:
    type: :Man
    source: :JohannGeorg
  AssignClass (71c9e44e-6c38-42b1-8a15-2e744fd6cc72)
 Call ID: 71c9e44e-6c38-42b1-8a15-2e744fd6cc72
  Args:
    type: :Person
    source: :JohannGeorg
  AssignClass (36e6d755-10dc-41f9-b40b-ebbefdfab2ca)
 Call ID: 36e6d755-10dc-41f9-b40b-ebbefdfab2ca
  Args:
    type: :Man
    source: :GeorgeOfSaxony
  AssignClass (f2f6c165-e5cf-4f12-84f2-287400a6380c)
 Call ID: f2f6c165-e5cf-4f12-84f2-287400a6380c
  Args:
    type: :Person
    source: :GeorgeOfSaxony
  AssignClass (1cb0e068-756d-4c35-8b39-14ab067e853c)
 Call ID: 1cb0e068-756d-4c35-8b39-14ab067e853c
  Args:
    source: :MariaAnnaOfPortugal
    type: :Woman
  AssignClass (79572a58-2f5e-4516-befc-b3c1bdf80306)
 Call ID: 79572a58-2f5e-4516-befc-b3c1bdf80306
  Args:
    source: :MariaAnnaOfPortugal
    type: :Person
  AssignClass (1b85bff6-28a1-476e-aa12-01b84157dc59)
 Call ID: 1b85bff6-28a1-476e-aa12-01b84157dc59
  Args:
    type: :Woman
    source: :MariaIIOfPortugal
  AssignClass (8faf3446-472e-4627-919d-0a3e6cb72b8a)
 Call ID: 8faf3446-472e-4627-919d-0a3e6cb72b8a
  Args:
    source: :MariaIIOfPortugal
    type: :Person
  AssignClass (26bd456f-298c-4db8-af44-86bc50e86c6c)
 Call ID: 26bd456f-298c-4db8-af44-86bc50e86c6c
  Args:
    type: :Man
    source: :FerdinandIIOfPortugal
  AssignClass (c8ab4e13-e1fb-45f4-b9c7-93fdfc9eb66f)
 Call ID: c8ab4e13-e1fb-45f4-b9c7-93fdfc9eb66f
  Args:
    type: :Person
    source: :FerdinandIIOfPortugal
  AssignClass (de17a9c0-efd6-4298-a272-680532f1d545)
 Call ID: de17a9c0-efd6-4298-a272-680532f1d545
  Args:
    source: :FrederickAugustusIII
    type: :Man
  AssignClass (4ea519aa-0ee8-4e5b-bd9f-8c45e01c1e84)
 Call ID: 4ea519aa-0ee8-4e5b-bd9f-8c45e01c1e84
  Args:
    source: :FrederickAugustusIII
    type: :Person
  AddLiteral (e2e146fa-1648-4024-b122-5d3945087917)
 Call ID: e2e146fa-1648-4024-b122-5d3945087917
  Args:
    relation: :hasBirthYear
    source: :MariaImmaculata
    literal_type: xsd:integer
    literal_value: 1874
  AddLiteral (98812ada-c644-4a4d-8441-d2452122182b)
 Call ID: 98812ada-c644-4a4d-8441-d2452122182b
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: :MariaImmaculata
    literal_value: 1947
  AddTriple (b51c71e8-b69e-477d-9b93-8ec284df5187)
 Call ID: b51c71e8-b69e-477d-9b93-8ec284df5187
  Args:
    source: :MariaImmaculata
    target: :Alfonso
    relation: :hasFather
  AddTriple (6fb4e351-ff50-48c6-8ba8-ee0f8cfefc3c)
 Call ID: 6fb4e351-ff50-48c6-8ba8-ee0f8cfefc3c
  Args:
    target: :MariaAntonietta
    source: :MariaImmaculata
    relation: :hasMother
  AddLiteral (268e4542-9a17-4c8f-8371-2c6fc3210623)
 Call ID: 268e4542-9a17-4c8f-8371-2c6fc3210623
  Args:
    literal_value: 1906
    literal_type: xsd:integer
    source: :MariaImmaculata
    relation: :hasMarriageYear
  AddTriple (310c26a8-fe57-4482-8b4e-3c9f45ccf769)
 Call ID: 310c26a8-fe57-4482-8b4e-3c9f45ccf769
  Args:
    target: :JohannGeorg
    source: :MariaImmaculata
    relation: :hasRelation
  AddTriple (8e887cf7-9348-4580-90bd-a05e8785347b)
 Call ID: 8e887cf7-9348-4580-90bd-a05e8785347b
  Args:
    target: :GeorgeOfSaxony
    source: :JohannGeorg
    relation: :hasFather
  AddTriple (cf9578a5-02ac-4057-ab35-7e41b64d06e3)
 Call ID: cf9578a5-02ac-4057-ab35-7e41b64d06e3
  Args:
    source: :JohannGeorg
    target: :MariaAnnaOfPortugal
    relation: :hasMother
  AddTriple (e6cf499a-e674-40a5-a87d-5c294885aa6b)
 Call ID: e6cf499a-e674-40a5-a87d-5c294885aa6b
  Args:
    target: :FerdinandIIOfPortugal
    source: :MariaAnnaOfPortugal
    relation: :hasFather
  AddTriple (ee91a05a-384e-4727-81e9-cabbf095e31c)
 Call ID: ee91a05a-384e-4727-81e9-cabbf095e31c
  Args:
    target: :MariaIIOfPortugal
    source: :MariaAnnaOfPortugal
    relation: :hasMother
  AddTriple (8a32db4b-458c-4a21-9dc2-a316bd3f28b7)
 Call ID: 8a32db4b-458c-4a21-9dc2-a316bd3f28b7
  Args:
    relation: :isBrotherOf
    target: :JohannGeorg
    source: :FrederickAugustusIII
  Finish (b4f02624-4a93-409a-a0fd-293f163617ad)
 Call ID: b4f02624-4a93-409a-a0fd-293f163617ad
  Args: