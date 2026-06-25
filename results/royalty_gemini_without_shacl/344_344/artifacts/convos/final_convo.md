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
Princess Françoise d'Orléans (Françoise Isabelle Louise Marie; 25 December 1902 - 25 February 1953) was born an Orléans Princess of France and became a Princess of Greece and Denmark by marriage.
She was thus a member of the Greek royal family and a descendant of the "Citizen-King" Louis Philippe I.


Life

Françoise d'Orléans was born in Paris, the second daughter of Jean d'Orléans, duc de Guise (an Orléanist pretender to the throne of France under the name Jean III) and his wife, the French Princess Isabelle of Orléans.
Françoise's brother, Prince Henri, Count of Paris, succeeded their father as the Orleanist pretender, under the name Henri VI.
In Palermo on 11 February 1929, she married Prince Christopher of Greece and Denmark (1888–1940).
This was Christopher's second marriage - he was the youngest son of King George I of Greece (1845–1913) and his wife, Grand Duchess Olga Constantinovna of Russia (1851–1926).
Through his father, he was thus a grandson of King Christian IX of Denmark (1818–1906), nicknamed "the father-in-law of Europe" due to his six children all marrying into other royal families.
They had only one child, the writer Prince Michael of Greece and Denmark (1939–2024), whose marriage to the Greek artist Marina Karella (born 1940) did not conform to the laws of the royal house and thus deprived him of all right of succession to the Greek throne.
She is grandmother of Princess Alexandra of Greece, an artist, art collector, arts patron, and child life specialist.
Her other grand-daughter is Princess Olga of Greece, who married Prince Aimone of Savoy-Aosta, one of two claimants to be Head of the House of Savoy.
The civil war in Greece was preventing her from entering, and the British government refused to grant her asylum.
Françoise and her son Michael went to Paris, where they lived in the home of Princess Isabella and her second husband, Prince Pierre Murat.
Françoise did not want to see anyone in their residence and rarely left her rooms.
She is buried alongside her husband in Tatoi Royal Cemetery, Greece.



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
  AssignClass (7975fb39-1adc-4252-a89e-b90b6c302f46)
 Call ID: 7975fb39-1adc-4252-a89e-b90b6c302f46
  Args:
    type: :Woman
    source: :FrancoiseDOrleans
  AddLiteral (09d2f776-5401-4ea7-bfa1-2f31baa02283)
 Call ID: 09d2f776-5401-4ea7-bfa1-2f31baa02283
  Args:
    source: :FrancoiseDOrleans
    literal_value: 1902
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (d5066386-b666-4237-82e9-bdfac9467774)
 Call ID: d5066386-b666-4237-82e9-bdfac9467774
  Args:
    literal_value: 1953
    source: :FrancoiseDOrleans
    literal_type: xsd:integer
    relation: :hasDeathYear
  AssignClass (79259602-d6f7-46fe-b373-d65fd3bc620e)
 Call ID: 79259602-d6f7-46fe-b373-d65fd3bc620e
  Args:
    source: :JeanDOrleansDucDeGuise
    type: :Man
  AssignClass (660378f9-dc01-402b-943d-7c4d34cfd25b)
 Call ID: 660378f9-dc01-402b-943d-7c4d34cfd25b
  Args:
    type: :Woman
    source: :IsabelleDOrleans
  AddTriple (01657bfc-766d-4c0d-a2e9-3c0951d5a6ab)
 Call ID: 01657bfc-766d-4c0d-a2e9-3c0951d5a6ab
  Args:
    source: :JeanDOrleansDucDeGuise
    target: :FrancoiseDOrleans
    relation: :isFatherOf
  AddTriple (b0727400-8173-4bcd-a388-7afc7acab7d5)
 Call ID: b0727400-8173-4bcd-a388-7afc7acab7d5
  Args:
    source: :IsabelleDOrleans
    target: :FrancoiseDOrleans
    relation: :isMotherOf
  AssignClass (0dda4788-f144-49e4-952a-ad4e20c8ef59)
 Call ID: 0dda4788-f144-49e4-952a-ad4e20c8ef59
  Args:
    type: :Man
    source: :PrinceHenriCountOfParis
  AddTriple (d86f2c46-e7d2-4a7c-8bac-982f13a9be5e)
 Call ID: d86f2c46-e7d2-4a7c-8bac-982f13a9be5e
  Args:
    target: :PrinceHenriCountOfParis
    source: :FrancoiseDOrleans
    relation: :isSiblingOf
  AddTriple (60392ca2-20da-4542-9297-17272d124e73)
 Call ID: 60392ca2-20da-4542-9297-17272d124e73
  Args:
    relation: :isFatherOf
    target: :PrinceHenriCountOfParis
    source: :JeanDOrleansDucDeGuise
  AssignClass (df988802-51e6-4fe0-ab99-6d4b6d0e8953)
 Call ID: df988802-51e6-4fe0-ab99-6d4b6d0e8953
  Args:
    type: :Man
    source: :PrinceChristopherOfGreeceAndDenmark
  AddLiteral (bffb37fe-f6fc-4e87-9c5b-e73b5d6d2f65)
 Call ID: bffb37fe-f6fc-4e87-9c5b-e73b5d6d2f65
  Args:
    source: :PrinceChristopherOfGreeceAndDenmark
    literal_value: 1888
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (9f3c908f-0545-40fc-9203-1dd7b9f54841)
 Call ID: 9f3c908f-0545-40fc-9203-1dd7b9f54841
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: :PrinceChristopherOfGreeceAndDenmark
    literal_value: 1940
  AddLiteral (6a6ac8ba-1a9a-4413-8c2f-cafb484f9942)
 Call ID: 6a6ac8ba-1a9a-4413-8c2f-cafb484f9942
  Args:
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: :FrancoiseDOrleans
    literal_value: 1929
  AddTriple (bee3a5da-6e0b-4c98-9486-fd2d67b2b8fa)
 Call ID: bee3a5da-6e0b-4c98-9486-fd2d67b2b8fa
  Args:
    target: :PrinceChristopherOfGreeceAndDenmark
    source: :FrancoiseDOrleans
    relation: :hasRelation
  AssignClass (edfa085a-6812-4b52-b23f-45bf16da796e)
 Call ID: edfa085a-6812-4b52-b23f-45bf16da796e
  Args:
    source: :KingGeorgeIOfGreece
    type: :Man
  AssignClass (26625805-d422-4216-a60e-35b30c60222c)
 Call ID: 26625805-d422-4216-a60e-35b30c60222c
  Args:
    source: :GrandDuchessOlgaConstantinovnaOfRussia
    type: :Woman
  AddTriple (eafa4654-1e2e-4930-8619-d4d8f9d53b16)
 Call ID: eafa4654-1e2e-4930-8619-d4d8f9d53b16
  Args:
    target: :PrinceChristopherOfGreeceAndDenmark
    source: :KingGeorgeIOfGreece
    relation: :isFatherOf
  AddTriple (e290f75d-4393-4f11-814c-d9559fe8c981)
 Call ID: e290f75d-4393-4f11-814c-d9559fe8c981
  Args:
    relation: :isMotherOf
    source: :GrandDuchessOlgaConstantinovnaOfRussia
    target: :PrinceChristopherOfGreeceAndDenmark
  AssignClass (1fe964ed-bd4c-4935-94f6-1112ad920414)
 Call ID: 1fe964ed-bd4c-4935-94f6-1112ad920414
  Args:
    type: :Man
    source: :KingChristianIXOfDenmark
  AddTriple (4594d119-3de0-438b-ae8f-de1ea6d8b811)
 Call ID: 4594d119-3de0-438b-ae8f-de1ea6d8b811
  Args:
    relation: :isFatherOf
    source: :KingChristianIXOfDenmark
    target: :KingGeorgeIOfGreece
  AssignClass (c4b5fd21-6d63-493c-a1e0-1313f9c350ba)
 Call ID: c4b5fd21-6d63-493c-a1e0-1313f9c350ba
  Args:
    source: :PrinceMichaelOfGreeceAndDenmark
    type: :Man
  AddLiteral (9657b78a-acfe-4291-9531-394847084ce6)
 Call ID: 9657b78a-acfe-4291-9531-394847084ce6
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: :PrinceMichaelOfGreeceAndDenmark
    literal_value: 1939
  AddLiteral (3f6272f0-17d8-400a-898e-dd7cb1d21539)
 Call ID: 3f6272f0-17d8-400a-898e-dd7cb1d21539
  Args:
    literal_value: 2024
    source: :PrinceMichaelOfGreeceAndDenmark
    literal_type: xsd:integer
    relation: :hasDeathYear
  AddTriple (cb3623c4-dba6-4240-904d-523ca0871453)
 Call ID: cb3623c4-dba6-4240-904d-523ca0871453
  Args:
    target: :FrancoiseDOrleans
    source: :PrinceMichaelOfGreeceAndDenmark
    relation: :isChildOf
  AddTriple (95deb77a-2b2c-40f7-a58e-623711fe9fc1)
 Call ID: 95deb77a-2b2c-40f7-a58e-623711fe9fc1
  Args:
    relation: :isChildOf
    source: :PrinceMichaelOfGreeceAndDenmark
    target: :PrinceChristopherOfGreeceAndDenmark
  AssignClass (e2cdbf3c-5be1-484d-8773-cc633e182336)
 Call ID: e2cdbf3c-5be1-484d-8773-cc633e182336
  Args:
    source: :MarinaKarella
    type: :Woman
  AddTriple (aa0876f1-8fad-47a9-beac-2de1d484bb73)
 Call ID: aa0876f1-8fad-47a9-beac-2de1d484bb73
  Args:
    relation: :hasRelation
    target: :MarinaKarella
    source: :PrinceMichaelOfGreeceAndDenmark
  AssignClass (b62f8f91-b718-43ce-839d-6284b2a88167)
 Call ID: b62f8f91-b718-43ce-839d-6284b2a88167
  Args:
    source: :PrincessAlexandraOfGreece
    type: :Woman
  AssignClass (9bab29e4-8e90-4e9d-8ee5-3cedec55740f)
 Call ID: 9bab29e4-8e90-4e9d-8ee5-3cedec55740f
  Args:
    source: :PrincessOlgaOfGreece
    type: :Woman
  AddTriple (91bd27a2-a8c1-4aea-ae11-1bb05bb8a2b4)
 Call ID: 91bd27a2-a8c1-4aea-ae11-1bb05bb8a2b4
  Args:
    relation: :isMotherOf
    source: :PrinceMichaelOfGreeceAndDenmark
    target: :PrincessAlexandraOfGreece
  AddTriple (e55429b4-3060-408c-b1c8-6fa26b9a7877)
 Call ID: e55429b4-3060-408c-b1c8-6fa26b9a7877
  Args:
    source: :PrinceMichaelOfGreeceAndDenmark
    target: :PrincessOlgaOfGreece
    relation: :isMotherOf
  AssignClass (ea1b592b-6c75-4327-abcc-c19272285002)
 Call ID: ea1b592b-6c75-4327-abcc-c19272285002
  Args:
    type: :Man
    source: :PrinceAimoneOfSavoyAosta
  AddTriple (d71c0c85-b622-43a8-930f-26ea1169cb43)
 Call ID: d71c0c85-b622-43a8-930f-26ea1169cb43
  Args:
    relation: :hasRelation
    source: :PrincessOlgaOfGreece
    target: :PrinceAimoneOfSavoyAosta
  AssignClass (4332a53a-c389-45db-82cc-5f8b3a6ad8bb)
 Call ID: 4332a53a-c389-45db-82cc-5f8b3a6ad8bb
  Args:
    source: :PrincessIsabella
    type: :Woman
  AssignClass (d97168fe-254a-4149-abd8-e9a15b70dd87)
 Call ID: d97168fe-254a-4149-abd8-e9a15b70dd87
  Args:
    type: :Man
    source: :PrincePierreMurat
  AddTriple (f7eb3dea-aef6-442b-ab9e-14711e8aa2f3)
 Call ID: f7eb3dea-aef6-442b-ab9e-14711e8aa2f3
  Args:
    relation: :hasRelation
    source: :PrincessIsabella
    target: :PrincePierreMurat
  Finish (7652dafe-4a89-43ec-9fbf-ea0a28819363)
 Call ID: 7652dafe-4a89-43ec-9fbf-ea0a28819363
  Args: