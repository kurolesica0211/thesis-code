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
  AssignClass (e57d267e-4914-4544-a8b6-1b1aece81847)
 Call ID: e57d267e-4914-4544-a8b6-1b1aece81847
  Args:
    source: PrinceFerdinandPius
    type: :Man
  AssignClass (28dc5e8a-0d96-4824-9119-0eba0fe7f874)
 Call ID: 28dc5e8a-0d96-4824-9119-0eba0fe7f874
  Args:
    type: :Man
    source: PrinceAlfonsoCountOfCaserta
  AssignClass (eb7fc549-0075-4367-8353-59952f7dcc98)
 Call ID: eb7fc549-0075-4367-8353-59952f7dcc98
  Args:
    type: :Woman
    source: PrincessMariaAntonietta
  AssignClass (2848f403-bc75-4a78-b9cf-2ea420fa01f9)
 Call ID: 2848f403-bc75-4a78-b9cf-2ea420fa01f9
  Args:
    type: :Man
    source: FerdinandIIOfTheTwoSicilies
  AssignClass (dd90a9b7-6ad1-4782-8636-ae34597992a2)
 Call ID: dd90a9b7-6ad1-4782-8636-ae34597992a2
  Args:
    type: :Man
    source: PrinceCarlosOfBourbonTwoSicilies
  AssignClass (23969272-6bcc-431d-a87c-db14f2519230)
 Call ID: 23969272-6bcc-431d-a87c-db14f2519230
  Args:
    source: MariaImmaculata
    type: :Woman
  AssignClass (f81bdd60-82a8-4bc9-bb68-43abebd583d0)
 Call ID: f81bdd60-82a8-4bc9-bb68-43abebd583d0
  Args:
    type: :Woman
    source: PrincessJohannGeorgOfSaxony
  AssignClass (847c84f0-5b5a-48df-850a-486d93049c6d)
 Call ID: 847c84f0-5b5a-48df-850a-486d93049c6d
  Args:
    source: MariaCristina
    type: :Woman
  AssignClass (23ed835a-3355-43cb-bd36-1acddd50d18e)
 Call ID: 23ed835a-3355-43cb-bd36-1acddd50d18e
  Args:
    type: :Woman
    source: ArchduchessPeterFerdinandOfAustria
  AssignClass (e21e2aef-b4be-4607-92b7-b7ac836121bf)
 Call ID: e21e2aef-b4be-4607-92b7-b7ac836121bf
  Args:
    source: MariaDiGrazia
    type: :Woman
  AssignClass (c53fe6bc-e6be-4ae5-876b-fa283a48efd1)
 Call ID: c53fe6bc-e6be-4ae5-876b-fa283a48efd1
  Args:
    type: :Woman
    source: PrincessImperialOfBrazil
  AssignClass (ac955114-bb34-4e39-9988-b91933f7e98c)
 Call ID: ac955114-bb34-4e39-9988-b91933f7e98c
  Args:
    type: :Man
    source: PrinceRanieriDukeOfCastro
  AssignClass (d993334f-98bc-4b4c-9798-7783375cfa38)
 Call ID: d993334f-98bc-4b4c-9798-7783375cfa38
  Args:
    type: :Man
    source: PrincePhilipOfBourbonTwoSicilies
  AssignClass (733b9b59-3ef2-494e-aecf-104e4e0f7147)
 Call ID: 733b9b59-3ef2-494e-aecf-104e4e0f7147
  Args:
    type: :Man
    source: PrinceGabrielOfBourbonTwoSicilies
  AssignClass (975d23ee-971c-4728-bd9b-ba74f29e9095)
 Call ID: 975d23ee-971c-4728-bd9b-ba74f29e9095
  Args:
    type: :Woman
    source: PrincessMariaLudwigaTheresiaOfBavaria
  AssignClass (641ae97f-0f2a-4105-8c3c-811b46c01ab5)
 Call ID: 641ae97f-0f2a-4105-8c3c-811b46c01ab5
  Args:
    source: KingLudwigIIIOfBavaria
    type: :Man
  AssignClass (a5548190-7a9b-4e8e-9faa-120f8b3ce5ca)
 Call ID: a5548190-7a9b-4e8e-9faa-120f8b3ce5ca
  Args:
    type: :Man
    source: InfanteAlfonsoDukeOfCalabria
  AssignClass (bcca4527-3d63-4984-a9a9-bbccdca3acf1)
 Call ID: bcca4527-3d63-4984-a9a9-bbccdca3acf1
  Args:
    source: HenriCountOfParis
    type: :Man
  AssignClass (51544fba-e44f-4981-939e-82a3503dc19c)
 Call ID: 51544fba-e44f-4981-939e-82a3503dc19c
  Args:
    source: MariaDeLasMercedesPrincessOfAsturias
    type: :Woman
  AddLiteral (e044f23f-0865-4ad3-8a35-a8823ee04323)
 Call ID: e044f23f-0865-4ad3-8a35-a8823ee04323
  Args:
    literal_type: xsd:integer
    literal_value: 1869
    source: PrinceFerdinandPius
    relation: :hasBirthYear
  AddLiteral (2866c356-25c3-45bc-b522-c604b6e69135)
 Call ID: 2866c356-25c3-45bc-b522-c604b6e69135
  Args:
    relation: :hasDeathYear
    source: PrinceFerdinandPius
    literal_value: 1960
    literal_type: xsd:integer
  AddTriple (44f96a9d-244b-4484-a041-6cf8e85767d0)
 Call ID: 44f96a9d-244b-4484-a041-6cf8e85767d0
  Args:
    relation: :hasFather
    target: PrinceAlfonsoCountOfCaserta
    source: PrinceFerdinandPius
  AddTriple (6ddc7c8e-df0c-43d0-9e45-aa1fde791ed4)
 Call ID: 6ddc7c8e-df0c-43d0-9e45-aa1fde791ed4
  Args:
    relation: :hasMother
    target: PrincessMariaAntonietta
    source: PrinceFerdinandPius
  AddTriple (bb6b2dc5-5cea-4bee-8da1-e4b1ed7193a9)
 Call ID: bb6b2dc5-5cea-4bee-8da1-e4b1ed7193a9
  Args:
    relation: :hasAncestor
    source: PrinceFerdinandPius
    target: FerdinandIIOfTheTwoSicilies
  AddTriple (4e66574d-e01f-4deb-98e4-2801ea045b76)
 Call ID: 4e66574d-e01f-4deb-98e4-2801ea045b76
  Args:
    relation: :isBrotherOf
    target: PrinceCarlosOfBourbonTwoSicilies
    source: PrinceFerdinandPius
  AddTriple (24148fa9-2b37-4c22-a70e-a436b1028f54)
 Call ID: 24148fa9-2b37-4c22-a70e-a436b1028f54
  Args:
    relation: :isBrotherOf
    target: PrinceRanieriDukeOfCastro
    source: PrinceFerdinandPius
  AddTriple (89dc6ae3-4798-4052-a622-9cf3667d0275)
 Call ID: 89dc6ae3-4798-4052-a622-9cf3667d0275
  Args:
    source: PrinceFerdinandPius
    target: PrincePhilipOfBourbonTwoSicilies
    relation: :isBrotherOf
  AddTriple (911afedd-c3c1-449c-aa4c-30698ddfca68)
 Call ID: 911afedd-c3c1-449c-aa4c-30698ddfca68
  Args:
    target: PrinceGabrielOfBourbonTwoSicilies
    source: PrinceFerdinandPius
    relation: :isBrotherOf
  AddTriple (c344ae63-ba8d-4c16-b794-6c71a09dcd0c)
 Call ID: c344ae63-ba8d-4c16-b794-6c71a09dcd0c
  Args:
    relation: :isSisterOf
    target: MariaImmaculata
    source: PrinceFerdinandPius
  AddTriple (37e66d59-6754-4086-a21e-3462843bf0cd)
 Call ID: 37e66d59-6754-4086-a21e-3462843bf0cd
  Args:
    relation: :isSisterOf
    source: PrinceFerdinandPius
    target: PrincessJohannGeorgOfSaxony
  AddTriple (9233670a-5606-4943-948f-ca4d7e2e0634)
 Call ID: 9233670a-5606-4943-948f-ca4d7e2e0634
  Args:
    target: MariaCristina
    source: PrinceFerdinandPius
    relation: :isSisterOf
  AddTriple (b4746144-ba8f-4d68-ac94-7138da9cb557)
 Call ID: b4746144-ba8f-4d68-ac94-7138da9cb557
  Args:
    target: ArchduchessPeterFerdinandOfAustria
    source: PrinceFerdinandPius
    relation: :isSisterOf
  AddTriple (88b9ce3b-00b0-4be6-bde7-ba97eb48dfac)
 Call ID: 88b9ce3b-00b0-4be6-bde7-ba97eb48dfac
  Args:
    relation: :isSisterOf
    target: MariaDiGrazia
    source: PrinceFerdinandPius
  AddTriple (ae5a801e-eec0-4c03-9c4d-418966c36321)
 Call ID: ae5a801e-eec0-4c03-9c4d-418966c36321
  Args:
    target: PrincessImperialOfBrazil
    source: PrinceFerdinandPius
    relation: :isSisterOf
  AddTriple (c0abb950-7924-41c7-b031-b6f50bed9c3f)
 Call ID: c0abb950-7924-41c7-b031-b6f50bed9c3f
  Args:
    relation: :hasFather
    source: PrincessMariaLudwigaTheresiaOfBavaria
    target: KingLudwigIIIOfBavaria
  AddTriple (ad6577f2-f9bf-41d9-862c-4cc4097994da)
 Call ID: ad6577f2-f9bf-41d9-862c-4cc4097994da
  Args:
    source: PrinceFerdinandPius
    target: PrincessMariaLudwigaTheresiaOfBavaria
    relation: :hasRelation
  AddLiteral (cdeb6b9a-8f52-4b5a-aed3-55ee51c0b130)
 Call ID: cdeb6b9a-8f52-4b5a-aed3-55ee51c0b130
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    source: PrinceFerdinandPius
    literal_value: 1897
  AddTriple (b22e6a74-35a2-4a8a-b545-fa5ede4b172e)
 Call ID: b22e6a74-35a2-4a8a-b545-fa5ede4b172e
  Args:
    target: PrinceAlfonsoCountOfCaserta
    source: PrinceCarlosOfBourbonTwoSicilies
    relation: :hasFather
  AddTriple (c9a4a954-5545-4645-be59-8480bf64028e)
 Call ID: c9a4a954-5545-4645-be59-8480bf64028e
  Args:
    relation: :hasMother
    source: PrinceCarlosOfBourbonTwoSicilies
    target: PrincessMariaAntonietta
  AddTriple (76126d24-99b1-435f-961f-ef556064d1aa)
 Call ID: 76126d24-99b1-435f-961f-ef556064d1aa
  Args:
    relation: :hasFather
    target: PrinceAlfonsoCountOfCaserta
    source: PrinceRanieriDukeOfCastro
  AddTriple (6bdd0df6-866f-4270-9866-46487327b969)
 Call ID: 6bdd0df6-866f-4270-9866-46487327b969
  Args:
    relation: :hasMother
    source: PrinceRanieriDukeOfCastro
    target: PrincessMariaAntonietta
  AddTriple (81cc2c92-d11d-4eb9-9b5c-a9cb16abb59a)
 Call ID: 81cc2c92-d11d-4eb9-9b5c-a9cb16abb59a
  Args:
    target: PrinceCarlosOfBourbonTwoSicilies
    source: InfanteAlfonsoDukeOfCalabria
    relation: :hasFather
  Finish (7db7572d-8093-4285-96a9-5e065c917791)
 Call ID: 7db7572d-8093-4285-96a9-5e065c917791
  Args: