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
  AssignClass (b8828f3a-61c5-484f-aa64-0fdf5537b25e)
 Call ID: b8828f3a-61c5-484f-aa64-0fdf5537b25e
  Args:
    type: :Person
    source: :Queen_Margrethe_II
  AssignClass (6e1a4218-c32b-417c-b00e-15cfddd8fb40)
 Call ID: 6e1a4218-c32b-417c-b00e-15cfddd8fb40
  Args:
    type: :Woman
    source: :Queen_Margrethe_II
  AssignClass (72cd12fc-8970-4355-8b10-b18d3f87aa66)
 Call ID: 72cd12fc-8970-4355-8b10-b18d3f87aa66
  Args:
    type: :Person
    source: :Count_Nikolai_of_Monpezat
  AssignClass (7e4f9129-64a4-45ae-a36e-9b3f6b727220)
 Call ID: 7e4f9129-64a4-45ae-a36e-9b3f6b727220
  Args:
    type: :Man
    source: :Count_Nikolai_of_Monpezat
  AssignClass (c23036f5-f3ab-452a-8965-d54d89ed17d7)
 Call ID: c23036f5-f3ab-452a-8965-d54d89ed17d7
  Args:
    type: :Person
    source: :Prince_Joachim
  AssignClass (e0a7c3e1-a70b-4244-9f87-07ccadbf89c7)
 Call ID: e0a7c3e1-a70b-4244-9f87-07ccadbf89c7
  Args:
    type: :Man
    source: :Prince_Joachim
  AssignClass (73600789-f5a6-405c-83b1-ab380a9a8c89)
 Call ID: 73600789-f5a6-405c-83b1-ab380a9a8c89
  Args:
    type: :Person
    source: :Alexandra_Countess_of_Frederiksborg
  AssignClass (83ebb988-c2b4-4b1e-8187-00f2e7af1fda)
 Call ID: 83ebb988-c2b4-4b1e-8187-00f2e7af1fda
  Args:
    type: :Woman
    source: :Alexandra_Countess_of_Frederiksborg
  AssignClass (d32298fd-9a6f-4a20-8d97-a113c00f6f27)
 Call ID: d32298fd-9a6f-4a20-8d97-a113c00f6f27
  Args:
    type: :Person
    source: :Prince_Henrik
  AssignClass (5a7d590f-2328-42a2-97bd-6e4c4d8b74cd)
 Call ID: 5a7d590f-2328-42a2-97bd-6e4c4d8b74cd
  Args:
    type: :Man
    source: :Prince_Henrik
  AssignClass (9944eb86-5f3d-44d1-a752-13a552eb51c0)
 Call ID: 9944eb86-5f3d-44d1-a752-13a552eb51c0
  Args:
    type: :Person
    source: :King_Frederik_X
  AssignClass (3161a3e7-72cc-40b1-bf99-bd71b4041a9d)
 Call ID: 3161a3e7-72cc-40b1-bf99-bd71b4041a9d
  Args:
    type: :Man
    source: :King_Frederik_X
  AssignClass (ed5e581a-d035-4887-b079-47708d0d290b)
 Call ID: ed5e581a-d035-4887-b079-47708d0d290b
  Args:
    type: :Person
    source: :Prince_Felix
  AssignClass (e1948841-a74f-4a86-8180-c65d7375e57b)
 Call ID: e1948841-a74f-4a86-8180-c65d7375e57b
  Args:
    type: :Man
    source: :Prince_Felix
  AssignClass (844ecd26-a260-4bee-888f-9655d017876c)
 Call ID: 844ecd26-a260-4bee-888f-9655d017876c
  Args:
    type: :Person
    source: :Henrik_half_sibling
  AssignClass (fdf92412-0e08-4edf-ba52-d7c76371f74d)
 Call ID: fdf92412-0e08-4edf-ba52-d7c76371f74d
  Args:
    type: :Man
    source: :Henrik_half_sibling
  AssignClass (a416804f-1daa-4028-acce-77de0f0afb71)
 Call ID: a416804f-1daa-4028-acce-77de0f0afb71
  Args:
    type: :Person
    source: :Athena_half_sibling
  AssignClass (ce81eae9-b129-4c22-8f62-ae03107f59ca)
 Call ID: ce81eae9-b129-4c22-8f62-ae03107f59ca
  Args:
    type: :Woman
    source: :Athena_half_sibling
  AssignClass (2710417c-d87b-4273-8c0f-eea15a2435e6)
 Call ID: 2710417c-d87b-4273-8c0f-eea15a2435e6
  Args:
    type: :Person
    source: :Marie_Cavallier
  AssignClass (2b5e053c-7bd4-46ad-afb1-824e5535b2e6)
 Call ID: 2b5e053c-7bd4-46ad-afb1-824e5535b2e6
  Args:
    type: :Woman
    source: :Marie_Cavallier
  AddTriple (9361f11c-af59-45d2-8d6a-9c23749806e7)
 Call ID: 9361f11c-af59-45d2-8d6a-9c23749806e7
  Args:
    relation: :hasFather
    source: :Count_Nikolai_of_Monpezat
    target: :Prince_Joachim
  AddTriple (2287ada1-28cf-4c85-9379-87fc4037301d)
 Call ID: 2287ada1-28cf-4c85-9379-87fc4037301d
  Args:
    target: :Alexandra_Countess_of_Frederiksborg
    source: :Count_Nikolai_of_Monpezat
    relation: :hasMother
  AddTriple (c6a3c151-7715-44b6-b800-17889635750f)
 Call ID: c6a3c151-7715-44b6-b800-17889635750f
  Args:
    target: :Prince_Joachim
    source: :Prince_Felix
    relation: :hasFather
  AddTriple (d73996d0-743d-4f88-ad2d-526d6276f1f8)
 Call ID: d73996d0-743d-4f88-ad2d-526d6276f1f8
  Args:
    relation: :hasMother
    source: :Prince_Felix
    target: :Alexandra_Countess_of_Frederiksborg
  AddTriple (afd7b667-ac9c-42c3-a82a-7e65a5db5ba4)
 Call ID: afd7b667-ac9c-42c3-a82a-7e65a5db5ba4
  Args:
    target: :Prince_Joachim
    relation: :hasFather
    source: :Henrik_half_sibling
  AddTriple (8f2f6b05-ee6f-42d0-ae22-5696eaf44018)
 Call ID: 8f2f6b05-ee6f-42d0-ae22-5696eaf44018
  Args:
    target: :Marie_Cavallier
    source: :Henrik_half_sibling
    relation: :hasMother
  AddTriple (90370ba5-0431-441a-8104-d803f018212e)
 Call ID: 90370ba5-0431-441a-8104-d803f018212e
  Args:
    relation: :hasFather
    source: :Athena_half_sibling
    target: :Prince_Joachim
  AddTriple (bf7f8eef-e069-4a7b-9976-ba72272b594e)
 Call ID: bf7f8eef-e069-4a7b-9976-ba72272b594e
  Args:
    relation: :hasMother
    source: :Athena_half_sibling
    target: :Marie_Cavallier
  AddLiteral (f0d3da55-bba7-451c-9efc-c87df13558c6)
 Call ID: f0d3da55-bba7-451c-9efc-c87df13558c6
  Args:
    literal_value: 1999
    literal_type: xsd:string
    source: :Count_Nikolai_of_Monpezat
    relation: :hasBirthYear
  AddTriple (ed4fdc36-1d0d-4e60-84a7-82702b082137)
 Call ID: ed4fdc36-1d0d-4e60-84a7-82702b082137
  Args:
    target: :Queen_Margrethe_II
    relation: :isChildOf
    source: :Prince_Joachim
  AddTriple (007dffba-a10e-4a64-ad23-b4e02116d20e)
 Call ID: 007dffba-a10e-4a64-ad23-b4e02116d20e
  Args:
    relation: :isChildOf
    source: :Prince_Joachim
    target: :Prince_Henrik
  Finish (7f8de9d5-0abd-445d-bae9-3ae108751d07)
 Call ID: 7f8de9d5-0abd-445d-bae9-3ae108751d07
  Args: