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
Princess Sophie Louise of Saxe-Weimar-Eisenach (20 March 1911 – 21 November 1988) was a princess of the House of Saxe-Weimar-Eisenach.
She was born in Weimar, the eldest child and only daughter of William Ernest, Grand Duke of Saxe-Weimar-Eisenach, by his second wife, Princess Feodora of Saxe-Meiningen.
As a relative of Wilhelmina of the Netherlands, Sophie was invited to the 1937 wedding of her daughter, Princess Juliana, as a bridesmaid.
She became entangled in a diplomatic scandal however after the passports of Sophie and two other German princesses were withheld by the Nazi government.
Though they were later released, Sophie opted out of attending at the last moment.
In 1938 Sophie married Friedrich Günther, Prince of Schwarzburg, but the couple were divorced by the end of the year.
Juliana's wedding

Invitation

Preparations for the wedding of Queen Wilhelmina of the Netherlands's only child Crown Princess Juliana to the German Prince Bernhard of Lippe-Biesterfeld were under way in 1937 when a small diplomatic scandal occurred.
These included Sophie herself (her and Bernhard's second cousin), Duchess Thyra of Mecklenburg-Schwerin (her second cousin), Grand Duchess Kira Kirillovna of Russia (her first cousin once removed), Duchess Woizlawa of Mecklenburg (her cousin), and two of Bernhard's first cousins, Princess Sieglinde of Lippe and Princess Elisabeth of Lippe.
Diplomatic scandal

Sophie became entangled in the small diplomatic scandal as preparations for the Dutch wedding commenced.
The German Nazi government, apparently outraged that their flag was not used in festivities related to the wedding, refused to release the passports of Sophie, along with those of Bernard's cousins Princesses Sieglinde and Elizabeth zur Lippe.
Though the passports were released, Sophie for unknown reasons revoked her acceptance and stated she could no longer attend the wedding at the last moment.
Princess Sophie was replaced as bridesmaid by Baroness von Heeckeren van Kell, one of Juliana's ladies-in-waiting.
Marriage

On 7 March 1938 at Heinrichau, Schlesien, Sophie married Friedrich Günther, Prince of Schwarzburg.
Consequently, his sister Marie Antoinette controversially succeeded him as Princess of Schwarzburg.
Sophie died on 21 November 1988 in Hamburg.



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
  AssignClass (14eaaf32-0880-490c-925d-003641ccd8d6)
 Call ID: 14eaaf32-0880-490c-925d-003641ccd8d6
  Args:
    type: :Woman
    source: :Sophie_Louise_of_Saxe-Weimar-Eisenach
  AssignClass (2235ab05-c437-4cbe-983e-9911e1287f25)
 Call ID: 2235ab05-c437-4cbe-983e-9911e1287f25
  Args:
    source: :Sophie_Louise_of_Saxe-Weimar-Eisenach
    type: :Person
  AddLiteral (d96eceb6-6fc1-4520-af70-c8c40ef17cac)
 Call ID: d96eceb6-6fc1-4520-af70-c8c40ef17cac
  Args:
    relation: :hasBirthYear
    literal_value: 1911
    source: :Sophie_Louise_of_Saxe-Weimar-Eisenach
    literal_type: xsd:integer
  AddLiteral (b0fa6154-e2c1-41c2-af4e-ea864f597485)
 Call ID: b0fa6154-e2c1-41c2-af4e-ea864f597485
  Args:
    source: :Sophie_Louise_of_Saxe-Weimar-Eisenach
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1988
  AssignClass (4a510490-6c93-43b4-8581-d6d3485b1fef)
 Call ID: 4a510490-6c93-43b4-8581-d6d3485b1fef
  Args:
    type: :Man
    source: :William_Ernest_Grand_Duke_of_Saxe-Weimar-Eisenach
  AssignClass (4a3d9bc8-96e6-4790-a2e2-3a58ec06b047)
 Call ID: 4a3d9bc8-96e6-4790-a2e2-3a58ec06b047
  Args:
    type: :Person
    source: :William_Ernest_Grand_Duke_of_Saxe-Weimar-Eisenach
  AssignClass (12b37d5d-567f-4d09-a9f8-9a20d4440b26)
 Call ID: 12b37d5d-567f-4d09-a9f8-9a20d4440b26
  Args:
    source: :William_Ernest_Grand_Duke_of_Saxe-Weimar-Eisenach
    type: :Ancestor
  AssignClass (22e5d161-0450-4c4b-8f30-198d400eb685)
 Call ID: 22e5d161-0450-4c4b-8f30-198d400eb685
  Args:
    source: :Feodora_of_Saxe-Meiningen
    type: :Woman
  AssignClass (6d1934be-66d6-4682-88f8-37d0cfc7e74c)
 Call ID: 6d1934be-66d6-4682-88f8-37d0cfc7e74c
  Args:
    source: :Feodora_of_Saxe-Meiningen
    type: :Person
  AssignClass (95f38dab-917b-4853-8253-c3da3ffdd37f)
 Call ID: 95f38dab-917b-4853-8253-c3da3ffdd37f
  Args:
    type: :Ancestor
    source: :Feodora_of_Saxe-Meiningen
  AddTriple (815839f7-5da9-46f6-bf3b-97bde5aee926)
 Call ID: 815839f7-5da9-46f6-bf3b-97bde5aee926
  Args:
    relation: :hasFather
    source: :Sophie_Louise_of_Saxe-Weimar-Eisenach
    target: :William_Ernest_Grand_Duke_of_Saxe-Weimar-Eisenach
  AddTriple (54de5d5b-78ae-428a-ae91-d0aa63e7da4b)
 Call ID: 54de5d5b-78ae-428a-ae91-d0aa63e7da4b
  Args:
    relation: :hasMother
    target: :Feodora_of_Saxe-Meiningen
    source: :Sophie_Louise_of_Saxe-Weimar-Eisenach
  AssignClass (9b9d2a59-d91c-48c0-8363-6a4f3895f65f)
 Call ID: 9b9d2a59-d91c-48c0-8363-6a4f3895f65f
  Args:
    type: :Man
    source: :Friedrich_Gunther_Prince_of_Schwarzburg
  AssignClass (fc2920d8-abe9-4624-8dd6-a161dcfd40c2)
 Call ID: fc2920d8-abe9-4624-8dd6-a161dcfd40c2
  Args:
    type: :Person
    source: :Friedrich_Gunther_Prince_of_Schwarzburg
  AddLiteral (bdf01493-0b00-4a32-819f-647a72b7757e)
 Call ID: bdf01493-0b00-4a32-819f-647a72b7757e
  Args:
    literal_type: xsd:integer
    source: :Sophie_Louise_of_Saxe-Weimar-Eisenach
    relation: :hasMarriageYear
    literal_value: 1938
  AddTriple (9ee8e01f-c5ce-49f5-b839-7305538863f8)
 Call ID: 9ee8e01f-c5ce-49f5-b839-7305538863f8
  Args:
    source: :Sophie_Louise_of_Saxe-Weimar-Eisenach
    target: :Friedrich_Gunther_Prince_of_Schwarzburg
    relation: :hasRelation
  AssignClass (2c797bd8-d6db-479e-89d0-fa3ef76f3768)
 Call ID: 2c797bd8-d6db-479e-89d0-fa3ef76f3768
  Args:
    source: :Marie_Antoinette_of_Schwarzburg
    type: :Woman
  AssignClass (fba8cd7b-7cb3-4105-be46-681946098b57)
 Call ID: fba8cd7b-7cb3-4105-be46-681946098b57
  Args:
    source: :Marie_Antoinette_of_Schwarzburg
    type: :Person
  AddTriple (96ba62ee-8c4d-46af-ad05-916c9c72e477)
 Call ID: 96ba62ee-8c4d-46af-ad05-916c9c72e477
  Args:
    relation: :hasSister
    source: :Friedrich_Gunther_Prince_of_Schwarzburg
    target: :Marie_Antoinette_of_Schwarzburg
  Finish (5753f21b-fb4c-40e9-9b3b-22b6c42ac8be)
 Call ID: 5753f21b-fb4c-40e9-9b3b-22b6c42ac8be
  Args: