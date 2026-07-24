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
Lady Davina Elizabeth Alice Benedikte Windsor (born 19 November 1977) is a member of the British royal family, and is the elder daughter of the Duke and Duchess of Gloucester.
She was known as Lady Davina Lewis between 2004 and 2018, during her marriage to Gary Lewis.
Early life and education

Davina Elizabeth Alice Benedikte Windsor was born on 19 November 1977 at St Mary's Hospital, London, the second child of Prince Richard, Duke of Gloucester and Birgitte, Duchess of Gloucester.
Her godparents are Captain Mark Phillips, the Duke of Buccleuch, Elisabeth, Lady Camoys, Susan Wigley, Roger Wellesley Smith and Caroline, Baroness Rosenørn-Lehn.
Lady Davina grew up in Kensington Palace.
Marriage and children

On 31 July 2004, Davina married Gary Christie Lewis (born 15 August 1970), a Māori.
Lewis is also the first person of known Māori descent to marry a member of the royal family, or to marry the daughter of a British prince.
As she is a legitimate descendant in the male line of George V and in line to the British throne, the Royal Marriages Act 1772 required that Royal Assent to the wedding be obtained in advance for the marriage to be legal and the descendants thereof to inherit rights of succession to the thrones of the Commonwealth realms, including that of New Zealand.
The wedding took place on 31 July 2004 at the private chapel of Kensington Palace, Davina's childhood home.
Apart from the Duke and Duchess of Gloucester and the bride's siblings, no other members of the royal family were present at the wedding; only close friends and family were involved.
Davina and her former husband have a daughter, Senna Kowhai, who was born on 22 June 2010 and a son, Tāne Mahuta, who was born 25 May 2012.
Davina was also stepmother to Lewis's son from a previous relationship, Ari (born 1992).
Davina does not carry out official functions but does attend family events including royal weddings.
Davina and Gary Lewis were invited to attend the Queen's reception for members of the New Zealand All Blacks at Buckingham Palace in 2005.
She and her then husband also attended Prince William's wedding in 2011.



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
  AssignClass (453bf8d2-7679-4f5c-b86d-f2e9fb919e77)
 Call ID: 453bf8d2-7679-4f5c-b86d-f2e9fb919e77
  Args:
    type: :Woman
    source: :Davina_Windsor
  AssignClass (0640cd48-3c96-488d-87d8-5e7bfed60701)
 Call ID: 0640cd48-3c96-488d-87d8-5e7bfed60701
  Args:
    type: :Person
    source: :Davina_Windsor
  AddLiteral (a0e9be5a-50fe-4277-909b-cf31eb223dab)
 Call ID: a0e9be5a-50fe-4277-909b-cf31eb223dab
  Args:
    literal_value: 1977
    source: :Davina_Windsor
    relation: :hasBirthYear
    literal_type: xsd:integer
  AssignClass (38cb9e7e-2297-41c8-9866-bceef0c635fd)
 Call ID: 38cb9e7e-2297-41c8-9866-bceef0c635fd
  Args:
    type: :Man
    source: :Prince_Richard_Duke_of_Gloucester
  AssignClass (66a44b9f-e561-40de-8bb2-3621a00b89a6)
 Call ID: 66a44b9f-e561-40de-8bb2-3621a00b89a6
  Args:
    type: :Person
    source: :Prince_Richard_Duke_of_Gloucester
  AssignClass (49493fc9-9b3a-4ae0-8216-8cf9b6a0e934)
 Call ID: 49493fc9-9b3a-4ae0-8216-8cf9b6a0e934
  Args:
    type: :Woman
    source: :Birgitte_Duchess_of_Gloucester
  AssignClass (4b5277d8-96bf-47c6-bbc2-48b7d4fbaa0b)
 Call ID: 4b5277d8-96bf-47c6-bbc2-48b7d4fbaa0b
  Args:
    type: :Person
    source: :Birgitte_Duchess_of_Gloucester
  AddTriple (97e342c5-3853-4f5f-ac71-5bf8ffaa0f58)
 Call ID: 97e342c5-3853-4f5f-ac71-5bf8ffaa0f58
  Args:
    target: :Prince_Richard_Duke_of_Gloucester
    source: :Davina_Windsor
    relation: :hasFather
  AddTriple (088c7965-0b25-4085-af3b-0e222291c1a0)
 Call ID: 088c7965-0b25-4085-af3b-0e222291c1a0
  Args:
    target: :Birgitte_Duchess_of_Gloucester
    source: :Davina_Windsor
    relation: :hasMother
  AssignClass (23c7a5fa-178d-483d-a570-a86af8c03880)
 Call ID: 23c7a5fa-178d-483d-a570-a86af8c03880
  Args:
    type: :Man
    source: :Gary_Christie_Lewis
  AssignClass (b3b8849d-73a3-4192-9899-597ec7035b3c)
 Call ID: b3b8849d-73a3-4192-9899-597ec7035b3c
  Args:
    type: :Person
    source: :Gary_Christie_Lewis
  AddLiteral (f540002f-2e09-4d64-8cae-92206442c7eb)
 Call ID: f540002f-2e09-4d64-8cae-92206442c7eb
  Args:
    source: :Gary_Christie_Lewis
    literal_value: 1970
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (2764bf84-f463-4a55-b39f-1a7f31284041)
 Call ID: 2764bf84-f463-4a55-b39f-1a7f31284041
  Args:
    relation: :hasMarriageYear
    literal_type: xsd:integer
    literal_value: 2004
    source: :Davina_Windsor
  AddTriple (8e328bb5-3127-486c-a742-bd1ea2eb9560)
 Call ID: 8e328bb5-3127-486c-a742-bd1ea2eb9560
  Args:
    target: :Gary_Christie_Lewis
    source: :Davina_Windsor
    relation: :hasRelation
  AssignClass (3be23ca9-26bd-4f5d-8431-c774e0334ec4)
 Call ID: 3be23ca9-26bd-4f5d-8431-c774e0334ec4
  Args:
    type: :Woman
    source: :Senna_Kowhai
  AssignClass (63e7ce2c-1f80-4dfa-85cc-1623212c2b19)
 Call ID: 63e7ce2c-1f80-4dfa-85cc-1623212c2b19
  Args:
    type: :Person
    source: :Senna_Kowhai
  AddTriple (bd322ac8-fbc8-4f1d-83fb-5da28c599b98)
 Call ID: bd322ac8-fbc8-4f1d-83fb-5da28c599b98
  Args:
    relation: :isChildOf
    target: :Davina_Windsor
    source: :Senna_Kowhai
  AddTriple (49e4b3c2-9052-4ea3-8476-d25d9f9aef8a)
 Call ID: 49e4b3c2-9052-4ea3-8476-d25d9f9aef8a
  Args:
    source: :Senna_Kowhai
    target: :Gary_Christie_Lewis
    relation: :isChildOf
  AssignClass (ee3f23c9-ce1f-4973-a195-136e6bce6e18)
 Call ID: ee3f23c9-ce1f-4973-a195-136e6bce6e18
  Args:
    type: :Man
    source: :Tane_Mahuta
  AssignClass (b0c9604d-6383-4a17-b622-44c10e230aeb)
 Call ID: b0c9604d-6383-4a17-b622-44c10e230aeb
  Args:
    type: :Person
    source: :Tane_Mahuta
  AddTriple (a84e1239-166d-46fb-b536-a080cbe86c70)
 Call ID: a84e1239-166d-46fb-b536-a080cbe86c70
  Args:
    target: :Davina_Windsor
    source: :Tane_Mahuta
    relation: :isChildOf
  AddTriple (9fecf215-4c28-4284-99c1-4e6ec6ab9c37)
 Call ID: 9fecf215-4c28-4284-99c1-4e6ec6ab9c37
  Args:
    relation: :isChildOf
    target: :Gary_Christie_Lewis
    source: :Tane_Mahuta
  AssignClass (38545e24-59e5-4a86-8c57-855cabfeb43a)
 Call ID: 38545e24-59e5-4a86-8c57-855cabfeb43a
  Args:
    type: :Man
    source: :Ari
  AssignClass (89d73f13-9431-4ea1-b894-f026c9cdac1c)
 Call ID: 89d73f13-9431-4ea1-b894-f026c9cdac1c
  Args:
    type: :Person
    source: :Ari
  AddLiteral (4219aa12-533a-4fc1-98f4-cac511b3f1c1)
 Call ID: 4219aa12-533a-4fc1-98f4-cac511b3f1c1
  Args:
    literal_value: 1992
    source: :Ari
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddTriple (fe84ee5c-b1e5-4bf3-85c9-a2178260bdfd)
 Call ID: fe84ee5c-b1e5-4bf3-85c9-a2178260bdfd
  Args:
    relation: :isChildOf
    target: :Gary_Christie_Lewis
    source: :Ari
  Finish (54eb4561-3f5c-4a54-b931-09fa3e8c9dc2)
 Call ID: 54eb4561-3f5c-4a54-b931-09fa3e8c9dc2
  Args: