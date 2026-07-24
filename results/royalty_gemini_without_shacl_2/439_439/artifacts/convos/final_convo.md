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
  AssignClass (1f04165a-8904-4c9f-93db-5c7c69e39559)
 Call ID: 1f04165a-8904-4c9f-93db-5c7c69e39559
  Args:
    source: :MaryCeciliaColman
    type: :Woman
  AssignClass (515bf172-a767-4ffb-bf37-b16f6d42a2ab)
 Call ID: 515bf172-a767-4ffb-bf37-b16f6d42a2ab
  Args:
    source: :MaryCeciliaColman
    type: :Person
  AddLiteral (314558f0-920d-4900-86c6-e0268de69d85)
 Call ID: 314558f0-920d-4900-86c6-e0268de69d85
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: :MaryCeciliaColman
    literal_value: 1932
  AddLiteral (f9cc1177-97f5-4ad2-b312-af45e9983a94)
 Call ID: f9cc1177-97f5-4ad2-b312-af45e9983a94
  Args:
    literal_value: 2021
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: :MaryCeciliaColman
  AssignClass (89b2042e-5463-4f44-ae4b-757425192797)
 Call ID: 89b2042e-5463-4f44-ae4b-757425192797
  Args:
    type: :Man
    source: :MichaelBowesLyon
  AssignClass (a3908cfc-de64-45df-9980-da25677b7702)
 Call ID: a3908cfc-de64-45df-9980-da25677b7702
  Args:
    type: :Person
    source: :MichaelBowesLyon
  AddLiteral (eb0c7e24-ae08-4654-999e-690effe3dad1)
 Call ID: eb0c7e24-ae08-4654-999e-690effe3dad1
  Args:
    literal_value: 1893
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: :MichaelBowesLyon
  AddLiteral (2485e9b8-0faf-4b95-af37-b6535a72a067)
 Call ID: 2485e9b8-0faf-4b95-af37-b6535a72a067
  Args:
    literal_value: 1953
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: :MichaelBowesLyon
  AssignClass (fb4f4dad-78b4-4ba4-9aee-4d1d345bb4be)
 Call ID: fb4f4dad-78b4-4ba4-9aee-4d1d345bb4be
  Args:
    source: :ElizabethMargaretCator
    type: :Woman
  AssignClass (9e528782-975f-4999-a94d-61b5f74d66eb)
 Call ID: 9e528782-975f-4999-a94d-61b5f74d66eb
  Args:
    source: :ElizabethMargaretCator
    type: :Person
  AddLiteral (e4668ea2-8512-46db-b687-0014abeee52e)
 Call ID: e4668ea2-8512-46db-b687-0014abeee52e
  Args:
    source: :ElizabethMargaretCator
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1899
  AddLiteral (8757c778-ce61-4a12-81ec-7775b6c94f8d)
 Call ID: 8757c778-ce61-4a12-81ec-7775b6c94f8d
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: :ElizabethMargaretCator
    literal_value: 1959
  AddTriple (b6c8264a-45e0-48f0-b5e5-efc63803a440)
 Call ID: b6c8264a-45e0-48f0-b5e5-efc63803a440
  Args:
    source: :MaryCeciliaColman
    target: :MichaelBowesLyon
    relation: :hasFather
  AddTriple (c5d3f36d-be82-43ad-a853-ee5d6735663f)
 Call ID: c5d3f36d-be82-43ad-a853-ee5d6735663f
  Args:
    relation: :hasMother
    source: :MaryCeciliaColman
    target: :ElizabethMargaretCator
  AssignClass (0ed51d95-8ef2-432d-a8b2-b755f9729fd0)
 Call ID: 0ed51d95-8ef2-432d-a8b2-b755f9729fd0
  Args:
    source: :PatriciaMaud
    type: :Woman
  AssignClass (08f94cc7-aea3-416d-a871-3bc4f6813835)
 Call ID: 08f94cc7-aea3-416d-a871-3bc4f6813835
  Args:
    source: :PatriciaMaud
    type: :Person
  AddTriple (4e82b96c-14d4-40e0-98aa-6738f2ad53b1)
 Call ID: 4e82b96c-14d4-40e0-98aa-6738f2ad53b1
  Args:
    relation: :hasSister
    source: :MaryCeciliaColman
    target: :PatriciaMaud
  AssignClass (d99da1c8-71e8-4e96-8457-67f1f097033d)
 Call ID: d99da1c8-71e8-4e96-8457-67f1f097033d
  Args:
    source: :FergusMichaelClaude
    type: :Man
  AssignClass (9c5e3cb1-be38-40e0-a2a5-78dbed7e8013)
 Call ID: 9c5e3cb1-be38-40e0-a2a5-78dbed7e8013
  Args:
    source: :FergusMichaelClaude
    type: :Person
  AddTriple (7b933c4c-44bb-49be-9db3-faa5a5ec3747)
 Call ID: 7b933c4c-44bb-49be-9db3-faa5a5ec3747
  Args:
    relation: :hasBrother
    target: :FergusMichaelClaude
    source: :MaryCeciliaColman
  AssignClass (310fa9e8-ca76-4b51-89ca-1bbe585f055e)
 Call ID: 310fa9e8-ca76-4b51-89ca-1bbe585f055e
  Args:
    source: :MichaelAlbemarle
    type: :Man
  AssignClass (f1e73c92-75bb-49dd-b180-f55545e28b3e)
 Call ID: f1e73c92-75bb-49dd-b180-f55545e28b3e
  Args:
    type: :Person
    source: :MichaelAlbemarle
  AddTriple (7a2cd31e-9acc-48f3-8a47-b2ab6f34d04c)
 Call ID: 7a2cd31e-9acc-48f3-8a47-b2ab6f34d04c
  Args:
    relation: :hasBrother
    target: :MichaelAlbemarle
    source: :MaryCeciliaColman
  AssignClass (734d8290-5211-496b-86fe-5884dfa02694)
 Call ID: 734d8290-5211-496b-86fe-5884dfa02694
  Args:
    source: :ClaudeBowesLyon
    type: :Man
  AssignClass (0ab54674-f4c6-49c1-a875-901228e0550e)
 Call ID: 0ab54674-f4c6-49c1-a875-901228e0550e
  Args:
    source: :ClaudeBowesLyon
    type: :Person
  AssignClass (50fce428-29d5-4641-b32b-d448c8dbecb9)
 Call ID: 50fce428-29d5-4641-b32b-d448c8dbecb9
  Args:
    source: :CeciliaBowesLyon
    type: :Woman
  AssignClass (d73e1f50-b143-4069-bb50-512c3714b91f)
 Call ID: d73e1f50-b143-4069-bb50-512c3714b91f
  Args:
    source: :CeciliaBowesLyon
    type: :Person
  AddTriple (6033c95b-48b7-4191-a3cb-34372b485f22)
 Call ID: 6033c95b-48b7-4191-a3cb-34372b485f22
  Args:
    source: :MichaelBowesLyon
    target: :ClaudeBowesLyon
    relation: :hasFather
  AddTriple (f05b9061-5cda-4bb4-a7a3-a6adc11311de)
 Call ID: f05b9061-5cda-4bb4-a7a3-a6adc11311de
  Args:
    target: :CeciliaBowesLyon
    source: :MichaelBowesLyon
    relation: :hasMother
  AssignClass (8abef165-4034-4c5e-b915-8a265ad763d5)
 Call ID: 8abef165-4034-4c5e-b915-8a265ad763d5
  Args:
    source: :TimothyColman
    type: :Man
  AssignClass (001ef8c7-4105-4e21-9787-17cea8a31fdf)
 Call ID: 001ef8c7-4105-4e21-9787-17cea8a31fdf
  Args:
    source: :TimothyColman
    type: :Person
  AddLiteral (e9bc18d5-2510-49d2-aa69-d1ac4bfb9a39)
 Call ID: e9bc18d5-2510-49d2-aa69-d1ac4bfb9a39
  Args:
    literal_value: 1951
    literal_type: xsd:integer
    relation: :hasMarriageYear
    source: :MaryCeciliaColman
  AddTriple (9f0e8b39-93b5-422e-9a86-dda11bcb3ebb)
 Call ID: 9f0e8b39-93b5-422e-9a86-dda11bcb3ebb
  Args:
    relation: :hasRelation
    source: :MaryCeciliaColman
    target: :TimothyColman
  AssignClass (889c05dd-818f-4916-b679-eb0524d9b2f5)
 Call ID: 889c05dd-818f-4916-b679-eb0524d9b2f5
  Args:
    source: :GeoffreyColman
    type: :Man
  AssignClass (7d284e06-00f5-40ba-b229-49d81580c794)
 Call ID: 7d284e06-00f5-40ba-b229-49d81580c794
  Args:
    source: :GeoffreyColman
    type: :Person
  AddTriple (7df7a6ed-a97d-491e-b8c4-bc72c08d2226)
 Call ID: 7df7a6ed-a97d-491e-b8c4-bc72c08d2226
  Args:
    target: :GeoffreyColman
    source: :TimothyColman
    relation: :hasFather
  Finish (b2e61ae1-e260-461a-8790-99d7b651dd63)
 Call ID: b2e61ae1-e260-461a-8790-99d7b651dd63
  Args: