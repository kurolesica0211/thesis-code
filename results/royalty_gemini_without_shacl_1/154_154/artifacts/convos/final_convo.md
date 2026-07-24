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
Prince Maurice of Battenberg (Maurice Victor Donald; 3 October 1891 – 27 October 1914) was a member of the Hessian princely Battenberg family and the extended British royal family, and the youngest grandchild of Queen Victoria.
He was styled as Prince Maurice throughout his life and died before the Battenberg family anglicised their surname to Mountbatten in 1917, meaning he was never known by that name.
Early life

Maurice was born on 3 October 1891.
His father was Prince Henry of Battenberg, the son of Prince Alexander of Hesse and by Rhine and Julie Therese née Countess of Hauke.
His mother was Princess Henry of Battenberg (née Princess Beatrice of the United Kingdom), the fifth daughter and the youngest child of Queen Victoria and Albert, Prince Consort.
As he was the child of a morganatic marriage, Prince Henry of Battenberg took his style of Prince of Battenberg from his mother, Countess Julia Hauke, who was created Princess of Battenberg in her own right.
As such, Maurice was styled as His Serene Highness Prince Maurice of Battenberg from birth.
In the United Kingdom, he was styled His Highness Prince Maurice of Battenberg under a royal warrant passed by Queen Victoria in 1886.
His godparents were the Duchess of Connaught and Strathearn (represented by Queen Victoria), the Princess of Leiningen (represented by Princess Christian of Schleswig-Holstein), the Duke of Clarence and Avondale (represented by Sir Henry Ponsonby), Prince Francis Joseph of Battenberg (represented by Sir Fleetwood Edwards) and the Hereditary Grand Duke of Hesse.
The youngest of his four siblings, Maurice most resembled his father, who died when he was only four, the same age his mother was when her own father died.
His elder sister Victoria Eugenie of Battenberg married Alfonso XIII of Spain and was Queen Consort of Spain between 1906 and 1931.
Later life

Maurice attended Wellington College and was a member of Benson House.
Maurice was made a Freemason in the Old Wellingtonian Lodge No. 3404 (the Lodge of the Old Wellingtonians) on 21 June 1912 and was installed Master of the Twelve Brothers Lodge, No. 785 Southampton on 22 April 1914.
After attending the Royal Military College, Sandhurst, Maurice was commissioned as a second lieutenant in the King's Royal Rifle Corps on 4 March 1911.
Poor  Maurice was killed outright just on top of the ridge.
"


Word of the Maurice's death was passed to Brigadier-General Fanshawe, commander of the 6th Infantry Brigade.
He said, "By the death of H.H. Prince Maurice of Battenberg the Army loses a most gallant and valuable officer.
His mother, Princess Beatrice, declined the offer of Lord Kitchener to have her son's body repatriated.
The battalion war diary notes that his funeral took place on 31 October 1914 and records that, "Denison, Gough, the Sgt Major, Sgt O'Leary and a few others went down to poor Maurice's funeral in Ypres".



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
  AssignClass (f5c0440c-897e-47b8-bf94-ef576b025dca)
 Call ID: f5c0440c-897e-47b8-bf94-ef576b025dca
  Args:
    type: :Man
    source: PrinceMauriceOfBattenberg
  AssignClass (e52047ac-7f51-43d9-87d2-d94410eb8e0d)
 Call ID: e52047ac-7f51-43d9-87d2-d94410eb8e0d
  Args:
    type: :Person
    source: PrinceMauriceOfBattenberg
  AddLiteral (ce99a908-c62a-4bf9-bf7b-22ca0c661124)
 Call ID: ce99a908-c62a-4bf9-bf7b-22ca0c661124
  Args:
    literal_type: xsd:string
    source: PrinceMauriceOfBattenberg
    relation: :alsoKnownAs
    literal_value: Maurice Victor Donald
  AddLiteral (2739f250-80f6-4c89-a176-53a996b114bf)
 Call ID: 2739f250-80f6-4c89-a176-53a996b114bf
  Args:
    literal_type: xsd:integer
    source: PrinceMauriceOfBattenberg
    relation: :hasBirthYear
    literal_value: 1891
  AddLiteral (d243952c-04bf-434c-b843-bc9e986b242c)
 Call ID: d243952c-04bf-434c-b843-bc9e986b242c
  Args:
    source: PrinceMauriceOfBattenberg
    relation: :hasDeathYear
    literal_value: 1914
    literal_type: xsd:integer
  AssignClass (808dbc0a-e9c7-4f65-a723-0589eb8c6e4c)
 Call ID: 808dbc0a-e9c7-4f65-a723-0589eb8c6e4c
  Args:
    source: PrinceHenryOfBattenberg
    type: :Man
  AssignClass (584d4f2b-6dca-4098-9bc0-11f4f0bc0988)
 Call ID: 584d4f2b-6dca-4098-9bc0-11f4f0bc0988
  Args:
    source: PrinceHenryOfBattenberg
    type: :Person
  AddTriple (53f0be7c-e7c4-4ac8-a01d-8ce5c6d102c5)
 Call ID: 53f0be7c-e7c4-4ac8-a01d-8ce5c6d102c5
  Args:
    relation: :hasFather
    target: PrinceHenryOfBattenberg
    source: PrinceMauriceOfBattenberg
  AssignClass (0ae0db7d-be9b-4130-b333-16eb29d8412e)
 Call ID: 0ae0db7d-be9b-4130-b333-16eb29d8412e
  Args:
    type: :Man
    source: PrinceAlexanderOfHesseAndByRhine
  AssignClass (3429bc52-1a8b-4d4d-bb25-8a1e20ccb145)
 Call ID: 3429bc52-1a8b-4d4d-bb25-8a1e20ccb145
  Args:
    type: :Person
    source: PrinceAlexanderOfHesseAndByRhine
  AddTriple (a84119e8-f72d-431b-8a7d-3a782ad9b0ea)
 Call ID: a84119e8-f72d-431b-8a7d-3a782ad9b0ea
  Args:
    source: PrinceHenryOfBattenberg
    target: PrinceAlexanderOfHesseAndByRhine
    relation: :hasFather
  AssignClass (a254b24d-e05d-4aa7-a5d9-48b7a6819d1f)
 Call ID: a254b24d-e05d-4aa7-a5d9-48b7a6819d1f
  Args:
    source: JulieThereseHauke
    type: :Woman
  AssignClass (0a628e36-c2fd-4bf7-8949-4b5074e7d06a)
 Call ID: 0a628e36-c2fd-4bf7-8949-4b5074e7d06a
  Args:
    type: :Person
    source: JulieThereseHauke
  AddTriple (873f705e-1354-463c-a5a7-c81362d099c0)
 Call ID: 873f705e-1354-463c-a5a7-c81362d099c0
  Args:
    source: PrinceHenryOfBattenberg
    target: JulieThereseHauke
    relation: :hasMother
  AssignClass (d7fd017c-05d1-4055-abd5-e3fd2869b4e1)
 Call ID: d7fd017c-05d1-4055-abd5-e3fd2869b4e1
  Args:
    type: :Woman
    source: PrincessBeatrice
  AssignClass (14e07caf-c595-4bdc-aa63-29342d5c5ae0)
 Call ID: 14e07caf-c595-4bdc-aa63-29342d5c5ae0
  Args:
    type: :Person
    source: PrincessBeatrice
  AddTriple (a374fba4-3daf-4ce3-b486-e8fae554a888)
 Call ID: a374fba4-3daf-4ce3-b486-e8fae554a888
  Args:
    source: PrinceMauriceOfBattenberg
    relation: :hasMother
    target: PrincessBeatrice
  AssignClass (90521cd0-2318-481a-a860-90b42e391d4e)
 Call ID: 90521cd0-2318-481a-a860-90b42e391d4e
  Args:
    type: :Woman
    source: QueenVictoria
  AssignClass (35e6b95e-9481-4fdc-b068-4632f9ff4703)
 Call ID: 35e6b95e-9481-4fdc-b068-4632f9ff4703
  Args:
    type: :Person
    source: QueenVictoria
  AssignClass (19f48136-eb52-45be-9d74-d7ea47a77b84)
 Call ID: 19f48136-eb52-45be-9d74-d7ea47a77b84
  Args:
    type: :Man
    source: AlbertPrinceConsort
  AssignClass (21415acb-3987-4132-9c81-417fa339072c)
 Call ID: 21415acb-3987-4132-9c81-417fa339072c
  Args:
    type: :Person
    source: AlbertPrinceConsort
  AddTriple (81cec7d3-7eff-4350-a992-fb629fba7f1a)
 Call ID: 81cec7d3-7eff-4350-a992-fb629fba7f1a
  Args:
    source: PrincessBeatrice
    target: QueenVictoria
    relation: :hasMother
  AddTriple (bb20b924-9de1-46a7-b022-f6364e4fd11e)
 Call ID: bb20b924-9de1-46a7-b022-f6364e4fd11e
  Args:
    target: AlbertPrinceConsort
    relation: :hasFather
    source: PrincessBeatrice
  AssignClass (9b26845e-7231-4731-9cf6-f808306e9731)
 Call ID: 9b26845e-7231-4731-9cf6-f808306e9731
  Args:
    source: VictoriaEugenieOfBattenberg
    type: :Woman
  AssignClass (20239163-9c06-4961-9819-249c2a0527ba)
 Call ID: 20239163-9c06-4961-9819-249c2a0527ba
  Args:
    type: :Person
    source: VictoriaEugenieOfBattenberg
  AddTriple (9d0b0d28-e5a7-4a13-b88a-e2dd2b0aac74)
 Call ID: 9d0b0d28-e5a7-4a13-b88a-e2dd2b0aac74
  Args:
    source: VictoriaEugenieOfBattenberg
    relation: :hasMother
    target: PrincessBeatrice
  AddTriple (2a478ee3-78fe-4eb2-9b86-20e8754fd570)
 Call ID: 2a478ee3-78fe-4eb2-9b86-20e8754fd570
  Args:
    source: VictoriaEugenieOfBattenberg
    target: PrinceHenryOfBattenberg
    relation: :hasFather
  AssignClass (8a7c709a-d916-437c-ad13-29be21009280)
 Call ID: 8a7c709a-d916-437c-ad13-29be21009280
  Args:
    type: :Man
    source: AlfonsoXIIIOfSpain
  AssignClass (123f3fd5-6132-4e7c-8270-6c5405e7edb0)
 Call ID: 123f3fd5-6132-4e7c-8270-6c5405e7edb0
  Args:
    type: :Person
    source: AlfonsoXIIIOfSpain
  AddTriple (f4bfd61e-ceda-4ced-8b9b-4a42d9dc0523)
 Call ID: f4bfd61e-ceda-4ced-8b9b-4a42d9dc0523
  Args:
    source: VictoriaEugenieOfBattenberg
    relation: :hasRelation
    target: AlfonsoXIIIOfSpain
  Finish (98c4b109-acab-4b09-bbdf-e413e851fbbb)
 Call ID: 98c4b109-acab-4b09-bbdf-e413e851fbbb
  Args: