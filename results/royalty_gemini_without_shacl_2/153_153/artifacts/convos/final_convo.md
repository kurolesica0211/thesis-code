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
Princess María de las Mercedes of Bourbon-Two Sicilies (.mw-parser-output .IPA-label-small{font-size:85%}.mw-parser-output .references .IPA-label-small,.mw-parser-output .infobox .IPA-label-small,.mw-parser-output .navbox .IPA-label-small{font-size:100%}Spanish: ; María de las Mercedes Cristina Genara Isabel Luisa Carolina Victoria y Todos los Santos de Borbón y Orléans; 23 December 1910 – 2 January 2000) was a member of the Spanish royal family and the mother of King Juan Carlos I.


The daughter of Prince Carlos of Bourbon-Two Sicilies and Princess Louise of Orléans, she married Infante Juan, Count of Barcelona, claimant to the Spanish throne.
Biography

María was born in Madrid, daughter of Prince Carlos of Bourbon-Two Sicilies, Infante of Spain, a grandson of King Ferdinand II of the Two Sicilies, and his second wife, Princess Louise of Orléans, daughter of Prince Philippe, Count of Paris, a pretender to the French throne.
She was granted, at birth, the rank and precedence of an infanta of Spain, although not the actual use of the title, her own being Princess of Bourbon-Two Sicilies.
When the Second Spanish Republic forced them into exile, they lived in Cannes and later in Paris, where she studied art at the Louvre.
On 14 January 1935, she attended the wedding, in Rome, of Infanta Beatriz of Spain, daughter of King Alfonso XIII, to Alessandro Torlonia, 5th Prince of Civitella-Cesi.
There she met the brother of the bride, her third cousin and future husband, the Infante Juan, fourth son and designated heir of Alfonso XIII.
When her husband took up Count of Barcelona as a title of pretence on 8 March 1941, María became the Countess of Barcelona.
They lived in Cannes and Rome, and, with the outbreak of World War II, they moved to Lausanne to live with Queen Victoria Eugenie, the mother of Infante Juan.
In 1953, the Countess represented the Spanish Royal Family at the coronation of Queen Elizabeth II.
In 1976, one year after the monarchy was restored in Spain in the person of her son, Juan Carlos, they returned to Spain.
She mediated between her son and her husband, estranged since Juan Carlos had been designated heir by Franco.
In 1977, Juan renounced his rights in favour of their son, who officially allowed him to retain the title of Count of Barcelona.
In 1995, her granddaughter Infanta Elena married in Seville in part because the Countess' love for the city.



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
  AssignClass (980fd617-1395-4d6c-850d-e2b73cbc4699)
 Call ID: 980fd617-1395-4d6c-850d-e2b73cbc4699
  Args:
    source: María de las Mercedes of Bourbon-Two Sicilies
    type: :Woman
  AssignClass (f09a9724-bbfb-48ad-b714-2c723e7ad0b6)
 Call ID: f09a9724-bbfb-48ad-b714-2c723e7ad0b6
  Args:
    source: María de las Mercedes of Bourbon-Two Sicilies
    type: :Person
  AddLiteral (b29204b5-8946-46d2-bc24-78550f445b6d)
 Call ID: b29204b5-8946-46d2-bc24-78550f445b6d
  Args:
    literal_type: xsd:positiveInteger
    literal_value: 1910
    source: María de las Mercedes of Bourbon-Two Sicilies
    relation: :hasBirthYear
  AddLiteral (d0c08e8b-bfb7-4b73-a889-ecae7624bd59)
 Call ID: d0c08e8b-bfb7-4b73-a889-ecae7624bd59
  Args:
    relation: :hasDeathYear
    source: María de las Mercedes of Bourbon-Two Sicilies
    literal_value: 2000
    literal_type: xsd:positiveInteger
  AssignClass (9b8d2d03-f2cd-4d93-a887-d290069d0e8a)
 Call ID: 9b8d2d03-f2cd-4d93-a887-d290069d0e8a
  Args:
    type: :Man
    source: Juan Carlos I
  AssignClass (c83723ee-33b1-46e5-ab80-e8fe83f26d9c)
 Call ID: c83723ee-33b1-46e5-ab80-e8fe83f26d9c
  Args:
    type: :Person
    source: Juan Carlos I
  AddTriple (70701b5c-2336-46cd-aea8-3ca8bea81d38)
 Call ID: 70701b5c-2336-46cd-aea8-3ca8bea81d38
  Args:
    target: Juan Carlos I
    relation: :isMotherOf
    source: María de las Mercedes of Bourbon-Two Sicilies
  AssignClass (107ec737-f114-4b36-90d5-187d203ad00c)
 Call ID: 107ec737-f114-4b36-90d5-187d203ad00c
  Args:
    type: :Man
    source: Carlos of Bourbon-Two Sicilies
  AssignClass (7ce22bd1-522b-436a-acb8-6f77a9db8c87)
 Call ID: 7ce22bd1-522b-436a-acb8-6f77a9db8c87
  Args:
    source: Carlos of Bourbon-Two Sicilies
    type: :Person
  AssignClass (4f97d760-76b7-4801-aa9d-5c16fc51e295)
 Call ID: 4f97d760-76b7-4801-aa9d-5c16fc51e295
  Args:
    source: Louise of Orléans
    type: :Woman
  AssignClass (a074168c-604e-47f0-9f58-3a5bf9f9adce)
 Call ID: a074168c-604e-47f0-9f58-3a5bf9f9adce
  Args:
    source: Louise of Orléans
    type: :Person
  AddTriple (893c3016-558e-4c09-8215-df31bc487201)
 Call ID: 893c3016-558e-4c09-8215-df31bc487201
  Args:
    target: Carlos of Bourbon-Two Sicilies
    relation: :hasFather
    source: María de las Mercedes of Bourbon-Two Sicilies
  AddTriple (ebd9a35a-c960-4c49-b943-f638920a0f27)
 Call ID: ebd9a35a-c960-4c49-b943-f638920a0f27
  Args:
    target: Louise of Orléans
    relation: :hasMother
    source: María de las Mercedes of Bourbon-Two Sicilies
  AssignClass (9ff78076-7784-4cf8-a8c8-880446f05352)
 Call ID: 9ff78076-7784-4cf8-a8c8-880446f05352
  Args:
    type: :Man
    source: Juan, Count of Barcelona
  AssignClass (92e78a47-6e21-4a1a-a5f1-b4cdf94060f8)
 Call ID: 92e78a47-6e21-4a1a-a5f1-b4cdf94060f8
  Args:
    type: :Person
    source: Juan, Count of Barcelona
  AddTriple (914e26eb-ae8b-4496-8a0a-c182367fd35b)
 Call ID: 914e26eb-ae8b-4496-8a0a-c182367fd35b
  Args:
    relation: :hasRelation
    target: Juan, Count of Barcelona
    source: María de las Mercedes of Bourbon-Two Sicilies
  AssignClass (c8be5a2a-4e1d-4d35-8f9c-39d08cae5be7)
 Call ID: c8be5a2a-4e1d-4d35-8f9c-39d08cae5be7
  Args:
    type: :Man
    source: Ferdinand II of the Two Sicilies
  AssignClass (8a24bc6c-9bfc-4bb7-8ff0-e4d6d3ccead1)
 Call ID: 8a24bc6c-9bfc-4bb7-8ff0-e4d6d3ccead1
  Args:
    source: Ferdinand II of the Two Sicilies
    type: :Person
  AddTriple (00557f90-1897-441a-bed2-04feda808d4f)
 Call ID: 00557f90-1897-441a-bed2-04feda808d4f
  Args:
    source: Ferdinand II of the Two Sicilies
    target: Carlos of Bourbon-Two Sicilies
    relation: :isFatherOf
  AssignClass (38e1eb31-8242-4969-88a0-0b60e80ff8ec)
 Call ID: 38e1eb31-8242-4969-88a0-0b60e80ff8ec
  Args:
    type: :Man
    source: Philippe, Count of Paris
  AssignClass (55923ff8-16ce-4cd2-b898-ce38c54e2bea)
 Call ID: 55923ff8-16ce-4cd2-b898-ce38c54e2bea
  Args:
    source: Philippe, Count of Paris
    type: :Person
  AddTriple (5593d492-8dff-4743-89e1-1dd0100d0272)
 Call ID: 5593d492-8dff-4743-89e1-1dd0100d0272
  Args:
    relation: :isFatherOf
    target: Louise of Orléans
    source: Philippe, Count of Paris
  AssignClass (3f3c96b7-b39b-4427-bb57-ed23f481cf53)
 Call ID: 3f3c96b7-b39b-4427-bb57-ed23f481cf53
  Args:
    source: Beatriz of Spain
    type: :Woman
  AssignClass (41b2194d-fc88-497a-b586-9305d51e2913)
 Call ID: 41b2194d-fc88-497a-b586-9305d51e2913
  Args:
    source: Beatriz of Spain
    type: :Person
  AssignClass (98b5aa7e-c84d-465c-b37b-2f276a825a3a)
 Call ID: 98b5aa7e-c84d-465c-b37b-2f276a825a3a
  Args:
    source: Alfonso XIII
    type: :Man
  AssignClass (9d146ce3-29c2-4381-90af-03f629cbdc6a)
 Call ID: 9d146ce3-29c2-4381-90af-03f629cbdc6a
  Args:
    type: :Person
    source: Alfonso XIII
  AddTriple (c045b85c-6555-43dc-83b7-a0a2b5590c0b)
 Call ID: c045b85c-6555-43dc-83b7-a0a2b5590c0b
  Args:
    source: Alfonso XIII
    relation: :isFatherOf
    target: Beatriz of Spain
  AddTriple (baf12d7b-53ca-4c01-b99b-956edf4d5565)
 Call ID: baf12d7b-53ca-4c01-b99b-956edf4d5565
  Args:
    source: Alfonso XIII
    target: Juan, Count of Barcelona
    relation: :isFatherOf
  AssignClass (3d1b7dcb-336c-47a4-b4d3-2099046b837e)
 Call ID: 3d1b7dcb-336c-47a4-b4d3-2099046b837e
  Args:
    type: :Man
    source: Alessandro Torlonia
  AssignClass (edb5bdd4-2b2f-448d-a7f1-4af56e729d61)
 Call ID: edb5bdd4-2b2f-448d-a7f1-4af56e729d61
  Args:
    type: :Person
    source: Alessandro Torlonia
  AssignClass (9b414754-40e5-472b-a5d4-36fa300c166d)
 Call ID: 9b414754-40e5-472b-a5d4-36fa300c166d
  Args:
    source: Victoria Eugenie
    type: :Woman
  AssignClass (c6d791dd-c737-44c2-8db2-936adb70a36f)
 Call ID: c6d791dd-c737-44c2-8db2-936adb70a36f
  Args:
    type: :Person
    source: Victoria Eugenie
  AddTriple (cd5f036a-6918-4053-8ace-4b58a1ec8f8f)
 Call ID: cd5f036a-6918-4053-8ace-4b58a1ec8f8f
  Args:
    source: Victoria Eugenie
    target: Juan, Count of Barcelona
    relation: :isMotherOf
  AssignClass (b84066f4-99cc-4af6-a1e6-358e5852b041)
 Call ID: b84066f4-99cc-4af6-a1e6-358e5852b041
  Args:
    source: Elena of Spain
    type: :Woman
  AssignClass (9fe85ca1-8c4d-4eb9-a5e4-c7bfd5e5822f)
 Call ID: 9fe85ca1-8c4d-4eb9-a5e4-c7bfd5e5822f
  Args:
    type: :Person
    source: Elena of Spain
  AddTriple (16eb68bf-3b02-4509-a591-b502dadd0805)
 Call ID: 16eb68bf-3b02-4509-a591-b502dadd0805
  Args:
    target: Elena of Spain
    relation: :isMotherOf
    source: Juan Carlos I
  Finish (747f2a02-e1bb-4cae-85c6-529aa40c548a)
 Call ID: 747f2a02-e1bb-4cae-85c6-529aa40c548a
  Args: