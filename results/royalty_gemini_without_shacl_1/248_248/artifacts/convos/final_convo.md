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
  AssignClass (93ea6fb4-9f72-406f-87e1-13b3ef045fed)
 Call ID: 93ea6fb4-9f72-406f-87e1-13b3ef045fed
  Args:
    type: :Woman
    source: Marie_Therese_of_Wurttemberg
  AssignClass (78bb5eb7-a314-4a69-a098-723f85a39014)
 Call ID: 78bb5eb7-a314-4a69-a098-723f85a39014
  Args:
    source: Marie_Therese_of_Wurttemberg
    type: :Person
  AddLiteral (90c38eff-b3b3-436b-90f6-70b449ca1401)
 Call ID: 90c38eff-b3b3-436b-90f6-70b449ca1401
  Args:
    literal_value: 1934
    source: Marie_Therese_of_Wurttemberg
    relation: :hasBirthYear
    literal_type: xsd:integer
  AssignClass (7594c9fd-6432-4b61-9e01-c385ee0b3b31)
 Call ID: 7594c9fd-6432-4b61-9e01-c385ee0b3b31
  Args:
    type: :Man
    source: Philipp_Albrecht_Duke_of_Wurttemberg
  AssignClass (152c5e4b-e588-4b9d-94a4-79b8c7a44e82)
 Call ID: 152c5e4b-e588-4b9d-94a4-79b8c7a44e82
  Args:
    type: :Person
    source: Philipp_Albrecht_Duke_of_Wurttemberg
  AssignClass (5d32ad45-2114-450e-900d-7b88d5a47278)
 Call ID: 5d32ad45-2114-450e-900d-7b88d5a47278
  Args:
    source: Rosa_of_Austria
    type: :Woman
  AssignClass (2908be62-f75c-4da6-bd6a-21204c816422)
 Call ID: 2908be62-f75c-4da6-bd6a-21204c816422
  Args:
    source: Rosa_of_Austria
    type: :Person
  AddTriple (799b5ac0-a459-40a5-927d-8df0e3b107da)
 Call ID: 799b5ac0-a459-40a5-927d-8df0e3b107da
  Args:
    target: Philipp_Albrecht_Duke_of_Wurttemberg
    source: Marie_Therese_of_Wurttemberg
    relation: :hasFather
  AddTriple (0618095f-cbd3-46e7-8ae9-7f4dd7ddfd32)
 Call ID: 0618095f-cbd3-46e7-8ae9-7f4dd7ddfd32
  Args:
    relation: :hasMother
    target: Rosa_of_Austria
    source: Marie_Therese_of_Wurttemberg
  AssignClass (236284da-a617-48f4-84cb-8d0e8c28d497)
 Call ID: 236284da-a617-48f4-84cb-8d0e8c28d497
  Args:
    type: :Man
    source: Carl_Duke_of_Wurttemberg
  AssignClass (0636ca9a-43d0-4b70-89fc-b3bca17cc0ec)
 Call ID: 0636ca9a-43d0-4b70-89fc-b3bca17cc0ec
  Args:
    source: Carl_Duke_of_Wurttemberg
    type: :Person
  AddTriple (8300b4d3-0392-4da0-8eda-adfd0f5d2340)
 Call ID: 8300b4d3-0392-4da0-8eda-adfd0f5d2340
  Args:
    source: Carl_Duke_of_Wurttemberg
    target: Marie_Therese_of_Wurttemberg
    relation: :isBrotherOf
  AssignClass (40db4e3a-ab31-4a85-ad86-60cc38b85292)
 Call ID: 40db4e3a-ab31-4a85-ad86-60cc38b85292
  Args:
    type: :Man
    source: Prince_Henri_Count_of_Clermont
  AssignClass (94fba3f0-b916-47c4-94c2-0842fd15c367)
 Call ID: 94fba3f0-b916-47c4-94c2-0842fd15c367
  Args:
    type: :Person
    source: Prince_Henri_Count_of_Clermont
  AddLiteral (62eacb73-ed06-4a64-ac49-bf57994a2af1)
 Call ID: 62eacb73-ed06-4a64-ac49-bf57994a2af1
  Args:
    source: Marie_Therese_of_Wurttemberg
    relation: :hasMarriageYear
    literal_value: 1957
    literal_type: xsd:integer
  AddTriple (8bde7c04-5858-44ff-8425-cff2b891e216)
 Call ID: 8bde7c04-5858-44ff-8425-cff2b891e216
  Args:
    target: Prince_Henri_Count_of_Clermont
    source: Marie_Therese_of_Wurttemberg
    relation: :hasRelation
  AssignClass (91f37387-be51-4b0c-a897-688ff7bcb2e6)
 Call ID: 91f37387-be51-4b0c-a897-688ff7bcb2e6
  Args:
    type: :Man
    source: Henri_Count_of_Paris
  AssignClass (1820b75d-fd7c-4f3b-8bc2-92401637e0f2)
 Call ID: 1820b75d-fd7c-4f3b-8bc2-92401637e0f2
  Args:
    source: Henri_Count_of_Paris
    type: :Person
  AssignClass (34f5b7f6-a154-45cb-9f67-0a50d3e26ec7)
 Call ID: 34f5b7f6-a154-45cb-9f67-0a50d3e26ec7
  Args:
    source: Isabelle_of_Orleans_Braganza
    type: :Woman
  AssignClass (3fdf6d55-586c-41d6-8c15-b1fa7e9bdd80)
 Call ID: 3fdf6d55-586c-41d6-8c15-b1fa7e9bdd80
  Args:
    type: :Person
    source: Isabelle_of_Orleans_Braganza
  AddTriple (a64ef1bb-485a-4465-9798-9c4ce64ec19a)
 Call ID: a64ef1bb-485a-4465-9798-9c4ce64ec19a
  Args:
    relation: :hasFather
    source: Prince_Henri_Count_of_Clermont
    target: Henri_Count_of_Paris
  AddTriple (632dc544-796c-4e88-a6af-c10a32335d16)
 Call ID: 632dc544-796c-4e88-a6af-c10a32335d16
  Args:
    source: Prince_Henri_Count_of_Clermont
    target: Isabelle_of_Orleans_Braganza
    relation: :hasMother
  AssignClass (09c633c0-2639-49be-b823-8a1d08e501ec)
 Call ID: 09c633c0-2639-49be-b823-8a1d08e501ec
  Args:
    type: :Woman
    source: Diane_dOrleans
  AssignClass (783beeec-8dda-48cf-9a1a-2fa87378ea6e)
 Call ID: 783beeec-8dda-48cf-9a1a-2fa87378ea6e
  Args:
    source: Diane_dOrleans
    type: :Person
  AddTriple (b34bf54f-e911-47bb-b828-85f65216f846)
 Call ID: b34bf54f-e911-47bb-b828-85f65216f846
  Args:
    source: Diane_dOrleans
    target: Prince_Henri_Count_of_Clermont
    relation: :isSisterOf
  AddTriple (f99108db-5663-4cc1-9529-cc0cf7c83569)
 Call ID: f99108db-5663-4cc1-9529-cc0cf7c83569
  Args:
    relation: :hasRelation
    target: Diane_dOrleans
    source: Carl_Duke_of_Wurttemberg
  Finish (d26b412e-cde6-4dd0-ba85-173a02499aa0)
 Call ID: d26b412e-cde6-4dd0-ba85-173a02499aa0
  Args: