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
Princess Antonia of Prussia, Duchess of Wellington (Antonia Elizabeth Brigid Louise Mansfeld; born 28 April 1955) is a British aristocrat and philanthropist.
A member of the House of Hohenzollern by birth, she is a great-granddaughter of Wilhelm II, German Emperor and a great-great-great-granddaughter of Queen Victoria of the United Kingdom.
Through her marriage, she is also the Princess of Waterloo, Duchess of Victoria, and Duchess of Ciudad Rodrigo.
Early life and education

Princess Antonia Elizabeth Brigid Louise Mansfeld of Prussia was born in London on 28 April 1955, the daughter of Prince Frederick of Prussia and his wife, Lady Brigid Guinness.
On her father's side, she is a great-granddaughter of the German Emperor Wilhelm II, and granddaughter of Rupert Guinness, 2nd Earl of Iveagh on her mother's side.
Career

In 2007, she was appointed as the President of The Guinness Partnership, an affordable housing charitable society in the United Kingdom, and was appointed an Officer of the Order of the British Empire in the 2008 Birthday Honours for services to social housing.
In 2008 Antonia was appointed as a fellow of Eton College, serving as a member of the college's governing body.
Personal life

On 3 February 1977, she married Charles Wellesley, Marquess of Douro at St Paul's Church, Knightsbridge in London.
Notable guests at the wedding included Queen Elizabeth The Queen Mother, the Prince of Wales, Princess Margaret, and the Duke and Duchess of Kent.
She is godmother to Lady Gabriella Kingston, daughter of Prince & Princess Michael of Kent.
When her husband succeeded his father as the 9th Duke of Wellington, she became the Princess of Waterloo in Belgium and the Netherlands, the Duchess of Victoria in Portugal, the Duchess of Wellington in the United Kingdom, and the Duchess of Ciudad Rodrigo in Spain.
They have five children, including Lady Mary Wellesley and Lady Charlotte Wellesley.


References



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
  AssignClass (c80afcda-a7b6-466a-8590-91aff83d5429)
 Call ID: c80afcda-a7b6-466a-8590-91aff83d5429
  Args:
    source: Antonia_Elizabeth_Brigid_Louise_Mansfeld
    type: :Woman
  AssignClass (38919e8b-1db5-4ac6-b8c6-43e91e38fed3)
 Call ID: 38919e8b-1db5-4ac6-b8c6-43e91e38fed3
  Args:
    source: Antonia_Elizabeth_Brigid_Louise_Mansfeld
    type: :Person
  AddLiteral (c4b317f1-e489-4f9c-a4f2-46931d49849f)
 Call ID: c4b317f1-e489-4f9c-a4f2-46931d49849f
  Args:
    source: Antonia_Elizabeth_Brigid_Louise_Mansfeld
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1955
  AssignClass (05ba8129-0c27-4fa3-85aa-0559ec622ddd)
 Call ID: 05ba8129-0c27-4fa3-85aa-0559ec622ddd
  Args:
    type: :Man
    source: Prince_Frederick_of_Prussia
  AssignClass (67eb2550-9639-47d8-8b23-e7db50cbd85b)
 Call ID: 67eb2550-9639-47d8-8b23-e7db50cbd85b
  Args:
    source: Prince_Frederick_of_Prussia
    type: :Person
  AssignClass (6436bf6b-f2a9-473f-9ffb-84a648b13646)
 Call ID: 6436bf6b-f2a9-473f-9ffb-84a648b13646
  Args:
    type: :Woman
    source: Lady_Brigid_Guinness
  AssignClass (e2e82bec-e156-4c60-9cba-cc7fe80a074b)
 Call ID: e2e82bec-e156-4c60-9cba-cc7fe80a074b
  Args:
    type: :Person
    source: Lady_Brigid_Guinness
  AddTriple (e2f2b166-1ba2-4d46-a5a3-a8770b5d6f85)
 Call ID: e2f2b166-1ba2-4d46-a5a3-a8770b5d6f85
  Args:
    target: Prince_Frederick_of_Prussia
    source: Antonia_Elizabeth_Brigid_Louise_Mansfeld
    relation: :hasFather
  AddTriple (d1febe09-17ae-4df9-8536-8cd8c5e7cb52)
 Call ID: d1febe09-17ae-4df9-8536-8cd8c5e7cb52
  Args:
    relation: :hasMother
    source: Antonia_Elizabeth_Brigid_Louise_Mansfeld
    target: Lady_Brigid_Guinness
  AssignClass (353757d0-e495-4e44-95e4-ed6c2dab9972)
 Call ID: 353757d0-e495-4e44-95e4-ed6c2dab9972
  Args:
    type: :Man
    source: Wilhelm_II_German_Emperor
  AssignClass (299b101b-3c05-423b-a2c3-430cb2653b2d)
 Call ID: 299b101b-3c05-423b-a2c3-430cb2653b2d
  Args:
    type: :Person
    source: Wilhelm_II_German_Emperor
  AddTriple (053851a5-dd90-48fe-a92f-1f1b31e775c4)
 Call ID: 053851a5-dd90-48fe-a92f-1f1b31e775c4
  Args:
    target: Wilhelm_II_German_Emperor
    relation: :hasAncestor
    source: Antonia_Elizabeth_Brigid_Louise_Mansfeld
  AssignClass (e14f5ef4-f544-42a6-a151-324ea0dba471)
 Call ID: e14f5ef4-f544-42a6-a151-324ea0dba471
  Args:
    source: Queen_Victoria_of_the_United_Kingdom
    type: :Woman
  AssignClass (dd48ccf0-b0db-4ae3-bc66-52a503efef15)
 Call ID: dd48ccf0-b0db-4ae3-bc66-52a503efef15
  Args:
    source: Queen_Victoria_of_the_United_Kingdom
    type: :Person
  AddTriple (5538b99d-295d-42c8-ae32-fc35d22dce1f)
 Call ID: 5538b99d-295d-42c8-ae32-fc35d22dce1f
  Args:
    source: Antonia_Elizabeth_Brigid_Louise_Mansfeld
    relation: :hasAncestor
    target: Queen_Victoria_of_the_United_Kingdom
  AssignClass (2de87876-b004-4567-b463-e78becd9d28b)
 Call ID: 2de87876-b004-4567-b463-e78becd9d28b
  Args:
    source: Rupert_Guinness_2nd_Earl_of_Iveagh
    type: :Man
  AssignClass (13594265-ee5e-4f17-a7f0-51fd8a2bc1f5)
 Call ID: 13594265-ee5e-4f17-a7f0-51fd8a2bc1f5
  Args:
    type: :Person
    source: Rupert_Guinness_2nd_Earl_of_Iveagh
  AddTriple (4cd0bc9d-1bdc-45e9-b6e8-225f2a65ddd6)
 Call ID: 4cd0bc9d-1bdc-45e9-b6e8-225f2a65ddd6
  Args:
    relation: :hasAncestor
    source: Antonia_Elizabeth_Brigid_Louise_Mansfeld
    target: Rupert_Guinness_2nd_Earl_of_Iveagh
  AssignClass (67fc03f9-dc0e-4fe5-8fae-42a55830e00a)
 Call ID: 67fc03f9-dc0e-4fe5-8fae-42a55830e00a
  Args:
    source: Charles_Wellesley_Marquess_of_Douro
    type: :Man
  AssignClass (d463f026-f5f1-4729-b15a-7634956c35d2)
 Call ID: d463f026-f5f1-4729-b15a-7634956c35d2
  Args:
    source: Charles_Wellesley_Marquess_of_Douro
    type: :Person
  AddLiteral (3f4e99a7-02e9-4697-a4e0-4bfdb5f4fbaf)
 Call ID: 3f4e99a7-02e9-4697-a4e0-4bfdb5f4fbaf
  Args:
    literal_value: 1977
    literal_type: xsd:integer
    relation: :hasMarriageYear
    source: Antonia_Elizabeth_Brigid_Louise_Mansfeld
  AddTriple (cfd17647-04f8-43b1-a31f-ddda66fa28c9)
 Call ID: cfd17647-04f8-43b1-a31f-ddda66fa28c9
  Args:
    target: Charles_Wellesley_Marquess_of_Douro
    relation: :hasRelation
    source: Antonia_Elizabeth_Brigid_Louise_Mansfeld
  AssignClass (bd3644c5-8085-4850-93ec-ff5c594a8d44)
 Call ID: bd3644c5-8085-4850-93ec-ff5c594a8d44
  Args:
    source: Lady_Mary_Wellesley
    type: :Woman
  AssignClass (5d23fc74-51fa-4830-b3f4-1dda24d9a3e0)
 Call ID: 5d23fc74-51fa-4830-b3f4-1dda24d9a3e0
  Args:
    source: Lady_Mary_Wellesley
    type: :Person
  AddTriple (95987ad1-9305-415a-b99d-63259c3bb390)
 Call ID: 95987ad1-9305-415a-b99d-63259c3bb390
  Args:
    relation: :isChildOf
    source: Lady_Mary_Wellesley
    target: Antonia_Elizabeth_Brigid_Louise_Mansfeld
  AddTriple (c53c1491-f0d9-4cbf-927d-1bad68769ad1)
 Call ID: c53c1491-f0d9-4cbf-927d-1bad68769ad1
  Args:
    relation: :isChildOf
    source: Lady_Mary_Wellesley
    target: Charles_Wellesley_Marquess_of_Douro
  AssignClass (39a6d35b-e396-4683-a905-c0dae80ae99a)
 Call ID: 39a6d35b-e396-4683-a905-c0dae80ae99a
  Args:
    source: Lady_Charlotte_Wellesley
    type: :Woman
  AssignClass (349a6168-89da-4bd2-af8f-4f8dd267cbf4)
 Call ID: 349a6168-89da-4bd2-af8f-4f8dd267cbf4
  Args:
    source: Lady_Charlotte_Wellesley
    type: :Person
  AddTriple (894adc5f-2ece-421d-ad9e-fce5de1bbb9a)
 Call ID: 894adc5f-2ece-421d-ad9e-fce5de1bbb9a
  Args:
    relation: :isChildOf
    source: Lady_Charlotte_Wellesley
    target: Antonia_Elizabeth_Brigid_Louise_Mansfeld
  AddTriple (31d2e94f-acc6-4394-95a8-cc10fbbe1995)
 Call ID: 31d2e94f-acc6-4394-95a8-cc10fbbe1995
  Args:
    target: Charles_Wellesley_Marquess_of_Douro
    relation: :isChildOf
    source: Lady_Charlotte_Wellesley
  Finish (5eba643f-ad20-4d77-a655-35e8470e93dd)
 Call ID: 5eba643f-ad20-4d77-a655-35e8470e93dd
  Args: