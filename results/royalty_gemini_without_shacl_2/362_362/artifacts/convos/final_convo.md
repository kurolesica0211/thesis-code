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
Don Alessandro Torlonia, 5th Prince of Civitella-Cesi (7 December 1911 – 1 May/12 May 1986) was an Italian banking heir and a member of the House of Torlonia.
About

Born in Rome on 7 December 1911, Torlonia was the son of Marino Torlonia, 4th Prince di Civitella-Cesi and his American wife, Mary Elsie Moore.
Don Alessandro's youngest sister was Donna Marina Torlonia di Civitella-Cesi, grandmother of the American actress Brooke Shields.
In 1941, when his mother was dying in New York City, Torlonia took a high speed boat from Portugal and was arrested in error by FBI, thinking he was an enemy of the state and taken to Ellis Island.
Not to be confused with his cousin with the same name, Alessandro Torlonia (1925–2017), Prince of Fucino and Prince assistant to the papal throne, head of another branch of the family.
In the 1980s, this cousin Torlonia held the title as the "richest man in Rome", as he was the heir to a banking fortune and owner of the famous Torlonia Collection of ancient art.
He died in the Palazzo Nuñez-Torlonia, Rome, in 1986.
Marriage and children

On 14 January 1935, Don Alessandro morganatically married in Rome the Infanta Beatriz of Spain (1909–2002), a daughter of King Alfonso XIII of Spain and of Princess Victoria Eugenie of Battenberg.



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
  AssignClass (43aa48cf-76b3-4237-b352-a185e5b98045)
 Call ID: 43aa48cf-76b3-4237-b352-a185e5b98045
  Args:
    source: Alessandro_Torlonia_5th_Prince_of_Civitella-Cesi
    type: :Man
  AssignClass (8de90f72-fb55-4882-aaf2-34830807c9cc)
 Call ID: 8de90f72-fb55-4882-aaf2-34830807c9cc
  Args:
    type: :Person
    source: Alessandro_Torlonia_5th_Prince_of_Civitella-Cesi
  AddLiteral (8cf2d118-067b-4dd0-8c4c-63cbfa657b86)
 Call ID: 8cf2d118-067b-4dd0-8c4c-63cbfa657b86
  Args:
    literal_type: xsd:integer
    literal_value: 1911
    source: Alessandro_Torlonia_5th_Prince_of_Civitella-Cesi
    relation: :hasBirthYear
  AddLiteral (1da6b51c-33b6-4179-b191-a6d33d3324d1)
 Call ID: 1da6b51c-33b6-4179-b191-a6d33d3324d1
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: Alessandro_Torlonia_5th_Prince_of_Civitella-Cesi
    literal_value: 1986
  AssignClass (88b19948-039c-47ae-9e61-9d28e0d6d08a)
 Call ID: 88b19948-039c-47ae-9e61-9d28e0d6d08a
  Args:
    source: Marino_Torlonia_4th_Prince_di_Civitella-Cesi
    type: :Man
  AssignClass (ed648f6b-b926-46e6-a94c-aed43dd4b17d)
 Call ID: ed648f6b-b926-46e6-a94c-aed43dd4b17d
  Args:
    type: :Person
    source: Marino_Torlonia_4th_Prince_di_Civitella-Cesi
  AddTriple (847224b6-db68-4ee1-847f-e3d7d209b143)
 Call ID: 847224b6-db68-4ee1-847f-e3d7d209b143
  Args:
    relation: :hasFather
    target: Marino_Torlonia_4th_Prince_di_Civitella-Cesi
    source: Alessandro_Torlonia_5th_Prince_of_Civitella-Cesi
  AssignClass (b261d465-8a24-4023-a8b4-21dfe2576303)
 Call ID: b261d465-8a24-4023-a8b4-21dfe2576303
  Args:
    type: :Woman
    source: Mary_Elsie_Moore
  AssignClass (f5618261-9736-46db-834c-c4f0851679f5)
 Call ID: f5618261-9736-46db-834c-c4f0851679f5
  Args:
    type: :Person
    source: Mary_Elsie_Moore
  AddTriple (459e831e-88a3-4d46-9df2-34dba1fa86a4)
 Call ID: 459e831e-88a3-4d46-9df2-34dba1fa86a4
  Args:
    target: Mary_Elsie_Moore
    source: Alessandro_Torlonia_5th_Prince_of_Civitella-Cesi
    relation: :hasMother
  AssignClass (2ca603b0-5777-4a94-bf92-c78ba6ce4a3d)
 Call ID: 2ca603b0-5777-4a94-bf92-c78ba6ce4a3d
  Args:
    source: Marina_Torlonia_di_Civitella-Cesi
    type: :Woman
  AssignClass (b0d3742a-ee80-4fe9-a54e-c7b1200a1e53)
 Call ID: b0d3742a-ee80-4fe9-a54e-c7b1200a1e53
  Args:
    source: Marina_Torlonia_di_Civitella-Cesi
    type: :Person
  AddTriple (44803835-129b-4e4c-95b1-7f52e2b2d530)
 Call ID: 44803835-129b-4e4c-95b1-7f52e2b2d530
  Args:
    target: Marina_Torlonia_di_Civitella-Cesi
    source: Alessandro_Torlonia_5th_Prince_of_Civitella-Cesi
    relation: :hasSister
  AssignClass (49a07db3-9657-475c-a017-bf96d676f074)
 Call ID: 49a07db3-9657-475c-a017-bf96d676f074
  Args:
    type: :Woman
    source: Beatriz_of_Spain
  AssignClass (92650118-8beb-490e-bb78-b6ae75d15452)
 Call ID: 92650118-8beb-490e-bb78-b6ae75d15452
  Args:
    type: :Person
    source: Beatriz_of_Spain
  AddTriple (5602414a-845c-4741-ba90-a77511c76e91)
 Call ID: 5602414a-845c-4741-ba90-a77511c76e91
  Args:
    source: Alessandro_Torlonia_5th_Prince_of_Civitella-Cesi
    target: Beatriz_of_Spain
    relation: :hasRelation
  AddLiteral (3d9b5636-9c44-4170-9736-bcaff8574e98)
 Call ID: 3d9b5636-9c44-4170-9736-bcaff8574e98
  Args:
    literal_value: 1935
    source: Alessandro_Torlonia_5th_Prince_of_Civitella-Cesi
    relation: :hasMarriageYear
    literal_type: xsd:integer
  AssignClass (a77d0bcf-ea53-4491-9504-90d8dff37ffa)
 Call ID: a77d0bcf-ea53-4491-9504-90d8dff37ffa
  Args:
    type: :Man
    source: Alfonso_XIII_of_Spain
  AssignClass (720a8ba5-7bce-4b14-ae27-943879b7dc6d)
 Call ID: 720a8ba5-7bce-4b14-ae27-943879b7dc6d
  Args:
    type: :Person
    source: Alfonso_XIII_of_Spain
  AddTriple (71b1b623-c15e-486c-a6c9-f4b954318720)
 Call ID: 71b1b623-c15e-486c-a6c9-f4b954318720
  Args:
    target: Alfonso_XIII_of_Spain
    source: Beatriz_of_Spain
    relation: :hasFather
  AssignClass (feb20b07-894e-49c3-981c-ce85f9ad1197)
 Call ID: feb20b07-894e-49c3-981c-ce85f9ad1197
  Args:
    source: Victoria_Eugenie_of_Battenberg
    type: :Woman
  AssignClass (e437a298-c56d-4d6d-98ea-2dba8e19d84b)
 Call ID: e437a298-c56d-4d6d-98ea-2dba8e19d84b
  Args:
    source: Victoria_Eugenie_of_Battenberg
    type: :Person
  AddTriple (6646b6b1-8f3c-4709-898f-85d22637e1df)
 Call ID: 6646b6b1-8f3c-4709-898f-85d22637e1df
  Args:
    source: Beatriz_of_Spain
    target: Victoria_Eugenie_of_Battenberg
    relation: :hasMother
  Finish (28479e73-eba9-4920-bab0-c9ef7a6348fd)
 Call ID: 28479e73-eba9-4920-bab0-c9ef7a6348fd
  Args: