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
Princess Dolores of Bourbon-Two Sicilies (15 November 1909 – 11 May 1996) was a daughter of Prince Carlos of Bourbon-Two Sicilies and his wife Princess Louise of Orléans.
Princess Dolores was born into the House of Bourbon-Two Sicilies and was a member of the Polish-Lithuanian noble Czartoryski family through her marriage to Prince Augustyn Józef Czartoryski.
She was also an aunt of Juan Carlos I of Spain, son of her sister Princess María de las Mercedes of Bourbon-Two Sicilies.
Early life

Born on 15 November 1909 at the Palace of Villamejor, Princess Dolores of Bourbon-Two Sicilies was the second child of Prince Carlos of Bourbon-Two Sicilies and his second wife Princess Louise of Orléans.
She was christened Maria de los Dolores Victoria Felipa Luisa Mercedes.
Princess Dolores, nicknamed Dola among his relatives, was closely related to the Spanish royal family.
Her father, Prince Carlos of Bourbon-Two Sicilies, had renounced his right to the throne of Two Sicilies becoming a Spanish citizen when he married his first wife, Mercedes, Princess of Asturias, the eldest sister of King Alfonso XIII of Spain.
Dolores’s mother, Princess Louise of Orléans was a first cousin once removed of the Spanish King.
As a result, Dolores and her sibling grew up in close proximity to the Spanish royal family.
Her cousins, the children of King Alfonso XIII and Queen Victoria Eugenie were the same age as Dolores and her younger siblings.
The family lived at the Palace of Villamejor in Madrid, vacations were spent near Seville in the Palace of Villamanrique, property of her maternal grandmother, Isabelle, Countess of Paris.
Princess Dolores studied with her sisters Mercedes  and Esperanza in a school of Irish nuns in Madrid.
Dolores was twelve years old when she moved with her family to Seville when her father was appointed Military Captain General of Andalusia.
The Princess and her sisters continued their studies as boarders at  the school of Irish nuns in Castilleja de la Cueva in Seville.
Marriage and later life

In Paris, Princess Dolores met a wealthy Polish aristocrat Prince Augustyn Józef Czartoryski, 13th Prince Czartoryski, Duke of Klewan and Zuków, son of Prince Adam Ludwik Czartoryski and his wife Countess Maria Ludwika Krasińska.
The couple settled in Kraków, Poland where Dolores’s husband took over the running of the Family Museum.
In September 1939 with the Invasion of Poland bombs fell on Kraków, Prince Augustyn and Princess Dolores, who was pregnant, decided to leave the country and move to Spain.
After reaching Paris, Princess Dolores and her husband moved permanently to Spain.
They settled in Seville where Princess Dolores gave birth to a son: Prince Adam Karol Czartoryski (born 2 January 1940).
In 1943 the couple bought a rural property in Dos Hermanas which they called it Garden of the Princess, the farm was self-sufficient for the subsistence of the family.
The couple had a second son also born in Seville, Prince Ludwik Piotr Czartoryski (13 March 1945 - 3 May 1946), but the child died at only fourteen months.
At the end of the war, the properties of the Czartoryski family were nationalized by the Polish government and the family decided not to return to Kraków, for fear of the Soviet occupation.
Prince Augustyn was in poor health, the troubles and tribulation of the war took a toll on his life and he died on 1 July 1946, aged thirty nine.
The deaths of  both her youngest son and her husband only two months apart in 1946 deeply affected the Princess, who was left a widow with a six-year-old child.
Princess Dolores continued living in Seville, Spain.
Four years into her widowhood, she fell in love with Carlos Chías Osorio (born at Barcelona 26 Feb 1925), an ex seminarist, teacher  and preceptor of her son Adam.
Carlos Chias Osorio quickly became well liked in Dos Hermanas and in spite of the age disparity the marriage was a happy one.
After the death of Princess Dolores's mother in April that year, the couple moved to Madrid.
In the following decades, the princess and her husband lived simply in Madrid.



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
  AssignClass (62fe7a45-3a81-4509-95ba-9ed2b63bdf71)
 Call ID: 62fe7a45-3a81-4509-95ba-9ed2b63bdf71
  Args:
    type: :Woman
    source: :PrincessDoloresOfBourbonTwoSicilies
  AddLiteral (805abfed-ceeb-4325-94ba-328b87fdbb7e)
 Call ID: 805abfed-ceeb-4325-94ba-328b87fdbb7e
  Args:
    literal_value: 1909
    source: :PrincessDoloresOfBourbonTwoSicilies
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (e5a2f00c-88f7-4681-a722-712bd71f6300)
 Call ID: e5a2f00c-88f7-4681-a722-712bd71f6300
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 1996
    source: :PrincessDoloresOfBourbonTwoSicilies
  AssignClass (24f77a87-6cf3-400b-8247-6028390834b1)
 Call ID: 24f77a87-6cf3-400b-8247-6028390834b1
  Args:
    type: :Man
    source: :PrinceCarlosOfBourbonTwoSicilies
  AssignClass (4076a55e-7ccb-4c9c-a1a3-824ee8c7268e)
 Call ID: 4076a55e-7ccb-4c9c-a1a3-824ee8c7268e
  Args:
    source: :PrincessLouiseOfOrléans
    type: :Woman
  AddTriple (54bbcf58-a33b-48ce-ae28-a2f882e14442)
 Call ID: 54bbcf58-a33b-48ce-ae28-a2f882e14442
  Args:
    source: :PrincessDoloresOfBourbonTwoSicilies
    target: :PrinceCarlosOfBourbonTwoSicilies
    relation: :hasFather
  AddTriple (188e28c8-47c6-4f2a-b1fb-d14a9bbf4e99)
 Call ID: 188e28c8-47c6-4f2a-b1fb-d14a9bbf4e99
  Args:
    relation: :hasMother
    target: :PrincessLouiseOfOrléans
    source: :PrincessDoloresOfBourbonTwoSicilies
  AssignClass (d8b8950d-bb22-4f15-8de5-067ec79a2ba7)
 Call ID: d8b8950d-bb22-4f15-8de5-067ec79a2ba7
  Args:
    source: :PrinceAugustynJózefCzartoryski
    type: :Man
  AddTriple (e21135d8-6dac-48a4-95d0-71889912c558)
 Call ID: e21135d8-6dac-48a4-95d0-71889912c558
  Args:
    relation: :hasRelation
    target: :PrinceAugustynJózefCzartoryski
    source: :PrincessDoloresOfBourbonTwoSicilies
  AssignClass (74f2b6b1-16f1-4aa0-866f-c48c3c168f19)
 Call ID: 74f2b6b1-16f1-4aa0-866f-c48c3c168f19
  Args:
    type: :Man
    source: :PrinceAdamLudwikCzartoryski
  AssignClass (241dacc6-c0b1-4755-ad72-36d409602c70)
 Call ID: 241dacc6-c0b1-4755-ad72-36d409602c70
  Args:
    source: :CountessMariaLudwikaKrasińska
    type: :Woman
  AddTriple (cf7438cb-207f-4a5c-8eb0-c9d260f0b34f)
 Call ID: cf7438cb-207f-4a5c-8eb0-c9d260f0b34f
  Args:
    source: :PrinceAugustynJózefCzartoryski
    relation: :hasFather
    target: :PrinceAdamLudwikCzartoryski
  AddTriple (cd7d8b53-fec0-4af1-9715-65f993b778e0)
 Call ID: cd7d8b53-fec0-4af1-9715-65f993b778e0
  Args:
    target: :CountessMariaLudwikaKrasińska
    relation: :hasMother
    source: :PrinceAugustynJózefCzartoryski
  AssignClass (a888934a-dbbb-4a53-9671-3b50c85537cf)
 Call ID: a888934a-dbbb-4a53-9671-3b50c85537cf
  Args:
    type: :Man
    source: :JuanCarlosIOfSpain
  AssignClass (3721d487-7405-433f-9afa-987238d95c4b)
 Call ID: 3721d487-7405-433f-9afa-987238d95c4b
  Args:
    type: :Woman
    source: :PrincessMaríaDeLasMercedesOfBourbonTwoSicilies
  AddTriple (89aa2c66-e2d4-4e29-91bd-e21dd890fb82)
 Call ID: 89aa2c66-e2d4-4e29-91bd-e21dd890fb82
  Args:
    source: :PrincessDoloresOfBourbonTwoSicilies
    target: :JuanCarlosIOfSpain
    relation: :isAuntOf
  AddTriple (58409167-07c6-4f1d-8ae4-0a2e632ba5f8)
 Call ID: 58409167-07c6-4f1d-8ae4-0a2e632ba5f8
  Args:
    target: :PrincessDoloresOfBourbonTwoSicilies
    relation: :isSisterOf
    source: :PrincessMaríaDeLasMercedesOfBourbonTwoSicilies
  AddTriple (03b55a86-3bd5-44c5-bdc9-b23163575f97)
 Call ID: 03b55a86-3bd5-44c5-bdc9-b23163575f97
  Args:
    target: :PrincessMaríaDeLasMercedesOfBourbonTwoSicilies
    relation: :hasMother
    source: :JuanCarlosIOfSpain
  AssignClass (cc623770-d1fd-47e6-9eb5-45f490997fb9)
 Call ID: cc623770-d1fd-47e6-9eb5-45f490997fb9
  Args:
    type: :Man
    source: :PrinceAdamKarolCzartoryski
  AddTriple (519cfc34-bc68-474b-8795-3bbfd5cc6260)
 Call ID: 519cfc34-bc68-474b-8795-3bbfd5cc6260
  Args:
    relation: :hasSon
    target: :PrinceAdamKarolCzartoryski
    source: :PrincessDoloresOfBourbonTwoSicilies
  AddTriple (06405c8d-6e0c-4b70-9a57-63e6f1c31714)
 Call ID: 06405c8d-6e0c-4b70-9a57-63e6f1c31714
  Args:
    target: :PrinceAugustynJózefCzartoryski
    relation: :hasFather
    source: :PrinceAdamKarolCzartoryski
  AssignClass (b04a1e40-633b-4dc5-ac27-881c52eb1e21)
 Call ID: b04a1e40-633b-4dc5-ac27-881c52eb1e21
  Args:
    type: :Man
    source: :PrinceLudwikPiotrCzartoryski
  AddTriple (a1c11df6-8d8c-47f2-b229-4312e3d76a0a)
 Call ID: a1c11df6-8d8c-47f2-b229-4312e3d76a0a
  Args:
    target: :PrinceLudwikPiotrCzartoryski
    relation: :hasSon
    source: :PrincessDoloresOfBourbonTwoSicilies
  AddTriple (2709be61-9dc3-4d21-9b49-0d8a4064fedc)
 Call ID: 2709be61-9dc3-4d21-9b49-0d8a4064fedc
  Args:
    source: :PrinceLudwikPiotrCzartoryski
    relation: :hasFather
    target: :PrinceAugustynJózefCzartoryski
  AssignClass (792930aa-64e9-48ad-bfea-5ab515c6a024)
 Call ID: 792930aa-64e9-48ad-bfea-5ab515c6a024
  Args:
    type: :Woman
    source: :PrincessEsperanzaOfBourbonTwoSicilies
  AddTriple (6fb62957-e383-4c94-901c-bdf41e82e2d5)
 Call ID: 6fb62957-e383-4c94-901c-bdf41e82e2d5
  Args:
    relation: :isSisterOf
    target: :PrincessDoloresOfBourbonTwoSicilies
    source: :PrincessEsperanzaOfBourbonTwoSicilies
  AssignClass (71e77497-8588-4838-ba6c-c6f74f7f8a78)
 Call ID: 71e77497-8588-4838-ba6c-c6f74f7f8a78
  Args:
    source: :CarlosChíasOsorio
    type: :Man
  AddTriple (4a979c34-6640-44ea-a407-17bd521bc506)
 Call ID: 4a979c34-6640-44ea-a407-17bd521bc506
  Args:
    source: :PrincessDoloresOfBourbonTwoSicilies
    target: :CarlosChíasOsorio
    relation: :hasRelation
  AssignClass (32af833e-e356-41c8-8c15-02f70b73c1a3)
 Call ID: 32af833e-e356-41c8-8c15-02f70b73c1a3
  Args:
    type: :Woman
    source: :IsabelleCountessOfParis
  AddTriple (eef55ccb-2656-448f-a94d-cad6123936ed)
 Call ID: eef55ccb-2656-448f-a94d-cad6123936ed
  Args:
    relation: :hasMother
    target: :IsabelleCountessOfParis
    source: :PrincessLouiseOfOrléans
  Finish (c0d1b23d-ac5a-4ecf-9302-03c7725b003e)
 Call ID: c0d1b23d-ac5a-4ecf-9302-03c7725b003e
  Args: