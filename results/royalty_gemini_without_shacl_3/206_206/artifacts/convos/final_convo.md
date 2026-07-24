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
  AssignClass (c141c951-8e8d-4bd5-a682-4a502e5394af)
 Call ID: c141c951-8e8d-4bd5-a682-4a502e5394af
  Args:
    type: :Woman
    source: Christina_Oxenberg
  AssignClass (76e6a7e1-039c-40ad-a528-89b8247aa976)
 Call ID: 76e6a7e1-039c-40ad-a528-89b8247aa976
  Args:
    type: :Person
    source: Christina_Oxenberg
  AddLiteral (c05d4a1e-1319-4366-bbe4-fe51505fa3e9)
 Call ID: c05d4a1e-1319-4366-bbe4-fe51505fa3e9
  Args:
    source: Christina_Oxenberg
    literal_value: 1962
    literal_type: xsd:integer
    relation: :hasBirthYear
  AssignClass (54c79201-e711-4cca-a99e-fd3898a4abaf)
 Call ID: 54c79201-e711-4cca-a99e-fd3898a4abaf
  Args:
    source: Princess_Elizabeth_of_Yugoslavia
    type: :Woman
  AssignClass (e8284888-86d5-46ab-893f-2256c58ad066)
 Call ID: e8284888-86d5-46ab-893f-2256c58ad066
  Args:
    source: Princess_Elizabeth_of_Yugoslavia
    type: :Person
  AddLiteral (d168dbe7-a069-4611-9f19-e999f0b2aef9)
 Call ID: d168dbe7-a069-4611-9f19-e999f0b2aef9
  Args:
    source: Princess_Elizabeth_of_Yugoslavia
    literal_type: xsd:integer
    literal_value: 1936
    relation: :hasBirthYear
  AssignClass (cd7ee7a3-209b-4c38-8080-6e77510cab66)
 Call ID: cd7ee7a3-209b-4c38-8080-6e77510cab66
  Args:
    source: Howard_Oxenberg
    type: :Man
  AssignClass (f2e692c0-1c53-49b0-bd06-6bc5137e23b5)
 Call ID: f2e692c0-1c53-49b0-bd06-6bc5137e23b5
  Args:
    type: :Person
    source: Howard_Oxenberg
  AddLiteral (e7c6de69-bf3f-47f9-a5fa-bddff0e47bee)
 Call ID: e7c6de69-bf3f-47f9-a5fa-bddff0e47bee
  Args:
    source: Howard_Oxenberg
    literal_value: 1919
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (bb1b4516-f9be-474b-957a-8197198aabce)
 Call ID: bb1b4516-f9be-474b-957a-8197198aabce
  Args:
    source: Howard_Oxenberg
    literal_type: xsd:integer
    literal_value: 2010
    relation: :hasDeathYear
  AddTriple (3451baae-4f2c-40c2-917f-b1bf4084f6cc)
 Call ID: 3451baae-4f2c-40c2-917f-b1bf4084f6cc
  Args:
    relation: :hasMother
    target: Princess_Elizabeth_of_Yugoslavia
    source: Christina_Oxenberg
  AddTriple (81e82668-40cf-4489-8662-cca53dc7146a)
 Call ID: 81e82668-40cf-4489-8662-cca53dc7146a
  Args:
    source: Christina_Oxenberg
    relation: :hasFather
    target: Howard_Oxenberg
  AssignClass (13119a9a-02ec-4fc7-9b13-de0c2d9fd0bf)
 Call ID: 13119a9a-02ec-4fc7-9b13-de0c2d9fd0bf
  Args:
    type: :Man
    source: Prince_Paul_of_Yugoslavia
  AssignClass (1ddc7891-8b49-4f2d-b4ae-7da82b38813c)
 Call ID: 1ddc7891-8b49-4f2d-b4ae-7da82b38813c
  Args:
    type: :Person
    source: Prince_Paul_of_Yugoslavia
  AssignClass (78cc2a70-dd49-4286-81d7-7b0cf0b7fff9)
 Call ID: 78cc2a70-dd49-4286-81d7-7b0cf0b7fff9
  Args:
    source: Princess_Olga_of_Greece_and_Denmark
    type: :Woman
  AssignClass (790812b8-e373-4017-844f-3bcb949b5c94)
 Call ID: 790812b8-e373-4017-844f-3bcb949b5c94
  Args:
    type: :Person
    source: Princess_Olga_of_Greece_and_Denmark
  AddTriple (55262955-c771-4a12-a7d0-f6ada5a8902d)
 Call ID: 55262955-c771-4a12-a7d0-f6ada5a8902d
  Args:
    source: Princess_Elizabeth_of_Yugoslavia
    relation: :hasFather
    target: Prince_Paul_of_Yugoslavia
  AddTriple (b90f942a-ff21-4253-a0b6-ade8b5034819)
 Call ID: b90f942a-ff21-4253-a0b6-ade8b5034819
  Args:
    source: Princess_Elizabeth_of_Yugoslavia
    target: Princess_Olga_of_Greece_and_Denmark
    relation: :hasMother
  AssignClass (af094c49-19e5-43d5-b5fc-da2a11ed6149)
 Call ID: af094c49-19e5-43d5-b5fc-da2a11ed6149
  Args:
    source: Catherine_Oxenberg
    type: :Woman
  AssignClass (0bc947c5-21db-4f2f-a60c-accc9f37ed99)
 Call ID: 0bc947c5-21db-4f2f-a60c-accc9f37ed99
  Args:
    source: Catherine_Oxenberg
    type: :Person
  AddTriple (8745a7e0-787d-4435-b3f3-f37d381cd942)
 Call ID: 8745a7e0-787d-4435-b3f3-f37d381cd942
  Args:
    target: Catherine_Oxenberg
    relation: :isSisterOf
    source: Christina_Oxenberg
  AssignClass (d97ecbed-94ea-4fdd-9338-3a49aad4c20c)
 Call ID: d97ecbed-94ea-4fdd-9338-3a49aad4c20c
  Args:
    source: Neil_Balfour
    type: :Man
  AssignClass (853f15a7-2fca-46d8-be38-6d848b420d42)
 Call ID: 853f15a7-2fca-46d8-be38-6d848b420d42
  Args:
    type: :Person
    source: Neil_Balfour
  AddLiteral (96c1c602-3a0b-4651-8dab-53ff7505296c)
 Call ID: 96c1c602-3a0b-4651-8dab-53ff7505296c
  Args:
    literal_value: 1970
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Neil_Balfour
  AddTriple (65da3567-90cd-447f-9fef-119c3cf951dc)
 Call ID: 65da3567-90cd-447f-9fef-119c3cf951dc
  Args:
    target: Princess_Elizabeth_of_Yugoslavia
    relation: :hasMother
    source: Neil_Balfour
  AssignClass (b1c0b723-de13-41f5-9b04-83c4d14589b5)
 Call ID: b1c0b723-de13-41f5-9b04-83c4d14589b5
  Args:
    type: :Man
    source: Robert_Oxenberg
  AssignClass (8b9296f8-25d9-4de1-be5b-3f8630d2b6d0)
 Call ID: 8b9296f8-25d9-4de1-be5b-3f8630d2b6d0
  Args:
    type: :Person
    source: Robert_Oxenberg
  AddTriple (8f37f3f0-032b-4f6b-bfcb-58ca4be54d51)
 Call ID: 8f37f3f0-032b-4f6b-bfcb-58ca4be54d51
  Args:
    source: Robert_Oxenberg
    target: Howard_Oxenberg
    relation: :hasFather
  AssignClass (95821c0e-2816-46b0-b1f4-40600fee2d85)
 Call ID: 95821c0e-2816-46b0-b1f4-40600fee2d85
  Args:
    source: Starr_Oxenberg
    type: :Woman
  AssignClass (2fff2f18-64d2-4fdf-be5f-1de013adc0b4)
 Call ID: 2fff2f18-64d2-4fdf-be5f-1de013adc0b4
  Args:
    source: Starr_Oxenberg
    type: :Person
  AddTriple (393810e8-5fe3-4cbb-babd-15e3a716b72a)
 Call ID: 393810e8-5fe3-4cbb-babd-15e3a716b72a
  Args:
    source: Starr_Oxenberg
    target: Howard_Oxenberg
    relation: :hasFather
  AssignClass (4d8e69d0-15a9-48dc-acf9-2b5ca5321003)
 Call ID: 4d8e69d0-15a9-48dc-acf9-2b5ca5321003
  Args:
    source: Ashley_Harcourt
    type: :Woman
  AssignClass (70822736-99a6-4f76-93b6-3e9625735dab)
 Call ID: 70822736-99a6-4f76-93b6-3e9625735dab
  Args:
    source: Ashley_Harcourt
    type: :Person
  AddTriple (96799c34-afa7-455d-a5fc-4b6d49f2d548)
 Call ID: 96799c34-afa7-455d-a5fc-4b6d49f2d548
  Args:
    source: Ashley_Harcourt
    relation: :hasFather
    target: Howard_Oxenberg
  AssignClass (1686cf50-12a3-424e-afb2-a68548f9a2da)
 Call ID: 1686cf50-12a3-424e-afb2-a68548f9a2da
  Args:
    source: Grand_Duchess_Elena_Vladimirovna_of_Russia
    type: :Woman
  AssignClass (6f152f69-f114-460e-b10c-45a47b67c829)
 Call ID: 6f152f69-f114-460e-b10c-45a47b67c829
  Args:
    source: Grand_Duchess_Elena_Vladimirovna_of_Russia
    type: :Person
  AssignClass (7409bc01-4e56-4c0d-bc4e-46926a660761)
 Call ID: 7409bc01-4e56-4c0d-bc4e-46926a660761
  Args:
    type: :Man
    source: Prince_Nicholas_of_Greece_and_Denmark
  AssignClass (c532d3f3-3b15-4f48-854f-41350cde490b)
 Call ID: c532d3f3-3b15-4f48-854f-41350cde490b
  Args:
    type: :Person
    source: Prince_Nicholas_of_Greece_and_Denmark
  AddTriple (85d6c6c0-ed54-4007-872f-17b9e1810364)
 Call ID: 85d6c6c0-ed54-4007-872f-17b9e1810364
  Args:
    source: Princess_Olga_of_Greece_and_Denmark
    relation: :hasMother
    target: Grand_Duchess_Elena_Vladimirovna_of_Russia
  AddTriple (38a86618-bc3c-4eb8-82fb-5a3481db254b)
 Call ID: 38a86618-bc3c-4eb8-82fb-5a3481db254b
  Args:
    source: Princess_Olga_of_Greece_and_Denmark
    relation: :hasFather
    target: Prince_Nicholas_of_Greece_and_Denmark
  AssignClass (06c0c0f2-8ee3-4ec1-b03d-403b73dfd018)
 Call ID: 06c0c0f2-8ee3-4ec1-b03d-403b73dfd018
  Args:
    source: Queen_Olga_Konstantinovna_of_the_Hellenes
    type: :Woman
  AssignClass (a1d9b482-9610-4271-8ba0-9dc244b6bc2e)
 Call ID: a1d9b482-9610-4271-8ba0-9dc244b6bc2e
  Args:
    source: Queen_Olga_Konstantinovna_of_the_Hellenes
    type: :Person
  AssignClass (ce1833fd-d5e2-4179-af9b-4d983ff8d053)
 Call ID: ce1833fd-d5e2-4179-af9b-4d983ff8d053
  Args:
    type: :Man
    source: King_George_of_Greece
  AssignClass (d559641c-776b-4779-9d28-7babdfed4d57)
 Call ID: d559641c-776b-4779-9d28-7babdfed4d57
  Args:
    source: King_George_of_Greece
    type: :Person
  AddTriple (bb78dd6b-4795-4b57-b831-8bf622df3020)
 Call ID: bb78dd6b-4795-4b57-b831-8bf622df3020
  Args:
    source: Prince_Nicholas_of_Greece_and_Denmark
    relation: :hasMother
    target: Queen_Olga_Konstantinovna_of_the_Hellenes
  AddTriple (c9c6a091-7457-49e6-9182-76c14b8e8a31)
 Call ID: c9c6a091-7457-49e6-9182-76c14b8e8a31
  Args:
    target: King_George_of_Greece
    relation: :hasFather
    source: Prince_Nicholas_of_Greece_and_Denmark
  AssignClass (7c910b17-c969-47f8-83f0-525642127f1b)
 Call ID: 7c910b17-c969-47f8-83f0-525642127f1b
  Args:
    type: :Woman
    source: Princess_Marina
  AssignClass (fb0e3058-99a4-4729-b0c3-20c3e99c837f)
 Call ID: fb0e3058-99a4-4729-b0c3-20c3e99c837f
  Args:
    type: :Person
    source: Princess_Marina
  AddTriple (dccfb552-c3f5-4ada-962a-7aeebf22b633)
 Call ID: dccfb552-c3f5-4ada-962a-7aeebf22b633
  Args:
    relation: :isSisterOf
    target: Princess_Marina
    source: Princess_Olga_of_Greece_and_Denmark
  AssignClass (618eb1c3-520b-4869-bf94-30ddc4135a68)
 Call ID: 618eb1c3-520b-4869-bf94-30ddc4135a68
  Args:
    source: Prince_George_Duke_of_Kent
    type: :Man
  AssignClass (505ada25-c6b3-4283-b214-3c429d20d5e8)
 Call ID: 505ada25-c6b3-4283-b214-3c429d20d5e8
  Args:
    source: Prince_George_Duke_of_Kent
    type: :Person
  AddTriple (485da72b-2a6d-461f-8c33-cadb85b2432a)
 Call ID: 485da72b-2a6d-461f-8c33-cadb85b2432a
  Args:
    source: Princess_Marina
    target: Prince_George_Duke_of_Kent
    relation: :hasRelation
  Finish (4b42f6ba-d224-48d3-9ac5-ac9938934545)
 Call ID: 4b42f6ba-d224-48d3-9ac5-ac9938934545
  Args: