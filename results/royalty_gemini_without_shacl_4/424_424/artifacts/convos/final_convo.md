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
  AssignClass (1fd910ee-ba55-4a5d-b896-012410a98344)
 Call ID: 1fd910ee-ba55-4a5d-b896-012410a98344
  Args:
    source: Antonia_of_Prussia
    type: :Woman
  AssignClass (44c206ce-53e3-4819-8f12-d50a73e0e796)
 Call ID: 44c206ce-53e3-4819-8f12-d50a73e0e796
  Args:
    type: :Person
    source: Antonia_of_Prussia
  AddLiteral (1d5f4eeb-b540-4eaa-8a9d-71a6f4e99fda)
 Call ID: 1d5f4eeb-b540-4eaa-8a9d-71a6f4e99fda
  Args:
    source: Antonia_of_Prussia
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1955
  AssignClass (89adbcad-1436-4a1c-a75b-0ecfd88c6596)
 Call ID: 89adbcad-1436-4a1c-a75b-0ecfd88c6596
  Args:
    source: Prince_Frederick_of_Prussia
    type: :Man
  AssignClass (6d493086-bb69-4aae-a6b5-395faf9e3f24)
 Call ID: 6d493086-bb69-4aae-a6b5-395faf9e3f24
  Args:
    type: :Person
    source: Prince_Frederick_of_Prussia
  AssignClass (022f8c89-1755-48cc-8fbc-e6676c976faa)
 Call ID: 022f8c89-1755-48cc-8fbc-e6676c976faa
  Args:
    type: :Woman
    source: Lady_Brigid_Guinness
  AssignClass (1fe1cc94-3f05-4a14-a993-7648fe73ec2a)
 Call ID: 1fe1cc94-3f05-4a14-a993-7648fe73ec2a
  Args:
    source: Lady_Brigid_Guinness
    type: :Person
  AddTriple (42f72b22-ca99-43fd-b0a9-1552ee177758)
 Call ID: 42f72b22-ca99-43fd-b0a9-1552ee177758
  Args:
    target: Prince_Frederick_of_Prussia
    source: Antonia_of_Prussia
    relation: :hasFather
  AddTriple (5ef98fe1-07d4-4d67-8eb5-6e1af575ae4c)
 Call ID: 5ef98fe1-07d4-4d67-8eb5-6e1af575ae4c
  Args:
    target: Lady_Brigid_Guinness
    source: Antonia_of_Prussia
    relation: :hasMother
  AssignClass (1d544f43-5542-44b7-9fa9-3e7291c2ee18)
 Call ID: 1d544f43-5542-44b7-9fa9-3e7291c2ee18
  Args:
    type: :Man
    source: Wilhelm_II
  AssignClass (00608252-d642-4212-9ef9-90f163875f06)
 Call ID: 00608252-d642-4212-9ef9-90f163875f06
  Args:
    source: Wilhelm_II
    type: :Person
  AddTriple (a5663590-0e75-43c2-8e2d-28530952d515)
 Call ID: a5663590-0e75-43c2-8e2d-28530952d515
  Args:
    relation: :hasAncestor
    source: Antonia_of_Prussia
    target: Wilhelm_II
  AssignClass (08cb11a8-e64b-493f-bab2-c34aac9874ab)
 Call ID: 08cb11a8-e64b-493f-bab2-c34aac9874ab
  Args:
    type: :Woman
    source: Queen_Victoria
  AssignClass (4e068285-144c-4fcb-963a-4f11c81adf6f)
 Call ID: 4e068285-144c-4fcb-963a-4f11c81adf6f
  Args:
    type: :Person
    source: Queen_Victoria
  AddTriple (ad3700d4-5c92-456b-b734-bb0852a71fca)
 Call ID: ad3700d4-5c92-456b-b734-bb0852a71fca
  Args:
    relation: :hasAncestor
    target: Queen_Victoria
    source: Antonia_of_Prussia
  AssignClass (97a67fe2-4f50-4b72-9c85-6cea7722ff33)
 Call ID: 97a67fe2-4f50-4b72-9c85-6cea7722ff33
  Args:
    source: Rupert_Guinness_2nd_Earl_of_Iveagh
    type: :Man
  AssignClass (6ab68957-cf24-4c3f-9014-8df84c5a77d5)
 Call ID: 6ab68957-cf24-4c3f-9014-8df84c5a77d5
  Args:
    type: :Person
    source: Rupert_Guinness_2nd_Earl_of_Iveagh
  AddTriple (48d6dd9d-33b6-4b6f-8737-6a7322f32623)
 Call ID: 48d6dd9d-33b6-4b6f-8737-6a7322f32623
  Args:
    target: Rupert_Guinness_2nd_Earl_of_Iveagh
    source: Antonia_of_Prussia
    relation: :hasAncestor
  AssignClass (a5660a1c-3705-45ca-8d51-3ed78f7a979e)
 Call ID: a5660a1c-3705-45ca-8d51-3ed78f7a979e
  Args:
    source: Charles_Wellesley_Marquess_of_Douro
    type: :Man
  AssignClass (92a8c14c-7d9e-4669-97fe-4ca215237607)
 Call ID: 92a8c14c-7d9e-4669-97fe-4ca215237607
  Args:
    source: Charles_Wellesley_Marquess_of_Douro
    type: :Person
  AddLiteral (89d01477-bc09-4d3a-9e52-7ca0f3f5e60c)
 Call ID: 89d01477-bc09-4d3a-9e52-7ca0f3f5e60c
  Args:
    source: Antonia_of_Prussia
    relation: :hasMarriageYear
    literal_type: xsd:integer
    literal_value: 1977
  AddTriple (e0a04d65-e984-4ae9-8c65-bca25a73e055)
 Call ID: e0a04d65-e984-4ae9-8c65-bca25a73e055
  Args:
    source: Antonia_of_Prussia
    target: Charles_Wellesley_Marquess_of_Douro
    relation: :hasRelation
  AssignClass (29c78f0a-da2d-4292-89f6-1b0835a715d9)
 Call ID: 29c78f0a-da2d-4292-89f6-1b0835a715d9
  Args:
    source: Lady_Mary_Wellesley
    type: :Woman
  AssignClass (e7ea83f4-c5f4-48de-891d-104cc4feb1d5)
 Call ID: e7ea83f4-c5f4-48de-891d-104cc4feb1d5
  Args:
    source: Lady_Mary_Wellesley
    type: :Person
  AddTriple (0835a325-73ac-421e-ad91-88121cbadbb9)
 Call ID: 0835a325-73ac-421e-ad91-88121cbadbb9
  Args:
    target: Lady_Mary_Wellesley
    source: Antonia_of_Prussia
    relation: :hasChild
  AssignClass (1a4cf335-5624-4925-8cf7-3a68ec7b3a7a)
 Call ID: 1a4cf335-5624-4925-8cf7-3a68ec7b3a7a
  Args:
    type: :Woman
    source: Lady_Charlotte_Wellesley
  AssignClass (887ff223-3b1c-4b2b-95ae-afff178b04eb)
 Call ID: 887ff223-3b1c-4b2b-95ae-afff178b04eb
  Args:
    source: Lady_Charlotte_Wellesley
    type: :Person
  AddTriple (9584e24d-0cf5-452c-89b7-6b81761674ae)
 Call ID: 9584e24d-0cf5-452c-89b7-6b81761674ae
  Args:
    target: Lady_Charlotte_Wellesley
    source: Antonia_of_Prussia
    relation: :hasChild
  Finish (51f0e943-17d7-4177-9136-d085d2f603c9)
 Call ID: 51f0e943-17d7-4177-9136-d085d2f603c9
  Args: