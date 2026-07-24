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
Franz Ulrich, 11th Prince Kinsky of Wchinitz and Tettau (German: Franz Ulrich Johannes Clemens Christophorus Antonius Bonaventura Maria Fürst Kinsky von Wchinitz und Tettau; 7 October 1936 – 2 April 2009) was the titular Prince Kinsky of Wchinitz and Tettau as well the head of an ancient House of Kinsky.
Early life

Franz Ulrich was born at Vienna, Federal State of Austria, as the youngest son of Ulrich, 10th Prince Kinsky of Wchinitz and Tettau by his second marriage to Baroness Marie Julia Mathilde von dem Bussche-Haddenhausen (1900–1974), the eldest daughter of Baron Hilmar von dem Bussche-Haddenhausen.
Franz Ulrich became the titular Prince upon the death of his father in 1938.
He was first cousin of Countess Marie Aglaë Kinsky of Wchinitz and Tettau who later became Princess consort of Liechtenstein, and second cousin of Claus von Amsberg, Prince consort of Queen Beatrix of the Netherlands, both descendants of Baron Julius von dem Bussche-Haddenhausen.
In 1942, Franz Ulrich inherited several estates from the Kinsky family, including the Kinsky Palace in Old Town Square in Prague.
Starting in 2003, Franz Ulrich complained against various Czech courts for the return of the assets.
Marriage and family

Franz Ulrich married on 14 April 1965 in Buenos Aires to Roberta Cavanagh (1942–2002), daughter of Roberto Cavanagh and his wife, Anne Rowell.
After Kinsky's death, his son and his widow, Countess Helena Victoria Hutten-Czapska entered a legal dispute over Kinsky's properties.
Later life

The Prince died on 2 April 2009, aged 72.



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
  AssignClass (ece0e991-3ea1-4a24-b30a-a09dc87a5d73)
 Call ID: ece0e991-3ea1-4a24-b30a-a09dc87a5d73
  Args:
    source: Franz_Ulrich_Kinsky
    type: :Man
  AssignClass (5aee0deb-b09d-49e9-8e51-6037d848652f)
 Call ID: 5aee0deb-b09d-49e9-8e51-6037d848652f
  Args:
    type: :Person
    source: Franz_Ulrich_Kinsky
  AssignClass (d63d04c4-cec7-447b-8cbe-4015af8c8644)
 Call ID: d63d04c4-cec7-447b-8cbe-4015af8c8644
  Args:
    source: Ulrich_Kinsky
    type: :Man
  AssignClass (9bfa9661-e1d8-4cf3-80a4-e7eb71bd7c16)
 Call ID: 9bfa9661-e1d8-4cf3-80a4-e7eb71bd7c16
  Args:
    type: :Person
    source: Ulrich_Kinsky
  AssignClass (96bfdbff-5811-4355-a702-bcf813522323)
 Call ID: 96bfdbff-5811-4355-a702-bcf813522323
  Args:
    type: :Woman
    source: Marie_Julia_Mathilde_von_dem_Bussche-Haddenhausen
  AssignClass (df908a39-0bf1-4416-ada4-e134480af34b)
 Call ID: df908a39-0bf1-4416-ada4-e134480af34b
  Args:
    source: Marie_Julia_Mathilde_von_dem_Bussche-Haddenhausen
    type: :Person
  AssignClass (3596260b-a271-45fd-9e00-234b2a209944)
 Call ID: 3596260b-a271-45fd-9e00-234b2a209944
  Args:
    type: :Man
    source: Hilmar_von_dem_Bussche-Haddenhausen
  AssignClass (d4fc8515-8737-493b-9a28-0a1c0e8ff968)
 Call ID: d4fc8515-8737-493b-9a28-0a1c0e8ff968
  Args:
    type: :Person
    source: Hilmar_von_dem_Bussche-Haddenhausen
  AssignClass (908d0cbc-4062-43e2-8d47-cc68df445c8e)
 Call ID: 908d0cbc-4062-43e2-8d47-cc68df445c8e
  Args:
    type: :Woman
    source: Roberta_Cavanagh
  AssignClass (298c5415-5d12-4fa9-a21d-00a64180db65)
 Call ID: 298c5415-5d12-4fa9-a21d-00a64180db65
  Args:
    source: Roberta_Cavanagh
    type: :Person
  AssignClass (116bbbf6-2e79-4c64-abad-6245f4d29205)
 Call ID: 116bbbf6-2e79-4c64-abad-6245f4d29205
  Args:
    type: :Man
    source: Roberto_Cavanagh
  AssignClass (9928cde9-0e7e-47ef-8d19-476f1ff18063)
 Call ID: 9928cde9-0e7e-47ef-8d19-476f1ff18063
  Args:
    type: :Person
    source: Roberto_Cavanagh
  AssignClass (080e8af2-0eb9-4302-9e2c-40fe743bab43)
 Call ID: 080e8af2-0eb9-4302-9e2c-40fe743bab43
  Args:
    type: :Woman
    source: Anne_Rowell
  AssignClass (ed24631f-f597-4368-9be3-5faec3f9ed28)
 Call ID: ed24631f-f597-4368-9be3-5faec3f9ed28
  Args:
    type: :Person
    source: Anne_Rowell
  AssignClass (66aeb77f-ffe0-4a10-babd-439af2002433)
 Call ID: 66aeb77f-ffe0-4a10-babd-439af2002433
  Args:
    type: :Woman
    source: Helena_Victoria_Hutten-Czapska
  AssignClass (9aa6d348-82dd-4f9a-af92-d67e2c95f5ce)
 Call ID: 9aa6d348-82dd-4f9a-af92-d67e2c95f5ce
  Args:
    source: Helena_Victoria_Hutten-Czapska
    type: :Person
  AddLiteral (a39095c6-7d55-4e89-a454-efdfbbe60083)
 Call ID: a39095c6-7d55-4e89-a454-efdfbbe60083
  Args:
    literal_value: 1936
    literal_type: xsd:integer
    source: Franz_Ulrich_Kinsky
    relation: :hasBirthYear
  AddLiteral (13acadc3-ba5b-4ecc-90e1-1f5be371e3d4)
 Call ID: 13acadc3-ba5b-4ecc-90e1-1f5be371e3d4
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: Franz_Ulrich_Kinsky
    literal_value: 2009
  AddTriple (4269b5db-79e9-4a89-b682-816cd9c050ad)
 Call ID: 4269b5db-79e9-4a89-b682-816cd9c050ad
  Args:
    target: Ulrich_Kinsky
    relation: :hasFather
    source: Franz_Ulrich_Kinsky
  AddTriple (12715a3d-0853-4c8b-a13e-aa7cfd511e85)
 Call ID: 12715a3d-0853-4c8b-a13e-aa7cfd511e85
  Args:
    target: Marie_Julia_Mathilde_von_dem_Bussche-Haddenhausen
    source: Franz_Ulrich_Kinsky
    relation: :hasMother
  AddLiteral (f4063ad2-c34e-4df7-a9f3-260b2fd2949e)
 Call ID: f4063ad2-c34e-4df7-a9f3-260b2fd2949e
  Args:
    literal_value: 1900
    relation: :hasBirthYear
    source: Marie_Julia_Mathilde_von_dem_Bussche-Haddenhausen
    literal_type: xsd:integer
  AddLiteral (bdf4df8e-619c-4d86-b6af-e8ceaf8adf99)
 Call ID: bdf4df8e-619c-4d86-b6af-e8ceaf8adf99
  Args:
    literal_value: 1974
    literal_type: xsd:integer
    source: Marie_Julia_Mathilde_von_dem_Bussche-Haddenhausen
    relation: :hasDeathYear
  AddTriple (e97cef26-45f4-4b27-90ba-05806d2c47df)
 Call ID: e97cef26-45f4-4b27-90ba-05806d2c47df
  Args:
    source: Marie_Julia_Mathilde_von_dem_Bussche-Haddenhausen
    relation: :hasFather
    target: Hilmar_von_dem_Bussche-Haddenhausen
  AddTriple (c0592861-7dbe-4756-9550-d1050fd072ce)
 Call ID: c0592861-7dbe-4756-9550-d1050fd072ce
  Args:
    source: Roberta_Cavanagh
    relation: :hasMother
    target: Anne_Rowell
  AddTriple (28f0a3e5-c8d3-424c-b077-1619d60f80fe)
 Call ID: 28f0a3e5-c8d3-424c-b077-1619d60f80fe
  Args:
    source: Roberta_Cavanagh
    relation: :hasFather
    target: Roberto_Cavanagh
  AddLiteral (671f07a4-1046-42c4-b0cd-2de931d82a2d)
 Call ID: 671f07a4-1046-42c4-b0cd-2de931d82a2d
  Args:
    literal_value: 1942
    source: Roberta_Cavanagh
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (12fc084d-9e55-45d4-89a3-f4a569b726aa)
 Call ID: 12fc084d-9e55-45d4-89a3-f4a569b726aa
  Args:
    literal_type: xsd:integer
    source: Roberta_Cavanagh
    relation: :hasDeathYear
    literal_value: 2002
  AddLiteral (aba12a83-6d16-4ba1-8c3f-29c6357282fc)
 Call ID: aba12a83-6d16-4ba1-8c3f-29c6357282fc
  Args:
    literal_value: 1965
    source: Franz_Ulrich_Kinsky
    relation: :hasMarriageYear
    literal_type: xsd:integer
  Finish (b729b48c-4d25-4186-8c3a-4d638a8617b5)
 Call ID: b729b48c-4d25-4186-8c3a-4d638a8617b5
  Args: