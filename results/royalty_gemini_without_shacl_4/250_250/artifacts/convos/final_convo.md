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
  AssignClass (ff17311a-9f08-4d18-aced-2fc383c69368)
 Call ID: ff17311a-9f08-4d18-aced-2fc383c69368
  Args:
    source: :Ludwig_Rudolf_of_Hanover
    type: :Man
  AssignClass (3f46820f-572d-4eaf-8ed7-789fcc6d72c8)
 Call ID: 3f46820f-572d-4eaf-8ed7-789fcc6d72c8
  Args:
    type: :Person
    source: :Ludwig_Rudolf_of_Hanover
  AddLiteral (b874eb42-aa1d-4d47-b86c-d3da832a9798)
 Call ID: b874eb42-aa1d-4d47-b86c-d3da832a9798
  Args:
    literal_type: xsd:integer
    source: :Ludwig_Rudolf_of_Hanover
    literal_value: 1955
    relation: :hasBirthYear
  AddLiteral (21413d7e-b69a-49b1-8067-0122491d8bf2)
 Call ID: 21413d7e-b69a-49b1-8067-0122491d8bf2
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: :Ludwig_Rudolf_of_Hanover
    literal_value: 1988
  AssignClass (f46f0e0d-3a5f-48e1-9217-2da9707cae8d)
 Call ID: f46f0e0d-3a5f-48e1-9217-2da9707cae8d
  Args:
    type: :Man
    source: :Ernst_August_Prince_of_Hanover
  AssignClass (99d76922-66e0-4e10-9076-aa57eb22026c)
 Call ID: 99d76922-66e0-4e10-9076-aa57eb22026c
  Args:
    source: :Ernst_August_Prince_of_Hanover
    type: :Person
  AddLiteral (c254635c-7205-4470-a71b-9c15b29720a6)
 Call ID: c254635c-7205-4470-a71b-9c15b29720a6
  Args:
    literal_type: xsd:integer
    source: :Ernst_August_Prince_of_Hanover
    literal_value: 1914
    relation: :hasBirthYear
  AddLiteral (4bd307fb-446e-4067-b0eb-99ed0181010d)
 Call ID: 4bd307fb-446e-4067-b0eb-99ed0181010d
  Args:
    literal_type: xsd:integer
    literal_value: 1987
    source: :Ernst_August_Prince_of_Hanover
    relation: :hasDeathYear
  AssignClass (a7c3e0b4-1958-4b47-a23b-f5afd4d989ec)
 Call ID: a7c3e0b4-1958-4b47-a23b-f5afd4d989ec
  Args:
    source: :Ortrud_of_Schleswig-Holstein-Sonderburg-Glücksburg
    type: :Woman
  AssignClass (cd00ac30-0f20-4d55-af88-c36010980450)
 Call ID: cd00ac30-0f20-4d55-af88-c36010980450
  Args:
    type: :Person
    source: :Ortrud_of_Schleswig-Holstein-Sonderburg-Glücksburg
  AddLiteral (f627a738-1b88-44c8-841e-29d03a8dd744)
 Call ID: f627a738-1b88-44c8-841e-29d03a8dd744
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: :Ortrud_of_Schleswig-Holstein-Sonderburg-Glücksburg
    literal_value: 1925
  AddLiteral (66f9e54d-7bdf-4e1e-8614-4e1fd601528d)
 Call ID: 66f9e54d-7bdf-4e1e-8614-4e1fd601528d
  Args:
    literal_value: 1980
    source: :Ortrud_of_Schleswig-Holstein-Sonderburg-Glücksburg
    relation: :hasDeathYear
    literal_type: xsd:integer
  AddTriple (603270a2-8046-4ccd-acef-bbf9fc020189)
 Call ID: 603270a2-8046-4ccd-acef-bbf9fc020189
  Args:
    source: :Ludwig_Rudolf_of_Hanover
    target: :Ernst_August_Prince_of_Hanover
    relation: :hasFather
  AddTriple (20bb446a-d158-4001-bad2-3e7f7ebdd182)
 Call ID: 20bb446a-d158-4001-bad2-3e7f7ebdd182
  Args:
    target: :Ortrud_of_Schleswig-Holstein-Sonderburg-Glücksburg
    source: :Ludwig_Rudolf_of_Hanover
    relation: :hasMother
  AssignClass (31d6281a-9329-4364-8480-a6980d837ae1)
 Call ID: 31d6281a-9329-4364-8480-a6980d837ae1
  Args:
    source: :Isabella_Maria_von_Thurn_und_Valsassina-Como-Vercelli
    type: :Woman
  AssignClass (2b138a99-e1c3-4a99-b408-4b8a7d7afbc7)
 Call ID: 2b138a99-e1c3-4a99-b408-4b8a7d7afbc7
  Args:
    type: :Person
    source: :Isabella_Maria_von_Thurn_und_Valsassina-Como-Vercelli
  AddLiteral (29b98445-5c84-4447-8b1d-c104a68a85b6)
 Call ID: 29b98445-5c84-4447-8b1d-c104a68a85b6
  Args:
    literal_value: 1962
    source: :Isabella_Maria_von_Thurn_und_Valsassina-Como-Vercelli
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddTriple (c0173412-ab12-4506-bf18-6e60d4dd89e2)
 Call ID: c0173412-ab12-4506-bf18-6e60d4dd89e2
  Args:
    relation: :hasMarriageYear
    source: :Ludwig_Rudolf_of_Hanover
    target: :Isabella_Maria_von_Thurn_und_Valsassina-Como-Vercelli
  AddLiteral (12e51890-4462-4087-95de-6cada91d8aa5)
 Call ID: 12e51890-4462-4087-95de-6cada91d8aa5
  Args:
    source: :Ludwig_Rudolf_of_Hanover
    literal_value: 1987
    relation: :hasMarriageYear
    literal_type: xsd:integer
  AssignClass (d2f767ae-0bac-422d-9c2b-b416dd555f6b)
 Call ID: d2f767ae-0bac-422d-9c2b-b416dd555f6b
  Args:
    type: :Man
    source: :Ariprand_von_Thurn_und_Valsassina-Como-Vercelli
  AssignClass (aba963af-fd4f-4960-aafe-6c4270582360)
 Call ID: aba963af-fd4f-4960-aafe-6c4270582360
  Args:
    type: :Person
    source: :Ariprand_von_Thurn_und_Valsassina-Como-Vercelli
  AddLiteral (37e47d25-4cfc-43a8-badf-920ab5b37fe0)
 Call ID: 37e47d25-4cfc-43a8-badf-920ab5b37fe0
  Args:
    literal_type: xsd:integer
    source: :Ariprand_von_Thurn_und_Valsassina-Como-Vercelli
    literal_value: 1925
    relation: :hasBirthYear
  AddLiteral (e2234a41-aedb-4b71-b0b8-9149f900884c)
 Call ID: e2234a41-aedb-4b71-b0b8-9149f900884c
  Args:
    literal_value: 1996
    source: :Ariprand_von_Thurn_und_Valsassina-Como-Vercelli
    relation: :hasDeathYear
    literal_type: xsd:integer
  AssignClass (8138567b-407f-4cee-87fd-a0b0af89838c)
 Call ID: 8138567b-407f-4cee-87fd-a0b0af89838c
  Args:
    type: :Woman
    source: :Maria_Perpetua_Euphemia_von_Auersperg
  AssignClass (371c7060-2636-4769-b6d8-929ccdc85aca)
 Call ID: 371c7060-2636-4769-b6d8-929ccdc85aca
  Args:
    type: :Person
    source: :Maria_Perpetua_Euphemia_von_Auersperg
  AddLiteral (7079491d-b02f-4bb5-884a-7c01a5a71019)
 Call ID: 7079491d-b02f-4bb5-884a-7c01a5a71019
  Args:
    relation: :hasBirthYear
    literal_value: 1929
    source: :Maria_Perpetua_Euphemia_von_Auersperg
    literal_type: xsd:integer
  AddTriple (426b6e14-56f0-486c-aaaa-36b8c33417c5)
 Call ID: 426b6e14-56f0-486c-aaaa-36b8c33417c5
  Args:
    source: :Isabella_Maria_von_Thurn_und_Valsassina-Como-Vercelli
    target: :Ariprand_von_Thurn_und_Valsassina-Como-Vercelli
    relation: :hasFather
  AddTriple (08765260-5436-4dc5-945f-7adafe3dc321)
 Call ID: 08765260-5436-4dc5-945f-7adafe3dc321
  Args:
    source: :Isabella_Maria_von_Thurn_und_Valsassina-Como-Vercelli
    target: :Maria_Perpetua_Euphemia_von_Auersperg
    relation: :hasMother
  AssignClass (60d224d5-c1b5-46b6-ae38-b712312b78a3)
 Call ID: 60d224d5-c1b5-46b6-ae38-b712312b78a3
  Args:
    source: :Otto_Heinrich
    type: :Man
  AssignClass (76ac28a5-4b0d-4a7e-b73d-6b21b6ea5bfc)
 Call ID: 76ac28a5-4b0d-4a7e-b73d-6b21b6ea5bfc
  Args:
    source: :Otto_Heinrich
    type: :Person
  AddTriple (0c9312ce-3331-47c2-a703-2cfd1cf71a48)
 Call ID: 0c9312ce-3331-47c2-a703-2cfd1cf71a48
  Args:
    source: :Otto_Heinrich
    target: :Ludwig_Rudolf_of_Hanover
    relation: :hasFather
  AddTriple (389332e8-7f5e-4478-875d-7959a6731ea0)
 Call ID: 389332e8-7f5e-4478-875d-7959a6731ea0
  Args:
    relation: :hasMother
    target: :Isabella_Maria_von_Thurn_und_Valsassina-Como-Vercelli
    source: :Otto_Heinrich
  AssignClass (88e34c41-dc7d-43fe-b625-a8087e6c7b7e)
 Call ID: 88e34c41-dc7d-43fe-b625-a8087e6c7b7e
  Args:
    type: :Man
    source: :Ernst_August_Brother
  AssignClass (de40cdaa-c225-48fe-9fb8-482267fed685)
 Call ID: de40cdaa-c225-48fe-9fb8-482267fed685
  Args:
    source: :Ernst_August_Brother
    type: :Person
  AddTriple (c212d515-1bd5-422c-8edf-a7bb8d34d38e)
 Call ID: c212d515-1bd5-422c-8edf-a7bb8d34d38e
  Args:
    relation: :hasBrother
    target: :Ernst_August_Brother
    source: :Ludwig_Rudolf_of_Hanover
  Finish (527b03be-fe7b-4169-8cf0-7cc880996546)
 Call ID: 527b03be-fe7b-4169-8cf0-7cc880996546
  Args: