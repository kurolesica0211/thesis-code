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
  AssignClass (00067fc6-46d6-4950-b4e3-d7f7ddae2336)
 Call ID: 00067fc6-46d6-4950-b4e3-d7f7ddae2336
  Args:
    type: :Woman
    source: Feodora_of_Saxe-Meiningen
  AssignClass (db016f27-de5a-42dd-9637-dff656dcc728)
 Call ID: db016f27-de5a-42dd-9637-dff656dcc728
  Args:
    type: :Person
    source: Feodora_of_Saxe-Meiningen
  AddLiteral (4a0b8626-2621-4351-946b-4305f943436e)
 Call ID: 4a0b8626-2621-4351-946b-4305f943436e
  Args:
    literal_type: xsd:integer
    source: Feodora_of_Saxe-Meiningen
    literal_value: 1879
    relation: :hasBirthYear
  AddLiteral (b7f1792a-1c53-41cf-a77a-3390648d3f59)
 Call ID: b7f1792a-1c53-41cf-a77a-3390648d3f59
  Args:
    literal_value: 1945
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: Feodora_of_Saxe-Meiningen
  AssignClass (a507c176-94e0-487e-aca3-72387e222f8e)
 Call ID: a507c176-94e0-487e-aca3-72387e222f8e
  Args:
    type: :Man
    source: Bernhard_III_of_Saxe-Meiningen
  AssignClass (67d18ef6-4f4a-43a0-94bc-4a44f0664b76)
 Call ID: 67d18ef6-4f4a-43a0-94bc-4a44f0664b76
  Args:
    type: :Person
    source: Bernhard_III_of_Saxe-Meiningen
  AssignClass (81b1107e-443e-46cb-9a25-d3ba58a20cc6)
 Call ID: 81b1107e-443e-46cb-9a25-d3ba58a20cc6
  Args:
    type: :Woman
    source: Charlotte_of_Prussia
  AssignClass (e1269373-7b0b-4591-94da-69fdfc81a1b3)
 Call ID: e1269373-7b0b-4591-94da-69fdfc81a1b3
  Args:
    type: :Person
    source: Charlotte_of_Prussia
  AddTriple (97529fe3-e442-44c7-b3e1-e1af3a4cbde1)
 Call ID: 97529fe3-e442-44c7-b3e1-e1af3a4cbde1
  Args:
    target: Bernhard_III_of_Saxe-Meiningen
    relation: :hasFather
    source: Feodora_of_Saxe-Meiningen
  AddTriple (5d818af9-a1fb-4a52-a610-61e6a1590ab7)
 Call ID: 5d818af9-a1fb-4a52-a610-61e6a1590ab7
  Args:
    relation: :hasMother
    target: Charlotte_of_Prussia
    source: Feodora_of_Saxe-Meiningen
  AssignClass (6c431903-a869-4526-a833-fe139b0dab8f)
 Call ID: 6c431903-a869-4526-a833-fe139b0dab8f
  Args:
    type: :Man
    source: Friedrich_III_of_Germany
  AssignClass (ae73cad4-66ab-47be-b88a-07820eb11363)
 Call ID: ae73cad4-66ab-47be-b88a-07820eb11363
  Args:
    type: :Person
    source: Friedrich_III_of_Germany
  AssignClass (91f14e2c-8760-49c8-9107-9b1b9d1aabd8)
 Call ID: 91f14e2c-8760-49c8-9107-9b1b9d1aabd8
  Args:
    type: :Woman
    source: Empress_Victoria
  AssignClass (13d1635f-4454-4cae-8ea2-c06f805a26ee)
 Call ID: 13d1635f-4454-4cae-8ea2-c06f805a26ee
  Args:
    type: :Person
    source: Empress_Victoria
  AddTriple (d858c06c-a688-4d80-946c-b59e1a959afc)
 Call ID: d858c06c-a688-4d80-946c-b59e1a959afc
  Args:
    relation: :hasFather
    target: Friedrich_III_of_Germany
    source: Charlotte_of_Prussia
  AddTriple (6a5d77a2-4021-412f-bed1-505257e702f8)
 Call ID: 6a5d77a2-4021-412f-bed1-505257e702f8
  Args:
    source: Charlotte_of_Prussia
    target: Empress_Victoria
    relation: :hasMother
  AssignClass (4d40d8d8-9348-467b-9183-955598585cc7)
 Call ID: 4d40d8d8-9348-467b-9183-955598585cc7
  Args:
    type: :Man
    source: William_I_German_Emperor
  AssignClass (d5ca316f-3b24-4f40-8f5a-f6049dd49d16)
 Call ID: d5ca316f-3b24-4f40-8f5a-f6049dd49d16
  Args:
    type: :Person
    source: William_I_German_Emperor
  AssignClass (a65017d9-6d33-4bc2-a01a-553f9114fe88)
 Call ID: a65017d9-6d33-4bc2-a01a-553f9114fe88
  Args:
    type: :Woman
    source: Queen_Victoria_of_the_United_Kingdom
  AssignClass (a656d455-4ecc-423e-8e14-ec0413679730)
 Call ID: a656d455-4ecc-423e-8e14-ec0413679730
  Args:
    type: :Person
    source: Queen_Victoria_of_the_United_Kingdom
  AssignClass (f5fac4bc-f421-4b32-9a9c-427c9ad02897)
 Call ID: f5fac4bc-f421-4b32-9a9c-427c9ad02897
  Args:
    type: :Man
    source: Heinrich_XXX_Reuss_of_Köstritz
  AssignClass (216357ee-9b36-4292-ad12-66c6e933eefb)
 Call ID: 216357ee-9b36-4292-ad12-66c6e933eefb
  Args:
    type: :Person
    source: Heinrich_XXX_Reuss_of_Köstritz
  AddLiteral (078581ab-2166-42f4-b16b-1cfaa64754c3)
 Call ID: 078581ab-2166-42f4-b16b-1cfaa64754c3
  Args:
    literal_type: xsd:integer
    source: Feodora_of_Saxe-Meiningen
    literal_value: 1898
    relation: :hasMarriageYear
  AddTriple (30298dbc-2ccd-4acf-9e34-faa100e2b35a)
 Call ID: 30298dbc-2ccd-4acf-9e34-faa100e2b35a
  Args:
    source: Feodora_of_Saxe-Meiningen
    relation: :hasRelation
    target: Heinrich_XXX_Reuss_of_Köstritz
  Finish (fd47adbe-3be4-443f-a340-5db32de84a8b)
 Call ID: fd47adbe-3be4-443f-a340-5db32de84a8b
  Args: