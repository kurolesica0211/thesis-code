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
Prince Maurice of Battenberg (Maurice Victor Donald; 3 October 1891 – 27 October 1914) was a member of the Hessian princely Battenberg family and the extended British royal family, and the youngest grandchild of Queen Victoria.
He was styled as Prince Maurice throughout his life and died before the Battenberg family anglicised their surname to Mountbatten in 1917, meaning he was never known by that name.
Early life

Maurice was born on 3 October 1891.
His father was Prince Henry of Battenberg, the son of Prince Alexander of Hesse and by Rhine and Julie Therese née Countess of Hauke.
His mother was Princess Henry of Battenberg (née Princess Beatrice of the United Kingdom), the fifth daughter and the youngest child of Queen Victoria and Albert, Prince Consort.
As he was the child of a morganatic marriage, Prince Henry of Battenberg took his style of Prince of Battenberg from his mother, Countess Julia Hauke, who was created Princess of Battenberg in her own right.
As such, Maurice was styled as His Serene Highness Prince Maurice of Battenberg from birth.
In the United Kingdom, he was styled His Highness Prince Maurice of Battenberg under a royal warrant passed by Queen Victoria in 1886.
His godparents were the Duchess of Connaught and Strathearn (represented by Queen Victoria), the Princess of Leiningen (represented by Princess Christian of Schleswig-Holstein), the Duke of Clarence and Avondale (represented by Sir Henry Ponsonby), Prince Francis Joseph of Battenberg (represented by Sir Fleetwood Edwards) and the Hereditary Grand Duke of Hesse.
The youngest of his four siblings, Maurice most resembled his father, who died when he was only four, the same age his mother was when her own father died.
His elder sister Victoria Eugenie of Battenberg married Alfonso XIII of Spain and was Queen Consort of Spain between 1906 and 1931.
Later life

Maurice attended Wellington College and was a member of Benson House.
Maurice was made a Freemason in the Old Wellingtonian Lodge No. 3404 (the Lodge of the Old Wellingtonians) on 21 June 1912 and was installed Master of the Twelve Brothers Lodge, No. 785 Southampton on 22 April 1914.
After attending the Royal Military College, Sandhurst, Maurice was commissioned as a second lieutenant in the King's Royal Rifle Corps on 4 March 1911.
Poor  Maurice was killed outright just on top of the ridge.
"


Word of the Maurice's death was passed to Brigadier-General Fanshawe, commander of the 6th Infantry Brigade.
He said, "By the death of H.H. Prince Maurice of Battenberg the Army loses a most gallant and valuable officer.
His mother, Princess Beatrice, declined the offer of Lord Kitchener to have her son's body repatriated.
The battalion war diary notes that his funeral took place on 31 October 1914 and records that, "Denison, Gough, the Sgt Major, Sgt O'Leary and a few others went down to poor Maurice's funeral in Ypres".



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
  AssignClass (108994c4-53ab-4674-af44-8f6bc40edb2b)
 Call ID: 108994c4-53ab-4674-af44-8f6bc40edb2b
  Args:
    source: Prince_Maurice_of_Battenberg
    type: :Man
  AssignClass (05278030-aa04-4373-b74c-80b8d075606f)
 Call ID: 05278030-aa04-4373-b74c-80b8d075606f
  Args:
    type: :Person
    source: Prince_Maurice_of_Battenberg
  AddLiteral (263e5055-3030-44d6-a292-7ef50ed44267)
 Call ID: 263e5055-3030-44d6-a292-7ef50ed44267
  Args:
    source: Prince_Maurice_of_Battenberg
    literal_type: xsd:integer
    literal_value: 1891
    relation: :hasBirthYear
  AddLiteral (15ea6f31-0a72-4d55-b54f-c362c4d4c932)
 Call ID: 15ea6f31-0a72-4d55-b54f-c362c4d4c932
  Args:
    relation: :hasDeathYear
    literal_value: 1914
    source: Prince_Maurice_of_Battenberg
    literal_type: xsd:integer
  AssignClass (3bec4cfa-7e26-445f-b65c-e2295b95ab8a)
 Call ID: 3bec4cfa-7e26-445f-b65c-e2295b95ab8a
  Args:
    source: Prince_Henry_of_Battenberg
    type: :Man
  AssignClass (bef57be1-2c74-4baa-9d71-98e3b9191d3f)
 Call ID: bef57be1-2c74-4baa-9d71-98e3b9191d3f
  Args:
    type: :Person
    source: Prince_Henry_of_Battenberg
  AddTriple (07c8db6b-7821-4c99-94a4-66b0e9d12575)
 Call ID: 07c8db6b-7821-4c99-94a4-66b0e9d12575
  Args:
    target: Prince_Henry_of_Battenberg
    relation: :hasFather
    source: Prince_Maurice_of_Battenberg
  AssignClass (d7389c52-340c-48e8-bcfb-880ecea1bba1)
 Call ID: d7389c52-340c-48e8-bcfb-880ecea1bba1
  Args:
    type: :Woman
    source: Princess_Beatrice_of_the_United_Kingdom
  AssignClass (4411b99c-3bff-4092-b358-88d8ba536a3c)
 Call ID: 4411b99c-3bff-4092-b358-88d8ba536a3c
  Args:
    type: :Person
    source: Princess_Beatrice_of_the_United_Kingdom
  AddTriple (198ec95b-3ed3-401a-9f06-365226c3c09f)
 Call ID: 198ec95b-3ed3-401a-9f06-365226c3c09f
  Args:
    relation: :hasMother
    target: Princess_Beatrice_of_the_United_Kingdom
    source: Prince_Maurice_of_Battenberg
  AssignClass (dfc79726-f8e1-49f9-93ab-73c362bfca00)
 Call ID: dfc79726-f8e1-49f9-93ab-73c362bfca00
  Args:
    source: Prince_Alexander_of_Hesse_and_by_Rhine
    type: :Man
  AssignClass (9e4a96b3-0096-494e-8d62-88950b2801b9)
 Call ID: 9e4a96b3-0096-494e-8d62-88950b2801b9
  Args:
    type: :Person
    source: Prince_Alexander_of_Hesse_and_by_Rhine
  AddTriple (7ca6e5e1-b793-4190-b590-b7b453fa4c2b)
 Call ID: 7ca6e5e1-b793-4190-b590-b7b453fa4c2b
  Args:
    source: Prince_Henry_of_Battenberg
    relation: :hasFather
    target: Prince_Alexander_of_Hesse_and_by_Rhine
  AssignClass (6d846b50-7463-455f-afe4-ccb54034e283)
 Call ID: 6d846b50-7463-455f-afe4-ccb54034e283
  Args:
    type: :Woman
    source: Julie_Therese_Countess_of_Hauke
  AssignClass (b0a6add4-225f-4145-84aa-77328c1e59a3)
 Call ID: b0a6add4-225f-4145-84aa-77328c1e59a3
  Args:
    source: Julie_Therese_Countess_of_Hauke
    type: :Person
  AddTriple (00ad1ce1-fa8b-4a2b-8ebf-24efd5f5dc2a)
 Call ID: 00ad1ce1-fa8b-4a2b-8ebf-24efd5f5dc2a
  Args:
    source: Prince_Henry_of_Battenberg
    relation: :hasMother
    target: Julie_Therese_Countess_of_Hauke
  AssignClass (76b4dbbb-058b-44d3-adc3-10c6fb131b0f)
 Call ID: 76b4dbbb-058b-44d3-adc3-10c6fb131b0f
  Args:
    type: :Woman
    source: Queen_Victoria
  AssignClass (67c60619-8a85-47cc-9a54-d891bd783024)
 Call ID: 67c60619-8a85-47cc-9a54-d891bd783024
  Args:
    type: :Person
    source: Queen_Victoria
  AssignClass (22329086-7688-4c7a-90f1-a46b90c1aeae)
 Call ID: 22329086-7688-4c7a-90f1-a46b90c1aeae
  Args:
    type: :Man
    source: Albert_Prince_Consort
  AssignClass (3f34101f-7fa3-457c-b3d3-101dacc8c09f)
 Call ID: 3f34101f-7fa3-457c-b3d3-101dacc8c09f
  Args:
    type: :Person
    source: Albert_Prince_Consort
  AddTriple (944107d3-4b4b-4709-91e7-e96ef5503dc6)
 Call ID: 944107d3-4b4b-4709-91e7-e96ef5503dc6
  Args:
    relation: :hasMother
    target: Queen_Victoria
    source: Princess_Beatrice_of_the_United_Kingdom
  AddTriple (c5d3d7e2-27ce-4a4e-9e00-3cbab3d9f59d)
 Call ID: c5d3d7e2-27ce-4a4e-9e00-3cbab3d9f59d
  Args:
    source: Princess_Beatrice_of_the_United_Kingdom
    relation: :hasFather
    target: Albert_Prince_Consort
  AssignClass (2a6851d2-2250-4a4b-8fad-fe23dd429561)
 Call ID: 2a6851d2-2250-4a4b-8fad-fe23dd429561
  Args:
    type: :Woman
    source: Victoria_Eugenie_of_Battenberg
  AssignClass (2f262ed9-4078-4340-b9d5-824c2e3089e3)
 Call ID: 2f262ed9-4078-4340-b9d5-824c2e3089e3
  Args:
    type: :Person
    source: Victoria_Eugenie_of_Battenberg
  AddTriple (bfeb8595-9704-4a65-b099-cea1a872c396)
 Call ID: bfeb8595-9704-4a65-b099-cea1a872c396
  Args:
    source: Victoria_Eugenie_of_Battenberg
    relation: :isSisterOf
    target: Prince_Maurice_of_Battenberg
  Finish (ddd20552-4398-43b1-98dc-16ecf805c8f0)
 Call ID: ddd20552-4398-43b1-98dc-16ecf805c8f0
  Args: