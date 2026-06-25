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
Louis Ferdinand, Prince of Prussia (German: Louis Ferdinand Victor Eduard Adalbert Michael Hubertus Prinz von Preußen; 9 November 1907 –  26 September 1994) was a grandson of Kaiser Wilhelm II and member of the  House of Hohenzollern, which occupied the Prussian and German thrones until the abolition of those monarchies in 1918.
Biography

Louis Ferdinand was born in Potsdam as the third in succession to the throne of the German Empire, after his father, German Crown Prince William and elder brother Prince Wilhelm of Prussia.
When Louis Ferdinand's older brother Prince Wilhelm renounced his succession rights to marry a member of the untitled nobility in 1933 (he was later to be killed in action in France in 1940 while fighting in the German army), Louis Ferdinand replaced him as second in the line of succession to the defunct German and Prussian thrones after the former Crown Prince.
Louis Ferdinand was educated in Berlin and deviated from his family's tradition by not pursuing a military career.
Louis Ferdinand dissociated himself from the Nazis after this.
He married his second cousin, Grand Duchess Kira Kirillovna of Russia, in 1938 in first a Russian Orthodox ceremony in Potsdam and then a Lutheran ceremony in Huis Doorn, Netherlands.
Kira was the second daughter of Grand Duke Kyril Vladimirovich and Princess Victoria Melita of Saxe-Coburg and Gotha.
His third son and heir apparent, Prince Louis Ferdinand, died in 1977 during military maneuvers, and thus his one-year-old grandson Georg Friedrich, Prince of Prussia (son of Prince Louis Ferdinand) became the new heir apparent to the defunct Prussian and German Imperial throne.
Upon Louis Ferdinand's death in 1994, Georg Friedrich became the pretender to the defunct thrones and head of the Hohenzollern family.
The prince was a popular figure.
In 1968 Der Spiegel reported that in a survey of their readers by Quick magazine about who would be the most honorable person to become President of the Federal Republic of Germany, Louis Ferdinand, the only one of twelve candidates who was not a politician, won with 39.8% before Carlo Schmid and Ludwig Erhard.
In a similar survey by the tabloid Bild, readers chose Louis Ferdinand by 55.6%.
In an interview with Quick, the prince indicated that he might accept the presidency but would not relinquish his claim to the imperial or Prussian crowns.
Instead of complying with his last wish after his death, the king had been laid to rest in the Garrison Church, Potsdam next to his unloved father Frederick William I of Prussia in 1786.
Both coffins were relocated during World War II and ended up in the prince's castle in what became West Germany.
The prince had Frederick William I's coffin taken to the crypt of the Church of Peace, Potsdam because the Garrison Church had been destroyed in 1945.
In interviews with C.L. Sulzberger for the book The Fall of Eagles, Louis Ferdinand expressed a deep sense of admiration for the informal bicycle monarchy and crowned republic style favored and used by the Dutch, Belgian, and Scandinavian royal families.
Praising how vehicles carrying the King or Queen would stop and wait at traffic lights, Louis Ferdinand stated that if the House of Hohenzollern were ever restored to the German throne during his lifetime, this same informality was a quality he fully intended to emulate.
Prince Ferdinand of Hohenzollern, a member of the senior Swabian branch of the Hohenzollern dynasty, Hohenzollern-Sigmaringen, is his godson.



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
  AssignClass (2e21ec96-0672-40d0-9d53-bb1c1a7928c4)
 Call ID: 2e21ec96-0672-40d0-9d53-bb1c1a7928c4
  Args:
    source: LouisFerdinand
    type: :Man
  AssignClass (91de7e7b-b0f9-4286-826b-222201e08f4b)
 Call ID: 91de7e7b-b0f9-4286-826b-222201e08f4b
  Args:
    source: LouisFerdinand
    type: :Person
  AddLiteral (29bd4a60-df38-4230-9cf2-d2ab47313a9c)
 Call ID: 29bd4a60-df38-4230-9cf2-d2ab47313a9c
  Args:
    relation: :hasBirthYear
    source: LouisFerdinand
    literal_value: 1907
    literal_type: xsd:integer
  AddLiteral (191dcd8a-a8f9-40be-9cc1-40fd9132e26b)
 Call ID: 191dcd8a-a8f9-40be-9cc1-40fd9132e26b
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: LouisFerdinand
    literal_value: 1994
  AssignClass (a58f28fc-081b-4b37-a208-7f99dcd850ea)
 Call ID: a58f28fc-081b-4b37-a208-7f99dcd850ea
  Args:
    type: :Man
    source: WilhelmII
  AssignClass (40bc37f5-1aa1-4eb3-b092-0104fcaf3a38)
 Call ID: 40bc37f5-1aa1-4eb3-b092-0104fcaf3a38
  Args:
    source: WilhelmII
    type: :Person
  AddTriple (19d33397-ce5c-4110-8b35-ced1ae871c66)
 Call ID: 19d33397-ce5c-4110-8b35-ced1ae871c66
  Args:
    source: LouisFerdinand
    relation: :hasAncestor
    target: WilhelmII
  AssignClass (a47ec757-4e57-4608-a0f2-2ce0dd480d34)
 Call ID: a47ec757-4e57-4608-a0f2-2ce0dd480d34
  Args:
    source: WilliamCrownPrince
    type: :Man
  AssignClass (df96c2f6-4eef-4769-9c8b-3dd8c34b18ed)
 Call ID: df96c2f6-4eef-4769-9c8b-3dd8c34b18ed
  Args:
    type: :Person
    source: WilliamCrownPrince
  AddTriple (9b373acc-b6e7-42aa-bb90-98a06604119d)
 Call ID: 9b373acc-b6e7-42aa-bb90-98a06604119d
  Args:
    relation: :hasFather
    target: WilliamCrownPrince
    source: LouisFerdinand
  AssignClass (1f2d2ab9-05fa-46e8-969a-b81feafe4501)
 Call ID: 1f2d2ab9-05fa-46e8-969a-b81feafe4501
  Args:
    source: WilhelmOfPrussia
    type: :Man
  AssignClass (75165a30-7735-40ad-b69c-778a144ba976)
 Call ID: 75165a30-7735-40ad-b69c-778a144ba976
  Args:
    type: :Person
    source: WilhelmOfPrussia
  AddTriple (110605c0-2656-4f5a-bc9e-58c17317e8cb)
 Call ID: 110605c0-2656-4f5a-bc9e-58c17317e8cb
  Args:
    source: LouisFerdinand
    relation: :hasBrother
    target: WilhelmOfPrussia
  AssignClass (439be427-8e76-44a0-979b-ac641c2f0761)
 Call ID: 439be427-8e76-44a0-979b-ac641c2f0761
  Args:
    type: :Woman
    source: KiraKirillovna
  AssignClass (edf3a6c7-ac12-4199-b28e-f44b441bbab3)
 Call ID: edf3a6c7-ac12-4199-b28e-f44b441bbab3
  Args:
    source: KiraKirillovna
    type: :Person
  AddTriple (def861f1-ce8f-44ed-bf8b-d38897254f0a)
 Call ID: def861f1-ce8f-44ed-bf8b-d38897254f0a
  Args:
    source: LouisFerdinand
    relation: :hasRelation
    target: KiraKirillovna
  AddLiteral (0244ee20-abf4-4fac-890c-162ee101e07a)
 Call ID: 0244ee20-abf4-4fac-890c-162ee101e07a
  Args:
    source: LouisFerdinand
    literal_value: 1938
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AssignClass (793071d2-8513-4ac0-9dfc-b39315b461f8)
 Call ID: 793071d2-8513-4ac0-9dfc-b39315b461f8
  Args:
    source: KyrilVladimirovich
    type: :Man
  AssignClass (6073969a-b65b-4d2b-a7a3-468c8d707f8a)
 Call ID: 6073969a-b65b-4d2b-a7a3-468c8d707f8a
  Args:
    type: :Person
    source: KyrilVladimirovich
  AssignClass (eeb65abe-f30e-435a-ad06-b23edeb3b37b)
 Call ID: eeb65abe-f30e-435a-ad06-b23edeb3b37b
  Args:
    source: VictoriaMelita
    type: :Woman
  AssignClass (8d455abc-bb5d-4448-9891-4afd6f82e8fd)
 Call ID: 8d455abc-bb5d-4448-9891-4afd6f82e8fd
  Args:
    type: :Person
    source: VictoriaMelita
  AddTriple (a4f11f20-2947-4970-82dd-e85bce687706)
 Call ID: a4f11f20-2947-4970-82dd-e85bce687706
  Args:
    source: KiraKirillovna
    relation: :hasFather
    target: KyrilVladimirovich
  AddTriple (90ef9fb0-8a56-441a-b31c-29e2dd3d9d28)
 Call ID: 90ef9fb0-8a56-441a-b31c-29e2dd3d9d28
  Args:
    source: KiraKirillovna
    relation: :hasMother
    target: VictoriaMelita
  AssignClass (c3f4fea5-75e1-468d-8d71-434a14419af3)
 Call ID: c3f4fea5-75e1-468d-8d71-434a14419af3
  Args:
    type: :Man
    source: PrinceLouisFerdinandJr
  AssignClass (26e67486-58e0-472e-9ec2-4f5ffc55aa89)
 Call ID: 26e67486-58e0-472e-9ec2-4f5ffc55aa89
  Args:
    type: :Person
    source: PrinceLouisFerdinandJr
  AddTriple (7737a66b-fe1a-417e-8c34-8975aced1537)
 Call ID: 7737a66b-fe1a-417e-8c34-8975aced1537
  Args:
    relation: :hasSon
    target: PrinceLouisFerdinandJr
    source: LouisFerdinand
  AddLiteral (adc4f48c-4f90-4ee1-8a81-86a8eb8c1cb5)
 Call ID: adc4f48c-4f90-4ee1-8a81-86a8eb8c1cb5
  Args:
    source: PrinceLouisFerdinandJr
    literal_value: 1977
    literal_type: xsd:integer
    relation: :hasDeathYear
  AssignClass (cf66f1d4-3b48-41f0-a13a-670ab23dbd03)
 Call ID: cf66f1d4-3b48-41f0-a13a-670ab23dbd03
  Args:
    type: :Man
    source: GeorgFriedrich
  AssignClass (4716e50d-eaaf-46c5-9f97-14bd1f1a94a8)
 Call ID: 4716e50d-eaaf-46c5-9f97-14bd1f1a94a8
  Args:
    source: GeorgFriedrich
    type: :Person
  AddTriple (ee5e9a73-a308-4299-a85d-465ba8239920)
 Call ID: ee5e9a73-a308-4299-a85d-465ba8239920
  Args:
    relation: :hasFather
    target: PrinceLouisFerdinandJr
    source: GeorgFriedrich
  AssignClass (f30820aa-f44a-4c38-92d4-8003d205367d)
 Call ID: f30820aa-f44a-4c38-92d4-8003d205367d
  Args:
    type: :Man
    source: FrederickWilliamI
  AssignClass (99c19d08-0a22-44b0-9753-4afa7e1625ba)
 Call ID: 99c19d08-0a22-44b0-9753-4afa7e1625ba
  Args:
    source: FrederickWilliamI
    type: :Person
  AddTriple (25479d02-3557-49ce-a423-2f0eb8b45fc7)
 Call ID: 25479d02-3557-49ce-a423-2f0eb8b45fc7
  Args:
    relation: :hasFather
    target: FrederickWilliamI
    source: LouisFerdinand
  AssignClass (b580b905-bff9-4819-a43f-31f86e9c42c2)
 Call ID: b580b905-bff9-4819-a43f-31f86e9c42c2
  Args:
    source: FerdinandOfHohenzollern
    type: :Man
  AssignClass (a4d0a013-87c8-4bf9-a59d-ceb9a5d02b47)
 Call ID: a4d0a013-87c8-4bf9-a59d-ceb9a5d02b47
  Args:
    type: :Person
    source: FerdinandOfHohenzollern
  AddTriple (979c6bb7-4d20-4dc3-a76f-97aa998dff1b)
 Call ID: 979c6bb7-4d20-4dc3-a76f-97aa998dff1b
  Args:
    relation: :hasRelation
    target: FerdinandOfHohenzollern
    source: LouisFerdinand
  Finish (cd966cc5-5e6d-4b14-8903-c50fefe27811)
 Call ID: cd966cc5-5e6d-4b14-8903-c50fefe27811
  Args: