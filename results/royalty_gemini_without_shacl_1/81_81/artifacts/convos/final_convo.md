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
Prince Vincent of Denmark, Count of Monpezat RE (Vincent Frederik Minik Alexander; born 8 January 2011) is a member of the Danish royal family.
He is the third child and younger son of King Frederik X and Queen Mary, the sixth grandchild and youngest grandson of Queen Margrethe II and Prince Henrik, and the older twin brother of Princess Josephine.
Vincent is third in line to the Danish throne, after his older brother, Crown Prince Christian, and older sister, Princess Isabella.
Birth and early life

Queen Margrethe II


Vincent was born on 8 January 2011 at Rigshospitalet, the Copenhagen University Hospital, in Copenhagen, at 10:30 am local time, 26 minutes before his twin sister.
Shortly after the birth, while speaking to the press, the Crown Prince joked about calling his newborn son Elvis, as the twins share a birthday with Elvis Presley.
Vincent and his sister were baptised by the royal confessor, the Bishop of Copenhagen Erik Norman Svendsen, on 14 April at the Church of Holmen in central Copenhagen.
The twins were baptised at the royal baptismal font which has been used for the baptism of royal children in Denmark since 1671.
Prince Vincent wore the royal christening gown which was made for his great-great-grandfather, King Christian X, in 1870, while his sister wore a gown found among Queen Ingrid's belongings.
His name was announced as Vincent Frederik Minik Alexander.
His godparents are his maternal uncle, John Stuart Donaldson; his father's first cousin, the Prince of Sayn-Wittgenstein-Berleburg (then the Hereditary Prince); his mother's lady-in-waiting, Caroline Heering; and friends of his parents, the King of Spain (then the Prince of Asturias), Count Michael Ahlefeldt-Laurvig-Bille and Baroness Helle Reedtz-Thott.
Under the old system of male-preference primogeniture, Vincent would have displaced his elder sister Isabella in the line of succession; with the new law, he comes directly after her instead.
On 15 August 2017, Vincent and his younger twin sister started school at Tranegårdsskolen in Gentofte – the same public school as their elder siblings.
Titles, styles, and honours

Vincent is styled as His Royal Highness Prince Vincent of Denmark, Count of Monpezat.



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
  AssignClass (e64c3f05-5aaf-4e00-a514-371662b8358c)
 Call ID: e64c3f05-5aaf-4e00-a514-371662b8358c
  Args:
    source: Prince Vincent of Denmark
    type: :Person
  AssignClass (c9209bf2-756d-4878-a008-b7f587b8363d)
 Call ID: c9209bf2-756d-4878-a008-b7f587b8363d
  Args:
    source: Prince Vincent of Denmark
    type: :Man
  AddLiteral (7d6161eb-acd2-46f8-94e6-a568528b6ceb)
 Call ID: 7d6161eb-acd2-46f8-94e6-a568528b6ceb
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Prince Vincent of Denmark
    literal_value: 2011
  AssignClass (68c6ab79-9456-4ab0-8ec7-109044855c91)
 Call ID: 68c6ab79-9456-4ab0-8ec7-109044855c91
  Args:
    type: :Person
    source: King Frederik X
  AssignClass (f0c99245-3443-4d41-bff4-17f724ed69f2)
 Call ID: f0c99245-3443-4d41-bff4-17f724ed69f2
  Args:
    type: :Man
    source: King Frederik X
  AssignClass (ac4ecee7-3c3f-4812-88d5-f99202980caa)
 Call ID: ac4ecee7-3c3f-4812-88d5-f99202980caa
  Args:
    type: :Person
    source: Queen Mary
  AssignClass (c683eca0-a87a-42ee-8d0b-13fec8d29959)
 Call ID: c683eca0-a87a-42ee-8d0b-13fec8d29959
  Args:
    source: Queen Mary
    type: :Woman
  AddTriple (4df6dcba-5937-4a69-ad3f-b60ec9686977)
 Call ID: 4df6dcba-5937-4a69-ad3f-b60ec9686977
  Args:
    relation: :hasFather
    target: King Frederik X
    source: Prince Vincent of Denmark
  AddTriple (c773d7a4-ce82-430d-8e43-5ec68f4de705)
 Call ID: c773d7a4-ce82-430d-8e43-5ec68f4de705
  Args:
    relation: :hasMother
    target: Queen Mary
    source: Prince Vincent of Denmark
  AssignClass (cd5f07b7-f70a-42b1-b077-58f70432b11e)
 Call ID: cd5f07b7-f70a-42b1-b077-58f70432b11e
  Args:
    type: :Person
    source: Queen Margrethe II
  AssignClass (bdc9f146-1279-49b2-a0cf-9ee2957b4de6)
 Call ID: bdc9f146-1279-49b2-a0cf-9ee2957b4de6
  Args:
    source: Queen Margrethe II
    type: :Woman
  AssignClass (91076626-fa13-4c59-b0f0-8dd528e4f789)
 Call ID: 91076626-fa13-4c59-b0f0-8dd528e4f789
  Args:
    source: Prince Henrik
    type: :Person
  AssignClass (c64a3696-5911-4375-b0ab-ffd333d7b003)
 Call ID: c64a3696-5911-4375-b0ab-ffd333d7b003
  Args:
    source: Prince Henrik
    type: :Man
  AddTriple (2d1dc0df-528f-4dd6-a00c-352c59677e2f)
 Call ID: 2d1dc0df-528f-4dd6-a00c-352c59677e2f
  Args:
    relation: :hasAncestor
    target: Queen Margrethe II
    source: Prince Vincent of Denmark
  AddTriple (fce06dcc-c566-4ea6-9c85-35175fc1862d)
 Call ID: fce06dcc-c566-4ea6-9c85-35175fc1862d
  Args:
    target: Prince Henrik
    source: Prince Vincent of Denmark
    relation: :hasAncestor
  AssignClass (bab55698-f578-40b5-a163-50dfe864f709)
 Call ID: bab55698-f578-40b5-a163-50dfe864f709
  Args:
    source: Princess Josephine
    type: :Person
  AssignClass (49dc67a3-b266-4acf-b653-f61165d5fd86)
 Call ID: 49dc67a3-b266-4acf-b653-f61165d5fd86
  Args:
    source: Princess Josephine
    type: :Woman
  AddTriple (8ee0de31-6850-493a-8452-2b62660926c8)
 Call ID: 8ee0de31-6850-493a-8452-2b62660926c8
  Args:
    relation: :isSiblingOf
    target: Princess Josephine
    source: Prince Vincent of Denmark
  AssignClass (c0df4e87-e8e0-4f59-8735-602bd0fac126)
 Call ID: c0df4e87-e8e0-4f59-8735-602bd0fac126
  Args:
    type: :Person
    source: Crown Prince Christian
  AssignClass (ae23dab2-bee5-445d-b58a-d57b7318f99c)
 Call ID: ae23dab2-bee5-445d-b58a-d57b7318f99c
  Args:
    type: :Man
    source: Crown Prince Christian
  AddTriple (7b689d32-57a6-4c6d-8380-609b2c7a431b)
 Call ID: 7b689d32-57a6-4c6d-8380-609b2c7a431b
  Args:
    relation: :isSiblingOf
    source: Prince Vincent of Denmark
    target: Crown Prince Christian
  AssignClass (8fb35549-2d84-46f2-aa73-d85834dc0e41)
 Call ID: 8fb35549-2d84-46f2-aa73-d85834dc0e41
  Args:
    source: Princess Isabella
    type: :Person
  AssignClass (b3ffcfbe-68b2-4c8b-a1e9-1922fd99c50f)
 Call ID: b3ffcfbe-68b2-4c8b-a1e9-1922fd99c50f
  Args:
    type: :Woman
    source: Princess Isabella
  AddTriple (b7c3ad2e-b0da-45c2-b6a9-f0fee56772c8)
 Call ID: b7c3ad2e-b0da-45c2-b6a9-f0fee56772c8
  Args:
    source: Prince Vincent of Denmark
    target: Princess Isabella
    relation: :isSiblingOf
  AssignClass (53630c5e-57a4-4414-88d9-35e60197be6b)
 Call ID: 53630c5e-57a4-4414-88d9-35e60197be6b
  Args:
    source: King Christian X
    type: :Person
  AssignClass (77c307e4-e605-48c1-be91-1e87776ae764)
 Call ID: 77c307e4-e605-48c1-be91-1e87776ae764
  Args:
    type: :Man
    source: King Christian X
  AddTriple (d9a7a210-5bc6-467d-909f-4e444cb4b922)
 Call ID: d9a7a210-5bc6-467d-909f-4e444cb4b922
  Args:
    source: Prince Vincent of Denmark
    target: King Christian X
    relation: :hasAncestor
  AssignClass (3ca227ae-252d-415d-90e0-ca98ed20b4b1)
 Call ID: 3ca227ae-252d-415d-90e0-ca98ed20b4b1
  Args:
    type: :Person
    source: Queen Ingrid
  AssignClass (73d0569e-c986-4e5e-acfa-933f2f4e0425)
 Call ID: 73d0569e-c986-4e5e-acfa-933f2f4e0425
  Args:
    type: :Woman
    source: Queen Ingrid
  Finish (85644b59-e274-4f82-9be6-1003ff1e30ce)
 Call ID: 85644b59-e274-4f82-9be6-1003ff1e30ce
  Args: