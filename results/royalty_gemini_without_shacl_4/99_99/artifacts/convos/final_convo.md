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
  AssignClass (7689cbbc-bb9a-444a-8c8b-3698f5edbb80)
 Call ID: 7689cbbc-bb9a-444a-8c8b-3698f5edbb80
  Args:
    source: :Feodora_of_Saxe-Meiningen
    type: :Woman
  AssignClass (c758fac1-fbf4-4c4a-8d4a-6dc4898a8ccf)
 Call ID: c758fac1-fbf4-4c4a-8d4a-6dc4898a8ccf
  Args:
    source: :Feodora_of_Saxe-Meiningen
    type: :Person
  AddLiteral (0115d55d-9b2c-4ded-a5e3-038443fac37b)
 Call ID: 0115d55d-9b2c-4ded-a5e3-038443fac37b
  Args:
    literal_value: 1879
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: :Feodora_of_Saxe-Meiningen
  AddLiteral (cc7408bc-f4b3-4ea4-85cf-b92ae9c66ebd)
 Call ID: cc7408bc-f4b3-4ea4-85cf-b92ae9c66ebd
  Args:
    literal_value: 1945
    source: :Feodora_of_Saxe-Meiningen
    relation: :hasDeathYear
    literal_type: xsd:integer
  AssignClass (7b90b53d-8c92-4900-8ca5-75933aef4321)
 Call ID: 7b90b53d-8c92-4900-8ca5-75933aef4321
  Args:
    source: :Bernhard_III_Duke_of_Saxe-Meiningen
    type: :Man
  AssignClass (cc393f00-972d-44f8-87a6-2e345e98f467)
 Call ID: cc393f00-972d-44f8-87a6-2e345e98f467
  Args:
    type: :Person
    source: :Bernhard_III_Duke_of_Saxe-Meiningen
  AssignClass (bb889889-359f-4cdd-8f30-557dcd17647e)
 Call ID: bb889889-359f-4cdd-8f30-557dcd17647e
  Args:
    source: :Charlotte_of_Prussia
    type: :Woman
  AssignClass (1ea14046-a115-4ebf-85c2-d03b49bb317c)
 Call ID: 1ea14046-a115-4ebf-85c2-d03b49bb317c
  Args:
    type: :Person
    source: :Charlotte_of_Prussia
  AddTriple (b1db5257-5507-4306-981d-9ee7efb7948c)
 Call ID: b1db5257-5507-4306-981d-9ee7efb7948c
  Args:
    target: :Bernhard_III_Duke_of_Saxe-Meiningen
    relation: :hasFather
    source: :Feodora_of_Saxe-Meiningen
  AddTriple (a051ca98-d62f-4ddf-b74a-124cdc664c1e)
 Call ID: a051ca98-d62f-4ddf-b74a-124cdc664c1e
  Args:
    source: :Feodora_of_Saxe-Meiningen
    relation: :hasMother
    target: :Charlotte_of_Prussia
  AssignClass (c6206789-9e54-489e-a640-2082bb109c9e)
 Call ID: c6206789-9e54-489e-a640-2082bb109c9e
  Args:
    source: :Friedrich_III_of_Germany
    type: :Man
  AssignClass (c9e0eaa1-678c-4eb5-a526-694502e5ed08)
 Call ID: c9e0eaa1-678c-4eb5-a526-694502e5ed08
  Args:
    type: :Person
    source: :Friedrich_III_of_Germany
  AssignClass (793212b7-4107-4b0c-a24c-33cb658a63d2)
 Call ID: 793212b7-4107-4b0c-a24c-33cb658a63d2
  Args:
    source: :Empress_Victoria_of_Germany
    type: :Woman
  AssignClass (17575b6e-568e-4ea5-a315-7209a02db3fc)
 Call ID: 17575b6e-568e-4ea5-a315-7209a02db3fc
  Args:
    source: :Empress_Victoria_of_Germany
    type: :Person
  AddTriple (6dcb2bb3-ab5d-4551-b0ff-be5192325fe9)
 Call ID: 6dcb2bb3-ab5d-4551-b0ff-be5192325fe9
  Args:
    target: :Friedrich_III_of_Germany
    relation: :hasFather
    source: :Charlotte_of_Prussia
  AddTriple (17d8d4f4-f407-4d8a-88b4-2229d9253882)
 Call ID: 17d8d4f4-f407-4d8a-88b4-2229d9253882
  Args:
    target: :Empress_Victoria_of_Germany
    relation: :hasMother
    source: :Charlotte_of_Prussia
  AssignClass (70038d88-2d45-4ead-89b6-825f88938ef3)
 Call ID: 70038d88-2d45-4ead-89b6-825f88938ef3
  Args:
    type: :Man
    source: :William_I_German_Emperor
  AssignClass (da474f52-2625-4007-8d33-02072926558a)
 Call ID: da474f52-2625-4007-8d33-02072926558a
  Args:
    type: :Person
    source: :William_I_German_Emperor
  AssignClass (62cbec69-1280-47c1-b0a9-064767411357)
 Call ID: 62cbec69-1280-47c1-b0a9-064767411357
  Args:
    source: :Queen_Victoria_of_the_United_Kingdom
    type: :Woman
  AssignClass (38952aba-f9aa-461c-b35b-214aceb64b29)
 Call ID: 38952aba-f9aa-461c-b35b-214aceb64b29
  Args:
    source: :Queen_Victoria_of_the_United_Kingdom
    type: :Person
  AssignClass (ea1786ce-810d-47af-92f9-80db5d253e1f)
 Call ID: ea1786ce-810d-47af-92f9-80db5d253e1f
  Args:
    type: :Man
    source: :Heinrich_XXX_Reuss_of_Köstritz
  AssignClass (6b467c85-d28b-418b-b474-2084ad8c9985)
 Call ID: 6b467c85-d28b-418b-b474-2084ad8c9985
  Args:
    type: :Person
    source: :Heinrich_XXX_Reuss_of_Köstritz
  AddTriple (b577a7f5-3298-4a91-99ca-9e45643b0b06)
 Call ID: b577a7f5-3298-4a91-99ca-9e45643b0b06
  Args:
    source: :Feodora_of_Saxe-Meiningen
    target: :Heinrich_XXX_Reuss_of_Köstritz
    relation: :hasRelation
  AddLiteral (e2a9894f-2e7d-4693-871f-7e3cda45af7b)
 Call ID: e2a9894f-2e7d-4693-871f-7e3cda45af7b
  Args:
    literal_value: 1898
    source: :Feodora_of_Saxe-Meiningen
    relation: :hasMarriageYear
    literal_type: xsd:integer
  AddLiteral (ca4eb470-f083-4528-9607-0b580d65165e)
 Call ID: ca4eb470-f083-4528-9607-0b580d65165e
  Args:
    literal_value: 1864
    source: :Heinrich_XXX_Reuss_of_Köstritz
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (288acfd3-1c4b-402f-ac60-d3cf0a4343f1)
 Call ID: 288acfd3-1c4b-402f-ac60-d3cf0a4343f1
  Args:
    literal_value: 1939
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: :Heinrich_XXX_Reuss_of_Köstritz
  AssignClass (bdd871f6-0c84-4c65-8244-dfcaa39ea01f)
 Call ID: bdd871f6-0c84-4c65-8244-dfcaa39ea01f
  Args:
    source: :Alice_of_Battenberg
    type: :Woman
  AssignClass (314441ae-8c01-4be2-9846-8c6165db0be0)
 Call ID: 314441ae-8c01-4be2-9846-8c6165db0be0
  Args:
    source: :Alice_of_Battenberg
    type: :Person
  Finish (077e8128-5bb7-4221-afa6-528a5798050c)
 Call ID: 077e8128-5bb7-4221-afa6-528a5798050c
  Args: