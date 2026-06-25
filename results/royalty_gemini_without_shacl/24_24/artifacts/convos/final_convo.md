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
Duchess Marie Antoinette of Mecklenburg-Schwerin, also Manette (Marie Antoinette Margarethe Mathilde; 28 May 1884 – 26 October 1944) was the Duchess of Mecklenburg-Schwerin by birth and potential bride for King Alfonso XIII of Spain.
Early life

Marie Antoinette was born in Venice, into the House of Mecklenburg, as the third child and the second daughter of Duke Paul Frederick of Mecklenburg and Princess Marie of Windisch-Graetz.
Her brothers and sisters were Duke Paul Friedrich of Mecklenburg, Duchess Maria Luise of Mecklenburg-Schwerin (1883–1883), Duke Heinrich Borwin of Mecklenburg-Schwerin (1885–1942), and Duke Joseph of Mecklenburg-Schwerin (1889–1889).
She had a difficult relationship with her cousin Frederick Francis IV, Grand Duke of Mecklenburg-Schwerin, who regularly had to amortize her debts.
So, Marie Antoinette regularly had to sell archaeological artifacts belonging to her mother, excavated in Austria and Carniola, including Hallstatt Archaeological Site in Vače.
Potential bride for the King of Spain

She was German Kaiser Wilhelm II's candidate for a bride for King Alfonso XIII of Spain although he would marry the Kaiser's maternal first cousin, Princess Victoria Eugenie, niece of British King Edward VII.



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
  AssignClass (6ead31ff-58e2-4f83-83e2-3679811202fd)
 Call ID: 6ead31ff-58e2-4f83-83e2-3679811202fd
  Args:
    source: :MarieAntoinetteOfMecklenburgSchwerin
    type: :Woman
  AssignClass (784cf99b-b204-457b-94ba-3231d4110167)
 Call ID: 784cf99b-b204-457b-94ba-3231d4110167
  Args:
    type: :Person
    source: :MarieAntoinetteOfMecklenburgSchwerin
  AddLiteral (7a60e762-86f8-44e6-bba7-82b9ed5acf69)
 Call ID: 7a60e762-86f8-44e6-bba7-82b9ed5acf69
  Args:
    literal_value: Manette
    literal_type: xsd:string
    source: :MarieAntoinetteOfMecklenburgSchwerin
    relation: :alsoKnownAs
  AddLiteral (d4c503f1-216d-4c5e-ace5-81e64b5b3dfa)
 Call ID: d4c503f1-216d-4c5e-ace5-81e64b5b3dfa
  Args:
    source: :MarieAntoinetteOfMecklenburgSchwerin
    relation: :hasBirthYear
    literal_value: 1884
    literal_type: xsd:integer
  AddLiteral (760e0afa-185f-46ef-8f11-16bebc7b80ab)
 Call ID: 760e0afa-185f-46ef-8f11-16bebc7b80ab
  Args:
    relation: :hasDeathYear
    source: :MarieAntoinetteOfMecklenburgSchwerin
    literal_type: xsd:integer
    literal_value: 1944
  AssignClass (ae31b108-a614-4232-acfa-0d64b06b1b89)
 Call ID: ae31b108-a614-4232-acfa-0d64b06b1b89
  Args:
    source: :DukePaulFrederickOfMecklenburg
    type: :Man
  AssignClass (31901403-c1a9-4391-9ca3-c9e3403565d0)
 Call ID: 31901403-c1a9-4391-9ca3-c9e3403565d0
  Args:
    type: :Person
    source: :DukePaulFrederickOfMecklenburg
  AssignClass (6001a4c9-1e0e-4339-b694-44d9db9260ac)
 Call ID: 6001a4c9-1e0e-4339-b694-44d9db9260ac
  Args:
    type: :Woman
    source: :PrincessMarieOfWindischGraetz
  AssignClass (9acd10c0-1552-4405-a96f-c3f5d48e8d33)
 Call ID: 9acd10c0-1552-4405-a96f-c3f5d48e8d33
  Args:
    type: :Person
    source: :PrincessMarieOfWindischGraetz
  AddTriple (1011d0f1-1b16-4200-8cf4-1ea409125a0a)
 Call ID: 1011d0f1-1b16-4200-8cf4-1ea409125a0a
  Args:
    target: :DukePaulFrederickOfMecklenburg
    relation: :hasFather
    source: :MarieAntoinetteOfMecklenburgSchwerin
  AddTriple (7d520e33-2135-499e-9fca-5a01dd66244a)
 Call ID: 7d520e33-2135-499e-9fca-5a01dd66244a
  Args:
    source: :MarieAntoinetteOfMecklenburgSchwerin
    relation: :hasMother
    target: :PrincessMarieOfWindischGraetz
  AssignClass (33bf5a9c-7c63-45a6-a668-6a10b5c7eff6)
 Call ID: 33bf5a9c-7c63-45a6-a668-6a10b5c7eff6
  Args:
    type: :Man
    source: :DukePaulFriedrichOfMecklenburg
  AssignClass (36c6eef9-f1f0-4a6b-b60e-94e774061f47)
 Call ID: 36c6eef9-f1f0-4a6b-b60e-94e774061f47
  Args:
    source: :DukePaulFriedrichOfMecklenburg
    type: :Person
  AssignClass (559dd1ba-9994-4dd5-92ac-a67ea3bce1a9)
 Call ID: 559dd1ba-9994-4dd5-92ac-a67ea3bce1a9
  Args:
    source: :DuchessMariaLuiseOfMecklenburgSchwerin
    type: :Woman
  AssignClass (d1deaa64-db03-438f-b8f6-ae111081ca7a)
 Call ID: d1deaa64-db03-438f-b8f6-ae111081ca7a
  Args:
    type: :Person
    source: :DuchessMariaLuiseOfMecklenburgSchwerin
  AddLiteral (b6840523-37e2-4390-8d59-2f3d53a9786a)
 Call ID: b6840523-37e2-4390-8d59-2f3d53a9786a
  Args:
    relation: :hasBirthYear
    source: :DuchessMariaLuiseOfMecklenburgSchwerin
    literal_value: 1883
    literal_type: xsd:integer
  AddLiteral (f86f4cfb-ac35-47f5-86f6-187cb29d9ac4)
 Call ID: f86f4cfb-ac35-47f5-86f6-187cb29d9ac4
  Args:
    literal_type: xsd:integer
    literal_value: 1883
    relation: :hasDeathYear
    source: :DuchessMariaLuiseOfMecklenburgSchwerin
  AssignClass (7cc14bec-d552-4d82-95d0-820c4cea454c)
 Call ID: 7cc14bec-d552-4d82-95d0-820c4cea454c
  Args:
    type: :Man
    source: :DukeHeinrichBorwinOfMecklenburgSchwerin
  AssignClass (28d3ffdd-26c7-4eda-99e8-ce38ffb6190a)
 Call ID: 28d3ffdd-26c7-4eda-99e8-ce38ffb6190a
  Args:
    type: :Person
    source: :DukeHeinrichBorwinOfMecklenburgSchwerin
  AddLiteral (1aa2bfc4-10c7-42a6-8b9b-cc51a22b4730)
 Call ID: 1aa2bfc4-10c7-42a6-8b9b-cc51a22b4730
  Args:
    source: :DukeHeinrichBorwinOfMecklenburgSchwerin
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1885
  AddLiteral (72fe91fd-5a58-4f87-8e3f-3af0cec1a35f)
 Call ID: 72fe91fd-5a58-4f87-8e3f-3af0cec1a35f
  Args:
    relation: :hasDeathYear
    source: :DukeHeinrichBorwinOfMecklenburgSchwerin
    literal_value: 1942
    literal_type: xsd:integer
  AssignClass (dd756f00-bb3f-4f99-8539-653beff69964)
 Call ID: dd756f00-bb3f-4f99-8539-653beff69964
  Args:
    source: :DukeJosephOfMecklenburgSchwerin
    type: :Man
  AssignClass (686751c1-dbab-4709-a94b-63183f4241fd)
 Call ID: 686751c1-dbab-4709-a94b-63183f4241fd
  Args:
    type: :Person
    source: :DukeJosephOfMecklenburgSchwerin
  AddLiteral (f7d23f83-da61-4600-b3ac-50e3b2d84b4e)
 Call ID: f7d23f83-da61-4600-b3ac-50e3b2d84b4e
  Args:
    source: :DukeJosephOfMecklenburgSchwerin
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1889
  AddLiteral (3be5cd40-710c-4d12-b62a-5f75db76838b)
 Call ID: 3be5cd40-710c-4d12-b62a-5f75db76838b
  Args:
    literal_type: xsd:integer
    literal_value: 1889
    source: :DukeJosephOfMecklenburgSchwerin
    relation: :hasDeathYear
  AddTriple (91aef13c-354d-4a32-b177-9eea674949d6)
 Call ID: 91aef13c-354d-4a32-b177-9eea674949d6
  Args:
    target: :DukePaulFriedrichOfMecklenburg
    relation: :isSiblingOf
    source: :MarieAntoinetteOfMecklenburgSchwerin
  AddTriple (9c2ef724-4abf-4551-94b3-8f9aa27e25cc)
 Call ID: 9c2ef724-4abf-4551-94b3-8f9aa27e25cc
  Args:
    source: :MarieAntoinetteOfMecklenburgSchwerin
    relation: :isSiblingOf
    target: :DuchessMariaLuiseOfMecklenburgSchwerin
  AddTriple (4b2a25bf-acc1-43f4-837c-112b44b51c10)
 Call ID: 4b2a25bf-acc1-43f4-837c-112b44b51c10
  Args:
    target: :DukeHeinrichBorwinOfMecklenburgSchwerin
    source: :MarieAntoinetteOfMecklenburgSchwerin
    relation: :isSiblingOf
  AddTriple (1806434a-7f79-46b8-8d5e-ea8b9bf3128f)
 Call ID: 1806434a-7f79-46b8-8d5e-ea8b9bf3128f
  Args:
    target: :DukeJosephOfMecklenburgSchwerin
    relation: :isSiblingOf
    source: :MarieAntoinetteOfMecklenburgSchwerin
  AssignClass (edceb80b-f057-42fb-9a74-1b2e030fcf2a)
 Call ID: edceb80b-f057-42fb-9a74-1b2e030fcf2a
  Args:
    source: :FrederickFrancisIVGrandDukeOfMecklenburgSchwerin
    type: :Man
  AssignClass (dec800d0-0191-44f8-8f82-cd5fb93d4bba)
 Call ID: dec800d0-0191-44f8-8f82-cd5fb93d4bba
  Args:
    source: :FrederickFrancisIVGrandDukeOfMecklenburgSchwerin
    type: :Person
  AddTriple (67fb2cf5-7260-41cc-ba70-eb84ffa0c504)
 Call ID: 67fb2cf5-7260-41cc-ba70-eb84ffa0c504
  Args:
    source: :MarieAntoinetteOfMecklenburgSchwerin
    relation: :isBloodrelationOf
    target: :FrederickFrancisIVGrandDukeOfMecklenburgSchwerin
  Finish (0803f1ff-4a43-4427-b895-f036fbb49d3c)
 Call ID: 0803f1ff-4a43-4427-b895-f036fbb49d3c
  Args: