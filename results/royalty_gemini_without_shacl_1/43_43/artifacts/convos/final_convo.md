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
  AssignClass (b86859e0-a013-4b08-bb49-c1f777ead950)
 Call ID: b86859e0-a013-4b08-bb49-c1f777ead950
  Args:
    source: :Prince_Pedro_Henrique_of_Orleans-Braganza
    type: :Man
  AssignClass (d4ccfaf1-2c2b-4d35-ae87-c982583cd9b8)
 Call ID: d4ccfaf1-2c2b-4d35-ae87-c982583cd9b8
  Args:
    type: :Person
    source: :Prince_Pedro_Henrique_of_Orleans-Braganza
  AddLiteral (49515b2b-5951-45ed-bd71-646315d42724)
 Call ID: 49515b2b-5951-45ed-bd71-646315d42724
  Args:
    source: :Prince_Pedro_Henrique_of_Orleans-Braganza
    relation: :hasBirthYear
    literal_value: 1909
    literal_type: xsd:integer
  AddLiteral (c2243cb0-1942-4613-ace1-f66241294460)
 Call ID: c2243cb0-1942-4613-ace1-f66241294460
  Args:
    relation: :hasDeathYear
    source: :Prince_Pedro_Henrique_of_Orleans-Braganza
    literal_type: xsd:integer
    literal_value: 1981
  AddLiteral (07d35348-7629-4e98-8bd2-d46b1ebf948f)
 Call ID: 07d35348-7629-4e98-8bd2-d46b1ebf948f
  Args:
    literal_value: The Expected Prince
    literal_type: xsd:string
    source: :Prince_Pedro_Henrique_of_Orleans-Braganza
    relation: :knownAs
  AssignClass (7f08a084-d627-4ccf-a8f9-5b365a426226)
 Call ID: 7f08a084-d627-4ccf-a8f9-5b365a426226
  Args:
    source: :Prince_Luis_of_Orleans-Braganza
    type: :Man
  AssignClass (49e19280-4608-42c8-b3b7-21ad135c37b5)
 Call ID: 49e19280-4608-42c8-b3b7-21ad135c37b5
  Args:
    source: :Prince_Luis_of_Orleans-Braganza
    type: :Person
  AddTriple (d6a60204-7430-48dd-97e6-a50c5a70f783)
 Call ID: d6a60204-7430-48dd-97e6-a50c5a70f783
  Args:
    relation: :hasFather
    source: :Prince_Pedro_Henrique_of_Orleans-Braganza
    target: :Prince_Luis_of_Orleans-Braganza
  AssignClass (7f823ca1-d5e7-473c-859a-24a952684459)
 Call ID: 7f823ca1-d5e7-473c-859a-24a952684459
  Args:
    type: :Woman
    source: :Princess_Maria_di_Grazia_of_Bourbon-Two_Sicilies
  AssignClass (973a4e33-a779-49ad-b6ef-9bb8a4e63bf0)
 Call ID: 973a4e33-a779-49ad-b6ef-9bb8a4e63bf0
  Args:
    source: :Princess_Maria_di_Grazia_of_Bourbon-Two_Sicilies
    type: :Person
  AddTriple (ce69c3dd-07d1-4f22-a55f-b936d29ffadb)
 Call ID: ce69c3dd-07d1-4f22-a55f-b936d29ffadb
  Args:
    source: :Prince_Pedro_Henrique_of_Orleans-Braganza
    target: :Princess_Maria_di_Grazia_of_Bourbon-Two_Sicilies
    relation: :hasMother
  AssignClass (bbfc4c7a-3959-4453-8375-1f86ef313823)
 Call ID: bbfc4c7a-3959-4453-8375-1f86ef313823
  Args:
    type: :Woman
    source: :Princess_Isabel_of_Brazil
  AssignClass (a945de72-be80-46ef-b24c-aff825a789f9)
 Call ID: a945de72-be80-46ef-b24c-aff825a789f9
  Args:
    type: :Person
    source: :Princess_Isabel_of_Brazil
  AddTriple (90035b72-ef7d-4bf4-b8d9-4740f5969cfc)
 Call ID: 90035b72-ef7d-4bf4-b8d9-4740f5969cfc
  Args:
    relation: :isMotherOf
    source: :Princess_Isabel_of_Brazil
    target: :Prince_Luis_of_Orleans-Braganza
  AssignClass (02aeea3e-65d4-4717-a7aa-43444cdafe57)
 Call ID: 02aeea3e-65d4-4717-a7aa-43444cdafe57
  Args:
    source: :Prince_Gaston_Count_of_Eu
    type: :Man
  AssignClass (b0cc306c-66ee-4fc1-be00-c9d8570f7f8d)
 Call ID: b0cc306c-66ee-4fc1-be00-c9d8570f7f8d
  Args:
    source: :Prince_Gaston_Count_of_Eu
    type: :Person
  AddTriple (d31ffd0c-c76b-4fdc-97e5-98df1dc3f92c)
 Call ID: d31ffd0c-c76b-4fdc-97e5-98df1dc3f92c
  Args:
    relation: :isFatherOf
    target: :Prince_Luis_of_Orleans-Braganza
    source: :Prince_Gaston_Count_of_Eu
  AssignClass (c8ca2746-c291-4cae-aa8a-2248bb6360a8)
 Call ID: c8ca2746-c291-4cae-aa8a-2248bb6360a8
  Args:
    source: :Princess_Maria_Pia_of_Bourbon-Two_Sicilies
    type: :Woman
  AssignClass (6b741dc5-91e0-49a6-b10b-036e900fddb3)
 Call ID: 6b741dc5-91e0-49a6-b10b-036e900fddb3
  Args:
    source: :Princess_Maria_Pia_of_Bourbon-Two_Sicilies
    type: :Person
  AddTriple (998da8c2-6228-427a-a2ec-2f584f9f1790)
 Call ID: 998da8c2-6228-427a-a2ec-2f584f9f1790
  Args:
    target: :Princess_Maria_Pia_of_Bourbon-Two_Sicilies
    source: :Prince_Pedro_Henrique_of_Orleans-Braganza
    relation: :hasMother
  AssignClass (4215fe04-e7f0-4647-a6f4-4349a5030547)
 Call ID: 4215fe04-e7f0-4647-a6f4-4349a5030547
  Args:
    source: :Prince_Alfonso_Count_of_Caserta
    type: :Man
  AssignClass (83adeb05-c2e6-49ea-a970-3c8ae09dc04d)
 Call ID: 83adeb05-c2e6-49ea-a970-3c8ae09dc04d
  Args:
    source: :Prince_Alfonso_Count_of_Caserta
    type: :Person
  AssignClass (aeee5f3e-6629-45a0-aed2-9623c7bd7f4b)
 Call ID: aeee5f3e-6629-45a0-aed2-9623c7bd7f4b
  Args:
    type: :Man
    source: :Luiz_Gastao
  AssignClass (e4a81664-3598-424d-b3ff-090134ff709c)
 Call ID: e4a81664-3598-424d-b3ff-090134ff709c
  Args:
    source: :Luiz_Gastao
    type: :Person
  AssignClass (e6df3b17-f220-4ada-af4d-2390ea0db5ba)
 Call ID: e6df3b17-f220-4ada-af4d-2390ea0db5ba
  Args:
    source: :Pia_Maria
    type: :Woman
  AssignClass (e739dd2b-9a1e-4d5c-abc3-d10f01230e13)
 Call ID: e739dd2b-9a1e-4d5c-abc3-d10f01230e13
  Args:
    source: :Pia_Maria
    type: :Person
  AddTriple (6410f93a-8b75-4e59-8fa2-749361374f54)
 Call ID: 6410f93a-8b75-4e59-8fa2-749361374f54
  Args:
    target: :Luiz_Gastao
    source: :Prince_Pedro_Henrique_of_Orleans-Braganza
    relation: :hasBrother
  AddTriple (c74207ce-1cee-4cfa-9874-538a92b47cce)
 Call ID: c74207ce-1cee-4cfa-9874-538a92b47cce
  Args:
    target: :Pia_Maria
    source: :Prince_Pedro_Henrique_of_Orleans-Braganza
    relation: :hasSister
  AssignClass (a4b25bf5-ddc8-4fcc-b978-ad6956c41808)
 Call ID: a4b25bf5-ddc8-4fcc-b978-ad6956c41808
  Args:
    type: :Man
    source: :Prince_Pedro_Gastao_of_Orleans-Braganza
  AssignClass (bdaa2b9a-4286-4197-bae3-3e7ae664a93b)
 Call ID: bdaa2b9a-4286-4197-bae3-3e7ae664a93b
  Args:
    source: :Prince_Pedro_Gastao_of_Orleans-Braganza
    type: :Person
  AssignClass (4fa15c1d-91db-44b5-805c-fabf557e9b1a)
 Call ID: 4fa15c1d-91db-44b5-805c-fabf557e9b1a
  Args:
    source: :Pedro_de_Alcantara_Prince_of_Grao-Para
    type: :Man
  AssignClass (02f35ef5-eb28-4812-8548-985e8efff7ae)
 Call ID: 02f35ef5-eb28-4812-8548-985e8efff7ae
  Args:
    source: :Pedro_de_Alcantara_Prince_of_Grao-Para
    type: :Person
  AddTriple (1f393b75-d5f8-485e-9ae1-525b6359191c)
 Call ID: 1f393b75-d5f8-485e-9ae1-525b6359191c
  Args:
    target: :Prince_Pedro_Gastao_of_Orleans-Braganza
    source: :Pedro_de_Alcantara_Prince_of_Grao-Para
    relation: :isFatherOf
  AssignClass (35e58c98-6a60-42fd-922f-c6416d666765)
 Call ID: 35e58c98-6a60-42fd-922f-c6416d666765
  Args:
    type: :Woman
    source: :Princess_Maria_Elisabeth_of_Bavaria
  AssignClass (e676527c-68d3-4d38-8c7a-5bd66fcc730b)
 Call ID: e676527c-68d3-4d38-8c7a-5bd66fcc730b
  Args:
    source: :Princess_Maria_Elisabeth_of_Bavaria
    type: :Person
  AddLiteral (2ff6308a-b385-41da-870e-7178485fb142)
 Call ID: 2ff6308a-b385-41da-870e-7178485fb142
  Args:
    literal_type: xsd:integer
    literal_value: 1937
    relation: :hasMarriageYear
    source: :Prince_Pedro_Henrique_of_Orleans-Braganza
  AddTriple (bd23c85d-c7f3-4c13-841d-02f490752f9b)
 Call ID: bd23c85d-c7f3-4c13-841d-02f490752f9b
  Args:
    relation: :hasRelation
    target: :Princess_Maria_Elisabeth_of_Bavaria
    source: :Prince_Pedro_Henrique_of_Orleans-Braganza
  Finish (dd92e683-a363-4363-87b4-b42df7a6df50)
 Call ID: dd92e683-a363-4363-87b4-b42df7a6df50
  Args: