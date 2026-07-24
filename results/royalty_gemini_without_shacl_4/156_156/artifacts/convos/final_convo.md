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
  AssignClass (39634313-8672-4cfb-952a-9f2b504c0c85)
 Call ID: 39634313-8672-4cfb-952a-9f2b504c0c85
  Args:
    source: Georg Donatus
    type: :Man
  AssignClass (0c504e8e-5740-420d-9f46-ecf98e69f184)
 Call ID: 0c504e8e-5740-420d-9f46-ecf98e69f184
  Args:
    type: :Man
    source: Ernest Louis
  AssignClass (e897b83e-fb5b-4a33-abda-0cdc1ce74fba)
 Call ID: e897b83e-fb5b-4a33-abda-0cdc1ce74fba
  Args:
    type: :Woman
    source: Eleonore of Solms-Hohensolms-Lich
  AddTriple (1c64d78d-ad51-4ce2-a255-b759e48e7902)
 Call ID: 1c64d78d-ad51-4ce2-a255-b759e48e7902
  Args:
    target: Ernest Louis
    source: Georg Donatus
    relation: :hasFather
  AddTriple (86f1e08f-fe1e-4b43-ad4d-ed6249df8ae9)
 Call ID: 86f1e08f-fe1e-4b43-ad4d-ed6249df8ae9
  Args:
    relation: :hasMother
    source: Georg Donatus
    target: Eleonore of Solms-Hohensolms-Lich
  AddLiteral (77d273ba-6e8d-4138-8f1d-43d07b8bfc9e)
 Call ID: 77d273ba-6e8d-4138-8f1d-43d07b8bfc9e
  Args:
    literal_type: xsd:integer
    literal_value: 1906
    source: Georg Donatus
    relation: :hasBirthYear
  AddLiteral (9d828ecd-2707-498e-9ef8-88866167c5f5)
 Call ID: 9d828ecd-2707-498e-9ef8-88866167c5f5
  Args:
    relation: :hasDeathYear
    source: Georg Donatus
    literal_value: 1937
    literal_type: xsd:integer
  AssignClass (69e43b96-df37-4ecd-ae27-39118f867e8a)
 Call ID: 69e43b96-df37-4ecd-ae27-39118f867e8a
  Args:
    source: Cecilie of Greece and Denmark
    type: :Woman
  AddLiteral (86944bee-5d6c-44b2-aec2-334724660dd5)
 Call ID: 86944bee-5d6c-44b2-aec2-334724660dd5
  Args:
    source: Georg Donatus
    relation: :hasMarriageYear
    literal_value: 1931
    literal_type: xsd:integer
  AddTriple (efa00505-20e6-4f96-9a92-16cb725f8013)
 Call ID: efa00505-20e6-4f96-9a92-16cb725f8013
  Args:
    target: Cecilie of Greece and Denmark
    relation: :hasRelation
    source: Georg Donatus
  AssignClass (c24643da-8ca2-4d89-90c0-9d86fc3ab009)
 Call ID: c24643da-8ca2-4d89-90c0-9d86fc3ab009
  Args:
    type: :Man
    source: Andrew of Greece and Denmark
  AssignClass (8424ef8f-b2c8-4187-8be4-62dc497ee7cb)
 Call ID: 8424ef8f-b2c8-4187-8be4-62dc497ee7cb
  Args:
    source: Alice of Battenberg
    type: :Woman
  AddTriple (c3bfff4e-d5c3-450f-bb1b-aeccb65a2a75)
 Call ID: c3bfff4e-d5c3-450f-bb1b-aeccb65a2a75
  Args:
    relation: :hasFather
    source: Cecilie of Greece and Denmark
    target: Andrew of Greece and Denmark
  AddTriple (515dc187-861d-47c0-829c-b349092871f4)
 Call ID: 515dc187-861d-47c0-829c-b349092871f4
  Args:
    relation: :hasMother
    source: Cecilie of Greece and Denmark
    target: Alice of Battenberg
  AssignClass (09b3643d-4250-4a64-b05b-e4706384d7b5)
 Call ID: 09b3643d-4250-4a64-b05b-e4706384d7b5
  Args:
    type: :Man
    source: Ludwig Ernst Andreas of Hesse and by Rhine
  AssignClass (7f1ffccb-f23a-4621-a87b-75aa7715bfb9)
 Call ID: 7f1ffccb-f23a-4621-a87b-75aa7715bfb9
  Args:
    source: Alexander Georg Karl Heinrich of Hesse and by Rhine
    type: :Man
  AssignClass (7db64d82-b35c-4ae7-a1db-f1ed75ff3e58)
 Call ID: 7db64d82-b35c-4ae7-a1db-f1ed75ff3e58
  Args:
    source: Johanna Marina Eleonore of Hesse and by Rhine
    type: :Woman
  AddTriple (5e8e59e8-cb83-4062-a36a-e4f982735981)
 Call ID: 5e8e59e8-cb83-4062-a36a-e4f982735981
  Args:
    target: Ludwig Ernst Andreas of Hesse and by Rhine
    relation: :hasChild
    source: Georg Donatus
  AddTriple (967ac21c-44c3-42a0-8038-47727de0b820)
 Call ID: 967ac21c-44c3-42a0-8038-47727de0b820
  Args:
    relation: :hasChild
    source: Georg Donatus
    target: Alexander Georg Karl Heinrich of Hesse and by Rhine
  AddTriple (e929643b-461a-4103-bc32-2dd5c02627a7)
 Call ID: e929643b-461a-4103-bc32-2dd5c02627a7
  Args:
    source: Georg Donatus
    relation: :hasChild
    target: Johanna Marina Eleonore of Hesse and by Rhine
  AddTriple (d6733f9e-ff96-43b0-8e44-c0705fef05c6)
 Call ID: d6733f9e-ff96-43b0-8e44-c0705fef05c6
  Args:
    source: Cecilie of Greece and Denmark
    relation: :hasChild
    target: Ludwig Ernst Andreas of Hesse and by Rhine
  AddTriple (8982dfce-5c87-4bb4-9ed8-570bc2954df8)
 Call ID: 8982dfce-5c87-4bb4-9ed8-570bc2954df8
  Args:
    target: Alexander Georg Karl Heinrich of Hesse and by Rhine
    source: Cecilie of Greece and Denmark
    relation: :hasChild
  AddTriple (c56e7a68-a56b-4a44-9094-17d4c0eeacdc)
 Call ID: c56e7a68-a56b-4a44-9094-17d4c0eeacdc
  Args:
    target: Johanna Marina Eleonore of Hesse and by Rhine
    source: Cecilie of Greece and Denmark
    relation: :hasChild
  AddLiteral (1a486a6a-550a-4941-8b7e-8d16663c07f9)
 Call ID: 1a486a6a-550a-4941-8b7e-8d16663c07f9
  Args:
    literal_value: 1937
    relation: :hasDeathYear
    source: Ludwig Ernst Andreas of Hesse and by Rhine
    literal_type: xsd:integer
  AddLiteral (6012cbef-bae5-4917-b5b9-cb9c6a851645)
 Call ID: 6012cbef-bae5-4917-b5b9-cb9c6a851645
  Args:
    literal_type: xsd:integer
    literal_value: 1937
    source: Alexander Georg Karl Heinrich of Hesse and by Rhine
    relation: :hasDeathYear
  AddLiteral (ba647f7d-2be9-4192-bb09-aaeabec29e24)
 Call ID: ba647f7d-2be9-4192-bb09-aaeabec29e24
  Args:
    literal_value: 1939
    relation: :hasDeathYear
    source: Johanna Marina Eleonore of Hesse and by Rhine
    literal_type: xsd:integer
  AssignClass (aa757643-35b9-45d4-b685-2c54349c307b)
 Call ID: aa757643-35b9-45d4-b685-2c54349c307b
  Args:
    type: :Man
    source: Louis
  AddTriple (b3d3c86c-b383-4623-945f-0badb6dd4bcd)
 Call ID: b3d3c86c-b383-4623-945f-0badb6dd4bcd
  Args:
    relation: :hasFather
    source: Louis
    target: Ernest Louis
  AddTriple (c3c9c21e-c48a-4b1e-943f-b6ab3efa7b48)
 Call ID: c3c9c21e-c48a-4b1e-943f-b6ab3efa7b48
  Args:
    target: Eleonore of Solms-Hohensolms-Lich
    source: Louis
    relation: :hasMother
  AddTriple (38544c3c-f796-4d7e-8617-bbd57d74d5c1)
 Call ID: 38544c3c-f796-4d7e-8617-bbd57d74d5c1
  Args:
    relation: :isSiblingOf
    source: Georg Donatus
    target: Louis
  Finish (422c3362-5b10-4297-9772-a43ddff02f0a)
 Call ID: 422c3362-5b10-4297-9772-a43ddff02f0a
  Args: