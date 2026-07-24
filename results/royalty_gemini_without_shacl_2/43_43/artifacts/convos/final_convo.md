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
Prince Pedro Henrique of Orléans-Braganza (13 September 1909 – 5 July 1981), nicknamed The Expected Prince (Portuguese: O Príncipe Esperado) was the eldest son of Prince Luís of Orléans-Braganza and Princess Maria di Grazia of Bourbon-Two Sicilies, and head of the Vassouras branch of the Imperial House of Brazil from 1921 until his death in 1981.
Pedro succeeded his grandmother, Princess Isabel of Brazil, as head of the family after her death.
His father, Prince Luiz of Orléans-Braganza, was the second son of the heir to the defunct Brazilian throne, the Princess Imperial Isabel, and Prince Gaston, Count of Eu.
His mother was Princess Maria Pia of Bourbon-Two Sicilies.
His godparents were his paternal grandmother, Princess Isabel of Brazil, and maternal grandfather Prince Alfonso, Count of Caserta, Head of the royal house of the Two Sicilies.
In the same year Brazil's banishment of the Orléans-Braganzas was revoked by the then President Epitácio Pessoa.
Pedro Henrique accompanied Count d'Eu when he led part of the Imperial Family back to Brazil, without the aged and infirm Princess Isabel.
Upon the death of his father in 1920 Pedro Henrique became claimant to the title of Prince Imperial, but on 14 November 1921 Princess Isabel died at the Castle d'Eu.
So, aged 12 Prince Pedro Henrique became the head of the imperial family.
He continued living in France with his mother, Princess Maria Pia, where she thought he could get a better education with his siblings Luiz Gastão and Pia Maria.
Prince Pedro Henrique was only able to return to Brazil in 1945, when the Second World War ended.
His cousin, Prince Pedro Gastão of Orléans-Braganza, the eldest son of Pedro de Alcântara, Prince of Grão-Pará, challenged Pedro Henrique's claim to the succession in 1946, on the basis that his father's renunciation had no legal force.
In 1951, D. Pedro Henrique bought a farm, Fazenda Santa Maria, in the town of Jacarezinho, interior of Paraná.
Pedro Henrique resided at a site called Santa Maria until the end of his life.
Marriage and children

Pedro Henrique married Princess Maria Elisabeth of Bavaria at Nymphenburg Palace, Bavaria, on 19 August 1937.



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
  AssignClass (1103e2d3-8496-41af-afa0-77c7b2343bdb)
 Call ID: 1103e2d3-8496-41af-afa0-77c7b2343bdb
  Args:
    type: :Man
    source: Pedro_Henrique_of_Orléans-Braganza
  AssignClass (c5b6125b-db85-4ae9-a451-279a76a9e250)
 Call ID: c5b6125b-db85-4ae9-a451-279a76a9e250
  Args:
    type: :Man
    source: Luís_of_Orléans-Braganza
  AssignClass (835a488d-bbdb-4d47-86b6-c5a5ce8182a5)
 Call ID: 835a488d-bbdb-4d47-86b6-c5a5ce8182a5
  Args:
    type: :Woman
    source: Maria_di_Grazia_of_Bourbon-Two_Sicilies
  AssignClass (5708f501-9ce7-4b57-8da9-03914d9448aa)
 Call ID: 5708f501-9ce7-4b57-8da9-03914d9448aa
  Args:
    type: :Woman
    source: Isabel_of_Brazil
  AssignClass (4982d6aa-7adb-4e95-82de-78f03921509a)
 Call ID: 4982d6aa-7adb-4e95-82de-78f03921509a
  Args:
    type: :Man
    source: Gaston_Count_of_Eu
  AssignClass (40c252dd-2bd3-438e-abb8-d0447fd33886)
 Call ID: 40c252dd-2bd3-438e-abb8-d0447fd33886
  Args:
    type: :Man
    source: Alfonso_Count_of_Caserta
  AssignClass (2836c823-f459-435c-a4e9-a77920805f41)
 Call ID: 2836c823-f459-435c-a4e9-a77920805f41
  Args:
    type: :Woman
    source: Maria_Pia_of_Bourbon-Two_Sicilies
  AssignClass (708c9b44-354b-4e86-8f03-cb5fa44a9eed)
 Call ID: 708c9b44-354b-4e86-8f03-cb5fa44a9eed
  Args:
    type: :Man
    source: Luiz_Gastão_of_Orléans-Braganza
  AssignClass (dbedf7c8-3c67-4090-a454-7e59b05a0850)
 Call ID: dbedf7c8-3c67-4090-a454-7e59b05a0850
  Args:
    type: :Woman
    source: Pia_Maria_of_Orléans-Braganza
  AssignClass (d3596245-d5cd-44ac-8ec8-8e946e968a12)
 Call ID: d3596245-d5cd-44ac-8ec8-8e946e968a12
  Args:
    type: :Man
    source: Pedro_Gastão_of_Orléans-Braganza
  AssignClass (bb8fb381-ee5c-41c7-ac43-14074476b9b8)
 Call ID: bb8fb381-ee5c-41c7-ac43-14074476b9b8
  Args:
    type: :Man
    source: Pedro_de_Alcântara_Prince_of_Grão-Pará
  AssignClass (f052ca50-6a43-4dd1-b87d-1729cd789b69)
 Call ID: f052ca50-6a43-4dd1-b87d-1729cd789b69
  Args:
    type: :Woman
    source: Maria_Elisabeth_of_Bavaria
  AddLiteral (9d28b56b-9442-4d93-895f-77ca7abcb45a)
 Call ID: 9d28b56b-9442-4d93-895f-77ca7abcb45a
  Args:
    source: Pedro_Henrique_of_Orléans-Braganza
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1909
  AddLiteral (29225755-e9da-48be-a33d-c32156e3c97f)
 Call ID: 29225755-e9da-48be-a33d-c32156e3c97f
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: Pedro_Henrique_of_Orléans-Braganza
    literal_value: 1981
  AddLiteral (ad084d68-402a-4664-b3df-6b6d0f5d2442)
 Call ID: ad084d68-402a-4664-b3df-6b6d0f5d2442
  Args:
    literal_value: The Expected Prince
    relation: :knownAs
    literal_type: xsd:string
    source: Pedro_Henrique_of_Orléans-Braganza
  AddLiteral (91d5b3ba-27c7-4afb-bd93-6b4475a57705)
 Call ID: 91d5b3ba-27c7-4afb-bd93-6b4475a57705
  Args:
    literal_value: O Príncipe Esperado
    source: Pedro_Henrique_of_Orléans-Braganza
    relation: :alsoKnownAs
    literal_type: xsd:string
  AddTriple (d86228b8-08a3-451d-876c-580923a0ee40)
 Call ID: d86228b8-08a3-451d-876c-580923a0ee40
  Args:
    source: Pedro_Henrique_of_Orléans-Braganza
    target: Luís_of_Orléans-Braganza
    relation: :hasFather
  AddTriple (c8aaecfd-237f-4694-8dc0-ec441aae40a7)
 Call ID: c8aaecfd-237f-4694-8dc0-ec441aae40a7
  Args:
    relation: :hasMother
    target: Maria_di_Grazia_of_Bourbon-Two_Sicilies
    source: Pedro_Henrique_of_Orléans-Braganza
  AddTriple (f69d6878-b87b-413c-95c2-d18f865557fc)
 Call ID: f69d6878-b87b-413c-95c2-d18f865557fc
  Args:
    source: Luís_of_Orléans-Braganza
    target: Gaston_Count_of_Eu
    relation: :hasFather
  AddTriple (c305f9fd-9e1a-4969-932d-2227efe14bc5)
 Call ID: c305f9fd-9e1a-4969-932d-2227efe14bc5
  Args:
    relation: :hasMother
    target: Isabel_of_Brazil
    source: Luís_of_Orléans-Braganza
  AddTriple (0e37492c-1ee0-47d8-9176-49907f35af5a)
 Call ID: 0e37492c-1ee0-47d8-9176-49907f35af5a
  Args:
    target: Maria_Pia_of_Bourbon-Two_Sicilies
    relation: :hasMother
    source: Pedro_Henrique_of_Orléans-Braganza
  AddTriple (3c5bd7b3-73f6-4c22-a04f-278f5f96a871)
 Call ID: 3c5bd7b3-73f6-4c22-a04f-278f5f96a871
  Args:
    relation: :isSiblingOf
    target: Luiz_Gastão_of_Orléans-Braganza
    source: Pedro_Henrique_of_Orléans-Braganza
  AddTriple (594de4f9-cc9b-43c6-a097-da91eb98a395)
 Call ID: 594de4f9-cc9b-43c6-a097-da91eb98a395
  Args:
    source: Pedro_Henrique_of_Orléans-Braganza
    target: Pia_Maria_of_Orléans-Braganza
    relation: :isSiblingOf
  AddTriple (0b6e6685-15d9-4283-a5ca-6acaa097d149)
 Call ID: 0b6e6685-15d9-4283-a5ca-6acaa097d149
  Args:
    source: Pedro_Gastão_of_Orléans-Braganza
    target: Pedro_de_Alcântara_Prince_of_Grão-Pará
    relation: :hasFather
  AddLiteral (536e9d77-09dc-4baf-ac90-5ca04d210f59)
 Call ID: 536e9d77-09dc-4baf-ac90-5ca04d210f59
  Args:
    literal_value: 1937
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: Pedro_Henrique_of_Orléans-Braganza
  AddTriple (df1bce74-2467-4b8a-907a-c0782b2a4903)
 Call ID: df1bce74-2467-4b8a-907a-c0782b2a4903
  Args:
    target: Maria_Elisabeth_of_Bavaria
    relation: :hasRelation
    source: Pedro_Henrique_of_Orléans-Braganza
  Finish (9a17a3b4-18c2-496e-aaab-eaba8cdc84b9)
 Call ID: 9a17a3b4-18c2-496e-aaab-eaba8cdc84b9
  Args: