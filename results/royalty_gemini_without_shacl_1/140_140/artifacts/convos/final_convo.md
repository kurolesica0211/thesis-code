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
  AssignClass (cd08c5e3-94bc-465e-a98e-ef49bc2a12f2)
 Call ID: cd08c5e3-94bc-465e-a98e-ef49bc2a12f2
  Args:
    type: :Man
    source: :FerdinandPius
  AssignClass (a17bff01-2d8f-45a3-bbd2-0e61d8f636cd)
 Call ID: a17bff01-2d8f-45a3-bbd2-0e61d8f636cd
  Args:
    source: :FerdinandPius
    type: :Person
  AddLiteral (c1d99092-3c04-4a16-b909-8b87cda5c55e)
 Call ID: c1d99092-3c04-4a16-b909-8b87cda5c55e
  Args:
    source: :FerdinandPius
    literal_value: 1869
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (ad73cb97-004c-46cd-886d-ec1fbb1c52c1)
 Call ID: ad73cb97-004c-46cd-886d-ec1fbb1c52c1
  Args:
    literal_value: 1960
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: :FerdinandPius
  AssignClass (8a2a996e-f6d6-4141-aa82-e49d7e010985)
 Call ID: 8a2a996e-f6d6-4141-aa82-e49d7e010985
  Args:
    type: :Man
    source: :AlfonsoCountOfCaserta
  AssignClass (f13b59ca-2338-4ece-a570-3613a297ccba)
 Call ID: f13b59ca-2338-4ece-a570-3613a297ccba
  Args:
    source: :AlfonsoCountOfCaserta
    type: :Person
  AssignClass (fc40e5cc-6f41-40f5-b0b0-717cdff7b454)
 Call ID: fc40e5cc-6f41-40f5-b0b0-717cdff7b454
  Args:
    source: :MariaAntonietta
    type: :Woman
  AssignClass (c4ee6e48-68c1-4748-b2fa-ad345c1489c0)
 Call ID: c4ee6e48-68c1-4748-b2fa-ad345c1489c0
  Args:
    source: :MariaAntonietta
    type: :Person
  AddTriple (0449f494-3780-4d6d-97c9-f363e9810271)
 Call ID: 0449f494-3780-4d6d-97c9-f363e9810271
  Args:
    source: :FerdinandPius
    target: :AlfonsoCountOfCaserta
    relation: :hasFather
  AddTriple (c9d21cee-678f-4759-a5e1-91f09125d245)
 Call ID: c9d21cee-678f-4759-a5e1-91f09125d245
  Args:
    relation: :hasMother
    target: :MariaAntonietta
    source: :FerdinandPius
  AssignClass (df59073d-6c4c-47f0-a315-60abf079dd18)
 Call ID: df59073d-6c4c-47f0-a315-60abf079dd18
  Args:
    source: :FerdinandII
    type: :Man
  AssignClass (75c3854b-417c-4f06-b67b-7c7dae661b35)
 Call ID: 75c3854b-417c-4f06-b67b-7c7dae661b35
  Args:
    type: :Person
    source: :FerdinandII
  AddTriple (e8a46103-0c08-45d0-9ac0-0226b8234681)
 Call ID: e8a46103-0c08-45d0-9ac0-0226b8234681
  Args:
    source: :FerdinandPius
    relation: :hasAncestor
    target: :FerdinandII
  AssignClass (c54f0ca4-937d-4e8f-b912-6ab973a44114)
 Call ID: c54f0ca4-937d-4e8f-b912-6ab973a44114
  Args:
    type: :Man
    source: :CarlosBourbonTwoSicilies
  AssignClass (af987adf-fa97-4893-b9e1-678cec0ed5db)
 Call ID: af987adf-fa97-4893-b9e1-678cec0ed5db
  Args:
    type: :Person
    source: :CarlosBourbonTwoSicilies
  AssignClass (56be0602-3a47-4b52-ad4f-d239de266832)
 Call ID: 56be0602-3a47-4b52-ad4f-d239de266832
  Args:
    type: :Woman
    source: :MariaImmaculata
  AssignClass (9060063a-df6b-4690-afda-a2dd61265c94)
 Call ID: 9060063a-df6b-4690-afda-a2dd61265c94
  Args:
    type: :Person
    source: :MariaImmaculata
  AssignClass (9d57eaf5-97a1-48db-9bd2-70db4e3a2c22)
 Call ID: 9d57eaf5-97a1-48db-9bd2-70db4e3a2c22
  Args:
    type: :Woman
    source: :MariaCristina
  AssignClass (31054f5a-68f2-4c58-bf6c-de4ebcb117b6)
 Call ID: 31054f5a-68f2-4c58-bf6c-de4ebcb117b6
  Args:
    source: :MariaCristina
    type: :Person
  AssignClass (efbf85a3-41dc-4046-aebd-a8c86828b826)
 Call ID: efbf85a3-41dc-4046-aebd-a8c86828b826
  Args:
    source: :MariaDiGrazia
    type: :Woman
  AssignClass (f46cb4ae-b00b-4035-ac18-93a16aed6478)
 Call ID: f46cb4ae-b00b-4035-ac18-93a16aed6478
  Args:
    source: :MariaDiGrazia
    type: :Person
  AssignClass (6e7ecdc9-e5ee-45da-9534-3faa7263cd76)
 Call ID: 6e7ecdc9-e5ee-45da-9534-3faa7263cd76
  Args:
    type: :Man
    source: :RanieriDukeOfCastro
  AssignClass (fe46441e-99d4-41f5-8bf6-7af037cb7803)
 Call ID: fe46441e-99d4-41f5-8bf6-7af037cb7803
  Args:
    source: :RanieriDukeOfCastro
    type: :Person
  AssignClass (fe4028e7-6439-45d6-bd7f-d41e57c25bd4)
 Call ID: fe4028e7-6439-45d6-bd7f-d41e57c25bd4
  Args:
    type: :Man
    source: :PhilipBourbonTwoSicilies
  AssignClass (63781f35-0f87-413e-a5fc-becbd560047b)
 Call ID: 63781f35-0f87-413e-a5fc-becbd560047b
  Args:
    source: :PhilipBourbonTwoSicilies
    type: :Person
  AssignClass (d0ce1877-8e1b-44e4-a244-9f012419b30e)
 Call ID: d0ce1877-8e1b-44e4-a244-9f012419b30e
  Args:
    type: :Man
    source: :GabrielBourbonTwoSicilies
  AssignClass (0f8b9827-19ae-4b20-a691-14ba15375a94)
 Call ID: 0f8b9827-19ae-4b20-a691-14ba15375a94
  Args:
    type: :Person
    source: :GabrielBourbonTwoSicilies
  AddTriple (be6249fb-9c5a-4548-8fa2-208c38b1d8f3)
 Call ID: be6249fb-9c5a-4548-8fa2-208c38b1d8f3
  Args:
    source: :FerdinandPius
    target: :CarlosBourbonTwoSicilies
    relation: :isSiblingOf
  AddTriple (eec059e3-2191-4f2d-aace-f74f6b5c3740)
 Call ID: eec059e3-2191-4f2d-aace-f74f6b5c3740
  Args:
    target: :MariaImmaculata
    relation: :isSiblingOf
    source: :FerdinandPius
  AddTriple (3027e7cb-8b3f-4976-8442-32d2b165c81c)
 Call ID: 3027e7cb-8b3f-4976-8442-32d2b165c81c
  Args:
    relation: :isSiblingOf
    target: :MariaCristina
    source: :FerdinandPius
  AddTriple (6a87e921-24a5-4446-a25e-2b9fdbdfd811)
 Call ID: 6a87e921-24a5-4446-a25e-2b9fdbdfd811
  Args:
    target: :MariaDiGrazia
    relation: :isSiblingOf
    source: :FerdinandPius
  AddTriple (a2adeb38-7cda-414a-a40d-432031006b80)
 Call ID: a2adeb38-7cda-414a-a40d-432031006b80
  Args:
    relation: :isSiblingOf
    target: :RanieriDukeOfCastro
    source: :FerdinandPius
  AddTriple (4b23678a-166e-40c1-b1f8-21b3ca170f0f)
 Call ID: 4b23678a-166e-40c1-b1f8-21b3ca170f0f
  Args:
    source: :FerdinandPius
    target: :PhilipBourbonTwoSicilies
    relation: :isSiblingOf
  AddTriple (3744de47-bc9b-4ab5-a532-24156cf091fc)
 Call ID: 3744de47-bc9b-4ab5-a532-24156cf091fc
  Args:
    source: :FerdinandPius
    target: :GabrielBourbonTwoSicilies
    relation: :isSiblingOf
  AssignClass (ac9178a4-55ae-4e1d-97a4-d891d2232817)
 Call ID: ac9178a4-55ae-4e1d-97a4-d891d2232817
  Args:
    type: :Woman
    source: :MariaLudwigaTheresia
  AssignClass (21e6e699-4be1-4938-83d7-b3d576a68566)
 Call ID: 21e6e699-4be1-4938-83d7-b3d576a68566
  Args:
    type: :Person
    source: :MariaLudwigaTheresia
  AddTriple (e8462aa0-0f3e-4507-a566-a8d1099ad14f)
 Call ID: e8462aa0-0f3e-4507-a566-a8d1099ad14f
  Args:
    target: :MariaLudwigaTheresia
    relation: :hasRelation
    source: :FerdinandPius
  AddLiteral (92cf16fe-2014-4004-93fe-8cd7d257b221)
 Call ID: 92cf16fe-2014-4004-93fe-8cd7d257b221
  Args:
    source: :FerdinandPius
    relation: :hasMarriageYear
    literal_type: xsd:integer
    literal_value: 1897
  AssignClass (3198f68e-b6e4-4615-af05-a68702b7b7e6)
 Call ID: 3198f68e-b6e4-4615-af05-a68702b7b7e6
  Args:
    source: :LudwigIII
    type: :Man
  AssignClass (26a01a9f-956e-4b49-9b2c-7a426400ea45)
 Call ID: 26a01a9f-956e-4b49-9b2c-7a426400ea45
  Args:
    source: :LudwigIII
    type: :Person
  AddTriple (f816bf3a-2b76-44a2-98ed-32c6cb3f249e)
 Call ID: f816bf3a-2b76-44a2-98ed-32c6cb3f249e
  Args:
    relation: :hasFather
    target: :LudwigIII
    source: :MariaLudwigaTheresia
  AssignClass (7139c32a-351f-4ff7-abf6-6ec5b54ede2d)
 Call ID: 7139c32a-351f-4ff7-abf6-6ec5b54ede2d
  Args:
    source: :AlfonsoDukeOfCalabria
    type: :Man
  AssignClass (c8f695e8-f099-4444-923e-71c24166e776)
 Call ID: c8f695e8-f099-4444-923e-71c24166e776
  Args:
    source: :AlfonsoDukeOfCalabria
    type: :Person
  AddTriple (c719f508-b3d6-451e-b1b0-a11fb1b65b7e)
 Call ID: c719f508-b3d6-451e-b1b0-a11fb1b65b7e
  Args:
    relation: :hasFather
    target: :CarlosBourbonTwoSicilies
    source: :AlfonsoDukeOfCalabria
  Finish (b4fa3bb9-a78c-46bd-82c4-d9ec1aad1608)
 Call ID: b4fa3bb9-a78c-46bd-82c4-d9ec1aad1608
  Args: