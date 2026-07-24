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
Princess Eugenie of Greece and Denmark (Greek: Ευγενία, romanized: Evyenía; 10 February 1910 – 13 February 1989) was by birth member of the Greek royal family and by marriage member of the House of Radziwiłł and House of Thurn und Taxis.
Early life and ancestry

Eugenie was the youngest child and only daughter of Prince George of Greece and Denmark and his wife, Princess Marie Bonaparte, daughter of Marie-Félix Blanc and Prince Roland Bonaparte, a great-nephew of Napoleon I.
Her father was the second son of George I of Greece and Olga Constantinovna of Russia.
She had one elder brother, Prince Peter of Greece and Denmark, who, at the time of his birth, was third in line of succession to the Greek throne, preceded only by his unmarried cousin Paul and his own and Eugenia's father, Prince George.
As a cousin of the bridegroom, Eugenie was a leading guest at the 1947 wedding of Princess Elizabeth and Philip, Duke of Edinburgh.
She authored Le Tsarevitch, Enfant Martyr, a biography of Aleksey Nikolaevich, Tsarevich of Russia, written in French, which was published in 1990.
Marriage and issue

She married Prince Dominik Rainer Radziwiłł, member of the House of Radziwiłł (and son of Prince Hieronim Radziwiłł and Archduchess Renata of Austria), on 30 May 1938 in Paris.
They had two children:


Eugénie remarried on 28 November 1949 to Prince Raymundo della Torre e Tasso, Duke of Castel Duino, a cadet member of the House of Thurn and Taxis.



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
  AssignClass (9ffd94a0-78ab-48e6-86c9-108ad05b748e)
 Call ID: 9ffd94a0-78ab-48e6-86c9-108ad05b748e
  Args:
    type: :Woman
    source: Eugenie_of_Greece_and_Denmark
  AssignClass (0992ccd0-aa16-442b-931c-56a1324b3dae)
 Call ID: 0992ccd0-aa16-442b-931c-56a1324b3dae
  Args:
    type: :Person
    source: Eugenie_of_Greece_and_Denmark
  AddLiteral (1c90a05c-cb0d-4136-918e-394b2ab2e237)
 Call ID: 1c90a05c-cb0d-4136-918e-394b2ab2e237
  Args:
    literal_value: 1910
    relation: :hasBirthYear
    literal_type: xsd:nonNegativeInteger
    source: Eugenie_of_Greece_and_Denmark
  AddLiteral (24d490b9-28fb-4898-9f8a-f36eb9a0110e)
 Call ID: 24d490b9-28fb-4898-9f8a-f36eb9a0110e
  Args:
    source: Eugenie_of_Greece_and_Denmark
    literal_type: xsd:nonNegativeInteger
    literal_value: 1989
    relation: :hasDeathYear
  AssignClass (2807c67b-68ba-48c9-a1e5-a8a2f6af4316)
 Call ID: 2807c67b-68ba-48c9-a1e5-a8a2f6af4316
  Args:
    type: :Man
    source: George_of_Greece_and_Denmark
  AssignClass (10929f94-18ed-42ac-84e0-6eea9bbdf2b8)
 Call ID: 10929f94-18ed-42ac-84e0-6eea9bbdf2b8
  Args:
    type: :Person
    source: George_of_Greece_and_Denmark
  AssignClass (d8e6b67b-770a-4634-9f1a-f09f6f421596)
 Call ID: d8e6b67b-770a-4634-9f1a-f09f6f421596
  Args:
    type: :Woman
    source: Marie_Bonaparte
  AssignClass (bb575bea-0511-4945-bb69-963f7397d9e4)
 Call ID: bb575bea-0511-4945-bb69-963f7397d9e4
  Args:
    type: :Person
    source: Marie_Bonaparte
  AddTriple (de668323-0219-462f-9ea0-bc45b64b468d)
 Call ID: de668323-0219-462f-9ea0-bc45b64b468d
  Args:
    source: Eugenie_of_Greece_and_Denmark
    relation: :hasFather
    target: George_of_Greece_and_Denmark
  AddTriple (d124a282-d3e2-4b97-826f-aa5c4caf1400)
 Call ID: d124a282-d3e2-4b97-826f-aa5c4caf1400
  Args:
    relation: :hasMother
    target: Marie_Bonaparte
    source: Eugenie_of_Greece_and_Denmark
  AssignClass (5296b51a-03f8-46d1-8655-036c7b1af1cb)
 Call ID: 5296b51a-03f8-46d1-8655-036c7b1af1cb
  Args:
    type: :Woman
    source: Marie-Felix_Blanc
  AssignClass (fcae300a-a084-48db-b3fa-10004e7c8d9a)
 Call ID: fcae300a-a084-48db-b3fa-10004e7c8d9a
  Args:
    type: :Person
    source: Marie-Felix_Blanc
  AssignClass (8089e783-23bf-47bb-9cc7-cd6400dfca55)
 Call ID: 8089e783-23bf-47bb-9cc7-cd6400dfca55
  Args:
    type: :Man
    source: Roland_Bonaparte
  AssignClass (adf84407-d4e7-4c9a-9601-b4be84fbb640)
 Call ID: adf84407-d4e7-4c9a-9601-b4be84fbb640
  Args:
    type: :Person
    source: Roland_Bonaparte
  AddTriple (da2778d0-d467-4b99-b95b-39040f95768b)
 Call ID: da2778d0-d467-4b99-b95b-39040f95768b
  Args:
    source: Marie_Bonaparte
    relation: :hasMother
    target: Marie-Felix_Blanc
  AddTriple (1925fbb1-6ec6-4b61-a3de-af8ec93ff3b4)
 Call ID: 1925fbb1-6ec6-4b61-a3de-af8ec93ff3b4
  Args:
    source: Marie_Bonaparte
    relation: :hasFather
    target: Roland_Bonaparte
  AssignClass (ef3a7e98-82c6-4dce-8574-d55e25349532)
 Call ID: ef3a7e98-82c6-4dce-8574-d55e25349532
  Args:
    type: :Man
    source: George_I_of_Greece
  AssignClass (b2479a0e-5b6a-486d-b866-6ea13fd6c8c5)
 Call ID: b2479a0e-5b6a-486d-b866-6ea13fd6c8c5
  Args:
    type: :Person
    source: George_I_of_Greece
  AssignClass (cc043308-efc0-42d6-81ea-23fbda0ecf66)
 Call ID: cc043308-efc0-42d6-81ea-23fbda0ecf66
  Args:
    type: :Woman
    source: Olga_Constantinovna_of_Russia
  AssignClass (bacd80b7-71c0-4736-90d2-3a1ccc9c9826)
 Call ID: bacd80b7-71c0-4736-90d2-3a1ccc9c9826
  Args:
    type: :Person
    source: Olga_Constantinovna_of_Russia
  AddTriple (6429726c-9e6a-49dc-bcfb-515ec369e3ee)
 Call ID: 6429726c-9e6a-49dc-bcfb-515ec369e3ee
  Args:
    source: George_of_Greece_and_Denmark
    relation: :hasFather
    target: George_I_of_Greece
  AddTriple (1009d552-8d43-495f-9f8b-27dbeab3df08)
 Call ID: 1009d552-8d43-495f-9f8b-27dbeab3df08
  Args:
    source: George_of_Greece_and_Denmark
    relation: :hasMother
    target: Olga_Constantinovna_of_Russia
  AssignClass (d00b94c8-ccea-461c-a234-af09cc9465f3)
 Call ID: d00b94c8-ccea-461c-a234-af09cc9465f3
  Args:
    type: :Man
    source: Peter_of_Greece_and_Denmark
  AssignClass (72402cd0-533a-483b-948c-7a43d8880bf3)
 Call ID: 72402cd0-533a-483b-948c-7a43d8880bf3
  Args:
    type: :Person
    source: Peter_of_Greece_and_Denmark
  AddTriple (c2945946-96b1-4ac5-a3d7-9cec0ddd43a2)
 Call ID: c2945946-96b1-4ac5-a3d7-9cec0ddd43a2
  Args:
    relation: :hasBrother
    target: Peter_of_Greece_and_Denmark
    source: Eugenie_of_Greece_and_Denmark
  AssignClass (965b79c0-1c3a-44b5-a813-1970336dd76f)
 Call ID: 965b79c0-1c3a-44b5-a813-1970336dd76f
  Args:
    type: :Man
    source: Dominik_Rainer_Radziwill
  AssignClass (3be08c64-d991-43fc-a92c-b41515c5d226)
 Call ID: 3be08c64-d991-43fc-a92c-b41515c5d226
  Args:
    type: :Person
    source: Dominik_Rainer_Radziwill
  AddLiteral (8ee9099a-282a-46cc-b805-b8455cc5a92a)
 Call ID: 8ee9099a-282a-46cc-b805-b8455cc5a92a
  Args:
    relation: :hasMarriageYear
    literal_value: 1938
    literal_type: xsd:nonNegativeInteger
    source: Dominik_Rainer_Radziwill
  AssignClass (fe3fae32-e615-452a-a22e-3ef4ba002b5e)
 Call ID: fe3fae32-e615-452a-a22e-3ef4ba002b5e
  Args:
    type: :Man
    source: Hieronim_Radziwill
  AssignClass (bcc52e40-c402-4ff1-a566-297d904ae207)
 Call ID: bcc52e40-c402-4ff1-a566-297d904ae207
  Args:
    type: :Person
    source: Hieronim_Radziwill
  AssignClass (d038f6a0-af77-4ed3-b69e-f1f3408636d8)
 Call ID: d038f6a0-af77-4ed3-b69e-f1f3408636d8
  Args:
    type: :Woman
    source: Renata_of_Austria
  AssignClass (cd5525ef-48e5-4f32-bc9a-30ab1d905f27)
 Call ID: cd5525ef-48e5-4f32-bc9a-30ab1d905f27
  Args:
    type: :Person
    source: Renata_of_Austria
  AddTriple (3cca9702-a173-4a1c-9d94-8464e74126c4)
 Call ID: 3cca9702-a173-4a1c-9d94-8464e74126c4
  Args:
    relation: :hasFather
    target: Hieronim_Radziwill
    source: Dominik_Rainer_Radziwill
  AddTriple (b9e7a592-6b9e-4849-bb87-8d641c097eb9)
 Call ID: b9e7a592-6b9e-4849-bb87-8d641c097eb9
  Args:
    relation: :hasMother
    target: Renata_of_Austria
    source: Dominik_Rainer_Radziwill
  AssignClass (ef01f98e-f9ce-4604-ae7d-08149c49e6ad)
 Call ID: ef01f98e-f9ce-4604-ae7d-08149c49e6ad
  Args:
    type: :Man
    source: Raymundo_della_Torre_e_Tasso
  AssignClass (da1c1e71-637a-465e-832b-62a970ecc437)
 Call ID: da1c1e71-637a-465e-832b-62a970ecc437
  Args:
    type: :Person
    source: Raymundo_della_Torre_e_Tasso
  AddLiteral (4bad9f4e-23ef-4344-9fe1-f5917bc229e9)
 Call ID: 4bad9f4e-23ef-4344-9fe1-f5917bc229e9
  Args:
    source: Raymundo_della_Torre_e_Tasso
    literal_type: xsd:nonNegativeInteger
    literal_value: 1949
    relation: :hasMarriageYear
  Finish (004bc0a5-acf0-4721-aed6-6e1ed0f89dfb)
 Call ID: 004bc0a5-acf0-4721-aed6-6e1ed0f89dfb
  Args: