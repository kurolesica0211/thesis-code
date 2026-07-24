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
  AssignClass (2b82b31f-cb46-45f2-8c1c-03e4fe5ac167)
 Call ID: 2b82b31f-cb46-45f2-8c1c-03e4fe5ac167
  Args:
    type: :Person
    source: Charlotte_Wellesley
  AssignClass (cf90fb99-2622-4626-855b-61b7837a13c1)
 Call ID: cf90fb99-2622-4626-855b-61b7837a13c1
  Args:
    type: :Woman
    source: Charlotte_Wellesley
  AddLiteral (e96b1107-e516-4c3a-90c7-5a7f86b2864c)
 Call ID: e96b1107-e516-4c3a-90c7-5a7f86b2864c
  Args:
    literal_value: 1990
    source: Charlotte_Wellesley
    literal_type: xsd:positiveInteger
    relation: :hasBirthYear
  AssignClass (ee4847e2-ad72-4dd6-a2cd-eecedb4d2f0d)
 Call ID: ee4847e2-ad72-4dd6-a2cd-eecedb4d2f0d
  Args:
    type: :Person
    source: Antonia_of_Prussia
  AssignClass (ad1997e3-df26-4145-8a35-c0131e840668)
 Call ID: ad1997e3-df26-4145-8a35-c0131e840668
  Args:
    type: :Woman
    source: Antonia_of_Prussia
  AssignClass (04c6482c-0d13-487a-9f0d-e3c93e71495f)
 Call ID: 04c6482c-0d13-487a-9f0d-e3c93e71495f
  Args:
    type: :Person
    source: Charles_Wellesley
  AssignClass (515778a8-9bfe-4fd6-b238-fd73626b457a)
 Call ID: 515778a8-9bfe-4fd6-b238-fd73626b457a
  Args:
    type: :Man
    source: Charles_Wellesley
  AddTriple (41da46ed-5dce-46ae-a0b7-68e624dff943)
 Call ID: 41da46ed-5dce-46ae-a0b7-68e624dff943
  Args:
    relation: :hasMother
    source: Charlotte_Wellesley
    target: Antonia_of_Prussia
  AddTriple (40b406ec-a67f-4615-bb53-d7935c2cf2a2)
 Call ID: 40b406ec-a67f-4615-bb53-d7935c2cf2a2
  Args:
    relation: :hasFather
    source: Charlotte_Wellesley
    target: Charles_Wellesley
  AssignClass (a790937d-7e09-494c-923b-a056edf87eb3)
 Call ID: a790937d-7e09-494c-923b-a056edf87eb3
  Args:
    type: :Person
    source: Valerian_Wellesley
  AssignClass (8caa0b44-f10e-4c01-a843-93e5c3d6f09d)
 Call ID: 8caa0b44-f10e-4c01-a843-93e5c3d6f09d
  Args:
    type: :Man
    source: Valerian_Wellesley
  AddTriple (210ec39f-9f61-4530-9d6c-dd166a541f1e)
 Call ID: 210ec39f-9f61-4530-9d6c-dd166a541f1e
  Args:
    target: Valerian_Wellesley
    source: Charles_Wellesley
    relation: :hasFather
  AddLiteral (3f016f71-4378-4a68-a064-6f8d5c3752f2)
 Call ID: 3f016f71-4378-4a68-a064-6f8d5c3752f2
  Args:
    relation: :hasDeathYear
    literal_value: 2014
    source: Valerian_Wellesley
    literal_type: xsd:positiveInteger
  AssignClass (00309d66-d338-44c2-8eb6-80ce33bca01f)
 Call ID: 00309d66-d338-44c2-8eb6-80ce33bca01f
  Args:
    type: :Person
    source: Frederick_of_Prussia
  AssignClass (60994141-ee4a-43b5-a9e6-6dfcdfb0d4cb)
 Call ID: 60994141-ee4a-43b5-a9e6-6dfcdfb0d4cb
  Args:
    type: :Man
    source: Frederick_of_Prussia
  AssignClass (ac313d58-5ccc-4810-aed9-9be25695b6fd)
 Call ID: ac313d58-5ccc-4810-aed9-9be25695b6fd
  Args:
    type: :Person
    source: Brigid_Guinness
  AssignClass (7f2996e5-7ee8-4bac-882e-9ca40bd18705)
 Call ID: 7f2996e5-7ee8-4bac-882e-9ca40bd18705
  Args:
    type: :Woman
    source: Brigid_Guinness
  AddTriple (b3e976a5-ffe7-4b22-a8ec-d4c73650a5bb)
 Call ID: b3e976a5-ffe7-4b22-a8ec-d4c73650a5bb
  Args:
    target: Frederick_of_Prussia
    source: Antonia_of_Prussia
    relation: :hasFather
  AddTriple (9c506b58-7c7b-453d-913f-0a0e6bb2d0d9)
 Call ID: 9c506b58-7c7b-453d-913f-0a0e6bb2d0d9
  Args:
    source: Antonia_of_Prussia
    target: Brigid_Guinness
    relation: :hasMother
  AssignClass (2f690a1f-26d7-4820-9e42-1184f5afcbe3)
 Call ID: 2f690a1f-26d7-4820-9e42-1184f5afcbe3
  Args:
    type: :Person
    source: Arthur_Wellesley
  AssignClass (82f74089-fd2d-40ad-aa9f-d2dd4084fa8b)
 Call ID: 82f74089-fd2d-40ad-aa9f-d2dd4084fa8b
  Args:
    type: :Man
    source: Arthur_Wellesley
  AssignClass (11998587-d9b8-4e6e-ae72-a8b69e4b5b56)
 Call ID: 11998587-d9b8-4e6e-ae72-a8b69e4b5b56
  Args:
    type: :Person
    source: Mary_Wellesley
  AssignClass (d74fef33-2f9c-48e6-9945-3df3b2642d7b)
 Call ID: d74fef33-2f9c-48e6-9945-3df3b2642d7b
  Args:
    type: :Woman
    source: Mary_Wellesley
  AddTriple (e51ec97d-f2d5-4e34-a0bc-7846ac8457c5)
 Call ID: e51ec97d-f2d5-4e34-a0bc-7846ac8457c5
  Args:
    target: Arthur_Wellesley
    source: Charlotte_Wellesley
    relation: :hasBrother
  AddTriple (f04d4faf-64a9-453e-8aa1-2185ef6c5fcf)
 Call ID: f04d4faf-64a9-453e-8aa1-2185ef6c5fcf
  Args:
    relation: :hasSister
    target: Mary_Wellesley
    source: Charlotte_Wellesley
  AssignClass (b44a75a5-931b-4658-9a6a-c9986a92c053)
 Call ID: b44a75a5-931b-4658-9a6a-c9986a92c053
  Args:
    type: :Person
    source: Alejandro_Santo_Domingo
  AssignClass (a64a0ecc-9557-4002-887d-d5afc0cf4f58)
 Call ID: a64a0ecc-9557-4002-887d-d5afc0cf4f58
  Args:
    type: :Man
    source: Alejandro_Santo_Domingo
  AddTriple (eaaab92c-e72f-4a26-aa63-cc2f1eb78f6e)
 Call ID: eaaab92c-e72f-4a26-aa63-cc2f1eb78f6e
  Args:
    relation: :hasRelation
    target: Alejandro_Santo_Domingo
    source: Charlotte_Wellesley
  AddLiteral (0df4c0ce-1b0a-421f-b0d4-6411d39c5e3f)
 Call ID: 0df4c0ce-1b0a-421f-b0d4-6411d39c5e3f
  Args:
    literal_value: 2016
    source: Charlotte_Wellesley
    literal_type: xsd:positiveInteger
    relation: :hasMarriageYear
  Finish (a8791043-d6da-4dd3-9b33-7e7690c4de86)
 Call ID: a8791043-d6da-4dd3-9b33-7e7690c4de86
  Args: