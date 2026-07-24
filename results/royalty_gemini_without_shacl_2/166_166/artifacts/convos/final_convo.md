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
  AssignClass (e070e164-3dff-4d4d-8ad5-5caca0f12c2b)
 Call ID: e070e164-3dff-4d4d-8ad5-5caca0f12c2b
  Args:
    type: :Woman
    source: :Princess_Eugenie_of_Greece_and_Denmark
  AssignClass (6d52af14-fba0-4d2f-b5a4-ba88821832b0)
 Call ID: 6d52af14-fba0-4d2f-b5a4-ba88821832b0
  Args:
    type: :Person
    source: :Princess_Eugenie_of_Greece_and_Denmark
  AddLiteral (4f1544d7-c5f7-4e56-9e42-96dede715883)
 Call ID: 4f1544d7-c5f7-4e56-9e42-96dede715883
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1910
    source: :Princess_Eugenie_of_Greece_and_Denmark
  AddLiteral (80e8ee75-50a6-4bc6-b996-1c8596e22f27)
 Call ID: 80e8ee75-50a6-4bc6-b996-1c8596e22f27
  Args:
    literal_value: 1989
    relation: :hasDeathYear
    source: :Princess_Eugenie_of_Greece_and_Denmark
    literal_type: xsd:integer
  AssignClass (6e82722e-8e05-4a58-9671-948ff66c7604)
 Call ID: 6e82722e-8e05-4a58-9671-948ff66c7604
  Args:
    type: :Man
    source: :Prince_George_of_Greece_and_Denmark
  AssignClass (785854d2-937a-47bf-8e15-70e9a1929316)
 Call ID: 785854d2-937a-47bf-8e15-70e9a1929316
  Args:
    type: :Person
    source: :Prince_George_of_Greece_and_Denmark
  AssignClass (3fa55431-2249-4fbd-9747-2a06c3ace97f)
 Call ID: 3fa55431-2249-4fbd-9747-2a06c3ace97f
  Args:
    type: :Woman
    source: :Princess_Marie_Bonaparte
  AssignClass (2fa810b7-0594-45da-a855-dd73519703c5)
 Call ID: 2fa810b7-0594-45da-a855-dd73519703c5
  Args:
    type: :Person
    source: :Princess_Marie_Bonaparte
  AddTriple (57df2527-3fc9-45ae-a063-6ffb9bc8c24e)
 Call ID: 57df2527-3fc9-45ae-a063-6ffb9bc8c24e
  Args:
    target: :Prince_George_of_Greece_and_Denmark
    source: :Princess_Eugenie_of_Greece_and_Denmark
    relation: :hasFather
  AddTriple (5555ea84-38a8-40c2-82e7-776262def0fd)
 Call ID: 5555ea84-38a8-40c2-82e7-776262def0fd
  Args:
    target: :Princess_Marie_Bonaparte
    source: :Princess_Eugenie_of_Greece_and_Denmark
    relation: :hasMother
  AssignClass (27df7796-d2d6-437e-8c9b-28f93280702e)
 Call ID: 27df7796-d2d6-437e-8c9b-28f93280702e
  Args:
    type: :Woman
    source: :Marie-Felix_Blanc
  AssignClass (06eb9d72-8f38-4125-85c4-64d832ec062a)
 Call ID: 06eb9d72-8f38-4125-85c4-64d832ec062a
  Args:
    type: :Person
    source: :Marie-Felix_Blanc
  AssignClass (d1016639-9bab-411e-8f49-1e1f08e01848)
 Call ID: d1016639-9bab-411e-8f49-1e1f08e01848
  Args:
    type: :Man
    source: :Prince_Roland_Bonaparte
  AssignClass (8432d090-de58-4540-bb32-581813fb5de6)
 Call ID: 8432d090-de58-4540-bb32-581813fb5de6
  Args:
    type: :Person
    source: :Prince_Roland_Bonaparte
  AddTriple (c6cf02bd-edbb-4605-b53c-a0473032dec6)
 Call ID: c6cf02bd-edbb-4605-b53c-a0473032dec6
  Args:
    source: :Princess_Marie_Bonaparte
    relation: :hasMother
    target: :Marie-Felix_Blanc
  AddTriple (b4993498-c730-4d9b-9eb2-59ee3207e96c)
 Call ID: b4993498-c730-4d9b-9eb2-59ee3207e96c
  Args:
    target: :Prince_Roland_Bonaparte
    relation: :hasFather
    source: :Princess_Marie_Bonaparte
  AssignClass (e1755470-de92-461b-b400-14c1f8962eda)
 Call ID: e1755470-de92-461b-b400-14c1f8962eda
  Args:
    type: :Man
    source: :George_I_of_Greece
  AssignClass (905a2903-0d2a-4ad7-8ad4-8e69491a88be)
 Call ID: 905a2903-0d2a-4ad7-8ad4-8e69491a88be
  Args:
    type: :Person
    source: :George_I_of_Greece
  AssignClass (da43f59d-f908-42f2-ba0e-82dfa8620dcc)
 Call ID: da43f59d-f908-42f2-ba0e-82dfa8620dcc
  Args:
    type: :Woman
    source: :Olga_Constantinovna_of_Russia
  AssignClass (f22269f3-252b-47d4-8103-433766302d74)
 Call ID: f22269f3-252b-47d4-8103-433766302d74
  Args:
    type: :Person
    source: :Olga_Constantinovna_of_Russia
  AddTriple (2bb4efb6-7618-45e1-aa0b-c34ed0e5c2a8)
 Call ID: 2bb4efb6-7618-45e1-aa0b-c34ed0e5c2a8
  Args:
    source: :Prince_George_of_Greece_and_Denmark
    relation: :hasFather
    target: :George_I_of_Greece
  AddTriple (fde9f4c0-eab6-48fe-962d-62c055072f8a)
 Call ID: fde9f4c0-eab6-48fe-962d-62c055072f8a
  Args:
    target: :Olga_Constantinovna_of_Russia
    source: :Prince_George_of_Greece_and_Denmark
    relation: :hasMother
  AssignClass (4bc4c76c-3249-4d63-88b4-4bac9b652a87)
 Call ID: 4bc4c76c-3249-4d63-88b4-4bac9b652a87
  Args:
    type: :Man
    source: :Prince_Peter_of_Greece_and_Denmark
  AssignClass (61761740-664b-4c85-8c09-d3a452639996)
 Call ID: 61761740-664b-4c85-8c09-d3a452639996
  Args:
    type: :Person
    source: :Prince_Peter_of_Greece_and_Denmark
  AddTriple (88e4d0fb-57a0-4702-8aaf-391639c5c9c4)
 Call ID: 88e4d0fb-57a0-4702-8aaf-391639c5c9c4
  Args:
    source: :Princess_Eugenie_of_Greece_and_Denmark
    relation: :hasBrother
    target: :Prince_Peter_of_Greece_and_Denmark
  AssignClass (882705e8-95e9-46b2-a65b-049b0e4cdd5b)
 Call ID: 882705e8-95e9-46b2-a65b-049b0e4cdd5b
  Args:
    type: :Man
    source: :Prince_Dominik_Rainer_Radziwill
  AssignClass (5dc7c8f5-6ace-4843-af42-7e4796722f3a)
 Call ID: 5dc7c8f5-6ace-4843-af42-7e4796722f3a
  Args:
    type: :Person
    source: :Prince_Dominik_Rainer_Radziwill
  AddLiteral (1d2fd00d-701b-4d03-82c3-91d9e6f5d30d)
 Call ID: 1d2fd00d-701b-4d03-82c3-91d9e6f5d30d
  Args:
    literal_value: 1938
    relation: :hasMarriageYear
    source: :Princess_Eugenie_of_Greece_and_Denmark
    literal_type: xsd:integer
  AssignClass (ed6e19e6-6e58-4991-b221-46e6d6bebc75)
 Call ID: ed6e19e6-6e58-4991-b221-46e6d6bebc75
  Args:
    type: :Man
    source: :Prince_Hieronim_Radziwill
  AssignClass (d8b4a435-7b71-4936-8617-958df1f96079)
 Call ID: d8b4a435-7b71-4936-8617-958df1f96079
  Args:
    type: :Person
    source: :Prince_Hieronim_Radziwill
  AssignClass (395d1ff0-736f-4616-97cc-f8f2445bacb1)
 Call ID: 395d1ff0-736f-4616-97cc-f8f2445bacb1
  Args:
    type: :Woman
    source: :Archduchess_Renata_of_Austria
  AssignClass (49d6b9c6-6084-48b6-87f5-fb2e3c588c20)
 Call ID: 49d6b9c6-6084-48b6-87f5-fb2e3c588c20
  Args:
    type: :Person
    source: :Archduchess_Renata_of_Austria
  AddTriple (d42ea70d-067d-4161-9f40-e7e1ebdb158a)
 Call ID: d42ea70d-067d-4161-9f40-e7e1ebdb158a
  Args:
    source: :Prince_Dominik_Rainer_Radziwill
    relation: :hasFather
    target: :Prince_Hieronim_Radziwill
  AddTriple (7ba2aaa8-320c-4a31-b201-3010af00f8da)
 Call ID: 7ba2aaa8-320c-4a31-b201-3010af00f8da
  Args:
    target: :Archduchess_Renata_of_Austria
    source: :Prince_Dominik_Rainer_Radziwill
    relation: :hasMother
  AssignClass (392ecb13-af69-466c-a672-72a0fe02bcc6)
 Call ID: 392ecb13-af69-466c-a672-72a0fe02bcc6
  Args:
    type: :Man
    source: :Prince_Raymundo_della_Torre_e_Tasso
  AssignClass (d12cf11c-20a2-41cf-87a4-5a18f9fc342b)
 Call ID: d12cf11c-20a2-41cf-87a4-5a18f9fc342b
  Args:
    type: :Person
    source: :Prince_Raymundo_della_Torre_e_Tasso
  AddLiteral (4c8955ed-99bc-41bd-99bd-e827e80009a0)
 Call ID: 4c8955ed-99bc-41bd-99bd-e827e80009a0
  Args:
    literal_value: 1949
    relation: :hasMarriageYear
    source: :Princess_Eugenie_of_Greece_and_Denmark
    literal_type: xsd:integer
  Finish (24c59bc1-1389-4606-82a3-60a296500286)
 Call ID: 24c59bc1-1389-4606-82a3-60a296500286
  Args: