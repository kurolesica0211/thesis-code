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
  AssignClass (281118a2-da92-47fd-b761-f8d9a997b631)
 Call ID: 281118a2-da92-47fd-b761-f8d9a997b631
  Args:
    source: George_William
    type: :Man
  AssignClass (01e12a53-c085-4a24-9963-d41e6fabd253)
 Call ID: 01e12a53-c085-4a24-9963-d41e6fabd253
  Args:
    type: :Person
    source: George_William
  AddLiteral (5d94a3e0-b103-48f2-978c-a3b5200ab1d3)
 Call ID: 5d94a3e0-b103-48f2-978c-a3b5200ab1d3
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: George_William
    literal_value: 1880
  AddLiteral (50d3804d-b7db-4c5a-9dbf-91895cd23001)
 Call ID: 50d3804d-b7db-4c5a-9dbf-91895cd23001
  Args:
    literal_value: 1912
    source: George_William
    literal_type: xsd:integer
    relation: :hasDeathYear
  AssignClass (ac79194a-dfcd-4041-9dac-b5ccea9e655c)
 Call ID: ac79194a-dfcd-4041-9dac-b5ccea9e655c
  Args:
    type: :Man
    source: Ernest_Augustus_Crown_Prince_of_Hanover
  AssignClass (ddd925e7-8b9d-4301-8e47-9977051013cb)
 Call ID: ddd925e7-8b9d-4301-8e47-9977051013cb
  Args:
    source: Ernest_Augustus_Crown_Prince_of_Hanover
    type: :Person
  AssignClass (1c5ffeb5-b58d-4aca-9dd7-0b5d8869ef8d)
 Call ID: 1c5ffeb5-b58d-4aca-9dd7-0b5d8869ef8d
  Args:
    source: Thyra_of_Denmark
    type: :Woman
  AssignClass (d8da098d-4f87-4272-b9a1-efdbca7594cf)
 Call ID: d8da098d-4f87-4272-b9a1-efdbca7594cf
  Args:
    source: Thyra_of_Denmark
    type: :Person
  AddTriple (8b00efed-61f8-4539-bd86-8a893d337de5)
 Call ID: 8b00efed-61f8-4539-bd86-8a893d337de5
  Args:
    relation: :hasFather
    target: Ernest_Augustus_Crown_Prince_of_Hanover
    source: George_William
  AddTriple (87677997-c17f-4005-ab60-802520e1fcdb)
 Call ID: 87677997-c17f-4005-ab60-802520e1fcdb
  Args:
    target: Thyra_of_Denmark
    source: George_William
    relation: :hasMother
  AssignClass (1695e451-798c-4c5d-89fe-a0ad4eeebaaf)
 Call ID: 1695e451-798c-4c5d-89fe-a0ad4eeebaaf
  Args:
    source: George_V_of_Hanover
    type: :Man
  AssignClass (2abf2c73-ee50-415e-a510-960a80b1f069)
 Call ID: 2abf2c73-ee50-415e-a510-960a80b1f069
  Args:
    source: George_V_of_Hanover
    type: :Person
  AddTriple (baba7b3b-2616-48e4-8a5f-f8191e8d46fc)
 Call ID: baba7b3b-2616-48e4-8a5f-f8191e8d46fc
  Args:
    relation: :hasFather
    source: Ernest_Augustus_Crown_Prince_of_Hanover
    target: George_V_of_Hanover
  AssignClass (4c4a9670-12f6-4d91-b910-baac6784fd07)
 Call ID: 4c4a9670-12f6-4d91-b910-baac6784fd07
  Args:
    source: Christian_IX_of_Denmark
    type: :Man
  AssignClass (d7bb139a-685e-4ffa-b99a-d60663b7033e)
 Call ID: d7bb139a-685e-4ffa-b99a-d60663b7033e
  Args:
    source: Christian_IX_of_Denmark
    type: :Person
  AddTriple (1bd6d434-0cab-4196-8642-79c8e8000ef3)
 Call ID: 1bd6d434-0cab-4196-8642-79c8e8000ef3
  Args:
    target: Christian_IX_of_Denmark
    source: Thyra_of_Denmark
    relation: :hasFather
  AssignClass (20a8263c-3338-4af1-a004-2e2a0ddce5c5)
 Call ID: 20a8263c-3338-4af1-a004-2e2a0ddce5c5
  Args:
    type: :Man
    source: Prince_Ernest_Augustus_Duke_of_Cumberland_and_Teviotdale
  AssignClass (dd2bada4-d477-474d-9fc4-3fc3f3f12800)
 Call ID: dd2bada4-d477-474d-9fc4-3fc3f3f12800
  Args:
    type: :Person
    source: Prince_Ernest_Augustus_Duke_of_Cumberland_and_Teviotdale
  AssignClass (6ab490ec-6faa-4bd4-9f6e-3ecfd7c25b36)
 Call ID: 6ab490ec-6faa-4bd4-9f6e-3ecfd7c25b36
  Args:
    type: :Man
    source: George_III_of_the_United_Kingdom
  AssignClass (2dfad74d-fe60-4d6c-83d4-ea0a5b09de86)
 Call ID: 2dfad74d-fe60-4d6c-83d4-ea0a5b09de86
  Args:
    source: George_III_of_the_United_Kingdom
    type: :Person
  AddTriple (86224c08-7f51-49a8-9e34-665ae23ca31d)
 Call ID: 86224c08-7f51-49a8-9e34-665ae23ca31d
  Args:
    target: George_III_of_the_United_Kingdom
    source: Prince_Ernest_Augustus_Duke_of_Cumberland_and_Teviotdale
    relation: :hasFather
  AssignClass (0be803bf-5b1a-432a-aa99-19b8f07b35bf)
 Call ID: 0be803bf-5b1a-432a-aa99-19b8f07b35bf
  Args:
    type: :Man
    source: Prince_Ernest_Augustus_the_Younger
  AssignClass (7768f847-1e2d-46ac-bdd9-d2a542c22fbe)
 Call ID: 7768f847-1e2d-46ac-bdd9-d2a542c22fbe
  Args:
    type: :Person
    source: Prince_Ernest_Augustus_the_Younger
  AddTriple (1270dec1-5f9b-4f9f-a097-bd57f42de1ab)
 Call ID: 1270dec1-5f9b-4f9f-a097-bd57f42de1ab
  Args:
    source: Prince_Ernest_Augustus_the_Younger
    target: Ernest_Augustus_Crown_Prince_of_Hanover
    relation: :hasFather
  AssignClass (821110f6-b902-4588-a566-6892eeb8dd35)
 Call ID: 821110f6-b902-4588-a566-6892eeb8dd35
  Args:
    source: Princess_Victoria_Louise_of_Prussia
    type: :Woman
  AssignClass (ebc1ab7d-c02f-4aa5-af60-9ed9ea421c6b)
 Call ID: ebc1ab7d-c02f-4aa5-af60-9ed9ea421c6b
  Args:
    type: :Person
    source: Princess_Victoria_Louise_of_Prussia
  AddLiteral (f4ea3bde-1209-441b-b0b5-0cd25b0d65e7)
 Call ID: f4ea3bde-1209-441b-b0b5-0cd25b0d65e7
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    source: Prince_Ernest_Augustus_the_Younger
    literal_value: 1913
  AddTriple (3253b440-b43d-4dbc-858a-bf515a43e5cb)
 Call ID: 3253b440-b43d-4dbc-858a-bf515a43e5cb
  Args:
    source: Prince_Ernest_Augustus_the_Younger
    target: Princess_Victoria_Louise_of_Prussia
    relation: :hasRelation
  AssignClass (b3e2eb6d-6284-4068-91ff-c2af8707b1f4)
 Call ID: b3e2eb6d-6284-4068-91ff-c2af8707b1f4
  Args:
    source: Frederick_VIII_of_Denmark
    type: :Man
  AssignClass (a49cf90c-0553-43b6-97a0-1dbbfdbf5dc5)
 Call ID: a49cf90c-0553-43b6-97a0-1dbbfdbf5dc5
  Args:
    source: Frederick_VIII_of_Denmark
    type: :Person
  Finish (ceffa7aa-72d7-47a3-8cc3-60515e3a647e)
 Call ID: ceffa7aa-72d7-47a3-8cc3-60515e3a647e
  Args: