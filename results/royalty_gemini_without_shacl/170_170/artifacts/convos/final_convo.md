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
Queen Margrethe II


Count Nikolai of Monpezat SK (born Prince Nikolai of Denmark; 28 August 1999) is a member of the Danish royal family.
He is the eldest son of Prince Joachim and his first wife, Alexandra, Countess of Frederiksborg, the eldest grandchild of Queen Margrethe II and Prince Henrik, and the eldest nephew of King Frederik X.
Biography

Nikolai was born a prince of Denmark at Rigshospitalet in Copenhagen on 28 August 1999.
He is the oldest grandchild of Queen Margrethe II and her late husband, Prince Henrik.
Nikolai was baptised in the chapel of the Fredensborg Palace on 6 November 1999 by the Danish Chaplain-in-Ordinary, Christian Thodberg.
At the christening, the musical work Lys på din vej, composed by Frederik Magle and dedicated to the prince, was performed for the first time.
His godparents are his paternal uncle King Frederik X, his maternal aunt Nicola Baird, Prince Edward, Duke of Edinburgh, Peter Steenstrup and Camilla Flint.
After their divorce in 2005, Prince Joachim and Alexandra had joint custody of the prince and his brother Prince Felix.
Nikolai and Felix have two half-siblings, Henrik and Athena, from their father's second marriage to Marie Cavallier.
Nikolai was confirmed on 18 May 2013 in Fredensborg Palace Church in the presence of his immediate family and all his godparents.
Like his father and uncle, Nikolai attended Krebs School in Copenhagen.
As part of that course, in 2023, Nikolai moved to Australia to take a semester at University of Technology Sydney.
In early 2018, Nikolai signed as a fashion model with the agency Scoop Models.
In February 2023, Nikolai signed as a model for Elite Model World - Paris under the name of 'Nikolai'.
Subsequently, in May he also signed with Barcelona-based modeling agency Sight Management Studio as 'Count Nikolai of Monpezat'.
In June 2024, Nikolai graduated from Copenhagen Business School with a Master of Science in Merchandising degree (cand.merc.).
In December 2025, it was announced that Nikolai would make his acting debut in the film adaptation of Hjalmar Söderberg's novel Doktor Glas (1905).
Titles, styles and honours

Titles and styles

Originally styled "His Highness Prince Nikolai of Denmark", Nikolai's style was expanded on 29 April 2008 to "His Highness Prince Nikolai of Denmark, Count of Monpezat".
In September 2022, Queen Margrethe II decided to restrict the titles Prince and Princess to the direct line of succession to the throne.
Since 1 January 2023, Count Nikolai is known as "His Excellency Count Nikolai of Monpezat".



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
  AssignClass (aeb02e01-60de-42d2-be56-6adc93bb70d1)
 Call ID: aeb02e01-60de-42d2-be56-6adc93bb70d1
  Args:
    type: :Person
    source: Queen_Margrethe_II
  AssignClass (1895c283-11cf-406a-81a0-490fabd036c9)
 Call ID: 1895c283-11cf-406a-81a0-490fabd036c9
  Args:
    source: Queen_Margrethe_II
    type: :Woman
  AssignClass (f6a28b90-eedf-4c8c-b7dd-715f3bc7b6f2)
 Call ID: f6a28b90-eedf-4c8c-b7dd-715f3bc7b6f2
  Args:
    source: Prince_Nikolai_of_Denmark
    type: :Person
  AssignClass (93d133ec-921e-4e7e-88de-45ba11dd649f)
 Call ID: 93d133ec-921e-4e7e-88de-45ba11dd649f
  Args:
    source: Prince_Nikolai_of_Denmark
    type: :Man
  AssignClass (e09ec21b-4073-4bdc-bda8-c57419cdaebb)
 Call ID: e09ec21b-4073-4bdc-bda8-c57419cdaebb
  Args:
    source: Prince_Joachim
    type: :Person
  AssignClass (89b13846-668b-4cdf-a2dd-b5da4872fa8b)
 Call ID: 89b13846-668b-4cdf-a2dd-b5da4872fa8b
  Args:
    type: :Man
    source: Prince_Joachim
  AssignClass (abd8cb65-b535-457e-bb80-3f5d5d34d707)
 Call ID: abd8cb65-b535-457e-bb80-3f5d5d34d707
  Args:
    source: Alexandra_Countess_of_Frederiksborg
    type: :Person
  AssignClass (b975e631-2642-49c9-b646-3bc607521214)
 Call ID: b975e631-2642-49c9-b646-3bc607521214
  Args:
    source: Alexandra_Countess_of_Frederiksborg
    type: :Woman
  AssignClass (835bdf35-0803-46d3-be4b-ed55f457c20f)
 Call ID: 835bdf35-0803-46d3-be4b-ed55f457c20f
  Args:
    source: Prince_Henrik
    type: :Person
  AssignClass (4550641d-3ba5-48d6-a85a-4bad36d8204d)
 Call ID: 4550641d-3ba5-48d6-a85a-4bad36d8204d
  Args:
    type: :Man
    source: Prince_Henrik
  AssignClass (137a8839-027a-48f9-b635-fc617ed9ce73)
 Call ID: 137a8839-027a-48f9-b635-fc617ed9ce73
  Args:
    source: King_Frederik_X
    type: :Person
  AssignClass (44d5381c-36fc-4f83-a243-20e3deb470ae)
 Call ID: 44d5381c-36fc-4f83-a243-20e3deb470ae
  Args:
    type: :Man
    source: King_Frederik_X
  AssignClass (867f31cd-218e-4ce4-9efd-fefbbac9e6d4)
 Call ID: 867f31cd-218e-4ce4-9efd-fefbbac9e6d4
  Args:
    type: :Person
    source: Prince_Felix
  AssignClass (6537836c-6604-4153-b1dd-1b6d32c18dfc)
 Call ID: 6537836c-6604-4153-b1dd-1b6d32c18dfc
  Args:
    source: Prince_Felix
    type: :Man
  AssignClass (c3f3e590-110d-4b38-afbe-0afd1ff2a186)
 Call ID: c3f3e590-110d-4b38-afbe-0afd1ff2a186
  Args:
    source: Henrik_half_sibling
    type: :Person
  AssignClass (a0a42a74-4a9e-473d-bba6-ec328a5d3cb4)
 Call ID: a0a42a74-4a9e-473d-bba6-ec328a5d3cb4
  Args:
    type: :Man
    source: Henrik_half_sibling
  AssignClass (c7e4f11a-2e41-4144-8b6e-dd3dc8b70e2a)
 Call ID: c7e4f11a-2e41-4144-8b6e-dd3dc8b70e2a
  Args:
    source: Athena_half_sibling
    type: :Person
  AssignClass (d3f36e97-9e5c-4e25-8ef6-60c860bbcc46)
 Call ID: d3f36e97-9e5c-4e25-8ef6-60c860bbcc46
  Args:
    type: :Woman
    source: Athena_half_sibling
  AssignClass (49bf7dc2-af1e-4be9-a156-37031657d806)
 Call ID: 49bf7dc2-af1e-4be9-a156-37031657d806
  Args:
    source: Marie_Cavallier
    type: :Person
  AssignClass (4f1c0efb-86d3-403a-b2f2-9ab944d1f746)
 Call ID: 4f1c0efb-86d3-403a-b2f2-9ab944d1f746
  Args:
    type: :Woman
    source: Marie_Cavallier
  AddTriple (7079d271-23f6-4beb-a8f3-b7684f7fdee8)
 Call ID: 7079d271-23f6-4beb-a8f3-b7684f7fdee8
  Args:
    relation: :hasFather
    target: Prince_Joachim
    source: Prince_Nikolai_of_Denmark
  AddTriple (dcf37042-0b4c-4d38-8b3c-5b3a287bde6e)
 Call ID: dcf37042-0b4c-4d38-8b3c-5b3a287bde6e
  Args:
    target: Alexandra_Countess_of_Frederiksborg
    source: Prince_Nikolai_of_Denmark
    relation: :hasMother
  AddTriple (ad122bd0-50f0-4fb7-bca8-f90ffb2eeb67)
 Call ID: ad122bd0-50f0-4fb7-bca8-f90ffb2eeb67
  Args:
    relation: :hasFather
    source: Prince_Felix
    target: Prince_Joachim
  AddTriple (6c76284b-9d5f-4ad7-85a0-c47c63cdb1d4)
 Call ID: 6c76284b-9d5f-4ad7-85a0-c47c63cdb1d4
  Args:
    source: Prince_Felix
    target: Alexandra_Countess_of_Frederiksborg
    relation: :hasMother
  AddTriple (eb74566d-bcdb-4fce-94cc-95ffbca0baff)
 Call ID: eb74566d-bcdb-4fce-94cc-95ffbca0baff
  Args:
    target: Prince_Joachim
    source: Henrik_half_sibling
    relation: :hasFather
  AddTriple (987a55ed-a65e-4e1c-906f-ae933e7d9cbd)
 Call ID: 987a55ed-a65e-4e1c-906f-ae933e7d9cbd
  Args:
    relation: :hasMother
    source: Henrik_half_sibling
    target: Marie_Cavallier
  AddTriple (f0d7e793-eeb9-4b3f-8af0-43e5d23e0e79)
 Call ID: f0d7e793-eeb9-4b3f-8af0-43e5d23e0e79
  Args:
    source: Athena_half_sibling
    target: Prince_Joachim
    relation: :hasFather
  AddTriple (9cbc6052-6cb6-4fd7-9ec8-1e71d224af57)
 Call ID: 9cbc6052-6cb6-4fd7-9ec8-1e71d224af57
  Args:
    relation: :hasMother
    target: Marie_Cavallier
    source: Athena_half_sibling
  AddTriple (6501d013-fa29-4269-b8a3-62cc2eda4be0)
 Call ID: 6501d013-fa29-4269-b8a3-62cc2eda4be0
  Args:
    target: Prince_Henrik
    source: Prince_Joachim
    relation: :hasFather
  AddTriple (1c567e6e-5544-4310-bfd9-73ce4e82a618)
 Call ID: 1c567e6e-5544-4310-bfd9-73ce4e82a618
  Args:
    relation: :hasMother
    source: Prince_Joachim
    target: Queen_Margrethe_II
  AddLiteral (03bcfc40-ad6b-4322-aa74-4b320fba3efc)
 Call ID: 03bcfc40-ad6b-4322-aa74-4b320fba3efc
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Prince_Nikolai_of_Denmark
    literal_value: 1999
  Finish (50d0cf51-6962-4449-b6ed-33d0e7762881)
 Call ID: 50d0cf51-6962-4449-b6ed-33d0e7762881
  Args: