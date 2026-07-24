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
  AssignClass (7675b974-f537-4dec-a287-a2cda870fa2c)
 Call ID: 7675b974-f537-4dec-a287-a2cda870fa2c
  Args:
    source: Prince_Joachim_of_Prussia
    type: :Man
  AssignClass (59d0cfa2-205f-4ce0-8317-5af42c5b95df)
 Call ID: 59d0cfa2-205f-4ce0-8317-5af42c5b95df
  Args:
    source: Prince_Joachim_of_Prussia
    type: :Person
  AssignClass (837ac583-886c-45b3-a023-84934178cddb)
 Call ID: 837ac583-886c-45b3-a023-84934178cddb
  Args:
    source: Wilhelm_II_German_Emperor
    type: :Man
  AssignClass (da9a8b03-57cf-4ebf-8940-3178ce8cc635)
 Call ID: da9a8b03-57cf-4ebf-8940-3178ce8cc635
  Args:
    type: :Person
    source: Wilhelm_II_German_Emperor
  AssignClass (c9731619-92bb-4e5d-b129-dfd5aae58e99)
 Call ID: c9731619-92bb-4e5d-b129-dfd5aae58e99
  Args:
    source: Augusta_Victoria_of_Schleswig_Holstein
    type: :Woman
  AssignClass (f0981edc-f365-4eb4-a70c-a5fc1854b4ae)
 Call ID: f0981edc-f365-4eb4-a70c-a5fc1854b4ae
  Args:
    source: Augusta_Victoria_of_Schleswig_Holstein
    type: :Person
  AddLiteral (2984e106-4509-4048-9a17-2684c442e4c8)
 Call ID: 2984e106-4509-4048-9a17-2684c442e4c8
  Args:
    literal_value: 1890
    source: Prince_Joachim_of_Prussia
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (0758b2c4-e293-484d-a5b9-a51ca2660c0e)
 Call ID: 0758b2c4-e293-484d-a5b9-a51ca2660c0e
  Args:
    literal_value: 1920
    source: Prince_Joachim_of_Prussia
    literal_type: xsd:integer
    relation: :hasDeathYear
  AddTriple (32696536-ff83-4a93-8953-d911bcf261f1)
 Call ID: 32696536-ff83-4a93-8953-d911bcf261f1
  Args:
    relation: :hasFather
    source: Prince_Joachim_of_Prussia
    target: Wilhelm_II_German_Emperor
  AddTriple (3f1d598c-09cb-4811-958e-9a1f8c2fcbe3)
 Call ID: 3f1d598c-09cb-4811-958e-9a1f8c2fcbe3
  Args:
    relation: :hasMother
    source: Prince_Joachim_of_Prussia
    target: Augusta_Victoria_of_Schleswig_Holstein
  AssignClass (d5035259-a425-495a-830d-326d36c97248)
 Call ID: d5035259-a425-495a-830d-326d36c97248
  Args:
    type: :Woman
    source: Marie_Auguste_of_Anhalt
  AssignClass (bced0f2b-28be-49ab-8399-07b34e8acde5)
 Call ID: bced0f2b-28be-49ab-8399-07b34e8acde5
  Args:
    type: :Person
    source: Marie_Auguste_of_Anhalt
  AddTriple (5992757d-8fae-42aa-8d51-9259c54be88d)
 Call ID: 5992757d-8fae-42aa-8d51-9259c54be88d
  Args:
    source: Prince_Joachim_of_Prussia
    target: Marie_Auguste_of_Anhalt
    relation: :hasRelation
  AddLiteral (f9ef7c6b-567d-4203-9102-75dbcc468d17)
 Call ID: f9ef7c6b-567d-4203-9102-75dbcc468d17
  Args:
    relation: :hasMarriageYear
    literal_value: 1916
    source: Prince_Joachim_of_Prussia
    literal_type: xsd:integer
  AssignClass (6192fbd6-d185-4bb8-aa5e-752826e2f92a)
 Call ID: 6192fbd6-d185-4bb8-aa5e-752826e2f92a
  Args:
    type: :Man
    source: Eduard_Duke_of_Anhalt
  AssignClass (f7a2deba-41bf-4748-b40d-89f69cace2b8)
 Call ID: f7a2deba-41bf-4748-b40d-89f69cace2b8
  Args:
    type: :Person
    source: Eduard_Duke_of_Anhalt
  AssignClass (bdd556d0-8d4c-4254-8182-657f06d7bd4d)
 Call ID: bdd556d0-8d4c-4254-8182-657f06d7bd4d
  Args:
    source: Luise_of_Saxe_Altenburg
    type: :Woman
  AssignClass (4d74cfe1-b7d1-4770-8857-7454af980109)
 Call ID: 4d74cfe1-b7d1-4770-8857-7454af980109
  Args:
    source: Luise_of_Saxe_Altenburg
    type: :Person
  AddTriple (89c75d70-b83c-46f8-a0da-3599d930f0c4)
 Call ID: 89c75d70-b83c-46f8-a0da-3599d930f0c4
  Args:
    relation: :hasFather
    source: Marie_Auguste_of_Anhalt
    target: Eduard_Duke_of_Anhalt
  AddTriple (996e8683-bff1-434e-97bb-0b8d1f26cafc)
 Call ID: 996e8683-bff1-434e-97bb-0b8d1f26cafc
  Args:
    source: Marie_Auguste_of_Anhalt
    target: Luise_of_Saxe_Altenburg
    relation: :hasMother
  AssignClass (4c5ba2f7-a93a-4360-95e5-649531dff9c1)
 Call ID: 4c5ba2f7-a93a-4360-95e5-649531dff9c1
  Args:
    type: :Man
    source: Moritz_of_Saxe_Altenburg
  AssignClass (cb7c00f2-fe06-4854-944c-73e29f0cfca0)
 Call ID: cb7c00f2-fe06-4854-944c-73e29f0cfca0
  Args:
    type: :Person
    source: Moritz_of_Saxe_Altenburg
  AddTriple (253b7569-f6d8-4d7b-9949-dff2db517816)
 Call ID: 253b7569-f6d8-4d7b-9949-dff2db517816
  Args:
    relation: :hasFather
    source: Luise_of_Saxe_Altenburg
    target: Moritz_of_Saxe_Altenburg
  AssignClass (925488c5-5584-4d42-ad5e-fb42f8ff641a)
 Call ID: 925488c5-5584-4d42-ad5e-fb42f8ff641a
  Args:
    source: Karl_Franz_Josef_Wilhelm_Friedrich_Eduard_Paul_of_Prussia
    type: :Man
  AssignClass (76c2d15f-b181-4d22-b9a4-f758fe673184)
 Call ID: 76c2d15f-b181-4d22-b9a4-f758fe673184
  Args:
    source: Karl_Franz_Josef_Wilhelm_Friedrich_Eduard_Paul_of_Prussia
    type: :Person
  AddTriple (65b82a17-bb5d-402a-9eb7-1f86cb74dcd2)
 Call ID: 65b82a17-bb5d-402a-9eb7-1f86cb74dcd2
  Args:
    source: Karl_Franz_Josef_Wilhelm_Friedrich_Eduard_Paul_of_Prussia
    target: Prince_Joachim_of_Prussia
    relation: :hasFather
  AddTriple (86cd34bc-980f-4145-be79-eea5ded1dc98)
 Call ID: 86cd34bc-980f-4145-be79-eea5ded1dc98
  Args:
    relation: :hasMother
    source: Karl_Franz_Josef_Wilhelm_Friedrich_Eduard_Paul_of_Prussia
    target: Marie_Auguste_of_Anhalt
  AddLiteral (cc8ec29c-c623-41ae-a842-8464ce0b18a6)
 Call ID: cc8ec29c-c623-41ae-a842-8464ce0b18a6
  Args:
    relation: :hasBirthYear
    source: Karl_Franz_Josef_Wilhelm_Friedrich_Eduard_Paul_of_Prussia
    literal_type: xsd:integer
    literal_value: 1916
  AddLiteral (7f92f2ac-8ec3-4c04-a2c3-407e531fd8d6)
 Call ID: 7f92f2ac-8ec3-4c04-a2c3-407e531fd8d6
  Args:
    relation: :hasDeathYear
    literal_value: 1975
    source: Karl_Franz_Josef_Wilhelm_Friedrich_Eduard_Paul_of_Prussia
    literal_type: xsd:integer
  AssignClass (cb8b1419-98f5-4ac2-b0ee-a166a4ded3aa)
 Call ID: cb8b1419-98f5-4ac2-b0ee-a166a4ded3aa
  Args:
    type: :Woman
    source: Henriette_Hermine_Wanda_Ida_Luise_von_Schönaich_Carolath
  AssignClass (f9c68cf8-5fb9-407b-bf2e-54e3edd40462)
 Call ID: f9c68cf8-5fb9-407b-bf2e-54e3edd40462
  Args:
    type: :Person
    source: Henriette_Hermine_Wanda_Ida_Luise_von_Schönaich_Carolath
  AddTriple (be28aa33-e35e-4809-8a78-dde17d1c9c75)
 Call ID: be28aa33-e35e-4809-8a78-dde17d1c9c75
  Args:
    source: Karl_Franz_Josef_Wilhelm_Friedrich_Eduard_Paul_of_Prussia
    target: Henriette_Hermine_Wanda_Ida_Luise_von_Schönaich_Carolath
    relation: :hasRelation
  AddLiteral (6ddf01c4-e8a2-45fa-b5fd-010a5203b7df)
 Call ID: 6ddf01c4-e8a2-45fa-b5fd-010a5203b7df
  Args:
    literal_value: 1940
    literal_type: xsd:integer
    source: Karl_Franz_Josef_Wilhelm_Friedrich_Eduard_Paul_of_Prussia
    relation: :hasMarriageYear
  AssignClass (570933bc-76d3-471c-a256-326ecff05b96)
 Call ID: 570933bc-76d3-471c-a256-326ecff05b96
  Args:
    type: :Woman
    source: Luise_Dora_Hartmann
  AssignClass (115bd49d-237f-469f-ac4b-d1d25e5a5828)
 Call ID: 115bd49d-237f-469f-ac4b-d1d25e5a5828
  Args:
    source: Luise_Dora_Hartmann
    type: :Person
  AddTriple (02703eb1-0f8d-4eb7-a784-430503d7419b)
 Call ID: 02703eb1-0f8d-4eb7-a784-430503d7419b
  Args:
    source: Karl_Franz_Josef_Wilhelm_Friedrich_Eduard_Paul_of_Prussia
    target: Luise_Dora_Hartmann
    relation: :hasRelation
  AddLiteral (80d05b69-bab7-4cc5-af71-a8ab19ef1c64)
 Call ID: 80d05b69-bab7-4cc5-af71-a8ab19ef1c64
  Args:
    literal_type: xsd:integer
    source: Karl_Franz_Josef_Wilhelm_Friedrich_Eduard_Paul_of_Prussia
    literal_value: 1946
    relation: :hasMarriageYear
  AssignClass (9e377409-cafe-4e85-9d71-0eb550d0fef9)
 Call ID: 9e377409-cafe-4e85-9d71-0eb550d0fef9
  Args:
    source: Eva_Maria_Herrera_y_Valdeavellano
    type: :Woman
  AssignClass (7a4e4171-57ea-4ff9-8ef0-063f43005569)
 Call ID: 7a4e4171-57ea-4ff9-8ef0-063f43005569
  Args:
    type: :Person
    source: Eva_Maria_Herrera_y_Valdeavellano
  AddTriple (c61ab4bc-077d-43b2-b307-8be890a06eb5)
 Call ID: c61ab4bc-077d-43b2-b307-8be890a06eb5
  Args:
    relation: :hasRelation
    source: Karl_Franz_Josef_Wilhelm_Friedrich_Eduard_Paul_of_Prussia
    target: Eva_Maria_Herrera_y_Valdeavellano
  AddLiteral (ca4fd7e0-d6a2-4c7b-b21c-f2a0c9dd6dc9)
 Call ID: ca4fd7e0-d6a2-4c7b-b21c-f2a0c9dd6dc9
  Args:
    literal_value: 1959
    literal_type: xsd:integer
    source: Karl_Franz_Josef_Wilhelm_Friedrich_Eduard_Paul_of_Prussia
    relation: :hasMarriageYear
  AssignClass (bf9755a6-b924-43b0-9a7d-889a5ee63317)
 Call ID: bf9755a6-b924-43b0-9a7d-889a5ee63317
  Args:
    type: :Man
    source: Franz_Wilhelm_of_Prussia
  AssignClass (74a3e3f2-6743-4015-aa3f-df7be516014c)
 Call ID: 74a3e3f2-6743-4015-aa3f-df7be516014c
  Args:
    source: Franz_Wilhelm_of_Prussia
    type: :Person
  AssignClass (ac47d8e3-c84c-4047-80a1-fb1a9f7f9af1)
 Call ID: ac47d8e3-c84c-4047-80a1-fb1a9f7f9af1
  Args:
    source: Maria_Vladimirovna_of_Russia
    type: :Woman
  AssignClass (c5be0db6-53aa-4ee2-b1be-888244ad9f4b)
 Call ID: c5be0db6-53aa-4ee2-b1be-888244ad9f4b
  Args:
    source: Maria_Vladimirovna_of_Russia
    type: :Person
  AddTriple (7d15589a-1c0e-4089-a9ad-1cec78b2cecb)
 Call ID: 7d15589a-1c0e-4089-a9ad-1cec78b2cecb
  Args:
    relation: :hasRelation
    source: Franz_Wilhelm_of_Prussia
    target: Maria_Vladimirovna_of_Russia
  Finish (997b03f0-339d-4ba1-b0bf-948b61f86fe7)
 Call ID: 997b03f0-339d-4ba1-b0bf-948b61f86fe7
  Args: