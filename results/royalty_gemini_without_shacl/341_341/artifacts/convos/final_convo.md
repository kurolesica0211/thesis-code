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
  AssignClass (7681d4f6-25da-475f-b7df-29bc05db7c50)
 Call ID: 7681d4f6-25da-475f-b7df-29bc05db7c50
  Args:
    type: :Man
    source: Prince_Heinrich_of_Prussia
  AssignClass (6992aafd-f093-46b9-b903-d54d5f42ed04)
 Call ID: 6992aafd-f093-46b9-b903-d54d5f42ed04
  Args:
    type: :Person
    source: Prince_Heinrich_of_Prussia
  AddLiteral (cb5d9d2f-f192-45d2-b598-d8a4b22ec487)
 Call ID: cb5d9d2f-f192-45d2-b598-d8a4b22ec487
  Args:
    literal_type: xsd:integer
    literal_value: 1862
    relation: :hasBirthYear
    source: Prince_Heinrich_of_Prussia
  AddLiteral (c19dc27d-d052-4626-a8ce-1187d1e6d571)
 Call ID: c19dc27d-d052-4626-a8ce-1187d1e6d571
  Args:
    source: Prince_Heinrich_of_Prussia
    literal_type: xsd:integer
    literal_value: 1929
    relation: :hasDeathYear
  AssignClass (7950d600-e0ae-43e5-9ec7-561f40732649)
 Call ID: 7950d600-e0ae-43e5-9ec7-561f40732649
  Args:
    type: :Man
    source: Wilhelm_II
  AssignClass (0d1ffece-e49d-4290-8cc8-6a062895fa07)
 Call ID: 0d1ffece-e49d-4290-8cc8-6a062895fa07
  Args:
    source: Wilhelm_II
    type: :Person
  AddTriple (6d610c31-d1a1-4e6f-b48b-67f74c14bc77)
 Call ID: 6d610c31-d1a1-4e6f-b48b-67f74c14bc77
  Args:
    relation: :isBrotherOf
    target: Wilhelm_II
    source: Prince_Heinrich_of_Prussia
  AssignClass (514e0212-fa8b-4aba-bbaf-80098b5efb06)
 Call ID: 514e0212-fa8b-4aba-bbaf-80098b5efb06
  Args:
    type: :Man
    source: Frederick_III
  AssignClass (f70c2ce0-b127-4e39-af59-edac7df71ca6)
 Call ID: f70c2ce0-b127-4e39-af59-edac7df71ca6
  Args:
    type: :Person
    source: Frederick_III
  AssignClass (07b3c130-1d87-4ef1-aecd-427827ffeffc)
 Call ID: 07b3c130-1d87-4ef1-aecd-427827ffeffc
  Args:
    source: Victoria_Princess_Royal
    type: :Woman
  AssignClass (8f058678-3f77-43f9-9f17-9e3eb6a8c245)
 Call ID: 8f058678-3f77-43f9-9f17-9e3eb6a8c245
  Args:
    type: :Person
    source: Victoria_Princess_Royal
  AddTriple (42598581-b1ac-4513-a41c-40d3a86a27ec)
 Call ID: 42598581-b1ac-4513-a41c-40d3a86a27ec
  Args:
    target: Frederick_III
    relation: :hasFather
    source: Prince_Heinrich_of_Prussia
  AddTriple (eaa3d6f2-0cb9-4317-944c-802b53e3e3b4)
 Call ID: eaa3d6f2-0cb9-4317-944c-802b53e3e3b4
  Args:
    relation: :hasMother
    target: Victoria_Princess_Royal
    source: Prince_Heinrich_of_Prussia
  AssignClass (ef80dc76-ee11-4fec-97cb-586164caa576)
 Call ID: ef80dc76-ee11-4fec-97cb-586164caa576
  Args:
    type: :Woman
    source: Queen_Victoria
  AssignClass (9a684d04-df85-4f62-8574-2a6f3ed56024)
 Call ID: 9a684d04-df85-4f62-8574-2a6f3ed56024
  Args:
    type: :Person
    source: Queen_Victoria
  AddTriple (e636f85e-fbfc-47fb-832a-4ea8c7fea155)
 Call ID: e636f85e-fbfc-47fb-832a-4ea8c7fea155
  Args:
    source: Victoria_Princess_Royal
    relation: :hasMother
    target: Queen_Victoria
  AssignClass (456ce125-e210-43fb-bdcf-7472ab0872c4)
 Call ID: 456ce125-e210-43fb-bdcf-7472ab0872c4
  Args:
    source: Princess_Irene_of_Hesse
    type: :Woman
  AssignClass (1ec41f39-1fc5-4339-8ad4-415c51bb83c5)
 Call ID: 1ec41f39-1fc5-4339-8ad4-415c51bb83c5
  Args:
    source: Princess_Irene_of_Hesse
    type: :Person
  AddTriple (7fac588d-bc20-40d2-b1f0-2ae1c37180e3)
 Call ID: 7fac588d-bc20-40d2-b1f0-2ae1c37180e3
  Args:
    source: Prince_Heinrich_of_Prussia
    relation: :hasRelation
    target: Princess_Irene_of_Hesse
  AddLiteral (4941c38a-114f-4e42-9ab4-edd3382091ef)
 Call ID: 4941c38a-114f-4e42-9ab4-edd3382091ef
  Args:
    literal_type: xsd:integer
    literal_value: 1888
    relation: :hasMarriageYear
    source: Prince_Heinrich_of_Prussia
  AssignClass (c1afce8d-18c1-43de-a0b0-0501681db29b)
 Call ID: c1afce8d-18c1-43de-a0b0-0501681db29b
  Args:
    type: :Man
    source: Waldemar
  AssignClass (57a0b658-a48d-4913-85dd-4295abf5db05)
 Call ID: 57a0b658-a48d-4913-85dd-4295abf5db05
  Args:
    type: :Person
    source: Waldemar
  AssignClass (c0ab8f33-8128-4960-b1ae-d99d04a49a74)
 Call ID: c0ab8f33-8128-4960-b1ae-d99d04a49a74
  Args:
    source: Heinrich_son
    type: :Man
  AssignClass (324e1b00-9cf1-4acb-ab93-bf8be2a25a74)
 Call ID: 324e1b00-9cf1-4acb-ab93-bf8be2a25a74
  Args:
    type: :Person
    source: Heinrich_son
  AddTriple (f4eb963d-52d1-4e3e-b6c9-05e6ccba5abf)
 Call ID: f4eb963d-52d1-4e3e-b6c9-05e6ccba5abf
  Args:
    source: Prince_Heinrich_of_Prussia
    target: Waldemar
    relation: :hasChild
  AddTriple (2e2b94dc-d5a7-45f2-98d5-c30493e6c41f)
 Call ID: 2e2b94dc-d5a7-45f2-98d5-c30493e6c41f
  Args:
    source: Prince_Heinrich_of_Prussia
    target: Heinrich_son
    relation: :hasChild
  AddTriple (c039a401-dd27-4bb2-afa0-5fcd192503fd)
 Call ID: c039a401-dd27-4bb2-afa0-5fcd192503fd
  Args:
    source: Waldemar
    target: Princess_Irene_of_Hesse
    relation: :hasMother
  AddTriple (3a69c12e-1128-436b-baab-d7df000a3c6a)
 Call ID: 3a69c12e-1128-436b-baab-d7df000a3c6a
  Args:
    source: Heinrich_son
    relation: :hasMother
    target: Princess_Irene_of_Hesse
  Finish (3b311c95-1b94-4886-acd6-dc654eb326a1)
 Call ID: 3b311c95-1b94-4886-acd6-dc654eb326a1
  Args: