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
Christina Oxenberg (born December 27, 1962) is an American writer, humorist, and fashion designer.
Her two knitwear clothing lines, Christina Oxenberg and Ox, have appeared in Barneys, Bloomingdale's, and luxury boutiques throughout the world.
Oxenberg is the daughter of Princess Elizabeth of Yugoslavia and is a descendant of the Serbian House of Karađorđević.
Early life

Christina Oxenberg was born in New York City.
She is a daughter of Princess Elizabeth of Yugoslavia (born 1936) and her first husband Howard Oxenberg (1919–2010), a Jewish self-made textile and clothing tycoon and close friend of the Kennedy family.
Princess Elizabeth is the only daughter of Prince Paul of Yugoslavia (who served as regent for his cousin's eldest son King Peter II of Yugoslavia) and Princess Olga of Greece and Denmark.
She has a full sister, Catherine Oxenberg, and a half-brother on her mother's side, Neil Balfour (born 1970).
On her father's side she has a half-brother, Robert Oxenberg, and two half-sisters Starr Oxenberg and Ashley Harcourt.
She is a first cousin of Prince Edward, Duke of Kent, and also a maternal second cousin of Queen Sofía of Spain, making her a second cousin once removed of King Charles III.
Career

After high school, Oxenberg worked various jobs in New York ranging from a secretary to a roller-rink attendant.
Upon her return, Oxenberg secured a job at Studio 54.
In 1994, Simon & Schuster commissioned Oxenberg to write a semi-autobiographical novel that would eventually be published as Royal Blue.
As a result of the book, Oxenberg appeared on the cover of New York Magazine and was profiled in People.
In 2000, Oxenberg went on hiatus from writing and took a job at Robert F. Kennedy Jr.'s Waterkeeper Alliance.
The two discussed the possibility of a clothing line using Oxenberg's name.
From 2002 to 2010, Oxenberg produced two clothing lines (Christina Oxenberg and Ox).
Christina Oxenberg would go on to self-publish several collections of short stories between 2010 and 2014, including Do These Gloves Make My Ass Look Fat?, Life is Short: Read Short Stories, and When in Doubt...Double the Dosage.
Since 2012 Oxenberg has contributed articles to Key West weekly magazine Konk Life.
In 2014, Oxenberg helped organize a visit by John Hemingway (Ernest Hemingway's grandson) to David Wolkowsky's Tennessee Williams Collection.
In 2015, Christina Oxenberg moved to Serbia for a year to write and research her book, Royal Dynasty – An Insider's History of the Serbian Royal Family, which was published in Serbian in 2015 by the publisher, Laguna.
For her work, Oxenberg received an award from the Serbian Academy of Sciences and Arts in 2016.
Subsequently, Oxenberg was interviewed by the Sunday Times, Radio Gorgeous and Tatler, and she presented the book at the Oxford Literary Festival on 22 March 2018.
Bibliography

Novels


Short story collections


Autobiographies


Ancestry

Christina Oxenberg is a direct descendant of Karađorđe, a peasant from Šumadija region in today's Serbia, leader of First Serbian Uprising against the Ottomans, and founder of the Karađorđević Dynasty; of King George I of Greece; of Tsar Alexander II of Russia; of King George II of Great Britain, Empress Catherine II of Russia, and  William the Conqueror, through Frederick of Mecklenburg-Schwerin.
Oxenberg's maternal grandmother, Princess Olga, was the daughter of Grand Duchess Elena Vladimirovna of Russia and Prince Nicholas of Greece and Denmark, himself the son of another Romanov grand duchess, Queen Olga Konstantinovna of the Hellenes and her Danish-born husband King George of Greece, brother of Queen Alexandra of the United Kingdom and the Empress Maria Fyodorovna.
Princess Olga was the sister of Princess Marina, who married Prince George, Duke of Kent (an uncle of Queen Elizabeth II); and Olga/Marina were also paternal first cousins of the Duke of Edinburgh (husband of Queen Elizabeth II) through their respective fathers Prince Nicholas of Greece and Denmark and Prince Andrew of Greece and Denmark, who were brothers.



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
  AssignClass (5929da65-3381-42f8-a3ac-b400a6937e06)
 Call ID: 5929da65-3381-42f8-a3ac-b400a6937e06
  Args:
    type: :Woman
    source: :Christina_Oxenberg
  AssignClass (3818214f-2c41-4a88-8eb4-4bb983887707)
 Call ID: 3818214f-2c41-4a88-8eb4-4bb983887707
  Args:
    type: :Person
    source: :Christina_Oxenberg
  AddLiteral (47e9a865-046d-4c84-8994-44c42e9f1991)
 Call ID: 47e9a865-046d-4c84-8994-44c42e9f1991
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: :Christina_Oxenberg
    literal_value: 1962
  AssignClass (3f6360ab-17af-4e6a-b168-ee6efb7ede89)
 Call ID: 3f6360ab-17af-4e6a-b168-ee6efb7ede89
  Args:
    type: :Woman
    source: :Princess_Elizabeth_of_Yugoslavia
  AssignClass (7b6c8738-c658-4acb-8696-71d6a8dde588)
 Call ID: 7b6c8738-c658-4acb-8696-71d6a8dde588
  Args:
    type: :Person
    source: :Princess_Elizabeth_of_Yugoslavia
  AddLiteral (d4e95df4-7214-4e92-ae83-bac453e83e1f)
 Call ID: d4e95df4-7214-4e92-ae83-bac453e83e1f
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1936
    source: :Princess_Elizabeth_of_Yugoslavia
  AssignClass (406195cb-1c0f-42da-ba95-c1f1d26a449a)
 Call ID: 406195cb-1c0f-42da-ba95-c1f1d26a449a
  Args:
    type: :Man
    source: :Howard_Oxenberg
  AssignClass (f12facd6-518e-4665-83ab-8856e113989f)
 Call ID: f12facd6-518e-4665-83ab-8856e113989f
  Args:
    type: :Person
    source: :Howard_Oxenberg
  AddLiteral (1c90575e-8f89-430d-a239-4e7fa2ca3932)
 Call ID: 1c90575e-8f89-430d-a239-4e7fa2ca3932
  Args:
    literal_value: 1919
    source: :Howard_Oxenberg
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (b76ea0d6-83f3-4cb1-8989-483f8b9d7c1f)
 Call ID: b76ea0d6-83f3-4cb1-8989-483f8b9d7c1f
  Args:
    literal_value: 2010
    source: :Howard_Oxenberg
    literal_type: xsd:integer
    relation: :hasDeathYear
  AddTriple (3885a57e-c645-4d3b-8075-c507ce493196)
 Call ID: 3885a57e-c645-4d3b-8075-c507ce493196
  Args:
    target: :Princess_Elizabeth_of_Yugoslavia
    relation: :hasMother
    source: :Christina_Oxenberg
  AddTriple (0ed570b9-cacc-4bea-a4d8-23400492b06d)
 Call ID: 0ed570b9-cacc-4bea-a4d8-23400492b06d
  Args:
    target: :Howard_Oxenberg
    relation: :hasFather
    source: :Christina_Oxenberg
  AssignClass (560c3de1-3cd2-4370-a773-8afb583168e0)
 Call ID: 560c3de1-3cd2-4370-a773-8afb583168e0
  Args:
    type: :Man
    source: :Prince_Paul_of_Yugoslavia
  AssignClass (83daf6d4-8d97-4bba-a0df-df483dbe50d6)
 Call ID: 83daf6d4-8d97-4bba-a0df-df483dbe50d6
  Args:
    type: :Person
    source: :Prince_Paul_of_Yugoslavia
  AssignClass (a091c5fe-e596-42b7-ac81-ae7f009d890e)
 Call ID: a091c5fe-e596-42b7-ac81-ae7f009d890e
  Args:
    type: :Woman
    source: :Princess_Olga_of_Greece_and_Denmark
  AssignClass (aa27291f-f87e-4e5a-8047-86da798c8b66)
 Call ID: aa27291f-f87e-4e5a-8047-86da798c8b66
  Args:
    type: :Person
    source: :Princess_Olga_of_Greece_and_Denmark
  AddTriple (e5e868ea-d655-4e21-aa56-4ed118550858)
 Call ID: e5e868ea-d655-4e21-aa56-4ed118550858
  Args:
    relation: :hasFather
    target: :Prince_Paul_of_Yugoslavia
    source: :Princess_Elizabeth_of_Yugoslavia
  AddTriple (c1cfb08f-d8bd-4840-ba06-44a369977c1a)
 Call ID: c1cfb08f-d8bd-4840-ba06-44a369977c1a
  Args:
    target: :Princess_Olga_of_Greece_and_Denmark
    relation: :hasMother
    source: :Princess_Elizabeth_of_Yugoslavia
  AssignClass (bcd8c346-25ec-4e81-9085-6b9a94e37b8a)
 Call ID: bcd8c346-25ec-4e81-9085-6b9a94e37b8a
  Args:
    type: :Woman
    source: :Catherine_Oxenberg
  AssignClass (ec02b6fc-5bc1-4fdc-a4fc-b84a5ea11f80)
 Call ID: ec02b6fc-5bc1-4fdc-a4fc-b84a5ea11f80
  Args:
    type: :Person
    source: :Catherine_Oxenberg
  AddTriple (b66b2bb4-16aa-4533-9f45-39e9becbeb05)
 Call ID: b66b2bb4-16aa-4533-9f45-39e9becbeb05
  Args:
    source: :Christina_Oxenberg
    relation: :hasSister
    target: :Catherine_Oxenberg
  AssignClass (1a8adef7-dccc-4ff9-8dde-192ace14c10e)
 Call ID: 1a8adef7-dccc-4ff9-8dde-192ace14c10e
  Args:
    type: :Man
    source: :Neil_Balfour
  AssignClass (70d5a1b1-9ff2-4881-bbca-a7a1fa789bf2)
 Call ID: 70d5a1b1-9ff2-4881-bbca-a7a1fa789bf2
  Args:
    type: :Person
    source: :Neil_Balfour
  AddLiteral (97e89ed5-36c6-4c7d-8085-0db116ae7504)
 Call ID: 97e89ed5-36c6-4c7d-8085-0db116ae7504
  Args:
    literal_value: 1970
    source: :Neil_Balfour
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddTriple (0854ee36-54f7-43c8-a3f3-4cb49a7f8c44)
 Call ID: 0854ee36-54f7-43c8-a3f3-4cb49a7f8c44
  Args:
    source: :Neil_Balfour
    relation: :hasMother
    target: :Princess_Elizabeth_of_Yugoslavia
  AssignClass (a988ac02-2c0a-46ca-9f5b-d3339968c5e5)
 Call ID: a988ac02-2c0a-46ca-9f5b-d3339968c5e5
  Args:
    type: :Man
    source: :Robert_Oxenberg
  AssignClass (70fa5edf-0dc7-488e-a880-70daec360183)
 Call ID: 70fa5edf-0dc7-488e-a880-70daec360183
  Args:
    type: :Person
    source: :Robert_Oxenberg
  AddTriple (f994bd6e-2282-4c80-b4fc-0a882221a675)
 Call ID: f994bd6e-2282-4c80-b4fc-0a882221a675
  Args:
    target: :Howard_Oxenberg
    relation: :hasFather
    source: :Robert_Oxenberg
  AssignClass (a8104c6c-0c31-4946-b513-2b5b07931932)
 Call ID: a8104c6c-0c31-4946-b513-2b5b07931932
  Args:
    type: :Woman
    source: :Starr_Oxenberg
  AssignClass (28c76ca1-6da4-47c8-a8ab-5846662575e2)
 Call ID: 28c76ca1-6da4-47c8-a8ab-5846662575e2
  Args:
    type: :Person
    source: :Starr_Oxenberg
  AddTriple (e5e704d9-fada-4caa-8975-a85ed0993c8d)
 Call ID: e5e704d9-fada-4caa-8975-a85ed0993c8d
  Args:
    relation: :hasFather
    target: :Howard_Oxenberg
    source: :Starr_Oxenberg
  AssignClass (3b89f798-0c0d-4d6f-910f-78308cc28515)
 Call ID: 3b89f798-0c0d-4d6f-910f-78308cc28515
  Args:
    type: :Woman
    source: :Ashley_Harcourt
  AssignClass (e18ff25d-ab38-4ec5-afe1-9d9b385e7e51)
 Call ID: e18ff25d-ab38-4ec5-afe1-9d9b385e7e51
  Args:
    type: :Person
    source: :Ashley_Harcourt
  AddTriple (5d718633-848f-4371-91aa-7f242880ead0)
 Call ID: 5d718633-848f-4371-91aa-7f242880ead0
  Args:
    relation: :hasFather
    target: :Howard_Oxenberg
    source: :Ashley_Harcourt
  AssignClass (9045899f-ec79-40ba-8c06-ac70d4e1b0a3)
 Call ID: 9045899f-ec79-40ba-8c06-ac70d4e1b0a3
  Args:
    type: :Woman
    source: :Grand_Duchess_Elena_Vladimirovna_of_Russia
  AssignClass (889b6071-7fea-4cd6-b4b1-c9560d76c674)
 Call ID: 889b6071-7fea-4cd6-b4b1-c9560d76c674
  Args:
    type: :Person
    source: :Grand_Duchess_Elena_Vladimirovna_of_Russia
  AssignClass (03ca47ee-38ff-49a5-863b-160e17b44133)
 Call ID: 03ca47ee-38ff-49a5-863b-160e17b44133
  Args:
    type: :Man
    source: :Prince_Nicholas_of_Greece_and_Denmark
  AssignClass (9f6ad655-e748-4d5b-9f94-cd1892646f66)
 Call ID: 9f6ad655-e748-4d5b-9f94-cd1892646f66
  Args:
    type: :Person
    source: :Prince_Nicholas_of_Greece_and_Denmark
  AddTriple (4640bafb-6d66-4459-b20d-92f113a97a5d)
 Call ID: 4640bafb-6d66-4459-b20d-92f113a97a5d
  Args:
    relation: :hasMother
    target: :Grand_Duchess_Elena_Vladimirovna_of_Russia
    source: :Princess_Olga_of_Greece_and_Denmark
  AddTriple (ae218820-4675-4adf-9afa-b5d5dcda8801)
 Call ID: ae218820-4675-4adf-9afa-b5d5dcda8801
  Args:
    relation: :hasFather
    target: :Prince_Nicholas_of_Greece_and_Denmark
    source: :Princess_Olga_of_Greece_and_Denmark
  AssignClass (f18d16bb-879b-42b8-acfc-973e24e4293f)
 Call ID: f18d16bb-879b-42b8-acfc-973e24e4293f
  Args:
    type: :Woman
    source: :Queen_Olga_Konstantinovna_of_the_Hellenes
  AssignClass (f119faaf-4027-4a1f-8ead-399fa863029d)
 Call ID: f119faaf-4027-4a1f-8ead-399fa863029d
  Args:
    type: :Person
    source: :Queen_Olga_Konstantinovna_of_the_Hellenes
  AssignClass (ebd2586d-ed1f-4df1-b7ae-313d959039a5)
 Call ID: ebd2586d-ed1f-4df1-b7ae-313d959039a5
  Args:
    type: :Man
    source: :King_George_of_Greece
  AssignClass (704753b5-2805-40e3-b60e-a83c613a4e7e)
 Call ID: 704753b5-2805-40e3-b60e-a83c613a4e7e
  Args:
    type: :Person
    source: :King_George_of_Greece
  AddTriple (b9c7ec95-078d-484e-8174-c8d06c8a9134)
 Call ID: b9c7ec95-078d-484e-8174-c8d06c8a9134
  Args:
    source: :Prince_Nicholas_of_Greece_and_Denmark
    relation: :hasMother
    target: :Queen_Olga_Konstantinovna_of_the_Hellenes
  AddTriple (09497a3d-950e-4051-a2fd-de4ba38bcb2b)
 Call ID: 09497a3d-950e-4051-a2fd-de4ba38bcb2b
  Args:
    relation: :hasFather
    target: :King_George_of_Greece
    source: :Prince_Nicholas_of_Greece_and_Denmark
  Finish (e8fe33c3-de46-49a7-be63-de13ff3f0206)
 Call ID: e8fe33c3-de46-49a7-be63-de13ff3f0206
  Args: