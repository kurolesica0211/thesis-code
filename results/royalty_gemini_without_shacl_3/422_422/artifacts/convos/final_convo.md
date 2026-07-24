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
@prefix ns1: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
@prefix ns2: <http://www.w3.org/2003/11/swrl#> .
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

ns1:isRuleEnabled a owl:AnnotationProperty .

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

:x a ns2:Variable .

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

:y a ns2:Variable .

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

[] a ns2:Imp ;
    rdfs:label "infer hasSon" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasBrother" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasSister" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (4efdaf11-54e0-42f8-9816-aee696a38ea0)
 Call ID: 4efdaf11-54e0-42f8-9816-aee696a38ea0
  Args:
    type: :Man
    source: Prince Karl Emich of Leiningen
  AssignClass (e30d33f9-6db8-446a-950c-b0ae63dc88ad)
 Call ID: e30d33f9-6db8-446a-950c-b0ae63dc88ad
  Args:
    source: Emich, 7th Prince of Leiningen
    type: :Man
  AssignClass (e177c351-e739-4a2d-97c3-b3423a3b90d7)
 Call ID: e177c351-e739-4a2d-97c3-b3423a3b90d7
  Args:
    type: :Woman
    source: Duchess Eilika of the Grand Duchy of Oldenburg
  AssignClass (0710940c-8053-43e4-93bf-1cf64c6939bf)
 Call ID: 0710940c-8053-43e4-93bf-1cf64c6939bf
  Args:
    source: Andreas, 8th Prince of Leiningen
    type: :Man
  AssignClass (9eafdbc0-313c-49e3-b17f-0ac55c47e42f)
 Call ID: 9eafdbc0-313c-49e3-b17f-0ac55c47e42f
  Args:
    type: :Woman
    source: Grand Duchess Maria Kirillovna
  AssignClass (e14dafba-3758-486d-983e-ff03cfea4d44)
 Call ID: e14dafba-3758-486d-983e-ff03cfea4d44
  Args:
    type: :Man
    source: Grand Duke Kirill Vladimirovich
  AssignClass (f743d235-56e7-4422-94ec-eb473a8d9118)
 Call ID: f743d235-56e7-4422-94ec-eb473a8d9118
  Args:
    type: :Man
    source: Emperor Alexander II of Russia
  AssignClass (7a528599-0881-43ea-b858-2a0dd18bab11)
 Call ID: 7a528599-0881-43ea-b858-2a0dd18bab11
  Args:
    type: :Man
    source: Grand Duke Vladimir Kirillovich of Russia
  AssignClass (42ac9a00-32b3-4a46-a387-a04cb1eeb3f6)
 Call ID: 42ac9a00-32b3-4a46-a387-a04cb1eeb3f6
  Args:
    type: :Woman
    source: Princess Margarita of Hohenlohe-Öhringen
  AssignClass (262c177c-d3f2-49bc-bff3-a4f13294c772)
 Call ID: 262c177c-d3f2-49bc-bff3-a4f13294c772
  Args:
    type: :Woman
    source: Princess Cécilia Marie Stephanie Margarita of Leiningen
  AssignClass (75e40c05-8c3a-42e6-93e9-3795dcd2bc18)
 Call ID: 75e40c05-8c3a-42e6-93e9-3795dcd2bc18
  Args:
    type: :Woman
    source: Gabriele Renate Thyssen
  AssignClass (9a697f12-9b5b-4d6b-8635-f1807a1f91e5)
 Call ID: 9a697f12-9b5b-4d6b-8635-f1807a1f91e5
  Args:
    source: Princess Theresa Anna Elisabeth of Leiningen
    type: :Woman
  AssignClass (0de6bcdc-9fab-4cab-8bde-d21eb3c65544)
 Call ID: 0de6bcdc-9fab-4cab-8bde-d21eb3c65544
  Args:
    source: Prince Emich Albrecht Karl of Leiningen
    type: :Man
  AddLiteral (1089fb9f-6c47-4786-a606-679505d2d88f)
 Call ID: 1089fb9f-6c47-4786-a606-679505d2d88f
  Args:
    literal_value: Nikolai Kirillovich Romanov
    relation: :alsoKnownAs
    source: Prince Karl Emich of Leiningen
    literal_type: xsd:string
  AddLiteral (c5d2e6a0-1616-4675-857c-9dd3199dbc52)
 Call ID: c5d2e6a0-1616-4675-857c-9dd3199dbc52
  Args:
    relation: :hasBirthYear
    literal_value: 1952
    source: Prince Karl Emich of Leiningen
    literal_type: xsd:integer
  AddTriple (39bf7e51-c566-45bf-8345-9849084501cd)
 Call ID: 39bf7e51-c566-45bf-8345-9849084501cd
  Args:
    relation: :hasFather
    source: Prince Karl Emich of Leiningen
    target: Emich, 7th Prince of Leiningen
  AddTriple (96a60cc2-cc01-4c16-b256-e66c71c5dbaa)
 Call ID: 96a60cc2-cc01-4c16-b256-e66c71c5dbaa
  Args:
    source: Prince Karl Emich of Leiningen
    target: Duchess Eilika of the Grand Duchy of Oldenburg
    relation: :hasMother
  AddTriple (5054cb6f-3a75-49dc-a679-13712f305d6b)
 Call ID: 5054cb6f-3a75-49dc-a679-13712f305d6b
  Args:
    source: Prince Karl Emich of Leiningen
    target: Andreas, 8th Prince of Leiningen
    relation: :hasBrother
  AddTriple (2046a49f-a494-41d8-83f6-743d1fc2fd4d)
 Call ID: 2046a49f-a494-41d8-83f6-743d1fc2fd4d
  Args:
    source: Prince Karl Emich of Leiningen
    target: Grand Duchess Maria Kirillovna
    relation: :hasMother
  AddTriple (41a9db8a-1c2b-4040-8add-2b1db346e7d3)
 Call ID: 41a9db8a-1c2b-4040-8add-2b1db346e7d3
  Args:
    relation: :hasFather
    source: Grand Duchess Maria Kirillovna
    target: Grand Duke Kirill Vladimirovich
  AddTriple (0d45705e-a4cf-416d-9f24-a7a1471d7414)
 Call ID: 0d45705e-a4cf-416d-9f24-a7a1471d7414
  Args:
    target: Princess Margarita of Hohenlohe-Öhringen
    source: Prince Karl Emich of Leiningen
    relation: :hasFather
  AddTriple (aee1e166-6aa8-4bda-bbab-4e78f53bdf0c)
 Call ID: aee1e166-6aa8-4bda-bbab-4e78f53bdf0c
  Args:
    relation: :hasDaughter
    target: Princess Cécilia Marie Stephanie Margarita of Leiningen
    source: Prince Karl Emich of Leiningen
  AddLiteral (e557b195-847d-482d-b06a-e843d16793ac)
 Call ID: e557b195-847d-482d-b06a-e843d16793ac
  Args:
    literal_type: xsd:integer
    source: Princess Cécilia Marie Stephanie Margarita of Leiningen
    literal_value: 1988
    relation: :hasBirthYear
  AddTriple (5c4d65fe-b030-4e13-8493-75637dbd704f)
 Call ID: 5c4d65fe-b030-4e13-8493-75637dbd704f
  Args:
    target: Gabriele Renate Thyssen
    source: Prince Karl Emich of Leiningen
    relation: :hasFather
  AddTriple (18a348fa-87fa-4127-855e-1b0f4ae13ce7)
 Call ID: 18a348fa-87fa-4127-855e-1b0f4ae13ce7
  Args:
    relation: :hasDaughter
    source: Prince Karl Emich of Leiningen
    target: Princess Theresa Anna Elisabeth of Leiningen
  AddLiteral (3dc7c90c-cd94-48e5-8339-76cbf82e2d62)
 Call ID: 3dc7c90c-cd94-48e5-8339-76cbf82e2d62
  Args:
    literal_type: xsd:integer
    source: Princess Theresa Anna Elisabeth of Leiningen
    relation: :hasBirthYear
    literal_value: 1992
  AddTriple (a06d5e58-98c6-45a4-8b56-6a3a181416a3)
 Call ID: a06d5e58-98c6-45a4-8b56-6a3a181416a3
  Args:
    relation: :hasSon
    target: Prince Emich Albrecht Karl of Leiningen
    source: Prince Karl Emich of Leiningen
  AddLiteral (a3afeb2a-d47e-4382-b5a1-4e6182a40ba8)
 Call ID: a3afeb2a-d47e-4382-b5a1-4e6182a40ba8
  Args:
    literal_type: xsd:integer
    source: Prince Emich Albrecht Karl of Leiningen
    literal_value: 2010
    relation: :hasBirthYear
  Finish (be049b94-3cd9-4cb6-8d5f-234af53e180b)
 Call ID: be049b94-3cd9-4cb6-8d5f-234af53e180b
  Args: