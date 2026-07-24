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
  AssignClass (02481a8f-7ed2-4249-b91f-ca7dd4ae3cfe)
 Call ID: 02481a8f-7ed2-4249-b91f-ca7dd4ae3cfe
  Args:
    source: Oskar_Prince_of_Prussia
    type: :Man
  AssignClass (dba97914-58e8-4133-ae3f-3356edb53ef2)
 Call ID: dba97914-58e8-4133-ae3f-3356edb53ef2
  Args:
    source: Oskar_Prince_of_Prussia
    type: :Person
  AddLiteral (c19b297f-422d-4759-9044-1650b65587ac)
 Call ID: c19b297f-422d-4759-9044-1650b65587ac
  Args:
    literal_type: xsd:date
    relation: :hasBirthYear
    source: Oskar_Prince_of_Prussia
    literal_value: 1888-07-27
  AddLiteral (9a24330a-087b-4745-a455-5c8296b692be)
 Call ID: 9a24330a-087b-4745-a455-5c8296b692be
  Args:
    relation: :hasDeathYear
    source: Oskar_Prince_of_Prussia
    literal_value: 1958-01-27
    literal_type: xsd:date
  AssignClass (9cb8a15e-bb7a-44c6-bdde-2d4d09a9e180)
 Call ID: 9cb8a15e-bb7a-44c6-bdde-2d4d09a9e180
  Args:
    type: :Man
    source: Wilhelm_II
  AssignClass (52d757fd-260b-4eb4-bea9-cbc97c13e605)
 Call ID: 52d757fd-260b-4eb4-bea9-cbc97c13e605
  Args:
    type: :Person
    source: Wilhelm_II
  AssignClass (40535ee9-f2e4-4ed5-917b-16509ea0cbc7)
 Call ID: 40535ee9-f2e4-4ed5-917b-16509ea0cbc7
  Args:
    type: :Woman
    source: Augusta_Victoria_of_Schleswig-Holstein
  AssignClass (f272bac6-67e2-462b-a96f-d06f09aa7d59)
 Call ID: f272bac6-67e2-462b-a96f-d06f09aa7d59
  Args:
    type: :Person
    source: Augusta_Victoria_of_Schleswig-Holstein
  AddTriple (0ee9e888-0231-4d24-89c3-07b1d6b73724)
 Call ID: 0ee9e888-0231-4d24-89c3-07b1d6b73724
  Args:
    source: Oskar_Prince_of_Prussia
    target: Wilhelm_II
    relation: :hasFather
  AddTriple (182e3dd2-417b-4028-8e52-a2ffe797b267)
 Call ID: 182e3dd2-417b-4028-8e52-a2ffe797b267
  Args:
    target: Augusta_Victoria_of_Schleswig-Holstein
    source: Oskar_Prince_of_Prussia
    relation: :hasMother
  AssignClass (87ba8598-800a-4885-8368-8e73b03de340)
 Call ID: 87ba8598-800a-4885-8368-8e73b03de340
  Args:
    type: :Man
    source: Crown_Prince_Wilhelm
  AssignClass (16dd0fc1-2a1e-4840-9da0-ae240f6b50c2)
 Call ID: 16dd0fc1-2a1e-4840-9da0-ae240f6b50c2
  Args:
    type: :Person
    source: Crown_Prince_Wilhelm
  AssignClass (770224be-97b2-4822-9aed-d93dcb8b4594)
 Call ID: 770224be-97b2-4822-9aed-d93dcb8b4594
  Args:
    type: :Man
    source: Prince_Eitel_Friedrich
  AssignClass (e64f7768-f6ff-4f60-abb3-c682e37b2e8c)
 Call ID: e64f7768-f6ff-4f60-abb3-c682e37b2e8c
  Args:
    type: :Person
    source: Prince_Eitel_Friedrich
  AssignClass (418d9f01-0eb8-4957-8b4c-72bc6e89a451)
 Call ID: 418d9f01-0eb8-4957-8b4c-72bc6e89a451
  Args:
    type: :Man
    source: Prince_Adalbert
  AssignClass (166eac8e-227a-4397-a101-f6f26ebee5eb)
 Call ID: 166eac8e-227a-4397-a101-f6f26ebee5eb
  Args:
    source: Prince_Adalbert
    type: :Person
  AssignClass (daa83515-acf9-42f8-8ebb-03919e9973d6)
 Call ID: daa83515-acf9-42f8-8ebb-03919e9973d6
  Args:
    source: Prince_August_Wilhelm
    type: :Man
  AssignClass (f70ed062-a1c6-4647-aec6-51b7ad8c8317)
 Call ID: f70ed062-a1c6-4647-aec6-51b7ad8c8317
  Args:
    source: Prince_August_Wilhelm
    type: :Person
  AssignClass (6a8c9b2b-046c-466e-8e6e-180c7fb68cd2)
 Call ID: 6a8c9b2b-046c-466e-8e6e-180c7fb68cd2
  Args:
    source: Prince_Joachim
    type: :Man
  AssignClass (42d81e5a-8573-4446-9f5c-7dfe5a8b2a19)
 Call ID: 42d81e5a-8573-4446-9f5c-7dfe5a8b2a19
  Args:
    source: Prince_Joachim
    type: :Person
  AssignClass (73ffed7b-00dd-454f-a70e-d4a8f3ab8325)
 Call ID: 73ffed7b-00dd-454f-a70e-d4a8f3ab8325
  Args:
    source: Princess_Viktoria_Luise
    type: :Woman
  AssignClass (c42bcf05-8b38-4884-a924-bc5551ae10cd)
 Call ID: c42bcf05-8b38-4884-a924-bc5551ae10cd
  Args:
    source: Princess_Viktoria_Luise
    type: :Person
  AddTriple (cbfb0890-263f-4c22-a583-e11cb1272335)
 Call ID: cbfb0890-263f-4c22-a583-e11cb1272335
  Args:
    source: Oskar_Prince_of_Prussia
    target: Crown_Prince_Wilhelm
    relation: :hasBrother
  AddTriple (e7ccd580-ac61-48dc-a23b-5adba43a580b)
 Call ID: e7ccd580-ac61-48dc-a23b-5adba43a580b
  Args:
    relation: :hasBrother
    target: Prince_Eitel_Friedrich
    source: Oskar_Prince_of_Prussia
  AddTriple (56b58279-28a5-421b-ac68-5d649e6c5d9f)
 Call ID: 56b58279-28a5-421b-ac68-5d649e6c5d9f
  Args:
    target: Prince_Adalbert
    source: Oskar_Prince_of_Prussia
    relation: :hasBrother
  AddTriple (f0c5bb1c-bd05-4707-9b89-a97608f26d49)
 Call ID: f0c5bb1c-bd05-4707-9b89-a97608f26d49
  Args:
    relation: :hasBrother
    target: Prince_August_Wilhelm
    source: Oskar_Prince_of_Prussia
  AddTriple (3043f3d4-315f-4954-b71f-25409622cd0e)
 Call ID: 3043f3d4-315f-4954-b71f-25409622cd0e
  Args:
    relation: :hasBrother
    target: Prince_Joachim
    source: Oskar_Prince_of_Prussia
  AddTriple (40d5841a-06d0-4dff-868a-9af5a38c4da6)
 Call ID: 40d5841a-06d0-4dff-868a-9af5a38c4da6
  Args:
    target: Princess_Viktoria_Luise
    source: Oskar_Prince_of_Prussia
    relation: :hasSister
  AssignClass (3ccbe58c-20ef-4bcc-bf07-74cc26253178)
 Call ID: 3ccbe58c-20ef-4bcc-bf07-74cc26253178
  Args:
    source: Ina-Marie_von_Bassewitz
    type: :Woman
  AssignClass (ed179979-c078-4f65-95dd-532525ec514e)
 Call ID: ed179979-c078-4f65-95dd-532525ec514e
  Args:
    source: Ina-Marie_von_Bassewitz
    type: :Person
  AddLiteral (d69d5c92-0b78-4535-8605-2310d5ce7cff)
 Call ID: d69d5c92-0b78-4535-8605-2310d5ce7cff
  Args:
    literal_type: xsd:date
    literal_value: 1914-07-31
    relation: :hasMarriageYear
    source: Oskar_Prince_of_Prussia
  AddTriple (6277ae62-61c5-402a-a517-213714c18570)
 Call ID: 6277ae62-61c5-402a-a517-213714c18570
  Args:
    target: Ina-Marie_von_Bassewitz
    source: Oskar_Prince_of_Prussia
    relation: :hasRelation
  AssignClass (8394a932-41d5-4cb4-a0e7-340807b49791)
 Call ID: 8394a932-41d5-4cb4-a0e7-340807b49791
  Args:
    type: :Man
    source: Oskar_Jr_son_of_Oskar
  AssignClass (63e42c1d-0f81-44ab-86f0-ea19d3693a27)
 Call ID: 63e42c1d-0f81-44ab-86f0-ea19d3693a27
  Args:
    type: :Person
    source: Oskar_Jr_son_of_Oskar
  AddTriple (b7466f6b-7871-4c04-8416-75b55c129e41)
 Call ID: b7466f6b-7871-4c04-8416-75b55c129e41
  Args:
    relation: :hasSon
    source: Oskar_Prince_of_Prussia
    target: Oskar_Jr_son_of_Oskar
  AssignClass (f9e3c275-8149-44c0-a325-92fe81ac1e3d)
 Call ID: f9e3c275-8149-44c0-a325-92fe81ac1e3d
  Args:
    type: :Man
    source: Wilhelm_Karl_son_of_Oskar
  AssignClass (9f1d4b7d-2d92-4a14-8418-c833bcfcbf73)
 Call ID: 9f1d4b7d-2d92-4a14-8418-c833bcfcbf73
  Args:
    source: Wilhelm_Karl_son_of_Oskar
    type: :Person
  AddTriple (9796091f-1899-493b-9af4-7df209669e1d)
 Call ID: 9796091f-1899-493b-9af4-7df209669e1d
  Args:
    target: Wilhelm_Karl_son_of_Oskar
    source: Oskar_Prince_of_Prussia
    relation: :hasSon
  Finish (30c74fe0-59ab-450c-b6c6-da93ca81dbcd)
 Call ID: 30c74fe0-59ab-450c-b6c6-da93ca81dbcd
  Args: