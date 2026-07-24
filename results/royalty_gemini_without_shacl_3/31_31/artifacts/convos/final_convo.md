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
Christoph of Schleswig-Holstein (22 August 1949 – 27 September 2023)
(German: Christoph Prinz zu Schleswig-Holstein) was the head of the House of Schleswig-Holstein-Sonderburg-Glücksburg (commonly known as the House of Glücksburg) and, by agnatic primogeniture, of the entire House of Oldenburg between 1980 and 2023.
Traditionally he would have been the eighth Duke of Schleswig-Holstein and Duke of Glücksburg, styled as His Highness.
House of Schleswig-Holstein-Sonderburg-Glücksburg

The House of Oldenburg — in one of its cadet branches — is patrilineally the royal house of Norway (1450–1818 and since 1905) and the United Kingdom (since 2022), and has been the reigning dynasty of several other countries including Denmark, Greece, Sweden and Russia.
As such, Christoph was the agnatic head of the family that today includes Harald V of Norway and, patrilineally, Charles III of the United Kingdom.
His great-great-grandfather, Friedrich, Duke of Schleswig-Holstein-Sonderburg-Glücksburg, was the older brother of Christian IX of Denmark, and through him Christoph is heir by male primogeniture to the Danish title Duke of Glücksburg (heir of the last extant ducal branch of the House of Schleswig-Holstein-Sonderburg) conferred by the Danish crown in 1825.
Christoph was also, cognatically, a descendant of Queen Victoria and Alexander II of Russia.
Life and activities

Christoph was born in Louisenlund Castle in Güby, near Eckernförde, Schleswig-Holstein, West Germany, the eldest son of Peter, Duke of Schleswig-Holstein (1922–1980), and his wife, Princess Marie Alix of Schaumburg-Lippe (1923-2021).
Christoph served as a Reservist in the German Army for two years, holding the rank of lieutenant.
Christoph succeeded to the headship of the ducal house on 30 September 1980 following the death of his father.
While possession of the united duchies of Schleswig and Holstein had been allocated by a series of wars and treaties since the First Schleswig War of 1848 and the London Protocol of 1852, the ducal title was borne by Christoph's father and paternal grandfather (as inherited from his great-grandfather, Friedrich Ferdinand, Duke of Schleswig-Holstein-Sonderburg-Glücksburg in 1934).
However, Christoph was known also by the title which is shared by male cadets of the dynasty, "Prinz zu (Prince of) Schleswig-Holstein-Sonderburg-Glücksburg".
From 1980 onward, Christoph chaired the board of the family foundation that owns the ancestral castle, Glücksburg Castle.
He was the owner of the Grünholz and Bienebek estates and was one of the largest landowners of Schleswig-Holstein.
Marriage and issue

Christoph married Princess Elisabeth of Lippe-Weissenfeld (b. 28 July 1957 in Munich), the youngest child of Prince Alfred Karl Friedrich Georg Franz of Lippe-Weissenfeld (1922-2024), who served as UNHCR representative for Italy, and his wife, Baroness Irmgard Julinka Wagner von Wehrborn (b. 1928).
They had four children: 


Death

Christoph died on 27 September 2023, at the age of 74, after a long-term illness.



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
  AssignClass (aa4be6a2-6c81-444c-a546-a067604d6ffe)
 Call ID: aa4be6a2-6c81-444c-a546-a067604d6ffe
  Args:
    type: :Man
    source: Christoph_of_Schleswig-Holstein
  AssignClass (bcaf7ebb-46af-40b4-9dce-fa005364414f)
 Call ID: bcaf7ebb-46af-40b4-9dce-fa005364414f
  Args:
    source: Christoph_of_Schleswig-Holstein
    type: :Person
  AddLiteral (c8bab737-9816-4ca3-a002-3f466b211f85)
 Call ID: c8bab737-9816-4ca3-a002-3f466b211f85
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1949
    source: Christoph_of_Schleswig-Holstein
  AddLiteral (69dda35f-a78a-449c-9869-4d62759723ee)
 Call ID: 69dda35f-a78a-449c-9869-4d62759723ee
  Args:
    source: Christoph_of_Schleswig-Holstein
    literal_value: 2023
    relation: :hasDeathYear
    literal_type: xsd:integer
  AddLiteral (46d8366d-1617-4416-9170-06b7795e5f00)
 Call ID: 46d8366d-1617-4416-9170-06b7795e5f00
  Args:
    source: Christoph_of_Schleswig-Holstein
    literal_value: Christoph Prinz zu Schleswig-Holstein
    relation: :knownAs
    literal_type: xsd:string
  AssignClass (6320533f-2b5d-4956-946b-94ecd9f9f858)
 Call ID: 6320533f-2b5d-4956-946b-94ecd9f9f858
  Args:
    type: :Man
    source: Peter_Duke_of_Schleswig-Holstein
  AssignClass (c87db9c8-c4a8-4d6a-8490-71a2a50a2434)
 Call ID: c87db9c8-c4a8-4d6a-8490-71a2a50a2434
  Args:
    source: Peter_Duke_of_Schleswig-Holstein
    type: :Person
  AddLiteral (c20b1154-4273-4ce7-a9d8-6c3c3849c09a)
 Call ID: c20b1154-4273-4ce7-a9d8-6c3c3849c09a
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1922
    source: Peter_Duke_of_Schleswig-Holstein
  AddLiteral (e913fc8c-eabc-4bdf-8b99-3436eaf55f19)
 Call ID: e913fc8c-eabc-4bdf-8b99-3436eaf55f19
  Args:
    source: Peter_Duke_of_Schleswig-Holstein
    literal_value: 1980
    relation: :hasDeathYear
    literal_type: xsd:integer
  AddTriple (cb62d9b2-4406-464f-b581-60fd8b9e942a)
 Call ID: cb62d9b2-4406-464f-b581-60fd8b9e942a
  Args:
    target: Peter_Duke_of_Schleswig-Holstein
    relation: :hasFather
    source: Christoph_of_Schleswig-Holstein
  AssignClass (b4d8ae96-8c86-4d1e-a7ae-a308102fa8ff)
 Call ID: b4d8ae96-8c86-4d1e-a7ae-a308102fa8ff
  Args:
    type: :Woman
    source: Princess_Marie_Alix_of_Schaumburg-Lippe
  AssignClass (8967fbea-af94-4925-8689-daff67202517)
 Call ID: 8967fbea-af94-4925-8689-daff67202517
  Args:
    type: :Person
    source: Princess_Marie_Alix_of_Schaumburg-Lippe
  AddLiteral (08b8d167-5aa6-46af-9e83-55756f0dcb44)
 Call ID: 08b8d167-5aa6-46af-9e83-55756f0dcb44
  Args:
    source: Princess_Marie_Alix_of_Schaumburg-Lippe
    literal_value: 1923
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (c7da6ad5-416a-49ba-a03b-fe7a80a8373a)
 Call ID: c7da6ad5-416a-49ba-a03b-fe7a80a8373a
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: Princess_Marie_Alix_of_Schaumburg-Lippe
    literal_value: 2021
  AddTriple (d2526ba3-f793-408c-a784-a78a7e34fea3)
 Call ID: d2526ba3-f793-408c-a784-a78a7e34fea3
  Args:
    source: Christoph_of_Schleswig-Holstein
    target: Princess_Marie_Alix_of_Schaumburg-Lippe
    relation: :hasMother
  AssignClass (e8906d4c-0f04-422d-846d-91c91744888c)
 Call ID: e8906d4c-0f04-422d-846d-91c91744888c
  Args:
    type: :Woman
    source: Princess_Elisabeth_of_Lippe-Weissenfeld
  AssignClass (0b254be8-84f4-4b34-b2a3-d033bd344424)
 Call ID: 0b254be8-84f4-4b34-b2a3-d033bd344424
  Args:
    source: Princess_Elisabeth_of_Lippe-Weissenfeld
    type: :Person
  AddLiteral (a65eb5de-597f-47db-9929-864bc81d9543)
 Call ID: a65eb5de-597f-47db-9929-864bc81d9543
  Args:
    literal_value: 1957
    source: Princess_Elisabeth_of_Lippe-Weissenfeld
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddTriple (983516c2-6bed-4b19-94f9-9c8ee85b63c8)
 Call ID: 983516c2-6bed-4b19-94f9-9c8ee85b63c8
  Args:
    target: Princess_Elisabeth_of_Lippe-Weissenfeld
    relation: :hasRelation
    source: Christoph_of_Schleswig-Holstein
  AssignClass (1e44c843-b3c0-47e9-babd-45265482e5b2)
 Call ID: 1e44c843-b3c0-47e9-babd-45265482e5b2
  Args:
    type: :Man
    source: Prince_Alfred_Karl_Friedrich_Georg_Franz_of_Lippe-Weissenfeld
  AssignClass (876cc9f0-865f-484f-82a9-fcd9567b79b1)
 Call ID: 876cc9f0-865f-484f-82a9-fcd9567b79b1
  Args:
    source: Prince_Alfred_Karl_Friedrich_Georg_Franz_of_Lippe-Weissenfeld
    type: :Person
  AddLiteral (def18950-2df3-44ce-952c-ff45262039b9)
 Call ID: def18950-2df3-44ce-952c-ff45262039b9
  Args:
    literal_value: 1922
    source: Prince_Alfred_Karl_Friedrich_Georg_Franz_of_Lippe-Weissenfeld
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (0357c12f-dd53-482a-8758-3fbcb614e1e1)
 Call ID: 0357c12f-dd53-482a-8758-3fbcb614e1e1
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 2024
    source: Prince_Alfred_Karl_Friedrich_Georg_Franz_of_Lippe-Weissenfeld
  AddTriple (d595d198-b550-4c55-816a-dbb8610f0b95)
 Call ID: d595d198-b550-4c55-816a-dbb8610f0b95
  Args:
    target: Prince_Alfred_Karl_Friedrich_Georg_Franz_of_Lippe-Weissenfeld
    relation: :hasFather
    source: Princess_Elisabeth_of_Lippe-Weissenfeld
  AssignClass (b68b235f-749c-451c-900b-0dda3415a04c)
 Call ID: b68b235f-749c-451c-900b-0dda3415a04c
  Args:
    source: Baroness_Irmgard_Julinka_Wagner_von_Wehrborn
    type: :Woman
  AssignClass (eb7ba672-7a2c-434f-a28c-c1d21280d7d1)
 Call ID: eb7ba672-7a2c-434f-a28c-c1d21280d7d1
  Args:
    source: Baroness_Irmgard_Julinka_Wagner_von_Wehrborn
    type: :Person
  AddLiteral (6562634d-5bd8-4daa-b780-778768653b9a)
 Call ID: 6562634d-5bd8-4daa-b780-778768653b9a
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Baroness_Irmgard_Julinka_Wagner_von_Wehrborn
    literal_value: 1928
  AddTriple (722b433f-2900-4b68-a0b3-b3b206e32057)
 Call ID: 722b433f-2900-4b68-a0b3-b3b206e32057
  Args:
    source: Princess_Elisabeth_of_Lippe-Weissenfeld
    target: Baroness_Irmgard_Julinka_Wagner_von_Wehrborn
    relation: :hasMother
  AssignClass (7370ad5d-680c-4251-8cc3-7eed0f723e92)
 Call ID: 7370ad5d-680c-4251-8cc3-7eed0f723e92
  Args:
    type: :Man
    source: Friedrich_Duke_of_Schleswig-Holstein-Sonderburg-Glücksburg
  AssignClass (12f9cf55-ebf7-4863-a640-aeea08c6932b)
 Call ID: 12f9cf55-ebf7-4863-a640-aeea08c6932b
  Args:
    type: :Person
    source: Friedrich_Duke_of_Schleswig-Holstein-Sonderburg-Glücksburg
  AssignClass (5f1de8bc-9cde-4066-aa51-311c3305ac0a)
 Call ID: 5f1de8bc-9cde-4066-aa51-311c3305ac0a
  Args:
    type: :Man
    source: Christian_IX_of_Denmark
  AssignClass (e982c172-d7db-4897-b525-0823e6a9d033)
 Call ID: e982c172-d7db-4897-b525-0823e6a9d033
  Args:
    source: Christian_IX_of_Denmark
    type: :Person
  AddTriple (6edcdcaf-b401-4802-be51-a431e2e80915)
 Call ID: 6edcdcaf-b401-4802-be51-a431e2e80915
  Args:
    source: Friedrich_Duke_of_Schleswig-Holstein-Sonderburg-Glücksburg
    relation: :hasBrother
    target: Christian_IX_of_Denmark
  Finish (a5b45496-335b-47e2-8619-2768b113d3d4)
 Call ID: a5b45496-335b-47e2-8619-2768b113d3d4
  Args: