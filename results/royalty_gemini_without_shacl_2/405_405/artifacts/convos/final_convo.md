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
  AssignClass (c373d05e-e296-4532-a12d-8cf6457e0854)
 Call ID: c373d05e-e296-4532-a12d-8cf6457e0854
  Args:
    source: Wolfgang_of_Hesse
    type: :Man
  AssignClass (39a76d6e-9fd7-4f1c-ab34-7cbcada6700a)
 Call ID: 39a76d6e-9fd7-4f1c-ab34-7cbcada6700a
  Args:
    source: Wolfgang_of_Hesse
    type: :Person
  AddLiteral (24b4d9c3-fdcc-4383-8771-78e85b322dea)
 Call ID: 24b4d9c3-fdcc-4383-8771-78e85b322dea
  Args:
    literal_type: xsd:integer
    literal_value: 1896
    source: Wolfgang_of_Hesse
    relation: :hasBirthYear
  AddLiteral (f71ed572-e2b5-4f39-a06c-1e7f13631969)
 Call ID: f71ed572-e2b5-4f39-a06c-1e7f13631969
  Args:
    source: Wolfgang_of_Hesse
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 1989
  AddLiteral (4832e9fc-aac4-41ff-a7a5-d056e509cf53)
 Call ID: 4832e9fc-aac4-41ff-a7a5-d056e509cf53
  Args:
    source: Wolfgang_of_Hesse
    relation: :alsoKnownAs
    literal_type: xsd:string
    literal_value: Wolfgang Moritz Prinz von Hessen
  AssignClass (eb82caa9-c39d-492d-8369-a9fc8ec94b0d)
 Call ID: eb82caa9-c39d-492d-8369-a9fc8ec94b0d
  Args:
    source: Frederick_Charles_of_Hesse
    type: :Man
  AssignClass (d4d6822d-5608-4e08-8340-00709adc3a88)
 Call ID: d4d6822d-5608-4e08-8340-00709adc3a88
  Args:
    type: :Ancestor
    source: Frederick_Charles_of_Hesse
  AssignClass (733dad73-dac0-4b91-89f0-d102773a53d8)
 Call ID: 733dad73-dac0-4b91-89f0-d102773a53d8
  Args:
    type: :Person
    source: Frederick_Charles_of_Hesse
  AddLiteral (728aa503-0f97-4de1-9244-72564e37becf)
 Call ID: 728aa503-0f97-4de1-9244-72564e37becf
  Args:
    relation: :hasBirthYear
    source: Frederick_Charles_of_Hesse
    literal_value: 1868
    literal_type: xsd:integer
  AddLiteral (e2ebf007-ceaa-41fb-9bc3-b1fef2ea063b)
 Call ID: e2ebf007-ceaa-41fb-9bc3-b1fef2ea063b
  Args:
    literal_value: 1940
    literal_type: xsd:integer
    source: Frederick_Charles_of_Hesse
    relation: :hasDeathYear
  AssignClass (4aa541ba-a110-4616-87d1-49b6e013d638)
 Call ID: 4aa541ba-a110-4616-87d1-49b6e013d638
  Args:
    source: Margaret_of_Prussia
    type: :Woman
  AssignClass (6039f7b8-df84-4937-9fdc-13ba6bab635f)
 Call ID: 6039f7b8-df84-4937-9fdc-13ba6bab635f
  Args:
    type: :Ancestor
    source: Margaret_of_Prussia
  AssignClass (75b9ae9b-f0fe-4ac8-81b4-670e7b763aff)
 Call ID: 75b9ae9b-f0fe-4ac8-81b4-670e7b763aff
  Args:
    source: Margaret_of_Prussia
    type: :Person
  AddLiteral (0a5eb13f-5ce1-411e-ad19-ea506193c4d9)
 Call ID: 0a5eb13f-5ce1-411e-ad19-ea506193c4d9
  Args:
    relation: :hasBirthYear
    source: Margaret_of_Prussia
    literal_type: xsd:integer
    literal_value: 1872
  AddLiteral (fafed16a-ce0d-44ec-a841-9b9afc907e80)
 Call ID: fafed16a-ce0d-44ec-a841-9b9afc907e80
  Args:
    literal_value: 1954
    literal_type: xsd:integer
    source: Margaret_of_Prussia
    relation: :hasDeathYear
  AddTriple (c956ed2b-7d19-4e59-b61e-51087001507b)
 Call ID: c956ed2b-7d19-4e59-b61e-51087001507b
  Args:
    target: Frederick_Charles_of_Hesse
    source: Wolfgang_of_Hesse
    relation: :hasFather
  AddTriple (c6ecf2aa-07a8-4f6c-95af-e6416709c70b)
 Call ID: c6ecf2aa-07a8-4f6c-95af-e6416709c70b
  Args:
    relation: :hasMother
    source: Wolfgang_of_Hesse
    target: Margaret_of_Prussia
  AssignClass (7c2309ce-ef38-4dcd-b116-29c6548b2cfb)
 Call ID: 7c2309ce-ef38-4dcd-b116-29c6548b2cfb
  Args:
    source: Philipp_of_Hesse
    type: :Man
  AssignClass (50dbaa8e-845e-49d7-8b29-dcf1381ab829)
 Call ID: 50dbaa8e-845e-49d7-8b29-dcf1381ab829
  Args:
    source: Philipp_of_Hesse
    type: :Person
  AddTriple (a9e8b413-6b5f-428a-9f38-7bbcf592d747)
 Call ID: a9e8b413-6b5f-428a-9f38-7bbcf592d747
  Args:
    relation: :isSiblingOf
    source: Wolfgang_of_Hesse
    target: Philipp_of_Hesse
  AssignClass (c864a79b-3653-4e4f-87f2-c4b7b87fd567)
 Call ID: c864a79b-3653-4e4f-87f2-c4b7b87fd567
  Args:
    source: Marie_Alexandra_of_Baden
    type: :Woman
  AssignClass (2da27be3-e58c-4ac4-9760-022eba244685)
 Call ID: 2da27be3-e58c-4ac4-9760-022eba244685
  Args:
    type: :Person
    source: Marie_Alexandra_of_Baden
  AddLiteral (805dd69e-1000-4047-bfe4-62d913434666)
 Call ID: 805dd69e-1000-4047-bfe4-62d913434666
  Args:
    literal_value: 1902
    literal_type: xsd:integer
    source: Marie_Alexandra_of_Baden
    relation: :hasBirthYear
  AddLiteral (54108b0a-ff94-4e8b-a969-d3f03989179f)
 Call ID: 54108b0a-ff94-4e8b-a969-d3f03989179f
  Args:
    source: Marie_Alexandra_of_Baden
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 1944
  AddTriple (c9bee509-9bd2-4a55-847a-72da80e5d48d)
 Call ID: c9bee509-9bd2-4a55-847a-72da80e5d48d
  Args:
    source: Wolfgang_of_Hesse
    relation: :hasRelation
    target: Marie_Alexandra_of_Baden
  AddLiteral (0767962c-8c43-40d7-ad62-e887b772327f)
 Call ID: 0767962c-8c43-40d7-ad62-e887b772327f
  Args:
    relation: :hasMarriageYear
    source: Wolfgang_of_Hesse
    literal_type: xsd:integer
    literal_value: 1924
  AssignClass (6e99a952-5c98-4ee3-bf21-ae9f2872e0c0)
 Call ID: 6e99a952-5c98-4ee3-bf21-ae9f2872e0c0
  Args:
    source: Maximilian_of_Baden
    type: :Man
  AssignClass (33b50632-3d4c-4c4f-9f24-0cb4f4c64803)
 Call ID: 33b50632-3d4c-4c4f-9f24-0cb4f4c64803
  Args:
    type: :Ancestor
    source: Maximilian_of_Baden
  AssignClass (880b223a-3425-4e15-9df9-a98c4b17d9ac)
 Call ID: 880b223a-3425-4e15-9df9-a98c4b17d9ac
  Args:
    type: :Person
    source: Maximilian_of_Baden
  AssignClass (a31dcee4-cc40-4f42-920d-3789c89c59ec)
 Call ID: a31dcee4-cc40-4f42-920d-3789c89c59ec
  Args:
    type: :Woman
    source: Marie_Louise_of_Hanover
  AssignClass (8f6b2bd3-bd56-4b17-861f-95a5c95f00de)
 Call ID: 8f6b2bd3-bd56-4b17-861f-95a5c95f00de
  Args:
    source: Marie_Louise_of_Hanover
    type: :Ancestor
  AssignClass (7cca83ea-b164-4daf-91ae-91e08117e9f8)
 Call ID: 7cca83ea-b164-4daf-91ae-91e08117e9f8
  Args:
    type: :Person
    source: Marie_Louise_of_Hanover
  AddTriple (e2dd7eed-3982-4e42-9e06-accf85de0b11)
 Call ID: e2dd7eed-3982-4e42-9e06-accf85de0b11
  Args:
    relation: :hasFather
    source: Marie_Alexandra_of_Baden
    target: Maximilian_of_Baden
  AddTriple (db6f7e79-fdee-4159-b473-d3a33fbe887e)
 Call ID: db6f7e79-fdee-4159-b473-d3a33fbe887e
  Args:
    relation: :hasMother
    source: Marie_Alexandra_of_Baden
    target: Marie_Louise_of_Hanover
  Finish (48bbe854-96f2-4d39-9465-7b2b4a813d26)
 Call ID: 48bbe854-96f2-4d39-9465-7b2b4a813d26
  Args: