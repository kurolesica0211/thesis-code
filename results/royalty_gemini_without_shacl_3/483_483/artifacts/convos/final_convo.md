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
Prince Hermann Friedrich Fernando Roland of Leiningen (German: Hermann Friedrich Fernando Roland Prinz zu Leiningen; born April 16, 1963) is a Canadian banker and the younger son of Prince Karl of Leiningen and Princess Marie Louise of Bulgaria.
Life

Leiningen was born in Toronto, Ontario.
Through his mother, Leiningen is a grandson of King Boris III of Bulgaria, a great-grandson of King Victor Emmanuel III of Italy and great-great-grandson of King Nicholas of Montenegro.
Leiningen is a financial analyst and banker, addressed as Mr. Hermann Leiningen professionally.
As of 2015, Leiningen worked for a division of Royal Bank of Canada.
On 16 May 1987, Leiningen married Deborah Cully (born December 2, 1961).
Prince Herman is an honorary member of the Board of Trustees of the H.C.V. Princess Marie Louise and of the King Boris and Queen Giovanna Fund who manages Vrana Palace in Sofia.



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
  AssignClass (ce06e72e-f24d-4332-b938-daa0262647c2)
 Call ID: ce06e72e-f24d-4332-b938-daa0262647c2
  Args:
    type: :Man
    source: Prince_Hermann_Friedrich_Fernando_Roland_of_Leiningen
  AssignClass (ca8edd4f-6f35-4742-8636-e8eb5959a059)
 Call ID: ca8edd4f-6f35-4742-8636-e8eb5959a059
  Args:
    type: :Person
    source: Prince_Hermann_Friedrich_Fernando_Roland_of_Leiningen
  AddLiteral (c5df1468-3fa2-4573-87e6-d3f2bc94539f)
 Call ID: c5df1468-3fa2-4573-87e6-d3f2bc94539f
  Args:
    source: Prince_Hermann_Friedrich_Fernando_Roland_of_Leiningen
    literal_type: xsd:integer
    literal_value: 1963
    relation: :hasBirthYear
  AddLiteral (5e477654-e7ce-48a1-99a9-65eaf6599185)
 Call ID: 5e477654-e7ce-48a1-99a9-65eaf6599185
  Args:
    relation: :knownAs
    literal_type: xsd:string
    literal_value: Hermann Leiningen
    source: Prince_Hermann_Friedrich_Fernando_Roland_of_Leiningen
  AssignClass (d29e26d7-dcad-4020-8828-b9eb5588d44c)
 Call ID: d29e26d7-dcad-4020-8828-b9eb5588d44c
  Args:
    type: :Man
    source: Prince_Karl_of_Leiningen
  AssignClass (95c6b2ca-c89d-405b-96c8-e2e997cdaa9f)
 Call ID: 95c6b2ca-c89d-405b-96c8-e2e997cdaa9f
  Args:
    type: :Person
    source: Prince_Karl_of_Leiningen
  AssignClass (7eda8bc6-5b16-439b-ae21-7b31ee11ea37)
 Call ID: 7eda8bc6-5b16-439b-ae21-7b31ee11ea37
  Args:
    type: :Woman
    source: Princess_Marie_Louise_of_Bulgaria
  AssignClass (1f5a1350-634d-445c-b67c-8ff1ba999262)
 Call ID: 1f5a1350-634d-445c-b67c-8ff1ba999262
  Args:
    type: :Person
    source: Princess_Marie_Louise_of_Bulgaria
  AddTriple (e7f5b598-a5f8-4396-9160-7cac3b0b1295)
 Call ID: e7f5b598-a5f8-4396-9160-7cac3b0b1295
  Args:
    relation: :hasFather
    source: Prince_Hermann_Friedrich_Fernando_Roland_of_Leiningen
    target: Prince_Karl_of_Leiningen
  AddTriple (16773af1-0973-47af-a84e-627ef54565eb)
 Call ID: 16773af1-0973-47af-a84e-627ef54565eb
  Args:
    relation: :hasMother
    source: Prince_Hermann_Friedrich_Fernando_Roland_of_Leiningen
    target: Princess_Marie_Louise_of_Bulgaria
  AssignClass (cdc2aca8-b3ab-4754-8d29-76f73e73ccce)
 Call ID: cdc2aca8-b3ab-4754-8d29-76f73e73ccce
  Args:
    type: :Man
    source: King_Boris_III_of_Bulgaria
  AssignClass (d044c8fd-923b-4f48-87f5-eb62884770b8)
 Call ID: d044c8fd-923b-4f48-87f5-eb62884770b8
  Args:
    type: :Person
    source: King_Boris_III_of_Bulgaria
  AddTriple (c368c540-19ef-4b31-97f3-21f1a5753703)
 Call ID: c368c540-19ef-4b31-97f3-21f1a5753703
  Args:
    source: Princess_Marie_Louise_of_Bulgaria
    target: King_Boris_III_of_Bulgaria
    relation: :hasFather
  AssignClass (ec6f08a8-f5bd-45e0-9a68-89a742a22a9b)
 Call ID: ec6f08a8-f5bd-45e0-9a68-89a742a22a9b
  Args:
    type: :Man
    source: King_Victor_Emmanuel_III_of_Italy
  AssignClass (6cb2ebac-abc2-469e-964d-9a1b1b15d774)
 Call ID: 6cb2ebac-abc2-469e-964d-9a1b1b15d774
  Args:
    type: :Person
    source: King_Victor_Emmanuel_III_of_Italy
  AddTriple (fa8586ea-d3eb-4854-b857-2f2805790760)
 Call ID: fa8586ea-d3eb-4854-b857-2f2805790760
  Args:
    relation: :hasFather
    source: King_Boris_III_of_Bulgaria
    target: King_Victor_Emmanuel_III_of_Italy
  AssignClass (5144fdd7-3010-47e2-ad3e-923d19075fee)
 Call ID: 5144fdd7-3010-47e2-ad3e-923d19075fee
  Args:
    type: :Man
    source: King_Nicholas_of_Montenegro
  AssignClass (ba1b0e94-2908-46a2-90cc-cd4fa3236074)
 Call ID: ba1b0e94-2908-46a2-90cc-cd4fa3236074
  Args:
    type: :Person
    source: King_Nicholas_of_Montenegro
  AddTriple (dfa76ce4-38b9-44da-9c91-07b05a1a25cd)
 Call ID: dfa76ce4-38b9-44da-9c91-07b05a1a25cd
  Args:
    relation: :hasFather
    target: King_Nicholas_of_Montenegro
    source: King_Victor_Emmanuel_III_of_Italy
  AssignClass (c943e9bc-e855-45c0-9212-c360531b978d)
 Call ID: c943e9bc-e855-45c0-9212-c360531b978d
  Args:
    type: :Woman
    source: Deborah_Cully
  AssignClass (7ed047dc-4ca7-4323-b6f4-d7ecf4d41251)
 Call ID: 7ed047dc-4ca7-4323-b6f4-d7ecf4d41251
  Args:
    type: :Person
    source: Deborah_Cully
  AddLiteral (231f9e05-ccfb-4960-a4ae-ae8f334f7477)
 Call ID: 231f9e05-ccfb-4960-a4ae-ae8f334f7477
  Args:
    literal_type: xsd:integer
    literal_value: 1961
    source: Deborah_Cully
    relation: :hasBirthYear
  AddTriple (0150e06c-35e1-4407-8a0d-b03730bbb7e6)
 Call ID: 0150e06c-35e1-4407-8a0d-b03730bbb7e6
  Args:
    relation: :hasRelation
    source: Prince_Hermann_Friedrich_Fernando_Roland_of_Leiningen
    target: Deborah_Cully
  AddLiteral (a77dba2e-875e-4145-b851-8e0656c18f08)
 Call ID: a77dba2e-875e-4145-b851-8e0656c18f08
  Args:
    source: Prince_Hermann_Friedrich_Fernando_Roland_of_Leiningen
    literal_value: 1987
    literal_type: xsd:integer
    relation: :hasMarriageYear
  Finish (ca238a44-a478-4cba-8adb-53da595ecfc7)
 Call ID: ca238a44-a478-4cba-8adb-53da595ecfc7
  Args: