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
Lady Charlotte Anne Santo Domingo (née Wellesley; 8 October 1990) is an English aristocrat and socialite and photography producer.
Early life and family

Lady Charlotte Wellesley was born at St Mary's Hospital, London on 8 October 1990 to Princess Antonia of Prussia and Charles Wellesley, Marquess of Douro.
After the death of her paternal grandfather, Valerian Wellesley, 8th Duke of Wellington, in 2014, her father succeeded him as the 9th Duke of Wellington, the 9th Prince of Waterloo, the 9th Duke of Victoria, and the 10th Duke of Ciudad Rodrigo.
Her mother, Princess Antonia, is the youngest child of Prince Frederick of Prussia and Lady Brigid Guinness.
Through her mother, Lady Charlotte is a great-great-granddaughter of Wilhelm II, German Emperor and a great-great-great-great-granddaughter of Queen Victoria.
Lady Charlotte grew up at Stratfield Saye House, her family's estate in Hampshire.
She is the younger sister of Arthur Wellesley, Earl of Mornington and Lady Mary Wellesley.
Education and career

Lady Charlotte attended Wycombe Abbey, an all-girls boarding school in Buckinghamshire.
Personal life

Lady Charlotte married Colombian-American financier Alejandro Santo Domingo in Íllora, Spain, on 28 May 2016.



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
  AssignClass (b2eda352-861c-4c58-ad8d-22d3e8b99c3d)
 Call ID: b2eda352-861c-4c58-ad8d-22d3e8b99c3d
  Args:
    type: :Woman
    source: Charlotte_Wellesley
  AssignClass (50a30dbd-4572-43e7-9402-e485a43103b3)
 Call ID: 50a30dbd-4572-43e7-9402-e485a43103b3
  Args:
    source: Charlotte_Wellesley
    type: :Person
  AddLiteral (ea10730a-9c8c-444b-be74-5604aa67e8de)
 Call ID: ea10730a-9c8c-444b-be74-5604aa67e8de
  Args:
    literal_value: 1990-10-08
    relation: :hasBirthYear
    literal_type: xsd:string
    source: Charlotte_Wellesley
  AssignClass (791e1eb2-427f-4265-9766-94075f11fdfb)
 Call ID: 791e1eb2-427f-4265-9766-94075f11fdfb
  Args:
    source: Antonia_of_Prussia
    type: :Woman
  AssignClass (63df1825-f7d4-45d9-a608-b4c460b407bd)
 Call ID: 63df1825-f7d4-45d9-a608-b4c460b407bd
  Args:
    type: :Person
    source: Antonia_of_Prussia
  AssignClass (9d983a9f-5d1e-4f4c-b2e4-c3d9f12d31d9)
 Call ID: 9d983a9f-5d1e-4f4c-b2e4-c3d9f12d31d9
  Args:
    type: :Man
    source: Charles_Wellesley
  AssignClass (5997af83-ce05-4c58-9c30-ea16f69ae744)
 Call ID: 5997af83-ce05-4c58-9c30-ea16f69ae744
  Args:
    source: Charles_Wellesley
    type: :Person
  AddTriple (aa4656ed-bd42-41c0-b79a-2e34178b5157)
 Call ID: aa4656ed-bd42-41c0-b79a-2e34178b5157
  Args:
    source: Charlotte_Wellesley
    target: Antonia_of_Prussia
    relation: :hasMother
  AddTriple (b51f3049-33ed-4427-a0a1-81b759b1c20b)
 Call ID: b51f3049-33ed-4427-a0a1-81b759b1c20b
  Args:
    relation: :hasFather
    source: Charlotte_Wellesley
    target: Charles_Wellesley
  AssignClass (94620c6d-170c-4109-8298-0926cea42def)
 Call ID: 94620c6d-170c-4109-8298-0926cea42def
  Args:
    type: :Man
    source: Valerian_Wellesley
  AssignClass (859d3b15-a187-42f7-929d-388e3fbcb22c)
 Call ID: 859d3b15-a187-42f7-929d-388e3fbcb22c
  Args:
    type: :Person
    source: Valerian_Wellesley
  AddTriple (e98deb9f-48b7-4b4d-88fc-f8af02b36218)
 Call ID: e98deb9f-48b7-4b4d-88fc-f8af02b36218
  Args:
    source: Charles_Wellesley
    target: Valerian_Wellesley
    relation: :hasFather
  AddLiteral (c2245d91-f2fd-4037-8548-96c7aeaf2537)
 Call ID: c2245d91-f2fd-4037-8548-96c7aeaf2537
  Args:
    source: Valerian_Wellesley
    literal_type: xsd:integer
    literal_value: 2014
    relation: :hasDeathYear
  AssignClass (422f7c90-fb51-436d-8e76-4e2b03833c50)
 Call ID: 422f7c90-fb51-436d-8e76-4e2b03833c50
  Args:
    type: :Man
    source: Frederick_of_Prussia
  AssignClass (883f8003-f760-4143-8db4-984bd91135bb)
 Call ID: 883f8003-f760-4143-8db4-984bd91135bb
  Args:
    source: Frederick_of_Prussia
    type: :Person
  AssignClass (d1ba4fd2-c607-4e81-991c-9183a09f71b5)
 Call ID: d1ba4fd2-c607-4e81-991c-9183a09f71b5
  Args:
    source: Brigid_Guinness
    type: :Woman
  AssignClass (a26b9b14-32c7-4ef1-afc8-88068f02026f)
 Call ID: a26b9b14-32c7-4ef1-afc8-88068f02026f
  Args:
    type: :Person
    source: Brigid_Guinness
  AddTriple (b616f71d-3ff2-4d3b-8848-4125402b992f)
 Call ID: b616f71d-3ff2-4d3b-8848-4125402b992f
  Args:
    target: Frederick_of_Prussia
    source: Antonia_of_Prussia
    relation: :hasFather
  AddTriple (94df20ce-ce6f-47a3-9449-7a688b7063f8)
 Call ID: 94df20ce-ce6f-47a3-9449-7a688b7063f8
  Args:
    target: Brigid_Guinness
    source: Antonia_of_Prussia
    relation: :hasMother
  AssignClass (671c7e12-3004-4cb2-b862-81ac1bebf6b1)
 Call ID: 671c7e12-3004-4cb2-b862-81ac1bebf6b1
  Args:
    type: :Man
    source: Arthur_Wellesley
  AssignClass (9a4c3e2d-900a-4682-bbfc-efdd8de292bc)
 Call ID: 9a4c3e2d-900a-4682-bbfc-efdd8de292bc
  Args:
    source: Arthur_Wellesley
    type: :Person
  AssignClass (e4929e6a-dafe-4391-a1d0-489aa86034b8)
 Call ID: e4929e6a-dafe-4391-a1d0-489aa86034b8
  Args:
    type: :Woman
    source: Mary_Wellesley
  AssignClass (b6f858ca-6938-4fca-bbfd-dc14b6b72e8d)
 Call ID: b6f858ca-6938-4fca-bbfd-dc14b6b72e8d
  Args:
    type: :Person
    source: Mary_Wellesley
  AddTriple (115697c4-ab64-4a81-bb7a-42634832035b)
 Call ID: 115697c4-ab64-4a81-bb7a-42634832035b
  Args:
    source: Charlotte_Wellesley
    target: Arthur_Wellesley
    relation: :hasBrother
  AddTriple (b7fe8086-3c0c-47df-aa83-00f1c3b5b603)
 Call ID: b7fe8086-3c0c-47df-aa83-00f1c3b5b603
  Args:
    relation: :hasSister
    source: Charlotte_Wellesley
    target: Mary_Wellesley
  AssignClass (7649aaf0-a3cd-4e29-9bd5-8dd70263755b)
 Call ID: 7649aaf0-a3cd-4e29-9bd5-8dd70263755b
  Args:
    source: Alejandro_Santo_Domingo
    type: :Man
  AssignClass (7da36523-14fd-4045-80fa-ef1cd7db7e90)
 Call ID: 7da36523-14fd-4045-80fa-ef1cd7db7e90
  Args:
    source: Alejandro_Santo_Domingo
    type: :Person
  AddTriple (d09b2f06-0a23-453a-aae3-23fa3a55118b)
 Call ID: d09b2f06-0a23-453a-aae3-23fa3a55118b
  Args:
    relation: :hasRelation
    source: Charlotte_Wellesley
    target: Alejandro_Santo_Domingo
  AddLiteral (e41f014c-e87c-4206-800c-58d0c7278b54)
 Call ID: e41f014c-e87c-4206-800c-58d0c7278b54
  Args:
    source: Charlotte_Wellesley
    literal_type: xsd:integer
    literal_value: 2016
    relation: :hasMarriageYear
  Finish (93c4c342-761f-4710-8e59-93b43d4a9fe9)
 Call ID: 93c4c342-761f-4710-8e59-93b43d4a9fe9
  Args: