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
Berthold Prinz und Markgraf von Baden (24 February 1906 – 27 October 1963), styled Margrave of Baden and Duke of Zähringen, was the head of the House of Baden, which had reigned over the Grand Duchy of Baden until 1918, from 1929 until his death.
He was the brother-in-law of Prince Philip, Duke of Edinburgh, through his marriage to Philip's sister, Princess Theodora of Greece and Denmark.
Marriage and children

The only son and younger child of Prince Maximilian, Margrave of Baden and Princess Marie Louise of Hanover, Berthold married his second cousin Princess Theodora of Greece and Denmark, daughter of Prince Andrew of Greece and Denmark and Princess Alice of Battenberg, on 17 August 1931 in Baden-Baden.
Via his marriage, he was the brother-in-law of Prince Philip of Greece and Denmark, later Prince Philip, Duke of Edinburgh from November 1947.
His bride was also his second cousin, through Christian IX of Denmark.
The couple had three children:


Personal life

He was conscripted as a soldier into the army of the Wehrmacht, but served only briefly and was exempted from military service in 1940 after being injured in France.
Death

Berthold died on 27 October 1963, aged 57, in Spaichingen.
He was succeeded as titular margrave and head of house by his son Max.



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
  AssignClass (cf12a60a-be89-4330-b777-c84c9c2359a8)
 Call ID: cf12a60a-be89-4330-b777-c84c9c2359a8
  Args:
    type: :Man
    source: Berthold_Prinz_und_Markgraf_von_Baden
  AssignClass (2bc97668-77de-4bcc-8fb3-84af359832f6)
 Call ID: 2bc97668-77de-4bcc-8fb3-84af359832f6
  Args:
    type: :Person
    source: Berthold_Prinz_und_Markgraf_von_Baden
  AddLiteral (d7f80e1d-29c4-4178-89af-9b0c4f5d0731)
 Call ID: d7f80e1d-29c4-4178-89af-9b0c4f5d0731
  Args:
    literal_value: 1906
    source: Berthold_Prinz_und_Markgraf_von_Baden
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (d274cc3d-ecfd-4eb1-b242-4d5ebc140710)
 Call ID: d274cc3d-ecfd-4eb1-b242-4d5ebc140710
  Args:
    literal_value: 1963
    source: Berthold_Prinz_und_Markgraf_von_Baden
    literal_type: xsd:integer
    relation: :hasDeathYear
  AssignClass (42c30e90-342f-43a2-8b7f-867c96404ee1)
 Call ID: 42c30e90-342f-43a2-8b7f-867c96404ee1
  Args:
    source: Prince_Maximilian_Margrave_of_Baden
    type: :Man
  AssignClass (b6041914-e878-4612-96eb-5b952a9a1223)
 Call ID: b6041914-e878-4612-96eb-5b952a9a1223
  Args:
    source: Prince_Maximilian_Margrave_of_Baden
    type: :Person
  AssignClass (ef2aa25d-6131-4fd3-9ed2-c5683454499b)
 Call ID: ef2aa25d-6131-4fd3-9ed2-c5683454499b
  Args:
    type: :Woman
    source: Princess_Marie_Louise_of_Hanover
  AssignClass (1ab2b494-db17-4a66-8e80-770eebb27d61)
 Call ID: 1ab2b494-db17-4a66-8e80-770eebb27d61
  Args:
    source: Princess_Marie_Louise_of_Hanover
    type: :Person
  AddTriple (65473199-3784-4a5b-9a2d-ca39b7df4556)
 Call ID: 65473199-3784-4a5b-9a2d-ca39b7df4556
  Args:
    target: Prince_Maximilian_Margrave_of_Baden
    source: Berthold_Prinz_und_Markgraf_von_Baden
    relation: :hasFather
  AddTriple (a8011bc4-aa36-414a-aa5d-5cd7e238071a)
 Call ID: a8011bc4-aa36-414a-aa5d-5cd7e238071a
  Args:
    target: Princess_Marie_Louise_of_Hanover
    source: Berthold_Prinz_und_Markgraf_von_Baden
    relation: :hasMother
  AssignClass (ce3ea81e-904a-470c-8a29-52096b34d74e)
 Call ID: ce3ea81e-904a-470c-8a29-52096b34d74e
  Args:
    source: Princess_Theodora_of_Greece_and_Denmark
    type: :Woman
  AssignClass (00b33703-1fcd-45f7-bec1-b252ab4a6159)
 Call ID: 00b33703-1fcd-45f7-bec1-b252ab4a6159
  Args:
    type: :Person
    source: Princess_Theodora_of_Greece_and_Denmark
  AddLiteral (07fd71d6-ea1f-476d-aa46-16bc301b4262)
 Call ID: 07fd71d6-ea1f-476d-aa46-16bc301b4262
  Args:
    relation: :hasMarriageYear
    literal_value: 1931
    source: Berthold_Prinz_und_Markgraf_von_Baden
    literal_type: xsd:integer
  AddTriple (a18a469c-4659-4d03-a8ee-f32e90adcf7f)
 Call ID: a18a469c-4659-4d03-a8ee-f32e90adcf7f
  Args:
    target: Princess_Theodora_of_Greece_and_Denmark
    source: Berthold_Prinz_und_Markgraf_von_Baden
    relation: :hasRelation
  AssignClass (d4dcfc22-d08f-42ec-acef-cd72f780a1d0)
 Call ID: d4dcfc22-d08f-42ec-acef-cd72f780a1d0
  Args:
    source: Prince_Andrew_of_Greece_and_Denmark
    type: :Man
  AssignClass (c4307792-da74-4664-87d8-49f752e6c499)
 Call ID: c4307792-da74-4664-87d8-49f752e6c499
  Args:
    source: Prince_Andrew_of_Greece_and_Denmark
    type: :Person
  AssignClass (a2e9336b-7749-49ee-8680-2c2597e52331)
 Call ID: a2e9336b-7749-49ee-8680-2c2597e52331
  Args:
    source: Princess_Alice_of_Battenberg
    type: :Woman
  AssignClass (9d970546-ccd6-4b60-be47-6f1aec308c49)
 Call ID: 9d970546-ccd6-4b60-be47-6f1aec308c49
  Args:
    source: Princess_Alice_of_Battenberg
    type: :Person
  AddTriple (b6b781c9-c12d-48ee-8ffc-f54b6e583a8a)
 Call ID: b6b781c9-c12d-48ee-8ffc-f54b6e583a8a
  Args:
    relation: :hasFather
    target: Prince_Andrew_of_Greece_and_Denmark
    source: Princess_Theodora_of_Greece_and_Denmark
  AddTriple (a109027e-5a07-458f-8e53-6a0684927adf)
 Call ID: a109027e-5a07-458f-8e53-6a0684927adf
  Args:
    target: Princess_Alice_of_Battenberg
    source: Princess_Theodora_of_Greece_and_Denmark
    relation: :hasMother
  AssignClass (fd4f9ef8-65e7-47e7-a2a1-00e52132c89f)
 Call ID: fd4f9ef8-65e7-47e7-a2a1-00e52132c89f
  Args:
    source: Prince_Philip_Duke_of_Edinburgh
    type: :Man
  AssignClass (687405cc-aa79-4cb3-97fe-61aada884d9b)
 Call ID: 687405cc-aa79-4cb3-97fe-61aada884d9b
  Args:
    type: :Person
    source: Prince_Philip_Duke_of_Edinburgh
  AddTriple (936ebc7d-4c1a-41fe-b4d8-893d746910b1)
 Call ID: 936ebc7d-4c1a-41fe-b4d8-893d746910b1
  Args:
    source: Prince_Philip_Duke_of_Edinburgh
    target: Princess_Theodora_of_Greece_and_Denmark
    relation: :isSiblingOf
  AssignClass (3be83bcb-edee-471c-8b6d-9ccab91fcc22)
 Call ID: 3be83bcb-edee-471c-8b6d-9ccab91fcc22
  Args:
    source: Max
    type: :Man
  AssignClass (9982d316-0013-4e91-a9cc-6b523d0a42d1)
 Call ID: 9982d316-0013-4e91-a9cc-6b523d0a42d1
  Args:
    type: :Person
    source: Max
  AddTriple (9095cd0e-39ab-4ec6-89ad-826c5d6b0220)
 Call ID: 9095cd0e-39ab-4ec6-89ad-826c5d6b0220
  Args:
    target: Berthold_Prinz_und_Markgraf_von_Baden
    source: Max
    relation: :hasFather
  Finish (acfcc755-cdad-4f2a-9767-2fe3b5cf919e)
 Call ID: acfcc755-cdad-4f2a-9767-2fe3b5cf919e
  Args: