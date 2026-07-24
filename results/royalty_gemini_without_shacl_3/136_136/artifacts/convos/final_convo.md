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
Prince Alexander Ferdinand Albrecht Achilles Wilhelm Joseph Viktor Karl Feodor of Prussia (26 December 1912 – 12 June 1985) was the only son of Prince August Wilhelm of Prussia and Princess Alexandra Victoria of Schleswig-Holstein-Sonderburg-Glücksburg.
Family and early life

Prince Alexander of Prussia was born on 26 December 1912 to Prince August Wilhelm of Prussia and his wife Princess Alexandra Victoria of Schleswig-Holstein-Sonderburg-Glücksburg.
August Wilhelm was a younger son of Kaiser Wilhelm II.
His parents divorced in 1920 and his mother remarried less than two years later; custody of the young prince was awarded to Alexander's father.
Alexander attended the 1932 wedding of the Swedish prince Gustaf Adolf, Duke of Västerbotten with Princess Sibylla of Saxe-Coburg-Gotha in the former duchy of Coburg; it was the first time that a member of the German imperial family had entered the duchy since it became a republic, or specifically a part of Bavaria in November 1919 after the ruling duke, Carl Eduard, had ended his reign on 14 November 1918.
Nazi Party and military career

As of November 1939, Prince Alexander was a first lieutenant in the Air Force Signal Corps, stationed in Wiesbaden.
Like his father, who became a prominent supporter of the Nazi Party, Alexander became an early supporter.
Prince August had secret hopes that Chancellor Adolf Hitler "would one day hoist him or his son Alexander up to the vacant throne of the Kaiser".
The support that father and son gave to the emerging party caused strong disagreements among the Hohenzollerns, with Wilhelm II urging them both to leave the party.
In 1933, Alexander quit the SA and became a private in the German regular army.
Unlike many other German princes, who became the targets of Hitler's mistrust and were removed from their commands in the military, Alexander was the only Hohenzollern allowed to remain at his post.
Marriage

On 19 December 1938 in the Dresden garrison church, Alexander non-dynastically married Armgard Weygand (22 August 1912 – 3 December 2001), daughter of Major Friedrich Weygand and Karla Franziska Oheim.
She was married from 1928 to 1933 to Werner Rosendorff, airman in the German Air Force, and was originally from Wiesbaden, where Alexander Ferdinand was stationed.
They had one son:


Death

Prince Alexander Ferdinand died on 12 June 1985 at Wiesbaden.
}} Media related to Prince Alexander Ferdinand of Prussia at Wikimedia Commons



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
  AssignClass (ef8d76bf-8b0d-4c39-bf3e-b41a7d9b8833)
 Call ID: ef8d76bf-8b0d-4c39-bf3e-b41a7d9b8833
  Args:
    type: :Man
    source: PrinceAlexanderFerdinandOfPrussia
  AssignClass (12791559-88bc-498f-b66a-f3119b63202b)
 Call ID: 12791559-88bc-498f-b66a-f3119b63202b
  Args:
    type: :Person
    source: PrinceAlexanderFerdinandOfPrussia
  AddLiteral (e1a7369b-58fe-4096-8859-39f26dffb708)
 Call ID: e1a7369b-58fe-4096-8859-39f26dffb708
  Args:
    literal_type: xsd:integer
    source: PrinceAlexanderFerdinandOfPrussia
    literal_value: 1912
    relation: :hasBirthYear
  AddLiteral (c3007399-a250-4b49-bd48-e3e7af064bab)
 Call ID: c3007399-a250-4b49-bd48-e3e7af064bab
  Args:
    relation: :hasDeathYear
    literal_value: 1985
    source: PrinceAlexanderFerdinandOfPrussia
    literal_type: xsd:integer
  AssignClass (dd09272c-c6ec-4477-811e-ad4da54cfbef)
 Call ID: dd09272c-c6ec-4477-811e-ad4da54cfbef
  Args:
    type: :Man
    source: PrinceAugustWilhelmOfPrussia
  AssignClass (c580d9a0-da4b-4d94-9230-f3291ddcd4de)
 Call ID: c580d9a0-da4b-4d94-9230-f3291ddcd4de
  Args:
    type: :Person
    source: PrinceAugustWilhelmOfPrussia
  AssignClass (58f42e64-e18d-449b-9184-7b23a01f6a6b)
 Call ID: 58f42e64-e18d-449b-9184-7b23a01f6a6b
  Args:
    source: PrincessAlexandraVictoriaOfSchleswigHolsteinSonderburgGlucksburg
    type: :Woman
  AssignClass (d85206fe-5cef-45d3-b7ac-dab1438f03d4)
 Call ID: d85206fe-5cef-45d3-b7ac-dab1438f03d4
  Args:
    type: :Person
    source: PrincessAlexandraVictoriaOfSchleswigHolsteinSonderburgGlucksburg
  AddTriple (8cf953e7-b24a-4ef3-a36a-ddb1e018421c)
 Call ID: 8cf953e7-b24a-4ef3-a36a-ddb1e018421c
  Args:
    source: PrinceAlexanderFerdinandOfPrussia
    target: PrinceAugustWilhelmOfPrussia
    relation: :hasFather
  AddTriple (3c7ca22b-7899-47d3-931f-357fb41452a4)
 Call ID: 3c7ca22b-7899-47d3-931f-357fb41452a4
  Args:
    target: PrincessAlexandraVictoriaOfSchleswigHolsteinSonderburgGlucksburg
    source: PrinceAlexanderFerdinandOfPrussia
    relation: :hasMother
  AssignClass (ee48497a-13c3-4432-8b00-0f71c56c6ed4)
 Call ID: ee48497a-13c3-4432-8b00-0f71c56c6ed4
  Args:
    type: :Man
    source: KaiserWilhelmII
  AssignClass (60adc4b2-334d-4a6d-b778-121246282ad5)
 Call ID: 60adc4b2-334d-4a6d-b778-121246282ad5
  Args:
    source: KaiserWilhelmII
    type: :Person
  AddTriple (53201b65-31f7-4e11-a37e-6e54f4e297ec)
 Call ID: 53201b65-31f7-4e11-a37e-6e54f4e297ec
  Args:
    source: PrinceAugustWilhelmOfPrussia
    target: KaiserWilhelmII
    relation: :hasFather
  AssignClass (77c8c96c-a00e-4ab7-bbc2-691b1a20fddd)
 Call ID: 77c8c96c-a00e-4ab7-bbc2-691b1a20fddd
  Args:
    type: :Woman
    source: ArmgardWeygand
  AssignClass (cb977530-9c4d-4047-94df-f8e409bb42fb)
 Call ID: cb977530-9c4d-4047-94df-f8e409bb42fb
  Args:
    type: :Person
    source: ArmgardWeygand
  AddLiteral (3b09808e-a7f9-4fbb-a2cd-e3b18adb1f78)
 Call ID: 3b09808e-a7f9-4fbb-a2cd-e3b18adb1f78
  Args:
    relation: :hasMarriageYear
    literal_value: 1938
    source: PrinceAlexanderFerdinandOfPrussia
    literal_type: xsd:integer
  AddTriple (84fc8944-dceb-44fe-8fb9-501f9d884e2f)
 Call ID: 84fc8944-dceb-44fe-8fb9-501f9d884e2f
  Args:
    target: ArmgardWeygand
    source: PrinceAlexanderFerdinandOfPrussia
    relation: :hasRelation
  AssignClass (89ad16c0-30be-4397-91d3-e152ef558a94)
 Call ID: 89ad16c0-30be-4397-91d3-e152ef558a94
  Args:
    source: MajorFriedrichWeygand
    type: :Man
  AssignClass (12f882c3-8a91-4914-a4f3-51f35b2d7ec1)
 Call ID: 12f882c3-8a91-4914-a4f3-51f35b2d7ec1
  Args:
    source: MajorFriedrichWeygand
    type: :Person
  AssignClass (f3e41d6b-1a52-493b-bd8a-d103e774ac17)
 Call ID: f3e41d6b-1a52-493b-bd8a-d103e774ac17
  Args:
    source: KarlaFranziskaOheim
    type: :Woman
  AssignClass (45678708-2c89-4b90-b9eb-8708d6139c1b)
 Call ID: 45678708-2c89-4b90-b9eb-8708d6139c1b
  Args:
    source: KarlaFranziskaOheim
    type: :Person
  AddTriple (3eaab1b9-ceee-4718-b6e6-4b2a0c2631a9)
 Call ID: 3eaab1b9-ceee-4718-b6e6-4b2a0c2631a9
  Args:
    source: ArmgardWeygand
    target: MajorFriedrichWeygand
    relation: :hasFather
  AddTriple (a14225e5-ba98-4430-82f6-8b69d66118af)
 Call ID: a14225e5-ba98-4430-82f6-8b69d66118af
  Args:
    source: ArmgardWeygand
    target: KarlaFranziskaOheim
    relation: :hasMother
  AssignClass (f78aab37-b12f-47fb-8ee2-6c2d4bf0f4e4)
 Call ID: f78aab37-b12f-47fb-8ee2-6c2d4bf0f4e4
  Args:
    type: :Man
    source: WernerRosendorff
  AssignClass (461cf79b-d986-4f3d-86ea-3ee2154718ba)
 Call ID: 461cf79b-d986-4f3d-86ea-3ee2154718ba
  Args:
    source: WernerRosendorff
    type: :Person
  AddTriple (efb945c6-b49a-4858-8bbc-c155e57a636f)
 Call ID: efb945c6-b49a-4858-8bbc-c155e57a636f
  Args:
    source: ArmgardWeygand
    target: WernerRosendorff
    relation: :hasRelation
  Finish (8ffe4b6d-0297-4670-ac8f-ad672f410437)
 Call ID: 8ffe4b6d-0297-4670-ac8f-ad672f410437
  Args: