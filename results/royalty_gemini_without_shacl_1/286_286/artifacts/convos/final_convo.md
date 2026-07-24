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
Rafael of Orléans-Braganza (Portuguese: Rafael de Orléans e Bragança; born 24 April 1986) is a member of the Imperial House of Brazil.
He is the heir presumptive to his childless uncle, Prince Bertrand, the current head of the Vassouras branch of the House of Orléans-Braganza and one of the claimants to the defunct Brazilian Throne.
Rafael became heir presumptive following the death of his father, Prince Antônio, in November 2024.
Family

Born in Petrópolis, Brazil on 26 April 1986, he is the third child and second son of Prince Antônio de Orleans e Bragança and Princess Christine of Ligne.
He has an older brother and sister, Prince Pedro Luiz and Princess Amélia and a younger sister, Princess Maria Gabriela.
His name in full is Rafael Antonio Maria José Francisco Miguel Gabriel Gonzaga de Orléans e Bragança e Ligne.
His paternal grandparents were Prince Pedro Henrique of Orléans-Bragança, one of two claimants to be head of the Brazilian Imperial House, and Princess Maria Elisabeth of Bavaria.
His maternal grandparents were Antoine, 13th Prince of Ligne, and Princess Alix of Luxembourg.
His mother's family, the House of Ligne, is one of the oldest and most prominent Wallonian noble families still extant in Belgium.
Christine is a niece of Grand Duke Jean, who reigned in Luxembourg until his abdication in 2000.
Personal life

Rafael has a degree in manufacturing engineering from Pontifical Catholic University of Rio de Janeiro, working at the InBev subsidiary in London.
Rafael also has a partnership and a tourism enterprise with headquarters in New York, Paris and Rio de Janeiro.
Rafael has expressed in statements his desire to marry a princess who is part of "Catholic royalty or high nobility".
Appointments

In February 2022, after the floods that devastated the city of Petrópolis, Rafael came to the aid of the victims, bringing them essential goods that the imperial house received from monarchist supporters.
Honors

Genealogy

Ancestry

Patrilineal descent

Rafael is a member of the House of Orléans-Braganza, a sub-branch of the House of Bourbon, itself a branch of the House of Capet and of the Robertians.
Rafael's patriline is the line from which he is descended father to son.
It follows the Dukes of Orléans, the Kings of France, the Dukes and Counts of Vendôme, the Counts of La Marche, the first Duke of Bourbon, a Count of Clermont, and before them, again the Kings of France.



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
  AssignClass (4a01c333-ca0d-47c1-9e36-fd3d409b8b7c)
 Call ID: 4a01c333-ca0d-47c1-9e36-fd3d409b8b7c
  Args:
    source: :Rafael_de_Orleans_e_Braganca
    type: :Man
  AssignClass (52862132-af4b-4c3a-8ee4-fd10c75fd35b)
 Call ID: 52862132-af4b-4c3a-8ee4-fd10c75fd35b
  Args:
    type: :Person
    source: :Rafael_de_Orleans_e_Braganca
  AddLiteral (448c0faa-205c-48bd-b8c5-b93ce993465e)
 Call ID: 448c0faa-205c-48bd-b8c5-b93ce993465e
  Args:
    source: :Rafael_de_Orleans_e_Braganca
    literal_value: 1986
    literal_type: xsd:integer
    relation: :hasBirthYear
  AssignClass (b32719ec-1433-4c23-b271-708314e70ae8)
 Call ID: b32719ec-1433-4c23-b271-708314e70ae8
  Args:
    type: :Man
    source: :Prince_Bertrand
  AssignClass (97ce0e15-e821-4a4f-aa90-1a64031eb365)
 Call ID: 97ce0e15-e821-4a4f-aa90-1a64031eb365
  Args:
    type: :Person
    source: :Prince_Bertrand
  AssignClass (29d76d74-b128-41dd-8174-2d1fdcbc780e)
 Call ID: 29d76d74-b128-41dd-8174-2d1fdcbc780e
  Args:
    source: :Prince_Antonio
    type: :Man
  AssignClass (2191196a-8297-40f7-b499-a0f309addb5d)
 Call ID: 2191196a-8297-40f7-b499-a0f309addb5d
  Args:
    source: :Prince_Antonio
    type: :Person
  AddLiteral (355acf5d-a04d-4bba-8c53-c9a2c5097fa9)
 Call ID: 355acf5d-a04d-4bba-8c53-c9a2c5097fa9
  Args:
    literal_value: 2024
    source: :Prince_Antonio
    literal_type: xsd:integer
    relation: :hasDeathYear
  AssignClass (5b1550e8-a293-4b31-9ac3-b0dde9c02b46)
 Call ID: 5b1550e8-a293-4b31-9ac3-b0dde9c02b46
  Args:
    type: :Woman
    source: :Princess_Christine_of_Ligne
  AssignClass (4194b65d-c60d-47b4-85aa-b0bbb1306817)
 Call ID: 4194b65d-c60d-47b4-85aa-b0bbb1306817
  Args:
    type: :Person
    source: :Princess_Christine_of_Ligne
  AssignClass (937cee9d-2793-4a17-aee9-b2e62ae3ee81)
 Call ID: 937cee9d-2793-4a17-aee9-b2e62ae3ee81
  Args:
    type: :Man
    source: :Prince_Pedro_Luiz
  AssignClass (fc91dc11-41f0-4eab-9cb3-609bb75d8f9c)
 Call ID: fc91dc11-41f0-4eab-9cb3-609bb75d8f9c
  Args:
    source: :Prince_Pedro_Luiz
    type: :Person
  AssignClass (6cb4e116-1241-41ee-89cd-2e4430eb7d97)
 Call ID: 6cb4e116-1241-41ee-89cd-2e4430eb7d97
  Args:
    type: :Woman
    source: :Princess_Amelia
  AssignClass (51e929fe-09a2-449e-8e7e-cfd32f26e6ce)
 Call ID: 51e929fe-09a2-449e-8e7e-cfd32f26e6ce
  Args:
    source: :Princess_Amelia
    type: :Person
  AssignClass (60193a93-2198-4288-8d44-0e1818caa264)
 Call ID: 60193a93-2198-4288-8d44-0e1818caa264
  Args:
    type: :Woman
    source: :Princess_Maria_Gabriela
  AssignClass (f3b717a6-db23-4960-8501-dc48a52a534f)
 Call ID: f3b717a6-db23-4960-8501-dc48a52a534f
  Args:
    type: :Person
    source: :Princess_Maria_Gabriela
  AssignClass (ab881b5d-a385-425c-b5b4-056d2b5a2976)
 Call ID: ab881b5d-a385-425c-b5b4-056d2b5a2976
  Args:
    source: :Prince_Pedro_Henrique
    type: :Man
  AssignClass (7cd084a2-f36e-44fc-ac85-d9dbdd7decb2)
 Call ID: 7cd084a2-f36e-44fc-ac85-d9dbdd7decb2
  Args:
    source: :Prince_Pedro_Henrique
    type: :Person
  AssignClass (4abb914b-4d8b-4350-9169-2a44739c1496)
 Call ID: 4abb914b-4d8b-4350-9169-2a44739c1496
  Args:
    type: :Woman
    source: :Princess_Maria_Elisabeth_of_Bavaria
  AssignClass (e0dce6e0-6fa7-4482-aa31-a57dc920b052)
 Call ID: e0dce6e0-6fa7-4482-aa31-a57dc920b052
  Args:
    type: :Person
    source: :Princess_Maria_Elisabeth_of_Bavaria
  AssignClass (616c8f42-f5a4-4aa0-9a86-faeec4a43eb3)
 Call ID: 616c8f42-f5a4-4aa0-9a86-faeec4a43eb3
  Args:
    type: :Man
    source: :Antoine_Prince_of_Ligne
  AssignClass (edbf6fbe-89a2-41ef-bba6-d4921a0a64e6)
 Call ID: edbf6fbe-89a2-41ef-bba6-d4921a0a64e6
  Args:
    type: :Person
    source: :Antoine_Prince_of_Ligne
  AssignClass (6d948069-642c-4469-9de5-89a1afdf43a8)
 Call ID: 6d948069-642c-4469-9de5-89a1afdf43a8
  Args:
    source: :Princess_Alix_of_Luxembourg
    type: :Woman
  AssignClass (7a240b53-6aa1-4b1a-a913-4dc646e16552)
 Call ID: 7a240b53-6aa1-4b1a-a913-4dc646e16552
  Args:
    source: :Princess_Alix_of_Luxembourg
    type: :Person
  AssignClass (e3c4b755-1ee3-490a-8430-5cbf3a21024c)
 Call ID: e3c4b755-1ee3-490a-8430-5cbf3a21024c
  Args:
    type: :Man
    source: :Grand_Duke_Jean
  AssignClass (c929937c-80a9-43eb-b62d-4a5fd3644f42)
 Call ID: c929937c-80a9-43eb-b62d-4a5fd3644f42
  Args:
    source: :Grand_Duke_Jean
    type: :Person
  AddTriple (1fb560c8-f7ea-4a18-b2d5-6c87b3321585)
 Call ID: 1fb560c8-f7ea-4a18-b2d5-6c87b3321585
  Args:
    target: :Prince_Antonio
    relation: :hasFather
    source: :Rafael_de_Orleans_e_Braganca
  AddTriple (79516e78-9e9b-4fb0-b441-10d07751ab6b)
 Call ID: 79516e78-9e9b-4fb0-b441-10d07751ab6b
  Args:
    source: :Rafael_de_Orleans_e_Braganca
    target: :Princess_Christine_of_Ligne
    relation: :hasMother
  AddTriple (30a699cb-a825-40bd-9d56-fe514f18fb82)
 Call ID: 30a699cb-a825-40bd-9d56-fe514f18fb82
  Args:
    target: :Prince_Pedro_Henrique
    relation: :hasFather
    source: :Prince_Antonio
  AddTriple (ce8bc3c6-7bb0-46d9-81cb-db6059b9e3f7)
 Call ID: ce8bc3c6-7bb0-46d9-81cb-db6059b9e3f7
  Args:
    source: :Prince_Antonio
    relation: :hasMother
    target: :Princess_Maria_Elisabeth_of_Bavaria
  AddTriple (59c3c5d4-2ae4-489e-960a-32dc21046bfa)
 Call ID: 59c3c5d4-2ae4-489e-960a-32dc21046bfa
  Args:
    source: :Princess_Christine_of_Ligne
    target: :Antoine_Prince_of_Ligne
    relation: :hasFather
  AddTriple (42106480-fea9-4b50-95a2-c9be31b4bbd0)
 Call ID: 42106480-fea9-4b50-95a2-c9be31b4bbd0
  Args:
    target: :Princess_Alix_of_Luxembourg
    relation: :hasMother
    source: :Princess_Christine_of_Ligne
  AddTriple (678d04bd-2d5c-4385-83ad-d46e4d7a5523)
 Call ID: 678d04bd-2d5c-4385-83ad-d46e4d7a5523
  Args:
    source: :Rafael_de_Orleans_e_Braganca
    relation: :isSiblingOf
    target: :Prince_Pedro_Luiz
  AddTriple (d0d9854a-cf18-4cce-8ab8-55010c9ac3c3)
 Call ID: d0d9854a-cf18-4cce-8ab8-55010c9ac3c3
  Args:
    source: :Rafael_de_Orleans_e_Braganca
    target: :Princess_Amelia
    relation: :isSiblingOf
  AddTriple (5bdd420c-c04a-4a23-9d85-84ef4d048880)
 Call ID: 5bdd420c-c04a-4a23-9d85-84ef4d048880
  Args:
    source: :Rafael_de_Orleans_e_Braganca
    target: :Princess_Maria_Gabriela
    relation: :isSiblingOf
  Finish (62d477ce-1b9e-4ed9-bde0-4ff7ac010700)
 Call ID: 62d477ce-1b9e-4ed9-bde0-4ff7ac010700
  Args: