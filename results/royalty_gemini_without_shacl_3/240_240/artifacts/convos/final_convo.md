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
Victoria Federica de Todos los Santos de Marichalar y Borbón, Lady of Tejada GE (born 9 September 2000) is the younger child and only daughter of Infanta Elena, Duchess of Lugo, and Jaime de Marichalar.
She is a granddaughter of King Juan Carlos I and Queen Sofía of Spain and a niece of King Felipe VI.
Victoria is fifth in the line of succession to the Spanish throne after her cousins, King Felipe's daughters Leonor, Princess of Asturias, and Infanta Sofía; her mother; and her brother, Felipe.
Early life and education

Victoria de Marichalar y Borbón was born 9 September 2000 at 13:00 in Ruber International Hospital in Madrid.
She made her first Holy Communion on 27 May 2009 at the Dominicos Church in Alcobendas, Spain.
Then she studied at a British boarding school for 3 years before returning to Spain at St. George's de La Moraleja.
Victoria studied ballet and horse riding.
Career

Marichalar has been reported to be working in the fashion industry and is quoted as saying that fashion is her "true calling".



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
  AssignClass (af3ae583-5646-4a14-ba9c-6784bbbec60c)
 Call ID: af3ae583-5646-4a14-ba9c-6784bbbec60c
  Args:
    source: Victoria_Federica_de_Marichalar_y_Borbon
    type: :Person
  AssignClass (c036d8a8-7bef-4f20-ba82-78e40c9f0ce8)
 Call ID: c036d8a8-7bef-4f20-ba82-78e40c9f0ce8
  Args:
    source: Victoria_Federica_de_Marichalar_y_Borbon
    type: :Woman
  AssignClass (e99304b5-9afa-4fa3-8e3b-ab6bf59ca9c4)
 Call ID: e99304b5-9afa-4fa3-8e3b-ab6bf59ca9c4
  Args:
    source: Infanta_Elena
    type: :Person
  AssignClass (87a8bdf3-f87e-431e-8204-e344ee4dc44d)
 Call ID: 87a8bdf3-f87e-431e-8204-e344ee4dc44d
  Args:
    source: Infanta_Elena
    type: :Woman
  AssignClass (a8927e6a-9cff-4485-bbb8-a08060eda8ac)
 Call ID: a8927e6a-9cff-4485-bbb8-a08060eda8ac
  Args:
    source: Jaime_de_Marichalar
    type: :Person
  AssignClass (7cbad100-1e8a-4b99-8229-addd02a2a009)
 Call ID: 7cbad100-1e8a-4b99-8229-addd02a2a009
  Args:
    source: Jaime_de_Marichalar
    type: :Man
  AssignClass (f993351c-5f9c-40b5-b5c5-b63e5c92f7db)
 Call ID: f993351c-5f9c-40b5-b5c5-b63e5c92f7db
  Args:
    type: :Person
    source: Juan_Carlos_I
  AssignClass (132d6df2-50ca-464d-9c68-278ab165e03d)
 Call ID: 132d6df2-50ca-464d-9c68-278ab165e03d
  Args:
    type: :Man
    source: Juan_Carlos_I
  AssignClass (cc8eb99b-bc0a-45d6-aa4f-9253ddf74193)
 Call ID: cc8eb99b-bc0a-45d6-aa4f-9253ddf74193
  Args:
    type: :Person
    source: Sofia_of_Spain
  AssignClass (886be4bd-67e6-4645-8a98-51b7746ced40)
 Call ID: 886be4bd-67e6-4645-8a98-51b7746ced40
  Args:
    source: Sofia_of_Spain
    type: :Woman
  AssignClass (7e686e94-0a9a-4e4d-8a56-1adf420e652d)
 Call ID: 7e686e94-0a9a-4e4d-8a56-1adf420e652d
  Args:
    type: :Person
    source: Felipe_VI
  AssignClass (0774b647-c960-407c-b1ba-98d27dfa3fe6)
 Call ID: 0774b647-c960-407c-b1ba-98d27dfa3fe6
  Args:
    type: :Man
    source: Felipe_VI
  AssignClass (a02bb274-b402-4258-b209-e2930197c269)
 Call ID: a02bb274-b402-4258-b209-e2930197c269
  Args:
    source: Leonor_Princess_of_Asturias
    type: :Person
  AssignClass (4a923ccc-a343-4fb2-815c-2c3d60b341aa)
 Call ID: 4a923ccc-a343-4fb2-815c-2c3d60b341aa
  Args:
    type: :Woman
    source: Leonor_Princess_of_Asturias
  AssignClass (aa186602-7813-4afc-b45e-cf67aff6b616)
 Call ID: aa186602-7813-4afc-b45e-cf67aff6b616
  Args:
    source: Infanta_Sofia
    type: :Person
  AssignClass (3c085c89-e279-4980-9024-78cb3b7361c3)
 Call ID: 3c085c89-e279-4980-9024-78cb3b7361c3
  Args:
    source: Infanta_Sofia
    type: :Woman
  AssignClass (2a487476-2c45-42f7-8677-94000967f332)
 Call ID: 2a487476-2c45-42f7-8677-94000967f332
  Args:
    type: :Person
    source: Felipe_de_Marichalar
  AssignClass (f47bca01-a834-4c07-9d96-aa78f23a5d1c)
 Call ID: f47bca01-a834-4c07-9d96-aa78f23a5d1c
  Args:
    source: Felipe_de_Marichalar
    type: :Man
  AddLiteral (58b8b070-c84c-4b47-b8d6-dc2c944f5696)
 Call ID: 58b8b070-c84c-4b47-b8d6-dc2c944f5696
  Args:
    literal_value: 2000
    source: Victoria_Federica_de_Marichalar_y_Borbon
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddTriple (34e72fbb-0718-4542-a72b-ce0da48c6509)
 Call ID: 34e72fbb-0718-4542-a72b-ce0da48c6509
  Args:
    source: Victoria_Federica_de_Marichalar_y_Borbon
    target: Infanta_Elena
    relation: :hasMother
  AddTriple (1f27b2c2-b5ab-49b2-8bb7-f469fba6e57c)
 Call ID: 1f27b2c2-b5ab-49b2-8bb7-f469fba6e57c
  Args:
    relation: :hasFather
    target: Jaime_de_Marichalar
    source: Victoria_Federica_de_Marichalar_y_Borbon
  AddTriple (8c8aa021-03b1-41c7-afd8-c27690e305cb)
 Call ID: 8c8aa021-03b1-41c7-afd8-c27690e305cb
  Args:
    target: Juan_Carlos_I
    source: Victoria_Federica_de_Marichalar_y_Borbon
    relation: :hasParent
  AddTriple (59df8890-7a2f-44fc-a59d-f83db9c733f9)
 Call ID: 59df8890-7a2f-44fc-a59d-f83db9c733f9
  Args:
    relation: :hasParent
    source: Victoria_Federica_de_Marichalar_y_Borbon
    target: Sofia_of_Spain
  AddTriple (4cea9f01-30de-4d4e-9b9d-0cddbe416c90)
 Call ID: 4cea9f01-30de-4d4e-9b9d-0cddbe416c90
  Args:
    relation: :hasBrother
    target: Felipe_de_Marichalar
    source: Victoria_Federica_de_Marichalar_y_Borbon
  AddTriple (159a7084-6588-4a5f-b4c2-f2cf8dad79cc)
 Call ID: 159a7084-6588-4a5f-b4c2-f2cf8dad79cc
  Args:
    source: Victoria_Federica_de_Marichalar_y_Borbon
    target: Infanta_Elena
    relation: :isChildOf
  AddTriple (76afa151-59e4-4064-b7d4-2c1a157ee1a0)
 Call ID: 76afa151-59e4-4064-b7d4-2c1a157ee1a0
  Args:
    target: Jaime_de_Marichalar
    source: Victoria_Federica_de_Marichalar_y_Borbon
    relation: :isChildOf
  Finish (f50533f3-1c48-4453-b3d2-a78cb5872dba)
 Call ID: f50533f3-1c48-4453-b3d2-a78cb5872dba
  Args: