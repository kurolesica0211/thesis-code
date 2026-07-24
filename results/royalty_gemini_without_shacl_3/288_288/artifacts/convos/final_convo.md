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
Lady Rose Victoria Birgitte Louise Gilman (née Windsor; born 1 March 1980) is a British film art assistant and member of the British royal family.
She is the daughter of Prince Richard, Duke of Gloucester, and his wife Birgitte, Duchess of Gloucester.
Early life and education

Rose Victoria Birgitte Louise Windsor was born on 1 March 1980 at St Mary's Hospital, London, the youngest child of Prince Richard, Duke of Gloucester and Birgitte, Duchess of Gloucester.
Her godparents included Prince Edward and Lady Sarah Armstrong-Jones.
Career

Rose has worked in the film industry as a film art assistant.
Her film credits include Harry Potter and the Order of the Phoenix, Harry Potter and the Half-Blood Prince, Margaret Thatcher: The Long Walk to Finchley, and the television series Little Britain.
Rose continues to make public appearances at state events alongside other members of the extended royal family, including the 2022 state funeral of Queen Elizabeth II and the 2023 coronation of King Charles III and Queen Camilla.
Marriage and children

Rose announced her engagement on 16 November 2007 to businessman George Gilman, the son of a former director of Leeds United.
Rose and her husband have a daughter, Lyla (born 30 May 2010, then 32nd in line of succession to the British throne), and a son, Rufus (born 30 October 2012, then 33rd in line of succession to the British throne).



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
  AssignClass (a807cdee-7872-41f9-8656-4e0c25c80f9b)
 Call ID: a807cdee-7872-41f9-8656-4e0c25c80f9b
  Args:
    type: :Woman
    source: :Rose_Windsor
  AssignClass (5e251fda-eec1-4ad2-856f-8fe0b72af359)
 Call ID: 5e251fda-eec1-4ad2-856f-8fe0b72af359
  Args:
    type: :Person
    source: :Rose_Windsor
  AssignClass (9d0d308e-080d-4691-8fbd-a6f65e784269)
 Call ID: 9d0d308e-080d-4691-8fbd-a6f65e784269
  Args:
    type: :Man
    source: :Prince_Richard_Duke_of_Gloucester
  AssignClass (bd637ab7-79ab-463b-adc2-046885c88250)
 Call ID: bd637ab7-79ab-463b-adc2-046885c88250
  Args:
    type: :Person
    source: :Prince_Richard_Duke_of_Gloucester
  AssignClass (1e184b7a-c928-49b0-9b3c-ab3517494ff7)
 Call ID: 1e184b7a-c928-49b0-9b3c-ab3517494ff7
  Args:
    source: :Birgitte_Duchess_of_Gloucester
    type: :Woman
  AssignClass (71075f2e-2259-46b2-a6d6-76a6f9908f94)
 Call ID: 71075f2e-2259-46b2-a6d6-76a6f9908f94
  Args:
    source: :Birgitte_Duchess_of_Gloucester
    type: :Person
  AssignClass (769e0bc7-7587-4e6c-b7c7-2d3b3190be0d)
 Call ID: 769e0bc7-7587-4e6c-b7c7-2d3b3190be0d
  Args:
    source: :George_Gilman
    type: :Man
  AssignClass (d92b7a17-a9a6-45c7-b266-6a46b5b18431)
 Call ID: d92b7a17-a9a6-45c7-b266-6a46b5b18431
  Args:
    source: :George_Gilman
    type: :Person
  AssignClass (59cb9b09-29b7-44e4-8ca6-62431648ae41)
 Call ID: 59cb9b09-29b7-44e4-8ca6-62431648ae41
  Args:
    source: :Lyla_Gilman
    type: :Woman
  AssignClass (bbdd16aa-db73-4730-9c60-d9d1a1532f87)
 Call ID: bbdd16aa-db73-4730-9c60-d9d1a1532f87
  Args:
    source: :Lyla_Gilman
    type: :Person
  AssignClass (248985cf-a402-48a6-b8ea-4992f480f195)
 Call ID: 248985cf-a402-48a6-b8ea-4992f480f195
  Args:
    source: :Rufus_Gilman
    type: :Man
  AssignClass (ebb5dd0f-8f36-4bf1-b3d7-e439877e6135)
 Call ID: ebb5dd0f-8f36-4bf1-b3d7-e439877e6135
  Args:
    source: :Rufus_Gilman
    type: :Person
  AddLiteral (3599a105-393b-43d6-ae93-4c0d36650772)
 Call ID: 3599a105-393b-43d6-ae93-4c0d36650772
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: :Rose_Windsor
    literal_value: 1980
  AddTriple (f908cd62-9d04-440c-90a8-53f0b959abf2)
 Call ID: f908cd62-9d04-440c-90a8-53f0b959abf2
  Args:
    source: :Rose_Windsor
    target: :Prince_Richard_Duke_of_Gloucester
    relation: :hasFather
  AddTriple (8fd96163-89b1-4b54-bf78-68b30b0d787d)
 Call ID: 8fd96163-89b1-4b54-bf78-68b30b0d787d
  Args:
    target: :Birgitte_Duchess_of_Gloucester
    relation: :hasMother
    source: :Rose_Windsor
  AddTriple (2abd17ab-9e77-4eee-aee3-b36f57d43086)
 Call ID: 2abd17ab-9e77-4eee-aee3-b36f57d43086
  Args:
    source: :Rose_Windsor
    target: :Prince_Richard_Duke_of_Gloucester
    relation: :isChildOf
  AddTriple (3d279c83-7cf4-412b-878e-db7240d06c65)
 Call ID: 3d279c83-7cf4-412b-878e-db7240d06c65
  Args:
    source: :Rose_Windsor
    relation: :isChildOf
    target: :Birgitte_Duchess_of_Gloucester
  AddTriple (2fa3f1de-5934-4b93-8c7f-4417a65cbb80)
 Call ID: 2fa3f1de-5934-4b93-8c7f-4417a65cbb80
  Args:
    target: :Rose_Windsor
    relation: :isParentOf
    source: :Prince_Richard_Duke_of_Gloucester
  AddTriple (7140030a-7dd9-46f9-a300-3b42fb0ff916)
 Call ID: 7140030a-7dd9-46f9-a300-3b42fb0ff916
  Args:
    source: :Birgitte_Duchess_of_Gloucester
    relation: :isParentOf
    target: :Rose_Windsor
  AddTriple (4e731e24-9242-4067-99a0-57029ac082d5)
 Call ID: 4e731e24-9242-4067-99a0-57029ac082d5
  Args:
    source: :Prince_Richard_Duke_of_Gloucester
    target: :Rose_Windsor
    relation: :hasChild
  AddTriple (c89535a6-59bb-4e37-b15b-c614904a1b14)
 Call ID: c89535a6-59bb-4e37-b15b-c614904a1b14
  Args:
    source: :Birgitte_Duchess_of_Gloucester
    target: :Rose_Windsor
    relation: :hasChild
  AddTriple (fe9852b9-638e-4b4f-98de-8a0d81b1acb7)
 Call ID: fe9852b9-638e-4b4f-98de-8a0d81b1acb7
  Args:
    relation: :hasChild
    target: :Lyla_Gilman
    source: :Rose_Windsor
  AddTriple (a97e4ecc-cc3c-4cc2-9cd4-48d02b565e75)
 Call ID: a97e4ecc-cc3c-4cc2-9cd4-48d02b565e75
  Args:
    source: :Rose_Windsor
    relation: :hasChild
    target: :Rufus_Gilman
  AddTriple (8a9bf5e1-2742-4db3-8a73-ea290512e361)
 Call ID: 8a9bf5e1-2742-4db3-8a73-ea290512e361
  Args:
    target: :Lyla_Gilman
    relation: :hasChild
    source: :George_Gilman
  AddTriple (75126c9f-7edf-4a96-b4cb-f2b3b8e3782d)
 Call ID: 75126c9f-7edf-4a96-b4cb-f2b3b8e3782d
  Args:
    relation: :hasChild
    target: :Rufus_Gilman
    source: :George_Gilman
  AddLiteral (d787a914-bd9d-4e4b-89fb-92cf4c1272eb)
 Call ID: d787a914-bd9d-4e4b-89fb-92cf4c1272eb
  Args:
    source: :Lyla_Gilman
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 2010
  AddLiteral (d2ca1076-8da2-48ce-9856-d8391935170d)
 Call ID: d2ca1076-8da2-48ce-9856-d8391935170d
  Args:
    source: :Rufus_Gilman
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 2012
  Finish (c6850832-631c-4c3a-b35f-265ec6822419)
 Call ID: c6850832-631c-4c3a-b35f-265ec6822419
  Args: