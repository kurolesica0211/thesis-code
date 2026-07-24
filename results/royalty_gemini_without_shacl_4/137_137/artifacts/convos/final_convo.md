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
Lord Leopold Arthur Louis Mountbatten (21 May 1889 – 23 April 1922) was a British Army officer and a descendant of the Hessian princely Battenberg family and the British royal family.
A grandson of Queen Victoria, he was known as Prince Leopold of Battenberg from his birth until 1917, when the British royal family relinquished their German titles during World War I, and the Battenberg family changed their name to Mountbatten.
Early life

Leopold was born on 21 May 1889.
His father was Prince Henry of Battenberg, the son of Prince Alexander of Hesse and by Rhine and Julia, Princess of Battenberg.
His mother was Princess Beatrice of the United Kingdom, the fifth daughter and the youngest child of Queen Victoria and Prince Albert.
As he was the product of a morganatic marriage, Prince Henry of Battenberg took his style of Prince of Battenberg from his mother, Julia von Hauke, who was created Princess of Battenberg in her own right.
As such, Leopold was styled as His Serene Highness Prince Leopold of Battenberg from birth.
In the United Kingdom, he was styled His Highness Prince Leopold of Battenberg under a royal warrant passed by Queen Victoria in 1886.
His godparents were Leopold II of Belgium (his first cousin twice removed, represented by the Prince of Wales, his maternal uncle), the Duke of Connaught and Strathearn (his maternal uncle, represented by Prince Albert of Schleswig-Holstein, his first cousin), Prince Louis of Battenberg (his paternal uncle, represented by the Marquess of Lorne, his maternal uncle), the Marchioness of Lorne (his maternal aunt), the Duchess of Albany (his maternal aunt) and Princess Marie of Erbach-Schönberg (his paternal aunt).
Leopold was a haemophiliac, a condition he inherited through his mother.
His namesake maternal uncle, Prince Leopold, Duke of Albany, had died from the same condition.
Military career

Leopold was commissioned a lieutenant (supernumerary) on 16 October 1909 in the 8th Battalion of the Isle of Wight Rifles, a Territorial Force unit.
Relinquishment of titles

During the First World War, anti-German feeling in the United Kingdom led Leopold's first cousin, George V to change the name of the royal house from the Germanic House of Saxe-Coburg and Gotha to the more English-sounding House of Windsor.
In response to this, Leopold renounced his title of Prince, the style His Highness and the designation 'of Battenberg' through a royal warrant from the King dated 14 July 1917, and became Sir Leopold Mountbatten by virtue of his being a Knight Grand Cross of the Royal Victorian Order.
Under a further warrant of 11 September 1917 he was granted the style and precedence of the younger son of a marquess, and became Lord Leopold Mountbatten.
Death

Lord Leopold died on 23 April 1922(1922-04-23) (aged 32), during a hip operation.



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
  AssignClass (5ce73bc3-6024-40ed-b1b8-f9472eb05a85)
 Call ID: 5ce73bc3-6024-40ed-b1b8-f9472eb05a85
  Args:
    type: :Man
    source: LeopoldMountbatten
  AssignClass (603b20c4-67cd-4bb6-a19d-b58147e47022)
 Call ID: 603b20c4-67cd-4bb6-a19d-b58147e47022
  Args:
    type: :Person
    source: LeopoldMountbatten
  AddLiteral (156ad107-a171-4e5c-9d4f-173e4b704376)
 Call ID: 156ad107-a171-4e5c-9d4f-173e4b704376
  Args:
    relation: :hasBirthYear
    source: LeopoldMountbatten
    literal_value: 1889
    literal_type: xsd:integer
  AddLiteral (062b448f-ebf7-4bbb-a641-c49c1805a473)
 Call ID: 062b448f-ebf7-4bbb-a641-c49c1805a473
  Args:
    literal_type: xsd:integer
    literal_value: 1922
    relation: :hasDeathYear
    source: LeopoldMountbatten
  AddLiteral (e4d20884-2e22-4188-8c52-6fa04552607b)
 Call ID: e4d20884-2e22-4188-8c52-6fa04552607b
  Args:
    literal_value: Prince Leopold of Battenberg
    literal_type: xsd:string
    source: LeopoldMountbatten
    relation: :formerlyKnownAs
  AddLiteral (4a5640b2-a1ac-42cd-902e-2b4a40b642ef)
 Call ID: 4a5640b2-a1ac-42cd-902e-2b4a40b642ef
  Args:
    relation: :alsoKnownAs
    source: LeopoldMountbatten
    literal_type: xsd:string
    literal_value: Sir Leopold Mountbatten
  AddLiteral (a9d0ee5a-1481-4261-ab11-442e6d5d312d)
 Call ID: a9d0ee5a-1481-4261-ab11-442e6d5d312d
  Args:
    source: LeopoldMountbatten
    relation: :knownAs
    literal_type: xsd:string
    literal_value: Lord Leopold Mountbatten
  AssignClass (bb1efd68-4890-439c-8c2d-5e044a7d1b8c)
 Call ID: bb1efd68-4890-439c-8c2d-5e044a7d1b8c
  Args:
    type: :Man
    source: HenryOfBattenberg
  AssignClass (cb54ff3e-e2e5-4b36-bc77-f4023a17bc49)
 Call ID: cb54ff3e-e2e5-4b36-bc77-f4023a17bc49
  Args:
    type: :Person
    source: HenryOfBattenberg
  AddTriple (05ad87f4-18be-485c-b098-783fc4a49c6f)
 Call ID: 05ad87f4-18be-485c-b098-783fc4a49c6f
  Args:
    relation: :hasFather
    source: LeopoldMountbatten
    target: HenryOfBattenberg
  AssignClass (1c7493e0-8585-4de2-80d1-c5a0832d5157)
 Call ID: 1c7493e0-8585-4de2-80d1-c5a0832d5157
  Args:
    type: :Woman
    source: BeatriceOfTheUnitedKingdom
  AssignClass (4f7e7969-81d2-46c1-bfbc-b7e923a5fb7c)
 Call ID: 4f7e7969-81d2-46c1-bfbc-b7e923a5fb7c
  Args:
    type: :Person
    source: BeatriceOfTheUnitedKingdom
  AddTriple (ea82145f-9c50-47d4-81c1-07a4530bb1c1)
 Call ID: ea82145f-9c50-47d4-81c1-07a4530bb1c1
  Args:
    target: BeatriceOfTheUnitedKingdom
    source: LeopoldMountbatten
    relation: :hasMother
  AssignClass (7dc38d0f-5b46-4d94-b8ca-2a5d566a13ac)
 Call ID: 7dc38d0f-5b46-4d94-b8ca-2a5d566a13ac
  Args:
    type: :Man
    source: AlexanderOfHesseAndByRhine
  AssignClass (ae5fc723-8a1a-4eea-ba4e-b8f7fba89a63)
 Call ID: ae5fc723-8a1a-4eea-ba4e-b8f7fba89a63
  Args:
    type: :Person
    source: AlexanderOfHesseAndByRhine
  AssignClass (6f73780e-7e83-44ec-89e1-bccdad1d9e36)
 Call ID: 6f73780e-7e83-44ec-89e1-bccdad1d9e36
  Args:
    type: :Woman
    source: JuliaPrincessOfBattenberg
  AssignClass (34bae70b-2d5e-4ac0-a633-a23cd0936877)
 Call ID: 34bae70b-2d5e-4ac0-a633-a23cd0936877
  Args:
    type: :Person
    source: JuliaPrincessOfBattenberg
  AddTriple (deb48802-b777-4861-a700-6872496d1d8c)
 Call ID: deb48802-b777-4861-a700-6872496d1d8c
  Args:
    target: AlexanderOfHesseAndByRhine
    source: HenryOfBattenberg
    relation: :hasFather
  AddTriple (9b70fcf0-29da-4cab-a0eb-05cc3e07b58a)
 Call ID: 9b70fcf0-29da-4cab-a0eb-05cc3e07b58a
  Args:
    relation: :hasMother
    source: HenryOfBattenberg
    target: JuliaPrincessOfBattenberg
  AssignClass (17a0dc1a-ba2c-4dc4-ab5d-6484f34f8397)
 Call ID: 17a0dc1a-ba2c-4dc4-ab5d-6484f34f8397
  Args:
    type: :Woman
    source: QueenVictoria
  AssignClass (ef778d62-bdff-4869-b4ce-f13c0e60546c)
 Call ID: ef778d62-bdff-4869-b4ce-f13c0e60546c
  Args:
    type: :Person
    source: QueenVictoria
  AssignClass (7e9cb077-0c7e-4eb2-8f2f-30a9be26d5f6)
 Call ID: 7e9cb077-0c7e-4eb2-8f2f-30a9be26d5f6
  Args:
    type: :Man
    source: PrinceAlbert
  AssignClass (4391205e-87ec-407a-b56b-f89f0ef41c92)
 Call ID: 4391205e-87ec-407a-b56b-f89f0ef41c92
  Args:
    type: :Person
    source: PrinceAlbert
  AddTriple (1b1110b3-9022-46d5-a139-93db9ecd7d34)
 Call ID: 1b1110b3-9022-46d5-a139-93db9ecd7d34
  Args:
    relation: :hasMother
    source: BeatriceOfTheUnitedKingdom
    target: QueenVictoria
  AddTriple (fc896576-1541-4cb2-bcbd-b8d541f89b70)
 Call ID: fc896576-1541-4cb2-bcbd-b8d541f89b70
  Args:
    target: PrinceAlbert
    source: BeatriceOfTheUnitedKingdom
    relation: :hasFather
  AssignClass (0acb4003-603c-4db9-bab0-039af2f26302)
 Call ID: 0acb4003-603c-4db9-bab0-039af2f26302
  Args:
    type: :Man
    source: PrinceLeopoldDukeOfAlbany
  AssignClass (ec810cfe-de58-4a36-85c5-42b3fb73999c)
 Call ID: ec810cfe-de58-4a36-85c5-42b3fb73999c
  Args:
    type: :Person
    source: PrinceLeopoldDukeOfAlbany
  AddTriple (9a29551c-13e5-4e3b-9a52-9dcb7248deb9)
 Call ID: 9a29551c-13e5-4e3b-9a52-9dcb7248deb9
  Args:
    relation: :isBrotherOf
    source: PrinceLeopoldDukeOfAlbany
    target: BeatriceOfTheUnitedKingdom
  Finish (4e4fda8f-9a35-424b-bada-883de1a15b19)
 Call ID: 4e4fda8f-9a35-424b-bada-883de1a15b19
  Args: