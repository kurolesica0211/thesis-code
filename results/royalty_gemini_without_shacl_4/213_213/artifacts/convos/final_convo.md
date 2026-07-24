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
  AssignClass (f6bc7119-fcbc-424d-b0e0-cb808b3b2d99)
 Call ID: f6bc7119-fcbc-424d-b0e0-cb808b3b2d99
  Args:
    type: :Man
    source: :Prince_Ferdinand_Pius
  AssignClass (48ea9a9e-6615-49fa-8db4-4f8e5c8c6b15)
 Call ID: 48ea9a9e-6615-49fa-8db4-4f8e5c8c6b15
  Args:
    source: :Prince_Ferdinand_Pius
    type: :Person
  AddLiteral (9fea04f2-a8b1-4e7f-a304-a6b83fbc405b)
 Call ID: 9fea04f2-a8b1-4e7f-a304-a6b83fbc405b
  Args:
    source: :Prince_Ferdinand_Pius
    literal_value: 1869
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (66278d10-b659-4f48-aa8a-96d95e24fc5c)
 Call ID: 66278d10-b659-4f48-aa8a-96d95e24fc5c
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1960
    source: :Prince_Ferdinand_Pius
  AssignClass (968c5f84-7b58-46df-bc60-c76c25fe344d)
 Call ID: 968c5f84-7b58-46df-bc60-c76c25fe344d
  Args:
    type: :Man
    source: :Prince_Alfonso_Count_of_Caserta
  AssignClass (75512858-3717-4e5d-9954-66601ab12e2f)
 Call ID: 75512858-3717-4e5d-9954-66601ab12e2f
  Args:
    source: :Prince_Alfonso_Count_of_Caserta
    type: :Person
  AssignClass (739d8228-347a-4aff-98c1-2ad65e241882)
 Call ID: 739d8228-347a-4aff-98c1-2ad65e241882
  Args:
    source: :Princess_Maria_Antonietta
    type: :Woman
  AssignClass (6fbd8faa-7bc7-4b83-a60e-42c0409a115d)
 Call ID: 6fbd8faa-7bc7-4b83-a60e-42c0409a115d
  Args:
    type: :Person
    source: :Princess_Maria_Antonietta
  AddTriple (aa517a1c-9b74-411d-8e43-bf40f7482213)
 Call ID: aa517a1c-9b74-411d-8e43-bf40f7482213
  Args:
    source: :Prince_Ferdinand_Pius
    target: :Prince_Alfonso_Count_of_Caserta
    relation: :hasFather
  AddTriple (62104fcd-b39a-4434-99e0-7c3208445b90)
 Call ID: 62104fcd-b39a-4434-99e0-7c3208445b90
  Args:
    relation: :hasMother
    source: :Prince_Ferdinand_Pius
    target: :Princess_Maria_Antonietta
  AssignClass (de9828fb-04fe-4611-b06e-5104c985c9a5)
 Call ID: de9828fb-04fe-4611-b06e-5104c985c9a5
  Args:
    source: :Ferdinand_II_of_the_Two_Sicilies
    type: :Man
  AssignClass (a791e75e-29bc-49a2-b6bc-02c8addea372)
 Call ID: a791e75e-29bc-49a2-b6bc-02c8addea372
  Args:
    source: :Ferdinand_II_of_the_Two_Sicilies
    type: :Person
  AddTriple (59a43d9e-4d0d-42b5-907b-24ddf35402f1)
 Call ID: 59a43d9e-4d0d-42b5-907b-24ddf35402f1
  Args:
    relation: :hasAncestor
    target: :Ferdinand_II_of_the_Two_Sicilies
    source: :Prince_Ferdinand_Pius
  AssignClass (be924ec3-88da-4167-8a2e-80ac81ee8cd5)
 Call ID: be924ec3-88da-4167-8a2e-80ac81ee8cd5
  Args:
    type: :Man
    source: :Prince_Carlos_of_Bourbon-Two_Sicilies
  AssignClass (dd0b7f0d-d8ae-4aa0-8562-b14eb4783d1d)
 Call ID: dd0b7f0d-d8ae-4aa0-8562-b14eb4783d1d
  Args:
    source: :Prince_Carlos_of_Bourbon-Two_Sicilies
    type: :Person
  AddTriple (30f6330c-a7c2-4a25-b548-a5af70b2aed0)
 Call ID: 30f6330c-a7c2-4a25-b548-a5af70b2aed0
  Args:
    relation: :isSiblingOf
    target: :Prince_Carlos_of_Bourbon-Two_Sicilies
    source: :Prince_Ferdinand_Pius
  AssignClass (5e3f029e-0302-4ad1-b11b-bd167b40bbe8)
 Call ID: 5e3f029e-0302-4ad1-b11b-bd167b40bbe8
  Args:
    type: :Woman
    source: :Princess_Maria_Immaculata
  AssignClass (a024b2d6-5869-499c-994e-d90199e6ecd7)
 Call ID: a024b2d6-5869-499c-994e-d90199e6ecd7
  Args:
    source: :Princess_Maria_Immaculata
    type: :Person
  AddTriple (8eca92db-5476-4f09-bf96-ad54efeec531)
 Call ID: 8eca92db-5476-4f09-bf96-ad54efeec531
  Args:
    relation: :isSiblingOf
    target: :Princess_Maria_Immaculata
    source: :Prince_Ferdinand_Pius
  AssignClass (715c7d4e-638e-41d0-8296-5528b273345a)
 Call ID: 715c7d4e-638e-41d0-8296-5528b273345a
  Args:
    source: :Princess_Maria_Cristina
    type: :Woman
  AssignClass (297ffdd8-2582-4672-813e-f0eee7ced012)
 Call ID: 297ffdd8-2582-4672-813e-f0eee7ced012
  Args:
    type: :Person
    source: :Princess_Maria_Cristina
  AddTriple (db724cb9-4587-443f-a4dc-1b08aea9f3bc)
 Call ID: db724cb9-4587-443f-a4dc-1b08aea9f3bc
  Args:
    relation: :isSiblingOf
    source: :Prince_Ferdinand_Pius
    target: :Princess_Maria_Cristina
  AssignClass (b4ad6954-3976-441f-86d2-915fec40acae)
 Call ID: b4ad6954-3976-441f-86d2-915fec40acae
  Args:
    type: :Woman
    source: :Princess_Maria_di_Grazia
  AssignClass (c9e2d8f6-61ae-45bf-a3dd-26d74fc615d2)
 Call ID: c9e2d8f6-61ae-45bf-a3dd-26d74fc615d2
  Args:
    source: :Princess_Maria_di_Grazia
    type: :Person
  AddTriple (ab0ad601-5f64-4783-bfd4-bb68aba596d6)
 Call ID: ab0ad601-5f64-4783-bfd4-bb68aba596d6
  Args:
    relation: :isSiblingOf
    target: :Princess_Maria_di_Grazia
    source: :Prince_Ferdinand_Pius
  AssignClass (0ea92ebe-19c9-4bf4-886e-d0521d225e09)
 Call ID: 0ea92ebe-19c9-4bf4-886e-d0521d225e09
  Args:
    source: :Prince_Ranieri_Duke_of_Castro
    type: :Man
  AssignClass (cc35e352-0471-49b4-9ed7-4a30cf3b4a98)
 Call ID: cc35e352-0471-49b4-9ed7-4a30cf3b4a98
  Args:
    type: :Person
    source: :Prince_Ranieri_Duke_of_Castro
  AddTriple (071bb874-81d8-4bd6-beb8-537b36751153)
 Call ID: 071bb874-81d8-4bd6-beb8-537b36751153
  Args:
    relation: :isSiblingOf
    source: :Prince_Ferdinand_Pius
    target: :Prince_Ranieri_Duke_of_Castro
  AssignClass (ba0b2d60-a6ae-44e1-b48b-c78c8cd20f49)
 Call ID: ba0b2d60-a6ae-44e1-b48b-c78c8cd20f49
  Args:
    source: :Prince_Philip_of_Bourbon-Two_Sicilies
    type: :Man
  AssignClass (ecbded72-9a92-4c24-a64e-73f21fa38653)
 Call ID: ecbded72-9a92-4c24-a64e-73f21fa38653
  Args:
    type: :Person
    source: :Prince_Philip_of_Bourbon-Two_Sicilies
  AddTriple (78981e56-cda8-4b68-8326-3beb8a5e4331)
 Call ID: 78981e56-cda8-4b68-8326-3beb8a5e4331
  Args:
    target: :Prince_Philip_of_Bourbon-Two_Sicilies
    source: :Prince_Ferdinand_Pius
    relation: :isSiblingOf
  AssignClass (c60571dd-2e21-495d-ae5e-0fc22294c4ea)
 Call ID: c60571dd-2e21-495d-ae5e-0fc22294c4ea
  Args:
    type: :Man
    source: :Prince_Gabriel_of_Bourbon-Two_Sicilies
  AssignClass (c72de9fa-b572-4830-a0ad-5352d960c4a8)
 Call ID: c72de9fa-b572-4830-a0ad-5352d960c4a8
  Args:
    type: :Person
    source: :Prince_Gabriel_of_Bourbon-Two_Sicilies
  AddTriple (73b97bcf-3576-4117-a3be-e24e1f6b2781)
 Call ID: 73b97bcf-3576-4117-a3be-e24e1f6b2781
  Args:
    source: :Prince_Ferdinand_Pius
    target: :Prince_Gabriel_of_Bourbon-Two_Sicilies
    relation: :isSiblingOf
  AssignClass (b7183a2e-d87b-47ef-a8d3-a090635ad325)
 Call ID: b7183a2e-d87b-47ef-a8d3-a090635ad325
  Args:
    source: :Princess_Maria_Ludwiga_Theresia_of_Bavaria
    type: :Woman
  AssignClass (143838a6-106c-4c92-9c98-63ea166461c9)
 Call ID: 143838a6-106c-4c92-9c98-63ea166461c9
  Args:
    type: :Person
    source: :Princess_Maria_Ludwiga_Theresia_of_Bavaria
  AddLiteral (628ab93e-8be5-4f4b-bf18-004032d5e152)
 Call ID: 628ab93e-8be5-4f4b-bf18-004032d5e152
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 1897
    source: :Prince_Ferdinand_Pius
  AddTriple (96e2c6a3-e837-4bd6-a008-da528f626d7d)
 Call ID: 96e2c6a3-e837-4bd6-a008-da528f626d7d
  Args:
    relation: :hasRelation
    source: :Prince_Ferdinand_Pius
    target: :Princess_Maria_Ludwiga_Theresia_of_Bavaria
  AssignClass (92c029a0-a9a1-47bd-bd87-c095833cfc24)
 Call ID: 92c029a0-a9a1-47bd-bd87-c095833cfc24
  Args:
    type: :Man
    source: :King_Ludwig_III_of_Bavaria
  AssignClass (9bcb6f63-1615-40dd-857b-70de25f73ba0)
 Call ID: 9bcb6f63-1615-40dd-857b-70de25f73ba0
  Args:
    source: :King_Ludwig_III_of_Bavaria
    type: :Person
  AddTriple (b1c28f0a-6fb6-411e-b77b-90cb2081d207)
 Call ID: b1c28f0a-6fb6-411e-b77b-90cb2081d207
  Args:
    relation: :hasFather
    source: :Princess_Maria_Ludwiga_Theresia_of_Bavaria
    target: :King_Ludwig_III_of_Bavaria
  AssignClass (9f5cd8e6-d64f-40ad-b06c-d368f626199a)
 Call ID: 9f5cd8e6-d64f-40ad-b06c-d368f626199a
  Args:
    type: :Man
    source: :Infante_Alfonso_Duke_of_Calabria
  AssignClass (d811a735-75ab-4a1e-a71a-2ce42328c66e)
 Call ID: d811a735-75ab-4a1e-a71a-2ce42328c66e
  Args:
    type: :Person
    source: :Infante_Alfonso_Duke_of_Calabria
  Finish (fb8d13f3-0bd6-41c9-b5cb-69c768b105a3)
 Call ID: fb8d13f3-0bd6-41c9-b5cb-69c768b105a3
  Args: