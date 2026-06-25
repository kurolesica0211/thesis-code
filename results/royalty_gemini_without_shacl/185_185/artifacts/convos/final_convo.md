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
Queen Anne-Marie


Queen Sofía of Spain


Marina, consort of Prince Michael


The Duke of AostaThe Duchess of Aosta


The Dowager Duchess of Aosta


Princess Olga Isabelle of Savoy-Aosta, Duchess of Aosta (née Princess Olga of Greece;
Greek: Πριγκίπισσα Όλγα της Ελλάδας; born 11 November 1971), is the younger daughter of author Prince Michael of Greece and Denmark and Marina Karella, an artist and daughter of the Greek business magnate Theódoros Karéllas.
Olga is married to her second cousin Prince Aimone, Duke of Aosta.
Early life

Princess Olga was born on 11 November 1971 in Athens, Greece.
She is the younger sister of Princess Alexandra and grew up in Paris and New York, spending summers at the family's island retreat at Patmos, Greece.
Although Olga worked for a while in interior decoration, she went to Panama to photograph and study phalaena.
As Princess Olga's parents' marriage is morganatic, and therefore non-dynastic, she is a Greek princess by birth but not a Danish princess, used the style Her Highness instead of Her Royal Highness (until her marriage), and is excluded from the line of succession to the former Greek throne.
Engagement, marriage and children

Olga's engagement to Prince Aimone of Savoy, son of Amedeo, 5th Duke of Aosta, was announced in May 2005.
Aimone and Olga are second cousins; both being great-grandchildren of the French pretender Jean d'Orléans, duc de Guise.
They are also second cousins once removed as George I of Greece is Aimone's great-great-grandfather and Olga's great-grandfather.
Olga's father, Prince Michael of Greece and Denmark, Aimone's paternal grandmother, Princess Irene, Duchess of Aosta (née Princess Irene of Greece and Denmark), and Prince Philip, Duke of Edinburgh (born Prince Philip of Greece and Denmark), were all first cousins.
A canonical dispensation was obtained from the Catholic Archbishop of Moscow, Monsignor Paolo Pezzi, who was the local Ordinary of prince Aimone.
On 7 March 2009, Princess Olga gave birth to a son named Umberto in Paris, France.
On 24 May 2011 in Paris, Olga gave birth to another son, named Amedeo Michele.
On 14 December 2012, Olga gave birth to a baby daughter, Isabella Vita Marina, in Paris, France.



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
  AssignClass (90927920-b45c-41a2-b36c-b5e05a97ff73)
 Call ID: 90927920-b45c-41a2-b36c-b5e05a97ff73
  Args:
    type: :Woman
    source: Princess Olga of Greece
  AssignClass (be35377d-bb7f-4329-981b-6de3c00a3bc4)
 Call ID: be35377d-bb7f-4329-981b-6de3c00a3bc4
  Args:
    source: Prince Michael of Greece and Denmark
    type: :Man
  AssignClass (9bfe1090-a7ba-412c-b914-b058b8f779b5)
 Call ID: 9bfe1090-a7ba-412c-b914-b058b8f779b5
  Args:
    type: :Woman
    source: Marina Karella
  AssignClass (3a308a73-7b81-458d-a282-6b3ae4485f66)
 Call ID: 3a308a73-7b81-458d-a282-6b3ae4485f66
  Args:
    source: Prince Aimone, Duke of Aosta
    type: :Man
  AssignClass (4ca75584-29c8-4f35-ae6e-988b15b156d6)
 Call ID: 4ca75584-29c8-4f35-ae6e-988b15b156d6
  Args:
    source: Amedeo, 5th Duke of Aosta
    type: :Man
  AssignClass (a7748edd-4cf7-405e-9bdc-27cceb447656)
 Call ID: a7748edd-4cf7-405e-9bdc-27cceb447656
  Args:
    type: :Woman
    source: Princess Alexandra
  AssignClass (0c9b9d35-4269-4c44-885a-ee4065480c74)
 Call ID: 0c9b9d35-4269-4c44-885a-ee4065480c74
  Args:
    type: :Man
    source: Umberto
  AssignClass (2fdc5e4f-f6df-4eff-871c-2671990b83ca)
 Call ID: 2fdc5e4f-f6df-4eff-871c-2671990b83ca
  Args:
    source: Amedeo Michele
    type: :Man
  AssignClass (ac7a2bf7-617d-4fa8-b2df-e035bbbe6bdd)
 Call ID: ac7a2bf7-617d-4fa8-b2df-e035bbbe6bdd
  Args:
    type: :Woman
    source: Isabella Vita Marina
  AssignClass (5b9b0654-81d7-4a66-ae86-284e6aae925f)
 Call ID: 5b9b0654-81d7-4a66-ae86-284e6aae925f
  Args:
    type: :Man
    source: Theódoros Karéllas
  AddTriple (e6c6591f-cc73-4965-883e-a43437990e8f)
 Call ID: e6c6591f-cc73-4965-883e-a43437990e8f
  Args:
    source: Princess Olga of Greece
    relation: :hasFather
    target: Prince Michael of Greece and Denmark
  AddTriple (ab52608f-9c43-4e14-acc7-bf6b9edbf8e0)
 Call ID: ab52608f-9c43-4e14-acc7-bf6b9edbf8e0
  Args:
    target: Marina Karella
    relation: :hasMother
    source: Princess Olga of Greece
  AddTriple (0b6693b5-23b9-4384-ba2c-5cb7e3cc7ee1)
 Call ID: 0b6693b5-23b9-4384-ba2c-5cb7e3cc7ee1
  Args:
    source: Marina Karella
    relation: :hasFather
    target: Theódoros Karéllas
  AddTriple (1b93b0b8-3345-431c-9879-a0fef81cc9ce)
 Call ID: 1b93b0b8-3345-431c-9879-a0fef81cc9ce
  Args:
    relation: :hasFather
    source: Prince Aimone, Duke of Aosta
    target: Amedeo, 5th Duke of Aosta
  AddTriple (b50fe6ed-9831-4892-9180-c5a401477904)
 Call ID: b50fe6ed-9831-4892-9180-c5a401477904
  Args:
    source: Princess Olga of Greece
    relation: :hasSister
    target: Princess Alexandra
  AddTriple (5b6c1ee3-1561-4920-838d-c8d3727a5f6e)
 Call ID: 5b6c1ee3-1561-4920-838d-c8d3727a5f6e
  Args:
    target: Prince Michael of Greece and Denmark
    source: Princess Alexandra
    relation: :hasFather
  AddTriple (10a6d793-586c-4f32-a68d-d132343a291c)
 Call ID: 10a6d793-586c-4f32-a68d-d132343a291c
  Args:
    target: Marina Karella
    source: Princess Alexandra
    relation: :hasMother
  AddTriple (b4a6d327-3fb7-48b6-9d58-5aeaf6d41b66)
 Call ID: b4a6d327-3fb7-48b6-9d58-5aeaf6d41b66
  Args:
    target: Princess Olga of Greece
    relation: :hasMother
    source: Umberto
  AddTriple (a909d32e-608f-4293-b238-77ce331862c4)
 Call ID: a909d32e-608f-4293-b238-77ce331862c4
  Args:
    target: Prince Aimone, Duke of Aosta
    relation: :hasFather
    source: Umberto
  AddTriple (a969ef8b-9892-4ba8-b9bf-5dc1b48e8d0e)
 Call ID: a969ef8b-9892-4ba8-b9bf-5dc1b48e8d0e
  Args:
    target: Princess Olga of Greece
    relation: :hasMother
    source: Amedeo Michele
  AddTriple (2e9e1f98-c0f6-41a9-884b-b8f57ce96209)
 Call ID: 2e9e1f98-c0f6-41a9-884b-b8f57ce96209
  Args:
    relation: :hasFather
    source: Amedeo Michele
    target: Prince Aimone, Duke of Aosta
  AddTriple (ec3f05c6-b027-419c-8bf5-863667ee763a)
 Call ID: ec3f05c6-b027-419c-8bf5-863667ee763a
  Args:
    source: Isabella Vita Marina
    relation: :hasMother
    target: Princess Olga of Greece
  AddTriple (55edcc7d-b4e9-4494-9830-b093693068a5)
 Call ID: 55edcc7d-b4e9-4494-9830-b093693068a5
  Args:
    target: Prince Aimone, Duke of Aosta
    source: Isabella Vita Marina
    relation: :hasFather
  AddLiteral (7b0370b7-3a2c-4909-8c0d-dce2ce85b92f)
 Call ID: 7b0370b7-3a2c-4909-8c0d-dce2ce85b92f
  Args:
    literal_value: 1971
    source: Princess Olga of Greece
    relation: :hasBirthYear
    literal_type: xsd:integer
  Finish (cc4029bc-1f7a-4af3-8f94-b7cfceb5b6b4)
 Call ID: cc4029bc-1f7a-4af3-8f94-b7cfceb5b6b4
  Args: