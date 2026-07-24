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
  AssignClass (ec54573c-2ac7-40df-b9b3-e336c5c88595)
 Call ID: ec54573c-2ac7-40df-b9b3-e336c5c88595
  Args:
    source: :Benedikte
    type: :Woman
  AssignClass (e8205734-c17d-4f11-a413-946cb28728c7)
 Call ID: e8205734-c17d-4f11-a413-946cb28728c7
  Args:
    source: :Benedikte
    type: :Person
  AddLiteral (8eaf1ea2-10ee-4c2b-84c5-d3d51c3407f0)
 Call ID: 8eaf1ea2-10ee-4c2b-84c5-d3d51c3407f0
  Args:
    source: :Benedikte
    literal_type: xsd:integer
    literal_value: 1944
    relation: :hasBirthYear
  AssignClass (dab09a09-2ead-4b59-97ab-38f828605db4)
 Call ID: dab09a09-2ead-4b59-97ab-38f828605db4
  Args:
    source: :FrederikIX
    type: :Man
  AssignClass (67808185-33c3-4ce4-a571-48d411733898)
 Call ID: 67808185-33c3-4ce4-a571-48d411733898
  Args:
    source: :FrederikIX
    type: :Person
  AssignClass (f6ee534a-487a-43cf-a00d-995aff318462)
 Call ID: f6ee534a-487a-43cf-a00d-995aff318462
  Args:
    type: :Woman
    source: :Ingrid
  AssignClass (2c8ad325-fcdd-4d98-b9c1-6a46db89420e)
 Call ID: 2c8ad325-fcdd-4d98-b9c1-6a46db89420e
  Args:
    type: :Person
    source: :Ingrid
  AddTriple (3a64fb27-7f21-4671-ad70-5d677a9300b4)
 Call ID: 3a64fb27-7f21-4671-ad70-5d677a9300b4
  Args:
    source: :Benedikte
    target: :FrederikIX
    relation: :hasFather
  AddTriple (af2dc99a-256f-4035-b89f-6f6d9872e7bf)
 Call ID: af2dc99a-256f-4035-b89f-6f6d9872e7bf
  Args:
    source: :Benedikte
    target: :Ingrid
    relation: :hasMother
  AssignClass (4f19098b-d774-484f-90d2-18898dab6b30)
 Call ID: 4f19098b-d774-484f-90d2-18898dab6b30
  Args:
    source: :MargretheII
    type: :Woman
  AssignClass (4c59ac3d-5c50-4de2-a999-002f546426a3)
 Call ID: 4c59ac3d-5c50-4de2-a999-002f546426a3
  Args:
    type: :Person
    source: :MargretheII
  AddTriple (92b71c26-cc04-458e-9974-303e8c682b88)
 Call ID: 92b71c26-cc04-458e-9974-303e8c682b88
  Args:
    source: :Benedikte
    target: :MargretheII
    relation: :isSisterOf
  AssignClass (2d793eb1-60d8-43c5-8075-6497cbe10ace)
 Call ID: 2d793eb1-60d8-43c5-8075-6497cbe10ace
  Args:
    type: :Man
    source: :FrederikX
  AssignClass (f00ffc54-77be-43bc-9df6-fef0cd7a7e46)
 Call ID: f00ffc54-77be-43bc-9df6-fef0cd7a7e46
  Args:
    type: :Person
    source: :FrederikX
  AddTriple (605edc6a-0f0e-4196-898d-7e26b4197e4c)
 Call ID: 605edc6a-0f0e-4196-898d-7e26b4197e4c
  Args:
    target: :MargretheII
    source: :FrederikX
    relation: :hasMother
  AssignClass (12cc616d-4196-4484-b3a9-04307e9fa401)
 Call ID: 12cc616d-4196-4484-b3a9-04307e9fa401
  Args:
    type: :Woman
    source: :AnneMarie
  AssignClass (f432a6e2-6b02-4ea8-96f2-0df80a57887d)
 Call ID: f432a6e2-6b02-4ea8-96f2-0df80a57887d
  Args:
    source: :AnneMarie
    type: :Person
  AddTriple (ac5b6211-ea91-44a5-95c0-b58a9d4bf5a2)
 Call ID: ac5b6211-ea91-44a5-95c0-b58a9d4bf5a2
  Args:
    relation: :isSisterOf
    target: :AnneMarie
    source: :Benedikte
  AssignClass (df8423af-811c-46f2-ba4e-89a9a85457eb)
 Call ID: df8423af-811c-46f2-ba4e-89a9a85457eb
  Args:
    type: :Man
    source: :Richard
  AssignClass (9c36264b-3a90-4641-9f45-21a3c4575713)
 Call ID: 9c36264b-3a90-4641-9f45-21a3c4575713
  Args:
    source: :Richard
    type: :Person
  AddLiteral (4d237ffe-e0b2-478d-b995-22acb611deec)
 Call ID: 4d237ffe-e0b2-478d-b995-22acb611deec
  Args:
    literal_value: 1968
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: :Benedikte
  AddTriple (7e4dd57a-5b5c-4548-aa72-854420c33cc9)
 Call ID: 7e4dd57a-5b5c-4548-aa72-854420c33cc9
  Args:
    relation: :hasRelation
    target: :Richard
    source: :Benedikte
  AssignClass (d9d74093-80f0-4202-9844-98f6ebbb57a9)
 Call ID: d9d74093-80f0-4202-9844-98f6ebbb57a9
  Args:
    source: :ChristianX
    type: :Man
  AssignClass (a718f413-06ee-4dae-80e8-7f8afba746c8)
 Call ID: a718f413-06ee-4dae-80e8-7f8afba746c8
  Args:
    type: :Person
    source: :ChristianX
  AssignClass (63c33458-6ede-493a-858c-f87adac5e670)
 Call ID: 63c33458-6ede-493a-858c-f87adac5e670
  Args:
    source: :Alexandrine
    type: :Woman
  AssignClass (5dff2036-28ad-493f-b410-60fe96e12fd2)
 Call ID: 5dff2036-28ad-493f-b410-60fe96e12fd2
  Args:
    type: :Person
    source: :Alexandrine
  AddTriple (df294f4b-cc32-4ede-96d0-343edaa75a3f)
 Call ID: df294f4b-cc32-4ede-96d0-343edaa75a3f
  Args:
    source: :FrederikIX
    target: :ChristianX
    relation: :hasFather
  AddTriple (b3700d1f-d825-498c-a300-e8a7eb63d561)
 Call ID: b3700d1f-d825-498c-a300-e8a7eb63d561
  Args:
    target: :Alexandrine
    source: :FrederikIX
    relation: :hasMother
  AssignClass (e6095fd5-6f35-48f1-97e7-0fb71037ff53)
 Call ID: e6095fd5-6f35-48f1-97e7-0fb71037ff53
  Args:
    source: :GustavAdolf
    type: :Man
  AssignClass (d59293f2-4a5f-4f7d-a44c-68c4fa9650cc)
 Call ID: d59293f2-4a5f-4f7d-a44c-68c4fa9650cc
  Args:
    source: :GustavAdolf
    type: :Person
  AssignClass (7521c59f-dca2-4b19-b62f-aa6699c59ffc)
 Call ID: 7521c59f-dca2-4b19-b62f-aa6699c59ffc
  Args:
    type: :Woman
    source: :MargaretConnaught
  AssignClass (70fbdd2f-2169-48db-a99b-12182a360e3d)
 Call ID: 70fbdd2f-2169-48db-a99b-12182a360e3d
  Args:
    type: :Person
    source: :MargaretConnaught
  AddTriple (6b867978-c0e5-42e8-a371-356824991ca1)
 Call ID: 6b867978-c0e5-42e8-a371-356824991ca1
  Args:
    relation: :hasFather
    source: :Ingrid
    target: :GustavAdolf
  AddTriple (c31d1b4f-8fbd-4eff-87c5-5be9c30d1819)
 Call ID: c31d1b4f-8fbd-4eff-87c5-5be9c30d1819
  Args:
    target: :MargaretConnaught
    source: :Ingrid
    relation: :hasMother
  AssignClass (a5131c3f-a463-4c83-9881-d0b42908c026)
 Call ID: a5131c3f-a463-4c83-9881-d0b42908c026
  Args:
    source: :ConstantineII
    type: :Man
  AssignClass (13aa1c4d-a1f1-4349-b426-e4332ebd50d1)
 Call ID: 13aa1c4d-a1f1-4349-b426-e4332ebd50d1
  Args:
    source: :ConstantineII
    type: :Person
  AddTriple (a6fc75ae-669e-4aa5-8940-34671f88e7e2)
 Call ID: a6fc75ae-669e-4aa5-8940-34671f88e7e2
  Args:
    source: :AnneMarie
    target: :ConstantineII
    relation: :hasRelation
  AssignClass (9c445a6a-9a41-4b49-8587-e57db7adc66b)
 Call ID: 9c445a6a-9a41-4b49-8587-e57db7adc66b
  Args:
    source: :Nathalie
    type: :Woman
  AssignClass (df8d9f4b-b45a-42c7-913d-b8108631b69b)
 Call ID: df8d9f4b-b45a-42c7-913d-b8108631b69b
  Args:
    type: :Person
    source: :Nathalie
  AddTriple (3aa3096a-3e71-4f14-b8ff-97558583d8aa)
 Call ID: 3aa3096a-3e71-4f14-b8ff-97558583d8aa
  Args:
    target: :Benedikte
    source: :Nathalie
    relation: :hasMother
  Finish (e55d486f-8422-4ac9-a05b-7869b73cbdb2)
 Call ID: e55d486f-8422-4ac9-a05b-7869b73cbdb2
  Args: