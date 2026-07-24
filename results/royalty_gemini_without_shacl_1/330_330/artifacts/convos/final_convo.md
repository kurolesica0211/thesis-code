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
Fergus Bowes-Lyon (18 April 1889 – 27 September 1915) was a British officer and older brother of Elizabeth Bowes-Lyon, who later became the queen consort of King George VI.
He was a maternal uncle of Queen Elizabeth II.
Early life and marriage

Fergus Bowes-Lyon was born at Forbes House in Ham, Surrey, the son of Claude Bowes-Lyon, 14th
Bowes-Lyon had his early education at Ludgrove School.
On 17 September 1914, Bowes-Lyon married Lady Christian Norah Dawson-Damer (7 August 1890 – 29 March 1959), daughter of the 5th Earl of Portarlington.
Rosemary was only two months old when Fergus died in the line of duty on 27 September 1915, only 10 days after the first anniversary of his wedding.
His issue:


World War I

In the First World War, Bowes-Lyon served with the 8th Battalion, Black Watch: as a lieutenant since 19 August 1914, and as temporary captain since 17 November.
Bowes-Lyon was killed in action on 27 September 1915, during the Battle of the Hohenzollern Redoubt in the Battle of Loos.
At the time of Bowes-Lyon's death, his brother John was also serving with the Black Watch.
His mother, Cecilia Bowes-Lyon, Countess of Strathmore and Kinghorne, was severely affected by the loss of her son, and after his death became an invalid, withdrawn from public life until the marriage of her daughter Elizabeth to the future king George VI in 1923.
Fergus's widow later married Captain William Frederick Martin (d. 6 October 1947).
In November 2011, Bowes-Lyon's grandson supplied family records to the Commonwealth War Graves Commission detailing his original burial place, and showing that it had remained marked until the end of the war.



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
  AssignClass (42fc5d9d-5fad-499a-97ff-756a3b174e0d)
 Call ID: 42fc5d9d-5fad-499a-97ff-756a3b174e0d
  Args:
    source: :Fergus_Bowes-Lyon
    type: :Man
  AssignClass (a96ba2af-7a3e-47e2-af32-8d8435776470)
 Call ID: a96ba2af-7a3e-47e2-af32-8d8435776470
  Args:
    type: :Person
    source: :Fergus_Bowes-Lyon
  AddLiteral (b0ce2cac-5d0f-4a22-b647-ffad0082ff33)
 Call ID: b0ce2cac-5d0f-4a22-b647-ffad0082ff33
  Args:
    literal_type: xsd:integer
    source: :Fergus_Bowes-Lyon
    relation: :hasBirthYear
    literal_value: 1889
  AddLiteral (fa90fac4-04c8-40f5-9609-32c17cc56ead)
 Call ID: fa90fac4-04c8-40f5-9609-32c17cc56ead
  Args:
    literal_type: xsd:integer
    source: :Fergus_Bowes-Lyon
    relation: :hasDeathYear
    literal_value: 1915
  AssignClass (9f080f1b-4f0c-45ca-95f0-9d130a04836d)
 Call ID: 9f080f1b-4f0c-45ca-95f0-9d130a04836d
  Args:
    type: :Woman
    source: :Elizabeth_Bowes-Lyon
  AssignClass (9ae51811-1295-4305-aed6-ce9f13597378)
 Call ID: 9ae51811-1295-4305-aed6-ce9f13597378
  Args:
    type: :Person
    source: :Elizabeth_Bowes-Lyon
  AddTriple (e3e9f881-607d-4e95-8707-8bab02bd3865)
 Call ID: e3e9f881-607d-4e95-8707-8bab02bd3865
  Args:
    source: :Elizabeth_Bowes-Lyon
    target: :Fergus_Bowes-Lyon
    relation: :isSisterOf
  AssignClass (9147193d-907f-474f-8586-cbb33f1143eb)
 Call ID: 9147193d-907f-474f-8586-cbb33f1143eb
  Args:
    source: :Claude_Bowes-Lyon
    type: :Man
  AssignClass (60f914d4-7e64-42df-900a-d3be24712cff)
 Call ID: 60f914d4-7e64-42df-900a-d3be24712cff
  Args:
    source: :Claude_Bowes-Lyon
    type: :Person
  AddTriple (7e7aaa7d-6b4a-499c-b658-4c7efe622429)
 Call ID: 7e7aaa7d-6b4a-499c-b658-4c7efe622429
  Args:
    relation: :hasFather
    target: :Claude_Bowes-Lyon
    source: :Fergus_Bowes-Lyon
  AssignClass (72f91f98-c0c3-4d90-948a-a100115fa2b5)
 Call ID: 72f91f98-c0c3-4d90-948a-a100115fa2b5
  Args:
    type: :Woman
    source: :Christian_Norah_Dawson-Damer
  AssignClass (dfe7cebe-a31b-4901-90a6-1b0af5048724)
 Call ID: dfe7cebe-a31b-4901-90a6-1b0af5048724
  Args:
    type: :Person
    source: :Christian_Norah_Dawson-Damer
  AddLiteral (71e152d6-d418-4c5f-9e9d-20d1ec700d9c)
 Call ID: 71e152d6-d418-4c5f-9e9d-20d1ec700d9c
  Args:
    source: :Fergus_Bowes-Lyon
    literal_type: xsd:integer
    literal_value: 1914
    relation: :hasMarriageYear
  AddTriple (675356bb-eb03-4c78-8715-eda8ecf4ad6e)
 Call ID: 675356bb-eb03-4c78-8715-eda8ecf4ad6e
  Args:
    relation: :hasRelation
    target: :Christian_Norah_Dawson-Damer
    source: :Fergus_Bowes-Lyon
  AssignClass (e4e3e6b9-1a23-4bd9-93b1-fcfa8c9d6e01)
 Call ID: e4e3e6b9-1a23-4bd9-93b1-fcfa8c9d6e01
  Args:
    type: :Woman
    source: :Cecilia_Bowes-Lyon
  AssignClass (c170244e-d812-418f-9b03-4c4b7fc65349)
 Call ID: c170244e-d812-418f-9b03-4c4b7fc65349
  Args:
    source: :Cecilia_Bowes-Lyon
    type: :Person
  AddTriple (3f4237e5-5a59-40ba-9a17-a5055d1c744b)
 Call ID: 3f4237e5-5a59-40ba-9a17-a5055d1c744b
  Args:
    source: :Fergus_Bowes-Lyon
    target: :Cecilia_Bowes-Lyon
    relation: :hasMother
  AssignClass (dde200ad-2b37-4a71-bd9b-dd986cf43c6b)
 Call ID: dde200ad-2b37-4a71-bd9b-dd986cf43c6b
  Args:
    source: :John_Bowes-Lyon
    type: :Man
  AssignClass (7de5dda6-5d68-42b5-9569-5971df0b1fdc)
 Call ID: 7de5dda6-5d68-42b5-9569-5971df0b1fdc
  Args:
    type: :Person
    source: :John_Bowes-Lyon
  AddTriple (dbd349ab-02a6-4ca9-a6cf-036c49ab1f3b)
 Call ID: dbd349ab-02a6-4ca9-a6cf-036c49ab1f3b
  Args:
    source: :John_Bowes-Lyon
    target: :Fergus_Bowes-Lyon
    relation: :isBrotherOf
  AssignClass (20964f78-41ec-4df4-815e-54bb2de27265)
 Call ID: 20964f78-41ec-4df4-815e-54bb2de27265
  Args:
    source: :Rosemary_Bowes-Lyon
    type: :Woman
  AssignClass (fccdf20e-86c8-4db4-8623-f04835a07ac3)
 Call ID: fccdf20e-86c8-4db4-8623-f04835a07ac3
  Args:
    type: :Person
    source: :Rosemary_Bowes-Lyon
  AddTriple (d42c7fee-dfc2-4be4-9352-9f21d87f8e65)
 Call ID: d42c7fee-dfc2-4be4-9352-9f21d87f8e65
  Args:
    source: :Rosemary_Bowes-Lyon
    target: :Fergus_Bowes-Lyon
    relation: :isChildOf
  AddTriple (725d8aad-a7da-4f74-869a-5056a3e061f0)
 Call ID: 725d8aad-a7da-4f74-869a-5056a3e061f0
  Args:
    target: :Christian_Norah_Dawson-Damer
    source: :Rosemary_Bowes-Lyon
    relation: :isChildOf
  Finish (64ea6ca9-e40e-41f1-943b-6ab7f0d9fc4e)
 Call ID: 64ea6ca9-e40e-41f1-943b-6ab7f0d9fc4e
  Args: