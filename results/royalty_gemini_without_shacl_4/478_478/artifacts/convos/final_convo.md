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


Princess Benedikte of Denmark, Princess of Sayn-Wittgenstein-Berleburg RE, SKmd, D.Ht.
(Benedikte Astrid Ingeborg Ingrid, born 29 April 1944) is a member of the Danish royal family.
She is the second daughter and child of King Frederik IX and Queen Ingrid of Denmark.
She is a younger sister of Queen Margrethe II of Denmark, and therefore an aunt of Margrethe's son, the current King of Denmark, Frederik X.
She is also an older sister of Queen Anne-Marie of Greece.
Princess Benedikte often represents the Danish monarch at official or semi-official events.
She and her late husband, Richard, 6th Prince of Sayn-Wittgenstein-Berleburg, had three children.
Princess Benedikte is currently tenth and last in the line of succession to the Danish throne.
Early life

Birth and family

Benedikte was born on 29 April 1944 at Frederik VIII's Palace, her parents' residence at the Amalienborg palace complex, the principal residence of the Danish royal family in the district of Frederiksstaden in central Copenhagen.
She was the second child and daughter of Crown Prince Frederik and Crown Princess Ingrid of Denmark.
Her father was the eldest son of King Christian X and Queen Alexandrine of Denmark, and her mother was the only daughter of Crown Prince Gustav Adolf of Sweden and his first wife, Princess Margaret of Connaught.
Her birth took place during Nazi Germany's Occupation of Denmark.
The day after the birth of the princess, members of the Danish resistance group Holger Danske performed a salute of 21 bombs in the Ørstedsparken public park in central Copenhagen as a reference to the traditional 21-gun salute performed by the Danish Army and Navy at the occasion of royal births.
Her godparents were King Christian X and Queen Alexandrine of Denmark (her paternal grandparents); Prince Gustav of Denmark (paternal grand-uncle); King Gustaf V of Sweden (maternal great-grandfather), Sigvard Bernadotte (maternal uncle); Princess Caroline-Mathilde of Denmark (paternal aunt by marriage); Princess Ingeborg of Denmark (paternal grand-aunt); Princess Margaretha of Sweden (her father's first cousin); Sir Alexander Ramsay (maternal grand-uncle by marriage) and Queen Elizabeth of the United Kingdom.
Benedikte has one elder sister, Margrethe, former Queen of Denmark, and a younger sister, Anne Marie, who was born in 1946 and married Constantine II of Greece.
Childhood and education

Benedikte and her sisters grew up in apartments at Frederik VIII's Palace at Amalienborg in Copenhagen and in Fredensborg Palace in North Zealand.
On 20 April 1947, King Christian X died and Benedikte's father ascended the throne as King Frederik IX.
At the time of her father's accession to the throne, only males could ascend the throne of Denmark.
As her parents had no sons, it was assumed that her uncle Prince Knud would one day assume the throne.
The popularity of Frederik IX and his daughters and the more prominent role of women in Danish life paved the way for a new Act of Succession in 1953 which permitted female succession to the throne following the principle of male-preference primogeniture, where a female can ascend to the throne if she has no brothers.
Benedikte's elder sister Margrethe therefore became heir presumptive, and Benedikte and Anne-Marie became second and third in the line of succession.
Benedikte was educated at N. Zahle's School, a private school in Copenhagen, followed by stays at an English boarding school, Benenden School in Kent (1957), and a Swiss finishing school, Brillantmont International School in Lausanne (1960-1961).
In 1965, she took a class at Margrethe-Skolen, a private fashion and design school in Copenhagen.
Marriage

Benedikte was married on 3 February 1968 at Fredensborg Palace Church to Richard, 6th Prince of Sayn-Wittgenstein-Berleburg (1934–2017).
They had three children:


Upon her marriage, it was decided that Benedikte's children would need to be raised in Denmark in order to have succession rights.
Since the condition was not met, Benedikte's three children are not in line to succeed to the throne.
The children of Benedikte are styled as Highnesses by a Danish Order in Council.
While she and her husband resided at Berleburg Castle, Benedikte and her family retained a close connection to Denmark.
Since her husband's death in 2017, her primary residence has been her apartment at Christian VIII's Palace in Copenhagen.
Interests

Benedikte has undertaken official engagements for the Danish royal family since her youth, particular within the areas of equestrianism, scouting, disabilities and illnesses as well as children and youths.
After Queen Ingrid's death in 2000, she took over several of her patronages and additionally began receiving a yearly appanage.
Among her patronages are SOS Children's Villages (Denmark), Parasport Denmark and the National Association against Eating Disorders and Self-Harm.
As of April 2026, Benedikte holds 23 patronages.
Equestrianism

Benedikte is very involved in equestrian sport and is patron of the World Breeding Federation for Sport Horses, the Danish Warmblood Association and Hestens Værn.
Following revelations about the handling of cases of animal cruelty within the federation as well as allegations of leadership misconduct from members of the board (on which her daughter, Nathalie, was a member) of the federation in 2024, Benedikte withdrew her patronage.
The then chairman of the DRF, Dan Boyter, was revealed to have contacted the private secretaries of both Benedikte and her nephew, King Frederik X, in an effort to have Princess Nathalie (who was among 4 members of the board to raise a motion of no confidence and subsequently file a complain with the National Olympic Committee and Sports Confederation of Denmark's Ethics Committee against Boyter) removed from the board.
Scouting

Benedikte was introduced to the scouting movement when she was a teenager by her mother who had been an active patron of the Danish Girl Guides since 1936.
In 1963, at the age of 19, Benedikte stepped in for her mother, who had fallen ill, and opened the Guiding World Conference in Nyborg with a speech held in both English and French.
Benedikte has retained a close commitment to Girl Guide and Girl Scout organisations in Denmark as well as internationally.
She succeeded her mother as chairman of Pigespejdernes Fællesråd Danmark (Joint Committee of Girl Guides in Denmark).
She is patron of De grønne pigespejdere (The Green Girl Guides, Denmark), Det Danske Spejderkorps (The Danish Guide and Scout Association) and the Danish YWCA in London.
She is an honorary member of the St George's Guilds in Denmark.
Honours and awards

As Princess of Denmark, Benedikte is entitled to the style "Her Royal Highness".



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
  AssignClass (db64499d-9608-438c-a0e8-32982cd6e3cc)
 Call ID: db64499d-9608-438c-a0e8-32982cd6e3cc
  Args:
    type: :Woman
    source: :PrincessBenedikteOfDenmark
  AssignClass (2d97cd11-354f-4f02-a601-6ef7e87e4020)
 Call ID: 2d97cd11-354f-4f02-a601-6ef7e87e4020
  Args:
    type: :Person
    source: :PrincessBenedikteOfDenmark
  AssignClass (e5ff54ed-2eda-499f-ad03-92af491da8c2)
 Call ID: e5ff54ed-2eda-499f-ad03-92af491da8c2
  Args:
    type: :Man
    source: :KingFrederikIX
  AssignClass (a95d6b7c-8839-485b-8bd5-d7140e2eb605)
 Call ID: a95d6b7c-8839-485b-8bd5-d7140e2eb605
  Args:
    type: :Person
    source: :KingFrederikIX
  AssignClass (2757a052-aacc-4115-84ae-748e803f702d)
 Call ID: 2757a052-aacc-4115-84ae-748e803f702d
  Args:
    type: :Woman
    source: :QueenIngridOfDenmark
  AssignClass (eac47bc8-567e-4ff1-91f0-3a0410d24fad)
 Call ID: eac47bc8-567e-4ff1-91f0-3a0410d24fad
  Args:
    type: :Person
    source: :QueenIngridOfDenmark
  AddTriple (929664bd-c5c1-4e4d-ad80-1356df6e1f75)
 Call ID: 929664bd-c5c1-4e4d-ad80-1356df6e1f75
  Args:
    target: :KingFrederikIX
    relation: :isDaughterOf
    source: :PrincessBenedikteOfDenmark
  AddTriple (af9f9bc6-8e9a-4269-bbb4-5a30c74f095e)
 Call ID: af9f9bc6-8e9a-4269-bbb4-5a30c74f095e
  Args:
    relation: :isDaughterOf
    target: :QueenIngridOfDenmark
    source: :PrincessBenedikteOfDenmark
  AddLiteral (75d27e58-deb4-491b-9546-e74b3dce2a65)
 Call ID: 75d27e58-deb4-491b-9546-e74b3dce2a65
  Args:
    literal_type: xsd:positiveInteger
    relation: :hasBirthYear
    literal_value: 1944
    source: :PrincessBenedikteOfDenmark
  AssignClass (eedff3af-8181-4026-8088-be8b1fbcd91c)
 Call ID: eedff3af-8181-4026-8088-be8b1fbcd91c
  Args:
    type: :Woman
    source: :QueenMargretheII
  AssignClass (f7d08a0b-1add-458a-a932-4bb6e721eff3)
 Call ID: f7d08a0b-1add-458a-a932-4bb6e721eff3
  Args:
    type: :Person
    source: :QueenMargretheII
  AddTriple (7e38ba84-3151-48bc-aeca-0f8776456278)
 Call ID: 7e38ba84-3151-48bc-aeca-0f8776456278
  Args:
    source: :PrincessBenedikteOfDenmark
    target: :QueenMargretheII
    relation: :isSisterOf
  AssignClass (11152ad4-78b4-4bec-930b-918b4ee1136d)
 Call ID: 11152ad4-78b4-4bec-930b-918b4ee1136d
  Args:
    type: :Man
    source: :KingFrederikX
  AssignClass (d16f19e4-7cfe-42e5-9314-3471323042f7)
 Call ID: d16f19e4-7cfe-42e5-9314-3471323042f7
  Args:
    type: :Person
    source: :KingFrederikX
  AddTriple (2c28c70e-4750-49ca-8796-88bb0ffafa1d)
 Call ID: 2c28c70e-4750-49ca-8796-88bb0ffafa1d
  Args:
    source: :KingFrederikX
    relation: :isSonOf
    target: :QueenMargretheII
  AssignClass (4c02c4f6-8a78-47c7-979f-6e62d825491f)
 Call ID: 4c02c4f6-8a78-47c7-979f-6e62d825491f
  Args:
    type: :Woman
    source: :QueenAnneMarieOfGreece
  AssignClass (f01b07ad-389d-4109-a56f-1d37ec880a26)
 Call ID: f01b07ad-389d-4109-a56f-1d37ec880a26
  Args:
    type: :Person
    source: :QueenAnneMarieOfGreece
  AddTriple (a19caf79-8864-4bcc-b852-4597c260592c)
 Call ID: a19caf79-8864-4bcc-b852-4597c260592c
  Args:
    relation: :isSisterOf
    target: :QueenAnneMarieOfGreece
    source: :PrincessBenedikteOfDenmark
  AssignClass (dac15382-195d-4f85-b5cb-0f84c2912eb4)
 Call ID: dac15382-195d-4f85-b5cb-0f84c2912eb4
  Args:
    type: :Man
    source: :Richard6thPrinceOfSaynWittgensteinBerleburg
  AssignClass (eb8b71bb-6c0d-46ca-99ce-82fc9f1d248f)
 Call ID: eb8b71bb-6c0d-46ca-99ce-82fc9f1d248f
  Args:
    type: :Person
    source: :Richard6thPrinceOfSaynWittgensteinBerleburg
  AddLiteral (f7131e86-c268-43c8-bebc-cd67b2a7fea1)
 Call ID: f7131e86-c268-43c8-bebc-cd67b2a7fea1
  Args:
    relation: :hasBirthYear
    literal_type: xsd:positiveInteger
    literal_value: 1934
    source: :Richard6thPrinceOfSaynWittgensteinBerleburg
  AddLiteral (5c671d52-e96a-4cd4-bb95-fbbf1c88642f)
 Call ID: 5c671d52-e96a-4cd4-bb95-fbbf1c88642f
  Args:
    source: :Richard6thPrinceOfSaynWittgensteinBerleburg
    literal_value: 2017
    literal_type: xsd:positiveInteger
    relation: :hasDeathYear
  AddLiteral (eb85c74a-5366-428e-b46d-b110a90becab)
 Call ID: eb85c74a-5366-428e-b46d-b110a90becab
  Args:
    relation: :hasMarriageYear
    literal_type: xsd:positiveInteger
    source: :PrincessBenedikteOfDenmark
    literal_value: 1968
  AssignClass (099b1b2d-de33-44e4-83e1-9acccb7976c7)
 Call ID: 099b1b2d-de33-44e4-83e1-9acccb7976c7
  Args:
    type: :Woman
    source: :PrincessNathalie
  AssignClass (f5ca8260-741e-4919-8c39-e7955845a3ef)
 Call ID: f5ca8260-741e-4919-8c39-e7955845a3ef
  Args:
    type: :Person
    source: :PrincessNathalie
  AddTriple (500431c0-c12c-430e-95bd-bd11c641c30f)
 Call ID: 500431c0-c12c-430e-95bd-bd11c641c30f
  Args:
    relation: :isDaughterOf
    target: :PrincessBenedikteOfDenmark
    source: :PrincessNathalie
  AddTriple (64b4249f-c643-4484-8da0-1dde1860d56a)
 Call ID: 64b4249f-c643-4484-8da0-1dde1860d56a
  Args:
    source: :PrincessNathalie
    relation: :isDaughterOf
    target: :Richard6thPrinceOfSaynWittgensteinBerleburg
  AssignClass (58b1fe84-f682-4da4-a98c-0d17089bf1bd)
 Call ID: 58b1fe84-f682-4da4-a98c-0d17089bf1bd
  Args:
    type: :Man
    source: :KingChristianX
  AssignClass (29a89a18-9669-450d-bc8f-6f8135fc7bcb)
 Call ID: 29a89a18-9669-450d-bc8f-6f8135fc7bcb
  Args:
    type: :Person
    source: :KingChristianX
  AssignClass (67ecc5d9-fdcc-4b28-9e34-e9329980ed66)
 Call ID: 67ecc5d9-fdcc-4b28-9e34-e9329980ed66
  Args:
    type: :Woman
    source: :QueenAlexandrineOfDenmark
  AssignClass (7b59a5f2-32e2-4643-a7a0-40ac2f3d7b8c)
 Call ID: 7b59a5f2-32e2-4643-a7a0-40ac2f3d7b8c
  Args:
    type: :Person
    source: :QueenAlexandrineOfDenmark
  AddTriple (20cb8ed2-24d7-463e-93b2-62762a739c69)
 Call ID: 20cb8ed2-24d7-463e-93b2-62762a739c69
  Args:
    relation: :isFatherOf
    target: :KingFrederikIX
    source: :KingChristianX
  AddTriple (b07d00fd-1275-4a42-8c92-ad0f1200a5a7)
 Call ID: b07d00fd-1275-4a42-8c92-ad0f1200a5a7
  Args:
    relation: :isMotherOf
    target: :KingFrederikIX
    source: :QueenAlexandrineOfDenmark
  AssignClass (d6be848a-d1ff-4ee9-b800-46bdf611b3c9)
 Call ID: d6be848a-d1ff-4ee9-b800-46bdf611b3c9
  Args:
    type: :Man
    source: :CrownPrinceGustavAdolfOfSweden
  AssignClass (20638844-675e-49f9-899d-e1ef7314bc17)
 Call ID: 20638844-675e-49f9-899d-e1ef7314bc17
  Args:
    type: :Person
    source: :CrownPrinceGustavAdolfOfSweden
  AssignClass (6dcc1c45-be47-45f2-a0ee-991e843f022b)
 Call ID: 6dcc1c45-be47-45f2-a0ee-991e843f022b
  Args:
    type: :Woman
    source: :PrincessMargaretOfConnaught
  AssignClass (71a904ba-20cd-49c8-a69c-bfc70240e75c)
 Call ID: 71a904ba-20cd-49c8-a69c-bfc70240e75c
  Args:
    type: :Person
    source: :PrincessMargaretOfConnaught
  AddTriple (23ebe180-32d6-49f8-adf9-db7d93e8bc96)
 Call ID: 23ebe180-32d6-49f8-adf9-db7d93e8bc96
  Args:
    source: :CrownPrinceGustavAdolfOfSweden
    relation: :isFatherOf
    target: :QueenIngridOfDenmark
  AddTriple (e8debaa1-57dc-4c89-8bf5-d74281f0c4cb)
 Call ID: e8debaa1-57dc-4c89-8bf5-d74281f0c4cb
  Args:
    source: :PrincessMargaretOfConnaught
    target: :QueenIngridOfDenmark
    relation: :isMotherOf
  AssignClass (cf16ac7b-b800-4ff7-88c1-cc982e813bec)
 Call ID: cf16ac7b-b800-4ff7-88c1-cc982e813bec
  Args:
    type: :Man
    source: :PrinceKnud
  AssignClass (182732ee-735c-43c3-99cc-83923f7fbb09)
 Call ID: 182732ee-735c-43c3-99cc-83923f7fbb09
  Args:
    type: :Person
    source: :PrinceKnud
  AddTriple (38c0360f-4879-40cd-b7a6-00fc174fc1d2)
 Call ID: 38c0360f-4879-40cd-b7a6-00fc174fc1d2
  Args:
    source: :KingChristianX
    relation: :isFatherOf
    target: :PrinceKnud
  AddTriple (0887ea0b-63eb-4065-85a3-77780bb7ef07)
 Call ID: 0887ea0b-63eb-4065-85a3-77780bb7ef07
  Args:
    source: :QueenAlexandrineOfDenmark
    relation: :isMotherOf
    target: :PrinceKnud
  AssignClass (1db1a1b3-e434-4143-8538-574e1f6a5736)
 Call ID: 1db1a1b3-e434-4143-8538-574e1f6a5736
  Args:
    type: :Man
    source: :ConstantineIIOfGreece
  AssignClass (4f3e0c11-12c9-4712-ad40-968543a53a5b)
 Call ID: 4f3e0c11-12c9-4712-ad40-968543a53a5b
  Args:
    type: :Person
    source: :ConstantineIIOfGreece
  Finish (330a1c6d-56fe-42ef-80f7-82768509ea11)
 Call ID: 330a1c6d-56fe-42ef-80f7-82768509ea11
  Args: