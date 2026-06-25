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
Georg Donatus, Hereditary Grand Duke of Hesse (Georg Donatus Wilhelm Nikolaus Eduard Heinrich Karl, 8 November 1906 – 16 November 1937), was the first child of Ernest Louis, Grand Duke of Hesse, and his second wife, Princess Eleonore of Solms-Hohensolms-Lich.
Marriage and children

On 2 February 1931, in Darmstadt, Georg Donatus, a great-grandson of Queen Victoria, married his first cousin once removed, Princess Cecilie of Greece and Denmark, daughter of Prince Andrew of Greece and Denmark and Princess Alice of Battenberg, sister of Prince Philip, Duke of Edinburgh, and great-great-granddaughter of Queen Victoria and Prince Albert.
The couple had four children:


• Prince Ludwig Ernst Andreas of Hesse and by Rhine (25 October 1931 – 16 November 1937), killed in the air accident.
• Prince Alexander Georg Karl Heinrich of Hesse and by Rhine (14 April 1933 – 16 November 1937), killed in the air accident.
• Princess Johanna Marina Eleonore of Hesse and by Rhine (20 September 1936 – 14 June 1939), died from meningitis.
On 1 May 1937, Georg Donatus and Cecilie both joined the Nazi Party.
Death

In October 1937, Georg Donatus's father, Grand Duke Ernest Louis of Hesse, died.
A few weeks after the funeral, his younger brother, Prince Louis, was due to marry the Hon.
On 16 November 1937, Georg Donatus, Cecilie, their two young sons, Georg Donatus's mother, Grand Duchess Eleonore, the children's nurse, a family friend, a pilot, and two crewmen took off in a Sabena Junkers Ju 52 aeroplane from Darmstadt, bound for the United Kingdom, where Louis's marriage ceremony was to take place.
Cecilie was in an advanced state of pregnancy with their fourth child at the time of the crash.
The remains of the newborn baby were found in the wreckage, indicating that Cecilie had gone into labour during the flight.
The funeral and burial of Georg Donatus and his family took place at the Rosenhöhe, Darmstadt, Hesse, a few days later.
Among those attending were Prince Philip, Prince Christoph of Hesse, Gottfried, Prince of Hohenlohe-Langenburg, Prince Philipp of Hesse, Berthold, Margrave of Baden, Prince August Wilhelm of Prussia, and Lord Louis Mountbatten.
A photograph of the funeral procession, showing Prince Louis as chief mourner, depicts crowds saluting the mourners with the Hitler salute.
Georg Donatus and Cecilie's 14‐month‐old daughter, Johanna, was the only member of the immediate family who was not on board the aircraft.
Johanna died of meningitis in 1939.
With the death of the childless Louis in 1968, the male line of the Hesse and by Rhine became extinct.
Titles

Georg Donatus never acceded to the grand‐ducal throne, as it had been abolished at the end of the First World War.



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
  AssignClass (c1d3728b-64af-48aa-a55f-bcf6880d48f7)
 Call ID: c1d3728b-64af-48aa-a55f-bcf6880d48f7
  Args:
    source: Georg_Donatus_Hereditary_Grand_Duke_of_Hesse
    type: :Man
  AssignClass (461aa224-3c61-45cc-8ab8-28ac0b330ad3)
 Call ID: 461aa224-3c61-45cc-8ab8-28ac0b330ad3
  Args:
    source: Ernest_Louis_Grand_Duke_of_Hesse
    type: :Man
  AssignClass (ee79bdc9-6110-40ba-aac9-10a6ba72770c)
 Call ID: ee79bdc9-6110-40ba-aac9-10a6ba72770c
  Args:
    source: Princess_Eleonore_of_Solms-Hohensolms-Lich
    type: :Woman
  AssignClass (ac93f4cc-5f37-4f4a-bcab-6a672fd42fee)
 Call ID: ac93f4cc-5f37-4f4a-bcab-6a672fd42fee
  Args:
    source: Princess_Cecilie_of_Greece_and_Denmark
    type: :Woman
  AssignClass (0da6c4f1-da4c-49b3-b4bd-d643d87f8a13)
 Call ID: 0da6c4f1-da4c-49b3-b4bd-d643d87f8a13
  Args:
    source: Prince_Andrew_of_Greece_and_Denmark
    type: :Man
  AssignClass (b70bbfa6-2a7c-4ced-9bdd-0d82bf1e87fb)
 Call ID: b70bbfa6-2a7c-4ced-9bdd-0d82bf1e87fb
  Args:
    source: Princess_Alice_of_Battenberg
    type: :Woman
  AssignClass (f1f29c9e-0120-4905-afe3-35ef9719c5ce)
 Call ID: f1f29c9e-0120-4905-afe3-35ef9719c5ce
  Args:
    source: Prince_Ludwig_Ernst_Andreas_of_Hesse_and_by_Rhine
    type: :Man
  AssignClass (fe0dbf8f-bfb7-4e7b-9ad0-3f2163587982)
 Call ID: fe0dbf8f-bfb7-4e7b-9ad0-3f2163587982
  Args:
    source: Prince_Alexander_Georg_Karl_Heinrich_of_Hesse_and_by_Rhine
    type: :Man
  AssignClass (f46c4844-27c3-4cf0-8cb2-1edec53fafcf)
 Call ID: f46c4844-27c3-4cf0-8cb2-1edec53fafcf
  Args:
    source: Princess_Johanna_Marina_Eleonore_of_Hesse_and_by_Rhine
    type: :Woman
  AssignClass (e82d294e-3144-4210-9211-a1e3b51219ea)
 Call ID: e82d294e-3144-4210-9211-a1e3b51219ea
  Args:
    source: Prince_Louis_of_Hesse_and_by_Rhine
    type: :Man
  AddLiteral (26f4068c-8779-4503-83ec-6ab20d0be309)
 Call ID: 26f4068c-8779-4503-83ec-6ab20d0be309
  Args:
    relation: :hasBirthYear
    source: Georg_Donatus_Hereditary_Grand_Duke_of_Hesse
    literal_type: xsd:integer
    literal_value: 1906
  AddLiteral (0f4672f7-10ea-488c-b671-655b356b472c)
 Call ID: 0f4672f7-10ea-488c-b671-655b356b472c
  Args:
    literal_type: xsd:integer
    literal_value: 1937
    source: Georg_Donatus_Hereditary_Grand_Duke_of_Hesse
    relation: :hasDeathYear
  AddLiteral (776eb890-82e8-4efa-b6ae-5b983b02e178)
 Call ID: 776eb890-82e8-4efa-b6ae-5b983b02e178
  Args:
    literal_type: xsd:integer
    literal_value: 1931
    source: Georg_Donatus_Hereditary_Grand_Duke_of_Hesse
    relation: :hasMarriageYear
  AddTriple (9b3f9e49-8f75-4ab4-aa2e-26d8303457b2)
 Call ID: 9b3f9e49-8f75-4ab4-aa2e-26d8303457b2
  Args:
    source: Georg_Donatus_Hereditary_Grand_Duke_of_Hesse
    relation: :hasFather
    target: Ernest_Louis_Grand_Duke_of_Hesse
  AddTriple (48f5486d-1f75-4c5a-9be8-863eb754f9d2)
 Call ID: 48f5486d-1f75-4c5a-9be8-863eb754f9d2
  Args:
    target: Princess_Eleonore_of_Solms-Hohensolms-Lich
    source: Georg_Donatus_Hereditary_Grand_Duke_of_Hesse
    relation: :hasMother
  AddTriple (cbf4b0d4-d41d-4bcd-8337-b865bfd6d5b3)
 Call ID: cbf4b0d4-d41d-4bcd-8337-b865bfd6d5b3
  Args:
    source: Princess_Cecilie_of_Greece_and_Denmark
    relation: :hasFather
    target: Prince_Andrew_of_Greece_and_Denmark
  AddTriple (8886f581-0c31-4caf-9d3e-b3536644d29f)
 Call ID: 8886f581-0c31-4caf-9d3e-b3536644d29f
  Args:
    source: Princess_Cecilie_of_Greece_and_Denmark
    relation: :hasMother
    target: Princess_Alice_of_Battenberg
  AddTriple (061b2c63-d944-4165-964a-62ef974aa9c7)
 Call ID: 061b2c63-d944-4165-964a-62ef974aa9c7
  Args:
    target: Prince_Ludwig_Ernst_Andreas_of_Hesse_and_by_Rhine
    source: Georg_Donatus_Hereditary_Grand_Duke_of_Hesse
    relation: :hasChild
  AddTriple (20a449e8-32af-4146-8cf1-33eed5e48a76)
 Call ID: 20a449e8-32af-4146-8cf1-33eed5e48a76
  Args:
    relation: :hasChild
    source: Georg_Donatus_Hereditary_Grand_Duke_of_Hesse
    target: Prince_Alexander_Georg_Karl_Heinrich_of_Hesse_and_by_Rhine
  AddTriple (0d6b8913-5705-44bd-9c3e-f5608b7a77ad)
 Call ID: 0d6b8913-5705-44bd-9c3e-f5608b7a77ad
  Args:
    target: Princess_Johanna_Marina_Eleonore_of_Hesse_and_by_Rhine
    relation: :hasChild
    source: Georg_Donatus_Hereditary_Grand_Duke_of_Hesse
  AddTriple (cd2e173f-79fb-47a6-8af0-ebc6dbb0a293)
 Call ID: cd2e173f-79fb-47a6-8af0-ebc6dbb0a293
  Args:
    source: Princess_Cecilie_of_Greece_and_Denmark
    relation: :hasChild
    target: Prince_Ludwig_Ernst_Andreas_of_Hesse_and_by_Rhine
  AddTriple (71e63e8d-9eeb-4810-9754-c85a448a0687)
 Call ID: 71e63e8d-9eeb-4810-9754-c85a448a0687
  Args:
    source: Princess_Cecilie_of_Greece_and_Denmark
    relation: :hasChild
    target: Prince_Alexander_Georg_Karl_Heinrich_of_Hesse_and_by_Rhine
  AddTriple (23468bfe-fe04-4677-9804-1e6b5969988c)
 Call ID: 23468bfe-fe04-4677-9804-1e6b5969988c
  Args:
    target: Princess_Johanna_Marina_Eleonore_of_Hesse_and_by_Rhine
    relation: :hasChild
    source: Princess_Cecilie_of_Greece_and_Denmark
  AddTriple (cd8b060e-bc90-46c8-84c4-20ae1658706c)
 Call ID: cd8b060e-bc90-46c8-84c4-20ae1658706c
  Args:
    relation: :isBrotherOf
    source: Prince_Louis_of_Hesse_and_by_Rhine
    target: Georg_Donatus_Hereditary_Grand_Duke_of_Hesse
  AddTriple (d9af888e-8ecc-41d3-b98c-aacf87f0649c)
 Call ID: d9af888e-8ecc-41d3-b98c-aacf87f0649c
  Args:
    source: Prince_Louis_of_Hesse_and_by_Rhine
    relation: :hasFather
    target: Ernest_Louis_Grand_Duke_of_Hesse
  AddTriple (93fbedcd-d106-453b-8e19-96c6b7bb93d9)
 Call ID: 93fbedcd-d106-453b-8e19-96c6b7bb93d9
  Args:
    relation: :hasMother
    source: Prince_Louis_of_Hesse_and_by_Rhine
    target: Princess_Eleonore_of_Solms-Hohensolms-Lich
  Finish (65cc990d-3822-4109-94e4-c0b909611409)
 Call ID: 65cc990d-3822-4109-94e4-c0b909611409
  Args: