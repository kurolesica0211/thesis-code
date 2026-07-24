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
Princess Nina Georgievna of Russia (Russian: Нина Георгиевна) (20 June 1901 – 27 February 1974), was the elder daughter of Grand Duke George Mikhailovich and Grand Duchess Maria Georgievna of Russia.
A great-granddaughter of Tsar Nicholas I of Russia, she left her native country in 1914, before World War I, finished her education in England, and spent the rest of her life in exile.
In London in 1922, she married Prince Paul Chavchavadze, a descendant of the last king of Georgia.
They had one child, Prince David Chavchavadze, born there two years later.
Princess Nina was an artist, her husband worked as an author; he wrote five books and translated several others.
Their son, Prince David Chavchavadze, served with the U.S. Army during World War II and, thanks in part to his knowledge of Russian, eventually became a CIA officer.
After his retirement, he wrote his memoirs and published those of his grandmother, Grand Duchess George, as well as a book about the grand dukes of Russia.
Early life

Princess Nina was born on June 20  1901 in the New Mikhailovsky Palace on the Palace Embankment in Saint Petersburg, the residence of her paternal grandfather, Grand Duke Michael Nicolaievich of Russia.
She was the elder daughter of Grand Duke George Mikhailovich and Grand Duchess Maria Georgievna of Russia.
Through her father, she was a member of the Romanov family, and princess of the Imperial blood as a great-granddaughter of Tsar Nicholas I of Russia.
Nina's mother was a princess of Greece and Denmark, and on her maternal side, Nina was a granddaughter of King George I of Greece, great-granddaughter of King Christian IX of Denmark and related to members of many European royal families.
Princess Nina spent the first years of her life in the family's apartments at the New Mikhailovsky Palace.
A contemporary of Tsar Nicholas II two youngest daughters, Princess Nina and her only sibling Princess Xenia, played sometimes with them, while they were in the Imperial capital.
The marriage of Nina's parents was unhappy.
Grand Duke George was a devoted father, and the two sisters were close to him, but Grand Duchess Maria Georgievna never liked Russia and eventually became estranged from her husband.
When the war broke out a month after her arrival, the Grand Duchess did not rush back to Russia and later it was too dangerous to attempt a return.
Princess Nina and her sister never saw their father again.
During the turbulent years of World War I and the Russian Revolution, Princess Nina remained living safely in London with her mother and her sister.
Marriage

Princess Nina married Prince Paul Alexandrovich Chavchavadze (1899–1971) on 3 September 1922 in London.
Paul descended from the House of Chavchavadze of the Kakheti province in Georgia, and also, in a direct line, from the last King of Georgia, George XII.
By the time they were married, the world they knew had changed radically, with the collapse of the feudal system in Russia, the rise of the Bolsheviks, and annexation of Georgia by the Soviet Union.
Prince Paul, who also lost his father at the hands of the Bolsheviks, served in the military service on two continents.
The couple had an only child, Prince David Chavchavadze, born in 1924 in London.
In 1927, Princess Nina moved with her family to the United States, where they settled in New York.
Princess Nina was an artist, her husband worked as an author; he wrote five books and translated several others.
Their son, Prince David Chavchavadze, thanks in part to his knowledge of Russian, eventually became a CIA officer.
After his retirement, he wrote a book about the Grand Dukes of Russia.
Princess Nina's husband died in 1971, she outlived him for only a couple of years.



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
  AssignClass (f5b78bdc-8461-4f19-abb0-c5a29d35b55c)
 Call ID: f5b78bdc-8461-4f19-abb0-c5a29d35b55c
  Args:
    type: :Woman
    source: :Princess_Nina_Georgievna_of_Russia
  AssignClass (1ef8bf52-8bb0-40de-96cc-d0ee66bbc1c2)
 Call ID: 1ef8bf52-8bb0-40de-96cc-d0ee66bbc1c2
  Args:
    source: :Princess_Nina_Georgievna_of_Russia
    type: :Person
  AddLiteral (c3634c09-096f-413b-9092-bef15538b74c)
 Call ID: c3634c09-096f-413b-9092-bef15538b74c
  Args:
    literal_value: 1901
    literal_type: xsd:integer
    source: :Princess_Nina_Georgievna_of_Russia
    relation: :hasBirthYear
  AddLiteral (935ece66-95d2-4977-b8d1-78e12e90e592)
 Call ID: 935ece66-95d2-4977-b8d1-78e12e90e592
  Args:
    relation: :hasDeathYear
    source: :Princess_Nina_Georgievna_of_Russia
    literal_type: xsd:integer
    literal_value: 1974
  AssignClass (e855f456-6d63-4132-9133-48a0524cba36)
 Call ID: e855f456-6d63-4132-9133-48a0524cba36
  Args:
    source: :Grand_Duke_George_Mikhailovich
    type: :Man
  AssignClass (ddf1a44a-e0c6-418e-a73d-c870a5c5bda7)
 Call ID: ddf1a44a-e0c6-418e-a73d-c870a5c5bda7
  Args:
    source: :Grand_Duke_George_Mikhailovich
    type: :Person
  AssignClass (ed016ca3-186f-4153-924a-fcd9044c5243)
 Call ID: ed016ca3-186f-4153-924a-fcd9044c5243
  Args:
    type: :Ancestor
    source: :Grand_Duke_George_Mikhailovich
  AssignClass (4aa6f147-8082-47c3-8edf-2101e94e814d)
 Call ID: 4aa6f147-8082-47c3-8edf-2101e94e814d
  Args:
    source: :Grand_Duchess_Maria_Georgievna_of_Russia
    type: :Woman
  AssignClass (89e7b7ab-5e01-4308-8c82-0ff0d7a51f4c)
 Call ID: 89e7b7ab-5e01-4308-8c82-0ff0d7a51f4c
  Args:
    source: :Grand_Duchess_Maria_Georgievna_of_Russia
    type: :Person
  AssignClass (b9b89f10-4ade-4d54-82e0-89b1b3967929)
 Call ID: b9b89f10-4ade-4d54-82e0-89b1b3967929
  Args:
    source: :Grand_Duchess_Maria_Georgievna_of_Russia
    type: :Ancestor
  AddTriple (86a84697-7132-4063-9e61-a9c1d854b982)
 Call ID: 86a84697-7132-4063-9e61-a9c1d854b982
  Args:
    target: :Grand_Duke_George_Mikhailovich
    relation: :hasFather
    source: :Princess_Nina_Georgievna_of_Russia
  AddTriple (cf574f86-5288-44fb-8b11-2ffb1b130038)
 Call ID: cf574f86-5288-44fb-8b11-2ffb1b130038
  Args:
    source: :Princess_Nina_Georgievna_of_Russia
    relation: :hasMother
    target: :Grand_Duchess_Maria_Georgievna_of_Russia
  AssignClass (c0465e82-3d1e-4642-acc3-c25cddfaed62)
 Call ID: c0465e82-3d1e-4642-acc3-c25cddfaed62
  Args:
    source: :Prince_Paul_Chavchavadze
    type: :Man
  AssignClass (84aed711-ea1a-4a4c-beb3-cdb8afedcfda)
 Call ID: 84aed711-ea1a-4a4c-beb3-cdb8afedcfda
  Args:
    source: :Prince_Paul_Chavchavadze
    type: :Person
  AddLiteral (42c3b551-ea6d-4da8-b316-32bcb8c09b89)
 Call ID: 42c3b551-ea6d-4da8-b316-32bcb8c09b89
  Args:
    source: :Princess_Nina_Georgievna_of_Russia
    relation: :hasMarriageYear
    literal_value: 1922
    literal_type: xsd:integer
  AddTriple (818b55d6-175e-4c8b-9cec-6d68a8a6e7b2)
 Call ID: 818b55d6-175e-4c8b-9cec-6d68a8a6e7b2
  Args:
    relation: :hasRelation
    source: :Princess_Nina_Georgievna_of_Russia
    target: :Prince_Paul_Chavchavadze
  AddLiteral (dff62d0c-4075-4a61-a772-1f078baaaef3)
 Call ID: dff62d0c-4075-4a61-a772-1f078baaaef3
  Args:
    literal_value: 1899
    literal_type: xsd:integer
    source: :Prince_Paul_Chavchavadze
    relation: :hasBirthYear
  AddLiteral (238818f8-b2c2-4be0-9dbe-bf7735847d3e)
 Call ID: 238818f8-b2c2-4be0-9dbe-bf7735847d3e
  Args:
    source: :Prince_Paul_Chavchavadze
    relation: :hasDeathYear
    literal_value: 1971
    literal_type: xsd:integer
  AssignClass (ce3a175a-f622-40f2-a2fd-0d4b56c43457)
 Call ID: ce3a175a-f622-40f2-a2fd-0d4b56c43457
  Args:
    source: :Prince_David_Chavchavadze
    type: :Man
  AssignClass (f5335412-bbdb-4b24-89b2-0ccf1bcbdfbd)
 Call ID: f5335412-bbdb-4b24-89b2-0ccf1bcbdfbd
  Args:
    type: :Person
    source: :Prince_David_Chavchavadze
  AddTriple (08245745-142f-474b-abf5-451c541d0d1a)
 Call ID: 08245745-142f-474b-abf5-451c541d0d1a
  Args:
    relation: :hasFather
    source: :Prince_David_Chavchavadze
    target: :Prince_Paul_Chavchavadze
  AddTriple (4dec215b-b122-440c-a2e1-cb52980322cb)
 Call ID: 4dec215b-b122-440c-a2e1-cb52980322cb
  Args:
    target: :Princess_Nina_Georgievna_of_Russia
    source: :Prince_David_Chavchavadze
    relation: :hasMother
  AssignClass (cb706182-8ab3-4c5b-adee-d3ce587fee75)
 Call ID: cb706182-8ab3-4c5b-adee-d3ce587fee75
  Args:
    source: :Princess_Xenia
    type: :Woman
  AssignClass (da38cf06-07a4-4ff0-b87b-2a7c36fc754c)
 Call ID: da38cf06-07a4-4ff0-b87b-2a7c36fc754c
  Args:
    source: :Princess_Xenia
    type: :Person
  AddTriple (4004e3da-6605-4034-9208-df14c804f82c)
 Call ID: 4004e3da-6605-4034-9208-df14c804f82c
  Args:
    source: :Princess_Nina_Georgievna_of_Russia
    relation: :hasSister
    target: :Princess_Xenia
  AddTriple (592a9b3d-eb65-4118-9813-90a5e2021744)
 Call ID: 592a9b3d-eb65-4118-9813-90a5e2021744
  Args:
    source: :Princess_Xenia
    relation: :hasFather
    target: :Grand_Duke_George_Mikhailovich
  AddTriple (8c2b20e6-9fac-49a5-8387-2249a7a68429)
 Call ID: 8c2b20e6-9fac-49a5-8387-2249a7a68429
  Args:
    source: :Princess_Xenia
    relation: :hasMother
    target: :Grand_Duchess_Maria_Georgievna_of_Russia
  AssignClass (47adb363-54b2-41fb-afe1-a35c9859b624)
 Call ID: 47adb363-54b2-41fb-afe1-a35c9859b624
  Args:
    source: :Grand_Duke_Michael_Nicolaievich_of_Russia
    type: :Man
  AssignClass (e8639e15-581b-4228-bda0-80d027d7d692)
 Call ID: e8639e15-581b-4228-bda0-80d027d7d692
  Args:
    source: :Grand_Duke_Michael_Nicolaievich_of_Russia
    type: :Person
  AssignClass (bd46b4fe-65e0-43cb-8e5e-17d7e85fdcb8)
 Call ID: bd46b4fe-65e0-43cb-8e5e-17d7e85fdcb8
  Args:
    type: :Ancestor
    source: :Grand_Duke_Michael_Nicolaievich_of_Russia
  AddTriple (2209884a-864f-4d98-a36e-fd9763778cdb)
 Call ID: 2209884a-864f-4d98-a36e-fd9763778cdb
  Args:
    source: :Grand_Duke_George_Mikhailovich
    relation: :hasFather
    target: :Grand_Duke_Michael_Nicolaievich_of_Russia
  Finish (29a547c1-d271-4745-a3fd-17c627c4a906)
 Call ID: 29a547c1-d271-4745-a3fd-17c627c4a906
  Args: