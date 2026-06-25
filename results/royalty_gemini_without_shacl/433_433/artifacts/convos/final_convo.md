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
Bernhard, Prince of Saxe-Meiningen (German: Bernhard, Prinz von Sachsen-Meiningen; 30 June 1901 – 4 October 1984) was the head of the House of Saxe-Meiningen from 1946 until his death.
Prince of Saxe-Meiningen

Bernhard was born in Köln the third son of Prince Frederick Johann of Saxe-Meiningen and Countess Adelaide of Lippe-Biesterfeld.
His father was the second son of Georg II, Duke of Saxe-Meiningen and his mother a daughter of Count Ernst of Lippe-Biesterfeld.
After the death of his older brother Prince Georg in 1946 his nephew Prince Frederick Alfred renounced his succession rights and so Bernhard succeeded to the headship of the house of Saxe-Meiningen and the nominal title of Duke of Saxe-Meiningen (as Bernhard IV).
As his first marriage was morganatic his second son Prince Frederick Konrad succeeded him as head of the ducal house following his death in Bad Krozingen.
Bernhard and his first wife were declared guilty of a Nazi conspiracy against Austria in 1933; he was sentenced to six weeks in prison, while she was placed under house arrest.
Family

Bernhard was married morganatically to Margot Grössler (1911–1998), from Wrocław, daughter of Friedrich Grössler, a merchant, and Erika Wägner, in Eichenhof
They had two children, both of whom had no succession rights:


Bernhard married secondly in Ziegenberg über Bad Nauheim on 11 August 1948 to Baroness Vera Schäffer von Bernstein (1914–1994), daughter of Baron Friedrich "Fritz" Schäffer von Bernstein (1868–1958) and Emma Carola, née Passavant (1884–1971).
They had three children, including a son, Konrad, with full rights to the succession to the house of Saxe-Meiningen:


Ancestry

References



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
  AssignClass (34443729-a792-4569-951f-c0bb64fceb75)
 Call ID: 34443729-a792-4569-951f-c0bb64fceb75
  Args:
    type: :Man
    source: Bernhard_Prince_of_Saxe-Meiningen
  AssignClass (32bcfc9c-13c7-49b4-9bfd-a202b9c1eda1)
 Call ID: 32bcfc9c-13c7-49b4-9bfd-a202b9c1eda1
  Args:
    source: Bernhard_Prince_of_Saxe-Meiningen
    type: :Person
  AddLiteral (b51098ea-1365-473a-9962-9a2e87ef3e3b)
 Call ID: b51098ea-1365-473a-9962-9a2e87ef3e3b
  Args:
    source: Bernhard_Prince_of_Saxe-Meiningen
    literal_value: 1901
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (7768d73a-3c51-4676-9478-6f9202718d9c)
 Call ID: 7768d73a-3c51-4676-9478-6f9202718d9c
  Args:
    relation: :hasDeathYear
    source: Bernhard_Prince_of_Saxe-Meiningen
    literal_value: 1984
    literal_type: xsd:integer
  AssignClass (0f36ac31-ced4-4639-a454-31b99ebb7e18)
 Call ID: 0f36ac31-ced4-4639-a454-31b99ebb7e18
  Args:
    source: Prince_Frederick_Johann_of_Saxe-Meiningen
    type: :Man
  AssignClass (b45fba44-5189-4c1d-b453-5502b9ac5d8f)
 Call ID: b45fba44-5189-4c1d-b453-5502b9ac5d8f
  Args:
    source: Prince_Frederick_Johann_of_Saxe-Meiningen
    type: :Person
  AssignClass (82c216ed-83e6-4303-968f-9cf518907835)
 Call ID: 82c216ed-83e6-4303-968f-9cf518907835
  Args:
    source: Countess_Adelaide_of_Lippe-Biesterfeld
    type: :Woman
  AssignClass (861c4a94-a7d8-4b1c-8e0f-786608419f56)
 Call ID: 861c4a94-a7d8-4b1c-8e0f-786608419f56
  Args:
    type: :Person
    source: Countess_Adelaide_of_Lippe-Biesterfeld
  AddTriple (c25ac882-6736-4700-843e-feaaeb16ffe1)
 Call ID: c25ac882-6736-4700-843e-feaaeb16ffe1
  Args:
    source: Bernhard_Prince_of_Saxe-Meiningen
    target: Prince_Frederick_Johann_of_Saxe-Meiningen
    relation: :hasFather
  AddTriple (2fff8cc9-9cd8-426d-ac2c-b05727aa1b12)
 Call ID: 2fff8cc9-9cd8-426d-ac2c-b05727aa1b12
  Args:
    target: Countess_Adelaide_of_Lippe-Biesterfeld
    source: Bernhard_Prince_of_Saxe-Meiningen
    relation: :hasMother
  AssignClass (a0fd6bb3-7f1d-455f-8e1d-cd7bc3230a78)
 Call ID: a0fd6bb3-7f1d-455f-8e1d-cd7bc3230a78
  Args:
    source: Georg_II_Duke_of_Saxe-Meiningen
    type: :Man
  AssignClass (4c5b48fe-d27e-4bed-a647-1b90fae1dde3)
 Call ID: 4c5b48fe-d27e-4bed-a647-1b90fae1dde3
  Args:
    source: Georg_II_Duke_of_Saxe-Meiningen
    type: :Person
  AddTriple (d60f000d-e8c9-4b74-8d29-58aa27344fab)
 Call ID: d60f000d-e8c9-4b74-8d29-58aa27344fab
  Args:
    relation: :hasFather
    source: Prince_Frederick_Johann_of_Saxe-Meiningen
    target: Georg_II_Duke_of_Saxe-Meiningen
  AssignClass (013b577c-6323-4be2-a8a6-c73e918a8e65)
 Call ID: 013b577c-6323-4be2-a8a6-c73e918a8e65
  Args:
    type: :Man
    source: Count_Ernst_of_Lippe-Biesterfeld
  AssignClass (ee175a5d-16c4-4a56-a6c1-b843fe3cd3af)
 Call ID: ee175a5d-16c4-4a56-a6c1-b843fe3cd3af
  Args:
    source: Count_Ernst_of_Lippe-Biesterfeld
    type: :Person
  AddTriple (b87441e0-c542-4c5f-9b0f-48446b6e513e)
 Call ID: b87441e0-c542-4c5f-9b0f-48446b6e513e
  Args:
    target: Count_Ernst_of_Lippe-Biesterfeld
    source: Countess_Adelaide_of_Lippe-Biesterfeld
    relation: :hasFather
  AssignClass (8799cc5d-b748-4365-9111-ba82a3722851)
 Call ID: 8799cc5d-b748-4365-9111-ba82a3722851
  Args:
    type: :Man
    source: Prince_Georg
  AssignClass (e052185c-b254-41d1-8ddb-d54185cf5794)
 Call ID: e052185c-b254-41d1-8ddb-d54185cf5794
  Args:
    source: Prince_Georg
    type: :Person
  AddTriple (70000096-9785-4874-84e5-2281aa0e3a28)
 Call ID: 70000096-9785-4874-84e5-2281aa0e3a28
  Args:
    relation: :isBrotherOf
    target: Prince_Georg
    source: Bernhard_Prince_of_Saxe-Meiningen
  AssignClass (f42f63b2-be32-4391-916c-977bf6dc5036)
 Call ID: f42f63b2-be32-4391-916c-977bf6dc5036
  Args:
    type: :Man
    source: Prince_Frederick_Alfred
  AssignClass (7289a790-501f-4228-9297-41919a8cdd53)
 Call ID: 7289a790-501f-4228-9297-41919a8cdd53
  Args:
    type: :Person
    source: Prince_Frederick_Alfred
  AddTriple (26909ae3-4c9c-4b92-ba81-07a280f1ac4d)
 Call ID: 26909ae3-4c9c-4b92-ba81-07a280f1ac4d
  Args:
    source: Prince_Frederick_Alfred
    target: Prince_Georg
    relation: :hasFather
  AssignClass (beecade6-f339-43ac-afef-16d1c6183252)
 Call ID: beecade6-f339-43ac-afef-16d1c6183252
  Args:
    source: Margot_Grössler
    type: :Woman
  AssignClass (c5ce82b9-868f-453d-a851-c0ed55088b65)
 Call ID: c5ce82b9-868f-453d-a851-c0ed55088b65
  Args:
    source: Margot_Grössler
    type: :Person
  AddLiteral (0b052ca9-2678-4e1f-8f6b-15cf3b2fecdf)
 Call ID: 0b052ca9-2678-4e1f-8f6b-15cf3b2fecdf
  Args:
    source: Margot_Grössler
    literal_value: 1911
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (81304a1c-edfc-4943-8c2d-8ec527280a33)
 Call ID: 81304a1c-edfc-4943-8c2d-8ec527280a33
  Args:
    relation: :hasDeathYear
    source: Margot_Grössler
    literal_value: 1998
    literal_type: xsd:integer
  AssignClass (1cd6b6eb-6deb-43f2-ba90-bf5a29da2241)
 Call ID: 1cd6b6eb-6deb-43f2-ba90-bf5a29da2241
  Args:
    source: Friedrich_Grössler
    type: :Man
  AssignClass (fb8848a5-9ae3-45a0-bbe9-4ec460456be6)
 Call ID: fb8848a5-9ae3-45a0-bbe9-4ec460456be6
  Args:
    source: Friedrich_Grössler
    type: :Person
  AssignClass (4ed69c87-6f91-42d7-af3e-504a8f1c3e7b)
 Call ID: 4ed69c87-6f91-42d7-af3e-504a8f1c3e7b
  Args:
    source: Erika_Wägner
    type: :Woman
  AssignClass (f52a37d3-5e52-435e-9850-7cfc4be76251)
 Call ID: f52a37d3-5e52-435e-9850-7cfc4be76251
  Args:
    type: :Person
    source: Erika_Wägner
  AddTriple (35968e43-7e5d-455a-a475-65b4ac599897)
 Call ID: 35968e43-7e5d-455a-a475-65b4ac599897
  Args:
    relation: :hasFather
    source: Margot_Grössler
    target: Friedrich_Grössler
  AddTriple (30f8ba12-1645-46eb-b234-1a0a21bcff41)
 Call ID: 30f8ba12-1645-46eb-b234-1a0a21bcff41
  Args:
    relation: :hasMother
    source: Margot_Grössler
    target: Erika_Wägner
  AssignClass (2a44dbd7-cd98-4642-93b5-9918fcd0bec5)
 Call ID: 2a44dbd7-cd98-4642-93b5-9918fcd0bec5
  Args:
    source: Prince_Frederick_Konrad
    type: :Man
  AssignClass (54df6c5b-0edc-4984-9d9d-62355adcf49a)
 Call ID: 54df6c5b-0edc-4984-9d9d-62355adcf49a
  Args:
    source: Prince_Frederick_Konrad
    type: :Person
  AddTriple (73006197-1bb9-4bb2-a396-48d8d016fea9)
 Call ID: 73006197-1bb9-4bb2-a396-48d8d016fea9
  Args:
    relation: :hasFather
    target: Bernhard_Prince_of_Saxe-Meiningen
    source: Prince_Frederick_Konrad
  AddTriple (0626a4d4-d143-4e47-820f-900202a260b6)
 Call ID: 0626a4d4-d143-4e47-820f-900202a260b6
  Args:
    relation: :hasMother
    source: Prince_Frederick_Konrad
    target: Margot_Grössler
  AssignClass (f1d7af2e-fef7-483e-8790-21b8b376c24a)
 Call ID: f1d7af2e-fef7-483e-8790-21b8b376c24a
  Args:
    type: :Woman
    source: Baroness_Vera_Schäffer_von_Bernstein
  AssignClass (cf5c4b90-e4a1-483f-a2ea-862d5763ecf3)
 Call ID: cf5c4b90-e4a1-483f-a2ea-862d5763ecf3
  Args:
    type: :Person
    source: Baroness_Vera_Schäffer_von_Bernstein
  AddLiteral (1785fc07-4ff0-4b6e-bbcb-5b24e9b63c28)
 Call ID: 1785fc07-4ff0-4b6e-bbcb-5b24e9b63c28
  Args:
    literal_type: xsd:integer
    literal_value: 1914
    source: Baroness_Vera_Schäffer_von_Bernstein
    relation: :hasBirthYear
  AddLiteral (d40c35cb-285e-473f-8d0a-8cf54e248684)
 Call ID: d40c35cb-285e-473f-8d0a-8cf54e248684
  Args:
    relation: :hasDeathYear
    literal_value: 1994
    source: Baroness_Vera_Schäffer_von_Bernstein
    literal_type: xsd:integer
  AddLiteral (4ca7d58d-0707-4285-98b0-d4356ef60bdc)
 Call ID: 4ca7d58d-0707-4285-98b0-d4356ef60bdc
  Args:
    source: Baroness_Vera_Schäffer_von_Bernstein
    literal_value: 1948
    relation: :hasMarriageYear
    literal_type: xsd:integer
  AssignClass (1f5fd41c-c401-4071-84a0-ee2c5d59ea44)
 Call ID: 1f5fd41c-c401-4071-84a0-ee2c5d59ea44
  Args:
    source: Baron_Friedrich_Fritz_Schäffer_von_Bernstein
    type: :Man
  AssignClass (bb5b0dc6-b8e7-4106-82fb-19f330764664)
 Call ID: bb5b0dc6-b8e7-4106-82fb-19f330764664
  Args:
    source: Baron_Friedrich_Fritz_Schäffer_von_Bernstein
    type: :Person
  AddLiteral (7b13aad1-adc7-434b-9444-c57aa872e1f7)
 Call ID: 7b13aad1-adc7-434b-9444-c57aa872e1f7
  Args:
    literal_value: 1868
    source: Baron_Friedrich_Fritz_Schäffer_von_Bernstein
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (befda9fc-8710-42e0-bd28-91179f9f1956)
 Call ID: befda9fc-8710-42e0-bd28-91179f9f1956
  Args:
    relation: :hasDeathYear
    source: Baron_Friedrich_Fritz_Schäffer_von_Bernstein
    literal_value: 1958
    literal_type: xsd:integer
  AssignClass (d93fe217-8564-4e7d-96e0-cdab581a0d70)
 Call ID: d93fe217-8564-4e7d-96e0-cdab581a0d70
  Args:
    type: :Woman
    source: Emma_Carola_Passavant
  AssignClass (43e017d4-b9d9-47a0-800f-34d201f5a8cf)
 Call ID: 43e017d4-b9d9-47a0-800f-34d201f5a8cf
  Args:
    source: Emma_Carola_Passavant
    type: :Person
  AddLiteral (ae9a130d-1652-4bb7-ba1a-306c3890e8c0)
 Call ID: ae9a130d-1652-4bb7-ba1a-306c3890e8c0
  Args:
    relation: :hasBirthYear
    source: Emma_Carola_Passavant
    literal_value: 1884
    literal_type: xsd:integer
  AddLiteral (d0d73e9e-77a9-4952-9e46-99974bd67cb5)
 Call ID: d0d73e9e-77a9-4952-9e46-99974bd67cb5
  Args:
    relation: :hasDeathYear
    literal_value: 1971
    source: Emma_Carola_Passavant
    literal_type: xsd:integer
  AddTriple (e9dfa7b8-1981-491a-8868-73698dd7d39a)
 Call ID: e9dfa7b8-1981-491a-8868-73698dd7d39a
  Args:
    target: Baron_Friedrich_Fritz_Schäffer_von_Bernstein
    source: Baroness_Vera_Schäffer_von_Bernstein
    relation: :hasFather
  AddTriple (0118209b-9e34-4d60-8d63-ca7d19317063)
 Call ID: 0118209b-9e34-4d60-8d63-ca7d19317063
  Args:
    source: Baroness_Vera_Schäffer_von_Bernstein
    target: Emma_Carola_Passavant
    relation: :hasMother
  AssignClass (381b1dd3-5b6e-43c4-8032-d3a127d0a5ec)
 Call ID: 381b1dd3-5b6e-43c4-8032-d3a127d0a5ec
  Args:
    type: :Man
    source: Konrad_Saxe-Meiningen
  AssignClass (1066a7cf-5a8a-46cd-82f9-e9ec7e95940d)
 Call ID: 1066a7cf-5a8a-46cd-82f9-e9ec7e95940d
  Args:
    source: Konrad_Saxe-Meiningen
    type: :Person
  AddTriple (254661c7-ff55-4d80-ac5d-0385acf5ab3e)
 Call ID: 254661c7-ff55-4d80-ac5d-0385acf5ab3e
  Args:
    relation: :hasFather
    target: Bernhard_Prince_of_Saxe-Meiningen
    source: Konrad_Saxe-Meiningen
  AddTriple (e6372bd4-c60e-4088-9d2d-a4fefc9dd60b)
 Call ID: e6372bd4-c60e-4088-9d2d-a4fefc9dd60b
  Args:
    relation: :hasMother
    target: Baroness_Vera_Schäffer_von_Bernstein
    source: Konrad_Saxe-Meiningen
  Finish (f8376ec6-4c0a-46a1-9f9f-01f614cec9c8)
 Call ID: f8376ec6-4c0a-46a1-9f9f-01f614cec9c8
  Args: