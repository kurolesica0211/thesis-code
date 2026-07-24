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
  AssignClass (17c6abab-9359-4217-9743-b3a1c2bf5a5d)
 Call ID: 17c6abab-9359-4217-9743-b3a1c2bf5a5d
  Args:
    source: :FerdinandPius
    type: :Man
  AssignClass (863d8909-9c93-4a53-a429-c3bcbeb0b0f7)
 Call ID: 863d8909-9c93-4a53-a429-c3bcbeb0b0f7
  Args:
    type: :Person
    source: :FerdinandPius
  AssignClass (d21649f7-4532-435d-a396-bebd10df6938)
 Call ID: d21649f7-4532-435d-a396-bebd10df6938
  Args:
    type: :Man
    source: :AlfonsoCountOfCaserta
  AssignClass (5277166a-7916-4db1-95db-6c2130d971a1)
 Call ID: 5277166a-7916-4db1-95db-6c2130d971a1
  Args:
    source: :AlfonsoCountOfCaserta
    type: :Person
  AssignClass (33243d40-0674-4f2a-b724-10110d607209)
 Call ID: 33243d40-0674-4f2a-b724-10110d607209
  Args:
    source: :MariaAntonietta
    type: :Woman
  AssignClass (4dbc99da-a6fb-49e7-ae89-ce757a29ceaf)
 Call ID: 4dbc99da-a6fb-49e7-ae89-ce757a29ceaf
  Args:
    source: :MariaAntonietta
    type: :Person
  AddLiteral (ff82c29b-4a8b-454e-9de8-9e433f5cc878)
 Call ID: ff82c29b-4a8b-454e-9de8-9e433f5cc878
  Args:
    relation: :hasBirthYear
    literal_value: 1869
    literal_type: xsd:integer
    source: :FerdinandPius
  AddLiteral (423f0479-41ff-45f9-a27f-d6639ea4daef)
 Call ID: 423f0479-41ff-45f9-a27f-d6639ea4daef
  Args:
    literal_type: xsd:integer
    source: :FerdinandPius
    relation: :hasDeathYear
    literal_value: 1960
  AddTriple (5565dc8e-206d-489d-a51d-822e1144e62d)
 Call ID: 5565dc8e-206d-489d-a51d-822e1144e62d
  Args:
    target: :AlfonsoCountOfCaserta
    source: :FerdinandPius
    relation: :hasFather
  AddTriple (386cdbad-a11a-41ab-9987-6cf93070ce67)
 Call ID: 386cdbad-a11a-41ab-9987-6cf93070ce67
  Args:
    relation: :hasMother
    target: :MariaAntonietta
    source: :FerdinandPius
  AssignClass (b460124c-f1f5-46cb-aa65-604e4cea4798)
 Call ID: b460124c-f1f5-46cb-aa65-604e4cea4798
  Args:
    source: :FerdinandII
    type: :Man
  AssignClass (adc98981-88e8-45ae-9e49-a6f11a1b58b2)
 Call ID: adc98981-88e8-45ae-9e49-a6f11a1b58b2
  Args:
    source: :FerdinandII
    type: :Person
  AddTriple (4e6ecc0f-5f6b-4536-933c-01e8e7186a4a)
 Call ID: 4e6ecc0f-5f6b-4536-933c-01e8e7186a4a
  Args:
    relation: :hasAncestor
    source: :FerdinandPius
    target: :FerdinandII
  AssignClass (3e93beba-1ca5-40aa-ba9d-243aed51ed8b)
 Call ID: 3e93beba-1ca5-40aa-ba9d-243aed51ed8b
  Args:
    source: :CarlosOfBourbonTwoSicilies
    type: :Man
  AssignClass (0aa69bab-9cfd-4c04-b400-1dc28aa3989e)
 Call ID: 0aa69bab-9cfd-4c04-b400-1dc28aa3989e
  Args:
    source: :CarlosOfBourbonTwoSicilies
    type: :Person
  AssignClass (beb44d5c-9a35-4d58-b5c3-aad4289d795d)
 Call ID: beb44d5c-9a35-4d58-b5c3-aad4289d795d
  Args:
    type: :Woman
    source: :MariaImmaculata
  AssignClass (fff4c50d-5c5f-4eab-bc51-fd44f61af0df)
 Call ID: fff4c50d-5c5f-4eab-bc51-fd44f61af0df
  Args:
    type: :Person
    source: :MariaImmaculata
  AssignClass (b0f5b34a-7f3f-49de-b47f-0e17ff9e42c3)
 Call ID: b0f5b34a-7f3f-49de-b47f-0e17ff9e42c3
  Args:
    type: :Woman
    source: :PrincessJohannGeorgOfSaxony
  AssignClass (ee60c685-afa3-4e6f-832e-c0b7eca0606f)
 Call ID: ee60c685-afa3-4e6f-832e-c0b7eca0606f
  Args:
    source: :PrincessJohannGeorgOfSaxony
    type: :Person
  AssignClass (9b87135e-14bb-4151-8b39-786d96bb0b1a)
 Call ID: 9b87135e-14bb-4151-8b39-786d96bb0b1a
  Args:
    type: :Woman
    source: :MariaCristina
  AssignClass (c3c88fd1-3589-42e7-8d14-49c2cb64e43d)
 Call ID: c3c88fd1-3589-42e7-8d14-49c2cb64e43d
  Args:
    source: :MariaCristina
    type: :Person
  AssignClass (5ed866bb-4cfc-4794-8020-70a7108c2585)
 Call ID: 5ed866bb-4cfc-4794-8020-70a7108c2585
  Args:
    type: :Woman
    source: :ArchduchessPeterFerdinandOfAustria
  AssignClass (3c346595-bdfa-446d-8375-7cc83b0a7522)
 Call ID: 3c346595-bdfa-446d-8375-7cc83b0a7522
  Args:
    source: :ArchduchessPeterFerdinandOfAustria
    type: :Person
  AssignClass (c3bd45ba-b97f-4bd9-991a-b16694612f67)
 Call ID: c3bd45ba-b97f-4bd9-991a-b16694612f67
  Args:
    source: :MariaDiGrazia
    type: :Woman
  AssignClass (c2d636bd-5b05-49ba-86ca-ea92ef8bde53)
 Call ID: c2d636bd-5b05-49ba-86ca-ea92ef8bde53
  Args:
    source: :MariaDiGrazia
    type: :Person
  AssignClass (dc9cc056-ac76-4450-9cdc-6c79d17d6be9)
 Call ID: dc9cc056-ac76-4450-9cdc-6c79d17d6be9
  Args:
    type: :Woman
    source: :PrincessImperialOfBrazil
  AssignClass (1c18d039-764b-40c1-9320-f2eb8df37177)
 Call ID: 1c18d039-764b-40c1-9320-f2eb8df37177
  Args:
    type: :Person
    source: :PrincessImperialOfBrazil
  AssignClass (b48346a9-46d3-4fec-b329-712cc492efac)
 Call ID: b48346a9-46d3-4fec-b329-712cc492efac
  Args:
    source: :RanieriDukeOfCastro
    type: :Man
  AssignClass (35a1d409-b2d6-435d-898f-6f034235cefb)
 Call ID: 35a1d409-b2d6-435d-898f-6f034235cefb
  Args:
    type: :Person
    source: :RanieriDukeOfCastro
  AssignClass (fc1b45d0-d831-4728-9b86-3bf421e5bffa)
 Call ID: fc1b45d0-d831-4728-9b86-3bf421e5bffa
  Args:
    source: :PhilipOfBourbonTwoSicilies
    type: :Man
  AssignClass (4e4f359b-ab7e-4908-9da3-bd1b9c40e9d8)
 Call ID: 4e4f359b-ab7e-4908-9da3-bd1b9c40e9d8
  Args:
    source: :PhilipOfBourbonTwoSicilies
    type: :Person
  AssignClass (fb4c90e4-58fa-4b26-b6e5-5b345d723781)
 Call ID: fb4c90e4-58fa-4b26-b6e5-5b345d723781
  Args:
    type: :Man
    source: :GabrielOfBourbonTwoSicilies
  AssignClass (1dc054cc-3a28-4b49-9e35-ff081bd84747)
 Call ID: 1dc054cc-3a28-4b49-9e35-ff081bd84747
  Args:
    source: :GabrielOfBourbonTwoSicilies
    type: :Person
  AddTriple (9b8fcca4-7694-45d5-b4e5-8396d289e923)
 Call ID: 9b8fcca4-7694-45d5-b4e5-8396d289e923
  Args:
    target: :CarlosOfBourbonTwoSicilies
    source: :FerdinandPius
    relation: :isSiblingOf
  AddTriple (dbc36182-7867-470a-966d-d68626882243)
 Call ID: dbc36182-7867-470a-966d-d68626882243
  Args:
    relation: :isSiblingOf
    source: :FerdinandPius
    target: :MariaImmaculata
  AddTriple (4cd13b74-60fa-40bb-ae7f-a13a2e6abc7d)
 Call ID: 4cd13b74-60fa-40bb-ae7f-a13a2e6abc7d
  Args:
    relation: :isSiblingOf
    target: :PrincessJohannGeorgOfSaxony
    source: :FerdinandPius
  AddTriple (9b8e98c9-442e-408e-aa6e-99022393c6eb)
 Call ID: 9b8e98c9-442e-408e-aa6e-99022393c6eb
  Args:
    relation: :isSiblingOf
    source: :FerdinandPius
    target: :MariaCristina
  AddTriple (ae484791-3eb8-4003-b07b-3562fd5e52fa)
 Call ID: ae484791-3eb8-4003-b07b-3562fd5e52fa
  Args:
    target: :ArchduchessPeterFerdinandOfAustria
    source: :FerdinandPius
    relation: :isSiblingOf
  AddTriple (de67e47c-c24d-4965-a674-07829f5f93c7)
 Call ID: de67e47c-c24d-4965-a674-07829f5f93c7
  Args:
    relation: :isSiblingOf
    source: :FerdinandPius
    target: :MariaDiGrazia
  AddTriple (507afae7-36db-4212-a591-51e3ea8a7275)
 Call ID: 507afae7-36db-4212-a591-51e3ea8a7275
  Args:
    relation: :isSiblingOf
    source: :FerdinandPius
    target: :PrincessImperialOfBrazil
  AddTriple (c47863f1-3115-41d6-bbc0-0a1dd02b00e9)
 Call ID: c47863f1-3115-41d6-bbc0-0a1dd02b00e9
  Args:
    relation: :isSiblingOf
    target: :RanieriDukeOfCastro
    source: :FerdinandPius
  AddTriple (ef5e6dfa-df9a-4155-9e1a-1eef0c152c93)
 Call ID: ef5e6dfa-df9a-4155-9e1a-1eef0c152c93
  Args:
    source: :FerdinandPius
    target: :PhilipOfBourbonTwoSicilies
    relation: :isSiblingOf
  AddTriple (5fda89f3-95b4-4464-a728-391c248283b1)
 Call ID: 5fda89f3-95b4-4464-a728-391c248283b1
  Args:
    relation: :isSiblingOf
    source: :FerdinandPius
    target: :GabrielOfBourbonTwoSicilies
  AssignClass (7fbd8e6b-5028-41fe-86ae-122aed4cd6ff)
 Call ID: 7fbd8e6b-5028-41fe-86ae-122aed4cd6ff
  Args:
    type: :Woman
    source: :MariaLudwigaTheresiaOfBavaria
  AssignClass (1afd56fe-babf-436b-b679-428acb33ead9)
 Call ID: 1afd56fe-babf-436b-b679-428acb33ead9
  Args:
    type: :Person
    source: :MariaLudwigaTheresiaOfBavaria
  AddLiteral (900f1a81-a23d-403f-a6ea-2f3b567f7cb7)
 Call ID: 900f1a81-a23d-403f-a6ea-2f3b567f7cb7
  Args:
    relation: :hasMarriageYear
    literal_value: 1897
    source: :FerdinandPius
    literal_type: xsd:integer
  AddTriple (5b254a6d-95be-40e5-9b0b-617e0ab0e30a)
 Call ID: 5b254a6d-95be-40e5-9b0b-617e0ab0e30a
  Args:
    relation: :hasRelation
    target: :MariaLudwigaTheresiaOfBavaria
    source: :FerdinandPius
  AssignClass (d315f5f3-9d12-4f2b-9bd5-5d6bcd3e04f0)
 Call ID: d315f5f3-9d12-4f2b-9bd5-5d6bcd3e04f0
  Args:
    source: :LudwigIIIOfBavaria
    type: :Man
  AssignClass (ea6b6e51-8a0b-47fe-86de-0d743b1cf075)
 Call ID: ea6b6e51-8a0b-47fe-86de-0d743b1cf075
  Args:
    type: :Person
    source: :LudwigIIIOfBavaria
  AddTriple (5184e70b-da03-40e7-b6f7-9437267b8a4d)
 Call ID: 5184e70b-da03-40e7-b6f7-9437267b8a4d
  Args:
    relation: :hasFather
    source: :MariaLudwigaTheresiaOfBavaria
    target: :LudwigIIIOfBavaria
  AssignClass (105eabf5-fa0f-4c64-92eb-011ddd421455)
 Call ID: 105eabf5-fa0f-4c64-92eb-011ddd421455
  Args:
    source: :InfanteAlfonsoDukeOfCalabria
    type: :Man
  AssignClass (42aa5abc-9f9a-45f8-83cd-e6e6fa97c2a5)
 Call ID: 42aa5abc-9f9a-45f8-83cd-e6e6fa97c2a5
  Args:
    type: :Person
    source: :InfanteAlfonsoDukeOfCalabria
  AddTriple (8266819b-baf7-448b-905a-afd3b34c755f)
 Call ID: 8266819b-baf7-448b-905a-afd3b34c755f
  Args:
    relation: :hasFather
    source: :InfanteAlfonsoDukeOfCalabria
    target: :CarlosOfBourbonTwoSicilies
  Finish (b912ed10-8d95-45d7-ba7e-b9b5fe7db139)
 Call ID: b912ed10-8d95-45d7-ba7e-b9b5fe7db139
  Args: