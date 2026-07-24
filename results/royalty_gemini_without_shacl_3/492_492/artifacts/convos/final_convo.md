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
Philipp, Prince of Hohenlohe-Langenburg (Philipp Gottfried Alexander; born 20 January 1970), is the head of the House of Hohenlohe-Langenburg, since the death of his father in 2004.
Early life and ancestry

He was born in Crailsheim, West Germany, the middle child and only son of Kraft, Prince of Hohenlohe-Langenburg (1935–2004) and his first wife, Princess Charlotte of Croÿ (b. 1938).
Paternally, he is a grandson of Princess Margarita of Greece and Denmark, and a grandnephew of Prince Philip, Duke of Edinburgh, whose funeral he attended.
Anne, Princess Royal is one of his godmothers.
Maternally, he is the grandson of Prince Alexander of Croy (1912–2002) and his Scottish wife, Anna Elspeth Campbell (1917–1986), granddaughter of Archibald Campbell, 6th of Glendaruel.
He sought public support from (then) Charles, Prince of Wales, the current King Charles III, and from former vice chancellor and foreign minister Joschka Fischer of the Green Party, who both attended a conference at Langenburg Castle in 2013.
Together with Fischer he founded the Langenburg Forum for Sustainability which cooperates with Charles' International Sustainability Unit


Langenburg castle is partially open to the public, including the state rooms and a museum of classic cars.
Marriage and issue

He married Saskia Binder (b. 15 January 1973 in Munich), daughter of former Deutsche Bank Munich director Hans Peter Binder, on 6 September 2003 in a civil ceremony at Langenburg.



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
  AssignClass (b1e1962b-7721-4906-a402-583247edbfa3)
 Call ID: b1e1962b-7721-4906-a402-583247edbfa3
  Args:
    source: Philipp_Prince_of_Hohenlohe-Langenburg
    type: :Man
  AddLiteral (8c29c421-f229-474a-a517-743f5d02a985)
 Call ID: 8c29c421-f229-474a-a517-743f5d02a985
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Philipp_Prince_of_Hohenlohe-Langenburg
    literal_value: 1970
  AssignClass (2ccb90ac-8a8c-45e1-ab88-95b8b359c82b)
 Call ID: 2ccb90ac-8a8c-45e1-ab88-95b8b359c82b
  Args:
    type: :Man
    source: Kraft_Prince_of_Hohenlohe-Langenburg
  AddLiteral (cc7d1f23-30e8-4452-8e4d-442af8bfa867)
 Call ID: cc7d1f23-30e8-4452-8e4d-442af8bfa867
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1935
    source: Kraft_Prince_of_Hohenlohe-Langenburg
  AddLiteral (66ded01b-185d-4ba8-9265-cd23023831e8)
 Call ID: 66ded01b-185d-4ba8-9265-cd23023831e8
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 2004
    source: Kraft_Prince_of_Hohenlohe-Langenburg
  AssignClass (36522bbe-a5f4-4819-a639-bdafda2b593b)
 Call ID: 36522bbe-a5f4-4819-a639-bdafda2b593b
  Args:
    type: :Woman
    source: Princess_Charlotte_of_Croy
  AddLiteral (77c2b4de-f7b9-48fa-9f08-b5d5932d5eb3)
 Call ID: 77c2b4de-f7b9-48fa-9f08-b5d5932d5eb3
  Args:
    source: Princess_Charlotte_of_Croy
    literal_value: 1938
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddTriple (37bed36b-77f5-48ae-b5c6-c9dd62a2a7cd)
 Call ID: 37bed36b-77f5-48ae-b5c6-c9dd62a2a7cd
  Args:
    source: Philipp_Prince_of_Hohenlohe-Langenburg
    target: Kraft_Prince_of_Hohenlohe-Langenburg
    relation: :hasFather
  AddTriple (50ca5822-04a6-4806-8b4b-6620314cc7d6)
 Call ID: 50ca5822-04a6-4806-8b4b-6620314cc7d6
  Args:
    source: Philipp_Prince_of_Hohenlohe-Langenburg
    target: Princess_Charlotte_of_Croy
    relation: :hasMother
  AssignClass (c914b52b-241e-4748-a024-a77a3fdb663e)
 Call ID: c914b52b-241e-4748-a024-a77a3fdb663e
  Args:
    type: :Woman
    source: Princess_Margarita_of_Greece_and_Denmark
  AddTriple (2e03f57e-d981-45cb-9c3a-85337043ee63)
 Call ID: 2e03f57e-d981-45cb-9c3a-85337043ee63
  Args:
    relation: :hasAncestor
    target: Princess_Margarita_of_Greece_and_Denmark
    source: Philipp_Prince_of_Hohenlohe-Langenburg
  AssignClass (16c49ca3-8b32-467f-913d-3d70e90092aa)
 Call ID: 16c49ca3-8b32-467f-913d-3d70e90092aa
  Args:
    source: Prince_Alexander_of_Croy
    type: :Man
  AddLiteral (325a293f-0369-4810-94f1-bb50f89823e6)
 Call ID: 325a293f-0369-4810-94f1-bb50f89823e6
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1912
    source: Prince_Alexander_of_Croy
  AddLiteral (bcc8dd2b-6faf-4a35-bb13-b2f0e04e8691)
 Call ID: bcc8dd2b-6faf-4a35-bb13-b2f0e04e8691
  Args:
    source: Prince_Alexander_of_Croy
    literal_value: 2002
    relation: :hasDeathYear
    literal_type: xsd:integer
  AssignClass (10ece3d6-cfa7-418a-ac89-12d77e2b1b61)
 Call ID: 10ece3d6-cfa7-418a-ac89-12d77e2b1b61
  Args:
    source: Anna_Elspeth_Campbell
    type: :Woman
  AddLiteral (34341d43-955d-420c-8ac3-17c91d593d9e)
 Call ID: 34341d43-955d-420c-8ac3-17c91d593d9e
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1917
    source: Anna_Elspeth_Campbell
  AddLiteral (42d7610f-1b85-4ca1-a38e-50c1c80d8785)
 Call ID: 42d7610f-1b85-4ca1-a38e-50c1c80d8785
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1986
    source: Anna_Elspeth_Campbell
  AddTriple (2ee85d94-8f36-4968-91a3-dbf05542cc99)
 Call ID: 2ee85d94-8f36-4968-91a3-dbf05542cc99
  Args:
    relation: :hasAncestor
    source: Philipp_Prince_of_Hohenlohe-Langenburg
    target: Prince_Alexander_of_Croy
  AddTriple (f7e7f8d4-2aa5-48b0-98a1-e6816511108b)
 Call ID: f7e7f8d4-2aa5-48b0-98a1-e6816511108b
  Args:
    source: Philipp_Prince_of_Hohenlohe-Langenburg
    target: Anna_Elspeth_Campbell
    relation: :hasAncestor
  AssignClass (f3766937-557c-4c90-8051-5fcdb070efc6)
 Call ID: f3766937-557c-4c90-8051-5fcdb070efc6
  Args:
    type: :Man
    source: Archibald_Campbell_6th_of_Glendaruel
  AddTriple (04d76712-9801-4734-b6ca-cd7215341828)
 Call ID: 04d76712-9801-4734-b6ca-cd7215341828
  Args:
    relation: :hasAncestor
    target: Archibald_Campbell_6th_of_Glendaruel
    source: Anna_Elspeth_Campbell
  AssignClass (9a4c5b03-2474-40da-b214-dde3e3395a04)
 Call ID: 9a4c5b03-2474-40da-b214-dde3e3395a04
  Args:
    type: :Woman
    source: Saskia_Binder
  AddLiteral (6572c4e8-6148-4d06-854e-af5a3c5a3d94)
 Call ID: 6572c4e8-6148-4d06-854e-af5a3c5a3d94
  Args:
    source: Saskia_Binder
    literal_value: 1973
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (5719532e-8bc9-432f-ae24-3bafed33a269)
 Call ID: 5719532e-8bc9-432f-ae24-3bafed33a269
  Args:
    literal_value: 2003
    source: Philipp_Prince_of_Hohenlohe-Langenburg
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AddTriple (5f45a320-9432-4874-b4d2-733ca616e722)
 Call ID: 5f45a320-9432-4874-b4d2-733ca616e722
  Args:
    relation: :hasRelation
    source: Philipp_Prince_of_Hohenlohe-Langenburg
    target: Saskia_Binder
  AssignClass (02b548e6-ab25-4a48-ae70-00821c76ef2a)
 Call ID: 02b548e6-ab25-4a48-ae70-00821c76ef2a
  Args:
    type: :Man
    source: Hans_Peter_Binder
  AddTriple (381a1987-1313-4d67-9c04-5169a3e82b28)
 Call ID: 381a1987-1313-4d67-9c04-5169a3e82b28
  Args:
    source: Saskia_Binder
    target: Hans_Peter_Binder
    relation: :hasFather
  Finish (c420e86a-00cd-4928-a857-866dc05af78b)
 Call ID: c420e86a-00cd-4928-a857-866dc05af78b
  Args: