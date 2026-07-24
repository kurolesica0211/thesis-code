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
  AssignClass (a2cd4e41-37ce-4b21-b0f7-5d924c01dddf)
 Call ID: a2cd4e41-37ce-4b21-b0f7-5d924c01dddf
  Args:
    type: :Woman
    source: Maria_Carolina_of_Bourbon-Two_Sicilies
  AssignClass (683c6ccd-322f-4785-ac14-cb80e8e6d957)
 Call ID: 683c6ccd-322f-4785-ac14-cb80e8e6d957
  Args:
    type: :Person
    source: Maria_Carolina_of_Bourbon-Two_Sicilies
  AddLiteral (0ee58369-1365-447c-a964-89d84e36d2d5)
 Call ID: 0ee58369-1365-447c-a964-89d84e36d2d5
  Args:
    source: Maria_Carolina_of_Bourbon-Two_Sicilies
    literal_type: xsd:date
    relation: :hasBirthYear
    literal_value: 2003-06-23
  AssignClass (9ea8b805-4f4f-4289-873f-a39798ed8e5a)
 Call ID: 9ea8b805-4f4f-4289-873f-a39798ed8e5a
  Args:
    type: :Man
    source: Carlo_of_Bourbon-Two_Sicilies
  AssignClass (edd00f8d-81a2-463a-9b6f-f64019da8f35)
 Call ID: edd00f8d-81a2-463a-9b6f-f64019da8f35
  Args:
    type: :Ancestor
    source: Carlo_of_Bourbon-Two_Sicilies
  AssignClass (f14758bf-86b9-4319-9ea0-60ff76125dc7)
 Call ID: f14758bf-86b9-4319-9ea0-60ff76125dc7
  Args:
    type: :Person
    source: Carlo_of_Bourbon-Two_Sicilies
  AssignClass (2f668ab0-d082-41cd-b80f-75aca0c82e6c)
 Call ID: 2f668ab0-d082-41cd-b80f-75aca0c82e6c
  Args:
    type: :Woman
    source: Camilla_Crociani
  AssignClass (c397f397-a009-4764-8ff6-c6a0da7ccb2c)
 Call ID: c397f397-a009-4764-8ff6-c6a0da7ccb2c
  Args:
    type: :Ancestor
    source: Camilla_Crociani
  AssignClass (ed33b858-97bc-4cf0-a520-33b269b9d709)
 Call ID: ed33b858-97bc-4cf0-a520-33b269b9d709
  Args:
    type: :Person
    source: Camilla_Crociani
  AddTriple (39d18fa4-7755-4564-b4fd-4d52351e267b)
 Call ID: 39d18fa4-7755-4564-b4fd-4d52351e267b
  Args:
    source: Maria_Carolina_of_Bourbon-Two_Sicilies
    target: Carlo_of_Bourbon-Two_Sicilies
    relation: :hasFather
  AddTriple (13e173e4-3fa9-4a2a-b76d-90c8f44b14d3)
 Call ID: 13e173e4-3fa9-4a2a-b76d-90c8f44b14d3
  Args:
    relation: :hasMother
    target: Camilla_Crociani
    source: Maria_Carolina_of_Bourbon-Two_Sicilies
  AssignClass (0376f99e-cdbf-4043-aecf-5fab0779aaf5)
 Call ID: 0376f99e-cdbf-4043-aecf-5fab0779aaf5
  Args:
    type: :Man
    source: Ferdinand_of_Bourbon-Two_Sicilies
  AssignClass (f09c7d8b-9500-45d7-bdf4-fd00b31a136a)
 Call ID: f09c7d8b-9500-45d7-bdf4-fd00b31a136a
  Args:
    type: :Ancestor
    source: Ferdinand_of_Bourbon-Two_Sicilies
  AssignClass (42c38ee0-4f09-4398-acfc-481cd009354a)
 Call ID: 42c38ee0-4f09-4398-acfc-481cd009354a
  Args:
    type: :Person
    source: Ferdinand_of_Bourbon-Two_Sicilies
  AddTriple (e0674123-e3e9-469e-b23c-6e5d7c3a66ee)
 Call ID: e0674123-e3e9-469e-b23c-6e5d7c3a66ee
  Args:
    relation: :hasFather
    target: Ferdinand_of_Bourbon-Two_Sicilies
    source: Carlo_of_Bourbon-Two_Sicilies
  AssignClass (84970180-1985-422f-8506-f5dd892ac1bc)
 Call ID: 84970180-1985-422f-8506-f5dd892ac1bc
  Args:
    type: :Woman
    source: Maria_Chiara_of_Bourbon-Two_Sicilies
  AssignClass (40531c60-e1ef-47e1-83d5-019419846800)
 Call ID: 40531c60-e1ef-47e1-83d5-019419846800
  Args:
    type: :Person
    source: Maria_Chiara_of_Bourbon-Two_Sicilies
  AddTriple (e6825021-8799-4ef3-905c-132038c5cc0f)
 Call ID: e6825021-8799-4ef3-905c-132038c5cc0f
  Args:
    target: Maria_Chiara_of_Bourbon-Two_Sicilies
    relation: :hasSister
    source: Maria_Carolina_of_Bourbon-Two_Sicilies
  AssignClass (0866efb0-7d3d-457c-878b-b77bef40bf0e)
 Call ID: 0866efb0-7d3d-457c-878b-b77bef40bf0e
  Args:
    type: :Woman
    source: Beatrice_of_Bourbon-Two_Sicilies
  AssignClass (d1d07a21-95c0-47b1-9ddf-039c11efaaf5)
 Call ID: d1d07a21-95c0-47b1-9ddf-039c11efaaf5
  Args:
    type: :Person
    source: Beatrice_of_Bourbon-Two_Sicilies
  AddTriple (639776b2-5429-401b-9bb2-d4723448eb2b)
 Call ID: 639776b2-5429-401b-9bb2-d4723448eb2b
  Args:
    target: Beatrice_of_Bourbon-Two_Sicilies
    relation: :hasSister
    source: Carlo_of_Bourbon-Two_Sicilies
  AssignClass (4cbf91c7-a1ca-4be3-85fc-92a72fda5d34)
 Call ID: 4cbf91c7-a1ca-4be3-85fc-92a72fda5d34
  Args:
    type: :Man
    source: Jean-Christophe_Prince_Napoleon
  AssignClass (d343a679-a433-411b-ae95-4f712960c0e1)
 Call ID: d343a679-a433-411b-ae95-4f712960c0e1
  Args:
    type: :Person
    source: Jean-Christophe_Prince_Napoleon
  AddTriple (0bb105b4-7170-48dc-ab61-afb8e47d7bdd)
 Call ID: 0bb105b4-7170-48dc-ab61-afb8e47d7bdd
  Args:
    relation: :hasRelation
    target: Jean-Christophe_Prince_Napoleon
    source: Maria_Carolina_of_Bourbon-Two_Sicilies
  AssignClass (c290c62b-ef96-4e54-8eed-0f4e83ae2463)
 Call ID: c290c62b-ef96-4e54-8eed-0f4e83ae2463
  Args:
    type: :Man
    source: Laurent_of_Belgium
  AssignClass (54cc5495-8493-436e-957f-95fe5508a9d8)
 Call ID: 54cc5495-8493-436e-957f-95fe5508a9d8
  Args:
    type: :Person
    source: Laurent_of_Belgium
  AssignClass (ce97492b-e4f5-48c6-be35-3168a50fc04b)
 Call ID: ce97492b-e4f5-48c6-be35-3168a50fc04b
  Args:
    type: :Man
    source: Philippe_of_Belgium
  AssignClass (92aa32be-246b-4427-a33a-af541835dec1)
 Call ID: 92aa32be-246b-4427-a33a-af541835dec1
  Args:
    type: :Person
    source: Philippe_of_Belgium
  AddTriple (84dd16a8-6f69-4ad8-8ec4-862bf897b423)
 Call ID: 84dd16a8-6f69-4ad8-8ec4-862bf897b423
  Args:
    source: Philippe_of_Belgium
    relation: :hasBrother
    target: Laurent_of_Belgium
  AssignClass (a804b08f-f3d0-4916-8050-54824ea9756f)
 Call ID: a804b08f-f3d0-4916-8050-54824ea9756f
  Args:
    type: :Man
    source: Leopold_of_Nassau
  AssignClass (c7cd683b-10ba-4b21-9f68-8638a2c5ae12)
 Call ID: c7cd683b-10ba-4b21-9f68-8638a2c5ae12
  Args:
    type: :Person
    source: Leopold_of_Nassau
  AssignClass (0655c880-d949-4245-b81e-5056ec37fa80)
 Call ID: 0655c880-d949-4245-b81e-5056ec37fa80
  Args:
    type: :Man
    source: Guillaume_of_Luxembourg
  AssignClass (0f12e0ba-0aad-457b-8b83-1fe325312d03)
 Call ID: 0f12e0ba-0aad-457b-8b83-1fe325312d03
  Args:
    type: :Person
    source: Guillaume_of_Luxembourg
  AddTriple (21cf5600-c069-4c48-a643-bef21836050c)
 Call ID: 21cf5600-c069-4c48-a643-bef21836050c
  Args:
    source: Leopold_of_Nassau
    target: Guillaume_of_Luxembourg
    relation: :hasFather
  Finish (de5a3e57-8b80-4193-80d3-adbb484c442f)
 Call ID: de5a3e57-8b80-4193-80d3-adbb484c442f
  Args: