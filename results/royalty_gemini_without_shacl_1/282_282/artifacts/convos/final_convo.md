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
Fergus Michael Claude Bowes-Lyon, 17th and 4th Earl of Strathmore and Kinghorne (31 December 1928 – 19 August 1987) was a British landowner and peer.
He was a nephew of Queen Elizabeth the Queen Mother, thus a first cousin of Queen Elizabeth II.
Early life and family

Born on 31 December 1928, Strathmore was the eldest son of Michael Claude Hamilton Bowes-Lyon and Elizabeth Margaret Cator (1899–1959).
His paternal grandparents were the 14th Earl and Countess of Strathmore and Kinghorne, and his maternal grandfather was John Cator, Conservative MP for Huntingdon.
In 1953, during the coronation of his cousin, Queen Elizabeth II, he was one of many servicemen lining the processional route.
Strathmore, then Captain Fergus Bowes-Lyon, married Mary Pamela McCorquodale (31 May 1932 – 28 April 2025) at St Margaret's, Westminster, on 10 April 1956 in a ceremony attended by his cousin, the Queen.
He was succeeded by his son, Michael.



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
  AssignClass (0bc8cb3c-28a9-4af8-8197-5762e0ca0922)
 Call ID: 0bc8cb3c-28a9-4af8-8197-5762e0ca0922
  Args:
    source: Fergus_Bowes-Lyon
    type: :Man
  AssignClass (edfe6f3c-48f9-4f3d-a8a4-8a01a16c59ee)
 Call ID: edfe6f3c-48f9-4f3d-a8a4-8a01a16c59ee
  Args:
    source: Fergus_Bowes-Lyon
    type: :Person
  AddLiteral (8973c162-5545-4afc-b4f5-4058c5a9c222)
 Call ID: 8973c162-5545-4afc-b4f5-4058c5a9c222
  Args:
    literal_value: 1928
    literal_type: xsd:integer
    source: Fergus_Bowes-Lyon
    relation: :hasBirthYear
  AddLiteral (ba4f52b0-aab8-45b4-bc56-ac49b120b079)
 Call ID: ba4f52b0-aab8-45b4-bc56-ac49b120b079
  Args:
    source: Fergus_Bowes-Lyon
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 1987
  AssignClass (3e8a0d35-b187-4fdb-b2bd-907b319f9502)
 Call ID: 3e8a0d35-b187-4fdb-b2bd-907b319f9502
  Args:
    type: :Man
    source: Michael_Claude_Hamilton_Bowes-Lyon
  AssignClass (8326f38d-fb7a-4d16-976b-879e3221d596)
 Call ID: 8326f38d-fb7a-4d16-976b-879e3221d596
  Args:
    type: :Person
    source: Michael_Claude_Hamilton_Bowes-Lyon
  AssignClass (582661b4-cb83-44d5-8f48-6a6c9c6eda50)
 Call ID: 582661b4-cb83-44d5-8f48-6a6c9c6eda50
  Args:
    type: :Woman
    source: Elizabeth_Margaret_Cator
  AssignClass (85642c66-f7cd-415e-964e-b83c3e9936c0)
 Call ID: 85642c66-f7cd-415e-964e-b83c3e9936c0
  Args:
    type: :Person
    source: Elizabeth_Margaret_Cator
  AddLiteral (f0477f90-8012-4e8f-834b-6b801ad5ccf3)
 Call ID: f0477f90-8012-4e8f-834b-6b801ad5ccf3
  Args:
    relation: :hasBirthYear
    source: Elizabeth_Margaret_Cator
    literal_type: xsd:integer
    literal_value: 1899
  AddLiteral (abeec9f3-12d7-4f8c-b36b-f0306341d893)
 Call ID: abeec9f3-12d7-4f8c-b36b-f0306341d893
  Args:
    source: Elizabeth_Margaret_Cator
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 1959
  AddTriple (810423ca-451b-4823-9544-e3315a6e0f2b)
 Call ID: 810423ca-451b-4823-9544-e3315a6e0f2b
  Args:
    target: Michael_Claude_Hamilton_Bowes-Lyon
    source: Fergus_Bowes-Lyon
    relation: :hasFather
  AddTriple (d34f5944-6cc5-4350-93a4-acfee8a61cf2)
 Call ID: d34f5944-6cc5-4350-93a4-acfee8a61cf2
  Args:
    source: Fergus_Bowes-Lyon
    relation: :hasMother
    target: Elizabeth_Margaret_Cator
  AssignClass (f6d62bb3-8000-40e7-a372-a72cfa9dfc9c)
 Call ID: f6d62bb3-8000-40e7-a372-a72cfa9dfc9c
  Args:
    type: :Woman
    source: Mary_Pamela_McCorquodale
  AssignClass (2cea7ee6-4442-46bd-bdb6-b3e4192f2437)
 Call ID: 2cea7ee6-4442-46bd-bdb6-b3e4192f2437
  Args:
    source: Mary_Pamela_McCorquodale
    type: :Person
  AddLiteral (03315c96-017e-4e5c-937e-074bafcc880e)
 Call ID: 03315c96-017e-4e5c-937e-074bafcc880e
  Args:
    source: Mary_Pamela_McCorquodale
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1932
  AddLiteral (f9e51597-f39b-4510-a527-07e2e0cb21bf)
 Call ID: f9e51597-f39b-4510-a527-07e2e0cb21bf
  Args:
    literal_value: 2025
    literal_type: xsd:integer
    source: Mary_Pamela_McCorquodale
    relation: :hasDeathYear
  AddLiteral (2ef351b1-741a-44e0-b2cc-10739e1b022a)
 Call ID: 2ef351b1-741a-44e0-b2cc-10739e1b022a
  Args:
    literal_value: 1956
    literal_type: xsd:integer
    source: Fergus_Bowes-Lyon
    relation: :hasMarriageYear
  AddTriple (564e4f31-8a53-442d-9d77-c1875d1445e9)
 Call ID: 564e4f31-8a53-442d-9d77-c1875d1445e9
  Args:
    relation: :hasRelation
    source: Fergus_Bowes-Lyon
    target: Mary_Pamela_McCorquodale
  AssignClass (ef726261-4acf-4854-a90e-1e54b728a259)
 Call ID: ef726261-4acf-4854-a90e-1e54b728a259
  Args:
    type: :Man
    source: Michael_Bowes-Lyon
  AssignClass (535947ec-b538-4c9d-844f-5dd5489a55aa)
 Call ID: 535947ec-b538-4c9d-844f-5dd5489a55aa
  Args:
    type: :Person
    source: Michael_Bowes-Lyon
  AddTriple (42729f30-94a5-451b-af14-3b8a4c9ff89f)
 Call ID: 42729f30-94a5-451b-af14-3b8a4c9ff89f
  Args:
    target: Fergus_Bowes-Lyon
    relation: :isSonOf
    source: Michael_Bowes-Lyon
  AssignClass (7d74b81a-c7b0-48b7-b3f0-daca5d1c5d40)
 Call ID: 7d74b81a-c7b0-48b7-b3f0-daca5d1c5d40
  Args:
    source: John_Cator
    type: :Man
  AssignClass (dbc542b8-b2a8-444a-a9fe-2d4de7d4f17c)
 Call ID: dbc542b8-b2a8-444a-a9fe-2d4de7d4f17c
  Args:
    source: John_Cator
    type: :Person
  AddTriple (671e2ff2-ccd8-4a8c-bab8-00259c8468db)
 Call ID: 671e2ff2-ccd8-4a8c-bab8-00259c8468db
  Args:
    target: Elizabeth_Margaret_Cator
    relation: :isFatherOf
    source: John_Cator
  Finish (c16a745e-0191-4d8f-a7c1-aca38ac82b7f)
 Call ID: c16a745e-0191-4d8f-a7c1-aca38ac82b7f
  Args: