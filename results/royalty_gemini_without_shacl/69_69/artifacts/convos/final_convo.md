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
  AssignClass (4938a5d7-10c6-462d-ad9b-42a1d4fc29f2)
 Call ID: 4938a5d7-10c6-462d-ad9b-42a1d4fc29f2
  Args:
    type: :Person
    source: :Margrethe_II
  AssignClass (d1a5883a-da62-46ff-ad61-3fbdb47d3252)
 Call ID: d1a5883a-da62-46ff-ad61-3fbdb47d3252
  Args:
    source: :Margrethe_II
    type: :Woman
  AssignClass (ca70bb13-58c0-48dd-a4bb-b12ce54eac0b)
 Call ID: ca70bb13-58c0-48dd-a4bb-b12ce54eac0b
  Args:
    type: :Person
    source: :Joachim_of_Denmark
  AssignClass (d0f94a24-7aea-4e24-9745-5679a2ce7e29)
 Call ID: d0f94a24-7aea-4e24-9745-5679a2ce7e29
  Args:
    type: :Man
    source: :Joachim_of_Denmark
  AddLiteral (97034593-7aed-46ab-8d7a-c7c926ef6620)
 Call ID: 97034593-7aed-46ab-8d7a-c7c926ef6620
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1969
    source: :Joachim_of_Denmark
  AddTriple (8ccbb960-be79-4298-b3cf-674d8c8414d5)
 Call ID: 8ccbb960-be79-4298-b3cf-674d8c8414d5
  Args:
    target: :Margrethe_II
    source: :Joachim_of_Denmark
    relation: :isChildOf
  AssignClass (ca9e9c75-fc39-49f4-9aad-af9c9adb9791)
 Call ID: ca9e9c75-fc39-49f4-9aad-af9c9adb9791
  Args:
    source: :Frederik_X
    type: :Person
  AssignClass (c617f7aa-4018-426d-9497-c5822e67917f)
 Call ID: c617f7aa-4018-426d-9497-c5822e67917f
  Args:
    type: :Man
    source: :Frederik_X
  AddTriple (44293c8c-f8cf-4338-bc11-0db97b1ae803)
 Call ID: 44293c8c-f8cf-4338-bc11-0db97b1ae803
  Args:
    relation: :isSiblingOf
    source: :Joachim_of_Denmark
    target: :Frederik_X
  AssignClass (6adbff00-0c25-4455-a713-83c538be1989)
 Call ID: 6adbff00-0c25-4455-a713-83c538be1989
  Args:
    type: :Person
    source: :Benedikte_of_Denmark
  AssignClass (6d2f5cd7-324c-48f9-8dbb-cfc31ab8328d)
 Call ID: 6d2f5cd7-324c-48f9-8dbb-cfc31ab8328d
  Args:
    source: :Benedikte_of_Denmark
    type: :Woman
  AddTriple (1bef943e-a4a2-4332-bfe0-9d959a7d78c9)
 Call ID: 1bef943e-a4a2-4332-bfe0-9d959a7d78c9
  Args:
    source: :Benedikte_of_Denmark
    relation: :isSisterOf
    target: :Margrethe_II
  AssignClass (7789fcb1-11d0-4f9d-8ca3-3a3710a31456)
 Call ID: 7789fcb1-11d0-4f9d-8ca3-3a3710a31456
  Args:
    source: :Jean_Baptiste_de_Laborde_de_Monpezat
    type: :Person
  AssignClass (6f65e3d7-ce65-46d8-a629-083600ab6c5c)
 Call ID: 6f65e3d7-ce65-46d8-a629-083600ab6c5c
  Args:
    type: :Man
    source: :Jean_Baptiste_de_Laborde_de_Monpezat
  AssignClass (07b77672-91e9-467e-aa57-90f6902c1b7b)
 Call ID: 07b77672-91e9-467e-aa57-90f6902c1b7b
  Args:
    source: :Christina_of_Sweden
    type: :Person
  AssignClass (2b4b2c97-d815-4ef6-82b1-8b2b68cc82b7)
 Call ID: 2b4b2c97-d815-4ef6-82b1-8b2b68cc82b7
  Args:
    type: :Woman
    source: :Christina_of_Sweden
  AssignClass (d53d0483-7af4-4156-8fe1-4ac88d8dab0b)
 Call ID: d53d0483-7af4-4156-8fe1-4ac88d8dab0b
  Args:
    type: :Person
    source: :Harald_V
  AssignClass (69ee9883-9b0a-424a-872c-7b6f50e4b5c8)
 Call ID: 69ee9883-9b0a-424a-872c-7b6f50e4b5c8
  Args:
    type: :Man
    source: :Harald_V
  AssignClass (cbda5de9-3a50-421f-8cb3-69046a641138)
 Call ID: cbda5de9-3a50-421f-8cb3-69046a641138
  Args:
    source: :Alexandra_Christina_Manley
    type: :Person
  AssignClass (7fbae6aa-4247-46ce-b62f-2f1718594e9d)
 Call ID: 7fbae6aa-4247-46ce-b62f-2f1718594e9d
  Args:
    source: :Alexandra_Christina_Manley
    type: :Woman
  AddLiteral (966cfee5-dd87-459c-a766-ccadbe64f0ea)
 Call ID: 966cfee5-dd87-459c-a766-ccadbe64f0ea
  Args:
    literal_value: 1995
    source: :Joachim_of_Denmark
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AddTriple (5e81b34b-7770-4fa4-be3c-1f603b99d566)
 Call ID: 5e81b34b-7770-4fa4-be3c-1f603b99d566
  Args:
    source: :Joachim_of_Denmark
    relation: :hasRelation
    target: :Alexandra_Christina_Manley
  AssignClass (32d6270b-df76-4af1-84d5-9756ffe8fe4b)
 Call ID: 32d6270b-df76-4af1-84d5-9756ffe8fe4b
  Args:
    type: :Person
    source: :Marie_Cavallier
  AssignClass (6cf341bf-46be-4c48-86d5-521f477f2b2f)
 Call ID: 6cf341bf-46be-4c48-86d5-521f477f2b2f
  Args:
    type: :Woman
    source: :Marie_Cavallier
  AddLiteral (f73273ba-ca87-4fb2-81e8-563e6bca76c7)
 Call ID: f73273ba-ca87-4fb2-81e8-563e6bca76c7
  Args:
    literal_value: 2007
    source: :Joachim_of_Denmark
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AddTriple (e7671eaf-8e8c-4d03-8bbf-9db253a8eae7)
 Call ID: e7671eaf-8e8c-4d03-8bbf-9db253a8eae7
  Args:
    source: :Joachim_of_Denmark
    relation: :hasRelation
    target: :Marie_Cavallier
  AssignClass (2e3600f9-cef1-463e-833f-6722560507d0)
 Call ID: 2e3600f9-cef1-463e-833f-6722560507d0
  Args:
    source: :Henrik_of_Monpezat
    type: :Person
  AssignClass (1408aaa4-2fad-4167-931f-92b7c31e927d)
 Call ID: 1408aaa4-2fad-4167-931f-92b7c31e927d
  Args:
    source: :Henrik_of_Monpezat
    type: :Man
  AssignClass (8f41936a-8cb9-4efa-9bd9-8a48c8aece70)
 Call ID: 8f41936a-8cb9-4efa-9bd9-8a48c8aece70
  Args:
    type: :Person
    source: :Athena_of_Monpezat
  AssignClass (8bf10db5-ab5f-4264-955e-82f1cde7d2f0)
 Call ID: 8bf10db5-ab5f-4264-955e-82f1cde7d2f0
  Args:
    type: :Woman
    source: :Athena_of_Monpezat
  AddTriple (868876d2-682c-4f85-a007-269244efd300)
 Call ID: 868876d2-682c-4f85-a007-269244efd300
  Args:
    relation: :isChildOf
    source: :Henrik_of_Monpezat
    target: :Joachim_of_Denmark
  AddTriple (aa22c2f4-090f-4bf5-93cd-aecac092df5a)
 Call ID: aa22c2f4-090f-4bf5-93cd-aecac092df5a
  Args:
    target: :Marie_Cavallier
    source: :Henrik_of_Monpezat
    relation: :isChildOf
  AddTriple (e99711d9-4804-4e7c-abdc-e40d940c63fd)
 Call ID: e99711d9-4804-4e7c-abdc-e40d940c63fd
  Args:
    target: :Joachim_of_Denmark
    source: :Athena_of_Monpezat
    relation: :isChildOf
  AddTriple (e45066c5-e182-4835-bdb0-ce922f882b2c)
 Call ID: e45066c5-e182-4835-bdb0-ce922f882b2c
  Args:
    source: :Athena_of_Monpezat
    relation: :isChildOf
    target: :Marie_Cavallier
  AssignClass (c34b1fc4-9f0a-43d6-af9c-7e2642432f51)
 Call ID: c34b1fc4-9f0a-43d6-af9c-7e2642432f51
  Args:
    type: :Person
    source: :Frederik_IX
  AssignClass (96c153bf-b39b-486e-9453-2ded2d3bf6c9)
 Call ID: 96c153bf-b39b-486e-9453-2ded2d3bf6c9
  Args:
    source: :Frederik_IX
    type: :Man
  AssignClass (9ff69d10-f130-4b4d-8c5a-ad672a4348f2)
 Call ID: 9ff69d10-f130-4b4d-8c5a-ad672a4348f2
  Args:
    type: :Person
    source: :Ingrid_of_Denmark
  AssignClass (d7b34625-e20a-4584-a4b2-78e6b25cf2dc)
 Call ID: d7b34625-e20a-4584-a4b2-78e6b25cf2dc
  Args:
    source: :Ingrid_of_Denmark
    type: :Woman
  Finish (a89f66e3-cdbb-4d7c-844f-223966451830)
 Call ID: a89f66e3-cdbb-4d7c-844f-223966451830
  Args: