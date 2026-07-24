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
  AssignClass (c426af4b-4a2a-4139-b1d2-3f1d254b7ce1)
 Call ID: c426af4b-4a2a-4139-b1d2-3f1d254b7ce1
  Args:
    type: :Man
    source: GranvilleJamesLevesonGower
  AssignClass (11dc19fa-6557-4679-ad42-bddc9e800588)
 Call ID: 11dc19fa-6557-4679-ad42-bddc9e800588
  Args:
    source: GranvilleJamesLevesonGower
    type: :Person
  AddLiteral (b16a4677-29c1-441f-a9ca-c62c6e3f8241)
 Call ID: b16a4677-29c1-441f-a9ca-c62c6e3f8241
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: GranvilleJamesLevesonGower
    literal_value: 1918
  AddLiteral (ef69c2a3-bad4-4fa4-a69e-35e036a63651)
 Call ID: ef69c2a3-bad4-4fa4-a69e-35e036a63651
  Args:
    literal_value: 1996
    source: GranvilleJamesLevesonGower
    literal_type: xsd:integer
    relation: :hasDeathYear
  AddLiteral (09b07944-4d27-4ae4-bbf6-d18bb1605e5f)
 Call ID: 09b07944-4d27-4ae4-bbf6-d18bb1605e5f
  Args:
    relation: :formerlyKnownAs
    literal_type: xsd:string
    source: GranvilleJamesLevesonGower
    literal_value: Lord Leveson
  AssignClass (0f2b4eae-0507-4529-93b1-6a81494a4140)
 Call ID: 0f2b4eae-0507-4529-93b1-6a81494a4140
  Args:
    source: WilliamLevesonGower
    type: :Man
  AssignClass (cfdd22b2-fada-4e23-b4dc-8743679143b5)
 Call ID: cfdd22b2-fada-4e23-b4dc-8743679143b5
  Args:
    type: :Person
    source: WilliamLevesonGower
  AddTriple (084f1b0f-0073-4fd6-b963-7b4734eaf325)
 Call ID: 084f1b0f-0073-4fd6-b963-7b4734eaf325
  Args:
    relation: :hasFather
    source: GranvilleJamesLevesonGower
    target: WilliamLevesonGower
  AssignClass (a05b4697-6649-489e-8fe4-3dd2b4ed3cf1)
 Call ID: a05b4697-6649-489e-8fe4-3dd2b4ed3cf1
  Args:
    source: LadyRoseBowesLyon
    type: :Woman
  AssignClass (e1b1eeeb-719b-4d61-9bf0-98a3e33e461b)
 Call ID: e1b1eeeb-719b-4d61-9bf0-98a3e33e461b
  Args:
    type: :Person
    source: LadyRoseBowesLyon
  AddTriple (41710e42-3f96-42b5-8469-cbac385f99bc)
 Call ID: 41710e42-3f96-42b5-8469-cbac385f99bc
  Args:
    source: GranvilleJamesLevesonGower
    target: LadyRoseBowesLyon
    relation: :hasMother
  AssignClass (9ca75a32-0769-41ce-9249-d5142980df46)
 Call ID: 9ca75a32-0769-41ce-9249-d5142980df46
  Args:
    source: ClaudeBowesLyon
    type: :Man
  AssignClass (c34225e0-cdd1-4b86-a016-169e7e1b4a59)
 Call ID: c34225e0-cdd1-4b86-a016-169e7e1b4a59
  Args:
    type: :Person
    source: ClaudeBowesLyon
  AddTriple (a4bfd2b6-e2cf-4bb2-b3e1-ee8ab702c155)
 Call ID: a4bfd2b6-e2cf-4bb2-b3e1-ee8ab702c155
  Args:
    relation: :hasFather
    target: ClaudeBowesLyon
    source: LadyRoseBowesLyon
  AssignClass (763f79e3-25ae-47ce-806c-d7af0d50b908)
 Call ID: 763f79e3-25ae-47ce-806c-d7af0d50b908
  Args:
    source: DoonAileenPlunket
    type: :Woman
  AssignClass (c9421abb-f909-4363-a90c-a859469eaaef)
 Call ID: c9421abb-f909-4363-a90c-a859469eaaef
  Args:
    source: DoonAileenPlunket
    type: :Person
  AddLiteral (f4e48e61-f23b-4983-939d-30c966474cbf)
 Call ID: f4e48e61-f23b-4983-939d-30c966474cbf
  Args:
    source: GranvilleJamesLevesonGower
    literal_value: 1958
    relation: :hasMarriageYear
    literal_type: xsd:integer
  AddTriple (01849b3c-6117-4de2-927e-55f9d462dfeb)
 Call ID: 01849b3c-6117-4de2-927e-55f9d462dfeb
  Args:
    source: GranvilleJamesLevesonGower
    target: DoonAileenPlunket
    relation: :hasRelation
  AssignClass (b3bd964c-2608-4c97-8f55-b7cc9ab730c2)
 Call ID: b3bd964c-2608-4c97-8f55-b7cc9ab730c2
  Args:
    source: BrindsleySheridanBushePlunket
    type: :Man
  AssignClass (2a60ac63-ba91-47c8-a7d0-6b3b0913cb97)
 Call ID: 2a60ac63-ba91-47c8-a7d0-6b3b0913cb97
  Args:
    type: :Person
    source: BrindsleySheridanBushePlunket
  AddTriple (af1addfb-3c45-4e63-9334-3eabb1b50de2)
 Call ID: af1addfb-3c45-4e63-9334-3eabb1b50de2
  Args:
    relation: :hasFather
    source: DoonAileenPlunket
    target: BrindsleySheridanBushePlunket
  AssignClass (d20fd058-1626-4e4e-9cac-53843a21ec95)
 Call ID: d20fd058-1626-4e4e-9cac-53843a21ec95
  Args:
    type: :Man
    source: WilliamPlunket
  AssignClass (bd091b13-be13-4c1d-9837-6f88a1aa4e73)
 Call ID: bd091b13-be13-4c1d-9837-6f88a1aa4e73
  Args:
    type: :Person
    source: WilliamPlunket
  AddTriple (d77c0bbf-e14a-48a7-bb1d-7897998ebc98)
 Call ID: d77c0bbf-e14a-48a7-bb1d-7897998ebc98
  Args:
    relation: :hasFather
    source: BrindsleySheridanBushePlunket
    target: WilliamPlunket
  AssignClass (44e8e863-f172-412e-8cf5-4583db6e8fc2)
 Call ID: 44e8e863-f172-412e-8cf5-4583db6e8fc2
  Args:
    source: AileenSibellMaryGuinness
    type: :Woman
  AssignClass (a6363b8b-cba4-407e-8c56-f0596db2f9da)
 Call ID: a6363b8b-cba4-407e-8c56-f0596db2f9da
  Args:
    type: :Person
    source: AileenSibellMaryGuinness
  AddTriple (e48e749a-7d38-4d82-978a-1376abe5f47e)
 Call ID: e48e749a-7d38-4d82-978a-1376abe5f47e
  Args:
    source: DoonAileenPlunket
    target: AileenSibellMaryGuinness
    relation: :hasMother
  AssignClass (4cda9396-e1da-4da4-acb5-9b313e02d199)
 Call ID: 4cda9396-e1da-4da4-acb5-9b313e02d199
  Args:
    source: EdwardGuinness
    type: :Man
  AssignClass (a3f7fdc9-a87f-4f30-a97f-acf2364739e8)
 Call ID: a3f7fdc9-a87f-4f30-a97f-acf2364739e8
  Args:
    source: EdwardGuinness
    type: :Person
  AddTriple (ce0a2afc-6824-4376-8005-9247c399f38e)
 Call ID: ce0a2afc-6824-4376-8005-9247c399f38e
  Args:
    relation: :hasFather
    source: AileenSibellMaryGuinness
    target: EdwardGuinness
  Finish (878d8fb3-4b54-4870-ac3c-0cf86bb9cff8)
 Call ID: 878d8fb3-4b54-4870-ac3c-0cf86bb9cff8
  Args: