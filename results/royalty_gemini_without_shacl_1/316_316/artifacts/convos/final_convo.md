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
Prince Adalbert Ferdinand Berengar Viktor of Prussia (14 July 1884 – 22 September 1948) was the third son of Wilhelm II, German Emperor, and Augusta Victoria of Schleswig-Holstein.
Early life

Prince Adalbert was born on 14 July 1884 as the third son of the then Prince Wilhelm of Prussia and his first wife, Princess Augusta Victoria of Schleswig-Holstein.
He was born in the Marmorpalais of Potsdam in the Province of Brandenburg, where his parents resided until his father acceded to the throne as Emperor Wilhelm II in 1888.
He spent his childhood with his siblings at the New Palace, also in Potsdam, and his school days with his brothers at the Prinzenhaus in Plön in his mother’s ancestral Schleswig-Holstein.
His bride was Princess Adelheid "Adi" of Saxe-Meiningen (16 August 1891 – 25 April 1971), daughter of Prince Frederick and Countess Adelaide of Lippe-Biesterfeld.
They married on 3 August 1914 in Wilhelmshaven, Germany, and had three children, five grandchildren, six great-grandchildren and two great-great-grandchildren:


Kaiserliche Marine

Regimental Commissions

Source:


Chivalric Orders

Source:


Military Decorations

Death

Adalbert died in La Tour de Peilz, Switzerland, aged 64.



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
  AssignClass (5e4ef9dd-a62f-4f30-9739-0d6f0dddecff)
 Call ID: 5e4ef9dd-a62f-4f30-9739-0d6f0dddecff
  Args:
    type: :Man
    source: Adalbert_of_Prussia
  AssignClass (6989e16b-49b1-4683-8da1-2e1fb2f80d10)
 Call ID: 6989e16b-49b1-4683-8da1-2e1fb2f80d10
  Args:
    type: :Person
    source: Adalbert_of_Prussia
  AssignClass (2c6bdf34-70a5-46e6-bc76-4b2aaddbef92)
 Call ID: 2c6bdf34-70a5-46e6-bc76-4b2aaddbef92
  Args:
    source: Wilhelm_II
    type: :Man
  AssignClass (416ad06b-b3e9-4a4e-97ed-14fcfea66542)
 Call ID: 416ad06b-b3e9-4a4e-97ed-14fcfea66542
  Args:
    source: Wilhelm_II
    type: :Person
  AssignClass (aec4b0c7-6574-4ca0-816c-c42ab1cf3adf)
 Call ID: aec4b0c7-6574-4ca0-816c-c42ab1cf3adf
  Args:
    source: Augusta_Victoria_of_Schleswig-Holstein
    type: :Woman
  AssignClass (5f5508df-4988-488a-abec-f594e66f50aa)
 Call ID: 5f5508df-4988-488a-abec-f594e66f50aa
  Args:
    type: :Person
    source: Augusta_Victoria_of_Schleswig-Holstein
  AssignClass (4b425803-9fbc-4c87-8b1f-8912702e3714)
 Call ID: 4b425803-9fbc-4c87-8b1f-8912702e3714
  Args:
    source: Adelheid_of_Saxe-Meiningen
    type: :Woman
  AssignClass (737177ff-2ad8-4a25-a14d-aa4be24de3ef)
 Call ID: 737177ff-2ad8-4a25-a14d-aa4be24de3ef
  Args:
    source: Adelheid_of_Saxe-Meiningen
    type: :Person
  AssignClass (e1ceec94-273e-4375-a411-ffca6c24bb4c)
 Call ID: e1ceec94-273e-4375-a411-ffca6c24bb4c
  Args:
    source: Frederick_of_Saxe-Meiningen
    type: :Man
  AssignClass (82f1dfeb-5b9e-4ed0-b2c6-03aa9a605314)
 Call ID: 82f1dfeb-5b9e-4ed0-b2c6-03aa9a605314
  Args:
    source: Frederick_of_Saxe-Meiningen
    type: :Person
  AssignClass (d74b0dbb-e0a5-4a71-ad1e-2f2bbd24b4e0)
 Call ID: d74b0dbb-e0a5-4a71-ad1e-2f2bbd24b4e0
  Args:
    source: Adelaide_of_Lippe-Biesterfeld
    type: :Woman
  AssignClass (64e4b387-4fa9-4815-aac5-9707c8092a55)
 Call ID: 64e4b387-4fa9-4815-aac5-9707c8092a55
  Args:
    source: Adelaide_of_Lippe-Biesterfeld
    type: :Person
  AddLiteral (174e883d-2f94-4934-b002-4baeed4fd411)
 Call ID: 174e883d-2f94-4934-b002-4baeed4fd411
  Args:
    source: Adalbert_of_Prussia
    relation: :hasBirthYear
    literal_value: 1884
    literal_type: xsd:integer
  AddLiteral (f1676e2b-7309-45cc-b02d-e862dfe3b978)
 Call ID: f1676e2b-7309-45cc-b02d-e862dfe3b978
  Args:
    source: Adalbert_of_Prussia
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 1948
  AddTriple (54be5cff-07af-4959-b3ea-2f6c55d512d8)
 Call ID: 54be5cff-07af-4959-b3ea-2f6c55d512d8
  Args:
    target: Wilhelm_II
    relation: :hasFather
    source: Adalbert_of_Prussia
  AddTriple (f8f5e322-b5ef-4afe-a931-7fde4116bd9e)
 Call ID: f8f5e322-b5ef-4afe-a931-7fde4116bd9e
  Args:
    target: Augusta_Victoria_of_Schleswig-Holstein
    relation: :hasMother
    source: Adalbert_of_Prussia
  AddLiteral (770294f5-8952-4a1d-9439-88fa874f5139)
 Call ID: 770294f5-8952-4a1d-9439-88fa874f5139
  Args:
    source: Adelheid_of_Saxe-Meiningen
    relation: :hasBirthYear
    literal_value: 1891
    literal_type: xsd:integer
  AddLiteral (6fffe551-5006-4a7f-868e-5c60a77e78e7)
 Call ID: 6fffe551-5006-4a7f-868e-5c60a77e78e7
  Args:
    relation: :hasDeathYear
    literal_value: 1971
    literal_type: xsd:integer
    source: Adelheid_of_Saxe-Meiningen
  AddTriple (ab271dfe-8f25-433a-be35-33751f72d67d)
 Call ID: ab271dfe-8f25-433a-be35-33751f72d67d
  Args:
    target: Frederick_of_Saxe-Meiningen
    source: Adelheid_of_Saxe-Meiningen
    relation: :hasFather
  AddTriple (b0cfc777-8f3b-42ff-920b-3f3596fb278b)
 Call ID: b0cfc777-8f3b-42ff-920b-3f3596fb278b
  Args:
    target: Adelaide_of_Lippe-Biesterfeld
    relation: :hasMother
    source: Adelheid_of_Saxe-Meiningen
  AddLiteral (49b3d087-a2c7-4fbd-bea5-2cfbea74dde6)
 Call ID: 49b3d087-a2c7-4fbd-bea5-2cfbea74dde6
  Args:
    source: Adalbert_of_Prussia
    relation: :hasMarriageYear
    literal_value: 1914
    literal_type: xsd:integer
  AddTriple (6b6aa9dc-12f8-438b-a6ec-6caaa5b4d830)
 Call ID: 6b6aa9dc-12f8-438b-a6ec-6caaa5b4d830
  Args:
    source: Adalbert_of_Prussia
    relation: :hasRelation
    target: Adelheid_of_Saxe-Meiningen
  AddLiteral (c6bf8285-8064-4ba4-a55f-d25590d63ac2)
 Call ID: c6bf8285-8064-4ba4-a55f-d25590d63ac2
  Args:
    source: Adelheid_of_Saxe-Meiningen
    relation: :knownAs
    literal_value: Adi
    literal_type: xsd:string
  Finish (abc004ac-ed3b-4aeb-8dc5-6bdc4d19336c)
 Call ID: abc004ac-ed3b-4aeb-8dc5-6bdc4d19336c
  Args: