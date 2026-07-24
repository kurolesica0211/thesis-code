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
Princess Nuria


Princess Françoise


Princess Mariam


Princess Monique


Prince Don Bagrat de Bagration y de Baviera, also Prince Bagrat Bagrationi-Mukhraneli and Prince Bagrat Bagration-Moukhransky (12 January 1949 – 20 March 2017) was a member of the Bagration dynasty which once ruled the Kingdom of Georgia and a relative of the royal family of Spain.
Background

He was born in Madrid, Spain on 12 January 1949 and named Bagrat Juan María de Fátima de Todos los Santos, the third child of Prince Irakli Bagration-Mukhrani (1909-1977) by his third wife, Infanta Doña María de las Mercedes de Baviera y Borbón (1911-1953), a niece of King Alfonso XIII of Spain.
His maternal great-grandfather was King Alfonso XII.
Prince Jorge de Bagration, a Spanish race car driver and pretender to the throne of Georgia, was his elder half brother.
His mother had been born in Madrid, and although part of her youth was spent in exile in the Basses Pyrénées of France, Bagrat was raised, along with Jorge and his elder sister Princess Mariam (born 1947), by his widowed father in Madrid and at the Palacio de Santillana del Mar in Santander.
Marriage and issue

Bagrat married Doña María del Carmen de Ulloa y Suelves (b. 6 May 1953) on 12 November 1976 at San Jerónimo el
The couple were divorced on 16 September 2005, and Bagrat remarried in a civil ceremony to Mme.



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
  AssignClass (90e4ca57-55da-4620-a884-460ad712bcca)
 Call ID: 90e4ca57-55da-4620-a884-460ad712bcca
  Args:
    type: :Man
    source: Prince_Bagrat_de_Bagration_y_de_Baviera
  AssignClass (5a5161b6-b87f-4a91-9702-934f5780a161)
 Call ID: 5a5161b6-b87f-4a91-9702-934f5780a161
  Args:
    type: :Person
    source: Prince_Bagrat_de_Bagration_y_de_Baviera
  AddLiteral (2169e3a0-c345-4b0d-ad52-b8e9deaf9d4d)
 Call ID: 2169e3a0-c345-4b0d-ad52-b8e9deaf9d4d
  Args:
    literal_type: xsd:string
    source: Prince_Bagrat_de_Bagration_y_de_Baviera
    literal_value: Bagrat Juan María de Fátima de Todos los Santos
    relation: :knownAs
  AddLiteral (264b80da-afa1-43f6-83b5-20b643a9b07c)
 Call ID: 264b80da-afa1-43f6-83b5-20b643a9b07c
  Args:
    relation: :alsoKnownAs
    literal_type: xsd:string
    source: Prince_Bagrat_de_Bagration_y_de_Baviera
    literal_value: Prince Bagrat Bagrationi-Mukhraneli
  AddLiteral (1c4ee460-6222-4358-b226-e55d959e36ea)
 Call ID: 1c4ee460-6222-4358-b226-e55d959e36ea
  Args:
    source: Prince_Bagrat_de_Bagration_y_de_Baviera
    literal_value: Prince Bagrat Bagration-Moukhransky
    literal_type: xsd:string
    relation: :alsoKnownAs
  AddLiteral (ded10b37-681f-4a75-92c0-452587fc43dc)
 Call ID: ded10b37-681f-4a75-92c0-452587fc43dc
  Args:
    literal_type: xsd:positiveInteger
    source: Prince_Bagrat_de_Bagration_y_de_Baviera
    literal_value: 1949
    relation: :hasBirthYear
  AddLiteral (01028bb3-5aec-4aa0-aa38-bcbdd055cbf0)
 Call ID: 01028bb3-5aec-4aa0-aa38-bcbdd055cbf0
  Args:
    literal_type: xsd:positiveInteger
    source: Prince_Bagrat_de_Bagration_y_de_Baviera
    literal_value: 2017
    relation: :hasDeathYear
  AssignClass (f7fe4a05-8b15-4e95-ad39-efeaf4314865)
 Call ID: f7fe4a05-8b15-4e95-ad39-efeaf4314865
  Args:
    type: :Man
    source: Prince_Irakli_Bagration-Mukhrani
  AssignClass (c5e6ff5e-c59a-403c-906b-8240a89832bc)
 Call ID: c5e6ff5e-c59a-403c-906b-8240a89832bc
  Args:
    type: :Person
    source: Prince_Irakli_Bagration-Mukhrani
  AddLiteral (a40e9610-f660-4a51-b103-9fea5f9618f9)
 Call ID: a40e9610-f660-4a51-b103-9fea5f9618f9
  Args:
    relation: :hasBirthYear
    literal_value: 1909
    source: Prince_Irakli_Bagration-Mukhrani
    literal_type: xsd:positiveInteger
  AddLiteral (548ab6e3-73bd-4038-a7f7-6e4d9dc1dd2b)
 Call ID: 548ab6e3-73bd-4038-a7f7-6e4d9dc1dd2b
  Args:
    literal_value: 1977
    source: Prince_Irakli_Bagration-Mukhrani
    literal_type: xsd:positiveInteger
    relation: :hasDeathYear
  AssignClass (42f46d80-969e-48c1-97d0-8a61227921b7)
 Call ID: 42f46d80-969e-48c1-97d0-8a61227921b7
  Args:
    type: :Woman
    source: Infanta_Doña_María_de_las_Mercedes_de_Baviera_y_Borbón
  AssignClass (e3727e49-1d1a-4e18-87dc-b896cd229bf9)
 Call ID: e3727e49-1d1a-4e18-87dc-b896cd229bf9
  Args:
    type: :Person
    source: Infanta_Doña_María_de_las_Mercedes_de_Baviera_y_Borbón
  AddLiteral (a8c50740-6c87-447a-9e0c-78eb91472361)
 Call ID: a8c50740-6c87-447a-9e0c-78eb91472361
  Args:
    relation: :hasBirthYear
    literal_value: 1911
    source: Infanta_Doña_María_de_las_Mercedes_de_Baviera_y_Borbón
    literal_type: xsd:positiveInteger
  AddLiteral (35919b66-ada7-4497-a4cf-127e456e6ee9)
 Call ID: 35919b66-ada7-4497-a4cf-127e456e6ee9
  Args:
    relation: :hasDeathYear
    literal_value: 1953
    source: Infanta_Doña_María_de_las_Mercedes_de_Baviera_y_Borbón
    literal_type: xsd:positiveInteger
  AddTriple (14d94d36-4bae-4124-b242-f6b270da5f40)
 Call ID: 14d94d36-4bae-4124-b242-f6b270da5f40
  Args:
    target: Prince_Irakli_Bagration-Mukhrani
    source: Prince_Bagrat_de_Bagration_y_de_Baviera
    relation: :hasFather
  AddTriple (2868b561-5e65-480d-a6cd-3f36725c3ba4)
 Call ID: 2868b561-5e65-480d-a6cd-3f36725c3ba4
  Args:
    source: Prince_Bagrat_de_Bagration_y_de_Baviera
    target: Infanta_Doña_María_de_las_Mercedes_de_Baviera_y_Borbón
    relation: :hasMother
  AssignClass (039acf62-7862-40ae-8ff8-a9324e715724)
 Call ID: 039acf62-7862-40ae-8ff8-a9324e715724
  Args:
    type: :Man
    source: King_Alfonso_XIII_of_Spain
  AssignClass (563e07a5-c0f7-437c-81c4-4b60c0df80e6)
 Call ID: 563e07a5-c0f7-437c-81c4-4b60c0df80e6
  Args:
    type: :Person
    source: King_Alfonso_XIII_of_Spain
  AssignClass (2a4cb1ad-522d-4621-8cd9-03563051b95b)
 Call ID: 2a4cb1ad-522d-4621-8cd9-03563051b95b
  Args:
    type: :Man
    source: King_Alfonso_XII
  AssignClass (59cea425-a4f3-4bb0-85a8-5061a270773f)
 Call ID: 59cea425-a4f3-4bb0-85a8-5061a270773f
  Args:
    type: :Person
    source: King_Alfonso_XII
  AssignClass (fbfbcaf0-ee6d-4a9c-a42d-8b23ceb90c52)
 Call ID: fbfbcaf0-ee6d-4a9c-a42d-8b23ceb90c52
  Args:
    type: :Man
    source: Prince_Jorge_de_Bagration
  AssignClass (60ebe6be-062e-4a5d-ab53-a949e6daf93b)
 Call ID: 60ebe6be-062e-4a5d-ab53-a949e6daf93b
  Args:
    type: :Person
    source: Prince_Jorge_de_Bagration
  AddTriple (c5d39f87-af1c-4b6b-a44d-af4f85f84b55)
 Call ID: c5d39f87-af1c-4b6b-a44d-af4f85f84b55
  Args:
    relation: :isBrotherOf
    source: Prince_Jorge_de_Bagration
    target: Prince_Bagrat_de_Bagration_y_de_Baviera
  AssignClass (7dcd643a-5d4a-454d-953b-d3f60e5563eb)
 Call ID: 7dcd643a-5d4a-454d-953b-d3f60e5563eb
  Args:
    type: :Woman
    source: Princess_Mariam
  AssignClass (7afcac7f-343e-4a03-8de1-635e9b46cfd8)
 Call ID: 7afcac7f-343e-4a03-8de1-635e9b46cfd8
  Args:
    type: :Person
    source: Princess_Mariam
  AddTriple (06c59a99-3182-488d-bb95-71de24d50a92)
 Call ID: 06c59a99-3182-488d-bb95-71de24d50a92
  Args:
    relation: :isSisterOf
    target: Prince_Bagrat_de_Bagration_y_de_Baviera
    source: Princess_Mariam
  AssignClass (acdaa43c-0d9b-4cd2-849a-25a909f5f3d6)
 Call ID: acdaa43c-0d9b-4cd2-849a-25a909f5f3d6
  Args:
    type: :Woman
    source: Doña_María_del_Carmen_de_Ulloa_y_Suelves
  AssignClass (82dd2e3e-1bfc-4ec2-9512-a36e414efc4b)
 Call ID: 82dd2e3e-1bfc-4ec2-9512-a36e414efc4b
  Args:
    type: :Person
    source: Doña_María_del_Carmen_de_Ulloa_y_Suelves
  AddLiteral (9b4ba1c9-c71a-49aa-9e71-a169709d6819)
 Call ID: 9b4ba1c9-c71a-49aa-9e71-a169709d6819
  Args:
    literal_value: 1953
    source: Doña_María_del_Carmen_de_Ulloa_y_Suelves
    literal_type: xsd:positiveInteger
    relation: :hasBirthYear
  AddTriple (6e7ba291-6b51-46f6-bca8-12767ca7a337)
 Call ID: 6e7ba291-6b51-46f6-bca8-12767ca7a337
  Args:
    target: Doña_María_del_Carmen_de_Ulloa_y_Suelves
    source: Prince_Bagrat_de_Bagration_y_de_Baviera
    relation: :hasRelation
  AddLiteral (5a24cac7-c090-4a7c-885d-447472437951)
 Call ID: 5a24cac7-c090-4a7c-885d-447472437951
  Args:
    literal_type: xsd:positiveInteger
    source: Prince_Bagrat_de_Bagration_y_de_Baviera
    literal_value: 1976
    relation: :hasMarriageYear
  AssignClass (05184976-9b6b-4053-8b68-96f83d7fce4e)
 Call ID: 05184976-9b6b-4053-8b68-96f83d7fce4e
  Args:
    type: :Woman
    source: Princess_Nuria
  AssignClass (7f8ff763-2281-4a54-9d1f-5fd593448798)
 Call ID: 7f8ff763-2281-4a54-9d1f-5fd593448798
  Args:
    type: :Person
    source: Princess_Nuria
  AssignClass (df199068-410a-487a-b166-20588d5674f4)
 Call ID: df199068-410a-487a-b166-20588d5674f4
  Args:
    type: :Woman
    source: Princess_Françoise
  AssignClass (3e7d3c26-e22e-4f5d-b203-1877cc963723)
 Call ID: 3e7d3c26-e22e-4f5d-b203-1877cc963723
  Args:
    type: :Person
    source: Princess_Françoise
  AssignClass (585e953c-379e-4b90-a77d-ad425ca260f0)
 Call ID: 585e953c-379e-4b90-a77d-ad425ca260f0
  Args:
    type: :Woman
    source: Princess_Monique
  AssignClass (3504ec9b-b79d-4ab6-82dc-8599cd21480f)
 Call ID: 3504ec9b-b79d-4ab6-82dc-8599cd21480f
  Args:
    type: :Person
    source: Princess_Monique
  Finish (830efee7-ee36-48e1-922f-4ebd9ad8fb14)
 Call ID: 830efee7-ee36-48e1-922f-4ebd9ad8fb14
  Args: