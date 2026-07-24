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
  AssignClass (a9be5736-6dd0-409d-9ce3-46991be8b0d7)
 Call ID: a9be5736-6dd0-409d-9ce3-46991be8b0d7
  Args:
    type: :Man
    source: Christoph_of_Schleswig-Holstein
  AssignClass (cd9ddaa9-3f93-4aeb-9c07-46e78a1ab352)
 Call ID: cd9ddaa9-3f93-4aeb-9c07-46e78a1ab352
  Args:
    source: Christoph_of_Schleswig-Holstein
    type: :Person
  AddLiteral (1bad1e28-2ab9-4162-9aad-1f86a999f7bc)
 Call ID: 1bad1e28-2ab9-4162-9aad-1f86a999f7bc
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1949
    source: Christoph_of_Schleswig-Holstein
  AddLiteral (64125678-33b3-43be-9360-c0c55af25488)
 Call ID: 64125678-33b3-43be-9360-c0c55af25488
  Args:
    source: Christoph_of_Schleswig-Holstein
    literal_value: 2023
    literal_type: xsd:integer
    relation: :hasDeathYear
  AssignClass (9ba1bf54-b0d2-4d0a-b1ff-34393b05e1f8)
 Call ID: 9ba1bf54-b0d2-4d0a-b1ff-34393b05e1f8
  Args:
    type: :Man
    source: Peter_Duke_of_Schleswig-Holstein
  AssignClass (613f431d-5b32-4a76-9e7a-0e602c25561a)
 Call ID: 613f431d-5b32-4a76-9e7a-0e602c25561a
  Args:
    source: Peter_Duke_of_Schleswig-Holstein
    type: :Person
  AddLiteral (a36a37b6-82ac-49c7-ba17-fc06a49c87ef)
 Call ID: a36a37b6-82ac-49c7-ba17-fc06a49c87ef
  Args:
    source: Peter_Duke_of_Schleswig-Holstein
    literal_value: 1922
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (2bfd01d8-0ef1-4521-b9fa-0213dddcb15b)
 Call ID: 2bfd01d8-0ef1-4521-b9fa-0213dddcb15b
  Args:
    source: Peter_Duke_of_Schleswig-Holstein
    literal_value: 1980
    literal_type: xsd:integer
    relation: :hasDeathYear
  AssignClass (76966177-159e-403f-97c5-f701050eaeaa)
 Call ID: 76966177-159e-403f-97c5-f701050eaeaa
  Args:
    type: :Woman
    source: Princess_Marie_Alix_of_Schaumburg-Lippe
  AssignClass (690dd152-1381-41a4-9243-30d3eb061ab3)
 Call ID: 690dd152-1381-41a4-9243-30d3eb061ab3
  Args:
    source: Princess_Marie_Alix_of_Schaumburg-Lippe
    type: :Person
  AddLiteral (d67e1757-295b-4410-884d-8933518905f0)
 Call ID: d67e1757-295b-4410-884d-8933518905f0
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1923
    source: Princess_Marie_Alix_of_Schaumburg-Lippe
  AddLiteral (a3c56ebe-6b28-4b4d-b9b6-5d1c54d2304b)
 Call ID: a3c56ebe-6b28-4b4d-b9b6-5d1c54d2304b
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: Princess_Marie_Alix_of_Schaumburg-Lippe
    literal_value: 2021
  AddTriple (127cf816-dd89-4f42-9995-6d616e38daaa)
 Call ID: 127cf816-dd89-4f42-9995-6d616e38daaa
  Args:
    relation: :hasFather
    source: Christoph_of_Schleswig-Holstein
    target: Peter_Duke_of_Schleswig-Holstein
  AddTriple (1582449f-0948-4598-9b8d-279d9c6dc032)
 Call ID: 1582449f-0948-4598-9b8d-279d9c6dc032
  Args:
    relation: :hasMother
    source: Christoph_of_Schleswig-Holstein
    target: Princess_Marie_Alix_of_Schaumburg-Lippe
  AssignClass (1c39f672-32cc-4d63-97b2-57101d2a8ea2)
 Call ID: 1c39f672-32cc-4d63-97b2-57101d2a8ea2
  Args:
    source: Princess_Elisabeth_of_Lippe-Weissenfeld
    type: :Woman
  AssignClass (899f57f8-c21d-42c0-8995-c3cf1e89485e)
 Call ID: 899f57f8-c21d-42c0-8995-c3cf1e89485e
  Args:
    type: :Person
    source: Princess_Elisabeth_of_Lippe-Weissenfeld
  AddLiteral (5b1259af-e4df-4e95-b976-3d4e7a0a6176)
 Call ID: 5b1259af-e4df-4e95-b976-3d4e7a0a6176
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1957
    source: Princess_Elisabeth_of_Lippe-Weissenfeld
  AddTriple (9fa7de3b-470b-4a1b-a1b7-d7e836e33d89)
 Call ID: 9fa7de3b-470b-4a1b-a1b7-d7e836e33d89
  Args:
    relation: :hasRelation
    source: Christoph_of_Schleswig-Holstein
    target: Princess_Elisabeth_of_Lippe-Weissenfeld
  AssignClass (48db63e9-0ad6-456c-8d26-d5de2b89061a)
 Call ID: 48db63e9-0ad6-456c-8d26-d5de2b89061a
  Args:
    type: :Man
    source: Prince_Alfred_Karl_Friedrich_Georg_Franz_of_Lippe-Weissenfeld
  AssignClass (650be298-929f-439e-aafc-4db3a28fcdd7)
 Call ID: 650be298-929f-439e-aafc-4db3a28fcdd7
  Args:
    source: Prince_Alfred_Karl_Friedrich_Georg_Franz_of_Lippe-Weissenfeld
    type: :Person
  AddLiteral (de570496-dab4-408f-bfb5-0cb951c2d8a0)
 Call ID: de570496-dab4-408f-bfb5-0cb951c2d8a0
  Args:
    literal_value: 1922
    source: Prince_Alfred_Karl_Friedrich_Georg_Franz_of_Lippe-Weissenfeld
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (dfbc23aa-65c2-4c9e-9aca-5f3d266d1392)
 Call ID: dfbc23aa-65c2-4c9e-9aca-5f3d266d1392
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: Prince_Alfred_Karl_Friedrich_Georg_Franz_of_Lippe-Weissenfeld
    literal_value: 2024
  AssignClass (3f57a696-2201-4bdf-8d8d-3a10428d7003)
 Call ID: 3f57a696-2201-4bdf-8d8d-3a10428d7003
  Args:
    type: :Woman
    source: Baroness_Irmgard_Julinka_Wagner_von_Wehrborn
  AssignClass (96e92449-5681-4ba2-b256-a479c49f2031)
 Call ID: 96e92449-5681-4ba2-b256-a479c49f2031
  Args:
    type: :Person
    source: Baroness_Irmgard_Julinka_Wagner_von_Wehrborn
  AddLiteral (b47f7c39-6bf5-46d3-ba1e-fb3d14d57304)
 Call ID: b47f7c39-6bf5-46d3-ba1e-fb3d14d57304
  Args:
    literal_value: 1928
    source: Baroness_Irmgard_Julinka_Wagner_von_Wehrborn
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddTriple (3e931e76-9737-4b42-8a30-58cc156ad354)
 Call ID: 3e931e76-9737-4b42-8a30-58cc156ad354
  Args:
    target: Prince_Alfred_Karl_Friedrich_Georg_Franz_of_Lippe-Weissenfeld
    source: Princess_Elisabeth_of_Lippe-Weissenfeld
    relation: :hasFather
  AddTriple (e45b044f-111f-49ba-b984-4f32c83f0ab8)
 Call ID: e45b044f-111f-49ba-b984-4f32c83f0ab8
  Args:
    source: Princess_Elisabeth_of_Lippe-Weissenfeld
    target: Baroness_Irmgard_Julinka_Wagner_von_Wehrborn
    relation: :hasMother
  AssignClass (7238229b-e92b-4994-8f81-2e78c675e9b6)
 Call ID: 7238229b-e92b-4994-8f81-2e78c675e9b6
  Args:
    type: :Man
    source: Friedrich_Duke_of_Schleswig-Holstein-Sonderburg-Glücksburg
  AssignClass (644d6e05-2f71-4fe3-9118-ad1ba982e632)
 Call ID: 644d6e05-2f71-4fe3-9118-ad1ba982e632
  Args:
    source: Friedrich_Duke_of_Schleswig-Holstein-Sonderburg-Glücksburg
    type: :Ancestor
  AssignClass (ab36311b-cb73-4c26-be8c-d77ba8ff5082)
 Call ID: ab36311b-cb73-4c26-be8c-d77ba8ff5082
  Args:
    type: :Person
    source: Friedrich_Duke_of_Schleswig-Holstein-Sonderburg-Glücksburg
  AssignClass (3e525432-915d-470d-a9a6-f7e5de2bb78c)
 Call ID: 3e525432-915d-470d-a9a6-f7e5de2bb78c
  Args:
    type: :Man
    source: Christian_IX_of_Denmark
  AssignClass (41459950-3dc1-49e2-aebc-806a524266eb)
 Call ID: 41459950-3dc1-49e2-aebc-806a524266eb
  Args:
    type: :Person
    source: Christian_IX_of_Denmark
  AddTriple (10853d6e-b8a4-4b5b-af2a-5df9e350b79c)
 Call ID: 10853d6e-b8a4-4b5b-af2a-5df9e350b79c
  Args:
    target: Christian_IX_of_Denmark
    source: Friedrich_Duke_of_Schleswig-Holstein-Sonderburg-Glücksburg
    relation: :isBrotherOf
  AssignClass (9fb813ef-6662-4cbb-8779-741f6f4dc8b9)
 Call ID: 9fb813ef-6662-4cbb-8779-741f6f4dc8b9
  Args:
    source: Friedrich_Ferdinand_Duke_of_Schleswig-Holstein-Sonderburg-Glücksburg
    type: :Man
  AssignClass (3641bb7a-c5c5-45be-86cc-25b0e35361fb)
 Call ID: 3641bb7a-c5c5-45be-86cc-25b0e35361fb
  Args:
    source: Friedrich_Ferdinand_Duke_of_Schleswig-Holstein-Sonderburg-Glücksburg
    type: :Ancestor
  AssignClass (8860147d-9d19-416a-a753-5a80417e6558)
 Call ID: 8860147d-9d19-416a-a753-5a80417e6558
  Args:
    source: Friedrich_Ferdinand_Duke_of_Schleswig-Holstein-Sonderburg-Glücksburg
    type: :Person
  Finish (ae1135f0-913d-414e-b404-11c3f15fc880)
 Call ID: ae1135f0-913d-414e-b404-11c3f15fc880
  Args: