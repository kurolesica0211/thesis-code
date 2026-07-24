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
  AssignClass (59632cb7-63d4-4bd1-864c-977efb94ee58)
 Call ID: 59632cb7-63d4-4bd1-864c-977efb94ee58
  Args:
    source: :Alfonso_of_Spain
    type: :Man
  AssignClass (86dcc07d-c6af-4689-a8cf-31952f4ce81a)
 Call ID: 86dcc07d-c6af-4689-a8cf-31952f4ce81a
  Args:
    type: :Person
    source: :Alfonso_of_Spain
  AddLiteral (7f2a939b-6e04-49a8-8388-3d0a911861f5)
 Call ID: 7f2a939b-6e04-49a8-8388-3d0a911861f5
  Args:
    literal_value: 1901
    literal_type: xsd:integer
    source: :Alfonso_of_Spain
    relation: :hasBirthYear
  AddLiteral (4160f6f3-31af-4186-b612-55cef8ef463e)
 Call ID: 4160f6f3-31af-4186-b612-55cef8ef463e
  Args:
    relation: :hasDeathYear
    literal_value: 1964
    literal_type: xsd:integer
    source: :Alfonso_of_Spain
  AssignClass (6b9e17d5-e952-4053-a69d-6b92495c1aac)
 Call ID: 6b9e17d5-e952-4053-a69d-6b92495c1aac
  Args:
    source: :Carlos_of_Bourbon-Two_Sicilies
    type: :Man
  AssignClass (47405a70-dbb1-4dd9-8e6f-3d18e1da5a4f)
 Call ID: 47405a70-dbb1-4dd9-8e6f-3d18e1da5a4f
  Args:
    source: :Carlos_of_Bourbon-Two_Sicilies
    type: :Person
  AssignClass (43dbf106-e151-4274-a610-508cf48c661a)
 Call ID: 43dbf106-e151-4274-a610-508cf48c661a
  Args:
    source: :Maria_de_las_Mercedes
    type: :Woman
  AssignClass (50d080e5-e4e2-43aa-bc44-18ec5429704e)
 Call ID: 50d080e5-e4e2-43aa-bc44-18ec5429704e
  Args:
    source: :Maria_de_las_Mercedes
    type: :Person
  AddTriple (a8b3bca4-f4d5-4571-936e-071cae614994)
 Call ID: a8b3bca4-f4d5-4571-936e-071cae614994
  Args:
    relation: :hasFather
    source: :Alfonso_of_Spain
    target: :Carlos_of_Bourbon-Two_Sicilies
  AddTriple (80e34bac-4d6a-4a1f-844c-3c7ac98611c1)
 Call ID: 80e34bac-4d6a-4a1f-844c-3c7ac98611c1
  Args:
    source: :Alfonso_of_Spain
    target: :Maria_de_las_Mercedes
    relation: :hasMother
  AssignClass (50fa3ff4-0742-4e21-826e-54f80f3721ba)
 Call ID: 50fa3ff4-0742-4e21-826e-54f80f3721ba
  Args:
    type: :Woman
    source: :Alice_of_Bourbon-Parma
  AssignClass (83ddd676-7acb-425f-8f22-7b22e3f59c49)
 Call ID: 83ddd676-7acb-425f-8f22-7b22e3f59c49
  Args:
    source: :Alice_of_Bourbon-Parma
    type: :Person
  AddTriple (97ac22e9-d6bf-432e-a652-ec200becb793)
 Call ID: 97ac22e9-d6bf-432e-a652-ec200becb793
  Args:
    target: :Alice_of_Bourbon-Parma
    source: :Alfonso_of_Spain
    relation: :hasRelation
  AddLiteral (59b8faa2-1444-4800-85b4-9b622934174a)
 Call ID: 59b8faa2-1444-4800-85b4-9b622934174a
  Args:
    relation: :hasMarriageYear
    source: :Alfonso_of_Spain
    literal_value: 1936
    literal_type: xsd:integer
  AssignClass (88427265-7bd7-4cbf-a3ba-8f8e20d30824)
 Call ID: 88427265-7bd7-4cbf-a3ba-8f8e20d30824
  Args:
    type: :Man
    source: :Elias_of_Parma
  AssignClass (085f07d1-f4c8-4140-9b60-ebbad1233c75)
 Call ID: 085f07d1-f4c8-4140-9b60-ebbad1233c75
  Args:
    source: :Elias_of_Parma
    type: :Person
  AssignClass (8c17627c-52d8-41a2-a536-8bffac27b4b7)
 Call ID: 8c17627c-52d8-41a2-a536-8bffac27b4b7
  Args:
    type: :Woman
    source: :Maria_Anna_of_Austria
  AssignClass (a32a0ba7-b3d5-4874-a7d8-ea537c696007)
 Call ID: a32a0ba7-b3d5-4874-a7d8-ea537c696007
  Args:
    type: :Person
    source: :Maria_Anna_of_Austria
  AddTriple (28578969-fe93-47c8-9b91-be9873dad4cc)
 Call ID: 28578969-fe93-47c8-9b91-be9873dad4cc
  Args:
    target: :Elias_of_Parma
    source: :Alice_of_Bourbon-Parma
    relation: :hasFather
  AddTriple (71d94ca7-3c31-4c13-a349-d364d6bce2a6)
 Call ID: 71d94ca7-3c31-4c13-a349-d364d6bce2a6
  Args:
    relation: :hasMother
    source: :Alice_of_Bourbon-Parma
    target: :Maria_Anna_of_Austria
  AssignClass (2d499a12-c769-4c98-9af7-649abfa033dc)
 Call ID: 2d499a12-c769-4c98-9af7-649abfa033dc
  Args:
    type: :Man
    source: :Alfonso_XIII_of_Spain
  AssignClass (3f78c299-6d67-4fc9-aa25-76046b90341b)
 Call ID: 3f78c299-6d67-4fc9-aa25-76046b90341b
  Args:
    type: :Person
    source: :Alfonso_XIII_of_Spain
  AssignClass (704c261a-7776-4fe8-8f48-5d3039d521a2)
 Call ID: 704c261a-7776-4fe8-8f48-5d3039d521a2
  Args:
    type: :Woman
    source: :Victoria_Eugenie_of_Spain
  AssignClass (e21bef60-06dc-458d-a92a-81754345bbdb)
 Call ID: e21bef60-06dc-458d-a92a-81754345bbdb
  Args:
    source: :Victoria_Eugenie_of_Spain
    type: :Person
  AssignClass (64eeb7bf-cb0f-4698-95cf-51f80f45fa7a)
 Call ID: 64eeb7bf-cb0f-4698-95cf-51f80f45fa7a
  Args:
    type: :Man
    source: :Alfonso_cousin
  AssignClass (55380ac4-8e64-47bb-a62b-f5b1af2a951c)
 Call ID: 55380ac4-8e64-47bb-a62b-f5b1af2a951c
  Args:
    type: :Person
    source: :Alfonso_cousin
  AddTriple (31b001c6-8c58-4abc-a0d7-a9d1ed8cf087)
 Call ID: 31b001c6-8c58-4abc-a0d7-a9d1ed8cf087
  Args:
    target: :Alfonso_XIII_of_Spain
    source: :Alfonso_cousin
    relation: :hasFather
  AddTriple (1ccbd861-3a06-4cc5-8df8-0a6be7ee47d7)
 Call ID: 1ccbd861-3a06-4cc5-8df8-0a6be7ee47d7
  Args:
    source: :Alfonso_cousin
    target: :Victoria_Eugenie_of_Spain
    relation: :hasMother
  Finish (4c44760a-50a4-4561-8dd9-36e119babcec)
 Call ID: 4c44760a-50a4-4561-8dd9-36e119babcec
  Args: