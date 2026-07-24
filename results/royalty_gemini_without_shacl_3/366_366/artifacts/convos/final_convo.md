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
Oskar Karl Gustav Adolf Prince of Prussia (27 July 1888 – 27 January 1958) was the fifth son of German Emperor Wilhelm II and Augusta Victoria of Schleswig-Holstein-Sonderburg-Augustenburg.
Biography

Birth and family

Prinz Oskar of Prussia was born on 27 July 1888 at his parents' residence in the Marmorpalais of Potsdam in the Province of Brandenburg.
He was the fifth son of the German Emperor Wilhelm II, and his first wife, Princess Augusta Victoria of Schleswig-Holstein, and was born in the so-called Year of the Three Emperors, just a month after his 29-year-old father had become German Emperor and King of Prussia.
Prince Oskar had five brothers: Crown Prince Wilhelm, Prince Eitel Friedrich, Prince Adalbert, Prince August Wilhelm, Prince Joachim and one sister: Princess Viktoria Luise.
Education

Prince Oskar was educated as a cadet at the Prinzenhaus in Plön, in his mother's ancestral Schleswig-Holstein, as his brothers had been before him.
Military career

During the early months of the First World War, he commanded Grenadierregiment "König Wilhelm I." (2.
Future fighter ace Manfred von Richthofen witnessed the 22 August 1914, attack on Virton, Belgium, and wrote of Prinz Oskar's bravery and his inspirational leadership at the front of his regiment as they went into combat.
For this action, Oskar earned the Iron Cross, Second Class.
A month later, at Verdun, Oskar again led his men in a successful assault into heavy combat, and was awarded the Iron Cross, First Class.
In the early 1920s, his name was listed with other members of the general staff or the royal family accused of war crimes, and was condemned in the Press for applying for a colonel's pension from the Weimar Republic.
During the 1930s, when the Hohenzollern family attempted to test the waters for a return to power through Nationalist Socialism, Oskar appears to have played along, and eventually was commissioned at Generalmajor zur Verfügung (rank equivalent to brigadier general, "available for assignment"), circa 1 March 1940.
As the family fell out of favour with Hitler (with the exception of Oskar's middle brother, August Wilhelm), it became evident that there would be no restoration of the monarchy through the Nazis.
With the early battlefield deaths of Oskar's son (also named Oskar, killed in Poland, September 1939) and his nephew (Wilhelm, son of the Crown Prince, died of wounds received in France, May 1940)
the German people harboured a newfound sentiment for the royal family amidst the totalitarian regime that was Nazi Germany.
As a consequence, the majority of royals serving in the German Armed Forces appear to have had their commissions canceled, including Prinz Oskar.
Master of Knights, Protestant Order of Saint John

The Johanniterorden (The Order of Saint John (Bailiwick of Brandenburg)) was a favourite of the Hohenzollerns, historically, and of Prince Oskar's immediate family specifically.
His father and uncle were members, and his brother, Eitel Friedrich, served as its Master of Knights (Herrenmeister), from 1907 to 1926.
Prinz Oskar served as the thirty-fifth Master of Knights from Eitel Friedrich's resignation in 1926 until his death in 1958.
Modern historians credit Prinz Oskar for saving the ancient order from oblivion during the cultural purges of the Nazi regime.
It is from this struggle that he held his anti-Nazi sentiments.
After his death in 1958, his youngest son, Prinz Wilhelm Karl, became his permanent successor.
Prinz Oskar's grandson, to whom he is namesake, Dr. Oskar Hohenzollern, is the current (thirty-seventh) Master of Knights.
Marriage and issue

Prinz Oskar was married on 31 July 1914 to Countess Ina-Marie Helene Adele Elise von Bassewitz (27 January 1888 – 17 September 1973).
On 27 July 1914, prior to the wedding, Ina Marie was granted the title "Countess von Ruppin".
Both the civil and religious ceremonies took place at Schloß Bellevue near Berlin, Prussia.
Initially the union was a morganatic marriage, but on 3 November 1919 was decreed to be dynastic in accordance with the house laws of the Royal House of Hohenzollern.
Henceforth, from 21 June 1920, his wife was titled "Princess of Prussia" with the style Royal Highness.
The couple had four children:


Death

Prince Oskar, whose health declined during the final years of his life, died of stomach cancer in a clinic in Munich on 27 January 1958, on his wife's 70th birthday and what would have been his father's 99th birthday.
He was the last surviving son of Wilhelm II.



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
  AssignClass (826050ce-4f25-4f0d-9e11-e35ea975c4e4)
 Call ID: 826050ce-4f25-4f0d-9e11-e35ea975c4e4
  Args:
    source: Oskar_Prince_of_Prussia
    type: :Man
  AssignClass (cf44b76e-57dd-4513-abd8-0dae3363d708)
 Call ID: cf44b76e-57dd-4513-abd8-0dae3363d708
  Args:
    type: :Person
    source: Oskar_Prince_of_Prussia
  AddLiteral (580eada3-41a3-4c21-937a-4de9e3d535b4)
 Call ID: 580eada3-41a3-4c21-937a-4de9e3d535b4
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Oskar_Prince_of_Prussia
    literal_value: 1888
  AddLiteral (f234c07d-28db-4703-b128-ca93f37f60f2)
 Call ID: f234c07d-28db-4703-b128-ca93f37f60f2
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 1958
    source: Oskar_Prince_of_Prussia
  AssignClass (016c0caf-ce11-452a-b425-c0e9c585796e)
 Call ID: 016c0caf-ce11-452a-b425-c0e9c585796e
  Args:
    type: :Man
    source: Wilhelm_II
  AssignClass (da34a246-59ab-49b6-aae4-1a2fa3b23302)
 Call ID: da34a246-59ab-49b6-aae4-1a2fa3b23302
  Args:
    type: :Person
    source: Wilhelm_II
  AssignClass (aa742d4b-ccd6-4578-bd96-2312a6c4e463)
 Call ID: aa742d4b-ccd6-4578-bd96-2312a6c4e463
  Args:
    source: Augusta_Victoria_of_Schleswig-Holstein
    type: :Woman
  AssignClass (297b582a-efbe-470a-a49b-e542e0800b76)
 Call ID: 297b582a-efbe-470a-a49b-e542e0800b76
  Args:
    source: Augusta_Victoria_of_Schleswig-Holstein
    type: :Person
  AddTriple (62fadc36-0eaa-4a5c-8922-3c401d4b00c7)
 Call ID: 62fadc36-0eaa-4a5c-8922-3c401d4b00c7
  Args:
    target: Wilhelm_II
    source: Oskar_Prince_of_Prussia
    relation: :hasFather
  AddTriple (dc6aa68a-14e7-4964-90bb-bbf13c403ab7)
 Call ID: dc6aa68a-14e7-4964-90bb-bbf13c403ab7
  Args:
    source: Oskar_Prince_of_Prussia
    target: Augusta_Victoria_of_Schleswig-Holstein
    relation: :hasMother
  AssignClass (6d3c776f-d117-4ba6-aef3-1889702589bb)
 Call ID: 6d3c776f-d117-4ba6-aef3-1889702589bb
  Args:
    type: :Man
    source: Crown_Prince_Wilhelm
  AssignClass (9b4b00e8-167c-4fa5-932b-09d54c73c3b0)
 Call ID: 9b4b00e8-167c-4fa5-932b-09d54c73c3b0
  Args:
    type: :Person
    source: Crown_Prince_Wilhelm
  AssignClass (386005f7-c796-480a-8b0b-7a9b0969dad5)
 Call ID: 386005f7-c796-480a-8b0b-7a9b0969dad5
  Args:
    source: Prince_Eitel_Friedrich
    type: :Man
  AssignClass (07f96c39-3827-4340-80eb-63b7d6470ee6)
 Call ID: 07f96c39-3827-4340-80eb-63b7d6470ee6
  Args:
    source: Prince_Eitel_Friedrich
    type: :Person
  AssignClass (777a3e6b-fd85-4774-a6b6-4388ead137e6)
 Call ID: 777a3e6b-fd85-4774-a6b6-4388ead137e6
  Args:
    type: :Man
    source: Prince_Adalbert
  AssignClass (83f1e1b0-b98d-47b5-ab27-528782167316)
 Call ID: 83f1e1b0-b98d-47b5-ab27-528782167316
  Args:
    source: Prince_Adalbert
    type: :Person
  AssignClass (4bb7673a-0e1b-4038-ac9f-10f81d7cc5fa)
 Call ID: 4bb7673a-0e1b-4038-ac9f-10f81d7cc5fa
  Args:
    type: :Man
    source: Prince_August_Wilhelm
  AssignClass (84887770-cb09-4982-a42a-dd0355772cbe)
 Call ID: 84887770-cb09-4982-a42a-dd0355772cbe
  Args:
    type: :Person
    source: Prince_August_Wilhelm
  AssignClass (1aff2ca6-68a6-418d-93ae-1b1936708d52)
 Call ID: 1aff2ca6-68a6-418d-93ae-1b1936708d52
  Args:
    source: Prince_Joachim
    type: :Man
  AssignClass (613b7418-357b-4ede-8d1a-aa910a9043de)
 Call ID: 613b7418-357b-4ede-8d1a-aa910a9043de
  Args:
    type: :Person
    source: Prince_Joachim
  AssignClass (e15adadc-9a97-49fb-ad7e-fc3f6fb60175)
 Call ID: e15adadc-9a97-49fb-ad7e-fc3f6fb60175
  Args:
    source: Princess_Viktoria_Luise
    type: :Woman
  AssignClass (ba66dd68-9dbb-4408-be62-35488d60ffbe)
 Call ID: ba66dd68-9dbb-4408-be62-35488d60ffbe
  Args:
    type: :Person
    source: Princess_Viktoria_Luise
  AddTriple (a210aae7-e8a0-421c-a53e-b2a207d7e1c1)
 Call ID: a210aae7-e8a0-421c-a53e-b2a207d7e1c1
  Args:
    target: Crown_Prince_Wilhelm
    source: Oskar_Prince_of_Prussia
    relation: :isSiblingOf
  AddTriple (d754ccfb-7acf-4f2e-82fb-f00d565a2d6a)
 Call ID: d754ccfb-7acf-4f2e-82fb-f00d565a2d6a
  Args:
    source: Oskar_Prince_of_Prussia
    target: Prince_Eitel_Friedrich
    relation: :isSiblingOf
  AddTriple (0a9d668f-6c13-4389-8b1a-eb77372ad08b)
 Call ID: 0a9d668f-6c13-4389-8b1a-eb77372ad08b
  Args:
    target: Prince_Adalbert
    source: Oskar_Prince_of_Prussia
    relation: :isSiblingOf
  AddTriple (550a37fe-735c-4f0c-8051-d95fbc96a50b)
 Call ID: 550a37fe-735c-4f0c-8051-d95fbc96a50b
  Args:
    source: Oskar_Prince_of_Prussia
    target: Prince_August_Wilhelm
    relation: :isSiblingOf
  AddTriple (923498f0-ce2b-46b3-a30d-ba4b9652e192)
 Call ID: 923498f0-ce2b-46b3-a30d-ba4b9652e192
  Args:
    relation: :isSiblingOf
    source: Oskar_Prince_of_Prussia
    target: Prince_Joachim
  AddTriple (899a71d1-435c-4a1c-aa7f-b6e7f0639b07)
 Call ID: 899a71d1-435c-4a1c-aa7f-b6e7f0639b07
  Args:
    source: Oskar_Prince_of_Prussia
    target: Princess_Viktoria_Luise
    relation: :isSiblingOf
  AssignClass (f263fa72-d170-4125-8f94-b6fc894f73a4)
 Call ID: f263fa72-d170-4125-8f94-b6fc894f73a4
  Args:
    source: Ina-Marie_von_Bassewitz
    type: :Woman
  AssignClass (d4510ac0-747c-4b6f-859e-0df1c150afaf)
 Call ID: d4510ac0-747c-4b6f-859e-0df1c150afaf
  Args:
    source: Ina-Marie_von_Bassewitz
    type: :Person
  AddLiteral (f3fb33b1-d3e0-425e-95f1-fcbbb6be9637)
 Call ID: f3fb33b1-d3e0-425e-95f1-fcbbb6be9637
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    source: Oskar_Prince_of_Prussia
    literal_value: 1914
  AddTriple (00fd8a41-8add-46e6-b70b-cd0bac903571)
 Call ID: 00fd8a41-8add-46e6-b70b-cd0bac903571
  Args:
    relation: :hasRelation
    target: Ina-Marie_von_Bassewitz
    source: Oskar_Prince_of_Prussia
  AssignClass (cee9c9bc-9a07-4688-bd1a-8ccae6213332)
 Call ID: cee9c9bc-9a07-4688-bd1a-8ccae6213332
  Args:
    type: :Man
    source: Oskar_son_of_Oskar
  AssignClass (2e136980-db21-4a36-bbda-776e66e7e826)
 Call ID: 2e136980-db21-4a36-bbda-776e66e7e826
  Args:
    type: :Person
    source: Oskar_son_of_Oskar
  AddTriple (33dd0ab6-3e05-42ce-b9e2-f631dbbb30fb)
 Call ID: 33dd0ab6-3e05-42ce-b9e2-f631dbbb30fb
  Args:
    relation: :isSonOf
    source: Oskar_son_of_Oskar
    target: Oskar_Prince_of_Prussia
  AssignClass (65b129d4-1321-4fb5-81b4-f3434b04d68a)
 Call ID: 65b129d4-1321-4fb5-81b4-f3434b04d68a
  Args:
    source: Wilhelm_Karl_son_of_Oskar
    type: :Man
  AssignClass (fc2bf536-05c4-4da0-8e74-b8217a5672da)
 Call ID: fc2bf536-05c4-4da0-8e74-b8217a5672da
  Args:
    type: :Person
    source: Wilhelm_Karl_son_of_Oskar
  AddTriple (c59f65f5-6767-4250-b2d7-fa42ec53181d)
 Call ID: c59f65f5-6767-4250-b2d7-fa42ec53181d
  Args:
    source: Wilhelm_Karl_son_of_Oskar
    target: Oskar_Prince_of_Prussia
    relation: :isSonOf
  AssignClass (5c71b5ce-c772-4735-bd22-1a6e37c97f8b)
 Call ID: 5c71b5ce-c772-4735-bd22-1a6e37c97f8b
  Args:
    type: :Man
    source: Dr_Oskar_Hohenzollern
  AssignClass (cb25217b-6b18-4c1f-bb3e-de34de3bca22)
 Call ID: cb25217b-6b18-4c1f-bb3e-de34de3bca22
  Args:
    type: :Person
    source: Dr_Oskar_Hohenzollern
  Finish (9897051e-1656-4e8d-b0d8-b2d5333704a0)
 Call ID: 9897051e-1656-4e8d-b0d8-b2d5333704a0
  Args: