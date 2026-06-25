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
  AssignClass (877b5af6-522d-40dd-aa95-4fda6d33f085)
 Call ID: 877b5af6-522d-40dd-aa95-4fda6d33f085
  Args:
    source: :PrincessBenedikte
    type: :Woman
  AssignClass (6d381bc2-da15-4f9f-a239-0a8a6ac9e8d7)
 Call ID: 6d381bc2-da15-4f9f-a239-0a8a6ac9e8d7
  Args:
    source: :PrincessBenedikte
    type: :Person
  AddLiteral (764c0a78-c75f-4be5-8875-261e3957f789)
 Call ID: 764c0a78-c75f-4be5-8875-261e3957f789
  Args:
    literal_value: Benedikte Astrid Ingeborg Ingrid
    literal_type: xsd:string
    relation: :knownAs
    source: :PrincessBenedikte
  AddLiteral (55de6eb4-e549-4d25-bea9-de41cdf44082)
 Call ID: 55de6eb4-e549-4d25-bea9-de41cdf44082
  Args:
    literal_value: 1944
    literal_type: xsd:integer
    source: :PrincessBenedikte
    relation: :hasBirthYear
  AssignClass (06b24af3-1057-4c24-886c-3721ace8752d)
 Call ID: 06b24af3-1057-4c24-886c-3721ace8752d
  Args:
    source: :KingFrederikIX
    type: :Man
  AssignClass (fb73db48-ff51-48b3-9649-996465f2fc4c)
 Call ID: fb73db48-ff51-48b3-9649-996465f2fc4c
  Args:
    source: :KingFrederikIX
    type: :Person
  AssignClass (b53704bf-6d47-4437-b59a-162a4fa56cda)
 Call ID: b53704bf-6d47-4437-b59a-162a4fa56cda
  Args:
    source: :QueenIngrid
    type: :Woman
  AssignClass (4a8725ce-1446-4ba7-b569-6d131dbb12d0)
 Call ID: 4a8725ce-1446-4ba7-b569-6d131dbb12d0
  Args:
    source: :QueenIngrid
    type: :Person
  AddTriple (f805fa25-99d1-4225-9c71-703716d93743)
 Call ID: f805fa25-99d1-4225-9c71-703716d93743
  Args:
    source: :PrincessBenedikte
    relation: :hasFather
    target: :KingFrederikIX
  AddTriple (df5ee3d0-12b0-48b9-92d2-95a58cab1d7b)
 Call ID: df5ee3d0-12b0-48b9-92d2-95a58cab1d7b
  Args:
    relation: :hasMother
    source: :PrincessBenedikte
    target: :QueenIngrid
  AssignClass (1215c3e1-565f-4950-ae87-94f571cbf230)
 Call ID: 1215c3e1-565f-4950-ae87-94f571cbf230
  Args:
    source: :QueenMargretheII
    type: :Woman
  AssignClass (5464f591-df3c-4aec-8efa-795ae8fc8a04)
 Call ID: 5464f591-df3c-4aec-8efa-795ae8fc8a04
  Args:
    source: :QueenMargretheII
    type: :Person
  AddTriple (b634345e-4d8e-4c56-9e0b-b39608b6f803)
 Call ID: b634345e-4d8e-4c56-9e0b-b39608b6f803
  Args:
    target: :QueenMargretheII
    relation: :isSisterOf
    source: :PrincessBenedikte
  AssignClass (aab20ed0-ac65-4f20-8bab-2594de0438e7)
 Call ID: aab20ed0-ac65-4f20-8bab-2594de0438e7
  Args:
    source: :FrederikX
    type: :Man
  AssignClass (6efd75a4-7c92-4d71-b309-16cc95ad26f0)
 Call ID: 6efd75a4-7c92-4d71-b309-16cc95ad26f0
  Args:
    source: :FrederikX
    type: :Person
  AddTriple (045487f9-b74e-4281-818b-b2ae674ce039)
 Call ID: 045487f9-b74e-4281-818b-b2ae674ce039
  Args:
    target: :QueenMargretheII
    source: :FrederikX
    relation: :hasMother
  AssignClass (c562fd35-feb8-4e9f-9c36-b992b19157b1)
 Call ID: c562fd35-feb8-4e9f-9c36-b992b19157b1
  Args:
    source: :QueenAnneMarie
    type: :Woman
  AssignClass (394ed9dd-8777-4c5a-8565-0a8a1849aea2)
 Call ID: 394ed9dd-8777-4c5a-8565-0a8a1849aea2
  Args:
    source: :QueenAnneMarie
    type: :Person
  AddTriple (b594264e-7b04-4819-afe3-39bd3ccc2d40)
 Call ID: b594264e-7b04-4819-afe3-39bd3ccc2d40
  Args:
    target: :QueenAnneMarie
    source: :PrincessBenedikte
    relation: :isSisterOf
  AssignClass (8de1b9e4-3624-425c-bd2f-e2086177addf)
 Call ID: 8de1b9e4-3624-425c-bd2f-e2086177addf
  Args:
    source: :RichardPrinceOfSaynWittgensteinBerleburg
    type: :Man
  AssignClass (ac4a4de1-6a19-4239-a0f9-04ddd328bbd1)
 Call ID: ac4a4de1-6a19-4239-a0f9-04ddd328bbd1
  Args:
    source: :RichardPrinceOfSaynWittgensteinBerleburg
    type: :Person
  AddLiteral (68e14706-486a-4118-851a-cd918b5bc9b0)
 Call ID: 68e14706-486a-4118-851a-cd918b5bc9b0
  Args:
    literal_type: xsd:integer
    literal_value: 1934
    source: :RichardPrinceOfSaynWittgensteinBerleburg
    relation: :hasBirthYear
  AddLiteral (261aeeba-8a66-426b-ad52-370a84edb2f5)
 Call ID: 261aeeba-8a66-426b-ad52-370a84edb2f5
  Args:
    literal_value: 2017
    literal_type: xsd:integer
    source: :RichardPrinceOfSaynWittgensteinBerleburg
    relation: :hasDeathYear
  AddLiteral (7f788a04-73d6-4823-92dd-99a140ee4d22)
 Call ID: 7f788a04-73d6-4823-92dd-99a140ee4d22
  Args:
    source: :PrincessBenedikte
    relation: :hasMarriageYear
    literal_value: 1968
    literal_type: xsd:integer
  AddTriple (654c7c0f-fb06-4c22-a104-680acd6cc758)
 Call ID: 654c7c0f-fb06-4c22-a104-680acd6cc758
  Args:
    target: :RichardPrinceOfSaynWittgensteinBerleburg
    source: :PrincessBenedikte
    relation: :hasRelation
  AssignClass (5d05e7d4-0a27-459f-842a-99cfb33f083d)
 Call ID: 5d05e7d4-0a27-459f-842a-99cfb33f083d
  Args:
    source: :KingChristianX
    type: :Man
  AssignClass (941c026f-8f37-4b71-b7c9-1cae53da9917)
 Call ID: 941c026f-8f37-4b71-b7c9-1cae53da9917
  Args:
    source: :KingChristianX
    type: :Person
  AssignClass (63b3a027-7fbe-4264-9f1b-b8883034682f)
 Call ID: 63b3a027-7fbe-4264-9f1b-b8883034682f
  Args:
    source: :QueenAlexandrine
    type: :Woman
  AssignClass (520c16c6-7c0f-4b49-8446-bdcde207f4f7)
 Call ID: 520c16c6-7c0f-4b49-8446-bdcde207f4f7
  Args:
    source: :QueenAlexandrine
    type: :Person
  AddTriple (e58164ba-3f67-4850-8117-8b3e3e0c3020)
 Call ID: e58164ba-3f67-4850-8117-8b3e3e0c3020
  Args:
    relation: :hasFather
    source: :KingFrederikIX
    target: :KingChristianX
  AddTriple (5ca4a2ca-cb90-4a16-aea3-f4a5896abba6)
 Call ID: 5ca4a2ca-cb90-4a16-aea3-f4a5896abba6
  Args:
    target: :QueenAlexandrine
    relation: :hasMother
    source: :KingFrederikIX
  AssignClass (d572c3b8-aec2-4990-ab64-4a37891b3e47)
 Call ID: d572c3b8-aec2-4990-ab64-4a37891b3e47
  Args:
    source: :CrownPrinceGustavAdolfOfSweden
    type: :Man
  AssignClass (19b2f7b1-f280-4444-bcbd-efc6d2594fb2)
 Call ID: 19b2f7b1-f280-4444-bcbd-efc6d2594fb2
  Args:
    source: :CrownPrinceGustavAdolfOfSweden
    type: :Person
  AssignClass (3a9b3da6-69e1-4b21-a51a-a81aff1e791b)
 Call ID: 3a9b3da6-69e1-4b21-a51a-a81aff1e791b
  Args:
    source: :PrincessMargaretOfConnaught
    type: :Woman
  AssignClass (46be2bf5-40ac-4a0b-83bf-9d5041c4e80a)
 Call ID: 46be2bf5-40ac-4a0b-83bf-9d5041c4e80a
  Args:
    source: :PrincessMargaretOfConnaught
    type: :Person
  AddTriple (c7a795fe-455c-4cb6-afa4-907c8074e283)
 Call ID: c7a795fe-455c-4cb6-afa4-907c8074e283
  Args:
    target: :CrownPrinceGustavAdolfOfSweden
    relation: :hasFather
    source: :QueenIngrid
  AddTriple (6f8a6082-1101-4da5-9e63-61a15c02048d)
 Call ID: 6f8a6082-1101-4da5-9e63-61a15c02048d
  Args:
    target: :PrincessMargaretOfConnaught
    relation: :hasMother
    source: :QueenIngrid
  AssignClass (dd026def-fa47-45cf-94e4-23a0bd2d71f3)
 Call ID: dd026def-fa47-45cf-94e4-23a0bd2d71f3
  Args:
    source: :PrinceKnud
    type: :Man
  AssignClass (bb6a19b8-5dcd-4273-a3dd-57f5300d2b06)
 Call ID: bb6a19b8-5dcd-4273-a3dd-57f5300d2b06
  Args:
    source: :PrinceKnud
    type: :Person
  AddTriple (d7c66d0c-ba58-435e-aa3c-8730e993650b)
 Call ID: d7c66d0c-ba58-435e-aa3c-8730e993650b
  Args:
    source: :KingFrederikIX
    relation: :hasBrother
    target: :PrinceKnud
  AssignClass (5210e610-3f66-4742-98ef-53ff8ab8b53d)
 Call ID: 5210e610-3f66-4742-98ef-53ff8ab8b53d
  Args:
    source: :ConstantineIIOfGreece
    type: :Man
  AssignClass (7482804f-6e96-48f6-ab08-2967edfac34b)
 Call ID: 7482804f-6e96-48f6-ab08-2967edfac34b
  Args:
    source: :ConstantineIIOfGreece
    type: :Person
  AddTriple (adaaa514-3878-48a4-a250-c066a7d836e9)
 Call ID: adaaa514-3878-48a4-a250-c066a7d836e9
  Args:
    relation: :hasRelation
    source: :QueenAnneMarie
    target: :ConstantineIIOfGreece
  AssignClass (d6f1327c-46eb-4421-9760-597cfd101854)
 Call ID: d6f1327c-46eb-4421-9760-597cfd101854
  Args:
    source: :Nathalie
    type: :Woman
  AssignClass (537e913b-0131-451d-b046-d893bac99ba6)
 Call ID: 537e913b-0131-451d-b046-d893bac99ba6
  Args:
    source: :Nathalie
    type: :Person
  AddTriple (6fe38cba-1269-4cc0-90fd-718577bcec3b)
 Call ID: 6fe38cba-1269-4cc0-90fd-718577bcec3b
  Args:
    target: :PrincessBenedikte
    source: :Nathalie
    relation: :hasMother
  Finish (b8890fc8-057b-449a-b455-1fc3433b006c)
 Call ID: b8890fc8-057b-449a-b455-1fc3433b006c
  Args: