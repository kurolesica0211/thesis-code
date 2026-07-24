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
  AssignClass (f58d64af-ad81-4bcc-90dd-75286aff038f)
 Call ID: f58d64af-ad81-4bcc-90dd-75286aff038f
  Args:
    source: Prince_Heinrich_of_Hesse-Kassel
    type: :Man
  AssignClass (53ca97d8-7da0-49d8-9ff6-d88ffe47a58e)
 Call ID: 53ca97d8-7da0-49d8-9ff6-d88ffe47a58e
  Args:
    source: Prince_Heinrich_of_Hesse-Kassel
    type: :Person
  AddLiteral (50d1b0d1-fccd-4767-8152-6ba9cb04dc0d)
 Call ID: 50d1b0d1-fccd-4767-8152-6ba9cb04dc0d
  Args:
    literal_value: 1927
    relation: :hasBirthYear
    source: Prince_Heinrich_of_Hesse-Kassel
    literal_type: xsd:integer
  AddLiteral (55472aa1-4f19-4b0a-851d-e112738ad7f5)
 Call ID: 55472aa1-4f19-4b0a-851d-e112738ad7f5
  Args:
    literal_value: 1999
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: Prince_Heinrich_of_Hesse-Kassel
  AddLiteral (6a02c371-baad-48b0-b884-b49d104bc7f2)
 Call ID: 6a02c371-baad-48b0-b884-b49d104bc7f2
  Args:
    source: Prince_Heinrich_of_Hesse-Kassel
    literal_type: xsd:string
    relation: :alsoKnownAs
    literal_value: Enrico d'Assia
  AssignClass (666a072b-88d0-424b-a1b5-92cdd1c3799c)
 Call ID: 666a072b-88d0-424b-a1b5-92cdd1c3799c
  Args:
    source: Prince_Philipp_of_Hesse
    type: :Man
  AssignClass (2d60a26b-403a-43b2-ac14-f90ddfbdd3fc)
 Call ID: 2d60a26b-403a-43b2-ac14-f90ddfbdd3fc
  Args:
    type: :Person
    source: Prince_Philipp_of_Hesse
  AssignClass (54f2ed21-bb10-4421-b02a-7a9971dffcf7)
 Call ID: 54f2ed21-bb10-4421-b02a-7a9971dffcf7
  Args:
    source: Princess_Mafalda_of_Savoy
    type: :Woman
  AssignClass (e970bd0d-13ad-49af-a431-5c778ee0add0)
 Call ID: e970bd0d-13ad-49af-a431-5c778ee0add0
  Args:
    source: Princess_Mafalda_of_Savoy
    type: :Person
  AddTriple (6e836da5-9a72-402e-8002-e9df872b065a)
 Call ID: 6e836da5-9a72-402e-8002-e9df872b065a
  Args:
    source: Prince_Heinrich_of_Hesse-Kassel
    target: Prince_Philipp_of_Hesse
    relation: :hasFather
  AddTriple (62b85911-2285-4acd-b164-0ed4432597d8)
 Call ID: 62b85911-2285-4acd-b164-0ed4432597d8
  Args:
    relation: :hasMother
    source: Prince_Heinrich_of_Hesse-Kassel
    target: Princess_Mafalda_of_Savoy
  AssignClass (5ec5047f-3a47-412b-82c5-71803f8d3dab)
 Call ID: 5ec5047f-3a47-412b-82c5-71803f8d3dab
  Args:
    type: :Man
    source: King_Victor_Emmanuel_III_of_Italy
  AssignClass (0ef8521e-9033-4dd2-9482-653c4cc76e76)
 Call ID: 0ef8521e-9033-4dd2-9482-653c4cc76e76
  Args:
    type: :Person
    source: King_Victor_Emmanuel_III_of_Italy
  AddTriple (f3017896-9154-4958-8791-28e4bc3dfae3)
 Call ID: f3017896-9154-4958-8791-28e4bc3dfae3
  Args:
    source: Princess_Mafalda_of_Savoy
    target: King_Victor_Emmanuel_III_of_Italy
    relation: :hasFather
  AssignClass (3f247633-3ea6-49ed-a9e5-70c506ba4881)
 Call ID: 3f247633-3ea6-49ed-a9e5-70c506ba4881
  Args:
    source: Moritz_of_Hesse
    type: :Man
  AssignClass (8c4b9ad6-4300-4dfa-90e5-f66540b67ec4)
 Call ID: 8c4b9ad6-4300-4dfa-90e5-f66540b67ec4
  Args:
    type: :Person
    source: Moritz_of_Hesse
  AssignClass (f4f86e0d-4bbc-4878-9cb8-6d209bba23e0)
 Call ID: f4f86e0d-4bbc-4878-9cb8-6d209bba23e0
  Args:
    type: :Man
    source: Otto_of_Hesse
  AssignClass (fb380756-29b0-4bf7-a17f-9b686ae8806f)
 Call ID: fb380756-29b0-4bf7-a17f-9b686ae8806f
  Args:
    source: Otto_of_Hesse
    type: :Person
  AssignClass (8100bb63-7884-4886-844f-bf839f56b514)
 Call ID: 8100bb63-7884-4886-844f-bf839f56b514
  Args:
    source: Elisabeth_of_Hesse
    type: :Woman
  AssignClass (c27a94a1-5689-4edf-b162-ff5a40f7b40e)
 Call ID: c27a94a1-5689-4edf-b162-ff5a40f7b40e
  Args:
    source: Elisabeth_of_Hesse
    type: :Person
  AddTriple (77cddebc-a313-4766-86a1-5fc9f1b0fd83)
 Call ID: 77cddebc-a313-4766-86a1-5fc9f1b0fd83
  Args:
    relation: :isSiblingOf
    source: Prince_Heinrich_of_Hesse-Kassel
    target: Moritz_of_Hesse
  AddTriple (9605281a-57f9-426b-acef-6bab4a70f6f9)
 Call ID: 9605281a-57f9-426b-acef-6bab4a70f6f9
  Args:
    relation: :isSiblingOf
    source: Prince_Heinrich_of_Hesse-Kassel
    target: Otto_of_Hesse
  AddTriple (2edceff4-d27b-481e-893a-4dd13ff2bbb3)
 Call ID: 2edceff4-d27b-481e-893a-4dd13ff2bbb3
  Args:
    relation: :isSiblingOf
    source: Prince_Heinrich_of_Hesse-Kassel
    target: Elisabeth_of_Hesse
  AssignClass (d56902a8-c3a5-4774-8a27-b7e272333184)
 Call ID: d56902a8-c3a5-4774-8a27-b7e272333184
  Args:
    source: Margaret_Campbell_Geddes
    type: :Woman
  AssignClass (5eef2be6-31fd-4801-bfed-51f606e3da58)
 Call ID: 5eef2be6-31fd-4801-bfed-51f606e3da58
  Args:
    type: :Person
    source: Margaret_Campbell_Geddes
  AssignClass (cafcec46-f958-4a4a-861c-400f8b11a31b)
 Call ID: cafcec46-f958-4a4a-861c-400f8b11a31b
  Args:
    source: Louis_Prince_of_Hesse_and_by_Rhine
    type: :Man
  AssignClass (ec34404f-c3b4-4879-9bc9-faa64f3bbd15)
 Call ID: ec34404f-c3b4-4879-9bc9-faa64f3bbd15
  Args:
    type: :Person
    source: Louis_Prince_of_Hesse_and_by_Rhine
  AddTriple (cc1bce53-a193-4006-9fbe-f70c857955fa)
 Call ID: cc1bce53-a193-4006-9fbe-f70c857955fa
  Args:
    source: Margaret_Campbell_Geddes
    target: Prince_Heinrich_of_Hesse-Kassel
    relation: :isAuntOf
  AddTriple (dd5cd2b9-bf97-4e4a-8ca7-1fa5e4b375ea)
 Call ID: dd5cd2b9-bf97-4e4a-8ca7-1fa5e4b375ea
  Args:
    source: Louis_Prince_of_Hesse_and_by_Rhine
    target: Prince_Heinrich_of_Hesse-Kassel
    relation: :isUncleOf
  Finish (9dbf8ef3-29ed-4421-92b2-7c2c35089713)
 Call ID: 9dbf8ef3-29ed-4421-92b2-7c2c35089713
  Args: