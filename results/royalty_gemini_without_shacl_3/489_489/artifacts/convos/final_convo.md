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
Wilhelm Karl Adalbert Erich Detloff Prinz von Preussen (30 January 1922 in Potsdam – 9 April 2007 in Holzminden) was the third son of Prince Oskar of Prussia, and the last surviving grandson of Wilhelm II, the last German Emperor.
Biography

Wilhelm-Karl was the youngest of Prince Oskar of Prussia and Countess Ina Marie von Bassewitz's four children.
Wilhelm-Karl worked tirelessly to keep the Order intact during the Cold War and helped to reunite its membership after the fall of East Germany.
Amongst other orders and awards, Wilhelm-Karl received the Grand Merit Cross (with star) of the Order of Merit of the Federal Republic of Germany and the Grand Cross of the Order pro merito Melitensi of the Sovereign Military Order of Malta.
Marriage and issue

In 1952, Wilhelm-Karl married Armgard Else Helene von Veltheim (17 February 1926 - 1 November 2019), daughter of Friedrich von Veltheim (1881–1955) and his wife, Ottonie von Alvensleben (1883–1960).



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
  AssignClass (20835416-86f8-47b0-8d09-7d3e51b7860b)
 Call ID: 20835416-86f8-47b0-8d09-7d3e51b7860b
  Args:
    source: :Wilhelm_Karl_Prinz_von_Preussen
    type: :Man
  AssignClass (4c1900f9-c6a1-42c4-8779-980bb89df5a1)
 Call ID: 4c1900f9-c6a1-42c4-8779-980bb89df5a1
  Args:
    type: :Person
    source: :Wilhelm_Karl_Prinz_von_Preussen
  AddLiteral (a413961b-dd71-4420-b7ba-5d7596894b45)
 Call ID: a413961b-dd71-4420-b7ba-5d7596894b45
  Args:
    source: :Wilhelm_Karl_Prinz_von_Preussen
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1922
  AddLiteral (bb4df022-d410-4792-a948-8d813faab865)
 Call ID: bb4df022-d410-4792-a948-8d813faab865
  Args:
    source: :Wilhelm_Karl_Prinz_von_Preussen
    literal_value: 2007
    relation: :hasDeathYear
    literal_type: xsd:integer
  AssignClass (57c803d2-ab3f-4bd0-9264-0e30aa848842)
 Call ID: 57c803d2-ab3f-4bd0-9264-0e30aa848842
  Args:
    source: :Prince_Oskar_of_Prussia
    type: :Man
  AssignClass (4bb9aba8-df33-4694-8701-4730919e1b89)
 Call ID: 4bb9aba8-df33-4694-8701-4730919e1b89
  Args:
    source: :Prince_Oskar_of_Prussia
    type: :Person
  AssignClass (929b30bd-c750-4627-861a-e3a38013ff36)
 Call ID: 929b30bd-c750-4627-861a-e3a38013ff36
  Args:
    source: :Countess_Ina_Marie_von_Bassewitz
    type: :Woman
  AssignClass (32ccd23a-42f7-4b6b-b3dd-0627aa815bc3)
 Call ID: 32ccd23a-42f7-4b6b-b3dd-0627aa815bc3
  Args:
    source: :Countess_Ina_Marie_von_Bassewitz
    type: :Person
  AddTriple (6a951e2f-4cfa-4092-8261-1b1de1917635)
 Call ID: 6a951e2f-4cfa-4092-8261-1b1de1917635
  Args:
    source: :Wilhelm_Karl_Prinz_von_Preussen
    relation: :hasFather
    target: :Prince_Oskar_of_Prussia
  AddTriple (f55f3ab2-5871-4c44-ba26-e81c740486fe)
 Call ID: f55f3ab2-5871-4c44-ba26-e81c740486fe
  Args:
    target: :Countess_Ina_Marie_von_Bassewitz
    source: :Wilhelm_Karl_Prinz_von_Preussen
    relation: :hasMother
  AssignClass (216a86fb-555f-49f1-a654-2874dcc61a42)
 Call ID: 216a86fb-555f-49f1-a654-2874dcc61a42
  Args:
    type: :Woman
    source: :Armgard_Else_Helene_von_Veltheim
  AssignClass (2e947d4d-effa-47ac-be35-58fc4715b46b)
 Call ID: 2e947d4d-effa-47ac-be35-58fc4715b46b
  Args:
    type: :Person
    source: :Armgard_Else_Helene_von_Veltheim
  AddLiteral (4043553b-7614-4a02-9dee-2b5ad4f2cdce)
 Call ID: 4043553b-7614-4a02-9dee-2b5ad4f2cdce
  Args:
    literal_value: 1952
    literal_type: xsd:integer
    relation: :hasMarriageYear
    source: :Wilhelm_Karl_Prinz_von_Preussen
  AddTriple (20e9e260-bab2-431c-a6bc-b1b542be59ba)
 Call ID: 20e9e260-bab2-431c-a6bc-b1b542be59ba
  Args:
    target: :Armgard_Else_Helene_von_Veltheim
    source: :Wilhelm_Karl_Prinz_von_Preussen
    relation: :hasRelation
  AddLiteral (009f5609-df42-40b4-bd8a-7d6b6e042d02)
 Call ID: 009f5609-df42-40b4-bd8a-7d6b6e042d02
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1926
    source: :Armgard_Else_Helene_von_Veltheim
  AddLiteral (8c4ccaac-29ea-4586-94fb-eddc759e3926)
 Call ID: 8c4ccaac-29ea-4586-94fb-eddc759e3926
  Args:
    source: :Armgard_Else_Helene_von_Veltheim
    literal_value: 2019
    literal_type: xsd:integer
    relation: :hasDeathYear
  AssignClass (e66093ff-4378-4785-a523-782dbfe5a1ae)
 Call ID: e66093ff-4378-4785-a523-782dbfe5a1ae
  Args:
    type: :Man
    source: :Friedrich_von_Veltheim
  AssignClass (b5a4fb4d-7e13-4fa8-89da-2328f874c97e)
 Call ID: b5a4fb4d-7e13-4fa8-89da-2328f874c97e
  Args:
    type: :Person
    source: :Friedrich_von_Veltheim
  AddLiteral (6c55a7b1-8923-422a-9ed9-e646a3556606)
 Call ID: 6c55a7b1-8923-422a-9ed9-e646a3556606
  Args:
    source: :Friedrich_von_Veltheim
    literal_value: 1881
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (95c6c8d4-f2fb-4726-b496-40d541758b4f)
 Call ID: 95c6c8d4-f2fb-4726-b496-40d541758b4f
  Args:
    source: :Friedrich_von_Veltheim
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1955
  AssignClass (a57673cf-7334-4751-a608-2c8125ee73b7)
 Call ID: a57673cf-7334-4751-a608-2c8125ee73b7
  Args:
    source: :Ottonie_von_Alvensleben
    type: :Woman
  AssignClass (74571386-b762-488a-8d8e-0460d3d60587)
 Call ID: 74571386-b762-488a-8d8e-0460d3d60587
  Args:
    source: :Ottonie_von_Alvensleben
    type: :Person
  AddLiteral (71c00a3d-cf62-4021-9497-9745fad0271f)
 Call ID: 71c00a3d-cf62-4021-9497-9745fad0271f
  Args:
    source: :Ottonie_von_Alvensleben
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1883
  AddLiteral (f3e6c726-10da-4054-a628-07593387393a)
 Call ID: f3e6c726-10da-4054-a628-07593387393a
  Args:
    literal_value: 1960
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: :Ottonie_von_Alvensleben
  AddTriple (dae13b6d-7516-435f-b6cb-8b851a3776f8)
 Call ID: dae13b6d-7516-435f-b6cb-8b851a3776f8
  Args:
    target: :Friedrich_von_Veltheim
    relation: :hasFather
    source: :Armgard_Else_Helene_von_Veltheim
  AddTriple (125f0dd9-9b3a-441e-a72d-2b388c8b3cc4)
 Call ID: 125f0dd9-9b3a-441e-a72d-2b388c8b3cc4
  Args:
    target: :Ottonie_von_Alvensleben
    source: :Armgard_Else_Helene_von_Veltheim
    relation: :hasMother
  Finish (64ae4e9f-8952-4571-9acd-2bac51021d51)
 Call ID: 64ae4e9f-8952-4571-9acd-2bac51021d51
  Args: