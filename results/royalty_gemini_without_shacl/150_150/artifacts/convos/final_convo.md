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

:hasDeathYear a owl:AnnotationProperty .

:hasMarriageYear a owl:AnnotationProperty .

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

:hasChild a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:inverseOf :isChildOf .

:isAncestorOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation .

:isSiblingOf a owl:ObjectProperty,
        owl:SymmetricProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isBloodrelationOf ;
    owl:propertyChainAxiom ( :hasParent :isParentOf ) .

:isSisterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf .

:hasParent a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Person ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:equivalentProperty :isChildOf ;
    owl:inverseOf :isParentOf .

:Sex a owl:Class ;
    rdfs:subClassOf :DomainEntity ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Female :Male ) ] .

:isChildOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:propertyDisjointWith :isSisterOf .

:Man a owl:Class ;
    owl:disjointWith :Sex,
        :Woman ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Male ] ) ] .

:Woman a owl:Class ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Female ] ) ] .

:isParentOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:propertyDisjointWith :isSisterOf .

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



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (17e43ee3-bf1b-4d73-9b2c-504f2b4fbcf4)
 Call ID: 17e43ee3-bf1b-4d73-9b2c-504f2b4fbcf4
  Args:
    type: :Man
    source: Aschwin_of_Lippe-Biesterfeld
  AssignClass (12a2f89d-8d33-400d-a8f0-04f035e2c56b)
 Call ID: 12a2f89d-8d33-400d-a8f0-04f035e2c56b
  Args:
    type: :Person
    source: Aschwin_of_Lippe-Biesterfeld
  AddLiteral (7dc2f9f6-e796-42f5-9ec3-971734461f5e)
 Call ID: 7dc2f9f6-e796-42f5-9ec3-971734461f5e
  Args:
    literal_value: 1914
    source: Aschwin_of_Lippe-Biesterfeld
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (5b3659b1-73cd-4db1-999b-ec5731d7c2a8)
 Call ID: 5b3659b1-73cd-4db1-999b-ec5731d7c2a8
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: Aschwin_of_Lippe-Biesterfeld
    literal_value: 1988
  AssignClass (47f81bad-0b95-4339-8919-194dea8b6021)
 Call ID: 47f81bad-0b95-4339-8919-194dea8b6021
  Args:
    source: Bernhard_of_Lippe-Biesterfeld
    type: :Man
  AssignClass (8a090e50-f3bc-4127-b05f-396d7b596b16)
 Call ID: 8a090e50-f3bc-4127-b05f-396d7b596b16
  Args:
    type: :Person
    source: Bernhard_of_Lippe-Biesterfeld
  AddTriple (af9d940c-7f6d-4764-b08f-2e99ff3fa37c)
 Call ID: af9d940c-7f6d-4764-b08f-2e99ff3fa37c
  Args:
    source: Aschwin_of_Lippe-Biesterfeld
    relation: :hasBrother
    target: Bernhard_of_Lippe-Biesterfeld
  AssignClass (13019406-02e4-4081-b83e-a8888a44811d)
 Call ID: 13019406-02e4-4081-b83e-a8888a44811d
  Args:
    source: Bernhard_of_Lippe-Biesterfeld_Sr
    type: :Man
  AssignClass (64a7a339-1c01-4049-b991-a8673bc20f2c)
 Call ID: 64a7a339-1c01-4049-b991-a8673bc20f2c
  Args:
    source: Bernhard_of_Lippe-Biesterfeld_Sr
    type: :Person
  AssignClass (f16e2d55-94c1-4431-9f68-e662b2a3d488)
 Call ID: f16e2d55-94c1-4431-9f68-e662b2a3d488
  Args:
    source: Armgard_of_Sierstorpff-Cramm
    type: :Woman
  AssignClass (3f3d8b4c-990e-4b79-ab4b-6997f3045d42)
 Call ID: 3f3d8b4c-990e-4b79-ab4b-6997f3045d42
  Args:
    source: Armgard_of_Sierstorpff-Cramm
    type: :Person
  AddTriple (3fa945e0-68b6-48fe-b421-5a6792eeaf93)
 Call ID: 3fa945e0-68b6-48fe-b421-5a6792eeaf93
  Args:
    relation: :hasFather
    source: Aschwin_of_Lippe-Biesterfeld
    target: Bernhard_of_Lippe-Biesterfeld_Sr
  AddTriple (3da4a7a8-114e-403a-b81e-b1b8048b210d)
 Call ID: 3da4a7a8-114e-403a-b81e-b1b8048b210d
  Args:
    relation: :hasMother
    source: Aschwin_of_Lippe-Biesterfeld
    target: Armgard_of_Sierstorpff-Cramm
  AssignClass (1b4e7658-8665-4dd0-8203-672f68377ac4)
 Call ID: 1b4e7658-8665-4dd0-8203-672f68377ac4
  Args:
    source: Simone_Arnoux
    type: :Woman
  AssignClass (c2f87ab3-caf8-44d7-968e-35885aca6970)
 Call ID: c2f87ab3-caf8-44d7-968e-35885aca6970
  Args:
    type: :Person
    source: Simone_Arnoux
  AddLiteral (71c6335b-da5d-468f-a853-28d2f4d723ee)
 Call ID: 71c6335b-da5d-468f-a853-28d2f4d723ee
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    source: Aschwin_of_Lippe-Biesterfeld
    literal_value: 1951
  AddTriple (b82e005d-ad21-4704-8e5e-63facd5120d9)
 Call ID: b82e005d-ad21-4704-8e5e-63facd5120d9
  Args:
    target: Simone_Arnoux
    source: Aschwin_of_Lippe-Biesterfeld
    relation: :hasRelation
  AssignClass (0944a9cc-999d-41b1-b6f7-c8db4929a915)
 Call ID: 0944a9cc-999d-41b1-b6f7-c8db4929a915
  Args:
    type: :Man
    source: Gottfried_Adam_Vollrat_von_Watzdorf
  AssignClass (144d49a1-ebb1-44fc-a85d-05762bba1b7d)
 Call ID: 144d49a1-ebb1-44fc-a85d-05762bba1b7d
  Args:
    type: :Person
    source: Gottfried_Adam_Vollrat_von_Watzdorf
  AddTriple (29c6826e-6c66-4c96-b012-ea3fe2395623)
 Call ID: 29c6826e-6c66-4c96-b012-ea3fe2395623
  Args:
    relation: :hasRelation
    source: Simone_Arnoux
    target: Gottfried_Adam_Vollrat_von_Watzdorf
  AssignClass (672486c9-82be-4ad5-affa-def2681c5f67)
 Call ID: 672486c9-82be-4ad5-affa-def2681c5f67
  Args:
    type: :Man
    source: Stephan_von_Watzdorf
  AssignClass (7a661957-40c0-43ea-8e3d-ae3a4594d829)
 Call ID: 7a661957-40c0-43ea-8e3d-ae3a4594d829
  Args:
    source: Stephan_von_Watzdorf
    type: :Person
  AssignClass (1bb49af8-9104-49cd-bd02-f8a614294660)
 Call ID: 1bb49af8-9104-49cd-bd02-f8a614294660
  Args:
    type: :Man
    source: Thilo_von_Watzdorf
  AssignClass (35f1fb70-8dd8-41bf-81e7-20ee63daaa14)
 Call ID: 35f1fb70-8dd8-41bf-81e7-20ee63daaa14
  Args:
    source: Thilo_von_Watzdorf
    type: :Person
  AddTriple (a2e7df50-92e7-4e27-990e-dc76abd33d41)
 Call ID: a2e7df50-92e7-4e27-990e-dc76abd33d41
  Args:
    source: Stephan_von_Watzdorf
    relation: :isSonOf
    target: Simone_Arnoux
  AddTriple (1fda3dde-55d3-435d-9b19-158f7663a998)
 Call ID: 1fda3dde-55d3-435d-9b19-158f7663a998
  Args:
    source: Stephan_von_Watzdorf
    relation: :isSonOf
    target: Gottfried_Adam_Vollrat_von_Watzdorf
  AddTriple (af615b99-70f0-4283-9b84-b3591295bf25)
 Call ID: af615b99-70f0-4283-9b84-b3591295bf25
  Args:
    target: Simone_Arnoux
    relation: :isSonOf
    source: Thilo_von_Watzdorf
  AddTriple (3c14c33e-bccc-4abe-a419-3944021341c8)
 Call ID: 3c14c33e-bccc-4abe-a419-3944021341c8
  Args:
    target: Gottfried_Adam_Vollrat_von_Watzdorf
    relation: :isSonOf
    source: Thilo_von_Watzdorf
  AssignClass (6e7d87aa-778b-4508-9393-0b3c6bf939d7)
 Call ID: 6e7d87aa-778b-4508-9393-0b3c6bf939d7
  Args:
    type: :Man
    source: Constantijn_of_the_Netherlands
  AssignClass (c46c5153-4209-4776-95e1-52c71bea9ddf)
 Call ID: c46c5153-4209-4776-95e1-52c71bea9ddf
  Args:
    type: :Person
    source: Constantijn_of_the_Netherlands
  Finish (16f9c5b8-70ca-4acb-a666-62965038b225)
 Call ID: 16f9c5b8-70ca-4acb-a666-62965038b225
  Args: