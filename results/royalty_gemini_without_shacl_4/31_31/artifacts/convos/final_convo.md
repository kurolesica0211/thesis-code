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
  AssignClass (04c81435-6044-4c80-9dd8-a1c55d90de5b)
 Call ID: 04c81435-6044-4c80-9dd8-a1c55d90de5b
  Args:
    type: :Man
    source: Christoph_of_Schleswig-Holstein
  AssignClass (ec735e1b-184b-4140-b988-af7e69910823)
 Call ID: ec735e1b-184b-4140-b988-af7e69910823
  Args:
    type: :Person
    source: Christoph_of_Schleswig-Holstein
  AddLiteral (b2ade2b4-3d4c-46dd-b051-0e58886d6498)
 Call ID: b2ade2b4-3d4c-46dd-b051-0e58886d6498
  Args:
    literal_type: xsd:integer
    literal_value: 1949
    relation: :hasBirthYear
    source: Christoph_of_Schleswig-Holstein
  AddLiteral (6aaac966-c5d2-401f-827c-3b36704a1411)
 Call ID: 6aaac966-c5d2-401f-827c-3b36704a1411
  Args:
    source: Christoph_of_Schleswig-Holstein
    relation: :hasDeathYear
    literal_value: 2023
    literal_type: xsd:integer
  AddLiteral (d401c933-6e03-49c8-b37a-03069c58e440)
 Call ID: d401c933-6e03-49c8-b37a-03069c58e440
  Args:
    literal_value: Christoph Prinz zu Schleswig-Holstein
    relation: :alsoKnownAs
    source: Christoph_of_Schleswig-Holstein
    literal_type: xsd:string
  AssignClass (f5130e47-8a83-4159-8a0c-4c39c345436b)
 Call ID: f5130e47-8a83-4159-8a0c-4c39c345436b
  Args:
    type: :Man
    source: Peter_Duke_of_Schleswig-Holstein
  AssignClass (d4204fc5-c74a-4093-80fd-5f4b6e898d29)
 Call ID: d4204fc5-c74a-4093-80fd-5f4b6e898d29
  Args:
    type: :Person
    source: Peter_Duke_of_Schleswig-Holstein
  AddLiteral (80cd45d3-1a2e-44db-9e7f-e6809c22a7f1)
 Call ID: 80cd45d3-1a2e-44db-9e7f-e6809c22a7f1
  Args:
    source: Peter_Duke_of_Schleswig-Holstein
    relation: :hasBirthYear
    literal_value: 1922
    literal_type: xsd:integer
  AddLiteral (644b564c-194d-4f25-9b27-4fe96113091a)
 Call ID: 644b564c-194d-4f25-9b27-4fe96113091a
  Args:
    literal_value: 1980
    relation: :hasDeathYear
    source: Peter_Duke_of_Schleswig-Holstein
    literal_type: xsd:integer
  AddTriple (3cbf1ba7-9689-4a67-acad-0057e33a7365)
 Call ID: 3cbf1ba7-9689-4a67-acad-0057e33a7365
  Args:
    relation: :hasFather
    target: Peter_Duke_of_Schleswig-Holstein
    source: Christoph_of_Schleswig-Holstein
  AssignClass (b20cdfcf-e50e-4fc4-ad92-db798e3ad1d7)
 Call ID: b20cdfcf-e50e-4fc4-ad92-db798e3ad1d7
  Args:
    source: Princess_Marie_Alix_of_Schaumburg-Lippe
    type: :Woman
  AssignClass (97d507e0-19d6-4997-ba44-e5b4a1367632)
 Call ID: 97d507e0-19d6-4997-ba44-e5b4a1367632
  Args:
    source: Princess_Marie_Alix_of_Schaumburg-Lippe
    type: :Person
  AddLiteral (4fb6ed7f-ab59-473b-87cf-84169dbc13e3)
 Call ID: 4fb6ed7f-ab59-473b-87cf-84169dbc13e3
  Args:
    literal_type: xsd:integer
    literal_value: 1923
    relation: :hasBirthYear
    source: Princess_Marie_Alix_of_Schaumburg-Lippe
  AddLiteral (61e88e5e-9c19-494a-8d24-6a49eb52fdbe)
 Call ID: 61e88e5e-9c19-494a-8d24-6a49eb52fdbe
  Args:
    literal_type: xsd:integer
    source: Princess_Marie_Alix_of_Schaumburg-Lippe
    relation: :hasDeathYear
    literal_value: 2021
  AddTriple (84b58678-d017-45f6-b401-900e1dbb2124)
 Call ID: 84b58678-d017-45f6-b401-900e1dbb2124
  Args:
    relation: :hasMother
    source: Christoph_of_Schleswig-Holstein
    target: Princess_Marie_Alix_of_Schaumburg-Lippe
  AssignClass (85202c6a-c88b-473e-84d9-b41116b3c8cf)
 Call ID: 85202c6a-c88b-473e-84d9-b41116b3c8cf
  Args:
    source: Princess_Elisabeth_of_Lippe-Weissenfeld
    type: :Woman
  AssignClass (6355dce5-65b7-4ca4-a0e1-07b60a659c98)
 Call ID: 6355dce5-65b7-4ca4-a0e1-07b60a659c98
  Args:
    source: Princess_Elisabeth_of_Lippe-Weissenfeld
    type: :Person
  AddLiteral (f6700b8a-c29f-4e86-950d-86a2f56d71e8)
 Call ID: f6700b8a-c29f-4e86-950d-86a2f56d71e8
  Args:
    relation: :hasBirthYear
    source: Princess_Elisabeth_of_Lippe-Weissenfeld
    literal_value: 1957
    literal_type: xsd:integer
  AddTriple (cf9e44c6-91fc-4d68-9a49-9824929d77bd)
 Call ID: cf9e44c6-91fc-4d68-9a49-9824929d77bd
  Args:
    source: Christoph_of_Schleswig-Holstein
    target: Princess_Elisabeth_of_Lippe-Weissenfeld
    relation: :hasRelation
  AssignClass (2af91158-ad7b-439e-ade9-d119cf1f2784)
 Call ID: 2af91158-ad7b-439e-ade9-d119cf1f2784
  Args:
    source: Prince_Alfred_Karl_Friedrich_Georg_Franz_of_Lippe-Weissenfeld
    type: :Man
  AssignClass (af1b1387-50a8-44a6-82b3-b26b8712e000)
 Call ID: af1b1387-50a8-44a6-82b3-b26b8712e000
  Args:
    source: Prince_Alfred_Karl_Friedrich_Georg_Franz_of_Lippe-Weissenfeld
    type: :Person
  AddLiteral (e2a8d7e0-e942-4c64-85b6-63c5da7a094d)
 Call ID: e2a8d7e0-e942-4c64-85b6-63c5da7a094d
  Args:
    source: Prince_Alfred_Karl_Friedrich_Georg_Franz_of_Lippe-Weissenfeld
    relation: :hasBirthYear
    literal_value: 1922
    literal_type: xsd:integer
  AddLiteral (af3ed681-3809-49b4-a467-819589130602)
 Call ID: af3ed681-3809-49b4-a467-819589130602
  Args:
    source: Prince_Alfred_Karl_Friedrich_Georg_Franz_of_Lippe-Weissenfeld
    relation: :hasDeathYear
    literal_value: 2024
    literal_type: xsd:integer
  AddTriple (1de5d24c-b1ca-4679-a780-020edc0e12c6)
 Call ID: 1de5d24c-b1ca-4679-a780-020edc0e12c6
  Args:
    target: Prince_Alfred_Karl_Friedrich_Georg_Franz_of_Lippe-Weissenfeld
    source: Princess_Elisabeth_of_Lippe-Weissenfeld
    relation: :hasFather
  AssignClass (1dbae682-1e06-4ce8-ba94-ad20eb0d4ea1)
 Call ID: 1dbae682-1e06-4ce8-ba94-ad20eb0d4ea1
  Args:
    type: :Woman
    source: Baroness_Irmgard_Julinka_Wagner_von_Wehrborn
  AssignClass (3a11f3d5-716e-4ab9-9982-f56dadd4f689)
 Call ID: 3a11f3d5-716e-4ab9-9982-f56dadd4f689
  Args:
    source: Baroness_Irmgard_Julinka_Wagner_von_Wehrborn
    type: :Person
  AddLiteral (490d75a4-a008-453c-bd19-688ee6b08eef)
 Call ID: 490d75a4-a008-453c-bd19-688ee6b08eef
  Args:
    literal_type: xsd:integer
    literal_value: 1928
    source: Baroness_Irmgard_Julinka_Wagner_von_Wehrborn
    relation: :hasBirthYear
  AddTriple (27fea3db-de71-4f58-82d2-46e524739fd7)
 Call ID: 27fea3db-de71-4f58-82d2-46e524739fd7
  Args:
    source: Princess_Elisabeth_of_Lippe-Weissenfeld
    target: Baroness_Irmgard_Julinka_Wagner_von_Wehrborn
    relation: :hasMother
  Finish (bcf4b88b-7723-47ab-be20-ab77fae4e59f)
 Call ID: bcf4b88b-7723-47ab-be20-ab77fae4e59f
  Args: