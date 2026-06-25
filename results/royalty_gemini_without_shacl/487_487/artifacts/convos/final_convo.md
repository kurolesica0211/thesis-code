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
  AssignClass (e61f1ae1-c7aa-4a49-82ad-44a5d977feb1)
 Call ID: e61f1ae1-c7aa-4a49-82ad-44a5d977feb1
  Args:
    type: :Woman
    source: Eleonore_von_Habsburg-Lothringen
  AssignClass (c6c77583-5894-4066-a205-6f0f0e708582)
 Call ID: c6c77583-5894-4066-a205-6f0f0e708582
  Args:
    source: Eleonore_von_Habsburg-Lothringen
    type: :Person
  AddLiteral (56df32e0-7993-40c2-b638-a2db5b6cb615)
 Call ID: 56df32e0-7993-40c2-b638-a2db5b6cb615
  Args:
    literal_type: xsd:integer
    literal_value: 1994
    source: Eleonore_von_Habsburg-Lothringen
    relation: :hasBirthYear
  AssignClass (ad5a610b-63b1-4518-a5c0-3c8d5c2b5c48)
 Call ID: ad5a610b-63b1-4518-a5c0-3c8d5c2b5c48
  Args:
    source: Karl_von_Habsburg
    type: :Man
  AssignClass (dbbb4382-13c9-4d78-a9f0-e36aa3091081)
 Call ID: dbbb4382-13c9-4d78-a9f0-e36aa3091081
  Args:
    type: :Person
    source: Karl_von_Habsburg
  AddTriple (97ca66b8-8842-41bb-80da-1ded6f289e82)
 Call ID: 97ca66b8-8842-41bb-80da-1ded6f289e82
  Args:
    source: Eleonore_von_Habsburg-Lothringen
    relation: :hasFather
    target: Karl_von_Habsburg
  AssignClass (432b8798-0f45-41a6-b696-b3e166538d8f)
 Call ID: 432b8798-0f45-41a6-b696-b3e166538d8f
  Args:
    source: Francesca_von_Thyssen-Bornemisza
    type: :Woman
  AssignClass (850c232f-74c6-4584-98e6-e76fc581f077)
 Call ID: 850c232f-74c6-4584-98e6-e76fc581f077
  Args:
    type: :Person
    source: Francesca_von_Thyssen-Bornemisza
  AddTriple (31e961ee-67b0-481b-96b7-e214a5d2ea15)
 Call ID: 31e961ee-67b0-481b-96b7-e214a5d2ea15
  Args:
    source: Eleonore_von_Habsburg-Lothringen
    relation: :hasMother
    target: Francesca_von_Thyssen-Bornemisza
  AssignClass (d00e378c-9e50-4a74-9ea6-6e5b136d47e5)
 Call ID: d00e378c-9e50-4a74-9ea6-6e5b136d47e5
  Args:
    source: Otto_von_Habsburg
    type: :Man
  AssignClass (3ccbbda7-2df5-453a-8b14-a55b473f9bfd)
 Call ID: 3ccbbda7-2df5-453a-8b14-a55b473f9bfd
  Args:
    type: :Person
    source: Otto_von_Habsburg
  AssignClass (febc297a-12f8-4ecb-af7c-d70651a1e9bc)
 Call ID: febc297a-12f8-4ecb-af7c-d70651a1e9bc
  Args:
    source: Regina_von_Saxe-Meiningen
    type: :Woman
  AssignClass (d437f963-a155-4434-a449-b2075cef5c1c)
 Call ID: d437f963-a155-4434-a449-b2075cef5c1c
  Args:
    type: :Person
    source: Regina_von_Saxe-Meiningen
  AddTriple (558e21c8-e5d7-4280-bb4f-94f003cba642)
 Call ID: 558e21c8-e5d7-4280-bb4f-94f003cba642
  Args:
    target: Otto_von_Habsburg
    relation: :hasFather
    source: Karl_von_Habsburg
  AddTriple (ca9c6920-3919-42b8-8fac-212f1f535d06)
 Call ID: ca9c6920-3919-42b8-8fac-212f1f535d06
  Args:
    source: Karl_von_Habsburg
    relation: :hasMother
    target: Regina_von_Saxe-Meiningen
  AssignClass (cc26b02f-1de5-499b-a4dc-2866f0d8d158)
 Call ID: cc26b02f-1de5-499b-a4dc-2866f0d8d158
  Args:
    type: :Man
    source: Charles_I_of_Austria
  AssignClass (1aac8e9a-ac44-4ceb-926c-5b1accddbdc8)
 Call ID: 1aac8e9a-ac44-4ceb-926c-5b1accddbdc8
  Args:
    source: Charles_I_of_Austria
    type: :Person
  AssignClass (035d590c-15a1-4fd0-97ca-740e85b5b6ca)
 Call ID: 035d590c-15a1-4fd0-97ca-740e85b5b6ca
  Args:
    type: :Woman
    source: Zita_of_Bourbon-Parma
  AssignClass (972bf602-6b90-4b85-8844-f663ce57d9d7)
 Call ID: 972bf602-6b90-4b85-8844-f663ce57d9d7
  Args:
    source: Zita_of_Bourbon-Parma
    type: :Person
  AddTriple (e7680e5b-bd86-4c55-a989-d322be5cc04e)
 Call ID: e7680e5b-bd86-4c55-a989-d322be5cc04e
  Args:
    target: Charles_I_of_Austria
    source: Otto_von_Habsburg
    relation: :hasFather
  AddTriple (17721777-b2dc-4807-82c8-0fefa9250c70)
 Call ID: 17721777-b2dc-4807-82c8-0fefa9250c70
  Args:
    relation: :hasMother
    source: Otto_von_Habsburg
    target: Zita_of_Bourbon-Parma
  AssignClass (1d635af2-de61-4aae-b401-816a2cf6c68f)
 Call ID: 1d635af2-de61-4aae-b401-816a2cf6c68f
  Args:
    source: Ferdinand_Habsburg
    type: :Man
  AssignClass (285f2c61-61ad-406d-ac94-bf48783d38b2)
 Call ID: 285f2c61-61ad-406d-ac94-bf48783d38b2
  Args:
    type: :Person
    source: Ferdinand_Habsburg
  AddTriple (a9daab62-86c8-4527-984e-32fe21dd2c65)
 Call ID: a9daab62-86c8-4527-984e-32fe21dd2c65
  Args:
    target: Karl_von_Habsburg
    relation: :hasFather
    source: Ferdinand_Habsburg
  AddTriple (c3fdc470-6c4d-416f-9f5b-a94113d6ac30)
 Call ID: c3fdc470-6c4d-416f-9f5b-a94113d6ac30
  Args:
    target: Francesca_von_Thyssen-Bornemisza
    relation: :hasMother
    source: Ferdinand_Habsburg
  AssignClass (83a36800-a477-4ecb-876f-8499156da07a)
 Call ID: 83a36800-a477-4ecb-876f-8499156da07a
  Args:
    source: Jerome_d_Ambrosio
    type: :Man
  AssignClass (3c33a1c9-c747-4564-8549-855532451cb5)
 Call ID: 3c33a1c9-c747-4564-8549-855532451cb5
  Args:
    source: Jerome_d_Ambrosio
    type: :Person
  AddLiteral (7bcc59d0-fde5-4ee2-b10e-4ee93ccb5347)
 Call ID: 7bcc59d0-fde5-4ee2-b10e-4ee93ccb5347
  Args:
    literal_value: 2020
    literal_type: xsd:integer
    source: Eleonore_von_Habsburg-Lothringen
    relation: :hasMarriageYear
  AddTriple (88caa367-8dcd-45e9-b800-c7d625e2f545)
 Call ID: 88caa367-8dcd-45e9-b800-c7d625e2f545
  Args:
    target: Jerome_d_Ambrosio
    relation: :hasRelation
    source: Eleonore_von_Habsburg-Lothringen
  AssignClass (bd669deb-9722-415d-b482-3116ddf4b3c2)
 Call ID: bd669deb-9722-415d-b482-3116ddf4b3c2
  Args:
    type: :Man
    source: Otto_d_Ambrosio
  AssignClass (830775e9-e8d3-4e37-a1dd-f715790e76d7)
 Call ID: 830775e9-e8d3-4e37-a1dd-f715790e76d7
  Args:
    source: Otto_d_Ambrosio
    type: :Person
  AddTriple (fcafd648-6491-46c6-be33-bc918476bb8c)
 Call ID: fcafd648-6491-46c6-be33-bc918476bb8c
  Args:
    relation: :hasFather
    source: Otto_d_Ambrosio
    target: Jerome_d_Ambrosio
  AddTriple (dc8eaf15-b7d2-4beb-a237-d480a3923e39)
 Call ID: dc8eaf15-b7d2-4beb-a237-d480a3923e39
  Args:
    target: Eleonore_von_Habsburg-Lothringen
    source: Otto_d_Ambrosio
    relation: :hasMother
  Finish (2df2b87a-7158-4269-975c-783f1d40daf0)
 Call ID: 2df2b87a-7158-4269-975c-783f1d40daf0
  Args: