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
Granville James Leveson-Gower, 5th Earl Granville MC (6 December 1918 – 31 October 1996) was a British soldier, banker, peer, and landowner, a member of the House of Lords from 1953 until his death.
Early life

The son of Vice-Admiral William Leveson-Gower, 4th Earl Granville, and his wife Lady Rose Bowes-Lyon, a daughter of Claude Bowes-Lyon, 14th
Earl of Strathmore and Kinghorne, he was educated at Eton College.
Known formally as Lord Leveson until 1953, he was commissioned into the Coldstream Guards and saw active service during the Second World War, in which he was twice wounded and mentioned in despatches.
Later career

After the war, Lord Leveson joined Coutts & Co., a private bank.
On 25 June 1953, he succeeded his father as Earl Granville (created 1833), Viscount Granville (1814), and Baron Leveson of Stone (1814), giving him a seat in the House of Lords.
In 1958, Granville married Doon Aileen Plunket, daughter of Brindsley Sheridan Bushe Plunket and granddaughter of William Plunket, 5th Baron Plunket.
Her mother was Aileen Sibell Mary Guinness, a granddaughter of Edward Guinness, 1st Earl of Iveagh.
In 1960, shortly after the birth of his first child, Granville bought the island of North Uist in the Outer Hebrides from the Duke of Hamilton, becoming its laird.
In 1974 Granville was appointed as a Deputy Lieutenant of Inverness-shire and was Vice-Lord-Lieutenant of the Western Isles between January 1976 and 1983, then Lord-Lieutenant from 1983 to December 1993, when he was succeeded by Viscount Dunrossil.



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
  AssignClass (711dcbfc-9bc0-4a33-9566-95f9e562a963)
 Call ID: 711dcbfc-9bc0-4a33-9566-95f9e562a963
  Args:
    source: Granville_James_Leveson-Gower
    type: :Man
  AssignClass (0176ab97-fee6-4a49-9235-a5575f2e7d3c)
 Call ID: 0176ab97-fee6-4a49-9235-a5575f2e7d3c
  Args:
    type: :Person
    source: Granville_James_Leveson-Gower
  AddLiteral (0bd18408-0661-4916-9239-582ff2ea9a79)
 Call ID: 0bd18408-0661-4916-9239-582ff2ea9a79
  Args:
    relation: :hasBirthYear
    source: Granville_James_Leveson-Gower
    literal_value: 1918
    literal_type: xsd:integer
  AddLiteral (278291e1-e94b-4231-b059-c5fc8029cd44)
 Call ID: 278291e1-e94b-4231-b059-c5fc8029cd44
  Args:
    literal_value: 1996
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: Granville_James_Leveson-Gower
  AddLiteral (0f666e97-ba44-469a-ac27-ad03457effeb)
 Call ID: 0f666e97-ba44-469a-ac27-ad03457effeb
  Args:
    relation: :formerlyKnownAs
    source: Granville_James_Leveson-Gower
    literal_value: Lord Leveson
    literal_type: xsd:string
  AssignClass (49378d83-b0fb-4a43-b345-f585fedf77d8)
 Call ID: 49378d83-b0fb-4a43-b345-f585fedf77d8
  Args:
    source: William_Leveson-Gower
    type: :Man
  AssignClass (4e640c75-8bce-42a1-879c-4ce530c9b7e1)
 Call ID: 4e640c75-8bce-42a1-879c-4ce530c9b7e1
  Args:
    type: :Person
    source: William_Leveson-Gower
  AddTriple (a4430701-c458-40d3-b717-45b3c106e4ae)
 Call ID: a4430701-c458-40d3-b717-45b3c106e4ae
  Args:
    target: William_Leveson-Gower
    source: Granville_James_Leveson-Gower
    relation: :hasFather
  AssignClass (ce2ee714-4281-4b60-ac65-e0ccf74ca09e)
 Call ID: ce2ee714-4281-4b60-ac65-e0ccf74ca09e
  Args:
    source: Lady_Rose_Bowes-Lyon
    type: :Woman
  AssignClass (f935cc28-95ad-48a5-84f3-cfd54a808bec)
 Call ID: f935cc28-95ad-48a5-84f3-cfd54a808bec
  Args:
    type: :Person
    source: Lady_Rose_Bowes-Lyon
  AddTriple (e4f16c47-30a3-4979-8659-ec4d004dc5fa)
 Call ID: e4f16c47-30a3-4979-8659-ec4d004dc5fa
  Args:
    target: Lady_Rose_Bowes-Lyon
    source: Granville_James_Leveson-Gower
    relation: :hasMother
  AssignClass (70045157-480e-4a74-8908-8653ae704888)
 Call ID: 70045157-480e-4a74-8908-8653ae704888
  Args:
    source: Claude_Bowes-Lyon
    type: :Man
  AssignClass (7280ccc3-401a-4783-874a-6ca561a52b3c)
 Call ID: 7280ccc3-401a-4783-874a-6ca561a52b3c
  Args:
    source: Claude_Bowes-Lyon
    type: :Person
  AddTriple (391f657b-04a6-4180-9be7-e13ccd777cbc)
 Call ID: 391f657b-04a6-4180-9be7-e13ccd777cbc
  Args:
    source: Lady_Rose_Bowes-Lyon
    relation: :hasFather
    target: Claude_Bowes-Lyon
  AssignClass (d33f0245-f7c4-445f-9c5c-234b1b0c05a2)
 Call ID: d33f0245-f7c4-445f-9c5c-234b1b0c05a2
  Args:
    source: Doon_Aileen_Plunket
    type: :Woman
  AssignClass (792ffe22-5478-471f-b87b-4f77807f5286)
 Call ID: 792ffe22-5478-471f-b87b-4f77807f5286
  Args:
    source: Doon_Aileen_Plunket
    type: :Person
  AddTriple (221a5d88-e09f-45aa-a6ec-b532506520d2)
 Call ID: 221a5d88-e09f-45aa-a6ec-b532506520d2
  Args:
    target: Doon_Aileen_Plunket
    source: Granville_James_Leveson-Gower
    relation: :hasRelation
  AddLiteral (bb76f0a1-8fd4-4b20-95c9-760227f916ca)
 Call ID: bb76f0a1-8fd4-4b20-95c9-760227f916ca
  Args:
    relation: :hasMarriageYear
    source: Granville_James_Leveson-Gower
    literal_value: 1958
    literal_type: xsd:integer
  AssignClass (3155ee85-1451-4891-888b-7f471995fade)
 Call ID: 3155ee85-1451-4891-888b-7f471995fade
  Args:
    source: Brindsley_Sheridan_Bushe_Plunket
    type: :Man
  AssignClass (52fa6f7d-6fb0-4106-ae49-bf2935dc18b4)
 Call ID: 52fa6f7d-6fb0-4106-ae49-bf2935dc18b4
  Args:
    source: Brindsley_Sheridan_Bushe_Plunket
    type: :Person
  AddTriple (d1562fcf-a721-42f6-a26d-fe1adfe4b64a)
 Call ID: d1562fcf-a721-42f6-a26d-fe1adfe4b64a
  Args:
    target: Brindsley_Sheridan_Bushe_Plunket
    relation: :hasFather
    source: Doon_Aileen_Plunket
  AssignClass (89f262a1-437a-4133-88b7-682ea9fb476b)
 Call ID: 89f262a1-437a-4133-88b7-682ea9fb476b
  Args:
    type: :Man
    source: William_Plunket
  AssignClass (0bfd13b5-bdf7-4fd4-943e-b202fa036e7f)
 Call ID: 0bfd13b5-bdf7-4fd4-943e-b202fa036e7f
  Args:
    source: William_Plunket
    type: :Person
  AssignClass (1294a891-aa39-4e8f-b804-76371dd2bd16)
 Call ID: 1294a891-aa39-4e8f-b804-76371dd2bd16
  Args:
    type: :Woman
    source: Aileen_Sibell_Mary_Guinness
  AssignClass (22825a37-ea59-4faa-bfe3-4c6db3044b26)
 Call ID: 22825a37-ea59-4faa-bfe3-4c6db3044b26
  Args:
    source: Aileen_Sibell_Mary_Guinness
    type: :Person
  AddTriple (ad9a80d4-e546-42d2-818d-8d771e74c054)
 Call ID: ad9a80d4-e546-42d2-818d-8d771e74c054
  Args:
    target: Aileen_Sibell_Mary_Guinness
    source: Doon_Aileen_Plunket
    relation: :hasMother
  AssignClass (45c827d0-7930-4080-a955-5a6cb062eb50)
 Call ID: 45c827d0-7930-4080-a955-5a6cb062eb50
  Args:
    source: Edward_Guinness
    type: :Man
  AssignClass (bba2e122-93c9-4c53-8cf7-dc3a027b8d4c)
 Call ID: bba2e122-93c9-4c53-8cf7-dc3a027b8d4c
  Args:
    type: :Person
    source: Edward_Guinness
  Finish (9a9018ae-9320-4f8d-b6b4-ab7249a33e73)
 Call ID: 9a9018ae-9320-4f8d-b6b4-ab7249a33e73
  Args: