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
  AssignClass (a086407d-7ef5-4ed2-b797-f7a6467702e5)
 Call ID: a086407d-7ef5-4ed2-b797-f7a6467702e5
  Args:
    type: :Woman
    source: :Princess_Nina_Georgievna_of_Russia
  AssignClass (fc5d913e-00fb-48d8-b6ec-afdf79aeb81c)
 Call ID: fc5d913e-00fb-48d8-b6ec-afdf79aeb81c
  Args:
    type: :Person
    source: :Princess_Nina_Georgievna_of_Russia
  AddLiteral (aa21b988-2bc0-46ad-abe1-4849dff96ab9)
 Call ID: aa21b988-2bc0-46ad-abe1-4849dff96ab9
  Args:
    source: :Princess_Nina_Georgievna_of_Russia
    literal_type: xsd:integer
    literal_value: 1901
    relation: :hasBirthYear
  AddLiteral (66c959d3-ad4d-40e0-b42b-576cbea5adf3)
 Call ID: 66c959d3-ad4d-40e0-b42b-576cbea5adf3
  Args:
    relation: :hasDeathYear
    literal_value: 1974
    source: :Princess_Nina_Georgievna_of_Russia
    literal_type: xsd:integer
  AssignClass (96349dd9-40d6-4891-ba14-74f3c18f83bb)
 Call ID: 96349dd9-40d6-4891-ba14-74f3c18f83bb
  Args:
    type: :Man
    source: :Grand_Duke_George_Mikhailovich
  AssignClass (6a63b3bd-1856-4569-9b98-1bbada6c3293)
 Call ID: 6a63b3bd-1856-4569-9b98-1bbada6c3293
  Args:
    type: :Person
    source: :Grand_Duke_George_Mikhailovich
  AssignClass (08373e6d-d47c-401e-a6c2-c40898eb14b1)
 Call ID: 08373e6d-d47c-401e-a6c2-c40898eb14b1
  Args:
    type: :Woman
    source: :Grand_Duchess_Maria_Georgievna_of_Russia
  AssignClass (575794b6-3293-4233-b8ba-6b5548617195)
 Call ID: 575794b6-3293-4233-b8ba-6b5548617195
  Args:
    type: :Person
    source: :Grand_Duchess_Maria_Georgievna_of_Russia
  AddTriple (8af23e43-9184-4076-80b0-17c5810a4c37)
 Call ID: 8af23e43-9184-4076-80b0-17c5810a4c37
  Args:
    relation: :hasFather
    source: :Princess_Nina_Georgievna_of_Russia
    target: :Grand_Duke_George_Mikhailovich
  AddTriple (b2cb96ee-b36c-4624-8633-5eef09cc0f3a)
 Call ID: b2cb96ee-b36c-4624-8633-5eef09cc0f3a
  Args:
    source: :Princess_Nina_Georgievna_of_Russia
    relation: :hasMother
    target: :Grand_Duchess_Maria_Georgievna_of_Russia
  AssignClass (2a84f558-2b82-41c3-a3c6-9233efd5bec5)
 Call ID: 2a84f558-2b82-41c3-a3c6-9233efd5bec5
  Args:
    type: :Man
    source: :Prince_Paul_Chavchavadze
  AssignClass (af7a535e-79d4-4137-85b5-fddb816b8813)
 Call ID: af7a535e-79d4-4137-85b5-fddb816b8813
  Args:
    type: :Person
    source: :Prince_Paul_Chavchavadze
  AddLiteral (606e674e-c63e-4d19-a2cd-fea796cf2738)
 Call ID: 606e674e-c63e-4d19-a2cd-fea796cf2738
  Args:
    literal_type: xsd:integer
    source: :Princess_Nina_Georgievna_of_Russia
    relation: :hasMarriageYear
    literal_value: 1922
  AddTriple (a69a1aca-1e9f-4201-82e8-ddc3fd851c57)
 Call ID: a69a1aca-1e9f-4201-82e8-ddc3fd851c57
  Args:
    source: :Princess_Nina_Georgievna_of_Russia
    relation: :hasRelation
    target: :Prince_Paul_Chavchavadze
  AddLiteral (c6c8f20b-f7a4-43c5-9c73-4ea6ddd6e5da)
 Call ID: c6c8f20b-f7a4-43c5-9c73-4ea6ddd6e5da
  Args:
    literal_value: 1899
    relation: :hasBirthYear
    source: :Prince_Paul_Chavchavadze
    literal_type: xsd:integer
  AddLiteral (7fa15e0e-8598-4073-abac-86e7b83e03bd)
 Call ID: 7fa15e0e-8598-4073-abac-86e7b83e03bd
  Args:
    literal_type: xsd:integer
    source: :Prince_Paul_Chavchavadze
    literal_value: 1971
    relation: :hasDeathYear
  AssignClass (b960abdb-cc61-4f07-88a1-ea6079259278)
 Call ID: b960abdb-cc61-4f07-88a1-ea6079259278
  Args:
    type: :Man
    source: :Prince_David_Chavchavadze
  AssignClass (30cb652f-ce21-4c42-a5c8-b7cee728f3bd)
 Call ID: 30cb652f-ce21-4c42-a5c8-b7cee728f3bd
  Args:
    type: :Person
    source: :Prince_David_Chavchavadze
  AddTriple (7e1da9d3-c361-4063-bdfe-163ec41f1d81)
 Call ID: 7e1da9d3-c361-4063-bdfe-163ec41f1d81
  Args:
    target: :Prince_Paul_Chavchavadze
    source: :Prince_David_Chavchavadze
    relation: :hasFather
  AddTriple (466cf8e3-1f3c-41f5-843c-5c255a8f761d)
 Call ID: 466cf8e3-1f3c-41f5-843c-5c255a8f761d
  Args:
    source: :Prince_David_Chavchavadze
    relation: :hasMother
    target: :Princess_Nina_Georgievna_of_Russia
  AssignClass (dedab9d9-07c7-423b-921c-ed985f094b21)
 Call ID: dedab9d9-07c7-423b-921c-ed985f094b21
  Args:
    type: :Woman
    source: :Princess_Xenia
  AssignClass (4612ea9e-6fb0-46c7-9bc5-3a84bf1f3c03)
 Call ID: 4612ea9e-6fb0-46c7-9bc5-3a84bf1f3c03
  Args:
    type: :Person
    source: :Princess_Xenia
  AddTriple (ac9e457e-82f0-435e-8186-60b43a3a3521)
 Call ID: ac9e457e-82f0-435e-8186-60b43a3a3521
  Args:
    target: :Princess_Xenia
    relation: :isSiblingOf
    source: :Princess_Nina_Georgievna_of_Russia
  AssignClass (992be055-835d-44e6-9508-39c3fb19949f)
 Call ID: 992be055-835d-44e6-9508-39c3fb19949f
  Args:
    type: :Man
    source: :Grand_Duke_Michael_Nicolaievich_of_Russia
  AssignClass (7f8df30c-d38f-4eac-82e5-e58bc20740fb)
 Call ID: 7f8df30c-d38f-4eac-82e5-e58bc20740fb
  Args:
    type: :Person
    source: :Grand_Duke_Michael_Nicolaievich_of_Russia
  AddTriple (f5a6f35c-2634-495a-8ee4-1c9567064344)
 Call ID: f5a6f35c-2634-495a-8ee4-1c9567064344
  Args:
    relation: :hasFather
    source: :Grand_Duke_George_Mikhailovich
    target: :Grand_Duke_Michael_Nicolaievich_of_Russia
  Finish (12bc2def-8635-42cf-8a33-7d25e29c8846)
 Call ID: 12bc2def-8635-42cf-8a33-7d25e29c8846
  Args: