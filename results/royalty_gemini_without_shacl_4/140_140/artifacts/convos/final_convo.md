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
  AssignClass (6e459500-d5b9-477b-8ffb-a12420f36a20)
 Call ID: 6e459500-d5b9-477b-8ffb-a12420f36a20
  Args:
    source: :FerdinandPius
    type: :Man
  AssignClass (5d2e990d-f0a9-4949-8122-7b448b0ef673)
 Call ID: 5d2e990d-f0a9-4949-8122-7b448b0ef673
  Args:
    type: :Person
    source: :FerdinandPius
  AssignClass (24b049b2-94e9-4221-949d-cba679cb9c03)
 Call ID: 24b049b2-94e9-4221-949d-cba679cb9c03
  Args:
    source: :AlfonsoCountOfCaserta
    type: :Man
  AssignClass (86064629-c4ad-4b75-96fe-f15143359bf1)
 Call ID: 86064629-c4ad-4b75-96fe-f15143359bf1
  Args:
    type: :Person
    source: :AlfonsoCountOfCaserta
  AssignClass (f4876983-2ddb-4ac6-82b5-7e31d3709b07)
 Call ID: f4876983-2ddb-4ac6-82b5-7e31d3709b07
  Args:
    type: :Woman
    source: :MariaAntonietta
  AssignClass (0b0b3ab9-d6fb-48b1-8d5b-5a4f6bb35bf2)
 Call ID: 0b0b3ab9-d6fb-48b1-8d5b-5a4f6bb35bf2
  Args:
    type: :Person
    source: :MariaAntonietta
  AddLiteral (12f381b8-1748-4a44-b1c7-94bd332fea11)
 Call ID: 12f381b8-1748-4a44-b1c7-94bd332fea11
  Args:
    literal_type: xsd:positiveInteger
    relation: :hasBirthYear
    literal_value: 1869
    source: :FerdinandPius
  AddLiteral (f28856e7-9dbd-412b-8be5-80c7a9f1ee32)
 Call ID: f28856e7-9dbd-412b-8be5-80c7a9f1ee32
  Args:
    source: :FerdinandPius
    literal_value: 1960
    relation: :hasDeathYear
    literal_type: xsd:positiveInteger
  AddTriple (d2177356-2eed-42eb-97ab-fbfeb90f520f)
 Call ID: d2177356-2eed-42eb-97ab-fbfeb90f520f
  Args:
    source: :FerdinandPius
    target: :AlfonsoCountOfCaserta
    relation: :hasFather
  AddTriple (c7e56f03-527b-4d46-8624-d55f6047591a)
 Call ID: c7e56f03-527b-4d46-8624-d55f6047591a
  Args:
    target: :MariaAntonietta
    relation: :hasMother
    source: :FerdinandPius
  AddTriple (e65a838c-66cb-4114-a5bd-0aa9c16da47a)
 Call ID: e65a838c-66cb-4114-a5bd-0aa9c16da47a
  Args:
    relation: :hasFather
    target: :FerdinandII
    source: :FerdinandPius
  AssignClass (bba2a680-ddfe-453b-8d06-6159420f1e9a)
 Call ID: bba2a680-ddfe-453b-8d06-6159420f1e9a
  Args:
    source: :FerdinandII
    type: :Man
  AssignClass (b674c517-6d65-4759-8090-493ef8a7e8c0)
 Call ID: b674c517-6d65-4759-8090-493ef8a7e8c0
  Args:
    type: :Person
    source: :FerdinandII
  AssignClass (de90661a-3ef8-48f5-a0c4-3121bec38ae0)
 Call ID: de90661a-3ef8-48f5-a0c4-3121bec38ae0
  Args:
    type: :Woman
    source: :MariaLudwigaTheresia
  AssignClass (f5ec0c8b-d319-4682-a0df-c473b840c945)
 Call ID: f5ec0c8b-d319-4682-a0df-c473b840c945
  Args:
    source: :MariaLudwigaTheresia
    type: :Person
  AddLiteral (43461a3b-1ab3-4fc5-8b4b-d1aa45cb2c57)
 Call ID: 43461a3b-1ab3-4fc5-8b4b-d1aa45cb2c57
  Args:
    literal_value: 1897
    source: :FerdinandPius
    literal_type: xsd:positiveInteger
    relation: :hasMarriageYear
  AddTriple (cb533e35-adc3-436c-801f-df414ab26b4e)
 Call ID: cb533e35-adc3-436c-801f-df414ab26b4e
  Args:
    source: :FerdinandPius
    relation: :hasRelation
    target: :MariaLudwigaTheresia
  AssignClass (b1f164bd-f628-4aeb-ace7-241d51872b0f)
 Call ID: b1f164bd-f628-4aeb-ace7-241d51872b0f
  Args:
    type: :Man
    source: :LudwigIIIOfBavaria
  AssignClass (65ee27cc-6888-4585-8172-157877403224)
 Call ID: 65ee27cc-6888-4585-8172-157877403224
  Args:
    source: :LudwigIIIOfBavaria
    type: :Person
  AddTriple (ae72bb11-030a-41ac-b753-a68bf534676e)
 Call ID: ae72bb11-030a-41ac-b753-a68bf534676e
  Args:
    source: :MariaLudwigaTheresia
    target: :LudwigIIIOfBavaria
    relation: :hasFather
  AssignClass (4960edfa-0163-40ce-893e-717e640e3893)
 Call ID: 4960edfa-0163-40ce-893e-717e640e3893
  Args:
    type: :Man
    source: :CarlosOfBourbonTwoSicilies
  AssignClass (9ee37896-352e-43c8-9117-7272782d3d90)
 Call ID: 9ee37896-352e-43c8-9117-7272782d3d90
  Args:
    source: :CarlosOfBourbonTwoSicilies
    type: :Person
  AddTriple (4f67f93b-80f9-4f16-85bb-40dbed7ed3be)
 Call ID: 4f67f93b-80f9-4f16-85bb-40dbed7ed3be
  Args:
    source: :FerdinandPius
    relation: :isSiblingOf
    target: :CarlosOfBourbonTwoSicilies
  AssignClass (68d2627d-2903-4cdc-8fce-0c6d10699e9f)
 Call ID: 68d2627d-2903-4cdc-8fce-0c6d10699e9f
  Args:
    source: :RanieriDukeOfCastro
    type: :Man
  AssignClass (4048540a-1697-48d3-8279-f95de22de357)
 Call ID: 4048540a-1697-48d3-8279-f95de22de357
  Args:
    source: :RanieriDukeOfCastro
    type: :Person
  AddTriple (23dd3ada-6d44-47f2-be66-1921f64c9907)
 Call ID: 23dd3ada-6d44-47f2-be66-1921f64c9907
  Args:
    source: :FerdinandPius
    relation: :isSiblingOf
    target: :RanieriDukeOfCastro
  AssignClass (60223809-a6b5-4d2c-8a22-7c3cfea278de)
 Call ID: 60223809-a6b5-4d2c-8a22-7c3cfea278de
  Args:
    type: :Woman
    source: :MariaImmaculata
  AssignClass (78de79d8-98d2-484b-9109-3d6e23d43300)
 Call ID: 78de79d8-98d2-484b-9109-3d6e23d43300
  Args:
    type: :Person
    source: :MariaImmaculata
  AddTriple (a3cd97f7-cc8b-4e45-a607-bba3d6278f66)
 Call ID: a3cd97f7-cc8b-4e45-a607-bba3d6278f66
  Args:
    source: :FerdinandPius
    target: :MariaImmaculata
    relation: :isSiblingOf
  AssignClass (f4ab4961-9b62-48af-8b21-ac68bd8a0011)
 Call ID: f4ab4961-9b62-48af-8b21-ac68bd8a0011
  Args:
    source: :MariaCristina
    type: :Woman
  AssignClass (13837b0f-e20d-4947-8989-c8aa79a0c4d0)
 Call ID: 13837b0f-e20d-4947-8989-c8aa79a0c4d0
  Args:
    type: :Person
    source: :MariaCristina
  AddTriple (b7e03a59-855b-48ae-b4d5-c9d5343a308e)
 Call ID: b7e03a59-855b-48ae-b4d5-c9d5343a308e
  Args:
    source: :FerdinandPius
    target: :MariaCristina
    relation: :isSiblingOf
  AssignClass (dfe48696-a020-42da-b850-22789a0c6d91)
 Call ID: dfe48696-a020-42da-b850-22789a0c6d91
  Args:
    type: :Woman
    source: :MariaDiGrazia
  AssignClass (2b244f23-e52e-48c2-bb38-11474ea333df)
 Call ID: 2b244f23-e52e-48c2-bb38-11474ea333df
  Args:
    type: :Person
    source: :MariaDiGrazia
  AddTriple (fd705834-c9e1-4328-a9f9-0e2b1dc89dd0)
 Call ID: fd705834-c9e1-4328-a9f9-0e2b1dc89dd0
  Args:
    source: :FerdinandPius
    relation: :isSiblingOf
    target: :MariaDiGrazia
  AssignClass (5f322f8d-6eb2-4ce0-a3e8-21bb0c9972b8)
 Call ID: 5f322f8d-6eb2-4ce0-a3e8-21bb0c9972b8
  Args:
    source: :PhilipOfBourbonTwoSicilies
    type: :Man
  AssignClass (435d703c-c280-4dfa-8f66-1f6b03fef13f)
 Call ID: 435d703c-c280-4dfa-8f66-1f6b03fef13f
  Args:
    source: :PhilipOfBourbonTwoSicilies
    type: :Person
  AddTriple (a780e8ec-351b-49c9-97f2-0d68652ee4b9)
 Call ID: a780e8ec-351b-49c9-97f2-0d68652ee4b9
  Args:
    source: :FerdinandPius
    target: :PhilipOfBourbonTwoSicilies
    relation: :isSiblingOf
  AssignClass (309059d0-7858-4ce8-8308-63f570a57665)
 Call ID: 309059d0-7858-4ce8-8308-63f570a57665
  Args:
    type: :Man
    source: :GabrielOfBourbonTwoSicilies
  AssignClass (34d4c3b7-95c9-4a13-beb3-8d2a3bef830f)
 Call ID: 34d4c3b7-95c9-4a13-beb3-8d2a3bef830f
  Args:
    type: :Person
    source: :GabrielOfBourbonTwoSicilies
  AddTriple (baaf458b-af89-498f-befc-cb6179db1417)
 Call ID: baaf458b-af89-498f-befc-cb6179db1417
  Args:
    source: :FerdinandPius
    relation: :isSiblingOf
    target: :GabrielOfBourbonTwoSicilies
  Finish (f146f9dc-ca3a-4c8b-8029-bc704f3b8b90)
 Call ID: f146f9dc-ca3a-4c8b-8029-bc704f3b8b90
  Args: