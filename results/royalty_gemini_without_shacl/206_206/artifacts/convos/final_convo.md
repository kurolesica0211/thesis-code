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
  AssignClass (e1d86fe5-a574-4bb8-8e61-6ebfe276d42e)
 Call ID: e1d86fe5-a574-4bb8-8e61-6ebfe276d42e
  Args:
    source: :Christina_Oxenberg
    type: :Woman
  AssignClass (7911895c-c14b-4a51-81e9-3ce1a935184c)
 Call ID: 7911895c-c14b-4a51-81e9-3ce1a935184c
  Args:
    source: :Christina_Oxenberg
    type: :Person
  AddLiteral (064ec713-db7e-4585-9de9-0b544df2c870)
 Call ID: 064ec713-db7e-4585-9de9-0b544df2c870
  Args:
    literal_value: 1962
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: :Christina_Oxenberg
  AssignClass (b8b59895-7154-4b44-bb94-c93d0dd669ac)
 Call ID: b8b59895-7154-4b44-bb94-c93d0dd669ac
  Args:
    source: :Princess_Elizabeth_of_Yugoslavia
    type: :Woman
  AssignClass (9d8735f9-e02b-4038-8021-30560903be1d)
 Call ID: 9d8735f9-e02b-4038-8021-30560903be1d
  Args:
    source: :Princess_Elizabeth_of_Yugoslavia
    type: :Person
  AddLiteral (890f60ec-46ba-488f-8e12-4ead79059400)
 Call ID: 890f60ec-46ba-488f-8e12-4ead79059400
  Args:
    source: :Princess_Elizabeth_of_Yugoslavia
    literal_type: xsd:integer
    literal_value: 1936
    relation: :hasBirthYear
  AssignClass (fd57f428-7d4f-4729-bf2d-5a10655f6cd1)
 Call ID: fd57f428-7d4f-4729-bf2d-5a10655f6cd1
  Args:
    source: :Howard_Oxenberg
    type: :Man
  AssignClass (a9795081-8619-4763-a6d3-2e2b71160ea3)
 Call ID: a9795081-8619-4763-a6d3-2e2b71160ea3
  Args:
    source: :Howard_Oxenberg
    type: :Person
  AddLiteral (a0f627df-47fa-4d08-a9dd-5de7e6bc37e0)
 Call ID: a0f627df-47fa-4d08-a9dd-5de7e6bc37e0
  Args:
    literal_type: xsd:integer
    source: :Howard_Oxenberg
    relation: :hasBirthYear
    literal_value: 1919
  AddLiteral (6760f199-4d8f-4fd8-9fdf-aabb70010d0a)
 Call ID: 6760f199-4d8f-4fd8-9fdf-aabb70010d0a
  Args:
    literal_value: 2010
    relation: :hasDeathYear
    source: :Howard_Oxenberg
    literal_type: xsd:integer
  AddTriple (3a08e5b0-35ab-43be-b3d7-d7866687d30a)
 Call ID: 3a08e5b0-35ab-43be-b3d7-d7866687d30a
  Args:
    target: :Princess_Elizabeth_of_Yugoslavia
    source: :Christina_Oxenberg
    relation: :hasMother
  AddTriple (2ac028ac-3b2f-4ead-a458-bda48faede7c)
 Call ID: 2ac028ac-3b2f-4ead-a458-bda48faede7c
  Args:
    source: :Christina_Oxenberg
    target: :Howard_Oxenberg
    relation: :hasFather
  AssignClass (125ef981-9d73-4cbd-b6f3-69c5d2431b05)
 Call ID: 125ef981-9d73-4cbd-b6f3-69c5d2431b05
  Args:
    source: :Prince_Paul_of_Yugoslavia
    type: :Man
  AssignClass (69762788-964f-43f9-b07c-e0c106241414)
 Call ID: 69762788-964f-43f9-b07c-e0c106241414
  Args:
    source: :Prince_Paul_of_Yugoslavia
    type: :Person
  AssignClass (37de9007-7e6b-4c19-98aa-a490daa1e174)
 Call ID: 37de9007-7e6b-4c19-98aa-a490daa1e174
  Args:
    source: :Princess_Olga_of_Greece_and_Denmark
    type: :Woman
  AssignClass (27f8553e-f8c0-48eb-ae38-53d3e8f162a5)
 Call ID: 27f8553e-f8c0-48eb-ae38-53d3e8f162a5
  Args:
    source: :Princess_Olga_of_Greece_and_Denmark
    type: :Person
  AddTriple (6ac3f336-1e2f-4636-a62e-8c33e658ae86)
 Call ID: 6ac3f336-1e2f-4636-a62e-8c33e658ae86
  Args:
    relation: :hasFather
    source: :Princess_Elizabeth_of_Yugoslavia
    target: :Prince_Paul_of_Yugoslavia
  AddTriple (bd93a9e1-e97d-4c20-89de-e3d98e86e674)
 Call ID: bd93a9e1-e97d-4c20-89de-e3d98e86e674
  Args:
    relation: :hasMother
    source: :Princess_Elizabeth_of_Yugoslavia
    target: :Princess_Olga_of_Greece_and_Denmark
  AssignClass (dead47ff-db26-4d7d-a3a5-6c3f96c988d8)
 Call ID: dead47ff-db26-4d7d-a3a5-6c3f96c988d8
  Args:
    source: :Catherine_Oxenberg
    type: :Woman
  AssignClass (b84d142c-781b-4534-aa05-f4199010388a)
 Call ID: b84d142c-781b-4534-aa05-f4199010388a
  Args:
    source: :Catherine_Oxenberg
    type: :Person
  AddTriple (d05464ae-e84b-4429-81e9-a871cc7a5616)
 Call ID: d05464ae-e84b-4429-81e9-a871cc7a5616
  Args:
    relation: :hasMother
    target: :Princess_Elizabeth_of_Yugoslavia
    source: :Catherine_Oxenberg
  AddTriple (7fc5a8c1-2be1-4e4b-af31-c975cc6f4ca6)
 Call ID: 7fc5a8c1-2be1-4e4b-af31-c975cc6f4ca6
  Args:
    relation: :hasFather
    target: :Howard_Oxenberg
    source: :Catherine_Oxenberg
  AssignClass (115897b5-1612-4762-855f-7ffce475f5ad)
 Call ID: 115897b5-1612-4762-855f-7ffce475f5ad
  Args:
    source: :Neil_Balfour
    type: :Man
  AssignClass (3b2b31b4-e580-490f-b37d-35636819a777)
 Call ID: 3b2b31b4-e580-490f-b37d-35636819a777
  Args:
    source: :Neil_Balfour
    type: :Person
  AddLiteral (7d6565b7-eb1e-4c90-8798-4748c23a9cce)
 Call ID: 7d6565b7-eb1e-4c90-8798-4748c23a9cce
  Args:
    literal_value: 1970
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: :Neil_Balfour
  AddTriple (f174a22c-4ffe-4d34-8862-d7431aee5b2a)
 Call ID: f174a22c-4ffe-4d34-8862-d7431aee5b2a
  Args:
    relation: :hasMother
    source: :Neil_Balfour
    target: :Princess_Elizabeth_of_Yugoslavia
  AssignClass (947a64a0-9389-4fb1-adb4-01a8b89d8cee)
 Call ID: 947a64a0-9389-4fb1-adb4-01a8b89d8cee
  Args:
    source: :Robert_Oxenberg
    type: :Man
  AssignClass (49f9d13c-4c42-4762-a696-bcb1d1c4a913)
 Call ID: 49f9d13c-4c42-4762-a696-bcb1d1c4a913
  Args:
    source: :Robert_Oxenberg
    type: :Person
  AddTriple (4fae8d93-06d4-47f1-8212-7f7dc2766404)
 Call ID: 4fae8d93-06d4-47f1-8212-7f7dc2766404
  Args:
    relation: :hasFather
    target: :Howard_Oxenberg
    source: :Robert_Oxenberg
  AssignClass (163e0988-4262-49c0-b9be-4e99f13c0ebc)
 Call ID: 163e0988-4262-49c0-b9be-4e99f13c0ebc
  Args:
    source: :Starr_Oxenberg
    type: :Woman
  AssignClass (fe1bc77b-7d11-441b-837b-b9c85c6c529f)
 Call ID: fe1bc77b-7d11-441b-837b-b9c85c6c529f
  Args:
    source: :Starr_Oxenberg
    type: :Person
  AddTriple (b86eee3f-fd19-4e91-a448-8d0fd088779b)
 Call ID: b86eee3f-fd19-4e91-a448-8d0fd088779b
  Args:
    target: :Howard_Oxenberg
    source: :Starr_Oxenberg
    relation: :hasFather
  AssignClass (470557ad-c913-4f84-8f4d-c820622bc550)
 Call ID: 470557ad-c913-4f84-8f4d-c820622bc550
  Args:
    source: :Ashley_Harcourt
    type: :Woman
  AssignClass (98bf394b-3495-40c5-bfe2-7bc988241226)
 Call ID: 98bf394b-3495-40c5-bfe2-7bc988241226
  Args:
    source: :Ashley_Harcourt
    type: :Person
  AddTriple (4f219858-2422-4445-aef8-a345097cab6f)
 Call ID: 4f219858-2422-4445-aef8-a345097cab6f
  Args:
    source: :Ashley_Harcourt
    target: :Howard_Oxenberg
    relation: :hasFather
  Finish (136c48c3-d059-4f5e-91de-edf3dba76989)
 Call ID: 136c48c3-d059-4f5e-91de-edf3dba76989
  Args: