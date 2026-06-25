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
Prince Ludwig Rudolf of Hanover, of Great Britain and Ireland, Duke of Brunswick and Lüneburg (German: Ludwig Rudolf Georg Wilhelm Philipp Friedrich Wolrad Maximilian Prinz von Hannover) (21 November 1955 – 29 November 1988) was a member of the House of Hanover and a music producer.
Early life and career

Ludwig Rudolf was born in Hanover, Lower Saxony, Germany, the third child and second son of Ernst August, Prince of Hanover, Hereditary Prince of Brunswick (1914–1987) and his wife, Princess Ortrud of Schleswig-Holstein-Sonderburg-Glücksburg (1925–1980).
Ludwig Rudolf was a great-great-great-great-grandson of George III of the United Kingdom and a great-grandson of Wilhelm II, German Emperor.
Ludwig Rudolf had trained to become a music producer in Los Angeles and London.
Marriage and death

Having obtained the consent of Elizabeth II by Order in Council on 15 September 1987 pursuant to the Royal Marriages Act 1772, Ludwig Rudolf, a Lutheran, married the Roman Catholic Countess Isabella Maria von Thurn und Valsassina-Como-Vercelli (born September 8 1962 in Gmunden, Upper Austria), a former fashion model at her father's ancestral Austrian estate, Bleiburg Castle, Carinthia on 4 October 1987.
She was the daughter of Count Ariprand von Thurn und Valsassina-Como-Vercelli (1925–1996), whose family, an Austrian branch of the Della Torre dynasty, ruled Milan in the 13th and 14th century, and his wife, Princess Maria Perpetua Euphemia von Auersperg (born 1929).
In the early hours of 29 November 1988, after the couple had entertained guests at their home, Königinvilla (The Queen's Villa) in Gmunden, a house left to them by Ludwig Rudolf's elder brother Ernst August, the prince went to the bedroom where his wife had retired before midnight, and found Isabella sprawled fully dressed across their bed.
Ludwig Rudolf, who had been investigated previously on suspicion of illegal drug purchases, placed a call to his brother, Ernst August, in London, imploring him to take care of the couple's 10-month-old son.
As authorities removed Isabella's body and investigated the scene, discovering syringes, cocaine and heroin, Ludwig Rudolf slipped away.
Hours later, the prince was found in his car near his family's hunting lodge several miles away, on Lake Traun.
Ludwig Rudolf and Isabelle were interred on 2 December 1988 at Grünau
Custody of their infant son Otto Heinrich was awarded, contrary to the expressed wishes of Ludwig Rudolf, to the child's maternal grandparents.
He grew up at their castle, Schloss Bleiburg, in Austria, and then studied art at Braunschweig University of Art in Brunswick (Braunschweig).



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
  AssignClass (c2a0e655-bdba-4fe0-9256-cb9b644b39ce)
 Call ID: c2a0e655-bdba-4fe0-9256-cb9b644b39ce
  Args:
    type: :Man
    source: Ludwig_Rudolf_of_Hanover
  AssignClass (58905e44-396c-44ce-91fc-21674d87f308)
 Call ID: 58905e44-396c-44ce-91fc-21674d87f308
  Args:
    source: Ludwig_Rudolf_of_Hanover
    type: :Person
  AddLiteral (4d1ef02f-ac27-4829-96a1-9236a4dd77b2)
 Call ID: 4d1ef02f-ac27-4829-96a1-9236a4dd77b2
  Args:
    source: Ludwig_Rudolf_of_Hanover
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1955
  AddLiteral (fa3a6394-e692-46a8-9281-cdc733868c50)
 Call ID: fa3a6394-e692-46a8-9281-cdc733868c50
  Args:
    literal_type: xsd:integer
    source: Ludwig_Rudolf_of_Hanover
    relation: :hasDeathYear
    literal_value: 1988
  AssignClass (8dcb1ab6-ff9d-4e0a-8938-57ddf38fb836)
 Call ID: 8dcb1ab6-ff9d-4e0a-8938-57ddf38fb836
  Args:
    source: Ernst_August_Prince_of_Hanover
    type: :Man
  AssignClass (3947e420-1fca-45a0-8372-b463c5536f1e)
 Call ID: 3947e420-1fca-45a0-8372-b463c5536f1e
  Args:
    source: Ernst_August_Prince_of_Hanover
    type: :Person
  AssignClass (4eac906e-72e6-4722-9d3b-66e53e7881ac)
 Call ID: 4eac906e-72e6-4722-9d3b-66e53e7881ac
  Args:
    source: Ortrud_of_Schleswig-Holstein-Sonderburg-Glücksburg
    type: :Woman
  AssignClass (5ba9d42a-0722-4b7a-9639-194aede61d28)
 Call ID: 5ba9d42a-0722-4b7a-9639-194aede61d28
  Args:
    type: :Person
    source: Ortrud_of_Schleswig-Holstein-Sonderburg-Glücksburg
  AddTriple (8bfcd1a4-6e52-41d1-862b-b2c6c2e0e4a5)
 Call ID: 8bfcd1a4-6e52-41d1-862b-b2c6c2e0e4a5
  Args:
    relation: :hasFather
    source: Ludwig_Rudolf_of_Hanover
    target: Ernst_August_Prince_of_Hanover
  AddTriple (14d8aa4a-b010-4949-9092-019f4becc90c)
 Call ID: 14d8aa4a-b010-4949-9092-019f4becc90c
  Args:
    source: Ludwig_Rudolf_of_Hanover
    relation: :hasMother
    target: Ortrud_of_Schleswig-Holstein-Sonderburg-Glücksburg
  AssignClass (3e50d282-a88a-49fa-92fb-20e4f4c5d61e)
 Call ID: 3e50d282-a88a-49fa-92fb-20e4f4c5d61e
  Args:
    type: :Woman
    source: Isabella_Maria_von_Thurn_und_Valsassina-Como-Vercelli
  AssignClass (417e073b-eb3b-433b-a843-116f979da51c)
 Call ID: 417e073b-eb3b-433b-a843-116f979da51c
  Args:
    source: Isabella_Maria_von_Thurn_und_Valsassina-Como-Vercelli
    type: :Person
  AddTriple (b5c248b5-0558-46ab-9306-c7a3eae431af)
 Call ID: b5c248b5-0558-46ab-9306-c7a3eae431af
  Args:
    target: Isabella_Maria_von_Thurn_und_Valsassina-Como-Vercelli
    source: Ludwig_Rudolf_of_Hanover
    relation: :hasRelation
  AddLiteral (a34ac3e9-f81a-4fc7-9558-e5db8eaacba5)
 Call ID: a34ac3e9-f81a-4fc7-9558-e5db8eaacba5
  Args:
    literal_type: xsd:integer
    source: Ludwig_Rudolf_of_Hanover
    relation: :hasMarriageYear
    literal_value: 1987
  AssignClass (625ddeed-3f10-44b3-bece-94b474138223)
 Call ID: 625ddeed-3f10-44b3-bece-94b474138223
  Args:
    source: Ariprand_von_Thurn_und_Valsassina-Como-Vercelli
    type: :Man
  AssignClass (535bdb5e-5244-44b8-9d5b-2e3efd41b058)
 Call ID: 535bdb5e-5244-44b8-9d5b-2e3efd41b058
  Args:
    type: :Person
    source: Ariprand_von_Thurn_und_Valsassina-Como-Vercelli
  AssignClass (8329b2ee-eba2-4322-80eb-dba8f2a6e475)
 Call ID: 8329b2ee-eba2-4322-80eb-dba8f2a6e475
  Args:
    type: :Woman
    source: Maria_Perpetua_Euphemia_von_Auersperg
  AssignClass (7825f426-3a1f-4c85-a5e6-fae0c57c6775)
 Call ID: 7825f426-3a1f-4c85-a5e6-fae0c57c6775
  Args:
    source: Maria_Perpetua_Euphemia_von_Auersperg
    type: :Person
  AddTriple (76d186ed-a3eb-4fae-aa65-54e9653cac7e)
 Call ID: 76d186ed-a3eb-4fae-aa65-54e9653cac7e
  Args:
    relation: :hasFather
    source: Isabella_Maria_von_Thurn_und_Valsassina-Como-Vercelli
    target: Ariprand_von_Thurn_und_Valsassina-Como-Vercelli
  AddTriple (ecf3b374-51e6-49ee-a72a-255246b6f806)
 Call ID: ecf3b374-51e6-49ee-a72a-255246b6f806
  Args:
    target: Maria_Perpetua_Euphemia_von_Auersperg
    source: Isabella_Maria_von_Thurn_und_Valsassina-Como-Vercelli
    relation: :hasMother
  AssignClass (4e12b282-d017-4c94-b470-07085316fd82)
 Call ID: 4e12b282-d017-4c94-b470-07085316fd82
  Args:
    source: Otto_Heinrich
    type: :Man
  AssignClass (aa98dfeb-5427-4cb2-8c7e-c442bd7aa107)
 Call ID: aa98dfeb-5427-4cb2-8c7e-c442bd7aa107
  Args:
    type: :Person
    source: Otto_Heinrich
  AddTriple (6f07dba4-8484-4ccc-b3dd-3fe61cacea13)
 Call ID: 6f07dba4-8484-4ccc-b3dd-3fe61cacea13
  Args:
    target: Ludwig_Rudolf_of_Hanover
    relation: :hasFather
    source: Otto_Heinrich
  AddTriple (758418db-c13b-4e28-b4f2-e39ea9bad53c)
 Call ID: 758418db-c13b-4e28-b4f2-e39ea9bad53c
  Args:
    relation: :hasMother
    source: Otto_Heinrich
    target: Isabella_Maria_von_Thurn_und_Valsassina-Como-Vercelli
  AssignClass (c0e0f256-3767-4a8a-901d-f7f9cc58dc34)
 Call ID: c0e0f256-3767-4a8a-901d-f7f9cc58dc34
  Args:
    source: Ernst_August_Brother
    type: :Man
  AssignClass (b8afa14d-3b66-4016-b995-c8f9721c9c0a)
 Call ID: b8afa14d-3b66-4016-b995-c8f9721c9c0a
  Args:
    type: :Person
    source: Ernst_August_Brother
  AddTriple (9d4567fc-e9ed-4899-9872-e7f99bc469a1)
 Call ID: 9d4567fc-e9ed-4899-9872-e7f99bc469a1
  Args:
    target: Ludwig_Rudolf_of_Hanover
    relation: :isBrotherOf
    source: Ernst_August_Brother
  Finish (032368e3-c108-43e1-8c0d-4c4ba6a10a76)
 Call ID: 032368e3-c108-43e1-8c0d-4c4ba6a10a76
  Args: