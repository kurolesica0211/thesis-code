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
  AssignClass (8109bd37-848b-49dc-a86b-3e307acaa36a)
 Call ID: 8109bd37-848b-49dc-a86b-3e307acaa36a
  Args:
    type: :Man
    source: Karl_Franz_of_Prussia
  AssignClass (925fd2f0-5bfd-4bfa-af72-2cdc2aee43f4)
 Call ID: 925fd2f0-5bfd-4bfa-af72-2cdc2aee43f4
  Args:
    type: :Person
    source: Karl_Franz_of_Prussia
  AddLiteral (31470290-1cea-47f8-b389-33f7270178b5)
 Call ID: 31470290-1cea-47f8-b389-33f7270178b5
  Args:
    relation: :hasBirthYear
    literal_value: 1916
    literal_type: xsd:integer
    source: Karl_Franz_of_Prussia
  AddLiteral (ab332350-53f2-44f6-bac8-8c97c176424e)
 Call ID: ab332350-53f2-44f6-bac8-8c97c176424e
  Args:
    relation: :hasDeathYear
    literal_value: 1975
    source: Karl_Franz_of_Prussia
    literal_type: xsd:integer
  AssignClass (fc519733-028c-46e3-8a0b-bf10abaa0906)
 Call ID: fc519733-028c-46e3-8a0b-bf10abaa0906
  Args:
    type: :Man
    source: Joachim_of_Prussia
  AssignClass (e8e13f29-3cda-4e93-b8fa-35ec30dea7a8)
 Call ID: e8e13f29-3cda-4e93-b8fa-35ec30dea7a8
  Args:
    type: :Person
    source: Joachim_of_Prussia
  AssignClass (f27e5b71-186b-4516-a9ed-c0fcced9eff1)
 Call ID: f27e5b71-186b-4516-a9ed-c0fcced9eff1
  Args:
    source: Marie-Auguste_of_Anhalt
    type: :Woman
  AssignClass (114f413a-b69e-4728-a85a-b37b437bd283)
 Call ID: 114f413a-b69e-4728-a85a-b37b437bd283
  Args:
    source: Marie-Auguste_of_Anhalt
    type: :Person
  AddTriple (f1e188c8-2b41-4101-92bc-93b12f473045)
 Call ID: f1e188c8-2b41-4101-92bc-93b12f473045
  Args:
    relation: :hasFather
    target: Joachim_of_Prussia
    source: Karl_Franz_of_Prussia
  AddTriple (65fb103f-298a-44aa-87b1-9a7d4360fef5)
 Call ID: 65fb103f-298a-44aa-87b1-9a7d4360fef5
  Args:
    relation: :hasMother
    target: Marie-Auguste_of_Anhalt
    source: Karl_Franz_of_Prussia
  AssignClass (baf207c1-ec0b-4030-be2b-d1c06cd7a5d3)
 Call ID: baf207c1-ec0b-4030-be2b-d1c06cd7a5d3
  Args:
    source: Wilhelm_II
    type: :Man
  AssignClass (1b233170-0095-4712-b28f-c9dd863dec42)
 Call ID: 1b233170-0095-4712-b28f-c9dd863dec42
  Args:
    source: Wilhelm_II
    type: :Person
  AddTriple (2316d7dd-4f32-440b-9cbb-f1eee81775fa)
 Call ID: 2316d7dd-4f32-440b-9cbb-f1eee81775fa
  Args:
    source: Karl_Franz_of_Prussia
    target: Wilhelm_II
    relation: :hasAncestor
  AssignClass (3f0b7afa-cb7a-43de-b997-08c39f86d1a7)
 Call ID: 3f0b7afa-cb7a-43de-b997-08c39f86d1a7
  Args:
    type: :Man
    source: Eitel_Friedrich_of_Prussia
  AssignClass (03052a9f-1303-4938-8f97-4a094fee6dba)
 Call ID: 03052a9f-1303-4938-8f97-4a094fee6dba
  Args:
    type: :Person
    source: Eitel_Friedrich_of_Prussia
  AssignClass (edf1b29a-0286-444b-8ad6-1b6a76c334ce)
 Call ID: edf1b29a-0286-444b-8ad6-1b6a76c334ce
  Args:
    type: :Woman
    source: Henriette_Hermine_Wanda_Ida_Luise_of_Schönaich-Carolath
  AssignClass (48d090ae-3686-4ead-b5a2-ae76b3d39e4b)
 Call ID: 48d090ae-3686-4ead-b5a2-ae76b3d39e4b
  Args:
    type: :Person
    source: Henriette_Hermine_Wanda_Ida_Luise_of_Schönaich-Carolath
  AddLiteral (3536fa08-6805-4c40-9559-0f086c8a8b96)
 Call ID: 3536fa08-6805-4c40-9559-0f086c8a8b96
  Args:
    literal_type: xsd:integer
    source: Karl_Franz_of_Prussia
    literal_value: 1940
    relation: :hasMarriageYear
  AssignClass (ef75f70a-c8fa-4ea5-8131-d900f20432e1)
 Call ID: ef75f70a-c8fa-4ea5-8131-d900f20432e1
  Args:
    type: :Woman
    source: Hermine_Reuss_of_Greiz
  AssignClass (6f484da5-b1aa-4a91-a4f2-1e2f48f0fbda)
 Call ID: 6f484da5-b1aa-4a91-a4f2-1e2f48f0fbda
  Args:
    source: Hermine_Reuss_of_Greiz
    type: :Person
  AddTriple (095b8231-a80b-4272-9090-208a64059c19)
 Call ID: 095b8231-a80b-4272-9090-208a64059c19
  Args:
    source: Henriette_Hermine_Wanda_Ida_Luise_of_Schönaich-Carolath
    relation: :hasMother
    target: Hermine_Reuss_of_Greiz
  AssignClass (32a70356-b2d6-4c05-9ddb-7131fb658435)
 Call ID: 32a70356-b2d6-4c05-9ddb-7131fb658435
  Args:
    type: :Woman
    source: Luise_Dora_Hartmann
  AssignClass (a3e54f14-695d-43b9-92ed-92a5c94a3f66)
 Call ID: a3e54f14-695d-43b9-92ed-92a5c94a3f66
  Args:
    source: Luise_Dora_Hartmann
    type: :Person
  AddLiteral (743f78f2-913f-4484-8774-495d4bf85841)
 Call ID: 743f78f2-913f-4484-8774-495d4bf85841
  Args:
    literal_type: xsd:integer
    source: Karl_Franz_of_Prussia
    literal_value: 1946
    relation: :hasMarriageYear
  AssignClass (9c5151a5-bf30-4738-89bb-50a0359d8ad4)
 Call ID: 9c5151a5-bf30-4738-89bb-50a0359d8ad4
  Args:
    source: Eva_Maria_Herrera_y_Valdeavellano
    type: :Woman
  AssignClass (b6b9d99c-c873-4b83-abaf-92bca2b129eb)
 Call ID: b6b9d99c-c873-4b83-abaf-92bca2b129eb
  Args:
    source: Eva_Maria_Herrera_y_Valdeavellano
    type: :Person
  AddLiteral (3bd7cc1d-88a8-4b06-882f-6bf16ad98f20)
 Call ID: 3bd7cc1d-88a8-4b06-882f-6bf16ad98f20
  Args:
    source: Karl_Franz_of_Prussia
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 1959
  Finish (d43e7011-2b38-443f-8f8c-0d4cf58965a1)
 Call ID: d43e7011-2b38-443f-8f8c-0d4cf58965a1
  Args: