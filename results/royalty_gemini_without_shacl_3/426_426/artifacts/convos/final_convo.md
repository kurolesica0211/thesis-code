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
  AssignClass (1d1d70c3-68f7-4610-87e0-f1ee40f8a9e1)
 Call ID: 1d1d70c3-68f7-4610-87e0-f1ee40f8a9e1
  Args:
    type: :Man
    source: :Amedeo_3rd_Duke_of_Aosta
  AssignClass (4010b875-3576-4362-97de-783665a8ab8d)
 Call ID: 4010b875-3576-4362-97de-783665a8ab8d
  Args:
    source: :Amedeo_3rd_Duke_of_Aosta
    type: :Person
  AddLiteral (a8742bd8-69d8-41e2-a9b0-374bf76e4478)
 Call ID: a8742bd8-69d8-41e2-a9b0-374bf76e4478
  Args:
    literal_type: xsd:string
    relation: :alsoKnownAs
    literal_value: Amedeo Umberto Isabella Luigi Filippo Maria Giuseppe Giovanni di Savoia-Aosta
    source: :Amedeo_3rd_Duke_of_Aosta
  AddLiteral (c5f5cf99-e965-4f93-873d-183b0162a98e)
 Call ID: c5f5cf99-e965-4f93-873d-183b0162a98e
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: :Amedeo_3rd_Duke_of_Aosta
    literal_value: 1898
  AddLiteral (97b63ac7-90c5-4b9c-9c38-eb64de2f274a)
 Call ID: 97b63ac7-90c5-4b9c-9c38-eb64de2f274a
  Args:
    literal_type: xsd:integer
    source: :Amedeo_3rd_Duke_of_Aosta
    literal_value: 1942
    relation: :hasDeathYear
  AssignClass (9796792b-861d-45a8-a957-87a70735f3dc)
 Call ID: 9796792b-861d-45a8-a957-87a70735f3dc
  Args:
    source: :Emanuele_Filiberto_2nd_Duke_of_Aosta
    type: :Man
  AssignClass (5a2db8fc-2ab3-4bf3-920c-b4e3e06b9a9c)
 Call ID: 5a2db8fc-2ab3-4bf3-920c-b4e3e06b9a9c
  Args:
    type: :Person
    source: :Emanuele_Filiberto_2nd_Duke_of_Aosta
  AddTriple (a0e1207f-2958-4040-a782-f222a036ad49)
 Call ID: a0e1207f-2958-4040-a782-f222a036ad49
  Args:
    target: :Emanuele_Filiberto_2nd_Duke_of_Aosta
    source: :Amedeo_3rd_Duke_of_Aosta
    relation: :hasFather
  AssignClass (85f9af7e-4f15-410e-92b1-cae4eb32694f)
 Call ID: 85f9af7e-4f15-410e-92b1-cae4eb32694f
  Args:
    source: :Princess_Helene
    type: :Woman
  AssignClass (eb665e06-92a9-4687-beb5-4a60f57384a0)
 Call ID: eb665e06-92a9-4687-beb5-4a60f57384a0
  Args:
    type: :Person
    source: :Princess_Helene
  AddTriple (d7c60497-bc79-454b-bbdd-34491859bc9f)
 Call ID: d7c60497-bc79-454b-bbdd-34491859bc9f
  Args:
    source: :Amedeo_3rd_Duke_of_Aosta
    relation: :hasMother
    target: :Princess_Helene
  AssignClass (ccd6f88f-043d-4549-a75f-04b9955c5a9a)
 Call ID: ccd6f88f-043d-4549-a75f-04b9955c5a9a
  Args:
    type: :Man
    source: :Amadeo_I_of_Spain
  AssignClass (26580d7f-d369-460c-9e53-681982ca8c7c)
 Call ID: 26580d7f-d369-460c-9e53-681982ca8c7c
  Args:
    source: :Amadeo_I_of_Spain
    type: :Person
  AssignClass (d917a5f9-cc11-4d7a-b058-0f6e7c40a5cf)
 Call ID: d917a5f9-cc11-4d7a-b058-0f6e7c40a5cf
  Args:
    type: :Woman
    source: :Princess_Maria_Vittoria
  AssignClass (994c795d-92d5-47c9-94f8-e5c0cf5b9abe)
 Call ID: 994c795d-92d5-47c9-94f8-e5c0cf5b9abe
  Args:
    type: :Person
    source: :Princess_Maria_Vittoria
  AddTriple (d54d72d2-86fb-479a-a411-9e6b2e34b884)
 Call ID: d54d72d2-86fb-479a-a411-9e6b2e34b884
  Args:
    target: :Amadeo_I_of_Spain
    relation: :hasFather
    source: :Emanuele_Filiberto_2nd_Duke_of_Aosta
  AddTriple (f6409a2f-2dd9-4270-bb2f-81bd7660cfb8)
 Call ID: f6409a2f-2dd9-4270-bb2f-81bd7660cfb8
  Args:
    target: :Princess_Maria_Vittoria
    relation: :hasMother
    source: :Emanuele_Filiberto_2nd_Duke_of_Aosta
  AssignClass (140e78bc-a023-41e1-b4b8-5014ff1aa9a4)
 Call ID: 140e78bc-a023-41e1-b4b8-5014ff1aa9a4
  Args:
    type: :Man
    source: :Prince_Philippe_of_Orleans
  AssignClass (f8c35191-7e89-4f23-8b11-1b0cce3407e5)
 Call ID: f8c35191-7e89-4f23-8b11-1b0cce3407e5
  Args:
    type: :Person
    source: :Prince_Philippe_of_Orleans
  AssignClass (4c08e092-b6bf-4732-9587-0ee052464ef3)
 Call ID: 4c08e092-b6bf-4732-9587-0ee052464ef3
  Args:
    source: :Princess_Marie_Isabelle_of_Orleans
    type: :Woman
  AssignClass (5b821896-bbc7-46f7-a228-9f81cc329a8a)
 Call ID: 5b821896-bbc7-46f7-a228-9f81cc329a8a
  Args:
    type: :Person
    source: :Princess_Marie_Isabelle_of_Orleans
  AddTriple (a8e6cfea-ce00-4afd-8ce1-b660f7220f8d)
 Call ID: a8e6cfea-ce00-4afd-8ce1-b660f7220f8d
  Args:
    relation: :hasFather
    source: :Princess_Helene
    target: :Prince_Philippe_of_Orleans
  AddTriple (822615d7-0891-421e-9d81-d6c695629957)
 Call ID: 822615d7-0891-421e-9d81-d6c695629957
  Args:
    source: :Princess_Helene
    relation: :hasMother
    target: :Princess_Marie_Isabelle_of_Orleans
  AssignClass (563d6751-4f7d-42c1-aca6-2ce5009c908e)
 Call ID: 563d6751-4f7d-42c1-aca6-2ce5009c908e
  Args:
    source: :Aimone_4th_Duke_of_Aosta
    type: :Man
  AssignClass (27c24b27-9d11-4090-99dc-18ced76d4e9d)
 Call ID: 27c24b27-9d11-4090-99dc-18ced76d4e9d
  Args:
    source: :Aimone_4th_Duke_of_Aosta
    type: :Person
  AddTriple (5aac5bba-afc4-4b28-b37d-d0243b675230)
 Call ID: 5aac5bba-afc4-4b28-b37d-d0243b675230
  Args:
    source: :Amedeo_3rd_Duke_of_Aosta
    relation: :hasBrother
    target: :Aimone_4th_Duke_of_Aosta
  AssignClass (3019a450-b527-4ae8-84c3-9b4495585445)
 Call ID: 3019a450-b527-4ae8-84c3-9b4495585445
  Args:
    type: :Woman
    source: :Princess_Anne_of_Orleans
  AssignClass (03841208-a7e0-4c17-8954-5d8f04cc1e79)
 Call ID: 03841208-a7e0-4c17-8954-5d8f04cc1e79
  Args:
    source: :Princess_Anne_of_Orleans
    type: :Person
  AddTriple (57c0293f-44cb-4732-b80e-ea4e0fc7d557)
 Call ID: 57c0293f-44cb-4732-b80e-ea4e0fc7d557
  Args:
    relation: :hasRelation
    source: :Amedeo_3rd_Duke_of_Aosta
    target: :Princess_Anne_of_Orleans
  AddLiteral (bd279494-cb50-49e1-b433-ecc05544ea18)
 Call ID: bd279494-cb50-49e1-b433-ecc05544ea18
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 1927
    source: :Amedeo_3rd_Duke_of_Aosta
  AssignClass (5a11dab3-2945-495c-8c3a-689e7e7d7c2e)
 Call ID: 5a11dab3-2945-495c-8c3a-689e7e7d7c2e
  Args:
    source: :Prince_Jean_Duke_of_Guise
    type: :Man
  AssignClass (54bf8af1-b9ec-4e01-8f2d-6f2cd1ba3d90)
 Call ID: 54bf8af1-b9ec-4e01-8f2d-6f2cd1ba3d90
  Args:
    source: :Prince_Jean_Duke_of_Guise
    type: :Person
  AssignClass (b6f25b29-b1e2-4310-b992-70f1e7a99eec)
 Call ID: b6f25b29-b1e2-4310-b992-70f1e7a99eec
  Args:
    type: :Woman
    source: :Princess_Isabelle_of_Orleans
  AssignClass (8613c6b7-0508-4de7-8f28-889242941c23)
 Call ID: 8613c6b7-0508-4de7-8f28-889242941c23
  Args:
    type: :Person
    source: :Princess_Isabelle_of_Orleans
  AddTriple (2e6b77ee-c9bd-436e-9b76-04d71ee27584)
 Call ID: 2e6b77ee-c9bd-436e-9b76-04d71ee27584
  Args:
    relation: :hasFather
    source: :Princess_Anne_of_Orleans
    target: :Prince_Jean_Duke_of_Guise
  AddTriple (93a84f7f-9ae7-4552-81c6-d07e2d90b862)
 Call ID: 93a84f7f-9ae7-4552-81c6-d07e2d90b862
  Args:
    target: :Princess_Isabelle_of_Orleans
    relation: :hasMother
    source: :Princess_Anne_of_Orleans
  Finish (de57cc1f-7bb9-43b0-bc4e-860964bc6161)
 Call ID: de57cc1f-7bb9-43b0-bc4e-860964bc6161
  Args: