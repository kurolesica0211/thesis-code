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
Princess Adelaide of Saxe-Meiningen (Adelaide Erna Caroline Marie Elisabeth; 16 August 1891 – 25 April 1971), later Princess Adalbert of Prussia, was the daughter of Prince Frederick John of Saxe-Meiningen and Countess Adelaide of Lippe-Biesterfeld.
Family

Adelaide (original German: Adelheid)'s father Prince Frederick was a younger son of George II of Saxe-Meiningen by his second wife Feodora of Hohenlohe-Langenburg.
She had five siblings, including Prince George, a prisoner of war killed during World War II, and Prince Bernard.
Adelaide's mother, also named Adelaide, was the eldest child of Ernst, Count of Lippe-Biesterfeld, who was the Regent of the principality of Lippe for seven years (1897–1904).
Marriage

On 3 August 1914, at the beginning of World War I, Adelaide married Prince Adalbert of Prussia at Wilhelmshaven, Schleswig-Holstein, Germany.
He was the third son of Kaiser William II of Germany.
Adelaide's father would die within a month, on 23 August 1914.
Less than a month after their marriage, Prince Adalbert was reported to have been killed in battle in Brussels.
This was only a rumor however, and the prince had been unharmed.
She and Prince Adalbert had three children:


Later life

After William II abdicated in 1918 at the end of World War I, Prince Adalbert sought refuge on his yacht, which had been maintained by a loyal crew.
Princess Adelaide and their children soon attempted to follow, travelling by train from Kiel.
They were delayed however, and eventually came to be staying in southern Bavaria with Prince Henry of Bavaria (a grandson of Ludwig III of Bavaria) and his wife.
She and Prince Adalbert were later reunited.
Princess Adelaide died on 25 April 1971 in La Tour-de-Peilz, Switzerland.



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
  AssignClass (b86fff39-31a0-4a38-bfc2-2991f0ce7f26)
 Call ID: b86fff39-31a0-4a38-bfc2-2991f0ce7f26
  Args:
    type: :Woman
    source: Princess_Adelaide_of_Saxe-Meiningen
  AssignClass (07d48170-6acd-4ae3-9370-212e26943cc6)
 Call ID: 07d48170-6acd-4ae3-9370-212e26943cc6
  Args:
    source: Prince_Frederick_John_of_Saxe-Meiningen
    type: :Man
  AssignClass (fdfcbe77-b8cf-4055-8d80-190d7661e5e6)
 Call ID: fdfcbe77-b8cf-4055-8d80-190d7661e5e6
  Args:
    source: Countess_Adelaide_of_Lippe-Biesterfeld
    type: :Woman
  AssignClass (a08cc1c7-a3ce-4744-873b-e91e79f4be50)
 Call ID: a08cc1c7-a3ce-4744-873b-e91e79f4be50
  Args:
    type: :Man
    source: George_II_of_Saxe-Meiningen
  AssignClass (5af103e2-5e62-4a0d-942c-b6954086c22a)
 Call ID: 5af103e2-5e62-4a0d-942c-b6954086c22a
  Args:
    source: Feodora_of_Hohenlohe-Langenburg
    type: :Woman
  AssignClass (d3c839fd-340e-497c-87b2-1e4e4edcb11a)
 Call ID: d3c839fd-340e-497c-87b2-1e4e4edcb11a
  Args:
    source: Prince_George
    type: :Man
  AssignClass (8b3c072b-f6a8-40a2-9c50-91d3f9d9260c)
 Call ID: 8b3c072b-f6a8-40a2-9c50-91d3f9d9260c
  Args:
    type: :Man
    source: Prince_Bernard
  AssignClass (a7f9e278-9571-4577-9c44-d7ecd5ae51c4)
 Call ID: a7f9e278-9571-4577-9c44-d7ecd5ae51c4
  Args:
    source: Ernst_Count_of_Lippe-Biesterfeld
    type: :Man
  AssignClass (0a0464da-9b8e-48d8-a16c-c3a910ccd1b4)
 Call ID: 0a0464da-9b8e-48d8-a16c-c3a910ccd1b4
  Args:
    source: Prince_Adalbert_of_Prussia
    type: :Man
  AssignClass (5e68490b-00bb-4237-8b1d-0572dedb56c2)
 Call ID: 5e68490b-00bb-4237-8b1d-0572dedb56c2
  Args:
    type: :Man
    source: Kaiser_William_II_of_Germany
  AssignClass (64479772-fa0f-4347-a0ad-9a6998adc9da)
 Call ID: 64479772-fa0f-4347-a0ad-9a6998adc9da
  Args:
    type: :Man
    source: Prince_Henry_of_Bavaria
  AssignClass (14852607-ded5-49fa-8bf4-ca74369fd4fd)
 Call ID: 14852607-ded5-49fa-8bf4-ca74369fd4fd
  Args:
    source: Ludwig_III_of_Bavaria
    type: :Man
  AddLiteral (5536eb55-7e1e-4b19-88ce-c59c584467f3)
 Call ID: 5536eb55-7e1e-4b19-88ce-c59c584467f3
  Args:
    literal_value: 1891
    source: Princess_Adelaide_of_Saxe-Meiningen
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (e30984d9-f82b-4077-aa26-d6b4fe86c35a)
 Call ID: e30984d9-f82b-4077-aa26-d6b4fe86c35a
  Args:
    literal_value: 1971
    source: Princess_Adelaide_of_Saxe-Meiningen
    relation: :hasDeathYear
    literal_type: xsd:integer
  AddTriple (414c94b8-b286-47d2-87c1-ab7261a490f7)
 Call ID: 414c94b8-b286-47d2-87c1-ab7261a490f7
  Args:
    target: Prince_Frederick_John_of_Saxe-Meiningen
    relation: :hasFather
    source: Princess_Adelaide_of_Saxe-Meiningen
  AddTriple (b344c94d-54e9-45d7-b56b-7d8598fdb192)
 Call ID: b344c94d-54e9-45d7-b56b-7d8598fdb192
  Args:
    target: Countess_Adelaide_of_Lippe-Biesterfeld
    source: Princess_Adelaide_of_Saxe-Meiningen
    relation: :hasMother
  AddTriple (c5077104-68e6-43ba-be02-a16b1c4fbcc2)
 Call ID: c5077104-68e6-43ba-be02-a16b1c4fbcc2
  Args:
    relation: :hasFather
    source: Prince_Frederick_John_of_Saxe-Meiningen
    target: George_II_of_Saxe-Meiningen
  AddTriple (2352a663-afd0-4ffc-9d02-e2589a7c0aa0)
 Call ID: 2352a663-afd0-4ffc-9d02-e2589a7c0aa0
  Args:
    target: Feodora_of_Hohenlohe-Langenburg
    relation: :hasMother
    source: Prince_Frederick_John_of_Saxe-Meiningen
  AddTriple (d40bd970-f007-45fd-b2a3-714536ab36ad)
 Call ID: d40bd970-f007-45fd-b2a3-714536ab36ad
  Args:
    source: Princess_Adelaide_of_Saxe-Meiningen
    relation: :isSiblingOf
    target: Prince_George
  AddTriple (535722e0-06c5-430c-9473-48253ab9bb1b)
 Call ID: 535722e0-06c5-430c-9473-48253ab9bb1b
  Args:
    source: Princess_Adelaide_of_Saxe-Meiningen
    relation: :isSiblingOf
    target: Prince_Bernard
  AddTriple (d95beeca-4f95-4738-88a5-a5a0225b18fc)
 Call ID: d95beeca-4f95-4738-88a5-a5a0225b18fc
  Args:
    target: Ernst_Count_of_Lippe-Biesterfeld
    source: Countess_Adelaide_of_Lippe-Biesterfeld
    relation: :hasFather
  AddLiteral (4d18b19a-57ed-4ba4-983a-7f1459ba9f11)
 Call ID: 4d18b19a-57ed-4ba4-983a-7f1459ba9f11
  Args:
    relation: :hasMarriageYear
    source: Princess_Adelaide_of_Saxe-Meiningen
    literal_value: 1914
    literal_type: xsd:integer
  AddTriple (416a66c0-b53f-4cb8-9a7e-9aa721d17673)
 Call ID: 416a66c0-b53f-4cb8-9a7e-9aa721d17673
  Args:
    relation: :hasFather
    source: Prince_Adalbert_of_Prussia
    target: Kaiser_William_II_of_Germany
  AddTriple (ea072680-b98b-4952-83d1-aaea29992659)
 Call ID: ea072680-b98b-4952-83d1-aaea29992659
  Args:
    relation: :hasFather
    source: Prince_Henry_of_Bavaria
    target: Ludwig_III_of_Bavaria
  Finish (c251ac1b-87f9-423a-9211-83afeb6bf322)
 Call ID: c251ac1b-87f9-423a-9211-83afeb6bf322
  Args: