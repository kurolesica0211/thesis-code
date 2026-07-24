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
  AssignClass (85acb3bc-d44a-4e7e-ac6e-6e66b3016be1)
 Call ID: 85acb3bc-d44a-4e7e-ac6e-6e66b3016be1
  Args:
    source: Thomas_Anson_2nd_Viscount_Anson
    type: :Man
  AssignClass (6f20d855-9c6f-4166-8fe4-85c7adfcc3e6)
 Call ID: 6f20d855-9c6f-4166-8fe4-85c7adfcc3e6
  Args:
    source: Thomas_Anson_2nd_Viscount_Anson
    type: :Person
  AddLiteral (47432f48-0d0f-441e-a641-f2806efc4ab6)
 Call ID: 47432f48-0d0f-441e-a641-f2806efc4ab6
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1795
    source: Thomas_Anson_2nd_Viscount_Anson
  AddLiteral (269c844a-8b1e-4e28-8aab-a8ea92e61fd8)
 Call ID: 269c844a-8b1e-4e28-8aab-a8ea92e61fd8
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1854
    source: Thomas_Anson_2nd_Viscount_Anson
  AssignClass (4cfbd30b-61cf-4bf5-bec5-60e2b780aaa7)
 Call ID: 4cfbd30b-61cf-4bf5-bec5-60e2b780aaa7
  Args:
    source: Thomas_Anson_1st_Viscount_Anson
    type: :Man
  AssignClass (c53a1cc3-9784-4010-af0c-122183e842f5)
 Call ID: c53a1cc3-9784-4010-af0c-122183e842f5
  Args:
    type: :Person
    source: Thomas_Anson_1st_Viscount_Anson
  AddTriple (a426ae7d-84dc-44d3-bad7-bd79e311319c)
 Call ID: a426ae7d-84dc-44d3-bad7-bd79e311319c
  Args:
    relation: :isFatherOf
    target: Thomas_Anson_2nd_Viscount_Anson
    source: Thomas_Anson_1st_Viscount_Anson
  AssignClass (2f173c7d-8d5e-4e3b-91a4-5c785861240e)
 Call ID: 2f173c7d-8d5e-4e3b-91a4-5c785861240e
  Args:
    type: :Man
    source: Patrick_Anson_5th_Earl_of_Lichfield
  AssignClass (5f493f44-8f5a-4a23-ac63-2dc5097b7f13)
 Call ID: 5f493f44-8f5a-4a23-ac63-2dc5097b7f13
  Args:
    source: Patrick_Anson_5th_Earl_of_Lichfield
    type: :Person
  AddLiteral (113b1ba2-601b-4922-819d-f8fd8d12cbae)
 Call ID: 113b1ba2-601b-4922-819d-f8fd8d12cbae
  Args:
    literal_value: Patrick Lichfield
    source: Patrick_Anson_5th_Earl_of_Lichfield
    relation: :knownAs
    literal_type: xsd:string
  AddLiteral (e2518b7e-096c-47c2-88c2-6677c8702c5b)
 Call ID: e2518b7e-096c-47c2-88c2-6677c8702c5b
  Args:
    source: Patrick_Anson_5th_Earl_of_Lichfield
    literal_value: 2005
    literal_type: xsd:integer
    relation: :hasDeathYear
  AssignClass (82098a0d-1e48-49c0-ba50-98119a31b44b)
 Call ID: 82098a0d-1e48-49c0-ba50-98119a31b44b
  Args:
    source: Thomas_William_Arnold_Anson_Viscount_Anson
    type: :Man
  AssignClass (672327a3-b7c2-453c-873b-063566da73e3)
 Call ID: 672327a3-b7c2-453c-873b-063566da73e3
  Args:
    source: Thomas_William_Arnold_Anson_Viscount_Anson
    type: :Person
  AddLiteral (4f0ced06-c6f9-49b6-aa45-d277ca827910)
 Call ID: 4f0ced06-c6f9-49b6-aa45-d277ca827910
  Args:
    source: Thomas_William_Arnold_Anson_Viscount_Anson
    literal_value: 1913
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (6aab6c81-6673-42a3-a402-dd1e3e10ace2)
 Call ID: 6aab6c81-6673-42a3-a402-dd1e3e10ace2
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1958
    source: Thomas_William_Arnold_Anson_Viscount_Anson
  AddTriple (e5ff55f3-ae83-4862-beb2-5c95fc43bb6b)
 Call ID: e5ff55f3-ae83-4862-beb2-5c95fc43bb6b
  Args:
    source: Thomas_William_Arnold_Anson_Viscount_Anson
    target: Patrick_Anson_5th_Earl_of_Lichfield
    relation: :isFatherOf
  AssignClass (d8373db1-e0c8-4848-89fc-2457568b3f97)
 Call ID: d8373db1-e0c8-4848-89fc-2457568b3f97
  Args:
    source: Thomas_William_Robert_Hugh_Anson_6th_Earl_of_Lichfield
    type: :Man
  AssignClass (5dd0f8be-f1d8-4c85-ad60-3bf1ee9cd0f5)
 Call ID: 5dd0f8be-f1d8-4c85-ad60-3bf1ee9cd0f5
  Args:
    type: :Person
    source: Thomas_William_Robert_Hugh_Anson_6th_Earl_of_Lichfield
  AddLiteral (8387ecf0-25c2-4fc9-bb6e-9e6c1c5aeb19)
 Call ID: 8387ecf0-25c2-4fc9-bb6e-9e6c1c5aeb19
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1978
    source: Thomas_William_Robert_Hugh_Anson_6th_Earl_of_Lichfield
  AddTriple (0f51c45f-420f-4267-9880-f37310568b20)
 Call ID: 0f51c45f-420f-4267-9880-f37310568b20
  Args:
    relation: :isFatherOf
    source: Patrick_Anson_5th_Earl_of_Lichfield
    target: Thomas_William_Robert_Hugh_Anson_6th_Earl_of_Lichfield
  AssignClass (a76beb8a-27d7-4346-a9f6-326a84d7dff3)
 Call ID: a76beb8a-27d7-4346-a9f6-326a84d7dff3
  Args:
    source: Lady_Leonora_Mary_Grosvenor
    type: :Woman
  AssignClass (6656ddc3-09a3-4e50-bebb-0577e21dab83)
 Call ID: 6656ddc3-09a3-4e50-bebb-0577e21dab83
  Args:
    type: :Person
    source: Lady_Leonora_Mary_Grosvenor
  AddTriple (b4686533-4676-4c57-ae1a-480ddc6aab08)
 Call ID: b4686533-4676-4c57-ae1a-480ddc6aab08
  Args:
    target: Thomas_William_Robert_Hugh_Anson_6th_Earl_of_Lichfield
    source: Lady_Leonora_Mary_Grosvenor
    relation: :isMotherOf
  AssignClass (cd7e8e3a-3e6e-4ce0-9d21-d75cfcb9c1be)
 Call ID: cd7e8e3a-3e6e-4ce0-9d21-d75cfcb9c1be
  Args:
    type: :Man
    source: Thomas_Ossian_Patrick_Wolfe_Anson_Viscount_Anson
  AssignClass (4e2d32e6-e6f8-48d7-8ee1-7ae6527e81d4)
 Call ID: 4e2d32e6-e6f8-48d7-8ee1-7ae6527e81d4
  Args:
    source: Thomas_Ossian_Patrick_Wolfe_Anson_Viscount_Anson
    type: :Person
  AddLiteral (da68d342-0a8d-42e4-98f7-66ee0f28278c)
 Call ID: da68d342-0a8d-42e4-98f7-66ee0f28278c
  Args:
    literal_value: 2011
    source: Thomas_Ossian_Patrick_Wolfe_Anson_Viscount_Anson
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddTriple (1888c160-b8a6-4f69-9fb6-3426c85aa603)
 Call ID: 1888c160-b8a6-4f69-9fb6-3426c85aa603
  Args:
    relation: :isFatherOf
    source: Thomas_William_Robert_Hugh_Anson_6th_Earl_of_Lichfield
    target: Thomas_Ossian_Patrick_Wolfe_Anson_Viscount_Anson
  AssignClass (4f18bc03-cd6a-4ac9-ba3f-aca4e8510f92)
 Call ID: 4f18bc03-cd6a-4ac9-ba3f-aca4e8510f92
  Args:
    type: :Man
    source: Finnian_Anson
  AssignClass (0946b505-1966-4f10-98d1-c211222e0419)
 Call ID: 0946b505-1966-4f10-98d1-c211222e0419
  Args:
    type: :Person
    source: Finnian_Anson
  AddLiteral (2ad7f80c-8336-450c-ba25-4d9008728d88)
 Call ID: 2ad7f80c-8336-450c-ba25-4d9008728d88
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 2014
    source: Finnian_Anson
  AddTriple (f3ecb3ba-87e4-4008-b6fc-1f35d054d73a)
 Call ID: f3ecb3ba-87e4-4008-b6fc-1f35d054d73a
  Args:
    relation: :isFatherOf
    source: Thomas_William_Robert_Hugh_Anson_6th_Earl_of_Lichfield
    target: Finnian_Anson
  AssignClass (0b12348c-18a6-4c20-9355-296536e861cb)
 Call ID: 0b12348c-18a6-4c20-9355-296536e861cb
  Args:
    source: Lady_Henrietta_Conyngham
    type: :Woman
  AssignClass (f7c5b054-45f1-468d-b114-68fa5a95e1cf)
 Call ID: f7c5b054-45f1-468d-b114-68fa5a95e1cf
  Args:
    source: Lady_Henrietta_Conyngham
    type: :Person
  AddLiteral (f6f24c88-7600-4873-9c12-01fe79b52d48)
 Call ID: f6f24c88-7600-4873-9c12-01fe79b52d48
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 2009
    source: Thomas_William_Robert_Hugh_Anson_6th_Earl_of_Lichfield
  Finish (fe739549-780c-43b8-a94a-02ab877b4012)
 Call ID: fe739549-780c-43b8-a94a-02ab877b4012
  Args: