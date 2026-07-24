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
  AssignClass (2be4d945-ffc7-4a72-bcc8-d05e9848eff9)
 Call ID: 2be4d945-ffc7-4a72-bcc8-d05e9848eff9
  Args:
    type: :Man
    source: Oskar_Prince_of_Prussia
  AssignClass (1f05c980-66d1-4e40-a7ed-632e5bd99927)
 Call ID: 1f05c980-66d1-4e40-a7ed-632e5bd99927
  Args:
    type: :Person
    source: Oskar_Prince_of_Prussia
  AddLiteral (138de08e-3c87-456a-8953-2a211e80860e)
 Call ID: 138de08e-3c87-456a-8953-2a211e80860e
  Args:
    literal_type: xsd:positiveInteger
    literal_value: 1888
    source: Oskar_Prince_of_Prussia
    relation: :hasBirthYear
  AddLiteral (bd3ec387-824a-471f-af59-38630338b97e)
 Call ID: bd3ec387-824a-471f-af59-38630338b97e
  Args:
    source: Oskar_Prince_of_Prussia
    relation: :hasDeathYear
    literal_type: xsd:positiveInteger
    literal_value: 1958
  AssignClass (5d3c60e6-7b00-4a6f-94fe-4b670dad2938)
 Call ID: 5d3c60e6-7b00-4a6f-94fe-4b670dad2938
  Args:
    type: :Man
    source: Wilhelm_II
  AssignClass (4b2a803c-1647-4cd1-b2c1-5e7daa8a2bb4)
 Call ID: 4b2a803c-1647-4cd1-b2c1-5e7daa8a2bb4
  Args:
    type: :Person
    source: Wilhelm_II
  AssignClass (94b9b95c-7b42-481c-b8bf-5ba0f920cb2e)
 Call ID: 94b9b95c-7b42-481c-b8bf-5ba0f920cb2e
  Args:
    source: Augusta_Victoria_of_Schleswig-Holstein
    type: :Woman
  AssignClass (b998f88f-902d-468d-9015-36c365b1e2d7)
 Call ID: b998f88f-902d-468d-9015-36c365b1e2d7
  Args:
    source: Augusta_Victoria_of_Schleswig-Holstein
    type: :Person
  AddTriple (895cfe28-8445-4f34-adf7-159feb255888)
 Call ID: 895cfe28-8445-4f34-adf7-159feb255888
  Args:
    target: Wilhelm_II
    source: Oskar_Prince_of_Prussia
    relation: :hasFather
  AddTriple (786b3e11-97ae-480b-9885-a0ce09a1e556)
 Call ID: 786b3e11-97ae-480b-9885-a0ce09a1e556
  Args:
    target: Augusta_Victoria_of_Schleswig-Holstein
    source: Oskar_Prince_of_Prussia
    relation: :hasMother
  AssignClass (8fe9eaf3-9955-4db0-b2b1-0a070c66515f)
 Call ID: 8fe9eaf3-9955-4db0-b2b1-0a070c66515f
  Args:
    source: Crown_Prince_Wilhelm
    type: :Man
  AssignClass (d3ce24cd-3a8b-45bf-8e98-e0b3791c2228)
 Call ID: d3ce24cd-3a8b-45bf-8e98-e0b3791c2228
  Args:
    type: :Man
    source: Prince_Eitel_Friedrich
  AssignClass (f147660a-f70f-498f-846d-53c7fc97d34a)
 Call ID: f147660a-f70f-498f-846d-53c7fc97d34a
  Args:
    source: Prince_Adalbert
    type: :Man
  AssignClass (e573c20a-db17-4305-a216-89f9329fe05f)
 Call ID: e573c20a-db17-4305-a216-89f9329fe05f
  Args:
    source: Prince_August_Wilhelm
    type: :Man
  AssignClass (590d5c84-3bfa-4f7f-b8a7-ef2ebecba184)
 Call ID: 590d5c84-3bfa-4f7f-b8a7-ef2ebecba184
  Args:
    type: :Man
    source: Prince_Joachim
  AssignClass (1d2f635a-5ac1-4bed-ba25-d06c39ae406f)
 Call ID: 1d2f635a-5ac1-4bed-ba25-d06c39ae406f
  Args:
    type: :Woman
    source: Princess_Viktoria_Luise
  AddTriple (ee5140e4-59fe-4f10-a9f8-a7bb71f3f145)
 Call ID: ee5140e4-59fe-4f10-a9f8-a7bb71f3f145
  Args:
    source: Oskar_Prince_of_Prussia
    relation: :isSiblingOf
    target: Crown_Prince_Wilhelm
  AddTriple (0dcb7808-d821-4d3b-b299-ee06d00589a9)
 Call ID: 0dcb7808-d821-4d3b-b299-ee06d00589a9
  Args:
    target: Prince_Eitel_Friedrich
    source: Oskar_Prince_of_Prussia
    relation: :isSiblingOf
  AddTriple (f2673cc2-ac46-417f-9042-3bce4b8eaef7)
 Call ID: f2673cc2-ac46-417f-9042-3bce4b8eaef7
  Args:
    source: Oskar_Prince_of_Prussia
    relation: :isSiblingOf
    target: Prince_Adalbert
  AddTriple (de67cc6a-f3ab-4c2b-a98f-41212d994dbb)
 Call ID: de67cc6a-f3ab-4c2b-a98f-41212d994dbb
  Args:
    source: Oskar_Prince_of_Prussia
    relation: :isSiblingOf
    target: Prince_August_Wilhelm
  AddTriple (0dfe08dd-fac8-4a63-b3e8-4feef5d944c1)
 Call ID: 0dfe08dd-fac8-4a63-b3e8-4feef5d944c1
  Args:
    relation: :isSiblingOf
    source: Oskar_Prince_of_Prussia
    target: Prince_Joachim
  AddTriple (88dec77d-1c52-4555-b4eb-8a71350f2481)
 Call ID: 88dec77d-1c52-4555-b4eb-8a71350f2481
  Args:
    target: Princess_Viktoria_Luise
    relation: :isSiblingOf
    source: Oskar_Prince_of_Prussia
  AssignClass (cbf23c5d-1c71-4ab5-933d-b7bf9538100f)
 Call ID: cbf23c5d-1c71-4ab5-933d-b7bf9538100f
  Args:
    type: :Woman
    source: Ina-Marie_von_Bassewitz
  AssignClass (f8f8ad4e-21e2-4ee0-ace4-25218033729d)
 Call ID: f8f8ad4e-21e2-4ee0-ace4-25218033729d
  Args:
    type: :Person
    source: Ina-Marie_von_Bassewitz
  AddLiteral (bd30e5b7-751b-42ed-98f9-4b984e9892bd)
 Call ID: bd30e5b7-751b-42ed-98f9-4b984e9892bd
  Args:
    literal_type: xsd:positiveInteger
    literal_value: 1914
    source: Oskar_Prince_of_Prussia
    relation: :hasMarriageYear
  AddTriple (71afb384-df88-4a90-a7e2-85bbf5975ef7)
 Call ID: 71afb384-df88-4a90-a7e2-85bbf5975ef7
  Args:
    relation: :hasRelation
    source: Oskar_Prince_of_Prussia
    target: Ina-Marie_von_Bassewitz
  AssignClass (7774249e-bf97-468f-a88b-59db71f69880)
 Call ID: 7774249e-bf97-468f-a88b-59db71f69880
  Args:
    source: Oskar_son_of_Oskar
    type: :Man
  AssignClass (33feccf3-56e0-4b05-a686-01b9c4e52c3f)
 Call ID: 33feccf3-56e0-4b05-a686-01b9c4e52c3f
  Args:
    type: :Person
    source: Oskar_son_of_Oskar
  AssignClass (ecbd476a-a3c1-4fdc-b1c4-69755c8a533c)
 Call ID: ecbd476a-a3c1-4fdc-b1c4-69755c8a533c
  Args:
    type: :Man
    source: Wilhelm_Karl_son_of_Oskar
  AssignClass (60c77b5e-e8e2-40cc-ba0d-85c63a71ad43)
 Call ID: 60c77b5e-e8e2-40cc-ba0d-85c63a71ad43
  Args:
    source: Wilhelm_Karl_son_of_Oskar
    type: :Person
  AddTriple (a7ee46db-c27d-4ff2-bfcb-a5a6f487d9e4)
 Call ID: a7ee46db-c27d-4ff2-bfcb-a5a6f487d9e4
  Args:
    target: Oskar_son_of_Oskar
    relation: :hasSon
    source: Oskar_Prince_of_Prussia
  AddTriple (00aadb38-a1bb-4adc-8e28-8e9c43b344ea)
 Call ID: 00aadb38-a1bb-4adc-8e28-8e9c43b344ea
  Args:
    relation: :hasSon
    source: Oskar_Prince_of_Prussia
    target: Wilhelm_Karl_son_of_Oskar
  Finish (0bfa5890-1036-4785-a932-095aa22951b6)
 Call ID: 0bfa5890-1036-4785-a932-095aa22951b6
  Args: