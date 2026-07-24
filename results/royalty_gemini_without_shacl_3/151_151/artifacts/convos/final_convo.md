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
  AssignClass (42085023-8d96-4907-8e6b-97c380e30b37)
 Call ID: 42085023-8d96-4907-8e6b-97c380e30b37
  Args:
    type: :Man
    source: Aschwin_of_Lippe-Biesterfeld
  AssignClass (b3c62fb0-6c5f-482d-b2d1-b85ad155c5de)
 Call ID: b3c62fb0-6c5f-482d-b2d1-b85ad155c5de
  Args:
    source: Aschwin_of_Lippe-Biesterfeld
    type: :Person
  AddLiteral (11867cc3-b604-496b-9434-b1c8a3e55c09)
 Call ID: 11867cc3-b604-496b-9434-b1c8a3e55c09
  Args:
    source: Aschwin_of_Lippe-Biesterfeld
    relation: :hasBirthYear
    literal_value: 1914
    literal_type: xsd:integer
  AddLiteral (2a3ce5de-1130-4a06-8d45-272851e9d74d)
 Call ID: 2a3ce5de-1130-4a06-8d45-272851e9d74d
  Args:
    relation: :hasDeathYear
    source: Aschwin_of_Lippe-Biesterfeld
    literal_value: 1988
    literal_type: xsd:integer
  AssignClass (9d646d18-623d-4f40-ac65-b98442c34d86)
 Call ID: 9d646d18-623d-4f40-ac65-b98442c34d86
  Args:
    source: Bernhard_of_Lippe-Biesterfeld
    type: :Man
  AssignClass (15163cff-44ed-4ff6-9fb1-b758f2874ae5)
 Call ID: 15163cff-44ed-4ff6-9fb1-b758f2874ae5
  Args:
    source: Bernhard_of_Lippe-Biesterfeld
    type: :Person
  AddTriple (5010d46d-9163-4591-b4c7-071f32e1c057)
 Call ID: 5010d46d-9163-4591-b4c7-071f32e1c057
  Args:
    target: Bernhard_of_Lippe-Biesterfeld
    source: Aschwin_of_Lippe-Biesterfeld
    relation: :hasBrother
  AssignClass (4189d17d-6952-4a2e-abf6-379f006fbc27)
 Call ID: 4189d17d-6952-4a2e-abf6-379f006fbc27
  Args:
    source: Bernhard_of_Lippe
    type: :Man
  AssignClass (edb5d2c7-5b90-4911-a660-b0250a8c997b)
 Call ID: edb5d2c7-5b90-4911-a660-b0250a8c997b
  Args:
    source: Bernhard_of_Lippe
    type: :Person
  AssignClass (5a11d78f-e901-42ca-877b-30820486804a)
 Call ID: 5a11d78f-e901-42ca-877b-30820486804a
  Args:
    source: Armgard_of_Sierstorpff-Cramm
    type: :Woman
  AssignClass (10e96972-4e35-40be-8a59-da1f41447cc6)
 Call ID: 10e96972-4e35-40be-8a59-da1f41447cc6
  Args:
    type: :Person
    source: Armgard_of_Sierstorpff-Cramm
  AddTriple (63acaf2f-f649-4271-8bca-0c0cf21ee4e9)
 Call ID: 63acaf2f-f649-4271-8bca-0c0cf21ee4e9
  Args:
    target: Bernhard_of_Lippe
    relation: :hasFather
    source: Aschwin_of_Lippe-Biesterfeld
  AddTriple (3661f8c0-1dbd-4974-a5cc-b525144113dd)
 Call ID: 3661f8c0-1dbd-4974-a5cc-b525144113dd
  Args:
    target: Armgard_of_Sierstorpff-Cramm
    source: Aschwin_of_Lippe-Biesterfeld
    relation: :hasMother
  AssignClass (5ac2b7f0-3997-4e63-9174-1357a76e09b5)
 Call ID: 5ac2b7f0-3997-4e63-9174-1357a76e09b5
  Args:
    type: :Woman
    source: Simone_Arnoux
  AssignClass (0cfc3728-21ba-4933-8aaa-da53794df1e8)
 Call ID: 0cfc3728-21ba-4933-8aaa-da53794df1e8
  Args:
    source: Simone_Arnoux
    type: :Person
  AddLiteral (4b2a0402-6779-4079-b286-50d172d3ff42)
 Call ID: 4b2a0402-6779-4079-b286-50d172d3ff42
  Args:
    literal_value: 1951
    literal_type: xsd:integer
    relation: :hasMarriageYear
    source: Aschwin_of_Lippe-Biesterfeld
  AddTriple (10d3ab13-fe8d-4ca6-915b-afa85edd77f4)
 Call ID: 10d3ab13-fe8d-4ca6-915b-afa85edd77f4
  Args:
    target: Simone_Arnoux
    source: Aschwin_of_Lippe-Biesterfeld
    relation: :hasRelation
  AssignClass (f4250957-dd3e-4d18-91b9-255ca41158e2)
 Call ID: f4250957-dd3e-4d18-91b9-255ca41158e2
  Args:
    source: Gottfried_Adam_Vollrat_von_Watzdorf
    type: :Man
  AssignClass (67c60d18-ab53-4026-b34e-5d0d79f47273)
 Call ID: 67c60d18-ab53-4026-b34e-5d0d79f47273
  Args:
    type: :Person
    source: Gottfried_Adam_Vollrat_von_Watzdorf
  AddTriple (57bfc4d3-f7a0-4fb6-b8f4-2a7378a32226)
 Call ID: 57bfc4d3-f7a0-4fb6-b8f4-2a7378a32226
  Args:
    target: Gottfried_Adam_Vollrat_von_Watzdorf
    source: Simone_Arnoux
    relation: :hasRelation
  AssignClass (51cb5d55-7adc-4030-bfc7-4194085e53c1)
 Call ID: 51cb5d55-7adc-4030-bfc7-4194085e53c1
  Args:
    type: :Man
    source: Stephan_von_Watzdorf
  AssignClass (92548cb6-f091-49b0-9694-a49fe9c20e4e)
 Call ID: 92548cb6-f091-49b0-9694-a49fe9c20e4e
  Args:
    source: Stephan_von_Watzdorf
    type: :Person
  AssignClass (a2f1fceb-f4ec-4de1-969d-3ffefe220a79)
 Call ID: a2f1fceb-f4ec-4de1-969d-3ffefe220a79
  Args:
    source: Thilo_von_Watzdorf
    type: :Man
  AssignClass (6e86aec8-9a96-4c96-ad8d-a1e0ff030a7d)
 Call ID: 6e86aec8-9a96-4c96-ad8d-a1e0ff030a7d
  Args:
    type: :Person
    source: Thilo_von_Watzdorf
  AddTriple (a09692d6-90ac-4dcf-9c70-a15bab4cb95f)
 Call ID: a09692d6-90ac-4dcf-9c70-a15bab4cb95f
  Args:
    source: Stephan_von_Watzdorf
    relation: :isSonOf
    target: Simone_Arnoux
  AddTriple (6460f652-2b92-41b3-8686-0e9891fc0f3d)
 Call ID: 6460f652-2b92-41b3-8686-0e9891fc0f3d
  Args:
    relation: :isSonOf
    source: Stephan_von_Watzdorf
    target: Gottfried_Adam_Vollrat_von_Watzdorf
  AddTriple (458cd3f7-d014-41b0-9893-50f6ea19f523)
 Call ID: 458cd3f7-d014-41b0-9893-50f6ea19f523
  Args:
    relation: :isSonOf
    source: Thilo_von_Watzdorf
    target: Simone_Arnoux
  AddTriple (3b8f4270-cae0-460e-a761-11aa51887a91)
 Call ID: 3b8f4270-cae0-460e-a761-11aa51887a91
  Args:
    target: Gottfried_Adam_Vollrat_von_Watzdorf
    source: Thilo_von_Watzdorf
    relation: :isSonOf
  AssignClass (46a092c2-036e-4ea3-8621-2247754ff35c)
 Call ID: 46a092c2-036e-4ea3-8621-2247754ff35c
  Args:
    type: :Man
    source: Constantijn_of_the_Netherlands
  AssignClass (e70f1c16-12e7-4715-b9cb-adc582be9ba8)
 Call ID: e70f1c16-12e7-4715-b9cb-adc582be9ba8
  Args:
    source: Constantijn_of_the_Netherlands
    type: :Person
  Finish (d2aa7857-0ada-4051-9a0c-614327c20258)
 Call ID: d2aa7857-0ada-4051-9a0c-614327c20258
  Args: