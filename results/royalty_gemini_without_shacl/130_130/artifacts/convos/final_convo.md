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
George William, Hereditary Prince of Hanover, Duke of Brunswick-Lüneburg (German: Georg Wilhelm Christian Albert Edward Alexander Friedrich Ernst Waldemar Adolf; 28 October 1880 – 20 May 1912) was a German prince from the House of Hanover.
He was the second child and eldest son of Ernest Augustus, Crown Prince of Hanover and Duke of Cumberland, and Princess Thyra of Denmark.
His father was the only son of George V of Hanover and his mother was the youngest daughter of Christian IX of Denmark.
His great-grandfather, Prince Ernest Augustus, Duke of Cumberland and Teviotdale, the fifth son of George III of the United Kingdom, became king of Hanover in 1837 because Salic Law barred Queen Victoria from inheriting the Hanoverian throne.
His godparents included his maternal grandfather Christian IX of Denmark, his uncle George I of Greece, his uncle Frederick, Crown Prince of Denmark, his uncle Alexander Alexandrovich, Tsarevich of Russia, his uncle Albert Edward, Prince of Wales, his uncle Prince Valdemar of Denmark, Prince George, Duke of Cambridge, and William, Duke of Brunswick.
The family had lived in exile in Austria since the Kingdom of Hanover was annexed by Prussia in the aftermath of the 1866 Austro-Prussian War.
His father succeeded as pretender to the Hanoverian throne and as Duke of Cumberland and Teviotdale in the peerage of Great Britain in 1878.
He represented his father at the funeral of Edward VII and the coronation of George V.


When his kinsman William, Duke of Brunswick, died unmarried in 1884, George William was his heir after his father.
Otto von Bismarck blocked Crown Ernest Augustus's claim because he had never relinquished his claim to Hanover and instead appointed Prince Albert of Prussia regent.
Prince Albert died in 1906 and Crown Ernest Augustus offered that he and George William would renounce their claims to Brunswick to allow his second son Prince Ernest Augustus to succeed.
The Bundesrat rejected this and appointed Duke John Albert of Mecklenburg as regent.
The younger Ernest Augustus finally succeeded in 1913 after he married the German Emperor's daughter after George William's death.
Death

On 20 May 1912, George William was killed, aged 31, in a car crash near Nackel, Brandenburg, while driving from Prague to Copenhagen to attend the funeral of his uncle, Frederick VIII of Denmark.
In response to George William's death, Wilhelm II, German Emperor, sent his sons Prince Eitel Friedrich and Prince August Wilhelm of Prussia to Nackel and sent a message of condolence to the Duke of Cumberland.
In response to this friendly gesture, the Duke sent his only surviving son, Ernest Augustus, to Berlin to thank the Emperor.
In Berlin, Ernest Augustus met and fell in love with the emperor's only daughter, Princess Victoria Louise of Prussia.
They married in 1913, thus reconciling the Houses of Hohenzollern and Hanover, and the Emperor approved Ernest Augustus's succession to the duchy of Brunswick shortly after.



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
  AssignClass (539ed3c8-07e5-4cd5-8edf-da1cec26485e)
 Call ID: 539ed3c8-07e5-4cd5-8edf-da1cec26485e
  Args:
    source: George_William_of_Hanover
    type: :Man
  AssignClass (0c1f2063-f45d-4a9e-8e75-ad606ad47997)
 Call ID: 0c1f2063-f45d-4a9e-8e75-ad606ad47997
  Args:
    source: George_William_of_Hanover
    type: :Person
  AddLiteral (b6387ff4-e62b-4acc-8a63-d1bb89afb424)
 Call ID: b6387ff4-e62b-4acc-8a63-d1bb89afb424
  Args:
    literal_type: xsd:integer
    literal_value: 1880
    source: George_William_of_Hanover
    relation: :hasBirthYear
  AddLiteral (269690cc-a65d-4710-9881-7d47bfc2b7fc)
 Call ID: 269690cc-a65d-4710-9881-7d47bfc2b7fc
  Args:
    source: George_William_of_Hanover
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 1912
  AssignClass (57985a65-55a1-4011-96cf-b5d654b9cc81)
 Call ID: 57985a65-55a1-4011-96cf-b5d654b9cc81
  Args:
    type: :Man
    source: Ernest_Augustus_Crown_Prince_of_Hanover
  AssignClass (59606f9d-4630-4535-9b84-7107b400ffb7)
 Call ID: 59606f9d-4630-4535-9b84-7107b400ffb7
  Args:
    type: :Person
    source: Ernest_Augustus_Crown_Prince_of_Hanover
  AssignClass (00bb32be-96bb-458b-a13b-c4b2a990ca5e)
 Call ID: 00bb32be-96bb-458b-a13b-c4b2a990ca5e
  Args:
    type: :Woman
    source: Princess_Thyra_of_Denmark
  AssignClass (7b107808-a28e-42d6-a6e2-d98d2ae4bca9)
 Call ID: 7b107808-a28e-42d6-a6e2-d98d2ae4bca9
  Args:
    source: Princess_Thyra_of_Denmark
    type: :Person
  AddTriple (84243795-05d6-4e18-a736-646e660b1957)
 Call ID: 84243795-05d6-4e18-a736-646e660b1957
  Args:
    source: George_William_of_Hanover
    relation: :hasFather
    target: Ernest_Augustus_Crown_Prince_of_Hanover
  AddTriple (90080f6c-2ffa-44b1-b4fa-51537048d46a)
 Call ID: 90080f6c-2ffa-44b1-b4fa-51537048d46a
  Args:
    target: Princess_Thyra_of_Denmark
    relation: :hasMother
    source: George_William_of_Hanover
  AssignClass (36aebac6-0784-4cbf-ab94-207d8f1b9c7f)
 Call ID: 36aebac6-0784-4cbf-ab94-207d8f1b9c7f
  Args:
    source: George_V_of_Hanover
    type: :Man
  AssignClass (0e9f7601-ed58-4dba-9a3f-ac6167cdb187)
 Call ID: 0e9f7601-ed58-4dba-9a3f-ac6167cdb187
  Args:
    source: George_V_of_Hanover
    type: :Person
  AddTriple (b4ad910c-6f5b-4ee4-8cf4-8ea15a6469c6)
 Call ID: b4ad910c-6f5b-4ee4-8cf4-8ea15a6469c6
  Args:
    target: George_V_of_Hanover
    source: Ernest_Augustus_Crown_Prince_of_Hanover
    relation: :hasFather
  AssignClass (0eb5cc3c-126c-4ca5-916e-959f0135815d)
 Call ID: 0eb5cc3c-126c-4ca5-916e-959f0135815d
  Args:
    type: :Man
    source: Christian_IX_of_Denmark
  AssignClass (b447febf-3d50-45a1-905b-3afbe406b41d)
 Call ID: b447febf-3d50-45a1-905b-3afbe406b41d
  Args:
    source: Christian_IX_of_Denmark
    type: :Person
  AddTriple (283f9a0e-857e-41b0-9aa4-f35ad00103f9)
 Call ID: 283f9a0e-857e-41b0-9aa4-f35ad00103f9
  Args:
    target: Christian_IX_of_Denmark
    source: Princess_Thyra_of_Denmark
    relation: :hasFather
  AssignClass (d4605fff-2e71-408e-adbb-83e8fcb1dcb6)
 Call ID: d4605fff-2e71-408e-adbb-83e8fcb1dcb6
  Args:
    type: :Man
    source: Prince_Ernest_Augustus_Duke_of_Cumberland_and_Teviotdale
  AssignClass (9b541032-a7d1-4ec6-8661-21af6550c9b0)
 Call ID: 9b541032-a7d1-4ec6-8661-21af6550c9b0
  Args:
    source: Prince_Ernest_Augustus_Duke_of_Cumberland_and_Teviotdale
    type: :Person
  AssignClass (710f34b5-0a77-4ab5-988b-db1b34fedcc8)
 Call ID: 710f34b5-0a77-4ab5-988b-db1b34fedcc8
  Args:
    type: :Man
    source: George_III_of_the_United_Kingdom
  AssignClass (36062325-2922-45cf-b609-860053b1f44a)
 Call ID: 36062325-2922-45cf-b609-860053b1f44a
  Args:
    source: George_III_of_the_United_Kingdom
    type: :Person
  AddTriple (10a401aa-d1b5-4645-bcfb-8a7ede9353c0)
 Call ID: 10a401aa-d1b5-4645-bcfb-8a7ede9353c0
  Args:
    target: George_III_of_the_United_Kingdom
    source: Prince_Ernest_Augustus_Duke_of_Cumberland_and_Teviotdale
    relation: :hasFather
  AddTriple (7563066a-eaeb-4d3a-b234-5166a74775d8)
 Call ID: 7563066a-eaeb-4d3a-b234-5166a74775d8
  Args:
    relation: :hasFather
    source: George_V_of_Hanover
    target: Prince_Ernest_Augustus_Duke_of_Cumberland_and_Teviotdale
  AssignClass (218de4e5-fc43-4ba7-b04c-be38942b9a2f)
 Call ID: 218de4e5-fc43-4ba7-b04c-be38942b9a2f
  Args:
    source: Prince_Ernest_Augustus_the_younger
    type: :Man
  AssignClass (6c3aa7a8-98ab-4d42-be43-14d1004aa117)
 Call ID: 6c3aa7a8-98ab-4d42-be43-14d1004aa117
  Args:
    source: Prince_Ernest_Augustus_the_younger
    type: :Person
  AddTriple (ad3d8019-b3af-473b-9014-8c4f5427193e)
 Call ID: ad3d8019-b3af-473b-9014-8c4f5427193e
  Args:
    source: Prince_Ernest_Augustus_the_younger
    relation: :hasFather
    target: Ernest_Augustus_Crown_Prince_of_Hanover
  AssignClass (7474924c-dcd9-4171-b013-1ae6d877189c)
 Call ID: 7474924c-dcd9-4171-b013-1ae6d877189c
  Args:
    source: Princess_Victoria_Louise_of_Prussia
    type: :Woman
  AssignClass (d19ed75f-6f4b-4296-89f8-9de3d708771f)
 Call ID: d19ed75f-6f4b-4296-89f8-9de3d708771f
  Args:
    type: :Person
    source: Princess_Victoria_Louise_of_Prussia
  AddLiteral (9a0c699e-5cad-46b9-ae8d-89e1ef23c7d3)
 Call ID: 9a0c699e-5cad-46b9-ae8d-89e1ef23c7d3
  Args:
    literal_type: xsd:integer
    literal_value: 1913
    source: Prince_Ernest_Augustus_the_younger
    relation: :hasMarriageYear
  AddTriple (fbb6b43c-c321-410e-b7a2-4909c391de83)
 Call ID: fbb6b43c-c321-410e-b7a2-4909c391de83
  Args:
    target: Princess_Victoria_Louise_of_Prussia
    relation: :hasRelation
    source: Prince_Ernest_Augustus_the_younger
  Finish (cb40eb50-8227-4147-9d6d-0ce3b9918f49)
 Call ID: cb40eb50-8227-4147-9d6d-0ce3b9918f49
  Args: