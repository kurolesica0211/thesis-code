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
Princess Françoise d'Orléans (Françoise Isabelle Louise Marie; 25 December 1902 - 25 February 1953) was born an Orléans Princess of France and became a Princess of Greece and Denmark by marriage.
She was thus a member of the Greek royal family and a descendant of the "Citizen-King" Louis Philippe I.


Life

Françoise d'Orléans was born in Paris, the second daughter of Jean d'Orléans, duc de Guise (an Orléanist pretender to the throne of France under the name Jean III) and his wife, the French Princess Isabelle of Orléans.
Françoise's brother, Prince Henri, Count of Paris, succeeded their father as the Orleanist pretender, under the name Henri VI.
In Palermo on 11 February 1929, she married Prince Christopher of Greece and Denmark (1888–1940).
This was Christopher's second marriage - he was the youngest son of King George I of Greece (1845–1913) and his wife, Grand Duchess Olga Constantinovna of Russia (1851–1926).
Through his father, he was thus a grandson of King Christian IX of Denmark (1818–1906), nicknamed "the father-in-law of Europe" due to his six children all marrying into other royal families.
They had only one child, the writer Prince Michael of Greece and Denmark (1939–2024), whose marriage to the Greek artist Marina Karella (born 1940) did not conform to the laws of the royal house and thus deprived him of all right of succession to the Greek throne.
She is grandmother of Princess Alexandra of Greece, an artist, art collector, arts patron, and child life specialist.
Her other grand-daughter is Princess Olga of Greece, who married Prince Aimone of Savoy-Aosta, one of two claimants to be Head of the House of Savoy.
The civil war in Greece was preventing her from entering, and the British government refused to grant her asylum.
Françoise and her son Michael went to Paris, where they lived in the home of Princess Isabella and her second husband, Prince Pierre Murat.
Françoise did not want to see anyone in their residence and rarely left her rooms.
She is buried alongside her husband in Tatoi Royal Cemetery, Greece.



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
  AssignClass (901dddbd-8bcf-4425-b48a-7d2acca5b2d5)
 Call ID: 901dddbd-8bcf-4425-b48a-7d2acca5b2d5
  Args:
    type: :Woman
    source: Françoise_dOrleans
  AssignClass (452f0eab-93d6-4a92-a0d1-4e0155a50784)
 Call ID: 452f0eab-93d6-4a92-a0d1-4e0155a50784
  Args:
    type: :Person
    source: Françoise_dOrleans
  AddLiteral (f4838c09-f6c2-4485-9c79-e7322374cf13)
 Call ID: f4838c09-f6c2-4485-9c79-e7322374cf13
  Args:
    source: Françoise_dOrleans
    relation: :hasBirthYear
    literal_value: 1902
    literal_type: xsd:integer
  AddLiteral (db338186-a14a-49f7-abb9-9f0714745cff)
 Call ID: db338186-a14a-49f7-abb9-9f0714745cff
  Args:
    source: Françoise_dOrleans
    relation: :hasDeathYear
    literal_value: 1953
    literal_type: xsd:integer
  AssignClass (0e804a29-e1b6-4957-9f73-15868a555c06)
 Call ID: 0e804a29-e1b6-4957-9f73-15868a555c06
  Args:
    type: :Man
    source: Jean_dOrleans_duc_de_Guise
  AssignClass (763c9ba4-615a-4de2-b371-fbe0fb4938a5)
 Call ID: 763c9ba4-615a-4de2-b371-fbe0fb4938a5
  Args:
    type: :Person
    source: Jean_dOrleans_duc_de_Guise
  AssignClass (eab06aab-356e-4599-9b3a-91aacb5fe1db)
 Call ID: eab06aab-356e-4599-9b3a-91aacb5fe1db
  Args:
    type: :Woman
    source: Isabelle_of_Orleans
  AssignClass (58e94aca-15fd-44b4-90e9-36d722460559)
 Call ID: 58e94aca-15fd-44b4-90e9-36d722460559
  Args:
    type: :Person
    source: Isabelle_of_Orleans
  AddTriple (911366e4-7cea-4af5-a86c-6e133ebbf5d6)
 Call ID: 911366e4-7cea-4af5-a86c-6e133ebbf5d6
  Args:
    relation: :isFatherOf
    target: Françoise_dOrleans
    source: Jean_dOrleans_duc_de_Guise
  AddTriple (9722582b-3323-40bd-adc5-e1b7ba86efbe)
 Call ID: 9722582b-3323-40bd-adc5-e1b7ba86efbe
  Args:
    source: Isabelle_of_Orleans
    target: Françoise_dOrleans
    relation: :isMotherOf
  AssignClass (404feb6c-60f9-40dd-8d12-5625b0885c58)
 Call ID: 404feb6c-60f9-40dd-8d12-5625b0885c58
  Args:
    type: :Man
    source: Prince_Henri_Count_of_Paris
  AssignClass (947a74c9-c7dc-4b0c-aa4b-9c520e3fe09e)
 Call ID: 947a74c9-c7dc-4b0c-aa4b-9c520e3fe09e
  Args:
    source: Prince_Henri_Count_of_Paris
    type: :Person
  AddTriple (81ce310e-6f59-4a20-a442-040110703382)
 Call ID: 81ce310e-6f59-4a20-a442-040110703382
  Args:
    source: Prince_Henri_Count_of_Paris
    target: Françoise_dOrleans
    relation: :isBrotherOf
  AssignClass (cc0df8f3-f9cf-4f20-8012-a2f0d24e08c4)
 Call ID: cc0df8f3-f9cf-4f20-8012-a2f0d24e08c4
  Args:
    source: Prince_Christopher_of_Greece_and_Denmark
    type: :Man
  AssignClass (918216f7-d449-49b3-997f-a9064bbb259b)
 Call ID: 918216f7-d449-49b3-997f-a9064bbb259b
  Args:
    source: Prince_Christopher_of_Greece_and_Denmark
    type: :Person
  AddLiteral (488a9e26-8ac9-4b89-b478-253ab3e0388c)
 Call ID: 488a9e26-8ac9-4b89-b478-253ab3e0388c
  Args:
    literal_type: xsd:integer
    literal_value: 1929
    relation: :hasMarriageYear
    source: Françoise_dOrleans
  AddTriple (34a19a0f-d098-4b33-ada4-8e01816e57a1)
 Call ID: 34a19a0f-d098-4b33-ada4-8e01816e57a1
  Args:
    source: Françoise_dOrleans
    target: Prince_Christopher_of_Greece_and_Denmark
    relation: :hasRelation
  AssignClass (d159b830-51bc-4100-9ad3-c1250a49aef5)
 Call ID: d159b830-51bc-4100-9ad3-c1250a49aef5
  Args:
    type: :Man
    source: King_George_I_of_Greece
  AssignClass (fd571182-bc73-428a-b0e9-17cf0ee222fa)
 Call ID: fd571182-bc73-428a-b0e9-17cf0ee222fa
  Args:
    type: :Person
    source: King_George_I_of_Greece
  AssignClass (9a53903e-6015-428a-81ae-16a97c006393)
 Call ID: 9a53903e-6015-428a-81ae-16a97c006393
  Args:
    source: Grand_Duchess_Olga_Constantinovna_of_Russia
    type: :Woman
  AssignClass (90907a10-93f4-47ab-a4a2-973e64f87fad)
 Call ID: 90907a10-93f4-47ab-a4a2-973e64f87fad
  Args:
    source: Grand_Duchess_Olga_Constantinovna_of_Russia
    type: :Person
  AddTriple (be1c8c0f-f355-4d25-945b-b3f2e2f2faf4)
 Call ID: be1c8c0f-f355-4d25-945b-b3f2e2f2faf4
  Args:
    relation: :isFatherOf
    target: Prince_Christopher_of_Greece_and_Denmark
    source: King_George_I_of_Greece
  AddTriple (b639cfec-623b-4932-9260-d4be763cfe72)
 Call ID: b639cfec-623b-4932-9260-d4be763cfe72
  Args:
    relation: :isMotherOf
    target: Prince_Christopher_of_Greece_and_Denmark
    source: Grand_Duchess_Olga_Constantinovna_of_Russia
  AssignClass (d17b4139-5233-4306-a3f4-3ce1680eec36)
 Call ID: d17b4139-5233-4306-a3f4-3ce1680eec36
  Args:
    source: King_Christian_IX_of_Denmark
    type: :Man
  AssignClass (48f28710-a476-455f-b2b9-b24b01cd1d6a)
 Call ID: 48f28710-a476-455f-b2b9-b24b01cd1d6a
  Args:
    source: King_Christian_IX_of_Denmark
    type: :Person
  AddTriple (79130194-063e-4a90-b06b-a4de61e49d6b)
 Call ID: 79130194-063e-4a90-b06b-a4de61e49d6b
  Args:
    relation: :isFatherOf
    source: King_Christian_IX_of_Denmark
    target: King_George_I_of_Greece
  AssignClass (35ff6f61-a4fa-4d2f-bfa0-40be60499e39)
 Call ID: 35ff6f61-a4fa-4d2f-bfa0-40be60499e39
  Args:
    type: :Man
    source: Prince_Michael_of_Greece_and_Denmark
  AssignClass (c0bcab9d-3e4c-423a-aa29-b6a894db938f)
 Call ID: c0bcab9d-3e4c-423a-aa29-b6a894db938f
  Args:
    source: Prince_Michael_of_Greece_and_Denmark
    type: :Person
  AddTriple (a0b57aba-4f19-4279-a135-9059facb8758)
 Call ID: a0b57aba-4f19-4279-a135-9059facb8758
  Args:
    target: Prince_Michael_of_Greece_and_Denmark
    source: Prince_Christopher_of_Greece_and_Denmark
    relation: :isFatherOf
  AddTriple (6674c3a8-4702-46fe-a45b-d1b6329704b7)
 Call ID: 6674c3a8-4702-46fe-a45b-d1b6329704b7
  Args:
    relation: :isMotherOf
    source: Françoise_dOrleans
    target: Prince_Michael_of_Greece_and_Denmark
  AssignClass (82f24961-86fa-464c-a831-b87c453b38e6)
 Call ID: 82f24961-86fa-464c-a831-b87c453b38e6
  Args:
    type: :Woman
    source: Marina_Karella
  AssignClass (e38aa184-f50d-40a7-808d-8aa7492166ba)
 Call ID: e38aa184-f50d-40a7-808d-8aa7492166ba
  Args:
    type: :Person
    source: Marina_Karella
  AddTriple (4853b666-ec00-4e6b-8d81-c7d65d7b38c3)
 Call ID: 4853b666-ec00-4e6b-8d81-c7d65d7b38c3
  Args:
    target: Marina_Karella
    source: Prince_Michael_of_Greece_and_Denmark
    relation: :hasRelation
  AssignClass (d605773d-c7c8-4a4b-a392-8391307d7df1)
 Call ID: d605773d-c7c8-4a4b-a392-8391307d7df1
  Args:
    source: Princess_Alexandra_of_Greece
    type: :Woman
  AssignClass (0c6443c9-834b-4a9d-ae90-a9d498a0ea9f)
 Call ID: 0c6443c9-834b-4a9d-ae90-a9d498a0ea9f
  Args:
    source: Princess_Alexandra_of_Greece
    type: :Person
  AssignClass (093849fc-fa17-4ddd-8832-aadfe613834a)
 Call ID: 093849fc-fa17-4ddd-8832-aadfe613834a
  Args:
    source: Princess_Olga_of_Greece
    type: :Woman
  AssignClass (ca81bc57-b0c3-4eb9-af77-74c7bd130678)
 Call ID: ca81bc57-b0c3-4eb9-af77-74c7bd130678
  Args:
    type: :Person
    source: Princess_Olga_of_Greece
  AddTriple (4074807f-6122-438c-9b17-1294ecdf41d9)
 Call ID: 4074807f-6122-438c-9b17-1294ecdf41d9
  Args:
    source: Françoise_dOrleans
    target: Princess_Alexandra_of_Greece
    relation: :isMotherOf
  AddTriple (95dd062f-9b9e-4463-96b0-72ae72ed35d5)
 Call ID: 95dd062f-9b9e-4463-96b0-72ae72ed35d5
  Args:
    relation: :isMotherOf
    source: Françoise_dOrleans
    target: Princess_Olga_of_Greece
  AssignClass (9913fa27-5a28-460b-bc3a-2d73cb2f4f6d)
 Call ID: 9913fa27-5a28-460b-bc3a-2d73cb2f4f6d
  Args:
    source: Prince_Aimone_of_Savoy_Aosta
    type: :Man
  AssignClass (c87d564d-2c9c-4671-8727-79bb923dd83c)
 Call ID: c87d564d-2c9c-4671-8727-79bb923dd83c
  Args:
    type: :Person
    source: Prince_Aimone_of_Savoy_Aosta
  AddTriple (1df4835f-f264-4ce7-8132-5d5fdb9f85e0)
 Call ID: 1df4835f-f264-4ce7-8132-5d5fdb9f85e0
  Args:
    relation: :hasRelation
    target: Prince_Aimone_of_Savoy_Aosta
    source: Princess_Olga_of_Greece
  AssignClass (8a5c13d0-48d8-49b5-9bd2-4279c6f89cda)
 Call ID: 8a5c13d0-48d8-49b5-9bd2-4279c6f89cda
  Args:
    source: Princess_Isabella
    type: :Woman
  AssignClass (0910db90-34af-40ea-8e74-a9d3f85c13d3)
 Call ID: 0910db90-34af-40ea-8e74-a9d3f85c13d3
  Args:
    type: :Person
    source: Princess_Isabella
  AssignClass (a68dd79c-3cf6-47d4-a06a-842f2134922c)
 Call ID: a68dd79c-3cf6-47d4-a06a-842f2134922c
  Args:
    type: :Man
    source: Prince_Pierre_Murat
  AssignClass (594a762f-12b4-4a4c-b049-4b85d5c2a26e)
 Call ID: 594a762f-12b4-4a4c-b049-4b85d5c2a26e
  Args:
    source: Prince_Pierre_Murat
    type: :Person
  AddTriple (ccdde1b8-a140-4618-b714-c951c1e12a5a)
 Call ID: ccdde1b8-a140-4618-b714-c951c1e12a5a
  Args:
    target: Prince_Pierre_Murat
    source: Princess_Isabella
    relation: :hasRelation
  Finish (43775f86-bedf-4ff7-98c4-e4bb56bf17e5)
 Call ID: 43775f86-bedf-4ff7-98c4-e4bb56bf17e5
  Args: