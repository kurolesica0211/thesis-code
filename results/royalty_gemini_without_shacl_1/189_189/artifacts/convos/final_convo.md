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
The Crown PrinceThe Crown Princess


Princess Tomislav


Princess Alexander


Princess Elizabeth


Princess Elizabeth of Yugoslavia (Serbian: Jelisaveta Karađorđević, Јелисавета Карађорђевић; born 7 April 1936) is a member of the royal House of Karađorđević, a human rights activist and a former presidential candidate for Serbia.
Early life

Princess Elizabeth was born in the White Palace, Belgrade as the third child and the only daughter of Prince Paul of Yugoslavia (prince regent of Yugoslavia 1934–1941) and Princess Olga of Greece and Denmark.
Her older brothers were Prince Nicholas and Prince Alexander of Yugoslavia, who married, firstly, Princess Maria Pia of Savoy and, secondly, Princess Barbara of Liechtenstein.
She is a paternal second cousin of Queen Sofía of Spain and King Charles III, and a maternal first cousin of Prince Edward, Duke of Kent and his siblings, Prince Michael of Kent and Princess Alexandra, The Honourable Lady Ogilvy.
She is a maternal third cousin of king Willem-Alexander of the Netherlands.
Elizabeth is also a great-great-granddaughter of Karađorđe, who started the first Serbian uprising against the Turks in 1804.
Her godmother and namesake was her maternal aunt, Princess Elizabeth of Greece and Denmark.
Elizabeth was educated in Kenya, South Africa, United Kingdom, Switzerland, and Paris, where she studied the history of fine art.
Together with her brother Alexander, she took part in the ship tour organized by Queen Frederica and her husband King Paul of Greece in 1954, which became known as the “Cruise of the Kings” and was attended by over 100 royals from all over Europe.
On this trip, Alexander met his first wife, Maria Pia of Savoy, a daughter of Umberto II of Italy and Marie-José of Belgium, while Elizabeth fell in love for the first time with her cousin, Prince Karl of Hesse.
Later, she developed a passion for a Russian nobleman, Prince Michel Obolensky (1926–1995), youngest brother of a family friend, Princess Irina Obolensky, but she was prevented from pursuing the relationship as her parents had another suitor in mind, Baudouin of Belgium.
Marriages and children

On 21 January 1960, Princess Elizabeth married firstly Howard Oxenberg (1919–2010), an American Jewish dress manufacturer and close friend of the Kennedy family.
They have two daughters (and three granddaughters):


Princess Elizabeth's second marriage was to Neil Balfour of Dawyck (born 1944) on 23 September 1969.
He was the grandson of Alexander Balfour, founder of the Liverpool shipping company Balfour Williamson.
In 1974, she was briefly engaged to an actor Richard Burton, after his first divorce from Elizabeth Taylor.
Princess Elizabeth was married a third time, to former Prime Minister of Peru Manuel Ulloa Elías (1922–1992) on 28 February 1987.
In 1992 Ulloa Elías died, which made the princess officially a widow.
Career

A businesswoman and writer, Elizabeth is the author of four storybooks for children and has created two perfumes- "Jelisaveta" and "E".
Elizabeth recognized early the warning signs of what would eventually be known as Balkanization in Yugoslavia.
Working behind the scenes through United Nations programs, she also journeyed to the Vatican in 1989 to ask Monsignor Tauran, then Holy See Secretary for Relations with States, to help improve relations between Catholic and Orthodox communities in Yugoslavia.
In December 1990, she created the Princess Elizabeth Foundation, a non-political, not-for-profit organization after foreseeing the crucial importance of a vehicle to address the tension brewing just below the surface.
Before the breakup of Yugoslavia began in 1991, she invited the Orthodox Bishop Sava and the Mufti of Belgrade, along with the Yugoslav Minister for Religious Affairs to attend a conference in Moscow that was hosted by Mikhail Gorbachev.
In 2002, Princess Elizabeth received the first Nuclear Disarmament Forum Award, the Demiurgus Peace International (accompanying president Vladimir Putin, Archbishop Desmond Tutu, Ted Turner and others), for outstanding achievements in the field of strengthening peace among nations in Zug, Switzerland.
She decided to run for President of Serbia in the 2004 Serbian presidential election, despite her cousin Alexander's having objected that the Royal Family should stay out of politics.
Royal property

After the death of King Alexander I, and during the Regency administration (of Regent Prince Paul, Radenko Stanković, and Ivo Perović) that followed, the City of Belgrade District Court issued Decree N° 0.428/34 on 27 October 1938.
The decree, which became official law on 4 March 1939, pronounced King Alexander
I's underage sons Crown Prince Peter, Prince Tomislav, and Prince Andrew, in equal parts, heirs to his entire estate.
On 2 August 1947, Edvard Kardelj, then vice-president of the Socialist Federal Republic of Yugoslavia, issued a decree that confiscated all these properties from the Karadjordjević family.
The decree by the National Assembly of the Presidency of the People's Federal Republic of Yugoslavia was abolished in 2001, after the deposing of Slobodan Milošević.
The new government of Yugoslavia restored to all members of the royal family both their citizenship and the use of the royal complex in Dedinje.
In 2013, it was announced that the villa "Crnogorka" (meaning Montenegrin), in Uzička Street, Dedinje, was to be returned to Princess Elizabeth.
The villa had been bought in 1940 by her mother Princess Olga and taken by the state in 1947.
Elizabeth settled permanently in Belgrade, living at the Villa "Montenegrina", until she sold it in 2018.
Arms

Princess Elizabeth was granted heraldic arms on 20 June 2008.



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
  AssignClass (ba036cba-7e74-4a52-a908-b00e9613fed7)
 Call ID: ba036cba-7e74-4a52-a908-b00e9613fed7
  Args:
    type: :Woman
    source: :PrincessElizabethOfYugoslavia
  AssignClass (5cf42a5a-7a2f-43fa-bb5a-4d386f13e59e)
 Call ID: 5cf42a5a-7a2f-43fa-bb5a-4d386f13e59e
  Args:
    type: :Man
    source: :PrincePaulOfYugoslavia
  AssignClass (c9d16553-70ba-4c75-9694-30356e71ac1e)
 Call ID: c9d16553-70ba-4c75-9694-30356e71ac1e
  Args:
    type: :Woman
    source: :PrincessOlgaOfGreeceAndDenmark
  AssignClass (ea18985d-0dd6-4438-89b3-cee26f1265d7)
 Call ID: ea18985d-0dd6-4438-89b3-cee26f1265d7
  Args:
    type: :Man
    source: :PrinceNicholasOfYugoslavia
  AssignClass (979786c8-f961-4819-a5f4-0d72ddbf3d02)
 Call ID: 979786c8-f961-4819-a5f4-0d72ddbf3d02
  Args:
    type: :Man
    source: :PrinceAlexanderOfYugoslavia
  AddTriple (f224d102-d585-479a-a976-4a9c8a38f979)
 Call ID: f224d102-d585-479a-a976-4a9c8a38f979
  Args:
    relation: :hasFather
    target: :PrincePaulOfYugoslavia
    source: :PrincessElizabethOfYugoslavia
  AddTriple (5ab164a8-30ba-449c-ae1c-435ea74d7832)
 Call ID: 5ab164a8-30ba-449c-ae1c-435ea74d7832
  Args:
    source: :PrincessElizabethOfYugoslavia
    target: :PrincessOlgaOfGreeceAndDenmark
    relation: :hasMother
  AddTriple (c6f6b0b5-656f-4782-99a5-82de3b9413f9)
 Call ID: c6f6b0b5-656f-4782-99a5-82de3b9413f9
  Args:
    relation: :hasBrother
    target: :PrinceNicholasOfYugoslavia
    source: :PrincessElizabethOfYugoslavia
  AddTriple (d48bcbf2-73a9-48bf-ae81-4bb0acd753cc)
 Call ID: d48bcbf2-73a9-48bf-ae81-4bb0acd753cc
  Args:
    target: :PrinceAlexanderOfYugoslavia
    source: :PrincessElizabethOfYugoslavia
    relation: :hasBrother
  AddLiteral (c13e5c7e-fdd8-473e-b559-89fc6c289e57)
 Call ID: c13e5c7e-fdd8-473e-b559-89fc6c289e57
  Args:
    literal_value: 1936
    relation: :hasBirthYear
    source: :PrincessElizabethOfYugoslavia
    literal_type: xsd:integer
  AddLiteral (7be0180e-5b2f-4468-bb91-aec19ad3436b)
 Call ID: 7be0180e-5b2f-4468-bb91-aec19ad3436b
  Args:
    literal_type: xsd:string
    source: :PrincessElizabethOfYugoslavia
    relation: :alsoKnownAs
    literal_value: Jelisaveta Karađorđević
  AssignClass (9557072e-f6eb-4174-aa91-90f6542858b4)
 Call ID: 9557072e-f6eb-4174-aa91-90f6542858b4
  Args:
    type: :Man
    source: :HowardOxenberg
  AddLiteral (11efbd4d-2055-4314-ba89-c40870d576e7)
 Call ID: 11efbd4d-2055-4314-ba89-c40870d576e7
  Args:
    source: :PrincessElizabethOfYugoslavia
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 1960
  AssignClass (d5895fdf-d5c0-4de3-8159-09da0dbbd576)
 Call ID: d5895fdf-d5c0-4de3-8159-09da0dbbd576
  Args:
    type: :Man
    source: :NeilBalfourOfDawyck
  AddLiteral (4d96cfc8-8e7d-47a6-a52c-f53ac355b9c2)
 Call ID: 4d96cfc8-8e7d-47a6-a52c-f53ac355b9c2
  Args:
    relation: :hasMarriageYear
    literal_value: 1969
    literal_type: xsd:integer
    source: :PrincessElizabethOfYugoslavia
  AssignClass (879a2ad2-c377-42ec-ab5d-1113fafdf6e1)
 Call ID: 879a2ad2-c377-42ec-ab5d-1113fafdf6e1
  Args:
    type: :Man
    source: :ManuelUlloaElias
  AddLiteral (dd3b3707-460a-42c7-86a7-5211853d3c46)
 Call ID: dd3b3707-460a-42c7-86a7-5211853d3c46
  Args:
    literal_value: 1987
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: :PrincessElizabethOfYugoslavia
  AddLiteral (c9bb51f5-ff22-4044-8b98-4f73468ee4ba)
 Call ID: c9bb51f5-ff22-4044-8b98-4f73468ee4ba
  Args:
    source: :ManuelUlloaElias
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1992
  Finish (950600d5-b804-415a-9e0f-d7f921639b36)
 Call ID: 950600d5-b804-415a-9e0f-d7f921639b36
  Args: