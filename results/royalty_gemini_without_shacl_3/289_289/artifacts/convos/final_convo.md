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
  AssignClass (a8d7687f-afce-4640-91da-c98f76647a3e)
 Call ID: a8d7687f-afce-4640-91da-c98f76647a3e
  Args:
    type: :Man
    source: Amedeo_3rd_Duke_of_Aosta
  AssignClass (e39635f2-ea8a-48b3-92b5-159c74dd3938)
 Call ID: e39635f2-ea8a-48b3-92b5-159c74dd3938
  Args:
    type: :Person
    source: Amedeo_3rd_Duke_of_Aosta
  AddLiteral (2298cd40-b9ec-453b-8e80-8e9b65708d8a)
 Call ID: 2298cd40-b9ec-453b-8e80-8e9b65708d8a
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Amedeo_3rd_Duke_of_Aosta
    literal_value: 1898
  AddLiteral (cbfe5658-dee2-427d-8215-ab1d29b7d14d)
 Call ID: cbfe5658-dee2-427d-8215-ab1d29b7d14d
  Args:
    source: Amedeo_3rd_Duke_of_Aosta
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1942
  AssignClass (a3b6241c-73ae-498e-be98-c149b3b639f3)
 Call ID: a3b6241c-73ae-498e-be98-c149b3b639f3
  Args:
    type: :Man
    source: Prince_Emanuele_Filiberto_2nd_Duke_of_Aosta
  AssignClass (d7338b12-7794-48ac-93f1-080c8f262fed)
 Call ID: d7338b12-7794-48ac-93f1-080c8f262fed
  Args:
    type: :Person
    source: Prince_Emanuele_Filiberto_2nd_Duke_of_Aosta
  AssignClass (2ed9ca92-f133-45a9-aac5-5ad0e454f077)
 Call ID: 2ed9ca92-f133-45a9-aac5-5ad0e454f077
  Args:
    type: :Woman
    source: Princess_Helene
  AssignClass (fc901788-3ae2-4ee1-9638-774ede936101)
 Call ID: fc901788-3ae2-4ee1-9638-774ede936101
  Args:
    type: :Person
    source: Princess_Helene
  AddTriple (a9d4f5b8-d5f4-45a8-94ea-0933cbee6f35)
 Call ID: a9d4f5b8-d5f4-45a8-94ea-0933cbee6f35
  Args:
    relation: :hasFather
    source: Amedeo_3rd_Duke_of_Aosta
    target: Prince_Emanuele_Filiberto_2nd_Duke_of_Aosta
  AddTriple (28927d79-f376-4a44-bc2f-f467b885beed)
 Call ID: 28927d79-f376-4a44-bc2f-f467b885beed
  Args:
    source: Amedeo_3rd_Duke_of_Aosta
    relation: :hasMother
    target: Princess_Helene
  AssignClass (c24ae230-863d-45af-8ece-644bb4eef91b)
 Call ID: c24ae230-863d-45af-8ece-644bb4eef91b
  Args:
    type: :Man
    source: Amadeo_I_of_Spain
  AssignClass (12e0b5b0-6017-4a45-9e9e-aee4a9cba0dd)
 Call ID: 12e0b5b0-6017-4a45-9e9e-aee4a9cba0dd
  Args:
    type: :Person
    source: Amadeo_I_of_Spain
  AssignClass (969f914f-272d-482b-9728-feef34c2f170)
 Call ID: 969f914f-272d-482b-9728-feef34c2f170
  Args:
    type: :Woman
    source: Princess_Maria_Vittoria
  AssignClass (4a43c291-1b50-4471-a571-bbf57f5f3a7c)
 Call ID: 4a43c291-1b50-4471-a571-bbf57f5f3a7c
  Args:
    type: :Person
    source: Princess_Maria_Vittoria
  AddTriple (95937d91-f775-4494-ad81-df81ff3c2d0d)
 Call ID: 95937d91-f775-4494-ad81-df81ff3c2d0d
  Args:
    target: Amadeo_I_of_Spain
    source: Prince_Emanuele_Filiberto_2nd_Duke_of_Aosta
    relation: :hasFather
  AddTriple (ba265a0f-7033-4595-b1fb-73a7c71d4e2e)
 Call ID: ba265a0f-7033-4595-b1fb-73a7c71d4e2e
  Args:
    relation: :hasMother
    source: Prince_Emanuele_Filiberto_2nd_Duke_of_Aosta
    target: Princess_Maria_Vittoria
  AssignClass (1b9c0777-2557-4345-8f54-2f1dbe922559)
 Call ID: 1b9c0777-2557-4345-8f54-2f1dbe922559
  Args:
    type: :Man
    source: Prince_Philippe_of_Orleans
  AssignClass (95a75244-5f78-4b0c-bb43-7ae4847a7e4b)
 Call ID: 95a75244-5f78-4b0c-bb43-7ae4847a7e4b
  Args:
    type: :Person
    source: Prince_Philippe_of_Orleans
  AssignClass (932d8087-64d1-4fe1-a72f-3f6f631b87dc)
 Call ID: 932d8087-64d1-4fe1-a72f-3f6f631b87dc
  Args:
    type: :Woman
    source: Princess_Marie_Isabelle_of_Orleans
  AssignClass (928fcc51-2391-48e4-a1c6-34f692d6426c)
 Call ID: 928fcc51-2391-48e4-a1c6-34f692d6426c
  Args:
    type: :Person
    source: Princess_Marie_Isabelle_of_Orleans
  AddTriple (d56d7230-fed4-43b6-9aba-9f00c264f211)
 Call ID: d56d7230-fed4-43b6-9aba-9f00c264f211
  Args:
    target: Prince_Philippe_of_Orleans
    source: Princess_Helene
    relation: :hasFather
  AddTriple (a04b18c8-6b7c-45ad-b225-8df5e8154426)
 Call ID: a04b18c8-6b7c-45ad-b225-8df5e8154426
  Args:
    target: Princess_Marie_Isabelle_of_Orleans
    relation: :hasMother
    source: Princess_Helene
  AssignClass (d634ae34-4242-4506-a8ce-1174dc2b29a5)
 Call ID: d634ae34-4242-4506-a8ce-1174dc2b29a5
  Args:
    type: :Man
    source: Aimone_4th_Duke_of_Aosta
  AssignClass (f74a1ad1-5e4e-4a5e-9e02-799ca91c7ecd)
 Call ID: f74a1ad1-5e4e-4a5e-9e02-799ca91c7ecd
  Args:
    type: :Person
    source: Aimone_4th_Duke_of_Aosta
  AddTriple (9389150d-c8dc-42c0-bf69-0b4c25c71dd3)
 Call ID: 9389150d-c8dc-42c0-bf69-0b4c25c71dd3
  Args:
    source: Amedeo_3rd_Duke_of_Aosta
    relation: :hasBrother
    target: Aimone_4th_Duke_of_Aosta
  AssignClass (56b1712a-7ca0-4614-8d33-49bc6f67b3d5)
 Call ID: 56b1712a-7ca0-4614-8d33-49bc6f67b3d5
  Args:
    type: :Woman
    source: Princess_Anne_of_Orleans
  AssignClass (cee429fc-bc68-439c-bdcf-686ac461a8cd)
 Call ID: cee429fc-bc68-439c-bdcf-686ac461a8cd
  Args:
    type: :Person
    source: Princess_Anne_of_Orleans
  AddLiteral (6d90194a-fcd3-481f-9ec1-f17dcda271e9)
 Call ID: 6d90194a-fcd3-481f-9ec1-f17dcda271e9
  Args:
    literal_value: 1927
    source: Amedeo_3rd_Duke_of_Aosta
    relation: :hasMarriageYear
    literal_type: xsd:integer
  AddTriple (8447851d-8ef5-4600-a2cb-0da25c6d8cba)
 Call ID: 8447851d-8ef5-4600-a2cb-0da25c6d8cba
  Args:
    target: Princess_Anne_of_Orleans
    relation: :hasRelation
    source: Amedeo_3rd_Duke_of_Aosta
  AssignClass (e5ac1ac2-14d2-4918-97b0-8a7dd280eb25)
 Call ID: e5ac1ac2-14d2-4918-97b0-8a7dd280eb25
  Args:
    type: :Man
    source: Prince_Jean_Duke_of_Guise
  AssignClass (ee0a8252-1b28-406f-a2e2-8e93637cd524)
 Call ID: ee0a8252-1b28-406f-a2e2-8e93637cd524
  Args:
    type: :Person
    source: Prince_Jean_Duke_of_Guise
  AssignClass (fb1cd6a8-f9a6-4421-8626-1e96fd9d1b63)
 Call ID: fb1cd6a8-f9a6-4421-8626-1e96fd9d1b63
  Args:
    type: :Woman
    source: Princess_Isabelle_of_Orleans
  AssignClass (ad7fea7a-3909-4257-98fd-333e7d2404df)
 Call ID: ad7fea7a-3909-4257-98fd-333e7d2404df
  Args:
    type: :Person
    source: Princess_Isabelle_of_Orleans
  AddTriple (88fc9fc0-2f9b-4578-80ea-61a6f1db5c92)
 Call ID: 88fc9fc0-2f9b-4578-80ea-61a6f1db5c92
  Args:
    source: Princess_Anne_of_Orleans
    relation: :hasFather
    target: Prince_Jean_Duke_of_Guise
  AddTriple (93c15aeb-2f99-4ce7-9ee5-053306380d7f)
 Call ID: 93c15aeb-2f99-4ce7-9ee5-053306380d7f
  Args:
    target: Princess_Isabelle_of_Orleans
    source: Princess_Anne_of_Orleans
    relation: :hasMother
  Finish (d737afd9-f177-44cc-8b45-4d7a9c411b46)
 Call ID: d737afd9-f177-44cc-8b45-4d7a9c411b46
  Args: