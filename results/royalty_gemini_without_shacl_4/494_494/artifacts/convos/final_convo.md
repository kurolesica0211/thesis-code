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
Bernhard Prinz und Markgraf von Baden (born 27 May 1970), styled Margrave of Baden and Duke of Zähringen, is the head of the House of Baden since 29 December 2022 following the death of his father, Maximilian.
Early life and family

Bernhard was born at Schloss Salem in Salem, Baden-Württemberg, on 27 May 1970.
He is the eldest son of Maximilian, Margrave of Baden, and Archduchess Valerie of Austria (born 1941) and was styled as the heir of his father, Hereditary Prince of Baden.
His paternal grandparents were Berthold, Margrave of Baden, and Princess Theodora of Greece and Denmark, who was a sister of Prince Philip, Duke of Edinburgh.
His maternal grandparents were Archduke Hubert Salvator of Austria and Princess Rosemary of Salm-Salm.
Prince Bernhard manages the family estates, including Staufenberg Castle, and the margravial wineries dedicated to preserving the grape variety Müller-Thurgau.
Bernhard has close relations with the British royal family, and his granduncle, Prince Philip, Duke of Edinburgh, often came to Germany to shoot with the Baden family.
On 17 April 2021, Bernhard was one of only thirty mourners at Prince Philip's ceremonial funeral at St George's Chapel, Windsor Castle.
Bernhard, along with his cousins Philipp, Prince of Hohenlohe-Langenburg, and Donatus, Landgrave of Hesse, was chosen to represent the families of the Duke's late sisters who had been prevented from attending his wedding in 1947.
Bernhard and his wife and siblings later attended a service of thanksgiving for Prince Philip's life at Westminster Abbey on 29 March 2022.
On 30 March 2023, he and his wife attended a state banquet given by Frank-Walter Steinmeier, President of Germany, at Bellevue Palace during King Charles III and Queen Camilla's state visit to Germany.
On 29 December 2022, his father, Maximilian, died and Bernhard became head of the former grand ducal house of Baden.
Though royal and noble titles were abolished in Germany in 1919 when the Weimar Republic was proclaimed, he is sometimes styled and titled His Royal Highness The Margrave of Baden, Duke of Zähringen, by courtesy.
Prior to this, he was styled and titled His Grand Ducal Highness Hereditary Prince of Baden.
On 24 April 2025 the Margrave attended the funeral of Andreas, Prince of Saxe-Coburg and Gotha as the representative of Charles III.
Marriage and children

Bernhard married Stephanie Anne Kaul (born 27 June 1966), daughter of Christian Kaul and Hannelore Scheel, in a civil ceremony on 22 June 2001 and a religious ceremony the following day at Schloss Salem.



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
  AssignClass (5dfc2258-6539-44f7-81c5-6219a6932a82)
 Call ID: 5dfc2258-6539-44f7-81c5-6219a6932a82
  Args:
    source: Bernhard_Prinz_von_Baden
    type: :Man
  AssignClass (64788039-968b-4a4c-9e7a-a77c23d75183)
 Call ID: 64788039-968b-4a4c-9e7a-a77c23d75183
  Args:
    source: Bernhard_Prinz_von_Baden
    type: :Person
  AddLiteral (58166018-c2ea-435a-a044-3d68fe96428d)
 Call ID: 58166018-c2ea-435a-a044-3d68fe96428d
  Args:
    literal_value: 1970
    literal_type: xsd:positiveInteger
    source: Bernhard_Prinz_von_Baden
    relation: :hasBirthYear
  AssignClass (a53cd2bf-476c-4883-9587-5049c675319f)
 Call ID: a53cd2bf-476c-4883-9587-5049c675319f
  Args:
    source: Maximilian_Margrave_of_Baden
    type: :Man
  AssignClass (4f3f4489-c0ed-4fdd-bb8e-b210a2f14966)
 Call ID: 4f3f4489-c0ed-4fdd-bb8e-b210a2f14966
  Args:
    type: :Person
    source: Maximilian_Margrave_of_Baden
  AssignClass (4fc1e4d4-f564-495c-a73b-15d6be5c1c31)
 Call ID: 4fc1e4d4-f564-495c-a73b-15d6be5c1c31
  Args:
    source: Maximilian_Margrave_of_Baden
    type: :Ancestor
  AddLiteral (1dee086b-aa79-449f-bf20-5a2ca2986f1b)
 Call ID: 1dee086b-aa79-449f-bf20-5a2ca2986f1b
  Args:
    literal_value: 2022
    relation: :hasDeathYear
    source: Maximilian_Margrave_of_Baden
    literal_type: xsd:positiveInteger
  AddTriple (e1d21937-309b-41b9-a86d-f070b7cc7953)
 Call ID: e1d21937-309b-41b9-a86d-f070b7cc7953
  Args:
    target: Maximilian_Margrave_of_Baden
    source: Bernhard_Prinz_von_Baden
    relation: :hasFather
  AssignClass (e6990279-8b23-40be-8884-f90abbe49a07)
 Call ID: e6990279-8b23-40be-8884-f90abbe49a07
  Args:
    type: :Woman
    source: Valerie_of_Austria
  AssignClass (bb8d91a1-78a5-4487-910f-cd871d810262)
 Call ID: bb8d91a1-78a5-4487-910f-cd871d810262
  Args:
    type: :Person
    source: Valerie_of_Austria
  AssignClass (5de8e65a-e9a9-41b9-bb1f-883b1beb14af)
 Call ID: 5de8e65a-e9a9-41b9-bb1f-883b1beb14af
  Args:
    type: :Ancestor
    source: Valerie_of_Austria
  AddLiteral (93ce6367-b6e1-4dce-805d-410be5974b47)
 Call ID: 93ce6367-b6e1-4dce-805d-410be5974b47
  Args:
    literal_value: 1941
    literal_type: xsd:positiveInteger
    relation: :hasBirthYear
    source: Valerie_of_Austria
  AddTriple (f70ca505-dfaf-448d-b186-831d0ef71aab)
 Call ID: f70ca505-dfaf-448d-b186-831d0ef71aab
  Args:
    relation: :hasMother
    source: Bernhard_Prinz_von_Baden
    target: Valerie_of_Austria
  AssignClass (db663245-ecd0-41a1-b2f4-aed763eac58f)
 Call ID: db663245-ecd0-41a1-b2f4-aed763eac58f
  Args:
    type: :Man
    source: Berthold_Margrave_of_Baden
  AssignClass (1bbf5b10-e08f-44c0-bf34-5b3ef1deadc5)
 Call ID: 1bbf5b10-e08f-44c0-bf34-5b3ef1deadc5
  Args:
    source: Berthold_Margrave_of_Baden
    type: :Ancestor
  AddTriple (c7eefd8c-26bf-404c-bb1b-f2a0bbb687e4)
 Call ID: c7eefd8c-26bf-404c-bb1b-f2a0bbb687e4
  Args:
    source: Maximilian_Margrave_of_Baden
    relation: :hasFather
    target: Berthold_Margrave_of_Baden
  AssignClass (4aa26f26-e92c-408f-bc35-8ebb68616d37)
 Call ID: 4aa26f26-e92c-408f-bc35-8ebb68616d37
  Args:
    type: :Woman
    source: Theodora_of_Greece_and_Denmark
  AssignClass (cbefde2f-3d6f-46f5-9a27-8d03ccfd5db7)
 Call ID: cbefde2f-3d6f-46f5-9a27-8d03ccfd5db7
  Args:
    type: :Ancestor
    source: Theodora_of_Greece_and_Denmark
  AddTriple (456fb46d-92ec-4961-85cb-8a0a1578e622)
 Call ID: 456fb46d-92ec-4961-85cb-8a0a1578e622
  Args:
    source: Maximilian_Margrave_of_Baden
    relation: :hasMother
    target: Theodora_of_Greece_and_Denmark
  AssignClass (9ef05ce5-3511-4280-ae5d-934b8642c279)
 Call ID: 9ef05ce5-3511-4280-ae5d-934b8642c279
  Args:
    source: Hubert_Salvator_of_Austria
    type: :Man
  AssignClass (2282f7e7-5876-4946-85fd-9763df01a4b5)
 Call ID: 2282f7e7-5876-4946-85fd-9763df01a4b5
  Args:
    source: Hubert_Salvator_of_Austria
    type: :Ancestor
  AddTriple (ae5c2694-ee66-4f61-8736-50a85856c43e)
 Call ID: ae5c2694-ee66-4f61-8736-50a85856c43e
  Args:
    source: Valerie_of_Austria
    relation: :hasFather
    target: Hubert_Salvator_of_Austria
  AssignClass (621f6052-a03f-4970-b3a5-fba75260d253)
 Call ID: 621f6052-a03f-4970-b3a5-fba75260d253
  Args:
    source: Rosemary_of_Salm-Salm
    type: :Woman
  AssignClass (6783968f-ff12-4130-870d-63aa15f58475)
 Call ID: 6783968f-ff12-4130-870d-63aa15f58475
  Args:
    source: Rosemary_of_Salm-Salm
    type: :Ancestor
  AddTriple (9bfe43d0-7d86-4a0b-839f-8f396def9b7e)
 Call ID: 9bfe43d0-7d86-4a0b-839f-8f396def9b7e
  Args:
    target: Rosemary_of_Salm-Salm
    source: Valerie_of_Austria
    relation: :hasMother
  AssignClass (b9bdab9c-fcc3-4567-adb9-1efef0a12930)
 Call ID: b9bdab9c-fcc3-4567-adb9-1efef0a12930
  Args:
    type: :Woman
    source: Stephanie_Anne_Kaul
  AssignClass (6eab3d7a-7afd-4fe2-9342-5a4edfd091ae)
 Call ID: 6eab3d7a-7afd-4fe2-9342-5a4edfd091ae
  Args:
    type: :Person
    source: Stephanie_Anne_Kaul
  AddLiteral (0e3dfb93-9903-4f9f-b313-46467ec0181f)
 Call ID: 0e3dfb93-9903-4f9f-b313-46467ec0181f
  Args:
    literal_type: xsd:positiveInteger
    source: Stephanie_Anne_Kaul
    relation: :hasBirthYear
    literal_value: 1966
  AddTriple (caf94154-3dbc-4e53-ad01-9781ea37b7d9)
 Call ID: caf94154-3dbc-4e53-ad01-9781ea37b7d9
  Args:
    source: Bernhard_Prinz_von_Baden
    relation: :hasRelation
    target: Stephanie_Anne_Kaul
  AddLiteral (6679d291-7c6e-4a38-acb3-5222d9d33490)
 Call ID: 6679d291-7c6e-4a38-acb3-5222d9d33490
  Args:
    literal_type: xsd:positiveInteger
    source: Bernhard_Prinz_von_Baden
    relation: :hasMarriageYear
    literal_value: 2001
  AssignClass (66083a1f-a375-44ec-81a1-9e0d8dbac87b)
 Call ID: 66083a1f-a375-44ec-81a1-9e0d8dbac87b
  Args:
    type: :Man
    source: Christian_Kaul
  AssignClass (69daab20-9c35-4f3b-9bc1-c8b5a33b879c)
 Call ID: 69daab20-9c35-4f3b-9bc1-c8b5a33b879c
  Args:
    type: :Ancestor
    source: Christian_Kaul
  AddTriple (2550708c-47de-4822-affc-37db8cf3c16f)
 Call ID: 2550708c-47de-4822-affc-37db8cf3c16f
  Args:
    target: Christian_Kaul
    relation: :hasFather
    source: Stephanie_Anne_Kaul
  AssignClass (a316e8e0-fde6-4021-898c-665ee7e377d6)
 Call ID: a316e8e0-fde6-4021-898c-665ee7e377d6
  Args:
    type: :Woman
    source: Hannelore_Scheel
  AssignClass (8777d711-e288-4c4a-8d16-124d19ee3e26)
 Call ID: 8777d711-e288-4c4a-8d16-124d19ee3e26
  Args:
    source: Hannelore_Scheel
    type: :Ancestor
  AddTriple (c4807408-8c37-4fd0-a8ba-75d3f54c8f45)
 Call ID: c4807408-8c37-4fd0-a8ba-75d3f54c8f45
  Args:
    target: Hannelore_Scheel
    relation: :hasMother
    source: Stephanie_Anne_Kaul
  Finish (e0fbf918-a98a-46f7-934f-3d04f24978a1)
 Call ID: e0fbf918-a98a-46f7-934f-3d04f24978a1
  Args: