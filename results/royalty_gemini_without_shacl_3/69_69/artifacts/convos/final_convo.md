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
  AssignClass (4990fae7-a9a4-4d68-8859-f6e765877b61)
 Call ID: 4990fae7-a9a4-4d68-8859-f6e765877b61
  Args:
    type: :Person
    source: :Queen_Margrethe_II
  AssignClass (2a47ca38-9801-4f16-9891-6750f47a8e75)
 Call ID: 2a47ca38-9801-4f16-9891-6750f47a8e75
  Args:
    source: :Queen_Margrethe_II
    type: :Woman
  AssignClass (55a3609f-2e21-42d3-aa6a-a11cf5636d44)
 Call ID: 55a3609f-2e21-42d3-aa6a-a11cf5636d44
  Args:
    source: :Prince_Joachim
    type: :Person
  AssignClass (1a18363b-adb9-4073-9d2d-558b6243b002)
 Call ID: 1a18363b-adb9-4073-9d2d-558b6243b002
  Args:
    type: :Man
    source: :Prince_Joachim
  AddLiteral (0d70982a-c501-4415-84e6-0474171f2556)
 Call ID: 0d70982a-c501-4415-84e6-0474171f2556
  Args:
    literal_type: xsd:integer
    literal_value: 1969
    source: :Prince_Joachim
    relation: :hasBirthYear
  AddTriple (e0823c64-4142-42a3-9d02-730ac47f6cba)
 Call ID: e0823c64-4142-42a3-9d02-730ac47f6cba
  Args:
    relation: :isChildOf
    target: :Queen_Margrethe_II
    source: :Prince_Joachim
  AssignClass (60f364c1-d422-4f5e-af8c-5eed71de0886)
 Call ID: 60f364c1-d422-4f5e-af8c-5eed71de0886
  Args:
    source: :King_Frederik_X
    type: :Person
  AssignClass (5a2b958e-1a77-4b94-a1c5-bad296036067)
 Call ID: 5a2b958e-1a77-4b94-a1c5-bad296036067
  Args:
    type: :Man
    source: :King_Frederik_X
  AddTriple (a3a85062-c5f0-4eec-820a-9726e3e51528)
 Call ID: a3a85062-c5f0-4eec-820a-9726e3e51528
  Args:
    relation: :isBrotherOf
    source: :Prince_Joachim
    target: :King_Frederik_X
  AssignClass (471d44bb-9a23-41f7-98ed-703e5fc50677)
 Call ID: 471d44bb-9a23-41f7-98ed-703e5fc50677
  Args:
    source: :Princess_Benedikte
    type: :Person
  AssignClass (de0e818b-a5ba-494e-ae3f-0b3df522c627)
 Call ID: de0e818b-a5ba-494e-ae3f-0b3df522c627
  Args:
    source: :Princess_Benedikte
    type: :Woman
  AddTriple (b96f014d-eee9-4f93-8e3e-a0d2f274219a)
 Call ID: b96f014d-eee9-4f93-8e3e-a0d2f274219a
  Args:
    target: :Princess_Benedikte
    source: :Queen_Margrethe_II
    relation: :hasSister
  AssignClass (07ef4877-a57c-4e28-adcb-aabae3e798ee)
 Call ID: 07ef4877-a57c-4e28-adcb-aabae3e798ee
  Args:
    type: :Person
    source: :Jean_Baptiste_de_Laborde_de_Monpezat
  AssignClass (2346dc87-6660-4afa-a1cf-23d75f3ab76d)
 Call ID: 2346dc87-6660-4afa-a1cf-23d75f3ab76d
  Args:
    source: :Jean_Baptiste_de_Laborde_de_Monpezat
    type: :Man
  AssignClass (88b375dd-28c1-4975-83f2-fae0e671d963)
 Call ID: 88b375dd-28c1-4975-83f2-fae0e671d963
  Args:
    type: :Person
    source: :Princess_Christina_of_Sweden
  AssignClass (bb25f96b-61eb-403c-b0b1-0d2744c4a77a)
 Call ID: bb25f96b-61eb-403c-b0b1-0d2744c4a77a
  Args:
    type: :Woman
    source: :Princess_Christina_of_Sweden
  AssignClass (e81aa3fa-e67c-4fc1-a89a-64bdab65e635)
 Call ID: e81aa3fa-e67c-4fc1-a89a-64bdab65e635
  Args:
    type: :Person
    source: :King_Harald_V
  AssignClass (5663b36b-a6e1-4775-8375-ce7668be1929)
 Call ID: 5663b36b-a6e1-4775-8375-ce7668be1929
  Args:
    type: :Man
    source: :King_Harald_V
  AssignClass (3f07a269-f76b-4ec2-bc0f-a9f1f822a8ae)
 Call ID: 3f07a269-f76b-4ec2-bc0f-a9f1f822a8ae
  Args:
    type: :Person
    source: :Alexandra_Christina_Manley
  AssignClass (497005f1-608a-4697-a69f-3f80bb347464)
 Call ID: 497005f1-608a-4697-a69f-3f80bb347464
  Args:
    source: :Alexandra_Christina_Manley
    type: :Woman
  AddTriple (6d4fe5a8-ed73-41b9-ad23-9501500262bd)
 Call ID: 6d4fe5a8-ed73-41b9-ad23-9501500262bd
  Args:
    relation: :hasRelation
    target: :Alexandra_Christina_Manley
    source: :Prince_Joachim
  AddLiteral (4ea461c7-a1c8-4b05-9a05-c8214ba7321b)
 Call ID: 4ea461c7-a1c8-4b05-9a05-c8214ba7321b
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    source: :Prince_Joachim
    literal_value: 1995
  AssignClass (c734e861-d618-418a-b5b0-dd8218fe364e)
 Call ID: c734e861-d618-418a-b5b0-dd8218fe364e
  Args:
    source: :Marie_Cavallier
    type: :Person
  AssignClass (4c059f15-f480-4998-ba77-7e7c48907177)
 Call ID: 4c059f15-f480-4998-ba77-7e7c48907177
  Args:
    type: :Woman
    source: :Marie_Cavallier
  AddTriple (86d480a9-47bf-4954-9ebe-58dbcd548e75)
 Call ID: 86d480a9-47bf-4954-9ebe-58dbcd548e75
  Args:
    target: :Marie_Cavallier
    source: :Prince_Joachim
    relation: :hasRelation
  AddLiteral (bef89034-9a72-4007-848e-d61a0220411c)
 Call ID: bef89034-9a72-4007-848e-d61a0220411c
  Args:
    literal_value: 2007
    source: :Prince_Joachim
    relation: :hasMarriageYear
    literal_type: xsd:integer
  AssignClass (d3982b5c-bc01-47a4-be9b-3a0da3005513)
 Call ID: d3982b5c-bc01-47a4-be9b-3a0da3005513
  Args:
    type: :Person
    source: :Count_Henrik
  AssignClass (d7ec9fed-e65a-40b7-a817-fa67e30c539c)
 Call ID: d7ec9fed-e65a-40b7-a817-fa67e30c539c
  Args:
    source: :Count_Henrik
    type: :Man
  AddTriple (98b9bd3c-559d-44a3-b5d9-31346e98b358)
 Call ID: 98b9bd3c-559d-44a3-b5d9-31346e98b358
  Args:
    relation: :isChildOf
    source: :Count_Henrik
    target: :Prince_Joachim
  AddTriple (6ec4aa42-5ba0-420e-bcf6-50ad24a0f04f)
 Call ID: 6ec4aa42-5ba0-420e-bcf6-50ad24a0f04f
  Args:
    source: :Count_Henrik
    target: :Marie_Cavallier
    relation: :isChildOf
  AssignClass (da89aa16-2c67-4729-a7c1-70dcce0d3847)
 Call ID: da89aa16-2c67-4729-a7c1-70dcce0d3847
  Args:
    type: :Person
    source: :Countess_Athena
  AssignClass (902d5ced-12be-49f0-b178-daa3bf2ec29c)
 Call ID: 902d5ced-12be-49f0-b178-daa3bf2ec29c
  Args:
    type: :Woman
    source: :Countess_Athena
  AddTriple (5d75af6f-5e64-4c2c-a392-b8fadb944f89)
 Call ID: 5d75af6f-5e64-4c2c-a392-b8fadb944f89
  Args:
    relation: :isChildOf
    source: :Countess_Athena
    target: :Prince_Joachim
  AddTriple (61253edc-0bd5-4882-9461-920b5d87106b)
 Call ID: 61253edc-0bd5-4882-9461-920b5d87106b
  Args:
    relation: :isChildOf
    target: :Marie_Cavallier
    source: :Countess_Athena
  AssignClass (caabbab7-0199-45ee-a6d8-e6801d40365d)
 Call ID: caabbab7-0199-45ee-a6d8-e6801d40365d
  Args:
    source: :King_Frederik_IX
    type: :Person
  AssignClass (9d18b163-b4c2-43b1-8a90-7918447fb65f)
 Call ID: 9d18b163-b4c2-43b1-8a90-7918447fb65f
  Args:
    type: :Man
    source: :King_Frederik_IX
  AssignClass (a080ef23-d4f3-4368-990b-be84e551c1a2)
 Call ID: a080ef23-d4f3-4368-990b-be84e551c1a2
  Args:
    source: :Queen_Ingrid
    type: :Person
  AssignClass (5db63a38-b7fa-4a7b-a112-fac5a3891742)
 Call ID: 5db63a38-b7fa-4a7b-a112-fac5a3891742
  Args:
    type: :Woman
    source: :Queen_Ingrid
  Finish (944470d4-81cb-4766-9d93-16dd56a02117)
 Call ID: 944470d4-81cb-4766-9d93-16dd56a02117
  Args: