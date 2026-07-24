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
  AssignClass (57b38da5-2059-4155-b897-1f956cdbff7c)
 Call ID: 57b38da5-2059-4155-b897-1f956cdbff7c
  Args:
    source: :Queen_Margrethe_II
    type: :Woman
  AssignClass (9d207e47-00b8-43eb-84a5-a00f290e45a5)
 Call ID: 9d207e47-00b8-43eb-84a5-a00f290e45a5
  Args:
    source: :Prince_Nikolai_of_Denmark
    type: :Man
  AssignClass (f76008d0-d66b-454d-8170-0b234c24c328)
 Call ID: f76008d0-d66b-454d-8170-0b234c24c328
  Args:
    source: :Prince_Joachim
    type: :Man
  AssignClass (f50b3875-86b0-4fdc-afb7-6dfd6a32e361)
 Call ID: f50b3875-86b0-4fdc-afb7-6dfd6a32e361
  Args:
    type: :Woman
    source: :Alexandra_Countess_of_Frederiksborg
  AssignClass (4600f287-ab9e-4b39-b04d-024bfcea1054)
 Call ID: 4600f287-ab9e-4b39-b04d-024bfcea1054
  Args:
    type: :Man
    source: :Prince_Henrik
  AssignClass (f6aa9cfd-d73a-4892-9085-bc201ba1cfcf)
 Call ID: f6aa9cfd-d73a-4892-9085-bc201ba1cfcf
  Args:
    type: :Man
    source: :King_Frederik_X
  AssignClass (0c25270f-f1f1-4305-a2f2-b374059e958b)
 Call ID: 0c25270f-f1f1-4305-a2f2-b374059e958b
  Args:
    type: :Man
    source: :Prince_Felix
  AssignClass (4d3927c1-3db4-4ff6-a179-28845e2fd524)
 Call ID: 4d3927c1-3db4-4ff6-a179-28845e2fd524
  Args:
    source: :Henrik
    type: :Man
  AssignClass (8bfbd11a-a8b9-42e5-9b1b-fc06bc45fe6d)
 Call ID: 8bfbd11a-a8b9-42e5-9b1b-fc06bc45fe6d
  Args:
    source: :Athena
    type: :Woman
  AssignClass (5a73acf2-3688-4920-92ba-6ae83686ba88)
 Call ID: 5a73acf2-3688-4920-92ba-6ae83686ba88
  Args:
    source: :Marie_Cavallier
    type: :Woman
  AddLiteral (9e48cb00-b2c2-41c0-a223-fa11a9e8a466)
 Call ID: 9e48cb00-b2c2-41c0-a223-fa11a9e8a466
  Args:
    literal_value: 1999
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: :Prince_Nikolai_of_Denmark
  AddTriple (f5a8dd4d-5921-4078-83b3-83dbf4fd7d25)
 Call ID: f5a8dd4d-5921-4078-83b3-83dbf4fd7d25
  Args:
    relation: :hasFather
    target: :Prince_Joachim
    source: :Prince_Nikolai_of_Denmark
  AddTriple (a9d45ddf-5029-44ab-b0de-743f34317b5f)
 Call ID: a9d45ddf-5029-44ab-b0de-743f34317b5f
  Args:
    source: :Prince_Nikolai_of_Denmark
    target: :Alexandra_Countess_of_Frederiksborg
    relation: :hasMother
  AddTriple (cb759292-2ec0-4430-a3c4-fa516d1c43cc)
 Call ID: cb759292-2ec0-4430-a3c4-fa516d1c43cc
  Args:
    source: :Prince_Nikolai_of_Denmark
    target: :Queen_Margrethe_II
    relation: :hasMother
  RemoveTriple (1321f375-df69-4d78-b1e2-f5a191604371)
 Call ID: 1321f375-df69-4d78-b1e2-f5a191604371
  Args:
    relation: :hasMother
    target: :Queen_Margrethe_II
    source: :Prince_Nikolai_of_Denmark
  AddTriple (78970cfa-fa5b-4a9c-8bf0-6f2085bbdeed)
 Call ID: 78970cfa-fa5b-4a9c-8bf0-6f2085bbdeed
  Args:
    target: :Prince_Joachim
    source: :Prince_Nikolai_of_Denmark
    relation: :isChildOf
  AddTriple (43c77a8e-2973-439b-bdce-f6d4c7e1c792)
 Call ID: 43c77a8e-2973-439b-bdce-f6d4c7e1c792
  Args:
    relation: :isChildOf
    target: :Alexandra_Countess_of_Frederiksborg
    source: :Prince_Nikolai_of_Denmark
  AddTriple (feb9b90a-838e-49b8-851c-caaf133fbb60)
 Call ID: feb9b90a-838e-49b8-851c-caaf133fbb60
  Args:
    source: :Prince_Felix
    target: :Prince_Joachim
    relation: :hasFather
  AddTriple (944c4c96-8305-4c95-abec-a78d096ddadc)
 Call ID: 944c4c96-8305-4c95-abec-a78d096ddadc
  Args:
    relation: :hasMother
    source: :Prince_Felix
    target: :Alexandra_Countess_of_Frederiksborg
  AddTriple (8e8cef88-e64a-4325-baff-1273a7b4d461)
 Call ID: 8e8cef88-e64a-4325-baff-1273a7b4d461
  Args:
    source: :Henrik
    target: :Prince_Joachim
    relation: :hasFather
  AddTriple (e2cd5161-b98b-4dd8-b3ef-d8496ff53848)
 Call ID: e2cd5161-b98b-4dd8-b3ef-d8496ff53848
  Args:
    target: :Marie_Cavallier
    source: :Henrik
    relation: :hasMother
  AddTriple (a5fce39a-5aec-4592-9918-093b428db619)
 Call ID: a5fce39a-5aec-4592-9918-093b428db619
  Args:
    relation: :hasFather
    source: :Athena
    target: :Prince_Joachim
  AddTriple (5e0cc00f-0e91-4017-9021-fdd76e716cd4)
 Call ID: 5e0cc00f-0e91-4017-9021-fdd76e716cd4
  Args:
    relation: :hasMother
    source: :Athena
    target: :Marie_Cavallier
  AddTriple (ce3250f5-19e7-4bcd-a31c-4d6404e184a7)
 Call ID: ce3250f5-19e7-4bcd-a31c-4d6404e184a7
  Args:
    source: :Prince_Joachim
    target: :Prince_Henrik
    relation: :hasFather
  AddTriple (b0f2b383-26b9-4fcc-a708-a3f957a21301)
 Call ID: b0f2b383-26b9-4fcc-a708-a3f957a21301
  Args:
    target: :Queen_Margrethe_II
    source: :Prince_Joachim
    relation: :hasMother
  AddLiteral (296d24f9-3d61-47cb-9181-3f6810e1adcb)
 Call ID: 296d24f9-3d61-47cb-9181-3f6810e1adcb
  Args:
    source: :Prince_Nikolai_of_Denmark
    literal_value: Count Nikolai of Monpezat
    relation: :knownAs
    literal_type: xsd:string
  Finish (8b904b2e-8a22-4259-b3d5-12714cd3dce8)
 Call ID: 8b904b2e-8a22-4259-b3d5-12714cd3dce8
  Args: