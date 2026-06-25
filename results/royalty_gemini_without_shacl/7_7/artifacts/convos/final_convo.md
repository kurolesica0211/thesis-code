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
  AssignClass (9c6dd90e-7c36-4e8f-b84c-72233ccc0f66)
 Call ID: 9c6dd90e-7c36-4e8f-b84c-72233ccc0f66
  Args:
    type: :Man
    source: Patrick_Anson_5th_Earl_of_Lichfield
  AssignClass (1e722708-1e96-42b6-a305-ab5e9e2165b9)
 Call ID: 1e722708-1e96-42b6-a305-ab5e9e2165b9
  Args:
    type: :Person
    source: Patrick_Anson_5th_Earl_of_Lichfield
  AddLiteral (acab8f63-a061-48f0-8fc4-86a1756eee75)
 Call ID: acab8f63-a061-48f0-8fc4-86a1756eee75
  Args:
    source: Thomas_William_Arnold_Anson_Viscount_Anson
    literal_value: 1960
    relation: :hasDeathYear
    literal_type: xsd:integer
  AddTriple (a846d4eb-28d2-4db5-97a1-e31a03f05a63)
 Call ID: a846d4eb-28d2-4db5-97a1-e31a03f05a63
  Args:
    target: Thomas_William_Arnold_Anson_Viscount_Anson
    source: Patrick_Anson_5th_Earl_of_Lichfield
    relation: :hasFather
  AssignClass (5f7e1b14-6687-4301-8adf-38416bc90868)
 Call ID: 5f7e1b14-6687-4301-8adf-38416bc90868
  Args:
    source: Thomas_William_Arnold_Anson_Viscount_Anson
    type: :Man
  AssignClass (b4d62a62-0b90-459f-8f91-54f2efcda536)
 Call ID: b4d62a62-0b90-459f-8f91-54f2efcda536
  Args:
    type: :Person
    source: Thomas_William_Arnold_Anson_Viscount_Anson
  AddLiteral (dcf4ad49-807f-45ec-b876-2588af280df4)
 Call ID: dcf4ad49-807f-45ec-b876-2588af280df4
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Thomas_William_Arnold_Anson_Viscount_Anson
    literal_value: 1913
  AddLiteral (7e4eda61-93d0-4b95-8ad2-388ebc48b085)
 Call ID: 7e4eda61-93d0-4b95-8ad2-388ebc48b085
  Args:
    literal_value: 1958
    source: Thomas_William_Arnold_Anson_Viscount_Anson
    literal_type: xsd:integer
    relation: :hasDeathYear
  AssignClass (4716e12f-edcd-407e-b81d-d5bcdd106bee)
 Call ID: 4716e12f-edcd-407e-b81d-d5bcdd106bee
  Args:
    source: Thomas_William_Robert_Hugh_Anson_6th_Earl_of_Lichfield
    type: :Man
  AssignClass (32d772c8-39ad-42e7-9bbc-8ffb80a0c13c)
 Call ID: 32d772c8-39ad-42e7-9bbc-8ffb80a0c13c
  Args:
    source: Thomas_William_Robert_Hugh_Anson_6th_Earl_of_Lichfield
    type: :Person
  AddLiteral (e84eb72f-ffcd-4d6e-93f4-624a518c6b20)
 Call ID: e84eb72f-ffcd-4d6e-93f4-624a518c6b20
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1978
    source: Thomas_William_Robert_Hugh_Anson_6th_Earl_of_Lichfield
  AddTriple (ce174d05-3cea-4917-b20a-57847d4b5b5a)
 Call ID: ce174d05-3cea-4917-b20a-57847d4b5b5a
  Args:
    source: Thomas_William_Robert_Hugh_Anson_6th_Earl_of_Lichfield
    target: Patrick_Anson_5th_Earl_of_Lichfield
    relation: :hasFather
  AssignClass (cf25a35d-4abc-4cc2-8d12-1e085cd1171c)
 Call ID: cf25a35d-4abc-4cc2-8d12-1e085cd1171c
  Args:
    type: :Woman
    source: Lady_Leonora_Mary_Grosvenor
  AssignClass (302dbb60-17e1-4d47-ba55-975cdf47ab2b)
 Call ID: 302dbb60-17e1-4d47-ba55-975cdf47ab2b
  Args:
    type: :Person
    source: Lady_Leonora_Mary_Grosvenor
  AddTriple (5f8edadc-7d19-4841-bbb8-92f58b86a84a)
 Call ID: 5f8edadc-7d19-4841-bbb8-92f58b86a84a
  Args:
    target: Lady_Leonora_Mary_Grosvenor
    source: Thomas_William_Robert_Hugh_Anson_6th_Earl_of_Lichfield
    relation: :hasMother
  AssignClass (e2026a82-4a1a-49d9-92b0-82063881dfb6)
 Call ID: e2026a82-4a1a-49d9-92b0-82063881dfb6
  Args:
    type: :Man
    source: Thomas_Ossian_Patrick_Wolfe_Anson_Viscount_Anson
  AssignClass (20e52c43-ecfd-4736-a1d6-3f9a5ac27a54)
 Call ID: 20e52c43-ecfd-4736-a1d6-3f9a5ac27a54
  Args:
    type: :Person
    source: Thomas_Ossian_Patrick_Wolfe_Anson_Viscount_Anson
  AddLiteral (c2f74a3d-0cee-43f8-959d-220a6654a5b7)
 Call ID: c2f74a3d-0cee-43f8-959d-220a6654a5b7
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 2011
    source: Thomas_Ossian_Patrick_Wolfe_Anson_Viscount_Anson
  AddTriple (bf56d87c-e223-4fa8-9aad-62588045bc04)
 Call ID: bf56d87c-e223-4fa8-9aad-62588045bc04
  Args:
    source: Thomas_Ossian_Patrick_Wolfe_Anson_Viscount_Anson
    target: Thomas_William_Robert_Hugh_Anson_6th_Earl_of_Lichfield
    relation: :hasFather
  AssignClass (5786c121-2a09-48e1-a4e8-92671fd10c40)
 Call ID: 5786c121-2a09-48e1-a4e8-92671fd10c40
  Args:
    source: Finnian_Anson
    type: :Man
  AssignClass (9b953b56-bb48-4e91-9bc6-b10533732953)
 Call ID: 9b953b56-bb48-4e91-9bc6-b10533732953
  Args:
    type: :Person
    source: Finnian_Anson
  AddLiteral (be9aab96-bc70-4d2a-9cd0-d76875a6a9d3)
 Call ID: be9aab96-bc70-4d2a-9cd0-d76875a6a9d3
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 2014
    source: Finnian_Anson
  AddTriple (fc5c4e58-627e-4e20-83a5-457319a0837a)
 Call ID: fc5c4e58-627e-4e20-83a5-457319a0837a
  Args:
    relation: :hasFather
    target: Thomas_William_Robert_Hugh_Anson_6th_Earl_of_Lichfield
    source: Finnian_Anson
  AssignClass (4439aec3-a4eb-4176-9a87-e5887ce374e8)
 Call ID: 4439aec3-a4eb-4176-9a87-e5887ce374e8
  Args:
    source: Thomas_Anson_2nd_Viscount_Anson
    type: :Man
  AssignClass (fdb82973-f3c7-4409-95e5-eecec38ee12b)
 Call ID: fdb82973-f3c7-4409-95e5-eecec38ee12b
  Args:
    source: Thomas_Anson_2nd_Viscount_Anson
    type: :Person
  AddLiteral (c7bd5e48-264f-4d52-81a7-32cfcbf05634)
 Call ID: c7bd5e48-264f-4d52-81a7-32cfcbf05634
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1795
    source: Thomas_Anson_2nd_Viscount_Anson
  AddLiteral (9e82f8be-49cc-40a9-9611-fff386e974b5)
 Call ID: 9e82f8be-49cc-40a9-9611-fff386e974b5
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: Thomas_Anson_2nd_Viscount_Anson
    literal_value: 1854
  AssignClass (12ae3d58-fda5-4f0e-8578-29edfd5c53b5)
 Call ID: 12ae3d58-fda5-4f0e-8578-29edfd5c53b5
  Args:
    source: Thomas_Anson_1st_Viscount_Anson
    type: :Man
  AssignClass (207745e5-9fa0-463b-bf4c-af9dacb8a345)
 Call ID: 207745e5-9fa0-463b-bf4c-af9dacb8a345
  Args:
    source: Thomas_Anson_1st_Viscount_Anson
    type: :Person
  AddTriple (520b36a7-71a0-4753-a70f-bd6da6910b64)
 Call ID: 520b36a7-71a0-4753-a70f-bd6da6910b64
  Args:
    source: Thomas_Anson_2nd_Viscount_Anson
    target: Thomas_Anson_1st_Viscount_Anson
    relation: :hasFather
  AssignClass (334f8c65-7181-459b-a562-406d18319a7a)
 Call ID: 334f8c65-7181-459b-a562-406d18319a7a
  Args:
    type: :Woman
    source: Lady_Henrietta_Conyngham
  AssignClass (78d60f37-1952-42ee-97ef-a1057b5a0260)
 Call ID: 78d60f37-1952-42ee-97ef-a1057b5a0260
  Args:
    type: :Person
    source: Lady_Henrietta_Conyngham
  AddLiteral (4bef383b-65d1-4b52-b95d-1e54e6e2e4ab)
 Call ID: 4bef383b-65d1-4b52-b95d-1e54e6e2e4ab
  Args:
    literal_value: 2009
    source: Thomas_William_Robert_Hugh_Anson_6th_Earl_of_Lichfield
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AddTriple (16b5c6bb-cc8f-45ca-8344-c8cbd6c0fb53)
 Call ID: 16b5c6bb-cc8f-45ca-8344-c8cbd6c0fb53
  Args:
    source: Thomas_William_Robert_Hugh_Anson_6th_Earl_of_Lichfield
    target: Lady_Henrietta_Conyngham
    relation: :hasRelation
  Finish (e98968ff-e32c-43f1-b10a-6d3f204052c3)
 Call ID: e98968ff-e32c-43f1-b10a-6d3f204052c3
  Args: