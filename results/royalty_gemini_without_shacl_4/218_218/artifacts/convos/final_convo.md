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
  AssignClass (157b0949-d9ee-4574-be42-7ddc0647cc4f)
 Call ID: 157b0949-d9ee-4574-be42-7ddc0647cc4f
  Args:
    type: :Man
    source: Adam_Karol_Czartoryski
  AssignClass (0d73b024-464a-4e51-a1c1-ef96228542af)
 Call ID: 0d73b024-464a-4e51-a1c1-ef96228542af
  Args:
    source: Adam_Karol_Czartoryski
    type: :Person
  AddLiteral (561eafa1-d947-420b-b804-904bcd623a54)
 Call ID: 561eafa1-d947-420b-b804-904bcd623a54
  Args:
    literal_type: xsd:positiveInteger
    source: Adam_Karol_Czartoryski
    literal_value: 1940
    relation: :hasBirthYear
  AssignClass (06b3e74b-bb35-4990-9f0a-cd03937dfc3a)
 Call ID: 06b3e74b-bb35-4990-9f0a-cd03937dfc3a
  Args:
    type: :Man
    source: Augustyn_Józef_Czartoryski
  AssignClass (a5616372-264d-4d49-a61f-01edad824710)
 Call ID: a5616372-264d-4d49-a61f-01edad824710
  Args:
    source: Augustyn_Józef_Czartoryski
    type: :Person
  AssignClass (21bdfd8f-0c38-4b3a-bd84-6f75f597677b)
 Call ID: 21bdfd8f-0c38-4b3a-bd84-6f75f597677b
  Args:
    type: :Ancestor
    source: Augustyn_Józef_Czartoryski
  AddLiteral (1be066cc-7ee0-4a23-97d5-d3ef8dcfef2c)
 Call ID: 1be066cc-7ee0-4a23-97d5-d3ef8dcfef2c
  Args:
    source: Augustyn_Józef_Czartoryski
    literal_type: xsd:positiveInteger
    literal_value: 1907
    relation: :hasBirthYear
  AddLiteral (7919bcd0-f2e2-4d0a-98ed-a1a3bbf9f07d)
 Call ID: 7919bcd0-f2e2-4d0a-98ed-a1a3bbf9f07d
  Args:
    source: Augustyn_Józef_Czartoryski
    literal_type: xsd:positiveInteger
    relation: :hasDeathYear
    literal_value: 1946
  AssignClass (189016d8-09d4-44c4-93a9-022130b44de7)
 Call ID: 189016d8-09d4-44c4-93a9-022130b44de7
  Args:
    type: :Woman
    source: María_de_los_Dolores_of_Bourbon-Two_Sicilies
  AssignClass (023afd57-7a2f-4541-b880-6fffaa758974)
 Call ID: 023afd57-7a2f-4541-b880-6fffaa758974
  Args:
    type: :Person
    source: María_de_los_Dolores_of_Bourbon-Two_Sicilies
  AssignClass (3eca90dc-23ef-4faf-afdd-18d4641f4073)
 Call ID: 3eca90dc-23ef-4faf-afdd-18d4641f4073
  Args:
    type: :Ancestor
    source: María_de_los_Dolores_of_Bourbon-Two_Sicilies
  AddTriple (cea10bd3-f87e-4b5e-bbf4-fccf571a19b1)
 Call ID: cea10bd3-f87e-4b5e-bbf4-fccf571a19b1
  Args:
    target: Augustyn_Józef_Czartoryski
    relation: :hasFather
    source: Adam_Karol_Czartoryski
  AddTriple (9a976334-1409-4dea-8693-5e442c652db6)
 Call ID: 9a976334-1409-4dea-8693-5e442c652db6
  Args:
    relation: :hasMother
    target: María_de_los_Dolores_of_Bourbon-Two_Sicilies
    source: Adam_Karol_Czartoryski
  AssignClass (0513131d-8efa-4643-b194-5422c36e8063)
 Call ID: 0513131d-8efa-4643-b194-5422c36e8063
  Args:
    source: Ludwik_Piotr
    type: :Man
  AssignClass (c3d5a6c1-4ea3-42fc-ac39-fb11e4f5807f)
 Call ID: c3d5a6c1-4ea3-42fc-ac39-fb11e4f5807f
  Args:
    source: Ludwik_Piotr
    type: :Person
  AddTriple (ac03f19f-8200-4022-9b14-6fc47b48e73e)
 Call ID: ac03f19f-8200-4022-9b14-6fc47b48e73e
  Args:
    target: Adam_Karol_Czartoryski
    relation: :isBrotherOf
    source: Ludwik_Piotr
  AddLiteral (3a701eee-d74f-4627-966d-16f31d1ccd3a)
 Call ID: 3a701eee-d74f-4627-966d-16f31d1ccd3a
  Args:
    literal_value: 1946
    relation: :hasDeathYear
    literal_type: xsd:positiveInteger
    source: Ludwik_Piotr
  AssignClass (66a3eaaa-c682-4eeb-a4a4-9ee0c52ed49f)
 Call ID: 66a3eaaa-c682-4eeb-a4a4-9ee0c52ed49f
  Args:
    source: Tamara_Czartoryska
    type: :Woman
  AssignClass (c60676a8-35d7-406f-b2a1-bedc2d7feda4)
 Call ID: c60676a8-35d7-406f-b2a1-bedc2d7feda4
  Args:
    source: Tamara_Czartoryska
    type: :Person
  AddTriple (0c18cb7a-be5e-40f9-93b8-54e7facd6d74)
 Call ID: 0c18cb7a-be5e-40f9-93b8-54e7facd6d74
  Args:
    relation: :isDaughterOf
    target: Adam_Karol_Czartoryski
    source: Tamara_Czartoryska
  AssignClass (5d3341bb-2e1c-44d0-903e-09004a4c1538)
 Call ID: 5d3341bb-2e1c-44d0-903e-09004a4c1538
  Args:
    source: Izabela_Czartoryska
    type: :Woman
  AssignClass (4f8dcf36-2c3e-45f5-97b3-d283ad219e59)
 Call ID: 4f8dcf36-2c3e-45f5-97b3-d283ad219e59
  Args:
    type: :Person
    source: Izabela_Czartoryska
  AssignClass (cbaa2bdc-18a0-4a11-9125-e0cd359b0ec4)
 Call ID: cbaa2bdc-18a0-4a11-9125-e0cd359b0ec4
  Args:
    type: :Ancestor
    source: Izabela_Czartoryska
  AssignClass (aa170472-f284-4c31-8f53-f80eedd4c3c3)
 Call ID: aa170472-f284-4c31-8f53-f80eedd4c3c3
  Args:
    type: :Man
    source: Adam_Jerzy_Czartoryski
  AssignClass (1686600e-8cf0-477a-b20c-4e8b8984a12f)
 Call ID: 1686600e-8cf0-477a-b20c-4e8b8984a12f
  Args:
    source: Adam_Jerzy_Czartoryski
    type: :Person
  AssignClass (9077118c-b71e-43ef-a902-a71038d6d8e2)
 Call ID: 9077118c-b71e-43ef-a902-a71038d6d8e2
  Args:
    source: Adam_Jerzy_Czartoryski
    type: :Ancestor
  AddTriple (aac711dd-0e91-4c25-91a3-ab9e9571ae40)
 Call ID: aac711dd-0e91-4c25-91a3-ab9e9571ae40
  Args:
    relation: :isSonOf
    target: Izabela_Czartoryska
    source: Adam_Jerzy_Czartoryski
  AssignClass (b43c204e-6b92-4b2b-8650-f85d0bfd68df)
 Call ID: b43c204e-6b92-4b2b-8650-f85d0bfd68df
  Args:
    type: :Man
    source: August_Aleksander_Czartoryski
  AssignClass (d5d791fc-5419-43c4-b69c-22731afbd4a1)
 Call ID: d5d791fc-5419-43c4-b69c-22731afbd4a1
  Args:
    source: August_Aleksander_Czartoryski
    type: :Person
  AssignClass (61684a68-ad12-44ff-858d-28898a84bd62)
 Call ID: 61684a68-ad12-44ff-858d-28898a84bd62
  Args:
    source: August_Aleksander_Czartoryski
    type: :Ancestor
  AddLiteral (8b461289-4b30-4712-b264-19251fcb1547)
 Call ID: 8b461289-4b30-4712-b264-19251fcb1547
  Args:
    literal_value: 1697
    relation: :hasBirthYear
    literal_type: xsd:positiveInteger
    source: August_Aleksander_Czartoryski
  AddLiteral (694b5019-2f0d-42b3-91c7-e3643eb43dde)
 Call ID: 694b5019-2f0d-42b3-91c7-e3643eb43dde
  Args:
    source: August_Aleksander_Czartoryski
    literal_type: xsd:positiveInteger
    relation: :hasDeathYear
    literal_value: 1782
  AssignClass (753f7014-ef5d-494c-a59d-80eda45eecfe)
 Call ID: 753f7014-ef5d-494c-a59d-80eda45eecfe
  Args:
    type: :Woman
    source: Zofia_von_Dönhoff
  AssignClass (30b30655-38dd-4369-8e7b-d3d6944a2ca5)
 Call ID: 30b30655-38dd-4369-8e7b-d3d6944a2ca5
  Args:
    source: Zofia_von_Dönhoff
    type: :Person
  Finish (f981dcc6-96b8-42db-b8c9-e1261666c4ae)
 Call ID: f981dcc6-96b8-42db-b8c9-e1261666c4ae
  Args: