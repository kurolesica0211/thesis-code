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
Prince Henry Victor Louis Frederick of Prussia (German: Heinrich Viktor Ludwig Friedrich; 9 January 1900 – 26 February 1904), was the third son and youngest child of Prince Henry of Prussia and Princess Irene of Hesse and by Rhine.
He was a grandson of Frederick III, German Emperor, through his father and a great-grandson of Queen Victoria.
Life

Prince Heinrich was born on 9 January 1900, in Kiel.
His father was pleased by the birth of yet another son, especially such a handsome one, as the Prince had blonde hair.
The newborn Prince immediately received the title Prince of Prussia with the style Royal Highness, and was baptised
His older brothers were Prince Waldemar, a namesake of his uncle, and Prince Sigismund, a namesake of his other deceased uncle.
The Prince was diagnosed with haemophilia as a young child, but, despite this, was a very cheerful and lively boy who liked to play a lot.
As Henry grew older he became more aware of his condition.
Death

On 25 February, Princess Irene left Heinrich unsupervised for a few minutes while she went to fetch something.
The playful Prince climbed a chair, and then he climbed onto the table.
He started to scream, which immediately attracted the Princess' attention.
However, experiencing this condition, it was certain the young Prince would die.
Aftermath

Prince Heinrich's premature death would later very much affect the Princess, who would withdraw into herself.
One of his older brothers, Prince Waldemar, also had haemophilia.
The middle sibling, Prince Sigismund, was unaffected by the disease.



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
  AssignClass (79d4a08a-8bad-407c-9366-5c75ebe7f7a2)
 Call ID: 79d4a08a-8bad-407c-9366-5c75ebe7f7a2
  Args:
    source: Prince_Henry_Victor_Louis_Frederick_of_Prussia
    type: :Man
  AssignClass (8339f455-a461-448d-b181-ebcbf0380998)
 Call ID: 8339f455-a461-448d-b181-ebcbf0380998
  Args:
    source: Prince_Henry_Victor_Louis_Frederick_of_Prussia
    type: :Person
  AddLiteral (9230c515-2a9e-488f-a4d5-299d2295503a)
 Call ID: 9230c515-2a9e-488f-a4d5-299d2295503a
  Args:
    literal_type: xsd:string
    relation: :knownAs
    source: Prince_Henry_Victor_Louis_Frederick_of_Prussia
    literal_value: Prince Henry Victor Louis Frederick of Prussia
  AddLiteral (2bd5f406-e376-4370-a014-eff669e3b8fc)
 Call ID: 2bd5f406-e376-4370-a014-eff669e3b8fc
  Args:
    relation: :hasBirthYear
    source: Prince_Henry_Victor_Louis_Frederick_of_Prussia
    literal_value: 1900
    literal_type: xsd:integer
  AddLiteral (1e95c4ec-5ca6-4751-97ac-330ceee1dd60)
 Call ID: 1e95c4ec-5ca6-4751-97ac-330ceee1dd60
  Args:
    literal_type: xsd:integer
    literal_value: 1904
    source: Prince_Henry_Victor_Louis_Frederick_of_Prussia
    relation: :hasDeathYear
  AssignClass (124bf061-3fd2-41bc-bb4c-80ad000a311a)
 Call ID: 124bf061-3fd2-41bc-bb4c-80ad000a311a
  Args:
    type: :Man
    source: Prince_Henry_of_Prussia
  AssignClass (9d24c868-43fe-4ea2-8c25-18a57391de5b)
 Call ID: 9d24c868-43fe-4ea2-8c25-18a57391de5b
  Args:
    source: Prince_Henry_of_Prussia
    type: :Person
  AssignClass (20320a7d-9e1e-4316-b45d-ddd95ff5f096)
 Call ID: 20320a7d-9e1e-4316-b45d-ddd95ff5f096
  Args:
    source: Princess_Irene_of_Hesse_and_by_Rhine
    type: :Woman
  AssignClass (5f66c20a-b437-4201-a090-72aa0b559a6c)
 Call ID: 5f66c20a-b437-4201-a090-72aa0b559a6c
  Args:
    source: Princess_Irene_of_Hesse_and_by_Rhine
    type: :Person
  AddTriple (8fc1bf5f-9fa3-4143-978d-9ef0627e1c14)
 Call ID: 8fc1bf5f-9fa3-4143-978d-9ef0627e1c14
  Args:
    relation: :hasFather
    source: Prince_Henry_Victor_Louis_Frederick_of_Prussia
    target: Prince_Henry_of_Prussia
  AddTriple (d8f9c728-e896-468f-9b86-1b7cc97ff8c2)
 Call ID: d8f9c728-e896-468f-9b86-1b7cc97ff8c2
  Args:
    target: Princess_Irene_of_Hesse_and_by_Rhine
    source: Prince_Henry_Victor_Louis_Frederick_of_Prussia
    relation: :hasMother
  AssignClass (f2b58934-cd0a-4abd-86ff-a0c647dbe9e1)
 Call ID: f2b58934-cd0a-4abd-86ff-a0c647dbe9e1
  Args:
    source: Frederick_III_German_Emperor
    type: :Man
  AssignClass (b517d305-9fda-4650-afdc-359fcafd6200)
 Call ID: b517d305-9fda-4650-afdc-359fcafd6200
  Args:
    type: :Person
    source: Frederick_III_German_Emperor
  AddTriple (7cdb54c6-7922-4d5a-bc6a-9c60631a1f3d)
 Call ID: 7cdb54c6-7922-4d5a-bc6a-9c60631a1f3d
  Args:
    source: Prince_Henry_of_Prussia
    relation: :hasFather
    target: Frederick_III_German_Emperor
  AssignClass (85a97027-f7c3-4170-9f4b-8fadcd860bae)
 Call ID: 85a97027-f7c3-4170-9f4b-8fadcd860bae
  Args:
    source: Queen_Victoria
    type: :Woman
  AssignClass (d6c04e29-95b2-4833-8c89-6cf7110b38a6)
 Call ID: d6c04e29-95b2-4833-8c89-6cf7110b38a6
  Args:
    type: :Person
    source: Queen_Victoria
  AddTriple (967e0fbf-1e7e-4170-a371-b8056b746b07)
 Call ID: 967e0fbf-1e7e-4170-a371-b8056b746b07
  Args:
    target: Queen_Victoria
    relation: :hasAncestor
    source: Prince_Henry_Victor_Louis_Frederick_of_Prussia
  AssignClass (9203ccae-4575-496f-af79-161e23644972)
 Call ID: 9203ccae-4575-496f-af79-161e23644972
  Args:
    type: :Man
    source: Prince_Waldemar
  AssignClass (ac0b52e3-2615-48c4-880e-29f5fc70bc64)
 Call ID: ac0b52e3-2615-48c4-880e-29f5fc70bc64
  Args:
    type: :Person
    source: Prince_Waldemar
  AssignClass (8b4c7f8c-fe2f-4c3d-9bd3-d8527a32dcda)
 Call ID: 8b4c7f8c-fe2f-4c3d-9bd3-d8527a32dcda
  Args:
    type: :Man
    source: Prince_Sigismund
  AssignClass (8e4811f7-bae2-425e-95fe-817b554aea7b)
 Call ID: 8e4811f7-bae2-425e-95fe-817b554aea7b
  Args:
    type: :Person
    source: Prince_Sigismund
  AddTriple (33e2c663-fdd7-45ae-80a3-96ee2e483e28)
 Call ID: 33e2c663-fdd7-45ae-80a3-96ee2e483e28
  Args:
    relation: :isSiblingOf
    source: Prince_Henry_Victor_Louis_Frederick_of_Prussia
    target: Prince_Waldemar
  AddTriple (88cc2072-1cbe-4f0d-885d-2e97179c622c)
 Call ID: 88cc2072-1cbe-4f0d-885d-2e97179c622c
  Args:
    source: Prince_Henry_Victor_Louis_Frederick_of_Prussia
    relation: :isSiblingOf
    target: Prince_Sigismund
  Finish (0e31f0b3-c9a8-463e-8838-4c88f2d14327)
 Call ID: 0e31f0b3-c9a8-463e-8838-4c88f2d14327
  Args: