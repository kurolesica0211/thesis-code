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
  AssignClass (ab40ff74-7870-4f2f-ac6d-15dc0341a267)
 Call ID: ab40ff74-7870-4f2f-ac6d-15dc0341a267
  Args:
    type: :Man
    source: Prince_Amedeo_3rd_Duke_of_Aosta
  AssignClass (8ff29712-7109-4919-a07d-1a97880feb60)
 Call ID: 8ff29712-7109-4919-a07d-1a97880feb60
  Args:
    type: :Person
    source: Prince_Amedeo_3rd_Duke_of_Aosta
  AddLiteral (eccd8ffa-b20e-4158-b885-97a19418021f)
 Call ID: eccd8ffa-b20e-4158-b885-97a19418021f
  Args:
    source: Prince_Amedeo_3rd_Duke_of_Aosta
    relation: :hasBirthYear
    literal_value: 1898
    literal_type: xsd:integer
  AddLiteral (d4f1b1bd-8aee-4e0c-87da-f3927a7cf91b)
 Call ID: d4f1b1bd-8aee-4e0c-87da-f3927a7cf91b
  Args:
    relation: :hasDeathYear
    source: Prince_Amedeo_3rd_Duke_of_Aosta
    literal_type: xsd:integer
    literal_value: 1942
  AssignClass (a8ddca7a-1162-4cb3-b3b3-47751bc9e91a)
 Call ID: a8ddca7a-1162-4cb3-b3b3-47751bc9e91a
  Args:
    source: Prince_Emanuele_Filiberto_2nd_Duke_of_Aosta
    type: :Man
  AssignClass (a3239019-0215-4554-a6c4-d28fcc44f275)
 Call ID: a3239019-0215-4554-a6c4-d28fcc44f275
  Args:
    source: Prince_Emanuele_Filiberto_2nd_Duke_of_Aosta
    type: :Person
  AssignClass (e2e1b5bc-b8bd-4675-8eab-f6db7c30dd45)
 Call ID: e2e1b5bc-b8bd-4675-8eab-f6db7c30dd45
  Args:
    type: :Woman
    source: Princess_Helene
  AssignClass (f3cbf825-f2ca-4209-95af-5f61ced0cc69)
 Call ID: f3cbf825-f2ca-4209-95af-5f61ced0cc69
  Args:
    source: Princess_Helene
    type: :Person
  AddTriple (dabff519-2889-43f7-bbc3-a6f0c18c2647)
 Call ID: dabff519-2889-43f7-bbc3-a6f0c18c2647
  Args:
    target: Prince_Emanuele_Filiberto_2nd_Duke_of_Aosta
    relation: :hasFather
    source: Prince_Amedeo_3rd_Duke_of_Aosta
  AddTriple (dc7affb9-e316-4200-bd87-761cd6676a77)
 Call ID: dc7affb9-e316-4200-bd87-761cd6676a77
  Args:
    source: Prince_Amedeo_3rd_Duke_of_Aosta
    relation: :hasMother
    target: Princess_Helene
  AssignClass (a939c871-b55e-4280-86c8-8604fefb9749)
 Call ID: a939c871-b55e-4280-86c8-8604fefb9749
  Args:
    type: :Man
    source: Amadeo_I_of_Spain
  AssignClass (609c51da-5ac3-4374-9993-6543df3e4a35)
 Call ID: 609c51da-5ac3-4374-9993-6543df3e4a35
  Args:
    source: Amadeo_I_of_Spain
    type: :Person
  AssignClass (c3d0b5c7-eb13-400f-be00-220283ecc189)
 Call ID: c3d0b5c7-eb13-400f-be00-220283ecc189
  Args:
    type: :Woman
    source: Princess_Maria_Vittoria
  AssignClass (4e513522-c411-490f-859d-18d79effcc83)
 Call ID: 4e513522-c411-490f-859d-18d79effcc83
  Args:
    type: :Person
    source: Princess_Maria_Vittoria
  AddTriple (698c0fac-419b-4627-929e-543e2414098a)
 Call ID: 698c0fac-419b-4627-929e-543e2414098a
  Args:
    relation: :hasFather
    source: Prince_Emanuele_Filiberto_2nd_Duke_of_Aosta
    target: Amadeo_I_of_Spain
  AddTriple (3dd4f2a8-ef18-4ea6-8837-c59e459adb52)
 Call ID: 3dd4f2a8-ef18-4ea6-8837-c59e459adb52
  Args:
    target: Princess_Maria_Vittoria
    source: Prince_Emanuele_Filiberto_2nd_Duke_of_Aosta
    relation: :hasMother
  AssignClass (c1be6182-dc84-4b1c-952f-8600abb7a6cd)
 Call ID: c1be6182-dc84-4b1c-952f-8600abb7a6cd
  Args:
    type: :Man
    source: Prince_Philippe_of_Orleans
  AssignClass (064b479a-d12c-4459-8753-081273de71a8)
 Call ID: 064b479a-d12c-4459-8753-081273de71a8
  Args:
    type: :Person
    source: Prince_Philippe_of_Orleans
  AssignClass (0f1e680a-e09b-47cf-8d20-7d66fcc8f9a3)
 Call ID: 0f1e680a-e09b-47cf-8d20-7d66fcc8f9a3
  Args:
    type: :Woman
    source: Princess_Marie_Isabelle_of_Orleans
  AssignClass (0853f14d-2065-4683-bc3e-c6182c0f9b53)
 Call ID: 0853f14d-2065-4683-bc3e-c6182c0f9b53
  Args:
    type: :Person
    source: Princess_Marie_Isabelle_of_Orleans
  AddTriple (911d836c-a707-43be-81c7-a7741b7376af)
 Call ID: 911d836c-a707-43be-81c7-a7741b7376af
  Args:
    source: Princess_Helene
    relation: :hasFather
    target: Prince_Philippe_of_Orleans
  AddTriple (98b182f5-6bbb-48c3-b261-124f8575688c)
 Call ID: 98b182f5-6bbb-48c3-b261-124f8575688c
  Args:
    target: Princess_Marie_Isabelle_of_Orleans
    source: Princess_Helene
    relation: :hasMother
  AssignClass (51792ea1-1b1b-400d-871b-2a91fb1a3079)
 Call ID: 51792ea1-1b1b-400d-871b-2a91fb1a3079
  Args:
    source: Aimone_4th_Duke_of_Aosta
    type: :Man
  AssignClass (6894410e-8178-4e5b-8f09-d79c0fe5f4e9)
 Call ID: 6894410e-8178-4e5b-8f09-d79c0fe5f4e9
  Args:
    source: Aimone_4th_Duke_of_Aosta
    type: :Person
  AddTriple (d0611c2f-0c6a-4c22-b195-c4e0661523b2)
 Call ID: d0611c2f-0c6a-4c22-b195-c4e0661523b2
  Args:
    source: Aimone_4th_Duke_of_Aosta
    relation: :isBrotherOf
    target: Prince_Amedeo_3rd_Duke_of_Aosta
  AssignClass (e21f9ed7-75e9-4b58-8087-8852dfb2d9af)
 Call ID: e21f9ed7-75e9-4b58-8087-8852dfb2d9af
  Args:
    type: :Woman
    source: Princess_Anne_of_Orleans
  AssignClass (ced97761-2e7b-47bc-8f3a-d97d70de8f49)
 Call ID: ced97761-2e7b-47bc-8f3a-d97d70de8f49
  Args:
    type: :Person
    source: Princess_Anne_of_Orleans
  AddTriple (5a0c8525-6ca2-4a26-a866-8c735b8b1736)
 Call ID: 5a0c8525-6ca2-4a26-a866-8c735b8b1736
  Args:
    relation: :hasRelation
    source: Prince_Amedeo_3rd_Duke_of_Aosta
    target: Princess_Anne_of_Orleans
  AddLiteral (6dbdddf4-8ac0-47fd-a5bf-20de20dd8049)
 Call ID: 6dbdddf4-8ac0-47fd-a5bf-20de20dd8049
  Args:
    relation: :hasMarriageYear
    source: Prince_Amedeo_3rd_Duke_of_Aosta
    literal_type: xsd:integer
    literal_value: 1927
  AssignClass (0e74d33b-e648-4b01-87d2-e429d1ca9cd9)
 Call ID: 0e74d33b-e648-4b01-87d2-e429d1ca9cd9
  Args:
    source: Prince_Jean_Duke_of_Guise
    type: :Man
  AssignClass (5b05cbfc-7c1a-4932-bd00-5e020a1950d7)
 Call ID: 5b05cbfc-7c1a-4932-bd00-5e020a1950d7
  Args:
    source: Prince_Jean_Duke_of_Guise
    type: :Person
  AssignClass (f18a139a-d4d3-4cfe-be9e-301e4da1e071)
 Call ID: f18a139a-d4d3-4cfe-be9e-301e4da1e071
  Args:
    type: :Woman
    source: Princess_Isabelle_of_Orleans
  AssignClass (f3ad4916-319e-4eda-b1c2-a6bb1e2f8263)
 Call ID: f3ad4916-319e-4eda-b1c2-a6bb1e2f8263
  Args:
    source: Princess_Isabelle_of_Orleans
    type: :Person
  AddTriple (d6e450e4-c7fe-4394-83d5-91cdb1cc7272)
 Call ID: d6e450e4-c7fe-4394-83d5-91cdb1cc7272
  Args:
    target: Prince_Jean_Duke_of_Guise
    source: Princess_Anne_of_Orleans
    relation: :hasFather
  AddTriple (beea984d-03e5-41e7-b97c-5850cada3659)
 Call ID: beea984d-03e5-41e7-b97c-5850cada3659
  Args:
    target: Princess_Isabelle_of_Orleans
    source: Princess_Anne_of_Orleans
    relation: :hasMother
  Finish (31c48103-e2f9-45ef-b8db-82b632ddbda1)
 Call ID: 31c48103-e2f9-45ef-b8db-82b632ddbda1
  Args: