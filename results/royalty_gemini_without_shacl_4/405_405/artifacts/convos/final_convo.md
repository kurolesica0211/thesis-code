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
  AssignClass (51004c50-bc21-4127-994f-320e9caf6de2)
 Call ID: 51004c50-bc21-4127-994f-320e9caf6de2
  Args:
    source: :Wolfgang_of_Hesse
    type: :Man
  AssignClass (d228fee6-2d04-4ecc-930c-1e11ded82d69)
 Call ID: d228fee6-2d04-4ecc-930c-1e11ded82d69
  Args:
    source: :Wolfgang_of_Hesse
    type: :Person
  AddLiteral (96fb5022-37fe-443e-a6c3-966e546f3e1a)
 Call ID: 96fb5022-37fe-443e-a6c3-966e546f3e1a
  Args:
    source: :Wolfgang_of_Hesse
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1896
  AddLiteral (32c3fe06-d2f1-4eeb-8efa-e03e1a4487f2)
 Call ID: 32c3fe06-d2f1-4eeb-8efa-e03e1a4487f2
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 1989
    source: :Wolfgang_of_Hesse
  AssignClass (033b2657-77d5-49a7-97c4-271f1a121cb8)
 Call ID: 033b2657-77d5-49a7-97c4-271f1a121cb8
  Args:
    source: :Frederick_Charles_of_Hesse
    type: :Man
  AssignClass (ffe36ece-2ff5-4739-92cf-6d74a1ad50ac)
 Call ID: ffe36ece-2ff5-4739-92cf-6d74a1ad50ac
  Args:
    source: :Frederick_Charles_of_Hesse
    type: :Person
  AddLiteral (52615b9a-06e5-4aee-9a6c-568ec3c3381e)
 Call ID: 52615b9a-06e5-4aee-9a6c-568ec3c3381e
  Args:
    source: :Frederick_Charles_of_Hesse
    literal_value: 1868
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (48cfccef-2ba7-416c-ac0c-8f32a11c8da1)
 Call ID: 48cfccef-2ba7-416c-ac0c-8f32a11c8da1
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1940
    source: :Frederick_Charles_of_Hesse
  AssignClass (48302283-138e-4da2-a2c8-4a2d6e65a6af)
 Call ID: 48302283-138e-4da2-a2c8-4a2d6e65a6af
  Args:
    type: :Woman
    source: :Margaret_of_Prussia
  AssignClass (345b00b5-b1a9-4a0b-93b1-6300736c530e)
 Call ID: 345b00b5-b1a9-4a0b-93b1-6300736c530e
  Args:
    source: :Margaret_of_Prussia
    type: :Person
  AddLiteral (0294d5e5-2ee6-49d3-9ea5-82794f4b4a46)
 Call ID: 0294d5e5-2ee6-49d3-9ea5-82794f4b4a46
  Args:
    source: :Margaret_of_Prussia
    literal_value: 1872
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (18bfe576-3dd9-4c88-8b1e-793640bbf4e8)
 Call ID: 18bfe576-3dd9-4c88-8b1e-793640bbf4e8
  Args:
    literal_value: 1954
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: :Margaret_of_Prussia
  AddTriple (24e6bf81-d06f-4b80-9070-03c8ebf7ea40)
 Call ID: 24e6bf81-d06f-4b80-9070-03c8ebf7ea40
  Args:
    target: :Frederick_Charles_of_Hesse
    relation: :hasFather
    source: :Wolfgang_of_Hesse
  AddTriple (6758b754-9c25-43da-9044-cb3d5fd72df0)
 Call ID: 6758b754-9c25-43da-9044-cb3d5fd72df0
  Args:
    source: :Wolfgang_of_Hesse
    relation: :hasMother
    target: :Margaret_of_Prussia
  AssignClass (0e5cfb17-4ca0-4123-80aa-b8eca5a4f485)
 Call ID: 0e5cfb17-4ca0-4123-80aa-b8eca5a4f485
  Args:
    type: :Man
    source: :Philipp_of_Hesse
  AssignClass (c0963752-d39f-44dd-9cf8-924267dc2f06)
 Call ID: c0963752-d39f-44dd-9cf8-924267dc2f06
  Args:
    type: :Person
    source: :Philipp_of_Hesse
  AddTriple (05e12e57-da44-46fb-99fb-8ac7c8fcd48f)
 Call ID: 05e12e57-da44-46fb-99fb-8ac7c8fcd48f
  Args:
    target: :Philipp_of_Hesse
    source: :Wolfgang_of_Hesse
    relation: :isSiblingOf
  AssignClass (8cbd96b9-f659-43c8-a48a-042c18189df7)
 Call ID: 8cbd96b9-f659-43c8-a48a-042c18189df7
  Args:
    type: :Woman
    source: :Marie_Alexandra_of_Baden
  AssignClass (10315af9-69bb-45b4-aa92-d0c6c83b7666)
 Call ID: 10315af9-69bb-45b4-aa92-d0c6c83b7666
  Args:
    type: :Person
    source: :Marie_Alexandra_of_Baden
  AddLiteral (6c8626db-3b1a-4eb9-a8a3-3ede6d29a820)
 Call ID: 6c8626db-3b1a-4eb9-a8a3-3ede6d29a820
  Args:
    literal_value: 1924
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: :Wolfgang_of_Hesse
  AddTriple (6e73266a-2951-4d40-ae74-523795c315d8)
 Call ID: 6e73266a-2951-4d40-ae74-523795c315d8
  Args:
    relation: :hasRelation
    source: :Wolfgang_of_Hesse
    target: :Marie_Alexandra_of_Baden
  AddLiteral (62e28d2f-2485-4365-bfdc-24a4cfafc482)
 Call ID: 62e28d2f-2485-4365-bfdc-24a4cfafc482
  Args:
    source: :Marie_Alexandra_of_Baden
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1902
  AddLiteral (34466ca7-1765-416a-9a84-24059e022a8c)
 Call ID: 34466ca7-1765-416a-9a84-24059e022a8c
  Args:
    source: :Marie_Alexandra_of_Baden
    literal_value: 1944
    literal_type: xsd:integer
    relation: :hasDeathYear
  AssignClass (c5c2cb61-6370-403b-a6fb-b205f8a725a0)
 Call ID: c5c2cb61-6370-403b-a6fb-b205f8a725a0
  Args:
    source: :Maximilian_of_Baden
    type: :Man
  AssignClass (7bc7dbb9-ba4d-4e34-bc5a-ae52918e6179)
 Call ID: 7bc7dbb9-ba4d-4e34-bc5a-ae52918e6179
  Args:
    source: :Maximilian_of_Baden
    type: :Person
  AssignClass (c3e21607-5faf-44dd-ba6e-b797588d3ea6)
 Call ID: c3e21607-5faf-44dd-ba6e-b797588d3ea6
  Args:
    source: :Marie_Louise_of_Hanover
    type: :Woman
  AssignClass (d1587240-a1ba-4fcf-9f97-618328368a5e)
 Call ID: d1587240-a1ba-4fcf-9f97-618328368a5e
  Args:
    type: :Person
    source: :Marie_Louise_of_Hanover
  AddTriple (7899bcf9-4aed-45dc-a943-b531998eee39)
 Call ID: 7899bcf9-4aed-45dc-a943-b531998eee39
  Args:
    source: :Marie_Alexandra_of_Baden
    relation: :hasFather
    target: :Maximilian_of_Baden
  AddTriple (36ae1984-9e4a-4c48-9ae2-433ffd977d1a)
 Call ID: 36ae1984-9e4a-4c48-9ae2-433ffd977d1a
  Args:
    target: :Marie_Louise_of_Hanover
    source: :Marie_Alexandra_of_Baden
    relation: :hasMother
  AssignClass (c6cd4967-ea05-42c6-b691-7ef98391a0b1)
 Call ID: c6cd4967-ea05-42c6-b691-7ef98391a0b1
  Args:
    source: :Wilhelm_II
    type: :Man
  AssignClass (22db5470-4234-4c51-b550-19cb395d8cbb)
 Call ID: 22db5470-4234-4c51-b550-19cb395d8cbb
  Args:
    source: :Wilhelm_II
    type: :Person
  AddTriple (0fe6ba92-87f2-4719-b8a5-cbb05be822f8)
 Call ID: 0fe6ba92-87f2-4719-b8a5-cbb05be822f8
  Args:
    relation: :isUncleOf
    source: :Wilhelm_II
    target: :Wolfgang_of_Hesse
  AssignClass (e8b54468-0c4b-4eb6-b15e-51a84bc2f6bf)
 Call ID: e8b54468-0c4b-4eb6-b15e-51a84bc2f6bf
  Args:
    type: :Man
    source: :Nicholas_II
  AssignClass (bdd66ceb-44a4-43e7-889c-f5305bd364b1)
 Call ID: bdd66ceb-44a4-43e7-889c-f5305bd364b1
  Args:
    type: :Person
    source: :Nicholas_II
  Finish (5ba05110-9779-41b1-93ac-52f29caa908e)
 Call ID: 5ba05110-9779-41b1-93ac-52f29caa908e
  Args: