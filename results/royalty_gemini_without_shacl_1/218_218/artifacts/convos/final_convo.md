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
Prince Adam Karol Czartoryski (.mw-parser-output .IPA-label-small{font-size:85%}.mw-parser-output .references .IPA-label-small,.mw-parser-output .infobox .IPA-label-small,.mw-parser-output .navbox .IPA-label-small{font-size:100%}Polish: ; Spanish: Adán Carlos, IPA:  born 2 January 1940) is a Polish and Spanish aristocrat who is head of the Polish-Lithuanian House of Czartoryski.
In 2016, he sold the family art collection held in the Czartoryski Museum to the Polish state for approximately €100 million.
Origins

Adam Karol Czartoryski is the son of Prince Augustyn Józef Czartoryski (1907–1946) and his wife, Princess María de los Dolores of Bourbon-Two Sicilies.
He is the head of the Polish House of Czartoryski, descendants of Gediminas (died 1341), ruler of the Grand Duchy of Lithuania.
The Czartoryski rose to power under August Aleksander Czartoryski (1697–1782) of the Klewa line, who married Countess Zofia von Dönhoff, the only heir to the Sieniawski family.
The Czartoryski and the Potocki were the two most influential aristocratic families of the last decades of the Polish–Lithuanian Commonwealth (1569–1795).
The Gestapo arrested Prince Augustyn and Princess Dolores, who was pregnant with Prince Adam Karol.
Adam Karol Czartoryski was born on 2 January 1940 in Seville, Spain.
Adam Karol's brother Ludwik Piotr was born in 1945.
Prince Augustyn and Ludwik Piotr both died in 1946 and were buried in the crypt of the Silesian Church in Seville.
Adam Karol Czartoryski was educated in Spain and then in England.
Returning to his native Spain at the end of the sixties, Czartoryski continued his Karate training  under the guidance of Japanese Sensei Yasunari Ishimi.
Czartoryski was director of several international karate organizations.
In 1976 the Chinese government gave sports medals to Adam Czartoryski Bourbon and Fernando Compte, president of the Spanish Wrestling Association.
In 1982 Czartoryski was elected vice-president of the World Karate Federation and the European Karate Federation.
In 1974 Czartoryski became head trustee of the Polish Dzialynska Trust, set up by his family in Norwich, England in 1899 to support Polish students in the United Kingdom and in Poland.
In 1989, after the fall of the Polish People's Republic, Czartoryski was able to visit Poland for the first time.
That year the Polish government restored ownership of the family art collection and library to Czartoryski.
In 1992 Czartoryski represented Poland at  the opening of "Circa 1492:
In 1997 Czartoryski noticed the sale at Sotheby's of a painting by the Dutch artist Jan Mostaert named Portrait of a Lady, Presumably Anne of Bretagne, which he claimed to have come from his family's looted art collection.
Czartoryski's mother, Princess María de los Dolores, died in Madrid in 1996.
In December 2016 he sold the Czartoryski collection to the Polish state at an extremely low price in a transaction that drew some criticism and resulted in legal battles.
Czartoryski collection sale

The Czartoryski collection was started in 1796 by Adam Karol Czartoryski's ancestor, Princess Izabela Czartoryska, a liberal progressive who corresponded with Voltaire, Jean-Jacques Rousseau and Benjamin Franklin.
In 1798 Prince Adam Jerzy Czartoryski, Izabela's son, visited Italy where he bought Leonardo da Vinci's Lady with an Ermine and Raphael's Portrait of a young man.
When the Germans invaded Poland that year, Augustyn Józef Czartoryski had the most valuable items hidden beneath the baroque Sieniawski family castle, while others were stored in the cellar of the museum.
After the war the Polish representative at the Allies Commission for the Retrieval of Works of Art found many of the stolen paintings and claimed them for the Czartoryski Museum.
In London in the late 1960s Adam Karol Czartoryski met Professor Marek Rostworowski , who had been appointed in 1965 as director of the Czartoryski Collection in Poland.
That year the High Court restored the Czartoryski Museum and Library and their contents to Czartoryski, who set up the Princes Czartoryski Foundation to manage the collection.
The Princes Czartoryski Museum in Kraków was closed for extensive renovations in 2010, including adding a glass and steel roof to a courtyard that was not being used.
Czartoryski decided to entrust his collection to the Polish Nation, including the Lady With An Ermine, Landscape with the Good Samaritan and works by Pierre-Auguste Renoir.
By law, the Czartoryski Collection could anyway not leave the country without authorization by the government.
The management board of the Czartoryski Foundation complained that they had not been consulted over the sale, and resigned.
The endowment was challenged by Czartoryski's daughter, Tamara, and in 2018 resulted in a lawsuit between Adam Karol and his daughter.



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
  AssignClass (bce10725-b8f1-4e33-ac01-a06146ad4206)
 Call ID: bce10725-b8f1-4e33-ac01-a06146ad4206
  Args:
    source: :Adam_Karol_Czartoryski
    type: :Person
  AssignClass (a117aa24-6d22-4cce-87c7-a6626d3ad9b0)
 Call ID: a117aa24-6d22-4cce-87c7-a6626d3ad9b0
  Args:
    source: :Adam_Karol_Czartoryski
    type: :Man
  AddLiteral (7cf255d0-7db8-4931-961d-8106a3e428ac)
 Call ID: 7cf255d0-7db8-4931-961d-8106a3e428ac
  Args:
    literal_value: 1940
    literal_type: xsd:integer
    source: :Adam_Karol_Czartoryski
    relation: :hasBirthYear
  AssignClass (1b91b011-b8a8-423e-bac2-8d2eaf7c9dfe)
 Call ID: 1b91b011-b8a8-423e-bac2-8d2eaf7c9dfe
  Args:
    type: :Person
    source: :Augustyn_Józef_Czartoryski
  AssignClass (63531946-ce13-417a-b0d2-66da9ab317e0)
 Call ID: 63531946-ce13-417a-b0d2-66da9ab317e0
  Args:
    type: :Man
    source: :Augustyn_Józef_Czartoryski
  AddLiteral (d5530130-dacb-4559-bdf5-f6cfd99b4db9)
 Call ID: d5530130-dacb-4559-bdf5-f6cfd99b4db9
  Args:
    literal_type: xsd:integer
    literal_value: 1907
    source: :Augustyn_Józef_Czartoryski
    relation: :hasBirthYear
  AddLiteral (628bb564-d6a1-43a4-af96-5636caedcaed)
 Call ID: 628bb564-d6a1-43a4-af96-5636caedcaed
  Args:
    relation: :hasDeathYear
    source: :Augustyn_Józef_Czartoryski
    literal_type: xsd:integer
    literal_value: 1946
  AssignClass (55896293-7282-4597-bb16-27fae2c372b1)
 Call ID: 55896293-7282-4597-bb16-27fae2c372b1
  Args:
    source: :María_de_los_Dolores
    type: :Person
  AssignClass (06925d12-2e5a-4c0d-bb07-bb8a81085d99)
 Call ID: 06925d12-2e5a-4c0d-bb07-bb8a81085d99
  Args:
    type: :Woman
    source: :María_de_los_Dolores
  AddLiteral (929ae678-9f0e-48d1-a245-74acae5c1324)
 Call ID: 929ae678-9f0e-48d1-a245-74acae5c1324
  Args:
    literal_type: xsd:integer
    literal_value: 1996
    source: :María_de_los_Dolores
    relation: :hasDeathYear
  AddTriple (6888e79f-fad2-4c3e-aa3e-d5b6000080b1)
 Call ID: 6888e79f-fad2-4c3e-aa3e-d5b6000080b1
  Args:
    relation: :hasFather
    target: :Augustyn_Józef_Czartoryski
    source: :Adam_Karol_Czartoryski
  AddTriple (c0dbbda1-4c25-41d3-951f-0fbd47f75b46)
 Call ID: c0dbbda1-4c25-41d3-951f-0fbd47f75b46
  Args:
    source: :Adam_Karol_Czartoryski
    relation: :hasMother
    target: :María_de_los_Dolores
  AssignClass (c669c231-3470-477b-b5c9-97d68c885e62)
 Call ID: c669c231-3470-477b-b5c9-97d68c885e62
  Args:
    type: :Person
    source: :Ludwik_Piotr
  AssignClass (a66b2128-e89b-4936-b50b-96e55df6dcc1)
 Call ID: a66b2128-e89b-4936-b50b-96e55df6dcc1
  Args:
    source: :Ludwik_Piotr
    type: :Man
  AddLiteral (ba3012a3-00f1-494b-a364-82728f2c4857)
 Call ID: ba3012a3-00f1-494b-a364-82728f2c4857
  Args:
    source: :Ludwik_Piotr
    relation: :hasBirthYear
    literal_value: 1945
    literal_type: xsd:integer
  AddLiteral (fede799b-c2d9-47ac-9ac6-968547db7bc0)
 Call ID: fede799b-c2d9-47ac-9ac6-968547db7bc0
  Args:
    relation: :hasDeathYear
    source: :Ludwik_Piotr
    literal_type: xsd:integer
    literal_value: 1946
  AddTriple (ec82b8e9-7a2e-4f23-8015-0ccc7bfad6c2)
 Call ID: ec82b8e9-7a2e-4f23-8015-0ccc7bfad6c2
  Args:
    relation: :hasBrother
    target: :Ludwik_Piotr
    source: :Adam_Karol_Czartoryski
  AssignClass (b0c7e51a-d2b6-4f8f-b48f-5923b92de3a8)
 Call ID: b0c7e51a-d2b6-4f8f-b48f-5923b92de3a8
  Args:
    source: :Tamara_Czartoryska
    type: :Person
  AssignClass (673aa5a4-a312-4d95-a3e9-e849253993e6)
 Call ID: 673aa5a4-a312-4d95-a3e9-e849253993e6
  Args:
    source: :Tamara_Czartoryska
    type: :Woman
  AddTriple (de43f045-9e8d-421f-91d3-c595dd48ebf2)
 Call ID: de43f045-9e8d-421f-91d3-c595dd48ebf2
  Args:
    source: :Adam_Karol_Czartoryski
    target: :Tamara_Czartoryska
    relation: :hasDaughter
  AssignClass (e258bf65-cbc7-4fe6-bbca-fe62f9de1aaf)
 Call ID: e258bf65-cbc7-4fe6-bbca-fe62f9de1aaf
  Args:
    source: :Izabela_Czartoryska
    type: :Person
  AssignClass (db7a09be-edb1-482d-abd8-ecff0281e2fa)
 Call ID: db7a09be-edb1-482d-abd8-ecff0281e2fa
  Args:
    source: :Izabela_Czartoryska
    type: :Woman
  AssignClass (2a21b3c0-3f15-40fd-87a0-0b55ec1a5c01)
 Call ID: 2a21b3c0-3f15-40fd-87a0-0b55ec1a5c01
  Args:
    source: :Adam_Jerzy_Czartoryski
    type: :Person
  AssignClass (7cee4759-1204-4eff-b944-928ed21c4cd6)
 Call ID: 7cee4759-1204-4eff-b944-928ed21c4cd6
  Args:
    type: :Man
    source: :Adam_Jerzy_Czartoryski
  AddTriple (e81c1d42-dbde-4e8d-9fbc-487c8871dd1e)
 Call ID: e81c1d42-dbde-4e8d-9fbc-487c8871dd1e
  Args:
    source: :Izabela_Czartoryska
    target: :Adam_Jerzy_Czartoryski
    relation: :hasSon
  AddTriple (2fc90bc8-b467-481f-bcab-a0ab39668e4e)
 Call ID: 2fc90bc8-b467-481f-bcab-a0ab39668e4e
  Args:
    source: :Adam_Karol_Czartoryski
    target: :Izabela_Czartoryska
    relation: :hasAncestor
  Finish (f8b6210f-0ced-4da7-ac10-269c2578ceba)
 Call ID: f8b6210f-0ced-4da7-ac10-269c2578ceba
  Args: