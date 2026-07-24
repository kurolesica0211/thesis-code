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
Beatrix Amelie Ehrengard Eilika von Storch (née Herzogin von Oldenburg; 27 May 1971) is a German politician and lawyer, who has been the Deputy Parliamentary Leader of the Alternative for Germany since July 2015 and a Member of the Bundestag since September 2017.
Family background

In accordance with the traditions of the House of Oldenburg, her dynastic style from birth was Her Highness Duchess Beatrix Amelie Ehrengard Eilika of Oldenburg.
Personal life

On 22 October 2010 she married German-Chilean businessman Sven von Storch (born 1970), member of a German noble family from Mecklenburg.
He is the son of businessman Berndt Detlev von Storch (1930–2004) and Antje Liete Krüger-Franke (b. 1938).
Education and early career

Von Storch was a banker before she studied law in Heidelberg and Lausanne.
Von Storch was a co-founder of the Göttinger Kreis – Students for the Rule of Law Association – an organization which sought to campaign for reparation for the expulsions and nationalization of land in the Soviet occupied zones of Germany and the former East Germany.
Von Storch was a member of the Free Democratic Party and in 2013, became a founding member of Election Alternative 13 set up by Bernd Lucke as the precursor to Alternative for Germany.
In 2014, Beatrix von Storch was elected a Member of European Parliament representing Alternative for Germany.
Von Storch has been described as a social conservative.
Von Storch also supported the United Kingdom's vote for Brexit and is a friend of British eurosceptic politician Nigel Farage.
She has been characterized as a member and supporter of the more moderate Alternative Mitte faction of the AfD.


Controversies

Legal battle with the Berliner Schaubühne

In November 2015, a leading Berlin theatre, the Schaubühne, was brought into legal conflict with Beatrix von Storch over a play, Falk Richter's FEAR, that parodied AfD leaders as zombies and mass murderers.
Beatrix von Storch is depicted facing retribution for her grandfather's role as a minister in Hitler's government.
Beatrix von Storch and the conservative activist Hedwig von Beverfoerde then requested and obtained a preliminary injunction against the theatre, prohibiting it from using images of them in the production.
Remarks about use of deadly force against refugees

In late February 2016, von Storch was "pied" by members of the German left-wing group Peng Collective at a party meeting in Kassel.
"Rapist hordes" tweet

Von Storch's Twitter account was blocked for twelve hours after she posted a criticism of the Cologne Police Department for publishing a New Years greeting in Arabic as well as in German, French and English.
Other prominent members of the AfD quickly sprang to von Storch's defense, including Alice Weidel.



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
  AssignClass (57f97524-4e9c-4093-bf9b-93bb3160fa62)
 Call ID: 57f97524-4e9c-4093-bf9b-93bb3160fa62
  Args:
    source: Beatrix_von_Storch
    type: :Woman
  AssignClass (5de93f09-9773-437d-8bdc-73c784932a4c)
 Call ID: 5de93f09-9773-437d-8bdc-73c784932a4c
  Args:
    type: :Person
    source: Beatrix_von_Storch
  AddLiteral (c48e94e1-9897-400b-875d-ab8d6ce89a3f)
 Call ID: c48e94e1-9897-400b-875d-ab8d6ce89a3f
  Args:
    relation: :knownAs
    source: Beatrix_von_Storch
    literal_type: xsd:string
    literal_value: Beatrix Amelie Ehrengard Eilika von Storch
  AddLiteral (42b6d8cd-3693-420a-a8bf-2858b77c6153)
 Call ID: 42b6d8cd-3693-420a-a8bf-2858b77c6153
  Args:
    source: Beatrix_von_Storch
    relation: :hasBirthYear
    literal_type: xsd:positiveInteger
    literal_value: 1971
  AssignClass (488b3fa0-4e3f-43f2-b0b1-08507f5cb339)
 Call ID: 488b3fa0-4e3f-43f2-b0b1-08507f5cb339
  Args:
    type: :Man
    source: Sven_von_Storch
  AssignClass (efe41643-b0ff-400d-8396-ed4b2fa13013)
 Call ID: efe41643-b0ff-400d-8396-ed4b2fa13013
  Args:
    source: Sven_von_Storch
    type: :Person
  AddLiteral (45095637-c4f9-4b5e-9190-a9598af50bb5)
 Call ID: 45095637-c4f9-4b5e-9190-a9598af50bb5
  Args:
    relation: :hasBirthYear
    source: Sven_von_Storch
    literal_type: xsd:positiveInteger
    literal_value: 1970
  AddLiteral (417432d1-a8d4-4c7c-b933-ab2c48a01edc)
 Call ID: 417432d1-a8d4-4c7c-b933-ab2c48a01edc
  Args:
    relation: :hasMarriageYear
    source: Beatrix_von_Storch
    literal_type: xsd:positiveInteger
    literal_value: 2010
  AddTriple (6d507892-b34b-4e1f-bf55-2aa2220069e3)
 Call ID: 6d507892-b34b-4e1f-bf55-2aa2220069e3
  Args:
    target: Sven_von_Storch
    source: Beatrix_von_Storch
    relation: :hasRelation
  AssignClass (33700c1b-1c27-4fd4-85c0-4d0969df3377)
 Call ID: 33700c1b-1c27-4fd4-85c0-4d0969df3377
  Args:
    source: Berndt_Detlev_von_Storch
    type: :Man
  AssignClass (09b96236-1bfa-4c74-9f08-09b99161b4bc)
 Call ID: 09b96236-1bfa-4c74-9f08-09b99161b4bc
  Args:
    source: Berndt_Detlev_von_Storch
    type: :Person
  AddLiteral (65957417-6b9b-480d-98f6-3367667d6b8b)
 Call ID: 65957417-6b9b-480d-98f6-3367667d6b8b
  Args:
    literal_type: xsd:positiveInteger
    relation: :hasBirthYear
    source: Berndt_Detlev_von_Storch
    literal_value: 1930
  AddLiteral (7de65d4e-baf2-400a-9374-86b77a5c9c70)
 Call ID: 7de65d4e-baf2-400a-9374-86b77a5c9c70
  Args:
    literal_value: 2004
    literal_type: xsd:positiveInteger
    source: Berndt_Detlev_von_Storch
    relation: :hasDeathYear
  AssignClass (960e9c01-e4ac-4f87-9b31-f10a719ab6a1)
 Call ID: 960e9c01-e4ac-4f87-9b31-f10a719ab6a1
  Args:
    source: Antje_Liete_Kruger-Franke
    type: :Woman
  AssignClass (0a02a812-82f8-41e5-aa42-8f002370d885)
 Call ID: 0a02a812-82f8-41e5-aa42-8f002370d885
  Args:
    source: Antje_Liete_Kruger-Franke
    type: :Person
  AddLiteral (4ae0cc89-9fc6-4e7d-8422-de2b53073338)
 Call ID: 4ae0cc89-9fc6-4e7d-8422-de2b53073338
  Args:
    source: Antje_Liete_Kruger-Franke
    literal_type: xsd:positiveInteger
    relation: :hasBirthYear
    literal_value: 1938
  AddTriple (a3d56e1b-1f15-4bcb-a100-ae68a528d698)
 Call ID: a3d56e1b-1f15-4bcb-a100-ae68a528d698
  Args:
    source: Sven_von_Storch
    relation: :hasFather
    target: Berndt_Detlev_von_Storch
  AddTriple (353630d1-893c-4632-a3c9-1991dfd1fe8a)
 Call ID: 353630d1-893c-4632-a3c9-1991dfd1fe8a
  Args:
    target: Antje_Liete_Kruger-Franke
    relation: :hasMother
    source: Sven_von_Storch
  Finish (a152796a-69ce-4943-9f42-8aca723ccb73)
 Call ID: a152796a-69ce-4943-9f42-8aca723ccb73
  Args: