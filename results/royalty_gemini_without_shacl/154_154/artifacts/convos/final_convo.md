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
  AssignClass (657215c3-4b33-4e1f-8b08-b73a42b7b9f8)
 Call ID: 657215c3-4b33-4e1f-8b08-b73a42b7b9f8
  Args:
    type: :Man
    source: :Maurice_of_Battenberg
  AssignClass (c5ef0a51-133d-436c-9318-7020e461dd7a)
 Call ID: c5ef0a51-133d-436c-9318-7020e461dd7a
  Args:
    type: :Person
    source: :Maurice_of_Battenberg
  AddLiteral (78a5bf02-b26f-49f0-bcbe-d587502a06fd)
 Call ID: 78a5bf02-b26f-49f0-bcbe-d587502a06fd
  Args:
    literal_value: 1891
    source: :Maurice_of_Battenberg
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (019c220d-f9bf-49a6-beb4-0a7f3211c2b1)
 Call ID: 019c220d-f9bf-49a6-beb4-0a7f3211c2b1
  Args:
    literal_value: 1914
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: :Maurice_of_Battenberg
  AssignClass (6791caa2-fa4c-46e3-97e1-6329d5437512)
 Call ID: 6791caa2-fa4c-46e3-97e1-6329d5437512
  Args:
    type: :Man
    source: :Henry_of_Battenberg
  AssignClass (8e222fd3-9ff2-4272-aca3-fd9f81c0b794)
 Call ID: 8e222fd3-9ff2-4272-aca3-fd9f81c0b794
  Args:
    source: :Henry_of_Battenberg
    type: :Person
  AddTriple (d931e946-6d3e-4490-88d8-a82f76bec8a1)
 Call ID: d931e946-6d3e-4490-88d8-a82f76bec8a1
  Args:
    target: :Henry_of_Battenberg
    relation: :hasFather
    source: :Maurice_of_Battenberg
  AssignClass (e5e983a5-7793-4b8d-87f9-d5dfa69d92de)
 Call ID: e5e983a5-7793-4b8d-87f9-d5dfa69d92de
  Args:
    type: :Man
    source: :Alexander_of_Hesse_and_by_Rhine
  AssignClass (a6a73db3-964e-4acb-adb5-070866eb0a52)
 Call ID: a6a73db3-964e-4acb-adb5-070866eb0a52
  Args:
    type: :Person
    source: :Alexander_of_Hesse_and_by_Rhine
  AddTriple (87a61a78-cf6d-4c5b-a405-dfe94bf37e2b)
 Call ID: 87a61a78-cf6d-4c5b-a405-dfe94bf37e2b
  Args:
    target: :Alexander_of_Hesse_and_by_Rhine
    source: :Henry_of_Battenberg
    relation: :hasFather
  AssignClass (8af42dfa-1643-46cf-bbd0-7a23cb1548b8)
 Call ID: 8af42dfa-1643-46cf-bbd0-7a23cb1548b8
  Args:
    source: :Julie_Therese_Hauke
    type: :Woman
  AssignClass (bfeecbdf-1442-4b91-8a21-480e6f488d1b)
 Call ID: bfeecbdf-1442-4b91-8a21-480e6f488d1b
  Args:
    source: :Julie_Therese_Hauke
    type: :Person
  AddTriple (c1aa3885-79c0-455b-9540-045d67f82aa0)
 Call ID: c1aa3885-79c0-455b-9540-045d67f82aa0
  Args:
    relation: :hasMother
    source: :Henry_of_Battenberg
    target: :Julie_Therese_Hauke
  AssignClass (e8e799a3-2ce3-4ca7-bcd0-6d314402e43b)
 Call ID: e8e799a3-2ce3-4ca7-bcd0-6d314402e43b
  Args:
    type: :Woman
    source: :Princess_Beatrice
  AssignClass (91d2802f-db0e-4bae-b850-211f2100f172)
 Call ID: 91d2802f-db0e-4bae-b850-211f2100f172
  Args:
    source: :Princess_Beatrice
    type: :Person
  AddTriple (c56a19dd-7f16-4c8b-8aa9-da86fe2d9f7e)
 Call ID: c56a19dd-7f16-4c8b-8aa9-da86fe2d9f7e
  Args:
    target: :Princess_Beatrice
    relation: :hasMother
    source: :Maurice_of_Battenberg
  AssignClass (6c0826f1-2ba6-4a3a-ae28-a92e64eb39ec)
 Call ID: 6c0826f1-2ba6-4a3a-ae28-a92e64eb39ec
  Args:
    source: :Queen_Victoria
    type: :Woman
  AssignClass (6f7c7661-dd51-461e-b28e-502625609b5b)
 Call ID: 6f7c7661-dd51-461e-b28e-502625609b5b
  Args:
    source: :Queen_Victoria
    type: :Person
  AddTriple (f9468f83-853d-4901-8abf-9c6be1e02afa)
 Call ID: f9468f83-853d-4901-8abf-9c6be1e02afa
  Args:
    source: :Princess_Beatrice
    relation: :hasMother
    target: :Queen_Victoria
  AssignClass (57681b3e-97d1-4d80-b4f0-a13d60aeb686)
 Call ID: 57681b3e-97d1-4d80-b4f0-a13d60aeb686
  Args:
    source: :Albert_Prince_Consort
    type: :Man
  AssignClass (49a51238-65fe-49dc-9b2f-7f5ae82b7df1)
 Call ID: 49a51238-65fe-49dc-9b2f-7f5ae82b7df1
  Args:
    type: :Person
    source: :Albert_Prince_Consort
  AddTriple (29adbff4-f9ce-4edb-b98c-8d2c3c8612e1)
 Call ID: 29adbff4-f9ce-4edb-b98c-8d2c3c8612e1
  Args:
    relation: :hasFather
    source: :Princess_Beatrice
    target: :Albert_Prince_Consort
  AssignClass (1d18de04-9034-4cd3-8b32-952bbb049b34)
 Call ID: 1d18de04-9034-4cd3-8b32-952bbb049b34
  Args:
    type: :Woman
    source: :Victoria_Eugenie_of_Battenberg
  AssignClass (66e5732e-ea85-4232-9eec-668f6019dad6)
 Call ID: 66e5732e-ea85-4232-9eec-668f6019dad6
  Args:
    type: :Person
    source: :Victoria_Eugenie_of_Battenberg
  AddTriple (2ab942ef-e2ae-4230-ba14-aed3d5e2bbbc)
 Call ID: 2ab942ef-e2ae-4230-ba14-aed3d5e2bbbc
  Args:
    relation: :hasSister
    source: :Maurice_of_Battenberg
    target: :Victoria_Eugenie_of_Battenberg
  AddTriple (2bf52957-95ea-4447-8e39-f3ddfcf32e7a)
 Call ID: 2bf52957-95ea-4447-8e39-f3ddfcf32e7a
  Args:
    relation: :hasMother
    source: :Victoria_Eugenie_of_Battenberg
    target: :Princess_Beatrice
  AddTriple (f51d57f2-438e-471e-b527-fedaf082177f)
 Call ID: f51d57f2-438e-471e-b527-fedaf082177f
  Args:
    target: :Henry_of_Battenberg
    source: :Victoria_Eugenie_of_Battenberg
    relation: :hasFather
  Finish (b8642719-e2d9-4226-b15f-e712f46cdf26)
 Call ID: b8642719-e2d9-4226-b15f-e712f46cdf26
  Args: