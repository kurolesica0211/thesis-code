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
  AssignClass (468de971-4a07-4c8b-97a5-cbeab38d18d1)
 Call ID: 468de971-4a07-4c8b-97a5-cbeab38d18d1
  Args:
    source: Olympia_Bonaparte
    type: :Woman
  AssignClass (6ad1e2c8-7e31-47c1-b0d9-48f08f47ec3e)
 Call ID: 6ad1e2c8-7e31-47c1-b0d9-48f08f47ec3e
  Args:
    source: Olympia_Bonaparte
    type: :Person
  AddLiteral (f0d5224d-a30c-43ec-a2f0-d38f8434007c)
 Call ID: f0d5224d-a30c-43ec-a2f0-d38f8434007c
  Args:
    source: Olympia_Bonaparte
    relation: :hasBirthYear
    literal_value: 1988
    literal_type: xsd:integer
  AssignClass (031efe7e-99ac-48ed-8fd9-2c44914641c4)
 Call ID: 031efe7e-99ac-48ed-8fd9-2c44914641c4
  Args:
    source: Jean-Christophe_Prince_Napoleon
    type: :Man
  AssignClass (768e5164-9250-4fba-a7eb-d29eeed52afb)
 Call ID: 768e5164-9250-4fba-a7eb-d29eeed52afb
  Args:
    type: :Person
    source: Jean-Christophe_Prince_Napoleon
  AddTriple (cb80f0c8-de2f-4e87-9543-6739a9f1446b)
 Call ID: cb80f0c8-de2f-4e87-9543-6739a9f1446b
  Args:
    relation: :hasRelation
    source: Olympia_Bonaparte
    target: Jean-Christophe_Prince_Napoleon
  AddLiteral (10a26eeb-fe09-4f73-b3e9-85e19f1ef0bd)
 Call ID: 10a26eeb-fe09-4f73-b3e9-85e19f1ef0bd
  Args:
    literal_value: 2019
    literal_type: xsd:integer
    source: Olympia_Bonaparte
    relation: :hasMarriageYear
  AssignClass (9eb94eab-f92b-4453-b05b-5c83930b5a61)
 Call ID: 9eb94eab-f92b-4453-b05b-5c83930b5a61
  Args:
    type: :Man
    source: Riprand_von_und_zu_Arco-Zinneberg
  AssignClass (c8b00b7b-43bb-45dd-83d4-626123c1b33f)
 Call ID: c8b00b7b-43bb-45dd-83d4-626123c1b33f
  Args:
    source: Riprand_von_und_zu_Arco-Zinneberg
    type: :Person
  AddLiteral (9da431f9-51e6-476b-b3b6-b3233938bb1f)
 Call ID: 9da431f9-51e6-476b-b3b6-b3233938bb1f
  Args:
    source: Riprand_von_und_zu_Arco-Zinneberg
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1955
  AddLiteral (1ef6a107-72a8-4ceb-b152-d9c7f1f55eb6)
 Call ID: 1ef6a107-72a8-4ceb-b152-d9c7f1f55eb6
  Args:
    relation: :hasDeathYear
    source: Riprand_von_und_zu_Arco-Zinneberg
    literal_value: 2021
    literal_type: xsd:integer
  AssignClass (ce269ea6-c782-4ee7-b57b-36efc228009c)
 Call ID: ce269ea6-c782-4ee7-b57b-36efc228009c
  Args:
    type: :Woman
    source: Maria_Beatrice_of_Austria-Este
  AssignClass (aee53193-11c4-4cf4-a53e-645fd67cbd3d)
 Call ID: aee53193-11c4-4cf4-a53e-645fd67cbd3d
  Args:
    source: Maria_Beatrice_of_Austria-Este
    type: :Person
  AddTriple (1fb97521-a3a2-4352-aae3-56f602aa1919)
 Call ID: 1fb97521-a3a2-4352-aae3-56f602aa1919
  Args:
    target: Riprand_von_und_zu_Arco-Zinneberg
    relation: :hasFather
    source: Olympia_Bonaparte
  AddTriple (6898adfa-d36a-4b3c-b5bc-2038238fce54)
 Call ID: 6898adfa-d36a-4b3c-b5bc-2038238fce54
  Args:
    target: Maria_Beatrice_of_Austria-Este
    relation: :hasMother
    source: Olympia_Bonaparte
  AssignClass (d1c35276-72de-4ca7-9cc2-9566b636101a)
 Call ID: d1c35276-72de-4ca7-9cc2-9566b636101a
  Args:
    type: :Man
    source: Louis_Charles_Riprand_Victor_Jerome_Marie
  AssignClass (d2fbf294-1a3d-401a-9292-6043f98bd3f7)
 Call ID: d2fbf294-1a3d-401a-9292-6043f98bd3f7
  Args:
    type: :Person
    source: Louis_Charles_Riprand_Victor_Jerome_Marie
  AddTriple (7c2152b0-faf8-456a-bcd9-37f0cab56ba9)
 Call ID: 7c2152b0-faf8-456a-bcd9-37f0cab56ba9
  Args:
    target: Olympia_Bonaparte
    source: Louis_Charles_Riprand_Victor_Jerome_Marie
    relation: :isSonOf
  AddTriple (2056acb4-313b-4eb7-9a27-5e2dbdfdadb8)
 Call ID: 2056acb4-313b-4eb7-9a27-5e2dbdfdadb8
  Args:
    relation: :isSonOf
    source: Louis_Charles_Riprand_Victor_Jerome_Marie
    target: Jean-Christophe_Prince_Napoleon
  Finish (e5d6f380-1971-4cc4-85bd-b3d0db88ce25)
 Call ID: e5d6f380-1971-4cc4-85bd-b3d0db88ce25
  Args: