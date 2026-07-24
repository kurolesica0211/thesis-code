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
Princess Marie Alix of Schaumburg-Lippe (Marie Alix zu Schaumburg-Lippe; 2 April 1923 – 1 November 2021) was Duchess of Schleswig-Holstein as the wife of Peter, Duke of Schleswig-Holstein from 1965 to 1980.
Biography

Family

Marie Alix was the only daughter of Prince Stefan of Schaumburg-Lippe  and Ingeborg Alix, Princess Stephan Alexander of Schaumburg-Lippe .
She was the niece of Adolf II, the last ruler of the Principality of Schaumburg-Lippe, who abdicated following the German Revolution of 1918–1919.
Marie Alix's younger brother, Prince Georg Moritz of Schaumburg-Lippe, was killed in a car accident in 1970 without marrying or having children.
Marriage and issue

Marie Alix married Peter, Duke of Schleswig-Holstein, third son of Wilhelm Friedrich, Duke of Schleswig-Holstein, and Princess Marie Melita of Hohenlohe-Langenburg, in Glücksburg on 9 October 1947.
They had four children:


Work

She was a co-founder of the Stiftung Louisenlund, which runs an eponymous boarding school in Güby, Schleswig-Holstein, Germany.
Death and funeral

Princess Marie Alix of Schaumburg-Lippe died in Thumby on 1 November 2021 at the age of 98.
Her funeral was held 11 November 2021 in Schleswig Cathedral and she was buried in a family crypt at the family home, Louisenlund.



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
  AssignClass (f87380f1-eaed-4dda-b721-048a2d6e450e)
 Call ID: f87380f1-eaed-4dda-b721-048a2d6e450e
  Args:
    source: :MarieAlixOfSchaumburgLippe
    type: :Woman
  AssignClass (da828204-3a3c-4e7e-904f-8a583fcb0ba9)
 Call ID: da828204-3a3c-4e7e-904f-8a583fcb0ba9
  Args:
    source: :MarieAlixOfSchaumburgLippe
    type: :Person
  AddLiteral (c6cfae98-efef-47d2-83c6-62787c4df472)
 Call ID: c6cfae98-efef-47d2-83c6-62787c4df472
  Args:
    source: :MarieAlixOfSchaumburgLippe
    literal_value: 1923
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (28d56004-dc5e-4ffa-b72a-717c34c4fe12)
 Call ID: 28d56004-dc5e-4ffa-b72a-717c34c4fe12
  Args:
    relation: :hasDeathYear
    literal_value: 2021
    literal_type: xsd:integer
    source: :MarieAlixOfSchaumburgLippe
  AssignClass (2be5de9d-7523-48b0-a3b8-fd4cf89b5024)
 Call ID: 2be5de9d-7523-48b0-a3b8-fd4cf89b5024
  Args:
    source: :PeterDukeOfSchleswigHolstein
    type: :Man
  AssignClass (c0588432-24af-4f54-ae5d-ab9de7d02edf)
 Call ID: c0588432-24af-4f54-ae5d-ab9de7d02edf
  Args:
    source: :PeterDukeOfSchleswigHolstein
    type: :Person
  AddLiteral (79dc9a79-a627-4285-b35e-4e30f11c39be)
 Call ID: 79dc9a79-a627-4285-b35e-4e30f11c39be
  Args:
    source: :MarieAlixOfSchaumburgLippe
    literal_value: 1947
    relation: :hasMarriageYear
    literal_type: xsd:integer
  AddTriple (8fd9ef5a-7c4e-492b-a701-39e2fdbc903d)
 Call ID: 8fd9ef5a-7c4e-492b-a701-39e2fdbc903d
  Args:
    relation: :hasRelation
    source: :MarieAlixOfSchaumburgLippe
    target: :PeterDukeOfSchleswigHolstein
  AssignClass (75dcdb43-f9d0-4205-a712-9744cbce0269)
 Call ID: 75dcdb43-f9d0-4205-a712-9744cbce0269
  Args:
    source: :PrinceStefanOfSchaumburgLippe
    type: :Man
  AssignClass (81b4788d-d88d-4f51-bdee-9563d2227fe9)
 Call ID: 81b4788d-d88d-4f51-bdee-9563d2227fe9
  Args:
    source: :PrinceStefanOfSchaumburgLippe
    type: :Person
  AssignClass (c1a9b1e5-0605-4b40-9515-9f0d8ec6cf3b)
 Call ID: c1a9b1e5-0605-4b40-9515-9f0d8ec6cf3b
  Args:
    type: :Woman
    source: :IngeborgAlixPrincessStephanAlexanderOfSchaumburgLippe
  AssignClass (b3e2b821-19fa-4617-a105-92ed90ac4245)
 Call ID: b3e2b821-19fa-4617-a105-92ed90ac4245
  Args:
    type: :Person
    source: :IngeborgAlixPrincessStephanAlexanderOfSchaumburgLippe
  AddTriple (0c943cf5-d754-4e3c-ab9c-2c7fa22086cd)
 Call ID: 0c943cf5-d754-4e3c-ab9c-2c7fa22086cd
  Args:
    relation: :hasFather
    source: :MarieAlixOfSchaumburgLippe
    target: :PrinceStefanOfSchaumburgLippe
  AddTriple (489af578-0299-4d2e-805f-c9f10b79f2dd)
 Call ID: 489af578-0299-4d2e-805f-c9f10b79f2dd
  Args:
    relation: :hasMother
    source: :MarieAlixOfSchaumburgLippe
    target: :IngeborgAlixPrincessStephanAlexanderOfSchaumburgLippe
  AssignClass (b7f3a0f3-29a5-473b-aaaa-e89ce62cc0da)
 Call ID: b7f3a0f3-29a5-473b-aaaa-e89ce62cc0da
  Args:
    source: :PrinceGeorgMoritzOfSchaumburgLippe
    type: :Man
  AssignClass (f150cb6d-0aeb-4d06-ab06-81a90a68601a)
 Call ID: f150cb6d-0aeb-4d06-ab06-81a90a68601a
  Args:
    type: :Person
    source: :PrinceGeorgMoritzOfSchaumburgLippe
  AddTriple (13cdd5e4-0007-45f3-91ef-dc6f7bc17af9)
 Call ID: 13cdd5e4-0007-45f3-91ef-dc6f7bc17af9
  Args:
    relation: :hasBrother
    source: :MarieAlixOfSchaumburgLippe
    target: :PrinceGeorgMoritzOfSchaumburgLippe
  AssignClass (8a37eda6-eb43-43ba-8b67-8887eb6efd65)
 Call ID: 8a37eda6-eb43-43ba-8b67-8887eb6efd65
  Args:
    type: :Man
    source: :AdolfII
  AssignClass (148ce865-a3ec-4be4-9176-d2391f523564)
 Call ID: 148ce865-a3ec-4be4-9176-d2391f523564
  Args:
    source: :AdolfII
    type: :Person
  AssignClass (38cfd0e5-52fa-4cff-a9fe-573600865a5a)
 Call ID: 38cfd0e5-52fa-4cff-a9fe-573600865a5a
  Args:
    type: :Man
    source: :WilhelmFriedrichDukeOfSchleswigHolstein
  AssignClass (af6461ce-2299-44f5-955f-b53629fe4991)
 Call ID: af6461ce-2299-44f5-955f-b53629fe4991
  Args:
    type: :Person
    source: :WilhelmFriedrichDukeOfSchleswigHolstein
  AssignClass (f1094c16-3463-4566-8858-992a439ce2a2)
 Call ID: f1094c16-3463-4566-8858-992a439ce2a2
  Args:
    type: :Woman
    source: :PrincessMarieMelitaOfHohenloheLangenburg
  AssignClass (f74fbf44-7ed5-46aa-9320-b42ddb3a4fde)
 Call ID: f74fbf44-7ed5-46aa-9320-b42ddb3a4fde
  Args:
    type: :Person
    source: :PrincessMarieMelitaOfHohenloheLangenburg
  AddTriple (8b8f37ea-3d1a-4420-bca2-e2228d520f09)
 Call ID: 8b8f37ea-3d1a-4420-bca2-e2228d520f09
  Args:
    source: :PeterDukeOfSchleswigHolstein
    target: :WilhelmFriedrichDukeOfSchleswigHolstein
    relation: :hasFather
  AddTriple (a04c599b-4295-444a-839e-f8aeb25c7ccb)
 Call ID: a04c599b-4295-444a-839e-f8aeb25c7ccb
  Args:
    source: :PeterDukeOfSchleswigHolstein
    target: :PrincessMarieMelitaOfHohenloheLangenburg
    relation: :hasMother
  Finish (41b96961-a0f4-44b5-a651-3909cefd5380)
 Call ID: 41b96961-a0f4-44b5-a651-3909cefd5380
  Args: