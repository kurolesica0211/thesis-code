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
  AssignClass (8005a573-8bd8-48cc-9b25-4c46a7591e5f)
 Call ID: 8005a573-8bd8-48cc-9b25-4c46a7591e5f
  Args:
    source: Thomas_Anson_2nd_Viscount_Anson
    type: :Man
  AssignClass (708ffd19-d972-40e9-a3e0-0bf23acdc94c)
 Call ID: 708ffd19-d972-40e9-a3e0-0bf23acdc94c
  Args:
    type: :Man
    source: Thomas_Anson_1st_Viscount_Anson
  AddTriple (77226987-9174-4fb7-833f-4fc701e19c55)
 Call ID: 77226987-9174-4fb7-833f-4fc701e19c55
  Args:
    target: Thomas_Anson_2nd_Viscount_Anson
    relation: :isFatherOf
    source: Thomas_Anson_1st_Viscount_Anson
  AddLiteral (a99dea51-5c46-49b1-af81-fa62a4813094)
 Call ID: a99dea51-5c46-49b1-af81-fa62a4813094
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Thomas_Anson_2nd_Viscount_Anson
    literal_value: 1795
  AddLiteral (e1abf0c3-1875-4a70-b72b-539dd0f3e1d5)
 Call ID: e1abf0c3-1875-4a70-b72b-539dd0f3e1d5
  Args:
    literal_value: 1854
    source: Thomas_Anson_2nd_Viscount_Anson
    literal_type: xsd:integer
    relation: :hasDeathYear
  AssignClass (cb6ccd3c-9547-45d4-8e17-07bb3fbcc9b1)
 Call ID: cb6ccd3c-9547-45d4-8e17-07bb3fbcc9b1
  Args:
    type: :Man
    source: Patrick_Anson_5th_Earl_of_Lichfield
  AssignClass (38cca804-d4ca-458c-8714-12240b0d6708)
 Call ID: 38cca804-d4ca-458c-8714-12240b0d6708
  Args:
    type: :Man
    source: Thomas_William_Arnold_Anson_Viscount_Anson
  AddTriple (a9113aee-d5bd-4e14-88e7-2304fe0a6ed7)
 Call ID: a9113aee-d5bd-4e14-88e7-2304fe0a6ed7
  Args:
    source: Thomas_William_Arnold_Anson_Viscount_Anson
    relation: :isFatherOf
    target: Patrick_Anson_5th_Earl_of_Lichfield
  AddLiteral (8dc1dda5-8abe-4109-9eb7-1e84e5053347)
 Call ID: 8dc1dda5-8abe-4109-9eb7-1e84e5053347
  Args:
    literal_value: 1913
    source: Thomas_William_Arnold_Anson_Viscount_Anson
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (3283fdc4-7496-43ba-9618-e946de7b0e3e)
 Call ID: 3283fdc4-7496-43ba-9618-e946de7b0e3e
  Args:
    literal_value: 1958
    source: Thomas_William_Arnold_Anson_Viscount_Anson
    literal_type: xsd:integer
    relation: :hasDeathYear
  AssignClass (97cc2b17-7322-4967-805c-d3f442a0aeda)
 Call ID: 97cc2b17-7322-4967-805c-d3f442a0aeda
  Args:
    type: :Man
    source: Thomas_William_Robert_Hugh_Anson_6th_Earl_of_Lichfield
  AssignClass (4f6d8314-179f-4882-85ab-de07f65893a6)
 Call ID: 4f6d8314-179f-4882-85ab-de07f65893a6
  Args:
    source: Lady_Leonora_Mary_Grosvenor
    type: :Woman
  AddTriple (f0d4cf6e-7c36-400e-a15f-941086bc79a9)
 Call ID: f0d4cf6e-7c36-400e-a15f-941086bc79a9
  Args:
    target: Thomas_William_Robert_Hugh_Anson_6th_Earl_of_Lichfield
    source: Patrick_Anson_5th_Earl_of_Lichfield
    relation: :isFatherOf
  AddTriple (3e5693ba-0c7e-40cb-8e71-eab52c91353e)
 Call ID: 3e5693ba-0c7e-40cb-8e71-eab52c91353e
  Args:
    relation: :isMotherOf
    source: Lady_Leonora_Mary_Grosvenor
    target: Thomas_William_Robert_Hugh_Anson_6th_Earl_of_Lichfield
  AddLiteral (fb4a0829-8799-43d8-9971-0a2c1214c06c)
 Call ID: fb4a0829-8799-43d8-9971-0a2c1214c06c
  Args:
    literal_value: 1978
    source: Thomas_William_Robert_Hugh_Anson_6th_Earl_of_Lichfield
    relation: :hasBirthYear
    literal_type: xsd:integer
  AssignClass (020f52f3-474e-4048-80a1-174a2778ebe3)
 Call ID: 020f52f3-474e-4048-80a1-174a2778ebe3
  Args:
    type: :Man
    source: Thomas_Ossian_Patrick_Wolfe_Anson_Viscount_Anson
  AssignClass (3bf2e7cb-4c6f-4934-9ef5-a4b491f955e5)
 Call ID: 3bf2e7cb-4c6f-4934-9ef5-a4b491f955e5
  Args:
    type: :Man
    source: Finnian_Anson
  AddTriple (f2cf483b-e528-48ee-ad99-36a9f688403d)
 Call ID: f2cf483b-e528-48ee-ad99-36a9f688403d
  Args:
    target: Thomas_Ossian_Patrick_Wolfe_Anson_Viscount_Anson
    relation: :isFatherOf
    source: Thomas_William_Robert_Hugh_Anson_6th_Earl_of_Lichfield
  AddTriple (9badbe58-336b-4620-b1db-f4e03e72437a)
 Call ID: 9badbe58-336b-4620-b1db-f4e03e72437a
  Args:
    target: Finnian_Anson
    relation: :isFatherOf
    source: Thomas_William_Robert_Hugh_Anson_6th_Earl_of_Lichfield
  AddLiteral (21901eea-aa59-4a0d-b7fd-4157d3524304)
 Call ID: 21901eea-aa59-4a0d-b7fd-4157d3524304
  Args:
    literal_value: 2011
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Thomas_Ossian_Patrick_Wolfe_Anson_Viscount_Anson
  AddLiteral (3bc5c0a7-bda7-4f3c-9271-f6514421c993)
 Call ID: 3bc5c0a7-bda7-4f3c-9271-f6514421c993
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Finnian_Anson
    literal_value: 2014
  AssignClass (69909c31-a02d-44eb-9009-e8181bb8aa65)
 Call ID: 69909c31-a02d-44eb-9009-e8181bb8aa65
  Args:
    type: :Woman
    source: Lady_Henrietta_Conyngham
  AddLiteral (3d5705a0-0151-4788-90de-589899923e9e)
 Call ID: 3d5705a0-0151-4788-90de-589899923e9e
  Args:
    literal_value: 2009
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: Thomas_William_Robert_Hugh_Anson_6th_Earl_of_Lichfield
  Finish (1e4370cd-518c-426e-8e98-bc6ba4c073cd)
 Call ID: 1e4370cd-518c-426e-8e98-bc6ba4c073cd
  Args: