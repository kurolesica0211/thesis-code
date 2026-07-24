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
Queen Margrethe II


Prince Joachim of Denmark, Count of Monpezat, RE, SKmd (.mw-parser-output .IPA-label-small{font-size:85%}.mw-parser-output .references .IPA-label-small,.mw-parser-output .infobox .IPA-label-small,.mw-parser-output .navbox .IPA-label-small{font-size:100%}Danish pronunciation: ; Joachim Holger Waldemar Christian; born 7 June 1969) is a member of the Danish royal family.
The younger son of Queen Margrethe II, he is fifth in the line of succession to the Danish throne, following the four children of his elder brother King Frederik X.


Early life

Joachim was born on 7 June 1969 at Rigshospitalet, part of the Copenhagen University Hospital in Copenhagen.
He was christened Joachim Holger Waldemar Christian on 15 July 1969 in Aarhus Cathedral, the first member of the royal family to have been christened outside of Copenhagen.
His godparents were his maternal aunt, Princess Benedikte of Denmark; his paternal uncle, Jean Baptiste de Laborde de Monpezat; his mother's first cousin, Princess Christina of Sweden; and King Harald V (then Crown Prince of Norway).
Joachim attended school as a private pupil from 1974 until 1976 at Amalienborg Palace and then from 1976 until 1982 at Krebs' Skole in Copenhagen.
In 1986, Joachim graduated from Øregård Gymnasium.
Schackenborg

In 1993, Joachim took over the estate of Schackenborg Castle in the town of Møgeltønder, in Southern Jutland, having been granted the estate in the will of Count Hans Schack in 1978.
Joachim and his first wife, now the Countess of Frederiksborg, received 13 million DKK collected by the people of Denmark as a national gift, reserved for restoration of the estate.
Joachim remained at Schackenborg – from 2007 alongside his second wife – until 2014 when the estate was handed over to the Schackenborg Foundation, which consists of Joachim, Bitten and Mads Clausens foundation, Ole Kirks Foundation, and Ecco Holding.
Joachim, Marie and their children moved from the castle to Klampenborg, north of Copenhagen, but still holiday at the castle.
Military career

As junior officer

In 1987, Joachim enlisted as a recruit in the Queen's Life Regiment, where from he first entered the NCO School and where after the lieutenant school.
Between 1989 and 1990, he served as platoon commander in the 3rd tank squadron/1st Battalion (3/I/PLR) of the Prince's Life Regiment.
Between 1996 and 2004, he served as squadron commander of 3rd tank squadron/2nd Battalion (3/II/PLR) also in the Prince's Life Regiment.
In 2015, Joachim was appointed special advisor to the Chief of Defense in the Royal Danish Army.
During the summer of 2019, Joachim, Princess Marie and their two children moved to Paris, France, while the Prince had been admitted to the highest-ranking military educational program at École Militaire by invitation from the French Minister of Defense.
Joachim graduated on 26 June 2020, being the first Danish Officer to complete the two-part special education.
As general officer and Denmark's military attaché to France

Earlier in June 2020, Minister of Defence Trine Bramsen promoted Joachim to Brigadier General due to his new acquired educational merits at École Militaire.
He was subsequently named Military Attaché at the Royal Danish Embassy in Paris, France, by the Danish Ministry of Defense, a position he was expected to hold for at least three years while maintaining his patronages and royal engagements in Denmark when possible.
Joachim commenced his new position on 1 September 2020.
On 24 July 2020, while on holiday in Château de Cayx, Joachim was admitted to Toulouse University Hospital for surgery on a blood clot in his brain.
Denmark's military attaché to the United States

In March 2023, it was announced that Joachim, Marie and their two younger children would be moving to Washington, D.C. where he would be taking up the role of defence industry attaché (Defence Industrial Cooperation Attaché) at the Danish Embassy from September 2023.
Marriages and children

First marriage

On 18 November 1995, at Frederiksborg Palace Church in Hillerød, near Copenhagen, Joachim married Alexandra Christina Manley, a Hong Kong-born former sales and marketing deputy chief executive of English, Chinese, and Austrian ancestry.
Alexandra received the title of Countess of Frederiksborg, and was permitted to retain the courtesy title of princess pending remarriage.
She subsequently remarried and forfeited the royal title, but retained the title of countess.
She continues to live in Denmark.
Second marriage

On 3 October 2007, the Danish court announced that Joachim had become engaged to French native Marie Cavallier.
The wedding date marked the 73rd anniversary of the wedding of Joachim's grandparents, King Frederik IX and Queen Ingrid of Denmark.
The couple have two children, Count Henrik and Countess Athena.
None of Joachim's four children have been styled as Royal Highnesses but simply as Highnesses per the Danish court.
From 1 January 2023 all four of his children are known as His or Her Excellency Count/Countess of Monpezat.
Joachim expressed his sadness at his mother's decision to make that change.
Interests

Joachim enjoys historic motor sports car racing and has participated in the Copenhagen Historic Grand Prix multiple times.
In 2019, Joachim presented the documentary series Prins Joachim fortæller for Danmarks Radio.
In the six-part series that he also co-produced, Joachim investigates the ideas and events that shaped Denmark's history.
Titles, styles, honours and arms

Titles and styles

Military ranks

Honours

National

Orders and appointments

Medals and decorations

Foreign

He has been honoured with:


Additional information

The Dansk Rugby Union (DRU) website names Prince Joachim as the patron of the DRU.



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
  AssignClass (66d43d65-f24a-4f96-8ba4-d99457c47a69)
 Call ID: 66d43d65-f24a-4f96-8ba4-d99457c47a69
  Args:
    type: :Man
    source: :Joachim_of_Denmark
  AssignClass (e53114f8-0a09-4300-bfac-3c5b5e731112)
 Call ID: e53114f8-0a09-4300-bfac-3c5b5e731112
  Args:
    type: :Person
    source: :Joachim_of_Denmark
  AddLiteral (259c2abc-6599-499c-817e-830edbac64aa)
 Call ID: 259c2abc-6599-499c-817e-830edbac64aa
  Args:
    relation: :hasBirthYear
    literal_value: 1969
    source: :Joachim_of_Denmark
    literal_type: xsd:integer
  AssignClass (67103a2c-98a2-4188-ba1e-a1c6edbd14e6)
 Call ID: 67103a2c-98a2-4188-ba1e-a1c6edbd14e6
  Args:
    type: :Woman
    source: :Margrethe_II
  AssignClass (4f68a63e-52b7-49b9-a0cc-cf78efcbae0f)
 Call ID: 4f68a63e-52b7-49b9-a0cc-cf78efcbae0f
  Args:
    type: :Person
    source: :Margrethe_II
  AddTriple (28795426-cf14-42e2-8aab-294d76019e4c)
 Call ID: 28795426-cf14-42e2-8aab-294d76019e4c
  Args:
    source: :Margrethe_II
    relation: :isMotherOf
    target: :Joachim_of_Denmark
  AssignClass (978c7853-667d-4b83-9669-8f34476d5c68)
 Call ID: 978c7853-667d-4b83-9669-8f34476d5c68
  Args:
    type: :Man
    source: :Frederik_X
  AssignClass (6379e7fa-bdfb-4532-83bc-51c0869987c2)
 Call ID: 6379e7fa-bdfb-4532-83bc-51c0869987c2
  Args:
    type: :Person
    source: :Frederik_X
  AddTriple (408b2ab2-c649-4228-8980-9c351a36c086)
 Call ID: 408b2ab2-c649-4228-8980-9c351a36c086
  Args:
    relation: :isBrotherOf
    target: :Joachim_of_Denmark
    source: :Frederik_X
  AssignClass (6bf6dadf-754c-48e9-953f-7d696d1942f8)
 Call ID: 6bf6dadf-754c-48e9-953f-7d696d1942f8
  Args:
    type: :Woman
    source: :Alexandra_Christina_Manley
  AssignClass (5158ba44-8c27-4c96-b0b8-54b779f7551f)
 Call ID: 5158ba44-8c27-4c96-b0b8-54b779f7551f
  Args:
    type: :Person
    source: :Alexandra_Christina_Manley
  AddTriple (7a35568a-8e85-47f7-8f1f-c48a74bb0c01)
 Call ID: 7a35568a-8e85-47f7-8f1f-c48a74bb0c01
  Args:
    target: :Alexandra_Christina_Manley
    relation: :hasRelation
    source: :Joachim_of_Denmark
  AddLiteral (ee4f8da7-bdef-47fa-867a-0e1f412ed091)
 Call ID: ee4f8da7-bdef-47fa-867a-0e1f412ed091
  Args:
    literal_value: 1995
    relation: :hasMarriageYear
    source: :Joachim_of_Denmark
    literal_type: xsd:integer
  AssignClass (3cf63d50-6868-441b-be89-d85a0c792df1)
 Call ID: 3cf63d50-6868-441b-be89-d85a0c792df1
  Args:
    type: :Woman
    source: :Marie_Cavallier
  AssignClass (a9bcb1cb-97f6-45fa-9cf0-2c9eaedc59a4)
 Call ID: a9bcb1cb-97f6-45fa-9cf0-2c9eaedc59a4
  Args:
    type: :Person
    source: :Marie_Cavallier
  AddTriple (cb330c43-4fb3-47b9-aaba-845f2efd3594)
 Call ID: cb330c43-4fb3-47b9-aaba-845f2efd3594
  Args:
    source: :Joachim_of_Denmark
    target: :Marie_Cavallier
    relation: :hasRelation
  AddLiteral (e05cb419-b168-43cb-a94b-ab4f1ed6ff4a)
 Call ID: e05cb419-b168-43cb-a94b-ab4f1ed6ff4a
  Args:
    source: :Joachim_of_Denmark
    literal_value: 2007
    relation: :hasMarriageYear
    literal_type: xsd:integer
  AssignClass (c8c7f197-7438-4c0c-bb34-087cc6162744)
 Call ID: c8c7f197-7438-4c0c-bb34-087cc6162744
  Args:
    type: :Man
    source: :Henrik_of_Monpezat
  AssignClass (84b71676-8dfc-4c75-a584-d1377f4dc875)
 Call ID: 84b71676-8dfc-4c75-a584-d1377f4dc875
  Args:
    type: :Person
    source: :Henrik_of_Monpezat
  AddTriple (b806a1ea-ef9f-4b58-8f00-f22cce875d02)
 Call ID: b806a1ea-ef9f-4b58-8f00-f22cce875d02
  Args:
    target: :Joachim_of_Denmark
    relation: :isSonOf
    source: :Henrik_of_Monpezat
  AddTriple (6315f352-89ad-4d5b-8104-d6f330eb53a9)
 Call ID: 6315f352-89ad-4d5b-8104-d6f330eb53a9
  Args:
    source: :Henrik_of_Monpezat
    relation: :isSonOf
    target: :Marie_Cavallier
  AssignClass (9689a0b7-f383-48b4-9c1a-25498a8250be)
 Call ID: 9689a0b7-f383-48b4-9c1a-25498a8250be
  Args:
    type: :Woman
    source: :Athena_of_Monpezat
  AssignClass (757442ce-0bb3-4f40-b8ea-2b6023d75f76)
 Call ID: 757442ce-0bb3-4f40-b8ea-2b6023d75f76
  Args:
    type: :Person
    source: :Athena_of_Monpezat
  AddTriple (90c69922-732b-47de-af23-7f9002d9f5f5)
 Call ID: 90c69922-732b-47de-af23-7f9002d9f5f5
  Args:
    source: :Athena_of_Monpezat
    target: :Joachim_of_Denmark
    relation: :isDaughterOf
  AddTriple (0a05adfb-1729-456e-9dff-06620fa5849d)
 Call ID: 0a05adfb-1729-456e-9dff-06620fa5849d
  Args:
    target: :Marie_Cavallier
    relation: :isDaughterOf
    source: :Athena_of_Monpezat
  AssignClass (663f8f84-5175-4ce6-81a8-fd7563d05eb9)
 Call ID: 663f8f84-5175-4ce6-81a8-fd7563d05eb9
  Args:
    type: :Woman
    source: :Benedikte_of_Denmark
  AssignClass (c7f03fca-ccc6-48f3-b87a-f42d4cbcf196)
 Call ID: c7f03fca-ccc6-48f3-b87a-f42d4cbcf196
  Args:
    type: :Person
    source: :Benedikte_of_Denmark
  AddTriple (f7c2fa12-a930-4e71-8727-7b5054ba9fe9)
 Call ID: f7c2fa12-a930-4e71-8727-7b5054ba9fe9
  Args:
    source: :Benedikte_of_Denmark
    target: :Joachim_of_Denmark
    relation: :isAuntOf
  AssignClass (8b672823-f6f6-49b4-941f-62b248827a9c)
 Call ID: 8b672823-f6f6-49b4-941f-62b248827a9c
  Args:
    type: :Man
    source: :Jean_Baptiste_de_Laborde_de_Monpezat
  AssignClass (37391911-e15f-4c82-9403-9fe546f879a1)
 Call ID: 37391911-e15f-4c82-9403-9fe546f879a1
  Args:
    type: :Person
    source: :Jean_Baptiste_de_Laborde_de_Monpezat
  AddTriple (06e73d2a-0938-45c6-9d8d-fdb4176fd6b3)
 Call ID: 06e73d2a-0938-45c6-9d8d-fdb4176fd6b3
  Args:
    source: :Jean_Baptiste_de_Laborde_de_Monpezat
    relation: :isUncleOf
    target: :Joachim_of_Denmark
  AssignClass (e9062721-9997-4e67-a82e-de19d5bcec23)
 Call ID: e9062721-9997-4e67-a82e-de19d5bcec23
  Args:
    type: :Man
    source: :Frederik_IX
  AssignClass (5b1f1af0-04a8-4763-b953-6ba20c3e6fc9)
 Call ID: 5b1f1af0-04a8-4763-b953-6ba20c3e6fc9
  Args:
    type: :Person
    source: :Frederik_IX
  AssignClass (caff60d4-4e6b-4154-95e3-9ce51787417c)
 Call ID: caff60d4-4e6b-4154-95e3-9ce51787417c
  Args:
    type: :Woman
    source: :Ingrid_of_Denmark
  AssignClass (7f4deee0-3405-42b4-bb92-af8358d427ab)
 Call ID: 7f4deee0-3405-42b4-bb92-af8358d427ab
  Args:
    type: :Person
    source: :Ingrid_of_Denmark
  AddTriple (d6d1e7c8-f1d3-431e-a313-e95480f0b3f6)
 Call ID: d6d1e7c8-f1d3-431e-a313-e95480f0b3f6
  Args:
    source: :Frederik_IX
    target: :Margrethe_II
    relation: :isFatherOf
  AddTriple (d226c6bb-c337-4280-bd55-4f96beb8ca49)
 Call ID: d226c6bb-c337-4280-bd55-4f96beb8ca49
  Args:
    source: :Ingrid_of_Denmark
    target: :Margrethe_II
    relation: :isMotherOf
  Finish (a7401fb9-8dcc-40cc-bbb3-898591e43061)
 Call ID: a7401fb9-8dcc-40cc-bbb3-898591e43061
  Args: