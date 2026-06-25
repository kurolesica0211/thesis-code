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
  AssignClass (01df83bc-dd5b-46a9-ba69-135c83930184)
 Call ID: 01df83bc-dd5b-46a9-ba69-135c83930184
  Args:
    type: :Man
    source: :Aschwin_of_Lippe-Biesterfeld
  AssignClass (74c79f16-f137-40d7-b8dc-728d622755c9)
 Call ID: 74c79f16-f137-40d7-b8dc-728d622755c9
  Args:
    type: :Person
    source: :Aschwin_of_Lippe-Biesterfeld
  AddLiteral (916b2efe-88ad-44f9-a1e4-856205f7b66a)
 Call ID: 916b2efe-88ad-44f9-a1e4-856205f7b66a
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: :Aschwin_of_Lippe-Biesterfeld
    literal_value: 1914
  AddLiteral (a86cb235-3fad-4d99-83f1-ea0e3f4cbdbb)
 Call ID: a86cb235-3fad-4d99-83f1-ea0e3f4cbdbb
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: :Aschwin_of_Lippe-Biesterfeld
    literal_value: 1988
  AssignClass (2793d73f-b3d2-41cb-98a7-928a04ff8953)
 Call ID: 2793d73f-b3d2-41cb-98a7-928a04ff8953
  Args:
    type: :Man
    source: :Bernhard_of_Lippe-Biesterfeld
  AssignClass (1c01771d-6098-4e56-9e16-f969c530000d)
 Call ID: 1c01771d-6098-4e56-9e16-f969c530000d
  Args:
    type: :Person
    source: :Bernhard_of_Lippe-Biesterfeld
  AddTriple (3f059399-0b79-4c1d-95b4-ea77cfd67976)
 Call ID: 3f059399-0b79-4c1d-95b4-ea77cfd67976
  Args:
    relation: :isBrotherOf
    target: :Bernhard_of_Lippe-Biesterfeld
    source: :Aschwin_of_Lippe-Biesterfeld
  AddTriple (2a36f320-e410-4151-b89c-d4905cab906b)
 Call ID: 2a36f320-e410-4151-b89c-d4905cab906b
  Args:
    relation: :isBrotherOf
    target: :Aschwin_of_Lippe-Biesterfeld
    source: :Bernhard_of_Lippe-Biesterfeld
  AssignClass (528c3476-0bd6-4250-816c-fe5388f39fbf)
 Call ID: 528c3476-0bd6-4250-816c-fe5388f39fbf
  Args:
    type: :Man
    source: :Bernhard_of_Lippe
  AssignClass (d8ecf806-f014-440b-839b-d6259b3d6781)
 Call ID: d8ecf806-f014-440b-839b-d6259b3d6781
  Args:
    source: :Bernhard_of_Lippe
    type: :Person
  AssignClass (30f19f8a-aea6-4b18-b847-353ff8079ed4)
 Call ID: 30f19f8a-aea6-4b18-b847-353ff8079ed4
  Args:
    source: :Armgard_of_Sierstorpff-Cramm
    type: :Woman
  AssignClass (ac7bb283-a640-4625-93e4-28456bd1bccb)
 Call ID: ac7bb283-a640-4625-93e4-28456bd1bccb
  Args:
    type: :Person
    source: :Armgard_of_Sierstorpff-Cramm
  AddTriple (b10d31b9-f0d7-4c87-a171-0aa7a622eedf)
 Call ID: b10d31b9-f0d7-4c87-a171-0aa7a622eedf
  Args:
    source: :Aschwin_of_Lippe-Biesterfeld
    target: :Bernhard_of_Lippe
    relation: :isChildOf
  AddTriple (2868093a-d865-466a-b0ba-6d55050984ea)
 Call ID: 2868093a-d865-466a-b0ba-6d55050984ea
  Args:
    target: :Armgard_of_Sierstorpff-Cramm
    relation: :isChildOf
    source: :Aschwin_of_Lippe-Biesterfeld
  AssignClass (959567c4-5b31-411b-b278-9c481470c985)
 Call ID: 959567c4-5b31-411b-b278-9c481470c985
  Args:
    type: :Woman
    source: :Simone_Arnoux
  AssignClass (a99f67f4-53a7-4a0b-86e9-b0be7d1ef80f)
 Call ID: a99f67f4-53a7-4a0b-86e9-b0be7d1ef80f
  Args:
    type: :Person
    source: :Simone_Arnoux
  AddLiteral (736cfe89-2ca9-4af9-b99c-9f43b8cb4860)
 Call ID: 736cfe89-2ca9-4af9-b99c-9f43b8cb4860
  Args:
    source: :Aschwin_of_Lippe-Biesterfeld
    literal_value: 1951
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AddTriple (b388e690-eac6-4dc9-a282-b15e73e90501)
 Call ID: b388e690-eac6-4dc9-a282-b15e73e90501
  Args:
    relation: :hasRelation
    target: :Simone_Arnoux
    source: :Aschwin_of_Lippe-Biesterfeld
  AssignClass (ec649e7a-fcac-4e1f-a7e7-69edb220bf70)
 Call ID: ec649e7a-fcac-4e1f-a7e7-69edb220bf70
  Args:
    source: :Gottfried_Adam_Vollrat_von_Watzdorf
    type: :Man
  AssignClass (2f973738-2550-4259-b5e9-f117ab3eb5c1)
 Call ID: 2f973738-2550-4259-b5e9-f117ab3eb5c1
  Args:
    source: :Gottfried_Adam_Vollrat_von_Watzdorf
    type: :Person
  AssignClass (25e64630-e9c5-4fac-b3fc-f12a06251a86)
 Call ID: 25e64630-e9c5-4fac-b3fc-f12a06251a86
  Args:
    type: :Man
    source: :Stephan_von_Watzdorf
  AssignClass (5653a858-7c4e-4115-b27a-11f11df1d96c)
 Call ID: 5653a858-7c4e-4115-b27a-11f11df1d96c
  Args:
    type: :Person
    source: :Stephan_von_Watzdorf
  AssignClass (b12f6d5a-b4ce-4422-9a83-144d1ce7efe6)
 Call ID: b12f6d5a-b4ce-4422-9a83-144d1ce7efe6
  Args:
    type: :Man
    source: :Thilo_von_Watzdorf
  AssignClass (d78c41b5-1a3f-4a49-85a1-bf660350b0fb)
 Call ID: d78c41b5-1a3f-4a49-85a1-bf660350b0fb
  Args:
    type: :Person
    source: :Thilo_von_Watzdorf
  AddTriple (2fc44336-9322-4c03-828a-143763000149)
 Call ID: 2fc44336-9322-4c03-828a-143763000149
  Args:
    relation: :isChildOf
    target: :Simone_Arnoux
    source: :Stephan_von_Watzdorf
  AddTriple (ad271786-1543-4e3c-aaff-26e2416becd6)
 Call ID: ad271786-1543-4e3c-aaff-26e2416becd6
  Args:
    relation: :isChildOf
    target: :Gottfried_Adam_Vollrat_von_Watzdorf
    source: :Stephan_von_Watzdorf
  AddTriple (a64a9b71-d4cb-4f00-acd0-2576c4ccf7aa)
 Call ID: a64a9b71-d4cb-4f00-acd0-2576c4ccf7aa
  Args:
    source: :Thilo_von_Watzdorf
    target: :Simone_Arnoux
    relation: :isChildOf
  AddTriple (a01e4900-0e6d-454f-b5e3-c8aeec2aee97)
 Call ID: a01e4900-0e6d-454f-b5e3-c8aeec2aee97
  Args:
    source: :Thilo_von_Watzdorf
    target: :Gottfried_Adam_Vollrat_von_Watzdorf
    relation: :isChildOf
  AssignClass (a6dff520-dd0b-4701-ae4a-efc480146846)
 Call ID: a6dff520-dd0b-4701-ae4a-efc480146846
  Args:
    source: :Constantijn_of_the_Netherlands
    type: :Man
  AssignClass (f8a1e055-f8b4-4a4e-92fa-747565a9944e)
 Call ID: f8a1e055-f8b4-4a4e-92fa-747565a9944e
  Args:
    type: :Person
    source: :Constantijn_of_the_Netherlands
  Finish (71fc0dbb-ae2e-44e1-ba46-dff2b1f9790c)
 Call ID: 71fc0dbb-ae2e-44e1-ba46-dff2b1f9790c
  Args: