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
Princess Alexandra of Hanover (Alexandra Louise Marie Olga Elisabeth Therese Vera; 29 September 1882 – 30 August 1963) was Grand Duchess of Mecklenburg-Schwerin as the wife of Grand Duke Frederick Francis IV from their marriage on 7 June 1904 until the Grand Duke abdicated on 14 November 1918, following the German Revolution of 1918.
Alexandra was the daughter of Ernest Augustus, Crown Prince of Hanover, and Princess Thyra of Denmark.
Family

Alexandra was the second eldest daughter and third child of Ernest Augustus, Crown Prince of Hanover (1845–1923) and Princess Thyra of Denmark (1853–1933), the youngest daughter of Christian IX of Denmark (1818–1906) and Louise of Hesse-Kassel (1817–1898).
Alexandra was a great-great-granddaughter of George III of the United Kingdom (1738–1820) and Charlotte of Mecklenburg-Strelitz (1744–1818).
Marriage and issue

Alexandra married on 7 June 1904 in Gmunden, Austria-Hungary to Frederick Francis IV, Grand Duke of Mecklenburg-Schwerin (1882–1945), son of Frederick Francis III, Grand Duke of Mecklenburg-Schwerin and his wife Grand Duchess Anastasia Mikhailovna of Russia.
The bridegroom gave Alexandra a diamond and aquamarine tiara by Faberge.
Alexandra and Frederick Francis had five children:


Grand Duchess of Mecklenburg-Schwerin

In 1913, a fire broke out at Schwerin Castle while the Grand Duke and Duchess were dining there with guests.
Everyone was able to make it out safely, although the grand ducal couple had to apparently rush through flying sparks when making their escape.
Later life

After the Grand Duke's forced abdication in 1918, the family briefly went into exile in Denmark, the native country of Alexandra's mother, Princess Thyra.
After his death in 1945, the widowed Alexandra retired to the Glucksburg family estates in Schleswig-Holstein.



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
  AssignClass (bd54d9fb-ec78-4f28-a6bf-bf8a3f9b4dd4)
 Call ID: bd54d9fb-ec78-4f28-a6bf-bf8a3f9b4dd4
  Args:
    type: :Woman
    source: Alexandra_of_Hanover
  AssignClass (8f45485d-4dab-4c7d-a2c5-2f1967aa204f)
 Call ID: 8f45485d-4dab-4c7d-a2c5-2f1967aa204f
  Args:
    type: :Person
    source: Alexandra_of_Hanover
  AddLiteral (071a9ac3-b9f8-4220-832f-b32e99d80c11)
 Call ID: 071a9ac3-b9f8-4220-832f-b32e99d80c11
  Args:
    source: Alexandra_of_Hanover
    relation: :hasBirthYear
    literal_value: 1882
    literal_type: xsd:integer
  AddLiteral (2fa6d0c1-733b-47f8-bd6e-0849dceb8347)
 Call ID: 2fa6d0c1-733b-47f8-bd6e-0849dceb8347
  Args:
    source: Alexandra_of_Hanover
    relation: :hasDeathYear
    literal_value: 1963
    literal_type: xsd:integer
  AssignClass (a36789ef-a31c-45d1-b32f-df165e13e05f)
 Call ID: a36789ef-a31c-45d1-b32f-df165e13e05f
  Args:
    type: :Man
    source: Ernest_Augustus_Crown_Prince_of_Hanover
  AssignClass (f5d10c4d-5032-4e84-b3a8-c435491f659a)
 Call ID: f5d10c4d-5032-4e84-b3a8-c435491f659a
  Args:
    type: :Person
    source: Ernest_Augustus_Crown_Prince_of_Hanover
  AddLiteral (029fd97e-eb53-4d0f-b603-bccbac1b8acc)
 Call ID: 029fd97e-eb53-4d0f-b603-bccbac1b8acc
  Args:
    literal_value: 1845
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Ernest_Augustus_Crown_Prince_of_Hanover
  AddLiteral (dc915556-920d-464d-aa20-8005eb5a6b26)
 Call ID: dc915556-920d-464d-aa20-8005eb5a6b26
  Args:
    relation: :hasDeathYear
    source: Ernest_Augustus_Crown_Prince_of_Hanover
    literal_value: 1923
    literal_type: xsd:integer
  AssignClass (df567c93-25c0-4ec0-93d1-b62aafbf8101)
 Call ID: df567c93-25c0-4ec0-93d1-b62aafbf8101
  Args:
    type: :Woman
    source: Thyra_of_Denmark
  AssignClass (44bf1dc2-1d6a-48b0-a5cc-8ba34cc9dc1b)
 Call ID: 44bf1dc2-1d6a-48b0-a5cc-8ba34cc9dc1b
  Args:
    type: :Person
    source: Thyra_of_Denmark
  AddLiteral (248a4232-556a-4304-ad2c-02eb958d9eaa)
 Call ID: 248a4232-556a-4304-ad2c-02eb958d9eaa
  Args:
    literal_type: xsd:integer
    literal_value: 1853
    relation: :hasBirthYear
    source: Thyra_of_Denmark
  AddLiteral (13ef464c-fc49-4a78-9b50-f28d89bc465f)
 Call ID: 13ef464c-fc49-4a78-9b50-f28d89bc465f
  Args:
    literal_value: 1933
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: Thyra_of_Denmark
  AddTriple (90fd2368-3e2b-44ad-9bb0-e77bdd6555a7)
 Call ID: 90fd2368-3e2b-44ad-9bb0-e77bdd6555a7
  Args:
    target: Ernest_Augustus_Crown_Prince_of_Hanover
    source: Alexandra_of_Hanover
    relation: :hasFather
  AddTriple (5b8e88e8-dfe6-4a25-a992-9a26158ec312)
 Call ID: 5b8e88e8-dfe6-4a25-a992-9a26158ec312
  Args:
    target: Thyra_of_Denmark
    relation: :hasMother
    source: Alexandra_of_Hanover
  AssignClass (6f39f7ad-7765-41e2-9c02-36b987ff789a)
 Call ID: 6f39f7ad-7765-41e2-9c02-36b987ff789a
  Args:
    type: :Man
    source: Christian_IX_of_Denmark
  AssignClass (10b692a0-082f-416e-9d01-4879c78e05e8)
 Call ID: 10b692a0-082f-416e-9d01-4879c78e05e8
  Args:
    type: :Person
    source: Christian_IX_of_Denmark
  AddLiteral (b7fb2fa9-f71e-421c-beda-531f5f5e0880)
 Call ID: b7fb2fa9-f71e-421c-beda-531f5f5e0880
  Args:
    literal_value: 1818
    literal_type: xsd:integer
    source: Christian_IX_of_Denmark
    relation: :hasBirthYear
  AddLiteral (e8dae118-145c-4a42-b988-3083f66f7a8e)
 Call ID: e8dae118-145c-4a42-b988-3083f66f7a8e
  Args:
    relation: :hasDeathYear
    source: Christian_IX_of_Denmark
    literal_type: xsd:integer
    literal_value: 1906
  AssignClass (f65dfb42-3f1f-4253-a911-b6e4dab5f5bf)
 Call ID: f65dfb42-3f1f-4253-a911-b6e4dab5f5bf
  Args:
    type: :Woman
    source: Louise_of_Hesse_Kassel
  AssignClass (07a374f2-7170-4886-a04f-493ad6a699f5)
 Call ID: 07a374f2-7170-4886-a04f-493ad6a699f5
  Args:
    type: :Person
    source: Louise_of_Hesse_Kassel
  AddLiteral (1d18ae16-5568-41bc-9727-1c50a7075877)
 Call ID: 1d18ae16-5568-41bc-9727-1c50a7075877
  Args:
    source: Louise_of_Hesse_Kassel
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1817
  AddLiteral (f73ee078-8c22-4241-bc79-6025581b7799)
 Call ID: f73ee078-8c22-4241-bc79-6025581b7799
  Args:
    literal_type: xsd:integer
    literal_value: 1898
    source: Louise_of_Hesse_Kassel
    relation: :hasDeathYear
  AddTriple (18ec1792-4a78-4bc6-aa9a-1c020c124fe5)
 Call ID: 18ec1792-4a78-4bc6-aa9a-1c020c124fe5
  Args:
    target: Christian_IX_of_Denmark
    source: Thyra_of_Denmark
    relation: :hasFather
  AddTriple (34d518dc-77d3-4ad6-91a1-6ae4ecd70b01)
 Call ID: 34d518dc-77d3-4ad6-91a1-6ae4ecd70b01
  Args:
    relation: :hasMother
    source: Thyra_of_Denmark
    target: Louise_of_Hesse_Kassel
  AssignClass (375aba82-2b49-4ebc-92b5-08c47e65a244)
 Call ID: 375aba82-2b49-4ebc-92b5-08c47e65a244
  Args:
    type: :Man
    source: George_III_of_the_United_Kingdom
  AssignClass (717c414b-323b-4f61-bd4f-abc18ed5fbd0)
 Call ID: 717c414b-323b-4f61-bd4f-abc18ed5fbd0
  Args:
    type: :Person
    source: George_III_of_the_United_Kingdom
  AddLiteral (2ed766c5-6087-49e2-aa95-1a85e6162d17)
 Call ID: 2ed766c5-6087-49e2-aa95-1a85e6162d17
  Args:
    source: George_III_of_the_United_Kingdom
    relation: :hasBirthYear
    literal_value: 1738
    literal_type: xsd:integer
  AddLiteral (4b0011fb-19da-41fd-ae1a-0158a3b5f66f)
 Call ID: 4b0011fb-19da-41fd-ae1a-0158a3b5f66f
  Args:
    literal_value: 1820
    literal_type: xsd:integer
    source: George_III_of_the_United_Kingdom
    relation: :hasDeathYear
  AssignClass (b62cd6b4-5ac0-4161-8d98-d071f953a0b8)
 Call ID: b62cd6b4-5ac0-4161-8d98-d071f953a0b8
  Args:
    type: :Woman
    source: Charlotte_of_Mecklenburg_Strelitz
  AssignClass (0550739d-17f7-45cc-8385-2992667b4e1e)
 Call ID: 0550739d-17f7-45cc-8385-2992667b4e1e
  Args:
    type: :Person
    source: Charlotte_of_Mecklenburg_Strelitz
  AddLiteral (7ca16f89-6ff1-4c76-a580-02092151dbac)
 Call ID: 7ca16f89-6ff1-4c76-a580-02092151dbac
  Args:
    literal_type: xsd:integer
    literal_value: 1744
    relation: :hasBirthYear
    source: Charlotte_of_Mecklenburg_Strelitz
  AddLiteral (71735150-fd7e-4a44-9609-c8f916585240)
 Call ID: 71735150-fd7e-4a44-9609-c8f916585240
  Args:
    source: Charlotte_of_Mecklenburg_Strelitz
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 1818
  AssignClass (0139fa0c-aa18-40fd-b801-baedb505728d)
 Call ID: 0139fa0c-aa18-40fd-b801-baedb505728d
  Args:
    type: :Man
    source: Frederick_Francis_IV_Grand_Duke_of_Mecklenburg_Schwerin
  AssignClass (9b68ce2f-9fef-40c1-b1ff-2f4a99e81a67)
 Call ID: 9b68ce2f-9fef-40c1-b1ff-2f4a99e81a67
  Args:
    type: :Person
    source: Frederick_Francis_IV_Grand_Duke_of_Mecklenburg_Schwerin
  AddLiteral (3838fe27-5965-47db-86ec-54b789101bff)
 Call ID: 3838fe27-5965-47db-86ec-54b789101bff
  Args:
    source: Frederick_Francis_IV_Grand_Duke_of_Mecklenburg_Schwerin
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1882
  AddLiteral (0f3f6ef1-e199-4dd4-8d0b-9801bbc80398)
 Call ID: 0f3f6ef1-e199-4dd4-8d0b-9801bbc80398
  Args:
    literal_type: xsd:integer
    literal_value: 1945
    relation: :hasDeathYear
    source: Frederick_Francis_IV_Grand_Duke_of_Mecklenburg_Schwerin
  AddLiteral (ca29e294-73f8-4511-b3a6-76e50cab1745)
 Call ID: ca29e294-73f8-4511-b3a6-76e50cab1745
  Args:
    source: Alexandra_of_Hanover
    relation: :hasMarriageYear
    literal_type: xsd:integer
    literal_value: 1904
  AddTriple (2137bca5-ef72-4d9f-834a-0a23213b2fe3)
 Call ID: 2137bca5-ef72-4d9f-834a-0a23213b2fe3
  Args:
    source: Alexandra_of_Hanover
    relation: :hasRelation
    target: Frederick_Francis_IV_Grand_Duke_of_Mecklenburg_Schwerin
  AssignClass (2f9e5950-24ec-4ab1-ae14-c2b5ceeedd72)
 Call ID: 2f9e5950-24ec-4ab1-ae14-c2b5ceeedd72
  Args:
    type: :Man
    source: Frederick_Francis_III_Grand_Duke_of_Mecklenburg_Schwerin
  AssignClass (9f647fe6-f595-457c-93d0-272d7f058a51)
 Call ID: 9f647fe6-f595-457c-93d0-272d7f058a51
  Args:
    type: :Person
    source: Frederick_Francis_III_Grand_Duke_of_Mecklenburg_Schwerin
  AssignClass (0c956161-1b01-4821-89ac-e0053a5bfb80)
 Call ID: 0c956161-1b01-4821-89ac-e0053a5bfb80
  Args:
    type: :Woman
    source: Anastasia_Mikhailovna_of_Russia
  AssignClass (1079896e-7321-4789-a381-c05887db5760)
 Call ID: 1079896e-7321-4789-a381-c05887db5760
  Args:
    type: :Person
    source: Anastasia_Mikhailovna_of_Russia
  AddTriple (88a251b4-561a-4e20-b1a1-433afcd70011)
 Call ID: 88a251b4-561a-4e20-b1a1-433afcd70011
  Args:
    relation: :hasFather
    source: Frederick_Francis_IV_Grand_Duke_of_Mecklenburg_Schwerin
    target: Frederick_Francis_III_Grand_Duke_of_Mecklenburg_Schwerin
  AddTriple (24867da0-ffa9-4b69-8a03-df69860cc6a4)
 Call ID: 24867da0-ffa9-4b69-8a03-df69860cc6a4
  Args:
    relation: :hasMother
    source: Frederick_Francis_IV_Grand_Duke_of_Mecklenburg_Schwerin
    target: Anastasia_Mikhailovna_of_Russia
  Finish (2fed84cd-513a-405d-aef6-1c387c58a8fb)
 Call ID: 2fed84cd-513a-405d-aef6-1c387c58a8fb
  Args: