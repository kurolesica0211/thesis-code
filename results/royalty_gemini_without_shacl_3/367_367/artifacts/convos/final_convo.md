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
  AssignClass (1d3b792e-9769-41fc-9a18-2eb78cc0ac0d)
 Call ID: 1d3b792e-9769-41fc-9a18-2eb78cc0ac0d
  Args:
    type: :Woman
    source: :Alexandra_of_Hanover
  AssignClass (a67b9183-c1d4-4307-b7c7-e24e9e7f5d5b)
 Call ID: a67b9183-c1d4-4307-b7c7-e24e9e7f5d5b
  Args:
    source: :Alexandra_of_Hanover
    type: :Person
  AddLiteral (6c7e81d7-d61f-420a-9511-43de2376b348)
 Call ID: 6c7e81d7-d61f-420a-9511-43de2376b348
  Args:
    literal_type: xsd:integer
    source: :Alexandra_of_Hanover
    literal_value: 1882
    relation: :hasBirthYear
  AddLiteral (bc306204-1aed-4029-a338-b88093c3e782)
 Call ID: bc306204-1aed-4029-a338-b88093c3e782
  Args:
    literal_type: xsd:integer
    source: :Alexandra_of_Hanover
    relation: :hasDeathYear
    literal_value: 1963
  AssignClass (887f73d2-fefc-4dba-8e72-61b355bdcaf2)
 Call ID: 887f73d2-fefc-4dba-8e72-61b355bdcaf2
  Args:
    source: :Ernest_Augustus_Crown_Prince_of_Hanover
    type: :Man
  AssignClass (8c4aad95-04c5-4767-ad63-e18839354758)
 Call ID: 8c4aad95-04c5-4767-ad63-e18839354758
  Args:
    source: :Ernest_Augustus_Crown_Prince_of_Hanover
    type: :Person
  AddLiteral (26129c80-1087-4f16-b2ea-f2a906a29329)
 Call ID: 26129c80-1087-4f16-b2ea-f2a906a29329
  Args:
    literal_value: 1845
    relation: :hasBirthYear
    source: :Ernest_Augustus_Crown_Prince_of_Hanover
    literal_type: xsd:integer
  AddLiteral (e1773cd7-cfa4-44c2-8ba4-932d6e92fc7a)
 Call ID: e1773cd7-cfa4-44c2-8ba4-932d6e92fc7a
  Args:
    literal_type: xsd:integer
    source: :Ernest_Augustus_Crown_Prince_of_Hanover
    literal_value: 1923
    relation: :hasDeathYear
  AssignClass (8dadf397-6f67-4075-8deb-2039bec404d5)
 Call ID: 8dadf397-6f67-4075-8deb-2039bec404d5
  Args:
    type: :Woman
    source: :Thyra_of_Denmark
  AssignClass (cc90e353-07d3-4051-b0da-dfbec760fcb2)
 Call ID: cc90e353-07d3-4051-b0da-dfbec760fcb2
  Args:
    type: :Person
    source: :Thyra_of_Denmark
  AddLiteral (562262c8-0f21-4d97-942f-16e186b8f06f)
 Call ID: 562262c8-0f21-4d97-942f-16e186b8f06f
  Args:
    literal_type: xsd:integer
    source: :Thyra_of_Denmark
    relation: :hasBirthYear
    literal_value: 1853
  AddLiteral (7429bdb6-d4c1-448f-82f1-04c90da2697a)
 Call ID: 7429bdb6-d4c1-448f-82f1-04c90da2697a
  Args:
    relation: :hasDeathYear
    literal_value: 1933
    source: :Thyra_of_Denmark
    literal_type: xsd:integer
  AddTriple (7a1efba6-bcee-4096-86a4-6c875f11a328)
 Call ID: 7a1efba6-bcee-4096-86a4-6c875f11a328
  Args:
    source: :Alexandra_of_Hanover
    relation: :hasFather
    target: :Ernest_Augustus_Crown_Prince_of_Hanover
  AddTriple (8f96b971-765b-4b28-9447-4684c8ce91f2)
 Call ID: 8f96b971-765b-4b28-9447-4684c8ce91f2
  Args:
    source: :Alexandra_of_Hanover
    target: :Thyra_of_Denmark
    relation: :hasMother
  AssignClass (e9863907-e605-4eca-87ac-af0469cafc14)
 Call ID: e9863907-e605-4eca-87ac-af0469cafc14
  Args:
    type: :Man
    source: :Frederick_Francis_IV_Grand_Duke_of_Mecklenburg_Schwerin
  AssignClass (749941a9-783f-477d-b3d2-5a4164f1b6a6)
 Call ID: 749941a9-783f-477d-b3d2-5a4164f1b6a6
  Args:
    type: :Person
    source: :Frederick_Francis_IV_Grand_Duke_of_Mecklenburg_Schwerin
  AddLiteral (c967fb57-4fe5-4820-bba9-6ebdc8827cd7)
 Call ID: c967fb57-4fe5-4820-bba9-6ebdc8827cd7
  Args:
    source: :Frederick_Francis_IV_Grand_Duke_of_Mecklenburg_Schwerin
    literal_type: xsd:integer
    literal_value: 1882
    relation: :hasBirthYear
  AddLiteral (47aa6fce-8dc9-442f-a6b0-8053cd693ddf)
 Call ID: 47aa6fce-8dc9-442f-a6b0-8053cd693ddf
  Args:
    literal_type: xsd:integer
    source: :Frederick_Francis_IV_Grand_Duke_of_Mecklenburg_Schwerin
    literal_value: 1945
    relation: :hasDeathYear
  AddLiteral (09468afc-51a3-4893-90a4-dd998f883bfb)
 Call ID: 09468afc-51a3-4893-90a4-dd998f883bfb
  Args:
    relation: :hasMarriageYear
    literal_value: 1904
    source: :Alexandra_of_Hanover
    literal_type: xsd:integer
  AddTriple (eedf8417-3d37-4a5b-bf6c-f4db035c1fab)
 Call ID: eedf8417-3d37-4a5b-bf6c-f4db035c1fab
  Args:
    source: :Alexandra_of_Hanover
    relation: :hasRelation
    target: :Frederick_Francis_IV_Grand_Duke_of_Mecklenburg_Schwerin
  AssignClass (3af2280b-7d9f-45ee-a88e-31a843154204)
 Call ID: 3af2280b-7d9f-45ee-a88e-31a843154204
  Args:
    type: :Man
    source: :Christian_IX_of_Denmark
  AssignClass (43241431-cdd6-42d3-a0a3-494741db4e15)
 Call ID: 43241431-cdd6-42d3-a0a3-494741db4e15
  Args:
    source: :Christian_IX_of_Denmark
    type: :Person
  AddLiteral (dfa6f718-ab58-400b-84e2-cb124a805eaf)
 Call ID: dfa6f718-ab58-400b-84e2-cb124a805eaf
  Args:
    literal_type: xsd:integer
    source: :Christian_IX_of_Denmark
    literal_value: 1818
    relation: :hasBirthYear
  AddLiteral (4c14e090-de95-49db-ba67-df291d0987c8)
 Call ID: 4c14e090-de95-49db-ba67-df291d0987c8
  Args:
    source: :Christian_IX_of_Denmark
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1906
  AssignClass (3ac8cb97-2b6e-4596-aa04-d17c49a112a4)
 Call ID: 3ac8cb97-2b6e-4596-aa04-d17c49a112a4
  Args:
    type: :Woman
    source: :Louise_of_Hesse_Kassel
  AssignClass (1f134189-df52-47b4-8785-e999e2e7d8db)
 Call ID: 1f134189-df52-47b4-8785-e999e2e7d8db
  Args:
    source: :Louise_of_Hesse_Kassel
    type: :Person
  AddLiteral (0cc65359-5b45-45bf-9591-4ad7fab95c91)
 Call ID: 0cc65359-5b45-45bf-9591-4ad7fab95c91
  Args:
    literal_value: 1817
    relation: :hasBirthYear
    source: :Louise_of_Hesse_Kassel
    literal_type: xsd:integer
  AddLiteral (f957651e-17f7-4cb4-aa10-a803f280a625)
 Call ID: f957651e-17f7-4cb4-aa10-a803f280a625
  Args:
    source: :Louise_of_Hesse_Kassel
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1898
  AddTriple (0e0341f3-9e1a-41a4-a059-9b9fda0ca555)
 Call ID: 0e0341f3-9e1a-41a4-a059-9b9fda0ca555
  Args:
    source: :Thyra_of_Denmark
    target: :Christian_IX_of_Denmark
    relation: :hasFather
  AddTriple (596b0fbd-3863-47b1-a9ce-0a6c39625e52)
 Call ID: 596b0fbd-3863-47b1-a9ce-0a6c39625e52
  Args:
    source: :Thyra_of_Denmark
    relation: :hasMother
    target: :Louise_of_Hesse_Kassel
  AssignClass (1b8a877c-8221-4637-afee-58382c7e15be)
 Call ID: 1b8a877c-8221-4637-afee-58382c7e15be
  Args:
    type: :Man
    source: :George_III_of_the_United_Kingdom
  AssignClass (4f3b9d50-8543-44b0-8c1a-bed9574ef29a)
 Call ID: 4f3b9d50-8543-44b0-8c1a-bed9574ef29a
  Args:
    source: :George_III_of_the_United_Kingdom
    type: :Person
  AddLiteral (bf23ac1e-e2b1-4f1b-a415-b0bcd622998f)
 Call ID: bf23ac1e-e2b1-4f1b-a415-b0bcd622998f
  Args:
    source: :George_III_of_the_United_Kingdom
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1738
  AddLiteral (470d0a94-b32b-4f9b-8a3c-a8864d5f1e04)
 Call ID: 470d0a94-b32b-4f9b-8a3c-a8864d5f1e04
  Args:
    literal_type: xsd:integer
    source: :George_III_of_the_United_Kingdom
    literal_value: 1820
    relation: :hasDeathYear
  AssignClass (478e7c34-93fe-4346-af29-01ac0bed44a9)
 Call ID: 478e7c34-93fe-4346-af29-01ac0bed44a9
  Args:
    type: :Woman
    source: :Charlotte_of_Mecklenburg_Strelitz
  AssignClass (35d3d444-5563-43e2-bac3-e0282d50fd99)
 Call ID: 35d3d444-5563-43e2-bac3-e0282d50fd99
  Args:
    type: :Person
    source: :Charlotte_of_Mecklenburg_Strelitz
  AddLiteral (5ee02d5c-9eec-42f5-8c7c-6ea47d309211)
 Call ID: 5ee02d5c-9eec-42f5-8c7c-6ea47d309211
  Args:
    literal_value: 1744
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: :Charlotte_of_Mecklenburg_Strelitz
  AddLiteral (af3b3cba-95f4-4ba2-9159-f85c3d59014f)
 Call ID: af3b3cba-95f4-4ba2-9159-f85c3d59014f
  Args:
    literal_type: xsd:integer
    source: :Charlotte_of_Mecklenburg_Strelitz
    relation: :hasDeathYear
    literal_value: 1818
  AssignClass (ed9a79e2-3d3f-463c-8455-cb7bfc66d284)
 Call ID: ed9a79e2-3d3f-463c-8455-cb7bfc66d284
  Args:
    source: :Frederick_Francis_III_Grand_Duke_of_Mecklenburg_Schwerin
    type: :Man
  AssignClass (94222112-95b2-452e-87df-78667485ea82)
 Call ID: 94222112-95b2-452e-87df-78667485ea82
  Args:
    type: :Person
    source: :Frederick_Francis_III_Grand_Duke_of_Mecklenburg_Schwerin
  AssignClass (d015dd28-fce7-4767-b473-39d83744e824)
 Call ID: d015dd28-fce7-4767-b473-39d83744e824
  Args:
    source: :Anastasia_Mikhailovna_of_Russia
    type: :Woman
  AssignClass (8089908b-4148-4e44-8da9-98c510fc824e)
 Call ID: 8089908b-4148-4e44-8da9-98c510fc824e
  Args:
    source: :Anastasia_Mikhailovna_of_Russia
    type: :Person
  AddTriple (0322a9ea-5dae-4540-81bf-3e3d76e6e7ca)
 Call ID: 0322a9ea-5dae-4540-81bf-3e3d76e6e7ca
  Args:
    source: :Frederick_Francis_IV_Grand_Duke_of_Mecklenburg_Schwerin
    relation: :hasFather
    target: :Frederick_Francis_III_Grand_Duke_of_Mecklenburg_Schwerin
  AddTriple (8f7d2683-0f3c-4694-b91a-8bb7c495c271)
 Call ID: 8f7d2683-0f3c-4694-b91a-8bb7c495c271
  Args:
    relation: :hasMother
    target: :Anastasia_Mikhailovna_of_Russia
    source: :Frederick_Francis_IV_Grand_Duke_of_Mecklenburg_Schwerin
  Finish (b2aaf2ca-06c1-460a-96ed-f441c77ecec5)
 Call ID: b2aaf2ca-06c1-460a-96ed-f441c77ecec5
  Args: