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
  AssignClass (adcdaa48-2b34-4bbc-b516-14fbfe856766)
 Call ID: adcdaa48-2b34-4bbc-b516-14fbfe856766
  Args:
    type: :Man
    source: :KarlEmichOfLeiningen
  AssignClass (3831bcd5-f8fd-4265-b3a8-cf1e62e0e600)
 Call ID: 3831bcd5-f8fd-4265-b3a8-cf1e62e0e600
  Args:
    type: :Person
    source: :KarlEmichOfLeiningen
  AddLiteral (5a84131a-cb80-4466-be33-a67f6e046dfc)
 Call ID: 5a84131a-cb80-4466-be33-a67f6e046dfc
  Args:
    source: :KarlEmichOfLeiningen
    relation: :hasBirthYear
    literal_value: 1952
    literal_type: xsd:integer
  AddLiteral (95de18a3-6359-4f5f-a1d3-c662015f85ee)
 Call ID: 95de18a3-6359-4f5f-a1d3-c662015f85ee
  Args:
    literal_value: Nikolai Kirillovich Romanov
    literal_type: xsd:string
    source: :KarlEmichOfLeiningen
    relation: :alsoKnownAs
  AssignClass (515c10a4-c2ed-432f-af20-c7845e395fea)
 Call ID: 515c10a4-c2ed-432f-af20-c7845e395fea
  Args:
    source: :Emich7thPrinceOfLeiningen
    type: :Man
  AssignClass (7fd97ce3-328e-4114-8cdc-ea32baa761de)
 Call ID: 7fd97ce3-328e-4114-8cdc-ea32baa761de
  Args:
    type: :Person
    source: :Emich7thPrinceOfLeiningen
  AssignClass (5ef0410a-3657-4088-a89e-a5f81ce28f98)
 Call ID: 5ef0410a-3657-4088-a89e-a5f81ce28f98
  Args:
    source: :DuchessEilikaOfOldenburg
    type: :Woman
  AssignClass (ae187a4e-fd88-4bf7-a506-4b3cd1ab1bab)
 Call ID: ae187a4e-fd88-4bf7-a506-4b3cd1ab1bab
  Args:
    type: :Person
    source: :DuchessEilikaOfOldenburg
  AddTriple (a0ded47a-4283-419a-b21f-31ef8f84652f)
 Call ID: a0ded47a-4283-419a-b21f-31ef8f84652f
  Args:
    target: :Emich7thPrinceOfLeiningen
    relation: :hasFather
    source: :KarlEmichOfLeiningen
  AddTriple (2f64dba2-7f29-43b8-89f7-171711bb6a80)
 Call ID: 2f64dba2-7f29-43b8-89f7-171711bb6a80
  Args:
    target: :DuchessEilikaOfOldenburg
    relation: :hasMother
    source: :KarlEmichOfLeiningen
  AssignClass (adee2718-db0c-4a8b-80c7-af7964e55468)
 Call ID: adee2718-db0c-4a8b-80c7-af7964e55468
  Args:
    source: :Andreas8thPrinceOfLeiningen
    type: :Man
  AssignClass (b778b76a-9fc5-40d4-93ba-9386fb08d77e)
 Call ID: b778b76a-9fc5-40d4-93ba-9386fb08d77e
  Args:
    source: :Andreas8thPrinceOfLeiningen
    type: :Person
  AddTriple (833bb8ea-e956-48dd-abc3-5328078da69e)
 Call ID: 833bb8ea-e956-48dd-abc3-5328078da69e
  Args:
    target: :KarlEmichOfLeiningen
    relation: :isBrotherOf
    source: :Andreas8thPrinceOfLeiningen
  AssignClass (7ea0ac6b-295a-4d61-a575-68709f538a60)
 Call ID: 7ea0ac6b-295a-4d61-a575-68709f538a60
  Args:
    source: :PrincessMargaritaOfHohenloheOhringen
    type: :Woman
  AssignClass (a40fa14e-a392-47b0-a9f1-9149e5188f16)
 Call ID: a40fa14e-a392-47b0-a9f1-9149e5188f16
  Args:
    type: :Person
    source: :PrincessMargaritaOfHohenloheOhringen
  AddLiteral (1d42a038-7b79-4ead-b2bf-7d7623942f95)
 Call ID: 1d42a038-7b79-4ead-b2bf-7d7623942f95
  Args:
    relation: :hasMarriageYear
    source: :KarlEmichOfLeiningen
    literal_type: xsd:integer
    literal_value: 1984
  AddTriple (d4d776dc-9276-4f0e-89fe-5324fbb9ebb4)
 Call ID: d4d776dc-9276-4f0e-89fe-5324fbb9ebb4
  Args:
    target: :PrincessMargaritaOfHohenloheOhringen
    source: :KarlEmichOfLeiningen
    relation: :hasRelation
  AssignClass (3b091383-3fb5-4cbd-a2d2-08341ba13847)
 Call ID: 3b091383-3fb5-4cbd-a2d2-08341ba13847
  Args:
    source: :PrincessCeciliaMarieStephanieMargaritaOfLeiningen
    type: :Woman
  AssignClass (ade6aa63-f3c6-4d4b-af60-dca9972c0083)
 Call ID: ade6aa63-f3c6-4d4b-af60-dca9972c0083
  Args:
    source: :PrincessCeciliaMarieStephanieMargaritaOfLeiningen
    type: :Person
  AddTriple (445c54d2-c173-4a4e-9d0d-a73ef7195352)
 Call ID: 445c54d2-c173-4a4e-9d0d-a73ef7195352
  Args:
    target: :PrincessCeciliaMarieStephanieMargaritaOfLeiningen
    relation: :hasDaughter
    source: :KarlEmichOfLeiningen
  AddTriple (38102cb9-e34f-400d-801d-bfbe609fb8d8)
 Call ID: 38102cb9-e34f-400d-801d-bfbe609fb8d8
  Args:
    source: :PrincessCeciliaMarieStephanieMargaritaOfLeiningen
    relation: :hasMother
    target: :PrincessMargaritaOfHohenloheOhringen
  AddLiteral (06e6507e-960d-41d0-a067-da4e24730aaa)
 Call ID: 06e6507e-960d-41d0-a067-da4e24730aaa
  Args:
    relation: :hasDeathYear
    source: :PrincessMargaritaOfHohenloheOhringen
    literal_type: xsd:integer
    literal_value: 1989
  AssignClass (ddcf020e-c9aa-4739-971e-58d9f11bfeba)
 Call ID: ddcf020e-c9aa-4739-971e-58d9f11bfeba
  Args:
    type: :Woman
    source: :GabrieleRenateThyssen
  AssignClass (ecff8f6f-5711-4d9b-8726-277e3932dd6c)
 Call ID: ecff8f6f-5711-4d9b-8726-277e3932dd6c
  Args:
    type: :Person
    source: :GabrieleRenateThyssen
  AddLiteral (e09959f8-37f3-4f47-968b-d5f4a539f8ee)
 Call ID: e09959f8-37f3-4f47-968b-d5f4a539f8ee
  Args:
    literal_value: 1991
    literal_type: xsd:integer
    source: :KarlEmichOfLeiningen
    relation: :hasMarriageYear
  AddTriple (d9ec7fb1-0ec6-4f8e-addb-57545b5fcd9a)
 Call ID: d9ec7fb1-0ec6-4f8e-addb-57545b5fcd9a
  Args:
    source: :KarlEmichOfLeiningen
    relation: :hasRelation
    target: :GabrieleRenateThyssen
  AssignClass (54b9eeac-9704-47f9-becf-9f200f4cab86)
 Call ID: 54b9eeac-9704-47f9-becf-9f200f4cab86
  Args:
    type: :Woman
    source: :PrincessTheresaAnnaElisabethOfLeiningen
  AssignClass (7253e4e8-14ac-4e2c-8562-c54fba655d25)
 Call ID: 7253e4e8-14ac-4e2c-8562-c54fba655d25
  Args:
    source: :PrincessTheresaAnnaElisabethOfLeiningen
    type: :Person
  AddTriple (fa5a7ef0-cca7-4ed8-8e57-1414ae5b7f4e)
 Call ID: fa5a7ef0-cca7-4ed8-8e57-1414ae5b7f4e
  Args:
    target: :PrincessTheresaAnnaElisabethOfLeiningen
    relation: :hasDaughter
    source: :KarlEmichOfLeiningen
  AddTriple (6daf13b3-c952-476e-81e3-4ca3189ac279)
 Call ID: 6daf13b3-c952-476e-81e3-4ca3189ac279
  Args:
    target: :GabrieleRenateThyssen
    relation: :hasMother
    source: :PrincessTheresaAnnaElisabethOfLeiningen
  AssignClass (e38e2898-e57a-4754-b57b-065c89a177be)
 Call ID: e38e2898-e57a-4754-b57b-065c89a177be
  Args:
    type: :Man
    source: :PrinceEmichAlbrechtKarlOfLeiningen
  AssignClass (47733d23-6ec4-4151-a72f-a30447204435)
 Call ID: 47733d23-6ec4-4151-a72f-a30447204435
  Args:
    type: :Person
    source: :PrinceEmichAlbrechtKarlOfLeiningen
  AddTriple (b174005d-025b-4066-ad29-317ebd3df331)
 Call ID: b174005d-025b-4066-ad29-317ebd3df331
  Args:
    source: :KarlEmichOfLeiningen
    relation: :hasSon
    target: :PrinceEmichAlbrechtKarlOfLeiningen
  AddTriple (48e0c2e5-e5f3-4b9f-9afc-3134ab3abb9e)
 Call ID: 48e0c2e5-e5f3-4b9f-9afc-3134ab3abb9e
  Args:
    target: :GabrieleRenateThyssen
    relation: :hasMother
    source: :PrinceEmichAlbrechtKarlOfLeiningen
  Finish (3b09fcb1-a9d1-4a5d-ac22-ca068743f2f3)
 Call ID: 3b09fcb1-a9d1-4a5d-ac22-ca068743f2f3
  Args: