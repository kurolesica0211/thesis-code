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
  AssignClass (5c47f1a3-dc27-41dd-8f47-442453aed2b9)
 Call ID: 5c47f1a3-dc27-41dd-8f47-442453aed2b9
  Args:
    source: George_William
    type: :Man
  AssignClass (78aeeed9-b059-4085-a2d3-e2cf5d7de38c)
 Call ID: 78aeeed9-b059-4085-a2d3-e2cf5d7de38c
  Args:
    type: :Person
    source: George_William
  AddLiteral (796ef9a7-2451-48ca-bf9d-5d2b29a3dde9)
 Call ID: 796ef9a7-2451-48ca-bf9d-5d2b29a3dde9
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: George_William
    literal_value: 1880
  AddLiteral (1ee588a1-334e-4497-be5b-ad5ccd33ffd8)
 Call ID: 1ee588a1-334e-4497-be5b-ad5ccd33ffd8
  Args:
    literal_value: 1912
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: George_William
  AssignClass (5d92fc05-c2a9-48e8-a59f-e68b6b53d5ca)
 Call ID: 5d92fc05-c2a9-48e8-a59f-e68b6b53d5ca
  Args:
    source: Ernest_Augustus_Crown_Prince_of_Hanover
    type: :Man
  AssignClass (bf9b4558-f9b2-4480-9081-f7f9305c4687)
 Call ID: bf9b4558-f9b2-4480-9081-f7f9305c4687
  Args:
    source: Ernest_Augustus_Crown_Prince_of_Hanover
    type: :Person
  AssignClass (c2779169-e3ad-4744-9db2-e4d782098177)
 Call ID: c2779169-e3ad-4744-9db2-e4d782098177
  Args:
    source: Princess_Thyra_of_Denmark
    type: :Woman
  AssignClass (c13be054-97b4-4e95-b6f5-7088e4424671)
 Call ID: c13be054-97b4-4e95-b6f5-7088e4424671
  Args:
    type: :Person
    source: Princess_Thyra_of_Denmark
  AddTriple (1b4d69f6-49f3-4e80-868a-125b48365a57)
 Call ID: 1b4d69f6-49f3-4e80-868a-125b48365a57
  Args:
    source: George_William
    target: Ernest_Augustus_Crown_Prince_of_Hanover
    relation: :hasFather
  AddTriple (85cc352e-9deb-429a-9e82-f43d76850772)
 Call ID: 85cc352e-9deb-429a-9e82-f43d76850772
  Args:
    source: George_William
    relation: :hasMother
    target: Princess_Thyra_of_Denmark
  AssignClass (cfa8b57d-7f3a-4a6c-8b9a-9ffce5a7eb3f)
 Call ID: cfa8b57d-7f3a-4a6c-8b9a-9ffce5a7eb3f
  Args:
    source: George_V_of_Hanover
    type: :Man
  AssignClass (715b2197-03b5-445f-aa72-19ed1eb8469c)
 Call ID: 715b2197-03b5-445f-aa72-19ed1eb8469c
  Args:
    source: George_V_of_Hanover
    type: :Person
  AddTriple (c7e03173-21bb-4bf3-b029-c252a7f87efa)
 Call ID: c7e03173-21bb-4bf3-b029-c252a7f87efa
  Args:
    source: Ernest_Augustus_Crown_Prince_of_Hanover
    target: George_V_of_Hanover
    relation: :hasFather
  AssignClass (daa90d31-d6ed-4830-bb00-5c63053b9c55)
 Call ID: daa90d31-d6ed-4830-bb00-5c63053b9c55
  Args:
    source: Christian_IX_of_Denmark
    type: :Man
  AssignClass (a8920922-d2e3-43fb-8dfd-289edeedf9f2)
 Call ID: a8920922-d2e3-43fb-8dfd-289edeedf9f2
  Args:
    type: :Person
    source: Christian_IX_of_Denmark
  AddTriple (edc5a3b0-e1bb-4c52-95e0-2c81399eaed7)
 Call ID: edc5a3b0-e1bb-4c52-95e0-2c81399eaed7
  Args:
    source: Princess_Thyra_of_Denmark
    target: Christian_IX_of_Denmark
    relation: :hasFather
  AssignClass (f0faa95e-56d4-410a-9847-789291ab4a28)
 Call ID: f0faa95e-56d4-410a-9847-789291ab4a28
  Args:
    source: Prince_Ernest_Augustus_Duke_of_Cumberland_and_Teviotdale
    type: :Man
  AssignClass (422e0965-8a47-4697-b695-49bd1c78fa99)
 Call ID: 422e0965-8a47-4697-b695-49bd1c78fa99
  Args:
    source: Prince_Ernest_Augustus_Duke_of_Cumberland_and_Teviotdale
    type: :Person
  AddTriple (9a69d92a-547d-4e77-9544-c287fb137e59)
 Call ID: 9a69d92a-547d-4e77-9544-c287fb137e59
  Args:
    target: Prince_Ernest_Augustus_Duke_of_Cumberland_and_Teviotdale
    relation: :hasFather
    source: Ernest_Augustus_Crown_Prince_of_Hanover
  AssignClass (9273b9fa-76b0-414b-b4a8-1127fd31d60b)
 Call ID: 9273b9fa-76b0-414b-b4a8-1127fd31d60b
  Args:
    type: :Man
    source: George_III_of_the_United_Kingdom
  AssignClass (b92f4c54-6d94-46c1-94da-3895dde1200b)
 Call ID: b92f4c54-6d94-46c1-94da-3895dde1200b
  Args:
    type: :Person
    source: George_III_of_the_United_Kingdom
  AddTriple (1607b88a-68f3-4f86-9065-fb1e29fbb990)
 Call ID: 1607b88a-68f3-4f86-9065-fb1e29fbb990
  Args:
    relation: :hasFather
    target: George_III_of_the_United_Kingdom
    source: Prince_Ernest_Augustus_Duke_of_Cumberland_and_Teviotdale
  AssignClass (4b4f04a3-fb41-4de3-a663-edd82f3c323b)
 Call ID: 4b4f04a3-fb41-4de3-a663-edd82f3c323b
  Args:
    source: Prince_Ernest_Augustus_son_of_Ernest_Augustus
    type: :Man
  AssignClass (4a0e3cdf-52e8-4b69-a3ff-fdd3e3903ff9)
 Call ID: 4a0e3cdf-52e8-4b69-a3ff-fdd3e3903ff9
  Args:
    source: Prince_Ernest_Augustus_son_of_Ernest_Augustus
    type: :Person
  AddTriple (88cc00c1-1269-47c3-adb7-616ecfb0b6f5)
 Call ID: 88cc00c1-1269-47c3-adb7-616ecfb0b6f5
  Args:
    relation: :hasFather
    target: Ernest_Augustus_Crown_Prince_of_Hanover
    source: Prince_Ernest_Augustus_son_of_Ernest_Augustus
  AssignClass (5252bed3-43ad-4fac-8e91-b580e713185d)
 Call ID: 5252bed3-43ad-4fac-8e91-b580e713185d
  Args:
    type: :Woman
    source: Princess_Victoria_Louise_of_Prussia
  AssignClass (773e082d-68d1-4679-b0b6-febe8a0cb289)
 Call ID: 773e082d-68d1-4679-b0b6-febe8a0cb289
  Args:
    type: :Person
    source: Princess_Victoria_Louise_of_Prussia
  AddLiteral (1c4719a2-d564-4010-a579-dd4c262c49a5)
 Call ID: 1c4719a2-d564-4010-a579-dd4c262c49a5
  Args:
    source: Prince_Ernest_Augustus_son_of_Ernest_Augustus
    relation: :hasMarriageYear
    literal_type: xsd:integer
    literal_value: 1913
  AddTriple (bc26df74-07a8-4b80-b3a3-bcd2d2077d32)
 Call ID: bc26df74-07a8-4b80-b3a3-bcd2d2077d32
  Args:
    source: Prince_Ernest_Augustus_son_of_Ernest_Augustus
    target: Princess_Victoria_Louise_of_Prussia
    relation: :hasRelation
  Finish (bbec411f-ad16-4862-b724-3cefd61126ae)
 Call ID: bbec411f-ad16-4862-b724-3cefd61126ae
  Args: