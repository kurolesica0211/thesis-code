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


Princess Isabella of Denmark, Countess of Monpezat, RE (Isabella Henrietta Ingrid Margrethe; born 21 April 2007) is a member of the Danish royal family.
She is the second child and elder daughter of King Frederik X and Queen Mary.
She is the fourth grandchild and oldest granddaughter of Queen Margrethe II and Prince Henrik.
She was the first girl born into the Danish royal family since the birth of her great-aunt, Queen Anne-Marie of Greece, in 1946.
Isabella is second in the line of succession to the Danish throne, after her older brother, Crown Prince Christian.
Early life and education

Isabella was born on 21 April 2007 at 4:02 pm CET at Rigshospitalet, the Copenhagen University Hospital, in Copenhagen, to then Crown Prince Frederik and Crown Princess Mary.
Incidentally, Isabella was the first princess whose birth was marked with 21 shots, as the number of shots in the cannon salute had previously been different depending on the sex of the newborn, as 21 shots were fired for a boy and 17 shots for a girl.
But before Prince Christian was born in October 2005, the palace decided that 21 shots should be fired, regardless of the child's sex.
Her christening took place on 1 July 2007 at the Royal Chapel of Fredensborg Palace and was performed by the Bishop of Copenhagen Erik Norman Svendsen.
She was baptised at the royal baptismal font which has been used for the baptism of royal children in Denmark since 1671, and wore the royal christening gown which was made for her great-great-grandfather, King Christian X, in 1870.
At the christening, her name, per Danish royal tradition, was revealed to be Isabella Henrietta Ingrid Margrethe, after the Danish queen consort and ancestress Isabella of Austria, the princess's maternal grandmother, paternal great-grandmother, and paternal grandmother respectively.
Her godparents were her father's first cousin, Princess Alexia of Greece and Denmark; Queen Mathilde of Belgium (then Duchess of Brabant), Nadine Johnston, Christian Buchwald, Peter Heering and Marie Louise Skeel.
Isabella received the Lutheran rite of confirmation in the same chapel on 30 April 2022, which was presided over by Henrik Wigh-Poulsen, the Danish royal Chaplain-in-Ordinary.
With the passing of the 2009 Danish Act of Succession referendum, Isabella became the first princess in Danish history to not get bypassed by a younger brother when Prince Vincent was born in 2011.
On 13 August 2013, Isabella started school at Tranegårdsskolen in Gentofte, the same public school as her older brother.
In January 2020, Isabella and her three siblings initiated a 12-week school stay at Lemania-Verbier International School in Verbier, Switzerland.
The stay was eventually cut short and the siblings returned home in March due to the intensification of the COVID-19 situation in Denmark.
In March 2022, it was announced that Isabella would continue her education at Herlufsholm School starting in August 2022.
However, on 26 June 2022, her parents announced in a statement that Isabella would not start Herlufsholm after all due to revelations of recurring problems of bullying, violence and sexual abuse at the school, and in September 2022, she started 9th form at Ingrid Jespersens Gymnasieskole in Copenhagen instead.
In August 2023, Isabella started upper secondary school at Øregård Gymnasium – the same school her father, Frederik, and uncle, Joachim, previously attended.
In March 2026, it was announced that Isabella will undertake conscription with the Guard Hussar Regiment in the Royal Danish Army starting August 2026.
Previously, Queen Margrethe II performed voluntary service with the Women's Flying Corps, a branch of the Danish Home Guard, between 1958 and 1970, and Queen Mary has also trained with the Home Guard, but neither have undergone formal training with the armed forces.
Public life

Isabella undertook her first official engagement, the baptism of a ferry – the M/F Prinsesse Isabella operating between Jutland and Samsø – named in her honour, on 6 June 2015.
During the reception, Isabella made her first ever public speech, thanking the city and the participants for a "very unique" birthday celebration.
On 15 April, the Danish court and the Royal Danish Theatre hosted a birthday performance for Isabella at the theatre's Old Stage featuring performances from the field of ballet, theatre, music and opera.
Youths between the age of 17 and 24 from across the kingdom were eligible to apply for tickets to the performance which was also attended by her parents and three siblings; her grandmother, Queen Margrethe II; her cousins, Count Nikolai and Count Felix of Monpezat; her great-aunts, Princess Benedikte of Denmark and Queen Anne-Marie of Greece; as well as the Prince and Princess of Sayn-Wittgenstein-Berleburg.


Titles, styles, and honours

Isabella was originally styled "Her Royal Highness Princess Isabella of Denmark".
Since 29 April 2008, she has been styled 
"Her Royal Highness Princess Isabella of Denmark, Countess of Monpezat".



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
  AssignClass (d74746cd-42ac-4f5f-9041-df23d73c4519)
 Call ID: d74746cd-42ac-4f5f-9041-df23d73c4519
  Args:
    type: :Person
    source: :Isabella_of_Denmark
  AssignClass (6b431519-226d-460f-ac35-a75450267387)
 Call ID: 6b431519-226d-460f-ac35-a75450267387
  Args:
    type: :Woman
    source: :Isabella_of_Denmark
  AssignClass (ad1e11f3-63d9-46c2-b512-ef1a486acf45)
 Call ID: ad1e11f3-63d9-46c2-b512-ef1a486acf45
  Args:
    type: :Person
    source: :Frederik_X
  AssignClass (02eda3f6-8da2-4e6a-a917-20ccd8864711)
 Call ID: 02eda3f6-8da2-4e6a-a917-20ccd8864711
  Args:
    type: :Man
    source: :Frederik_X
  AssignClass (e1dd93a7-e78a-42f1-a87a-6edafe4e1ac1)
 Call ID: e1dd93a7-e78a-42f1-a87a-6edafe4e1ac1
  Args:
    type: :Ancestor
    source: :Frederik_X
  AssignClass (515565a3-27f0-472a-a855-71089d7aadd9)
 Call ID: 515565a3-27f0-472a-a855-71089d7aadd9
  Args:
    type: :Person
    source: :Mary_of_Denmark
  AssignClass (a89e379b-0388-4a27-a8af-005753c58596)
 Call ID: a89e379b-0388-4a27-a8af-005753c58596
  Args:
    type: :Woman
    source: :Mary_of_Denmark
  AssignClass (be678191-4d1b-493d-8023-4a52e08f5ec1)
 Call ID: be678191-4d1b-493d-8023-4a52e08f5ec1
  Args:
    type: :Ancestor
    source: :Mary_of_Denmark
  AssignClass (842f59d6-404a-4cbb-a2b1-dd46bb82f08b)
 Call ID: 842f59d6-404a-4cbb-a2b1-dd46bb82f08b
  Args:
    type: :Person
    source: :Margrethe_II
  AssignClass (1cbfba08-0d0e-4357-b19a-f775bef69943)
 Call ID: 1cbfba08-0d0e-4357-b19a-f775bef69943
  Args:
    type: :Woman
    source: :Margrethe_II
  AssignClass (0a5c7daf-e080-4246-8e76-dd40bcb718df)
 Call ID: 0a5c7daf-e080-4246-8e76-dd40bcb718df
  Args:
    type: :Ancestor
    source: :Margrethe_II
  AssignClass (cf0e6dd2-2d68-493f-965b-db0f87fbc00a)
 Call ID: cf0e6dd2-2d68-493f-965b-db0f87fbc00a
  Args:
    type: :Person
    source: :Henrik_of_Denmark
  AssignClass (aa5e940a-4601-4cfa-bb26-891d401460ca)
 Call ID: aa5e940a-4601-4cfa-bb26-891d401460ca
  Args:
    type: :Man
    source: :Henrik_of_Denmark
  AssignClass (02766173-5c9d-4e39-9f50-08250f7881b6)
 Call ID: 02766173-5c9d-4e39-9f50-08250f7881b6
  Args:
    type: :Ancestor
    source: :Henrik_of_Denmark
  AssignClass (bedb5e3b-e7fd-4102-b33f-77df3573c6ef)
 Call ID: bedb5e3b-e7fd-4102-b33f-77df3573c6ef
  Args:
    type: :Person
    source: :Christian_of_Denmark
  AssignClass (38d6c0b3-492b-47c2-9f55-3901a34e57bd)
 Call ID: 38d6c0b3-492b-47c2-9f55-3901a34e57bd
  Args:
    type: :Man
    source: :Christian_of_Denmark
  AssignClass (9d25eb8b-2b94-4a9b-a715-d234b208ce71)
 Call ID: 9d25eb8b-2b94-4a9b-a715-d234b208ce71
  Args:
    type: :Person
    source: :Anne-Marie_of_Greece
  AssignClass (e42fac48-c9ce-44b1-a7a4-a8098e9b01bb)
 Call ID: e42fac48-c9ce-44b1-a7a4-a8098e9b01bb
  Args:
    type: :Woman
    source: :Anne-Marie_of_Greece
  AssignClass (bdd6f3f4-0a00-4dc1-a37a-07cfeda8e087)
 Call ID: bdd6f3f4-0a00-4dc1-a37a-07cfeda8e087
  Args:
    type: :Person
    source: :Vincent_of_Denmark
  AssignClass (1790ced6-4caf-43cb-954e-73816bcd6fa5)
 Call ID: 1790ced6-4caf-43cb-954e-73816bcd6fa5
  Args:
    type: :Man
    source: :Vincent_of_Denmark
  AddTriple (3bc67aeb-4ccb-4563-a30a-fb6fe5b7d28d)
 Call ID: 3bc67aeb-4ccb-4563-a30a-fb6fe5b7d28d
  Args:
    relation: :hasFather
    source: :Isabella_of_Denmark
    target: :Frederik_X
  AddTriple (761ac30c-5985-4de8-a80d-24d7b103215d)
 Call ID: 761ac30c-5985-4de8-a80d-24d7b103215d
  Args:
    relation: :hasMother
    target: :Mary_of_Denmark
    source: :Isabella_of_Denmark
  AddTriple (71363246-0264-496e-abcd-f2147a7b5593)
 Call ID: 71363246-0264-496e-abcd-f2147a7b5593
  Args:
    relation: :hasFather
    source: :Frederik_X
    target: :Henrik_of_Denmark
  AddTriple (10140c38-9420-4d02-9c15-85e4b0c36330)
 Call ID: 10140c38-9420-4d02-9c15-85e4b0c36330
  Args:
    relation: :hasMother
    target: :Margrethe_II
    source: :Frederik_X
  AddTriple (46bf8813-60af-4809-814f-c648e90b7cf7)
 Call ID: 46bf8813-60af-4809-814f-c648e90b7cf7
  Args:
    relation: :isBrotherOf
    target: :Isabella_of_Denmark
    source: :Christian_of_Denmark
  AddTriple (cbd0e8dd-034a-4c35-829a-6c5e7ed9881e)
 Call ID: cbd0e8dd-034a-4c35-829a-6c5e7ed9881e
  Args:
    target: :Isabella_of_Denmark
    source: :Vincent_of_Denmark
    relation: :isBrotherOf
  AddLiteral (bba401cf-5605-4d54-a90c-d7558f9b6a9d)
 Call ID: bba401cf-5605-4d54-a90c-d7558f9b6a9d
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: :Isabella_of_Denmark
    literal_value: 2007
  AddLiteral (30ad1b90-05b7-4cbd-bd02-c6acc00248f0)
 Call ID: 30ad1b90-05b7-4cbd-bd02-c6acc00248f0
  Args:
    relation: :hasSex
    literal_type: xsd:string
    literal_value: Female
    source: :Isabella_of_Denmark
  Finish (d5078816-ebb7-4d0b-960c-abc460a9aa0b)
 Call ID: d5078816-ebb7-4d0b-960c-abc460a9aa0b
  Args: