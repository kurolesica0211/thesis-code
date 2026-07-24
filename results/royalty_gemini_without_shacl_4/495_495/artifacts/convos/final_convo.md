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
Woizlawa Feodora Princess Reuss (née Duchess of Mecklenburg-Schwerin, 17 December 1918 – 3 June 2019) was a member of the German nobility, by birth of the House of Mecklenburg-Schwerin.
Her father was the seventh son of Frederick Francis II, Grand Duke of Mecklenburg-Schwerin (1823–1883) by his third wife Princess Marie of Schwarzburg-Rudolstadt (1850–1922).
Her mother was Viktoria Feodora Reuss zu Schleiz (1889–1918), the eldest child of Heinrich XXVII, Prince of Reuss zu Schleiz, regent of Principality of Reuss-Greiz and Princess Elise of Hohenlohe-Langenburg, granddaughter of Princess Feodora of Leiningen, half-sister of Queen Victoria.
She was a first cousin of:


Juliana's wedding

Preparations for the wedding of Queen Wilhelmina of the Netherlands' only child Crown Princess Juliana to the German Prince Bernhard of Lippe-Biesterfeld were underway in 1937 when a diplomatic scandal occurred.
These included Woizlawa herself (being first cousins), Duchess Thyra of Mecklenburg-Schwerin (her second cousin), Grand Duchess Kira Kirillovna of Russia (her first cousin once removed), Princess Sophie of Saxe-Weimar-Eisenach (her second cousin), and two of Bernhard's first cousins, Princess Sieglinde and Princess Elisabeth of Lippe.
Marriage and family

On 15 September 1939, she married in Bad Doberan to her distant relative Heinrich I Prinz Reuss (1910−1982), the eldest son of Prince Heinrich XXXIV Reuss of Schleiz (1887-1956) and his wife and cousin, Princess Sophie Renata Reuss of Köstritz (1884-1968).



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
  AssignClass (75bca7cc-2622-4ddf-9beb-0d8c0cee4bc9)
 Call ID: 75bca7cc-2622-4ddf-9beb-0d8c0cee4bc9
  Args:
    type: :Woman
    source: :Woizlawa_Feodora_Princess_Reuss
  AddLiteral (9157816e-b6a8-4d97-9512-ebce2ddfb4d3)
 Call ID: 9157816e-b6a8-4d97-9512-ebce2ddfb4d3
  Args:
    literal_value: 1918
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: :Woizlawa_Feodora_Princess_Reuss
  AddLiteral (dd195fd4-0b52-4444-a41f-8534f2b5d719)
 Call ID: dd195fd4-0b52-4444-a41f-8534f2b5d719
  Args:
    literal_type: xsd:integer
    source: :Woizlawa_Feodora_Princess_Reuss
    literal_value: 2019
    relation: :hasDeathYear
  AssignClass (3d7efa3f-1974-4caf-aac2-603850026ff3)
 Call ID: 3d7efa3f-1974-4caf-aac2-603850026ff3
  Args:
    type: :Man
    source: :Frederick_Francis_II
  AddLiteral (93b615e4-9083-4dd2-a50a-91617b848bef)
 Call ID: 93b615e4-9083-4dd2-a50a-91617b848bef
  Args:
    source: :Frederick_Francis_II
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1823
  AddLiteral (3a7c16b5-2ad0-4e15-8aea-9f509a941d07)
 Call ID: 3a7c16b5-2ad0-4e15-8aea-9f509a941d07
  Args:
    source: :Frederick_Francis_II
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1883
  AssignClass (e659dbf2-4ad0-4e23-a65d-79f6a585537e)
 Call ID: e659dbf2-4ad0-4e23-a65d-79f6a585537e
  Args:
    type: :Woman
    source: :Princess_Marie_of_Schwarzburg-Rudolstadt
  AddLiteral (ebcaac21-c3e1-4f07-bdde-4d51067d90ac)
 Call ID: ebcaac21-c3e1-4f07-bdde-4d51067d90ac
  Args:
    relation: :hasBirthYear
    literal_value: 1850
    source: :Princess_Marie_of_Schwarzburg-Rudolstadt
    literal_type: xsd:integer
  AddLiteral (ef6d30c8-4c11-4acb-accf-60bf3fa47a05)
 Call ID: ef6d30c8-4c11-4acb-accf-60bf3fa47a05
  Args:
    literal_value: 1922
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: :Princess_Marie_of_Schwarzburg-Rudolstadt
  AddTriple (c13f380c-b0d7-494a-8f95-6121ebefaac6)
 Call ID: c13f380c-b0d7-494a-8f95-6121ebefaac6
  Args:
    source: :Frederick_Francis_II
    relation: :isFatherOf
    target: :Woizlawa_Father
  AddTriple (ed31bae9-5afd-4a95-a6d8-de8225868e3c)
 Call ID: ed31bae9-5afd-4a95-a6d8-de8225868e3c
  Args:
    target: :Woizlawa_Father
    source: :Princess_Marie_of_Schwarzburg-Rudolstadt
    relation: :isMotherOf
  AssignClass (2ba2215f-1f4e-4417-9591-ed30f7ad95a1)
 Call ID: 2ba2215f-1f4e-4417-9591-ed30f7ad95a1
  Args:
    type: :Man
    source: :Woizlawa_Father
  AddTriple (d38e1368-24d9-4f70-8fcf-37d807265a5c)
 Call ID: d38e1368-24d9-4f70-8fcf-37d807265a5c
  Args:
    target: :Woizlawa_Father
    source: :Woizlawa_Feodora_Princess_Reuss
    relation: :hasFather
  AssignClass (c4430365-3438-4c20-b326-3eef7a09024f)
 Call ID: c4430365-3438-4c20-b326-3eef7a09024f
  Args:
    type: :Woman
    source: :Viktoria_Feodora_Reuss_zu_Schleiz
  AddLiteral (370b19f8-83e6-42fe-8a54-452d03ab89c5)
 Call ID: 370b19f8-83e6-42fe-8a54-452d03ab89c5
  Args:
    literal_value: 1889
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: :Viktoria_Feodora_Reuss_zu_Schleiz
  AddLiteral (faad7ee5-24a6-4e92-9db6-49ecab186748)
 Call ID: faad7ee5-24a6-4e92-9db6-49ecab186748
  Args:
    relation: :hasDeathYear
    literal_value: 1918
    source: :Viktoria_Feodora_Reuss_zu_Schleiz
    literal_type: xsd:integer
  AddTriple (9c3ab36e-18dd-47a7-8704-31336a37b25e)
 Call ID: 9c3ab36e-18dd-47a7-8704-31336a37b25e
  Args:
    relation: :hasMother
    source: :Woizlawa_Feodora_Princess_Reuss
    target: :Viktoria_Feodora_Reuss_zu_Schleiz
  AssignClass (3eb55516-7cf5-4de6-ba5b-4559b688ff40)
 Call ID: 3eb55516-7cf5-4de6-ba5b-4559b688ff40
  Args:
    type: :Man
    source: :Heinrich_XXVII_Prince_of_Reuss_zu_Schleiz
  AssignClass (d9a9c1ba-d4c1-4d38-abc8-f34acbb7241c)
 Call ID: d9a9c1ba-d4c1-4d38-abc8-f34acbb7241c
  Args:
    type: :Woman
    source: :Princess_Elise_of_Hohenlohe-Langenburg
  AddTriple (a276852f-4cbb-46c2-8e6c-458e805af593)
 Call ID: a276852f-4cbb-46c2-8e6c-458e805af593
  Args:
    target: :Viktoria_Feodora_Reuss_zu_Schleiz
    source: :Heinrich_XXVII_Prince_of_Reuss_zu_Schleiz
    relation: :isFatherOf
  AddTriple (25d2793a-26d2-4bdd-a855-d1983075e049)
 Call ID: 25d2793a-26d2-4bdd-a855-d1983075e049
  Args:
    target: :Viktoria_Feodora_Reuss_zu_Schleiz
    relation: :isMotherOf
    source: :Princess_Elise_of_Hohenlohe-Langenburg
  AssignClass (69495829-80dc-4bc9-b9a1-cb225362b5ae)
 Call ID: 69495829-80dc-4bc9-b9a1-cb225362b5ae
  Args:
    type: :Man
    source: :Heinrich_I_Prinz_Reuss
  AddLiteral (01eeb94a-bb6b-4394-ab51-47fa823fb678)
 Call ID: 01eeb94a-bb6b-4394-ab51-47fa823fb678
  Args:
    relation: :hasBirthYear
    literal_value: 1910
    source: :Heinrich_I_Prinz_Reuss
    literal_type: xsd:integer
  AddLiteral (2844e06f-4874-4b0f-8fa1-f0b954ff354a)
 Call ID: 2844e06f-4874-4b0f-8fa1-f0b954ff354a
  Args:
    relation: :hasDeathYear
    literal_value: 1982
    source: :Heinrich_I_Prinz_Reuss
    literal_type: xsd:integer
  AddLiteral (58a9396c-1513-41f5-a192-3d7e18b912ae)
 Call ID: 58a9396c-1513-41f5-a192-3d7e18b912ae
  Args:
    literal_value: 1939
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: :Woizlawa_Feodora_Princess_Reuss
  AddTriple (67663189-ac87-4461-84dd-1eeac9f23293)
 Call ID: 67663189-ac87-4461-84dd-1eeac9f23293
  Args:
    source: :Woizlawa_Feodora_Princess_Reuss
    relation: :hasRelation
    target: :Heinrich_I_Prinz_Reuss
  AssignClass (6c623524-ba61-4336-a1ab-c5fde06d9cdd)
 Call ID: 6c623524-ba61-4336-a1ab-c5fde06d9cdd
  Args:
    type: :Man
    source: :Prince_Heinrich_XXXIV_Reuss_of_Schleiz
  AddLiteral (9464ab20-d0a5-4908-b950-b423a3eeccaf)
 Call ID: 9464ab20-d0a5-4908-b950-b423a3eeccaf
  Args:
    literal_type: xsd:integer
    source: :Prince_Heinrich_XXXIV_Reuss_of_Schleiz
    literal_value: 1887
    relation: :hasBirthYear
  AddLiteral (8fc698e4-eb66-4e58-bafa-c177c79b51f7)
 Call ID: 8fc698e4-eb66-4e58-bafa-c177c79b51f7
  Args:
    literal_type: xsd:integer
    source: :Prince_Heinrich_XXXIV_Reuss_of_Schleiz
    literal_value: 1956
    relation: :hasDeathYear
  AssignClass (3382526f-c01c-41b0-b3b7-847bc5b48e8c)
 Call ID: 3382526f-c01c-41b0-b3b7-847bc5b48e8c
  Args:
    type: :Woman
    source: :Princess_Sophie_Renata_Reuss_of_Köstritz
  AddLiteral (e6ae502f-bc0a-425f-9e4b-42a41d7331d7)
 Call ID: e6ae502f-bc0a-425f-9e4b-42a41d7331d7
  Args:
    literal_type: xsd:integer
    source: :Princess_Sophie_Renata_Reuss_of_Köstritz
    literal_value: 1884
    relation: :hasBirthYear
  AddLiteral (0bcfe66a-fbf9-4ada-a632-b44799bfb77f)
 Call ID: 0bcfe66a-fbf9-4ada-a632-b44799bfb77f
  Args:
    source: :Princess_Sophie_Renata_Reuss_of_Köstritz
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1968
  AddTriple (107164f3-ee3b-4053-9672-bd6a4282bbf1)
 Call ID: 107164f3-ee3b-4053-9672-bd6a4282bbf1
  Args:
    source: :Heinrich_I_Prinz_Reuss
    relation: :hasFather
    target: :Prince_Heinrich_XXXIV_Reuss_of_Schleiz
  AddTriple (f5a9a8d0-081f-48e1-b3df-0cd4ddf6cb21)
 Call ID: f5a9a8d0-081f-48e1-b3df-0cd4ddf6cb21
  Args:
    source: :Heinrich_I_Prinz_Reuss
    relation: :hasMother
    target: :Princess_Sophie_Renata_Reuss_of_Köstritz
  Finish (96344ed2-5094-4de4-bd77-05d75704feaa)
 Call ID: 96344ed2-5094-4de4-bd77-05d75704feaa
  Args: