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
Queen Margrethe II


Count Nikolai of Monpezat SK (born Prince Nikolai of Denmark; 28 August 1999) is a member of the Danish royal family.
He is the eldest son of Prince Joachim and his first wife, Alexandra, Countess of Frederiksborg, the eldest grandchild of Queen Margrethe II and Prince Henrik, and the eldest nephew of King Frederik X.
Biography

Nikolai was born a prince of Denmark at Rigshospitalet in Copenhagen on 28 August 1999.
He is the oldest grandchild of Queen Margrethe II and her late husband, Prince Henrik.
Nikolai was baptised in the chapel of the Fredensborg Palace on 6 November 1999 by the Danish Chaplain-in-Ordinary, Christian Thodberg.
At the christening, the musical work Lys på din vej, composed by Frederik Magle and dedicated to the prince, was performed for the first time.
His godparents are his paternal uncle King Frederik X, his maternal aunt Nicola Baird, Prince Edward, Duke of Edinburgh, Peter Steenstrup and Camilla Flint.
After their divorce in 2005, Prince Joachim and Alexandra had joint custody of the prince and his brother Prince Felix.
Nikolai and Felix have two half-siblings, Henrik and Athena, from their father's second marriage to Marie Cavallier.
Nikolai was confirmed on 18 May 2013 in Fredensborg Palace Church in the presence of his immediate family and all his godparents.
Like his father and uncle, Nikolai attended Krebs School in Copenhagen.
As part of that course, in 2023, Nikolai moved to Australia to take a semester at University of Technology Sydney.
In early 2018, Nikolai signed as a fashion model with the agency Scoop Models.
In February 2023, Nikolai signed as a model for Elite Model World - Paris under the name of 'Nikolai'.
Subsequently, in May he also signed with Barcelona-based modeling agency Sight Management Studio as 'Count Nikolai of Monpezat'.
In June 2024, Nikolai graduated from Copenhagen Business School with a Master of Science in Merchandising degree (cand.merc.).
In December 2025, it was announced that Nikolai would make his acting debut in the film adaptation of Hjalmar Söderberg's novel Doktor Glas (1905).
Titles, styles and honours

Titles and styles

Originally styled "His Highness Prince Nikolai of Denmark", Nikolai's style was expanded on 29 April 2008 to "His Highness Prince Nikolai of Denmark, Count of Monpezat".
In September 2022, Queen Margrethe II decided to restrict the titles Prince and Princess to the direct line of succession to the throne.
Since 1 January 2023, Count Nikolai is known as "His Excellency Count Nikolai of Monpezat".



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
  AssignClass (b0a89a87-399b-4ed4-bd3e-82edd0009d8c)
 Call ID: b0a89a87-399b-4ed4-bd3e-82edd0009d8c
  Args:
    type: :Man
    source: :Nikolai
  AssignClass (ad539e4d-c51c-4d1b-bfa8-58a00e03a1e7)
 Call ID: ad539e4d-c51c-4d1b-bfa8-58a00e03a1e7
  Args:
    type: :Person
    source: :Nikolai
  AssignClass (c3833c7f-8b0a-49c4-a09d-2b13381f3a87)
 Call ID: c3833c7f-8b0a-49c4-a09d-2b13381f3a87
  Args:
    type: :Man
    source: :Joachim
  AssignClass (7a345bc9-251e-488a-96a8-215fac444b31)
 Call ID: 7a345bc9-251e-488a-96a8-215fac444b31
  Args:
    type: :Person
    source: :Joachim
  AssignClass (577b2191-95a3-480d-b229-1a51caf64040)
 Call ID: 577b2191-95a3-480d-b229-1a51caf64040
  Args:
    type: :Woman
    source: :Alexandra
  AssignClass (3d638eb3-b615-4b5f-ad98-5ebd78728cc5)
 Call ID: 3d638eb3-b615-4b5f-ad98-5ebd78728cc5
  Args:
    type: :Person
    source: :Alexandra
  AssignClass (e016c488-7f1e-4137-a95d-03aff450eb85)
 Call ID: e016c488-7f1e-4137-a95d-03aff450eb85
  Args:
    type: :Woman
    source: :MargretheII
  AssignClass (79bfffe3-cef7-4daf-bbc0-7c5de34bb4b0)
 Call ID: 79bfffe3-cef7-4daf-bbc0-7c5de34bb4b0
  Args:
    type: :Person
    source: :MargretheII
  AssignClass (269deb1d-dd3f-490c-9eb0-730884eb06a9)
 Call ID: 269deb1d-dd3f-490c-9eb0-730884eb06a9
  Args:
    type: :Man
    source: :HenrikSr
  AssignClass (9fb0ea7d-cf0a-4ea4-969e-85b1f13b3e8e)
 Call ID: 9fb0ea7d-cf0a-4ea4-969e-85b1f13b3e8e
  Args:
    type: :Person
    source: :HenrikSr
  AssignClass (57499c63-8ff6-4806-8d07-d20fe5d05bf6)
 Call ID: 57499c63-8ff6-4806-8d07-d20fe5d05bf6
  Args:
    type: :Man
    source: :FrederikX
  AssignClass (eed28e7a-55f2-4254-96cd-76a7ceeb7ba5)
 Call ID: eed28e7a-55f2-4254-96cd-76a7ceeb7ba5
  Args:
    type: :Person
    source: :FrederikX
  AssignClass (59eeab1f-275a-4402-8d08-879c5cd6a679)
 Call ID: 59eeab1f-275a-4402-8d08-879c5cd6a679
  Args:
    type: :Man
    source: :Felix
  AssignClass (6ef17d67-be0e-4583-9271-eb7a25aabb07)
 Call ID: 6ef17d67-be0e-4583-9271-eb7a25aabb07
  Args:
    type: :Person
    source: :Felix
  AssignClass (e842b60c-fa7d-41d8-aa50-b25ca6173c9e)
 Call ID: e842b60c-fa7d-41d8-aa50-b25ca6173c9e
  Args:
    type: :Man
    source: :HenrikJr
  AssignClass (1936e076-4231-4bbb-8caa-f0b25d90dd8f)
 Call ID: 1936e076-4231-4bbb-8caa-f0b25d90dd8f
  Args:
    type: :Person
    source: :HenrikJr
  AssignClass (fd2a0886-5bab-4577-9791-92715b3a5e47)
 Call ID: fd2a0886-5bab-4577-9791-92715b3a5e47
  Args:
    type: :Woman
    source: :Athena
  AssignClass (79df80f6-3a2b-4b89-9377-8c74d949ebcd)
 Call ID: 79df80f6-3a2b-4b89-9377-8c74d949ebcd
  Args:
    type: :Person
    source: :Athena
  AssignClass (c7a70828-be5b-4955-bec3-476c3c4bfb4e)
 Call ID: c7a70828-be5b-4955-bec3-476c3c4bfb4e
  Args:
    type: :Woman
    source: :MarieCavallier
  AssignClass (980b0f27-4766-4e1f-83e6-27512fcbde59)
 Call ID: 980b0f27-4766-4e1f-83e6-27512fcbde59
  Args:
    type: :Person
    source: :MarieCavallier
  AddLiteral (4919b988-40cb-41ae-839f-57dfc77e9f02)
 Call ID: 4919b988-40cb-41ae-839f-57dfc77e9f02
  Args:
    literal_type: xsd:integer
    literal_value: 1999
    source: :Nikolai
    relation: :hasBirthYear
  AddTriple (e1fc37bb-db8e-4c2c-bb8b-21e097f5c387)
 Call ID: e1fc37bb-db8e-4c2c-bb8b-21e097f5c387
  Args:
    source: :Nikolai
    relation: :hasFather
    target: :Joachim
  AddTriple (41f003a0-474f-4dae-bc65-92da6b2615d8)
 Call ID: 41f003a0-474f-4dae-bc65-92da6b2615d8
  Args:
    source: :Nikolai
    relation: :hasMother
    target: :Alexandra
  AddTriple (b59997c5-bc94-47a9-aa94-863a2badb4df)
 Call ID: b59997c5-bc94-47a9-aa94-863a2badb4df
  Args:
    target: :Nikolai
    source: :Joachim
    relation: :isFatherOf
  AddTriple (1725befe-98d0-46d0-a1e0-5eb43bc6408d)
 Call ID: 1725befe-98d0-46d0-a1e0-5eb43bc6408d
  Args:
    relation: :isMotherOf
    source: :Alexandra
    target: :Nikolai
  AddTriple (479fe7d1-764f-4f26-9d74-3a555a613060)
 Call ID: 479fe7d1-764f-4f26-9d74-3a555a613060
  Args:
    source: :Nikolai
    relation: :hasFather
    target: :Joachim
  AddTriple (22154816-b7e5-4e41-bf6d-33dcdb6fae79)
 Call ID: 22154816-b7e5-4e41-bf6d-33dcdb6fae79
  Args:
    relation: :isBrotherOf
    source: :Nikolai
    target: :Felix
  AddTriple (bb3c278c-f2f8-4561-baea-3089bdc50001)
 Call ID: bb3c278c-f2f8-4561-baea-3089bdc50001
  Args:
    target: :Nikolai
    relation: :isBrotherOf
    source: :Felix
  AddTriple (305eb387-0446-4571-982d-4a657499743c)
 Call ID: 305eb387-0446-4571-982d-4a657499743c
  Args:
    target: :Joachim
    relation: :hasFather
    source: :Felix
  AddTriple (b2b9d720-9304-4e39-b36a-03a02b9e45a4)
 Call ID: b2b9d720-9304-4e39-b36a-03a02b9e45a4
  Args:
    relation: :hasMother
    source: :Felix
    target: :Alexandra
  AddTriple (0d410b12-a83f-4707-8168-46b3b96bff88)
 Call ID: 0d410b12-a83f-4707-8168-46b3b96bff88
  Args:
    relation: :hasFather
    source: :HenrikJr
    target: :Joachim
  AddTriple (0af8705f-a33e-4306-858e-46356570f842)
 Call ID: 0af8705f-a33e-4306-858e-46356570f842
  Args:
    target: :MarieCavallier
    relation: :hasMother
    source: :HenrikJr
  AddTriple (ce1c9a12-866f-4fef-8c1d-7cd94a1d72be)
 Call ID: ce1c9a12-866f-4fef-8c1d-7cd94a1d72be
  Args:
    target: :Joachim
    relation: :hasFather
    source: :Athena
  AddTriple (9a53c00c-7d89-4bfc-b6d1-3c84031cd270)
 Call ID: 9a53c00c-7d89-4bfc-b6d1-3c84031cd270
  Args:
    relation: :hasMother
    source: :Athena
    target: :MarieCavallier
  Finish (34c92550-2557-4f43-85a5-3657d2cb1c1d)
 Call ID: 34c92550-2557-4f43-85a5-3657d2cb1c1d
  Args: