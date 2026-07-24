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
  AssignClass (26487a74-6373-4ab3-8509-9d65a3ebddd5)
 Call ID: 26487a74-6373-4ab3-8509-9d65a3ebddd5
  Args:
    source: Kira_Kirillovna_of_Russia
    type: :Person
  AssignClass (ae6549dc-6ee8-466d-bb3e-dd80dd25fbc9)
 Call ID: ae6549dc-6ee8-466d-bb3e-dd80dd25fbc9
  Args:
    type: :Woman
    source: Kira_Kirillovna_of_Russia
  AddLiteral (d94027df-0ac2-4f8d-86a3-99a49198f2dc)
 Call ID: d94027df-0ac2-4f8d-86a3-99a49198f2dc
  Args:
    literal_type: xsd:integer
    literal_value: 1909
    source: Kira_Kirillovna_of_Russia
    relation: :hasBirthYear
  AddLiteral (a567d09d-5ded-443a-b507-736c7362f18a)
 Call ID: a567d09d-5ded-443a-b507-736c7362f18a
  Args:
    relation: :hasDeathYear
    source: Kira_Kirillovna_of_Russia
    literal_value: 1967
    literal_type: xsd:integer
  AssignClass (86beee69-9779-4cda-8028-786e4687da93)
 Call ID: 86beee69-9779-4cda-8028-786e4687da93
  Args:
    type: :Person
    source: Kirill_Vladimirovich_of_Russia
  AssignClass (7d1450f5-9461-498d-ae16-526fde73cd61)
 Call ID: 7d1450f5-9461-498d-ae16-526fde73cd61
  Args:
    source: Kirill_Vladimirovich_of_Russia
    type: :Man
  AddTriple (1d83e9ea-139c-4b30-96ec-dad2e6d83fa8)
 Call ID: 1d83e9ea-139c-4b30-96ec-dad2e6d83fa8
  Args:
    relation: :hasFather
    source: Kira_Kirillovna_of_Russia
    target: Kirill_Vladimirovich_of_Russia
  AssignClass (7b3376ba-a99a-4126-b208-2013ea9bb991)
 Call ID: 7b3376ba-a99a-4126-b208-2013ea9bb991
  Args:
    source: Victoria_Melita_of_Saxe-Coburg_and_Gotha
    type: :Person
  AssignClass (5fe44b7e-d0ca-4490-bc00-78f3cbbfbbcb)
 Call ID: 5fe44b7e-d0ca-4490-bc00-78f3cbbfbbcb
  Args:
    source: Victoria_Melita_of_Saxe-Coburg_and_Gotha
    type: :Woman
  AddTriple (e313636c-28a5-4a91-91d3-6c0cb6c52729)
 Call ID: e313636c-28a5-4a91-91d3-6c0cb6c52729
  Args:
    relation: :hasMother
    source: Kira_Kirillovna_of_Russia
    target: Victoria_Melita_of_Saxe-Coburg_and_Gotha
  AssignClass (209b4279-c922-4117-9aa7-5fd20b1363f1)
 Call ID: 209b4279-c922-4117-9aa7-5fd20b1363f1
  Args:
    type: :Person
    source: Louis_Ferdinand_of_Prussia
  AssignClass (f3c4687c-f85f-4c09-b82d-77c32ec9f827)
 Call ID: f3c4687c-f85f-4c09-b82d-77c32ec9f827
  Args:
    type: :Man
    source: Louis_Ferdinand_of_Prussia
  AddTriple (d05725d5-48e4-464f-a52d-02ea66a5315b)
 Call ID: d05725d5-48e4-464f-a52d-02ea66a5315b
  Args:
    target: Louis_Ferdinand_of_Prussia
    source: Kira_Kirillovna_of_Russia
    relation: :hasRelation
  AddLiteral (d4737d2a-59d2-4a1f-aacf-1ce64ab02f4e)
 Call ID: d4737d2a-59d2-4a1f-aacf-1ce64ab02f4e
  Args:
    relation: :hasMarriageYear
    source: Kira_Kirillovna_of_Russia
    literal_type: xsd:integer
    literal_value: 1938
  AssignClass (e97d237b-043f-426e-89d5-593402518b64)
 Call ID: e97d237b-043f-426e-89d5-593402518b64
  Args:
    type: :Person
    source: Wilhelm_II
  AssignClass (0f7c5e6d-9d0d-454f-bad8-52f74e239a67)
 Call ID: 0f7c5e6d-9d0d-454f-bad8-52f74e239a67
  Args:
    type: :Man
    source: Wilhelm_II
  AddTriple (3372968c-b1d7-41d8-ac0b-b4b99ebf4f35)
 Call ID: 3372968c-b1d7-41d8-ac0b-b4b99ebf4f35
  Args:
    target: Louis_Ferdinand_of_Prussia
    source: Wilhelm_II
    relation: :isAncestorOf
  AssignClass (81b696e5-90d7-4bb3-993a-b5abc867521f)
 Call ID: 81b696e5-90d7-4bb3-993a-b5abc867521f
  Args:
    type: :Person
    source: Maria_of_Russia
  AssignClass (e9d8cdec-82ab-410d-af69-de330906f88f)
 Call ID: e9d8cdec-82ab-410d-af69-de330906f88f
  Args:
    type: :Woman
    source: Maria_of_Russia
  AddTriple (307eaacc-c9a8-4f8e-9a40-924135e604d6)
 Call ID: 307eaacc-c9a8-4f8e-9a40-924135e604d6
  Args:
    source: Maria_of_Russia
    relation: :isSisterOf
    target: Kira_Kirillovna_of_Russia
  AssignClass (7049d801-2d1c-43a3-97dc-7cb1c363e270)
 Call ID: 7049d801-2d1c-43a3-97dc-7cb1c363e270
  Args:
    type: :Person
    source: Ernest_Louis_of_Hesse
  AssignClass (dedc4794-e72d-442c-9f98-3d6b6b7b9544)
 Call ID: dedc4794-e72d-442c-9f98-3d6b6b7b9544
  Args:
    source: Ernest_Louis_of_Hesse
    type: :Man
  AddTriple (f8126457-0470-4628-ba3e-a1710eed5dbf)
 Call ID: f8126457-0470-4628-ba3e-a1710eed5dbf
  Args:
    source: Ernest_Louis_of_Hesse
    relation: :hasRelation
    target: Victoria_Melita_of_Saxe-Coburg_and_Gotha
  AssignClass (85760435-e095-4745-a8b8-2c46819f5827)
 Call ID: 85760435-e095-4745-a8b8-2c46819f5827
  Args:
    type: :Person
    source: Alexandra_Feodorovna
  AssignClass (c7634d00-9610-4fda-a1d5-e61471881009)
 Call ID: c7634d00-9610-4fda-a1d5-e61471881009
  Args:
    source: Alexandra_Feodorovna
    type: :Woman
  AddTriple (045c6e73-8116-441d-a7f0-d32da0f23367)
 Call ID: 045c6e73-8116-441d-a7f0-d32da0f23367
  Args:
    source: Alexandra_Feodorovna
    relation: :isSisterOf
    target: Ernest_Louis_of_Hesse
  AssignClass (412b7b16-35ad-4bd3-aa31-94e0764c2e7c)
 Call ID: 412b7b16-35ad-4bd3-aa31-94e0764c2e7c
  Args:
    source: Friedrich_Wilhelm_of_Prussia
    type: :Person
  AssignClass (e15b637d-5051-4b31-afd1-0d94301881b1)
 Call ID: e15b637d-5051-4b31-afd1-0d94301881b1
  Args:
    type: :Man
    source: Friedrich_Wilhelm_of_Prussia
  AddTriple (d3d9843c-762d-46d7-beaa-1412a4afd718)
 Call ID: d3d9843c-762d-46d7-beaa-1412a4afd718
  Args:
    relation: :hasSon
    source: Kira_Kirillovna_of_Russia
    target: Friedrich_Wilhelm_of_Prussia
  AssignClass (e3b5660a-9d53-45a7-bbfa-68bc0680037b)
 Call ID: e3b5660a-9d53-45a7-bbfa-68bc0680037b
  Args:
    source: Vladimir_of_Russia
    type: :Person
  AssignClass (acd8093e-3478-40a2-b824-479feb9a0296)
 Call ID: acd8093e-3478-40a2-b824-479feb9a0296
  Args:
    source: Vladimir_of_Russia
    type: :Man
  AddTriple (31448ea4-8b91-420c-8536-540b7cedd5a6)
 Call ID: 31448ea4-8b91-420c-8536-540b7cedd5a6
  Args:
    target: Kira_Kirillovna_of_Russia
    relation: :isBrotherOf
    source: Vladimir_of_Russia
  AssignClass (58f2c5cb-26fb-4f8b-aacd-2232b2ce8ed1)
 Call ID: 58f2c5cb-26fb-4f8b-aacd-2232b2ce8ed1
  Args:
    source: Cecilie_of_Prussia
    type: :Person
  AssignClass (681fcae5-b9bd-47b5-b757-c41663268a36)
 Call ID: 681fcae5-b9bd-47b5-b757-c41663268a36
  Args:
    source: Cecilie_of_Prussia
    type: :Woman
  AddTriple (4585b435-09ba-4eca-b90f-cca417223317)
 Call ID: 4585b435-09ba-4eca-b90f-cca417223317
  Args:
    relation: :hasMother
    source: Louis_Ferdinand_of_Prussia
    target: Cecilie_of_Prussia
  AssignClass (ee4e826e-66a6-4c1d-8c2d-4143a84bf294)
 Call ID: ee4e826e-66a6-4c1d-8c2d-4143a84bf294
  Args:
    source: Andrei_Vladimirovich_of_Russia
    type: :Person
  AssignClass (07105f64-afee-4869-81c8-ca05f27f82af)
 Call ID: 07105f64-afee-4869-81c8-ca05f27f82af
  Args:
    source: Andrei_Vladimirovich_of_Russia
    type: :Man
  AddTriple (68c83340-7bd2-4bcc-a1d6-a685c69f239e)
 Call ID: 68c83340-7bd2-4bcc-a1d6-a685c69f239e
  Args:
    target: Vladimir_of_Russia
    relation: :hasFather
    source: Andrei_Vladimirovich_of_Russia
  Finish (7d6539b6-c62e-4997-ab72-3095455867ff)
 Call ID: 7d6539b6-c62e-4997-ab72-3095455867ff
  Args: