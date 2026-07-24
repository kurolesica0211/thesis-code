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
Angelica Margherita Edwina Hicks (born 16 September 1992) is a British fashion illustrator and internet personality.
As the great-granddaughter of Louis Mountbatten, 1st Earl Mountbatten of Burma, she is a relative of the British royal family and is included in the line of succession to the British throne.
Early life and family

Hicks was born on 16 September 1992 to Marina Allegra Federica Silvia Tondato, an Italian designer, and Ashley Louis David Hicks, a British artist and interior designer.
Hicks' paternal grandparents were the English interior decorator and designer David Nightingale Hicks and Lady Pamela Mountbatten, who served as a bridesmaid and as a lady-in-waiting to Elizabeth II.
Through her grandmother, Hicks is a relative of the Mountbatten family, itself a branch of the German princely Battenberg family, and a relative of the British royal family.
Hicks' great-grandparents, Louis Mountbatten, 1st Earl Mountbatten of Burma and The Honourable Edwina Ashley, served as the Viceroy and Vicereine of India.
She is a great-great-granddaughter of Prince Louis of Battenberg (later the 1st Marquess of Milford Haven) and Princess Victoria of Hesse and by Rhine, a granddaughter of Queen Victoria.
Hicks grew up in Chelsea, London and was educated at a boarding school.
Career

Hicks works as a visual artist and fashion illustrator.
Hicks also made commissioned pieces for the American fashion designer Tory Burch and illustrated for the magazines Elle and Porter.
In 2021, Hicks launched a TikTok channel where she parodies haute couture outfits from red carpet events and fashion shows, recreating them out of duct tape, trash bags, metallic wrappers, foil, candy, and other materials.
Her recreations included a Louis Vuitton tank dress worn by Emma Corrin on the cover of Vogue, which she made out of multigrain crackers, a Maison Schiaparelli couture cape that she made out of a white mattress cover, and Cagole boots by Balenciaga that she made out of duct tape.
By July 2022, Hicks amassed over 48,000 followers and her videos collectively received over 4 million likes.
Her videos led to Hicks collaborating with Valentino and Vogue Italia.
By September 2022, Hicks had over 86,000 followers on TikTok.
Personal life

Hicks resides in Carroll Gardens in Brooklyn, New York.



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix ns1: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
@prefix ns2: <http://www.w3.org/2003/11/swrl#> .
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

ns1:isRuleEnabled a owl:AnnotationProperty .

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

:x a ns2:Variable .

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

:y a ns2:Variable .

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

[] a ns2:Imp ;
    rdfs:label "infer hasSon" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasBrother" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasSister" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (5be7b33c-75a0-483a-a201-b086ea827357)
 Call ID: 5be7b33c-75a0-483a-a201-b086ea827357
  Args:
    source: :AngelicaMargheritaEdwinaHicks
    type: :Woman
  AssignClass (8e7f6d6e-147d-4ecd-8f63-915b8b869de2)
 Call ID: 8e7f6d6e-147d-4ecd-8f63-915b8b869de2
  Args:
    type: :Person
    source: :AngelicaMargheritaEdwinaHicks
  AddLiteral (d5992513-8a63-4825-a1b6-fe25a3cc599d)
 Call ID: d5992513-8a63-4825-a1b6-fe25a3cc599d
  Args:
    literal_value: 1992
    relation: :hasBirthYear
    source: :AngelicaMargheritaEdwinaHicks
    literal_type: xsd:positiveInteger
  AssignClass (1abc740c-47ba-41be-baf9-9bc638df8215)
 Call ID: 1abc740c-47ba-41be-baf9-9bc638df8215
  Args:
    source: :MarinaAllegraFedericaSilviaTondato
    type: :Woman
  AssignClass (8857abdb-480d-4f93-acad-193d18328562)
 Call ID: 8857abdb-480d-4f93-acad-193d18328562
  Args:
    source: :MarinaAllegraFedericaSilviaTondato
    type: :Person
  AssignClass (d9b4a093-e4df-4b65-963f-4ee1c6404361)
 Call ID: d9b4a093-e4df-4b65-963f-4ee1c6404361
  Args:
    type: :Man
    source: :AshleyLouisDavidHicks
  AssignClass (3cb11761-15dd-482d-aaa8-c897d99f89ad)
 Call ID: 3cb11761-15dd-482d-aaa8-c897d99f89ad
  Args:
    type: :Person
    source: :AshleyLouisDavidHicks
  AddTriple (a5624da5-8211-4354-b98f-22d22def933c)
 Call ID: a5624da5-8211-4354-b98f-22d22def933c
  Args:
    relation: :hasMother
    source: :AngelicaMargheritaEdwinaHicks
    target: :MarinaAllegraFedericaSilviaTondato
  AddTriple (820a0547-fefa-47a7-bce3-9e19d2a3f52b)
 Call ID: 820a0547-fefa-47a7-bce3-9e19d2a3f52b
  Args:
    target: :AshleyLouisDavidHicks
    relation: :hasFather
    source: :AngelicaMargheritaEdwinaHicks
  AssignClass (8e9834d3-15b4-4e60-80aa-a169db7b6f4c)
 Call ID: 8e9834d3-15b4-4e60-80aa-a169db7b6f4c
  Args:
    type: :Man
    source: :DavidNightingaleHicks
  AssignClass (23f33657-d7ad-4a5f-8a1d-cdbd8dce9c2e)
 Call ID: 23f33657-d7ad-4a5f-8a1d-cdbd8dce9c2e
  Args:
    type: :Person
    source: :DavidNightingaleHicks
  AssignClass (bbc15b97-14ad-47fe-8ec8-29e08fe91778)
 Call ID: bbc15b97-14ad-47fe-8ec8-29e08fe91778
  Args:
    source: :LadyPamelaMountbatten
    type: :Woman
  AssignClass (9db82133-e8b2-4f98-a1bd-b163f4ed2ec2)
 Call ID: 9db82133-e8b2-4f98-a1bd-b163f4ed2ec2
  Args:
    type: :Person
    source: :LadyPamelaMountbatten
  AddTriple (0f50ff0d-3e08-4339-9578-eea95e679d2c)
 Call ID: 0f50ff0d-3e08-4339-9578-eea95e679d2c
  Args:
    source: :AshleyLouisDavidHicks
    relation: :hasFather
    target: :DavidNightingaleHicks
  AddTriple (d48a38a8-d177-4fca-8ec6-a8625ef60b8b)
 Call ID: d48a38a8-d177-4fca-8ec6-a8625ef60b8b
  Args:
    source: :AshleyLouisDavidHicks
    relation: :hasMother
    target: :LadyPamelaMountbatten
  AssignClass (4eacfe48-e155-4160-8b5f-2601db6c0d4a)
 Call ID: 4eacfe48-e155-4160-8b5f-2601db6c0d4a
  Args:
    source: :LouisMountbatten1stEarlMountbattenOfBurma
    type: :Man
  AssignClass (43ced7b2-05a9-49eb-a3cf-afe3b0cc80ce)
 Call ID: 43ced7b2-05a9-49eb-a3cf-afe3b0cc80ce
  Args:
    source: :LouisMountbatten1stEarlMountbattenOfBurma
    type: :Person
  AssignClass (8e0479e5-b260-4a5a-aba3-50fa73d77133)
 Call ID: 8e0479e5-b260-4a5a-aba3-50fa73d77133
  Args:
    source: :TheHonourableEdwinaAshley
    type: :Woman
  AssignClass (32bb40ab-21e9-478d-a39c-a0f6a076d7cd)
 Call ID: 32bb40ab-21e9-478d-a39c-a0f6a076d7cd
  Args:
    type: :Person
    source: :TheHonourableEdwinaAshley
  AddTriple (fa9cf3fe-c5fe-47cf-be8a-8647912dbe5d)
 Call ID: fa9cf3fe-c5fe-47cf-be8a-8647912dbe5d
  Args:
    relation: :hasFather
    source: :LadyPamelaMountbatten
    target: :LouisMountbatten1stEarlMountbattenOfBurma
  AddTriple (4f48132f-d7fc-4220-83b5-824b7c6c4347)
 Call ID: 4f48132f-d7fc-4220-83b5-824b7c6c4347
  Args:
    source: :LadyPamelaMountbatten
    relation: :hasMother
    target: :TheHonourableEdwinaAshley
  AssignClass (9f53f40f-7567-4b1d-aa87-19982280376f)
 Call ID: 9f53f40f-7567-4b1d-aa87-19982280376f
  Args:
    source: :PrinceLouisOfBattenberg
    type: :Man
  AssignClass (66ba12fe-0f24-406b-a803-21a095753f23)
 Call ID: 66ba12fe-0f24-406b-a803-21a095753f23
  Args:
    type: :Person
    source: :PrinceLouisOfBattenberg
  AssignClass (3031484a-5f63-40ce-b407-d2a10afc5901)
 Call ID: 3031484a-5f63-40ce-b407-d2a10afc5901
  Args:
    type: :Woman
    source: :PrincessVictoriaOfHesseAndByRhine
  AssignClass (9e0f9de6-eb79-44dd-9364-972122ae3588)
 Call ID: 9e0f9de6-eb79-44dd-9364-972122ae3588
  Args:
    source: :PrincessVictoriaOfHesseAndByRhine
    type: :Person
  AddTriple (3e6dc15c-8f77-43b3-b352-b924a3a0346f)
 Call ID: 3e6dc15c-8f77-43b3-b352-b924a3a0346f
  Args:
    target: :PrinceLouisOfBattenberg
    source: :LouisMountbatten1stEarlMountbattenOfBurma
    relation: :hasFather
  AddTriple (6731de1d-a925-4ab3-8253-b267528e5701)
 Call ID: 6731de1d-a925-4ab3-8253-b267528e5701
  Args:
    relation: :hasMother
    source: :LouisMountbatten1stEarlMountbattenOfBurma
    target: :PrincessVictoriaOfHesseAndByRhine
  AssignClass (c144006c-d2e5-4538-b960-3c6b22d79378)
 Call ID: c144006c-d2e5-4538-b960-3c6b22d79378
  Args:
    type: :Woman
    source: :QueenVictoria
  AssignClass (4f062a78-7986-4454-8ace-10c73b9f4ad6)
 Call ID: 4f062a78-7986-4454-8ace-10c73b9f4ad6
  Args:
    type: :Person
    source: :QueenVictoria
  AddTriple (412671cf-88e9-45fc-ba1a-df4f57937812)
 Call ID: 412671cf-88e9-45fc-ba1a-df4f57937812
  Args:
    source: :PrincessVictoriaOfHesseAndByRhine
    relation: :hasMother
    target: :QueenVictoria
  Finish (0cf0a32a-5a5c-4994-ab2c-0ac19889df43)
 Call ID: 0cf0a32a-5a5c-4994-ab2c-0ac19889df43
  Args: