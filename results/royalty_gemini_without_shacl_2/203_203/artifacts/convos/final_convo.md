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
  AssignClass (07a70345-b172-4b3f-9757-0ee5c241311d)
 Call ID: 07a70345-b172-4b3f-9757-0ee5c241311d
  Args:
    source: :Davina_Windsor
    type: :Woman
  AssignClass (10eb07b5-498b-49fb-ba99-33d92a249a44)
 Call ID: 10eb07b5-498b-49fb-ba99-33d92a249a44
  Args:
    source: :Davina_Windsor
    type: :Person
  AddLiteral (b2a14156-828a-41c9-8dc1-60696054d36c)
 Call ID: b2a14156-828a-41c9-8dc1-60696054d36c
  Args:
    literal_value: 1977
    relation: :hasBirthYear
    source: :Davina_Windsor
    literal_type: xsd:integer
  AddLiteral (472ac8b5-6bbf-4a6d-8e23-06fcdbe8254b)
 Call ID: 472ac8b5-6bbf-4a6d-8e23-06fcdbe8254b
  Args:
    literal_value: Lady Davina Lewis
    source: :Davina_Windsor
    literal_type: xsd:string
    relation: :alsoKnownAs
  AssignClass (458382d9-6f7d-4c0e-9618-7515bde8530e)
 Call ID: 458382d9-6f7d-4c0e-9618-7515bde8530e
  Args:
    type: :Man
    source: :Prince_Richard_Duke_of_Gloucester
  AssignClass (3145f89f-1907-42b1-86c2-49f671fb5b13)
 Call ID: 3145f89f-1907-42b1-86c2-49f671fb5b13
  Args:
    source: :Prince_Richard_Duke_of_Gloucester
    type: :Person
  AssignClass (ee554cb3-8bb4-4890-9d0c-545440f16d9a)
 Call ID: ee554cb3-8bb4-4890-9d0c-545440f16d9a
  Args:
    type: :Woman
    source: :Birgitte_Duchess_of_Gloucester
  AssignClass (91a0dcbc-5d73-4ad5-8b5f-db1d618ab3e1)
 Call ID: 91a0dcbc-5d73-4ad5-8b5f-db1d618ab3e1
  Args:
    source: :Birgitte_Duchess_of_Gloucester
    type: :Person
  AddTriple (961e9b58-d1d3-4699-a0b8-a4ea5dd91503)
 Call ID: 961e9b58-d1d3-4699-a0b8-a4ea5dd91503
  Args:
    target: :Davina_Windsor
    source: :Prince_Richard_Duke_of_Gloucester
    relation: :isFatherOf
  AddTriple (65ea7632-f08c-4280-970f-cd31dc7c5cac)
 Call ID: 65ea7632-f08c-4280-970f-cd31dc7c5cac
  Args:
    source: :Birgitte_Duchess_of_Gloucester
    target: :Davina_Windsor
    relation: :isMotherOf
  AssignClass (3fffca44-b640-4ec1-9f08-b9e4e8c75b3c)
 Call ID: 3fffca44-b640-4ec1-9f08-b9e4e8c75b3c
  Args:
    type: :Man
    source: :Gary_Christie_Lewis
  AssignClass (5cd2f9d6-90df-4bf5-866d-527faef87dc1)
 Call ID: 5cd2f9d6-90df-4bf5-866d-527faef87dc1
  Args:
    source: :Gary_Christie_Lewis
    type: :Person
  AddLiteral (f265f3ca-f497-4718-a2db-6d34befe0362)
 Call ID: f265f3ca-f497-4718-a2db-6d34befe0362
  Args:
    literal_value: 1970
    source: :Gary_Christie_Lewis
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (a30585e6-7a7b-4f21-9e75-8fc4fc0124d5)
 Call ID: a30585e6-7a7b-4f21-9e75-8fc4fc0124d5
  Args:
    literal_value: 2004
    relation: :hasMarriageYear
    source: :Davina_Windsor
    literal_type: xsd:integer
  AssignClass (6dfd54d8-5f30-4e6b-9f26-f039fbbfebe0)
 Call ID: 6dfd54d8-5f30-4e6b-9f26-f039fbbfebe0
  Args:
    source: :Senna_Kowhai
    type: :Woman
  AssignClass (7b81b3a4-1b9c-4659-8f95-f17ff0bda25d)
 Call ID: 7b81b3a4-1b9c-4659-8f95-f17ff0bda25d
  Args:
    type: :Person
    source: :Senna_Kowhai
  AddTriple (308b543a-1879-4521-83eb-90c8c7f0b35a)
 Call ID: 308b543a-1879-4521-83eb-90c8c7f0b35a
  Args:
    relation: :isChildOf
    target: :Davina_Windsor
    source: :Senna_Kowhai
  AddTriple (d7422fbe-1275-42ba-b77a-4c9c6e31cffd)
 Call ID: d7422fbe-1275-42ba-b77a-4c9c6e31cffd
  Args:
    target: :Gary_Christie_Lewis
    source: :Senna_Kowhai
    relation: :isChildOf
  AssignClass (cd6a771e-fc27-434b-80e5-9892cd5bf16c)
 Call ID: cd6a771e-fc27-434b-80e5-9892cd5bf16c
  Args:
    type: :Man
    source: :Tane_Mahuta
  AssignClass (94803661-3ea2-4b9d-b592-bd3a4fb15fa2)
 Call ID: 94803661-3ea2-4b9d-b592-bd3a4fb15fa2
  Args:
    type: :Person
    source: :Tane_Mahuta
  AddTriple (e4601f25-a3a7-4f64-888a-de2447a11403)
 Call ID: e4601f25-a3a7-4f64-888a-de2447a11403
  Args:
    relation: :isChildOf
    target: :Davina_Windsor
    source: :Tane_Mahuta
  AddTriple (a82cae93-1d10-4671-9482-c1a04fa7d0f7)
 Call ID: a82cae93-1d10-4671-9482-c1a04fa7d0f7
  Args:
    source: :Tane_Mahuta
    target: :Gary_Christie_Lewis
    relation: :isChildOf
  AssignClass (75c866a8-3ec0-4b10-86d4-c655e215d05c)
 Call ID: 75c866a8-3ec0-4b10-86d4-c655e215d05c
  Args:
    type: :Man
    source: :Ari
  AssignClass (70dfc3c8-4000-4af6-91bf-d592be6bdd47)
 Call ID: 70dfc3c8-4000-4af6-91bf-d592be6bdd47
  Args:
    source: :Ari
    type: :Person
  AddLiteral (5b979caf-889a-4ac6-b0f8-4d9e709ee3ad)
 Call ID: 5b979caf-889a-4ac6-b0f8-4d9e709ee3ad
  Args:
    source: :Ari
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1992
  AddTriple (21da5503-1633-46c2-a8dd-e9837eefca8a)
 Call ID: 21da5503-1633-46c2-a8dd-e9837eefca8a
  Args:
    target: :Gary_Christie_Lewis
    source: :Ari
    relation: :isChildOf
  Finish (d425427b-160e-4401-bb7b-c03b62dae3d9)
 Call ID: d425427b-160e-4401-bb7b-c03b62dae3d9
  Args: