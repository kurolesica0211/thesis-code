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
The Dowager Princess Napoléon


Olympia Bonaparte, Princess Napoléon (Olympia Elene Marie; née Countess Olympia von und zu Arco-Zinneberg, born 4 January 1988), is the wife of Jean-Christophe, Prince Napoléon, the disputed head of the House of Bonaparte and, in the view of Bonapartists, the pretender to the abolished French imperial throne.
Early life and family

Countess Olympia Elene Marie von und zu Arco-Zinneberg was born on 4 January 1988 in Munich to Count Riprand von und zu Arco-Zinneberg (1955-2021) and his wife, Archduchess Maria Beatrice of Austria-Este.
Through her father she is a great-great-granddaughter of Ludwig III and Maria Theresa of Austria-Este, the last king and queen of Bavaria.
Through her mother she is the granddaughter of Robert, Archduke of Austria-Este and Princess Margherita of Savoy-Aosta.
She is a great-granddaughter of Charles I and Zita of Bourbon-Parma, the last emperor and empress of Austria.
Olympia is also the great-great-great-great-grandniece of Marie Louise, Duchess of Parma, the second wife of Napoleon I.


Personal life

Olympia graduated from Yale University with a bachelor's degree in political science and from Columbia University in 2015 with a Master of Arts degree in art history.
She met Jean-Christophe, Prince Napoléon during a semester studying abroad in Paris.
Olympia and Jean-Christophe first held a civil marriage on 17 October 2019 at the town hall of Neuilly-sur-Seine.
The wedding festivities were attended by members of European royal and noble families including Henri, Grand Duke of Luxembourg; Guillaume, Hereditary Grand Duke of Luxembourg; Stéphanie, Hereditary Grand Duchess of Luxembourg; Princess Maria Laura of Belgium, Archduchess of Austria-Este; Pavlos, Crown Prince of Greece; Princess Maria-Olympia of Greece and Denmark; Prince Philippos of Greece and Denmark; Nina Flohr; Prince Félix of Luxembourg; Princess Claire of Luxembourg; Prince Christian of Hanover; Princess Christian of Hanover; Princess Beatrice of York; and Edoardo Mapelli Mozzi.
The Princess gave birth to a son, Louis Charles Riprand Victor Jérôme Marie, on 7 December 2022 in Paris.



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
  AssignClass (f0822a3a-4603-494c-8876-49996d07e962)
 Call ID: f0822a3a-4603-494c-8876-49996d07e962
  Args:
    type: :Woman
    source: Olympia_Bonaparte
  AssignClass (d357f88d-3745-42ab-bd5b-136c452f594c)
 Call ID: d357f88d-3745-42ab-bd5b-136c452f594c
  Args:
    source: Olympia_Bonaparte
    type: :Person
  AddLiteral (1e5ead7a-331e-4ca1-8fa4-a14405495cd8)
 Call ID: 1e5ead7a-331e-4ca1-8fa4-a14405495cd8
  Args:
    source: Olympia_Bonaparte
    literal_type: xsd:nonNegativeInteger
    relation: :hasBirthYear
    literal_value: 1988
  AssignClass (11b6761c-48f7-4c02-9935-0a2d417ef7e8)
 Call ID: 11b6761c-48f7-4c02-9935-0a2d417ef7e8
  Args:
    type: :Man
    source: Jean-Christophe_Prince_Napoleon
  AssignClass (b619f582-35fd-40d6-8c1b-00ad1d0b15bc)
 Call ID: b619f582-35fd-40d6-8c1b-00ad1d0b15bc
  Args:
    type: :Person
    source: Jean-Christophe_Prince_Napoleon
  AddTriple (043c236a-3d96-476e-a0ee-0b5f4ee2da90)
 Call ID: 043c236a-3d96-476e-a0ee-0b5f4ee2da90
  Args:
    source: Olympia_Bonaparte
    relation: :hasRelation
    target: Jean-Christophe_Prince_Napoleon
  AddLiteral (013824e4-88f3-4515-b0bd-22c168f9ad67)
 Call ID: 013824e4-88f3-4515-b0bd-22c168f9ad67
  Args:
    literal_type: xsd:nonNegativeInteger
    relation: :hasMarriageYear
    literal_value: 2019
    source: Olympia_Bonaparte
  AssignClass (7d83d8b9-53e0-4886-9e57-39e11457e730)
 Call ID: 7d83d8b9-53e0-4886-9e57-39e11457e730
  Args:
    source: Riprand_von_und_zu_Arco-Zinneberg
    type: :Man
  AssignClass (1d47cd44-72d7-408d-be13-216a3a9ac3e4)
 Call ID: 1d47cd44-72d7-408d-be13-216a3a9ac3e4
  Args:
    type: :Person
    source: Riprand_von_und_zu_Arco-Zinneberg
  AssignClass (fd7e8d8a-e188-4aa6-89f7-2619fb2225db)
 Call ID: fd7e8d8a-e188-4aa6-89f7-2619fb2225db
  Args:
    type: :Ancestor
    source: Riprand_von_und_zu_Arco-Zinneberg
  AddLiteral (e05a8204-3d30-4aa7-a05b-ddddfdc466eb)
 Call ID: e05a8204-3d30-4aa7-a05b-ddddfdc466eb
  Args:
    source: Riprand_von_und_zu_Arco-Zinneberg
    literal_value: 1955
    relation: :hasBirthYear
    literal_type: xsd:nonNegativeInteger
  AddLiteral (57bcfe5a-6eb9-4b8f-a6cc-9490a7869660)
 Call ID: 57bcfe5a-6eb9-4b8f-a6cc-9490a7869660
  Args:
    relation: :hasDeathYear
    literal_value: 2021
    literal_type: xsd:nonNegativeInteger
    source: Riprand_von_und_zu_Arco-Zinneberg
  AssignClass (df63fb85-96e0-4aec-9c62-a00e0583b2ae)
 Call ID: df63fb85-96e0-4aec-9c62-a00e0583b2ae
  Args:
    source: Maria_Beatrice_of_Austria-Este
    type: :Woman
  AssignClass (b1ddf33a-39cb-4e09-98f2-4f66f8af1b6d)
 Call ID: b1ddf33a-39cb-4e09-98f2-4f66f8af1b6d
  Args:
    source: Maria_Beatrice_of_Austria-Este
    type: :Person
  AssignClass (ae1b1d1d-e7c9-49ee-867f-2c3617c74c72)
 Call ID: ae1b1d1d-e7c9-49ee-867f-2c3617c74c72
  Args:
    type: :Ancestor
    source: Maria_Beatrice_of_Austria-Este
  AddTriple (453861a4-528d-4e3d-a2ed-4a8eb6818dc0)
 Call ID: 453861a4-528d-4e3d-a2ed-4a8eb6818dc0
  Args:
    source: Olympia_Bonaparte
    target: Riprand_von_und_zu_Arco-Zinneberg
    relation: :hasFather
  AddTriple (99157500-afa4-46cf-a523-e3672b8ade77)
 Call ID: 99157500-afa4-46cf-a523-e3672b8ade77
  Args:
    target: Maria_Beatrice_of_Austria-Este
    relation: :hasMother
    source: Olympia_Bonaparte
  AssignClass (c518cfb3-8804-469a-ad61-0f594db7068d)
 Call ID: c518cfb3-8804-469a-ad61-0f594db7068d
  Args:
    type: :Man
    source: Louis_Charles_Riprand_Victor_Jerome_Marie
  AssignClass (8c6b81be-4545-4b3a-a3f5-5f99c9e79b63)
 Call ID: 8c6b81be-4545-4b3a-a3f5-5f99c9e79b63
  Args:
    type: :Person
    source: Louis_Charles_Riprand_Victor_Jerome_Marie
  AddTriple (c1998492-88c5-4695-8a81-98290c50f88a)
 Call ID: c1998492-88c5-4695-8a81-98290c50f88a
  Args:
    source: Louis_Charles_Riprand_Victor_Jerome_Marie
    target: Jean-Christophe_Prince_Napoleon
    relation: :hasFather
  AddTriple (8eab4bc4-3d70-4187-856c-20336eeeca90)
 Call ID: 8eab4bc4-3d70-4187-856c-20336eeeca90
  Args:
    source: Louis_Charles_Riprand_Victor_Jerome_Marie
    target: Olympia_Bonaparte
    relation: :hasMother
  Finish (fe4f5407-c168-4f13-9ceb-d9582436b82b)
 Call ID: fe4f5407-c168-4f13-9ceb-d9582436b82b
  Args: