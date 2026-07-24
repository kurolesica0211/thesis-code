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
Princess Cecilie of Prussia (Cecilie Viktoria Anastasia Zita Thyra Adelheid; 5 September 1917 – 21 April 1975) was a member of the House of Hohenzollern.
She was the younger daughter and sixth child of Wilhelm, German Crown Prince, and Duchess Cecilie of Mecklenburg-Schwerin.
Early life

Cecilie was born on 5 September 1917 at Cecilienhof Palace in Potsdam, which had only been completed weeks prior to her birth, during World War I and the reign of paternal grandfather, Wilhelm II, as German Emperor and King of Prussia.
One year after her birth, on 9 November 1918, her grandfather and other German monarchs abdicated and the German Empire was abolished.
Cecilienhof was returned to Cecilie's family in 1926.
During World War II, Cecilie worked at a pharmacy in Potsdam and trained as a nurse with the German Red Cross.
As the Red Army descended on Potsdam at the end of the war, Cecilie was sent to live with Hessian relatives at Schloss Wolfsgarten.
There, she met American Captain Clyde Kenneth Harris, a member of the Monuments, Fine Arts, and Archives Unit who was investigating the Darmstadt Madonna for her cousin, Ludwig, Prince of Hesse and by Rhine.
Prince Vsevolod of Russia proposed to her twice, but she declined both times.
Marriage and family

Cecilie and Harris were married on 21 June 1949 at Hohenzollern Castle.
They had one daughter, Kira Alexandrine Brigid Cecilie Ingrid Harris (born 20 October 1954) who married John Mitchell Johnson (12 May 1951 Dallas, Texas-) and had one son, Philip Louis Johnson (18 Oct 1985 Fort Worth, Texas-).
While visiting family in Germany, Cecilie died in Königstein im Taunus on 21 April 1975, aged 57.



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
  AssignClass (614f7361-16ce-4afe-b605-67b6c6e98bda)
 Call ID: 614f7361-16ce-4afe-b605-67b6c6e98bda
  Args:
    source: Cecilie_of_Prussia
    type: :Woman
  AssignClass (e9f4ca05-e180-473a-8805-2b1b583deabc)
 Call ID: e9f4ca05-e180-473a-8805-2b1b583deabc
  Args:
    type: :Person
    source: Cecilie_of_Prussia
  AddLiteral (dcca1c3a-a989-4815-b176-35aa5278eb91)
 Call ID: dcca1c3a-a989-4815-b176-35aa5278eb91
  Args:
    source: Cecilie_of_Prussia
    literal_value: 1917
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (e97c9a5e-d3fc-441d-ba42-cbe75ae7582e)
 Call ID: e97c9a5e-d3fc-441d-ba42-cbe75ae7582e
  Args:
    source: Cecilie_of_Prussia
    literal_value: 1975
    relation: :hasDeathYear
    literal_type: xsd:integer
  AssignClass (11ff16e6-da9f-43c3-85a2-04e228b995b8)
 Call ID: 11ff16e6-da9f-43c3-85a2-04e228b995b8
  Args:
    source: Wilhelm_German_Crown_Prince
    type: :Man
  AssignClass (78a6e7da-f90f-475a-ba08-ed8e10ffa6f0)
 Call ID: 78a6e7da-f90f-475a-ba08-ed8e10ffa6f0
  Args:
    source: Wilhelm_German_Crown_Prince
    type: :Person
  AssignClass (5de122f3-7390-4220-b46a-3e9bf2b33acd)
 Call ID: 5de122f3-7390-4220-b46a-3e9bf2b33acd
  Args:
    type: :Woman
    source: Duchess_Cecilie_of_Mecklenburg-Schwerin
  AssignClass (5e9c7507-226f-4ad9-8c0b-178e089d5f9f)
 Call ID: 5e9c7507-226f-4ad9-8c0b-178e089d5f9f
  Args:
    source: Duchess_Cecilie_of_Mecklenburg-Schwerin
    type: :Person
  AddTriple (e0ed82ef-43c0-4a30-b63a-e3119f73cfeb)
 Call ID: e0ed82ef-43c0-4a30-b63a-e3119f73cfeb
  Args:
    source: Cecilie_of_Prussia
    target: Wilhelm_German_Crown_Prince
    relation: :hasFather
  AddTriple (cfbc13ed-ae32-49d7-96a1-fdecfa301690)
 Call ID: cfbc13ed-ae32-49d7-96a1-fdecfa301690
  Args:
    source: Cecilie_of_Prussia
    relation: :hasMother
    target: Duchess_Cecilie_of_Mecklenburg-Schwerin
  AssignClass (d5eeb1db-8e1c-4841-bb4f-e77c50a9cf8a)
 Call ID: d5eeb1db-8e1c-4841-bb4f-e77c50a9cf8a
  Args:
    source: Clyde_Kenneth_Harris
    type: :Man
  AssignClass (dfd50249-8902-46d6-ac00-fb8c5ca34108)
 Call ID: dfd50249-8902-46d6-ac00-fb8c5ca34108
  Args:
    type: :Person
    source: Clyde_Kenneth_Harris
  AddTriple (8ca918fd-e3c6-44a6-a1c3-69d2d7e40c84)
 Call ID: 8ca918fd-e3c6-44a6-a1c3-69d2d7e40c84
  Args:
    source: Cecilie_of_Prussia
    target: Clyde_Kenneth_Harris
    relation: :hasRelation
  AddLiteral (a0c7e999-523a-4da5-a90a-f74642af3a64)
 Call ID: a0c7e999-523a-4da5-a90a-f74642af3a64
  Args:
    source: Cecilie_of_Prussia
    literal_value: 1949
    relation: :hasMarriageYear
    literal_type: xsd:integer
  AssignClass (bfaca23c-ae5b-4eb2-b00c-6460e6288101)
 Call ID: bfaca23c-ae5b-4eb2-b00c-6460e6288101
  Args:
    source: Kira_Alexandrine_Brigid_Cecilie_Ingrid_Harris
    type: :Woman
  AssignClass (10e8bab4-2794-41bf-bb1e-4a1628d7f1ae)
 Call ID: 10e8bab4-2794-41bf-bb1e-4a1628d7f1ae
  Args:
    type: :Person
    source: Kira_Alexandrine_Brigid_Cecilie_Ingrid_Harris
  AddTriple (c6ea8c92-64c4-4b18-847f-e2e008550763)
 Call ID: c6ea8c92-64c4-4b18-847f-e2e008550763
  Args:
    target: Cecilie_of_Prussia
    relation: :hasMother
    source: Kira_Alexandrine_Brigid_Cecilie_Ingrid_Harris
  AddTriple (2a0cf97c-3414-4a2f-82b7-4d87c689ebdd)
 Call ID: 2a0cf97c-3414-4a2f-82b7-4d87c689ebdd
  Args:
    relation: :hasFather
    target: Clyde_Kenneth_Harris
    source: Kira_Alexandrine_Brigid_Cecilie_Ingrid_Harris
  AssignClass (788f5416-53b7-4bd9-9671-6cae77d2c235)
 Call ID: 788f5416-53b7-4bd9-9671-6cae77d2c235
  Args:
    source: John_Mitchell_Johnson
    type: :Man
  AssignClass (241234fc-d73e-4e94-88a2-46f9ff296a71)
 Call ID: 241234fc-d73e-4e94-88a2-46f9ff296a71
  Args:
    source: John_Mitchell_Johnson
    type: :Person
  AddTriple (d5bc7d78-cff2-43ff-a5c4-7a3e870247fe)
 Call ID: d5bc7d78-cff2-43ff-a5c4-7a3e870247fe
  Args:
    relation: :hasRelation
    target: John_Mitchell_Johnson
    source: Kira_Alexandrine_Brigid_Cecilie_Ingrid_Harris
  AssignClass (4dd7bc9c-1e36-4b01-b9e3-960ec8b0dda2)
 Call ID: 4dd7bc9c-1e36-4b01-b9e3-960ec8b0dda2
  Args:
    source: Philip_Louis_Johnson
    type: :Man
  AssignClass (42886cbe-23ab-4b10-9f6b-d5c9b8375710)
 Call ID: 42886cbe-23ab-4b10-9f6b-d5c9b8375710
  Args:
    type: :Person
    source: Philip_Louis_Johnson
  AddTriple (516709d9-f12d-45ad-a8f6-0c97c403291e)
 Call ID: 516709d9-f12d-45ad-a8f6-0c97c403291e
  Args:
    source: Philip_Louis_Johnson
    target: Kira_Alexandrine_Brigid_Cecilie_Ingrid_Harris
    relation: :hasMother
  AddTriple (507fe1fb-cf6b-40b1-9ac4-a9eedb729fbc)
 Call ID: 507fe1fb-cf6b-40b1-9ac4-a9eedb729fbc
  Args:
    target: John_Mitchell_Johnson
    relation: :hasFather
    source: Philip_Louis_Johnson
  Finish (d061e987-a3d6-42f8-9acf-b6ba9f9c780c)
 Call ID: d061e987-a3d6-42f8-9acf-b6ba9f9c780c
  Args: