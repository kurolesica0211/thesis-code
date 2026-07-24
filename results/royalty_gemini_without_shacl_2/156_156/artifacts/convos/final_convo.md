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
  AssignClass (42635d5f-70e1-4d22-9bba-c83654719d0f)
 Call ID: 42635d5f-70e1-4d22-9bba-c83654719d0f
  Args:
    type: :Man
    source: GeorgDonatus
  AssignClass (03144962-aa17-4725-aa00-3f56942382a7)
 Call ID: 03144962-aa17-4725-aa00-3f56942382a7
  Args:
    type: :Person
    source: GeorgDonatus
  AddLiteral (ac8e1a47-7fd3-4742-bc5f-608e40a10fd8)
 Call ID: ac8e1a47-7fd3-4742-bc5f-608e40a10fd8
  Args:
    relation: :hasBirthYear
    literal_value: 1906
    source: GeorgDonatus
    literal_type: xsd:integer
  AddLiteral (4227ac98-5f4a-4661-a914-4bdf684f43f4)
 Call ID: 4227ac98-5f4a-4661-a914-4bdf684f43f4
  Args:
    relation: :hasDeathYear
    source: GeorgDonatus
    literal_type: xsd:integer
    literal_value: 1937
  AssignClass (fb9b1809-de0b-4ad3-9d3c-3e655147258a)
 Call ID: fb9b1809-de0b-4ad3-9d3c-3e655147258a
  Args:
    type: :Man
    source: ErnestLouis
  AssignClass (f05a37aa-c803-4fec-a016-9333521dd180)
 Call ID: f05a37aa-c803-4fec-a016-9333521dd180
  Args:
    source: ErnestLouis
    type: :Person
  AssignClass (34ff6118-df84-48b8-b2c5-a28fd4904cd8)
 Call ID: 34ff6118-df84-48b8-b2c5-a28fd4904cd8
  Args:
    source: Eleonore
    type: :Woman
  AssignClass (f8158cd7-bd5d-4809-b9c9-cd047f7c0382)
 Call ID: f8158cd7-bd5d-4809-b9c9-cd047f7c0382
  Args:
    type: :Person
    source: Eleonore
  AddTriple (44a32c6c-fe4f-4ff0-90f2-a64384ab850f)
 Call ID: 44a32c6c-fe4f-4ff0-90f2-a64384ab850f
  Args:
    relation: :isFatherOf
    target: GeorgDonatus
    source: ErnestLouis
  AddTriple (32888198-7080-4708-876c-75bdecf9dd58)
 Call ID: 32888198-7080-4708-876c-75bdecf9dd58
  Args:
    source: Eleonore
    target: GeorgDonatus
    relation: :isMotherOf
  AssignClass (cea79de7-0a07-46fc-9fc2-26304d7315cc)
 Call ID: cea79de7-0a07-46fc-9fc2-26304d7315cc
  Args:
    type: :Woman
    source: Cecilie
  AssignClass (2c7d5878-9791-4e11-96d0-6c35e96514d2)
 Call ID: 2c7d5878-9791-4e11-96d0-6c35e96514d2
  Args:
    type: :Person
    source: Cecilie
  AddLiteral (4b051e85-cb9b-454b-b9e2-966e3bc37d0b)
 Call ID: 4b051e85-cb9b-454b-b9e2-966e3bc37d0b
  Args:
    relation: :hasMarriageYear
    source: GeorgDonatus
    literal_type: xsd:integer
    literal_value: 1931
  AddTriple (fe48f7ec-6250-444b-ac2b-ad8915acc149)
 Call ID: fe48f7ec-6250-444b-ac2b-ad8915acc149
  Args:
    source: GeorgDonatus
    target: Cecilie
    relation: :hasRelation
  AssignClass (cd36fdd2-f5bc-411d-8964-83b007322551)
 Call ID: cd36fdd2-f5bc-411d-8964-83b007322551
  Args:
    type: :Man
    source: AndrewOfGreeceAndDenmark
  AssignClass (e0187bc6-abf4-45a5-8ab6-b14a06ece2f5)
 Call ID: e0187bc6-abf4-45a5-8ab6-b14a06ece2f5
  Args:
    source: AndrewOfGreeceAndDenmark
    type: :Person
  AssignClass (3cf050bf-7766-4c9b-884c-dfc6f4a1e784)
 Call ID: 3cf050bf-7766-4c9b-884c-dfc6f4a1e784
  Args:
    source: AliceOfBattenberg
    type: :Woman
  AssignClass (e9f7f692-83e3-456d-89d8-63242475bc3c)
 Call ID: e9f7f692-83e3-456d-89d8-63242475bc3c
  Args:
    type: :Person
    source: AliceOfBattenberg
  AddTriple (6df962bc-528e-4369-890b-c5dbe28233b1)
 Call ID: 6df962bc-528e-4369-890b-c5dbe28233b1
  Args:
    source: AndrewOfGreeceAndDenmark
    relation: :isFatherOf
    target: Cecilie
  AddTriple (e409328f-c647-4a5c-9e77-d6324cf9134c)
 Call ID: e409328f-c647-4a5c-9e77-d6324cf9134c
  Args:
    relation: :isMotherOf
    target: Cecilie
    source: AliceOfBattenberg
  AssignClass (485ef9c5-498b-4acf-be20-eef1f15f7da1)
 Call ID: 485ef9c5-498b-4acf-be20-eef1f15f7da1
  Args:
    type: :Man
    source: LudwigErnstAndreas
  AssignClass (313dd514-73b3-4ebf-875b-b5b2ec0f0dd7)
 Call ID: 313dd514-73b3-4ebf-875b-b5b2ec0f0dd7
  Args:
    type: :Person
    source: LudwigErnstAndreas
  AddLiteral (75e54470-00ba-4629-95f0-8d2a98cf7fbe)
 Call ID: 75e54470-00ba-4629-95f0-8d2a98cf7fbe
  Args:
    literal_value: 1931
    source: LudwigErnstAndreas
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (782441ac-880b-4965-aa7d-acac78618e81)
 Call ID: 782441ac-880b-4965-aa7d-acac78618e81
  Args:
    relation: :hasDeathYear
    literal_value: 1937
    source: LudwigErnstAndreas
    literal_type: xsd:integer
  AddTriple (83fe0183-09de-4628-804e-cf0eb4a7535e)
 Call ID: 83fe0183-09de-4628-804e-cf0eb4a7535e
  Args:
    source: GeorgDonatus
    relation: :isFatherOf
    target: LudwigErnstAndreas
  AddTriple (f39308bc-e7b4-471d-82ce-bb6663249175)
 Call ID: f39308bc-e7b4-471d-82ce-bb6663249175
  Args:
    target: LudwigErnstAndreas
    relation: :isMotherOf
    source: Cecilie
  AssignClass (2eff4031-9524-4976-9f54-9bf8ad2908c3)
 Call ID: 2eff4031-9524-4976-9f54-9bf8ad2908c3
  Args:
    type: :Man
    source: AlexanderGeorgKarlHeinrich
  AssignClass (7be84c1b-0b26-437d-9817-567077b147e3)
 Call ID: 7be84c1b-0b26-437d-9817-567077b147e3
  Args:
    type: :Person
    source: AlexanderGeorgKarlHeinrich
  AddLiteral (102e1760-f2a6-43e9-b185-3b57a09d26be)
 Call ID: 102e1760-f2a6-43e9-b185-3b57a09d26be
  Args:
    literal_value: 1933
    source: AlexanderGeorgKarlHeinrich
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (dd98e7b5-af8b-4b1d-ac50-0d7790a2b19d)
 Call ID: dd98e7b5-af8b-4b1d-ac50-0d7790a2b19d
  Args:
    source: AlexanderGeorgKarlHeinrich
    literal_type: xsd:integer
    literal_value: 1937
    relation: :hasDeathYear
  AddTriple (ccb4a049-c053-4794-8c58-b3c1a4469bd5)
 Call ID: ccb4a049-c053-4794-8c58-b3c1a4469bd5
  Args:
    source: GeorgDonatus
    relation: :isFatherOf
    target: AlexanderGeorgKarlHeinrich
  AddTriple (66f2e595-47db-4ca4-9d99-6fc8e1c1afd0)
 Call ID: 66f2e595-47db-4ca4-9d99-6fc8e1c1afd0
  Args:
    source: Cecilie
    target: AlexanderGeorgKarlHeinrich
    relation: :isMotherOf
  AssignClass (e03b3ff4-7572-46a4-9d6e-b19ab210bc09)
 Call ID: e03b3ff4-7572-46a4-9d6e-b19ab210bc09
  Args:
    source: JohannaMarinaEleonore
    type: :Woman
  AssignClass (0d2bd950-b42a-4634-924e-31974710eba6)
 Call ID: 0d2bd950-b42a-4634-924e-31974710eba6
  Args:
    source: JohannaMarinaEleonore
    type: :Person
  AddLiteral (62c041a9-bcbf-4f01-a584-b106fbab11e0)
 Call ID: 62c041a9-bcbf-4f01-a584-b106fbab11e0
  Args:
    literal_value: 1936
    source: JohannaMarinaEleonore
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (cf7f065f-c6ff-40fa-ac83-95816a66a382)
 Call ID: cf7f065f-c6ff-40fa-ac83-95816a66a382
  Args:
    relation: :hasDeathYear
    source: JohannaMarinaEleonore
    literal_type: xsd:integer
    literal_value: 1939
  AddTriple (6996d423-8b4c-4555-9d05-48fb00df7a52)
 Call ID: 6996d423-8b4c-4555-9d05-48fb00df7a52
  Args:
    source: GeorgDonatus
    target: JohannaMarinaEleonore
    relation: :isFatherOf
  AddTriple (b7582db0-c1db-4306-83b5-b8e4a7237ac2)
 Call ID: b7582db0-c1db-4306-83b5-b8e4a7237ac2
  Args:
    source: Cecilie
    relation: :isMotherOf
    target: JohannaMarinaEleonore
  AssignClass (2d64aa98-149b-4d1c-93b0-ba92d024b859)
 Call ID: 2d64aa98-149b-4d1c-93b0-ba92d024b859
  Args:
    source: Louis
    type: :Man
  AssignClass (49f2ea9b-2986-4c36-baec-9222346cedc9)
 Call ID: 49f2ea9b-2986-4c36-baec-9222346cedc9
  Args:
    source: Louis
    type: :Person
  AddTriple (bc83a566-29c9-4dde-bd4e-27f2b7f00d7f)
 Call ID: bc83a566-29c9-4dde-bd4e-27f2b7f00d7f
  Args:
    target: GeorgDonatus
    relation: :isBrotherOf
    source: Louis
  AddLiteral (c58e3dcf-04b1-49c6-9dbc-79e01ea6a221)
 Call ID: c58e3dcf-04b1-49c6-9dbc-79e01ea6a221
  Args:
    relation: :hasDeathYear
    literal_value: 1968
    source: Louis
    literal_type: xsd:integer
  Finish (ffc33d06-573a-465e-972a-41ccc971dc9f)
 Call ID: ffc33d06-573a-465e-972a-41ccc971dc9f
  Args: