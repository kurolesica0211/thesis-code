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
Queen Anne-Marie


Queen Sofía of Spain


Marina, consort of Prince Michael


Prince Nikolaos of Greece and Denmark (Greek: Νικόλαος Ντε Γκρες, romanized: Nikólaos de Grèce; born 1 October 1969) is the third child of Constantine II and Anne-Marie, who were the last King and Queen of Greece, from 1964 to 1973.
Early life and education

Nikolaos was born at Casa di Cura Privata Nuova Villa Claudia in Rome, Italy, on October 1, 1969.
He is the first royal child to be born in hospital from Constantine II of Greece and Anne-Marie of Denmark.
His godparents were Queen Sofía, Queen of Spain (his paternal aunt), Princess Irene of Greece and Denmark (another paternal aunt), Margareta of Romania (his paternal second cousin), and Crown Prince Alexander of Yugoslavia (another paternal second cousin).
He is a member of board of the Anna-Maria Foundation, designed to help victims of natural disasters like floods and earthquakes in Greece.
Nikolaos has an older sister Princess Alexia, an older brother Crown Prince Pavlos, a younger sister Princess Theodora, and a younger brother, Prince Philippos.
Personal life

Relationships

The engagement of Nikolaos to Tatiana Ellinka Blatnik, with whom he had been in a long-term relationship, was announced on 28 December 2009 by the office of King Constantine in London.
On 25 August 2010, the couple married at the Orthodox Church of St. Nicholas in Spetses, Greece.
In January 2025, Nikolaos became engaged to Chrysí Vardinogiánni, daughter of Greek businessman Giórgos Vardinogiánnis and Agapi Politi.
Citizenship

Οn 20 December 2024, Nikolaos along with other members of the former royal family acquired Greek citizenship, under the surname de Grèce.



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
  AssignClass (cd6b9c6c-183d-44a0-aea4-dcb44e4dc356)
 Call ID: cd6b9c6c-183d-44a0-aea4-dcb44e4dc356
  Args:
    source: :Anne-Marie
    type: :Woman
  AssignClass (e8764e1a-9f0e-4aa4-bbc2-013a8b213a50)
 Call ID: e8764e1a-9f0e-4aa4-bbc2-013a8b213a50
  Args:
    source: :Sofia
    type: :Woman
  AssignClass (69fa29d6-0458-4b5a-830c-5733ee011039)
 Call ID: 69fa29d6-0458-4b5a-830c-5733ee011039
  Args:
    source: :Marina
    type: :Woman
  AssignClass (6bcf5c85-5076-45d6-ab70-edbebc57b431)
 Call ID: 6bcf5c85-5076-45d6-ab70-edbebc57b431
  Args:
    source: :Michael
    type: :Man
  AssignClass (26453cdf-20e3-4f23-a88d-92d3dcbb89c8)
 Call ID: 26453cdf-20e3-4f23-a88d-92d3dcbb89c8
  Args:
    type: :Man
    source: :Nikolaos
  AssignClass (fbdbb7cf-6a04-4c45-8f28-3b8c9aa7c82d)
 Call ID: fbdbb7cf-6a04-4c45-8f28-3b8c9aa7c82d
  Args:
    source: :ConstantineII
    type: :Man
  AssignClass (799d602c-952a-4467-a3f6-91787a05a884)
 Call ID: 799d602c-952a-4467-a3f6-91787a05a884
  Args:
    source: :Irene
    type: :Woman
  AssignClass (ae3a72f1-0a9d-485e-b2df-e9768dded039)
 Call ID: ae3a72f1-0a9d-485e-b2df-e9768dded039
  Args:
    type: :Woman
    source: :Margareta
  AssignClass (7d9d6039-f241-49fb-91d4-3a9fb4bc5939)
 Call ID: 7d9d6039-f241-49fb-91d4-3a9fb4bc5939
  Args:
    source: :Alexander
    type: :Man
  AssignClass (a5df1875-0332-4664-b79c-ee84bda45deb)
 Call ID: a5df1875-0332-4664-b79c-ee84bda45deb
  Args:
    type: :Woman
    source: :Alexia
  AssignClass (345785ae-7f3c-4985-bfb1-3184d7e9c232)
 Call ID: 345785ae-7f3c-4985-bfb1-3184d7e9c232
  Args:
    type: :Man
    source: :Pavlos
  AssignClass (084f1346-1d1c-4dde-893b-6a52fc837cbe)
 Call ID: 084f1346-1d1c-4dde-893b-6a52fc837cbe
  Args:
    type: :Woman
    source: :Theodora
  AssignClass (9acb8878-5bf9-4dea-8e0d-0f9d73c03e11)
 Call ID: 9acb8878-5bf9-4dea-8e0d-0f9d73c03e11
  Args:
    type: :Man
    source: :Philippos
  AssignClass (d3924a5f-1d4c-4d6d-83f2-29a485a04de9)
 Call ID: d3924a5f-1d4c-4d6d-83f2-29a485a04de9
  Args:
    source: :TatianaEllinkaBlatnik
    type: :Woman
  AssignClass (530dafe1-98de-4112-9e3a-3758307be120)
 Call ID: 530dafe1-98de-4112-9e3a-3758307be120
  Args:
    source: :ChrysiVardinogianni
    type: :Woman
  AssignClass (4efb5c68-3d72-4f13-8304-247e4c4084d5)
 Call ID: 4efb5c68-3d72-4f13-8304-247e4c4084d5
  Args:
    type: :Man
    source: :GiorgosVardinogiannis
  AssignClass (56128724-dbbd-4490-94a9-595976e7ce01)
 Call ID: 56128724-dbbd-4490-94a9-595976e7ce01
  Args:
    type: :Woman
    source: :AgapiPoliti
  AddLiteral (52201516-bdcc-4035-bea9-b22577086986)
 Call ID: 52201516-bdcc-4035-bea9-b22577086986
  Args:
    literal_type: xsd:integer
    literal_value: 1969
    source: :Nikolaos
    relation: :hasBirthYear
  AddTriple (e088396b-c6bf-412c-b2d4-7c9f03ec8206)
 Call ID: e088396b-c6bf-412c-b2d4-7c9f03ec8206
  Args:
    target: :ConstantineII
    source: :Nikolaos
    relation: :hasFather
  AddTriple (f6c1468b-2826-406d-9d1f-aa7f2b0f308d)
 Call ID: f6c1468b-2826-406d-9d1f-aa7f2b0f308d
  Args:
    target: :Anne-Marie
    source: :Nikolaos
    relation: :hasMother
  AddTriple (7aec73f4-837b-493e-995b-eab7ec65de97)
 Call ID: 7aec73f4-837b-493e-995b-eab7ec65de97
  Args:
    relation: :hasSister
    source: :Nikolaos
    target: :Alexia
  AddTriple (e9075b4c-5ce7-422c-8663-5f6239ae1a7a)
 Call ID: e9075b4c-5ce7-422c-8663-5f6239ae1a7a
  Args:
    target: :Pavlos
    relation: :hasBrother
    source: :Nikolaos
  AddTriple (5205e8ad-f067-4d9e-828c-1ca3a35d7e72)
 Call ID: 5205e8ad-f067-4d9e-828c-1ca3a35d7e72
  Args:
    source: :Nikolaos
    relation: :hasSister
    target: :Theodora
  AddTriple (90d93ae3-7897-448b-964a-8104f3715082)
 Call ID: 90d93ae3-7897-448b-964a-8104f3715082
  Args:
    relation: :hasBrother
    source: :Nikolaos
    target: :Philippos
  AddLiteral (3df6c880-46a6-4214-b0a0-ac29dc748a04)
 Call ID: 3df6c880-46a6-4214-b0a0-ac29dc748a04
  Args:
    source: :Nikolaos
    relation: :hasMarriageYear
    literal_value: 2010
    literal_type: xsd:integer
  AddTriple (826a0f96-32d7-47a7-b88a-25995391d001)
 Call ID: 826a0f96-32d7-47a7-b88a-25995391d001
  Args:
    source: :ChrysiVardinogianni
    relation: :hasFather
    target: :GiorgosVardinogiannis
  AddTriple (9a528e84-188d-4ed9-89d3-3b4013311f35)
 Call ID: 9a528e84-188d-4ed9-89d3-3b4013311f35
  Args:
    target: :AgapiPoliti
    relation: :hasMother
    source: :ChrysiVardinogianni
  Finish (0246aca4-624d-4dcb-aaf4-11d687b219f5)
 Call ID: 0246aca4-624d-4dcb-aaf4-11d687b219f5
  Args: