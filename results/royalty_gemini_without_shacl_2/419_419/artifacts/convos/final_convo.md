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
  AssignClass (3e09b7e2-1ff7-4eee-8665-3266cfc13deb)
 Call ID: 3e09b7e2-1ff7-4eee-8665-3266cfc13deb
  Args:
    type: :Woman
    source: :Olympia_Bonaparte
  AssignClass (98eeff53-8632-4ef1-9c71-acac30917691)
 Call ID: 98eeff53-8632-4ef1-9c71-acac30917691
  Args:
    type: :Person
    source: :Olympia_Bonaparte
  AddLiteral (f5a3e043-4532-4a1d-ad5d-76f6d6a08daf)
 Call ID: f5a3e043-4532-4a1d-ad5d-76f6d6a08daf
  Args:
    literal_type: xsd:integer
    literal_value: 1988
    relation: :hasBirthYear
    source: :Olympia_Bonaparte
  AssignClass (e61ec4ec-127b-41f4-9684-8e20f49e1905)
 Call ID: e61ec4ec-127b-41f4-9684-8e20f49e1905
  Args:
    type: :Man
    source: :Jean-Christophe_Prince_Napoleon
  AssignClass (c30c23b5-7a93-419d-9afd-536148dbb7d9)
 Call ID: c30c23b5-7a93-419d-9afd-536148dbb7d9
  Args:
    type: :Person
    source: :Jean-Christophe_Prince_Napoleon
  AddTriple (e20550a2-fa72-4a4d-ab71-901ffa840c36)
 Call ID: e20550a2-fa72-4a4d-ab71-901ffa840c36
  Args:
    target: :Jean-Christophe_Prince_Napoleon
    relation: :hasRelation
    source: :Olympia_Bonaparte
  AssignClass (11c1d12d-937d-4f8c-9596-23a2a1dfee73)
 Call ID: 11c1d12d-937d-4f8c-9596-23a2a1dfee73
  Args:
    type: :Man
    source: :Count_Riprand_von_und_zu_Arco-Zinneberg
  AssignClass (7cddca50-52d7-468b-b771-9261761f4c92)
 Call ID: 7cddca50-52d7-468b-b771-9261761f4c92
  Args:
    type: :Person
    source: :Count_Riprand_von_und_zu_Arco-Zinneberg
  AssignClass (1798d4aa-830c-406e-a113-49d3b34a5f20)
 Call ID: 1798d4aa-830c-406e-a113-49d3b34a5f20
  Args:
    type: :Ancestor
    source: :Count_Riprand_von_und_zu_Arco-Zinneberg
  AddLiteral (0ea35208-125c-438d-9f13-38e89aed66fe)
 Call ID: 0ea35208-125c-438d-9f13-38e89aed66fe
  Args:
    literal_value: 1955
    source: :Count_Riprand_von_und_zu_Arco-Zinneberg
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (2e00f8f1-05bc-4d1c-a82c-c0f4b7c0527c)
 Call ID: 2e00f8f1-05bc-4d1c-a82c-c0f4b7c0527c
  Args:
    literal_type: xsd:integer
    source: :Count_Riprand_von_und_zu_Arco-Zinneberg
    relation: :hasDeathYear
    literal_value: 2021
  AssignClass (33807182-3cf0-4603-8ec1-9b9acf422be1)
 Call ID: 33807182-3cf0-4603-8ec1-9b9acf422be1
  Args:
    type: :Woman
    source: :Archduchess_Maria_Beatrice_of_Austria-Este
  AssignClass (1e1767e3-a9ba-49f2-9452-7d33a7e410d9)
 Call ID: 1e1767e3-a9ba-49f2-9452-7d33a7e410d9
  Args:
    type: :Person
    source: :Archduchess_Maria_Beatrice_of_Austria-Este
  AssignClass (9c91646f-1a8d-4e37-9630-425b7f9b8474)
 Call ID: 9c91646f-1a8d-4e37-9630-425b7f9b8474
  Args:
    type: :Ancestor
    source: :Archduchess_Maria_Beatrice_of_Austria-Este
  AddTriple (64fff9f8-0bad-414a-bf4f-aee1cc0b623a)
 Call ID: 64fff9f8-0bad-414a-bf4f-aee1cc0b623a
  Args:
    relation: :hasFather
    source: :Olympia_Bonaparte
    target: :Count_Riprand_von_und_zu_Arco-Zinneberg
  AddTriple (5e0a792b-20c8-4435-b280-387ccd12b25e)
 Call ID: 5e0a792b-20c8-4435-b280-387ccd12b25e
  Args:
    target: :Archduchess_Maria_Beatrice_of_Austria-Este
    relation: :hasMother
    source: :Olympia_Bonaparte
  AssignClass (d63b815b-5787-4ee8-9faa-a9d6bfb9cd1b)
 Call ID: d63b815b-5787-4ee8-9faa-a9d6bfb9cd1b
  Args:
    type: :Man
    source: :Louis_Charles_Riprand_Victor_Jerome_Marie
  AssignClass (266eccb2-b0d5-4395-90e0-7640651f5507)
 Call ID: 266eccb2-b0d5-4395-90e0-7640651f5507
  Args:
    type: :Person
    source: :Louis_Charles_Riprand_Victor_Jerome_Marie
  AddTriple (71a071d8-43e2-4617-84ce-fa84fb019ccf)
 Call ID: 71a071d8-43e2-4617-84ce-fa84fb019ccf
  Args:
    source: :Louis_Charles_Riprand_Victor_Jerome_Marie
    relation: :isSonOf
    target: :Olympia_Bonaparte
  AddTriple (aa663167-1e69-4fd3-a4fc-c0e443b26eaf)
 Call ID: aa663167-1e69-4fd3-a4fc-c0e443b26eaf
  Args:
    target: :Jean-Christophe_Prince_Napoleon
    relation: :isSonOf
    source: :Louis_Charles_Riprand_Victor_Jerome_Marie
  AddLiteral (ab23587d-6e15-4e14-8267-f299dfc716bb)
 Call ID: ab23587d-6e15-4e14-8267-f299dfc716bb
  Args:
    literal_type: xsd:integer
    literal_value: 2022
    source: :Louis_Charles_Riprand_Victor_Jerome_Marie
    relation: :hasBirthYear
  Finish (f0ca3299-0826-4e04-9b3a-a4053e6b2f26)
 Call ID: f0ca3299-0826-4e04-9b3a-a4053e6b2f26
  Args: