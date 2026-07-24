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
King Juan Carlos IQueen Sofía


The Duchess of Soria and HernaniThe Duke of Soria and Hernani


The Dowager Duchess of Calabria


Infanta Sofía of Spain (Sofía de Todos los Santos de Borbón y Ortiz; born 29 April 2007) is a member of the Spanish royal family.
She is the younger daughter of King Felipe VI and Queen Letizia and, as such, is second in the line of succession to the Spanish throne behind her sister, Leonor, Princess of Asturias.
Sofía was born at the Ruber International Hospital in Madrid during the reign of her paternal grandfather, King Juan Carlos.
Early life and family

Infanta Sofía was born on 29 April 2007 at 16:50 (CET) at the Ruber International Hospital in Madrid by means of a caesarean section, two days after due date.
The parents, then the Prince and Princess of Asturias, did the same with Leonor's cells: they were taken to a private center in Arizona, which caused controversy in Spain.
Sofía was named after her paternal grandmother, Queen Sofía.
Education

Like her older sister, in 2009, Sofía started her education at the Escuela Infantil Guardia Real, the daycare for the children of the Spanish Royal Guard.
After announcing in April 2025 that the Infanta had decided not to undergo military service, in July 2025 the Royal Household confirmed that she would study Politics and International Relations at Forward College, an institution affiliated with the University of London.
Activities

As Infanta of Spain, it is very common to see her in official events with her parents and sister, such as the opening of Parliament, the National Day parade or the Princess of Asturias and Princess of Girona Awards ceremonies.
In 2021, Infanta Sofía and Princess Leonor participated in their first joint act without their parents, representing the "A Tree for Europe" campaign of the European youth association Equipo Europa .
On 16 July 2022, she accompanied her sister Leonor in her first international trip.
In late August 2023, she travelled with her mother, Queen Letizia, to Australia to see the final of the 2023 FIFA Women's World Cup between Spain and England.
The Queen and the Infanta delivered the trophy to the World Champions, Spain, and celebrated with them on the pitch.
In July 2024, she travelled with her father, King Felipe, to watch the Spanish national football team compete in the UEFA Euro 2024 final.
The photography contest aims to showcase the beauty of Spain.
On 5 December 2024 announced that the photography contest would only feature Sofía and not her parents or her older sister.
Sofía is due to present the second edition of the photography contest later in 2025.
In addition, to the photography contest a painting contest formerly known as “Ciudad de Hellín (City of Hellín)” will be changed to the “Certamen Internacional de Pintura “Infanta Sofía” de Hellín (International Painting Contest of Infanata Sofía of Hellín)” to honor her.
At the end of the month, she attended the Princess of Girona Awards ceremony and the UEFA Women's Euro 2025 final.
On 4 August 2025, Infanta Sofía along with her sister Leonor, Princess of Asturias attended the annual reception at Marivent Palace for Balearic Islands' authorities and personalities.
The reception also had King Felipe VI, Queen Letizia, and Queen Sofia in attendance.
This event marked the first reception attended by Leonor and Sofía.
Her older sister Leonor’s first official visit to Portugal took place on 12 July 2024.
In January 2026, Sofía attended the funeral of Princess Irene of Greece and Denmark and replaced her grandmother, Queen Sofía, in some public events.
Titles, styles and honours

As children of the prince of Asturias, Sofía was born infanta and styled "Her Royal Highness Infanta Doña Sofia".
Although with the same dignity and status as a prince, Sofia does not hold the title of princess, because in Spain only the heir to the Crown is allowed to carry that title.



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
  AssignClass (d693bba2-ac46-427d-afa0-d863c4687279)
 Call ID: d693bba2-ac46-427d-afa0-d863c4687279
  Args:
    source: :InfantaSofia
    type: :Person
  AssignClass (cdf77ebb-2717-40ee-92e8-9855c12fbf81)
 Call ID: cdf77ebb-2717-40ee-92e8-9855c12fbf81
  Args:
    type: :Woman
    source: :InfantaSofia
  AssignClass (66abc6f9-0550-4047-bb48-b602d6ac2dde)
 Call ID: 66abc6f9-0550-4047-bb48-b602d6ac2dde
  Args:
    type: :Person
    source: :KingFelipeVI
  AssignClass (e448f94c-d346-4c41-afa4-94bc347a812f)
 Call ID: e448f94c-d346-4c41-afa4-94bc347a812f
  Args:
    type: :Man
    source: :KingFelipeVI
  AssignClass (1c7c338f-8890-4020-85ae-f1a47013ed93)
 Call ID: 1c7c338f-8890-4020-85ae-f1a47013ed93
  Args:
    type: :Person
    source: :QueenLetizia
  AssignClass (325943b9-a957-4b59-b53f-3247b497f8f2)
 Call ID: 325943b9-a957-4b59-b53f-3247b497f8f2
  Args:
    type: :Woman
    source: :QueenLetizia
  AssignClass (397c6290-c810-4fab-a2ca-c0ce7b65acac)
 Call ID: 397c6290-c810-4fab-a2ca-c0ce7b65acac
  Args:
    source: :PrincessLeonor
    type: :Person
  AssignClass (8f17eb6a-9a35-4f47-9b67-4e25efb648d8)
 Call ID: 8f17eb6a-9a35-4f47-9b67-4e25efb648d8
  Args:
    source: :PrincessLeonor
    type: :Woman
  AssignClass (99e4f262-6f3b-45a9-bf7b-301e8120b337)
 Call ID: 99e4f262-6f3b-45a9-bf7b-301e8120b337
  Args:
    source: :KingJuanCarlos
    type: :Person
  AssignClass (01dc8466-f4d2-4685-83bc-1e4635be7a3d)
 Call ID: 01dc8466-f4d2-4685-83bc-1e4635be7a3d
  Args:
    source: :KingJuanCarlos
    type: :Man
  AssignClass (08b31617-6ffa-461c-a76b-83672d8197ab)
 Call ID: 08b31617-6ffa-461c-a76b-83672d8197ab
  Args:
    type: :Person
    source: :QueenSofia
  AssignClass (777029d1-dec9-44a8-a82c-b6fee44f9251)
 Call ID: 777029d1-dec9-44a8-a82c-b6fee44f9251
  Args:
    type: :Woman
    source: :QueenSofia
  AddTriple (7288c788-0450-4123-a792-02f21b0e8796)
 Call ID: 7288c788-0450-4123-a792-02f21b0e8796
  Args:
    source: :InfantaSofia
    relation: :hasFather
    target: :KingFelipeVI
  AddTriple (48ae55aa-8a9e-4521-b5a1-b140895d6b8b)
 Call ID: 48ae55aa-8a9e-4521-b5a1-b140895d6b8b
  Args:
    relation: :hasMother
    source: :InfantaSofia
    target: :QueenLetizia
  AddTriple (2f9e85ee-c92e-4188-829f-b0dd94f0892b)
 Call ID: 2f9e85ee-c92e-4188-829f-b0dd94f0892b
  Args:
    source: :InfantaSofia
    relation: :isSisterOf
    target: :PrincessLeonor
  AddTriple (ce7071bb-3af2-40a1-94c8-4bdeba08de78)
 Call ID: ce7071bb-3af2-40a1-94c8-4bdeba08de78
  Args:
    relation: :hasFather
    source: :PrincessLeonor
    target: :KingFelipeVI
  AddTriple (7ba4c248-8577-42c7-b329-15f2b006e82c)
 Call ID: 7ba4c248-8577-42c7-b329-15f2b006e82c
  Args:
    target: :QueenLetizia
    source: :PrincessLeonor
    relation: :hasMother
  AddTriple (987acdb2-415e-421d-902e-eae1c6c599c9)
 Call ID: 987acdb2-415e-421d-902e-eae1c6c599c9
  Args:
    target: :KingJuanCarlos
    source: :KingFelipeVI
    relation: :hasFather
  AddTriple (a4f11a45-c435-40ba-96ed-82e03ef10b00)
 Call ID: a4f11a45-c435-40ba-96ed-82e03ef10b00
  Args:
    source: :KingFelipeVI
    relation: :hasMother
    target: :QueenSofia
  AddLiteral (844c9735-e734-4306-a4a7-20144bd6b881)
 Call ID: 844c9735-e734-4306-a4a7-20144bd6b881
  Args:
    literal_type: xsd:integer
    source: :InfantaSofia
    relation: :hasBirthYear
    literal_value: 2007
  Finish (2ec1b979-3d9d-4a53-a642-5080277238e0)
 Call ID: 2ec1b979-3d9d-4a53-a642-5080277238e0
  Args: