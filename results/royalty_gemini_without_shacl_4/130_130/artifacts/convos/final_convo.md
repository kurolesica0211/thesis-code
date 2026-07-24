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
  AssignClass (f25a3282-f422-4834-9312-3e9cd0444002)
 Call ID: f25a3282-f422-4834-9312-3e9cd0444002
  Args:
    source: George_William_of_Hanover
    type: :Man
  AssignClass (8aa99bb4-0004-42c1-8bae-3a51757c1da4)
 Call ID: 8aa99bb4-0004-42c1-8bae-3a51757c1da4
  Args:
    type: :Person
    source: George_William_of_Hanover
  AddLiteral (53715e6a-7494-409d-97f7-88810eedfd63)
 Call ID: 53715e6a-7494-409d-97f7-88810eedfd63
  Args:
    literal_value: 1880
    source: George_William_of_Hanover
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (eac64116-ccb0-40e9-9647-b26295b6b3da)
 Call ID: eac64116-ccb0-40e9-9647-b26295b6b3da
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1912
    source: George_William_of_Hanover
  AssignClass (89626326-f288-4caa-93c8-cf795a812ccd)
 Call ID: 89626326-f288-4caa-93c8-cf795a812ccd
  Args:
    source: Ernest_Augustus_Crown_Prince_of_Hanover
    type: :Man
  AssignClass (e03eb157-aeac-4749-96fb-ceb7f4777c9c)
 Call ID: e03eb157-aeac-4749-96fb-ceb7f4777c9c
  Args:
    type: :Person
    source: Ernest_Augustus_Crown_Prince_of_Hanover
  AssignClass (78074e66-a2a7-4440-8710-b4aacd921948)
 Call ID: 78074e66-a2a7-4440-8710-b4aacd921948
  Args:
    type: :Woman
    source: Princess_Thyra_of_Denmark
  AssignClass (22a1701f-686f-4ba0-80da-6a558b1660a6)
 Call ID: 22a1701f-686f-4ba0-80da-6a558b1660a6
  Args:
    type: :Person
    source: Princess_Thyra_of_Denmark
  AddTriple (408988ba-1567-4095-8750-685e518f401b)
 Call ID: 408988ba-1567-4095-8750-685e518f401b
  Args:
    source: George_William_of_Hanover
    target: Ernest_Augustus_Crown_Prince_of_Hanover
    relation: :hasFather
  AddTriple (79b7cca8-ffbf-4990-9db4-df2e9f652d89)
 Call ID: 79b7cca8-ffbf-4990-9db4-df2e9f652d89
  Args:
    source: George_William_of_Hanover
    target: Princess_Thyra_of_Denmark
    relation: :hasMother
  AssignClass (3d459ee6-0c21-4bfe-aa37-5d4274c219e2)
 Call ID: 3d459ee6-0c21-4bfe-aa37-5d4274c219e2
  Args:
    type: :Man
    source: George_V_of_Hanover
  AssignClass (461dd3bd-7861-4a32-a938-554e24ab305c)
 Call ID: 461dd3bd-7861-4a32-a938-554e24ab305c
  Args:
    source: George_V_of_Hanover
    type: :Person
  AddTriple (b8a41cec-0a9c-451e-a456-6f418b7c1ee7)
 Call ID: b8a41cec-0a9c-451e-a456-6f418b7c1ee7
  Args:
    relation: :hasFather
    source: Ernest_Augustus_Crown_Prince_of_Hanover
    target: George_V_of_Hanover
  AssignClass (6da7d4bc-8573-4d2a-bdd4-22dd9f27c91e)
 Call ID: 6da7d4bc-8573-4d2a-bdd4-22dd9f27c91e
  Args:
    source: Christian_IX_of_Denmark
    type: :Man
  AssignClass (7345ac90-6262-4854-8b4f-0c9570f7a37b)
 Call ID: 7345ac90-6262-4854-8b4f-0c9570f7a37b
  Args:
    type: :Person
    source: Christian_IX_of_Denmark
  AddTriple (72324f44-4d97-4ffc-993c-c656121d8666)
 Call ID: 72324f44-4d97-4ffc-993c-c656121d8666
  Args:
    relation: :hasFather
    target: Christian_IX_of_Denmark
    source: Princess_Thyra_of_Denmark
  AssignClass (f4dd26df-3c62-4c76-88a7-95a257abc89a)
 Call ID: f4dd26df-3c62-4c76-88a7-95a257abc89a
  Args:
    type: :Man
    source: Prince_Ernest_Augustus_Duke_of_Cumberland_and_Teviotdale
  AssignClass (1ee42330-338d-4c83-b607-76d40fa9c4e6)
 Call ID: 1ee42330-338d-4c83-b607-76d40fa9c4e6
  Args:
    source: Prince_Ernest_Augustus_Duke_of_Cumberland_and_Teviotdale
    type: :Person
  AddTriple (07368c72-5573-460b-aab0-7e32c0c25c67)
 Call ID: 07368c72-5573-460b-aab0-7e32c0c25c67
  Args:
    target: George_V_of_Hanover
    source: Prince_Ernest_Augustus_Duke_of_Cumberland_and_Teviotdale
    relation: :isFatherOf
  AssignClass (01870d85-f92e-4cc5-a6dd-72dd8b74b4c1)
 Call ID: 01870d85-f92e-4cc5-a6dd-72dd8b74b4c1
  Args:
    source: George_III_of_the_United_Kingdom
    type: :Man
  AssignClass (a04cdd87-bbf7-4b1c-83ba-3d1239853603)
 Call ID: a04cdd87-bbf7-4b1c-83ba-3d1239853603
  Args:
    type: :Person
    source: George_III_of_the_United_Kingdom
  AddTriple (0c5c0e2b-1221-4053-be68-3f8b3cf7b142)
 Call ID: 0c5c0e2b-1221-4053-be68-3f8b3cf7b142
  Args:
    relation: :hasFather
    source: Prince_Ernest_Augustus_Duke_of_Cumberland_and_Teviotdale
    target: George_III_of_the_United_Kingdom
  AssignClass (f66826c0-0cc6-430a-baf5-719a80abbb47)
 Call ID: f66826c0-0cc6-430a-baf5-719a80abbb47
  Args:
    type: :Man
    source: Ernest_Augustus_son_of_Ernest_Augustus
  AssignClass (1bf45eae-6f21-4ba0-8b19-61a60538e0fe)
 Call ID: 1bf45eae-6f21-4ba0-8b19-61a60538e0fe
  Args:
    source: Ernest_Augustus_son_of_Ernest_Augustus
    type: :Person
  AddTriple (673ba6aa-85ec-447d-9e9e-6366a41ef1e8)
 Call ID: 673ba6aa-85ec-447d-9e9e-6366a41ef1e8
  Args:
    source: Ernest_Augustus_son_of_Ernest_Augustus
    target: Ernest_Augustus_Crown_Prince_of_Hanover
    relation: :hasFather
  AddTriple (ae0bbffc-d83e-47d8-ad63-c9ca9b8b9e96)
 Call ID: ae0bbffc-d83e-47d8-ad63-c9ca9b8b9e96
  Args:
    relation: :hasMother
    source: Ernest_Augustus_son_of_Ernest_Augustus
    target: Princess_Thyra_of_Denmark
  AssignClass (9fbfb6f8-2841-4165-89b2-dc56bdb40c38)
 Call ID: 9fbfb6f8-2841-4165-89b2-dc56bdb40c38
  Args:
    type: :Woman
    source: Princess_Victoria_Louise_of_Prussia
  AssignClass (139b2c8e-dc3d-4b89-9eef-c7f646adb5ed)
 Call ID: 139b2c8e-dc3d-4b89-9eef-c7f646adb5ed
  Args:
    source: Princess_Victoria_Louise_of_Prussia
    type: :Person
  AddTriple (35433b53-ec9f-4784-897f-a901ff7b3783)
 Call ID: 35433b53-ec9f-4784-897f-a901ff7b3783
  Args:
    target: Princess_Victoria_Louise_of_Prussia
    source: Ernest_Augustus_son_of_Ernest_Augustus
    relation: :hasRelation
  AddLiteral (e158e55e-8607-46ad-9a67-8cb2a923d40c)
 Call ID: e158e55e-8607-46ad-9a67-8cb2a923d40c
  Args:
    literal_value: 1913
    source: Ernest_Augustus_son_of_Ernest_Augustus
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AddTriple (e8efb653-87aa-48e3-9f83-9ba22fd711a1)
 Call ID: e8efb653-87aa-48e3-9f83-9ba22fd711a1
  Args:
    relation: :hasMarriageYear
    source: Princess_Victoria_Louise_of_Prussia
    target: Ernest_Augustus_son_of_Ernest_Augustus
  Finish (ff6e3619-d75c-42a6-8f40-c0376ed29bf9)
 Call ID: ff6e3619-d75c-42a6-8f40-c0376ed29bf9
  Args: