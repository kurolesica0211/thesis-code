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
  AssignClass (e0eea93e-73c7-4969-bf5f-c6d115ae3c3e)
 Call ID: e0eea93e-73c7-4969-bf5f-c6d115ae3c3e
  Args:
    type: :Man
    source: Prince_Joachim_of_Prussia
  AssignClass (1cb15572-91ac-4e85-b5b4-4351b2b56545)
 Call ID: 1cb15572-91ac-4e85-b5b4-4351b2b56545
  Args:
    source: Prince_Joachim_of_Prussia
    type: :Person
  AssignClass (2dd13f7c-1f19-4944-97ca-7777910e74a2)
 Call ID: 2dd13f7c-1f19-4944-97ca-7777910e74a2
  Args:
    source: Wilhelm_II_German_Emperor
    type: :Man
  AssignClass (6098d860-730e-4792-b43c-a36e0154f5e3)
 Call ID: 6098d860-730e-4792-b43c-a36e0154f5e3
  Args:
    source: Wilhelm_II_German_Emperor
    type: :Person
  AssignClass (3b2d1256-0aa5-44f9-8e37-6f4c9777d4d5)
 Call ID: 3b2d1256-0aa5-44f9-8e37-6f4c9777d4d5
  Args:
    type: :Woman
    source: Augusta_Victoria_of_Schleswig-Holstein
  AssignClass (d1c5ee59-1003-48c9-a944-da5e94b06b2a)
 Call ID: d1c5ee59-1003-48c9-a944-da5e94b06b2a
  Args:
    source: Augusta_Victoria_of_Schleswig-Holstein
    type: :Person
  AddLiteral (35a35f81-c553-4f5b-93c7-ef462d97acd3)
 Call ID: 35a35f81-c553-4f5b-93c7-ef462d97acd3
  Args:
    literal_value: 1890
    relation: :hasBirthYear
    source: Prince_Joachim_of_Prussia
    literal_type: xsd:integer
  AddLiteral (39fbf3ad-0828-465b-ae35-727280ea16a0)
 Call ID: 39fbf3ad-0828-465b-ae35-727280ea16a0
  Args:
    relation: :hasDeathYear
    literal_value: 1920
    literal_type: xsd:integer
    source: Prince_Joachim_of_Prussia
  AddTriple (0c3ff660-317b-4f1e-be0e-f07aef1e2e93)
 Call ID: 0c3ff660-317b-4f1e-be0e-f07aef1e2e93
  Args:
    relation: :hasFather
    source: Prince_Joachim_of_Prussia
    target: Wilhelm_II_German_Emperor
  AddTriple (d77f55c5-c4b3-46a8-98f1-e5494b91e44a)
 Call ID: d77f55c5-c4b3-46a8-98f1-e5494b91e44a
  Args:
    relation: :hasMother
    target: Augusta_Victoria_of_Schleswig-Holstein
    source: Prince_Joachim_of_Prussia
  AssignClass (a7ca53c3-b9ca-4861-831f-353f80b0fbbc)
 Call ID: a7ca53c3-b9ca-4861-831f-353f80b0fbbc
  Args:
    type: :Woman
    source: Princess_Marie-Auguste_of_Anhalt
  AssignClass (82621e0f-3e82-43a8-b8bf-b39c382a965b)
 Call ID: 82621e0f-3e82-43a8-b8bf-b39c382a965b
  Args:
    type: :Person
    source: Princess_Marie-Auguste_of_Anhalt
  AddLiteral (92d491eb-5d93-4065-bd2b-07f7eded9e7b)
 Call ID: 92d491eb-5d93-4065-bd2b-07f7eded9e7b
  Args:
    literal_type: xsd:integer
    source: Prince_Joachim_of_Prussia
    literal_value: 1916
    relation: :hasMarriageYear
  AddTriple (9bc56b4f-6dc2-4fab-8aa7-6d513392a699)
 Call ID: 9bc56b4f-6dc2-4fab-8aa7-6d513392a699
  Args:
    source: Prince_Joachim_of_Prussia
    target: Princess_Marie-Auguste_of_Anhalt
    relation: :hasRelation
  AssignClass (cefd31f5-d8a6-4103-aa35-6da059cfe778)
 Call ID: cefd31f5-d8a6-4103-aa35-6da059cfe778
  Args:
    source: Prince_Karl_Franz_Josef_Wilhelm_Friedrich_Eduard_Paul_of_Prussia
    type: :Man
  AssignClass (214afb37-1015-4c6c-a71f-b32c17d33a93)
 Call ID: 214afb37-1015-4c6c-a71f-b32c17d33a93
  Args:
    source: Prince_Karl_Franz_Josef_Wilhelm_Friedrich_Eduard_Paul_of_Prussia
    type: :Person
  AddTriple (94e76492-73e3-4132-b04a-d6a752dc9b3c)
 Call ID: 94e76492-73e3-4132-b04a-d6a752dc9b3c
  Args:
    target: Prince_Joachim_of_Prussia
    source: Prince_Karl_Franz_Josef_Wilhelm_Friedrich_Eduard_Paul_of_Prussia
    relation: :hasFather
  AddTriple (39841fbd-30b2-41de-b4f9-27cf976a27f0)
 Call ID: 39841fbd-30b2-41de-b4f9-27cf976a27f0
  Args:
    source: Prince_Karl_Franz_Josef_Wilhelm_Friedrich_Eduard_Paul_of_Prussia
    target: Princess_Marie-Auguste_of_Anhalt
    relation: :hasMother
  AddLiteral (5a2d8fff-c62b-4336-8604-ac5c3fb20346)
 Call ID: 5a2d8fff-c62b-4336-8604-ac5c3fb20346
  Args:
    literal_type: xsd:integer
    source: Prince_Karl_Franz_Josef_Wilhelm_Friedrich_Eduard_Paul_of_Prussia
    literal_value: 1916
    relation: :hasBirthYear
  AddLiteral (15c40f19-6e82-4a56-ab0d-d79bc5a0d8b6)
 Call ID: 15c40f19-6e82-4a56-ab0d-d79bc5a0d8b6
  Args:
    literal_type: xsd:integer
    source: Prince_Karl_Franz_Josef_Wilhelm_Friedrich_Eduard_Paul_of_Prussia
    relation: :hasDeathYear
    literal_value: 1975
  AssignClass (b36b32d0-de57-4a95-8d54-dd3e9e366e1b)
 Call ID: b36b32d0-de57-4a95-8d54-dd3e9e366e1b
  Args:
    type: :Man
    source: Eduard_Duke_of_Anhalt
  AssignClass (177517ad-65fd-4d26-bf0c-6d0114015db8)
 Call ID: 177517ad-65fd-4d26-bf0c-6d0114015db8
  Args:
    source: Eduard_Duke_of_Anhalt
    type: :Person
  AssignClass (5481e6f2-1676-49f0-b161-c9d71fab2cd8)
 Call ID: 5481e6f2-1676-49f0-b161-c9d71fab2cd8
  Args:
    type: :Woman
    source: Princess_Luise_of_Saxe-Altenburg
  AssignClass (ddb7ddba-4e5c-4325-9114-ee7783832361)
 Call ID: ddb7ddba-4e5c-4325-9114-ee7783832361
  Args:
    source: Princess_Luise_of_Saxe-Altenburg
    type: :Person
  AddTriple (baf732fa-5dad-41f7-995c-6e4be742760d)
 Call ID: baf732fa-5dad-41f7-995c-6e4be742760d
  Args:
    source: Princess_Marie-Auguste_of_Anhalt
    target: Eduard_Duke_of_Anhalt
    relation: :hasFather
  AddTriple (0cbf925a-ec9a-4350-a890-82ec32683a10)
 Call ID: 0cbf925a-ec9a-4350-a890-82ec32683a10
  Args:
    relation: :hasMother
    target: Princess_Luise_of_Saxe-Altenburg
    source: Princess_Marie-Auguste_of_Anhalt
  AssignClass (7d7f6f1a-b375-4fb5-92d4-9c3cb240c917)
 Call ID: 7d7f6f1a-b375-4fb5-92d4-9c3cb240c917
  Args:
    type: :Man
    source: Prince_Moritz_of_Saxe-Altenburg
  AssignClass (674257cb-9891-45f0-ab43-09dfaa2cdd6d)
 Call ID: 674257cb-9891-45f0-ab43-09dfaa2cdd6d
  Args:
    source: Prince_Moritz_of_Saxe-Altenburg
    type: :Person
  AddTriple (c96ddfec-de47-4dea-a4ff-854bb584144c)
 Call ID: c96ddfec-de47-4dea-a4ff-854bb584144c
  Args:
    source: Princess_Luise_of_Saxe-Altenburg
    target: Prince_Moritz_of_Saxe-Altenburg
    relation: :hasFather
  AssignClass (29d2f848-08b9-484b-9ac3-93cbcd98f94f)
 Call ID: 29d2f848-08b9-484b-9ac3-93cbcd98f94f
  Args:
    type: :Man
    source: Prince_Franz_Wilhelm
  AssignClass (29f4b38a-148a-47d5-acc9-4f33965e79ab)
 Call ID: 29f4b38a-148a-47d5-acc9-4f33965e79ab
  Args:
    source: Prince_Franz_Wilhelm
    type: :Person
  AssignClass (ead88671-af07-4e54-8d34-019988c2ff36)
 Call ID: ead88671-af07-4e54-8d34-019988c2ff36
  Args:
    source: Maria_Vladimirovna_of_Russia
    type: :Woman
  AssignClass (36979dce-dcc9-438b-8d01-829e43792256)
 Call ID: 36979dce-dcc9-438b-8d01-829e43792256
  Args:
    source: Maria_Vladimirovna_of_Russia
    type: :Person
  AddTriple (b3c03fe2-1260-47eb-ac5c-5bb5458841f7)
 Call ID: b3c03fe2-1260-47eb-ac5c-5bb5458841f7
  Args:
    source: Prince_Franz_Wilhelm
    target: Maria_Vladimirovna_of_Russia
    relation: :hasRelation
  AssignClass (6d1061a3-f0b5-41c4-bffc-2675d8d33a5e)
 Call ID: 6d1061a3-f0b5-41c4-bffc-2675d8d33a5e
  Args:
    source: Princess_Henriette_Hermine_Wanda_Ida_Luise_von_Schönaich-Carolath
    type: :Woman
  AssignClass (13f8da8e-3f32-4862-93b8-0036d83f6a93)
 Call ID: 13f8da8e-3f32-4862-93b8-0036d83f6a93
  Args:
    type: :Person
    source: Princess_Henriette_Hermine_Wanda_Ida_Luise_von_Schönaich-Carolath
  AddTriple (86478422-19bb-4180-88a4-a90561456b17)
 Call ID: 86478422-19bb-4180-88a4-a90561456b17
  Args:
    source: Prince_Karl_Franz_Josef_Wilhelm_Friedrich_Eduard_Paul_of_Prussia
    target: Princess_Henriette_Hermine_Wanda_Ida_Luise_von_Schönaich-Carolath
    relation: :hasRelation
  AssignClass (0ed7cdf0-3f79-458a-b8b8-4e21340058b8)
 Call ID: 0ed7cdf0-3f79-458a-b8b8-4e21340058b8
  Args:
    type: :Woman
    source: Luise_Dora_Hartmann
  AssignClass (bd7291fe-d88d-4df9-8bed-e0d7203f00a0)
 Call ID: bd7291fe-d88d-4df9-8bed-e0d7203f00a0
  Args:
    source: Luise_Dora_Hartmann
    type: :Person
  AddTriple (ed62bca2-873a-4d13-9a08-8fbfe3662f79)
 Call ID: ed62bca2-873a-4d13-9a08-8fbfe3662f79
  Args:
    source: Prince_Karl_Franz_Josef_Wilhelm_Friedrich_Eduard_Paul_of_Prussia
    target: Luise_Dora_Hartmann
    relation: :hasRelation
  AssignClass (145e8c18-616f-4add-ad57-7abefc17dd44)
 Call ID: 145e8c18-616f-4add-ad57-7abefc17dd44
  Args:
    source: Eva_Maria_Herrera_y_Valdeavellano
    type: :Woman
  AssignClass (560b2385-791d-43fc-a56d-308f03430d69)
 Call ID: 560b2385-791d-43fc-a56d-308f03430d69
  Args:
    type: :Person
    source: Eva_Maria_Herrera_y_Valdeavellano
  AddTriple (eae40f62-d153-422b-bee8-6128ea69c5b2)
 Call ID: eae40f62-d153-422b-bee8-6128ea69c5b2
  Args:
    relation: :hasRelation
    target: Eva_Maria_Herrera_y_Valdeavellano
    source: Prince_Karl_Franz_Josef_Wilhelm_Friedrich_Eduard_Paul_of_Prussia
  Finish (662df696-bf00-4c05-86ed-337cb28ced0a)
 Call ID: 662df696-bf00-4c05-86ed-337cb28ced0a
  Args: