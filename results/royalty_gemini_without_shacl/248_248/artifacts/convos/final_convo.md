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
The Duchess of Montpensier


The Count of ÉvreuxThe Countess of Évreux


Princess Béatrice


The Duke of OrléansThe Duchess of Orléans


The Dowager Countess of La Marche


The Countess of Schönborn-Buchheim


Princess Hélène, Countess of Limburg Stirum


The Dowager Duchess of Calabria


The Dowager Duchess of Württemberg


Princess Claude, Mrs. Gandolfi


Princess Chantal, Baroness of Sambucy de Sorgue


Duchess Marie-Thérèse of Württemberg (German: Marie Therese Nadejda Albertine Rosa Philippine Margarethe Christine Helene Josepha Martina Leopoldine Herzogin von Württemberg; born 12 November 1934) is a German-born aristocrat.
Family

Marie Thérèse was the fifth child and fourth daughter of Philipp Albrecht, Duke of Württemberg, and his second wife, Archduchess Rosa of Austria, Princess of Tuscany.
She was born at Altshausen Castle, Baden-Württemberg, Germany.
Marriage and issue

Marie Thérèse married Prince Henri, Count of Clermont, eldest son of Henri, Count of Paris, and Princess Isabelle of Orléans-Braganza, on 5 July 1957 in Dreux, France.
Three years later, her younger brother Carl, Duke of Württemberg, would marry Henri's younger sister, Princess Diane d'Orléans.
She received the title Duchess of Montpensier from her former father-in-law after divorce.



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
  AssignClass (7d04354c-558f-494b-81cc-4c27e0be4afc)
 Call ID: 7d04354c-558f-494b-81cc-4c27e0be4afc
  Args:
    source: Marie_Therese_of_Wurttemberg
    type: :Woman
  AssignClass (2ea52272-4238-4110-86c2-deb69386832a)
 Call ID: 2ea52272-4238-4110-86c2-deb69386832a
  Args:
    source: Marie_Therese_of_Wurttemberg
    type: :Person
  AddLiteral (fb68785e-6a8a-4d5c-b9f9-106bb965d58a)
 Call ID: fb68785e-6a8a-4d5c-b9f9-106bb965d58a
  Args:
    literal_type: xsd:integer
    literal_value: 1934
    relation: :hasBirthYear
    source: Marie_Therese_of_Wurttemberg
  AssignClass (fecad875-e8b4-4b34-bf06-4f60e551ba58)
 Call ID: fecad875-e8b4-4b34-bf06-4f60e551ba58
  Args:
    source: Philipp_Albrecht_Duke_of_Wurttemberg
    type: :Man
  AssignClass (1ccdf2b4-1c84-43a8-81ec-122b04df456d)
 Call ID: 1ccdf2b4-1c84-43a8-81ec-122b04df456d
  Args:
    type: :Ancestor
    source: Philipp_Albrecht_Duke_of_Wurttemberg
  AssignClass (69fbb2b6-2f0a-4bad-a07d-7b1d22588312)
 Call ID: 69fbb2b6-2f0a-4bad-a07d-7b1d22588312
  Args:
    type: :Woman
    source: Rosa_of_Austria
  AssignClass (cee3bbad-32bb-49b9-8df0-9014ba9382ea)
 Call ID: cee3bbad-32bb-49b9-8df0-9014ba9382ea
  Args:
    source: Rosa_of_Austria
    type: :Ancestor
  AddTriple (6fd1b0d3-b9de-4b14-b117-704720dc5444)
 Call ID: 6fd1b0d3-b9de-4b14-b117-704720dc5444
  Args:
    target: Marie_Therese_of_Wurttemberg
    relation: :isFatherOf
    source: Philipp_Albrecht_Duke_of_Wurttemberg
  AddTriple (d66ff9b8-c977-487d-bc03-c5e44d7a085a)
 Call ID: d66ff9b8-c977-487d-bc03-c5e44d7a085a
  Args:
    relation: :isMotherOf
    target: Marie_Therese_of_Wurttemberg
    source: Rosa_of_Austria
  AssignClass (840f6ee3-b1c0-4012-809e-3b719dee16e6)
 Call ID: 840f6ee3-b1c0-4012-809e-3b719dee16e6
  Args:
    type: :Man
    source: Henri_Count_of_Clermont
  AssignClass (9047b63c-ee49-4f58-b9e1-f5eb9f32d2c6)
 Call ID: 9047b63c-ee49-4f58-b9e1-f5eb9f32d2c6
  Args:
    source: Henri_Count_of_Clermont
    type: :Person
  AddTriple (abf3b378-0cdb-40e3-8cec-72e640a23b0c)
 Call ID: abf3b378-0cdb-40e3-8cec-72e640a23b0c
  Args:
    source: Marie_Therese_of_Wurttemberg
    relation: :hasRelation
    target: Henri_Count_of_Clermont
  AddLiteral (edfb10b6-1e91-489c-8766-e5b1c9c83b26)
 Call ID: edfb10b6-1e91-489c-8766-e5b1c9c83b26
  Args:
    relation: :hasMarriageYear
    literal_value: 1957
    literal_type: xsd:integer
    source: Marie_Therese_of_Wurttemberg
  AssignClass (65d4c280-a0ff-4d1d-93da-282b29c80311)
 Call ID: 65d4c280-a0ff-4d1d-93da-282b29c80311
  Args:
    type: :Man
    source: Henri_Count_of_Paris
  AssignClass (b58e9ecf-f4a4-4d3a-8d19-1c14671c7af7)
 Call ID: b58e9ecf-f4a4-4d3a-8d19-1c14671c7af7
  Args:
    source: Henri_Count_of_Paris
    type: :Ancestor
  AssignClass (95a8db89-68e9-49df-a477-40a6b46c67c4)
 Call ID: 95a8db89-68e9-49df-a477-40a6b46c67c4
  Args:
    source: Isabelle_of_Orleans_Braganza
    type: :Woman
  AssignClass (ce766484-6e31-44f5-932a-c68673648dea)
 Call ID: ce766484-6e31-44f5-932a-c68673648dea
  Args:
    type: :Ancestor
    source: Isabelle_of_Orleans_Braganza
  AddTriple (4dc82b2a-7425-4939-b877-7542c159c16c)
 Call ID: 4dc82b2a-7425-4939-b877-7542c159c16c
  Args:
    target: Henri_Count_of_Clermont
    relation: :isFatherOf
    source: Henri_Count_of_Paris
  AddTriple (6abbd017-528f-41d9-97f2-c33b5863d6d4)
 Call ID: 6abbd017-528f-41d9-97f2-c33b5863d6d4
  Args:
    target: Henri_Count_of_Clermont
    relation: :isMotherOf
    source: Isabelle_of_Orleans_Braganza
  AssignClass (8611f1eb-9bc8-4b13-b506-f5a6fe114eba)
 Call ID: 8611f1eb-9bc8-4b13-b506-f5a6fe114eba
  Args:
    type: :Man
    source: Carl_Duke_of_Wurttemberg
  AssignClass (5f87e315-02d3-48bb-9a9d-b5b5e934d33e)
 Call ID: 5f87e315-02d3-48bb-9a9d-b5b5e934d33e
  Args:
    source: Carl_Duke_of_Wurttemberg
    type: :Person
  AddTriple (c1da14ac-04eb-494b-a749-a7e4c2c77776)
 Call ID: c1da14ac-04eb-494b-a749-a7e4c2c77776
  Args:
    source: Carl_Duke_of_Wurttemberg
    relation: :isBrotherOf
    target: Marie_Therese_of_Wurttemberg
  AssignClass (9d4fd1c3-e802-41a3-8d91-a17e176b08d4)
 Call ID: 9d4fd1c3-e802-41a3-8d91-a17e176b08d4
  Args:
    source: Diane_dOrleans
    type: :Woman
  AssignClass (b4473c80-dd1a-437d-ae8b-5c4ca1ff1d46)
 Call ID: b4473c80-dd1a-437d-ae8b-5c4ca1ff1d46
  Args:
    type: :Person
    source: Diane_dOrleans
  AddTriple (25a123b2-cd30-43c0-8ece-2d63d3fc93db)
 Call ID: 25a123b2-cd30-43c0-8ece-2d63d3fc93db
  Args:
    source: Diane_dOrleans
    target: Henri_Count_of_Clermont
    relation: :isSisterOf
  AddTriple (3b9e812b-acef-41f4-94f1-5989a451991c)
 Call ID: 3b9e812b-acef-41f4-94f1-5989a451991c
  Args:
    source: Henri_Count_of_Paris
    relation: :isFatherOf
    target: Diane_dOrleans
  AddTriple (982166ce-e27e-48a8-80bf-ec6f6964b450)
 Call ID: 982166ce-e27e-48a8-80bf-ec6f6964b450
  Args:
    source: Isabelle_of_Orleans_Braganza
    relation: :isMotherOf
    target: Diane_dOrleans
  AddTriple (2c4808bc-b6dc-4021-a534-6aceed076b12)
 Call ID: 2c4808bc-b6dc-4021-a534-6aceed076b12
  Args:
    source: Carl_Duke_of_Wurttemberg
    relation: :hasRelation
    target: Diane_dOrleans
  Finish (87294d30-fe55-4575-bbfb-544a3668f083)
 Call ID: 87294d30-fe55-4575-bbfb-544a3668f083
  Args: