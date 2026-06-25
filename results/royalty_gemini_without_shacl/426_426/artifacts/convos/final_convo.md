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
Prince Amedeo, 3rd Duke of Aosta (Amedeo Umberto Isabella Luigi Filippo Maria Giuseppe Giovanni di Savoia-Aosta; 21 October 1898 – 3 March 1942) was the third Duke of Aosta and a first cousin once removed of the King of Italy, Victor Emmanuel III.
Biography

Amedeo was born in Turin, Piedmont, to Prince Emanuele Filiberto, 2nd Duke of Aosta (son of Amadeo I of Spain and Princess Maria Vittoria), and Princess Hélène (daughter of Prince Philippe of Orléans and Princess Marie Isabelle of Orléans).
He was known from birth by the courtesy title of Duke of Apulia.
Amedeo was a very tall man (in stark contrast to the King, who was known to be quite short).
According to Amedeo Guillet, he was once referred to by a journalist as "Your Highness" (which in Italian could also be interpreted to mean "your height").
The Duke replied in jest: "198 centimetres ".
Education and early military career

Amedeo was educated at St David's College, Reigate, Surrey, in England.
Amedeo entered the Nunziatella, the military academy in Naples, joined the Italian Royal Army (Regio Esercito) and fought with distinction in the artillery during World War I.
Amedeo subsequently rejoined the Italian armed forces and became a pilot.
Amedeo served under Marshal Rodolfo Graziani and Libyan Governor Pietro Badoglio during the later stages of the so-called "pacification of Libya" (1911 to 1932).
Amedeo and his fellow airmen harried the Senussi forces of Omar Mukhtar from the sky.
When hostilities in Libya came to an end in early 1932, much was made of the participation of the "Duke of Apulia" as the commander of the airmen who forced the Senussi to flee Libya and seek relief in Egypt.
Amedeo, portrayed by the tall actor Sky du Mont, appears in several non-flying scenes with Graziani in the movie The Lion of the Desert, about the Italian conquest of Libya.
On 4 July 1931, upon the death of his father, Amedeo became the Duke of Aosta.
Viceroy and governor-general

In 1937, after the Italian conquest of Ethiopia during the Second Italo-Abyssinian War, the Duke of Aosta replaced Marshal Graziani as Viceroy and as Governor-General of Italian East Africa.
Amedeo was succeeded by his brother, Aimone, 4th Duke of Aosta.
Aftermath

Amedeo was well known and highly regarded for being a gentleman.
Count Galeazzo Ciano, Italian Foreign Minister under his father-in-law, Italian dictator Benito Mussolini, paid Amedeo a high compliment in his famous diaries.
Upon being given the news of the Duke's death, Ciano wrote, "So dies the image of a Prince and an Italian.
"


Emperor Haile Selassie of Ethiopia was also impressed by the respect and care that the Duke of Aosta showed to the exiled Emperor's personal property left behind in Addis Ababa.
In a gesture of thanks, the Emperor during his state visit to Italy in 1953 invited the widowed Duchess of Aosta to tea during his stay in Milan, but was then informed by the Italian government that receiving the Duchess would cause offence to the Italian Republic, and so the Emperor cancelled the visit.
Instead he invited the 5th Duke of Aosta to Ethiopia in the mid-1960s, and accorded him all the protocol due to visiting royalty.
Family

Amedeo was married on 5 November 1927, in Naples, to his first cousin Princess Anne of Orléans (1906–1986), daughter of Prince Jean, Duke of Guise, and Princess Isabelle of Orléans.
They had two daughters:


Cultural depictions

Prince Amedeo's time in Italian Cyrenaica was depicted in the 1981 film Lion of the Desert; Amedeo was played by Sky du Mont.


Amedeo was also briefly mentioned in A Farewell to Arms by Ernest Hemingway.
In the popular mod for the grand strategy game Hearts of Iron IV, Kaiserreich, Amedeo is depicted as King Amadeo I di Savoia-Aosta of Sardinia, an exiled monarchist government of Italy seeking to reclaim the land from the northern Socialist Republic of Italy and southern Kingdom of the Two Sicilies.



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
  AssignClass (116158a2-34cd-4f18-8e7f-f133d0f160b7)
 Call ID: 116158a2-34cd-4f18-8e7f-f133d0f160b7
  Args:
    source: :Amedeo_3rd_Duke_of_Aosta
    type: :Man
  AssignClass (db7aa6b1-98b3-41a3-a503-44efe1fbc30c)
 Call ID: db7aa6b1-98b3-41a3-a503-44efe1fbc30c
  Args:
    type: :Person
    source: :Amedeo_3rd_Duke_of_Aosta
  AddLiteral (da833a5c-831b-4f5c-af68-73380961066f)
 Call ID: da833a5c-831b-4f5c-af68-73380961066f
  Args:
    source: :Amedeo_3rd_Duke_of_Aosta
    literal_type: xsd:integer
    literal_value: 1898
    relation: :hasBirthYear
  AddLiteral (5c4cfe78-a763-4160-8699-178b2ec7fc72)
 Call ID: 5c4cfe78-a763-4160-8699-178b2ec7fc72
  Args:
    literal_type: xsd:integer
    source: :Amedeo_3rd_Duke_of_Aosta
    relation: :hasDeathYear
    literal_value: 1942
  AssignClass (1d9e9a18-d8b0-4482-a2f3-a1488e0f63eb)
 Call ID: 1d9e9a18-d8b0-4482-a2f3-a1488e0f63eb
  Args:
    source: :Prince_Emanuele_Filiberto_2nd_Duke_of_Aosta
    type: :Man
  AssignClass (d624e83b-d21c-4e89-9c83-c7318b4cd048)
 Call ID: d624e83b-d21c-4e89-9c83-c7318b4cd048
  Args:
    type: :Person
    source: :Prince_Emanuele_Filiberto_2nd_Duke_of_Aosta
  AssignClass (d175cce0-9aeb-4167-9ddf-c7ac0c9048d4)
 Call ID: d175cce0-9aeb-4167-9ddf-c7ac0c9048d4
  Args:
    source: :Princess_Helene
    type: :Woman
  AssignClass (66075a3a-af49-40cc-bac6-9f46e22a7d6c)
 Call ID: 66075a3a-af49-40cc-bac6-9f46e22a7d6c
  Args:
    source: :Princess_Helene
    type: :Person
  AddTriple (898a3aba-6e6f-4663-af03-a558fa4b29fa)
 Call ID: 898a3aba-6e6f-4663-af03-a558fa4b29fa
  Args:
    source: :Amedeo_3rd_Duke_of_Aosta
    target: :Prince_Emanuele_Filiberto_2nd_Duke_of_Aosta
    relation: :hasFather
  AddTriple (269bd302-d755-47b0-a840-e76e90906a4c)
 Call ID: 269bd302-d755-47b0-a840-e76e90906a4c
  Args:
    relation: :hasMother
    target: :Princess_Helene
    source: :Amedeo_3rd_Duke_of_Aosta
  AssignClass (179a495e-5eae-4aad-a867-52481a4107ff)
 Call ID: 179a495e-5eae-4aad-a867-52481a4107ff
  Args:
    type: :Man
    source: :Amadeo_I_of_Spain
  AssignClass (5e465592-3388-46e5-8a45-ae4e29c9473b)
 Call ID: 5e465592-3388-46e5-8a45-ae4e29c9473b
  Args:
    source: :Amadeo_I_of_Spain
    type: :Person
  AssignClass (5fec1789-0b26-4616-9079-ed74fa7f39aa)
 Call ID: 5fec1789-0b26-4616-9079-ed74fa7f39aa
  Args:
    source: :Princess_Maria_Vittoria
    type: :Woman
  AssignClass (74de19bc-3f6e-4d70-98ea-c979c01f9e10)
 Call ID: 74de19bc-3f6e-4d70-98ea-c979c01f9e10
  Args:
    source: :Princess_Maria_Vittoria
    type: :Person
  AddTriple (52d42096-3d89-47bd-bb3d-d4aa276f4498)
 Call ID: 52d42096-3d89-47bd-bb3d-d4aa276f4498
  Args:
    source: :Prince_Emanuele_Filiberto_2nd_Duke_of_Aosta
    target: :Amadeo_I_of_Spain
    relation: :hasFather
  AddTriple (605d0d9a-ed3f-4824-bf5a-422e5c318c1f)
 Call ID: 605d0d9a-ed3f-4824-bf5a-422e5c318c1f
  Args:
    source: :Prince_Emanuele_Filiberto_2nd_Duke_of_Aosta
    target: :Princess_Maria_Vittoria
    relation: :hasMother
  AssignClass (0b38c679-bb8f-4187-826f-797091b25b61)
 Call ID: 0b38c679-bb8f-4187-826f-797091b25b61
  Args:
    type: :Man
    source: :Prince_Philippe_of_Orleans
  AssignClass (68f4cfa0-c837-402f-9f81-74d918f749a9)
 Call ID: 68f4cfa0-c837-402f-9f81-74d918f749a9
  Args:
    source: :Prince_Philippe_of_Orleans
    type: :Person
  AssignClass (e9308f5d-2c57-432f-853e-396a6691c271)
 Call ID: e9308f5d-2c57-432f-853e-396a6691c271
  Args:
    type: :Woman
    source: :Princess_Marie_Isabelle_of_Orleans
  AssignClass (1d6ebf6e-09e4-43c6-af02-179d82808eca)
 Call ID: 1d6ebf6e-09e4-43c6-af02-179d82808eca
  Args:
    type: :Person
    source: :Princess_Marie_Isabelle_of_Orleans
  AddTriple (c86c7429-b41a-4daf-84ae-0edbf54a6f04)
 Call ID: c86c7429-b41a-4daf-84ae-0edbf54a6f04
  Args:
    source: :Princess_Helene
    target: :Prince_Philippe_of_Orleans
    relation: :hasFather
  AddTriple (c4c5b750-9697-4bd3-b05a-7502e69a7d6c)
 Call ID: c4c5b750-9697-4bd3-b05a-7502e69a7d6c
  Args:
    relation: :hasMother
    target: :Princess_Marie_Isabelle_of_Orleans
    source: :Princess_Helene
  AssignClass (4be64ba1-be9f-44fa-ae8a-df8cd34673ec)
 Call ID: 4be64ba1-be9f-44fa-ae8a-df8cd34673ec
  Args:
    type: :Man
    source: :Aimone_4th_Duke_of_Aosta
  AssignClass (7bab45e2-0c26-4f3d-9de5-a2d946d20164)
 Call ID: 7bab45e2-0c26-4f3d-9de5-a2d946d20164
  Args:
    source: :Aimone_4th_Duke_of_Aosta
    type: :Person
  AddTriple (f92f887f-6b1f-4094-a80a-734dc69ff098)
 Call ID: f92f887f-6b1f-4094-a80a-734dc69ff098
  Args:
    source: :Aimone_4th_Duke_of_Aosta
    relation: :isBrotherOf
    target: :Amedeo_3rd_Duke_of_Aosta
  AssignClass (fc9a376a-c9ff-4caf-bb2e-d8e3b80a2691)
 Call ID: fc9a376a-c9ff-4caf-bb2e-d8e3b80a2691
  Args:
    source: :Princess_Anne_of_Orleans
    type: :Woman
  AssignClass (f8061e3e-fae6-43d9-834a-0878f0e95e47)
 Call ID: f8061e3e-fae6-43d9-834a-0878f0e95e47
  Args:
    source: :Princess_Anne_of_Orleans
    type: :Person
  AddTriple (5b8a217f-4c99-44b3-8488-c0f03ac36b8a)
 Call ID: 5b8a217f-4c99-44b3-8488-c0f03ac36b8a
  Args:
    source: :Amedeo_3rd_Duke_of_Aosta
    target: :Princess_Anne_of_Orleans
    relation: :hasRelation
  AddLiteral (9ede6ca5-9533-48a9-b34f-5b462b8363b2)
 Call ID: 9ede6ca5-9533-48a9-b34f-5b462b8363b2
  Args:
    relation: :hasMarriageYear
    literal_value: 1927
    source: :Amedeo_3rd_Duke_of_Aosta
    literal_type: xsd:integer
  AssignClass (65669afc-f9b2-4512-b8f7-231f44c94d6c)
 Call ID: 65669afc-f9b2-4512-b8f7-231f44c94d6c
  Args:
    source: :Prince_Jean_Duke_of_Guise
    type: :Man
  AssignClass (6186bba1-339d-4f92-9984-01ad093e96e6)
 Call ID: 6186bba1-339d-4f92-9984-01ad093e96e6
  Args:
    type: :Person
    source: :Prince_Jean_Duke_of_Guise
  AssignClass (b4c3dfe2-f18d-4b0d-9549-bd0acec65c6c)
 Call ID: b4c3dfe2-f18d-4b0d-9549-bd0acec65c6c
  Args:
    source: :Princess_Isabelle_of_Orleans
    type: :Woman
  AssignClass (e1adeca9-6055-4a58-8224-f758a8750b2a)
 Call ID: e1adeca9-6055-4a58-8224-f758a8750b2a
  Args:
    source: :Princess_Isabelle_of_Orleans
    type: :Person
  AddTriple (112e3a11-2ff3-410b-8232-b1f78fc58c3e)
 Call ID: 112e3a11-2ff3-410b-8232-b1f78fc58c3e
  Args:
    target: :Prince_Jean_Duke_of_Guise
    relation: :hasFather
    source: :Princess_Anne_of_Orleans
  AddTriple (797d307e-f769-499f-a2f7-1d6ad1eed8f6)
 Call ID: 797d307e-f769-499f-a2f7-1d6ad1eed8f6
  Args:
    target: :Princess_Isabelle_of_Orleans
    relation: :hasMother
    source: :Princess_Anne_of_Orleans
  Finish (e26e72c1-6c40-43bf-abbb-5f7f885bb18f)
 Call ID: e26e72c1-6c40-43bf-abbb-5f7f885bb18f
  Args: