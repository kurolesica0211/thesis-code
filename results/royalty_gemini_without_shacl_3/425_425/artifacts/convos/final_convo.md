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
  AssignClass (4bddc9b9-09f1-4c5b-a7eb-e0632efe9f47)
 Call ID: 4bddc9b9-09f1-4c5b-a7eb-e0632efe9f47
  Args:
    type: :Woman
    source: :Maria_Carolina_of_Bourbon-Two_Sicilies
  AssignClass (765116ec-f644-474d-96e0-18c59f8c7f80)
 Call ID: 765116ec-f644-474d-96e0-18c59f8c7f80
  Args:
    source: :Maria_Carolina_of_Bourbon-Two_Sicilies
    type: :Person
  AddLiteral (4e0eaef8-9f6d-475e-93d9-9e1d44f05e4c)
 Call ID: 4e0eaef8-9f6d-475e-93d9-9e1d44f05e4c
  Args:
    source: :Maria_Carolina_of_Bourbon-Two_Sicilies
    relation: :hasBirthYear
    literal_value: 2003
    literal_type: xsd:integer
  AssignClass (9c06c60b-f0b7-476e-a121-d0e26569b02c)
 Call ID: 9c06c60b-f0b7-476e-a121-d0e26569b02c
  Args:
    type: :Man
    source: :Carlo_of_Bourbon-Two_Sicilies
  AssignClass (982e7e14-6e49-45d7-9115-e8e0086dec89)
 Call ID: 982e7e14-6e49-45d7-9115-e8e0086dec89
  Args:
    type: :Person
    source: :Carlo_of_Bourbon-Two_Sicilies
  AssignClass (4cb124cf-16cb-406b-af92-bc2cc0beee8d)
 Call ID: 4cb124cf-16cb-406b-af92-bc2cc0beee8d
  Args:
    source: :Carlo_of_Bourbon-Two_Sicilies
    type: :Ancestor
  AssignClass (c3a09f90-8ef5-4f34-9b49-3a7bd92b2862)
 Call ID: c3a09f90-8ef5-4f34-9b49-3a7bd92b2862
  Args:
    type: :Woman
    source: :Camilla_Crociani
  AssignClass (bf7cb3ab-1480-4bbc-9bcb-9926cfe8b64f)
 Call ID: bf7cb3ab-1480-4bbc-9bcb-9926cfe8b64f
  Args:
    type: :Person
    source: :Camilla_Crociani
  AssignClass (f8563898-06bc-43f0-860f-cae79ac2959d)
 Call ID: f8563898-06bc-43f0-860f-cae79ac2959d
  Args:
    type: :Ancestor
    source: :Camilla_Crociani
  AddTriple (43c66ede-5c72-4b84-82a6-7df17450dd5f)
 Call ID: 43c66ede-5c72-4b84-82a6-7df17450dd5f
  Args:
    target: :Carlo_of_Bourbon-Two_Sicilies
    source: :Maria_Carolina_of_Bourbon-Two_Sicilies
    relation: :hasFather
  AddTriple (2e1ba783-9c41-46c5-badc-ba18adeaf13f)
 Call ID: 2e1ba783-9c41-46c5-badc-ba18adeaf13f
  Args:
    source: :Maria_Carolina_of_Bourbon-Two_Sicilies
    relation: :hasMother
    target: :Camilla_Crociani
  AssignClass (f380c8a4-7f4a-4095-a9d0-1a0d48cf13da)
 Call ID: f380c8a4-7f4a-4095-a9d0-1a0d48cf13da
  Args:
    source: :Ferdinand_of_Bourbon-Two_Sicilies
    type: :Man
  AssignClass (6540c365-878b-4b15-b579-397241d46db7)
 Call ID: 6540c365-878b-4b15-b579-397241d46db7
  Args:
    source: :Ferdinand_of_Bourbon-Two_Sicilies
    type: :Person
  AssignClass (3bca49f8-1d63-4cf1-b20c-5ce2dd70afaa)
 Call ID: 3bca49f8-1d63-4cf1-b20c-5ce2dd70afaa
  Args:
    type: :Ancestor
    source: :Ferdinand_of_Bourbon-Two_Sicilies
  AddTriple (dbef7e61-77de-4a14-98f3-a6eb44ae0715)
 Call ID: dbef7e61-77de-4a14-98f3-a6eb44ae0715
  Args:
    relation: :hasFather
    source: :Carlo_of_Bourbon-Two_Sicilies
    target: :Ferdinand_of_Bourbon-Two_Sicilies
  AssignClass (c486bf59-0a5f-463a-9a72-4c919ca6b717)
 Call ID: c486bf59-0a5f-463a-9a72-4c919ca6b717
  Args:
    source: :Maria_Chiara_of_Bourbon-Two_Sicilies
    type: :Woman
  AssignClass (8852aa6a-11c3-4297-a6e3-b1deb6ef9579)
 Call ID: 8852aa6a-11c3-4297-a6e3-b1deb6ef9579
  Args:
    source: :Maria_Chiara_of_Bourbon-Two_Sicilies
    type: :Person
  AddTriple (330873d9-d960-43c2-951d-ad88ea0e88eb)
 Call ID: 330873d9-d960-43c2-951d-ad88ea0e88eb
  Args:
    target: :Maria_Chiara_of_Bourbon-Two_Sicilies
    source: :Maria_Carolina_of_Bourbon-Two_Sicilies
    relation: :hasSister
  AssignClass (f52b9399-4a37-4860-b3bc-3a36c5fb4349)
 Call ID: f52b9399-4a37-4860-b3bc-3a36c5fb4349
  Args:
    source: :Beatrice_of_Bourbon-Two_Sicilies
    type: :Woman
  AssignClass (04138616-b5cb-42fd-925b-12d76365a0a7)
 Call ID: 04138616-b5cb-42fd-925b-12d76365a0a7
  Args:
    source: :Beatrice_of_Bourbon-Two_Sicilies
    type: :Person
  AddTriple (bc690e51-fd48-4463-8c83-f3637030c16e)
 Call ID: bc690e51-fd48-4463-8c83-f3637030c16e
  Args:
    target: :Maria_Carolina_of_Bourbon-Two_Sicilies
    source: :Beatrice_of_Bourbon-Two_Sicilies
    relation: :isAuntOf
  AssignClass (b11dec0d-4128-4bb2-be29-495714167786)
 Call ID: b11dec0d-4128-4bb2-be29-495714167786
  Args:
    type: :Man
    source: :Jean-Christophe_Prince_Napoleon
  AssignClass (4cf2bafc-5c4e-4b78-a00c-4710199319d3)
 Call ID: 4cf2bafc-5c4e-4b78-a00c-4710199319d3
  Args:
    source: :Jean-Christophe_Prince_Napoleon
    type: :Person
  AddTriple (f03bd017-cf0b-4289-9f7b-b4d1984cf89b)
 Call ID: f03bd017-cf0b-4289-9f7b-b4d1984cf89b
  Args:
    target: :Jean-Christophe_Prince_Napoleon
    relation: :isBloodrelationOf
    source: :Maria_Carolina_of_Bourbon-Two_Sicilies
  AssignClass (27860486-9a57-4eaf-9199-d17162d1c35e)
 Call ID: 27860486-9a57-4eaf-9199-d17162d1c35e
  Args:
    type: :Man
    source: :Laurent_of_Belgium
  AssignClass (1e3ac0b5-4d37-44db-b3c5-496042e644b6)
 Call ID: 1e3ac0b5-4d37-44db-b3c5-496042e644b6
  Args:
    type: :Person
    source: :Laurent_of_Belgium
  AssignClass (c935a7f3-8234-4b62-8228-124a18f957b8)
 Call ID: c935a7f3-8234-4b62-8228-124a18f957b8
  Args:
    type: :Man
    source: :Philippe_of_Belgium
  AssignClass (3ffa7038-3ac5-4bf7-88bd-c8f7ffa2e80f)
 Call ID: 3ffa7038-3ac5-4bf7-88bd-c8f7ffa2e80f
  Args:
    source: :Philippe_of_Belgium
    type: :Person
  AddTriple (7a38b3fc-7871-4ad2-9f43-1655f7c1e008)
 Call ID: 7a38b3fc-7871-4ad2-9f43-1655f7c1e008
  Args:
    target: :Laurent_of_Belgium
    source: :Philippe_of_Belgium
    relation: :hasBrother
  AssignClass (167ceb16-83c9-46e0-9b28-a1047e291a93)
 Call ID: 167ceb16-83c9-46e0-9b28-a1047e291a93
  Args:
    type: :Man
    source: :Leopold_of_Nassau
  AssignClass (ce866452-62e5-4b48-b921-5da4dc23cd1e)
 Call ID: ce866452-62e5-4b48-b921-5da4dc23cd1e
  Args:
    source: :Leopold_of_Nassau
    type: :Person
  AssignClass (7d92ff01-6afe-4075-b684-840d8a2680a9)
 Call ID: 7d92ff01-6afe-4075-b684-840d8a2680a9
  Args:
    source: :Guillaume_of_Luxembourg
    type: :Man
  AssignClass (48e9a480-4256-4de0-8788-a4359a40124f)
 Call ID: 48e9a480-4256-4de0-8788-a4359a40124f
  Args:
    source: :Guillaume_of_Luxembourg
    type: :Person
  AddTriple (6509427e-a50b-42fa-9e46-325fda2a1ba7)
 Call ID: 6509427e-a50b-42fa-9e46-325fda2a1ba7
  Args:
    relation: :hasFather
    source: :Leopold_of_Nassau
    target: :Guillaume_of_Luxembourg
  Finish (548b106c-b42d-420f-935f-c30dd0819a49)
 Call ID: 548b106c-b42d-420f-935f-c30dd0819a49
  Args: