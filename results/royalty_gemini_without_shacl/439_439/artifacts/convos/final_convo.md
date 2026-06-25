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
Lady Mary Cecilia Colman (née Bowes-Lyon; 30 January 1932 – 2 January 2021) was an English socialite, philanthropist, and extra lady-in-waiting to Princess Alexandra, The Honourable Lady Ogilvy.
The daughter of Michael Bowes-Lyon and Elizabeth Margaret Cator, her paternal aunt was Queen Elizabeth
The Queen Mother, and she was thus a first cousin of Queen Elizabeth II and Princess Margaret, Countess of Snowdon.
Early life

Mary Cecilia Bowes-Lyon was born on 30 January 1932 at Gastlings, the Bowes-Lyon family home in Biggleswade, Bedfordshire.
Her father, Michael Bowes-Lyon (1893–1953), was the fifth son of Claude Bowes-Lyon, 14th
Earl of Strathmore and Kinghorne and Cecilia Bowes-Lyon, Countess of Strathmore and Kinghorne (née Cavendish-Bentinck).
Her mother, Elizabeth Margaret Cator (1899–1959), was a great-granddaughter of Charles Yorke, 4th Earl of Hardwicke.
She had a twin sister, Patricia Maud, later Lady Patricia Tetley, an older brother, Fergus Michael Claude, later Fergus Bowes-Lyon, 17th Earl of Strathmore and Kinghorne, and a younger brother, Michael Albemarle.
Lady Mary was also a godmother to Diana, Princess of Wales.
In 1949, a coming-out ball was held for her and her twin sister Patricia at Londonderry House, which was attended by their aunt, the Queen, and their cousins, The Princess Elizabeth and The Princess Margaret.
Marriage and children

On 10 November 1951 at St Bartholomew-the-Great in London, Mary married the then-Lieutenant Timothy Colman, son of the cricketer Geoffrey Colman.
Work and later life

In 1970, Mary was appointed an Extra Lady-in-waiting to another of the Queen's first cousins, Princess Alexandra, The Hon.
After her elder brother succeeded their cousin as 17th Earl of Strathmore and Kinghorne, she received the title and precedence of a daughter of an earl by royal warrant of precedence in 1974.
Lady Mary died at her home in Bixley, Norfolk on 2 January 2021, at the age of 88.



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
  AssignClass (abf51d80-46d7-4808-b646-560d12e45202)
 Call ID: abf51d80-46d7-4808-b646-560d12e45202
  Args:
    source: :LadyMaryCeciliaColman
    type: :Woman
  AssignClass (21f21149-c229-4c67-bda1-e44809aa9197)
 Call ID: 21f21149-c229-4c67-bda1-e44809aa9197
  Args:
    source: :MichaelBowes-Lyon
    type: :Man
  AssignClass (c10ea88d-0a7c-4f69-bb0b-882236afb74a)
 Call ID: c10ea88d-0a7c-4f69-bb0b-882236afb74a
  Args:
    type: :Woman
    source: :ElizabethMargaretCator
  AssignClass (3be601bc-3019-4f9a-a591-db95a1e5ef01)
 Call ID: 3be601bc-3019-4f9a-a591-db95a1e5ef01
  Args:
    source: :TimothyColman
    type: :Man
  AssignClass (f1e10419-fa34-43f2-82ff-11a938a4079c)
 Call ID: f1e10419-fa34-43f2-82ff-11a938a4079c
  Args:
    source: :GeoffreyColman
    type: :Man
  AssignClass (f7a380cb-df72-4494-9020-dde26943957c)
 Call ID: f7a380cb-df72-4494-9020-dde26943957c
  Args:
    type: :Woman
    source: :PatriciaMaud
  AssignClass (308f597b-cec7-46ca-b831-50e9e93c0af9)
 Call ID: 308f597b-cec7-46ca-b831-50e9e93c0af9
  Args:
    source: :FergusMichaelClaude
    type: :Man
  AssignClass (5c0147ad-1610-47cd-84ab-329a9e4cf10d)
 Call ID: 5c0147ad-1610-47cd-84ab-329a9e4cf10d
  Args:
    source: :MichaelAlbemarle
    type: :Man
  AssignClass (16edd1c3-b803-4b0c-83b8-1f318889b397)
 Call ID: 16edd1c3-b803-4b0c-83b8-1f318889b397
  Args:
    source: :ClaudeBowes-Lyon
    type: :Man
  AssignClass (345fb00b-ff21-4884-a26f-c3ac4b359006)
 Call ID: 345fb00b-ff21-4884-a26f-c3ac4b359006
  Args:
    type: :Woman
    source: :CeciliaBowes-Lyon
  AddLiteral (fe81aae3-df2a-46f6-a489-825c62b412a0)
 Call ID: fe81aae3-df2a-46f6-a489-825c62b412a0
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: :LadyMaryCeciliaColman
    literal_value: 1932
  AddLiteral (b40b771c-4902-4bad-9dce-42efd9d69d5d)
 Call ID: b40b771c-4902-4bad-9dce-42efd9d69d5d
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 2021
    source: :LadyMaryCeciliaColman
  AddLiteral (427ba413-1637-4de3-b8cb-4e8162673cc1)
 Call ID: 427ba413-1637-4de3-b8cb-4e8162673cc1
  Args:
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: :LadyMaryCeciliaColman
    literal_value: 1951
  AddTriple (342bc89d-19dd-400d-b1eb-c1ae86e5ea08)
 Call ID: 342bc89d-19dd-400d-b1eb-c1ae86e5ea08
  Args:
    target: :MichaelBowes-Lyon
    source: :LadyMaryCeciliaColman
    relation: :hasFather
  AddTriple (0cdbce65-f6ad-49ec-bd4f-33e56f278728)
 Call ID: 0cdbce65-f6ad-49ec-bd4f-33e56f278728
  Args:
    target: :ElizabethMargaretCator
    source: :LadyMaryCeciliaColman
    relation: :hasMother
  AddTriple (ca8da53c-40d1-4433-88d9-0ae725086c8b)
 Call ID: ca8da53c-40d1-4433-88d9-0ae725086c8b
  Args:
    source: :MichaelBowes-Lyon
    target: :ClaudeBowes-Lyon
    relation: :hasFather
  AddTriple (08e22601-c04a-4417-bf5f-2a8a843d6486)
 Call ID: 08e22601-c04a-4417-bf5f-2a8a843d6486
  Args:
    relation: :hasMother
    source: :MichaelBowes-Lyon
    target: :CeciliaBowes-Lyon
  AddTriple (e8a75ead-9da4-40cf-8635-de7764327ae0)
 Call ID: e8a75ead-9da4-40cf-8635-de7764327ae0
  Args:
    target: :GeoffreyColman
    source: :TimothyColman
    relation: :hasFather
  AddTriple (6a15160e-b609-4c1f-93f5-5a4517d04614)
 Call ID: 6a15160e-b609-4c1f-93f5-5a4517d04614
  Args:
    relation: :isSisterOf
    source: :PatriciaMaud
    target: :LadyMaryCeciliaColman
  AddTriple (ed96094b-df9b-488e-b5d2-938299b7d152)
 Call ID: ed96094b-df9b-488e-b5d2-938299b7d152
  Args:
    relation: :hasBrother
    target: :FergusMichaelClaude
    source: :LadyMaryCeciliaColman
  AddTriple (3e6b13b3-cc94-44b8-8af2-95be885ba344)
 Call ID: 3e6b13b3-cc94-44b8-8af2-95be885ba344
  Args:
    target: :MichaelAlbemarle
    source: :LadyMaryCeciliaColman
    relation: :hasBrother
  Finish (9aa75921-3023-4be1-981d-08762e2e30f7)
 Call ID: 9aa75921-3023-4be1-981d-08762e2e30f7
  Args: