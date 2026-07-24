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
  AssignClass (2ef04886-a4b6-415e-abc9-1c8b9fbc7596)
 Call ID: 2ef04886-a4b6-415e-abc9-1c8b9fbc7596
  Args:
    source: :Alexandra_of_Hanover
    type: :Woman
  AssignClass (c181844e-5519-4c42-bedc-b3cc49a8e579)
 Call ID: c181844e-5519-4c42-bedc-b3cc49a8e579
  Args:
    source: :Alexandra_of_Hanover
    type: :Person
  AddLiteral (6eb7b21a-566d-4214-9dba-5f025cadb878)
 Call ID: 6eb7b21a-566d-4214-9dba-5f025cadb878
  Args:
    relation: :hasBirthYear
    literal_value: 1882
    literal_type: xsd:integer
    source: :Alexandra_of_Hanover
  AddLiteral (0a57d57d-b300-49d0-87a4-dca1f5dc344e)
 Call ID: 0a57d57d-b300-49d0-87a4-dca1f5dc344e
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: :Alexandra_of_Hanover
    literal_value: 1963
  AssignClass (76c1c3af-4de8-4d8e-8543-d751facd88c5)
 Call ID: 76c1c3af-4de8-4d8e-8543-d751facd88c5
  Args:
    type: :Man
    source: :Ernest_Augustus_Crown_Prince_of_Hanover
  AssignClass (1a49b187-c0b9-43ce-a5ac-68c8e530a6a6)
 Call ID: 1a49b187-c0b9-43ce-a5ac-68c8e530a6a6
  Args:
    type: :Person
    source: :Ernest_Augustus_Crown_Prince_of_Hanover
  AddLiteral (f1188eba-7879-49fa-ba0d-3ef3645856c4)
 Call ID: f1188eba-7879-49fa-ba0d-3ef3645856c4
  Args:
    literal_value: 1845
    source: :Ernest_Augustus_Crown_Prince_of_Hanover
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (4691a662-5992-4408-874f-edab39dc5b51)
 Call ID: 4691a662-5992-4408-874f-edab39dc5b51
  Args:
    relation: :hasDeathYear
    source: :Ernest_Augustus_Crown_Prince_of_Hanover
    literal_type: xsd:integer
    literal_value: 1923
  AssignClass (501c0b28-8496-4f6b-96e4-defd0dc139a0)
 Call ID: 501c0b28-8496-4f6b-96e4-defd0dc139a0
  Args:
    type: :Woman
    source: :Thyra_of_Denmark
  AssignClass (7479cb5f-5afc-4ed5-9dec-0e23684ced45)
 Call ID: 7479cb5f-5afc-4ed5-9dec-0e23684ced45
  Args:
    source: :Thyra_of_Denmark
    type: :Person
  AddLiteral (d091424c-ce9e-4447-95c0-8d97b112413a)
 Call ID: d091424c-ce9e-4447-95c0-8d97b112413a
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: :Thyra_of_Denmark
    literal_value: 1853
  AddLiteral (c36e7e37-d305-45ea-9e2c-2171b3a22044)
 Call ID: c36e7e37-d305-45ea-9e2c-2171b3a22044
  Args:
    literal_value: 1933
    literal_type: xsd:integer
    source: :Thyra_of_Denmark
    relation: :hasDeathYear
  AddTriple (4ff882dc-12e4-4478-9acf-127d04b690e9)
 Call ID: 4ff882dc-12e4-4478-9acf-127d04b690e9
  Args:
    relation: :hasFather
    target: :Ernest_Augustus_Crown_Prince_of_Hanover
    source: :Alexandra_of_Hanover
  AddTriple (377fffe7-6213-4dd0-a970-a7e5d6364ede)
 Call ID: 377fffe7-6213-4dd0-a970-a7e5d6364ede
  Args:
    relation: :hasMother
    source: :Alexandra_of_Hanover
    target: :Thyra_of_Denmark
  AssignClass (3a0b2c7c-fed6-4c90-a876-bf2aaaf86d52)
 Call ID: 3a0b2c7c-fed6-4c90-a876-bf2aaaf86d52
  Args:
    source: :Frederick_Francis_IV_Grand_Duke_of_Mecklenburg_Schwerin
    type: :Man
  AssignClass (55d03fb5-5025-41d7-bd80-f135420e3ad4)
 Call ID: 55d03fb5-5025-41d7-bd80-f135420e3ad4
  Args:
    type: :Person
    source: :Frederick_Francis_IV_Grand_Duke_of_Mecklenburg_Schwerin
  AddLiteral (2bf8bae1-e035-47ac-a9a2-a6afe94865be)
 Call ID: 2bf8bae1-e035-47ac-a9a2-a6afe94865be
  Args:
    literal_type: xsd:integer
    source: :Frederick_Francis_IV_Grand_Duke_of_Mecklenburg_Schwerin
    literal_value: 1882
    relation: :hasBirthYear
  AddLiteral (28054cf4-7789-4360-8d70-ef71b0c9f8f0)
 Call ID: 28054cf4-7789-4360-8d70-ef71b0c9f8f0
  Args:
    literal_value: 1945
    literal_type: xsd:integer
    source: :Frederick_Francis_IV_Grand_Duke_of_Mecklenburg_Schwerin
    relation: :hasDeathYear
  AddLiteral (ee53fdda-6329-49c8-b322-9cc5e87b4cff)
 Call ID: ee53fdda-6329-49c8-b322-9cc5e87b4cff
  Args:
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: :Alexandra_of_Hanover
    literal_value: 1904
  AssignClass (d8ad8d7f-a69c-4b98-8839-ac70ba555ae5)
 Call ID: d8ad8d7f-a69c-4b98-8839-ac70ba555ae5
  Args:
    source: :Christian_IX_of_Denmark
    type: :Man
  AssignClass (85e1008b-0c24-4158-9872-29b43b3c3511)
 Call ID: 85e1008b-0c24-4158-9872-29b43b3c3511
  Args:
    type: :Person
    source: :Christian_IX_of_Denmark
  AddLiteral (0d079bc5-b987-4f95-a12a-3a6ea5c30b11)
 Call ID: 0d079bc5-b987-4f95-a12a-3a6ea5c30b11
  Args:
    literal_value: 1818
    source: :Christian_IX_of_Denmark
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (e3765b1e-854c-4489-86ae-53b9f65e9fd9)
 Call ID: e3765b1e-854c-4489-86ae-53b9f65e9fd9
  Args:
    source: :Christian_IX_of_Denmark
    literal_type: xsd:integer
    literal_value: 1906
    relation: :hasDeathYear
  AssignClass (1cd17411-22e8-4deb-8700-72866fbfd248)
 Call ID: 1cd17411-22e8-4deb-8700-72866fbfd248
  Args:
    source: :Louise_of_Hesse_Kassel
    type: :Woman
  AssignClass (c616695c-f221-4681-90a8-aaff99f156f4)
 Call ID: c616695c-f221-4681-90a8-aaff99f156f4
  Args:
    type: :Person
    source: :Louise_of_Hesse_Kassel
  AddLiteral (b857f379-c5b3-4721-8faa-cb9db843f1b6)
 Call ID: b857f379-c5b3-4721-8faa-cb9db843f1b6
  Args:
    relation: :hasBirthYear
    literal_value: 1817
    source: :Louise_of_Hesse_Kassel
    literal_type: xsd:integer
  AddLiteral (ac50cf43-f503-4d67-b7d8-041ee49072ae)
 Call ID: ac50cf43-f503-4d67-b7d8-041ee49072ae
  Args:
    source: :Louise_of_Hesse_Kassel
    literal_type: xsd:integer
    literal_value: 1898
    relation: :hasDeathYear
  AddTriple (9c84a810-b9da-4b2c-8c5e-ac76cae8b08e)
 Call ID: 9c84a810-b9da-4b2c-8c5e-ac76cae8b08e
  Args:
    source: :Thyra_of_Denmark
    target: :Christian_IX_of_Denmark
    relation: :hasFather
  AddTriple (aca9753a-167e-4149-a46c-3c3240078bdf)
 Call ID: aca9753a-167e-4149-a46c-3c3240078bdf
  Args:
    source: :Thyra_of_Denmark
    target: :Louise_of_Hesse_Kassel
    relation: :hasMother
  AssignClass (6c5e2ccd-0cde-4d00-aedd-c1f78dde3213)
 Call ID: 6c5e2ccd-0cde-4d00-aedd-c1f78dde3213
  Args:
    source: :George_III_of_the_United_Kingdom
    type: :Man
  AssignClass (c564c71c-1d2c-4722-b681-2e9f2aaeff31)
 Call ID: c564c71c-1d2c-4722-b681-2e9f2aaeff31
  Args:
    type: :Person
    source: :George_III_of_the_United_Kingdom
  AddLiteral (cd20a432-4798-43c7-9b25-9983c86e1007)
 Call ID: cd20a432-4798-43c7-9b25-9983c86e1007
  Args:
    relation: :hasBirthYear
    literal_value: 1738
    literal_type: xsd:integer
    source: :George_III_of_the_United_Kingdom
  AddLiteral (7afadfd2-8d7b-4f82-8b63-0d68f19d1b88)
 Call ID: 7afadfd2-8d7b-4f82-8b63-0d68f19d1b88
  Args:
    source: :George_III_of_the_United_Kingdom
    literal_type: xsd:integer
    literal_value: 1820
    relation: :hasDeathYear
  AssignClass (13c0ef23-7307-4d28-8ec1-2e88d4402d97)
 Call ID: 13c0ef23-7307-4d28-8ec1-2e88d4402d97
  Args:
    type: :Woman
    source: :Charlotte_of_Mecklenburg_Strelitz
  AssignClass (7a64fb37-e040-4584-b020-564ee1129167)
 Call ID: 7a64fb37-e040-4584-b020-564ee1129167
  Args:
    source: :Charlotte_of_Mecklenburg_Strelitz
    type: :Person
  AddLiteral (f244c45c-4e60-4a2b-8e3a-555a69d0b1b3)
 Call ID: f244c45c-4e60-4a2b-8e3a-555a69d0b1b3
  Args:
    source: :Charlotte_of_Mecklenburg_Strelitz
    literal_type: xsd:integer
    literal_value: 1744
    relation: :hasBirthYear
  AddLiteral (8ac19800-2bed-4124-b5ef-e65573d2ffd9)
 Call ID: 8ac19800-2bed-4124-b5ef-e65573d2ffd9
  Args:
    relation: :hasDeathYear
    source: :Charlotte_of_Mecklenburg_Strelitz
    literal_type: xsd:integer
    literal_value: 1818
  AssignClass (3ea9cce4-6788-4019-9967-ad61db65a3c3)
 Call ID: 3ea9cce4-6788-4019-9967-ad61db65a3c3
  Args:
    type: :Man
    source: :Frederick_Francis_III_Grand_Duke_of_Mecklenburg_Schwerin
  AssignClass (85bcf39c-49e4-47eb-a71d-478df7dd2ae4)
 Call ID: 85bcf39c-49e4-47eb-a71d-478df7dd2ae4
  Args:
    type: :Person
    source: :Frederick_Francis_III_Grand_Duke_of_Mecklenburg_Schwerin
  AssignClass (3a0eb231-8c84-4ca5-bbc7-4de58f755f63)
 Call ID: 3a0eb231-8c84-4ca5-bbc7-4de58f755f63
  Args:
    type: :Woman
    source: :Anastasia_Mikhailovna_of_Russia
  AssignClass (4f2a2974-dae3-40bb-ae73-989f1d26f692)
 Call ID: 4f2a2974-dae3-40bb-ae73-989f1d26f692
  Args:
    source: :Anastasia_Mikhailovna_of_Russia
    type: :Person
  AddTriple (35d111cc-6f2e-4bde-a4c2-87a0840bf177)
 Call ID: 35d111cc-6f2e-4bde-a4c2-87a0840bf177
  Args:
    target: :Frederick_Francis_III_Grand_Duke_of_Mecklenburg_Schwerin
    source: :Frederick_Francis_IV_Grand_Duke_of_Mecklenburg_Schwerin
    relation: :hasFather
  AddTriple (489a19ac-3fef-4ec9-9892-6250fa6fb6dd)
 Call ID: 489a19ac-3fef-4ec9-9892-6250fa6fb6dd
  Args:
    source: :Frederick_Francis_IV_Grand_Duke_of_Mecklenburg_Schwerin
    target: :Anastasia_Mikhailovna_of_Russia
    relation: :hasMother
  Finish (577c3164-6d57-4ec4-80f5-9153d5f96110)
 Call ID: 577c3164-6d57-4ec4-80f5-9153d5f96110
  Args: