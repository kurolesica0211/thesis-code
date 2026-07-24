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
Archduchess Helena of Austria (full German name: Helena Marie Alice Christine Josefa Anna Margareta Madeleine Walburga Blandina Cäcilie Philomena Carmela Ignatia Rita de Cascia, Erzherzogin von Österreich, Prinzessin von Toskana; 30 October 1903 – 8 September 1924) was a member of the Tuscan branch of the House of Habsburg-Lorraine and an Archduchess of Austria and Princess of Bohemia, Hungary, and Tuscany by birth.
Through her marriage to Philipp Albrecht, Hereditary Duke of Württemberg, Helena became a member of the House of Württemberg and Hereditary Duchess consort of Württemberg.
Early life

Helena was born in Linz, Austria-Hungary, the second-eldest child and eldest daughter of Archduke Peter Ferdinand, Prince of Tuscany and his wife Princess Maria Cristina of Bourbon-Two Sicilies.
Helena was raised with her three siblings in Salzburg and Vienna until the end of World War I in 1918 when her family was exiled and moved to Lucerne, Switzerland.
Marriage and issue

Helena married Philipp Albrecht, Hereditary Duke of Württemberg, eldest child and son of Albrecht, Duke of Württemberg and his wife, Archduchess Margarete Sophie of Austria, on 24 October 1923 in Altshausen.
Helena and Philipp Albrecht had one daughter:


Death

Helena died just a week after giving birth to her daughter Maria Christina, aged only 20.
Her husband later married her sister Archduchess Rosa of Austria, Princess of Tuscany in 1928.



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
  AssignClass (38bff337-c2ea-433d-b6a0-6be22e58fff7)
 Call ID: 38bff337-c2ea-433d-b6a0-6be22e58fff7
  Args:
    type: :Woman
    source: Helena_of_Austria
  AssignClass (6ce9c6a8-29da-479f-92c3-fcca2f8a8e8f)
 Call ID: 6ce9c6a8-29da-479f-92c3-fcca2f8a8e8f
  Args:
    source: Helena_of_Austria
    type: :Person
  AddLiteral (de80db30-e704-4bfe-889b-5e2439e50b0f)
 Call ID: de80db30-e704-4bfe-889b-5e2439e50b0f
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1903
    source: Helena_of_Austria
  AddLiteral (74d47aba-c30d-431d-8217-18db53fdbbf0)
 Call ID: 74d47aba-c30d-431d-8217-18db53fdbbf0
  Args:
    source: Helena_of_Austria
    relation: :hasDeathYear
    literal_value: 1924
    literal_type: xsd:integer
  AssignClass (09f18730-0ae1-4873-9ee9-bbc41bba35e5)
 Call ID: 09f18730-0ae1-4873-9ee9-bbc41bba35e5
  Args:
    type: :Man
    source: Peter_Ferdinand
  AssignClass (6ba0e512-9a16-4ddd-a18d-3dcbb517f844)
 Call ID: 6ba0e512-9a16-4ddd-a18d-3dcbb517f844
  Args:
    source: Peter_Ferdinand
    type: :Person
  AssignClass (1c5fb59b-f23f-43c5-8444-4cd3115776a5)
 Call ID: 1c5fb59b-f23f-43c5-8444-4cd3115776a5
  Args:
    type: :Woman
    source: Maria_Cristina_of_Bourbon_Two_Sicilies
  AssignClass (8328292a-e229-4448-b37f-cafed90645e1)
 Call ID: 8328292a-e229-4448-b37f-cafed90645e1
  Args:
    type: :Person
    source: Maria_Cristina_of_Bourbon_Two_Sicilies
  AddTriple (1391d742-a5f9-41a4-8507-0da2089ddbd6)
 Call ID: 1391d742-a5f9-41a4-8507-0da2089ddbd6
  Args:
    relation: :hasFather
    source: Helena_of_Austria
    target: Peter_Ferdinand
  AddTriple (4151c754-1bcf-4300-a8bf-0f5b48b7cecb)
 Call ID: 4151c754-1bcf-4300-a8bf-0f5b48b7cecb
  Args:
    source: Helena_of_Austria
    relation: :hasMother
    target: Maria_Cristina_of_Bourbon_Two_Sicilies
  AssignClass (8e618bb8-f269-45a4-98ad-d8cb07951805)
 Call ID: 8e618bb8-f269-45a4-98ad-d8cb07951805
  Args:
    type: :Man
    source: Philipp_Albrecht
  AssignClass (66a85a89-e158-4a49-87d6-ddff04442873)
 Call ID: 66a85a89-e158-4a49-87d6-ddff04442873
  Args:
    type: :Person
    source: Philipp_Albrecht
  AddLiteral (a61b2a70-1422-47b4-83dd-2980e5fcc3a4)
 Call ID: a61b2a70-1422-47b4-83dd-2980e5fcc3a4
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 1923
    source: Helena_of_Austria
  AddTriple (16bf8d10-a08e-4485-abe8-b398b9544700)
 Call ID: 16bf8d10-a08e-4485-abe8-b398b9544700
  Args:
    target: Philipp_Albrecht
    source: Helena_of_Austria
    relation: :hasRelation
  AssignClass (790accc7-12e3-45b8-9683-1eb87e80eb5e)
 Call ID: 790accc7-12e3-45b8-9683-1eb87e80eb5e
  Args:
    type: :Man
    source: Albrecht_of_Wurttemberg
  AssignClass (86b46e1b-937f-45b1-9971-9f6130c8f05b)
 Call ID: 86b46e1b-937f-45b1-9971-9f6130c8f05b
  Args:
    type: :Person
    source: Albrecht_of_Wurttemberg
  AssignClass (eef46cbb-e7ee-4a54-8912-4f159dd6c2d4)
 Call ID: eef46cbb-e7ee-4a54-8912-4f159dd6c2d4
  Args:
    type: :Woman
    source: Margarete_Sophie_of_Austria
  AssignClass (bf0c5860-9b5f-4ce6-87b5-75c09b43bfac)
 Call ID: bf0c5860-9b5f-4ce6-87b5-75c09b43bfac
  Args:
    source: Margarete_Sophie_of_Austria
    type: :Person
  AddTriple (4c9a09c8-202b-40db-9758-63d3949337f8)
 Call ID: 4c9a09c8-202b-40db-9758-63d3949337f8
  Args:
    target: Albrecht_of_Wurttemberg
    source: Philipp_Albrecht
    relation: :hasFather
  AddTriple (4f080762-9421-4567-9348-50c9d73ceb1e)
 Call ID: 4f080762-9421-4567-9348-50c9d73ceb1e
  Args:
    relation: :hasMother
    source: Philipp_Albrecht
    target: Margarete_Sophie_of_Austria
  AssignClass (a1f7abcb-7ab4-4dc0-9bbd-77172272220a)
 Call ID: a1f7abcb-7ab4-4dc0-9bbd-77172272220a
  Args:
    source: Maria_Christina_daughter_of_Helena
    type: :Woman
  AssignClass (a38463eb-b661-4dd5-aeb0-baac9d6460b3)
 Call ID: a38463eb-b661-4dd5-aeb0-baac9d6460b3
  Args:
    type: :Person
    source: Maria_Christina_daughter_of_Helena
  AddTriple (878fddef-fb0f-44bb-8c02-93f87761798f)
 Call ID: 878fddef-fb0f-44bb-8c02-93f87761798f
  Args:
    target: Helena_of_Austria
    relation: :hasMother
    source: Maria_Christina_daughter_of_Helena
  AddTriple (418a6327-124f-4a78-9c04-abeb6d4c3ea2)
 Call ID: 418a6327-124f-4a78-9c04-abeb6d4c3ea2
  Args:
    target: Philipp_Albrecht
    source: Maria_Christina_daughter_of_Helena
    relation: :hasFather
  AssignClass (c186f75a-f7c4-4858-8a8e-c735af59b9d8)
 Call ID: c186f75a-f7c4-4858-8a8e-c735af59b9d8
  Args:
    source: Rosa_of_Austria
    type: :Woman
  AssignClass (c786a99a-8b40-46e0-bce9-d852307c0c5c)
 Call ID: c786a99a-8b40-46e0-bce9-d852307c0c5c
  Args:
    type: :Person
    source: Rosa_of_Austria
  AddTriple (c1e636f8-6d56-43b2-81f5-84a358e6c078)
 Call ID: c1e636f8-6d56-43b2-81f5-84a358e6c078
  Args:
    relation: :isSisterOf
    source: Rosa_of_Austria
    target: Helena_of_Austria
  AddLiteral (1e47ec75-5810-4cda-a56f-8a95c5b68861)
 Call ID: 1e47ec75-5810-4cda-a56f-8a95c5b68861
  Args:
    relation: :hasMarriageYear
    literal_value: 1928
    literal_type: xsd:integer
    source: Philipp_Albrecht
  AddTriple (12221072-77e7-49dc-adc1-fc0a41faeb96)
 Call ID: 12221072-77e7-49dc-adc1-fc0a41faeb96
  Args:
    relation: :hasRelation
    source: Philipp_Albrecht
    target: Rosa_of_Austria
  Finish (27e8995c-9581-40fe-8cb5-48a5e58ec875)
 Call ID: 27e8995c-9581-40fe-8cb5-48a5e58ec875
  Args: