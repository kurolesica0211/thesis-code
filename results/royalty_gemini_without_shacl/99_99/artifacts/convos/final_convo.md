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
Princess Feodora of Saxe-Meiningen (Feodora Viktoria Auguste Marie Marianne; 12 May 1879 – 26 August 1945) was born at Potsdam, the only child of Bernhard III, Duke of Saxe-Meiningen and Duchess Charlotte (the eldest daughter of Emperor Friedrich III of Germany and Empress Victoria).
Feodora was the first great-grandchild of both William I, German Emperor and Queen Victoria of the United Kingdom.
Early life

Princess Feodora was born on 12 May 1879 as the only child of Bernhard, Hereditary Prince of Saxe-Meiningen, and his wife Princess Charlotte of Prussia, herself the eldest daughter of German Crown Prince Frederick William and Crown Princess Victoria.
The new baby was the first grandchild of the Crown Prince and Princess, and through her mother was also the first great-grandchild of the British Queen Victoria.
Charlotte, who loved to socialize, had hated being pregnant, believing that it limited her activities.
Preferring to return to enjoying social life in Berlin, she declared after Feodora's birth that she would have no further children, dismaying her mother, Crown Princess Victoria.
It was unusual to be an only child in European royal families, and Feodora likely endured a lonely childhood.
Charlotte loved to travel, and often left her daughter with Vicky at Friedrichshof, whom she viewed as the source of a convenient nursery.
The Crown Princess, for her part, loved having the chance to spend time with her eldest granddaughter.
Describing Feodora on one visit, she wrote that "she is really a good little child, & far easier to manage than her Mama".
Victoria, who became German empress in 1888, perceived a deficit in Feodora's upbringing and gradually became concerned about the girl's physical appearance and mental development, describing the thirteen-year-old as possessing "sharp pinched features" and an unusually short stature.
Feodora also cared little for her studies, preferring instead to discuss fashion.
With Charlotte for an example, what else can one expect...
She hardly knows what home life is!"


Queen Victoria was fond of her eldest great-grandchild.
In June 1887, the young Feodora and her parents attended the queen's  Golden Jubilee in London.
While her parents stayed at Buckingham Palace, Feodora stayed with her young cousin Princess Alice of Battenberg at the home of the Dowager Duchess of Buccleuch at Whitehall, allowing the girls to watch the royal procession as it made its way to Westminster Abbey.
Queen Victoria described her as "sweet little Feo, who is so good and I think grown quite pretty.
"


Marriage

As Feodora grew older, her marriage began to be a consideration.
The widowed, exiled Prince Peter Karađorđević, thirty-six years older than Feodora, proposed himself as a suitor, though this was likely a bid to gain support for succeeding to the Serbian throne.
Charlotte declared that "for such a throne Feodora is far too good".
In the mid-1890s, Princess Feodora was considered as a potential bride for King Alexander I of Serbia.
As a niece of German Emperor Wilhelm II, she was regarded as a suitable match, and in early 1896 the emperor gave his preliminary approval, advising the Serbian court to initiate formal negotiations with Feodora’s parents.
Despite this opportunity, by the end of 1897 the Serbian court had explored other prospective brides from Greece, Montenegro, and Russia without success, leaving the marriage negotiations with Feodora unresolved.
Her mother's maternal first cousin Alfred, Hereditary Prince of Saxe-Coburg and Gotha, the only son of Charlotte's friend (and Feodora's maternal grandaunt)
the Duchess of Saxe-Coburg and Gotha, was also considered.
Several months after returning from Queen Victoria's Diamond Jubilee celebrations in June 1897, Feodora became engaged to Prince Heinrich XXX Reuss of Köstritz (1864-1939), with the betrothal announced in early October.
Princess Feodora was the only great-grandchild of Queen Victoria and only grandchild of German Empress Victoria to be married in their lifetimes; she married in 1898 and both the Queen and the German Empress died in 1901.
Feodora's grandmother Empress Victoria was surprised at the choice of groom, particularly his lack of position, but observed that the bride at least seemed happy.
Of the fifteen-year age gap, Victoria commented, "I am very glad he is older than she is, and if he is wise and steady and firm, he may do her a vast deal of good, and it may turn out very well, but she has had a strange example in her mother, and is a strange little creature."
The historian John Van der Kiste writes that Feodora was "evidently besotted" with her new husband, and she likely also sought marriage as an escape from her "irksome home life".
Once returned from their honeymoon, Henry spent much of his time on duty with his regiment, while Feodora joined a reading group and attended the opera and theatre in Berlin.
Feodora also often accompanied her husband during his military assignments, travelling throughout Germany.
Last years

Feodora suffered most of her adult life from ill health, describing it as "the old story" of her life.
Like her mother and maternal grandmother, and maternal great grandmother Feodora's illnesses included dizziness, insomnia, nausea, various pains, paralysis, constipation, and diarrhoea.
Feodora visited Windsor Castle in 1900, which would be the last time she saw her great-grandmother before Queen Victoria's death the following year.
Henry attended her funeral, but ill health kept Feodora from attending.
Feodora blamed malaria for her condition, though Charlotte told family members that Henry had given his wife a venereal disease, an allegation Feodora furiously denied.
Charlotte asked her daughter to get tested by Charlotte's personal physician; when Feodora refused, it confirmed to Charlotte that her beliefs were correct.
In reaction, Feodora refused to enter her mother's house and complained to family members of Charlotte's "incredible" actions.
Feodora found that the region's mild climate had a positive impact on her health.
By this stage, relations between him and his wife had deteriorated; Henry believed Feodora enjoyed complaining about being sick and seeing doctors.
After the war concluded with Germany's defeat, Feodora's father's rule over the Duchy of Saxe-Meiningen was ended.
Her post-war life is mostly unknown, and records of her subsequent medical history have mainly been lost.
In describing Feodora's life, the historian John Van der Kiste writes that "the princess who had so desperately wanted children of her own had instead continued to battle with constant physical ailments, insomnia and severe depression, and endured many years of ill-health similar to that of her mother".
Medical analysis

In the 1990s, the historian John Röhl and his colleagues Martin Warren and David Hunt found Feodora's grave in Poland, exhuming the body for DNA analysis in the belief that it would reveal signs of the genetic disease porphyria however, it was proved inconclusive.



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
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

:hasDeathYear a owl:AnnotationProperty .

:hasMarriageYear a owl:AnnotationProperty .

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

:hasChild a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:inverseOf :isChildOf .

:isAncestorOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation .

:isSiblingOf a owl:ObjectProperty,
        owl:SymmetricProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isBloodrelationOf ;
    owl:propertyChainAxiom ( :hasParent :isParentOf ) .

:isSisterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf .

:hasParent a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Person ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:equivalentProperty :isChildOf ;
    owl:inverseOf :isParentOf .

:Sex a owl:Class ;
    rdfs:subClassOf :DomainEntity ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Female :Male ) ] .

:isChildOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:propertyDisjointWith :isSisterOf .

:Man a owl:Class ;
    owl:disjointWith :Sex,
        :Woman ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Male ] ) ] .

:Woman a owl:Class ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Female ] ) ] .

:isParentOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:propertyDisjointWith :isSisterOf .

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



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (bc54f474-5c83-4ed5-ae47-3e55526159e2)
 Call ID: bc54f474-5c83-4ed5-ae47-3e55526159e2
  Args:
    type: :Person
    source: :Feodora_of_Saxe-Meiningen
  AssignClass (e936eb0e-bb40-4886-b2d0-8dbfe38d774d)
 Call ID: e936eb0e-bb40-4886-b2d0-8dbfe38d774d
  Args:
    type: :Woman
    source: :Feodora_of_Saxe-Meiningen
  AddLiteral (7ed5348d-3f0a-4002-bf53-5264be108028)
 Call ID: 7ed5348d-3f0a-4002-bf53-5264be108028
  Args:
    relation: :alsoKnownAs
    source: :Feodora_of_Saxe-Meiningen
    literal_value: Feodora Viktoria Auguste Marie Marianne
    literal_type: xsd:string
  AddLiteral (eac962a3-2855-4571-8c1c-1d160c1b9a2f)
 Call ID: eac962a3-2855-4571-8c1c-1d160c1b9a2f
  Args:
    relation: :hasBirthYear
    source: :Feodora_of_Saxe-Meiningen
    literal_value: 1879
    literal_type: xsd:integer
  AddLiteral (eccc6d58-6c37-4033-bdb3-9929a9f1c39d)
 Call ID: eccc6d58-6c37-4033-bdb3-9929a9f1c39d
  Args:
    literal_type: xsd:integer
    literal_value: 1945
    source: :Feodora_of_Saxe-Meiningen
    relation: :hasDeathYear
  AssignClass (0df54551-325b-48b8-a634-afece9443bb7)
 Call ID: 0df54551-325b-48b8-a634-afece9443bb7
  Args:
    type: :Person
    source: :Bernhard_III_of_Saxe-Meiningen
  AssignClass (ac8f8bd9-fbd3-4075-84e9-b448fd699f40)
 Call ID: ac8f8bd9-fbd3-4075-84e9-b448fd699f40
  Args:
    type: :Man
    source: :Bernhard_III_of_Saxe-Meiningen
  AssignClass (2cc54687-07f4-4f38-a71d-b4d62e4628e2)
 Call ID: 2cc54687-07f4-4f38-a71d-b4d62e4628e2
  Args:
    type: :Person
    source: :Charlotte_of_Prussia
  AssignClass (9fb01021-a2ef-406b-a6ed-1f52bf0f29b9)
 Call ID: 9fb01021-a2ef-406b-a6ed-1f52bf0f29b9
  Args:
    type: :Woman
    source: :Charlotte_of_Prussia
  AddTriple (fbb9614e-663d-4341-9d8e-4e6d138336f1)
 Call ID: fbb9614e-663d-4341-9d8e-4e6d138336f1
  Args:
    target: :Bernhard_III_of_Saxe-Meiningen
    source: :Feodora_of_Saxe-Meiningen
    relation: :hasFather
  AddTriple (be0369e6-1803-4af6-8a24-ca49bfbbd870)
 Call ID: be0369e6-1803-4af6-8a24-ca49bfbbd870
  Args:
    source: :Feodora_of_Saxe-Meiningen
    target: :Charlotte_of_Prussia
    relation: :hasMother
  AssignClass (a62b9f37-9b70-46e5-82d7-9071c016a780)
 Call ID: a62b9f37-9b70-46e5-82d7-9071c016a780
  Args:
    type: :Person
    source: :Friedrich_III_of_Germany
  AssignClass (1152e235-9747-41b7-9efe-ba6a33527aea)
 Call ID: 1152e235-9747-41b7-9efe-ba6a33527aea
  Args:
    type: :Man
    source: :Friedrich_III_of_Germany
  AssignClass (8e914b8d-27a7-4303-a9ed-808864bfe5fb)
 Call ID: 8e914b8d-27a7-4303-a9ed-808864bfe5fb
  Args:
    type: :Person
    source: :Empress_Victoria
  AssignClass (f3f5a289-916e-4ac7-a10f-4229a733c169)
 Call ID: f3f5a289-916e-4ac7-a10f-4229a733c169
  Args:
    type: :Woman
    source: :Empress_Victoria
  AddTriple (22f815f4-b2c1-4151-8940-b69a143c24f6)
 Call ID: 22f815f4-b2c1-4151-8940-b69a143c24f6
  Args:
    source: :Charlotte_of_Prussia
    target: :Friedrich_III_of_Germany
    relation: :hasFather
  AddTriple (2fa8967f-727c-4b6e-bc9c-7a275e5f3512)
 Call ID: 2fa8967f-727c-4b6e-bc9c-7a275e5f3512
  Args:
    relation: :hasMother
    source: :Charlotte_of_Prussia
    target: :Empress_Victoria
  AssignClass (3b9004fd-44ce-4864-8d04-3a0f3eea3bba)
 Call ID: 3b9004fd-44ce-4864-8d04-3a0f3eea3bba
  Args:
    type: :Person
    source: :William_I_German_Emperor
  AssignClass (b4785f7f-fdb0-491e-b8c2-84c28a49bd7b)
 Call ID: b4785f7f-fdb0-491e-b8c2-84c28a49bd7b
  Args:
    type: :Man
    source: :William_I_German_Emperor
  AssignClass (64f31cf1-6d0b-49c7-bed8-8f11c0b1216a)
 Call ID: 64f31cf1-6d0b-49c7-bed8-8f11c0b1216a
  Args:
    type: :Person
    source: :Queen_Victoria_of_the_United_Kingdom
  AssignClass (c645e88e-1fcf-42b5-ac15-d2378b84b233)
 Call ID: c645e88e-1fcf-42b5-ac15-d2378b84b233
  Args:
    type: :Woman
    source: :Queen_Victoria_of_the_United_Kingdom
  AssignClass (e091b050-6711-49dd-95bc-6aee9ad8321e)
 Call ID: e091b050-6711-49dd-95bc-6aee9ad8321e
  Args:
    type: :Person
    source: :Heinrich_XXX_Reuss_of_Köstritz
  AssignClass (f0171037-bb54-4048-a541-f5bcfdecab8b)
 Call ID: f0171037-bb54-4048-a541-f5bcfdecab8b
  Args:
    type: :Man
    source: :Heinrich_XXX_Reuss_of_Köstritz
  AddLiteral (41b61ca3-257c-4a96-bb22-88ac1def98e6)
 Call ID: 41b61ca3-257c-4a96-bb22-88ac1def98e6
  Args:
    relation: :hasMarriageYear
    source: :Feodora_of_Saxe-Meiningen
    literal_value: 1898
    literal_type: xsd:integer
  AddTriple (e47a277d-cc56-4571-9dcc-02b7ddf98390)
 Call ID: e47a277d-cc56-4571-9dcc-02b7ddf98390
  Args:
    relation: :hasRelation
    source: :Feodora_of_Saxe-Meiningen
    target: :Heinrich_XXX_Reuss_of_Köstritz
  Finish (30814086-a158-49e2-8a77-7a8d1d8707ea)
 Call ID: 30814086-a158-49e2-8a77-7a8d1d8707ea
  Args: