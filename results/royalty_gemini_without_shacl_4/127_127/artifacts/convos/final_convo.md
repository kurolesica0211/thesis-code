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
Countess Adelaide of Lippe-Biesterfeld (22 June 1870 – 3 September 1948) was the eldest child of Ernest II, Count of Lippe-Biesterfeld and Countess Karoline von Wartensleben.
Family and early life

Adelaide was born on 22 June 1870 to Ernest II, Count of Lippe-Biesterfeld and his wife, Countess Karoline von Wartensleben.
After the death of Woldemar, Prince of Lippe in 1895, her parents were involved in a regency and succession dispute to the principality of Lippe.
Consequently, two branches of the House of Lippe argued over rights to a regency.
Prince Adolf of Schaumburg-Lippe, a brother-in-law of Wilhelm II, German Emperor was chosen, but a court-settlement allowed Ernest to become the regent of Lippe-Detmold on 17 July 1897.
Marriage and issue

At Neudorf, Adelaide married Prince Friedrich Johann of Saxe-Meiningen, son of Georg II, Duke of Saxe-Meiningen, on 24 April 1889.
They had six children together:


Role in Lippe succession dispute

Two branches of the House of Lippe debated over rights to the principality of Lippe-Detmold.
As Adelaide's great-grandmother was a member of the lower nobility (Modeste Christiane von Unruh) and has one quarter commoner ancestry, her family's claim to full royalty was challenged.
This claim threatened the succession to Saxe-Meiningen, as Adelaide was married to the Duke of Saxe-Meiningen's heir apparent; were her father deemed a lesser royal status, it might be thought that her own claim was not equal enough for her husband's family.



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
  AssignClass (a65a7085-7649-40fc-86fa-9f7ae0e36c25)
 Call ID: a65a7085-7649-40fc-86fa-9f7ae0e36c25
  Args:
    type: :Woman
    source: Adelaide_of_Lippe-Biesterfeld
  AssignClass (1b5b08c6-633a-4a0b-8c81-d6ea2c6e7304)
 Call ID: 1b5b08c6-633a-4a0b-8c81-d6ea2c6e7304
  Args:
    type: :Person
    source: Adelaide_of_Lippe-Biesterfeld
  AddLiteral (2b071013-e32d-4935-be28-e849aaa2e9a8)
 Call ID: 2b071013-e32d-4935-be28-e849aaa2e9a8
  Args:
    literal_value: 1870
    literal_type: xsd:nonNegativeInteger
    source: Adelaide_of_Lippe-Biesterfeld
    relation: :hasBirthYear
  AddLiteral (d20d8273-8098-4c92-adf0-1fd196b01a42)
 Call ID: d20d8273-8098-4c92-adf0-1fd196b01a42
  Args:
    source: Adelaide_of_Lippe-Biesterfeld
    relation: :hasDeathYear
    literal_type: xsd:nonNegativeInteger
    literal_value: 1948
  AssignClass (f8ab795b-985f-48f8-984e-d22f50a73ad9)
 Call ID: f8ab795b-985f-48f8-984e-d22f50a73ad9
  Args:
    type: :Man
    source: Ernest_II_of_Lippe-Biesterfeld
  AssignClass (ec3764fc-2202-41e3-b4d2-c297b2ebb470)
 Call ID: ec3764fc-2202-41e3-b4d2-c297b2ebb470
  Args:
    type: :Ancestor
    source: Ernest_II_of_Lippe-Biesterfeld
  AssignClass (e28eb1da-1caa-40eb-9c0b-e64aee5d08f6)
 Call ID: e28eb1da-1caa-40eb-9c0b-e64aee5d08f6
  Args:
    type: :Person
    source: Ernest_II_of_Lippe-Biesterfeld
  AssignClass (38d18efb-65d3-41df-b5ae-d95d50a4ecbc)
 Call ID: 38d18efb-65d3-41df-b5ae-d95d50a4ecbc
  Args:
    type: :Woman
    source: Karoline_von_Wartensleben
  AssignClass (899feb15-3834-4282-853e-df4bae1c62ab)
 Call ID: 899feb15-3834-4282-853e-df4bae1c62ab
  Args:
    type: :Ancestor
    source: Karoline_von_Wartensleben
  AssignClass (928ad908-2903-4cba-8571-b5624241fddd)
 Call ID: 928ad908-2903-4cba-8571-b5624241fddd
  Args:
    type: :Person
    source: Karoline_von_Wartensleben
  AddTriple (21460196-40e3-4621-98aa-a4b978340e9d)
 Call ID: 21460196-40e3-4621-98aa-a4b978340e9d
  Args:
    target: Ernest_II_of_Lippe-Biesterfeld
    source: Adelaide_of_Lippe-Biesterfeld
    relation: :hasFather
  AddTriple (3e3611cb-8bb1-45ff-a004-294046c2bd4f)
 Call ID: 3e3611cb-8bb1-45ff-a004-294046c2bd4f
  Args:
    relation: :hasMother
    source: Adelaide_of_Lippe-Biesterfeld
    target: Karoline_von_Wartensleben
  AssignClass (0797ca63-75b5-4239-bead-03fde23eaaa6)
 Call ID: 0797ca63-75b5-4239-bead-03fde23eaaa6
  Args:
    type: :Man
    source: Friedrich_Johann_of_Saxe-Meiningen
  AssignClass (3ac7bf4e-aada-4c7c-a089-866128a58487)
 Call ID: 3ac7bf4e-aada-4c7c-a089-866128a58487
  Args:
    type: :Person
    source: Friedrich_Johann_of_Saxe-Meiningen
  AddLiteral (a57ce791-200e-42d1-ad04-48d2d50a5fb0)
 Call ID: a57ce791-200e-42d1-ad04-48d2d50a5fb0
  Args:
    relation: :hasMarriageYear
    source: Adelaide_of_Lippe-Biesterfeld
    literal_value: 1889
    literal_type: xsd:nonNegativeInteger
  AddTriple (d2e203c7-7fc1-4387-befb-4fc885200e53)
 Call ID: d2e203c7-7fc1-4387-befb-4fc885200e53
  Args:
    target: Friedrich_Johann_of_Saxe-Meiningen
    relation: :hasRelation
    source: Adelaide_of_Lippe-Biesterfeld
  AssignClass (383e31e7-6fc8-43d3-8a2f-fd30b5a80ac0)
 Call ID: 383e31e7-6fc8-43d3-8a2f-fd30b5a80ac0
  Args:
    type: :Man
    source: Georg_II_of_Saxe-Meiningen
  AssignClass (9d9e1003-7766-40bf-b254-1b3a5641f9d3)
 Call ID: 9d9e1003-7766-40bf-b254-1b3a5641f9d3
  Args:
    type: :Ancestor
    source: Georg_II_of_Saxe-Meiningen
  AssignClass (57d5e69e-a5b6-4ddf-a440-f924898ba521)
 Call ID: 57d5e69e-a5b6-4ddf-a440-f924898ba521
  Args:
    type: :Person
    source: Georg_II_of_Saxe-Meiningen
  AddTriple (098934aa-9e67-4d1e-ab74-3cb8ad09faff)
 Call ID: 098934aa-9e67-4d1e-ab74-3cb8ad09faff
  Args:
    target: Georg_II_of_Saxe-Meiningen
    relation: :hasFather
    source: Friedrich_Johann_of_Saxe-Meiningen
  AssignClass (e618611e-2653-4309-84e9-64ca349c619b)
 Call ID: e618611e-2653-4309-84e9-64ca349c619b
  Args:
    type: :Woman
    source: Modeste_Christiane_von_Unruh
  AssignClass (63bc895d-5be2-4c17-9757-e036eda392d7)
 Call ID: 63bc895d-5be2-4c17-9757-e036eda392d7
  Args:
    type: :Ancestor
    source: Modeste_Christiane_von_Unruh
  AssignClass (95f8398f-5f98-43e4-8bc8-99cc7e0b562d)
 Call ID: 95f8398f-5f98-43e4-8bc8-99cc7e0b562d
  Args:
    type: :Person
    source: Modeste_Christiane_von_Unruh
  AddTriple (7b2297f5-f3cc-4ce9-a2c7-20e0564ec6c7)
 Call ID: 7b2297f5-f3cc-4ce9-a2c7-20e0564ec6c7
  Args:
    relation: :hasAncestor
    source: Adelaide_of_Lippe-Biesterfeld
    target: Modeste_Christiane_von_Unruh
  Finish (ec29aa2c-0a46-4ce5-b458-e9d0ea22d9e3)
 Call ID: ec29aa2c-0a46-4ce5-b458-e9d0ea22d9e3
  Args: