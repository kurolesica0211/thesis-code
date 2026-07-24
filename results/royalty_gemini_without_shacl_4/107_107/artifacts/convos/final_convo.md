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
Princess Beatrix*


Princess Margriet*Pieter van Vollenhoven*


Prince Bernhard Lucas Emmanuel of Orange-Nassau, van Vollenhoven (born 25 December 1969) is a Dutch racing driver, entrepreneur and member of the Dutch royal family.
He is the second son of Princess Margriet of the Netherlands and Pieter van Vollenhoven.
With Willem-Alexander's succession however, he is no longer a member of the Dutch Royal House, and is no longer in line to direct succession to the Dutch throne, but still retains his membership of the Dutch royal family 


Early life and education

Bernhard was born on 25 December 1969 in Nijmegen in the Netherlands.
He is the second son of Princess Margriet and Pieter van Vollenhoven.
He has three brothers: Princes Maurits, Pieter-Christiaan, and Floris.
Subsequently, in 1989 he attended Groningen University in the Netherlands where he studied marketing and market research.
Business

Bernhard is a self-employed entrepreneur.
In 2002, the name Ritzen Koeriers was changed to Logistieke Meesters, at which time Bernhard was no longer involved in the business.
Marriage and family

While studying in Groningen, Bernhard met Annette Sekrève, (born 18 April 1972).
They have three children: Isabella Lily Juliana (born 2002), Samuel Bernhard Louis (born 2004), and Benjamin Pieter Floris (born 2008).
According to a royal decree of 5 July 2000, the children were granted the family name van Vollenhoven, without titles.
In January 2026, Bernhard and Annette announced that they were to divorce.
Upon the announcement of the planned abdication of Queen Beatrix, which took place on 30 April 2013, it was also restated that after the abdication, the children of Princess Margriet and Pieter van Vollenhoven would no longer be eligible for the throne.
Health

Bernhard has been receiving treatment for Crohn's disease since 2002.
Ancestry

References

External links

2 gave up the title "Prince of the Netherlands, but still held the title "Prince of Orange-Nassau"
3 title granted by Royal Decree to descendants of Princess Irene



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
  AssignClass (ccee8771-7090-4e54-a5e2-9eaab6507a10)
 Call ID: ccee8771-7090-4e54-a5e2-9eaab6507a10
  Args:
    source: :Beatrix
    type: :Person
  AssignClass (fc5b3c9f-980f-4094-8a68-fc49a91d46b8)
 Call ID: fc5b3c9f-980f-4094-8a68-fc49a91d46b8
  Args:
    type: :Woman
    source: :Beatrix
  AssignClass (fcabd508-2459-4981-9e57-60cbec76b260)
 Call ID: fcabd508-2459-4981-9e57-60cbec76b260
  Args:
    source: :Margriet
    type: :Person
  AssignClass (02db1d42-6ddb-4480-94f7-a1363774b989)
 Call ID: 02db1d42-6ddb-4480-94f7-a1363774b989
  Args:
    source: :Margriet
    type: :Woman
  AssignClass (8e5e296d-46ea-4635-ac44-91a20e01ca9b)
 Call ID: 8e5e296d-46ea-4635-ac44-91a20e01ca9b
  Args:
    type: :Person
    source: :PieterVanVollenhoven
  AssignClass (c5f2b43f-6b74-429a-b221-e27d107d4d08)
 Call ID: c5f2b43f-6b74-429a-b221-e27d107d4d08
  Args:
    type: :Man
    source: :PieterVanVollenhoven
  AssignClass (a5f1a1fb-b2f2-438f-839b-1682d555ad06)
 Call ID: a5f1a1fb-b2f2-438f-839b-1682d555ad06
  Args:
    source: :BernhardVanVollenhoven
    type: :Person
  AssignClass (497f1cad-8fbe-41ef-8bd1-5047e1657056)
 Call ID: 497f1cad-8fbe-41ef-8bd1-5047e1657056
  Args:
    source: :BernhardVanVollenhoven
    type: :Man
  AddLiteral (7154fd7c-b4c7-49c0-b48d-4f262275e887)
 Call ID: 7154fd7c-b4c7-49c0-b48d-4f262275e887
  Args:
    relation: :hasBirthYear
    literal_value: 1969
    literal_type: xsd:integer
    source: :BernhardVanVollenhoven
  AddTriple (1fe9e117-0174-46a3-a0af-cc370ecd5506)
 Call ID: 1fe9e117-0174-46a3-a0af-cc370ecd5506
  Args:
    source: :BernhardVanVollenhoven
    target: :Margriet
    relation: :hasMother
  AddTriple (f1695e63-2e26-4f6e-b5af-a742463fe132)
 Call ID: f1695e63-2e26-4f6e-b5af-a742463fe132
  Args:
    source: :BernhardVanVollenhoven
    target: :PieterVanVollenhoven
    relation: :hasFather
  AssignClass (69d703c4-564a-4b07-ace8-a538beb42416)
 Call ID: 69d703c4-564a-4b07-ace8-a538beb42416
  Args:
    source: :Maurits
    type: :Person
  AssignClass (159d1596-4593-48ff-bc87-3e0c52bc03f9)
 Call ID: 159d1596-4593-48ff-bc87-3e0c52bc03f9
  Args:
    source: :Maurits
    type: :Man
  AddTriple (7243d584-a048-4f7e-9a14-b7302a7724b4)
 Call ID: 7243d584-a048-4f7e-9a14-b7302a7724b4
  Args:
    relation: :isBrotherOf
    target: :Maurits
    source: :BernhardVanVollenhoven
  AssignClass (9f177bda-78cb-48db-8db9-34513beb53b5)
 Call ID: 9f177bda-78cb-48db-8db9-34513beb53b5
  Args:
    type: :Person
    source: :PieterChristiaan
  AssignClass (4705e58c-7e1d-4b98-8fed-816acc28d81d)
 Call ID: 4705e58c-7e1d-4b98-8fed-816acc28d81d
  Args:
    source: :PieterChristiaan
    type: :Man
  AddTriple (70dc2b03-915a-4445-8d75-6a54f505fdb8)
 Call ID: 70dc2b03-915a-4445-8d75-6a54f505fdb8
  Args:
    relation: :isBrotherOf
    source: :BernhardVanVollenhoven
    target: :PieterChristiaan
  AssignClass (d09c058b-6a8d-4e25-92b8-4cb5ce130755)
 Call ID: d09c058b-6a8d-4e25-92b8-4cb5ce130755
  Args:
    source: :Floris
    type: :Person
  AssignClass (b6ffa163-7a9b-4c26-877c-4071f26219c5)
 Call ID: b6ffa163-7a9b-4c26-877c-4071f26219c5
  Args:
    type: :Man
    source: :Floris
  AddTriple (8b00690f-f160-4a7c-b016-c917e87dde66)
 Call ID: 8b00690f-f160-4a7c-b016-c917e87dde66
  Args:
    source: :BernhardVanVollenhoven
    target: :Floris
    relation: :isBrotherOf
  AssignClass (b143e031-d059-4ddd-8a35-df3f55a0ab17)
 Call ID: b143e031-d059-4ddd-8a35-df3f55a0ab17
  Args:
    type: :Person
    source: :AnnetteSekreve
  AssignClass (417dc26c-9138-4ebd-8131-2cd9d98c3dff)
 Call ID: 417dc26c-9138-4ebd-8131-2cd9d98c3dff
  Args:
    type: :Woman
    source: :AnnetteSekreve
  AddLiteral (e4e37fab-1d27-4b76-957a-b099d841c159)
 Call ID: e4e37fab-1d27-4b76-957a-b099d841c159
  Args:
    literal_value: 1972
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: :AnnetteSekreve
  AssignClass (7dd375da-27a6-4881-afd8-4a765d33700c)
 Call ID: 7dd375da-27a6-4881-afd8-4a765d33700c
  Args:
    source: :IsabellaLilyJuliana
    type: :Person
  AssignClass (e61bb6bf-f717-4020-8d1e-6b0a1f614c15)
 Call ID: e61bb6bf-f717-4020-8d1e-6b0a1f614c15
  Args:
    source: :IsabellaLilyJuliana
    type: :Woman
  AddLiteral (c5f24e99-9993-47c3-8954-bbf7db4adbf4)
 Call ID: c5f24e99-9993-47c3-8954-bbf7db4adbf4
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 2002
    source: :IsabellaLilyJuliana
  AddTriple (b8d7091d-f50d-48b7-b76c-69f04d11752c)
 Call ID: b8d7091d-f50d-48b7-b76c-69f04d11752c
  Args:
    target: :BernhardVanVollenhoven
    source: :IsabellaLilyJuliana
    relation: :isChildOf
  AddTriple (df4620bd-fa78-4d7b-becc-c08d6bfd40a9)
 Call ID: df4620bd-fa78-4d7b-becc-c08d6bfd40a9
  Args:
    relation: :isChildOf
    target: :AnnetteSekreve
    source: :IsabellaLilyJuliana
  AssignClass (3b215c96-1825-4be8-8dd7-911ab94cb48d)
 Call ID: 3b215c96-1825-4be8-8dd7-911ab94cb48d
  Args:
    type: :Person
    source: :SamuelBernhardLouis
  AssignClass (ddf18720-4649-4561-828a-01d164f5305c)
 Call ID: ddf18720-4649-4561-828a-01d164f5305c
  Args:
    source: :SamuelBernhardLouis
    type: :Man
  AddLiteral (8626bd6e-aa23-430e-99f1-bf7bc4528e23)
 Call ID: 8626bd6e-aa23-430e-99f1-bf7bc4528e23
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 2004
    source: :SamuelBernhardLouis
  AddTriple (92d3e8bb-36db-4c65-bc37-749fe077e489)
 Call ID: 92d3e8bb-36db-4c65-bc37-749fe077e489
  Args:
    target: :BernhardVanVollenhoven
    source: :SamuelBernhardLouis
    relation: :isChildOf
  AddTriple (b67b839f-1b06-4647-9522-710927c061e8)
 Call ID: b67b839f-1b06-4647-9522-710927c061e8
  Args:
    target: :AnnetteSekreve
    source: :SamuelBernhardLouis
    relation: :isChildOf
  AssignClass (f679576e-d260-405a-81a2-cc78cec5a281)
 Call ID: f679576e-d260-405a-81a2-cc78cec5a281
  Args:
    type: :Person
    source: :BenjaminPieterFloris
  AssignClass (919601b2-3621-4afd-9a31-36eb393c5c2b)
 Call ID: 919601b2-3621-4afd-9a31-36eb393c5c2b
  Args:
    type: :Man
    source: :BenjaminPieterFloris
  AddLiteral (3d3e857e-a388-46d8-85ed-429d87dd2933)
 Call ID: 3d3e857e-a388-46d8-85ed-429d87dd2933
  Args:
    source: :BenjaminPieterFloris
    literal_type: xsd:integer
    literal_value: 2008
    relation: :hasBirthYear
  AddTriple (8c1edbd9-23c2-4499-ba39-a5e51505304b)
 Call ID: 8c1edbd9-23c2-4499-ba39-a5e51505304b
  Args:
    target: :BernhardVanVollenhoven
    source: :BenjaminPieterFloris
    relation: :isChildOf
  AddTriple (02f81d3b-11d1-4cd8-b475-7560a1c7a6d7)
 Call ID: 02f81d3b-11d1-4cd8-b475-7560a1c7a6d7
  Args:
    relation: :isChildOf
    source: :BenjaminPieterFloris
    target: :AnnetteSekreve
  Finish (742efaaa-26ba-423c-95a2-d0c42a5402d6)
 Call ID: 742efaaa-26ba-423c-95a2-d0c42a5402d6
  Args: