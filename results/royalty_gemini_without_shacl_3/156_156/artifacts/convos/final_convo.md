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
  AssignClass (b0939e23-1f6b-4c47-9646-432672b8e364)
 Call ID: b0939e23-1f6b-4c47-9646-432672b8e364
  Args:
    source: GeorgDonatus
    type: :Man
  AssignClass (450b6104-316a-490b-94db-ada68e6d0e58)
 Call ID: 450b6104-316a-490b-94db-ada68e6d0e58
  Args:
    source: GeorgDonatus
    type: :Person
  AssignClass (66857bb4-ef7c-4dca-bf5b-0a8ee072666d)
 Call ID: 66857bb4-ef7c-4dca-bf5b-0a8ee072666d
  Args:
    type: :Man
    source: ErnestLouis
  AssignClass (3bb31e42-02ef-4e6a-abeb-6925c78b3259)
 Call ID: 3bb31e42-02ef-4e6a-abeb-6925c78b3259
  Args:
    type: :Person
    source: ErnestLouis
  AssignClass (6e2047f1-df8e-40f2-93c2-8dac8a81174a)
 Call ID: 6e2047f1-df8e-40f2-93c2-8dac8a81174a
  Args:
    source: EleonoreOfSolmsHohensolmsLich
    type: :Woman
  AssignClass (0c3140d9-0127-4b4c-871d-469b6605a228)
 Call ID: 0c3140d9-0127-4b4c-871d-469b6605a228
  Args:
    type: :Person
    source: EleonoreOfSolmsHohensolmsLich
  AddLiteral (738a5b5f-9639-432d-a800-70edf8791348)
 Call ID: 738a5b5f-9639-432d-a800-70edf8791348
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1906
    source: GeorgDonatus
  AddLiteral (bee66d1c-1aec-48ed-9ba6-ec32646b0584)
 Call ID: bee66d1c-1aec-48ed-9ba6-ec32646b0584
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 1937
    source: GeorgDonatus
  AddTriple (3144e570-289e-4c11-b71f-3c16568da874)
 Call ID: 3144e570-289e-4c11-b71f-3c16568da874
  Args:
    relation: :hasFather
    target: ErnestLouis
    source: GeorgDonatus
  AddTriple (f34b4a50-ebf5-41c3-95c5-69c8549d99b5)
 Call ID: f34b4a50-ebf5-41c3-95c5-69c8549d99b5
  Args:
    source: GeorgDonatus
    target: EleonoreOfSolmsHohensolmsLich
    relation: :hasMother
  AssignClass (3adb2796-6d22-4c56-ac67-86f54a939e42)
 Call ID: 3adb2796-6d22-4c56-ac67-86f54a939e42
  Args:
    type: :Woman
    source: CecilieOfGreeceAndDenmark
  AssignClass (5d7b6230-e984-4a4e-bdbd-6f0b94945edc)
 Call ID: 5d7b6230-e984-4a4e-bdbd-6f0b94945edc
  Args:
    source: CecilieOfGreeceAndDenmark
    type: :Person
  AddTriple (9ae9a4c4-c0a9-48df-b7a1-57edf3e58a3f)
 Call ID: 9ae9a4c4-c0a9-48df-b7a1-57edf3e58a3f
  Args:
    source: GeorgDonatus
    target: CecilieOfGreeceAndDenmark
    relation: :hasRelation
  AddLiteral (597f8492-ce3a-41e9-b110-1535171c80b1)
 Call ID: 597f8492-ce3a-41e9-b110-1535171c80b1
  Args:
    literal_value: 1931
    source: GeorgDonatus
    relation: :hasMarriageYear
    literal_type: xsd:integer
  AssignClass (31dbbbd5-70fb-4c60-b1cd-0434f39b90c4)
 Call ID: 31dbbbd5-70fb-4c60-b1cd-0434f39b90c4
  Args:
    type: :Man
    source: PrinceLudwigErnstAndreas
  AssignClass (350408c1-e77e-4064-9c68-5cd790aced49)
 Call ID: 350408c1-e77e-4064-9c68-5cd790aced49
  Args:
    type: :Person
    source: PrinceLudwigErnstAndreas
  AddTriple (db426489-8a1a-4820-bda6-627815a9d858)
 Call ID: db426489-8a1a-4820-bda6-627815a9d858
  Args:
    relation: :isSonOf
    source: PrinceLudwigErnstAndreas
    target: GeorgDonatus
  AddTriple (16dc43da-f183-4c08-ae05-4d6786afff5c)
 Call ID: 16dc43da-f183-4c08-ae05-4d6786afff5c
  Args:
    relation: :isSonOf
    target: CecilieOfGreeceAndDenmark
    source: PrinceLudwigErnstAndreas
  AssignClass (b8f5f9b0-6ff6-465a-b4c6-8688d8a3689b)
 Call ID: b8f5f9b0-6ff6-465a-b4c6-8688d8a3689b
  Args:
    source: PrinceAlexanderGeorgKarlHeinrich
    type: :Man
  AssignClass (13c5e42d-ba8c-45a0-bbb0-016dbd84730b)
 Call ID: 13c5e42d-ba8c-45a0-bbb0-016dbd84730b
  Args:
    source: PrinceAlexanderGeorgKarlHeinrich
    type: :Person
  AddTriple (23692a1e-deda-48ab-84de-2a32f1d00f43)
 Call ID: 23692a1e-deda-48ab-84de-2a32f1d00f43
  Args:
    relation: :isSonOf
    source: PrinceAlexanderGeorgKarlHeinrich
    target: GeorgDonatus
  AddTriple (73686cbd-a8ec-46fb-9648-2bb1ee322cb8)
 Call ID: 73686cbd-a8ec-46fb-9648-2bb1ee322cb8
  Args:
    relation: :isSonOf
    target: CecilieOfGreeceAndDenmark
    source: PrinceAlexanderGeorgKarlHeinrich
  AssignClass (a13649c2-9ce4-4951-a31a-074147c21944)
 Call ID: a13649c2-9ce4-4951-a31a-074147c21944
  Args:
    type: :Woman
    source: PrincessJohannaMarinaEleonore
  AssignClass (a7d80811-2876-484a-b7a4-23496ea127eb)
 Call ID: a7d80811-2876-484a-b7a4-23496ea127eb
  Args:
    type: :Person
    source: PrincessJohannaMarinaEleonore
  AddTriple (cba708e9-de51-4ec7-81d9-f4afcc808e4e)
 Call ID: cba708e9-de51-4ec7-81d9-f4afcc808e4e
  Args:
    target: GeorgDonatus
    source: PrincessJohannaMarinaEleonore
    relation: :isDaughterOf
  AddTriple (5a360ea6-55ba-4eca-853b-df306f38058c)
 Call ID: 5a360ea6-55ba-4eca-853b-df306f38058c
  Args:
    relation: :isDaughterOf
    source: PrincessJohannaMarinaEleonore
    target: CecilieOfGreeceAndDenmark
  AssignClass (3da5ee5e-39ee-42bc-aad2-a64b3f3434c8)
 Call ID: 3da5ee5e-39ee-42bc-aad2-a64b3f3434c8
  Args:
    source: PrinceAndrewOfGreeceAndDenmark
    type: :Man
  AssignClass (18483bcc-6190-4812-982f-ee43ba129e0f)
 Call ID: 18483bcc-6190-4812-982f-ee43ba129e0f
  Args:
    type: :Person
    source: PrinceAndrewOfGreeceAndDenmark
  AssignClass (3451c65c-fa10-495a-a34f-8401675683e2)
 Call ID: 3451c65c-fa10-495a-a34f-8401675683e2
  Args:
    type: :Woman
    source: PrincessAliceOfBattenberg
  AssignClass (e0de41e2-b121-4e7f-90bf-007e7b278e0d)
 Call ID: e0de41e2-b121-4e7f-90bf-007e7b278e0d
  Args:
    source: PrincessAliceOfBattenberg
    type: :Person
  AddTriple (71b39718-dcf7-4d17-8c15-7887a5188859)
 Call ID: 71b39718-dcf7-4d17-8c15-7887a5188859
  Args:
    relation: :hasFather
    source: CecilieOfGreeceAndDenmark
    target: PrinceAndrewOfGreeceAndDenmark
  AddTriple (9e96d4dc-9fbe-4d7e-b06f-d282aefb052f)
 Call ID: 9e96d4dc-9fbe-4d7e-b06f-d282aefb052f
  Args:
    relation: :hasMother
    source: CecilieOfGreeceAndDenmark
    target: PrincessAliceOfBattenberg
  AssignClass (f2ab748c-ab67-4cc8-ab4e-b37f389ed6fc)
 Call ID: f2ab748c-ab67-4cc8-ab4e-b37f389ed6fc
  Args:
    type: :Man
    source: PrinceLouis
  AssignClass (c5692ce7-9238-4225-b433-4216111c2433)
 Call ID: c5692ce7-9238-4225-b433-4216111c2433
  Args:
    source: PrinceLouis
    type: :Person
  AddTriple (4ed62e07-28fd-40cf-a349-dfbdabed1c85)
 Call ID: 4ed62e07-28fd-40cf-a349-dfbdabed1c85
  Args:
    target: GeorgDonatus
    source: PrinceLouis
    relation: :isBrotherOf
  Finish (94c7fd50-da93-4301-8a81-7ae271e4589d)
 Call ID: 94c7fd50-da93-4301-8a81-7ae271e4589d
  Args: