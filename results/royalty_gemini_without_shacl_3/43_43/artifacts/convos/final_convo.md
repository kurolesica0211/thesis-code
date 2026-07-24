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
  AssignClass (6b8e0921-4dc4-4b53-b7cd-52fba0ff08fb)
 Call ID: 6b8e0921-4dc4-4b53-b7cd-52fba0ff08fb
  Args:
    type: :Man
    source: Pedro_Henrique_of_Orléans-Braganza
  AssignClass (6d5017d8-4bae-446c-bbf3-6796043cab84)
 Call ID: 6d5017d8-4bae-446c-bbf3-6796043cab84
  Args:
    type: :Man
    source: Luís_of_Orléans-Braganza
  AssignClass (00e0da47-2251-43ef-b49c-7b2084f54b8d)
 Call ID: 00e0da47-2251-43ef-b49c-7b2084f54b8d
  Args:
    source: Maria_di_Grazia_of_Bourbon-Two_Sicilies
    type: :Woman
  AssignClass (16ab0b53-2c54-4fc4-8888-2ea31877f7e4)
 Call ID: 16ab0b53-2c54-4fc4-8888-2ea31877f7e4
  Args:
    type: :Woman
    source: Isabel_of_Brazil
  AssignClass (cd2219d5-ba81-4478-8f3c-1127fdfd4f85)
 Call ID: cd2219d5-ba81-4478-8f3c-1127fdfd4f85
  Args:
    source: Gaston_Count_of_Eu
    type: :Man
  AssignClass (a2ae7da5-50e8-4650-a45d-cc06e8479491)
 Call ID: a2ae7da5-50e8-4650-a45d-cc06e8479491
  Args:
    type: :Woman
    source: Maria_Pia_of_Bourbon-Two_Sicilies
  AssignClass (145d571d-c565-4c6f-a3fc-f051bd3b5450)
 Call ID: 145d571d-c565-4c6f-a3fc-f051bd3b5450
  Args:
    source: Alfonso_Count_of_Caserta
    type: :Man
  AssignClass (330680e7-94cd-49e1-871d-508a30262e1a)
 Call ID: 330680e7-94cd-49e1-871d-508a30262e1a
  Args:
    type: :Man
    source: Luiz_Gastão_of_Orléans-Braganza
  AssignClass (cb67ac21-4bb4-46ea-99bb-c71363739cd5)
 Call ID: cb67ac21-4bb4-46ea-99bb-c71363739cd5
  Args:
    type: :Woman
    source: Pia_Maria_of_Orléans-Braganza
  AssignClass (e5b1b0b9-333d-4ea6-8477-be98cbb1c43a)
 Call ID: e5b1b0b9-333d-4ea6-8477-be98cbb1c43a
  Args:
    source: Pedro_Gastão_of_Orléans-Braganza
    type: :Man
  AssignClass (01cf7683-96cd-4907-8138-118202db4de7)
 Call ID: 01cf7683-96cd-4907-8138-118202db4de7
  Args:
    source: Pedro_de_Alcântara_Prince_of_Grão-Pará
    type: :Man
  AssignClass (4ea94fc3-7496-48ea-8feb-a082404eab40)
 Call ID: 4ea94fc3-7496-48ea-8feb-a082404eab40
  Args:
    source: Maria_Elisabeth_of_Bavaria
    type: :Woman
  AddLiteral (55b09844-5579-4a54-ad0a-e7ab77d2228c)
 Call ID: 55b09844-5579-4a54-ad0a-e7ab77d2228c
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Pedro_Henrique_of_Orléans-Braganza
    literal_value: 1909
  AddLiteral (429f9819-8455-4e2d-8719-f9389eb98d69)
 Call ID: 429f9819-8455-4e2d-8719-f9389eb98d69
  Args:
    literal_value: 1981
    source: Pedro_Henrique_of_Orléans-Braganza
    relation: :hasDeathYear
    literal_type: xsd:integer
  AddLiteral (1f70bf30-01e4-4617-9321-0f417872db00)
 Call ID: 1f70bf30-01e4-4617-9321-0f417872db00
  Args:
    literal_value: The Expected Prince
    source: Pedro_Henrique_of_Orléans-Braganza
    relation: :knownAs
    literal_type: xsd:string
  AddTriple (18e59c66-9249-47b2-a555-610cef604308)
 Call ID: 18e59c66-9249-47b2-a555-610cef604308
  Args:
    target: Luís_of_Orléans-Braganza
    source: Pedro_Henrique_of_Orléans-Braganza
    relation: :hasFather
  AddTriple (b04d69a5-2bae-46aa-8145-42949b9bd014)
 Call ID: b04d69a5-2bae-46aa-8145-42949b9bd014
  Args:
    source: Pedro_Henrique_of_Orléans-Braganza
    relation: :hasMother
    target: Maria_di_Grazia_of_Bourbon-Two_Sicilies
  AddTriple (f4fcb2a2-97bd-4c24-bd09-30ac586092f6)
 Call ID: f4fcb2a2-97bd-4c24-bd09-30ac586092f6
  Args:
    relation: :hasMother
    source: Luís_of_Orléans-Braganza
    target: Isabel_of_Brazil
  AddTriple (eac0ec39-d66a-4145-b8ec-b81c03fe1586)
 Call ID: eac0ec39-d66a-4145-b8ec-b81c03fe1586
  Args:
    target: Gaston_Count_of_Eu
    relation: :hasFather
    source: Luís_of_Orléans-Braganza
  AddTriple (d5bf61fe-2609-4e7c-ab52-607a8e6a2c26)
 Call ID: d5bf61fe-2609-4e7c-ab52-607a8e6a2c26
  Args:
    source: Pedro_Henrique_of_Orléans-Braganza
    relation: :isSiblingOf
    target: Luiz_Gastão_of_Orléans-Braganza
  AddTriple (d24abaeb-2757-48c0-ab7e-05653d16b128)
 Call ID: d24abaeb-2757-48c0-ab7e-05653d16b128
  Args:
    source: Pedro_Henrique_of_Orléans-Braganza
    relation: :isSiblingOf
    target: Pia_Maria_of_Orléans-Braganza
  AddTriple (5be68f6d-e2cc-40a8-ad69-a8f24d5423e2)
 Call ID: 5be68f6d-e2cc-40a8-ad69-a8f24d5423e2
  Args:
    target: Pedro_de_Alcântara_Prince_of_Grão-Pará
    source: Pedro_Gastão_of_Orléans-Braganza
    relation: :hasFather
  AddTriple (fa3938aa-27b9-4a43-a64c-c26cf4d268bd)
 Call ID: fa3938aa-27b9-4a43-a64c-c26cf4d268bd
  Args:
    relation: :hasFather
    source: Pedro_Henrique_of_Orléans-Braganza
    target: Maria_Elisabeth_of_Bavaria
  AddLiteral (1eef53c8-d3d6-4f91-a5bd-a940859336dd)
 Call ID: 1eef53c8-d3d6-4f91-a5bd-a940859336dd
  Args:
    literal_value: 1937
    source: Pedro_Henrique_of_Orléans-Braganza
    relation: :hasMarriageYear
    literal_type: xsd:integer
  Finish (8ede15f1-255e-4125-9e4b-3916b9f1a175)
 Call ID: 8ede15f1-255e-4125-9e4b-3916b9f1a175
  Args: