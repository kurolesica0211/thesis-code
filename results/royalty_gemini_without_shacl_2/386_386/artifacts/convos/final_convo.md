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
Prince Karl Franz Josef Wilhelm Friedrich Eduard Paul of Prussia (15 December 1916 – 23 January 1975) was the only child of Prince Joachim of Prussia and Princess Marie-Auguste of Anhalt.
He was also a grandson of Wilhelm II, German Emperor.
Early life

Prince Karl Franz was born on 15 December 1916 in Potsdam.
He was the only child born to Prince Joachim of Prussia and Princess Marie-Auguste of Anhalt and was the Emperor's fourth grandchild to be born since World War I began; he was consequently very young when Hohenzollern fortunes fell.
His grandfather abdicated in 1918, and his father, Prince Joachim, committed suicide in 1920.
At the time of his grandfather's abdication, Prince Karl Franz was twelfth in line of succession to the German and Prussian thrones.
After his father's suicide, Karl Franz was taken into custody by his paternal uncle, Prince Eitel Friedrich of Prussia.
As the legal head of the House of Hohenzollern, he claimed this right because Emperor Wilhelm had issued an edict placing Hohenzollern powers in Eitel's hands.
Eitel's defence had also stated that Marie-Auguste was not a fit person for Karl Franz's guardianship.
Marie-Auguste went to court however and made a plea that she was heartbroken, which may have helped win the case for her.
In 1922, Marie-Auguste sued ex-Emperor Wilhelm for financial support that had been promised in her and Joachim's marriage contract.
Wilhelm's attorney argued that the House of Hohenzollern laws were no longer valid, and therefore there was no obligation to support her.
In World War II, Karl Franz served as a lieutenant in an armoured car division, and at one point was stationed on the Polish front.
Marriages

First

On 1 October 1940, Karl Franz married Princess Henriette Hermine Wanda Ida Luise of Schönaich-Carolath.
She was the daughter of Princess Hermine Reuss of Greiz, who had been the second wife of Karl Franz's grandfather Emperor Wilhelm II since 1922 (Henriette was thus Kaiser Wilhelm's stepdaughter).
Held at Wilhelm's private residence without much ceremony, he and Hermine attended the ceremony, as did a few other guests.
Second

Karl Franz married secondly, on 9 November 1946, to Luise Dora Hartmann (5 September 1909 Hamburg, Germany –
Third

Karl Franz married lastly, on 20 July 1959 in Lima, Peru, Eva Maria Herrera y Valdeavellano (10 June 1922 Lima, Peru – 6 March 1987 Lima, Peru).
They were married until Prince Karl's death and had two daughters:


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
  AssignClass (acf35f8e-c48c-499d-b2db-57dcac3402b7)
 Call ID: acf35f8e-c48c-499d-b2db-57dcac3402b7
  Args:
    source: Karl_Franz_of_Prussia
    type: :Man
  AssignClass (c46cedec-e264-4bd2-9774-b9f44517a727)
 Call ID: c46cedec-e264-4bd2-9774-b9f44517a727
  Args:
    source: Karl_Franz_of_Prussia
    type: :Person
  AddLiteral (42467616-0991-4736-b0b1-5822d26672b1)
 Call ID: 42467616-0991-4736-b0b1-5822d26672b1
  Args:
    literal_value: 1916
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Karl_Franz_of_Prussia
  AddLiteral (5b743353-34fd-4c44-91b8-8b37d5d74196)
 Call ID: 5b743353-34fd-4c44-91b8-8b37d5d74196
  Args:
    relation: :hasDeathYear
    literal_value: 1975
    source: Karl_Franz_of_Prussia
    literal_type: xsd:integer
  AssignClass (184190b0-ce17-442e-8a7c-e0f8320599a6)
 Call ID: 184190b0-ce17-442e-8a7c-e0f8320599a6
  Args:
    source: Joachim_of_Prussia
    type: :Man
  AssignClass (b21565c3-d7a1-4bd0-915e-bfa58ccabdb3)
 Call ID: b21565c3-d7a1-4bd0-915e-bfa58ccabdb3
  Args:
    source: Joachim_of_Prussia
    type: :Person
  AddTriple (14a49e0c-e9e1-4e0b-a27a-32d111e05c7a)
 Call ID: 14a49e0c-e9e1-4e0b-a27a-32d111e05c7a
  Args:
    source: Karl_Franz_of_Prussia
    relation: :hasFather
    target: Joachim_of_Prussia
  AssignClass (a97e524a-dcee-4cea-8697-fc98ecf4b18f)
 Call ID: a97e524a-dcee-4cea-8697-fc98ecf4b18f
  Args:
    source: Marie-Auguste_of_Anhalt
    type: :Woman
  AssignClass (3a1f8265-3bb7-4747-85a0-1791d4fc850f)
 Call ID: 3a1f8265-3bb7-4747-85a0-1791d4fc850f
  Args:
    source: Marie-Auguste_of_Anhalt
    type: :Person
  AddTriple (fc699ee4-6072-4267-9d71-5c1ec542fac9)
 Call ID: fc699ee4-6072-4267-9d71-5c1ec542fac9
  Args:
    relation: :hasMother
    target: Marie-Auguste_of_Anhalt
    source: Karl_Franz_of_Prussia
  AssignClass (ead80bc7-7144-4133-8f87-be4722e28be6)
 Call ID: ead80bc7-7144-4133-8f87-be4722e28be6
  Args:
    source: Wilhelm_II
    type: :Man
  AssignClass (68646c81-b689-4e0c-8a7b-384c8407c3f2)
 Call ID: 68646c81-b689-4e0c-8a7b-384c8407c3f2
  Args:
    type: :Person
    source: Wilhelm_II
  AddTriple (74492240-aac5-46f4-bb20-d93dee1b7cf1)
 Call ID: 74492240-aac5-46f4-bb20-d93dee1b7cf1
  Args:
    source: Joachim_of_Prussia
    relation: :hasFather
    target: Wilhelm_II
  AssignClass (815a85b1-5d16-4b11-a955-1b21bc9d905b)
 Call ID: 815a85b1-5d16-4b11-a955-1b21bc9d905b
  Args:
    type: :Man
    source: Eitel_Friedrich_of_Prussia
  AssignClass (c0c57ae3-cac2-4367-b0c9-f3c3f3d25daf)
 Call ID: c0c57ae3-cac2-4367-b0c9-f3c3f3d25daf
  Args:
    type: :Person
    source: Eitel_Friedrich_of_Prussia
  AddTriple (82f3898e-6d21-4406-b8a5-dc4d8f307080)
 Call ID: 82f3898e-6d21-4406-b8a5-dc4d8f307080
  Args:
    relation: :hasFather
    target: Wilhelm_II
    source: Eitel_Friedrich_of_Prussia
  AssignClass (b0be8743-0d29-4467-bd8b-5885527c9fcd)
 Call ID: b0be8743-0d29-4467-bd8b-5885527c9fcd
  Args:
    source: Henriette_of_Schoenaich-Carolath
    type: :Woman
  AssignClass (ed3545b7-2058-43ae-98d0-ea0e3b09366e)
 Call ID: ed3545b7-2058-43ae-98d0-ea0e3b09366e
  Args:
    source: Henriette_of_Schoenaich-Carolath
    type: :Person
  AddTriple (46a154d8-5677-4ba0-9685-26a7cdf58c63)
 Call ID: 46a154d8-5677-4ba0-9685-26a7cdf58c63
  Args:
    relation: :hasRelation
    target: Henriette_of_Schoenaich-Carolath
    source: Karl_Franz_of_Prussia
  AddLiteral (cc181940-e072-4b30-8465-3fa1abdef6f1)
 Call ID: cc181940-e072-4b30-8465-3fa1abdef6f1
  Args:
    literal_value: 1940
    relation: :hasMarriageYear
    source: Karl_Franz_of_Prussia
    literal_type: xsd:integer
  AssignClass (d187a9a7-2bca-4b4c-a7c6-4099968994c3)
 Call ID: d187a9a7-2bca-4b4c-a7c6-4099968994c3
  Args:
    source: Hermine_Reuss_of_Greiz
    type: :Woman
  AssignClass (81ce0c50-18fa-4a68-adcf-c9bcb5d908e4)
 Call ID: 81ce0c50-18fa-4a68-adcf-c9bcb5d908e4
  Args:
    source: Hermine_Reuss_of_Greiz
    type: :Person
  AddTriple (8018bddd-b5a3-4bc0-a797-e93b4d9d963d)
 Call ID: 8018bddd-b5a3-4bc0-a797-e93b4d9d963d
  Args:
    source: Henriette_of_Schoenaich-Carolath
    relation: :hasMother
    target: Hermine_Reuss_of_Greiz
  AddTriple (1e669149-c24f-4d7e-8524-5a6d5920b3a0)
 Call ID: 1e669149-c24f-4d7e-8524-5a6d5920b3a0
  Args:
    source: Wilhelm_II
    target: Hermine_Reuss_of_Greiz
    relation: :hasRelation
  AddLiteral (f623c546-d048-4db8-bdd1-e46431abb95e)
 Call ID: f623c546-d048-4db8-bdd1-e46431abb95e
  Args:
    relation: :hasMarriageYear
    literal_value: 1922
    literal_type: xsd:integer
    source: Wilhelm_II
  AssignClass (65699872-e9fb-4196-b522-396d32cedbb5)
 Call ID: 65699872-e9fb-4196-b522-396d32cedbb5
  Args:
    source: Luise_Dora_Hartmann
    type: :Woman
  AssignClass (3d152e68-a45a-4e1a-9879-9f36757fc7c3)
 Call ID: 3d152e68-a45a-4e1a-9879-9f36757fc7c3
  Args:
    type: :Person
    source: Luise_Dora_Hartmann
  AddTriple (9ee63ec4-0ca0-45b3-b09b-5b9120108264)
 Call ID: 9ee63ec4-0ca0-45b3-b09b-5b9120108264
  Args:
    source: Karl_Franz_of_Prussia
    relation: :hasRelation
    target: Luise_Dora_Hartmann
  AddLiteral (141427bb-8251-46d3-8648-8c796c009efa)
 Call ID: 141427bb-8251-46d3-8648-8c796c009efa
  Args:
    literal_value: 1946
    relation: :hasMarriageYear
    source: Karl_Franz_of_Prussia
    literal_type: xsd:integer
  AssignClass (4b9859c5-6ebc-4211-bb56-402813143e6f)
 Call ID: 4b9859c5-6ebc-4211-bb56-402813143e6f
  Args:
    type: :Woman
    source: Eva_Maria_Herrera_y_Valdeavellano
  AssignClass (1a5f9c38-56a5-4abb-b55f-d730f079503e)
 Call ID: 1a5f9c38-56a5-4abb-b55f-d730f079503e
  Args:
    source: Eva_Maria_Herrera_y_Valdeavellano
    type: :Person
  AddTriple (5584ce2f-f04b-4080-8079-26b60419e57d)
 Call ID: 5584ce2f-f04b-4080-8079-26b60419e57d
  Args:
    source: Karl_Franz_of_Prussia
    relation: :hasRelation
    target: Eva_Maria_Herrera_y_Valdeavellano
  AddLiteral (42d8c702-ec44-4d8e-a8c5-5cceb248a2f5)
 Call ID: 42d8c702-ec44-4d8e-a8c5-5cceb248a2f5
  Args:
    source: Karl_Franz_of_Prussia
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 1959
  Finish (4300104e-c3b6-4d13-83e7-e23cbc3e279a)
 Call ID: 4300104e-c3b6-4d13-83e7-e23cbc3e279a
  Args: