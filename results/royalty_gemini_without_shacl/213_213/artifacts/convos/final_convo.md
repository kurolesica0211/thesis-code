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
Prince Ferdinand Pius (Ferdinando Pio Maria), Duke of Calabria and Castro (25 July 1869, Rome – 7 January 1960, Lindau), was head of the House of Bourbon-Two Sicilies and pretender to the throne of the extinct Kingdom of the Two Sicilies from 1934 to 1960.
Family

Ferdinand was the eldest child of Prince Alfonso, Count of Caserta and his wife Princess Maria Antonietta of Bourbon-Two Sicilies.
He was a grandson of Ferdinand II of the Two Sicilies and an older brother of Prince Carlos of Bourbon-Two Sicilies, Maria Immaculata, Princess Johann Georg of Saxony, Maria Cristina, Archduchess Peter Ferdinand of Austria, Maria di Grazia, Princess Imperial of Brazil, Prince Ranieri, Duke of Castro, Prince Philip of Bourbon-Two Sicilies, and Prince Gabriel of Bourbon-Two Sicilies.
Marriage

Ferdinand married Princess Maria Ludwiga Theresia of Bavaria, daughter of King Ludwig III of Bavaria on 31 May 1897.
They had six children:


Ferdinand and Maria lived for many years at Villa Amsee, Lindau.
Disputed succession

Following Ferdinand's death, the headship of the House of Bourbon-Two Sicilies was claimed by both his nephew Infante Alfonso, Duke of Calabria, and his brother Prince Ranieri, Duke of Castro, and remains disputed between their descendants.
The basis of Alfonso’s claim was that his late father, Prince Carlos of Bourbon-Two Sicilies (1870–1949), had been Ferdinand's next oldest brother.
But Henri, Count of Paris, upheld the claim of Ferdinand's younger brother, Prince Ranieri, Duke of Castro (1883–1973), contending that Carlos had renounced his rights of succession for himself and his descendants in 1901 when he married the Spanish heiress presumptive María de las Mercedes, Princess of Asturias.
The Count of Paris was well aware that his own claim to the French throne depended on the validity of the renunciation in 1713 of Philip V of Spain, in favor of the junior House of Orléans.
In 1900, Prince Carlos had executed the Act of Cannes, in anticipation of his marriage to María de las Mercedes, and in 1901 he became a Spanish subject and accepted the title of Infante.
The position of Ranieri was that by so doing Carlos had renounced any claim to the throne of the Two Sicilies.
But Alfonso had a different interpretation, which was that the Act of Cannes would have taken effect only if Mercedes and Carlos had succeeded to the Spanish throne.
He also argued that the Act of Cannes was invalid under the succession rules of the house of Two Sicilies.
Military service

Ferdinand initially served in the Spanish Army, and after leaving service held the honorary rank of Comandante of the General Staff of the Spanish Army.
Feld-Artillerie-Regiment "Prinz Ferdinand von Bourbon, Herzog von Calabrien"), which was renamed in honor of him.



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
  AssignClass (758d2225-3cb3-483b-ba4f-95ddda64be81)
 Call ID: 758d2225-3cb3-483b-ba4f-95ddda64be81
  Args:
    type: :Man
    source: FerdinandPius
  AssignClass (5a1e7b1a-8316-41ba-bc4a-d6e9483e569b)
 Call ID: 5a1e7b1a-8316-41ba-bc4a-d6e9483e569b
  Args:
    type: :Person
    source: FerdinandPius
  AddLiteral (7240285d-0d8f-4dfd-8b0f-5dab5e23cf35)
 Call ID: 7240285d-0d8f-4dfd-8b0f-5dab5e23cf35
  Args:
    source: FerdinandPius
    literal_type: xsd:integer
    literal_value: 1869
    relation: :hasBirthYear
  AddLiteral (62805bfe-7325-478f-af8d-0714bc27737b)
 Call ID: 62805bfe-7325-478f-af8d-0714bc27737b
  Args:
    source: FerdinandPius
    relation: :hasDeathYear
    literal_value: 1960
    literal_type: xsd:integer
  AssignClass (2798dcd3-b679-4dac-8d27-1fde3e7bf5f1)
 Call ID: 2798dcd3-b679-4dac-8d27-1fde3e7bf5f1
  Args:
    type: :Man
    source: AlfonsoCountOfCaserta
  AssignClass (2d237a90-9055-4ddb-afa7-d86b65354aa2)
 Call ID: 2d237a90-9055-4ddb-afa7-d86b65354aa2
  Args:
    type: :Person
    source: AlfonsoCountOfCaserta
  AssignClass (3a1914bb-ef4e-46af-b57f-0e983cc336c2)
 Call ID: 3a1914bb-ef4e-46af-b57f-0e983cc336c2
  Args:
    source: MariaAntonietta
    type: :Woman
  AssignClass (73f2c6d4-194c-47f1-a979-a45230576ca6)
 Call ID: 73f2c6d4-194c-47f1-a979-a45230576ca6
  Args:
    type: :Person
    source: MariaAntonietta
  AddTriple (94659799-b47f-4b9d-9491-91a5381cb2b4)
 Call ID: 94659799-b47f-4b9d-9491-91a5381cb2b4
  Args:
    target: AlfonsoCountOfCaserta
    relation: :hasFather
    source: FerdinandPius
  AddTriple (10cc9146-aaa6-4923-99f9-0e5f2571c2a2)
 Call ID: 10cc9146-aaa6-4923-99f9-0e5f2571c2a2
  Args:
    source: FerdinandPius
    relation: :hasMother
    target: MariaAntonietta
  AssignClass (1e412b04-1573-42b8-959a-bb57f915cfbe)
 Call ID: 1e412b04-1573-42b8-959a-bb57f915cfbe
  Args:
    source: FerdinandII
    type: :Man
  AssignClass (c298bac8-c017-4b4b-bde2-096e4fbb2cf7)
 Call ID: c298bac8-c017-4b4b-bde2-096e4fbb2cf7
  Args:
    source: FerdinandII
    type: :Person
  AddTriple (91164075-0a0a-46ce-9577-4284b0346eae)
 Call ID: 91164075-0a0a-46ce-9577-4284b0346eae
  Args:
    target: FerdinandII
    relation: :hasFather
    source: AlfonsoCountOfCaserta
  AssignClass (5baeef76-8195-4cc1-90dc-b46a145ab2ac)
 Call ID: 5baeef76-8195-4cc1-90dc-b46a145ab2ac
  Args:
    source: CarlosBourbonTwoSicilies
    type: :Man
  AssignClass (6fb6ec6a-a86d-4678-929d-c1c5c754db71)
 Call ID: 6fb6ec6a-a86d-4678-929d-c1c5c754db71
  Args:
    source: CarlosBourbonTwoSicilies
    type: :Person
  AddTriple (5f0e3e3e-c78c-4cab-868c-8a74f228c96b)
 Call ID: 5f0e3e3e-c78c-4cab-868c-8a74f228c96b
  Args:
    relation: :isSiblingOf
    target: CarlosBourbonTwoSicilies
    source: FerdinandPius
  AssignClass (54cd3739-5192-4343-8225-2f372899ac25)
 Call ID: 54cd3739-5192-4343-8225-2f372899ac25
  Args:
    source: MariaImmaculata
    type: :Woman
  AssignClass (bd419e1c-a624-48ae-8019-1ceab59043da)
 Call ID: bd419e1c-a624-48ae-8019-1ceab59043da
  Args:
    source: MariaImmaculata
    type: :Person
  AddTriple (d05583a1-561e-46c6-93c3-c031aa1384e6)
 Call ID: d05583a1-561e-46c6-93c3-c031aa1384e6
  Args:
    relation: :isSiblingOf
    target: MariaImmaculata
    source: FerdinandPius
  AssignClass (5e1651b6-4167-4c95-bf76-600c95a866c6)
 Call ID: 5e1651b6-4167-4c95-bf76-600c95a866c6
  Args:
    type: :Woman
    source: MariaCristina
  AssignClass (24bde166-756b-41ce-bb74-92027053cbd7)
 Call ID: 24bde166-756b-41ce-bb74-92027053cbd7
  Args:
    source: MariaCristina
    type: :Person
  AddTriple (6aa2fc17-0301-437c-bb6b-3b7e991a657e)
 Call ID: 6aa2fc17-0301-437c-bb6b-3b7e991a657e
  Args:
    source: FerdinandPius
    target: MariaCristina
    relation: :isSiblingOf
  AssignClass (dfa9165c-d314-4aa5-a903-172e8ed73eec)
 Call ID: dfa9165c-d314-4aa5-a903-172e8ed73eec
  Args:
    type: :Woman
    source: MariaDiGrazia
  AssignClass (08c12270-3170-4279-b8d9-f0102b376663)
 Call ID: 08c12270-3170-4279-b8d9-f0102b376663
  Args:
    source: MariaDiGrazia
    type: :Person
  AddTriple (3c29e679-3d31-460c-8266-c441a347ea48)
 Call ID: 3c29e679-3d31-460c-8266-c441a347ea48
  Args:
    source: FerdinandPius
    relation: :isSiblingOf
    target: MariaDiGrazia
  AssignClass (59ab6ee0-e485-4787-b576-cbde923118bf)
 Call ID: 59ab6ee0-e485-4787-b576-cbde923118bf
  Args:
    source: RanieriDukeOfCastro
    type: :Man
  AssignClass (37c5728b-493e-4781-89f1-258d0aa1d21e)
 Call ID: 37c5728b-493e-4781-89f1-258d0aa1d21e
  Args:
    type: :Person
    source: RanieriDukeOfCastro
  AddTriple (518061e3-bcb6-45dc-a3d1-22b7a58d1e39)
 Call ID: 518061e3-bcb6-45dc-a3d1-22b7a58d1e39
  Args:
    source: FerdinandPius
    target: RanieriDukeOfCastro
    relation: :isSiblingOf
  AssignClass (084726fa-f363-4fe8-9cbd-cc4103288000)
 Call ID: 084726fa-f363-4fe8-9cbd-cc4103288000
  Args:
    source: PhilipBourbonTwoSicilies
    type: :Man
  AssignClass (d1cec0d7-6776-4234-b026-0a8d68f0f332)
 Call ID: d1cec0d7-6776-4234-b026-0a8d68f0f332
  Args:
    type: :Person
    source: PhilipBourbonTwoSicilies
  AddTriple (786a27ad-d2fe-4c0d-a06b-5475e7a14905)
 Call ID: 786a27ad-d2fe-4c0d-a06b-5475e7a14905
  Args:
    source: FerdinandPius
    relation: :isSiblingOf
    target: PhilipBourbonTwoSicilies
  AssignClass (4f6b3dcf-78a3-44ca-88d9-10a64f75decb)
 Call ID: 4f6b3dcf-78a3-44ca-88d9-10a64f75decb
  Args:
    source: GabrielBourbonTwoSicilies
    type: :Man
  AssignClass (0d9a9821-a2c2-43dc-9d2b-fad3ab0a50f8)
 Call ID: 0d9a9821-a2c2-43dc-9d2b-fad3ab0a50f8
  Args:
    source: GabrielBourbonTwoSicilies
    type: :Person
  AddTriple (d6d0c888-a591-4d7f-8241-6d5f40f808b2)
 Call ID: d6d0c888-a591-4d7f-8241-6d5f40f808b2
  Args:
    source: FerdinandPius
    relation: :isSiblingOf
    target: GabrielBourbonTwoSicilies
  AssignClass (4537f3bc-504d-4c3f-a3fc-4cb293bab0c9)
 Call ID: 4537f3bc-504d-4c3f-a3fc-4cb293bab0c9
  Args:
    source: MariaLudwigaTheresia
    type: :Woman
  AssignClass (c80bc8fe-f40e-4a07-bac8-8751fd4f6904)
 Call ID: c80bc8fe-f40e-4a07-bac8-8751fd4f6904
  Args:
    source: MariaLudwigaTheresia
    type: :Person
  AddTriple (0f85b21d-2b57-440b-a9a8-6633a8e594f2)
 Call ID: 0f85b21d-2b57-440b-a9a8-6633a8e594f2
  Args:
    target: MariaLudwigaTheresia
    relation: :hasRelation
    source: FerdinandPius
  AddLiteral (afb0b790-e58f-45c4-a04d-f987a1a32107)
 Call ID: afb0b790-e58f-45c4-a04d-f987a1a32107
  Args:
    relation: :hasMarriageYear
    literal_value: 1897
    literal_type: xsd:integer
    source: FerdinandPius
  AssignClass (4a02a402-42c7-49e7-a7ba-59fc9d14642e)
 Call ID: 4a02a402-42c7-49e7-a7ba-59fc9d14642e
  Args:
    type: :Man
    source: LudwigIII
  AssignClass (a666efb3-a508-42cf-b26b-cf518edbf22e)
 Call ID: a666efb3-a508-42cf-b26b-cf518edbf22e
  Args:
    source: LudwigIII
    type: :Person
  AddTriple (1c787823-14c5-4154-aff3-60b446b97415)
 Call ID: 1c787823-14c5-4154-aff3-60b446b97415
  Args:
    target: LudwigIII
    relation: :hasFather
    source: MariaLudwigaTheresia
  AssignClass (35a38053-e0a6-4b53-8352-5c75bd9dd304)
 Call ID: 35a38053-e0a6-4b53-8352-5c75bd9dd304
  Args:
    source: AlfonsoDukeOfCalabria
    type: :Man
  AssignClass (8453c708-d0b6-4cd2-8098-45b785c5a5e5)
 Call ID: 8453c708-d0b6-4cd2-8098-45b785c5a5e5
  Args:
    source: AlfonsoDukeOfCalabria
    type: :Person
  AddTriple (c6e2d80e-b3b9-41a9-94f7-97af15052c7c)
 Call ID: c6e2d80e-b3b9-41a9-94f7-97af15052c7c
  Args:
    source: AlfonsoDukeOfCalabria
    relation: :hasFather
    target: CarlosBourbonTwoSicilies
  Finish (4875a59f-e199-4c74-995b-b46511fa12ae)
 Call ID: 4875a59f-e199-4c74-995b-b46511fa12ae
  Args: