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
Nikolaus, Hereditary Grand Duke of Oldenburg (German: Nikolaus Friedrich Wilhelm von Holstein-Gottorp, Erbgroßherzog von Oldenburg; 10 August 1897 – 3 April 1970) was the eldest son of Frederick Augustus II, Grand Duke of Oldenburg, who was the last ruling Grand Duke of Oldenburg.
In 1931, Nikolaus succeeded to his father's titles and assumed the role of pretender to the Grand Duchy, until his death in 1970.
Early life

Nikolaus was born at Oldenburg, Grand Duchy of Oldenburg, the third child and first son of Frederick Augustus II, Grand Duke of Oldenburg (1852–1931) (son of Peter II, Grand Duke of Oldenburg and Princess Elisabeth of Saxe-Altenburg) and his wife, Duchess Elisabeth Alexandrine of Mecklenburg-Schwerin (1869–1955) (daughter of Frederick Francis II, Grand Duke of Mecklenburg-Schwerin and Princess Marie of Schwarzburg-Rudolstadt).
Marriage and issue

Nikolaus married on 26 October 1921 in Arolsen to Princess Helena of Waldeck and Pyrmont (1899–1948), only daughter of Friedrich, Prince of Waldeck and Pyrmont, and Princess Bathildis of Schaumburg-Lippe.
They had nine children:


When his first wife died in 1948, he married secondly on 20 September 1950 in Güldenstein to a fellow noblewoman, Anne-Marie von Schutzbar genannt Milchling (1903–1991), former wife of Count Bechtold von Bernstorff, daughter of Rudolf von Schutzbar gen. Milchling (1853-1935) and Rose Marston (1872-1957).



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
  AssignClass (001a878e-b47c-4bc7-bb33-fcb0008bd5a6)
 Call ID: 001a878e-b47c-4bc7-bb33-fcb0008bd5a6
  Args:
    type: :Man
    source: Nikolaus
  AssignClass (f5babc22-d323-4125-a246-fc42cdbadb0b)
 Call ID: f5babc22-d323-4125-a246-fc42cdbadb0b
  Args:
    type: :Person
    source: Nikolaus
  AddLiteral (5f004276-141e-4f43-918b-7e0d6b01ffee)
 Call ID: 5f004276-141e-4f43-918b-7e0d6b01ffee
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Nikolaus
    literal_value: 1897
  AddLiteral (9dc7a6d2-5416-4984-a57e-e70a66357429)
 Call ID: 9dc7a6d2-5416-4984-a57e-e70a66357429
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 1970
    source: Nikolaus
  AssignClass (48fa3f63-59c8-45e0-b5e5-64d0e542d231)
 Call ID: 48fa3f63-59c8-45e0-b5e5-64d0e542d231
  Args:
    type: :Man
    source: FrederickAugustusII
  AssignClass (3213fc24-a371-40c2-94bf-a927fe78651c)
 Call ID: 3213fc24-a371-40c2-94bf-a927fe78651c
  Args:
    type: :Person
    source: FrederickAugustusII
  AddLiteral (ccf46a9a-eb0e-436f-9e4e-e4fa07a84c1e)
 Call ID: ccf46a9a-eb0e-436f-9e4e-e4fa07a84c1e
  Args:
    literal_value: 1852
    source: FrederickAugustusII
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (ee5f98f4-3839-4d27-a885-dfa2869164ac)
 Call ID: ee5f98f4-3839-4d27-a885-dfa2869164ac
  Args:
    literal_value: 1931
    source: FrederickAugustusII
    literal_type: xsd:integer
    relation: :hasDeathYear
  AddTriple (f5de9cef-4491-4db0-a944-f28034b4cc92)
 Call ID: f5de9cef-4491-4db0-a944-f28034b4cc92
  Args:
    source: Nikolaus
    target: FrederickAugustusII
    relation: :isSonOf
  AssignClass (7031a606-0d69-46c7-a6c8-3cf2dae4b963)
 Call ID: 7031a606-0d69-46c7-a6c8-3cf2dae4b963
  Args:
    type: :Man
    source: PeterII
  AssignClass (66370eeb-9843-4793-87bc-85826b8d8c96)
 Call ID: 66370eeb-9843-4793-87bc-85826b8d8c96
  Args:
    type: :Person
    source: PeterII
  AssignClass (c13fe0e0-a919-4d22-9dc6-ec680739a0b4)
 Call ID: c13fe0e0-a919-4d22-9dc6-ec680739a0b4
  Args:
    type: :Woman
    source: ElisabethSaxeAltenburg
  AssignClass (b579dce5-e745-4762-a5c2-069a3013a645)
 Call ID: b579dce5-e745-4762-a5c2-069a3013a645
  Args:
    type: :Person
    source: ElisabethSaxeAltenburg
  AddTriple (75ceadce-812b-4568-84b5-24bf70639c07)
 Call ID: 75ceadce-812b-4568-84b5-24bf70639c07
  Args:
    relation: :isSonOf
    target: PeterII
    source: FrederickAugustusII
  AddTriple (6dae6cec-6b19-44c0-94c9-0b9784de2a80)
 Call ID: 6dae6cec-6b19-44c0-94c9-0b9784de2a80
  Args:
    relation: :hasMother
    source: FrederickAugustusII
    target: ElisabethSaxeAltenburg
  AssignClass (689d2353-d159-4c8b-9abd-aa63b293dd85)
 Call ID: 689d2353-d159-4c8b-9abd-aa63b293dd85
  Args:
    type: :Woman
    source: ElisabethAlexandrineMecklenburgSchwerin
  AssignClass (83f77d56-099f-4f10-9c05-6681f0d239c7)
 Call ID: 83f77d56-099f-4f10-9c05-6681f0d239c7
  Args:
    type: :Person
    source: ElisabethAlexandrineMecklenburgSchwerin
  AddLiteral (bdc7d4d2-231f-4e7d-a8f7-aee7fa1043dd)
 Call ID: bdc7d4d2-231f-4e7d-a8f7-aee7fa1043dd
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: ElisabethAlexandrineMecklenburgSchwerin
    literal_value: 1869
  AddLiteral (054b921a-3db2-45b7-af90-0616ccfc18a8)
 Call ID: 054b921a-3db2-45b7-af90-0616ccfc18a8
  Args:
    source: ElisabethAlexandrineMecklenburgSchwerin
    literal_value: 1955
    literal_type: xsd:integer
    relation: :hasDeathYear
  AddTriple (ba8e9bb9-b0c1-45c6-961b-ca3cd9a1e127)
 Call ID: ba8e9bb9-b0c1-45c6-961b-ca3cd9a1e127
  Args:
    relation: :hasMother
    source: Nikolaus
    target: ElisabethAlexandrineMecklenburgSchwerin
  AssignClass (90c96d47-112c-43e3-8eaf-080f77a9edd2)
 Call ID: 90c96d47-112c-43e3-8eaf-080f77a9edd2
  Args:
    type: :Man
    source: FrederickFrancisII
  AssignClass (00408567-da84-4d4d-99e9-25697a380137)
 Call ID: 00408567-da84-4d4d-99e9-25697a380137
  Args:
    type: :Person
    source: FrederickFrancisII
  AssignClass (a148548e-b80c-4e26-8393-24eaddcb0b55)
 Call ID: a148548e-b80c-4e26-8393-24eaddcb0b55
  Args:
    type: :Woman
    source: MarieSchwarzburgRudolstadt
  AssignClass (0f134117-dcff-49b4-be47-6729ac28aa85)
 Call ID: 0f134117-dcff-49b4-be47-6729ac28aa85
  Args:
    type: :Person
    source: MarieSchwarzburgRudolstadt
  AddTriple (6ea3bd7c-35c2-47f0-8932-dcf75534d6fb)
 Call ID: 6ea3bd7c-35c2-47f0-8932-dcf75534d6fb
  Args:
    relation: :isDaughterOf
    source: ElisabethAlexandrineMecklenburgSchwerin
    target: FrederickFrancisII
  AddTriple (480f8a7c-ea8c-430e-8dba-e2c2c318d3ad)
 Call ID: 480f8a7c-ea8c-430e-8dba-e2c2c318d3ad
  Args:
    source: ElisabethAlexandrineMecklenburgSchwerin
    target: MarieSchwarzburgRudolstadt
    relation: :hasMother
  AssignClass (ce3767ca-e850-43ef-813f-26ddf5b6209d)
 Call ID: ce3767ca-e850-43ef-813f-26ddf5b6209d
  Args:
    type: :Woman
    source: HelenaWaldeckPyrmont
  AssignClass (697f6010-05eb-4df6-be2b-9065a8b3fca3)
 Call ID: 697f6010-05eb-4df6-be2b-9065a8b3fca3
  Args:
    type: :Person
    source: HelenaWaldeckPyrmont
  AddLiteral (ff7f1aa4-38f8-405f-8cb9-0d89731cd873)
 Call ID: ff7f1aa4-38f8-405f-8cb9-0d89731cd873
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: HelenaWaldeckPyrmont
    literal_value: 1899
  AddLiteral (292d5e41-2184-4c40-a1b3-5334db5a247e)
 Call ID: 292d5e41-2184-4c40-a1b3-5334db5a247e
  Args:
    literal_value: 1948
    source: HelenaWaldeckPyrmont
    relation: :hasDeathYear
    literal_type: xsd:integer
  AddLiteral (dfec4f30-11f4-4be9-bbfa-3442dc40ead0)
 Call ID: dfec4f30-11f4-4be9-bbfa-3442dc40ead0
  Args:
    source: Nikolaus
    literal_value: 1921
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AddTriple (75d1ab6d-7865-4b94-af57-d9208a077dbd)
 Call ID: 75d1ab6d-7865-4b94-af57-d9208a077dbd
  Args:
    source: Nikolaus
    target: HelenaWaldeckPyrmont
    relation: :hasRelation
  AssignClass (7a422bee-53a5-46d2-abeb-525d4266fa3e)
 Call ID: 7a422bee-53a5-46d2-abeb-525d4266fa3e
  Args:
    type: :Man
    source: FriedrichWaldeckPyrmont
  AssignClass (0543e235-c5ff-43a2-ba51-eaef5b0e9a34)
 Call ID: 0543e235-c5ff-43a2-ba51-eaef5b0e9a34
  Args:
    type: :Person
    source: FriedrichWaldeckPyrmont
  AssignClass (f3521a91-4ae5-41b1-9260-8970b9b7314a)
 Call ID: f3521a91-4ae5-41b1-9260-8970b9b7314a
  Args:
    type: :Woman
    source: BathildisSchaumburgLippe
  AssignClass (9f8ca0e2-ae1f-4f8e-b468-8e84bcb13a89)
 Call ID: 9f8ca0e2-ae1f-4f8e-b468-8e84bcb13a89
  Args:
    type: :Person
    source: BathildisSchaumburgLippe
  AddTriple (86725b79-4efe-4142-9106-23c3544392da)
 Call ID: 86725b79-4efe-4142-9106-23c3544392da
  Args:
    relation: :isDaughterOf
    target: FriedrichWaldeckPyrmont
    source: HelenaWaldeckPyrmont
  AddTriple (7e7c2b91-d382-4f26-906b-da42b8337f62)
 Call ID: 7e7c2b91-d382-4f26-906b-da42b8337f62
  Args:
    target: BathildisSchaumburgLippe
    source: HelenaWaldeckPyrmont
    relation: :hasMother
  AssignClass (c6f6b28a-34b2-4b5f-8a88-83e134c2dc59)
 Call ID: c6f6b28a-34b2-4b5f-8a88-83e134c2dc59
  Args:
    type: :Woman
    source: AnneMarieSchutzbarMilchling
  AssignClass (24ca1713-2786-4d84-8e61-727722c5121b)
 Call ID: 24ca1713-2786-4d84-8e61-727722c5121b
  Args:
    type: :Person
    source: AnneMarieSchutzbarMilchling
  AddLiteral (44a3d54b-4687-4906-bc7f-c969f5d3cdde)
 Call ID: 44a3d54b-4687-4906-bc7f-c969f5d3cdde
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: AnneMarieSchutzbarMilchling
    literal_value: 1903
  AddLiteral (96cc937e-16d9-4f6d-947e-832dd77af937)
 Call ID: 96cc937e-16d9-4f6d-947e-832dd77af937
  Args:
    literal_value: 1991
    source: AnneMarieSchutzbarMilchling
    relation: :hasDeathYear
    literal_type: xsd:integer
  AddLiteral (1395aa6a-72c6-4e42-9585-cbb793dcc340)
 Call ID: 1395aa6a-72c6-4e42-9585-cbb793dcc340
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 1950
    source: Nikolaus
  AddTriple (96d85e75-530c-497e-b388-91d95d120838)
 Call ID: 96d85e75-530c-497e-b388-91d95d120838
  Args:
    target: AnneMarieSchutzbarMilchling
    source: Nikolaus
    relation: :hasRelation
  AssignClass (1159f6b0-ba98-48ed-82c0-d20e423e6f55)
 Call ID: 1159f6b0-ba98-48ed-82c0-d20e423e6f55
  Args:
    type: :Man
    source: BechtoldBernstorff
  AssignClass (857445a8-cc6b-4c79-99f0-aa34a428adcb)
 Call ID: 857445a8-cc6b-4c79-99f0-aa34a428adcb
  Args:
    type: :Person
    source: BechtoldBernstorff
  AddTriple (ea9b7519-2342-48c9-af72-850afc866cc2)
 Call ID: ea9b7519-2342-48c9-af72-850afc866cc2
  Args:
    relation: :hasRelation
    target: BechtoldBernstorff
    source: AnneMarieSchutzbarMilchling
  AssignClass (d989d02e-4ede-425e-b726-b9972482a3ed)
 Call ID: d989d02e-4ede-425e-b726-b9972482a3ed
  Args:
    type: :Man
    source: RudolfSchutzbarMilchling
  AssignClass (dc667afb-0eef-45e6-b1da-7b3b29e67147)
 Call ID: dc667afb-0eef-45e6-b1da-7b3b29e67147
  Args:
    type: :Person
    source: RudolfSchutzbarMilchling
  AddLiteral (883ff4b6-2c01-468e-bb9c-712b9212449c)
 Call ID: 883ff4b6-2c01-468e-bb9c-712b9212449c
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1853
    source: RudolfSchutzbarMilchling
  AddLiteral (fdbd7f61-1679-4961-baaf-f29fa9f2b554)
 Call ID: fdbd7f61-1679-4961-baaf-f29fa9f2b554
  Args:
    literal_value: 1935
    source: RudolfSchutzbarMilchling
    relation: :hasDeathYear
    literal_type: xsd:integer
  AssignClass (a5c843de-6cbd-44ac-aa58-df27d6dda0aa)
 Call ID: a5c843de-6cbd-44ac-aa58-df27d6dda0aa
  Args:
    type: :Woman
    source: RoseMarston
  AssignClass (a8d8586a-38bb-444b-9abe-8b09f89df193)
 Call ID: a8d8586a-38bb-444b-9abe-8b09f89df193
  Args:
    type: :Person
    source: RoseMarston
  AddLiteral (3fbabd87-cc99-4f20-a895-9cb59b60a27f)
 Call ID: 3fbabd87-cc99-4f20-a895-9cb59b60a27f
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: RoseMarston
    literal_value: 1872
  AddLiteral (0c4147e8-47ca-4a28-b513-163b6f3b663d)
 Call ID: 0c4147e8-47ca-4a28-b513-163b6f3b663d
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: RoseMarston
    literal_value: 1957
  AddTriple (7e3dfa8c-6272-4cc9-b827-e59f82f431f7)
 Call ID: 7e3dfa8c-6272-4cc9-b827-e59f82f431f7
  Args:
    source: AnneMarieSchutzbarMilchling
    target: RudolfSchutzbarMilchling
    relation: :isDaughterOf
  AddTriple (8af18bfb-e2dd-44c7-aaca-f168079485bb)
 Call ID: 8af18bfb-e2dd-44c7-aaca-f168079485bb
  Args:
    target: RoseMarston
    source: AnneMarieSchutzbarMilchling
    relation: :hasMother
  Finish (4b91f9ca-384e-4396-8d96-28d0cc19ae14)
 Call ID: 4b91f9ca-384e-4396-8d96-28d0cc19ae14
  Args: