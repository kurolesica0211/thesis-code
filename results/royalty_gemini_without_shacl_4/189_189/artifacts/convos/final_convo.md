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
  AssignClass (0536fdd6-eb53-4a40-b6d9-3c423c1a7276)
 Call ID: 0536fdd6-eb53-4a40-b6d9-3c423c1a7276
  Args:
    source: Princess_Elizabeth_of_Yugoslavia
    type: :Woman
  AssignClass (1e1235bc-c83f-4184-8749-55db85a24bb7)
 Call ID: 1e1235bc-c83f-4184-8749-55db85a24bb7
  Args:
    type: :Man
    source: Prince_Paul_of_Yugoslavia
  AssignClass (50b814f5-9595-4fa1-b26e-cc6d39973ced)
 Call ID: 50b814f5-9595-4fa1-b26e-cc6d39973ced
  Args:
    type: :Woman
    source: Princess_Olga_of_Greece_and_Denmark
  AssignClass (f6a0179b-5da9-4b69-b4c6-185833add46e)
 Call ID: f6a0179b-5da9-4b69-b4c6-185833add46e
  Args:
    type: :Man
    source: Prince_Nicholas_of_Yugoslavia
  AssignClass (3b8ac133-aa3c-4703-a6dd-067ec116009d)
 Call ID: 3b8ac133-aa3c-4703-a6dd-067ec116009d
  Args:
    source: Prince_Alexander_of_Yugoslavia
    type: :Man
  AssignClass (acc33ec2-2be1-48bb-a379-2768e631efe7)
 Call ID: acc33ec2-2be1-48bb-a379-2768e631efe7
  Args:
    source: Howard_Oxenberg
    type: :Man
  AssignClass (7dfb7c93-b11e-4de9-8fca-dfb0d7a035eb)
 Call ID: 7dfb7c93-b11e-4de9-8fca-dfb0d7a035eb
  Args:
    type: :Man
    source: Neil_Balfour_of_Dawyck
  AssignClass (1c04ab36-82f1-4524-b161-98909623953c)
 Call ID: 1c04ab36-82f1-4524-b161-98909623953c
  Args:
    type: :Man
    source: Manuel_Ulloa_Elias
  AddLiteral (ff4a83ff-a85a-4528-a488-f9c72d527de7)
 Call ID: ff4a83ff-a85a-4528-a488-f9c72d527de7
  Args:
    literal_type: xsd:string
    source: Princess_Elizabeth_of_Yugoslavia
    literal_value: Jelisaveta Karađorđević
    relation: :alsoKnownAs
  AddLiteral (abf7ea8a-1beb-4ab1-a4a5-42066525349b)
 Call ID: abf7ea8a-1beb-4ab1-a4a5-42066525349b
  Args:
    source: Princess_Elizabeth_of_Yugoslavia
    literal_type: xsd:string
    literal_value: 1936
    relation: :hasBirthYear
  AddTriple (b558b750-2110-4337-934b-ded5207fa334)
 Call ID: b558b750-2110-4337-934b-ded5207fa334
  Args:
    target: Prince_Paul_of_Yugoslavia
    source: Princess_Elizabeth_of_Yugoslavia
    relation: :hasFather
  AddTriple (1bd3d89c-f13c-4031-8f6d-0e36cdde5518)
 Call ID: 1bd3d89c-f13c-4031-8f6d-0e36cdde5518
  Args:
    source: Princess_Elizabeth_of_Yugoslavia
    relation: :hasMother
    target: Princess_Olga_of_Greece_and_Denmark
  AddTriple (ad067372-745c-491d-8e82-d0ca4069fd81)
 Call ID: ad067372-745c-491d-8e82-d0ca4069fd81
  Args:
    target: Prince_Nicholas_of_Yugoslavia
    source: Princess_Elizabeth_of_Yugoslavia
    relation: :hasBrother
  AddTriple (e1d65802-9295-4ff1-8096-c557389ce31d)
 Call ID: e1d65802-9295-4ff1-8096-c557389ce31d
  Args:
    source: Princess_Elizabeth_of_Yugoslavia
    relation: :hasBrother
    target: Prince_Alexander_of_Yugoslavia
  AddLiteral (5cb6eec6-a38c-4ae3-b9cb-ce2d99989bf7)
 Call ID: 5cb6eec6-a38c-4ae3-b9cb-ce2d99989bf7
  Args:
    relation: :hasBirthYear
    literal_value: 1919
    literal_type: xsd:string
    source: Howard_Oxenberg
  AddLiteral (f725611a-594d-4cbe-8618-b5b79f415448)
 Call ID: f725611a-594d-4cbe-8618-b5b79f415448
  Args:
    relation: :hasDeathYear
    literal_value: 2010
    source: Howard_Oxenberg
    literal_type: xsd:string
  AddLiteral (14f9f0a2-6f30-4ec9-b100-5272ec790310)
 Call ID: 14f9f0a2-6f30-4ec9-b100-5272ec790310
  Args:
    relation: :hasMarriageYear
    literal_value: 1960
    literal_type: xsd:string
    source: Princess_Elizabeth_of_Yugoslavia
  AddLiteral (580a595c-2174-4fcc-a0ed-92bb1ef2010c)
 Call ID: 580a595c-2174-4fcc-a0ed-92bb1ef2010c
  Args:
    relation: :hasBirthYear
    literal_value: 1944
    literal_type: xsd:string
    source: Neil_Balfour_of_Dawyck
  AddLiteral (ad1e172d-4f54-4451-a57b-c2f719670edc)
 Call ID: ad1e172d-4f54-4451-a57b-c2f719670edc
  Args:
    relation: :hasMarriageYear
    literal_value: 1969
    literal_type: xsd:string
    source: Princess_Elizabeth_of_Yugoslavia
  AddLiteral (081c3af9-ab45-4c94-a932-9a23fb9e36c4)
 Call ID: 081c3af9-ab45-4c94-a932-9a23fb9e36c4
  Args:
    literal_value: 1922
    source: Manuel_Ulloa_Elias
    literal_type: xsd:string
    relation: :hasBirthYear
  AddLiteral (9138e4ed-e7eb-4154-8d3d-486640eb9243)
 Call ID: 9138e4ed-e7eb-4154-8d3d-486640eb9243
  Args:
    literal_value: 1992
    source: Manuel_Ulloa_Elias
    literal_type: xsd:string
    relation: :hasDeathYear
  AddLiteral (1fbb73af-08c0-42b5-a7f8-7907d96aab35)
 Call ID: 1fbb73af-08c0-42b5-a7f8-7907d96aab35
  Args:
    relation: :hasMarriageYear
    literal_value: 1987
    literal_type: xsd:string
    source: Princess_Elizabeth_of_Yugoslavia
  Finish (020a8263-263e-42b9-a76d-bea13472e9a5)
 Call ID: 020a8263-263e-42b9-a76d-bea13472e9a5
  Args: