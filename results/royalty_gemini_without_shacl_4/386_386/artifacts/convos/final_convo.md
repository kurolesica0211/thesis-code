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
  AssignClass (a629cb29-aa73-4cff-b3a4-70031b8cb9d6)
 Call ID: a629cb29-aa73-4cff-b3a4-70031b8cb9d6
  Args:
    type: :Man
    source: Karl_Franz_of_Prussia
  AssignClass (b52bacfa-1a20-47bb-8879-f05b85b361c8)
 Call ID: b52bacfa-1a20-47bb-8879-f05b85b361c8
  Args:
    type: :Person
    source: Karl_Franz_of_Prussia
  AddLiteral (41e0fec3-e75b-4940-97b0-cf2f0b8b4c6e)
 Call ID: 41e0fec3-e75b-4940-97b0-cf2f0b8b4c6e
  Args:
    literal_value: 1916
    source: Karl_Franz_of_Prussia
    relation: :hasBirthYear
    literal_type: xsd:nonNegativeInteger
  AddLiteral (d1e682e0-ef81-4c02-acc9-ef44976552c0)
 Call ID: d1e682e0-ef81-4c02-acc9-ef44976552c0
  Args:
    literal_type: xsd:nonNegativeInteger
    relation: :hasDeathYear
    source: Karl_Franz_of_Prussia
    literal_value: 1975
  AssignClass (3c0a27b4-d735-4ac3-9418-4ca13c8b52f6)
 Call ID: 3c0a27b4-d735-4ac3-9418-4ca13c8b52f6
  Args:
    type: :Man
    source: Joachim_of_Prussia
  AssignClass (f236be06-8116-4a5b-98b7-edd795725691)
 Call ID: f236be06-8116-4a5b-98b7-edd795725691
  Args:
    type: :Person
    source: Joachim_of_Prussia
  AssignClass (17e10020-3e0e-4052-aa37-e7af865d47f7)
 Call ID: 17e10020-3e0e-4052-aa37-e7af865d47f7
  Args:
    type: :Woman
    source: Marie_Auguste_of_Anhalt
  AssignClass (6ef9dbae-d25e-46c1-a56c-09afd55ea3fb)
 Call ID: 6ef9dbae-d25e-46c1-a56c-09afd55ea3fb
  Args:
    type: :Person
    source: Marie_Auguste_of_Anhalt
  AddTriple (3f4fdc8c-586c-4276-8afe-ebd813320510)
 Call ID: 3f4fdc8c-586c-4276-8afe-ebd813320510
  Args:
    relation: :hasFather
    target: Joachim_of_Prussia
    source: Karl_Franz_of_Prussia
  AddTriple (7262ea73-f571-4227-a4b1-69cde369c37f)
 Call ID: 7262ea73-f571-4227-a4b1-69cde369c37f
  Args:
    relation: :hasMother
    target: Marie_Auguste_of_Anhalt
    source: Karl_Franz_of_Prussia
  AssignClass (2546481b-1eaa-4fe3-9902-56fd7cf93001)
 Call ID: 2546481b-1eaa-4fe3-9902-56fd7cf93001
  Args:
    type: :Man
    source: Wilhelm_II
  AssignClass (e3a269c6-abeb-4281-a650-4e46ab7ce6dd)
 Call ID: e3a269c6-abeb-4281-a650-4e46ab7ce6dd
  Args:
    type: :Person
    source: Wilhelm_II
  AddTriple (577cfe9c-0b9b-4575-bfd1-4312cf126749)
 Call ID: 577cfe9c-0b9b-4575-bfd1-4312cf126749
  Args:
    target: Wilhelm_II
    relation: :hasAncestor
    source: Karl_Franz_of_Prussia
  AssignClass (cc4aaa94-6bc8-4550-99f2-e323ab9252a0)
 Call ID: cc4aaa94-6bc8-4550-99f2-e323ab9252a0
  Args:
    type: :Man
    source: Eitel_Friedrich_of_Prussia
  AssignClass (e24fd918-f38a-41e8-80ac-37f6a1bd93a1)
 Call ID: e24fd918-f38a-41e8-80ac-37f6a1bd93a1
  Args:
    type: :Person
    source: Eitel_Friedrich_of_Prussia
  AddTriple (e37799e6-49a7-4204-81f1-096e732977cf)
 Call ID: e37799e6-49a7-4204-81f1-096e732977cf
  Args:
    target: Eitel_Friedrich_of_Prussia
    relation: :hasBrother
    source: Joachim_of_Prussia
  AssignClass (041872d8-828f-432a-8576-47f84d30fdf6)
 Call ID: 041872d8-828f-432a-8576-47f84d30fdf6
  Args:
    type: :Woman
    source: Henriette_of_Schoenaich_Carolath
  AssignClass (001ab79f-10d1-4d26-8a72-59e4d2222f1c)
 Call ID: 001ab79f-10d1-4d26-8a72-59e4d2222f1c
  Args:
    type: :Person
    source: Henriette_of_Schoenaich_Carolath
  AddTriple (6dfce348-a071-4242-95b6-a6773de65527)
 Call ID: 6dfce348-a071-4242-95b6-a6773de65527
  Args:
    source: Karl_Franz_of_Prussia
    relation: :hasRelation
    target: Henriette_of_Schoenaich_Carolath
  AddLiteral (c3b3d6fb-2b72-4a9a-a8fb-8d7675d91031)
 Call ID: c3b3d6fb-2b72-4a9a-a8fb-8d7675d91031
  Args:
    source: Karl_Franz_of_Prussia
    literal_value: 1940
    literal_type: xsd:nonNegativeInteger
    relation: :hasMarriageYear
  AssignClass (c1f9cc11-d852-40fa-a3d2-94c031aebdac)
 Call ID: c1f9cc11-d852-40fa-a3d2-94c031aebdac
  Args:
    type: :Woman
    source: Hermine_Reuss_of_Greiz
  AssignClass (98983d0c-fc78-4c50-869e-6aec4ccf72ef)
 Call ID: 98983d0c-fc78-4c50-869e-6aec4ccf72ef
  Args:
    type: :Person
    source: Hermine_Reuss_of_Greiz
  AddTriple (47d8bb5c-bf0c-4d6f-ad98-290003f0c410)
 Call ID: 47d8bb5c-bf0c-4d6f-ad98-290003f0c410
  Args:
    source: Henriette_of_Schoenaich_Carolath
    target: Hermine_Reuss_of_Greiz
    relation: :hasMother
  AssignClass (4c4b8e45-e152-42a2-9718-6c1b13980dea)
 Call ID: 4c4b8e45-e152-42a2-9718-6c1b13980dea
  Args:
    type: :Woman
    source: Luise_Dora_Hartmann
  AssignClass (7c4562bb-1a55-4337-b876-80a34c9019b2)
 Call ID: 7c4562bb-1a55-4337-b876-80a34c9019b2
  Args:
    type: :Person
    source: Luise_Dora_Hartmann
  AddTriple (c85cd71d-16e1-4c06-b952-9fc8ed921873)
 Call ID: c85cd71d-16e1-4c06-b952-9fc8ed921873
  Args:
    source: Karl_Franz_of_Prussia
    target: Luise_Dora_Hartmann
    relation: :hasRelation
  AddLiteral (24d44fba-a41c-4eb9-ae30-a87bbd5b0286)
 Call ID: 24d44fba-a41c-4eb9-ae30-a87bbd5b0286
  Args:
    literal_type: xsd:nonNegativeInteger
    relation: :hasMarriageYear
    literal_value: 1946
    source: Karl_Franz_of_Prussia
  AssignClass (8757f93a-4b55-4f3c-858d-b978af51ccf3)
 Call ID: 8757f93a-4b55-4f3c-858d-b978af51ccf3
  Args:
    type: :Woman
    source: Eva_Maria_Herrera_y_Valdeavellano
  AssignClass (be53a7dc-8f22-435b-8c2f-29e7889fd539)
 Call ID: be53a7dc-8f22-435b-8c2f-29e7889fd539
  Args:
    type: :Person
    source: Eva_Maria_Herrera_y_Valdeavellano
  AddTriple (d220c190-301f-4a34-b4f4-3b051dfe2b7b)
 Call ID: d220c190-301f-4a34-b4f4-3b051dfe2b7b
  Args:
    target: Eva_Maria_Herrera_y_Valdeavellano
    relation: :hasRelation
    source: Karl_Franz_of_Prussia
  AddLiteral (ac26f541-6dc7-4d0a-88e4-524943169e39)
 Call ID: ac26f541-6dc7-4d0a-88e4-524943169e39
  Args:
    source: Karl_Franz_of_Prussia
    literal_value: 1959
    relation: :hasMarriageYear
    literal_type: xsd:nonNegativeInteger
  Finish (68ea41b5-64a5-4894-8eb0-2b05c880d06f)
 Call ID: 68ea41b5-64a5-4894-8eb0-2b05c880d06f
  Args: