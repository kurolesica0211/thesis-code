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
Prince Joachim Franz Humbert of Prussia (17 December 1890 – 18 July 1920) was the youngest son and sixth child of Wilhelm II, German Emperor, by his first wife, Augusta Victoria of Schleswig-Holstein.
Prince Joachim was educated as an officer and participated in the First World War.
Early life

Birth and family

Prince Joachim was born on 17 December 1890, two years after his father had become the German Emperor, at the Berlin Palace in central Berlin.
He was the sixth and youngest son of Emperor Wilhelm II, and his first wife, Princess Augusta Victoria of Schleswig-Holstein.
Education

Prince Joachim spent his childhood with his siblings at the New Palace in Potsdam, and his school days at the Prinzenhaus in Plön, in his mother's ancestral Schleswig-Holstein, as his brothers had been before him.
Marriage

On 11 March 1916 in Berlin, Joachim married Princess Marie-Auguste of Anhalt (10 June 1898 – 22 May 1983), the daughter of Eduard, Duke of Anhalt and his wife Princess Luise of Saxe-Altenburg (daughter of Prince Moritz of Saxe-Altenburg).
He and Marie-Auguste had been engaged since 14 October of the previous year.
The wedding was celebrated at Bellevue Palace, and was attended by Joachim's father and mother, the Duke and Duchess of Anhalt, as well as other relatives.
The couple had one son, Prince Karl Franz Josef Wilhelm Friedrich Eduard Paul (15 December 1916 in Potsdam – 22 January 1975 in Arica, Chile).
Their grandson, Prince Franz Wilhelm, married Maria Vladimirovna of Russia, a claimant to the Imperial Russian throne.
Candidate for thrones

Ireland

During the Easter Rising in Dublin in 1916, some republican leaders, including Patrick Pearse and Joseph Plunkett, contemplated giving the throne of an independent Ireland to Prince Joachim.
Pearse and Plunkett thought that if the rising were successful and Germany won the First World War, an independent Ireland would be a monarchy with a German prince as king, like Romania and Bulgaria before it.
The fact that Joachim did not speak English was also considered an advantage, as he might be more disposed to learning and promoting the use of the Irish language.
He would naturally turn to those who were more Irish and Gaelic, as to his friends, for the non-nationalist element in our country had shown themselves to be so bitterly anti-German.
For the first generation or so it would be an advantage, in view of our natural weakness, to have a ruler who linked us with a dominant European power, and thereafter, when we were better prepared to stand alone, or when it might be undesirable that our ruler should turn by personal choice to one power rather than be guided by what was most natural and beneficial for our country, the ruler of that time would have become completely Irish."

Ernest Blythe recalled that in January 1915 he heard Plunkett and Thomas MacDonagh express support for the idea at an Irish Volunteers meeting.
Georgia

After Georgia's declaration of independence following the Russian Revolution of 1917, Joachim was briefly considered by the German representative Count Friedrich Werner von der Schulenburg and Georgian royalists as a candidate for the Georgian throne.
The Germans presented various proposals to incorporate Lithuania into the German Empire, particularly Prussia.
One such proposal offered the crown of Lithuania to Joachim.
On 4 June 1918, they voted to offer the Lithuanian throne to the German noble Wilhelm Karl, Duke of Urach.
Divorce and death

Following the German Revolution in November 1918, the Emperor was forced to abdicate, thus depriving Joachim of his titles, position and prospects for heading any newly established monarchies in Europe.
On 31 May 1918, Joachim was examined by the psychiatrist Robert Gaupp, who submitted a report concluding that he "was incurably ill, both mentally and physically ... was extremely easily emotionally and sexually aroused", and "was inclined to 'violent, uncontrollably exploding outbursts of anger in which all self-control  lost'".
The relationship between Joachim and his wife had already started to deteriorate.
According to one report, Marie-Auguste had previously abandoned her husband and child to run away with another man, had been forcibly brought back home on the orders of the Kaiser, but had filed for divorce as soon as the war ended, when she saw that her husband's family were at their lowest ebb.
According to Hans von Gontard, who served as the Kaiser's Hofmarschall in exile, Joachim was "quite out of control and had beaten his wife".
Following the divorce, Joachim shot himself in Potsdam on 18 July 1920.
His own brother Prince Eitel Friedrich of Prussia commented that he suffered from "a fit of excessive dementia".
Kaiser Wilhelm's reaction to the news of his son's suicide was one of fury, commenting that he was outraged "that the oaf should have done this, too, to us and especially to his mother!"
She desperately wanted to believe that his death had been accidental but she knew better.


Children and grandchildren

The only issue of the marriage of Prince Joachim and Princess Marie-Auguste was their son, Prince Karl Franz Josef Wilhelm Friedrich Eduard of Prussia (15 December 1916 – 22 January 1975).
On 5 October 1940, Prince Karl married Princess Henriette Hermine Wanda Ida Luise von Schönaich-Carolath (25 November 1918 –
They were the parents of three children:


After the divorce, Prince Karl married, morganatically, Luise Dora Hartmann (5 September 1909 – 23 April 1961) on 9 November 1946.
Prince Karl's last marriage was to Eva Maria Herrera y Valdeavellano (10 June 1922 – 6 March 1987) on 20 July 1959 in Lima, Peru.
They were married until Prince Karl's death and had two daughters;


Regimental Commissions

Honours

Prince Joachim received the following orders and decorations:
Ancestry

Portrayal in fiction

Prince Joachim was played by American actor Jesse Plemons and portrayed as the main antagonist in the 2021 Disney fantasy adventure film Jungle Cruise.



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
  AssignClass (38886d8c-04de-4bc9-b813-01444229609a)
 Call ID: 38886d8c-04de-4bc9-b813-01444229609a
  Args:
    type: :Man
    source: :PrinceJoachimOfPrussia
  AssignClass (e0d64223-cea5-423c-b0cd-ea9a94e56b91)
 Call ID: e0d64223-cea5-423c-b0cd-ea9a94e56b91
  Args:
    type: :Person
    source: :PrinceJoachimOfPrussia
  AddLiteral (98b99f29-0479-4253-9fd8-4cf11284a7a0)
 Call ID: 98b99f29-0479-4253-9fd8-4cf11284a7a0
  Args:
    source: :PrinceJoachimOfPrussia
    literal_value: 1890
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (cb41a650-7cbc-4c26-a47b-dc371b287773)
 Call ID: cb41a650-7cbc-4c26-a47b-dc371b287773
  Args:
    literal_value: 1920
    source: :PrinceJoachimOfPrussia
    literal_type: xsd:integer
    relation: :hasDeathYear
  AssignClass (05b63a29-6610-4463-a40c-2e15267e48fc)
 Call ID: 05b63a29-6610-4463-a40c-2e15267e48fc
  Args:
    source: :WilhelmII
    type: :Man
  AssignClass (01ba4035-b7e6-4bd4-8022-c725100cd242)
 Call ID: 01ba4035-b7e6-4bd4-8022-c725100cd242
  Args:
    type: :Person
    source: :WilhelmII
  AssignClass (4613e1d6-ee01-4c3a-a4a8-f936b3be2f6d)
 Call ID: 4613e1d6-ee01-4c3a-a4a8-f936b3be2f6d
  Args:
    type: :Woman
    source: :AugustaVictoriaOfSchleswigHolstein
  AssignClass (455c971e-f441-490b-8778-e2d2aa8d051a)
 Call ID: 455c971e-f441-490b-8778-e2d2aa8d051a
  Args:
    type: :Person
    source: :AugustaVictoriaOfSchleswigHolstein
  AddTriple (48afeed7-c42f-4ba8-b455-66de67abf189)
 Call ID: 48afeed7-c42f-4ba8-b455-66de67abf189
  Args:
    source: :PrinceJoachimOfPrussia
    target: :WilhelmII
    relation: :hasFather
  AddTriple (45231e34-dcbe-4c2e-930b-bc5639bda41f)
 Call ID: 45231e34-dcbe-4c2e-930b-bc5639bda41f
  Args:
    source: :PrinceJoachimOfPrussia
    target: :AugustaVictoriaOfSchleswigHolstein
    relation: :hasMother
  AssignClass (4f6c916b-73e9-4198-9e38-e9b3b85fd9b2)
 Call ID: 4f6c916b-73e9-4198-9e38-e9b3b85fd9b2
  Args:
    source: :PrincessMarieAugusteOfAnhalt
    type: :Woman
  AssignClass (ab442618-e26a-4183-9561-752c5fb146cc)
 Call ID: ab442618-e26a-4183-9561-752c5fb146cc
  Args:
    type: :Person
    source: :PrincessMarieAugusteOfAnhalt
  AddLiteral (36518c98-6728-4e44-bb83-3dd9becbbcf4)
 Call ID: 36518c98-6728-4e44-bb83-3dd9becbbcf4
  Args:
    source: :PrinceJoachimOfPrussia
    literal_value: 1916
    relation: :hasMarriageYear
    literal_type: xsd:integer
  AddTriple (10c55831-75ae-40e6-856d-3cfbf2d8f6d0)
 Call ID: 10c55831-75ae-40e6-856d-3cfbf2d8f6d0
  Args:
    relation: :hasRelation
    source: :PrinceJoachimOfPrussia
    target: :PrincessMarieAugusteOfAnhalt
  AssignClass (fa9efcf1-b297-4f80-8d8c-8412819aafd7)
 Call ID: fa9efcf1-b297-4f80-8d8c-8412819aafd7
  Args:
    type: :Man
    source: :EduardDukeOfAnhalt
  AssignClass (c35a02c5-962c-4d1b-bb26-233614335f83)
 Call ID: c35a02c5-962c-4d1b-bb26-233614335f83
  Args:
    type: :Person
    source: :EduardDukeOfAnhalt
  AssignClass (25f2bcc2-deb5-4e5c-b66a-701a13e5a751)
 Call ID: 25f2bcc2-deb5-4e5c-b66a-701a13e5a751
  Args:
    source: :PrincessLuiseOfSaxeAltenburg
    type: :Woman
  AssignClass (781a2885-7b7d-41fe-9b77-37f7633ccd33)
 Call ID: 781a2885-7b7d-41fe-9b77-37f7633ccd33
  Args:
    type: :Person
    source: :PrincessLuiseOfSaxeAltenburg
  AddTriple (c059416c-9934-42fd-99b0-94a19a6ae397)
 Call ID: c059416c-9934-42fd-99b0-94a19a6ae397
  Args:
    source: :PrincessMarieAugusteOfAnhalt
    target: :EduardDukeOfAnhalt
    relation: :hasFather
  AddTriple (91d746f2-9913-49e3-893c-c881d4088fdd)
 Call ID: 91d746f2-9913-49e3-893c-c881d4088fdd
  Args:
    relation: :hasMother
    source: :PrincessMarieAugusteOfAnhalt
    target: :PrincessLuiseOfSaxeAltenburg
  AssignClass (4c0e2565-9902-4c28-b839-dae5b68abb2c)
 Call ID: 4c0e2565-9902-4c28-b839-dae5b68abb2c
  Args:
    type: :Man
    source: :PrinceMoritzOfSaxeAltenburg
  AssignClass (e9fbc8ec-823f-4504-b59b-b411ee32042c)
 Call ID: e9fbc8ec-823f-4504-b59b-b411ee32042c
  Args:
    type: :Person
    source: :PrinceMoritzOfSaxeAltenburg
  AddTriple (a6b790f4-a99a-4d58-ab27-e3f5b8e2620d)
 Call ID: a6b790f4-a99a-4d58-ab27-e3f5b8e2620d
  Args:
    relation: :hasFather
    source: :PrincessLuiseOfSaxeAltenburg
    target: :PrinceMoritzOfSaxeAltenburg
  AssignClass (f43af029-300d-470d-8ca2-3061692cc532)
 Call ID: f43af029-300d-470d-8ca2-3061692cc532
  Args:
    source: :PrinceKarlFranzJosefWilhelmFriedrichEduardPaul
    type: :Man
  AssignClass (4fb2a9e3-4210-4f76-ae5b-5a690ad8bf02)
 Call ID: 4fb2a9e3-4210-4f76-ae5b-5a690ad8bf02
  Args:
    type: :Person
    source: :PrinceKarlFranzJosefWilhelmFriedrichEduardPaul
  AddTriple (5999fc8c-85e9-4cf9-8790-76c9f86a3586)
 Call ID: 5999fc8c-85e9-4cf9-8790-76c9f86a3586
  Args:
    relation: :hasFather
    source: :PrinceKarlFranzJosefWilhelmFriedrichEduardPaul
    target: :PrinceJoachimOfPrussia
  AddTriple (8a941f29-bc0f-493c-9f9f-33d0c9cf0e82)
 Call ID: 8a941f29-bc0f-493c-9f9f-33d0c9cf0e82
  Args:
    source: :PrinceKarlFranzJosefWilhelmFriedrichEduardPaul
    target: :PrincessMarieAugusteOfAnhalt
    relation: :hasMother
  AddLiteral (4a6524b5-69f4-468e-8614-324fbfc9838e)
 Call ID: 4a6524b5-69f4-468e-8614-324fbfc9838e
  Args:
    literal_value: 1916
    source: :PrinceKarlFranzJosefWilhelmFriedrichEduardPaul
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (911f0786-f9a6-40f9-b0a1-3edea9bcd026)
 Call ID: 911f0786-f9a6-40f9-b0a1-3edea9bcd026
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1975
    source: :PrinceKarlFranzJosefWilhelmFriedrichEduardPaul
  AssignClass (18310167-ba50-4d7a-90c5-871a9d13de6a)
 Call ID: 18310167-ba50-4d7a-90c5-871a9d13de6a
  Args:
    type: :Man
    source: :PrinceFranzWilhelm
  AssignClass (5eb0e7ef-5df3-40e3-87e8-a7abe653adce)
 Call ID: 5eb0e7ef-5df3-40e3-87e8-a7abe653adce
  Args:
    type: :Person
    source: :PrinceFranzWilhelm
  AssignClass (91721dd4-4eb9-4e13-a97a-36d4c915cf7f)
 Call ID: 91721dd4-4eb9-4e13-a97a-36d4c915cf7f
  Args:
    type: :Woman
    source: :MariaVladimirovnaOfRussia
  AssignClass (0d58e927-aab7-4254-b5d5-826a4dfe3917)
 Call ID: 0d58e927-aab7-4254-b5d5-826a4dfe3917
  Args:
    type: :Person
    source: :MariaVladimirovnaOfRussia
  AddTriple (03798877-a99c-43b5-a600-26562faccb65)
 Call ID: 03798877-a99c-43b5-a600-26562faccb65
  Args:
    relation: :hasRelation
    source: :PrinceFranzWilhelm
    target: :MariaVladimirovnaOfRussia
  AssignClass (6bd6ef4a-e47d-438d-ac2b-e2725c8349a1)
 Call ID: 6bd6ef4a-e47d-438d-ac2b-e2725c8349a1
  Args:
    source: :PrincessHenrietteHermineWandaIdaLuiseVonSchonaichCarolath
    type: :Woman
  AssignClass (6c239761-efa9-49af-bde6-044fd7f6deb9)
 Call ID: 6c239761-efa9-49af-bde6-044fd7f6deb9
  Args:
    type: :Person
    source: :PrincessHenrietteHermineWandaIdaLuiseVonSchonaichCarolath
  AddTriple (a23e6be1-04e4-4c7f-82b0-9bc755d22f9c)
 Call ID: a23e6be1-04e4-4c7f-82b0-9bc755d22f9c
  Args:
    source: :PrinceKarlFranzJosefWilhelmFriedrichEduardPaul
    target: :PrincessHenrietteHermineWandaIdaLuiseVonSchonaichCarolath
    relation: :hasRelation
  AssignClass (fb29dea0-e68a-4320-9f28-c30ad0ab2412)
 Call ID: fb29dea0-e68a-4320-9f28-c30ad0ab2412
  Args:
    type: :Woman
    source: :LuiseDoraHartmann
  AssignClass (21fc9105-480a-48f4-8ab6-672bb8f6ee4c)
 Call ID: 21fc9105-480a-48f4-8ab6-672bb8f6ee4c
  Args:
    type: :Person
    source: :LuiseDoraHartmann
  AddTriple (7e3d9699-329c-48f3-aec2-e66560b17080)
 Call ID: 7e3d9699-329c-48f3-aec2-e66560b17080
  Args:
    relation: :hasRelation
    source: :PrinceKarlFranzJosefWilhelmFriedrichEduardPaul
    target: :LuiseDoraHartmann
  AssignClass (6cc30fa8-1ede-462b-958f-4f9642e0ff60)
 Call ID: 6cc30fa8-1ede-462b-958f-4f9642e0ff60
  Args:
    type: :Woman
    source: :EvaMariaHerreraYValdeavellano
  AssignClass (817ec81c-5ed1-4ad8-9c62-f161a8752c3a)
 Call ID: 817ec81c-5ed1-4ad8-9c62-f161a8752c3a
  Args:
    source: :EvaMariaHerreraYValdeavellano
    type: :Person
  AddTriple (ae51e3a5-d10c-4e78-9c65-aeedeb0944af)
 Call ID: ae51e3a5-d10c-4e78-9c65-aeedeb0944af
  Args:
    relation: :hasRelation
    source: :PrinceKarlFranzJosefWilhelmFriedrichEduardPaul
    target: :EvaMariaHerreraYValdeavellano
  AssignClass (c8743eb5-bc32-498a-a397-25a9fbee756d)
 Call ID: c8743eb5-bc32-498a-a397-25a9fbee756d
  Args:
    type: :Man
    source: :PrinceEitelFriedrichOfPrussia
  AssignClass (687dda77-499b-468b-b39c-0caa901cfe6d)
 Call ID: 687dda77-499b-468b-b39c-0caa901cfe6d
  Args:
    source: :PrinceEitelFriedrichOfPrussia
    type: :Person
  AddTriple (e9850f6c-2198-404e-a941-497551369a5f)
 Call ID: e9850f6c-2198-404e-a941-497551369a5f
  Args:
    source: :PrinceJoachimOfPrussia
    target: :PrinceEitelFriedrichOfPrussia
    relation: :isSiblingOf
  Finish (90697764-8afa-4024-a4a5-6fdafe6ed186)
 Call ID: 90697764-8afa-4024-a4a5-6fdafe6ed186
  Args: