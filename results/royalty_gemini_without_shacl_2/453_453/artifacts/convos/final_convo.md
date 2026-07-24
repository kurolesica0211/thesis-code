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
John Herbert Bowes-Lyon (1 April 1886 – 7 February 1930) was the second son of the 14th
Earl of Strathmore and Kinghorne and the Countess of Strathmore and Kinghorne, and the brother of Elizabeth Bowes-Lyon, the future Queen Elizabeth the Queen Mother.
He was the uncle of Queen Elizabeth II, although he died when she was a small child and before her sister Princess Margaret was born.
Early life

John Bowes-Lyon was educated at Eton and New College, Oxford, where he played first-class cricket for the university side in three matches in 1906 and 1907, playing as a fast-medium bowler.
Marriage and children

On 29 September 1914, Bowes-Lyon married Fenella Hepburn-Stuart-Forbes-Trefusis (19 August 1889 – 19 July 1966), the younger daughter of Charles Hepburn-Stuart-Forbes-Trefusis, 21st Baron Clinton.
They had five daughters:


World War I

Before the outbreak of World War I, Bowes-Lyon worked as a stockbroker in the City of London for the firm Rowe and Pitman.
While receiving treatment in the UK, he admitted having experienced a nervous breakdown in 1912 and also suffered from neurasthenia.
Death

Bowes-Lyon died at the family home of Glamis Castle just after midnight on the morning of 7 February 1930 of pneumonia, aged 43, leaving his widow to care for their four young children.
Bowes-Lyon's widow, Fenella Trefusis, was a leading guest at the 1947 wedding of Princess Elizabeth and Philip Mountbatten.



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
  AssignClass (704b32f2-a0f5-41da-b689-5514dd4b556a)
 Call ID: 704b32f2-a0f5-41da-b689-5514dd4b556a
  Args:
    type: :Man
    source: John_Herbert_Bowes-Lyon
  AddLiteral (fa54153e-161a-4399-8e4e-7c3fd849635f)
 Call ID: fa54153e-161a-4399-8e4e-7c3fd849635f
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1886
    source: John_Herbert_Bowes-Lyon
  AddLiteral (2175fe4c-2f19-4870-b0dd-e4361bc18c1e)
 Call ID: 2175fe4c-2f19-4870-b0dd-e4361bc18c1e
  Args:
    source: John_Herbert_Bowes-Lyon
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1930
  AssignClass (2dfe73da-1ab1-4ad9-a1bb-c6dc1e43645e)
 Call ID: 2dfe73da-1ab1-4ad9-a1bb-c6dc1e43645e
  Args:
    type: :Man
    source: Earl_of_Strathmore_and_Kinghorne_14th
  AssignClass (2dc392d9-ad72-4fb4-b918-60ad5c8a1fb9)
 Call ID: 2dc392d9-ad72-4fb4-b918-60ad5c8a1fb9
  Args:
    type: :Woman
    source: Countess_of_Strathmore_and_Kinghorne
  AddTriple (5320a3e7-bc60-43a1-ad9b-fd0888d4fc34)
 Call ID: 5320a3e7-bc60-43a1-ad9b-fd0888d4fc34
  Args:
    target: Earl_of_Strathmore_and_Kinghorne_14th
    source: John_Herbert_Bowes-Lyon
    relation: :isSonOf
  AddTriple (a126435c-6a3d-4f09-b8dd-f7ce62b3d46b)
 Call ID: a126435c-6a3d-4f09-b8dd-f7ce62b3d46b
  Args:
    relation: :isSonOf
    source: John_Herbert_Bowes-Lyon
    target: Countess_of_Strathmore_and_Kinghorne
  AssignClass (7eba92dc-e8f9-4298-a230-217d3287d4ff)
 Call ID: 7eba92dc-e8f9-4298-a230-217d3287d4ff
  Args:
    source: Elizabeth_Bowes-Lyon
    type: :Woman
  AddTriple (f20242f6-e454-4050-9497-8182763e1a98)
 Call ID: f20242f6-e454-4050-9497-8182763e1a98
  Args:
    target: Elizabeth_Bowes-Lyon
    source: John_Herbert_Bowes-Lyon
    relation: :isSiblingOf
  AssignClass (283ac97f-2d61-40f6-bd04-f35b005757f8)
 Call ID: 283ac97f-2d61-40f6-bd04-f35b005757f8
  Args:
    type: :Woman
    source: Queen_Elizabeth_II
  AddTriple (7e479ea8-4c4c-4f53-be74-a132c0e2d9ed)
 Call ID: 7e479ea8-4c4c-4f53-be74-a132c0e2d9ed
  Args:
    relation: :isUncleOf
    source: John_Herbert_Bowes-Lyon
    target: Queen_Elizabeth_II
  AssignClass (f44dabdc-a511-4cdd-a4a5-32a6c358d1c5)
 Call ID: f44dabdc-a511-4cdd-a4a5-32a6c358d1c5
  Args:
    source: Princess_Margaret
    type: :Woman
  AssignClass (a7220d5d-e890-43e7-8c26-094e2f7312ed)
 Call ID: a7220d5d-e890-43e7-8c26-094e2f7312ed
  Args:
    type: :Woman
    source: Fenella_Hepburn-Stuart-Forbes-Trefusis
  AddLiteral (cd025dfd-8ded-427b-b37b-447f785083d7)
 Call ID: cd025dfd-8ded-427b-b37b-447f785083d7
  Args:
    source: Fenella_Hepburn-Stuart-Forbes-Trefusis
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1889
  AddLiteral (58895b57-ab2a-4616-b499-067c601d3b70)
 Call ID: 58895b57-ab2a-4616-b499-067c601d3b70
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 1966
    source: Fenella_Hepburn-Stuart-Forbes-Trefusis
  AddLiteral (57b8a992-b9d8-4db4-88c0-69d0cee2ad2b)
 Call ID: 57b8a992-b9d8-4db4-88c0-69d0cee2ad2b
  Args:
    relation: :hasMarriageYear
    literal_type: xsd:integer
    literal_value: 1914
    source: John_Herbert_Bowes-Lyon
  AddTriple (1690c64f-f0de-47b0-ab73-8acfa4f9b369)
 Call ID: 1690c64f-f0de-47b0-ab73-8acfa4f9b369
  Args:
    relation: :hasRelation
    source: John_Herbert_Bowes-Lyon
    target: Fenella_Hepburn-Stuart-Forbes-Trefusis
  AssignClass (531fcf66-8c06-44cb-9af1-5b8cd73aeaf6)
 Call ID: 531fcf66-8c06-44cb-9af1-5b8cd73aeaf6
  Args:
    type: :Man
    source: Charles_Hepburn-Stuart-Forbes-Trefusis_21st_Baron_Clinton
  AddTriple (8c5f28a7-90c3-413e-b222-e5551132317d)
 Call ID: 8c5f28a7-90c3-413e-b222-e5551132317d
  Args:
    target: Charles_Hepburn-Stuart-Forbes-Trefusis_21st_Baron_Clinton
    source: Fenella_Hepburn-Stuart-Forbes-Trefusis
    relation: :isDaughterOf
  AssignClass (78cbed79-9cf5-4038-94a9-67cc1631bb85)
 Call ID: 78cbed79-9cf5-4038-94a9-67cc1631bb85
  Args:
    type: :Man
    source: Philip_Mountbatten
  Finish (63f0aff2-4114-4b52-a21d-d7908b18bd28)
 Call ID: 63f0aff2-4114-4b52-a21d-d7908b18bd28
  Args: