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
Don Alessandro Torlonia, 5th Prince of Civitella-Cesi (7 December 1911 – 1 May/12 May 1986) was an Italian banking heir and a member of the House of Torlonia.
About

Born in Rome on 7 December 1911, Torlonia was the son of Marino Torlonia, 4th Prince di Civitella-Cesi and his American wife, Mary Elsie Moore.
Don Alessandro's youngest sister was Donna Marina Torlonia di Civitella-Cesi, grandmother of the American actress Brooke Shields.
In 1941, when his mother was dying in New York City, Torlonia took a high speed boat from Portugal and was arrested in error by FBI, thinking he was an enemy of the state and taken to Ellis Island.
Not to be confused with his cousin with the same name, Alessandro Torlonia (1925–2017), Prince of Fucino and Prince assistant to the papal throne, head of another branch of the family.
In the 1980s, this cousin Torlonia held the title as the "richest man in Rome", as he was the heir to a banking fortune and owner of the famous Torlonia Collection of ancient art.
He died in the Palazzo Nuñez-Torlonia, Rome, in 1986.
Marriage and children

On 14 January 1935, Don Alessandro morganatically married in Rome the Infanta Beatriz of Spain (1909–2002), a daughter of King Alfonso XIII of Spain and of Princess Victoria Eugenie of Battenberg.



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
  AssignClass (1c380639-8df9-4043-a3b7-e4e8ec3d7475)
 Call ID: 1c380639-8df9-4043-a3b7-e4e8ec3d7475
  Args:
    source: Don_Alessandro_Torlonia
    type: :Man
  AssignClass (8b316bef-966a-4a32-a432-95596eecb23f)
 Call ID: 8b316bef-966a-4a32-a432-95596eecb23f
  Args:
    source: Don_Alessandro_Torlonia
    type: :Person
  AddLiteral (8411733c-61f0-4865-b984-f2056e8e97ed)
 Call ID: 8411733c-61f0-4865-b984-f2056e8e97ed
  Args:
    source: Don_Alessandro_Torlonia
    literal_type: xsd:positiveInteger
    literal_value: 1911
    relation: :hasBirthYear
  AddLiteral (5b112671-9886-4c91-a004-5bc363495ad4)
 Call ID: 5b112671-9886-4c91-a004-5bc363495ad4
  Args:
    literal_value: 1986
    relation: :hasDeathYear
    source: Don_Alessandro_Torlonia
    literal_type: xsd:positiveInteger
  AssignClass (8b1744a4-f5f4-485b-a69b-3b04d65823b6)
 Call ID: 8b1744a4-f5f4-485b-a69b-3b04d65823b6
  Args:
    type: :Man
    source: Marino_Torlonia
  AssignClass (03612e28-493e-40d6-ada7-ff6ba3b6045b)
 Call ID: 03612e28-493e-40d6-ada7-ff6ba3b6045b
  Args:
    source: Marino_Torlonia
    type: :Person
  AssignClass (5e7bc89c-9168-41ed-9ff0-1b45a5394174)
 Call ID: 5e7bc89c-9168-41ed-9ff0-1b45a5394174
  Args:
    source: Mary_Elsie_Moore
    type: :Woman
  AssignClass (fe35887d-849d-4ff1-a0e0-e1d1f7972654)
 Call ID: fe35887d-849d-4ff1-a0e0-e1d1f7972654
  Args:
    type: :Person
    source: Mary_Elsie_Moore
  AddTriple (f7b394a7-3f50-4b1d-b97e-479bc356acc2)
 Call ID: f7b394a7-3f50-4b1d-b97e-479bc356acc2
  Args:
    target: Marino_Torlonia
    source: Don_Alessandro_Torlonia
    relation: :hasFather
  AddTriple (f744dd88-eb1c-403d-a52e-af09da8a4130)
 Call ID: f744dd88-eb1c-403d-a52e-af09da8a4130
  Args:
    relation: :hasMother
    target: Mary_Elsie_Moore
    source: Don_Alessandro_Torlonia
  AssignClass (b20e1e0f-0fe9-4ccb-8e9b-e6dfe995ba20)
 Call ID: b20e1e0f-0fe9-4ccb-8e9b-e6dfe995ba20
  Args:
    type: :Woman
    source: Donna_Marina_Torlonia
  AssignClass (9a02a2a4-4437-4528-95f4-e59d953e7b13)
 Call ID: 9a02a2a4-4437-4528-95f4-e59d953e7b13
  Args:
    source: Donna_Marina_Torlonia
    type: :Person
  AddTriple (a37b7218-e608-42b3-b055-0786a7dc8909)
 Call ID: a37b7218-e608-42b3-b055-0786a7dc8909
  Args:
    source: Don_Alessandro_Torlonia
    target: Donna_Marina_Torlonia
    relation: :hasSister
  AssignClass (02ed278f-46b8-440a-8769-55c8623f4978)
 Call ID: 02ed278f-46b8-440a-8769-55c8623f4978
  Args:
    type: :Woman
    source: Infanta_Beatriz_of_Spain
  AssignClass (57d1a81b-8a8b-4ed7-b71f-73f0d63474b1)
 Call ID: 57d1a81b-8a8b-4ed7-b71f-73f0d63474b1
  Args:
    source: Infanta_Beatriz_of_Spain
    type: :Person
  AddLiteral (0194dadd-422f-4986-b64a-704d2c199010)
 Call ID: 0194dadd-422f-4986-b64a-704d2c199010
  Args:
    relation: :hasMarriageYear
    literal_value: 1935
    source: Don_Alessandro_Torlonia
    literal_type: xsd:positiveInteger
  AddTriple (a6b8dcc0-40ad-45fa-9626-4a90058dcdee)
 Call ID: a6b8dcc0-40ad-45fa-9626-4a90058dcdee
  Args:
    source: Don_Alessandro_Torlonia
    target: Infanta_Beatriz_of_Spain
    relation: :hasRelation
  AssignClass (c15d1ee8-25ad-403b-b371-e11d8bf91f74)
 Call ID: c15d1ee8-25ad-403b-b371-e11d8bf91f74
  Args:
    source: King_Alfonso_XIII_of_Spain
    type: :Man
  AssignClass (624ed8ed-e39f-4349-8c84-046bde418a36)
 Call ID: 624ed8ed-e39f-4349-8c84-046bde418a36
  Args:
    type: :Person
    source: King_Alfonso_XIII_of_Spain
  AssignClass (716e21df-a230-49e2-bd51-731c8cd02925)
 Call ID: 716e21df-a230-49e2-bd51-731c8cd02925
  Args:
    type: :Woman
    source: Princess_Victoria_Eugenie_of_Battenberg
  AssignClass (666ada63-23ad-4715-8ea0-0494615d545b)
 Call ID: 666ada63-23ad-4715-8ea0-0494615d545b
  Args:
    source: Princess_Victoria_Eugenie_of_Battenberg
    type: :Person
  AddTriple (48b2a40b-5757-4885-bedb-2b1308ba1151)
 Call ID: 48b2a40b-5757-4885-bedb-2b1308ba1151
  Args:
    target: King_Alfonso_XIII_of_Spain
    source: Infanta_Beatriz_of_Spain
    relation: :hasFather
  AddTriple (f55db4d3-4cb9-4c7e-8a06-e2763d6ded75)
 Call ID: f55db4d3-4cb9-4c7e-8a06-e2763d6ded75
  Args:
    relation: :hasMother
    source: Infanta_Beatriz_of_Spain
    target: Princess_Victoria_Eugenie_of_Battenberg
  AssignClass (521cc542-67eb-4995-88a8-df952f9f66f3)
 Call ID: 521cc542-67eb-4995-88a8-df952f9f66f3
  Args:
    type: :Man
    source: Alessandro_Torlonia_cousin
  AssignClass (379244a4-fb20-463e-a63d-c352ef902508)
 Call ID: 379244a4-fb20-463e-a63d-c352ef902508
  Args:
    source: Alessandro_Torlonia_cousin
    type: :Person
  AddLiteral (146e1dc0-9dde-4d09-8124-d86a897f6b00)
 Call ID: 146e1dc0-9dde-4d09-8124-d86a897f6b00
  Args:
    literal_type: xsd:positiveInteger
    source: Alessandro_Torlonia_cousin
    relation: :hasBirthYear
    literal_value: 1925
  AddLiteral (6f45d721-3b3c-41b1-ad9a-5fd0048089be)
 Call ID: 6f45d721-3b3c-41b1-ad9a-5fd0048089be
  Args:
    literal_value: 2017
    relation: :hasDeathYear
    source: Alessandro_Torlonia_cousin
    literal_type: xsd:positiveInteger
  Finish (a379cfff-aee2-458f-a65b-9915d95f188a)
 Call ID: a379cfff-aee2-458f-a65b-9915d95f188a
  Args: