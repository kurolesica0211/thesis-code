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
Prince Heinrich of Prussia (German: Albert Wilhelm Heinrich; 14 August 1862 – 20 April 1929) was a younger brother of German Emperor and King of Prussia Wilhelm II and a Prince of Prussia.
Biography

Born in Berlin, Prince Heinrich was the third child and second son of eight children born to Crown Prince Frederick William (later Emperor Frederick III), and Victoria, Princess Royal (later Empress Victoria and in widowhood Empress Frederick), eldest daughter of the British Queen Victoria.
Henry was three years younger than his brother, the future Emperor William II (born 27 January 1859).
He was born on the same day as King Frederick William I "Soldier-King" of Prussia.
Early commands

As a Prussian prince, Henry quickly achieved command.
Squadron commands

From 1897, Prince Henry commanded several naval task forces; these included an improvised squadron that took part with the East Asia Squadron in consolidating and securing the German hold on the region of Kiaochow and the port of Tsingtao in 1898.
The prince's success was more of the diplomatic than the military variety; he became the first European potentate ever to be received at the Chinese imperial court.
From 1906 to 1909, Henry was commander of the High Seas Fleet.
I

At the beginning of World War I, Prince Henry was named as Commander-in-Chief of the Baltic Fleet.
After the end of hostilities with Russia, his mission was ended, and Prince Henry simply left active duty.
With the war's end and the dissolution of the monarchy in Germany, Prince Henry left the navy.
Family

On 24 May 1888, Henry married Princess Irene of Hesse and by Rhine, his first cousin.
His dying father, German Emperor Frederick III and his mother Empress Victoria were in attendance.
The marriage produced three children:


Their sons Waldemar and Heinrich were both hemophiliacs, a disease which they inherited through Irene from the maternal grandmother of both of their parents, Queen Victoria, who was a carrier.
Personality and private life

Henry received one of the first pilot's licenses in Germany, and was judged a spirited and excellent seaman.
A yachting enthusiast, Prince Henry became one of the first members of the Yacht Club of Kiel, established by a group of naval officers in 1887, and quickly became the club's patron.
Henry was interested in motor cars as well and supposedly invented a windshield wiper and, according to other sources, the car horn.
In his honor, the Prinz-Heinrich-Fahrt (Prince Heinrich Tour) was established in 1908, like the earlier Kaiserpreis a precursor to the German Grand Prix.
Henry and his brother William gave patronage to the Kaiserlicher Automobilclub (Imperial Automobile Club).
From 1911 to 1914 the British car makers Vauxhall Motors produced a model, the C-10, which was called the "Vauxhall Prince Henry" in his honour after initially being built for participation in the 1911 race.
After the German Revolution, Henry lived with his family in Hemmelmark near Eckernförde, in Schleswig-Holstein.
He popularized the Prince Henry cap, which is still worn, especially by older sailors.
In 1899, Henry received an honorary doctorate (Doctor of Engineering honoris causa) from the Technische Hochschule in Charlottenburg (now Technische Universität Berlin) .
Prince Henry died of throat cancer on 20 April 1929 in Hemmelmark.



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
  AssignClass (77c180e6-bb49-486e-8c54-faec2c85e61e)
 Call ID: 77c180e6-bb49-486e-8c54-faec2c85e61e
  Args:
    source: :Prince_Heinrich_of_Prussia
    type: :Man
  AssignClass (642d4d1c-1d42-49b5-97d7-7f58b903cf5e)
 Call ID: 642d4d1c-1d42-49b5-97d7-7f58b903cf5e
  Args:
    source: :Prince_Heinrich_of_Prussia
    type: :Person
  AddLiteral (5bab39f0-8a54-42a7-b0e8-d7019f56e0b8)
 Call ID: 5bab39f0-8a54-42a7-b0e8-d7019f56e0b8
  Args:
    literal_type: xsd:string
    relation: :alsoKnownAs
    literal_value: Albert Wilhelm Heinrich
    source: :Prince_Heinrich_of_Prussia
  AddLiteral (1aec6c94-b6db-4b11-a942-82895bbb5bc7)
 Call ID: 1aec6c94-b6db-4b11-a942-82895bbb5bc7
  Args:
    relation: :hasBirthYear
    source: :Prince_Heinrich_of_Prussia
    literal_value: 1862
    literal_type: xsd:integer
  AddLiteral (24cbce34-c70d-4de1-9499-ac8f09b81fab)
 Call ID: 24cbce34-c70d-4de1-9499-ac8f09b81fab
  Args:
    literal_type: xsd:integer
    source: :Prince_Heinrich_of_Prussia
    literal_value: 1929
    relation: :hasDeathYear
  AssignClass (6f4ff5bc-9db8-4866-bfdd-c3a7192d5715)
 Call ID: 6f4ff5bc-9db8-4866-bfdd-c3a7192d5715
  Args:
    type: :Man
    source: :Wilhelm_II
  AssignClass (6a5a1b52-874a-4c01-b236-2fddad7ee65f)
 Call ID: 6a5a1b52-874a-4c01-b236-2fddad7ee65f
  Args:
    type: :Person
    source: :Wilhelm_II
  AddTriple (6686c70b-ee9e-4f6a-b387-f76e69a7f10a)
 Call ID: 6686c70b-ee9e-4f6a-b387-f76e69a7f10a
  Args:
    target: :Wilhelm_II
    source: :Prince_Heinrich_of_Prussia
    relation: :isBrotherOf
  AssignClass (f79f3978-27d3-4ea6-8627-26f43d5ae10e)
 Call ID: f79f3978-27d3-4ea6-8627-26f43d5ae10e
  Args:
    source: :Frederick_III
    type: :Man
  AssignClass (0bb225b5-aec2-49f2-b2a2-0c2faee8d895)
 Call ID: 0bb225b5-aec2-49f2-b2a2-0c2faee8d895
  Args:
    source: :Frederick_III
    type: :Ancestor
  AssignClass (d5654462-2d95-45e2-af6c-268958847b8a)
 Call ID: d5654462-2d95-45e2-af6c-268958847b8a
  Args:
    source: :Frederick_III
    type: :Person
  AssignClass (4c31df79-ad75-46fe-a69e-5d351f5cc484)
 Call ID: 4c31df79-ad75-46fe-a69e-5d351f5cc484
  Args:
    source: :Empress_Victoria
    type: :Woman
  AssignClass (ba08539d-665f-424c-8633-10403aa6b86c)
 Call ID: ba08539d-665f-424c-8633-10403aa6b86c
  Args:
    source: :Empress_Victoria
    type: :Ancestor
  AssignClass (e5d34824-b24e-4889-96d9-006951944de7)
 Call ID: e5d34824-b24e-4889-96d9-006951944de7
  Args:
    type: :Person
    source: :Empress_Victoria
  AddTriple (2635aa34-f9f7-489d-8b47-db9896870274)
 Call ID: 2635aa34-f9f7-489d-8b47-db9896870274
  Args:
    source: :Prince_Heinrich_of_Prussia
    target: :Frederick_III
    relation: :hasFather
  AddTriple (0e268f1f-29e8-48a0-bb74-705fb115e4c5)
 Call ID: 0e268f1f-29e8-48a0-bb74-705fb115e4c5
  Args:
    relation: :hasMother
    source: :Prince_Heinrich_of_Prussia
    target: :Empress_Victoria
  AssignClass (0e25f006-70f1-4508-8768-3cf01962fc3b)
 Call ID: 0e25f006-70f1-4508-8768-3cf01962fc3b
  Args:
    source: :Queen_Victoria
    type: :Woman
  AssignClass (27ad9f65-aaff-48dc-83a6-9cd19543aa85)
 Call ID: 27ad9f65-aaff-48dc-83a6-9cd19543aa85
  Args:
    type: :Ancestor
    source: :Queen_Victoria
  AssignClass (b646b0ee-b114-4260-a387-916bd10ebec8)
 Call ID: b646b0ee-b114-4260-a387-916bd10ebec8
  Args:
    type: :Person
    source: :Queen_Victoria
  AddTriple (2cd4046a-fe40-4ae1-afcf-d416a717ceb3)
 Call ID: 2cd4046a-fe40-4ae1-afcf-d416a717ceb3
  Args:
    relation: :hasMother
    source: :Empress_Victoria
    target: :Queen_Victoria
  AssignClass (6c809470-a3be-4817-a423-9e099b228d8d)
 Call ID: 6c809470-a3be-4817-a423-9e099b228d8d
  Args:
    type: :Woman
    source: :Princess_Irene
  AssignClass (841538c3-81ce-45aa-88f4-cf9483456a85)
 Call ID: 841538c3-81ce-45aa-88f4-cf9483456a85
  Args:
    source: :Princess_Irene
    type: :Person
  AddTriple (6ba2f483-f279-47ba-a2a2-909497963108)
 Call ID: 6ba2f483-f279-47ba-a2a2-909497963108
  Args:
    relation: :hasRelation
    source: :Prince_Heinrich_of_Prussia
    target: :Princess_Irene
  AddLiteral (6d6958c5-4ff4-4cb0-a444-bb9f8117a80c)
 Call ID: 6d6958c5-4ff4-4cb0-a444-bb9f8117a80c
  Args:
    relation: :hasMarriageYear
    literal_value: 1888
    source: :Prince_Heinrich_of_Prussia
    literal_type: xsd:integer
  AssignClass (dad50e9a-c9fe-4b10-98b9-130f6abd5ee3)
 Call ID: dad50e9a-c9fe-4b10-98b9-130f6abd5ee3
  Args:
    type: :Man
    source: :Waldemar
  AssignClass (9945c731-2c34-4397-b80a-fa0d0bd9b5a5)
 Call ID: 9945c731-2c34-4397-b80a-fa0d0bd9b5a5
  Args:
    type: :Person
    source: :Waldemar
  AssignClass (d0f75281-7119-408d-99a7-5a5e28e8225f)
 Call ID: d0f75281-7119-408d-99a7-5a5e28e8225f
  Args:
    source: :Heinrich_son
    type: :Man
  AssignClass (e40cc80e-1978-4789-8c22-ffe41dd1f79b)
 Call ID: e40cc80e-1978-4789-8c22-ffe41dd1f79b
  Args:
    type: :Person
    source: :Heinrich_son
  AddTriple (95cfbc64-2a1f-4bcf-a5e8-9f19709501bb)
 Call ID: 95cfbc64-2a1f-4bcf-a5e8-9f19709501bb
  Args:
    target: :Waldemar
    source: :Prince_Heinrich_of_Prussia
    relation: :hasSon
  AddTriple (a843271b-df70-4b1a-9759-df6a843b0c82)
 Call ID: a843271b-df70-4b1a-9759-df6a843b0c82
  Args:
    relation: :hasSon
    source: :Prince_Heinrich_of_Prussia
    target: :Heinrich_son
  AddTriple (36530293-9f38-4dac-b7a9-559065238272)
 Call ID: 36530293-9f38-4dac-b7a9-559065238272
  Args:
    relation: :hasMother
    source: :Waldemar
    target: :Princess_Irene
  AddTriple (9a4bc71a-42f2-4feb-8af7-1e6dac017e74)
 Call ID: 9a4bc71a-42f2-4feb-8af7-1e6dac017e74
  Args:
    relation: :hasMother
    source: :Heinrich_son
    target: :Princess_Irene
  Finish (4753c7d9-0050-400f-85cb-bc4f3e478583)
 Call ID: 4753c7d9-0050-400f-85cb-bc4f3e478583
  Args: