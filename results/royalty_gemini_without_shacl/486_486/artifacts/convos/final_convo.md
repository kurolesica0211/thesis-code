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
Prince Heinrich Wilhelm Konstantin Viktor Franz of Hesse-Kassel (30 October 1927 – 18 November 1999), also known as Enrico d'Assia, was the second child of Prince Philipp of Hesse and Princess Mafalda of Savoy.
Heinrich became an artist, set designer, and memoirist after World War II.
Life

Prince Heinrich was born in Rome, Italy, as the second son of Prince Philipp of Hesse and Princess Mafalda of Savoy, daughter of King Victor Emmanuel III of Italy.
During the Second World War, Heinrich's father, an important former aristocratic Nazi party member, was arrested by the Gestapo.
Heinrich and his siblings (Moritz, Otto and Elisabeth) were given sanctuary in the Vatican under the care of their aunt and uncle, Margaret Campbell Geddes and Louis, Prince of Hesse and by Rhine, who adopted them.
Heinrich was an artist and set designer, active mainly in Italy under the name Enrico d'Assia.



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
  AssignClass (c53a7383-0935-46fd-ad73-2cc984008c58)
 Call ID: c53a7383-0935-46fd-ad73-2cc984008c58
  Args:
    type: :Man
    source: Prince_Heinrich_of_Hesse-Kassel
  AssignClass (0fb70732-0494-46bd-955d-5a0577e8f2b4)
 Call ID: 0fb70732-0494-46bd-955d-5a0577e8f2b4
  Args:
    type: :Person
    source: Prince_Heinrich_of_Hesse-Kassel
  AssignClass (78aa553c-d71e-4485-87c9-cbdac3e1f33e)
 Call ID: 78aa553c-d71e-4485-87c9-cbdac3e1f33e
  Args:
    source: Prince_Philipp_of_Hesse
    type: :Man
  AssignClass (ab11423d-11e7-41a8-bdae-625d76d69b8d)
 Call ID: ab11423d-11e7-41a8-bdae-625d76d69b8d
  Args:
    type: :Person
    source: Prince_Philipp_of_Hesse
  AssignClass (a3a2e19f-750c-4a6b-b3dd-a10fb2f28c90)
 Call ID: a3a2e19f-750c-4a6b-b3dd-a10fb2f28c90
  Args:
    source: Princess_Mafalda_of_Savoy
    type: :Woman
  AssignClass (095c7571-857d-47ad-ac60-c62466fa94aa)
 Call ID: 095c7571-857d-47ad-ac60-c62466fa94aa
  Args:
    source: Princess_Mafalda_of_Savoy
    type: :Person
  AssignClass (1dfc4fca-2723-4c6a-9cea-b95b29f65544)
 Call ID: 1dfc4fca-2723-4c6a-9cea-b95b29f65544
  Args:
    type: :Man
    source: King_Victor_Emmanuel_III_of_Italy
  AssignClass (9650d11e-4c66-4832-83e3-1700cb02911a)
 Call ID: 9650d11e-4c66-4832-83e3-1700cb02911a
  Args:
    type: :Person
    source: King_Victor_Emmanuel_III_of_Italy
  AssignClass (7e535e92-a33f-4080-b781-7340d47f9ca9)
 Call ID: 7e535e92-a33f-4080-b781-7340d47f9ca9
  Args:
    type: :Man
    source: Moritz_of_Hesse-Kassel
  AssignClass (cc46486a-2877-4647-b1e0-598244745b53)
 Call ID: cc46486a-2877-4647-b1e0-598244745b53
  Args:
    source: Moritz_of_Hesse-Kassel
    type: :Person
  AssignClass (7ae027c2-80b9-40e0-93cb-389d101f4de3)
 Call ID: 7ae027c2-80b9-40e0-93cb-389d101f4de3
  Args:
    source: Otto_of_Hesse-Kassel
    type: :Man
  AssignClass (3af61885-011f-462c-8276-38bb4a54a114)
 Call ID: 3af61885-011f-462c-8276-38bb4a54a114
  Args:
    source: Otto_of_Hesse-Kassel
    type: :Person
  AssignClass (3ae7584b-149a-4e38-aa64-7631515bf258)
 Call ID: 3ae7584b-149a-4e38-aa64-7631515bf258
  Args:
    type: :Woman
    source: Elisabeth_of_Hesse-Kassel
  AssignClass (47f4012a-9b2e-4c10-8a5c-0e0d701d025e)
 Call ID: 47f4012a-9b2e-4c10-8a5c-0e0d701d025e
  Args:
    type: :Person
    source: Elisabeth_of_Hesse-Kassel
  AssignClass (35980543-aa3e-471e-9dfc-41e826f06fa4)
 Call ID: 35980543-aa3e-471e-9dfc-41e826f06fa4
  Args:
    source: Margaret_Campbell_Geddes
    type: :Woman
  AssignClass (d6324a25-8352-4896-bbbf-e14f65473a52)
 Call ID: d6324a25-8352-4896-bbbf-e14f65473a52
  Args:
    source: Margaret_Campbell_Geddes
    type: :Person
  AssignClass (98bb38ef-7dcc-4d88-a382-fb3fb7e6d4a3)
 Call ID: 98bb38ef-7dcc-4d88-a382-fb3fb7e6d4a3
  Args:
    type: :Man
    source: Louis_Prince_of_Hesse_and_by_Rhine
  AssignClass (748654c8-837d-4589-9b73-8cdbe8370312)
 Call ID: 748654c8-837d-4589-9b73-8cdbe8370312
  Args:
    source: Louis_Prince_of_Hesse_and_by_Rhine
    type: :Person
  AddLiteral (3d64a1d4-8bda-45bb-b342-e238fafcaf35)
 Call ID: 3d64a1d4-8bda-45bb-b342-e238fafcaf35
  Args:
    source: Prince_Heinrich_of_Hesse-Kassel
    literal_type: xsd:string
    relation: :alsoKnownAs
    literal_value: Enrico d'Assia
  AddLiteral (f4e34b77-4188-422d-b960-c2486e5864e6)
 Call ID: f4e34b77-4188-422d-b960-c2486e5864e6
  Args:
    literal_value: 1927
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Prince_Heinrich_of_Hesse-Kassel
  AddLiteral (093cdb05-7a24-400d-ac96-4b52ec3cafd1)
 Call ID: 093cdb05-7a24-400d-ac96-4b52ec3cafd1
  Args:
    literal_value: 1999
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: Prince_Heinrich_of_Hesse-Kassel
  AddTriple (abcbbb8d-1073-4dd3-af6b-aab8684e8241)
 Call ID: abcbbb8d-1073-4dd3-af6b-aab8684e8241
  Args:
    relation: :hasFather
    target: Prince_Philipp_of_Hesse
    source: Prince_Heinrich_of_Hesse-Kassel
  AddTriple (b39a615e-4c0a-4444-89a0-aa87e25c3c03)
 Call ID: b39a615e-4c0a-4444-89a0-aa87e25c3c03
  Args:
    relation: :hasMother
    source: Prince_Heinrich_of_Hesse-Kassel
    target: Princess_Mafalda_of_Savoy
  AddTriple (0ee82662-a843-47ea-888c-bd0aff62ebec)
 Call ID: 0ee82662-a843-47ea-888c-bd0aff62ebec
  Args:
    relation: :hasFather
    source: Princess_Mafalda_of_Savoy
    target: King_Victor_Emmanuel_III_of_Italy
  AddTriple (fadc38dd-fa68-46af-93fe-84a71606ec61)
 Call ID: fadc38dd-fa68-46af-93fe-84a71606ec61
  Args:
    relation: :hasBrother
    source: Prince_Heinrich_of_Hesse-Kassel
    target: Moritz_of_Hesse-Kassel
  AddTriple (7d9e1a7b-8ef8-43a2-8b3c-eb7a2d11f5c0)
 Call ID: 7d9e1a7b-8ef8-43a2-8b3c-eb7a2d11f5c0
  Args:
    source: Prince_Heinrich_of_Hesse-Kassel
    target: Otto_of_Hesse-Kassel
    relation: :hasBrother
  AddTriple (1fd07c5e-b79e-4884-b40e-f52a0886679b)
 Call ID: 1fd07c5e-b79e-4884-b40e-f52a0886679b
  Args:
    target: Elisabeth_of_Hesse-Kassel
    source: Prince_Heinrich_of_Hesse-Kassel
    relation: :hasSister
  Finish (5f2d2de7-8448-42f3-a7c9-4a92d5d1d160)
 Call ID: 5f2d2de7-8448-42f3-a7c9-4a92d5d1d160
  Args: