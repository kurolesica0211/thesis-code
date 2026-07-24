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
  AssignClass (5b0dbb5b-10d9-4ce1-9e83-941a6f416efb)
 Call ID: 5b0dbb5b-10d9-4ce1-9e83-941a6f416efb
  Args:
    type: :Person
    source: Sofía_of_Spain
  AssignClass (84915d8a-4163-4b7b-b473-3d23ea29a654)
 Call ID: 84915d8a-4163-4b7b-b473-3d23ea29a654
  Args:
    type: :Woman
    source: Sofía_of_Spain
  AssignClass (1855d073-9aeb-4403-abc5-9cb936b325b4)
 Call ID: 1855d073-9aeb-4403-abc5-9cb936b325b4
  Args:
    type: :Person
    source: Felipe_VI
  AssignClass (354c3c08-a50c-4a99-a23a-dfbc380ca8c2)
 Call ID: 354c3c08-a50c-4a99-a23a-dfbc380ca8c2
  Args:
    type: :Man
    source: Felipe_VI
  AssignClass (2d1f7bdc-19ea-419c-8987-7270f9210dbd)
 Call ID: 2d1f7bdc-19ea-419c-8987-7270f9210dbd
  Args:
    type: :Person
    source: Letizia
  AssignClass (59424593-1114-4aaf-9fa2-62573a04c4fd)
 Call ID: 59424593-1114-4aaf-9fa2-62573a04c4fd
  Args:
    type: :Woman
    source: Letizia
  AssignClass (7c250a93-5422-4c3b-887e-99d516d89e45)
 Call ID: 7c250a93-5422-4c3b-887e-99d516d89e45
  Args:
    type: :Person
    source: Leonor_of_Spain
  AssignClass (7355d4cd-0ceb-461b-8a48-2e7e0c4ab965)
 Call ID: 7355d4cd-0ceb-461b-8a48-2e7e0c4ab965
  Args:
    type: :Woman
    source: Leonor_of_Spain
  AssignClass (727f4f7d-2b66-4cad-af9e-d79bb6ec25a0)
 Call ID: 727f4f7d-2b66-4cad-af9e-d79bb6ec25a0
  Args:
    type: :Person
    source: Juan_Carlos_I
  AssignClass (205183a4-625b-4a45-a5f3-d66a9b529f7e)
 Call ID: 205183a4-625b-4a45-a5f3-d66a9b529f7e
  Args:
    type: :Man
    source: Juan_Carlos_I
  AssignClass (7e3b7192-c9e9-40a0-8bba-a59babffb3c8)
 Call ID: 7e3b7192-c9e9-40a0-8bba-a59babffb3c8
  Args:
    type: :Person
    source: Queen_Sofía
  AssignClass (d6700788-01be-47fa-9cec-71fce7f350fe)
 Call ID: d6700788-01be-47fa-9cec-71fce7f350fe
  Args:
    type: :Woman
    source: Queen_Sofía
  AddTriple (c41e467f-a1ae-447d-b3f5-527530355103)
 Call ID: c41e467f-a1ae-447d-b3f5-527530355103
  Args:
    source: Sofía_of_Spain
    relation: :hasFather
    target: Felipe_VI
  AddTriple (5ca28678-e27a-4520-8880-bb497bd6707d)
 Call ID: 5ca28678-e27a-4520-8880-bb497bd6707d
  Args:
    source: Sofía_of_Spain
    relation: :hasMother
    target: Letizia
  AddTriple (c868ae94-9a77-4b65-b1ae-d20c1299f366)
 Call ID: c868ae94-9a77-4b65-b1ae-d20c1299f366
  Args:
    target: Leonor_of_Spain
    source: Sofía_of_Spain
    relation: :hasSister
  AddTriple (2703d05e-2fc5-4f53-971a-923157986e9a)
 Call ID: 2703d05e-2fc5-4f53-971a-923157986e9a
  Args:
    source: Felipe_VI
    relation: :hasFather
    target: Juan_Carlos_I
  AddTriple (0b4b05bc-f580-4ae6-90fe-cf699b0dd7de)
 Call ID: 0b4b05bc-f580-4ae6-90fe-cf699b0dd7de
  Args:
    target: Queen_Sofía
    relation: :hasMother
    source: Felipe_VI
  AddLiteral (862759a9-50b1-4872-9ec4-7aff38be3084)
 Call ID: 862759a9-50b1-4872-9ec4-7aff38be3084
  Args:
    literal_type: xsd:integer
    source: Sofía_of_Spain
    relation: :hasBirthYear
    literal_value: 2007
  Finish (691cd2ad-6d0e-4339-83cc-8d588363d292)
 Call ID: 691cd2ad-6d0e-4339-83cc-8d588363d292
  Args: