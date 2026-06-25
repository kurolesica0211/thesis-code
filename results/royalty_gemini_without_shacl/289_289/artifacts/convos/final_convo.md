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
  AssignClass (34501b35-1413-4a1d-866b-de7affaaa2db)
 Call ID: 34501b35-1413-4a1d-866b-de7affaaa2db
  Args:
    type: :Man
    source: :Prince_Amedeo_3rd_Duke_of_Aosta
  AssignClass (993b2e6b-64fc-4a7d-951b-d1d43e650203)
 Call ID: 993b2e6b-64fc-4a7d-951b-d1d43e650203
  Args:
    source: :Prince_Amedeo_3rd_Duke_of_Aosta
    type: :Person
  AddLiteral (64a7b9c3-b2fa-4bdd-be53-81f271f2c40d)
 Call ID: 64a7b9c3-b2fa-4bdd-be53-81f271f2c40d
  Args:
    relation: :hasBirthYear
    source: :Prince_Amedeo_3rd_Duke_of_Aosta
    literal_value: 1898
    literal_type: xsd:integer
  AddLiteral (9175d366-cb46-4c09-8395-d186a734f03c)
 Call ID: 9175d366-cb46-4c09-8395-d186a734f03c
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1942
    source: :Prince_Amedeo_3rd_Duke_of_Aosta
  AssignClass (73517092-0a02-4822-939a-00815f3dfb77)
 Call ID: 73517092-0a02-4822-939a-00815f3dfb77
  Args:
    type: :Man
    source: :Prince_Emanuele_Filiberto_2nd_Duke_of_Aosta
  AssignClass (bb3e2ca3-5b9f-4df5-a96c-3d172220ea3e)
 Call ID: bb3e2ca3-5b9f-4df5-a96c-3d172220ea3e
  Args:
    type: :Person
    source: :Prince_Emanuele_Filiberto_2nd_Duke_of_Aosta
  AddTriple (d5d51638-e3ed-48bd-a2ea-32e2d76dd075)
 Call ID: d5d51638-e3ed-48bd-a2ea-32e2d76dd075
  Args:
    source: :Prince_Amedeo_3rd_Duke_of_Aosta
    relation: :hasFather
    target: :Prince_Emanuele_Filiberto_2nd_Duke_of_Aosta
  AssignClass (71e52ff6-fe30-40fd-866c-e7ab4a3307a1)
 Call ID: 71e52ff6-fe30-40fd-866c-e7ab4a3307a1
  Args:
    source: :Princess_Helene
    type: :Woman
  AssignClass (f0105dc3-d009-482d-9d02-63938042ea64)
 Call ID: f0105dc3-d009-482d-9d02-63938042ea64
  Args:
    source: :Princess_Helene
    type: :Person
  AddTriple (a3d26eac-01f2-41bb-97d2-83615aa4ba42)
 Call ID: a3d26eac-01f2-41bb-97d2-83615aa4ba42
  Args:
    target: :Princess_Helene
    relation: :hasMother
    source: :Prince_Amedeo_3rd_Duke_of_Aosta
  AssignClass (4516ebac-4faf-41d3-8d85-ef54483a2fe5)
 Call ID: 4516ebac-4faf-41d3-8d85-ef54483a2fe5
  Args:
    type: :Man
    source: :Amadeo_I_of_Spain
  AssignClass (d41ede2b-9105-4dca-b6fe-736bb9d69ce5)
 Call ID: d41ede2b-9105-4dca-b6fe-736bb9d69ce5
  Args:
    type: :Person
    source: :Amadeo_I_of_Spain
  AddTriple (4e6ad5ef-adbb-4c47-ac85-ec14d238d392)
 Call ID: 4e6ad5ef-adbb-4c47-ac85-ec14d238d392
  Args:
    relation: :hasFather
    source: :Prince_Emanuele_Filiberto_2nd_Duke_of_Aosta
    target: :Amadeo_I_of_Spain
  AssignClass (6be4e867-59dc-4718-b758-b9a383a0b91d)
 Call ID: 6be4e867-59dc-4718-b758-b9a383a0b91d
  Args:
    type: :Woman
    source: :Princess_Maria_Vittoria
  AssignClass (d20f507b-acb7-43ee-8451-1fc5a5d13b38)
 Call ID: d20f507b-acb7-43ee-8451-1fc5a5d13b38
  Args:
    type: :Person
    source: :Princess_Maria_Vittoria
  AddTriple (b85e6b4a-9476-4ab1-a307-aa279687c835)
 Call ID: b85e6b4a-9476-4ab1-a307-aa279687c835
  Args:
    target: :Princess_Maria_Vittoria
    relation: :hasMother
    source: :Prince_Emanuele_Filiberto_2nd_Duke_of_Aosta
  AssignClass (289b3ad2-9678-4079-adbe-7e3aadbff8f7)
 Call ID: 289b3ad2-9678-4079-adbe-7e3aadbff8f7
  Args:
    type: :Man
    source: :Prince_Philippe_of_Orleans
  AssignClass (bfd3c9e0-d099-49b5-94d5-7e5345ecb08f)
 Call ID: bfd3c9e0-d099-49b5-94d5-7e5345ecb08f
  Args:
    type: :Person
    source: :Prince_Philippe_of_Orleans
  AddTriple (bb3ae301-1da1-438b-a76f-cdb2c5b00302)
 Call ID: bb3ae301-1da1-438b-a76f-cdb2c5b00302
  Args:
    target: :Prince_Philippe_of_Orleans
    source: :Princess_Helene
    relation: :hasFather
  AssignClass (327b121f-a37e-4b8c-a64d-f510ffb2ecfa)
 Call ID: 327b121f-a37e-4b8c-a64d-f510ffb2ecfa
  Args:
    source: :Princess_Marie_Isabelle_of_Orleans
    type: :Woman
  AssignClass (348ea4c5-5661-4c67-a505-17b780b4c1b2)
 Call ID: 348ea4c5-5661-4c67-a505-17b780b4c1b2
  Args:
    source: :Princess_Marie_Isabelle_of_Orleans
    type: :Person
  AddTriple (93fe42af-d224-4d92-9743-51c3d474ac15)
 Call ID: 93fe42af-d224-4d92-9743-51c3d474ac15
  Args:
    source: :Princess_Helene
    relation: :hasMother
    target: :Princess_Marie_Isabelle_of_Orleans
  AssignClass (7ec61742-5ff8-430e-906f-cee4e799cd83)
 Call ID: 7ec61742-5ff8-430e-906f-cee4e799cd83
  Args:
    source: :Aimone_4th_Duke_of_Aosta
    type: :Man
  AssignClass (2e596ad8-cd96-4d0c-9f74-b278eb6c3296)
 Call ID: 2e596ad8-cd96-4d0c-9f74-b278eb6c3296
  Args:
    type: :Person
    source: :Aimone_4th_Duke_of_Aosta
  AddTriple (43aabaff-8238-4658-a65f-523c668323ca)
 Call ID: 43aabaff-8238-4658-a65f-523c668323ca
  Args:
    relation: :isBrotherOf
    source: :Aimone_4th_Duke_of_Aosta
    target: :Prince_Amedeo_3rd_Duke_of_Aosta
  AssignClass (deec44a5-8ca6-4359-9d58-69a556d45ad7)
 Call ID: deec44a5-8ca6-4359-9d58-69a556d45ad7
  Args:
    source: :Princess_Anne_of_Orleans
    type: :Woman
  AssignClass (64894bd3-5fbf-4d4c-8a8e-f456d6065e2f)
 Call ID: 64894bd3-5fbf-4d4c-8a8e-f456d6065e2f
  Args:
    source: :Princess_Anne_of_Orleans
    type: :Person
  AddTriple (257a6cce-310c-43f7-bb3d-79573b0a1df2)
 Call ID: 257a6cce-310c-43f7-bb3d-79573b0a1df2
  Args:
    source: :Prince_Amedeo_3rd_Duke_of_Aosta
    relation: :hasRelation
    target: :Princess_Anne_of_Orleans
  AddLiteral (5fd823a2-2306-4742-bc8d-e8bd2cb88819)
 Call ID: 5fd823a2-2306-4742-bc8d-e8bd2cb88819
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 1927
    source: :Prince_Amedeo_3rd_Duke_of_Aosta
  AssignClass (b0c0a167-a37d-40c5-b7ae-ee4d6b3447a6)
 Call ID: b0c0a167-a37d-40c5-b7ae-ee4d6b3447a6
  Args:
    source: :Prince_Jean_Duke_of_Guise
    type: :Man
  AssignClass (237fde1f-8cb6-4c16-8ae4-f66caa2c130a)
 Call ID: 237fde1f-8cb6-4c16-8ae4-f66caa2c130a
  Args:
    source: :Prince_Jean_Duke_of_Guise
    type: :Person
  AddTriple (6f095a05-5dfa-49cb-89a1-8fe4c6f7cbd2)
 Call ID: 6f095a05-5dfa-49cb-89a1-8fe4c6f7cbd2
  Args:
    target: :Prince_Jean_Duke_of_Guise
    relation: :hasFather
    source: :Princess_Anne_of_Orleans
  AssignClass (ebdcde1d-5ba8-4d4e-b447-8aec335da521)
 Call ID: ebdcde1d-5ba8-4d4e-b447-8aec335da521
  Args:
    source: :Princess_Isabelle_of_Orleans
    type: :Woman
  AssignClass (758b2723-51ba-40bd-a2e0-1737decaaa3e)
 Call ID: 758b2723-51ba-40bd-a2e0-1737decaaa3e
  Args:
    source: :Princess_Isabelle_of_Orleans
    type: :Person
  AddTriple (a2a4f45a-5d4c-458a-a05f-65a833a63046)
 Call ID: a2a4f45a-5d4c-458a-a05f-65a833a63046
  Args:
    relation: :hasMother
    source: :Princess_Anne_of_Orleans
    target: :Princess_Isabelle_of_Orleans
  Finish (0bdb3b8c-8cd2-48d3-bd82-90ff8a65821f)
 Call ID: 0bdb3b8c-8cd2-48d3-bd82-90ff8a65821f
  Args: