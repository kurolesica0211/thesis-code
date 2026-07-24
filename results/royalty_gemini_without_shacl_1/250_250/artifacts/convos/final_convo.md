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
  AssignClass (84944504-916b-4aa5-9a50-f7980f64b90a)
 Call ID: 84944504-916b-4aa5-9a50-f7980f64b90a
  Args:
    type: :Man
    source: Ludwig_Rudolf_of_Hanover
  AssignClass (16a0b5a7-69fa-4ffc-875a-bd300b896705)
 Call ID: 16a0b5a7-69fa-4ffc-875a-bd300b896705
  Args:
    type: :Person
    source: Ludwig_Rudolf_of_Hanover
  AddLiteral (609934b8-3bd4-4756-9b85-ffdc5bba38ea)
 Call ID: 609934b8-3bd4-4756-9b85-ffdc5bba38ea
  Args:
    source: Ludwig_Rudolf_of_Hanover
    literal_value: 1955
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (2787c530-8ac5-4dbc-a7cc-fa7176de782b)
 Call ID: 2787c530-8ac5-4dbc-a7cc-fa7176de782b
  Args:
    literal_value: 1988
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: Ludwig_Rudolf_of_Hanover
  AssignClass (e820c2c4-8774-4dd6-b570-e016653c6239)
 Call ID: e820c2c4-8774-4dd6-b570-e016653c6239
  Args:
    source: Ernst_August_Prince_of_Hanover
    type: :Man
  AssignClass (336e3a6a-1815-4d41-ae9a-b79c0a6fc198)
 Call ID: 336e3a6a-1815-4d41-ae9a-b79c0a6fc198
  Args:
    type: :Ancestor
    source: Ernst_August_Prince_of_Hanover
  AssignClass (b9433dce-e5bf-4491-9cdd-1b70f9dab77f)
 Call ID: b9433dce-e5bf-4491-9cdd-1b70f9dab77f
  Args:
    source: Ernst_August_Prince_of_Hanover
    type: :Person
  AddLiteral (6dad6226-307e-415c-b237-7db00264dd61)
 Call ID: 6dad6226-307e-415c-b237-7db00264dd61
  Args:
    literal_value: 1914
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Ernst_August_Prince_of_Hanover
  AddLiteral (e81e58af-9158-4c57-8a47-1f06eb35be13)
 Call ID: e81e58af-9158-4c57-8a47-1f06eb35be13
  Args:
    source: Ernst_August_Prince_of_Hanover
    literal_value: 1987
    relation: :hasDeathYear
    literal_type: xsd:integer
  AssignClass (c08e8151-1583-4e28-9b6e-e63f5d47a9b9)
 Call ID: c08e8151-1583-4e28-9b6e-e63f5d47a9b9
  Args:
    source: Ortrud_of_Schleswig-Holstein-Sonderburg-Glücksburg
    type: :Woman
  AssignClass (707ed841-b8eb-4c69-9a6a-18635f745209)
 Call ID: 707ed841-b8eb-4c69-9a6a-18635f745209
  Args:
    source: Ortrud_of_Schleswig-Holstein-Sonderburg-Glücksburg
    type: :Ancestor
  AssignClass (4b8ec8b8-eb93-4301-95f5-d1443f2e8013)
 Call ID: 4b8ec8b8-eb93-4301-95f5-d1443f2e8013
  Args:
    source: Ortrud_of_Schleswig-Holstein-Sonderburg-Glücksburg
    type: :Person
  AddLiteral (456fdde2-6b7e-4364-8a9a-3380cd34cbfa)
 Call ID: 456fdde2-6b7e-4364-8a9a-3380cd34cbfa
  Args:
    source: Ortrud_of_Schleswig-Holstein-Sonderburg-Glücksburg
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1925
  AddLiteral (060a422c-3172-4a8f-82b7-3d7ecb7e0c1e)
 Call ID: 060a422c-3172-4a8f-82b7-3d7ecb7e0c1e
  Args:
    source: Ortrud_of_Schleswig-Holstein-Sonderburg-Glücksburg
    literal_value: 1980
    literal_type: xsd:integer
    relation: :hasDeathYear
  AddTriple (6e4be65d-450a-493f-b637-1d07b094ff54)
 Call ID: 6e4be65d-450a-493f-b637-1d07b094ff54
  Args:
    source: Ludwig_Rudolf_of_Hanover
    target: Ernst_August_Prince_of_Hanover
    relation: :hasFather
  AddTriple (63c7ee17-f5be-4a61-8b97-382201ecbde4)
 Call ID: 63c7ee17-f5be-4a61-8b97-382201ecbde4
  Args:
    target: Ortrud_of_Schleswig-Holstein-Sonderburg-Glücksburg
    relation: :hasMother
    source: Ludwig_Rudolf_of_Hanover
  AssignClass (755493a4-d5ee-497d-b6d2-6c5be4983a95)
 Call ID: 755493a4-d5ee-497d-b6d2-6c5be4983a95
  Args:
    source: Isabella_Maria_von_Thurn_und_Valsassina-Como-Vercelli
    type: :Woman
  AssignClass (d1315749-b1d7-4838-b31a-dc154226c3f6)
 Call ID: d1315749-b1d7-4838-b31a-dc154226c3f6
  Args:
    source: Isabella_Maria_von_Thurn_und_Valsassina-Como-Vercelli
    type: :Person
  AddLiteral (be13fa41-d618-44ef-bec8-79d9759bdd15)
 Call ID: be13fa41-d618-44ef-bec8-79d9759bdd15
  Args:
    source: Isabella_Maria_von_Thurn_und_Valsassina-Como-Vercelli
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1962
  AddTriple (658829a6-2a80-4a63-aa1a-e018cb76a99a)
 Call ID: 658829a6-2a80-4a63-aa1a-e018cb76a99a
  Args:
    source: Ludwig_Rudolf_of_Hanover
    target: Isabella_Maria_von_Thurn_und_Valsassina-Como-Vercelli
    relation: :hasMarriageYear
  AddLiteral (51620a8d-f5c6-4c36-893f-820dc7a2da35)
 Call ID: 51620a8d-f5c6-4c36-893f-820dc7a2da35
  Args:
    literal_value: 1987
    literal_type: xsd:integer
    relation: :hasMarriageYear
    source: Ludwig_Rudolf_of_Hanover
  AssignClass (abc5ecbe-fe53-4369-aae3-1fae033fa0bf)
 Call ID: abc5ecbe-fe53-4369-aae3-1fae033fa0bf
  Args:
    source: Ariprand_von_Thurn_und_Valsassina-Como-Vercelli
    type: :Man
  AssignClass (58ba0262-28ed-4fbc-808c-9811672b4173)
 Call ID: 58ba0262-28ed-4fbc-808c-9811672b4173
  Args:
    source: Ariprand_von_Thurn_und_Valsassina-Como-Vercelli
    type: :Ancestor
  AssignClass (e08229f8-4bb4-48e4-986f-b2d624cf016d)
 Call ID: e08229f8-4bb4-48e4-986f-b2d624cf016d
  Args:
    type: :Person
    source: Ariprand_von_Thurn_und_Valsassina-Como-Vercelli
  AddLiteral (50aea83b-7450-4f9d-9671-b174b583e453)
 Call ID: 50aea83b-7450-4f9d-9671-b174b583e453
  Args:
    source: Ariprand_von_Thurn_und_Valsassina-Como-Vercelli
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1925
  AddLiteral (576f0261-fc7e-4f98-83d1-4a11ced9ef40)
 Call ID: 576f0261-fc7e-4f98-83d1-4a11ced9ef40
  Args:
    source: Ariprand_von_Thurn_und_Valsassina-Como-Vercelli
    literal_value: 1996
    relation: :hasDeathYear
    literal_type: xsd:integer
  AssignClass (fa1a95d1-ec9e-4184-a726-d09d10195813)
 Call ID: fa1a95d1-ec9e-4184-a726-d09d10195813
  Args:
    type: :Woman
    source: Maria_Perpetua_Euphemia_von_Auersperg
  AssignClass (ac763ec1-3b48-43da-be1f-8c202696c1ba)
 Call ID: ac763ec1-3b48-43da-be1f-8c202696c1ba
  Args:
    source: Maria_Perpetua_Euphemia_von_Auersperg
    type: :Ancestor
  AssignClass (dcfa0f85-911d-4de5-b477-929093f3a534)
 Call ID: dcfa0f85-911d-4de5-b477-929093f3a534
  Args:
    source: Maria_Perpetua_Euphemia_von_Auersperg
    type: :Person
  AddLiteral (2be9bc97-dc91-49b5-9545-a7c9ca6d0d2b)
 Call ID: 2be9bc97-dc91-49b5-9545-a7c9ca6d0d2b
  Args:
    source: Maria_Perpetua_Euphemia_von_Auersperg
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1929
  AddTriple (6abc4c34-f677-41e7-95ad-7bed6756367c)
 Call ID: 6abc4c34-f677-41e7-95ad-7bed6756367c
  Args:
    target: Ariprand_von_Thurn_und_Valsassina-Como-Vercelli
    relation: :hasFather
    source: Isabella_Maria_von_Thurn_und_Valsassina-Como-Vercelli
  AddTriple (6e47e302-4033-49cb-8dd8-970c86a7c45b)
 Call ID: 6e47e302-4033-49cb-8dd8-970c86a7c45b
  Args:
    target: Maria_Perpetua_Euphemia_von_Auersperg
    relation: :hasMother
    source: Isabella_Maria_von_Thurn_und_Valsassina-Como-Vercelli
  AssignClass (c8bd6583-0dc4-43c2-87b4-62a637ab8493)
 Call ID: c8bd6583-0dc4-43c2-87b4-62a637ab8493
  Args:
    source: Otto_Heinrich
    type: :Man
  AssignClass (dc453666-a8f5-44f5-89a7-425ca1dec4d2)
 Call ID: dc453666-a8f5-44f5-89a7-425ca1dec4d2
  Args:
    type: :Person
    source: Otto_Heinrich
  AddTriple (d4b77beb-2e02-42ef-85ce-3d0329bb4286)
 Call ID: d4b77beb-2e02-42ef-85ce-3d0329bb4286
  Args:
    target: Ludwig_Rudolf_of_Hanover
    relation: :hasFather
    source: Otto_Heinrich
  AddTriple (9158afd2-2c5e-4809-8f03-05a823472b58)
 Call ID: 9158afd2-2c5e-4809-8f03-05a823472b58
  Args:
    source: Otto_Heinrich
    target: Isabella_Maria_von_Thurn_und_Valsassina-Como-Vercelli
    relation: :hasMother
  AssignClass (bb1ce0c8-6a08-433e-a0f3-0e346e407a37)
 Call ID: bb1ce0c8-6a08-433e-a0f3-0e346e407a37
  Args:
    type: :Man
    source: Ernst_August_Brother
  AssignClass (39dbfcbb-feb8-48f3-b351-92f9efbbafce)
 Call ID: 39dbfcbb-feb8-48f3-b351-92f9efbbafce
  Args:
    type: :Person
    source: Ernst_August_Brother
  AddTriple (468a95dd-c344-49e9-b88f-7e3217234f4d)
 Call ID: 468a95dd-c344-49e9-b88f-7e3217234f4d
  Args:
    source: Ludwig_Rudolf_of_Hanover
    relation: :hasBrother
    target: Ernst_August_Brother
  Finish (19b8564a-5299-44ae-a4f9-f8237665342f)
 Call ID: 19b8564a-5299-44ae-a4f9-f8237665342f
  Args: