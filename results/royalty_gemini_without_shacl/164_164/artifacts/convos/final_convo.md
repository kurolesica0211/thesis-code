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
Grand Duchess Kira Kirillovna of Russia (9 May 1909 – 8 September 1967) was the second daughter of Grand Duke Kirill Vladimirovich of Russia and Princess Victoria Melita of Saxe-Coburg and Gotha.
She married Prince Louis Ferdinand of Prussia, grandson of the last German Emperor Wilhelm II.
Early life

Grand Duchess Kira Kirilovna of Russia was born on 9 May 1909, at her parents' house on Avenue Henri Martin in Paris.
Named after her father, she was the second child of Grand Duke Kirill Vladimirovich of Russia, and his wife, Princess Victoria Melita of Saxe-Coburg and Gotha.
In addition, her mother had divorced her former husband, Ernest Louis, Grand Duke of Hesse, the brother of the Tsarina Alexandra Feodorovna.
In 1908, after the death of Grand Duke Alexei Alexandrovich and before Kira's birth, Nicholas II restored Kirill to his rank of captain in the Imperial Russian Navy and his position as aide de camp to the emperor.
He was given the title Grand Duke of Russia and from then on his wife was styled as Her Imperial Highness Grand Duchess Viktoria Feodorovna.
Kira and her elder sister, Maria, had a privileged childhood.
Kira's early years were spent in luxury at her father's palace at 13 Glinka Street in Saint Petersburg, where her parents entertained their guests lavishly.
During World War I, Kira's father served as the commander of a unit of the Naval Guards, while her mother oversaw a motorized ambulance.
At the outbreak of the Russian revolution, Kira's father marched to the Tauride Palace at the head of the Naval Guards before the establishment of the Russian Provisional Government.
In June, Kira's father obtained permission from the provisional government to move to Finland.
Kira, eight at the time, recalled that they rode on a public train.
The family waited in Finland, hoping that the White guard would defeat the Bolsheviks and they could return to Russia.
Kira, then age nine, amused herself by taking long walks hunting for mushrooms, and as a treat went to the cinema every Friday.
Grand Duke Kirill's family stayed in Finland until May 1920.
Family

The family eventually left Finland and headed first to Coburg and then to Saint-Briac, France.
Kira was born Princess Kira Kirillovna of Russia, but her father later gave her illegally the title "Grand Duchess" when he declared himself Guardian of the Throne in 1924.
Dowager Empress Maria Feodorovna openly mocked Kirill's pretension.
Blonde-haired, blue-eyed Kira, high-spirited and straightforward also had an even temper.
Kira also frequently visited her cousins at various royal courts or attended house parties in the United Kingdom.
Princess Kira had some difficulty finding a suitable husband.
She was interested in the hemophiliac Alfonso, Prince of Asturias, son of Alfonso XIII of Spain, but was disappointed when the prince showed more interest in one of the daughters of Prince Nicholas of Greece.
Later, she was fond of Prince Constantine "Teddy" Soutzo, a Romanian aristocrat.
Finally, Kira married Prince Louis Ferdinand of Prussia in 1938.
After World War II

Kira was called upon to testify in the case of Anna Anderson, the woman who claimed to be Grand Duchess Anastasia Nikolaevna of Russia.
Kira had met Anderson briefly in 1952 at the urging of her mother-in-law, Crown Princess Cecilie of Prussia, who believed Anderson's claim.
Kira was not convinced.
Kira had last seen Anastasia when she was a child of seven.
Kira's uncle, Grand Duke Andrei Vladimirovich of Russia had been convinced Anderson was Anastasia, but her father and mother were unconvinced by Anderson's claim.
In later years, Kira was disappointed when her eldest son, Friedrich Wilhelm, renounced his rights to the title and married a commoner.
She was in good spirits on a visit to her brother Grand Duke Vladimir of Russia at Saint-Briac in September 1967, where she ate well and dumped several spoonfuls of sugar into her coffee, commenting, "God forbid I should eat anything healthy!"



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
  AssignClass (654e509d-ca4f-44be-93e9-edaa304897b1)
 Call ID: 654e509d-ca4f-44be-93e9-edaa304897b1
  Args:
    source: Kira_Kirillovna_of_Russia
    type: :Woman
  AssignClass (1de193c4-e481-418c-a258-bb4c3948bc18)
 Call ID: 1de193c4-e481-418c-a258-bb4c3948bc18
  Args:
    source: Kira_Kirillovna_of_Russia
    type: :Person
  AddLiteral (0d34580e-cabb-45ee-959d-dba474732448)
 Call ID: 0d34580e-cabb-45ee-959d-dba474732448
  Args:
    literal_value: 1909
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Kira_Kirillovna_of_Russia
  AddLiteral (0461a148-a3a9-4206-9a2a-2a6609f7df2e)
 Call ID: 0461a148-a3a9-4206-9a2a-2a6609f7df2e
  Args:
    literal_value: 1967
    literal_type: xsd:integer
    source: Kira_Kirillovna_of_Russia
    relation: :hasDeathYear
  AssignClass (04325859-2ec3-4aa0-bba9-05ebf0573888)
 Call ID: 04325859-2ec3-4aa0-bba9-05ebf0573888
  Args:
    source: Kirill_Vladimirovich_of_Russia
    type: :Man
  AssignClass (c022c7f7-d64c-4e4a-bdfa-38b85d7a53be)
 Call ID: c022c7f7-d64c-4e4a-bdfa-38b85d7a53be
  Args:
    type: :Person
    source: Kirill_Vladimirovich_of_Russia
  AssignClass (9cb34e40-f437-424c-bc4c-307e4e83e872)
 Call ID: 9cb34e40-f437-424c-bc4c-307e4e83e872
  Args:
    type: :Woman
    source: Victoria_Melita_of_Saxe-Coburg_and_Gotha
  AssignClass (43d70243-16de-4a15-9425-b176ec9a7180)
 Call ID: 43d70243-16de-4a15-9425-b176ec9a7180
  Args:
    type: :Person
    source: Victoria_Melita_of_Saxe-Coburg_and_Gotha
  AddTriple (f6612fc9-e13c-407e-b509-40b9fb49ad9d)
 Call ID: f6612fc9-e13c-407e-b509-40b9fb49ad9d
  Args:
    relation: :hasFather
    target: Kirill_Vladimirovich_of_Russia
    source: Kira_Kirillovna_of_Russia
  AddTriple (dcdc65da-5019-4a19-8f9d-43998fea3af2)
 Call ID: dcdc65da-5019-4a19-8f9d-43998fea3af2
  Args:
    target: Victoria_Melita_of_Saxe-Coburg_and_Gotha
    source: Kira_Kirillovna_of_Russia
    relation: :hasMother
  AssignClass (1d9d48b7-1a81-4377-8330-f029af698bbb)
 Call ID: 1d9d48b7-1a81-4377-8330-f029af698bbb
  Args:
    source: Louis_Ferdinand_of_Prussia
    type: :Man
  AssignClass (e099d1c1-228c-4eac-a6b0-f606e323d337)
 Call ID: e099d1c1-228c-4eac-a6b0-f606e323d337
  Args:
    source: Louis_Ferdinand_of_Prussia
    type: :Person
  AddLiteral (a9216f0c-89ff-4890-82e5-e1d27300084d)
 Call ID: a9216f0c-89ff-4890-82e5-e1d27300084d
  Args:
    literal_type: xsd:integer
    literal_value: 1938
    relation: :hasMarriageYear
    source: Kira_Kirillovna_of_Russia
  AddTriple (2a3f651e-f5a2-428b-ad35-01ae1c6f96cf)
 Call ID: 2a3f651e-f5a2-428b-ad35-01ae1c6f96cf
  Args:
    relation: :hasRelation
    source: Kira_Kirillovna_of_Russia
    target: Louis_Ferdinand_of_Prussia
  AssignClass (a28153f0-37a0-49f9-aee9-32cc1e5004fc)
 Call ID: a28153f0-37a0-49f9-aee9-32cc1e5004fc
  Args:
    source: Maria_of_Russia
    type: :Woman
  AssignClass (6716d26f-f1c5-465b-8d48-d14861cb6318)
 Call ID: 6716d26f-f1c5-465b-8d48-d14861cb6318
  Args:
    type: :Person
    source: Maria_of_Russia
  AddTriple (cbd2deb2-34a7-4fa7-8fb1-4763b3ba9c76)
 Call ID: cbd2deb2-34a7-4fa7-8fb1-4763b3ba9c76
  Args:
    source: Kira_Kirillovna_of_Russia
    target: Maria_of_Russia
    relation: :hasSister
  AssignClass (f56f44a9-c1e5-4bd5-a73e-a53312f75b4d)
 Call ID: f56f44a9-c1e5-4bd5-a73e-a53312f75b4d
  Args:
    source: Ernest_Louis_of_Hesse
    type: :Man
  AssignClass (2fc18dca-3708-42e1-92d5-d757020da6e0)
 Call ID: 2fc18dca-3708-42e1-92d5-d757020da6e0
  Args:
    type: :Person
    source: Ernest_Louis_of_Hesse
  AddTriple (1c7e26bb-04ae-4761-8829-19a42a61a562)
 Call ID: 1c7e26bb-04ae-4761-8829-19a42a61a562
  Args:
    target: Ernest_Louis_of_Hesse
    source: Victoria_Melita_of_Saxe-Coburg_and_Gotha
    relation: :hasRelation
  AssignClass (18983a86-b3c4-425d-b12c-e533245b0de3)
 Call ID: 18983a86-b3c4-425d-b12c-e533245b0de3
  Args:
    type: :Woman
    source: Alexandra_Feodorovna_Tsarina
  AssignClass (34d757db-4a48-4796-8650-855cf32a3a8f)
 Call ID: 34d757db-4a48-4796-8650-855cf32a3a8f
  Args:
    type: :Person
    source: Alexandra_Feodorovna_Tsarina
  AddTriple (014df353-7022-4594-b7bd-aabe8f6b9842)
 Call ID: 014df353-7022-4594-b7bd-aabe8f6b9842
  Args:
    relation: :hasSister
    source: Alexandra_Feodorovna_Tsarina
    target: Ernest_Louis_of_Hesse
  AssignClass (5193228b-00a3-439a-9566-c5325bcaa141)
 Call ID: 5193228b-00a3-439a-9566-c5325bcaa141
  Args:
    type: :Man
    source: Friedrich_Wilhelm_of_Prussia
  AssignClass (a33d396b-2812-466a-a8cb-f4c35894126a)
 Call ID: a33d396b-2812-466a-a8cb-f4c35894126a
  Args:
    source: Friedrich_Wilhelm_of_Prussia
    type: :Person
  AddTriple (c4475ed7-5f97-49e8-b92a-dcae529c3b1a)
 Call ID: c4475ed7-5f97-49e8-b92a-dcae529c3b1a
  Args:
    target: Friedrich_Wilhelm_of_Prussia
    source: Kira_Kirillovna_of_Russia
    relation: :hasSon
  AssignClass (2fac3658-40c0-4269-a433-54b2c7ad1f6c)
 Call ID: 2fac3658-40c0-4269-a433-54b2c7ad1f6c
  Args:
    type: :Man
    source: Vladimir_of_Russia
  AssignClass (817dc4df-6976-4ae1-af83-f535c36d7735)
 Call ID: 817dc4df-6976-4ae1-af83-f535c36d7735
  Args:
    source: Vladimir_of_Russia
    type: :Person
  AddTriple (790a2dc7-a444-488b-a2f6-9132aa5ca1f4)
 Call ID: 790a2dc7-a444-488b-a2f6-9132aa5ca1f4
  Args:
    target: Vladimir_of_Russia
    source: Kira_Kirillovna_of_Russia
    relation: :hasBrother
  AssignClass (dc6a5a10-e1d0-4031-bc36-41ba21b030fa)
 Call ID: dc6a5a10-e1d0-4031-bc36-41ba21b030fa
  Args:
    source: Andrei_Vladimirovich_of_Russia
    type: :Man
  AssignClass (3ab627ca-04ab-432f-9e62-0434b89320ae)
 Call ID: 3ab627ca-04ab-432f-9e62-0434b89320ae
  Args:
    source: Andrei_Vladimirovich_of_Russia
    type: :Person
  AddTriple (a0a9f370-8e8d-4fc0-a5b3-9d16e7dd7e0b)
 Call ID: a0a9f370-8e8d-4fc0-a5b3-9d16e7dd7e0b
  Args:
    relation: :hasRelation
    source: Kira_Kirillovna_of_Russia
    target: Andrei_Vladimirovich_of_Russia
  Finish (c54eb3fb-db22-47d5-abf2-43538452da86)
 Call ID: c54eb3fb-db22-47d5-abf2-43538452da86
  Args: