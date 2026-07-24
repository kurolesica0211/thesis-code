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
Paul Dmitrievich Romanovsky-Ilyinsky (January 27, 1928 – February 10, 2004) was a three-time mayor of Palm Beach, Florida, and the only child of Grand Duke Dmitri Pavlovich of Russia and his morganatic wife, Cincinnati heiress Audrey Emery.
He was a great-grandson of Tsar Alexander II of Russia and, following the death of Grand Duke Vladimir Kirillovich in 1992, the heir-male of the Ilyinsky claim of the House of Romanov (a position now held by his elder son), a first cousin once removed of Nicholas II, first cousin of Prince Lennart of Sweden, Duke of Småland and the second cousin of Charles III.
Early life

Prince Paul Romanovsky-Ilyinsky was born on 27 January 1928 at his parents' home, 26 Manchester Square, London.
His father, Grand Duke Dmitri, as a direct consequence of his involvement in the murder of Grigori Rasputin in 1916, had been sent to the Persian front, which ultimately saved his life, as many of his Imperial relatives were executed by the Bolsheviks during the October Revolution .
Dmitri, who was working as a champagne salesman, married Cincinnati heiress Audrey Emery in 1926.
Grand Duke Cyril Vladimirovich of Russia, Dmitri's cousin and the self-proclaimed emperor in exile, elevated Grand Duke Dmitri's wife and their descendants to Russian princely (Russian: knyaz) rank (rank of nobility, not royalty).
Any children the couple would have would be known as Romanovsky-Ilyinsky, the latter half of the surname derived from Dmitri's former property in Russia, Ilinskoe.
Ilynskiy's parents were divorced in 1937, and Ilyinsky was raised by his mother, who mostly lived in France.
Dmitri Pavlovich's health had always been somewhat frail, and in the 1930s, his chronic tuberculosis became acute, leading to his death in 1942.
Education and career

Ilyinsky, who was a U.S. citizen, attended Woodberry Forest School in Virginia and the Royal Military Academy Sandhurst, England, before joining the U.S. Marine Corps.
Ilyinsky lived in Cincinnati for about 20 years, serving on the board of the company founded by his mother's family, Emery Industries, and working as an author and photographer.
Ilyinsky died at his home in Palm Beach, Florida, on February 10, 2004.
Personal life

Ilyinsky was married twice; he married his first wife, Mary Evelyn Prince in 1948 (annulment in 1951), and married his second wife, Angelica Philippa Kauffmann in 1953.
Ilyinsky had four children:


Ancestry

References



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
  AssignClass (32e9b0eb-cb75-483f-a68d-79cba067aa50)
 Call ID: 32e9b0eb-cb75-483f-a68d-79cba067aa50
  Args:
    type: :Man
    source: Paul_Dmitrievich_Romanovsky-Ilyinsky
  AssignClass (a5bdb685-c1c8-46fc-81b9-a3b85cb63f82)
 Call ID: a5bdb685-c1c8-46fc-81b9-a3b85cb63f82
  Args:
    type: :Person
    source: Paul_Dmitrievich_Romanovsky-Ilyinsky
  AddLiteral (7067656b-a751-4480-87a8-84a20c0f96d5)
 Call ID: 7067656b-a751-4480-87a8-84a20c0f96d5
  Args:
    literal_value: 1928
    source: Paul_Dmitrievich_Romanovsky-Ilyinsky
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (62da26e2-bd2d-40d6-90f7-3f19183caecb)
 Call ID: 62da26e2-bd2d-40d6-90f7-3f19183caecb
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: Paul_Dmitrievich_Romanovsky-Ilyinsky
    literal_value: 2004
  AssignClass (b7f23501-46c2-4c71-9251-f816117bdbe6)
 Call ID: b7f23501-46c2-4c71-9251-f816117bdbe6
  Args:
    type: :Man
    source: Dmitri_Pavlovich_of_Russia
  AssignClass (6b2da159-89cb-4d05-99c0-1dcedd2f4dae)
 Call ID: 6b2da159-89cb-4d05-99c0-1dcedd2f4dae
  Args:
    type: :Person
    source: Dmitri_Pavlovich_of_Russia
  AddLiteral (1f05f6c0-cf96-457d-bb09-09c913cbb188)
 Call ID: 1f05f6c0-cf96-457d-bb09-09c913cbb188
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: Dmitri_Pavlovich_of_Russia
    literal_value: 1942
  AssignClass (b9fe36fb-539c-456f-ae86-cda42de9ddf3)
 Call ID: b9fe36fb-539c-456f-ae86-cda42de9ddf3
  Args:
    type: :Woman
    source: Audrey_Emery
  AssignClass (7390087c-e362-4e86-a042-5ae28f7cd80a)
 Call ID: 7390087c-e362-4e86-a042-5ae28f7cd80a
  Args:
    type: :Person
    source: Audrey_Emery
  AddTriple (317e53e6-0f4f-4565-bd47-889c79778bca)
 Call ID: 317e53e6-0f4f-4565-bd47-889c79778bca
  Args:
    source: Paul_Dmitrievich_Romanovsky-Ilyinsky
    target: Dmitri_Pavlovich_of_Russia
    relation: :hasFather
  AddTriple (ec8b4683-b270-476d-ae8e-d67d89693d5a)
 Call ID: ec8b4683-b270-476d-ae8e-d67d89693d5a
  Args:
    relation: :hasMother
    target: Audrey_Emery
    source: Paul_Dmitrievich_Romanovsky-Ilyinsky
  AddLiteral (ac2bee32-9d5a-41e9-961d-f861f7ad588d)
 Call ID: ac2bee32-9d5a-41e9-961d-f861f7ad588d
  Args:
    relation: :hasMarriageYear
    literal_type: xsd:integer
    literal_value: 1926
    source: Dmitri_Pavlovich_of_Russia
  AddTriple (c8d900ae-33bc-499e-96d8-7de7798b69c3)
 Call ID: c8d900ae-33bc-499e-96d8-7de7798b69c3
  Args:
    relation: :hasRelation
    target: Audrey_Emery
    source: Dmitri_Pavlovich_of_Russia
  AssignClass (e0897e3a-4ef0-4ff7-84f8-0c334d44d65e)
 Call ID: e0897e3a-4ef0-4ff7-84f8-0c334d44d65e
  Args:
    type: :Woman
    source: Mary_Evelyn_Prince
  AssignClass (3bdf2dd2-a440-4f9a-b08b-de104dc6890f)
 Call ID: 3bdf2dd2-a440-4f9a-b08b-de104dc6890f
  Args:
    type: :Person
    source: Mary_Evelyn_Prince
  AddTriple (4e93de31-29e1-4800-9a9f-360fbe23d7f1)
 Call ID: 4e93de31-29e1-4800-9a9f-360fbe23d7f1
  Args:
    relation: :hasRelation
    source: Paul_Dmitrievich_Romanovsky-Ilyinsky
    target: Mary_Evelyn_Prince
  AddLiteral (2268f97f-b2d4-47b2-a166-7a30460d6427)
 Call ID: 2268f97f-b2d4-47b2-a166-7a30460d6427
  Args:
    source: Paul_Dmitrievich_Romanovsky-Ilyinsky
    literal_value: 1948
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AssignClass (1b5eb1e7-acfe-4009-8059-9d2c24c4c4ae)
 Call ID: 1b5eb1e7-acfe-4009-8059-9d2c24c4c4ae
  Args:
    type: :Woman
    source: Angelica_Philippa_Kauffmann
  AssignClass (6421d8a9-8c6c-423a-b8d5-864d44ec9736)
 Call ID: 6421d8a9-8c6c-423a-b8d5-864d44ec9736
  Args:
    type: :Person
    source: Angelica_Philippa_Kauffmann
  AddTriple (43db3d21-e551-4d97-97e5-3b39c0655f77)
 Call ID: 43db3d21-e551-4d97-97e5-3b39c0655f77
  Args:
    relation: :hasRelation
    target: Angelica_Philippa_Kauffmann
    source: Paul_Dmitrievich_Romanovsky-Ilyinsky
  AddLiteral (718ac538-3741-42d2-9c98-cd7ec9f0bb5f)
 Call ID: 718ac538-3741-42d2-9c98-cd7ec9f0bb5f
  Args:
    literal_value: 1953
    source: Paul_Dmitrievich_Romanovsky-Ilyinsky
    relation: :hasMarriageYear
    literal_type: xsd:integer
  Finish (5e201c9b-f1fa-4d2f-ac54-4ffd7498916b)
 Call ID: 5e201c9b-f1fa-4d2f-ac54-4ffd7498916b
  Args: