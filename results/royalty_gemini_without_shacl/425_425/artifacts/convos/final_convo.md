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
The Duke of Castro  The Duchess of Castro


Princess Maria Carolina of Bourbon-Two Sicilies, Duchess of Calabria and Palermo (Italian: Maria Carolina di Borbone delle Due Sicilie; born 23 June 2003) is an Italian socialite, model, and social media influencer.
She is the eldest daughter and heiress of Prince Carlo, Duke of Castro, the disputed head of the House of Bourbon-Two Sicilies.
Early life and education

Maria Carolina was born in Rome on 23 June 2003 to Camilla Crociani, an Italian socialite and heiress, and Prince Carlo of Bourbon-Two Sicilies, Duke of Castro, the disputed head of the House of Bourbon-Two Sicilies.
Her paternal grandfather was Prince Ferdinand, Duke of Castro.
She is the older sister of Princess Maria Chiara.
Her paternal aunt is Princess Béatrice of Bourbon-Two Sicilies.
She is a first cousin of Jean-Christophe, Prince Napoléon.
Maria Carolina was baptized in the Palatine Chapel of the Royal Palace of Caserta.
Her godfather is Prince Laurent of Belgium, younger brother of King Philippe of Belgium.
Maria Carolina grew up between Paris, Monte Carlo, and Rome.
Career, public life, and charitable work

Maria Carolina is an ambassador for the Passion Sea Project, a nonprofit organization that focuses on ocean conservation.
Maria Carolina is a patroness of Rokethon, a Monaco-based charity for abandoned dogs.
In 2016, following her father's abolishment of Salic law, she became the heiress apparent to the headship of the House of Bourbon-Two Sicilies.
She was dressed by Ralph & Russo for the event, and escorted by Prince Léopold of Nassau, son of Prince Guillaume of Luxembourg.
Maria Carolina is a social media influencer, with large followings on Instagram, YouTube, and TikTok.
Personal life

Maria Carolina is fluent in six languages: Italian, French, Spanish, Portuguese, English, and Russian.
In May 2025, Princess Maria Carolina was involved in a near-fatal motorcycle crashing in Monaco.
She was saved by the helmet she was wearing and was later treated at Princess Grace Hospital Centre.



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
  AssignClass (fa6dd30e-bde8-4e05-a10f-32539a7defd6)
 Call ID: fa6dd30e-bde8-4e05-a10f-32539a7defd6
  Args:
    type: :Person
    source: Maria_Carolina_of_Bourbon-Two_Sicilies
  AssignClass (94de3441-3061-4888-a061-a99c1e570670)
 Call ID: 94de3441-3061-4888-a061-a99c1e570670
  Args:
    type: :Woman
    source: Maria_Carolina_of_Bourbon-Two_Sicilies
  AssignClass (d9be4cfe-e30d-4c67-ad03-cc4a10ac5d10)
 Call ID: d9be4cfe-e30d-4c67-ad03-cc4a10ac5d10
  Args:
    type: :Person
    source: Carlo_of_Bourbon-Two_Sicilies
  AssignClass (61dce846-6448-4149-be14-381c695bf7d7)
 Call ID: 61dce846-6448-4149-be14-381c695bf7d7
  Args:
    type: :Man
    source: Carlo_of_Bourbon-Two_Sicilies
  AssignClass (7c4e62d2-bcb5-4461-ae76-f55762d28330)
 Call ID: 7c4e62d2-bcb5-4461-ae76-f55762d28330
  Args:
    source: Camilla_Crociani
    type: :Person
  AssignClass (60cf41b2-002e-415e-9cae-8575f0170506)
 Call ID: 60cf41b2-002e-415e-9cae-8575f0170506
  Args:
    type: :Woman
    source: Camilla_Crociani
  AssignClass (c5d8e478-20a7-4ad9-aa57-4506b13bc7b5)
 Call ID: c5d8e478-20a7-4ad9-aa57-4506b13bc7b5
  Args:
    source: Ferdinand_of_Bourbon-Two_Sicilies
    type: :Person
  AssignClass (f2179dcb-1613-458d-a658-7069697eeaf5)
 Call ID: f2179dcb-1613-458d-a658-7069697eeaf5
  Args:
    type: :Man
    source: Ferdinand_of_Bourbon-Two_Sicilies
  AssignClass (c3d7bd20-d906-4c70-9b56-0e88eac8e26f)
 Call ID: c3d7bd20-d906-4c70-9b56-0e88eac8e26f
  Args:
    source: Maria_Chiara_of_Bourbon-Two_Sicilies
    type: :Person
  AssignClass (91d47bbf-0280-4ab2-a039-8bf7952eca6f)
 Call ID: 91d47bbf-0280-4ab2-a039-8bf7952eca6f
  Args:
    type: :Woman
    source: Maria_Chiara_of_Bourbon-Two_Sicilies
  AssignClass (cf86e59c-7529-4332-90bf-e1af246f378e)
 Call ID: cf86e59c-7529-4332-90bf-e1af246f378e
  Args:
    type: :Person
    source: Béatrice_of_Bourbon-Two_Sicilies
  AssignClass (f2c5e427-ef57-488d-b7bb-d48f48f67e37)
 Call ID: f2c5e427-ef57-488d-b7bb-d48f48f67e37
  Args:
    source: Béatrice_of_Bourbon-Two_Sicilies
    type: :Woman
  AddTriple (c430394e-b263-4a7a-9f72-fa7fa79bb278)
 Call ID: c430394e-b263-4a7a-9f72-fa7fa79bb278
  Args:
    target: Carlo_of_Bourbon-Two_Sicilies
    relation: :hasFather
    source: Maria_Carolina_of_Bourbon-Two_Sicilies
  AddTriple (37393d96-c584-405b-bb10-8e7bd29b2f96)
 Call ID: 37393d96-c584-405b-bb10-8e7bd29b2f96
  Args:
    source: Maria_Carolina_of_Bourbon-Two_Sicilies
    relation: :hasMother
    target: Camilla_Crociani
  AddTriple (7a3d0de3-592e-4a54-8599-11ff66ffebc7)
 Call ID: 7a3d0de3-592e-4a54-8599-11ff66ffebc7
  Args:
    relation: :hasFather
    target: Ferdinand_of_Bourbon-Two_Sicilies
    source: Carlo_of_Bourbon-Two_Sicilies
  AddTriple (593e3067-a157-4b6c-a187-4d3f47f14c20)
 Call ID: 593e3067-a157-4b6c-a187-4d3f47f14c20
  Args:
    target: Maria_Chiara_of_Bourbon-Two_Sicilies
    relation: :hasSister
    source: Maria_Carolina_of_Bourbon-Two_Sicilies
  AddTriple (7b130fde-8006-4e8a-8992-a97be6610ad2)
 Call ID: 7b130fde-8006-4e8a-8992-a97be6610ad2
  Args:
    source: Béatrice_of_Bourbon-Two_Sicilies
    relation: :isSisterOf
    target: Carlo_of_Bourbon-Two_Sicilies
  AddLiteral (26e1d416-da55-45df-9f95-e67dbb42dd7b)
 Call ID: 26e1d416-da55-45df-9f95-e67dbb42dd7b
  Args:
    literal_type: xsd:date
    literal_value: 2003-06-23
    relation: :hasBirthYear
    source: Maria_Carolina_of_Bourbon-Two_Sicilies
  Finish (7a61ed3a-e5e8-47cd-bda6-478dbe4f8583)
 Call ID: 7a61ed3a-e5e8-47cd-bda6-478dbe4f8583
  Args: