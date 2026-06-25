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
Princess Eugenie of Greece and Denmark (Greek: Ευγενία, romanized: Evyenía; 10 February 1910 – 13 February 1989) was by birth member of the Greek royal family and by marriage member of the House of Radziwiłł and House of Thurn und Taxis.
Early life and ancestry

Eugenie was the youngest child and only daughter of Prince George of Greece and Denmark and his wife, Princess Marie Bonaparte, daughter of Marie-Félix Blanc and Prince Roland Bonaparte, a great-nephew of Napoleon I.
Her father was the second son of George I of Greece and Olga Constantinovna of Russia.
She had one elder brother, Prince Peter of Greece and Denmark, who, at the time of his birth, was third in line of succession to the Greek throne, preceded only by his unmarried cousin Paul and his own and Eugenia's father, Prince George.
As a cousin of the bridegroom, Eugenie was a leading guest at the 1947 wedding of Princess Elizabeth and Philip, Duke of Edinburgh.
She authored Le Tsarevitch, Enfant Martyr, a biography of Aleksey Nikolaevich, Tsarevich of Russia, written in French, which was published in 1990.
Marriage and issue

She married Prince Dominik Rainer Radziwiłł, member of the House of Radziwiłł (and son of Prince Hieronim Radziwiłł and Archduchess Renata of Austria), on 30 May 1938 in Paris.
They had two children:


Eugénie remarried on 28 November 1949 to Prince Raymundo della Torre e Tasso, Duke of Castel Duino, a cadet member of the House of Thurn and Taxis.



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
  AssignClass (dc741da5-5358-480b-bf61-6d811c4fb308)
 Call ID: dc741da5-5358-480b-bf61-6d811c4fb308
  Args:
    type: :Woman
    source: :EugenieOfGreeceAndDenmark
  AddLiteral (cfe90ab3-7ca4-4c99-b7a7-48376c4352b5)
 Call ID: cfe90ab3-7ca4-4c99-b7a7-48376c4352b5
  Args:
    literal_type: xsd:integer
    source: :EugenieOfGreeceAndDenmark
    literal_value: 1910
    relation: :hasBirthYear
  AddLiteral (ae588938-a77e-44db-a007-b999a8822d39)
 Call ID: ae588938-a77e-44db-a007-b999a8822d39
  Args:
    relation: :hasDeathYear
    literal_value: 1989
    source: :EugenieOfGreeceAndDenmark
    literal_type: xsd:integer
  AssignClass (948a2310-58c6-4cda-b112-db6947ce3903)
 Call ID: 948a2310-58c6-4cda-b112-db6947ce3903
  Args:
    type: :Man
    source: :PrinceGeorgeOfGreeceAndDenmark
  AssignClass (6f610bee-1f6b-40ad-aa2b-44332b841dae)
 Call ID: 6f610bee-1f6b-40ad-aa2b-44332b841dae
  Args:
    source: :PrincessMarieBonaparte
    type: :Woman
  AddTriple (01275d63-62f5-48c9-a3b5-5e60b42d2060)
 Call ID: 01275d63-62f5-48c9-a3b5-5e60b42d2060
  Args:
    relation: :hasFather
    target: :PrinceGeorgeOfGreeceAndDenmark
    source: :EugenieOfGreeceAndDenmark
  AddTriple (efc2beee-cd0e-47d5-8e5c-d97ee68b4d07)
 Call ID: efc2beee-cd0e-47d5-8e5c-d97ee68b4d07
  Args:
    target: :PrincessMarieBonaparte
    relation: :hasMother
    source: :EugenieOfGreeceAndDenmark
  AssignClass (ea8d5be9-e603-4474-a0a7-f8ea1744fffb)
 Call ID: ea8d5be9-e603-4474-a0a7-f8ea1744fffb
  Args:
    source: :MarieFelixBlanc
    type: :Woman
  AssignClass (3c2e9d58-21d9-4009-b342-c9381a08233e)
 Call ID: 3c2e9d58-21d9-4009-b342-c9381a08233e
  Args:
    type: :Man
    source: :PrinceRolandBonaparte
  AddTriple (a580a51b-5eaf-4644-a556-f94c95d1e535)
 Call ID: a580a51b-5eaf-4644-a556-f94c95d1e535
  Args:
    source: :PrincessMarieBonaparte
    relation: :hasFather
    target: :PrinceRolandBonaparte
  AddTriple (080ecc01-1532-4dac-8a22-bc64f2e6e4c7)
 Call ID: 080ecc01-1532-4dac-8a22-bc64f2e6e4c7
  Args:
    target: :MarieFelixBlanc
    relation: :hasMother
    source: :PrincessMarieBonaparte
  AssignClass (35e5cb77-dee2-45d0-a433-f921ace27a70)
 Call ID: 35e5cb77-dee2-45d0-a433-f921ace27a70
  Args:
    source: :GeorgeIOfGreece
    type: :Man
  AssignClass (3d8ee8f0-e319-4950-8a4d-94f7417a3530)
 Call ID: 3d8ee8f0-e319-4950-8a4d-94f7417a3530
  Args:
    type: :Woman
    source: :OlgaConstantinovnaOfRussia
  AddTriple (8fefc0a9-b3dc-4598-aee2-62e161590861)
 Call ID: 8fefc0a9-b3dc-4598-aee2-62e161590861
  Args:
    source: :PrinceGeorgeOfGreeceAndDenmark
    relation: :hasFather
    target: :GeorgeIOfGreece
  AddTriple (7d46163c-a588-422c-a319-3f17dd210fda)
 Call ID: 7d46163c-a588-422c-a319-3f17dd210fda
  Args:
    source: :PrinceGeorgeOfGreeceAndDenmark
    relation: :hasMother
    target: :OlgaConstantinovnaOfRussia
  AssignClass (32eddf46-57a8-47cc-bab1-c5f69d8376e7)
 Call ID: 32eddf46-57a8-47cc-bab1-c5f69d8376e7
  Args:
    source: :PrincePeterOfGreeceAndDenmark
    type: :Man
  AddTriple (a55cece2-718d-454b-8ebc-a6a65ac10931)
 Call ID: a55cece2-718d-454b-8ebc-a6a65ac10931
  Args:
    relation: :hasBrother
    target: :PrincePeterOfGreeceAndDenmark
    source: :EugenieOfGreeceAndDenmark
  AddTriple (e63075b4-eb01-49f9-8a5e-585d32fe22ea)
 Call ID: e63075b4-eb01-49f9-8a5e-585d32fe22ea
  Args:
    target: :PrinceGeorgeOfGreeceAndDenmark
    relation: :hasFather
    source: :PrincePeterOfGreeceAndDenmark
  AddTriple (47ab0602-a3d9-4054-8595-d2564a0471e6)
 Call ID: 47ab0602-a3d9-4054-8595-d2564a0471e6
  Args:
    source: :PrincePeterOfGreeceAndDenmark
    relation: :hasMother
    target: :PrincessMarieBonaparte
  AssignClass (204ccb38-6656-4f56-8cdb-2d5582686b18)
 Call ID: 204ccb38-6656-4f56-8cdb-2d5582686b18
  Args:
    type: :Man
    source: :PrinceDominikRainerRadziwill
  AddLiteral (6cafa0e1-ce2d-434a-b996-40f907fb3b19)
 Call ID: 6cafa0e1-ce2d-434a-b996-40f907fb3b19
  Args:
    literal_value: 1938
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: :EugenieOfGreeceAndDenmark
  AddTriple (d3483587-676b-4571-92fc-a85d0bd38c94)
 Call ID: d3483587-676b-4571-92fc-a85d0bd38c94
  Args:
    target: :PrinceDominikRainerRadziwill
    relation: :hasRelation
    source: :EugenieOfGreeceAndDenmark
  AssignClass (779315b9-92c5-4be3-a4e0-ac41bbf679c2)
 Call ID: 779315b9-92c5-4be3-a4e0-ac41bbf679c2
  Args:
    source: :PrinceHieronimRadziwill
    type: :Man
  AssignClass (f5d5b3fc-46c0-451c-b506-18c7e18fe4d2)
 Call ID: f5d5b3fc-46c0-451c-b506-18c7e18fe4d2
  Args:
    source: :ArchduchessRenataOfAustria
    type: :Woman
  AddTriple (76b53e81-e7f2-48de-8e42-f67e21bed9cb)
 Call ID: 76b53e81-e7f2-48de-8e42-f67e21bed9cb
  Args:
    source: :PrinceDominikRainerRadziwill
    relation: :hasFather
    target: :PrinceHieronimRadziwill
  AddTriple (c13afd55-3fa4-4730-87ff-5ed702ef8e8b)
 Call ID: c13afd55-3fa4-4730-87ff-5ed702ef8e8b
  Args:
    source: :PrinceDominikRainerRadziwill
    relation: :hasMother
    target: :ArchduchessRenataOfAustria
  AssignClass (49e2cc3c-850a-4e79-b31f-0e349b672d1d)
 Call ID: 49e2cc3c-850a-4e79-b31f-0e349b672d1d
  Args:
    source: :PrinceRaymundoDellaTorreETasso
    type: :Man
  AddLiteral (4fb835a4-ccee-45fa-92c8-fa6e111e06a9)
 Call ID: 4fb835a4-ccee-45fa-92c8-fa6e111e06a9
  Args:
    literal_value: 1949
    relation: :hasMarriageYear
    source: :EugenieOfGreeceAndDenmark
    literal_type: xsd:integer
  AddTriple (85f1a3b6-3b30-4e4f-a4b6-c470c496f98b)
 Call ID: 85f1a3b6-3b30-4e4f-a4b6-c470c496f98b
  Args:
    source: :EugenieOfGreeceAndDenmark
    target: :PrinceRaymundoDellaTorreETasso
    relation: :hasRelation
  Finish (41baf775-0236-4f3c-aa5b-5937519c360b)
 Call ID: 41baf775-0236-4f3c-aa5b-5937519c360b
  Args: