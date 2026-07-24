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
Princess Marie Louise of Hanover and Cumberland (11 October 1879 – 31 January 1948) was the eldest child of Ernest Augustus, Crown Prince of Hanover, and Princess Thyra of Denmark, the youngest daughter of Christian IX of Denmark and Louise of Hesse-Kassel.
Through her father, Marie Louise was a great-great-granddaughter of George III of the United Kingdom and Charlotte of Mecklenburg-Strelitz.
Marriage and children

Marie Louise married Prince Maximilian of Baden (1867–1929), her third cousin twice removed, on 10 July 1900 in Gmunden, Austria-Hungary.
He was the son of Prince Wilhelm of Baden and Princess Maria Maximilianovna of Leuchtenberg and became a first cousin twice removed of Napoleon III of France.
Marie Louise and Maximilian had one daughter and one son:


Ancestry

References

External links



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
  AssignClass (e532efa3-b3cf-4e74-9af6-25098829c264)
 Call ID: e532efa3-b3cf-4e74-9af6-25098829c264
  Args:
    source: :PrincessMarieLouiseOfHanoverAndCumberland
    type: :Woman
  AssignClass (8c2e5773-bdbd-4a62-b89e-4901d3b9c945)
 Call ID: 8c2e5773-bdbd-4a62-b89e-4901d3b9c945
  Args:
    source: :PrincessMarieLouiseOfHanoverAndCumberland
    type: :Person
  AddLiteral (c9921428-bdcc-4a0b-bebb-4857afaa41ba)
 Call ID: c9921428-bdcc-4a0b-bebb-4857afaa41ba
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: :PrincessMarieLouiseOfHanoverAndCumberland
    literal_value: 1879
  AddLiteral (28b9ca16-eab1-45ff-b9bf-42a907688216)
 Call ID: 28b9ca16-eab1-45ff-b9bf-42a907688216
  Args:
    source: :PrincessMarieLouiseOfHanoverAndCumberland
    literal_value: 1948
    literal_type: xsd:integer
    relation: :hasDeathYear
  AssignClass (455fb1d5-d738-494f-9f45-fc37cda8fe1e)
 Call ID: 455fb1d5-d738-494f-9f45-fc37cda8fe1e
  Args:
    type: :Man
    source: :ErnestAugustusCrownPrinceOfHanover
  AssignClass (fd13a74c-b87d-474a-b437-929592bf36e2)
 Call ID: fd13a74c-b87d-474a-b437-929592bf36e2
  Args:
    source: :ErnestAugustusCrownPrinceOfHanover
    type: :Person
  AssignClass (cbe21855-a6b1-41ba-a611-43329d1bae93)
 Call ID: cbe21855-a6b1-41ba-a611-43329d1bae93
  Args:
    type: :Woman
    source: :PrincessThyraOfDenmark
  AssignClass (fa2d3e61-3e00-4776-b100-ce2c4cdf4298)
 Call ID: fa2d3e61-3e00-4776-b100-ce2c4cdf4298
  Args:
    source: :PrincessThyraOfDenmark
    type: :Person
  AddTriple (6464dbde-6520-4a2d-906b-b532269a4a76)
 Call ID: 6464dbde-6520-4a2d-906b-b532269a4a76
  Args:
    relation: :hasFather
    target: :ErnestAugustusCrownPrinceOfHanover
    source: :PrincessMarieLouiseOfHanoverAndCumberland
  AddTriple (8e8279a0-8b69-4d1f-b4cc-b24d042f02ad)
 Call ID: 8e8279a0-8b69-4d1f-b4cc-b24d042f02ad
  Args:
    relation: :hasMother
    target: :PrincessThyraOfDenmark
    source: :PrincessMarieLouiseOfHanoverAndCumberland
  AssignClass (b4769827-0a7e-4e63-946e-cbb0daa9c933)
 Call ID: b4769827-0a7e-4e63-946e-cbb0daa9c933
  Args:
    source: :ChristianIXOfDenmark
    type: :Man
  AssignClass (803317d5-ffe6-4a3e-859f-4a21c6dd0131)
 Call ID: 803317d5-ffe6-4a3e-859f-4a21c6dd0131
  Args:
    type: :Person
    source: :ChristianIXOfDenmark
  AssignClass (32cbd086-5be8-4142-a911-e02fe9dab4bd)
 Call ID: 32cbd086-5be8-4142-a911-e02fe9dab4bd
  Args:
    type: :Woman
    source: :LouiseOfHesseKassel
  AssignClass (fc26b765-ba01-4564-b687-3352879388bf)
 Call ID: fc26b765-ba01-4564-b687-3352879388bf
  Args:
    type: :Person
    source: :LouiseOfHesseKassel
  AddTriple (b6927cd1-5090-4253-b762-292b258bf778)
 Call ID: b6927cd1-5090-4253-b762-292b258bf778
  Args:
    source: :PrincessThyraOfDenmark
    target: :ChristianIXOfDenmark
    relation: :hasFather
  AddTriple (7d75af45-6ba2-4052-9b24-e9f180908c7f)
 Call ID: 7d75af45-6ba2-4052-9b24-e9f180908c7f
  Args:
    source: :PrincessThyraOfDenmark
    relation: :hasMother
    target: :LouiseOfHesseKassel
  AssignClass (1382e89c-79bb-4247-ae76-a8701fa31f93)
 Call ID: 1382e89c-79bb-4247-ae76-a8701fa31f93
  Args:
    type: :Man
    source: :GeorgeIIIOfTheUnitedKingdom
  AssignClass (17bea0d6-1ad7-47fe-9ee2-cbaa9b8f37e4)
 Call ID: 17bea0d6-1ad7-47fe-9ee2-cbaa9b8f37e4
  Args:
    type: :Person
    source: :GeorgeIIIOfTheUnitedKingdom
  AssignClass (1a1a49e0-83cc-4dc6-bc40-d42740b88ef0)
 Call ID: 1a1a49e0-83cc-4dc6-bc40-d42740b88ef0
  Args:
    source: :CharlotteOfMecklenburgStrelitz
    type: :Woman
  AssignClass (8ca51f0f-f089-4931-a8d6-af2bc94d9aaa)
 Call ID: 8ca51f0f-f089-4931-a8d6-af2bc94d9aaa
  Args:
    type: :Person
    source: :CharlotteOfMecklenburgStrelitz
  AddTriple (55dedb38-31bc-48e6-b78e-b0e72c501cee)
 Call ID: 55dedb38-31bc-48e6-b78e-b0e72c501cee
  Args:
    relation: :hasAncestor
    target: :GeorgeIIIOfTheUnitedKingdom
    source: :PrincessMarieLouiseOfHanoverAndCumberland
  AddTriple (e6c0f15b-2f4a-4e47-ac1b-64d8b88f8930)
 Call ID: e6c0f15b-2f4a-4e47-ac1b-64d8b88f8930
  Args:
    target: :CharlotteOfMecklenburgStrelitz
    relation: :hasAncestor
    source: :PrincessMarieLouiseOfHanoverAndCumberland
  AssignClass (d452cdca-f9d5-46d9-87ba-be043434caa6)
 Call ID: d452cdca-f9d5-46d9-87ba-be043434caa6
  Args:
    type: :Man
    source: :PrinceMaximilianOfBaden
  AssignClass (bb715148-a793-4358-bf11-0f97e59e6a78)
 Call ID: bb715148-a793-4358-bf11-0f97e59e6a78
  Args:
    source: :PrinceMaximilianOfBaden
    type: :Person
  AddLiteral (c78f48d2-b011-41d2-bd25-a1be61869ad2)
 Call ID: c78f48d2-b011-41d2-bd25-a1be61869ad2
  Args:
    source: :PrinceMaximilianOfBaden
    literal_value: 1867
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (b1282c4a-9c80-4d06-aa40-6d569b5e2673)
 Call ID: b1282c4a-9c80-4d06-aa40-6d569b5e2673
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: :PrinceMaximilianOfBaden
    literal_value: 1929
  AddLiteral (faee8833-2da7-4e3d-b601-8491805d7096)
 Call ID: faee8833-2da7-4e3d-b601-8491805d7096
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 1900
    source: :PrincessMarieLouiseOfHanoverAndCumberland
  AddTriple (fa9654fa-869f-4efd-847e-8839947ad3ec)
 Call ID: fa9654fa-869f-4efd-847e-8839947ad3ec
  Args:
    target: :PrinceMaximilianOfBaden
    relation: :hasRelation
    source: :PrincessMarieLouiseOfHanoverAndCumberland
  AssignClass (4f12ceb8-637e-4c08-b1ed-a8c076b47933)
 Call ID: 4f12ceb8-637e-4c08-b1ed-a8c076b47933
  Args:
    type: :Man
    source: :PrinceWilhelmOfBaden
  AssignClass (78875a32-5304-402e-9453-55c563fea7c5)
 Call ID: 78875a32-5304-402e-9453-55c563fea7c5
  Args:
    source: :PrinceWilhelmOfBaden
    type: :Person
  AssignClass (29dd68c4-94cb-4813-9ff2-2333f103854b)
 Call ID: 29dd68c4-94cb-4813-9ff2-2333f103854b
  Args:
    type: :Woman
    source: :PrincessMariaMaximilianovnaOfLeuchtenberg
  AssignClass (c0c44db5-8746-4808-8d9e-b2ab472a22f8)
 Call ID: c0c44db5-8746-4808-8d9e-b2ab472a22f8
  Args:
    type: :Person
    source: :PrincessMariaMaximilianovnaOfLeuchtenberg
  AddTriple (443c9725-24f9-4afe-ae0c-0ba1b7265795)
 Call ID: 443c9725-24f9-4afe-ae0c-0ba1b7265795
  Args:
    source: :PrinceMaximilianOfBaden
    relation: :hasFather
    target: :PrinceWilhelmOfBaden
  AddTriple (03ea88e1-7001-49c9-8a83-2456200a0588)
 Call ID: 03ea88e1-7001-49c9-8a83-2456200a0588
  Args:
    source: :PrinceMaximilianOfBaden
    target: :PrincessMariaMaximilianovnaOfLeuchtenberg
    relation: :hasMother
  Finish (38a9bb75-7498-4f54-b8d4-2b2ba0518619)
 Call ID: 38a9bb75-7498-4f54-b8d4-2b2ba0518619
  Args: