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
Princess Isabelle Françoise Hélène Marie d'Orléans (27 November 1900, Le Nouvion-en-Thiérache, France – 12 February 1983, Neuilly-sur-Seine, France) was a member of the House of Orléans and, by marriage, a member of the ducal Harcourt family and of the princely House of Murat.
She was one of the four children of Prince Jean, Duke of Guise (1874–1940), who would become the Orleanist pretender to the French throne in 1926, and Princess Isabelle of Orléans.
Marriages

In 1923 the tradition of Orléans princesses marrying only other royalty (since the alleged 1681 wedding of La Grande Mademoiselle) was dispensed with, as nearly all of her relatives attended Isabelle's wedding at Amélie of Orléans château in Le Chesnay on 12 September to Count Bruno d'Harcourt (1899–1930), son of Count Eugène d'Harcourt and Armande de Pierre de Bernis.
An automobile racer, Harcourt was killed during practice for the Moroccan Grand Prix, leaving his wife with four children:


As a widow, Isabelle remarried the Bonapartist Prince Pierre Murat (1900–1948) in 1934, at Jouy-en-Josas, "upon renunciation of the rank and prerogatives appertaining to princesses of the House of France".
Prince Murat was a  great-grandson of Prince Lucien Murat.
In 1940, as World War II began and when her father died, Isabelle again took refuge at the family estate, Larache, in Morocco, where she shared quarters with her mother, and her elder sister the widowed Princess Françoise of Greece, along with her brother Henri, Count of Paris and the latter's son, Prince Michel d'Orléans.Isabella often visited her parents in Morocco, Belgium and France, especially during World 
War II.
In 1953, her younger sister,Princess Françoise, widow of Prince Christopher of Greece, died in her Paris home after a long period of depression.
Princess Isabella herself died in 1983 and is buried in the Montparnasse Cemetery in Paris.



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
  AssignClass (18950b05-6363-486b-a17c-ee62226726c7)
 Call ID: 18950b05-6363-486b-a17c-ee62226726c7
  Args:
    source: :Isabelle_dOrleans
    type: :Woman
  AssignClass (7281c477-ca89-4583-8099-a816fdc0e14c)
 Call ID: 7281c477-ca89-4583-8099-a816fdc0e14c
  Args:
    type: :Person
    source: :Isabelle_dOrleans
  AddLiteral (fb247fdb-bc56-4c62-acfd-48a3ba1c282d)
 Call ID: fb247fdb-bc56-4c62-acfd-48a3ba1c282d
  Args:
    literal_value: 1900
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: :Isabelle_dOrleans
  AddLiteral (d7f46c8a-eb6e-4430-aff4-3a3375490870)
 Call ID: d7f46c8a-eb6e-4430-aff4-3a3375490870
  Args:
    literal_value: 1983
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: :Isabelle_dOrleans
  AssignClass (7cae9d08-364c-40eb-b51c-cbf0a172e2c5)
 Call ID: 7cae9d08-364c-40eb-b51c-cbf0a172e2c5
  Args:
    source: :Jean_Duke_of_Guise
    type: :Man
  AssignClass (1d853969-bc2c-475f-9cc6-5f173652361b)
 Call ID: 1d853969-bc2c-475f-9cc6-5f173652361b
  Args:
    type: :Ancestor
    source: :Jean_Duke_of_Guise
  AddLiteral (e3fee435-cdd1-4a9d-85da-178879303ee8)
 Call ID: e3fee435-cdd1-4a9d-85da-178879303ee8
  Args:
    literal_value: 1874
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: :Jean_Duke_of_Guise
  AddLiteral (5b3ea0b5-218d-4def-8b9a-02a7c0af73dd)
 Call ID: 5b3ea0b5-218d-4def-8b9a-02a7c0af73dd
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: :Jean_Duke_of_Guise
    literal_value: 1940
  AssignClass (1ea73d3b-6337-4dcf-b85b-a8713bf48d68)
 Call ID: 1ea73d3b-6337-4dcf-b85b-a8713bf48d68
  Args:
    type: :Woman
    source: :Isabelle_of_Orleans
  AssignClass (8b6beb9f-81f2-48a8-919a-5ce4b6e80d80)
 Call ID: 8b6beb9f-81f2-48a8-919a-5ce4b6e80d80
  Args:
    source: :Isabelle_of_Orleans
    type: :Ancestor
  AddTriple (9be2c3dc-30d6-435e-9009-3218daf7fee3)
 Call ID: 9be2c3dc-30d6-435e-9009-3218daf7fee3
  Args:
    source: :Isabelle_dOrleans
    target: :Jean_Duke_of_Guise
    relation: :hasFather
  AddTriple (3c551610-6027-40c8-ac8a-77c430eaa4ca)
 Call ID: 3c551610-6027-40c8-ac8a-77c430eaa4ca
  Args:
    relation: :hasMother
    source: :Isabelle_dOrleans
    target: :Isabelle_of_Orleans
  AssignClass (16b5815f-a4ef-48a7-84d3-3ef0e1e755a1)
 Call ID: 16b5815f-a4ef-48a7-84d3-3ef0e1e755a1
  Args:
    type: :Man
    source: :Bruno_dHarcourt
  AssignClass (7a6c47c2-0405-4b6e-86e0-c3116280aefc)
 Call ID: 7a6c47c2-0405-4b6e-86e0-c3116280aefc
  Args:
    type: :Person
    source: :Bruno_dHarcourt
  AddLiteral (9526eb8e-a7d6-45af-b35f-34d5c929a1e1)
 Call ID: 9526eb8e-a7d6-45af-b35f-34d5c929a1e1
  Args:
    source: :Isabelle_dOrleans
    relation: :hasMarriageYear
    literal_type: xsd:integer
    literal_value: 1923
  AddTriple (ed3d2d2d-4ce0-4920-a9ee-8ead0212763d)
 Call ID: ed3d2d2d-4ce0-4920-a9ee-8ead0212763d
  Args:
    relation: :hasRelation
    target: :Bruno_dHarcourt
    source: :Isabelle_dOrleans
  AssignClass (95ef2902-f57e-4760-8961-363e6f2c9f66)
 Call ID: 95ef2902-f57e-4760-8961-363e6f2c9f66
  Args:
    source: :Pierre_Murat
    type: :Man
  AssignClass (3d19fd53-3b9c-4f8d-b9ce-fa3f81e69045)
 Call ID: 3d19fd53-3b9c-4f8d-b9ce-fa3f81e69045
  Args:
    source: :Pierre_Murat
    type: :Person
  AddLiteral (9c5772aa-957f-4f1a-bb22-0c8e22e9500d)
 Call ID: 9c5772aa-957f-4f1a-bb22-0c8e22e9500d
  Args:
    literal_value: 1934
    source: :Isabelle_dOrleans
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AddTriple (2cce2a26-3d23-4a99-b704-0aa58fe3b747)
 Call ID: 2cce2a26-3d23-4a99-b704-0aa58fe3b747
  Args:
    source: :Isabelle_dOrleans
    target: :Pierre_Murat
    relation: :hasRelation
  AssignClass (d09c8bfb-8440-4a58-a931-8556401b5257)
 Call ID: d09c8bfb-8440-4a58-a931-8556401b5257
  Args:
    source: :Francoise_of_Greece
    type: :Woman
  AssignClass (5430e3bf-5670-4805-85dc-9eeacb27d2a3)
 Call ID: 5430e3bf-5670-4805-85dc-9eeacb27d2a3
  Args:
    source: :Francoise_of_Greece
    type: :Person
  AddTriple (9d73835f-6519-444b-8c53-4be4325a78f9)
 Call ID: 9d73835f-6519-444b-8c53-4be4325a78f9
  Args:
    source: :Isabelle_dOrleans
    target: :Francoise_of_Greece
    relation: :hasSister
  AssignClass (4538f436-f164-4e3a-b83b-631097a49430)
 Call ID: 4538f436-f164-4e3a-b83b-631097a49430
  Args:
    source: :Henri_Count_of_Paris
    type: :Man
  AssignClass (1a445104-0bb4-45fc-af32-5edc274c5b33)
 Call ID: 1a445104-0bb4-45fc-af32-5edc274c5b33
  Args:
    source: :Henri_Count_of_Paris
    type: :Person
  AddTriple (c869c702-8619-4160-84e7-dc5c1de63bc3)
 Call ID: c869c702-8619-4160-84e7-dc5c1de63bc3
  Args:
    target: :Henri_Count_of_Paris
    source: :Isabelle_dOrleans
    relation: :hasBrother
  AssignClass (6fdc90dd-3c19-41d8-af2c-aaf93db5445c)
 Call ID: 6fdc90dd-3c19-41d8-af2c-aaf93db5445c
  Args:
    source: :Michel_dOrleans
    type: :Man
  AssignClass (0c0fb549-d3ab-41a5-9483-3ab9dd5f7860)
 Call ID: 0c0fb549-d3ab-41a5-9483-3ab9dd5f7860
  Args:
    type: :Person
    source: :Michel_dOrleans
  AddTriple (1b5828df-0b02-4722-9219-0d29fbb19267)
 Call ID: 1b5828df-0b02-4722-9219-0d29fbb19267
  Args:
    target: :Henri_Count_of_Paris
    source: :Michel_dOrleans
    relation: :hasFather
  Finish (d1cf02cb-1579-47fa-aa55-134c33e577e5)
 Call ID: d1cf02cb-1579-47fa-aa55-134c33e577e5
  Args: