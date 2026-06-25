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
Prince Wolfgang of Hesse (Wolfgang Moritz Prinz von Hessen; 6 November 1896 – 12 July 1989) was the district administrator of Obertaunuskreis from 1933 to 1945.
Wolfgang was born at Castle Rumpenheim, Offenbach am Main, the fourth son of Prince Frederick Charles of Hesse (1868–1940) and Princess Margaret of Prussia (1872–1954).
His maternal uncle was the German Emperor Willhelm II.
In World War I, Wolfgang served as an officer in the command of Field Marshal August von Mackensen.
Towards the end of the war, Wolfgang's father Frederick Charles of Hesse was selected by the Central Powers as a prospective King of Finland on 9 October 1918, to replace his first cousin once removed, the deposed Russian emperor, Nicholas II, who was titled Grand Duke of Finland.
Wolfgang was designated heir, in preference to his elder twin brother Philipp to ensure the separation of the thrones of Hesse and Finland.
However, Frederick Charles renounced his candidature on 14 December 1918, and the title was never actually held by the family.
Wolfgang married on 17 September 1924 Princess Marie Alexandra of Baden (1902–1944), daughter of Prince Maximilian of Baden and Princess Marie Louise of Hanover; they had no children.
He joined the NSDAP and the SA in December 1933, and was appointed Landrat (district administrator) of Obertaunuskreis, a landkreis in the state of Hesse, serving in that capacity until the end of  World War II.



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
  AssignClass (c94273db-a641-4fd3-a3a1-2d7be95e9f17)
 Call ID: c94273db-a641-4fd3-a3a1-2d7be95e9f17
  Args:
    source: Wolfgang_of_Hesse
    type: :Man
  AddLiteral (b09093ef-4133-448b-9e69-ce689d50e6ed)
 Call ID: b09093ef-4133-448b-9e69-ce689d50e6ed
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Wolfgang_of_Hesse
    literal_value: 1896
  AddLiteral (83c73356-aa80-4462-a445-713bccc16a9c)
 Call ID: 83c73356-aa80-4462-a445-713bccc16a9c
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: Wolfgang_of_Hesse
    literal_value: 1989
  AddLiteral (11cc20ef-8caa-445e-80f1-046844334268)
 Call ID: 11cc20ef-8caa-445e-80f1-046844334268
  Args:
    source: Wolfgang_of_Hesse
    literal_value: Wolfgang Moritz Prinz von Hessen
    relation: :alsoKnownAs
    literal_type: xsd:string
  AssignClass (85406583-07e2-49f5-8ac8-68b9999495ce)
 Call ID: 85406583-07e2-49f5-8ac8-68b9999495ce
  Args:
    type: :Man
    source: Frederick_Charles_of_Hesse
  AddLiteral (ea6cc70b-02ee-4ce7-9fad-b3274bf8fbe6)
 Call ID: ea6cc70b-02ee-4ce7-9fad-b3274bf8fbe6
  Args:
    source: Frederick_Charles_of_Hesse
    literal_value: 1868
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (77693831-e887-44af-817a-71c9a0958cc4)
 Call ID: 77693831-e887-44af-817a-71c9a0958cc4
  Args:
    source: Frederick_Charles_of_Hesse
    literal_value: 1940
    relation: :hasDeathYear
    literal_type: xsd:integer
  AssignClass (9071f47e-e939-418a-adb9-75c8a8a2a943)
 Call ID: 9071f47e-e939-418a-adb9-75c8a8a2a943
  Args:
    type: :Woman
    source: Margaret_of_Prussia
  AddLiteral (e7d054a2-0f1e-4223-a0cb-5af7be94f9f9)
 Call ID: e7d054a2-0f1e-4223-a0cb-5af7be94f9f9
  Args:
    source: Margaret_of_Prussia
    literal_value: 1872
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (5e511b9b-abb5-41ff-b737-72d1adb8e256)
 Call ID: 5e511b9b-abb5-41ff-b737-72d1adb8e256
  Args:
    source: Margaret_of_Prussia
    literal_value: 1954
    relation: :hasDeathYear
    literal_type: xsd:integer
  AddTriple (c399a9d2-21bf-48ee-8e0e-85635d2d6e2d)
 Call ID: c399a9d2-21bf-48ee-8e0e-85635d2d6e2d
  Args:
    source: Wolfgang_of_Hesse
    target: Frederick_Charles_of_Hesse
    relation: :hasFather
  AddTriple (c6212312-419d-45ee-8a83-2605fb4eacc1)
 Call ID: c6212312-419d-45ee-8a83-2605fb4eacc1
  Args:
    source: Wolfgang_of_Hesse
    target: Margaret_of_Prussia
    relation: :hasMother
  AssignClass (9503df11-240c-4ed6-ad24-6fa2f5318fbd)
 Call ID: 9503df11-240c-4ed6-ad24-6fa2f5318fbd
  Args:
    source: Philipp_of_Hesse
    type: :Man
  AddTriple (cfc6d449-ad92-423b-bc6d-8bb034bd8b73)
 Call ID: cfc6d449-ad92-423b-bc6d-8bb034bd8b73
  Args:
    relation: :isSiblingOf
    target: Philipp_of_Hesse
    source: Wolfgang_of_Hesse
  AssignClass (211f5235-3b38-45b4-a027-64a22cd7d16d)
 Call ID: 211f5235-3b38-45b4-a027-64a22cd7d16d
  Args:
    source: Marie_Alexandra_of_Baden
    type: :Woman
  AddLiteral (5836be94-bc23-4daa-ab00-3b5ace7b9482)
 Call ID: 5836be94-bc23-4daa-ab00-3b5ace7b9482
  Args:
    literal_value: 1902
    source: Marie_Alexandra_of_Baden
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (487feb3a-0912-4061-9fb3-76489ff82f35)
 Call ID: 487feb3a-0912-4061-9fb3-76489ff82f35
  Args:
    literal_value: 1944
    source: Marie_Alexandra_of_Baden
    relation: :hasDeathYear
    literal_type: xsd:integer
  AddLiteral (5b1749b6-66d4-4b10-9088-213d9dadc897)
 Call ID: 5b1749b6-66d4-4b10-9088-213d9dadc897
  Args:
    source: Wolfgang_of_Hesse
    literal_value: 1924
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AddTriple (645acd01-aebb-4d32-ba7a-4a96070d4d06)
 Call ID: 645acd01-aebb-4d32-ba7a-4a96070d4d06
  Args:
    relation: :hasRelation
    target: Marie_Alexandra_of_Baden
    source: Wolfgang_of_Hesse
  AssignClass (def66468-cfbf-4497-9cbc-037dfc8aa768)
 Call ID: def66468-cfbf-4497-9cbc-037dfc8aa768
  Args:
    type: :Man
    source: Maximilian_of_Baden
  AssignClass (03d280fb-56b0-4d8a-a2fe-23df6a497c29)
 Call ID: 03d280fb-56b0-4d8a-a2fe-23df6a497c29
  Args:
    source: Marie_Louise_of_Hanover
    type: :Woman
  AddTriple (a8ff6830-31b6-4e9c-8570-94c8256896c3)
 Call ID: a8ff6830-31b6-4e9c-8570-94c8256896c3
  Args:
    source: Marie_Alexandra_of_Baden
    target: Maximilian_of_Baden
    relation: :hasFather
  AddTriple (4456f593-6179-44e2-8957-b04f8ae377de)
 Call ID: 4456f593-6179-44e2-8957-b04f8ae377de
  Args:
    target: Marie_Louise_of_Hanover
    source: Marie_Alexandra_of_Baden
    relation: :hasMother
  Finish (ccd3e160-e37c-4dad-bee6-eb851ec7225a)
 Call ID: ccd3e160-e37c-4dad-bee6-eb851ec7225a
  Args: