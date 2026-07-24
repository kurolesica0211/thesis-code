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
Earl of Lichfield is a title that has been created three times, twice in the  Peerage of England (1645 and 1674) and once in the Peerage of the United Kingdom (1831).
Following his father's death in 1960, Patrick Anson, 5th Earl of Lichfield, decided to give Shugborough Hall up to the National Trust in lieu of death duties, an arrangement finalized in 1966.
For his own burial, he chose the Anson vault at Colwich and was buried there in 2005.
Earls of Lichfield, third creation (1831)

The third creation, in the Peerage of the United Kingdom, came in William IV's coronation honours of 1831 in favour of Thomas Anson, 2nd Viscount Anson (1795–1854), a landowner and Whig politician from the Anson family who served as Master of the Buckhounds from 1830 to 1834 and as Postmaster General from 1835 to 1841.
The 1st Earl was the eldest son of Thomas Anson, 1st Viscount Anson, who on 17 February 1806 had been created Baron Soberton, of Soberton in the County of Southampton, and Viscount Anson, of Shugborough and Orgreave in the County of Stafford, both in the Peerage of the United Kingdom.
Also in 1831, the 1st Earl's cousin William Anson was made a baronet (see Anson Baronets).
The earldom of Lichfield continued to descend within the Anson family from father to son until the death of the 4th Earl, in 1960.
He was succeeded by his grandson, the 5th Earl, the only son of Lieutenant-Colonel Thomas William Arnold Anson, Viscount Anson (1913–1958), eldest son of the 4th Earl.
Known professionally as Patrick Lichfield, he was a successful photographer.
As of 2017 the titles are held by the 6th Earl, only son of the 5th Earl and Lady Leonora Grosvenor, daughter of the 5th Duke of Westminster.
He succeeded as the 6th Earl of Lichfield upon his father's death on 11 November 2005.
The 6th Earl married in December 2009 Lady Henrietta Conyngham, daughter of Henry Conyngham, 8th Marquess Conyngham.
List of title holders

Earls of Lichfield (1645)

Earls of Lichfield (1674)

Earls of Lichfield (1831)
Present peer

Thomas William Robert Hugh Anson, 6th Earl of Lichfield (born 19 July 1978) is the son of the 5th Earl and his wife Lady Leonora Mary Grosvenor.
Styled as Viscount Anson from birth, on 11 November 2005 he succeeded his father as Earl of Lichfield (UK, 1831), Viscount Anson, of Shugborough (UK, 1806), and Baron Soberton (UK, 1806).
They have two children, Thomas Ossian Patrick Wolfe Anson, Viscount Anson (born 2011), and the Hon.
Finnian Anson (born 2014).



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
  AssignClass (2e703ece-d16f-453a-8880-e8b0cb50ff8c)
 Call ID: 2e703ece-d16f-453a-8880-e8b0cb50ff8c
  Args:
    type: :Man
    source: Patrick Anson
  AssignClass (22e70e68-dbff-4c3e-a326-dcbc846019bd)
 Call ID: 22e70e68-dbff-4c3e-a326-dcbc846019bd
  Args:
    source: Patrick Anson
    type: :Person
  AddLiteral (97ed5849-fdfd-41cc-a7a7-1b5408664a18)
 Call ID: 97ed5849-fdfd-41cc-a7a7-1b5408664a18
  Args:
    source: Patrick Anson
    relation: :knownAs
    literal_type: xsd:string
    literal_value: 5th Earl of Lichfield
  AddLiteral (a0c7c4df-b176-4e7a-9223-c3c3ac677dc7)
 Call ID: a0c7c4df-b176-4e7a-9223-c3c3ac677dc7
  Args:
    source: Patrick Anson
    literal_value: 2005
    relation: :hasDeathYear
    literal_type: xsd:integer
  AssignClass (718492db-96e6-48b7-888c-909983309632)
 Call ID: 718492db-96e6-48b7-888c-909983309632
  Args:
    source: Thomas Anson (2nd Viscount Anson)
    type: :Man
  AssignClass (86e73b60-c3c5-4cc0-a6f0-3028d9612354)
 Call ID: 86e73b60-c3c5-4cc0-a6f0-3028d9612354
  Args:
    type: :Person
    source: Thomas Anson (2nd Viscount Anson)
  AddLiteral (e2a0e9fa-395d-46bc-a692-89a79997feec)
 Call ID: e2a0e9fa-395d-46bc-a692-89a79997feec
  Args:
    literal_type: xsd:string
    relation: :knownAs
    literal_value: 2nd Viscount Anson
    source: Thomas Anson (2nd Viscount Anson)
  AddLiteral (e357018d-07d6-47a3-abd3-d60ad1ff4aab)
 Call ID: e357018d-07d6-47a3-abd3-d60ad1ff4aab
  Args:
    source: Thomas Anson (2nd Viscount Anson)
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1795
  AddLiteral (d489d52d-6ad6-4d21-8799-3e73d607e3cb)
 Call ID: d489d52d-6ad6-4d21-8799-3e73d607e3cb
  Args:
    source: Thomas Anson (2nd Viscount Anson)
    literal_value: 1854
    relation: :hasDeathYear
    literal_type: xsd:integer
  AssignClass (f54737ab-ee58-4a09-991a-1286f9beb4e1)
 Call ID: f54737ab-ee58-4a09-991a-1286f9beb4e1
  Args:
    source: Thomas Anson (1st Viscount Anson)
    type: :Man
  AssignClass (38d1f871-e5f0-4281-b4c2-fd659e0df2a7)
 Call ID: 38d1f871-e5f0-4281-b4c2-fd659e0df2a7
  Args:
    source: Thomas Anson (1st Viscount Anson)
    type: :Person
  AddTriple (750cc593-1720-4f3e-b92a-3f37a883fd2e)
 Call ID: 750cc593-1720-4f3e-b92a-3f37a883fd2e
  Args:
    target: Thomas Anson (2nd Viscount Anson)
    source: Thomas Anson (1st Viscount Anson)
    relation: :isFatherOf
  AssignClass (3cdcba48-fa57-43c8-9474-d3f58c6c3108)
 Call ID: 3cdcba48-fa57-43c8-9474-d3f58c6c3108
  Args:
    type: :Man
    source: Thomas William Arnold Anson
  AssignClass (8c14f552-a39f-4330-94ef-189d0587ac04)
 Call ID: 8c14f552-a39f-4330-94ef-189d0587ac04
  Args:
    source: Thomas William Arnold Anson
    type: :Person
  AddLiteral (583ed199-2c8c-4d35-8b49-573f83ce7c06)
 Call ID: 583ed199-2c8c-4d35-8b49-573f83ce7c06
  Args:
    source: Thomas William Arnold Anson
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1913
  AddLiteral (3e1d02fd-8696-44a2-be15-c59053f9f983)
 Call ID: 3e1d02fd-8696-44a2-be15-c59053f9f983
  Args:
    literal_value: 1958
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: Thomas William Arnold Anson
  AddTriple (8e46a503-c2f9-4a86-bcd9-4e600f5cf4de)
 Call ID: 8e46a503-c2f9-4a86-bcd9-4e600f5cf4de
  Args:
    source: Thomas William Arnold Anson
    target: Patrick Anson
    relation: :isFatherOf
  AssignClass (01839eb5-219f-489a-850f-20e00f0e70b4)
 Call ID: 01839eb5-219f-489a-850f-20e00f0e70b4
  Args:
    source: Thomas William Robert Hugh Anson
    type: :Man
  AssignClass (1fd9bbce-b928-4b14-a2a7-553b05323da0)
 Call ID: 1fd9bbce-b928-4b14-a2a7-553b05323da0
  Args:
    type: :Person
    source: Thomas William Robert Hugh Anson
  AddLiteral (4165a8f9-5a87-4c24-ba4b-878a2d492953)
 Call ID: 4165a8f9-5a87-4c24-ba4b-878a2d492953
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1978
    source: Thomas William Robert Hugh Anson
  AddLiteral (3843ffba-dfdc-4ce8-962b-6895fb6f3dad)
 Call ID: 3843ffba-dfdc-4ce8-962b-6895fb6f3dad
  Args:
    literal_type: xsd:string
    relation: :knownAs
    literal_value: 6th Earl of Lichfield
    source: Thomas William Robert Hugh Anson
  AddTriple (c605be95-99b6-4245-a539-e00765cc5076)
 Call ID: c605be95-99b6-4245-a539-e00765cc5076
  Args:
    source: Patrick Anson
    target: Thomas William Robert Hugh Anson
    relation: :isFatherOf
  AssignClass (dd6a32cc-a08e-40a5-8bd4-7dd871517b4a)
 Call ID: dd6a32cc-a08e-40a5-8bd4-7dd871517b4a
  Args:
    source: Lady Leonora Mary Grosvenor
    type: :Woman
  AssignClass (6ebfe019-64f8-4f8b-bd01-fa3ad5d64166)
 Call ID: 6ebfe019-64f8-4f8b-bd01-fa3ad5d64166
  Args:
    source: Lady Leonora Mary Grosvenor
    type: :Person
  AddTriple (b35edafa-af9e-4020-8346-5a22c4606ddc)
 Call ID: b35edafa-af9e-4020-8346-5a22c4606ddc
  Args:
    relation: :isMotherOf
    target: Thomas William Robert Hugh Anson
    source: Lady Leonora Mary Grosvenor
  AssignClass (fc25d088-8430-4f18-9316-79e2be879641)
 Call ID: fc25d088-8430-4f18-9316-79e2be879641
  Args:
    source: Thomas Ossian Patrick Wolfe Anson
    type: :Man
  AssignClass (2a3a23e4-715c-40de-8bb1-b9cfbac4f4c4)
 Call ID: 2a3a23e4-715c-40de-8bb1-b9cfbac4f4c4
  Args:
    source: Thomas Ossian Patrick Wolfe Anson
    type: :Person
  AddLiteral (e428a543-f216-42ae-ba6a-9af6dd24ab94)
 Call ID: e428a543-f216-42ae-ba6a-9af6dd24ab94
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 2011
    source: Thomas Ossian Patrick Wolfe Anson
  AddTriple (8f5e7d52-cc95-46ce-8f41-7f4f33370b2d)
 Call ID: 8f5e7d52-cc95-46ce-8f41-7f4f33370b2d
  Args:
    relation: :isFatherOf
    source: Thomas William Robert Hugh Anson
    target: Thomas Ossian Patrick Wolfe Anson
  AssignClass (ab877142-4e17-4a12-af93-5eb7d66f09bd)
 Call ID: ab877142-4e17-4a12-af93-5eb7d66f09bd
  Args:
    type: :Man
    source: Finnian Anson
  AssignClass (147dc2ce-2ada-4253-87c8-b0a85d1efe2c)
 Call ID: 147dc2ce-2ada-4253-87c8-b0a85d1efe2c
  Args:
    type: :Person
    source: Finnian Anson
  AddLiteral (1f7b16c1-10e5-4d0d-bda7-af816ac6814f)
 Call ID: 1f7b16c1-10e5-4d0d-bda7-af816ac6814f
  Args:
    literal_value: 2014
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Finnian Anson
  AddTriple (0014115b-011d-4564-98b8-00cd3cfd8f51)
 Call ID: 0014115b-011d-4564-98b8-00cd3cfd8f51
  Args:
    source: Thomas William Robert Hugh Anson
    target: Finnian Anson
    relation: :isFatherOf
  AssignClass (94742161-321f-4539-b9f2-f72e03e48a47)
 Call ID: 94742161-321f-4539-b9f2-f72e03e48a47
  Args:
    type: :Woman
    source: Lady Henrietta Conyngham
  AssignClass (9c0cb9c0-3801-45e2-b070-520cc242a593)
 Call ID: 9c0cb9c0-3801-45e2-b070-520cc242a593
  Args:
    type: :Person
    source: Lady Henrietta Conyngham
  AddTriple (1d4b1223-43ca-44dd-996a-bdb7973d5820)
 Call ID: 1d4b1223-43ca-44dd-996a-bdb7973d5820
  Args:
    relation: :hasRelation
    source: Thomas William Robert Hugh Anson
    target: Lady Henrietta Conyngham
  AddLiteral (5db1f3b7-8d27-435a-b2f2-b0ef2d1128d8)
 Call ID: 5db1f3b7-8d27-435a-b2f2-b0ef2d1128d8
  Args:
    literal_value: 2009
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: Thomas William Robert Hugh Anson
  Finish (74c942bc-310f-4d50-953e-182d3c070c7a)
 Call ID: 74c942bc-310f-4d50-953e-182d3c070c7a
  Args: