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
Prince Heinrich of Prussia (German: Albert Wilhelm Heinrich; 14 August 1862 – 20 April 1929) was a younger brother of German Emperor and King of Prussia Wilhelm II and a Prince of Prussia.
Biography

Born in Berlin, Prince Heinrich was the third child and second son of eight children born to Crown Prince Frederick William (later Emperor Frederick III), and Victoria, Princess Royal (later Empress Victoria and in widowhood Empress Frederick), eldest daughter of the British Queen Victoria.
Henry was three years younger than his brother, the future Emperor William II (born 27 January 1859).
He was born on the same day as King Frederick William I "Soldier-King" of Prussia.
Early commands

As a Prussian prince, Henry quickly achieved command.
Squadron commands

From 1897, Prince Henry commanded several naval task forces; these included an improvised squadron that took part with the East Asia Squadron in consolidating and securing the German hold on the region of Kiaochow and the port of Tsingtao in 1898.
The prince's success was more of the diplomatic than the military variety; he became the first European potentate ever to be received at the Chinese imperial court.
From 1906 to 1909, Henry was commander of the High Seas Fleet.
I

At the beginning of World War I, Prince Henry was named as Commander-in-Chief of the Baltic Fleet.
After the end of hostilities with Russia, his mission was ended, and Prince Henry simply left active duty.
With the war's end and the dissolution of the monarchy in Germany, Prince Henry left the navy.
Family

On 24 May 1888, Henry married Princess Irene of Hesse and by Rhine, his first cousin.
His dying father, German Emperor Frederick III and his mother Empress Victoria were in attendance.
The marriage produced three children:


Their sons Waldemar and Heinrich were both hemophiliacs, a disease which they inherited through Irene from the maternal grandmother of both of their parents, Queen Victoria, who was a carrier.
Personality and private life

Henry received one of the first pilot's licenses in Germany, and was judged a spirited and excellent seaman.
A yachting enthusiast, Prince Henry became one of the first members of the Yacht Club of Kiel, established by a group of naval officers in 1887, and quickly became the club's patron.
Henry was interested in motor cars as well and supposedly invented a windshield wiper and, according to other sources, the car horn.
In his honor, the Prinz-Heinrich-Fahrt (Prince Heinrich Tour) was established in 1908, like the earlier Kaiserpreis a precursor to the German Grand Prix.
Henry and his brother William gave patronage to the Kaiserlicher Automobilclub (Imperial Automobile Club).
From 1911 to 1914 the British car makers Vauxhall Motors produced a model, the C-10, which was called the "Vauxhall Prince Henry" in his honour after initially being built for participation in the 1911 race.
After the German Revolution, Henry lived with his family in Hemmelmark near Eckernförde, in Schleswig-Holstein.
He popularized the Prince Henry cap, which is still worn, especially by older sailors.
In 1899, Henry received an honorary doctorate (Doctor of Engineering honoris causa) from the Technische Hochschule in Charlottenburg (now Technische Universität Berlin) .
Prince Henry died of throat cancer on 20 April 1929 in Hemmelmark.



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
  AssignClass (3fe6078d-210f-4dc4-b4ec-e99712986f0a)
 Call ID: 3fe6078d-210f-4dc4-b4ec-e99712986f0a
  Args:
    type: :Man
    source: Prince_Heinrich_of_Prussia
  AssignClass (048e9202-3cef-427e-8316-cb7ea9af36ab)
 Call ID: 048e9202-3cef-427e-8316-cb7ea9af36ab
  Args:
    type: :Person
    source: Prince_Heinrich_of_Prussia
  AssignClass (eb925844-6f95-41ef-8aa1-0551973f4b52)
 Call ID: eb925844-6f95-41ef-8aa1-0551973f4b52
  Args:
    type: :Man
    source: Wilhelm_II
  AssignClass (8bcfe04d-53a0-4651-b1be-cb024185632a)
 Call ID: 8bcfe04d-53a0-4651-b1be-cb024185632a
  Args:
    type: :Person
    source: Wilhelm_II
  AssignClass (76ca443c-6e30-45d0-b9d5-135367c3e8a9)
 Call ID: 76ca443c-6e30-45d0-b9d5-135367c3e8a9
  Args:
    type: :Man
    source: Frederick_III
  AssignClass (bc6d647c-ffe7-4c58-a20e-e027b14063c1)
 Call ID: bc6d647c-ffe7-4c58-a20e-e027b14063c1
  Args:
    type: :Person
    source: Frederick_III
  AssignClass (51e5e603-b4d5-4d8f-baff-a95690af2a8e)
 Call ID: 51e5e603-b4d5-4d8f-baff-a95690af2a8e
  Args:
    type: :Woman
    source: Empress_Victoria
  AssignClass (dbd82bd5-f086-4fdd-9148-1bb2d605cb2c)
 Call ID: dbd82bd5-f086-4fdd-9148-1bb2d605cb2c
  Args:
    type: :Person
    source: Empress_Victoria
  AssignClass (e17cfc4c-374d-4984-ab85-0fcd02e6417a)
 Call ID: e17cfc4c-374d-4984-ab85-0fcd02e6417a
  Args:
    type: :Woman
    source: Queen_Victoria
  AssignClass (6b8becb0-7789-41ff-9294-cd88ead1c03c)
 Call ID: 6b8becb0-7789-41ff-9294-cd88ead1c03c
  Args:
    type: :Person
    source: Queen_Victoria
  AssignClass (85ffb589-651d-4eff-ba9c-ebf6f05ec086)
 Call ID: 85ffb589-651d-4eff-ba9c-ebf6f05ec086
  Args:
    type: :Woman
    source: Princess_Irene_of_Hesse_and_by_Rhine
  AssignClass (f3db5273-0664-4343-8ba4-51cfa19fd96b)
 Call ID: f3db5273-0664-4343-8ba4-51cfa19fd96b
  Args:
    type: :Person
    source: Princess_Irene_of_Hesse_and_by_Rhine
  AssignClass (5cc9417a-4949-48b7-85e6-6bc006e4d5cb)
 Call ID: 5cc9417a-4949-48b7-85e6-6bc006e4d5cb
  Args:
    type: :Man
    source: Waldemar
  AssignClass (921cb89b-a2e7-4b71-b198-f7e4c4c4a4c6)
 Call ID: 921cb89b-a2e7-4b71-b198-f7e4c4c4a4c6
  Args:
    type: :Person
    source: Waldemar
  AssignClass (beade10b-7337-464d-b106-e2d16b8f555c)
 Call ID: beade10b-7337-464d-b106-e2d16b8f555c
  Args:
    type: :Man
    source: Heinrich_son_of_Henry
  AssignClass (9db46ada-4272-408c-a35c-78859e2f1075)
 Call ID: 9db46ada-4272-408c-a35c-78859e2f1075
  Args:
    type: :Person
    source: Heinrich_son_of_Henry
  AddLiteral (38078e68-9acd-49a2-bcee-fc6742fe6d8d)
 Call ID: 38078e68-9acd-49a2-bcee-fc6742fe6d8d
  Args:
    source: Prince_Heinrich_of_Prussia
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1862
  AddLiteral (9e4ec127-9255-4640-8979-35c2f1f0b011)
 Call ID: 9e4ec127-9255-4640-8979-35c2f1f0b011
  Args:
    literal_value: 1929
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: Prince_Heinrich_of_Prussia
  AddTriple (c6f658f1-7a1b-41c8-9db4-ea6f38e16764)
 Call ID: c6f658f1-7a1b-41c8-9db4-ea6f38e16764
  Args:
    target: Wilhelm_II
    relation: :hasBrother
    source: Prince_Heinrich_of_Prussia
  AddTriple (6ed5139e-f0fc-4866-bdfc-57905d93180e)
 Call ID: 6ed5139e-f0fc-4866-bdfc-57905d93180e
  Args:
    relation: :hasFather
    target: Frederick_III
    source: Prince_Heinrich_of_Prussia
  AddTriple (55a1d2c1-c383-46e6-9179-6298c17619e7)
 Call ID: 55a1d2c1-c383-46e6-9179-6298c17619e7
  Args:
    source: Prince_Heinrich_of_Prussia
    relation: :hasMother
    target: Empress_Victoria
  AddTriple (279ccc63-c70d-4055-a9f5-c4303fc53e11)
 Call ID: 279ccc63-c70d-4055-a9f5-c4303fc53e11
  Args:
    source: Empress_Victoria
    target: Queen_Victoria
    relation: :hasMother
  AddTriple (13d29882-938f-4d15-8cae-9db2461e00b3)
 Call ID: 13d29882-938f-4d15-8cae-9db2461e00b3
  Args:
    source: Wilhelm_II
    relation: :hasFather
    target: Frederick_III
  AddTriple (5797bb1b-387b-47f6-95e8-6de41ee62e5a)
 Call ID: 5797bb1b-387b-47f6-95e8-6de41ee62e5a
  Args:
    source: Wilhelm_II
    target: Empress_Victoria
    relation: :hasMother
  AddLiteral (e024eb7f-abaa-4492-9eb4-8b0eeeb02e60)
 Call ID: e024eb7f-abaa-4492-9eb4-8b0eeeb02e60
  Args:
    relation: :hasMarriageYear
    literal_value: 1888
    literal_type: xsd:integer
    source: Prince_Heinrich_of_Prussia
  AddTriple (06c5e9af-5aec-4ddc-bbf9-7d73005fdd7b)
 Call ID: 06c5e9af-5aec-4ddc-bbf9-7d73005fdd7b
  Args:
    source: Prince_Heinrich_of_Prussia
    relation: :hasRelation
    target: Princess_Irene_of_Hesse_and_by_Rhine
  AddTriple (8d039d7d-f576-4c15-8785-af29817fd722)
 Call ID: 8d039d7d-f576-4c15-8785-af29817fd722
  Args:
    source: Prince_Heinrich_of_Prussia
    relation: :hasChild
    target: Waldemar
  AddTriple (331f7724-e99f-4004-8239-ee5712027161)
 Call ID: 331f7724-e99f-4004-8239-ee5712027161
  Args:
    relation: :hasChild
    target: Heinrich_son_of_Henry
    source: Prince_Heinrich_of_Prussia
  AddTriple (363231cd-481b-494d-96c2-3a2746619a7f)
 Call ID: 363231cd-481b-494d-96c2-3a2746619a7f
  Args:
    source: Princess_Irene_of_Hesse_and_by_Rhine
    target: Waldemar
    relation: :hasChild
  AddTriple (5a99c026-6d28-4514-b1da-44118f975bca)
 Call ID: 5a99c026-6d28-4514-b1da-44118f975bca
  Args:
    relation: :hasChild
    target: Heinrich_son_of_Henry
    source: Princess_Irene_of_Hesse_and_by_Rhine
  Finish (ab2035c5-3ac3-45f8-ab81-d83a5cf03c77)
 Call ID: ab2035c5-3ac3-45f8-ab81-d83a5cf03c77
  Args: