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
  AssignClass (7640f06c-b899-4b4f-94ca-a6731f57eba9)
 Call ID: 7640f06c-b899-4b4f-94ca-a6731f57eba9
  Args:
    type: :Man
    source: Oskar_Prince_of_Prussia
  AssignClass (857c98ea-e928-4f90-b3e1-67649f5f59b0)
 Call ID: 857c98ea-e928-4f90-b3e1-67649f5f59b0
  Args:
    type: :Man
    source: Wilhelm_II
  AssignClass (e151e72d-1b9c-403e-82c2-4d2cd7007e83)
 Call ID: e151e72d-1b9c-403e-82c2-4d2cd7007e83
  Args:
    source: Augusta_Victoria_of_Schleswig-Holstein-Sonderburg-Augustenburg
    type: :Woman
  AddLiteral (a94550b1-c037-407f-ac1d-a7efe42e551b)
 Call ID: a94550b1-c037-407f-ac1d-a7efe42e551b
  Args:
    literal_value: 1888
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Oskar_Prince_of_Prussia
  AddLiteral (d17655a2-a9fa-48d0-81ae-47c94774eecf)
 Call ID: d17655a2-a9fa-48d0-81ae-47c94774eecf
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: Oskar_Prince_of_Prussia
    literal_value: 1958
  AddTriple (d4a176cf-c789-41ee-a983-da55eef4a884)
 Call ID: d4a176cf-c789-41ee-a983-da55eef4a884
  Args:
    target: Wilhelm_II
    relation: :hasFather
    source: Oskar_Prince_of_Prussia
  AddTriple (ddd6635a-b9d4-4459-94e9-4f275ef58527)
 Call ID: ddd6635a-b9d4-4459-94e9-4f275ef58527
  Args:
    relation: :hasMother
    source: Oskar_Prince_of_Prussia
    target: Augusta_Victoria_of_Schleswig-Holstein-Sonderburg-Augustenburg
  AssignClass (ba566e86-382d-4ecb-a9da-818eb625e838)
 Call ID: ba566e86-382d-4ecb-a9da-818eb625e838
  Args:
    source: Crown_Prince_Wilhelm
    type: :Man
  AssignClass (37a24786-85a5-4ff9-8995-f00abddc410e)
 Call ID: 37a24786-85a5-4ff9-8995-f00abddc410e
  Args:
    source: Prince_Eitel_Friedrich
    type: :Man
  AssignClass (276c85cf-dfab-4c32-a4ea-97a635152229)
 Call ID: 276c85cf-dfab-4c32-a4ea-97a635152229
  Args:
    type: :Man
    source: Prince_Adalbert
  AssignClass (48679b9d-f4f9-4183-ae42-599849c6c8fc)
 Call ID: 48679b9d-f4f9-4183-ae42-599849c6c8fc
  Args:
    source: Prince_August_Wilhelm
    type: :Man
  AssignClass (62671caa-cf8f-4f0a-b7f4-7a6b619cb1d6)
 Call ID: 62671caa-cf8f-4f0a-b7f4-7a6b619cb1d6
  Args:
    type: :Man
    source: Prince_Joachim
  AssignClass (1eb0102b-5472-4ffc-9890-f4723e80f44a)
 Call ID: 1eb0102b-5472-4ffc-9890-f4723e80f44a
  Args:
    source: Princess_Viktoria_Luise
    type: :Woman
  AddTriple (8865be16-af39-4a55-b2de-844fa6ec9ea0)
 Call ID: 8865be16-af39-4a55-b2de-844fa6ec9ea0
  Args:
    target: Crown_Prince_Wilhelm
    relation: :isSiblingOf
    source: Oskar_Prince_of_Prussia
  AddTriple (08df8a8c-47aa-43b0-a915-0a7c397dec95)
 Call ID: 08df8a8c-47aa-43b0-a915-0a7c397dec95
  Args:
    source: Oskar_Prince_of_Prussia
    relation: :isSiblingOf
    target: Prince_Eitel_Friedrich
  AddTriple (98fded8b-1ffc-49ce-aa21-3b9df2685b99)
 Call ID: 98fded8b-1ffc-49ce-aa21-3b9df2685b99
  Args:
    relation: :isSiblingOf
    source: Oskar_Prince_of_Prussia
    target: Prince_Adalbert
  AddTriple (d5bcdf02-000b-4098-8eb8-374f276ba0d6)
 Call ID: d5bcdf02-000b-4098-8eb8-374f276ba0d6
  Args:
    target: Prince_August_Wilhelm
    relation: :isSiblingOf
    source: Oskar_Prince_of_Prussia
  AddTriple (930a576a-eb26-4c54-ae55-66a74747b128)
 Call ID: 930a576a-eb26-4c54-ae55-66a74747b128
  Args:
    target: Prince_Joachim
    relation: :isSiblingOf
    source: Oskar_Prince_of_Prussia
  AddTriple (62794756-83bb-4d01-b096-9311079a95ad)
 Call ID: 62794756-83bb-4d01-b096-9311079a95ad
  Args:
    target: Princess_Viktoria_Luise
    source: Oskar_Prince_of_Prussia
    relation: :isSiblingOf
  AssignClass (4dece7ec-1d01-4b82-a7af-18fe9d68ce1a)
 Call ID: 4dece7ec-1d01-4b82-a7af-18fe9d68ce1a
  Args:
    type: :Man
    source: Oskar_son_of_Oskar
  AddTriple (849b887d-5266-4a65-a253-d32160635ab0)
 Call ID: 849b887d-5266-4a65-a253-d32160635ab0
  Args:
    source: Oskar_son_of_Oskar
    relation: :isSonOf
    target: Oskar_Prince_of_Prussia
  AssignClass (3d0dbe17-160a-43da-af9d-76e0c2507fbf)
 Call ID: 3d0dbe17-160a-43da-af9d-76e0c2507fbf
  Args:
    source: Prinz_Wilhelm_Karl
    type: :Man
  AddTriple (db41013d-361c-48a2-848c-c86350f87733)
 Call ID: db41013d-361c-48a2-848c-c86350f87733
  Args:
    target: Oskar_Prince_of_Prussia
    relation: :isSonOf
    source: Prinz_Wilhelm_Karl
  AssignClass (e8b3edbc-c129-4113-9588-86a1ff9a3791)
 Call ID: e8b3edbc-c129-4113-9588-86a1ff9a3791
  Args:
    type: :Woman
    source: Ina-Marie_von_Bassewitz
  AddLiteral (e74db98e-a967-4d19-925a-9b35cf7d95e9)
 Call ID: e74db98e-a967-4d19-925a-9b35cf7d95e9
  Args:
    literal_value: 1914
    relation: :hasMarriageYear
    source: Oskar_Prince_of_Prussia
    literal_type: xsd:integer
  AddTriple (a41929b3-6ba3-44d2-b075-8c8636b8c617)
 Call ID: a41929b3-6ba3-44d2-b075-8c8636b8c617
  Args:
    target: Ina-Marie_von_Bassewitz
    relation: :hasRelation
    source: Oskar_Prince_of_Prussia
  Finish (21072c82-c0d3-4a8e-86e1-f0c0d257ede2)
 Call ID: 21072c82-c0d3-4a8e-86e1-f0c0d257ede2
  Args: