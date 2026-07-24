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
Eleonore von Habsburg-Lothringen (Eleonore Maria del Pilar Iona Christina Jelena; born 28 February 1994) is an Austrian jewellery designer, gemologist, and model.
She is the daughter of Karl von Habsburg, the head of the House of Habsburg-Lorraine.
Early life and background

Eleonore Habsburg-Lorraine was born in 1994 in Salzburg to Karl von Habsburg, a politician and head of the House of Habsburg-Lorraine, and Francesca von Thyssen-Bornemisza de Kászon et Impérfalva, an art collector and by birth member of the Thyssen-Bornemisza family.
Her paternal grandparents were Otto, Crown Prince of Austria and Princess Regina of Saxe-Meiningen.
Her paternal great-grandparents Charles I of Austria and Zita of Bourbon-Parma were the last Emperor and Empress of Austria.
Her brother is racing car driver Ferdinand Habsburg.
Education and career

Habsburg-Lorraine attended boarding school in Gstaad before studying law at the European Business School London.
Habsburg has also worked as a fashion model, being featured in advertisement campaigns and walking the runway for Dolce & Gabbana.
Personal life

On 20 July 2020, Eleonore von Habsburg-Lorraine married Belgian race car driver Jérôme d'Ambrosio in a small civil ceremony at the Civil Registry of Monaco, conducted by the Mayor of Monaco Georges Marsan.
On 20 October 2021 she gave birth to a son, Otto d'Ambrosio, named after her grandfather Otto von Habsburg.



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
  AssignClass (7a31d216-a2da-4709-bcda-989f7fa78cdb)
 Call ID: 7a31d216-a2da-4709-bcda-989f7fa78cdb
  Args:
    type: :Woman
    source: Eleonore_von_Habsburg-Lothringen
  AssignClass (ca2a1d8c-e7f1-4b01-9c4d-24864ac15f35)
 Call ID: ca2a1d8c-e7f1-4b01-9c4d-24864ac15f35
  Args:
    type: :Person
    source: Eleonore_von_Habsburg-Lothringen
  AddLiteral (2c9e46d0-c693-4e07-a471-1fb35654be9f)
 Call ID: 2c9e46d0-c693-4e07-a471-1fb35654be9f
  Args:
    relation: :hasBirthYear
    literal_type: xsd:positiveInteger
    source: Eleonore_von_Habsburg-Lothringen
    literal_value: 1994
  AssignClass (9be6c02a-55a9-47c4-9184-f326d66d1799)
 Call ID: 9be6c02a-55a9-47c4-9184-f326d66d1799
  Args:
    source: Karl_von_Habsburg
    type: :Man
  AssignClass (3f5789e9-3d50-4def-ae92-291cf005c0f9)
 Call ID: 3f5789e9-3d50-4def-ae92-291cf005c0f9
  Args:
    type: :Person
    source: Karl_von_Habsburg
  AddTriple (a27d4eaa-43ee-4b62-8d90-e7b30744b120)
 Call ID: a27d4eaa-43ee-4b62-8d90-e7b30744b120
  Args:
    target: Karl_von_Habsburg
    relation: :hasFather
    source: Eleonore_von_Habsburg-Lothringen
  AssignClass (a3c8225e-84a0-44c9-aa2e-083e8a9dae6b)
 Call ID: a3c8225e-84a0-44c9-aa2e-083e8a9dae6b
  Args:
    type: :Woman
    source: Francesca_von_Thyssen-Bornemisza
  AssignClass (b39b187e-c71a-4cfb-a16d-0623ed741f07)
 Call ID: b39b187e-c71a-4cfb-a16d-0623ed741f07
  Args:
    source: Francesca_von_Thyssen-Bornemisza
    type: :Person
  AddTriple (3cfb8f74-46d8-49ab-acf3-25c090dcb7b5)
 Call ID: 3cfb8f74-46d8-49ab-acf3-25c090dcb7b5
  Args:
    target: Francesca_von_Thyssen-Bornemisza
    relation: :hasMother
    source: Eleonore_von_Habsburg-Lothringen
  AssignClass (a06dcd59-67a3-454d-8c6a-f31b413eb352)
 Call ID: a06dcd59-67a3-454d-8c6a-f31b413eb352
  Args:
    source: Otto_von_Habsburg
    type: :Man
  AssignClass (4eaf4376-4402-4255-9c4a-94275d7c64bf)
 Call ID: 4eaf4376-4402-4255-9c4a-94275d7c64bf
  Args:
    type: :Person
    source: Otto_von_Habsburg
  AssignClass (7ecb9845-5b5e-4b27-878f-576c5ad373f8)
 Call ID: 7ecb9845-5b5e-4b27-878f-576c5ad373f8
  Args:
    type: :Woman
    source: Regina_von_Saxe-Meiningen
  AssignClass (cb70e4a0-8ab5-40fa-9044-94e2dd954f92)
 Call ID: cb70e4a0-8ab5-40fa-9044-94e2dd954f92
  Args:
    type: :Person
    source: Regina_von_Saxe-Meiningen
  AddTriple (968f071e-2bbf-4f40-90ab-5670a8397eaa)
 Call ID: 968f071e-2bbf-4f40-90ab-5670a8397eaa
  Args:
    relation: :hasFather
    source: Karl_von_Habsburg
    target: Otto_von_Habsburg
  AddTriple (5d38c55a-fe18-40fb-8480-dcc1e7cfc6aa)
 Call ID: 5d38c55a-fe18-40fb-8480-dcc1e7cfc6aa
  Args:
    relation: :hasMother
    source: Karl_von_Habsburg
    target: Regina_von_Saxe-Meiningen
  AssignClass (5fab753a-fd55-490e-8fc6-b736440d4975)
 Call ID: 5fab753a-fd55-490e-8fc6-b736440d4975
  Args:
    type: :Man
    source: Charles_I_of_Austria
  AssignClass (9f94644d-b272-4b0a-99bc-6bc2b5bb0f80)
 Call ID: 9f94644d-b272-4b0a-99bc-6bc2b5bb0f80
  Args:
    source: Charles_I_of_Austria
    type: :Person
  AssignClass (b05ab5f8-1bed-4b6b-8423-48257068a635)
 Call ID: b05ab5f8-1bed-4b6b-8423-48257068a635
  Args:
    source: Zita_of_Bourbon-Parma
    type: :Woman
  AssignClass (240c3e52-7c3a-489d-ba82-803f5d2b6a51)
 Call ID: 240c3e52-7c3a-489d-ba82-803f5d2b6a51
  Args:
    type: :Person
    source: Zita_of_Bourbon-Parma
  AddTriple (99db20e3-1ad4-4cb5-a6d1-85c68806337c)
 Call ID: 99db20e3-1ad4-4cb5-a6d1-85c68806337c
  Args:
    source: Otto_von_Habsburg
    relation: :hasFather
    target: Charles_I_of_Austria
  AddTriple (059568fe-4d34-4e48-b65c-daafba94ebd5)
 Call ID: 059568fe-4d34-4e48-b65c-daafba94ebd5
  Args:
    relation: :hasMother
    source: Otto_von_Habsburg
    target: Zita_of_Bourbon-Parma
  AssignClass (eb6d133c-be5f-4298-a279-5203c00d594b)
 Call ID: eb6d133c-be5f-4298-a279-5203c00d594b
  Args:
    source: Ferdinand_Habsburg
    type: :Man
  AssignClass (ea978f6b-fc07-43e3-9033-914f5301b682)
 Call ID: ea978f6b-fc07-43e3-9033-914f5301b682
  Args:
    source: Ferdinand_Habsburg
    type: :Person
  AddTriple (03d28a14-45d9-45ad-afcd-80f2d06167d9)
 Call ID: 03d28a14-45d9-45ad-afcd-80f2d06167d9
  Args:
    relation: :hasFather
    source: Ferdinand_Habsburg
    target: Karl_von_Habsburg
  AddTriple (7d89070c-4bbc-427b-8220-8c36cb9a0cae)
 Call ID: 7d89070c-4bbc-427b-8220-8c36cb9a0cae
  Args:
    target: Francesca_von_Thyssen-Bornemisza
    source: Ferdinand_Habsburg
    relation: :hasMother
  AssignClass (5a4664f1-3d6f-477b-a43c-aaa5b5aad53c)
 Call ID: 5a4664f1-3d6f-477b-a43c-aaa5b5aad53c
  Args:
    type: :Man
    source: Jérôme_d'Ambrosio
  AssignClass (b55d0c8b-c36c-4a75-82f6-b04806a05bd9)
 Call ID: b55d0c8b-c36c-4a75-82f6-b04806a05bd9
  Args:
    source: Jérôme_d'Ambrosio
    type: :Person
  AddLiteral (55125f21-3d49-4dfa-a5ba-288d4c7b8fb9)
 Call ID: 55125f21-3d49-4dfa-a5ba-288d4c7b8fb9
  Args:
    relation: :hasMarriageYear
    literal_type: xsd:positiveInteger
    literal_value: 2020
    source: Eleonore_von_Habsburg-Lothringen
  AssignClass (89541b33-2003-44cb-a490-74ce974783fe)
 Call ID: 89541b33-2003-44cb-a490-74ce974783fe
  Args:
    source: Otto_d'Ambrosio
    type: :Man
  AssignClass (1ac5048a-7c61-40ea-a070-c3b7deae95a0)
 Call ID: 1ac5048a-7c61-40ea-a070-c3b7deae95a0
  Args:
    type: :Person
    source: Otto_d'Ambrosio
  AddTriple (87e624f8-39b1-48ca-9964-9818ee54a42f)
 Call ID: 87e624f8-39b1-48ca-9964-9818ee54a42f
  Args:
    target: Jérôme_d'Ambrosio
    relation: :hasFather
    source: Otto_d'Ambrosio
  AddTriple (d0f3ad3d-e4ab-4294-afab-eecdc4a47058)
 Call ID: d0f3ad3d-e4ab-4294-afab-eecdc4a47058
  Args:
    relation: :hasMother
    source: Otto_d'Ambrosio
    target: Eleonore_von_Habsburg-Lothringen
  Finish (067f887a-88c6-4479-8041-02223532a735)
 Call ID: 067f887a-88c6-4479-8041-02223532a735
  Args: