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
Moritz, Landgrave of Hesse (legally Moritz Friedrich Karl Emanuel Humbert Prinz und Landgraf von Hessen; 6 August 1926 – 23 May 2013) was the son of Prince Philip, Landgrave of Hesse, and the head of the House of Hesse, also known as the House of Brabant.
Life

Landgrave Moritz was born at Racconigi Castle, in Italy.
During the Second World War, Moritz's mother, Princess Mafalda of Savoy, was arrested by the Nazis for alleged subversive activities and died in the Buchenwald concentration camp in 1944 as a result of a U.S. bombing raid on the camp.
Moritz and his siblings (Heinrich, Otto and Elisabeth) were given sanctuary in the Vatican under the care of their uncle Louis, Prince of Hesse and by Rhine and aunt Margaret Campbell Geddes who adopted them.
Prince Louis of Hesse and by Rhine, the last head of the Hesse-Darmstadt line, died in 1968, at which time Moritz's father succeeded him as head of the entire house.
Moritz became the head of the House of Hesse after the death of his father Philip on 25 October 1980.
Moritz was a world-famous art collector.
He presided over the Foundation of the House of Hesse which is the proprietor of the Kronberg Palace Hotel and several manor estates and palaces.
Marriage and children

Moritz married Princess Tatiana of Sayn-Wittgenstein-Berleburg, daughter of Prince Gustav Albrecht.



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
  AssignClass (02845d1e-ae18-496e-843b-cb9765b214de)
 Call ID: 02845d1e-ae18-496e-843b-cb9765b214de
  Args:
    source: Moritz
    type: :Man
  AddLiteral (570dc87b-93cc-4068-8d41-426de0bde0fe)
 Call ID: 570dc87b-93cc-4068-8d41-426de0bde0fe
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Moritz
    literal_value: 1926
  AddLiteral (ea70b542-7fa9-472c-bcc8-1a70fd8f8efa)
 Call ID: ea70b542-7fa9-472c-bcc8-1a70fd8f8efa
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: Moritz
    literal_value: 2013
  AssignClass (0c656a68-af27-46a1-95a6-bb1717cbf685)
 Call ID: 0c656a68-af27-46a1-95a6-bb1717cbf685
  Args:
    source: Philip
    type: :Man
  AddTriple (7f4743a3-a4be-4303-af62-29f56de1f896)
 Call ID: 7f4743a3-a4be-4303-af62-29f56de1f896
  Args:
    target: Philip
    source: Moritz
    relation: :hasFather
  AssignClass (cd18320e-5532-4289-b743-88a8f45f8723)
 Call ID: cd18320e-5532-4289-b743-88a8f45f8723
  Args:
    source: Mafalda_of_Savoy
    type: :Woman
  AddTriple (f31a262d-d20c-4fe4-8fcd-1ae31f67b90b)
 Call ID: f31a262d-d20c-4fe4-8fcd-1ae31f67b90b
  Args:
    relation: :hasMother
    target: Mafalda_of_Savoy
    source: Moritz
  AddLiteral (a265c8fd-6e8d-44b3-be13-a08f891344ca)
 Call ID: a265c8fd-6e8d-44b3-be13-a08f891344ca
  Args:
    literal_value: 1944
    relation: :hasDeathYear
    source: Mafalda_of_Savoy
    literal_type: xsd:integer
  AssignClass (5937d16b-edbb-4f30-a2bb-1c2bd792a1f8)
 Call ID: 5937d16b-edbb-4f30-a2bb-1c2bd792a1f8
  Args:
    type: :Man
    source: Heinrich
  AssignClass (5566b539-ea95-45b2-aaf6-f970b3e0a8f1)
 Call ID: 5566b539-ea95-45b2-aaf6-f970b3e0a8f1
  Args:
    type: :Man
    source: Otto
  AssignClass (803b0303-c0b9-4831-94fc-03ce55975fa9)
 Call ID: 803b0303-c0b9-4831-94fc-03ce55975fa9
  Args:
    source: Elisabeth
    type: :Woman
  AddTriple (54dd9716-3f97-4d68-9767-80369ba1be26)
 Call ID: 54dd9716-3f97-4d68-9767-80369ba1be26
  Args:
    relation: :isSiblingOf
    target: Heinrich
    source: Moritz
  AddTriple (e6b473ae-5dae-4128-b46f-5a77a85eb962)
 Call ID: e6b473ae-5dae-4128-b46f-5a77a85eb962
  Args:
    target: Otto
    source: Moritz
    relation: :isSiblingOf
  AddTriple (8c1c1cbb-168b-4653-8a95-e3c6fa22db05)
 Call ID: 8c1c1cbb-168b-4653-8a95-e3c6fa22db05
  Args:
    target: Elisabeth
    source: Moritz
    relation: :isSiblingOf
  AssignClass (e20affd3-070f-4d18-b61c-169c7ec87e7d)
 Call ID: e20affd3-070f-4d18-b61c-169c7ec87e7d
  Args:
    type: :Man
    source: Louis
  AssignClass (491ba34a-024d-4efc-adce-54f14cb1791a)
 Call ID: 491ba34a-024d-4efc-adce-54f14cb1791a
  Args:
    source: Margaret_Campbell_Geddes
    type: :Woman
  AddTriple (230be48e-26e5-408b-aed3-3528c93fe5c0)
 Call ID: 230be48e-26e5-408b-aed3-3528c93fe5c0
  Args:
    target: Moritz
    source: Louis
    relation: :isUncleOf
  AddTriple (afd6afa3-d52c-4876-ab0b-43dbf2d50a5d)
 Call ID: afd6afa3-d52c-4876-ab0b-43dbf2d50a5d
  Args:
    source: Margaret_Campbell_Geddes
    target: Moritz
    relation: :isAuntOf
  AddLiteral (f477c3e4-63a0-4984-a0be-850e76af9f5d)
 Call ID: f477c3e4-63a0-4984-a0be-850e76af9f5d
  Args:
    source: Louis
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1968
  AddLiteral (0bb35331-02f2-4e52-8027-7b4ccc2576ae)
 Call ID: 0bb35331-02f2-4e52-8027-7b4ccc2576ae
  Args:
    literal_value: 1980
    source: Philip
    literal_type: xsd:integer
    relation: :hasDeathYear
  AssignClass (b4d58b11-97cd-4e2d-be90-806661c45b20)
 Call ID: b4d58b11-97cd-4e2d-be90-806661c45b20
  Args:
    source: Tatiana_of_Sayn-Wittgenstein-Berleburg
    type: :Woman
  AddTriple (96da050c-25c0-475f-832f-20135f0e77a2)
 Call ID: 96da050c-25c0-475f-832f-20135f0e77a2
  Args:
    target: Tatiana_of_Sayn-Wittgenstein-Berleburg
    source: Moritz
    relation: :hasRelation
  AssignClass (294aeb76-88ba-4f20-b24e-d1520b2df020)
 Call ID: 294aeb76-88ba-4f20-b24e-d1520b2df020
  Args:
    source: Gustav_Albrecht
    type: :Man
  AddTriple (2c52ae1c-6eb1-4a00-8c4c-fdc37702d39f)
 Call ID: 2c52ae1c-6eb1-4a00-8c4c-fdc37702d39f
  Args:
    target: Gustav_Albrecht
    source: Tatiana_of_Sayn-Wittgenstein-Berleburg
    relation: :hasFather
  Finish (2f55b221-0ea9-4c4b-adab-c91131b2c6d6)
 Call ID: 2f55b221-0ea9-4c4b-adab-c91131b2c6d6
  Args: