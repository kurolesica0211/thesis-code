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
@prefix ns1: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
@prefix ns2: <http://www.w3.org/2003/11/swrl#> .
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

ns1:isRuleEnabled a owl:AnnotationProperty .

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

:x a ns2:Variable .

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

:y a ns2:Variable .

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

[] a ns2:Imp ;
    rdfs:label "infer hasSon" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasBrother" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasSister" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (79c044cc-28f5-4452-8afb-d32c1821338a)
 Call ID: 79c044cc-28f5-4452-8afb-d32c1821338a
  Args:
    source: Ludwig_Rudolf_of_Hanover
    type: :Man
  AssignClass (2f6f2bb7-ddcf-45a8-a59a-e1c77020b4f8)
 Call ID: 2f6f2bb7-ddcf-45a8-a59a-e1c77020b4f8
  Args:
    source: Ernst_August_Prince_of_Hanover
    type: :Man
  AssignClass (c957e096-5d5e-4d54-8089-0d9f7cc24864)
 Call ID: c957e096-5d5e-4d54-8089-0d9f7cc24864
  Args:
    type: :Woman
    source: Ortrud_of_Schleswig-Holstein-Sonderburg-Glücksburg
  AssignClass (b5fe04e0-e049-43c9-8427-bd41095e9714)
 Call ID: b5fe04e0-e049-43c9-8427-bd41095e9714
  Args:
    source: Isabella_Maria_von_Thurn_und_Valsassina-Como-Vercelli
    type: :Woman
  AssignClass (4e5ec35c-11d0-42e7-8720-fe6c4428b36f)
 Call ID: 4e5ec35c-11d0-42e7-8720-fe6c4428b36f
  Args:
    type: :Man
    source: Ariprand_von_Thurn_und_Valsassina-Como-Vercelli
  AssignClass (0ab3dfb6-3c14-411b-acbc-a29452ecf625)
 Call ID: 0ab3dfb6-3c14-411b-acbc-a29452ecf625
  Args:
    source: Maria_Perpetua_Euphemia_von_Auersperg
    type: :Woman
  AssignClass (262ce905-7d46-4511-aa78-edaf291d6494)
 Call ID: 262ce905-7d46-4511-aa78-edaf291d6494
  Args:
    type: :Man
    source: Otto_Heinrich
  AssignClass (971af3e0-8902-4027-9f14-fab102c20856)
 Call ID: 971af3e0-8902-4027-9f14-fab102c20856
  Args:
    source: Ernst_August_elder_brother
    type: :Man
  AddLiteral (538c35ae-b465-4b77-bee8-2a09778ee8d7)
 Call ID: 538c35ae-b465-4b77-bee8-2a09778ee8d7
  Args:
    literal_value: 1955
    source: Ludwig_Rudolf_of_Hanover
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (1c65e5e9-f9d5-4c8e-b94f-3ba031e33e8e)
 Call ID: 1c65e5e9-f9d5-4c8e-b94f-3ba031e33e8e
  Args:
    source: Ludwig_Rudolf_of_Hanover
    literal_value: 1988
    relation: :hasDeathYear
    literal_type: xsd:integer
  AddLiteral (4d51e6cf-78c3-40d1-9879-1063fb2065af)
 Call ID: 4d51e6cf-78c3-40d1-9879-1063fb2065af
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1914
    source: Ernst_August_Prince_of_Hanover
  AddLiteral (8ec51e73-f07d-44ad-aeab-0dc608c4e8e1)
 Call ID: 8ec51e73-f07d-44ad-aeab-0dc608c4e8e1
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1987
    source: Ernst_August_Prince_of_Hanover
  AddLiteral (baccc443-9a34-4d36-97c7-37e48854637a)
 Call ID: baccc443-9a34-4d36-97c7-37e48854637a
  Args:
    source: Ortrud_of_Schleswig-Holstein-Sonderburg-Glücksburg
    literal_value: 1925
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (c1ea8313-7681-4cac-8539-eadda1c69130)
 Call ID: c1ea8313-7681-4cac-8539-eadda1c69130
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1980
    source: Ortrud_of_Schleswig-Holstein-Sonderburg-Glücksburg
  AddLiteral (b9d95309-e5d4-4677-831f-068d09187a0e)
 Call ID: b9d95309-e5d4-4677-831f-068d09187a0e
  Args:
    source: Isabella_Maria_von_Thurn_und_Valsassina-Como-Vercelli
    literal_value: 1962
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (3e7c7fff-5627-409f-b855-19af638c12eb)
 Call ID: 3e7c7fff-5627-409f-b855-19af638c12eb
  Args:
    source: Ariprand_von_Thurn_und_Valsassina-Como-Vercelli
    literal_value: 1925
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (95fd8205-2fca-4e5d-a71f-a834d1d4d707)
 Call ID: 95fd8205-2fca-4e5d-a71f-a834d1d4d707
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 1996
    source: Ariprand_von_Thurn_und_Valsassina-Como-Vercelli
  AddLiteral (5853eac1-d2e2-4947-8f9c-84d805ef3a4b)
 Call ID: 5853eac1-d2e2-4947-8f9c-84d805ef3a4b
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Maria_Perpetua_Euphemia_von_Auersperg
    literal_value: 1929
  AddTriple (67ca7170-41d7-4104-8b6c-7cda5d8e180b)
 Call ID: 67ca7170-41d7-4104-8b6c-7cda5d8e180b
  Args:
    source: Ludwig_Rudolf_of_Hanover
    target: Ernst_August_Prince_of_Hanover
    relation: :hasFather
  AddTriple (59c84728-b3e2-4958-9d65-c1d9437f9ce2)
 Call ID: 59c84728-b3e2-4958-9d65-c1d9437f9ce2
  Args:
    target: Ortrud_of_Schleswig-Holstein-Sonderburg-Glücksburg
    relation: :hasMother
    source: Ludwig_Rudolf_of_Hanover
  AddTriple (cd74309f-d301-45d6-90af-36874d9ce615)
 Call ID: cd74309f-d301-45d6-90af-36874d9ce615
  Args:
    target: Ariprand_von_Thurn_und_Valsassina-Como-Vercelli
    relation: :hasFather
    source: Isabella_Maria_von_Thurn_und_Valsassina-Como-Vercelli
  AddTriple (a9d1892a-9f4e-4c65-84db-11c4bbc4fd7f)
 Call ID: a9d1892a-9f4e-4c65-84db-11c4bbc4fd7f
  Args:
    target: Maria_Perpetua_Euphemia_von_Auersperg
    relation: :hasMother
    source: Isabella_Maria_von_Thurn_und_Valsassina-Como-Vercelli
  AddTriple (05e54ddc-85f8-4ce3-ad3c-e375703ed627)
 Call ID: 05e54ddc-85f8-4ce3-ad3c-e375703ed627
  Args:
    source: Otto_Heinrich
    relation: :hasFather
    target: Ludwig_Rudolf_of_Hanover
  AddTriple (9372fad5-e3f8-4a71-906a-118fb20f9932)
 Call ID: 9372fad5-e3f8-4a71-906a-118fb20f9932
  Args:
    source: Otto_Heinrich
    target: Isabella_Maria_von_Thurn_und_Valsassina-Como-Vercelli
    relation: :hasMother
  AddTriple (7706d737-69f5-43e1-8d21-b1d9e36541f0)
 Call ID: 7706d737-69f5-43e1-8d21-b1d9e36541f0
  Args:
    relation: :hasBrother
    target: Ernst_August_elder_brother
    source: Ludwig_Rudolf_of_Hanover
  AddTriple (20d0b21a-3218-4970-a009-c8c6ea1420d7)
 Call ID: 20d0b21a-3218-4970-a009-c8c6ea1420d7
  Args:
    source: Ernst_August_elder_brother
    relation: :hasBrother
    target: Ludwig_Rudolf_of_Hanover
  AddLiteral (f85b9c44-d05b-4da5-aed9-e8d5e31371cc)
 Call ID: f85b9c44-d05b-4da5-aed9-e8d5e31371cc
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    source: Ludwig_Rudolf_of_Hanover
    literal_value: 1987
  AddTriple (1a0155d4-56c1-4066-91b9-ae3857459c8e)
 Call ID: 1a0155d4-56c1-4066-91b9-ae3857459c8e
  Args:
    relation: :hasRelation
    target: Isabella_Maria_von_Thurn_und_Valsassina-Como-Vercelli
    source: Ludwig_Rudolf_of_Hanover
  Finish (3736a36d-9546-416e-9c51-0edbea327f90)
 Call ID: 3736a36d-9546-416e-9c51-0edbea327f90
  Args: