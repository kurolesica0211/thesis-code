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
Princess María de las Mercedes of Bavaria, Infanta of Spain (3 October 1911 – 11 September 1953) was a German-Spanish princess.
She was the third wife of Georgian Prince Irakli Bagration of Mukhrani.
Through her father, Prince Ferdinand of Bavaria, she was a member of the Bavarian House of Wittelsbach.
Through her mother, Infanta María Teresa of Spain, she was a granddaughter of Alfonso XII and niece of Alfonso XIII.
Early life

Princess María de las Mercedes of Bavaria, Infanta of Spain, was born on 3 October 1911 at the Palace of the Cuesta de la Vega, Madrid, to Prince Ferdinand of Bavaria and Infanta María Teresa of Spain.
Her parents were first cousins, both grandchildren of Isabella II of Spain.
Prior to her birth, her uncle, King Alfonso XIII, declared that any children born of her parents' marriage would be Infantes or Infantas of Spain.
She was christened María de las Mercedes Teresa María de la
Her godparents were Infanta María de la Paz of Spain (her paternal grandmother) and Prince Adalbert of Bavaria (her paternal uncle, for whom Prince Carlos of Bourbon-Two Sicilies stood proxy).
She had two elder brothers, Luis Alfonso (1906–1983) and José Eugenio (1909–1966), and one younger sister, María del Pilar (1912–1918).
Marriage and issue

On 29 August 1946, Infanta María de las Mercedes married Prince Irakli Bagration of Mukhrani at the Miramar Palace in San Sebastián.
In 1948, Irakli's sister Leonida married Grand Duke Vladimir.



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
  AssignClass (539095ba-efd2-4dd0-b222-22d016680c5a)
 Call ID: 539095ba-efd2-4dd0-b222-22d016680c5a
  Args:
    source: :Maria_de_las_Mercedes_of_Bavaria
    type: :Person
  AssignClass (7bae2a2e-a3a3-46b0-b4c5-0ba606dbef90)
 Call ID: 7bae2a2e-a3a3-46b0-b4c5-0ba606dbef90
  Args:
    type: :Woman
    source: :Maria_de_las_Mercedes_of_Bavaria
  AssignClass (e092ba3f-87e5-4503-b82c-eb7bc10bc1f0)
 Call ID: e092ba3f-87e5-4503-b82c-eb7bc10bc1f0
  Args:
    type: :Person
    source: :Irakli_Bagration_of_Mukhrani
  AssignClass (1f4c5915-7833-44a6-904b-9270760de17c)
 Call ID: 1f4c5915-7833-44a6-904b-9270760de17c
  Args:
    source: :Irakli_Bagration_of_Mukhrani
    type: :Man
  AssignClass (96ce086f-b9b1-4783-9163-1b4a22446e9f)
 Call ID: 96ce086f-b9b1-4783-9163-1b4a22446e9f
  Args:
    type: :Person
    source: :Ferdinand_of_Bavaria
  AssignClass (a6fe7b22-98c9-484e-bd9a-ebaae41a95b5)
 Call ID: a6fe7b22-98c9-484e-bd9a-ebaae41a95b5
  Args:
    source: :Ferdinand_of_Bavaria
    type: :Man
  AssignClass (1c15f94d-2d0a-4766-88d5-5ead131d9274)
 Call ID: 1c15f94d-2d0a-4766-88d5-5ead131d9274
  Args:
    source: :Maria_Teresa_of_Spain
    type: :Person
  AssignClass (6c4f08ce-f03d-44d1-b239-402b21b91c4f)
 Call ID: 6c4f08ce-f03d-44d1-b239-402b21b91c4f
  Args:
    type: :Woman
    source: :Maria_Teresa_of_Spain
  AssignClass (e855f85d-66d4-41a6-b106-bf9b6ccfd824)
 Call ID: e855f85d-66d4-41a6-b106-bf9b6ccfd824
  Args:
    type: :Person
    source: :Alfonso_XII
  AssignClass (adaa02bb-d33a-491d-9875-39ffd5c89ead)
 Call ID: adaa02bb-d33a-491d-9875-39ffd5c89ead
  Args:
    type: :Man
    source: :Alfonso_XII
  AssignClass (9ffb5384-06f3-4c5b-b168-c6f6d7331e9b)
 Call ID: 9ffb5384-06f3-4c5b-b168-c6f6d7331e9b
  Args:
    type: :Person
    source: :Alfonso_XIII
  AssignClass (f28abf1a-4f79-4c27-84bf-268d1148c520)
 Call ID: f28abf1a-4f79-4c27-84bf-268d1148c520
  Args:
    source: :Alfonso_XIII
    type: :Man
  AssignClass (52f4c8c2-fb4d-460c-ae72-9aae7a66f3ad)
 Call ID: 52f4c8c2-fb4d-460c-ae72-9aae7a66f3ad
  Args:
    type: :Person
    source: :Isabella_II_of_Spain
  AssignClass (f88f2e16-10b7-43dc-8ae5-cd5d4c36bb2f)
 Call ID: f88f2e16-10b7-43dc-8ae5-cd5d4c36bb2f
  Args:
    source: :Isabella_II_of_Spain
    type: :Woman
  AssignClass (0d348838-b0fa-4332-99e4-465242bb4c56)
 Call ID: 0d348838-b0fa-4332-99e4-465242bb4c56
  Args:
    type: :Person
    source: :Maria_de_la_Paz_of_Spain
  AssignClass (606d2b39-79ba-42df-9efd-0bba9a4d86ff)
 Call ID: 606d2b39-79ba-42df-9efd-0bba9a4d86ff
  Args:
    type: :Woman
    source: :Maria_de_la_Paz_of_Spain
  AssignClass (f9db86d5-bffa-40ad-b676-cd3dcd4dc5ac)
 Call ID: f9db86d5-bffa-40ad-b676-cd3dcd4dc5ac
  Args:
    source: :Adalbert_of_Bavaria
    type: :Person
  AssignClass (2761b090-c2b8-43f7-87a7-430c1773bfd7)
 Call ID: 2761b090-c2b8-43f7-87a7-430c1773bfd7
  Args:
    type: :Man
    source: :Adalbert_of_Bavaria
  AssignClass (1e4d999b-952b-43da-9242-c982bf7a42e3)
 Call ID: 1e4d999b-952b-43da-9242-c982bf7a42e3
  Args:
    type: :Person
    source: :Carlos_of_Bourbon-Two_Sicilies
  AssignClass (2306af7c-117e-440b-a3f6-886b33d78136)
 Call ID: 2306af7c-117e-440b-a3f6-886b33d78136
  Args:
    type: :Man
    source: :Carlos_of_Bourbon-Two_Sicilies
  AssignClass (64337568-6eab-44b7-86ec-599d8c0fcf5f)
 Call ID: 64337568-6eab-44b7-86ec-599d8c0fcf5f
  Args:
    source: :Luis_Alfonso
    type: :Person
  AssignClass (4809bc4c-7086-4144-9cad-8e283dcf65c3)
 Call ID: 4809bc4c-7086-4144-9cad-8e283dcf65c3
  Args:
    type: :Man
    source: :Luis_Alfonso
  AssignClass (d40669d2-e9f8-4550-8556-d51c48608b7c)
 Call ID: d40669d2-e9f8-4550-8556-d51c48608b7c
  Args:
    source: :Jose_Eugenio
    type: :Person
  AssignClass (f100b6e6-3216-4a34-af24-48f27fa7e1ec)
 Call ID: f100b6e6-3216-4a34-af24-48f27fa7e1ec
  Args:
    source: :Jose_Eugenio
    type: :Man
  AssignClass (d0a66a5e-c631-4cb7-93dc-bbbceb9d160a)
 Call ID: d0a66a5e-c631-4cb7-93dc-bbbceb9d160a
  Args:
    type: :Person
    source: :Maria_del_Pilar
  AssignClass (9cbd34a2-f25f-4369-bf5a-f7ddf17ef79e)
 Call ID: 9cbd34a2-f25f-4369-bf5a-f7ddf17ef79e
  Args:
    source: :Maria_del_Pilar
    type: :Woman
  AssignClass (43a2a8e5-2ec2-40d0-8237-48dcbc28f11c)
 Call ID: 43a2a8e5-2ec2-40d0-8237-48dcbc28f11c
  Args:
    type: :Person
    source: :Leonida_Bagration
  AssignClass (2b4256af-5249-4b68-96f3-9d1225a92290)
 Call ID: 2b4256af-5249-4b68-96f3-9d1225a92290
  Args:
    source: :Leonida_Bagration
    type: :Woman
  AssignClass (54bedf66-3992-4133-8a85-cb7a12781bc9)
 Call ID: 54bedf66-3992-4133-8a85-cb7a12781bc9
  Args:
    type: :Person
    source: :Vladimir
  AssignClass (33ce6ba0-95f4-402c-a4f4-1921c8e0aaa1)
 Call ID: 33ce6ba0-95f4-402c-a4f4-1921c8e0aaa1
  Args:
    type: :Man
    source: :Vladimir
  AddLiteral (ce88743a-1152-4caf-af8e-cf0f93e38e25)
 Call ID: ce88743a-1152-4caf-af8e-cf0f93e38e25
  Args:
    literal_type: xsd:integer
    source: :Maria_de_las_Mercedes_of_Bavaria
    literal_value: 1911
    relation: :hasBirthYear
  AddLiteral (b792fb93-f7dc-45d6-badb-f4fe8e8a5495)
 Call ID: b792fb93-f7dc-45d6-badb-f4fe8e8a5495
  Args:
    source: :Maria_de_las_Mercedes_of_Bavaria
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1953
  AddLiteral (0c662c9d-32d5-4b10-b9a4-ae411f593cc7)
 Call ID: 0c662c9d-32d5-4b10-b9a4-ae411f593cc7
  Args:
    literal_type: xsd:integer
    source: :Maria_de_las_Mercedes_of_Bavaria
    literal_value: 1946
    relation: :hasMarriageYear
  AddLiteral (06cb037f-89e0-440a-8acd-66e965934fa9)
 Call ID: 06cb037f-89e0-440a-8acd-66e965934fa9
  Args:
    source: :Luis_Alfonso
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1906
  AddLiteral (1e4535a3-0094-4663-a582-825e40c8dda6)
 Call ID: 1e4535a3-0094-4663-a582-825e40c8dda6
  Args:
    source: :Luis_Alfonso
    literal_type: xsd:integer
    literal_value: 1983
    relation: :hasDeathYear
  AddLiteral (70b6ff0f-aacb-49f1-b0cc-bb7db8663ca9)
 Call ID: 70b6ff0f-aacb-49f1-b0cc-bb7db8663ca9
  Args:
    source: :Jose_Eugenio
    literal_type: xsd:integer
    literal_value: 1909
    relation: :hasBirthYear
  AddLiteral (af131bd5-d6b0-45f2-98f9-54923337972d)
 Call ID: af131bd5-d6b0-45f2-98f9-54923337972d
  Args:
    literal_value: 1966
    relation: :hasDeathYear
    source: :Jose_Eugenio
    literal_type: xsd:integer
  AddLiteral (13d6ddf0-2741-4df8-81e8-57ba379c547f)
 Call ID: 13d6ddf0-2741-4df8-81e8-57ba379c547f
  Args:
    literal_value: 1912
    relation: :hasBirthYear
    source: :Maria_del_Pilar
    literal_type: xsd:integer
  AddLiteral (bab51734-0d60-4c47-ba40-3cece42879fa)
 Call ID: bab51734-0d60-4c47-ba40-3cece42879fa
  Args:
    source: :Maria_del_Pilar
    literal_type: xsd:integer
    literal_value: 1918
    relation: :hasDeathYear
  AddTriple (dd57f5fa-6b92-47d4-9b6a-1b4dad9bfa5e)
 Call ID: dd57f5fa-6b92-47d4-9b6a-1b4dad9bfa5e
  Args:
    target: :Ferdinand_of_Bavaria
    relation: :hasFather
    source: :Maria_de_las_Mercedes_of_Bavaria
  AddTriple (1efd92fb-be6d-43a4-a066-ff554aeb8fe6)
 Call ID: 1efd92fb-be6d-43a4-a066-ff554aeb8fe6
  Args:
    target: :Maria_Teresa_of_Spain
    relation: :hasMother
    source: :Maria_de_las_Mercedes_of_Bavaria
  AddTriple (ecdfc130-1c8f-4ca9-8acb-252f3d5ae4e2)
 Call ID: ecdfc130-1c8f-4ca9-8acb-252f3d5ae4e2
  Args:
    target: :Alfonso_XII
    relation: :hasFather
    source: :Maria_Teresa_of_Spain
  AddTriple (f15ab96f-f96c-4dd4-bcae-d114ea638c8d)
 Call ID: f15ab96f-f96c-4dd4-bcae-d114ea638c8d
  Args:
    relation: :hasMother
    target: :Maria_Teresa_of_Spain
    source: :Maria_de_las_Mercedes_of_Bavaria
  AddTriple (a0d06926-3eb0-4c1e-9519-253682dd32b6)
 Call ID: a0d06926-3eb0-4c1e-9519-253682dd32b6
  Args:
    source: :Ferdinand_of_Bavaria
    relation: :hasMother
    target: :Maria_de_la_Paz_of_Spain
  AddTriple (15b623b0-4740-478d-a35e-1640fa28a2fe)
 Call ID: 15b623b0-4740-478d-a35e-1640fa28a2fe
  Args:
    source: :Maria_de_las_Mercedes_of_Bavaria
    target: :Ferdinand_of_Bavaria
    relation: :hasFather
  AddTriple (c3506766-05ba-4c68-9426-2b74508b4b9a)
 Call ID: c3506766-05ba-4c68-9426-2b74508b4b9a
  Args:
    source: :Maria_de_las_Mercedes_of_Bavaria
    target: :Luis_Alfonso
    relation: :hasBrother
  AddTriple (9287cd88-3ed9-44ea-b2f1-f7fc5b262fb9)
 Call ID: 9287cd88-3ed9-44ea-b2f1-f7fc5b262fb9
  Args:
    source: :Maria_de_las_Mercedes_of_Bavaria
    target: :Jose_Eugenio
    relation: :hasBrother
  AddTriple (48b983e5-1b80-4a2f-96ed-f511db6cedc6)
 Call ID: 48b983e5-1b80-4a2f-96ed-f511db6cedc6
  Args:
    source: :Maria_de_las_Mercedes_of_Bavaria
    target: :Maria_del_Pilar
    relation: :hasSister
  AddTriple (7f50e601-0f04-4c1a-a710-94a5b9b05619)
 Call ID: 7f50e601-0f04-4c1a-a710-94a5b9b05619
  Args:
    source: :Irakli_Bagration_of_Mukhrani
    relation: :hasSister
    target: :Leonida_Bagration
  AddTriple (30b678ed-2398-428b-9952-a155517ab8ee)
 Call ID: 30b678ed-2398-428b-9952-a155517ab8ee
  Args:
    source: :Leonida_Bagration
    target: :Vladimir
    relation: :hasMarriageYear
  Finish (ba268137-e0c7-426f-8094-697f3429afff)
 Call ID: ba268137-e0c7-426f-8094-697f3429afff
  Args: