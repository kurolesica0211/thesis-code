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
  AssignClass (a7941166-4b1e-4c6a-abfd-0895bc0eab9f)
 Call ID: a7941166-4b1e-4c6a-abfd-0895bc0eab9f
  Args:
    type: :Woman
    source: :Princess_Benedikte
  AssignClass (506cb1b8-8d75-444b-ac4b-9d050e18476e)
 Call ID: 506cb1b8-8d75-444b-ac4b-9d050e18476e
  Args:
    source: :King_Frederik_IX
    type: :Man
  AssignClass (e2b46ff2-8ccc-49c5-b77d-f32db7b82328)
 Call ID: e2b46ff2-8ccc-49c5-b77d-f32db7b82328
  Args:
    source: :Queen_Ingrid
    type: :Woman
  AssignClass (9d93972a-15fc-4ef9-8285-c7c58d55cd6e)
 Call ID: 9d93972a-15fc-4ef9-8285-c7c58d55cd6e
  Args:
    type: :Woman
    source: :Queen_Margrethe_II
  AssignClass (b6afbac1-0b4b-45f9-b61d-0fe0ebbcbd5e)
 Call ID: b6afbac1-0b4b-45f9-b61d-0fe0ebbcbd5e
  Args:
    source: :King_Frederik_X
    type: :Man
  AssignClass (d8e5659f-9772-4fa0-ab99-9b696ec46001)
 Call ID: d8e5659f-9772-4fa0-ab99-9b696ec46001
  Args:
    source: :Queen_Anne-Marie
    type: :Woman
  AssignClass (839c45fd-cbdd-45a2-82cd-5fee3d6ee8ab)
 Call ID: 839c45fd-cbdd-45a2-82cd-5fee3d6ee8ab
  Args:
    source: :Richard_6th_Prince_of_Sayn-Wittgenstein-Berleburg
    type: :Man
  AssignClass (9edc3d4f-1634-49cc-8bae-377354000539)
 Call ID: 9edc3d4f-1634-49cc-8bae-377354000539
  Args:
    type: :Woman
    source: :Princess_Nathalie
  AssignClass (b8ba3486-79ce-4c14-a207-3f889ca3c413)
 Call ID: b8ba3486-79ce-4c14-a207-3f889ca3c413
  Args:
    type: :Man
    source: :King_Christian_X
  AssignClass (372185aa-36a7-4001-8091-b87069ddf64a)
 Call ID: 372185aa-36a7-4001-8091-b87069ddf64a
  Args:
    type: :Woman
    source: :Queen_Alexandrine
  AssignClass (ca110c9c-23f5-4a2f-93e9-a3733e9d833f)
 Call ID: ca110c9c-23f5-4a2f-93e9-a3733e9d833f
  Args:
    source: :Crown_Prince_Gustav_Adolf_of_Sweden
    type: :Man
  AssignClass (17efc99a-d1bc-4d67-a179-062ef40a7a3a)
 Call ID: 17efc99a-d1bc-4d67-a179-062ef40a7a3a
  Args:
    type: :Woman
    source: :Princess_Margaret_of_Connaught
  AssignClass (932f38af-17f2-4b07-a6b8-726771bda4a3)
 Call ID: 932f38af-17f2-4b07-a6b8-726771bda4a3
  Args:
    source: :Constantine_II_of_Greece
    type: :Man
  AddLiteral (188155e2-581e-434a-97e2-05d49b5f0129)
 Call ID: 188155e2-581e-434a-97e2-05d49b5f0129
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1944
    source: :Princess_Benedikte
  AddTriple (898c583b-fd12-411d-a85f-5ccf867e5cac)
 Call ID: 898c583b-fd12-411d-a85f-5ccf867e5cac
  Args:
    target: :King_Frederik_IX
    source: :Princess_Benedikte
    relation: :hasFather
  AddTriple (33cc4896-3cec-40db-a539-2da0a877eed5)
 Call ID: 33cc4896-3cec-40db-a539-2da0a877eed5
  Args:
    target: :Queen_Ingrid
    source: :Princess_Benedikte
    relation: :hasMother
  AddTriple (b9146579-2662-4cd2-a93c-9075b875b7e7)
 Call ID: b9146579-2662-4cd2-a93c-9075b875b7e7
  Args:
    target: :Queen_Margrethe_II
    source: :Princess_Benedikte
    relation: :isSisterOf
  AddTriple (38bae9dc-a5bb-4fa4-88f5-ddd05454a49d)
 Call ID: 38bae9dc-a5bb-4fa4-88f5-ddd05454a49d
  Args:
    source: :Princess_Benedikte
    target: :Queen_Anne-Marie
    relation: :isSisterOf
  AddTriple (d9cded17-40a5-433c-a6ed-93a49bd84605)
 Call ID: d9cded17-40a5-433c-a6ed-93a49bd84605
  Args:
    relation: :isMotherOf
    target: :King_Frederik_X
    source: :Queen_Margrethe_II
  AddTriple (8177f270-2076-4311-a2e7-b3cde0ba8e7f)
 Call ID: 8177f270-2076-4311-a2e7-b3cde0ba8e7f
  Args:
    relation: :hasFather
    source: :King_Frederik_IX
    target: :King_Christian_X
  AddTriple (73a6d887-e9b2-40b8-9a8b-f5812ca240c0)
 Call ID: 73a6d887-e9b2-40b8-9a8b-f5812ca240c0
  Args:
    relation: :hasMother
    target: :Queen_Alexandrine
    source: :King_Frederik_IX
  AddTriple (f755d12a-10cc-4a63-8d4e-0520a987b737)
 Call ID: f755d12a-10cc-4a63-8d4e-0520a987b737
  Args:
    relation: :hasFather
    target: :Crown_Prince_Gustav_Adolf_of_Sweden
    source: :Queen_Ingrid
  AddTriple (e4baffea-16d0-46a7-ab53-b9f86d7911d7)
 Call ID: e4baffea-16d0-46a7-ab53-b9f86d7911d7
  Args:
    relation: :hasMother
    target: :Princess_Margaret_of_Connaught
    source: :Queen_Ingrid
  AddTriple (e20141e3-2c74-4080-9e4b-921961fa5672)
 Call ID: e20141e3-2c74-4080-9e4b-921961fa5672
  Args:
    relation: :hasMother
    source: :Queen_Anne-Marie
    target: :Queen_Ingrid
  AddTriple (341050b2-f101-4bf4-a31f-5df3da20dacf)
 Call ID: 341050b2-f101-4bf4-a31f-5df3da20dacf
  Args:
    relation: :hasFather
    source: :Queen_Anne-Marie
    target: :King_Frederik_IX
  AddTriple (89fc59b3-937c-4513-aa33-82e291d87ae2)
 Call ID: 89fc59b3-937c-4513-aa33-82e291d87ae2
  Args:
    source: :Queen_Margrethe_II
    target: :Queen_Ingrid
    relation: :hasMother
  AddTriple (a9ff3211-34a1-451f-9a9b-6c8961985e15)
 Call ID: a9ff3211-34a1-451f-9a9b-6c8961985e15
  Args:
    relation: :hasFather
    source: :Queen_Margrethe_II
    target: :King_Frederik_IX
  AddLiteral (45b7a6ee-978d-4497-86bd-a5d929be1f2c)
 Call ID: 45b7a6ee-978d-4497-86bd-a5d929be1f2c
  Args:
    literal_type: xsd:integer
    literal_value: 1968
    relation: :hasMarriageYear
    source: :Princess_Benedikte
  AddTriple (94baf26a-eb9b-4e2f-9279-adcfa0beb30b)
 Call ID: 94baf26a-eb9b-4e2f-9279-adcfa0beb30b
  Args:
    relation: :hasMother
    source: :Princess_Nathalie
    target: :Princess_Benedikte
  AddTriple (c44eba14-30fd-4e04-908a-051e532b7f54)
 Call ID: c44eba14-30fd-4e04-908a-051e532b7f54
  Args:
    source: :Princess_Nathalie
    target: :Richard_6th_Prince_of_Sayn-Wittgenstein-Berleburg
    relation: :hasFather
  AddTriple (05b4b5d9-7f03-438d-89b5-f182b0400ffb)
 Call ID: 05b4b5d9-7f03-438d-89b5-f182b0400ffb
  Args:
    target: :Constantine_II_of_Greece
    source: :Queen_Anne-Marie
    relation: :isMotherOf
  AddLiteral (6d4c3abb-6b70-49a2-b9bc-292862c1cd08)
 Call ID: 6d4c3abb-6b70-49a2-b9bc-292862c1cd08
  Args:
    relation: :hasDeathYear
    literal_value: 2017
    literal_type: xsd:integer
    source: :Richard_6th_Prince_of_Sayn-Wittgenstein-Berleburg
  Finish (ace9b60d-1df5-422e-90b3-60fb93937796)
 Call ID: ace9b60d-1df5-422e-90b3-60fb93937796
  Args: