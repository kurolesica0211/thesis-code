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
Prince Aschwin of Lippe-Biesterfeld (13 June 1914 – 14 May 1988) was an expert in Chinese painting and Indian sculpture and curator at the Metropolitan Museum of Art in New York.
He was the younger brother of Prince Bernhard of Lippe-Biesterfeld.
Life and career

Aschwin was the second and last child of Prince Bernhard of Lippe and Baroness Armgard of Sierstorpff-Cramm.
He was born with the title of count of Biesterfeld and grew up with his elder brother Bernhard at their parents' estate, Castle Reckenwalde (now Wojnowo, Lubusz Voivodeship, Poland).
When Adolf Hitler came to power, Aschwin openly supported the Nazis and became a Wehrmacht officer.
During the war, Aschwin continued his education in East Asian art.
On 11 September 1951, Prince Aschwin married Simone Arnoux (1915-2001) in London.
She was previously married to German aristocrat Gottfried Adam Vollrat von Watzdorf, from whom she had two children (Stephan von Watzdorf, born 1942, and Thilo von Watzdorf, born 1944), but none with Prince Aschwin.
After the birth of Prince Constantijn of the Netherlands on 11 October 1969, Prince Aschwin became one of his godfathers.
Although Bernhard cut off communications with Nazi supporters, including his brother, their relationships resumed after the war.
In the 1970s, Bernhard persuaded Aschwin, who was suffering from Parkinson's disease, to return to the Netherlands, where he died in 1988, aged 73.
}} Media related to Aschwin of Lippe-Biesterfeld at Wikimedia Commons



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
  AssignClass (945790f2-72b3-4d25-ad9b-dbb0901e0c0b)
 Call ID: 945790f2-72b3-4d25-ad9b-dbb0901e0c0b
  Args:
    source: Aschwin_of_Lippe-Biesterfeld
    type: :Man
  AssignClass (a473b28b-6a7d-4414-9abb-0961c2c170b9)
 Call ID: a473b28b-6a7d-4414-9abb-0961c2c170b9
  Args:
    type: :Person
    source: Aschwin_of_Lippe-Biesterfeld
  AddLiteral (4e3d9084-6384-44d4-9dc7-c726f246ff84)
 Call ID: 4e3d9084-6384-44d4-9dc7-c726f246ff84
  Args:
    source: Aschwin_of_Lippe-Biesterfeld
    literal_value: 1914
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (0e65d427-0d91-4cfe-9996-23af7a462545)
 Call ID: 0e65d427-0d91-4cfe-9996-23af7a462545
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: Aschwin_of_Lippe-Biesterfeld
    literal_value: 1988
  AssignClass (6c5bb664-bff6-4eae-95d2-75afd4e20438)
 Call ID: 6c5bb664-bff6-4eae-95d2-75afd4e20438
  Args:
    source: Bernhard_of_Lippe-Biesterfeld
    type: :Man
  AssignClass (a822ed55-40b4-4eac-91fb-84fb68ca2336)
 Call ID: a822ed55-40b4-4eac-91fb-84fb68ca2336
  Args:
    type: :Person
    source: Bernhard_of_Lippe-Biesterfeld
  AddTriple (5a85e63e-8098-4827-a3f3-fbe14640e2e0)
 Call ID: 5a85e63e-8098-4827-a3f3-fbe14640e2e0
  Args:
    relation: :isBrotherOf
    source: Aschwin_of_Lippe-Biesterfeld
    target: Bernhard_of_Lippe-Biesterfeld
  AssignClass (f716a1d5-c459-45ff-8e33-f62cb81b8fa4)
 Call ID: f716a1d5-c459-45ff-8e33-f62cb81b8fa4
  Args:
    type: :Man
    source: Prince_Bernhard_of_Lippe
  AssignClass (b8549302-d6e5-4852-9167-f3da27af1179)
 Call ID: b8549302-d6e5-4852-9167-f3da27af1179
  Args:
    source: Prince_Bernhard_of_Lippe
    type: :Person
  AssignClass (be262672-c381-4756-85bf-363b3b23dc7f)
 Call ID: be262672-c381-4756-85bf-363b3b23dc7f
  Args:
    type: :Woman
    source: Baroness_Armgard_of_Sierstorpff-Cramm
  AssignClass (29c057ed-01f6-4934-b73b-bd1960b5bfd1)
 Call ID: 29c057ed-01f6-4934-b73b-bd1960b5bfd1
  Args:
    type: :Person
    source: Baroness_Armgard_of_Sierstorpff-Cramm
  AddTriple (42aa767b-e977-4607-931a-5dfbe5a3d396)
 Call ID: 42aa767b-e977-4607-931a-5dfbe5a3d396
  Args:
    target: Prince_Bernhard_of_Lippe
    source: Aschwin_of_Lippe-Biesterfeld
    relation: :hasFather
  AddTriple (0bf8005c-3d27-4c9e-8fca-5367bbb01d71)
 Call ID: 0bf8005c-3d27-4c9e-8fca-5367bbb01d71
  Args:
    target: Baroness_Armgard_of_Sierstorpff-Cramm
    source: Aschwin_of_Lippe-Biesterfeld
    relation: :hasMother
  AssignClass (b47ca11c-10d5-47d0-9da2-39ee961aae80)
 Call ID: b47ca11c-10d5-47d0-9da2-39ee961aae80
  Args:
    source: Simone_Arnoux
    type: :Woman
  AssignClass (bfc27676-53f0-4f2b-ba7c-0ff7644655dd)
 Call ID: bfc27676-53f0-4f2b-ba7c-0ff7644655dd
  Args:
    source: Simone_Arnoux
    type: :Person
  AddLiteral (94f0bf2d-37a9-44fe-b6f2-06ab1aa8fa4e)
 Call ID: 94f0bf2d-37a9-44fe-b6f2-06ab1aa8fa4e
  Args:
    literal_value: 1951
    source: Aschwin_of_Lippe-Biesterfeld
    relation: :hasMarriageYear
    literal_type: xsd:integer
  AddTriple (c025d3e3-543f-4445-bfaf-6d2e6cb01266)
 Call ID: c025d3e3-543f-4445-bfaf-6d2e6cb01266
  Args:
    target: Simone_Arnoux
    source: Aschwin_of_Lippe-Biesterfeld
    relation: :hasRelation
  AssignClass (fc1c1bdb-e501-4a22-8068-00e522f23a44)
 Call ID: fc1c1bdb-e501-4a22-8068-00e522f23a44
  Args:
    source: Gottfried_Adam_Vollrat_von_Watzdorf
    type: :Man
  AssignClass (45a16d91-594c-4581-b227-dba084110a25)
 Call ID: 45a16d91-594c-4581-b227-dba084110a25
  Args:
    source: Gottfried_Adam_Vollrat_von_Watzdorf
    type: :Person
  AddTriple (198a5de9-910d-4412-9465-dbc8595c84b2)
 Call ID: 198a5de9-910d-4412-9465-dbc8595c84b2
  Args:
    target: Gottfried_Adam_Vollrat_von_Watzdorf
    source: Simone_Arnoux
    relation: :hasRelation
  AssignClass (98f4fc7a-f619-4e82-b78b-ec776b9aaa6b)
 Call ID: 98f4fc7a-f619-4e82-b78b-ec776b9aaa6b
  Args:
    source: Stephan_von_Watzdorf
    type: :Man
  AssignClass (44add9de-1332-42a7-b73b-d3b3090e8eae)
 Call ID: 44add9de-1332-42a7-b73b-d3b3090e8eae
  Args:
    source: Stephan_von_Watzdorf
    type: :Person
  AssignClass (a3903bb8-8df4-4172-9cf5-f880178ede57)
 Call ID: a3903bb8-8df4-4172-9cf5-f880178ede57
  Args:
    source: Thilo_von_Watzdorf
    type: :Man
  AssignClass (f2c17fba-a216-43f3-a9a6-0dc89b8d8ed7)
 Call ID: f2c17fba-a216-43f3-a9a6-0dc89b8d8ed7
  Args:
    source: Thilo_von_Watzdorf
    type: :Person
  AddTriple (74073b05-f1f3-4036-b13f-43a016276a53)
 Call ID: 74073b05-f1f3-4036-b13f-43a016276a53
  Args:
    target: Gottfried_Adam_Vollrat_von_Watzdorf
    source: Stephan_von_Watzdorf
    relation: :hasFather
  AddTriple (ebf85110-393d-42ee-b74d-0b849bd6cb1e)
 Call ID: ebf85110-393d-42ee-b74d-0b849bd6cb1e
  Args:
    relation: :hasMother
    target: Simone_Arnoux
    source: Stephan_von_Watzdorf
  AddTriple (8fcd18a7-57cc-4a2a-8cd2-2ff7f8fd3d99)
 Call ID: 8fcd18a7-57cc-4a2a-8cd2-2ff7f8fd3d99
  Args:
    relation: :hasFather
    target: Gottfried_Adam_Vollrat_von_Watzdorf
    source: Thilo_von_Watzdorf
  AddTriple (a5f0081e-c0cc-445c-8590-a96b86dc5c97)
 Call ID: a5f0081e-c0cc-445c-8590-a96b86dc5c97
  Args:
    relation: :hasMother
    source: Thilo_von_Watzdorf
    target: Simone_Arnoux
  AssignClass (e46ed9f7-fe03-4083-9539-bb0990a91072)
 Call ID: e46ed9f7-fe03-4083-9539-bb0990a91072
  Args:
    type: :Man
    source: Prince_Constantijn_of_the_Netherlands
  AssignClass (46b41e0a-557b-4127-bccc-ffe57fa4f7d8)
 Call ID: 46b41e0a-557b-4127-bccc-ffe57fa4f7d8
  Args:
    type: :Person
    source: Prince_Constantijn_of_the_Netherlands
  Finish (14211b98-b9db-40cd-bef2-71774419a38e)
 Call ID: 14211b98-b9db-40cd-bef2-71774419a38e
  Args: