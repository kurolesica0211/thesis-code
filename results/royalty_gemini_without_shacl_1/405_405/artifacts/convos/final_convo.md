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
  AssignClass (6bcf0a28-9059-4301-8d7c-169e1374ba1e)
 Call ID: 6bcf0a28-9059-4301-8d7c-169e1374ba1e
  Args:
    type: :Man
    source: Wolfgang_of_Hesse
  AssignClass (c95bc4c3-d390-4c4e-97b9-4e81163caa04)
 Call ID: c95bc4c3-d390-4c4e-97b9-4e81163caa04
  Args:
    type: :Person
    source: Wolfgang_of_Hesse
  AddLiteral (08a0ca2a-6ddb-46b5-8329-0c949832cade)
 Call ID: 08a0ca2a-6ddb-46b5-8329-0c949832cade
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Wolfgang_of_Hesse
    literal_value: 1896
  AddLiteral (022fcaa2-60b5-4900-812b-56eace5fdcc8)
 Call ID: 022fcaa2-60b5-4900-812b-56eace5fdcc8
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: Wolfgang_of_Hesse
    literal_value: 1989
  AddLiteral (7843a9a3-8ec6-4c05-b754-603c2d6dda89)
 Call ID: 7843a9a3-8ec6-4c05-b754-603c2d6dda89
  Args:
    literal_type: xsd:string
    relation: :alsoKnownAs
    source: Wolfgang_of_Hesse
    literal_value: Wolfgang Moritz Prinz von Hessen
  AssignClass (c0afebb1-3f74-45a1-b972-136315b86e82)
 Call ID: c0afebb1-3f74-45a1-b972-136315b86e82
  Args:
    type: :Man
    source: Frederick_Charles_of_Hesse
  AssignClass (86929e1c-4626-418e-a0af-e6c5199068b4)
 Call ID: 86929e1c-4626-418e-a0af-e6c5199068b4
  Args:
    type: :Person
    source: Frederick_Charles_of_Hesse
  AddLiteral (5b301ab0-eb4c-43cb-b6cb-a5655aa4a3db)
 Call ID: 5b301ab0-eb4c-43cb-b6cb-a5655aa4a3db
  Args:
    literal_value: 1868
    source: Frederick_Charles_of_Hesse
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (65ce565b-195e-402f-8b99-e9346d723973)
 Call ID: 65ce565b-195e-402f-8b99-e9346d723973
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: Frederick_Charles_of_Hesse
    literal_value: 1940
  AssignClass (b0ceeca9-69c2-4f93-9bf9-54afa45a808f)
 Call ID: b0ceeca9-69c2-4f93-9bf9-54afa45a808f
  Args:
    type: :Woman
    source: Margaret_of_Prussia
  AssignClass (596a34e2-acd7-40d5-b76c-57f4bfb80f22)
 Call ID: 596a34e2-acd7-40d5-b76c-57f4bfb80f22
  Args:
    type: :Person
    source: Margaret_of_Prussia
  AddLiteral (0411bd17-b83c-4b69-8d07-2b3759c6e8a4)
 Call ID: 0411bd17-b83c-4b69-8d07-2b3759c6e8a4
  Args:
    literal_value: 1872
    source: Margaret_of_Prussia
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (4da86f1f-45a7-4be7-8677-8b8f80fb52f8)
 Call ID: 4da86f1f-45a7-4be7-8677-8b8f80fb52f8
  Args:
    literal_value: 1954
    source: Margaret_of_Prussia
    relation: :hasDeathYear
    literal_type: xsd:integer
  AddTriple (9d2b7bf8-f031-47a2-a2b0-9811366cc1da)
 Call ID: 9d2b7bf8-f031-47a2-a2b0-9811366cc1da
  Args:
    target: Frederick_Charles_of_Hesse
    relation: :hasFather
    source: Wolfgang_of_Hesse
  AddTriple (95cef581-7439-4ca6-935b-126d07378e59)
 Call ID: 95cef581-7439-4ca6-935b-126d07378e59
  Args:
    source: Wolfgang_of_Hesse
    relation: :hasMother
    target: Margaret_of_Prussia
  AssignClass (adf92d5e-4906-4fd8-b520-ccc717eb2104)
 Call ID: adf92d5e-4906-4fd8-b520-ccc717eb2104
  Args:
    type: :Man
    source: Philipp_of_Hesse
  AssignClass (a8d08411-94e8-4636-96dd-0ed5ae4f7bc6)
 Call ID: a8d08411-94e8-4636-96dd-0ed5ae4f7bc6
  Args:
    type: :Person
    source: Philipp_of_Hesse
  AddTriple (df412f3b-0668-46a9-90c2-2b6a34cb5372)
 Call ID: df412f3b-0668-46a9-90c2-2b6a34cb5372
  Args:
    target: Philipp_of_Hesse
    relation: :isSiblingOf
    source: Wolfgang_of_Hesse
  AssignClass (bba2397a-5997-4de1-b60c-ed46b2c47493)
 Call ID: bba2397a-5997-4de1-b60c-ed46b2c47493
  Args:
    type: :Woman
    source: Marie_Alexandra_of_Baden
  AssignClass (43ca077a-70d1-4269-90c3-bfc262e0448c)
 Call ID: 43ca077a-70d1-4269-90c3-bfc262e0448c
  Args:
    type: :Person
    source: Marie_Alexandra_of_Baden
  AddLiteral (ff34bccb-70b1-403a-9dc5-00c5c3ce65d4)
 Call ID: ff34bccb-70b1-403a-9dc5-00c5c3ce65d4
  Args:
    source: Marie_Alexandra_of_Baden
    literal_value: 1902
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (df1b1829-04c6-4063-802d-018a1f104274)
 Call ID: df1b1829-04c6-4063-802d-018a1f104274
  Args:
    literal_value: 1944
    source: Marie_Alexandra_of_Baden
    relation: :hasDeathYear
    literal_type: xsd:integer
  AddLiteral (ea50f02f-82ec-4011-8474-84da34cb7da2)
 Call ID: ea50f02f-82ec-4011-8474-84da34cb7da2
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    source: Wolfgang_of_Hesse
    literal_value: 1924
  AddTriple (e4074798-c1bd-4006-bfdc-175956010213)
 Call ID: e4074798-c1bd-4006-bfdc-175956010213
  Args:
    source: Wolfgang_of_Hesse
    target: Marie_Alexandra_of_Baden
    relation: :hasRelation
  AssignClass (b9c4113f-8a00-472d-9d02-1aecf57e82bd)
 Call ID: b9c4113f-8a00-472d-9d02-1aecf57e82bd
  Args:
    type: :Man
    source: Maximilian_of_Baden
  AssignClass (7c45ba2f-1385-409a-9801-4a3a132aecc6)
 Call ID: 7c45ba2f-1385-409a-9801-4a3a132aecc6
  Args:
    type: :Person
    source: Maximilian_of_Baden
  AssignClass (b32ce6e9-457b-46f8-b71d-3df0164f8621)
 Call ID: b32ce6e9-457b-46f8-b71d-3df0164f8621
  Args:
    type: :Woman
    source: Marie_Louise_of_Hanover
  AssignClass (bdf9b1e1-ad26-4745-befa-dbe78853a53e)
 Call ID: bdf9b1e1-ad26-4745-befa-dbe78853a53e
  Args:
    type: :Person
    source: Marie_Louise_of_Hanover
  AddTriple (5e82af2d-5928-4de9-b943-2682bfff92b2)
 Call ID: 5e82af2d-5928-4de9-b943-2682bfff92b2
  Args:
    relation: :hasFather
    target: Maximilian_of_Baden
    source: Marie_Alexandra_of_Baden
  AddTriple (7ea2a023-7566-4b6f-a4c5-3fbb231e4439)
 Call ID: 7ea2a023-7566-4b6f-a4c5-3fbb231e4439
  Args:
    target: Marie_Louise_of_Hanover
    relation: :hasMother
    source: Marie_Alexandra_of_Baden
  AssignClass (6c16bbb1-d743-43bc-a217-75f6fdab3eaf)
 Call ID: 6c16bbb1-d743-43bc-a217-75f6fdab3eaf
  Args:
    type: :Man
    source: Willhelm_II
  AssignClass (c346425e-d807-4443-b26b-016d9e81ba60)
 Call ID: c346425e-d807-4443-b26b-016d9e81ba60
  Args:
    type: :Person
    source: Willhelm_II
  AssignClass (be24c700-3ff6-4472-bd6c-8ea87569b94c)
 Call ID: be24c700-3ff6-4472-bd6c-8ea87569b94c
  Args:
    type: :Man
    source: Nicholas_II
  AssignClass (9a029c58-c8f0-41bb-9a36-b77983b46388)
 Call ID: 9a029c58-c8f0-41bb-9a36-b77983b46388
  Args:
    type: :Person
    source: Nicholas_II
  Finish (aec5e190-6a0e-4186-9ce8-6a80c5bdbffc)
 Call ID: aec5e190-6a0e-4186-9ce8-6a80c5bdbffc
  Args: