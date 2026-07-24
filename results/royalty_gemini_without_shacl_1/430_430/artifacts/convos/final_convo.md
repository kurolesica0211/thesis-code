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
Rose Constance Leveson-Gower, Countess Granville (née Bowes-Lyon; 6 May 1890 – 17 November 1967) was the third daughter of the 14th Earl of Strathmore and Kinghorne by his wife, Cecilia Cavendish-Bentinck.
An elder sister of Queen Elizabeth the Queen Mother, she was therefore a maternal aunt of Queen Elizabeth II.


Life and family

On 24 May 1916, Lady Rose Bowes-Lyon married The Hon.
William Leveson-Gower, who succeeded to his childless brother's earldom on 21 July 1939.
As a result, she was styled as Countess Granville.
The couple had two children:


The Countess Granville stood godmother to her niece, Princess Margaret Rose of York, at the latter's christening on 3 October 1930.
She was also awarded the honorary degree of Doctor of Laws (LL.D.) by Queen's University Belfast.
Lord Granville died on 25 June 1953, aged 72.
Lady Granville outlived him by fourteen years when she died on 17 November 1967, aged 77.
She was the last surviving sibling of Queen Elizabeth The Queen Mother.



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
  AssignClass (5b997e23-23d8-41f5-be2e-2e1bf9a86d09)
 Call ID: 5b997e23-23d8-41f5-be2e-2e1bf9a86d09
  Args:
    type: :Woman
    source: :RoseConstanceLevesonGower
  AssignClass (c13f9621-ec35-4507-8410-68fdd7e56683)
 Call ID: c13f9621-ec35-4507-8410-68fdd7e56683
  Args:
    source: :RoseConstanceLevesonGower
    type: :Person
  AddLiteral (e0bfa5c2-503f-4520-9e84-f5bc10f7ef73)
 Call ID: e0bfa5c2-503f-4520-9e84-f5bc10f7ef73
  Args:
    source: :RoseConstanceLevesonGower
    literal_value: 1890
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (cb74de48-eb04-4e74-8851-fd9ace6c1418)
 Call ID: cb74de48-eb04-4e74-8851-fd9ace6c1418
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 1967
    source: :RoseConstanceLevesonGower
  AssignClass (1161f59b-276e-4a58-8839-9c2c8a5968b8)
 Call ID: 1161f59b-276e-4a58-8839-9c2c8a5968b8
  Args:
    type: :Man
    source: :14thEarlOfStrathmoreAndKinghorne
  AssignClass (24570f41-f1a7-436a-8848-c7e6604d8296)
 Call ID: 24570f41-f1a7-436a-8848-c7e6604d8296
  Args:
    source: :14thEarlOfStrathmoreAndKinghorne
    type: :Person
  AssignClass (5ea0346a-df31-4e49-8308-c164ef810ebf)
 Call ID: 5ea0346a-df31-4e49-8308-c164ef810ebf
  Args:
    source: :14thEarlOfStrathmoreAndKinghorne
    type: :Ancestor
  AssignClass (b54e8dea-eccd-4458-83fb-a82b6118f812)
 Call ID: b54e8dea-eccd-4458-83fb-a82b6118f812
  Args:
    type: :Woman
    source: :CeciliaCavendishBentinck
  AssignClass (f9ba252f-eb9f-4e22-a7d4-72c04a8ad1a7)
 Call ID: f9ba252f-eb9f-4e22-a7d4-72c04a8ad1a7
  Args:
    source: :CeciliaCavendishBentinck
    type: :Person
  AssignClass (e175f0d8-5153-43d1-87ed-cac353142c69)
 Call ID: e175f0d8-5153-43d1-87ed-cac353142c69
  Args:
    type: :Ancestor
    source: :CeciliaCavendishBentinck
  AddTriple (75e75b7e-2514-423d-afaa-79e52bd3d24a)
 Call ID: 75e75b7e-2514-423d-afaa-79e52bd3d24a
  Args:
    relation: :hasFather
    target: :14thEarlOfStrathmoreAndKinghorne
    source: :RoseConstanceLevesonGower
  AddTriple (c986b89c-5f12-4499-a6cc-408be049e360)
 Call ID: c986b89c-5f12-4499-a6cc-408be049e360
  Args:
    target: :CeciliaCavendishBentinck
    source: :RoseConstanceLevesonGower
    relation: :hasMother
  AssignClass (68041fb7-37da-4c67-abae-186828f3306c)
 Call ID: 68041fb7-37da-4c67-abae-186828f3306c
  Args:
    type: :Woman
    source: :QueenElizabethTheQueenMother
  AssignClass (17c8040f-babb-4f67-a5a3-192604728440)
 Call ID: 17c8040f-babb-4f67-a5a3-192604728440
  Args:
    type: :Person
    source: :QueenElizabethTheQueenMother
  AddTriple (a300213f-ee58-4eb7-968e-936ca2656605)
 Call ID: a300213f-ee58-4eb7-968e-936ca2656605
  Args:
    source: :RoseConstanceLevesonGower
    target: :QueenElizabethTheQueenMother
    relation: :isSisterOf
  AssignClass (a388685a-7884-4453-83d2-0a13187018bc)
 Call ID: a388685a-7884-4453-83d2-0a13187018bc
  Args:
    type: :Woman
    source: :QueenElizabethII
  AssignClass (b65648de-bcd2-4955-afc7-4310622f8ed5)
 Call ID: b65648de-bcd2-4955-afc7-4310622f8ed5
  Args:
    type: :Person
    source: :QueenElizabethII
  AddTriple (d5eb8113-f01a-4aec-a6c6-3e2a64bc79f0)
 Call ID: d5eb8113-f01a-4aec-a6c6-3e2a64bc79f0
  Args:
    source: :RoseConstanceLevesonGower
    target: :QueenElizabethII
    relation: :isAuntOf
  AssignClass (d585304c-2912-443b-97ff-02d61d9803e2)
 Call ID: d585304c-2912-443b-97ff-02d61d9803e2
  Args:
    source: :WilliamLevesonGower
    type: :Man
  AssignClass (1f41e8c4-4d86-4a04-a47a-4c3d8298b0b3)
 Call ID: 1f41e8c4-4d86-4a04-a47a-4c3d8298b0b3
  Args:
    source: :WilliamLevesonGower
    type: :Person
  AddLiteral (55145b89-8b89-4033-9d9e-d1b49717fe43)
 Call ID: 55145b89-8b89-4033-9d9e-d1b49717fe43
  Args:
    relation: :hasMarriageYear
    literal_type: xsd:integer
    literal_value: 1916
    source: :RoseConstanceLevesonGower
  AddTriple (87372f6b-c398-4951-b408-962e57060b99)
 Call ID: 87372f6b-c398-4951-b408-962e57060b99
  Args:
    target: :WilliamLevesonGower
    source: :RoseConstanceLevesonGower
    relation: :hasRelation
  AssignClass (1df49dae-25ed-4175-843e-4c2944751256)
 Call ID: 1df49dae-25ed-4175-843e-4c2944751256
  Args:
    type: :Woman
    source: :PrincessMargaretRoseOfYork
  AssignClass (54c6684e-8a7b-4393-9523-d837ad398e3b)
 Call ID: 54c6684e-8a7b-4393-9523-d837ad398e3b
  Args:
    source: :PrincessMargaretRoseOfYork
    type: :Person
  AddTriple (4fea9508-b1de-4d37-957e-81e560249878)
 Call ID: 4fea9508-b1de-4d37-957e-81e560249878
  Args:
    relation: :isAuntOf
    source: :RoseConstanceLevesonGower
    target: :PrincessMargaretRoseOfYork
  AddLiteral (63c3a92b-b3be-49ad-ad5e-08e38cb8ba4e)
 Call ID: 63c3a92b-b3be-49ad-ad5e-08e38cb8ba4e
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: :WilliamLevesonGower
    literal_value: 1953
  Finish (7e2bab0e-798b-4c6e-b398-36e5ea2d156b)
 Call ID: 7e2bab0e-798b-4c6e-b398-36e5ea2d156b
  Args: