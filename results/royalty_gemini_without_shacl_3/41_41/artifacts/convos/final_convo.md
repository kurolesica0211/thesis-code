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
Infante Alfonso of Spain, Prince of the Two Sicilies, Duke of Calabria (30 November 1901 – 3 February 1964) was one of two claimants to the title of the head of the House of Bourbon-Two Sicilies from 1960 until his death in 1964.
He was the son of Prince Carlos of Bourbon-Two Sicilies and María de las Mercedes, Princess of Asturias.
He was born and died in Madrid, Spain.
Alfonso's mother was María de las Mercedes, Princess of Asturias, but she died in childbirth in 1904.
Alfonso XIII, King of Spain, was unmarried at the time so as the Princess of the Asturias's eldest son, the young infante became heir presumptive to the Spanish crown, though, unlike his mother, he never held the title of Prince of Asturias.
He was heir presumptive until the birth of his cousin, Alfonso, to Alfonso XIII and Queen Victoria Eugenie in 1907.
Marriage and issue

Alfonso married Princess Alice of Bourbon-Parma (1917–2017), his second cousin, daughter of Elias, Duke of Parma and Piacenza, and Archduchess Maria Anna of Austria, on 16 April 1936 in Vienna, Austria.



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
  AssignClass (0dcb47f5-2052-4a5f-bcf9-6a80792ddabe)
 Call ID: 0dcb47f5-2052-4a5f-bcf9-6a80792ddabe
  Args:
    source: Alfonso_of_Spain
    type: :Man
  AssignClass (f41eccc6-e3e5-4f2b-a931-0d807989454e)
 Call ID: f41eccc6-e3e5-4f2b-a931-0d807989454e
  Args:
    source: Alfonso_of_Spain
    type: :Person
  AddLiteral (2590a946-ce37-407d-af80-43a1a1a09f0e)
 Call ID: 2590a946-ce37-407d-af80-43a1a1a09f0e
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1901
    source: Alfonso_of_Spain
  AddLiteral (a2fb73ad-96e6-4eaa-86cc-1221fe5be9f3)
 Call ID: a2fb73ad-96e6-4eaa-86cc-1221fe5be9f3
  Args:
    source: Alfonso_of_Spain
    literal_value: 1964
    relation: :hasDeathYear
    literal_type: xsd:integer
  AssignClass (a97e60e2-a0c1-41c8-8fd9-3b4058308439)
 Call ID: a97e60e2-a0c1-41c8-8fd9-3b4058308439
  Args:
    source: Carlos_of_Bourbon-Two_Sicilies
    type: :Man
  AssignClass (b6b56005-32a4-4480-a8c0-dbee71e21c8a)
 Call ID: b6b56005-32a4-4480-a8c0-dbee71e21c8a
  Args:
    type: :Person
    source: Carlos_of_Bourbon-Two_Sicilies
  AssignClass (338a2b82-b77e-4e37-b3e7-a28a2bd3d162)
 Call ID: 338a2b82-b77e-4e37-b3e7-a28a2bd3d162
  Args:
    type: :Woman
    source: Maria_de_las_Mercedes
  AssignClass (9e19d8dc-216c-44b1-b0e2-e2ed06325996)
 Call ID: 9e19d8dc-216c-44b1-b0e2-e2ed06325996
  Args:
    source: Maria_de_las_Mercedes
    type: :Person
  AddTriple (14f7a41e-3dee-4868-b2ea-9cfe88b9ddb4)
 Call ID: 14f7a41e-3dee-4868-b2ea-9cfe88b9ddb4
  Args:
    relation: :hasFather
    source: Alfonso_of_Spain
    target: Carlos_of_Bourbon-Two_Sicilies
  AddTriple (aecbe52f-ac1a-4fda-bbb5-de0a3f6fa08d)
 Call ID: aecbe52f-ac1a-4fda-bbb5-de0a3f6fa08d
  Args:
    target: Maria_de_las_Mercedes
    source: Alfonso_of_Spain
    relation: :hasMother
  AssignClass (1937ee1b-8d65-4b43-af87-3e4b47d9efec)
 Call ID: 1937ee1b-8d65-4b43-af87-3e4b47d9efec
  Args:
    type: :Woman
    source: Alice_of_Bourbon-Parma
  AssignClass (4bc8a990-805b-4b60-970a-1ec4f7e4548c)
 Call ID: 4bc8a990-805b-4b60-970a-1ec4f7e4548c
  Args:
    type: :Person
    source: Alice_of_Bourbon-Parma
  AddLiteral (7ce4f362-69af-458d-bb03-937cbb800563)
 Call ID: 7ce4f362-69af-458d-bb03-937cbb800563
  Args:
    literal_value: 1936
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: Alfonso_of_Spain
  AddTriple (326e52b0-6630-4d2b-84f8-f839d5faa3da)
 Call ID: 326e52b0-6630-4d2b-84f8-f839d5faa3da
  Args:
    source: Alfonso_of_Spain
    target: Alice_of_Bourbon-Parma
    relation: :hasRelation
  AssignClass (e90f84ad-fd57-4b06-b780-0597e3138e46)
 Call ID: e90f84ad-fd57-4b06-b780-0597e3138e46
  Args:
    type: :Man
    source: Elias_of_Parma
  AssignClass (3ba92087-2a6a-4a89-ad93-6143ffe844ce)
 Call ID: 3ba92087-2a6a-4a89-ad93-6143ffe844ce
  Args:
    type: :Person
    source: Elias_of_Parma
  AssignClass (7020b4d4-3bbb-4691-8bb4-258e7c6934ae)
 Call ID: 7020b4d4-3bbb-4691-8bb4-258e7c6934ae
  Args:
    source: Maria_Anna_of_Austria
    type: :Woman
  AssignClass (ce6ab9f7-688f-4a37-949f-d57834438fbe)
 Call ID: ce6ab9f7-688f-4a37-949f-d57834438fbe
  Args:
    source: Maria_Anna_of_Austria
    type: :Person
  AddTriple (0ac9e6be-fe05-4649-a6a0-18922065fcf2)
 Call ID: 0ac9e6be-fe05-4649-a6a0-18922065fcf2
  Args:
    relation: :hasFather
    target: Elias_of_Parma
    source: Alice_of_Bourbon-Parma
  AddTriple (308adb29-1eae-4892-a434-4d76348c55fc)
 Call ID: 308adb29-1eae-4892-a434-4d76348c55fc
  Args:
    relation: :hasMother
    source: Alice_of_Bourbon-Parma
    target: Maria_Anna_of_Austria
  AssignClass (3bb7445b-d8bf-496c-92ca-9aea4a7cbc6f)
 Call ID: 3bb7445b-d8bf-496c-92ca-9aea4a7cbc6f
  Args:
    type: :Man
    source: Alfonso_XIII
  AssignClass (12727ab3-f154-40dc-aa73-fab39bb29429)
 Call ID: 12727ab3-f154-40dc-aa73-fab39bb29429
  Args:
    source: Alfonso_XIII
    type: :Person
  AssignClass (4e2766cd-00d3-47d4-8a64-eb502379be23)
 Call ID: 4e2766cd-00d3-47d4-8a64-eb502379be23
  Args:
    type: :Woman
    source: Victoria_Eugenie
  AssignClass (5c3bf54e-6192-40f3-a965-47a86a7b17f7)
 Call ID: 5c3bf54e-6192-40f3-a965-47a86a7b17f7
  Args:
    type: :Person
    source: Victoria_Eugenie
  AssignClass (2e926278-8141-4f86-bde7-33571eed0faa)
 Call ID: 2e926278-8141-4f86-bde7-33571eed0faa
  Args:
    source: Alfonso_cousin
    type: :Man
  AssignClass (7e9bfa3b-30b3-4288-b54b-22ba1ee0fd3e)
 Call ID: 7e9bfa3b-30b3-4288-b54b-22ba1ee0fd3e
  Args:
    source: Alfonso_cousin
    type: :Person
  AddTriple (329e500a-e34d-4d81-ab8e-f36f869db97a)
 Call ID: 329e500a-e34d-4d81-ab8e-f36f869db97a
  Args:
    target: Alfonso_XIII
    source: Alfonso_cousin
    relation: :hasFather
  AddTriple (b0b6b939-8194-44a1-88ef-8467975a0eba)
 Call ID: b0b6b939-8194-44a1-88ef-8467975a0eba
  Args:
    source: Alfonso_cousin
    target: Victoria_Eugenie
    relation: :hasMother
  Finish (d49b4179-e84b-413b-ac1c-4153a2ac7633)
 Call ID: d49b4179-e84b-413b-ac1c-4153a2ac7633
  Args: