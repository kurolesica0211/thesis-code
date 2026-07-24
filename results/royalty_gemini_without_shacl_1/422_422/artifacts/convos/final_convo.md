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
Prince Nikolai Kirillovich Romanov   Princess Yekaterina Fyodorovna


Prince Karl Emich of Leiningen (German: Karl Emich Nikolaus Friedrich Hermann Prinz zu Leiningen; Russian: Карл Эмих Николаус Фридрих Герман цу Лейнинген; born 12 June 1952), also known by his Orthodox Russian name Nikolai Kirillovich Romanov (Николай Кириллович Романов), and recognized with the regnal name Emperor Nicholas III by Monarchist Party supporters of the Imperial Throne, is the eldest son of Emich, 7th Prince of Leiningen, and Duchess Eilika of the Grand Duchy of Oldenburg, and is an elder brother of Andreas, 8th Prince of Leiningen.
He is a claimant to the defunct throne of the Russian Empire, held until 1917 by the Imperial House of Romanov, as a grandson of Grand Duchess Maria Kirillovna (1907–1951), eldest child of Grand Duke Kirill Vladimirovich, who claimed the Russian crown from exile in 1924.
He is a great-great-great-grandson of Emperor Alexander II of Russia and grandnephew of Grand Duke Vladimir Kirillovich of Russia.
In 2013, the Monarchist Party of Russia declared him the primary heir to the Russian throne upon his conversion from Lutheranism to Eastern Orthodox Christianity, and in 2014 announced the formation of the Imperial Throne, wherein Karl Emich had agreed to assume imperial dignity as Emperor Nicholas III.
As such, however, he came into competition with the widely recognized pretender to the throne, Grand Duchess Maria Vladimirovna of Russia, who is recognized by the Patriarch of Moscow.
He also claimed the headship of the House of Leiningen in the past.
Marriages and children

He married Princess Margarita of Hohenlohe-Öhringen on 8 June 1984.
He had one daughter by this marriage, Princess Cécilia Marie Stephanie Margarita of Leiningen (born 10 June 1988).
Princess Margarita died in 1989 in a car accident.
On 24 May 1991, Prince Karl Emich married morganatically Gabriele Renate Thyssen.
After an inheritance dispute, he desisted claim to the family's legacy in favour of his younger brother Andreas, 8th Prince of Leiningen.
The couple had one daughter, Princess Theresa Anna Elisabeth of Leiningen (born 16 April 1992)
In 1998, Karl Emich and Gabriele were divorced and she became the second wife of the Aga Khan IV.
On 12 April 2010, they had a son, Prince Emich Albrecht Karl of Leiningen.
Because his marriage to Countess Isabelle would not have been deemed equal according to the Pauline Laws, their son, Prince Emich, though considered a dynast of the House of Leiningen, cannot inherit his claim to the headship of the House of Romanov, which shall pass to his brother, Prince Andreas (b. 1955 ), and the latter's descendants born of equal marriages upon the death of Karl Emich, and on the condition that they should convert to Orthodoxy.
Lawsuit


In 2000, Karl Emich began the final round of a lawsuit to inherit £100 million worth of castles, property, and a Mediterranean island that had been denied him by his family because he chose to marry Gabriele Renate Thyssen.
Karl Emich was disinherited shortly after his 1991 wedding, as his mother, father, and brother Andreas withheld approval, contending that the bride did not meet the mediatized family's traditional standard for aristocratic lineage.
The marriage was therefore deemed to constitute a violation of an 1897 Leiningen family edict requiring that dynastically valid marriages be authorised by the head of the Leiningen family (or by successful appeal to a panel of mediatized nobles), such permission historically being granted for brides descended from royalty or the titled nobility.
Karl remarked about the whole affair, 

"From the very beginning of our marriage I was turned into an enemy.
Karl Emich maintained that the stress this feud put upon his marriage is the reason why Thyssen left him, converted to Islam, and eloped with Aga Khan IV.
Claim to the Russian throne

Karl Emich and his supporters argue that the marriage of Maria Vladimirovna's parents was in contravention of the Pauline Laws.
They maintain that the House of Bagration-Mukhrani did not possess sovereign status and was not recognized as equal by Nicholas II for the purpose of dynastic marriages at the time of the union of Princess Tatiana Constantinovna of Russia and Prince Constantine Bagration-Mukhransky in 1911, thirty seven years prior to that of Princess Leonida and Grand Duke Vladimir Kirillovich.
Therefore, as the next of kin to Vladimir (in the exclusion of his daughter), the Russian Monarchist Party recognises Karl Emich as the heir to the Russian throne, since he and his wife converted on 1 June 2013, from Lutheranism to Eastern Orthodox Christianity, enabling his accession.
He outlined that Karl Emich, upon adhering to the Orthodox denomination, obtained a right to take this see according to pre-Revolution Fundamental Laws of the Russian Empire.
Bakov proposed that the Prince accept the throne, thereby forming a new independent state and incorporate it into Bakov's promotional projects such as the Monarchist Party's Imperial Throne micronation and several others.
In April 2014 Bakov and Karl Emich appeared in a newspaper textual and photo report declaring that the Prince accepted the proposals as well as the title of "Emperor Nicholas III" (as successor to Nicholas II).
In the report Bakov emphasized that Karl Emich has long been an entrepreneur but henceforth he would refrain from all non-royalist related public activities.
He also announced that Russian President Vladimir Putin declined to grant such a plot in Yekaterinburg (Bakov's residence and site of the 1918 Romanov assassination) in response to Karl Emich's request, transmitted to Putin by Bakov, a former MP.
In June 2021 Karl Emich, or Nikolai Kirillovich (Nicholas III) gave his first-ever interview in Russian language where he clarified his civil and political attitude and told some details about history of his family.



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
  AssignClass (b6b8170f-cc3e-495e-9622-2ca72c95207b)
 Call ID: b6b8170f-cc3e-495e-9622-2ca72c95207b
  Args:
    type: :Man
    source: Karl_Emich_of_Leiningen
  AssignClass (f629f1fa-f67c-4fcc-afae-fc0610bd18d9)
 Call ID: f629f1fa-f67c-4fcc-afae-fc0610bd18d9
  Args:
    type: :Person
    source: Karl_Emich_of_Leiningen
  AddLiteral (6639ec72-193c-4921-bf0e-ed3447a69475)
 Call ID: 6639ec72-193c-4921-bf0e-ed3447a69475
  Args:
    literal_value: Nikolai Kirillovich Romanov
    literal_type: xsd:string
    source: Karl_Emich_of_Leiningen
    relation: :alsoKnownAs
  AddLiteral (82106ea6-1326-413a-8b5f-bd26acd94e5f)
 Call ID: 82106ea6-1326-413a-8b5f-bd26acd94e5f
  Args:
    literal_type: xsd:string
    source: Karl_Emich_of_Leiningen
    literal_value: Emperor Nicholas III
    relation: :alsoKnownAs
  AddLiteral (156e9788-c283-4fc0-a318-9f51610b606a)
 Call ID: 156e9788-c283-4fc0-a318-9f51610b606a
  Args:
    relation: :hasBirthYear
    literal_value: 1952
    literal_type: xsd:integer
    source: Karl_Emich_of_Leiningen
  AssignClass (8f0bfb33-75f0-4991-a12f-c2c6d6f2179e)
 Call ID: 8f0bfb33-75f0-4991-a12f-c2c6d6f2179e
  Args:
    type: :Man
    source: Emich_7th_Prince_of_Leiningen
  AssignClass (77df7453-7cca-457b-af1f-5ae6a3e9b1aa)
 Call ID: 77df7453-7cca-457b-af1f-5ae6a3e9b1aa
  Args:
    type: :Person
    source: Emich_7th_Prince_of_Leiningen
  AddTriple (174f4113-8db0-44da-ba40-fbfea77c855e)
 Call ID: 174f4113-8db0-44da-ba40-fbfea77c855e
  Args:
    relation: :hasFather
    target: Emich_7th_Prince_of_Leiningen
    source: Karl_Emich_of_Leiningen
  AssignClass (5075a4dc-96fd-42ef-bc43-302b1fa1b30f)
 Call ID: 5075a4dc-96fd-42ef-bc43-302b1fa1b30f
  Args:
    type: :Woman
    source: Duchess_Eilika_of_Oldenburg
  AssignClass (60345bf6-506b-4d92-864e-ad69d47dca32)
 Call ID: 60345bf6-506b-4d92-864e-ad69d47dca32
  Args:
    type: :Person
    source: Duchess_Eilika_of_Oldenburg
  AddTriple (9dae3ab3-1c64-4f94-ba45-cad10092a7cf)
 Call ID: 9dae3ab3-1c64-4f94-ba45-cad10092a7cf
  Args:
    source: Karl_Emich_of_Leiningen
    relation: :hasMother
    target: Duchess_Eilika_of_Oldenburg
  AssignClass (36d72b17-631a-4a5c-ab63-0d53c0cd4abe)
 Call ID: 36d72b17-631a-4a5c-ab63-0d53c0cd4abe
  Args:
    type: :Man
    source: Andreas_8th_Prince_of_Leiningen
  AssignClass (126fc6f7-6aae-4a4b-8b68-db188970c1fa)
 Call ID: 126fc6f7-6aae-4a4b-8b68-db188970c1fa
  Args:
    type: :Person
    source: Andreas_8th_Prince_of_Leiningen
  AddTriple (baec84bc-64a3-4b4c-b060-1c28ba4172fe)
 Call ID: baec84bc-64a3-4b4c-b060-1c28ba4172fe
  Args:
    relation: :isBrotherOf
    target: Karl_Emich_of_Leiningen
    source: Andreas_8th_Prince_of_Leiningen
  AssignClass (abe16e47-1b34-49e0-8f47-0822c572c4a9)
 Call ID: abe16e47-1b34-49e0-8f47-0822c572c4a9
  Args:
    type: :Woman
    source: Grand_Duchess_Maria_Kirillovna
  AssignClass (f4b3997f-9f11-4585-8659-9c24963aa839)
 Call ID: f4b3997f-9f11-4585-8659-9c24963aa839
  Args:
    type: :Person
    source: Grand_Duchess_Maria_Kirillovna
  AddTriple (cad96bb7-de29-404e-97a0-a5b339491195)
 Call ID: cad96bb7-de29-404e-97a0-a5b339491195
  Args:
    relation: :hasAncestor
    target: Grand_Duchess_Maria_Kirillovna
    source: Karl_Emich_of_Leiningen
  AssignClass (363f08d6-41f4-422b-ab76-82ca3ee1db24)
 Call ID: 363f08d6-41f4-422b-ab76-82ca3ee1db24
  Args:
    type: :Woman
    source: Princess_Margarita_of_Hohenlohe-Ohringen
  AssignClass (aeb55ad1-eb8a-4991-aeac-197e9aa7b8c3)
 Call ID: aeb55ad1-eb8a-4991-aeac-197e9aa7b8c3
  Args:
    type: :Person
    source: Princess_Margarita_of_Hohenlohe-Ohringen
  AddTriple (6101ddae-8235-4213-8240-c8a2ed3534c2)
 Call ID: 6101ddae-8235-4213-8240-c8a2ed3534c2
  Args:
    source: Karl_Emich_of_Leiningen
    relation: :hasRelation
    target: Princess_Margarita_of_Hohenlohe-Ohringen
  AddLiteral (772a0bf3-6c96-4fff-a661-bd6ac8ce33d0)
 Call ID: 772a0bf3-6c96-4fff-a661-bd6ac8ce33d0
  Args:
    source: Karl_Emich_of_Leiningen
    literal_type: xsd:integer
    literal_value: 1984
    relation: :hasMarriageYear
  AssignClass (04283766-a2b8-490a-b765-807369696a4d)
 Call ID: 04283766-a2b8-490a-b765-807369696a4d
  Args:
    type: :Woman
    source: Princess_Cecilia_Marie_Stephanie_Margarita_of_Leiningen
  AssignClass (651dde3e-4b41-473c-8771-8686e0cabfbc)
 Call ID: 651dde3e-4b41-473c-8771-8686e0cabfbc
  Args:
    type: :Person
    source: Princess_Cecilia_Marie_Stephanie_Margarita_of_Leiningen
  AddTriple (46aa3e15-d1c3-48a7-ac8a-69aff6172588)
 Call ID: 46aa3e15-d1c3-48a7-ac8a-69aff6172588
  Args:
    source: Princess_Cecilia_Marie_Stephanie_Margarita_of_Leiningen
    relation: :isDaughterOf
    target: Karl_Emich_of_Leiningen
  AddTriple (77a64d78-01cf-4d9f-8de2-37f1b2a49156)
 Call ID: 77a64d78-01cf-4d9f-8de2-37f1b2a49156
  Args:
    relation: :isDaughterOf
    target: Princess_Margarita_of_Hohenlohe-Ohringen
    source: Princess_Cecilia_Marie_Stephanie_Margarita_of_Leiningen
  AssignClass (4f256bf7-cfbb-40c0-9c46-f7885f06b70d)
 Call ID: 4f256bf7-cfbb-40c0-9c46-f7885f06b70d
  Args:
    type: :Woman
    source: Gabriele_Renate_Thyssen
  AssignClass (af62f837-30d9-4da9-b758-e01c8da07dcf)
 Call ID: af62f837-30d9-4da9-b758-e01c8da07dcf
  Args:
    type: :Person
    source: Gabriele_Renate_Thyssen
  AddTriple (ddedcbd3-b87c-42b2-a34b-6ff717fb40a0)
 Call ID: ddedcbd3-b87c-42b2-a34b-6ff717fb40a0
  Args:
    relation: :hasRelation
    target: Gabriele_Renate_Thyssen
    source: Karl_Emich_of_Leiningen
  AddLiteral (e36f7986-2cab-4d7b-9976-c9a77848d2b2)
 Call ID: e36f7986-2cab-4d7b-9976-c9a77848d2b2
  Args:
    source: Karl_Emich_of_Leiningen
    literal_type: xsd:integer
    literal_value: 1991
    relation: :hasMarriageYear
  AssignClass (29bfa90b-f806-4842-822e-fbb97aecc871)
 Call ID: 29bfa90b-f806-4842-822e-fbb97aecc871
  Args:
    type: :Woman
    source: Princess_Theresa_Anna_Elisabeth_of_Leiningen
  AssignClass (9e12d896-409b-45b6-98e7-44790ba16bff)
 Call ID: 9e12d896-409b-45b6-98e7-44790ba16bff
  Args:
    type: :Person
    source: Princess_Theresa_Anna_Elisabeth_of_Leiningen
  AddTriple (44c18401-25c8-4d49-b614-41ea11a5426f)
 Call ID: 44c18401-25c8-4d49-b614-41ea11a5426f
  Args:
    relation: :isDaughterOf
    target: Karl_Emich_of_Leiningen
    source: Princess_Theresa_Anna_Elisabeth_of_Leiningen
  AddTriple (c335af66-2944-45fe-9914-771c119b1892)
 Call ID: c335af66-2944-45fe-9914-771c119b1892
  Args:
    relation: :isDaughterOf
    target: Gabriele_Renate_Thyssen
    source: Princess_Theresa_Anna_Elisabeth_of_Leiningen
  AssignClass (5ac8bc92-799d-4ca2-843e-39a3b1c78911)
 Call ID: 5ac8bc92-799d-4ca2-843e-39a3b1c78911
  Args:
    type: :Man
    source: Prince_Emich_Albrecht_Karl_of_Leiningen
  AssignClass (8b1bd3b9-9d3d-47a8-82e6-516ca9cc39bc)
 Call ID: 8b1bd3b9-9d3d-47a8-82e6-516ca9cc39bc
  Args:
    type: :Person
    source: Prince_Emich_Albrecht_Karl_of_Leiningen
  AddTriple (410a5e84-5149-4399-90bb-9c7b1165649b)
 Call ID: 410a5e84-5149-4399-90bb-9c7b1165649b
  Args:
    relation: :isSonOf
    target: Karl_Emich_of_Leiningen
    source: Prince_Emich_Albrecht_Karl_of_Leiningen
  AddTriple (bdd05af8-612f-40b6-b8a6-74b33511928d)
 Call ID: bdd05af8-612f-40b6-b8a6-74b33511928d
  Args:
    source: Prince_Emich_Albrecht_Karl_of_Leiningen
    relation: :isSonOf
    target: Gabriele_Renate_Thyssen
  Finish (00a50730-1a4f-4799-98e0-1f30f6f4f8db)
 Call ID: 00a50730-1a4f-4799-98e0-1f30f6f4f8db
  Args: