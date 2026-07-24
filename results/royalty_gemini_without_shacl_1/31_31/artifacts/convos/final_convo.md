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
  AssignClass (68322f13-e458-4f50-8361-ad0bbb9a4765)
 Call ID: 68322f13-e458-4f50-8361-ad0bbb9a4765
  Args:
    source: Christoph_of_Schleswig-Holstein
    type: :Man
  AssignClass (3c3060cc-21a6-4c87-8a9a-42b65fd94a4d)
 Call ID: 3c3060cc-21a6-4c87-8a9a-42b65fd94a4d
  Args:
    source: Christoph_of_Schleswig-Holstein
    type: :Person
  AddLiteral (dda2abb1-c3c7-40c2-b7d1-e4073059f068)
 Call ID: dda2abb1-c3c7-40c2-b7d1-e4073059f068
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1949
    source: Christoph_of_Schleswig-Holstein
  AddLiteral (dd72bce6-be26-441e-954b-c6b9483b4fb9)
 Call ID: dd72bce6-be26-441e-954b-c6b9483b4fb9
  Args:
    literal_value: 2023
    source: Christoph_of_Schleswig-Holstein
    literal_type: xsd:integer
    relation: :hasDeathYear
  AssignClass (67bcc2d3-c6d3-4e78-a408-948c09858e18)
 Call ID: 67bcc2d3-c6d3-4e78-a408-948c09858e18
  Args:
    type: :Man
    source: Peter_Duke_of_Schleswig-Holstein
  AssignClass (3edb98d2-deef-421f-9ba6-f87fed632608)
 Call ID: 3edb98d2-deef-421f-9ba6-f87fed632608
  Args:
    source: Peter_Duke_of_Schleswig-Holstein
    type: :Person
  AddLiteral (f6a49b27-2d6e-4b42-9391-3a53fd79da7c)
 Call ID: f6a49b27-2d6e-4b42-9391-3a53fd79da7c
  Args:
    source: Peter_Duke_of_Schleswig-Holstein
    literal_value: 1922
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (31ddfe4e-5350-4f56-8b00-ae4ece38078e)
 Call ID: 31ddfe4e-5350-4f56-8b00-ae4ece38078e
  Args:
    source: Peter_Duke_of_Schleswig-Holstein
    literal_value: 1980
    relation: :hasDeathYear
    literal_type: xsd:integer
  AddTriple (52df0fb3-8871-490b-bf9a-9196b1fb96ee)
 Call ID: 52df0fb3-8871-490b-bf9a-9196b1fb96ee
  Args:
    target: Peter_Duke_of_Schleswig-Holstein
    source: Christoph_of_Schleswig-Holstein
    relation: :hasFather
  AssignClass (2561f5cd-644b-4880-96d8-cd821ab84011)
 Call ID: 2561f5cd-644b-4880-96d8-cd821ab84011
  Args:
    source: Marie_Alix_of_Schaumburg-Lippe
    type: :Woman
  AssignClass (d175c305-3de5-4bf3-ad7f-33142e4615cc)
 Call ID: d175c305-3de5-4bf3-ad7f-33142e4615cc
  Args:
    source: Marie_Alix_of_Schaumburg-Lippe
    type: :Person
  AddLiteral (d3bce63b-c848-49d9-af5d-0a500dac763c)
 Call ID: d3bce63b-c848-49d9-af5d-0a500dac763c
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Marie_Alix_of_Schaumburg-Lippe
    literal_value: 1923
  AddLiteral (ca55f8e1-0679-4914-9c8c-b064b08a0de8)
 Call ID: ca55f8e1-0679-4914-9c8c-b064b08a0de8
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: Marie_Alix_of_Schaumburg-Lippe
    literal_value: 2021
  AddTriple (0c3b9071-3d55-48b7-9cf0-9db698d2efe4)
 Call ID: 0c3b9071-3d55-48b7-9cf0-9db698d2efe4
  Args:
    target: Marie_Alix_of_Schaumburg-Lippe
    source: Christoph_of_Schleswig-Holstein
    relation: :hasMother
  AssignClass (55f46b64-4c75-403d-bd8e-4423974afa64)
 Call ID: 55f46b64-4c75-403d-bd8e-4423974afa64
  Args:
    type: :Woman
    source: Elisabeth_of_Lippe-Weissenfeld
  AssignClass (4cd2c880-5a5d-4074-ac30-3e6f5feda354)
 Call ID: 4cd2c880-5a5d-4074-ac30-3e6f5feda354
  Args:
    source: Elisabeth_of_Lippe-Weissenfeld
    type: :Person
  AddLiteral (f382517c-682e-487b-b22c-63fa89e3fdc7)
 Call ID: f382517c-682e-487b-b22c-63fa89e3fdc7
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Elisabeth_of_Lippe-Weissenfeld
    literal_value: 1957
  AssignClass (344f0332-969e-4c03-b9a3-9685bd05df68)
 Call ID: 344f0332-969e-4c03-b9a3-9685bd05df68
  Args:
    type: :Man
    source: Alfred_Karl_Friedrich_Georg_Franz_of_Lippe-Weissenfeld
  AssignClass (64304599-843d-4154-a046-d7843d4ee3da)
 Call ID: 64304599-843d-4154-a046-d7843d4ee3da
  Args:
    source: Alfred_Karl_Friedrich_Georg_Franz_of_Lippe-Weissenfeld
    type: :Person
  AddLiteral (491b54da-c0d8-4b8d-8289-98eff7ae3aa6)
 Call ID: 491b54da-c0d8-4b8d-8289-98eff7ae3aa6
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Alfred_Karl_Friedrich_Georg_Franz_of_Lippe-Weissenfeld
    literal_value: 1922
  AddLiteral (99ab0dc0-3bfd-43a4-be01-6c52792ed365)
 Call ID: 99ab0dc0-3bfd-43a4-be01-6c52792ed365
  Args:
    source: Alfred_Karl_Friedrich_Georg_Franz_of_Lippe-Weissenfeld
    literal_value: 2024
    relation: :hasDeathYear
    literal_type: xsd:integer
  AddTriple (23d430fe-a8f0-4ba5-a529-4ebff02fae64)
 Call ID: 23d430fe-a8f0-4ba5-a529-4ebff02fae64
  Args:
    relation: :hasFather
    target: Alfred_Karl_Friedrich_Georg_Franz_of_Lippe-Weissenfeld
    source: Elisabeth_of_Lippe-Weissenfeld
  AssignClass (bb7ff24e-796a-4198-86f2-4e1381bd21c1)
 Call ID: bb7ff24e-796a-4198-86f2-4e1381bd21c1
  Args:
    source: Irmgard_Julinka_Wagner_von_Wehrborn
    type: :Woman
  AssignClass (a7f1768c-ed37-4762-8bd0-c653d99b843a)
 Call ID: a7f1768c-ed37-4762-8bd0-c653d99b843a
  Args:
    source: Irmgard_Julinka_Wagner_von_Wehrborn
    type: :Person
  AddLiteral (99770fe4-3550-4b31-abad-e17f66dbc317)
 Call ID: 99770fe4-3550-4b31-abad-e17f66dbc317
  Args:
    literal_value: 1928
    source: Irmgard_Julinka_Wagner_von_Wehrborn
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddTriple (d6d37744-d47d-4552-8ebb-a79001938c8a)
 Call ID: d6d37744-d47d-4552-8ebb-a79001938c8a
  Args:
    source: Elisabeth_of_Lippe-Weissenfeld
    target: Irmgard_Julinka_Wagner_von_Wehrborn
    relation: :hasMother
  AddTriple (b236d0d1-a8df-4015-956d-544ac39f3254)
 Call ID: b236d0d1-a8df-4015-956d-544ac39f3254
  Args:
    relation: :hasRelation
    source: Christoph_of_Schleswig-Holstein
    target: Elisabeth_of_Lippe-Weissenfeld
  Finish (69b34744-f8df-48c0-94d1-8854e44ab0c9)
 Call ID: 69b34744-f8df-48c0-94d1-8854e44ab0c9
  Args: