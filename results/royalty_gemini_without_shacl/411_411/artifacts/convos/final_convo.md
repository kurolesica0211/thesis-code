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
Duke Christian Louis of Mecklenburg (German: Christian-Ludwig Herzog zu Mecklenburg; 29 September 1912 – 18 July 1996) was the second son of the last reigning Grand Duke of Mecklenburg-Schwerin, Frederick Francis IV.
Early life

Born in Schloss Ludwigslust, as a member of an elder, Mecklenburg-Schwerin line of an ancient House of Mecklenburg, he was the second child of the reigning Grand Duke of Mecklenburg-Schwerin, Frederick Francis IV, and his wife, Princess Alexandra of Hanover, third child and second daughter of Ernest Augustus, Crown Prince of Hanover and Princess Thyra of Denmark.
After the abolition of the monarchy, in 1919 the family went at the invitation of Queen Alexandrine, consort of Christian X of Denmark and sister of the Grand Duke, into exile in Denmark, where they lived for a year in Sorgenfri Palace.
Later, the family returned to Mecklenburg and lived in Gelbensande, and from 1921 the family settled at Ludwigslust Castle.
After the war

When the war ended, Ludwigslust was first occupied by the British, but soon was transferred to the Soviet occupation, so that Christian Louis initially went with his family to Glücksburg Castle in Schleswig-Holstein.
Together with his sister Thyra, he took part in the ship tour organized by Queen Frederica and her husband King Paul of Greece in 1954, which became known as the “Cruise of the Kings” and was attended by over 100 royals from all over Europe.
Marriage and family

On 5 July 1954 in Glücksburg, Christian Louis married in a civil wedding Princess Barbara of Prussia (1920–1994), the daughter of Prince Sigismund of Prussia and his wife, Princess Charlotte of Saxe-Altenburg.



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
  AssignClass (2d9333af-638c-4f34-b0a6-6300a627f3b1)
 Call ID: 2d9333af-638c-4f34-b0a6-6300a627f3b1
  Args:
    type: :Man
    source: :ChristianLouisOfMecklenburg
  AssignClass (6a8a05cc-ca91-4848-902f-69ce3f464a08)
 Call ID: 6a8a05cc-ca91-4848-902f-69ce3f464a08
  Args:
    source: :ChristianLouisOfMecklenburg
    type: :Person
  AddLiteral (202de757-90d4-4a4b-85d3-807a279b8240)
 Call ID: 202de757-90d4-4a4b-85d3-807a279b8240
  Args:
    source: :ChristianLouisOfMecklenburg
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1912
  AddLiteral (2ede4db2-bc9f-4791-a8ec-1ee357b2e60e)
 Call ID: 2ede4db2-bc9f-4791-a8ec-1ee357b2e60e
  Args:
    literal_value: 1996
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: :ChristianLouisOfMecklenburg
  AssignClass (76bf225f-91d1-49fa-8165-442f917edccd)
 Call ID: 76bf225f-91d1-49fa-8165-442f917edccd
  Args:
    type: :Man
    source: :FrederickFrancisIV
  AssignClass (95a8e2ba-428c-471b-8592-3aa20e0d1b44)
 Call ID: 95a8e2ba-428c-471b-8592-3aa20e0d1b44
  Args:
    source: :FrederickFrancisIV
    type: :Person
  AddTriple (35a6fa76-8c32-4b52-9377-a9657d72af73)
 Call ID: 35a6fa76-8c32-4b52-9377-a9657d72af73
  Args:
    source: :ChristianLouisOfMecklenburg
    relation: :hasFather
    target: :FrederickFrancisIV
  AssignClass (0c892c19-8276-49e8-8a86-91fce7de91ad)
 Call ID: 0c892c19-8276-49e8-8a86-91fce7de91ad
  Args:
    source: :PrincessAlexandraOfHanover
    type: :Woman
  AssignClass (4d71ad6f-3091-42b0-a95e-2bf2d10e738a)
 Call ID: 4d71ad6f-3091-42b0-a95e-2bf2d10e738a
  Args:
    source: :PrincessAlexandraOfHanover
    type: :Person
  AddTriple (3208fdc5-ea37-4778-affe-07c5f0c1f096)
 Call ID: 3208fdc5-ea37-4778-affe-07c5f0c1f096
  Args:
    target: :PrincessAlexandraOfHanover
    relation: :hasMother
    source: :ChristianLouisOfMecklenburg
  AssignClass (47993a38-652d-4310-8ac2-b5949cc7b131)
 Call ID: 47993a38-652d-4310-8ac2-b5949cc7b131
  Args:
    type: :Man
    source: :ErnestAugustusCrownPrinceOfHanover
  AssignClass (95574a29-261e-4813-ae97-14b3e8974781)
 Call ID: 95574a29-261e-4813-ae97-14b3e8974781
  Args:
    source: :ErnestAugustusCrownPrinceOfHanover
    type: :Person
  AddTriple (048a4ce1-4508-4b49-8b67-a0061cb26347)
 Call ID: 048a4ce1-4508-4b49-8b67-a0061cb26347
  Args:
    target: :ErnestAugustusCrownPrinceOfHanover
    relation: :hasFather
    source: :PrincessAlexandraOfHanover
  AssignClass (04c81bfb-b47d-4577-90f4-cfd659734427)
 Call ID: 04c81bfb-b47d-4577-90f4-cfd659734427
  Args:
    source: :PrincessThyraOfDenmark
    type: :Woman
  AssignClass (7514dd67-ca4d-4040-ab73-c12d2975dd2c)
 Call ID: 7514dd67-ca4d-4040-ab73-c12d2975dd2c
  Args:
    type: :Person
    source: :PrincessThyraOfDenmark
  AddTriple (02275f78-0f15-473a-a7d5-5a8ad5772b3a)
 Call ID: 02275f78-0f15-473a-a7d5-5a8ad5772b3a
  Args:
    relation: :hasMother
    target: :PrincessThyraOfDenmark
    source: :PrincessAlexandraOfHanover
  AssignClass (eccef649-d0d9-434e-94b1-1c342f8e4836)
 Call ID: eccef649-d0d9-434e-94b1-1c342f8e4836
  Args:
    type: :Woman
    source: :ThyraMecklenburg
  AssignClass (6a24c6ce-918e-47b2-8e81-9d7fcd6c06f2)
 Call ID: 6a24c6ce-918e-47b2-8e81-9d7fcd6c06f2
  Args:
    source: :ThyraMecklenburg
    type: :Person
  AddTriple (b2c4a172-16c7-4803-ad74-fb9be9404a73)
 Call ID: b2c4a172-16c7-4803-ad74-fb9be9404a73
  Args:
    source: :ChristianLouisOfMecklenburg
    relation: :isSiblingOf
    target: :ThyraMecklenburg
  AssignClass (bb0b8b56-afec-4263-a1ae-ad2c8ae7834d)
 Call ID: bb0b8b56-afec-4263-a1ae-ad2c8ae7834d
  Args:
    source: :PrincessBarbaraOfPrussia
    type: :Woman
  AssignClass (ca666414-d321-4ee8-814e-ff424e105e3d)
 Call ID: ca666414-d321-4ee8-814e-ff424e105e3d
  Args:
    source: :PrincessBarbaraOfPrussia
    type: :Person
  AddLiteral (21efa8a7-aef4-4388-bd1a-b7a159507524)
 Call ID: 21efa8a7-aef4-4388-bd1a-b7a159507524
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1920
    source: :PrincessBarbaraOfPrussia
  AddLiteral (e93f97ef-75ab-40a0-8de4-c98cc0216fa1)
 Call ID: e93f97ef-75ab-40a0-8de4-c98cc0216fa1
  Args:
    literal_value: 1994
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: :PrincessBarbaraOfPrussia
  AddLiteral (0e30837e-cc93-4713-b86b-2102f12341fa)
 Call ID: 0e30837e-cc93-4713-b86b-2102f12341fa
  Args:
    relation: :hasMarriageYear
    literal_value: 1954
    literal_type: xsd:integer
    source: :ChristianLouisOfMecklenburg
  AddTriple (7239a6b6-9316-4244-bef5-7020a5eb8222)
 Call ID: 7239a6b6-9316-4244-bef5-7020a5eb8222
  Args:
    relation: :hasRelation
    target: :PrincessBarbaraOfPrussia
    source: :ChristianLouisOfMecklenburg
  AssignClass (351d023a-9bb8-4278-a1fe-a6b8ce3ced60)
 Call ID: 351d023a-9bb8-4278-a1fe-a6b8ce3ced60
  Args:
    source: :PrinceSigismundOfPrussia
    type: :Man
  AssignClass (a8d3a6e4-4473-46be-9fe6-b64d95a180b9)
 Call ID: a8d3a6e4-4473-46be-9fe6-b64d95a180b9
  Args:
    type: :Person
    source: :PrinceSigismundOfPrussia
  AddTriple (c2be74c8-41c2-44ab-8ffb-bd83182da404)
 Call ID: c2be74c8-41c2-44ab-8ffb-bd83182da404
  Args:
    target: :PrinceSigismundOfPrussia
    relation: :hasFather
    source: :PrincessBarbaraOfPrussia
  AssignClass (ab18a687-daa8-4f26-bebc-09d9da1d0735)
 Call ID: ab18a687-daa8-4f26-bebc-09d9da1d0735
  Args:
    source: :PrincessCharlotteOfSaxeAltenburg
    type: :Woman
  AssignClass (78405999-9e2d-4b57-b36d-42bc282a5baf)
 Call ID: 78405999-9e2d-4b57-b36d-42bc282a5baf
  Args:
    type: :Person
    source: :PrincessCharlotteOfSaxeAltenburg
  AddTriple (e73bded3-c0e9-459d-803a-2e766ffd790a)
 Call ID: e73bded3-c0e9-459d-803a-2e766ffd790a
  Args:
    source: :PrincessBarbaraOfPrussia
    target: :PrincessCharlotteOfSaxeAltenburg
    relation: :hasMother
  Finish (a7a2986d-0616-412c-9e38-fc5b8749fa0a)
 Call ID: a7a2986d-0616-412c-9e38-fc5b8749fa0a
  Args: